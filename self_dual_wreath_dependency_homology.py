"""Pair-common quotient and emergent cross-dependency homology.

For a balanced child merge, let W be the cross-synthesis dependency space
after quotienting each child's internal syzygies.  Every exact common range of
a leaf pair ``(e,f)`` supplies a two-leaf relation in the raw cross kernel.
Project that relation onto W and let ``W_pair`` be the span of all such pair
classes.  Define the finite dependency homology

    H_em = W / W_pair,                                      (1)

represented by the orthogonal complement of ``W_pair`` in W.

This quotient distinguishes exact trivial/sign pair-common structure from
genuinely many-leaf emergence.  The label-distinct W3 plane has no pair-common
relations and a two-dimensional ``H_em``; its neutral emergent class is the
sharp norm-one case of the weighted carrier graph.  Isolated W5 and screened
S6 common channels are pair-generated.  Pair generation alone does not prove
balance: a globally distinct S6 affine plane has a 34-dimensional
pair-generated intersection with exact nonhalf channels.  The
left-minus-right grading is therefore audited on ``W_pair``, ``H_em``, and
their cross block.

The construction is basis-independent and uses only the leaf block Gram.  It
is not yet an all-n representation-ring chain complex: explicit pair-common
intertwiners and their higher relations still require recoupling data.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_orientation_pair_angle_spectrum import (
    exact_pair_principal_angle_spectrum,
)
from self_dual_wreath_shorted_overlap_balance import unique_affine_flag_merges
from self_dual_wreath_sparse_invariant_dependency import (
    orientation_invariant_range_basis,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_dependency_homology.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class DependencyHomologyNode:
    node_id: str
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    active_left_orientation_masks: tuple[int, ...]
    active_right_orientation_masks: tuple[int, ...]
    cross_dependency_dimension: int
    exact_pair_common_edge_count: int
    exact_pair_common_dimension_sum: int
    pair_dependency_class_dimension: int
    emergent_dependency_homology_dimension: int
    pair_class_overlap_dimension: int
    full_grading_neutrality_residual: float
    pair_class_grading_residual: float
    emergent_class_grading_residual: float
    pair_emergent_grading_coupling_residual: float
    fractional_eigenvalues: tuple[float, ...]
    maximum_fractional_half_residual: float
    pair_classes_exhaust_cross_dependencies: bool
    emergent_dependency_present: bool
    pair_classes_totally_neutral: bool
    emergent_classes_totally_neutral: bool
    exact_dependency_homology_audit: bool
    status: str


@dataclass(frozen=True)
class DependencyHomologyControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    globally_distinct_source_partitions: bool
    pairwise_distinct_physical_labels: bool
    audited_fractional_merge_count: int
    pair_generated_merge_count: int
    emergent_merge_count: int
    nonneutral_merge_count: int
    maximum_cross_dependency_dimension: int
    maximum_pair_dependency_class_dimension: int
    maximum_emergent_homology_dimension: int
    maximum_full_grading_neutrality_residual: float
    exact_homology_audit_failure_count: int
    records: list[DependencyHomologyNode]
    status: str


@dataclass(frozen=True)
class DependencyHomologyReport:
    created_at: str
    quotient_contract: dict[str, Any]
    controls: list[DependencyHomologyControl]
    scaling_records: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    return vectors[:, values > tolerance]


def _null_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("dependency Gram is not positive semidefinite")
    return vectors[:, values <= 100 * tolerance]


def _dependency_basis_from_blocks(
    left: np.ndarray,
    right: np.ndarray,
    cross: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    left_support = _support_basis(left, tolerance)
    right_support = _support_basis(right, tolerance)
    quotient = np.zeros(
        (
            left.shape[0] + right.shape[0],
            left_support.shape[1] + right_support.shape[1],
        ),
        dtype=complex,
    )
    quotient[: left.shape[0], : left_support.shape[1]] = left_support
    quotient[left.shape[0] :, left_support.shape[1] :] = right_support
    signed = np.block([[left, -cross], [-cross.conj().T, right]])
    restricted = quotient.conj().T @ signed @ quotient
    dependency = quotient @ _null_basis(restricted, tolerance)
    return dependency


def _orthonormal_span(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if not matrix.size or not matrix.shape[1]:
        return np.zeros((matrix.shape[0], 0), dtype=complex)
    left, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    return left[:, singular_values > 100 * tolerance]


def _orthogonal_complement(
    basis: np.ndarray,
    dimension: int,
    tolerance: float,
) -> np.ndarray:
    if not basis.shape[1]:
        return np.eye(dimension, dtype=complex)
    _, _, right = np.linalg.svd(basis.conj().T, full_matrices=True)
    return right[basis.shape[1] :, :].conj().T


def audit_dependency_homology_node(
    node_id: str,
    gram: np.ndarray,
    slices: dict[int, tuple[int, ...]],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    target: tuple[int, ...] | None = None,
    labels: tuple[Label, ...] | None = None,
    tolerance: float = 1e-8,
) -> DependencyHomologyNode | None:
    active_left = tuple(mask for mask in left_masks if mask in slices)
    active_right = tuple(mask for mask in right_masks if mask in slices)
    if not active_left or not active_right:
        return None
    left_indices = tuple(
        index for mask in active_left for index in slices[mask]
    )
    right_indices = tuple(
        index for mask in active_right for index in slices[mask]
    )
    left = gram[np.ix_(left_indices, left_indices)]
    right = gram[np.ix_(right_indices, right_indices)]
    cross = gram[np.ix_(left_indices, right_indices)]
    dependency = _dependency_basis_from_blocks(
        left,
        right,
        cross,
        tolerance,
    )
    dependency_dimension = dependency.shape[1]
    if not dependency_dimension:
        return None

    left_local: dict[int, tuple[int, ...]] = {}
    right_local: dict[int, tuple[int, ...]] = {}
    offset = 0
    for mask in active_left:
        width = len(slices[mask])
        left_local[mask] = tuple(range(offset, offset + width))
        offset += width
    offset = 0
    for mask in active_right:
        width = len(slices[mask])
        right_local[mask] = tuple(range(offset, offset + width))
        offset += width

    pair_classes = []
    pair_edge_count = 0
    pair_dimension_sum = 0
    for left_mask in active_left:
        for right_mask in active_right:
            left_global = slices[left_mask]
            right_global = slices[right_mask]
            pair_left = gram[np.ix_(left_global, left_global)]
            pair_right = gram[np.ix_(right_global, right_global)]
            pair_cross = gram[np.ix_(left_global, right_global)]
            pair_dependency = _dependency_basis_from_blocks(
                pair_left,
                pair_right,
                pair_cross,
                tolerance,
            )
            pair_dimension = pair_dependency.shape[1]
            if not pair_dimension:
                continue
            pair_edge_count += 1
            pair_dimension_sum += pair_dimension
            embedded = np.zeros(
                (len(left_indices) + len(right_indices), pair_dimension),
                dtype=complex,
            )
            embedded[np.ix_(left_local[left_mask], range(pair_dimension))] = (
                pair_dependency[: len(left_global), :]
            )
            right_rows = tuple(
                len(left_indices) + index
                for index in right_local[right_mask]
            )
            embedded[np.ix_(right_rows, range(pair_dimension))] = (
                pair_dependency[len(left_global) :, :]
            )
            pair_classes.append(dependency.conj().T @ embedded)

    pair_coordinates = _orthonormal_span(
        np.concatenate(pair_classes, axis=1)
        if pair_classes
        else np.zeros((dependency_dimension, 0), dtype=complex),
        tolerance,
    )
    pair_dimension = pair_coordinates.shape[1]
    emergent_coordinates = _orthogonal_complement(
        pair_coordinates,
        dependency_dimension,
        tolerance,
    )
    emergent_dimension = emergent_coordinates.shape[1]

    grading = np.diag(
        np.concatenate(
            (np.ones(len(left_indices)), -np.ones(len(right_indices)))
        )
    )
    full_defect = dependency.conj().T @ grading @ dependency
    full_defect = (full_defect + full_defect.conj().T) / 2
    pair_defect = pair_coordinates.conj().T @ full_defect @ pair_coordinates
    emergent_defect = (
        emergent_coordinates.conj().T
        @ full_defect
        @ emergent_coordinates
    )
    coupling = (
        pair_coordinates.conj().T
        @ full_defect
        @ emergent_coordinates
    )
    full_residual = float(np.linalg.norm(full_defect, ord=2))
    pair_residual = float(
        np.linalg.norm(pair_defect, ord=2) if pair_defect.size else 0.0
    )
    emergent_residual = float(
        np.linalg.norm(emergent_defect, ord=2)
        if emergent_defect.size
        else 0.0
    )
    coupling_residual = float(
        np.linalg.norm(coupling, ord=2) if coupling.size else 0.0
    )
    defects = np.linalg.eigvalsh(full_defect)
    fractional = np.sort((1.0 - defects) / 2.0)
    half_residual = max(
        (abs(float(value) - 0.5) for value in fractional),
        default=0.0,
    )

    exact_pair_prediction = 0
    if target is not None and labels is not None:
        exact_pair_prediction = sum(
            multiplicity
            for left_mask in active_left
            for right_mask in active_right
            for value, multiplicity, _ in exact_pair_principal_angle_spectrum(
                target,
                labels,
                left_mask,
                right_mask,
            )
            if value == 1
        )
    overlap_dimension = pair_dimension_sum - pair_dimension
    verified = bool(
        pair_dimension <= dependency_dimension
        and emergent_dimension == dependency_dimension - pair_dimension
        and (
            target is None
            or labels is None
            or exact_pair_prediction == pair_dimension_sum
        )
        and np.all(fractional >= -100 * tolerance)
        and np.all(fractional <= 1 + 100 * tolerance)
    )
    pair_generated = pair_dimension == dependency_dimension
    emergent = emergent_dimension > 0
    neutral = full_residual <= 100 * tolerance
    return DependencyHomologyNode(
        node_id=node_id,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        active_left_orientation_masks=active_left,
        active_right_orientation_masks=active_right,
        cross_dependency_dimension=dependency_dimension,
        exact_pair_common_edge_count=pair_edge_count,
        exact_pair_common_dimension_sum=pair_dimension_sum,
        pair_dependency_class_dimension=pair_dimension,
        emergent_dependency_homology_dimension=emergent_dimension,
        pair_class_overlap_dimension=overlap_dimension,
        full_grading_neutrality_residual=full_residual,
        pair_class_grading_residual=pair_residual,
        emergent_class_grading_residual=emergent_residual,
        pair_emergent_grading_coupling_residual=coupling_residual,
        fractional_eigenvalues=tuple(float(value) for value in fractional),
        maximum_fractional_half_residual=half_residual,
        pair_classes_exhaust_cross_dependencies=pair_generated,
        emergent_dependency_present=emergent,
        pair_classes_totally_neutral=pair_residual <= 100 * tolerance,
        emergent_classes_totally_neutral=(
            emergent_residual <= 100 * tolerance
        ),
        exact_dependency_homology_audit=verified,
        status=(
            "exact-neutral-pair-generated-dependency"
            if verified and neutral and pair_generated
            else "exact-neutral-emergent-dependency"
            if verified and neutral and emergent
            else "exact-nonneutral-dependency-homology"
            if verified
            else "dependency-homology-audit-failure"
        ),
    )


def audit_dependency_homology_control(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    *,
    selected_merges: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ]
    | None = None,
    tolerance: float = 1e-8,
) -> DependencyHomologyControl:
    requested_masks = (
        tuple(
            sorted(
                {
                    mask
                    for left, right in selected_merges
                    for mask in (*left, *right)
                }
            )
        )
        if selected_merges is not None
        else tuple(range(1 << len(labels)))
    )
    bases = {
        mask: orientation_invariant_range_basis(
            target,
            labels,
            mask,
            tolerance=tolerance,
        )[0]
        for mask in requested_masks
    }
    active = tuple(mask for mask, basis in bases.items() if basis.shape[1])
    slices = {}
    offset = 0
    for mask in active:
        width = bases[mask].shape[1]
        slices[mask] = tuple(range(offset, offset + width))
        offset += width
    gram = np.zeros((offset, offset), dtype=complex)
    for left_index, left_mask in enumerate(active):
        left_slice = slices[left_mask]
        gram[np.ix_(left_slice, left_slice)] = np.eye(len(left_slice))
        for right_mask in active[left_index + 1 :]:
            right_slice = slices[right_mask]
            block = bases[left_mask].conj().T @ bases[right_mask]
            gram[np.ix_(left_slice, right_slice)] = block
            gram[np.ix_(right_slice, left_slice)] = block.conj().T
    merges = selected_merges or unique_affine_flag_merges()
    records = []
    seen = set()
    for left, right in merges:
        active_key = (
            tuple(mask for mask in left if mask in slices),
            tuple(mask for mask in right if mask in slices),
        )
        if active_key in seen:
            continue
        seen.add(active_key)
        record = audit_dependency_homology_node(
            f"{control_id}-W{len(left)}-{'-'.join(map(str, left))}-{'-'.join(map(str, right))}",
            gram,
            slices,
            left,
            right,
            target=target,
            labels=labels,
            tolerance=tolerance,
        )
        if record is not None:
            records.append(record)
    failures = sum(not record.exact_dependency_homology_audit for record in records)
    source = tuple(partition for label in labels for partition in label)
    pair_generated = sum(
        record.pair_classes_exhaust_cross_dependencies for record in records
    )
    emergent = sum(record.emergent_dependency_present for record in records)
    nonneutral = sum(
        record.full_grading_neutrality_residual > 100 * tolerance
        for record in records
    )
    return DependencyHomologyControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        globally_distinct_source_partitions=len(source) == len(set(source)),
        pairwise_distinct_physical_labels=len(labels) == len(set(labels)),
        audited_fractional_merge_count=len(records),
        pair_generated_merge_count=pair_generated,
        emergent_merge_count=emergent,
        nonneutral_merge_count=nonneutral,
        maximum_cross_dependency_dimension=max(
            (record.cross_dependency_dimension for record in records),
            default=0,
        ),
        maximum_pair_dependency_class_dimension=max(
            (record.pair_dependency_class_dimension for record in records),
            default=0,
        ),
        maximum_emergent_homology_dimension=max(
            (record.emergent_dependency_homology_dimension for record in records),
            default=0,
        ),
        maximum_full_grading_neutrality_residual=max(
            (record.full_grading_neutrality_residual for record in records),
            default=0.0,
        ),
        exact_homology_audit_failure_count=failures,
        records=records,
        status=(
            "nonneutral-dependency-homology-present"
            if not failures and nonneutral
            else "neutral-emergent-dependency-homology-present"
            if not failures and emergent
            else "all-dependencies-neutral-and-pair-generated"
            if not failures and records
            else "dependency-homology-audit-failure"
        ),
    )


@lru_cache(maxsize=1)
def _cached_controls() -> tuple[DependencyHomologyControl, ...]:
    distinct_triangle: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    w6_labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((4, 2), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    noncommuting_labels: tuple[Label, ...] = (
        ((6,), (4, 2)),
        ((5, 1), (2, 2, 2)),
        ((3, 3), (2, 1, 1, 1, 1)),
        ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    return (
        audit_dependency_homology_control(
            "W3-DISTINCT-EMERGENT",
            3,
            (2, 1),
            distinct_triangle,
        ),
        audit_dependency_homology_control(
            "W3-REPEATED-NONNEUTRAL",
            3,
            (2, 1),
            (((3,), (2, 1)),) * 3,
        ),
        audit_dependency_homology_control(
            "W5-ISOLATED-PAIR",
            5,
            (3, 2),
            _w5_probe_labels()[0],
        ),
        audit_dependency_homology_control(
            "W6-RICH-MULTIPLICITY-TWO",
            6,
            (5, 1),
            w6_labels,
        ),
        audit_dependency_homology_control(
            "W6-COLLISION-FREE-NONCOMMUTING-CORE",
            6,
            (6,),
            noncommuting_labels,
            selected_merges=(((2, 5), (11, 12)),),
        ),
    )


def _controls() -> list[DependencyHomologyControl]:
    return list(_cached_controls())


def run_dependency_homology() -> DependencyHomologyReport:
    controls = _controls()
    distinct, repeated, w5, w6, noncommuting = controls
    failures = sum(
        control.exact_homology_audit_failure_count for control in controls
    )
    metrics: dict[str, int | float] = {
        "dependency_homology_quotient_count": int(failures == 0),
        "finite_control_count": len(controls),
        "finite_homology_audit_failure_count": failures,
        "finite_fractional_merge_count": sum(
            control.audited_fractional_merge_count for control in controls
        ),
        "finite_pair_generated_merge_count": sum(
            control.pair_generated_merge_count for control in controls
        ),
        "finite_emergent_merge_count": sum(
            control.emergent_merge_count for control in controls
        ),
        "w3_distinct_maximum_emergent_homology_dimension": (
            distinct.maximum_emergent_homology_dimension
        ),
        "w5_pair_generated_merge_count": w5.pair_generated_merge_count,
        "w6_pair_generated_merge_count": w6.pair_generated_merge_count,
        "repeated_label_nonneutral_merge_count": repeated.nonneutral_merge_count,
        "collision_free_nonneutral_pair_generated_merge_count": (
            noncommuting.nonneutral_merge_count
        ),
        "collision_free_nonneutral_cross_dependency_dimension": (
            noncommuting.maximum_cross_dependency_dimension
        ),
        "collision_free_nonneutral_grading_residual": (
            noncommuting.maximum_full_grading_neutrality_residual
        ),
        "all_n_pair_common_chain_complex_count": 0,
        "all_n_emergent_homology_vanishing_or_neutrality_count": 0,
        "coherent_pair_common_quotient_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    scaling = [
        {
            "n": n,
            "information_threshold_copy_count": math.ceil(
                math.lgamma(n + 1) / math.log(2)
            ),
            "finite_pair_dependency_quotient_available": True,
            "symbolic_pair_common_chain_complex_proved": False,
            "emergent_homology_dimension_bounded": False,
            "emergent_homology_grading_neutrality_proved": False,
            "coherent_pair_common_quotient_compiled": False,
            "status": "finite-dependency-homology-all-n-chain-complex-open",
        }
        for n in (6, 8, 16, 32, 64, 128, 256, 512)
    ]
    return DependencyHomologyReport(
        created_at=utc_now(),
        quotient_contract={
            "cross_dependency_space": "W is the cross-child synthesis kernel modulo both child-internal kernels.",
            "pair_classes": "Each exact two-leaf common range maps to a class in W; W_pair is their span after quotient projection.",
            "emergent_homology": "H_em=W/W_pair, represented by the orthogonal complement of W_pair in W.",
            "grading_decomposition": "The left-minus-right grading is audited on W_pair, H_em, and the pair/emergent coupling block.",
            "scope": "Finite leaf Gram bases compute the quotient exactly; no all-n recoupling chain complex or coherent quotient is yet known.",
        },
        controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "finite_pair_dependency_quotient",
                "resolved": failures == 0,
                "resolution": "Every exact pair relation is projected into the canonical cross-syzygy quotient and rank-checked against pair-angle multiplicities.",
            },
            {
                "obligation": "classify_emergent_dependencies",
                "resolved": True,
                "resolution": "The W3 distinct plane is genuinely emergent; selected W5/S6 channels and the collision-free nonneutral S6 counterexample are pair-generated.",
            },
            {
                "obligation": "all_n_pair_common_chain_complex",
                "resolved": False,
                "resolution": "Higher relations among trivial/sign pair intertwiners are not expressed in symbolic representation labels.",
            },
            {
                "obligation": "all_n_emergent_homology_neutrality",
                "resolved": False,
                "resolution": "A collision-free S6 pair-generated counterexample is already nonneutral, while W3 also shows emergent homology need not vanish.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Every child intersection is a sum of exact pairwise common ranges.",
                "resolved": True,
                "resolution": "The label-distinct W3 plane has two-dimensional dependency homology and no exact pair-common edge.",
            },
            {
                "objection": "Pair-generated dependencies are automatically neutral.",
                "resolved": noncommuting.nonneutral_merge_count > 0,
                "resolution": "False even with globally distinct source partitions: the S6 noncommuting-core plane is entirely pair-generated but has grading defect 1/17.",
            },
            {
                "objection": "Vanishing emergent homology gives a circuit.",
                "resolved": False,
                "resolution": "One still needs a coherent basis for pair classes, their overlaps, and the quotient map at threshold scale.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "finite_dependency_homology_quotient_verified": failures == 0,
            "w3_distinct_dependency_is_genuinely_emergent": (
                distinct.maximum_emergent_homology_dimension > 0
            ),
            "selected_w5_dependencies_pair_generated": (
                w5.audited_fractional_merge_count
                == w5.pair_generated_merge_count
            ),
            "selected_w6_dependencies_pair_generated": (
                w6.audited_fractional_merge_count
                == w6.pair_generated_merge_count
            ),
            "collision_free_pair_generated_half_balance_falsified": (
                noncommuting.nonneutral_merge_count > 0
                and noncommuting.pair_generated_merge_count > 0
            ),
            "universal_pair_generation_proved": False,
            "all_n_emergent_homology_neutrality_proved": False,
            "coherent_pair_common_quotient_compiled": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": "Finite pair and emergent classes are separated exactly, and a collision-free S6 pair-generated class falsifies universal half-balance. No all-n recoupling block classification or coherent quotient map is known.",
        },
        status="collision-free-pair-generated-nonneutral-block-classification-open",
        summary=(
            "Constructed the pair-common quotient of cross dependencies: W3 has genuine neutral emergent homology, while a globally distinct S6 affine plane has an entirely pair-generated nonneutral 34-dimensional intersection."
        ),
        falsifiers_triggered=[
            "Exact pair-common ranges do not exhaust every finite child intersection.",
            "A raw pair-edge count ignores linear dependencies and overlap among pair classes.",
            "Pair generation must be separated from grading neutrality.",
            "Collision-free source labels do not restore universal pair-class half-balance.",
            "A finite dependency quotient is not a coherent all-n recoupling transform.",
        ],
    )


def write_dependency_homology(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_dependency_homology())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    output = write_dependency_homology()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
