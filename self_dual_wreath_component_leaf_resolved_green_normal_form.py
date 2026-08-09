"""Leaf-resolved Green-function normal form for compressed component M4.

Aggregate child-frame moments cannot determine component commutator mass.  The
missing natural quantity has an exact leaf-resolved ambient-space form.

Let ``E_e`` be one child's orientation projections,

    F = sum_e E_e,

and let ``X:C^r -> H`` be an isometry for the sibling common span inside
``Ran(F)``.  Put

    B = X^* F^+ X,
    Y = F^+ X B^{-1/2},
    K = Y Y^* = F^+ X B^{-1} X^* F^+.                    (1)

The canonical component effects are ``H_e=Y^*E_eY``.  The kernel ``K`` obeys

    K F K = K,                                             (2)

and ``F^{1/2} K F^{1/2}`` is an orthogonal projection.  For every leaf word,

    Tr(H_e1 ... H_em)
      = Tr(E_e1 K E_e2 K ... E_em K).                      (3)

Consequently the exact commutator fourth-moment gap is

    Tr(D_com) = sum_(e,f) [
        Tr(E_e K E_e K E_f K E_f K)
        - Tr(E_e K E_f K E_e K E_f K)].                   (4)

Equation (4), not an aggregate word in ``F``, is the natural target.

At the final root let ``q`` be the child leaf count, ``g=|G|``, and normalize
the subgroup-projection walk by

    A = (g/q) F.

Its nonzero spectrum is on the natural order-one scale.  If
``C=X^*A^+X``, then

    K = (g/q) A^+ X C^{-1} X^* A^+.                       (5)

The pseudoinverse is a Green operator,

    A^+ = integral_0^infinity exp(-tA) supp(A) dt,          (6)

or the strong limit ``A(A+eta I)^{-2}`` as ``eta->0+``.
The powers/heat kernel in (6) are return operators of the explicit one-common-
multiplier subgroup walk.  Equations (4)-(6) therefore reduce natural
component noncommutativity to leaf-marked multi-return Green correlations plus
the sibling common-span insertion.

The regular-master source decomposition is preserved by every operation in
(1).  Taking normalized regular trace of (4) is exactly the independent-
Plancherel physically normalized ``M_4`` from the trace-mass bridge.  Global-
distinct conditioning must still be transferred separately.

This module is a normal form, not a positive-moment theorem.  It proves why
existing aggregate sibling words are insufficient and specifies the smallest
new representation-theoretic object: a leaf-marked four-word Green kernel.
No convergence, edge, compiler, or speedup follows from the identity alone.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_leaf_resolved_green_normal_form.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class LeafResolvedGreenControl:
    control_id: str
    ambient_dimension: int
    common_fiber_dimension: int
    leaf_count: int
    child_frame_rank: int
    child_frame_minimum_positive_eigenvalue: float
    child_frame_maximum_eigenvalue: float
    component_effect_sum_residual: float
    green_reflexive_inverse_residual: float
    whitened_green_projection_residual: float
    maximum_leaf_word_trace_residual_through_degree: int
    maximum_leaf_word_trace_residual: float
    direct_component_commutator_trace: float
    leaf_resolved_green_commutator_trace: float
    commutator_trace_residual: float
    regularized_pseudoinverse_residual: float
    exact_green_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class GreenScalingRecord:
    group_order_to_child_leaf_ratio: float
    child_leaf_count_decimal: str
    group_order_decimal: str
    normalized_walk_scale: float
    green_prefactor: float
    leaf_resolved_fourth_word_required: bool
    aggregate_frame_words_sufficient: bool
    natural_green_moment_bound_proved: bool
    status: str


@dataclass(frozen=True)
class ComponentLeafResolvedGreenNormalFormReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[LeafResolvedGreenControl]
    scaling_records: list[GreenScalingRecord]
    regular_master_reduction: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def component_green_kernel(
    leaves: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, tuple[np.ndarray, ...]]:
    """Return frame ``F``, Green kernel ``K``, and canonical effects."""

    if not leaves:
        raise ValueError("at least one leaf projection is required")
    ambient = leaves[0].shape[0]
    if ambient < 1 or any(leaf.shape != (ambient, ambient) for leaf in leaves):
        raise ValueError("leaves must share one positive square ambient space")
    if common_isometry.ndim != 2 or common_isometry.shape[0] != ambient:
        raise ValueError("common isometry has the wrong ambient dimension")
    frame = sum(leaves, np.zeros((ambient, ambient), dtype=complex))
    frame_inverse = _psd_power(frame, -1.0, tolerance=tolerance)
    metric = common_isometry.conj().T @ frame_inverse @ common_isometry
    metric_inverse = _psd_power(metric, -1.0, tolerance=tolerance)
    metric_inverse_root = _psd_power(metric, -0.5, tolerance=tolerance)
    synthesis = frame_inverse @ common_isometry @ metric_inverse_root
    green = (
        frame_inverse
        @ common_isometry
        @ metric_inverse
        @ common_isometry.conj().T
        @ frame_inverse
    )
    effects = tuple(
        synthesis.conj().T @ leaf @ synthesis for leaf in leaves
    )
    return frame, green, effects


def leaf_resolved_commutator_trace(
    leaves: tuple[np.ndarray, ...],
    green: np.ndarray,
) -> float:
    noncrossing = 0.0
    crossing = 0.0
    for left in leaves:
        for right in leaves:
            noncrossing += float(
                np.trace(
                    left @ green @ left @ green @ right @ green @ right @ green
                ).real
            )
            crossing += float(
                np.trace(
                    left @ green @ right @ green @ left @ green @ right @ green
                ).real
            )
    return noncrossing - crossing


def _direct_commutator_trace(effects: tuple[np.ndarray, ...]) -> float:
    output = 0.0
    for left_index, left in enumerate(effects):
        for right in effects[left_index + 1 :]:
            commutator = left @ right - right @ left
            output += float(np.trace(commutator.conj().T @ commutator).real)
    return output


def _maximum_word_trace_residual(
    leaves: tuple[np.ndarray, ...],
    green: np.ndarray,
    effects: tuple[np.ndarray, ...],
    highest_degree: int,
) -> float:
    maximum = 0.0
    leaf_count = len(leaves)
    # Complete words are exponential. The finite controls use at most four
    # leaves and degree four, which is exactly the commutator target.
    for degree in range(1, highest_degree + 1):
        for word_index in range(leaf_count**degree):
            word = []
            value = word_index
            for _ in range(degree):
                word.append(value % leaf_count)
                value //= leaf_count
            direct = np.eye(effects[0].shape[0], dtype=complex)
            ambient = np.eye(green.shape[0], dtype=complex)
            for index in word:
                direct = direct @ effects[index]
                ambient = ambient @ leaves[index] @ green
            maximum = max(
                maximum,
                abs(float(np.trace(direct).real) - float(np.trace(ambient).real)),
            )
    return maximum


def audit_leaf_resolved_green_normal_form(
    control_id: str,
    leaves: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    highest_word_degree: int = 4,
    regularization: float = 1e-7,
    tolerance: float = 1e-9,
) -> LeafResolvedGreenControl:
    frame, green, effects = component_green_kernel(
        leaves,
        common_isometry,
        tolerance=tolerance,
    )
    ambient = frame.shape[0]
    fiber = common_isometry.shape[1]
    identity = np.eye(fiber, dtype=complex)
    frame_values = np.linalg.eigvalsh((frame + frame.conj().T) / 2.0)
    positive = frame_values[frame_values > 100 * tolerance]
    effect_sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    reflexive = float(np.linalg.norm(green @ frame @ green - green, ord=2))
    frame_root = _psd_power(frame, 0.5, tolerance=tolerance)
    whitened = frame_root @ green @ frame_root
    projection = float(
        np.linalg.norm(whitened @ whitened - whitened, ord=2)
    )
    word_residual = _maximum_word_trace_residual(
        leaves,
        green,
        effects,
        highest_word_degree,
    )
    direct = _direct_commutator_trace(effects)
    resolved = leaf_resolved_commutator_trace(leaves, green)
    commutator_residual = abs(direct - resolved)

    frame_inverse = _psd_power(frame, -1.0, tolerance=tolerance)
    regularized = frame @ np.linalg.inv(
        frame + regularization * np.eye(ambient)
    ) @ np.linalg.inv(frame + regularization * np.eye(ambient))
    regularized_residual = float(np.linalg.norm(regularized - frame_inverse, ord=2))
    exact = bool(
        max(
            effect_sum_residual,
            reflexive,
            projection,
            word_residual,
            commutator_residual,
        )
        <= 1000 * tolerance
        and regularized_residual <= 10 * regularization / positive[0] ** 2
    )
    return LeafResolvedGreenControl(
        control_id=control_id,
        ambient_dimension=ambient,
        common_fiber_dimension=fiber,
        leaf_count=len(leaves),
        child_frame_rank=len(positive),
        child_frame_minimum_positive_eigenvalue=float(positive[0]),
        child_frame_maximum_eigenvalue=float(positive[-1]),
        component_effect_sum_residual=effect_sum_residual,
        green_reflexive_inverse_residual=reflexive,
        whitened_green_projection_residual=projection,
        maximum_leaf_word_trace_residual_through_degree=highest_word_degree,
        maximum_leaf_word_trace_residual=word_residual,
        direct_component_commutator_trace=direct,
        leaf_resolved_green_commutator_trace=resolved,
        commutator_trace_residual=commutator_residual,
        regularized_pseudoinverse_residual=regularized_residual,
        exact_green_normal_form_verified=exact,
        status=(
            "exact-leaf-resolved-green-component-M4-normal-form"
            if exact
            else "leaf-resolved-green-normal-form-control-failure"
        ),
    )


def green_scaling_record(group_order: int, child_leaf_count: int) -> GreenScalingRecord:
    if group_order < 2 or child_leaf_count < 2:
        raise ValueError("group order and child leaf count must be at least two")
    prefactor = group_order / child_leaf_count
    return GreenScalingRecord(
        group_order_to_child_leaf_ratio=prefactor,
        child_leaf_count_decimal=str(child_leaf_count),
        group_order_decimal=str(group_order),
        normalized_walk_scale=prefactor,
        green_prefactor=prefactor,
        leaf_resolved_fourth_word_required=True,
        aggregate_frame_words_sufficient=False,
        natural_green_moment_bound_proved=False,
        status="natural-leaf-resolved-green-correlation-open",
    )


def _trine_projection_frame() -> tuple[np.ndarray, ...]:
    leaves = []
    for angle in (0.0, 2 * math.pi / 3, 4 * math.pi / 3):
        vector = np.asarray(
            [[1.0], [complex(math.cos(angle), math.sin(angle))]],
            dtype=complex,
        ) / math.sqrt(2)
        leaves.append(vector @ vector.conj().T)
    return tuple(leaves)


def _mub_projection_frame(dimension: int = 3) -> tuple[np.ndarray, ...]:
    computational = tuple(
        np.outer(vector, vector.conj())
        for vector in np.eye(dimension, dtype=complex).T
    )
    root = np.exp(2j * np.pi / dimension)
    fourier = np.asarray(
        [
            [root ** (row * column) / math.sqrt(dimension) for column in range(dimension)]
            for row in range(dimension)
        ],
        dtype=complex,
    )
    return (*computational, *(np.outer(v, v.conj()) for v in fourier.T))


def run_component_leaf_resolved_green_normal_form(
) -> ComponentLeafResolvedGreenNormalFormReport:
    controls = [
        audit_leaf_resolved_green_normal_form(
            "TRINE-FULL-COMMON",
            _trine_projection_frame(),
            np.eye(2, dtype=complex),
        ),
        audit_leaf_resolved_green_normal_form(
            "MUB-D3-FULL-COMMON",
            _mub_projection_frame(3),
            np.eye(3, dtype=complex),
        ),
    ]
    failures = sum(not row.exact_green_normal_form_verified for row in controls)
    exact = failures == 0
    scaling = []
    for n in (8, 12, 16, 24, 32, 48, 64, 96):
        group_order = math.factorial(n)
        threshold = (group_order - 1).bit_length()
        child_leaves = 1 << (threshold + 1)
        scaling.append(green_scaling_record(group_order, child_leaves))
    return ComponentLeafResolvedGreenNormalFormReport(
        created_at=utc_now(),
        theorem_contract={
            "green_kernel": (
                "K=F^+X(X^*F^+X)^-1X^*F^+ obeys KFK=K and has "
                "F^(1/2)KF^(1/2) equal to a projection."
            ),
            "leaf_word_identity": (
                "Every component word trace equals the ambient leaf-resolved "
                "word with K inserted after every leaf."
            ),
            "commutator_word": (
                "Tr(D_com) is exactly the sum of AABB-minus-ABAB leaf-resolved "
                "four-words in equation (4)."
            ),
            "regular_master_green_walk": (
                "With A=(g/q)F, K=(g/q)A^+X(X^*A^+X)^-1X^*A^+. "
                "A^+ is the Green operator of the one-common-multiplier subgroup walk."
            ),
            "scope": (
                "This is an exact normal form. No natural Green correlation "
                "bound, globally distinct transfer, compiler, or speedup is proved."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        regular_master_reduction={
            "independent_plancherel_M4": (
                "normalized regular trace of sum_(e,f)(E_e K E_e K E_f K E_f K-E_e K E_f K E_e K E_f K)"
            ),
            "globally_distinct_conditioning_transferred": False,
            "aggregate_sibling_word_moments_sufficient": False,
            "leaf_marked_green_return_bound_proved": False,
            "natural_M4_lower_bound_proved": False,
        },
        proof_obligations=[
            {
                "obligation": "derive_exact_leaf_resolved_ambient_normal_form_for_component_M4",
                "resolved": exact,
                "resolution": "Equations (1)-(4) follow by cyclic trace contraction of Y^*E_eY and pass complete degree-four controls."
            },
            {
                "obligation": "identify_the_regular_master_random_walk_quantity",
                "resolved": exact,
                "resolution": "After natural scaling A=(g/q)F, the inserted kernel is a sibling-compressed Green operator of the subgroup-projection walk."
            },
            {
                "obligation": "bound_natural_leaf_marked_green_AABB_minus_ABAB",
                "resolved": False,
                "resolution": "Need representation-theoretic multi-return estimates that retain orientation labels and the sibling common projection."
            },
            {
                "obligation": "transfer_independent_plancherel_green_gap_to_global_distinct_sources",
                "resolved": False,
                "resolution": "A positive independent-source result must have a quantitative error stable under collision-free conditioning."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Aggregate subgroup-walk return probabilities determine component M4.",
                "resolved": True,
                "resolution": "False without leaf marks; identical aggregate frames can have zero or constant component gap."
            },
            {
                "objection": "The pseudoinverse can be omitted because the child frame is well conditioned on average.",
                "resolved": False,
                "resolution": "The exact effects contain K. No natural edge or state-weighted replacement has justified removing it."
            },
            {
                "objection": "The Green normal form itself proves a positive gap.",
                "resolved": False,
                "resolution": "It only identifies the signed AABB-minus-ABAB correlation whose positivity remains open."
            },
        ],
        headline_metrics={
            "leaf_resolved_green_word_normal_form_theorem_count": int(exact),
            "component_M4_green_AABB_minus_ABAB_identity_theorem_count": int(exact),
            "regular_master_subgroup_walk_green_reduction_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "natural_leaf_marked_green_gap_theorem_count": 0,
            "natural_compressed_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "leaf_resolved_green_normal_form_proved": exact,
            "aggregate_sibling_words_suffice_for_component_M4": False,
            "natural_leaf_marked_green_gap_positive": False,
            "global_distinct_green_gap_transfer_proved": False,
            "natural_noncommutative_component_physical_mass_proved": False,
            "coherent_green_or_component_compiler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact missing Green correlation is now explicit, but no "
                "natural lower bound or coherent implementation is known."
            ),
        },
        status=(
            "exact-leaf-resolved-green-target-derived-natural-gap-open"
            if exact
            else "leaf-resolved-green-normal-form-control-failure"
        ),
        summary=(
            "Derived the exact leaf-marked Green-function trace word whose "
            "natural AABB-minus-ABAB gap would prove component noncommutative mass."
        ),
        falsifiers_triggered=[
            "Aggregate frame moments and resolvents omit the leaf labels required by component M4.",
            "The sibling common projection and child pseudoinverse remain inside the exact Green kernel.",
            "A positive Haar gap does not evaluate the natural leaf-marked Green word.",
            "No natural gap, globally distinct transfer, compiler, decoder, or speedup is proved.",
        ],
    )


def write_component_leaf_resolved_green_normal_form_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_leaf_resolved_green_normal_form())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM."
                ),
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
                    "self_dual_wreath_component_leaf_resolved_green_normal_form": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_component_leaf_resolved_green_normal_form_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
