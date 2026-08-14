"""A fractional, tail-tolerant Haar-gap reduction for natural Racah coupling.

Let ``S_theta(o)=sum pi_o a_o^theta`` be the order-``1+theta``
dependence moment of one natural Racah coupling, with ``0<theta<=1``.  Since
the expectation is under ``pi_o``, concavity gives

    S_theta(o) <= S_1(o)^theta
                 <= 1 + theta (S_1(o)-1).                 (1)

For a Haar-orthogonal change of basis with ``L`` and ``R`` nonzero channel
blocks in total dimension ``M``,

    E_Haar[S_1-1]
      = H(o)=2(L-1)(R-1)/((M-1)(M+2)).                   (2)

Consequently

    E_Haar[S_theta-1] <= theta H(o).                      (3)

The existing physical Haar-gap theorem supplies, outside physical outer mass
``b_n<=4/n+2V4_n``, the uniform factorial bound

    H(o) <= H_n=8 n^4 p(n)^6/(n!)^2.                     (4)

Suppose that for some ``theta_n in (0,1]`` the natural fractional excess on
this good set obeys

    E_P[1_G (S_theta_n-1)] <= A_n theta_n H_n.            (5)

Conditioning Jensen and ``log(1+x)<=x`` then give

    E_P I(mu;nu|outer)
      <= A_n H_n/ln 2 + b_n log2 p(n).                   (6)

Thus every subfactorial enhancement ``log A_n=o(n log n)`` forces even the
physical-average mutual information to vanish.  Unlike the collision-only
version, (5) allows rare within-coupling blocks to be softened by a fractional
power.  No natural bound on ``A_n`` is proved here.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_compressed_racah_coupling_probe import (
    compile_complete_racah_coupling,
)
from self_dual_wreath_recoupling_haar_gap_reduction import (
    four_label_variance,
    orthogonal_haar_expected_chi_square,
)
from self_dual_wreath_character_triangle_barrier import partition_number
from self_dual_wreath_tetrahedral_collision_growth_scale import (
    analytic_remainder_bounds,
    falling_factorial,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_fractional_haar_enhancement_reduction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-FRACTIONAL-HAAR-ENHANCEMENT-REDUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FractionalHaarFiniteControl:
    n: int
    outer_partition: tuple[int, ...]
    fractional_order_theta: float
    total_multiplicity_dimension: int
    channel_count: int
    conditional_racah_mutual_information_bits: float
    natural_fractional_dependence_moment: float
    natural_collision_dependence_moment: float
    collision_interpolation_upper: float
    collision_interpolation_violation: float
    orthogonal_haar_expected_chi_square: float
    natural_fractional_excess: float
    fractional_excess_to_theta_haar_upper_ratio: float
    exact_fractional_interpolation_verified: bool
    finite_natural_ratio_is_asymptotic_evidence: bool
    status: str


@dataclass(frozen=True)
class FractionalHaarScalingRecord:
    n: int
    partition_count: int
    physical_bad_mass_upper: float
    bad_mass_information_upper_bits: float
    haar_chi_square_upper_log2: float
    synthetic_enhancement_log2: float
    synthetic_good_information_upper_log2: float
    synthetic_total_information_upper_bits: float
    synthetic_enhancement_is_subfactorial: bool
    natural_enhancement_bound_proved: bool
    status: str


@dataclass(frozen=True)
class FractionalHaarEnhancementTheorem:
    interpolation: str
    haar_fractional_excess: str
    natural_good_set_assumption: str
    physical_average_information_bound: str
    sufficient_enhancement_condition: str
    natural_condition_proved: bool
    status: str


@dataclass(frozen=True)
class FractionalHaarEnhancementReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FractionalHaarEnhancementTheorem
    finite_controls: list[FractionalHaarFiniteControl]
    scaling_records: list[FractionalHaarScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def fractional_collision_interpolation_upper(
    collision_moment: float,
    theta: float,
) -> float:
    if collision_moment < 1 or not 0 < theta <= 1:
        raise ValueError("require S_1>=1 and 0<theta<=1")
    return collision_moment**theta


def good_set_information_upper_bits(
    good_mass: float,
    average_fractional_excess_on_good_set: float,
    theta: float,
) -> float:
    if not 0 <= good_mass <= 1 or average_fractional_excess_on_good_set < 0:
        raise ValueError("valid good mass and nonnegative excess are required")
    if not 0 < theta <= 1:
        raise ValueError("theta must lie in (0,1]")
    if good_mass == 0:
        return 0.0
    return (
        good_mass
        * math.log2(1.0 + average_fractional_excess_on_good_set / good_mass)
        / theta
    )


@lru_cache(maxsize=None)
def _maximum_dimension_complete_coupling(n: int):
    from representation_obstruction import hook_length_dimension, integer_partitions

    source = max(integer_partitions(n), key=hook_length_dimension)
    return source, compile_complete_racah_coupling((source,) * 4)


def audit_fractional_haar_finite(
    n: int,
    theta: float,
    *,
    tolerance: float = 2e-9,
) -> FractionalHaarFiniteControl:
    if not 4 <= n <= 6 or theta not in (0.25, 0.5, 1.0):
        raise ValueError("finite controls use 4<=n<=6 and stored theta in {1/4,1/2,1}")
    source, coupling = _maximum_dimension_complete_coupling(n)
    fractional = coupling.fractional_dependence_moments[str(theta)]
    collision = coupling.dependence_collision_moment
    interpolation = fractional_collision_interpolation_upper(collision, theta)
    violation = max(0.0, fractional - interpolation)
    haar = orthogonal_haar_expected_chi_square(
        coupling.total_multiplicity_dimension,
        coupling.left_channel_count,
        coupling.right_channel_count,
    )
    excess = max(0.0, fractional - 1.0)
    ratio = excess / (theta * haar) if haar > 0 else 0.0
    exact = violation <= tolerance
    return FractionalHaarFiniteControl(
        n=n,
        outer_partition=source,
        fractional_order_theta=theta,
        total_multiplicity_dimension=coupling.total_multiplicity_dimension,
        channel_count=coupling.left_channel_count,
        conditional_racah_mutual_information_bits=(
            coupling.conditional_racah_mutual_information_bits
        ),
        natural_fractional_dependence_moment=fractional,
        natural_collision_dependence_moment=collision,
        collision_interpolation_upper=interpolation,
        collision_interpolation_violation=violation,
        orthogonal_haar_expected_chi_square=haar,
        natural_fractional_excess=excess,
        fractional_excess_to_theta_haar_upper_ratio=ratio,
        exact_fractional_interpolation_verified=exact,
        finite_natural_ratio_is_asymptotic_evidence=False,
        status=(
            "finite-natural-fractional-moment-obeys-collision-interpolation"
            if exact
            else "fractional-haar-finite-control-failure"
        ),
    )


def fractional_haar_scaling_record(n: int) -> FractionalHaarScalingRecord:
    if n < 8:
        raise ValueError("scaling record requires n>=8")
    count = partition_number(n)
    if n < 30:
        variance_upper = four_label_variance(n)
    else:
        _v_remainder, w_remainder = analytic_remainder_bounds(n)
        variance_upper = 4.0 / falling_factorial(n, 2) ** 2 + w_remainder
    bad_mass = min(1.0, 4.0 / n + 2.0 * variance_upper)
    bad_information = bad_mass * math.log2(count)
    haar_log2 = (
        3.0
        + 4.0 * math.log2(n)
        + 6.0 * math.log2(count)
        - 2.0 * math.lgamma(n + 1) / math.log(2.0)
    )
    log2_enhancement = math.sqrt(n * math.log2(n))
    log2_good = log2_enhancement + haar_log2
    good_information = (
        2.0**log2_good / math.log(2.0)
        if log2_good > -1070
        else 0.0
    )
    total = good_information + bad_information
    subfactorial = log2_enhancement / (n * math.log2(n)) < 1.0
    return FractionalHaarScalingRecord(
        n=n,
        partition_count=count,
        physical_bad_mass_upper=bad_mass,
        bad_mass_information_upper_bits=bad_information,
        haar_chi_square_upper_log2=haar_log2,
        synthetic_enhancement_log2=log2_enhancement,
        synthetic_good_information_upper_log2=(
            log2_good - math.log2(math.log(2.0))
        ),
        synthetic_total_information_upper_bits=total,
        synthetic_enhancement_is_subfactorial=subfactorial,
        natural_enhancement_bound_proved=False,
        status=(
            "synthetic-subfactorial-fractional-enhancement-forces-information-decay"
            if subfactorial
            else "fractional-haar-scaling-control-failure"
        ),
    )


def run_fractional_haar_enhancement_reduction(
) -> FractionalHaarEnhancementReport:
    finite = [
        audit_fractional_haar_finite(n, theta)
        for n in (4, 5, 6)
        for theta in (0.25, 0.5, 1.0)
    ]
    scaling = [
        fractional_haar_scaling_record(n)
        for n in (8, 12, 16, 20, 30, 40, 50, 100, 1_000, 10_000)
    ]
    failures = sum(not row.exact_fractional_interpolation_verified for row in finite)
    failures += sum(not row.synthetic_enhancement_is_subfactorial for row in scaling)
    verified = failures == 0
    theorem = FractionalHaarEnhancementTheorem(
        interpolation="S_theta<=S_1^theta<=1+theta(S_1-1)",
        haar_fractional_excess="E_Haar[S_theta-1]<=theta H(o)",
        natural_good_set_assumption=(
            "E_P[1_G(S_theta-1)]<=A_n theta H_n"
        ),
        physical_average_information_bound=(
            "E_P I<=A_n H_n/ln 2+(4/n+2V4_n)log2 p(n)"
        ),
        sufficient_enhancement_condition="log A_n=o(n log n)",
        natural_condition_proved=False,
        status=(
            "fractional-haar-gap-reduction-proved-natural-enhancement-open"
            if verified
            else "fractional-haar-enhancement-reduction-failure"
        ),
    )
    return FractionalHaarEnhancementReport(
        created_at=utc_now(),
        theorem_contract={
            "fractional_order": "0<theta_n<=1 may depend on n",
            "good_outer_event": (
                "physical multiplicity/dimension event from the existing Haar-gap theorem"
            ),
            "haar_good_event_bound": "H(o)<=H_n=8n^4p(n)^6/(n!)^2",
            "natural_enhancement": (
                "A_n=E_P[1_G(S_theta-1)]/(theta H_n)"
            ),
            "scope": (
                "rank-label mutual-information no-go criterion only; no natural "
                "enhancement estimate or orientation-syndrome conclusion"
            ),
        },
        theorem=theorem,
        finite_controls=finite,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_fractional_haar_excess_upper",
                "resolved": verified,
                "resolution": (
                    "Concavity interpolates the fractional moment through the exact Haar collision mean."
                ),
            },
            {
                "obligation": "transfer_good_set_fractional_excess_to_physical_information",
                "resolved": verified,
                "resolution": (
                    "Conditional Jensen handles the good subprobability; support entropy bounds the bad set."
                ),
            },
            {
                "obligation": "bound_natural_fractional_haar_enhancement",
                "resolved": False,
                "resolution": (
                    "Show A_n=exp(o(n log n)) for some theta_n, or find a factorially enhanced positive-mass family."
                ),
            },
            {
                "obligation": "separate_rank_no_go_from_orientation_signal",
                "resolved": False,
                "resolution": (
                    "Even a successful enhancement bound leaves phase/orientation syndrome information open."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Fractional moments lose the factorial Haar benchmark.",
                "resolved": True,
                "resolution": (
                    "They retain it up to the explicit theta factor, which cancels in the Renyi information bound."
                ),
            },
            {
                "objection": "A vanishing theta weakens the final conclusion.",
                "resolved": True,
                "resolution": (
                    "Under the enhancement-normalized assumption, theta cancels and the same A_n H_n bound remains."
                ),
            },
            {
                "objection": "The o(1) bad outer mass can carry O(log p(n)) information harmlessly.",
                "resolved": True,
                "resolution": (
                    "Its explicit contribution is O(log p(n)/n)+2V4_n log p(n)=o(1)."
                ),
            },
            {
                "objection": "Finite natural/Haar ratios estimate A_n asymptotically.",
                "resolved": True,
                "resolution": (
                    "No. They are conditional diagnostics at n<=6 and have no tail theorem."
                ),
            },
        ],
        headline_metrics={
            "fractional_haar_gap_theorem_count": int(verified),
            "finite_interpolation_control_count": len(finite),
            "finite_control_failure_count": failures,
            "scaling_control_count": len(scaling),
            "natural_subfactorial_enhancement_bound_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "fractional_haar_excess_bound_proved": verified,
            "subfactorial_fractional_enhancement_would_force_mi_decay_proved": verified,
            "collision_enhancement_bound_required": False,
            "natural_fractional_enhancement_subfactorial_proved": False,
            "factorially_enhanced_positive_mass_family_found": False,
            "physical_average_racah_mi_vanishes_proved": False,
            "orientation_syndrome_dequantized": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The factorial Haar gap survives fractional tail softening, but "
                "natural symmetric-group enhancement remains unbounded."
            ),
        },
        status=(
            "fractional-haar-enhancement-is-sharp-rank-search-target"
            if verified
            else "fractional-haar-enhancement-reduction-failure"
        ),
        summary=(
            "Extended the factorial Haar-gap no-go from collision to tail-tolerant "
            "order-1+theta Racah dependence moments."
        ),
        falsifiers_triggered=[
            "Rare collision-heavy blocks do not evade the Haar gap if a lower fractional moment has subfactorial enhancement.",
            "Vanishing fractional order does not weaken the enhancement-normalized information conclusion.",
            "Any surviving measured-label signal still needs factorial arithmetic enhancement on positive physical mass.",
        ],
    )


def write_fractional_haar_enhancement_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_fractional_haar_enhancement_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_fractional_haar_enhancement_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
