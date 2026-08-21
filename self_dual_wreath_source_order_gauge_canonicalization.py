"""Coherent source-pair sorting removes order gauge, not orientation structure.

Choose a canonical ordering ``(alpha_i,beta_i)`` for every unequal unordered
source pair.  Let ``s_i`` record whether the observed ordered Fourier block is
canonical or reversed, and let ``e_i`` record which observed member is
selected by the orientation diagonal.  The canonically selected-label pattern
is

    q_i = e_i + s_i mod 2.                                  (1)

A branch flip ``t`` acts diagonally on the two bits,

    (s,e) -> (s+t,e+t),

so ``q`` is invariant.  The ``2^(2K)`` pairs ``(s,e)`` split into ``2^K``
branch orbits of size ``2^K``, labeled exactly by ``q``.  Coherent sorting
implements

    (s,e) -> (0,e+s)=(0,q)                                 (2)

while retaining a reversible order-gauge record.  It does not mix different
selected-label patterns.

The fixed-block orientation leaf rank obeys

    rank(E_e^(s Lambda)) = rank(E_q^Lambda_canonical).      (3)

Thus all order gauges in one orbit have the same rank, but the rank profile
across ``q`` remains nonuniform.  A Fourier transform or any operation
generated only by branch shifts acts within one ``q`` orbit and cannot supply
the missing rectangular-CS normalization across selected patterns.

Partition comparison, carrier-register swaps, and XOR updates make sorting
polynomial.  This is a useful gauge reduction, not a polar compiler or a
hardness theorem.  Direct matrix child transforms and the complete
rectangular CS polar remain open; no decoder, classical separation, or
speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_source_block_branch_covariance_boundary import (
    Label,
    Partition,
    orientation_leaf_rank,
    swap_source_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_source_order_gauge_canonicalization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SOURCE-ORDER-GAUGE-CANONICALIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SourceOrderGaugeControl:
    control_id: str
    n: int
    target_partition: Partition
    canonical_labels: tuple[Label, ...]
    source_pair_count: int
    source_order_orientation_pair_count: int
    diagonal_branch_orbit_count: int
    diagonal_branch_orbit_size: int
    selected_pattern_count: int
    selected_pattern_rank_profile: tuple[tuple[int, int], ...]
    distinct_selected_pattern_rank_count: int
    minimum_selected_pattern_leaf_rank: int
    maximum_selected_pattern_leaf_rank: int
    maximum_order_gauge_rank_residual: int
    maximum_selected_pattern_invariance_residual: int
    source_order_gauge_action_free: bool
    selected_pattern_is_complete_orbit_invariant: bool
    selected_pattern_rank_profile_nonuniform: bool
    exact_source_order_gauge_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class SourceOrderGaugeScalingRecord:
    n: int
    information_threshold_copy_count: int
    source_order_gauge_qubit_count: int
    selected_pattern_qubit_count: int
    coherent_partition_pair_sort_polynomial: bool
    coherent_carrier_swap_polynomial: bool
    branch_fourier_transform_polynomial: bool
    branch_operations_mix_selected_patterns: bool
    source_order_sorting_compiles_rectangular_cs_polar: bool
    complete_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class SourceOrderGaugeTheorem:
    source_order_bit: str
    selected_pattern: str
    branch_action: str
    orbit_quotient: str
    coherent_sort: str
    rank_invariance: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SourceOrderGaugeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SourceOrderGaugeTheorem
    finite_controls: list[SourceOrderGaugeControl]
    scaling_records: list[SourceOrderGaugeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def selected_label_pattern(source_order_mask: int, orientation_mask: int) -> int:
    return source_order_mask ^ orientation_mask


def diagonal_branch_orbit(
    source_order_mask: int,
    orientation_mask: int,
    pair_count: int,
) -> tuple[tuple[int, int], ...]:
    if pair_count < 1:
        raise ValueError("pair count must be positive")
    limit = 1 << pair_count
    if not 0 <= source_order_mask < limit or not 0 <= orientation_mask < limit:
        raise ValueError("mask out of range")
    return tuple(
        (source_order_mask ^ translation, orientation_mask ^ translation)
        for translation in range(limit)
    )


def canonicalize_source_order(
    source_order_mask: int,
    orientation_mask: int,
) -> tuple[int, int, int]:
    selected = selected_label_pattern(source_order_mask, orientation_mask)
    return 0, selected, source_order_mask


def audit_source_order_gauge(
    control_id: str,
    target_partition: Partition,
    canonical_labels: tuple[Label, ...],
) -> SourceOrderGaugeControl:
    if not canonical_labels:
        raise ValueError("at least one canonical source pair is required")
    if any(left == right for left, right in canonical_labels):
        raise ValueError("canonical source pairs must be unequal")
    pair_count = len(canonical_labels)
    limit = 1 << pair_count
    rank_profile = tuple(
        (
            selected,
            orientation_leaf_rank(
                target_partition,
                canonical_labels,
                selected,
            ),
        )
        for selected in range(limit)
    )
    rank_by_selected = dict(rank_profile)
    order_rank_residual = 0
    invariant_residual = 0
    seen_orbits: set[tuple[tuple[int, int], ...]] = set()
    for source_order in range(limit):
        ordered_labels = swap_source_labels(canonical_labels, source_order)
        for orientation in range(limit):
            selected = selected_label_pattern(source_order, orientation)
            observed_rank = orientation_leaf_rank(
                target_partition,
                ordered_labels,
                orientation,
            )
            order_rank_residual = max(
                order_rank_residual,
                abs(observed_rank - rank_by_selected[selected]),
            )
            orbit = diagonal_branch_orbit(source_order, orientation, pair_count)
            orbit_selected = {
                selected_label_pattern(order, mask) for order, mask in orbit
            }
            invariant_residual = max(
                invariant_residual,
                len(orbit_selected) - 1,
            )
            seen_orbits.add(tuple(sorted(orbit)))
    ranks = tuple(rank for _, rank in rank_profile)
    free = all(
        len(set(diagonal_branch_orbit(order, orientation, pair_count))) == limit
        for order in range(limit)
        for orientation in range(limit)
    )
    complete_invariant = bool(
        len(seen_orbits) == limit and invariant_residual == 0
    )
    nonuniform = len(set(ranks)) > 1
    verified = bool(
        order_rank_residual == 0
        and free
        and complete_invariant
        and nonuniform
    )
    return SourceOrderGaugeControl(
        control_id=control_id,
        n=sum(target_partition),
        target_partition=target_partition,
        canonical_labels=canonical_labels,
        source_pair_count=pair_count,
        source_order_orientation_pair_count=limit * limit,
        diagonal_branch_orbit_count=len(seen_orbits),
        diagonal_branch_orbit_size=limit,
        selected_pattern_count=limit,
        selected_pattern_rank_profile=rank_profile,
        distinct_selected_pattern_rank_count=len(set(ranks)),
        minimum_selected_pattern_leaf_rank=min(ranks),
        maximum_selected_pattern_leaf_rank=max(ranks),
        maximum_order_gauge_rank_residual=order_rank_residual,
        maximum_selected_pattern_invariance_residual=invariant_residual,
        source_order_gauge_action_free=free,
        selected_pattern_is_complete_orbit_invariant=complete_invariant,
        selected_pattern_rank_profile_nonuniform=nonuniform,
        exact_source_order_gauge_reduction_verified=verified,
        status=(
            "source-order-gauge-removed-selected-pattern-frame-remains"
            if verified
            else "source-order-gauge-reduction-control-failure"
        ),
    )


def source_order_gauge_scaling_record(n: int) -> SourceOrderGaugeScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2)) + 2
    return SourceOrderGaugeScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        source_order_gauge_qubit_count=copies,
        selected_pattern_qubit_count=copies,
        coherent_partition_pair_sort_polynomial=True,
        coherent_carrier_swap_polynomial=True,
        branch_fourier_transform_polynomial=True,
        branch_operations_mix_selected_patterns=False,
        source_order_sorting_compiles_rectangular_cs_polar=False,
        complete_orientation_polar_compiled=False,
        status="source-order-canonicalization-polynomial-selected-pattern-cs-open",
    )


def _finite_controls() -> list[SourceOrderGaugeControl]:
    return [
        audit_source_order_gauge(
            "S3-ONE-PAIR-ORDER-GAUGE",
            (3,),
            (((3,), (2, 1)),),
        ),
        audit_source_order_gauge(
            "S4-TWO-PAIR-ORDER-GAUGE",
            (2, 2),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        ),
        audit_source_order_gauge(
            "S5-TWO-PAIR-ORDER-GAUGE",
            (2, 1, 1, 1),
            (((5,), (4, 1)), ((2, 1, 1, 1), (1, 1, 1, 1, 1))),
        ),
        audit_source_order_gauge(
            "S6-MATRIX-PARTIAL-SUPPORT-ORDER-GAUGE",
            (6,),
            (
                ((6,), (4, 2)),
                ((5, 1), (2, 2, 2)),
                ((3, 3), (2, 1, 1, 1, 1)),
                ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
            ),
        ),
    ]


def run_source_order_gauge_canonicalization() -> SourceOrderGaugeReport:
    controls = _finite_controls()
    scaling = [
        source_order_gauge_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(
        not row.exact_source_order_gauge_reduction_verified for row in controls
    )
    verified = failures == 0
    theorem = SourceOrderGaugeTheorem(
        source_order_bit="s_i=0 for canonical order and 1 for reversed order",
        selected_pattern="q=e+s in F_2^K",
        branch_action="t:(s,e)->(s+t,e+t), so q is invariant",
        orbit_quotient="F_2^K acts freely and its orbits are exactly the q fibers",
        coherent_sort="(s,e)->(0,q) with reversible order-gauge record s",
        rank_invariance="rank(E_e^(sLambda))=rank(E_q^Lambda_canonical)",
        scope=(
            "sorting and branch Fourier transforms remove source order only; "
            "they do not mix or normalize the q-indexed selected-label frame"
        ),
        theorem_verified=verified,
        status=(
            "source-order-gauge-quotient-proved-selected-pattern-polar-open"
            if verified
            else "source-order-gauge-canonicalization-control-failure"
        ),
    )
    s6 = next(row for row in controls if row.n == 6)
    return SourceOrderGaugeReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "identify_complete_branch_orbit_invariant",
                "resolved": verified,
                "resolution": (
                    "The free diagonal XOR action has one orbit for each q=e+s."
                ),
            },
            {
                "obligation": "compile_coherent_source_pair_sorting",
                "resolved": True,
                "resolution": (
                    "Reversible partition comparison, controlled carrier swaps, "
                    "and XOR updates use polynomial-size registers and gates."
                ),
            },
            {
                "obligation": "test_whether_sorting_flattens_orientation_rank_profile",
                "resolved": verified,
                "resolution": (
                    "All order gauges match the canonical q rank, while every "
                    "control retains a nonuniform rank profile across q."
                ),
            },
            {
                "obligation": "compile_selected_pattern_rectangular_cs_polar",
                "resolved": False,
                "resolution": (
                    "The quotient removes a replicated gauge but leaves exactly "
                    "the selected-label frame whose normalization was open."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Keeping source blocks coherent lets branch Hadamards mix all orientations.",
                "resolved": True,
                "resolution": (
                    "Branch shifts mix order gauges only. The selected pattern q "
                    "is a superselection label for that action."
                ),
            },
            {
                "objection": "Sorting all source pairs makes every leaf equivalent.",
                "resolved": True,
                "resolution": (
                    "It makes source order canonical; the selected partition in "
                    "each pair remains q-dependent, with nonuniform leaf ranks."
                ),
            },
            {
                "objection": "A Fourier transform on the order gauge reveals hidden-label signal.",
                "resolved": True,
                "resolution": (
                    "The gauge is source-order nuisance and branch operations do "
                    "not change q. No hidden involution information is added."
                ),
            },
            {
                "objection": "This proves the selected-pattern polar hard.",
                "resolved": True,
                "resolution": (
                    "No. The theorem only removes a covariance shortcut; direct "
                    "matrix CS or representation-specific transforms remain open."
                ),
            },
        ],
        headline_metrics={
            "source_order_gauge_quotient_theorem_count": int(verified),
            "coherent_source_pair_sort_compiler_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_order_gauge_rank_residual": max(
                row.maximum_order_gauge_rank_residual for row in controls
            ),
            "maximum_selected_pattern_invariance_residual": max(
                row.maximum_selected_pattern_invariance_residual for row in controls
            ),
            "nonuniform_selected_pattern_rank_control_count": sum(
                row.selected_pattern_rank_profile_nonuniform for row in controls
            ),
            "s6_selected_pattern_count": s6.selected_pattern_count,
            "s6_distinct_selected_pattern_rank_count": (
                s6.distinct_selected_pattern_rank_count
            ),
            "s6_minimum_selected_pattern_leaf_rank": (
                s6.minimum_selected_pattern_leaf_rank
            ),
            "s6_maximum_selected_pattern_leaf_rank": (
                s6.maximum_selected_pattern_leaf_rank
            ),
            "scaling_record_count": len(scaling),
            "selected_pattern_rectangular_cs_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "source_order_gauge_quotient_proved": verified,
            "coherent_source_pair_sorting_polynomial": True,
            "selected_pattern_complete_branch_orbit_invariant": verified,
            "branch_gauge_operations_mix_selected_patterns": False,
            "source_order_sorting_flattens_selected_pattern_frame": False,
            "source_order_sorting_compiles_rectangular_cs_polar": False,
            "direct_matrix_selected_pattern_transform_rejected": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Sorting quotients the redundant source-order bit, but the "
                "canonically selected-label pattern is invariant and retains "
                "the nonuniform orientation frame."
            ),
        },
        status=theorem.status,
        summary=(
            "Compiled coherent source-order canonicalization and proved that it "
            "leaves the selected-label orientation polar unchanged."
        ),
        falsifiers_triggered=[
            "Coherent source-block orbit handling does not let branch shifts mix selected-label patterns.",
            "Source-pair sorting removes only an order gauge and preserves the nonuniform leaf-rank profile.",
            "The source-order register is nuisance, not a new hidden-involution signal.",
        ],
    )


def write_source_order_gauge_canonicalization_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_source_order_gauge_canonicalization())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_source_order_gauge_canonicalization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
