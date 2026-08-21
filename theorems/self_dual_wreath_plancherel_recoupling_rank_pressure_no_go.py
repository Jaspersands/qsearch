"""Independent-Plancherel rank pressure trivializes the 6j certificate.

For a symmetric-group recoupling block write

    g1=g(mu,gamma,lambda), g2=g(alpha,beta,mu),
    g3=g(alpha,nu,lambda), g4=g(beta,gamma,nu).

The dimension-uniform 6j certificate bounds the squared operator norm by the
minimum of one and two raw rank bounds.  This module proves that those raw
bounds exceed one with probability tending to one when all six labels are
independent Plancherel samples.  It therefore falsifies the idea that the
certificate generically contracts an unconstrained Plancherel bulk.

Put ``G=n!``, ``q_rho=d_rho^2/G``, ``p=p(n)``, and ``delta=1/n``.  For one
Plancherel draw,

    Pr[q_rho < delta/p] <= delta,                         (1)

because there are only ``p`` atoms.  A union bound controls all six labels.
For each of the four Kronecker triples, character orthogonality gives

    g(a,b,c) = d_a d_b d_c (1+X_abc)/G,
    E[X_abc^2] = V_n := sum_(C != 1) 1/|C|.              (2)

Another union bound and Chebyshev show that all four ``1+X`` factors are at
least ``1/2`` except with probability at most ``16 V_n``.  No independence
between the four remainders is required.

On the intersection of these events, direct substitution into either raw
rank bound gives

    raw_bound >= G delta^(7/2) / (4 p^(7/2)).             (3)

The right side diverges: ``p(n)<=2^(n-1)`` and
``n!/(n 2^(n-1))^(7/2) -> infinity``.  The inherited reciprocal-class theorem
gives ``V_n=o(1)``.  Hence both raw bounds are at least one with probability
``1-o(1)``, and the clipped certificate is exactly the trivial value one.

This is deliberately an independent-label null model.  A physical
recoupling path samples intermediate labels from dimension-weighted
Kronecker transitions and correlates the two coupling trees.  Equations
(1)-(3) neither prove triviality nor contraction under that correlated law.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_plancherel_kronecker_positivity import (
    reciprocal_nonidentity_class_sum,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_recoupling_rank_pressure_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-RANK-PRESSURE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class IndependentPlancherelPressureRecord:
    n: int
    partition_count: int
    delta: float
    reciprocal_class_variance: float
    simultaneous_good_event_probability_lower_bound: float
    raw_squared_bound_lower_log2: float
    raw_squared_bound_lower_exceeds_one: bool
    status: str


@dataclass(frozen=True)
class IndependentPlancherelRankPressureReport:
    created_at: str
    theorem_contract: dict[str, Any]
    scaling_records: list[IndependentPlancherelPressureRecord]
    asymptotic_proof: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def partition_number(n: int) -> int:
    if n < 0:
        return 0
    values = [0] * (n + 1)
    values[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            values[total] += values[total - part]
    return values[n]


def raw_squared_bound_lower_log2(n: int, *, delta: float | None = None) -> float:
    """Return log2 of ``n! delta^(7/2)/(4 p(n)^(7/2))``."""

    if n < 2:
        raise ValueError("n must be at least two")
    threshold = 1 / n if delta is None else delta
    if not 0 < threshold <= 1:
        raise ValueError("delta must lie in (0,1]")
    return (
        math.lgamma(n + 1) / math.log(2)
        + 3.5 * math.log2(threshold)
        - 3.5 * math.log2(partition_number(n))
        - 2.0
    )


def good_event_probability_lower_bound(
    n: int, *, delta: float | None = None
) -> float:
    """Return the union-bound certificate ``max(0,1-6 delta-16 V_n)``."""

    if n < 2:
        raise ValueError("n must be at least two")
    threshold = 1 / n if delta is None else delta
    if not 0 < threshold <= 1:
        raise ValueError("delta must lie in (0,1]")
    variance = float(reciprocal_nonidentity_class_sum(n))
    return max(0.0, 1.0 - 6.0 * threshold - 16.0 * variance)


def pressure_record(n: int) -> IndependentPlancherelPressureRecord:
    delta = 1 / n
    variance = float(reciprocal_nonidentity_class_sum(n))
    probability = max(0.0, 1.0 - 6.0 * delta - 16.0 * variance)
    lower_log2 = raw_squared_bound_lower_log2(n, delta=delta)
    return IndependentPlancherelPressureRecord(
        n=n,
        partition_count=partition_number(n),
        delta=delta,
        reciprocal_class_variance=variance,
        simultaneous_good_event_probability_lower_bound=probability,
        raw_squared_bound_lower_log2=lower_log2,
        raw_squared_bound_lower_exceeds_one=lower_log2 > 0,
        status=(
            "certified-independent-bulk-certificate-triviality-event"
            if probability > 0 and lower_log2 > 0
            else "finite-n-asymptotic-bound-not-yet-informative"
        ),
    )


def run_plancherel_recoupling_rank_pressure_no_go(
) -> IndependentPlancherelRankPressureReport:
    rows = [pressure_record(n) for n in (8, 12, 16, 20, 24, 30)]
    tail = rows[-1]
    return IndependentPlancherelRankPressureReport(
        created_at=utc_now(),
        theorem_contract={
            "atom_event": (
                "For rho~Plancherel, Pr[q_rho<delta/p(n)]<=delta; union over "
                "six labels costs at most 6 delta."
            ),
            "kronecker_event": (
                "For each of four independent-Plancherel triples, "
                "g=d_a d_b d_c(1+X)/n! and E[X^2]=V_n; unioned Chebyshev "
                "at |X|=1/2 costs at most 16 V_n."
            ),
            "pressure_substitution": (
                "On the joint event, each of the two raw squared 6j "
                "dimension-rank bounds is at least "
                "n! delta^(7/2)/(4 p(n)^(7/2))."
            ),
            "asymptotic_conclusion": (
                "With delta=1/n, the event probability tends to one and the "
                "raw lower bound diverges, so the clipped certificate equals one."
            ),
            "scope": (
                "All six labels are independent Plancherel draws. Natural "
                "dimension-weighted coupling paths and shared-source 3nj "
                "networks are correlated and are not covered."
            ),
        },
        scaling_records=rows,
        asymptotic_proof={
            "partition_atom_count": "p(n)",
            "atom_tail_bound": "Pr[q<delta/p(n)]<=delta",
            "six_label_union_bound": "6 delta",
            "four_remainder_union_bound": "16 V_n",
            "reciprocal_class_variance": "V_n=o(1)",
            "partition_count_bound": "p(n)<=2^(n-1)",
            "factorial_dominance": (
                "n!/(n 2^(n-1))^(7/2) tends to infinity"
            ),
            "independent_bulk_certificate_trivial_with_probability_one_minus_o_one": True,
        },
        proof_obligations=[
            {
                "obligation": "independent_plancherel_6j_rank_pressure",
                "resolved": True,
                "resolution": (
                    "Atom counting, the exact normalized-Kronecker variance, "
                    "and direct substitution force both raw bounds above one."
                ),
            },
            {
                "obligation": "physical_coupling_path_rank_pressure",
                "resolved": False,
                "resolution": (
                    "Derive the joint law after conditioning intermediate labels "
                    "on dimension-weighted Kronecker transitions."
                ),
            },
            {
                "obligation": "shared_source_3nj_contraction",
                "resolved": False,
                "resolution": (
                    "Control correlated channel sums and interference across the "
                    "full row/column recoupling network."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The four Kronecker remainders share labels, so their union bound is invalid.",
                "resolved": True,
                "resolution": (
                    "A union bound needs no mutual independence; each triple has "
                    "three independent Plancherel labels under the six-label law."
                ),
            },
            {
                "objection": "Typical dimensions require an unproved limit-shape estimate.",
                "resolved": True,
                "resolution": (
                    "The lower tail uses only that Plancherel measure has p(n) atoms."
                ),
            },
            {
                "objection": "This proves the physical recoupling certificate is asymptotically trivial.",
                "resolved": False,
                "resolution": (
                    "False: physical intermediate labels are multiplicity-biased "
                    "and the two trees share leaves and final output."
                ),
            },
        ],
        headline_metrics={
            "independent_plancherel_rank_pressure_no_go_theorem_count": 1,
            "finite_scaling_record_count": len(rows),
            "tail_n": tail.n,
            "tail_good_event_probability_lower_bound": (
                tail.simultaneous_good_event_probability_lower_bound
            ),
            "tail_raw_squared_bound_lower_log2": (
                tail.raw_squared_bound_lower_log2
            ),
            "physical_path_rank_pressure_theorem_count": 0,
            "shared_source_3nj_contraction_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "independent_plancherel_bulk_certificate_trivial_aas_proved": True,
            "physical_dimension_weighted_path_certificate_trivial_proved": False,
            "physical_dimension_weighted_path_contraction_proved": False,
            "generalized_3nj_contraction_proved": False,
            "coherent_recoupling_compiled": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The generic independent bulk is closed, but the correlated "
                "physical path and its coherent 3nj transform remain unresolved."
            ),
        },
        status="independent-plancherel-rank-pressure-no-go-physical-path-open",
        summary=(
            "Proved that typical independent Plancherel Kronecker ranks erase "
            "the dimension-uniform 6j contraction certificate by a factorial margin."
        ),
        falsifiers_triggered=[
            "Generic independent Plancherel labels do not yield nontrivial rank-aware 6j contraction.",
            "A low-rank exceptional-channel argument must pay its source-mass cost.",
            "Independent-label triviality must not be promoted to the correlated physical path.",
        ],
    )


def write_plancherel_recoupling_rank_pressure_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_plancherel_recoupling_rank_pressure_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> int:
    payload = write_plancherel_recoupling_rank_pressure_no_go_report()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
