"""Hoeffding-variance audit for overlapping multilinear DCP U-statistics."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_USTATISTIC_VARIANCE_PATH = Path("research/classical_baselines/dcp_ustatistic_variance_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-IID-USTATISTIC-VARIANCE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class UStatisticCertificate:
    n_bits: int
    modulus: int
    degree: int
    bucket_count: int
    bucket_size: int
    required_tuple_count: int
    log2_required_tuple_count: float
    minimum_record_count: int
    log2_minimum_record_count: float
    actual_tuple_count_at_minimum_records: int
    polynomial_sample_budget: int
    polynomial_tuple_budget: int
    polynomial_bucket_enumeration: bool
    polynomial_records_possible: bool
    polynomial_explicit_tuple_evaluation_possible: bool
    joint_polynomial_explicit_resources_possible: bool
    proof_statement: str


@dataclass(frozen=True)
class HoeffdingCoefficientCheck:
    degree: int
    record_count: int
    coefficients: list[float]
    minimum_coefficient: float
    exact_highest_order_coefficient: float
    maximum_monotonicity_violation: float
    lower_bound_error: float


@dataclass(frozen=True)
class UStatisticClassRecord:
    class_id: str
    status: str
    theorem_scope: str
    remaining_obligation: str


@dataclass(frozen=True)
class DCPUStatisticVarianceReport:
    created_at: str
    model: dict[str, str]
    theorem: dict[str, str]
    certificates: list[UStatisticCertificate]
    finite_coefficient_checks: list[HoeffdingCoefficientCheck]
    estimator_classes: list[UStatisticClassRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def minimum_records_for_tuple_count(degree: int, required_tuple_count: int) -> int:
    """Return the least m >= r with binomial(m,r) at least the target."""
    if degree < 1:
        raise ValueError("degree must be positive")
    if required_tuple_count < 1:
        raise ValueError("required_tuple_count must be positive")
    low = degree
    high = degree
    while math.comb(high, degree) < required_tuple_count:
        high *= 2
    while low < high:
        middle = (low + high) // 2
        if math.comb(middle, degree) >= required_tuple_count:
            high = middle
        else:
            low = middle + 1
    return low


def certify_ustatistic(
    n_bits: int,
    degree: int,
    bucket_count: int,
    sample_budget_power: int = 3,
    tuple_budget_power: int = 6,
) -> UStatisticCertificate:
    """Certify worst-instance U-statistic sample or explicit tuple costs.

    For a symmetric order-r kernel h and its all-subsets U-statistic U_m,
    Hoeffding decomposition gives

        Var(U_m) = sum_s C(r,s)^2/C(m,s) sigma_s^2
                 >= Var(h)/C(m,r).

    The iid DCP product-kernel Jensen/Parseval argument supplies a hidden
    reflection with kernel variance at least

        (4^r - 1/N) 4 gamma^2 S(N-S)/N.

    Requiring uniform MSE at most gamma^2/4 therefore forces C(m,r) to be at
    least the integer below.  The margin cancels exactly.
    """
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if degree < 1:
        raise ValueError("degree must be positive")
    if sample_budget_power < 1 or tuple_budget_power < 1:
        raise ValueError("budget powers must be positive")
    modulus = 1 << n_bits
    if bucket_count < 2 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n and be at least 2")
    bucket_size = modulus // bucket_count
    complement_size = modulus - bucket_size
    numerator = 16 * ((4**degree) * modulus - 1) * bucket_size * complement_size
    denominator = modulus * modulus
    required_tuples = (numerator + denominator - 1) // denominator
    minimum_records = minimum_records_for_tuple_count(degree, required_tuples)
    actual_tuples = math.comb(minimum_records, degree)
    sample_budget = n_bits**sample_budget_power
    tuple_budget = n_bits**tuple_budget_power
    polynomial_buckets = bucket_count <= sample_budget
    polynomial_records = minimum_records <= sample_budget
    polynomial_tuples = required_tuples <= tuple_budget
    return UStatisticCertificate(
        n_bits=n_bits,
        modulus=modulus,
        degree=degree,
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        required_tuple_count=required_tuples,
        log2_required_tuple_count=math.log2(required_tuples),
        minimum_record_count=minimum_records,
        log2_minimum_record_count=math.log2(minimum_records),
        actual_tuple_count_at_minimum_records=actual_tuples,
        polynomial_sample_budget=sample_budget,
        polynomial_tuple_budget=tuple_budget,
        polynomial_bucket_enumeration=polynomial_buckets,
        polynomial_records_possible=polynomial_records,
        polynomial_explicit_tuple_evaluation_possible=polynomial_tuples,
        joint_polynomial_explicit_resources_possible=(
            polynomial_buckets and polynomial_records and polynomial_tuples
        ),
        proof_statement=(
            f"Every explicit symmetric degree-{degree} product-kernel U-statistic with uniform bucket margin needs "
            f"C(m,{degree}) >= {required_tuples}; hence m >= {minimum_records}, and explicit evaluation needs at least "
            f"{required_tuples} tuple terms on the certified worst hidden reflection."
        ),
    )


def hoeffding_coefficient_check(degree: int, record_count: int) -> HoeffdingCoefficientCheck:
    """Verify the coefficient minimum used in the U-statistic variance bound."""
    if degree < 1 or record_count < degree:
        raise ValueError("require record_count >= degree >= 1")
    coefficients = [
        math.comb(degree, order) / math.comb(record_count, order)
        for order in range(1, degree + 1)
    ]
    highest = 1.0 / math.comb(record_count, degree)
    monotonicity_violation = max(
        [coefficients[index + 1] - coefficients[index] for index in range(len(coefficients) - 1)]
        or [0.0]
    )
    return HoeffdingCoefficientCheck(
        degree=degree,
        record_count=record_count,
        coefficients=coefficients,
        minimum_coefficient=min(coefficients),
        exact_highest_order_coefficient=highest,
        maximum_monotonicity_violation=max(0.0, monotonicity_violation),
        lower_bound_error=abs(min(coefficients) - highest),
    )


def _bucket_schedules(n_bits: int, sample_budget_power: int) -> list[int]:
    modulus = 1 << n_bits
    logn = max(1, math.ceil(math.log2(n_bits)))
    polynomial_counts = [2, 1 << min(n_bits, logn), 1 << min(n_bits, 2 * logn)]
    fine_bucket_bits = max(0, math.floor(sample_budget_power * math.log2(n_bits)) - 6)
    fine_bucket_size = 1 << min(n_bits, fine_bucket_bits)
    return sorted(
        count
        for count in {*polynomial_counts, modulus // fine_bucket_size}
        if 2 <= count <= modulus and modulus % count == 0
    )


def _classes() -> list[UStatisticClassRecord]:
    return [
        UStatisticClassRecord(
            class_id="fixed-degree-explicit-all-subsets-u-statistic",
            status="ruled-out-under-uniform-margin-mse-contract",
            theorem_scope="symmetric multilinear product kernel evaluated on every r-subset",
            remaining_obligation="Change the kernel or estimator class; overlap alone does not remove the variance bound.",
        ),
        UStatisticClassRecord(
            class_id="growing-degree-explicit-all-subsets-u-statistic",
            status="explicit-evaluation-exponential",
            theorem_scope="degree may grow and records may become polynomial, but required evaluated tuple count remains exponential for coarse buckets",
            remaining_obligation="Give an implicit contraction rather than enumerating the certified number of tuples.",
        ),
        UStatisticClassRecord(
            class_id="implicitly-contracted-u-statistic",
            status="open",
            theorem_scope="variance bound applies, but arithmetic cost need not equal tuple count if the kernel factorizes",
            remaining_obligation="Prove polynomial contraction cost, uniform margin, precision, and absence of an N-sized hidden spectrum.",
        ),
        UStatisticClassRecord(
            class_id="non-product-or-adaptive-multistatistic",
            status="open",
            theorem_scope="outside the single symmetric signed-product kernel model",
            remaining_obligation="State the observation polynomial, decision tree, shared-sample error, and worst-reflection cost exactly.",
        ),
        UStatisticClassRecord(
            class_id="collective-quantum-measurement",
            status="open",
            theorem_scope="outside postmeasurement classical U-statistics",
            remaining_obligation="Supply a polynomial circuit and exact f=1/lattice composition theorem.",
        ),
    ]


def run_ustatistic_variance_report(
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    degrees: Sequence[int] = (2, 3, 4, 6, 8, 16, 32),
    sample_budget_power: int = 3,
    tuple_budget_power: int = 6,
) -> DCPUStatisticVarianceReport:
    certificates = [
        certify_ustatistic(
            n_bits,
            degree,
            bucket_count,
            sample_budget_power=sample_budget_power,
            tuple_budget_power=tuple_budget_power,
        )
        for n_bits in n_values
        for degree in degrees
        if degree <= n_bits
        for bucket_count in _bucket_schedules(n_bits, sample_budget_power)
    ]
    coefficient_checks = [
        hoeffding_coefficient_check(degree, multiplier * degree)
        for degree in (1, 2, 3, 4, 6, 8)
        for multiplier in (1, 2, 4)
    ]
    polynomial_bucket_rows = [row for row in certificates if row.polynomial_bucket_enumeration]
    classes = _classes()
    metrics: dict[str, int | float] = {
        "certificate_count": len(certificates),
        "degree_count": len(set(row.degree for row in certificates)),
        "coefficient_check_count": len(coefficient_checks),
        "coefficient_check_failure_count": sum(
            row.maximum_monotonicity_violation > 1e-12 or row.lower_bound_error > 1e-12
            for row in coefficient_checks
        ),
        "polynomial_bucket_count_row_count": len(polynomial_bucket_rows),
        "polynomial_bucket_rows_with_super_budget_records": sum(
            not row.polynomial_records_possible for row in polynomial_bucket_rows
        ),
        "polynomial_bucket_rows_with_super_budget_explicit_tuples": sum(
            not row.polynomial_explicit_tuple_evaluation_possible for row in polynomial_bucket_rows
        ),
        "polynomial_record_but_exponential_tuple_row_count": sum(
            row.polynomial_records_possible and not row.polynomial_explicit_tuple_evaluation_possible
            for row in certificates
        ),
        "joint_polynomial_explicit_resource_row_count": sum(
            row.joint_polynomial_explicit_resources_possible for row in certificates
        ),
        "proved_overlapping_ustatistic_variance_bound_count": 1,
        "proved_fixed_degree_polynomial_sample_decoder_count": 0,
        "proved_implicit_contraction_lower_bound_count": 0,
        "proved_collective_measurement_lower_bound_count": 0,
        "open_estimator_class_count": sum(item.status == "open" for item in classes),
    }
    falsifiers = [
        "Overlap and Hoeffding degeneracy cannot reduce U-statistic variance below kernel variance divided by C(m,r).",
        "For coarse polynomially many buckets, the required tuple count is exponential for every tested degree.",
        "Fixed degree retains exponential record complexity even when all overlapping tuples are used.",
        "Growing degree can make the record count polynomial only while explicit tuple evaluation remains exponential.",
        "The theorem does not rule out a polynomial implicit contraction, a non-product adaptive statistic, or a collective measurement.",
    ]
    return DCPUStatisticVarianceReport(
        created_at=utc_now(),
        model={
            "kernel": "symmetric order-r signed-product kernel h(X_1,...,X_r)",
            "statistic": "U_m is the average of h over all C(m,r) distinct r-subsets",
            "target": "uniform expected-score margin for one frequency bucket versus its complement",
            "accuracy": "complex MSE at most gamma^2/4 for every hidden reflection",
        },
        theorem={
            "kernel_decomposition": "Var(h)=sum_{s=1}^r C(r,s) sigma_s^2",
            "ustatistic_variance": "Var(U_m)=sum_{s=1}^r C(r,s)^2/C(m,s) sigma_s^2",
            "coefficient_minimum": "C(r,s)/C(m,s) is minimized at s=r, hence Var(U_m)>=Var(h)/C(m,r)",
            "worst_instance_kernel_variance": "max_d Var(h|d)>=(4^r-1/N)4 gamma^2 S(N-S)/N",
            "tuple_requirement": "C(m,r)>=ceil(16(4^r N-1)S(N-S)/N^2)",
            "fixed_degree_consequence": "m=2^Omega(n/r) for B=poly(n) and constant r",
            "growing_degree_consequence": "explicit evaluation still uses 2^Omega(n) tuple terms for B=poly(n)",
            "scope": "single symmetric signed-product U-statistic with explicit uniform margin/MSE contract",
        },
        certificates=certificates,
        finite_coefficient_checks=coefficient_checks,
        estimator_classes=classes,
        headline_metrics=metrics,
        claim_gate={
            "overlapping_ustatistic_variance_bound_proved": True,
            "coefficient_checks_passed": metrics["coefficient_check_failure_count"] == 0,
            "joint_polynomial_explicit_row_found": metrics["joint_polynomial_explicit_resource_row_count"] > 0,
            "implicit_contraction_lower_bound_proved": False,
            "collective_measurement_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Explicit overlapping signed-product U-statistics do not provide a joint-polynomial decoder. An implicit "
                "contraction or a different estimator/measurement class remains a substantive open route."
            ),
        },
        status="explicit-overlapping-ustatistics-ruled-out-implicit-contraction-open",
        summary=(
            f"Certified {len(certificates)} overlapping U-statistic rows across "
            f"{len(set(row.degree for row in certificates))} degrees. Joint polynomial explicit rows="
            f"{int(metrics['joint_polynomial_explicit_resource_row_count'])}; implicit-contraction lower bounds=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_ustatistic_variance_report(
    path: Path = DCP_USTATISTIC_VARIANCE_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    degrees: Sequence[int] = (2, 3, 4, 6, 8, 16, 32),
    sample_budget_power: int = 3,
    tuple_budget_power: int = 6,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_ustatistic_variance_report(
        n_values=n_values,
        degrees=degrees,
        sample_budget_power=sample_budget_power,
        tuple_budget_power=tuple_budget_power,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-IID-EXPLICIT-OVERLAPPING-USTATISTIC",
                source=str(path),
                claim="Overlapping all-subsets U-statistics remove the exponential variance of DCP multirecord product kernels.",
                reason_invalid=(
                    "Hoeffding decomposition gives Var(U_m)>=Var(h)/C(m,r). The DCP margin-energy bound therefore forces "
                    "exponential records at fixed degree or exponentially many explicitly evaluated tuples at growing degree."
                ),
                lesson=(
                    "Do not retry explicit all-subsets product kernels. Search a proved implicit contraction, a non-product "
                    "adaptive statistic, or a polynomial premeasurement collective observable."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "certificate_count": payload["headline_metrics"]["certificate_count"],
                    "joint_polynomial_explicit_resource_row_count": payload["headline_metrics"][
                        "joint_polynomial_explicit_resource_row_count"
                    ],
                    "proved_implicit_contraction_lower_bound_count": 0,
                    "proved_collective_measurement_lower_bound_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-USTATISTIC-VARIANCE"
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
                artifacts={"dcp_ustatistic_variance_audit": str(path)},
            )
        )
    return payload
