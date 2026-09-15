from fractions import Fraction
import json
import math

import numpy as np
import pytest
from sympy.functions.combinatorial.numbers import partition

from coset_mask_tail_fidelity import regular_selector_query_control
from coset_selector_coefficient_mass import (audit_coefficient_mass_channel_bound,
    coefficient_mass_scaling_controls, exact_shifted_character_square_audit, involution_rotation_word,
    exact_single_irrep_reflection_controls)
from coset_selector_schur import _batch_kron, _source_kernels
from isotypic_instruments import source_selector_coefficient_mass_contract as contract


FLAGS = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
    unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
    no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
    source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
    physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True,
    declared_coefficient_mass_bound_holds=True)


def test_cross_isometries_and_tensor_products_match_full_physical_channels():
    report = audit_coefficient_mass_channel_bound()
    assert report["verified"]
    assert sum(c["group_pairs_checked"] for c in report["cross_channel_controls"]) == 612
    assert sum(c["ancilla_operator_probes"] for c in report["cross_channel_controls"]) == 192
    for row in report["cross_channel_controls"]:
        assert row["hidden_members_checked"] == 3
        assert max(row["errors"].values()) < 1e-8
    assert sum(c["source_tuples_checked"] for c in report["tensor_controls"]) == 61
    for row in report["tensor_controls"]:
        assert max(row["physical_reconstruction_residual"], row["tensor_telescoping_residual"]) < 1e-8
    for flag in ("all_common_queries_nontrivially_obstructed", "classical_sampler_supplied",
                 "formal_proof_verification", "independent_review", "novelty_established"):
        assert not report[flag]
    json.dumps(report, allow_nan=False)


def test_exact_shifted_character_sums_cover_every_shift_including_the_identity():
    rows = exact_shifted_character_square_audit()
    assert sum(r["shifts_checked"] for r in rows) == 750
    for row in rows:
        assert row["verified"]
        assert Fraction(row["exact_full_group_cap"]) == Fraction(row["class_count"], row["hidden_members_checked"])
        assert Fraction(row["exact_maximum_shifted_square_average"]) <= Fraction(row["exact_full_group_cap"])


def test_averaging_the_hidden_member_before_tensoring_is_detectably_wrong():
    data, _, _, a, _ = regular_selector_query_control(3)
    p = data[3][:, None]*data[2]/len(a)
    kernels = np.array([_source_kernels(p+p[:, h], data[6], data[7]) for h in data[8]])
    actual = np.mean([_batch_kron(b[1], b[1]) for b in kernels], axis=0)
    averaged = kernels.mean(axis=0)[1]
    assert np.max(np.abs(actual-_batch_kron(averaged, averaged))) > .001


def test_rotation_word_coefficients_are_exact_and_l2_normalization_is_not_l1_normalization():
    data, _, _, _, _ = regular_selector_query_control(3)
    v, w = int(data[8][0][0]), int(data[8][1][0])
    for word in ([], [v], [v, w], [v, w, v, w, v]):
        row = involution_rotation_word(data, word)
        assert sum(x*x+y*y for x, y in row["gaussian_integer_coefficients"]) == 2**len(word)
        assert row["coefficient_l1_squared_upper_bound"] == 2**len(word)
        assert not row["arbitrary_gate_count_lower_bound"]
    one = involution_rotation_word(data, [v])
    assert one["support_size"] == 2
    assert sum(math.hypot(x, y) for x, y in one["gaussian_integer_coefficients"])**2/one["normalization_squared"] == pytest.approx(2)
    for bad in ([0], [True], [len(data[0])], [int(next(g for g in range(len(data[0])) if data[6][g] != g))]):
        with pytest.raises(ValueError):
            involution_rotation_word(data, bad)


