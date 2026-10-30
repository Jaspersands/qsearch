"""Exact algebraic controls, not candidate toy oracle algorithms."""
from collections import Counter
from fractions import Fraction
from itertools import islice, product

from flint import nmod_mat
import pytest

from theorems.norm_sampler_clock import (
    acceptance_from_count, ag_forecast, clock_bound, count_under_distance_promise,
    exact_full_support_count, projective_vectors, stopped_success_bound,
)


@pytest.mark.parametrize("p,B", [
    (3, [[1, 1, 1, 1]]), (5, [[4, 3, 2, 1]]),
    (5, [[4, 3, 2, 1, 1]]), (5, [[1, 4, 0, 0], [0, 0, 1, 4]]),
])
def test_projective_count_matches_every_native_syndrome(p, B):
    k, m = len(B), len(B[0])
    counts = Counter(tuple(sum(a*b for a, b in zip(row, y)) % p for row in B)
                     for y in product(range(1, p), repeat=m))
    for syndrome in product(range(p), repeat=k):
        result = exact_full_support_count(p, B, syndrome)
        assert result["count"] == counts[syndrome]
        assert result["projective_words"] == (p**k-1)//(p-1)
        mean = Fraction((p-1)**m, p**k)
        theta = Fraction(result["count"], mean)-1
        assert abs(theta) <= clock_bound(p, k, result["rowspace_distance"])["fourier_slack_upper"]


def test_projective_lines_partition_nonzero_vectors():
    p, k = 5, 3
    vectors = [tuple(a*x % p for x in line)
               for line in projective_vectors(p, k) for a in range(1, p)]
    assert len(vectors) == len(set(vectors)) == p**k-1
    assert (0,)*k not in vectors


def test_large_prime_does_not_allocate_a_field_table():
    p = 2**127-1
    assert list(islice(projective_vectors(p, 2), 3)) == [(1, 0), (1, 1), (1, 2)]
    exact = exact_full_support_count(p, [[1, 1, 1, 1]], [0])
    assert exact["count"] == ((p-1)**4+p-1)//p
    assert exact["projective_words"] == 1
    fast = count_under_distance_promise(p, [[1]*4], [0], 4, Fraction(1, 2))
    assert fast["projective_words"] == 0
    assert fast["count"] == Fraction((p-1)**4, p)


def test_both_fptas_branches_and_exact_cutoff():
    B, syndrome = [[1]*4], [0]
    fast = count_under_distance_promise(3, B, syndrome, 4, Fraction(1, 2))
    assert fast["count"] == Fraction(16, 3)
    assert fast["conditional_on_distance_promise"]
    assert not fast["distance_promise_verified"]
    assert abs(fast["count"]-6)/6 <= fast["relative_error_upper"]
    exact = count_under_distance_promise(3, B, syndrome, 4, Fraction(1, 4))
    assert exact["status"] == "EXACT_COUNT" and exact["count"] == 6
    assert exact["projective_words"] < exact["projective_work_upper"]
    assert not exact["conditional_on_distance_promise"]


def test_false_distance_is_not_silently_certified():
    B = [[1, 0, 0, 0]]
    fast = count_under_distance_promise(3, B, [0], 4, Fraction(3, 4))
    assert fast["count"] > 0 and not fast["distance_promise_verified"]
    assert exact_full_support_count(3, B, [0])["count"] == 0
    with pytest.raises(ValueError, match="contradicts"):
        count_under_distance_promise(3, B, [0], 4, Fraction(1, 4))


def test_enumeration_cap_is_unknown_not_a_count_or_hardness_claim():
    result = count_under_distance_promise(3, [[1]*4], [0], 4,
                                         Fraction(1, 4), max_projective=0)
    assert result["status"] == "UNKNOWN_ENUMERATION_CAP"
    assert result["count"] is None and not result["hardness_evidence"]
    assert count_under_distance_promise(3, [[1]*4], [0], 4,
                                       Fraction(1, 4), max_projective=None)["count"] == 6


@pytest.mark.parametrize("outside,syndrome,count,expected", [
    (1, 1, 205, Fraction(13284, 15725)),
    (0, 0, 52, Fraction(67392, 78625)),
])
def test_acceptance_identity_matches_previous_exact_norm_controls(outside, syndrome, count, expected):
    B = [[4, 3, 2, 1]+([1] if outside else [])]
    assert exact_full_support_count(5, B, [syndrome])["count"] == count
    Z = 1+Fraction(4, 625)
    assert acceptance_from_count(5, 1, 4+outside, 4, count, Z) == expected


