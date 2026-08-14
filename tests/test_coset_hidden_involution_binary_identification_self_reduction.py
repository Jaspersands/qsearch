import pytest

from coset_hidden_involution_binary_identification_self_reduction import (
    audit_batched_known_edge_character_reduction,
    audit_edge_dephasing_reduction,
    binary_identification_scaling_record,
    build_binary_identification_self_reduction_report,
    write_binary_identification_self_reduction_report,
)


def test_edge_dephasing_is_exact_membership_channel():
    row = audit_edge_dephasing_reduction(4)
    assert row.exact_edge_membership_channel_verified
    assert row.true_edge_in_subgroup
    assert not row.false_edge_in_subgroup
    assert row.true_dephasing_preservation_residual < 1e-8
    assert row.false_dephasing_to_null_residual < 1e-8
    assert row.true_conditional_subgroup_state_residual < 1e-8
    assert row.false_conditional_subgroup_null_residual < 1e-8
    assert row.known_swap_plus_probability == pytest.approx(0.5)
    assert row.known_swap_plus_probability_under_null == pytest.approx(0.5)
    assert row.true_reduced_hidden_state_residual < 1e-8
    assert row.false_reduced_null_state_residual < 1e-8


@pytest.mark.parametrize("spec", ((1, 2), (2, 1), (3, 1), (4, 1)))
def test_all_known_edges_are_batched_at_constant_success(spec):
    row = audit_batched_known_edge_character_reduction(*spec)
    assert row.exact_batched_character_reduction_verified
    assert row.positive_character_count * 2 == row.character_count
    assert row.positive_character_total_probability == pytest.approx(0.5)
    assert row.positive_character_total_probability_under_null == pytest.approx(0.5)
    assert row.maximum_positive_hidden_state_residual < 1e-8
    assert row.maximum_negative_hidden_state_residual < 1e-8
    assert row.maximum_null_state_residual < 1e-8
    assert not row.recursion_depth_compounds_postselection


def test_scaling_is_polynomial_given_polynomial_binary_detector():
    rows = [binary_identification_scaling_record(m) for m in (2, 3, 4, 8, 16, 32)]
    assert all(
        row.worst_case_edge_membership_test_count == row.half_degree**2 - 1
        for row in rows
    )
    assert all(
        row.polynomial_binary_detector_implies_polynomial_identifier
        for row in rows
    )
    assert all(
        row.polynomial_identifier_implies_polynomial_binary_detector
        for row in rows
    )
    assert all(not row.efficient_binary_detector_constructed for row in rows)
    with pytest.raises(ValueError, match="at least two"):
        binary_identification_scaling_record(1)


def test_report_proves_equivalence_without_claiming_detector(tmp_path):
    report = build_binary_identification_self_reduction_report(
        scaling_half_degrees=(2, 3, 4, 8, 16),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_subgroup_dephasing_proved
    assert report.theorem.constant_success_batched_recursion_proved
    assert report.theorem.binary_to_identification_polynomial_reduction_proved
    assert report.theorem.identification_to_binary_polynomial_reduction_proved
    assert not report.theorem.efficient_binary_detector_constructed
    assert not report.theorem.hidden_involution_algorithm_constructed
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_binary_identification_self_reduction_report(
        tmp_path / "binary-identification.json",
        scaling_half_degrees=(2, 3, 4, 8),
    )
    assert payload["status"] == (
        "binary-identification-polynomial-equivalence-proved-detector-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0


def test_invalid_finite_controls_are_rejected():
    with pytest.raises(ValueError, match="even n"):
        audit_edge_dephasing_reduction(3)
    with pytest.raises(ValueError, match="intentionally limited"):
        audit_edge_dephasing_reduction(6)
    with pytest.raises(ValueError, match="positive"):
        audit_batched_known_edge_character_reduction(0, 1)
