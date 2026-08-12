from __future__ import annotations

import pytest

from self_dual_wreath_final_root_common_window_metric import (
    _window_control_frames,
    audit_common_window_metric,
    common_window_scaling_record,
    marchenko_pastur_edges,
    run_final_root_common_window_metric,
)


@pytest.mark.parametrize("alpha", [2.0, 2.5, 3.0, 4.0])
def test_uniform_window_contains_every_final_root_mp_support(alpha: float) -> None:
    lower, upper = marchenko_pastur_edges(alpha)
    row = common_window_scaling_record(alpha)

    assert 0.1 < lower <= upper < 10
    assert row.fixed_window_contains_limiting_support
    assert row.cross_metric_condition_number_upper_bound == pytest.approx(100)
    assert row.endpoint_minimum_weight_lower_bound == pytest.approx(1 / 200)


def test_common_window_metric_and_endpoint_bounds_hold() -> None:
    left, right = _window_control_frames(12, 2, 2, 4201)
    control = audit_common_window_metric("D12", left, right)

    assert control.common_window_rank >= control.common_window_rank_lower_bound
    assert control.cross_metric_minimum_eigenvalue >= control.cross_metric_minimum_lower_bound
    assert control.cross_metric_maximum_eigenvalue <= control.cross_metric_maximum_upper_bound
    assert control.left_endpoint_minimum_eigenvalue >= control.endpoint_minimum_lower_bound
    assert control.right_endpoint_minimum_eigenvalue >= control.endpoint_minimum_lower_bound
    assert control.native_root_state_loss <= control.hilbert_schmidt_state_loss_upper_bound
    assert control.state_loss_bound_verified
    assert control.exact_window_metric_bounds_verified


def test_window_control_counts_removed_outliers() -> None:
    left, right = _window_control_frames(16, 3, 2, 4202)
    control = audit_common_window_metric("OUTLIERS", left, right)

    assert control.left_window_outlier_count == 3
    assert control.right_window_outlier_count == 2
    assert control.common_window_rank >= 11


def test_invalid_mp_aspect_and_window_are_rejected() -> None:
    with pytest.raises(ValueError):
        marchenko_pastur_edges(1.0)
    left, right = _window_control_frames(8, 1, 1, 4203)
    with pytest.raises(ValueError):
        audit_common_window_metric("BAD", left, right, window_lower=2, window_upper=1)


def test_report_preserves_rank_trim_and_access_boundaries() -> None:
    report = run_final_root_common_window_metric()

    assert report.headline_metrics["rank_dense_common_window_metric_theorem_count"] == 1
    assert report.headline_metrics["uniform_cross_metric_condition_number_upper_bound"] == 100
    assert report.headline_metrics["uniform_endpoint_minimum_weight_lower_bound"] == pytest.approx(1 / 200)
    assert report.claim_gate["rank_dense_final_root_common_window_proved"]
    assert report.claim_gate["constant_condition_final_root_cross_metric_on_window_proved"]
    assert report.claim_gate["native_state_weight_retention_proved"]
    assert report.claim_gate["native_state_gentle_success_retention_proved"]
    assert not report.claim_gate["untrimmed_final_root_no_outlier_edge_proved"]
    assert not report.claim_gate["structured_child_window_projectors_compiled"]
    assert not report.claim_gate["all_depth_node_metric_conditioning_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
