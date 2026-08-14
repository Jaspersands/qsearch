"""Sparse pairwise YJM fibers for arbitrary symmetric-group irreps.

For irreps ``V_left``, ``V_right`` and ``V_target`` of ``S_n``, the diagonal
Jucys--Murphy family on ``V_left tensor V_right`` has one joint eigenspace for
each standard tableau of shape ``target``.  Every such eigenspace has dimension
``g(left,right,target)``.  Isolating one tableau therefore recovers a complete
Kronecker multiplicity fiber without constructing an invariant tensor of size
``d_left d_right d_target``.

The remaining tableau fibers are propagated by sparse adjacent transpositions.
Stacking them gives gauge-dependent, but exactly equivariant, isometries

    E_i : V_target -> V_left tensor V_right.

Gauge-invariant contractions of these isometries can be used to measure Racah
block masses.  The construction saves a factor ``d_target`` in the eigensolve;
it is still exponential in ``n`` for Plancherel-shaped irreps and is not a
uniform efficient Clebsch--Gordan transform.
"""

from __future__ import annotations

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
from symmetric_character import kronecker_coefficient


Partition = tuple[int, ...]


@dataclass(frozen=True)
class PairYJMFiberMetrics:
    n: int
    left_partition: Partition
    right_partition: Partition
    target_partition: Partition
    left_dimension: int
    right_dimension: int
    target_dimension: int
    multiplicity: int
    eigensolve_vector_dimension: int
    direct_invariant_vector_dimension: int
    eliminated_target_dimension_factor: int
    arpack_subspace_dimension: int
    penalty_gap: float
    maximum_penalty_residual: float
    maximum_fiber_orthogonality_residual: float
    maximum_tableau_propagation_residual: float
    embedding_isometry_residual: float
    finite_representation_space_only: bool
    status: str


@lru_cache(maxsize=None)
def _adjacent_sparse(partition: Partition) -> tuple[csr_matrix, ...]:
    return tuple(
        csr_matrix(matrix)
        for matrix in adjacent_transposition_matrices(partition)
    )


@lru_cache(maxsize=None)
def _pair_yjm_terms(
    left_partition: Partition,
    right_partition: Partition,
) -> tuple[tuple[tuple[csr_matrix, csr_matrix], ...], ...]:
    n = sum(left_partition)
    if sum(right_partition) != n:
        raise ValueError("left and right partitions must have the same size")
    return tuple(
        tuple(
            (
                csr_matrix(transposition_matrix(left_partition, index, label)),
                csr_matrix(transposition_matrix(right_partition, index, label)),
            )
            for index in range(1, label)
        )
        for label in range(2, n + 1)
    )


def _apply_pair(
    tensor: np.ndarray,
    left: csr_matrix,
    right: csr_matrix,
) -> np.ndarray:
    return _apply_sparse_axis(
        _apply_sparse_axis(tensor, left, 0),
        right,
        1,
    )


def _apply_yjm(
    tensor: np.ndarray,
    terms: tuple[tuple[csr_matrix, csr_matrix], ...],
) -> np.ndarray:
    result = np.zeros_like(tensor)
    for left, right in terms:
        result += _apply_pair(tensor, left, right)
    return result


def pair_yjm_content_penalty_operator(
    left_partition: Partition,
    right_partition: Partition,
    content_vector: tuple[int, ...],
) -> LinearOperator:
    """Return ``sum_k (Y_k-c_k I)^2`` on a diagonal tensor product."""

    n = sum(left_partition)
    if sum(right_partition) != n or len(content_vector) != n:
        raise ValueError("partitions and content vector must have common size n")
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    terms_by_label = _pair_yjm_terms(left_partition, right_partition)
    size = left_dimension * right_dimension

    def matvec(vector: np.ndarray) -> np.ndarray:
        tensor = vector.reshape(left_dimension, right_dimension)
        result = np.zeros_like(tensor)
        for label, terms in enumerate(terms_by_label, start=2):
            shifted = _apply_yjm(tensor, terms) - content_vector[label - 1] * tensor
            result += _apply_yjm(shifted, terms) - content_vector[label - 1] * shifted
        return result.ravel()

    return LinearOperator((size, size), matvec=matvec, dtype=float)


