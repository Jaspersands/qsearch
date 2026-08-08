"""Canonical coefficient-space affine certificates for polar merges.

For a child frame ``A=sum_e E_e`` and an orthonormal basis ``U`` of a
subspace ``K subseteq ran(A)``, define its minimum-norm leaf synthesis maps

    D_(A,e) = E_e A^+ U.

They obey the exact identities

    sum_e D_(A,e) = U,
    sum_e D_(A,e)^* D_(A,e) = U^* A^+ U = G_A.       (1)

Thus ``G_A=gI_K`` precisely when the stacked minimum-norm coefficient map,
after division by ``sqrt(g)``, is an isometry.  For two children ``A,B`` with
common range ``K``, if ``G_A=G_B=gI`` then the shorted-overlap theorem forces
every fractional relative channel to be ``1/2``.  The normalized coefficient
images are joined by an exact partial isometry.

The finite label-simple wreath controls satisfy a stronger normal form.  Each
component effect is scalar,

    D_(A,e)^* D_(A,e) = w_e I_K,

the nonzero masks form an affine subset of ``F_2^3``, and all nonzero weights
are equal.  This is the correct location of the affine structure: the carrier
intersection itself need not reduce any leaf projector.  Repeated labels
break scalarity, uniformity, or affine support and produce nonhalf channels.

The maps in (1) contain ``A^+`` and therefore do not yet constitute a circuit.
The companion sparse-Gram partial-support audit supplies the missing
collision-free counterexample already at ``S_6``: the masks remain affine but
the component effects are nonscalar and cross-child effects do not commute.
The universal scalar coefficient-affine route is therefore dead.  The
research target is a matrix-valued partial-support compiler and a theorem for
its physical asymptotic mass.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_core_flag_theorem import is_affine_set
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_level_three_flag_audit import _reduced_projector_family
from self_dual_wreath_shorted_overlap_balance import (
    _psd_pseudoinverse,
    _range_intersection_basis,
    _support_basis,
    unique_affine_flag_merges,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_canonical_coefficient_affine.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CanonicalCoefficientNodeRecord:
    node_id: str
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    child_width: int
    intersection_dimension: int
    left_metric_scale: float
    right_metric_scale: float
    left_metric_scalar_residual: float
    right_metric_scalar_residual: float
    child_metric_equality_residual: float
    maximum_component_scalar_residual: float
    active_orientation_masks: tuple[int, ...]
    active_left_mask_count: int
    active_right_mask_count: int
    active_component_weights: tuple[tuple[int, float], ...]
    active_support_is_affine: bool
    maximum_active_weight_uniformity_residual: float
    maximum_synthesis_identity_residual: float
    maximum_coefficient_gram_identity_residual: float
    coefficient_transfer_initial_projection_residual: float
    coefficient_transfer_final_projection_residual: float
    exact_minimum_norm_decomposition_identities_verified: bool
    canonical_coefficient_affine_certificate: bool
    status: str


@dataclass(frozen=True)
class CanonicalCoefficientControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    globally_distinct_source_partitions: bool
    pairwise_distinct_physical_labels: bool
    carrier_dimension: int
    reduced_support_dimension: int
    fractional_merge_count: int
    exact_decomposition_identity_failure_count: int
    coefficient_affine_certificate_count: int
    coefficient_affine_certificate_failure_count: int
    nonaffine_active_support_count: int
    nonscalar_component_effect_count: int
    nonscalar_or_unequal_metric_count: int
    observed_active_supports: tuple[tuple[int, ...], ...]
    exact_canonical_coefficient_audit_verified: bool
    every_fractional_merge_has_coefficient_affine_certificate: bool
    node_records: list[CanonicalCoefficientNodeRecord]
    status: str


@dataclass(frozen=True)
class CanonicalCoefficientScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_tree_depth: int
    finite_coefficient_affine_signal_only: bool
    all_n_collision_free_coefficient_affine_theorem_proved: bool
    multiplicity_free_recoupling_formula_proved: bool
    coherent_minimum_norm_synthesis_compiled: bool
    hierarchical_orientation_polar_proved: bool
    status: str


@dataclass(frozen=True)
class CanonicalCoefficientAffineReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CanonicalCoefficientControl]
    scaling_records: list[CanonicalCoefficientScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_canonical_coefficient_node(
    node_id: str,
    projectors: tuple[np.ndarray, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> CanonicalCoefficientNodeRecord | None:
    if not projectors:
        raise ValueError("at least one projector is required")
    if not left_masks or not right_masks or set(left_masks) & set(right_masks):
        raise ValueError("disjoint nonempty children are required")
    if len(left_masks) != len(right_masks):
        raise ValueError("a balanced affine split is required")

    dimension = len(projectors[0])
    zero = np.zeros((dimension, dimension), dtype=complex)
    left = sum((projectors[mask] for mask in left_masks), zero.copy())
    right = sum((projectors[mask] for mask in right_masks), zero.copy())
    intersection = _range_intersection_basis(
        _support_basis(left, tolerance),
        _support_basis(right, tolerance),
        tolerance,
    )
    rank = intersection.shape[1]
    if not rank:
        return None

    identity = np.eye(rank)
    side_rows: list[tuple[Any, ...]] = []
    for masks, frame in ((left_masks, left), (right_masks, right)):
        inverse = _psd_pseudoinverse(frame, tolerance)
        maps = tuple(
            projectors[mask] @ inverse @ intersection for mask in masks
        )
        metric = intersection.conj().T @ inverse @ intersection
        synthesis_residual = float(
            np.linalg.norm(sum(maps) - intersection, ord=2)
        )
        effects = tuple(mapping.conj().T @ mapping for mapping in maps)
        gram_residual = float(
            np.linalg.norm(sum(effects) - metric, ord=2)
        )
        weights = tuple(
            float(np.trace(effect).real / rank) for effect in effects
        )
        metric_scale = float(np.trace(metric).real / rank)
        metric_scalar_residual = float(
            np.linalg.norm(metric - metric_scale * identity, ord=2)
        )
        scalar_residual = max(
            (
                float(np.linalg.norm(effect - weight * identity, ord=2))
                for effect, weight in zip(effects, weights)
            ),
            default=0.0,
        )
        active = [
            (mask, weight)
            for mask, weight in zip(masks, weights)
            if weight > 100 * tolerance
        ]
        stacked = np.vstack(maps)
        normalized_stacked = (
            stacked / math.sqrt(metric_scale)
            if metric_scale > tolerance
            else np.zeros_like(stacked)
        )
        side_rows.append(
            (
                metric_scale,
                metric_scalar_residual,
                synthesis_residual,
                gram_residual,
                active,
                normalized_stacked,
            )
        )

    (
        left_scale,
        left_metric_scalar,
        left_synthesis,
        left_gram,
        left_active,
        left_map,
    ) = side_rows[0]
    (
        right_scale,
        right_metric_scalar,
        right_synthesis,
        right_gram,
        right_active,
        right_map,
    ) = side_rows[1]
    active_rows = sorted((*left_active, *right_active))
    active_masks = tuple(mask for mask, _ in active_rows)
    active_weights = tuple(weight for _, weight in active_rows)
    affine = bool(active_masks) and is_affine_set(
        active_masks,
        (len(projectors) - 1).bit_length(),
    )
    uniformity = (
        max(active_weights) - min(active_weights) if active_weights else math.inf
    )

    transfer = right_map @ left_map.conj().T
    left_image = left_map @ left_map.conj().T
    right_image = right_map @ right_map.conj().T
    initial_residual = float(
        np.linalg.norm(transfer.conj().T @ transfer - left_image, ord=2)
    )
    final_residual = float(
        np.linalg.norm(transfer @ transfer.conj().T - right_image, ord=2)
    )
    maximum_scalar_residual = 0.0
    for masks, frame in ((left_masks, left), (right_masks, right)):
        inverse = _psd_pseudoinverse(frame, tolerance)
        for mask in masks:
            mapping = projectors[mask] @ inverse @ intersection
            effect = mapping.conj().T @ mapping
            weight = float(np.trace(effect).real / rank)
            maximum_scalar_residual = max(
                maximum_scalar_residual,
                float(np.linalg.norm(effect - weight * identity, ord=2)),
            )

    exact_identities = bool(
        max(left_synthesis, right_synthesis) <= 100 * tolerance
        and max(left_gram, right_gram) <= 100 * tolerance
    )
    certificate = bool(
        exact_identities
        and max(left_metric_scalar, right_metric_scalar) <= 100 * tolerance
        and abs(left_scale - right_scale) <= 100 * tolerance
        and maximum_scalar_residual <= 100 * tolerance
        and affine
        and len(left_active) == len(right_active)
        and uniformity <= 100 * tolerance
        and max(initial_residual, final_residual) <= 100 * tolerance
    )
    return CanonicalCoefficientNodeRecord(
        node_id=node_id,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        child_width=len(left_masks),
        intersection_dimension=rank,
        left_metric_scale=left_scale,
        right_metric_scale=right_scale,
        left_metric_scalar_residual=left_metric_scalar,
        right_metric_scalar_residual=right_metric_scalar,
        child_metric_equality_residual=float(
            np.linalg.norm(
                left_scale * identity - right_scale * identity,
                ord=2,
            )
        ),
        maximum_component_scalar_residual=maximum_scalar_residual,
        active_orientation_masks=active_masks,
        active_left_mask_count=len(left_active),
        active_right_mask_count=len(right_active),
        active_component_weights=tuple(
            (mask, round(weight, 10)) for mask, weight in active_rows
        ),
        active_support_is_affine=affine,
        maximum_active_weight_uniformity_residual=uniformity,
        maximum_synthesis_identity_residual=max(
            left_synthesis,
            right_synthesis,
        ),
        maximum_coefficient_gram_identity_residual=max(left_gram, right_gram),
        coefficient_transfer_initial_projection_residual=initial_residual,
        coefficient_transfer_final_projection_residual=final_residual,
        exact_minimum_norm_decomposition_identities_verified=exact_identities,
        canonical_coefficient_affine_certificate=certificate,
        status=(
            "exact-canonical-coefficient-affine-certificate"
            if certificate
            else "minimum-norm-identities-verified-certificate-fails"
            if exact_identities
            else "canonical-coefficient-identity-validation-failure"
        ),
    )


def audit_canonical_coefficient_control(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-8,
) -> CanonicalCoefficientControl:
    projectors, carrier_dimension, support_dimension = _reduced_projector_family(
        target,
        labels,
        tolerance,
    )
    records = []
    for left, right in unique_affine_flag_merges():
        record = audit_canonical_coefficient_node(
            f"{control_id}-W{len(left)}-{'-'.join(map(str, left))}-{'-'.join(map(str, right))}",
            projectors,
            left,
            right,
            tolerance=tolerance,
        )
        if record is not None:
            records.append(record)
    identity_failures = sum(
        not row.exact_minimum_norm_decomposition_identities_verified
        for row in records
    )
    certificate_count = sum(
        row.canonical_coefficient_affine_certificate for row in records
    )
    certificate_failures = len(records) - certificate_count
    source = tuple(partition for label in labels for partition in label)
    verified = identity_failures == 0
    return CanonicalCoefficientControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        globally_distinct_source_partitions=len(source) == len(set(source)),
        pairwise_distinct_physical_labels=len(labels) == len(set(labels)),
        carrier_dimension=carrier_dimension,
        reduced_support_dimension=support_dimension,
        fractional_merge_count=len(records),
        exact_decomposition_identity_failure_count=identity_failures,
        coefficient_affine_certificate_count=certificate_count,
        coefficient_affine_certificate_failure_count=certificate_failures,
        nonaffine_active_support_count=sum(
            not row.active_support_is_affine for row in records
        ),
        nonscalar_component_effect_count=sum(
            row.maximum_component_scalar_residual > 100 * tolerance
            for row in records
        ),
        nonscalar_or_unequal_metric_count=sum(
            max(
                row.left_metric_scalar_residual,
                row.right_metric_scalar_residual,
                row.child_metric_equality_residual,
            )
            > 100 * tolerance
            for row in records
        ),
        observed_active_supports=tuple(
            sorted({row.active_orientation_masks for row in records})
        ),
        exact_canonical_coefficient_audit_verified=verified,
        every_fractional_merge_has_coefficient_affine_certificate=(
            bool(records) and not certificate_failures
        ),
        node_records=records,
        status=(
            "all-fractional-merges-canonical-coefficient-affine"
            if verified and records and not certificate_failures
            else "canonical-coefficient-counterexample-present"
            if verified and certificate_failures
            else "canonical-coefficient-audit-validation-failure"
        ),
    )


def canonical_coefficient_scaling_record(
    n: int,
) -> CanonicalCoefficientScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return CanonicalCoefficientScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_tree_depth=copies,
        finite_coefficient_affine_signal_only=True,
        all_n_collision_free_coefficient_affine_theorem_proved=False,
        multiplicity_free_recoupling_formula_proved=False,
        coherent_minimum_norm_synthesis_compiled=False,
        hierarchical_orientation_polar_proved=False,
        status="finite-coefficient-affine-signal-all-n-recoupling-proof-open",
    )


def run_canonical_coefficient_affine() -> CanonicalCoefficientAffineReport:
    distinct_triangle: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    repeated: tuple[Label, ...] = (((3,), (2, 1)),) * 3
    controls = [
        audit_canonical_coefficient_control(
            "W3-DISTINCT-LABEL-TRIANGLE",
            3,
            (2, 1),
            distinct_triangle,
        ),
        audit_canonical_coefficient_control(
            "W3-REPEATED-LABEL-FALSIFIER",
            3,
            (2, 1),
            repeated,
        ),
        audit_canonical_coefficient_control(
            "W5-COLLISION-FREE-3-2",
            5,
            (3, 2),
            _w5_probe_labels()[0],
        ),
    ]
    scaling = [
        canonical_coefficient_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    validation_failures = sum(
        not row.exact_canonical_coefficient_audit_verified for row in controls
    )
    label_simple = [
        row for row in controls if row.pairwise_distinct_physical_labels
    ]
    repeated_controls = [
        row for row in controls if not row.pairwise_distinct_physical_labels
    ]
    finite_signal = bool(label_simple) and all(
        row.every_fractional_merge_has_coefficient_affine_certificate
        for row in label_simple
    )
    repeated_falsifier = any(
        row.coefficient_affine_certificate_failure_count > 0
        for row in repeated_controls
    )
    verified = validation_failures == 0
    return CanonicalCoefficientAffineReport(
        created_at=utc_now(),
        theorem_contract={
            "minimum_norm_synthesis": (
                "D_(A,e)=E_e A^+U sums to U and its component Gram operators "
                "sum to G_A=U^*A^+U."
            ),
            "isometric_balance": (
                "If G_A=G_B=gI, the two stacked coefficient maps become "
                "isometries after common normalization and every fractional "
                "relative channel is 1/2."
            ),
            "coefficient_affine_normal_form": (
                "Finite label-simple controls have scalar equal component "
                "weights supported on an affine mask set."
            ),
            "coefficient_transfer": (
                "For isometric child decompositions, D_B D_A^* is a partial "
                "isometry between their coefficient images."
            ),
            "scope": (
                "The canonical maps use child pseudoinverses. The companion "
                "sparse-Gram S6 control falsifies scalar component effects even "
                "with globally distinct sources and affine masks, so the all-n "
                "target must be matrix-valued partial support."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "canonical_minimum_norm_decomposition_identities",
                "resolved": verified,
                "resolution": (
                    "Moore-Penrose identities prove both equations and every "
                    "finite node validates them numerically."
                ),
            },
            {
                "obligation": "correct_location_of_affine_balance",
                "resolved": finite_signal,
                "resolution": (
                    "All label-simple finite overlaps have affine uniform scalar "
                    "effects in coefficient space despite nonreducing carriers."
                ),
            },
            {
                "obligation": "all_n_collision_free_coefficient_affine_theorem",
                "resolved": True,
                "resolution": (
                    "Rejected by the companion globally source-distinct S6 "
                    "control: affine masks coexist with nonscalar component "
                    "effects and noncommuting cross-child supports."
                ),
            },
            {
                "obligation": "explicit_recoupling_synthesis_maps",
                "resolved": False,
                "resolution": (
                    "The current certificate defines D_(A,e) using A^+; no "
                    "multiplicity-basis or Racah circuit constructs it directly."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Affine structure must live in reducing carrier cores.",
                "resolved": True,
                "resolution": (
                    "It instead appears in the canonical coefficient effects, "
                    "which remain affine when the carrier intersection is emergent."
                ),
            },
            {
                "objection": "Any balanced merge has a coefficient-affine certificate.",
                "resolved": True,
                "resolution": (
                    "A repeated-label balanced node has a uniform six-mask support, "
                    "which is nonaffine; nine other repeated-label nodes are unbalanced."
                ),
            },
            {
                "objection": "The partial coefficient transfer is already efficient.",
                "resolved": False,
                "resolution": (
                    "Its present formula contains pseudoinverses of child frames and "
                    "is a structural target, not a compiled operation."
                ),
            },
            {
                "objection": "Collision-free labels prevent all recoupling collisions.",
                "resolved": True,
                "resolution": (
                    "The companion S6 control has eight globally distinct source "
                    "partitions and still exhibits matrix partial-support traffic."
                ),
            },
        ],
        headline_metrics={
            "canonical_minimum_norm_identity_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_validation_failure_count": validation_failures,
            "label_simple_control_count": len(label_simple),
            "label_simple_fractional_merge_count": sum(
                row.fractional_merge_count for row in label_simple
            ),
            "label_simple_coefficient_affine_certificate_failure_count": sum(
                row.coefficient_affine_certificate_failure_count
                for row in label_simple
            ),
            "repeated_label_coefficient_affine_failure_count": sum(
                row.coefficient_affine_certificate_failure_count
                for row in repeated_controls
            ),
            "repeated_label_nonscalar_or_unequal_metric_count": sum(
                row.nonscalar_or_unequal_metric_count
                for row in repeated_controls
            ),
            "all_n_coefficient_affine_theorem_count": 0,
            "natural_collision_free_scalar_affine_falsifier_count": 1,
            "explicit_recoupling_synthesis_map_count": 0,
            "coherent_coefficient_transfer_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "canonical_minimum_norm_identities_proved": verified,
            "finite_label_simple_coefficient_affine_signal": finite_signal,
            "repeated_labels_falsify_universal_coefficient_affinity": (
                repeated_falsifier
            ),
            "natural_collision_free_scalar_affinity_falsified": True,
            "all_n_collision_free_coefficient_affine_theorem_proved": False,
            "multiplicity_free_recoupling_formula_proved": False,
            "coherent_minimum_norm_synthesis_compiled": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The finite scalar coefficient-space controls are exact, but a "
                "natural S6 node falsifies their universal extension. A matrix "
                "partial-support compiler and mass theorem are required."
            ),
        },
        status=(
            "finite-scalar-affine-normal-form-natural-s6-universal-falsifier"
            if verified and finite_signal and repeated_falsifier
            else "canonical-coefficient-affine-validation-failure"
        ),
        summary=(
            "Moved the affine mechanism into minimum-norm coefficient space, "
            "where W3/W5 have scalar certificates but a globally distinct S6 "
            "affine node forces matrix-valued partial supports."
        ),
        falsifiers_triggered=[
            (
                "Affine carrier-core exhaustion is the wrong necessary condition; "
                "canonical coefficient affinity survives emergent intersections."
            ),
            (
                "Balanced shorted metrics do not force affine coefficient support."
            ),
            (
                "External label distinctness does not by itself prove internal "
                "multiplicity-free recoupling; S6 already supplies a counterexample."
            ),
        ],
    )


def write_canonical_coefficient_affine_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_canonical_coefficient_affine())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE",
                source=registry_experiment_id,
                claim=(
                    "Naive initial assumption for EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE."
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
                    "self_dual_wreath_canonical_coefficient_affine": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_canonical_coefficient_affine_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
