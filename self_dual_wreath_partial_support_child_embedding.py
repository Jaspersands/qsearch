"""Natural partial-support obstruction to the scalar affine GPE compiler.

The recursive-node compiler is efficient in a flat scalar affine sector:
every active mask component of a normalized child embedding has effect
``w I`` on one common fiber.  Affine mask support alone does not imply this.

This module reconstructs normalized child embeddings using only the leaf
block Gram, without forming ambient projectors.  Let ``Q_e`` be leaf
isometries, ``S_L,S_R`` the child syntheses, and let ``Z=(Z_L,Z_R)`` be an
orthonormal basis of the cross-dependency kernel

    S_L Z_L = S_R Z_R.                                   (1)

After orthonormalizing the physical common image, the minimum-energy
preimages ``P_s`` give short metrics ``A_s=P_s^*P_s`` and normalized child
embeddings ``W_s=P_s A_s^(-1/2)``.  Their mask effects

    H_(s,e) = W_(s,e)^* W_(s,e)                           (2)

are positive and sum exactly to identity on each child.  A flat scalar fiber
requires every nonzero ``H_(s,e)=w_e I``.  More generally, nontrivial supports
and noncommuting effects form a matrix-valued partial-support sheaf.

The globally source-distinct S6 noncommuting-core control is a direct natural
falsifier of the scalar route.  Its four active masks form an affine plane,
but one child has complementary rank-9/rank-25 projector effects while the
other has a rank-9 effect of weight ``1/178`` and a full-rank complement.
Cross-child effects have nonzero commutator norm ``1/356``.  The endpoint
weights reproduce the known channels ``8/17``, ``1/2``, and ``89/170`` (up to
left/right convention).

This does not rule out a recursive GPE compiler.  It changes the target: the
compiler must coherently select partial supports, transport each support
channel, implement the matrix endpoint mixer, and resolve their holonomy.
The companion source-mass theorem proves that this direct S6 trivial/sign
mechanism is factorially rare.  No all-n circuit or positive-mass theorem for
high-dimensional-source partial supports is proved here.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_core_flag_theorem import is_affine_set
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_dependency_homology import _dependency_basis_from_blocks
from self_dual_wreath_sparse_invariant_dependency import (
    orientation_invariant_range_basis,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_partial_support_child_embedding.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ComponentEffectRecord:
    side: str
    orientation_mask: int
    coefficient_block_dimension: int
    support_rank: int
    trace_weight: float
    minimum_positive_eigenvalue: float
    maximum_eigenvalue: float
    full_fiber_scalar_residual: float
    support_scalar_residual: float
    exact_full_fiber_scalar: bool
    exact_scalar_on_support: bool
    status: str


@dataclass(frozen=True)
class PartialSupportChildControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    globally_distinct_source_partitions: bool
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    active_orientation_masks: tuple[int, ...]
    active_support_is_affine: bool
    ambient_physical_dimension: int
    common_span_dimension: int
    child_dependency_coefficient_dimension: int
    maximum_leaf_isometry_residual: float
    common_image_left_gram_residual: float
    common_image_right_gram_residual: float
    common_image_cross_gram_residual: float
    left_embedding_isometry_residual: float
    right_embedding_isometry_residual: float
    left_effect_sum_residual: float
    right_effect_sum_residual: float
    left_short_metric_minimum_eigenvalue: float
    left_short_metric_maximum_eigenvalue: float
    right_short_metric_minimum_eigenvalue: float
    right_short_metric_maximum_eigenvalue: float
    short_metric_equality_residual: float
    short_metric_commutator_norm: float
    maximum_component_full_fiber_scalar_residual: float
    maximum_component_support_scalar_residual: float
    maximum_cross_child_effect_commutator_norm: float
    endpoint_left_weight_spectrum: tuple[tuple[str, int], ...]
    endpoint_right_weight_spectrum: tuple[tuple[str, int], ...]
    component_effects: list[ComponentEffectRecord]
    exact_gram_reconstruction_verified: bool
    scalar_flat_affine_child_embedding_certificate: bool
    matrix_partial_support_required: bool
    status: str


@dataclass(frozen=True)
class PartialSupportChildEmbeddingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[PartialSupportChildControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_inverse_root(
    matrix: np.ndarray,
    *,
    tolerance: float,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("matrix is not positive semidefinite")
    inverse = np.zeros_like(values)
    positive = values > 100 * tolerance
    inverse[positive] = values[positive] ** -0.5
    return (vectors * inverse) @ vectors.conj().T


def _block_gram(
    bases: dict[int, np.ndarray],
    rows: tuple[int, ...],
    columns: tuple[int, ...],
) -> np.ndarray:
    return np.block(
        [
            [bases[left].conj().T @ bases[right] for right in columns]
            for left in rows
        ]
    )


def _spectrum_with_multiplicity(
    matrix: np.ndarray,
    *,
    tolerance: float,
) -> tuple[tuple[str, int], ...]:
    values = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    groups: list[list[float | int]] = []
    for value in values:
        if groups and abs(float(value) - float(groups[-1][0])) <= 100 * tolerance:
            groups[-1][1] = int(groups[-1][1]) + 1
        else:
            groups.append([float(value), 1])
    return tuple(
        (
            str(Fraction(float(value)).limit_denominator(100_000)),
            int(multiplicity),
        )
        for value, multiplicity in groups
    )


def _component_effect_records(
    side: str,
    masks: tuple[int, ...],
    widths: tuple[int, ...],
    embedding: np.ndarray,
    *,
    tolerance: float,
) -> tuple[list[ComponentEffectRecord], dict[int, np.ndarray]]:
    records = []
    effects = {}
    offset = 0
    fiber_dimension = embedding.shape[1]
    identity = np.eye(fiber_dimension, dtype=complex)
    for mask, width in zip(masks, widths):
        block = embedding[offset : offset + width]
        offset += width
        effect = (block.conj().T @ block + block.conj().T @ block) / 2
        effects[mask] = effect
        values, vectors = np.linalg.eigh(effect)
        positive = values > 100 * tolerance
        rank = int(np.sum(positive))
        if rank:
            support = vectors[:, positive] @ vectors[:, positive].conj().T
            support_scale = float(np.mean(values[positive]))
            minimum_positive = float(values[positive].min())
            maximum = float(values[positive].max())
            support_residual = float(
                np.linalg.norm(effect - support_scale * support, ord=2)
            )
        else:
            support = np.zeros_like(effect)
            support_scale = 0.0
            minimum_positive = 0.0
            maximum = 0.0
            support_residual = 0.0
        full_scale = float(np.trace(effect).real / fiber_dimension)
        full_residual = float(
            np.linalg.norm(effect - full_scale * identity, ord=2)
        )
        full_scalar = full_residual <= 1000 * tolerance
        support_scalar = support_residual <= 1000 * tolerance
        records.append(
            ComponentEffectRecord(
                side=side,
                orientation_mask=mask,
                coefficient_block_dimension=width,
                support_rank=rank,
                trace_weight=float(np.trace(effect).real),
                minimum_positive_eigenvalue=minimum_positive,
                maximum_eigenvalue=maximum,
                full_fiber_scalar_residual=full_residual,
                support_scalar_residual=support_residual,
                exact_full_fiber_scalar=full_scalar,
                exact_scalar_on_support=support_scalar,
                status=(
                    "scalar-full-fiber-component"
                    if full_scalar
                    else "scalar-partial-support-component"
                    if support_scalar
                    else "matrix-valued-partial-support-component"
                ),
            )
        )
    return records, effects


def audit_partial_support_child_embedding(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> PartialSupportChildControl:
    if not left_masks or not right_masks or set(left_masks) & set(right_masks):
        raise ValueError("disjoint nonempty child masks are required")
    requested = tuple(sorted((*left_masks, *right_masks)))
    bases = {
        mask: orientation_invariant_range_basis(
            target,
            labels,
            mask,
            tolerance=tolerance,
        )[0]
        for mask in requested
    }
    active = tuple(mask for mask in requested if bases[mask].shape[1])
    if active != requested:
        raise ValueError("the selected control contains an inactive orientation")
    ambient = next(iter(bases.values())).shape[0]
    leaf_residual = max(
        float(
            np.linalg.norm(
                basis.conj().T @ basis - np.eye(basis.shape[1]),
                ord=2,
            )
        )
        for basis in bases.values()
    )

    left_gram = _block_gram(bases, left_masks, left_masks)
    right_gram = _block_gram(bases, right_masks, right_masks)
    cross_gram = _block_gram(bases, left_masks, right_masks)
    dependency = _dependency_basis_from_blocks(
        left_gram,
        right_gram,
        cross_gram,
        tolerance,
    )
    if not dependency.shape[1]:
        raise ValueError("the selected child spans do not intersect")
    left_dimension = left_gram.shape[0]
    left_dependency = dependency[:left_dimension]
    right_dependency = dependency[left_dimension:]
    physical_gram_left = (
        left_dependency.conj().T @ left_gram @ left_dependency
    )
    physical_gram_right = (
        right_dependency.conj().T @ right_gram @ right_dependency
    )
    physical_gram = (physical_gram_left + physical_gram_right) / 2
    physical_inverse_root = _psd_inverse_root(
        physical_gram,
        tolerance=tolerance,
    )
    left_preimage = left_dependency @ physical_inverse_root
    right_preimage = right_dependency @ physical_inverse_root
    fiber_dimension = dependency.shape[1]
    identity = np.eye(fiber_dimension, dtype=complex)
    left_common_residual = float(
        np.linalg.norm(
            left_preimage.conj().T @ left_gram @ left_preimage - identity,
            ord=2,
        )
    )
    right_common_residual = float(
        np.linalg.norm(
            right_preimage.conj().T @ right_gram @ right_preimage - identity,
            ord=2,
        )
    )
    cross_common_residual = float(
        np.linalg.norm(
            left_preimage.conj().T @ cross_gram @ right_preimage - identity,
            ord=2,
        )
    )

    left_metric = left_preimage.conj().T @ left_preimage
    right_metric = right_preimage.conj().T @ right_preimage
    left_embedding = left_preimage @ _psd_inverse_root(
        left_metric,
        tolerance=tolerance,
    )
    right_embedding = right_preimage @ _psd_inverse_root(
        right_metric,
        tolerance=tolerance,
    )
    left_isometry = float(
        np.linalg.norm(left_embedding.conj().T @ left_embedding - identity, ord=2)
    )
    right_isometry = float(
        np.linalg.norm(right_embedding.conj().T @ right_embedding - identity, ord=2)
    )
    left_widths = tuple(bases[mask].shape[1] for mask in left_masks)
    right_widths = tuple(bases[mask].shape[1] for mask in right_masks)
    left_records, left_effects = _component_effect_records(
        "left",
        left_masks,
        left_widths,
        left_embedding,
        tolerance=tolerance,
    )
    right_records, right_effects = _component_effect_records(
        "right",
        right_masks,
        right_widths,
        right_embedding,
        tolerance=tolerance,
    )
    records = [*left_records, *right_records]
    left_sum = sum(left_effects.values(), np.zeros_like(identity))
    right_sum = sum(right_effects.values(), np.zeros_like(identity))
    cross_commutator = max(
        (
            float(np.linalg.norm(left @ right - right @ left, ord=2))
            for left in left_effects.values()
            for right in right_effects.values()
        ),
        default=0.0,
    )
    metric_commutator = float(
        np.linalg.norm(
            left_metric @ right_metric - right_metric @ left_metric,
            ord=2,
        )
    )
    scalar_residual = max(
        record.full_fiber_scalar_residual for record in records
    )
    support_residual = max(record.support_scalar_residual for record in records)
    bit_count = len(labels)
    affine = is_affine_set(active, bit_count)
    exact = bool(
        max(
            leaf_residual,
            left_common_residual,
            right_common_residual,
            cross_common_residual,
            left_isometry,
            right_isometry,
            float(np.linalg.norm(left_sum - identity, ord=2)),
            float(np.linalg.norm(right_sum - identity, ord=2)),
        )
        <= 1000 * tolerance
    )
    scalar_certificate = bool(exact and affine and scalar_residual <= 1000 * tolerance)
    partial_required = bool(exact and not scalar_certificate)
    source = tuple(partition for label in labels for partition in label)
    left_values = np.linalg.eigvalsh((left_metric + left_metric.conj().T) / 2)
    right_values = np.linalg.eigvalsh((right_metric + right_metric.conj().T) / 2)
    return PartialSupportChildControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        globally_distinct_source_partitions=len(source) == len(set(source)),
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        active_orientation_masks=active,
        active_support_is_affine=affine,
        ambient_physical_dimension=ambient,
        common_span_dimension=fiber_dimension,
        child_dependency_coefficient_dimension=dependency.shape[0],
        maximum_leaf_isometry_residual=leaf_residual,
        common_image_left_gram_residual=left_common_residual,
        common_image_right_gram_residual=right_common_residual,
        common_image_cross_gram_residual=cross_common_residual,
        left_embedding_isometry_residual=left_isometry,
        right_embedding_isometry_residual=right_isometry,
        left_effect_sum_residual=float(np.linalg.norm(left_sum - identity, ord=2)),
        right_effect_sum_residual=float(np.linalg.norm(right_sum - identity, ord=2)),
        left_short_metric_minimum_eigenvalue=float(left_values.min()),
        left_short_metric_maximum_eigenvalue=float(left_values.max()),
        right_short_metric_minimum_eigenvalue=float(right_values.min()),
        right_short_metric_maximum_eigenvalue=float(right_values.max()),
        short_metric_equality_residual=float(
            np.linalg.norm(left_metric - right_metric, ord=2)
        ),
        short_metric_commutator_norm=metric_commutator,
        maximum_component_full_fiber_scalar_residual=scalar_residual,
        maximum_component_support_scalar_residual=support_residual,
        maximum_cross_child_effect_commutator_norm=cross_commutator,
        endpoint_left_weight_spectrum=_spectrum_with_multiplicity(
            left_dependency.conj().T @ left_dependency,
            tolerance=tolerance,
        ),
        endpoint_right_weight_spectrum=_spectrum_with_multiplicity(
            right_dependency.conj().T @ right_dependency,
            tolerance=tolerance,
        ),
        component_effects=records,
        exact_gram_reconstruction_verified=exact,
        scalar_flat_affine_child_embedding_certificate=scalar_certificate,
        matrix_partial_support_required=partial_required,
        status=(
            "exact-scalar-flat-affine-child-embedding"
            if scalar_certificate
            else "exact-affine-mask-matrix-partial-support-child-embedding"
            if partial_required and affine
            else "exact-nonaffine-matrix-partial-support-child-embedding"
            if partial_required
            else "partial-support-child-embedding-audit-failure"
        ),
    )


def _controls() -> list[PartialSupportChildControl]:
    w3_labels: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    s6_labels: tuple[Label, ...] = (
        ((6,), (4, 2)),
        ((5, 1), (2, 2, 2)),
        ((3, 3), (2, 1, 1, 1, 1)),
        ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    return [
        audit_partial_support_child_embedding(
            "W3-DISTINCT-SCALAR-AFFINE-CONTROL",
            3,
            (2, 1),
            w3_labels,
            (0, 2),
            (5, 7),
        ),
        audit_partial_support_child_embedding(
            "W6-COLLISION-FREE-NONCOMMUTING-PARTIAL-SUPPORT",
            6,
            (6,),
            s6_labels,
            (2, 5),
            (11, 12),
        ),
    ]


def run_partial_support_child_embedding() -> PartialSupportChildEmbeddingReport:
    controls = _controls()
    scalar, partial = controls
    failures = sum(not row.exact_gram_reconstruction_verified for row in controls)
    natural_falsifier = bool(
        partial.globally_distinct_source_partitions
        and partial.active_support_is_affine
        and not partial.scalar_flat_affine_child_embedding_certificate
        and partial.maximum_cross_child_effect_commutator_norm > 1e-8
    )
    verified = failures == 0 and natural_falsifier
    return PartialSupportChildEmbeddingReport(
        created_at=utc_now(),
        theorem_contract={
            "gram_reconstruction": (
                "The leaf block Gram determines the cross dependency, the "
                "orthonormal physical common image, both short metrics, and "
                "every normalized child component effect without ambient "
                "projectors."
            ),
            "component_povm": (
                "For each child, H_(s,e)=W_(s,e)^*W_(s,e) is positive and "
                "the component effects sum exactly to identity."
            ),
            "scalar_affine_boundary": (
                "The flat scalar affine compiler requires every active effect "
                "to be scalar on the full common fiber; affine mask support "
                "alone is insufficient."
            ),
            "natural_s6_falsifier": (
                "A globally source-distinct S6 affine plane has nonscalar "
                "partial-support effects and noncommuting cross-child effects, "
                "while reproducing the known nonhalf endpoint spectrum."
            ),
            "scope": (
                "This redirects the compiler to matrix-valued partial supports. "
                "The companion source-mass theorem makes the direct trivial/sign "
                "mechanism factorially rare. No uniform GPE support SELECT or "
                "high-dimensional-source mass theorem is established."
            ),
        },
        controls=controls,
        proof_obligations=[
            {
                "obligation": "gram_only_normalized_child_embedding_reconstruction",
                "resolved": failures == 0,
                "resolution": "Both controls reconstruct common images, short metrics, isometric child embeddings, and component POVMs from block Grams.",
            },
            {
                "obligation": "collision_free_affine_support_implies_scalar_fibers",
                "resolved": True,
                "resolution": "Rejected by the globally source-distinct S6 affine-plane control with nonscalar partial supports and nonzero cross-effect commutator.",
            },
            {
                "obligation": "compile_matrix_partial_support_sheaf_with_gpe",
                "resolved": False,
                "resolution": "Need coherent support/eigenchannel SELECT, compatible GPE transports, matrix endpoint mixing, and holonomy filtering without width normalization.",
            },
            {
                "obligation": "prove_positive_native_pgm_mass_of_partial_support_obstruction",
                "resolved": False,
                "resolution": "The S6 control is natural and collision-free but finite; its frame-weighted asymptotic mass is unknown.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Affine active masks imply the flat scalar affine compiler.",
                "resolved": True,
                "resolution": "False. The S6 masks form an affine plane while component effects split the common fiber into unequal partial supports.",
            },
            {
                "objection": "Globally distinct source partitions prevent matrix recoupling traffic.",
                "resolved": True,
                "resolution": "False at n=6: every source partition is distinct and cross-child component effects still fail to commute.",
            },
            {
                "objection": "Commuting short metrics make the entire child embedding scalar.",
                "resolved": True,
                "resolution": "The S6 short metrics commute, but their mask-resolved component effects do not. Endpoint diagonalization and support routing are separate gates.",
            },
            {
                "objection": "A finite partial-support counterexample kills the collective PGM route.",
                "resolved": False,
                "resolution": "Only a positive frame-weighted asymptotic mass theorem or a uniform compiler/no-go can decide that.",
            },
        ],
        headline_metrics={
            "gram_only_child_embedding_reconstruction_theorem_count": int(failures == 0),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "scalar_affine_positive_control_count": int(
                scalar.scalar_flat_affine_child_embedding_certificate
            ),
            "natural_collision_free_scalar_affine_falsifier_count": int(natural_falsifier),
            "natural_partial_support_common_dimension": partial.common_span_dimension,
            "natural_partial_support_maximum_full_scalar_residual": partial.maximum_component_full_fiber_scalar_residual,
            "natural_partial_support_cross_effect_commutator_norm": partial.maximum_cross_child_effect_commutator_norm,
            "matrix_partial_support_gpe_compiler_count": 0,
            "positive_native_mass_partial_support_theorem_count": 0,
            "companion_direct_s6_source_mass_no_go_count": 1,
            "recursive_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "gram_only_normalized_child_embedding_reconstruction_proved": failures == 0,
            "selected_w3_scalar_affine_control_passes": scalar.scalar_flat_affine_child_embedding_certificate,
            "collision_free_affine_support_suffices_for_scalar_fibers": False,
            "natural_s6_requires_matrix_partial_support": natural_falsifier,
            "direct_s6_trivial_sign_mechanism_has_vanishing_natural_mass": True,
            "globally_distinct_sources_prevent_matrix_recoupling": False,
            "matrix_partial_support_gpe_compiler_proved": False,
            "positive_native_mass_partial_support_obstruction_proved": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A natural collision-free affine node already falsifies scalar "
                "fibers, but its trivial/sign mechanism is factorially rare. The "
                "surviving risk is matrix support generated entirely by typical "
                "high-dimensional sources; its GPE compiler and mass are open."
            ),
        },
        status=(
            "universal-scalar-affine-falsified-direct-s6-mass-negligible-high-dimensional-route-open"
            if verified
            else "partial-support-child-embedding-control-failure"
        ),
        summary=(
            "Reconstructed child embeddings from sparse leaf Grams and used a "
            "globally distinct S6 affine node to falsify the scalar-fiber "
            "compiler, replacing it with a matrix partial-support target."
        ),
        falsifiers_triggered=[
            "Affine orientation support does not imply scalar coefficient fibers.",
            "Global source distinctness does not remove noncommuting recoupling effects.",
            "Commuting short metrics do not imply commuting mask-resolved component effects.",
            "The finite W3/W5 scalar affine compiler cannot be extrapolated as the all-depth mechanism.",
            "The direct S6 trivial/sign pattern cannot supply positive asymptotic natural mass.",
        ],
    )


def write_partial_support_child_embedding_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_partial_support_child_embedding())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_partial_support_child_embedding_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
