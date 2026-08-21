"""Scalar pressure and target reduction for contiguous mixed A/B frames.

Consider

    E T_1 ... T_u F E F,        T_i in {A,B},

with arbitrary nonempty same/different supports ``S,D``.  The support
color-one relations are independent of the A/B frame types, so the exact
two-fiber entropy theorem still pays

    max(log2|S union {0}|, log2|D|)

permutation-group exponents.  If ``w_A`` is the ordered product of A-frame
variables, the split color-zero equation and a base ``q in D`` reduce to

    A (bT) A^-1 = w_q b,        T=w_barq^-1 w_A,          (1)

after putting ``A=a w_A``.  Hence the uniform ``|G|k(G)`` outer bound survives
for every A/B pattern, proving scalar crossing pressure at most ``-1``.

The same algebra preserves the target instead of discarding it.  Put

    X=x_1...x_u,       R=w_A^-1 X.

Modulo (1), the full target product is exactly ``A R A^-1``.  Every normalized
irreducible character therefore evaluates to ``chi(R)/d`` on every solution.
This removes the outer variables from the character value, but not from the
measure: the number of allowed conjugators is either zero or
``|C_G(bT)|``.  The remaining high-value problem is thus a weighted frame-word
character estimate under the split-B and support-fiber relations.

The theorem does not bound that signed weighted average.  In particular,
scalar pressure control is not a component moment or a quantum speedup.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_contiguous_all_a_support_pressure import (
    audit_contiguous_all_a_support_pressure,
)
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    _evaluate_signed_word,
    _substitute_generator,
    canonical_relator,
    free_reduce,
    marked_support_presentation,
    normalize_relations,
    orientable_quadratic_genus,
    tietze_reduce_presentation,
)
from self_dual_wreath_mixed_split_target_genus import cyclic_one_run_count


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_contiguous_frame_target_factorization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Assignment = tuple[int, ...]


@dataclass(frozen=True)
class ContiguousFrameTargetControl:
    control_id: str
    frame_types: tuple[str, ...]
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    different_base_assignment: Assignment
    split_b_run_count: int
    split_target_genus: int
    a_frame_subword: SignedWord
    b_frame_subword: SignedWord
    full_frame_word: SignedWord
    target_frame_word: SignedWord
    outer_conjugacy_twist_word: SignedWord
    transformed_outer_relation: SignedWord
    transformed_target_word: SignedWord
    target_after_outer_relation: SignedWord
    selected_frame_relations: tuple[SignedWord, ...]
    selected_frame_target_residual: SignedWord
    selected_frame_target_orientable_genus: int | None
    full_reduced_frame_relations: tuple[SignedWord, ...]
    full_reduced_frame_target_residual: SignedWord
    full_reduced_frame_target_orientable_genus: int | None
    full_reduced_frame_target_is_relator: bool
    full_presentation_target_residual: SignedWord
    full_presentation_freely_kills_target: bool
    full_presentation_symbolically_kills_target: bool
    scalar_crossing_pressure_upper_bound: float
    scalar_crossing_pressure_margin: float
    zero_same_assignment_present: bool
    zero_same_cell_forces_target_identity: bool
    scalar_pressure_saturation_condition_verified: bool
    nonzero_target_pressure_margin_lower_bound: float
    target_survival_pressure_tradeoff_verified: bool
    exact_outer_conjugacy_factorization_verified: bool
    exact_target_conjugacy_factorization_verified: bool
    exact_mixed_frame_scalar_pressure_verified: bool
    weighted_frame_character_bound_proved: bool
    status: str


@dataclass(frozen=True)
class ContiguousFrameTargetScalingRecord:
    frame_position_count: int
    checked_frame_type_base_pair_count: int
    outer_factorization_failure_count: int
    target_factorization_failure_count: int
    maximum_split_target_genus: int
    status: str


@dataclass(frozen=True)
class ContiguousTargetSurvivalLiftControl:
    lift_depth: int
    frame_position_count: int
    frame_types: tuple[str, ...]
    same_support_size: int
    different_support_size: int
    real_entropy_certificate_margin: float
    scalar_crossing_pressure_margin: float
    predicted_margin: float
    symmetric_group_degree: int
    target_permutation: tuple[int, ...]
    target_is_nonidentity: bool
    all_full_presentation_relations_satisfied: bool
    exact_identity_frame_lift_verified: bool
    status: str


@dataclass(frozen=True)
class ContiguousFrameTargetFactorizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[ContiguousFrameTargetControl]
    target_survival_lift_controls: list[ContiguousTargetSurvivalLiftControl]
    scaling_records: list[ContiguousFrameTargetScalingRecord]
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


def _subword(bits: Iterable[int | bool]) -> SignedWord:
    return tuple(index + 1 for index, bit in enumerate(bits) if bit)


def _inverse(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _transport_word(word: SignedWord, reduction: Any) -> SignedWord:
    for step in reduction.elimination_steps:
        word = _substitute_generator(
            word,
            step.eliminated_generator,
            step.replacement_word,
        )
    return free_reduce(word)


def _compose_permutations(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def audit_target_survival_identity_frame_lift(
    lift_depth: int,
) -> ContiguousTargetSurvivalLiftControl:
    """Audit the old identity-frame lift against the stronger integer bound."""

    if lift_depth < 0:
        raise ValueError("lift depth must be nonnegative")
    identity = (0, 1, 2)
    seed_frames = (
        (0, 2, 1),
        (1, 0, 2),
        (0, 2, 1),
        (2, 0, 1),
    )
    seed_same = (1, 0, 1, 0)
    seed_different = ((0, 0, 0, 0), (0, 1, 1, 1))
    suffixes = tuple(itertools.product((0, 1), repeat=lift_depth))
    same = tuple((*seed_same, *suffix) for suffix in suffixes)
    different_pool = tuple(
        sorted(
            (*seed, *suffix)
            for seed in seed_different
            for suffix in suffixes
        )
    )
    different = different_pool[: len(same) + 1]
    frame_types = (*tuple("BABA"), *("A",) * lift_depth)
    frames = (*seed_frames, *(identity,) * lift_depth)

    # A=a*w_A, b, and the reconstructed original outer variables for q=0.
    transformed_a = (0, 2, 1)
    outer_b = (1, 2, 0)
    w_a = identity
    for frame_type, value in zip(frame_types, frames):
        if frame_type == "A":
            w_a = _compose_permutations(w_a, value)
    original_a = _compose_permutations(
        transformed_a,
        _inverse_permutation(w_a),
    )
    outer_c = (1, 0, 2)
    outer_e = (2, 0, 1)
    pattern = "E" + "".join(frame_types) + "FEF"
    values = (original_a, *frames, outer_b, outer_c, outer_e)
    assignment = dict(enumerate(values, start=1))
    relations = marked_support_presentation(pattern, same, different)
    relation_exact = all(
        _evaluate_signed_word(relation, assignment) == identity
        for relation in relations
    )
    target = _evaluate_signed_word(
        tuple(range(1, len(pattern) + 1)),
        assignment,
    )
    pressure = audit_contiguous_all_a_support_pressure(
        "IDENTITY-FRAME-LIFT",
        same,
        different,
    )
    real_entropy_margin = 0.5 * math.log2(1.0 + 1.0 / len(same))
    dominant_size = max(len({(0,) * len(same[0]), *same}), len(different))
    predicted = (
        (dominant_size - 1).bit_length()
        - 0.5 * math.log2(len(same) * len(different))
    )
    exact = (
        relation_exact
        and target != identity
        and len(same) == 2**lift_depth
        and len(different) == 2**lift_depth + 1
        and abs(pressure.crossing_pressure_margin - predicted) <= 1e-12
    )
    return ContiguousTargetSurvivalLiftControl(
        lift_depth=lift_depth,
        frame_position_count=4 + lift_depth,
        frame_types=frame_types,
        same_support_size=len(same),
        different_support_size=len(different),
        real_entropy_certificate_margin=real_entropy_margin,
        scalar_crossing_pressure_margin=pressure.crossing_pressure_margin,
        predicted_margin=predicted,
        symmetric_group_degree=3,
        target_permutation=target,
        target_is_nonidentity=target != identity,
        all_full_presentation_relations_satisfied=relation_exact,
        exact_identity_frame_lift_verified=exact,
        status=(
            "exact-identity-lift-closed-by-integer-generator-gap"
            if exact
            else "target-survival-lift-control-failure"
        ),
    )


def audit_contiguous_frame_target_factorization(
    control_id: str,
    frame_types: tuple[str, ...],
    same_support: Iterable[Assignment],
    different_support: Iterable[Assignment],
) -> ContiguousFrameTargetControl:
    if not frame_types or any(token not in "AB" for token in frame_types):
        raise ValueError("frame types must be a nonempty A/B tuple")
    same = _normalize_support(same_support)
    different = _normalize_support(different_support)
    width = len(frame_types)
    if len(same[0]) != width or len(different[0]) != width:
        raise ValueError("support width must equal the frame count")
    base = different[0]
    scalar = audit_contiguous_all_a_support_pressure(
        control_id,
        same,
        different,
    )

    full = tuple(range(1, width + 1))
    a_word = _subword(token == "A" for token in frame_types)
    b_word = _subword(token == "B" for token in frame_types)
    base_word = _subword(base)
    complement_word = _subword(1 - bit for bit in base)
    target_frame = free_reduce((*_inverse(a_word), *full))
    twist = free_reduce((*_inverse(complement_word), *a_word))
    outer_a = width + 1
    outer_b = width + 2

    transformed_outer = free_reduce(
        (
            outer_a,
            outer_b,
            *twist,
            -outer_a,
            -outer_b,
            *_inverse(base_word),
        )
    )
    substituted_outer = free_reduce(
        (
            outer_a,
            *_inverse(a_word),
            *a_word,
            outer_b,
            *_inverse(complement_word),
            *a_word,
            -outer_a,
            -outer_b,
            *_inverse(base_word),
        )
    )
    transformed_target = free_reduce(
        (
            outer_a,
            *target_frame,
            outer_b,
            *twist,
            -outer_a,
            -outer_b,
            *_inverse(base_word),
        )
    )
    substituted_target = free_reduce(
        (
            outer_a,
            *_inverse(a_word),
            *full,
            outer_b,
            *_inverse(complement_word),
            *a_word,
            -outer_a,
            -outer_b,
            *_inverse(base_word),
        )
    )
    g_word = (outer_b, *twist)
    # The outer equation replaces h^-1=b^-1*w_q^-1 by A*g^-1*A^-1.
    target_after_relation = free_reduce(
        (
            outer_a,
            *target_frame,
            *g_word,
            -outer_a,
            outer_a,
            *_inverse(g_word),
            -outer_a,
        )
    )
    expected_target = free_reduce((outer_a, *target_frame, -outer_a))
    exact_outer = substituted_outer == transformed_outer
    exact_target = (
        substituted_target == transformed_target
        and target_after_relation == expected_target
    )

    relative_different = tuple(
        free_reduce((*_subword(row), *_inverse(base_word)))
        for row in different
    )
    selected_frame_relations = normalize_relations(
        (
            b_word,
            *(_subword(row) for row in same),
            *relative_different,
        )
    )
    frame_reduction = tietze_reduce_presentation(
        width,
        selected_frame_relations,
    )
    selected_target_residual = _transport_word(target_frame, frame_reduction)
    selected_genus = (
        orientable_quadratic_genus(selected_target_residual)
        if selected_target_residual
        else 0
    )

    same_complement_relations = tuple(
        free_reduce(
            (
                *_inverse(a_word),
                *_subword(1 - bit for bit in row),
            )
        )
        for row in same
    )
    different_complement_relations = tuple(
        free_reduce(
            (
                *_subword(1 - bit for bit in row),
                *_inverse(complement_word),
            )
        )
        for row in different
    )
    full_reduced_frame_relations = normalize_relations(
        (
            *selected_frame_relations,
            *same_complement_relations,
            *different_complement_relations,
        )
    )
    full_frame_reduction = tietze_reduce_presentation(
        width,
        full_reduced_frame_relations,
    )
    full_frame_target_residual = _transport_word(
        target_frame,
        full_frame_reduction,
    )
    full_frame_genus = (
        orientable_quadratic_genus(full_frame_target_residual)
        if full_frame_target_residual
        else 0
    )
    full_frame_target_is_relator = bool(
        full_frame_target_residual
        and canonical_relator(full_frame_target_residual)
        in full_frame_reduction.residual_relations
    )

    pattern = "E" + "".join(frame_types) + "FEF"
    full_relations = marked_support_presentation(pattern, same, different)
    full_reduction = tietze_reduce_presentation(len(pattern), full_relations)
    full_target = tuple(range(1, len(pattern) + 1))
    full_target_residual = _transport_word(full_target, full_reduction)
    full_target_is_relator = bool(
        full_target_residual
        and canonical_relator(full_target_residual)
        in full_reduction.residual_relations
    )
    full_symbolically_kills_target = (
        not full_frame_target_residual
        or full_frame_target_is_relator
        or not full_target_residual
        or full_target_is_relator
    )

    zero = (0,) * width
    zero_same = zero in same
    zero_forces_target = (
        not zero_same
        or canonical_relator(target_frame) in full_reduced_frame_relations
        or not full_frame_target_residual
        or full_frame_target_is_relator
    )
    equal_power_of_two_supports = (
        len(same) == len(different)
        and len(same) & (len(same) - 1) == 0
    )
    saturation_expected = zero_same and equal_power_of_two_supports
    saturation_actual = abs(scalar.crossing_pressure_margin) <= 1e-12
    saturation_verified = saturation_actual == saturation_expected
    target_margin_lower_bound = (
        0.0
        if zero_same
        else (
            (max(len(same) + 1, len(different)) - 1).bit_length()
            - 0.5 * math.log2(len(same) * len(different))
        )
    )
    survival_tradeoff = (
        zero_forces_target
        and (
            zero_same
            or scalar.crossing_pressure_margin
            >= target_margin_lower_bound - 1e-12
        )
    )

    scalar_exact = (
        scalar.exact_all_support_pressure_theorem_verified
        and exact_outer
        and scalar.crossing_pressure_upper_bound <= -1 + 1e-12
    )
    return ContiguousFrameTargetControl(
        control_id=control_id,
        frame_types=frame_types,
        same_support=same,
        different_support=different,
        different_base_assignment=base,
        split_b_run_count=cyclic_one_run_count(
            tuple(token == "B" for token in frame_types)
        ),
        split_target_genus=max(
            0,
            cyclic_one_run_count(tuple(token == "B" for token in frame_types)) - 1,
        ),
        a_frame_subword=a_word,
        b_frame_subword=b_word,
        full_frame_word=full,
        target_frame_word=target_frame,
        outer_conjugacy_twist_word=twist,
        transformed_outer_relation=transformed_outer,
        transformed_target_word=transformed_target,
        target_after_outer_relation=expected_target,
        selected_frame_relations=selected_frame_relations,
        selected_frame_target_residual=selected_target_residual,
        selected_frame_target_orientable_genus=selected_genus,
        full_reduced_frame_relations=full_reduced_frame_relations,
        full_reduced_frame_target_residual=full_frame_target_residual,
        full_reduced_frame_target_orientable_genus=full_frame_genus,
        full_reduced_frame_target_is_relator=full_frame_target_is_relator,
        full_presentation_target_residual=full_target_residual,
        full_presentation_freely_kills_target=not full_target_residual,
        full_presentation_symbolically_kills_target=(
            full_symbolically_kills_target
        ),
        scalar_crossing_pressure_upper_bound=scalar.crossing_pressure_upper_bound,
        scalar_crossing_pressure_margin=scalar.crossing_pressure_margin,
        zero_same_assignment_present=zero_same,
        zero_same_cell_forces_target_identity=zero_forces_target,
        scalar_pressure_saturation_condition_verified=saturation_verified,
        nonzero_target_pressure_margin_lower_bound=target_margin_lower_bound,
        target_survival_pressure_tradeoff_verified=survival_tradeoff,
        exact_outer_conjugacy_factorization_verified=exact_outer,
        exact_target_conjugacy_factorization_verified=exact_target,
        exact_mixed_frame_scalar_pressure_verified=scalar_exact,
        weighted_frame_character_bound_proved=False,
        status=(
            "target-reduced-to-weighted-frame-character"
            if scalar_exact and exact_target
            else "contiguous-frame-factorization-failure"
        ),
    )


def run_contiguous_frame_target_factorization(
    maximum_frame_count: int = 8,
) -> ContiguousFrameTargetFactorizationReport:
    from self_dual_wreath_target_survival_surface_seed import (
        audit_power_boundary_lift,
    )

    if maximum_frame_count < 1:
        raise ValueError("maximum frame count must be positive")
    scaling: list[ContiguousFrameTargetScalingRecord] = []
    total_checks = 0
    outer_failures = 0
    target_failures = 0
    maximum_genus = 0
    singleton_same_cache: dict[int, tuple[Assignment, ...]] = {}
    for width in range(1, maximum_frame_count + 1):
        zero = (0,) * width
        singleton_same_cache[width] = (zero,)
        row_checks = 0
        row_outer_failures = 0
        row_target_failures = 0
        row_maximum_genus = 0
        for frame_types in itertools.product("AB", repeat=width):
            for base in itertools.product((0, 1), repeat=width):
                control = audit_contiguous_frame_target_factorization(
                    "SYMBOLIC-SCALING",
                    frame_types,
                    (zero,),
                    (base,),
                )
                row_checks += 1
                row_outer_failures += not (
                    control.exact_outer_conjugacy_factorization_verified
                )
                row_target_failures += not (
                    control.exact_target_conjugacy_factorization_verified
                )
                row_maximum_genus = max(
                    row_maximum_genus,
                    control.split_target_genus,
                )
        total_checks += row_checks
        outer_failures += row_outer_failures
        target_failures += row_target_failures
        maximum_genus = max(maximum_genus, row_maximum_genus)
        scaling.append(
            ContiguousFrameTargetScalingRecord(
                frame_position_count=width,
                checked_frame_type_base_pair_count=row_checks,
                outer_factorization_failure_count=row_outer_failures,
                target_factorization_failure_count=row_target_failures,
                maximum_split_target_genus=row_maximum_genus,
                status=(
                    "all-symbolic-factorizations-passed"
                    if not row_outer_failures and not row_target_failures
                    else "symbolic-factorization-failure"
                ),
            )
        )

    representatives = [
        audit_contiguous_frame_target_factorization(
            "ALL-A-TARGET-CANCELS",
            ("A", "A", "A", "A"),
            ((0, 0, 0, 0),),
            ((0, 0, 0, 0),),
        ),
        audit_contiguous_frame_target_factorization(
            "ONE-B-RUN-TARGET-CANCELS",
            ("A", "A", "B", "B"),
            ((0, 0, 0, 0),),
            ((1, 0, 1, 0),),
        ),
        audit_contiguous_frame_target_factorization(
            "ALTERNATING-GENUS-ONE-SURVIVES-SELECTED-RELATIONS",
            ("A", "B", "A", "B"),
            ((0, 1, 0, 1),),
            ((0, 0, 0, 0),),
        ),
        audit_contiguous_frame_target_factorization(
            "ALTERNATING-SUPPORT-CONDITIONED",
            ("A", "B", "A", "B", "A", "B"),
            ((0, 0, 0, 0, 0, 0), (1, 0, 1, 0, 0, 1)),
            ((1, 0, 0, 1, 0, 1), (0, 1, 1, 0, 1, 0)),
        ),
    ]
    target_lifts = [
        audit_target_survival_identity_frame_lift(depth)
        for depth in range(13)
    ]
    power_boundary_lifts = [
        audit_power_boundary_lift(depth) for depth in range(1, 9)
    ]
    power_boundary_exact = all(
        row.exact_power_boundary_lift_classified for row in power_boundary_lifts
    )
    lift_exact = all(row.exact_identity_frame_lift_verified for row in target_lifts)
    exact = outer_failures == target_failures == 0 and lift_exact and all(
        row.exact_mixed_frame_scalar_pressure_verified
        and row.exact_target_conjugacy_factorization_verified
        and row.scalar_pressure_saturation_condition_verified
        and row.target_survival_pressure_tradeoff_verified
        for row in representatives
    )
    surviving_selected = sum(
        bool(row.selected_frame_target_residual) for row in representatives
    )
    return ContiguousFrameTargetFactorizationReport(
        created_at=utc_now(),
        theorem_contract={
            "mixed_frame_scalar_pressure": (
                "Support color-one fibers do not depend on A/B types, and the "
                "split color-zero equation retains the |G|k(G) conjugacy bound."
            ),
            "target_factorization": (
                "On every solution the full target is conjugate to "
                "R=w_A^-1(x_1...x_u), so normalized characters equal chi(R)/d."
            ),
            "remaining_weight": (
                "Frame assignments are weighted by the conjugator count "
                "1[bT conjugate w_q b]*|C_G(bT)| summed over b."
            ),
            "target_survival_pressure_tradeoff": (
                "Under the integer suffix-branch bound, pressure saturation "
                "occurs exactly when 0 is in S and |S|=|D| is a power of two. "
                "The zero same cell contributes R itself, so every saturating "
                "profile forces target identity."
            ),
            "scope": (
                "The word must have contiguous A/B frames between the first E "
                "and F. No signed weighted-frame character bound is proved."
            ),
        },
        representative_controls=representatives,
        target_survival_lift_controls=target_lifts,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "extend_scalar_support_pressure_to_contiguous_B_frames",
                "resolved": exact,
                "resolution": (
                    "The two support fibers and outer conjugacy count are unchanged "
                    "except for the explicit twist T=w_barq^-1*w_A."
                ),
            },
            {
                "obligation": "remove_outer_variables_from_target_character_value",
                "resolved": exact,
                "resolution": (
                    "The target equals A*R*A^-1 modulo the exact outer equation."
                ),
            },
            {
                "obligation": "bound_weighted_support_conditioned_frame_character",
                "resolved": False,
                "resolution": (
                    "Control the character of R under split/support equations with "
                    "the nonuniform centralizer/conjugacy weight from the outer fiber."
                ),
            },
            {
                "obligation": "separate_nontrivial_targets_from_scalar_pressure_saturation",
                "resolved": exact,
                "resolution": (
                    "The exact equality condition requires the zero same cell, "
                    "which inserts R as a frame relator. Nontrivial targets have "
                    "a strictly positive fixed-width scalar margin."
                ),
            },
            {
                "obligation": "make_target_survival_pressure_gap_uniform_at_growing_width",
                "resolved": False,
                "resolution": (
                    "Pruning the identity lift to sizes 2^k-1 and 2^k makes the "
                    "strongest generic integer-certificate margin tend to zero. "
                    "However, its exact presentation is genus two with one free "
                    "generator and has true pressure margin greater than one. A "
                    "surviving actual-presentation counterexample remains open."
                ),
            },
            {
                "obligation": "extend_to_interleaved_leaf_patterns",
                "resolved": False,
                "resolution": (
                    "Interleaved E/F leaves break the single two-variable outer "
                    "conjugacy equation and require a multi-boundary analogue."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A scalar pressure theorem automatically controls the target.",
                "resolved": True,
                "resolution": (
                    "False. Scalar counting only localizes the target to R; it gives "
                    "no sign or cancellation estimate for chi(R)."
                ),
            },
            {
                "objection": "Eliminating the outer variables makes frame assignments uniform.",
                "resolved": True,
                "resolution": (
                    "False. Each frame assignment retains a conjugacy indicator and "
                    "centralizer-size weight depending on bT and w_q b."
                ),
            },
            {
                "objection": "Every mixed frame pattern has a surviving target.",
                "resolved": True,
                "resolution": (
                    "False. Zero or one cyclic B-run gives genus zero, and support "
                    "relations can kill targets that survive the split alone."
                ),
            },
            {
                "objection": "A profile can both saturate scalar pressure and retain a nonidentity target.",
                "resolved": True,
                "resolution": (
                    "Impossible in this family: saturation requires 0 in S, and "
                    "that same-coordinate cell contributes R as an exact relator."
                ),
            },
            {
                "objection": "The strict fixed-width target margin can be upgraded to a uniform constant.",
                "resolved": False,
                "resolution": (
                    "No generic certificate can do this: the pruned power-boundary "
                    "lift has vanishing integer-certificate margin. Its exact "
                    "surface-times-free presentation is nevertheless uniformly "
                    "subleading, so the actual-presentation theorem remains open."
                ),
            },
        ],
        headline_metrics={
            "checked_frame_type_base_pair_count": total_checks,
            "outer_factorization_failure_count": outer_failures,
            "target_factorization_failure_count": target_failures,
            "maximum_split_target_genus": maximum_genus,
            "representative_selected_target_survival_count": surviving_selected,
            "growing_width_mixed_frame_scalar_pressure_theorem_count": int(exact),
            "exact_target_to_frame_character_reduction_theorem_count": int(exact),
            "target_survival_strict_pressure_tradeoff_theorem_count": int(exact),
            "growing_width_uniform_target_survival_pressure_gap_theorem_count": 0,
            "exact_S3_target_survival_identity_frame_lift_count": len(target_lifts),
            "target_survival_lift_failure_count": sum(
                not row.exact_identity_frame_lift_verified for row in target_lifts
            ),
            "minimum_target_survival_lift_pressure_margin": min(
                row.scalar_crossing_pressure_margin for row in target_lifts
            ),
            "minimum_real_entropy_lift_certificate_margin": min(
                row.real_entropy_certificate_margin for row in target_lifts
            ),
            "real_entropy_certificate_gap_falsified_count": int(lift_exact),
            "integer_suffix_branch_identity_lift_gap_closed_count": int(lift_exact),
            "uniform_certificate_pressure_gap_falsified_count": 0,
            "power_boundary_integer_certificate_gap_falsified_count": int(
                power_boundary_exact
            ),
            "power_boundary_actual_presentation_escape_count": 0,
            "weighted_frame_character_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "contiguous_mixed_frame_scalar_pressure_proved": exact,
            "target_character_value_reduced_to_frame_word": exact,
            "pressure_saturation_forces_target_identity": exact,
            "fixed_width_nontrivial_target_strictly_subthreshold": exact,
            "growing_width_uniform_target_survival_gap_proved": False,
            "real_entropy_certificate_gap_falsified": lift_exact,
            "identity_lift_closed_by_integer_suffix_branch_bound": lift_exact,
            "uniform_certificate_pressure_gap_falsified": False,
            "power_boundary_integer_certificate_gap_falsified": (
                power_boundary_exact
            ),
            "power_boundary_actual_presentation_survives": False,
            "asymptotic_Sn_target_survival_lower_bound_proved": False,
            "weighted_frame_character_average_controlled": False,
            "interleaved_leaf_patterns_certified": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The target value is now a frame-only character, but its "
                "support-conditioned centralizer-weighted average and a "
                "growing-width S_n lower/upper bound are open. The previous "
                "identity-lift gap falsifier is closed by the stronger integer "
                "suffix-branch theorem. A pruned power-boundary lift defeats the "
                "generic certificate but itself collapses to surface-times-free."
            ),
        },
        status=(
            "contiguous-frame-target-reduced-weighted-character-open"
            if exact
            else "contiguous-frame-target-factorization-failure"
        ),
        summary=(
            "Extended arbitrary-support scalar pressure to mixed contiguous "
            "frames and reduced every surviving target character exactly to a "
            "weighted frame-word character problem; scalar saturation itself "
            "now provably forces target identity."
        ),
        falsifiers_triggered=[
            "Outer elimination preserves a nonuniform centralizer weight.",
            "Genus-zero split patterns cannot carry a nontrivial target.",
            "Additional support relations can erase split-only target topology.",
            "Identity-frame lifts only make the obsolete real entropy margin vanish.",
            "The integer suffix-branch bound restores a uniform gap on that lift.",
            "Power-boundary pruning defeats the generic bound but not the true presentation.",
            "The S3 lift does not establish asymptotic S_n solution mass.",
            "No result here supplies a positive component moment or decoder.",
        ],
    )


def write_contiguous_frame_target_factorization_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    report = asdict(run_contiguous_frame_target_factorization())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    return report


if __name__ == "__main__":
    result = write_contiguous_frame_target_factorization_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
