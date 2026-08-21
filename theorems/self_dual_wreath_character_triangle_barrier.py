"""Pointwise character bounds cannot close the projected word-map target.

The canonical retained threshold is

    D_n=floor(sqrt(|S_n|)/(p(n)log2|S_n|)).

Suppose, much more strongly than known uniform character theorems, that every
nonidentity word in a parity-coset partition function obeyed

    |r_lambda(w)|=|chi_lambda(w)|/d_lambda <= 1/d_lambda <= 1/D_n.

There are order ``|S_n|^3`` input triples and six character-ratio factors, so
termwise absolute summation only gives

    |F_x| <= |S_n|^3 D_n^-6
            approximately (p(n)log2|S_n|)^6.               (1)

The right side diverges.  Squaring and summing seven sectors under a
probability measure gives the still worse bound

    S_B <= 7 |S_n|^6 D_n^-12
          approximately 7(p(n)log2|S_n|)^12.               (2)

Thus no proof that bounds six character factors pointwise and then applies
triangle inequality over the three free group inputs can prove the required
``S_B=o(1)``.  This remains true under the idealized ``|chi|<=1`` assumption;
actual general bounds are weaker.

Teyssier--Thevenin (arXiv:2411.04347, Theorem 1.6) prove

    |chi_lambda(sigma)| <= d_lambda^((1+C/log n)E(sigma)),

and their cycle-count corollary still has a positive exponent for the
ordinary character.  Those results are powerful for products of conjugacy
classes but cannot overcome (1) by termwise summation in this six-edge,
three-input contraction.

Any viable proof must preserve cancellation or use Plancherel orthogonality,
projected class kernels, collision geometry, or a comparable multilinear
estimate before taking absolute values.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_character_triangle_barrier.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-TRIANGLE-BARRIER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CharacterTriangleBarrierRecord:
    n: int
    partition_count: int
    group_order_log2: float
    canonical_dimension_threshold_log2: float
    idealized_partition_function_bound_log2: float
    idealized_seven_sector_energy_bound_log2: float
    continuous_threshold_partition_function_bound_log2: float
    continuous_threshold_energy_bound_log2: float
    idealized_bound_is_below_one: bool
    pointwise_triangle_method_certifies_decay: bool
    status: str


@dataclass(frozen=True)
class CharacterTriangleBarrierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    scaling_records: list[CharacterTriangleBarrierRecord]
    literature_boundary: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def partition_number(n: int) -> int:
    """Return ``p(n)`` by Euler's generalized pentagonal recurrence."""

    if n < 0:
        return 0
    values = [1] + [0] * n
    for target in range(1, n + 1):
        total = 0
        k = 1
        while True:
            left = k * (3 * k - 1) // 2
            right = k * (3 * k + 1) // 2
            if left > target:
                break
            sign = 1 if k % 2 else -1
            total += sign * values[target - left]
            if right <= target:
                total += sign * values[target - right]
            k += 1
        values[target] = total
    return values[n]


def character_triangle_barrier_record(n: int) -> CharacterTriangleBarrierRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    partition_count = partition_number(n)
    log_order = math.lgamma(n + 1) / math.log(2.0)
    threshold = max(
        1,
        math.isqrt(math.factorial(n))
        // max(1, math.ceil(partition_count * log_order)),
    )
    log_threshold = math.log2(threshold)
    exact_log_bound = 3.0 * log_order - 6.0 * log_threshold
    exact_energy_log_bound = math.log2(7.0) + 2.0 * exact_log_bound
    normalizer_log = math.log2(partition_count * log_order)
    continuous_log_bound = 6.0 * normalizer_log
    continuous_energy_log_bound = math.log2(7.0) + 12.0 * normalizer_log
    below_one = exact_log_bound < 0.0
    return CharacterTriangleBarrierRecord(
        n=n,
        partition_count=partition_count,
        group_order_log2=log_order,
        canonical_dimension_threshold_log2=log_threshold,
        idealized_partition_function_bound_log2=exact_log_bound,
        idealized_seven_sector_energy_bound_log2=exact_energy_log_bound,
        continuous_threshold_partition_function_bound_log2=continuous_log_bound,
        continuous_threshold_energy_bound_log2=continuous_energy_log_bound,
        idealized_bound_is_below_one=below_one,
        pointwise_triangle_method_certifies_decay=False,
        status="ideal-pointwise-character-bound-still-triangle-vacuous",
    )


