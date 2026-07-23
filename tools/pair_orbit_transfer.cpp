#include <algorithm>
#include <array>
#include <boost/multiprecision/cpp_int.hpp>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

#ifndef QSEARCH_N
#define QSEARCH_N 8
#endif

constexpr int N = QSEARCH_N;
using Permutation = std::array<std::uint8_t, N>;
using Pair = std::pair<Permutation, Permutation>;
using Weight = boost::multiprecision::cpp_int;
using Key = unsigned __int128;

struct KeyHash {
    std::size_t operator()(Key key) const noexcept {
        const auto low = static_cast<std::uint64_t>(key);
        const auto high = static_cast<std::uint64_t>(key >> 64);
        return std::hash<std::uint64_t>{}(low)
            ^ (std::hash<std::uint64_t>{}(high) + 0x9e3779b97f4a7c15ULL
               + (low << 6) + (low >> 2));
    }
};

using Distribution = std::unordered_map<Key, Weight, KeyHash>;

Permutation identity() {
    Permutation result{};
    for (int index = 0; index < N; ++index) {
        result[index] = static_cast<std::uint8_t>(index);
    }
    return result;
}

Permutation transposition(int first, int second) {
    auto result = identity();
    std::swap(result[first], result[second]);
    return result;
}

Permutation three_cycle(int first, int second, int third) {
    auto result = identity();
    result[first] = static_cast<std::uint8_t>(second);
    result[second] = static_cast<std::uint8_t>(third);
    result[third] = static_cast<std::uint8_t>(first);
    return result;
}

Permutation compose(const Permutation& left, const Permutation& right) {
    Permutation result{};
    for (int index = 0; index < N; ++index) {
        result[index] = left[right[index]];
    }
    return result;
}

Permutation inverse(const Permutation& permutation) {
    Permutation result{};
    for (int index = 0; index < N; ++index) {
        result[permutation[index]] = static_cast<std::uint8_t>(index);
    }
    return result;
}

Key pack_pair(const Permutation& left, const Permutation& right) {
    Key result = 0;
    for (int index = 0; index < N; ++index) {
        result |= static_cast<Key>(left[index]) << (4 * index);
        result |= static_cast<Key>(right[index]) << (4 * N + 4 * index);
    }
    return result;
}

Pair unpack_pair(Key packed) {
    Permutation left{};
    Permutation right{};
    for (int index = 0; index < N; ++index) {
        left[index] = static_cast<std::uint8_t>((packed >> (4 * index)) & 15);
        right[index] = static_cast<std::uint8_t>((packed >> (4 * N + 4 * index)) & 15);
    }
    return {left, right};
}

using ComponentEncoding = std::vector<std::uint8_t>;

ComponentEncoding rooted_component_encoding(
    const Permutation& left,
    const Permutation& right,
    const Permutation& left_inverse,
    const Permutation& right_inverse,
    std::uint16_t component_mask,
    int root
) {
    std::array<int, N> relabel{};
    relabel.fill(-1);
    std::array<int, N> order{};
    int size = 1;
    order[0] = root;
    relabel[root] = 0;
    for (int cursor = 0; cursor < size; ++cursor) {
        const int point = order[cursor];
        const std::array<int, 4> images = {
            left[point], right[point], left_inverse[point], right_inverse[point]
        };
        for (const int image : images) {
            if ((component_mask & (1U << image)) && relabel[image] < 0) {
                relabel[image] = size;
                order[size++] = image;
            }
        }
    }
    ComponentEncoding encoding;
    encoding.reserve(1 + 2 * size);
    encoding.push_back(static_cast<std::uint8_t>(size));
    for (int index = 0; index < size; ++index) {
        encoding.push_back(static_cast<std::uint8_t>(relabel[left[order[index]]]));
    }
    for (int index = 0; index < size; ++index) {
        encoding.push_back(static_cast<std::uint8_t>(relabel[right[order[index]]]));
    }
    return encoding;
}

Key canonical_pair(const Permutation& left, const Permutation& right) {
    const auto left_inverse = inverse(left);
    const auto right_inverse = inverse(right);
    std::uint16_t unseen = 0;
    for (int point = 0; point < N; ++point) {
        if (left[point] != point || right[point] != point) {
            unseen |= static_cast<std::uint16_t>(1U << point);
        }
    }

    std::vector<ComponentEncoding> components;
    while (unseen) {
        int seed = 0;
        while (!(unseen & (1U << seed))) {
            ++seed;
        }
        std::uint16_t component = static_cast<std::uint16_t>(1U << seed);
        std::array<int, N> pending{};
        int pending_size = 1;
        pending[0] = seed;
        for (int cursor = 0; cursor < pending_size; ++cursor) {
            const int point = pending[cursor];
            const std::array<int, 4> images = {
                left[point], right[point], left_inverse[point], right_inverse[point]
            };
            for (const int image : images) {
                if (!(component & (1U << image))) {
                    component |= static_cast<std::uint16_t>(1U << image);
                    pending[pending_size++] = image;
                }
            }
        }
        unseen &= static_cast<std::uint16_t>(~component);
        ComponentEncoding best;
        bool first = true;
        for (int root = 0; root < N; ++root) {
            if (!(component & (1U << root))) {
                continue;
            }
            auto encoding = rooted_component_encoding(
                left, right, left_inverse, right_inverse, component, root
            );
            if (first || encoding < best) {
                best = std::move(encoding);
                first = false;
            }
        }
        components.push_back(std::move(best));
    }
    std::sort(components.begin(), components.end());

    auto canonical_left = identity();
    auto canonical_right = identity();
    int offset = 0;
    for (const auto& component : components) {
        const int size = component[0];
        for (int index = 0; index < size; ++index) {
            canonical_left[offset + index] = static_cast<std::uint8_t>(
                offset + component[1 + index]
            );
            canonical_right[offset + index] = static_cast<std::uint8_t>(
                offset + component[1 + size + index]
            );
        }
        offset += size;
    }
    return pack_pair(canonical_left, canonical_right);
}

