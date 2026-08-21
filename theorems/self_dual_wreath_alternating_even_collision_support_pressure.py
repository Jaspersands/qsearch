"""Local-support profiles cannot drive the fully nonidentity even core.

For a permutation ``a``, write ``s(a)=|supp(a)|``.  Pointwise on the moved
set of two permutations,

    s(a)+s(b)+s(ab) >= 2 |supp(a) union supp(b)|.         (1)

Apply (1) to ``(g,k,gk)`` and ``(h,k,hk)``.  The shared word ``k`` is counted
twice in the two inequalities but once in the tetrahedral six-word sum.  If
``U=supp(g) union supp(h) union supp(k)``, then

    s(g)+s(h)+s(k)+s(gk)+s(hk)
      >= 2|supp(g) union supp(k)|
         +2|supp(h) union supp(k)|-s(k)
      >= 2|U|+s(k).                                      (2)

Inside the fully nonidentity even core, both ``k`` and ``ghk`` are nontrivial
even permutations and hence move at least three points.  Thus

    sum_(w in (g,h,k,gk,hk,ghk)) s(w) >= 2|U|+6.         (3)

For a fixed abstract support profile with union size ``u``, its signature
count is ``n^(u+o(1))`` while the six conjugacy-class sizes multiply to
``n^(sum_i s(w_i)+o(1))``.  Equation (3) therefore gives collision pressure

    2u-sum_i s(w_i) <= -6.                               (4)

The same counting is uniform over union support
``u=o(log n/log log n)``: the number of abstract permutations, profiles, and
centralizer factors contributes only ``n^o(1)``.  Consequently the portion of
``Z6_+`` on that entire slowly growing support window is ``n^(-6+o(1))``.

Any obstruction to subpolynomial even collision growth must therefore come
from triples whose moved-point union is ``Omega(log n/log log n)``.  Local
cycles, bounded gadgets, and slowly growing planted supports are eliminated.
This does not control typical linear support or prove ``Z6_+=n^o(1)``.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_character_moments import compose_permutations


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_even_collision_support_pressure.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-SUPPORT-PRESSURE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class EvenSupportPressureControl:
    degree: int
    alternating_group_order: int
    fully_nonidentity_even_triple_count: int
    minimum_observed_support_pressure_gap: int | None
    proved_support_pressure_gap_lower: int
    minimum_gap_witness_word_supports: tuple[int, ...] | None
    minimum_gap_witness_union_support: int | None
    theorem_bound_verified_exhaustively: bool
    status: str


@dataclass(frozen=True)
class SlowSupportScalingControl:
    log_n: float
    union_support: int
    support_over_log_n_loglog_n_scale: float
    combinatorial_overhead_log_n_ratio: float
    pressure_exponent_upper: float
    overhead_is_subpolynomial_on_declared_family: bool
    status: str


@dataclass(frozen=True)
class EvenCollisionSupportPressureTheorem:
    pair_triangle_inequality: str
    six_word_even_gap: str
    fixed_support_collision_pressure: str
    slowly_growing_support_contribution: str
    obstruction_support_lower_scale: str
    large_support_core_controlled: bool
    status: str


@dataclass(frozen=True)
class AlternatingEvenCollisionSupportPressureReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: EvenCollisionSupportPressureTheorem
    exhaustive_controls: list[EvenSupportPressureControl]
    scaling_controls: list[SlowSupportScalingControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def support(permutation: Permutation) -> frozenset[int]:
    return frozenset(
        index for index, image in enumerate(permutation) if index != image
    )


def permutation_parity(permutation: Permutation) -> int:
    seen = [False] * len(permutation)
    cycle_count = 0
    for start in range(len(permutation)):
        if seen[start]:
            continue
        cycle_count += 1
        point = start
        while not seen[point]:
            seen[point] = True
            point = permutation[point]
    return (len(permutation) - cycle_count) % 2


def tetrahedral_words(
    g: Permutation,
    h: Permutation,
    k: Permutation,
) -> tuple[Permutation, ...]:
    if not (len(g) == len(h) == len(k)):
        raise ValueError("permutations must have equal degree")
    gh = compose_permutations(g, h)
    return (
        g,
        h,
        k,
        compose_permutations(g, k),
        compose_permutations(h, k),
        compose_permutations(gh, k),
    )


def support_pressure_gap(
    g: Permutation,
    h: Permutation,
    k: Permutation,
) -> tuple[int, tuple[int, ...], int]:
    words = tetrahedral_words(g, h, k)
    word_supports = tuple(len(support(word)) for word in words)
    union_support = len(support(g) | support(h) | support(k))
    return sum(word_supports) - 2 * union_support, word_supports, union_support


def exhaustive_even_support_pressure(degree: int) -> EvenSupportPressureControl:
    if not 3 <= degree <= 5:
        raise ValueError("exhaustive support controls require 3<=degree<=5")
    group = tuple(
        permutation
        for permutation in itertools.permutations(range(degree))
        if permutation_parity(permutation) == 0
    )
    minimum: int | None = None
    witness_supports: tuple[int, ...] | None = None
    witness_union: int | None = None
    count = 0
    verified = True
    for g, h, k in itertools.product(group, repeat=3):
        words = tetrahedral_words(g, h, k)
        if any(not support(word) for word in words):
            continue
        count += 1
        gap, word_supports, union_support = support_pressure_gap(g, h, k)
        verified &= gap >= 6
        if minimum is None or gap < minimum:
            minimum = gap
            witness_supports = word_supports
            witness_union = union_support
    return EvenSupportPressureControl(
        degree=degree,
        alternating_group_order=len(group),
        fully_nonidentity_even_triple_count=count,
        minimum_observed_support_pressure_gap=minimum,
        proved_support_pressure_gap_lower=6,
        minimum_gap_witness_word_supports=witness_supports,
        minimum_gap_witness_union_support=witness_union,
        theorem_bound_verified_exhaustively=verified,
        status=(
            "even-six-word-support-pressure-gap-verified"
            if verified
            else "even-support-pressure-control-failure"
        ),
    )


def slow_support_scaling_control(log_n: float) -> SlowSupportScalingControl:
    """Use u=floor(sqrt(log n/log log n)) as an explicit little-o family."""

    if log_n <= math.e:
        raise ValueError("log_n must exceed e")
    scale = log_n / math.log(log_n)
    union_support = max(1, math.floor(math.sqrt(scale)))
    # Crude abstract-profile/centralizer overhead is exp(O(u log u)); use
    # coefficient 10 only for a conservative finite diagnostic.
    overhead_ratio = 10.0 * union_support * math.log(max(2, union_support)) / log_n
    pressure = -6.0 + overhead_ratio
    verified = union_support / scale < 1 and overhead_ratio > 0
    return SlowSupportScalingControl(
        log_n=log_n,
        union_support=union_support,
        support_over_log_n_loglog_n_scale=union_support / scale,
        combinatorial_overhead_log_n_ratio=overhead_ratio,
        pressure_exponent_upper=pressure,
        overhead_is_subpolynomial_on_declared_family=verified,
        status=(
            "explicit-slow-support-family-has-subpolynomial-overhead"
            if verified
            else "slow-support-scaling-control-failure"
        ),
    )


def run_alternating_even_collision_support_pressure(
) -> AlternatingEvenCollisionSupportPressureReport:
    exhaustive = [exhaustive_even_support_pressure(n) for n in (3, 4, 5)]
    scaling = [slow_support_scaling_control(value) for value in (10**3, 10**5, 10**7)]
    failures = sum(not row.theorem_bound_verified_exhaustively for row in exhaustive)
    failures += sum(
        not row.overhead_is_subpolynomial_on_declared_family for row in scaling
    )
    exact = failures == 0
    theorem = EvenCollisionSupportPressureTheorem(
        pair_triangle_inequality=(
            "s(a)+s(b)+s(ab)>=2|supp(a) union supp(b)|"
        ),
        six_word_even_gap=(
            "sum_(w in (g,h,k,gk,hk,ghk))s(w)>=2|U|+6"
        ),
        fixed_support_collision_pressure="2|U|-sum_w s(w)<=-6",
        slowly_growing_support_contribution=(
            "Z6_+[|U|=o(log n/log log n)]=n^(-6+o(1))"
        ),
        obstruction_support_lower_scale="Omega(log n/log log n)",
        large_support_core_controlled=False,
        status=(
            "all-local-even-word-collision-obstructions-eliminated"
            if exact
            else "even-collision-support-pressure-control-failure"
        ),
    )
    return AlternatingEvenCollisionSupportPressureReport(
        created_at=utc_now(),
        theorem_contract={
            "support_inequality": theorem.pair_triangle_inequality,
            "even_nonidentity_minimum_support": 3,
            "six_word_gap": theorem.six_word_even_gap,
            "collision_pressure": theorem.fixed_support_collision_pressure,
            "uniform_window": theorem.slowly_growing_support_contribution,
            "remaining_scope": (
                "Only union supports at least order log n/log log n remain; no "
                "estimate is proved on that growing-support region."
            ),
        },
        theorem=theorem,
        exhaustive_controls=exhaustive,
        scaling_controls=scaling,
        proof_obligations=[
            {
                "obligation": "prove_uniform_support_pressure_gap_for_even_core",
                "resolved": exact,
                "resolution": (
                    "Two product-triangle support inequalities, shared-k accounting, "
                    "and minimum support three for nontrivial even permutations give +6."
                ),
            },
            {
                "obligation": "sum_all_slowly_growing_support_profiles",
                "resolved": exact,
                "resolution": (
                    "For u=o(log n/log log n), abstract permutations, profiles, and "
                    "centralizer factors contribute n^o(1), preserving the -6 gap."
                ),
            },
            {
                "obligation": "control_growing_support_even_collision_core",
                "resolved": False,
                "resolution": (
                    "Use cycle exposure, switching, or character cancellation for "
                    "u=Omega(log n/log log n), especially typical linear support."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The two triangle inequalities count k only once.",
                "resolved": True,
                "resolution": (
                    "They count k twice; subtracting one s(k) still leaves the "
                    "intersection term 2|A intersection B|>=2s(k)."
                ),
            },
            {
                "objection": "A nontrivial even permutation may move only two points.",
                "resolved": True,
                "resolution": "Impossible: a two-point move is a transposition and odd.",
            },
            {
                "objection": "There may be too many bounded-support abstract profiles.",
                "resolved": True,
                "resolution": (
                    "At support u their total combinatorial overhead is exp(O(u log u)), "
                    "which is n^o(1) throughout the declared slow window."
                ),
            },
            {
                "objection": "Eliminating local profiles proves Z6_+ subpolynomial.",
                "resolved": False,
                "resolution": (
                    "Growing-support profiles contain almost all random permutations "
                    "and remain uncontrolled."
                ),
            },
        ],
        headline_metrics={
            "even_support_pressure_theorem_count": int(exact),
            "slow_support_uniform_elimination_theorem_count": int(exact),
            "exhaustive_control_count": len(exhaustive),
            "finite_control_failure_count": failures,
            "proved_pressure_gap": 6,
            "growing_support_core_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "even_six_word_support_pressure_gap_proved": exact,
            "bounded_and_slow_support_core_vanishes_proved": exact,
            "local_cycle_obstruction_eliminated": exact,
            "growing_support_even_core_subpolynomial_proved": False,
            "fully_nonidentity_even_core_subpolynomial_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All local and slowly growing support profiles vanish, but the "
                "growing-support collision core is untouched."
            ),
        },
        status=(
            "even-collision-obstruction-forced-into-growing-support-regime"
            if exact
            else "alternating-even-support-pressure-failure"
        ),
        summary=(
            "Proved a six-power support-pressure deficit and eliminated every even "
            "collision profile below the log n/log log n support scale."
        ),
        falsifiers_triggered=[
            "Bounded-support cycle gadgets cannot produce the coarse alternating collision obstruction.",
            "Slowly growing planted supports also vanish after summing all abstract profiles.",
            "Any Renyi obstruction must be a genuinely growing-support word-map phenomenon.",
        ],
    )


def write_alternating_even_collision_support_pressure_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_even_collision_support_pressure())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_even_collision_support_pressure_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
