from collections import Counter
from fractions import Fraction as F
import math
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.linalg import expm

import coherent_sign as c

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hdqi-parent-gap-2026-10-23"))
from parent_gap import build_model


@pytest.mark.parametrize("counts", ((0, 0), (1, 1), (2, 1), (2, 2), (1, 2, 1)))
def test_labelled_histories_keep_correct_repeated_word_multiplicity(counts):
    words = Counter(c.labelled_permutations(counts))
    assert sum(words.values()) == math.factorial(sum(counts))
    assert set(words.values()) == {math.prod(math.factorial(k) for k in counts)}


@pytest.mark.parametrize("edges", ((), ((0, 1),), ((0, 1), (1, 2))))
def test_prepare_phase_unprepare_produces_signed_conditional_mean(edges):
    model = c.s.Model.create([1, -1, F(1, 2)], F(1, 4), edges)
    out = c.finite_unitary_control(model)
    assert out["unitarity_error"] < 1e-13
    assert np.linalg.norm(out["joint"]) == pytest.approx(1)
    assert np.max(np.abs(out["joint"][:, 0]-out["expected_good"])) < 1e-13
    assert np.max(np.abs(out["joint"][:, 0]-c.finite_exact_branch(model, F(1, 100)))) < 1e-13


def test_one_edge_zero_amplitude_is_rejected_coherently_not_floored():
    model = c.s.Model.create([1, 1], F(1, 4), [(0, 1)])
    out = c.finite_unitary_control(model)
    assert out["q"][3] > 0
    assert abs(out["joint"][3, 0]) < 1e-14
    assert np.dot(out["joint"][3], out["joint"][3]) == pytest.approx(out["q"][3])


def test_known_sign_is_essential_even_when_basis_probabilities_match():
    model = c.s.Model.create([1, -1], F(1, 4), [])
    right = c.finite_unitary_control(model)["joint"][:, 0]
    wrong = c.finite_unitary_control(model, include_known_sign=False)["joint"][:, 0]
    assert np.max(np.abs(right*right-wrong*wrong)) < 1e-14
    assert np.linalg.norm(right-wrong) > 0.2
    assert right[1] < 0 and right[2] > 0


def test_discarding_work_is_not_uncomputation_or_a_pure_pilot():
    model = c.s.Model.create([1, 1], F(1, 4), [(0, 1)])
    wrong = c.finite_unitary_control(model, unprepare=False)["joint"]
    rho = wrong @ wrong.T
    assert np.trace(rho) == pytest.approx(1)
    assert np.trace(rho@rho) < 0.9999
    correct = c.finite_unitary_control(model)["joint"][:, 0]
    correct /= np.linalg.norm(correct)
    assert np.linalg.norm(rho-np.outer(correct, correct)) > 1e-3


@pytest.mark.parametrize("edges", ((), ((0, 1),), ((0, 1), (1, 2)),
                                   ((0, 1), (0, 2), (1, 2))))
def test_precise_success_vector_and_cost_against_dense_exponential(edges):
    model = c.s.Model.create([1, -1, F(1, 2)], F(1, 4), edges)
    plan = c.precision_ledger(model)
    finite = c.finite_exact_branch(model, plan["site_tail"])
    matrix = build_model(3, edges, [float(j) for j in model.couplings]).h
    a = expm(-float(model.beta)*matrix/2)[:, 0]
    zc = math.prod(math.cosh(float(model.beta*j)) for j in model.couplings)
    assert np.linalg.norm(finite-a/math.sqrt(zc)) <= float(plan["whole_trial_operator_error"])+1e-14
    assert np.dot(finite, finite) >= float(plan["success_probability_lower"])
    assert np.linalg.norm(finite/np.linalg.norm(finite)-a/np.linalg.norm(a)) <= float(plan["conditional_trace_distance_upper"])


@pytest.mark.parametrize("epsilon,delta", ((F(1, 4), F(1, 4)), (F(1, 1000), F(1, 10000))))
def test_precision_and_repetition_budget_is_exact_and_not_free_postselection(epsilon, delta):
    model = c.s.Model.create([1, 1], F(1, 4), [(0, 1)])
    plan = c.precision_ledger(model, epsilon, delta)
    eta, cb = plan["site_tail"], plan["ratio_upper"]
    assert math.sqrt(float(10*model.m*eta))+float(2*model.m*eta) <= float(epsilon/(16*cb))
    assert plan["abstract_rotation_count_bound"]*plan["per_abstract_rotation_error"] == plan["whole_trial_operator_error"]
    assert plan["max_attempts"]*plan["success_probability_lower"] >= math.log(1/float(delta))
    assert plan["failure_probability_upper"] <= delta
    assert plan["conditional_trace_distance_upper"] <= epsilon
    assert not plan["amplitude_amplification_used"]


def test_zero_and_tiny_couplings_are_supported_without_odd_rejection():
    for beta in (F(0), F(1, 10**200)):
        model = c.s.Model.create([0, 1], beta, [])
        plan = c.precision_ledger(model)
        assert plan["ratio_upper"] == 1
        even, odd, proposal = c.tables(model, plan["site_tail"])
        assert odd[0] is None
        assert proposal[0].probabilities()[1][1] == 0
        if beta:
            assert proposal[1].probabilities()[1][1] > 0
            assert odd[1].law.outcomes == (1,)
        else:
            assert plan["max_word_letters"] == 0


def test_finite_controls_refuse_to_be_used_as_scalable_preparations():
    model = c.s.Model.create([1]*4, F(1, 4), [])
    with pytest.raises(ValueError):
        c.finite_unitary_control(model)
    with pytest.raises(ValueError):
        c.finite_exact_branch(model, F(1, 100))
    with pytest.raises(ValueError):
        tuple(c.labelled_permutations((8,)))
    with pytest.raises(ValueError):
        c.precision_ledger(model, epsilon=F(1, 2))


def test_large_model_only_builds_polynomial_local_tables_and_records_scope():
    model = c.s.Model.create([1]*128, F(1, 8), [(i, i+1) for i in range(127)])
    plan = c.precision_ledger(model)
    assert plan["local_table_entries"] < 20*model.m
    assert plan["max_word_letters"] < 20*model.m
    assert plan["max_attempts"] == 24
    assert plan["shuffle_history_bits_bound"] > 0
    assert not plan["quantum_execution"] and not plan["is_compiled_gate_count"]

