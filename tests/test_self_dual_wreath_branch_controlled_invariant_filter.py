import pytest

from self_dual_wreath_branch_controlled_invariant_filter import (
    branch_controlled_filter_scaling_record,
    run_branch_controlled_invariant_filter,
    validate_branch_controlled_invariant_filter,
)


def test_physical_branch_filter_is_projective_and_covariant() -> None:
    record = validate_branch_controlled_invariant_filter()
    assert record.physical_carrier_dimension == 144
    assert record.physical_filter_idempotence_residual < 1e-10
    assert record.hidden_conjugation_commutator_residual < 1e-10
    assert record.maximum_selected_sector_annihilation_residual < 1e-10
    assert record.exact_physical_filter_validation


def test_finite_filter_reduces_spike_without_destroying_carrier() -> None:
    record = validate_branch_controlled_invariant_filter()
    assert record.filtered_frame_trace_retention > 0.8
    assert record.unfiltered_frame_top_eigenvalue == pytest.approx(0.5)
    assert record.filtered_frame_top_eigenvalue == pytest.approx(0.375)
    assert record.frame_top_eigenvalue_reduction == pytest.approx(0.125)


def test_expected_natural_filter_loss_is_negligible() -> None:
    record = branch_controlled_filter_scaling_record(128)
    assert record.complete_block_count > 80
    assert record.expected_removed_state_fraction_upper_bound < 1e-200
    assert record.expected_retained_state_fraction == 1.0
    assert record.expected_retained_fraction_tends_to_one
    assert not record.residual_polynomial_frame_norm_proved


def test_report_keeps_residual_spectrum_and_circuit_gates_closed() -> None:
    report = run_branch_controlled_invariant_filter()
    assert report.headline_metrics[
        "finite_physical_filter_validation_failure_count"
    ] == 0
    assert report.claim_gate[
        "branch_controlled_physical_filter_projector_proved"
    ]
    assert report.claim_gate["hidden_conjugation_covariance_proved"]
    assert report.claim_gate[
        "expected_natural_state_retention_one_minus_o_one_proved"
    ]
    assert report.claim_gate["finite_frame_spike_reduction_observed"]
    assert not report.claim_gate["residual_polynomial_frame_norm_proved"]
    assert not report.claim_gate["all_high_frame_spikes_removed"]
    assert not report.claim_gate[
        "fault_tolerant_polynomial_filter_circuit_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
