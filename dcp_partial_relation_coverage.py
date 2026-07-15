"""Coverage obstruction for explicit signed-difference partial fiber maps.

A signed relation z in {-1,0,1}^m with

    sum_j A_j z_j = 2^k mod 2^(k+1)

defines a partial child-fiber pairing: compatible x have x_j=0 when z_j=1
and x_j=1 when z_j=-1, and are mapped to x+z.  Its two oriented domains
cover at most 2^(1-|supp z|) of uniformly sampled assignments.

For independent uniform labels and any fixed nonzero z, the signed sum is
uniform modulo 2^(k+1).  A union bound over all supports of size at most beta*n
has exponent H_2(beta)+beta-alpha when k=alpha*n and m=n+O(1).  At
alpha=1/2 and beta=1/16 this exponent is negative.  Therefore every such
relation has linear support with exponentially high probability, and any
polynomial explicit dictionary has exponentially small subset-sample-weighted
coverage.

The theorem does not cover an implicitly computed relation indexed by each of
exponentially many target fibers, general non-translation maps, or quantum
walks whose transitions are not a polynomial dictionary of fixed masks.
"""

from __future__ import annotations

import itertools
import json
import math
import random
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


DCP_PARTIAL_RELATION_COVERAGE_PATH = Path(
    "research/phase_workbench/dcp_partial_relation_coverage.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-PARTIAL-RELATION-COVERAGE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class PartialRelationCoverageTheorem:
    theorem_id: str
    source: str
    relation_count: str
    single_relation_probability: str
    union_bound_exponent: str
    chosen_depth_fraction: float
    chosen_support_fraction: float
    asymptotic_exponent: float
    negative_exponent_proved: bool
    linear_minimum_support_with_high_probability_proved: bool
    polynomial_dictionary_exponential_coverage_bound_proved: bool
    scope_exclusions: list[str]


@dataclass(frozen=True)
class PartialRelationScalingRow:
    n_bits: int
    register_count: int
    depth: int
    maximum_ruled_out_support: int
    log2_relation_count: float
    log2_existence_union_bound: float
    existence_union_bound: float
    polynomial_dictionary_size: int
    log2_dictionary_source_coverage_bound: float
    dictionary_source_coverage_bound: float
    inverse_polynomial_existence_ruled_out: bool
    inverse_polynomial_dictionary_coverage_ruled_out: bool


@dataclass(frozen=True)
class PartialRelationFiniteRow:
    n_bits: int
    register_count: int
    depth: int
    trial_index: int
    minimum_relation_support: int | None
    minimum_relation_paired_domain_fraction: float
    searched_relation_count: int
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class PartialRelationCoverageReport:
    created_at: str
    theorem: PartialRelationCoverageTheorem
    scaling_rows: list[PartialRelationScalingRow]
    finite_rows: list[PartialRelationFiniteRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_entropy(value: float) -> float:
    if value <= 0.0 or value >= 1.0:
        return 0.0
    return -value * math.log2(value) - (1.0 - value) * math.log2(1.0 - value)


def signed_relation_sum(
    relation: Sequence[int], labels: Sequence[int], modulus: int
) -> int:
    if len(relation) != len(labels):
        raise ValueError("relation and labels must have equal length")
    return sum(z * label for z, label in zip(relation, labels)) % modulus


def relation_hits_next_bit(
    relation: Sequence[int], labels: Sequence[int], depth: int
) -> bool:
    return signed_relation_sum(relation, labels, 1 << (depth + 1)) == 1 << depth


def relation_paired_domain_fraction(relation: Sequence[int]) -> float:
    support = sum(value != 0 for value in relation)
    return min(1.0, 2.0 ** (1 - support)) if support else 0.0


def signed_relation_count(register_count: int, maximum_support: int) -> int:
    return sum(
        math.comb(register_count, support) * (1 << support)
        for support in range(1, maximum_support + 1)
    )


def minimum_signed_relation_support(
    labels: Sequence[int], depth: int
) -> tuple[int | None, int]:
    width = len(labels)
    searched = 0
    for support in range(1, width + 1):
        for indices in itertools.combinations(range(width), support):
            for signs in itertools.product((-1, 1), repeat=support):
                searched += 1
                relation = [0] * width
                for index, sign in zip(indices, signs):
                    relation[index] = sign
                if relation_hits_next_bit(relation, labels, depth):
                    return support, searched
    return None, searched


def build_coverage_theorem(
    depth_fraction: float = 0.5,
    support_fraction: float = 1 / 16,
) -> PartialRelationCoverageTheorem:
    exponent = binary_entropy(support_fraction) + support_fraction - depth_fraction
    return PartialRelationCoverageTheorem(
        theorem_id="THEOREM-DCP-EXPLICIT-PARTIAL-RELATION-COVERAGE",
        source="m=n+O(1) independent uniform labels modulo 2^n",
        relation_count="sum_{s<=beta*n} binom(m,s) 2^s",
        single_relation_probability="2^-(k+1), because any +/-1 coefficient makes the signed sum uniform",
        union_bound_exponent="H_2(beta)+beta-alpha+o(1) for k=alpha*n",
        chosen_depth_fraction=depth_fraction,
        chosen_support_fraction=support_fraction,
        asymptotic_exponent=exponent,
        negative_exponent_proved=exponent < 0,
        linear_minimum_support_with_high_probability_proved=exponent < 0,
        polynomial_dictionary_exponential_coverage_bound_proved=exponent < 0,
        scope_exclusions=[
            "target-indexed implicit families containing exponentially many distinct masks",
            "partial maps not expressible as fixed signed translations",
            "non-bijective relation samplers",
            "quantum walks with implicit global transition structure",
            "uniform-supported-target coverage without a source-law transfer",
        ],
    )


def scaling_row(
    n_bits: int,
    register_offset: int = 4,
    depth_fraction: float = 0.5,
    support_fraction: float = 1 / 16,
    dictionary_degree: int = 4,
) -> PartialRelationScalingRow:
    register_count = n_bits + register_offset
    depth = max(1, min(n_bits - 1, math.floor(depth_fraction * n_bits)))
    maximum_support = max(1, math.floor(support_fraction * n_bits))
    relation_count = signed_relation_count(register_count, maximum_support)
    log2_count = math.log2(relation_count)
    log2_existence = log2_count - (depth + 1)
    existence_bound = min(1.0, 2.0**log2_existence)
    dictionary_size = n_bits**dictionary_degree
    log2_coverage = 1.0 + math.log2(dictionary_size) - (maximum_support + 1)
    coverage_bound = min(1.0, 2.0**log2_coverage)
    threshold = n_bits**-2
    return PartialRelationScalingRow(
        n_bits=n_bits,
        register_count=register_count,
        depth=depth,
        maximum_ruled_out_support=maximum_support,
        log2_relation_count=log2_count,
        log2_existence_union_bound=log2_existence,
        existence_union_bound=existence_bound,
        polynomial_dictionary_size=dictionary_size,
        log2_dictionary_source_coverage_bound=log2_coverage,
        dictionary_source_coverage_bound=coverage_bound,
        inverse_polynomial_existence_ruled_out=existence_bound < threshold,
        inverse_polynomial_dictionary_coverage_ruled_out=coverage_bound < threshold,
    )


def finite_row(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
) -> PartialRelationFiniteRow:
    register_count = n_bits + register_offset
    if register_count > 12:
        raise ValueError("exact ternary enumeration is capped at 12 registers")
    depth = max(1, n_bits // 2)
    rng = random.Random(seed)
    labels = [rng.randrange(1 << n_bits) for _ in range(register_count)]
    support, searched = minimum_signed_relation_support(labels, depth)
    return PartialRelationFiniteRow(
        n_bits=n_bits,
        register_count=register_count,
        depth=depth,
        trial_index=trial_index,
        minimum_relation_support=support,
        minimum_relation_paired_domain_fraction=(
            2.0 ** (1 - support) if support is not None else 0.0
        ),
        searched_relation_count=searched,
        finite_row_is_asymptotic_theorem=False,
    )


def run_partial_relation_coverage_audit(
    n_values: Sequence[int] = (64, 128, 256, 512, 1024),
    register_offset: int = 4,
    finite_n_values: Sequence[int] = (6, 8, 10),
    finite_register_offset: int = 2,
    finite_trials: int = 2,
    seed: int = 0,
) -> PartialRelationCoverageReport:
    theorem = build_coverage_theorem()
    scaling_rows = [scaling_row(n, register_offset=register_offset) for n in n_values]
    finite_rows = [
        finite_row(
            n,
            finite_register_offset,
            trial,
            seed + 1_000_003 * n_index + trial,
        )
        for n_index, n in enumerate(finite_n_values)
        for trial in range(finite_trials)
    ]
    asymptotic_rows = [row for row in scaling_rows if row.n_bits >= 256]
    metrics: dict[str, int | float] = {
        "linear_minimum_support_theorem_count": int(
            theorem.linear_minimum_support_with_high_probability_proved
        ),
        "polynomial_dictionary_exponential_coverage_theorem_count": int(
            theorem.polynomial_dictionary_exponential_coverage_bound_proved
        ),
        "asymptotic_union_bound_exponent": theorem.asymptotic_exponent,
        "scaling_row_count": len(scaling_rows),
        "asymptotic_inverse_polynomial_existence_no_go_row_count": sum(
            row.inverse_polynomial_existence_ruled_out for row in asymptotic_rows
        ),
        "asymptotic_inverse_polynomial_dictionary_coverage_no_go_row_count": sum(
            row.inverse_polynomial_dictionary_coverage_ruled_out
            for row in asymptotic_rows
        ),
        "finite_row_count": len(finite_rows),
        "maximum_finite_minimum_relation_support": max(
            (row.minimum_relation_support or 0 for row in finite_rows), default=0
        ),
        "proved_target_indexed_implicit_map_no_go_count": 0,
        "proved_polynomial_relation_solver_count": 0,
    }
    return PartialRelationCoverageReport(
        created_at=utc_now(),
        theorem=theorem,
        scaling_rows=scaling_rows,
        finite_rows=finite_rows,
        headline_metrics=metrics,
        claim_gate={
            "polynomial_explicit_signed_relation_dictionary_route_alive": False,
            "target_indexed_implicit_partial_map_route_alive": True,
            "nontranslation_partial_map_route_alive": True,
            "polynomial_relation_solver_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "At linear depth, every fixed signed-difference relation has linear support with exponentially high "
                "probability, so polynomial explicit dictionaries have exponentially small subset-sample-weighted "
                "coverage. Exponentially indexed target-dependent maps and nontranslation relations remain open."
            ),
        },
        status="explicit-partial-relation-dictionaries-closed-implicit-target-indexed-route-open",
        summary=(
            f"Proved asymptotic signed-relation union-bound exponent {theorem.asymptotic_exponent:.6g} and closed "
            f"polynomial explicit dictionaries under subset-sample weighting. Finite rows={len(finite_rows)}; "
            "target-indexed implicit map no-go theorems=0."
        ),
        falsifiers_triggered=[
            "Inverse-polynomial coverage from one fixed translation requires logarithmic support, which is absent with exponentially high probability.",
            "A polynomial dictionary cannot compensate for the exponentially small domain of linear-support relations.",
            "Finite low-support relations do not override the negative asymptotic union-bound exponent.",
            "Subset-sample-weighted coverage is not silently substituted for uniform-supported-target coverage.",
            "The theorem leaves exponentially indexed target-dependent or nontranslation maps open.",
        ],
    )


def write_partial_relation_coverage_audit(
    path: Path = DCP_PARTIAL_RELATION_COVERAGE_PATH,
    n_values: Sequence[int] = (64, 128, 256, 512, 1024),
    register_offset: int = 4,
    finite_n_values: Sequence[int] = (6, 8, 10),
    finite_register_offset: int = 2,
    finite_trials: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_partial_relation_coverage_audit(
            n_values=n_values,
            register_offset=register_offset,
            finite_n_values=finite_n_values,
            finite_register_offset=finite_register_offset,
            finite_trials=finite_trials,
            seed=seed,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-POLYNOMIAL-SIGNED-RELATION-DICTIONARY-AS-PARTIAL-MAP",
                source=str(path),
                claim=(
                    "A polynomial dictionary of explicit signed-difference masks gives inverse-polynomial "
                    "source-weighted child-fiber pairing coverage at linear depth."
                ),
                reason_invalid=(
                    "With exponentially high probability every mask has linear support, hence exponentially small "
                    "compatible domain; polynomially many masks remain exponentially small in total."
                ),
                lesson=(
                    "Remove explicit signed-relation dictionaries from synthesis. A surviving partial map must be "
                    "implicitly target-indexed or nontranslation and must prove its exact source-law coverage."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or (
            f"RESULT-{registry_experiment_id}-DCP-PARTIAL-RELATION-COVERAGE"
        )
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
                artifacts={"dcp_partial_relation_coverage": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_partial_relation_coverage_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
