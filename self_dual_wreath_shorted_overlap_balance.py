"""Exact shorted-overlap criterion for hierarchical polar balance.

Let ``A,B >= 0``, ``S=A+B``, and

    C = S^(-1/2) A S^(-1/2)

on ``supp(S)``.  Put ``K=ran(A) intersect ran(B)`` and let ``U`` be any
isometry onto ``K``.  The positive-definite range metrics

    G_A = U^* A^+ U,       G_B = U^* B^+ U

contain exactly the nontrivial generalized spectrum of the merge:

    spec(C) intersect (0,1)
      = spec(G_B, G_A+G_B).                                  (1)

Indeed, ``Cz=lambda z`` is equivalent to
``A x=lambda(A+B)x`` for ``x=S^(-1/2)z``.  Then
``y=(A+B)x`` lies in ``K`` and its coordinates obey

    lambda G_A y = (1-lambda) G_B y.

Conversely, equality of the two minimum-norm preimages modulo
``ker(A)+ker(B)=K^perp`` reconstructs ``x``.  Thus (1) is bijective and
recovers the known fractional-rank/intersection identity.

The shorted operators of ``A`` and ``B`` to ``K`` are

    A_K = U G_A^(-1) U^*,   B_K = U G_B^(-1) U^*.

Consequently every fractional channel is exactly balanced at ``1/2`` iff

    G_A=G_B, equivalently A_K=B_K.                            (2)

This criterion is strictly more general than reducing affine cores.  Genuine
label-distinct ``W_3`` orientation frames have emergent, nonreducing child
intersections while satisfying (2) exactly.  Repeated labels violate (2) and
produce ``1/3,4/9,5/9,2/3`` channels.  The all-n research target is therefore
not affine-core exhaustion; it is a representation-theoretic proof (or
counterexample) of shorted-metric equality for natural collision-free affine
splits, together with coherent access to the intersection and its metric.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import eigh

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_level_three_flag_audit import (
    _reduced_projector_family,
    flag_leaf_order,
    ordered_f2_three_bases,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_shorted_overlap_balance.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SHORTED-OVERLAP-BALANCE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ShortedOverlapNodeRecord:
    node_id: str
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    child_width: int
    left_rank: int
    right_rank: int
    parent_rank: int
    child_range_intersection_dimension: int
    fractional_relative_eigenvalue_count: int
    actual_fractional_eigenvalues: tuple[float, ...]
    metric_predicted_fractional_eigenvalues: tuple[float, ...]
    maximum_metric_spectrum_residual: float
    compressed_pseudoinverse_metric_balance_residual: float
    shorted_operator_balance_residual: float
    maximum_fractional_half_residual: float
    maximum_leaf_reduction_leakage: float
    pairwise_common_span_dimension: int | None
    emergent_intersection_dimension: int | None
    exact_shorted_overlap_spectrum_verified: bool
    balanced_shorted_overlap: bool
    reducing_core_exhaustion_falsified_at_node: bool
    status: str


@dataclass(frozen=True)
class WreathShortedOverlapControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    globally_distinct_source_partitions: bool
    pairwise_distinct_physical_labels: bool
    carrier_dimension: int
    reduced_support_dimension: int
    unique_affine_merge_count: int
    fractional_merge_count: int
    balanced_fractional_merge_count: int
    unbalanced_fractional_merge_count: int
    nonreducing_fractional_merge_count: int
    pairwise_audited_fractional_merge_count: int
    emergent_fractional_merge_count: int
    maximum_metric_spectrum_residual: float
    maximum_balanced_metric_residual: float
    observed_fractional_eigenvalues: tuple[float, ...]
    exact_shorted_overlap_theorem_verified: bool
    all_fractional_merges_balanced: bool
    reducing_affine_core_exhaustion_falsified: bool
    node_records: list[ShortedOverlapNodeRecord]
    status: str


@dataclass(frozen=True)
class ShortedOverlapScalingRecord:
    n: int
    information_threshold_copy_count: int
    affine_tree_depth: int
    exact_shorted_overlap_criterion_available: bool
    collision_free_shorted_metric_equality_proved_all_n: bool
    coherent_child_intersection_transform_proved: bool
    coherent_compressed_metric_transform_proved: bool
    hierarchical_orientation_polar_proved: bool
    status: str


@dataclass(frozen=True)
class ShortedOverlapBalanceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    generic_controls: list[ShortedOverlapNodeRecord]
    wreath_controls: list[WreathShortedOverlapControl]
    scaling_records: list[ShortedOverlapScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    return eigenvectors[:, eigenvalues > tolerance]


def _psd_pseudoinverse(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = eigenvalues > tolerance
    if not np.any(positive):
        return np.zeros_like(matrix)
    return (
        eigenvectors[:, positive]
        * (1.0 / eigenvalues[positive])
    ) @ eigenvectors[:, positive].conj().T


def _range_intersection_basis(
    left_basis: np.ndarray,
    right_basis: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    dimension = left_basis.shape[0]
    if not left_basis.shape[1] or not right_basis.shape[1]:
        return np.zeros((dimension, 0), dtype=complex)
    left_vectors, singular_values, _ = np.linalg.svd(
        left_basis.conj().T @ right_basis,
        full_matrices=False,
    )
    return left_basis @ left_vectors[:, singular_values >= 1 - 10 * tolerance]


def _relative_effect_spectrum(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, int]:
    parent = left + right
    parent_basis = _support_basis(parent, tolerance)
    parent_inverse = _psd_pseudoinverse(parent, tolerance)
    parent_inverse_root_eigenvalues, parent_inverse_root_vectors = np.linalg.eigh(
        (parent_inverse + parent_inverse.conj().T) / 2
    )
    parent_inverse_root = (
        parent_inverse_root_vectors
        * np.sqrt(np.maximum(parent_inverse_root_eigenvalues, 0.0))
    ) @ parent_inverse_root_vectors.conj().T
    effect = parent_inverse_root @ left @ parent_inverse_root
    restricted = parent_basis.conj().T @ effect @ parent_basis
    eigenvalues = np.linalg.eigvalsh((restricted + restricted.conj().T) / 2)
    fractional = eigenvalues[
        (eigenvalues > 10 * tolerance)
        & (eigenvalues < 1 - 10 * tolerance)
    ]
    return fractional, parent_basis.shape[1]


def _span_basis(
    bases: tuple[np.ndarray, ...],
    dimension: int,
    tolerance: float,
) -> np.ndarray:
    active = [basis for basis in bases if basis.shape[1]]
    if not active:
        return np.zeros((dimension, 0), dtype=complex)
    columns = np.concatenate(active, axis=1)
    left, singular_values, _ = np.linalg.svd(columns, full_matrices=False)
    return left[:, singular_values > tolerance]


def audit_shorted_overlap_node(
    node_id: str,
    projectors: tuple[np.ndarray, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    compute_pairwise_generation: bool = False,
    tolerance: float = 1e-8,
) -> ShortedOverlapNodeRecord:
    if not projectors:
        raise ValueError("at least one projector is required")
    if not left_masks or not right_masks or set(left_masks) & set(right_masks):
        raise ValueError("disjoint nonempty children are required")
    if len(left_masks) != len(right_masks):
        raise ValueError("a balanced affine split is required")
    if any(mask < 0 or mask >= len(projectors) for mask in (*left_masks, *right_masks)):
        raise ValueError("orientation mask out of range")

    dimension = len(projectors[0])
    zero = np.zeros((dimension, dimension), dtype=complex)
    left = sum((projectors[mask] for mask in left_masks), zero.copy())
    right = sum((projectors[mask] for mask in right_masks), zero.copy())
    left_basis = _support_basis(left, tolerance)
    right_basis = _support_basis(right, tolerance)
    intersection = _range_intersection_basis(
        left_basis,
        right_basis,
        tolerance,
    )
    intersection_dimension = intersection.shape[1]
    actual, parent_rank = _relative_effect_spectrum(left, right, tolerance)

    if intersection_dimension:
        left_metric = (
            intersection.conj().T
            @ _psd_pseudoinverse(left, tolerance)
            @ intersection
        )
        right_metric = (
            intersection.conj().T
            @ _psd_pseudoinverse(right, tolerance)
            @ intersection
        )
        metric_sum = left_metric + right_metric
        predicted = eigh(
            right_metric,
            metric_sum,
            eigvals_only=True,
            check_finite=True,
        )
        left_shorted = (
            intersection
            @ np.linalg.inv(left_metric)
            @ intersection.conj().T
        )
        right_shorted = (
            intersection
            @ np.linalg.inv(right_metric)
            @ intersection.conj().T
        )
        metric_balance = float(
            np.linalg.norm(left_metric - right_metric, ord=2)
        )
        shorted_balance = float(
            np.linalg.norm(left_shorted - right_shorted, ord=2)
        )
        intersection_projector = intersection @ intersection.conj().T
        complement = np.eye(dimension) - intersection_projector
        reduction_leakage = max(
            float(
                np.linalg.norm(
                    complement @ projectors[mask] @ intersection,
                    ord=2,
                )
            )
            for mask in (*left_masks, *right_masks)
        )
    else:
        predicted = np.asarray([], dtype=float)
        metric_balance = 0.0
        shorted_balance = 0.0
        reduction_leakage = 0.0

    if len(actual) == len(predicted):
        spectrum_residual = max(
            (
                abs(float(left_value) - float(right_value))
                for left_value, right_value in zip(
                    np.sort(actual),
                    np.sort(predicted),
                )
            ),
            default=0.0,
        )
    else:
        spectrum_residual = float("inf")

    pairwise_dimension: int | None = None
    emergent_dimension: int | None = None
    if compute_pairwise_generation:
        leaf_bases = {
            mask: _support_basis(projectors[mask], tolerance)
            for mask in (*left_masks, *right_masks)
        }
        pairwise_bases = tuple(
            _range_intersection_basis(
                leaf_bases[left_mask],
                leaf_bases[right_mask],
                tolerance,
            )
            for left_mask in left_masks
            for right_mask in right_masks
        )
        pairwise_span = _span_basis(pairwise_bases, dimension, tolerance)
        pairwise_dimension = pairwise_span.shape[1]
        if pairwise_dimension and intersection_dimension:
            contained_rank = np.linalg.matrix_rank(
                intersection.conj().T @ pairwise_span,
                tol=100 * tolerance,
            )
        else:
            contained_rank = 0
        emergent_dimension = intersection_dimension - int(contained_rank)

    half_residual = max(
        (abs(float(value) - 0.5) for value in actual),
        default=0.0,
    )
    theorem_verified = bool(
        len(actual) == intersection_dimension
        and spectrum_residual <= 100 * tolerance
    )
    balanced = bool(
        intersection_dimension
        and half_residual <= 100 * tolerance
        and metric_balance <= 100 * tolerance
        and shorted_balance <= 100 * tolerance
    )
    exhaustion_falsified = bool(
        intersection_dimension and reduction_leakage > 100 * tolerance
    )
    return ShortedOverlapNodeRecord(
        node_id=node_id,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        child_width=len(left_masks),
        left_rank=left_basis.shape[1],
        right_rank=right_basis.shape[1],
        parent_rank=parent_rank,
        child_range_intersection_dimension=intersection_dimension,
        fractional_relative_eigenvalue_count=len(actual),
        actual_fractional_eigenvalues=tuple(
            round(float(value), 10) for value in np.sort(actual)
        ),
        metric_predicted_fractional_eigenvalues=tuple(
            round(float(value), 10) for value in np.sort(predicted)
        ),
        maximum_metric_spectrum_residual=spectrum_residual,
        compressed_pseudoinverse_metric_balance_residual=metric_balance,
        shorted_operator_balance_residual=shorted_balance,
        maximum_fractional_half_residual=half_residual,
        maximum_leaf_reduction_leakage=reduction_leakage,
        pairwise_common_span_dimension=pairwise_dimension,
        emergent_intersection_dimension=emergent_dimension,
        exact_shorted_overlap_spectrum_verified=theorem_verified,
        balanced_shorted_overlap=balanced,
        reducing_core_exhaustion_falsified_at_node=exhaustion_falsified,
        status=(
            "exact-balanced-shorted-overlap-nonreducing"
            if theorem_verified and balanced and exhaustion_falsified
            else "exact-balanced-shorted-overlap"
            if theorem_verified and balanced
            else "exact-unbalanced-shorted-overlap"
            if theorem_verified and intersection_dimension
            else "exact-no-fractional-overlap"
            if theorem_verified
            else "shorted-overlap-validation-failure"
        ),
    )


def unique_affine_flag_merges() -> tuple[
    tuple[tuple[int, ...], tuple[int, ...]], ...
]:
    merges: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for basis in ordered_f2_three_bases():
        level = [(orientation,) for orientation in flag_leaf_order(basis)]
        for _ in range(3):
            next_level = []
            for index in range(0, len(level), 2):
                children = tuple(sorted((level[index], level[index + 1])))
                merges.add(children)
                next_level.append(tuple(sorted(children[0] + children[1])))
            level = next_level
    return tuple(sorted(merges, key=lambda row: (len(row[0]), row)))


def audit_wreath_shorted_overlap(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    *,
    compute_pairwise_generation: bool,
    tolerance: float = 1e-8,
) -> WreathShortedOverlapControl:
    projectors, carrier_dimension, support_dimension = _reduced_projector_family(
        target,
        labels,
        tolerance,
    )
    records = [
        audit_shorted_overlap_node(
            f"{control_id}-W{len(left)}-{'-'.join(map(str, left))}-{'-'.join(map(str, right))}",
            projectors,
            left,
            right,
            compute_pairwise_generation=compute_pairwise_generation,
            tolerance=tolerance,
        )
        for left, right in unique_affine_flag_merges()
    ]
    fractional = [
        row for row in records if row.child_range_intersection_dimension > 0
    ]
    balanced = [row for row in fractional if row.balanced_shorted_overlap]
    unbalanced = [row for row in fractional if not row.balanced_shorted_overlap]
    nonreducing = [
        row
        for row in fractional
        if row.reducing_core_exhaustion_falsified_at_node
    ]
    pairwise_audited = [
        row for row in fractional if row.emergent_intersection_dimension is not None
    ]
    emergent = [
        row
        for row in pairwise_audited
        if (row.emergent_intersection_dimension or 0) > 0
    ]
    source = tuple(partition for label in labels for partition in label)
    verified = all(row.exact_shorted_overlap_spectrum_verified for row in records)
    observed = tuple(
        sorted(
            {
                value
                for row in fractional
                for value in row.actual_fractional_eigenvalues
            }
        )
    )
    return WreathShortedOverlapControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        globally_distinct_source_partitions=len(source) == len(set(source)),
        pairwise_distinct_physical_labels=len(labels) == len(set(labels)),
        carrier_dimension=carrier_dimension,
        reduced_support_dimension=support_dimension,
        unique_affine_merge_count=len(records),
        fractional_merge_count=len(fractional),
        balanced_fractional_merge_count=len(balanced),
        unbalanced_fractional_merge_count=len(unbalanced),
        nonreducing_fractional_merge_count=len(nonreducing),
        pairwise_audited_fractional_merge_count=len(pairwise_audited),
        emergent_fractional_merge_count=len(emergent),
        maximum_metric_spectrum_residual=max(
            (row.maximum_metric_spectrum_residual for row in records),
            default=0.0,
        ),
        maximum_balanced_metric_residual=max(
            (
                row.compressed_pseudoinverse_metric_balance_residual
                for row in balanced
            ),
            default=0.0,
        ),
        observed_fractional_eigenvalues=observed,
        exact_shorted_overlap_theorem_verified=verified,
        all_fractional_merges_balanced=bool(fractional) and not unbalanced,
        reducing_affine_core_exhaustion_falsified=bool(nonreducing),
        node_records=fractional,
        status=(
            "all-affine-merges-shorted-balanced-affine-exhaustion-false"
            if verified and fractional and not unbalanced and nonreducing
            else "all-affine-merges-shorted-balanced"
            if verified and fractional and not unbalanced
            else "unbalanced-shorted-overlap-counterexample"
            if verified and unbalanced
            else "shorted-overlap-control-validation-failure"
            if not verified
            else "no-fractional-overlap"
        ),
    )


def shorted_overlap_scaling_record(n: int) -> ShortedOverlapScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copy_count = math.ceil(math.lgamma(n + 1) / math.log(2))
    return ShortedOverlapScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        affine_tree_depth=copy_count,
        exact_shorted_overlap_criterion_available=True,
        collision_free_shorted_metric_equality_proved_all_n=False,
        coherent_child_intersection_transform_proved=False,
        coherent_compressed_metric_transform_proved=False,
        hierarchical_orientation_polar_proved=False,
        status="exact-balance-criterion-all-n-wreath-proof-open",
    )


def _generic_controls() -> list[ShortedOverlapNodeRecord]:
    identity = np.eye(2)
    unequal_left = np.diag((2.0, 1.0))
    unequal_right = np.diag((1.0, 2.0))
    return [
        audit_shorted_overlap_node(
            "generic-equal-positive-frames",
            (identity, identity),
            (0,),
            (1,),
        ),
        audit_shorted_overlap_node(
            "generic-unequal-positive-frames",
            (unequal_left, unequal_right),
            (0,),
            (1,),
        ),
    ]


def run_shorted_overlap_balance() -> ShortedOverlapBalanceReport:
    distinct_triangle: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    repeated: tuple[Label, ...] = (((3,), (2, 1)),) * 3
    w5_labels = _w5_probe_labels()[0]
    controls = [
        audit_wreath_shorted_overlap(
            "W3-DISTINCT-LABEL-TRIANGLE",
            3,
            (2, 1),
            distinct_triangle,
            compute_pairwise_generation=True,
        ),
        audit_wreath_shorted_overlap(
            "W3-REPEATED-LABEL-FALSIFIER",
            3,
            (2, 1),
            repeated,
            compute_pairwise_generation=True,
        ),
        audit_wreath_shorted_overlap(
            "W5-COLLISION-FREE-3-2",
            5,
            (3, 2),
            w5_labels,
            compute_pairwise_generation=False,
        ),
    ]
    generic = _generic_controls()
    scaling = [
        shorted_overlap_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    theorem_failures = sum(
        not row.exact_shorted_overlap_theorem_verified for row in controls
    ) + sum(not row.exact_shorted_overlap_spectrum_verified for row in generic)
    label_simple = [
        row
        for row in controls
        if row.pairwise_distinct_physical_labels
    ]
    repeated_controls = [
        row
        for row in controls
        if not row.pairwise_distinct_physical_labels
    ]
    finite_label_simple_balance = bool(label_simple) and all(
        row.all_fractional_merges_balanced for row in label_simple
    )
    repeated_falsifier = any(
        row.unbalanced_fractional_merge_count > 0 for row in repeated_controls
    )
    affine_exhaustion_falsified = any(
        row.reducing_affine_core_exhaustion_falsified
        and row.all_fractional_merges_balanced
        for row in label_simple
    )
    emergent_balanced = any(
        row.emergent_fractional_merge_count > 0
        and row.all_fractional_merges_balanced
        for row in label_simple
    )
    verified = theorem_failures == 0
    return ShortedOverlapBalanceReport(
        created_at=utc_now(),
        theorem_contract={
            "fractional_metric_pencil": (
                "For K=ran(A) intersect ran(B), the fractional spectrum of "
                "S^-1/2 A S^-1/2 equals the generalized spectrum of "
                "(G_B,G_A+G_B), where G_A=U^*A^+U and G_B=U^*B^+U."
            ),
            "balance_if_and_only_if": (
                "Every fractional eigenvalue is 1/2 iff G_A=G_B, equivalently "
                "the shorted operators of A and B to K are equal."
            ),
            "affine_core_scope": (
                "Reducing affine-incidence cores imply shorted equality, but "
                "are not necessary: label-distinct W3 has balanced emergent "
                "nonreducing intersections."
            ),
            "new_all_n_target": (
                "Prove or falsify equality of the two compressed pseudoinverse "
                "metrics for every natural collision-free affine split."
            ),
            "constructive_boundary": (
                "An equality theorem still requires coherent transforms for "
                "the child intersection and its compressed range metric."
            ),
        },
        generic_controls=generic,
        wreath_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "shorted_overlap_fractional_spectrum_theorem",
                "resolved": verified,
                "resolution": (
                    "The generalized eigenvector/preimage argument is exact; "
                    "all finite controls reproduce every fractional eigenvalue."
                ),
            },
            {
                "obligation": "affine_core_exhaustion_as_required_mechanism",
                "resolved": True,
                "resolution": (
                    "Falsified as a necessity: balanced label-distinct W3 "
                    "intersections are emergent and do not reduce the leaves."
                ),
            },
            {
                "obligation": "collision_free_shorted_metric_equality_all_n",
                "resolved": False,
                "resolution": (
                    "Finite W3/W5 controls satisfy equality. No representation-"
                    "theoretic proof covers growing copy count or all sectors."
                ),
            },
            {
                "obligation": "coherent_shorted_metric_sampler",
                "resolved": False,
                "resolution": (
                    "Neither the child-intersection transform nor a coherent "
                    "compressed pseudoinverse metric transform is compiled."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Half-integrality follows from affine membership cores.",
                "resolved": True,
                "resolution": (
                    "That route is insufficient: genuine balanced controls have "
                    "nonreducing and pairwise-emergent intersections."
                ),
            },
            {
                "objection": "Balanced child cardinality forces shorted equality.",
                "resolved": True,
                "resolution": (
                    "Repeated labels use the same balanced affine splits but "
                    "violate metric equality and produce nonhalf channels."
                ),
            },
            {
                "objection": "The exact criterion already provides a circuit.",
                "resolved": False,
                "resolution": (
                    "The criterion contains pseudoinverses and an implicit "
                    "intersection basis; using it directly would be circular."
                ),
            },
            {
                "objection": "Finite equality is evidence of an asymptotic theorem.",
                "resolved": False,
                "resolution": (
                    "The control set is too small and representation collisions "
                    "may appear at growing depth. The all-n gate remains closed."
                ),
            },
        ],
        headline_metrics={
            "shorted_overlap_fractional_spectrum_theorem_count": int(verified),
            "shorted_balance_if_and_only_if_theorem_count": int(verified),
            "finite_control_count": len(generic) + len(controls),
            "finite_validation_failure_count": theorem_failures,
            "label_simple_wreath_control_count": len(label_simple),
            "label_simple_unbalanced_merge_count": sum(
                row.unbalanced_fractional_merge_count for row in label_simple
            ),
            "repeated_label_unbalanced_merge_count": sum(
                row.unbalanced_fractional_merge_count for row in repeated_controls
            ),
            "balanced_nonreducing_merge_count": sum(
                row.nonreducing_fractional_merge_count
                for row in label_simple
                if row.all_fractional_merges_balanced
            ),
            "balanced_emergent_merge_count": sum(
                row.emergent_fractional_merge_count
                for row in label_simple
                if row.all_fractional_merges_balanced
            ),
            "affine_core_exhaustion_necessity_falsifier_count": int(
                affine_exhaustion_falsified
            ),
            "collision_free_shorted_metric_all_n_theorem_count": 0,
            "coherent_shorted_metric_sampler_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_shorted_overlap_criterion_proved": verified,
            "affine_core_exhaustion_required": False,
            "affine_core_exhaustion_necessity_falsified": (
                affine_exhaustion_falsified
            ),
            "finite_label_simple_shorted_balance_observed": (
                finite_label_simple_balance
            ),
            "finite_emergent_shorted_balance_observed": emergent_balanced,
            "repeated_labels_falsify_universal_balance": repeated_falsifier,
            "collision_free_shorted_metric_equality_proved_all_n": False,
            "coherent_child_intersection_transform_proved": False,
            "coherent_compressed_metric_transform_proved": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Shorted-metric equality is now the exact half-balance target, "
                "but its all-n wreath proof and coherent implementation are open."
            ),
        },
        status=(
            "exact-shorted-balance-criterion-all-n-wreath-proof-open"
            if verified and finite_label_simple_balance and repeated_falsifier
            else "shorted-overlap-theorem-validation-failure"
        ),
        summary=(
            "Replaced affine-core exhaustion with an exact pseudoinverse-metric "
            "criterion, verified balanced emergent intersections on label-simple "
            "controls, and localized repeated-label failure to metric imbalance."
        ),
        falsifiers_triggered=[
            (
                "Reducing affine-core exhaustion is not necessary for exact "
                "half-integral relative spectra."
            ),
            (
                "Balanced affine child sizes do not force equal shorted metrics."
            ),
            (
                "A finite exact balance pattern does not prove an all-n metric "
                "identity or supply coherent metric access."
            ),
        ],
    )


def write_shorted_overlap_balance_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SHORTED-OVERLAP-BALANCE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_shorted_overlap_balance())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_shorted_overlap_balance_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
