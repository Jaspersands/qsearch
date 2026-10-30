"""Exact finite controls for a conditional hash deduction, not a sampler.

All enumeration is deliberately confined to tiny finite fixtures. No SAT
backend, production field module, filesystem output, or timing claim is used.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, lcm

import pytest


def hash_value(rows, u):
    return sum(((row & u).bit_count() & 1) << i for i, row in enumerate(rows))


def binary_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            bit = row.bit_length() - 1
            if bit not in pivots:
                pivots[bit] = row
                break
            row ^= pivots[bit]
    return len(pivots)


def hash_statistics(solutions, bits, checks, *, full_rank_only=False):
    """Exhaust tiny hash spaces; use integer accumulation before Fractions."""
    assert 0 <= bits <= 3 and 0 <= checks <= bits
    assert solutions and len(set(solutions)) == len(solutions)
    assert all(0 <= u < 1 << bits for u in solutions)
    size = len(solutions)
    scale = lcm(*range(1, size + 1))
    transitions = [[0] * size for _ in solutions]
    anchored_sizes = [0] * size
    matrices = nonempty = square_mass = 0
    ranks = Counter()
    for rows in product(range(1 << bits), repeat=checks):
        rank = binary_rank(rows)
        if full_rank_only and rank != checks:
            continue
        matrices += 1
        ranks[rank] += 1
        buckets = defaultdict(list)
        for i, u in enumerate(solutions):
            buckets[hash_value(rows, u)].append(i)
        nonempty += len(buckets)
        square_mass += sum(len(cell) ** 2 for cell in buckets.values())
        for cell in buckets.values():
            for i in cell:
                anchored_sizes[i] += len(cell)
                for j in cell:
                    transitions[i][j] += scale // len(cell)
    denominator = matrices * (1 << checks)
    return {
        "kernel": tuple(tuple(F(v, matrices * scale) for v in row)
                        for row in transitions),
        "initial_success": F(nonempty, denominator),
        "mean_size": F(matrices * size, denominator),
        "second_moment": F(square_mass, denominator),
        "anchored_sizes": tuple(F(v, matrices) for v in anchored_sizes),
        "matrices": matrices,
        "ranks": ranks,
    }


@pytest.mark.parametrize("checks", [0, 1, 2, 3])
def test_every_nonempty_subset_of_binary_three_space(checks):
    p = F(1, 1 << checks)
    for mask in range(1, 1 << 8):
        solutions = tuple(u for u in range(8) if mask >> u & 1)
        size = len(solutions)
        stats = hash_statistics(solutions, 3, checks)
        kernel = stats["kernel"]
        load = size * p
        minor = p / (2 + (size - 2) * p)
        assert stats["matrices"] == 1 << (3 * checks)
        assert stats["mean_size"] == load
        assert stats["second_moment"] == load + size * (size - 1) * p * p
        assert stats["anchored_sizes"] == (1 + (size - 1) * p,) * size
        assert stats["initial_success"] >= load / (1 + (size - 1) * p)
        for i, row in enumerate(kernel):
            assert sum(row) == 1
            for j, value in enumerate(row):
                assert value == kernel[j][i]
                assert value >= minor
        if F(1, 2) <= load <= F(3, 2):
            assert stats["initial_success"] >= F(1, 3)
            assert stats["mean_size"] <= F(3, 2)
            assert all(v <= F(5, 2) for v in stats["anchored_sizes"])
            assert all(v >= F(1, 5 * size) for row in kernel for v in row)


@pytest.mark.parametrize("checks", [0, 1, 2, 3])
def test_binary_three_point_collision_conditional_size(checks):
    solutions = (0, 1, 2, 3, 7)
    u, v = 1, 7
    collisions = third_collisions = size_sum = 0
    matrices = 1 << (3 * checks)
    for rows in product(range(8), repeat=checks):
        if hash_value(rows, u) == hash_value(rows, v):
            collisions += 1
            third_collisions += hash_value(rows, 3) == hash_value(rows, u)
            size_sum += sum(hash_value(rows, w) == hash_value(rows, u)
                            for w in solutions)
    p = F(1, 1 << checks)
    assert F(collisions, matrices) == p
    assert F(third_collisions, matrices) == p * p
    assert F(size_sum, collisions) == 2 + (len(solutions) - 2) * p


def test_rank_deficiency_is_included_and_full_rank_conditioning_changes_law():
    solutions = tuple(range(8))
    stats = hash_statistics(solutions, 3, 2)
    conditioned = hash_statistics(solutions, 3, 2, full_rank_only=True)
    assert stats["ranks"] == {0: 1, 1: 21, 2: 42}
    assert F(22, 64) <= F((1 << 2) - 1, 1 << 3)
    assert stats["kernel"] != conditioned["kernel"]
    for rows in product(range(8), repeat=2):
        rank = binary_rank(rows)
        cells = Counter(hash_value(rows, u) for u in solutions)
        assert set(cells.values()) == {1 << (3 - rank)}
        assert len(cells) == 1 << rank
        for t in range(4):
            assert cells[t] in (0, 1 << (3 - rank))
    assert Counter(hash_value((0, 0), u) for u in solutions) == {0: 8}
    assert conditioned["kernel"][0][0] == F(1, 2)


def multiply_law(law, kernel):
    return tuple(sum(law[i] * kernel[i][j] for i in range(len(law)))
                 for j in range(len(law)))


def tv(left, right):
    return sum(abs(a - b) for a, b in zip(left, right)) / 2


@pytest.mark.parametrize("solutions,checks", [((0, 1, 2), 1),
                                               ((0, 1, 3, 4, 7), 2),
                                               ((0,), 0)])
def test_exact_contraction_from_every_point_mass(solutions, checks):
    kernel = hash_statistics(solutions, 3, checks)["kernel"]
    uniform = (F(1, len(solutions)),) * len(solutions)
    assert multiply_law(uniform, kernel) == uniform
    for start in range(len(solutions)):
        law = tuple(F(i == start) for i in range(len(solutions)))
        for step in range(7):
            assert tv(law, uniform) <= F(4, 5) ** step
            law = multiply_law(law, kernel)


def test_arbitrary_initial_witness_is_biased_and_arbitrary_cell_choice_is_wrong():
    solutions = (0, 1, 2)
    initial = Counter()
    wrong = [[F(0)] * 3 for _ in solutions]
    for row in range(4):
        for t in range(2):
            cell = [u for u in solutions if hash_value((row,), u) == t]
            if cell:
                initial[min(cell)] += 1
        for i, u in enumerate(solutions):
            cell = [v for v in solutions
                    if hash_value((row,), v) == hash_value((row,), u)]
            wrong[i][solutions.index(min(cell))] += F(1, 4)
    law = tuple(F(initial[u], sum(initial.values())) for u in solutions)
    uniform = (F(1, 3),) * 3
    assert law == (F(4, 7), F(2, 7), F(1, 7))
    assert tv(law, uniform) == F(5, 21)
    assert multiply_law(uniform, wrong) != uniform
    assert wrong[0][1] != wrong[1][0]


@pytest.mark.parametrize("solutions", [(), (0,), (0, 1, 2)])
@pytest.mark.parametrize("trial_cap", [0, 1, 3])
def test_capped_initialization_and_heatbath_retain_abort_mass(solutions, trial_cap):
    trial_mass = Counter()
    for row in range(4):
        for t in range(2):
            cell = [u for u in solutions if hash_value((row,), u) == t]
            trial_mass[min(cell) if cell else None] += F(1, 8)
    failure = trial_mass[None]
    abort = failure ** trial_cap
    retries = sum((failure ** j for j in range(trial_cap)), F(0))
    law = tuple(trial_mass[u] * retries for u in solutions)
    assert sum(law) + abort == 1
    if not solutions:
        assert abort == 1 and law == ()
        return
    kernel = hash_statistics(solutions, 2, 1)["kernel"]
    target = (F(1, len(solutions)),) * len(solutions) + (F(0),)
    for step in range(6):
        assert sum(law) + abort == 1
        assert tv(law + (abort,), target) <= abort + F(4, 5) ** step
        if trial_cap:
            normalized = tuple(value / (1 - abort) for value in law)
            assert tv(normalized, target[:-1]) <= F(4, 5) ** step
        law = multiply_law(law, kernel)


def test_cost_correlated_with_success_still_has_paid_geometric_restart():
    success, failure = F(1, 3), F(2, 3)
    mean_trial_cost = success * 7 + failure * 1
    expected_total = mean_trial_cost / success
    assert expected_total == 9
    assert expected_total == success * 7 + failure * (1 + expected_total)
    for cap in range(1, 8):
        stopped_cost = sum(failure ** j * mean_trial_cost for j in range(cap))
        assert stopped_cost == expected_total * (1 - failure ** cap)
        completed_mass = sum(failure ** j * success for j in range(cap))
        assert completed_mass + failure ** cap == 1


def test_abort_coupling_handles_output_correlated_cost_and_markov_clock():
    # Half the outputs are slow: conditioning away ABORT is not the same law.
    atoms = ((0, 1, F(1, 2)), (1, 100, F(1, 2)))
    ideal = (F(1, 2), F(1, 2), F(0))
    mean_work = sum(cost * mass for _, cost, mass in atoms)
    for budget in (0, 1, 99, 100, 404):
        capped = [F(0)] * 3
        timeout = F(0)
        for output, cost, mass in atoms:
            if cost > budget:
                capped[2] += mass
                timeout += mass
            else:
                capped[output] += mass
        assert tv(capped, ideal) <= timeout
        if budget:
            assert timeout <= mean_work / budget
        if budget == 1:
            assert tuple(capped) == (F(1, 2), F(0), F(1, 2))
            assert tv(capped, ideal) == F(1, 2)
            assert (capped[0] / (1 - capped[2]), capped[1]) == (1, 0)
    epsilon = F(1, 4)
    budget = 2 * mean_work / epsilon
    assert mean_work / budget == epsilon / 2
    assert budget == 404


def test_exact_uniform_index_requires_rejection_not_modulo():
    accepted = Counter(value for value in range(4) if value < 3)
    modulo = Counter(value % 3 for value in range(4))
    assert tuple(F(accepted[i], sum(accepted.values())) for i in range(3)) == (F(1, 3),) * 3
    assert tuple(F(modulo[i], 4) for i in range(3)) == (F(1, 2), F(1, 4), F(1, 4))


def gf_mul(a, b):
    """GF(16) in the fixed polynomial basis X^4+X+1, test fixtures only."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 0b10011
    return result


