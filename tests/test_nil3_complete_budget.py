"""Exact finite-rank probabilities and uniform retry accounting."""
from fractions import Fraction
from itertools import product

import pytest

from theorems.folded_rs_decoder import affine_solution
from theorems.nil3_complete_budget import (
    ceil_log, controls, cyclic_budget, rank_failure, rank_sample_count, recursion_call_cap,
)


def test_rank_formula_matches_exhaustive_odd_prime_matrices():
    for p, dimension, samples in [(3, 2, 1), (3, 2, 3), (3, 1, 2), (5, 1, 3)]:
        deficient, total = 0, p**(dimension*samples)
        for entries in product(range(p), repeat=dimension*samples):
            rows = [entries[i*dimension:(i+1)*dimension] for i in range(samples)]
            deficient += bool(affine_solution(p, rows, [0]*samples, dimension)["basis"])
        assert rank_failure(p, dimension, samples) == Fraction(deficient, total)


@pytest.mark.parametrize("p", [5, 7, 11, 47])
def test_uniform_rank_schedule_and_worst_case_trivial_input(p):
    error = Fraction(1, 10000)
    for ambient in range(1, 9):
        samples = rank_sample_count(p, ambient, error)
        for actual_rank in range(ambient+1):
            assert rank_failure(p, actual_rank, samples) <= error
        assert rank_failure(p, ambient, ambient-1) == 1


@pytest.mark.parametrize("p,m,n", [(5, 2, 1), (7, 3, 3), (11, 2, 3), (47, 2, 3), (101, 5, 7)])
def test_every_error_term_and_all_original_copies_are_charged(p, m, n):
    result = cyclic_budget(p, m, n, Fraction(1, 1000))
    eta = Fraction(result["per_event_budget"])
    assert all(Fraction(value) <= eta for value in result["failure_terms"].values())
    assert Fraction(result["failure_union_bound"]) <= Fraction(1, 1000)
    assert result["total_original_copy_cap"] == (
        result["normal_intersection_original_copies"]
        +result["quotient_outputs"]*result["original_copies_per_quotient_output"]
        +result["hpgp_original_copy_cap"])
    assert result["hpgp_original_copy_cap"] == (
        result["hpgp_equation_attempts_per_dimension"]
        *result["hpgp_label_attempts_per_packet"]
        *sum((k+1)**2 for k in range(1, n+1)))


def test_stricter_confidence_cannot_reduce_the_copy_cap():
    caps = [cyclic_budget(11, 2, 3, error)["total_original_copy_cap"]
            for error in (Fraction(1, 3), Fraction(1, 100), Fraction(1, 1000000))]
    assert caps == sorted(caps)


def test_exact_logarithms_do_not_round_at_power_boundaries():
    assert ceil_log(5, Fraction(25)) == 2
    assert ceil_log(5, Fraction(126, 5)) == 3
    assert ceil_log(5, Fraction(1)) == 0


def test_recursive_calls_account_for_final_unsuccessful_chain():
    for d in range(1, 12):
        assert recursion_call_cap(d) == d*(d+1)
        assert recursion_call_cap(d) >= d*d


def test_report_cannot_be_mistaken_for_an_executed_hsp_solver():
    result = controls()
    assert result["actual_quantum_copy_consumption"] is None
    assert not result["guarded_dispatch_executed"]
    assert not result["iss_recursion_executed"]
    assert not result["independent_proof_review_complete"]
    with pytest.raises(ValueError, match="abelian"):
        cyclic_budget(11, 3, 0)