def run_character_triangle_barrier() -> CharacterTriangleBarrierReport:
    rows = [
        character_triangle_barrier_record(n)
        for n in (10, 12, 16, 20, 24, 30, 40, 50, 75, 100)
    ]
    barrier = all(
        row.continuous_threshold_partition_function_bound_log2 > 0.0
        and row.continuous_threshold_energy_bound_log2 > 0.0
        and not row.pointwise_triangle_method_certifies_decay
        for row in rows
    )
    tail = rows[-1]
    return CharacterTriangleBarrierReport(
        created_at=utc_now(),
        theorem_contract={
            "idealized_pointwise_assumption": (
                "Assume |chi_lambda(w)|<=1, hence |r_lambda(w)|<=D_n^-1, "
                "on every retained nonidentity word."
            ),
            "triangle_partition_function_bound": "|F_x|<=|S_n|^3 D_n^-6.",
            "canonical_continuous_value": (
                "For D*=sqrt(n!)/(p(n)log2(n!)), the bound equals "
                "(p(n)log2(n!))^6."
            ),
            "seven_sector_energy_bound": "S_B<=7|S_n|^6D_n^-12.",
            "methodological_no_go": (
                "Pointwise character bounds followed by triangle inequality cannot "
                "prove canonical adaptive-energy decay."
            ),
            "required_replacement": (
                "Retain cancellation via projected kernels, collision geometry, "
                "orthogonality, or a multilinear norm estimate."
            ),
            "scope": (
                "This rules out a proof strategy, not decay or survival of S_B itself."
            ),
        },
        scaling_records=rows,
        literature_boundary=[
            {
                "id": "teyssier-thevenin-sharp-character-bounds-2025",
                "url": "https://arxiv.org/abs/2411.04347",
                "precise_use": (
                    "Theorem 1.6 bounds ordinary characters by a positive power of "
                    "dimension controlled by the orbit-growth exponent."
                ),
                "boundary": (
                    "It does not supply cancellation across the |S_n|^3 correlated "
                    "tetrahedral input triples."
                ),
            },
            {
                "id": "lifschitz-marmor-hypercontractive-characters-2023",
                "url": "https://arxiv.org/abs/2308.08694",
                "precise_use": (
                    "Provides strong level/cycle-sensitive character control."
                ),
                "boundary": (
                    "Any application that takes termwise absolute values before the "
                    "six-edge contraction encounters the same exponent barrier."
                ),
            },
        ],
        proof_obligations=[
            {
                "obligation": "audit_pointwise_triangle_route_at_canonical_trim",
                "resolved": barrier,
                "resolution": (
                    "Even |chi|<=1 leaves the divergent factor "
                    "(p(n)log2(n!))^6 before squaring."
                ),
            },
            {
                "obligation": "derive_cancellation_preserving_face_twist_bound",
                "resolved": False,
                "resolution": (
                    "Estimate the projected parity-coset kernel before absolute values."
                ),
            },
            {
                "obligation": "derive_cancellation_preserving_opposite_twist_bound",
                "resolved": False,
                "resolution": (
                    "Exploit the four-edge twist's distinct collision geometry rather "
                    "than recycling a pointwise ratio estimate."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A sharper constant in a known character-ratio theorem may suffice.",
                "resolved": True,
                "resolution": (
                    "The barrier assumes the stronger ordinary-character bound |chi|<=1; "
                    "constant improvements cannot change the conclusion."
                ),
            },
            {
                "objection": "Typical random words have few cycles, so triangle inequality should work.",
                "resolved": True,
                "resolution": (
                    "Even the zero-exponent ideal leaves exactly the trim normalizer to "
                    "the sixth power; typical-cycle corrections only worsen it."
                ),
            },
            {
                "objection": "The barrier proves adaptive energy survives.",
                "resolved": False,
                "resolution": (
                    "It proves only that a lossy proof method is incapable of deciding it."
                ),
            },
        ],
        headline_metrics={
            "pointwise_triangle_strategy_no_go_theorem_count": int(barrier),
            "scaling_record_count": len(rows),
            "maximum_scaling_n": tail.n,
            "n100_idealized_partition_bound_log2": (
                tail.idealized_partition_function_bound_log2
            ),
            "n100_continuous_energy_bound_log2": (
                tail.continuous_threshold_energy_bound_log2
            ),
            "cancellation_preserving_asymptotic_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pointwise_triangle_route_eliminated_proved": barrier,
            "known_character_bounds_close_adaptive_energy": False,
            "canonical_adaptive_energy_vanishes_proved": False,
            "canonical_adaptive_energy_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The available pointwise route is provably exponent-vacuous; a "
                "cancellation-preserving multilinear estimate is still missing."
            ),
        },
        status=(
            "pointwise-character-triangle-route-eliminated"
            if barrier
            else "character-triangle-barrier-control-failure"
        ),
        summary=(
            "Proved that even ideal pointwise character bounds cannot establish the "
            "canonical projected parity-coset energy estimate by triangle inequality."
        ),
        falsifiers_triggered=[
            "Improving constants in pointwise character bounds cannot close this target.",
            "Typical few-cycle word values do not help after termwise absolute summation.",
            "Future proofs must preserve cancellation across group inputs or Fourier labels.",
        ],
    )


def write_character_triangle_barrier_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_character_triangle_barrier())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_character_triangle_barrier_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
