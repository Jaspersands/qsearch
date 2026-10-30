"""Exact arithmetic controls for weak-isogeny masks and sign normalization.

These are finite-module and integer-order checks, not curves, geometric
interpolation, kernel recovery, field-construction timings, or hardness tests.
There are 2**s square roots at s odd prime levels, but only 2**(s-1)
relative sign choices after identifying one simultaneous global negation.
"""

from itertools import combinations, product
from math import gcd, prod

import pytest
from flint import nmod_mat


ELL = 61
PHI = ((6, -5, 0, 0), (5, 6, 0, 0),
       (0, 0, 6, 5), (0, 0, -5, 6))


def _crt(residues, moduli):
    modulus = prod(moduli)
    return sum(a * (modulus // r) * pow(modulus // r, -1, r)
               for a, r in zip(residues, moduli)) % modulus


def _form(dimension, prime):
    return nmod_mat([[1 if i % 2 == 0 and j == i + 1 else
                      -1 if i % 2 == 1 and j == i - 1 else 0
                      for j in range(dimension)]
                     for i in range(dimension)], prime)


def _graph(prime, sign):
    return nmod_mat([[2 * int(i == j) for j in range(4)]
                     for i in range(4)] +
                    [[sign * entry for entry in row] for row in PHI], prime)


def _negation_class(point, modulus):
    point = tuple(x % modulus for x in point)
    return min(point, tuple(-x % modulus for x in point))


def _small_order(base, modulus):
    assert 1 < modulus <= 15625 and gcd(base, modulus) == 1
    value = 1
    for exponent in range(1, modulus):
        value = value * base % modulus
        if value == 1:
            return exponent
    raise AssertionError("unit order not found in bounded fixture")


def _prime_power_order(base, prime, exponent):
    """Odd-prime order lifting; enumerate only the small base prime."""
    assert prime > 2 and exponent >= 1
    order = _small_order(base, prime)
    difference = abs(base**order - 1)
    assert difference != 0
    valuation = 0
    while difference % prime == 0:
        difference //= prime
        valuation += 1
    return order * prime**max(0, exponent - valuation)


@pytest.mark.parametrize("primes", [(3,), (3, 5), (3, 5, 7), (3, 5, 7, 13)])
@pytest.mark.parametrize("mask", [1, 2, 11])
def test_unit_square_roots_and_relative_sign_count(primes, mask):
    modulus = prod(primes)
    assert gcd(mask, modulus) == 1
    for prime in primes:
        roots = {x for x in range(prime) if (x*x - mask*mask) % prime == 0}
        assert roots == {mask % prime, -mask % prime}
        assert len(roots) == 2

    # Exhaustive roots are confined to these tiny squarefree fixtures.
    roots = {x for x in range(modulus) if (x*x - mask*mask) % modulus == 0}
    crt_roots = {_crt([sign * mask for sign in signs], primes)
                 for signs in product((-1, 1), repeat=len(primes))}
    assert roots == crt_roots
    assert len(roots) == 2**len(primes)
    assert len({min(x, -x % modulus) for x in roots}) == 2**(len(primes) - 1)


def test_nonunit_square_does_not_have_two_roots_per_prime():
    assert {x for x in range(5) if x*x % 5 == 0} == {0}


def test_raw_unit_mask_is_not_already_an_exact_kummer_image():
    target = tuple(row[0] for row in PHI)
    masked = tuple(2 * x for x in target)
    assert _negation_class(masked, 13) != _negation_class(target, 13)


def test_crt_sign_gauge_preserves_weak_replies_including_composite_queries():
    primes = (3, 5, 13)
    masks = {3: 2, 5: 3, 13: 4, 15: 7, 39: 10, 65: 19, 195: 23}
    assert masks[15] % 3 != masks[3]  # No cross-query mask consistency.
    for signs in product((-1, 1), repeat=len(primes)):
        sign_at = dict(zip(primes, signs))
        for size in range(1, len(primes) + 1):
            for levels in combinations(primes, size):
                modulus = prod(levels)
                epsilon = _crt([sign_at[r] for r in levels], levels)
                mask = masks[modulus]
                assert gcd(mask, modulus) == 1
                assert epsilon*epsilon % modulus == 1
                remasked = mask * epsilon % modulus
                assert remasked*remasked % modulus == mask*mask % modulus
                for row in PHI:
                    for entry in row:
                        assert (remasked * epsilon * entry) % modulus == (mask * entry) % modulus
                for prime in levels:
                    assert epsilon % prime == sign_at[prime] % prime
        if len(set(signs)) > 1:
            assert _crt(signs, primes) not in (1, prod(primes) - 1)


@pytest.mark.parametrize("prime", [5, 13])
def test_both_graph_signs_are_distinct_maximal_isotropic_subspaces(prime):
    assert 2**2 + ELL == 65 and 65 % prime == 0
    phi = nmod_mat(PHI, prime)
    j = _form(4, prime)
    assert j.rank() == 4
    ell_j = nmod_mat([[ELL * int(j[i, k]) for k in range(4)]
                     for i in range(4)], prime)
    assert phi.transpose() * j * phi == ell_j
    assert phi.rank() == 4

    ambient = _form(8, prime)
    assert ambient.rank() == 8
    plus, minus = _graph(prime, 1), _graph(prime, -1)
    for graph in (plus, minus):
        assert graph.rank() == 4 == ambient.nrows() // 2
        assert graph.transpose() * ambient * graph == nmod_mat(4, 4, prime)

    # Different matrices alone would not establish different column spaces.
    joined = nmod_mat([[int(plus[i, j]) for j in range(4)] +
                       [int(minus[i, j]) for j in range(4)]
                      for i in range(8)], prime)
    assert joined.rank() == 8  # The two graph subspaces intersect only at zero.


@pytest.mark.parametrize("prime", [5, 13])
def test_product_kummer_uses_simultaneous_not_componentwise_negation(prime):
    # Arithmetic analogue of the global +/- orbit, not Kummer coordinates.
    source = (2, 0, 0, 0)
    target = tuple(row[0] for row in PHI)
    point = source + target
    simultaneous = tuple(-x for x in point)
    second_only = source + tuple(-x for x in target)
    assert _negation_class(point, prime) == _negation_class(simultaneous, prime)
    assert _negation_class(point, prime) != _negation_class(second_only, prime)
    assert _negation_class(target, prime) == _negation_class(tuple(-x for x in target), prime)


def test_mixed_crt_graph_sign_is_not_one_global_sign():
    epsilon = _crt((1, -1), (5, 13))
    assert epsilon == 51 and epsilon**2 % 65 == 1
    source = (2, 0, 0, 0)
    target = tuple(row[0] for row in PHI)
    mixed = source + tuple(epsilon * x for x in target)
    for sign in (-1, 1):
        uniform = source + tuple(sign * x for x in target)
        assert _negation_class(mixed, 65) != _negation_class(uniform, 65)


@pytest.mark.parametrize("base, prime", [(-11, 3), (-11, 5), (-971, 3)])
@pytest.mark.parametrize("exponent", range(1, 7))
def test_prime_power_order_formula_matches_bounded_exact_orders(base, prime, exponent):
    assert _prime_power_order(base, prime, exponent) == _small_order(base, prime**exponent)


@pytest.mark.parametrize("exponent", [64, 256, 1024])
def test_p11_large_prime_power_order_without_enumeration(exponent):
    modulus = 3**exponent
    order = _prime_power_order(-11, 3, exponent)
    assert order == 3**(exponent - 1)
    assert modulus == 3 * order
    assert pow(-11, order, modulus) == 1
    # The proposed order is a pure power of 3, so this certifies minimality.
    assert pow(-11, order // 3, modulus) != 1


@pytest.mark.parametrize("exponent", range(1, 8))
def test_positive_high_valuation_case_p971(exponent):
    assert 971 % 4 == 3 and 971 + 1 == 4 * 3**5
    assert 3**5 > ELL
    order = _prime_power_order(-971, 3, exponent)
    assert order == 3**max(0, exponent - 5)
    assert pow(-971, order, 3**exponent) == 1
    if exponent <= 5:
        assert order == 1
    else:
        assert pow(-971, order // 3, 3**exponent) != 1
    if exponent == 5:
        assert _prime_power_order(-11, 3, exponent) == 81


@pytest.mark.parametrize("exponent", range(1, 6))
def test_one_odd_prime_power_has_only_a_global_sign_after_normalization(exponent):
    modulus, mask = 3**exponent, 2
    roots = {x for x in range(modulus) if (x*x - mask*mask) % modulus == 0}
    assert roots == {mask % modulus, -mask % modulus}
    for root in roots:
        sign = mask * pow(root, -1, modulus) % modulus
        assert sign in (1, modulus - 1)
        assert _negation_class(tuple(sign * row[0] for row in PHI), modulus) == _negation_class(
            tuple(row[0] for row in PHI), modulus)
