from copy import deepcopy
from fractions import Fraction
from math import comb
import json
import subprocess

import numpy as np
import pytest

from theorems import dcp_physical_bad_register_lineage as A


def stored():
    return json.loads(A.REPORT.read_text())


def node_check(payload):
    return subprocess.run([
        "node", "-e",
        "const A=require('./research/certificates/dcp_physical_bad_register_lineage_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(A.verify(JSON.parse(s)))));",
    ], input=json.dumps(payload), text=True, capture_output=True, cwd=A.ROOT)


@pytest.mark.parametrize("p,b,q,c", (
    ("0", "1/2", "0", "1/2"), ("0", "1/2", "1", "1"),
    ("1", "0", "0", "1/2"), ("1", "1", "1", "1"),
    ("1/32", "1/2", "1/32", "1/2"), ("1/32", "1", "1/32", "1"),
))
def test_actual_CNOT_branches_match_density_formulas(p, b, q, c):
    left = A.source_density(32, 11, "left", p, b)
    right = A.source_density(32, 7, "right", q, c)
    total = Fraction(0)
    for branch in (0, 1):
        result, out = A.merge(left, right, branch, independent_given_secret=True)
        prob, literal = A.literal_merge(left, right, branch, 13)
        total += Fraction(result["exact_branch_probability"])
        assert prob == pytest.approx(float(Fraction(result["exact_branch_probability"])))
        if out is None:
            assert literal is None
        else:
            assert out.literal_density(13) == pytest.approx(literal)
            assert np.linalg.eigvalsh(literal).min() >= -1e-12
            assert np.trace(literal).real == pytest.approx(1)
    assert total == 1


def test_bad_zero_bad_zero_is_deterministic_not_half_probability():
    left = A.source_density(32, 11, "left", "1", "1")
    right = A.source_density(32, 7, "right", "1", "1")
    yes, out = A.merge(left, right, 0, independent_given_secret=True)
    no, impossible = A.merge(left, right, 1, independent_given_secret=True)
    assert yes["exact_branch_probability"] == "1"
    assert out.phase_visibility == 0
    assert no["exact_branch_probability"] == "0"
    assert impossible is None
    assert no["status"] == "IMPOSSIBLE_BRANCH_NOT_A_POSTSELECTED_STATE"


def test_bad_basis_in_either_input_destroys_this_combiner_coherence():
    for bad_left in (False, True):
        left = A.source_density(32, 11, "left", "1" if bad_left else "0", "0")
        right = A.source_density(32, 7, "right", "0" if bad_left else "1", "1")
        for branch in (0, 1):
            _, out = A.merge(left, right, branch, independent_given_secret=True)
            assert out.phase_visibility == 0


def test_zero_label_visibility_is_not_hidden_secret_information():
    left = A.source_density(32, 7, "left", "0")
    right = A.source_density(32, 7, "right", "0")
    _, out = A.merge(left, right, 1, independent_given_secret=True)
    assert out.label == 0 and out.phase_visibility == 1
    assert out.literal_density(0) == pytest.approx(out.literal_density(13))
    assert not out.audit_record()["phase_visibility_alone_certifies_secret_information_at_zero_label"]


def test_balanced_visibility_multiplies_for_every_branch_in_actual_disjoint_tree():
    p, leaves = Fraction(1, 32), 16
    states = [A.source_density(64, 2 * j + 1, f"original:{j}", p) for j in range(leaves)]
    layer = 0
    while len(states) > 1:
        next_layer = []
        for j in range(0, len(states), 2):
            result, out = A.merge(states[j], states[j + 1], (j + layer) % 2, independent_given_secret=True)
            assert result["exact_branch_probability"] == "1/2"
            next_layer.append(out)
        states = next_layer
        layer += 1
    assert states[0].phase_visibility == (1 - p) ** leaves
    assert len(states[0].source_ids) == leaves
    assert states[0].merge_depth == 4


def test_reused_ancestors_are_not_free_independent_state_copies():
    state = A.source_density(32, 7, "original", "1/32")
    with pytest.raises(ValueError, match="ancestors"):
        A.merge(state, state, 0, independent_given_secret=True)


def test_conditional_product_noise_is_required_in_addition_to_disjoint_IDs():
    left = A.source_density(32, 11, "left", "1/32")
    right = A.source_density(32, 7, "right", "1/32")
    with pytest.raises(ValueError, match="product source"):
        A.merge(left, right, 0)
    counter = A.correlated_noise_countercontrol()
    assert counter["literal_joint_branches"][1]["exact_output_visibility"] == "1"
    independent, _ = A.merge(left, right, 1, independent_given_secret=True)
    assert Fraction(independent["output_audit"]["PRIVATE_density_phase_visibility"]) < 1
    assert not counter["IDs_or_marginal_rates_prove_independence"]


