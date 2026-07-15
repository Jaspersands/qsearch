"""Degree-indexed audit of multilinear estimators over iid DCP records."""

from __future__ import annotations

import itertools
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


DCP_MULTIRECORD_HIERARCHY_PATH = Path(
    "research/classical_baselines/dcp_multirecord_estimator_hierarchy.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class MultilinearDegreeCertificate:
    n_bits: int
    modulus: int
    degree: int
    sign_pattern: str
    bucket_count: int
    bucket_size: int
    decision_margin: float
    exact_minimum_response_energy: str
    exact_disjoint_block_lower_bound: int
    exact_record_sample_lower_bound: int
    log2_record_sample_lower_bound: float
    polynomial_sample_budget: int
    polynomial_bucket_enumeration: bool
    polynomial_samples_ruled_out: bool
    joint_polynomial_resources_possible: bool
    relative_record_cost_vs_degree_one: float
    proof_statement: str


@dataclass(frozen=True)
class FiniteAggregateLabelCheck:
    n_bits: int
    modulus: int
    degree: int
    sign_pattern: str
    tuple_count: int
    expected_count_per_label: int
    maximum_label_count_deviation: int
    target_energy: float
    aggregate_weight_second_moment: float
    full_kernel_second_moment: float
    jensen_gap: float
    parseval_error: float
    maximum_response_error: float


@dataclass(frozen=True)
class EstimatorClassRecord:
    class_id: str
    access_legal: bool
    resource_status: str
    theorem_status: str
    finding: str
    open_obligation: str


@dataclass(frozen=True)
class DCPMultirecordHierarchyReport:
    created_at: str
    observation_model: dict[str, str]
    theorem: dict[str, str]
    certificates: list[MultilinearDegreeCertificate]
    finite_checks: list[FiniteAggregateLabelCheck]
    estimator_classes: list[EstimatorClassRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _fraction(value: float) -> Fraction:
    if not 0.0 < value <= 1.0:
        raise ValueError("decision_margin must lie in (0,1]")
    return Fraction(value).limit_denominator(1_000_000)


def _fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _signs(degree: int) -> tuple[int, ...]:
    return tuple(1 if index % 2 == 0 else -1 for index in range(degree))


def _sign_pattern(degree: int) -> str:
    return "".join("+" if sign > 0 else "-" for sign in _signs(degree))


def certify_disjoint_multilinear_score(
    n_bits: int,
    degree: int,
    bucket_count: int,
    decision_margin: float = 1.0 / 8.0,
    sample_budget_power: int = 3,
) -> MultilinearDegreeCertificate:
    """Certify a sample lower bound for one kernel on disjoint degree-r blocks."""
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if degree < 1:
        raise ValueError("degree must be positive")
    if sample_budget_power < 1:
        raise ValueError("sample_budget_power must be positive")
    modulus = 1 << n_bits
    if bucket_count < 2 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n and be at least 2")
    margin = _fraction(decision_margin)
    bucket_size = modulus // bucket_count
    complement_size = modulus - bucket_size
    response_energy = Fraction(
        4 * margin.numerator**2 * bucket_size * complement_size,
        margin.denominator**2 * modulus,
    )

    block_numerator = 16 * ((4**degree) * modulus - 1) * bucket_size * complement_size
    block_denominator = modulus * modulus
    block_count = (block_numerator + block_denominator - 1) // block_denominator
    record_count = degree * block_count
    degree_one_numerator = 16 * (4 * modulus - 1) * bucket_size * complement_size
    degree_one_blocks = (degree_one_numerator + block_denominator - 1) // block_denominator
    budget = n_bits**sample_budget_power
    polynomial_buckets = bucket_count <= budget
    samples_ruled_out = record_count > budget
    return MultilinearDegreeCertificate(
        n_bits=n_bits,
        modulus=modulus,
        degree=degree,
        sign_pattern=_sign_pattern(degree),
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        decision_margin=float(margin),
        exact_minimum_response_energy=_fraction_string(response_energy),
        exact_disjoint_block_lower_bound=block_count,
        exact_record_sample_lower_bound=record_count,
        log2_record_sample_lower_bound=math.log2(record_count),
        polynomial_sample_budget=budget,
        polynomial_bucket_enumeration=polynomial_buckets,
        polynomial_samples_ruled_out=samples_ruled_out,
        joint_polynomial_resources_possible=polynomial_buckets and not samples_ruled_out,
        relative_record_cost_vs_degree_one=record_count / degree_one_blocks,
        proof_statement=(
            f"A degree-{degree} multilinear kernel on disjoint iid blocks that uniformly separates one of "
            f"{bucket_count} buckets needs at least {block_count} independent blocks, hence {record_count} records, "
            "under the margin-squared MSE contract."
        ),
    )


def finite_aggregate_label_check(
    n_bits: int,
    degree: int,
    bucket_count: int = 4,
    decision_margin: float = 1.0 / 8.0,
) -> FiniteAggregateLabelCheck:
    """Exhaustively verify uniform signed sums and the optimal aggregate kernel."""
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if degree < 1:
        raise ValueError("degree must be positive")
    modulus = 1 << n_bits
    if bucket_count < 2 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n and be at least 2")
    bucket_size = modulus // bucket_count
    gamma = float(_fraction(decision_margin))
    inside = 2.0 * gamma * (bucket_count - 1) / bucket_count
    outside = -2.0 * gamma / bucket_count
    response = np.full(modulus, outside, dtype=np.complex128)
    response[:bucket_size] = inside
    aggregate_weights = np.fft.fft(response)

    signs = _signs(degree)
    counts = np.zeros(modulus, dtype=np.int64)
    full_kernel_energy_sum = 0.0
    for labels in itertools.product(range(modulus), repeat=degree):
        aggregate = sum(sign * label for sign, label in zip(signs, labels)) % modulus
        counts[aggregate] += 1
        full_kernel_energy_sum += float(abs(aggregate_weights[aggregate]) ** 2)
    tuple_count = modulus**degree
    expected_count = modulus ** (degree - 1)
    full_kernel_second_moment = full_kernel_energy_sum / tuple_count
    aggregate_second_moment = float(np.mean(np.abs(aggregate_weights) ** 2))
    reconstructed = np.fft.ifft(aggregate_weights)
    target_energy = float(np.sum(np.abs(response) ** 2))
    return FiniteAggregateLabelCheck(
        n_bits=n_bits,
        modulus=modulus,
        degree=degree,
        sign_pattern=_sign_pattern(degree),
        tuple_count=tuple_count,
        expected_count_per_label=expected_count,
        maximum_label_count_deviation=int(np.max(np.abs(counts - expected_count))),
        target_energy=target_energy,
        aggregate_weight_second_moment=aggregate_second_moment,
        full_kernel_second_moment=full_kernel_second_moment,
        jensen_gap=full_kernel_second_moment - aggregate_second_moment,
        parseval_error=abs(aggregate_second_moment - target_energy),
        maximum_response_error=float(np.max(np.abs(reconstructed - response))),
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


def _estimator_classes() -> list[EstimatorClassRecord]:
    return [
        EstimatorClassRecord(
            class_id="disjoint-block-single-multilinear-kernel",
            access_legal=True,
            resource_status="ruled-out-under-uniform-margin-mse-contract",
            theorem_status="proved-restricted",
            finding="Signed sums of independent uniform labels remain uniform; degree r multiplies the block second moment by 4^r.",
            open_obligation="None inside the stated one-kernel disjoint-block MSE model; alter the estimator class.",
        ),
        EstimatorClassRecord(
            class_id="all-overlapping-fixed-degree-u-statistic",
            access_legal=True,
            resource_status="open-dependent-tuple-variance",
            theorem_status="unproved",
            finding="The disjoint-block lower bound does not control cancellation among overlapping tuples or degenerate Hoeffding projections.",
            open_obligation="Bound every Hoeffding projection or construct a degenerate kernel with uniform bucket margin and polynomial evaluation.",
        ),
        EstimatorClassRecord(
            class_id="adaptive-multiple-linear-statistics",
            access_legal=True,
            resource_status="open-adaptive-decision-tree",
            theorem_status="unproved",
            finding="A family of scores can route adaptively without any one score separating the complete bucket from its complement.",
            open_obligation="Charge the number of scores, shared-sample dependence, per-node margin, and worst-reflection error.",
        ),
        EstimatorClassRecord(
            class_id="growing-degree-explicit-tuple-enumeration",
            access_legal=True,
            resource_status="superpolynomial-when-degree-grows",
            theorem_status="resource-accounting",
            finding="Enumerating all m^r tuples is superpolynomial once r grows with n unless an implicit contraction is proved.",
            open_obligation="Give a polynomial-description contraction or factorization and audit whether it recreates an N-sized spectrum.",
        ),
        EstimatorClassRecord(
            class_id="collective-quantum-multiregister-measurement",
            access_legal=True,
            resource_status="open",
            theorem_status="outside-classical-kernel-theorem",
            finding="Classical postmeasurement multilinear bounds do not constrain entangled measurements before local X/Y readout.",
            open_obligation="Provide a polynomial-size measurement circuit, exact f=1 robustness, and full lattice composition.",
        ),
    ]


def run_multirecord_hierarchy_report(
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    degrees: Sequence[int] = (1, 2, 3, 4, 6, 8),
    decision_margin: float = 1.0 / 8.0,
    sample_budget_power: int = 3,
    finite_n_bits: int = 4,
    finite_degrees: Sequence[int] = (1, 2, 3),
) -> DCPMultirecordHierarchyReport:
    certificates = [
        certify_disjoint_multilinear_score(
            n_bits,
            degree,
            bucket_count,
            decision_margin=decision_margin,
            sample_budget_power=sample_budget_power,
        )
        for n_bits in n_values
        for degree in degrees
        for bucket_count in _bucket_schedules(n_bits, sample_budget_power)
    ]
    finite_checks = [
        finite_aggregate_label_check(
            finite_n_bits,
            degree,
            bucket_count=4,
            decision_margin=decision_margin,
        )
        for degree in finite_degrees
    ]
    polynomial_bucket_rows = [row for row in certificates if row.polynomial_bucket_enumeration]
    classes = _estimator_classes()
    metrics: dict[str, int | float] = {
        "certificate_count": len(certificates),
        "degree_count": len(set(row.degree for row in certificates)),
        "finite_check_count": len(finite_checks),
        "finite_check_failure_count": sum(
            row.maximum_label_count_deviation != 0
            or row.jensen_gap < -1e-9
            or row.parseval_error > 1e-8
            or row.maximum_response_error > 1e-9
            for row in finite_checks
        ),
        "polynomial_bucket_count_row_count": len(polynomial_bucket_rows),
        "polynomial_bucket_rows_with_super_budget_samples": sum(
            row.polynomial_samples_ruled_out for row in polynomial_bucket_rows
        ),
        "joint_polynomial_resource_row_count": sum(row.joint_polynomial_resources_possible for row in certificates),
        "higher_degree_rows_cheaper_than_degree_one_count": sum(
            row.degree > 1 and row.relative_record_cost_vs_degree_one < 1.0 for row in certificates
        ),
        "maximum_relative_record_cost_vs_degree_one": max(
            (row.relative_record_cost_vs_degree_one for row in certificates), default=0.0
        ),
        "proved_disjoint_block_multilinear_no_go_count": 1,
        "proved_overlapping_ustatistic_lower_bound_count": 0,
        "proved_adaptive_multistatistic_lower_bound_count": 0,
        "proved_collective_measurement_lower_bound_count": 0,
        "open_estimator_class_count": sum(item.theorem_status == "unproved" or "outside" in item.theorem_status for item in classes),
    }
    falsifiers = [
        "A signed sum of any fixed number of independent uniform DCP labels is still uniform and does not synthesize chosen-label access.",
        "A single degree-r multilinear kernel on disjoint blocks obeys the same response Parseval bound and incurs a 4^r outcome second moment.",
        "Increasing degree makes the certified disjoint-block record cost worse, not better.",
        "The theorem does not cover overlapping U-statistics because dependent tuples can have degenerate Hoeffding projections.",
        "The theorem does not cover adaptive score families or collective quantum measurements.",
    ]
    return DCPMultirecordHierarchyReport(
        created_at=utc_now(),
        observation_model={
            "records": "independent (k_j,y_j), uniform k_j in Z_N, E[y_j|k_j]=chi_d(k_j), |y_j|=2",
            "degree_r_kernel": "Z=A(k_1,...,k_r) uses y_j for positive signs and conjugate(y_j) for negative signs, on disjoint blocks",
            "aggregate_label": "K=sum_j sigma_j k_j mod N for fixed public signs sigma_j in {+1,-1}",
            "target": "one bucket versus its complement with a uniform expected-score margin",
        },
        theorem={
            "aggregate_uniformity": "K is uniform for every fixed degree and sign pattern",
            "conditional_kernel": "a(K)=E[A|K] and Jensen gives E|A|^2>=E|a(K)|^2",
            "response_parseval": "E|a(K)|^2=sum_d|H(d)|^2",
            "margin_energy": "sum_d|H(d)|^2>=4 gamma^2 S(N-S)/N",
            "block_second_moment": "E|Z|^2=4^r E|A|^2",
            "average_block_variance": "average_d Var(Z|d)>=(4^r-1/N)4 gamma^2 S(N-S)/N",
            "record_lower_bound": "m>=r ceil(16(4^r N-1)S(N-S)/N^2) for disjoint blocks and uniform MSE<=gamma^2/4",
            "scope": "one multilinear kernel averaged over independent disjoint blocks",
        },
        certificates=certificates,
        finite_checks=finite_checks,
        estimator_classes=classes,
        headline_metrics=metrics,
        claim_gate={
            "disjoint_block_multilinear_no_go_proved": True,
            "finite_checks_passed": metrics["finite_check_failure_count"] == 0,
            "joint_polynomial_disjoint_block_row_found": metrics["joint_polynomial_resource_row_count"] > 0,
            "overlapping_ustatistic_lower_bound_proved": False,
            "adaptive_multistatistic_lower_bound_proved": False,
            "collective_measurement_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Naive fixed-degree disjoint multilinear sketches are ruled out under the margin/MSE contract. The most "
                "important nonlinear classes remain open and require separate dependence or circuit analyses."
            ),
        },
        status="disjoint-multilinear-sketches-ruled-out-overlapping-adaptive-collective-open",
        summary=(
            f"Certified {len(certificates)} degree-indexed disjoint-block rows through degree "
            f"{max(degrees, default=0)}. Joint polynomial rows={int(metrics['joint_polynomial_resource_row_count'])}; "
            f"open estimator classes={int(metrics['open_estimator_class_count'])}."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_multirecord_hierarchy_report(
    path: Path = DCP_MULTIRECORD_HIERARCHY_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    degrees: Sequence[int] = (1, 2, 3, 4, 6, 8),
    decision_margin: float = 1.0 / 8.0,
    sample_budget_power: int = 3,
    finite_n_bits: int = 4,
    finite_degrees: Sequence[int] = (1, 2, 3),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_multirecord_hierarchy_report(
        n_values=n_values,
        degrees=degrees,
        decision_margin=decision_margin,
        sample_budget_power=sample_budget_power,
        finite_n_bits=finite_n_bits,
        finite_degrees=finite_degrees,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-IID-DISJOINT-MULTIRECORD-MARGIN-PARSEVAL",
                source=str(path),
                claim="A fixed-degree product of iid DCP quadrature records creates a sample-efficient coarse-frequency sketch.",
                reason_invalid=(
                    "Every fixed signed aggregate label remains uniform. Conditional Jensen and Parseval retain the "
                    "margin-energy lower bound, while the product outcome contributes a 4^r second moment on disjoint blocks."
                ),
                lesson=(
                    "Do not retry disjoint fixed-degree product kernels. Analyze overlapping degenerate U-statistics, "
                    "adaptive score families, implicit contractions, or premeasurement collective observables."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "certificate_count": payload["headline_metrics"]["certificate_count"],
                    "joint_polynomial_resource_row_count": payload["headline_metrics"][
                        "joint_polynomial_resource_row_count"
                    ],
                    "proved_overlapping_ustatistic_lower_bound_count": 0,
                    "proved_collective_measurement_lower_bound_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-MULTIRECORD-HIERARCHY"
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
                artifacts={"dcp_multirecord_estimator_hierarchy": str(path)},
            )
        )
    return payload
