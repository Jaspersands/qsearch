"""Linear-depth no-go for the implemented local DCP fiber walk.

The current fiber-transport graph uses three target-independent move classes
inside a low-bit fiber modulo ``Q=2^k``:

* flip coordinate ``i`` when ``a_i=0 mod Q``;
* swap coordinates ``i,j`` when ``a_i=a_j mod Q``;
* replace one Boolean pattern by another inside an explicit small block when
  the two block subset sums agree modulo ``Q``.

For independent uniform labels, each flip trigger has probability ``Q^-1``
and each swap trigger has probability ``Q^-1``.  For two distinct patterns in
a fixed block, their signed difference has a coefficient ``+/-1``; its label
sum is therefore uniform modulo ``Q``, so the block-collision probability is
also ``Q^-1``.  A union bound gives

    Pr[any local move exists]
      <= [m + C(m,2) + F C(2^b,2)] / 2^k,               (1)

for ``F`` explicit blocks of width at most ``b``.

Independently, for uniform target ``t`` the low-fiber size ``X_t`` has mean
``lambda=2^(m-k)`` and variance ``lambda(1-2^-k)`` because distinct Boolean
assignment indicators have a unit minor and are pairwise independent.  Hence

    Pr[X_t < lambda/2] <= 4/lambda.                     (2)

The exact second moment also gives

    Pr[X_t>0] >= lambda/[1+lambda(1-2^-m)].              (3)

After conditioning on a legal target, (1)--(3) show that at linear depth
``k=alpha n``, with ``m=n+O(1)``, polynomial ``F``, and ``b=O(log n)``, the
implemented graph is edgeless while its fiber has exponentially many vertices
with probability ``1-2^-Omega(n)``.  Its largest component fraction is then at
most ``2/lambda``.

This eliminates the current local graph and any target-independent explicit
polynomial dictionary of logarithmic blocks as a linear-depth walk.  It does
not eliminate target-dependent global moves, implicit collision generation,
or a walk whose edges are found by a separate nonlocal quantum primitive.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from dcp_fiber_transport_graph import (
    build_fiber_transport_graph,
    enumerate_low_fibers,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/phase_workbench/dcp_linear_depth_fiber_walk_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-LINEAR-DEPTH-FIBER-WALK-NO-GO"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ExactFiberGraphTriggerControl:
    control_id: str
    modulus_bits: int
    depth: int
    register_count: int
    block_size: int
    supported_fiber_count: int
    divisible_coordinate_trigger_count: int
    equal_residue_pair_trigger_count: int
    block_pattern_collision_trigger_count: int
    total_trigger_count: int
    total_graph_edge_count: int
    maximum_fiber_vertex_count: int
    no_trigger_implies_every_fiber_edgeless: bool
    status: str


@dataclass(frozen=True)
class LinearDepthFiberWalkScalingRecord:
    n_bits: int
    register_offset: int
    register_count: int
    depth_fraction: float
    depth: int
    block_log_multiplier: int
    block_size: int
    block_family_power: int
    block_family_size: int
    mean_fiber_log2_size: int
    legal_probability_lower_bound: float
    log2_flip_union_bound: float
    log2_swap_union_bound: float
    log2_block_union_bound: float
    log2_any_move_union_bound: float
    log2_small_fiber_probability_bound: float
    conditioned_legal_failure_probability_upper_bound: float
    edgeless_large_fiber_probability_lower_bound: float
    largest_component_fraction_upper_bound_on_good_event: float
    exponentially_fragmented: bool
    status: str


@dataclass(frozen=True)
class LinearDepthFiberWalkNoGoTheorem:
    move_trigger_bound: str
    fiber_first_moment: str
    fiber_variance: str
    legal_probability_bound: str
    conditioned_good_event: str
    asymptotic_regime: str
    asymptotic_conclusion: str
    current_local_fiber_walk_eliminated: bool
    polynomial_log_block_dictionary_eliminated: bool
    target_dependent_global_moves_eliminated: bool
    implicit_collision_oracle_eliminated: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPLinearDepthFiberWalkNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[ExactFiberGraphTriggerControl]
    scaling_records: list[LinearDepthFiberWalkScalingRecord]
    theorem: LinearDepthFiberWalkNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _log2_add(*values: float) -> float:
    finite = [value for value in values if value != -math.inf]
    if not finite:
        return -math.inf
    maximum = max(finite)
    return maximum + math.log2(sum(2.0 ** (value - maximum) for value in finite))


def legal_probability_lower_bound(register_count: int, depth: int) -> float:
    if register_count < 1 or not 1 <= depth <= register_count:
        raise ValueError("require 1 <= depth <= register count")
    inverse_load = 2.0 ** (-(register_count - depth))
    return 1.0 / (
        inverse_load + 1.0 - 2.0 ** (-register_count)
    )


def move_union_bound_logs(
    register_count: int,
    depth: int,
    block_size: int,
    block_family_size: int,
) -> tuple[float, float, float, float]:
    if register_count < 1 or depth < 1 or block_size < 1 or block_family_size < 0:
        raise ValueError("invalid move dictionary dimensions")
    flip = math.log2(register_count) - depth
    swap_pairs = math.comb(register_count, 2)
    swap = math.log2(swap_pairs) - depth if swap_pairs else -math.inf
    pattern_pairs = math.comb(1 << block_size, 2)
    block = (
        math.log2(block_family_size)
        + math.log2(pattern_pairs)
        - depth
        if block_family_size and pattern_pairs
        else -math.inf
    )
    return flip, swap, block, _log2_add(flip, swap, block)


def _trigger_counts(
    labels: Sequence[int],
    depth: int,
    block_size: int,
) -> tuple[int, int, int]:
    modulus = 1 << depth
    low = [int(label) % modulus for label in labels]
    flips = sum(value == 0 for value in low)
    swaps = sum(
        low[left] == low[right]
        for left in range(len(low))
        for right in range(left)
    )
    block_collisions = 0
    for start in range(0, len(low), block_size):
        block = low[start : start + block_size]
        counts: dict[int, int] = {}
        for pattern in range(1 << len(block)):
            value = sum(
                label
                for index, label in enumerate(block)
                if (pattern >> index) & 1
            ) % modulus
            counts[value] = counts.get(value, 0) + 1
        block_collisions += sum(math.comb(count, 2) for count in counts.values())
    return flips, swaps, block_collisions


def audit_exact_trigger_control(
    control_id: str,
    labels: Sequence[int],
    modulus_bits: int,
    depth: int,
    block_size: int,
) -> ExactFiberGraphTriggerControl:
    if not labels or not 1 <= depth < modulus_bits:
        raise ValueError("invalid exact control dimensions")
    if any(not 0 <= int(label) < (1 << modulus_bits) for label in labels):
        raise ValueError("label outside ambient modulus")
    flips, swaps, blocks = _trigger_counts(labels, depth, block_size)
    fibers = enumerate_low_fibers(labels, depth)
    edge_count = 0
    maximum_fiber = 0
    for target, vertices in fibers.items():
        graph = build_fiber_transport_graph(
            labels, depth, target, block_size=block_size
        )
        edge_count += graph.number_of_edges()
        maximum_fiber = max(maximum_fiber, len(vertices))
    triggers = flips + swaps + blocks
    implication = triggers != 0 or edge_count == 0
    return ExactFiberGraphTriggerControl(
        control_id=control_id,
        modulus_bits=modulus_bits,
        depth=depth,
        register_count=len(labels),
        block_size=block_size,
        supported_fiber_count=len(fibers),
        divisible_coordinate_trigger_count=flips,
        equal_residue_pair_trigger_count=swaps,
        block_pattern_collision_trigger_count=blocks,
        total_trigger_count=triggers,
        total_graph_edge_count=edge_count,
        maximum_fiber_vertex_count=maximum_fiber,
        no_trigger_implies_every_fiber_edgeless=implication,
        status=(
            "move-trigger-necessity-verified"
            if implication
            else "unexpected-edge-without-trigger"
        ),
    )


def scaling_record(
    n_bits: int,
    register_offset: int,
    depth_fraction: float,
    block_log_multiplier: int,
    block_family_power: int,
) -> LinearDepthFiberWalkScalingRecord:
    if n_bits < 8 or register_offset < 0 or not 0 < depth_fraction < 1:
        raise ValueError("invalid linear-depth schedule")
    if block_log_multiplier < 1 or block_family_power < 0:
        raise ValueError("invalid block dictionary schedule")
    register_count = n_bits + register_offset
    depth = max(1, min(n_bits - 1, math.floor(depth_fraction * n_bits)))
    block_size = max(1, math.ceil(block_log_multiplier * math.log2(n_bits)))
    family_size = n_bits**block_family_power
    flip, swap, block, move = move_union_bound_logs(
        register_count, depth, block_size, family_size
    )
    mean_log2 = register_count - depth
    small_fiber_log2 = min(0.0, 2.0 - mean_log2)
    legal_lower = legal_probability_lower_bound(register_count, depth)
    unconditional_failure_log2 = _log2_add(move, small_fiber_log2)
    conditioned = min(
        1.0,
        2.0**unconditional_failure_log2 / legal_lower,
    )
    component_fraction = min(1.0, 2.0 ** (1 - mean_log2))
    exponential = (
        move <= -0.25 * n_bits
        and small_fiber_log2 <= -0.25 * n_bits
        and component_fraction <= 2.0 ** (-0.25 * n_bits)
    )
    return LinearDepthFiberWalkScalingRecord(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        depth_fraction=depth_fraction,
        depth=depth,
        block_log_multiplier=block_log_multiplier,
        block_size=block_size,
        block_family_power=block_family_power,
        block_family_size=family_size,
        mean_fiber_log2_size=mean_log2,
        legal_probability_lower_bound=legal_lower,
        log2_flip_union_bound=flip,
        log2_swap_union_bound=swap,
        log2_block_union_bound=block,
        log2_any_move_union_bound=move,
        log2_small_fiber_probability_bound=small_fiber_log2,
        conditioned_legal_failure_probability_upper_bound=conditioned,
        edgeless_large_fiber_probability_lower_bound=max(0.0, 1.0 - conditioned),
        largest_component_fraction_upper_bound_on_good_event=component_fraction,
        exponentially_fragmented=exponential,
        status=(
            "linear-depth-local-walk-exponentially-edgeless"
            if exponential
            else "finite-schedule-not-yet-in-exponential-regime"
        ),
    )


def linear_depth_fiber_walk_no_go_theorem() -> LinearDepthFiberWalkNoGoTheorem:
    return LinearDepthFiberWalkNoGoTheorem(
        move_trigger_bound=(
            "Pr[any edge trigger] <= [m+C(m,2)+F*C(2^b,2)]/2^k"
        ),
        fiber_first_moment="E[X_t]=lambda=2^(m-k)",
        fiber_variance="Var(X_t)=lambda(1-2^-k) by pairwise independence",
        legal_probability_bound=(
            "Pr[X_t>0]>=lambda/[1+lambda(1-2^-m)]"
        ),
        conditioned_good_event=(
            "conditioned legal, graph edgeless and X_t>=lambda/2 except with "
            "probability at most (move_bound+4/lambda)/Pr[legal]"
        ),
        asymptotic_regime=(
            "m=n+O(1), k=alpha n for fixed alpha in (0,1), "
            "F=poly(n), b=O(log n)"
        ),
        asymptotic_conclusion=(
            "with probability 1-2^-Omega(n), every local-move component is a "
            "singleton inside a fiber of size 2^((1-alpha)n+O(1))"
        ),
        current_local_fiber_walk_eliminated=True,
        polynomial_log_block_dictionary_eliminated=True,
        target_dependent_global_moves_eliminated=False,
        implicit_collision_oracle_eliminated=False,
        theorem_verified=True,
        status="linear-depth-local-fiber-walk-edgeless-with-high-probability",
    )


def run_linear_depth_fiber_walk_no_go(
    n_values: Sequence[int] = (128, 256, 512, 1024, 2048),
) -> DCPLinearDepthFiberWalkNoGoReport:
    controls = [
        audit_exact_trigger_control(
            "explicit-no-trigger-family",
            (1, 2, 4, 8, 3, 5),
            modulus_bits=8,
            depth=4,
            block_size=2,
        ),
        audit_exact_trigger_control(
            "flip-trigger-family",
            (0, 1, 2, 4, 7, 9),
            modulus_bits=8,
            depth=4,
            block_size=2,
        ),
        audit_exact_trigger_control(
            "swap-trigger-family",
            (1, 17, 2, 4, 7, 9),
            modulus_bits=8,
            depth=4,
            block_size=2,
        ),
    ]
    rows = [
        scaling_record(
            n_bits,
            register_offset=offset,
            depth_fraction=depth_fraction,
            block_log_multiplier=block_multiplier,
            block_family_power=family_power,
        )
        for n_bits in n_values
        for offset in (0, 2)
        for depth_fraction in (0.4, 0.5, 0.6)
        for block_multiplier in (1, 2)
        for family_power in (1, 3)
    ]
    theorem = linear_depth_fiber_walk_no_go_theorem()
    failures = sum(
        not row.no_trigger_implies_every_fiber_edgeless for row in controls
    )
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "linear_depth_local_walk_no_go_theorem_count": 1,
        "exact_control_count": len(controls),
        "exact_control_failure_count": failures,
        "scaling_row_count": len(rows),
        "exponentially_fragmented_row_count": sum(
            row.exponentially_fragmented for row in rows
        ),
        "tail_exponentially_fragmented_row_count": sum(
            row.exponentially_fragmented for row in tail
        ),
        "tail_row_count": len(tail),
        "minimum_tail_edgeless_large_fiber_probability_lower_bound": min(
            row.edgeless_large_fiber_probability_lower_bound for row in tail
        ),
        "maximum_tail_largest_component_fraction_upper_bound": max(
            row.largest_component_fraction_upper_bound_on_good_event for row in tail
        ),
        "proved_current_fiber_graph_linear_depth_failure_count": 1,
        "proved_polynomial_log_block_dictionary_failure_count": 1,
        "proved_target_dependent_global_move_failure_count": 0,
        "polynomial_fiber_walk_count": 0,
        "polynomial_dcp_decoder_count": 0,
    }
    return DCPLinearDepthFiberWalkNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "source": (
                "independent uniform labels modulo 2^n and independent uniform "
                "target conditioned on a nonempty low fiber"
            ),
            "move_set": (
                "divisible-coordinate flips, equal-low-residue swaps, and an "
                "explicit target-independent family of blocks of width b"
            ),
            "proved": (
                "at linear depth and logarithmic block width, the graph is "
                "edgeless on exponentially large legal fibers with overwhelming probability"
            ),
            "excluded": (
                "target-dependent global relations, adaptive block discovery, "
                "and implicit nonlocal quantum move oracles"
            ),
        },
        exact_controls=controls,
        scaling_records=rows,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-DCP-FIBER-WALK-EDGE-UNION",
                "description": "Bound every implemented edge trigger at linear depth.",
                "satisfied": True,
                "evidence": (
                    "each nonzero move relation contains a unit coefficient and "
                    "is uniform modulo 2^k"
                ),
            },
            {
                "id": "PO-DCP-FIBER-WALK-LARGE-FIBER",
                "description": (
                    "Prove the graph is edgeless inside a genuinely large legal fiber."
                ),
                "satisfied": True,
                "evidence": (
                    "pairwise-independent assignment indicators give exact mean, "
                    "variance, and the conditioned Chebyshev bound"
                ),
            },
            {
                "id": "PO-DCP-TARGET-DEPENDENT-GLOBAL-MOVE",
                "description": (
                    "Construct a polynomial reversible global move using target "
                    "and high labels with inverse-polynomial source coverage."
                ),
                "satisfied": False,
                "evidence": "outside the explicit local dictionary",
            },
            {
                "id": "PO-DCP-IMPLICIT-COLLISION-WALK",
                "description": (
                    "Construct an implicit edge oracle without first solving the "
                    "same modular relation problem."
                ),
                "satisfied": False,
                "evidence": "no nonlocal edge-generation primitive exists",
            },
        ],
        adversarial_audit=[
            {
                "attack": "Use polynomially many overlapping logarithmic blocks.",
                "survives": False,
                "reason": (
                    "the union bound charges every block-pattern pair and remains "
                    "exponentially small for any polynomial block family"
                ),
            },
            {
                "attack": "Argue that an edgeless graph is harmless because the fiber is tiny.",
                "survives": False,
                "reason": (
                    "the low fiber has mean 2^(m-k) and pairwise-independent "
                    "concentration makes it exponentially large on legal source mass"
                ),
            },
            {
                "attack": "Choose blocks adaptively after finding label relations.",
                "survives": True,
                "reason": (
                    "the theorem charges only an explicit target-independent family; "
                    "relation-finding cost must be analyzed separately"
                ),
            },
            {
                "attack": "Use a target-dependent global coherent transport.",
                "survives": True,
                "reason": "its move relation is not in the implemented local graph",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "implemented_local_fiber_walk_linear_depth_route_alive": False,
            "polynomial_log_block_dictionary_route_alive": False,
            "target_dependent_global_transport_route_alive": True,
            "implicit_nonlocal_collision_walk_route_alive": True,
            "polynomial_fiber_walk_constructed": False,
            "polynomial_dcp_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The implemented local graph is overwhelmingly edgeless at the "
                "linear depths needed for inversion, despite exponentially large "
                "fibers. Only a target-dependent or implicit nonlocal edge "
                "primitive can keep the walk route alive."
            ),
        },
        status="implemented-linear-depth-fiber-walk-asymptotically-edgeless",
        summary=(
            "Proved that divisible flips, equal-residue swaps, and any explicit "
            "polynomial family of logarithmic block substitutions produce an "
            "edgeless graph on exponentially large linear-depth fibers with "
            "probability 1-2^-Omega(n). Target-dependent global and implicit "
            "nonlocal moves remain open."
        ),
        falsifiers_triggered=[
            "Positive spectral gaps on shallow finite fibers do not extrapolate to linear depth.",
            "The implemented graph loses all edges before state-preparation cost becomes the only issue.",
            "Adding polynomially many fixed logarithmic blocks does not restore linear-depth transport.",
            "The theorem does not reject a separately constructed target-dependent global edge oracle.",
        ],
    )


def write_linear_depth_fiber_walk_no_go(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-LINEAR-DEPTH-FIBER-WALK-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_linear_depth_fiber_walk_no_go(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_linear_depth_fiber_walk_no_go()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
