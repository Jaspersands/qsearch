import pytest

from dcp_low_bit_candidate_list_no_go import (
    audit_exact_low_bit_list_bound,
    conditional_legal_list_success_upper_bound,
    legal_probability_lower_bound,
    low_bit_candidate_list_no_go_theorem,
    low_bit_list_scaling_record,
    run_low_bit_candidate_list_no_go,
)


def test_exact_high_enumeration_obeys_union_bound() -> None:
    control = audit_exact_low_bit_list_bound(4, 2, (1, 1, 3), 2, 2)
    assert control.exact_low_bit_list_bound_verified
    assert control.selected_assignment_count <= 2
    assert control.exact_success_probability <= control.union_bound
    assert control.bound_residual == 0


def test_legal_probability_bound_is_constant_at_fixed_offset() -> None:
    values = [legal_probability_lower_bound(n, 0) for n in (8, 32, 128)]
    assert all(value >= 0.5 for value in values)
    offset_values = [legal_probability_lower_bound(n, 4) for n in (8, 32, 128)]
    assert all(value >= 16 / 17 for value in offset_values)


def test_polynomial_low_bit_list_has_exponential_success_bound() -> None:
    row = low_bit_list_scaling_record(1024, 4, 3, 6)
    assert row.low_bits <= 30
    assert row.quotient_bits >= 994
    assert row.exponentially_small_success
    assert row.log2_conditional_legal_success_upper_bound < -930


def test_conditional_bound_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError, match="low_bits"):
        conditional_legal_list_success_upper_bound(8, 0, 8, 4)
    with pytest.raises(ValueError, match="nonnegative"):
        conditional_legal_list_success_upper_bound(8, 0, 2, -1)
    with pytest.raises(ValueError, match="dimensions"):
        legal_probability_lower_bound(0, 0)


def test_theorem_preserves_joint_and_coherent_routes() -> None:
    theorem = low_bit_candidate_list_no_go_theorem()
    assert theorem.theorem_verified
    assert theorem.low_bit_only_polynomial_list_solver_eliminated
    assert not theorem.joint_low_high_geometry_eliminated
    assert not theorem.coherent_implicit_decoder_eliminated
    assert "not covered" in theorem.scope_limit


def test_report_keeps_speedup_gate_closed() -> None:
    report = run_low_bit_candidate_list_no_go()
    assert report.headline_metrics["low_bit_candidate_list_no_go_theorem_count"] == 1
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert not report.claim_gate["low_bit_only_polynomial_explicit_list_survives"]
    assert report.claim_gate["joint_low_high_preconditioner_survives"]
    assert report.claim_gate["coherent_implicit_low_fiber_decoder_survives"]
    assert not report.claim_gate["speedup_claim_allowed"]