def gf_power(a, exponent):
    result = 1
    while exponent:
        if exponent & 1:
            result = gf_mul(result, a)
        a = gf_mul(a, a)
        exponent >>= 1
    return result


@lru_cache(None)
def gf_inverse(a):
    return gf_power(a, 14)


@lru_cache(None)
def gf_trace(a):
    result = 0
    for _ in range(4):
        result ^= a
        a = gf_mul(a, a)
    assert result in (0, 1)
    return result


def trace_parameters(bit):
    pivot = next(i for i in range(4) if gf_trace(1 << i))
    basis = tuple((1 << i) ^ ((1 << pivot) if gf_trace(1 << i) else 0)
                  for i in range(4) if i != pivot)
    values = []
    for u in range(8):
        y = (1 << pivot) if bit else 0
        for i, value in enumerate(basis):
            if u >> i & 1:
                y ^= value
        values.append(y)
    return tuple(values)


def native_syndrome(points, word):
    a = b = 0
    for point, value in zip(points, word):
        a ^= value
        b ^= gf_mul(point, value)
    return a, b


def decode_native(points, targets, h, u):
    free = tuple(gf_inverse(trace_parameters(targets[2 + i])[(u >> (3 * i)) & 7])
                 for i in range(2))
    s0 = h[0] ^ free[0] ^ free[1]
    s1 = h[1] ^ gf_mul(points[2], free[0]) ^ gf_mul(points[3], free[1])
    x1 = gf_mul(s1 ^ gf_mul(points[0], s0), gf_inverse(points[0] ^ points[1]))
    return (s0 ^ x1, x1) + free


