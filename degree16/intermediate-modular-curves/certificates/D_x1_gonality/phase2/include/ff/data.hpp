#pragma once
#include "field.hpp"
#include <algorithm>
#include <fstream>
#include <string>

namespace ff {
using Terms = std::vector<std::pair<size_t, size_t>>;
struct Place {
    size_t degree, limit;
    std::vector<Integer> rows;
};
struct Check {
    size_t dimension;
    Terms terms;
};
struct Data {
    FieldSpec field;
    size_t genus, bound, rational, maxdegree;
    std::vector<Place> places;
    std::vector<Check> checks;
    size_t minimum() const {
        Integer n = (Integer(rational) + field.q) / (field.q + 1);
        return n.get_ui();
    }
};
inline Data read(const std::string &path) {
    std::ifstream in(path);
    require(bool(in), "cannot open export");
    Data d{};
    std::string tag;
    size_t version = 0, count = 0;
    in >> tag >> version >> d.field.p >> d.field.degree >> d.field.q >> d.genus >> d.bound >>
        d.rational >> d.maxdegree >> count;
    require(bool(in) && tag == "FFJETS" && version == 1, "invalid FFJETS header");
    require(d.bound > 0 && d.bound <= 100000 && d.genus <= 100000 && count <= 10000000 &&
                d.rational <= count,
            "invalid dimensions");
    require(d.field.degree > 0 && d.field.degree <= 4096 && d.field.q >= 2, "invalid field header");
    in >> tag;
    require(tag == "POLY", "missing field polynomial");
    d.field.polynomial.resize(d.field.degree + 1);
    for (auto &c : d.field.polynomial)
        in >> c;
    PolynomialField verified(d.field);
    require(d.maxdegree == std::max(size_t(1), d.bound - std::min(d.minimum(), d.bound - 1)),
            "incomplete place degree range");
    in >> tag;
    require(tag == "COUNTS", "missing degree counts");
    std::vector<size_t> counts(d.maxdegree), seen(d.maxdegree);
    size_t total = 0;
    for (auto &c : counts) {
        in >> c;
        require(c <= count, "invalid degree count");
        total += c;
    }
    require(total == count && counts[0] == d.rational, "inconsistent degree counts");
    for (size_t i = 0; i < count; ++i) {
        size_t id = 0;
        Place p{};
        in >> tag >> id >> p.degree >> p.limit;
        require(bool(in) && tag == "PLACE" && id == i && p.degree > 0 && p.degree <= d.maxdegree,
                "invalid place");
        require(i == 0 || p.degree >= d.places.back().degree, "places not sorted");
        size_t budget = d.bound - std::min(d.bound, d.minimum());
        size_t required = p.degree == 1 ? std::max(size_t(2), budget + 1) : budget / p.degree;
        require(p.limit >= required && p.limit > 0 && p.limit <= std::max(size_t(2), d.bound),
                "invalid jet precision");
        require(p.limit * p.degree <= 1000000 && d.genus <= 10000000 / (p.limit * p.degree),
                "oversized matrix");
        p.rows.resize(p.limit * p.degree * d.genus);
        for (auto &v : p.rows) {
            in >> v;
            require(v >= 0 && v < d.field.q, "invalid coefficient encoding");
        }
        require(bool(in), "truncated matrix");
        ++seen[p.degree - 1];
        d.places.push_back(std::move(p));
    }
    require(seen == counts, "place counts disagree");
    bool end = false;
    while (in >> tag) {
        if (tag == "END") {
            end = true;
            break;
        }
        require(tag == "CHECK", "unexpected record");
        Check c{};
        size_t n = 0;
        in >> n >> c.dimension;
        require(n <= count, "invalid check");
        for (size_t j = 0; j < n; ++j) {
            size_t p = 0, m = 0;
            in >> p >> m;
            require(p < count && m > 0 && m <= d.places[p].limit, "invalid check term");
            require(c.terms.empty() || p > c.terms.back().first, "unsorted check");
            c.terms.emplace_back(p, m);
        }
        require(bool(in), "truncated check");
        d.checks.push_back(std::move(c));
    }
    require(end && !(in >> tag), "missing END or trailing data");
    return d;
}
} // namespace ff
