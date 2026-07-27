"""Exact finite-field YJM multiplicity-block contraction.

Young's rational seminormal form avoids the square roots in the orthogonal
tableau representation.  Over a prime field, the diagonal content penalty

    L_T = sum_k (Y_k - c_k(T))^2

has kernel equal to one target-tableau Kronecker multiplicity fiber.  Its
nonzero eigenvalues are explicit positive integers, so

    P_T = product_{e in spec(L_T), e != 0} (L_T-e I)/(-e)

is an exact spectral projector modulo any prime larger than the maximum
penalty.  This module applies that projector without expanding pair group
algebra.  The ambient ``dim(lambda)^2`` space remains exponential for typical
partitions; this is an exact finite-block architecture, not a polynomial
quantum algorithm.
"""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from coset_jucys_murphy_label_transform import (
    standard_young_tableaux,
    tableau_content_vector,
    tableau_positions,
)
from representation_obstruction import integer_partitions
from symmetric_character import kronecker_coefficient


Partition = tuple[int, ...]
TensorBatch = np.ndarray


@dataclass(frozen=True)
class ModularSeminormalGenerator:
    diagonal: np.ndarray
    incoming_off_diagonal: np.ndarray
    outgoing_off_diagonal: np.ndarray
    partner: np.ndarray


@dataclass(frozen=True)
class ModularYJMBlockMetrics:
    n: int
    prime: int
    source_partition: Partition
    target_partition: Partition
    source_dimension: int
    tensor_dimension: int
    target_dimension: int
    multiplicity: int
    distinct_nonzero_penalty_count: int
    maximum_penalty_eigenvalue: int
    projector_polynomial_degree: int
    projected_trial_count: int
    projected_rank: int
    tableau_fiber_count: int
    exact_field_arithmetic: bool
    pair_group_states_materialized: bool


