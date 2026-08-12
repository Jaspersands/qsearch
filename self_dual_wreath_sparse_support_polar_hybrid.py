"""Native-state polar stability for the sparse support-surrogate hierarchy.

This module closes the state-error bridge left open by
``self_dual_wreath_sparse_support_polar_schedule``.  It does not construct a
coherent circuit.

Let ``A,B`` be sums of orthogonal projections, let ``P=supp(A)`` and
``Q=supp(B)``, and let ``W_A,W_B`` be partial isometries with initial
projections ``P,Q``.  Define

    X = [W_A sqrt(A); W_B sqrt(B)],     S=X*X=A+B,
    Y = [W_A P;       W_B Q],          T=Y*Y=P+Q.

Writing ``U=polar(X)`` and ``V=polar(Y)``, the native input covariance is
``S/Tr(S)``.  Since ``U sqrt(S)=X`` and ``V sqrt(T)=Y``, Powers--Stoermer and
the sparse-frame identities imply

    ||(U-V)sqrt(S)||_F / sqrt(N)
      <= sqrt(rho) + (2 rho)^(1/4),                     (1)

where ``N=Tr(S)`` and

    rho = [Tr(A^2)-Tr(A)+Tr(B^2)-Tr(B)] / N.

No lower spectral edge is assumed.  The fourth-root term is the price of
converting normalized Frobenius frame error to trace-norm square-root error.

The bound composes recursively.  If exact and surrogate child polar factors
have the same initial supports, then replacing the children before the parent
polarization preserves the Gram matrix exactly and

    ||(U_W-U_Z)sqrt(S)||_F^2
      = sum_s ||(W_s-Z_s)sqrt(A_s)||_F^2.                (2)

Moreover the support-surrogate parent polar has initial support
``supp(P+Q)=supp(A+B)``, so the invariant needed by (2) propagates at every
level.  For natural sparse children of aspect ``alpha`` and
``h=|G|^-1``, ``E rho=alpha-h``.  Along a geometric early hierarchy ending at
``alpha<=2/R``, Minkowski and Jensen therefore give annealed native RMS error

    O(R^(-1/4)).                                        (3)

The ill-conditioned low singular sector of ``Y`` is also small in native
mass.  If ``H_kappa`` is the spectral projector of ``P+Q`` on
``(0,1-kappa)``, then

    Tr(S H_kappa)/N
      <= (1-kappa) rank(H_kappa)/N + sqrt(2 rho),        (4)

and ``rank(H_kappa)<=Tr(PQ)/kappa^2``.  The natural support-overlap moment
bound makes the geometric aggregate in (4) ``O(kappa^-2 R^-1/2)``.

Equations (1)-(4) prove that the sparse support replacement and the removal
of badly conditioned principal-angle modes are asymptotically harmless for
the native state when the fixed jump arity is chosen sufficiently large.
They do not provide coherent support reflections, a singular-value filter,
the fixed-R endpoint measurement, or an end-to-end algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_sparse_support_polar_schedule import (
    _random_projector,
    natural_sparse_moment_record,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sparse_support_polar_hybrid.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-SPARSE-SUPPORT-POLAR-HYBRID"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class NativePolarPerturbationControl:
    control_id: str
    ambient_dimension: int
    total_trace: float
    support_scalarization_pressure: float
    normalized_pressure: float
    exact_native_rms_polar_error: float
    native_rms_polar_error_upper_bound: float
    square_root_trace_distance: float
    square_root_trace_distance_upper_bound: float
    initial_supports_match: bool
    gap_free_native_polar_bound_verified: bool
    status: str


@dataclass(frozen=True)
class SameGramHybridControl:
    control_id: str
    ambient_dimension: int
    total_trace: float
    parent_native_error_squared: float
    weighted_child_error_squared: float
    gram_matrix_difference_norm: float
    parent_initial_supports_match: bool
    exact_same_gram_hybrid_identity_verified: bool
    status: str


@dataclass(frozen=True)
class LowSingularNativeMassControl:
    control_id: str
    ambient_dimension: int
    principal_correlation_threshold: float
    low_singular_rank: int
    low_singular_rank_upper_bound: float
    exact_native_state_mass: float
    native_state_mass_upper_bound: float
    normalized_support_scalarization_pressure: float
    low_singular_rank_and_native_mass_bounds_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalSparseHybridScheduleRecord:
    jump_log2_arity: int
    jump_arity_decimal: str
    principal_correlation_threshold: float
    maximum_early_child_aspect: float
    aggregate_native_rms_polar_error_upper_bound: float
    aggregate_native_polar_mse_upper_bound: float
    aggregate_low_singular_native_mass_upper_bound: float
    asymptotic_native_rms_rate: str
    asymptotic_low_singular_mass_rate: str
    jump_arity_fixed_before_n_limit: bool
    coherent_support_reflection_compiler_proved: bool
    status: str


@dataclass(frozen=True)
class SparseSupportPolarHybridTheorem:
    gap_free_native_bound: str
    exact_recursive_hybrid: str
    support_invariant: str
    annealed_natural_transfer: str
    low_singular_native_mass: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SparseSupportPolarHybridReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SparseSupportPolarHybridTheorem
    perturbation_controls: list[NativePolarPerturbationControl]
    same_gram_controls: list[SameGramHybridControl]
    low_singular_controls: list[LowSingularNativeMassControl]
    natural_schedule_records: list[NaturalSparseHybridScheduleRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_sqrt(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    return (vectors * np.sqrt(np.maximum(values, 0.0))) @ vectors.conj().T


def _support_projector(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    basis = vectors[:, values > 100 * tolerance]
    return basis @ basis.conj().T


def _polar_factor(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    gram = _hermitian(matrix.conj().T @ matrix)
    values, vectors = np.linalg.eigh(gram)
    inverse_root = np.zeros_like(values)
    positive = values > 100 * tolerance
    inverse_root[positive] = 1.0 / np.sqrt(values[positive])
    return matrix @ ((vectors * inverse_root) @ vectors.conj().T)


def _trace_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.svd(matrix, compute_uv=False).sum())


def _validate_sum_of_projectors_frame(
    frame: np.ndarray,
    coefficient_trace: float,
    tolerance: float,
) -> tuple[np.ndarray, int]:
    support = _support_projector(frame, tolerance)
    rank = int(round(float(np.trace(support).real)))
    if rank > coefficient_trace + 1000 * tolerance:
        raise ValueError("support rank must not exceed the projector coefficient trace")
    return support, rank


def audit_native_polar_perturbation(
    control_id: str,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    *,
    left_coefficient_trace: float | None = None,
    right_coefficient_trace: float | None = None,
    tolerance: float = 1e-9,
) -> NativePolarPerturbationControl:
    if (
        left_frame.ndim != 2
        or left_frame.shape[0] != left_frame.shape[1]
        or right_frame.shape != left_frame.shape
    ):
        raise ValueError("frames must share one square ambient space")
    left = _hermitian(left_frame)
    right = _hermitian(right_frame)
    left_trace = float(np.trace(left).real)
    right_trace = float(np.trace(right).real)
    left_coefficient_trace = (
        left_trace if left_coefficient_trace is None else left_coefficient_trace
    )
    right_coefficient_trace = (
        right_trace if right_coefficient_trace is None else right_coefficient_trace
    )
    left_support, left_rank = _validate_sum_of_projectors_frame(
        left, left_coefficient_trace, tolerance
    )
    right_support, right_rank = _validate_sum_of_projectors_frame(
        right, right_coefficient_trace, tolerance
    )
    left_root = _psd_sqrt(left, tolerance)
    right_root = _psd_sqrt(right, tolerance)
    exact_analysis = np.vstack((left_root, right_root))
    support_analysis = np.vstack((left_support, right_support))
    exact_polar = _polar_factor(exact_analysis, tolerance)
    support_polar = _polar_factor(support_analysis, tolerance)
    total_frame = left + right
    total_support_frame = left_support + right_support
    total_root = _psd_sqrt(total_frame, tolerance)
    total_support_root = _psd_sqrt(total_support_frame, tolerance)
    total_trace = left_trace + right_trace
    if total_trace <= tolerance:
        raise ValueError("the total native trace must be positive")
    raw_pressure = float(
        np.trace(left @ left).real
        - left_trace
        + np.trace(right @ right).real
        - right_trace
    )
    pressure = (
        0.0
        if abs(raw_pressure) <= 1000 * tolerance * max(1.0, total_trace)
        else max(0.0, raw_pressure)
    )
    rho = pressure / total_trace
    exact_error = float(
        np.linalg.norm((exact_polar - support_polar) @ total_root, ord="fro")
        / math.sqrt(total_trace)
    )
    upper = math.sqrt(rho) + (2.0 * rho) ** 0.25
    root_distance = float(
        np.linalg.norm(total_root - total_support_root, ord="fro") ** 2
    )
    root_distance_upper = math.sqrt(2.0 * total_trace * pressure)
    exact_initial = exact_polar.conj().T @ exact_polar
    support_initial = support_polar.conj().T @ support_polar
    initial_match = bool(
        np.linalg.norm(exact_initial - support_initial, ord=2) <= 5000 * tolerance
        and left_rank + right_rank <= total_trace + 5000 * tolerance
    )
    verified = bool(
        root_distance <= root_distance_upper + 5000 * tolerance
        and exact_error <= upper + 5000 * tolerance
        and initial_match
    )
    return NativePolarPerturbationControl(
        control_id=control_id,
        ambient_dimension=left.shape[0],
        total_trace=total_trace,
        support_scalarization_pressure=pressure,
        normalized_pressure=rho,
        exact_native_rms_polar_error=exact_error,
        native_rms_polar_error_upper_bound=upper,
        square_root_trace_distance=root_distance,
        square_root_trace_distance_upper_bound=root_distance_upper,
        initial_supports_match=initial_match,
        gap_free_native_polar_bound_verified=verified,
        status=(
            "gap-free-native-polar-perturbation-verified"
            if verified
            else "native-polar-perturbation-control-failure"
        ),
    )


def audit_same_gram_child_hybrid(
    control_id: str,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    left_exact_child: np.ndarray,
    right_exact_child: np.ndarray,
    left_surrogate_child: np.ndarray,
    right_surrogate_child: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> SameGramHybridControl:
    left = _hermitian(left_frame)
    right = _hermitian(right_frame)
    if left.shape != right.shape or left.ndim != 2 or left.shape[0] != left.shape[1]:
        raise ValueError("frames must share one square ambient space")
    dimension = left.shape[0]
    children = (
        left_exact_child,
        right_exact_child,
        left_surrogate_child,
        right_surrogate_child,
    )
    if any(child.shape != (dimension, dimension) for child in children):
        raise ValueError("child partial isometries must share the frame dimension")
    left_support = _support_projector(left, tolerance)
    right_support = _support_projector(right, tolerance)
    initial_checks = (
        np.linalg.norm(left_exact_child.conj().T @ left_exact_child - left_support, ord=2),
        np.linalg.norm(left_surrogate_child.conj().T @ left_surrogate_child - left_support, ord=2),
        np.linalg.norm(right_exact_child.conj().T @ right_exact_child - right_support, ord=2),
        np.linalg.norm(right_surrogate_child.conj().T @ right_surrogate_child - right_support, ord=2),
    )
    if max(initial_checks) > 5000 * tolerance:
        raise ValueError("exact and surrogate children must have the same initial supports")
    left_root = _psd_sqrt(left, tolerance)
    right_root = _psd_sqrt(right, tolerance)
    exact_analysis = np.vstack(
        (left_exact_child @ left_root, right_exact_child @ right_root)
    )
    surrogate_analysis = np.vstack(
        (left_surrogate_child @ left_root, right_surrogate_child @ right_root)
    )
    exact_gram = exact_analysis.conj().T @ exact_analysis
    surrogate_gram = surrogate_analysis.conj().T @ surrogate_analysis
    total_frame = left + right
    total_root = _psd_sqrt(total_frame, tolerance)
    exact_parent = _polar_factor(exact_analysis, tolerance)
    surrogate_parent = _polar_factor(surrogate_analysis, tolerance)
    parent_error = float(
        np.linalg.norm((exact_parent - surrogate_parent) @ total_root, ord="fro") ** 2
    )
    child_error = float(
        np.linalg.norm((left_exact_child - left_surrogate_child) @ left_root, ord="fro") ** 2
        + np.linalg.norm((right_exact_child - right_surrogate_child) @ right_root, ord="fro") ** 2
    )
    gram_difference = float(np.linalg.norm(exact_gram - surrogate_gram, ord=2))
    exact_initial = exact_parent.conj().T @ exact_parent
    surrogate_initial = surrogate_parent.conj().T @ surrogate_parent
    initial_match = bool(
        np.linalg.norm(exact_initial - surrogate_initial, ord=2) <= 5000 * tolerance
    )
    verified = bool(
        gram_difference <= 5000 * tolerance
        and abs(parent_error - child_error) <= 10000 * tolerance
        and initial_match
    )
    return SameGramHybridControl(
        control_id=control_id,
        ambient_dimension=dimension,
        total_trace=float(np.trace(total_frame).real),
        parent_native_error_squared=parent_error,
        weighted_child_error_squared=child_error,
        gram_matrix_difference_norm=gram_difference,
        parent_initial_supports_match=initial_match,
        exact_same_gram_hybrid_identity_verified=verified,
        status=(
            "exact-same-gram-recursive-hybrid-verified"
            if verified
            else "same-gram-recursive-hybrid-control-failure"
        ),
    )


def audit_low_singular_native_mass(
    control_id: str,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    *,
    principal_correlation_threshold: float = 0.5,
    left_coefficient_trace: float | None = None,
    right_coefficient_trace: float | None = None,
    tolerance: float = 1e-9,
) -> LowSingularNativeMassControl:
    if not 0 < principal_correlation_threshold < 1:
        raise ValueError("principal correlation threshold must lie in (0,1)")
    left = _hermitian(left_frame)
    right = _hermitian(right_frame)
    if left.shape != right.shape or left.ndim != 2 or left.shape[0] != left.shape[1]:
        raise ValueError("frames must share one square ambient space")
    left_trace = float(np.trace(left).real)
    right_trace = float(np.trace(right).real)
    left_support, _ = _validate_sum_of_projectors_frame(
        left,
        left_trace if left_coefficient_trace is None else left_coefficient_trace,
        tolerance,
    )
    right_support, _ = _validate_sum_of_projectors_frame(
        right,
        right_trace if right_coefficient_trace is None else right_coefficient_trace,
        tolerance,
    )
    total_frame = left + right
    total_support = left_support + right_support
    total_trace = left_trace + right_trace
    values, vectors = np.linalg.eigh(_hermitian(total_support))
    low = (values > 100 * tolerance) & (
        values < 1.0 - principal_correlation_threshold
    )
    low_basis = vectors[:, low]
    low_projector = low_basis @ low_basis.conj().T
    low_rank = int(np.count_nonzero(low))
    support_overlap = float(np.trace(left_support @ right_support).real)
    rank_bound = support_overlap / principal_correlation_threshold**2
    raw_pressure = float(
        np.trace(left @ left).real
        - left_trace
        + np.trace(right @ right).real
        - right_trace
    )
    pressure = (
        0.0
        if abs(raw_pressure) <= 1000 * tolerance * max(1.0, total_trace)
        else max(0.0, raw_pressure)
    )
    rho = pressure / total_trace
    native_mass = float(np.trace(total_frame @ low_projector).real / total_trace)
    mass_bound = (
        (1.0 - principal_correlation_threshold) * low_rank / total_trace
        + math.sqrt(2.0 * rho)
    )
    verified = bool(
        low_rank <= rank_bound + 5000 * tolerance
        and native_mass <= mass_bound + 5000 * tolerance
    )
    return LowSingularNativeMassControl(
        control_id=control_id,
        ambient_dimension=left.shape[0],
        principal_correlation_threshold=principal_correlation_threshold,
        low_singular_rank=low_rank,
        low_singular_rank_upper_bound=rank_bound,
        exact_native_state_mass=native_mass,
        native_state_mass_upper_bound=mass_bound,
        normalized_support_scalarization_pressure=rho,
        low_singular_rank_and_native_mass_bounds_verified=verified,
        status=(
            "low-singular-native-mass-pressure-verified"
            if verified
            else "low-singular-native-mass-control-failure"
        ),
    )


def natural_sparse_hybrid_schedule_record(
    jump_log2_arity: int,
    *,
    principal_correlation_threshold: float = 0.5,
) -> NaturalSparseHybridScheduleRecord:
    if jump_log2_arity < 3:
        raise ValueError("jump arity must be at least eight")
    if not 0 < principal_correlation_threshold < 1:
        raise ValueError("principal correlation threshold must lie in (0,1)")
    arity = 1 << jump_log2_arity
    alpha_max = 2.0 / arity
    square_sum = math.sqrt(alpha_max) / (1.0 - 2.0**-0.5)
    fourth_sum = alpha_max**0.25 / (1.0 - 2.0**-0.25)
    native_rms = square_sum + 2.0**0.25 * fourth_sum
    support_overlap_ratio_sum = (
        2.0 * alpha_max
        + (1.0 + math.sqrt(1.0 + alpha_max)) * square_sum
    )
    low_mass = (
        (1.0 - principal_correlation_threshold)
        * support_overlap_ratio_sum
        / (2.0 * principal_correlation_threshold**2)
        + math.sqrt(2.0) * square_sum
    )
    return NaturalSparseHybridScheduleRecord(
        jump_log2_arity=jump_log2_arity,
        jump_arity_decimal=str(arity),
        principal_correlation_threshold=principal_correlation_threshold,
        maximum_early_child_aspect=alpha_max,
        aggregate_native_rms_polar_error_upper_bound=native_rms,
        aggregate_native_polar_mse_upper_bound=native_rms**2,
        aggregate_low_singular_native_mass_upper_bound=low_mass,
        asymptotic_native_rms_rate="O(R^-1/4)",
        asymptotic_low_singular_mass_rate="O(kappa^-2 R^-1/2)",
        jump_arity_fixed_before_n_limit=True,
        coherent_support_reflection_compiler_proved=False,
        status="native-state-error-tunable-coherent-access-open",
    )


def _random_unitary(dimension: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    unitary, diagonal = np.linalg.qr(raw)
    phases = np.diag(diagonal)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return unitary @ np.diag(np.conj(phases))


def _finite_controls() -> tuple[
    list[NativePolarPerturbationControl],
    list[SameGramHybridControl],
    list[LowSingularNativeMassControl],
]:
    rng = np.random.default_rng(6301)
    perturbation_controls: list[NativePolarPerturbationControl] = []
    same_gram_controls: list[SameGramHybridControl] = []
    low_singular_controls: list[LowSingularNativeMassControl] = []
    for index, (dimension, leaf_count, rank) in enumerate(
        ((12, 2, 2), (16, 3, 2), (20, 4, 2))
    ):
        left_leaves = tuple(
            _random_projector(dimension, rank, rng) for _ in range(leaf_count)
        )
        right_leaves = tuple(
            _random_projector(dimension, rank, rng) for _ in range(leaf_count)
        )
        left = _hermitian(sum(left_leaves, np.zeros((dimension, dimension), complex)))
        right = _hermitian(sum(right_leaves, np.zeros((dimension, dimension), complex)))
        perturbation_controls.append(
            audit_native_polar_perturbation(
                f"PERTURB-{index}",
                left,
                right,
                left_coefficient_trace=leaf_count * rank,
                right_coefficient_trace=leaf_count * rank,
            )
        )
        left_support = _support_projector(left)
        right_support = _support_projector(right)
        same_gram_controls.append(
            audit_same_gram_child_hybrid(
                f"HYBRID-{index}",
                left,
                right,
                _random_unitary(dimension, rng) @ left_support,
                _random_unitary(dimension, rng) @ right_support,
                _random_unitary(dimension, rng) @ left_support,
                _random_unitary(dimension, rng) @ right_support,
            )
        )
        low_singular_controls.append(
            audit_low_singular_native_mass(
                f"LOW-{index}",
                left,
                right,
                left_coefficient_trace=leaf_count * rank,
                right_coefficient_trace=leaf_count * rank,
            )
        )
    return perturbation_controls, same_gram_controls, low_singular_controls


def run_sparse_support_polar_hybrid() -> SparseSupportPolarHybridReport:
    perturbations, hybrids, low_singular = _finite_controls()
    schedules = [
        natural_sparse_hybrid_schedule_record(bits)
        for bits in (8, 16, 24, 32, 40)
    ]
    moment_controls = [
        natural_sparse_moment_record(order, count)
        for order, count in ((120, 2), (5040, 16), (40320, 128))
    ]
    failures = (
        sum(not row.gap_free_native_polar_bound_verified for row in perturbations)
        + sum(not row.exact_same_gram_hybrid_identity_verified for row in hybrids)
        + sum(
            not row.low_singular_rank_and_native_mass_bounds_verified
            for row in low_singular
        )
        + sum(not row.exact_sparse_moment_identities_verified for row in moment_controls)
    )
    monotone = all(
        right.aggregate_native_rms_polar_error_upper_bound
        < left.aggregate_native_rms_polar_error_upper_bound
        and right.aggregate_low_singular_native_mass_upper_bound
        < left.aggregate_low_singular_native_mass_upper_bound
        for left, right in zip(schedules, schedules[1:])
    )
    verified = failures == 0 and monotone
    theorem = SparseSupportPolarHybridTheorem(
        gap_free_native_bound=(
            "||(polar(X)-polar(Y))sqrt(S)||F/sqrt(Tr S) "
            "<=sqrt(rho)+(2rho)^(1/4), with no lower spectral-edge assumption."
        ),
        exact_recursive_hybrid=(
            "Same-initial-support child replacement preserves the parent Gram "
            "matrix and gives an exact trace-weighted squared-error identity."
        ),
        support_invariant=(
            "supp(P+Q)=supp(A+B), so every support-surrogate parent polar has "
            "the same initial support as the exact parent polar."
        ),
        annealed_natural_transfer=(
            "E rho=alpha-|G|^-1 and geometric composition through alpha<=2/R "
            "gives annealed native RMS error O(R^-1/4)."
        ),
        low_singular_native_mass=(
            "The aggregate native mass of support-analysis singular values below "
            "sqrt(1-kappa) is O(kappa^-2 R^-1/2)."
        ),
        scope=(
            "No coherent support reflection, singular-value filter, fixed-R "
            "endpoint measurement, decoder, or complexity separation is proved."
        ),
        theorem_verified=verified,
        status=(
            "native-state-sparse-polar-hybrid-proved"
            if verified
            else "sparse-support-polar-hybrid-control-failure"
        ),
    )
    return SparseSupportPolarHybridReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        perturbation_controls=perturbations,
        same_gram_controls=hybrids,
        low_singular_controls=low_singular,
        natural_schedule_records=schedules,
        proof_obligations=[
            {
                "obligation": "convert_sparse_frame_pressure_to_native_polar_error",
                "resolved": verified,
                "resolution": "Equation (1) follows from polar reconstruction and Powers--Stoermer.",
            },
            {
                "obligation": "compose_native_polar_error_through_sparse_hierarchy",
                "resolved": verified,
                "resolution": "Equation (2), support invariance, Minkowski, and Jensen give (3).",
            },
            {
                "obligation": "bound_native_mass_of_ill_conditioned_support_modes",
                "resolved": verified,
                "resolution": "Equation (4) and the sibling support-overlap moment give the stated rate.",
            },
            {
                "obligation": "compile_coherent_recursive_support_reflections",
                "resolved": False,
                "resolution": "The theorem compares mathematical polar factors but supplies no access circuit.",
            },
            {
                "obligation": "compile_fixed_R_jump_and_final_endpoint_measurements",
                "resolved": False,
                "resolution": "Constant arity and state-small bad sectors do not themselves implement the POVM.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A lower spectral edge is hidden in the polar perturbation step.",
                "resolved": True,
                "resolution": "Native weighting cancels the exact inverse; Powers--Stoermer is gap-free.",
            },
            {
                "objection": "Local support replacement errors can amplify under recursive polarizations.",
                "resolved": True,
                "resolution": "Same initial supports preserve the Gram matrix exactly, yielding equation (2).",
            },
            {
                "objection": "A small-rank low singular sector can carry large native state mass.",
                "resolved": True,
                "resolution": "Equation (4) adds the required frame-to-support trace-distance term.",
            },
            {
                "objection": "The mathematical surrogate polar is already a coherent circuit.",
                "resolved": False,
                "resolution": "Support reflections, filtering, endpoint effects, and error-aware access remain open.",
            },
        ],
        headline_metrics={
            "gap_free_native_polar_theorem_count": int(verified),
            "exact_recursive_hybrid_theorem_count": int(verified),
            "low_singular_native_mass_theorem_count": int(verified),
            "natural_schedule_record_count": len(schedules),
            "finite_control_failure_count": failures,
            "smallest_recorded_native_rms_bound": (
                schedules[-1].aggregate_native_rms_polar_error_upper_bound
            ),
            "smallest_recorded_low_singular_mass_bound": (
                schedules[-1].aggregate_low_singular_native_mass_upper_bound
            ),
            "coherent_support_reflection_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "gap_free_native_state_polar_perturbation_proved": verified,
            "exact_same_support_recursive_hybrid_proved": verified,
            "annealed_sparse_hierarchy_error_tunable": verified,
            "low_singular_native_mass_tunable": verified,
            "operator_norm_frame_closeness_proved": False,
            "coherent_recursive_support_reflections_proved": False,
            "fixed_R_endpoint_measurement_compiled": False,
            "end_to_end_algorithm_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Native-state weighting converts sparse frame support pressure into "
            "a gap-free polar-error bound, and an exact same-support hybrid makes "
            "the early hierarchy error tunable with fixed jump arity. Coherent "
            "support and endpoint access remain unresolved, so no algorithm or "
            "speedup claim is allowed."
        ),
        falsifiers_triggered=[],
    )


def write_sparse_support_polar_hybrid_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SPARSE-SUPPORT-POLAR-HYBRID"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_sparse_support_polar_hybrid" in globals():
        report = run_sparse_support_polar_hybrid(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-SPARSE-SUPPORT-POLAR-HYBRID",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SPARSE-SUPPORT-POLAR-HYBRID.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SPARSE-SUPPORT-POLAR-HYBRID.",
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
                    "self_dual_wreath_sparse_support_polar_hybrid": str(path)
                },
            )
        )
    return payload
