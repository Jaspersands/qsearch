"""Exact class-Fourier contraction for quotient transfer distributions."""

from __future__ import annotations

import itertools
import math
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np

from coset_typical_commutant_moment_audit import _cycle_type
from representation_obstruction import integer_partitions
from symmetric_character import symmetric_character


@dataclass(frozen=True)
class TranslationContractionMetrics:
    n: int
    target_count: int
    maximum_degree: int
    quotient_state_union_count: int
    unique_left_translation_count: int
    unique_right_translation_count: int
    conjugacy_class_count: int
    temporary_character_table_bytes: int
    chunk_rows: int
    maximum_character_chunk_bytes: int


def unpack_pair(
    key: int,
    n: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left = tuple((key >> (4 * index)) & 15 for index in range(n))
    right = tuple((key >> (4 * n + 4 * index)) & 15 for index in range(n))
    return left, right


def class_block_target_contractions(
    selected_right_characters: np.ndarray,
    left_characters: np.ndarray,
    class_boundaries: tuple[tuple[int, int], ...],
    target_characters_by_type: np.ndarray,
) -> np.ndarray:
    class_sums = np.empty(
        (selected_right_characters.shape[0], len(class_boundaries)),
        dtype=np.int64,
    )
    for type_index, (start, end) in enumerate(class_boundaries):
        class_sums[:, type_index] = (
            selected_right_characters[:, start:end]
            @ left_characters[start:end]
        )
    return class_sums @ target_characters_by_type.T


def exact_translation_character_contraction(
    *,
    n: int,
    source_partition: tuple[int, ...],
    distributions: dict[int, dict[int, int]],
    target_certificates: tuple[dict[str, object], ...],
    orbit_denominator: int,
    chunk_rows: int = 128,
) -> tuple[
    dict[tuple[int, ...], tuple[Fraction, ...]],
    TranslationContractionMetrics,
]:
    if not distributions:
        raise ValueError("at least one transfer distribution is required")
    if chunk_rows < 1:
        raise ValueError("chunk_rows must be positive")
    targets = tuple(item["target"] for item in target_certificates)
    keys = set().union(*(set(rows) for rows in distributions.values()))
    pairs = {key: unpack_pair(key, n) for key in keys}
    lefts = sorted({left for left, _ in pairs.values()})
    rights = sorted({right for _, right in pairs.values()})
    right_indices = {right: index for index, right in enumerate(rights)}

    permutations = np.array(
        list(itertools.permutations(range(n))),
        dtype=np.uint8,
    )
    cycle_types = tuple(integer_partitions(n))
    cycle_type_ids = {value: index for index, value in enumerate(cycle_types)}
    rank_group_type_ids = np.fromiter(
        (cycle_type_ids[_cycle_type(tuple(row))] for row in permutations),
        dtype=np.uint8,
        count=len(permutations),
    )
    class_order = np.argsort(rank_group_type_ids, kind="stable")
    permutations = permutations[class_order]
    group_type_ids = rank_group_type_ids[class_order]
    class_counts = np.bincount(
        group_type_ids,
        minlength=len(cycle_types),
    )
    class_offsets = np.concatenate(([0], np.cumsum(class_counts)))
    class_boundaries = tuple(
        (int(class_offsets[index]), int(class_offsets[index + 1]))
        for index in range(len(cycle_types))
    )
    source_by_type = np.array(
        [symmetric_character(source_partition, value) for value in cycle_types],
        dtype=np.int16,
    )
    source_by_rank = source_by_type[rank_group_type_ids]
    target_by_type = np.array(
        [
            [symmetric_character(target, value) for value in cycle_types]
            for target in targets
        ],
        dtype=np.int16,
    ).astype(np.int64)
    factorial_weights = np.array(
        [math.factorial(n - index - 1) for index in range(n)],
        dtype=np.int64,
    )

    def translated_source_characters(right: tuple[int, ...]) -> np.ndarray:
        translated = permutations[:, right]
        ranks = np.zeros(len(permutations), dtype=np.int64)
        for index in range(n - 1):
            ranks += (
                np.sum(
                    translated[:, index, None]
                    > translated[:, index + 1 :],
                    axis=1,
                )
                * factorial_weights[index]
            )
        return source_by_rank[ranks]

    with tempfile.TemporaryDirectory(
        prefix=f"qsearch-s{n}-characters-"
    ) as directory:
        character_path = Path(directory) / "right_characters.dat"
        right_characters = np.memmap(
            character_path,
            dtype=np.int16,
            mode="w+",
            shape=(len(rights), len(permutations)),
        )
        for index, right in enumerate(rights):
            right_characters[index] = translated_source_characters(right)
        right_characters.flush()

        pairs_by_left: defaultdict[
            tuple[int, ...], list[tuple[int, int]]
        ] = defaultdict(list)
        for key, (left, right) in pairs.items():
            pairs_by_left[left].append((key, right_indices[right]))
        contractions: dict[int, tuple[int, ...]] = {}
        for left in lefts:
            left_characters = translated_source_characters(left).astype(np.int64)
            rows = pairs_by_left[left]
            for start in range(0, len(rows), chunk_rows):
                chunk = rows[start : start + chunk_rows]
                selected = right_characters[[index for _, index in chunk]]
                values = class_block_target_contractions(
                    selected,
                    left_characters,
                    class_boundaries,
                    target_by_type,
                )
                for row_index, (key, _) in enumerate(chunk):
                    contractions[key] = tuple(
                        int(values[row_index, target_index])
                        for target_index in range(len(targets))
                    )

    result: dict[tuple[int, ...], tuple[Fraction, ...]] = {}
    for target_index, item in enumerate(target_certificates):
        traces = []
        for degree in range(1, int(item["multiplicity"]) + 1):
            numerator = sum(
                weight * contractions[key][target_index]
                for key, weight in distributions[degree].items()
            )
            traces.append(
                Fraction(
                    numerator,
                    math.factorial(n) * orbit_denominator ** (degree - 1),
                )
            )
        result[item["target"]] = tuple(traces)
    metrics = TranslationContractionMetrics(
        n=n,
        target_count=len(targets),
        maximum_degree=max(distributions),
        quotient_state_union_count=len(keys),
        unique_left_translation_count=len(lefts),
        unique_right_translation_count=len(rights),
        conjugacy_class_count=len(cycle_types),
        temporary_character_table_bytes=(
            len(rights) * math.factorial(n) * np.dtype(np.int16).itemsize
        ),
        chunk_rows=chunk_rows,
        maximum_character_chunk_bytes=(
            chunk_rows * math.factorial(n) * np.dtype(np.int16).itemsize
        ),
    )
    return result, metrics
