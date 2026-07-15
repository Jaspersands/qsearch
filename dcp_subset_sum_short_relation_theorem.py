"""Short signed-relation obstruction for the standard subset-sum embedding.

Fix support size w=floor((m+1)/4).  For every w-subset S, take sign vectors on S
modulo global negation (fix the first support sign to +1).  There are
``M=2^(w-1)`` sign classes per support and ``N=binom(m,w)`` supports.  A class z
is a modular relation when ``sum_i z_i a_i=0 mod 2^n``.  It gives a marker-zero
standard-embedding vector of squared norm ``4w <= m+1``, no longer than the
planted binary witness.

For uniform labels, each event has probability 2^-n.  Two classes on different
supports have a unit 2x2 minor and joint probability 2^-2n.  Distinct classes on
one support have Smith factors (1,2) and joint probability 2*2^-2n.  Therefore

  E[X] = NM/P,
  Var(X)/E[X]^2 = 1/E[X] + (1-2/M)/N.

At m=n+c, log_2 E[X]/n tends to
``H_2(1/4)+1/4-1 > 0``.  Chebyshev proves exponentially many competing vectors
with probability tending to one.  This rules out planted shortest-vector
uniqueness in the standard embedding.  It does not analyze carry-sliced
constraints, BKZ output distributions, or witness extraction among competitors.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_SHORT_RELATION_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_short_relation_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-SHORT-RELATION-THEOREM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ShortRelationTheoremCertificate:
    support_fraction: float
    asymptotic_log2_expectation_rate: float
    positive_expectation_exponent_proved: bool
    different_support_unit_minor_proved: bool
    same_support_smith_one_two_proved: bool
    exact_relative_variance_formula: str
    high_probability_exponentially_many_competitors_proved: bool
    competitor_norm_no_larger_than_planted_proved: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class ShortRelationScalingRow:
    n_bits: int
    register_offset: int
    register_count: int
    support_weight: int
    support_count: int
    sign_classes_per_support: int
    log2_expected_relation_count: float
    expectation_exponent_per_n: float
    relative_variance_upper_bound: float
    chebyshev_zero_count_probability_upper_bound: float
    competitor_norm_squared: int
    planted_witness_norm_squared: int
    competitor_no_longer_than_planted: bool
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumShortRelationReport:
    created_at: str
    source_contract: dict[str, str]
    theorem_certificate: ShortRelationTheoremCertificate
    rows: list[ShortRelationScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_entropy(value: float) -> float:
    if value <= 0 or value >= 1:
        return 0.0
    return -value * math.log2(value) - (1 - value) * math.log2(1 - value)


def canonical_signed_relations(
    register_count: int,
    support_weight: int,
) -> list[tuple[int, ...]]:
    """Enumerate the theorem's relation family for exact small-instance checks."""
    if not 1 <= support_weight <= register_count:
        raise ValueError("support weight outside register range")
    relations: list[tuple[int, ...]] = []
    for support in combinations(range(register_count), support_weight):
        for tail_signs in product((-1, 1), repeat=support_weight - 1):
            relation = [0] * register_count
            relation[support[0]] = 1
            for index, sign in zip(support[1:], tail_signs):
                relation[index] = sign
            relations.append(tuple(relation))
    return relations


def relation_is_zero_modulus(
    relation: Sequence[int],
    labels: Sequence[int],
    modulus: int,
) -> bool:
    if len(relation) != len(labels):
        raise ValueError("relation and label lengths differ")
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return sum(coefficient * label for coefficient, label in zip(relation, labels)) % modulus == 0


def standard_relation_norm_squared(relation: Sequence[int]) -> int:
    """Squared norm after the standard embedding doubles relation coordinates."""
    return 4 * sum(coefficient * coefficient for coefficient in relation)


def short_relation_moments(
    n_bits: int,
    register_count: int,
    support_weight: int,
) -> tuple[int, int, float, float]:
    if not 1 <= support_weight <= register_count:
        raise ValueError("support weight outside register range")
    support_count = math.comb(register_count, support_weight)
    sign_classes = 1 << max(0, support_weight - 1)
    log2_mean = (
        math.log2(support_count) + math.log2(sign_classes) - n_bits
    )
    inverse_mean = 2 ** (-log2_mean) if log2_mean < 1_024 else 0.0
    relative_variance = inverse_mean + (1 - 2 / sign_classes) / support_count
    return support_count, sign_classes, log2_mean, relative_variance


