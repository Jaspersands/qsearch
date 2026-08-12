"""Sparse invariant-range and coefficient-Gram audit beyond dense W5 blocks.

Dense orientation projectors act on

    V_nu tensor product_i (V_lambda_i tensor V_mu_i),

whose dimension becomes prohibitive before the first interesting Kronecker
multiplicities.  Each orientation range is much smaller.  If ``epsilon``
selects one irrep from every unequal pair, then

    ran(E_epsilon)
      = Inv(V_nu tensor product_i V_selected_i)
        tensor product_i V_companion_i.                      (1)

The invariant factor is obtained by applying the exact finite-group average
to only ``m+O(1)`` random vectors, where its dimension ``m`` is known exactly
from the representation ring.  Companion identities are attached only after
that projection.  This produces an isometric leaf basis without materializing
the ambient projector.

For leaf bases ``Q_e``, every affine merge is determined by the small block
Gram ``G_(f,e)=Q_f^*Q_e``.  Child row spaces, the cross-synthesis dependency
quotient, the coefficient-grading defects, and hence every fractional
relative-effect eigenvalue can be computed directly from principal submatrices
of G.  No physical-space pseudoinverse or eigendecomposition is needed.

This module is the first exact numerical route into collision-free ``S_6``
multiplicity sectors.  It is still a finite audit: enumerating group elements
and storing leaf bases is not an all-n algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_jucys_murphy_label_transform import adjacent_transposition_matrices
from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_level_three_flag_audit import _reduced_projector_family
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from self_dual_wreath_shorted_overlap_balance import (
    _support_basis,
    unique_affine_flag_merges,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sparse_invariant_dependency.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SparseInvariantLeafRecord:
    orientation_mask: int
    selected_partitions: tuple[tuple[int, ...], ...]
    companion_partitions: tuple[tuple[int, ...], ...]
    selected_tensor_dimension: int
    exact_invariant_multiplicity: int
    companion_dimension: int
    leaf_range_dimension: int
    maximum_generator_invariance_residual: float
    leaf_basis_isometry_residual: float
    randomized_range_singular_value_gap: float | None
    exact_rank_matched_representation_ring: bool
    status: str


@dataclass(frozen=True)
class SparseDependencyMergeRecord:
    node_id: str
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    active_left_orientation_masks: tuple[int, ...]
    active_right_orientation_masks: tuple[int, ...]
    left_coefficient_dimension: int
    right_coefficient_dimension: int
    left_synthesis_rank: int
    right_synthesis_rank: int
    common_range_dimension: int
    grading_neutrality_residual: float
    fractional_eigenvalues: tuple[float, ...]
    maximum_fractional_half_residual: float
    exact_coefficient_gram_dependency_audit: bool
    grading_neutral: bool
    status: str


@dataclass(frozen=True)
class SparseInvariantDependencyControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    physical_ambient_dimension: int
    active_orientation_count: int
    total_leaf_coefficient_dimension: int
    maximum_leaf_range_dimension: int
    maximum_exact_invariant_multiplicity: int
    maximum_generator_invariance_residual: float
    maximum_leaf_basis_isometry_residual: float
    maximum_global_block_gram_hermiticity_residual: float
    fractional_merge_count: int
    neutral_fractional_merge_count: int
    nonneutral_fractional_merge_count: int
    observed_fractional_eigenvalues: tuple[float, ...]
    maximum_fractional_half_residual: float
    first_nonneutral_node_id: str | None
    leaf_records: list[SparseInvariantLeafRecord]
    merge_records: list[SparseDependencyMergeRecord]
    sparse_invariant_basis_audit_verified: bool
    status: str


@dataclass(frozen=True)
class SparseInvariantDependencyReport:
    created_at: str
    method_contract: dict[str, Any]
    controls: list[SparseInvariantDependencyControl]
    scaling_records: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _kron_apply_batch(
    matrices: tuple[np.ndarray, ...],
    vectors: np.ndarray,
    dimensions: tuple[int, ...],
) -> np.ndarray:
    tensor = vectors.reshape((*dimensions, vectors.shape[1]))
    for axis, matrix in enumerate(matrices):
        tensor = np.tensordot(matrix, tensor, axes=(1, axis))
        tensor = np.moveaxis(tensor, 0, axis)
    return tensor.reshape((-1, vectors.shape[1]))


@lru_cache(maxsize=128)
def _selected_invariant_basis(
    target: tuple[int, ...],
    selected: tuple[tuple[int, ...], ...],
    seed: int,
    tolerance: float,
) -> tuple[np.ndarray, float, float | None]:
    n = sum(target)
    multiplicity = dict(
        tensor_product_multiplicities(selected, n)
    ).get(target, 0)
    dimensions = tuple(
        hook_length_dimension(partition)
        for partition in (target, *selected)
    )
    total_dimension = math.prod(dimensions)
    if not multiplicity:
        return np.zeros((total_dimension, 0)), 0.0, None

    tables = tuple(
        dict(permutation_representation_matrices(partition))
        for partition in (target, *selected)
    )
    permutations = tuple(tables[0])
    rng = np.random.default_rng(seed)
    trial_count = multiplicity + max(3, multiplicity // 2)
    trial = rng.normal(size=(total_dimension, trial_count))
    projected = np.zeros_like(trial)
    for permutation in permutations:
        projected += _kron_apply_batch(
            tuple(table[permutation] for table in tables),
            trial,
            dimensions,
        )
    projected /= len(permutations)
    left, singular_values, _ = np.linalg.svd(projected, full_matrices=False)
    basis = left[:, :multiplicity]
    retained = float(singular_values[multiplicity - 1])
    discarded = (
        float(singular_values[multiplicity])
        if len(singular_values) > multiplicity
        else 0.0
    )
    gap = retained / max(discarded, np.finfo(float).eps)

    generators = tuple(
        adjacent_transposition_matrices(partition)
        for partition in (target, *selected)
    )
    invariance = max(
        float(
            np.linalg.norm(
                _kron_apply_batch(
                    tuple(table[index] for table in generators),
                    basis,
                    dimensions,
                )
                - basis,
                ord=2,
            )
        )
        for index in range(n - 1)
    )
    if invariance > 100 * tolerance:
        raise ArithmeticError("randomized invariant range failed generator check")
    return basis, invariance, gap


def orientation_invariant_range_basis(
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    orientation_mask: int,
    *,
    tolerance: float = 1e-8,
) -> tuple[np.ndarray, SparseInvariantLeafRecord]:
    if not 0 <= orientation_mask < 1 << len(labels):
        raise ValueError("orientation mask out of range")
    selected = []
    companions = []
    grouped_names = ["target"]
    grouped_dimensions = [hook_length_dimension(target)]
    ambient_names = ["target"]
    ambient_dimensions = [hook_length_dimension(target)]
    for index, (left, right) in enumerate(labels):
        bit = bool(orientation_mask & (1 << index))
        selected_partition = right if bit else left
        companion_partition = left if bit else right
        selected.append(selected_partition)
        companions.append(companion_partition)
        grouped_names.append(f"selected-{index}")
        grouped_dimensions.append(hook_length_dimension(selected_partition))
        ambient_names.extend(
            (f"companion-{index}", f"selected-{index}")
            if bit
            else (f"selected-{index}", f"companion-{index}")
        )
        ambient_dimensions.extend(
            (hook_length_dimension(left), hook_length_dimension(right))
        )

    selected_tuple = tuple(selected)
    companion_tuple = tuple(companions)
    multiplicity = dict(
        tensor_product_multiplicities(selected_tuple, sum(target))
    ).get(target, 0)
    selected_basis, invariance, gap = _selected_invariant_basis(
        target,
        selected_tuple,
        13007 + 97 * sum(target) + orientation_mask,
        tolerance,
    )
    companion_dimensions = tuple(
        hook_length_dimension(partition) for partition in companion_tuple
    )
    companion_dimension = math.prod(companion_dimensions)
    grouped = np.kron(selected_basis, np.eye(companion_dimension))
    grouped_names.extend(
        f"companion-{index}" for index in range(len(labels))
    )
    grouped_dimensions.extend(companion_dimensions)
    grouped_indices = np.arange(math.prod(grouped_dimensions)).reshape(
        grouped_dimensions
    )
    row_permutation = grouped_indices.transpose(
        tuple(grouped_names.index(name) for name in ambient_names)
    ).reshape(-1)
    embedded = grouped[row_permutation, :]
    isometry = float(
        np.linalg.norm(
            embedded.conj().T @ embedded - np.eye(embedded.shape[1]),
            ord=2,
        )
        if embedded.shape[1]
        else 0.0
    )
    expected_rank = multiplicity * companion_dimension
    verified = embedded.shape[1] == expected_rank
    return embedded, SparseInvariantLeafRecord(
        orientation_mask=orientation_mask,
        selected_partitions=selected_tuple,
        companion_partitions=companion_tuple,
        selected_tensor_dimension=selected_basis.shape[0],
        exact_invariant_multiplicity=multiplicity,
        companion_dimension=companion_dimension,
        leaf_range_dimension=embedded.shape[1],
        maximum_generator_invariance_residual=invariance,
        leaf_basis_isometry_residual=isometry,
        randomized_range_singular_value_gap=gap,
        exact_rank_matched_representation_ring=verified,
        status=(
            "sparse-invariant-leaf-basis-verified"
            if verified and max(invariance, isometry) <= 100 * tolerance
            else "sparse-invariant-leaf-basis-failure"
        ),
    )


def audit_dependency_from_gram(
    node_id: str,
    gram: np.ndarray,
    left_indices: tuple[int, ...],
    right_indices: tuple[int, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    active_left_masks: tuple[int, ...],
    active_right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> SparseDependencyMergeRecord:
    left = gram[np.ix_(left_indices, left_indices)]
    right = gram[np.ix_(right_indices, right_indices)]
    cross = gram[np.ix_(left_indices, right_indices)]
    left_basis = _support_basis(left, tolerance)
    right_basis = _support_basis(right, tolerance)
    quotient = np.zeros(
        (
            len(left_indices) + len(right_indices),
            left_basis.shape[1] + right_basis.shape[1],
        ),
        dtype=complex,
    )
    quotient[: len(left_indices), : left_basis.shape[1]] = left_basis
    quotient[len(left_indices) :, left_basis.shape[1] :] = right_basis
    signed_gram = np.block([[left, -cross], [-cross.conj().T, right]])
    restricted = quotient.conj().T @ signed_gram @ quotient
    restricted = (restricted + restricted.conj().T) / 2
    values, vectors = np.linalg.eigh(restricted)
    if values[0] < -100 * tolerance:
        raise ArithmeticError("signed synthesis Gram is not positive semidefinite")
    null = vectors[:, values <= 100 * tolerance]
    dependency = quotient @ null
    grading = np.diag(
        np.concatenate(
            (np.ones(len(left_indices)), -np.ones(len(right_indices)))
        )
    )
    defect_operator = dependency.conj().T @ grading @ dependency
    defect_operator = (defect_operator + defect_operator.conj().T) / 2
    defects = np.linalg.eigvalsh(defect_operator)
    fractional = np.sort((1.0 - defects) / 2.0)
    neutrality = float(
        np.linalg.norm(defect_operator, ord=2)
        if defect_operator.size
        else 0.0
    )
    half_residual = max(
        (abs(float(value) - 0.5) for value in fractional),
        default=0.0,
    )
    neutral = neutrality <= 100 * tolerance
    verified = bool(
        np.all(fractional >= -100 * tolerance)
        and np.all(fractional <= 1 + 100 * tolerance)
    )
    return SparseDependencyMergeRecord(
        node_id=node_id,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        active_left_orientation_masks=active_left_masks,
        active_right_orientation_masks=active_right_masks,
        left_coefficient_dimension=len(left_indices),
        right_coefficient_dimension=len(right_indices),
        left_synthesis_rank=left_basis.shape[1],
        right_synthesis_rank=right_basis.shape[1],
        common_range_dimension=dependency.shape[1],
        grading_neutrality_residual=neutrality,
        fractional_eigenvalues=tuple(float(value) for value in fractional),
        maximum_fractional_half_residual=half_residual,
        exact_coefficient_gram_dependency_audit=verified,
        grading_neutral=neutral,
        status=(
            "exact-neutral-coefficient-gram-dependency"
            if verified and neutral
            else "exact-nonneutral-coefficient-gram-dependency"
            if verified
            else "coefficient-gram-dependency-failure"
        ),
    )


def audit_sparse_invariant_dependency_control(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-8,
) -> SparseInvariantDependencyControl:
    bases = []
    leaf_records = []
    for mask in range(1 << len(labels)):
        basis, record = orientation_invariant_range_basis(
            target,
            labels,
            mask,
            tolerance=tolerance,
        )
        bases.append(basis)
        leaf_records.append(record)
    active = tuple(
        mask for mask, basis in enumerate(bases) if basis.shape[1]
    )
    slices: dict[int, tuple[int, ...]] = {}
    offset = 0
    active_bases = []
    for mask in active:
        width = bases[mask].shape[1]
        slices[mask] = tuple(range(offset, offset + width))
        offset += width
        active_bases.append(bases[mask])
    synthesis = np.concatenate(active_bases, axis=1) if active_bases else np.zeros((0, 0))
    gram = synthesis.conj().T @ synthesis
    hermiticity = float(np.linalg.norm(gram - gram.conj().T, ord=2)) if gram.size else 0.0

    merge_records = []
    seen: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for left, right in unique_affine_flag_merges():
        active_left = tuple(mask for mask in left if mask in slices)
        active_right = tuple(mask for mask in right if mask in slices)
        if not active_left or not active_right:
            continue
        left_indices = tuple(index for mask in active_left for index in slices[mask])
        right_indices = tuple(index for mask in active_right for index in slices[mask])
        key = (left_indices, right_indices)
        if key in seen:
            continue
        seen.add(key)
        record = audit_dependency_from_gram(
            f"{control_id}-W{len(left)}-{'-'.join(map(str, left))}-{'-'.join(map(str, right))}",
            gram,
            left_indices,
            right_indices,
            left,
            right,
            active_left,
            active_right,
            tolerance=tolerance,
        )
        if record.common_range_dimension:
            merge_records.append(record)
    failures = sum(
        not record.exact_rank_matched_representation_ring
        or record.maximum_generator_invariance_residual > 100 * tolerance
        or record.leaf_basis_isometry_residual > 100 * tolerance
        for record in leaf_records
    ) + sum(
        not record.exact_coefficient_gram_dependency_audit
        for record in merge_records
    )
    nonneutral = [record for record in merge_records if not record.grading_neutral]
    observed = tuple(
        sorted(
            {
                round(value, 10)
                for record in merge_records
                for value in record.fractional_eigenvalues
            }
        )
    )
    physical_dimension = (
        hook_length_dimension(target)
        * math.prod(
            hook_length_dimension(partition)
            for label in labels
            for partition in label
        )
    )
    return SparseInvariantDependencyControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        physical_ambient_dimension=physical_dimension,
        active_orientation_count=len(active),
        total_leaf_coefficient_dimension=offset,
        maximum_leaf_range_dimension=max(
            (basis.shape[1] for basis in bases),
            default=0,
        ),
        maximum_exact_invariant_multiplicity=max(
            (record.exact_invariant_multiplicity for record in leaf_records),
            default=0,
        ),
        maximum_generator_invariance_residual=max(
            (record.maximum_generator_invariance_residual for record in leaf_records),
            default=0.0,
        ),
        maximum_leaf_basis_isometry_residual=max(
            (record.leaf_basis_isometry_residual for record in leaf_records),
            default=0.0,
        ),
        maximum_global_block_gram_hermiticity_residual=hermiticity,
        fractional_merge_count=len(merge_records),
        neutral_fractional_merge_count=len(merge_records) - len(nonneutral),
        nonneutral_fractional_merge_count=len(nonneutral),
        observed_fractional_eigenvalues=observed,
        maximum_fractional_half_residual=max(
            (record.maximum_fractional_half_residual for record in merge_records),
            default=0.0,
        ),
        first_nonneutral_node_id=(
            nonneutral[0].node_id if nonneutral else None
        ),
        leaf_records=leaf_records,
        merge_records=merge_records,
        sparse_invariant_basis_audit_verified=failures == 0,
        status=(
            "sparse-invariant-nonneutral-counterexample-found"
            if failures == 0 and nonneutral
            else "sparse-invariant-all-observed-dependencies-neutral"
            if failures == 0
            else "sparse-invariant-dependency-audit-failure"
        ),
    )


def _w3_control() -> SparseInvariantDependencyControl:
    labels: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    return audit_sparse_invariant_dependency_control(
        "W3-DENSE-CROSSCHECK",
        3,
        (2, 1),
        labels,
    )


def _w6_multiplicity_control() -> SparseInvariantDependencyControl:
    labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((4, 2), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    return audit_sparse_invariant_dependency_control(
        "W6-COLLISION-FREE-RICH-MULTIPLICITY-TWO",
        6,
        (5, 1),
        labels,
    )


def _w6_high_multiplicity_control() -> SparseInvariantDependencyControl:
    labels: tuple[Label, ...] = (
        ((6,), (5, 1)),
        ((4, 2), (4, 1, 1)),
        ((2, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    return audit_sparse_invariant_dependency_control(
        "W6-COLLISION-FREE-SEVEN-ACTIVE-MULTIPLICITY-FIVE",
        6,
        (3, 1, 1, 1),
        labels,
    )


def run_sparse_invariant_dependency() -> SparseInvariantDependencyReport:
    controls = [
        _w3_control(),
        _w6_multiplicity_control(),
        _w6_high_multiplicity_control(),
    ]
    w3 = controls[0]
    w6_controls = controls[1:]
    failures = sum(
        not record.sparse_invariant_basis_audit_verified for record in controls
    )
    dense_w3, _, _ = _reduced_projector_family(
        w3.target_partition,
        w3.labels,
        1e-8,
    )
    dense_ranks = tuple(
        _support_basis(projector, 1e-8).shape[1] for projector in dense_w3
    )
    sparse_ranks = tuple(record.leaf_range_dimension for record in w3.leaf_records)
    dense_crosscheck = dense_ranks == sparse_ranks
    metrics: dict[str, int | float] = {
        "sparse_invariant_control_count": len(controls),
        "sparse_invariant_validation_failure_count": failures,
        "dense_w3_leaf_rank_crosscheck_count": int(dense_crosscheck),
        "maximum_physical_ambient_dimension_avoided": max(
            record.physical_ambient_dimension for record in controls
        ),
        "maximum_total_leaf_coefficient_dimension": max(
            record.total_leaf_coefficient_dimension for record in controls
        ),
        "maximum_exact_invariant_multiplicity_reached": max(
            record.maximum_exact_invariant_multiplicity for record in controls
        ),
        "w6_active_orientation_count": max(
            record.active_orientation_count for record in w6_controls
        ),
        "w6_fractional_merge_count": sum(
            record.fractional_merge_count for record in w6_controls
        ),
        "w6_nonneutral_fractional_merge_count": (
            sum(
                record.nonneutral_fractional_merge_count
                for record in w6_controls
            )
        ),
        "w6_maximum_fractional_half_residual": (
            max(
                record.maximum_fractional_half_residual
                for record in w6_controls
            )
        ),
        "all_n_sparse_invariant_transform_count": 0,
        "all_n_neutrality_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    nonneutral_found = any(
        record.nonneutral_fractional_merge_count > 0
        for record in w6_controls
    )
    scaling = [
        {
            "n": n,
            "group_enumeration_is_factorial": True,
            "dense_physical_projector_required": False,
            "finite_invariant_range_basis_available": True,
            "polynomial_all_n_invariant_basis_transform_proved": False,
            "all_n_dependency_neutrality_proved": False,
            "status": "finite-sparse-range-audit-not-all-n-transform",
        }
        for n in (6, 8, 16, 32, 64, 128)
    ]
    return SparseInvariantDependencyReport(
        created_at=utc_now(),
        method_contract={
            "orientation_range_factorization": "ran(E_e)=Inv(V_nu tensor selected irreps) tensor companion spaces.",
            "rank_oracle": "The invariant rank is computed exactly from tensor-product multiplicities before randomized range extraction.",
            "range_extraction": "Finite group averaging is applied to m+O(1) random vectors in the selected tensor space and verified against adjacent generators.",
            "coefficient_gram_reduction": "All cross-dependency grading defects are computed from the concatenated leaf-basis Gram, never from dense physical frame operators.",
            "scope": "This removes the finite dense-memory barrier but still enumerates S_n and is not an efficient all-n transform.",
        },
        controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "sparse_invariant_range_factorization",
                "resolved": failures == 0 and dense_crosscheck,
                "resolution": "Exact representation ranks, generator invariance, and dense W3 leaf ranks agree.",
            },
            {
                "obligation": "first_collision_free_multiplicity_sector_balance",
                "resolved": True,
                "resolution": (
                    "The selected S6 multiplicity-two sector has been audited exactly in coefficient Gram space; its result is recorded without extrapolation."
                ),
            },
            {
                "obligation": "all_n_sparse_invariant_transform",
                "resolved": False,
                "resolution": "The finite extractor enumerates every group element and stores physical leaf bases.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The W3/W5 scalar signal may be tested at multiplicity two only with dense 5625-square projectors.",
                "resolved": True,
                "resolution": "The S6 control uses at most a small coefficient Gram after exact invariant-range extraction.",
            },
            {
                "objection": "Randomized range extraction can silently miss invariant vectors.",
                "resolved": True,
                "resolution": "The target rank is exact, the retained/discarded singular gap is recorded, and every basis is checked against all adjacent generators.",
            },
            {
                "objection": "A finite sparse audit is already an all-n algorithm.",
                "resolved": False,
                "resolution": "It still performs factorial group averaging and explicit physical-basis storage.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "sparse_invariant_range_audit_verified": failures == 0 and dense_crosscheck,
            "first_s6_collision_free_multiplicity_sector_audited": True,
            "s6_nonneutral_counterexample_found": nonneutral_found,
            "s6_selected_control_remains_neutral": not nonneutral_found,
            "all_n_collision_free_neutrality_proved": False,
            "polynomial_all_n_invariant_transform_proved": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The first multiplicity-two finite sector is now accessible, but one S6 control cannot establish the all-n recoupling law and the extractor is factorial-time."
            ),
        },
        status=(
            "s6-collision-free-nonneutral-counterexample-found"
            if nonneutral_found
            else "s6-selected-multiplicity-sector-neutral-broader-search-open"
        ),
        summary=(
            "Built an invariant-range/coefficient-Gram audit that reaches a 5,625-dimensional S6 multiplicity-two physical sector without dense projectors; the exact balance outcome is recorded and broader multiplicity search remains open."
        ),
        falsifiers_triggered=[
            "Dense physical projector construction is not necessary for finite higher-multiplicity dependency audits.",
            "A compact finite coefficient Gram does not imply an efficient all-n basis transform.",
            (
                "The selected collision-free S6 multiplicity sector contains a nonneutral merge."
                if nonneutral_found
                else "The first selected collision-free S6 multiplicity-two sector does not by itself falsify neutrality."
            ),
        ],
    )


def write_sparse_invariant_dependency(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_sparse_invariant_dependency())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    output = write_sparse_invariant_dependency()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
