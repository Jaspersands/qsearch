from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_sparse_support_polar_schedule import (
    _random_projector,
    audit_sibling_support_overlap,
    audit_sparse_frame_support,
    natural_sparse_moment_record,
    run_sparse_support_polar_schedule,
    tunable_jump_schedule_record,
)


def test_sparse_frame_rank_and_support_scalarization_bounds_are_exact() -> None:
    rng = np.random.default_rng(6201)
    leaves = tuple(_random_projector(12, 2, rng) for _ in range(4))
    control = audit_sparse_frame_support("FRAME", leaves)

    assert control.rank_and_scalarization_identities_verified
    assert control.rank_deficiency <= control.rank_deficiency_upper_bound + 1e-8
    assert control.frame_to_support_frobenius_squared <= control.frame_to_support_upper_bound + 1e-8
    assert control.frame_to_support_frobenius_squared == pytest.approx(
        control.ordered_pair_overlap - control.rank_deficiency,
        abs=1e-8,
    )


def test_sibling_overlap_controls_high_principal_angle_rank() -> None:
    rng = np.random.default_rng(6202)
    left = sum((_random_projector(16, 2, rng) for _ in range(3)), np.zeros((16, 16), complex))
    right = sum((_random_projector(16, 2, rng) for _ in range(3)), np.zeros((16, 16), complex))
    control = audit_sibling_support_overlap("SIBLING", left, right)

    assert control.deterministic_overlap_and_angle_bounds_verified
    assert control.support_cross_trace <= control.support_cross_trace_upper_bound + 1e-8
    assert control.high_principal_correlation_count <= control.high_correlation_count_upper_bound + 1e-8
    assert control.retained_support_analysis_condition_number <= 3 + 1e-8


@pytest.mark.parametrize(
    ("order", "count"),
    [(120, 1), (120, 2), (120, 8), (5040, 16), (5040, 128)],
)
def test_natural_sparse_moment_and_variance_identities(
    order: int,
    count: int,
) -> None:
    row = natural_sparse_moment_record(order, count)

    assert row.exact_sparse_moment_identities_verified
    assert row.expected_ordered_pair_overlap_per_dimension == pytest.approx(
        row.child_aspect * (row.child_aspect - row.inverse_group_order)
    )
    assert row.size_biased_variance == pytest.approx(row.size_biased_variance_formula)
    assert row.expected_rank_deficiency_upper_bound_per_dimension >= 0


def test_fixed_arity_jump_pressure_decreases_with_arity() -> None:
    rows = [tunable_jump_schedule_record(bits) for bits in (8, 12, 16, 20)]

    assert all(
        right.aggregate_frame_support_pressure_upper_bound
        < left.aggregate_frame_support_pressure_upper_bound
        for left, right in zip(rows, rows[1:])
    )
    assert all(
        right.aggregate_high_angle_rank_pressure_upper_bound
        < left.aggregate_high_angle_rank_pressure_upper_bound
        for left, right in zip(rows, rows[1:])
    )
    assert all(row.jump_arity_fixed_independent_of_n for row in rows)
    assert all(row.constant_arity_joint_freeness_applicable for row in rows)
    assert all(not row.state_weighted_polar_error_composition_proved for row in rows)


def test_invalid_sparse_schedule_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        natural_sparse_moment_record(10, 11)
    with pytest.raises(ValueError):
        tunable_jump_schedule_record(2)
    with pytest.raises(ValueError):
        tunable_jump_schedule_record(8, principal_correlation_threshold=1.0)


def test_report_keeps_polar_stability_and_compilation_open() -> None:
    report = run_sparse_support_polar_schedule()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["exact_sparse_frame_support_scalarization_proved"]
    assert report.claim_gate["natural_sparse_support_overlap_pressure_proved"]
    assert report.claim_gate["fixed_arity_jump_makes_early_pressure_arbitrarily_small"]
    assert not report.claim_gate["operator_norm_sparse_frame_closeness_proved"]
    assert not report.claim_gate["native_state_polar_error_bound_proved"]
    assert not report.claim_gate["coherent_recursive_support_reflections_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
