"""Exact polynomial label arithmetic for the S_(2m) class 2^m.

The two-quotient/hook formula is prior art. This is classical postprocessing
of supplied labels, not a way to obtain those labels from an HSP input.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from representation_obstruction import hook_length_dimension


@dataclass(frozen=True)
class InvolutionCharacterCertificate:
    partition: tuple[int, ...]
    degree: int
    quotient: tuple[tuple[int, ...], tuple[int, ...]]
    runner_bead_counts: tuple[int, int]
    two_core_empty: bool
    domino_sign: int
    character: int
    dimension: int
    character_ratio: Fraction
    tableau_paths_enumerated: int
    integer_bit_length_upper_bound: int


def fixed_point_free_character_certificate(partition: tuple[int, ...]) -> InvolutionCharacterCertificate:
    if (not isinstance(partition, tuple) or any(type(part) is not int or part < 1 for part in partition)
            or any(a < b for a, b in zip(partition, partition[1:]))):
        raise ValueError("partition must be a nonincreasing tuple of positive integers")
    degree = sum(partition)
    if degree % 2:
        raise ValueError("a fixed-point-free involution requires even degree")
    width = len(partition) + len(partition) % 2
    padded = partition + (0,) * (width - len(partition))
    beta = tuple(part + width - index - 1 for index, part in enumerate(padded))
    runners = tuple(tuple(value // 2 for value in beta if value % 2 == parity) for parity in (0, 1))
    quotient = tuple(tuple(value - len(runner) + index + 1
                           for index, value in enumerate(runner)
                           if value - len(runner) + index + 1 > 0) for runner in runners)
    empty_core = len(runners[0]) == len(runners[1])
    sign = -1 if sum(partition[1::2]) % 2 else 1
    if empty_core:
        left, right = quotient
        if sum(left) + sum(right) != degree // 2:
            raise ArithmeticError("two-quotient size identity failed")
        magnitude = (math.comb(degree // 2, sum(left))
                     * hook_length_dimension(left) * hook_length_dimension(right))
        character = sign * magnitude
    else:
        character = 0
    dimension = hook_length_dimension(partition)
    return InvolutionCharacterCertificate(
        partition, degree, quotient, (len(runners[0]), len(runners[1])), empty_core,
        sign, character, dimension, Fraction(character, dimension), 0,
        max(1, math.factorial(degree).bit_length()),
    )


def fixed_point_free_character(partition: tuple[int, ...]) -> int:
    return fixed_point_free_character_certificate(partition).character


def two_copy_label_decision(left: tuple[int, ...], right: tuple[int, ...], target: tuple[int, ...]) -> dict:
    """Score actual supplied labels; never enumerate/sample their joint law.

    The caller must obtain a legal target from the quantum front end. Checking
    or sampling a Kronecker target classically is NOT part of this interface.
    """
    records = [fixed_point_free_character_certificate(shape) for shape in (left, right, target)]
    if records[0].degree < 2 or len({row.degree for row in records}) != 1:
        raise ValueError("source and target labels must have the same positive even degree")
    score = sum((row.character_ratio for row in records), Fraction())
    return {
        "degree": records[0].degree,
        "likelihood_difference": score,
        "accept_hidden_class": score > 0,
        "tie": score == 0,
        "arithmetic": "exact rational two-quotient and hook-length arithmetic; polynomial bit complexity in degree",
        "score_numerator_bits": abs(score.numerator).bit_length(),
        "score_denominator_bits": score.denominator.bit_length(),
        "tableau_paths_enumerated": 0,
        "labels_supplied_by_caller": True,
        "classical_sampler_for_joint_label_law_supplied": False,
        "natural_source_mass_certified_by_this_score": False,
        "constant_copy_algorithm_has_scalable_advantage": False,
    }


def label_arithmetic_scaling_controls() -> list[dict]:
    controls = []
    for degree in (128, 512, 2048, 4096):
        # lambda tensor lambda always contains the trivial target. These are
        # arithmetic regressions, not selected high-mass algorithm branches.
        shape = (degree // 2, degree // 2)
        record = fixed_point_free_character_certificate(shape)
        decision = two_copy_label_decision(shape, shape, (degree,))
        controls.append({
            "degree": degree, "source_partition": list(shape), "target_partition": [degree],
            "dimension_bits": record.dimension.bit_length(), "character_bits": abs(record.character).bit_length(),
            "score_numerator_bits": decision["score_numerator_bits"],
            "score_denominator_bits": decision["score_denominator_bits"],
            "accept_hidden_class": decision["accept_hidden_class"],
            "absolute_ratio_at_most_one": abs(record.character_ratio) <= 1,
            "tableau_paths_enumerated": 0, "enumerated_all_partitions": False,
            "natural_source_coverage_claimed": False,
        })
    return controls
