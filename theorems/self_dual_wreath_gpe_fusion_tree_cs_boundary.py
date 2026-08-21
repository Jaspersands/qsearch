"""Recursive GPE compiles recoupling unitaries, not their CS subblock polar.

Coherent generalized phase estimation (GPE) on a representation

    R = direct_sum_alpha M_alpha tensor V_alpha

exports the irrep label and a clean carrier row while leaving the unknown
multiplicity state untouched and pairing the Fourier column with the residual
carrier in a fixed maximally entangled state.  This output can be fused with a
new representation factor.  Repeating the construction along a binary tree
gives a polynomial coherent fusion-tree transform whenever the group QFT and
controlled factor actions are efficient.  Uncomputing one tree and computing
another implements the associated Racah/recoupling unitary without naming a
classical multiplicity basis.

This positive capability does not by itself implement the connected
orientation polar.  The ``B``-fixed and ``D``-fixed spaces select rectangular
subspaces of two decompositions.  If ``U_T`` is the full fusion-tree
recoupling and ``P,Q`` select those fixed labels, their overlap is the
subblock

    C = Q U_T P.                                           (1)

The desired operation is ``polar(C)``, not ``U_T``.  Pre- and post-composing
(1) with fusion-tree unitaries preserves every singular value.  A one-crossing
architecture can equal the polar only when all active singular values are
already one, or when an independently known direct partial isometry replaces
the subblock.

The solved pair-GPE transport is exactly the exceptional direct case: on each
active carrier block ``C=c U`` with one scalar ``c=1/d`` and a known carrier
reassociation ``U``.  GPE implements ``U`` directly and ignores ``c``.  At the
first higher orientation controls, the fixed-space subblock has multiple
active singular levels.  No single carrier reassociation can discard them.

Multiple alternating projections/reflections or generic QSVT can polarize
(1), but their cost is inverse in the smallest retained principal cosine.  In
the natural flat benchmark the normalized overlap amplitude is
``Theta(|S_n|^-1/2)``.  Recursive GPE does not alter that generic query
boundary unless it also supplies a direct CS singular-vector pairing.

The remaining positive target is therefore precise: find fusion labels or a
holonomy/F-move network in which the occupied rectangular Racah subblock has
an efficiently computable direct polar, including its output gauge.  This
module does not rule that out and proves no arbitrary-circuit lower bound.
No complete orientation polar, decoder, classical separation, or speedup is
claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_gpe_fusion_tree_cs_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GPE-FUSION-TREE-CS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class FusionTreeSubblockControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_count: int
    base_dimension: int
    fixed_space_cross_map_dimension: tuple[int, int]
    active_singular_value_count: int
    distinct_active_singular_value_count: int
    minimum_active_singular_value: float
    maximum_active_singular_value: float
    active_singular_condition_ratio: float
    minimum_one_crossing_unitary_only_polar_distance: float
    active_subblock_is_scalar_times_partial_isometry: bool
    active_subblock_already_partial_isometry: bool
    exact_subblock_polar_identity_verified: bool
    status: str


@dataclass(frozen=True)
class GpeFusionTreeScalingRecord:
    n: int
    copy_count: int
    tensor_factor_count: int
    binary_fusion_internal_node_count: int
    gpe_call_count_per_tree_upper_bound: int
    gpe_call_count_for_tree_change_upper_bound: int
    group_ancilla_qubit_count_upper_bound: int
    coherent_opaque_multiplicity_preserved: bool
    full_tree_recoupling_unitary_polynomial: bool
    flat_normalized_subblock_singular_amplitude_log2: float
    generic_reflection_query_scale_log2: float
    direct_pair_reassociation_available: bool
    direct_global_rectangular_cs_polar_available: bool
    status: str


@dataclass(frozen=True)
class GpeFusionTreeCsTheorem:
    gpe_isometry: str
    recursive_tree: str
    tree_change: str
    fixed_space_subblock: str
    unitary_only_boundary: str
    pair_exception: str
    global_target: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class GpeFusionTreeCsReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: GpeFusionTreeCsTheorem
    finite_controls: list[FusionTreeSubblockControl]
    scaling_records: list[GpeFusionTreeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse_square_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    inverse = np.zeros_like(values)
    inverse[values > tolerance] = 1.0 / np.sqrt(values[values > tolerance])
    return (vectors * inverse) @ vectors.conj().T


def _polar(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, right_star = np.linalg.svd(matrix, full_matrices=False)
    retained = singular_values > tolerance
    return left[:, retained] @ right_star[retained, :]


def audit_fusion_tree_subblock(
    control_id: str,
    target_partition: Partition,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> FusionTreeSubblockControl:
    if not labels:
        raise ValueError("at least one label pair is required")
    projectors = tuple(
        orientation_invariant_projector(target_partition, labels, orientation)
        for orientation in range(1 << len(labels))
    )
    dimension = projectors[0].shape[0]
    orientation_count = len(projectors)
    branch_embedding = np.vstack(
        tuple(np.eye(dimension) for _ in range(orientation_count))
    ) / math.sqrt(orientation_count)
    diagonal_projector = np.zeros(
        (orientation_count * dimension, orientation_count * dimension),
        dtype=complex,
    )
    for orientation, projector in enumerate(projectors):
        start = orientation * dimension
        diagonal_projector[
            start : start + dimension,
            start : start + dimension,
        ] = projector
    cross_map = diagonal_projector @ branch_embedding
    singular_values = np.linalg.svd(cross_map, compute_uv=False)
    active = singular_values[singular_values > tolerance]
    rounded = {round(float(value), 10) for value in active}
    frame = sum(projectors, np.zeros_like(projectors[0]))
    predicted_polar = np.vstack(projectors) @ _inverse_square_root(frame, tolerance)
    exact_polar = _polar(cross_map, tolerance)
    polar_residual = float(np.linalg.norm(exact_polar - predicted_polar, ord=2))
    scalar = bool(len(active) and np.max(active) - np.min(active) <= tolerance)
    already = bool(len(active) and np.max(np.abs(active - 1.0)) <= tolerance)
    unitary_distance = max(abs(1.0 - float(value)) for value in active)
    return FusionTreeSubblockControl(
        control_id=control_id,
        n=sum(target_partition),
        target_partition=target_partition,
        labels=labels,
        orientation_count=orientation_count,
        base_dimension=dimension,
        fixed_space_cross_map_dimension=cross_map.shape,
        active_singular_value_count=len(active),
        distinct_active_singular_value_count=len(rounded),
        minimum_active_singular_value=float(np.min(active)),
        maximum_active_singular_value=float(np.max(active)),
        active_singular_condition_ratio=float(np.max(active) / np.min(active)),
        minimum_one_crossing_unitary_only_polar_distance=unitary_distance,
        active_subblock_is_scalar_times_partial_isometry=scalar,
        active_subblock_already_partial_isometry=already,
        exact_subblock_polar_identity_verified=polar_residual <= 100 * tolerance,
        status=(
            "scalar-pair-subblock-direct-reassociation-possible"
            if scalar
            else "matrix-valued-rectangular-racah-subblock-direct-cs-polar-open"
        ),
    )


def gpe_fusion_tree_scaling_record(n: int) -> GpeFusionTreeScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    group_order_log2 = math.lgamma(n + 1) / math.log(2)
    copy_count = math.ceil(group_order_log2) + 2
    factors = 2 * copy_count + 1
    internal = factors - 1
    return GpeFusionTreeScalingRecord(
        n=n,
        copy_count=copy_count,
        tensor_factor_count=factors,
        binary_fusion_internal_node_count=internal,
        gpe_call_count_per_tree_upper_bound=internal,
        gpe_call_count_for_tree_change_upper_bound=2 * internal,
        group_ancilla_qubit_count_upper_bound=2 * internal * math.ceil(group_order_log2),
        coherent_opaque_multiplicity_preserved=True,
        full_tree_recoupling_unitary_polynomial=True,
        flat_normalized_subblock_singular_amplitude_log2=-0.5 * group_order_log2,
        generic_reflection_query_scale_log2=0.5 * group_order_log2,
        direct_pair_reassociation_available=True,
        direct_global_rectangular_cs_polar_available=False,
        status="gpe-tree-recoupling-polynomial-rectangular-cs-polar-open",
    )


def run_gpe_fusion_tree_cs_boundary() -> GpeFusionTreeCsReport:
    controls = [
        audit_fusion_tree_subblock(
            "S3-SCALAR-PAIR",
            (2, 1),
            (((3,), (2, 1)),),
        ),
        audit_fusion_tree_subblock(
            "S3-MATRIX-TWO-PAIR",
            (2, 1),
            (
                ((3,), (2, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        audit_fusion_tree_subblock(
            "S4-SCALAR-TWO-PAIR-CONTROL",
            (3, 1),
            (
                ((4,), (3, 1)),
                ((2, 2), (2, 1, 1)),
            ),
        ),
    ]
    scaling = [
        gpe_fusion_tree_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(not row.exact_subblock_polar_identity_verified for row in controls)
    scalar_controls = sum(row.active_subblock_is_scalar_times_partial_isometry for row in controls)
    matrix_controls = len(controls) - scalar_controls
    verified = failures == 0 and scalar_controls >= 1 and matrix_controls >= 1
    theorem = GpeFusionTreeCsTheorem(
        gpe_isometry=(
            "Coherent GPE exports irrep and carrier row, leaves multiplicity "
            "untouched, and parks column/residual carrier in a fixed EPR state."
        ),
        recursive_tree=(
            "Exported carrier rows can be fused recursively, giving a polynomial "
            "coherent association-tree transform."
        ),
        tree_change=(
            "Uncompute one tree and compute another to implement the full Racah "
            "recoupling unitary without naming multiplicity coordinates."
        ),
        fixed_space_subblock="The connected overlap is C=Q U_T P, a rectangular Racah subblock.",
        unitary_only_boundary=(
            "Tree unitaries before/after C preserve its singular values and do "
            "not implement polar(C) for a non-isometric subblock."
        ),
        pair_exception=(
            "Pair GPE has C=cU on each active carrier and implements the known U directly."
        ),
        global_target=(
            "Find a direct polar of the occupied rectangular subblock, or a "
            "holonomy network proved to equal it with the physical output gauge."
        ),
        scope=(
            "No global CS singular-vector pairing, complete orientation polar, "
            "classical separation, or speedup."
        ),
        theorem_verified=verified,
        status=(
            "gpe-fusion-trees-compile-recoupling-rectangular-cs-polar-open"
            if verified
            else "gpe-fusion-tree-cs-boundary-control-failure"
        ),
    )
    return GpeFusionTreeCsReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "compile_recursive_gpe_fusion_tree_transform",
                "resolved": True,
                "resolution": (
                    "Every internal node uses one coherent GPE on the current "
                    "exported carrier and next factor; opaque multiplicity is spectator."
                ),
            },
            {
                "obligation": "compile_full_fusion_tree_recoupling_unitary",
                "resolved": True,
                "resolution": (
                    "Compose one tree inverse with the other tree forward; the "
                    "number of GPE calls is linear in the tensor-factor count."
                ),
            },
            {
                "obligation": "separate_full_recoupling_from_fixed_space_cs_polar",
                "resolved": verified,
                "resolution": (
                    "The exact controls recover the orientation polar as polar(C); "
                    "the higher S3 subblock has multiple singular levels."
                ),
            },
            {
                "obligation": "compile_direct_rectangular_racah_subblock_polar",
                "resolved": False,
                "resolution": (
                    "Need singular-vector pairing or a direct higher-order partial "
                    "isometry; tree unitaries and fixed-label projection are insufficient."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "GPE is only weak Fourier sampling and cannot recouple opaque multiplicity.",
                "resolved": True,
                "resolution": (
                    "False. Kept coherent, its row output can be recursively fused; "
                    "tree changes implement Racah unitaries implicitly."
                ),
            },
            {
                "objection": "An efficient full Racah unitary automatically gives the fixed-space polar.",
                "resolved": True,
                "resolution": (
                    "False. The polar is that unitary's rectangular fixed-label "
                    "subblock with all active singular values replaced by one."
                ),
            },
            {
                "objection": "The pair-GPE success proves every higher subblock has a direct reassociation.",
                "resolved": True,
                "resolution": (
                    "False. Pair blocks are scalar times partial isometries; the "
                    "two-pair S3 control has multiple active singular levels."
                ),
            },
            {
                "objection": "This rules out all GPE-based global circuits.",
                "resolved": True,
                "resolution": (
                    "Not proved. A GPE-derived direct CS basis, multi-pass holonomy "
                    "network, or structured singular-vector pairing remains open."
                ),
            },
        ],
        headline_metrics={
            "recursive_gpe_fusion_tree_compiler_count": 1,
            "full_gpe_tree_recoupling_unitary_compiler_count": 1,
            "rectangular_subblock_cs_boundary_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "scalar_direct_reassociation_control_count": scalar_controls,
            "matrix_valued_subblock_control_count": matrix_controls,
            "minimum_finite_one_crossing_polar_distance": min(
                row.minimum_one_crossing_unitary_only_polar_distance
                for row in controls
            ),
            "scaling_record_count": len(scaling),
            "direct_global_rectangular_cs_polar_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "recursive_gpe_fusion_tree_transform_polynomial": True,
            "full_gpe_tree_recoupling_unitary_polynomial": True,
            "connected_fixed_space_overlap_is_rectangular_racah_subblock": verified,
            "pair_gpe_direct_reassociation_available": scalar_controls >= 1,
            "full_recoupling_unitary_automatically_compiles_subblock_polar": False,
            "direct_global_rectangular_cs_polar_compiled": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Recursive GPE can compile full fusion-tree recouplings, but the "
                "orientation gate is the polar of a non-isometric rectangular "
                "fixed-label subblock. Its direct CS pairing remains open."
            ),
        },
        status=theorem.status,
        summary=(
            "Upgraded GPE from pair transport to full coherent fusion-tree "
            "recoupling, then proved that the orientation compiler remains the "
            "distinct rectangular Racah-subblock polar problem."
        ),
        falsifiers_triggered=[
            "GPE is capable of coherent fusion-tree recoupling; lack of named multiplicity coordinates is not the blocker.",
            "A full Racah recoupling unitary is not the polar of its fixed-space rectangular subblock.",
            "The pair scalar-reassociation mechanism does not extend automatically to the first matrix-valued higher block.",
        ],
    )


def write_gpe_fusion_tree_cs_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_gpe_fusion_tree_cs_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_gpe_fusion_tree_cs_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