def test_ideal_normalizer_against_every_coset_and_incident_rank():
    p, k, t, r = 5, 2, 4, 2
    B = [[1, 4, 0, 0], [0, 0, 1, 4]]
    A = [[1, 1, 0, 0], [0, 0, 1, 1]]
    ranks = Counter()
    for lam in product(range(p), repeat=k):
        if not any(lam):
            continue
        c = [sum(lam[j]*B[j][i] for j in range(k)) % p for i in range(t)]
        U = [[row[i]*c[i] % p for i in range(t)] for row in A]
        assert all(sum(x*y for x, y in zip(u, a)) % p == 0 for u in U for a in A)
        rank = nmod_mat(U, p).rank()
        assert rank <= min(r, t-r)
        ranks[rank] += 1
    assert ranks == {1: 8, 2: 16}
    Z_star = 1+sum(Fraction(number, p**(2*rank)) for rank, number in ranks.items())
    moment = 0
    for tail in product(range(p), repeat=4):
        a, b = (0, tail[0], 0, tail[1]), (0, tail[2], 0, tail[3])
        M = [[2*sum(row[i]*a[i]*v[i] for i in range(t)) % p for v in A]
             + [-4*sum(row[i]*b[i]*v[i] for i in range(t)) % p for v in A] for row in B]
        moment += p**(k-nmod_mat(M, p).rank())
    assert Z_star == Fraction(moment, p**(2*t-2*r)) == Fraction(841, 625)
    assert Z_star >= 1+Fraction(p**k-1, p**t)
    assert Z_star < 1+Fraction(p**k-1, p**2)


@pytest.mark.parametrize("p", [3, 5, 7, 11])
def test_all_support_dimension_envelope(p):
    rho = Fraction(p*p-1, p*p)
    for k in range(1, 9):
        for t in range(0, 2*k+4):
            minimum_Z = 1+Fraction(p**k-1, p**t)
            assert rho**t/minimum_Z <= rho**k/(1-Fraction(1, p**k))
            for R in range(t//2+1):
                assert 1+Fraction(p**k-1, p**(2*R)) >= minimum_Z


def test_stopped_policies_do_not_inherit_until_success_expectation_bound():
    u = Fraction(1, 10)
    assert stopped_success_bound(u, 0) == 0
    assert stopped_success_bound(u, 1) == u
    assert stopped_success_bound(u, 5) <= 5*u
    # A one-trial cap completes one trial, less than the until-success 1/u.
    assert 1 < 1/u


@pytest.mark.parametrize("p,e", [(1019, 8), (1019, 64), (1019, 128), (1031, 8)])
def test_ag_square_gap_and_symbolic_clock_are_rigorous(p, e):
    k, d = 5*e+3, 12*e-3
    assert (p-1)**d > p**(2*k)
    result = ag_forecast(p, e)
    assert result["until_success_expected_trials_lower_power_of_two"] == max(0, k//(p*p)-1)
    assert not result["ag_promise_verified"] and not result["native_matrix_generated"]


def test_large_forecast_never_builds_large_native_input_or_huge_exponentials():
    forecast = ag_forecast(1019, 2**40)
    assert forecast["until_success_expected_trials_lower_power_of_two"] > 5_000_000
    assert not forecast["previous_large_field_range"]
    assert not forecast["native_matrix_generated"]


@pytest.mark.parametrize("n", [1, 2, 4])
def test_arbitrarily_accurate_root_count_does_not_give_prefix_counts(n):
    m = 3*n+1
    root = exact_full_support_count(3, [[1]*m], [0])["count"]
    mean = Fraction(2**m, 3)
    assert abs(Fraction(root, mean)-1) == Fraction(1, 2**(3*n))
    assert exact_full_support_count(3, [[1]], [0])["count"] == 0
    assert root > 0  # All-ones prefix of length3n leaves syndrome0 for one nonzero variable.


@pytest.mark.parametrize("p", [True, 2, 9, 15, 2**64])
def test_bad_fields_fail_closed(p):
    with pytest.raises(ValueError):
        clock_bound(p, 1, 4)


def test_bad_shapes_rank_precision_and_square_gap_fail_closed():
    for B, target in [([], []), ([[1], [1]], [0, 0]), ([[1, 2], [1]], [0, 0]), ([[3]], [0]), ([[1]], [])]:
        with pytest.raises(ValueError):
            exact_full_support_count(3, B, target)
    for epsilon in (True, 0.1, 0, 1, -1):
        with pytest.raises(ValueError):
            count_under_distance_promise(3, [[1]*4], [0], 4, epsilon)
    with pytest.raises(ValueError, match="square-gap"):
        count_under_distance_promise(3, [[1]*4], [0], 1, Fraction(1, 2))
