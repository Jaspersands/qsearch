"""A label-retaining purification is a program state, not yet a Naimark gate.

At the final binary merge put

    K = [sqrt(A); sqrt(B)],       S = K^*K = A+B,
    V = K S^(-1/2).                                      (1)

The desired endpoint ``V`` is an isometry.  A normalized coherent
purification of the unnormalized positive frame has operator representative

    F = K/sqrt(Tr S) = V sqrt(rho),   rho=S/Tr(S),         (2)

and hence carries the right endpoint ``V`` while retaining the Schmidt
weights of ``rho``.  This immediately defeats a tempting inverse-width
claim.  Among one-sided successful filters ``X`` satisfying

    F X = sqrt(p) V/sqrt(D),                             (3)

where ``D=dim(H)``, the filter and its success probability obey

    X = sqrt(p/D) rho^(-1/2),
    p <= p_* := D lambda_min(rho).                        (4)

The contraction ``X_*=sqrt(lambda_min(rho))rho^(-1/2)`` attains equality.
Thus if ``m I <= S <= M I`` then ``p_*>=m/M``; on the retained final-root
window ``0.5 I<=S<=16 I`` this is at least ``1/32``, independent of the
factorial orientation width.

Equation (4) is simultaneously the obstruction: the unique exact filter is
the unresolved whitening map.  Mathematical single-copy convertibility does
not compile that map from the existing Schur/QFT/GPE interfaces.

There is a second, logically separate boundary.  Even granting the flattened
program state ``|V>>/sqrt(D)``, a Bell outcome indexed by a unitary error
basis ``{U_a}`` produces

    |psi> -> V U_a^* |psi>/D,                             (5)

with probability ``1/D^2``.  Retaining all ``D^2`` outcomes is deterministic
exactly when controlled output corrections satisfying

    W_a V = V U_a                                        (6)

are available.  On ``ran(V)`` their action is the conjugated logical algebra
``V U_a V^*``.  If the outcome is forgotten without correction, the channel
is completely depolarizing on the endpoint range.  A selected clean outcome
therefore costs amplitude amplification ``D``.  The prior rank-dense retained
window and high-row theorems give
``log D >= log d_nu+o(log d_nu)`` and
``d_nu>sqrt(n!)/p(n)`` on asymptotically full natural mass.

This theorem falsifies label retention as a *standalone* direct-Naimark
compiler, not label-retaining constructions themselves.  A positive route
may still implement the whitening filter by representation structure,
compile all conjugated byproducts, or use a different structured
Choi-to-channel transducer.  No lower bound for arbitrary processors, no
physical PGM circuit, decoder, classical separation, or speedup is claimed.
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
from self_dual_wreath_final_root_metric_access_width_no_go import (
    PARENT_WINDOW_LOWER,
    PARENT_WINDOW_UPPER,
)
from self_dual_wreath_joint_character_natural_sector_mass import partition_number


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_purification_naimark_program_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-"
    "PURIFICATION-NAIMARK-PROGRAM-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-FINAL-ROOT-PURIFICATION-PROGRAM-NOT-NAIMARK-GATE"
)
VIDAL_PAPER_ID = "vidal-single-copy-entanglement-conversion-1999"
VIDAL_PAPER_URL = "https://arxiv.org/abs/quant-ph/9902033"
NIELSEN_CHUANG_PAPER_ID = "nielsen-chuang-programmable-gate-arrays-1997"
NIELSEN_CHUANG_PAPER_URL = "https://arxiv.org/abs/quant-ph/9703032"


@dataclass(frozen=True)
class PurificationFlatteningControl:
    control_id: str
    input_dimension: int
    output_dimension: int
    metric_minimum_eigenvalue: float
    metric_maximum_eigenvalue: float
    metric_condition_number: float
    resource_minimum_schmidt_probability: float
    resource_maximum_schmidt_probability: float
    optimal_flattening_success_probability: float
    metric_ratio_success_lower_bound: float
    retained_window_uniform_success_lower_bound: float
    optimal_filter_operator_norm: float
    resource_normalization_residual: float
    endpoint_isometry_residual: float
    exact_flattening_residual: float
    success_norm_identity_residual: float
    filter_optimality_residual: float
    filter_uniqueness_residual: float
    constant_success_without_width_charge_verified: bool
    exact_unique_whitening_filter_verified: bool
    status: str


@dataclass(frozen=True)
class BellTransductionControl:
    control_id: str
    input_dimension: int
    output_dimension: int
    unitary_error_basis_size: int
    maximum_error_basis_unitarity_residual: float
    maximum_error_basis_orthogonality_residual: float
    maximum_bell_link_identity_residual: float
    maximum_outcome_probability_residual: float
    selected_clean_outcome_probability: float
    selected_clean_outcome_amplitude_amplification_factor: float
    maximum_byproduct_correction_residual: float
    maximum_correction_unitarity_residual: float
    coherent_all_outcome_correction_residual: float
    discarded_label_depolarizing_residual: float
    exact_bell_program_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class MetricOnlyCorrectionObstructionControl:
    input_dimension: int
    common_metric_residual: float
    common_schmidt_spectrum_residual: float
    endpoint_program_overlap: float
    endpoint_isometry_distance: float
    shared_correction_gram_obstruction: float
    same_metric_does_not_determine_byproduct_correction_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalProgramScalingRecord:
    n: int
    partition_count_decimal: str
    natural_high_row_irrep_dimension_lower_bound_decimal: str
    natural_high_row_irrep_dimension_lower_bound_log2: float
    selected_bell_success_log2_upper_bound_leading_term: float
    selected_bell_amplification_log2_lower_bound_leading_term: float
    independent_source_high_row_mass_lower_bound: float
    retained_logical_dimension_same_factorial_exponent_proved: bool
    selected_outcome_transduction_superpolynomial: bool
    all_outcome_byproduct_correction_compiled: bool
    status: str


@dataclass(frozen=True)
class PurificationNaimarkProgramTheorem:
    normalized_purification: str
    exact_filter_normal_form: str
    optimal_success: str
    retained_window_consequence: str
    bell_link: str
    byproduct_criterion: str
    natural_dimension_consequence: str
    surviving_construction: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PurificationNaimarkProgramReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PurificationNaimarkProgramTheorem
    flattening_controls: list[PurificationFlatteningControl]
    bell_transduction_controls: list[BellTransductionControl]
    metric_only_correction_obstruction: MetricOnlyCorrectionObstructionControl
    scaling_records: list[NaturalProgramScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
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
    tolerance: float,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if len(values) and float(values[0]) < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = values > 100 * tolerance
    if exponent < 0 and not bool(np.all(positive)):
        raise ValueError("negative powers require positive definiteness")
    transformed = np.zeros_like(values)
    transformed[positive] = values[positive] ** exponent
    return (vectors * transformed) @ vectors.conj().T


def final_root_endpoint(
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return ``K,S,V,rho`` from equations (1)-(2)."""

    if left_metric.shape != right_metric.shape:
        raise ValueError("child metric shape mismatch")
    if left_metric.ndim != 2 or left_metric.shape[0] != left_metric.shape[1]:
        raise ValueError("child metrics must be square")
    left = _hermitian(np.asarray(left_metric, dtype=complex))
    right = _hermitian(np.asarray(right_metric, dtype=complex))
    if min(
        float(np.min(np.linalg.eigvalsh(left))),
        float(np.min(np.linalg.eigvalsh(right))),
    ) < -100 * tolerance:
        raise ValueError("child metrics must be positive semidefinite")
    total = _hermitian(left + right)
    if float(np.min(np.linalg.eigvalsh(total))) <= 100 * tolerance:
        raise ValueError("the parent metric must be positive definite")
    analysis = np.vstack(
        (
            _psd_power(left, 0.5, tolerance=tolerance),
            _psd_power(right, 0.5, tolerance=tolerance),
        )
    )
    endpoint = analysis @ _psd_power(total, -0.5, tolerance=tolerance)
    density = total / float(np.trace(total).real)
    return analysis, total, endpoint, density


