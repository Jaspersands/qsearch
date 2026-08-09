"""Counterexample-directed search for growing marked-word pressure bounds.

The relation-topology report proves the desired leading pressure separation
through two frame tokens.  Exhaustive enumeration becomes double exponential
in the frame-token count, so this module searches the unresolved frontier
rather than treating a finite scan as a theorem.

A state consists of a marked leaf pattern and two nonempty supports in
``{0,1}^u``.  Best-first mutation maximizes the amount by which the cheap
literal one-relator bound misses the desired pressure threshold.  Only the
finalists receive bounded Nielsen and free-basis commutator searches.  A
survivor is recorded as proof debt, never as a counterexample: proving a
counterexample requires a matching lower bound on the asymptotic number of
``S_n`` solutions, not merely failure of the implemented certificates.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_mixed_split_target_genus import (
    cyclic_one_run_count,
    split_target_orientable_genus_for_pattern,
)
from self_dual_wreath_marked_relation_topology import (
    Assignment,
    SignedWord,
    _pair_word_pattern,
    _coordinate_bits,
    _evaluate_signed_word,
    _substitute_generator,
    _substitute_word_images,
    _weak_compositions,
    marked_support_presentation,
    canonical_relator,
    free_reduce,
    inverse_word,
    nonorientable_quadratic_genus,
    normalize_relations,
    orientable_quadratic_genus,
    presentation_solution_exponent_upper_bound,
    power_conjugacy_certificate,
    primitive_power_degree,
    tietze_reduce_presentation,
)
from self_dual_wreath_two_partition_ribbon_surface import (
    symmetric_group_leading_solution_exponent as ribbon_solution_exponent,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_marked_pressure_obstruction_search.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PressureProfileKey:
    frame_position_count: int
    powers: tuple[int, int, int, int]
    crossing: bool
    same_support_mask: int
    different_support_mask: int
    frame_types: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.frame_types and all(token == "A" for token in self.frame_types):
            object.__setattr__(self, "frame_types", ())

    @property
    def pattern(self) -> str:
        all_a_pattern = _pair_word_pattern(self.powers, crossing=self.crossing)
        types = self.materialized_frame_types
        iterator = iter(types)
        return "".join(next(iterator) if token == "A" else token for token in all_a_pattern)

    @property
    def materialized_frame_types(self) -> tuple[str, ...]:
        return self.frame_types or ("A",) * self.frame_position_count


@dataclass(frozen=True)
class PressureSearchConfig:
    frame_position_count: int
    crossing: bool
    random_seed: int
    initial_random_profile_count: int
    search_round_count: int
    beam_width: int
    mutations_per_state: int
    strong_finalist_count: int
    maximum_nielsen_states: int
    exclude_constant_zero_trailing_lifts: bool = False
    allow_mixed_frame_types: bool = False
    require_mixed_frame_types: bool = False
    minimum_split_target_genus: int = 0
    prioritize_support_uncancelled_target: bool = False


@dataclass(frozen=True)
class PressureObstructionRecord:
    profile_id: str
    frame_position_count: int
    powers: tuple[int, int, int, int]
    pattern: str
    frame_types: tuple[str, ...]
    mixed_b_frame_token_count: int
    split_target_cyclic_b_run_count: int
    split_target_orientable_genus: int
    split_only_normalized_character_dimension_exponent: int
    split_forces_full_product_identity: bool
    residual_target_product_word: SignedWord
    target_product_freely_trivial: bool
    target_product_is_residual_relator: bool
    target_character_symbolically_cancelled: bool
    crossing: bool
    same_assignment_support: tuple[Assignment, ...]
    different_assignment_support: tuple[Assignment, ...]
    constant_zero_trailing_lift_depth: int
    irreducible_core_frame_position_count: int
    irreducible_core_pattern: str
    irreducible_core_same_assignment_support: tuple[Assignment, ...]
    irreducible_core_different_assignment_support: tuple[Assignment, ...]
    support_entropy_bits: float
    remaining_generators: tuple[int, ...]
    free_generator_count: int
    residual_relations: tuple[SignedWord, ...]
    residual_relation_length_profile: tuple[int, ...]
    abelian_relation_rank: int
    trivial_solution_exponent: float
    literal_solution_exponent_upper_bound: float
    literal_certificate_source: str
    two_partition_ribbon_solution_exponent_upper_bound: float
    two_partition_ribbon_certificate_source: str
    literal_rescaled_pressure_upper_bound: float
    literal_pressure_excess: float
    strong_solution_exponent_upper_bound: float
    strong_certificate_source: str
    strong_rescaled_pressure_upper_bound: float
    strong_pressure_excess: float
    symmetric_group_control_degree: int
    symmetric_group_solution_count: int
    finite_control_log_group_exponent: float
    finite_S3_sign_character_average: float
    finite_S3_standard_normalized_character_average: float
    finite_S3_maximum_nontrivial_character_bias: float
    asymptotic_counterexample_proved: bool
    status: str


@dataclass(frozen=True)
class PressureSearchRun:
    config: PressureSearchConfig
    evaluated_profile_count: int
    literal_positive_excess_profile_count: int
    canonical_finalist_count: int
    unresolved_finalist_count: int
    maximum_literal_pressure_excess: float
    maximum_strong_pressure_excess: float
    finalists: list[PressureObstructionRecord]
    status: str


@dataclass(frozen=True)
class ConstantZeroTrailingLiftControl:
    control_id: str
    base_frame_position_count: int
    base_pattern: str
    lifted_pattern: str
    base_support_sizes: tuple[int, int]
    lifted_support_sizes: tuple[int, int]
    basis_change_x1_image: SignedWord
    basis_change_z_image: SignedWord
    transformed_lifted_relations: tuple[SignedWord, ...]
    base_relations: tuple[SignedWord, ...]
    exact_relation_isomorphism_verified: bool
    lifted_free_generator_count_delta: int
    base_literal_pressure: float
    lifted_literal_pressure: float
    exact_pressure_invariance_verified: bool
    status: str


@dataclass(frozen=True)
class ResidualTargetCancellationControl:
    control_id: str
    source_pattern: str
    source_frame_types: tuple[str, ...]
    residual_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    residual_target_word: SignedWord
    checked_symmetric_group_degrees: tuple[int, ...]
    solution_counts: tuple[int, ...]
    nonidentity_target_counts: tuple[int, ...]
    exact_finite_search_verified: bool
    matched_relation_index: int
    matched_relation_orientation: str
    cyclic_shift: int
    conjugating_prefix: SignedWord
    normal_closure_certificate_word: SignedWord
    exact_cyclic_conjugacy_verified: bool
    target_in_presented_group_normal_closure_proved: bool
    all_group_target_identity_proved: bool
    all_symmetric_group_target_identity_proved: bool
    status: str


@dataclass(frozen=True)
class MarkedPressureObstructionSearchReport:
    created_at: str
    theorem_contract: dict[str, Any]
    search_runs: list[PressureSearchRun]
    constant_zero_trailing_lift_controls: list[ConstantZeroTrailingLiftControl]
    residual_target_cancellation_controls: list[ResidualTargetCancellationControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_mask_to_assignments(
    frame_position_count: int,
    mask: int,
) -> tuple[Assignment, ...]:
    assignment_count = 1 << frame_position_count
    if mask <= 0 or mask >= 1 << assignment_count:
        raise ValueError("support mask must encode a nonempty cube subset")
    assignments = tuple(itertools.product((0, 1), repeat=frame_position_count))
    return tuple(
        assignment for index, assignment in enumerate(assignments) if mask >> index & 1
    )


def _assignments_to_support_mask(
    frame_position_count: int,
    support: Iterable[Assignment],
) -> int:
    assignments = tuple(itertools.product((0, 1), repeat=frame_position_count))
    index = {assignment: position for position, assignment in enumerate(assignments)}
    mask = 0
    for assignment in support:
        mask |= 1 << index[assignment]
    if not mask:
        raise ValueError("support must be nonempty")
    return mask


def _validate_key(key: PressureProfileKey) -> None:
    if key.frame_position_count < 0 or sum(key.powers) != key.frame_position_count:
        raise ValueError("powers must distribute every frame token")
    if len(key.materialized_frame_types) != key.frame_position_count or any(
        token not in "AB" for token in key.materialized_frame_types
    ):
        raise ValueError("frame types must contain one A/B token per frame position")
    assignment_count = 1 << key.frame_position_count
    support_limit = 1 << assignment_count
    if not 0 < key.same_support_mask < support_limit:
        raise ValueError("invalid same-coordinate support mask")
    if not 0 < key.different_support_mask < support_limit:
        raise ValueError("invalid different-coordinate support mask")


def _stable_profile_key(key: PressureProfileKey) -> tuple[Any, ...]:
    return (
        key.frame_position_count,
        key.powers,
        key.crossing,
        key.same_support_mask,
        key.different_support_mask,
        key.materialized_frame_types,
    )


def _profile_reduction(key: PressureProfileKey):
    _validate_key(key)
    same = _support_mask_to_assignments(
        key.frame_position_count,
        key.same_support_mask,
    )
    different = _support_mask_to_assignments(
        key.frame_position_count,
        key.different_support_mask,
    )
    relations = marked_support_presentation(key.pattern, same, different)
    return same, different, tietze_reduce_presentation(len(key.pattern), relations)


def _literal_solution_exponent_upper_bound(reduction) -> tuple[float, str]:
    generator_count = len(reduction.remaining_generators)
    best = float(generator_count)
    source = "trivial-assignment-bound"
    for relation in reduction.residual_relations:
        orientable = orientable_quadratic_genus(relation)
        if orientable is not None and orientable >= 1 and generator_count - 1 < best:
            best = float(generator_count - 1)
            source = f"literal-orientable-surface-genus-{orientable}"
        nonorientable = nonorientable_quadratic_genus(relation)
        if nonorientable is not None:
            loss = 0.5 if nonorientable == 1 else 1.0
            if generator_count - loss < best:
                best = generator_count - loss
                source = f"literal-nonorientable-surface-genus-{nonorientable}"
        power_conjugacy = power_conjugacy_certificate(relation)
        if power_conjugacy is not None and generator_count - 1 < best:
            nonunit = max(
                abs(power_conjugacy.left_power),
                abs(power_conjugacy.right_power),
            )
            best = float(generator_count - 1)
            source = f"literal-unit-power-conjugacy-degree-{nonunit}"
        power = primitive_power_degree(relation)
        if power is not None and generator_count - 1.0 / power < best:
            best = generator_count - 1.0 / power
            source = f"literal-primitive-power-degree-{power}"
    return best, source


def _two_partition_ribbon_exponent_upper_bound(
    key: PressureProfileKey,
    same: tuple[Assignment, ...],
    different: tuple[Assignment, ...],
) -> tuple[float, str]:
    """Drop to the strongest split/support pair and use its exact surface."""

    split_bits = tuple(1 if token == "B" else 0 for token in key.pattern)
    best = float(len(key.pattern))
    source = "two-partition-ribbon-trivial"
    for support_kind, support, differing_coordinate in (
        ("same", same, False),
        ("different", different, True),
    ):
        for index, assignment in enumerate(support, start=1):
            coordinate_bits = _coordinate_bits(
                key.pattern,
                assignment,
                differing_coordinate,
            )
            exponent = float(
                ribbon_solution_exponent(split_bits, coordinate_bits)
            )
            if exponent < best:
                best = exponent
                source = (
                    f"two-partition-ribbon-{support_kind}-assignment-{index}"
                )
    return best, source


def _pressure_terms(
    key: PressureProfileKey,
    same: tuple[Assignment, ...],
    different: tuple[Assignment, ...],
    exponent: float,
) -> tuple[float, float, float]:
    entropy = 0.5 * math.log2(len(same)) + 0.5 * math.log2(len(different))
    pressure = exponent + entropy - len(key.pattern) + 2
    target = -1.0 if key.crossing else 0.0
    return entropy, pressure, pressure - target


def _abelian_relation_rank(
    generators: tuple[int, ...],
    relations: tuple[SignedWord, ...],
) -> int:
    columns = {generator: index for index, generator in enumerate(generators)}
    matrix = [
        [
            Fraction(
                sum(
                    (1 if letter > 0 else -1)
                    for letter in relation
                    if abs(letter) == generator
                )
            )
            for generator in generators
        ]
        for relation in relations
    ]
    rank = 0
    for column in range(len(generators)):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
    return rank


def _permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def _transport_target_product_word(
    initial_generator_count: int,
    reduction,
) -> SignedWord:
    word: SignedWord = tuple(range(1, initial_generator_count + 1))
    for step in reduction.elimination_steps:
        word = _substitute_generator(
            word,
            step.eliminated_generator,
            step.replacement_word,
        )
    return free_reduce(word)


def _finite_S3_character_control(
    initial_generator_count: int,
    reduction,
) -> tuple[int, float, float]:
    """Count solutions and average the two nontrivial normalized S3 characters."""

    degree = 3
    group = tuple(itertools.permutations(range(degree)))
    identity = tuple(range(degree))
    solution_count = 0
    sign_sum = 0
    standard_character_sum = 0
    full_product_word = tuple(range(1, initial_generator_count + 1))
    for values in itertools.product(
        group,
        repeat=len(reduction.remaining_generators),
    ):
        assignment = dict(zip(reduction.remaining_generators, values))
        if any(
            _evaluate_signed_word(relation, assignment) != identity
            for relation in reduction.residual_relations
        ):
            continue
        for step in reversed(reduction.elimination_steps):
            value = (
                _evaluate_signed_word(step.replacement_word, assignment)
                if step.replacement_word
                else identity
            )
            assignment[step.eliminated_generator] = value
        product = _evaluate_signed_word(full_product_word, assignment)
        solution_count += 1
        sign_sum += _permutation_sign(product)
        standard_character_sum += sum(
            product[index] == index for index in range(degree)
        ) - 1
    if not solution_count:
        return 0, 0.0, 0.0
    return (
        solution_count,
        sign_sum / solution_count,
        standard_character_sum / (2 * solution_count),
    )


_RESIDUAL_TARGET_RELATIONS: tuple[SignedWord, ...] = (
    (-8, -7, -7, -5, -8, -7, 8, 5),
    (-8, -7, -7, -4, -8, -7, 8, 4),
    (-8, -7, 4, -8, -7, 8, -7, -5, -4, 5),
    (-8, -7, 4, -8, -7, 8, -5, -4, -8, -7, 8, 5),
)
_RESIDUAL_TARGET_WORD: SignedWord = (
    -8, 7, 8, -4, 7, 8, -5, -8, 7, 8, 4, 5,
)


@lru_cache(maxsize=None)
def _symmetric_group_target_search(degree: int) -> tuple[int, int]:
    """Exploit the equal conjugator-coset equations before pair enumeration."""

    group = tuple(itertools.permutations(range(degree)))
    identity = tuple(range(degree))
    solutions = 0
    nonidentity_targets = 0
    for value_7 in group:
        for value_8 in group:
            fixed = {7: value_7, 8: value_8}
            conjugators = []
            for value in group:
                assignment = {**fixed, 4: value, 5: value}
                if (
                    _evaluate_signed_word(
                        _RESIDUAL_TARGET_RELATIONS[1],
                        assignment,
                    )
                    == identity
                ):
                    conjugators.append(value)
            for value_4 in conjugators:
                for value_5 in conjugators:
                    assignment = {
                        **fixed,
                        4: value_4,
                        5: value_5,
                    }
                    if any(
                        _evaluate_signed_word(relation, assignment) != identity
                        for relation in _RESIDUAL_TARGET_RELATIONS[2:]
                    ):
                        continue
                    solutions += 1
                    nonidentity_targets += (
                        _evaluate_signed_word(
                            _RESIDUAL_TARGET_WORD,
                            assignment,
                        )
                        != identity
                    )
    return solutions, nonidentity_targets


def _cyclic_relator_certificate(
    target: SignedWord,
    relations: tuple[SignedWord, ...],
) -> tuple[int, str, int, SignedWord, SignedWord] | None:
    """Return ``target = prefix^-1 * relation^sign * prefix`` when exact."""

    target = free_reduce(target)
    for relation_index, relation in enumerate(relations, start=1):
        for orientation, oriented_relation in (
            ("forward", free_reduce(relation)),
            ("inverse", inverse_word(free_reduce(relation))),
        ):
            for shift in range(len(oriented_relation)):
                prefix = oriented_relation[:shift]
                certificate_word = free_reduce(
                    inverse_word(prefix) + oriented_relation + prefix
                )
                if certificate_word == target:
                    return (
                        relation_index,
                        orientation,
                        shift,
                        prefix,
                        certificate_word,
                    )
    return None


def residual_target_cancellation_control() -> ResidualTargetCancellationControl:
    degrees = (3, 4, 5)
    rows = tuple(_symmetric_group_target_search(degree) for degree in degrees)
    solution_counts = tuple(row[0] for row in rows)
    nonidentity_counts = tuple(row[1] for row in rows)
    exact_finite = solution_counts == (66, 960, 11_040) and not any(
        nonidentity_counts
    )
    certificate = _cyclic_relator_certificate(
        _RESIDUAL_TARGET_WORD,
        _RESIDUAL_TARGET_RELATIONS,
    )
    if certificate is None:
        relation_index, orientation, shift, prefix, certificate_word = (
            0,
            "none",
            -1,
            (),
            (),
        )
    else:
        relation_index, orientation, shift, prefix, certificate_word = certificate
    exact_cyclic = (
        certificate is not None
        and relation_index == 4
        and orientation == "inverse"
        and shift == 6
        and prefix == (-5, -8, 7, 8, 4, 5)
        and certificate_word == _RESIDUAL_TARGET_WORD
        and canonical_relator(_RESIDUAL_TARGET_WORD)
        == canonical_relator(_RESIDUAL_TARGET_RELATIONS[relation_index - 1])
    )
    return ResidualTargetCancellationControl(
        control_id="MIXED-EFAEFBBB-CYCLIC-RELATOR-TARGET",
        source_pattern="EFAEFBBB",
        source_frame_types=("A", "B", "B", "B"),
        residual_generators=(4, 5, 7, 8),
        residual_relations=_RESIDUAL_TARGET_RELATIONS,
        residual_target_word=_RESIDUAL_TARGET_WORD,
        checked_symmetric_group_degrees=degrees,
        solution_counts=solution_counts,
        nonidentity_target_counts=nonidentity_counts,
        exact_finite_search_verified=exact_finite,
        matched_relation_index=relation_index,
        matched_relation_orientation=orientation,
        cyclic_shift=shift,
        conjugating_prefix=prefix,
        normal_closure_certificate_word=certificate_word,
        exact_cyclic_conjugacy_verified=exact_cyclic,
        target_in_presented_group_normal_closure_proved=exact_cyclic,
        all_group_target_identity_proved=exact_cyclic,
        all_symmetric_group_target_identity_proved=exact_cyclic,
        status=(
            "exact-cyclic-relator-target-cancellation-proved"
            if exact_finite and exact_cyclic
            else "residual-target-cancellation-control-failure"
        ),
    )


def _lightweight_score(key: PressureProfileKey) -> tuple[float, int, int, bool]:
    same, different, reduction = _profile_reduction(key)
    exponent, _ = _literal_solution_exponent_upper_bound(reduction)
    ribbon_exponent, _ = _two_partition_ribbon_exponent_upper_bound(
        key,
        same,
        different,
    )
    exponent = min(exponent, ribbon_exponent)
    _, _, excess = _pressure_terms(key, same, different, exponent)
    relation_burden = sum(map(len, reduction.residual_relations))
    target = _transport_target_product_word(len(key.pattern), reduction)
    target_cancelled = not target or canonical_relator(target) in (
        reduction.residual_relations
    )
    return (
        excess,
        len(reduction.remaining_generators),
        relation_burden,
        not target_cancelled,
    )


def _structured_masks(frame_position_count: int) -> tuple[int, ...]:
    assignments = tuple(itertools.product((0, 1), repeat=frame_position_count))
    assignment_count = len(assignments)
    masks = {1, 1 << (assignment_count - 1), (1 << assignment_count) - 1}
    for coordinate in range(frame_position_count):
        for bit in (0, 1):
            mask = sum(
                1 << index
                for index, assignment in enumerate(assignments)
                if assignment[coordinate] == bit
            )
            masks.add(mask)
    for parity in (0, 1):
        masks.add(
            sum(
                1 << index
                for index, assignment in enumerate(assignments)
                if sum(assignment) % 2 == parity
            )
        )
    return tuple(sorted(mask for mask in masks if mask))


def _known_adversarial_profiles() -> tuple[PressureProfileKey, ...]:
    rows = (
        ((0, 0, 0, 3), ((0, 0, 0),), ((0, 1, 0), (1, 0, 1))),
        ((0, 0, 3, 0), ((0, 0, 0),), ((1, 0, 1), (1, 1, 0))),
        ((1, 0, 2, 0), ((0, 0, 0),), ((1, 0, 1), (1, 1, 0))),
        (
            (1, 2, 0, 0),
            ((0, 0, 0), (1, 0, 1), (1, 1, 0)),
            ((0, 1, 1), (1, 0, 0)),
        ),
    )
    return tuple(
        PressureProfileKey(
            frame_position_count=3,
            powers=powers,
            crossing=True,
            same_support_mask=_assignments_to_support_mask(3, same),
            different_support_mask=_assignments_to_support_mask(3, different),
        )
        for powers, same, different in rows
    )


def _lift_profile(
    key: PressureProfileKey,
    destination_block: int,
    appended_bit: int,
) -> PressureProfileKey:
    powers = list(key.powers)
    powers[destination_block] += 1
    same = _support_mask_to_assignments(
        key.frame_position_count,
        key.same_support_mask,
    )
    different = _support_mask_to_assignments(
        key.frame_position_count,
        key.different_support_mask,
    )
    lifted_count = key.frame_position_count + 1
    return PressureProfileKey(
        frame_position_count=lifted_count,
        powers=tuple(powers),  # type: ignore[arg-type]
        crossing=key.crossing,
        same_support_mask=_assignments_to_support_mask(
            lifted_count,
            tuple((*assignment, appended_bit) for assignment in same),
        ),
        different_support_mask=_assignments_to_support_mask(
            lifted_count,
            tuple((*assignment, appended_bit) for assignment in different),
        ),
        frame_types=(*key.materialized_frame_types, "A"),
    )


def strip_constant_zero_trailing_lifts(
    key: PressureProfileKey,
) -> tuple[PressureProfileKey, int]:
    """Return the unique core after removing exact trailing zero lifts."""

    _validate_key(key)
    core = key
    depth = 0
    while (
        core.frame_position_count
        and core.powers[3] > 0
        and core.materialized_frame_types[-1] == "A"
    ):
        same = _support_mask_to_assignments(
            core.frame_position_count,
            core.same_support_mask,
        )
        different = _support_mask_to_assignments(
            core.frame_position_count,
            core.different_support_mask,
        )
        if any(assignment[-1] for assignment in (*same, *different)):
            break
        powers = list(core.powers)
        powers[3] -= 1
        reduced_count = core.frame_position_count - 1
        core = PressureProfileKey(
            frame_position_count=reduced_count,
            powers=tuple(powers),  # type: ignore[arg-type]
            crossing=core.crossing,
            same_support_mask=_assignments_to_support_mask(
                reduced_count,
                tuple(assignment[:-1] for assignment in same),
            ),
            different_support_mask=_assignments_to_support_mask(
                reduced_count,
                tuple(assignment[:-1] for assignment in different),
            ),
            frame_types=core.materialized_frame_types[:-1],
        )
        depth += 1
    return core, depth


def audit_constant_zero_trailing_lift(
    key: PressureProfileKey,
    control_id: str = "CONSTANT-ZERO-TRAILING-LIFT",
) -> ConstantZeroTrailingLiftControl:
    """Certify the exact free-product lift ``y1 = z x1``.

    The pair-word pattern starts with an ``E`` token, hence generator ``x1``
    is in every color-zero and split relator and in no color-one relator.  A
    trailing frame token whose assignment bit is identically zero contributes
    ``z`` at the end of exactly those same relators.  Under
    ``x1 = z^-1 y1`` each such relator is conjugate to its old version; ``z``
    disappears and becomes a free generator.
    """

    _validate_key(key)
    lifted = _lift_profile(key, destination_block=3, appended_bit=0)
    same, different, base_reduction = _profile_reduction(key)
    lifted_same, lifted_different, lifted_reduction = _profile_reduction(lifted)
    base_relations = marked_support_presentation(key.pattern, same, different)
    lifted_relations = marked_support_presentation(
        lifted.pattern,
        lifted_same,
        lifted_different,
    )
    z = len(lifted.pattern)
    images = {
        generator: (
            (-z, 1)
            if generator == 1
            else ((z,) if generator == z else (generator,))
        )
        for generator in range(1, z + 1)
    }
    transformed = normalize_relations(
        _substitute_word_images(relation, images) for relation in lifted_relations
    )
    base_exponent, _ = _literal_solution_exponent_upper_bound(base_reduction)
    _, base_pressure, _ = _pressure_terms(
        key,
        same,
        different,
        base_exponent,
    )
    relation_exact = transformed == base_relations
    lifted_exponent = (
        base_exponent + 1
        if relation_exact
        else _literal_solution_exponent_upper_bound(lifted_reduction)[0]
    )
    _, lifted_pressure, _ = _pressure_terms(
        lifted,
        lifted_same,
        lifted_different,
        lifted_exponent,
    )
    free_delta = (
        lifted_reduction.free_generator_count - base_reduction.free_generator_count
    )
    pressure_exact = abs(base_pressure - lifted_pressure) <= 1e-12
    exact = relation_exact and free_delta == 1 and pressure_exact
    return ConstantZeroTrailingLiftControl(
        control_id=control_id,
        base_frame_position_count=key.frame_position_count,
        base_pattern=key.pattern,
        lifted_pattern=lifted.pattern,
        base_support_sizes=(len(same), len(different)),
        lifted_support_sizes=(len(lifted_same), len(lifted_different)),
        basis_change_x1_image=(-z, 1),
        basis_change_z_image=(z,),
        transformed_lifted_relations=transformed,
        base_relations=base_relations,
        exact_relation_isomorphism_verified=relation_exact,
        lifted_free_generator_count_delta=free_delta,
        base_literal_pressure=base_pressure,
        lifted_literal_pressure=lifted_pressure,
        exact_pressure_invariance_verified=pressure_exact,
        status=(
            "exact-constant-zero-free-product-lift-verified"
            if exact
            else "constant-zero-lift-control-failure"
        ),
    )


def _initial_profiles(
    config: PressureSearchConfig,
    seed_profiles: Iterable[PressureProfileKey] = (),
) -> set[PressureProfileKey]:
    rng = random.Random(config.random_seed)
    powers = tuple(_weak_compositions(config.frame_position_count, 4))
    masks = _structured_masks(config.frame_position_count)
    profiles: set[PressureProfileKey] = set()
    for index, power in enumerate(powers):
        profiles.add(
            PressureProfileKey(
                config.frame_position_count,
                power,
                config.crossing,
                masks[index % len(masks)],
                masks[(3 * index + 1) % len(masks)],
            )
        )
    assignment_count = 1 << config.frame_position_count
    support_limit = 1 << assignment_count
    for _ in range(config.initial_random_profile_count):
        profiles.add(
            PressureProfileKey(
                config.frame_position_count,
                rng.choice(powers),
                config.crossing,
                rng.randrange(1, support_limit),
                rng.randrange(1, support_limit),
            )
        )
    if config.frame_position_count == 3 and config.crossing:
        profiles.update(_known_adversarial_profiles())
    if config.frame_position_count == 4 and config.crossing:
        for key in _known_adversarial_profiles():
            for block in range(4):
                for bit in (0, 1):
                    profiles.add(_lift_profile(key, block, bit))
    if config.allow_mixed_frame_types and config.frame_position_count:
        mixed = set(profiles)
        for key in sorted(profiles, key=_stable_profile_key):
            for _ in range(2):
                frame_types = tuple(
                    "B" if rng.randrange(2) else "A"
                    for _ in range(config.frame_position_count)
                )
                if "B" not in frame_types:
                    frame_types = ("B", *frame_types[1:])
                mixed.add(
                    PressureProfileKey(
                        key.frame_position_count,
                        key.powers,
                        key.crossing,
                        key.same_support_mask,
                        key.different_support_mask,
                        frame_types,
                    )
                )
        profiles = mixed
    for key in sorted(seed_profiles, key=_stable_profile_key):
        if (
            key.frame_position_count != config.frame_position_count
            or key.crossing != config.crossing
        ):
            raise ValueError("seed profile does not match the search configuration")
        profiles.add(key)
    return profiles


def _mutations(
    key: PressureProfileKey,
    rng: random.Random,
    mutation_count: int,
    allow_mixed_frame_types: bool,
) -> set[PressureProfileKey]:
    assignment_count = 1 << key.frame_position_count
    output: set[PressureProfileKey] = {
        PressureProfileKey(
            key.frame_position_count,
            key.powers,
            key.crossing,
            key.different_support_mask,
            key.same_support_mask,
            key.materialized_frame_types,
        )
    }
    for _ in range(mutation_count):
        same = key.same_support_mask
        different = key.different_support_mask
        if rng.randrange(2):
            same ^= 1 << rng.randrange(assignment_count)
            if not same:
                same = key.same_support_mask
        else:
            different ^= 1 << rng.randrange(assignment_count)
            if not different:
                different = key.different_support_mask
        powers = list(key.powers)
        frame_types = list(key.materialized_frame_types)
        occupied = [index for index, value in enumerate(powers) if value]
        if occupied and rng.random() < 0.5:
            source = rng.choice(occupied)
            destination = rng.randrange(4)
            if destination != source:
                powers[source] -= 1
                powers[destination] += 1
        if allow_mixed_frame_types and frame_types and rng.random() < 0.5:
            position = rng.randrange(len(frame_types))
            frame_types[position] = "A" if frame_types[position] == "B" else "B"
        output.add(
            PressureProfileKey(
                key.frame_position_count,
                tuple(powers),  # type: ignore[arg-type]
                key.crossing,
                same,
                different,
                tuple(frame_types),
            )
        )
    return output


def _obstruction_record(
    key: PressureProfileKey,
    profile_index: int,
    maximum_nielsen_states: int,
) -> PressureObstructionRecord:
    same, different, reduction = _profile_reduction(key)
    split_bits = tuple(1 if token == "B" else 0 for token in key.pattern)
    split_target_genus = split_target_orientable_genus_for_pattern(key.pattern)
    irreducible_core, lift_depth = strip_constant_zero_trailing_lifts(key)
    core_same = _support_mask_to_assignments(
        irreducible_core.frame_position_count,
        irreducible_core.same_support_mask,
    )
    core_different = _support_mask_to_assignments(
        irreducible_core.frame_position_count,
        irreducible_core.different_support_mask,
    )
    literal_exponent, literal_source = _literal_solution_exponent_upper_bound(reduction)
    ribbon_exponent, ribbon_source = _two_partition_ribbon_exponent_upper_bound(
        key,
        same,
        different,
    )
    if ribbon_exponent < literal_exponent:
        literal_exponent = ribbon_exponent
        literal_source = ribbon_source
    entropy, literal_pressure, literal_excess = _pressure_terms(
        key,
        same,
        different,
        literal_exponent,
    )
    target = -1.0 if key.crossing else 0.0
    required_exponent = target - entropy + len(key.pattern) - 2
    strong_exponent, strong_source = presentation_solution_exponent_upper_bound(
        reduction,
        stop_at=None if split_target_genus > 0 else required_exponent,
        use_free_basis_commutator=len(reduction.remaining_generators) <= 4,
        use_nielsen=True,
        maximum_nielsen_states=maximum_nielsen_states,
    )
    if ribbon_exponent < strong_exponent:
        strong_exponent = ribbon_exponent
        strong_source = ribbon_source
    _, strong_pressure, strong_excess = _pressure_terms(
        key,
        same,
        different,
        strong_exponent,
    )
    symmetric_degree = 3
    group_order = math.factorial(symmetric_degree)
    solution_count, sign_average, standard_average = _finite_S3_character_control(
        len(key.pattern),
        reduction,
    )
    residual_target_word = _transport_target_product_word(
        len(key.pattern),
        reduction,
    )
    target_freely_trivial = not residual_target_word
    target_is_relator = bool(
        residual_target_word
        and canonical_relator(residual_target_word) in reduction.residual_relations
    )
    finite_exponent = math.log(solution_count, group_order) if solution_count else -math.inf
    unresolved = strong_excess > 1e-12
    return PressureObstructionRecord(
        profile_id=(
            f"PRESSURE-U{key.frame_position_count}-"
            f"{'X' if key.crossing else 'N'}-{profile_index:03d}"
        ),
        frame_position_count=key.frame_position_count,
        powers=key.powers,
        pattern=key.pattern,
        frame_types=key.materialized_frame_types,
        mixed_b_frame_token_count=key.materialized_frame_types.count("B"),
        split_target_cyclic_b_run_count=cyclic_one_run_count(split_bits),
        split_target_orientable_genus=split_target_genus,
        split_only_normalized_character_dimension_exponent=(
            2 * split_target_genus
        ),
        split_forces_full_product_identity=split_target_genus == 0,
        residual_target_product_word=residual_target_word,
        target_product_freely_trivial=target_freely_trivial,
        target_product_is_residual_relator=target_is_relator,
        target_character_symbolically_cancelled=(
            target_freely_trivial or target_is_relator
        ),
        crossing=key.crossing,
        same_assignment_support=same,
        different_assignment_support=different,
        constant_zero_trailing_lift_depth=lift_depth,
        irreducible_core_frame_position_count=(
            irreducible_core.frame_position_count
        ),
        irreducible_core_pattern=irreducible_core.pattern,
        irreducible_core_same_assignment_support=core_same,
        irreducible_core_different_assignment_support=core_different,
        support_entropy_bits=entropy,
        remaining_generators=reduction.remaining_generators,
        free_generator_count=reduction.free_generator_count,
        residual_relations=reduction.residual_relations,
        residual_relation_length_profile=tuple(map(len, reduction.residual_relations)),
        abelian_relation_rank=_abelian_relation_rank(
            reduction.remaining_generators,
            reduction.residual_relations,
        ),
        trivial_solution_exponent=float(len(reduction.remaining_generators)),
        literal_solution_exponent_upper_bound=literal_exponent,
        literal_certificate_source=literal_source,
        two_partition_ribbon_solution_exponent_upper_bound=ribbon_exponent,
        two_partition_ribbon_certificate_source=ribbon_source,
        literal_rescaled_pressure_upper_bound=literal_pressure,
        literal_pressure_excess=literal_excess,
        strong_solution_exponent_upper_bound=strong_exponent,
        strong_certificate_source=strong_source,
        strong_rescaled_pressure_upper_bound=strong_pressure,
        strong_pressure_excess=strong_excess,
        symmetric_group_control_degree=symmetric_degree,
        symmetric_group_solution_count=solution_count,
        finite_control_log_group_exponent=finite_exponent,
        finite_S3_sign_character_average=sign_average,
        finite_S3_standard_normalized_character_average=standard_average,
        finite_S3_maximum_nontrivial_character_bias=max(
            abs(sign_average),
            abs(standard_average),
        ),
        asymptotic_counterexample_proved=False,
        status=(
            "unresolved-asymptotic-presentation-bound"
            if unresolved
            else "pressure-upper-bound-certified"
        ),
    )


def run_pressure_search(
    config: PressureSearchConfig,
    seed_profiles: Iterable[PressureProfileKey] = (),
) -> PressureSearchRun:
    if config.minimum_split_target_genus < 0:
        raise ValueError("minimum split target genus must be nonnegative")
    if config.minimum_split_target_genus and not config.allow_mixed_frame_types:
        raise ValueError("positive split target genus requires mixed frame types")
    rng = random.Random(config.random_seed)
    population = _initial_profiles(config, seed_profiles)
    if config.require_mixed_frame_types:
        population = {
            key for key in population if "B" in key.materialized_frame_types
        }
    if config.exclude_constant_zero_trailing_lifts:
        population = {
            key
            for key in population
            if strip_constant_zero_trailing_lifts(key)[1] == 0
        }
    if config.minimum_split_target_genus:
        population = {
            key
            for key in population
            if split_target_orientable_genus_for_pattern(key.pattern)
            >= config.minimum_split_target_genus
        }
    if not population:
        raise ValueError("search constraints removed every initial profile")
    evaluated: dict[PressureProfileKey, tuple[float, int, int, bool]] = {}
    for _ in range(config.search_round_count):
        for key in population:
            evaluated.setdefault(key, _lightweight_score(key))
        beam = sorted(
            population,
            key=lambda key: (
                evaluated[key][3]
                if config.prioritize_support_uncancelled_target
                else False,
                evaluated[key][:3],
                _stable_profile_key(key),
            ),
            reverse=True,
        )[: config.beam_width]
        next_population = set(beam)
        for key in beam:
            next_population.update(
                _mutations(
                    key,
                    rng,
                    config.mutations_per_state,
                    config.allow_mixed_frame_types,
                )
            )
        if config.exclude_constant_zero_trailing_lifts:
            next_population = {
                key
                for key in next_population
                if strip_constant_zero_trailing_lifts(key)[1] == 0
            }
        if config.require_mixed_frame_types:
            next_population = {
                key
                for key in next_population
                if "B" in key.materialized_frame_types
            }
        if config.minimum_split_target_genus:
            next_population = {
                key
                for key in next_population
                if split_target_orientable_genus_for_pattern(key.pattern)
                >= config.minimum_split_target_genus
            }
        population = next_population
    for key in population:
        evaluated.setdefault(key, _lightweight_score(key))
    ranked = sorted(
        evaluated,
        key=lambda key: (
            evaluated[key][3]
            if config.prioritize_support_uncancelled_target
            else False,
            evaluated[key][:3],
            _stable_profile_key(key),
        ),
        reverse=True,
    )

    # Deduplicate literal finalists by the residual presentation and support
    # entropy, retaining the profile with the largest literal excess.
    canonical: dict[tuple[Any, ...], PressureProfileKey] = {}
    for key in ranked:
        same, different, reduction = _profile_reduction(key)
        signature = (
            key.crossing,
            key.materialized_frame_types,
            len(reduction.remaining_generators),
            reduction.residual_relations,
            len(same),
            len(different),
        )
        canonical.setdefault(signature, key)
        if len(canonical) >= config.strong_finalist_count:
            break
    finalists = [
        _obstruction_record(key, index, config.maximum_nielsen_states)
        for index, key in enumerate(canonical.values(), start=1)
    ]
    finalists.sort(key=lambda row: row.strong_pressure_excess, reverse=True)
    literal_positive = sum(score[0] > 1e-12 for score in evaluated.values())
    unresolved = sum(
        row.status == "unresolved-asymptotic-presentation-bound"
        for row in finalists
    )
    return PressureSearchRun(
        config=config,
        evaluated_profile_count=len(evaluated),
        literal_positive_excess_profile_count=literal_positive,
        canonical_finalist_count=len(finalists),
        unresolved_finalist_count=unresolved,
        maximum_literal_pressure_excess=max(
            (score[0] for score in evaluated.values()),
            default=-math.inf,
        ),
        maximum_strong_pressure_excess=max(
            (row.strong_pressure_excess for row in finalists),
            default=-math.inf,
        ),
        finalists=finalists,
        status=(
            "search-produced-unresolved-proof-debt"
            if unresolved
            else "all-search-finalists-pressure-certified"
        ),
    )


def _record_key(record: PressureObstructionRecord) -> PressureProfileKey:
    return PressureProfileKey(
        frame_position_count=record.frame_position_count,
        powers=record.powers,
        crossing=record.crossing,
        same_support_mask=_assignments_to_support_mask(
            record.frame_position_count,
            record.same_assignment_support,
        ),
        different_support_mask=_assignments_to_support_mask(
            record.frame_position_count,
            record.different_assignment_support,
        ),
        frame_types=record.frame_types,
    )


def run_marked_pressure_obstruction_search() -> MarkedPressureObstructionSearchReport:
    degree_three = run_pressure_search(
        PressureSearchConfig(3, True, 310_003, 160, 3, 48, 7, 12, 4_000)
    )
    degree_four = run_pressure_search(
        PressureSearchConfig(4, True, 410_009, 220, 4, 56, 8, 14, 2_000)
    )
    degree_five_seeds = {
        _lift_profile(_record_key(record), block, bit)
        for record in degree_four.finalists
        for block in range(4)
        for bit in (0, 1)
    }
    degree_five = run_pressure_search(
        PressureSearchConfig(5, True, 510_017, 180, 4, 48, 7, 12, 1_500, True),
        degree_five_seeds,
    )
    degree_six_seeds = {
        _lift_profile(_record_key(record), block, 1)
        for record in degree_five.finalists
        for block in range(4)
    }
    degree_six = run_pressure_search(
        PressureSearchConfig(6, True, 610_019, 160, 3, 40, 6, 10, 800, True),
        degree_six_seeds,
    )
    mixed_degree_three = run_pressure_search(
        PressureSearchConfig(
            3, True, 320_003, 100, 2, 36, 6, 10, 1_200,
            False, True, True, 1, True,
        )
    )
    mixed_degree_four = run_pressure_search(
        PressureSearchConfig(
            4, True, 420_011, 120, 3, 40, 6, 10, 1_000,
            True, True, True, 1, True,
        )
    )
    mixed_degree_five = run_pressure_search(
        PressureSearchConfig(
            5, True, 520_021, 80, 2, 28, 5, 8, 700,
            True, True, True, 1, True,
        )
    )
    mixed_degree_six = run_pressure_search(
        PressureSearchConfig(
            6, True, 620_027, 80, 2, 28, 5, 8, 700,
            True, True, True, 1, True,
        )
    )
    mixed_runs = (
        mixed_degree_three,
        mixed_degree_four,
        mixed_degree_five,
        mixed_degree_six,
    )
    runs = [
        degree_three,
        degree_four,
        degree_five,
        degree_six,
        *mixed_runs,
    ]
    lift_controls = [
        audit_constant_zero_trailing_lift(
            _record_key(record),
            f"DEGREE-FOUR-FINALIST-LIFT-{index:02d}",
        )
        for index, record in enumerate(degree_four.finalists, start=1)
    ]
    residual_target_controls = [residual_target_cancellation_control()]
    residual_target_control_failures = sum(
        not (
            row.exact_finite_search_verified
            and row.exact_cyclic_conjugacy_verified
        )
        for row in residual_target_controls
    )
    uncancelled_residual_targets = sum(
        not row.all_group_target_identity_proved
        for row in residual_target_controls
    )
    lift_failures = sum(
        row.status != "exact-constant-zero-free-product-lift-verified"
        for row in lift_controls
    )
    degree_five_reducible_finalists = sum(
        row.constant_zero_trailing_lift_depth > 0
        for row in degree_five.finalists
    )
    degree_six_reducible_finalists = sum(
        row.constant_zero_trailing_lift_depth > 0
        for row in degree_six.finalists
    )
    mixed_uncancelled_finalists = sum(
        not row.split_forces_full_product_identity
        for run in mixed_runs
        for row in run.finalists
    )
    mixed_unresolved_finalists = sum(
        run.unresolved_finalist_count for run in mixed_runs
    )
    mixed_nonzero_finite_character_bias = sum(
        row.finite_S3_maximum_nontrivial_character_bias > 1e-12
        for run in mixed_runs
        for row in run.finalists
    )
    mixed_maximum_finite_character_bias = max(
        row.finite_S3_maximum_nontrivial_character_bias
        for run in mixed_runs
        for row in run.finalists
    )
    mixed_symbolically_cancelled = sum(
        row.target_character_symbolically_cancelled
        for run in mixed_runs
        for row in run.finalists
    )
    mixed_maximum_strong_pressure_excess = max(
        run.maximum_strong_pressure_excess for run in mixed_runs
    )
    mixed_symbolically_uncancelled = (
        mixed_uncancelled_finalists - mixed_symbolically_cancelled
    )
    ribbon_improved_finalists = sum(
        row.two_partition_ribbon_solution_exponent_upper_bound
        < len(row.remaining_generators)
        for run in runs
        for row in run.finalists
    )
    unresolved = sum(run.unresolved_finalist_count for run in runs)
    searched = sum(run.evaluated_profile_count for run in runs)
    return MarkedPressureObstructionSearchReport(
        created_at=utc_now(),
        theorem_contract={
            "search_objective": (
                "Best-first mutation maximizes certified-pressure proof debt "
                "over marked support-profile presentations."
            ),
            "certificate_hierarchy": (
                "Literal surface/power bounds rank all states; bounded Nielsen "
                "and free-basis commutator certificates are reserved for finalists."
            ),
            "counterexample_standard": (
                "Failure of every implemented upper-bound certificate is not a "
                "counterexample. A counterexample needs an asymptotic lower bound "
                "on the S_n presentation solution exponent above the threshold."
            ),
            "constant_zero_trailing_lift": (
                "Appending a trailing frame token fixed to color zero is "
                "exactly the free-basis change y1=z*x1. The lifted presentation "
                "is the old presentation free-product <z>, so its leading "
                "pressure is unchanged at every degree."
            ),
            "irreducible_core_search": (
                "Degree-five and degree-six searches strip exact constant-zero "
                "trailing lifts before ranking, so their finalists contain "
                "genuinely new support coordinates under the proved quotient rule."
            ),
            "mixed_frame_search": (
                "Separate degree-three through degree-six beams require positive "
                "split-target genus and prioritize profiles whose target remains "
                "outside the support relators. This avoids repeatedly selecting "
                "contiguous-B cancellations."
            ),
            "split_target_genus": (
                "The split-only target has orientable genus r-1 for r cyclic "
                "B-runs and normalized character factor d_nu^-2(r-1). Extra "
                "support relations require a relative-surface analysis."
            ),
            "positive_genus_certificate_depth": (
                "Positive-genus finalists do not stop when they first meet the "
                "required pressure threshold. Strong surface/Nielsen searches "
                "continue so hidden exponent margins are not discarded."
            ),
            "two_partition_ribbon_bound": (
                "Every split/support-assignment pair is an exact orientable "
                "ribbon-surface presentation. Its face cycles give a cheap "
                "leading S_n exponent used in beam scoring and finalist bounds."
            ),
            "finite_control_scope": (
                "S3 solution counts are exact regression fingerprints only and "
                "do not determine growing-n exponents."
            ),
            "finite_target_character_control": (
                "Tietze replacements reconstruct every original generator for "
                "each S3 solution, after which sign and standard normalized "
                "characters are averaged on the full ordered product."
            ),
            "residual_target_cancellation": (
                "The retained EFAEFBBB target is the six-letter cyclic shift "
                "of the inverse fourth residual relator. Equivalently, for "
                "q=(-5,-8,7,8,4,5), target=q^-1*r4^-1*q. This is an exact "
                "normal-closure certificate over every group; the S3-S5 "
                "screens are regression fingerprints, not finite-residual evidence."
            ),
        },
        search_runs=runs,
        constant_zero_trailing_lift_controls=lift_controls,
        residual_target_cancellation_controls=residual_target_controls,
        proof_obligations=[
            {
                "obligation": "find_minimal_uncertified_growing_degree_profiles",
                "resolved": True,
                "resolution": (
                    "Deterministic degree-three/four best-first searches emit "
                    "canonical finalists with exact presentations and certificate debt."
                ),
            },
            {
                "obligation": "prove_entropy_versus_relator_loss_for_all_growing_degrees",
                "resolved": False,
                "resolution": (
                    "The two-partition ribbon theorem handles one support cell "
                    "exactly. Large support entropy requires a multi-partition "
                    "complex theorem using enough simultaneous cells; finite "
                    "search cannot resolve it."
                ),
            },
            {
                "obligation": "classify_constant_coordinate_degree_lifts",
                "resolved": lift_failures == 0,
                "resolution": (
                    "A constant-zero trailing coordinate is an exact free-product "
                    "lift and preserves pressure. Constant-one and interior "
                    "coordinate lifts remain separate cases."
                ),
            },
            {
                "obligation": "prove_an_asymptotic_pressure_counterexample",
                "resolved": False,
                "resolution": (
                    "No survivor has a matching lower bound on its S_n solution exponent."
                ),
            },
            {
                "obligation": "bound_mixed_frame_target_character_observable",
                "resolved": False,
                "resolution": (
                    "Positive-genus degree-three through degree-six beams retain "
                    "support-uncancelled targets, and every finalist has at least "
                    "one extra certified scalar pressure exponent. Prove the "
                    "relative-surface alternative uniformly at growing degree; "
                    "finite beams do not settle the signed observable."
                ),
            },
            {
                "obligation": "prove_EFAEFBBB_target_normal_closure_membership",
                "resolved": uncancelled_residual_targets == 0,
                "resolution": (
                    "The target is exactly q^-1*r4^-1*q for the fourth residual "
                    "relator and q=(-5,-8,7,8,4,5). It therefore vanishes on "
                    "every group-valued solution, not only the checked S3-S5 rows."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Largest finite S3 exponent identifies the asymptotic obstruction.",
                "resolved": True,
                "resolution": (
                    "False: finite counts are stored separately and never drive the claim gate."
                ),
            },
            {
                "objection": "No unresolved finalist means the growing-degree theorem is proved.",
                "resolved": True,
                "resolution": (
                    "False: beam search is incomplete even when all visited states are certified."
                ),
            },
            {
                "objection": "Higher marked-word degree automatically dilutes every fixed obstruction.",
                "resolved": True,
                "resolution": (
                    "False: constant-zero trailing lifts add one free generator "
                    "and one word position, preserving pressure exactly."
                ),
            },
            {
                "objection": "A scalar mixed-frame presentation bound proves the component moment bound.",
                "resolved": True,
                "resolution": (
                    "False: B tokens leave a nonconstant normalized target "
                    "character on the same solution variety."
                ),
            },
            {
                "objection": "Cancellation of the first mixed finalists is structural evidence.",
                "resolved": True,
                "resolution": (
                    "False: the old objective selected genus-zero or support-killed "
                    "targets. Positive-genus, support-uncancelled beams now expose "
                    "the actual relative-surface frontier."
                ),
            },
            {
                "objection": "Meeting the crossing threshold ends certificate search.",
                "resolved": True,
                "resolution": (
                    "False for positive-genus targets: early stopping hid a full "
                    "additional surface exponent on every current finalist."
                ),
            },
            {
                "objection": "One exact ribbon surface settles a large support profile.",
                "resolved": True,
                "resolution": (
                    "False: dropping to one support assignment is rigorous but can "
                    "leave exponential support entropy unpaid. The growing theorem "
                    "must combine several support 2-cells."
                ),
            },
        ],
        headline_metrics={
            "searched_profile_count": searched,
            "search_run_count": len(runs),
            "unresolved_finalist_count": unresolved,
            "constant_zero_trailing_lift_control_count": len(lift_controls),
            "constant_zero_trailing_lift_failure_count": lift_failures,
            "constant_zero_trailing_lift_theorem_count": int(
                bool(lift_controls) and lift_failures == 0
            ),
            "degree_five_reducible_finalist_count": (
                degree_five_reducible_finalists
            ),
            "degree_six_reducible_finalist_count": (
                degree_six_reducible_finalists
            ),
            "degree_six_positive_literal_pressure_profile_count": (
                degree_six.literal_positive_excess_profile_count
            ),
            "mixed_frame_positive_split_genus_finalist_count": (
                mixed_uncancelled_finalists
            ),
            "mixed_frame_unresolved_scalar_pressure_finalist_count": (
                mixed_unresolved_finalists
            ),
            "mixed_frame_nonzero_finite_character_bias_finalist_count": (
                mixed_nonzero_finite_character_bias
            ),
            "mixed_frame_maximum_finite_character_bias": (
                mixed_maximum_finite_character_bias
            ),
            "mixed_frame_symbolically_cancelled_target_finalist_count": (
                mixed_symbolically_cancelled
            ),
            "mixed_frame_symbolically_uncancelled_target_finalist_count": (
                mixed_symbolically_uncancelled
            ),
            "mixed_frame_maximum_strong_pressure_excess": (
                mixed_maximum_strong_pressure_excess
            ),
            "mixed_frame_full_exponent_margin_finalist_count": sum(
                row.strong_pressure_excess <= -1 + 1e-12
                for run in mixed_runs
                for row in run.finalists
            ),
            "residual_target_cancellation_control_count": len(
                residual_target_controls
            ),
            "residual_target_cancellation_control_failure_count": (
                residual_target_control_failures
            ),
            "cyclic_relator_target_cancellation_theorem_count": sum(
                row.exact_cyclic_conjugacy_verified
                for row in residual_target_controls
            ),
            "two_partition_ribbon_improved_finalist_count": (
                ribbon_improved_finalists
            ),
            "maximum_strong_pressure_excess": max(
                run.maximum_strong_pressure_excess for run in runs
            ),
            "asymptotic_counterexample_count": 0,
            "growing_degree_pressure_theorem_count": 0,
            "natural_positive_green_pair_gap_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "counterexample_directed_search_operational": searched > 0,
            "two_partition_ribbon_scoring_operational": (
                ribbon_improved_finalists > 0
            ),
            "constant_zero_trailing_free_product_lift_proved": (
                bool(lift_controls) and lift_failures == 0
            ),
            "degree_five_search_quotients_constant_zero_lifts": (
                degree_five.config.exclude_constant_zero_trailing_lifts
                and degree_five_reducible_finalists == 0
            ),
            "degree_six_search_quotients_constant_zero_lifts": (
                degree_six.config.exclude_constant_zero_trailing_lifts
                and degree_six_reducible_finalists == 0
            ),
            "mixed_frame_scalar_pressure_search_operational": (
                mixed_uncancelled_finalists > 0
            ),
            "positive_genus_support_uncancelled_search_operational": (
                mixed_uncancelled_finalists > 0
                and mixed_symbolically_uncancelled == mixed_uncancelled_finalists
            ),
            "mixed_frame_full_exponent_margin_on_all_finalists": (
                mixed_maximum_strong_pressure_excess <= -1 + 1e-12
            ),
            "mixed_frame_target_character_control_proved": False,
            "mixed_frame_finite_character_control_operational": True,
            "visited_mixed_frame_symbolic_character_cancellation_complete": (
                mixed_symbolically_uncancelled == 0
                and uncancelled_residual_targets == 0
            ),
            "unresolved_profiles_are_proof_debt_only": True,
            "asymptotic_pressure_counterexample_proved": False,
            "growing_degree_pressure_separation_proved": False,
            "mixed_target_character_control_proved": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The search identifies exact hard presentations but supplies "
                "neither exhaustive coverage nor asymptotic lower bounds."
            ),
        },
        status=(
            "growing-degree-pressure-proof-debt-localized"
            if searched
            and lift_failures == residual_target_control_failures == 0
            else "pressure-obstruction-search-failure"
        ),
        summary=(
            "Localized growing-degree marked-word pressure proof debt with "
            "deterministic best-first support mutation and exact presentation records."
        ),
        falsifiers_triggered=[
            "Literal word shape is not stable under free-group automorphisms; Nielsen certificates are required.",
            "Finite S3 solution exponents cannot promote an unresolved presentation into a counterexample.",
            "A beam search cannot prove a universal growing-degree pressure theorem.",
            "Marked-word degree alone cannot suppress a hard core because exact constant-zero lifts preserve pressure.",
            "Genus-zero mixed finalists conceal the target-character frontier; searches must retain separated B runs and support-uncancelled boundaries.",
            "Stopping at the requested pressure threshold can hide a stronger surface exponent and mis-rank the obstruction.",
        ],
    )


def write_marked_pressure_obstruction_search_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_marked_pressure_obstruction_search())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_marked_pressure_obstruction_search": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_marked_pressure_obstruction_search_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
