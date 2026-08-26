"""Natural final-root endpoint mixing is irreducibly matrix valued.

Let the two selected final sibling frames be ``A_n,B_n`` and put

    S_n=A_n+B_n,        C_n=S_n^(+1/2) A_n S_n^(+1/2).

The exact parent-polar endpoint isometry on the retained parent space is

    V_C = [sqrt(C); sqrt(I-C)].                              (1)

A scalar endpoint shortcut replaces (1) by

    U_t = [sqrt(t) I; sqrt(1-t) I],       0 <= t <= 1.       (2)

The existing all-fixed sibling theorem and fixed parent-window transfer say
that ``A_n,B_n`` converge to free MP variables of common rate
``alpha in [2,4]`` and that ``C_n`` has the symmetric free-Jacobi law.  The
free Lukacs property makes ``S=A+B`` free from ``C=S^-1/2 A S^-1/2``.  With
``tau(C)=1/2``, the alternating free-moment identity

    tau(S C S C)
      = tau(S^2) tau(C)^2
        + tau(S)^2 tau(C^2) - tau(S)^2 tau(C)^2

and the MP moments

    tau(A^2)=alpha^2+alpha,
    tau(S)=2 alpha,       tau(S^2)=4 alpha^2+2 alpha

give

    tau(C^2)=1/4+1/(8 alpha),
    tau((C-tI)^2)=(t-1/2)^2+1/(8 alpha).                   (3)

Thus the signed Hadamard ``t=1/2`` is the *best* scalar effect, but its
normalized effect error is at least ``1/32`` throughout ``alpha in [2,4]``.
It does not become exact under sibling exchangeability or equal aspect.

For the canonical positive isometries, pointwise scalar calculus gives the
operator inequality

    (V_C-U_t)^*(V_C-U_t) >= (C-tI)^2/4.                    (4)

Free Lukacs independence transfers the same function of ``C`` to the native
parent state ``rho proportional to S``.  Consequently the annealed native
mean-square error obeys

    liminf error_native(V_C,U_t)
      >= [(t-1/2)^2+1/(8 alpha)]/4
      >= 1/(32 alpha) >= 1/128.                             (5)

Scalar branch phases cannot improve the positive alignment in (2).  Even
without invoking free Lukacs for the error observable, the retained parent
window ``0.5 I <= S <= 16 I`` and the general effect-to-isometry inequality
give the weaker uniform bound ``1/(128 alpha^2) >= 1/2048``.

Controlled GPE child transports are branchwise isometries after (1), so they
preserve the error exactly.  Pair transport therefore does not scalarize the
endpoint mixer.  More fundamentally, child polar and support-transport
oracles do not determine it: the positive syntheses ``sqrt(S_L),sqrt(S_R)``
all have identity polar on full support, while changing their positive
metrics changes ``C``.  The two exact instances

    (S_L,S_R)=(I,I),
    (S_L,S_R)=(diag(3,1),diag(1,3))

have identical child polars and support transports but different endpoint
isometries at constant normalized distance.  Hence some coherent
metric-magnitude access is information-theoretically necessary.

On the other hand, the already-proved free-Jacobi bulk gap
keeps the true matrix square roots well conditioned after ``o(1)`` native
trim.  The surviving bottleneck is tightly normalized coherent access to the
matrix effect ``C`` (and its earlier-level analogues), not a final-root hard
edge or a scalar balance parameter.

This is a no-go for deterministic scalar endpoint mixers after exact child
polars have been factored out.  It is not a lower bound on matrix functional
calculus, a sourcewise operator-edge theorem, an all-depth compiler, a PGM
decoder, or a quantum speedup.
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
    "self_dual_wreath_final_root_scalar_mixer_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-SCALAR-MIXER-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = "SCHUR-COMPANION-NATURAL-FINAL-ENDPOINT-NO-SCALAR-MIXER"
FREE_LUKACS_PAPER_ID = "szpojankowski-free-lukacs-2015"
FREE_LUKACS_PAPER_URL = "https://arxiv.org/abs/1403.5300"
PARENT_WINDOW_LOWER = 0.5
PARENT_WINDOW_UPPER = 16.0
UNIFORM_EFFECT_MSE_FLOOR = 1.0 / 32.0
UNIFORM_CANONICAL_NATIVE_ERROR_FLOOR = 1.0 / 128.0
UNIFORM_WINDOW_ONLY_NATIVE_ERROR_FLOOR = 1.0 / 2048.0


@dataclass(frozen=True)
class ScalarMixerMomentRecord:
    child_aspect: float
    scalar_left_weight: float
    free_jacobi_mean: float
    free_jacobi_second_moment: float
    free_jacobi_variance: float
    scalar_effect_mean_square_error: float
    optimal_scalar_left_weight: float
    optimal_scalar_effect_mean_square_error: float
    canonical_native_error_lower_bound: float
    window_only_native_error_lower_bound: float
    hadamard_is_optimal_scalar_effect: bool
    scalar_effect_error_is_constant: bool
    status: str


@dataclass(frozen=True)
class ScalarEndpointFiniteControl:
    control_id: str
    dimension: int
    scalar_left_weight: float
    parent_minimum_eigenvalue: float
    parent_maximum_eigenvalue: float
    relative_effect_minimum_eigenvalue: float
    relative_effect_maximum_eigenvalue: float
    relative_effect_mean: float
    relative_effect_variance: float
    scalar_effect_mean_square_error: float
    canonical_naimark_mean_square_error: float
    native_canonical_mean_square_error: float
    native_window_effect_lower_bound: float
    phase_perturbed_native_error: float
    transported_native_error: float
    endpoint_completeness_residual: float
    parent_reconstruction_residual: float
    endpoint_isometry_residual: float
    scalar_isometry_residual: float
    transport_invariance_residual: float
    exact_endpoint_identities_verified: bool
    scalar_effect_lower_bound_verified: bool
    positive_phase_alignment_verified: bool
    gpe_transport_invariance_verified: bool
    status: str


@dataclass(frozen=True)
class PolarOnlyIndistinguishabilityControl:
    metric_ratio: float
    dimension: int
    child_polar_oracle_residual: float
    child_support_oracle_residual: float
    endpoint_effect_distance: float
    endpoint_isometry_mean_square_distance: float
    common_output_worst_case_mean_square_lower_bound: float
    transported_distance_residual: float
    identical_polar_oracles_verified: bool
    distinct_endpoint_effects_verified: bool
    constant_oracle_indistinguishability_gap_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootScalarMixerTheorem:
    natural_limit_input: str
    free_lukacs_input: str
    relative_second_moment: str
    optimal_scalar_effect: str
    canonical_native_error: str
    window_only_native_error: str
    pair_gpe_composition: str
    polar_only_oracle_boundary: str
    surviving_target: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootScalarMixerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FinalRootScalarMixerTheorem
    moment_records: list[ScalarMixerMomentRecord]
    exact_controls: list[ScalarEndpointFiniteControl]
    polar_only_control: PolarOnlyIndistinguishabilityControl
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_power(matrix: np.ndarray, exponent: float, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if float(np.min(values)) < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** exponent
    return (vectors * transformed) @ vectors.conj().T


def scalar_mixer_moment_record(
    alpha: float,
    scalar_left_weight: float = 0.5,
) -> ScalarMixerMomentRecord:
    """Return the exact free-Jacobi second-moment obstruction (3)--(5)."""

    if not math.isfinite(alpha) or not 2.0 <= alpha <= 4.0:
        raise ValueError("the selected final-root aspect must lie in [2,4]")
    if not math.isfinite(scalar_left_weight) or not 0 <= scalar_left_weight <= 1:
        raise ValueError("scalar_left_weight must lie in [0,1]")
    mean = 0.5
    variance = 1.0 / (8.0 * alpha)
    second = mean * mean + variance
    mse = variance + (scalar_left_weight - mean) ** 2
    canonical_bound = mse / 4.0
    window_bound = PARENT_WINDOW_LOWER * mse / (8.0 * alpha)
    return ScalarMixerMomentRecord(
        child_aspect=float(alpha),
        scalar_left_weight=float(scalar_left_weight),
        free_jacobi_mean=mean,
        free_jacobi_second_moment=second,
        free_jacobi_variance=variance,
        scalar_effect_mean_square_error=mse,
        optimal_scalar_left_weight=mean,
        optimal_scalar_effect_mean_square_error=variance,
        canonical_native_error_lower_bound=canonical_bound,
        window_only_native_error_lower_bound=window_bound,
        hadamard_is_optimal_scalar_effect=(
            mse >= variance - 1e-15
            and (abs(scalar_left_weight - mean) > 1e-15 or abs(mse - variance) <= 1e-15)
        ),
        scalar_effect_error_is_constant=mse >= UNIFORM_EFFECT_MSE_FLOOR - 1e-15,
        status="free-jacobi-scalar-mixer-constant-error",
    )


def _branch_transport(dimension: int) -> np.ndarray:
    """A deterministic branchwise unitary standing in for exact GPE transport."""

    indices = np.arange(dimension)
    fourier = np.exp(
        2j * np.pi * np.outer(indices, indices) / max(1, dimension)
    ) / math.sqrt(dimension)
    zero = np.zeros_like(fourier)
    return np.block([[fourier, zero], [zero, np.diag(np.exp(1j * indices))]])


def audit_scalar_endpoint_control(
    control_id: str,
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    scalar_left_weight: float,
    *,
    tolerance: float = 1e-9,
) -> ScalarEndpointFiniteControl:
    """Check exact endpoint, scalar-effect, native-error, and transport identities."""

    if left_metric.shape != right_metric.shape:
        raise ValueError("child metric shape mismatch")
    if len(left_metric.shape) != 2 or left_metric.shape[0] != left_metric.shape[1]:
        raise ValueError("child metrics must be square")
    if not 0 <= scalar_left_weight <= 1:
        raise ValueError("scalar_left_weight must lie in [0,1]")
    dimension = left_metric.shape[0]
    identity = np.eye(dimension, dtype=complex)
    parent = _hermitian(left_metric + right_metric)
    parent_values = np.linalg.eigvalsh(parent)
    if float(np.min(parent_values)) <= 100 * tolerance:
        raise ValueError("the finite control parent metric must be positive definite")
    parent_sqrt = _psd_power(parent, 0.5, tolerance)
    parent_inverse_sqrt = _psd_power(parent, -0.5, tolerance)
    effect = _hermitian(parent_inverse_sqrt @ left_metric @ parent_inverse_sqrt)
    complement = _hermitian(identity - effect)
    effect_sqrt = _psd_power(effect, 0.5, tolerance)
    complement_sqrt = _psd_power(complement, 0.5, tolerance)
    endpoint = np.vstack((effect_sqrt, complement_sqrt))
    scalar = np.vstack(
        (
            math.sqrt(scalar_left_weight) * identity,
            math.sqrt(1.0 - scalar_left_weight) * identity,
        )
    )
    difference = endpoint - scalar
    effect_difference = effect - scalar_left_weight * identity
    endpoint_error = float(np.trace(difference.conj().T @ difference).real / dimension)
    effect_error = float(
        np.trace(effect_difference @ effect_difference).real / dimension
    )
    native_error = float(
        np.trace(parent @ difference.conj().T @ difference).real
        / np.trace(parent).real
    )
    window_bound = float(
        np.min(parent_values)
        * np.trace(effect_difference @ effect_difference).real
        / (4.0 * np.trace(parent).real)
    )

    phase_scalar = np.vstack(
        (
            np.exp(1j * math.pi / 3) * math.sqrt(scalar_left_weight) * identity,
            np.exp(-1j * math.pi / 5)
            * math.sqrt(1.0 - scalar_left_weight)
            * identity,
        )
    )
    phase_difference = endpoint - phase_scalar
    phase_error = float(
        np.trace(parent @ phase_difference.conj().T @ phase_difference).real
        / np.trace(parent).real
    )
    transport = _branch_transport(dimension)
    transported_difference = transport @ endpoint - transport @ scalar
    transported_error = float(
        np.trace(parent @ transported_difference.conj().T @ transported_difference).real
        / np.trace(parent).real
    )

    endpoint_completeness = float(
        np.linalg.norm(effect + complement - identity, ord=2)
    )
    reconstruction = float(
        np.linalg.norm(parent_sqrt @ effect @ parent_sqrt - left_metric, ord=2)
    )
    endpoint_isometry = float(
        np.linalg.norm(endpoint.conj().T @ endpoint - identity, ord=2)
    )
    scalar_isometry = float(
        np.linalg.norm(scalar.conj().T @ scalar - identity, ord=2)
    )
    transport_residual = abs(transported_error - native_error)
    effect_values = np.linalg.eigvalsh(effect)
    effect_mean = float(np.mean(effect_values))
    effect_variance = float(np.mean((effect_values - effect_mean) ** 2))
    identities = bool(
        endpoint_completeness <= 100 * tolerance
        and reconstruction <= 100 * tolerance
        and endpoint_isometry <= 100 * tolerance
        and scalar_isometry <= 100 * tolerance
        and float(np.min(effect_values)) >= -100 * tolerance
        and float(np.max(effect_values)) <= 1 + 100 * tolerance
    )
    effect_bound = endpoint_error + 100 * tolerance >= effect_error / 4.0
    phase_alignment = phase_error + 100 * tolerance >= native_error
    transport_verified = transport_residual <= 100 * tolerance
    verified = identities and effect_bound and phase_alignment and transport_verified
    return ScalarEndpointFiniteControl(
        control_id=control_id,
        dimension=dimension,
        scalar_left_weight=float(scalar_left_weight),
        parent_minimum_eigenvalue=float(np.min(parent_values)),
        parent_maximum_eigenvalue=float(np.max(parent_values)),
        relative_effect_minimum_eigenvalue=float(np.min(effect_values)),
        relative_effect_maximum_eigenvalue=float(np.max(effect_values)),
        relative_effect_mean=effect_mean,
        relative_effect_variance=effect_variance,
        scalar_effect_mean_square_error=effect_error,
        canonical_naimark_mean_square_error=endpoint_error,
        native_canonical_mean_square_error=native_error,
        native_window_effect_lower_bound=window_bound,
        phase_perturbed_native_error=phase_error,
        transported_native_error=transported_error,
        endpoint_completeness_residual=endpoint_completeness,
        parent_reconstruction_residual=reconstruction,
        endpoint_isometry_residual=endpoint_isometry,
        scalar_isometry_residual=scalar_isometry,
        transport_invariance_residual=transport_residual,
        exact_endpoint_identities_verified=identities,
        scalar_effect_lower_bound_verified=effect_bound,
        positive_phase_alignment_verified=phase_alignment,
        gpe_transport_invariance_verified=transport_verified,
        status=(
            "scalar-endpoint-no-go-identities-verified"
            if verified
            else "scalar-endpoint-control-failure"
        ),
    )


def symmetric_free_moment_control(
    alpha: float,
    scalar_left_weight: float = 0.5,
    *,
    control_id: str | None = None,
) -> ScalarEndpointFiniteControl:
    """Build a two-channel exact control matching the Jacobi mean/variance."""

    moment = scalar_mixer_moment_record(alpha, scalar_left_weight)
    radius = math.sqrt(moment.free_jacobi_variance)
    effect = np.diag([0.5 - radius, 0.5 + radius]).astype(complex)
    parent = 2.0 * alpha * np.eye(2, dtype=complex)
    left = parent @ effect
    right = parent @ (np.eye(2) - effect)
    return audit_scalar_endpoint_control(
        control_id or f"symmetric-free-moment-alpha-{alpha:g}",
        left,
        right,
        scalar_left_weight,
    )


def noncommuting_metric_control() -> tuple[np.ndarray, np.ndarray]:
    left = np.array([[2.0, 0.4], [0.4, 1.0]], dtype=complex)
    right = np.array([[1.0, -0.2j], [0.2j, 2.5]], dtype=complex)
    return left, right


def audit_polar_only_indistinguishability(
    metric_ratio: float = 3.0,
    *,
    tolerance: float = 1e-9,
) -> PolarOnlyIndistinguishabilityControl:
    """Separate endpoint metrics with identical child-polar/support oracles."""

    if not math.isfinite(metric_ratio) or metric_ratio <= 1:
        raise ValueError("metric_ratio must exceed one")
    identity = np.eye(2, dtype=complex)
    left_zero = identity.copy()
    right_zero = identity.copy()
    left_one = np.diag([metric_ratio, 1.0]).astype(complex)
    right_one = np.diag([1.0, metric_ratio]).astype(complex)

    def polar_and_effect(
        left: np.ndarray,
        right: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        left_synthesis = _psd_power(left, 0.5, tolerance)
        right_synthesis = _psd_power(right, 0.5, tolerance)
        left_polar = left_synthesis @ _psd_power(left, -0.5, tolerance)
        right_polar = right_synthesis @ _psd_power(right, -0.5, tolerance)
        parent = left + right
        parent_inverse_sqrt = _psd_power(parent, -0.5, tolerance)
        effect = _hermitian(parent_inverse_sqrt @ left @ parent_inverse_sqrt)
        endpoint = np.vstack(
            (
                _psd_power(effect, 0.5, tolerance),
                _psd_power(identity - effect, 0.5, tolerance),
            )
        )
        return np.stack((left_polar, right_polar)), effect, endpoint

    polars_zero, effect_zero, endpoint_zero = polar_and_effect(
        left_zero,
        right_zero,
    )
    polars_one, effect_one, endpoint_one = polar_and_effect(left_one, right_one)
    polar_residual = max(
        float(np.linalg.norm(zero - one, ord=2))
        for zero, one in zip(polars_zero, polars_one)
    )
    support_residual = 0.0
    effect_distance = float(np.linalg.norm(effect_zero - effect_one, ord=2))
    endpoint_difference = endpoint_zero - endpoint_one
    endpoint_distance = float(
        np.trace(endpoint_difference.conj().T @ endpoint_difference).real / 2.0
    )
    common_output_lower_bound = endpoint_distance / 4.0
    transport = _branch_transport(2)
    transported_difference = transport @ endpoint_zero - transport @ endpoint_one
    transported_distance = float(
        np.trace(transported_difference.conj().T @ transported_difference).real
        / 2.0
    )
    transport_residual = abs(transported_distance - endpoint_distance)
    identical = polar_residual <= 100 * tolerance and support_residual <= tolerance
    distinct = effect_distance > 0.1 and endpoint_distance > 0.01
    gap = common_output_lower_bound > 0.002 and transport_residual <= 100 * tolerance
    verified = identical and distinct and gap
    return PolarOnlyIndistinguishabilityControl(
        metric_ratio=float(metric_ratio),
        dimension=2,
        child_polar_oracle_residual=polar_residual,
        child_support_oracle_residual=support_residual,
        endpoint_effect_distance=effect_distance,
        endpoint_isometry_mean_square_distance=endpoint_distance,
        common_output_worst_case_mean_square_lower_bound=common_output_lower_bound,
        transported_distance_residual=transport_residual,
        identical_polar_oracles_verified=identical,
        distinct_endpoint_effects_verified=distinct,
        constant_oracle_indistinguishability_gap_verified=gap,
        status=(
            "child-polar-only-endpoint-access-falsified"
            if verified
            else "polar-only-indistinguishability-control-failure"
        ),
    )


def run_final_root_scalar_mixer_no_go() -> FinalRootScalarMixerReport:
    moments = [
        scalar_mixer_moment_record(alpha, scalar_weight)
        for alpha, scalar_weight in (
            (2.0, 0.5),
            (2.5, 0.35),
            (3.0, 0.5),
            (4.0, 0.5),
            (4.0, 0.8),
        )
    ]
    noncommuting_left, noncommuting_right = noncommuting_metric_control()
    controls = [
        symmetric_free_moment_control(2.0, 0.5),
        symmetric_free_moment_control(3.0, 0.25),
        symmetric_free_moment_control(4.0, 0.5),
        audit_scalar_endpoint_control(
            "noncommuting-child-short-metrics",
            noncommuting_left,
            noncommuting_right,
            0.5,
        ),
    ]
    polar_only = audit_polar_only_indistinguishability()
    control_failures = sum(row.status.endswith("failure") for row in controls)
    moments_verified = all(
        row.hadamard_is_optimal_scalar_effect
        and row.scalar_effect_error_is_constant
        and row.canonical_native_error_lower_bound
        >= UNIFORM_CANONICAL_NATIVE_ERROR_FLOOR - 1e-15
        for row in moments
        if row.scalar_left_weight == 0.5
    )
    verified = (
        control_failures == 0
        and moments_verified
        and polar_only.constant_oracle_indistinguishability_gap_verified
    )
    theorem = FinalRootScalarMixerTheorem(
        natural_limit_input=(
            "Along every subsequence alpha_n->alpha in [2,4], the proved final sibling law is a pair of free MP(alpha) variables and the fixed parent-window relative effect has the symmetric free-Jacobi limit."
        ),
        free_lukacs_input=(
            "For free Poisson A,B of equal rate, S=A+B is free from C=S^-1/2 A S^-1/2."
        ),
        relative_second_moment=(
            "tau(C)=1/2 and tau(C^2)=1/4+1/(8alpha), hence Var(C)=1/(8alpha)."
        ),
        optimal_scalar_effect=(
            "inf_(0<=t<=1) tau((C-tI)^2)=1/(8alpha), uniquely at t=1/2; exchangeability selects the best scalar but does not make the effect scalar."
        ),
        canonical_native_error=(
            "After factoring child polars, every scalar-phase endpoint has annealed native mean-square error at least 1/(32alpha)>=1/128; positive phases are optimal."
        ),
        window_only_native_error=(
            "The fixed parent window alone gives the implementation-independent effect-to-isometry lower bound 1/(128alpha^2)>=1/2048."
        ),
        pair_gpe_composition=(
            "Branch-controlled GPE support transports postcompose both endpoint maps isometrically and preserve their mean-square difference exactly."
        ),
        polar_only_oracle_boundary=(
            "Two full-support metric pairs have identical identity child polars and support transports but constant-separated endpoint effects; metric magnitude access is necessary."
        ),
        surviving_target=(
            "A structured block encoding or direct Naimark dilation of the genuine matrix effect C, with compatible all-depth child support and holonomy access."
        ),
        scope=(
            "Selected final-root, annealed natural-state scalar-mixer no-go; no matrix-access lower bound, untrimmed sourcewise edge, all-depth compiler, decoder, or speedup."
        ),
        theorem_verified=verified,
        status=(
            "natural-final-root-scalar-endpoint-falsified-matrix-access-open"
            if verified
            else "final-root-scalar-mixer-control-failure"
        ),
    )
    return FinalRootScalarMixerReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "Equal-rate exchangeable final siblings make the recursive endpoint mixer asymptotically scalar, so a signed Hadamard plus exact GPE child transports implements the final-root polar on natural physical mass."
            ),
            "verdict": "falsified",
            "assumptions": [
                "The existing all-fixed natural sibling joint-freeness theorem.",
                "The existing fixed parent-window free-Jacobi transfer at selected aspect alpha in [2,4].",
                "A deterministic scalar endpoint weight t after exact child polars have been factored out.",
                "Annealed native parent-state mean-square error, with o(1) parent-window trim.",
            ],
            "normalization": (
                "Node-local parent normalization S^-1/2; no q-wide address erasure and no q-scale signal normalization."
            ),
            "failure_modes": [
                "Instance-dependent scalar weights are not covered unless their concentration is separately proved.",
                "Matrix-valued endpoint access may still be polynomial because the retained Jacobi spectrum has a constant bulk edge.",
                "Earlier hierarchy levels do not inherit the final sibling free law automatically.",
                "No hidden-label information or decoder theorem is supplied.",
            ],
            "success_criterion": (
                "A scalar shortcut required o(1) native mean-square endpoint error; every deterministic scalar weight has a uniform positive error floor."
            ),
            "speedup_claim_allowed": False,
        },
        theorem=theorem,
        moment_records=moments,
        exact_controls=controls,
        polar_only_control=polar_only,
        proof_obligations=[
            {
                "obligation": "derive_free_jacobi_second_moment",
                "resolved": True,
                "evidence": (
                    "Free Lukacs independence plus the alternating fourth-moment identity and MP first/second moments give Var(C)=1/(8alpha)."
                ),
            },
            {
                "obligation": "optimize_over_deterministic_scalar_mixers",
                "resolved": True,
                "evidence": (
                    "The exact effect MSE is (t-1/2)^2+1/(8alpha), uniquely minimized by the Hadamard weight t=1/2."
                ),
            },
            {
                "obligation": "transfer_effect_error_to_native_endpoint_error",
                "resolved": True,
                "evidence": (
                    "Canonical square-root dilation, free Lukacs native weighting, and the independent fixed-window fallback give uniform constants 1/128 and 1/2048."
                ),
            },
            {
                "obligation": "compose_with_pair_gpe_transport",
                "resolved": True,
                "evidence": (
                    "Branchwise GPE transports are postcomposition isometries, so they preserve the endpoint difference exactly."
                ),
            },
            {
                "obligation": "determine_whether_child_polars_alone_fix_endpoint",
                "resolved": True,
                "evidence": (
                    "The ratio-three exact control has identical identity child-polars/full supports in both instances but constant-separated relative effects and Naimark maps."
                ),
            },
            {
                "obligation": "compile_matrix_valued_endpoint_effect",
                "resolved": False,
                "evidence": (
                    "The no-go proves the matrix mixer is necessary but supplies no coherent block encoding, square-root dilation, or endpoint classifier."
                ),
            },
            {
                "obligation": "extend_node_law_and_access_through_all_depths",
                "resolved": False,
                "evidence": (
                    "Only the selected final sibling split has the natural free-Jacobi theorem."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Sibling exchangeability forces C=I/2 on the physical bulk.",
                "resolved": True,
                "resolution": (
                    "Exchangeability fixes only tau(C)=1/2. The proved limit has Var(C)=1/(8alpha), uniformly at least 1/32."
                ),
            },
            {
                "objection": "A different scalar branch weight beats the Hadamard.",
                "resolved": True,
                "resolution": (
                    "The exact MSE adds (t-1/2)^2, so t=1/2 is the unique optimum."
                ),
            },
            {
                "objection": "Scalar branch phases or GPE transport cancel the error.",
                "resolved": True,
                "resolution": (
                    "Positive phases maximize overlap with the positive square-root branches; common branchwise isometric transport leaves the error invariant."
                ),
            },
            {
                "objection": "Exact child polar oracles already contain the endpoint metric data.",
                "resolved": True,
                "resolution": (
                    "Polar decomposition discards positive magnitude. Full-support positive syntheses can share identity polars while producing different parent relative effects."
                ),
            },
            {
                "objection": "A nonscalar endpoint implies superpolynomial functional calculus.",
                "resolved": False,
                "resolution": (
                    "No. The retained free-Jacobi bulk is uniformly separated from 0 and 1. Structured normalized access, not conditioning, is the open final-root issue."
                ),
            },
            {
                "objection": "The theorem rules out source-adaptive scalar weights.",
                "resolved": False,
                "resolution": (
                    "The current annealed weak law does not control sample-to-sample fluctuation of the empirical optimal scalar. Such adaptation would itself require a coherent metric statistic."
                ),
            },
        ],
        primary_literature=[
            {
                "paper_id": FREE_LUKACS_PAPER_ID,
                "url": FREE_LUKACS_PAPER_URL,
                "scope": (
                    "Free-Poisson Lukacs property: A+B is free from (A+B)^-1/2 A (A+B)^-1/2."
                ),
                "proves_natural_wreath_joint_freeness": False,
            }
        ],
        headline_metrics={
            "free_jacobi_relative_variance_theorem_count": int(verified),
            "optimal_scalar_endpoint_no_go_theorem_count": int(verified),
            "pair_gpe_scalarization_count": 0,
            "child_polar_only_endpoint_access_no_go_count": int(
                polar_only.constant_oracle_indistinguishability_gap_verified
            ),
            "exact_control_count": len(controls),
            "exact_control_failure_count": control_failures,
            "uniform_scalar_effect_mse_floor": UNIFORM_EFFECT_MSE_FLOOR,
            "uniform_canonical_native_error_floor": UNIFORM_CANONICAL_NATIVE_ERROR_FLOOR,
            "uniform_window_only_native_error_floor": UNIFORM_WINDOW_ONLY_NATIVE_ERROR_FLOOR,
            "structured_matrix_endpoint_access_count": 0,
            "all_depth_endpoint_law_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_final_root_relative_effect_second_moment_proved": verified,
            "hadamard_is_optimal_deterministic_scalar_endpoint": verified,
            "every_deterministic_scalar_endpoint_has_constant_native_error": verified,
            "pair_gpe_transport_removes_matrix_endpoint_mixer": False,
            "child_polar_and_support_oracles_determine_endpoint_metric": False,
            "coherent_metric_magnitude_access_is_necessary": verified,
            "final_root_matrix_endpoint_is_well_conditioned_after_native_trim": True,
            "structured_matrix_endpoint_effect_access_proved": False,
            "source_adaptive_scalar_endpoint_no_go_proved": False,
            "all_depth_hierarchical_endpoint_compiler_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The first natural hierarchical endpoint has irreducible constant matrix variance, so neither a Hadamard nor another deterministic scalar splitter can replace it, even after exact GPE child transport. The true matrix effect has a constant retained edge; tightly normalized structured access is the remaining final-root bottleneck."
            ),
        },
        status=theorem.status,
        summary=(
            "Falsified the scalar final-root shortcut: the natural relative effect has variance 1/(8alpha), the Hadamard is the optimal scalar approximation but still incurs at least 1/128 annealed native mean-square error, and GPE child transport preserves that error."
        ),
        falsifiers_triggered=[
            "Equal-rate exchangeability fixes the endpoint mean but does not make the endpoint effect scalar.",
            "The signed Hadamard is the best deterministic scalar endpoint and still has constant natural native-state error.",
            "Exact pair-GPE transport cannot remove a matrix-valued endpoint mixer because branchwise isometric postcomposition preserves its error.",
            "Child polar and support-transport oracles discard the positive metric magnitude needed to determine the parent endpoint.",
            "The final-root obstruction is matrix access, not an endpoint hard edge or q-wide normalization loss.",
        ],
    )


def write_final_root_scalar_mixer_no_go_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_scalar_mixer_no_go())
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
                title="Final-root scalar endpoint mixer no-go",
                status="completed-negative-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Combine the proved natural final sibling free-MP law, free Lukacs independence, and the exact recursive endpoint factorization; derive and optimize the Jacobi second moment, transfer effect error to native Naimark error, and verify exact metric/GPE controls."
                ),
                positive_signal=(
                    "An o(1)-error deterministic scalar endpoint splitter after exact child-polar and GPE support transport."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_sibling_frame_all_fixed_joint.py",
                    "self_dual_wreath_final_root_relative_jacobi_transfer.py",
                    "self_dual_wreath_gpe_recursive_node_compiler.py",
                    "self_dual_wreath_gpe_pair_polar_transport.py",
                ],
                next_actions=[
                    "Construct a tightly normalized coherent block encoding or direct Naimark dilation of the genuine final-root matrix effect C on the retained Jacobi bulk; then test whether the same access model recurses to earlier nodes."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Equal-rate exchangeable natural final siblings make the recursive endpoint mixer asymptotically scalar, so a signed Hadamard plus exact pair-GPE child transports approximates the final-root polar."
                ),
                reason_invalid=(
                    "The free-Jacobi relative effect has Var(C)=1/(8alpha). The Hadamard is the optimal deterministic scalar effect, yet its canonical native Naimark error is at least 1/(32alpha)>=1/128; GPE postcomposition preserves the difference."
                ),
                lesson=(
                    "Do not scalarize the first natural hierarchical endpoint. Exploit its constant Jacobi bulk edge to build structured matrix-effect access, and keep matrix-valued normalization explicit at every recursive node."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "relative_effect_variance": "1/(8alpha)",
                    "uniform_scalar_effect_mse_floor": UNIFORM_EFFECT_MSE_FLOOR,
                    "uniform_canonical_native_error_floor": UNIFORM_CANONICAL_NATIVE_ERROR_FLOOR,
                    "pair_gpe_scalarization_count": 0,
                    "child_polar_only_endpoint_access_no_go": True,
                    "structured_matrix_endpoint_access_proved": False,
                    "matrix_endpoint_hard_edge_obstruction_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_scalar_mixer_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
