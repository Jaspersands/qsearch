"""Independent finite checks; no parent rank or moment routines are used."""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import importlib.util
import json
import random


def subsets(values):
    values = tuple(values)
    return [frozenset(c) for n in range(len(values) + 1)
            for c in combinations(values, n)]


def span(rows):
    result = {frozenset()}
    for row in rows:
        result |= {word ^ row for word in result}
    return result


def dimension(code):
    size = len(code)
    assert size > 0 and size & (size - 1) == 0
    return size.bit_length() - 1


def overlap(shared):
    first = [(i, 0) for i in range(4)]
    second = [(i, 0 if i in shared else 1) for i in range(4)]
    vertices = tuple(dict.fromkeys(first + second))
    low_rows = [frozenset(tup[j:j + 2])
                for tup in (first, second) for j in (0, 2)]
    high_rows = [frozenset(first), frozenset(second)]
    components = [{v} for v in vertices]
    for edge in low_rows:
        touched = [part for part in components if part & edge]
        components = [part for part in components if not part & edge]
        components.append(set().union(*touched))
    return vertices, low_rows, high_rows, components


def walsh(values):
    values = list(values)
    step = 1
    while step < len(values):
        for start in range(0, len(values), 2 * step):
            for j in range(start, start + step):
                a, b = values[j], values[j + step]
                values[j], values[j + step] = a + b, a - b
        step *= 2
    return values


def structural_controls():
    records, support_cases, affine_coefficients = [], 0, 0
    all_overlaps = []
    for shared in subsets(range(4)):
        vertices, low_rows, high_rows, components = overlap(shared)
        universe = frozenset(vertices)
        low, high = span(low_rows), span(high_rows)
        rl, rh, v = dimension(low), dimension(high), len(vertices)
        assert rl == v - len(components)
        maxima = []
        for support in subsets(vertices):
            dl = dimension({word for word in low if word <= support})
            dh = dimension({word for word in high if word <= support})
            occupied = sum(bool(part & support) for part in components)
            outside = universe - support
            projected_high = dimension({word & outside for word in high})
            assert dl == len(support) - occupied
            assert projected_high == rh - dh
            power = v - rl - 2 * rh + dl + 2 * dh - len(support)
            missed = len(components) - occupied
            assert power == missed - 2 * projected_high
            assert missed <= 2 * projected_high
            maxima.append(power)
            support_cases += 1
        assert max(maxima) == 0

        position = {vertex: i for i, vertex in enumerate(vertices)}
        mask = lambda word: sum(1 << position[x] for x in word)
        for rows, code in ((low_rows, low), (high_rows, high)):
            for target in (0, 1):
                rhs = [0, target, 0, target] if len(rows) == 4 else [target, target]
                row_masks = [mask(row) for row in rows]
                truth = [int(all((x & row).bit_count() % 2 == bit
                                 for row, bit in zip(row_masks, rhs)))
                         for x in range(1 << v)]
                coefficients = walsh(truth)
                code_masks = {mask(word) for word in code}
                shift = mask({x for x in vertices if x[0] == 2}) if target else 0
                for frequency, coefficient in enumerate(coefficients):
                    phase = -1 if (frequency & shift).bit_count() % 2 else 1
                    expected = phase * (1 << v) // len(code) if frequency in code_masks else 0
                    assert coefficient == expected
                    affine_coefficients += 1
        records.append({"shared": sorted(shared), "variables": v,
                        "low_rank": rl, "high_rank": rh,
                        "components": len(components), "maximum_power": max(maxima)})
        all_overlaps.append((shared, vertices, low, high))

    envelopes, confined_checks = [], 0
    for rank in range(3, 19):
        t, length = rank // 3, 2 ** ((rank + 2) // 3)
        eps, second = F(1, 4 * length), F(0)
        for shared, vertices, low, high in all_overlaps:
            histogram = Counter({frozenset(): 1})
            for code in [low] * t + [high] * (rank - t):
                updated = Counter()
                for support, multiplicity in histogram.items():
                    for word in code:
                        updated[support | word] += multiplicity
                histogram = updated
            for support in subsets(vertices):
                actual = sum(n for exact, n in histogram.items() if exact <= support)
                low_count = sum(word <= support for word in low)
                high_count = sum(word <= support for word in high)
                assert actual == low_count ** t * high_count ** (rank - t)
                confined_checks += 1
            normalizer = len(low) ** t * len(high) ** (rank - t)
            assert sum(histogram.values()) == normalizer
            probability_bound = sum(n * eps ** len(a) for a, n in histogram.items()) / normalizer
            tuple_pairs = length ** 4 * (length - 1) ** (4 - len(shared))
            second += tuple_pairs * probability_bound
        assert second <= F(117, 16) ** 4
        envelopes.append({"rank": rank, "second_moment_envelope": str(second),
                          "decimal": float(second)})
    return {"support_cases": support_cases, "affine_coefficients": affine_coefficients,
            "confined_support_checks": confined_checks, "overlaps": records,
            "exact_support_envelopes": envelopes}


