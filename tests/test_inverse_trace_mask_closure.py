"""Exact classical mask-closure controls, not quantum/oracle benchmarks.

The field arithmetic below is deliberately independent integer polynomial
arithmetic. Native-size fixtures retain N=n^2 and K=floor(N/8); the small
enumeration only checks the exact combinatorial first-moment identity.
"""

from fractions import Fraction
from itertools import product
from random import Random

import pytest

from theorems.binary_subspace_correction import (
    mds_mask_rank_bound,
    random_subspace_annihilation_probability,
    solve_binary_columns,
)


def mul(a, b, modulus):
    result = 0
    degree = modulus.bit_length() - 1
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a >> degree:
            a ^= modulus
    return result


def power(a, exponent, modulus):
    result = 1
    while exponent:
        if exponent & 1:
            result = mul(result, a, modulus)
        a = mul(a, a, modulus)
        exponent >>= 1
    return result


def inv(a, n, modulus):
    return power(a, (1 << n) - 2, modulus) if a else 0


def trace(a, n, modulus):
    result = 0
    for _ in range(n):
        result ^= a
        a = mul(a, a, modulus)
    assert result in (0, 1)
    return result


def linear(columns, value):
    result = 0
    for j, column in enumerate(columns):
        if value >> j & 1:
            result ^= column
    return result


def inverse_linear(columns):
    n = len(columns)
    solutions = [solve_binary_columns(columns, 1 << j, n) for j in range(n)]
    assert all(s.rank == n and s.coefficients is not None for s in solutions)
    return [s.coefficients for s in solutions]


def random_linear(n, rng):
    for _ in range(128):
        columns = [rng.randrange(1 << n) for _ in range(n)]
        if solve_binary_columns(columns, 0, n).rank == n:
            return columns
    raise AssertionError("bounded random mask generation exhausted")