def modular_inverse(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        raise ZeroDivisionError("zero has no finite-field inverse")
    return pow(value, prime - 2, prime)


@lru_cache(maxsize=None)
def rational_seminormal_generators(
    partition: Partition,
    prime: int,
) -> tuple[ModularSeminormalGenerator, ...]:
    """Return Young rational-seminormal adjacent generators modulo ``prime``."""

    n = sum(partition)
    if prime <= n:
        raise ValueError("prime must exceed every axial-distance denominator")
    tableaux = standard_young_tableaux(partition)
    index = {tableau: position for position, tableau in enumerate(tableaux)}
    positions = [tableau_positions(tableau) for tableau in tableaux]
    generators: list[ModularSeminormalGenerator] = []
    for adjacent in range(1, n):
        diagonal = np.zeros(len(tableaux), dtype=np.int64)
        outgoing = np.zeros(len(tableaux), dtype=np.int64)
        partner = np.arange(len(tableaux), dtype=np.int64)
        for column, tableau in enumerate(tableaux):
            row_i, col_i = positions[column][adjacent - 1]
            row_j, col_j = positions[column][adjacent]
            distance = (col_j - row_j) - (col_i - row_i)
            inverse_distance = modular_inverse(distance, prime)
            diagonal[column] = inverse_distance
            if abs(distance) == 1:
                continue
            mutable = [list(row) for row in tableau]
            mutable[row_i][col_i], mutable[row_j][col_j] = (
                mutable[row_j][col_j],
                mutable[row_i][col_i],
            )
            swapped = tuple(tuple(row) for row in mutable)
            partner[column] = index[swapped]
            outgoing[column] = (1 + inverse_distance) % prime
        incoming = outgoing[partner]
        generators.append(
            ModularSeminormalGenerator(
                diagonal=diagonal,
                incoming_off_diagonal=incoming,
                outgoing_off_diagonal=outgoing,
                partner=partner,
            )
        )
    return tuple(generators)


def apply_generator_axis(
    tensors: TensorBatch,
    generator: ModularSeminormalGenerator,
    *,
    axis: int,
    prime: int,
) -> TensorBatch:
    if tensors.ndim != 3 or axis not in (1, 2):
        raise ValueError("expected a (batch,dim,dim) tensor and source axis 1 or 2")
    if tensors.shape[axis] != len(generator.diagonal):
        raise ValueError("generator dimension does not match tensor axis")
    if axis == 1:
        diagonal = generator.diagonal[None, :, None]
        incoming = generator.incoming_off_diagonal[None, :, None]
    else:
        diagonal = generator.diagonal[None, None, :]
        incoming = generator.incoming_off_diagonal[None, None, :]
    swapped = np.take(tensors, generator.partner, axis=axis)
    return (diagonal * tensors + incoming * swapped) % prime


def apply_diagonal_generator(
    tensors: TensorBatch,
    generator: ModularSeminormalGenerator,
    *,
    prime: int,
) -> TensorBatch:
    transformed = apply_generator_axis(
        tensors,
        generator,
        axis=1,
        prime=prime,
    )
    return apply_generator_axis(
        transformed,
        generator,
        axis=2,
        prime=prime,
    )


def transposition_word(left: int, right: int) -> tuple[int, ...]:
    if not 1 <= left < right:
        raise ValueError("expected one-indexed left < right")
    return tuple(
        [*range(left - 1, right - 1), *range(right - 3, left - 2, -1)]
    )


def apply_transposition_axis(
    tensors: TensorBatch,
    generators: tuple[ModularSeminormalGenerator, ...],
    left: int,
    right: int,
    *,
    axis: int,
    prime: int,
) -> TensorBatch:
    transformed = tensors
    for generator_index in reversed(transposition_word(left, right)):
        transformed = apply_generator_axis(
            transformed,
            generators[generator_index],
            axis=axis,
            prime=prime,
        )
    return transformed


def apply_pair_product(
    tensors: TensorBatch,
    generators: tuple[ModularSeminormalGenerator, ...],
    *,
    left_factors: tuple[tuple[int, int], ...],
    right_factors: tuple[tuple[int, int], ...],
    prime: int,
) -> TensorBatch:
    """Apply products of transpositions in mathematical left-to-right order."""

    transformed = tensors
    for left, right in reversed(left_factors):
        transformed = apply_transposition_axis(
            transformed,
            generators,
            left,
            right,
            axis=1,
            prime=prime,
        )
    for left, right in reversed(right_factors):
        transformed = apply_transposition_axis(
            transformed,
            generators,
            left,
            right,
            axis=2,
            prime=prime,
        )
    return transformed


def apply_representative_separator(
    tensors: TensorBatch,
    generators: tuple[ModularSeminormalGenerator, ...],
    *,
    prime: int,
) -> TensorBatch:
    """Apply the TT1+TC1 representatives used by the typical separator."""

    tt = apply_pair_product(
        tensors,
        generators,
        left_factors=((1, 2),),
        right_factors=((1, 3),),
        prime=prime,
    )
    tc = apply_pair_product(
        tensors,
        generators,
        left_factors=((1, 2),),
        right_factors=((1, 3), (3, 4)),
        prime=prime,
    )
    return (tt + tc) % prime


def apply_diagonal_yjm(
    tensors: TensorBatch,
    generators: tuple[ModularSeminormalGenerator, ...],
    label: int,
    *,
    prime: int,
) -> TensorBatch:
    if not 2 <= label <= len(generators) + 1:
        raise ValueError("YJM label is outside the represented symmetric group")
    adjacent = generators[label - 2]
    transformed = apply_diagonal_generator(
        tensors,
        adjacent,
        prime=prime,
    )
    if label == 2:
        return transformed
    inner = apply_diagonal_yjm(
        transformed,
        generators,
        label - 1,
        prime=prime,
    )
    return (
        apply_diagonal_generator(
            inner,
            adjacent,
            prime=prime,
        )
        + transformed
    ) % prime


def apply_content_penalty(
    tensors: TensorBatch,
    generators: tuple[ModularSeminormalGenerator, ...],
    content_vector: tuple[int, ...],
    *,
    prime: int,
) -> TensorBatch:
    result = np.zeros_like(tensors)
    for label in range(2, len(content_vector) + 1):
        content = content_vector[label - 1] % prime
        shifted = (
            apply_diagonal_yjm(
                tensors,
                generators,
                label,
                prime=prime,
            )
            - content * tensors
        ) % prime
        squared = (
            apply_diagonal_yjm(
                shifted,
                generators,
                label,
                prime=prime,
            )
            - content * shifted
        ) % prime
        result = (result + squared) % prime
    return result


@lru_cache(maxsize=None)
def content_penalty_spectrum(
    source_partition: Partition,
    target_partition: Partition,
    *,
    tableau_index: int = 0,
) -> tuple[int, ...]:
    if sum(source_partition) != sum(target_partition):
        raise ValueError("source and target must partition the same n")
    target_tableaux = standard_young_tableaux(target_partition)
    if not 0 <= tableau_index < len(target_tableaux):
        raise ValueError("target tableau index is out of range")
    target_content = tableau_content_vector(target_tableaux[tableau_index])
    values: set[int] = set()
    for partition in integer_partitions(sum(source_partition)):
        if not kronecker_coefficient(
            source_partition,
            source_partition,
            partition,
        ):
            continue
        for tableau in standard_young_tableaux(partition):
            content = tableau_content_vector(tableau)
            values.add(
                sum(
                    (observed - expected) ** 2
                    for observed, expected in zip(content, target_content)
                )
            )
    if 0 not in values:
        raise ArithmeticError("target tableau is absent from the tensor square")
    return tuple(sorted(values))


def apply_exact_content_projector(
    tensors: TensorBatch,
    source_partition: Partition,
    target_partition: Partition,
    *,
    prime: int,
    tableau_index: int = 0,
) -> TensorBatch:
    spectrum = content_penalty_spectrum(
        source_partition,
        target_partition,
        tableau_index=tableau_index,
    )
    if prime <= spectrum[-1]:
        raise ValueError("prime must exceed the maximum integer penalty")
    generators = rational_seminormal_generators(source_partition, prime)
    content = tableau_content_vector(
        standard_young_tableaux(target_partition)[tableau_index]
    )
    projected = tensors % prime
    for eigenvalue in spectrum:
        if eigenvalue == 0:
            continue
        projected = (
            apply_content_penalty(
                projected,
                generators,
                content,
                prime=prime,
            )
            - eigenvalue * projected
        ) % prime
        projected = (
            projected * modular_inverse(-eigenvalue, prime)
        ) % prime
    return projected


def independent_row_basis(
    vectors: TensorBatch,
    *,
    prime: int,
) -> tuple[TensorBatch, tuple[int, ...]]:
    flattened = vectors.reshape(vectors.shape[0], -1) % prime
    basis: list[np.ndarray] = []
    pivots: list[int] = []
    for candidate in flattened:
        reduced = candidate.copy()
        for pivot, row in zip(pivots, basis):
            if reduced[pivot]:
                reduced = (reduced - reduced[pivot] * row) % prime
        nonzero = np.flatnonzero(reduced)
        if not len(nonzero):
            continue
        pivot = int(nonzero[0])
        reduced = (
            reduced * modular_inverse(int(reduced[pivot]), prime)
        ) % prime
        basis.append(reduced)
        pivots.append(pivot)
    if not basis:
        return np.empty((0, *vectors.shape[1:]), dtype=np.int64), ()
    return (
        np.stack(basis).reshape((len(basis), *vectors.shape[1:])),
        tuple(pivots),
    )


def modular_projected_fiber(
    source_partition: Partition,
    target_partition: Partition,
    multiplicity: int,
    *,
    prime: int,
    seed: int = 0,
    oversampling: int = 3,
) -> tuple[TensorBatch, tuple[int, ...], int]:
    dimension = len(standard_young_tableaux(source_partition))
    rng = np.random.default_rng(seed)
    trials = multiplicity + oversampling
    random_vectors = rng.integers(
        0,
        prime,
        size=(trials, dimension, dimension),
        dtype=np.int64,
    )
    projected = apply_exact_content_projector(
        random_vectors,
        source_partition,
        target_partition,
        prime=prime,
    )
    basis, pivots = independent_row_basis(projected, prime=prime)
    if len(basis) != multiplicity:
        raise ArithmeticError(
            f"projected rank {len(basis)} differs from multiplicity {multiplicity}"
        )
    return basis, pivots, trials


def _project_random_trial(
    arguments: tuple[Partition, Partition, int, int],
) -> np.ndarray:
    source_partition, target_partition, prime, seed = arguments
    dimension = len(standard_young_tableaux(source_partition))
    rng = np.random.default_rng(seed)
    random_vector = rng.integers(
        0,
        prime,
        size=(1, dimension, dimension),
        dtype=np.int64,
    )
    return apply_exact_content_projector(
        random_vector,
        source_partition,
        target_partition,
        prime=prime,
    )[0]


def modular_projected_fiber_parallel(
    source_partition: Partition,
    target_partition: Partition,
    multiplicity: int,
    *,
    prime: int,
    seed: int = 0,
    workers: int | None = None,
    maximum_trials: int | None = None,
) -> tuple[TensorBatch, tuple[int, ...], int, tuple[int, ...]]:
    """Project independent vectors in worker processes until the fiber spans."""

    worker_count = workers or min(multiplicity, os.cpu_count() or 1)
    if worker_count < 1:
        raise ValueError("workers must be positive")
    trial_limit = maximum_trials or multiplicity + 3
    if trial_limit < multiplicity:
        raise ValueError("maximum_trials must be at least the multiplicity")
    projected: list[np.ndarray] = []
    used_seeds: list[int] = []
    next_trial = 0
    current_rank = 0
    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        while next_trial < trial_limit:
            batch_size = min(
                worker_count,
                trial_limit - next_trial,
                max(1, multiplicity - current_rank),
            )
            seeds = tuple(
                seed + next_trial + offset
                for offset in range(batch_size)
            )
            arguments = tuple(
                (source_partition, target_partition, prime, trial_seed)
                for trial_seed in seeds
            )
            projected.extend(executor.map(_project_random_trial, arguments))
            used_seeds.extend(seeds)
            next_trial += batch_size
            basis, pivots = independent_row_basis(
                np.stack(projected),
                prime=prime,
            )
            if len(basis) == multiplicity:
                return basis, pivots, len(projected), tuple(used_seeds)
            if len(basis) > multiplicity:
                raise ArithmeticError(
                    "modular projector rank exceeds the exact multiplicity"
                )
            current_rank = len(basis)
    raise ArithmeticError(
        f"projected rank {len(basis)} stayed below multiplicity {multiplicity}"
    )


def seminormal_gram_weights(
    partition: Partition,
    *,
    prime: int,
) -> np.ndarray:
    generators = rational_seminormal_generators(partition, prime)
    dimension = len(standard_young_tableaux(partition))
    weights = np.full(dimension, -1, dtype=np.int64)
    weights[0] = 1
    pending = [0]
    while pending:
        tableau = pending.pop()
        for generator in generators:
            neighbor = int(generator.partner[tableau])
            if neighbor == tableau:
                continue
            ratio = (
                int(generator.incoming_off_diagonal[tableau])
                * modular_inverse(
                    int(generator.outgoing_off_diagonal[tableau]),
                    prime,
                )
            ) % prime
            candidate = int(weights[tableau]) * ratio % prime
            if weights[neighbor] == -1:
                weights[neighbor] = candidate
                pending.append(neighbor)
            elif int(weights[neighbor]) != candidate:
                raise ArithmeticError("seminormal Gram propagation is inconsistent")
    if np.any(weights < 0):
        raise ArithmeticError("seminormal tableau graph is disconnected")
    return weights


def matrix_inverse_mod(matrix: np.ndarray, prime: int) -> np.ndarray:
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    n = matrix.shape[0]
    augmented = np.concatenate(
        (matrix.copy() % prime, np.eye(n, dtype=np.int64)),
        axis=1,
    )
    for column in range(n):
        candidates = np.flatnonzero(augmented[column:, column])
        if not len(candidates):
            raise ArithmeticError("matrix is singular modulo the selected prime")
        pivot = column + int(candidates[0])
        if pivot != column:
            augmented[[column, pivot]] = augmented[[pivot, column]]
        augmented[column] = (
            augmented[column]
            * modular_inverse(int(augmented[column, column]), prime)
        ) % prime
        for row in range(n):
            if row == column or not augmented[row, column]:
                continue
            augmented[row] = (
                augmented[row]
                - augmented[row, column] * augmented[column]
            ) % prime
    return augmented[:, n:]


def weighted_pairing(
    left: TensorBatch,
    right: TensorBatch,
    pair_weights: np.ndarray,
    *,
    prime: int,
) -> np.ndarray:
    left_flat = left.reshape(left.shape[0], -1)
    right_flat = right.reshape(right.shape[0], -1)
    weighted = (left_flat * pair_weights[None, :]) % prime
    return (weighted @ right_flat.T) % prime


def modular_separator_block_from_fiber(
    source_partition: Partition,
    target_partition: Partition,
    root_fiber: TensorBatch,
    *,
    prime: int,
    root_tableau_index: int = 0,
) -> tuple[np.ndarray, int]:
    source_generators = rational_seminormal_generators(
        source_partition,
        prime,
    )
    target_generators = rational_seminormal_generators(
        target_partition,
        prime,
    )
    target_dimension = len(standard_young_tableaux(target_partition))
    children: dict[int, list[tuple[int, int]]] = {
        index: [] for index in range(target_dimension)
    }
    seen = {root_tableau_index}
    pending = [root_tableau_index]
    while pending:
        tableau = pending.pop(0)
        for generator_index, generator in enumerate(target_generators):
            neighbor = int(generator.partner[tableau])
            if neighbor == tableau or neighbor in seen:
                continue
            seen.add(neighbor)
            pending.append(neighbor)
            children[tableau].append((neighbor, generator_index))
    if len(seen) != target_dimension:
        raise ArithmeticError("target tableau spanning tree is incomplete")

    source_weights = seminormal_gram_weights(
        source_partition,
        prime=prime,
    )
    target_weights = seminormal_gram_weights(
        target_partition,
        prime=prime,
    )
    inverse_root_target_weight = modular_inverse(
        int(target_weights[root_tableau_index]),
        prime,
    )
    pair_weights = (
        source_weights[:, None] * source_weights[None, :]
    ).reshape(-1) % prime
    gram = weighted_pairing(
        root_fiber,
        root_fiber,
        pair_weights,
        prime=prime,
    )
    gram_inverse = matrix_inverse_mod(gram, prime)
    contracted = np.zeros_like(gram)
    visited = 0

    def visit(tableau: int, fiber: TensorBatch) -> None:
        nonlocal contracted
        nonlocal visited
        visited += 1
        transformed = apply_representative_separator(
            fiber,
            source_generators,
            prime=prime,
        )
        target_gram_ratio = (
            int(target_weights[tableau]) * inverse_root_target_weight
        ) % prime
        contracted = (
            contracted
            + modular_inverse(target_gram_ratio, prime)
            * weighted_pairing(
                    fiber,
                    transformed,
                    pair_weights,
                    prime=prime,
                )
        ) % prime
        for neighbor, generator_index in children[tableau]:
            target_generator = target_generators[generator_index]
            outgoing = int(
                target_generator.outgoing_off_diagonal[tableau]
            )
            child = (
                apply_diagonal_generator(
                    fiber,
                    source_generators[generator_index],
                    prime=prime,
                )
                - int(target_generator.diagonal[tableau]) * fiber
            ) % prime
            child = (child * modular_inverse(outgoing, prime)) % prime
            visit(neighbor, child)

    visit(root_tableau_index, root_fiber)
    contracted = (
        contracted * modular_inverse(target_dimension, prime)
    ) % prime
    block = (gram_inverse @ contracted) % prime
    return block, visited


def matrix_power_traces_mod(
    matrix: np.ndarray,
    maximum_degree: int,
    *,
    prime: int,
) -> tuple[int, ...]:
    if maximum_degree < 0:
        raise ValueError("maximum degree must be nonnegative")
    power = np.eye(matrix.shape[0], dtype=np.int64)
    traces = []
    for _ in range(maximum_degree):
        power = (power @ matrix) % prime
        traces.append(int(np.trace(power) % prime))
    return tuple(traces)


def characteristic_polynomial_mod(
    matrix: np.ndarray,
    *,
    prime: int,
) -> tuple[int, ...]:
    """Return monic characteristic coefficients via Newton identities."""

    degree = matrix.shape[0]
    traces = matrix_power_traces_mod(matrix, degree, prime=prime)
    coefficients = [1]
    for order in range(1, degree + 1):
        total = 0
        for index in range(1, order + 1):
            total += coefficients[order - index] * traces[index - 1]
        coefficients.append(
            (-total * modular_inverse(order, prime)) % prime
        )
    return tuple(coefficients)


def _polynomial_strip(
    coefficients: tuple[int, ...],
    prime: int,
) -> tuple[int, ...]:
    reduced = tuple(value % prime for value in coefficients)
    first = 0
    while first < len(reduced) - 1 and reduced[first] == 0:
        first += 1
    return reduced[first:]


def polynomial_remainder_mod(
    dividend: tuple[int, ...],
    divisor: tuple[int, ...],
    *,
    prime: int,
) -> tuple[int, ...]:
    numerator = list(_polynomial_strip(dividend, prime))
    denominator = _polynomial_strip(divisor, prime)
    if denominator == (0,):
        raise ZeroDivisionError("polynomial division by zero")
    inverse_lead = modular_inverse(denominator[0], prime)
    while len(numerator) >= len(denominator) and any(numerator):
        factor = numerator[0] * inverse_lead % prime
        for index, value in enumerate(denominator):
            numerator[index] = (
                numerator[index] - factor * value
            ) % prime
        numerator = list(_polynomial_strip(tuple(numerator), prime))
    return tuple(numerator)


def polynomial_gcd_mod(
    left: tuple[int, ...],
    right: tuple[int, ...],
    *,
    prime: int,
) -> tuple[int, ...]:
    first = _polynomial_strip(left, prime)
    second = _polynomial_strip(right, prime)
    while second != (0,):
        first, second = second, polynomial_remainder_mod(
            first,
            second,
            prime=prime,
        )
    inverse_lead = modular_inverse(first[0], prime)
    return tuple(value * inverse_lead % prime for value in first)


def characteristic_polynomial_square_free_mod(
    coefficients: tuple[int, ...],
    *,
    prime: int,
) -> bool:
    degree = len(coefficients) - 1
    derivative = tuple(
        coefficient * (degree - index) % prime
        for index, coefficient in enumerate(coefficients[:-1])
    )
    return polynomial_gcd_mod(
        coefficients,
        derivative,
        prime=prime,
    ) == (1,)


def modular_yjm_separator_block(
    source_partition: Partition,
    target_partition: Partition,
    multiplicity: int,
    *,
    prime: int,
    seed: int = 0,
) -> tuple[np.ndarray, ModularYJMBlockMetrics]:
    expected = kronecker_coefficient(
        source_partition,
        source_partition,
        target_partition,
    )
    if expected != multiplicity:
        raise ValueError(
            f"declared multiplicity {multiplicity} differs from exact {expected}"
        )
    spectrum = content_penalty_spectrum(source_partition, target_partition)
    if prime <= spectrum[-1]:
        raise ValueError("prime must exceed maximum penalty eigenvalue")
    fiber, _, trials = modular_projected_fiber(
        source_partition,
        target_partition,
        multiplicity,
        prime=prime,
        seed=seed,
    )
    block, visited = modular_separator_block_from_fiber(
        source_partition,
        target_partition,
        fiber,
        prime=prime,
    )
    source_dimension = len(standard_young_tableaux(source_partition))
    target_dimension = len(standard_young_tableaux(target_partition))
    return block, ModularYJMBlockMetrics(
        n=sum(source_partition),
        prime=prime,
        source_partition=source_partition,
        target_partition=target_partition,
        source_dimension=source_dimension,
        tensor_dimension=source_dimension * source_dimension,
        target_dimension=target_dimension,
        multiplicity=multiplicity,
        distinct_nonzero_penalty_count=len(spectrum) - 1,
        maximum_penalty_eigenvalue=spectrum[-1],
        projector_polynomial_degree=len(spectrum) - 1,
        projected_trial_count=trials,
        projected_rank=len(fiber),
        tableau_fiber_count=visited,
        exact_field_arithmetic=True,
        pair_group_states_materialized=False,
    )