def accepted(word, targets):
    return all(gf_trace(gf_inverse(x)) == bit for x, bit in zip(word, targets))


def test_reciprocal_trace_basis_is_bijective_and_zero_complete():
    assert gf_inverse(0) == 0
    for bit in (0, 1):
        ys = trace_parameters(bit)
        xs = tuple(gf_inverse(y) for y in ys)
        assert len(set(ys)) == len(set(xs)) == 8
        assert all(gf_trace(y) == bit for y in ys)
        assert set(xs) == {x for x in range(16) if gf_trace(gf_inverse(x)) == bit}
        assert (0 in xs) == (bit == 0)
    assert all(gf_mul(x, gf_inverse(x)) == 1 for x in range(1, 16))


@pytest.mark.parametrize("points", [(0, 1, 2, 3), (9, 4, 14, 6)])
@pytest.mark.parametrize("targets", [(0, 0, 0, 0), (1, 1, 1, 1), (0, 1, 0, 1)])
def test_native_residual_all_syndromes_bijection_prange_and_selected_hashes(points, targets):
    # These are actual N=16,K=2,m=4,r=2 residuals, not a changed-rate surrogate.
    alphabets = [tuple(x for x in range(16) if gf_trace(gf_inverse(x)) == bit)
                 for bit in targets]
    index = [{gf_inverse(y): u for u, y in enumerate(trace_parameters(bit))}
             for bit in targets[2:]]
    direct = defaultdict(dict)
    for word in product(*alphabets):
        h = native_syndrome(points, word)
        u = index[0][word[2]] | (index[1][word[3]] << 3)
        assert u not in direct[h]
        direct[h][u] = word
    assert sum(map(len, direct.values())) == 8 ** 4
    assert F(sum(map(len, direct.values())), 16 ** 2) == 16  # mu=2^(6-2)
    selected_rows = ((1, 2, 4, 8), (1, 1, 0, 8), (0, 0, 0, 0))
    for h in product(range(16), repeat=2):
        actual = {}
        for u in range(64):
            word = decode_native(points, targets, h, u)
            assert native_syndrome(points, word) == h
            assert accepted(word[2:], targets[2:])
            if accepted(word, targets):
                actual[u] = word
        assert actual == direct[h]
        size = len(actual)
        g = F(size, 16)
        assert F(size, 64) == g * F(1, 4)
        if size:
            assert F(1, 64) / F(size, 64) == F(1, size)
        if h in ((0, 0), (3, 7), (12, 4)):
            for rows in selected_rows:
                rank = binary_rank(rows)
                for t in range(16):
                    ambient = [u for u in range(64) if hash_value(rows, u) == t]
                    assert len(ambient) in (0, 1 << (6 - rank))
                    from_bits = {decode_native(points, targets, h, u)
                                 for u in ambient if u in actual}
                    from_words = {word for u, word in direct[h].items()
                                  if hash_value(rows, u) == t}
                    assert from_bits == from_words
    if targets == (0, 0, 0, 0):
        assert direct[(0, 0)][0] == (0, 0, 0, 0)
    if targets == (1, 1, 1, 1):
        assert all(all(word) for fiber in direct.values() for word in fiber.values())