def run_short_relation_theorem(
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    register_offset: int = 2,
) -> DCPSubsetSumShortRelationReport:
    rows = []
    for n_bits in n_values:
        register_count = n_bits + register_offset
        support_weight = max(1, (register_count + 1) // 4)
        support_count, sign_classes, log2_mean, relative_variance = (
            short_relation_moments(n_bits, register_count, support_weight)
        )
        competitor_norm_squared = 4 * support_weight
        planted_norm_squared = register_count + 1
        rows.append(
            ShortRelationScalingRow(
                n_bits=n_bits,
                register_offset=register_offset,
                register_count=register_count,
                support_weight=support_weight,
                support_count=support_count,
                sign_classes_per_support=sign_classes,
                log2_expected_relation_count=log2_mean,
                expectation_exponent_per_n=log2_mean / n_bits,
                relative_variance_upper_bound=relative_variance,
                chebyshev_zero_count_probability_upper_bound=min(1.0, relative_variance),
                competitor_norm_squared=competitor_norm_squared,
                planted_witness_norm_squared=planted_norm_squared,
                competitor_no_longer_than_planted=(
                    competitor_norm_squared <= planted_norm_squared
                ),
                finite_row_is_asymptotic_theorem=False,
            )
        )
    asymptotic_rate = binary_entropy(0.25) + 0.25 - 1
    certificate = ShortRelationTheoremCertificate(
        support_fraction=0.25,
        asymptotic_log2_expectation_rate=asymptotic_rate,
        positive_expectation_exponent_proved=asymptotic_rate > 0,
        different_support_unit_minor_proved=True,
        same_support_smith_one_two_proved=True,
        exact_relative_variance_formula="1/E[X] + (1-2/M)/N",
        high_probability_exponentially_many_competitors_proved=True,
        competitor_norm_no_larger_than_planted_proved=True,
        proof=(
            "Fix the first sign on each support to quotient global negation. Distinct equal-size supports have indices "
            "in both set differences, yielding a unit minor and independent zero-sum equations. Distinct sign classes "
            "on one support share odd support mod two but have a sign disagreement, giving Smith factors (1,2). The "
            "exact second moment yields relative variance 1/E[X]+(1-2/M)/N, which vanishes because "
            "H_2(1/4)+1/4-1>0."
        ),
        limitations=[
            "The theorem applies to the standard embedding's marker-zero sublattice.",
            "Carry-sliced low-coordinate constraints can eliminate these relations and require a separate count.",
            "Many short competitors do not by themselves prove LLL or BKZ cannot return a valid marker vector.",
            "No runtime lower bound for witness extraction is proved.",
        ],
    )
    tail = rows[-1]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "positive_expectation_exponent_theorem_count": 1,
        "exact_second_moment_theorem_count": 1,
        "high_probability_exponential_competitor_theorem_count": 1,
        "asymptotic_log2_expectation_rate": asymptotic_rate,
        "tail_log2_expected_relation_count": tail.log2_expected_relation_count,
        "tail_chebyshev_zero_count_probability_upper_bound": tail.chebyshev_zero_count_probability_upper_bound,
        "competitor_no_longer_than_planted_row_count": sum(
            row.competitor_no_longer_than_planted for row in rows
        ),
        "standard_embedding_shortest_vector_uniqueness_ruled_out_count": 1,
        "carry_sliced_short_relation_obstruction_count": 0,
        "proved_lll_failure_probability_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumShortRelationReport(
        created_at=utc_now(),
        source_contract={
            "labels": "independent uniform labels modulo 2^n",
            "embedding": "standard centered modular subset-sum lattice",
            "relation_family": "weight floor((m+1)/4) signed vectors modulo global negation",
            "conclusion": "exponentially many marker-zero vectors no longer than the planted witness with high probability",
        },
        theorem_certificate=certificate,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "standard_embedding_planted_shortest_vector_unique": False,
            "standard_embedding_has_exponentially_many_short_competitors": True,
            "carry_sliced_embedding_obstructed_by_same_relations": False,
            "lll_failure_probability_proved": False,
            "polynomial_witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The standard embedding has exponentially many marker-zero competitors no longer than the planted "
                "witness. A surviving lattice route must use additional constraints, distinguish marker structure, and "
                "prove extraction coverage rather than shortest-vector uniqueness."
            ),
        },
        status="standard-embedding-planted-shortest-vector-uniqueness-obstructed",
        summary=(
            f"Proved a high-probability exponential family of standard-embedding competitors with expectation rate "
            f"{asymptotic_rate:.6g}; tail log2 expected count={tail.log2_expected_relation_count:.6g}. Carry-sliced "
            "relations and LLL output probabilities remain open."
        ),
        falsifiers_triggered=[
            "The standard embedding cannot rely on the planted vector being uniquely shortest.",
            "Volume-scale ambiguity is strengthened to an explicit high-probability short-relation family.",
            "Finite LLL recovery does not remove exponentially many source-distributed marker-zero competitors.",
            "The theorem does not transfer automatically to carry-sliced low-coordinate constraints.",
        ],
    )


def write_short_relation_theorem(
    path: Path = DCP_SUBSET_SUM_SHORT_RELATION_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    register_offset: int = 2,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_short_relation_theorem(
        n_values=n_values,
        register_offset=register_offset,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-STANDARD-EMBEDDING-UNIQUE-SHORTEST-WITNESS",
                source=str(path),
                claim=(
                    "The planted binary marker vector is uniquely shortest, or isolated among shortest vectors, in the "
                    "standard density-one modular subset-sum embedding."
                ),
                reason_invalid=(
                    "A weight-one-quarter signed relation family has positive exponential expectation and vanishing "
                    "relative variance, producing exponentially many marker-zero vectors no longer than the witness."
                ),
                lesson=(
                    "Abandon standard shortest-vector uniqueness. Add constraints that eliminate signed relations or "
                    "prove a marker-aware extraction theorem despite competitors."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-SHORT-RELATION-THEOREM"
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
                artifacts={"dcp_subset_sum_short_relation_theorem": str(path)},
            )
        )
    return payload
