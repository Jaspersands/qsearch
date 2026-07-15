"""Parseval no-go audit for biased margin-separated linear DCP scores."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_BIASED_LINEAR_MARGIN_PATH = Path("research/classical_baselines/dcp_biased_linear_margin_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class MarginEnergyCertificate:
    n_bits: int
    modulus: int
    bucket_count: int
    bucket_size: int
    decision_margin: float
    optimal_inside_level: float
    optimal_outside_level: float
    optimal_threshold: float
    exact_minimum_energy: str
    log2_minimum_energy: float
    exact_uniform_mse_sample_lower_bound: int
    log2_sample_lower_bound: float
    polynomial_sample_budget: int
    polynomial_bucket_enumeration: bool
    polynomial_samples_ruled_out: bool
    joint_polynomial_resources_possible: bool
    proof_statement: str


@dataclass(frozen=True)
class FiniteMarginCheck:
    n_bits: int
    modulus: int
    bucket_count: int
    bucket_size: int
    decision_margin: float
    minimum_inside_gap: float
    minimum_outside_gap: float
    target_energy: float
    weight_second_moment: float
    theoretical_minimum_energy: float
    maximum_reconstruction_error: float
    parseval_error: float
    optimality_error: float


@dataclass(frozen=True)
class DCPBiasedLinearMarginReport:
    created_at: str
    estimator_model: dict[str, str]
    theorem: dict[str, str]
    certificates: list[MarginEnergyCertificate]
    finite_checks: list[FiniteMarginCheck]
    headline_metrics: dict[str, int | float]
    excluded_and_open_classes: dict[str, list[str]]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _as_fraction(value: float) -> Fraction:
    if not 0.0 < value <= 1.0:
        raise ValueError("decision_margin must lie in (0,1]")
    return Fraction(value).limit_denominator(1_000_000)


def _rational_string(numerator: int, denominator: int) -> str:
    value = Fraction(numerator, denominator)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def certify_margin_separated_score(
    n_bits: int,
    bucket_count: int,
    decision_margin: float = 1.0 / 8.0,
    sample_budget_power: int = 3,
) -> MarginEnergyCertificate:
    """Certify the minimum energy of a uniformly margin-separated linear score.

    Write H(d)=E[y a(k)|d].  If Re H is at least t+gamma on a
    bucket S and at most t-gamma off it, Parseval and a two-level convex
    minimization give

        E_k |a(k)|^2 >= 4 gamma^2 |S|(N-|S|)/N.

    The average one-record variance over d is at least (4-1/N) times this
    energy.  Consequently an empirical mean with uniform complex MSE at most
    gamma^2/4 needs at least

        16(4N-1)|S|(N-|S|)/N^2

    records.  This is a theorem about one linear score and an MSE-certified
    margin rule, not a lower bound for arbitrary classification algorithms.
    """
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if sample_budget_power < 1:
        raise ValueError("sample_budget_power must be positive")
    modulus = 1 << n_bits
    if bucket_count < 2 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n and be at least 2")
    margin = _as_fraction(decision_margin)
    bucket_size = modulus // bucket_count
    complement_size = modulus - bucket_size

    energy_numerator = 4 * margin.numerator**2 * bucket_size * complement_size
    energy_denominator = margin.denominator**2 * modulus
    energy = Fraction(energy_numerator, energy_denominator)
    mse_numerator = 16 * (4 * modulus - 1) * bucket_size * complement_size
    mse_denominator = modulus * modulus
    sample_lower_bound = (mse_numerator + mse_denominator - 1) // mse_denominator

    budget = n_bits**sample_budget_power
    polynomial_buckets = bucket_count <= budget
    samples_ruled_out = sample_lower_bound > budget
    gamma = float(margin)
    inside_level = 2.0 * gamma * (bucket_count - 1) / bucket_count
    outside_level = -2.0 * gamma / bucket_count
    threshold = (inside_level + outside_level) / 2.0
    return MarginEnergyCertificate(
        n_bits=n_bits,
        modulus=modulus,
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        decision_margin=gamma,
        optimal_inside_level=inside_level,
        optimal_outside_level=outside_level,
        optimal_threshold=threshold,
        exact_minimum_energy=_rational_string(energy.numerator, energy.denominator),
        log2_minimum_energy=math.log2(energy.numerator) - math.log2(energy.denominator),
        exact_uniform_mse_sample_lower_bound=sample_lower_bound,
        log2_sample_lower_bound=math.log2(sample_lower_bound),
        polynomial_sample_budget=budget,
        polynomial_bucket_enumeration=polynomial_buckets,
        polynomial_samples_ruled_out=samples_ruled_out,
        joint_polynomial_resources_possible=polynomial_buckets and not samples_ruled_out,
        proof_statement=(
            f"Every one-pass linear score separating one of {bucket_count} equal buckets by margin {gamma:g} "
            f"has energy at least {energy} and needs at least {sample_lower_bound} records to guarantee "
            "empirical-mean MSE at most gamma^2/4 on every hidden reflection."
        ),
    )


def finite_margin_check(n_bits: int, bucket_count: int, decision_margin: float = 1.0 / 8.0) -> FiniteMarginCheck:
    """Construct the optimal two-level response and verify Parseval numerically."""
    certificate = certify_margin_separated_score(n_bits, bucket_count, decision_margin)
    modulus = certificate.modulus
    bucket_size = certificate.bucket_size
    response = np.full(modulus, certificate.optimal_outside_level, dtype=np.complex128)
    response[:bucket_size] = certificate.optimal_inside_level
    weights = np.fft.fft(response)
    reconstruction = np.fft.ifft(weights)
    target_energy = float(np.sum(np.abs(response) ** 2))
    weight_second_moment = float(np.mean(np.abs(weights) ** 2))
    theoretical = 4.0 * decision_margin**2 * bucket_size * (modulus - bucket_size) / modulus
    inside_gap = float(np.min(response[:bucket_size].real - certificate.optimal_threshold))
    outside_gap = float(np.min(certificate.optimal_threshold - response[bucket_size:].real))
    return FiniteMarginCheck(
        n_bits=n_bits,
        modulus=modulus,
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        decision_margin=decision_margin,
        minimum_inside_gap=inside_gap,
        minimum_outside_gap=outside_gap,
        target_energy=target_energy,
        weight_second_moment=weight_second_moment,
        theoretical_minimum_energy=theoretical,
        maximum_reconstruction_error=float(np.max(np.abs(reconstruction - response))),
        parseval_error=abs(weight_second_moment - target_energy),
        optimality_error=abs(target_energy - theoretical),
    )


def _bucket_schedules(n_bits: int, sample_budget_power: int) -> list[int]:
    modulus = 1 << n_bits
    logn = max(1, math.ceil(math.log2(n_bits)))
    polynomial_counts = [2, 1 << min(n_bits, logn), 1 << min(n_bits, 2 * logn)]
    fine_bucket_bits = max(0, math.floor(sample_budget_power * math.log2(n_bits)) - 6)
    fine_bucket_size = 1 << min(n_bits, fine_bucket_bits)
    exponential_count = modulus // fine_bucket_size
    return sorted(
        count
        for count in {*polynomial_counts, exponential_count}
        if 2 <= count <= modulus and modulus % count == 0
    )


def run_biased_linear_margin_report(
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    decision_margin: float = 1.0 / 8.0,
    sample_budget_power: int = 3,
    finite_check_n_values: Sequence[int] = (6, 8, 10),
) -> DCPBiasedLinearMarginReport:
    certificates = [
        certify_margin_separated_score(
            n_bits,
            bucket_count,
            decision_margin=decision_margin,
            sample_budget_power=sample_budget_power,
        )
        for n_bits in n_values
        for bucket_count in _bucket_schedules(n_bits, sample_budget_power)
    ]
    finite_checks = [
        finite_margin_check(n_bits, bucket_count, decision_margin)
        for n_bits in finite_check_n_values
        for bucket_count in (2, 4, 8)
        if bucket_count <= (1 << n_bits)
    ]
    polynomial_bucket_rows = [row for row in certificates if row.polynomial_bucket_enumeration]
    polynomial_sample_rows = [row for row in certificates if not row.polynomial_samples_ruled_out]
    metrics: dict[str, int | float] = {
        "certificate_count": len(certificates),
        "finite_check_count": len(finite_checks),
        "finite_check_failure_count": sum(
            row.minimum_inside_gap + 1e-10 < decision_margin
            or row.minimum_outside_gap + 1e-10 < decision_margin
            or row.maximum_reconstruction_error > 1e-9
            or row.parseval_error > 1e-8
            or row.optimality_error > 1e-8
            for row in finite_checks
        ),
        "polynomial_bucket_count_row_count": len(polynomial_bucket_rows),
        "polynomial_bucket_rows_with_super_budget_samples": sum(
            row.polynomial_samples_ruled_out for row in polynomial_bucket_rows
        ),
        "polynomial_sample_row_count": len(polynomial_sample_rows),
        "polynomial_sample_rows_with_exponential_bucket_count": sum(
            not row.polynomial_bucket_enumeration for row in polynomial_sample_rows
        ),
        "joint_polynomial_resource_row_count": sum(row.joint_polynomial_resources_possible for row in certificates),
        "maximum_log2_sample_lower_bound": max((row.log2_sample_lower_bound for row in certificates), default=0.0),
        "proved_uniform_margin_linear_no_go_count": 1,
        "proved_arbitrary_linear_classifier_lower_bound_count": 0,
        "proved_nonlinear_decoder_lower_bound_count": 0,
    }
    falsifiers = [
        "Allowing biased expected scores does not evade Parseval when every in-bucket and out-of-bucket reflection must be separated by a common margin.",
        "The minimum energy is attained by two constant levels separated by twice the margin; oscillatory responses cannot lower it.",
        "Coarse polynomial bucket counts still force exponential samples for a uniform empirical-mean MSE guarantee.",
        "Fine sample-feasible buckets still leave exponentially many bucket tests.",
        "The theorem does not cover nonlinear record coupling, multiple adaptive scores, non-MSE decision analyses, or collective measurements.",
    ]
    return DCPBiasedLinearMarginReport(
        created_at=utc_now(),
        estimator_model={
            "record": "iid (k,y) with uniform k in Z_N, E[y|k]=exp(2 pi i k d/N), and |y|=2",
            "score": "T=(1/m) sum_j y_j a(k_j), with one public-label weight function a",
            "margin_contract": "there exist t,gamma>0 with Re H(d)>=t+gamma in the bucket and <=t-gamma outside",
            "accuracy_contract": "the empirical score has complex MSE at most gamma^2/4 uniformly over d",
        },
        theorem={
            "parseval": "E_k|a(k)|^2=sum_d|H(d)|^2",
            "minimum_energy": "sum_d|H(d)|^2 >= 4 gamma^2 S(N-S)/N for a target set of size S",
            "optimizer": "H is constant on the target and complement, with levels 2 gamma(N-S)/N and -2 gamma S/N",
            "average_variance": "average_d Var[y a(k)|d] >= (4-1/N) E_k|a(k)|^2",
            "uniform_mse_samples": "m >= ceil(16(4N-1)S(N-S)/N^2) for MSE <= gamma^2/4 on every d",
            "scope": "one linear empirical-mean score with uniform margin and MSE certification",
        },
        certificates=certificates,
        finite_checks=finite_checks,
        headline_metrics=metrics,
        excluded_and_open_classes={
            "excluded": [
                "biased one-pass linear bucket scores with a uniform margin and uniform empirical-mean MSE guarantee",
                "linear bit tests that rely on reducing the response amplitude while preserving its decision margin",
                "linear hash proposals that replace exact indicators by uniformly separated smooth responses",
            ],
            "open": [
                "nonlinear or robust decision rules whose error is not certified through score MSE",
                "multiple adaptive linear scores sharing records",
                "U-statistics and higher-degree couplings among iid records",
                "implicit nonseparable optimization and collective quantum measurements",
            ],
        },
        claim_gate={
            "uniform_margin_linear_no_go_proved": True,
            "finite_checks_passed": metrics["finite_check_failure_count"] == 0,
            "joint_polynomial_linear_row_found": metrics["joint_polynomial_resource_row_count"] > 0,
            "arbitrary_linear_classifier_lower_bound_proved": False,
            "nonlinear_decoder_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Bias and smoothing do not rescue a single uniformly margin-separated empirical linear score under the "
                "stated MSE contract. More general decision rules and nonlinear record couplings remain unresolved."
            ),
        },
        status="uniform-margin-linear-mse-scores-ruled-out-nonlinear-open",
        summary=(
            f"Certified {len(certificates)} biased linear margin tradeoff rows and {len(finite_checks)} finite optimality "
            f"checks. Joint polynomial rows={int(metrics['joint_polynomial_resource_row_count'])}; general nonlinear "
            "lower bounds=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_biased_linear_margin_report(
    path: Path = DCP_BIASED_LINEAR_MARGIN_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    decision_margin: float = 1.0 / 8.0,
    sample_budget_power: int = 3,
    finite_check_n_values: Sequence[int] = (6, 8, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_biased_linear_margin_report(
        n_values=n_values,
        decision_margin=decision_margin,
        sample_budget_power=sample_budget_power,
        finite_check_n_values=finite_check_n_values,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-IID-BIASED-LINEAR-MARGIN-PARSEVAL",
                source=str(path),
                claim="A biased or smoothed one-pass linear score gives sample-efficient coarse DCP frequency buckets while retaining a uniform decision margin.",
                reason_invalid=(
                    "Parseval plus the optimal two-level margin response forces energy at least "
                    "4 gamma^2 S(N-S)/N. Resolving the margin by a uniformly MSE-controlled empirical mean retains "
                    "the exponential sample-versus-bucket-enumeration tradeoff."
                ),
                lesson=(
                    "Do not mutate exact indicators into smooth biased linear scores without changing the estimator class. "
                    "Search nonlinear record coupling, multiple adaptive statistics, or collective measurements."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "certificate_count": payload["headline_metrics"]["certificate_count"],
                    "joint_polynomial_resource_row_count": payload["headline_metrics"][
                        "joint_polynomial_resource_row_count"
                    ],
                    "proved_uniform_margin_linear_no_go_count": 1,
                    "proved_nonlinear_decoder_lower_bound_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-BIASED-LINEAR-MARGIN"
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
                artifacts={"dcp_biased_linear_margin_audit": str(path)},
            )
        )
    return payload
