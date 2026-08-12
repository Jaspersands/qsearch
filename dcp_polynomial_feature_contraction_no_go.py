"""Polynomial-feature signed-contraction no-go for iid DCP records.

This module closes the polynomial-rank extension left open by the rank-one
factorized-contraction audit.  Work in a real (or realified complex) feature
space of dimension ``R``.  For hidden shift ``d``, one local measured record
has feature vector ``Z_d`` with

    E[Z_d] = F_d,
    Cov(Z_d) = 4 A - F_d F_d^T,
    A = sum_u F_u F_u^T.                               (1)

Equation (1) is the Fourier/Parseval covariance contract used by the existing
DCP factorized-observable model.

Let ``T`` be any symmetric degree-``r`` multilinear form and let the complete
U-statistic average ``T`` over all distinct ``r``-subsets of ``m`` iid records.
Its response and response gradient are

    H_d = T(F_d,...,F_d),
    g_d = grad H(F_d),

so Euler's identity gives ``g_d^T F_d = r H_d``.  The first Hoeffding
projection contributes exactly

    (1/m) g_d^T Cov(Z_d) g_d                           (2)

to the estimator variance.

Suppose ``|H_d| >= gamma`` on a set ``C`` of ``L`` hidden shifts.  Form the
``L x L`` matrix ``M[d,u]=g_d^T F_u``.  It has rank at most ``R`` and diagonal
magnitude at least ``r gamma``.  Rotate rows to make the diagonal positive.
The trace/nuclear/Frobenius inequalities imply

    ||M||_F^2 >= L^2 r^2 gamma^2 / R.

Some row therefore has squared norm at least ``L r^2 gamma^2/R``.  Equation
(1) then gives, for that hidden shift,

    g_d^T Cov(Z_d) g_d >= 3 L r^2 gamma^2 / R.          (3)

Uniform mean-squared error at most ``gamma^2/4`` requires

    m >= 12 L r^2 / R.                                 (4)

If ``R=poly(n)`` and a robust response covers ``L=2^n/poly(n)`` shifts, the
record requirement is exponential.  The theorem covers arbitrary signed
coefficients and cancellation among polynomially many product components; it
does not cover biased estimators without the MSE contract, adaptive/sequential
measurements, exponentially large local feature spaces hidden behind an
oracle, or entangled collective quantum measurements.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/classical_baselines/dcp_polynomial_feature_contraction_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-POLYNOMIAL-FEATURE-CONTRACTION-NO-GO"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class FeatureRankTraceControl:
    control_id: str
    hidden_count: int
    feature_rank: int
    degree: int
    response_support_size: int
    response_margin: float
    response_gradient_euler_residual: float
    gradient_response_matrix_rank: int
    gradient_response_matrix_frobenius_squared: float
    trace_rank_lower_bound: float
    maximum_class_row_energy: float
    row_energy_lower_bound: float
    maximum_first_projection_variance: float
    first_projection_variance_lower_bound: float
    covariance_minimum_eigenvalue: float
    trace_rank_inequality_verified: bool
    first_projection_inequality_verified: bool
    status: str


@dataclass(frozen=True)
class PolynomialFeatureScalingRecord:
    n_bits: int
    degree_power: int
    degree: int
    feature_rank_power: int
    feature_rank_log2: float
    response_coverage_power: int
    response_support_log2_lower_bound: float
    log2_record_lower_bound: float
    polynomial_record_budget_power: int
    log2_polynomial_record_budget: float
    polynomial_records_possible: bool
    status: str


@dataclass(frozen=True)
class PolynomialFeatureContractionTheorem:
    record_covariance_contract: str
    estimator_class: str
    euler_identity: str
    first_projection_identity: str
    rank_trace_lemma: str
    variance_lower_bound: str
    record_lower_bound: str
    polynomial_rank_consequence: str
    arbitrary_symmetric_multilinear_form: bool
    arbitrary_signed_coefficients: bool
    polynomial_rank_component_cancellation_covered: bool
    inverse_polynomial_response_support_closed: bool
    adaptive_estimators_closed: bool
    collective_quantum_measurements_closed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPPolynomialFeatureContractionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FeatureRankTraceControl]
    scaling_records: list[PolynomialFeatureScalingRecord]
    theorem: PolynomialFeatureContractionTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def trace_rank_frobenius_lower_bound(
    diagonal_magnitudes: Sequence[float],
    rank_upper_bound: int,
) -> float:
    if len(diagonal_magnitudes) == 0 or rank_upper_bound < 1:
        raise ValueError("a nonempty diagonal and positive rank are required")
    if any(value < 0 for value in diagonal_magnitudes):
        raise ValueError("diagonal magnitudes must be nonnegative")
    return sum(diagonal_magnitudes) ** 2 / rank_upper_bound


def polynomial_feature_record_lower_bound(
    response_support_size: int,
    degree: int,
    feature_rank: int,
) -> float:
    if min(response_support_size, degree, feature_rank) < 1:
        raise ValueError("support, degree, and feature rank must be positive")
    return 12.0 * response_support_size * degree * degree / feature_rank


def _diagonal_power_response(
    features: np.ndarray,
    coefficients: np.ndarray,
    degree: int,
) -> tuple[np.ndarray, np.ndarray]:
    if features.ndim != 2 or coefficients.shape != (features.shape[1],):
        raise ValueError("feature and coefficient dimensions do not match")
    if degree < 1:
        raise ValueError("degree must be positive")
    responses = np.sum(coefficients[None, :] * features**degree, axis=1)
    gradients = (
        degree
        * coefficients[None, :]
        * features ** max(0, degree - 1)
    )
    return responses, gradients


def audit_feature_rank_trace_control(
    control_id: str,
    hidden_count: int,
    feature_rank: int,
    degree: int,
    response_support_size: int,
    *,
    seed: int,
    tolerance: float = 1e-9,
) -> FeatureRankTraceControl:
    if hidden_count < 2 or not 1 <= feature_rank <= hidden_count:
        raise ValueError("invalid hidden count or feature rank")
    if degree < 1 or not 1 <= response_support_size <= hidden_count:
        raise ValueError("invalid degree or response support size")
    rng = np.random.default_rng(seed)
    features = rng.normal(size=(hidden_count, feature_rank))
    coefficients = rng.normal(size=feature_rank)
    responses, gradients = _diagonal_power_response(
        features, coefficients, degree
    )
    support = np.argsort(np.abs(responses))[-response_support_size:]
    margin = float(np.min(np.abs(responses[support])))
    if margin <= tolerance:
        raise ArithmeticError("control response margin is numerically zero")

    class_features = features[support, :]
    class_gradients = gradients[support, :]
    matrix = class_gradients @ class_features.T
    diagonal = np.diag(matrix)
    euler_residual = float(
        np.max(np.abs(diagonal - degree * responses[support]))
    )
    matrix_rank = int(np.linalg.matrix_rank(matrix, tol=tolerance))
    frobenius_squared = float(np.linalg.norm(matrix, ord="fro") ** 2)
    trace_lower = trace_rank_frobenius_lower_bound(
        np.abs(diagonal), feature_rank
    )
    row_energies = np.sum(np.abs(matrix) ** 2, axis=1)
    maximum_row = float(np.max(row_energies))
    row_lower = (
        response_support_size * degree * degree * margin * margin / feature_rank
    )

    gram = features.T @ features
    projection_variances = []
    covariance_minima = []
    for hidden in support:
        vector = features[hidden]
        covariance = 4.0 * gram - np.outer(vector, vector)
        covariance_minima.append(float(np.min(np.linalg.eigvalsh(covariance))))
        gradient = gradients[hidden]
        projection_variances.append(float(gradient @ covariance @ gradient))
    maximum_variance = max(projection_variances)
    variance_lower = 3.0 * row_lower
    trace_verified = (
        matrix_rank <= feature_rank
        and euler_residual <= 100 * tolerance
        and frobenius_squared + 100 * tolerance >= trace_lower
        and maximum_row + 100 * tolerance >= row_lower
    )
    variance_verified = maximum_variance + 100 * tolerance >= variance_lower
    return FeatureRankTraceControl(
        control_id=control_id,
        hidden_count=hidden_count,
        feature_rank=feature_rank,
        degree=degree,
        response_support_size=response_support_size,
        response_margin=margin,
        response_gradient_euler_residual=euler_residual,
        gradient_response_matrix_rank=matrix_rank,
        gradient_response_matrix_frobenius_squared=frobenius_squared,
        trace_rank_lower_bound=trace_lower,
        maximum_class_row_energy=maximum_row,
        row_energy_lower_bound=row_lower,
        maximum_first_projection_variance=maximum_variance,
        first_projection_variance_lower_bound=variance_lower,
        covariance_minimum_eigenvalue=min(covariance_minima),
        trace_rank_inequality_verified=trace_verified,
        first_projection_inequality_verified=variance_verified,
        status=(
            "feature-rank-trace-variance-bound-verified"
            if trace_verified and variance_verified
            else "feature-rank-trace-control-failure"
        ),
    )


def scaling_record(
    n_bits: int,
    degree_power: int,
    feature_rank_power: int,
    response_coverage_power: int,
    polynomial_record_budget_power: int,
) -> PolynomialFeatureScalingRecord:
    if n_bits < 2 or min(
        degree_power,
        feature_rank_power,
        response_coverage_power,
        polynomial_record_budget_power,
    ) < 0:
        raise ValueError("invalid polynomial scaling parameters")
    degree = max(1, n_bits**degree_power)
    feature_rank_log2 = feature_rank_power * math.log2(n_bits)
    support_log2 = max(0.0, n_bits - response_coverage_power * math.log2(n_bits))
    record_log2 = (
        math.log2(12.0)
        + support_log2
        + 2 * math.log2(degree)
        - feature_rank_log2
    )
    budget_log2 = polynomial_record_budget_power * math.log2(n_bits)
    return PolynomialFeatureScalingRecord(
        n_bits=n_bits,
        degree_power=degree_power,
        degree=degree,
        feature_rank_power=feature_rank_power,
        feature_rank_log2=feature_rank_log2,
        response_coverage_power=response_coverage_power,
        response_support_log2_lower_bound=support_log2,
        log2_record_lower_bound=record_log2,
        polynomial_record_budget_power=polynomial_record_budget_power,
        log2_polynomial_record_budget=budget_log2,
        polynomial_records_possible=record_log2 <= budget_log2,
        status=(
            "polynomial-record-budget-not-excluded"
            if record_log2 <= budget_log2
            else "polynomial-feature-contraction-needs-superpolynomial-records"
        ),
    )


def polynomial_feature_contraction_theorem() -> PolynomialFeatureContractionTheorem:
    return PolynomialFeatureContractionTheorem(
        record_covariance_contract=(
            "E[Z_d]=F_d, Cov(Z_d)=4A-F_dF_d^T, and "
            "A=sum_u F_uF_u^T"
        ),
        estimator_class=(
            "complete U-statistic of an arbitrary symmetric degree-r "
            "multilinear form on an R-dimensional local feature vector"
        ),
        euler_identity="g_d^T F_d=r H_d",
        first_projection_identity=(
            "Var(U_m)>=m^-1 g_d^T Cov(Z_d) g_d"
        ),
        rank_trace_lemma=(
            "rank(M)<=R and |diag M|>=r gamma on L indices imply "
            "max_d sum_u |M_du|^2 >= L r^2 gamma^2/R"
        ),
        variance_lower_bound=(
            "some covered d has first-projection numerator at least "
            "3 L r^2 gamma^2/R"
        ),
        record_lower_bound="uniform MSE<=gamma^2/4 requires m>=12 L r^2/R",
        polynomial_rank_consequence=(
            "R=poly(n) and L=2^n/poly(n) force exponentially many iid records"
        ),
        arbitrary_symmetric_multilinear_form=True,
        arbitrary_signed_coefficients=True,
        polynomial_rank_component_cancellation_covered=True,
        inverse_polynomial_response_support_closed=True,
        adaptive_estimators_closed=False,
        collective_quantum_measurements_closed=False,
        theorem_verified=True,
        status="polynomial-feature-signed-contraction-record-lower-bound-proved",
    )


def run_polynomial_feature_contraction_no_go(
    n_values: Sequence[int] = (64, 128, 256, 512, 1024),
) -> DCPPolynomialFeatureContractionReport:
    controls = [
        audit_feature_rank_trace_control("quadratic-rank-two", 12, 2, 2, 6, seed=11),
        audit_feature_rank_trace_control("cubic-rank-three", 16, 3, 3, 8, seed=17),
        audit_feature_rank_trace_control("quartic-rank-five", 20, 5, 4, 10, seed=23),
    ]
    rows = [
        scaling_record(
            n_bits,
            degree_power=degree_power,
            feature_rank_power=feature_power,
            response_coverage_power=coverage_power,
            polynomial_record_budget_power=8,
        )
        for n_bits in n_values
        for degree_power in (0, 1)
        for feature_power in (2, 6)
        for coverage_power in (2, 8)
    ]
    theorem = polynomial_feature_contraction_theorem()
    failures = sum(
        not (
            row.trace_rank_inequality_verified
            and row.first_projection_inequality_verified
        )
        for row in controls
    )
    metrics: dict[str, int | float] = {
        "polynomial_feature_contraction_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "scaling_row_count": len(rows),
        "superpolynomial_record_row_count": sum(
            not row.polynomial_records_possible for row in rows
        ),
        "maximum_n_bits": max(n_values),
        "maximum_log2_record_lower_bound": max(
            row.log2_record_lower_bound for row in rows
        ),
        "proved_polynomial_rank_signed_contraction_lower_bound_count": 1,
        "proved_inverse_polynomial_support_contraction_lower_bound_count": 1,
        "proved_adaptive_estimator_lower_bound_count": 0,
        "proved_collective_measurement_lower_bound_count": 0,
        "polynomial_dcp_decoder_count": 0,
    }
    return DCPPolynomialFeatureContractionReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "iid measured DCP records satisfying the inherited vector "
                "Fourier/Parseval covariance identity"
            ),
            "estimator": (
                "unbiased complete symmetric multilinear U-statistic with "
                "local feature dimension R"
            ),
            "success": (
                "response magnitude at least gamma on L hidden shifts and "
                "uniform MSE at most gamma^2/4"
            ),
            "proved": "record lower bound m>=12 L r^2/R",
            "excluded": (
                "biased heavy-tail decisions, adaptive record processing, "
                "sequential sieves, and entangled collective measurements"
            ),
        },
        finite_controls=controls,
        scaling_records=rows,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-DCP-POLY-FEATURE-TRACE-RANK",
                "description": (
                    "Prove cancellation among arbitrary signed multilinear "
                    "components cannot suppress every first projection."
                ),
                "satisfied": True,
                "evidence": (
                    "the L-by-L gradient-response matrix has rank at most R; "
                    "its large diagonal forces Frobenius mass"
                ),
            },
            {
                "id": "PO-DCP-POLY-FEATURE-COVARIANCE",
                "description": (
                    "Transfer Frobenius row mass to measured-record variance."
                ),
                "satisfied": True,
                "evidence": (
                    "Cov=4A-F_dF_d^T and A=sum_u F_uF_u^T give the factor-three bound"
                ),
            },
            {
                "id": "PO-DCP-ADAPTIVE-SIGNED-SIEVE",
                "description": (
                    "Analyze adaptive or sequential contractions that do not "
                    "form a fixed-feature U-statistic."
                ),
                "satisfied": False,
                "evidence": "outside the estimator class",
            },
            {
                "id": "PO-DCP-COLLECTIVE-SIGNED-MEASUREMENT",
                "description": (
                    "Construct or lower-bound a coherent collective measurement "
                    "without reducing it to measured iid features."
                ),
                "satisfied": False,
                "evidence": "measurement before contraction is essential to the theorem",
            },
        ],
        adversarial_audit=[
            {
                "attack": "Cancel rank-one first projections with signed polynomial rank.",
                "survives": False,
                "reason": (
                    "large diagonal response forces Frobenius mass in the "
                    "rank-R gradient-response matrix despite cancellation"
                ),
            },
            {
                "attack": "Use a polynomially small but nonuniform covered set.",
                "survives": True,
                "reason": (
                    "the lower bound scales with L; it is exponential only when "
                    "coverage contains 2^n/poly(n) hidden shifts"
                ),
            },
            {
                "attack": "Use a biased or heavy-tailed threshold estimator with large MSE.",
                "survives": True,
                "reason": "the theorem imposes an explicit robust MSE contract",
            },
            {
                "attack": "Keep records coherent and perform an entangled measurement.",
                "survives": True,
                "reason": "the iid measured-feature covariance model no longer applies",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "rank_one_signed_contractions_closed": True,
            "polynomial_rank_signed_contractions_closed_under_mse_contract": True,
            "inverse_polynomial_hidden_support_closed_under_mse_contract": True,
            "low_bond_sequential_contractions_closed": False,
            "adaptive_estimators_closed": False,
            "collective_quantum_measurements_closed": False,
            "polynomial_dcp_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Polynomial signed feature rank cannot provide robust "
                "inverse-polynomial hidden-shift coverage with polynomially many "
                "measured iid records. A survivor must be adaptive, sequential, "
                "non-robust in a separately justified way, or genuinely collective."
            ),
        },
        status="polynomial-rank-iid-signed-contractions-obstructed",
        summary=(
            "Proved m>=12 L r^2/R for arbitrary signed degree-r symmetric "
            "multilinear U-statistics over R local features. This closes "
            "polynomial-rank iid contractions with inverse-polynomial hidden "
            "coverage under the robust MSE contract; adaptive and coherent "
            "collective routes remain open."
        ),
        falsifiers_triggered=[
            "Polynomially many signed rank-one components cannot cancel every first projection while retaining broad robust response.",
            "Efficient all-subsets contraction does not imply polynomial record complexity at polynomial feature rank.",
            "The lower bound is proportional to response-support size and does not reject exponentially sparse response sets.",
            "The theorem does not apply after retaining quantum coherence across records.",
        ],
    )


def write_polynomial_feature_contraction_no_go(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-POLYNOMIAL-FEATURE-CONTRACTION-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_polynomial_feature_contraction_no_go(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_polynomial_feature_contraction_no_go()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
