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


def independent_pair_label_likelihood(pairs: tuple, unused_source_labels: tuple = ()) -> Fraction:
    """Exact terminal score for disjoint quantum pair measurements, shared h.

    Each complete label law is constant over the hidden conjugacy class, so
    these likelihood ratios multiply despite sharing h. This does not apply
    to overlapping sequential pair measurements or grant classical sampling.
    Actual legal labels must be supplied by the caller's quantum front end.
    """
    degree, ratio = None, Fraction(1)
    for labels in pairs:
        if len(labels) != 3:
            raise ValueError("each disjoint pair needs two source labels and one target")
        row = two_copy_label_decision(*labels)
        if degree is not None and row["degree"] != degree:
            raise ValueError("all pairs must have the same degree")
        degree = row["degree"]
        factor = 1 + row["likelihood_difference"]
        if factor < 0:
            raise ValueError("negative likelihood from incompatible quantum label outcome")
        ratio *= factor
    for label in unused_source_labels:
        record = fixed_point_free_character_certificate(label)
        if degree is not None and record.degree != degree:
            raise ValueError("all source labels must have the same degree")
        degree = record.degree
        ratio *= 1 + record.character_ratio
    if degree is None or degree < 2:
        raise ValueError("at least one positive-degree input required")
    return ratio


def coherent_walsh_terminal_decision(source_labels: tuple, outcomes: tuple, rule: str, *,
        phase_corrected: bool = False, threshold: int | None = None, complement: bool = False,
        parity_selection: str = "all") -> dict:
    """A declared cheap terminal rule, not an optimal likelihood-table lookup.

    Inputs are actual S_n fixed-point-free source labels and Walsh bits from
    the negative-character subset-phase program. Optional bit correction uses
    the known singleton phase. Neither a good success rate nor a speedup is
    guaranteed; threshold and accepting orientation are not fitted here.
    """
    if not source_labels or len(source_labels) != len(outcomes):
        raise ValueError("matching nonempty source labels and observed bits required")
    if any(type(bit) is not int or bit not in (0, 1) for bit in outcomes):
        raise ValueError("observed outcomes must be integer bits")
    if any(type(flag) is not bool for flag in (phase_corrected, complement)) or rule not in ("parity", "threshold"):
        raise ValueError("explicit correction flag and parity/threshold rule required")
    k = len(outcomes)
    if parity_selection not in ("all", "negative", "positive", "zero") or (rule != "parity" and parity_selection != "all"):
        raise ValueError("source selection is available only for parity, using a declared character-sign predicate")
    if rule == "parity" and threshold is not None:
        raise ValueError("parity does not take a threshold")
    if rule == "threshold":
        threshold = k // 2 + 1 if threshold is None else threshold
        if type(threshold) is not int or not 1 <= threshold <= k:
            raise ValueError("threshold must be an integer in [1,k]")
    records = [fixed_point_free_character_certificate(label) for label in source_labels]
    if records[0].degree < 2 or len({row.degree for row in records}) != 1:
        raise ValueError("all source labels must have the same positive even degree")
    selected = [parity_selection == "all" or
        (parity_selection == "negative" and row.character < 0) or
        (parity_selection == "positive" and row.character > 0) or
        (parity_selection == "zero" and row.character == 0) for row in records]
    weight = sum(bit ^ int(phase_corrected and row.character < 0)
                 for bit, row, keep in zip(outcomes, records, selected) if keep)
    decision = bool(weight % 2) if rule == "parity" else weight >= threshold
    return {"degree": records[0].degree, "copy_count": k, "rule": rule,
        "phase_corrected": phase_corrected, "threshold": threshold, "complement": complement,
        "observed_weight": weight, "parity_selection": parity_selection, "selected_copy_count": sum(selected),
        "parity_positions_fixed_before_source_labels": parity_selection == "all",
        "accept_hidden_class": decision != complement,
        "polynomial_terminal_arithmetic": True,
        "uses_fitted_likelihood_table": False, "quantum_frontend_classically_replaced": False,
        "scalable_success_established": False}


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
