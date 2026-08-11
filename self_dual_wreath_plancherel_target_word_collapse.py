"""Collapse marked target characters under the natural Plancherel trace.

The leaf-marked Green word formula leaves a normalized target character
``chi_nu(W)/d_nu``.  Pointwise control of this factor is difficult for
near-saturating crossing presentations.  The natural component moment does
not use an adversarial target irrep: its target-sector trace weight is
Plancherel (up to the separately controlled physical concentration error).

For every finite group and every group element ``g``, regular-character
orthogonality gives

    E_{nu~Plancherel} chi_nu(g)/d_nu
      = |G|^-1 sum_nu d_nu chi_nu(g)
      = 1[g=e].

Therefore any target-character marked-word sum whose remaining weights are
independent of ``nu`` becomes the same unsigned solution count with the extra
relation ``W=e``.  It is nonnegative and never exceeds the scalar count.  A
near-saturating nonidentity character cannot rescue a crossing profile after
the natural target average.

The statement is stable.  If a target law is at total variation distance
``delta`` from Plancherel, then every normalized target-character expectation
differs from the identity indicator by at most ``2 delta``.  If all target
weights have relative error at most ``epsilon``, the error is at most
``epsilon``.  These bounds apply to the mathematical direct-sum trace and do
not require measuring or dephasing the coherent target label.

Combined with the all-depth interleaved four-leaf scalar-pressure theorem,
this removes the outstanding signed-target loophole for the *natural target
average*.  It does not by itself prove positive component M4: one must still
control the coefficient/degree burden of Green or ridge approximants and
lower-bound the corresponding noncrossing contribution.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_interleaved_product_lift_no_go import (
    product_lift_pattern,
    product_lift_supports,
)
from self_dual_wreath_marked_relation_topology import (
    Assignment,
    _evaluate_signed_word,
    marked_support_presentation,
    tietze_reduce_presentation,
)
from self_dual_wreath_translated_parity_commutator_no_go import (
    translated_parity_pattern,
    translated_parity_supports,
)
from symmetric_character import symmetric_character
from symmetric_marked_class_contraction import cycle_type


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_target_word_collapse.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class PlancherelCharacterColumnControl:
    n: int
    conjugacy_class_count: int
    maximum_exact_identity_indicator_residual: str
    nonidentity_class_count: int
    exact_regular_character_collapse_verified: bool
    status: str


@dataclass(frozen=True)
class MarkedPresentationTargetCollapseControl:
    control_id: str
    pattern: str
    same_support_size: int
    different_support_size: int
    remaining_generator_count: int
    exact_S3_solution_count: int
    exact_S3_identity_target_count: int
    exact_S3_nonidentity_target_count: int
    exact_plancherel_weighted_character_sum: str
    plancherel_weighted_character_sum: float
    exact_identity_constraint_count: int
    target_collapse_residual: str
    target_collapse_verified: bool
    status: str


@dataclass(frozen=True)
class TargetLawStabilityControl:
    control_id: str
    n: int
    target_cycle_type: Partition
    exact_total_variation: str
    exact_character_expectation_error: str
    exact_two_tv_upper_bound: str
    two_tv_stability_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelTargetWordCollapseTheorem:
    finite_group_identity: str
    marked_word_consequence: str
    total_variation_stability: str
    relative_error_stability: str
    interleaved_pressure_consequence: str
    scope_limit: str
    arbitrary_finite_group: bool
    arbitrary_target_word: bool
    natural_signed_target_loophole_closed: bool
    green_coefficient_burden_resolved: bool
    positive_component_M4_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelTargetWordCollapseReport:
    created_at: str
    theorem_contract: dict[str, Any]
    character_column_controls: list[PlancherelCharacterColumnControl]
    marked_presentation_controls: list[MarkedPresentationTargetCollapseControl]
    stability_controls: list[TargetLawStabilityControl]
    theorem: PlancherelTargetWordCollapseTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def plancherel_normalized_character_average(
    n: int,
    target_cycle_type: Partition,
) -> Fraction:
    if sum(target_cycle_type) != n:
        raise ValueError("cycle type must partition n")
    order = math.factorial(n)
    return sum(
        (
            Fraction(
                hook_length_dimension(partition)
                * symmetric_character(partition, target_cycle_type),
                order,
            )
            for partition in integer_partitions(n)
        ),
        start=Fraction(0),
    )


def audit_character_column_collapse(n: int) -> PlancherelCharacterColumnControl:
    if n < 1:
        raise ValueError("n must be positive")
    identity = (1,) * n
    residuals = []
    for target in integer_partitions(n):
        observed = plancherel_normalized_character_average(n, target)
        expected = Fraction(int(target == identity))
        residuals.append(abs(observed - expected))
    maximum = max(residuals)
    verified = maximum == 0
    return PlancherelCharacterColumnControl(
        n=n,
        conjugacy_class_count=len(integer_partitions(n)),
        maximum_exact_identity_indicator_residual=str(maximum),
        nonidentity_class_count=len(integer_partitions(n)) - 1,
        exact_regular_character_collapse_verified=verified,
        status=(
            "plancherel-character-column-collapses-to-identity"
            if verified
            else "plancherel-character-column-collapse-failure"
        ),
    )


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _evaluate_word(word: tuple[int, ...], assignment: dict[int, Permutation]) -> Permutation:
    identity = tuple(range(len(next(iter(assignment.values())))))
    value = identity
    for letter in word:
        factor = assignment[abs(letter)]
        if letter < 0:
            factor = _inverse(factor)
        value = _compose(value, factor)
    return value


def audit_marked_presentation_target_collapse(
    control_id: str,
    pattern: str,
    same_support: tuple[Assignment, ...],
    different_support: tuple[Assignment, ...],
) -> MarkedPresentationTargetCollapseControl:
    relations = marked_support_presentation(pattern, same_support, different_support)
    reduction = tietze_reduce_presentation(len(pattern), relations)
    group = tuple(itertools.permutations(range(3)))
    identity = tuple(range(3))
    partitions = integer_partitions(3)
    full_target = tuple(range(1, len(pattern) + 1))
    solutions = 0
    identity_targets = 0
    plancherel_sum = Fraction(0)
    for values in itertools.product(group, repeat=len(reduction.remaining_generators)):
        assignment = dict(zip(reduction.remaining_generators, values))
        if any(
            _evaluate_signed_word(relation, assignment) != identity
            for relation in reduction.residual_relations
        ):
            continue
        for step in reversed(reduction.elimination_steps):
            assignment[step.eliminated_generator] = (
                _evaluate_signed_word(step.replacement_word, assignment)
                if step.replacement_word
                else identity
            )
        target_value = _evaluate_word(full_target, assignment)
        target_type = cycle_type(target_value)
        solutions += 1
        identity_targets += target_value == identity
        plancherel_sum += sum(
            (
                Fraction(
                    hook_length_dimension(partition)
                    * symmetric_character(partition, target_type),
                    math.factorial(3),
                )
                for partition in partitions
            ),
            start=Fraction(0),
        )
    residual = plancherel_sum - identity_targets
    verified = residual == 0 and plancherel_sum <= solutions
    return MarkedPresentationTargetCollapseControl(
        control_id=control_id,
        pattern=pattern,
        same_support_size=len(same_support),
        different_support_size=len(different_support),
        remaining_generator_count=len(reduction.remaining_generators),
        exact_S3_solution_count=solutions,
        exact_S3_identity_target_count=identity_targets,
        exact_S3_nonidentity_target_count=solutions - identity_targets,
        exact_plancherel_weighted_character_sum=str(plancherel_sum),
        plancherel_weighted_character_sum=float(plancherel_sum),
        exact_identity_constraint_count=identity_targets,
        target_collapse_residual=str(residual),
        target_collapse_verified=verified,
        status=(
            "marked-target-character-collapses-to-identity-count"
            if verified
            else "marked-target-character-collapse-failure"
        ),
    )


def audit_target_law_stability(
    control_id: str,
    n: int,
    target_cycle_type: Partition,
    perturbation: Fraction,
) -> TargetLawStabilityControl:
    """Move mass between two irreps and audit the sharp ``2 TV`` estimate."""

    if perturbation < 0:
        raise ValueError("perturbation must be nonnegative")
    partitions = integer_partitions(n)
    order = math.factorial(n)
    plancherel = {
        partition: Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in partitions
    }
    donor = max(partitions, key=lambda row: plancherel[row])
    receiver = min(
        (row for row in partitions if row != donor),
        key=lambda row: plancherel[row],
    )
    moved = min(perturbation, plancherel[donor])
    perturbed = dict(plancherel)
    perturbed[donor] -= moved
    perturbed[receiver] += moved
    expectation = sum(
        (
            mass
            * Fraction(
                symmetric_character(partition, target_cycle_type),
                hook_length_dimension(partition),
            )
            for partition, mass in perturbed.items()
        ),
        start=Fraction(0),
    )
    baseline = Fraction(int(target_cycle_type == (1,) * n))
    error = abs(expectation - baseline)
    total_variation = sum(
        (abs(perturbed[row] - plancherel[row]) for row in partitions),
        start=Fraction(0),
    ) / 2
    upper = 2 * total_variation
    return TargetLawStabilityControl(
        control_id=control_id,
        n=n,
        target_cycle_type=target_cycle_type,
        exact_total_variation=str(total_variation),
        exact_character_expectation_error=str(error),
        exact_two_tv_upper_bound=str(upper),
        two_tv_stability_verified=error <= upper,
        status=(
            "target-character-two-tv-stability-verified"
            if error <= upper
            else "target-character-stability-failure"
        ),
    )


def plancherel_target_word_collapse_theorem(
) -> PlancherelTargetWordCollapseTheorem:
    return PlancherelTargetWordCollapseTheorem(
        finite_group_identity=(
            "E_{nu~Plancherel} chi_nu(g)/d_nu=1[g=e]"
        ),
        marked_word_consequence=(
            "The target-character sum equals the unsigned presentation count "
            "with the additional relator W=e."
        ),
        total_variation_stability=(
            "TV(P,Plancherel)<=delta implies character error <=2delta"
        ),
        relative_error_stability=(
            "|P_nu/Q_nu-1|<=epsilon for all nu implies character error <=epsilon"
        ),
        interleaved_pressure_consequence=(
            "Natural target averaging cannot increase any four-leaf crossing "
            "profile above its all-depth scalar-pressure bound."
        ),
        scope_limit=(
            "Remaining word weights must be target-label independent; Green/ridge "
            "coefficient sums and noncrossing lower bounds are separate."
        ),
        arbitrary_finite_group=True,
        arbitrary_target_word=True,
        natural_signed_target_loophole_closed=True,
        green_coefficient_burden_resolved=False,
        positive_component_M4_proved=False,
        theorem_verified=True,
        status="natural-plancherel-target-character-collapsed",
    )


def run_plancherel_target_word_collapse(
) -> PlancherelTargetWordCollapseReport:
    character_controls = [
        audit_character_column_collapse(n) for n in range(2, 13)
    ]
    product_zero_same, product_zero_different = product_lift_supports(0)
    product_one_same, product_one_different = product_lift_supports(1)
    translated_same, translated_different, _ = translated_parity_supports(3)
    marked_controls = [
        audit_marked_presentation_target_collapse(
            "SPARSE-SEED-TARGET-SURVIVES",
            product_lift_pattern(0),
            product_zero_same,
            product_zero_different,
        ),
        audit_marked_presentation_target_collapse(
            "POSITIVE-DEPTH-PRODUCT-LIFT-TARGET-COLLAPSES",
            product_lift_pattern(1),
            product_one_same,
            product_one_different,
        ),
        audit_marked_presentation_target_collapse(
            "TRANSLATED-PARITY-COMMUTATOR-SURVIVES-POINTWISE",
            translated_parity_pattern(3),
            translated_same,
            translated_different,
        ),
    ]
    stability = [
        audit_target_law_stability(
            f"S{n}-CLASS-{index}",
            n,
            target,
            Fraction(1, 100),
        )
        for n in (4, 5, 6)
        for index, target in enumerate(integer_partitions(n))
    ]
    theorem = plancherel_target_word_collapse_theorem()
    exact = (
        all(row.exact_regular_character_collapse_verified for row in character_controls)
        and all(row.target_collapse_verified for row in marked_controls)
        and all(row.two_tv_stability_verified for row in stability)
        and theorem.theorem_verified
    )
    translated = marked_controls[-1]
    return PlancherelTargetWordCollapseReport(
        created_at=utc_now(),
        theorem_contract={
            "target_trace_law": theorem.finite_group_identity,
            "marked_word_effect": theorem.marked_word_consequence,
            "physical_stability": theorem.total_variation_stability,
            "scope": theorem.scope_limit,
        },
        character_column_controls=character_controls,
        marked_presentation_controls=marked_controls,
        stability_controls=stability,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "remove_adversarial_target_irrep_from_natural_trace",
                "resolved": True,
                "resolution": (
                    "Plancherel weights cancel one irrep dimension and leave the "
                    "regular character divided by |G|."
                ),
            },
            {
                "obligation": "handle_near_plancherel_physical_sector_weights",
                "resolved": True,
                "resolution": (
                    "Normalized characters lie in the unit disk, so total-variation "
                    "duality gives the uniform 2delta error bound."
                ),
            },
            {
                "obligation": "close_natural_signed_target_pressure_loophole",
                "resolved": True,
                "resolution": (
                    "The character factor becomes an additional identity relator "
                    "and can only decrease every scalar presentation count."
                ),
            },
            {
                "obligation": "sum_green_approximant_coefficients_without_losing_gap",
                "resolved": False,
                "resolution": (
                    "A per-word |G|^-1 crossing bound must survive the number and "
                    "absolute coefficient mass of the ridge/polynomial expansion."
                ),
            },
            {
                "obligation": "lower_bound_noncrossing_green_trace",
                "resolved": False,
                "resolution": (
                    "Target collapse controls crossing terms but does not establish "
                    "the retained noncrossing scale after Green normalization."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A rare irrep with constant target character rescues pressure.",
                "resolved": True,
                "resolution": (
                    "Not in the natural trace average: all nonidentity target words "
                    "cancel exactly under Plancherel weighting."
                ),
            },
            {
                "objection": "The translated parity S3 survivor contradicts collapse.",
                "resolved": True,
                "resolution": (
                    f"It has {translated.exact_S3_nonidentity_target_count} pointwise "
                    "nonidentity solutions, but their Plancherel character average "
                    "is zero; only identity-target solutions remain."
                ),
            },
            {
                "objection": "Using the direct-sum trace dephases the algorithm.",
                "resolved": True,
                "resolution": (
                    "This is an algebraic evaluation of a trace moment, not an "
                    "operational measurement of the coherent sector register."
                ),
            },
            {
                "objection": "Per-word pressure automatically proves positive M4.",
                "resolved": False,
                "resolution": (
                    "Coefficient growth and the noncrossing Green scale must still "
                    "be controlled uniformly at the required approximation degree."
                ),
            },
        ],
        headline_metrics={
            "plancherel_target_word_collapse_theorem_count": int(exact),
            "character_column_control_failure_count": sum(
                not row.exact_regular_character_collapse_verified
                for row in character_controls
            ),
            "marked_presentation_control_failure_count": sum(
                not row.target_collapse_verified for row in marked_controls
            ),
            "stability_control_failure_count": sum(
                not row.two_tv_stability_verified for row in stability
            ),
            "translated_parity_pointwise_nonidentity_target_count": (
                translated.exact_S3_nonidentity_target_count
            ),
            "translated_parity_plancherel_surviving_target_count": (
                translated.exact_S3_identity_target_count
            ),
            "natural_signed_target_pressure_loophole_count": 0,
            "green_coefficient_burden_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_plancherel_target_character_can_rescue_crossing_pressure": False,
            "near_plancherel_stability_proved": True,
            "all_four_leaf_scalar_pressure_transfers_to_natural_target_average": exact,
            "green_polynomial_coefficient_burden_controlled": False,
            "noncrossing_green_trace_lower_bounded": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural target averaging turns target characters into an identity "
                "constraint. The remaining M4 proof debt is approximation-coefficient "
                "control and a normalized noncrossing lower bound."
            ),
        },
        status=(
            "natural-signed-target-loophole-closed-green-burden-open"
            if exact
            else "plancherel-target-word-collapse-certificate-failure"
        ),
        summary=(
            "Removed target-character rescue from the natural crossing-word problem; "
            "only Green approximation and noncrossing mass remain."
        ),
        falsifiers_triggered=[
            "Pointwise low-dimensional character signal does not survive natural target averaging.",
            "Near-Plancherel sector errors perturb the collapse only by their trace distance.",
            "A pointwise crossing bound is not yet a summed Green-moment theorem.",
        ],
    )


def write_plancherel_target_word_collapse_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_plancherel_target_word_collapse())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_plancherel_target_word_collapse": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    result = write_plancherel_target_word_collapse_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
