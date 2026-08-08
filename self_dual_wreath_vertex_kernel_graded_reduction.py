"""Exact graded reduction for arbitrary vertex-kernel carrier sheaves.

The scalar flat-channel reduction assumes that every residual pair-core
overlap in one channel is the same scalar ``gamma``.  Natural Kronecker/Racah
blocks need not have one scale, one-dimensional multiplicity fibers, or
commuting overlap matrices.  Those assumptions are unnecessary for the
graded Schur reduction.

Let ``H=(V,E)`` be the orientation support graph.  Edge ``e`` carries a
coefficient space ``C_e``.  At every orientation vertex ``v``, the physical
endpoint embeddings of the incident edge coefficients have a positive
semidefinite block Gram kernel ``K_v`` with identity diagonal blocks.  After
the canonical incidence signs are applied, write

    A_L = sum_{v in L} K_v,       A_R = sum_{v in R} K_v.

The full relation metric and sibling grading are

    M = A_L + A_R,                J = A_L - A_R.            (1)

Internal left edges occur only in ``A_L`` and internal right edges only in
``A_R``.  Therefore the internal block of ``M`` is a direct sum.  Shorting
the internal edge variables gives, exactly,

    M_q = E_L + E_R,              J_q = E_L - E_R,          (2)

where ``E_s`` is the Schur short of ``A_s`` from the side's internal edges to
the common crossing-edge coefficient space.  The Moore-Penrose inverse is
valid even for singular endpoint kernels because positivity supplies the
required range inclusion.

This is the matrix-sheaf and nonuniform-correlation extension of the earlier
graph Laplacian resolvent formula.  If both endpoint effects are positive
definite, their generalized eigenvalue ratios ``t`` again give grading
defects ``(t-1)/(t+1)``.  Thus the exact all-depth target is two-sided
comparability of *shorted physical endpoint kernels*.  Scalarization,
commuting carrier atoms, and a common reciprocal scale are useful ways to
prove that comparability, but they are not prerequisites for stating or
testing it.

The theorem does not provide comparability by itself.  A crossing-only
complete bipartite scalar kernel remains a counterfamily with a closing
endpoint gap.  The value of (2) is that mixed-scale or matrix-valued natural
blocks can now be admitted honestly rather than discarded by the extractor.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_global_carrier_channel_extractor import (
    global_residual_pair_core_bases,
)
from self_dual_wreath_orientation_laplacian_gap import (
    _core_bases,
    live_pair_cores,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_vertex_kernel_graded_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-KERNEL-GRADED-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Vertex = int
Edge = tuple[Vertex, Vertex]


@dataclass(frozen=True)
class VertexKernelReductionControl:
    control_id: str
    vertex_count: int
    edge_count: int
    crossing_edge_count: int
    left_internal_edge_count: int
    right_internal_edge_count: int
    total_coefficient_dimension: int
    crossing_coefficient_dimension: int
    minimum_local_kernel_eigenvalue: float
    maximum_local_identity_diagonal_residual: float
    quotient_metric_minimum_eigenvalue: float
    left_endpoint_effect_minimum_eigenvalue: float
    right_endpoint_effect_minimum_eigenvalue: float
    grading_defect_norm: float
    endpoint_gap: float
    generalized_ratio_minimum: float
    generalized_ratio_maximum: float
    generalized_ratio_predicted_defect: float
    direct_to_shorted_metric_residual: float
    direct_to_shorted_grading_residual: float
    generalized_ratio_defect_residual: float
    exact_vertex_kernel_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalVertexKernelControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_count: int
    live_pair_core_count: int
    residual_pair_core_count: int
    exact_common_dimension_removed: int
    audited_split_count: int
    maximum_grading_defect_norm: float
    minimum_endpoint_gap: float
    maximum_direct_to_shorted_residual: float
    all_splits_verified: bool
    split_controls: list[VertexKernelReductionControl]
    status: str


@dataclass(frozen=True)
class VertexKernelGradedReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    abstract_controls: list[VertexKernelReductionControl]
    physical_controls: list[PhysicalVertexKernelControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _canonical_edges(edges: Iterable[Edge]) -> tuple[Edge, ...]:
    canonical = {
        (min(left, right), max(left, right)) for left, right in edges
    }
    if any(left == right for left, right in canonical):
        raise ValueError("self-loops are not valid pair cores")
    return tuple(sorted(canonical))


def _edge_offsets(
    edges: tuple[Edge, ...],
    edge_dimensions: dict[Edge, int],
) -> dict[Edge, tuple[int, int]]:
    offsets: dict[Edge, tuple[int, int]] = {}
    position = 0
    for edge in edges:
        dimension = edge_dimensions.get(edge, 0)
        if dimension < 1:
            raise ValueError("every edge fiber must have positive dimension")
        offsets[edge] = (position, position + dimension)
        position += dimension
    return offsets


def _edge_indices(
    edges: tuple[Edge, ...],
    offsets: dict[Edge, tuple[int, int]],
) -> tuple[int, ...]:
    return tuple(
        index
        for edge in edges
        for index in range(offsets[edge][0], offsets[edge][1])
    )


def endpoint_gram_from_edge_bases(
    vertex: Vertex,
    incident_edges: tuple[Edge, ...],
    edge_bases: dict[Edge, np.ndarray],
) -> np.ndarray:
    """Return the unsigned local endpoint Gram in sorted incident-edge order."""

    incident_edges = tuple(sorted(incident_edges))
    if any(vertex not in edge for edge in incident_edges):
        raise ValueError("every supplied edge must be incident to the vertex")
    if not incident_edges:
        return np.zeros((0, 0), dtype=complex)
    return np.concatenate(
        [edge_bases[edge] for edge in incident_edges], axis=1
    ).conj().T @ np.concatenate(
        [edge_bases[edge] for edge in incident_edges], axis=1
    )


def vertex_kernel_side_matrices(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    left_vertices: tuple[Vertex, ...],
    edge_dimensions: dict[Edge, int],
    local_endpoint_grams: dict[Vertex, np.ndarray],
    *,
    tolerance: float = 1e-9,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Embed signed local PSD kernels into the two sibling side matrices."""

    edges = _canonical_edges(edges)
    vertex_set = set(vertices)
    if vertex_set != {vertex for edge in edges for vertex in edge}:
        raise ValueError("vertices must equal the support of the edge graph")
    left = set(left_vertices)
    if not left or left == vertex_set or not left <= vertex_set:
        raise ValueError("the split must have two nonempty children")
    offsets = _edge_offsets(edges, edge_dimensions)
    total_dimension = offsets[edges[-1]][1]
    side_left = np.zeros((total_dimension, total_dimension), dtype=complex)
    side_right = np.zeros_like(side_left)
    minimum_kernel = math.inf
    diagonal_residual = 0.0

    for vertex in vertices:
        incident = tuple(sorted(edge for edge in edges if vertex in edge))
        local_offsets = _edge_offsets(incident, edge_dimensions)
        local_dimension = local_offsets[incident[-1]][1]
        kernel = np.asarray(local_endpoint_grams[vertex], dtype=complex)
        if kernel.shape != (local_dimension, local_dimension):
            raise ValueError("local endpoint kernel has the wrong shape")
        kernel = (kernel + kernel.conj().T) / 2
        minimum_kernel = min(
            minimum_kernel,
            float(np.linalg.eigvalsh(kernel).min()),
        )
        for edge in incident:
            local_start, local_stop = local_offsets[edge]
            dimension = edge_dimensions[edge]
            diagonal_residual = max(
                diagonal_residual,
                float(
                    np.linalg.norm(
                        kernel[
                            local_start:local_stop,
                            local_start:local_stop,
                        ]
                        - np.eye(dimension),
                        ord=2,
                    )
                ),
            )
        if minimum_kernel < -100 * tolerance:
            raise ValueError("local endpoint kernels must be positive semidefinite")
        if diagonal_residual > 100 * tolerance:
            raise ValueError("local endpoint kernels need identity diagonal blocks")

        target = side_left if vertex in left else side_right
        for first in incident:
            first_local = local_offsets[first]
            first_global = offsets[first]
            first_sign = 1 if vertex == first[0] else -1
            for second in incident:
                second_local = local_offsets[second]
                second_global = offsets[second]
                second_sign = 1 if vertex == second[0] else -1
                target[
                    first_global[0] : first_global[1],
                    second_global[0] : second_global[1],
                ] += first_sign * second_sign * kernel[
                    first_local[0] : first_local[1],
                    second_local[0] : second_local[1],
                ]

    left_internal = tuple(
        edge for edge in edges if edge[0] in left and edge[1] in left
    )
    right_internal = tuple(
        edge for edge in edges if edge[0] not in left and edge[1] not in left
    )
    crossing = tuple(
        edge for edge in edges if (edge[0] in left) != (edge[1] in left)
    )
    return side_left, side_right, {
        "offsets": offsets,
        "left_internal_edges": left_internal,
        "right_internal_edges": right_internal,
        "crossing_edges": crossing,
        "minimum_local_kernel_eigenvalue": minimum_kernel,
        "maximum_local_identity_diagonal_residual": diagonal_residual,
    }


