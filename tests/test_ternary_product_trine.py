from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random
import subprocess

import numpy as np
import pytest

from ternary_covariant_noise import CovariantRecord, phase
from ternary_product_trine import (
    F3, TrineRecord, error_budget, fixed_trine_gate, fixed_trine_gram,
    joint_correlation_control, joint_posterior, physical_compiler_control,
    posterior_control, randomized_outcome, randomized_recipe, uniform_root,
)


@pytest.mark.parametrize("q", [3, 9, 27])
@pytest.mark.parametrize("state", [[1, 0, 0], [0, 1, 0], [1/np.sqrt(14), 2j/np.sqrt(14), -3/np.sqrt(14)]])
def test_randomized_trine_replays_original_qft_receiver_on_arbitrary_inputs(q, state):
    c = physical_compiler_control(q, state)
    assert c["arbitrary_input_not_just_native_phases"]
    assert max(v for k, v in c.items() if k.endswith("residual")) < 2e-12


@pytest.mark.parametrize("q", [3, 9])
def test_every_branch_effect_equals_covariant_effect_over_three_including_off_diagonals(q):
    total = np.zeros((3, 3), dtype=complex)
    for a, b, z in product(range(q), range(q), range(3)):
        y = randomized_outcome(q, a, b, z)
        row = F3[z]*np.array([1, phase(-a, q), phase(-b, q)])
        actual = np.outer(row.conj(), row)/(q*q)
        vector = np.array([1, phase(y[0], q), phase(y[1], q)])
        assert np.max(abs(actual-np.outer(vector, vector.conj())/(3*q*q))) < 1e-14
        total += actual
    assert np.max(abs(total-np.eye(3))) < 1e-12


def test_large_root_recipe_needs_no_exponential_ancilla_or_povm_table():
    c = randomized_recipe(64)
    assert c["clean_quantum_ancillas"] == 0 and c["uniform_independent_public_random_trits"] == 128
    assert not c["full_q_squared_table_required"] and not c["hardware_gate_export_implemented"]
    assert 0 <= uniform_root(64, random.Random(19)) < 3**64
    assert error_budget(Fraction(1, 100), Fraction(1, 100), Fraction(1, 10))["outcome_TV_upper"] == "3/25"
    with pytest.raises(ValueError): error_budget(0, 0, 2)


@pytest.mark.parametrize("q,n", [(3, 1), (9, 1), (27, 1), (3, 2)])
def test_exact_full_label_gram_keeps_zero_and_nonprimitive_secrets(q, n):
    secrets = tuple(product(range(q), repeat=n))
    for s, t in product(secrets, repeat=2):
        expected = (Fraction(2, 3) if any(s) else Fraction(2)) if s == t else Fraction(0)
        assert fixed_trine_gram(q, s, t) == expected


@pytest.mark.parametrize("q,n", [(3, 1), (9, 1), (3, 2)])
def test_actual_born_likelihood_gram_matches_exact_root_character_calculation(q, n):
    secrets = tuple(product(range(q), repeat=n))
    rows = tuple(product(range(q), repeat=n))
    centered = np.array([[3*TrineRecord(a, c, z, q).probability(s)-1 for s in secrets]
                         for a, c, z in product(rows, rows, range(3))])
    actual = centered.T @ centered/len(centered)
    expected = np.diag([2 if not any(s) else 2/3 for s in secrets])
    assert np.max(abs(actual-expected)) < 2e-12


@pytest.mark.parametrize("r", [16, 32, 64])
def test_fixed_readout_exponentially_weak_population_signal_is_not_all_locc_bound(r):
    c = fixed_trine_gate(1, r, r-2)
    assert not c["necessary_copy_gate_passed"]
    assert c["zero_secret_exception_kept"]
    assert Fraction(c["zero_secret_advantage_upper"]) < Fraction(1, 3**r)
    assert Fraction(c["nonzero_contribution_advantage_upper_squared"]) < Fraction(5, 9)**r/2
    assert not c["other_bases_or_adaptive_LOCC_covered"] and not c["unmeasured_states_covered"]


def test_zero_copy_gate_and_large_surplus_are_not_falsely_excluded():
    c = fixed_trine_gate(1, 4, 0)
    assert c["nonzero_contribution_advantage_upper_squared"] == "0"
    assert c["zero_secret_advantage_upper"] == "0" and not c["necessary_copy_gate_passed"]
    assert fixed_trine_gate(1, 4, 100)["necessary_copy_gate_passed"]


def test_actual_optimal_one_copy_success_under_complete_iid_labels_is_bounded():
    q = 9
    success = 0.0
    for a, c, z in product(range(q), range(q), range(3)):
        masses = [sum(TrineRecord((a,), (c,), z, q).probability((s,)) for s in range(t, q, 3))
                  for t in range(3)]
        success += max(masses)/(q**3)
    gate = fixed_trine_gate(1, 2, 1)
    bound = np.sqrt(float(Fraction(gate["nonzero_contribution_advantage_upper_squared"])))+float(Fraction(gate["zero_secret_advantage_upper"]))
    assert success > 1/3 and success-1/3 <= bound


