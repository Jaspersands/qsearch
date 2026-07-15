"""Exact legal-versus-planted target distribution audit for modular subset sum."""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_target_distribution.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-TARGET-DISTRIBUTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class TargetDistributionMomentCertificate:
    n_bits: int
    register_offset: int
    register_count: int
    expected_uniform_target_multiplicity: float
    expected_second_factorial_moment: float
    linear_threshold: int
    quadratic_threshold: int
    linear_threshold_probability_upper_bound: float
    quadratic_threshold_probability_upper_bound: float
    exact_first_moment_proved: bool
    exact_second_factorial_moment_proved: bool
    polynomial_tail_lower_bound_proved: bool
    statement: str


@dataclass(frozen=True)
class TargetDistributionRow:
    n_bits: int
    register_count: int
    register_offset: int
    trial_index: int
    target_count: int
    legal_target_count: int
    legal_target_fraction: float
    expected_uniform_target_multiplicity: float
    empirical_uniform_target_mean_multiplicity: float
    uniform_legal_mean_multiplicity: float
    planted_mean_multiplicity: float
    planted_to_uniform_legal_mean_ratio: float
    planted_vs_uniform_legal_total_variation: float
    poisson_total_variation: float
    empirical_second_factorial_moment: float
    theoretical_second_factorial_moment: float
    second_factorial_moment_ratio: float
    maximum_multiplicity: int
    linear_threshold: int
    quadratic_threshold: int
    uniform_target_linear_tail_probability: float
    uniform_legal_linear_tail_probability: float
    planted_linear_tail_probability: float
    uniform_target_quadratic_tail_probability: float
    uniform_legal_quadratic_tail_probability: float
    planted_quadratic_tail_probability: float
    source_contract_solver_constructed: bool