std::vector<Pair> shared_transposition_orbit() {
    std::vector<Pair> result;
    for (int common = 0; common < N; ++common) {
        for (int left = 0; left < N; ++left) {
            if (left == common) {
                continue;
            }
            for (int right = 0; right < N; ++right) {
                if (right == common || right == left) {
                    continue;
                }
                result.push_back(
                    {transposition(common, left), transposition(common, right)}
                );
            }
        }
    }
    return result;
}

std::vector<Pair> tc_intersection_one_orbit() {
    std::vector<Pair> result;
    for (int first = 0; first < N; ++first) {
        for (int second = first + 1; second < N; ++second) {
            for (int third = second + 1; third < N; ++third) {
                const std::array<std::array<int, 3>, 2> cycles = {{
                    {{first, second, third}},
                    {{first, third, second}},
                }};
                const std::array<int, 3> support = {first, second, third};
                for (const auto& cycle : cycles) {
                    for (const int shared : support) {
                        for (int outside = 0; outside < N; ++outside) {
                            if (outside == first || outside == second || outside == third) {
                                continue;
                            }
                            result.push_back({
                                transposition(shared, outside),
                                three_cycle(cycle[0], cycle[1], cycle[2]),
                            });
                        }
                    }
                }
            }
        }
    }
    return result;
}

void add_transition(
    Distribution& output,
    const Pair& state,
    const Weight& weight,
    const std::vector<Pair>& orbit,
    std::uint64_t orbit_weight
) {
    for (const auto& term : orbit) {
        const auto key = canonical_pair(
            compose(state.first, term.first),
            compose(state.second, term.second)
        );
        output[key] += weight * orbit_weight;
    }
}

int parse_max_degree(int argc, char** argv) {
    int max_degree = 4;
    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        if (argument == "--max-degree" && index + 1 < argc) {
            max_degree = std::atoi(argv[++index]);
        } else {
            throw std::invalid_argument("usage: pair_orbit_transfer [--max-degree 1..32]");
        }
    }
    if (max_degree < 1 || max_degree > 32) {
        throw std::invalid_argument("max degree must be between 1 and 32");
    }
    return max_degree;
}

void emit_distribution(int degree, const Distribution& distribution) {
    std::map<Key, Weight> ordered(
        distribution.begin(), distribution.end()
    );
    Weight total_weight = 0;
    for (const auto& [key, weight] : ordered) {
        total_weight += weight;
    }
    std::cerr << "degree=" << degree << " states=" << ordered.size()
              << " total_weight=" << total_weight << '\n';
    for (const auto& [key, weight] : ordered) {
        std::string encoded(2 * N, '0');
        for (int index = 2 * N - 1; index >= 0; --index) {
            const int value = static_cast<int>(
                (key >> (4 * (2 * N - 1 - index))) & 15
            );
            encoded[index] = static_cast<char>(value < 10 ? '0' + value : 'a' + value - 10);
        }
        std::cout << degree << '\t' << encoded << '\t' << weight << '\n';
    }
}

}  // namespace

int main(int argc, char** argv) {
    try {
        const int max_degree = parse_max_degree(argc, argv);
        const auto tt1_orbit = shared_transposition_orbit();
        const auto tc1_orbit = tc_intersection_one_orbit();
        const std::size_t expected_tt1 = N * (N - 1) * (N - 2);
        const std::size_t expected_tc1 = expected_tt1 * (N - 3);
        if (tt1_orbit.size() != expected_tt1 || tc1_orbit.size() != expected_tc1) {
            throw std::runtime_error("unexpected orbit size");
        }

        Distribution current;
        current[canonical_pair(transposition(0, 1), transposition(0, 2))] += 1;
        current[canonical_pair(transposition(0, 1), three_cycle(0, 2, 3))] += 1;
        emit_distribution(1, current);
        for (int degree = 2; degree <= max_degree; ++degree) {
            Distribution next;
            next.reserve(43206);
            for (const auto& [key, weight] : current) {
                const auto state = unpack_pair(key);
                add_transition(next, state, weight, tt1_orbit, N - 3);
                add_transition(next, state, weight, tc1_orbit, 1);
            }
            current = std::move(next);
            emit_distribution(degree, current);
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
