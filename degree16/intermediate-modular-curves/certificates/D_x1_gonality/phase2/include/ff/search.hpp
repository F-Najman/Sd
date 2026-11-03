#pragma once
#include "linear_algebra.hpp"
#include <atomic>
#include <chrono>
#include <cmath>
#include <condition_variable>
#include <deque>
#include <functional>
#include <mutex>
#include <thread>
#include <type_traits>

namespace ff {
using Clock = std::chrono::steady_clock;
struct Options {
    size_t degree = 0, threads = 1;
    int baseline = -1;
    uint64_t vector_budget = 1000000;
    double seconds = 0;
};
struct Statistics {
    uint64_t covers = 0, vectors = 0, nodes = 0, fallbacks = 0;
};
struct Result {
    bool found = false, complete = true;
    size_t baseline = 0;
    Statistics stats;
    Terms witness;
    double seconds = 0;
    Integer expected_covers = 0;
};
inline Integer binomial(size_t n, size_t k) {
    if (k > n)
        return 0;
    k = std::min(k, n - k);
    Integer c = 1;
    for (size_t i = 1; i <= k; ++i) {
        c *= n - k + i;
        c /= i;
    }
    return c;
}
inline Integer count_covers(const Data &d, size_t degree, size_t b) {
    size_t n = d.minimum(), budget = degree - n;
    std::vector<Integer> nonrational(budget + 1);
    nonrational[0] = 1;
    for (size_t p = d.rational; p < d.places.size(); ++p)
        for (size_t j = d.places[p].degree; j <= budget; ++j)
            nonrational[j] += nonrational[j - d.places[p].degree];
    Integer count = 0;
    for (size_t j = 0; j <= budget; ++j) {
        size_t r = degree - j;
        Integer rational = 0;
        if (r < n + b)
            rational = 1;
        else
            for (size_t s = 1; s <= d.rational && (b + 1) * s <= r; ++s) {
                size_t overhead = b * s + (s < n ? n - s : 0);
                if (overhead + s <= r)
                    rational += binomial(d.rational, s) * binomial(r - overhead - 1, s - 1);
            }
        count += nonrational[j] * rational;
    }
    return count;
}
// Cost model includes both cover count and the unavoidable RR nullity of
// the largest cover. It prevents choosing tiny covers with enormous kernels.
inline size_t choose_baseline(const Data &d, size_t degree) {
    if (!d.rational)
        return 0;
    double best = INFINITY;
    size_t chosen = 1;
    size_t limit = std::min(size_t(8), d.places[0].limit);
    for (size_t b = 1; b <= limit; ++b) {
        size_t rows = b * d.rational + degree - d.minimum();
        size_t nullity = rows > d.genus ? rows - d.genus : 0;
        double logq = mpz_sizeinbase(d.field.q.get_mpz_t(), 2) * std::log(2.0);
        double score = std::log(std::max(1.0, count_covers(d, degree, b).get_d())) +
                       std::log(double(std::max(size_t(1), d.genus))) +
                       std::max(0.0, (double(nullity) - 1) * logq);
        if (score < best) {
            best = score;
            chosen = b;
        }
    }
    return chosen;
}

template <class Field, class Visit, class Stop>
void projective_vectors(const Field &f, const Elimination<Field> &e, Visit visit, Stop stop) {
    using E = typename Field::Element;
    // Normalize the last nonzero basis coefficient to 1. Earlier coefficients
    // range over the field; every projective class appears exactly once.
    for (size_t last = 0; last < e.kernel.size() && !stop(); ++last) {
        std::vector<E> value = e.kernel[last];
        std::function<void(size_t)> walk = [&](size_t j) {
            if (stop())
                return;
            if (j == last) {
                visit(value);
                return;
            }
            E previous = 0;
            using Counter = std::remove_cvref_t<decltype(f.order())>;
            Counter order = f.order();
            for (Counter a = 0; a < order && !stop(); ++a) {
                E next = f.from_index(a), delta = f.sub(next, previous);
                if (delta != 0)
                    for (size_t i = 0; i < e.coordinates.size(); ++i)
                        value[i] = f.add(value[i], f.mul(delta, e.kernel[j][i]));
                walk(j + 1);
                previous = next;
            }
            if (previous != 0)
                for (size_t i = 0; i < e.coordinates.size(); ++i)
                    value[i] = f.sub(value[i], f.mul(previous, e.kernel[j][i]));
        };
        walk(0);
    }
}
template <class Field>
Terms pole_divisor(const Elimination<Field> &e, const std::vector<typename Field::Element> &v,
                   size_t place_count) {
    std::vector<size_t> orders(place_count);
    for (size_t j = 0; j < e.coordinates.size(); ++j)
        if (v[j] != 0) {
            auto c = e.coordinates[j];
            orders[c.place] = std::max(orders[c.place], c.order);
        }
    Terms result;
    for (size_t p = 0; p < orders.size(); ++p)
        if (orders[p])
            result.emplace_back(p, orders[p]);
    return result;
}
inline size_t divisor_degree(const Data &d, const Terms &ts) {
    size_t degree = 0;
    for (auto [p, m] : ts)
        degree += m * d.places[p].degree;
    return degree;
}

template <class Field> Result search(const Data &d, const Field &field, Options opt) {
    require(opt.degree <= d.bound, "query exceeds export");
    require(opt.threads >= 1 && opt.threads <= 256, "invalid thread count");
    require(std::isfinite(opt.seconds) && opt.seconds >= 0, "invalid time limit");
    auto started = Clock::now();
    Result result;
    if (opt.degree == 0 || d.minimum() > opt.degree)
        return result;
    size_t b = opt.baseline < 0 ? choose_baseline(d, opt.degree) : size_t(opt.baseline);
    if (!d.rational)
        b = 0;
    require(b <= 8, "invalid baseline");
    for (size_t p = 0; p < d.rational; ++p)
        require(b <= d.places[p].limit, "baseline exceeds precision");
    result.baseline = b;
    std::atomic<bool> stop = false, found = false, timed_out = false;
    std::mutex mutex;
    std::condition_variable readable, writable;
    std::deque<Terms> queue;
    bool done = false;
    std::exception_ptr error;
    auto interrupted = [&]() {
        if (stop.load(std::memory_order_relaxed))
            return true;
        if (opt.seconds > 0 &&
            std::chrono::duration<double>(Clock::now() - started).count() >= opt.seconds) {
            timed_out = true;
            stop = true;
            readable.notify_all();
            writable.notify_all();
            return true;
        }
        return false;
    };
    auto report = [&](Terms witness) {
        std::lock_guard lock(mutex);
        if (!found.exchange(true))
            result.witness = std::move(witness);
        stop = true;
        readable.notify_all();
        writable.notify_all();
    };
    size_t capacity = b ? b * d.rational + opt.degree - d.minimum() : opt.degree;
    auto worker = [&]() {
        Statistics stats;
        try {
            Elimination<Field> e(field, d.genus, capacity);
            for (size_t p = 0; p < d.rational && b; ++p)
                for (size_t m = 1; m <= b; ++m)
                    e.layer(d, p, m);
            const size_t base = e.mark();
            while (true) {
                Terms terms;
                {
                    std::unique_lock lock(mutex);
                    readable.wait(lock, [&] { return done || stop || !queue.empty(); });
                    if (stop || queue.empty())
                        break;
                    terms = std::move(queue.front());
                    queue.pop_front();
                    writable.notify_one();
                }
                if (interrupted())
                    break;
                ++stats.covers;
                if (b) {
                    for (auto [p, m] : terms)
                        for (size_t j = (p < d.rational ? b : 0) + 1; j <= m; ++j)
                            e.layer(d, p, j);
                } else
                    e.terms(d, terms);
                Integer vectors = 0, power = 1;
                for (size_t k = 0; k < e.kernel.size(); ++k) {
                    vectors += power;
                    if (vectors > opt.vector_budget)
                        break;
                    power *= d.field.q;
                }
                if (vectors <= opt.vector_budget) {
                    projective_vectors(
                        field, e,
                        [&](const auto &v) {
                            ++stats.vectors;
                            // A nonzero coordinate needs at least one slot in the
                            // degree-weighted pole divisor, over every finite field.
                            size_t weight = 0;
                            for (size_t j = 0; j < e.coordinates.size(); ++j)
                                if (v[j] != 0)
                                    ++weight;
                            if (weight > opt.degree)
                                return;
                            auto poles = pole_divisor(e, v, d.places.size());
                            if (divisor_degree(d, poles) <= opt.degree)
                                report(std::move(poles));
                        },
                        interrupted);
                } else {
                    ++stats.fallbacks;
                    Terms caps;
                    std::vector<size_t> limits(d.places.size());
                    for (auto c : e.coordinates)
                        limits[c.place] = std::max(limits[c.place], c.order);
                    for (size_t p = 0; p < limits.size(); ++p)
                        if (limits[p])
                            caps.emplace_back(p, limits[p]);
                    Elimination<Field> sub(field, d.genus, opt.degree);
                    Terms chosen;
                    std::function<void(size_t, size_t)> descend = [&](size_t begin, size_t degree) {
                        ++stats.nodes;
                        if (interrupted())
                            return;
                        if (!sub.kernel.empty()) {
                            report(chosen);
                            return;
                        }
                        for (size_t i = begin; i < caps.size() && !stop; ++i) {
                            auto [p, limit] = caps[i];
                            size_t mark = sub.mark();
                            for (size_t m = 1;
                                 m <= limit && degree + m * d.places[p].degree <= opt.degree &&
                                 !stop;
                                 ++m) {
                                sub.layer(d, p, m);
                                chosen.emplace_back(p, m);
                                descend(i + 1, degree + m * d.places[p].degree);
                                chosen.pop_back();
                            }
                            sub.rollback(mark);
                        }
                    };
                    descend(0, 0);
                }
                e.rollback(base);
            }
        } catch (...) {
            std::lock_guard lock(mutex);
            if (!error)
                error = std::current_exception();
            stop = true;
            readable.notify_all();
            writable.notify_all();
        }
        std::lock_guard lock(mutex);
        result.stats.covers += stats.covers;
        result.stats.vectors += stats.vectors;
        result.stats.nodes += stats.nodes;
        result.stats.fallbacks += stats.fallbacks;
    };
    std::vector<std::thread> workers;
    for (size_t t = 0; t < opt.threads; ++t)
        workers.emplace_back(worker);
    auto push = [&](const Terms &terms) {
        if (interrupted())
            return;
        std::unique_lock lock(mutex);
        writable.wait(lock, [&] { return stop || queue.size() < 256; });
        if (!stop) {
            queue.push_back(terms);
            readable.notify_one();
        }
    };
    try {
        Terms terms;
        if (!b) {
            // No rational point: do not pad to degree d, since that could miss
            // smaller degrees. Enumerate every effective divisor up to d.
            std::function<void(size_t, size_t)> direct = [&](size_t begin, size_t degree) {
                if (interrupted())
                    return;
                if (degree)
                    push(terms);
                for (size_t p = begin; p < d.places.size() && !stop; ++p)
                    for (size_t m = 1; m <= d.places[p].limit &&
                                       degree + m * d.places[p].degree <= opt.degree && !stop;
                         ++m) {
                        terms.emplace_back(p, m);
                        direct(p + 1, degree + m * d.places[p].degree);
                        terms.pop_back();
                    }
            };
            direct(0, 0);
        } else {
            const size_t n = d.minimum();
            std::function<void(size_t, size_t, size_t, size_t)> excess =
                [&](size_t begin, size_t support, size_t sum, size_t budget) {
                    if (interrupted())
                        return;
                    size_t cost = sum + b * support + (support < n ? n - support : 0);
                    if (cost == budget) {
                        push(terms);
                        return;
                    }
                    size_t next = b + 1 - (support < n ? 1 : 0);
                    if (cost + next > budget)
                        return;
                    for (size_t p = begin; p < d.rational && !stop; ++p)
                        for (size_t m = 1;
                             m <= d.places[p].limit - b && cost + next + m - 1 <= budget && !stop;
                             ++m) {
                            terms.emplace_back(p, b + m);
                            excess(p + 1, support + 1, sum + m, budget);
                            terms.pop_back();
                        }
                };
            std::function<void(size_t, size_t)> nonrational = [&](size_t begin, size_t degree) {
                if (interrupted())
                    return;
                size_t budget = opt.degree - degree;
                if (budget < n + b)
                    push(terms);
                else
                    excess(0, 0, 0, budget);
                for (size_t p = begin; p < d.places.size() && !stop; ++p)
                    for (size_t m = 1; m <= d.places[p].limit &&
                                       degree + m * d.places[p].degree <= opt.degree - n && !stop;
                         ++m) {
                        terms.emplace_back(p, m);
                        nonrational(p + 1, degree + m * d.places[p].degree);
                        terms.pop_back();
                    }
            };
            nonrational(d.rational, 0);
        }
    } catch (...) {
        std::lock_guard lock(mutex);
        if (!error)
            error = std::current_exception();
        stop = true;
    }
    {
        std::lock_guard lock(mutex);
        done = true;
    }
    readable.notify_all();
    writable.notify_all();
    for (auto &t : workers)
        t.join();
    if (error)
        std::rethrow_exception(error);
    result.found = found;
    result.complete = found || !timed_out;
    if (found)
        require(dimension(d, field, result.witness) > 1 &&
                    divisor_degree(d, result.witness) <= opt.degree,
                "independent witness check failed");
    if (b && result.complete && !found) {
        result.expected_covers = count_covers(d, opt.degree, b);
        require(result.expected_covers == result.stats.covers, "cover exhaustion audit failed");
    }
    result.seconds = std::chrono::duration<double>(Clock::now() - started).count();
    return result;
}
} // namespace ff