@dataclass(frozen=True)
class DCPSubsetSumTargetDistributionReport:
    created_at: str
    distribution_contract: dict[str, str]
    rows: list[TargetDistributionRow]
    moment_certificates: list[TargetDistributionMomentCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def moment_certificate(n_bits: int, register_offset: int) -> TargetDistributionMomentCertificate:
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    register_count = n_bits + register_offset
    modulus = 1 << n_bits
    assignment_count = 1 << register_count
    mean = assignment_count / modulus
    second_factorial = assignment_count * (assignment_count - 1) / (modulus * modulus)
    linear = max(2, n_bits)
    quadratic = max(2, n_bits * n_bits)
    return TargetDistributionMomentCertificate(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        expected_uniform_target_multiplicity=mean,
        expected_second_factorial_moment=second_factorial,
        linear_threshold=linear,
        quadratic_threshold=quadratic,
        linear_threshold_probability_upper_bound=min(
            1.0, second_factorial / (linear * (linear - 1))
        ),
        quadratic_threshold_probability_upper_bound=min(
            1.0, second_factorial / (quadratic * (quadratic - 1))
        ),
        exact_first_moment_proved=True,
        exact_second_factorial_moment_proved=True,
        polynomial_tail_lower_bound_proved=False,
        statement=(
            "For uniform A in Z_(2^n)^m and independent uniform target t, C_t=#{x:Ax=t} has "
            "E[C_t]=2^m/2^n. For x!=y, x-y contains a unit coefficient, so Ax=Ay with probability "
            "2^-n; hence E[C_t(C_t-1)]=2^m(2^m-1)/2^(2n). The resulting factorial-moment "
            "tail bound is an upper bound only and does not prove hardness or exclude inverse-polynomial rare targets."
        ),
    )


def _poisson_total_variation(counts: np.ndarray, mean: float) -> float:
    maximum = int(np.max(counts))
    histogram = np.bincount(counts.astype(np.int64), minlength=maximum + 1).astype(np.float64)
    empirical = histogram / counts.size
    probabilities = np.zeros(maximum + 1, dtype=np.float64)
    probabilities[0] = math.exp(-mean)
    for value in range(maximum):
        probabilities[value + 1] = probabilities[value] * mean / (value + 1)
    poisson_tail = max(0.0, 1.0 - float(np.sum(probabilities)))
    return 0.5 * (float(np.sum(np.abs(empirical - probabilities))) + poisson_tail)


def analyze_target_distribution(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
) -> TargetDistributionRow:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    assignment_count = 1 << register_count
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    counts = subset_sum_counts(n_bits, labels).astype(np.int64)
    legal_mask = counts > 0
    legal_counts = counts[legal_mask].astype(np.float64)
    legal_target_count = int(np.count_nonzero(legal_mask))
    uniform_legal_mean = float(np.mean(legal_counts)) if legal_target_count else 0.0
    planted_mean = float(np.sum(counts.astype(np.float64) ** 2) / assignment_count)
    uniform_legal = np.zeros(modulus, dtype=np.float64)
    if legal_target_count:
        uniform_legal[legal_mask] = 1.0 / legal_target_count
    planted = counts.astype(np.float64) / assignment_count
    planted_legal_tv = 0.5 * float(np.sum(np.abs(planted - uniform_legal)))
    certificate = moment_certificate(n_bits, register_offset)
    second_factorial = float(np.mean(counts.astype(np.float64) * (counts - 1)))

    def tail_probabilities(threshold: int) -> tuple[float, float, float]:
        mask = counts >= threshold
        uniform_target = float(np.count_nonzero(mask) / modulus)
        uniform_legal_probability = (
            float(np.count_nonzero(mask) / legal_target_count) if legal_target_count else 0.0
        )
        planted_probability = float(np.sum(counts[mask]) / assignment_count)
        return uniform_target, uniform_legal_probability, planted_probability

    linear_uniform, linear_legal, linear_planted = tail_probabilities(certificate.linear_threshold)
    quadratic_uniform, quadratic_legal, quadratic_planted = tail_probabilities(
        certificate.quadratic_threshold
    )
    return TargetDistributionRow(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        trial_index=trial_index,
        target_count=modulus,
        legal_target_count=legal_target_count,
        legal_target_fraction=legal_target_count / modulus,
        expected_uniform_target_multiplicity=certificate.expected_uniform_target_multiplicity,
        empirical_uniform_target_mean_multiplicity=float(np.mean(counts)),
        uniform_legal_mean_multiplicity=uniform_legal_mean,
        planted_mean_multiplicity=planted_mean,
        planted_to_uniform_legal_mean_ratio=(
            planted_mean / uniform_legal_mean if uniform_legal_mean else 0.0
        ),
        planted_vs_uniform_legal_total_variation=planted_legal_tv,
        poisson_total_variation=_poisson_total_variation(counts, certificate.expected_uniform_target_multiplicity),
        empirical_second_factorial_moment=second_factorial,
        theoretical_second_factorial_moment=certificate.expected_second_factorial_moment,
        second_factorial_moment_ratio=(
            second_factorial / certificate.expected_second_factorial_moment
            if certificate.expected_second_factorial_moment
            else 0.0
        ),
        maximum_multiplicity=int(np.max(counts)),
        linear_threshold=certificate.linear_threshold,
        quadratic_threshold=certificate.quadratic_threshold,
        uniform_target_linear_tail_probability=linear_uniform,
        uniform_legal_linear_tail_probability=linear_legal,
        planted_linear_tail_probability=linear_planted,
        uniform_target_quadratic_tail_probability=quadratic_uniform,
        uniform_legal_quadratic_tail_probability=quadratic_legal,
        planted_quadratic_tail_probability=quadratic_planted,
        source_contract_solver_constructed=False,
    )


def run_target_distribution_audit(
    n_values: Sequence[int] = (10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (0, 2, 4),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPSubsetSumTargetDistributionReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    certificates = [
        moment_certificate(n_bits, offset)
        for n_bits in n_values
        for offset in register_offsets
    ]
    rows = [
        analyze_target_distribution(
            n_bits,
            offset,
            trial,
            seed + 1_000_003 * ni + 10_007 * oi + trial,
        )
        for ni, n_bits in enumerate(n_values)
        for oi, offset in enumerate(register_offsets)
        for trial in range(trials_per_row)
    ]
    tail_n = max(n_values)
    tail_rows = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "moment_certificate_count": len(certificates),
        "exact_first_moment_certificate_count": sum(item.exact_first_moment_proved for item in certificates),
        "exact_second_factorial_moment_certificate_count": sum(
            item.exact_second_factorial_moment_proved for item in certificates
        ),
        "mean_tail_legal_target_fraction": sum(row.legal_target_fraction for row in tail_rows) / len(tail_rows),
        "mean_tail_planted_vs_uniform_legal_total_variation": sum(
            row.planted_vs_uniform_legal_total_variation for row in tail_rows
        ) / len(tail_rows),
        "maximum_tail_planted_to_uniform_legal_mean_ratio": max(
            row.planted_to_uniform_legal_mean_ratio for row in tail_rows
        ),
        "maximum_tail_uniform_target_linear_tail_probability": max(
            row.uniform_target_linear_tail_probability for row in tail_rows
        ),
        "maximum_tail_uniform_target_quadratic_tail_probability": max(
            row.uniform_target_quadratic_tail_probability for row in tail_rows
        ),
        "maximum_tail_planted_quadratic_tail_probability": max(
            row.planted_quadratic_tail_probability for row in tail_rows
        ),
        "mean_tail_poisson_total_variation": sum(row.poisson_total_variation for row in tail_rows) / len(tail_rows),
        "proved_inverse_polynomial_high_multiplicity_legal_subfamily_count": 0,
        "proved_polynomial_representation_solver_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumTargetDistributionReport(
        created_at=utc_now(),
        distribution_contract={
            "source_target": "independent uniform t in Z_(2^n), with success charged over the source legal-input distribution",
            "uniform_legal_target": "uniform over residues with at least one binary witness for fixed labels",
            "planted_target": "choose x uniformly and set t=Ax; this size-biases a target by its witness multiplicity",
            "representation_statistic": "binary witness multiplicity C_t; generalized representations require separate accounting",
            "promotion_requirement": (
                "detectable inverse-polynomial source-target subfamily plus a polynomial witness algorithm and matching interface"
            ),
        },
        rows=rows,
        moment_certificates=certificates,
        headline_metrics=metrics,
        claim_gate={
            "uniform_legal_and_planted_targets_separated": True,
            "exact_first_two_factorial_moments_proved": (
                metrics["exact_first_moment_certificate_count"] == len(certificates)
                and metrics["exact_second_factorial_moment_certificate_count"] == len(certificates)
            ),
            "finite_poisson_similarity_is_asymptotic_theorem": False,
            "polynomial_multiplicity_tail_excluded": False,
            "inverse_polynomial_high_multiplicity_legal_subfamily_proved": False,
            "polynomial_representation_solver_constructed": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Planted targets are explicitly size-biased and cannot stand in for the source distribution. Exact first "
                "and second moments constrain but do not exclude inverse-polynomial rare high-multiplicity targets, and no "
                "polynomial representation solver is constructed."
            ),
        },
        status="target-distributions-separated-representation-solver-open",
        summary=(
            f"Audited {len(rows)} full target tables through n={tail_n}. Mean tail planted-versus-uniform-legal TV="
            f"{metrics['mean_tail_planted_vs_uniform_legal_total_variation']:.6g}, maximum uniform-target quadratic-tail "
            f"probability={metrics['maximum_tail_uniform_target_quadratic_tail_probability']:.6g}, and source-contract solvers=0."
        ),
        falsifiers_triggered=[
            "Planted-witness targets are not treated as uniform legal targets.",
            "Representation multiplicity is measured over the entire target table, not selected successful instances.",
            "Exact factorial moments are used only as upper bounds and do not become hardness claims.",
            "Finite Poisson similarity does not prove an asymptotic law or rule out inverse-polynomial rare subfamilies.",
            "Multiplicity without an efficient detectable witness algorithm is not a partial solver.",
        ],
    )


def write_target_distribution_audit(
    path: Path = DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH,
    n_values: Sequence[int] = (10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (0, 2, 4),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_target_distribution_audit(n_values, register_offsets, trials_per_row, seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-PLANTED-TARGET-REPRESENTATION-SIZE-BIAS",
                source=str(path),
                claim=(
                    "High representation multiplicity observed on planted-witness subset-sum targets transfers directly "
                    "to Regev's uniform source-target distribution."
                ),
                reason_invalid=(
                    "Planting samples targets proportional to witness multiplicity. The exact audit separates this "
                    "size-biased law from uniform legal and independent uniform source targets."
                ),
                lesson=(
                    "Evaluate representation attacks on independent uniform targets and charge legal-input coverage. A "
                    "rare subfamily must be efficiently detectable and have a polynomial witness algorithm."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "mean_tail_planted_vs_uniform_legal_total_variation": payload["headline_metrics"][
                        "mean_tail_planted_vs_uniform_legal_total_variation"
                    ],
                    "maximum_tail_uniform_target_quadratic_tail_probability": payload["headline_metrics"][
                        "maximum_tail_uniform_target_quadratic_tail_probability"
                    ],
                    "proved_polynomial_representation_solver_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-TARGET-DISTRIBUTION"
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
                artifacts={"dcp_subset_sum_target_distribution": str(path)},
            )
        )
    return payload
