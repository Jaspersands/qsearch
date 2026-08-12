from __future__ import annotations

import math

import pytest

from self_dual_wreath_final_root_relative_jacobi_transfer import (
    ENDPOINT_TRIM_THRESHOLD,
    UNIFORM_JACOBI_ENDPOINT_FLOOR,
    _gaussian_child_frames,
    audit_relative_endpoint_trim,
    final_root_relative_scaling_record,
    relative_jacobi_aspect_record,
    run_final_root_relative_jacobi_transfer,
)


@pytest.mark.parametrize("alpha", [2.0, 2.5, 3.0, 4.0])
def test_uniform_parent_and_relative_windows_cover_final_aspects(alpha: float) -> None:
    row = relative_jacobi_aspect_record(alpha)

    assert row.parent_mp_lower_edge >= 1.0
    assert row.parent_mp_upper_edge < 16.0
    assert row.relative_endpoint_gap >= UNIFORM_JACOBI_ENDPOINT_FLOOR - 1e-12
    assert row.fixed_parent_window_contains_limit
    assert row.fixed_endpoint_trim_lies_below_limit


def test_uniform_endpoint_floor_is_attained_at_aspect_two() -> None:
    row = relative_jacobi_aspect_record(2.0)

    assert row.relative_endpoint_gap == pytest.approx((2 - math.sqrt(3)) / 4)
    assert ENDPOINT_TRIM_THRESHOLD < row.relative_endpoint_gap


def test_relative_endpoint_trim_identities_and_state_bounds_hold() -> None:
    left, right = _gaussian_child_frames(20, 2.5, 5201)
    control = audit_relative_endpoint_trim("CONTROL", left, right)

    assert control.exact_trim_identities_verified
    assert control.endpoint_completeness_residual < 1e-8
    assert control.exact_relative_isometry_residual < 1e-8
    assert control.rounded_relative_isometry_residual < 1e-8
    assert (
        control.native_total_discarded_state_mass
        <= control.hilbert_schmidt_state_mass_upper_bound + 1e-8
    )
    assert control.rounded_naimark_mean_square_error <= control.rounded_error_upper_bound + 1e-8


def test_scaling_records_use_two_extra_copies_and_keep_access_open() -> None:
    row = final_root_relative_scaling_record(32)

    assert row.selected_copy_count == row.information_threshold_copy_count + 2
    assert 2 <= row.child_aspect < 4
    assert row.weak_relative_jacobi_law_proved
    assert not row.operator_norm_relative_edge_proved
    assert not row.structured_endpoint_effect_access_proved


def test_invalid_aspect_and_trim_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        relative_jacobi_aspect_record(1.9)
    left, right = _gaussian_child_frames(8, 2.0, 5202)
    with pytest.raises(ValueError):
        audit_relative_endpoint_trim("BAD-WINDOW", left, right, parent_window_lower=2, parent_window_upper=1)
    with pytest.raises(ValueError):
        audit_relative_endpoint_trim("BAD-ENDPOINT", left, right, endpoint_threshold=0.5)


def test_report_bypasses_intersection_but_not_coherent_access() -> None:
    report = run_final_root_relative_jacobi_transfer()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["natural_final_root_relative_jacobi_weak_law_proved"]
    assert report.claim_gate["uniform_final_root_endpoint_bulk_gap_proved"]
    assert report.claim_gate["annealed_native_endpoint_trim_loss_vanishes"]
    assert not report.claim_gate["exact_sibling_intersection_required_for_final_direct_polar"]
    assert not report.claim_gate["untrimmed_operator_norm_endpoint_edge_proved"]
    assert not report.claim_gate["structured_endpoint_effect_block_encoding_proved"]
    assert not report.claim_gate["all_depth_relative_jacobi_law_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
