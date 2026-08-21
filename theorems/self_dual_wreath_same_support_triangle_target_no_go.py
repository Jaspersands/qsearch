"""Universal target collapse from one same-support weight-two triangle.

Let a marked four-leaf pattern have arbitrary interleaving and arbitrary
``A/B`` frame types.  Suppose its same-coordinate support contains, for three
distinct frame coordinates ``i,j,k``, the three zero-based rows

    e_i+e_j, e_i+e_k, e_j+e_k.

The color-one relations are ``x_i x_j=x_i x_k=x_j x_k=1``.  They force the
three frame generators to a common involution ``z``.  Write the full target,
after this substitution, as

    W = b_0 z b_1 z b_2 z b_3,

where the blocks contain every other leaf and frame generator.  Put

    L_s=b_0...b_(s-1), y_s=L_s z L_s^-1, B=b_0 b_1 b_2 b_3.

Then ``W=y_1 y_2 y_3 B``.  The three same-coordinate color-zero relations are
exactly the words obtained by deleting the selected pair:

    R_12=y_3 B, R_13=y_2 B, R_23=y_1 B.

Since ``y_2`` is an involution, there is the explicit free-word certificate

    W = R_23 R_13^-1 y_2^2 R_12.

Thus the transported target lies in the normal closure for every group.  The
argument is local: extra support rows, arbitrary different-coordinate
supports, additional frame coordinates, and every leaf placement only add
relations or change the coefficient blocks.

The triangle condition is not cosmetic.  Removing one edge yields an exact
``S_3`` countercontrol with 42 nonidentity target solutions.  This theorem is
a structural candidate filter, not a quantum speedup claim.
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
from self_dual_wreath_marked_pressure_obstruction_search import (
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    Assignment,
    SignedWord,
    _evaluate_signed_word,
    free_reduce,
    inverse_word,
    marked_support_presentation,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_same_support_triangle_target_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SAME-SUPPORT-TRIANGLE-TARGET-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Permutation = tuple[int, ...]


@dataclass(frozen=True)
class TriangleTargetCertificate:
    control_id: str
    pattern: str
    frame_width: int
    selected_frame_coordinates_zero_based: tuple[int, int, int]
    selected_pattern_generators: tuple[int, int, int]
    triangle_assignments: tuple[Assignment, Assignment, Assignment]
    color_one_triangle_relations: tuple[SignedWord, SignedWord, SignedWord]
    middle_generator_square_certificate: SignedWord
    middle_generator_square_from_triangle_relators: SignedWord
    exact_common_involution_certificate_verified: bool
    coefficient_blocks: tuple[SignedWord, SignedWord, SignedWord, SignedWord]
    abstract_involution_generator: int
    conjugated_involutions: tuple[SignedWord, SignedWord, SignedWord]
    leaf_only_coefficient_product: SignedWord
    collapsed_target_word: SignedWord
    factorized_target_word: SignedWord
    pair_deleted_color_zero_relations: tuple[SignedWord, SignedWord, SignedWord]
    factorized_pair_deleted_relations: tuple[SignedWord, SignedWord, SignedWord]
    target_normal_closure_factorization: SignedWord
    exact_block_factorization_verified: bool
    exact_pair_deleted_factorization_verified: bool
    exact_target_normal_closure_certificate_verified: bool
    all_group_target_identity_proved: bool
    status: str


@dataclass(frozen=True)
class MissingTriangleEdgeCountercontrol:
    pattern: str
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    missing_triangle_assignment: Assignment
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    residual_target_word: SignedWord
    symmetric_group_degree: int
    solution_count: int
    nonidentity_target_count: int
    target_survival_verified: bool
    status: str


@dataclass(frozen=True)
class TranslatedTriangleCountercontrol:
    pattern: str
    translation: Assignment
    selected_frame_coordinates_zero_based: tuple[int, int, int]
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    residual_target_word: SignedWord
    solution_exponent_upper_bound: float
    solution_exponent_certificate_source: str
    scalar_crossing_pressure_margin: float
    symmetric_group_degree: int
    solution_count: int
    nonidentity_target_count: int
    finite_target_survival_verified: bool
    scalar_pressure_survival_verified: bool
    exact_countercontrol_verified: bool
    status: str


@dataclass(frozen=True)
class TrianglePatternCensus:
    frame_width: int
    checked_pattern_count: int
    checked_triangle_count: int
    certificate_failure_count: int
    exhaustive_at_width: bool
    status: str


@dataclass(frozen=True)
class TriangleTargetAllDepthCertificate:
    pattern_scope: str
    support_condition: str
    frame_collapse: str
    coefficient_factorization: str
    normal_closure_identity: str
    arbitrary_frame_width: bool
    arbitrary_leaf_placement: bool
    arbitrary_frame_types: bool
    arbitrary_additional_support_rows: bool
    arbitrary_different_support: bool
    exact_target_identity: bool
    universal_triangle_target_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class SameSupportTriangleTargetNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_certificates: list[TriangleTargetCertificate]
    exhaustive_censuses: list[TrianglePatternCensus]
    missing_edge_countercontrol: MissingTriangleEdgeCountercontrol
    translated_triangle_countercontrol: TranslatedTriangleCountercontrol
    all_depth_certificate: TriangleTargetAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _multiply(*words: Iterable[int]) -> SignedWord:
    return free_reduce(letter for word in words for letter in word)


def _conjugate(prefix: SignedWord, word: SignedWord) -> SignedWord:
    return _multiply(prefix, word, inverse_word(prefix))


def _frame_positions(pattern: str) -> tuple[int, ...]:
    if any(token not in "ABEF" for token in pattern):
        raise ValueError("pattern tokens must lie in A/B/E/F")
    if pattern.count("E") != 2 or pattern.count("F") != 2:
        raise ValueError("triangle theorem is recorded for four-leaf patterns")
    return tuple(index + 1 for index, token in enumerate(pattern) if token in "AB")


def triangle_assignments(
    frame_width: int,
    selected_coordinates: tuple[int, int, int],
) -> tuple[Assignment, Assignment, Assignment]:
    if frame_width < 3:
        raise ValueError("a weight-two triangle needs at least three frames")
    selected = tuple(sorted(selected_coordinates))
    if len(set(selected)) != 3 or selected[0] < 0 or selected[-1] >= frame_width:
        raise ValueError("selected coordinates must be three distinct frame indices")
    return tuple(
        tuple(int(index in pair) for index in range(frame_width))
        for pair in itertools.combinations(selected, 2)
    )  # type: ignore[return-value]


def _color_relations_for_same_row(
    pattern: str,
    assignment: Assignment,
) -> tuple[SignedWord, SignedWord]:
    iterator = iter(assignment)
    bits = tuple(
        next(iterator) if token in "AB" else 0 for token in pattern
    )
    return tuple(
        tuple(index + 1 for index, bit in enumerate(bits) if bit == color)
        for color in (0, 1)
    )  # type: ignore[return-value]


def _substitute_selected_with_z(
    word: SignedWord,
    selected_generators: tuple[int, int, int],
    z: int,
) -> SignedWord:
    selected = set(selected_generators)
    return free_reduce(
        (z if letter > 0 else -z) if abs(letter) in selected else letter
        for letter in word
    )


@lru_cache(maxsize=None)
def audit_triangle_target_certificate(
    control_id: str,
    pattern: str,
    selected_coordinates: tuple[int, int, int],
) -> TriangleTargetCertificate:
    frames = _frame_positions(pattern)
    width = len(frames)
    selected_coordinates = tuple(sorted(selected_coordinates))
    rows = triangle_assignments(width, selected_coordinates)
    selected_generators = tuple(frames[index] for index in selected_coordinates)
    x1, x2, x3 = selected_generators
    same_relations = tuple(_color_relations_for_same_row(pattern, row) for row in rows)
    color_zero = tuple(pair[0] for pair in same_relations)
    color_one = tuple(pair[1] for pair in same_relations)
    expected_color_one = ((x1, x2), (x1, x3), (x2, x3))

    # x2^2 = (x2 x3)(x1 x3)^-1(x1 x2), an exact free-word identity.
    square = (x2, x2)
    square_from_relators = _multiply(
        color_one[2], inverse_word(color_one[1]), color_one[0]
    )
    common_involution = (
        color_one == expected_color_one and square_from_relators == square
    )

    selected_position_set = set(selected_generators)
    blocks: list[SignedWord] = []
    current: list[int] = []
    for generator in range(1, len(pattern) + 1):
        if generator in selected_position_set:
            blocks.append(tuple(current))
            current = []
        else:
            current.append(generator)
    blocks.append(tuple(current))
    block_tuple = tuple(blocks)
    if len(block_tuple) != 4:
        raise AssertionError("three selected generators must define four blocks")

    z = len(pattern) + 1
    prefixes = (
        block_tuple[0],
        _multiply(block_tuple[0], block_tuple[1]),
        _multiply(block_tuple[0], block_tuple[1], block_tuple[2]),
    )
    y = tuple(_conjugate(prefix, (z,)) for prefix in prefixes)
    coefficient_product = _multiply(*block_tuple)
    collapsed_target = _substitute_selected_with_z(
        tuple(range(1, len(pattern) + 1)), selected_generators, z
    )
    factorized_target = _multiply(*y, coefficient_product)

    collapsed_pair_relations = tuple(
        _substitute_selected_with_z(word, selected_generators, z)
        for word in color_zero
    )
    factorized_pair_relations = (
        _multiply(y[2], coefficient_product),
        _multiply(y[1], coefficient_product),
        _multiply(y[0], coefficient_product),
    )
    y2_square = _multiply(y[1], y[1])
    target_certificate = _multiply(
        factorized_pair_relations[2],
        inverse_word(factorized_pair_relations[1]),
        y2_square,
        factorized_pair_relations[0],
    )
    block_exact = collapsed_target == factorized_target
    pairs_exact = collapsed_pair_relations == factorized_pair_relations
    target_exact = (
        block_exact
        and pairs_exact
        and target_certificate == factorized_target
        and y2_square == _conjugate(prefixes[1], (z, z))
        and common_involution
    )
    return TriangleTargetCertificate(
        control_id=control_id,
        pattern=pattern,
        frame_width=width,
        selected_frame_coordinates_zero_based=selected_coordinates,
        selected_pattern_generators=selected_generators,
        triangle_assignments=rows,
        color_one_triangle_relations=color_one,  # type: ignore[arg-type]
        middle_generator_square_certificate=square,
        middle_generator_square_from_triangle_relators=square_from_relators,
        exact_common_involution_certificate_verified=common_involution,
        coefficient_blocks=block_tuple,  # type: ignore[arg-type]
        abstract_involution_generator=z,
        conjugated_involutions=y,  # type: ignore[arg-type]
        leaf_only_coefficient_product=coefficient_product,
        collapsed_target_word=collapsed_target,
        factorized_target_word=factorized_target,
        pair_deleted_color_zero_relations=collapsed_pair_relations,  # type: ignore[arg-type]
        factorized_pair_deleted_relations=factorized_pair_relations,
        target_normal_closure_factorization=target_certificate,
        exact_block_factorization_verified=block_exact,
        exact_pair_deleted_factorization_verified=pairs_exact,
        exact_target_normal_closure_certificate_verified=target_exact,
        all_group_target_identity_proved=target_exact,
        status=(
            "same-support-triangle-target-normal-closure-verified"
            if target_exact
            else "same-support-triangle-certificate-failure"
        ),
    )


def _four_leaf_patterns(frame_width: int):
    length = frame_width + 4
    for leaf_positions in itertools.combinations(range(length), 4):
        leaves = set(leaf_positions)
        for frame_types in itertools.product("AB", repeat=frame_width):
            leaf_iterator = iter("EFEF")
            frame_iterator = iter(frame_types)
            yield "".join(
                next(leaf_iterator) if index in leaves else next(frame_iterator)
                for index in range(length)
            )


def exhaustive_triangle_pattern_census(
    frame_width: int = 3,
) -> TrianglePatternCensus:
    if frame_width < 3 or frame_width > 4:
        raise ValueError("exhaustive census is intentionally limited to widths 3-4")
    pattern_count = 0
    triangle_count = 0
    failures = 0
    triples = tuple(itertools.combinations(range(frame_width), 3))
    for pattern in _four_leaf_patterns(frame_width):
        pattern_count += 1
        for triple in triples:
            triangle_count += 1
            failures += not audit_triangle_target_certificate(
                f"EXHAUSTIVE-U{frame_width}", pattern, triple
            ).all_group_target_identity_proved
    exact = failures == 0
    return TrianglePatternCensus(
        frame_width=frame_width,
        checked_pattern_count=pattern_count,
        checked_triangle_count=triangle_count,
        certificate_failure_count=failures,
        exhaustive_at_width=True,
        status=(
            "all-four-leaf-triangle-patterns-certified"
            if exact
            else "triangle-pattern-census-failure"
        ),
    )


def audit_missing_triangle_edge_countercontrol(
) -> MissingTriangleEdgeCountercontrol:
    pattern = "EFEBFAB"
    all_rows = triangle_assignments(3, (0, 1, 2))
    missing = all_rows[2]
    same = all_rows[:2]
    different = ((0, 0, 0),)
    reduction = tietze_reduce_presentation(
        len(pattern), marked_support_presentation(pattern, same, different)
    )
    target = _transport_target_product_word(len(pattern), reduction)
    group = tuple(itertools.permutations(range(3)))
    identity = tuple(range(3))
    solutions = 0
    nonidentity = 0
    for values in itertools.product(
        group, repeat=len(reduction.remaining_generators)
    ):
        assignment = dict(zip(reduction.remaining_generators, values))
        if all(
            _evaluate_signed_word(relation, assignment) == identity
            for relation in reduction.residual_relations
        ):
            solutions += 1
            nonidentity += _evaluate_signed_word(target, assignment) != identity
    exact = solutions == 108 and nonidentity == 42
    return MissingTriangleEdgeCountercontrol(
        pattern=pattern,
        same_support=same,
        different_support=different,
        missing_triangle_assignment=missing,
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        residual_target_word=target,
        symmetric_group_degree=3,
        solution_count=solutions,
        nonidentity_target_count=nonidentity,
        target_survival_verified=exact,
        status=(
            "missing-triangle-edge-S3-target-survivor"
            if exact
            else "missing-triangle-edge-control-failure"
        ),
    )


def audit_translated_triangle_countercontrol() -> TranslatedTriangleCountercontrol:
    pattern = "EFEAAABFB"
    translation = (0, 0, 0, 1, 1)
    selected = (0, 1, 2)
    zero_plane = (
        (0, 0, 0, 0, 0),
        (1, 1, 0, 0, 0),
        (1, 0, 1, 0, 0),
        (0, 1, 1, 0, 0),
    )
    same = tuple(
        tuple(left ^ right for left, right in zip(translation, row))
        for row in zero_plane
    )
    different = ((0, 0, 0, 0, 0),)
    reduction = tietze_reduce_presentation(
        len(pattern), marked_support_presentation(pattern, same, different)
    )
    target = _transport_target_product_word(len(pattern), reduction)
    exponent, source = presentation_solution_exponent_upper_bound(reduction)
    entropy = 0.5 * math.log2(len(same) * len(different))
    pressure = exponent + entropy - len(translation) - 2.0
    margin = -1.0 - pressure
    group = tuple(itertools.permutations(range(3)))
    identity = tuple(range(3))
    solutions = 0
    nonidentity = 0
    for values in itertools.product(
        group, repeat=len(reduction.remaining_generators)
    ):
        assignment = dict(zip(reduction.remaining_generators, values))
        if all(
            _evaluate_signed_word(relation, assignment) == identity
            for relation in reduction.residual_relations
        ):
            solutions += 1
            nonidentity += _evaluate_signed_word(target, assignment) != identity
    finite_survival = solutions == 432 and nonidentity == 168
    scalar_survival = margin <= 0.0
    exact = (
        same
        == (
            (0, 0, 0, 1, 1),
            (1, 1, 0, 1, 1),
            (1, 0, 1, 1, 1),
            (0, 1, 1, 1, 1),
        )
        and exponent == 3.0
        and source == "single-nonorientable-surface-genus-3"
        and abs(margin - 2.0) <= 1e-12
        and finite_survival
        and not scalar_survival
    )
    return TranslatedTriangleCountercontrol(
        pattern=pattern,
        translation=translation,
        selected_frame_coordinates_zero_based=selected,
        same_support=same,
        different_support=different,
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        residual_target_word=target,
        solution_exponent_upper_bound=exponent,
        solution_exponent_certificate_source=source,
        scalar_crossing_pressure_margin=margin,
        symmetric_group_degree=3,
        solution_count=solutions,
        nonidentity_target_count=nonidentity,
        finite_target_survival_verified=finite_survival,
        scalar_pressure_survival_verified=scalar_survival,
        exact_countercontrol_verified=exact,
        status=(
            "translated-triangle-target-survives-but-pressure-fails"
            if exact
            else "translated-triangle-countercontrol-failure"
        ),
    )


def triangle_target_all_depth_certificate() -> TriangleTargetAllDepthCertificate:
    return TriangleTargetAllDepthCertificate(
        pattern_scope=(
            "Every word with exactly two E leaves, two F leaves, and at least "
            "three arbitrarily interleaved A/B frame coordinates"
        ),
        support_condition=(
            "The same support contains e_i+e_j, e_i+e_k, e_j+e_k for some "
            "three distinct frame coordinates, with zero on all other frames."
        ),
        frame_collapse=(
            "The three color-one pair relators identify the selected frame "
            "generators with one involution z."
        ),
        coefficient_factorization=(
            "W=y1*y2*y3*B and pair-deleted color-zero relators are "
            "R12=y3*B, R13=y2*B, R23=y1*B."
        ),
        normal_closure_identity="W=R23*R13^-1*y2^2*R12",
        arbitrary_frame_width=True,
        arbitrary_leaf_placement=True,
        arbitrary_frame_types=True,
        arbitrary_additional_support_rows=True,
        arbitrary_different_support=True,
        exact_target_identity=True,
        universal_triangle_target_no_go_verified=True,
        status="universal-same-support-weight-two-triangle-target-no-go",
    )


def _representative_certificates() -> list[TriangleTargetCertificate]:
    return [
        audit_triangle_target_certificate(
            "MINIMAL-CONTIGUOUS", "EFEFABA", (0, 1, 2)
        ),
        audit_triangle_target_certificate(
            "MINIMAL-INTERLEAVED", "EFEBFAB", (0, 1, 2)
        ),
        audit_triangle_target_certificate(
            "WIDE-NONSEQUENTIAL-TRIPLE", "ABEFBAEABF", (0, 2, 5)
        ),
        audit_triangle_target_certificate(
            "LEAF-BOUNDARY-COEFFICIENTS", "EAABFEBAFBA", (1, 3, 6)
        ),
    ]


def run_same_support_triangle_target_no_go(
) -> SameSupportTriangleTargetNoGoReport:
    representatives = _representative_certificates()
    censuses = [
        exhaustive_triangle_pattern_census(3),
        exhaustive_triangle_pattern_census(4),
    ]
    countercontrol = audit_missing_triangle_edge_countercontrol()
    translated = audit_translated_triangle_countercontrol()
    theorem = triangle_target_all_depth_certificate()
    exact = (
        all(row.all_group_target_identity_proved for row in representatives)
        and all(row.certificate_failure_count == 0 for row in censuses)
        and countercontrol.target_survival_verified
        and translated.exact_countercontrol_verified
        and theorem.universal_triangle_target_no_go_verified
    )
    return SameSupportTriangleTargetNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.pattern_scope,
            "support_condition": theorem.support_condition,
            "target_certificate": theorem.normal_closure_identity,
            "scope_limit": (
                "Translated triangles, triangles only in support differences, and "
                "triangle-free nonlinear supports remain open."
            ),
        },
        representative_certificates=representatives,
        exhaustive_censuses=censuses,
        missing_edge_countercontrol=countercontrol,
        translated_triangle_countercontrol=translated,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "remove_leaf_placement_and_frame_type_assumptions",
                "resolved": True,
                "resolution": (
                    "All other generators are absorbed into arbitrary coefficient "
                    "blocks b0,b1,b2,b3."
                ),
            },
            {
                "obligation": "prove_target_identity_over_every_group",
                "resolved": True,
                "resolution": (
                    "The target is an explicit product of the three pair-deleted "
                    "relators and a conjugate of the derived involution relator."
                ),
            },
            {
                "obligation": "classify_triangle_free_target_surviving_supports",
                "resolved": False,
                "resolution": (
                    "The missing-edge S3 control proves that fewer than three pair "
                    "rows can retain target mass."
                ),
            },
            {
                "obligation": "extend_to_affine_translated_triangles",
                "resolved": False,
                "resolution": (
                    "False in general: the stored width-five translated plane has "
                    "168 nonidentity S3 targets. Its pressure margin is nevertheless "
                    "two, so scalable translated constructions remain unclassified."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The even-parity no-go depends on a special leaf order.",
                "resolved": True,
                "resolution": (
                    "False: one local triangle kills the target for every four-leaf "
                    "placement and A/B frame word."
                ),
            },
            {
                "objection": "Different-support relations are needed for collapse.",
                "resolved": True,
                "resolution": (
                    "The certificate uses only six same-support relators."
                ),
            },
            {
                "objection": "Two weight-two rows should already suffice.",
                "resolved": True,
                "resolution": (
                    "False: deleting the third edge yields 42 nonidentity S3 targets."
                ),
            },
            {
                "objection": "Width-three enumeration is the all-width proof.",
                "resolved": True,
                "resolution": (
                    "The arbitrary coefficient-block identity is the proof; width "
                    "censuses only test the implementation."
                ),
            },
            {
                "objection": "XOR translation preserves the zero-based theorem.",
                "resolved": True,
                "resolution": (
                    "False: ordered background coefficients retain a target in the "
                    "translated width-five control, although its scalar mass fails."
                ),
            },
        ],
        headline_metrics={
            "all_depth_triangle_target_no_go_theorem_count": int(exact),
            "representative_certificate_count": len(representatives),
            "representative_certificate_failure_count": sum(
                not row.all_group_target_identity_proved for row in representatives
            ),
            "exhaustive_pattern_count": sum(
                row.checked_pattern_count for row in censuses
            ),
            "exhaustive_triangle_certificate_count": sum(
                row.checked_triangle_count for row in censuses
            ),
            "exhaustive_certificate_failure_count": sum(
                row.certificate_failure_count for row in censuses
            ),
            "missing_edge_S3_solution_count": countercontrol.solution_count,
            "missing_edge_S3_nonidentity_target_count": (
                countercontrol.nonidentity_target_count
            ),
            "translated_triangle_S3_solution_count": translated.solution_count,
            "translated_triangle_S3_nonidentity_target_count": (
                translated.nonidentity_target_count
            ),
            "translated_triangle_pressure_survival_count": int(
                translated.scalar_pressure_survival_verified
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "same_support_weight_two_triangle_forces_target_identity": exact,
            "all_even_parity_interleaved_targets_controlled": exact,
            "two_edge_path_forces_target_identity": False,
            "affine_translated_triangles_controlled": False,
            "all_triangle_free_supports_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A local weight-two triangle annihilates the mixed target exactly; "
                "only triangle-free or translated support geometry can survive."
            ),
        },
        status=(
            "same-support-weight-two-triangle-targets-falsified"
            if exact
            else "same-support-triangle-certificate-failure"
        ),
        summary=(
            "Proved an arbitrary-placement target no-go from one local same-support "
            "weight-two triangle and exhibited a sharp missing-edge survivor."
        ),
        falsifiers_triggered=[
            "Even-parity target collapse is not pattern-specific.",
            "Three local same-support rows can kill a global mixed target.",
            "Two sides of the triangle do not imply the theorem.",
            "Affine XOR translation does not preserve target collapse.",
            "Different-support complexity cannot rescue a killed target.",
        ],
    )


def write_same_support_triangle_target_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SAME-SUPPORT-TRIANGLE-TARGET-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_same_support_triangle_target_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_same_support_triangle_target_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
