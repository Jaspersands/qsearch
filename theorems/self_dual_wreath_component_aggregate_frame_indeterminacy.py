"""Aggregate sibling frames do not determine component commutator mass.

The repository has exact low-order moments, word normal forms, and surrogate
resolvents for aggregate sibling frames

    F = sum_e E_e.

Those data cannot determine the canonical component algebra, even if the
entire aggregate frame matrix is known exactly.

Fix ``d>=2``.  Let ``P_i`` be the computational rank-one projections on
``C^d`` and ``Q_j`` the Fourier-basis projections.  Compare two ``2d``-leaf
projection frames:

    commuting:     P_1,...,P_d,P_1,...,P_d,
    noncommuting:  P_1,...,P_d,Q_1,...,Q_d.                (1)

Both have exactly the same aggregate frame

    F = 2 I.                                               (2)

They therefore have identical support, condition number, spectrum, every
normalized moment, every resolvent, every polynomial/Borel function of ``F``,
and every joint aggregate word if used as one side of an otherwise identical
sibling pair.  Their full-support canonical effects are simply ``H_e=E_e/2``.

The first family commutes.  In the second, mutually unbiased overlaps give

    P_i Q_j P_i = P_i/d,      Q_j P_i Q_j = Q_j/d.

Summing the exact commutator squares over all cross-basis pairs yields

    D_com = (1-1/d) I / 8,                                 (3)
    Tr(D_com)/d = (1-1/d)/8 -> 1/8.                        (4)

Thus aggregate-frame data of *all* orders are compatible with either zero or
constant component commutator mass.  Existing sibling-frame degree-four
freeness, growing-word control, or even an exact aggregate resolvent cannot
settle the compressed component ``M_4`` gate without leaf-resolved incidence.

The natural target must retain the individual orientation blocks through the
normalization.  Sufficient data would include leaf-resolved Green-function
words such as

    Tr(E_e R E_f R E_e R E_f R),

where ``R`` contains the child pseudoinverse and sibling-common projection,
or an equivalent representation-theoretic recoupling formula.  Aggregate
moments alone are categorically insufficient.

This is a generic linear-algebra no-go, not a natural wreath commutativity or
noncommutativity theorem.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_commutator_trace_mass_bridge import (
    audit_component_commutator_trace,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_aggregate_frame_indeterminacy.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AggregateFrameIndeterminacyControl:
    dimension: int
    outcome_count: int
    leaf_rank: int
    commuting_frame_residual_from_two_identity: float
    noncommuting_frame_residual_from_two_identity: float
    aggregate_frame_difference_norm: float
    maximum_moment_difference_through_degree: int
    maximum_normalized_aggregate_moment_residual: float
    maximum_resolvent_residual: float
    commuting_normalized_commutator_trace: float
    noncommuting_normalized_commutator_trace: float
    predicted_noncommuting_normalized_commutator_trace: float
    noncommuting_commutator_defect_minimum_eigenvalue: float
    noncommuting_commutator_defect_maximum_eigenvalue: float
    mutually_unbiased_overlap_residual: float
    exact_all_order_aggregate_indeterminacy_verified: bool
    status: str


@dataclass(frozen=True)
class AggregateFrameIndeterminacyScalingRecord:
    dimension: int
    outcome_count: int
    aggregate_frame_condition_number: float
    commuting_normalized_commutator_trace: float
    noncommuting_normalized_commutator_trace: float
    limiting_noncommuting_normalized_commutator_trace: float
    identical_all_order_aggregate_frame_data: bool
    natural_leaf_resolved_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class ComponentAggregateFrameIndeterminacyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[AggregateFrameIndeterminacyControl]
    scaling_records: list[AggregateFrameIndeterminacyScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def computational_and_fourier_projectors(
    dimension: int,
) -> tuple[tuple[np.ndarray, ...], tuple[np.ndarray, ...]]:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    computational = tuple(
        np.outer(vector, vector.conj())
        for vector in np.eye(dimension, dtype=complex).T
    )
    root = np.exp(2j * np.pi / dimension)
    fourier_matrix = np.asarray(
        [
            [root ** (row * column) / math.sqrt(dimension) for column in range(dimension)]
            for row in range(dimension)
        ],
        dtype=complex,
    )
    fourier = tuple(
        np.outer(vector, vector.conj()) for vector in fourier_matrix.T
    )
    return computational, fourier


def aggregate_indeterminacy_projection_frames(
    dimension: int,
) -> tuple[tuple[np.ndarray, ...], tuple[np.ndarray, ...]]:
    computational, fourier = computational_and_fourier_projectors(dimension)
    return (
        (*computational, *computational),
        (*computational, *fourier),
    )


def audit_aggregate_frame_indeterminacy(
    dimension: int,
    *,
    highest_moment_degree: int = 8,
    tolerance: float = 1e-9,
) -> AggregateFrameIndeterminacyControl:
    if highest_moment_degree < 1:
        raise ValueError("at least one aggregate moment is required")
    commuting_leaves, noncommuting_leaves = (
        aggregate_indeterminacy_projection_frames(dimension)
    )
    identity = np.eye(dimension, dtype=complex)
    commuting_frame = sum(commuting_leaves, np.zeros_like(identity))
    noncommuting_frame = sum(noncommuting_leaves, np.zeros_like(identity))
    target_frame = 2 * identity
    commuting_frame_residual = float(
        np.linalg.norm(commuting_frame - target_frame, ord=2)
    )
    noncommuting_frame_residual = float(
        np.linalg.norm(noncommuting_frame - target_frame, ord=2)
    )
    frame_difference = float(
        np.linalg.norm(commuting_frame - noncommuting_frame, ord=2)
    )

    moment_residual = 0.0
    commuting_power = identity.copy()
    noncommuting_power = identity.copy()
    for _ in range(highest_moment_degree):
        commuting_power = commuting_power @ commuting_frame
        noncommuting_power = noncommuting_power @ noncommuting_frame
        moment_residual = max(
            moment_residual,
            abs(
                float(np.trace(commuting_power).real / dimension)
                - float(np.trace(noncommuting_power).real / dimension)
            ),
        )
    resolvent_residual = 0.0
    for spectral_parameter in (0.1, 0.5, 1.0, 3.0, 10.0):
        left = np.linalg.inv(commuting_frame + spectral_parameter * identity)
        right = np.linalg.inv(noncommuting_frame + spectral_parameter * identity)
        resolvent_residual = max(
            resolvent_residual,
            float(np.linalg.norm(left - right, ord=2)),
        )

    commuting_effects = tuple(leaf / 2 for leaf in commuting_leaves)
    noncommuting_effects = tuple(leaf / 2 for leaf in noncommuting_leaves)
    commuting = audit_component_commutator_trace(
        f"COMMUTING-D{dimension}",
        commuting_effects,
        tolerance=tolerance,
    )
    noncommuting = audit_component_commutator_trace(
        f"MUB-D{dimension}",
        noncommuting_effects,
        tolerance=tolerance,
    )
    noncommuting_defect = np.zeros_like(identity)
    for left_index, left in enumerate(noncommuting_effects):
        for right in noncommuting_effects[left_index + 1 :]:
            commutator = left @ right - right @ left
            noncommuting_defect += commutator.conj().T @ commutator
    defect_values = np.linalg.eigvalsh(
        (noncommuting_defect + noncommuting_defect.conj().T) / 2
    )
    computational, fourier = computational_and_fourier_projectors(dimension)
    overlap_residual = max(
        abs(float(np.trace(left @ right).real) - 1.0 / dimension)
        for left in computational
        for right in fourier
    )
    predicted = (1.0 - 1.0 / dimension) / 8.0
    exact = bool(
        max(
            commuting_frame_residual,
            noncommuting_frame_residual,
            frame_difference,
            moment_residual,
            resolvent_residual,
            overlap_residual,
            abs(commuting.normalized_commutator_trace),
            abs(noncommuting.normalized_commutator_trace - predicted),
            abs(float(defect_values[0]) - predicted),
            abs(float(defect_values[-1]) - predicted),
        )
        <= 1000 * tolerance
        and commuting.effects_pairwise_commute
        and not noncommuting.effects_pairwise_commute
    )
    return AggregateFrameIndeterminacyControl(
        dimension=dimension,
        outcome_count=2 * dimension,
        leaf_rank=1,
        commuting_frame_residual_from_two_identity=commuting_frame_residual,
        noncommuting_frame_residual_from_two_identity=noncommuting_frame_residual,
        aggregate_frame_difference_norm=frame_difference,
        maximum_moment_difference_through_degree=highest_moment_degree,
        maximum_normalized_aggregate_moment_residual=moment_residual,
        maximum_resolvent_residual=resolvent_residual,
        commuting_normalized_commutator_trace=commuting.normalized_commutator_trace,
        noncommuting_normalized_commutator_trace=noncommuting.normalized_commutator_trace,
        predicted_noncommuting_normalized_commutator_trace=predicted,
        noncommuting_commutator_defect_minimum_eigenvalue=float(defect_values[0]),
        noncommuting_commutator_defect_maximum_eigenvalue=(
            noncommuting.commutator_defect_maximum_eigenvalue
        ),
        mutually_unbiased_overlap_residual=overlap_residual,
        exact_all_order_aggregate_indeterminacy_verified=exact,
        status=(
            "identical-aggregate-frame-zero-versus-constant-component-gap-verified"
            if exact
            else "aggregate-frame-indeterminacy-control-failure"
        ),
    )


def aggregate_frame_indeterminacy_scaling_record(
    dimension: int,
) -> AggregateFrameIndeterminacyScalingRecord:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    return AggregateFrameIndeterminacyScalingRecord(
        dimension=dimension,
        outcome_count=2 * dimension,
        aggregate_frame_condition_number=1.0,
        commuting_normalized_commutator_trace=0.0,
        noncommuting_normalized_commutator_trace=(1 - 1 / dimension) / 8,
        limiting_noncommuting_normalized_commutator_trace=1 / 8,
        identical_all_order_aggregate_frame_data=True,
        natural_leaf_resolved_transfer_proved=False,
        status="all-order-aggregate-data-cannot-determine-component-M4",
    )


def run_component_aggregate_frame_indeterminacy(
) -> ComponentAggregateFrameIndeterminacyReport:
    controls = [audit_aggregate_frame_indeterminacy(dimension) for dimension in (2, 3, 4, 5, 8)]
    failures = sum(
        not row.exact_all_order_aggregate_indeterminacy_verified for row in controls
    )
    exact = failures == 0
    scaling = [
        aggregate_frame_indeterminacy_scaling_record(dimension)
        for dimension in (2, 3, 4, 5, 8, 16, 32, 64, 128, 256)
    ]
    tail = scaling[-1]
    return ComponentAggregateFrameIndeterminacyReport(
        created_at=utc_now(),
        theorem_contract={
            "identical_aggregate_frames": (
                "Two copies of the computational basis and the union of the "
                "computational/Fourier bases both sum to 2I, so every aggregate "
                "moment, resolvent, support, edge, and Borel functional agrees."
            ),
            "different_component_algebras": (
                "After canonical scaling by 1/2, the repeated basis commutes "
                "while the mutually unbiased pair has "
                "D_com=(1-1/d)I/8."
            ),
            "all_order_boundary": (
                "Even exact aggregate frame knowledge of all orders cannot "
                "determine component M_4; leaf-resolved normalized incidence is required."
            ),
            "scope": (
                "This is a generic projection-frame no-go and not a natural "
                "wreath component-algebra theorem."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "test_whether_aggregate_sibling_moments_can_determine_component_M4",
                "resolved": exact,
                "resolution": "Refuted at every d>=2 by exactly equal aggregate frames with zero versus (1-1/d)/8 normalized commutator gap."
            },
            {
                "obligation": "identify_minimum_missing_natural_data",
                "resolved": exact,
                "resolution": "Retain leaf labels through child Green/pseudoinverse and sibling-common compression; aggregate words alone are insufficient."
            },
            {
                "obligation": "derive_natural_leaf_resolved_compressed_fourth_moment",
                "resolved": False,
                "resolution": "Need regular-master traces of leaf-resolved Green-function words or an equivalent recoupling formula."
            },
            {
                "obligation": "prove_positive_natural_component_M4",
                "resolved": False,
                "resolution": "Neither identical aggregate data nor the Haar benchmark decides the natural crossing gap."
            },
        ],
        adversarial_audit=[
            {
                "objection": "A growing-word or exact aggregate resolvent theorem would settle component noncommutativity.",
                "resolved": True,
                "resolution": "False. Both families have the same aggregate matrix 2I itself, not merely matching finitely many moments."
            },
            {
                "objection": "The difference disappears in high dimension.",
                "resolved": True,
                "resolution": "The noncommuting normalized gap tends to 1/8 while the commuting gap remains zero."
            },
            {
                "objection": "The generic counterfamily proves natural aggregate moments are useless for every purpose.",
                "resolved": False,
                "resolution": "They remain useful for dimensions and conditioning, but cannot determine leaf-resolved component algebra without extra structure."
            },
        ],
        headline_metrics={
            "aggregate_frame_all_order_indeterminacy_theorem_count": int(exact),
            "mutually_unbiased_constant_component_gap_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "tail_dimension": tail.dimension,
            "tail_noncommuting_normalized_gap": tail.noncommuting_normalized_commutator_trace,
            "limiting_noncommuting_normalized_gap": tail.limiting_noncommuting_normalized_commutator_trace,
            "natural_leaf_resolved_compressed_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "aggregate_sibling_frame_data_determine_component_M4": False,
            "all_order_aggregate_indeterminacy_proved": exact,
            "leaf_resolved_green_function_moments_required": exact,
            "natural_compressed_component_M4_positive": False,
            "natural_noncommutative_component_physical_mass_proved": False,
            "coherent_component_algebra_compiler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact aggregate frames can hide either commuting or constant-"
                "gap component algebras. Natural progress requires leaf-resolved "
                "pseudoinverse/common-span moments."
            ),
        },
        status=(
            "aggregate-frame-route-falsified-leaf-resolved-green-moments-required"
            if exact
            else "aggregate-frame-indeterminacy-control-failure"
        ),
        summary=(
            "Proved that identical aggregate frames of all orders can have zero "
            "or asymptotically constant component commutator mass."
        ),
        falsifiers_triggered=[
            "Uncompressed sibling-frame degree-four freeness cannot determine compressed component M_4.",
            "Even an exact aggregate resolvent cannot determine the component algebra.",
            "The missing theorem must retain individual orientation leaves through normalization and common-span compression.",
            "The mutually unbiased constant is a generic counterexample, not natural wreath evidence.",
        ],
    )


def write_component_aggregate_frame_indeterminacy_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_aggregate_frame_indeterminacy())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_component_aggregate_frame_indeterminacy_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
