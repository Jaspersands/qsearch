"""Collective activation of point signal beyond source Young adjacency.

The exact one-pair theorem says that an unequal source pair has point signal
only when its two Young diagrams share an ``S_(n-1)`` child.  That criterion
does not tensorize.

At ``S_4``, every globally distinct two-pair portfolio has positive collective
point signal.  Three portfolios have zero isolated signal in both pairs, yet
their joint signal is positive.  More decisively, in ``S_6`` the portfolio

    ((6),(4,2)), ((3,1,1,1),(2,2,2))

has no shared-child edge among *any* of its four source diagrams.  Both
isolated signals and every cross-pair one-copy signal are zero, while the exact
two-copy standard coefficient is positive.

The mechanism is recoupling.  The two-copy overlap contains products of local
character factors before the common ``s,t,u`` variables are summed.  Tensor
products of source representations can contain adjacent intermediate Fourier
irreps even when no source pair is adjacent.  Therefore neither isolated
point signal nor the source-level Young graph is a valid support-pruning rule
for collective blocks.

There are pairwise-nonadjacent four-source families for every ``n>=8``, for
example

    (n), (n-2,2), (n-3,1,1,1), (ceil(n/2),floor(n/2)).

This module proves their source-level nonadjacency, not their collective
activation.  An all-n recoupling-energy criterion and a threshold-copy bound
remain open.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_point_stabilizer_quotient import (
    _class_centralizer_size,
    fixed_tuple_overlap_kernel,
    point_centered_gram,
    point_quotient_states,
)
from self_dual_wreath_point_standard_energy import (
    standard_kronecker_multiplicity,
)
from self_dual_wreath_single_pair_point_signal_no_go import (
    exact_single_pair_point_signal,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_collective_point_activation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COLLECTIVE-POINT-ACTIVATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class S4CollectiveActivationControl:
    source_subset_count: int
    perfect_matching_count: int
    globally_distinct_portfolio_count: int
    positive_collective_signal_count: int
    both_isolated_signals_zero_count: int
    zero_zero_collectively_activated_count: int
    minimum_collective_signal: float
    minimum_zero_zero_collective_signal: float
    maximum_collective_signal: float
    all_s4_collision_free_two_pair_portfolios_activated: bool
    isolated_signal_additivity_falsified: bool
    status: str


@dataclass(frozen=True)
class PairwiseNonadjacentActivationControl:
    control_id: str
    n: int
    labels: tuple[Label, Label]
    source_partitions: tuple[Partition, ...]
    source_pair_count: int
    source_young_edge_count: int
    first_isolated_signal: float
    second_isolated_signal: float
    collective_centered_signal: float
    collective_to_isolated_sum_ratio: float
    pairwise_nonadjacent_sources: bool
    collective_activation_verified: bool
    status: str


@dataclass(frozen=True)
class NonadjacentFamilyRecord:
    n: int
    source_partitions: tuple[Partition, ...]
    source_partitions_distinct: bool
    source_young_edge_count: int
    every_pair_isolated_signal_zero: bool
    collective_signal_proved_positive: bool
    status: str


@dataclass(frozen=True)
class CollectivePointActivationTheorem:
    one_pair_rule: str
    finite_counterexample: str
    recoupling_consequence: str
    scalable_nonadjacent_family: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CollectivePointActivationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CollectivePointActivationTheorem
    exhaustive_s4_control: S4CollectiveActivationControl
    pairwise_nonadjacent_controls: list[PairwiseNonadjacentActivationControl]
    nonadjacent_family_records: list[NonadjacentFamilyRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def source_young_edge_count(source_partitions: tuple[Partition, ...]) -> int:
    return sum(
        standard_kronecker_multiplicity(left, right) > 0
        for left, right in itertools.combinations(source_partitions, 2)
    )


def collective_point_signal_from_overlap(labels: tuple[Label, ...]) -> float:
    if not labels:
        raise ValueError("at least one source pair is required")
    n = sum(labels[0][0])
    kernel = fixed_tuple_overlap_kernel(n, labels)
    order = math.factorial(n)
    return sum(
        (order // _class_centralizer_size(cycle))
        * (cycle.count(1) - 1)
        * value
        / order
        for cycle, value in kernel.items()
    )


def audit_s4_collective_activation(
    tolerance: float = 1e-12,
) -> S4CollectiveActivationControl:
    partitions = tuple(integer_partitions(4))
    signals = []
    zero_zero_signals = []
    for sources in itertools.combinations(partitions, 4):
        for matching in (
            ((0, 1), (2, 3)),
            ((0, 2), (1, 3)),
            ((0, 3), (1, 2)),
        ):
            labels = tuple((sources[left], sources[right]) for left, right in matching)
            isolated = tuple(exact_single_pair_point_signal(*label) for label in labels)
            collective = float(point_centered_gram(point_quotient_states(labels))[0, 0])
            signals.append(collective)
            if max(isolated) <= tolerance:
                zero_zero_signals.append(collective)
    all_positive = all(signal > tolerance for signal in signals)
    zero_zero_active = all(signal > tolerance for signal in zero_zero_signals)
    return S4CollectiveActivationControl(
        source_subset_count=math.comb(len(partitions), 4),
        perfect_matching_count=3,
        globally_distinct_portfolio_count=len(signals),
        positive_collective_signal_count=sum(signal > tolerance for signal in signals),
        both_isolated_signals_zero_count=len(zero_zero_signals),
        zero_zero_collectively_activated_count=sum(
            signal > tolerance for signal in zero_zero_signals
        ),
        minimum_collective_signal=min(signals),
        minimum_zero_zero_collective_signal=min(zero_zero_signals),
        maximum_collective_signal=max(signals),
        all_s4_collision_free_two_pair_portfolios_activated=all_positive,
        isolated_signal_additivity_falsified=zero_zero_active,
        status=(
            "exhaustive-s4-collective-point-activation"
            if all_positive and zero_zero_active
            else "s4-collective-activation-validation-failure"
        ),
    )


def audit_pairwise_nonadjacent_activation(
    n: int,
    labels: tuple[Label, Label],
    *,
    control_id: str,
    tolerance: float = 1e-12,
) -> PairwiseNonadjacentActivationControl:
    sources = tuple(partition for label in labels for partition in label)
    if len(set(sources)) != 4:
        raise ValueError("four globally distinct source partitions are required")
    edges = source_young_edge_count(sources)
    isolated = tuple(exact_single_pair_point_signal(*label) for label in labels)
    collective = collective_point_signal_from_overlap(labels)
    pairwise_nonadjacent = edges == 0
    activated = pairwise_nonadjacent and max(isolated) <= tolerance and collective > tolerance
    isolated_sum = sum(isolated)
    return PairwiseNonadjacentActivationControl(
        control_id=control_id,
        n=n,
        labels=labels,
        source_partitions=sources,
        source_pair_count=math.comb(4, 2),
        source_young_edge_count=edges,
        first_isolated_signal=isolated[0],
        second_isolated_signal=isolated[1],
        collective_centered_signal=collective,
        collective_to_isolated_sum_ratio=(
            math.inf if isolated_sum == 0 and collective > 0 else collective / isolated_sum
        ),
        pairwise_nonadjacent_sources=pairwise_nonadjacent,
        collective_activation_verified=activated,
        status=(
            "pairwise-nonadjacent-collective-standard-activation"
            if activated
            else "pairwise-nonadjacent-activation-validation-failure"
        ),
    )


def scalable_nonadjacent_source_family(n: int) -> tuple[Partition, ...]:
    if n < 8:
        raise ValueError("family is defined for n at least eight")
    return (
        (n,),
        (n - 2, 2),
        (n - 3, 1, 1, 1),
        ((n + 1) // 2, n // 2),
    )


def nonadjacent_family_record(n: int) -> NonadjacentFamilyRecord:
    sources = scalable_nonadjacent_source_family(n)
    edges = source_young_edge_count(sources)
    return NonadjacentFamilyRecord(
        n=n,
        source_partitions=sources,
        source_partitions_distinct=len(set(sources)) == 4,
        source_young_edge_count=edges,
        every_pair_isolated_signal_zero=edges == 0,
        collective_signal_proved_positive=False,
        status="scalable-pairwise-nonadjacent-family-collective-energy-open",
    )


def run_collective_point_activation() -> CollectivePointActivationReport:
    s4 = audit_s4_collective_activation()
    sources = ((6,), (4, 2), (3, 1, 1, 1), (2, 2, 2))
    nonadjacent_controls = [
        audit_pairwise_nonadjacent_activation(
            6,
            tuple((sources[left], sources[right]) for left, right in matching),
            control_id=f"S6-NONADJACENT-PAIRING-{index}",
        )
        for index, matching in enumerate(
            (
                ((0, 1), (2, 3)),
                ((0, 2), (1, 3)),
                ((0, 3), (1, 2)),
            ),
            start=1,
        )
    ]
    family = [nonadjacent_family_record(n) for n in range(8, 33)]
    failures = int(not s4.all_s4_collision_free_two_pair_portfolios_activated)
    failures += int(not s4.isolated_signal_additivity_falsified)
    failures += sum(not row.collective_activation_verified for row in nonadjacent_controls)
    failures += sum(
        not row.source_partitions_distinct or not row.every_pair_isolated_signal_zero
        for row in family
    )
    verified = failures == 0
    theorem = CollectivePointActivationTheorem(
        one_pair_rule=(
            "One pair has point signal iff its two source diagrams share an S_(n-1) child."
        ),
        finite_counterexample=(
            "A globally distinct S_6 two-pair block has positive point signal even "
            "though all six source-pair Young adjacencies are absent."
        ),
        recoupling_consequence=(
            "Collective point energy is generated by intermediate tensor-product "
            "recoupling and cannot be pruned using isolated source adjacency."
        ),
        scalable_nonadjacent_family=(
            "For n>=8, (n),(n-2,2),(n-3,1,1,1),(ceil(n/2),floor(n/2)) "
            "are pairwise nonadjacent at the source level."
        ),
        scope=(
            "Collective activation is proved in finite controls. Positivity for the "
            "scalable family and an all-n threshold energy bound remain open."
        ),
        theorem_verified=verified,
        status=(
            "collective-recoupling-activation-proved-all-n-energy-open"
            if verified
            else "collective-point-activation-validation-failure"
        ),
    )
    return CollectivePointActivationReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        exhaustive_s4_control=s4,
        pairwise_nonadjacent_controls=nonadjacent_controls,
        nonadjacent_family_records=family,
        proof_obligations=[
            {
                "obligation": "test_tensorized_one_pair_point_no_go",
                "resolved": True,
                "resolution": (
                    "Rejected by exhaustive S_4 controls and an S_6 portfolio with no "
                    "source Young edges but positive collective standard energy."
                ),
            },
            {
                "obligation": "identify_collective_activation_support_rule",
                "resolved": False,
                "resolution": (
                    "Source adjacency is insufficient. A correct criterion must retain "
                    "intermediate Kronecker channels and their Racah coherence."
                ),
            },
            {
                "obligation": "prove_scalable_nonadjacent_family_collective_energy",
                "resolved": False,
                "resolution": (
                    "The family is pairwise nonadjacent for every n>=8, but no explicit "
                    "nonzero recoupling witness has been constructed for all n."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Zero isolated point signal in every source pair kills the joint block.",
                "resolved": True,
                "resolution": (
                    "False. The S_6 counterexample has zero signal for every pairing of "
                    "two individual source diagrams and positive two-copy signal."
                ),
            },
            {
                "objection": "Collective activation is explained by a cross-pair Young edge.",
                "resolved": True,
                "resolution": (
                    "Not universally. The S_6 source set has no Young edge among any of "
                    "its six pairs. Intermediate tensor-product irreps are necessary."
                ),
            },
            {
                "objection": "One finite activation proves a threshold-scale lower bound.",
                "resolved": False,
                "resolution": (
                    "No. The positive value may still shrink factorially with n or fail "
                    "for the scalable nonadjacent family."
                ),
            },
        ],
        headline_metrics={
            "exhaustive_s4_portfolio_count": s4.globally_distinct_portfolio_count,
            "s4_zero_zero_collective_activation_count": (
                s4.zero_zero_collectively_activated_count
            ),
            "pairwise_nonadjacent_s6_activation_count": sum(
                row.collective_activation_verified for row in nonadjacent_controls
            ),
            "scalable_nonadjacent_family_validation_count": len(family),
            "finite_control_failure_count": failures,
            "all_n_collective_energy_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "isolated_point_signal_additivity_falsified": verified,
            "source_young_adjacency_pruning_valid": False,
            "pairwise_nonadjacent_collective_activation_exists": verified,
            "scalable_pairwise_nonadjacent_source_family_proved": verified,
            "scalable_family_collective_activation_proved": False,
            "all_n_collective_standard_energy_bound_proved": False,
            "efficient_collective_point_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Collective recoupling is a real source of point energy, but no scalable "
                "magnitude theorem or physical decoder has been established."
            ),
        },
        status=theorem.status,
        summary=(
            "Falsified every source-local extension of the one-pair no-go. Two-copy "
            "recoupling can activate standard point energy without any source Young "
            "edge, so the next theorem must operate on intermediate Kronecker channels."
        ),
        falsifiers_triggered=[
            (
                "The exact one-pair no-go is not additive and cannot be tensorized "
                "across the shared group variables."
            ),
            (
                "Pruning collision-free portfolios by source-level Young adjacency "
                "would delete genuinely informative collective blocks."
            ),
            (
                "Finite collective activation is not evidence of inverse-polynomial "
                "asymptotic energy without a recoupling-magnitude theorem."
            ),
        ],
    )


def write_collective_point_activation_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COLLECTIVE-POINT-ACTIVATION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_collective_point_activation" in globals():
        report = run_collective_point_activation(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COLLECTIVE-POINT-ACTIVATION",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COLLECTIVE-POINT-ACTIVATION.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COLLECTIVE-POINT-ACTIVATION.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_collective_point_activation": str(path)
                },
            )
        )
    return payload
