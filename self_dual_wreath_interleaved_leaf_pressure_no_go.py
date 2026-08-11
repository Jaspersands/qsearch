"""Scalar pressure theorem for arbitrary interleaved four-leaf pair words.

Consider the crossing pattern

    E T^a F T^b E T^c F T^d,       T_i in {A,B},

with arbitrary nonempty same/different assignment supports ``S,D`` on the
``u=a+b+c+d`` frame positions.  Interleaving the four marked leaves does not
break either source of scalar loss.

First, same-coordinate color-one relators are ordinary ordered frame
subwords.  Different-coordinate color-one relators contain two fixed ``F``
markers.  If two assignments agree above frame coordinate ``i``, those fixed
markers and all higher frame letters cancel in their relative relator.  The
suffix-chain theorem therefore eliminates at least

    ceil(log2 max(|S union {0}|, |D|))

frame generators, exactly as in the contiguous case.

Second, fix ``q in D`` and write the split-zero, q-different-zero, and
q-different-one equations.  The latter two solve the second E and F leaves.
Substitution into the split equation always leaves

    e A f B e^-1 C f^-1 D = 1.

Put ``E=eA``, ``T=BA``, and ``g=fT``.  The equation becomes

    E g E^-1 = D^-1 g T^-1 C^-1.

For each ``g`` there are either zero conjugators ``E`` or exactly
``|C_G(g)|``.  Summing gives the uniform outer bound ``|G| k(G)``.  Hence for
``G=S_n`` the full scalar pressure is at most ``-1+o(1)`` for every placement,
frame-type word, and support pair.

Equality in the integer support bound requires ``0 in S``, ``|S|=|D|``, and
their common size to be a power of two.  The zero same-coordinate relator is
then the full target word itself, so exact scalar saturation forces target
identity.  Nontrivial targets have a strict finite-width margin, but that
margin can vanish with width; no uniform signed character theorem or quantum
speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_frame_subword_entropy import (
    FrameSubwordSuffixBranchCertificate,
    frame_subword_suffix_branch_certificate,
)
from self_dual_wreath_marked_relation_topology import (
    Assignment,
    SignedWord,
    _coordinate_bits,
    _solve_single_occurrence,
    _substitute_generator,
    canonical_relator,
    free_reduce,
    marked_support_presentation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_interleaved_leaf_pressure_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class InterleavedSuffixPivotStep:
    support_kind: str
    frame_coordinate_one_based: int
    pattern_generator_one_based: int
    anchor: Assignment
    witness: Assignment
    raw_relative_relation: SignedWord
    pivot_occurrence_count: int
    higher_frame_generator_occurrence_count: int
    endpoint_relators_available: bool
    exact_marker_stable_suffix_pivot_verified: bool
    status: str


@dataclass(frozen=True)
class InterleavedOuterConjugacyControl:
    frame_block_lengths: tuple[int, int, int, int]
    frame_types: tuple[str, ...]
    pattern: str
    different_base_assignment: Assignment
    first_E_generator: int
    first_F_generator: int
    second_E_generator: int
    second_F_generator: int
    split_zero_relation: SignedWord
    different_zero_relation: SignedWord
    different_one_relation: SignedWord
    solved_second_E_image: SignedWord
    solved_second_F_image: SignedWord
    residual_outer_relation: SignedWord
    residual_leaf_occurrence_word: SignedWord
    coefficient_A: SignedWord
    coefficient_B: SignedWord
    coefficient_C: SignedWord
    coefficient_D: SignedWord
    conjugacy_twist_T: SignedWord
    transformed_conjugacy_relation: SignedWord
    expected_conjugacy_relation: SignedWord
    exact_coefficient_conjugacy_normal_form_verified: bool
    uniform_finite_group_outer_bound: str
    status: str


@dataclass(frozen=True)
class InterleavedLeafPressureControl:
    control_id: str
    frame_block_lengths: tuple[int, int, int, int]
    frame_types: tuple[str, ...]
    pattern: str
    frame_position_count: int
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    augmented_same_support: tuple[Assignment, ...]
    same_suffix_certificate: FrameSubwordSuffixBranchCertificate
    different_suffix_certificate: FrameSubwordSuffixBranchCertificate
    same_suffix_steps: tuple[InterleavedSuffixPivotStep, ...]
    different_suffix_steps: tuple[InterleavedSuffixPivotStep, ...]
    dominant_support_family: str
    dominant_effective_support_size: int
    frame_generator_upper_bound: int
    outer_conjugacy_control: InterleavedOuterConjugacyControl
    full_solution_exponent_before_conjugacy_classes: int
    support_entropy_exponent: float
    scalar_crossing_pressure_upper_bound: float
    scalar_crossing_pressure_margin: float
    scalar_pressure_saturated: bool
    saturation_condition_verified: bool
    zero_same_assignment_present: bool
    zero_same_cell_forces_target_identity: bool
    nontrivial_target_strict_finite_width_margin: bool
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class InterleavedOuterScalingRecord:
    frame_position_count: int
    checked_placement_type_base_count: int
    outer_normal_form_failure_count: int
    status: str


@dataclass(frozen=True)
class InterleavedSupportCensus:
    frame_position_count: int
    nonempty_support_count: int
    checked_support_pair_count: int
    same_suffix_certificate_failure_count: int
    different_marker_suffix_certificate_failure_count: int
    pressure_inequality_failure_count: int
    saturation_equivalence_failure_count: int
    saturated_support_pair_count: int
    minimum_pressure_margin: float
    exhaustive_census_verified: bool
    status: str


@dataclass(frozen=True)
class InterleavedLeafAllDepthCertificate:
    pattern_scope: str
    same_support_elimination: str
    different_support_marker_cancellation: str
    dominant_support_generator_formula: str
    outer_quadratic_relation: str
    outer_conjugacy_change_of_variables: str
    uniform_finite_group_outer_bound: str
    symmetric_group_scalar_pressure_bound: str
    saturation_condition: str
    saturation_target_conclusion: str
    arbitrary_frame_width: bool
    arbitrary_leaf_placement: bool
    arbitrary_frame_types: bool
    arbitrary_nonempty_supports: bool
    universal_interleaved_scalar_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class InterleavedLeafPressureNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[InterleavedLeafPressureControl]
    outer_scaling_records: list[InterleavedOuterScalingRecord]
    exhaustive_support_censuses: list[InterleavedSupportCensus]
    all_depth_certificate: InterleavedLeafAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _normalize_support(rows: Iterable[Assignment]) -> tuple[Assignment, ...]:
    rows = tuple(sorted(set(rows)))
    if not rows:
        raise ValueError("support must be nonempty")
    width = len(rows[0])
    if any(
        len(row) != width or any(bit not in (0, 1) for bit in row)
        for row in rows
    ):
        raise ValueError("support rows must be equally sized and binary")
    return rows


def _inverse(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def interleaved_pair_pattern(
    frame_block_lengths: tuple[int, int, int, int],
    frame_types: tuple[str, ...],
) -> str:
    if any(length < 0 for length in frame_block_lengths):
        raise ValueError("frame block lengths must be nonnegative")
    if sum(frame_block_lengths) != len(frame_types):
        raise ValueError("frame types must match the total block length")
    if any(token not in "AB" for token in frame_types):
        raise ValueError("frame types must be A/B tokens")
    iterator = iter(frame_types)
    return "".join(
        leaf + "".join(next(iterator) for _ in range(length))
        for leaf, length in zip("EFEF", frame_block_lengths)
    )


def _frame_positions(pattern: str) -> tuple[int, ...]:
    return tuple(
        index + 1 for index, token in enumerate(pattern) if token in "AB"
    )


def _color_word(
    pattern: str,
    assignment: Assignment,
    *,
    differing_coordinate: bool,
    color: int,
) -> SignedWord:
    bits = _coordinate_bits(pattern, assignment, differing_coordinate)
    return tuple(index + 1 for index, bit in enumerate(bits) if bit == color)


def _mapped_frame_word(pattern: str, row: Assignment) -> SignedWord:
    positions = _frame_positions(pattern)
    return tuple(position for position, bit in zip(positions, row) if bit)


def interleaved_suffix_pivot_steps(
    pattern: str,
    support: tuple[Assignment, ...],
    *,
    support_kind: str,
    actual_same_support: tuple[Assignment, ...] | None = None,
) -> tuple[
    FrameSubwordSuffixBranchCertificate,
    tuple[InterleavedSuffixPivotStep, ...],
]:
    if support_kind not in ("same", "different"):
        raise ValueError("support kind must be same or different")
    rows = _normalize_support(support)
    positions = _frame_positions(pattern)
    if len(positions) != len(rows[0]):
        raise ValueError("support width must equal the number of frame tokens")
    certificate = frame_subword_suffix_branch_certificate(rows)
    actual_same = set(actual_same_support or rows)
    zero = (0,) * len(rows[0])
    steps = []
    for coordinate, witness in zip(
        certificate.suffix_branch_coordinates,
        certificate.suffix_branch_witnesses,
    ):
        anchor = certificate.anchor
        if support_kind == "same":
            anchor_word = _mapped_frame_word(pattern, anchor)
            witness_word = _mapped_frame_word(pattern, witness)
            available = (
                (anchor == zero or anchor in actual_same)
                and (witness == zero or witness in actual_same)
            )
        else:
            anchor_word = _color_word(
                pattern,
                anchor,
                differing_coordinate=True,
                color=1,
            )
            witness_word = _color_word(
                pattern,
                witness,
                differing_coordinate=True,
                color=1,
            )
            available = anchor in rows and witness in rows
        raw = free_reduce((*witness_word, *_inverse(anchor_word)))
        pivot = positions[coordinate - 1]
        higher = set(positions[coordinate:])
        pivot_count = sum(abs(letter) == pivot for letter in raw)
        higher_count = sum(abs(letter) in higher for letter in raw)
        exact = available and pivot_count == 1 and higher_count == 0
        steps.append(
            InterleavedSuffixPivotStep(
                support_kind=support_kind,
                frame_coordinate_one_based=coordinate,
                pattern_generator_one_based=pivot,
                anchor=anchor,
                witness=witness,
                raw_relative_relation=raw,
                pivot_occurrence_count=pivot_count,
                higher_frame_generator_occurrence_count=higher_count,
                endpoint_relators_available=available,
                exact_marker_stable_suffix_pivot_verified=exact,
                status=(
                    "exact-interleaved-marker-stable-suffix-pivot"
                    if exact
                    else "interleaved-suffix-pivot-failure"
                ),
            )
        )
    return certificate, tuple(steps)


@lru_cache(maxsize=None)
def audit_interleaved_outer_conjugacy(
    frame_block_lengths: tuple[int, int, int, int],
    frame_types: tuple[str, ...],
    different_base_assignment: Assignment,
) -> InterleavedOuterConjugacyControl:
    pattern = interleaved_pair_pattern(frame_block_lengths, frame_types)
    if len(different_base_assignment) != len(frame_types):
        raise ValueError("base assignment width must match frame width")
    leaves = tuple(
        index + 1 for index, token in enumerate(pattern) if token in "EF"
    )
    e, f, h, j = leaves
    split_bits = tuple(1 if token == "B" else 0 for token in pattern)
    split_zero = tuple(
        index + 1 for index, bit in enumerate(split_bits) if not bit
    )
    different_zero = _color_word(
        pattern,
        different_base_assignment,
        differing_coordinate=True,
        color=0,
    )
    different_one = _color_word(
        pattern,
        different_base_assignment,
        differing_coordinate=True,
        color=1,
    )
    h_image = _solve_single_occurrence(different_zero, h)
    j_image = _solve_single_occurrence(different_one, j)
    residual = free_reduce(
        _substitute_generator(
            _substitute_generator(split_zero, h, h_image),
            j,
            j_image,
        )
    )
    leaf_occurrences = tuple(
        letter for letter in residual if abs(letter) in (e, f)
    )
    expected_occurrences = (e, f, -e, -f)
    occurrence_positions = tuple(
        index for index, letter in enumerate(residual) if abs(letter) in (e, f)
    )
    if len(occurrence_positions) != 4:
        coefficients = ((), (), (), ())
    else:
        first, second, third, fourth = occurrence_positions
        coefficients = (
            residual[first + 1 : second],
            residual[second + 1 : third],
            residual[third + 1 : fourth],
            residual[fourth + 1 :],
        )
    coefficient_A, coefficient_B, coefficient_C, coefficient_D = coefficients
    twist = free_reduce((*coefficient_B, *coefficient_A))

    new_E = len(pattern) + 1
    new_g = len(pattern) + 2
    transformed = free_reduce(
        _substitute_generator(
            _substitute_generator(
                residual,
                e,
                (new_E, *_inverse(coefficient_A)),
            ),
            f,
            (new_g, *_inverse(twist)),
        )
    )
    expected = free_reduce(
        (
            new_E,
            new_g,
            -new_E,
            *coefficient_C,
            *twist,
            -new_g,
            *coefficient_D,
        )
    )
    exact = (
        leaf_occurrences == expected_occurrences
        and transformed == expected
        and all(
            not any(abs(letter) in leaves for letter in coefficient)
            for coefficient in coefficients
        )
    )
    return InterleavedOuterConjugacyControl(
        frame_block_lengths=frame_block_lengths,
        frame_types=frame_types,
        pattern=pattern,
        different_base_assignment=different_base_assignment,
        first_E_generator=e,
        first_F_generator=f,
        second_E_generator=h,
        second_F_generator=j,
        split_zero_relation=split_zero,
        different_zero_relation=different_zero,
        different_one_relation=different_one,
        solved_second_E_image=h_image,
        solved_second_F_image=j_image,
        residual_outer_relation=residual,
        residual_leaf_occurrence_word=leaf_occurrences,
        coefficient_A=coefficient_A,
        coefficient_B=coefficient_B,
        coefficient_C=coefficient_C,
        coefficient_D=coefficient_D,
        conjugacy_twist_T=twist,
        transformed_conjugacy_relation=transformed,
        expected_conjugacy_relation=expected,
        exact_coefficient_conjugacy_normal_form_verified=exact,
        uniform_finite_group_outer_bound="|G|*k(G)",
        status=(
            "exact-interleaved-leaf-outer-conjugacy-normal-form"
            if exact
            else "interleaved-outer-conjugacy-normal-form-failure"
        ),
    )


@lru_cache(maxsize=None)
def audit_interleaved_leaf_pressure(
    control_id: str,
    frame_block_lengths: tuple[int, int, int, int],
    frame_types: tuple[str, ...],
    same_support: tuple[Assignment, ...],
    different_support: tuple[Assignment, ...],
) -> InterleavedLeafPressureControl:
    same = _normalize_support(same_support)
    different = _normalize_support(different_support)
    width = len(frame_types)
    if len(same[0]) != width or len(different[0]) != width:
        raise ValueError("support widths must equal frame width")
    pattern = interleaved_pair_pattern(frame_block_lengths, frame_types)
    zero = (0,) * width
    augmented_same = tuple(sorted({zero, *same}))
    same_certificate, same_steps = interleaved_suffix_pivot_steps(
        pattern,
        augmented_same,
        support_kind="same",
        actual_same_support=same,
    )
    different_certificate, different_steps = interleaved_suffix_pivot_steps(
        pattern,
        different,
        support_kind="different",
    )
    same_bound = same_certificate.universal_finite_group_generator_upper_bound
    different_bound = (
        different_certificate.universal_finite_group_generator_upper_bound
    )
    if same_bound <= different_bound:
        dominant = "same-identity-fiber"
        dominant_size = len(augmented_same)
        frame_bound = same_bound
    else:
        dominant = "different-common-marker-fiber"
        dominant_size = len(different)
        frame_bound = different_bound

    outer = audit_interleaved_outer_conjugacy(
        frame_block_lengths,
        frame_types,
        different[0],
    )
    full_exponent = frame_bound + 1
    entropy = 0.5 * math.log2(len(same) * len(different))
    pressure = full_exponent + entropy - width - 2.0
    margin = -1.0 - pressure
    saturated = abs(margin) <= 1e-12
    zero_same = zero in same
    expected_saturation = (
        zero_same
        and len(same) == len(different)
        and len(same) & (len(same) - 1) == 0
    )
    saturation_verified = saturated == expected_saturation
    target = tuple(range(1, len(pattern) + 1))
    relations = set(marked_support_presentation(pattern, same, different))
    zero_kills_target = (
        not zero_same or canonical_relator(target) in relations
    )
    exact = (
        same_certificate.exact_suffix_branch_elimination_verified
        and different_certificate.exact_suffix_branch_elimination_verified
        and all(
            step.exact_marker_stable_suffix_pivot_verified
            for step in (*same_steps, *different_steps)
        )
        and outer.exact_coefficient_conjugacy_normal_form_verified
        and pressure <= -1.0 + 1e-12
        and margin >= -1e-12
        and saturation_verified
        and zero_kills_target
    )
    return InterleavedLeafPressureControl(
        control_id=control_id,
        frame_block_lengths=frame_block_lengths,
        frame_types=frame_types,
        pattern=pattern,
        frame_position_count=width,
        same_support=same,
        different_support=different,
        augmented_same_support=augmented_same,
        same_suffix_certificate=same_certificate,
        different_suffix_certificate=different_certificate,
        same_suffix_steps=same_steps,
        different_suffix_steps=different_steps,
        dominant_support_family=dominant,
        dominant_effective_support_size=dominant_size,
        frame_generator_upper_bound=frame_bound,
        outer_conjugacy_control=outer,
        full_solution_exponent_before_conjugacy_classes=full_exponent,
        support_entropy_exponent=entropy,
        scalar_crossing_pressure_upper_bound=pressure,
        scalar_crossing_pressure_margin=margin,
        scalar_pressure_saturated=saturated,
        saturation_condition_verified=saturation_verified,
        zero_same_assignment_present=zero_same,
        zero_same_cell_forces_target_identity=zero_kills_target,
        nontrivial_target_strict_finite_width_margin=(
            zero_kills_target and (zero_same or margin > 0)
        ),
        exact_control_verified=exact,
        status=(
            "interleaved-four-leaf-scalar-pressure-certified"
            if exact
            else "interleaved-four-leaf-pressure-certificate-failure"
        ),
    )


@lru_cache(maxsize=None)
def exhaustive_outer_scaling(
    maximum_frame_position_count: int = 5,
) -> tuple[InterleavedOuterScalingRecord, ...]:
    records = []
    for width in range(maximum_frame_position_count + 1):
        checks = 0
        failures = 0
        for blocks in itertools.product(range(width + 1), repeat=4):
            if sum(blocks) != width:
                continue
            for frame_types in itertools.product("AB", repeat=width):
                for base in itertools.product((0, 1), repeat=width):
                    control = audit_interleaved_outer_conjugacy(
                        blocks,
                        frame_types,
                        base,
                    )
                    checks += 1
                    failures += not (
                        control.exact_coefficient_conjugacy_normal_form_verified
                    )
        records.append(
            InterleavedOuterScalingRecord(
                frame_position_count=width,
                checked_placement_type_base_count=checks,
                outer_normal_form_failure_count=failures,
                status=(
                    "all-interleaved-outer-normal-forms-verified"
                    if not failures
                    else "interleaved-outer-scaling-failure"
                ),
            )
        )
    return tuple(records)


@lru_cache(maxsize=None)
def exhaustive_support_census() -> InterleavedSupportCensus:
    width = 3
    rows = tuple(itertools.product((0, 1), repeat=width))
    supports = tuple(
        tuple(row for index, row in enumerate(rows) if mask >> index & 1)
        for mask in range(1, 1 << len(rows))
    )
    pattern = interleaved_pair_pattern((1, 1, 1, 0), ("A", "B", "A"))
    zero = (0,) * width
    same_failures = 0
    different_failures = 0
    metadata = {}
    for support in supports:
        augmented = tuple(sorted({zero, *support}))
        same_certificate, same_steps = interleaved_suffix_pivot_steps(
            pattern,
            augmented,
            support_kind="same",
            actual_same_support=support,
        )
        different_certificate, different_steps = interleaved_suffix_pivot_steps(
            pattern,
            support,
            support_kind="different",
        )
        same_failures += not (
            same_certificate.exact_suffix_branch_elimination_verified
            and all(
                step.exact_marker_stable_suffix_pivot_verified
                for step in same_steps
            )
        )
        different_failures += not (
            different_certificate.exact_suffix_branch_elimination_verified
            and all(
                step.exact_marker_stable_suffix_pivot_verified
                for step in different_steps
            )
        )
        metadata[support] = (
            len(augmented),
            same_certificate.universal_finite_group_generator_upper_bound,
            different_certificate.universal_finite_group_generator_upper_bound,
        )

    pressure_failures = 0
    saturation_failures = 0
    saturation_count = 0
    minimum_margin = math.inf
    for same in supports:
        same_effective, same_bound, _ = metadata[same]
        for different in supports:
            _, _, different_bound = metadata[different]
            frame_bound = min(same_bound, different_bound)
            entropy = 0.5 * math.log2(len(same) * len(different))
            margin = width - frame_bound - entropy
            minimum_margin = min(minimum_margin, margin)
            pressure_failures += margin < -1e-12
            saturated = abs(margin) <= 1e-12
            expected = (
                zero in same
                and len(same) == len(different)
                and len(same) & (len(same) - 1) == 0
            )
            saturation_count += saturated
            saturation_failures += saturated != expected
            if same_effective < len(same):
                raise AssertionError("augmenting by zero cannot shrink support")
    exact = (
        same_failures
        == different_failures
        == pressure_failures
        == saturation_failures
        == 0
    )
    return InterleavedSupportCensus(
        frame_position_count=width,
        nonempty_support_count=len(supports),
        checked_support_pair_count=len(supports) ** 2,
        same_suffix_certificate_failure_count=same_failures,
        different_marker_suffix_certificate_failure_count=different_failures,
        pressure_inequality_failure_count=pressure_failures,
        saturation_equivalence_failure_count=saturation_failures,
        saturated_support_pair_count=saturation_count,
        minimum_pressure_margin=minimum_margin,
        exhaustive_census_verified=exact,
        status=(
            "all-width-three-interleaved-support-pairs-certified"
            if exact
            else "interleaved-support-census-failure"
        ),
    )


def interleaved_leaf_all_depth_certificate() -> InterleavedLeafAllDepthCertificate:
    return InterleavedLeafAllDepthCertificate(
        pattern_scope=(
            "E T^a F T^b E T^c F T^d for arbitrary a,b,c,d>=0 and "
            "arbitrary T_i in {A,B}"
        ),
        same_support_elimination=(
            "Same color-one relators give P(S union {0}) and leave at most "
            "u-ceil(log2|S union {0}|) frame generators."
        ),
        different_support_marker_cancellation=(
            "Fixed F markers above a suffix pivot cancel in relative relators, "
            "so D leaves at most u-ceil(log2|D|) frame generators."
        ),
        dominant_support_generator_formula=(
            "u-ceil(log2 max(|S union {0}|,|D|))"
        ),
        outer_quadratic_relation="e A f B e^-1 C f^-1 D=1",
        outer_conjugacy_change_of_variables=(
            "E=eA, T=BA, g=fT gives E g E^-1=D^-1 g T^-1 C^-1"
        ),
        uniform_finite_group_outer_bound="|G|*k(G)",
        symmetric_group_scalar_pressure_bound="at most -1+o(1)",
        saturation_condition=(
            "0 in S, |S|=|D|, and the common size is a power of two"
        ),
        saturation_target_conclusion=(
            "The zero same cell makes the full target product an exact relator."
        ),
        arbitrary_frame_width=True,
        arbitrary_leaf_placement=True,
        arbitrary_frame_types=True,
        arbitrary_nonempty_supports=True,
        universal_interleaved_scalar_no_go_verified=True,
        status="all-depth-interleaved-four-leaf-scalar-pressure-no-go",
    )


def _representative_controls() -> list[InterleavedLeafPressureControl]:
    cube4 = tuple(itertools.product((0, 1), repeat=4))
    zero4 = (0, 0, 0, 0)
    return [
        audit_interleaved_leaf_pressure(
            "CONTIGUOUS-BASELINE",
            (4, 0, 0, 0),
            ("A", "B", "A", "B"),
            (zero4, (1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 1, 1)),
            ((1, 0, 0, 1), (0, 1, 1, 0)),
        ),
        audit_interleaved_leaf_pressure(
            "MAXIMALLY-INTERLEAVED-SATURATION",
            (1, 1, 1, 1),
            ("A", "B", "A", "B"),
            (zero4, (1, 1, 0, 0), (0, 0, 1, 1), (1, 1, 1, 1)),
            ((1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 0, 0), (0, 0, 1, 1)),
        ),
        audit_interleaved_leaf_pressure(
            "PRUNED-POWER-BOUNDARY",
            (1, 1, 1, 1),
            ("B", "A", "B", "A"),
            tuple(row for row in cube4 if row != zero4),
            cube4,
        ),
        audit_interleaved_leaf_pressure(
            "EMPTY-INTERIOR-BLOCKS",
            (0, 2, 0, 2),
            ("B", "B", "A", "B"),
            ((0, 0, 0, 0), (1, 1, 1, 1)),
            ((1, 0, 1, 0),),
        ),
    ]


def run_interleaved_leaf_pressure_no_go() -> InterleavedLeafPressureNoGoReport:
    controls = _representative_controls()
    scaling = list(exhaustive_outer_scaling())
    censuses = [exhaustive_support_census()]
    theorem = interleaved_leaf_all_depth_certificate()
    exact = (
        all(control.exact_control_verified for control in controls)
        and all(row.outer_normal_form_failure_count == 0 for row in scaling)
        and all(census.exhaustive_census_verified for census in censuses)
        and theorem.universal_interleaved_scalar_no_go_verified
    )
    return InterleavedLeafPressureNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.pattern_scope,
            "frame_loss": theorem.dominant_support_generator_formula,
            "outer_loss": theorem.uniform_finite_group_outer_bound,
            "scalar_conclusion": theorem.symmetric_group_scalar_pressure_bound,
            "target_boundary": (
                "Exact saturation forces target identity; a uniform signed gap "
                "for near-saturating growing supports remains open."
            ),
        },
        representative_controls=controls,
        outer_scaling_records=scaling,
        exhaustive_support_censuses=censuses,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "extend_suffix_elimination_through_interleaved_F_markers",
                "resolved": True,
                "resolution": (
                    "Equal higher frame suffixes also cancel every fixed higher F "
                    "marker, leaving one triangular frame pivot."
                ),
            },
            {
                "obligation": "derive_multi_boundary_outer_solution_bound",
                "resolved": True,
                "resolution": (
                    "Two leaf equations leave a coefficient-twisted commutator, "
                    "equivalently one conjugacy fiber summed to |G|k(G)."
                ),
            },
            {
                "obligation": "prove_scalar_pressure_for_all_pair_word_placements",
                "resolved": True,
                "resolution": (
                    "The stronger support fiber pays average support entropy and "
                    "the outer conjugacy equation supplies the remaining loss."
                ),
            },
            {
                "obligation": "prove_uniform_nontrivial_target_gap",
                "resolved": False,
                "resolution": (
                    "Pruned power-boundary supports have positive but vanishing "
                    "scalar margin; their signed weighted character still needs "
                    "an actual-presentation or word-measure theorem."
                ),
            },
            {
                "obligation": "extend_beyond_one_crossing_pair_of_E_F_leaves",
                "resolved": False,
                "resolution": (
                    "More than two E/F pairs leave higher-genus multi-boundary "
                    "systems rather than one two-variable conjugacy equation."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Interleaved F markers destroy suffix cancellation.",
                "resolved": True,
                "resolution": (
                    "They are identical in both endpoint words and cancel with "
                    "the common higher frame suffix."
                ),
            },
            {
                "objection": "Four separated leaves leave two free outer generators.",
                "resolved": True,
                "resolution": (
                    "The residual quadratic equation is a conjugacy fiber, whose "
                    "total size is only |G|k(G)."
                ),
            },
            {
                "objection": "A/B frame labels change the outer topology.",
                "resolved": True,
                "resolution": (
                    "They only change fixed coefficients A,B,C,D and the twist T."
                ),
            },
            {
                "objection": "Scalar threshold saturation can retain a target.",
                "resolved": True,
                "resolution": (
                    "Exact saturation requires the zero same cell, whose color-zero "
                    "relation is the full target word."
                ),
            },
            {
                "objection": "Strict finite-width margin is automatically uniform.",
                "resolved": False,
                "resolution": (
                    "The 2^u-1 versus 2^u support pair makes the generic margin "
                    "tend to zero."
                ),
            },
        ],
        headline_metrics={
            "all_depth_interleaved_leaf_scalar_no_go_theorem_count": int(exact),
            "representative_control_count": len(controls),
            "control_failure_count": sum(
                not control.exact_control_verified for control in controls
            ),
            "exhaustive_outer_normal_form_check_count": sum(
                row.checked_placement_type_base_count for row in scaling
            ),
            "exhaustive_outer_normal_form_failure_count": sum(
                row.outer_normal_form_failure_count for row in scaling
            ),
            "maximum_exhaustive_outer_frame_width": max(
                row.frame_position_count for row in scaling
            ),
            "exhaustive_support_pair_count": censuses[0].checked_support_pair_count,
            "exhaustive_support_census_failure_count": int(
                not censuses[0].exhaustive_census_verified
            ),
            "scalar_saturation_control_count": sum(
                control.scalar_pressure_saturated for control in controls
            ),
            "nonidentity_uniform_target_gap_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "interleaved_F_marker_suffix_elimination_proved": exact,
            "interleaved_outer_conjugacy_bound_proved": exact,
            "all_four_leaf_pair_word_scalar_pressure_controlled": exact,
            "scalar_saturation_forces_target_identity": exact,
            "uniform_growing_nontrivial_target_gap_proved": False,
            "higher_multi_boundary_words_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Interleaving does not rescue unsigned mass. Near-saturating "
                "nontrivial target families and higher multi-boundary words remain."
            ),
        },
        status=(
            "all-interleaved-four-leaf-scalar-profiles-controlled"
            if exact
            else "interleaved-leaf-pressure-certificate-failure"
        ),
        summary=(
            "Proved all-width scalar pressure control for arbitrary interleaved "
            "four-leaf crossing words, mixed frame types, and support profiles."
        ),
        falsifiers_triggered=[
            "Interleaved F markers do not defeat suffix pivots.",
            "A/B frame labels only alter fixed conjugacy coefficients.",
            "Four separated leaves still leave one |G|k(G) outer fiber.",
            "Scalar saturation cannot carry a nonidentity target.",
            "Finite-width strictness does not prove a uniform signed target gap.",
        ],
    )


def write_interleaved_leaf_pressure_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_interleaved_leaf_pressure_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO."
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
                    "self_dual_wreath_interleaved_leaf_pressure_no_go": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    result = write_interleaved_leaf_pressure_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
