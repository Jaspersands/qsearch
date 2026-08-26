from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_final_root_addressed_weyl_assembly_boundary import (
    _selected_final_root_parameters,
    addressed_leaf_frame,
    audit_addressed_whitened_blocks,
    audit_addressed_width_control,
    audit_pair_local_indeterminacy,
    audit_two_child_weyl_factorization,
    conditional_aggregate_compiler_record,
    deterministic_child_metrics,
    natural_addressed_weyl_scaling_record,
    run_final_root_addressed_weyl_assembly_boundary,
    write_final_root_addressed_weyl_assembly_boundary_report,
)


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_positive_child_weyl_blocks_and_canonical_gauge_are_exact(
    dimension: int,
) -> None:
    row = audit_two_child_weyl_factorization(
        f"d{dimension}",
        *deterministic_child_metrics(dimension),
    )

    assert row.exact_two_child_weyl_factorization_verified
    assert row.parent_minimum_eigenvalue >= 1.0 - 1e-10
    assert row.parent_maximum_eigenvalue <= 3.0 + 1e-10
    assert 0.0 < row.relative_effect_minimum_eigenvalue
    assert row.relative_effect_maximum_eigenvalue < 1.0
    assert row.child_metric_commutator_norm > 1e-5
    assert row.parent_reconstruction_residual < 1e-10
    assert row.positive_endpoint_isometry_residual < 1e-10
    assert row.canonical_endpoint_isometry_residual < 1e-10
    assert row.maximum_positive_four_block_residual < 1e-10
    assert row.maximum_branch_gauge_endpoint_residual < 1e-10
    assert row.maximum_canonical_four_block_residual < 1e-10
    assert row.shift_byproduct_operator_norm == pytest.approx(1.0)
    assert row.clock_byproduct_operator_norm == pytest.approx(1.0)


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_addressed_raw_blocks_differ_from_globally_whitened_weyl_blocks(
    dimension: int,
) -> None:
    row = audit_addressed_whitened_blocks(
        f"d{dimension}",
        *addressed_leaf_frame(dimension),
    )

    assert row.exact_addressed_whitened_formula_verified
    assert row.leaves_per_child == dimension + 1
    assert row.total_leaf_count == 2 * (dimension + 1)
    assert row.parent_minimum_eigenvalue >= 2.0 - 1e-10
    assert row.parent_maximum_eigenvalue <= 4.0 + 1e-10
    assert row.child_metric_commutator_norm > 1e-5
    assert row.maximum_addressed_raw_cross_map_residual < 1e-12
    assert row.maximum_addressed_whitened_weyl_block_residual < 1e-12
    assert row.full_leaf_byproduct_factorization_residual < 1e-10
    assert row.maximum_raw_to_whitened_weyl_block_gap > 0.1
    assert not row.raw_addressed_cross_maps_equal_target_blocks


def test_pair_local_data_do_not_determine_global_whitened_shift_block() -> None:
    row = audit_pair_local_indeterminacy()

    assert row.exact_pair_local_indeterminacy_verified
    assert row.selected_pair_raw_cross_map_residual < 1e-12
    assert row.selected_pair_polar_residual < 1e-12
    assert row.parent_metric_operator_distance == pytest.approx(1.0)
    assert row.first_selected_shift_block == pytest.approx(0.5)
    assert row.second_selected_shift_block == pytest.approx(1 / math.sqrt(3))
    assert row.selected_whitened_shift_block_gap > 0.05
    assert not row.pair_local_data_determine_whitened_weyl_block


@pytest.mark.parametrize("width", [4, 8, 16, 32, 64])
def test_uniform_address_assembly_has_sharp_width_signal(width: int) -> None:
    row = audit_addressed_width_control(width)

    assert row.sharp_width_normalization_verified
    assert row.addressed_entry_query_normalization == pytest.approx(1.0)
    assert row.dense_gram_linear_assembly_normalization == pytest.approx(width)
    assert row.normalized_parent_metric_eigenvalue == pytest.approx(1 / width)
    assert row.normalized_analysis_singular_value == pytest.approx(1 / math.sqrt(width))
    assert row.bernstein_qsvt_degree_lower_bound == pytest.approx(
        0.9 * math.sqrt(width - 1)
    )
    assert row.analysis_gram_residual < 1e-12
    assert row.dense_gram_residual < 1e-12
    assert row.known_structure_specific_identity_bypass


