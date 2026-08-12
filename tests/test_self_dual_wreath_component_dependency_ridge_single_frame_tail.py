import numpy as np
import pytest

from self_dual_wreath_component_dependency_ridge_physical_spectrum import (
    _random_synthesis_with_common_subspace,
    dependency_physical_frames,
    support_ridge_tail,
)
from self_dual_wreath_component_dependency_ridge_single_frame_tail import (
    audit_single_frame_tail_reduction,
    dependency_ridge_single_frame_tail_theorem,
    excluded_frame_tail_is_dominated,
    near_zero_tail_scaling_record,
    run_component_dependency_ridge_single_frame_tail,
    small_eigenvalue_tail_upper_bound,
)


def test_excluded_compression_tail_is_dominated_by_full_frame_tail() -> None:
    synthesis, common = _random_synthesis_with_common_subspace(
        12,
        16,
        10,
        4,
        seed=401,
    )
    row = audit_single_frame_tail_reduction(
        "DOMINATION",
        synthesis,
        common,
        1e-2,
    )
    assert row.exact_single_frame_tail_reduction_verified
    assert row.full_frame_nullity == row.excluded_restriction_nullity
    assert row.rank_drop_residual == 0
    assert row.minimum_positive_eigenvalue_interlacing_slack > -1e-9
    assert row.excluded_support_ridge_tail <= row.full_support_ridge_tail + 1e-9


def test_rank_deficient_frame_preserves_nullity_match_and_tail_bound() -> None:
    synthesis, common = _random_synthesis_with_common_subspace(
        14,
        18,
        10,
        4,
        seed=403,
    )
    row = audit_single_frame_tail_reduction(
        "DEFICIENT",
        synthesis,
        common,
        3e-3,
    )
    assert row.full_frame_rank == 10
    assert row.excluded_frame_rank == 6
    assert row.full_frame_nullity == 4
    assert row.excluded_restriction_nullity == 4
    assert row.exact_single_frame_tail_reduction_verified


def test_direct_diagonal_compression_obeys_positive_eigenvalue_interlacing() -> None:
    frame = np.diag([0.0, 0.0, 0.1, 0.4, 1.0, 2.0]).astype(complex)
    common = np.eye(6, dtype=complex)[:, [4, 5]]
    full, excluded, slack, full_rank, excluded_rank, nullity, restricted_nullity = (
        excluded_frame_tail_is_dominated(frame, common, 0.03)
    )
    assert full_rank == 4
    assert excluded_rank == 2
    assert nullity == restricted_nullity == 2
    assert slack >= 0
    assert excluded <= full


def test_small_eigenvalue_count_split_bounds_exact_tail() -> None:
    frame = np.diag([0.0, 1e-4, 0.05, 0.4, 1.2]).astype(complex)
    eta = 1e-5
    threshold = 0.1
    upper, count, rank = small_eigenvalue_tail_upper_bound(
        frame,
        eta,
        threshold,
    )
    exact = support_ridge_tail(frame, eta)
    assert count == 2
    assert rank == 4
    assert exact <= upper


def test_near_zero_density_schedule_needs_no_uniform_edge() -> None:
    row = near_zero_tail_scaling_record(
        4096,
        target_physical_M4_signal=1e-4,
    )
    assert not row.uniform_minimum_eigenvalue_required
    assert row.normalized_dependency_error_upper_bound < 1e-6
    assert row.parity_curl_transfer_error_upper_bound < 0.02
    assert not row.transfer_preserves_target_signal


def test_report_removes_second_tail_but_keeps_natural_law_and_rate_open() -> None:
    report = run_component_dependency_ridge_single_frame_tail()
    assert report.headline_metrics[
        "single_frame_tail_domination_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "excluded_frame_tail_dominated_by_child_frame_tail"
    ]
    assert report.claim_gate["vanishing_near_zero_eigenvalue_density_suffices"]
    assert report.claim_gate["global_distinct_bounded_tail_transfer_proved"]
    assert not report.claim_gate["all_fixed_natural_moment_convergence_proved"]
    assert not report.claim_gate[
        "inverse_polynomial_near_zero_density_rate_proved"
    ]
    assert not report.claim_gate["natural_support_ridge_tail_small"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_replaces_uniform_edge_by_one_frame_density() -> None:
    theorem = dependency_ridge_single_frame_tail_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_positive_frame
    assert "T_eta(F_perp)<=T_eta(F)" == theorem.excluded_tail_domination
    assert "N_F^+(tau)" in theorem.near_zero_split
    assert "1-Pr(C)" in theorem.collision_free_transfer
