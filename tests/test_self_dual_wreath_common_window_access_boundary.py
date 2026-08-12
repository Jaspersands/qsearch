from __future__ import annotations

import math

import pytest

from self_dual_wreath_common_window_access_boundary import (
    audit_window_intersection_access,
    run_common_window_access_boundary,
    window_access_scaling_record,
)


@pytest.mark.parametrize(
    ("dimension", "angle"),
    [(8, 0.2), (12, 0.05), (16, 0.01)],
)
def test_cross_relation_factorization_and_branch_recovery_are_exact(
    dimension: int,
    angle: float,
) -> None:
    _, factorization = audit_window_intersection_access(
        "FACTOR",
        dimension,
        angle,
    )

    assert factorization.exact_factorization_verified
    assert factorization.direct_cross_relation_residual < 1e-8
    assert factorization.synthesis_annihilation_residual < 1e-8
    assert factorization.endpoint_completeness_residual < 1e-8
    assert factorization.left_branch_polar_recovery_residual < 1e-8
    assert factorization.right_branch_polar_recovery_residual < 1e-8
    assert factorization.cross_metric_condition_number <= 100
    assert factorization.left_endpoint_minimum_eigenvalue >= 1 / 200 - 1e-8


def test_dense_windows_have_exact_principal_angle_gaps() -> None:
    control, _ = audit_window_intersection_access("ANGLE", 14, 0.025)

    assert control.left_window_rank == 13
    assert control.right_window_rank == 13
    assert control.common_window_rank == 12
    assert control.common_codimension_fraction == pytest.approx(2 / 14)
    assert control.defect_smallest_positive_eigenvalue == pytest.approx(
        1 - math.cos(0.025)
    )
    assert control.reflection_smallest_nonzero_eigenphase == pytest.approx(0.05)
    assert control.dense_but_small_angle_boundary_verified


def test_identical_marginal_spectra_do_not_control_intersection_access() -> None:
    wide, _ = audit_window_intersection_access("WIDE", 12, 0.2)
    narrow, _ = audit_window_intersection_access("NARROW", 12, 0.01)

    assert wide.individual_spectrum_residual < 1e-10
    assert narrow.individual_spectrum_residual < 1e-10
    assert narrow.common_codimension == wide.common_codimension == 2
    assert narrow.native_root_state_loss < 0.25
    assert narrow.phase_resolution_query_lower_bound > 10 * wide.phase_resolution_query_lower_bound


def test_scaling_has_vanishing_rank_loss_and_exponential_phase_cost() -> None:
    first = window_access_scaling_record(16)
    second = window_access_scaling_record(32)

    assert second.common_codimension_fraction < first.common_codimension_fraction
    assert second.native_state_loss_upper_bound < first.native_state_loss_upper_bound
    assert second.phase_resolution_query_lower_bound_log2 == pytest.approx(31)
    assert second.reflection_phase_gap_log2 == pytest.approx(-31)
    assert second.weak_mp_marginals_compatible
    assert not second.polynomial_reflection_oracle_intersection_access


def test_invalid_window_counterfamily_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        audit_window_intersection_access("SMALL", 3, 0.1)
    with pytest.raises(ValueError):
        audit_window_intersection_access("ANGLE", 8, 0.0)
    with pytest.raises(ValueError):
        audit_window_intersection_access("OUTLIER", 8, 0.1, outlier_eigenvalue=0.2)


def test_report_keeps_structured_access_and_speedup_blocked() -> None:
    report = run_common_window_access_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["exact_recursive_cross_polar_factorization_proved"]
    assert report.claim_gate["constant_conditioned_endpoint_mixer_proved"]
    assert report.claim_gate["cross_relation_contains_dense_child_polar_proved"]
    assert not report.claim_gate["rank_dense_window_implies_polynomial_intersection_access"]
    assert not report.claim_gate["structured_natural_common_space_access_proved"]
    assert not report.claim_gate["dense_restricted_child_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
