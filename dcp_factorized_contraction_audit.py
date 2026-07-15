"""Audit efficiently contracted rank-one DCP product U-statistics."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
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


DCP_FACTORIZED_CONTRACTION_PATH = Path("research/classical_baselines/dcp_factorized_contraction_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class RankOneContractionCertificate:
    n_bits: int
    modulus: int
    degree: int
    bucket_count: int
    bucket_size: int
    worst_large_class_size: int
    exact_record_sample_lower_bound: int
    log2_record_sample_lower_bound: float
    polynomial_sample_budget: int
    polynomial_bucket_enumeration: bool
    polynomial_samples_possible: bool
    polynomial_contraction_time_possible: bool
    joint_polynomial_resources_possible: bool
    proof_statement: str


@dataclass(frozen=True)
class FiniteRankOneVarianceCheck:
    n_bits: int
    modulus: int
    degree: int
    record_count: int
    bucket_count: int
    bucket_size: int
    margin: float
    base_response_energy: float
    target_base_mean_magnitude: float
    one_record_variance: float
    exact_ustatistic_variance: float
    first_projection_variance_term: float
    analytic_first_projection_lower_bound: float
    variance_bound_violation: float


@dataclass(frozen=True)
class ContractionClassRecord:
    class_id: str
    contraction_cost: str
    theorem_status: str
    finding: str
    next_obligation: str


@dataclass(frozen=True)
class DCPFactorizedContractionReport:
    created_at: str
    model: dict[str, str]
    theorem: dict[str, str]
    certificates: list[RankOneContractionCertificate]
    finite_variance_checks: list[FiniteRankOneVarianceCheck]
    contraction_classes: list[ContractionClassRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def certify_rank_one_contraction(
    n_bits: int,
    degree: int,
    bucket_count: int,
    sample_budget_power: int = 3,
) -> RankOneContractionCertificate:
    """Certify the first-projection sample cost of a rank-one contraction.

    A rank-one signed-product kernel has h=prod_i z_i and expectation H(d)=F(d)^r.
    Its all-subsets U-statistic is an elementary symmetric polynomial, so it can
    be contracted in O(mr).  If Re H separates a bucket S from its complement
    by margin gamma around any threshold, one of the two classes has
    |H(d)|>=gamma throughout.  Calling its size L>=min(S,N-S), Parseval gives
    E|a|^2>=L gamma^(2/r).  At any d in that class, the first Hoeffding term is

        r^2/m |F|^(2r-2) (4 E|a|^2-|F|^2)
        >= 3 r^2 L gamma^2/m.

    Uniform MSE <= gamma^2/4 therefore requires m>=12 r^2 L.
    """
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if degree < 1:
        raise ValueError("degree must be positive")
    if sample_budget_power < 1:
        raise ValueError("sample_budget_power must be positive")
    modulus = 1 << n_bits
    if bucket_count < 2 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n and be at least 2")
    bucket_size = modulus // bucket_count
    large_class_lower_bound = min(bucket_size, modulus - bucket_size)
    record_lower_bound = 12 * degree * degree * large_class_lower_bound
    budget = n_bits**sample_budget_power
    polynomial_buckets = bucket_count <= budget
    polynomial_samples = record_lower_bound <= budget
    # The elementary-symmetric dynamic program is O(mr), so its arithmetic is
    # polynomial exactly when the certified required record count is.
    polynomial_contraction = polynomial_samples and degree <= budget
    return RankOneContractionCertificate(
        n_bits=n_bits,
        modulus=modulus,
        degree=degree,
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        worst_large_class_size=large_class_lower_bound,
        exact_record_sample_lower_bound=record_lower_bound,
        log2_record_sample_lower_bound=math.log2(record_lower_bound),
        polynomial_sample_budget=budget,
        polynomial_bucket_enumeration=polynomial_buckets,
        polynomial_samples_possible=polynomial_samples,
        polynomial_contraction_time_possible=polynomial_contraction,
        joint_polynomial_resources_possible=polynomial_buckets and polynomial_contraction,
        proof_statement=(
            f"Every rank-one degree-{degree} elementary-symmetric contraction separating one of {bucket_count} "
            f"equal buckets needs at least {record_lower_bound} iid records under the uniform margin/MSE contract."
        ),
    )


def finite_rank_one_variance_check(
    n_bits: int,
    degree: int,
    record_count: int,
    bucket_count: int = 4,
    margin: float = 1.0 / 8.0,
) -> FiniteRankOneVarianceCheck:
    """Check the exact Hoeffding variance of a sparse two-level rank-one response."""
    if n_bits < 2 or degree < 1 or record_count < degree:
        raise ValueError("require n_bits>=2 and record_count>=degree>=1")
    if not 0.0 < margin <= 1.0:
        raise ValueError("margin must lie in (0,1]")
    modulus = 1 << n_bits
    if bucket_count < 2 or modulus % bucket_count:
        raise ValueError("bucket_count must divide 2^n and be at least 2")
    bucket_size = modulus // bucket_count
    # H=2 gamma on the smaller target class and zero outside.  The threshold
    # gamma gives the required two-sided margin.  Choose the positive real rth root.
    base_inside = (2.0 * margin) ** (1.0 / degree)
    base_response = np.zeros(modulus, dtype=np.complex128)
    base_response[:bucket_size] = base_inside
    weights = np.fft.fft(base_response)
    base_energy = float(np.mean(np.abs(weights) ** 2))
    mu = base_inside
    one_record_variance = 4.0 * base_energy - mu * mu
    terms = [
        (math.comb(degree, order) ** 2 / math.comb(record_count, order))
        * (mu ** (2 * (degree - order)))
        * (one_record_variance**order)
        for order in range(1, degree + 1)
    ]
    first_term = terms[0]
    lower_bound = 3.0 * degree * degree * bucket_size * margin * margin / record_count
    return FiniteRankOneVarianceCheck(
        n_bits=n_bits,
        modulus=modulus,
        degree=degree,
        record_count=record_count,
        bucket_count=bucket_count,
        bucket_size=bucket_size,
        margin=margin,
        base_response_energy=base_energy,
        target_base_mean_magnitude=mu,
        one_record_variance=one_record_variance,
        exact_ustatistic_variance=sum(terms),
        first_projection_variance_term=first_term,
        analytic_first_projection_lower_bound=lower_bound,
        variance_bound_violation=max(0.0, lower_bound - first_term),
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


def _classes() -> list[ContractionClassRecord]:
    return [
        ContractionClassRecord(
            class_id="rank-one-elementary-symmetric-product-kernel",
            contraction_cost="O(mr) arithmetic and O(r) state",
            theorem_status="ruled-out-under-uniform-margin-mse-contract",
            finding="The first Hoeffding projection forces Omega(r^2 N/B) records for an equal target bucket.",
            next_obligation="Change tensor rank or estimator class; efficient rank-one contraction alone is insufficient.",
        ),
        ContractionClassRecord(
            class_id="polynomial-rank-sum-of-product-kernels",
            contraction_cost="potentially O(Rmr) for rank R",
            theorem_status="open",
            finding="Different rank components may cancel first projections while retaining the final margin.",
            next_obligation="Bound tensor rank, coefficient norm, projection cancellation, precision, and response margin jointly.",
        ),
        ContractionClassRecord(
            class_id="tensor-train-or-matrix-product-kernel",
            contraction_cost="polynomial when bond dimension and local maps are polynomial",
            theorem_status="open",
            finding="Low-bond contractions can represent more than sums of independent scalar powers.",
            next_obligation="Search low-bond kernels and reject any contraction whose bond or intermediate Fourier dimension is exponential.",
        ),
        ContractionClassRecord(
            class_id="adaptive-or-nonpolynomial-observation-functional",
            contraction_cost="unknown",
            theorem_status="open",
            finding="The rank-one power response H=F^r is no longer the correct model.",
            next_obligation="Formalize the statistic, access legality, arithmetic circuit size, and worst-instance error.",
        ),
        ContractionClassRecord(
            class_id="collective-quantum-measurement",
            contraction_cost="quantum circuit size and decoder cost",
            theorem_status="outside-classical-contraction-theorem",
            finding="Premeasurement entanglement is not a classical elementary-symmetric contraction.",
            next_obligation="Prove polynomial circuit size, exact f=1 robustness, and lattice composition.",
        ),
    ]


def run_factorized_contraction_report(
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    degrees: Sequence[int] = (2, 3, 4, 8, 16, 32),
    sample_budget_power: int = 3,
) -> DCPFactorizedContractionReport:
    certificates = [
        certify_rank_one_contraction(
            n_bits,
            degree,
            bucket_count,
            sample_budget_power=sample_budget_power,
        )
        for n_bits in n_values
        for degree in degrees
        if degree <= n_bits
        for bucket_count in _bucket_schedules(n_bits, sample_budget_power)
    ]
    finite_checks = [
        finite_rank_one_variance_check(4, degree, max(16, 4 * degree), bucket_count=4)
        for degree in (1, 2, 3, 4)
    ]
    polynomial_bucket_rows = [row for row in certificates if row.polynomial_bucket_enumeration]
    classes = _classes()
    metrics: dict[str, int | float] = {
        "certificate_count": len(certificates),
        "degree_count": len(set(row.degree for row in certificates)),
        "finite_variance_check_count": len(finite_checks),
        "finite_variance_check_failure_count": sum(row.variance_bound_violation > 1e-9 for row in finite_checks),
        "polynomial_bucket_count_row_count": len(polynomial_bucket_rows),
        "polynomial_bucket_rows_with_super_budget_samples": sum(
            not row.polynomial_samples_possible for row in polynomial_bucket_rows
        ),
        "joint_polynomial_resource_row_count": sum(row.joint_polynomial_resources_possible for row in certificates),
        "proved_rank_one_implicit_contraction_no_go_count": 1,
        "proved_polynomial_rank_contraction_lower_bound_count": 0,
        "proved_tensor_train_contraction_lower_bound_count": 0,
        "proved_collective_measurement_lower_bound_count": 0,
        "open_contraction_class_count": sum(item.theorem_status == "open" for item in classes),
    }
    falsifiers = [
        "Elementary-symmetric dynamic programming removes explicit tuple enumeration but not the first Hoeffding projection.",
        "A uniform bucket margin forces one complete class to have response magnitude at least gamma.",
        "Parseval then forces enough base-response energy to make rank-one sample complexity Omega(r^2 N/B).",
        "Every polynomial-bucket rank-one row in the sweep exceeds the polynomial record budget.",
        "The theorem does not cover cancellation among polynomially many rank components or low-bond tensor networks.",
    ]
    return DCPFactorizedContractionReport(
        created_at=utc_now(),
        model={
            "record_scalar": "z_j=y_j a(k_j) for one public label-weight function a",
            "kernel": "h(X_1,...,X_r)=product_j z_j",
            "response": "H(d)=F(d)^r where F(d)=E[z|d]",
            "contraction": "all-subsets U-statistic computed as an elementary symmetric polynomial in O(mr)",
            "target": "one bucket versus its complement with a uniform expected-response margin",
        },
        theorem={
            "large_response_class": "one side of any two-sided margin threshold has |H(d)|>=gamma throughout",
            "base_energy": "if that class has size L, Parseval gives E|a|^2=sum_d|F(d)|^2>=L gamma^(2/r)",
            "first_projection": "Var(U_m)>=r^2/m |F|^(2r-2)(4E|a|^2-|F|^2)",
            "sample_bound": "m>=12 r^2 L>=12 r^2 min(S,N-S) for uniform MSE<=gamma^2/4",
            "equal_bucket_consequence": "m=Omega(r^2 N/B), exponential for B=poly(log N)",
            "scope": "one rank-one factorized signed-product kernel with elementary-symmetric contraction",
        },
        certificates=certificates,
        finite_variance_checks=finite_checks,
        contraction_classes=classes,
        headline_metrics=metrics,
        claim_gate={
            "rank_one_implicit_contraction_no_go_proved": True,
            "finite_variance_checks_passed": metrics["finite_variance_check_failure_count"] == 0,
            "joint_polynomial_rank_one_row_found": metrics["joint_polynomial_resource_row_count"] > 0,
            "polynomial_rank_contraction_lower_bound_proved": False,
            "tensor_train_contraction_lower_bound_proved": False,
            "collective_measurement_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The simplest polynomial implicit contraction is sample-exponential. Higher tensor rank, low-bond "
                "networks, adaptive statistics, and collective measurements remain open and require separate audits."
            ),
        },
        status="rank-one-implicit-contraction-ruled-out-higher-rank-open",
        summary=(
            f"Certified {len(certificates)} rank-one contraction rows across "
            f"{len(set(row.degree for row in certificates))} degrees. Joint polynomial rows="
            f"{int(metrics['joint_polynomial_resource_row_count'])}; polynomial-rank lower bounds=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_factorized_contraction_report(
    path: Path = DCP_FACTORIZED_CONTRACTION_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    degrees: Sequence[int] = (2, 3, 4, 8, 16, 32),
    sample_budget_power: int = 3,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_factorized_contraction_report(
        n_values=n_values,
        degrees=degrees,
        sample_budget_power=sample_budget_power,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-IID-RANK-ONE-IMPLICIT-CONTRACTION",
                source=str(path),
                claim="Elementary-symmetric contraction of a rank-one product kernel gives a polynomial DCP bucket decoder.",
                reason_invalid=(
                    "Although the contraction costs O(mr), the first Hoeffding projection and response Parseval energy "
                    "force m>=12 r^2 min(S,N-S), exponential for coarse polynomially many buckets."
                ),
                lesson=(
                    "Do not retry scalar rank-one power kernels. Search polynomial-rank cancellations or low-bond tensor "
                    "networks with explicit norm, precision, margin, and intermediate-dimension accounting."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "certificate_count": payload["headline_metrics"]["certificate_count"],
                    "joint_polynomial_resource_row_count": payload["headline_metrics"][
                        "joint_polynomial_resource_row_count"
                    ],
                    "proved_polynomial_rank_contraction_lower_bound_count": 0,
                    "proved_tensor_train_contraction_lower_bound_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-FACTORIZED-CONTRACTION"
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
                artifacts={"dcp_factorized_contraction_audit": str(path)},
            )
        )
    return payload
