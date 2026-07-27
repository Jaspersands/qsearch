"""Sparse YJM fiber isolation for symmetric-group Kronecker multiplicities.

The diagonal Jucys-Murphy operators on ``V_lambda tensor V_lambda`` commute.
Fixing the content vector of one standard tableau of shape ``nu`` isolates a
fiber of dimension ``g(lambda,lambda,nu)``.  Adjacent diagonal transpositions
then propagate that fiber through every tableau of shape ``nu`` without
another eigensolve.

This avoids the extra ``dim(nu)`` factor in a direct invariant-tensor
Coxeter solve.  It is still a finite representation-space computation, not a
polynomial-time multiplicity transform.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, eigsh

from coset_jucys_murphy_label_transform import (
    adjacent_transposition_matrices,
    standard_young_tableaux,
    tableau_content_vector,
    transposition_matrix,
)
from coset_stable_subspace_transition_probe import _apply_sparse_axis
from representation_obstruction import hook_length_dimension


Partition = tuple[int, ...]


@dataclass(frozen=True)
class YJMFiberMetrics:
    n: int
    source_partition: Partition
    target_partition: Partition
    source_dimension: int
    target_dimension: int
    multiplicity: int
    fiber_vector_dimension: int
    direct_invariant_vector_dimension: int
    vector_dimension_reduction_factor: int
    arpack_subspace_dimension: int
    estimated_arpack_basis_bytes: int
    penalty_eigenvalues: tuple[float, ...]
    penalty_gap: float
    maximum_penalty_residual: float
    tableau_fiber_count: int
    maximum_fiber_orthogonality_residual: float
    maximum_tableau_propagation_residual: float


@lru_cache(maxsize=None)
def _source_adjacent_generators(
    source_partition: Partition,
) -> tuple[csr_matrix, ...]:
    return tuple(
        csr_matrix(matrix)
        for matrix in adjacent_transposition_matrices(source_partition)
    )


@lru_cache(maxsize=None)
def _diagonal_yjm_terms(
    source_partition: Partition,
) -> tuple[tuple[csr_matrix, ...], ...]:
    n = sum(source_partition)
    return tuple(
        tuple(
            csr_matrix(transposition_matrix(source_partition, index, label))
            for index in range(1, label)
        )
        for label in range(2, n + 1)
    )


def _apply_diagonal_pair(
    tensor: np.ndarray,
    matrix: csr_matrix,
    *,
    first_axis: int,
) -> np.ndarray:
    transformed = _apply_sparse_axis(tensor, matrix, first_axis)
    return _apply_sparse_axis(transformed, matrix, first_axis + 1)


def _apply_yjm(
    tensor: np.ndarray,
    terms: tuple[csr_matrix, ...],
    *,
    first_axis: int,
) -> np.ndarray:
    result = np.zeros_like(tensor)
    for matrix in terms:
        result += _apply_diagonal_pair(
            tensor,
            matrix,
            first_axis=first_axis,
        )
    return result


def yjm_content_penalty_operator(
    source_partition: Partition,
    content_vector: tuple[int, ...],
) -> LinearOperator:
    """Return sum_k (Y_k-content_k I)^2 on the diagonal tensor square."""

    n = sum(source_partition)
    if len(content_vector) != n:
        raise ValueError("content vector length must equal the partition size")
    source_dimension = hook_length_dimension(source_partition)
    terms_by_label = _diagonal_yjm_terms(source_partition)
    size = source_dimension * source_dimension

    def matvec(vector: np.ndarray) -> np.ndarray:
        tensor = vector.reshape(source_dimension, source_dimension)
        result = np.zeros_like(tensor)
        for label, terms in enumerate(terms_by_label, start=2):
            content = content_vector[label - 1]
            shifted = _apply_yjm(
                tensor,
                terms,
                first_axis=0,
            ) - content * tensor
            result += _apply_yjm(
                shifted,
                terms,
                first_axis=0,
            ) - content * shifted
        return result.ravel()

    return LinearOperator((size, size), matvec=matvec, dtype=float)


def isolate_yjm_fiber(
    source_partition: Partition,
    target_partition: Partition,
    multiplicity: int,
    *,
    arpack_subspace_dimension: int | None = None,
    root_tableau_index: int = 0,
) -> tuple[np.ndarray, tuple[float, ...], float, int]:
    """Isolate one target-tableau multiplicity fiber in the tensor square."""

    if sum(source_partition) != sum(target_partition):
        raise ValueError("source and target must partition the same n")
    if multiplicity < 1:
        raise ValueError("multiplicity must be positive")
    tableaux = standard_young_tableaux(target_partition)
    if not 0 <= root_tableau_index < len(tableaux):
        raise ValueError("root tableau index is out of range")
    content = tableau_content_vector(tableaux[root_tableau_index])
    operator = yjm_content_penalty_operator(source_partition, content)
    eigenvector_count = multiplicity + 2
    ncv = arpack_subspace_dimension or max(
        eigenvector_count + 2,
        2 * multiplicity + 4,
    )
    if not eigenvector_count < ncv < operator.shape[0]:
        raise ValueError("ARPACK subspace must exceed k and remain below dimension")
    initial = np.linspace(1.0, 2.0, operator.shape[0], dtype=float)
    initial /= np.linalg.norm(initial)
    eigenvalues, eigenvectors = eigsh(
        operator,
        k=eigenvector_count,
        which="SA",
        tol=5e-10,
        maxiter=5_000,
        ncv=ncv,
        v0=initial,
    )
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    if float(np.max(np.abs(eigenvalues[:multiplicity]))) > 1e-7:
        raise ArithmeticError("YJM penalty missed the expected multiplicity fiber")
    if float(eigenvalues[multiplicity]) <= 1e-7:
        raise ArithmeticError("YJM fiber nullity exceeds the Kronecker multiplicity")
    source_dimension = hook_length_dimension(source_partition)
    fiber = eigenvectors[:, :multiplicity].T.reshape(
        multiplicity,
        source_dimension,
        source_dimension,
    )
    residual = max(
        float(np.linalg.norm(operator @ vector.ravel()))
        for vector in fiber
    )
    return fiber, tuple(float(value) for value in eigenvalues), residual, ncv


def propagate_tableau_fibers(
    source_partition: Partition,
    target_partition: Partition,
    root_fiber: np.ndarray,
    *,
    root_tableau_index: int = 0,
) -> tuple[tuple[np.ndarray, ...], float, float]:
    """Generate every target-tableau fiber from one YJM fiber."""

    tableaux = standard_young_tableaux(target_partition)
    target_generators = adjacent_transposition_matrices(target_partition)
    source_generators = _source_adjacent_generators(source_partition)
    if len(target_generators) != len(source_generators):
        raise ValueError("source and target degrees differ")
    fibers: dict[int, np.ndarray] = {root_tableau_index: root_fiber}
    pending = [root_tableau_index]
    propagation_residual = 0.0
    while pending:
        tableau_index = pending.pop()
        fiber = fibers[tableau_index]
        for generator_index, target_generator in enumerate(target_generators):
            column = target_generator[:, tableau_index]
            neighbors = np.flatnonzero(
                np.abs(column) > 1e-12
            )
            neighbors = neighbors[neighbors != tableau_index]
            if len(neighbors) == 0:
                continue
            if len(neighbors) != 1:
                raise ArithmeticError("seminormal generator has multiple neighbors")
            neighbor = int(neighbors[0])
            beta = float(column[neighbor])
            alpha = float(column[tableau_index])
            transformed = _apply_diagonal_pair(
                fiber,
                source_generators[generator_index],
                first_axis=1,
            )
            candidate = (transformed - alpha * fiber) / beta
            if neighbor in fibers:
                propagation_residual = max(
                    propagation_residual,
                    float(np.linalg.norm(candidate - fibers[neighbor])),
                )
            else:
                fibers[neighbor] = candidate
                pending.append(neighbor)
    if len(fibers) != len(tableaux):
        raise ArithmeticError("tableau graph propagation was incomplete")
    ordered = tuple(fibers[index] for index in range(len(tableaux)))
    multiplicity = root_fiber.shape[0]
    identity = np.eye(multiplicity)
    orthogonality_residual = max(
        float(
            np.linalg.norm(
                np.einsum("mij,nij->mn", fiber, fiber, optimize=True)
                - identity
            )
        )
        for fiber in ordered
    )
    return ordered, orthogonality_residual, propagation_residual


def representative_separator_block_from_fibers(
    source_partition: Partition,
    fibers: tuple[np.ndarray, ...],
) -> tuple[np.ndarray, float]:
    """Contract TT1+TC1 by tracing one representative over target tableaux."""

    if not fibers:
        raise ValueError("at least one tableau fiber is required")
    tt_left = csr_matrix(transposition_matrix(source_partition, 1, 2))
    tt_right = csr_matrix(transposition_matrix(source_partition, 1, 3))
    tc_right = csr_matrix(
        transposition_matrix(source_partition, 1, 3)
        @ transposition_matrix(source_partition, 3, 4)
    )

    def apply_pair(
        fiber: np.ndarray,
        left: csr_matrix,
        right: csr_matrix,
    ) -> np.ndarray:
        transformed = _apply_sparse_axis(fiber, left, 1)
        return _apply_sparse_axis(transformed, right, 2)

    multiplicity = fibers[0].shape[0]
    block = np.zeros((multiplicity, multiplicity))
    for fiber in fibers:
        transformed = (
            apply_pair(fiber, tt_left, tt_right)
            + apply_pair(fiber, tt_left, tc_right)
        )
        block += np.einsum(
            "mij,nij->mn",
            fiber,
            transformed,
            optimize=True,
        )
    block /= len(fibers)
    symmetry_residual = float(np.linalg.norm(block - block.T))
    return (block + block.T) / 2, symmetry_residual


def stream_representative_separator_block(
    source_partition: Partition,
    target_partition: Partition,
    root_fiber: np.ndarray,
    *,
    root_tableau_index: int = 0,
) -> tuple[np.ndarray, float, float, float, int]:
    """Contract all tableau fibers along a spanning tree without storing them."""

    tableaux = standard_young_tableaux(target_partition)
    target_generators = adjacent_transposition_matrices(target_partition)
    source_generators = _source_adjacent_generators(source_partition)
    children: dict[int, list[tuple[int, int, float, float, float]]] = {
        index: [] for index in range(len(tableaux))
    }
    seen = {root_tableau_index}
    pending = [root_tableau_index]
    while pending:
        tableau_index = pending.pop(0)
        for generator_index, target_generator in enumerate(target_generators):
            column = target_generator[:, tableau_index]
            neighbors = np.flatnonzero(np.abs(column) > 1e-12)
            neighbors = neighbors[neighbors != tableau_index]
            if len(neighbors) == 0:
                continue
            if len(neighbors) != 1:
                raise ArithmeticError("seminormal generator has multiple neighbors")
            neighbor = int(neighbors[0])
            if neighbor in seen:
                continue
            seen.add(neighbor)
            pending.append(neighbor)
            children[tableau_index].append(
                (
                    neighbor,
                    generator_index,
                    float(column[tableau_index]),
                    float(column[neighbor]),
                    float(target_generator[neighbor, neighbor]),
                )
            )
    if len(seen) != len(tableaux):
        raise ArithmeticError("tableau graph spanning tree is incomplete")

    tt_left = csr_matrix(transposition_matrix(source_partition, 1, 2))
    tt_right = csr_matrix(transposition_matrix(source_partition, 1, 3))
    tc_right = csr_matrix(
        transposition_matrix(source_partition, 1, 3)
        @ transposition_matrix(source_partition, 3, 4)
    )

    def apply_pair(
        fiber: np.ndarray,
        left: csr_matrix,
        right: csr_matrix,
    ) -> np.ndarray:
        transformed = _apply_sparse_axis(fiber, left, 1)
        return _apply_sparse_axis(transformed, right, 2)

    multiplicity = root_fiber.shape[0]
    identity = np.eye(multiplicity)
    block = np.zeros((multiplicity, multiplicity))
    orthogonality_residual = 0.0
    propagation_residual = 0.0
    visited_count = 0

    def visit(tableau_index: int, fiber: np.ndarray) -> None:
        nonlocal block
        nonlocal orthogonality_residual
        nonlocal propagation_residual
        nonlocal visited_count
        visited_count += 1
        orthogonality_residual = max(
            orthogonality_residual,
            float(
                np.linalg.norm(
                    np.einsum("mij,nij->mn", fiber, fiber, optimize=True)
                    - identity
                )
            ),
        )
        transformed = (
            apply_pair(fiber, tt_left, tt_right)
            + apply_pair(fiber, tt_left, tc_right)
        )
        block += np.einsum(
            "mij,nij->mn",
            fiber,
            transformed,
            optimize=True,
        )
        for (
            child,
            generator_index,
            parent_alpha,
            beta,
            child_alpha,
        ) in children[tableau_index]:
            diagonal_action = _apply_diagonal_pair(
                fiber,
                source_generators[generator_index],
                first_axis=1,
            )
            child_fiber = (diagonal_action - parent_alpha * fiber) / beta
            reverse_action = _apply_diagonal_pair(
                child_fiber,
                source_generators[generator_index],
                first_axis=1,
            )
            recovered_parent = (
                reverse_action - child_alpha * child_fiber
            ) / beta
            propagation_residual = max(
                propagation_residual,
                float(np.linalg.norm(recovered_parent - fiber)),
            )
            visit(child, child_fiber)

    visit(root_tableau_index, root_fiber)
    block /= len(tableaux)
    symmetry_residual = float(np.linalg.norm(block - block.T))
    return (
        (block + block.T) / 2,
        symmetry_residual,
        orthogonality_residual,
        propagation_residual,
        visited_count,
    )


def yjm_separator_block(
    source_partition: Partition,
    target_partition: Partition,
    multiplicity: int,
    *,
    arpack_subspace_dimension: int | None = None,
) -> tuple[np.ndarray, YJMFiberMetrics]:
    """Compute the multiplicity block using one YJM eigensolve."""

    root, penalty, penalty_residual, ncv = isolate_yjm_fiber(
        source_partition,
        target_partition,
        multiplicity,
        arpack_subspace_dimension=arpack_subspace_dimension,
    )
    (
        block,
        symmetry,
        orthogonality,
        propagation,
        tableau_fiber_count,
    ) = stream_representative_separator_block(
        source_partition,
        target_partition,
        root,
    )
    if symmetry > 1e-7:
        raise ArithmeticError("YJM-contracted separator block is not symmetric")
    source_dimension = hook_length_dimension(source_partition)
    target_dimension = hook_length_dimension(target_partition)
    vector_dimension = source_dimension * source_dimension
    metrics = YJMFiberMetrics(
        n=sum(source_partition),
        source_partition=source_partition,
        target_partition=target_partition,
        source_dimension=source_dimension,
        target_dimension=target_dimension,
        multiplicity=multiplicity,
        fiber_vector_dimension=vector_dimension,
        direct_invariant_vector_dimension=target_dimension * vector_dimension,
        vector_dimension_reduction_factor=target_dimension,
        arpack_subspace_dimension=ncv,
        estimated_arpack_basis_bytes=ncv * vector_dimension * 8,
        penalty_eigenvalues=penalty,
        penalty_gap=penalty[multiplicity],
        maximum_penalty_residual=penalty_residual,
        tableau_fiber_count=tableau_fiber_count,
        maximum_fiber_orthogonality_residual=orthogonality,
        maximum_tableau_propagation_residual=propagation,
    )
    return block, metrics
