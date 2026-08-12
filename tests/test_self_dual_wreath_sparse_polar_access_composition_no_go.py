from __future__ import annotations

import math

import pytest

from self_dual_wreath_sparse_polar_access_composition_no_go import (
    audit_orthogonal_hierarchy_access,
    fixed_arity_access_scaling_record,
    run_sparse_polar_access_composition_no_go,
)


@pytest.mark.parametrize("depth", range(1, 9))
def test_zero_error_orthogonal_hierarchy_retains_binary_normalization(
    depth: int,
) -> None:
    row = audit_orthogonal_hierarchy_access(depth)

    assert row.every_local_gram_is_exactly_flat
    assert row.support_scalarization_pressure == 0
    assert row.aggregate_native_polar_error == 0
    assert row.aggregate_low_singular_native_mass == 0
    assert row.normalized_binary_analysis_singular_value == pytest.approx(
        1 / math.sqrt(2)
    )
    assert row.maximum_degree_one_qsvt_output_amplitude == pytest.approx(
        1 / math.sqrt(2)
    )
    assert row.minimum_nontrivial_odd_qsvt_degree == 3
    assert row.nested_qsvt_leaf_query_lower_bound == 3**depth
    assert row.global_flat_black_box_query_lower_bound == pytest.approx(2 ** (depth / 2))
    assert row.zero_error_does_not_remove_access_normalization


def test_fixed_arity_only_subtracts_a_constant_number_of_binary_levels() -> None:
    low = fixed_arity_access_scaling_record(32, jump_log2_arity=20)
    high = fixed_arity_access_scaling_record(64, jump_log2_arity=20)

    assert low.fixed_jump_log2_arity == high.fixed_jump_log2_arity == 20
    assert high.early_binary_depth > low.early_binary_depth
    assert (
        high.normalized_black_box_query_log2_lower_bound
        > low.normalized_black_box_query_log2_lower_bound
    )
    assert not low.fixed_arity_removes_asymptotic_width_barrier
    assert not high.fixed_arity_removes_asymptotic_width_barrier


def test_large_n_fixed_arity_access_is_superpolynomial() -> None:
    row = fixed_arity_access_scaling_record(80)

    assert row.nested_local_qsvt_superpolynomial
    assert row.normalized_black_box_access_superpolynomial
    assert not row.fixed_arity_removes_asymptotic_width_barrier


def test_invalid_access_controls_are_rejected() -> None:
    with pytest.raises(ValueError):
        audit_orthogonal_hierarchy_access(0)
    with pytest.raises(ValueError):
        audit_orthogonal_hierarchy_access(2, requested_output_amplitude=0.7)
    with pytest.raises(ValueError):
        fixed_arity_access_scaling_record(2)


def test_report_forces_structured_global_router_without_overclaiming() -> None:
    report = run_sparse_polar_access_composition_no_go()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["nested_local_qsvt_superpolynomial_proved"]
    assert report.claim_gate["normalized_black_box_width_boundary_retained"]
    assert not report.claim_gate["constant_local_gap_suffices_for_recursive_qsvt"]
    assert not report.claim_gate["arbitrary_circuit_lower_bound_proved"]
    assert not report.claim_gate["representation_specific_global_router_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