def test_all_mask_scaling_is_nontrivial_only_with_a_useful_query_mass_certificate():
    rows = coefficient_mass_scaling_controls()
    assert [r["average_individual_trace_distance_upper_bound_power_of_two"] for r in rows] == [
        -133, -19, -35, 0, -143, -894, -400, -336, 0, -909, -2097, -1093, -837, 0, -2113]
    for row in rows:
        assert row["covers_all_fixed_selector_masks"]
        assert not row["covers_all_common_group_algebra_queries_nontrivially"]
        assert not row["raw_copy_cap_applied_to_average_individual_distance"]
        assert not row["coefficient_mass_is_a_general_gate_lower_bound"]
        assert row["class_decision_trace_distance_upper_bound_power_of_two"] == row["average_individual_trace_distance_upper_bound_power_of_two"]
        n = row["degree"]
        b = Fraction(row["effective_coefficient_l1_squared_upper_bound"])
        square = Fraction(4*n**4*int(partition(n)), math.prod(range(1, n, 2)))*b*b
        power = row["average_individual_trace_distance_upper_bound_power_of_two"]
        assert min(1, square) <= Fraction(2)**(2*power)
        if power < 0:
            assert square > Fraction(2)**(2*(power-1))
    assert contract(128, 10**100, 1, **FLAGS)["bound_is_vacuous"]


@pytest.mark.parametrize("flag", FLAGS)
def test_every_architecture_and_coefficient_assumption_is_required(flag):
    row = contract(128, 100, 1, **dict(FLAGS, **{flag: False}))
    assert not row["applicable"] and not row["covers_all_fixed_selector_masks"]
    assert row["average_individual_trace_distance_upper_bound_power_of_two"] is None
    with pytest.raises(ValueError):
        contract(128, 100, 1, **dict(FLAGS, **{flag: 1}))


@pytest.mark.parametrize("n,k,b", ((7, 1, 1), (9, 1, 1), (8, True, 1), (8, 0, 1),
    (8, 1, True), (8, 1, .5), (8, 1, 0), (8, 1, Fraction(1, 2)), (True, 1, 1)))
def test_invalid_mass_and_degree_inputs(n, k, b):
    with pytest.raises(ValueError):
        contract(n, k, b, **FLAGS)


def test_large_dense_certificate_remains_serializable_without_disabling_integer_safety_limits():
    row = contract(4096, 4096**2, math.factorial(4096), **FLAGS)
    assert row["bound_is_vacuous"]
    encoded = row["effective_coefficient_l1_squared_upper_bound"]
    assert Fraction(int(encoded["numerator_hex"], 16), int(encoded["denominator_hex"], 16)) == math.factorial(4096)
    json.dumps(row, allow_nan=False)


def test_low_dimensional_irrep_reflections_can_be_dense_but_still_fail_the_coefficient_mass_gate():
    controls = exact_single_irrep_reflection_controls()
    assert len(controls) == 19 and all(row["verified"] for row in controls)
    for row in controls:
        assert Fraction(row["exact_coefficient_l1"]) <= row["coefficient_l1_upper_bound"]
        if row["is_sign_irrep"]:
            n = row["degree"]
            assert Fraction(row["exact_coefficient_l1"]) == 3-Fraction(4, math.factorial(n))
            assert Fraction(row["exact_squared_coefficient_l1"]) < 9
            assert row["is_missing_harmonic_for_this_hidden_class"] == (n in (3, 6))
    assert any(row["is_sign_irrep"] and not row["is_missing_harmonic_for_this_hidden_class"] for row in controls)


def test_coefficient_proof_gate_requires_all_local_and_tensor_evidence(tmp_path, monkeypatch):
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    keys = ("finite_complete_channel_evaluation_verified", "source_character_square_bound_verified",
        "selector_cross_channel_isometry_controls_verified", "selector_coefficient_tensor_hybrid_controls_verified",
        "selector_shifted_character_square_average_verified", "selector_coefficient_mass_all_fixed_masks_bound_derived")
    gate = dict.fromkeys(keys, True)
    path.write_text(json.dumps({"claim_gate": gate}))
    lemmas = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")
    assert len(lemmas) == len({row.id for row in lemmas})
    assert lemmas[22].status == "derived-selector-coefficient-mass-bound-review-pending"
    for missing in keys:
        path.write_text(json.dumps({"claim_gate": dict(gate, **{missing: False})}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[22].status == "blocked-selector-coefficient-mass-evidence-missing"
