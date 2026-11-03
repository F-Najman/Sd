#include "include/ff_gonality.hpp"
#include <iostream>
#include <sstream>

using namespace ff;
template <class Field>
int run(const Data &d, const Field &field, const Options &opt, size_t repeat,
        const Terms &divisor) {
    for (const auto &c : d.checks)
        require(dimension(d, field, c.terms) == c.dimension, "Magma dimension check failed");
    if (!divisor.empty()) {
        size_t degree = divisor_degree(d, divisor);
        Elimination<Field> e(field, d.genus, degree);
        e.terms(d, divisor);
        Integer count = 0, power = 1;
        for (size_t j = 0; j < e.kernel.size(); ++j) {
            count += power;
            power *= d.field.q;
        }
        require(count <= 1000000, "spectrum too large");
        std::vector<size_t> values;
        projective_vectors(
            field, e,
            [&](const auto &v) {
                values.push_back(divisor_degree(d, pole_divisor(e, v, d.places.size())));
            },
            [] { return false; });
        std::sort(values.begin(), values.end());
        std::cout << '[';
        for (size_t i = 0; i < values.size(); ++i)
            std::cout << (i ? "," : "") << values[i];
        std::cout << "]\n";
        return 0;
    }
    std::vector<double> times;
    Result r;
    for (size_t i = 0; i < repeat; ++i) {
        r = search(d, field, opt);
        times.push_back(r.seconds);
        if (!r.complete)
            break;
    }
    std::sort(times.begin(), times.end());
    std::cout << "{\"field_size\":\"" << d.field.q
              << "\",\"answer\":" << (r.complete ? (r.found ? "true" : "false") : "null")
              << ",\"complete\":" << (r.complete ? "true" : "false") << ",\"degree\":" << opt.degree
              << ",\"genus\":" << d.genus << ",\"threads\":" << opt.threads
              << ",\"baseline\":" << r.baseline << ",\"seconds\":" << times[times.size() / 2]
              << ",\"covers\":" << r.stats.covers << ",\"vectors\":" << r.stats.vectors
              << ",\"fallbacks\":" << r.stats.fallbacks << ",\"nodes\":" << r.stats.nodes
              << ",\"expected_covers\":\"" << r.expected_covers
              << "\",\"magma_checks\":" << d.checks.size() << ",\"witness\":[";
    for (size_t i = 0; i < r.witness.size(); ++i)
        std::cout << (i ? "," : "") << '[' << r.witness[i].first << ',' << r.witness[i].second
                  << ']';
    std::cout << "]}\n";
    return r.complete ? 0 : 2;
}
int main(int argc, char **argv) {
    try {
        require(
            argc >= 2,
            "usage: ffgon FILE [--degree D] [--threads T] [--baseline auto|0..8] [--seconds S] "
            "[--vector-budget V] [--repeat R] [--divisor id:m,...] [--arithmetic auto|generic]");
        Data d = read(argv[1]);
        Options opt;
        opt.degree = d.bound;
        size_t repeat = 1;
        Terms divisor;
        bool generic = false;
        for (int i = 2; i < argc; ++i) {
            std::string a = argv[i];
            require(i + 1 < argc, "missing option value");
            std::string v = argv[++i];
            if (a == "--degree")
                opt.degree = std::stoull(v);
            else if (a == "--threads")
                opt.threads = std::stoull(v);
            else if (a == "--baseline")
                opt.baseline = v == "auto" ? -1 : std::stoi(v);
            else if (a == "--seconds")
                opt.seconds = std::stod(v);
            else if (a == "--vector-budget")
                opt.vector_budget = std::stoull(v);
            else if (a == "--repeat")
                repeat = std::stoull(v);
            else if (a == "--arithmetic") {
                require(v == "auto" || v == "generic", "invalid arithmetic mode");
                generic = v == "generic";
            } else if (a == "--divisor") {
                std::istringstream in(v);
                std::string item;
                while (std::getline(in, item, ',')) {
                    size_t colon = item.find(':');
                    require(colon != std::string::npos, "invalid divisor");
                    divisor.emplace_back(std::stoull(item.substr(0, colon)),
                                         std::stoull(item.substr(colon + 1)));
                }
                std::sort(divisor.begin(), divisor.end());
                for (size_t j = 0; j < divisor.size(); ++j)
                    require(divisor[j].first < d.places.size() && divisor[j].second > 0 &&
                                divisor[j].second <= d.places[divisor[j].first].limit &&
                                (!j || divisor[j - 1].first < divisor[j].first),
                            "invalid divisor term");
            } else
                throw std::runtime_error("unknown option: " + a);
        }
        require(repeat > 0 && repeat <= 100000, "invalid repeat count");
        return with_field(d.field, generic,
                          [&](const auto &field) { return run(d, field, opt, repeat, divisor); });
    } catch (const std::exception &e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
