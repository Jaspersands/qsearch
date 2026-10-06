from fractions import Fraction

import pytest

from dcp_carry_source_law import (
    SELECTION, certify_q8_source, overlapping_menu_bound,
    quadratic_variety_inconsistency_control, run_controls,
)


def certificate(low, directions, background=0):
    return certify_q8_source(low, directions, background, selection_model=SELECTION)


def test_disjoint_zero_sum_source_remains_fresh_without_rejection():
    result = certificate([[1, 1, 1, 1]], (3, 12))
    assert result["overlap_span_dimension"] == 0
    assert result["native_acceptance_probability"]["denominator_binary_exponent"] == 0
    assert result["conditional_output_labels_jointly_iid_uniform_mod_four"]
    assert result["conditional_output_entropy_bits"] == 4


def test_overlapping_fresh_outputs_pay_native_not_only_branch_cost():
    result = certificate([[1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1]], (15, 51))
    assert result["overlap_span_dimension"] == 1
    assert result["native_acceptance_probability"]["denominator_binary_exponent"] == 2
    assert result["conditional_output_labels_jointly_iid_uniform_mod_four"]
    assert result["conditional_output_entropy_bits"] == 8
    assert not result["selection_lineage_programmatically_verified"]


def test_accepted_product_states_need_not_have_fresh_iid_labels():
    result = certificate([[1, 1, 1, 1]], (3, 15))
    assert result["acceptance_possible"]
    assert result["retained_overlap_intersection_dimension"] == 1
    assert not result["conditional_output_labels_jointly_iid_uniform_mod_four"]
    assert result["conditional_output_entropy_bits"] == 3
    assert result["conditional_low_output_constraints"] == [
        {"output_low_bit_parity_mask": 1, "target_by_component": [0]}]
    assert result["not_a_claim_that_entropy_deficit_makes_decoding_hard"]
    assert not result["unconditional_mixture_over_low_labels_or_changed_bases_classified"]


def test_background_mixing_does_not_restore_lost_label_entropy():
    reference = certificate([[1, 1, 1, 1]], (3, 15))
    for x in range(16):
        current = certificate([[1, 1, 1, 1]], (3, 15), x)
        assert current["conditional_low_output_constraints"] == reference["conditional_low_output_constraints"]
        assert current["native_acceptance_probability"] == reference["native_acceptance_probability"]


def test_illegal_source_selection_and_nonkernel_directions_are_rejected():
    with pytest.raises(ValueError, match="different source theorem"):
        certify_q8_source([[1, 1]], (3,), selection_model="all-public-label-bits")
    with pytest.raises(ValueError, match="binary residues"):
        certificate([[1, 3]], (3,))
    with pytest.raises(ValueError, match="parity kernel"):
        certificate([[1, 1]], (1,))
    with pytest.raises(ValueError, match="independent"):
        certificate([[1, 1]], (3, 3))
    with pytest.raises(ValueError, match="background"):
        certificate([[1, 1]], (3,), 4)


def test_quadratic_and_cubic_failures_get_zero_native_acceptance():
    quadratic = certificate([[1, 1, 1]], (3, 5))
    assert not quadratic["acceptance_possible"]
    assert quadratic["reason"] == "quadratic parity obstruction"
    cubic = certificate([[1] * 8], (15, 51, 85))
    assert not cubic["acceptance_possible"]
    assert cubic["reason"] == "cubic interaction"


def test_polynomial_menu_does_not_grant_free_high_bit_adaptation():
    result = overlapping_menu_bound(128, 128**2, 128**2)
    value = result["native_probability_any_accepted_overlapping_packet_upper_bound"]
    assert Fraction(int(value["numerator_hex"], 16), 1 << value["denominator_binary_exponent"]) == Fraction(1, 1 << 100)
    assert result["selection_can_use_middle_and_top_public_label_bits"]
    assert not result["outcome_adaptive_retained_subspaces_covered"]
    assert not result["arbitrary_polynomial_subspace_synthesis_covered"]
    assert overlapping_menu_bound(4, 32)["bound_vacuous"]


def test_growing_modulus_strengthens_the_same_native_source_penalty():
    result = overlapping_menu_bound(128, 128**2, 128**2, modulus=128)
    probability = result["native_probability_any_accepted_overlapping_packet_upper_bound"]
    assert probability == {"numerator_hex": "0x1", "denominator_binary_exponent": 612}
    with pytest.raises(ValueError, match="power-of-two"):
        overlapping_menu_bound(8, 1, modulus=12)


def test_source_certificate_scales_without_exhausting_quantum_assignments():
    u = (1 << 64) - 1
    v = ((1 << 32) - 1) | (((1 << 32) - 1) << 64)
    result = certificate([[0] * 128 for _ in range(8)], (u, v))
    assert result["input_qubits"] == 128
    assert result["overlap_span_dimension"] == 1
    assert result["retained_overlap_intersection_dimension"] == 0
    assert result["conditional_output_entropy_bits"] == 32
    assert result["native_acceptance_probability"]["denominator_binary_exponent"] == 8
    assert result["conditional_output_labels_jointly_iid_uniform_mod_four"]


def test_triorthogonal_parity_checks_do_not_replace_divisibility_consistency():
    control = quadratic_variety_inconsistency_control()
    assert control["physical_coordinates"] == 36
    assert control["all_degree_one_two_three_parity_checks_pass"]
    assert control["special_pair_xor_is_zero"]
    assert control["middle_constraint_target_xor"] == 1
    assert not control["certificate"]["acceptance_possible"]


def test_complete_source_controls_preserve_unresolved_claims():
    report = run_controls()
    assert len(report["source_controls"]) == 5
    assert report["physical_background_invariance_checks"] == 176
    assert all(row["higher_bit_tables_exhausted_per_component"] > 0 for row in report["source_controls"])
    assert not report["claim_gate"]["new_decoder"]
    assert not report["claim_gate"]["general_outcome_adaptive_no_go"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