@pytest.mark.parametrize("checks,length", [(1, 3), (2, 4), (3, 6)])
def test_parseval_and_every_exact_rs_support_bound(checks, length):
    alphabet = [x for x in range(16) if gf_trace(gf_inverse(x)) == 1]
    weights = tuple(F(sum((-1) ** gf_trace(gf_mul(a, x)) for x in alphabet), 8) ** 2
                    for a in range(16))
    assert weights[0] == 1 and sum(weights) == 2 and sum(weights[1:]) == 1
    beta2 = max(weights[1:])
    assert beta2 == F(1, 4)
    by_support = defaultdict(F)
    for coefficients in product(range(16), repeat=checks):
        if not any(coefficients):
            continue
        values = []
        for point in range(length):
            value = 0
            for coefficient in reversed(coefficients):
                value = gf_mul(value, point) ^ coefficient
            values.append(value)
        support = tuple(i for i, value in enumerate(values) if value)
        weight = F(1)
        for value in values:
            weight *= weights[value]
        by_support[support] += weight
    for support, mass in by_support.items():
        assert len(support) >= length - checks + 1
        assert mass <= beta2 ** (length - checks)
    variance = sum(by_support.values())
    support_count = sum(comb(length, w) for w in range(length - checks + 1, length + 1))
    assert variance <= support_count * beta2 ** (length - checks)
    assert support_count <= 1 << length
    if (checks, length) == (2, 4):
        hist = Counter(native_syndrome(tuple(range(4)), word)
                       for word in product(alphabet, repeat=4))
        direct_variance = sum((F(hist[h], 16) - 1) ** 2
                              for h in product(range(16), repeat=2)) / 256
        assert direct_variance == variance == F(53, 2048)