def test_one_copy_bad_flag_is_not_available_without_unknown_phase_information():
    c = A.one_register_heralding_control()
    assert c["exact_uniform_secret_good_density"] == c["exact_balanced_bad_density"]
    assert c["diagnostic_same_good_bad_probabilities"] == pytest.approx((.5, .5, .5, .5, 1))
    assert c["PSD_effect_rejecting_both_bad_basis_states_must_be_zero"]
    assert not c["all_collective_or_posterior_conditioned_purification_excluded"]


def test_balanced_bad_subclass_reuses_existing_physical_Z_without_full_promise_promotion():
    bridge = A.physical_Z_subclass_bridge()
    assert bridge["equivalent_physical_Z_flip_rate"] == "1/10"
    assert bridge["diagnostic_balanced_density_channel_error"] < 1e-12
    assert bridge["diagnostic_biased_basis_density_channel_error"] == pytest.approx(.1)
    for row in bridge["existing_packet_noise_contrasts"]:
        assert Fraction(row["exact_existing_physical_Z_contrast"]) == Fraction(4, 5) ** row["original_physical_phase_error_support"]
    assert not bridge["FULL_arbitrary_basis_contamination_promise_covered_by_existing_physical_Z"]
    assert not bridge["unknown_coset_phases_are_made_classically_known_by_noise_bridge"]


def test_exact_and_capped_lineage_bounds_do_not_fake_zero_or_general_no_go():
    mild = A.balanced_lineage_ledger(32, 1, 6)
    exact = Fraction(31, 32) ** 64
    assert Fraction(mild["visibility_exact_power_box"]["lower"]) <= exact <= Fraction(mild["output_phase_visibility_upper"])
    harsh = A.balanced_lineage_ledger(1024, 1, 32)
    assert harsh["visibility_exact_power_box"]["status"] == "UNKNOWN_EXACT_POWER_CAP"
    assert 0 < Fraction(harsh["output_phase_visibility_upper"]) <= Fraction(1, 2 ** 192)
    assert harsh["label_target_success_certifies_phase_information"] is False
    assert harsh["visibility_bound_is_for_LEGAL_MAX_RATE_BALANCED_subclass_NOT_all_smaller_rates"]
    assert not harsh["arbitrary_collective_DCP_decoder_or_fault_correction_excluded"]


def test_exact_commuting_parity_laws_respect_copy_lower_bound():
    gamma = Fraction(1, 4)
    minimum = int(np.ceil(float(1 / (8 * gamma * gamma))))
    for copies in range(1, minimum):
        total_variation = sum(Fraction(comb(copies, k), 1) * abs(((1 + gamma) / 2) ** k * ((1 - gamma) / 2) ** (copies - k)
                              - ((1 - gamma) / 2) ** k * ((1 + gamma) / 2) ** (copies - k))
                              for k in range(copies + 1)) / 2
        assert (1 + total_variation) / 2 < Fraction(3, 4)


def test_density_audit_parameters_are_not_in_solver_view():
    state = A.source_density(32, 7, "original", "1/32")
    view = state.public_solver_view()
    assert set(view) == {"modulus", "measured_Fourier_label", "original_state_receipt_IDs", "merge_depth"}
    assert "PRIVATE_density_phase_visibility" not in view


def test_original_source_receipts_are_immutable_copies_not_shared_mutable_lists():
    ids = ["original"]
    state = A.PhaseDensity(32, 7, ids, Fraction(1, 2), Fraction(1))
    ids.append("fabricated")
    assert state.source_ids == ("original",)
    assert state.public_solver_view()["original_state_receipt_IDs"] == ("original",)


def test_float_underflow_does_not_fabricate_an_impossible_branch():
    left = A.PhaseDensity(32, 7, ("left",), Fraction(1, 10 ** 800), Fraction(0))
    right = A.PhaseDensity(32, 11, ("right",), Fraction(1), Fraction(0))
    result, out = A.merge(left, right, 0, independent_given_secret=True)
    assert Fraction(result["exact_branch_probability"]) > 0
    assert out is not None
    with pytest.raises(ArithmeticError, match="underflow"):
        A.literal_merge(left, right, 0, 13)


