"""Exact obstruction to transferring leaf commutators through whitening.

Let ``E_1,...,E_q`` be orthogonal projections whose frame operator

    F = sum_e E_e

is positive definite on their common span.  The canonical component effects
are

    H_e = F^{-1/2} E_e F^{-1/2},        sum_e H_e = I.       (1)

The natural-leaf theorem proves that almost every balanced pair of the
unwhitened ``E_e`` has an inverse-polynomial commutator.  This module proves
that neither that fact, bounded conditioning of ``F``, small leaf rank,
constant total-rank aspect, nor full-rank nonscalarity can force the effects
in (1) to be noncommutative.

There is also an exact structural criterion.  If the ``H_e`` commute, choose
their common eigenbasis and write ``H_e=diag(h_ei)``.  Since ``E_e`` is a
projection,

    H_e F H_e = H_e.                                      (2)

Consequently, every positive ``h_ei`` equals ``1/F_ii``; ``F_ii`` is the
positive integer counting effects supported on coordinate ``i``; and the
support of every effect is an independent set in the graph of nonzero
off-diagonal entries of ``F``.  Conversely, every such integer-degree
independent-set cover produces a projection frame with commuting canonical
effects.  In particular, a commuting full-support canonical effect can have
only reciprocal-integer nonzero eigenvalues.  A non-reciprocal eigenvalue is
therefore an exact noncommutativity witness only in this full-support setting.
The sibling common-span compression used by the actual final-root effects
removes this rigidity: the companion universality no-go realizes every POVM.

The counterfamily below is stronger than a repeated rank-one basis.  It has
distinct rank-``b`` leaves.  Put ``r=sp`` coordinates into ``s`` parts of size
``p`` and set

    F = b I + (b/r) A,

where ``A`` is one between different parts and zero within a part.  In every
part use the ``p`` cyclic intervals of length ``b`` as effect supports, with
``H_e=(1/b) P_e``.  Every coordinate occurs in exactly ``b`` supports, while
each support is independent in the nonzero graph of ``F``.  Thus
``E_e=F^{1/2}H_eF^{1/2}`` are distinct rank-``b`` projections and their
canonical effects commute.

For leaves in different parts, all nonzero principal correlations collapse to
one value ``b/r``, so

    ||[E_e,E_f]|| = (b/r) sqrt(1-(b/r)^2).                 (3)

The cross-part pair fraction tends to one as ``s`` grows.  Nevertheless,
``cond(F)=(2-1/s)/(1-1/s)<3`` and

    sum_e (H_e-Tr(H_e)I/r)^2 = (1/b-1/r) I.               (4)

Hence even density-one inverse-polynomial leaf noncommutativity, a uniformly
conditioned frame, constant component aspect, vanishing relative leaf rank,
distinct leaves, and a constant nonscalarity edge can whiten to a completely
commutative POVM.  The natural wreath problem now needs a direct theorem for
the compressed component commutator or a representation-specific simultaneous
eigenbasis; generic conditioning and full-support spectral arithmetic cannot
close the gate.
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
    "self_dual_wreath_leaf_whitening_commutator_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CommutingWhiteningControl:
    control_id: str
    part_count: int
    part_size: int
    leaf_rank: int
    fiber_dimension: int
    outcome_count: int
    total_leaf_rank: int
    total_rank_aspect: float
    relative_leaf_rank: float
    frame_minimum_eigenvalue: float
    frame_maximum_eigenvalue: float
    predicted_frame_condition_number: float
    observed_frame_condition_number: float
    cross_part_pair_fraction: float
    predicted_cross_leaf_principal_cosine: float
    observed_cross_leaf_principal_cosine: float
    predicted_cross_leaf_commutator_norm: float
    observed_cross_leaf_commutator_norm: float
    predicted_nonscalarity_defect_edge: float
    observed_nonscalarity_defect_edge: float
    maximum_leaf_idempotence_residual: float
    frame_reconstruction_residual: float
    canonical_whitening_residual: float
    canonical_effect_sum_residual: float
    maximum_canonical_effect_commutator_norm: float
    distinct_leaf_projectors: bool
    reciprocal_integer_effect_spectrum_verified: bool
    exact_counterfamily_verified: bool
    status: str


@dataclass(frozen=True)
class CommutingWhiteningScalingRecord:
    part_count: int
    part_size: int
    leaf_rank: int
    fiber_dimension: int
    outcome_count: int
    total_leaf_rank: int
    total_rank_aspect: float
    relative_leaf_rank: float
    frame_condition_number: float
    cross_part_pair_fraction: float
    cross_leaf_commutator_norm: float
    inverse_cross_leaf_commutator_scale: float
    nonscalarity_defect_edge: float
    leaves_pairwise_distinct: bool
    density_one_leaf_noncommutativity: bool
    canonical_effects_pairwise_commute: bool
    status: str


@dataclass(frozen=True)
class LeafWhiteningCommutatorNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CommutingWhiteningControl]
    scaling_records: list[CommutingWhiteningScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_parameters(part_count: int, part_size: int, leaf_rank: int) -> None:
    if part_count < 2:
        raise ValueError("at least two parts are required")
    if part_size < 3:
        raise ValueError("part size must be at least three")
    if not 1 < leaf_rank < part_size:
        raise ValueError("leaf rank must lie strictly between one and part size")


def _cyclic_supports(
    part_count: int,
    part_size: int,
    leaf_rank: int,
) -> tuple[tuple[int, ...], ...]:
    supports: list[tuple[int, ...]] = []
    for part in range(part_count):
        offset = part * part_size
        for start in range(part_size):
            supports.append(
                tuple(
                    offset + ((start + step) % part_size)
                    for step in range(leaf_rank)
                )
            )
    return tuple(supports)


def construct_commuting_whitening_counterfamily(
    part_count: int,
    part_size: int,
    leaf_rank: int,
) -> tuple[np.ndarray, tuple[np.ndarray, ...], tuple[np.ndarray, ...], tuple[tuple[int, ...], ...]]:
    """Construct ``F``, commuting ``H_e``, projection leaves ``E_e``, supports."""

    _validate_parameters(part_count, part_size, leaf_rank)
    dimension = part_count * part_size
    frame = leaf_rank * np.eye(dimension, dtype=float)
    cross_entry = leaf_rank / dimension
    for left in range(dimension):
        left_part = left // part_size
        for right in range(dimension):
            if left_part != right // part_size:
                frame[left, right] = cross_entry

    values, vectors = np.linalg.eigh(frame)
    if values[0] <= 0:
        raise AssertionError("counterfamily frame must be positive definite")
    frame_sqrt = (vectors * np.sqrt(values)) @ vectors.T

    supports = _cyclic_supports(part_count, part_size, leaf_rank)
    effects: list[np.ndarray] = []
    leaves: list[np.ndarray] = []
    for support in supports:
        effect = np.zeros((dimension, dimension), dtype=float)
        effect[list(support), list(support)] = 1.0 / leaf_rank
        effects.append(effect)
        leaves.append(frame_sqrt @ effect @ frame_sqrt)
    return frame, tuple(effects), tuple(leaves), supports


def verify_diagonal_commuting_projection_frame_certificate(
    frame: np.ndarray,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> dict[str, bool | float | int]:
    """Verify the exact independent-set certificate in a common eigenbasis."""

    if not effects or frame.ndim != 2 or frame.shape[0] != frame.shape[1]:
        raise ValueError("a square frame and at least one effect are required")
    dimension = frame.shape[0]
    if any(effect.shape != frame.shape for effect in effects):
        raise ValueError("all effects must match the frame dimension")

    diagonality = max(
        float(np.linalg.norm(effect - np.diag(np.diag(effect)), ord=2))
        for effect in effects
    )
    effect_sum = sum(effects, np.zeros_like(frame))
    sum_residual = float(np.linalg.norm(effect_sum - np.eye(dimension), ord=2))
    equation_residual = max(
        float(np.linalg.norm(effect @ frame @ effect - effect, ord=2))
        for effect in effects
    )

    frame_diagonal = np.diag(frame).real
    integer_diagonal_residual = float(
        np.max(np.abs(frame_diagonal - np.rint(frame_diagonal)))
    )
    incidence = np.zeros(dimension, dtype=int)
    reciprocal_residual = 0.0
    independent_set_residual = 0.0
    for effect in effects:
        diagonal = np.diag(effect).real
        support = np.flatnonzero(diagonal > 100 * tolerance)
        incidence[support] += 1
        if support.size:
            reciprocal_residual = max(
                reciprocal_residual,
                float(
                    np.max(
                        np.abs(
                            diagonal[support]
                            - 1.0 / frame_diagonal[support]
                        )
                    )
                ),
            )
            restricted = frame[np.ix_(support, support)].copy()
            restricted -= np.diag(np.diag(restricted))
            independent_set_residual = max(
                independent_set_residual,
                float(np.linalg.norm(restricted, ord=2)),
            )
    incidence_residual = int(
        np.max(np.abs(incidence - np.rint(frame_diagonal).astype(int)))
    )
    verified = bool(
        diagonality <= 100 * tolerance
        and sum_residual <= 100 * tolerance
        and equation_residual <= 1000 * tolerance
        and integer_diagonal_residual <= 100 * tolerance
        and reciprocal_residual <= 100 * tolerance
        and independent_set_residual <= 100 * tolerance
        and incidence_residual == 0
    )
    return {
        "effects_diagonal_residual": diagonality,
        "effect_sum_residual": sum_residual,
        "projection_equation_residual": equation_residual,
        "integer_frame_diagonal_residual": integer_diagonal_residual,
        "reciprocal_spectrum_residual": reciprocal_residual,
        "independent_set_residual": independent_set_residual,
        "incidence_residual": incidence_residual,
        "certificate_verified": verified,
    }


def _projection_commutator_norm(cosine: float) -> float:
    return cosine * math.sqrt(max(0.0, 1.0 - cosine * cosine))


def commuting_whitening_scaling_record(
    part_count: int,
    *,
    part_size: int = 5,
    leaf_rank: int = 2,
) -> CommutingWhiteningScalingRecord:
    _validate_parameters(part_count, part_size, leaf_rank)
    dimension = part_count * part_size
    outcome_count = dimension
    total_rank = outcome_count * leaf_rank
    cosine = leaf_rank / dimension
    condition = (2.0 - 1.0 / part_count) / (1.0 - 1.0 / part_count)
    pair_fraction = part_size * (part_count - 1) / (dimension - 1)
    commutator = _projection_commutator_norm(cosine)
    return CommutingWhiteningScalingRecord(
        part_count=part_count,
        part_size=part_size,
        leaf_rank=leaf_rank,
        fiber_dimension=dimension,
        outcome_count=outcome_count,
        total_leaf_rank=total_rank,
        total_rank_aspect=total_rank / dimension,
        relative_leaf_rank=leaf_rank / dimension,
        frame_condition_number=condition,
        cross_part_pair_fraction=pair_fraction,
        cross_leaf_commutator_norm=commutator,
        inverse_cross_leaf_commutator_scale=1.0 / commutator,
        nonscalarity_defect_edge=1.0 / leaf_rank - 1.0 / dimension,
        leaves_pairwise_distinct=True,
        density_one_leaf_noncommutativity=True,
        canonical_effects_pairwise_commute=True,
        status="density-one-noncommuting-distinct-leaves-whiten-to-commuting-effects",
    )


def audit_commuting_whitening_counterfamily(
    control_id: str,
    part_count: int,
    *,
    part_size: int = 5,
    leaf_rank: int = 2,
    tolerance: float = 1e-9,
) -> CommutingWhiteningControl:
    frame, effects, leaves, supports = construct_commuting_whitening_counterfamily(
        part_count,
        part_size,
        leaf_rank,
    )
    dimension = frame.shape[0]
    outcome_count = len(effects)
    values, vectors = np.linalg.eigh(frame)
    frame_inverse_sqrt = (vectors * (1.0 / np.sqrt(values))) @ vectors.T

    idempotence = max(
        float(np.linalg.norm(leaf @ leaf - leaf, ord=2)) for leaf in leaves
    )
    reconstruction = float(
        np.linalg.norm(sum(leaves, np.zeros_like(frame)) - frame, ord=2)
    )
    canonical = max(
        float(
            np.linalg.norm(
                frame_inverse_sqrt @ leaf @ frame_inverse_sqrt - effect,
                ord=2,
            )
        )
        for leaf, effect in zip(leaves, effects)
    )
    effect_sum = float(
        np.linalg.norm(
            sum(effects, np.zeros_like(frame)) - np.eye(dimension),
            ord=2,
        )
    )
    canonical_commutator = 0.0
    for left in effects:
        for right in effects:
            canonical_commutator = max(
                canonical_commutator,
                float(np.linalg.norm(left @ right - right @ left, ord=2)),
            )

    left_index = 0
    right_index = part_size
    left_support = supports[left_index]
    right_support = supports[right_index]
    left_basis = frame[:, list(left_support)]
    del left_basis  # The exact cross Gram is read directly from F below.
    cross_gram = frame[np.ix_(left_support, right_support)] / leaf_rank
    singular_values = np.linalg.svd(cross_gram, compute_uv=False)
    observed_cosine = float(singular_values[0])
    leaf_commutator = float(
        np.linalg.norm(
            leaves[left_index] @ leaves[right_index]
            - leaves[right_index] @ leaves[left_index],
            ord=2,
        )
    )

    identity = np.eye(dimension)
    nonscalarity = np.zeros_like(frame)
    for effect in effects:
        scalar = float(np.trace(effect).real / dimension)
        centered = effect - scalar * identity
        nonscalarity += centered @ centered
    nonscalarity_edge = float(np.linalg.eigvalsh(nonscalarity)[0])

    certificate = verify_diagonal_commuting_projection_frame_certificate(
        frame,
        effects,
        tolerance=tolerance,
    )
    distinct = len(set(supports)) == len(supports)
    expected_cosine = leaf_rank / dimension
    expected_commutator = _projection_commutator_norm(expected_cosine)
    expected_condition = (2.0 - 1.0 / part_count) / (
        1.0 - 1.0 / part_count
    )
    expected_nonscalarity = 1.0 / leaf_rank - 1.0 / dimension
    exact = bool(
        certificate["certificate_verified"]
        and distinct
        and idempotence <= 1000 * tolerance
        and reconstruction <= 1000 * tolerance
        and canonical <= 1000 * tolerance
        and effect_sum <= 100 * tolerance
        and canonical_commutator <= 100 * tolerance
        and abs(observed_cosine - expected_cosine) <= 100 * tolerance
        and abs(leaf_commutator - expected_commutator) <= 1000 * tolerance
        and abs(nonscalarity_edge - expected_nonscalarity) <= 1000 * tolerance
    )
    total_rank = outcome_count * leaf_rank
    return CommutingWhiteningControl(
        control_id=control_id,
        part_count=part_count,
        part_size=part_size,
        leaf_rank=leaf_rank,
        fiber_dimension=dimension,
        outcome_count=outcome_count,
        total_leaf_rank=total_rank,
        total_rank_aspect=total_rank / dimension,
        relative_leaf_rank=leaf_rank / dimension,
        frame_minimum_eigenvalue=float(values[0]),
        frame_maximum_eigenvalue=float(values[-1]),
        predicted_frame_condition_number=expected_condition,
        observed_frame_condition_number=float(values[-1] / values[0]),
        cross_part_pair_fraction=(
            part_size * (part_count - 1) / (dimension - 1)
        ),
        predicted_cross_leaf_principal_cosine=expected_cosine,
        observed_cross_leaf_principal_cosine=observed_cosine,
        predicted_cross_leaf_commutator_norm=expected_commutator,
        observed_cross_leaf_commutator_norm=leaf_commutator,
        predicted_nonscalarity_defect_edge=expected_nonscalarity,
        observed_nonscalarity_defect_edge=nonscalarity_edge,
        maximum_leaf_idempotence_residual=idempotence,
        frame_reconstruction_residual=reconstruction,
        canonical_whitening_residual=canonical,
        canonical_effect_sum_residual=effect_sum,
        maximum_canonical_effect_commutator_norm=canonical_commutator,
        distinct_leaf_projectors=distinct,
        reciprocal_integer_effect_spectrum_verified=bool(
            certificate["reciprocal_spectrum_residual"] <= 100 * tolerance
        ),
        exact_counterfamily_verified=exact,
        status=(
            "exact-duplicate-free-commuting-whitening-counterfamily-verified"
            if exact
            else "commuting-whitening-counterfamily-control-failure"
        ),
    )


def run_leaf_whitening_commutator_no_go() -> LeafWhiteningCommutatorNoGoReport:
    controls = [
        audit_commuting_whitening_counterfamily(
            f"CYCLIC-INDEPENDENT-SET-COVER-S{part_count}-P5-B2",
            part_count,
        )
        for part_count in (2, 3, 5, 8)
    ]
    scaling = [
        commuting_whitening_scaling_record(part_count)
        for part_count in (2, 3, 5, 8, 12, 20, 32, 48, 64, 96)
    ]
    failures = sum(not row.exact_counterfamily_verified for row in controls)
    exact = failures == 0
    tail = scaling[-1]
    return LeafWhiteningCommutatorNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "commuting_whitening_criterion": (
                "In a common eigenbasis of canonical effects H_e, projection "
                "idempotence is equivalent to H_e F H_e=H_e. Every positive "
                "entry is 1/F_ii, every F_ii is its integer incidence count, "
                "and every effect support is independent in the nonzero "
                "off-diagonal graph of F; these conditions are also sufficient."
            ),
            "spectral_arithmetic_corollary": (
                "Every nonzero eigenvalue of a commuting full-support canonical "
                "effect is the reciprocal of a positive integer. One eigenvalue "
                "outside {1,1/2,...,1/q} proves noncommutativity only before "
                "proper sibling common-span compression."
            ),
            "counterfamily": (
                "Cyclic interval supports inside parts give distinct rank-b "
                "projection leaves. Cross-part leaves have principal cosine "
                "b/r and density tending one, while whitening gives the "
                "commuting diagonal effects (1/b)P_e."
            ),
            "conditioning": (
                "The frame spectrum is b, b(1-1/s), and b(2-1/s), so its "
                "condition number is below three and tends to two."
            ),
            "nonscalarity": (
                "The component nonscalarity defect is exactly "
                "(1/b-1/r)I despite a zero commutator defect."
            ),
            "scope": (
                "This is a generic full-support projection-frame no-go, not a "
                "natural wreath counterexample. The reciprocal-integer criterion "
                "does not apply to properly compressed final-root effects."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_commuting_canonical_projection_frame_criterion",
                "resolved": exact,
                "resolution": "Projection idempotence reduces to the integer-degree independent-set cover criterion in the simultaneous effect eigenbasis.",
            },
            {
                "obligation": "test_leaf_commutator_transfer_under_bounded_frame_conditioning",
                "resolved": exact,
                "resolution": "The duplicate-free cyclic counterfamily has condition number below three and density-one inverse-polynomial leaf commutators but exactly commuting canonical effects.",
            },
            {
                "obligation": "derive_direct_natural_compressed_component_commutator_or_simultaneous_basis_theorem",
                "resolved": False,
                "resolution": "Common-span compression is POVM-universal, so the full-support integer-cover criterion cannot decide this gate. Analyze the natural compressed regular-master formula directly.",
            },
            {
                "obligation": "compile_natural_commuting_or_noncommuting_component_measurement",
                "resolved": False,
                "resolution": "The structural dichotomy supplies neither the simultaneous eigenbasis nor a matrix-POVM dilation circuit.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The whitening failure only occurs for an ill-conditioned frame.",
                "resolved": True,
                "resolution": "The exact frame condition number is below three and tends to two."
            },
            {
                "objection": "The whitening failure uses duplicate rank-one leaves.",
                "resolved": True,
                "resolution": "All cyclic supports and resulting rank-b leaf projectors are pairwise distinct."
            },
            {
                "objection": "Only a negligible fraction of leaves fail to commute before whitening.",
                "resolved": True,
                "resolution": "The cross-part pair fraction tends to one, and every cross-part pair has the exact inverse-linear commutator in (3)."
            },
            {
                "objection": "Full-rank nonscalarity or constant aspect should prevent canonical commutativity.",
                "resolved": True,
                "resolution": "The counterfamily has total-rank aspect b and nonscalarity edge tending to 1/b while every canonical commutator vanishes."
            },
            {
                "objection": "The abstract counterfamily proves natural wreath effects commute.",
                "resolved": False,
                "resolution": "It does not. Direct natural compressed commutator support or a coherent simultaneous-basis theorem remains open."
            },
        ],
        headline_metrics={
            "commuting_whitening_integer_cover_criterion_theorem_count": int(exact),
            "full_support_reciprocal_integer_spectral_witness_theorem_count": int(exact),
            "duplicate_free_bounded_condition_counterfamily_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "tail_fiber_dimension": tail.fiber_dimension,
            "tail_frame_condition_number": tail.frame_condition_number,
            "tail_cross_part_pair_fraction": tail.cross_part_pair_fraction,
            "tail_cross_leaf_commutator_norm": tail.cross_leaf_commutator_norm,
            "tail_nonscalarity_defect_edge": tail.nonscalarity_defect_edge,
            "full_support_spectral_criterion_survives_common_span_compression_count": 0,
            "natural_canonical_component_commutator_mass_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "generic_leaf_commutator_conditioning_transfer_valid": False,
            "generic_leaf_commutator_aspect_rank_transfer_valid": False,
            "commuting_canonical_projection_frame_characterized": exact,
            "nonreciprocal_full_support_effect_eigenvalue_is_exact_noncommutativity_witness": exact,
            "full_support_integer_cover_applies_after_common_span_compression": False,
            "natural_canonical_component_effect_algebra_noncommutative_on_positive_mass": False,
            "coherent_component_measurement_compiled": False,
            "physical_pgm_outside_mrs_transcript_postprocessing_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All currently proved coarse natural leaf/frame properties are "
                "compatible with commuting canonical effects. Proper common-span "
                "compression is POVM-universal, so a direct natural compressed "
                "commutator or simultaneous-basis theorem is required."
            ),
        },
        status=(
            "generic-full-support-leaf-transfer-falsified-compressed-component-analysis-open"
            if exact
            else "commuting-whitening-counterfamily-control-failure"
        ),
        summary=(
            "Characterized commuting canonical effects for projection frames "
            "and built a bounded-condition, duplicate-free counterfamily that "
            "kills every coarse leaf-to-component commutator transfer route."
        ),
        falsifiers_triggered=[
            "Density-one inverse-polynomial leaf commutators do not imply noncommuting canonical effects.",
            "A bounded frame condition number does not rescue leaf-to-component commutator transfer.",
            "Distinct high-rank leaves, constant total-rank aspect, vanishing relative leaf rank, and full-rank nonscalarity still do not rescue the transfer.",
            "Full-support spectral arithmetic also fails after proper common-span compression; the next natural gate is direct compressed commutator support or a simultaneous-basis compiler.",
        ],
    )


def write_leaf_whitening_commutator_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_leaf_whitening_commutator_no_go())
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
                id="NEG-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO."
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
                    "self_dual_wreath_leaf_whitening_commutator_no_go": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_leaf_whitening_commutator_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
