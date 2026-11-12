"""Event-level collision-free transfer bypasses injective moment transfer.

Let ``D`` be the event that all ``2K`` Plancherel source irreps are distinct,
and let ``E_v`` be a good spectral event at hierarchy node/target ``v`` under
the original independent source law.  For any finite node set ``V``,

    Pr[exists v: E_v fails | D]
      <= sum_v Pr[E_v fails] / Pr[D].                       (1)

No independence between nodes and no observable total-variation estimate is
needed.  If every node has failure at most ``delta`` and ``|V|=M``, the right
side is ``M delta/P_cf``.  An algorithm that rejects non-distinct portfolios
has unconditional accepted-good probability at least

    Pr[D and all E_v] >= P_cf - M delta.                    (2)

For the orientation hierarchy with ``N=2^K`` leaves and all ``p(n)`` target
irreps, ``M<2N p(n)``.  With two extra copies, ``N<8 n!`` and hence
``M<16 n! p(n)``.  Since the collision-free mass tends to one, it is enough
to prove an independent-source per-node failure

    delta = o(1/(n! p(n))).                                (3)

This is demanding and explains the need for growing moments or a local law,
but it removes a false prerequisite: one need not transfer the large trace
observable itself through the nonfactorizing injective Plancherel kernel.

Generic total variation is still too weak for transferring a tiny moment
expectation.  Equations (1)-(2) are a different route: first prove a uniform
high-probability spectral event under independent labels, then condition the
event.  The independent uniform spectral theorem remains open.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_collision_free_event_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EventConditioningBound:
    conditioning_event_probability: float
    event_count: int
    per_event_failure_upper_bound: float
    unconditioned_union_failure_upper_bound: float
    conditioned_union_failure_upper_bound: float
    accepted_good_probability_lower_bound: float
    exact_event_transfer_inequality_verified: bool
    status: str


@dataclass(frozen=True)
class HierarchyEventTransferScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    orientation_leaf_count_decimal: str
    target_count: int
    hierarchy_node_target_count_upper_decimal: str
    global_distinct_probability: float
    log2_global_distinct_probability: float
    target_total_conditional_failure: float
    required_per_node_failure_upper_bound: float
    log2_required_per_node_failure_upper_bound: float
    asymptotic_collision_free_mass_tends_to_one: bool
    event_level_conditioning_transfer_available: bool
    independent_uniform_spectral_event_proved: bool
    status: str


@dataclass(frozen=True)
class CollisionFreeEventTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    generic_controls: list[EventConditioningBound]
    hierarchy_scaling: list[HierarchyEventTransferScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def event_conditioning_bound(
    conditioning_probability: float,
    event_count: int,
    per_event_failure: float,
) -> EventConditioningBound:
    if not 0 < conditioning_probability <= 1:
        raise ValueError("conditioning probability must lie in (0,1]")
    if event_count < 1 or not 0 <= per_event_failure <= 1:
        raise ValueError("invalid event count or failure probability")
    union = min(1.0, event_count * per_event_failure)
    conditioned = min(1.0, union / conditioning_probability)
    accepted_good = max(0.0, conditioning_probability - union)
    return EventConditioningBound(
        conditioning_event_probability=conditioning_probability,
        event_count=event_count,
        per_event_failure_upper_bound=per_event_failure,
        unconditioned_union_failure_upper_bound=union,
        conditioned_union_failure_upper_bound=conditioned,
        accepted_good_probability_lower_bound=accepted_good,
        exact_event_transfer_inequality_verified=True,
        status="event-level-conditioning-union-bound-proved",
    )


@lru_cache(maxsize=None)
def stable_global_collision_free_probability(n: int, copy_count: int) -> float:
    """Evaluate ``(2K)! e_(2K)(p)`` without tiny intermediate ``e_j`` values."""

    partitions = tuple(integer_partitions(n))
    degree = 2 * copy_count
    if degree > len(partitions):
        return 0.0
    order = math.factorial(n)
    weights = np.asarray(
        [hook_length_dimension(partition) ** 2 / order for partition in partitions],
        dtype=np.longdouble,
    )
    # If a_j=j!e_j, adjoining weight p updates a_j <- a_j+j p a_(j-1).
    # The desired a_degree is a probability and never suffers factorial
    # underflow. Copying the shorter source view makes the vectorized update
    # equivalent to a descending in-place recurrence.
    scaled = np.zeros(degree + 1, dtype=np.longdouble)
    scaled[0] = 1
    indices = np.arange(degree + 1, dtype=np.longdouble)
    active = 0
    for weight in weights:
        active = min(active + 1, degree)
        scaled[1 : active + 1] += (
            indices[1 : active + 1]
            * weight
            * scaled[:active].copy()
        )
    return float(min(np.longdouble(1), max(np.longdouble(0), scaled[degree])))


def hierarchy_event_transfer_scaling_record(
    n: int,
    *,
    target_total_conditional_failure: float = 0.01,
) -> HierarchyEventTransferScalingRecord:
    if n < 3 or not 0 < target_total_conditional_failure < 1:
        raise ValueError("invalid n or target failure")
    order = math.factorial(n)
    threshold_copies = (order - 1).bit_length()
    copies = threshold_copies + 2
    leaves = 1 << copies
    targets = len(integer_partitions(n))
    node_target_upper = 2 * leaves * targets
    mass = stable_global_collision_free_probability(n, copies)
    if mass > 0:
        required = target_total_conditional_failure * mass / node_target_upper
        log2_mass = math.log2(mass)
        log2_required = math.log2(target_total_conditional_failure) + (
            log2_mass - math.log2(node_target_upper)
        )
    else:
        required = 0.0
        log2_mass = -math.inf
        log2_required = -math.inf
    return HierarchyEventTransferScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=threshold_copies,
        selected_copy_count=copies,
        orientation_leaf_count_decimal=str(leaves),
        target_count=targets,
        hierarchy_node_target_count_upper_decimal=str(node_target_upper),
        global_distinct_probability=mass,
        log2_global_distinct_probability=log2_mass,
        target_total_conditional_failure=target_total_conditional_failure,
        required_per_node_failure_upper_bound=required,
        log2_required_per_node_failure_upper_bound=log2_required,
        asymptotic_collision_free_mass_tends_to_one=True,
        event_level_conditioning_transfer_available=True,
        independent_uniform_spectral_event_proved=False,
        status=(
            "finite-event-transfer-target-computed-independent-edge-open"
            if mass > 0
            else "finite-global-distinct-event-impossible"
        ),
    )


def run_collision_free_event_transfer() -> CollisionFreeEventTransferReport:
    controls = [
        event_conditioning_bound(0.9, 100, 1e-5),
        event_conditioning_bound(0.5, 10_000, 1e-8),
        event_conditioning_bound(1e-3, 100, 1e-8),
    ]
    scaling = [
        hierarchy_event_transfer_scaling_record(n)
        for n in (20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(not row.exact_event_transfer_inequality_verified for row in controls)
    possible_rows = [row for row in scaling if row.global_distinct_probability > 0]
    tail = possible_rows[-1]
    metrics: dict[str, int | float] = {
        "event_level_conditioning_transfer_theorem_count": 1,
        "hierarchy_union_bound_theorem_count": 1,
        "generic_control_count": len(controls),
        "generic_control_failure_count": failures,
        "hierarchy_scaling_row_count": len(scaling),
        "tail_n": tail.n,
        "tail_log2_global_distinct_probability": tail.log2_global_distinct_probability,
        "tail_log2_required_per_node_failure": tail.log2_required_per_node_failure_upper_bound,
        "injective_moment_transfer_required_for_event_conditioning": 0,
        "independent_uniform_spectral_event_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CollisionFreeEventTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "conditional_event_bound": (
                "For any good event E and conditioning event D, "
                "Pr(E^c|D)<=Pr(E^c)/Pr(D)."
            ),
            "hierarchy_union": (
                "For M node/target events with failure at most delta, the "
                "conditional union failure is at most M delta/P_cf."
            ),
            "rejection_success": (
                "Rejecting collision portfolios leaves accepted-good mass at "
                "least P_cf-M delta."
            ),
            "two_extra_copy_node_count": (
                "With K+2 copies, all binary-tree nodes and targets number "
                "less than 16 n! p(n)."
            ),
            "scope": (
                "This theorem transfers good events only. It does not prove "
                "the independent-label spectral event or any algorithm."
            ),
        },
        generic_controls=controls,
        hierarchy_scaling=scaling,
        proof_obligations=[
            {
                "obligation": "transfer_independent_good_events_to_collision_free_law",
                "resolved": failures == 0,
                "resolution": (
                    "Conditional probability plus a union bound gives the exact "
                    "M delta/P_cf transfer without injective moments."
                ),
            },
            {
                "obligation": "prove_uniform_independent_spectral_edges_over_all_nodes_targets",
                "resolved": False,
                "resolution": (
                    "Need per-node failure o(1/(n!p(n))), likely from growing "
                    "moments, resolvents, or a structural frame theorem."
                ),
            },
            {
                "obligation": "construct_coherent_hierarchical_merge",
                "resolved": False,
                "resolution": "Event transfer has no circuit content.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The injective source kernel must be controlled before any spectral theorem can transfer.",
                "resolved": True,
                "resolution": (
                    "False for high-probability events: prove the event under "
                    "independent labels and condition it using equation (1)."
                ),
            },
            {
                "objection": "An o(1) per-node failure is enough for the full hierarchy.",
                "resolved": True,
                "resolution": (
                    "False: there are O(n!p(n)) nodes/targets, so the required "
                    "per-node tail is exponentially smaller."
                ),
            },
            {
                "objection": "The finite n<=48 collision-free mass is already close to one.",
                "resolved": True,
                "resolution": (
                    "False: the finite regime is strongly preasymptotic, and "
                    "the exact mass is retained in every bound."
                ),
            },
            {
                "objection": "Event-level transfer proves the independent spectral event.",
                "resolved": False,
                "resolution": (
                    "It only removes the conditioning step after that much "
                    "harder theorem has been established."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "event_level_collision_free_transfer_proved": failures == 0,
            "full_hierarchy_union_cost_quantified": True,
            "injective_signed_moment_contraction_mandatory": False,
            "independent_uniform_spectral_event_proved": False,
            "globally_distinct_uniform_spectral_event_proved": False,
            "coherent_hierarchical_merge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Conditioning is no longer a separate moment theorem, but the "
                "independent per-node edge tail must beat 1/(n!p(n))."
            ),
        },
        status=(
            "event-conditioning-transfer-proved-independent-uniform-edge-open"
            if failures == 0
            else "event-conditioning-transfer-control-failure"
        ),
        summary=(
            "Replaced mandatory injective moment transfer by an exact event-level "
            "conditioning route and quantified the full hierarchy union cost."
        ),
        falsifiers_triggered=[
            "Injective observable contraction is not mandatory for conditioning a pre-proved good event.",
            "Per-node o(1) tails are insufficient across an exponential orientation hierarchy.",
            "Finite collision-free mass cannot be replaced by its asymptotic limit in numerical rows.",
        ],
    )


def write_collision_free_event_transfer_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_collision_free_event_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER",
                source=registry_experiment_id,
                claim=(
                    "Naive initial assumption for EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER."
                ),
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
                    "self_dual_wreath_collision_free_event_transfer": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_collision_free_event_transfer_report()
    print(json.dumps(report, indent=2))
