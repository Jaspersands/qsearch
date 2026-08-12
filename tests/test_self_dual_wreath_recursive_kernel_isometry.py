from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_recursive_kernel_isometry import (
    _random_rank_one_leaves,
    _resolve_kernel_node,
    _three_lines_augmented_control,
    audit_recursive_kernel_isometry,
    recursive_kernel_scaling_record,
    run_recursive_kernel_isometry,
)


def test_emergent_four_line_kernel_is_resolved_orthonormally() -> None:
    control = audit_recursive_kernel_isometry(
        "FOUR-LINES",
        _three_lines_augmented_control(),
    )

    assert control.direct_kernel_dimension == 2
    assert control.recursive_kernel_dimension == 2
    assert control.nontrivial_cross_relation_node_count == 1
    assert control.maximum_recursive_kernel_projector_residual < 1e-10
    assert control.exact_all_node_kernel_isometry_verified


@pytest.mark.parametrize("physical_dimension,seed", [(3, 901), (5, 902)])
def test_random_eight_leaf_hierarchy_matches_direct_kernel(
    physical_dimension: int,
    seed: int,
) -> None:
    control = audit_recursive_kernel_isometry(
        f"RANDOM-{physical_dimension}",
        _random_rank_one_leaves(physical_dimension, 8, seed),
    )

    assert control.direct_kernel_dimension == control.recursive_kernel_dimension
    assert control.root_support_rank == control.synthesis_rank
    assert control.root_support_reflection_unitarity_residual < 1e-10
    assert control.exact_all_node_kernel_isometry_verified


def test_each_cross_relation_is_whitened_and_child_orthogonal() -> None:
    leaves = _random_rank_one_leaves(3, 8, 1001)
    data = _resolve_kernel_node(leaves, tuple(range(8)), "ROOT", 1e-9)
    nontrivial = [row for row in data.records if row.common_span_dimension]

    assert nontrivial
    assert all(row.cross_relation_isometry_residual < 1e-10 for row in nontrivial)
    assert all(row.child_cross_orthogonality_residual < 1e-10 for row in nontrivial)
    assert all(row.exact_recursive_kernel_isometry_verified for row in data.records)


def test_support_projector_is_complement_of_recursive_kernel() -> None:
    leaves = _three_lines_augmented_control()
    data = _resolve_kernel_node(leaves, tuple(range(4)), "ROOT", 1e-9)
    kernel_projector = data.kernel_isometry @ data.kernel_isometry.conj().T

    assert np.linalg.norm(data.support_projector + kernel_projector - np.eye(4)) < 1e-10
    assert np.linalg.norm(data.support_projector @ data.support_projector - data.support_projector) < 1e-10


def test_non_power_of_two_leaf_family_is_rejected() -> None:
    with pytest.raises(ValueError):
        audit_recursive_kernel_isometry(
            "THREE",
            _three_lines_augmented_control()[:3],
        )


def test_scaling_bypasses_global_gap_but_keeps_node_gates_open() -> None:
    row = recursive_kernel_scaling_record(64)

    assert row.maximum_factor_graph_degree == 3
    assert not row.global_sheaf_gap_required_given_direct_relation_isometry
    assert not row.coherent_child_pseudoinverse_proved
    assert not row.coherent_common_span_basis_proved
    assert not row.natural_cross_metric_conditioning_proved
    assert not row.physical_endpoint_gauge_proved


def test_report_does_not_promote_exact_algebra_to_compiler() -> None:
    report = run_recursive_kernel_isometry()

    assert report.headline_metrics["orthonormal_recursive_kernel_isometry_theorem_count"] == 1
    assert report.headline_metrics["global_sheaf_gap_bypass_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["exact_dependency_coverage_proved_information_theoretically"]
    assert not report.claim_gate["global_sheaf_gap_required_if_relation_isometry_compiled"]
    assert not report.claim_gate["coherent_natural_child_pseudoinverses_proved"]
    assert not report.claim_gate["natural_all_depth_cross_metric_conditioning_proved"]
    assert not report.claim_gate["physical_endpoint_gauge_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
