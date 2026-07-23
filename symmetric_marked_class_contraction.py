"""Conjugacy-class compression for bounded-support character contractions.

For fixed permutations ``a,b`` supported on ``s=O(1)`` points, the signature
counts of

    (cycle_type(g), cycle_type(g a), cycle_type(g b)),  g in S_n

do not require enumerating ``n!`` permutations.  Inside one conjugacy class,
choose a canonical representative ``r``.  A uniformly random conjugate of
``r`` sees the marked support at a uniformly random ordered injection into its
``n`` positions.  Enumerating ``n_(s)`` injections therefore gives the exact
class contribution.  This is polynomial in ``n`` for fixed support, although
the current iteration over all integer partitions is not claimed as a quantum
circuit or as a polynomial-time algorithm in the bit length of ``n``.
"""

from __future__ import annotations

import itertools
import math
from collections import Counter
from fractions import Fraction
from functools import lru_cache

import numpy as np

from representation_obstruction import integer_partitions
from symmetric_character import conjugacy_class_size


Permutation = tuple[int, ...]
PairComponent = tuple[Permutation, Permutation]
PairKey = tuple[PairComponent, ...]


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)


def cycle_type(permutation: Permutation) -> tuple[int, ...]:
    visited = [False] * len(permutation)
    lengths: list[int] = []
    for start in range(len(permutation)):
        if visited[start]:
            continue
        current = start
        length = 0
        while not visited[current]:
            visited[current] = True
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def _rooted_component_encoding(
    left: Permutation,
    right: Permutation,
    component: set[int],
    root: int,
) -> PairComponent:
    left_inverse = inverse(left)
    right_inverse = inverse(right)
    order = [root]
    relabel = {root: 0}
    cursor = 0
    while cursor < len(order):
        point = order[cursor]
        cursor += 1
        for generator in (left, right, left_inverse, right_inverse):
            image = generator[point]
            if image in component and image not in relabel:
                relabel[image] = len(order)
                order.append(image)
    if len(order) != len(component):
        raise ArithmeticError("pair-generator component traversal was incomplete")
    return (
        tuple(relabel[left[point]] for point in order),
        tuple(relabel[right[point]] for point in order),
    )


def canonical_pair_key(left: Permutation, right: Permutation) -> PairKey:
    """Canonicalize a permutation pair under simultaneous conjugation."""

    if len(left) != len(right):
        raise ValueError("permutations must have equal degree")
    active = {
        point
        for point in range(len(left))
        if left[point] != point or right[point] != point
    }
    if not active:
        return ()
    left_inverse = inverse(left)
    right_inverse = inverse(right)
    unseen = set(active)
    components: list[PairComponent] = []
    while unseen:
        seed = min(unseen)
        component = {seed}
        pending = [seed]
        while pending:
            point = pending.pop()
            for generator in (left, right, left_inverse, right_inverse):
                image = generator[point]
                if image not in component:
                    component.add(image)
                    pending.append(image)
        unseen.difference_update(component)
        encodings = [
            _rooted_component_encoding(left, right, component, root)
            for root in component
        ]
        components.append(min(encodings))
    return tuple(sorted(components))


def pair_from_key(key: PairKey) -> tuple[Permutation, Permutation]:
    support_size = sum(len(component[0]) for component in key)
    left = list(range(support_size))
    right = list(range(support_size))
    offset = 0
    for left_component, right_component in key:
        if len(left_component) != len(right_component):
            raise ValueError("component permutations must have equal degree")
        for index, image in enumerate(left_component):
            left[offset + index] = offset + image
        for index, image in enumerate(right_component):
            right[offset + index] = offset + image
        offset += len(left_component)
    return tuple(left), tuple(right)


def _canonical_class_representative(cycle_partition: tuple[int, ...]) -> Permutation:
    n = sum(cycle_partition)
    permutation = list(range(n))
    offset = 0
    for length in cycle_partition:
        for index in range(length):
            permutation[offset + index] = offset + (index + 1) % length
        offset += length
    return tuple(permutation)


def _right_product_cycle_type(
    representative: Permutation,
    active: Permutation,
    injection: tuple[int, ...],
) -> tuple[int, ...]:
    product = list(representative)
    for local_point, image in enumerate(active):
        product[injection[local_point]] = representative[injection[image]]
    return cycle_type(tuple(product))


@lru_cache(maxsize=None)
def class_compressed_signature_counts(
    n: int,
    key: PairKey,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray]:
    """Count bounded-support character signatures exactly by conjugacy class."""

    active_left, active_right = pair_from_key(key)
    support_size = len(active_left)
    if support_size > n:
        raise ValueError("active support exceeds permutation degree")
    cycle_types = tuple(integer_partitions(n))
    cycle_type_ids = {
        cycle_partition: index
        for index, cycle_partition in enumerate(cycle_types)
    }
    type_count = len(cycle_types)
    rational_counts: dict[int, Fraction] = {}
    injection_count = math.perm(n, support_size)
    for group_type in cycle_types:
        representative = _canonical_class_representative(group_type)
        local_counts: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
        for injection in itertools.permutations(range(n), support_size):
            left_type = _right_product_cycle_type(
                representative, active_left, injection
            )
            right_type = _right_product_cycle_type(
                representative, active_right, injection
            )
            local_counts[(left_type, right_type)] += 1
        factor = Fraction(conjugacy_class_size(group_type), injection_count)
        group_index = cycle_type_ids[group_type]
        for (left_type, right_type), count in local_counts.items():
            code = (
                group_index * type_count * type_count
                + cycle_type_ids[left_type] * type_count
                + cycle_type_ids[right_type]
            )
            rational_counts[code] = rational_counts.get(code, Fraction()) + count * factor
    counts = np.zeros(type_count**3, dtype=np.int64)
    for code, count in rational_counts.items():
        if count.denominator != 1:
            raise ArithmeticError("compressed conjugacy-class count is not integral")
        counts[code] = count.numerator
    if int(counts.sum()) != math.factorial(n):
        raise ArithmeticError("compressed signatures do not sum to |S_n|")
    return cycle_types, counts


def pair_support_size(key: PairKey) -> int:
    return sum(len(component[0]) for component in key)
