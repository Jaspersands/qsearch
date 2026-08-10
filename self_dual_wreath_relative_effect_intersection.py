"""Intersection localization theorem for hierarchical polar sampling.

Let ``A,B>=0``, ``S=A+B``, and work on ``supp(S)``.  The left relative effect

    C = S^(-1/2) A S^(-1/2)

satisfies ``0<=C<=I`` and ``I-C=S^(-1/2)BS^(-1/2)``.  Congruence preserves
ranks, so if ``r_A,r_B,r_S`` are the three support ranks, then

    rank(C)=r_A,  rank(I-C)=r_B.

If ``n_f`` is the number of eigenvalues strictly between zero and one, simple
rank counting gives

    n_f = r_A + r_B - r_S
        = dim(range(A) intersection range(B)).                 (1)

Thus nonorthogonal but linearly independent child ranges become exact routing
channels (relative eigenvalues zero or one) after canonical whitening.  All
genuinely weighted conditional sampling is localized to the child-range
intersection.  If a reducing common core carries proportional child frames
``A=aH`` and ``B=bH``, its relative eigenvalue is the computable ratio
``a/(a+b)``.

Complete ``W_4`` hierarchical controls satisfy (1).  Every fractional channel
is exactly balanced at ``1/2``.  This converts the large-n research target from
a global angle bound into a sharper overlap-core problem: classify the
intersections of nested orientation-coset frames, prove their relative weights
stay inverse-polynomially balanced (or are exact routable endpoints), and give
a coherent basis-free implementation of the resulting relative effects.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_hierarchical_polar_tree import (
    _psd_powers,
    relative_merge_isometry,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_relative_effect_intersection.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RelativeEffectRankControl:
    control_id: str
    carrier_dimension: int
    left_rank: int
    right_rank: int
    parent_rank: int
    child_range_intersection_dimension: int
    strict_fractional_eigenvalue_count: int
    zero_relative_eigenvalue_count: int
    one_relative_eigenvalue_count: int
    minimum_fractional_eigenvalue: float | None
    maximum_fractional_eigenvalue: float | None
    fractional_rank_identity_residual: int
    relative_effect_complement_residual: float
    exact_intersection_localization_verified: bool
    status: str


@dataclass(frozen=True)
class WreathRelativeIntersectionControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    left_rank: int
    right_rank: int
    parent_rank: int
    child_range_intersection_dimension: int
    strict_fractional_eigenvalue_count: int
    fractional_eigenvalues: tuple[float, ...]
    half_balance_residual: float
    child_frames_commute: bool
    exact_intersection_localization_verified: bool
    finite_balanced_overlap_core_observed: bool
    status: str


@dataclass(frozen=True)
class RelativeIntersectionScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_tree_depth: int
    relative_merge_count_when_level_indexed: int
    fractional_channels_equal_overlap_dimension_theorem: bool
    nonoverlap_channels_exactly_routable: bool
    typical_overlap_dimension_bound_proved: bool
    typical_overlap_weight_balance_proved: bool
    coherent_overlap_core_resolver_proved: bool
    status: str


@dataclass(frozen=True)
class RelativeEffectIntersectionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    generic_controls: list[RelativeEffectRankControl]
    wreath_controls: list[WreathRelativeIntersectionControl]
    scaling_records: list[RelativeIntersectionScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _rank(matrix: np.ndarray, tolerance: float) -> int:
    return int(
        np.count_nonzero(
            np.linalg.eigvalsh((matrix + matrix.conj().T) / 2) > tolerance
        )
    )


def audit_relative_effect_rank_identity(
    control_id: str,
    left: np.ndarray,
    right: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> RelativeEffectRankControl:
    relative, effect, support = relative_merge_isometry(
        left,
        right,
        tolerance=tolerance,
    )
    parent = left + right
    _, _, _, support_basis = _psd_powers(parent, tolerance)
    restricted = support_basis.conj().T @ effect @ support_basis
    eigenvalues = np.linalg.eigvalsh((restricted + restricted.conj().T) / 2)
    zero = int(np.count_nonzero(eigenvalues <= tolerance))
    one = int(np.count_nonzero(eigenvalues >= 1 - tolerance))
    fractional = eigenvalues[
        (eigenvalues > tolerance) & (eigenvalues < 1 - tolerance)
    ]
    left_rank = _rank(left, tolerance)
    right_rank = _rank(right, tolerance)
    parent_rank = support_basis.shape[1]
    intersection = left_rank + right_rank - parent_rank
    rank_residual = len(fractional) - intersection
    complement_residual = float(
        np.linalg.norm(relative.conj().T @ relative - support, ord=2)
    )
    verified = bool(
        rank_residual == 0
        and zero == parent_rank - left_rank
        and one == parent_rank - right_rank
        and complement_residual <= 100 * tolerance
    )
    return RelativeEffectRankControl(
        control_id=control_id,
        carrier_dimension=len(left),
        left_rank=left_rank,
        right_rank=right_rank,
        parent_rank=parent_rank,
        child_range_intersection_dimension=intersection,
        strict_fractional_eigenvalue_count=len(fractional),
        zero_relative_eigenvalue_count=zero,
        one_relative_eigenvalue_count=one,
        minimum_fractional_eigenvalue=(
            float(fractional[0]) if len(fractional) else None
        ),
        maximum_fractional_eigenvalue=(
            float(fractional[-1]) if len(fractional) else None
        ),
        fractional_rank_identity_residual=rank_residual,
        relative_effect_complement_residual=complement_residual,
        exact_intersection_localization_verified=verified,
        status=(
            "exact-relative-effect-intersection-localization"
            if verified
            else "relative-effect-rank-validation-failure"
        ),
    )


def _projector(vector: np.ndarray) -> np.ndarray:
    normalized = np.asarray(vector, dtype=float)
    normalized /= np.linalg.norm(normalized)
    return np.outer(normalized, normalized)


def _generic_controls() -> list[RelativeEffectRankControl]:
    e0 = np.asarray([1.0, 0.0, 0.0])
    e1 = np.asarray([0.0, 1.0, 0.0])
    e2 = np.asarray([0.0, 0.0, 1.0])
    nonorthogonal_disjoint = audit_relative_effect_rank_identity(
        "nonorthogonal-linearly-independent",
        _projector(e0),
        _projector(e0 + e1),
    )
    shared = _projector(e0)
    balanced_common = audit_relative_effect_rank_identity(
        "balanced-common-core",
        shared + _projector(e1),
        shared + _projector(e2),
    )
    unbalanced_common = audit_relative_effect_rank_identity(
        "unbalanced-common-core",
        3 * shared + _projector(e1),
        shared + 2 * _projector(e2),
    )
    positive_definite = audit_relative_effect_rank_identity(
        "full-overlap-positive-definite",
        np.diag([4.0, 2.0, 1.0]),
        np.asarray(
            [
                [2.0, 0.4, 0.0],
                [0.4, 1.5, 0.2],
                [0.0, 0.2, 3.0],
            ]
        ),
    )
    return [
        nonorthogonal_disjoint,
        balanced_common,
        unbalanced_common,
        positive_definite,
    ]


def _wreath_control(
    control_id: str,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    tolerance: float = 1e-8,
) -> WreathRelativeIntersectionControl:
    projectors = {
        mask: orientation_invariant_projector(target, labels, mask)
        for mask in (*left_masks, *right_masks)
    }
    zero = np.zeros_like(next(iter(projectors.values())))
    left = sum((projectors[mask] for mask in left_masks), zero.copy())
    right = sum((projectors[mask] for mask in right_masks), zero.copy())
    generic = audit_relative_effect_rank_identity(
        control_id,
        left,
        right,
        tolerance=tolerance,
    )
    _, effect, _ = relative_merge_isometry(left, right, tolerance=tolerance)
    _, _, _, support_basis = _psd_powers(left + right, tolerance)
    restricted = support_basis.conj().T @ effect @ support_basis
    eigenvalues = np.linalg.eigvalsh((restricted + restricted.conj().T) / 2)
    fractional = tuple(
        float(value)
        for value in eigenvalues
        if tolerance < value < 1 - tolerance
    )
    half_residual = max(
        (abs(value - 0.5) for value in fractional),
        default=0.0,
    )
    commute = bool(
        np.linalg.norm(left @ right - right @ left, ord=2)
        <= 100 * tolerance
    )
    balanced = bool(half_residual <= 100 * tolerance)
    return WreathRelativeIntersectionControl(
        control_id=control_id,
        n=4,
        target_partition=target,
        labels=labels,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        left_rank=generic.left_rank,
        right_rank=generic.right_rank,
        parent_rank=generic.parent_rank,
        child_range_intersection_dimension=(
            generic.child_range_intersection_dimension
        ),
        strict_fractional_eigenvalue_count=(
            generic.strict_fractional_eigenvalue_count
        ),
        fractional_eigenvalues=fractional,
        half_balance_residual=half_residual,
        child_frames_commute=commute,
        exact_intersection_localization_verified=(
            generic.exact_intersection_localization_verified
        ),
        finite_balanced_overlap_core_observed=balanced,
        status=(
            "exact-balanced-w4-overlap-core"
            if generic.exact_intersection_localization_verified and balanced
            else "w4-relative-intersection-validation-failure"
        ),
    )


def _wreath_controls() -> list[WreathRelativeIntersectionControl]:
    pairings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    controls: list[WreathRelativeIntersectionControl] = []
    for tuple_index, labels in enumerate(_w4_collision_free_labels()):
        for target in integer_partitions(4):
            if not any(
                float(
                    np.trace(
                        orientation_invariant_projector(target, labels, mask)
                    ).real
                )
                > 1e-8
                for mask in range(4)
            ):
                continue
            for pairing_index, (left, right) in enumerate(pairings):
                controls.append(
                    _wreath_control(
                        (
                            f"W4-{tuple_index}-{'-'.join(map(str, target))}-"
                            f"PAIRING-{pairing_index}"
                        ),
                        target,
                        labels,
                        left,
                        right,
                    )
                )
    return controls


def relative_intersection_scaling_record(
    n: int,
) -> RelativeIntersectionScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return RelativeIntersectionScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_tree_depth=copies,
        relative_merge_count_when_level_indexed=copies,
        fractional_channels_equal_overlap_dimension_theorem=True,
        nonoverlap_channels_exactly_routable=True,
        typical_overlap_dimension_bound_proved=False,
        typical_overlap_weight_balance_proved=False,
        coherent_overlap_core_resolver_proved=False,
        status="relative-complexity-localized-to-overlap-cores",
    )


def run_relative_effect_intersection() -> RelativeEffectIntersectionReport:
    generic = _generic_controls()
    wreath = _wreath_controls()
    scaling = [
        relative_intersection_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    generic_failures = sum(
        not row.exact_intersection_localization_verified for row in generic
    )
    wreath_failures = sum(
        not row.exact_intersection_localization_verified for row in wreath
    )
    balance_failures = sum(
        not row.finite_balanced_overlap_core_observed for row in wreath
    )
    fractional = sum(row.strict_fractional_eigenvalue_count for row in wreath)
    intersecting = sum(row.child_range_intersection_dimension > 0 for row in wreath)
    noncommuting_intersections = sum(
        row.child_range_intersection_dimension > 0 and not row.child_frames_commute
        for row in wreath
    )
    verified = generic_failures == wreath_failures == 0
    return RelativeEffectIntersectionReport(
        created_at=utc_now(),
        theorem_contract={
            "relative_effect": "C=S^-1/2 A S^-1/2 on supp(S), S=A+B.",
            "rank_identities": (
                "rank(C)=rank(A), rank(I-C)=rank(B), and "
                "rank(S)=dim(range(A)+range(B))."
            ),
            "fractional_localization": (
                "The number of eigenvalues c in (0,1) is rank(A)+rank(B)-"
                "rank(S)=dim(range(A) intersection range(B))."
            ),
            "sharp_routing": (
                "All dimensions outside the child-range intersection become "
                "exact c=0 or c=1 routing channels after parent whitening."
            ),
            "proportional_common_core": (
                "On a reducing common core with A=aH and B=bH, the relative "
                "effect is the scalar a/(a+b)."
            ),
            "new_asymptotic_target": (
                "Classify nested orientation-frame intersections, bound their "
                "relative weights away from nonexact endpoints, and implement "
                "their coherent resolver."
            ),
        },
        generic_controls=generic,
        wreath_controls=wreath,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "fractional_rank_intersection_identity",
                "resolved": verified,
                "resolution": (
                    "Rank counting for C and I-C proves the identity exactly; "
                    "generic and complete W4 controls validate conventions."
                ),
            },
            {
                "obligation": "nonoverlap_exact_routing",
                "resolved": verified,
                "resolution": (
                    "When child ranges intersect trivially, every relative "
                    "eigenvalue is exactly zero or one, regardless of angle."
                ),
            },
            {
                "obligation": "finite_w4_overlap_balance",
                "resolved": balance_failures == 0,
                "resolution": (
                    "All W4 fractional relative effects are exactly one half. "
                    "The noncommuting child-frame controls have disjoint ranges "
                    "and therefore reduce entirely to endpoint routing."
                ),
            },
            {
                "obligation": "typical_large_n_overlap_core_classification",
                "resolved": False,
                "resolution": (
                    "Existing recurring-irrep incidence certifies some common "
                    "directions but does not exhaust nested child intersections."
                ),
            },
            {
                "obligation": "typical_relative_weight_balance",
                "resolved": False,
                "resolution": (
                    "No theorem prevents a shared range from carrying an "
                    "exponentially unbalanced nonzero ratio between two children."
                ),
            },
            {
                "obligation": "coherent_overlap_core_resolver",
                "resolved": False,
                "resolution": (
                    "No polynomial transform labels all overlap cores and applies "
                    "their matrix-valued conditional rotation coherently."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Near-parallel disjoint child ranges create tiny relative probabilities.",
                "resolved": True,
                "resolution": (
                    "After canonical parent whitening, linearly independent "
                    "ranges are exact endpoint channels; their Euclidean angle "
                    "does not create a fractional eigenvalue."
                ),
            },
            {
                "objection": "Large recurring intersections necessarily kill the sampler.",
                "resolved": False,
                "resolution": (
                    "Intersection size only counts weighted channels. If their "
                    "child frames are equal or have computable balanced ratios, "
                    "they may be the easiest part of the recursion."
                ),
            },
            {
                "objection": "The W4 half ratios prove all orientation splits are balanced.",
                "resolved": False,
                "resolution": (
                    "W4 has four leaves and sparse active sectors. Growing-depth "
                    "nested frames can carry unequal incidence multiplicities."
                ),
            },
            {
                "objection": "The rank theorem supplies a circuit for endpoint routing.",
                "resolved": False,
                "resolution": (
                    "It is an algebraic localization theorem. A coherent basis-"
                    "free implementation of the canonical routing projectors is open."
                ),
            },
        ],
        headline_metrics={
            "relative_effect_intersection_localization_theorem_count": 1,
            "nonoverlap_exact_routing_theorem_count": 1,
            "generic_control_count": len(generic),
            "generic_validation_failure_count": generic_failures,
            "complete_w4_control_count": len(wreath),
            "w4_validation_failure_count": wreath_failures,
            "w4_balanced_overlap_failure_count": balance_failures,
            "w4_intersecting_control_count": intersecting,
            "w4_noncommuting_intersection_control_count": noncommuting_intersections,
            "w4_fractional_relative_channel_count": fractional,
            "tail_n": scaling[-1].n,
            "tail_orientation_tree_depth": scaling[-1].orientation_tree_depth,
            "typical_overlap_classification_theorem_count": 0,
            "typical_overlap_balance_theorem_count": 0,
            "coherent_overlap_core_resolver_count": 0,
            "global_nonorthogonal_sampler_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "relative_complexity_localized_to_child_intersections": verified,
            "nonoverlap_channels_exactly_routable_algebraically": verified,
            "finite_w4_overlap_channels_balanced": balance_failures == 0,
            "typical_large_n_overlap_cores_classified": False,
            "typical_overlap_weights_inverse_polynomially_balanced": False,
            "coherent_overlap_core_resolver_proved": False,
            "hierarchical_polar_sampler_polynomial": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The unresolved hierarchy is now localized to shared child "
                "ranges. Their all-n structure, balance, and coherent resolver "
                "remain unproved."
            ),
        },
        status=(
            "relative-polar-complexity-localized-to-overlap-cores"
            if verified and balance_failures == 0
            else "relative-effect-intersection-validation-failure"
        ),
        summary=(
            "Proved that strictly weighted relative-frame channels are counted "
            "exactly by child-range intersection dimension. Complete W4 "
            "intersections are commuting and balanced at one half, while "
            "noncommuting controls have disjoint child ranges. The next theorem "
            "must classify and resolve nested overlap cores at typical large n."
        ),
        falsifiers_triggered=[
            (
                "Do not use Euclidean near-parallelism of disjoint child ranges "
                "as a recursive-conditioning obstruction."
            ),
            (
                "Do not treat recurring common ranges only as spikes to reject; "
                "they are precisely the weighted channels the sampler must route."
            ),
            (
                "Do not promote finite half balance without an all-n incidence-"
                "weight theorem and coherent overlap resolver."
            ),
        ],
    )


def write_relative_effect_intersection_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_relative_effect_intersection())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION."
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
                    "self_dual_wreath_relative_effect_intersection": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_relative_effect_intersection_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
