"""Exact low-degree syzygy invariants for binary linear codes.

For a full-rank generator matrix with ``k`` rows, its columns are points in
``F_2^k``.  Evaluation of homogeneous polynomials on those points defines the
quadratic relation space ``I_2``.  The dimensions

``beta_1_2 = dim(I_2)`` and
``beta_2_3 = dim ker(I_2 tensor S_1 -> S_3)``

are invariant under generator-basis changes and coordinate permutations.  A
mismatch therefore proves that two codes are not permutation equivalent.  A
match is only an invariant collision and is never evidence of hardness.

The implementation represents vectors as Python integers and performs exact
GF(2) elimination.  It does not sample relations or coordinates.
"""

from __future__ import annotations

import itertools
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

import numpy as np

from code_schur_filtration import row_basis


@dataclass(frozen=True)
class SyzygyInvariant:
    length: int
    dimension: int
    quadratic_monomial_count: int
    cubic_monomial_count: int
    square_code_dimension: int
    beta_1_2: int
    multiplication_domain_dimension: int
    multiplication_rank: int
    beta_2_3: int
    exact: bool = True

    @property
    def key(self) -> tuple[int, ...]:
        return (
            self.length,
            self.dimension,
            self.square_code_dimension,
            self.beta_1_2,
            self.beta_2_3,
        )

    def to_dict(self) -> dict[str, int | bool]:
        return asdict(self)


def homogeneous_monomials(variable_count: int, degree: int) -> tuple[tuple[int, ...], ...]:
    if variable_count < 0:
        raise ValueError("variable_count must be nonnegative")
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if degree == 0:
        return ((),)
    return tuple(itertools.combinations_with_replacement(range(variable_count), degree))


def gf2_bit_rank(vectors: Iterable[int]) -> int:
    """Return the exact rank of integer-encoded binary column vectors."""

    pivots: dict[int, int] = {}
    for raw in vectors:
        value = int(raw)
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def gf2_kernel_from_columns(columns: Sequence[int]) -> tuple[int, tuple[int, ...]]:
    """Return image rank and an exact kernel basis for a column map.

    Each input integer encodes one column of a GF(2)-linear map.  Kernel basis
    vectors are integers over the column-index coordinate space.
    """

    pivots: dict[int, tuple[int, int]] = {}
    kernel: list[int] = []
    for index, raw in enumerate(columns):
        value = int(raw)
        combination = 1 << index
        while value:
            pivot = value.bit_length() - 1
            previous = pivots.get(pivot)
            if previous is None:
                pivots[pivot] = (value, combination)
                break
            value ^= previous[0]
            combination ^= previous[1]
        if value == 0:
            kernel.append(combination)
    return len(pivots), tuple(kernel)


def _column_bits(generator: np.ndarray) -> tuple[int, ...]:
    matrix = row_basis(np.asarray(generator, dtype=np.uint8) & 1)
    columns: list[int] = []
    for coordinate in range(matrix.shape[1]):
        value = 0
        for variable, bit in enumerate(matrix[:, coordinate].tolist()):
            if bit:
                value |= 1 << variable
        columns.append(value)
    return tuple(columns)


def monomial_evaluation_vectors(
    generator: np.ndarray,
    monomials: Sequence[tuple[int, ...]],
) -> tuple[int, ...]:
    """Evaluate monomials on generator columns as coordinate bit vectors."""

    columns = _column_bits(generator)
    evaluations: list[int] = []
    for monomial in monomials:
        evaluation = 0
        for coordinate, point in enumerate(columns):
            if all((point >> variable) & 1 for variable in monomial):
                evaluation |= 1 << coordinate
        evaluations.append(evaluation)
    return tuple(evaluations)


def quadratic_relation_basis(generator: np.ndarray) -> tuple[tuple[tuple[int, int], ...], tuple[int, ...], int]:
    matrix = row_basis(np.asarray(generator, dtype=np.uint8) & 1)
    monomials = homogeneous_monomials(int(matrix.shape[0]), 2)
    evaluations = monomial_evaluation_vectors(matrix, monomials)
    square_rank, relations = gf2_kernel_from_columns(evaluations)
    return monomials, relations, square_rank


def _multiply_quadratic_relation(
    relation: int,
    variable: int,
    quadratic_monomials: Sequence[tuple[int, int]],
    cubic_index: dict[tuple[int, int, int], int],
) -> int:
    product = 0
    remaining = int(relation)
    while remaining:
        low_bit = remaining & -remaining
        monomial_index = low_bit.bit_length() - 1
        triple = tuple(sorted((*quadratic_monomials[monomial_index], int(variable))))
        product ^= 1 << cubic_index[triple]
        remaining ^= low_bit
    return product


def syzygy_invariant(generator: np.ndarray) -> SyzygyInvariant:
    """Compute exact quadratic and linear-syzygy Betti invariants."""

    matrix = row_basis(np.asarray(generator, dtype=np.uint8) & 1)
    if matrix.ndim != 2:
        raise ValueError("generator matrix must be two-dimensional")
    dimension, length = map(int, matrix.shape)
    quadratic_monomials, relations, square_rank = quadratic_relation_basis(matrix)
    cubic_monomials = homogeneous_monomials(dimension, 3)
    cubic_index = {monomial: index for index, monomial in enumerate(cubic_monomials)}
    products = (
        _multiply_quadratic_relation(relation, variable, quadratic_monomials, cubic_index)
        for relation in relations
        for variable in range(dimension)
    )
    multiplication_rank = gf2_bit_rank(products)
    domain_dimension = len(relations) * dimension
    return SyzygyInvariant(
        length=length,
        dimension=dimension,
        quadratic_monomial_count=len(quadratic_monomials),
        cubic_monomial_count=len(cubic_monomials),
        square_code_dimension=square_rank,
        beta_1_2=len(relations),
        multiplication_domain_dimension=domain_dimension,
        multiplication_rank=multiplication_rank,
        beta_2_3=domain_dimension - multiplication_rank,
    )


def validate_syzygy_certificate(invariant: SyzygyInvariant) -> list[str]:
    issues: list[str] = []
    if not invariant.exact:
        issues.append("syzygy certificate is not exact")
    if invariant.square_code_dimension + invariant.beta_1_2 != invariant.quadratic_monomial_count:
        issues.append("quadratic rank-nullity identity failed")
    if invariant.multiplication_rank + invariant.beta_2_3 != invariant.multiplication_domain_dimension:
        issues.append("syzygy rank-nullity identity failed")
    if invariant.multiplication_rank > invariant.cubic_monomial_count:
        issues.append("multiplication rank exceeds cubic ambient dimension")
    if min(invariant.beta_1_2, invariant.beta_2_3, invariant.multiplication_rank) < 0:
        issues.append("negative invariant dimension")
    return issues


__all__ = [
    "SyzygyInvariant",
    "gf2_bit_rank",
    "gf2_kernel_from_columns",
    "homogeneous_monomials",
    "monomial_evaluation_vectors",
    "quadratic_relation_basis",
    "syzygy_invariant",
    "validate_syzygy_certificate",
]
