"""Audit the high-bit quotient distribution after polynomial low-bit conditioning."""

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


DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_conditioned_quotient.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ConditionedQuotientRow:
    n_bits: int
    register_count: int
    register_offset: int
    log_multiplier: int
    constrained_low_bits: int
    quotient_bits: int
    trial_index: int
    low_fiber_assignment_count: int
    quotient_state_count: int
    supported_quotient_count: int
    quotient_support_fraction: float
    shannon_entropy_bits: float
    normalized_shannon_entropy: float
    collision_effective_support: float
    normalized_collision_effective_support: float
    maximum_quotient_probability: float
    exact_target_quotient_probability: float
    polynomial_candidate_budget: int
    top_polynomial_candidate_mass: float
    inverse_polynomial_target_mass_observed: bool
    polynomial_candidate_concentration_observed: bool
    source_contract_satisfied: bool


@dataclass(frozen=True)
class DCPSubsetSumConditionedQuotientReport:
    created_at: str
    quotient_contract: dict[str, str]
    rows: list[ConditionedQuotientRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def analyze_conditioned_quotient(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
    trial_index: int,
    seed: int,
) -> ConditionedQuotientRow:
    if n_bits < 4:
        raise ValueError("n_bits must be at least 4")
    register_count = n_bits + register_offset
    constrained = min(n_bits - 1, max(1, math.ceil(log_multiplier * math.log2(n_bits))))
    quotient_bits = n_bits - constrained
    modulus = 1 << n_bits
    low_modulus = 1 << constrained
    quotient_states = 1 << quotient_bits
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    counts = subset_sum_counts(n_bits, labels)
    low_residue = target & (low_modulus - 1)
    quotient_counts = counts[low_residue::low_modulus].astype(np.float64)
    total = float(np.sum(quotient_counts))
    if total <= 0:
        probabilities = np.zeros(quotient_states, dtype=np.float64)
    else:
        probabilities = quotient_counts / total
    positive = probabilities[probabilities > 0.0]
    entropy = float(-np.sum(positive * np.log2(positive))) if positive.size else 0.0
    collision = float(np.sum(probabilities**2))
    effective_support = 1.0 / collision if collision > 0.0 else 0.0
    polynomial_budget = min(quotient_states, max(1, n_bits**3))
    if polynomial_budget == quotient_states:
        top_mass = float(np.sum(probabilities))
    else:
        partition = np.partition(probabilities, quotient_states - polynomial_budget)
        top_mass = float(np.sum(partition[-polynomial_budget:]))
    target_quotient = target >> constrained
    target_probability = float(probabilities[target_quotient])
    inverse_poly_threshold = n_bits ** -3
    return ConditionedQuotientRow(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        log_multiplier=log_multiplier,
        constrained_low_bits=constrained,
        quotient_bits=quotient_bits,
        trial_index=trial_index,
        low_fiber_assignment_count=int(total),
        quotient_state_count=quotient_states,
        supported_quotient_count=int(np.count_nonzero(quotient_counts)),
        quotient_support_fraction=float(np.count_nonzero(quotient_counts) / quotient_states),
        shannon_entropy_bits=entropy,
        normalized_shannon_entropy=entropy / quotient_bits,
        collision_effective_support=effective_support,
        normalized_collision_effective_support=effective_support / quotient_states,
        maximum_quotient_probability=float(np.max(probabilities)),
        exact_target_quotient_probability=target_probability,
        polynomial_candidate_budget=polynomial_budget,
        top_polynomial_candidate_mass=top_mass,
        inverse_polynomial_target_mass_observed=target_probability >= inverse_poly_threshold,
        polynomial_candidate_concentration_observed=top_mass >= inverse_poly_threshold,
        source_contract_satisfied=False,
    )


def run_conditioned_quotient_audit(
    n_values: Sequence[int] = (10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPSubsetSumConditionedQuotientReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows = [
        analyze_conditioned_quotient(
            n_bits,
            offset,
            multiplier,
            trial,
            seed + 1_000_003 * n_index + 10_007 * offset_index + 101 * multiplier_index + trial,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for multiplier_index, multiplier in enumerate(log_multipliers)
        for trial in range(trials_per_row)
    ]
    tail_n = max(n_values)
    tail_rows = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "tail_row_count": len(tail_rows),
        "minimum_normalized_shannon_entropy": min(row.normalized_shannon_entropy for row in rows),
        "minimum_tail_normalized_shannon_entropy": min(row.normalized_shannon_entropy for row in tail_rows),
        "minimum_tail_support_fraction": min(row.quotient_support_fraction for row in tail_rows),
        "minimum_tail_collision_effective_support_fraction": min(
            row.normalized_collision_effective_support for row in tail_rows
        ),
        "maximum_tail_exact_target_probability": max(row.exact_target_quotient_probability for row in tail_rows),
        "maximum_tail_top_polynomial_candidate_mass": max(row.top_polynomial_candidate_mass for row in tail_rows),
        "tail_inverse_polynomial_target_mass_row_count": sum(
            row.inverse_polynomial_target_mass_observed for row in tail_rows
        ),
        "tail_polynomial_candidate_concentration_row_count": sum(
            row.polynomial_candidate_concentration_observed for row in tail_rows
        ),
        "proved_uniform_high_entropy_quotient_count": 0,
        "proved_polynomial_high_bit_decoder_count": 0,
        "proved_high_bit_geometry_improvement_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumConditionedQuotientReport(
        created_at=utc_now(),
        quotient_contract={
            "conditioning": "uniform assignments x satisfying sum_i a_i x_i=t modulo 2^b",
            "quotient": "q=(sum_i a_i x_i-t)/2^b modulo 2^(n-b); the full witness requires q=0",
            "measurement": "exact multiplicity distribution from all full-modulus subset-sum counts at small n",
            "candidate_budget": "top n^3 quotient residues, deliberately generous polynomial explicit list",
            "promotion_requirement": "uniform entropy/concentration theorem plus a polynomial implicit decoder or changed lattice geometry",
        },
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "exact_conditioned_quotient_distribution_computed": True,
            "finite_high_entropy_is_lower_bound": False,
            "uniform_high_entropy_quotient_proved": False,
            "polynomial_high_bit_decoder_constructed": False,
            "high_bit_geometry_improvement_proved": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact finite audit tests whether logarithmic low-bit conditioning concentrates the remaining quotient. "
                "Any broad/high-entropy result is a falsifier for explicit high-residue lists, not a lower bound or decoder theorem."
            ),
        },
        status="conditioned-high-bit-quotient-audited-no-polynomial-decoder",
        summary=(
            f"Audited {len(rows)} exact conditioned quotient distributions through n={tail_n}; tail minimum normalized "
            f"entropy={metrics['minimum_tail_normalized_shannon_entropy']:.6g}, maximum target mass="
            f"{metrics['maximum_tail_exact_target_probability']:.6g}, and source-contract rows=0."
        ),
        falsifiers_triggered=[
            "Low-bit conditioning is tested against exact quotient multiplicities rather than assumed to reveal high bits.",
            "Top polynomial explicit quotient lists are charged and do not become implicit decoders.",
            "Finite high entropy rejects only concentration shortcuts; it is not a subset-sum lower bound.",
            "A useful preconditioner must prove changed high-bit lattice/representation geometry, not merely exact state preparation.",
        ],
    )


def write_conditioned_quotient_audit(
    path: Path = DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH,
    n_values: Sequence[int] = (10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_conditioned_quotient_audit(
        n_values, register_offsets, log_multipliers, trials_per_row, seed
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-LOW-BIT-CONDITIONING-AS-HIGH-BIT-CONCENTRATION-SHORTCUT",
                source=str(path),
                claim="Polynomial low-bit conditioning automatically concentrates the remaining quotient onto a polynomial explicit candidate set.",
                reason_invalid="Exact finite quotient distributions retain broad support/high entropy and no implicit high-bit decoder or geometry theorem is supplied.",
                lesson="Keep the BDD preconditioner, but require a mechanism that changes quotient geometry and prove it asymptotically.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "minimum_tail_normalized_shannon_entropy": payload["headline_metrics"]["minimum_tail_normalized_shannon_entropy"],
                    "maximum_tail_top_polynomial_candidate_mass": payload["headline_metrics"]["maximum_tail_top_polynomial_candidate_mass"],
                    "proved_high_bit_geometry_improvement_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT"
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
                artifacts={"dcp_subset_sum_conditioned_quotient": str(path)},
            )
        )
    return payload
