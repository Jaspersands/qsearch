import pytest

from self_dual_wreath_graded_channel_graph_reduction import (
    audit_graded_channel_graph,
)
from self_dual_wreath_vertex_kernel_graded_reduction import (
    _matrix_endpoint_grams,
    audit_physical_vertex_kernels,
    audit_vertex_kernel_reduction,
    run_vertex_kernel_graded_reduction,
    uniform_scalar_endpoint_grams,
)


def test_uniform_scalar_kernel_recovers_old_graph_reduction() -> None:
    vertices = (2, 5, 11, 12)
    edges = ((2, 12), (5, 12), (11, 12))
    left = (2, 5)
    dimensions, kernels = uniform_scalar_endpoint_grams(
        vertices, edges, 1 / 5
    )

    general = audit_vertex_kernel_reduction(
        "GENERAL-STAR", vertices, edges, left, dimensions, kernels
    )
    scalar = audit_graded_channel_graph(
        "SCALAR-STAR", vertices, edges, left, 1 / 5
    )

    assert general.exact_vertex_kernel_reduction_verified
    assert general.grading_defect_norm == pytest.approx(
        scalar.grading_defect_norm
    )
    assert general.endpoint_gap == pytest.approx(scalar.endpoint_gap)


def test_nonuniform_scalar_kernel_needs_no_common_gamma() -> None:
    import numpy as np

    vertices = (0, 1, 2, 3)
    edges = ((0, 1), (0, 2), (0, 3))
    kernels = {
        0: np.array(
            [[1.0, 0.10, 0.18], [0.10, 1.0, 0.27], [0.18, 0.27, 1.0]]
        ),
        1: np.eye(1),
        2: np.eye(1),
        3: np.eye(1),
    }

    record = audit_vertex_kernel_reduction(
        "NONUNIFORM",
        vertices,
        edges,
        (0, 1),
        {edge: 1 for edge in edges},
        kernels,
    )

    assert record.exact_vertex_kernel_reduction_verified
    assert record.direct_to_shorted_metric_residual < 1e-10
    assert record.direct_to_shorted_grading_residual < 1e-10
    assert 0 < record.endpoint_gap < 0.5


def test_matrix_valued_noncommuting_fibers_reduce_exactly() -> None:
    vertices = tuple(range(6))
    edges = (
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 4),
        (2, 5),
        (3, 4),
        (3, 5),
        (4, 5),
    )
    dimensions, kernels = _matrix_endpoint_grams(vertices, edges, 2)

    record = audit_vertex_kernel_reduction(
        "MATRIX-SHEAF",
        vertices,
        edges,
        (0, 1, 2),
        dimensions,
        kernels,
    )

    assert record.exact_vertex_kernel_reduction_verified
    assert record.crossing_coefficient_dimension == 4
    assert record.maximum_local_identity_diagonal_residual < 1e-10
    assert record.minimum_local_kernel_eigenvalue > -1e-10


def test_physical_w6_pair_cores_match_the_side_short_identity() -> None:
    labels = (
        ((6,), (2, 2, 2)),
        ((5, 1), (2, 2, 1, 1)),
        ((4, 2), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )

    record = audit_physical_vertex_kernels(
        "W6-PHYSICAL", (6,), labels, tuple(range(16))
    )

    assert record.all_splits_verified
    assert record.audited_split_count == 4
    assert record.maximum_direct_to_shorted_residual < 1e-8
    assert record.maximum_grading_defect_norm == pytest.approx(1 / 9)


def test_report_keeps_natural_comparability_blocked() -> None:
    report = run_vertex_kernel_graded_reduction()

    assert report.claim_gate["arbitrary_psd_vertex_kernel_reduction_proved"]
    assert report.claim_gate["nonuniform_correlations_supported"]
    assert report.claim_gate["matrix_valued_multiplicity_sheaves_supported"]
    assert not report.claim_gate["natural_shorted_endpoint_comparability_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["control_failure_count"] == 0
