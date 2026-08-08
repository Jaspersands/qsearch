"""Exact hierarchical resolution of emergent synthesis dependencies.

Direct pair-common relations need not generate the synthesis kernel.  A binary
span hierarchy nevertheless gives an exact information-theoretic resolution.
For a node ``T=L union R`` with child syntheses ``S_L,S_R``, let

    V_L=range(S_L),  V_R=range(S_R),  K=V_L intersection V_R.

Every parent dependency has a unique orthogonal decomposition into a left
child dependency, a right child dependency, and

    z_x = S_L^+ x direct_sum (-S_R^+ x),   x in K.          (1)

Indeed, the Moore-Penrose preimages in (1) are orthogonal to the child
kernels and synthesize to ``x-x=0``.  Dimension counting then gives

    ker[S_L S_R] = ker S_L direct_sum ker S_R direct_sum Z_K. (2)

Recursing (2) resolves the full leaf synthesis kernel even when every
original pair intersection vanishes.  This is the correct information-level
answer to the augmented-H0 obstruction.

The same formula exposes the remaining conditioning problem.  Write
``F_s=S_s S_s^*``.  In an orthonormal basis ``X`` of ``K``, the parent relation
metric and sibling grading are

    M = X^*(F_L^+ + F_R^+)X,
    J = X^*(F_L^+ - F_R^+)X.                               (3)

Thus the endpoint gap is controlled by comparability of the two child
pseudoinverse frames on their common span.  Completeness alone gives no such
bound.  If the left child contains ``p`` copies of one line while the right
child contains that line once plus ``p-1`` orthogonal lines, (2) is exact but
the smaller endpoint weight is ``1/(p+1)``.  At exponentially wide nodes this
is exponentially small.

This module proves exact hierarchical cokernel completeness and precisely
relocates the research gate to natural child-frame comparability and coherent
implementation.  It does not prove either gate.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_augmented_common_core_cech import (
    augmented_common_core_cech_data,
)
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_relation_cokernel_transfer import pair_common_boundary


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_hierarchical_cokernel_resolution.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HierarchicalCokernelNode:
    node_id: str
    leaf_indices: tuple[int, ...]
    left_leaf_count: int
    right_leaf_count: int
    coefficient_dimension: int
    physical_span_rank: int
    kernel_dimension: int
    left_internal_kernel_dimension: int
    right_internal_kernel_dimension: int
    parent_span_intersection_dimension: int
    decomposed_kernel_dimension: int
    kernel_dimension_identity_residual: int
    relation_annihilation_residual: float
    relation_to_child_kernel_orthogonality_residual: float
    hierarchical_kernel_projector_residual: float
    pseudoinverse_metric_formula_residual: float
    pseudoinverse_grading_formula_residual: float
    maximum_grading_defect: float
    minimum_endpoint_gap: float
    exact_node_cokernel_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class HierarchicalCokernelControl:
    control_id: str
    control_family: str
    physical_dimension: int
    leaf_count: int
    leaf_coefficient_dimension: int
    root_synthesis_rank: int
    root_kernel_dimension: int
    original_pair_relation_rank: int
    original_pair_emergent_h0_dimension: int
    hierarchical_parent_relation_dimension_sum: int
    nontrivial_parent_relation_node_count: int
    minimum_hierarchical_endpoint_gap: float
    maximum_hierarchical_grading_defect: float
    maximum_kernel_projector_residual: float
    maximum_metric_formula_residual: float
    maximum_grading_formula_residual: float
    hierarchical_relations_exhaust_root_kernel: bool
    exact_hierarchical_cokernel_audit: bool
    nodes: list[HierarchicalCokernelNode]
    status: str


@dataclass(frozen=True)
class HierarchicalConditioningCounterRecord:
    child_width: int
    total_leaf_count: int
    left_common_frame_eigenvalue: float
    right_common_frame_eigenvalue: float
    left_pseudoinverse_weight: float
    right_pseudoinverse_weight: float
    grading_defect: float
    minimum_endpoint_gap: float
    inverse_gap_cost: float
    exact_hierarchy_complete: bool
    constant_endpoint_gap: bool
    status: str


@dataclass(frozen=True)
class HierarchicalCokernelResolutionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[HierarchicalCokernelControl]
    conditioning_counterfamily: list[HierarchicalConditioningCounterRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@dataclass
class _NodeData:
    synthesis: np.ndarray
    kernel_basis: np.ndarray
    relation_basis: np.ndarray
    records: list[HierarchicalCokernelNode]
    leaf_indices: tuple[int, ...]


def _matrix_rank(matrix: np.ndarray, tolerance: float) -> int:
    if not matrix.size:
        return 0
    return int(np.sum(np.linalg.svd(matrix, compute_uv=False) > 100 * tolerance))


def _orthonormal_span(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if not matrix.size or not matrix.shape[1]:
        return np.zeros((matrix.shape[0], 0), dtype=complex)
    left, values, _ = np.linalg.svd(matrix, full_matrices=False)
    return left[:, values > 100 * tolerance]


def _kernel_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if not matrix.shape[1]:
        return np.zeros((0, 0), dtype=complex)
    _, values, right = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(values > 100 * tolerance))
    return right[rank:, :].conj().T


def _intersection_basis(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    if not left.shape[1] or not right.shape[1]:
        return np.zeros((left.shape[0], 0), dtype=complex)
    overlap = left.conj().T @ right
    left_vectors, singular_values, _ = np.linalg.svd(
        overlap,
        full_matrices=False,
    )
    common = singular_values >= 1 - 100 * tolerance
    return left @ left_vectors[:, common]


def _projector(basis: np.ndarray) -> np.ndarray:
    return basis @ basis.conj().T


def _embed_child_kernels(
    left_kernel: np.ndarray,
    right_kernel: np.ndarray,
    left_dimension: int,
    right_dimension: int,
) -> np.ndarray:
    output = np.zeros(
        (
            left_dimension + right_dimension,
            left_kernel.shape[1] + right_kernel.shape[1],
        ),
        dtype=complex,
    )
    output[:left_dimension, : left_kernel.shape[1]] = left_kernel
    output[
        left_dimension:,
        left_kernel.shape[1] :,
    ] = right_kernel
    return output


def _generalized_defect(
    metric: np.ndarray,
    grading: np.ndarray,
    tolerance: float,
) -> tuple[float, float]:
    if not metric.size:
        return 0.0, 0.5
    values, vectors = np.linalg.eigh((metric + metric.conj().T) / 2)
    if values[0] <= 100 * tolerance:
        raise ArithmeticError("parent relation metric is singular")
    inverse_root = (vectors * values**-0.5) @ vectors.conj().T
    defect = inverse_root @ grading @ inverse_root
    defect_values = np.linalg.eigvalsh((defect + defect.conj().T) / 2)
    maximum = max((abs(float(value)) for value in defect_values), default=0.0)
    return maximum, (1 - maximum) / 2


def _resolve_node(
    leaf_bases: tuple[np.ndarray, ...],
    leaf_indices: tuple[int, ...],
    node_id: str,
    tolerance: float,
) -> _NodeData:
    if len(leaf_indices) == 1:
        synthesis = leaf_bases[leaf_indices[0]]
        kernel = _kernel_basis(synthesis, tolerance)
        return _NodeData(
            synthesis=synthesis,
            kernel_basis=kernel,
            relation_basis=np.zeros((synthesis.shape[1], 0), dtype=complex),
            records=[],
            leaf_indices=leaf_indices,
        )

    middle = len(leaf_indices) // 2
    left = _resolve_node(
        leaf_bases,
        leaf_indices[:middle],
        f"{node_id}L",
        tolerance,
    )
    right = _resolve_node(
        leaf_bases,
        leaf_indices[middle:],
        f"{node_id}R",
        tolerance,
    )
    synthesis = np.concatenate((left.synthesis, right.synthesis), axis=1)
    left_dimension = left.synthesis.shape[1]
    right_dimension = right.synthesis.shape[1]
    left_span = _orthonormal_span(left.synthesis, tolerance)
    right_span = _orthonormal_span(right.synthesis, tolerance)
    common = _intersection_basis(left_span, right_span, tolerance)

    left_inverse = np.linalg.pinv(left.synthesis, rcond=tolerance)
    right_inverse = np.linalg.pinv(right.synthesis, rcond=tolerance)
    relation = np.vstack(
        (left_inverse @ common, -(right_inverse @ common))
    )
    internal = _embed_child_kernels(
        left.kernel_basis,
        right.kernel_basis,
        left_dimension,
        right_dimension,
    )
    decomposition = np.concatenate((internal, relation), axis=1)
    decomposition_basis = _orthonormal_span(decomposition, tolerance)
    kernel = _kernel_basis(synthesis, tolerance)

    annihilation = float(
        np.linalg.norm(synthesis @ relation, ord=2)
        if relation.shape[1]
        else 0.0
    )
    orthogonality = float(
        np.linalg.norm(internal.conj().T @ relation, ord=2)
        if internal.shape[1] and relation.shape[1]
        else 0.0
    )
    projector_residual = float(
        np.linalg.norm(
            _projector(decomposition_basis) - _projector(kernel),
            ord=2,
        )
    )

    actual_metric = relation.conj().T @ relation
    grading_operator = np.diag(
        np.concatenate(
            (np.ones(left_dimension), -np.ones(right_dimension))
        )
    )
    actual_grading = relation.conj().T @ grading_operator @ relation
    left_frame = left.synthesis @ left.synthesis.conj().T
    right_frame = right.synthesis @ right.synthesis.conj().T
    left_frame_inverse = np.linalg.pinv(left_frame, rcond=tolerance)
    right_frame_inverse = np.linalg.pinv(right_frame, rcond=tolerance)
    predicted_metric = (
        common.conj().T
        @ (left_frame_inverse + right_frame_inverse)
        @ common
    )
    predicted_grading = (
        common.conj().T
        @ (left_frame_inverse - right_frame_inverse)
        @ common
    )
    metric_residual = float(
        np.linalg.norm(actual_metric - predicted_metric, ord=2)
        if actual_metric.size
        else 0.0
    )
    grading_residual = float(
        np.linalg.norm(actual_grading - predicted_grading, ord=2)
        if actual_grading.size
        else 0.0
    )
    defect, endpoint_gap = _generalized_defect(
        actual_metric,
        actual_grading,
        tolerance,
    )
    decomposed_dimension = decomposition_basis.shape[1]
    dimension_identity_residual = abs(kernel.shape[1] - decomposed_dimension)
    verified = bool(
        dimension_identity_residual == 0
        and annihilation <= 1000 * tolerance
        and orthogonality <= 1000 * tolerance
        and projector_residual <= 1000 * tolerance
        and metric_residual <= 1000 * tolerance
        and grading_residual <= 1000 * tolerance
        and relation.shape[1] == common.shape[1]
    )
    record = HierarchicalCokernelNode(
        node_id=node_id,
        leaf_indices=leaf_indices,
        left_leaf_count=len(left.leaf_indices),
        right_leaf_count=len(right.leaf_indices),
        coefficient_dimension=synthesis.shape[1],
        physical_span_rank=_matrix_rank(synthesis, tolerance),
        kernel_dimension=kernel.shape[1],
        left_internal_kernel_dimension=left.kernel_basis.shape[1],
        right_internal_kernel_dimension=right.kernel_basis.shape[1],
        parent_span_intersection_dimension=common.shape[1],
        decomposed_kernel_dimension=decomposed_dimension,
        kernel_dimension_identity_residual=dimension_identity_residual,
        relation_annihilation_residual=annihilation,
        relation_to_child_kernel_orthogonality_residual=orthogonality,
        hierarchical_kernel_projector_residual=projector_residual,
        pseudoinverse_metric_formula_residual=metric_residual,
        pseudoinverse_grading_formula_residual=grading_residual,
        maximum_grading_defect=defect,
        minimum_endpoint_gap=endpoint_gap,
        exact_node_cokernel_decomposition_verified=verified,
        status=(
            "exact-hierarchical-parent-cokernel-decomposition"
            if verified
            else "hierarchical-parent-cokernel-decomposition-failure"
        ),
    )
    relation_basis = np.concatenate(
        (
            internal[:, : left.kernel_basis.shape[1]],
            internal[:, left.kernel_basis.shape[1] :],
            relation,
        ),
        axis=1,
    )
    return _NodeData(
        synthesis=synthesis,
        kernel_basis=kernel,
        relation_basis=relation_basis,
        records=[*left.records, *right.records, record],
        leaf_indices=leaf_indices,
    )


def audit_hierarchical_cokernel_resolution(
    control_id: str,
    control_family: str,
    leaf_bases: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> HierarchicalCokernelControl:
    if len(leaf_bases) < 2:
        raise ValueError("at least two leaf subspaces are required")
    physical_dimension = leaf_bases[0].shape[0]
    if any(basis.shape[0] != physical_dimension for basis in leaf_bases):
        raise ValueError("all leaf bases must share a physical carrier")
    for basis in leaf_bases:
        if basis.shape[1] and np.linalg.norm(
            basis.conj().T @ basis - np.eye(basis.shape[1]), ord=2
        ) > 1000 * tolerance:
            raise ValueError("leaf bases must be isometries")

    root = _resolve_node(
        leaf_bases,
        tuple(range(len(leaf_bases))),
        "ROOT",
        tolerance,
    )
    pair_boundary = pair_common_boundary(leaf_bases, tolerance=tolerance)
    pair_rank = _matrix_rank(pair_boundary, tolerance)
    root_kernel = root.kernel_basis.shape[1]
    direct_h0 = root_kernel - pair_rank
    relation_sum = sum(
        record.parent_span_intersection_dimension for record in root.records
    )
    nontrivial = [
        record
        for record in root.records
        if record.parent_span_intersection_dimension
    ]
    exact = bool(
        all(record.exact_node_cokernel_decomposition_verified for record in root.records)
        and relation_sum == root_kernel
    )
    return HierarchicalCokernelControl(
        control_id=control_id,
        control_family=control_family,
        physical_dimension=physical_dimension,
        leaf_count=len(leaf_bases),
        leaf_coefficient_dimension=root.synthesis.shape[1],
        root_synthesis_rank=_matrix_rank(root.synthesis, tolerance),
        root_kernel_dimension=root_kernel,
        original_pair_relation_rank=pair_rank,
        original_pair_emergent_h0_dimension=direct_h0,
        hierarchical_parent_relation_dimension_sum=relation_sum,
        nontrivial_parent_relation_node_count=len(nontrivial),
        minimum_hierarchical_endpoint_gap=min(
            (record.minimum_endpoint_gap for record in nontrivial),
            default=0.5,
        ),
        maximum_hierarchical_grading_defect=max(
            (record.maximum_grading_defect for record in nontrivial),
            default=0.0,
        ),
        maximum_kernel_projector_residual=max(
            (record.hierarchical_kernel_projector_residual for record in root.records),
            default=0.0,
        ),
        maximum_metric_formula_residual=max(
            (record.pseudoinverse_metric_formula_residual for record in root.records),
            default=0.0,
        ),
        maximum_grading_formula_residual=max(
            (record.pseudoinverse_grading_formula_residual for record in root.records),
            default=0.0,
        ),
        hierarchical_relations_exhaust_root_kernel=relation_sum == root_kernel,
        exact_hierarchical_cokernel_audit=exact,
        nodes=root.records,
        status=(
            "exact-hierarchical-cokernel-resolution"
            if exact
            else "hierarchical-cokernel-resolution-failure"
        ),
    )


def conditioning_counter_record(
    child_width: int,
) -> HierarchicalConditioningCounterRecord:
    if child_width < 1:
        raise ValueError("child width must be positive")
    left_weight = 1 / child_width
    right_weight = 1.0
    defect = abs(left_weight - right_weight) / (left_weight + right_weight)
    gap = (1 - defect) / 2
    return HierarchicalConditioningCounterRecord(
        child_width=child_width,
        total_leaf_count=2 * child_width,
        left_common_frame_eigenvalue=float(child_width),
        right_common_frame_eigenvalue=1.0,
        left_pseudoinverse_weight=left_weight,
        right_pseudoinverse_weight=right_weight,
        grading_defect=defect,
        minimum_endpoint_gap=gap,
        inverse_gap_cost=1 / gap,
        exact_hierarchy_complete=True,
        constant_endpoint_gap=gap >= 0.1,
        status=(
            "complete-hierarchy-constant-gap-small-width"
            if gap >= 0.1
            else "complete-hierarchy-vanishing-endpoint-gap"
        ),
    )


def _abstract_controls() -> list[HierarchicalCokernelControl]:
    e0 = np.asarray([[1.0], [0.0]], dtype=complex)
    e1 = np.asarray([[0.0], [1.0]], dtype=complex)
    diagonal = (e0 + e1) / np.sqrt(2)
    zero = np.zeros((2, 0), dtype=complex)

    width = 8
    standard = tuple(
        np.eye(width, dtype=complex)[:, [index]]
        for index in range(width)
    )
    imbalanced = (standard[0],) * width + standard
    return [
        audit_hierarchical_cokernel_resolution(
            "THREE-LINES-EMERGENT-DEPENDENCY-RESOLVED",
            "abstract-emergent-h0",
            (e0, e1, diagonal, zero),
        ),
        audit_hierarchical_cokernel_resolution(
            "FOUR-IDENTICAL-LINES-HIERARCHICAL-INCIDENCE",
            "abstract-pair-generated",
            (e0, e0, e0, e0),
        ),
        audit_hierarchical_cokernel_resolution(
            "IMBALANCED-COMPLETE-HIERARCHY-WIDTH-8",
            "abstract-conditioning-counterfamily",
            imbalanced,
        ),
    ]


def _physical_control() -> HierarchicalCokernelControl:
    labels: tuple[Label, ...] = (
        ((5,), (4, 1)),
        ((3, 2), (2, 2, 1)),
        ((2, 1, 1, 1), (1, 1, 1, 1, 1)),
    )
    bases, cells, _, _, _ = augmented_common_core_cech_data(
        (3, 2),
        labels,
        (0, 3, 5, 6),
    )
    return audit_hierarchical_cokernel_resolution(
        "W5-HIERARCHICAL-COKERNEL-RESOLUTION",
        "physical-wreath-orientation-family",
        tuple(bases[cell] for cell in cells[1]),
    )


def run_hierarchical_cokernel_resolution() -> (
    HierarchicalCokernelResolutionReport
):
    controls = [*_abstract_controls(), _physical_control()]
    counterfamily = [
        conditioning_counter_record(1 << exponent)
        for exponent in range(1, 21)
    ]
    failures = sum(not row.exact_hierarchical_cokernel_audit for row in controls)
    emergent = [row for row in controls if row.original_pair_emergent_h0_dimension]
    tail = counterfamily[-1]
    verified = failures == 0
    metrics: dict[str, int | float] = {
        "exact_hierarchical_cokernel_decomposition_theorem_count": int(verified),
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "emergent_h0_control_count": len(emergent),
        "emergent_h0_resolved_control_count": sum(
            row.hierarchical_relations_exhaust_root_kernel for row in emergent
        ),
        "physical_control_count": sum(
            row.control_family.startswith("physical") for row in controls
        ),
        "conditioning_counterfamily_row_count": len(counterfamily),
        "tail_counterfamily_child_width": tail.child_width,
        "tail_counterfamily_endpoint_gap": tail.minimum_endpoint_gap,
        "tail_counterfamily_inverse_gap_cost": tail.inverse_gap_cost,
        "natural_child_frame_comparability_theorem_count": 0,
        "coherent_hierarchical_kernel_transform_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return HierarchicalCokernelResolutionReport(
        created_at=utc_now(),
        theorem_contract={
            "orthogonal_kernel_recursion": (
                "ker[S_L S_R]=ker S_L direct_sum ker S_R direct_sum "
                "{S_L^+x direct_sum -S_R^+x:x in range(S_L) intersection range(S_R)}."
            ),
            "hierarchical_completeness": (
                "Recursing the parent relation construction spans the full leaf "
                "synthesis kernel for every finite subspace family."
            ),
            "parent_metric": "M=X^*(F_L^+ + F_R^+)X on the common child span.",
            "parent_grading": "J=X^*(F_L^+ - F_R^+)X on the common child span.",
            "scope": (
                "Completeness is information-theoretic. No natural asymptotic "
                "comparability, coherent pseudoinverse-frame transform, or "
                "polynomial endpoint-gap theorem is supplied."
            ),
        },
        controls=controls,
        conditioning_counterfamily=counterfamily,
        proof_obligations=[
            {
                "obligation": "resolve_augmented_h0_information_theoretically",
                "resolved": verified,
                "resolution": (
                    "Every emergent leaf dependency appears as an intersection "
                    "of recursively formed child spans and is lifted by child "
                    "pseudoinverses."
                ),
            },
            {
                "obligation": "prove_natural_child_frame_pseudoinverse_comparability",
                "resolved": False,
                "resolution": (
                    "The exact gap is governed by F_L^+ versus F_R^+ on their "
                    "common span. Generic complete hierarchies can have gap 1/(p+1)."
                ),
            },
            {
                "obligation": "compile_hierarchical_cokernel_transform_coherently",
                "resolved": False,
                "resolution": (
                    "No efficient controlled construction of child supports, "
                    "common-span bases, or pseudoinverse preimages is known."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Nonzero direct augmented H0 kills hierarchical polar sampling.",
                "resolved": True,
                "resolution": (
                    "The three-lines control has direct H0=1 but the root child "
                    "spans intersect in exactly one dimension, resolving it."
                ),
            },
            {
                "objection": "Exact hierarchical cokernel completeness implies a constant gap.",
                "resolved": True,
                "resolution": (
                    "The repeated-line counterfamily is complete but has endpoint "
                    "gap 1/(p+1)."
                ),
            },
            {
                "objection": "A parent relation is determined only by support projectors.",
                "resolved": True,
                "resolution": (
                    "Its metric depends on the full pseudoinverse frames F_L^+ "
                    "and F_R^+, not merely their common support."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "direct_pair_common_cech_complete": False,
            "hierarchical_span_relations_exhaust_full_cokernel": verified,
            "augmented_h0_is_information_theoretic_no_go": False,
            "natural_child_pseudoinverse_frames_comparable": False,
            "natural_hierarchical_endpoint_gap_proved": False,
            "coherent_hierarchical_cokernel_transform_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Hierarchical span relations are exactly complete, but their "
                "graded conditioning is controlled by unproved natural "
                "pseudoinverse-frame comparability and no coherent transform exists."
            ),
        },
        status=(
            "hierarchical-cokernel-complete-frame-comparability-open"
            if verified
            else "hierarchical-cokernel-control-failure"
        ),
        summary=(
            "Resolved augmented H0 exactly by recursive child-span relations "
            "and isolated child pseudoinverse-frame comparability as the true "
            "endpoint-gap gate."
        ),
        falsifiers_triggered=[
            "Direct pair-common incompleteness is not a no-go for hierarchical span relations.",
            "Exact hierarchical relation completeness does not imply efficient conditioning.",
            "Support topology alone cannot determine parent endpoint weights.",
        ],
    )


def write_hierarchical_cokernel_resolution_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_hierarchical_cokernel_resolution())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_hierarchical_cokernel_resolution": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_hierarchical_cokernel_resolution_report()
    print(json.dumps(report, indent=2))
