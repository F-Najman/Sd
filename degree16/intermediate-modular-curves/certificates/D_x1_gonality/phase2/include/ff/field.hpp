#pragma once
#include <cstdint>
#include <gmpxx.h>
#include <stdexcept>
#include <utility>
#include <vector>

namespace ff {
inline void require(bool ok, const char *message) {
    if (!ok)
        throw std::runtime_error(message);
}
using Integer = mpz_class;
inline Integer mod(Integer a, const Integer &p) {
    mpz_mod(a.get_mpz_t(), a.get_mpz_t(), p.get_mpz_t());
    return a;
}
// Canonical element encoding: sum a_i p^i for the polynomial basis
// 1,z,...,z^(r-1). This is independent of Magma's printed generator names.
struct FieldSpec {
    Integer p, q;
    size_t degree;
    std::vector<Integer> polynomial;
};
class PolynomialField {
    FieldSpec spec_;
    std::vector<Integer> decode(Integer a) const {
        std::vector<Integer> v(spec_.degree);
        for (auto &x : v) {
            x = a % spec_.p;
            a /= spec_.p;
        }
        return v;
    }
    Integer encode(const std::vector<Integer> &v) const {
        Integer a = 0;
        for (size_t i = v.size(); i-- > 0;) {
            a *= spec_.p;
            a += mod(v[i], spec_.p);
        }
        return a;
    }

  public:
    using Element = Integer;
    explicit PolynomialField(FieldSpec spec) : spec_(std::move(spec)) {
        require(spec_.degree > 0 && spec_.degree <= 4096, "invalid extension degree");
        require(spec_.p >= 2 && mpz_probab_prime_p(spec_.p.get_mpz_t(), 40) != 0,
                "invalid field characteristic");
        Integer q;
        mpz_pow_ui(q.get_mpz_t(), spec_.p.get_mpz_t(), spec_.degree);
        require(q == spec_.q, "inconsistent field order");
        require(spec_.polynomial.size() == spec_.degree + 1 && spec_.polynomial.back() == 1,
                "field polynomial must be monic");
        for (auto &c : spec_.polynomial)
            require(c >= 0 && c < spec_.p, "invalid polynomial coefficient");
        // Rabin irreducibility criterion. Prime characteristic is also certified
        // by the trusted Magma producer; GMP provides an extra corruption check.
        if (spec_.degree > 1) {
            Integer x = spec_.p, y = x;
            for (size_t i = 1; i <= spec_.degree; ++i) {
                y = power(y, spec_.p);
                if (i <= spec_.degree / 2 && spec_.degree % i == 0) {
                    auto b = decode(sub(y, x));
                    auto a = spec_.polynomial;
                    auto trim = [](auto &v) {
                        while (!v.empty() && v.back() == 0)
                            v.pop_back();
                    };
                    trim(b);
                    while (!b.empty()) {
                        Integer inv;
                        require(
                            mpz_invert(inv.get_mpz_t(), b.back().get_mpz_t(), spec_.p.get_mpz_t()),
                            "noninvertible coefficient");
                        while (a.size() >= b.size()) {
                            size_t shift = a.size() - b.size();
                            Integer c = mod(a.back() * inv, spec_.p);
                            for (size_t j = 0; j < b.size(); ++j)
                                a[j + shift] = mod(a[j + shift] - c * b[j], spec_.p);
                            trim(a);
                        }
                        a.swap(b);
                    }
                    require(a.size() == 1, "reducible field polynomial");
                }
            }
            require(y == x, "reducible field polynomial");
        }
    }
    const Integer &order() const { return spec_.q; }
    Element from_integer(const Integer &a) const {
        require(a >= 0 && a < spec_.q, "invalid field element");
        return a;
    }
    Element from_index(const Integer &a) const { return a; }
    Element add(const Element &a, const Element &b) const {
        if (spec_.degree == 1)
            return mod(a + b, spec_.p);
        auto x = decode(a), y = decode(b);
        for (size_t i = 0; i < x.size(); ++i)
            x[i] += y[i];
        return encode(x);
    }
    Element sub(const Element &a, const Element &b) const {
        if (spec_.degree == 1)
            return mod(a - b, spec_.p);
        auto x = decode(a), y = decode(b);
        for (size_t i = 0; i < x.size(); ++i)
            x[i] -= y[i];
        return encode(x);
    }
    Element mul(const Element &a, const Element &b) const {
        if (a == 0 || b == 0)
            return 0;
        if (spec_.degree == 1)
            return mod(a * b, spec_.p);
        auto x = decode(a), y = decode(b);
        const size_t r = spec_.degree;
        std::vector<Integer> z(2 * r - 1);
        for (size_t i = 0; i < r; ++i)
            for (size_t j = 0; j < r; ++j)
                z[i + j] += x[i] * y[j];
        for (size_t i = z.size(); i-- > r;) {
            Integer c = mod(z[i], spec_.p);
            for (size_t j = 0; j < r; ++j)
                z[i - r + j] -= c * spec_.polynomial[j];
        }
        z.resize(r);
        return encode(z);
    }
    Element power(Element a, Integer n) const {
        Element b = 1;
        while (n > 0) {
            if (mpz_odd_p(n.get_mpz_t()))
                b = mul(b, a);
            n >>= 1;
            if (n > 0)
                a = mul(a, a);
        }
        return b;
    }
    Element inverse(const Element &a) const {
        require(a != 0, "division by zero");
        return power(a, spec_.q - 2);
    }
};

// Constant moduli let the compiler replace division with multiply/shift.
template <uint32_t P> struct PrimeField {
    using Element = uint32_t;
    constexpr uint32_t order() const { return P; }
    Element from_integer(const Integer &a) const {
        require(a >= 0 && a < P, "invalid field element");
        return a.get_ui();
    }
    static constexpr Element from_index(uint32_t a) { return a; }
    static constexpr Element add(Element a, Element b) { return (a + b) % P; }
    static constexpr Element sub(Element a, Element b) { return (a + P - b) % P; }
    static constexpr Element mul(Element a, Element b) { return (uint64_t(a) * b) % P; }
    static constexpr Element inverse(Element a) {
        if (!a)
            throw std::runtime_error("division by zero");
        Element b = 1;
        uint32_t n = P - 2;
        while (n) {
            if (n & 1)
                b = mul(b, a);
            a = mul(a, a);
            n >>= 1;
        }
        return b;
    }
};

// Small extension fields use dense operation tables (<= 256 KiB each).
class TableField {
    uint32_t q_;
    std::vector<uint32_t> add_, sub_, mul_, inv_;

