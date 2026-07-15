"""Exact symmetric-group characters and Kronecker coefficients.

Characters are computed by Murnaghan-Nakayama.  A removable rim hook is
enumerated as a skew partition that is edge-connected and contains no 2x2
block.  The resulting character table supports exact class-algebra and
multi-copy recoupling calculations without constructing factorial-size group
matrices.
"""

from __future__ import annotations

import math
from functools import lru_cache

from representation_obstruction import integer_partitions


def normalize_partition(partition: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(value for value in partition if value > 0)


def conjugacy_class_size(cycle_type: tuple[int, ...]) -> int:
    n = sum(cycle_type)
    multiplicities: dict[int, int] = {}
    for part in cycle_type:
        multiplicities[part] = multiplicities.get(part, 0) + 1
    denominator = 1
    for length, count in multiplicities.items():
        denominator *= (length**count) * math.factorial(count)
    return math.factorial(n) // denominator


def _contained_partitions(
    partition: tuple[int, ...],
    target_size: int,
) -> tuple[tuple[int, ...], ...]:
    rows: list[tuple[int, ...]] = []

    def visit(index: int, previous: int, remaining: int, prefix: list[int]) -> None:
        if index == len(partition):
            if remaining == 0:
                rows.append(normalize_partition(tuple(prefix)))
            return
        maximum = min(previous, partition[index], remaining)
        for value in range(maximum, -1, -1):
            visit(index + 1, value, remaining - value, [*prefix, value])

    visit(0, partition[0] if partition else 0, target_size, [])
    return tuple(rows)


def _border_strip_height(
    partition: tuple[int, ...],
    subpartition: tuple[int, ...],
) -> int | None:
    padded = (*subpartition, *((0,) * (len(partition) - len(subpartition))))
    cells = {
        (row, column)
        for row, length in enumerate(partition)
        for column in range(padded[row], length)
    }
    if not cells:
        return None
    pending = [next(iter(cells))]
    visited = set(pending)
    while pending:
        row, column = pending.pop()
        for neighbor in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if neighbor in cells and neighbor not in visited:
                visited.add(neighbor)
                pending.append(neighbor)
    if visited != cells:
        return None
    for row, column in cells:
        if {
            (row, column),
            (row + 1, column),
            (row, column + 1),
            (row + 1, column + 1),
        }.issubset(cells):
            return None
    return len({row for row, _ in cells})


@lru_cache(maxsize=None)
def rim_hook_removals(
    partition: tuple[int, ...],
    length: int,
) -> tuple[tuple[tuple[int, ...], int], ...]:
    if length < 1 or length > sum(partition):
        return ()
    target = sum(partition) - length
    rows = []
    for subpartition in _contained_partitions(partition, target):
        height = _border_strip_height(partition, subpartition)
        if height is not None:
            rows.append((subpartition, height))
    return tuple(rows)


@lru_cache(maxsize=None)
def symmetric_character(
    partition: tuple[int, ...],
    cycle_type: tuple[int, ...],
) -> int:
    partition = normalize_partition(partition)
    cycle_type = tuple(sorted((value for value in cycle_type if value > 0), reverse=True))
    if not cycle_type:
        return 1 if not partition else 0
    if sum(partition) != sum(cycle_type):
        return 0
    length = cycle_type[0]
    tail = cycle_type[1:]
    return sum(
        (-1 if height % 2 == 0 else 1) * symmetric_character(reduced, tail)
        for reduced, height in rim_hook_removals(partition, length)
    )


@lru_cache(maxsize=None)
def kronecker_coefficient(
    left: tuple[int, ...],
    right: tuple[int, ...],
    target: tuple[int, ...],
) -> int:
    n = sum(left)
    if sum(right) != n or sum(target) != n:
        return 0
    numerator = sum(
        conjugacy_class_size(cycle_type)
        * symmetric_character(left, cycle_type)
        * symmetric_character(right, cycle_type)
        * symmetric_character(target, cycle_type)
        for cycle_type in integer_partitions(n)
    )
    order = math.factorial(n)
    if numerator % order:
        raise ArithmeticError("character inner product is not integral")
    value = numerator // order
    if value < 0:
        raise ArithmeticError("Kronecker coefficient is negative")
    return value
