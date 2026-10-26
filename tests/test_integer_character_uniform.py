from fractions import Fraction as Q
import json

import pytest

from theorems import integer_character_uniform as uniform


def test_uniform_constants_have_strict_exact_margins():
    cert = uniform.uniform_constants()
    assert cert["minimum_length"] == 20000
    assert Q(cert["edge_tail_upper_coefficient_over_m"])/20000 < Q(1, 40)
    assert Q(cert["mean_squared_lower"]) > Q(cert["mean_cosine_lower"])**2
    assert Q(cert["mean_cosine_lower"]) > Q(3, 10)


@pytest.mark.parametrize("length", [20000, 20001, 20199, 10**6, 10**12])
def test_tail_bounds_include_floor_and_both_sign_counts(length):
    cert = uniform.tail_bounds(length)
    assert cert["cap_each_sign"] == 7*length//200
    assert Q(cert["retained_mass_lower"]) > Q(1, 4)
    assert Q(cert["edge_mass_lower"]) > Q(39, 40)


@pytest.mark.parametrize("length", [0, 19999, True, 20000.0])
def test_no_uniform_claim_below_its_proved_range(length):
    with pytest.raises(ValueError):
        uniform.tail_bounds(length)


def test_error_budget_pays_for_postselection_and_verification():
    cert = uniform.error_budget()
    assert Q(cert["conditional_output_tv_upper"]) == Q(1, 10000)
    assert Q(cert["herald_probability_lower"]) > Q(1, 8)
    assert Q(cert["accepted_given_herald_probability_lower"]) > Q(1, 2000)
    assert Q(cert["accepted_per_trial_probability_lower"]) > Q(1, 16000)
    assert Q(cert["robust_score_threshold"]) == Q(3, 10)+2*Q(1, 100000)


@pytest.mark.parametrize("kwargs", [
    {"retained_mass_lower": Q(1, 5)},
    {"tv_error": Q(1, 2)},
    {"score_error": Q(1, 100)},
    {"mean_lower": 0.9},
])
def test_invalid_or_destructive_error_budgets_are_rejected(kwargs):
    with pytest.raises(ValueError):
        uniform.error_budget(**kwargs)


def test_repetitions_count_failed_source_trials():
    cert = uniform.repetition_certificate(20)
    assert cert["maximum_trials"] == 320000
    assert Q(cert["failure_probability_upper"]) == Q(1, 2**20)
    assert Q(cert["per_trial_success_lower"])*cert["trials_per_failure_bit"] >= 1


@pytest.mark.parametrize("exponent", [2, 3, 4])
def test_crt_fourier_labels_match_exact_characters(exponent):
    q = 3**(exponent-1)
    order = 2*q
    labels = [uniform.crt_character_label(e, v, exponent)
              for e in range(2) for v in range(q)]
    assert sorted(labels) == list(range(order))
    for s in range(order):
        for e in range(2):
            for v in range(q):
                x = uniform.crt_character_label(e, v, exponent)
                assert (s*x-q*(s % 2)*e-2*(s % q)*v) % order == 0


def test_resource_counts_are_blocks_not_fault_tolerant_gates():
    cert = uniform.resource_structure(1024, 584)
    assert cert["cyclic_order_bits"] == 926
    assert cert["qft_ternary_fourier_blocks"] == 583
    assert cert["qft_two_qutrit_controlled_phase_blocks"] == 583*582//2
    blocks = 1+583+583*582//2
    assert Q(cert["qft_per_block_operator_error"])*blocks == Q(1, 20000)
    assert Q(cert["source_per_local_operator_error"])*1024 == Q(1, 80000)
    assert not cert["qft_primitive_counts_are_compiled_gate_counts"]
    assert not cert["concrete_qubit_or_T_count_claimed"]


def test_big_integer_score_controls_and_interval_precision():
    order = 2*3**583
    labels = [1, order-1, order//3+11]
    assignment = order-7
    centers = [a*assignment % order for a in labels]
    lo, hi = uniform.score_interval(labels, centers, order, assignment)
    assert lo <= 1 <= hi
    antipodal = [(c+order//2) % order for c in centers]
    lo, hi = uniform.score_interval(labels, antipodal, order, assignment)
    assert lo <= -1 <= hi
    lo, hi = uniform.score_interval(labels, [0]*3, order, assignment)
    assert -1 <= lo <= hi <= 1
    assert hi-lo < Q(1, 10**20)


def test_score_acceptance_is_a_verified_lower_bound_not_a_float_comparison():
    order = 2*3**583
    labels = [1, order-1, order//3+11]
    assignment = order-7
    centers = [a*assignment % order for a in labels]
    accepted = uniform.verify_score(labels, centers, order, assignment)
    assert accepted["accepted"]
    assert Q(accepted["score_lower"]) >= Q(3, 10)
    rejected = uniform.verify_score(
        labels, [(c+order//2) % order for c in centers], order, assignment)
    assert not rejected["accepted"]
    assert rejected["exact_modular_residues_used"]


@pytest.mark.parametrize("args", [
    ([1], [0.0], 18, 1),
    ([1], [0], 18, 18),
    ([18], [0], 18, 1),
    ([], [], 18, 1),
])
def test_score_verifier_rejects_lossy_or_noncanonical_input(args):
    with pytest.raises(ValueError):
        uniform.score_interval(*args)


def test_live_report_replays_without_quantum_execution_claim():
    saved = json.loads(uniform.REPORT.read_text())
    assert saved == uniform.report()
    assert saved["uniform_constants"]["mean_cosine_lower"] == "601/2000"
    assert not saved["quantum_optimizer_executed"]
    assert not saved["coherent_circuit_compiled"]
    assert not saved["classical_hardness_or_speedup_proved"]