def isolate_pair_yjm_fiber(
    left_partition: Partition,
    right_partition: Partition,
    target_partition: Partition,
    multiplicity: int | None = None,
    *,
    root_tableau_index: int = 0,
    arpack_subspace_dimension: int | None = None,
) -> tuple[np.ndarray, tuple[float, ...], float, int]:
    """Isolate one target-tableau multiplicity fiber in ``left tensor right``."""

    n = sum(left_partition)
    if sum(right_partition) != n or sum(target_partition) != n:
        raise ValueError("all partitions must have common size n")
    expected = kronecker_coefficient(
        left_partition,
        right_partition,
        target_partition,
    )
    multiplicity = expected if multiplicity is None else multiplicity
    if multiplicity != expected or multiplicity < 1:
        raise ValueError("multiplicity must equal the positive Kronecker coefficient")
    tableaux = standard_young_tableaux(target_partition)
    if not 0 <= root_tableau_index < len(tableaux):
        raise ValueError("root tableau index is out of range")
    content = tableau_content_vector(tableaux[root_tableau_index])
    operator = pair_yjm_content_penalty_operator(
        left_partition,
        right_partition,
        content,
    )
    eigenvector_count = multiplicity + 2
    if operator.shape[0] <= 64:
        identity = np.eye(operator.shape[0])
        dense = np.column_stack(
            [operator @ identity[:, index] for index in range(operator.shape[0])]
        )
        eigenvalues, eigenvectors = np.linalg.eigh((dense + dense.T) / 2)
        ncv = operator.shape[0]
    else:
        ncv = arpack_subspace_dimension or max(
            eigenvector_count + 2,
            2 * multiplicity + 4,
            12,
        )
        ncv = min(ncv, operator.shape[0] - 1)
        if not eigenvector_count < ncv < operator.shape[0]:
            raise ValueError(
                "pair YJM fiber is too small for the guarded sparse eigensolve"
            )
        initial = np.linspace(1.0, 2.0, operator.shape[0], dtype=float)
        initial /= np.linalg.norm(initial)
        eigenvalues, eigenvectors = eigsh(
            operator,
            k=eigenvector_count,
            which="SA",
            tol=5e-10,
            maxiter=10_000,
            ncv=ncv,
            v0=initial,
        )
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    if float(np.max(np.abs(eigenvalues[:multiplicity]))) > 1e-7:
        raise ArithmeticError("pair YJM penalty missed the expected null fiber")
    if (
        len(eigenvalues) > multiplicity
        and float(eigenvalues[multiplicity]) <= 1e-7
    ):
        raise ArithmeticError("pair YJM nullity exceeds the Kronecker multiplicity")
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    fiber = eigenvectors[:, :multiplicity].T.reshape(
        multiplicity,
        left_dimension,
        right_dimension,
    )
    residual = max(
        float(np.linalg.norm(operator @ vector.ravel()))
        for vector in fiber
    )
    return fiber, tuple(float(value) for value in eigenvalues), residual, ncv


def propagate_pair_tableau_fibers(
    left_partition: Partition,
    right_partition: Partition,
    target_partition: Partition,
    root_fiber: np.ndarray,
    *,
    root_tableau_index: int = 0,
) -> tuple[tuple[np.ndarray, ...], float, float]:
    """Propagate one multiplicity fiber through the target tableau graph."""

    tableaux = standard_young_tableaux(target_partition)
    target_generators = adjacent_transposition_matrices(target_partition)
    left_generators = _adjacent_sparse(left_partition)
    right_generators = _adjacent_sparse(right_partition)
    if not len(target_generators) == len(left_generators) == len(right_generators):
        raise ValueError("all partitions must have common size n")
    fibers: dict[int, np.ndarray] = {root_tableau_index: root_fiber}
    pending = [root_tableau_index]
    propagation_residual = 0.0
    while pending:
        tableau_index = pending.pop()
        fiber = fibers[tableau_index]
        for generator_index, target_generator in enumerate(target_generators):
            column = target_generator[:, tableau_index]
            neighbors = np.flatnonzero(np.abs(column) > 1e-12)
            neighbors = neighbors[neighbors != tableau_index]
            if len(neighbors) == 0:
                continue
            if len(neighbors) != 1:
                raise ArithmeticError("seminormal generator has multiple tableau neighbors")
            neighbor = int(neighbors[0])
            beta = float(column[neighbor])
            alpha = float(column[tableau_index])
            transformed = np.empty_like(fiber)
            for multiplicity_index, vector in enumerate(fiber):
                transformed[multiplicity_index] = _apply_pair(
                    vector,
                    left_generators[generator_index],
                    right_generators[generator_index],
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
        raise ArithmeticError("target tableau graph propagation was incomplete")
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


@lru_cache(maxsize=32)
def pair_intertwiner_embeddings(
    left_partition: Partition,
    right_partition: Partition,
    target_partition: Partition,
) -> tuple[np.ndarray, PairYJMFiberMetrics]:
    """Return isometries with shape ``(g,d_left,d_right,d_target)``."""

    multiplicity = kronecker_coefficient(
        left_partition,
        right_partition,
        target_partition,
    )
    root, eigenvalues, penalty_residual, ncv = isolate_pair_yjm_fiber(
        left_partition,
        right_partition,
        target_partition,
        multiplicity,
    )
    fibers, orthogonality, propagation = propagate_pair_tableau_fibers(
        left_partition,
        right_partition,
        target_partition,
        root,
    )
    embeddings = np.stack(fibers, axis=-1)
    target_dimension = embeddings.shape[-1]
    gram = np.einsum(
        "iabt,jabu->ijtu",
        embeddings,
        embeddings,
        optimize=True,
    )
    expected = np.einsum(
        "ij,tu->ijtu",
        np.eye(multiplicity),
        np.eye(target_dimension),
    )
    isometry_residual = float(np.linalg.norm(gram - expected))
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    exact = max(penalty_residual, orthogonality, propagation, isometry_residual) < 1e-6
    metrics = PairYJMFiberMetrics(
        n=sum(left_partition),
        left_partition=left_partition,
        right_partition=right_partition,
        target_partition=target_partition,
        left_dimension=left_dimension,
        right_dimension=right_dimension,
        target_dimension=target_dimension,
        multiplicity=multiplicity,
        eigensolve_vector_dimension=left_dimension * right_dimension,
        direct_invariant_vector_dimension=(
            left_dimension * right_dimension * target_dimension
        ),
        eliminated_target_dimension_factor=target_dimension,
        arpack_subspace_dimension=ncv,
        penalty_gap=(
            float(eigenvalues[multiplicity])
            if len(eigenvalues) > multiplicity
            else math.inf
        ),
        maximum_penalty_residual=penalty_residual,
        maximum_fiber_orthogonality_residual=orthogonality,
        maximum_tableau_propagation_residual=propagation,
        embedding_isometry_residual=isometry_residual,
        finite_representation_space_only=True,
        status=(
            "pairwise-yjm-fiber-compiled"
            if exact
            else "pairwise-yjm-fiber-control-failure"
        ),
    )
    return embeddings, metrics