def _short_to_crossing(
    side_matrix: np.ndarray,
    internal_indices: tuple[int, ...],
    crossing_indices: tuple[int, ...],
    *,
    tolerance: float,
) -> np.ndarray:
    cc = side_matrix[np.ix_(crossing_indices, crossing_indices)]
    if not internal_indices:
        return (cc + cc.conj().T) / 2
    ii = side_matrix[np.ix_(internal_indices, internal_indices)]
    ic = side_matrix[np.ix_(internal_indices, crossing_indices)]
    short = cc - ic.conj().T @ np.linalg.pinv(ii, rcond=tolerance) @ ic
    return (short + short.conj().T) / 2


def direct_internal_schur_quotient(
    metric: np.ndarray,
    grading: np.ndarray,
    internal_indices: tuple[int, ...],
    crossing_indices: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply the metric-orthogonal internal quotient to ``M`` and ``J``."""

    xx = metric[np.ix_(crossing_indices, crossing_indices)]
    jxx = grading[np.ix_(crossing_indices, crossing_indices)]
    if not internal_indices:
        return (xx + xx.conj().T) / 2, (jxx + jxx.conj().T) / 2
    ii = metric[np.ix_(internal_indices, internal_indices)]
    ix = metric[np.ix_(internal_indices, crossing_indices)]
    jii = grading[np.ix_(internal_indices, internal_indices)]
    jix = grading[np.ix_(internal_indices, crossing_indices)]
    coefficients = np.linalg.pinv(ii, rcond=tolerance) @ ix
    quotient_metric = xx - ix.conj().T @ coefficients
    quotient_grading = (
        jxx
        - coefficients.conj().T @ jix
        - jix.conj().T @ coefficients
        + coefficients.conj().T @ jii @ coefficients
    )
    return (
        (quotient_metric + quotient_metric.conj().T) / 2,
        (quotient_grading + quotient_grading.conj().T) / 2,
    )


def _inverse_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    if float(values.min()) <= 100 * tolerance:
        raise ValueError("endpoint comparison requires a positive definite metric")
    return vectors @ np.diag(1 / np.sqrt(values)) @ vectors.conj().T


def audit_vertex_kernel_reduction(
    control_id: str,
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    left_vertices: tuple[Vertex, ...],
    edge_dimensions: dict[Edge, int],
    local_endpoint_grams: dict[Vertex, np.ndarray],
    *,
    tolerance: float = 1e-9,
) -> VertexKernelReductionControl:
    """Audit equations (1)-(2) and endpoint-effect comparability exactly."""

    edges = _canonical_edges(edges)
    side_left, side_right, metadata = vertex_kernel_side_matrices(
        vertices,
        edges,
        left_vertices,
        edge_dimensions,
        local_endpoint_grams,
        tolerance=tolerance,
    )
    offsets = metadata["offsets"]
    left_internal = metadata["left_internal_edges"]
    right_internal = metadata["right_internal_edges"]
    crossing = metadata["crossing_edges"]
    if not crossing:
        raise ValueError("the channel has no crossing edge")
    left_indices = _edge_indices(left_internal, offsets)
    right_indices = _edge_indices(right_internal, offsets)
    internal_indices = (*left_indices, *right_indices)
    crossing_indices = _edge_indices(crossing, offsets)

    metric = side_left + side_right
    grading = side_left - side_right
    direct_metric, direct_grading = direct_internal_schur_quotient(
        metric,
        grading,
        internal_indices,
        crossing_indices,
        tolerance=tolerance,
    )
    left_effect = _short_to_crossing(
        side_left,
        left_indices,
        crossing_indices,
        tolerance=tolerance,
    )
    right_effect = _short_to_crossing(
        side_right,
        right_indices,
        crossing_indices,
        tolerance=tolerance,
    )
    predicted_metric = left_effect + right_effect
    predicted_grading = left_effect - right_effect
    metric_residual = float(
        np.linalg.norm(direct_metric - predicted_metric, ord=2)
    )
    grading_residual = float(
        np.linalg.norm(direct_grading - predicted_grading, ord=2)
    )

    metric_inverse_root = _inverse_root(predicted_metric, tolerance)
    defect_operator = metric_inverse_root @ predicted_grading @ metric_inverse_root
    defect_operator = (defect_operator + defect_operator.conj().T) / 2
    defect = float(np.max(np.abs(np.linalg.eigvalsh(defect_operator))))
    right_inverse_root = _inverse_root(right_effect, tolerance)
    ratio_operator = right_inverse_root @ left_effect @ right_inverse_root
    ratios = np.linalg.eigvalsh((ratio_operator + ratio_operator.conj().T) / 2)
    ratio_defect = max(
        abs(float((ratio - 1) / (ratio + 1))) for ratio in ratios
    )
    ratio_residual = abs(defect - ratio_defect)
    verified = bool(
        metric_residual <= 100 * tolerance
        and grading_residual <= 100 * tolerance
        and ratio_residual <= 100 * tolerance
    )
    return VertexKernelReductionControl(
        control_id=control_id,
        vertex_count=len(vertices),
        edge_count=len(edges),
        crossing_edge_count=len(crossing),
        left_internal_edge_count=len(left_internal),
        right_internal_edge_count=len(right_internal),
        total_coefficient_dimension=metric.shape[0],
        crossing_coefficient_dimension=len(crossing_indices),
        minimum_local_kernel_eigenvalue=float(
            metadata["minimum_local_kernel_eigenvalue"]
        ),
        maximum_local_identity_diagonal_residual=float(
            metadata["maximum_local_identity_diagonal_residual"]
        ),
        quotient_metric_minimum_eigenvalue=float(
            np.linalg.eigvalsh(predicted_metric).min()
        ),
        left_endpoint_effect_minimum_eigenvalue=float(
            np.linalg.eigvalsh(left_effect).min()
        ),
        right_endpoint_effect_minimum_eigenvalue=float(
            np.linalg.eigvalsh(right_effect).min()
        ),
        grading_defect_norm=defect,
        endpoint_gap=(1 - defect) / 2,
        generalized_ratio_minimum=float(ratios.min()),
        generalized_ratio_maximum=float(ratios.max()),
        generalized_ratio_predicted_defect=ratio_defect,
        direct_to_shorted_metric_residual=metric_residual,
        direct_to_shorted_grading_residual=grading_residual,
        generalized_ratio_defect_residual=ratio_residual,
        exact_vertex_kernel_reduction_verified=verified,
        status=(
            "vertex-kernel-graded-reduction-verified"
            if verified
            else "vertex-kernel-graded-reduction-mismatch"
        ),
    )


def uniform_scalar_endpoint_grams(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    correlation: float,
) -> tuple[dict[Edge, int], dict[Vertex, np.ndarray]]:
    """Build local equicorrelation kernels for the old flat scalar model."""

    if not 0 <= correlation < 1:
        raise ValueError("correlation must lie in [0,1)")
    edges = _canonical_edges(edges)
    dimensions = {edge: 1 for edge in edges}
    kernels = {}
    for vertex in vertices:
        degree = sum(vertex in edge for edge in edges)
        kernels[vertex] = (
            (1 - correlation) * np.eye(degree)
            + correlation * np.ones((degree, degree))
        )
    return dimensions, kernels


def _matrix_endpoint_grams(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    fiber_dimension: int,
) -> tuple[dict[Edge, int], dict[Vertex, np.ndarray]]:
    """Deterministic PSD matrix-valued control with varying local amplitudes."""

    edges = _canonical_edges(edges)
    dimensions = {edge: fiber_dimension for edge in edges}
    kernels: dict[Vertex, np.ndarray] = {}
    for vertex in vertices:
        incident = tuple(edge for edge in edges if vertex in edge)
        degree = len(incident)
        common_dimension = fiber_dimension
        ambient = degree * fiber_dimension + common_dimension
        embeddings = []
        for index, _edge in enumerate(incident):
            weight = 0.12 + 0.07 * ((vertex + 2 * index) % 4)
            phase = 0.19 * (1 + vertex) * (1 + index)
            unitary = np.eye(fiber_dimension, dtype=complex)
            if fiber_dimension >= 2:
                unitary[:2, :2] = np.array(
                    [
                        [math.cos(phase), -math.sin(phase)],
                        [math.sin(phase), math.cos(phase)],
                    ],
                    dtype=complex,
                )
                unitary[1, 1] *= np.exp(0.13j * (vertex + index + 1))
                unitary[:, 1] /= np.linalg.norm(unitary[:, 1])
                q, _ = np.linalg.qr(unitary)
                unitary = q
            embedding = np.zeros((ambient, fiber_dimension), dtype=complex)
            start = index * fiber_dimension
            embedding[start : start + fiber_dimension] = math.sqrt(1 - weight) * np.eye(
                fiber_dimension
            )
            embedding[-common_dimension:] = math.sqrt(weight) * unitary
            embeddings.append(embedding)
        joined = np.concatenate(embeddings, axis=1)
        kernels[vertex] = joined.conj().T @ joined
    return dimensions, kernels


def audit_physical_vertex_kernels(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    orientation_family: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> PhysicalVertexKernelControl:
    """Run every crossing bit split directly on physical residual pair cores."""

    edges = live_pair_cores(target, labels, orientation_family)
    bases = _core_bases(target, labels, edges)
    residual, removed = global_residual_pair_core_bases(
        bases,
        edges,
        tolerance=tolerance,
    )
    residual_edges = tuple(sorted(residual))
    vertices = tuple(
        sorted({vertex for edge in residual_edges for vertex in edge})
    )
    dimensions = {edge: residual[edge].shape[1] for edge in residual_edges}
    local = {
        vertex: endpoint_gram_from_edge_bases(
            vertex,
            tuple(edge for edge in residual_edges if vertex in edge),
            residual,
        )
        for vertex in vertices
    }
    split_controls = []
    for bit in range(len(labels)):
        left = tuple(vertex for vertex in vertices if not (vertex >> bit) & 1)
        if not left or len(left) == len(vertices):
            continue
        if not any(
            (edge[0] in set(left)) != (edge[1] in set(left))
            for edge in residual_edges
        ):
            continue
        split_controls.append(
            audit_vertex_kernel_reduction(
                f"{control_id}-BIT-{bit}",
                vertices,
                residual_edges,
                left,
                dimensions,
                local,
                tolerance=tolerance,
            )
        )
    maximum_residual = max(
        (
            max(
                row.direct_to_shorted_metric_residual,
                row.direct_to_shorted_grading_residual,
            )
            for row in split_controls
        ),
        default=0.0,
    )
    verified = bool(
        split_controls
        and all(row.exact_vertex_kernel_reduction_verified for row in split_controls)
    )
    return PhysicalVertexKernelControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        orientation_count=len(orientation_family),
        live_pair_core_count=len(edges),
        residual_pair_core_count=len(residual_edges),
        exact_common_dimension_removed=removed,
        audited_split_count=len(split_controls),
        maximum_grading_defect_norm=max(
            (row.grading_defect_norm for row in split_controls), default=0.0
        ),
        minimum_endpoint_gap=min(
            (row.endpoint_gap for row in split_controls), default=0.5
        ),
        maximum_direct_to_shorted_residual=maximum_residual,
        all_splits_verified=verified,
        split_controls=split_controls,
        status=(
            "physical-vertex-kernel-splits-verified"
            if verified
            else "physical-vertex-kernel-split-failure"
        ),
    )


def run_vertex_kernel_graded_reduction() -> VertexKernelGradedReductionReport:
    plane_vertices = (2, 5, 11, 12)
    plane_star = ((2, 12), (5, 12), (11, 12))
    scalar_dimensions, scalar_kernels = uniform_scalar_endpoint_grams(
        plane_vertices,
        plane_star,
        1 / 5,
    )
    nonuniform_kernels = {
        0: np.array(
            [
                [1.0, 0.10, 0.18],
                [0.10, 1.0, 0.27],
                [0.18, 0.27, 1.0],
            ]
        ),
        1: np.eye(1),
        2: np.eye(1),
        3: np.eye(1),
    }
    nonuniform_vertices = (0, 1, 2, 3)
    nonuniform_edges = ((0, 1), (0, 2), (0, 3))
    matrix_vertices = tuple(range(6))
    matrix_edges = (
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 4),
        (2, 5),
        (3, 4),
        (3, 5),
        (4, 5),
    )
    matrix_dimensions, matrix_kernels = _matrix_endpoint_grams(
        matrix_vertices,
        matrix_edges,
        2,
    )
    bipartite_vertices = tuple(range(8))
    bipartite_left = tuple(range(4))
    bipartite_edges = tuple(
        (left, right) for left in bipartite_left for right in range(4, 8)
    )
    bipartite_dimensions, bipartite_kernels = uniform_scalar_endpoint_grams(
        bipartite_vertices,
        bipartite_edges,
        1 / 5,
    )
    abstract = [
        audit_vertex_kernel_reduction(
            "UNIFORM-SCALAR-AFFINE-STAR",
            plane_vertices,
            plane_star,
            (2, 5),
            scalar_dimensions,
            scalar_kernels,
        ),
        audit_vertex_kernel_reduction(
            "NONUNIFORM-SCALAR-AFFINE-STAR",
            nonuniform_vertices,
            nonuniform_edges,
            (0, 1),
            {edge: 1 for edge in nonuniform_edges},
            nonuniform_kernels,
        ),
        audit_vertex_kernel_reduction(
            "MATRIX-VALUED-NONUNIFORM-SHEAF",
            matrix_vertices,
            matrix_edges,
            (0, 1, 2),
            matrix_dimensions,
            matrix_kernels,
        ),
        audit_vertex_kernel_reduction(
            "CROSSING-ONLY-K4-4-MATRIX-FRAMEWORK-NO-GO",
            bipartite_vertices,
            bipartite_edges,
            bipartite_left,
            bipartite_dimensions,
            bipartite_kernels,
        ),
    ]

    labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (2, 2, 1, 1)),
        ((4, 2), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    physical = [
        audit_physical_vertex_kernels(
            "W6-CARRIER-5-PHYSICAL-VERTEX-KERNEL",
            (6,),
            labels,
            tuple(range(16)),
        )
    ]
    failures = sum(
        not row.exact_vertex_kernel_reduction_verified for row in abstract
    ) + sum(not row.all_splits_verified for row in physical)
    all_controls = [*abstract, *(row for item in physical for row in item.split_controls)]
    maximum_residual = max(
        (
            max(
                row.direct_to_shorted_metric_residual,
                row.direct_to_shorted_grading_residual,
            )
            for row in all_controls
        ),
        default=0.0,
    )
    bipartite = abstract[-1]
    verified = failures == 0
    metrics: dict[str, int | float] = {
        "arbitrary_psd_vertex_kernel_reduction_theorem_count": 1,
        "matrix_valued_sheaf_reduction_theorem_count": 1,
        "nonuniform_correlation_reduction_theorem_count": 1,
        "abstract_control_count": len(abstract),
        "physical_control_count": len(physical),
        "physical_split_control_count": sum(
            row.audited_split_count for row in physical
        ),
        "control_failure_count": failures,
        "maximum_direct_to_shorted_residual": maximum_residual,
        "crossing_bipartite_endpoint_gap": bipartite.endpoint_gap,
        "natural_endpoint_comparability_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return VertexKernelGradedReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_input": (
                "Each orientation vertex supplies an arbitrary PSD block Gram "
                "kernel on its incident pair-core coefficient fibers."
            ),
            "full_relation": "M=A_L+A_R and J=A_L-A_R after incidence signs.",
            "shorted_endpoint_identity": (
                "After eliminating all same-child edge variables, M_q=E_L+E_R "
                "and J_q=E_L-E_R for the two child shorted endpoint kernels."
            ),
            "comparability": (
                "Generalized eigenvalue t of E_L relative to E_R contributes "
                "grading defect (t-1)/(t+1)."
            ),
            "scope": (
                "The reduction permits unequal dimensions, varying correlations, "
                "and matrix fibers. It does not prove natural endpoint comparability."
            ),
        },
        abstract_controls=abstract,
        physical_controls=physical,
        proof_obligations=[
            {
                "obligation": "remove_uniform_scalar_channel_assumption",
                "resolved": verified,
                "resolution": "The side-short identity is algebraic for arbitrary PSD vertex kernels and variable edge fibers.",
            },
            {
                "obligation": "admit_noncommuting_matrix_multiplicity_sheaves",
                "resolved": verified,
                "resolution": "A two-dimensional nonuniform matrix-fiber control matches the direct graded quotient.",
            },
            {
                "obligation": "prove_natural_shorted_endpoint_comparability",
                "resolved": False,
                "resolution": "Need representation-theoretic control of the physical child shorts on globally distinct Plancherel portfolios.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Different reciprocal carrier scales invalidate the graph reduction.",
                "resolved": True,
                "resolution": "They enter the local PSD kernels directly; no common gamma is used in the side-short theorem.",
            },
            {
                "objection": "Noncommuting multiplicity maps cannot be scalar-channel atomized.",
                "resolved": True,
                "resolution": "Scalar atomization is unnecessary for equations (1)-(2); full matrix endpoint kernels are retained.",
            },
            {
                "objection": "The general theorem itself forces a constant endpoint gap.",
                "resolved": False,
                "resolution": "The crossing-only K4,4 control remains poorly conditioned and scales to zero gap.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "arbitrary_psd_vertex_kernel_reduction_proved": verified,
            "nonuniform_correlations_supported": verified,
            "matrix_valued_multiplicity_sheaves_supported": verified,
            "physical_w6_direct_short_identity_verified": all(
                row.all_splits_verified for row in physical
            ),
            "scalar_channelization_required_for_reduction": False,
            "natural_shorted_endpoint_comparability_proved": False,
            "natural_pgm_endpoint_gap_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact graded target now covers the full physical matrix "
                "sheaf, but no natural-mass theorem compares its two child shorts."
            ),
        },
        status=(
            "arbitrary-vertex-kernel-graded-reduction-verified-"
            "natural-comparability-open"
            if verified
            else "vertex-kernel-graded-reduction-control-failure"
        ),
        summary=(
            "Extended the graded endpoint-effect theorem from one uniform scalar "
            "gamma to arbitrary PSD, nonuniform, matrix-valued physical kernels."
        ),
        falsifiers_triggered=[
            "A common residual correlation is not required to define the exact graded quotient.",
            "Failure of commuting support-projector atomization no longer blocks finite physical evaluation.",
            "The crossing-only bipartite family still proves that endpoint comparability is substantive, not automatic.",
        ],
    )


def write_vertex_kernel_graded_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_vertex_kernel_graded_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_vertex_kernel_graded_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