def optimal_purification_flattening_filter(
    density: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, float]:
    """Return the optimal one-sided exact flattening filter and success."""

    rho = _hermitian(np.asarray(density, dtype=complex))
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        raise ValueError("density must be square")
    values = np.linalg.eigvalsh(rho)
    if float(values[0]) <= 100 * tolerance:
        raise ValueError("density must be positive definite")
    if abs(float(np.trace(rho).real) - 1.0) > 1000 * tolerance:
        raise ValueError("density must have trace one")
    minimum = float(values[0])
    filt = math.sqrt(minimum) * _psd_power(rho, -0.5, tolerance=tolerance)
    return filt, rho.shape[0] * minimum


def audit_purification_flattening(
    control_id: str,
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> PurificationFlatteningControl:
    """Verify the exact filter normal form and optimal success in (3)-(4)."""

    analysis, total, endpoint, density = final_root_endpoint(
        left_metric,
        right_metric,
        tolerance=tolerance,
    )
    dimension = total.shape[0]
    identity = np.eye(dimension, dtype=complex)
    resource = analysis / math.sqrt(float(np.trace(total).real))
    filt, success = optimal_purification_flattening_filter(
        density,
        tolerance=tolerance,
    )
    expected = math.sqrt(success / dimension) * endpoint
    converted = resource @ filt
    metric_values = np.linalg.eigvalsh(total)
    density_values = np.linalg.eigvalsh(density)
    filter_norm = float(np.linalg.norm(filt, ord=2))

    probe_success = success / 3.0
    solved_filter = np.linalg.solve(
        _psd_power(density, 0.5, tolerance=tolerance),
        math.sqrt(probe_success / dimension) * identity,
    )
    unique_filter = (
        math.sqrt(probe_success / dimension)
        * _psd_power(density, -0.5, tolerance=tolerance)
    )
    uniqueness_residual = float(np.linalg.norm(solved_filter - unique_filter, ord=2))
    conversion_residual = float(np.linalg.norm(converted - expected, ord=2))
    success_residual = abs(float(np.linalg.norm(converted, ord="fro") ** 2) - success)
    optimality_residual = max(0.0, filter_norm - 1.0)
    endpoint_residual = float(
        np.linalg.norm(endpoint.conj().T @ endpoint - identity, ord=2)
    )
    resource_residual = abs(float(np.linalg.norm(resource, ord="fro")) - 1.0)
    metric_ratio = float(metric_values[0] / metric_values[-1])
    verified = bool(
        conversion_residual <= 100 * tolerance
        and success_residual <= 100 * tolerance
        and optimality_residual <= 100 * tolerance
        and uniqueness_residual <= 100 * tolerance
        and endpoint_residual <= 100 * tolerance
        and resource_residual <= 100 * tolerance
        and success + 100 * tolerance >= metric_ratio
    )
    return PurificationFlatteningControl(
        control_id=control_id,
        input_dimension=dimension,
        output_dimension=analysis.shape[0],
        metric_minimum_eigenvalue=float(metric_values[0]),
        metric_maximum_eigenvalue=float(metric_values[-1]),
        metric_condition_number=float(metric_values[-1] / metric_values[0]),
        resource_minimum_schmidt_probability=float(density_values[0]),
        resource_maximum_schmidt_probability=float(density_values[-1]),
        optimal_flattening_success_probability=success,
        metric_ratio_success_lower_bound=metric_ratio,
        retained_window_uniform_success_lower_bound=(
            PARENT_WINDOW_LOWER / PARENT_WINDOW_UPPER
        ),
        optimal_filter_operator_norm=filter_norm,
        resource_normalization_residual=resource_residual,
        endpoint_isometry_residual=endpoint_residual,
        exact_flattening_residual=conversion_residual,
        success_norm_identity_residual=success_residual,
        filter_optimality_residual=optimality_residual,
        filter_uniqueness_residual=uniqueness_residual,
        constant_success_without_width_charge_verified=verified,
        exact_unique_whitening_filter_verified=verified,
        status=(
            "exact-constant-success-program-state-flattening"
            if verified
            else "purification-flattening-validation-failure"
        ),
    )


def weyl_unitary_error_basis(dimension: int) -> tuple[np.ndarray, ...]:
    """Return the ``D^2`` Weyl unitaries with Hilbert--Schmidt norm sqrt(D)."""

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    shift = np.roll(np.eye(dimension, dtype=complex), 1, axis=0)
    phase = np.diag(
        np.exp(2j * np.pi * np.arange(dimension, dtype=float) / dimension)
    )
    return tuple(
        np.linalg.matrix_power(shift, p) @ np.linalg.matrix_power(phase, q)
        for p in range(dimension)
        for q in range(dimension)
    )


def bell_link_output(
    endpoint: np.ndarray,
    input_state: np.ndarray,
    error: np.ndarray,
) -> np.ndarray:
    """Contract an input and normalized endpoint Choi state with one Bell bra."""

    dimension = endpoint.shape[1]
    if input_state.shape != (dimension,) or error.shape != (dimension, dimension):
        raise ValueError("Bell-link dimensions do not match")
    resource = endpoint / math.sqrt(dimension)
    bell = error / math.sqrt(dimension)
    joint = np.einsum("a,or->aor", input_state, resource)
    return np.einsum("ar,aor->o", bell.conj(), joint)


def audit_bell_transduction(
    control_id: str,
    endpoint: np.ndarray,
    input_state: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> BellTransductionControl:
    """Verify Bell byproducts, exact corrections, and discarded-label twirl."""

    if endpoint.ndim != 2:
        raise ValueError("endpoint must be a matrix")
    dimension = endpoint.shape[1]
    output_dimension = endpoint.shape[0]
    identity = np.eye(dimension, dtype=complex)
    output_identity = np.eye(output_dimension, dtype=complex)
    if np.linalg.norm(endpoint.conj().T @ endpoint - identity, ord=2) > 1000 * tolerance:
        raise ValueError("endpoint must be an isometry")
    psi = np.asarray(input_state, dtype=complex)
    if psi.shape != (dimension,) or abs(float(np.linalg.norm(psi)) - 1.0) > 1000 * tolerance:
        raise ValueError("input_state must be a normalized input vector")

    errors = weyl_unitary_error_basis(dimension)
    projector = endpoint @ endpoint.conj().T
    maximum_unitarity = 0.0
    maximum_orthogonality = 0.0
    maximum_link = 0.0
    maximum_probability = 0.0
    maximum_correction = 0.0
    maximum_correction_unitarity = 0.0
    corrected_outputs: list[np.ndarray] = []
    discarded_channel = np.zeros((output_dimension, output_dimension), dtype=complex)

    for index, error in enumerate(errors):
        maximum_unitarity = max(
            maximum_unitarity,
            float(np.linalg.norm(error.conj().T @ error - identity, ord=2)),
        )
        for other_index, other in enumerate(errors):
            target = dimension if index == other_index else 0.0
            maximum_orthogonality = max(
                maximum_orthogonality,
                abs(complex(np.trace(error.conj().T @ other)) - target),
            )
        observed = bell_link_output(endpoint, psi, error)
        expected = endpoint @ error.conj().T @ psi / dimension
        maximum_link = max(maximum_link, float(np.linalg.norm(observed - expected)))
        maximum_probability = max(
            maximum_probability,
            abs(float(np.vdot(observed, observed).real) - 1.0 / dimension**2),
        )
        correction = endpoint @ error @ endpoint.conj().T + output_identity - projector
        corrected = correction @ observed
        maximum_correction = max(
            maximum_correction,
            float(np.linalg.norm(corrected - endpoint @ psi / dimension)),
        )
        maximum_correction_unitarity = max(
            maximum_correction_unitarity,
            float(np.linalg.norm(correction.conj().T @ correction - output_identity, ord=2)),
        )
        corrected_outputs.append(corrected)
        discarded_channel += np.outer(observed, observed.conj())

    coherent_observed = np.concatenate(corrected_outputs)
    coherent_expected = np.tile(endpoint @ psi / dimension, len(errors))
    coherent_residual = float(np.linalg.norm(coherent_observed - coherent_expected))
    depolarizing_expected = projector / dimension
    depolarizing_residual = float(
        np.linalg.norm(discarded_channel - depolarizing_expected, ord=2)
    )
    verified = bool(
        maximum_unitarity <= 100 * tolerance
        and maximum_orthogonality <= 100 * tolerance
        and maximum_link <= 100 * tolerance
        and maximum_probability <= 100 * tolerance
        and maximum_correction <= 100 * tolerance
        and maximum_correction_unitarity <= 100 * tolerance
        and coherent_residual <= 100 * tolerance
        and depolarizing_residual <= 100 * tolerance
    )
    return BellTransductionControl(
        control_id=control_id,
        input_dimension=dimension,
        output_dimension=output_dimension,
        unitary_error_basis_size=len(errors),
        maximum_error_basis_unitarity_residual=maximum_unitarity,
        maximum_error_basis_orthogonality_residual=maximum_orthogonality,
        maximum_bell_link_identity_residual=maximum_link,
        maximum_outcome_probability_residual=maximum_probability,
        selected_clean_outcome_probability=1.0 / dimension**2,
        selected_clean_outcome_amplitude_amplification_factor=float(dimension),
        maximum_byproduct_correction_residual=maximum_correction,
        maximum_correction_unitarity_residual=maximum_correction_unitarity,
        coherent_all_outcome_correction_residual=coherent_residual,
        discarded_label_depolarizing_residual=depolarizing_residual,
        exact_bell_program_boundary_verified=verified,
        status=(
            "exact-choi-program-bell-byproduct-boundary"
            if verified
            else "bell-transduction-validation-failure"
        ),
    )


def audit_metric_only_correction_obstruction(
    *,
    tolerance: float = 1e-9,
) -> MetricOnlyCorrectionObstructionControl:
    """Exhibit equal ``S`` and equal Schmidt weights but incompatible corrections."""

    identity = np.eye(2, dtype=complex)
    _, total_one, endpoint_one, rho_one = final_root_endpoint(
        0.5 * identity,
        0.5 * identity,
        tolerance=tolerance,
    )
    left_two = np.diag([0.9, 0.4]).astype(complex)
    right_two = identity - left_two
    _, total_two, endpoint_two, rho_two = final_root_endpoint(
        left_two,
        right_two,
        tolerance=tolerance,
    )
    shift = weyl_unitary_error_basis(2)[2]
    cross_gram = endpoint_one.conj().T @ endpoint_two
    obstruction = float(
        np.linalg.norm(cross_gram - shift.conj().T @ cross_gram @ shift, ord=2)
    )
    common_metric_residual = float(np.linalg.norm(total_one - total_two, ord=2))
    spectrum_residual = float(
        np.linalg.norm(
            np.sort(np.linalg.eigvalsh(rho_one))
            - np.sort(np.linalg.eigvalsh(rho_two))
        )
    )
    overlap = abs(complex(np.trace(cross_gram))) / 2.0
    distance = float(np.linalg.norm(endpoint_one - endpoint_two, ord=2))
    verified = bool(
        common_metric_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
        and overlap > tolerance
        and distance > 100 * tolerance
        and obstruction > 100 * tolerance
    )
    return MetricOnlyCorrectionObstructionControl(
        input_dimension=2,
        common_metric_residual=common_metric_residual,
        common_schmidt_spectrum_residual=spectrum_residual,
        endpoint_program_overlap=float(overlap),
        endpoint_isometry_distance=distance,
        shared_correction_gram_obstruction=obstruction,
        same_metric_does_not_determine_byproduct_correction_verified=verified,
        status=(
            "equal-metric-incompatible-byproduct-corrections"
            if verified
            else "metric-only-correction-obstruction-failure"
        ),
    )


def natural_program_scaling_record(n: int) -> NaturalProgramScalingRecord:
    """Transfer the natural high-row lower bound to selected Bell transduction."""

    if n < 4:
        raise ValueError("n must be at least four")
    partitions = partition_number(n)
    threshold = math.isqrt(math.factorial(n)) // partitions
    irrep_dimension_lower_bound = threshold + 1
    log_dimension = math.log2(irrep_dimension_lower_bound)
    return NaturalProgramScalingRecord(
        n=n,
        partition_count_decimal=str(partitions),
        natural_high_row_irrep_dimension_lower_bound_decimal=str(irrep_dimension_lower_bound),
        natural_high_row_irrep_dimension_lower_bound_log2=log_dimension,
        selected_bell_success_log2_upper_bound_leading_term=-2.0 * log_dimension,
        selected_bell_amplification_log2_lower_bound_leading_term=log_dimension,
        independent_source_high_row_mass_lower_bound=max(0.0, 1.0 - 1.0 / partitions),
        retained_logical_dimension_same_factorial_exponent_proved=True,
        selected_outcome_transduction_superpolynomial=True,
        all_outcome_byproduct_correction_compiled=False,
        status="natural-selected-bell-outcome-superpolynomial-byproducts-open",
    )


def _rotated_metric_pair(dimension: int) -> tuple[np.ndarray, np.ndarray]:
    seed = np.arange(1, dimension * dimension + 1, dtype=float).reshape(
        dimension,
        dimension,
    )
    seed = seed + 1j * np.flipud(seed) / 7.0
    metric_basis, _ = np.linalg.qr(seed + (dimension + 1) * np.eye(dimension))
    effect_basis, _ = np.linalg.qr(
        np.rot90(seed) + 1j * np.eye(dimension) * (dimension + 2)
    )
    metric_values = np.geomspace(PARENT_WINDOW_LOWER, 8.0, dimension)
    effect_values = np.linspace(0.2, 0.8, dimension)
    total = (metric_basis * metric_values) @ metric_basis.conj().T
    effect = (effect_basis * effect_values) @ effect_basis.conj().T
    total_root = _psd_power(total, 0.5, tolerance=1e-12)
    left = total_root @ effect @ total_root
    right = total_root @ (np.eye(dimension) - effect) @ total_root
    return _hermitian(left), _hermitian(right)


def run_final_root_purification_naimark_program_boundary(
) -> PurificationNaimarkProgramReport:
    flattening_controls = [
        audit_purification_flattening(
            "flat-maximally-entangled",
            0.5 * np.eye(2),
            0.5 * np.eye(2),
        ),
        audit_purification_flattening(
            "diagonal-conditioned",
            np.diag([0.1, 1.0, 6.0]),
            np.diag([0.4, 1.0, 2.0]),
        ),
        audit_purification_flattening(
            "rotated-noncommuting-d3",
            *_rotated_metric_pair(3),
        ),
        audit_purification_flattening(
            "rotated-complex-d4",
            *_rotated_metric_pair(4),
        ),
    ]
    bell_controls: list[BellTransductionControl] = []
    for dimension, identifier in ((2, "weyl-d2"), (3, "weyl-d3"), (4, "weyl-d4")):
        left, right = _rotated_metric_pair(dimension)
        _, _, endpoint, _ = final_root_endpoint(left, right)
        psi = np.arange(1, dimension + 1, dtype=complex)
        psi += 1j * np.arange(dimension, 0, -1, dtype=complex) / 3.0
        psi /= np.linalg.norm(psi)
        bell_controls.append(audit_bell_transduction(identifier, endpoint, psi))
    correction_obstruction = audit_metric_only_correction_obstruction()
    scaling = [natural_program_scaling_record(n) for n in (8, 12, 16, 24, 32, 48)]
    flattening_failures = sum(
        not row.exact_unique_whitening_filter_verified for row in flattening_controls
    )
    bell_failures = sum(not row.exact_bell_program_boundary_verified for row in bell_controls)
    verified = bool(
        flattening_failures == 0
        and bell_failures == 0
        and correction_obstruction.same_metric_does_not_determine_byproduct_correction_verified
    )
    theorem = PurificationNaimarkProgramTheorem(
        normalized_purification=(
            "F=K/sqrt(TrS)=V sqrt(rho), rho=S/TrS, and ||F||_F=1."
        ),
        exact_filter_normal_form=(
            "FX=sqrt(p/D)V implies uniquely X=sqrt(p/D)rho^(-1/2)."
        ),
        optimal_success=(
            "X is a contraction iff p<=D lambda_min(rho); equality is attained by X_*=sqrt(lambda_min(rho))rho^(-1/2)."
        ),
        retained_window_consequence=(
            "If 0.5I<=S<=16I then p_*=D lambda_min(S)/Tr(S)>=1/32, independent of orientation width."
        ),
        bell_link=(
            "A normalized endpoint Choi state and Bell outcome a produce VU_a^*|psi>/D with probability 1/D^2."
        ),
        byproduct_criterion=(
            "All outcomes are usable iff controlled corrections obey W_aV=VU_a; on ran(V) they implement VU_aV^*."
        ),
        natural_dimension_consequence=(
            "The prior rank-dense retained-window and high-row theorems give log(D)>=log(d_nu)+o(log(d_nu)) with d_nu>sqrt(n!)/p(n), so selecting one clean Bell outcome is superpolynomial."
        ),
        surviving_construction=(
            "Compile scale-free Schmidt whitening plus the conjugated logical byproduct algebra, or provide a different structured Choi-to-channel transducer."
        ),
        scope=(
            "This is an exact one-sided-filter theorem and canonical Bell-transduction boundary, not an arbitrary programmable-processor lower bound."
        ),
        theorem_verified=verified,
        status=(
            "constant-success-program-flattening-proved-direct-naimark-still-open"
            if verified
            else "purification-naimark-program-boundary-control-failure"
        ),
    )
    return PurificationNaimarkProgramReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "Retaining a normalized purification of [sqrt(A);sqrt(B)] bypasses the final-root width charge and by itself supplies a polynomial direct Naimark implementation."
            ),
            "access_model": (
                "One normalized operator-state purification F=K/sqrt(TrS), one successful contraction on its Schmidt/input leg, and canonical D-dimensional Bell transduction from a flattened endpoint Choi state."
            ),
            "positive_result": (
                "The resource state has optimal exact flattening probability D lambda_min(S)/TrS, at least 1/32 on the retained window; inverse width is not information-theoretically forced at state level."
            ),
            "negative_boundary": (
                "The exact filter is uniquely proportional to S^(-1/2), and Bell transduction needs either a 1/D^2 selected outcome or controlled V-conjugated logical byproducts."
            ),
            "natural_input_relevance": (
                "The prior rank-dense retained-window and annealed Plancherel high-row theorems give the logical D the same factorial exponent as d_nu>sqrt(n!)/p(n) on asymptotically full natural mass."
            ),
            "classical_alternative": (
                "All finite controls are direct dense linear algebra. No polynomial classical contraction or quantum/classical separation is established."
            ),
            "claim_boundary": (
                "Alternative structured multi-copy/program processors and representation-specific correction algebras are outside the theorem."
            ),
        },
        theorem=theorem,
        flattening_controls=flattening_controls,
        bell_transduction_controls=bell_controls,
        metric_only_correction_obstruction=correction_obstruction,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "decide_inverse_width_overlap_for_label_retaining_purification_state",
                "resolved": True,
                "evidence": "False on the bounded parent window: exact optimal state-flattening success is at least 1/32.",
            },
            {
                "obligation": "characterize_exact_one_sided_flattening_operation",
                "resolved": True,
                "evidence": "Full column rank gives the unique filter X=sqrt(p/D)rho^(-1/2), with sharp contraction bound p<=D lambda_min(rho).",
            },
            {
                "obligation": "compile_scale_free_whitening_filter_from_schur_qft_gpe",
                "resolved": False,
                "evidence": "The theorem identifies the filter with the unresolved endpoint inverse metric; no circuit is supplied by the existing interfaces.",
            },
            {
                "obligation": "compile_endpoint_conjugated_logical_byproduct_algebra",
                "resolved": False,
                "evidence": "Canonical all-outcome Bell transduction requires controlled W_a with W_aV=VU_a for a full D^2 unitary error basis.",
            },
            {
                "obligation": "prove_lower_bound_for_arbitrary_structured_choi_to_channel_processors",
                "resolved": False,
                "evidence": "Only the canonical Bell architecture and exact one-sided filters are covered.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Every normalized purification inherits the inverse orientation width.",
                "resolved": True,
                "resolution": "False. Width cancels from the Schmidt law rho=S/TrS, and bounded condition number gives constant optimal exact conversion probability.",
            },
            {
                "objection": "Constant-success pure-state conversion is already a direct Naimark circuit.",
                "resolved": True,
                "resolution": "False. The unique successful filter is the missing rho^(-1/2) whitening operation; existence does not compile it.",
            },
            {
                "objection": "The flattened Choi state can simply be teleported onto an arbitrary physical input.",
                "resolved": True,
                "resolution": "A clean selected Bell outcome has probability 1/D^2. Using all outcomes requires the V-conjugated logical error basis on the output range.",
            },
            {
                "objection": "The metric S alone determines those corrections.",
                "resolved": True,
                "resolution": "Two exact S=I controls have identical Schmidt spectra but a nonzero cross-Gram obstruction to any shared correction for the shift byproduct.",
            },
            {
                "objection": "The Bell calculation proves every possible Choi-to-channel processor is expensive.",
                "resolved": False,
                "resolution": "No. A different representation-specific processor or efficiently correctable structured endpoint family remains open.",
            },
        ],
        primary_literature=[
            {
                "paper_id": VIDAL_PAPER_ID,
                "url": VIDAL_PAPER_URL,
                "scope": "General optimal probabilistic single-copy pure-state conversion; the filter formula used here is also proved directly.",
            },
            {
                "paper_id": NIELSEN_CHUANG_PAPER_ID,
                "url": NIELSEN_CHUANG_PAPER_URL,
                "scope": "Exact programmable-gate context; cited only to delimit program-state versus executable-gate claims, not as the theorem's lower-bound engine.",
            },
        ],
        headline_metrics={
            "exact_purification_flattening_normal_form_theorem_count": int(verified),
            "constant_success_program_state_flattening_theorem_count": int(verified),
            "inverse_width_purification_state_no_go_count": 0,
            "exact_bell_byproduct_boundary_theorem_count": int(verified),
            "metric_only_byproduct_correction_obstruction_count": int(correction_obstruction.same_metric_does_not_determine_byproduct_correction_verified),
            "flattening_control_count": len(flattening_controls),
            "flattening_control_failure_count": flattening_failures,
            "bell_control_count": len(bell_controls),
            "bell_control_failure_count": bell_failures,
            "retained_window_flattening_success_lower_bound": PARENT_WINDOW_LOWER / PARENT_WINDOW_UPPER,
            "scale_free_whitening_filter_compiler_count": 0,
            "conjugated_byproduct_algebra_compiler_count": 0,
            "direct_matrix_povm_naimark_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "label_retaining_purification_state_has_constant_success_flattening": verified,
            "inverse_width_overlap_unavoidable_for_purification_state": False,
            "exact_one_sided_flattening_filter_is_unique_whitening": verified,
            "scale_free_whitening_filter_compiled": False,
            "flattened_choi_state_is_an_executable_isometry_oracle": False,
            "canonical_selected_bell_outcome_probability_is_inverse_dimension_squared": verified,
            "canonical_all_outcome_transduction_requires_conjugated_byproducts": verified,
            "conjugated_byproduct_algebra_compiled": False,
            "arbitrary_choi_to_channel_processor_lower_bound_proved": False,
            "direct_matrix_povm_naimark_dilation_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Label retention removes the factorial normalization only for mathematical program-state flattening. The uniquely required whitening circuit and a channel transducer with endpoint-dependent byproduct corrections remain uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that well-conditioned label-retaining purification states can be flattened exactly with constant success, then separated that state-conversion fact from direct Naimark implementation by deriving the unique whitening filter and the exact Bell byproduct algebra."
        ),
        falsifiers_triggered=[
            "An inverse-width overlap is not unavoidable for a bounded-condition label-retaining purification state.",
            "Constant-success Choi-state flattening does not by itself supply the endpoint isometry as a circuit.",
            "The exact one-sided flattening operation is not a new primitive: it is precisely inverse-metric whitening.",
            "Retaining Bell outcome labels does not erase byproducts; it moves the task to the conjugated logical matrix algebra on ran(V).",
            "Selecting only the identity Bell outcome reintroduces inverse logical dimension rather than inverse orientation width.",
        ],
    )