def test_uniform_single_marginals_do_not_imply_uninformative_joint_product_readout():
    c = joint_correlation_control()
    assert c["joint_MAP_success"] == Fraction(19, 27)
    assert c["joint_trit_laws"][0][0] == Fraction(19, 81)
    assert c["joint_trit_laws"][1][0] == Fraction(4, 81)
    assert all(sum(row) == 1 for row in c["joint_trit_laws"])
    assert all(x == Fraction(1, 3) for row in c["single_qutrit_marginals"] for x in row)
    assert c["final_effect_word_Hamming_radius"] == 2 and c["entangling_readout_gates"] == 0
    assert c["prespecified_legal_labels_not_IID_population_evidence"] and not c["speedup_claim_allowed"]


@pytest.mark.parametrize("digits", list(product(range(3), repeat=2)))
def test_exact_posterior_decodes_real_joint_likelihood_not_covariant_data_law(digits):
    records = [TrineRecord((1,), (2,), digits[0], 81), TrineRecord((26,), (52,), digits[1], 81)]
    c = posterior_control(records)
    result = c["solver"]
    assert c["actual_fixed_trine_likelihood_residual"] < 2e-11
    assert not result["paired_covariant_generative_law_used"]
    assert "digit" in result["records"][0] and "outcome" not in result["records"][0]
    assert result["cost_ledger"]["generic_time_not_polynomial"]
    assert not result["polynomial_native_weak_learner_implemented"]


def test_vector_secret_and_non_root_three_phase_cancellations_are_not_discarded():
    records = [TrineRecord((1, 2), (3, 4), 2, 9), TrineRecord((8, 5), (2, 7), 0, 9),
               TrineRecord((4, 0), (1, 3), 1, 9)]
    assert posterior_control(records)["actual_fixed_trine_likelihood_residual"] < 2e-11


def test_impossible_data_and_exhausted_reference_have_no_fake_trit_certificate():
    records = [TrineRecord((0,), (0,), 1, 9)]
    assert joint_posterior(records, [0])["posterior"]["status"] == "ZERO_LIKELIHOOD_DATA_NO_POSTERIOR"
    records = [TrineRecord((1,), (2,), 0, 81), TrineRecord((26,), (52,), 0, 81)]
    c = joint_posterior(records, [0, 1], max_half_states=1)
    assert c["status"] == "EXACT_REFERENCE_BUDGET_EXHAUSTED_NO_POSTERIOR" and c["posterior"] is None
    assert not c["paired_covariant_generative_law_used"] and not c["speedup_claim_allowed"]


def test_records_cannot_smuggle_wrong_models_reused_ancestors_or_illegal_digits():
    with pytest.raises(ValueError): TrineRecord((1,), (2,), True, 9)
    with pytest.raises(ValueError): TrineRecord((1,), (2,), 3, 9)
    with pytest.raises(ValueError): TrineRecord((1,), (2,), 0, 10)
    with pytest.raises(ValueError): joint_posterior([CovariantRecord((1,), (2,), (0, 0), 9)], [0])
    with pytest.raises(ValueError): joint_posterior([TrineRecord((1,), (2,), 0, 9)]*2, [0, 0])
    with pytest.raises(ValueError): joint_posterior([TrineRecord((1,), (2,), 0, 9), TrineRecord((1,), (2,), 0, 27)], [0, 1])
    with pytest.raises(ValueError): physical_compiler_control(3, [float("nan"), 0, 0])
    with pytest.raises(ValueError): fixed_trine_gate(1, 4, True)


@pytest.mark.parametrize("mutation", ["gate", "zero", "scope", "joint", "posterior", "compiler", "promotion"])
def test_standalone_checker_rejects_changed_proof_or_promotion(tmp_path, mutation):
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root/"research/classical_baselines/ternary_product_trine.json").read_text())
    if mutation == "gate": record["fixed_readout_scaling_gates"][0]["necessary_copy_gate_passed"] = True
    if mutation == "zero": record["fixed_readout_scaling_gates"][0]["zero_secret_advantage_upper"] = "0"
    if mutation == "scope": record["fixed_readout_scaling_gates"][0]["other_bases_or_adaptive_LOCC_covered"] = True
    if mutation == "joint": record["joint_correlation_countercontrol"]["joint_trit_laws"][0][0] = "20/81"
    if mutation == "posterior": record["exact_posterior_controls"][0]["solver"]["posterior"]["class_likelihood_numerators"][0] = [["0", "500"]]
    if mutation == "compiler": record["randomized_recipes"][0]["clean_quantum_ancillas"] = 1
    if mutation == "promotion": record["quantum_speedup_proved"] = True
    path = tmp_path/"mutant.json"; path.write_text(json.dumps(record))
    c = subprocess.run(["node", str(root/"research/certificates/ternary_product_trine_crosscheck.js"), str(path)], capture_output=True, text=True)
    assert c.returncode != 0, c.stdout
