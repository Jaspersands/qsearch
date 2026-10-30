from fractions import Fraction
from collections import Counter
from itertools import combinations, product
from math import factorial, prod

import pytest

from source_tree import (
    adaptive_pool_bound, dependence_probability, filiform_bracket, profile,
    rank_mod,
)


@pytest.mark.parametrize("p,r,k", [(2, 3, 3), (3, 2, 2), (3, 3, 2), (5, 2, 2)])
def test_rank_probability_by_complete_enumeration(p, r, k):
    vectors = tuple(product(range(p), repeat=r))
    dependent = sum(rank_mod(rows, p) < k for rows in product(vectors, repeat=k))
    assert dependence_probability(p, r, k) == Fraction(dependent, p ** (r * k))


@pytest.mark.parametrize("p,r,n", [(3, 2, 1), (3, 2, 2), (3, 2, 3), (2, 3, 3)])
def test_pool_bound_covers_best_adaptive_subset(p, r, n):
    vectors = tuple(product(range(p), repeat=r))
    k = min(n, r)
    bad = 0
    for rows in product(vectors, repeat=n):
        bad += any(rank_mod(subset, p) < k for subset in combinations(rows, k))
    actual = Fraction(bad, p ** (r * n))
    assert actual <= adaptive_pool_bound(p, r, n)
    if n <= r:
        assert actual == adaptive_pool_bound(p, r, n)


@pytest.mark.parametrize("r", [1, 2, 3, 5])
def test_full_spark_support_obstruction(r):
    p = 11
    labels = [tuple(pow(t, i, p) for i in range(r)) for t in range(7)]
    for chosen in combinations(labels, r):
        assert rank_mod(chosen, p) == r
    # Vandermonde controls are deliberately structured, not random-source runs.


def test_linear_dependence_does_not_supply_a_power_witness():
    p = 5
    assert rank_mod([(1,), (2,)], p) == 1
    assert not any(
        (a or b) and (a * a + 2 * b * b) % p == 0
        for a, b in product(range(p), repeat=2)
    )


@pytest.mark.parametrize("p,r", [(3, 2), (5, 3)])
def test_correct_label_marginals_do_not_imply_independent_sources(p, r):
    labels = tuple(product(range(p), repeat=r))
    bank = [(label, tuple(-a % p for a in label)) for label in labels]
    assert Counter(a for a, _ in bank) == Counter(labels)
    assert Counter(b for _, b in bank) == Counter(labels)
    assert all(all((a[j] + b[j]) % p == 0 for j in range(r)) for a, b in bank)
    assert all(rank_mod([a, b], p) < 2 for a, b in bank)
    assert adaptive_pool_bound(p, r, 2) < 1


@pytest.mark.parametrize("p,r,d", [(3, 2, 2), (5, 2, 3), (7, 2, 4)])
def test_nonzero_diagonal_witness_has_dependent_active_labels(p, r, d):
    labels = ((1, 0), (0, 1), (1, 1))
    for scales in product(range(p), repeat=len(labels)):
        active = [label for label, scale in zip(labels, scales) if scale]
        if active and all(
            sum(pow(s, d, p) * label[j] for label, s in zip(labels, scales)) % p == 0
            for j in range(r)
        ):
            assert rank_mod(active, p) < len(active)


@pytest.mark.parametrize("c,p", [(1, 3), (2, 5), (3, 7), (5, 11), (8, 2**127 - 1)])
def test_filiform_actual_lower_central_ranks_and_hidden_line(c, p):
    n = c + 1
    basis = [tuple(int(i == j) for i in range(n)) for j in range(n)]
    current = basis
    ranks = []
    for j in range(1, c + 2):
        ranks.append(rank_mod(current, p))
        current = [
            value for u in basis for v in current
            if any(value := filiform_bracket(u, v, p))
        ]
    assert ranks == [n] + list(range(c - 1, 0, -1)) + [0]
    hidden = (1,) + tuple((i * i + 1) % p for i in range(c))
    for j in range(2, c + 1):
        gamma = basis[j:]
        assert rank_mod(gamma + [hidden], p) == len(gamma) + 1
    if c >= 2:
        # y_0 rather than a terminal central vector witnesses nonnormality.
        assert rank_mod([hidden, filiform_bracket(basis[1], hidden, p)], p) == 2
    for u, v, w in product(basis, repeat=3):
        terms = [filiform_bracket(a, filiform_bracket(b, z, p), p)
                 for a, b, z in [(u, v, w), (v, w, u), (w, u, v)]]
        assert all(sum(term[i] for term in terms) % p == 0 for i in range(n))


@pytest.mark.parametrize("c", [1, 2, 3, 5, 10, 20, 32])
def test_factorial_leaf_cost(c):
    result = profile(c, 2**127 - 1, 100, 0)
    assert result["lifted_leaves_if_no_exception"] == factorial(c)
    assert result["native_copies_if_no_exception"] == c * factorial(c)
    assert not result["general_hsp_lower_bound"]


def test_fixed_public_subdivisions_cannot_lower_product():
    for r in range(1, 10):
        for cuts in product([False, True], repeat=r - 1):
            blocks = [1]
            for cut in cuts:
                if cut:
                    blocks.append(1)
                else:
                    blocks[-1] += 1
            assert prod(b + 1 for b in blocks) >= r + 1


def test_large_field_replay_is_nonvacuous_but_not_a_quantum_run():
    result = profile(32, 2**521 - 1, 10**6, 10**6)
    assert Fraction(1, 100000) < result["terminal_source_success_upper_bound"] < Fraction(1, 50000)
    assert result["native_copies_if_no_exception"] > 10**36
    assert not result["algorithmic_advantage_established"]
    smaller = profile(32, 2**521 - 1, 1000, 1000)
    assert 0 < smaller["terminal_source_success_upper_bound"] < Fraction(1, 10**90)


def test_replay_encodes_large_exact_probabilities_without_decimal_limit():
    from replay import encode
    value = dependence_probability(2**521 - 1, 31, 31)
    encoded = encode(value)
    assert Fraction(int(encoded["numerator_hex"], 16),
                    int(encoded["denominator_hex"], 16)) == value


def test_budget_boundary_and_small_field_can_make_bound_vacuous():
    c, p = 3, 7
    assert profile(c, p, 100, 0)["terminal_source_success_upper_bound"] == 1
    result = profile(c, 2**127 - 1, 5, c * factorial(c))
    assert result["terminal_source_success_upper_bound"] == 1
    assert adaptive_pool_bound(5, 3, 0) == 0
    assert dependence_probability(5, 3, 4) == 1


@pytest.mark.parametrize("args", [(0, 5, 5, 5), (3, 3, 5, 5), (3, 9, 5, 5),
                                    (1, 2, 5, 5), (3, 5, -1, 5), (3, 5, 5, -1)])
def test_invalid_contract_rejected(args):
    with pytest.raises(ValueError):
        profile(*args)