def write_final_root_purification_naimark_program_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_purification_naimark_program_boundary())
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
                title="Final-root purification Naimark program boundary",
                status="completed-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Derive the unique exact one-sided purification-flattening filter and sharp success probability, verify canonical Weyl/Bell transduction and its corrections, exhibit equal-metric incompatible corrections, and transfer the natural high-row dimension theorem."
                ),
                positive_signal=(
                    "A representation-specific circuit for the unique scale-free whitening filter together with the endpoint-conjugated logical byproduct algebra, or a different polynomial Choi-to-channel transducer."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_final_root_metric_access_width_no_go.py",
                    "self_dual_wreath_joint_character_purification_access_boundary.py",
                    "self_dual_wreath_joint_character_natural_sector_mass.py",
                    "self_dual_wreath_physical_pgm_intertwiner.py",
                ],
                next_actions=[
                    "Test whether the physical generalized Fourier row-copy makes the endpoint-conjugated Weyl generators VXV^* and VZV^* representation-theoretically sparse or recursively factorizable; two generators suffice to compile all Bell corrections."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "A label-retaining purification of [sqrt(A);sqrt(B)] is already a direct final-root Naimark compiler once the retained parent metric is well conditioned."
                ),
                reason_invalid=(
                    "Bounded conditioning does give constant-success program-state flattening, but its unique exact filter is proportional to rho^(-1/2). Even granting the flattened Choi state, canonical Bell application either selects one 1/D^2 outcome or requires controlled endpoint-conjugated logical byproducts VU_aV^*."
                ),
                lesson=(
                    "Charge state flattening and program-to-channel transduction separately. A viable direct Naimark route must compile the whitening operation and either the conjugated logical generators or a different structured transducer; coherent labels alone supply neither."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "optimal_flattening_success": "D lambda_min(S)/Tr(S)",
                    "retained_window_success_lower_bound": "1/32",
                    "unique_filter": "sqrt(p/D)(S/TrS)^(-1/2)",
                    "selected_bell_probability": "1/D^2",
                    "all_outcome_correction": "W_a V=V U_a",
                    "natural_dimension": "log D>=log d_nu+o(log d_nu), with d_nu>sqrt(n!)/p(n) on rank-dense high natural mass",
                    "arbitrary_processor_lower_bound_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_purification_naimark_program_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
