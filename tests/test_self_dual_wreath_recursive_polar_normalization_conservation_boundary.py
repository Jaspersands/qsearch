from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_recursive_polar_normalization_conservation_boundary import (
    _selected_parameters,
    audit_child_polar_metric_scale,
    audit_coefficient_normalization,
    audit_orthogonal_hierarchy_normalization,
    audit_shorted_metric_scale,
    audit_support_aware_tree,
    audit_trim_compatibility,
    deterministic_rank_deficient_leaves,
    natural_recursive_normalization_scaling_record,
    run_recursive_polar_normalization_conservation_boundary,
    write_recursive_polar_normalization_conservation_boundary_report,
)


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_support_aware_recursive_polar_factors_telescope(dimension: int) -> None:
    leaves = deterministic_rank_deficient_leaves(dimension)
    row = audit_support_aware_tree(f"d{dimension}", leaves)

    assert row.exact_support_aware_telescoping_verified
    assert row.leaf_count == 2 * dimension
    assert row.root_rank == dimension
    assert row.contains_rank_deficient_leaf_frames
    assert row.maximum_node_polar_residual < 1e-10
    assert row.maximum_node_chain_rule_residual < 1e-10
    assert row.maximum_node_relative_isometry_residual < 1e-10
    assert row.maximum_node_support_projection_residual < 1e-10
    assert row.recursive_to_direct_root_polar_residual < 1e-10


@pytest.mark.parametrize(
    "normalizations",
    [
        (1.0,) * 8,
        (1.0, 1.5, 2.0, 0.75, 3.0, 1.25, 2.5),
    ],
)
def test_coefficient_normalizations_obey_grouping_independent_l2_law(
    normalizations: tuple[float, ...],
) -> None:
    row = audit_coefficient_normalization("control", normalizations)
    expected = math.sqrt(sum(value * value for value in normalizations))

    assert row.sharp_l2_normalization_recurrence_verified
    assert row.balanced_root_normalization == pytest.approx(expected)
    assert row.left_deep_root_normalization == pytest.approx(expected)
    assert row.closed_form_root_normalization == pytest.approx(expected)
    assert row.unit_leaf_root_normalization == pytest.approx(math.sqrt(len(normalizations)))
    assert row.maximum_prepare_state_norm_residual < 1e-12
    assert row.maximum_equal_block_coefficient_residual < 1e-12
    assert row.tree_grouping_normalization_residual < 1e-12


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_child_polar_moves_but_does_not_remove_analysis_normalization(
    dimension: int,
) -> None:
    analysis = np.vstack(deterministic_rank_deficient_leaves(dimension)[:-1])
    alpha = math.sqrt(2 * dimension - 1)
    row = audit_child_polar_metric_scale("control", analysis, alpha)

    assert row.exact_metric_scale_inheritance_verified
    assert row.analysis_normalization == pytest.approx(alpha)
    assert row.frame_rank == dimension
    assert row.child_polar_partial_isometry_residual < 1e-10
    assert row.recovered_normalized_square_root_residual < 1e-10
    assert row.recovered_to_unscaled_square_root_gap > 0.5
    assert not row.child_polar_resets_analysis_normalization


@pytest.mark.parametrize(
    ("left_alpha", "right_alpha", "equal_balance", "unequal_spoils"),
    [(2.0, 2.0, True, False), (2.0, 3.0, False, True)],
)
def test_shorted_metrics_inherit_rather_than_cancel_analysis_scale(
    left_alpha: float,
    right_alpha: float,
    equal_balance: bool,
    unequal_spoils: bool,
) -> None:
    row = audit_shorted_metric_scale("control", left_alpha, right_alpha)

    assert row.exact_shorted_metric_scale_inheritance_verified
    assert row.intersection_dimension == 2
    assert row.true_compressed_inverse_metric_balance_residual == pytest.approx(0.0)
    assert row.maximum_encoded_compressed_inverse_scaling_residual < 1e-10
    assert row.maximum_encoded_shorted_operator_scaling_residual < 1e-10
    assert row.equal_normalizations_preserve_balance_equality is equal_balance
    assert row.unequal_normalizations_spoil_apparent_balance is unequal_spoils
    assert not row.shorted_metric_cancels_analysis_normalization
    if unequal_spoils:
        assert row.encoded_compressed_inverse_metric_balance_residual > 1.0
        assert row.encoded_shorted_operator_balance_residual > 0.1


def test_independent_child_trims_need_not_compose_to_parent_trim() -> None:
    row = audit_trim_compatibility()

    assert row.exact_trim_compatibility_boundary_verified
    assert row.discarded_child_eigenvalue == pytest.approx(0.4)
    assert row.accumulated_parent_eigenvalue == pytest.approx(0.8)
    assert row.minimum_retained_child_eigenvalue == pytest.approx(1.0)
    assert row.minimum_retained_parent_eigenvalue == pytest.approx(0.8)
    assert row.incompatible_analysis_operator_gap == pytest.approx(math.sqrt(0.8))
    assert row.incompatible_frame_operator_gap == pytest.approx(0.8)
    assert row.incompatible_polar_operator_gap == pytest.approx(1.0)
    assert row.compatible_analysis_operator_residual == pytest.approx(0.0)
    assert not row.independent_good_conditioning_implies_parent_trim_compatibility


