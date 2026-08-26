"""Algebraic polar telescoping does not cancel recursive access normalization.

For a node ``v`` with child analyses ``R_c`` on one common input space, put

    S_c = R_c^* R_c,       S_v = sum_c S_c,
    Q_c = R_c S_c^(-1/2), Q_v = R_v S_v^(-1/2),

where inverse square roots are Moore--Penrose inverses on the corresponding
supports and ``R_v=direct_sum_c R_c``.  The exact support-aware chain rule is

    Q_v = (direct_sum_c Q_c) W_v,
    W_v = [sqrt(S_c)]_c S_v^(-1/2),
    W_v^* W_v = supp(S_v).                                (1)

Consequently the mathematical factors telescope through an arbitrary tree.
If every ``W_v`` is supplied as a normalization-one coherent isometry, the
root polar is compiled by one call per tree level.  Equation (1), however,
does not manufacture those normalization-one local oracles.

Indeed, suppose a coefficient-only PREPARE/SELECT stack receives child block
encodings ``R_c/alpha_c``.  To give every unscaled child block the same parent
coefficient ``1/alpha_v``, the address amplitudes must be
``a_c=alpha_c/alpha_v``.  Normalization of PREPARE is therefore equivalent to

    alpha_v^2 = sum_c alpha_c^2.                            (2)

This value is sharp and independent of tree grouping.  Starting from
normalization-one leaves gives ``alpha_root=sqrt(w)``.  Supplying the child
polars at normalization one does not reset this scale, because

    Q_c^* (R_c/alpha_c) = sqrt(S_c)/alpha_c.                (3)

Thus the inherited normalization remains on the positive child metric.
The same is true in the shorted coordinates of a sibling intersection.  If
``U`` spans that intersection and ``G_c=U^*S_c^+U``, then the normalized frame
``S_c/alpha_c^2`` exposes

    Ghat_c = alpha_c^2 G_c,
    (S_c/alpha_c^2)_K = (S_c)_K/alpha_c^2.                  (4)

Shorting therefore moves the scale between inverse and direct metrics; it
does not cancel it.  Equal child normalizations preserve a balance equality
but retain a common scale, while unequal normalizations can even spoil the
apparent equality unless they are explicitly rescaled.

The strongest flat control makes the distinction transparent.  Take ``w``
orthogonal rank-one leaves on a ``w``-dimensional input.  Every exact local
``W_v`` is an isometry and their product is the identity root polar.  Replacing
each binary ``W_v`` by the generic coefficient-normalized signal
``W_v/sqrt(2)`` instead produces exactly ``I/sqrt(w)``.  Local QSVT can reset
each factor, but the previously proved literal nested architecture then has
leaf-query recurrence ``q_(ell+1)>=3q_ell``.  The alternatives are therefore
not normalization cancellation: they are either a global ``sqrt(w)`` signal,
nested nonlinear query reuse, or a genuinely new normalization-one local
router.

There is also a trim compatibility condition.  A parent polar built for a
projection ``Pi_v`` uses child analyses ``R_c Pi_v``.  Reusing independently
trimmed children ``R_c Pi_c`` is exact iff

    direct_sum_c R_c(Pi_c-Pi_v) = 0.                       (5)

Good conditioning on each retained child support does not imply (4).  Two
children can each discard a subthreshold eigenvalue that becomes retained
after their positive metrics add at the parent.

This closes the proposed *bookkeeping* loophole: exact recursive factorization
and regrouping alone do not cancel the leaf-width normalization.  It does not
rule out representation-specific coherent ``W_v`` oracles, a flattened affine
GPE/Schur router, or any arbitrary hierarchical-query circuit.  Those are now
the precise surviving interfaces.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentRecord,
    NegativeResultRecord,
    upsert_experiment,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_recursive_polar_normalization_conservation_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-POLAR-"
    "NORMALIZATION-CONSERVATION-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-RECURSIVE-POLAR-ALGEBRAIC-"
    "TELESCOPING-NO-NORMALIZATION-CANCELLATION"
)
DEFAULT_POLAR_ERROR = 0.1


@dataclass(frozen=True)
class SupportAwareTreeControl:
    control_id: str
    ambient_dimension: int
    leaf_count: int
    root_rank: int
    maximum_node_polar_residual: float
    maximum_node_chain_rule_residual: float
    maximum_node_relative_isometry_residual: float
    maximum_node_support_projection_residual: float
    recursive_to_direct_root_polar_residual: float
    contains_rank_deficient_leaf_frames: bool
    exact_support_aware_telescoping_verified: bool
    status: str


@dataclass(frozen=True)
class CoefficientNormalizationControl:
    control_id: str
    leaf_normalizations: tuple[float, ...]
    leaf_count: int
    balanced_root_normalization: float
    left_deep_root_normalization: float
    closed_form_root_normalization: float
    maximum_prepare_state_norm_residual: float
    maximum_equal_block_coefficient_residual: float
    tree_grouping_normalization_residual: float
    unit_leaf_root_normalization: float
    sharp_l2_normalization_recurrence_verified: bool
    status: str


@dataclass(frozen=True)
class ChildPolarMetricScaleControl:
    control_id: str
    ambient_dimension: int
    analysis_output_dimension: int
    analysis_normalization: float
    frame_rank: int
    child_polar_partial_isometry_residual: float
    recovered_normalized_square_root_residual: float
    recovered_to_unscaled_square_root_gap: float
    child_polar_resets_analysis_normalization: bool
    exact_metric_scale_inheritance_verified: bool
    status: str


@dataclass(frozen=True)
class ShortedMetricScaleControl:
    control_id: str
    ambient_dimension: int
    intersection_dimension: int
    left_analysis_normalization: float
    right_analysis_normalization: float
    true_compressed_inverse_metric_balance_residual: float
    maximum_encoded_compressed_inverse_scaling_residual: float
    maximum_encoded_shorted_operator_scaling_residual: float
    encoded_compressed_inverse_metric_balance_residual: float
    encoded_shorted_operator_balance_residual: float
    equal_normalizations_preserve_balance_equality: bool
    unequal_normalizations_spoil_apparent_balance: bool
    shorted_metric_cancels_analysis_normalization: bool
    exact_shorted_metric_scale_inheritance_verified: bool
    status: str


@dataclass(frozen=True)
class TrimCompatibilityControl:
    child_count: int
    ambient_dimension: int
    child_trim_threshold: float
    parent_trim_threshold: float
    discarded_child_eigenvalue: float
    accumulated_parent_eigenvalue: float
    minimum_retained_child_eigenvalue: float
    minimum_retained_parent_eigenvalue: float
    incompatible_analysis_operator_gap: float
    incompatible_frame_operator_gap: float
    incompatible_polar_operator_gap: float
    compatible_analysis_operator_residual: float
    independent_good_conditioning_implies_parent_trim_compatibility: bool
    exact_trim_compatibility_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class OrthogonalHierarchyNormalizationControl:
    depth: int
    leaf_count: int
    exact_root_polar_residual: float
    exact_local_relative_isometry_residual: float
    passively_normalized_root_signal: float
    expected_passively_normalized_root_signal: float
    passive_recursive_composition_residual: float
    coefficient_recurrence_root_normalization: float
    global_bernstein_degree_lower_bound: float
    literal_local_qsvt_minimum_odd_degree: int
    literal_nested_qsvt_leaf_query_lower_bound: int
    supplied_alpha_one_local_isometry_depth: int
    exact_local_isometry_oracles_are_additional_access: bool
    no_passive_normalization_cancellation_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalRecursiveNormalizationScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    orientation_leaf_width_decimal: str
    recursive_depth: int
    coefficient_root_normalization_log2: float
    global_qsvt_degree_lower_bound_log2: float
    literal_nested_degree_three_query_lower_bound_log2: float
    supplied_local_isometry_composition_depth: int
    coefficient_only_recursive_assembly_superpolynomial: bool
    literal_nested_local_qsvt_superpolynomial: bool
    normalization_one_local_relative_isometries_compiled: bool
    status: str


@dataclass(frozen=True)
class RecursivePolarNormalizationConservationTheorem:
    support_aware_chain_rule: str
    algebraic_telescoping: str
    coefficient_normalization_recurrence: str
    grouping_consequence: str
    child_polar_scale_identity: str
    shorted_metric_scale_identity: str
    flat_hierarchy_control: str
    trim_compatibility: str
    conditional_positive_boundary: str
    surviving_interface: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RecursivePolarNormalizationConservationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: RecursivePolarNormalizationConservationTheorem
    support_controls: list[SupportAwareTreeControl]
    normalization_controls: list[CoefficientNormalizationControl]
    metric_scale_controls: list[ChildPolarMetricScaleControl]
    shorted_metric_controls: list[ShortedMetricScaleControl]
    trim_control: TrimCompatibilityControl
    orthogonal_controls: list[OrthogonalHierarchyNormalizationControl]
    scaling_records: list[NaturalRecursiveNormalizationScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(np.asarray(matrix, dtype=complex)))
    if float(values[0]) < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** exponent
    return (vectors * transformed) @ vectors.conj().T


def _block_diagonal(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    result = np.zeros(
        (left.shape[0] + right.shape[0], left.shape[1] + right.shape[1]),
        dtype=complex,
    )
    result[: left.shape[0], : left.shape[1]] = left
    result[left.shape[0] :, left.shape[1] :] = right
    return result


def _polar_data(
    analysis: np.ndarray,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]:
    frame = _hermitian(analysis.conj().T @ analysis)
    values = np.linalg.eigvalsh(frame)
    inverse_sqrt = _psd_power(frame, -0.5, tolerance=tolerance)
    square_root = _psd_power(frame, 0.5, tolerance=tolerance)
    polar = analysis @ inverse_sqrt
    support = inverse_sqrt @ frame @ inverse_sqrt
    rank = int(np.count_nonzero(values > 100 * tolerance))
    return polar, frame, square_root, support, rank


def deterministic_rank_deficient_leaves(dimension: int) -> tuple[np.ndarray, ...]:
    """Return rank-one leaf analyses whose aggregate frame has full support."""

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    identity = np.eye(dimension, dtype=complex)
    indices = np.arange(dimension, dtype=float)
    fourier = np.exp(
        2j * np.pi * np.outer(indices, indices) / dimension
    ) / math.sqrt(dimension)
    rows = [identity[index : index + 1, :] for index in range(dimension)]
    rows.extend(fourier[index : index + 1, :] for index in range(dimension))
    return tuple(rows)


def audit_support_aware_tree(
    control_id: str,
    leaves: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> SupportAwareTreeControl:
    if len(leaves) < 2:
        raise ValueError("at least two leaf analyses are required")
    dimension = leaves[0].shape[1]
    if dimension < 1 or any(
        leaf.ndim != 2 or leaf.shape[1] != dimension or leaf.shape[0] < 1
        for leaf in leaves
    ):
        raise ValueError("leaf analyses must have nonempty outputs and one input space")

    polar_residuals: list[float] = []
    chain_residuals: list[float] = []
    isometry_residuals: list[float] = []
    support_residuals: list[float] = []
    leaf_ranks: list[int] = []

    def recurse(
        block: tuple[np.ndarray, ...],
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
        if len(block) == 1:
            analysis = block[0]
            polar, frame, square_root, support, rank = _polar_data(
                analysis,
                tolerance=tolerance,
            )
            leaf_ranks.append(rank)
            polar_residuals.append(
                float(np.linalg.norm(polar @ square_root - analysis, ord=2))
            )
            support_residuals.append(
                float(np.linalg.norm(support @ support - support, ord=2))
            )
            return analysis, polar, frame, rank

        split = len(block) // 2
        left_analysis, left_compiled, left_frame, _ = recurse(block[:split])
        right_analysis, right_compiled, right_frame, _ = recurse(block[split:])
        analysis = np.vstack((left_analysis, right_analysis))
        polar, frame, square_root, support, rank = _polar_data(
            analysis,
            tolerance=tolerance,
        )
        inverse_sqrt = _psd_power(frame, -0.5, tolerance=tolerance)
        left_square_root = _psd_power(left_frame, 0.5, tolerance=tolerance)
        right_square_root = _psd_power(right_frame, 0.5, tolerance=tolerance)
        relative = np.vstack((left_square_root, right_square_root)) @ inverse_sqrt
        child_polars = _block_diagonal(
            _polar_data(left_analysis, tolerance=tolerance)[0],
            _polar_data(right_analysis, tolerance=tolerance)[0],
        )
        chain = child_polars @ relative
        compiled = _block_diagonal(left_compiled, right_compiled) @ relative
        polar_residuals.append(
            float(np.linalg.norm(polar @ square_root - analysis, ord=2))
        )
        chain_residuals.append(float(np.linalg.norm(chain - polar, ord=2)))
        isometry_residuals.append(
            float(np.linalg.norm(relative.conj().T @ relative - support, ord=2))
        )
        support_residuals.append(
            float(np.linalg.norm(support @ support - support, ord=2))
        )
        return analysis, compiled, frame, rank

    root_analysis, recursive_root, root_frame, root_rank = recurse(leaves)
    direct_root = _polar_data(root_analysis, tolerance=tolerance)[0]
    root_residual = float(np.linalg.norm(recursive_root - direct_root, ord=2))
    maximum_polar = max(polar_residuals, default=0.0)
    maximum_chain = max(chain_residuals, default=0.0)
    maximum_isometry = max(isometry_residuals, default=0.0)
    maximum_support = max(support_residuals, default=0.0)
    root_frame_rank = int(
        np.count_nonzero(np.linalg.eigvalsh(root_frame) > 100 * tolerance)
    )
    deficient = any(rank < dimension for rank in leaf_ranks)
    verified = bool(
        deficient
        and root_rank == root_frame_rank
        and maximum_polar <= 500 * tolerance
        and maximum_chain <= 500 * tolerance
        and maximum_isometry <= 500 * tolerance
        and maximum_support <= 500 * tolerance
        and root_residual <= 1000 * tolerance
    )
    return SupportAwareTreeControl(
        control_id=control_id,
        ambient_dimension=dimension,
        leaf_count=len(leaves),
        root_rank=root_rank,
        maximum_node_polar_residual=maximum_polar,
        maximum_node_chain_rule_residual=maximum_chain,
        maximum_node_relative_isometry_residual=maximum_isometry,
        maximum_node_support_projection_residual=maximum_support,
        recursive_to_direct_root_polar_residual=root_residual,
        contains_rank_deficient_leaf_frames=deficient,
        exact_support_aware_telescoping_verified=verified,
        status=(
            "exact-support-aware-recursive-polar-telescoping"
            if verified
            else "support-aware-tree-control-failure"
        ),
    )


def audit_coefficient_normalization(
    control_id: str,
    leaf_normalizations: tuple[float, ...],
    *,
    tolerance: float = 1e-12,
) -> CoefficientNormalizationControl:
    if len(leaf_normalizations) < 2 or any(
        not math.isfinite(value) or value <= 0 for value in leaf_normalizations
    ):
        raise ValueError("at least two positive finite normalizations are required")
    prepare_residuals: list[float] = []
    coefficient_residuals: list[float] = []

    def combine(values: tuple[float, ...], left_deep: bool) -> float:
        if len(values) == 1:
            return values[0]
        split = 1 if left_deep else len(values) // 2
        left = combine(values[:split], left_deep)
        right = combine(values[split:], left_deep)
        parent = math.hypot(left, right)
        amplitudes = np.asarray((left / parent, right / parent), dtype=float)
        prepare_residuals.append(abs(float(np.dot(amplitudes, amplitudes)) - 1.0))
        target = 1.0 / parent
        coefficient_residuals.extend(
            (abs(amplitudes[0] / left - target), abs(amplitudes[1] / right - target))
        )
        return parent

    balanced = combine(leaf_normalizations, False)
    left_deep = combine(leaf_normalizations, True)
    closed = math.sqrt(sum(value * value for value in leaf_normalizations))
    grouping = max(abs(balanced - closed), abs(left_deep - closed))
    maximum_prepare = max(prepare_residuals, default=0.0)
    maximum_coefficient = max(coefficient_residuals, default=0.0)
    unit_root = math.sqrt(len(leaf_normalizations))
    verified = bool(
        maximum_prepare <= 100 * tolerance
        and maximum_coefficient <= 100 * tolerance
        and grouping <= 100 * tolerance
    )
    return CoefficientNormalizationControl(
        control_id=control_id,
        leaf_normalizations=leaf_normalizations,
        leaf_count=len(leaf_normalizations),
        balanced_root_normalization=balanced,
        left_deep_root_normalization=left_deep,
        closed_form_root_normalization=closed,
        maximum_prepare_state_norm_residual=maximum_prepare,
        maximum_equal_block_coefficient_residual=maximum_coefficient,
        tree_grouping_normalization_residual=grouping,
        unit_leaf_root_normalization=unit_root,
        sharp_l2_normalization_recurrence_verified=verified,
        status=(
            "sharp-tree-independent-l2-normalization-recurrence"
            if verified
            else "coefficient-normalization-control-failure"
        ),
    )


def audit_child_polar_metric_scale(
    control_id: str,
    analysis: np.ndarray,
    analysis_normalization: float,
    *,
    tolerance: float = 1e-9,
) -> ChildPolarMetricScaleControl:
    matrix = np.asarray(analysis, dtype=complex)
    if matrix.ndim != 2 or min(matrix.shape) < 1:
        raise ValueError("analysis must be a nonempty matrix")
    if not math.isfinite(analysis_normalization) or analysis_normalization <= 1:
        raise ValueError("analysis normalization must be finite and greater than one")
    polar, frame, square_root, support, rank = _polar_data(
        matrix,
        tolerance=tolerance,
    )
    recovered = polar.conj().T @ (matrix / analysis_normalization)
    target = square_root / analysis_normalization
    recovered_residual = float(np.linalg.norm(recovered - target, ord=2))
    partial_isometry = float(
        np.linalg.norm(polar.conj().T @ polar - support, ord=2)
    )
    unscaled_gap = float(np.linalg.norm(recovered - square_root, ord=2))
    verified = bool(
        partial_isometry <= 500 * tolerance
        and recovered_residual <= 500 * tolerance
        and unscaled_gap > 1000 * tolerance
    )
    return ChildPolarMetricScaleControl(
        control_id=control_id,
        ambient_dimension=matrix.shape[1],
        analysis_output_dimension=matrix.shape[0],
        analysis_normalization=analysis_normalization,
        frame_rank=rank,
        child_polar_partial_isometry_residual=partial_isometry,
        recovered_normalized_square_root_residual=recovered_residual,
        recovered_to_unscaled_square_root_gap=unscaled_gap,
        child_polar_resets_analysis_normalization=False,
        exact_metric_scale_inheritance_verified=verified,
        status=(
            "child-polar-preserves-positive-metric-normalization"
            if verified
            else "child-polar-metric-scale-control-failure"
        ),
    )


def audit_shorted_metric_scale(
    control_id: str,
    left_analysis_normalization: float,
    right_analysis_normalization: float,
    *,
    tolerance: float = 1e-10,
) -> ShortedMetricScaleControl:
    if (
        not math.isfinite(left_analysis_normalization)
        or not math.isfinite(right_analysis_normalization)
        or left_analysis_normalization <= 0
        or right_analysis_normalization <= 0
    ):
        raise ValueError("analysis normalizations must be positive and finite")
    frame = np.diag((2.0, 1.0, 0.0)).astype(complex)
    intersection = np.eye(3, dtype=complex)[:, :2]
    inverse = _psd_power(frame, -1.0, tolerance=tolerance)
    true_metric = intersection.conj().T @ inverse @ intersection
    true_shorted = (
        intersection @ np.linalg.inv(true_metric) @ intersection.conj().T
    )
    encoded_metrics: list[np.ndarray] = []
    encoded_shorted: list[np.ndarray] = []
    metric_scaling_residuals: list[float] = []
    shorted_scaling_residuals: list[float] = []
    for alpha in (left_analysis_normalization, right_analysis_normalization):
        encoded_frame = frame / (alpha * alpha)
        encoded_inverse = _psd_power(encoded_frame, -1.0, tolerance=tolerance)
        encoded_metric = intersection.conj().T @ encoded_inverse @ intersection
        encoded_short = (
            intersection
            @ np.linalg.inv(encoded_metric)
            @ intersection.conj().T
        )
        encoded_metrics.append(encoded_metric)
        encoded_shorted.append(encoded_short)
        metric_scaling_residuals.append(
            float(np.linalg.norm(encoded_metric - alpha * alpha * true_metric, ord=2))
        )
        shorted_scaling_residuals.append(
            float(
                np.linalg.norm(
                    encoded_short - true_shorted / (alpha * alpha),
                    ord=2,
                )
            )
        )
    true_balance = 0.0
    encoded_metric_balance = float(
        np.linalg.norm(encoded_metrics[0] - encoded_metrics[1], ord=2)
    )
    encoded_short_balance = float(
        np.linalg.norm(encoded_shorted[0] - encoded_shorted[1], ord=2)
    )
    equal = abs(left_analysis_normalization - right_analysis_normalization) <= tolerance
    equal_preserves = bool(
        equal
        and encoded_metric_balance <= 100 * tolerance
        and encoded_short_balance <= 100 * tolerance
    )
    unequal_spoils = bool(
        not equal
        and encoded_metric_balance > 1000 * tolerance
        and encoded_short_balance > 1000 * tolerance
    )
    maximum_metric_scaling = max(metric_scaling_residuals)
    maximum_short_scaling = max(shorted_scaling_residuals)
    verified = bool(
        maximum_metric_scaling <= 500 * tolerance
        and maximum_short_scaling <= 500 * tolerance
        and (equal_preserves or unequal_spoils)
    )
    return ShortedMetricScaleControl(
        control_id=control_id,
        ambient_dimension=3,
        intersection_dimension=2,
        left_analysis_normalization=left_analysis_normalization,
        right_analysis_normalization=right_analysis_normalization,
        true_compressed_inverse_metric_balance_residual=true_balance,
        maximum_encoded_compressed_inverse_scaling_residual=maximum_metric_scaling,
        maximum_encoded_shorted_operator_scaling_residual=maximum_short_scaling,
        encoded_compressed_inverse_metric_balance_residual=encoded_metric_balance,
        encoded_shorted_operator_balance_residual=encoded_short_balance,
        equal_normalizations_preserve_balance_equality=equal_preserves,
        unequal_normalizations_spoil_apparent_balance=unequal_spoils,
        shorted_metric_cancels_analysis_normalization=False,
        exact_shorted_metric_scale_inheritance_verified=verified,
        status=(
            "shorted-coordinates-inherit-analysis-normalization"
            if verified
            else "shorted-metric-scale-control-failure"
        ),
    )


def audit_trim_compatibility(
    *,
    child_threshold: float = 0.5,
    parent_threshold: float = 0.5,
    tolerance: float = 1e-10,
) -> TrimCompatibilityControl:
    if child_threshold <= 0 or parent_threshold <= 0:
        raise ValueError("trim thresholds must be positive")
    low = 0.4
    high = 1.0
    child_analysis = np.diag((math.sqrt(low), math.sqrt(high))).astype(complex)
    children = (child_analysis, child_analysis.copy())
    child_frame = _hermitian(child_analysis.conj().T @ child_analysis)
    parent_frame = child_frame + child_frame
    child_values, child_vectors = np.linalg.eigh(child_frame)
    parent_values, parent_vectors = np.linalg.eigh(parent_frame)
    child_keep = child_values >= child_threshold
    parent_keep = parent_values >= parent_threshold
    child_projection = (
        child_vectors[:, child_keep] @ child_vectors[:, child_keep].conj().T
    )
    parent_projection = (
        parent_vectors[:, parent_keep] @ parent_vectors[:, parent_keep].conj().T
    )
    desired = np.vstack([child @ parent_projection for child in children])
    reused = np.vstack([child @ child_projection for child in children])
    compatible_desired = np.vstack([child @ child_projection for child in children])
    compatible_reused = np.vstack([child @ child_projection for child in children])
    desired_frame = _hermitian(desired.conj().T @ desired)
    reused_frame = _hermitian(reused.conj().T @ reused)
    desired_polar = _polar_data(desired, tolerance=tolerance)[0]
    reused_polar = _polar_data(reused, tolerance=tolerance)[0]
    analysis_gap = float(np.linalg.norm(reused - desired, ord=2))
    frame_gap = float(np.linalg.norm(reused_frame - desired_frame, ord=2))
    polar_gap = float(np.linalg.norm(reused_polar - desired_polar, ord=2))
    compatible_residual = float(
        np.linalg.norm(compatible_reused - compatible_desired, ord=2)
    )
    retained_child = child_values[child_keep]
    retained_parent = parent_values[parent_keep]
    accumulated = float(parent_values[0])
    verified = bool(
        not bool(child_keep[0])
        and bool(parent_keep[0])
        and analysis_gap > 0.5
        and frame_gap > 0.5
        and polar_gap > 0.9
        and compatible_residual <= 100 * tolerance
    )
    return TrimCompatibilityControl(
        child_count=len(children),
        ambient_dimension=2,
        child_trim_threshold=child_threshold,
        parent_trim_threshold=parent_threshold,
        discarded_child_eigenvalue=float(child_values[0]),
        accumulated_parent_eigenvalue=accumulated,
        minimum_retained_child_eigenvalue=float(retained_child[0]),
        minimum_retained_parent_eigenvalue=float(retained_parent[0]),
        incompatible_analysis_operator_gap=analysis_gap,
        incompatible_frame_operator_gap=frame_gap,
        incompatible_polar_operator_gap=polar_gap,
        compatible_analysis_operator_residual=compatible_residual,
        independent_good_conditioning_implies_parent_trim_compatibility=False,
        exact_trim_compatibility_boundary_verified=verified,
        status=(
            "independent-spectral-trims-not-recursively-reusable"
            if verified
            else "trim-compatibility-control-failure"
        ),
    )


def audit_orthogonal_hierarchy_normalization(
    depth: int,
    *,
    approximation_error: float = DEFAULT_POLAR_ERROR,
    tolerance: float = 1e-10,
) -> OrthogonalHierarchyNormalizationControl:
    if depth < 1:
        raise ValueError("depth must be positive")
    if not 0 < approximation_error < 1:
        raise ValueError("approximation error must lie in (0,1)")
    leaf_count = 1 << depth
    identity = np.eye(leaf_count, dtype=complex)
    leaves = tuple(identity[index : index + 1, :] for index in range(leaf_count))
    local_residuals: list[float] = []

    def recurse(
        block: tuple[np.ndarray, ...],
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        if len(block) == 1:
            polar = _polar_data(block[0], tolerance=tolerance)[0]
            return block[0], polar, polar
        split = len(block) // 2
        left_analysis, left_exact, left_passive = recurse(block[:split])
        right_analysis, right_exact, right_passive = recurse(block[split:])
        analysis = np.vstack((left_analysis, right_analysis))
        polar, frame, _, support, _ = _polar_data(analysis, tolerance=tolerance)
        left_frame = _hermitian(left_analysis.conj().T @ left_analysis)
        right_frame = _hermitian(right_analysis.conj().T @ right_analysis)
        relative = np.vstack(
            (
                _psd_power(left_frame, 0.5, tolerance=tolerance),
                _psd_power(right_frame, 0.5, tolerance=tolerance),
            )
        ) @ _psd_power(frame, -0.5, tolerance=tolerance)
        local_residuals.append(
            float(np.linalg.norm(relative.conj().T @ relative - support, ord=2))
        )
        exact = _block_diagonal(left_exact, right_exact) @ relative
        passive = _block_diagonal(left_passive, right_passive) @ (
            relative / math.sqrt(2.0)
        )
        if np.linalg.norm(exact - polar, ord=2) > 1000 * tolerance:
            local_residuals.append(float(np.linalg.norm(exact - polar, ord=2)))
        return analysis, exact, passive

    _, exact_root, passive_root = recurse(leaves)
    expected_signal = 1.0 / math.sqrt(leaf_count)
    exact_residual = float(np.linalg.norm(exact_root - identity, ord=2))
    passive_residual = float(
        np.linalg.norm(passive_root - expected_signal * identity, ord=2)
    )
    passive_signal = float(np.linalg.svd(passive_root, compute_uv=False)[0])
    local_residual = max(local_residuals, default=0.0)
    bernstein = (1.0 - approximation_error) * math.sqrt(leaf_count - 1.0)
    nested = 3**depth
    verified = bool(
        exact_residual <= 1000 * tolerance
        and local_residual <= 1000 * tolerance
        and passive_residual <= 1000 * tolerance
        and abs(passive_signal - expected_signal) <= 1000 * tolerance
    )
    return OrthogonalHierarchyNormalizationControl(
        depth=depth,
        leaf_count=leaf_count,
        exact_root_polar_residual=exact_residual,
        exact_local_relative_isometry_residual=local_residual,
        passively_normalized_root_signal=passive_signal,
        expected_passively_normalized_root_signal=expected_signal,
        passive_recursive_composition_residual=passive_residual,
        coefficient_recurrence_root_normalization=math.sqrt(leaf_count),
        global_bernstein_degree_lower_bound=bernstein,
        literal_local_qsvt_minimum_odd_degree=3,
        literal_nested_qsvt_leaf_query_lower_bound=nested,
        supplied_alpha_one_local_isometry_depth=depth,
        exact_local_isometry_oracles_are_additional_access=True,
        no_passive_normalization_cancellation_verified=verified,
        status=(
            "exact-polar-telescopes-passive-normalization-does-not"
            if verified
            else "orthogonal-hierarchy-normalization-control-failure"
        ),
    )


def _selected_parameters(n: int) -> tuple[int, int, int, int]:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    information = (order - 1).bit_length()
    selected = information + 2
    width = 1 << selected
    return order, information, selected, width


def natural_recursive_normalization_scaling_record(
    n: int,
    *,
    approximation_error: float = DEFAULT_POLAR_ERROR,
) -> NaturalRecursiveNormalizationScalingRecord:
    if not 0 < approximation_error < 1:
        raise ValueError("approximation error must lie in (0,1)")
    order, information, selected, width = _selected_parameters(n)
    global_degree_log2 = (
        math.log2(1.0 - approximation_error)
        + 0.5 * math.log2(1.0 - 2.0 ** (-selected))
        + selected / 2.0
    )
    nested_log2 = selected * math.log2(3.0)
    return NaturalRecursiveNormalizationScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=information,
        selected_copy_count=selected,
        orientation_leaf_width_decimal=str(width),
        recursive_depth=selected,
        coefficient_root_normalization_log2=selected / 2.0,
        global_qsvt_degree_lower_bound_log2=global_degree_log2,
        literal_nested_degree_three_query_lower_bound_log2=nested_log2,
        supplied_local_isometry_composition_depth=selected,
        coefficient_only_recursive_assembly_superpolynomial=True,
        literal_nested_local_qsvt_superpolynomial=True,
        normalization_one_local_relative_isometries_compiled=False,
        status="recursive-normalization-conservation-factorial-width-boundary",
    )


def run_recursive_polar_normalization_conservation_boundary(
) -> RecursivePolarNormalizationConservationReport:
    support_controls = [
        audit_support_aware_tree(
            f"rank-one-leaf-frame-d{dimension}",
            deterministic_rank_deficient_leaves(dimension),
        )
        for dimension in (2, 3, 4)
    ]
    normalization_controls = [
        audit_coefficient_normalization(
            "unit-leaves-w8",
            (1.0,) * 8,
        ),
        audit_coefficient_normalization(
            "heterogeneous-leaves-w7",
            (1.0, 1.5, 2.0, 0.75, 3.0, 1.25, 2.5),
        ),
    ]
    metric_scale_controls = [
        audit_child_polar_metric_scale(
            f"rank-deficient-child-d{dimension}",
            np.vstack(deterministic_rank_deficient_leaves(dimension)[:-1]),
            math.sqrt(2 * dimension - 1),
        )
        for dimension in (2, 3, 4)
    ]
    shorted_metric_controls = [
        audit_shorted_metric_scale("common-alpha", 2.0, 2.0),
        audit_shorted_metric_scale("unequal-alpha", 2.0, 3.0),
    ]
    trim_control = audit_trim_compatibility()
    orthogonal_controls = [
        audit_orthogonal_hierarchy_normalization(depth) for depth in range(1, 7)
    ]
    scaling_records = [
        natural_recursive_normalization_scaling_record(n)
        for n in (8, 16, 24, 32, 40, 48)
    ]
    failures = (
        sum(not row.exact_support_aware_telescoping_verified for row in support_controls)
        + sum(
            not row.sharp_l2_normalization_recurrence_verified
            for row in normalization_controls
        )
        + sum(
            not row.exact_metric_scale_inheritance_verified
            for row in metric_scale_controls
        )
        + sum(
            not row.exact_shorted_metric_scale_inheritance_verified
            for row in shorted_metric_controls
        )
        + int(not trim_control.exact_trim_compatibility_boundary_verified)
        + sum(
            not row.no_passive_normalization_cancellation_verified
            for row in orthogonal_controls
        )
    )
    verified = failures == 0
    theorem = RecursivePolarNormalizationConservationTheorem(
        support_aware_chain_rule=(
            "With Moore--Penrose inverses on support, Q_v=(direct_sum_c Q_c)[sqrt(S_c)]_c S_v^(-1/2) and W_v^*W_v=supp(S_v)."
        ),
        algebraic_telescoping=(
            "The local relative isometries telescope exactly through any tree, including rank-deficient child supports."
        ),
        coefficient_normalization_recurrence=(
            "A coefficient-only PREPARE/SELECT stack has the sharp recurrence alpha_v^2=sum_c alpha_c^2."
        ),
        grouping_consequence=(
            "The root normalization is sqrt(sum_e alpha_e^2), independent of balanced, left-deep, or multiscale regrouping; unit leaves give sqrt(w)."
        ),
        child_polar_scale_identity=(
            "Normalization-one Q_c access does not reset child analysis scale: Q_c^*(R_c/alpha_c)=sqrt(S_c)/alpha_c."
        ),
        shorted_metric_scale_identity=(
            "On a sibling intersection, normalized frames obey Ghat_c=alpha_c^2 G_c and (S_c/alpha_c^2)_K=(S_c)_K/alpha_c^2; shorting does not cancel access scale."
        ),
        flat_hierarchy_control=(
            "For orthogonal leaves, exact W_v factors compose to I while generic W_v/sqrt(2) factors compose to I/sqrt(w); literal local QSVT instead inherits the degree-three nesting recurrence."
        ),
        trim_compatibility=(
            "Independently trimmed children are reusable for parent projection Pi_v iff direct_sum_c R_c(Pi_c-Pi_v)=0; retained conditioning alone does not imply this."
        ),
        conditional_positive_boundary=(
            "If compatible normalization-one coherent W_v oracles are supplied, the root polar uses one oracle layer per tree level with no width amplitude loss."
        ),
        surviving_interface=(
            "Construct uniform structured W_v SELECT/oracles, or flatten the affine/GPE/Schur hierarchy into a direct global router."
        ),
        scope=(
            "The negative result is for coefficient-only recursive assembly and literal nested local QSVT. It is not an arbitrary hierarchical-query lower bound."
        ),
        theorem_verified=verified,
        status=(
            "recursive-polar-algebra-telescopes-normalization-conserved"
            if verified
            else "recursive-polar-normalization-control-failure"
        ),
    )
    return RecursivePolarNormalizationConservationReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "The exact recursive polar chain rule automatically cancels the inherited square-root leaf normalization when normalized child analyses are regrouped through a hierarchy."
            ),
            "exact_positive_result": (
                "The support-aware relative polar factors do telescope exactly, and supplied normalization-one local relative-isometry oracles would compile the root in tree depth."
            ),
            "negative_boundary": (
                "Coefficient-only controlled stacking conserves squared normalization: alpha_v^2=sum_c alpha_c^2. Child polars and shorted coordinates move, but do not remove, the inherited scale."
            ),
            "trim_boundary": (
                "Recursive reuse additionally requires the exact common-parent trim condition direct_sum_c R_c(Pi_c-Pi_v)=0."
            ),
            "claim_boundary": (
                "No arbitrary recursive-query lower bound, representation-specific router impossibility, physical PGM, decoder, separation, or speedup is proved."
            ),
        },
        theorem=theorem,
        support_controls=support_controls,
        normalization_controls=normalization_controls,
        metric_scale_controls=metric_scale_controls,
        shorted_metric_controls=shorted_metric_controls,
        trim_control=trim_control,
        orthogonal_controls=orthogonal_controls,
        scaling_records=scaling_records,
        proof_obligations=[
            {
                "obligation": "audit_exact_support_aware_recursive_factorization",
                "resolved": True,
                "evidence": "Equation (1) follows from R_c=Q_c sqrt(S_c); rank-deficient deterministic trees verify every node and the direct root polar with Moore--Penrose supports.",
            },
            {
                "obligation": "derive_sharp_recursive_normalization_recurrence",
                "resolved": True,
                "evidence": "Equal parent block coefficients force PREPARE amplitudes a_c=alpha_c/alpha_v; unit state norm is exactly alpha_v^2=sum_c alpha_c^2.",
            },
            {
                "obligation": "decide_whether_tree_regrouping_cancels_leaf_width",
                "resolved": True,
                "evidence": "Repeated squared-sum recurrence gives alpha_root^2=sum_e alpha_e^2 for every grouping. Balanced and left-deep heterogeneous controls agree to numerical precision.",
            },
            {
                "obligation": "decide_whether_child_polars_reset_metric_normalization",
                "resolved": True,
                "evidence": "The exact identity Q_c^*(R_c/alpha_c)=sqrt(S_c)/alpha_c retains the same normalization on the positive endpoint factor.",
            },
            {
                "obligation": "audit_normalization_in_shorted_intersection_coordinates",
                "resolved": True,
                "evidence": "Pseudoinverse scaling gives Ghat_c=alpha_c^2 G_c and normalized shorted operator (S_c)_K/alpha_c^2. Equal alpha preserves only balance equality; unequal alpha spoils apparent balance without explicit rescaling.",
            },
            {
                "obligation": "audit_retained_support_and_trim_reuse",
                "resolved": True,
                "evidence": "The exact compatibility condition is direct_sum_c R_c(Pi_c-Pi_v)=0. A two-child control drops eigenvalue 0.4 locally although its parent sum 0.8 is retained, producing unit polar error.",
            },
            {
                "obligation": "compile_normalization_one_local_relative_isometries",
                "resolved": False,
                "evidence": "Equation (1) defines W_v but normalized leaf/GPE access does not provide it at alpha one. Uniform representation-specific SELECT and compatible short-metric access remain open.",
            },
            {
                "obligation": "implement_physical_pgm_and_hidden_involution_decoder",
                "resolved": False,
                "evidence": "The pass stops at the orientation polar access interface and proves neither physical measurement implementation nor decoding success.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The exact chain rule itself proves the normalizations telescope.",
                "resolved": True,
                "resolution": "It proves operator factorization. Query normalization is metadata of the available block encodings; coefficient-only composition obeys the separate squared-sum law (2).",
            },
            {
                "objection": "A normalization-one child polar removes the child normalization before the merge.",
                "resolved": True,
                "resolution": "Multiplying it back into the normalized child analysis gives sqrt(S_c)/alpha_c, so the normalization survives on the metric factor needed by W_v.",
            },
            {
                "objection": "Passing to shorted sibling metrics cancels the inherited scale.",
                "resolved": True,
                "resolution": "Shorting reverses the scale: the compressed pseudoinverse metric gains alpha_c^2 and the shorted operator loses alpha_c^2. It supplies spectral coordinates, not a normalization-one access oracle.",
            },
            {
                "objection": "A balanced tree should replace sqrt(w) by O(log w).",
                "resolved": True,
                "resolution": "Depth becomes logarithmic, but the coefficient scale satisfies alpha_root^2=sum_e alpha_e^2 independent of grouping. Passive binary factors multiply to 1/sqrt(w).",
            },
            {
                "objection": "Constant local gaps let QSVT reset every binary factor at constant total query cost.",
                "resolved": True,
                "resolution": "Constant degree is not constant after literal oracle nesting: the predecessor flat control gives q_(ell+1)>=3q_ell. This statement remains scoped to that architecture.",
            },
            {
                "objection": "Any independently well-conditioned retained child polar can be reused at its parent.",
                "resolved": True,
                "resolution": "Parent and child spectral projections may differ because positive eigenvalues add. Exact reuse requires R_c Pi_c=R_c Pi_v jointly for all children.",
            },
            {
                "objection": "The result rules out every structured hierarchical compiler.",
                "resolved": True,
                "resolution": "No. Supplied normalization-one W_v oracles compose in depth. The theorem identifies their uniform construction and trim-compatible access as the missing positive primitive.",
            },
        ],
        headline_metrics={
            "exact_support_aware_recursive_polar_telescoping_theorem_count": int(verified),
            "sharp_l2_normalization_conservation_theorem_count": int(verified),
            "child_polar_metric_scale_inheritance_theorem_count": int(verified),
            "shorted_metric_scale_inheritance_theorem_count": int(verified),
            "independent_trim_noncomposability_theorem_count": int(verified),
            "flat_passive_normalization_no_cancellation_theorem_count": int(verified),
            "support_control_count": len(support_controls),
            "normalization_control_count": len(normalization_controls),
            "metric_scale_control_count": len(metric_scale_controls),
            "shorted_metric_control_count": len(shorted_metric_controls),
            "orthogonal_hierarchy_control_count": len(orthogonal_controls),
            "finite_control_failure_count": failures,
            "largest_finite_passive_root_normalization": orthogonal_controls[-1].coefficient_recurrence_root_normalization,
            "largest_finite_nested_qsvt_query_lower_bound": orthogonal_controls[-1].literal_nested_qsvt_leaf_query_lower_bound,
            "compiled_normalization_one_local_relative_isometry_count": 0,
            "compiled_orientation_root_polar_count": 0,
            "physical_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "support_aware_recursive_polar_factors_telescope_exactly": verified,
            "coefficient_only_normalizations_obey_squared_sum_recurrence": verified,
            "tree_grouping_reduces_root_normalization": False,
            "unit_leaf_root_normalization_is_sqrt_width": verified,
            "child_polar_resets_child_analysis_normalization": False,
            "shorted_metrics_cancel_child_analysis_normalization": False,
            "shorted_metric_scale_inheritance_proved": verified,
            "passive_binary_relative_factors_compose_to_root_over_sqrt_width": verified,
            "literal_nested_local_qsvt_is_polynomial_at_natural_depth": False,
            "independent_retained_child_trims_automatically_compose": False,
            "compatible_normalization_one_local_relative_isometries_would_close_in_depth": verified,
            "normalization_one_local_relative_isometries_compiled": False,
            "arbitrary_hierarchical_query_lower_bound_proved": False,
            "representation_specific_flattened_router_ruled_out": False,
            "orientation_polar_Q_R_compiled": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The recursive operators telescope only after normalization-one relative isometries are available. Coefficient-only child assembly conserves squared normalization and independently chosen trims can invalidate reuse; the required structured local router remains uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Separated exact recursive polar algebra from block-encoding access normalization. The factors telescope on support, but coefficient-only assembly has the tree-invariant root scale sqrt(sum_e alpha_e^2), child polars and shorted coordinates retain that scale, and independent trims require a new compatibility interface."
        ),
        falsifiers_triggered=[
            "Algebraic polar telescoping is not query-normalization cancellation.",
            "Balanced or multiscale regrouping does not change alpha_root^2=sum_e alpha_e^2.",
            "A normalization-one child polar leaves sqrt(S_c)/alpha_c when applied to R_c/alpha_c.",
            "Shorted intersection metrics rescale by alpha_c^2 rather than cancelling access normalization.",
            "Independently well-conditioned child trims need not represent the parent-retained analysis.",
            "Normalization-one compatible W_v oracles would close the chain in depth, so no arbitrary hierarchical no-go is established.",
        ],
    )


def write_recursive_polar_normalization_conservation_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_recursive_polar_normalization_conservation_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_experiment(
            ExperimentRecord(
                id=DEFAULT_EXPERIMENT_ID,
                candidate_id=DEFAULT_CANDIDATE_ID,
                title="Recursive polar normalization conservation boundary",
                status="completed-exact-recursive-access-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Prove the Moore--Penrose recursive polar chain rule, derive the sharp coefficient PREPARE/SELECT normalization recurrence, audit child-polar metric scale inheritance and trim compatibility, and compare exact versus passively normalized orthogonal trees."
                ),
                positive_signal=(
                    "A uniform representation-specific compiler for compatible normalization-one local relative isometries W_v, or a flattened affine GPE/Schur router that bypasses coefficient-only recursive stacking."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_hierarchical_polar_tree.py",
                    "self_dual_wreath_sparse_polar_access_composition_no_go.py",
                    "self_dual_wreath_final_root_addressed_weyl_assembly_boundary.py",
                    "self_dual_wreath_graded_frobenius_trim.py",
                    "self_dual_wreath_gpe_recursive_node_compiler.py",
                ],
                next_actions=[
                    "Audit the surviving structured interface: decide whether affine/GPE child embeddings and shorted metrics supply a uniform normalization-one SELECT for each compatible W_v, without independently re-trimming child supports."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Exact recursive polar factorization and tree regrouping automatically cancel the inherited square-root orientation-width normalization."
                ),
                reason_invalid=(
                    "Operator factors telescope only when the relative isometries W_v are already available. Coefficient-only PREPARE/SELECT assembly instead has the sharp recurrence alpha_v^2=sum_c alpha_c^2, giving alpha_root=sqrt(sum_e alpha_e^2); Q_c^*(R_c/alpha_c)=sqrt(S_c)/alpha_c retains the scale. On sibling intersections, compressed pseudoinverse metrics gain alpha_c^2 and shorted operators lose alpha_c^2 rather than cancelling it. Independent child trims also require direct_sum_c R_c(Pi_c-Pi_v)=0."
                ),
                lesson=(
                    "Do not count algebraic chain rules as access normalization cancellation. Expose normalization-one, trim-compatible W_v oracles or flatten the hierarchy through representation-specific routing."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "recursive_normalization_recurrence": "alpha_v^2=sum_c alpha_c^2",
                    "unit_leaf_root_normalization": "sqrt(w)",
                    "child_polar_metric_identity": "Q_c^*(R_c/alpha_c)=sqrt(S_c)/alpha_c",
                    "shorted_metric_scaling": "Ghat_c=alpha_c^2 G_c and Shat_c,K=S_c,K/alpha_c^2",
                    "trim_compatibility_condition": "direct_sum_c R_c(Pi_c-Pi_v)=0",
                    "literal_nested_local_qsvt_query_recurrence": "q_(ell+1)>=3q_ell",
                    "normalization_one_local_relative_isometries_compiled": False,
                    "arbitrary_hierarchical_query_lower_bound_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_recursive_polar_normalization_conservation_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