def test_constant_normalization_aggregate_children_make_binary_top_merge_easy() -> None:
    row = conditional_aggregate_compiler_record()

    assert row.maximum_child_square_root_normalization == pytest.approx(4.0)
    assert row.binary_lcu_normalization == pytest.approx(4 * math.sqrt(2))
    assert row.minimum_binary_lcu_signal == pytest.approx(1 / 8)
    assert row.maximum_binary_lcu_signal == pytest.approx(1 / math.sqrt(2))
    assert row.endpoint_weyl_byproduct_uses_two_endpoint_calls
    assert row.width_independent_given_aggregate_access
    assert not row.aggregate_child_access_supplied_by_addressed_oracle


@pytest.mark.parametrize("n", [8, 16, 24, 32, 40, 48])
def test_natural_scaling_places_charge_in_leaf_aggregation_not_binary_lcu(
    n: int,
) -> None:
    row = natural_addressed_weyl_scaling_record(n)
    order, information, selected, child_width, _ = _selected_final_root_parameters(n)

    assert row.group_order_decimal == str(order)
    assert row.information_threshold_copy_count == information
    assert row.selected_copy_count == selected
    assert row.child_leaf_width_decimal == str(child_width)
    assert row.total_leaf_width_decimal == str(2 * child_width)
    assert row.total_leaf_width_log2 == pytest.approx(selected)
    assert row.retained_signal_maximum_singular_value_log2 == pytest.approx(
        2 - selected / 2
    )
    assert row.canonical_uniform_assembly_superpolynomial
    assert not row.final_binary_lcu_additional_width_charge
    assert not row.representation_specific_global_polar_ruled_out


def test_input_validation() -> None:
    with pytest.raises(ValueError):
        deterministic_child_metrics(1)
    with pytest.raises(ValueError):
        addressed_leaf_frame(1)
    with pytest.raises(ValueError):
        audit_addressed_width_control(3)
    with pytest.raises(ValueError):
        audit_addressed_width_control(5)
    with pytest.raises(ValueError):
        natural_addressed_weyl_scaling_record(2)
    with pytest.raises(ValueError):
        audit_two_child_weyl_factorization(
            "shape",
            np.eye(2),
            np.eye(3),
        )
    left, right = addressed_leaf_frame(2)
    with pytest.raises(ValueError):
        audit_addressed_whitened_blocks("count", left, right[:-1])
    bad = list(left)
    bad[0] = 2 * bad[0]
    with pytest.raises(ValueError):
        audit_addressed_whitened_blocks("norm", tuple(bad), right)


def test_report_closes_pair_local_route_but_keeps_hierarchical_route_open() -> None:
    report = run_final_root_addressed_weyl_assembly_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["exact_positive_child_weyl_four_block_theorem_count"] == 1
    assert report.headline_metrics["exact_addressed_leaf_whitened_block_theorem_count"] == 1
    assert report.headline_metrics["conditional_constant_cost_binary_merge_theorem_count"] == 1
    assert report.claim_gate["positive_child_metric_four_block_formula_proved"]
    assert report.claim_gate["target_leaf_blocks_require_shared_parent_inverse_metric"]
    assert not report.claim_gate["pair_local_functional_calculus_suffices"]
    assert report.claim_gate["bounded_qsvt_uniform_assembly_degree_omega_sqrt_w"]
    assert report.claim_gate["final_binary_merge_width_independent_given_aggregate_access"]
    assert not report.claim_gate[
        "addressed_leaf_oracle_supplies_constant_normalization_aggregate_child_maps"
    ]
    assert not report.claim_gate["arbitrary_multi_query_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "addressed-weyl-boundary.json"
    payload = write_final_root_addressed_weyl_assembly_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"]["finite_control_failure_count"] == 0
    assert not payload["claim_gate"]["endpoint_weyl_shift_compiled"]
    assert not payload["claim_gate"]["endpoint_weyl_clock_compiled"]
