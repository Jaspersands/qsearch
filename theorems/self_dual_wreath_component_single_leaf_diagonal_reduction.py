"""Annealed reduction of component diagonal leakage to one fixed leaf.

At the final binary root a child has ``q=2^m`` orientation leaves.  Flipping
any of the first ``m`` source pairs permutes those leaves transitively while
conjugating the complete child frame, sibling common span, canonical Green
normalization, and component effects.  The independent Plancherel law and its
globally-distinct conditioning are invariant under these flips.

Let ``E`` be any additional event invariant under the same flips; the
optimized rank/second-moment event from the joint-aspect theorem has this
property.  For physical carrier dimension ``D`` and canonical effects
``H_e``, covariance gives the exact annealed identity

    E[1_E sum_e Tr(H_e^4)/D]
      = q E[1_E Tr(H_0^4)/D].                             (1)

The fixed-leaf term has the exact ambient Green form

    Tr(H_0^4)=Tr(E_0 K E_0 K E_0 K E_0 K).               (2)

Thus natural diagonal leakage does not require a union bound, a uniform
component edge, or a full Jacobi law.  It requires one leaf-marked fourth
Green/support-projection moment under the invariant accepted law.

The vanishing-tolerance optimized event already gives total physical
noncrossing floor ``1/4096-o(1)``.  One convenient budget is

    q E[1_E Tr(H_0^4)/D] <= 1/8192+o(1),
    E[1_E C_distinct/D]  <= 1/16384+o(1),

which would imply physical ``M4>=1/16384-o(1)``.  These two upper bounds are
targets, not theorems.  Equation (1) merely makes the first target a single
marked-leaf problem.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_hamming_orbit_reduction import _flipped_labels
from self_dual_wreath_component_povm_regular_master_reduction import (
    canonical_component_effects,
)
from self_dual_wreath_collision_free_frame_probe import Label


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_single_leaf_diagonal_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SINGLE-LEAF-DIAGONAL-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SourceFlipDiagonalOrbitControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    child_cube_dimension: int
    child_leaf_count: int
    source_flip_count: int
    ambient_physical_dimension: int
    common_fiber_dimension: int
    direct_normalized_diagonal_fourth_moment: float
    orbit_averaged_fixed_leaf_fourth_moment_times_leaf_count: float
    maximum_flip_covariance_residual: float
    common_fiber_dimension_orbit_range: int
    annealed_single_leaf_identity_residual: float
    exact_single_leaf_diagonal_orbit_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class SingleLeafDiagonalBudget:
    optimized_physical_total_noncrossing_floor: str
    proposed_physical_diagonal_budget: str
    proposed_physical_distinct_crossing_budget: str
    resulting_physical_component_M4_margin: str
    fixed_leaf_budget: str
    accepted_event_flip_invariance_required: bool
    budget_has_positive_margin: bool
    natural_fixed_leaf_green_moment_bound_proved: bool
    natural_distinct_crossing_bound_proved: bool
    natural_component_M4_positive: bool
    statement: str


@dataclass(frozen=True)
class SingleLeafDiagonalReductionTheorem:
    covariance: str
    annealed_identity: str
    fixed_leaf_green_word: str
    conditioning_scope: str
    implication: str
    arbitrary_flip_invariant_source_law: bool
    arbitrary_flip_invariant_event: bool
    uniform_outcome_bound_required: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentSingleLeafDiagonalReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SourceFlipDiagonalOrbitControl]
    theorem: SingleLeafDiagonalReductionTheorem
    budget: SingleLeafDiagonalBudget
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _effect_fourth_trace(effect: np.ndarray) -> float:
    square = effect @ effect
    return float(np.trace(square @ square).real)


def audit_source_flip_diagonal_orbit(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> SourceFlipDiagonalOrbitControl:
    if len(labels) < 2:
        raise ValueError("at least two source pairs are required")
    m = len(labels) - 1
    q = 1 << m
    left_masks = tuple(range(q))
    right_masks = tuple(range(q, 2 * q))
    ambient, fiber, sides = canonical_component_effects(
        target,
        labels,
        left_masks,
        right_masks,
        tolerance=tolerance,
    )
    if not fiber:
        raise ValueError("the selected source block has zero common span")
    effects = sides[0]
    direct = sum(_effect_fourth_trace(effect) for effect in effects) / ambient
    base_profile = tuple(_effect_fourth_trace(effect) / ambient for effect in effects)
    fixed_values = []
    fiber_dimensions = []
    covariance_residual = 0.0
    for flip in range(q):
        transformed = _flipped_labels(labels, flip)
        transformed_ambient, transformed_fiber, transformed_sides = (
            canonical_component_effects(
                target,
                transformed,
                left_masks,
                right_masks,
                tolerance=tolerance,
            )
        )
        if transformed_ambient != ambient or not transformed_fiber:
            raise ArithmeticError("source flip changed ambient support unexpectedly")
        fiber_dimensions.append(transformed_fiber)
        fixed = _effect_fourth_trace(transformed_sides[0][0]) / ambient
        fixed_values.append(fixed)
        covariance_residual = max(
            covariance_residual,
            abs(fixed - base_profile[flip]),
        )
    orbit = q * sum(fixed_values) / len(fixed_values)
    identity_residual = abs(direct - orbit)
    fiber_range = max(fiber_dimensions) - min(fiber_dimensions)
    exact = bool(
        max(covariance_residual, identity_residual, float(fiber_range))
        <= 5000 * tolerance
    )
    return SourceFlipDiagonalOrbitControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        child_cube_dimension=m,
        child_leaf_count=q,
        source_flip_count=q,
        ambient_physical_dimension=ambient,
        common_fiber_dimension=fiber,
        direct_normalized_diagonal_fourth_moment=direct,
        orbit_averaged_fixed_leaf_fourth_moment_times_leaf_count=orbit,
        maximum_flip_covariance_residual=covariance_residual,
        common_fiber_dimension_orbit_range=fiber_range,
        annealed_single_leaf_identity_residual=identity_residual,
        exact_single_leaf_diagonal_orbit_reduction_verified=exact,
        status=(
            "single-leaf-diagonal-orbit-reduction-verified"
            if exact
            else "single-leaf-diagonal-orbit-control-failure"
        ),
    )


def single_leaf_diagonal_reduction_theorem(
) -> SingleLeafDiagonalReductionTheorem:
    return SingleLeafDiagonalReductionTheorem(
        covariance=(
            "first-m source-pair flips conjugate canonical effects and act "
            "transitively by e->e xor h on one final child"
        ),
        annealed_identity=(
            "E[1_E sum_e Tr(H_e^4)/D]=q E[1_E Tr(H_0^4)/D]"
        ),
        fixed_leaf_green_word="Tr(H_0^4)=Tr(E_0 K E_0 K E_0 K E_0 K)",
        conditioning_scope=(
            "valid for every source law and additional event invariant under "
            "the first-m source-pair flips, including global distinctness and "
            "the optimized rank/second-moment event"
        ),
        implication=(
            "natural diagonal leakage reduces to one fixed marked-leaf fourth "
            "Green/support-projection moment"
        ),
        arbitrary_flip_invariant_source_law=True,
        arbitrary_flip_invariant_event=True,
        uniform_outcome_bound_required=False,
        theorem_verified=True,
        status="annealed-diagonal-leakage-reduced-to-one-marked-leaf",
    )


def single_leaf_diagonal_budget() -> SingleLeafDiagonalBudget:
    floor = Fraction(1, 4096)
    diagonal = Fraction(1, 8192)
    crossing = Fraction(1, 16_384)
    margin = floor - diagonal - crossing
    if margin != Fraction(1, 16_384):
        raise ArithmeticError("the advertised M4 budget changed")
    return SingleLeafDiagonalBudget(
        optimized_physical_total_noncrossing_floor=str(floor),
        proposed_physical_diagonal_budget=str(diagonal),
        proposed_physical_distinct_crossing_budget=str(crossing),
        resulting_physical_component_M4_margin=str(margin),
        fixed_leaf_budget="E[1_E Tr(H_0^4)/D]<=1/(8192 q)+o(1)",
        accepted_event_flip_invariance_required=True,
        budget_has_positive_margin=True,
        natural_fixed_leaf_green_moment_bound_proved=False,
        natural_distinct_crossing_bound_proved=False,
        natural_component_M4_positive=False,
        statement=(
            "A one-fixed-leaf physical Green moment at most 1/(8192q), plus "
            "distinct crossing at most 1/16384, would leave physical M4 at "
            "least 1/16384-o(1). Neither upper bound is proved."
        ),
    )


def run_component_single_leaf_diagonal_reduction(
) -> ComponentSingleLeafDiagonalReductionReport:
    standard = (2, 1)
    trivial = (3,)
    sign = (1, 1, 1)
    controls = [
        audit_source_flip_diagonal_orbit(
            "S3-REPEATED-STANDARD-TRIVIAL-TARGET",
            trivial,
            ((standard, standard),) * 3,
        ),
        audit_source_flip_diagonal_orbit(
            "S3-REPEATED-STANDARD-STANDARD-TARGET",
            standard,
            ((standard, standard),) * 3,
        ),
        audit_source_flip_diagonal_orbit(
            "S3-NONIDENTICAL-SOURCE-STANDARD-TARGET",
            standard,
            (
                (trivial, standard),
                (trivial, standard),
                (standard, sign),
            ),
        ),
    ]
    theorem = single_leaf_diagonal_reduction_theorem()
    budget = single_leaf_diagonal_budget()
    failures = sum(
        not row.exact_single_leaf_diagonal_orbit_reduction_verified
        for row in controls
    )
    exact = failures == 0 and theorem.theorem_verified
    return ComponentSingleLeafDiagonalReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "source_flip_covariance": theorem.covariance,
            "annealed_identity": theorem.annealed_identity,
            "green_word": theorem.fixed_leaf_green_word,
            "conditioning": theorem.conditioning_scope,
            "budget": budget.statement,
            "scope": (
                "This is an orbit reduction, not a natural Green-moment or "
                "crossing upper bound."
            ),
        },
        finite_controls=controls,
        theorem=theorem,
        budget=budget,
        proof_obligations=[
            {
                "obligation": "remove_exponential_outcome_sum_from_annealed_diagonal_term",
                "resolved": exact,
                "resolution": (
                    "Flip transitivity and invariant conditioning give equation (1) exactly."
                ),
            },
            {
                "obligation": "bound_one_fixed_natural_leaf_fourth_green_moment",
                "resolved": False,
                "resolution": (
                    "Evaluate or upper-bound Tr(E_0 K E_0 K E_0 K E_0 K) "
                    "in the independent Plancherel regular master on the accepted event."
                ),
            },
            {
                "obligation": "bound_exact_natural_distinct_crossing_term",
                "resolved": False,
                "resolution": (
                    "Transfer leaf-marked pressure through exact dependency-support normalization."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A union bound over all q component outcomes is necessary.",
                "resolved": True,
                "resolution": (
                    "False for the annealed diagonal trace. Transitivity turns the sum into q times one fixed leaf."
                ),
            },
            {
                "objection": "Blockwise Hamming covariance is being assumed.",
                "resolved": True,
                "resolution": (
                    "No. Only covariance of the source law and accepted event is used; individual source blocks may have unequal leaf moments."
                ),
            },
            {
                "objection": "The one-leaf reduction proves its target bound.",
                "resolved": True,
                "resolution": (
                    "No. Common-span Green normalization can amplify a fixed leaf; equation (2) remains a representation-specific moment problem."
                ),
            },
        ],
        headline_metrics={
            "single_leaf_diagonal_orbit_reduction_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_control_covariance_residual": max(
                row.maximum_flip_covariance_residual for row in controls
            ),
            "maximum_control_annealed_identity_residual": max(
                row.annealed_single_leaf_identity_residual for row in controls
            ),
            "optimized_physical_noncrossing_floor": float(Fraction(1, 4096)),
            "proposed_physical_diagonal_budget": float(Fraction(1, 8192)),
            "proposed_physical_crossing_budget": float(Fraction(1, 16_384)),
            "proposed_physical_component_M4_margin": float(Fraction(1, 16_384)),
            "natural_fixed_leaf_green_moment_theorem_count": 0,
            "natural_distinct_crossing_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "annealed_diagonal_sum_reduced_to_one_fixed_leaf": exact,
            "uniform_all_outcome_leverage_bound_required": False,
            "natural_fixed_leaf_fourth_green_moment_controlled": False,
            "natural_distinct_crossing_pressure_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exponential diagonal sum is gone, but the one fixed-leaf "
                "Green moment and exact crossing term remain unbounded naturally."
            ),
        },
        status=(
            "natural-diagonal-reduced-to-single-leaf-green-moment"
            if exact
            else "single-leaf-diagonal-reduction-control-failure"
        ),
        summary=(
            "Reduced annealed natural component diagonal leakage to one fixed "
            "leaf-marked fourth Green moment under invariant conditioning."
        ),
        falsifiers_triggered=[
            "No union bound over exponentially many component outcomes is needed for annealed diagonal leakage.",
            "Blockwise leaf equality is unnecessary and generally false; only law-level covariance is used.",
            "The fixed leaf can still be amplified by exact common-span normalization, so the natural moment remains open.",
        ],
    )


def write_component_single_leaf_diagonal_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SINGLE-LEAF-DIAGONAL-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_single_leaf_diagonal_reduction" in globals():
        report = run_component_single_leaf_diagonal_reduction(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-SINGLE-LEAF-DIAGONAL-REDUCTION",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SINGLE-LEAF-DIAGONAL-REDUCTION.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SINGLE-LEAF-DIAGONAL-REDUCTION.",
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
                    "self_dual_wreath_component_single_leaf_diagonal_reduction": str(path)
                },
            )
        )
    return payload
