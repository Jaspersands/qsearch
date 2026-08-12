"""Sharp collision-free transfer for normalized component commutator mass.

For a source portfolio ``Lambda``, let

    Z(Lambda) = Tr(D_com,Lambda) / D_phys,Lambda.

The component trace-mass bridge proves ``0 <= Z <= 1``.  Let ``C`` be the
event that all source partitions are globally distinct and write
``p=Pr(C)``.  If ``mu=E[Z]`` and ``mu_C=E[Z|C]``, then

    mu = p mu_C + (1-p) E[Z|not C].                       (1)

The range of ``Z`` makes the exact worst-case transfer

    mu_C >= max(0, (mu-(1-p))/p),                         (2)
    |mu_C-mu| <= 1-p.                                    (3)

Both bounds are sharp.  Thus an independent-Plancherel lower bound
``mu>=eta`` transfers whenever ``1-p=o(eta)``.  At information-threshold
copy count, the Plancherel birthday bound and the maximal-dimension theorem
give

    1-p <= binom(2K,2) C_n
        = exp(-Theta(sqrt(n)) + O(log(n))) = n^{-omega(1)}.

Consequently every constant or inverse-polynomial independent component M4
lower bound survives global-distinct conditioning at the same asymptotic
scale.  The conditioned physical commutator-support mass and source-block
noncommutativity probability are then each at least half of (2).

This closes only the conditioning step.  It does not prove a positive
independent-Plancherel component moment.  Exact finite collision-free masses
are strongly preasymptotic through the computable range, so finite rows below
correctly leave the transfer bound vacuous for the illustrative moment scale.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_collision_free_event_transfer import (
    stable_global_collision_free_probability,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_commutator_collision_free_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ConditionalMomentTransferBound:
    conditioning_probability: float
    independent_moment_lower_bound: float
    collision_probability_upper_bound: float
    sharp_conditioned_moment_lower_bound: float
    conditioned_physical_support_mass_lower_bound: float
    conditioned_source_block_probability_lower_bound: float
    additive_expectation_change_upper_bound: float
    lower_bound_nonvacuous: bool
    exact_bounded_variable_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class ConditionalMomentSharpnessControl:
    control_id: str
    conditioning_probability: float
    target_unconditioned_mean: float
    value_on_conditioning_event: float
    value_off_conditioning_event: float
    reconstructed_unconditioned_mean: float
    sharp_lower_bound: float
    absolute_conditional_mean_change: float
    additive_change_upper_bound: float
    lower_bound_saturated: bool
    additive_bound_saturated: bool
    status: str


@dataclass(frozen=True)
class CollisionFreeMomentScalingRecord:
    n: int
    information_threshold_copy_count: int
    selected_copy_count: int
    global_distinct_probability: float
    source_collision_probability: float
    illustrative_independent_moment_lower_bound: float
    sharp_conditioned_moment_lower_bound: float
    finite_transfer_nonvacuous: bool
    asymptotic_collision_probability_superpolynomially_small: bool
    inverse_polynomial_independent_moment_transfers_asymptotically: bool
    natural_independent_moment_lower_bound_proved: bool
    status: str


@dataclass(frozen=True)
class ComponentCommutatorCollisionFreeTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    sharpness_controls: list[ConditionalMomentSharpnessControl]
    finite_scaling: list[CollisionFreeMomentScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def conditional_moment_transfer_bound(
    conditioning_probability: float,
    independent_moment_lower_bound: float,
) -> ConditionalMomentTransferBound:
    """Return the sharp lower bound for a random variable in ``[0,1]``."""

    if not 0 < conditioning_probability <= 1:
        raise ValueError("conditioning probability must lie in (0,1]")
    if not 0 <= independent_moment_lower_bound <= 1:
        raise ValueError("moment lower bound must lie in [0,1]")
    collision = 1.0 - conditioning_probability
    conditioned = max(
        0.0,
        (independent_moment_lower_bound - collision)
        / conditioning_probability,
    )
    return ConditionalMomentTransferBound(
        conditioning_probability=conditioning_probability,
        independent_moment_lower_bound=independent_moment_lower_bound,
        collision_probability_upper_bound=collision,
        sharp_conditioned_moment_lower_bound=conditioned,
        conditioned_physical_support_mass_lower_bound=conditioned / 2.0,
        conditioned_source_block_probability_lower_bound=conditioned / 2.0,
        additive_expectation_change_upper_bound=collision,
        lower_bound_nonvacuous=conditioned > 0,
        exact_bounded_variable_transfer_proved=True,
        status=(
            "sharp-conditioned-component-moment-lower-bound-positive"
            if conditioned > 0
            else "finite-conditioned-component-moment-bound-vacuous"
        ),
    )


def sharpness_control(
    control_id: str,
    conditioning_probability: float,
    target_unconditioned_mean: float,
    *,
    tolerance: float = 1e-12,
) -> ConditionalMomentSharpnessControl:
    """Construct a two-atom distribution saturating the lower bound (2)."""

    bound = conditional_moment_transfer_bound(
        conditioning_probability,
        target_unconditioned_mean,
    )
    p = conditioning_probability
    if target_unconditioned_mean <= 1.0 - p:
        on_event = 0.0
        off_event = target_unconditioned_mean / (1.0 - p)
    else:
        off_event = 1.0
        on_event = (target_unconditioned_mean - (1.0 - p)) / p
    reconstructed = p * on_event + (1.0 - p) * off_event
    change = abs(on_event - reconstructed)
    lower_saturated = abs(on_event - bound.sharp_conditioned_moment_lower_bound) <= tolerance
    # The additive bound is saturated only at the extremal distributions with
    # event/off-event values {0,1}; other rows audit the sharp lower envelope.
    additive_saturated = abs(change - (1.0 - p)) <= tolerance
    verified = bool(
        -tolerance <= on_event <= 1.0 + tolerance
        and -tolerance <= off_event <= 1.0 + tolerance
        and abs(reconstructed - target_unconditioned_mean) <= tolerance
        and lower_saturated
        and change <= (1.0 - p) + tolerance
    )
    return ConditionalMomentSharpnessControl(
        control_id=control_id,
        conditioning_probability=p,
        target_unconditioned_mean=target_unconditioned_mean,
        value_on_conditioning_event=on_event,
        value_off_conditioning_event=off_event,
        reconstructed_unconditioned_mean=reconstructed,
        sharp_lower_bound=bound.sharp_conditioned_moment_lower_bound,
        absolute_conditional_mean_change=change,
        additive_change_upper_bound=1.0 - p,
        lower_bound_saturated=lower_saturated,
        additive_bound_saturated=additive_saturated,
        status=(
            "sharp-bounded-variable-conditioning-control-verified"
            if verified
            else "bounded-variable-conditioning-control-failure"
        ),
    )


def additive_sharpness_control(
    control_id: str,
    conditioning_probability: float,
    *,
    tolerance: float = 1e-12,
) -> ConditionalMomentSharpnessControl:
    """Construct ``Z=1_C``, which saturates the additive bound (3)."""

    if not 0 < conditioning_probability <= 1:
        raise ValueError("conditioning probability must lie in (0,1]")
    p = conditioning_probability
    mean = p
    bound = conditional_moment_transfer_bound(p, mean)
    on_event = 1.0
    off_event = 0.0
    change = 1.0 - p
    additive_saturated = abs(change - bound.additive_expectation_change_upper_bound) <= tolerance
    return ConditionalMomentSharpnessControl(
        control_id=control_id,
        conditioning_probability=p,
        target_unconditioned_mean=mean,
        value_on_conditioning_event=on_event,
        value_off_conditioning_event=off_event,
        reconstructed_unconditioned_mean=mean,
        sharp_lower_bound=bound.sharp_conditioned_moment_lower_bound,
        absolute_conditional_mean_change=change,
        additive_change_upper_bound=bound.additive_expectation_change_upper_bound,
        lower_bound_saturated=abs(on_event - bound.sharp_conditioned_moment_lower_bound) <= tolerance,
        additive_bound_saturated=additive_saturated,
        status=(
            "sharp-additive-conditioning-control-verified"
            if additive_saturated
            else "bounded-variable-conditioning-control-failure"
        ),
    )


def collision_free_moment_scaling_record(
    n: int,
    *,
    illustrative_independent_moment_lower_bound: float = 1e-3,
) -> CollisionFreeMomentScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    threshold = (math.factorial(n) - 1).bit_length()
    copies = threshold + 2
    probability = stable_global_collision_free_probability(n, copies)
    bound = conditional_moment_transfer_bound(
        probability,
        illustrative_independent_moment_lower_bound,
    )
    return CollisionFreeMomentScalingRecord(
        n=n,
        information_threshold_copy_count=threshold,
        selected_copy_count=copies,
        global_distinct_probability=probability,
        source_collision_probability=1.0 - probability,
        illustrative_independent_moment_lower_bound=(
            illustrative_independent_moment_lower_bound
        ),
        sharp_conditioned_moment_lower_bound=(
            bound.sharp_conditioned_moment_lower_bound
        ),
        finite_transfer_nonvacuous=bound.lower_bound_nonvacuous,
        asymptotic_collision_probability_superpolynomially_small=True,
        inverse_polynomial_independent_moment_transfers_asymptotically=True,
        natural_independent_moment_lower_bound_proved=False,
        status=(
            "finite-collision-free-moment-transfer-nonvacuous"
            if bound.lower_bound_nonvacuous
            else "finite-preasymptotic-transfer-vacuous-asymptotic-transfer-proved"
        ),
    )


def run_component_commutator_collision_free_transfer(
) -> ComponentCommutatorCollisionFreeTransferReport:
    controls = [
        sharpness_control("VACUOUS-BRANCH-SATURATION", 0.6, 0.2),
        sharpness_control("POSITIVE-BRANCH-SATURATION", 0.6, 0.75),
        additive_sharpness_control("ADDITIVE-BOUND-SATURATION", 0.6),
        sharpness_control("UNIT-CONDITIONING", 1.0, 0.37),
    ]
    control_failures = sum(
        row.status
        not in {
            "sharp-bounded-variable-conditioning-control-verified",
            "sharp-additive-conditioning-control-verified",
        }
        for row in controls
    )
    finite = [
        collision_free_moment_scaling_record(n)
        for n in (20, 24, 28, 32, 36, 40, 44, 48)
    ]
    finite_nonvacuous = sum(row.finite_transfer_nonvacuous for row in finite)
    exact = control_failures == 0
    return ComponentCommutatorCollisionFreeTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "sharp_conditional_expectation_bound": (
                "For 0<=Z<=1 and Pr(C)=p, E[Z|C]>=max(0,(E[Z]-(1-p))/p), "
                "and this lower envelope is attained by a two-atom law."
            ),
            "additive_stability": (
                "The exact decomposition E[Z]=pE[Z|C]+(1-p)E[Z|not C] "
                "implies |E[Z|C]-E[Z]|<=1-p."
            ),
            "plancherel_asymptotic_transfer": (
                "At K=Theta(n log n), 1-P_cf<=binom(2K,2)C_n="
                "n^{-omega(1)}. Hence every inverse-polynomial independent "
                "M4 lower bound survives globally distinct conditioning."
            ),
            "support_mass_consequence": (
                "Conditioned physical commutator-support mass and conditioned "
                "source-block noncommutativity probability are each at least "
                "half the transferred component M4 lower bound."
            ),
            "scope": (
                "The theorem closes conditioning only. It does not prove a "
                "positive independent-Plancherel component M4 or a compiler."
            ),
        },
        sharpness_controls=controls,
        finite_scaling=finite,
        proof_obligations=[
            {
                "obligation": "transfer_bounded_component_M4_through_global_distinct_conditioning",
                "resolved": exact,
                "resolution": "The sharp conditional-expectation inequality uses only 0<=Z<=1.",
            },
            {
                "obligation": "show_inverse_polynomial_M4_scale_dominates_collision_error",
                "resolved": True,
                "resolution": "The Plancherel birthday error is n^{-omega(1)} at information-threshold copy count.",
            },
            {
                "obligation": "prove_positive_independent_plancherel_leaf_resolved_green_gap",
                "resolved": False,
                "resolution": "The leaf-marked Green AABB-minus-ABAB expectation remains the sole natural mass gate.",
            },
            {
                "obligation": "construct_coherent_component_algebra_measurement",
                "resolved": False,
                "resolution": "Conditioning and support mass have no circuit or decoder content.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Conditioning can destroy a positive independent expectation even when P_cf tends to one.",
                "resolved": True,
                "resolution": "Only if the positive scale is no larger than 1-P_cf. Every inverse-polynomial scale dominates the proved superpolynomially small collision error.",
            },
            {
                "objection": "A multiplicative E[Z|C]>=E[Z]/P_cf bound follows from nonnegativity.",
                "resolved": True,
                "resolution": "False direction. The sharp lower bound must subtract the worst-case off-event mass 1-P_cf.",
            },
            {
                "objection": "Current finite n collision-free masses numerically certify the transfer.",
                "resolved": True,
                "resolution": "False through n=48 for the illustrative 1e-3 scale; the asymptotic theorem is strongly preasymptotic.",
            },
            {
                "objection": "Closing conditioning proves positive natural component mass.",
                "resolved": False,
                "resolution": "No independent-Plancherel M4 lower bound has been proved.",
            },
        ],
        headline_metrics={
            "sharp_bounded_variable_conditioning_theorem_count": int(exact),
            "inverse_polynomial_M4_collision_free_transfer_theorem_count": int(exact),
            "sharpness_control_count": len(controls),
            "sharpness_control_failure_count": control_failures,
            "finite_scaling_row_count": len(finite),
            "finite_nonvacuous_transfer_row_count": finite_nonvacuous,
            "tail_n": finite[-1].n,
            "tail_global_distinct_probability": finite[-1].global_distinct_probability,
            "natural_independent_plancherel_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "sharp_component_M4_conditioning_transfer_proved": exact,
            "inverse_polynomial_independent_M4_survives_conditioning": exact,
            "natural_independent_plancherel_M4_positive": False,
            "globally_distinct_natural_component_M4_positive": False,
            "natural_noncommutative_component_physical_mass_proved": False,
            "coherent_component_algebra_compiler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Global-distinct conditioning is no longer a gate at any "
                "inverse-polynomial moment scale, but the independent natural "
                "leaf-resolved Green gap remains unproved."
            ),
        },
        status=(
            "collision-free-component-M4-transfer-proved-independent-gap-open"
            if exact
            else "component-M4-conditioning-transfer-control-failure"
        ),
        summary=(
            "Proved the sharp bounded-variable transfer of component M4 through "
            "global-distinct conditioning and reduced the natural mass problem "
            "to the independent-Plancherel Green gap alone."
        ),
        falsifiers_triggered=[
            "A positive expectation cannot be transferred by dividing by collision-free mass; the sharp lower bound subtracts off-event mass.",
            "Finite n<=48 collision-free rows remain too preasymptotic to certify the illustrative moment scale.",
            "Any constant or inverse-polynomial independent M4 does survive asymptotically because the collision error is n^{-omega(1)}.",
            "No independent natural M4, compiler, decoder, or speedup is proved.",
        ],
    )


def write_component_commutator_collision_free_transfer_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_commutator_collision_free_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_component_commutator_collision_free_transfer_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
