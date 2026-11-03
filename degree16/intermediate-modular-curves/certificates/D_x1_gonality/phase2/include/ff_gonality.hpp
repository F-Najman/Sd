#pragma once
#include "ff/search.hpp"
#include <variant>

namespace ff {
// Dispatch is shared by the API and CLI. The GMP path supports arbitrary
// characteristics and extension degrees; small fields get compact elements.
template <class Function>
decltype(auto) with_field(const FieldSpec &spec, bool generic, Function &&fn) {
    if (!generic && spec.degree == 1) {
        if (spec.p == 2)
            return fn(PrimeField<2>{});
        if (spec.p == 3)
            return fn(PrimeField<3>{});
        if (spec.p == 5)
            return fn(PrimeField<5>{});
        if (spec.p == 7)
            return fn(PrimeField<7>{});
    }
    PolynomialField field(spec);
    if (!generic && spec.q <= 256)
        return fn(TableField(field));
    return fn(field);
}
using Arithmetic = std::variant<PrimeField<2>, PrimeField<3>, PrimeField<5>, PrimeField<7>,
                                TableField, PolynomialField>;

class Engine {
    Data data_;
    Arithmetic arithmetic_;

  public:
    explicit Engine(const std::string &path)
        : data_(read(path)),
          arithmetic_(
              with_field(data_.field, false, [](auto field) -> Arithmetic { return field; })) {
        std::visit(
            [&](const auto &field) {
                for (const auto &c : data_.checks)
                    require(dimension(data_, field, c.terms) == c.dimension,
                            "Magma dimension check failed");
            },
            arithmetic_);
    }
    const Data &data() const { return data_; }
    Result query(size_t degree, Options options = {}) const {
        options.degree = degree;
        return std::visit([&](const auto &field) { return search(data_, field, options); },
                          arithmetic_);
    }
    bool HasFunctionOfDegreeAtMost(size_t degree, size_t threads = 1) const {
        Options options;
        options.threads = threads;
        auto result = query(degree, options);
        require(result.complete, "search incomplete");
        return result.found;
    }
};
} // namespace ff
