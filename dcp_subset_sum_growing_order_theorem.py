"""Uniform obstruction for sub-half-logarithmic subset-sum moment order.

For moment order k, write q=2^k.  Along a Boolean-column lattice-transfer path,
the lattice can enlarge at most q times because each non-self transition makes
at least one new Boolean pattern permanently available.  For a terminal bad
rank-r lattice with Boolean self-loop base b, row distinctness gives
``b/2^r <= 1-1/q``.

Choosing the non-self transition positions and patterns and applying the Smith
determinant bound gives

  E[B_k] <= (m+1)^q (q+1)^q k^(k/2) q^c (1-1/q)^n,

for m=n+c and fixed c.  Therefore ``E[B_k] -> 0`` whenever
``q^2 log n = 4^k log n = o(n)``.  In particular every schedule
``k(n) <= (1/2-epsilon) log_2 n`` is obstructed for fixed epsilon>0.

This does not cover the half-logarithmic boundary, larger order, signed
statistics outside the nonnegative bad-tuple contribution, or decoder costs.
"""

from __future__ import annotations

import json
import math
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


DCP_SUBSET_SUM_GROWING_ORDER_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_growing_order_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-MOMENT-THEOREM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class GrowingOrderTheoremCertificate:
    condition: str
    sufficient_schedule: str
    nonself_transition_bound: str
    path_count_bound: str
    smith_numerator_bound: str
    bad_state_contraction_bound: str
    sub_half_log_order_obstructed: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class GrowingOrderScalingRow:
    n_bits: int
    epsilon: float
    register_offset: int
    moment_order: int
    boolean_pattern_count: int
    log2_bad_contribution_upper_bound: float
    finite_upper_bound_below_one: bool
    four_to_k_log_n_over_n: float
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumGrowingOrderReport:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificate: GrowingOrderTheoremCertificate
    rows: list[GrowingOrderScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def log2_bad_contribution_bound(
    n_bits: int,
    moment_order: int,
    register_offset: int = 2,
) -> float:
    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    if moment_order < 2:
        raise ValueError("moment_order must be at least two")
    q = 1 << moment_order
    register_count = n_bits + register_offset
    natural_log_bound = (
        q * math.log(register_count + 1)
        + q * math.log(q + 1)
        + 0.5 * moment_order * math.log(moment_order)
        + register_offset * math.log(q)
        + n_bits * math.log1p(-1 / q)
    )
    return natural_log_bound / math.log(2)


def scheduled_moment_order(n_bits: int, epsilon: float) -> int:
    if not 0 < epsilon < 0.5:
        raise ValueError("epsilon must lie strictly between zero and one half")
    return max(2, math.floor((0.5 - epsilon) * math.log2(n_bits)))


def run_growing_order_theorem(
    n_values: Sequence[int] = (256, 1_024, 4_096, 65_536, 1_048_576),
    epsilons: Sequence[float] = (0.2,),
    register_offset: int = 2,
) -> DCPSubsetSumGrowingOrderReport:
    rows = []
    for n_bits in n_values:
        for epsilon in epsilons:
            order = scheduled_moment_order(n_bits, epsilon)
            q = 1 << order
            log_bound = log2_bad_contribution_bound(n_bits, order, register_offset)
            rows.append(
                GrowingOrderScalingRow(
                    n_bits=n_bits,
                    epsilon=epsilon,
                    register_offset=register_offset,
                    moment_order=order,
                    boolean_pattern_count=q,
                    log2_bad_contribution_upper_bound=log_bound,
                    finite_upper_bound_below_one=log_bound < 0,
                    four_to_k_log_n_over_n=(4**order * math.log(n_bits)) / n_bits,
                    finite_row_is_asymptotic_theorem=False,
                )
            )
    certificate = GrowingOrderTheoremCertificate(
        condition="4^k(n) * log n = o(n)",
        sufficient_schedule="k(n) <= (1/2-epsilon) log_2 n for any fixed epsilon>0",
        nonself_transition_bound="at most q=2^k lattice-enlarging columns",
        path_count_bound="(m+1)^q (q+1)^q",
        smith_numerator_bound="product of relevant Smith gcd factors <= k^(k/2)",
        bad_state_contraction_bound="b/2^r <= 1-1/q",
        sub_half_log_order_obstructed=True,
        proof=(
            "Each non-self transition adds a Boolean pattern not previously in the integer lattice, so at most q occur. "
            "Choose their positions and identities with (m+1)^q(q+1)^q possibilities. All intervening self-loop "
            "patterns lie in the final bad lattice and contribute at most b per coordinate. Hadamard bounds the Smith "
            "numerator by k^(k/2). Dividing the logarithm of the path overhead by the contraction exponent n/q leaves "
            "O(q^2 log n/n), which vanishes under the stated condition."
        ),
        limitations=[
            "The half-logarithmic boundary k approximately (1/2)log_2 n is not closed.",
            "Larger growing orders are not controlled.",
            "The theorem bounds a nonnegative source bad-tuple contribution, not arbitrary signed observables.",
            "It does not construct or rule out a polynomial decoder based on non-moment geometry.",
        ],
    )
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "finite_bound_below_one_row_count": sum(row.finite_upper_bound_below_one for row in rows),
        "maximum_instantiated_moment_order": max((row.moment_order for row in rows), default=0),
        "maximum_four_to_k_log_n_over_n": max(
            (row.four_to_k_log_n_over_n for row in rows), default=0.0
        ),
        "proved_sub_half_log_growing_order_obstruction_count": 1,
        "proved_half_log_boundary_obstruction_count": 0,
        "proved_super_half_log_order_obstruction_count": 0,
        "proved_signed_statistic_obstruction_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumGrowingOrderReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "uniform independent density-one modular subset-sum labels and target",
            "order_schedule": "k=k(n), q=2^k",
            "register_regime": "m=n+c for fixed c",
            "conclusion": "nonnegative bad-tuple source contribution tends to zero if 4^k log n=o(n)",
            "excluded": "half-log boundary, larger order, signed observables, and reduced-basis geometry",
        },
        theorem_certificate=certificate,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "sub_half_log_growing_order_closed": True,
            "half_log_boundary_closed": False,
            "larger_growing_order_closed": False,
            "signed_statistics_closed": False,
            "reduced_basis_geometry_closed": False,
            "polynomial_witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every nonnegative moment route below the half-logarithmic order threshold is asymptotically "
                "obstructed. A survivor must operate at the boundary or above with explicit resources, or leave this "
                "moment class."
            ),
        },
        status="sub-half-logarithmic-growing-order-moments-asymptotically-obstructed",
        summary=(
            f"Proved bad-tuple decay whenever 4^k log n=o(n); instantiated {len(rows)} scaling rows with "
            f"{sum(row.finite_upper_bound_below_one for row in rows)} finite bounds below one. The half-log boundary, "
            "larger orders, signed observables, and basis geometry remain open."
        ),
        falsifiers_triggered=[
            "Any fixed or sub-half-logarithmic nonnegative moment-order schedule is asymptotically obstructed.",
            "Increasing k without charging q=2^k transition patterns is rejected.",
            "Finite positive moment excess cannot override the uniform path-count theorem.",
            "The theorem does not reject half-logarithmic or signed/non-moment mechanisms.",
        ],
    )


def write_growing_order_theorem(
    path: Path = DCP_SUBSET_SUM_GROWING_ORDER_PATH,
    n_values: Sequence[int] = (256, 1_024, 4_096, 65_536, 1_048_576),
    epsilons: Sequence[float] = (0.2,),
    register_offset: int = 2,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_growing_order_theorem(
        n_values=n_values,
        epsilons=epsilons,
        register_offset=register_offset,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-SUB-HALF-LOG-MOMENT-ORDER",
                source=str(path),
                claim=(
                    "A nonnegative bad-tuple moment with 4^k log n=o(n) retains persistent source signal for "
                    "density-one modular subset sum."
                ),
                reason_invalid=(
                    "At most 2^k non-self lattice transitions occur, and their full path overhead is dominated by the "
                    "strict bad-state contraction whenever 4^k log n=o(n)."
                ),
                lesson=(
                    "Moment proposals must reach the half-logarithmic boundary or higher and charge q=2^k patterns, "
                    "or use a signed/non-moment mechanism with an explicit decoder."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-GROWING-ORDER-MOMENT-THEOREM"
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
                artifacts={"dcp_subset_sum_growing_order_theorem": str(path)},
            )
        )
    return payload
