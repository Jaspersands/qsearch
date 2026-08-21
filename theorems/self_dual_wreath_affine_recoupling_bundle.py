"""Flat affine recoupling bundles behind coefficient-balanced merges.

Suppose a child overlap ``K`` has canonical minimum-norm leaf maps

    D_e = E_e A^+ U

whose nonzero effects are uniform scalars ``D_e^*D_e=w I_K``.  Then
``V_e=D_e/sqrt(w)`` is an isometry from one common fiber ``K`` into the
coefficient block at mask ``e``.  For active masks ``e,f`` define

    T_(f,e) = V_f V_e^*.

These are partial isometries and form a flat transport system:

    T_(g,f) T_(f,e) = T_(g,e)

on the source fiber.  If the active masks form an affine space and each child
contains an equal affine half, its normalized coefficient map is

    |C_X|^(-1/2) sum_(e in C_X) |e> V_e.                 (1)

Choose one affine origin.  Equation (1) can be compiled from a uniform affine
superposition and transports along a basis of affine generators, provided
those generator transports have efficient representation-theoretic circuits.

This separates an algebraic fact from the real algorithmic obligation.  Flat
transport is automatic once the canonical fiber maps exist; it does not make
them efficient.  The selected ``W_3`` control has nonidentity internal fiber
maps, so a mask XOR alone cannot implement the transfer.  The companion GPE
pair-polar theorem and finite pair-path network now compile the selected W3/W5
generator transports without an inverse-correlation penalty.  What remains is
an all-n structured-fiber theorem and a compact uniform generator SELECT, not
a finite Racah matrix.  A repeated-label balanced control has a uniform
six-mask support that is not affine, showing that half-balance alone does not
imply the affine-bundle architecture.  More decisively, the companion
partial-support theorem gives a globally source-distinct S6 affine plane whose
component effects are nonscalar and noncommuting.  The scalar affine-bundle
hypothesis is therefore falsified as a universal collision-free theorem, not
merely unproved.
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
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_affine_recoupling_bundle.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RECOUPLING-BUNDLE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AffineRecouplingBundleControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    intersection_dimension: int
    active_orientation_masks: tuple[int, ...]
    active_left_mask_count: int
    active_right_mask_count: int
    active_support_affine_dimension: int | None
    affine_origin_mask: int | None
    affine_generator_masks: tuple[int, ...]
    common_component_weight: float | None
    left_metric_scale: float
    right_metric_scale: float
    child_metric_equality_residual: float
    maximum_component_scalar_residual: float
    maximum_component_weight_uniformity_residual: float
    maximum_fiber_isometry_residual: float
    maximum_transport_initial_projection_residual: float
    maximum_transport_final_projection_residual: float
    maximum_transport_cocycle_residual: float
    maximum_generator_fiber_map_difference: float
    generator_edge_transport_count: int
    coefficient_support_is_affine: bool
    equal_affine_child_halves: bool
    exact_flat_fiber_transport_verified: bool
    affine_recoupling_bundle_certificate: bool
    simple_mask_relabeling_suffices: bool
    status: str


@dataclass(frozen=True)
class AffineRecouplingScalingRecord:
    n: int
    information_threshold_copy_count: int
    maximum_affine_bundle_dimension: int
    flat_transport_given_fiber_maps: bool
    all_n_collision_free_affine_bundle_decomposition_proved: bool
    generator_transports_identified_as_racah_maps: bool
    polynomial_controlled_generator_transport_circuit_proved: bool
    hierarchical_orientation_polar_proved: bool
    status: str


@dataclass(frozen=True)
class AffineRecouplingBundleReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[AffineRecouplingBundleControl]
    scaling_records: list[AffineRecouplingScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _binary_rank(vectors: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        reduced = vector
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return len(pivots)


def affine_basis(
    elements: tuple[int, ...],
    bit_count: int,
) -> tuple[int, tuple[int, ...]]:
    if not is_affine_set(elements, bit_count):
        raise ValueError("an affine mask set is required")
    origin = min(elements)
    generators: list[int] = []
    for difference in sorted(element ^ origin for element in elements):
        if difference and _binary_rank(tuple((*generators, difference))) > len(
            generators
        ):
            generators.append(difference)
    if 1 << len(generators) != len(elements):
        raise ArithmeticError("failed to recover the affine support dimension")
    return origin, tuple(generators)


def audit_affine_recoupling_bundle(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> AffineRecouplingBundleControl:
    if len(left_masks) != len(right_masks) or not left_masks:
        raise ValueError("equal nonempty child mask sets are required")
    projectors, _, _ = _reduced_projector_family(
        target,
        labels,
        tolerance,
    )
    dimension = len(projectors[0])
    zero = np.zeros((dimension, dimension), dtype=complex)
    left = sum((projectors[mask] for mask in left_masks), zero.copy())
    right = sum((projectors[mask] for mask in right_masks), zero.copy())
    core = _range_intersection_basis(
        _support_basis(left, tolerance),
        _support_basis(right, tolerance),
        tolerance,
    )
    rank = core.shape[1]
    if not rank:
        raise ValueError("the selected merge has no child-range intersection")

    identity = np.eye(rank)
    fiber_maps: dict[int, np.ndarray] = {}
    weights: dict[int, float] = {}
    scalar_residual = 0.0
    metric_scales = []
    metrics = []
    for masks, frame in ((left_masks, left), (right_masks, right)):
        inverse = _psd_pseudoinverse(frame, tolerance)
        metric = core.conj().T @ inverse @ core
        metrics.append(metric)
        metric_scales.append(float(np.trace(metric).real / rank))
        for mask in masks:
            mapping = projectors[mask] @ inverse @ core
            effect = mapping.conj().T @ mapping
            weight = float(np.trace(effect).real / rank)
            weights[mask] = weight
            scalar_residual = max(
                scalar_residual,
                float(np.linalg.norm(effect - weight * identity, ord=2)),
            )
            if weight > 100 * tolerance:
                fiber_maps[mask] = mapping / math.sqrt(weight)

    active = tuple(sorted(fiber_maps))
    active_weights = tuple(weights[mask] for mask in active)
    uniformity = (
        max(active_weights) - min(active_weights)
        if active_weights
        else math.inf
    )
    bit_count = (len(projectors) - 1).bit_length()
    affine = bool(active) and is_affine_set(active, bit_count)
    if affine:
        origin, generators = affine_basis(active, bit_count)
        affine_dimension: int | None = len(generators)
    else:
        origin = None
        generators = ()
        affine_dimension = None

    left_active = tuple(mask for mask in left_masks if mask in fiber_maps)
    right_active = tuple(mask for mask in right_masks if mask in fiber_maps)
    equal_halves = bool(
        affine
        and left_active
        and len(left_active) == len(right_active)
        and len(left_active) + len(right_active) == len(active)
    )
    isometry_residual = max(
        (
            float(
                np.linalg.norm(
                    mapping.conj().T @ mapping - identity,
                    ord=2,
                )
            )
            for mapping in fiber_maps.values()
        ),
        default=math.inf,
    )

    transports: dict[tuple[int, int], np.ndarray] = {
        (target_mask, source_mask): (
            fiber_maps[target_mask] @ fiber_maps[source_mask].conj().T
        )
        for source_mask in active
        for target_mask in active
    }
    initial_residual = 0.0
    final_residual = 0.0
    for (target_mask, source_mask), transport in transports.items():
        source_projection = (
            fiber_maps[source_mask] @ fiber_maps[source_mask].conj().T
        )
        target_projection = (
            fiber_maps[target_mask] @ fiber_maps[target_mask].conj().T
        )
        initial_residual = max(
            initial_residual,
            float(
                np.linalg.norm(
                    transport.conj().T @ transport - source_projection,
                    ord=2,
                )
            ),
        )
        final_residual = max(
            final_residual,
            float(
                np.linalg.norm(
                    transport @ transport.conj().T - target_projection,
                    ord=2,
                )
            ),
        )
    cocycle_residual = max(
        (
            float(
                np.linalg.norm(
                    transports[(third, second)]
                    @ transports[(second, first)]
                    - transports[(third, first)],
                    ord=2,
                )
            )
            for first in active
            for second in active
            for third in active
        ),
        default=math.inf,
    )

    generator_differences = []
    generator_edge_count = 0
    if affine:
        for generator in generators:
            for mask in active:
                partner = mask ^ generator
                if mask < partner and partner in fiber_maps:
                    generator_edge_count += 1
                    generator_differences.append(
                        float(
                            np.linalg.norm(
                                fiber_maps[mask] - fiber_maps[partner],
                                ord=2,
                            )
                        )
                    )
    maximum_fiber_difference = max(generator_differences, default=0.0)
    flat = bool(
        isometry_residual <= 100 * tolerance
        and initial_residual <= 100 * tolerance
        and final_residual <= 100 * tolerance
        and cocycle_residual <= 100 * tolerance
    )
    certificate = bool(
        affine
        and equal_halves
        and scalar_residual <= 100 * tolerance
        and uniformity <= 100 * tolerance
        and abs(metric_scales[0] - metric_scales[1]) <= 100 * tolerance
        and flat
    )
    simple_relabel = bool(
        certificate and maximum_fiber_difference <= 100 * tolerance
    )
    return AffineRecouplingBundleControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        intersection_dimension=rank,
        active_orientation_masks=active,
        active_left_mask_count=len(left_active),
        active_right_mask_count=len(right_active),
        active_support_affine_dimension=affine_dimension,
        affine_origin_mask=origin,
        affine_generator_masks=generators,
        common_component_weight=(
            sum(active_weights) / len(active_weights) if active_weights else None
        ),
        left_metric_scale=metric_scales[0],
        right_metric_scale=metric_scales[1],
        child_metric_equality_residual=float(
            np.linalg.norm(metrics[0] - metrics[1], ord=2)
        ),
        maximum_component_scalar_residual=scalar_residual,
        maximum_component_weight_uniformity_residual=uniformity,
        maximum_fiber_isometry_residual=isometry_residual,
        maximum_transport_initial_projection_residual=initial_residual,
        maximum_transport_final_projection_residual=final_residual,
        maximum_transport_cocycle_residual=cocycle_residual,
        maximum_generator_fiber_map_difference=maximum_fiber_difference,
        generator_edge_transport_count=generator_edge_count,
        coefficient_support_is_affine=affine,
        equal_affine_child_halves=equal_halves,
        exact_flat_fiber_transport_verified=flat,
        affine_recoupling_bundle_certificate=certificate,
        simple_mask_relabeling_suffices=simple_relabel,
        status=(
            "exact-flat-affine-recoupling-bundle"
            if certificate
            else "flat-fibers-nonaffine-or-nonuniform-support"
            if flat
            else "affine-recoupling-bundle-validation-failure"
        ),
    )


def affine_recoupling_scaling_record(n: int) -> AffineRecouplingScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return AffineRecouplingScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        maximum_affine_bundle_dimension=copies,
        flat_transport_given_fiber_maps=True,
        all_n_collision_free_affine_bundle_decomposition_proved=False,
        generator_transports_identified_as_racah_maps=False,
        polynomial_controlled_generator_transport_circuit_proved=False,
        hierarchical_orientation_polar_proved=False,
        status="flat-bundle-identity-explicit-generator-recoupling-open",
    )


def run_affine_recoupling_bundle() -> AffineRecouplingBundleReport:
    distinct: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    repeated: tuple[Label, ...] = (((3,), (2, 1)),) * 3
    controls = [
        audit_affine_recoupling_bundle(
            "W3-DISTINCT-AFFINE-PLANE",
            3,
            (2, 1),
            distinct,
            (0, 2),
            (5, 7),
        ),
        audit_affine_recoupling_bundle(
            "W3-DISTINCT-SCALED-AFFINE-PLANE",
            3,
            (2, 1),
            distinct,
            (0, 5),
            (2, 7),
        ),
        audit_affine_recoupling_bundle(
            "W5-ISOLATED-AFFINE-LINE",
            5,
            (3, 2),
            _w5_probe_labels()[0],
            (0, 1, 2, 3),
            (4, 5, 6, 7),
        ),
        audit_affine_recoupling_bundle(
            "W3-REPEATED-BALANCED-NONAFFINE-FALSIFIER",
            3,
            (2, 1),
            repeated,
            (0, 3, 5, 6),
            (1, 2, 4, 7),
        ),
    ]
    scaling = [
        affine_recoupling_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    positive = controls[:3]
    nonaffine = controls[3]
    validation_failures = sum(
        not row.exact_flat_fiber_transport_verified for row in positive
    )
    finite_affine_signal = all(
        row.affine_recoupling_bundle_certificate for row in positive
    )
    nonaffine_falsifier = bool(
        nonaffine.child_metric_equality_residual <= 1e-7
        and not nonaffine.coefficient_support_is_affine
        and not nonaffine.affine_recoupling_bundle_certificate
    )
    nontrivial_internal = any(
        row.maximum_generator_fiber_map_difference > 1e-6
        for row in positive
        if row.n == 3
    )
    verified = validation_failures == 0
    return AffineRecouplingBundleReport(
        created_at=utc_now(),
        theorem_contract={
            "fiber_isometries": (
                "Uniform scalar component effects define normalized isometries "
                "V_e from one common overlap fiber."
            ),
            "flat_transport": (
                "T_(f,e)=V_f V_e^* is a partial isometry and obeys the exact "
                "transport cocycle on fiber images."
            ),
            "affine_compilation_normal_form": (
                "An affine active support reduces leaf preparation to Hadamards "
                "on affine coordinates plus controlled generator transports."
            ),
            "nontrivial_internal_transport": (
                "W3 generator fibers differ by constant operator norm, so mask "
                "XOR without internal recoupling cannot implement the transfer."
            ),
            "scope": (
                "The canonical V_e still contain child pseudoinverses. The "
                "companion recursive-node theorem compiles the selected finite "
                "fibers through GPE pair paths. The companion S6 partial-support "
                "control falsifies universal scalar fibers; a matrix-support and "
                "uniform generator-SELECT theorem is now required."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "flat_affine_fiber_transport_theorem",
                "resolved": verified,
                "resolution": (
                    "Isometric fibers make the partial-isometry and cocycle "
                    "identities algebraic; all finite controls validate them."
                ),
            },
            {
                "obligation": "finite_label_simple_affine_bundle_signal",
                "resolved": finite_affine_signal,
                "resolution": (
                    "Both W3 affine-plane controls and the W5 anchor-line control "
                    "satisfy the complete bundle certificate."
                ),
            },
            {
                "obligation": "all_n_affine_bundle_decomposition",
                "resolved": True,
                "resolution": (
                    "Rejected by the companion globally source-distinct S6 "
                    "affine-plane control, whose component effects are nonscalar "
                    "partial supports with noncommuting cross-child effects."
                ),
            },
            {
                "obligation": "selected_finite_generator_recoupling_circuit",
                "resolved": True,
                "resolution": (
                    "The companion pair-path and direct-GPE theorems compile "
                    "all three positive W3/W5 controls in constant size."
                ),
            },
            {
                "obligation": "all_n_uniform_generator_recoupling_circuit",
                "resolved": False,
                "resolution": (
                    "No compact reversible SELECT generates compatible paths and "
                    "gauges for exponentially many growing-mask fibers."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Flat transport itself supplies an efficient circuit.",
                "resolved": True,
                "resolution": (
                    "Flatness alone is insufficient. The selected finite controls "
                    "need the separate GPE pair-path compiler; the all-n implication "
                    "remains false without uniform SELECT."
                ),
            },
            {
                "objection": "Mask translation implements every affine bundle.",
                "resolved": True,
                "resolution": (
                    "W3 generator fiber maps differ by constant norm, requiring "
                    "nontrivial internal transport."
                ),
            },
            {
                "objection": "Half-balance implies affine support.",
                "resolved": True,
                "resolution": (
                    "The repeated-label six-mask control has equal child metrics, "
                    "but its component effects are nonscalar and its support is "
                    "not affine."
                ),
            },
            {
                "objection": "External label distinctness guarantees easy Racah maps.",
                "resolved": False,
                "resolution": (
                    "Internal Kronecker multiplicities can grow despite distinct "
                    "external partitions."
                ),
            },
        ],
        headline_metrics={
            "flat_fiber_transport_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_flat_transport_validation_failure_count": validation_failures,
            "label_simple_affine_bundle_control_count": sum(
                row.affine_recoupling_bundle_certificate for row in positive
            ),
            "balanced_nonaffine_bundle_falsifier_count": int(nonaffine_falsifier),
            "nontrivial_internal_transport_control_count": int(
                nontrivial_internal
            ),
            "maximum_w3_generator_fiber_difference": max(
                row.maximum_generator_fiber_map_difference
                for row in positive
                if row.n == 3
            ),
            "all_n_affine_bundle_decomposition_theorem_count": 0,
            "natural_collision_free_scalar_affine_falsifier_count": 1,
            "explicit_generator_racah_formula_count": 0,
            "companion_finite_gpe_generator_compiler_count": 3,
            "polynomial_controlled_generator_transport_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "flat_affine_fiber_transport_proved": verified,
            "finite_label_simple_affine_bundle_signal": finite_affine_signal,
            "balanced_nonaffine_support_falsifier_present": nonaffine_falsifier,
            "natural_collision_free_scalar_affine_falsifier_present": True,
            "simple_mask_relabeling_falsified_for_w3": nontrivial_internal,
            "selected_finite_generator_transports_compiled_by_gpe": True,
            "all_n_collision_free_affine_bundle_decomposition_proved": False,
            "generator_transports_identified_as_racah_maps": False,
            "polynomial_controlled_generator_transport_circuit_proved": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Selected finite internal transports now compile through GPE pair "
                "paths, but a natural S6 node falsifies scalar fibers. The all-n "
                "target is matrix partial support plus uniform coherent SELECT."
            ),
        },
        status=(
            "finite-flat-affine-gpe-compiled-universal-scalar-fibers-falsified"
            if verified and finite_affine_signal and nonaffine_falsifier
            else "affine-recoupling-bundle-validation-failure"
        ),
        summary=(
            "Converted uniform affine coefficient support into a flat transport "
            "bundle; companion GPE pair paths compile the selected finite fibers, "
            "while the companion natural S6 control forces a matrix partial-"
            "support replacement at scale."
        ),
        falsifiers_triggered=[
            (
                "Affine mask relabeling alone cannot move the W3 internal fibers."
            ),
            (
                "Balanced coefficient metrics do not force affine leaf support."
            ),
            "Formal flatness alone is not evidence of an all-n efficient recoupling circuit.",
            "A globally source-distinct S6 affine plane falsifies universal scalar coefficient fibers.",
        ],
    )


def write_affine_recoupling_bundle_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RECOUPLING-BUNDLE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_affine_recoupling_bundle())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_affine_recoupling_bundle_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
