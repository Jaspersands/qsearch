import math

import numpy as np
import pytest

from self_dual_wreath_all_level_component_trim import (
    all_level_component_trim_theorem,
    all_level_trim_scaling_record,
    audit_high_cap_operator_norm,
    audit_hierarchy_rank_budget,
    audit_second_moment_component_trim,
    overlapping_block_counterexample,
    run_all_level_component_trim,
)


def test_nested_coordinate_partitions_have_one_global_rank_budget() -> None:
    levels = (
        ((0, 1, 2, 3),),
        ((0, 1), (2, 3)),
        ((0,), (1,), (2,), (3,)),
    )
    row = audit_hierarchy_rank_budget(
        "TEST-BINARY-HIERARCHY",
        (2, 3, 4, 1),
        levels,
        seed=101,
    )
    assert row.global_coefficient_dimension == 10
    assert row.all_level_rank_budget_verified
    assert all(
        transition.aggregate_component_rank <= 10
        for transition in row.transitions
    )
    assert all(
        transition.aggregate_child_block_dimension == 10
        for transition in row.transitions
    )


def test_nonpartition_hierarchy_is_rejected() -> None:
    with pytest.raises(ValueError, match="partition"):
        audit_hierarchy_rank_budget(
            "OVERLAPPING",
            (2, 2, 2),
            (
                ((0, 1, 2),),
                ((0, 1), (1, 2)),
            ),
            seed=7,
        )


def test_overlapping_blocks_can_double_the_rank_budget() -> None:
    row = overlapping_block_counterexample()
    assert not row.blocks_form_partition
    assert row.aggregate_component_rank == 2 * row.global_coefficient_dimension
    assert row.fixed_partition_premise_necessary


def test_one_sided_high_cap_needs_no_lower_cutoff() -> None:
    effect = np.diag([0.2, 0.0, 0.0, 0.0, 0.0]).astype(complex)
    row = audit_high_cap_operator_norm(
        "ONE-SIDED",
        (1.875, 1.875, 1.875, 1.875, 2.5),
        2.0,
        effect,
        0.02,
    )
    assert not row.lower_root_cutoff_used
    assert row.retained_trace_fraction == pytest.approx(0.75)
    assert row.operator_norm_bound_verified
    assert row.component_error_bound_verified
    assert row.exact_component_failure == pytest.approx(0.05)


def test_arbitrarily_small_retained_root_eigenvalue_is_allowed() -> None:
    effect = np.diag([0.0, 0.04, 0.03, 0.02, 0.01]).astype(complex)
    row = audit_high_cap_operator_norm(
        "TINY-LOW-EDGE",
        (1e-15, 0.25, 0.75, 2.0, 5.0),
        2.0,
        effect,
        0.0125,
    )
    assert row.frame_eigenvalues[0] < 1e-12
    assert row.operator_norm_bound_verified
    assert row.component_error_bound_verified


def test_native_second_moment_removes_every_root_spectral_filter() -> None:
    effect = np.diag([0.0, 0.0, 0.0, 0.2]).astype(complex)
    row = audit_second_moment_component_trim(
        "UNFILTERED-SKEW",
        (0.001, 0.099, 0.9, 9.0),
        effect,
        0.02,
    )
    assert not row.root_spectral_filter_used
    assert row.discarded_effect_contraction_verified
    assert row.trace_rank_budget_verified
    assert row.second_moment_error_bound_verified
    assert row.exact_component_failure == pytest.approx(0.18)
    assert row.second_moment_failure_upper_bound > row.exact_component_failure


def test_discarded_effect_must_respect_trace_rank_budget() -> None:
    with pytest.raises(ValueError, match="trace-rank budget"):
        audit_high_cap_operator_norm(
            "INVALID-DISCARD",
            (1.0, 1.0),
            1.0,
            np.eye(2, dtype=complex),
            0.1,
        )


def test_scaling_threshold_is_inverse_polynomial_in_tree_depth() -> None:
    rows = [all_level_trim_scaling_record(n) for n in (8, 16, 32, 64, 128)]
    assert all(row.inverse_polynomial_threshold_proved for row in rows)
    assert all(not row.lower_root_spectral_cutoff_required for row in rows)
    assert all(not row.root_high_cap_required for row in rows)
    assert all(row.high_capped_pgm_success_lower_bound > 0.69 for row in rows)
    assert all(
        row.all_level_component_error_upper_bound
        == pytest.approx(row.target_component_hybrid_error)
        for row in rows
    )
    assert max(row.orientation_to_hidden_ratio for row in rows) < 8
    assert max(row.collision_second_moment_factor for row in rows) <= 1.25
    ratios = [row.inverse_threshold_to_level_fourth_ratio for row in rows]
    assert all(math.isfinite(value) and value > 0 for value in ratios)
    assert max(ratios) / min(ratios) < 2


def test_theorem_removes_stale_rank_and_lower_window_prerequisites() -> None:
    theorem = all_level_component_trim_theorem()
    assert theorem.all_level_rank_budget_proved
    assert not theorem.lower_root_spectral_cutoff_required
    assert not theorem.root_high_cap_required
    assert not theorem.postselected_child_flatness_required
    assert theorem.inverse_polynomial_component_threshold_proved
    assert not theorem.structured_high_cap_compiled
    assert not theorem.coherent_component_select_compiled


def test_report_keeps_algorithm_claim_gate_closed() -> None:
    report = run_all_level_component_trim()
    assert report.status == (
        "all-level-component-trim-bound-proved-component-select-open"
    )
    assert report.headline_metrics[
        "all_level_fixed_register_rank_budget_theorem_count"
    ] == 1
    assert report.headline_metrics["hierarchy_control_failure_count"] == 0
    assert report.headline_metrics["high_cap_control_failure_count"] == 0
    assert report.headline_metrics[
        "unfiltered_second_moment_control_failure_count"
    ] == 0
    assert report.headline_metrics["scaling_failure_count"] == 0
    assert report.claim_gate[
        "all_level_aggregate_component_rank_budget_proved"
    ]
    assert not report.claim_gate["root_high_cap_required_for_component_trim"]
    assert not report.claim_gate["speedup_claim_allowed"]
