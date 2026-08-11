from functools import lru_cache

import numpy as np

from self_dual_wreath_component_coefficient_projection_normal_form import (
    _random_leaf_system,
    audit_coefficient_projection_normal_form,
    coefficient_projection_normal_form,
    coefficient_projection_normal_form_theorem,
    run_component_coefficient_projection_normal_form,
)


@lru_cache(maxsize=1)
def _report():
    return run_component_coefficient_projection_normal_form()


def test_support_difference_equals_normalized_minimum_preimage_projection():
    leaves, common = _random_leaf_system(
        2101,
        physical_dimension=8,
        block_dimensions=(2, 3, 4, 5),
        common_dimension=4,
    )
    _, embedding, projection, _, _ = coefficient_projection_normal_form(
        leaves,
        common,
    )
    np.testing.assert_allclose(
        embedding @ embedding.conj().T,
        projection,
        atol=1e-9,
    )
    np.testing.assert_allclose(projection @ projection, projection, atol=1e-9)
    assert round(float(np.trace(projection).real)) == common.shape[1]


def test_rank_deficient_child_keeps_exact_kernel_quotient_identity():
    leaves, common = _random_leaf_system(
        2111,
        physical_dimension=9,
        block_dimensions=(3, 4, 5, 6),
        common_dimension=5,
    )
    row = audit_coefficient_projection_normal_form(
        "rank-deficient",
        leaves,
        common,
    )
    assert row.child_kernel_dimension > 0
    assert row.constrained_kernel_dimension - row.child_kernel_dimension == 5
    assert row.support_difference_rank == 5
    assert row.exact_coefficient_projection_normal_form_verified


def test_all_component_words_through_degree_four_use_only_projection_blocks():
    leaves, common = _random_leaf_system(
        2129,
        physical_dimension=7,
        block_dimensions=(2, 2, 3, 4),
        common_dimension=3,
    )
    row = audit_coefficient_projection_normal_form(
        "word-traces",
        leaves,
        common,
        highest_word_degree=4,
    )
    assert row.maximum_word_trace_residual <= 1e-8
    assert row.maximum_pair_block_formula_residual <= 1e-8
    assert row.commutator_gap_residual <= 1e-8
    assert row.direct_commutator_fourth_moment_gap > 0
    assert row.exact_coefficient_projection_normal_form_verified


def test_theorem_eliminates_metric_inverse_but_not_natural_projection():
    theorem = coefficient_projection_normal_form_theorem()
    assert theorem.arbitrary_leaf_ranks
    assert theorem.arbitrary_common_subspace_inside_child_range
    assert theorem.common_metric_inverse_eliminated_from_trace_target
    assert theorem.theorem_verified
    assert not theorem.natural_dependency_projection_controlled
    assert not theorem.natural_component_M4_positive


def test_report_moves_boundary_to_dependency_projection_block_moments():
    report = _report()
    assert report.headline_metrics[
        "coefficient_projection_normal_form_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "common_metric_inverse_elimination_theorem_count"
    ] == 1
    assert report.headline_metrics["distinct_pair_block_formula_theorem_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["common_metric_inverse_eliminated_from_trace_target"]
    assert not report.claim_gate["natural_dependency_projection_controlled"]
    assert not report.claim_gate["natural_distinct_pair_block_moments_separated"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
