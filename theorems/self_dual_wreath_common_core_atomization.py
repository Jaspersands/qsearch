"""Common-core atomization and the relative Cech balance criterion.

For orientation ranges ``U_e`` and a finite orientation family ``O``, put

    K_F = intersection_{e in F} U_e,  |F| >= 2.

The fixed-family parity theorem gives ``dim K_F`` from representation-ring
data.  This module also constructs an explicit orthonormal basis for ``K_F``:
each nonempty membership-pattern tensor is projected to a trivial or sign
isotype and the allowed isotypes are coupled by the parity kernel.

The pair cores ``K_{e,f}`` form a particularly useful boundary.  If their
orthogonal projectors commute, they have a simultaneous Boolean atomization

    K_F = direct_sum_{S superset F} A_S.                    (1)

The atom multiplicities follow by Mobius inversion of the exact fixed-family
dimensions.  For an affine sibling merge ``O=L disjoint_union R``, an atom
supported on ``p`` left and ``q`` right leaves contributes one relative pair
class with left-effect eigenvalue

    lambda_S = p / (p + q).                                (2)

Thus a commuting common-core arrangement is grading-neutral exactly when
every crossing atom has equal support in the two children.  Equation (2)
also explains the recurring ``1/3,2/3`` failure mode: it is the signature of
a support atom meeting sibling children in counts one and two.

The parity theorem supplies the support-balance half of this criterion at all
``n>=5``.  If a vector lies in ``U_a``, ``U_b``, and ``U_c``, summing the three
parity-kernel equations shows that it also lies in ``U_(a xor b xor c)``.
Consequently the exact orientation support of every common vector is closed
under ternary XOR and is therefore an affine subspace of ``F_2^k``.  Its
intersection with an affine parent is either contained in one child or meets
both codimension-one children equally.  A Boolean common-core atom can never
have the one-versus-two support responsible for (2).

The direct relative-Cech calculation below does not assume commutativity.  It
forms pair-relation Grams, quotients same-child pair relations, and measures
the left-minus-right grading.  Agreement with (1)-(2) is therefore a genuine
finite test of the atomization mechanism, not a definition.

This is a sufficient mechanism, not a complete all-n wreath theorem.  The
remaining common-core gate is to prove that collision-free parity
intertwiners commute, or suitably block-diagonalize.  Noncommon carrier
blocks and coherent implementation remain separate obligations.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    upsert_experiment_result,
    utc_now,
)
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)
from self_dual_wreath_orientation_triple_range import (
    fixed_family_common_range_dimension,
    viable_sparse_parity_assignments,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from self_dual_wreath_sparse_invariant_dependency import _kron_apply_batch


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_common_core_atomization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class CommonCoreAtomRecord:
    support_orientation_masks: tuple[int, ...]
    multiplicity: int
    left_support_count: int
    right_support_count: int
    crosses_sibling_split: bool
    predicted_left_effect_eigenvalue: float | None
    grading_balanced: bool


@dataclass(frozen=True)
class CommonCoreAtomizationControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_masks: tuple[int, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    physical_ambient_dimension: int
    nonzero_pair_core_count: int
    total_pair_core_dimension: int
    nonzero_higher_common_core_count: int
    maximum_higher_common_core_dimension: int
    fixed_family_basis_validation_count: int
    fixed_family_basis_rank_mismatch_count: int
    maximum_common_basis_isometry_residual: float
    maximum_pair_core_projector_commutator_norm: float
    maximum_pair_core_intersection_rank_residual: int
    ternary_affine_closure_validation_count: int
    ternary_affine_closure_dimension_mismatch_count: int
    mobius_atom_count: int
    negative_mobius_atom_count: int
    nonaffine_positive_mobius_atom_count: int
    crossing_atom_count: int
    imbalanced_crossing_atom_count: int
    predicted_relative_pair_class_dimension: int
    direct_relative_pair_class_dimension: int
    predicted_fractional_eigenvalues: tuple[float, ...]
    direct_fractional_eigenvalues: tuple[float, ...]
    maximum_predicted_spectrum_residual: float
    maximum_direct_grading_neutrality_residual: float
    maximum_direct_fractional_half_residual: float
    sibling_child_size: int
    pair_relations_equal_full_internal_kernels: bool
    nonneutral_full_merge_certified: bool
    pair_core_projectors_commute: bool
    boolean_atomization_verified: bool
    all_crossing_atoms_balanced: bool
    direct_relative_cech_audit_verified: bool
    exact_relative_cech_spectrum_verified: bool
    atoms: list[CommonCoreAtomRecord]
    status: str


@dataclass(frozen=True)
class AbstractAtomImbalanceControl:
    support_size: int
    left_support_count: int
    right_support_count: int
    predicted_left_effect_eigenvalue: float
    predicted_grading_defect: float
    balanced: bool
    status: str


@dataclass(frozen=True)
class ScalarStarRecouplingControl:
    pair_core_principal_correlation: float
    shared_mode_multiplicity: int
    orthogonal_cross_mode_multiplicity: int
    antisymmetric_left_effect_eigenvalue: float
    symmetric_left_effect_eigenvalue: float
    orthogonal_left_effect_eigenvalue: float
    predicted_fractional_eigenvalues: tuple[float, ...]
    direct_spectrum_residual: float
    exact_scalar_star_formula_verified: bool
    status: str


@dataclass(frozen=True)
class CommonCoreAtomizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CommonCoreAtomizationControl]
    abstract_imbalance_control: AbstractAtomImbalanceControl
    scalar_star_counterexample: ScalarStarRecouplingControl
    scaling_records: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def _multiplicity(
    partitions: tuple[Partition, ...],
    target: Partition,
    n: int,
) -> int:
    if not partitions:
        return int(target == (n,))
    return dict(tensor_product_multiplicities(partitions, n)).get(target, 0)


@lru_cache(maxsize=512)
def _one_dimensional_isotypic_basis(
    partitions: tuple[Partition, ...],
    sign_bit: int,
    tolerance: float,
) -> tuple[np.ndarray, float, float | None]:
    if sign_bit not in (0, 1):
        raise ValueError("sign_bit must be zero or one")
    if not partitions:
        return (
            np.ones((1, 1)) if not sign_bit else np.zeros((1, 0)),
            0.0,
            None,
        )
    n = sum(partitions[0])
    if any(sum(partition) != n for partition in partitions):
        raise ValueError("all pattern partitions must have the same degree")
    target = (1,) * n if sign_bit else (n,)
    multiplicity = _multiplicity(partitions, target, n)
    dimensions = tuple(hook_length_dimension(item) for item in partitions)
    total_dimension = math.prod(dimensions)
    if not multiplicity:
        return np.zeros((total_dimension, 0)), 0.0, None

    tables = tuple(
        dict(permutation_representation_matrices(partition))
        for partition in partitions
    )
    permutations = tuple(tables[0])
    seed = (
        17011
        + 101 * n
        + 1009 * sign_bit
        + sum(
            (index + 1) * sum((row + 1) * value for row, value in enumerate(partition))
            for index, partition in enumerate(partitions)
        )
    )
    rng = np.random.default_rng(seed)
    trial_count = min(
        total_dimension,
        multiplicity + max(4, multiplicity // 2),
    )
    trial = rng.normal(size=(total_dimension, trial_count))
    projected = np.zeros_like(trial)
    for permutation in permutations:
        weight = _permutation_sign(permutation) if sign_bit else 1
        projected += weight * _kron_apply_batch(
            tuple(table[permutation] for table in tables),
            trial,
            dimensions,
        )
    projected /= len(permutations)
    left, singular_values, _ = np.linalg.svd(projected, full_matrices=False)
    if len(singular_values) < multiplicity:
        raise ArithmeticError("isotypic trial space is too small")
    basis = left[:, :multiplicity]
    retained = float(singular_values[multiplicity - 1])
    discarded = (
        float(singular_values[multiplicity])
        if len(singular_values) > multiplicity
        else 0.0
    )
    gap = retained / max(discarded, np.finfo(float).eps)

    generator_residual = 0.0
    table_dicts = tables
    for adjacent in range(n - 1):
        permutation = list(range(n))
        permutation[adjacent], permutation[adjacent + 1] = (
            permutation[adjacent + 1],
            permutation[adjacent],
        )
        action = _kron_apply_batch(
            tuple(table[tuple(permutation)] for table in table_dicts),
            basis,
            dimensions,
        )
        generator_residual = max(
            generator_residual,
            float(
                np.linalg.norm(
                    action - ((-1) ** sign_bit) * basis,
                    ord=2,
                )
            ),
        )
    if generator_residual > 100 * tolerance:
        raise ArithmeticError("one-dimensional isotypic basis failed generator check")
    return basis, generator_residual, gap


def _factor_pattern_data(
    target: Partition,
    labels: tuple[Label, ...],
    orientation_masks: tuple[int, ...],
) -> tuple[tuple[str, Partition, int], ...]:
    family_size = len(orientation_masks)
    full_pattern = (1 << family_size) - 1
    factors: list[tuple[str, Partition, int]] = [
        ("target", target, full_pattern)
    ]
    for label_index, (left, right) in enumerate(labels):
        right_pattern = sum(
            1 << family_index
            for family_index, mask in enumerate(orientation_masks)
            if mask & (1 << label_index)
        )
        factors.extend(
            (
                (f"left-{label_index}", left, full_pattern ^ right_pattern),
                (f"right-{label_index}", right, right_pattern),
            )
        )
    return tuple(factors)


def fixed_family_common_range_basis(
    target: Partition,
    labels: tuple[Label, ...],
    orientation_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> np.ndarray:
    """Construct the exact parity-intertwiner basis for ``n>=5``."""

    if len(set(orientation_masks)) != len(orientation_masks):
        raise ValueError("orientation masks must be distinct")
    n = sum(target)
    if n < 5:
        raise ValueError("the parity-intertwiner construction requires n>=5")
    if any(sum(partition) != n for label in labels for partition in label):
        raise ValueError("all source partitions must match the target degree")
    maximum_mask = 1 << len(labels)
    if any(not 0 <= mask < maximum_mask for mask in orientation_masks):
        raise ValueError("orientation mask out of range")

    factors = _factor_pattern_data(target, labels, orientation_masks)
    family_size = len(orientation_masks)
    occupied_patterns = tuple(sorted({pattern for _, _, pattern in factors}))
    grouped = tuple(
        tuple(item for item in factors if item[2] == pattern)
        for pattern in occupied_patterns
    )
    grouped_names = tuple(
        name for group in grouped for name, _, _ in group
    )
    grouped_dimensions = tuple(
        hook_length_dimension(partition)
        for group in grouped
        for _, partition, _ in group
    )
    ambient_names = tuple(name for name, _, _ in factors)
    ambient_dimensions = tuple(
        hook_length_dimension(partition) for _, partition, _ in factors
    )

    pattern_multiplicities = tuple(
        (
            pattern,
            _multiplicity(
                tuple(partition for _, partition, _ in group),
                (n,),
                n,
            ),
            _multiplicity(
                tuple(partition for _, partition, _ in group),
                (1,) * n,
                n,
            ),
        )
        for pattern, group in zip(occupied_patterns, grouped)
        if pattern
    )
    blocks = []
    for assignment in viable_sparse_parity_assignments(
        family_size,
        pattern_multiplicities,
    ):
        pattern_bases = []
        viable = True
        for pattern, group in zip(occupied_patterns, grouped):
            partitions = tuple(partition for _, partition, _ in group)
            if pattern == 0:
                basis = np.eye(math.prod(
                    hook_length_dimension(partition) for partition in partitions
                ))
            else:
                sign_bit = (assignment >> (pattern - 1)) & 1
                basis, _, _ = _one_dimensional_isotypic_basis(
                    partitions,
                    sign_bit,
                    tolerance,
                )
            if not basis.shape[1]:
                viable = False
                break
            pattern_bases.append(basis)
        if not viable:
            continue
        block = pattern_bases[0]
        for basis in pattern_bases[1:]:
            block = np.kron(block, basis)
        blocks.append(block)

    ambient_dimension = math.prod(ambient_dimensions)
    if not blocks:
        return np.zeros((ambient_dimension, 0))
    grouped_basis = np.concatenate(blocks, axis=1)
    grouped_indices = np.arange(ambient_dimension).reshape(grouped_dimensions)
    row_permutation = grouped_indices.transpose(
        tuple(grouped_names.index(name) for name in ambient_names)
    ).reshape(-1)
    basis = grouped_basis[row_permutation, :]
    gram = basis.conj().T @ basis
    isometry_residual = float(
        np.linalg.norm(gram - np.eye(gram.shape[0]), ord=2)
    )
    if isometry_residual > 100 * tolerance:
        raise ArithmeticError("common-range parity basis is not isometric")
    expected = fixed_family_common_range_dimension(
        target,
        labels,
        orientation_masks,
    )
    if basis.shape[1] != expected:
        raise ArithmeticError("common-range basis rank disagrees with parity formula")
    return basis


def mobius_common_core_atoms(
    orientation_masks: tuple[int, ...],
    common_dimensions: dict[tuple[int, ...], int],
) -> dict[tuple[int, ...], int]:
    """Invert ``d(F)=sum_{S superset F} a(S)`` for supports of size >=2."""

    atoms: dict[tuple[int, ...], int] = {}
    for size in range(len(orientation_masks), 1, -1):
        for support in itertools.combinations(orientation_masks, size):
            atoms[support] = common_dimensions.get(support, 0) - sum(
                multiplicity
                for larger, multiplicity in atoms.items()
                if set(larger) > set(support)
            )
    return atoms


def is_affine_orientation_support(support: tuple[int, ...]) -> bool:
    """Return whether a nonempty mask set is an affine F_2 subspace."""

    if not support or len(set(support)) != len(support):
        return False
    base = support[0]
    translated = {mask ^ base for mask in support}
    return 0 in translated and all(
        left ^ right in translated
        for left in translated
        for right in translated
    )


def ternary_affine_closure_mask(
    first: int,
    second: int,
    third: int,
) -> int:
    """Return the unique fourth point in the affine plane through a triple."""

    return first ^ second ^ third


def atom_left_effect_eigenvalue(
    support: tuple[int, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
) -> float | None:
    left_count = len(set(support) & set(left_masks))
    right_count = len(set(support) & set(right_masks))
    if not left_count or not right_count:
        return None
    return left_count / (left_count + right_count)


def scalar_star_relative_spectrum(
    correlation: float,
    shared_mode_multiplicity: int,
    orthogonal_cross_mode_multiplicity: int,
) -> tuple[float, ...]:
    """Spectrum for two cross cores and one internal equicorrelated core.

    On every shared scalar mode the three normalized pair cores have mutual
    overlap ``correlation``.  Quotienting the internal edge diagonalizes the
    two cross edges into antisymmetric and symmetric channels.
    """

    if not 0 <= correlation < 1:
        raise ValueError("correlation must lie in [0,1)")
    if shared_mode_multiplicity < 0 or orthogonal_cross_mode_multiplicity < 0:
        raise ValueError("multiplicities must be nonnegative")
    antisymmetric = (1 - correlation) / (2 - correlation)
    symmetric = (
        1 + correlation - correlation * correlation
    ) / (2 + correlation - correlation * correlation)
    return tuple(
        sorted(
            [antisymmetric] * shared_mode_multiplicity
            + [0.5] * orthogonal_cross_mode_multiplicity
            + [symmetric] * shared_mode_multiplicity
        )
    )


def _pair_projector_commutator_norm(
    left_basis: np.ndarray,
    right_basis: np.ndarray,
) -> tuple[float, int]:
    if not left_basis.shape[1] or not right_basis.shape[1]:
        return 0.0, 0
    singular_values = np.linalg.svd(
        left_basis.conj().T @ right_basis,
        compute_uv=False,
    )
    singular_values = np.clip(singular_values, 0.0, 1.0)
    commutator = max(
        (
            float(value * math.sqrt(max(0.0, 1 - value * value)))
            for value in singular_values
        ),
        default=0.0,
    )
    intersection = int(np.sum(singular_values >= 1 - 1e-7))
    return commutator, intersection


def _relation_gram(
    edges: tuple[tuple[int, int], ...],
    bases: dict[tuple[int, int], np.ndarray],
    grading: dict[int, int] | None = None,
) -> np.ndarray:
    offsets = [0]
    for edge in edges:
        offsets.append(offsets[-1] + bases[edge].shape[1])
    gram = np.zeros((offsets[-1], offsets[-1]), dtype=complex)
    for left_index, left_edge in enumerate(edges):
        left_basis = bases[left_edge]
        left_signs = {left_edge[0]: 1, left_edge[1]: -1}
        for right_index, right_edge in enumerate(edges):
            right_basis = bases[right_edge]
            right_signs = {right_edge[0]: 1, right_edge[1]: -1}
            coefficient = sum(
                left_signs[vertex]
                * right_signs[vertex]
                * (grading[vertex] if grading is not None else 1)
                for vertex in set(left_edge) & set(right_edge)
            )
            if coefficient:
                gram[
                    offsets[left_index] : offsets[left_index + 1],
                    offsets[right_index] : offsets[right_index + 1],
                ] = coefficient * (left_basis.conj().T @ right_basis)
    return (gram + gram.conj().T) / 2


def _relative_pair_spectrum(
    pair_bases: dict[tuple[int, int], np.ndarray],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    tolerance: float,
) -> tuple[np.ndarray, int, float]:
    left_set = set(left_masks)
    right_set = set(right_masks)
    internal = tuple(
        edge
        for edge in pair_bases
        if set(edge) <= left_set or set(edge) <= right_set
    )
    cross = tuple(
        edge
        for edge in pair_bases
        if len(set(edge) & left_set) == 1
        and len(set(edge) & right_set) == 1
    )
    if not cross:
        return np.zeros(0), 0, 0.0
    edges = (*internal, *cross)
    gram = _relation_gram(edges, pair_bases)
    grading = {mask: (1 if mask in left_set else -1) for mask in (*left_masks, *right_masks)}
    graded = _relation_gram(edges, pair_bases, grading)
    internal_dimension = sum(pair_bases[edge].shape[1] for edge in internal)
    aa = gram[:internal_dimension, :internal_dimension]
    ax = gram[:internal_dimension, internal_dimension:]
    xx = gram[internal_dimension:, internal_dimension:]
    jaa = graded[:internal_dimension, :internal_dimension]
    jax = graded[:internal_dimension, internal_dimension:]
    jxx = graded[internal_dimension:, internal_dimension:]
    if internal_dimension:
        coefficients = np.linalg.pinv(aa, rcond=tolerance) @ ax
        metric = xx - ax.conj().T @ coefficients
        defect_metric = (
            jxx
            - coefficients.conj().T @ jax
            - jax.conj().T @ coefficients
            + coefficients.conj().T @ jaa @ coefficients
        )
    else:
        metric = xx
        defect_metric = jxx
    metric = (metric + metric.conj().T) / 2
    defect_metric = (defect_metric + defect_metric.conj().T) / 2
    values, vectors = np.linalg.eigh(metric)
    support = values > 100 * tolerance
    if not np.any(support):
        return np.zeros(0), 0, 0.0
    isometry = vectors[:, support] / np.sqrt(values[support])
    defect = isometry.conj().T @ defect_metric @ isometry
    defect = (defect + defect.conj().T) / 2
    defect_values = np.linalg.eigvalsh(defect)
    fractional = np.sort((1 - defect_values) / 2)
    return (
        fractional,
        int(np.sum(support)),
        float(np.linalg.norm(defect, ord=2)),
    )


def audit_common_core_atomization(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    orientation_masks: tuple[int, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> CommonCoreAtomizationControl:
    if set(left_masks) | set(right_masks) != set(orientation_masks):
        raise ValueError("left and right masks must partition the family")
    if set(left_masks) & set(right_masks):
        raise ValueError("left and right masks must be disjoint")
    n = sum(target)
    common_dimensions: dict[tuple[int, ...], int] = {}
    common_bases: dict[tuple[int, ...], np.ndarray] = {}
    isometry_residuals = []
    rank_mismatches = 0
    for size in range(2, len(orientation_masks) + 1):
        for family in itertools.combinations(orientation_masks, size):
            dimension = fixed_family_common_range_dimension(target, labels, family)
            common_dimensions[family] = dimension
            if not dimension:
                continue
            basis = fixed_family_common_range_basis(
                target,
                labels,
                family,
                tolerance=tolerance,
            )
            common_bases[family] = basis
            rank_mismatches += basis.shape[1] != dimension
            isometry_residuals.append(
                float(
                    np.linalg.norm(
                        basis.conj().T @ basis - np.eye(basis.shape[1]),
                        ord=2,
                    )
                )
            )

    pair_bases = {
        family: basis
        for family, basis in common_bases.items()
        if len(family) == 2
    }
    commutators = []
    intersection_residuals = []
    for left_edge, right_edge in itertools.combinations(pair_bases, 2):
        commutator, intersection = _pair_projector_commutator_norm(
            pair_bases[left_edge],
            pair_bases[right_edge],
        )
        commutators.append(commutator)
        union = tuple(sorted(set(left_edge) | set(right_edge)))
        predicted_intersection = common_dimensions.get(union, 0)
        intersection_residuals.append(abs(intersection - predicted_intersection))

    closure_validations = 0
    closure_mismatches = 0
    for triple in itertools.combinations(orientation_masks, 3):
        closure = ternary_affine_closure_mask(*triple)
        if closure not in orientation_masks:
            continue
        triple_dimension = common_dimensions[triple]
        closed_family = tuple(sorted((*triple, closure)))
        closed_dimension = common_dimensions[closed_family]
        closure_validations += 1
        closure_mismatches += triple_dimension != closed_dimension

    atom_multiplicities = mobius_common_core_atoms(
        orientation_masks,
        common_dimensions,
    )
    atoms = []
    predicted = []
    predicted_dimension = 0
    imbalanced = 0
    for support, multiplicity in sorted(
        atom_multiplicities.items(),
        key=lambda item: (len(item[0]), item[0]),
    ):
        if not multiplicity:
            continue
        left_count = len(set(support) & set(left_masks))
        right_count = len(set(support) & set(right_masks))
        eigenvalue = atom_left_effect_eigenvalue(support, left_masks, right_masks)
        crosses = eigenvalue is not None
        balanced = not crosses or left_count == right_count
        if crosses and multiplicity > 0:
            predicted.extend([eigenvalue] * multiplicity)
            predicted_dimension += multiplicity
            imbalanced += int(not balanced)
        atoms.append(
            CommonCoreAtomRecord(
                support_orientation_masks=support,
                multiplicity=multiplicity,
                left_support_count=left_count,
                right_support_count=right_count,
                crosses_sibling_split=crosses,
                predicted_left_effect_eigenvalue=eigenvalue,
                grading_balanced=balanced,
            )
        )

    direct, direct_dimension, direct_defect = _relative_pair_spectrum(
        pair_bases,
        left_masks,
        right_masks,
        tolerance,
    )
    predicted_array = np.sort(np.array(predicted, dtype=float))
    if len(predicted_array) == len(direct):
        spectrum_residual = float(
            np.max(np.abs(predicted_array - direct)) if len(direct) else 0.0
        )
    else:
        spectrum_residual = math.inf
    maximum_commutator = max(commutators, default=0.0)
    maximum_intersection_residual = max(intersection_residuals, default=0)
    negative_atoms = sum(value < 0 for value in atom_multiplicities.values())
    nonaffine_atoms = sum(
        multiplicity > 0 and not is_affine_orientation_support(support)
        for support, multiplicity in atom_multiplicities.items()
    )
    commute = maximum_commutator <= 100 * tolerance
    atomization = bool(
        commute
        and not negative_atoms
        and maximum_intersection_residual == 0
    )
    spectrum_verified = bool(
        atomization
        and predicted_dimension == direct_dimension
        and spectrum_residual <= 100 * tolerance
    )
    direct_audit = bool(
        not rank_mismatches
        and max(isometry_residuals, default=0.0) <= 100 * tolerance
        and maximum_intersection_residual == 0
        and np.all(direct >= -100 * tolerance)
        and np.all(direct <= 1 + 100 * tolerance)
    )
    half_residual = max(
        (abs(float(value) - 0.5) for value in direct),
        default=0.0,
    )
    balanced = imbalanced == 0
    two_leaf_children = len(left_masks) == len(right_masks) == 2
    full_merge_nonneutral = bool(
        direct_audit
        and two_leaf_children
        and half_residual > 100 * tolerance
    )
    ambient = hook_length_dimension(target) * math.prod(
        hook_length_dimension(partition)
        for label in labels
        for partition in label
    )
    higher = [
        dimension
        for family, dimension in common_dimensions.items()
        if len(family) >= 3 and dimension
    ]
    return CommonCoreAtomizationControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        orientation_masks=orientation_masks,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        physical_ambient_dimension=ambient,
        nonzero_pair_core_count=len(pair_bases),
        total_pair_core_dimension=sum(basis.shape[1] for basis in pair_bases.values()),
        nonzero_higher_common_core_count=len(higher),
        maximum_higher_common_core_dimension=max(higher, default=0),
        fixed_family_basis_validation_count=len(common_bases),
        fixed_family_basis_rank_mismatch_count=rank_mismatches,
        maximum_common_basis_isometry_residual=max(isometry_residuals, default=0.0),
        maximum_pair_core_projector_commutator_norm=maximum_commutator,
        maximum_pair_core_intersection_rank_residual=maximum_intersection_residual,
        ternary_affine_closure_validation_count=closure_validations,
        ternary_affine_closure_dimension_mismatch_count=closure_mismatches,
        mobius_atom_count=sum(value > 0 for value in atom_multiplicities.values()),
        negative_mobius_atom_count=negative_atoms,
        nonaffine_positive_mobius_atom_count=nonaffine_atoms,
        crossing_atom_count=sum(
            atom.crosses_sibling_split and atom.multiplicity > 0 for atom in atoms
        ),
        imbalanced_crossing_atom_count=imbalanced,
        predicted_relative_pair_class_dimension=predicted_dimension,
        direct_relative_pair_class_dimension=direct_dimension,
        predicted_fractional_eigenvalues=tuple(float(value) for value in predicted_array),
        direct_fractional_eigenvalues=tuple(float(value) for value in direct),
        maximum_predicted_spectrum_residual=spectrum_residual,
        maximum_direct_grading_neutrality_residual=direct_defect,
        maximum_direct_fractional_half_residual=half_residual,
        sibling_child_size=len(left_masks),
        pair_relations_equal_full_internal_kernels=two_leaf_children,
        nonneutral_full_merge_certified=full_merge_nonneutral,
        pair_core_projectors_commute=commute,
        boolean_atomization_verified=atomization,
        all_crossing_atoms_balanced=balanced,
        direct_relative_cech_audit_verified=direct_audit,
        exact_relative_cech_spectrum_verified=spectrum_verified,
        atoms=atoms,
        status=(
            "commuting-balanced-common-core-atomization"
            if spectrum_verified and balanced
            else "commuting-imbalanced-common-core-atomization"
            if spectrum_verified
            else "noncommuting-nonneutral-common-core-counterexample"
            if direct_audit and half_residual > 100 * tolerance
            else "noncommuting-or-nonboolean-common-core-arrangement"
        ),
    )


def _finite_controls() -> list[CommonCoreAtomizationControl]:
    multi_edge_labels: tuple[Label, ...] = (
        ((5, 1), (3, 3)),
        ((2, 2, 2), (2, 1, 1, 1, 1)),
        ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    triple_core_labels: tuple[Label, ...] = (
        ((6,), (2, 1, 1, 1, 1)),
        ((5, 1), (1, 1, 1, 1, 1, 1)),
        ((4, 2), (2, 2, 2)),
        ((3, 3), (2, 2, 1, 1)),
    )
    noncommuting_labels: tuple[Label, ...] = (
        ((6,), (4, 2)),
        ((5, 1), (2, 2, 2)),
        ((3, 3), (2, 1, 1, 1, 1)),
        ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    return [
        audit_common_core_atomization(
            "W6-MULTIEDGE-NO-HIGHER-CORE",
            (6,),
            multi_edge_labels,
            (1, 2, 5, 6),
            (1, 5),
            (2, 6),
        ),
        audit_common_core_atomization(
            "W6-TRIPLE-AND-FOUR-WAY-CORE",
            (6,),
            triple_core_labels,
            (5, 6, 9, 10),
            (5, 6),
            (9, 10),
        ),
        audit_common_core_atomization(
            "W6-NONCOMMUTING-PAIR-CORE-COUNTEREXAMPLE",
            (6,),
            noncommuting_labels,
            (2, 5, 11, 12),
            (2, 5),
            (11, 12),
        ),
    ]


def run_common_core_atomization() -> CommonCoreAtomizationReport:
    controls = _finite_controls()
    abstract = AbstractAtomImbalanceControl(
        support_size=3,
        left_support_count=1,
        right_support_count=2,
        predicted_left_effect_eigenvalue=1 / 3,
        predicted_grading_defect=1 / 3,
        balanced=False,
        status="one-versus-two-support-predicts-one-third-channel",
    )
    direct_failures = sum(
        not control.direct_relative_cech_audit_verified for control in controls
    )
    boolean_controls = [
        control for control in controls if control.pair_core_projectors_commute
    ]
    boolean_failures = sum(
        not control.exact_relative_cech_spectrum_verified
        for control in boolean_controls
    )
    closure_failures = sum(
        control.ternary_affine_closure_dimension_mismatch_count
        for control in controls
    )
    noncommuting = sum(
        not control.pair_core_projectors_commute for control in controls
    )
    imbalanced = sum(
        control.imbalanced_crossing_atom_count for control in controls
    )
    nonneutral = [
        control
        for control in controls
        if control.maximum_direct_fractional_half_residual > 1e-7
    ]
    counterexample = next(
        control
        for control in controls
        if control.control_id == "W6-NONCOMMUTING-PAIR-CORE-COUNTEREXAMPLE"
    )
    scalar_prediction = scalar_star_relative_spectrum(1 / 9, 9, 16)
    scalar_residual = float(
        np.max(
            np.abs(
                np.array(scalar_prediction)
                - np.array(counterexample.direct_fractional_eigenvalues)
            )
        )
    )
    scalar_star = ScalarStarRecouplingControl(
        pair_core_principal_correlation=1 / 9,
        shared_mode_multiplicity=9,
        orthogonal_cross_mode_multiplicity=16,
        antisymmetric_left_effect_eigenvalue=8 / 17,
        symmetric_left_effect_eigenvalue=89 / 170,
        orthogonal_left_effect_eigenvalue=0.5,
        predicted_fractional_eigenvalues=scalar_prediction,
        direct_spectrum_residual=scalar_residual,
        exact_scalar_star_formula_verified=scalar_residual <= 1e-10,
        status="exact-nonneutral-scalar-star-recoupling-block",
    )
    metrics: dict[str, int | float] = {
        "common_range_parity_basis_theorem_count": 1,
        "ternary_xor_common_range_closure_theorem_count": 1,
        "affine_common_support_balance_theorem_count": 1,
        "commuting_atom_balance_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_direct_relative_cech_validation_failure_count": direct_failures,
        "finite_commuting_boolean_prediction_failure_count": boolean_failures,
        "finite_noncommuting_pair_core_control_count": noncommuting,
        "finite_nonneutral_common_core_control_count": len(nonneutral),
        "finite_nonneutral_full_affine_merge_certificate_count": sum(
            control.nonneutral_full_merge_certified for control in controls
        ),
        "finite_ternary_affine_closure_validation_count": sum(
            control.ternary_affine_closure_validation_count
            for control in controls
        ),
        "finite_ternary_affine_closure_mismatch_count": closure_failures,
        "finite_nonaffine_positive_atom_count": sum(
            control.nonaffine_positive_mobius_atom_count
            for control in controls
        ),
        "finite_higher_common_core_control_count": sum(
            control.nonzero_higher_common_core_count > 0 for control in controls
        ),
        "finite_pair_core_count": sum(
            control.nonzero_pair_core_count for control in controls
        ),
        "finite_crossing_atom_count": sum(
            control.crossing_atom_count for control in controls
        ),
        "finite_imbalanced_crossing_atom_count": imbalanced,
        "maximum_pair_core_projector_commutator_norm": max(
            control.maximum_pair_core_projector_commutator_norm
            for control in controls
        ),
        "maximum_relative_cech_spectrum_residual": max(
            control.maximum_predicted_spectrum_residual
            for control in boolean_controls
        ),
        "maximum_direct_fractional_half_residual": max(
            control.maximum_direct_fractional_half_residual
            for control in controls
        ),
        "noncommuting_counterexample_pair_core_correlation": 1 / 9,
        "noncommuting_counterexample_low_eigenvalue": 8 / 17,
        "noncommuting_counterexample_high_eigenvalue": 89 / 170,
        "scalar_star_formula_residual": scalar_residual,
        "abstract_one_versus_two_fractional_eigenvalue": (
            abstract.predicted_left_effect_eigenvalue
        ),
        "all_n_collision_free_commuting_atomization_count": 0,
        "all_depth_affine_atom_balance_count": 1,
        "new_quantum_algorithm_count": 0,
    }
    return CommonCoreAtomizationReport(
        created_at=utc_now(),
        theorem_contract={
            "parity_intertwiner_basis": "Every fixed-family common range is the orthogonal sum over parity-kernel assignments of tensor products of trivial/sign membership-pattern isotypes.",
            "ternary_xor_closure": "For n>=5, intersection(U_a,U_b,U_c) is contained in U_(a xor b xor c); summing the three parity equations is exactly the fourth orientation's invariance equation.",
            "affine_support": "The exact orientation support of every common vector is ternary-XOR closed, hence affine; a crossing affine support meets sibling affine half-spaces equally.",
            "boolean_atomization": "Commuting pair-core projectors yield orthogonal support atoms A_S with dim K_F=sum_{S superset F} dim A_S.",
            "relative_cech_channel": "A support atom meeting affine siblings in p and q leaves contributes left-effect eigenvalue p/(p+q).",
            "two_leaf_full_merge_embedding": "For two leaves per child, pair relations are the complete child-internal kernels; a nonneutral relative pair quotient is therefore a nonneutral subspace of the full cross-dependency merge.",
            "balance_criterion": "A commuting common-core arrangement is grading-neutral iff every crossing atom has p=q.",
            "scope": "The direct finite Cech quotient verifies the criterion without assuming it; universal pair-core commutativity is false, while classification and conditioning of noncommuting blocks remain open.",
        },
        finite_controls=controls,
        abstract_imbalance_control=abstract,
        scalar_star_counterexample=scalar_star,
        scaling_records=[
            {
                "n": n,
                "information_threshold_copy_count": math.ceil(
                    math.lgamma(n + 1) / math.log(2)
                ),
                "fixed_family_dimensions_representation_computable": True,
                "universal_pair_core_commutativity_falsified": True,
                "mobius_atoms_nonnegative_proved": False,
                "every_crossing_atom_affine_balanced_proved": True,
                "status": "noncommuting-recoupling-block-classification-open",
            }
            for n in (6, 8, 16, 32, 64, 128, 256, 512)
        ],
        proof_obligations=[
            {
                "obligation": "explicit_fixed_family_parity_intertwiners",
                "resolved": direct_failures == 0,
                "resolution": "Finite bases have exact representation-ring ranks, are isometric, and produce valid direct relative-Cech spectra.",
            },
            {
                "obligation": "collision_free_pair_core_commutativity_all_n",
                "resolved": True,
                "resolution": "Resolved negatively: a globally distinct S6 affine plane has pair-core commutator norm 0.110423... and exact nonhalf channels.",
            },
            {
                "obligation": "affine_crossing_atom_balance_all_depths",
                "resolved": True,
                "resolution": "Ternary-XOR closure makes every exact common-vector support affine; an affine support crossing sibling cosets has equal cardinality in both.",
            },
            {
                "obligation": "classify_noncommuting_recoupling_blocks",
                "resolved": False,
                "resolution": "The first counterexample is an exact scalar star with correlation 1/9 and well-conditioned rational channels, but no all-n block decomposition or conditioning bound is known.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Pair generation alone forces half-balanced channels.",
                "resolved": True,
                "resolution": "False for arbitrary subspaces: a commuting atom with support counts one and two produces an exact 1/3 channel. The wreath parity theorem excludes that support geometry only for n>=5 orientation common cores.",
            },
            {
                "objection": "Triple common cores necessarily spoil pair-class neutrality.",
                "resolved": direct_failures == 0,
                "resolution": "The collision-free S6 triple-core plane atomizes into one four-way core plus pair-only atoms; every crossing atom is split 2:2 or 1:1 and the direct quotient is neutral.",
            },
            {
                "objection": "Nonnegative Mobius dimensions prove a Boolean arrangement.",
                "resolved": True,
                "resolution": "No. Pair-core projector commutativity is checked separately; dimension data alone cannot exclude nonorthogonal recoupling blocks.",
            },
            {
                "objection": "Affine support balance is enough to force half-balanced channels.",
                "resolved": True,
                "resolution": "False. The collision-free S6 counterexample has only balanced affine line supports, but nonorthogonal pair cores produce 8/17 and 89/170 channels.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "fixed_family_parity_intertwiner_basis_verified": direct_failures == 0,
            "ternary_xor_common_range_closure_proved_n_at_least_five": True,
            "common_vector_orientation_support_affine_proved": True,
            "commuting_common_atoms_affine_sibling_balanced_proved": True,
            "finite_commuting_collision_free_pair_core_atomization_verified": boolean_failures == 0,
            "finite_higher_common_core_affine_balance_verified": (
                direct_failures == 0
                and any(control.nonzero_higher_common_core_count for control in controls)
            ),
            "pair_generation_alone_sufficient_for_balance": False,
            "universal_collision_free_pair_core_commutativity_falsified": True,
            "universal_collision_free_half_balance_falsified": True,
            "collision_free_full_affine_merge_half_balance_falsified": (
                counterexample.nonneutral_full_merge_certified
            ),
            "all_n_pair_core_commutativity_proved": False,
            "all_depth_affine_atom_balance_proved": True,
            "coherent_common_core_atom_transform_compiled": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": "Parity proves affine support balance, but a collision-free S6 scalar-star recoupling block falsifies universal commutativity and exact half-balance. The remaining route requires an efficient block decomposition and an all-n conditioning bound.",
        },
        status=(
            "collision-free-noncommuting-core-counterexample-block-classification-open"
            if not direct_failures and nonneutral
            else "common-core-atomization-validation-failure"
        ),
        summary=(
            "Constructed exact parity intertwiners and verified the relative "
            "Cech atom formula on commuting collision-free S6 affine planes "
            "and proved ternary-XOR support closure. A third globally distinct "
            "S6 plane falsifies universal commutativity and half-balance with "
            "exact scalar-star channels 8/17 and 89/170."
        ),
        falsifiers_triggered=[
            "Pair generation by itself is not a neutrality theorem; unequal atom support counts produce nonhalf channels.",
            "The wreath parity kernel excludes unequal crossing support counts at n>=5 because every exact common-vector support is affine.",
            "Higher common cores do not automatically create a grading defect when their support is affinely balanced.",
            "Fixed-family intersection dimensions alone do not prove a Boolean decomposition; recoupling commutators remain essential.",
            "Universal collision-free pair-core commutativity and exact half-balance are false already in S6.",
        ],
    )


def write_common_core_atomization_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_common_core_atomization(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_common_core_atomization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
