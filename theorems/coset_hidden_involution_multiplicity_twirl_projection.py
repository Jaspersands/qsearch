"""Compressed twirl projection for hyperoctahedral multiplicity blocks.

Let ``K_m=C_2 wr S_m`` and let an ``S_(2m)`` irrep ``V_lambda`` contain a
``K_m`` irrep ``mu`` with multiplicity ``b``.  On its isotypic component,

    V_lambda[mu] ~= C^b tensor V_mu,

the conjugation twirl of any ambient operator is the Hilbert--Schmidt
projection onto

    End_K(V_lambda[mu]) ~= M_b tensor I_(V_mu).           (1)

Consequently a ``K_m``-orbit sum need not be constructed by enumerating its
possibly large orbit.  Compress one representative to the isotypic component
and project it onto the small commutant in (1).  For Hermitian orbit sums the
target has only ``b(b+1)/2`` real symmetric coordinates.

This module implements that reduction for arbitrary bipartitions
``mu=(alpha,beta)``.  It projects to one signed ``C_2^m`` weight sector,
isolates ``alpha`` and ``beta`` with the two stabilizer Casimirs, transports
all equal-weight sectors to the reference sector, and projects under
``S_|alpha| x S_|beta|``.  An explicit full ``K_4`` twirl validates this
compressed identity independently.  Exact branching dimensions gate every
selected isotypic block.

The compressed method reproduces the known support thresholds on repeated
multiplicity-two blocks:

    m=5: support <=4 is proper; support <=5 gives M_2,
    m=6: support <=5 is proper; support <=6 gives M_2.

At ``m=7`` it finds that support at most six already gives ``M_2`` on the
continuation ``lambda=(10,4), alpha=(5,2)`` and on three further low-
does not justify extrapolating a strict rank-tracking law or an unbounded-
support theorem.  A multiplicity-three block closes at support five, while
three nontrivial-``beta`` controls close at support four.  Support six could
still fail on other or asymptotically natural blocks.

This is a classical diagnostic, not a coherent transform.  It avoids orbit-
matrix construction in the audit, but does not compile the isotypic basis,
the commutant projection, a source-aware polar, or a hidden-involution
measurement on a quantum computer.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    Permutation,
    _K_generators,
    moved_point_support,
)
from coset_hidden_involution_commutant_support_growth_boundary import (
    _adjacent_word,
    _matrix_for_permutation,
    hyperoctahedral_group,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    hyperoctahedral_branching_coefficient,
)
from coset_hidden_involution_rank_tracking_commutant_witness import (
    bounded_support_permutations,
)
from coset_jucys_murphy_label_transform import (
    standard_young_tableaux,
    tableau_positions,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_multiplicity_twirl_projection.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-TWIRL-PROJECTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SupportCutoffAlgebraStep:
    maximum_moved_point_support: int
    hermitian_orbit_representative_count: int
    symmetric_commutant_span_dimension: int
    generated_copy_algebra_dimension: int
    exact_copy_algebra_dimension: int
    generates_full_copy_algebra: bool
    status: str


@dataclass(frozen=True)
class MultiplicityTwirlProjectionControl:
    half_degree: int
    symmetric_partition: Partition
    hyperoctahedral_partition: Partition
    negative_hyperoctahedral_partition: Partition
    selected_character_negative_pair_count: int
    symmetric_irrep_dimension: int
    hyperoctahedral_irrep_dimension: int
    exact_branching_multiplicity: int
    pair_flip_fixed_space_dimension: int
    expected_isotypic_dimension: int
    observed_isotypic_dimension: int
    symmetric_commutant_dimension: int
    full_copy_algebra_dimension: int
    maximum_support_audited: int
    total_hermitian_orbit_representative_count: int
    support_steps: list[SupportCutoffAlgebraStep]
    minimum_full_copy_algebra_support: int | None
    first_full_support_witness: Permutation | None
    first_full_support_witness_cycles: tuple[tuple[int, ...], ...]
    maximum_pair_flip_projector_residual: float
    maximum_isotypic_projector_residual: float
    maximum_symmetric_commutant_orthogonality_residual: float
    maximum_symmetric_commutant_K_commutator_residual: float
    maximum_sparse_representation_action_residual: float
    compressed_twirl_projection_verified: bool
    finite_control_only: bool
    status: str


@dataclass(frozen=True)
class MultiplicityTwirlProjectionTheorem:
    commutant_projection: str
    flip_trivial_isotypic_extraction: str
    signed_weight_isotypic_extraction: str
    orbit_enumeration_reduction: str
    reproduced_thresholds: str
    rank_seven_falsifier: str
    scope: str
    hilbert_schmidt_twirl_projection_proved: bool
    compressed_orbit_representative_method_verified: bool
    multiplicity_three_block_verified: bool
    nontrivial_beta_blocks_verified: bool
    rank_five_six_thresholds_reproduced: bool
    strict_rank_tracking_support_growth_falsified: bool
    universal_support_six_generation_proved: bool
    unbounded_support_requirement_proved: bool
    coherent_commutant_transform_compiled: bool
    hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ExactSignedTwirlValidation:
    half_degree: int
    symmetric_partition: Partition
    hyperoctahedral_partition: Partition
    negative_hyperoctahedral_partition: Partition
    hyperoctahedral_group_order: int
    selected_character_isotypic_dimension: int
    projected_restriction_residual: float
    validation_passed: bool
    status: str


@dataclass(frozen=True)
class MultiplicityTwirlProjectionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: MultiplicityTwirlProjectionTheorem
    exact_signed_twirl_validation: ExactSignedTwirlValidation
    controls: list[MultiplicityTwirlProjectionControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _pair_permutation(half_degree: int, permutation: Permutation) -> Permutation:
    if len(permutation) != half_degree:
        raise ValueError("pair permutation has the wrong degree")
    return tuple(
        point
        for pair in range(half_degree)
        for point in (2 * permutation[pair], 2 * permutation[pair] + 1)
    )


def _pair_flip(half_degree: int, pair: int) -> Permutation:
    output = list(range(2 * half_degree))
    output[2 * pair], output[2 * pair + 1] = (
        output[2 * pair + 1],
        output[2 * pair],
    )
    return tuple(output)


def _pair_transposition(
    half_degree: int,
    left: int,
    right: int,
) -> Permutation:
    permutation = list(range(half_degree))
    permutation[left], permutation[right] = (
        permutation[right],
        permutation[left],
    )
    return _pair_permutation(half_degree, tuple(permutation))


def partition_content(partition: Partition) -> int:
    return sum(
        column - row
        for row, length in enumerate(partition)
        for column in range(length)
    )


def permutation_cycles(permutation: Permutation) -> tuple[tuple[int, ...], ...]:
    seen: set[int] = set()
    output: list[tuple[int, ...]] = []
    for start in range(len(permutation)):
        if start in seen or permutation[start] == start:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        output.append(tuple(cycle))
    return tuple(output)


@lru_cache(maxsize=None)
def hermitian_bounded_support_orbit_representatives(
    half_degree: int,
    maximum_support: int,
) -> tuple[Permutation, ...]:
    """Enumerate one representative per K-conjugacy/inverse orbit.

    Generator BFS visits every bounded-support permutation once and avoids the
    previous full-``K`` enumeration for every candidate representative.
    """

    if half_degree < 2 or not 2 <= maximum_support <= 2 * half_degree:
        raise ValueError("invalid half degree or support cutoff")
    generators = _K_generators(half_degree)
    seen: set[Permutation] = set()
    output: list[Permutation] = []
    for permutation in bounded_support_permutations(
        2 * half_degree,
        maximum_support,
    ):
        if permutation in seen:
            continue
        inverse = inverse_permutation(permutation)
        orbit = {permutation, inverse}
        queue = [permutation] if inverse == permutation else [permutation, inverse]
        for element in queue:
            for generator in generators:
                conjugate = compose_permutations(
                    compose_permutations(generator, element),
                    generator,
                )
                for candidate in (
                    conjugate,
                    inverse_permutation(conjugate),
                ):
                    if candidate not in orbit:
                        orbit.add(candidate)
                        queue.append(candidate)
        seen.update(orbit)
        output.append(min(orbit))
    return tuple(output)


@lru_cache(maxsize=None)
def _seminormal_sparse_data(
    symmetric_partition: Partition,
) -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray], ...]:
    """Construct Young-seminormal generators without dense d-by-d matrices."""

    tableaux = standard_young_tableaux(symmetric_partition)
    index = {tableau: position for position, tableau in enumerate(tableaux)}
    positions = [tableau_positions(tableau) for tableau in tableaux]
    output = []
    for adjacent in range(1, sum(symmetric_partition)):
        diagonal = np.empty(len(tableaux), dtype=float)
        partner = np.arange(len(tableaux))
        coefficient = np.zeros(len(tableaux), dtype=float)
        for column, tableau in enumerate(tableaux):
            row_i, col_i = positions[column][adjacent - 1]
            row_j, col_j = positions[column][adjacent]
            axial_distance = (col_j - row_j) - (col_i - row_i)
            diagonal[column] = 1.0 / axial_distance
            if abs(axial_distance) == 1:
                continue
            mutable = [list(row) for row in tableau]
            mutable[row_i][col_i], mutable[row_j][col_j] = (
                mutable[row_j][col_j],
                mutable[row_i][col_i],
            )
            partner[column] = index[tuple(tuple(row) for row in mutable)]
            coefficient[column] = math.sqrt(
                1.0 - 1.0 / (axial_distance * axial_distance)
            )
        output.append((diagonal, partner, coefficient))
    return tuple(output)


def _signed_weight_rank(
    half_degree: int,
    symmetric_partition: Partition,
    negative_pair_count: int,
) -> int:
    positive_pair_count = half_degree - negative_pair_count
    return sum(
        hyperoctahedral_branching_coefficient(
            symmetric_partition,
            alpha,
            beta,
        )
        * hook_length_dimension(alpha)
        * hook_length_dimension(beta)
        for alpha in integer_partitions(positive_pair_count)
        for beta in integer_partitions(negative_pair_count)
    )


@lru_cache(maxsize=None)
def _signed_weight_workspace(
    half_degree: int,
    symmetric_partition: Partition,
    negative_pair_count: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple[Any, ...], float]:
    degree = 2 * half_degree
    if sum(symmetric_partition) != degree:
        raise ValueError("symmetric partition has the wrong degree")
    if not 0 <= negative_pair_count <= half_degree:
        raise ValueError("negative pair count is outside 0..m")
    positive_pair_count = half_degree - negative_pair_count
    dimension = hook_length_dimension(symmetric_partition)
    weight_rank = _signed_weight_rank(
        half_degree,
        symmetric_partition,
        negative_pair_count,
    )
    sparse_data = _seminormal_sparse_data(symmetric_partition)
    random = np.random.default_rng(
        20260903 + 97 * half_degree + 1009 * negative_pair_count + sum(
            (index + 1) * value
            for index, value in enumerate(symmetric_partition)
        )
    )
    projected = random.normal(size=(dimension, weight_rank))
    for pair in range(half_degree):
        acted = _apply_representation_sparse(
            _pair_flip(half_degree, pair),
            projected,
            sparse_data,
        )
        sign = 1.0 if pair < positive_pair_count else -1.0
        projected = (projected + sign * acted) / 2.0
    weight_basis, triangular = np.linalg.qr(projected, mode="reduced")
    if weight_basis.shape[1] != weight_rank or np.min(
        np.abs(np.diag(triangular))
    ) <= 1e-12:
        raise ArithmeticError("randomized signed-weight range basis lost exact rank")
    flip_residual = max(
        float(
            np.linalg.norm(
                _apply_representation_sparse(
                    _pair_flip(half_degree, pair),
                    weight_basis,
                    sparse_data,
                )
                - (1.0 if pair < positive_pair_count else -1.0)
                * weight_basis
            )
        )
        for pair in range(half_degree)
    )
    casimirs = []
    for indices in (
        range(positive_pair_count),
        range(positive_pair_count, half_degree),
    ):
        casimir = np.zeros((weight_basis.shape[1], weight_basis.shape[1]))
        for left, right in combinations(indices, 2):
            acted = _apply_representation_sparse(
                _pair_transposition(half_degree, left, right),
                weight_basis,
                sparse_data,
            )
            casimir += weight_basis.T @ acted
        casimirs.append((casimir + casimir.T) / 2.0)
    return (
        weight_basis,
        casimirs[0],
        casimirs[1],
        sparse_data,
        flip_residual,
    )


@lru_cache(maxsize=None)
def _flip_trivial_workspace(
    half_degree: int,
    symmetric_partition: Partition,
) -> tuple[np.ndarray, np.ndarray, tuple[Any, ...], float]:
    basis, positive_casimir, _, sparse_data, residual = _signed_weight_workspace(
        half_degree,
        symmetric_partition,
        0,
    )
    return basis, positive_casimir, sparse_data, residual


def _isotypic_basis(
    half_degree: int,
    symmetric_partition: Partition,
    hyperoctahedral_partition: Partition,
    negative_hyperoctahedral_partition: Partition = (),
    *,
    tolerance: float,
) -> tuple[np.ndarray, int, float, float]:
    negative_pair_count = sum(negative_hyperoctahedral_partition)
    if sum(hyperoctahedral_partition) + negative_pair_count != half_degree:
        raise ValueError("bipartition has the wrong rank")
    weight_basis, positive_casimir, negative_casimir, _, flip_residual = (
        _signed_weight_workspace(
            half_degree,
            symmetric_partition,
            negative_pair_count,
        )
    )
    multiplicity = hyperoctahedral_branching_coefficient(
        symmetric_partition,
        hyperoctahedral_partition,
        negative_hyperoctahedral_partition,
    )
    if multiplicity < 2:
        raise ValueError("a repeated hyperoctahedral branch is required")

    positive_target = partition_content(hyperoctahedral_partition)
    eigenvalues, eigenvectors = np.linalg.eigh(positive_casimir)
    positive_selected = np.abs(eigenvalues - positive_target) <= tolerance
    positive_basis = weight_basis @ eigenvectors[:, positive_selected]
    restricted_negative = (
        eigenvectors[:, positive_selected].T
        @ negative_casimir
        @ eigenvectors[:, positive_selected]
    )
    negative_target = partition_content(negative_hyperoctahedral_partition)
    negative_values, negative_vectors = np.linalg.eigh(
        (restricted_negative + restricted_negative.T) / 2.0
    )
    negative_selected = np.abs(negative_values - negative_target) <= tolerance
    isotypic = positive_basis @ negative_vectors[:, negative_selected]
    expected = (
        multiplicity
        * hook_length_dimension(hyperoctahedral_partition)
        * hook_length_dimension(negative_hyperoctahedral_partition)
    )
    if isotypic.shape[1] != expected:
        raise ArithmeticError(
            "signed-sector Casimirs do not isolate the requested bipartition"
        )
    isotypic_projector = isotypic @ isotypic.T
    return (
        isotypic,
        multiplicity,
        flip_residual,
        float(
            np.linalg.norm(
                isotypic_projector @ isotypic_projector - isotypic_projector
            )
        ),
    )


def _restricted_pair_generators(
    half_degree: int,
    negative_pair_count: int,
    isotypic_basis: np.ndarray,
    sparse_data: tuple[Any, ...],
) -> tuple[tuple[np.ndarray, ...], tuple[tuple[int, int], ...], int]:
    output = []
    swaps = []
    positive_pair_count = half_degree - negative_pair_count
    for start, size in (
        (0, positive_pair_count),
        (positive_pair_count, negative_pair_count),
    ):
        for pair in range(start, start + size - 1):
            acted = _apply_representation_sparse(
                _pair_transposition(half_degree, pair, pair + 1),
                isotypic_basis,
                sparse_data,
            )
            restricted = isotypic_basis.T @ acted
            output.append((restricted + restricted.T) / 2.0)
            swaps.append((pair, pair + 1))
    return (
        tuple(output),
        tuple(swaps),
        math.factorial(positive_pair_count) * math.factorial(negative_pair_count),
    )


def _symmetric_commutant_basis(
    half_degree: int,
    pair_generators: tuple[np.ndarray, ...],
    generator_swaps: tuple[tuple[int, int], ...],
    stabilizer_order: int,
    multiplicity: int,
    *,
    tolerance: float,
) -> tuple[tuple[np.ndarray, ...], float, float]:
    identity_permutation = tuple(range(half_degree))
    identity = np.eye(pair_generators[0].shape[0])
    representations = {identity_permutation: identity}
    queue = [identity_permutation]
    for permutation in queue:
        for (left, right), generator in zip(generator_swaps, pair_generators):
            adjacent = list(range(half_degree))
            adjacent[left], adjacent[right] = (
                adjacent[right],
                adjacent[left],
            )
            product = compose_permutations(permutation, tuple(adjacent))
            if product not in representations:
                representations[product] = representations[permutation] @ generator
                queue.append(product)
    if len(representations) != stabilizer_order:
        raise ArithmeticError("pair generators did not enumerate the signed-weight stabilizer")

    expected = multiplicity * (multiplicity + 1) // 2
    basis: list[np.ndarray] = []

    def add(matrix: np.ndarray) -> None:
        residual = (matrix + matrix.T) / 2.0
        for _ in range(2):
            for vector in basis:
                residual -= float(np.sum(vector * residual)) * vector
        norm = float(np.linalg.norm(residual))
        if norm > tolerance:
            basis.append(residual / norm)

    add(identity)
    random = np.random.default_rng(20260903 + half_degree)
    for _ in range(8 * expected):
        vector = random.normal(size=identity.shape[0])
        average = sum(
            np.outer(matrix @ vector, matrix @ vector)
            for matrix in representations.values()
        ) / len(representations)
        add(average)
        if len(basis) == expected:
            break
    if len(basis) != expected:
        raise ArithmeticError("failed to span the symmetric multiplicity commutant")
    orthogonality = float(
        np.linalg.norm(
            np.asarray(
                [
                    [float(np.sum(left * right)) for right in basis]
                    for left in basis
                ]
            )
            - np.eye(expected)
        )
    )
    commutator = max(
        float(np.linalg.norm(matrix @ generator - generator @ matrix))
        for matrix in basis
        for generator in pair_generators
    )
    return tuple(basis), orthogonality, commutator


def _apply_representation_sparse(
    permutation: Permutation,
    basis: np.ndarray,
    sparse_data: tuple[Any, ...],
) -> np.ndarray:
    output = basis.copy()
    for generator_index in reversed(_adjacent_word(permutation)):
        diagonal, partner, coefficient = sparse_data[generator_index]
        output = (
            diagonal[:, np.newaxis] * output
            + coefficient[:, np.newaxis] * output[partner, :]
        )
    return output


@lru_cache(maxsize=None)
def _signed_weight_transports(
    half_degree: int,
    negative_pair_count: int,
) -> tuple[Permutation, ...]:
    """Pair permutations carrying each sign character to the reference one."""

    reference_negative = tuple(
        range(half_degree - negative_pair_count, half_degree)
    )
    reference_positive = tuple(
        index for index in range(half_degree) if index not in reference_negative
    )
    output = []
    for source_negative in combinations(range(half_degree), negative_pair_count):
        source_set = set(source_negative)
        source_positive = tuple(
            index for index in range(half_degree) if index not in source_set
        )
        mapping = [0] * half_degree
        for source, target in zip(source_positive, reference_positive):
            mapping[source] = target
        for source, target in zip(source_negative, reference_negative):
            mapping[source] = target
        output.append(_pair_permutation(half_degree, tuple(mapping)))
    return tuple(output)


def _projected_hermitian_orbit_matrix(
    symmetric_partition: Partition,
    representative: Permutation,
    isotypic_basis: np.ndarray,
    commutant_basis: tuple[np.ndarray, ...],
    sparse_data: tuple[Any, ...],
    transport_permutations: tuple[Permutation, ...],
) -> tuple[np.ndarray, float]:
    inverse = inverse_permutation(representative)
    compressed = np.zeros((isotypic_basis.shape[1], isotypic_basis.shape[1]))
    source_bases = []
    for transport in transport_permutations:
        source_basis = _apply_representation_sparse(
            inverse_permutation(transport),
            isotypic_basis,
            sparse_data,
        )
        source_bases.append(source_basis)
        forward = _apply_representation_sparse(
            representative,
            source_basis,
            sparse_data,
        )
        backward = _apply_representation_sparse(
            inverse,
            source_basis,
            sparse_data,
        )
        compressed += (
            source_basis.T @ forward + source_basis.T @ backward
        ) / 2.0
    compressed /= len(transport_permutations)
    projected = sum(
        float(np.sum(basis * compressed)) * basis for basis in commutant_basis
    )
    dense_residual = 0.0
    if (
        moved_point_support(representative) <= 3
        and isotypic_basis.shape[0] <= 2000
    ):
        dense = _matrix_for_permutation(symmetric_partition, representative)
        dense_inverse = _matrix_for_permutation(symmetric_partition, inverse)
        direct = sum(
            source_basis.T
            @ ((dense + dense_inverse) / 2.0)
            @ source_basis
            for source_basis in source_bases
        ) / len(source_bases)
        dense_residual = float(np.linalg.norm(direct - compressed))
    return (projected + projected.T) / 2.0, dense_residual


@lru_cache(maxsize=1)
def validate_signed_weight_projection_against_full_twirl(
    *,
    tolerance: float = 1e-9,
) -> ExactSignedTwirlValidation:
    """Compare signed-sector compression with an explicit full K_4 twirl."""

    half_degree = 4
    symmetric_partition = (4, 2, 2)
    alpha = (2,)
    beta = (2,)
    negative_pair_count = sum(beta)
    isotypic, multiplicity, _, _ = _isotypic_basis(
        half_degree,
        symmetric_partition,
        alpha,
        beta,
        tolerance=tolerance,
    )
    _, _, _, sparse_data, _ = _signed_weight_workspace(
        half_degree,
        symmetric_partition,
        negative_pair_count,
    )
    generators, swaps, stabilizer_order = _restricted_pair_generators(
        half_degree,
        negative_pair_count,
        isotypic,
        sparse_data,
    )
    commutant_basis, _, _ = _symmetric_commutant_basis(
        half_degree,
        generators,
        swaps,
        stabilizer_order,
        multiplicity,
        tolerance=tolerance,
    )
    representative = _pair_transposition(half_degree, 0, 2)
    projected, _ = _projected_hermitian_orbit_matrix(
        symmetric_partition,
        representative,
        isotypic,
        commutant_basis,
        sparse_data,
        _signed_weight_transports(half_degree, negative_pair_count),
    )
    inverse = inverse_permutation(representative)
    operator = (
        _matrix_for_permutation(symmetric_partition, representative)
        + _matrix_for_permutation(symmetric_partition, inverse)
    ) / 2.0
    group = hyperoctahedral_group(half_degree)
    exact_twirl = np.zeros_like(operator)
    for element in group:
        representation = _matrix_for_permutation(
            symmetric_partition,
            element,
        )
        exact_twirl += representation @ operator @ representation.T
    exact_twirl /= len(group)
    exact_restriction = isotypic.T @ exact_twirl @ isotypic
    residual = float(np.linalg.norm(projected - exact_restriction))
    passed = residual <= tolerance
    return ExactSignedTwirlValidation(
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        hyperoctahedral_partition=alpha,
        negative_hyperoctahedral_partition=beta,
        hyperoctahedral_group_order=len(group),
        selected_character_isotypic_dimension=isotypic.shape[1],
        projected_restriction_residual=residual,
        validation_passed=passed,
        status=(
            "signed-sector-compression-matches-full-twirl"
            if passed
            else "signed-sector-compression-validation-failed"
        ),
    )


def _matrix_span_dimension(
    matrices: list[np.ndarray],
    *,
    tolerance: float,
) -> int:
    if not matrices:
        return 0
    singular = np.linalg.svd(
        np.stack([matrix.reshape(-1) for matrix in matrices]),
        compute_uv=False,
    )
    return int(np.count_nonzero(singular > tolerance))


def _generated_algebra_dimension(
    matrices: list[np.ndarray],
    *,
    dimension_upper_bound: int,
    tolerance: float,
) -> int:
    basis: list[np.ndarray] = []
    frontier: list[np.ndarray] = []

    def add(matrix: np.ndarray) -> None:
        residual = matrix.reshape(-1).copy()
        for _ in range(2):
            for vector in basis:
                residual -= float(np.dot(vector, residual)) * vector
        norm = float(np.linalg.norm(residual))
        if norm > tolerance:
            basis.append(residual / norm)
            frontier.append(matrix)

    add(np.eye(matrices[0].shape[0]))
    for matrix in matrices:
        add(matrix)
    while frontier and len(basis) < dimension_upper_bound:
        left = frontier.pop(0)
        for right in matrices:
            add(left @ right)
            if len(basis) >= dimension_upper_bound:
                break
    return len(basis)


@lru_cache(maxsize=None)
def audit_multiplicity_twirl_projection(
    half_degree: int,
    symmetric_partition: Partition,
    hyperoctahedral_partition: Partition,
    maximum_support: int,
    *,
    negative_hyperoctahedral_partition: Partition = (),
    tolerance: float = 1e-7,
) -> MultiplicityTwirlProjectionControl:
    negative_pair_count = sum(negative_hyperoctahedral_partition)
    isotypic, multiplicity, flip_residual, isotypic_residual = _isotypic_basis(
        half_degree,
        symmetric_partition,
        hyperoctahedral_partition,
        negative_hyperoctahedral_partition,
        tolerance=tolerance,
    )
    _, _, _, sparse_data, _ = _signed_weight_workspace(
        half_degree, symmetric_partition, negative_pair_count
    )
    pair_generators, generator_swaps, stabilizer_order = _restricted_pair_generators(
        half_degree,
        negative_pair_count,
        isotypic,
        sparse_data,
    )
    commutant_basis, orthogonality, commutator = _symmetric_commutant_basis(
        half_degree,
        pair_generators,
        generator_swaps,
        stabilizer_order,
        multiplicity,
        tolerance=tolerance,
    )
    representatives = hermitian_bounded_support_orbit_representatives(
        half_degree,
        maximum_support,
    )
    transports = _signed_weight_transports(
        half_degree,
        negative_pair_count,
    )
    projected: list[tuple[Permutation, np.ndarray]] = []
    sparse_residual = 0.0
    for representative in representatives:
        matrix, residual = _projected_hermitian_orbit_matrix(
            symmetric_partition,
            representative,
            isotypic,
            commutant_basis,
            sparse_data,
            transports,
        )
        projected.append((representative, matrix))
        sparse_residual = max(sparse_residual, residual)

    full_dimension = multiplicity**2
    steps = []
    previous_full = False
    minimum_full: int | None = None
    witness: Permutation | None = None
    for cutoff in range(2, maximum_support + 1):
        active = [
            matrix
            for representative, matrix in projected
            if moved_point_support(representative) <= cutoff
        ]
        span = _matrix_span_dimension(active, tolerance=tolerance)
        algebra = _generated_algebra_dimension(
            active,
            dimension_upper_bound=full_dimension,
            tolerance=tolerance,
        )
        full = algebra == full_dimension
        if full and minimum_full is None:
            minimum_full = cutoff
            if not previous_full:
                lower = [
                    matrix
                    for representative, matrix in projected
                    if moved_point_support(representative) < cutoff
                ]
                for representative, matrix in projected:
                    if moved_point_support(representative) != cutoff:
                        continue
                    if _generated_algebra_dimension(
                        [*lower, matrix],
                        dimension_upper_bound=full_dimension,
                        tolerance=tolerance,
                    ) == full_dimension:
                        witness = representative
                        break
        previous_full = full
        steps.append(
            SupportCutoffAlgebraStep(
                maximum_moved_point_support=cutoff,
                hermitian_orbit_representative_count=len(active),
                symmetric_commutant_span_dimension=span,
                generated_copy_algebra_dimension=algebra,
                exact_copy_algebra_dimension=full_dimension,
                generates_full_copy_algebra=full,
                status=(
                    "bounded-support-generates-full-copy-algebra"
                    if full
                    else "bounded-support-copy-algebra-proper"
                ),
            )
        )

    carrier_weight_dimension = (
        hook_length_dimension(hyperoctahedral_partition)
        * hook_length_dimension(negative_hyperoctahedral_partition)
    )
    expected_isotypic = multiplicity * carrier_weight_dimension
    verified = bool(
        isotypic.shape[1] == expected_isotypic
        and len(commutant_basis) == multiplicity * (multiplicity + 1) // 2
        and flip_residual <= 100 * tolerance
        and isotypic_residual <= 100 * tolerance
        and orthogonality <= 100 * tolerance
        and commutator <= 1000 * tolerance
        and sparse_residual <= 100 * tolerance
    )
    return MultiplicityTwirlProjectionControl(
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        hyperoctahedral_partition=hyperoctahedral_partition,
        negative_hyperoctahedral_partition=negative_hyperoctahedral_partition,
        selected_character_negative_pair_count=negative_pair_count,
        symmetric_irrep_dimension=hook_length_dimension(symmetric_partition),
        hyperoctahedral_irrep_dimension=(
            math.comb(half_degree, negative_pair_count)
            * carrier_weight_dimension
        ),
        exact_branching_multiplicity=multiplicity,
        pair_flip_fixed_space_dimension=(
            _signed_weight_workspace(
                half_degree,
                symmetric_partition,
                negative_pair_count,
            )[0].shape[1]
        ),
        expected_isotypic_dimension=expected_isotypic,
        observed_isotypic_dimension=isotypic.shape[1],
        symmetric_commutant_dimension=len(commutant_basis),
        full_copy_algebra_dimension=full_dimension,
        maximum_support_audited=maximum_support,
        total_hermitian_orbit_representative_count=len(representatives),
        support_steps=steps,
        minimum_full_copy_algebra_support=minimum_full,
        first_full_support_witness=witness,
        first_full_support_witness_cycles=(
            permutation_cycles(witness) if witness is not None else ()
        ),
        maximum_pair_flip_projector_residual=flip_residual,
        maximum_isotypic_projector_residual=isotypic_residual,
        maximum_symmetric_commutant_orthogonality_residual=orthogonality,
        maximum_symmetric_commutant_K_commutator_residual=commutator,
        maximum_sparse_representation_action_residual=sparse_residual,
        compressed_twirl_projection_verified=verified,
        finite_control_only=True,
        status=(
            "compressed-multiplicity-twirl-projection-verified"
            if verified
            else "multiplicity-twirl-projection-control-failure"
        ),
    )


def run_multiplicity_twirl_projection(
    *,
    include_rank_seven_portfolio: bool = True,
    include_extended_portfolio: bool | None = None,
) -> MultiplicityTwirlProjectionReport:
    if include_extended_portfolio is None:
        include_extended_portfolio = include_rank_seven_portfolio
    specs = [
        (5, (6, 3, 1), (3, 1, 1), (), 5),
        (6, (8, 4), (4, 2), (), 6),
        (7, (10, 4), (5, 2), (), 6),
    ]
    if include_rank_seven_portfolio:
        specs.extend(
            [
                (7, (10, 2, 2), (5, 2), (), 6),
                (7, (10, 3, 1), (5, 1, 1), (), 6),
                (7, (10, 3, 1), (4, 2, 1), (), 6),
            ]
        )
    if include_extended_portfolio:
        specs.extend(
            [
                (7, (9, 4, 1), (4, 2, 1), (), 6),
                (7, (10, 2, 2), (5,), (2,), 6),
                (7, (10, 2, 2), (4, 1), (2,), 6),
                (7, (10, 3, 1), (4, 1), (1, 1), 6),
            ]
        )
    controls = [
        audit_multiplicity_twirl_projection(
            half_degree,
            symmetric_partition,
            alpha,
            maximum_support,
            negative_hyperoctahedral_partition=beta,
        )
        for half_degree, symmetric_partition, alpha, beta, maximum_support in specs
    ]
    exact_signed_validation = validate_signed_weight_projection_against_full_twirl()
    verified = all(control.compressed_twirl_projection_verified for control in controls)
    rank_five = controls[0].minimum_full_copy_algebra_support == 5
    rank_six = controls[1].minimum_full_copy_algebra_support == 6
    rank_seven = [control for control in controls if control.half_degree == 7]
    rank_seven_six_full = bool(rank_seven) and all(
        control.minimum_full_copy_algebra_support is not None
        and control.minimum_full_copy_algebra_support <= 6
        for control in rank_seven
    )
    strict_tracking_falsified = rank_five and rank_six and rank_seven_six_full
    multiplicity_three = [
        control for control in controls if control.exact_branching_multiplicity >= 3
    ]
    multiplicity_three_verified = bool(multiplicity_three) and all(
        control.compressed_twirl_projection_verified
        and control.minimum_full_copy_algebra_support is not None
        and control.minimum_full_copy_algebra_support <= 6
        for control in multiplicity_three
    )
    nontrivial_beta = [
        control
        for control in controls
        if control.negative_hyperoctahedral_partition
    ]
    nontrivial_beta_verified = bool(nontrivial_beta) and all(
        control.compressed_twirl_projection_verified
        and control.minimum_full_copy_algebra_support is not None
        and control.minimum_full_copy_algebra_support <= 6
        for control in nontrivial_beta
    )
    extended_portfolio_verified = (
        multiplicity_three_verified and nontrivial_beta_verified
    )
    theorem = MultiplicityTwirlProjectionTheorem(
        commutant_projection=(
            "K-conjugation twirling is the Hilbert-Schmidt orthogonal projection "
            "onto End_K; on a multiplicity-b isotypic block this is M_b tensor I."
        ),
        flip_trivial_isotypic_extraction=(
            "Pair-flip projection followed by the pair-transposition Casimir "
            "isolates every audited (alpha,empty) repeated branch at its exact "
            "branching dimension."
        ),
        signed_weight_isotypic_extraction=(
            "Fixing one base-group sign character, resolving the positive and "
            "negative pair-permutation Casimirs, averaging transported character "
            "sectors, and projecting under its stabilizer exactly reproduces the "
            "restriction of the full K twirl."
        ),
        orbit_enumeration_reduction=(
            "One representative compression plus a small commutant projection "
            "replaces construction of every full K-conjugacy orbit matrix."
        ),
        reproduced_thresholds=(
            "The repeated m=5 and m=6 controls first generate M_2 at supports "
            "five and six, respectively."
        ),
        rank_seven_falsifier=(
            (
                "Support at most six generates the full copy algebra on every "
                "audited m=7 branch. The multiplicity-three block closes at support "
                "five and all three nontrivial-beta controls close at support four, "
                "so the 4,5,6 sequence cannot be extrapolated as a strict "
                "rank-tracking law."
            )
            if extended_portfolio_verified
            else (
                "Support at most six already generates M_2 on the audited m=7 "
                "continuation, so the 4,5,6 sequence cannot be extrapolated as a "
                "strict rank-tracking law."
            )
        ),
        scope=(
            (
                "The m=7 portfolio is finite even after adding multiplicity three "
                "and nontrivial beta. It neither proves a uniform support-six theorem "
                "nor compiles the compression as a coherent source-aware transform."
            )
            if extended_portfolio_verified
            else (
                "The finite portfolio neither proves a uniform support-six theorem "
                "nor compiles the compression as a coherent source-aware transform."
            )
        ),
        hilbert_schmidt_twirl_projection_proved=True,
        compressed_orbit_representative_method_verified=(
            verified and exact_signed_validation.validation_passed
        ),
        multiplicity_three_block_verified=multiplicity_three_verified,
        nontrivial_beta_blocks_verified=nontrivial_beta_verified,
        rank_five_six_thresholds_reproduced=rank_five and rank_six,
        strict_rank_tracking_support_growth_falsified=strict_tracking_falsified,
        universal_support_six_generation_proved=False,
        unbounded_support_requirement_proved=False,
        coherent_commutant_transform_compiled=False,
        hidden_involution_decoder_compiled=False,
        theorem_verified=(
            verified
            and exact_signed_validation.validation_passed
            and strict_tracking_falsified
        ),
        status=(
            "strict-support-growth-falsified-multiplicity-three-and-signed-"
            "sectors-close-uniformity-open"
            if extended_portfolio_verified
            else "strict-support-growth-extrapolation-falsified-support-six-uniformity-open"
        ),
    )
    metrics: dict[str, int | float] = {
        "hilbert_schmidt_commutant_projection_theorem_count": 1,
        "compressed_orbit_representative_method_theorem_count": int(verified),
        "exact_signed_sector_full_twirl_validation_count": int(
            exact_signed_validation.validation_passed
        ),
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not control.compressed_twirl_projection_verified for control in controls
        ),
        "rank_five_support_threshold": controls[0].minimum_full_copy_algebra_support or 0,
        "rank_six_support_threshold": controls[1].minimum_full_copy_algebra_support or 0,
        "rank_seven_control_count": len(rank_seven),
        "rank_seven_support_six_full_count": sum(
            control.minimum_full_copy_algebra_support is not None
            and control.minimum_full_copy_algebra_support <= 6
            for control in rank_seven
        ),
        "multiplicity_three_control_count": len(multiplicity_three),
        "multiplicity_three_support_six_full_count": sum(
            control.minimum_full_copy_algebra_support is not None
            and control.minimum_full_copy_algebra_support <= 6
            for control in multiplicity_three
        ),
        "nontrivial_beta_control_count": len(nontrivial_beta),
        "nontrivial_beta_support_six_full_count": sum(
            control.minimum_full_copy_algebra_support is not None
            and control.minimum_full_copy_algebra_support <= 6
            for control in nontrivial_beta
        ),
        "strict_rank_tracking_support_growth_falsifier_count": int(
            strict_tracking_falsified
        ),
        "maximum_full_representation_dimension_avoided": max(
            control.symmetric_irrep_dimension for control in controls
        ),
        "maximum_multiplicity_block_dimension_used": max(
            control.observed_isotypic_dimension for control in controls
        ),
        "universal_support_six_generation_theorem_count": 0,
        "unbounded_support_lower_bound_count": 0,
        "coherent_commutant_transform_count": 0,
        "hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return MultiplicityTwirlProjectionReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "one symmetric-group irrep lambda, one repeated hyperoctahedral "
                "bipartition (alpha,beta), and bounded-support K-conjugacy orbit "
                "representatives"
            ),
            "output": (
                "small copy-space matrices and the generated multiplicity algebra "
                "dimension at each support cutoff"
            ),
            "exact_identity": (
                "Reynolds twirling equals Hilbert-Schmidt projection onto the "
                "representation commutant"
            ),
            "non_claim": (
                "No uniform support cutoff, coherent basis transform, natural-mass "
                "coverage, source polar, decoder, or speedup"
            ),
        },
        theorem=theorem,
        exact_signed_twirl_validation=exact_signed_validation,
        controls=controls,
        proof_obligations=[
            {
                "obligation": "validate_compressed_twirl_against_exact_commutant",
                "resolved": verified,
                "resolution": (
                    "Exact branching dimensions, projector identities, K commutators, "
                    "and sparse-versus-dense representation actions all agree."
                ),
            },
            {
                "obligation": "validate_signed_sector_transport_against_full_twirl",
                "resolved": exact_signed_validation.validation_passed,
                "resolution": (
                    "The transported-character/stabilizer projection agrees with "
                    "an explicit 384-element K_4 twirl to numerical tolerance."
                ),
            },
            {
                "obligation": "test_strict_rank_tracking_support_growth",
                "resolved": strict_tracking_falsified,
                "resolution": (
                    "Every audited m=7 repeated branch closes by support six rather "
                    "than requiring support seven; multiplicity-three and signed "
                    "sectors close even earlier in the audited controls."
                ),
            },
            {
                "obligation": "prove_or_falsify_uniform_support_six_generation",
                "resolved": False,
                "resolution": (
                    "The scan covers selected low-dimensional and one larger "
                    "multiplicity-three branch, not all blocks or the natural source law."
                ),
            },
            {
                "obligation": "compile_coherent_commutant_projection_and_source_polar",
                "resolved": False,
                "resolution": (
                    "The diagnostic uses classical eigendecomposition and Reynolds "
                    "averages; no reversible implementation or normalization theorem exists."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A single representative cannot determine its orbit average.",
                "survives": False,
                "response": "Its orthogonal projection onto End_K is exactly the K-conjugation Reynolds average.",
            },
            {
                "challenge": "Numerical low reach may come from a noncyclic test vector.",
                "survives": False,
                "response": "The audit computes the generated matrix-algebra dimension directly inside the exact multiplicity block.",
            },
            {
                "challenge": "The 4,5,6 finite sequence proves support must grow with m.",
                "survives": False,
                "response": "The m=7 continuation and the broader low-dimensional portfolio already close at support six.",
            },
            {
                "challenge": "Finite support-six closure proves a uniform compiler.",
                "survives": True,
                "response": "Other branches, natural mass, spectral gaps, coherent basis access, and source-aware normalization remain open.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "hilbert_schmidt_commutant_projection_proved": True,
            "compressed_orbit_representative_method_verified": verified,
            "exact_signed_sector_full_twirl_validation_passed": (
                exact_signed_validation.validation_passed
            ),
            "multiplicity_three_block_verified": multiplicity_three_verified,
            "nontrivial_beta_blocks_verified": nontrivial_beta_verified,
            "rank_five_six_thresholds_reproduced": rank_five and rank_six,
            "strict_rank_tracking_support_growth_falsified": strict_tracking_falsified,
            "all_audited_rank_seven_blocks_close_by_support_six": rank_seven_six_full,
            "universal_support_six_generation_proved": False,
            "unbounded_support_requirement_proved": False,
            "coherent_commutant_transform_compiled": False,
            "source_aware_normalized_polar_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Compressed finite blocks falsify strict support growth and keep "
                "support six plausible, but uniform natural-block generation, gaps, "
                "coherent access, source normalization, and decoding are all open."
            ),
        },
        status=theorem.status,
        summary=(
            (
                "Extended commutant-projected orbit diagnostics to sparse signed "
                "sectors, validated them against an exact full K_4 twirl, and found "
                "support-five M_3 and support-four nontrivial-beta closure at rank seven."
            )
            if extended_portfolio_verified
            else (
                "Built a commutant-projected orbit diagnostic, reproduced the "
                "support-five/six boundaries, and falsified strict rank tracking."
            )
        ),
        falsifiers_triggered=[
            "The finite support threshold sequence 4,5,6 is not evidence of an unbounded-support theorem.",
            "Full orbit-average matrices are unnecessary for classical multiplicity-block generation audits.",
            "Support-six closure on selected S_14 blocks is not a uniform all-rank compiler theorem.",
            "A classical commutant projection is not a coherent source-aware quantum transform.",
        ],
    )


def write_multiplicity_twirl_projection_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_multiplicity_twirl_projection(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Hyperoctahedral multiplicity twirl projection",
                status="completed-strict-support-growth-falsified-uniformity-open",
                hypothesis=(
                    "Projecting orbit representatives directly into repeated "
                    "multiplicity blocks can test whether bounded-support commutant "
                    "generation truly requires growing support."
                ),
                protocol=(
                    "Extract exact signed-weight isotypic blocks, transport all "
                    "weight sectors, validate against a full K_4 twirl, project one "
                    "representative per Hermitian K orbit, and close the generated "
                    "copy algebra at each support cutoff."
                ),
                positive_signal=(
                    "Uniform support-six generation with inverse-polynomial gaps and "
                    "a coherent source-aware commutant transform on natural mass."
                ),
                falsifiers=[
                    "finite support thresholds are extrapolated as an all-rank law",
                    "noncyclic-vector reach is used as an algebra certificate",
                    "full orbit matrices are built despite exact commutant projection",
                    "selected finite bipartition branches are called the natural law",
                    "classical compression is called a coherent quantum transform",
                ],
                metrics=[
                    "hilbert_schmidt_commutant_projection_theorem_count",
                    "rank_five_support_threshold",
                    "rank_six_support_threshold",
                    "rank_seven_support_six_full_count",
                    "strict_rank_tracking_support_growth_falsifier_count",
                    "universal_support_six_generation_theorem_count",
                ],
                dependencies=[
                    "coset_hidden_involution_rank_tracking_commutant_witness.py",
                    "coset_hidden_involution_paired_tower_missing_label_boundary.py",
                    "hyperoctahedral branching coefficients",
                    "Reynolds projection onto representation commutants",
                ],
                next_actions=[
                    "scan all computationally feasible repeated S_14 bipartitions",
                    "measure natural source mass and spectral gaps of generated blocks",
                    "derive a symbolic support-six generation or counterexample invariant",
                    "test natural source mass of support-six generated blocks",
                    "compile coherent commutant projection only after uniformity and gaps survive",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-TWIRL-"
            "PROJECTION-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "coset_hidden_involution_multiplicity_twirl_projection": str(
                        path
                    )
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="RANK-TRACKING-4-5-6-NOT-UNBOUNDED-SUPPORT-EVIDENCE",
                source=registry_experiment_id,
                claim=(
                    "The finite support threshold sequence 4,5,6 demonstrates that "
                    "the required hyperoctahedral commutant support grows with rank."
                ),
                reason_invalid=(
                    "Eight rank-seven controls, including a multiplicity-three block "
                    "and three nontrivial-beta blocks, generate their copy algebra by "
                    "support six; several close strictly earlier."
                ),
                lesson=(
                    "Use compressed multiplicity-block scans or a symbolic invariant; "
                    "do not infer asymptotic growth from three finite thresholds."
                ),
                applies_to=[
                    registry_candidate_id,
                    "bounded-support hyperoctahedral commutants",
                    "rank-tracking support conjecture",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="CLASSICAL-COMMUTANT-TWIRL-PROJECTION-NOT-COHERENT-TRANSFORM",
                source=registry_experiment_id,
                claim=(
                    "Efficient classical projection of orbit representatives into "
                    "small multiplicity blocks supplies the missing quantum transform."
                ),
                reason_invalid=(
                    "The diagnostic uses classical isotypic eigendecomposition and "
                    "Reynolds averages, with no reversible source lift, normalization, "
                    "or coherent multiplicity basis circuit."
                ),
                lesson=(
                    "Treat compressed generation as a theorem-search tool and keep all "
                    "coherent access and decoder gates open."
                ),
                applies_to=[
                    registry_candidate_id,
                    "multiplicity commutant projection",
                    "coherent subduction transform",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_multiplicity_twirl_projection_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
