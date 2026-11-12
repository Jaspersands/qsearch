"""Global Plancherel collision reduction for natural wreath tuples.

A natural physical label is built from two independent Plancherel partitions.
At k=ceil(log2(n!)) copies, the full source therefore consists of 2k iid
Plancherel draws before unordered pair packaging.

If C_n=sum_lambda p_lambda^2 is the Plancherel collision probability, then

    Pr(any repeated source partition)
        <= binom(2k,2) C_n.

The maximal Plancherel atom theorem gives
C_n<=max_lambda p_lambda=exp(-Theta(sqrt(n))).  Since k=Theta(n log n), the
right side tends to zero.  Thus the natural asymptotic critical path is not
an arbitrary all-unequal tuple: with probability 1-o(1), all 2k source
partitions are globally distinct.

This removes repeated-label low-dimensional counterexamples, including the
W_3 trivial-sign unequal block whose norm remains 1/2.  It does not prove a
norm bound for collision-free tuples.  The next theorem must exploit
representation diversity without enumerating an exponentially large
partition portfolio.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_character_moments import (
    PhysicalWreathIrrepDescriptor,
)
from self_dual_wreath_natural_unequal_dominance import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
    plancherel_probabilities,
    physical_label_type_masses,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_global_partition_collision.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class GlobalCollisionRecord:
    n: int
    partition_count: int
    copy_count: int
    source_partition_draw_count: int
    exact_pair_collision_probability: str
    pair_collision_probability: float
    collision_pair_union_coefficient: int
    union_bound_any_global_collision: float
    exact_all_distinct_probability: float
    exact_occupancy_computed: bool
    all_distinct_probability_lower_bound: float
    finite_all_distinct_dominance_verified: bool
    status: str


@dataclass(frozen=True)
class CounterexampleExclusionRecord:
    label_ids: tuple[str, ...]
    source_partition_occurrence_count: int
    distinct_source_partition_count: int
    globally_distinct: bool
    maximum_frame_eigenvalue: float
    excluded_by_global_distinct_event: bool
    status: str


@dataclass(frozen=True)
class GlobalPartitionCollisionReport:
    created_at: str
    source_law_contract: dict[str, Any]
    literature_linked_theorem: dict[str, Any]
    records: list[GlobalCollisionRecord]
    counterexample_exclusions: list[CounterexampleExclusionRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_all_distinct_probability(n: int, draw_count: int) -> float:
    """Return the ordered no-collision probability by stable DP."""

    probabilities = tuple(
        float(mass) for _, mass in plancherel_probabilities(n)
    )
    if draw_count > len(probabilities):
        return 0.0
    ordered = [0.0] * (draw_count + 1)
    ordered[0] = 1.0
    processed = 0
    for probability in probabilities:
        processed += 1
        for selected in range(min(draw_count, processed), 0, -1):
            ordered[selected] += (
                selected * probability * ordered[selected - 1]
            )
    return min(1.0, max(0.0, ordered[draw_count]))


def global_collision_record(
    n: int,
    compute_exact_occupancy: bool = True,
) -> GlobalCollisionRecord:
    probabilities = plancherel_probabilities(n)
    collision, _ = physical_label_type_masses(n)
    copy_count = math.ceil(math.log2(math.factorial(n)))
    draw_count = 2 * copy_count
    pair_count = math.comb(draw_count, 2)
    union_bound = min(1.0, pair_count * float(collision))
    exact = (
        exact_all_distinct_probability(n, draw_count)
        if compute_exact_occupancy
        else math.nan
    )
    lower = max(0.0, 1.0 - union_bound)
    return GlobalCollisionRecord(
        n=n,
        partition_count=len(probabilities),
        copy_count=copy_count,
        source_partition_draw_count=draw_count,
        exact_pair_collision_probability=str(collision),
        pair_collision_probability=float(collision),
        collision_pair_union_coefficient=pair_count,
        union_bound_any_global_collision=union_bound,
        exact_all_distinct_probability=exact,
        exact_occupancy_computed=compute_exact_occupancy,
        all_distinct_probability_lower_bound=lower,
        finite_all_distinct_dominance_verified=lower >= 0.9,
        status=(
            "finite-global-distinct-dominance"
            if lower >= 0.9
            else "finite-collision-bound-not-yet-conclusive"
        ),
    )


def source_partitions_globally_distinct(
    descriptors: Iterable[PhysicalWreathIrrepDescriptor],
) -> bool:
    partitions: list[tuple[int, ...]] = []
    for descriptor in descriptors:
        partitions.extend(
            (descriptor.left_partition, descriptor.right_partition)
        )
    return len(partitions) == len(set(partitions))


def known_repeated_source_counterexample() -> CounterexampleExclusionRecord:
    labels = (
        "UNEQ-3__1-1-1",
        "UNEQ-3__1-1-1",
        "UNEQ-3__1-1-1",
    )
    return CounterexampleExclusionRecord(
        label_ids=labels,
        source_partition_occurrence_count=6,
        distinct_source_partition_count=2,
        globally_distinct=False,
        maximum_frame_eigenvalue=0.5,
        excluded_by_global_distinct_event=True,
        status="repeated-source-half-norm-counterexample-excluded",
    )


def run_global_partition_collision() -> GlobalPartitionCollisionReport:
    records = [
        global_collision_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32)
    ]
    counterexamples = [known_repeated_source_counterexample()]
    metrics: dict[str, int | float] = {
        "global_collision_control_count": len(records),
        "maximum_exact_occupancy_n": max(record.n for record in records),
        "global_source_draw_as_iid_plancherel_theorem_count": 1,
        "global_collision_union_bound_theorem_count": 1,
        "asymptotic_global_all_distinct_dominance_theorem_count": 1,
        "finite_ninety_percent_global_distinct_row_count": sum(
            record.finite_all_distinct_dominance_verified
            for record in records
        ),
        "repeated_source_half_norm_counterexample_count": len(
            counterexamples
        ),
        "repeated_source_counterexample_exclusion_count": sum(
            record.excluded_by_global_distinct_event
            for record in counterexamples
        ),
        "collision_free_tuple_norm_theorem_count": 0,
        "collision_free_growing_moment_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    tail = records[-1]
    return GlobalPartitionCollisionReport(
        created_at=utc_now(),
        source_law_contract={
            "unpackaged_source": (
                "k natural physical labels are 2k iid Plancherel partitions "
                "before unordered pair packaging"
            ),
            "global_collision_bound": (
                "Pr(any repeat)<=binom(2k,2) C_n, "
                "C_n=sum_lambda p_lambda^2"
            ),
            "asymptotic_decay": (
                "C_n<=max p_lambda=exp(-Theta(sqrt(n))) while "
                "k=Theta(n log n), hence k^2 C_n=o(1)"
            ),
            "critical_path": (
                "prove the frame norm or growing moment for arbitrary tuples "
                "whose 2k source partitions are globally distinct"
            ),
        },
        literature_linked_theorem={
            "literature_id": MAXIMAL_DIMENSION_PAPER_ID,
            "url": MAXIMAL_DIMENSION_PAPER_URL,
            "result_used": (
                "max_lambda d_lambda=sqrt(n!) "
                "exp(-(constant+o(1))sqrt(n))"
            ),
            "derived_consequence": (
                "the maximal Plancherel atom and therefore C_n decay as "
                "exp(-Theta(sqrt(n)))"
            ),
        },
        records=records,
        counterexample_exclusions=counterexamples,
        headline_metrics=metrics,
        claim_gate={
            "global_source_draws_are_iid_plancherel": True,
            "global_collision_union_bound_proved": True,
            "asymptotic_global_all_distinct_dominance_proved": True,
            "known_repeated_source_half_norm_counterexample_excluded": True,
            "collision_free_tuple_norm_bound_proved": False,
            "collision_free_growing_moment_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Global source collisions vanish asymptotically and remove "
                "known repeated-label counterexamples, but no norm theorem "
                "exists for arbitrary collision-free representation tuples."
            ),
        },
        status=(
            "global-plancherel-collisions-asymptotically-vanish-"
            "collision-free-norm-open"
        ),
        summary=(
            "Proved that natural threshold tuples have globally distinct "
            "source partitions with probability 1-o(1), excluding the known "
            "repeated-source 1/2-norm block; finite controls through n="
            f"{tail.n} remain preasymptotic."
        ),
        falsifiers_triggered=[
            "Within-label inequality is weaker than global distinctness across all 2k source partitions.",
            "The information-threshold copy count is polynomial and cannot overcome exponential collision decay.",
            "Known W3 half-norm unequal counterexamples reuse source partitions and are asymptotically negligible.",
            "Finite n controls remain preasymptotic and are not evidence of early global-distinct dominance.",
            "Global distinctness alone does not prove frame-norm decay.",
            "No collision-free contraction, measurement circuit, decoder, or classical separation is claimed.",
        ],
    )


def write_global_partition_collision_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_global_partition_collision())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-WREATH-ALL-UNEQUAL-"
                    "NOT-GLOBALLY-DISTINCT"
                ),
                source=str(path),
                claim=(
                    "Within-label inequality is the strongest natural source "
                    "conditioning needed for growing frame moments."
                ),
                reason_invalid=(
                    "The full source is 2k iid Plancherel draws. Repeated "
                    "partitions across labels are asymptotically absent and "
                    "support known finite half-norm counterexamples."
                ),
                lesson=(
                    "Target arbitrary collision-free source tuples and discard "
                    "the o(1) global-collision event before seeking a uniform "
                    "tensor contraction."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-NATURAL-ACCESS",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_global_partition_collision": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_global_partition_collision_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
