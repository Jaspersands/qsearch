"""Low-rank implicit-contraction search for iid DCP frequency localization."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.optimize import linprog

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_LOW_RANK_CONTRACTION_PATH = Path("research/classical_baselines/dcp_low_rank_contraction_search.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class LowRankContractionRow:
    n_bits: int
    modulus: int
    bucket_count: int
    bucket_size: int
    degree: int
    dictionary_id: str
    requested_rank: int
    effective_rank: int
    maximum_bandwidth: int
    lp_success: bool
    normalized_margin: float
    threshold: float
    coefficient_l1_norm: float
    coefficient_l2_norm: float
    active_component_count: int
    response_fit_mse: float
    minimum_record_count: int | None
    log2_minimum_record_count: float | None
    worst_instance_variance_at_minimum: float | None
    target_mse: float | None
    precision_bits_from_margin: int | None
    contraction_operation_estimate: int | None
    polynomial_sample_budget: int
    polynomial_rank_budget: int
    polynomial_precision_budget: int
    polynomial_samples: bool
    polynomial_rank: bool
    polynomial_precision: bool
    polynomial_contraction_operations: bool
    runtime_materializes_modulus_spectrum: bool
    joint_polynomial_survivor: bool
    falsifier: str


@dataclass(frozen=True)
class DictionaryRecord:
    dictionary_id: str
    feature_description: str
    evaluator_description: str
    query_model: str
    hidden_cost_risk: str


@dataclass(frozen=True)
class DCPLowRankContractionReport:
    created_at: str
    search_contract: dict[str, str]
    dictionaries: list[DictionaryRecord]
    rows: list[LowRankContractionRow]
    headline_metrics: dict[str, int | float]
    scaling_fits: dict[str, float | int | str]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _fejer_response(modulus: int, center: float, bandwidth: int) -> np.ndarray:
    points = np.arange(modulus, dtype=np.float64)
    angles = np.pi * (points - center) / modulus
    denominator = np.sin(angles)
    response = np.ones(modulus, dtype=np.float64)
    mask = np.abs(denominator) > 1e-14
    response[mask] = (
        np.sin(bandwidth * angles[mask]) / (bandwidth * denominator[mask])
    ) ** 2
    return response


def _unique_bandwidths(maximum: int, count: int) -> list[int]:
    if count <= 1 or maximum <= 1:
        return [1]
    values = np.geomspace(1, maximum, num=count)
    return sorted({max(1, min(maximum, int(round(value)))) for value in values})


def build_response_dictionary(
    n_bits: int,
    bucket_count: int,
    rank: int,
    dictionary_id: str,
) -> tuple[np.ndarray, int]:
    """Build public response features F_l(d) with closed-form label weights."""
    if n_bits < 2 or rank < 1:
        raise ValueError("require n_bits>=2 and rank>=1")
    modulus = 1 << n_bits
    if bucket_count < 2 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n and be at least 2")
    bucket_size = modulus // bucket_count
    center = (bucket_size - 1) / 2.0
    points = np.arange(modulus, dtype=np.float64)

    if dictionary_id == "cosine-low-frequency":
        frequencies = list(range(rank))
        features = [np.cos(2.0 * np.pi * frequency * (points - center) / modulus) for frequency in frequencies]
        return np.column_stack(features), max(frequencies, default=0)

    maximum_bandwidth = min(modulus // 2, max(bucket_count, bucket_count * rank))
    bandwidths = _unique_bandwidths(maximum_bandwidth, rank)
    fejer = [_fejer_response(modulus, center, bandwidth) for bandwidth in bandwidths]
    if dictionary_id == "fejer-multiscale":
        return np.column_stack(fejer), max(bandwidths)

    if dictionary_id == "hybrid-fejer-cosine":
        fejer_count = max(1, rank // 2)
        cosine_count = max(1, rank - fejer_count)
        bandwidths = _unique_bandwidths(maximum_bandwidth, fejer_count)
        fejer = [_fejer_response(modulus, center, bandwidth) for bandwidth in bandwidths]
        cosine = [
            np.cos(2.0 * np.pi * frequency * (points - center) / modulus)
            for frequency in range(cosine_count)
        ]
        return np.column_stack([*fejer, *cosine]), max(max(bandwidths), cosine_count - 1)

    raise ValueError(f"unknown dictionary_id: {dictionary_id}")


def optimize_uniform_margin(features: np.ndarray, degree: int, bucket_size: int) -> tuple[np.ndarray, float, float, bool]:
    """Maximize the worst-point bucket margin under ||c||_1<=1."""
    if degree < 1 or not 0 < bucket_size < features.shape[0]:
        raise ValueError("invalid degree or bucket_size")
    powered = np.asarray(features, dtype=np.float64) ** degree
    modulus, rank = powered.shape
    # Variables are c_plus, c_minus, threshold, margin.
    objective = np.zeros(2 * rank + 2, dtype=np.float64)
    objective[-1] = -1.0
    constraints: list[np.ndarray] = []
    bounds_rhs: list[float] = []
    for index in range(modulus):
        row = np.zeros(2 * rank + 2, dtype=np.float64)
        sign = 1.0 if index < bucket_size else -1.0
        # sign * (G c - threshold) >= margin.
        row[:rank] = -sign * powered[index]
        row[rank : 2 * rank] = sign * powered[index]
        row[-2] = sign
        row[-1] = 1.0
        constraints.append(row)
        bounds_rhs.append(0.0)
    l1_row = np.zeros(2 * rank + 2, dtype=np.float64)
    l1_row[: 2 * rank] = 1.0
    constraints.append(l1_row)
    bounds_rhs.append(1.0)
    result = linprog(
        objective,
        A_ub=np.vstack(constraints),
        b_ub=np.asarray(bounds_rhs),
        bounds=[(0.0, None)] * (2 * rank) + [(-1.0, 1.0), (0.0, 1.0)],
        method="highs",
    )
    if not result.success:
        return np.zeros(rank), 0.0, 0.0, False
    coefficients = result.x[:rank] - result.x[rank : 2 * rank]
    return coefficients, float(result.x[-2]), max(0.0, float(result.x[-1])), True


def _projection_variances(
    features: np.ndarray,
    coefficients: np.ndarray,
    degree: int,
) -> np.ndarray:
    """Return sigma_s^2(d) for every hidden d and Hoeffding order s."""
    modulus, rank = features.shape
    gram = features.T @ features
    variances = np.zeros((modulus, degree), dtype=np.float64)
    for hidden in range(modulus):
        base = features[hidden]
        covariance = 4.0 * gram - np.outer(base, base)
        for order in range(1, degree + 1):
            vector = coefficients * (base ** (degree - order))
            covariance_power = covariance**order
            value = float(vector @ covariance_power @ vector)
            variances[hidden, order - 1] = max(0.0, value)
    return variances


def _maximum_ustatistic_variance(projection_variances: np.ndarray, degree: int, records: int) -> float:
    coefficients = np.asarray(
        [math.comb(degree, order) ** 2 / math.comb(records, order) for order in range(1, degree + 1)],
        dtype=np.float64,
    )
    return float(np.max(projection_variances @ coefficients))


def minimum_records_for_variance(
    projection_variances: np.ndarray,
    degree: int,
    target_mse: float,
    maximum_records: int = 1 << 60,
) -> tuple[int | None, float | None]:
    """Find the least m with worst-instance exact U-statistic variance <= target."""
    if target_mse <= 0.0:
        return None, None
    low = degree
    high = degree
    while _maximum_ustatistic_variance(projection_variances, degree, high) > target_mse:
        if high >= maximum_records:
            return None, None
        high = min(maximum_records, high * 2)
    while low < high:
        middle = (low + high) // 2
        if _maximum_ustatistic_variance(projection_variances, degree, middle) <= target_mse:
            high = middle
        else:
            low = middle + 1
    return low, _maximum_ustatistic_variance(projection_variances, degree, low)


def evaluate_low_rank_contraction(
    n_bits: int,
    degree: int,
    rank: int,
    dictionary_id: str,
    bucket_count: int | None = None,
    sample_budget_power: int = 3,
    rank_budget_power: int = 2,
    precision_budget_power: int = 2,
) -> LowRankContractionRow:
    modulus = 1 << n_bits
    resolved_bucket_count = bucket_count or (1 << min(n_bits - 1, math.ceil(math.log2(n_bits))))
    features, maximum_bandwidth = build_response_dictionary(
        n_bits,
        resolved_bucket_count,
        rank,
        dictionary_id,
    )
    effective_rank = features.shape[1]
    bucket_size = modulus // resolved_bucket_count
    coefficients, threshold, margin, lp_success = optimize_uniform_margin(features, degree, bucket_size)
    powered = features**degree
    response = powered @ coefficients
    labels = np.full(modulus, -1.0)
    labels[:bucket_size] = 1.0
    fitted_target = threshold + labels * margin
    fit_mse = float(np.mean((response - fitted_target) ** 2))
    l1 = float(np.sum(np.abs(coefficients)))
    l2 = float(np.linalg.norm(coefficients))
    active = int(np.sum(np.abs(coefficients) > 1e-9))
    sample_budget = n_bits**sample_budget_power
    rank_budget = n_bits**rank_budget_power
    precision_budget = n_bits**precision_budget_power

    minimum_records: int | None = None
    worst_variance: float | None = None
    target_mse: float | None = None
    precision_bits: int | None = None
    operations: int | None = None
    if lp_success and margin > 1e-12 and active > 0:
        projection_variances = _projection_variances(features, coefficients, degree)
        target_mse = margin * margin / 4.0
        minimum_records, worst_variance = minimum_records_for_variance(
            projection_variances,
            degree,
            target_mse,
        )
        precision_bits = max(1, math.ceil(-math.log2(margin)))
        if minimum_records is not None:
            operations = (
                resolved_bucket_count * active * degree * minimum_records
            )

    polynomial_samples = minimum_records is not None and minimum_records <= sample_budget
    polynomial_rank = active <= rank_budget
    polynomial_precision = precision_bits is not None and precision_bits <= precision_budget
    polynomial_operations = operations is not None and operations <= n_bits ** (sample_budget_power + rank_budget_power + 2)
    survivor = (
        lp_success
        and margin > 1e-12
        and polynomial_samples
        and polynomial_rank
        and polynomial_precision
        and polynomial_operations
    )
    if not lp_success or margin <= 1e-12:
        falsifier = "dictionary cannot uniformly separate every target and non-target frequency under the coefficient budget"
    elif not polynomial_samples:
        falsifier = "exact Hoeffding projection variance requires superpolynomial iid records"
    elif not polynomial_precision:
        falsifier = "uniform margin requires superpolynomial coefficient/decision precision"
    elif not polynomial_operations:
        falsifier = "bucket-by-rank contraction operation count is superpolynomial"
    else:
        falsifier = "none in implemented finite audit; requires asymptotic family proof and exact f=1/lattice composition"
    return LowRankContractionRow(
        n_bits=n_bits,
        modulus=modulus,
        bucket_count=resolved_bucket_count,
        bucket_size=bucket_size,
        degree=degree,
        dictionary_id=dictionary_id,
        requested_rank=rank,
        effective_rank=effective_rank,
        maximum_bandwidth=maximum_bandwidth,
        lp_success=lp_success,
        normalized_margin=margin,
        threshold=threshold,
        coefficient_l1_norm=l1,
        coefficient_l2_norm=l2,
        active_component_count=active,
        response_fit_mse=fit_mse,
        minimum_record_count=minimum_records,
        log2_minimum_record_count=math.log2(minimum_records) if minimum_records else None,
        worst_instance_variance_at_minimum=worst_variance,
        target_mse=target_mse,
        precision_bits_from_margin=precision_bits,
        contraction_operation_estimate=operations,
        polynomial_sample_budget=sample_budget,
        polynomial_rank_budget=rank_budget,
        polynomial_precision_budget=precision_budget,
        polynomial_samples=polynomial_samples,
        polynomial_rank=polynomial_rank,
        polynomial_precision=polynomial_precision,
        polynomial_contraction_operations=polynomial_operations,
        runtime_materializes_modulus_spectrum=False,
        joint_polynomial_survivor=survivor,
        falsifier=falsifier,
    )


def _dictionary_records() -> list[DictionaryRecord]:
    return [
        DictionaryRecord(
            dictionary_id="cosine-low-frequency",
            feature_description="low-frequency real characters centered on the target bucket",
            evaluator_description="each label weight has constant Fourier support and O(1) evaluation",
            query_model="iid random public labels only",
            hidden_cost_risk="uniform step separation may require high rank or exponentially small margin",
        ),
        DictionaryRecord(
            dictionary_id="fejer-multiscale",
            feature_description="multiscale positive Fejer kernels with polynomial bandwidth",
            evaluator_description="triangular compact Fourier support with closed-form O(1) coefficient lookup",
            query_model="iid random public labels only",
            hidden_cost_risk="localization energy and first projections may force exponential samples",
        ),
        DictionaryRecord(
            dictionary_id="hybrid-fejer-cosine",
            feature_description="joint multiscale localized and oscillatory response dictionary",
            evaluator_description="polynomial compact support and closed-form public-label weights",
            query_model="iid random public labels only",
            hidden_cost_risk="projection cancellation may require ill-conditioned coefficients or precision",
        ),
    ]


def run_low_rank_contraction_search(
    n_values: Sequence[int] = (6, 8, 10),
    degrees: Sequence[int] = (2, 4, 8),
    rank_multiplier: int = 2,
    dictionary_ids: Sequence[str] = (
        "cosine-low-frequency",
        "fejer-multiscale",
        "hybrid-fejer-cosine",
    ),
) -> DCPLowRankContractionReport:
    rows = [
        evaluate_low_rank_contraction(
            n_bits,
            degree,
            max(2, rank_multiplier * n_bits),
            dictionary_id,
        )
        for n_bits in n_values
        for degree in degrees
        if degree <= n_bits
        for dictionary_id in dictionary_ids
    ]
    separated = [row for row in rows if row.lp_success and row.normalized_margin > 1e-12]
    finite_logs = [row for row in separated if row.log2_minimum_record_count is not None]
    slopes: list[float] = []
    for dictionary_id in dictionary_ids:
        for degree in degrees:
            group = [
                row
                for row in finite_logs
                if row.dictionary_id == dictionary_id and row.degree == degree
            ]
            if len(group) >= 2:
                slope = float(
                    np.polyfit(
                        [row.n_bits for row in group],
                        [float(row.log2_minimum_record_count) for row in group],
                        1,
                    )[0]
                )
                slopes.append(slope)
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "uniform_separation_row_count": len(separated),
        "no_uniform_separation_row_count": len(rows) - len(separated),
        "superpolynomial_sample_row_count": sum(
            row.lp_success and row.normalized_margin > 1e-12 and not row.polynomial_samples for row in rows
        ),
        "superpolynomial_precision_row_count": sum(
            row.lp_success and row.normalized_margin > 1e-12 and not row.polynomial_precision for row in rows
        ),
        "superpolynomial_contraction_row_count": sum(
            row.lp_success and row.normalized_margin > 1e-12 and not row.polynomial_contraction_operations for row in rows
        ),
        "joint_polynomial_finite_survivor_count": sum(row.joint_polynomial_survivor for row in rows),
        "proved_uniform_low_rank_family_count": 0,
        "proved_exact_f1_robust_low_rank_decoder_count": 0,
        "proved_lattice_composition_count": 0,
        "runtime_modulus_spectrum_materialization_count": sum(row.runtime_materializes_modulus_spectrum for row in rows),
    }
    scaling = {
        "fit_count": len(slopes),
        "minimum_log2_sample_slope_per_n": min(slopes) if slopes else "unavailable",
        "maximum_log2_sample_slope_per_n": max(slopes) if slopes else "unavailable",
        "interpretation": "Positive slopes are finite evidence of exponential sample scaling, not asymptotic lower bounds.",
    }
    falsifiers = [
        "Low-rank response features that do not separate every discrete boundary point are rejected before variance claims.",
        "Every separating row is charged through all exact Hoeffding projection orders, not only the first projection.",
        "Polynomial tensor rank does not suffice when records, decision precision, or bucket-by-rank contraction work is superpolynomial.",
        "Finite survivors, if any, remain blocked until a uniform asymptotic family and exact f=1/lattice composition are proved.",
        "No runtime decoder may use the N-point analysis grid or an N-entry intermediate spectrum.",
    ]
    return DCPLowRankContractionReport(
        created_at=utc_now(),
        search_contract={
            "objective": "maximize worst-point target-bucket margin under coefficient L1 norm at most one",
            "variance": "exact all-orders Hoeffding covariance for the fitted sum of rank-one product kernels",
            "contraction": "O(B R r m) elementary-symmetric work across B candidate buckets",
            "access": "iid public DCP labels; all feature weights are closed-form and nonadaptive",
            "promotion": "requires polynomial samples, rank, precision, contraction operations, uniform asymptotics, f=1 robustness, and lattice composition",
        },
        dictionaries=_dictionary_records(),
        rows=rows,
        headline_metrics=metrics,
        scaling_fits=scaling,
        claim_gate={
            "finite_joint_polynomial_survivor_found": metrics["joint_polynomial_finite_survivor_count"] > 0,
            "uniform_low_rank_family_proved": False,
            "exact_f1_robust_decoder_proved": False,
            "lattice_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Finite low-rank contractions are only search evidence. Promotion requires a uniform resource theorem, "
                "adversarial contamination robustness, and exact composition to the lattice reduction."
            ),
        },
        status=(
            "finite-low-rank-survivor-needs-theorem"
            if metrics["joint_polynomial_finite_survivor_count"]
            else "tested-low-rank-dictionaries-falsified"
        ),
        summary=(
            f"Audited {len(rows)} low-rank contraction rows; uniform separators={len(separated)}, finite joint-polynomial "
            f"survivors={int(metrics['joint_polynomial_finite_survivor_count'])}, proved uniform families=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_low_rank_contraction_search(
    path: Path = DCP_LOW_RANK_CONTRACTION_PATH,
    n_values: Sequence[int] = (6, 8, 10),
    degrees: Sequence[int] = (2, 4, 8),
    rank_multiplier: int = 2,
    dictionary_ids: Sequence[str] = (
        "cosine-low-frequency",
        "fejer-multiscale",
        "hybrid-fejer-cosine",
    ),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_low_rank_contraction_search(
        n_values=n_values,
        degrees=degrees,
        rank_multiplier=rank_multiplier,
        dictionary_ids=dictionary_ids,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry and not payload["headline_metrics"]["joint_polynomial_finite_survivor_count"]:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-IID-TESTED-LOW-RANK-CONTRACTION-DICTIONARIES",
                source=str(path),
                claim="Standard polynomial-rank bandlimited or Fejer response contractions yield a polynomial DCP bucket decoder.",
                reason_invalid=(
                    "Every tested row either lacked a uniform discrete margin or failed exact Hoeffding sample, precision, "
                    "or contraction-operation accounting. No finite joint-polynomial survivor remained."
                ),
                lesson=(
                    "Do not retry these dictionaries without a new projection-cancellation mechanism. Search structured "
                    "tensor networks or algebraic kernels and keep the exact all-order variance gate."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
    if write_registry:
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-LOW-RANK-CONTRACTION"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_low_rank_contraction_search": str(path)},
            )
        )
    return payload
