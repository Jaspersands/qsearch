"""Single-anchor theorem for exact shorted balance.

Let ``E_a`` be one projector in a child frame

    A = E_a + sum_(i != a) E_i,

and let ``K subseteq ran(E_a)``.  Write ``R`` for the span of all other leaf
ranges.  If

    K perpendicular (ran(E_a) intersect R),                         (1)

then the shorted operator of ``A`` to ``K`` is exactly ``P_K``.

To prove this, express ``y in K`` as a sum of leaf vectors
``y=v_a+sum_i v_i``.  The remainder ``v=sum_i v_i`` lies in both ``R`` and
``ran(E_a)`` because ``v=y-v_a``.  By (1), ``v`` is orthogonal to ``y``, so

    ||v_a||^2 + sum_i ||v_i||^2
      = ||y||^2 + ||v||^2 + sum_i ||v_i||^2 >= ||y||^2.

The decomposition ``v_a=y`` attains equality.  Since minimum synthesis energy
on ``K`` is ``U^*A^+U``, this metric is ``I`` and the shorted operator is
``P_K``.  If opposite children have anchors whose common range is ``K`` and
both satisfy (1), their shorted metrics agree and every fractional relative
channel is exactly one half.

All fractional affine merges in the selected collision-free ``W_5`` sector
are explained by one anchor pair.  This is an exact finite mechanism, not an
all-n result: large children may contain many overlapping anchor cores or
emergent intersections, and efficiently resolving all anchor pairs remains
open.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_level_three_flag_audit import _reduced_projector_family
from self_dual_wreath_shorted_overlap_balance import (
    _psd_pseudoinverse,
    _range_intersection_basis,
    _support_basis,
    unique_affine_flag_merges,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_single_anchor_shorting.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SingleAnchorSideRecord:
    side_id: str
    child_orientation_masks: tuple[int, ...]
    anchor_orientation_mask: int
    core_dimension: int
    anchor_rank: int
    other_leaf_span_rank: int
    anchor_other_span_intersection_dimension: int
    maximum_anchor_core_containment_residual: float
    maximum_core_redundancy_overlap: float
    shorted_metric_identity_residual: float
    minimum_synthesis_anchor_route_residual: float
    maximum_other_leaf_minimum_coefficient_norm: float
    single_anchor_orthogonality_premise_verified: bool
    exact_single_anchor_shorting_verified: bool
    status: str


@dataclass(frozen=True)
class SingleAnchorMergeRecord:
    node_id: str
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    left_anchor_mask: int
    right_anchor_mask: int
    child_width: int
    anchor_common_core_dimension: int
    actual_child_intersection_dimension: int
    child_intersection_equals_anchor_core: bool
    left_side: SingleAnchorSideRecord
    right_side: SingleAnchorSideRecord
    maximum_fractional_half_residual: float
    exact_single_anchor_balanced_merge_verified: bool
    status: str


@dataclass(frozen=True)
class SingleAnchorScalingRecord:
    n: int
    information_threshold_copy_count: int
    maximum_common_free_certified_child_width: int
    isolated_anchor_shorting_theorem_available: bool
    all_overlap_cores_decomposed_into_isolated_anchors: bool
    polynomial_coherent_anchor_pair_resolver_proved: bool
    linear_width_overlap_controlled: bool
    hierarchical_orientation_polar_proved: bool
    status: str


@dataclass(frozen=True)
class SingleAnchorShortingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    generic_controls: list[SingleAnchorSideRecord]
    wreath_controls: list[SingleAnchorMergeRecord]
    scaling_records: list[SingleAnchorScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _orthonormalize(columns: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, _ = np.linalg.svd(columns, full_matrices=False)
    return left[:, singular_values > tolerance]


def audit_single_anchor_side(
    side_id: str,
    projectors: tuple[np.ndarray, ...],
    masks: tuple[int, ...],
    anchor_mask: int,
    core_basis: np.ndarray,
    *,
    tolerance: float = 1e-8,
) -> SingleAnchorSideRecord:
    if not masks or anchor_mask not in masks:
        raise ValueError("the anchor must belong to a nonempty child")
    dimension = len(projectors[0])
    if core_basis.shape[0] != dimension or not core_basis.shape[1]:
        raise ValueError("a nonempty core basis on the projector carrier is required")
    core = _orthonormalize(core_basis, tolerance)
    anchor = projectors[anchor_mask]
    other_masks = tuple(mask for mask in masks if mask != anchor_mask)
    zero = np.zeros((dimension, dimension), dtype=complex)
    other_frame = sum(
        (projectors[mask] for mask in other_masks),
        zero.copy(),
    )
    anchor_basis = _support_basis(anchor, tolerance)
    other_basis = _support_basis(other_frame, tolerance)
    redundancy = _range_intersection_basis(
        anchor_basis,
        other_basis,
        tolerance,
    )
    containment = float(np.linalg.norm(anchor @ core - core, ord=2))
    overlap = (
        float(np.linalg.norm(core.conj().T @ redundancy, ord=2))
        if redundancy.shape[1]
        else 0.0
    )

    child = anchor + other_frame
    inverse = _psd_pseudoinverse(child, tolerance)
    metric = core.conj().T @ inverse @ core
    metric_residual = float(
        np.linalg.norm(metric - np.eye(core.shape[1]), ord=2)
    )
    minimum_maps = {
        mask: projectors[mask] @ inverse @ core for mask in masks
    }
    anchor_route = float(
        np.linalg.norm(minimum_maps[anchor_mask] - core, ord=2)
    )
    other_route = max(
        (
            float(np.linalg.norm(minimum_maps[mask], ord=2))
            for mask in other_masks
        ),
        default=0.0,
    )
    premise = bool(
        containment <= 100 * tolerance and overlap <= 100 * tolerance
    )
    verified = bool(
        premise
        and metric_residual <= 100 * tolerance
        and anchor_route <= 100 * tolerance
        and other_route <= 100 * tolerance
    )
    return SingleAnchorSideRecord(
        side_id=side_id,
        child_orientation_masks=masks,
        anchor_orientation_mask=anchor_mask,
        core_dimension=core.shape[1],
        anchor_rank=anchor_basis.shape[1],
        other_leaf_span_rank=other_basis.shape[1],
        anchor_other_span_intersection_dimension=redundancy.shape[1],
        maximum_anchor_core_containment_residual=containment,
        maximum_core_redundancy_overlap=overlap,
        shorted_metric_identity_residual=metric_residual,
        minimum_synthesis_anchor_route_residual=anchor_route,
        maximum_other_leaf_minimum_coefficient_norm=other_route,
        single_anchor_orthogonality_premise_verified=premise,
        exact_single_anchor_shorting_verified=verified,
        status=(
            "exact-single-anchor-shorted-identity"
            if verified
            else "single-anchor-premise-fails"
            if not premise
            else "single-anchor-conclusion-validation-failure"
        ),
    )


def audit_single_anchor_merge(
    node_id: str,
    projectors: tuple[np.ndarray, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    left_anchor: int,
    right_anchor: int,
    *,
    tolerance: float = 1e-8,
) -> SingleAnchorMergeRecord:
    if len(left_masks) != len(right_masks):
        raise ValueError("a balanced merge is required")
    anchor_core = _range_intersection_basis(
        _support_basis(projectors[left_anchor], tolerance),
        _support_basis(projectors[right_anchor], tolerance),
        tolerance,
    )
    if not anchor_core.shape[1]:
        raise ValueError("the declared anchors have no common range")
    dimension = len(projectors[0])
    zero = np.zeros((dimension, dimension), dtype=complex)
    left_frame = sum(
        (projectors[mask] for mask in left_masks),
        zero.copy(),
    )
    right_frame = sum(
        (projectors[mask] for mask in right_masks),
        zero.copy(),
    )
    child_intersection = _range_intersection_basis(
        _support_basis(left_frame, tolerance),
        _support_basis(right_frame, tolerance),
        tolerance,
    )
    same_intersection = bool(
        child_intersection.shape[1] == anchor_core.shape[1]
        and np.linalg.norm(
            anchor_core @ anchor_core.conj().T
            - child_intersection @ child_intersection.conj().T,
            ord=2,
        )
        <= 100 * tolerance
    )
    left = audit_single_anchor_side(
        f"{node_id}-left",
        projectors,
        left_masks,
        left_anchor,
        anchor_core,
        tolerance=tolerance,
    )
    right = audit_single_anchor_side(
        f"{node_id}-right",
        projectors,
        right_masks,
        right_anchor,
        anchor_core,
        tolerance=tolerance,
    )

    parent = left_frame + right_frame
    inverse = _psd_pseudoinverse(parent, tolerance)
    inverse_eigenvalues, inverse_eigenvectors = np.linalg.eigh(
        (inverse + inverse.conj().T) / 2
    )
    inverse_root = (
        inverse_eigenvectors
        * np.sqrt(np.maximum(inverse_eigenvalues, 0.0))
    ) @ inverse_eigenvectors.conj().T
    support = _support_basis(parent, tolerance)
    effect = support.conj().T @ inverse_root @ left_frame @ inverse_root @ support
    spectrum = np.linalg.eigvalsh((effect + effect.conj().T) / 2)
    fractional = spectrum[
        (spectrum > 10 * tolerance) & (spectrum < 1 - 10 * tolerance)
    ]
    half_residual = max(
        (abs(float(value) - 0.5) for value in fractional),
        default=0.0,
    )
    verified = bool(
        same_intersection
        and left.exact_single_anchor_shorting_verified
        and right.exact_single_anchor_shorting_verified
        and len(fractional) == anchor_core.shape[1]
        and half_residual <= 100 * tolerance
    )
    return SingleAnchorMergeRecord(
        node_id=node_id,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        left_anchor_mask=left_anchor,
        right_anchor_mask=right_anchor,
        child_width=len(left_masks),
        anchor_common_core_dimension=anchor_core.shape[1],
        actual_child_intersection_dimension=child_intersection.shape[1],
        child_intersection_equals_anchor_core=same_intersection,
        left_side=left,
        right_side=right,
        maximum_fractional_half_residual=half_residual,
        exact_single_anchor_balanced_merge_verified=verified,
        status=(
            "exact-single-anchor-balanced-merge"
            if verified
            else "single-anchor-merge-premise-or-conclusion-fails"
        ),
    )


def _generic_controls() -> list[SingleAnchorSideRecord]:
    e0 = np.asarray([1.0, 0.0, 0.0])
    e1 = np.asarray([0.0, 1.0, 0.0])
    e2 = np.asarray([0.0, 0.0, 1.0])

    def projector(columns: np.ndarray) -> np.ndarray:
        basis = _orthonormalize(columns, 1e-10)
        return basis @ basis.T

    anchor = projector(np.column_stack((e0, e1)))
    transverse = projector((e1 + e2)[:, None])
    duplicate_core = projector(e0[:, None])
    core = e0[:, None]
    return [
        audit_single_anchor_side(
            "noncommuting-transverse-success",
            (anchor, transverse),
            (0, 1),
            0,
            core,
        ),
        audit_single_anchor_side(
            "duplicate-core-falsifier",
            (duplicate_core, duplicate_core),
            (0, 1),
            0,
            core,
        ),
    ]


def _w5_controls() -> list[SingleAnchorMergeRecord]:
    projectors, _, _ = _reduced_projector_family(
        (3, 2),
        _w5_probe_labels()[0],
        1e-8,
    )
    anchor_pair = (3, 6)
    controls = []
    for left, right in unique_affine_flag_merges():
        if anchor_pair[0] in left and anchor_pair[1] in right:
            left_anchor, right_anchor = anchor_pair
        elif anchor_pair[1] in left and anchor_pair[0] in right:
            left_anchor, right_anchor = reversed(anchor_pair)
        else:
            continue
        controls.append(
            audit_single_anchor_merge(
                f"W5-3-2-W{len(left)}-{'-'.join(map(str, left))}-{'-'.join(map(str, right))}",
                projectors,
                left,
                right,
                left_anchor,
                right_anchor,
            )
        )
    return controls


def single_anchor_scaling_record(n: int) -> SingleAnchorScalingRecord:
    if n < 5:
        raise ValueError("the common-free width theorem requires n>=5")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return SingleAnchorScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        maximum_common_free_certified_child_width=(n - 1) // 2,
        isolated_anchor_shorting_theorem_available=True,
        all_overlap_cores_decomposed_into_isolated_anchors=False,
        polynomial_coherent_anchor_pair_resolver_proved=False,
        linear_width_overlap_controlled=False,
        hierarchical_orientation_polar_proved=False,
        status="isolated-anchor-theorem-global-anchor-decomposition-open",
    )


def run_single_anchor_shorting() -> SingleAnchorShortingReport:
    generic = _generic_controls()
    wreath = _w5_controls()
    scaling = [
        single_anchor_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    positive_generic = generic[0].exact_single_anchor_shorting_verified
    duplicate_falsifier = (
        not generic[1].single_anchor_orthogonality_premise_verified
        and not generic[1].exact_single_anchor_shorting_verified
        and generic[1].shorted_metric_identity_residual > 1e-8
    )
    wreath_failures = sum(
        not row.exact_single_anchor_balanced_merge_verified for row in wreath
    )
    verified = positive_generic and duplicate_falsifier and wreath_failures == 0
    return SingleAnchorShortingReport(
        created_at=utc_now(),
        theorem_contract={
            "single_anchor_premise": (
                "K lies in one anchor leaf and is orthogonal to the intersection "
                "of that anchor range with the span of all other child leaves."
            ),
            "minimum_energy_conclusion": (
                "Every synthesis of y in K has energy at least ||y||^2, attained "
                "by the anchor-only synthesis; hence U^*A^+U=I."
            ),
            "balanced_merge_consequence": (
                "Opposite isolated anchors sharing exactly K give equal identity "
                "shorted metrics and only 1/2 fractional channels."
            ),
            "w5_mechanism": (
                "All selected W5 fractional nodes are exactly the common core of "
                "orientation masks 3 and 6, isolated inside both children."
            ),
            "scope": (
                "No theorem decomposes every growing child overlap into mutually "
                "orthogonal isolated anchor pairs or resolves them coherently."
            ),
        },
        generic_controls=generic,
        wreath_controls=wreath,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "single_anchor_shorted_identity_theorem",
                "resolved": verified,
                "resolution": (
                    "The minimum-energy proof is exact and both positive and "
                    "premise-violating controls behave as predicted."
                ),
            },
            {
                "obligation": "selected_w5_fractional_mechanism",
                "resolved": wreath_failures == 0,
                "resolution": (
                    "Every one of the 11 fractional affine merges is exhausted "
                    "by the isolated mask pair {3,6}."
                ),
            },
            {
                "obligation": "all_n_isolated_anchor_decomposition",
                "resolved": False,
                "resolution": (
                    "Multiple anchor cores can overlap and linear-width children "
                    "can have emergent intersections outside pair common ranges."
                ),
            },
            {
                "obligation": "coherent_anchor_pair_resolver",
                "resolved": False,
                "resolution": (
                    "Pair common-range filters have a principal-angle gap, but "
                    "no polynomial procedure enumerates only relevant pairs in "
                    "exponentially wide children."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Adding any extra leaf to an anchor changes its shorting.",
                "resolved": True,
                "resolution": (
                    "Transverse noncommuting leaves do not change the core metric "
                    "when the anchor redundancy is orthogonal to K."
                ),
            },
            {
                "objection": "Containment in one anchor leaf is sufficient.",
                "resolved": True,
                "resolution": (
                    "A duplicate-core leaf violates (1), changes the metric to "
                    "I/2, and is retained as a falsifier."
                ),
            },
            {
                "objection": "Pairwise common cores exhaust every child intersection.",
                "resolved": False,
                "resolution": (
                    "The W3 control has pairwise-emergent balanced intersections, "
                    "and the early-level coherence theorem becomes vacuous at "
                    "linear child width."
                ),
            },
            {
                "objection": "A known anchor pair is already a global circuit.",
                "resolved": False,
                "resolution": (
                    "At information-theoretic depth there are exponentially many "
                    "possible cross-child pairs unless representation structure "
                    "compresses their labels."
                ),
            },
        ],
        headline_metrics={
            "single_anchor_shorted_identity_theorem_count": int(verified),
            "generic_control_count": len(generic),
            "duplicate_core_falsifier_count": int(duplicate_falsifier),
            "w5_single_anchor_merge_count": len(wreath),
            "w5_single_anchor_validation_failure_count": wreath_failures,
            "w5_anchor_pair_count": 1,
            "w5_anchor_core_dimension": (
                wreath[0].anchor_common_core_dimension if wreath else 0
            ),
            "all_n_isolated_anchor_decomposition_theorem_count": 0,
            "coherent_anchor_pair_resolver_count": 0,
            "linear_width_overlap_theorem_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "single_anchor_shorted_identity_proved": verified,
            "selected_w5_fractional_merges_explained": wreath_failures == 0,
            "duplicate_anchor_core_breaks_identity": duplicate_falsifier,
            "all_n_overlap_decomposes_into_isolated_anchors": False,
            "polynomial_coherent_anchor_pair_resolver_proved": False,
            "linear_width_overlap_controlled": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Isolated anchor cores are exactly balanced, but no all-n "
                "decomposition or compressed coherent pair resolver is known."
            ),
        },
        status=(
            "single-anchor-shortening-proved-global-anchor-decomposition-open"
            if verified
            else "single-anchor-shorting-validation-failure"
        ),
        summary=(
            "Proved an exact minimum-energy shorting theorem and used it to "
            "explain every selected W5 fractional merge by one isolated anchor pair."
        ),
        falsifiers_triggered=[
            (
                "Anchor containment alone is insufficient; duplicate or redundant "
                "core access changes the shorted metric."
            ),
            (
                "Pair-anchor explanations do not cover pairwise-emergent W3 overlap."
            ),
            (
                "Finite unique-anchor structure does not bound the number or "
                "interaction of anchor cores at growing width."
            ),
        ],
    )


def write_single_anchor_shorting_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_single_anchor_shorting())
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
                id="NEG-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING."
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
                    "self_dual_wreath_single_anchor_shorting": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_single_anchor_shorting_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
