"""The zero-sum node of the Rees Schedule 3 forest at kappa_d = p-1 (theorems/rees_zero_sum_node.py)."""

from __future__ import annotations

import random
from fractions import Fraction as F
from itertools import product

import pytest

from theorems import rees_zero_sum_node as z


def test_witness_equivalence_d_equals_p_minus_1():
    # s^(p-1) is 1 off zero, so a witness is exactly a nonempty zero-sum support.
    p, d = 5, 4
    lab = [(1, 2), (4, 3), (2, 2)]
    for s in product(range(p), repeat=3):
        T = [i for i in range(3) if s[i]]
        zs = bool(T) and all(sum(lab[i][j] for i in T) % p == 0 for j in range(2))
        assert z.is_witness(lab, s, p, d) == zs


@pytest.mark.parametrize("p,a,M", [(2, 2, 3), (3, 1, 3), (3, 2, 3), (5, 1, 3), (5, 2, 2)])
def test_moments_and_bound_by_enumeration(p, a, M):
    e1, e2, none = z.count_moments(p, a, M)
    pe1, pe2 = z.predicted_moments(p, a, M)
    assert (e1, e2) == (pe1, pe2)
    assert none == z.exact_zero_sum_free_probability(p, a, M)
    assert none <= z.second_moment_bound(p, a, M)


@pytest.mark.parametrize("p,a", [(3, 1), (3, 2), (5, 1), (7, 1), (2, 3)])
def test_davenport_arity_exact_and_tight(p, a):
    assert z.exact_zero_sum_free_probability(p, a, z.davenport_arity(p, a)) == 0
    bank = [tuple(int(j == i) for j in range(a)) for i in range(a) for _ in range(p - 1)]
    assert z.exhaustive_zero_sum(bank, p)[0] is None and z.dp_zero_sum(bank, p)[0] is None


def test_searches_agree_and_return_witnesses():
    rng = random.Random(1)
    for _ in range(400):
        p = rng.choice((3, 5, 7))
        g = rng.randint(1, 3)
        M = rng.randint(1, 7)
        lab = [tuple(rng.randrange(p) for _ in range(g)) for _ in range(M)]
        s1, _ = z.exhaustive_zero_sum(lab, p)
        s2, big = z.dp_zero_sum(lab, p)
        assert (s1 is None) == (s2 is None)
        assert big <= min(2 ** M - 1, p ** g)
        for s in (s1, s2):
            if s is not None:
                assert z.is_witness(lab, s, p, p - 1)


@pytest.mark.parametrize("p,g", [(3, 1), (5, 2), (7, 3), (11, 1)])
@pytest.mark.parametrize("tau", [F(1, 2), F(1, 1000), F(1, 3 ** 20)])
def test_arities(p, g, tau):
    Me = z.zero_sum_arity_explicit(p, g, tau)
    Ml = z.zero_sum_arity_least(p, g, tau)
    # explicit uses p^g in place of p^g - 1 and a spare factor 2, so it can exceed the least by 2
    assert Ml <= Me <= Ml + 2
    assert z.second_moment_bound(p, g, Me) < tau and z.second_moment_bound(p, g, Ml) <= tau
    assert Ml == 1 or z.second_moment_bound(p, g, Ml - 1) > tau


def test_filiform_budgets():
    # Schedule 1 at Gamma_0 reproduces the B.5 numbers of the 2026-11-04 fcs-budget report.
    expect_s1 = {3: 58.9, 5: 155.8, 9: 676.8}
    expect_det = {3: 13.2, 5: 24.3, 9: 42.3}
    for r, p in z.CASES:
        prof = z.filiform_profile(r)
        s1 = z.budget_p_c_plus_1(prof, p, variant="S1")
        det = z.budget_p_c_plus_1(prof, p, variant="davenport")
        least = z.budget_p_c_plus_1(prof, p, variant="least")
        assert round(s1["log2_Q"], 1) == expect_s1[r]
        assert round(det["log2_Q"], 1) == expect_det[r]
        assert det["M_d0"] == p and least["M_d0"] > det["M_d0"]
        for row in (s1, det, least):
            assert row["budget_ok"]
