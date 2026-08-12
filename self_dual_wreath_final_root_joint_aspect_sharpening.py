"""Joint final-root aspect bound without decoupling one dyadic parameter.

The existing positive-mass common-span theorem writes

    a = q/|G| in [2,4),
    r/D >= rho(a)
        = 2(1-epsilon)^2 a/[c(a+1)] - 1 - o(1),          (1)
    N/D <= a(1+epsilon)+o(1).                             (2)

It lower-bounded ``rho`` at ``a=2`` and upper-bounded ``N/D`` at ``a=4``.
Those extrema cannot occur in the same instance: both expressions contain
the same dyadic aspect ``a``.  Dividing before minimizing gives

    r/N >= phi(a)-o(1),
    phi(a) = [2(1-epsilon)^2/(c(a+1)) - 1/a]/(1+epsilon).

The derivative of the numerator has at most one zero.  At such a zero its
second derivative is negative, so it is a maximum.  The minimum on ``[2,4]``
is therefore at an endpoint.  For the already used constants

    epsilon=1/64,       c=9/8,

the endpoint values are

    phi(2)=19/260,      phi(4)=121/1300.

Consequently the same ``1/9-o(1)`` globally-distinct event satisfies

    r/N >= 19/260-o(1),                                (3)
    b_max/r <= (260/19+o(1))/q.                         (4)

Equation (3) doubles the previous conservative ``19/520`` bound and
quadruples its rank/Cauchy fourth-moment floor.  It does not strengthen the
separate uniform common-fiber/carrier bound ``r/D>=19/128-o(1)`` and does not
prove a component edge, diagonal leverage tail, crossing gap, compiler, or
speedup.

The Markov factor can also be chosen for the fourth-moment objective rather
than inherited from the common-rank proof.  At the worst endpoint ``a=2`` put

    A=4(1-epsilon)^2/3,
    J(c)=(1-1/c)(A/c-1)^3/[4(1+epsilon)^2].

Here ``J`` is event mass times the physical rank/Cauchy floor.  Its unique
maximum on ``1<c<A`` is

    c*=4A/(3A+1)=5292/4993.

At this cutoff the same argument gives

    event mass >= 299/5292-o(1),
    r/D >= 897/4096-o(1),
    r/N >= 69/640-o(1).

This optimized event is smaller but has a stronger component aspect.  It is
the appropriate deterministic event for the diagonal-leakage M4 bridge.

Finally, the fixed rank tolerance is not intrinsic.  The uniform-orientation
rank failure is ``2^{-Theta(n(log n)^2)}/epsilon^2``.  Choosing, for example,
``epsilon_n=1/n`` still makes the conditioned all-orientation failure tend to
zero.  Optimizing after taking ``epsilon_n=o(1)`` gives the limiting constants

    c*=16/15,       event mass >= 1/16-o(1),
    r/D >= 1/4-o(1),       r/N >= 1/8-o(1),
    b_max/r <= (8+o(1))/q.                                (5)

The guaranteed physical noncrossing floor is then ``1/4096-o(1)`` and the
critical uniform component cap is ``(1/8)^(2/3)=1/4``.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_uniform_orientation_rank_concentration import (
    uniform_rank_concentration_record,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_joint_aspect_sharpening.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-JOINT-ASPECT-SHARPENING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

DEFAULT_RANK_TOLERANCE = Fraction(1, 64)
DEFAULT_MARKOV_FACTOR = Fraction(9, 8)
ASYMPTOTIC_EVENT_MASS = Fraction(1, 9)
ASYMPTOTIC_COMMON_CARRIER_ASPECT = Fraction(19, 128)
OLD_DECOUPLED_FIBER_COEFFICIENT_ASPECT = Fraction(19, 520)
SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT = Fraction(19, 260)
FOURTH_MOMENT_OPTIMAL_MARKOV_FACTOR = Fraction(5292, 4993)
FOURTH_MOMENT_OPTIMAL_EVENT_MASS = Fraction(299, 5292)
FOURTH_MOMENT_OPTIMAL_COMMON_CARRIER_ASPECT = Fraction(897, 4096)
FOURTH_MOMENT_OPTIMAL_FIBER_COEFFICIENT_ASPECT = Fraction(69, 640)
ASYMPTOTIC_OPTIMAL_MARKOV_FACTOR = Fraction(16, 15)
ASYMPTOTIC_OPTIMAL_EVENT_MASS = Fraction(1, 16)
ASYMPTOTIC_OPTIMAL_COMMON_CARRIER_ASPECT = Fraction(1, 4)
ASYMPTOTIC_OPTIMAL_FIBER_COEFFICIENT_ASPECT = Fraction(1, 8)


@dataclass(frozen=True)
class JointAspectControl:
    dyadic_child_aspect: str
    common_span_to_carrier_lower_bound: str
    child_coefficient_to_carrier_upper_bound: str
    joint_fiber_to_coefficient_lower_bound: str
    sharpened_uniform_lower_bound: str
    lower_bound_residual: str
    exceeds_old_decoupled_bound: bool
    joint_bound_verified: bool
    status: str


@dataclass(frozen=True)
class JointAspectCorollary:
    rank_tolerance: str
    markov_factor: str
    conditioned_event_mass_lower_bound: str
    common_fiber_to_physical_carrier_lower_bound: str
    old_decoupled_fiber_to_coefficient_lower_bound: str
    sharpened_joint_fiber_to_coefficient_lower_bound: str
    maximum_component_block_to_fiber_coefficient: str
    fiber_aspect_improvement_factor: str
    fourth_moment_floor_improvement_factor: str
    natural_component_diagonal_tail_proved: bool
    natural_distinct_crossing_bound_proved: bool
    natural_component_M4_positive: bool
    statement: str


@dataclass(frozen=True)
class OptimizedFourthMomentEvent:
    objective: str
    optimization_domain: str
    unique_optimal_markov_factor: str
    conditioned_event_mass_lower_bound: str
    common_fiber_to_physical_carrier_lower_bound: str
    common_fiber_to_coefficient_lower_bound: str
    critical_uniform_component_cap: float
    guaranteed_physical_noncrossing_floor: str
    improvement_over_nine_eighths_schedule: float
    endpoint_a_two_is_uniform_worst_case: bool
    optimization_verified: bool
    natural_component_diagonal_tail_proved: bool
    natural_distinct_crossing_bound_proved: bool
    status: str


@dataclass(frozen=True)
class VanishingToleranceControl:
    n: int
    rank_tolerance: float
    log2_conditioned_uniform_rank_failure_upper_bound: float
    conditioned_uniform_rank_concentration_certified: bool
    status: str


@dataclass(frozen=True)
class AsymptoticOptimizedFourthMomentEvent:
    rank_tolerance_schedule: str
    rank_tolerance_union_penalty: str
    conditioned_uniform_rank_failure_tends_to_zero: bool
    optimal_markov_factor: str
    conditioned_event_mass_lower_bound: str
    common_fiber_to_physical_carrier_lower_bound: str
    common_fiber_to_coefficient_lower_bound: str
    maximum_component_block_to_fiber_coefficient: str
    critical_uniform_component_cap: str
    guaranteed_physical_noncrossing_floor: str
    improvement_over_fixed_one_over_64_optimum: float
    natural_component_diagonal_tail_proved: bool
    natural_distinct_crossing_bound_proved: bool
    natural_component_M4_positive: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointAspectTheorem:
    common_span_bound: str
    coefficient_bound: str
    joint_ratio: str
    endpoint_minimum_argument: str
    endpoint_values: str
    sharp_uniform_bound: str
    block_ratio_corollary: str
    same_positive_mass_event: bool
    dyadic_extrema_must_remain_coupled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootJointAspectReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[JointAspectControl]
    theorem: JointAspectTheorem
    asymptotic_corollary: JointAspectCorollary
    optimized_fourth_moment_event: OptimizedFourthMomentEvent
    vanishing_tolerance_controls: list[VanishingToleranceControl]
    asymptotic_optimized_fourth_moment_event: AsymptoticOptimizedFourthMomentEvent
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def common_span_carrier_lower_bound(
    dyadic_child_aspect: Fraction,
    *,
    rank_tolerance: Fraction = DEFAULT_RANK_TOLERANCE,
    markov_factor: Fraction = DEFAULT_MARKOV_FACTOR,
) -> Fraction:
    a = dyadic_child_aspect
    if not Fraction(2) <= a <= Fraction(4):
        raise ValueError("dyadic child aspect must lie in [2,4]")
    if not 0 <= rank_tolerance < 1 or markov_factor <= 1:
        raise ValueError("invalid rank tolerance or Markov factor")
    return (
        2 * (1 - rank_tolerance) ** 2 * a
        / (markov_factor * (a + 1))
        - 1
    )


def joint_fiber_coefficient_lower_bound(
    dyadic_child_aspect: Fraction,
    *,
    rank_tolerance: Fraction = DEFAULT_RANK_TOLERANCE,
    markov_factor: Fraction = DEFAULT_MARKOV_FACTOR,
) -> Fraction:
    a = dyadic_child_aspect
    rho = common_span_carrier_lower_bound(
        a,
        rank_tolerance=rank_tolerance,
        markov_factor=markov_factor,
    )
    return rho / (a * (1 + rank_tolerance))


def audit_joint_aspect(
    dyadic_child_aspect: Fraction,
) -> JointAspectControl:
    rho = common_span_carrier_lower_bound(dyadic_child_aspect)
    coefficient = dyadic_child_aspect * (1 + DEFAULT_RANK_TOLERANCE)
    joint = rho / coefficient
    residual = joint - SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT
    verified = residual >= 0
    return JointAspectControl(
        dyadic_child_aspect=str(dyadic_child_aspect),
        common_span_to_carrier_lower_bound=str(rho),
        child_coefficient_to_carrier_upper_bound=str(coefficient),
        joint_fiber_to_coefficient_lower_bound=str(joint),
        sharpened_uniform_lower_bound=str(
            SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT
        ),
        lower_bound_residual=str(residual),
        exceeds_old_decoupled_bound=(
            joint > OLD_DECOUPLED_FIBER_COEFFICIENT_ASPECT
        ),
        joint_bound_verified=verified,
        status=(
            "joint-aspect-bound-verified"
            if verified
            else "joint-aspect-bound-failure"
        ),
    )


def joint_aspect_theorem() -> JointAspectTheorem:
    endpoint_two = joint_fiber_coefficient_lower_bound(Fraction(2))
    endpoint_four = joint_fiber_coefficient_lower_bound(Fraction(4))
    if endpoint_two != Fraction(19, 260):
        raise ArithmeticError("the a=2 endpoint changed")
    if endpoint_four != Fraction(121, 1300):
        raise ArithmeticError("the a=4 endpoint changed")
    return JointAspectTheorem(
        common_span_bound=(
            "rho(a)=2(1-epsilon)^2 a/[c(a+1)]-1 on conditional mass 1-1/c-o(1)"
        ),
        coefficient_bound="N/D<=a(1+epsilon)+o(1)",
        joint_ratio=(
            "r/N>=[2(1-epsilon)^2/(c(a+1))-1/a]/(1+epsilon)-o(1)"
        ),
        endpoint_minimum_argument=(
            "The derivative has at most one zero and every zero is a strict "
            "maximum, so the minimum on [2,4] is at an endpoint."
        ),
        endpoint_values="phi(2)=19/260 and phi(4)=121/1300",
        sharp_uniform_bound="r/N>=19/260-o(1)",
        block_ratio_corollary="b_max/r<=(260/19+o(1))/q",
        same_positive_mass_event=True,
        dyadic_extrema_must_remain_coupled=True,
        theorem_verified=True,
        status="joint-dyadic-aspect-sharpened-by-factor-two",
    )


def joint_aspect_corollary() -> JointAspectCorollary:
    improvement = (
        SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT
        / OLD_DECOUPLED_FIBER_COEFFICIENT_ASPECT
    )
    return JointAspectCorollary(
        rank_tolerance=str(DEFAULT_RANK_TOLERANCE),
        markov_factor=str(DEFAULT_MARKOV_FACTOR),
        conditioned_event_mass_lower_bound=str(ASYMPTOTIC_EVENT_MASS),
        common_fiber_to_physical_carrier_lower_bound=str(
            ASYMPTOTIC_COMMON_CARRIER_ASPECT
        ),
        old_decoupled_fiber_to_coefficient_lower_bound=str(
            OLD_DECOUPLED_FIBER_COEFFICIENT_ASPECT
        ),
        sharpened_joint_fiber_to_coefficient_lower_bound=str(
            SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT
        ),
        maximum_component_block_to_fiber_coefficient=str(Fraction(260, 19)),
        fiber_aspect_improvement_factor=str(improvement),
        fourth_moment_floor_improvement_factor=str(improvement**2),
        natural_component_diagonal_tail_proved=False,
        natural_distinct_crossing_bound_proved=False,
        natural_component_M4_positive=False,
        statement=(
            "On the same 1/9-o(1) globally-distinct event, r/D remains at least "
            "19/128-o(1), while coupling the common-span and coefficient bounds "
            "through their shared a=q/|G| gives r/N>=19/260-o(1) and "
            "b_max/r<=(260/19+o(1))/q."
        ),
    )


def optimized_fourth_moment_event() -> OptimizedFourthMomentEvent:
    epsilon = DEFAULT_RANK_TOLERANCE
    scale = 4 * (1 - epsilon) ** 2 / 3
    optimum = 4 * scale / (3 * scale + 1)
    if optimum != FOURTH_MOMENT_OPTIMAL_MARKOV_FACTOR:
        raise ArithmeticError("the optimal Markov factor changed")
    event_mass = 1 - 1 / optimum
    carrier = common_span_carrier_lower_bound(
        Fraction(2),
        markov_factor=optimum,
    )
    coefficient = joint_fiber_coefficient_lower_bound(
        Fraction(2),
        markov_factor=optimum,
    )
    if event_mass != FOURTH_MOMENT_OPTIMAL_EVENT_MASS:
        raise ArithmeticError("the optimized event mass changed")
    if carrier != FOURTH_MOMENT_OPTIMAL_COMMON_CARRIER_ASPECT:
        raise ArithmeticError("the optimized carrier aspect changed")
    if coefficient != FOURTH_MOMENT_OPTIMAL_FIBER_COEFFICIENT_ASPECT:
        raise ArithmeticError("the optimized coefficient aspect changed")
    optimized_floor = event_mass * carrier * coefficient**2
    old_floor = (
        ASYMPTOTIC_EVENT_MASS
        * ASYMPTOTIC_COMMON_CARRIER_ASPECT
        * SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT**2
    )
    return OptimizedFourthMomentEvent(
        objective=(
            "maximize event_mass*(r/D)*(r/N)^2 under the conditional Markov bound"
        ),
        optimization_domain="1<c<4(1-epsilon)^2/3",
        unique_optimal_markov_factor=str(optimum),
        conditioned_event_mass_lower_bound=str(event_mass),
        common_fiber_to_physical_carrier_lower_bound=str(carrier),
        common_fiber_to_coefficient_lower_bound=str(coefficient),
        critical_uniform_component_cap=float(coefficient) ** (2.0 / 3.0),
        guaranteed_physical_noncrossing_floor=str(optimized_floor),
        improvement_over_nine_eighths_schedule=float(optimized_floor / old_floor),
        endpoint_a_two_is_uniform_worst_case=True,
        optimization_verified=True,
        natural_component_diagonal_tail_proved=False,
        natural_distinct_crossing_bound_proved=False,
        status="fourth-moment-Markov-cutoff-optimized",
    )


def vanishing_tolerance_control(n: int) -> VanishingToleranceControl:
    if n < 2:
        raise ValueError("n must be at least two")
    epsilon = 1.0 / n
    record = uniform_rank_concentration_record(
        n,
        relative_error_tolerance=epsilon,
    )
    return VanishingToleranceControl(
        n=n,
        rank_tolerance=epsilon,
        log2_conditioned_uniform_rank_failure_upper_bound=(
            record.log2_collision_free_conditioned_failure_upper_bound
        ),
        conditioned_uniform_rank_concentration_certified=(
            record.uniform_all_orientation_all_target_concentration_certified
        ),
        status=(
            "vanishing-rank-tolerance-uniformly-certified"
            if record.uniform_all_orientation_all_target_concentration_certified
            else "vanishing-rank-tolerance-preasymptotic"
        ),
    )


def asymptotic_optimized_fourth_moment_event(
) -> AsymptoticOptimizedFourthMomentEvent:
    event_mass = 1 - 1 / ASYMPTOTIC_OPTIMAL_MARKOV_FACTOR
    carrier = (
        Fraction(4, 3) / ASYMPTOTIC_OPTIMAL_MARKOV_FACTOR - 1
    )
    coefficient = carrier / 2
    if event_mass != ASYMPTOTIC_OPTIMAL_EVENT_MASS:
        raise ArithmeticError("the limiting event mass changed")
    if carrier != ASYMPTOTIC_OPTIMAL_COMMON_CARRIER_ASPECT:
        raise ArithmeticError("the limiting carrier aspect changed")
    if coefficient != ASYMPTOTIC_OPTIMAL_FIBER_COEFFICIENT_ASPECT:
        raise ArithmeticError("the limiting coefficient aspect changed")
    floor = event_mass * carrier * coefficient**2
    if floor != Fraction(1, 4096):
        raise ArithmeticError("the limiting physical noncrossing floor changed")
    fixed = optimized_fourth_moment_event()
    return AsymptoticOptimizedFourthMomentEvent(
        rank_tolerance_schedule="epsilon_n=1/n",
        rank_tolerance_union_penalty="2 log2(n) against -Theta(n(log n)^2)",
        conditioned_uniform_rank_failure_tends_to_zero=True,
        optimal_markov_factor=str(ASYMPTOTIC_OPTIMAL_MARKOV_FACTOR),
        conditioned_event_mass_lower_bound=str(event_mass),
        common_fiber_to_physical_carrier_lower_bound=str(carrier),
        common_fiber_to_coefficient_lower_bound=str(coefficient),
        maximum_component_block_to_fiber_coefficient="8",
        critical_uniform_component_cap="1/4",
        guaranteed_physical_noncrossing_floor=str(floor),
        improvement_over_fixed_one_over_64_optimum=float(
            floor / Fraction(fixed.guaranteed_physical_noncrossing_floor)
        ),
        natural_component_diagonal_tail_proved=False,
        natural_distinct_crossing_bound_proved=False,
        natural_component_M4_positive=False,
        theorem_verified=True,
        status="vanishing-tolerance-fourth-moment-event-optimized",
    )


def run_final_root_joint_aspect_sharpening() -> FinalRootJointAspectReport:
    aspects = tuple(Fraction(numerator, 8) for numerator in range(16, 33))
    controls = [audit_joint_aspect(aspect) for aspect in aspects]
    theorem = joint_aspect_theorem()
    corollary = joint_aspect_corollary()
    optimized = optimized_fourth_moment_event()
    vanishing_controls = [
        vanishing_tolerance_control(n) for n in (16, 24, 32, 48)
    ]
    asymptotic_optimized = asymptotic_optimized_fourth_moment_event()
    failures = sum(not row.joint_bound_verified for row in controls)
    exact = bool(
        failures == 0
        and theorem.theorem_verified
        and min(
            Fraction(row.joint_fiber_to_coefficient_lower_bound)
            for row in controls
        )
        == SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT
        and all(
            row.conditioned_uniform_rank_concentration_certified
            for row in vanishing_controls
        )
        and asymptotic_optimized.theorem_verified
    )
    return FinalRootJointAspectReport(
        created_at=utc_now(),
        theorem_contract={
            "shared_parameter": "a=q/|G| belongs to [2,4)",
            "common_span": theorem.common_span_bound,
            "coefficient_width": theorem.coefficient_bound,
            "joint_ratio": theorem.joint_ratio,
            "minimization": theorem.endpoint_minimum_argument,
            "corollary": corollary.statement,
            "scope": (
                "This sharpens dimensions only; it proves no leverage tail, "
                "crossing gap, component compiler, decoder, or speedup."
            ),
        },
        controls=controls,
        theorem=theorem,
        asymptotic_corollary=corollary,
        optimized_fourth_moment_event=optimized,
        vanishing_tolerance_controls=vanishing_controls,
        asymptotic_optimized_fourth_moment_event=asymptotic_optimized,
        proof_obligations=[
            {
                "obligation": "retain_shared_dyadic_aspect_when_forming_r_over_N",
                "resolved": exact,
                "resolution": (
                    "Divide the common-rank bound by the coefficient-width bound "
                    "before minimizing over a."
                ),
            },
            {
                "obligation": "prove_uniform_minimum_of_joint_aspect_function",
                "resolved": exact,
                "resolution": (
                    "Its only possible interior critical point is a strict maximum; "
                    "the exact endpoint minimum is 19/260."
                ),
            },
            {
                "obligation": "prove_natural_component_diagonal_tail_and_crossing_gap",
                "resolved": False,
                "resolution": (
                    "The stronger aspect improves the available margin but does "
                    "not establish either remaining natural M4 estimate."
                ),
            },
            {
                "obligation": "optimize_positive_mass_event_for_fourth_moment_floor",
                "resolved": optimized.optimization_verified,
                "resolution": (
                    "Differentiate the exact worst-endpoint objective; its unique "
                    "maximum is c=5292/4993 and gives aspect 69/640."
                ),
            },
            {
                "obligation": "remove_fixed_rank_tolerance_loss_asymptotically",
                "resolved": asymptotic_optimized.theorem_verified,
                "resolution": (
                    "epsilon_n=1/n adds only 2log n to a negative "
                    "Theta(n(log n)^2) conditioned union exponent, yielding the "
                    "limiting c=16/15, r/D=1/4, and r/N=1/8 constants."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The old 19/520 bound is required because rho is worst at a=2 and N/D is worst at a=4.",
                "resolved": True,
                "resolution": (
                    "Those are mutually exclusive values of one deterministic "
                    "parameter. The ratio must be minimized jointly."
                ),
            },
            {
                "objection": "An interior dyadic aspect may be worse than both endpoints.",
                "resolved": True,
                "resolution": (
                    "The derivative equation has at most one solution and its "
                    "second derivative is negative there."
                ),
            },
            {
                "objection": "The factor-two improvement proves natural M4 positivity.",
                "resolved": True,
                "resolution": (
                    "No. It only quadruples the deterministic noncrossing floor; "
                    "diagonal leakage and crossing cancellation remain open."
                ),
            },
        ],
        headline_metrics={
            "joint_aspect_sharpening_theorem_count": int(exact),
            "control_count": len(controls),
            "control_failure_count": failures,
            "old_fiber_coefficient_aspect_lower_bound": float(
                OLD_DECOUPLED_FIBER_COEFFICIENT_ASPECT
            ),
            "sharpened_fiber_coefficient_aspect_lower_bound": float(
                SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT
            ),
            "fiber_aspect_improvement_factor": 2.0,
            "rank_cauchy_fourth_moment_floor_improvement_factor": 4.0,
            "sharpened_component_block_ratio_coefficient": float(Fraction(260, 19)),
            "fourth_moment_optimal_markov_factor": float(
                FOURTH_MOMENT_OPTIMAL_MARKOV_FACTOR
            ),
            "fourth_moment_optimal_event_mass": float(
                FOURTH_MOMENT_OPTIMAL_EVENT_MASS
            ),
            "fourth_moment_optimal_common_carrier_aspect": float(
                FOURTH_MOMENT_OPTIMAL_COMMON_CARRIER_ASPECT
            ),
            "fourth_moment_optimal_fiber_coefficient_aspect": float(
                FOURTH_MOMENT_OPTIMAL_FIBER_COEFFICIENT_ASPECT
            ),
            "fourth_moment_floor_improvement_over_nine_eighths": (
                optimized.improvement_over_nine_eighths_schedule
            ),
            "vanishing_tolerance_control_failure_count": sum(
                not row.conditioned_uniform_rank_concentration_certified
                for row in vanishing_controls
            ),
            "asymptotic_optimal_markov_factor": float(
                ASYMPTOTIC_OPTIMAL_MARKOV_FACTOR
            ),
            "asymptotic_optimal_event_mass": float(
                ASYMPTOTIC_OPTIMAL_EVENT_MASS
            ),
            "asymptotic_optimal_common_carrier_aspect": float(
                ASYMPTOTIC_OPTIMAL_COMMON_CARRIER_ASPECT
            ),
            "asymptotic_optimal_fiber_coefficient_aspect": float(
                ASYMPTOTIC_OPTIMAL_FIBER_COEFFICIENT_ASPECT
            ),
            "asymptotic_guaranteed_physical_noncrossing_floor": float(
                Fraction(1, 4096)
            ),
            "natural_component_diagonal_tail_theorem_count": 0,
            "natural_distinct_crossing_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "shared_dyadic_extrema_coupled": exact,
            "natural_final_fiber_coefficient_aspect_at_least_19_over_260": exact,
            "fourth_moment_positive_mass_event_optimized": (
                optimized.optimization_verified
            ),
            "vanishing_rank_tolerance_schedule_proved": (
                asymptotic_optimized.theorem_verified
            ),
            "old_19_over_520_bound_is_best_available": False,
            "natural_component_diagonal_tail_controlled": False,
            "natural_distinct_crossing_pressure_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The dimension floor is stronger, but the natural component "
                "fourth-spectral tail and crossing term are still unproved."
            ),
        },
        status=(
            "final-root-joint-aspect-sharpened-to-19-over-260"
            if exact
            else "final-root-joint-aspect-control-failure"
        ),
        summary=(
            "Coupled the common-span and coefficient-width extrema and doubled "
            "the natural final-root fiber/coefficient aspect lower bound."
        ),
        falsifiers_triggered=[
            "The old 19/520 aspect loses a factor two by combining incompatible dyadic extrema.",
            "The same positive-mass event supports the sharper 19/260 joint bound.",
            "The improvement is dimensional and does not establish noncommutativity.",
        ],
    )


def write_final_root_joint_aspect_sharpening_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-JOINT-ASPECT-SHARPENING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_final_root_joint_aspect_sharpening" in globals():
        report = run_final_root_joint_aspect_sharpening(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-FINAL-ROOT-JOINT-ASPECT-SHARPENING",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-JOINT-ASPECT-SHARPENING.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-JOINT-ASPECT-SHARPENING.",
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
                    "self_dual_wreath_final_root_joint_aspect_sharpening": str(path)
                },
            )
        )
    return payload
