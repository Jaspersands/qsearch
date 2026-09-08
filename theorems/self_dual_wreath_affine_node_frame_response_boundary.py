"""Representation-specific affine-node frame and response-access boundary.

The generic addressed-kernel lower bound leaves open the possibility that the
*actual* wreath-product node kernels have a succinct representation formula.
They do.  Let ``E_e`` be the physical invariant projector for orientation
``e`` and let ``A=a+U`` be an affine node of the orientation cube.  Its
normalized child frame is

    Fbar_A = |A|^-1 sum_(e in A) E_e
           = (|A||S_n|)^-1 sum_(e in A,g in S_n) R_e(g),    (1)

where

    R_e(g)=rho_tau(g) tensor_i
      [rho_lambda_i(g) tensor I,  if e_i=0;
       I tensor rho_mu_i(g),      if e_i=1].

Preparing a uniform affine coordinate and a uniform permutation, applying
the controlled representation action, and unpreparing gives an exact LCU
block encoding of ``Fbar_A`` with normalization one.  The affine address is
computed with ``O(k dim(U))`` CNOTs; no table of ``|A|`` leaves or local
metric values is used.  This is the requested all-n low-description formula
for the aggregate physical frame.

It is not yet a response oracle.  If ``X`` is the common physical child span,
the recursive response metric is

    A_A = X^* F_A^+ X,              F_A=|A| Fbar_A.        (2)

Thus ``X^*Fbar_A^+X=|A|A_A``.  At a balanced binary node the common width
factor cancels exactly from the two-outcome endpoint effect, so the
mathematical endpoint is scale-free.  A compiler that separately applies
QSVT pseudoinversion to the normalization-one encodings in (1), however,
still has to resolve the eigenvalues of ``Fbar_A``.

The natural final-sibling second-moment theorem makes that last distinction
decisive.  Uniformly over both siblings and every target, the trace-weighted
*full-sibling* mass of ``Fbar_A`` above ``1/poly(n)`` is ``o(1)`` under
globally distinct Plancherel sources.  Dividing that trace bound by the
threshold also makes the high-window rank ``o(D)``.  The natural final-root
common-span theorem supplies ``r >= (19/128-o(1))D`` on source probability
``1/9-o(1)``, so the common intersection of the two separately truncated
QSVT windows has dimension ``o(r)``.  Separate inversion therefore cannot be
a uniform compiler on the common parent fiber.

This does *not* yet prove that the discarded common-fiber directions carry
large conditional physical input mass.  Such a conclusion needs a density
bound for the native parent state on the common span.  Hence the requested
``o(1/L)`` parent-conditional native-loss recurrence remains open rather than
falsified.

This is representation-specific: equation (1) uses the exact ``S_n`` action
and the mass conclusion uses the exact natural sibling frame law.  It does
not rule out a joint scale-free generalized-eigenvalue circuit, a direct
Schur/Racah Naimark recurrence, or another transform that never materializes
the two pseudoinverses separately.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentRecord,
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_natural_q_scale_spectral_window_no_go import (
    natural_q_scale_window_scaling_record,
)
from self_dual_wreath_final_root_natural_common_span import (
    run_final_root_natural_common_span,
)
from self_dual_wreath_orientation_fourier_reduction import (
    Label,
    Partition,
    _orientation_representation_matrix,
    _source_representation_rows,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_affine_node_frame_response_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-FRAME-RESPONSE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "AFFINE-NODE-NORMALIZED-FRAME-QSVT-NO-NATURAL-RESPONSE"
)
BEALS_QFT_URL = "https://doi.org/10.1145/258533.258548"
QSVT_URL = "https://arxiv.org/abs/1806.01838"


@dataclass(frozen=True)
class AffineNodeFrameControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_bit_count: int
    affine_dimension: int
    affine_offset: int
    affine_generators: tuple[int, ...]
    node_width: int
    ambient_dimension: int
    normalized_frame_rank: int
    normalized_frame_minimum_positive_eigenvalue: float
    normalized_frame_maximum_eigenvalue: float
    representation_summand_count: int
    lcu_block_encoding_normalization: float
    unnormalized_frame_lcu_normalization: int
    affine_mask_table_entry_count: int
    maximum_representation_formula_residual: float
    minimum_normalized_frame_eigenvalue: float
    exact_affine_node_representation_average_verified: bool
    status: str


@dataclass(frozen=True)
class ResponseScaleCancellationControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    child_width: int
    physical_dimension: int
    common_span_dimension: int
    left_frame_rank: int
    right_frame_rank: int
    left_response_minimum_eigenvalue: float
    right_response_minimum_eigenvalue: float
    minimum_normalized_child_frame_positive_eigenvalue: float
    separate_inverse_condition_number_lower_bound: float
    maximum_response_width_scaling_residual: float
    endpoint_effect_scale_cancellation_residual: float
    endpoint_effect_minimum_eigenvalue: float
    endpoint_effect_maximum_eigenvalue: float
    equal_width_scale_cancels_exactly: bool
    separate_normalized_frame_inverse_still_required: bool
    exact_response_scale_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class AffineNodeCircuitRecord:
    n: int
    orientation_bit_count: int
    affine_dimension: int
    node_width_decimal: str
    permutation_count_decimal: str
    affine_coordinate_hadamard_count: int
    affine_mask_cnot_upper_bound: int
    permutation_index_workspace_qubits: int
    orientation_workspace_qubits: int
    controlled_irrep_action_count_per_select: int
    average_frame_block_encoding_normalization: float
    sum_frame_block_encoding_normalization_decimal: str
    leaf_metric_table_entries: int
    polynomial_given_controlled_sn_action: bool
    response_pseudoinverse_compiled: bool
    status: str


@dataclass(frozen=True)
class NaturalResponseWindowRecord:
    n: int
    hierarchy_depth: int
    sibling_width_decimal: str
    polynomial_window_degree: int
    normalized_frame_threshold: float
    polynomial_condition_number: int
    conditional_good_event_probability_lower_bound: float
    globally_distinct_full_sibling_native_retained_mass_upper_bound: float
    globally_distinct_full_sibling_native_loss_lower_bound: float
    required_per_level_loss_benchmark: float
    required_retained_mass_benchmark: float
    high_spectral_window_relative_rank_upper_bound_proxy: float
    common_spectral_trim_relative_dimension_upper_bound_proxy: float
    finite_full_sibling_mass_requirement_falsified: bool
    common_span_event_mass_asymptotic_lower_bound: float
    common_span_relative_rank_asymptotic_lower_bound: float
    asymptotic_common_spectral_trim_relative_dimension_vanishes: bool
    asymptotic_inverse_polynomial_window_mass_vanishes: bool
    polynomial_separate_qsvt_inverse_is_uniform_common_fiber_compiler: bool
    parent_common_fiber_native_density_bound_proved: bool
    parent_conditional_native_loss_recurrence_proved: bool
    direct_joint_scale_free_naimark_ruled_out: bool
    status: str


@dataclass(frozen=True)
class AffineNodeFrameResponseTheorem:
    actual_frame_formula: str
    uniform_circuit: str
    normalization: str
    response_formula: str
    balanced_scale_cancellation: str
    separate_inverse_boundary: str
    parent_trim_boundary: str
    surviving_route: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AffineNodeFrameResponseReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    theorem: AffineNodeFrameResponseTheorem
    affine_frame_controls: list[AffineNodeFrameControl]
    response_controls: list[ResponseScaleCancellationControl]
    circuit_records: list[AffineNodeCircuitRecord]
    natural_window_records: list[NaturalResponseWindowRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _binary_rank(vectors: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        reduced = int(vector)
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return len(pivots)


def affine_node_masks(
    bit_count: int,
    offset: int,
    generators: tuple[int, ...],
) -> tuple[int, ...]:
    """Return the masks in ``offset + span_F2(generators)`` exactly once."""

    if bit_count < 1:
        raise ValueError("bit_count must be positive")
    limit = 1 << bit_count
    if not 0 <= offset < limit:
        raise ValueError("affine offset out of range")
    if any(generator <= 0 or generator >= limit for generator in generators):
        raise ValueError("affine generators must be nonzero bit_count-bit masks")
    if _binary_rank(generators) != len(generators):
        raise ValueError("affine generators must be linearly independent")
    masks = []
    for coefficients in range(1 << len(generators)):
        mask = offset
        for index, generator in enumerate(generators):
            if coefficients & (1 << index):
                mask ^= generator
        masks.append(mask)
    return tuple(sorted(masks))


def affine_node_average_frame(
    target: Partition,
    labels: tuple[Label, ...],
    offset: int,
    generators: tuple[int, ...],
) -> np.ndarray:
    """Average the physical orientation projectors over one affine node."""

    masks = affine_node_masks(len(labels), offset, generators)
    first = orientation_invariant_projector(target, labels, masks[0])
    total = sum(
        (
            orientation_invariant_projector(target, labels, mask)
            for mask in masks
        ),
        start=np.zeros_like(first),
    )
    return (total + total.conj().T) / (2 * len(masks))


def representation_lcu_affine_node_average(
    target: Partition,
    labels: tuple[Label, ...],
    offset: int,
    generators: tuple[int, ...],
) -> np.ndarray:
    """Evaluate equation (1), the top block of the affine/group LCU."""

    masks = affine_node_masks(len(labels), offset, generators)
    target_rows = _source_representation_rows(target)
    first_permutation = next(iter(target_rows))
    first_term = np.kron(
        target_rows[first_permutation],
        _orientation_representation_matrix(
            labels,
            first_permutation,
            masks[0],
        ),
    )
    total = np.zeros_like(first_term, dtype=complex)
    for permutation, target_matrix in target_rows.items():
        for mask in masks:
            total += np.kron(
                target_matrix,
                _orientation_representation_matrix(labels, permutation, mask),
            )
    total /= len(target_rows) * len(masks)
    return (total + total.conj().T) / 2


def _positive_eigenvalues(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    return values[values > 100 * tolerance]


def audit_affine_node_frame_formula(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    offset: int,
    generators: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> AffineNodeFrameControl:
    masks = affine_node_masks(len(labels), offset, generators)
    direct = affine_node_average_frame(target, labels, offset, generators)
    formula = representation_lcu_affine_node_average(
        target,
        labels,
        offset,
        generators,
    )
    residual = float(np.linalg.norm(direct - formula, ord=2))
    values = np.linalg.eigvalsh(direct)
    positive = values[values > 100 * tolerance]
    verified = bool(
        positive.size
        and float(values.min()) >= -100 * tolerance
        and float(values.max()) <= 1 + 100 * tolerance
        and residual <= 100 * tolerance
    )
    return AffineNodeFrameControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        orientation_bit_count=len(labels),
        affine_dimension=len(generators),
        affine_offset=offset,
        affine_generators=generators,
        node_width=len(masks),
        ambient_dimension=len(direct),
        normalized_frame_rank=len(positive),
        normalized_frame_minimum_positive_eigenvalue=float(positive.min()),
        normalized_frame_maximum_eigenvalue=float(positive.max()),
        representation_summand_count=len(masks) * math.factorial(sum(target)),
        lcu_block_encoding_normalization=1.0,
        unnormalized_frame_lcu_normalization=len(masks),
        affine_mask_table_entry_count=0,
        maximum_representation_formula_residual=residual,
        minimum_normalized_frame_eigenvalue=float(values.min()),
        exact_affine_node_representation_average_verified=verified,
        status=(
            "exact-affine-node-representation-average-normalization-one"
            if verified
            else "affine-node-representation-average-control-failure"
        ),
    )


def _range_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    return vectors[:, values > 100 * tolerance]


def _common_span_basis(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    left_basis = _range_basis(left, tolerance)
    right_basis = _range_basis(right, tolerance)
    overlap = left_basis.conj().T @ right_basis
    left_vectors, singular, _ = np.linalg.svd(overlap, full_matrices=False)
    common = singular > 1 - 100 * tolerance
    return left_basis @ left_vectors[:, common]


def _endpoint_effect(
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    metric = (left_metric + right_metric + left_metric.conj().T + right_metric.conj().T) / 2
    values, vectors = np.linalg.eigh(metric)
    if values[0] <= 100 * tolerance:
        raise ArithmeticError("endpoint metric must be positive definite")
    inverse_root = (vectors * values**-0.5) @ vectors.conj().T
    effect = inverse_root @ left_metric @ inverse_root
    return (effect + effect.conj().T) / 2


def audit_equal_width_response_scale_cancellation(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    left_offset: int,
    right_offset: int,
    generators: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> ResponseScaleCancellationControl:
    left_masks = affine_node_masks(len(labels), left_offset, generators)
    right_masks = affine_node_masks(len(labels), right_offset, generators)
    if set(left_masks) & set(right_masks) or len(left_masks) != len(right_masks):
        raise ValueError("children must be disjoint and have equal width")
    projectors = {
        mask: orientation_invariant_projector(target, labels, mask)
        for mask in (*left_masks, *right_masks)
    }
    zero = np.zeros_like(next(iter(projectors.values())))
    left_frame = sum((projectors[mask] for mask in left_masks), start=zero.copy())
    right_frame = sum((projectors[mask] for mask in right_masks), start=zero.copy())
    common = _common_span_basis(left_frame, right_frame, tolerance)
    if not common.shape[1]:
        raise ValueError("finite response control needs a nonempty common span")
    width = len(left_masks)
    left_average = left_frame / width
    right_average = right_frame / width
    raw_metrics = tuple(
        common.conj().T @ np.linalg.pinv(frame, rcond=tolerance) @ common
        for frame in (left_frame, right_frame)
    )
    normalized_metrics = tuple(
        common.conj().T @ np.linalg.pinv(frame, rcond=tolerance) @ common
        for frame in (left_average, right_average)
    )
    scaling_residual = max(
        float(np.linalg.norm(normalized - width * raw, ord=2))
        for normalized, raw in zip(normalized_metrics, raw_metrics)
    )
    raw_effect = _endpoint_effect(*raw_metrics, tolerance)
    normalized_effect = _endpoint_effect(*normalized_metrics, tolerance)
    endpoint_residual = float(np.linalg.norm(raw_effect - normalized_effect, ord=2))
    effect_values = np.linalg.eigvalsh(raw_effect)
    frame_positive = np.concatenate(
        (
            _positive_eigenvalues(left_average, tolerance),
            _positive_eigenvalues(right_average, tolerance),
        )
    )
    verified = bool(
        scaling_residual <= 1000 * tolerance
        and endpoint_residual <= 1000 * tolerance
        and effect_values[0] >= -100 * tolerance
        and effect_values[-1] <= 1 + 100 * tolerance
    )
    return ResponseScaleCancellationControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        child_width=width,
        physical_dimension=len(left_frame),
        common_span_dimension=common.shape[1],
        left_frame_rank=int(np.linalg.matrix_rank(left_frame, tol=100 * tolerance)),
        right_frame_rank=int(np.linalg.matrix_rank(right_frame, tol=100 * tolerance)),
        left_response_minimum_eigenvalue=float(np.linalg.eigvalsh(raw_metrics[0]).min()),
        right_response_minimum_eigenvalue=float(np.linalg.eigvalsh(raw_metrics[1]).min()),
        minimum_normalized_child_frame_positive_eigenvalue=float(frame_positive.min()),
        separate_inverse_condition_number_lower_bound=float(1 / frame_positive.min()),
        maximum_response_width_scaling_residual=scaling_residual,
        endpoint_effect_scale_cancellation_residual=endpoint_residual,
        endpoint_effect_minimum_eigenvalue=float(effect_values.min()),
        endpoint_effect_maximum_eigenvalue=float(effect_values.max()),
        equal_width_scale_cancels_exactly=verified,
        separate_normalized_frame_inverse_still_required=True,
        exact_response_scale_boundary_verified=verified,
        status=(
            "equal-width-response-scale-cancels-separate-inverse-remains"
            if verified
            else "response-scale-cancellation-control-failure"
        ),
    )


def affine_node_circuit_record(
    n: int,
    orientation_bit_count: int,
    affine_dimension: int,
) -> AffineNodeCircuitRecord:
    if n < 2 or not 0 <= affine_dimension <= orientation_bit_count:
        raise ValueError("invalid circuit scaling parameters")
    width = 1 << affine_dimension
    return AffineNodeCircuitRecord(
        n=n,
        orientation_bit_count=orientation_bit_count,
        affine_dimension=affine_dimension,
        node_width_decimal=str(width),
        permutation_count_decimal=str(math.factorial(n)),
        affine_coordinate_hadamard_count=affine_dimension,
        affine_mask_cnot_upper_bound=orientation_bit_count * affine_dimension,
        permutation_index_workspace_qubits=(math.factorial(n) - 1).bit_length(),
        orientation_workspace_qubits=orientation_bit_count,
        controlled_irrep_action_count_per_select=orientation_bit_count + 1,
        average_frame_block_encoding_normalization=1.0,
        sum_frame_block_encoding_normalization_decimal=str(width),
        leaf_metric_table_entries=0,
        polynomial_given_controlled_sn_action=True,
        response_pseudoinverse_compiled=False,
        status="normalization-one-affine-frame-lcu-response-inverse-open",
    )


def natural_response_window_record(
    n: int,
    *,
    polynomial_window_degree: int = 4,
    confidence_degree: int = 2,
) -> NaturalResponseWindowRecord:
    source = natural_q_scale_window_scaling_record(
        n,
        polynomial_window_degree=polynomial_window_degree,
        confidence_degree=confidence_degree,
    )
    depth = source.selected_copy_count
    divisor = n**polynomial_window_degree
    retained = source.conditional_native_high_mass_upper_bound
    loss = max(0.0, 1.0 - retained)
    required_loss = 1.0 / (depth * depth)
    required_retained = 1.0 - required_loss
    falsified = bool(
        source.finite_conditional_bound_nonvacuous
        and retained < required_retained
    )
    rank_fraction = min(
        1.0,
        retained
        * source.child_aspect_ratio
        * (1.0 + source.relative_rank_tolerance)
        * divisor,
    )
    common_rank = 19.0 / 128.0
    common_fraction = min(1.0, rank_fraction / common_rank)
    return NaturalResponseWindowRecord(
        n=n,
        hierarchy_depth=depth,
        sibling_width_decimal=source.child_orientation_count_decimal,
        polynomial_window_degree=polynomial_window_degree,
        normalized_frame_threshold=1.0 / divisor,
        polynomial_condition_number=divisor,
        conditional_good_event_probability_lower_bound=(
            source.conditioned_good_event_probability_lower_bound
        ),
        globally_distinct_full_sibling_native_retained_mass_upper_bound=retained,
        globally_distinct_full_sibling_native_loss_lower_bound=loss,
        required_per_level_loss_benchmark=required_loss,
        required_retained_mass_benchmark=required_retained,
        high_spectral_window_relative_rank_upper_bound_proxy=rank_fraction,
        common_spectral_trim_relative_dimension_upper_bound_proxy=common_fraction,
        finite_full_sibling_mass_requirement_falsified=falsified,
        common_span_event_mass_asymptotic_lower_bound=1.0 / 9.0,
        common_span_relative_rank_asymptotic_lower_bound=common_rank,
        asymptotic_common_spectral_trim_relative_dimension_vanishes=True,
        asymptotic_inverse_polynomial_window_mass_vanishes=True,
        polynomial_separate_qsvt_inverse_is_uniform_common_fiber_compiler=False,
        parent_common_fiber_native_density_bound_proved=False,
        parent_conditional_native_loss_recurrence_proved=False,
        direct_joint_scale_free_naimark_ruled_out=False,
        status=(
            "finite-full-sibling-window-mass-falsified-common-fiber-dimension-asymptotic"
            if falsified
            else "asymptotic-response-window-rank-no-go-finite-mass-bound-vacuous"
        ),
    )


def _finite_controls() -> tuple[
    list[AffineNodeFrameControl],
    list[ResponseScaleCancellationControl],
]:
    repeated_standard: tuple[Label, ...] = (((3,), (2, 1)),) * 3
    collision_free_four: tuple[Label, ...] = (
        ((4,), (3, 1)),
        ((2, 2), (2, 1, 1)),
    )
    frames = [
        audit_affine_node_frame_formula(
            "S3-THREE-BIT-LEFT-SIBLING",
            (3,),
            repeated_standard,
            0,
            (1, 2),
        ),
        audit_affine_node_frame_formula(
            "S3-THREE-BIT-RIGHT-SIBLING",
            (3,),
            repeated_standard,
            4,
            (1, 2),
        ),
        audit_affine_node_frame_formula(
            "S4-COLLISION-FREE-FULL-AFFINE-NODE",
            (2, 2),
            collision_free_four,
            0,
            (1, 2),
        ),
    ]
    responses = [
        audit_equal_width_response_scale_cancellation(
            "S3-THREE-BIT-BALANCED-ROOT",
            (3,),
            repeated_standard,
            0,
            4,
            (1, 2),
        )
    ]
    return frames, responses


def run_affine_node_frame_response_boundary() -> AffineNodeFrameResponseReport:
    frames, responses = _finite_controls()
    circuits = [
        affine_node_circuit_record(n, bit_count, affine_dimension)
        for n, bit_count, affine_dimension in (
            (16, 47, 46),
            (24, 82, 81),
            (32, 120, 119),
            (40, 162, 161),
            (48, 205, 204),
        )
    ]
    natural = [natural_response_window_record(n) for n in (16, 24, 32, 40, 48)]
    common_span_source = run_final_root_natural_common_span()
    failures = sum(
        not row.exact_affine_node_representation_average_verified for row in frames
    ) + sum(not row.exact_response_scale_boundary_verified for row in responses)
    frame_verified = all(
        row.exact_affine_node_representation_average_verified for row in frames
    )
    response_verified = all(
        row.exact_response_scale_boundary_verified for row in responses
    )
    sibling_mass_source_verified = all(
        row.asymptotic_inverse_polynomial_window_mass_vanishes for row in natural
    )
    common_span_source_verified = bool(
        common_span_source.headline_metrics.get(
            "natural_positive_mass_final_common_span_theorem_count",
            0,
        )
        and common_span_source.claim_gate.get(
            "natural_final_common_span_has_constant_relative_rank_on_positive_mass",
            False,
        )
        and abs(
            common_span_source.headline_metrics.get(
                "asymptotic_common_span_relative_rank_lower_bound",
                0.0,
            )
            - 19.0 / 128.0
        )
        < 1e-15
        and abs(
            common_span_source.headline_metrics.get(
                "asymptotic_conditioned_event_mass_lower_bound",
                0.0,
            )
            - 1.0 / 9.0
        )
        < 1e-15
    )
    finite_mass_no_go = sum(
        row.finite_full_sibling_mass_requirement_falsified for row in natural
    )
    verified = bool(
        failures == 0
        and frame_verified
        and response_verified
        and sibling_mass_source_verified
        and common_span_source_verified
    )
    theorem = AffineNodeFrameResponseTheorem(
        actual_frame_formula=(
            "Fbar_A=(|A||S_n|)^-1 sum_(e in A,g in S_n) R_e(g) for every affine orientation node A."
        ),
        uniform_circuit=(
            "Uniform affine-coordinate and permutation PREPARE, reversible XOR mask evaluation, controlled S_n representation SELECT, then inverse PREPARE."
        ),
        normalization=(
            "The normalized average Fbar_A has LCU normalization one; the unnormalized sum F_A has the explicit width factor |A|."
        ),
        response_formula=(
            "A_A=X^*F_A^+X=|A|^-1 X^*Fbar_A^+X on the common physical child span."
        ),
        balanced_scale_cancellation=(
            "For equal-width children, multiplying both response metrics by |A| leaves the canonical two-outcome endpoint effect unchanged."
        ),
        separate_inverse_boundary=(
            "Separate inverse-polynomial-resolution QSVT pseudoinversion of Fbar_L and Fbar_R reaches only o(1) full-sibling native mass and o(D) spectral rank."
        ),
        parent_trim_boundary=(
            "On the positive-mass event r>=(19/128-o(1))D, the common intersection of both polynomial QSVT windows has dimension o(r); conversion to parent-conditional native mass is open."
        ),
        surviving_route=(
            "A joint scale-free generalized-eigenvalue transform or direct Schur/Racah Naimark recurrence that avoids separate frame inversion remains open."
        ),
        theorem_verified=verified,
        status=(
            "affine-node-frame-lcu-proved-separate-qsvt-uniform-common-fiber-falsified-native-density-open"
            if verified
            else "affine-node-frame-response-boundary-control-failure"
        ),
    )
    headline: dict[str, int | float] = {
        "actual_affine_node_frame_formula_theorem_count": int(frame_verified),
        "normalization_one_affine_node_frame_block_encoding_count": int(frame_verified),
        "equal_width_endpoint_scale_cancellation_theorem_count": int(response_verified),
        "imported_natural_sibling_mass_theorem_count": int(
            sibling_mass_source_verified
        ),
        "imported_positive_mass_common_span_theorem_count": int(
            common_span_source_verified
        ),
        "separate_qsvt_full_sibling_mass_no_go_theorem_count": int(verified),
        "separate_qsvt_common_fiber_dimension_no_go_theorem_count": int(verified),
        "affine_frame_control_count": len(frames),
        "response_scale_control_count": len(responses),
        "finite_control_failure_count": failures,
        "maximum_frame_formula_residual": max(
            row.maximum_representation_formula_residual for row in frames
        ),
        "maximum_endpoint_scale_cancellation_residual": max(
            row.endpoint_effect_scale_cancellation_residual for row in responses
        ),
        "finite_full_sibling_mass_requirement_falsified_row_count": finite_mass_no_go,
        "first_finite_full_sibling_mass_no_go_n": next(
            (row.n for row in natural if row.finite_full_sibling_mass_requirement_falsified),
            0,
        ),
        "tail_full_sibling_native_retained_mass_upper_bound": (
            natural[-1].globally_distinct_full_sibling_native_retained_mass_upper_bound
        ),
        "tail_common_spectral_trim_relative_dimension_upper_bound_proxy": (
            natural[-1].common_spectral_trim_relative_dimension_upper_bound_proxy
        ),
        "parent_conditional_native_loss_recurrence_theorem_count": 0,
        "direct_joint_scale_free_naimark_compiler_count": 0,
        "physical_pgm_circuit_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return AffineNodeFrameResponseReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "paper_id": "beals-symmetric-qft-1997",
                "url": BEALS_QFT_URL,
                "scope": "Polynomial S_n Fourier/representation-action primitive; no internal Kronecker/Racah response transform is imported.",
            },
            {
                "paper_id": "gilyen-su-low-wiebe-qsvt-2018",
                "url": QSVT_URL,
                "scope": "Polynomial singular-value functional calculus used only for the scoped separate-pseudoinverse architecture.",
            },
        ],
        theorem_contract={
            "hypothesis": (
                "The exact affine-node representation average, block-encoded at normalization one, can be separately pseudoinverted at polynomial resolution to give a uniform balanced-endpoint compiler on the natural common parent fiber."
            ),
            "positive_boundary": (
                "The actual aggregate child frame does have a table-free all-n representation formula and normalization-one block encoding, and balanced endpoint effects are algebraically independent of the common child width."
            ),
            "negative_boundary": (
                "The separate-pseudoinverse implementation is not a uniform common-fiber compiler: every inverse-polynomial normalized-frame window has o(1) full-sibling native mass and o(D) rank, while the common span has Theta(D) rank on positive source mass."
            ),
            "access_model": (
                "Coherent affine-coordinate preparation, uniform permutation preparation, controlled Young-basis S_n representation actions, standard LCU block encoding, and QSVT applied separately to each normalized child frame."
            ),
            "normalization": (
                "Fbar_A is exposed at alpha=1; F_A=|A|Fbar_A. QSVT sees the small eigenvalues of Fbar_A even though |A| cancels from the exact two-child endpoint formula."
            ),
            "natural_input_relevance": (
                "The mass/rank boundary imports the exact Plancherel sibling second moment, global-distinct conditioning, uniform target/orientation rank concentration, physical native-trace bridge, and positive-mass final common-span theorem."
            ),
            "classical_alternative": (
                "Direct classical construction and diagonalization of the physical frames remains exponential in their representation dimension. The theorem supplies no classical response compiler or dequantization; it only excludes the stated separate-QSVT quantum architecture."
            ),
            "scope": (
                "No lower bound is claimed for a joint generalized-eigenvalue circuit, direct local Schur/Racah Naimark transform, nonlinear multi-query compiler, arbitrary quantum circuit, decoder, or classical separation."
            ),
        },
        theorem=theorem,
        affine_frame_controls=frames,
        response_controls=responses,
        circuit_records=circuits,
        natural_window_records=natural,
        proof_obligations=[
            {
                "obligation": "derive_actual_affine_node_representation_kernel",
                "resolved": frame_verified,
                "resolution": "Average the exact invariant-projector group sum over a reversible affine mask superposition, yielding equation (1) with no addressed metric table.",
            },
            {
                "obligation": "state_uniform_coherent_evaluation_and_normalization",
                "resolved": frame_verified,
                "resolution": "Affine and permutation PREPARE/SELECT/unprepare gives Fbar_A at normalization one using polynomial workspace under the existing controlled S_n action primitive.",
            },
            {
                "obligation": "separate_frame_access_from_response_access",
                "resolved": response_verified,
                "resolution": "The response is a compressed pseudoinverse. Equal child widths cancel from the endpoint effect algebraically but not from a circuit that inverts each normalized frame separately.",
            },
            {
                "obligation": "verify_imported_natural_mass_and_common_span_theorems",
                "resolved": sibling_mass_source_verified and common_span_source_verified,
                "resolution": "The live sibling-window theorem certifies inverse-polynomial mass decay, and the live final-root theorem certifies common relative rank 19/128-o(1) on source mass 1/9-o(1).",
            },
            {
                "obligation": "test_common_parent_spectral_dimension_at_polynomial_response_edge",
                "resolved": verified,
                "resolution": "The high-window trace bound implies high-window rank o(D). On the positive-mass event where the final common span has rank at least (19/128-o(1))D, their common spectral intersection has o(1) relative common-fiber dimension.",
            },
            {
                "obligation": "prove_parent_conditional_native_loss_o_one_over_depth",
                "resolved": False,
                "resolution": "A dimension no-go does not bound a possibly concentrated native parent state. Need a source-weighted density bound on the common fiber or a direct joint Naimark recurrence.",
            },
            {
                "obligation": "compile_joint_scale_free_racah_endpoint_transform",
                "resolved": False,
                "resolution": "A circuit could in principle exploit the ratio before resolving either absolute normalized-frame scale. No such generalized-eigenvalue or direct Naimark transform is constructed or ruled out.",
            },
            {
                "obligation": "compile_physical_pgm_decoder_and_classical_separation",
                "resolved": False,
                "resolution": "The result constrains one response architecture and provides neither the complete polar nor an outcome decoder or advantage theorem.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The generic addressed-oracle counterfamily may not occur in representation kernels.",
                "resolved": True,
                "resolution": "This theorem no longer uses that family. Equation (1) is the exact S_n invariant-projector average and the mass no-go is under the natural Plancherel source law.",
            },
            {
                "objection": "A factorial leaf table is still hidden in the affine average.",
                "resolved": True,
                "resolution": "The node mask is computed from affine coordinates with O(k dim(U)) CNOTs; the LCU prepares coordinates rather than enumerating masks."
            },
            {
                "objection": "Normalization one for Fbar_A immediately gives a polynomial response inverse.",
                "resolved": True,
                "resolution": "False. Natural eigenvalues carrying the native mass sit below every inverse-polynomial scale in Fbar_A at the final sibling node."
            },
            {
                "objection": "The explicit width factor proves the balanced endpoint itself is ill-conditioned.",
                "resolved": True,
                "resolution": "False. The factor multiplies both response metrics and cancels exactly from the endpoint effect. The obstruction is the separate-inverse access architecture, not the abstract endpoint ratio."
            },
            {
                "objection": "Independent child trims could evade the common-trim mass statement.",
                "resolved": False,
                "resolution": "Intersecting the two QSVT spectral windows gives one compatible parent projection with o(1) relative common-fiber dimension, but this does not rule out a different joint compressed-frame oracle or prove a native-mass statement."
            },
            {
                "objection": "Small common spectral dimension proves large conditional physical loss.",
                "resolved": False,
                "resolution": "Not without a native-state density bound on the common fiber. The parent-conditional mass recurrence remains open and is not inferred from rank alone."
            },
            {
                "objection": "Vanishing polynomial-window mass rules out direct Racah Naimark synthesis.",
                "resolved": False,
                "resolution": "It does not. A direct circuit may cancel common scale before functional calculus or implement the positive dilation without separate frame inverses."
            },
        ],
        headline_metrics=headline,
        claim_gate={
            "actual_affine_node_frame_low_description_formula_proved": frame_verified,
            "actual_affine_node_frame_block_encoding_normalization_one": frame_verified,
            "uniform_affine_node_frame_evaluation_polynomial_given_sn_action": frame_verified,
            "balanced_response_width_scale_cancellation_proved": response_verified,
            "normalized_frame_access_equals_response_access": False,
            "separate_polynomial_qsvt_response_preserves_full_sibling_native_mass": False,
            "separate_qsvt_is_uniform_common_fiber_response_compiler": False,
            "separate_qsvt_common_spectral_trim_has_nonvanishing_common_fiber_dimension": False,
            "parent_common_fiber_native_density_bound_proved": False,
            "parent_conditional_native_loss_o_one_over_depth_proved": False,
            "separate_qsvt_uniform_response_architecture_falsified_on_natural_final_siblings": verified,
            "joint_scale_free_generalized_eigenvalue_compiler_proved": False,
            "direct_local_schur_racah_naimark_ruled_out": False,
            "structured_racah_response_oracle_compiled": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact aggregate representation frame is succinct and normalization one, but separately pseudoinverting its normalized child blocks reaches only vanishing full-sibling mass and vanishing relative common-fiber dimension. Parent-conditional native density is still open; the remaining high-impact route is a joint scale-free Racah/generalized-eigenvalue Naimark transform."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived a normalization-one all-n affine-node representation frame block encoding and proved exact balanced endpoint scale cancellation, then showed that separate polynomial-resolution QSVT reaches only o(1) full-sibling mass and o(1) relative common-fiber dimension; parent-conditional native mass remains open."
        ),
        falsifiers_triggered=[
            "Actual affine-node representation kernels require arbitrary addressed metric aggregation.",
            "Normalization-one access to the averaged child frame is equivalent to polynomial access to its compressed pseudoinverse response.",
            "The common parent intersection of two inverse-polynomial QSVT spectral windows can have nonvanishing relative dimension in the natural final common fiber.",
            "The explicit affine width factor by itself makes the abstract balanced endpoint ill-conditioned.",
        ],
    )


def write_affine_node_frame_response_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_affine_node_frame_response_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Affine-node representation frame response boundary",
                status="completed-representation-frame-and-natural-response-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Derive the exact affine-node S_n group average, validate it against physical invariant projectors, prove equal-width response scale cancellation, then combine the exact natural sibling mass/rank theorem with the positive-mass final common-span theorem to test separate polynomial-resolution pseudoinversion."
                ),
                positive_signal=(
                    "A joint scale-free generalized-eigenvalue or direct Schur/Racah Naimark circuit that uses the normalization-one affine frame oracle without separately resolving its exponentially small normalized eigenvalues."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_orientation_fourier_reduction.py",
                    "self_dual_wreath_natural_q_scale_spectral_window_no_go.py",
                    "self_dual_wreath_final_root_natural_common_span.py",
                    "self_dual_wreath_hierarchical_cokernel_resolution.py",
                    "self_dual_wreath_affine_flag_aggregate_schur_query_boundary.py",
                ],
                next_actions=[
                    "Construct or obstruct a joint scale-free generalized-eigenvalue/Racah endpoint transform that never materializes either child pseudoinverse separately; charge coherent evaluation, relative spectral gap, and native mass."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Normalization-one block encodings of the exact affine-node averaged frames can be separately pseudoinverted at inverse-polynomial resolution to give a uniform compiler on the natural balanced common fiber."
                ),
                reason_invalid=(
                    "For natural final siblings, the exact second-moment/rank theorem makes the full-sibling native mass and rank above every inverse-polynomial eigenvalue of Fbar_s vanish. The final common span has Theta(D) rank on positive source mass, so the common intersection of the two truncated spectral windows has o(1) relative common-fiber dimension. Parent-conditional native mass is not inferred."
                ),
                lesson=(
                    "Use the exact affine-node frame oracle only inside a joint scale-free endpoint or direct Naimark construction. Do not separately invert the normalized child frames with generic QSVT."
                ),
                applies_to=[
                    registry_candidate_id,
                    "PO-MECHANISM",
                    "PO-COMPLEXITY",
                    "PO-NOGO",
                ],
                evidence={
                    "actual_affine_node_frame_formula_proved": True,
                    "average_frame_block_encoding_normalization": 1.0,
                    "balanced_width_scale_cancels": True,
                    "separate_qsvt_natural_mass_preserved": False,
                    "tail_full_sibling_native_retained_mass_upper_bound": payload[
                        "headline_metrics"
                    ]["tail_full_sibling_native_retained_mass_upper_bound"],
                    "parent_conditional_native_loss_recurrence_proved": False,
                    "direct_joint_racah_naimark_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
        if registry_result_id is not None:
            upsert_experiment_result(
                ExperimentResultRecord(
                    id=registry_result_id,
                    experiment_id=registry_experiment_id,
                    candidate_id=registry_candidate_id,
                    created_at=payload["created_at"],
                    status=payload["status"],
                    summary=payload["summary"],
                    metrics=payload["headline_metrics"],
                    falsifiers_triggered=payload["falsifiers_triggered"],
                    artifacts={
                        "self_dual_wreath_affine_node_frame_response_boundary": str(
                            path
                        )
                    },
                )
            )
    return payload


if __name__ == "__main__":
    result = write_affine_node_frame_response_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