  public:
    using Element = uint32_t;
    explicit TableField(const PolynomialField &f)
        : q_(f.order().get_ui()), add_(q_ * q_), sub_(q_ * q_), mul_(q_ * q_), inv_(q_) {
        require(f.order() <= 256, "table field too large");
        for (uint32_t a = 0; a < q_; ++a) {
            if (a)
                inv_[a] = f.inverse(Integer(a)).get_ui();
            for (uint32_t b = 0; b < q_; ++b) {
                add_[a * q_ + b] = f.add(Integer(a), Integer(b)).get_ui();
                sub_[a * q_ + b] = f.sub(Integer(a), Integer(b)).get_ui();
                mul_[a * q_ + b] = f.mul(Integer(a), Integer(b)).get_ui();
            }
        }
    }
    uint32_t order() const { return q_; }
    Element from_integer(const Integer &a) const {
        require(a >= 0 && a < q_, "invalid field element");
        return a.get_ui();
    }
    Element from_index(uint32_t a) const { return a; }
    Element add(Element a, Element b) const { return add_[a * q_ + b]; }
    Element sub(Element a, Element b) const { return sub_[a * q_ + b]; }
    Element mul(Element a, Element b) const { return mul_[a * q_ + b]; }
    Element inverse(Element a) const {
        require(a != 0, "division by zero");
        return inv_[a];
    }
};
} // namespace ff
