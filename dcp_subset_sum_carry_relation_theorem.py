"""Source-coverage obstruction for carry-sliced subset-sum embeddings.

Write a uniform label modulo ``2^n`` as independent low and high parts modulo
``B=2^b`` and ``Q=2^(n-b)``.  Choose an even support ``w<= (m+1)/4`` and
balanced signed vectors with ``h=w/2`` plus and minus entries, modulo global
negation.  Such a vector is a marker-zero carry-sliced lattice vector of norm
``sqrt(4w)`` whenever

    sum z_i low_i = 0 over the integers,
    sum z_i high_i = 0 modulo Q.

The first event is a collision between two sums of ``h`` uniform low labels.
Cauchy-Schwarz gives collision probability at least ``1/(hB)``; the high event
has probability ``1/Q``.  There are

    K = binom(m,w) binom(w,h) / 2

canonical relations, so ``E[X] >= K/(h 2^n)`` and its exponent at density one
is ``H_2(1/4)+1/4-1 > 0``.  For any two distinct canonical relations, a
nonzero 2x2 minor has absolute determinant one or two.  Conditioning on the
other low labels gives joint low probability at most ``B^-2``; Smith factors
give joint high probability at most ``2Q^-2``.  Hence

    E[X^2]/E[X]^2 <= 1/E[X] + 2h^2.

Paley-Zygmund proves inverse-quadratic source mass containing exponentially
many short competitors.  This rules out a uniform carry-sliced shortest-vector
isolation argument.  It does not prove high-probability competition, LLL/BKZ
failure, or rule out a marker-aware decoder on a different source subset.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_CARRY_RELATION_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_carry_relation_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-CARRY-RELATION-THEOREM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CarryRelationTheoremCertificate:
    family: str
    family_count_formula: str
    first_moment_lower_bound: str
    second_moment_ratio_upper_bound: str
    source_coverage_lower_bound: str
    asymptotic_log2_expectation_rate: float
    positive_expectation_exponent_proved: bool
    inverse_polynomial_source_coverage_proved: bool
    high_probability_source_coverage_proved: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class CarryRelationScalingRow:
    n_bits: int
    register_offset: int
    register_count: int
    constrained_low_bits: int
    low_modulus: int
    high_modulus: int
    support_weight: int
    positive_sign_count: int
    canonical_relation_count: int
    log2_first_moment_lower_bound: float
    first_moment_lower_bound_exceeds_one: bool
    second_moment_ratio_upper_bound: float
    paley_zygmund_source_coverage_lower_bound: float
    inverse_source_coverage_polynomial_upper_bound: float
    competitor_norm_squared: int
    planted_witness_norm_squared: int
    competitor_no_longer_than_planted: bool
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumCarryRelationReport:
    created_at: str
    source_contract: dict[str, str]
    theorem_certificate: CarryRelationTheoremCertificate
    rows: list[CarryRelationScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_entropy(value: float) -> float:
    if value <= 0 or value >= 1:
        return 0.0
    return -value * math.log2(value) - (1 - value) * math.log2(1 - value)


def theorem_support_weight(register_count: int) -> int:
    if register_count < 7:
        raise ValueError("register count must be at least seven")
    support = (register_count + 1) // 4
    support -= support % 2
    return max(2, support)


def balanced_canonical_relations(
    register_count: int,
    support_weight: int,
) -> list[tuple[int, ...]]:
    """Enumerate the balanced family for exact small-instance verification."""
    if support_weight < 2 or support_weight % 2 or support_weight > register_count:
        raise ValueError("support weight must be positive, even, and at most the register count")
    half = support_weight // 2
    rows: list[tuple[int, ...]] = []
    for support in combinations(range(register_count), support_weight):
        anchor = support[0]
        for positive_tail in combinations(support[1:], half - 1):
            positive = {anchor, *positive_tail}
            rows.append(tuple(1 if i in positive else -1 if i in support else 0 for i in range(register_count)))
    return rows


def balanced_relation_count(register_count: int, support_weight: int) -> int:
    if support_weight < 2 or support_weight % 2 or support_weight > register_count:
        raise ValueError("support weight must be positive, even, and at most the register count")
    return math.comb(register_count, support_weight) * math.comb(
        support_weight, support_weight // 2
    ) // 2


def is_carry_sliced_relation(
    relation: Sequence[int],
    low_labels: Sequence[int],
    high_labels: Sequence[int],
    high_modulus: int,
) -> bool:
    if len(relation) != len(low_labels) or len(relation) != len(high_labels):
        raise ValueError("relation and label lengths differ")
    if high_modulus <= 0:
        raise ValueError("high modulus must be positive")
    low_sum = sum(z * label for z, label in zip(relation, low_labels))
    high_sum = sum(z * label for z, label in zip(relation, high_labels))
    return low_sum == 0 and high_sum % high_modulus == 0


def run_carry_relation_theorem(
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    register_offset: int = 2,
    log_multiplier: int = 1,
) -> DCPSubsetSumCarryRelationReport:
    if log_multiplier < 1:
        raise ValueError("log multiplier must be positive")
    rows: list[CarryRelationScalingRow] = []
    for n_bits in n_values:
        if n_bits < 8:
            raise ValueError("n values must be at least eight")
        register_count = n_bits + register_offset
        low_bits = min(n_bits - 1, max(1, math.ceil(log_multiplier * math.log2(n_bits))))
        low_modulus = 1 << low_bits
        high_modulus = 1 << (n_bits - low_bits)
        support_weight = theorem_support_weight(register_count)
        half = support_weight // 2
        family_count = balanced_relation_count(register_count, support_weight)
        log2_mean_lower = math.log2(family_count) - math.log2(half) - n_bits
        inverse_mean_upper = 2 ** (-log2_mean_lower) if log2_mean_lower < 1_024 else 0.0
        second_ratio = inverse_mean_upper + 2 * half**2
        source_coverage = 1 / (4 * second_ratio)
        rows.append(
            CarryRelationScalingRow(
                n_bits=n_bits,
                register_offset=register_offset,
                register_count=register_count,
                constrained_low_bits=low_bits,
                low_modulus=low_modulus,
                high_modulus=high_modulus,
                support_weight=support_weight,
                positive_sign_count=half,
                canonical_relation_count=family_count,
                log2_first_moment_lower_bound=log2_mean_lower,
                first_moment_lower_bound_exceeds_one=log2_mean_lower > 0,
                second_moment_ratio_upper_bound=second_ratio,
                paley_zygmund_source_coverage_lower_bound=source_coverage,
                inverse_source_coverage_polynomial_upper_bound=1 / source_coverage,
                competitor_norm_squared=4 * support_weight,
                planted_witness_norm_squared=register_count + 1,
                competitor_no_longer_than_planted=4 * support_weight <= register_count + 1,
                finite_row_is_asymptotic_theorem=False,
            )
        )

    asymptotic_rate = binary_entropy(0.25) + 0.25 - 1
    certificate = CarryRelationTheoremCertificate(
        family="balanced signed vectors of even weight w<=floor((m+1)/4), modulo global negation",
        family_count_formula="binom(m,w)*binom(w,w/2)/2",
        first_moment_lower_bound="E[X] >= K/((w/2)*2^n)",
        second_moment_ratio_upper_bound="E[X^2]/E[X]^2 <= 1/E[X] + 2*(w/2)^2",
        source_coverage_lower_bound="Pr[X>=E[X]/2] >= 1/(4*(1/E[X]+2*(w/2)^2))",
        asymptotic_log2_expectation_rate=asymptotic_rate,
        positive_expectation_exponent_proved=asymptotic_rate > 0,
        inverse_polynomial_source_coverage_proved=True,
        high_probability_source_coverage_proved=False,
        proof=(
            "Cauchy-Schwarz on the at most h(B-1)+1 low subset-sum values gives low collision probability at least "
            "1/(hB); an odd high coefficient gives high relation probability 1/Q. Distinct canonical relation rows "
            "have a nonzero 2x2 minor of magnitude one or two, so their joint low probability is at most B^-2 and "
            "their joint high probability at most 2Q^-2. The displayed second-moment ratio and Paley-Zygmund bound "
            "follow. Since BQ=2^n, logarithmic slicing changes only polynomial factors."
        ),
        limitations=[
            "The proved source mass is inverse polynomial, not probability tending to one.",
            "The theorem rules out uniform shortest-vector isolation but not a decoder succeeding on another source subset.",
            "It does not characterize LLL or BKZ output distributions.",
            "A marker-aware extractor may still identify planted vectors among marker-zero competitors.",
        ],
    )
    tail = rows[-1]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "balanced_relation_family_theorem_count": 1,
        "positive_expectation_exponent_theorem_count": 1,
        "pairwise_joint_probability_bound_theorem_count": 1,
        "inverse_polynomial_source_coverage_theorem_count": 1,
        "high_probability_source_coverage_theorem_count": 0,
        "asymptotic_log2_expectation_rate": asymptotic_rate,
        "tail_log2_first_moment_lower_bound": tail.log2_first_moment_lower_bound,
        "tail_source_coverage_lower_bound": tail.paley_zygmund_source_coverage_lower_bound,
        "competitor_no_longer_than_planted_row_count": sum(
            row.competitor_no_longer_than_planted for row in rows
        ),
        "carry_sliced_uniform_shortest_vector_isolation_ruled_out_count": 1,
        "proved_lll_failure_probability_count": 0,
        "polynomial_marker_aware_decoder_count": 0,
    }
    return DCPSubsetSumCarryRelationReport(
        created_at=utc_now(),
        source_contract={
            "labels": "independent uniform labels modulo 2^n, split into independent low/high parts",
            "regime": "m=n+O(1), b=O(log n)",
            "embedding": "every target/carry member of the exact carry-sliced embedding family",
            "coverage": "inverse-polynomial source mass, not high probability",
        },
        theorem_certificate=certificate,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "carry_sliced_uniform_shortest_vector_isolation_valid": False,
            "inverse_polynomial_competitor_source_mass_proved": True,
            "high_probability_competitor_source_mass_proved": False,
            "lll_failure_probability_proved": False,
            "marker_aware_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Logarithmic low-bit slicing leaves inverse-polynomial source mass with exponentially many marker-zero "
                "competitors no longer than the witness. A surviving route needs a source-subset separation or a "
                "marker-aware extraction theorem."
            ),
        },
        status="carry-sliced-uniform-shortest-vector-isolation-obstructed",
        summary=(
            f"Proved inverse-polynomial source coverage for exponentially many carry-sliced competitors; asymptotic "
            f"expectation rate={asymptotic_rate:.6g}, tail log2 lower mean={tail.log2_first_moment_lower_bound:.6g}, "
            f"tail coverage lower bound={tail.paley_zygmund_source_coverage_lower_bound:.6g}."
        ),
        falsifiers_triggered=[
            "O(log n) exact low-bit slicing does not exponentially suppress balanced signed relations.",
            "The carry-sliced embedding cannot claim uniform planted shortest-vector isolation.",
            "The theorem does not establish high-probability competition or an LLL failure rate.",
            "A partial solver could still target a different inverse-polynomial source subset.",
        ],
    )


def write_carry_relation_theorem(
    path: Path = DCP_SUBSET_SUM_CARRY_RELATION_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    register_offset: int = 2,
    log_multiplier: int = 1,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_carry_relation_theorem(
            n_values=n_values,
            register_offset=register_offset,
            log_multiplier=log_multiplier,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-CARRY-SLICED-UNIFORM-SHORTEST-ISOLATION",
                source=str(path),
                claim=(
                    "Logarithmic low-bit carry slicing uniformly isolates the planted binary witness among shortest "
                    "vectors of the quotient embedding."
                ),
                reason_invalid=(
                    "A balanced signed-relation family retains positive exponential expectation and has a rigorous "
                    "inverse-polynomial Paley-Zygmund source-coverage bound."
                ),
                lesson=(
                    "Require a source-subset theorem that avoids the competitor event or a marker-aware extractor; do "
                    "not infer isolation from low-bit exactness or finite LLL success."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-CARRY-RELATION-THEOREM"
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
                artifacts={"dcp_subset_sum_carry_relation_theorem": str(path)},
            )
        )
    return payload
