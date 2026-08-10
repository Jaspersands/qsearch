"""Exact no-go theorem for support-difference-peelable frame lifts.

Consider any valid marked pattern and designate some frame coordinates as
inserted variables.  If one support class contains a Hamming-cube edge in an
inserted direction, its two color-one relators have the form

    P Q = 1,                 P z_i Q = 1.

Their quotient is ``P z_i P^-1``, so the inserted generator ``z_i`` is the
identity in every target group.  If every inserted direction is covered by an
edge (the edge may use a different support class or base fiber each time), all
inserted generators disappear.  Deleting them projects every relation and the
full-product target exactly to the marked presentation on the projected
supports.

This elementary edge step bootstraps.  Once a set K of inserted generators is
known to be identity, a same-fiber support pair may differ on several inserted
coordinates provided exactly one difference remains outside K.  Substitution
reduces the pair to the same conjugated-singleton relation and kills the next
generator.  Iterating this support-difference peeling process is exact.

The argument needs neither a complete suffix cube, direct edges in every
direction, nor contiguous insertions.  It closes full cubes, sparse star
fibers, chained multi-coordinate differences, and interleaved lifts whenever
their peeling closure covers every inserted coordinate.  The remaining
high-upside search space consists of nonpeelable difference cores whose
coupled residual words may retain genuinely growing group and target laws.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    free_reduce,
    marked_support_presentation,
    normalize_relations,
)
from self_dual_wreath_target_survival_surface_seed import (
    target_survival_lift_supports,
    target_survival_power_boundary_supports,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_support_difference_peeling_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Assignment = tuple[int, ...]


@dataclass(frozen=True)
class SupportDifferencePeelingWitness:
    appended_frame_coordinate_one_based: int
    appended_pattern_generator: int
    support_kind: str
    projected_base_assignment: Assignment
    lower_assignment: Assignment
    upper_assignment: Assignment
    pair_difference_coordinates_one_based: tuple[int, ...]
    assumed_identity_coordinates_one_based: tuple[int, ...]
    residual_difference_coordinates_one_based: tuple[int, ...]
    direct_coordinate_edge: bool
    lower_color_one_relation: SignedWord
    upper_color_one_relation: SignedWord
    lower_relation_modulo_assumed_identities: SignedWord
    upper_relation_modulo_assumed_identities: SignedWord
    relation_quotient: SignedWord
    conjugating_prefix: SignedWord
    expected_conjugated_generator: SignedWord
    exact_conjugate_identity_verified: bool
    status: str


@dataclass(frozen=True)
class SupportDifferencePeelingControl:
    control_id: str
    lifted_pattern: str
    projected_pattern: str
    frame_coordinate_count: int
    appended_frame_coordinates_one_based: tuple[int, ...]
    appended_pattern_generators: tuple[int, ...]
    insertions_interleaved: bool
    lifted_same_support_size: int
    lifted_different_support_size: int
    projected_same_support: tuple[Assignment, ...]
    projected_different_support: tuple[Assignment, ...]
    support_difference_hyperedges_one_based: tuple[tuple[int, ...], ...]
    forcing_witnesses: tuple[SupportDifferencePeelingWitness, ...]
    direct_coordinate_edge_witness_count: int
    multi_difference_peeling_witness_count: int
    peeling_round_count: int
    uncovered_appended_coordinates_one_based: tuple[int, ...]
    residual_core_is_stopping_set: bool
    peeling_core_pattern: str
    peeling_core_same_support: tuple[Assignment, ...]
    peeling_core_different_support: tuple[Assignment, ...]
    peeled_coordinate_count: int
    peeling_core_inserted_coordinate_count: int
    peeling_core_frame_coordinate_count: int
    nonpeelable_core_support_size_upper_bound: int | None
    nonpeelable_core_half_cube_bound_verified: bool
    original_support_entropy_bits: float | None
    peeling_core_support_entropy_bits: float | None
    support_entropy_padding_slack: float | None
    scalar_pressure_cannot_increase_under_peeling: bool
    relations_modulo_forced_identities: tuple[SignedWord, ...]
    peeling_core_relations: tuple[SignedWord, ...]
    exact_peeling_core_relation_projection_verified: bool
    target_modulo_forced_identities: SignedWord
    peeling_core_target: SignedWord
    exact_peeling_core_target_projection_verified: bool
    exact_peeling_core_tietze_reduction_verified: bool
    every_appended_generator_forced_to_identity: bool
    collapsed_lifted_relations: tuple[SignedWord, ...]
    projected_relations: tuple[SignedWord, ...]
    exact_relation_projection_verified: bool
    collapsed_lifted_target: SignedWord
    projected_target: SignedWord
    exact_target_projection_verified: bool
    exact_marked_tietze_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class SupportDifferencePeelingNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[SupportDifferencePeelingControl]
    nonpeelable_boundary_controls: list[SupportDifferencePeelingControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _normalize_support(
    rows: Iterable[Assignment],
    width: int,
) -> tuple[Assignment, ...]:
    output = tuple(sorted(set(rows)))
    if any(
        len(row) != width or any(bit not in (0, 1) for bit in row)
        for row in output
    ):
        raise ValueError("support must contain binary rows of the frame width")
    return output


def _support_entropy_bits(
    same: tuple[Assignment, ...],
    different: tuple[Assignment, ...],
) -> float | None:
    if not same or not different:
        return None
    return 0.5 * math.log2(len(same)) + 0.5 * math.log2(len(different))


def _frame_token_positions(pattern: str) -> tuple[int, ...]:
    return tuple(index for index, token in enumerate(pattern) if token in "AB")


def _support_color_one_relation(
    pattern: str,
    assignment: Assignment,
    differing_coordinate: bool,
) -> SignedWord:
    frame_positions = _frame_token_positions(pattern)
    if len(assignment) != len(frame_positions):
        raise ValueError("assignment must specify every frame coordinate")
    iterator = iter(assignment)
    bits = tuple(
        next(iterator)
        if token in "AB"
        else (1 if token == "F" and differing_coordinate else 0)
        for token in pattern
    )
    return tuple(index + 1 for index, bit in enumerate(bits) if bit)


def _inverse(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _delete_coordinates(
    row: Assignment,
    deleted_zero_based: frozenset[int],
) -> Assignment:
    return tuple(
        bit for index, bit in enumerate(row) if index not in deleted_zero_based
    )


def _collapse_word(
    word: SignedWord,
    deleted_pattern_generators: tuple[int, ...],
) -> SignedWord:
    deleted = frozenset(deleted_pattern_generators)
    output = []
    for letter in word:
        generator = abs(letter)
        if generator in deleted:
            continue
        collapsed = generator - sum(
            deleted_generator < generator
            for deleted_generator in deleted_pattern_generators
        )
        output.append(collapsed if letter > 0 else -collapsed)
    return free_reduce(output)


def _substitute_identity_generators(
    word: SignedWord,
    identity_generators: frozenset[int],
) -> SignedWord:
    return free_reduce(
        letter for letter in word if abs(letter) not in identity_generators
    )


def _find_peeling_witness(
    pattern: str,
    appended_zero_based: tuple[int, ...],
    killed_zero_based: frozenset[int],
    same: tuple[Assignment, ...],
    different: tuple[Assignment, ...],
) -> SupportDifferencePeelingWitness | None:
    frame_positions = _frame_token_positions(pattern)
    appended_set = frozenset(appended_zero_based)
    deleted_base_coordinates = appended_set
    killed_pattern_generators = frozenset(
        frame_positions[coordinate] + 1 for coordinate in killed_zero_based
    )
    for support_kind, rows, differing_coordinate in (
        ("different", different, True),
        ("same", same, False),
    ):
        for first, second in itertools.combinations(rows, 2):
            projected_first = _delete_coordinates(first, deleted_base_coordinates)
            if projected_first != _delete_coordinates(
                second,
                deleted_base_coordinates,
            ):
                continue
            difference = tuple(
                coordinate
                for coordinate in appended_zero_based
                if first[coordinate] != second[coordinate]
            )
            residual = tuple(
                coordinate
                for coordinate in difference
                if coordinate not in killed_zero_based
            )
            if len(residual) != 1:
                continue
            pivot = residual[0]
            lower, upper = (
                (first, second) if first[pivot] == 0 else (second, first)
            )
            pattern_generator = frame_positions[pivot] + 1
            lower_relation = _support_color_one_relation(
                pattern,
                lower,
                differing_coordinate,
            )
            upper_relation = _support_color_one_relation(
                pattern,
                upper,
                differing_coordinate,
            )
            lower_modulo = _substitute_identity_generators(
                lower_relation,
                killed_pattern_generators,
            )
            upper_modulo = _substitute_identity_generators(
                upper_relation,
                killed_pattern_generators,
            )
            quotient = free_reduce((*upper_modulo, *_inverse(lower_modulo)))
            prefix = tuple(
                generator
                for generator in lower_modulo
                if generator < pattern_generator
            )
            expected = free_reduce(
                (*prefix, pattern_generator, *_inverse(prefix))
            )
            exact = quotient == expected
            return SupportDifferencePeelingWitness(
                appended_frame_coordinate_one_based=pivot + 1,
                appended_pattern_generator=pattern_generator,
                support_kind=support_kind,
                projected_base_assignment=projected_first,
                lower_assignment=lower,
                upper_assignment=upper,
                pair_difference_coordinates_one_based=tuple(
                    coordinate + 1 for coordinate in difference
                ),
                assumed_identity_coordinates_one_based=tuple(
                    coordinate + 1 for coordinate in sorted(killed_zero_based)
                ),
                residual_difference_coordinates_one_based=(pivot + 1,),
                direct_coordinate_edge=len(difference) == 1,
                lower_color_one_relation=lower_relation,
                upper_color_one_relation=upper_relation,
                lower_relation_modulo_assumed_identities=lower_modulo,
                upper_relation_modulo_assumed_identities=upper_modulo,
                relation_quotient=quotient,
                conjugating_prefix=prefix,
                expected_conjugated_generator=expected,
                exact_conjugate_identity_verified=exact,
                status=(
                    "exact-support-difference-peeling-relator"
                    if exact
                    else "support-difference-peeling-word-failure"
                ),
            )
    return None


def _support_difference_hyperedges(
    appended_zero_based: tuple[int, ...],
    same: tuple[Assignment, ...],
    different: tuple[Assignment, ...],
) -> tuple[tuple[int, ...], ...]:
    appended_set = frozenset(appended_zero_based)
    edges: set[tuple[int, ...]] = set()
    for rows in (same, different):
        for first, second in itertools.combinations(rows, 2):
            if _delete_coordinates(first, appended_set) != _delete_coordinates(
                second,
                appended_set,
            ):
                continue
            edge = tuple(
                coordinate + 1
                for coordinate in appended_zero_based
                if first[coordinate] != second[coordinate]
            )
            if edge:
                edges.add(edge)
    return tuple(sorted(edges, key=lambda edge: (len(edge), edge)))


def audit_support_difference_peeling_lift(
    control_id: str,
    lifted_pattern: str,
    appended_frame_coordinates_one_based: Iterable[int],
    lifted_same_support: Iterable[Assignment],
    lifted_different_support: Iterable[Assignment],
) -> SupportDifferencePeelingControl:
    """Audit the universal support-difference peeling reduction.

    Appended coordinates are indexed among the A/B frame tokens, not among all
    pattern positions.  They may occur anywhere in the pattern.
    """

    if any(token not in "EABF" for token in lifted_pattern):
        raise ValueError("pattern contains an unknown token")
    frame_positions = _frame_token_positions(lifted_pattern)
    frame_count = len(frame_positions)
    appended_one_based = tuple(sorted(set(appended_frame_coordinates_one_based)))
    if not appended_one_based:
        raise ValueError("at least one appended frame coordinate is required")
    if any(
        coordinate < 1 or coordinate > frame_count
        for coordinate in appended_one_based
    ):
        raise ValueError("appended frame coordinate is outside the pattern")
    appended_zero_based = tuple(coordinate - 1 for coordinate in appended_one_based)
    deleted_coordinates = frozenset(appended_zero_based)
    deleted_pattern_generators = tuple(
        frame_positions[coordinate] + 1 for coordinate in appended_zero_based
    )
    same = _normalize_support(lifted_same_support, frame_count)
    different = _normalize_support(lifted_different_support, frame_count)

    deleted_pattern_indices = {
        frame_positions[coordinate] for coordinate in appended_zero_based
    }
    projected_pattern = "".join(
        token
        for index, token in enumerate(lifted_pattern)
        if index not in deleted_pattern_indices
    )
    projected_same = tuple(
        sorted({_delete_coordinates(row, deleted_coordinates) for row in same})
    )
    projected_different = tuple(
        sorted({_delete_coordinates(row, deleted_coordinates) for row in different})
    )
    difference_hyperedges = _support_difference_hyperedges(
        appended_zero_based,
        same,
        different,
    )

    killed: set[int] = set()
    witness_list: list[SupportDifferencePeelingWitness] = []
    while len(killed) < len(appended_zero_based):
        witness = _find_peeling_witness(
            lifted_pattern,
            appended_zero_based,
            frozenset(killed),
            same,
            different,
        )
        if witness is None:
            break
        witness_list.append(witness)
        if not witness.exact_conjugate_identity_verified:
            break
        killed.add(witness.appended_frame_coordinate_one_based - 1)
    witnesses = tuple(witness_list)
    covered = {coordinate + 1 for coordinate in killed}
    uncovered = tuple(
        coordinate for coordinate in appended_one_based if coordinate not in covered
    )
    residual_core = frozenset(uncovered)
    stopping_set = all(
        len(residual_core.intersection(edge)) != 1
        for edge in difference_hyperedges
    )
    all_forced = not uncovered and all(
        witness.exact_conjugate_identity_verified for witness in witnesses
    )

    lifted_relations = marked_support_presentation(
        lifted_pattern,
        same,
        different,
    )
    killed_coordinates = frozenset(killed)
    killed_pattern_generators = tuple(
        frame_positions[coordinate] + 1 for coordinate in sorted(killed)
    )
    killed_pattern_indices = {
        frame_positions[coordinate] for coordinate in killed
    }
    peeling_core_pattern = "".join(
        token
        for index, token in enumerate(lifted_pattern)
        if index not in killed_pattern_indices
    )
    peeling_core_same = tuple(
        sorted({_delete_coordinates(row, killed_coordinates) for row in same})
    )
    peeling_core_different = tuple(
        sorted({_delete_coordinates(row, killed_coordinates) for row in different})
    )
    relations_modulo_forced = normalize_relations(
        _collapse_word(relation, killed_pattern_generators)
        for relation in lifted_relations
    )
    peeling_core_relations = marked_support_presentation(
        peeling_core_pattern,
        peeling_core_same,
        peeling_core_different,
    )
    core_relation_projection = relations_modulo_forced == peeling_core_relations

    collapsed_relations = normalize_relations(
        _collapse_word(relation, deleted_pattern_generators)
        for relation in lifted_relations
    )
    projected_relations = marked_support_presentation(
        projected_pattern,
        projected_same,
        projected_different,
    )
    relation_projection = collapsed_relations == projected_relations

    lifted_target = tuple(range(1, len(lifted_pattern) + 1))
    target_modulo_forced = _collapse_word(
        lifted_target,
        killed_pattern_generators,
    )
    peeling_core_target = tuple(range(1, len(peeling_core_pattern) + 1))
    core_target_projection = target_modulo_forced == peeling_core_target
    core_exact = (
        stopping_set
        and all(witness.exact_conjugate_identity_verified for witness in witnesses)
        and core_relation_projection
        and core_target_projection
    )
    peeled_count = len(killed)
    core_inserted_count = len(uncovered)
    core_frame_count = len(_frame_token_positions(peeling_core_pattern))
    core_support_bound = (
        1 << (core_frame_count - 1) if core_inserted_count else None
    )
    half_cube_bound = (
        core_support_bound is None
        or (
            len(peeling_core_same) <= core_support_bound
            and len(peeling_core_different) <= core_support_bound
        )
    )
    original_entropy = _support_entropy_bits(same, different)
    core_entropy = _support_entropy_bits(
        peeling_core_same,
        peeling_core_different,
    )
    entropy_slack = (
        None
        if original_entropy is None or core_entropy is None
        else core_entropy + peeled_count - original_entropy
    )
    pressure_nonincrease = core_exact and (
        entropy_slack is None or entropy_slack >= -1e-12
    )
    collapsed_target = _collapse_word(
        lifted_target,
        deleted_pattern_generators,
    )
    projected_target = tuple(range(1, len(projected_pattern) + 1))
    target_projection = collapsed_target == projected_target
    exact = all_forced and core_exact and relation_projection and target_projection
    trailing_coordinates = tuple(
        range(frame_count - len(appended_one_based) + 1, frame_count + 1)
    )
    return SupportDifferencePeelingControl(
        control_id=control_id,
        lifted_pattern=lifted_pattern,
        projected_pattern=projected_pattern,
        frame_coordinate_count=frame_count,
        appended_frame_coordinates_one_based=appended_one_based,
        appended_pattern_generators=deleted_pattern_generators,
        insertions_interleaved=appended_one_based != trailing_coordinates,
        lifted_same_support_size=len(same),
        lifted_different_support_size=len(different),
        projected_same_support=projected_same,
        projected_different_support=projected_different,
        support_difference_hyperedges_one_based=difference_hyperedges,
        forcing_witnesses=witnesses,
        direct_coordinate_edge_witness_count=sum(
            witness.direct_coordinate_edge for witness in witnesses
        ),
        multi_difference_peeling_witness_count=sum(
            not witness.direct_coordinate_edge for witness in witnesses
        ),
        peeling_round_count=len(witnesses),
        uncovered_appended_coordinates_one_based=uncovered,
        residual_core_is_stopping_set=stopping_set,
        peeling_core_pattern=peeling_core_pattern,
        peeling_core_same_support=peeling_core_same,
        peeling_core_different_support=peeling_core_different,
        peeled_coordinate_count=peeled_count,
        peeling_core_inserted_coordinate_count=core_inserted_count,
        peeling_core_frame_coordinate_count=core_frame_count,
        nonpeelable_core_support_size_upper_bound=core_support_bound,
        nonpeelable_core_half_cube_bound_verified=half_cube_bound,
        original_support_entropy_bits=original_entropy,
        peeling_core_support_entropy_bits=core_entropy,
        support_entropy_padding_slack=entropy_slack,
        scalar_pressure_cannot_increase_under_peeling=pressure_nonincrease,
        relations_modulo_forced_identities=relations_modulo_forced,
        peeling_core_relations=peeling_core_relations,
        exact_peeling_core_relation_projection_verified=core_relation_projection,
        target_modulo_forced_identities=target_modulo_forced,
        peeling_core_target=peeling_core_target,
        exact_peeling_core_target_projection_verified=core_target_projection,
        exact_peeling_core_tietze_reduction_verified=core_exact,
        every_appended_generator_forced_to_identity=all_forced,
        collapsed_lifted_relations=collapsed_relations,
        projected_relations=projected_relations,
        exact_relation_projection_verified=relation_projection,
        collapsed_lifted_target=collapsed_target,
        projected_target=projected_target,
        exact_target_projection_verified=target_projection,
        exact_marked_tietze_reduction_verified=exact,
        status=(
            "exact-support-difference-peeling-reduces-to-projection"
            if exact
            else (
                "exact-nonpeelable-support-difference-core-isolated"
                if core_exact
                else "support-difference-peeling-certificate-failure"
            )
        ),
    )


def audit_full_suffix_cube_lift(
    control_id: str,
    base_frame_types: tuple[str, ...],
    lift_depth: int,
    lifted_same_support: Iterable[Assignment],
    lifted_different_support: Iterable[Assignment],
    complete_fiber_base: Assignment,
) -> SupportDifferencePeelingControl:
    """Apply the peeling theorem to a full different suffix cube."""

    if not base_frame_types or any(token not in "AB" for token in base_frame_types):
        raise ValueError("base frame types must be a nonempty A/B tuple")
    if lift_depth < 1:
        raise ValueError("lift depth must be positive")
    if len(complete_fiber_base) != len(base_frame_types):
        raise ValueError("complete fiber base has the wrong width")
    different = tuple(lifted_different_support)
    suffixes = tuple(itertools.product((0, 1), repeat=lift_depth))
    expected_fiber = {(*complete_fiber_base, *suffix) for suffix in suffixes}
    if not expected_fiber.issubset(set(different)):
        raise ValueError("different support does not contain the complete suffix fiber")
    pattern = "E" + "".join(base_frame_types) + "A" * lift_depth + "FEF"
    first_appended = len(base_frame_types) + 1
    return audit_support_difference_peeling_lift(
        control_id,
        pattern,
        range(first_appended, first_appended + lift_depth),
        lifted_same_support,
        different,
    )


def _sparse_star_control(depth: int = 6) -> SupportDifferencePeelingControl:
    zero = (0,) * depth
    same = ((1, 0, 1, 0, *zero),)
    different = (
        (0, 0, 0, 0, *zero),
        *tuple(
            (0, 0, 0, 0, *tuple(int(index == coordinate) for index in range(depth)))
            for coordinate in range(depth)
        ),
    )
    return audit_support_difference_peeling_lift(
        "SPARSE-STAR-PARTIAL-SUFFIX-FIBER",
        "E" + "BABA" + "A" * depth + "FEF",
        range(5, 5 + depth),
        same,
        different,
    )


def _interleaved_control() -> SupportDifferencePeelingControl:
    pattern = "EBAABAAFEF"
    zero = (0, 0, 0, 0, 0, 0)
    same = (zero, (0, 1, 0, 0, 0, 0))
    different = (
        (1, 0, 0, 1, 0, 1),
        (1, 0, 0, 1, 1, 1),
    )
    return audit_support_difference_peeling_lift(
        "INTERLEAVED-SPLIT-SUPPORT-EDGE-COVER",
        pattern,
        (2, 5),
        same,
        different,
    )


def _chained_multi_difference_control() -> SupportDifferencePeelingControl:
    zero = (0, 0, 0)
    same = ((1, 0, 1, 0, *zero),)
    different = (
        (0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 1, 0, 0),
        (0, 0, 0, 1, 0, 0, 0),
        (0, 0, 0, 1, 1, 1, 0),
        (0, 0, 1, 0, 0, 0, 0),
        (0, 0, 1, 0, 0, 1, 1),
    )
    return audit_support_difference_peeling_lift(
        "CHAINED-MULTI-DIFFERENCE-FIBERS",
        "EBABAAAAFEF",
        (5, 6, 7),
        same,
        different,
    )


def _nonpeelable_boundary_control() -> SupportDifferencePeelingControl:
    return audit_support_difference_peeling_lift(
        "TWO-VARIABLE-NONPEELABLE-STOPPING-CORE",
        "EBAAFEF",
        (2, 3),
        ((0, 0, 0), (0, 1, 1)),
        (),
    )


def run_support_difference_peeling_no_go() -> SupportDifferencePeelingNoGoReport:
    controls = []
    full_cube_controls = []
    for depth in range(1, 7):
        _, same, different = target_survival_lift_supports(depth)
        full_cube_controls.append(
            audit_full_suffix_cube_lift(
                "ORIGINAL-IDENTITY-LIFT",
                tuple("BABA"),
                depth,
                same,
                different,
                (0, 0, 0, 0),
            )
        )
        _, same, different = target_survival_power_boundary_supports(depth)
        full_cube_controls.append(
            audit_full_suffix_cube_lift(
                "POWER-BOUNDARY-PRUNED-LIFT",
                tuple("BABA"),
                depth,
                same,
                different,
                (0, 0, 0, 0),
            )
        )
    controls.extend(full_cube_controls)

    suffixes = tuple(itertools.product((0, 1), repeat=3))
    generic_same = tuple(
        (*base, *suffix)
        for base in ((0, 1, 0), (1, 0, 1))
        for suffix in suffixes
        if suffix != (1, 1, 1) or base == (1, 0, 1)
    )
    generic_different = tuple(
        (*base, *suffix)
        for base in ((0, 0, 1), (1, 1, 0))
        for suffix in suffixes
    )
    controls.append(
        audit_full_suffix_cube_lift(
            "GENERIC-MIXED-BASE-CONTROL",
            tuple("ABB"),
            3,
            generic_same,
            generic_different,
            (0, 0, 1),
        )
    )
    sparse = _sparse_star_control()
    interleaved = _interleaved_control()
    chained = _chained_multi_difference_control()
    controls.extend((sparse, interleaved, chained))
    boundary = _nonpeelable_boundary_control()

    exact = all(row.exact_marked_tietze_reduction_verified for row in controls)
    return SupportDifferencePeelingNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "coordinate_edge_lemma": (
                "For an edge x,x+e_i in either support class, the two color-one "
                "relators are PQ and Pz_iQ; their quotient is Pz_iP^-1."
            ),
            "peeling_induction": (
                "After generators in K are identity, a same-fiber pair whose "
                "inserted-coordinate difference has one element outside K "
                "reduces to a conjugate of that remaining generator."
            ),
            "peeling_closure_reduction": (
                "If iterated support-difference peeling reaches every designated "
                "coordinate, every inserted generator is identity in every group."
            ),
            "stopping_set_boundary": (
                "At the peeling fixed point, the uncovered coordinate set meets "
                "every same-fiber difference hyperedge in zero or at least two "
                "positions. Conversely, any singleton intersection is a valid "
                "next peeling step."
            ),
            "canonical_core_projection": (
                "Deleting all generators proved identity by peeling maps every "
                "relation and the target exactly to the projected support instance "
                "on the residual stopping core, even when that core is nonempty."
            ),
            "pressure_monotonicity": (
                "If k coordinates peel, each projected support row has at most "
                "2^k preimages. Hence H(original)<=H(core)+k, while the pattern "
                "is longer by k and the group/target law is unchanged. Scalar "
                "pressure cannot increase under peeling padding."
            ),
            "stopping_core_codensity": (
                "Within every projected base fiber, either support projects to an "
                "independent set of the residual Boolean cube. A nonempty c-bit "
                "core therefore has at most 2^(b+c-1) rows per support: at least "
                "one full codensity bit is unavoidable."
            ),
            "marked_projection": (
                "Deleting the forced generators maps all split/support relators "
                "and the full-product target exactly to the projected instance."
            ),
            "full_cube_corollary": (
                "A complete suffix cube contains the zero-to-e_i edges, but "
                "exponentially many rows are unnecessary; a k-edge star suffices."
            ),
            "scope": (
                "Inserted positions may be contiguous or interleaved, and each "
                "peeling witness may use a different support class/base fiber. "
                "Nonpeelable difference cores remain open."
            ),
        },
        representative_controls=controls,
        nonpeelable_boundary_controls=[boundary],
        proof_obligations=[
            {
                "obligation": "prove_support_difference_peeling_lift_trivialization",
                "resolved": exact,
                "resolution": (
                    "Inductive identity substitution turns each peeling pair into "
                    "an exact conjugated singleton; projection then recovers the "
                    "marked presentation and target."
                ),
            },
            {
                "obligation": "remove_complete_cube_direct_edge_and_contiguity_assumptions",
                "resolved": sparse.exact_marked_tietze_reduction_verified
                and interleaved.exact_marked_tietze_reduction_verified
                and chained.exact_marked_tietze_reduction_verified
                and chained.multi_difference_peeling_witness_count == 2,
                "resolution": (
                    "Sparse, interleaved, and chained controls show that full "
                    "cubes, direct edges in every direction, and suffix placement "
                    "are all unnecessary."
                ),
            },
            {
                "obligation": "classify_nonpeelable_support_difference_cores",
                "resolved": False,
                "resolution": (
                    "After peeling closure stalls, every same-fiber pair differs "
                    "in zero or at least two core variables. Their residual group "
                    "rank, word-map pressure, and target survival remain open."
                ),
            },
            {
                "obligation": "characterize_the_exact_peeling_stopping_boundary",
                "resolved": boundary.residual_core_is_stopping_set
                and boundary.uncovered_appended_coordinates_one_based == (2, 3),
                "resolution": (
                    "The residual core is exactly a stopping set of the pair-"
                    "difference hypergraph; the stored two-variable boundary has "
                    "one size-two hyperedge and no legal singleton peel."
                ),
            },
            {
                "obligation": "prove_canonical_projection_to_nonpeelable_core",
                "resolved": all(
                    row.exact_peeling_core_tietze_reduction_verified
                    for row in (*controls, boundary)
                ),
                "resolution": (
                    "Sequential witness substitutions followed by exact relation/"
                    "target projection produce the stopping-core instance."
                ),
            },
            {
                "obligation": "prove_peeling_padding_cannot_improve_scalar_pressure",
                "resolved": all(
                    row.scalar_pressure_cannot_increase_under_peeling
                    and row.nonpeelable_core_half_cube_bound_verified
                    for row in (*controls, boundary)
                ),
                "resolution": (
                    "The support-fiber multiplicity bound pays exactly for every "
                    "deleted pattern coordinate; stopping-core fibers are Boolean-"
                    "cube independent sets."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Exponential support growth creates new rank.",
                "resolved": True,
                "resolution": (
                    "False whenever difference peeling covers the new variables; "
                    "only k+1 rows in a star already kill k inserted generators."
                ),
            },
            {
                "objection": "Every killed direction needs a literal cube edge.",
                "resolved": True,
                "resolution": (
                    "False: the chained control kills its last two directions from "
                    "two-coordinate differences after earlier identities are used."
                ),
            },
            {
                "objection": "Interleaving prevents the two-relator quotient.",
                "resolved": True,
                "resolution": (
                    "False: common suffix factors cancel before the conjugating "
                    "prefix, independently of the inserted token's position."
                ),
            },
            {
                "objection": "The group collapses but the target retains inserts.",
                "resolved": True,
                "resolution": (
                    "False: the full-product word deletes the same identity "
                    "generators and becomes the projected target exactly."
                ),
            },
        ],
        headline_metrics={
            "all_pattern_support_difference_peeling_no_go_theorem_count": int(exact),
            "full_suffix_cube_corollary_control_count": len(full_cube_controls) + 1,
            "sparse_partial_suffix_peeling_control_count": int(
                sparse.exact_marked_tietze_reduction_verified
            ),
            "interleaved_peeling_control_count": int(
                interleaved.exact_marked_tietze_reduction_verified
            ),
            "chained_multi_difference_control_count": int(
                chained.exact_marked_tietze_reduction_verified
            ),
            "chained_multi_difference_witness_count": (
                chained.multi_difference_peeling_witness_count
            ),
            "stored_nonpeelable_boundary_control_count": 1,
            "stored_nonpeelable_boundary_core_size": len(
                boundary.uncovered_appended_coordinates_one_based
            ),
            "stopping_set_boundary_theorem_count": int(
                all(
                    row.residual_core_is_stopping_set
                    for row in (*controls, boundary)
                )
            ),
            "canonical_peeling_core_projection_theorem_count": int(
                all(
                    row.exact_peeling_core_tietze_reduction_verified
                    for row in (*controls, boundary)
                )
            ),
            "peeling_scalar_pressure_monotonicity_theorem_count": int(
                all(
                    row.scalar_pressure_cannot_increase_under_peeling
                    for row in (*controls, boundary)
                )
            ),
            "nonpeelable_core_half_cube_bound_theorem_count": int(
                all(
                    row.nonpeelable_core_half_cube_bound_verified
                    for row in (*controls, boundary)
                )
            ),
            "stored_lift_control_count": len(controls),
            "lift_control_failure_count": sum(
                not row.exact_marked_tietze_reduction_verified for row in controls
            ),
            "maximum_stored_inserted_frame_count": max(
                len(row.appended_frame_coordinates_one_based) for row in controls
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "support_difference_peelable_lifts_reduce_to_projection": exact,
            "coordinate_edge_covered_lifts_reduce_to_projection": exact,
            "full_suffix_cube_lifts_reduce_to_projection": exact,
            "partial_suffix_peelable_lifts_controlled": (
                sparse.exact_marked_tietze_reduction_verified
            ),
            "interleaved_peelable_lifts_controlled": (
                interleaved.exact_marked_tietze_reduction_verified
            ),
            "multi_difference_peeling_controlled": (
                chained.exact_marked_tietze_reduction_verified
            ),
            "all_partial_suffix_lifts_controlled": False,
            "all_interleaved_lifts_controlled": False,
            "nonpeelable_difference_core_lifts_controlled": False,
            "nonpeelable_core_exactly_identified_as_stopping_set": (
                boundary.residual_core_is_stopping_set
            ),
            "arbitrary_lift_reduces_to_canonical_peeling_core": all(
                row.exact_peeling_core_tietze_reduction_verified
                for row in (*controls, boundary)
            ),
            "peeling_padding_can_improve_scalar_pressure": False,
            "nonempty_stopping_core_requires_one_codensity_bit": all(
                row.nonpeelable_core_half_cube_bound_verified
                for row in (*controls, boundary)
            ),
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every support-difference-peelable lift is marked Tietze padding "
                "of its projection. Only nonpeelable coupled cores remain."
            ),
        },
        status=(
            "support-difference-peelable-frame-lifts-trivialized"
            if exact
            else "support-difference-peeling-certificate-failure"
        ),
        summary=(
            "Proved that iterative support-difference peeling, not a complete "
            "cube, direct edge cover, or contiguous suffix, exactly trivializes "
            "every inserted frame in its closure."
        ),
        falsifiers_triggered=[
            "Full suffix cubes create no new marked presentation or target law.",
            "Sparse star fibers already kill every inserted direction.",
            "Multi-coordinate differences can continue the identity cascade.",
            "Interleaving alone does not evade support-difference peeling.",
            "A viable lift must retain a nonempty nonpeelable difference core.",
        ],
    )


def write_support_difference_peeling_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    report = asdict(run_support_difference_peeling_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

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
                id="NEG-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO."
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
                    "self_dual_wreath_support_difference_peeling_no_go": str(path)
                },
            )
        )
    return report


if __name__ == "__main__":
    result = write_support_difference_peeling_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