@pytest.mark.parametrize("depth", [1, 2, 3, 4, 5, 6])
def test_exact_local_isometries_telescope_but_passive_normalizations_multiply(
    depth: int,
) -> None:
    row = audit_orthogonal_hierarchy_normalization(depth)
    width = 1 << depth

    assert row.no_passive_normalization_cancellation_verified
    assert row.leaf_count == width
    assert row.exact_root_polar_residual < 1e-10
    assert row.exact_local_relative_isometry_residual < 1e-10
    assert row.passively_normalized_root_signal == pytest.approx(1 / math.sqrt(width))
    assert row.expected_passively_normalized_root_signal == pytest.approx(
        1 / math.sqrt(width)
    )
    assert row.passive_recursive_composition_residual < 1e-10
    assert row.coefficient_recurrence_root_normalization == pytest.approx(
        math.sqrt(width)
    )
    assert row.global_bernstein_degree_lower_bound == pytest.approx(
        0.9 * math.sqrt(width - 1)
    )
    assert row.literal_local_qsvt_minimum_odd_degree == 3
    assert row.literal_nested_qsvt_leaf_query_lower_bound == 3**depth
    assert row.supplied_alpha_one_local_isometry_depth == depth
    assert row.exact_local_isometry_oracles_are_additional_access


@pytest.mark.parametrize("n", [8, 16, 24, 32, 40, 48])
def test_natural_recursive_scaling_keeps_access_charge(n: int) -> None:
    row = natural_recursive_normalization_scaling_record(n)
    order, information, selected, width = _selected_parameters(n)

    assert row.group_order_decimal == str(order)
    assert row.information_threshold_copy_count == information
    assert row.selected_copy_count == selected
    assert row.orientation_leaf_width_decimal == str(width)
    assert row.recursive_depth == selected
    assert row.coefficient_root_normalization_log2 == pytest.approx(selected / 2)
    assert row.literal_nested_degree_three_query_lower_bound_log2 == pytest.approx(
        selected * math.log2(3)
    )
    assert row.supplied_local_isometry_composition_depth == selected
    assert row.coefficient_only_recursive_assembly_superpolynomial
    assert row.literal_nested_local_qsvt_superpolynomial
    assert not row.normalization_one_local_relative_isometries_compiled


def test_input_validation() -> None:
    with pytest.raises(ValueError):
        deterministic_rank_deficient_leaves(1)
    with pytest.raises(ValueError):
        audit_support_aware_tree("few", (np.eye(2),))
    with pytest.raises(ValueError):
        audit_support_aware_tree("shape", (np.eye(2), np.eye(3)))
    with pytest.raises(ValueError):
        audit_coefficient_normalization("few", (1.0,))
    with pytest.raises(ValueError):
        audit_coefficient_normalization("negative", (1.0, -1.0))
    with pytest.raises(ValueError):
        audit_child_polar_metric_scale("alpha", np.eye(2), 1.0)
    with pytest.raises(ValueError):
        audit_shorted_metric_scale("alpha", 0.0, 1.0)
    with pytest.raises(ValueError):
        audit_trim_compatibility(child_threshold=0.0)
    with pytest.raises(ValueError):
        audit_orthogonal_hierarchy_normalization(0)
    with pytest.raises(ValueError):
        audit_orthogonal_hierarchy_normalization(1, approximation_error=1.0)
    with pytest.raises(ValueError):
        natural_recursive_normalization_scaling_record(2)


def test_report_closes_bookkeeping_loophole_but_preserves_structured_router() -> None:
    report = run_recursive_polar_normalization_conservation_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "exact_support_aware_recursive_polar_telescoping_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "sharp_l2_normalization_conservation_theorem_count"
    ] == 1
    assert report.claim_gate[
        "support_aware_recursive_polar_factors_telescope_exactly"
    ]
    assert report.claim_gate[
        "coefficient_only_normalizations_obey_squared_sum_recurrence"
    ]
    assert not report.claim_gate["tree_grouping_reduces_root_normalization"]
    assert not report.claim_gate["child_polar_resets_child_analysis_normalization"]
    assert report.claim_gate["shorted_metric_scale_inheritance_proved"]
    assert not report.claim_gate[
        "shorted_metrics_cancel_child_analysis_normalization"
    ]
    assert not report.claim_gate[
        "independent_retained_child_trims_automatically_compose"
    ]
    assert report.claim_gate[
        "compatible_normalization_one_local_relative_isometries_would_close_in_depth"
    ]
    assert not report.claim_gate["normalization_one_local_relative_isometries_compiled"]
    assert not report.claim_gate["arbitrary_hierarchical_query_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "recursive-normalization.json"
    payload = write_recursive_polar_normalization_conservation_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["status"] == (
        "recursive-polar-algebra-telescopes-normalization-conserved"
    )
    assert payload["headline_metrics"]["finite_control_failure_count"] == 0
