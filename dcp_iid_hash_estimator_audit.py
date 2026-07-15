"""Parseval no-go audit for linear iid hash-bin estimators on DCP records."""

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


DCP_IID_HASH_ESTIMATOR_PATH = Path("research/classical_baselines/dcp_iid_hash_estimator_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class LinearBucketEstimatorCertificate:
    n_bits: int
    modulus: int
    bucket_count: int
    bucket_size: int
    bucket_count_class: str
    exact_weight_second_moment: int
    target_mse: float
    exact_unbiased_sample_lower_bound: int
    log2_sample_lower_bound: float
    polynomial_sample_budget: int
    sample_budget_power: int
    polynomial_samples_ruled_out: bool
    polynomial_bucket_enumeration: bool
    joint_polynomial_resources_possible: bool
    proof_statement: str


@dataclass(frozen=True)
class FiniteParsevalCheck:
    n_bits: int
    modulus: int
    bucket_count: int
    bucket_size: int
    target_energy: float
    weight_second_moment: float
    maximum_reconstruction_error: float
    parseval_error: float


@dataclass(frozen=True)
class DCPIIDHashEstimatorReport:
    created_at: str
    estimator_model: dict[str, str]
    theorem: dict[str, str]
    certificates: list[LinearBucketEstimatorCertificate]
    finite_parseval_checks: list[FiniteParsevalCheck]
    headline_metrics: dict[str, int | float]
    excluded_and_open_classes: dict[str, list[str]]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def finite_parseval_check(n_bits: int, bucket_count: int) -> FiniteParsevalCheck:
    """Construct exact interval-membership weights and verify normalized Parseval."""
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    modulus = 1 << n_bits
    if bucket_count < 1 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n")
    bucket_size = modulus // bucket_count
    target = np.zeros(modulus, dtype=np.complex128)
    target[:bucket_size] = 1.0
    # H(d)=(1/N) sum_k a(k) exp(+2 pi i k d/N), so a is the forward FFT of H.
    weights = np.fft.fft(target)
    reconstruction = np.fft.ifft(weights)
    target_energy = float(np.sum(np.abs(target) ** 2))
    weight_second_moment = float(np.mean(np.abs(weights) ** 2))
    return FiniteParsevalCheck(
        n_bits=n_bits,
        modulus=modulus,
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        target_energy=target_energy,
        weight_second_moment=weight_second_moment,
        maximum_reconstruction_error=float(np.max(np.abs(reconstruction - target))),
        parseval_error=abs(weight_second_moment - target_energy),
    )


def certify_linear_bucket_estimator(
    n_bits: int,
    bucket_count: int,
    target_mse: float = 1.0 / 9.0,
    sample_budget_power: int = 3,
) -> LinearBucketEstimatorCertificate:
    """Certify sample/enumeration costs for an exact unbiased linear test.

    Let T=m^-1 sum_j y_j a(k_j), with E[y|k]=chi_d(k) and |y|=2.
    If E[T|d] equals a bucket indicator h(d), normalized Parseval gives
    E_k|a(k)|^2=sum_d|h(d)|^2=N/B.  On d inside the bucket, one-sample
    variance is 4N/B-1, hence m >= (4N/B-1)/MSE.
    """
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    modulus = 1 << n_bits
    if bucket_count < 1 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n")
    if not 0.0 < target_mse < 1.0:
        raise ValueError("target_mse must lie in (0,1)")
    if sample_budget_power < 1:
        raise ValueError("sample_budget_power must be positive")
    bucket_size = modulus // bucket_count
    second_moment = bucket_size
    mse_fraction = Fraction(target_mse).limit_denominator(1_000_000)
    variance_numerator = 4 * second_moment - 1
    lower_bound = max(
        1,
        (variance_numerator * mse_fraction.denominator + mse_fraction.numerator - 1)
        // mse_fraction.numerator,
    )
    budget = n_bits**sample_budget_power
    polynomial_buckets = bucket_count <= n_bits**sample_budget_power
    return LinearBucketEstimatorCertificate(
        n_bits=n_bits,
        modulus=modulus,
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        bucket_count_class="poly(n)" if polynomial_buckets else "superpolynomial/exponential in n",
        exact_weight_second_moment=second_moment,
        target_mse=target_mse,
        exact_unbiased_sample_lower_bound=lower_bound,
        log2_sample_lower_bound=math.log2(lower_bound),
        polynomial_sample_budget=budget,
        sample_budget_power=sample_budget_power,
        polynomial_samples_ruled_out=lower_bound > budget,
        polynomial_bucket_enumeration=polynomial_buckets,
        joint_polynomial_resources_possible=lower_bound <= budget and polynomial_buckets,
        proof_statement=(
            f"Any exact unbiased one-pass linear estimator for one of {bucket_count} equal frequency buckets has "
            f"E|a(k)|^2={second_moment} and needs at least {lower_bound} iid records for MSE <= {target_mse:g}."
        ),
    )


def _bucket_schedules(n_bits: int, sample_budget_power: int) -> list[int]:
    modulus = 1 << n_bits
    logn = max(1, math.ceil(math.log2(n_bits)))
    polynomial_counts = [2, 1 << min(n_bits, logn), 1 << min(n_bits, 2 * logn)]
    # Leave a factor 64 for the variance constant so this row is genuinely
    # sample-feasible under the n^p comparison budget.
    fine_bucket_bits = max(0, math.floor(sample_budget_power * math.log2(n_bits)) - 6)
    fine_bucket_size = 1 << min(n_bits, fine_bucket_bits)
    exponential_count = max(1, modulus // fine_bucket_size)
    return sorted({count for count in [*polynomial_counts, exponential_count] if count <= modulus and modulus % count == 0})


def run_iid_hash_estimator_report(
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    target_mse: float = 1.0 / 9.0,
    sample_budget_power: int = 3,
    finite_check_n_values: Sequence[int] = (6, 8, 10),
) -> DCPIIDHashEstimatorReport:
    certificates = [
        certify_linear_bucket_estimator(
            n_bits,
            bucket_count,
            target_mse=target_mse,
            sample_budget_power=sample_budget_power,
        )
        for n_bits in n_values
        for bucket_count in _bucket_schedules(n_bits, sample_budget_power)
    ]
    finite_checks = [
        finite_parseval_check(n_bits, bucket_count)
        for n_bits in finite_check_n_values
        for bucket_count in (2, 4, 8)
        if bucket_count <= (1 << n_bits)
    ]
    polynomial_bucket_rows = [row for row in certificates if row.polynomial_bucket_enumeration]
    polynomial_sample_rows = [row for row in certificates if not row.polynomial_samples_ruled_out]
    metrics: dict[str, int | float] = {
        "certificate_count": len(certificates),
        "finite_parseval_check_count": len(finite_checks),
        "finite_parseval_failure_count": sum(
            row.maximum_reconstruction_error > 1e-9 or row.parseval_error > 1e-8 for row in finite_checks
        ),
        "polynomial_bucket_count_row_count": len(polynomial_bucket_rows),
        "polynomial_bucket_rows_with_exponential_sample_lower_bound": sum(
            row.polynomial_samples_ruled_out for row in polynomial_bucket_rows
        ),
        "polynomial_sample_row_count": len(polynomial_sample_rows),
        "polynomial_sample_rows_with_exponential_bucket_count": sum(
            not row.polynomial_bucket_enumeration for row in polynomial_sample_rows
        ),
        "joint_polynomial_resource_row_count": sum(row.joint_polynomial_resources_possible for row in certificates),
        "maximum_log2_sample_lower_bound": max((row.log2_sample_lower_bound for row in certificates), default=0.0),
        "proved_exact_linear_estimator_no_go_count": 1,
        "proved_nonlinear_decoder_lower_bound_count": 0,
        "proved_collective_measurement_lower_bound_count": 0,
    }
    falsifiers = [
        "A coarse exact linear bucket indicator has Fourier weight energy N/B, so iid Monte Carlo variance is exponential when B=poly(log N).",
        "Making one bucket test sample-efficient forces B to be exponential, leaving exponentially many candidate buckets.",
        "Closed-form evaluation of Dirichlet or square-wave weights does not remove their Parseval second moment.",
        "This theorem excludes exact unbiased one-pass linear estimators only; nonlinear multi-sample decoding remains open.",
        "The theorem does not lower-bound collective quantum measurements or generic DCP sieves.",
    ]
    return DCPIIDHashEstimatorReport(
        created_at=utc_now(),
        estimator_model={
            "record": "iid (k,y) with uniform k in Z_N, E[y|k]=exp(2 pi i k d/N), and |y|=2",
            "linear_estimator": "T=(1/m) sum_j y_j a(k_j), with a computable from public k only",
            "target": "exact unbiased indicator of one equal frequency bucket for every hidden d",
            "costs_charged": "iid state samples, arithmetic, bucket enumeration, weight evaluation, and stored candidates",
        },
        theorem={
            "parseval_identity": "E_k |a(k)|^2 = sum_d |E[T|d]|^2",
            "bucket_energy": "for an indicator of a bucket of size N/B, E_k|a(k)|^2=N/B",
            "variance": "inside the bucket, Var(y a(k))=4N/B-1",
            "sample_lower_bound": "m >= (4N/B-1)/epsilon for mean-square error at most epsilon",
            "tradeoff": "coarse B=poly(log N) costs exponential samples; N/B=poly(log N) leaves exponential B",
        },
        certificates=certificates,
        finite_parseval_checks=finite_checks,
        headline_metrics=metrics,
        excluded_and_open_classes={
            "excluded": [
                "exact unbiased one-pass linear binary-search bit estimators",
                "exact unbiased linear interval-bucket indicators with polynomially many buckets",
                "linear hash-bin proposals justified only by closed-form weight evaluation",
            ],
            "open": [
                "biased estimators with a proved inverse-polynomial decision margin and lower second moment",
                "nonlinear estimators coupling many iid records",
                "implicit optimization over exponentially many frequencies without an N-sized state",
                "collective quantum measurements and subexponential phase-state sieves",
            ],
        },
        claim_gate={
            "linear_bucket_no_go_proved": True,
            "finite_parseval_checks_passed": metrics["finite_parseval_failure_count"] == 0,
            "joint_polynomial_linear_row_found": metrics["joint_polynomial_resource_row_count"] > 0,
            "nonlinear_decoder_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The proposed iid hash-bin shortcut is ruled out for exact unbiased linear estimators, but this restricted "
                "theorem neither constructs nor excludes a nonlinear random-example decoder."
            ),
        },
        status="exact-linear-iid-hash-estimators-ruled-out-nonlinear-open",
        summary=(
            f"Certified {len(certificates)} Parseval sample/enumeration tradeoff rows and {len(finite_checks)} exact finite "
            f"transform checks. Joint polynomial linear rows={int(metrics['joint_polynomial_resource_row_count'])}; "
            "nonlinear decoder lower bounds=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_iid_hash_estimator_report(
    path: Path = DCP_IID_HASH_ESTIMATOR_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    target_mse: float = 1.0 / 9.0,
    sample_budget_power: int = 3,
    finite_check_n_values: Sequence[int] = (6, 8, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_iid_hash_estimator_report(
        n_values=n_values,
        target_mse=target_mse,
        sample_budget_power=sample_budget_power,
        finite_check_n_values=finite_check_n_values,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-IID-EXACT-LINEAR-HASH-BIN-PARSEVAL",
                source=str(path),
                claim="Exact linear iid Monte Carlo estimators provide sample-efficient coarse frequency buckets for DCP decoding.",
                reason_invalid=(
                    "Normalized Parseval forces second moment N/B for a bucket of size N/B. Polynomially many coarse "
                    "buckets require exponential samples, while polynomial samples require exponentially many buckets."
                ),
                lesson="Search nonlinear iid localization or prove a biased low-variance margin; do not retry exact linear bucket indicators.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "certificate_count": payload["headline_metrics"]["certificate_count"],
                    "joint_polynomial_resource_row_count": payload["headline_metrics"][
                        "joint_polynomial_resource_row_count"
                    ],
                    "proved_nonlinear_decoder_lower_bound_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-IID-LINEAR-HASH"
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
                artifacts={"dcp_iid_hash_estimator_audit": str(path)},
            )
        )
    return payload
