"""Natural constant lower bound for the noncrossing component moment.

The component commutator target is

    Tr(D_com) = Tr(S_2^2) - sum_(e,f) Tr(H_e H_f H_e H_f),
    S_2 = sum_e H_e^2.

The first term had been left as a separate natural proof obligation.  It is
already controlled by the coefficient-space geometry.  Every canonical child
POVM is a coordinate compression

    H_e = W^* D_e W,

where ``W:C^r -> C^N`` is an isometry and the orthogonal coordinate blocks
``D_e`` have dimensions ``b_e`` summing to ``N``.  Hence

    rank(H_e) <= b_e,
    Tr(H_e^2) >= Tr(H_e)^2 / b_e.

Two applications of Cauchy--Schwarz give the exact deterministic chain

    Tr(S_2)   >= r^2/N,
    Tr(S_2^2) >= Tr(S_2)^2/r >= r^3/N^2.                 (1)

No positive component edge, trace balance, frame condition number, or random
matrix assumption is used.  The bound is sharp both for a uniform scalar POVM
and for an orthogonal projective measurement, so it cannot by itself prove a
commutator gap.

The existing final-root natural theorem supplies, on globally-distinct source
mass ``1/9-o(1)``,

    r/D_phys >= 19/128-o(1),       r/N >= 19/520-o(1).

Equation (1) therefore proves on that event

    Tr(S_2^2)/D_phys >= (19/128)(19/520)^2-o(1)
                     = 6859/34611200-o(1),               (2)

and conditional expectation at least

    6859/311500800-o(1).                                  (3)

This controls the total noncrossing term, but not the distinct-outcome part
needed by the commutator.  Terms with ``e=f`` cancel identically against the
crossing sum.  An orthogonal PVM attains (1) with all noncrossing mass diagonal
and has zero commutator.  The theorem therefore also proves that aspect/rank
data alone cannot close component M4.  One must lower-bound distinct-pair
noncrossing mass and separate it from the matching crossing word.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_noncrossing_lower_bound.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

ASYMPTOTIC_EVENT_MASS = Fraction(1, 9)
ASYMPTOTIC_COMMON_CARRIER_ASPECT = Fraction(19, 128)
ASYMPTOTIC_FIBER_COEFFICIENT_ASPECT = Fraction(19, 520)


@dataclass(frozen=True)
class CoordinateCompressionNoncrossingControl:
    control_id: str
    coefficient_dimension: int
    fiber_dimension: int
    outcome_count: int
    block_dimensions: tuple[int, ...]
    maximum_effect_rank_excess: int
    effect_sum_identity_residual: float
    observed_second_power_trace: float
    rank_cauchy_second_power_trace_lower_bound: float
    second_power_trace_bound_residual: float
    observed_noncrossing_fourth_moment: float
    coordinate_noncrossing_fourth_moment_lower_bound: float
    noncrossing_bound_residual: float
    diagonal_same_outcome_noncrossing_moment: float
    distinct_outcome_noncrossing_moment: float
    commutator_fourth_moment_gap: float
    deterministic_chain_verified: bool
    lower_bound_tight: bool
    effects_pairwise_commute: bool
    status: str


@dataclass(frozen=True)
class NaturalNoncrossingCorollary:
    conditioned_source_event_mass_lower_bound: str
    common_fiber_to_physical_carrier_lower_bound: str
    common_fiber_to_child_coefficient_lower_bound: str
    conditional_noncrossing_physical_mass_lower_bound: str
    expected_noncrossing_physical_mass_lower_bound: str
    positive_component_edge_required: bool
    trace_balance_required: bool
    natural_noncrossing_lower_bound_proved: bool
    natural_distinct_outcome_noncrossing_lower_bound_proved: bool
    natural_crossing_upper_bound_proved: bool
    natural_component_M4_positive: bool
    statement: str


@dataclass(frozen=True)
class ComponentNoncrossingLowerBoundTheorem:
    coordinate_rank_bound: str
    second_power_trace_bound: str
    noncrossing_fourth_moment_bound: str
    sharpness: str
    natural_consequence: str
    remaining_gate: str
    arbitrary_block_dimensions: bool
    arbitrary_coordinate_compression: bool
    edge_free: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentNoncrossingLowerBoundReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CoordinateCompressionNoncrossingControl]
    theorem: ComponentNoncrossingLowerBoundTheorem
    natural_corollary: NaturalNoncrossingCorollary
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def coordinate_compression_effects(
    isometry: np.ndarray,
    block_dimensions: tuple[int, ...],
) -> tuple[np.ndarray, ...]:
    if isometry.ndim != 2 or not block_dimensions:
        raise ValueError("an isometry and nonempty coordinate partition are required")
    coefficient, fiber = isometry.shape
    if fiber < 1 or coefficient < fiber:
        raise ValueError("the coefficient dimension must dominate the fiber")
    if any(block < 1 for block in block_dimensions):
        raise ValueError("coordinate blocks must be positive")
    if sum(block_dimensions) != coefficient:
        raise ValueError("coordinate blocks must partition the coefficient space")
    effects = []
    offset = 0
    for block in block_dimensions:
        rows = isometry[offset : offset + block]
        offset += block
        effect = rows.conj().T @ rows
        effects.append((effect + effect.conj().T) / 2.0)
    return tuple(effects)


def audit_coordinate_compression_noncrossing(
    control_id: str,
    isometry: np.ndarray,
    block_dimensions: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> CoordinateCompressionNoncrossingControl:
    coefficient, fiber = isometry.shape
    identity = np.eye(fiber, dtype=complex)
    isometry_residual = float(
        np.linalg.norm(isometry.conj().T @ isometry - identity, ord=2)
    )
    if isometry_residual > 1000 * tolerance:
        raise ValueError("the supplied matrix must be an isometry")
    effects = coordinate_compression_effects(isometry, block_dimensions)
    sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    ranks = tuple(
        int(np.count_nonzero(np.linalg.eigvalsh(effect) > 100 * tolerance))
        for effect in effects
    )
    rank_excess = max(
        0,
        *(rank - block for rank, block in zip(ranks, block_dimensions)),
    )
    second = sum((effect @ effect for effect in effects), np.zeros_like(identity))
    second_trace = float(np.trace(second).real)
    second_lower = fiber * fiber / coefficient
    second_residual = max(0.0, second_lower - second_trace)
    noncrossing = float(np.trace(second @ second).real)
    noncrossing_lower = fiber**3 / coefficient**2
    noncrossing_residual = max(0.0, noncrossing_lower - noncrossing)
    diagonal = sum(
        float(np.trace(effect @ effect @ effect @ effect).real)
        for effect in effects
    )
    distinct = noncrossing - diagonal
    crossing = sum(
        float(np.trace(left @ right @ left @ right).real)
        for left in effects
        for right in effects
    )
    commutator_gap = noncrossing - crossing
    commutator = max(
        (
            float(np.linalg.norm(left @ right - right @ left, ord=2))
            for left in effects
            for right in effects
        ),
        default=0.0,
    )
    verified = bool(
        max(
            sum_residual,
            second_residual,
            noncrossing_residual,
            max(0, rank_excess),
        )
        <= 1000 * tolerance
    )
    tight = abs(noncrossing - noncrossing_lower) <= 1000 * tolerance
    commute = commutator <= 1000 * tolerance
    return CoordinateCompressionNoncrossingControl(
        control_id=control_id,
        coefficient_dimension=coefficient,
        fiber_dimension=fiber,
        outcome_count=len(block_dimensions),
        block_dimensions=block_dimensions,
        maximum_effect_rank_excess=rank_excess,
        effect_sum_identity_residual=sum_residual,
        observed_second_power_trace=second_trace,
        rank_cauchy_second_power_trace_lower_bound=second_lower,
        second_power_trace_bound_residual=second_residual,
        observed_noncrossing_fourth_moment=noncrossing,
        coordinate_noncrossing_fourth_moment_lower_bound=noncrossing_lower,
        noncrossing_bound_residual=noncrossing_residual,
        diagonal_same_outcome_noncrossing_moment=diagonal,
        distinct_outcome_noncrossing_moment=distinct,
        commutator_fourth_moment_gap=commutator_gap,
        deterministic_chain_verified=verified,
        lower_bound_tight=tight,
        effects_pairwise_commute=commute,
        status=(
            "sharp-commuting-coordinate-noncrossing-bound"
            if verified and tight and commute
            else "coordinate-noncrossing-bound-verified"
            if verified
            else "coordinate-noncrossing-bound-failure"
        ),
    )


def component_noncrossing_lower_bound_theorem(
) -> ComponentNoncrossingLowerBoundTheorem:
    return ComponentNoncrossingLowerBoundTheorem(
        coordinate_rank_bound="rank(H_e)<=b_e for H_e=W^*D_eW",
        second_power_trace_bound="Tr(sum_e H_e^2)>=r^2/N",
        noncrossing_fourth_moment_bound=(
            "Tr((sum_e H_e^2)^2)>=r^3/N^2"
        ),
        sharpness=(
            "Equality holds for uniform scalar coordinate compressions and "
            "orthogonal projective measurements."
        ),
        natural_consequence=(
            "On the existing final-root event, total noncrossing/D_phys is at least "
            "(19/128)(19/520)^2-o(1)."
        ),
        remaining_gate=(
            "Lower-bound the distinct-outcome noncrossing term and separate it "
            "from its crossing partner; diagonal e=f terms cancel exactly."
        ),
        arbitrary_block_dimensions=True,
        arbitrary_coordinate_compression=True,
        edge_free=True,
        theorem_verified=True,
        status="natural-total-noncrossing-scale-closed-distinct-pair-open",
    )


def natural_noncrossing_corollary() -> NaturalNoncrossingCorollary:
    conditional = (
        ASYMPTOTIC_COMMON_CARRIER_ASPECT
        * ASYMPTOTIC_FIBER_COEFFICIENT_ASPECT**2
    )
    expected = ASYMPTOTIC_EVENT_MASS * conditional
    if conditional != Fraction(6859, 34_611_200):
        raise ArithmeticError("the advertised conditional lower bound changed")
    if expected != Fraction(6859, 311_500_800):
        raise ArithmeticError("the advertised expected lower bound changed")
    return NaturalNoncrossingCorollary(
        conditioned_source_event_mass_lower_bound=str(ASYMPTOTIC_EVENT_MASS),
        common_fiber_to_physical_carrier_lower_bound=str(
            ASYMPTOTIC_COMMON_CARRIER_ASPECT
        ),
        common_fiber_to_child_coefficient_lower_bound=str(
            ASYMPTOTIC_FIBER_COEFFICIENT_ASPECT
        ),
        conditional_noncrossing_physical_mass_lower_bound=str(conditional),
        expected_noncrossing_physical_mass_lower_bound=str(expected),
        positive_component_edge_required=False,
        trace_balance_required=False,
        natural_noncrossing_lower_bound_proved=True,
        natural_distinct_outcome_noncrossing_lower_bound_proved=False,
        natural_crossing_upper_bound_proved=False,
        natural_component_M4_positive=False,
        statement=(
            "Conditioned on globally distinct sources, at least 1/9-o(1) mass "
            "has total noncrossing physical moment at least "
            "6859/34611200-o(1); "
            "the unconditional conditioned-law expectation is at least "
            "6859/311500800-o(1). Same-outcome mass may account for this entire "
            "floor and cancels from component M4."
        ),
    )


def _uniform_scalar_isometry(
    fiber_dimension: int,
    outcome_count: int,
) -> tuple[np.ndarray, tuple[int, ...]]:
    identity = np.eye(fiber_dimension, dtype=complex)
    isometry = np.vstack(
        tuple(identity / np.sqrt(outcome_count) for _ in range(outcome_count))
    )
    return isometry, (fiber_dimension,) * outcome_count


def _orthogonal_projective_isometry(
    outcome_count: int,
    block_dimension: int,
) -> tuple[np.ndarray, tuple[int, ...]]:
    dimension = outcome_count * block_dimension
    return np.eye(dimension, dtype=complex), (block_dimension,) * outcome_count


def _random_isometry(
    coefficient_dimension: int,
    fiber_dimension: int,
    *,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(coefficient_dimension, fiber_dimension)) + 1j * rng.normal(
        size=(coefficient_dimension, fiber_dimension)
    )
    isometry, _ = np.linalg.qr(raw, mode="reduced")
    return isometry


def run_component_noncrossing_lower_bound(
) -> ComponentNoncrossingLowerBoundReport:
    scalar_isometry, scalar_blocks = _uniform_scalar_isometry(4, 7)
    projective_isometry, projective_blocks = _orthogonal_projective_isometry(5, 3)
    controls = [
        audit_coordinate_compression_noncrossing(
            "UNIFORM-SCALAR-Q7-R4",
            scalar_isometry,
            scalar_blocks,
        ),
        audit_coordinate_compression_noncrossing(
            "ORTHOGONAL-PROJECTIVE-Q5-B3",
            projective_isometry,
            projective_blocks,
        ),
        audit_coordinate_compression_noncrossing(
            "HAAR-UNEQUAL-BLOCKS-N31-R11",
            _random_isometry(31, 11, seed=1801),
            (2, 3, 5, 7, 14),
        ),
        audit_coordinate_compression_noncrossing(
            "HAAR-SPARSE-BLOCKS-N48-R17",
            _random_isometry(48, 17, seed=1811),
            (3,) * 16,
        ),
    ]
    theorem = component_noncrossing_lower_bound_theorem()
    corollary = natural_noncrossing_corollary()
    failures = sum(not row.deterministic_chain_verified for row in controls)
    exact = failures == 0 and theorem.theorem_verified
    conditional = Fraction(
        corollary.conditional_noncrossing_physical_mass_lower_bound
    )
    expected = Fraction(corollary.expected_noncrossing_physical_mass_lower_bound)
    return ComponentNoncrossingLowerBoundReport(
        created_at=utc_now(),
        theorem_contract={
            "coordinate_compression": "H_e=W^*D_eW, W^*W=I_r, sum b_e=N",
            "rank_cauchy_chain": (
                "rank(H_e)<=b_e implies Tr(S_2)>=r^2/N and "
                "Tr(S_2^2)>=r^3/N^2"
            ),
            "natural_final_root": corollary.statement,
            "scope": theorem.remaining_gate,
        },
        finite_controls=controls,
        theorem=theorem,
        natural_corollary=corollary,
        proof_obligations=[
            {
                "obligation": "lower_bound_natural_component_total_noncrossing_moment",
                "resolved": exact,
                "resolution": (
                    "Coordinate rank plus two Cauchy inequalities and the proved "
                    "final-root aspect event give a constant physical lower bound."
                ),
            },
            {
                "obligation": "avoid_unproved_component_positive_edge",
                "resolved": True,
                "resolution": (
                    "The proof uses only ranks, total coefficient dimension, and "
                    "common-fiber aspects; arbitrarily small positive eigenvalues "
                    "are allowed."
                ),
            },
            {
                "obligation": "lower_bound_distinct_outcome_noncrossing_mass",
                "resolved": False,
                "resolution": (
                    "The total floor can be entirely diagonal, as the sharp "
                    "orthogonal-PVM control demonstrates. A natural incidence or "
                    "overlap theorem must force off-diagonal mass."
                ),
            },
            {
                "obligation": "separate_distinct_noncrossing_and_crossing_words",
                "resolved": False,
                "resolution": (
                    "After e=f cancellation, compare the two distinct-leaf word "
                    "sums under canonical normalization."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Exponentially many outcomes force the noncrossing term to vanish.",
                "resolved": True,
                "resolution": (
                    "The relevant ratio is r/N, already bounded below by 19/520; "
                    "the number of coordinate blocks does not enter equation (1)."
                ),
            },
            {
                "objection": "A positive noncrossing term proves noncommutativity.",
                "resolved": True,
                "resolution": (
                    "False. Uniform scalar and orthogonal projective controls attain "
                    "the lower bound while commuting; crossing equals noncrossing."
                ),
            },
            {
                "objection": "Trace balance or a Jacobi edge is hidden in the proof.",
                "resolved": True,
                "resolution": (
                    "Weighted Cauchy uses only sum_e Tr(H_e)=r and sum_e b_e=N."
                ),
            },
            {
                "objection": "The total lower bound automatically lower-bounds distinct pairs.",
                "resolved": True,
                "resolution": (
                    "False. The orthogonal projective control has zero distinct-pair "
                    "noncrossing mass and puts the entire total moment on e=f."
                ),
            },
        ],
        headline_metrics={
            "coordinate_noncrossing_lower_bound_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "sharp_commuting_control_count": sum(
                row.lower_bound_tight and row.effects_pairwise_commute
                for row in controls
            ),
            "asymptotic_conditional_noncrossing_lower_bound": float(conditional),
            "asymptotic_expected_noncrossing_lower_bound": float(expected),
            "natural_noncrossing_lower_bound_theorem_count": int(exact),
            "natural_distinct_noncrossing_lower_bound_theorem_count": 0,
            "natural_crossing_upper_bound_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_component_total_noncrossing_moment_lower_bounded": exact,
            "natural_component_distinct_noncrossing_moment_lower_bounded": False,
            "positive_component_edge_required_for_noncrossing_bound": False,
            "natural_normalized_crossing_moment_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The total noncrossing term has a constant natural floor, but its "
                "same-outcome part cancels exactly and can contain the full floor."
            ),
        },
        status=(
            "natural-total-noncrossing-scale-closed-distinct-pair-open"
            if exact
            else "component-noncrossing-lower-bound-control-failure"
        ),
        summary=(
            "Proved a sharp total noncrossing scale and showed why dimensions alone "
            "cannot lower-bound the distinct-pair component-M4 contribution."
        ),
        falsifiers_triggered=[
            "The natural total noncrossing scale is not an open spectral-edge problem.",
            "A positive noncrossing lower bound alone cannot distinguish scalar or projective commuting POVMs.",
            "Any remaining M4 proof must force distinct-pair noncrossing mass and control its crossing partner.",
        ],
    )


def write_component_noncrossing_lower_bound_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_component_noncrossing_lower_bound())
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND."
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
                    "self_dual_wreath_component_noncrossing_lower_bound": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    payload = write_component_noncrossing_lower_bound_report()
    print(json.dumps(payload["headline_metrics"], indent=2, sort_keys=True))
