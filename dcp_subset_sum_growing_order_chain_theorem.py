"""Near-logarithmic growing-order subset-sum moment obstruction.

The earlier growing-order theorem bounded the number of proper lattice
transitions by the number ``2^k`` of Boolean column patterns.  Integer-lattice
index gives a much smaller uniform bound.

At rank ``r``, every transfer lattice contains ``r`` independent Boolean
generators.  Its index in the saturated lattice of its rational span divides a
nonzero ``r x r`` Boolean minor and is therefore at most ``r^(r/2)`` by
Hadamard.  Every proper same-rank enlargement reduces this integer index by a
factor of at least two.  Rank can increase at most ``k-1`` times.  Consequently
every non-self transfer path has length at most

    (k-1) + sum_{r=1}^k ceil((r/2) log_2 r) = O(k^2 log k).

Substituting this bound into the monotone Smith-transfer path count proves
source bad-tuple decay whenever

    2^k k^2 log k (log n + k) = o(n).

This includes every ``k(n) <= (1-epsilon) log_2 n`` schedule and, more
conservatively, ``k <= log_2 n-(4+epsilon)log_2 log_2 n``.  The theorem is for
the nonnegative source bad-tuple contribution.  It does not cover signed
observables, the final near-logarithmic window, reduced-basis geometry, or
decoder complexity.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

from dcp_subset_sum_smith_transfer import build_smith_transfer_system
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_GROWING_ORDER_CHAIN_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_growing_order_chain_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-CHAIN-THEOREM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class LatticeChainTheoremCertificate:
    moment_order_symbol: str
    rank_increase_upper_bound: str
    same_rank_index_upper_bound: str
    same_rank_transition_upper_bound: str
    total_nonself_transition_upper_bound: str
    hadamard_index_lemma_proved: bool
    proper_extension_index_drop_proved: bool
    polynomial_chain_length_proved: bool
    bad_contribution_condition: str
    fixed_fraction_log_schedule_obstructed: bool
    near_log_schedule_obstructed: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class ExactChainControl:
    moment_order: int
    boolean_pattern_count: int
    reachable_state_count: int
    exact_longest_nonself_path: int
    chain_length_upper_bound: int
    bound_verified: bool


@dataclass(frozen=True)
class GrowingOrderChainScalingRow:
    n_bits: int
    register_offset: int
    schedule: str
    schedule_parameter: float
    moment_order: int
    boolean_pattern_count: int
    chain_length_upper_bound: int
    log2_bad_contribution_upper_bound: float
    asymptotic_condition_ratio: float
    finite_upper_bound_below_one: bool
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class DCPGrowingOrderChainReport:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificate: LatticeChainTheoremCertificate
    exact_controls: list[ExactChainControl]
    rows: list[GrowingOrderChainScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def lattice_chain_length_upper_bound(moment_order: int) -> int:
    if moment_order < 2:
        raise ValueError("moment_order must be at least two")
    same_rank = sum(
        math.ceil(0.5 * rank * math.log2(rank))
        for rank in range(2, moment_order + 1)
    )
    return moment_order - 1 + same_rank


def growing_order_chain_condition_ratio(
    n_bits: int,
    moment_order: int,
) -> float:
    if n_bits < 2 or moment_order < 2:
        raise ValueError("invalid scaling parameters")
    q = 1 << moment_order
    chain = lattice_chain_length_upper_bound(moment_order)
    return (
        q
        * chain
        * (math.log(n_bits) + moment_order)
        / n_bits
    )


def log2_chain_bad_contribution_bound(
    n_bits: int,
    moment_order: int,
    register_offset: int = 2,
) -> float:
    if register_offset < 0:
        raise ValueError("register offset must be nonnegative")
    q = 1 << moment_order
    chain = lattice_chain_length_upper_bound(moment_order)
    register_count = n_bits + register_offset
    natural_log_bound = (
        chain * math.log(register_count + 1)
        + chain * math.log(q + 1)
        + 0.5 * moment_order * math.log(moment_order)
        + register_offset * math.log(q)
        + n_bits * math.log1p(-1 / q)
    )
    return natural_log_bound / math.log(2)


def fixed_fraction_log_order(n_bits: int, epsilon: float) -> int:
    if not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must lie in (0,1)")
    return max(2, math.floor((1.0 - epsilon) * math.log2(n_bits)))


def near_log_order(n_bits: int, deficit_multiplier: float) -> int:
    if deficit_multiplier <= 0.0:
        raise ValueError("deficit multiplier must be positive")
    log_n = math.log2(n_bits)
    return max(
        2,
        math.floor(
            log_n - deficit_multiplier * math.log2(max(2.0, log_n))
        ),
    )


@lru_cache(maxsize=8)
def exact_longest_nonself_path(moment_order: int) -> tuple[int, int]:
    system = build_smith_transfer_system(moment_order)
    memo = {}
    visiting = set()

    def longest(state) -> int:
        if state in memo:
            return memo[state]
        if state in visiting:
            raise AssertionError("non-self transfer graph contains a cycle")
        visiting.add(state)
        value = 0
        for target, _ in system.transitions[state]:
            if target != state:
                value = max(value, 1 + longest(target))
        visiting.remove(state)
        memo[state] = value
        return value

    return longest(system.start), len(system.transitions)


def exact_chain_control(moment_order: int) -> ExactChainControl:
    longest, state_count = exact_longest_nonself_path(moment_order)
    bound = lattice_chain_length_upper_bound(moment_order)
    return ExactChainControl(
        moment_order=moment_order,
        boolean_pattern_count=1 << moment_order,
        reachable_state_count=state_count,
        exact_longest_nonself_path=longest,
        chain_length_upper_bound=bound,
        bound_verified=longest <= bound,
    )


def theorem_certificate() -> LatticeChainTheoremCertificate:
    return LatticeChainTheoremCertificate(
        moment_order_symbol="k",
        rank_increase_upper_bound="k-1",
        same_rank_index_upper_bound=(
            "[Sat(span L):L] <= |det B| <= r^(r/2) for some independent "
            "r x r Boolean minor B"
        ),
        same_rank_transition_upper_bound=(
            "ceil((r/2)log_2 r) proper extensions while rank equals r"
        ),
        total_nonself_transition_upper_bound=(
            "L(k)=(k-1)+sum_{r=2}^k ceil((r/2)log_2 r)=O(k^2 log k)"
        ),
        hadamard_index_lemma_proved=True,
        proper_extension_index_drop_proved=True,
        polynomial_chain_length_proved=True,
        bad_contribution_condition=(
            "2^k L(k)(log n+k)/n -> 0"
        ),
        fixed_fraction_log_schedule_obstructed=True,
        near_log_schedule_obstructed=True,
        proof=(
            "At every rank r, choose r independent Boolean generators already "
            "contained in L and r coordinate rows with nonzero determinant. "
            "The determinantal divisor [Sat(span L):L] divides every full-rank "
            "minor, so it is at most the chosen Boolean determinant and hence "
            "r^(r/2). A proper same-span extension has integer index at least "
            "two and therefore reduces this saturation index by at least two. "
            "There are at most k-1 rank increases, yielding L(k). Choose the "
            "positions and Boolean identities of the non-self columns with "
            "(m+1)^L(2^k+1)^L possibilities. Every self-loop pattern on a path "
            "to a bad terminal lattice is contained in that terminal lattice, "
            "whose relative Boolean base is at most 1-2^-k. The Smith numerator "
            "and fixed register-offset factors are bounded by k^(k/2)2^(kc). "
            "Taking logarithms gives the stated condition."
        ),
        limitations=[
            "The theorem controls the nonnegative source bad-tuple contribution.",
            "It does not cover arbitrary signed statistics or cancellation mechanisms.",
            "The window k=log_2 n-O(log log n) not satisfying the condition remains open.",
            "Orders at or above log_2 n are not closed.",
            "Reduced-basis events and non-moment geometry are not controlled.",
            "No computational lower bound or witness decoder follows.",
        ],
    )


def run_growing_order_chain_theorem(
    n_values: Sequence[int] = (
        1 << 16,
        1 << 24,
        1 << 32,
        1 << 48,
        1 << 64,
    ),
    fixed_fraction_epsilons: Sequence[float] = (0.25,),
    near_log_deficit_multipliers: Sequence[float] = (5.0,),
    register_offset: int = 2,
    exact_control_orders: Sequence[int] = (2, 3, 4, 5),
) -> DCPGrowingOrderChainReport:
    controls = [exact_chain_control(order) for order in exact_control_orders]
    rows = []
    for n_bits in n_values:
        for epsilon in fixed_fraction_epsilons:
            order = fixed_fraction_log_order(n_bits, epsilon)
            log_bound = log2_chain_bad_contribution_bound(
                n_bits, order, register_offset
            )
            rows.append(
                GrowingOrderChainScalingRow(
                    n_bits=n_bits,
                    register_offset=register_offset,
                    schedule="fixed-fraction-log",
                    schedule_parameter=epsilon,
                    moment_order=order,
                    boolean_pattern_count=1 << order,
                    chain_length_upper_bound=lattice_chain_length_upper_bound(
                        order
                    ),
                    log2_bad_contribution_upper_bound=log_bound,
                    asymptotic_condition_ratio=(
                        growing_order_chain_condition_ratio(n_bits, order)
                    ),
                    finite_upper_bound_below_one=log_bound < 0.0,
                    finite_row_is_asymptotic_theorem=False,
                )
            )
        for multiplier in near_log_deficit_multipliers:
            order = near_log_order(n_bits, multiplier)
            log_bound = log2_chain_bad_contribution_bound(
                n_bits, order, register_offset
            )
            rows.append(
                GrowingOrderChainScalingRow(
                    n_bits=n_bits,
                    register_offset=register_offset,
                    schedule="near-log-deficit",
                    schedule_parameter=multiplier,
                    moment_order=order,
                    boolean_pattern_count=1 << order,
                    chain_length_upper_bound=lattice_chain_length_upper_bound(
                        order
                    ),
                    log2_bad_contribution_upper_bound=log_bound,
                    asymptotic_condition_ratio=(
                        growing_order_chain_condition_ratio(n_bits, order)
                    ),
                    finite_upper_bound_below_one=log_bound < 0.0,
                    finite_row_is_asymptotic_theorem=False,
                )
            )
    metrics: dict[str, int | float] = {
        "exact_control_count": len(controls),
        "exact_chain_bound_failure_count": sum(
            not control.bound_verified for control in controls
        ),
        "maximum_exact_control_order": max(
            (control.moment_order for control in controls), default=0
        ),
        "maximum_exact_longest_nonself_path": max(
            (control.exact_longest_nonself_path for control in controls),
            default=0,
        ),
        "polynomial_chain_length_theorem_count": 1,
        "proved_fixed_fraction_log_obstruction_count": 1,
        "proved_near_log_deficit_obstruction_count": 1,
        "row_count": len(rows),
        "finite_bound_below_one_row_count": sum(
            row.finite_upper_bound_below_one for row in rows
        ),
        "maximum_instantiated_moment_order": max(
            (row.moment_order for row in rows), default=0
        ),
        "maximum_asymptotic_condition_ratio": max(
            (row.asymptotic_condition_ratio for row in rows), default=0.0
        ),
        "proved_final_near_log_window_obstruction_count": 0,
        "proved_signed_statistic_obstruction_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    certificate = theorem_certificate()
    return DCPGrowingOrderChainReport(
        created_at=utc_now(),
        theorem_contract={
            "source": (
                "uniform independent density-one modular subset-sum labels and target"
            ),
            "moment": (
                "nonnegative source-nongeneric ordered distinct k-tuple contribution"
            ),
            "register_regime": "m=n+c for fixed c",
            "condition": "2^k L(k)(log n+k)=o(n)",
            "closed_schedules": (
                "k<=(1-epsilon)log_2 n for fixed epsilon>0, and "
                "k<=log_2 n-(4+epsilon)log_2 log_2 n"
            ),
            "excluded": (
                "final near-log window, k>=log n, signed observables, basis geometry, "
                "and decoder complexity"
            ),
        },
        theorem_certificate=certificate,
        exact_controls=controls,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "polynomial_lattice_chain_bound_proved": True,
            "fixed_fraction_log_orders_closed": True,
            "near_log_deficit_orders_closed": True,
            "final_near_log_window_closed": False,
            "signed_statistics_closed": False,
            "reduced_basis_geometry_closed": False,
            "polynomial_witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Nonnegative growing-order moments are now obstructed almost up to "
                "logarithmic order. Survivors must enter the final near-log window, "
                "use signed cancellation, or leave moment geometry."
            ),
        },
        status="near-log-growing-order-nonnegative-moments-asymptotically-obstructed",
        summary=(
            "Proved an O(k^2 log k) non-self lattice-chain bound, replacing "
            "the previous 2^k bound and closing every fixed-fraction logarithmic "
            "moment schedule plus a conservative near-log deficit schedule."
        ),
        falsifiers_triggered=[
            "The 2^k Boolean-pattern count is not a valid worst-case chain-length prefactor.",
            "Every k<=(1-epsilon)log_2 n nonnegative bad-tuple moment schedule is asymptotically obstructed.",
            "The conservative log n-(4+epsilon)log log n schedule is also obstructed.",
            "The theorem cannot be transferred to signed observables, reduced-basis events, or decoder lower bounds.",
        ],
    )


def write_growing_order_chain_theorem(
    path: Path = DCP_GROWING_ORDER_CHAIN_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict[str, object]:
    payload = asdict(run_growing_order_chain_theorem(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-NEAR-LOG-GROWING-MOMENT-CHAIN",
                source=str(path),
                claim=(
                    "A nonnegative source bad-tuple moment at any fixed fraction "
                    "below logarithmic order can retain asymptotic density-one signal."
                ),
                reason_invalid=(
                    "Integer saturation indices bound every non-self Boolean-lattice "
                    "transfer path by O(k^2 log k), so terminal bad-state contraction "
                    "dominates whenever 2^k L(k)(log n+k)=o(n)."
                ),
                lesson=(
                    "Search only the final near-log window with full resource accounting, "
                    "a signed observable, or non-moment reduced-basis geometry."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
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
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=payload["headline_metrics"],
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={
                    "dcp_subset_sum_growing_order_chain_theorem": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_growing_order_chain_theorem()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