def first_moment_stress():
    rank, length, eps = 3, 2, F(1, 8)
    uniform = [F(1, 8)] * 8
    laws = [uniform.copy() for _ in range(4)]
    for i, sign in ((0, 1), (1, -1)):
        laws[i] = [F(1, 8) * (1 + sign * eps * (-1) ** (x & 1)) for x in range(8)]
    for law in laws:
        assert sum(law) == 1 and min(law) >= 0
        assert max(abs(x) for x in walsh(law)[1:]) <= eps
    probabilities = []
    for target in range(8):
        p = F(0)
        for a, b, c in product(range(8), repeat=3):
            d = target ^ a ^ b ^ c
            if not ((a ^ b) & 1):
                p += laws[0][a] * laws[1][b] * laws[2][c] * laws[3][d]
        assert p == F(1, 16) * (1 - eps ** 2)
        probabilities.append(str(p))
    return {"opposite_character_tilts_first_tuple_probabilities": probabilities,
            "iid_violation_countercontrol": {
                "construction": "Each list repeats one independent uniform value; rank=12, target arbitrary.",
                "success_probability": str(F(1, 2 ** 16)),
                "below_claimed_floor": F(1, 2 ** 16) < F(1, 8000)}}


def arithmetic_controls():
    p0 = F(49, 64) / F(117, 16) ** 4
    capped = p0 - F(1, 8000)
    assert p0 == F(50176, 187388721) and p0 > F(1, 4000)
    assert capped > F(1, 8000)
    for rank in range(3, 301):
        t, length = rank // 3, 2 ** ((rank + 2) // 3)
        eps = F(1, 4 * length)
        first_error = 2 * (2 ** t - 1) * eps ** 2 + (2 ** (rank + t) - 2 ** (t + 1) + 1) * eps ** 4
        assert first_error <= F(17, 256) < F(1, 8)
        expected_pairs = F(2 * length ** 2, 2 ** t) * (1 + (2 ** t - 1) * eps ** 2)
        assert expected_pairs < 5 * length
    tower = []
    for e in (8, 16, 32, 64, 128, 256, 512, 1024):
        g, a, worst_rank = 5 * e + 1, 2 * e - 9, 10 * e + 2
        degrees = [e // 2 - 3] + [e // 2 - 2] * 3
        assert sum(degrees) == a
        exponent = (worst_rank + 2) // 3
        ratios = [F(100003 ** n, 64 * ((g + 1) * (n + 6)) ** 2 * 2 ** (2 * exponent)) for n in degrees]
        assert all(x >= 1 for x in ratios) == (e >= 64)
        tower.append({"e": e, "degrees": degrees, "list_exponent": exponent,
                      "minimum_ratio_floor": ratios[0].numerator // ratios[0].denominator,
                      "sufficient": all(x >= 1 for x in ratios)})
    assert tower[3]["minimum_ratio_floor"] == 1776281
    growth_bound = F(100003, 4 * 2 ** 14)
    assert growth_bound > 1
    for e in range(64, 4097, 2):
        ratio_c = F((5 * e + 12) * (e + 8), (5 * e + 2) * (e + 6))
        increment = (10 * (e + 2) + 4) // 3 - (10 * e + 4) // 3
        assert ratio_c < 2 and increment <= 7
    return {"untruncated_lower": str(p0), "capped_lower": str(capped),
            "retry_expectation_upper": str(1 / capped),
            "retry_expectation_upper_decimal": float(1 / capped),
            "rank_constant_checks": [3, 300], "tower": tower,
            "all_even_level_growth_lower": str(growth_bound)}


def implementation_controls():
    spec = importlib.util.spec_from_file_location("reviewed_four_list", "reviewed/four_list.py")
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    rng, calls, matches = random.Random(261026), 0, 0
    for rank in range(3, 12):
        n, length, mask = 2 ** rank, 2 ** ((rank + 2) // 3), 2 ** (rank // 3) - 1
        fixtures = [[[0] * length for _ in range(4)]]
        fixtures += [[[rng.randrange(n) for _ in range(length)] for _ in range(4)] for _ in range(7)]
        for lists in fixtures:
            targets = range(n) if rank <= 8 else rng.sample(range(n), 128)
            possible = {a ^ b ^ c ^ d for a, b, c, d in product(*lists) if not ((a ^ b) & mask)}
            for target in targets:
                result = parent.four_list_match(lists, rank, target)
                assert (result["indices"] is not None) == (target in possible)
                if result["indices"] is not None:
                    values = [lists[i][index] for i, index in enumerate(result["indices"])]
                    assert values[0] ^ values[1] ^ values[2] ^ values[3] == target
                    matches += 1
                calls += 1
    cap4 = parent.four_list_match([[0, 0]] * 4, 3, 0, pair_cap=4)
    cap5 = parent.four_list_match([[0, 0]] * 4, 3, 0, pair_cap=5)
    assert cap4["status"] == "UNKNOWN_PAIR_CAP" and cap4["pairs_visited"] == 5
    assert cap5["indices"] is not None and cap5["pairs_visited"] == 5
    return {"join_checks": calls, "matches": matches,
            "duplicate_pair_cap4": cap4, "duplicate_pair_cap5": cap5}


if __name__ == "__main__":
    print(json.dumps({"structure": structural_controls(),
                      "first_moment_stress": first_moment_stress(),
                      "arithmetic": arithmetic_controls(),
                      "implementation": implementation_controls()}, indent=2))