def subfield_basis(n, modulus):
    assert n % 2 == 0
    basis = []
    for j in range(n):
        x = 1 << j
        value = x ^ power(x, 1 << (n // 2), modulus)
        if solve_binary_columns(basis, value, n).coefficients is None:
            basis.append(value)
    assert len(basis) == n // 2
    assert all(power(x, 1 << (n // 2), modulus) == x for x in basis)
    return basis


def contribution(point, value, k, n, modulus):
    result, coefficient = 0, 1
    for j in range(k):
        result |= mul(coefficient, value, modulus) << (j * n)
        coefficient = mul(coefficient, point, modulus)
    return result


def masked_correction(points, targets, masks, centers, offsets, syndrome, n, modulus):
    k = len(points) // 8
    accepted = subfield_basis(n, modulus)
    trace_one = next(1 << j for j in range(n) if trace(1 << j, n, modulus))
    one_value = inv(trace_one, n, modulus)
    word, columns, owners = [], [], []
    residual = syndrome
    for i, (point, bit, mask, center, offset) in enumerate(
        zip(points, targets, masks, centers, offsets)
    ):
        backwards = inverse_linear(mask)
        effective_bit = bit ^ offset
        value = linear(backwards, center ^ (one_value if effective_bit else 0))
        word.append(value)
        residual ^= contribution(point, value, k, n, modulus)
        if not effective_bit:
            for w in accepted:
                direction = linear(backwards, w)
                columns.append(contribution(point, direction, k, n, modulus))
                owners.append((i, direction))
    correction = solve_binary_columns(columns, residual, n * k)
    if correction.coefficients is None:
        return correction, None
    for j, (i, direction) in enumerate(owners):
        if correction.coefficients >> j & 1:
            word[i] ^= direction
    # Verify in the original public coordinates, not the normalized problem.
    actual = 0
    for point, x, bit, mask, center, offset in zip(
        points, word, targets, masks, centers, offsets
    ):
        actual ^= contribution(point, x, k, n, modulus)
        assert trace(inv(linear(mask, x) ^ center, n, modulus), n, modulus) ^ offset == bit
    assert actual == syndrome
    return correction, word


@pytest.mark.parametrize("n,modulus", [(6, 0b1000011), (8, 0b100011011), (10, 0b10000001001)])
def test_masked_native_affine_relation_has_verified_classical_witness(n, modulus):
    rng = Random(20261023 + n)
    size, k = n*n, n*n // 8
    points = rng.sample(range(1 << n), size)
    masks = [random_linear(n, rng) for _ in points]
    centers = [rng.randrange(1 << n) for _ in points]
    offsets = [rng.randrange(2) for _ in points]
    effective = [i % 2 for i in range(size)]
    targets = [b ^ offset for b, offset in zip(effective, offsets)]
    syndrome = rng.randrange(1 << (n * k))
    correction, word = masked_correction(
        points, targets, masks, centers, offsets, syndrome, n, modulus
    )
    assert correction.rank == n * k and word is not None
    # The irreducible moduli are independently certified in a separate test.
    bound = mds_mask_rank_bound(n, k, effective.count(0), n // 2)
    assert bound.failure_upper_bound <= bound.simple_upper_bound < Fraction(1, 1 << n)


def test_dimension_count_does_not_replace_rank_or_randomness():
    n, modulus, size = 8, 0b100011011, 64
    identity = [1 << j for j in range(n)]
    targets = [1] + [0] * (size - 1)
    correction, word = masked_correction(
        list(range(size)), targets, [identity] * size,
        [0] * size, [0] * size, 0, n, modulus,
    )
    assert correction.rank < n * (size // 8)
    assert correction.coefficients is None and word is None
    # This is failure of the subspace-only ansatz. The review's stronger
    # unmasked buffer algorithm still solves this original native instance.


def test_rank_deficient_consistent_syndrome_is_not_rejected():
    result = solve_binary_columns([3, 3, 0], 3, 4)
    assert result.rank == 1 and result.coefficients is not None
    assert linear([3, 3, 0], result.coefficients) == 3


def test_exact_mds_first_moment_matches_all_binary_masks_on_projective_line():
    n, modulus = 2, 0b111
    # All five points of P^1(F4); every two columns are F4-independent.
    h = [(1, a) for a in range(4)] + [(0, 1)]
    failures = annihilators = 0
    for directions in product(range(1, 4), repeat=5):
        columns = [mul(a, w, modulus) | (mul(b, w, modulus) << n)
                   for (a, b), w in zip(h, directions)]
        rank = solve_binary_columns(columns, 0, 4).rank
        failures += rank < 4
        annihilators += (1 << (4 - rank)) - 1
    bound = mds_mask_rank_bound(2, 2, 5, 1)
    assert bound.expected_nonzero_annihilators == Fraction(annihilators, 3**5)
    assert Fraction(failures, 3**5) <= bound.failure_upper_bound <= Fraction(1, 2)


@pytest.mark.parametrize("n,m", [(2, 1), (3, 1), (4, 1), (3, 2), (4, 2)])
def test_random_subspace_hyperplane_probability_by_enumeration(n, m):
    spaces = set()
    for basis in product(range(1, 1 << n), repeat=m):
        if solve_binary_columns(basis, 0, n).rank != m:
            continue
        spaces.add(tuple(sorted(linear(basis, mask) for mask in range(1 << m))))
    contained = sum(all(v & 1 == 0 for v in space) for space in spaces)
    assert Fraction(contained, len(spaces)) == random_subspace_annihilation_probability(n, m)


def test_adaptive_support_union_is_charged_and_not_fixed_support_bound():
    fixed = mds_mask_rank_bound(8, 8, 17, 4)
    adaptive = mds_mask_rank_bound(8, 8, 17, 4, population=64)
    assert fixed.failure_upper_bound < 1
    assert adaptive.simultaneous_support_upper_bound == 1
    strong = mds_mask_rank_bound(20, 50, 200, 10, population=400)
    assert strong.simultaneous_support_upper_bound < Fraction(1, 1 << 500)


def test_scalar_frobenius_and_translation_normalization_including_zero():
    n, modulus, center, coefficient = 6, 0b1000011, 19, 11
    for j in range(n):
        adjusted = power(coefficient, 1 << ((n - j) % n), modulus)
        for x in range(1 << n):
            inverse = inv(x ^ center, n, modulus)
            original = trace(mul(coefficient, power(inverse, 1 << j, modulus), modulus), n, modulus)
            normalized = mul(x ^ center, inv(adjusted, n, modulus), modulus)
            assert original == trace(inv(normalized, n, modulus), n, modulus)


def test_totalized_mobius_pole_is_not_silently_absorbed_into_a_trace_offset():
    n, modulus = 6, 0b1000011
    a = next(1 << j for j in range(n) if trace(1 << j, n, modulus))
    for x in range(1 << n):
        # ax/(x+1), with division by zero totalized to zero.
        direct = mul(mul(a, x, modulus), inv(x ^ 1, n, modulus), modulus)
        rewritten = a ^ mul(a, inv(x ^ 1, n, modulus), modulus)
        if x == 1:
            assert trace(direct, n, modulus) == 0
            assert trace(rewritten, n, modulus) == 1
        else:
            assert direct == rewritten


@pytest.mark.parametrize("args", [([8], 0, 3), ([1], 8, 3), ([-1], 0, 3), ([True], 0, 1), ([], 0, 0)])
def test_binary_contract_rejects_invalid_values(args):
    with pytest.raises(ValueError):
        solve_binary_columns(*args)


@pytest.mark.parametrize("args", [(4, 2, 1, 2), (4, 2, 4, 5), (4, 2, 4, 0), (True, 1, 1, 1)])
def test_bound_rejects_invalid_dimensions(args):
    with pytest.raises(ValueError):
        mds_mask_rank_bound(*args)


@pytest.mark.parametrize("n,modulus", [(2, 0b111), (6, 0b1000011), (8, 0b100011011), (10, 0b10000001001)])
def test_fixture_moduli_are_irreducible(n, modulus):
    def remainder(a, b):
        while a and a.bit_length() >= b.bit_length():
            a ^= b << (a.bit_length() - b.bit_length())
        return a

    def gcd(a, b):
        while b:
            a, b = b, remainder(a, b)
        return a

    x = 2
    for j in range(1, n + 1):
        x = mul(x, x, modulus)
        if j <= n // 2:
            assert gcd(x ^ 2, modulus) == 1
    assert x == 2
