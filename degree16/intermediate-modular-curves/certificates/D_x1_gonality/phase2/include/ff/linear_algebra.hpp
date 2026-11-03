#pragma once
#include "data.hpp"
namespace ff {
struct Coordinate {
    size_t place, order;
};
// Immutable old pivots allow cheap rollback. Dependency vectors are expressed
// in ORIGINAL ordered jet slots: arbitrary row compression would lose poles.
template <class Field> class Elimination {
  public:
    using E = typename Field::Element;
    const Field &field;
    size_t genus, capacity, rank = 0;
    std::vector<std::vector<E>> pivots, labels, kernel;
    std::vector<int> history;
    std::vector<Coordinate> coordinates;
    Elimination(const Field &f, size_t g, size_t cap)
        : field(f), genus(g), capacity(cap), pivots(g), labels(g) {
        coordinates.reserve(cap);
        history.reserve(cap);
    }
    size_t mark() const { return history.size(); }
    void append(std::vector<E> row, Coordinate c) {
        size_t slot = mark();
        require(slot < capacity, "coordinate capacity exceeded");
        std::vector<E> label(capacity);
        label[slot] = 1;
        for (size_t j = 0; j < genus; ++j)
            if (row[j] != 0) {
                if (pivots[j].empty()) {
                    E inv = field.inverse(row[j]);
                    for (size_t i = j; i < genus; ++i)
                        row[i] = field.mul(row[i], inv);
                    for (size_t i = 0; i <= slot; ++i)
                        label[i] = field.mul(label[i], inv);
                    pivots[j] = std::move(row);
                    labels[j] = std::move(label);
                    history.push_back(int(j));
                    coordinates.push_back(c);
                    ++rank;
                    return;
                }
                E a = row[j];
                for (size_t i = j; i < genus; ++i)
                    row[i] = field.sub(row[i], field.mul(a, pivots[j][i]));
                for (size_t i = 0; i <= slot; ++i)
                    label[i] = field.sub(label[i], field.mul(a, labels[j][i]));
            }
        history.push_back(-1);
        coordinates.push_back(c);
        kernel.push_back(std::move(label));
    }
    void layer(const Data &d, size_t p, size_t m) {
        const auto &place = d.places[p];
        require(m > 0 && m <= place.limit, "missing jet precision");
        for (size_t j = (m - 1) * place.degree; j < m * place.degree; ++j) {
            std::vector<E> row(genus);
            for (size_t k = 0; k < genus; ++k)
                row[k] = field.from_integer(place.rows[j * genus + k]);
            append(std::move(row), {p, m});
        }
    }
    void terms(const Data &d, const Terms &ts) {
        for (auto [p, m] : ts)
            for (size_t j = 1; j <= m; ++j)
                layer(d, p, j);
    }
    void rollback(size_t mark) {
        while (history.size() > mark) {
            int j = history.back();
            history.pop_back();
            coordinates.pop_back();
            if (j < 0)
                kernel.pop_back();
            else {
                pivots[j].clear();
                labels[j].clear();
                --rank;
            }
        }
    }
};
// Separate batch Gaussian elimination for export checks and final witnesses.
// This deliberately does not call the incremental elimination implementation.
template <class Field> size_t dimension(const Data &d, const Field &f, const Terms &ts) {
    using E = typename Field::Element;
    std::vector<std::vector<E>> a;
    for (auto [p, m] : ts) {
        require(p < d.places.size() && m > 0 && m <= d.places[p].limit, "invalid divisor");
        for (size_t j = 0; j < m * d.places[p].degree; ++j) {
            std::vector<E> row(d.genus);
            for (size_t k = 0; k < d.genus; ++k)
                row[k] = f.from_integer(d.places[p].rows[j * d.genus + k]);
            a.push_back(std::move(row));
        }
    }
    size_t rank = 0;
    for (size_t c = 0; c < d.genus && rank < a.size(); ++c) {
        size_t p = rank;
        while (p < a.size() && a[p][c] == 0)
            ++p;
        if (p == a.size())
            continue;
        std::swap(a[p], a[rank]);
        auto inv = f.inverse(a[rank][c]);
        for (size_t i = rank + 1; i < a.size(); ++i) {
            auto factor = f.mul(a[i][c], inv);
            for (size_t j = c; j < d.genus; ++j)
                a[i][j] = f.sub(a[i][j], f.mul(factor, a[rank][j]));
        }
        ++rank;
    }
    return a.size() + 1 - rank;
}
} // namespace ff