def test_reduction_noise_repair_is_not_variable_f_polynomial_theorem():
    p = A.reduction_noise_tradeoff(32)
    assert p["published_DCP_log2N"] == 4128
    assert p["minimum_integer_f_for_Bernoulli_visibility_lower_at_least_half"] >= 6
    assert p["diagnostic_approximation_exceeds_LLL_2_to_nminus1over2"]
    assert not p["variable_f_is_covered_by_constant_f_polynomial_reduction"]
    assert not p["different_sieves_or_collective_noise_handling_excluded"]


@pytest.mark.parametrize("call", (
    lambda: A.PhaseDensity(32, 7, ("a",), Fraction(0), Fraction(1)),
    lambda: A.PhaseDensity(32, 32, ("a",), Fraction(1, 2), Fraction(1)),
    lambda: A.source_density(32, 7, "a", "-1/2"),
    lambda: A.balanced_lineage_ledger(2, 1, 3),
    lambda: A.balanced_lineage_ledger(32, 1, 4097),
    lambda: A.reduction_noise_tradeoff(4097),
))
def test_physical_density_and_whole_work_scope_validation(call):
    with pytest.raises(ValueError):
        call()


def test_independent_checker_replays_full_current_audit():
    result = node_check(stored())
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["verified"]


@pytest.mark.parametrize("kind", (
    "branch-probability", "visibility", "impossible", "lineage", "power", "parity-price", "allowed-source-scope",
    "global-no-go", "variable-f", "prime-price", "phase-evaluator", "full-family", "actual-producer", "hash",
    "independence", "correlated-law", "herald-free-flag", "zero-label-information", "noise-bridge-rate", "noise-bridge-full-coverage",
))
def test_independent_checker_rejects_physical_information_and_access_tampering(kind):
    p = deepcopy(stored())
    control = p["literal_physical_merge_controls"][4]
    line = p["balanced_bad_register_lineage_profiles"][6]
    if kind == "branch-probability":
        control["literal_branches"][0]["merge"]["exact_branch_probability"] = "1"
    elif kind == "visibility":
        control["literal_branches"][0]["merge"]["output_audit"]["PRIVATE_density_phase_visibility"] = "1"
    elif kind == "impossible":
        p["literal_physical_merge_controls"][3]["literal_branches"][1]["merge"]["status"] = "ACTUAL_CNOT_MEASURED_TARGET_BRANCH"
    elif kind == "lineage":
        line["disjoint_original_state_leaves"] = "1"
    elif kind == "power":
        line["output_phase_visibility_upper"] = "1"
    elif kind == "parity-price":
        line["necessary_INDEPENDENT_target_copies_for_parity_success3over4_lower"] = "1"
    elif kind == "allowed-source-scope":
        line["visibility_bound_is_for_LEGAL_MAX_RATE_BALANCED_subclass_NOT_all_smaller_rates"] = False
    elif kind == "global-no-go":
        line["arbitrary_collective_DCP_decoder_or_fault_correction_excluded"] = True
    elif kind == "variable-f":
        p["source_reduction_failure_tradeoffs"][1]["variable_f_is_covered_by_constant_f_polynomial_reduction"] = True
    elif kind == "prime-price":
        p["source_reduction_failure_tradeoffs"][1]["published_prime_lower_bound_n_power"] = 4
    elif kind == "phase-evaluator":
        p["coherent_phase_evaluator_or_chosen_label_queries_supplied"] = True
    elif kind == "full-family":
        p["existing_state_input_theorem_contract"]["full_family_coverage"] = True
    elif kind == "actual-producer":
        p["actual_lattice_to_coset_state_generator_implemented"] = True
    elif kind == "independence":
        line["source_ID_uniqueness_establishes_statistical_independence"] = True
    elif kind == "correlated-law":
        p["correlated_bad_register_countercontrol"]["marginal_product_CNOT_formula_applies"] = True
    elif kind == "herald-free-flag":
        p["single_register_heralding_countercontrol"]["source_phase_or_other_register_information_given_to_filter"] = True
    elif kind == "zero-label-information":
        control["input_audits"][0]["phase_visibility_alone_certifies_secret_information_at_zero_label"] = True
    elif kind == "noise-bridge-rate":
        p["existing_physical_Z_balanced_subclass_bridge"]["equivalent_physical_Z_flip_rate"] = "1/5"
    elif kind == "noise-bridge-full-coverage":
        p["existing_physical_Z_balanced_subclass_bridge"]["FULL_arbitrary_basis_contamination_promise_covered_by_existing_physical_Z"] = True
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
