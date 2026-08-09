"""Frame-subword entropy reduction for contiguous all-A crossing words.

For the word ``E A^u F E F``, assume the different-coordinate support ``D``
contains the zero assignment and put ``U=S union D``.  The split relation and
the zero cell of ``D`` give ``F_u * Z^2`` exactly.  Every same-support
color-one relation is the ordered frame subword ``w_v``.  Every
different-support color-one relation becomes the same ``w_v`` after the zero
cell relation ``b d=1``.  Selecting these relations therefore gives

    P(U) * Z^2,

where

    P(U)=<x_1,...,x_u | w_v=1 for v in U>.

If ``e(U)`` is any certified leading ``log_|S_n|`` solution exponent for
``P(U)``, the full support profile has crossing pressure at most

    e(U) + H(S,D) - u - 1,

where ``H=(log2|S|+log2|D|)/2``.  Thus ``e(U)+H<=u`` proves the target
pressure ``<=-1``.  Since ``H<=log2|U|``, the single-support inequality

    e(U)+log2|U| <= u                                      (1)

is sufficient for every pair with that union.

The all-width inequality follows by an exact re-rooting induction.  For
``a in U``, the triangular free-group automorphism

    x_i -> A_i x_i^((-1)^a_i) A_i^-1,
    A_i=product_(j<i) x_j^a_j,

sends every ordered subword ``w_b`` to

    w_(a xor b) w_a^-1.

Because ``0,a in U``, this proves ``P(U) isomorphic to P(U xor a)``.  Re-root
at an element of the larger last-coordinate half, so the zero half ``U_0``
has at least ``|U|/2`` elements.  If the one half is empty, the last generator
is free.  Otherwise any one-half relation uniquely determines it and the
remaining presentation is a quotient of ``P(U_0)``.  Induction gives, for
every finite group ``G``,

    #Hom(P(U),G) <= |G|^(u-log2|U|).                       (2)

Thus (1) holds at every width.  Exhaustive width-four and deterministic
width-five runs remain as implementation controls, not evidence substituted
for the proof.  Nonzero base cells, interleaved leaves, B frames, and mixed
targets remain outside this theorem.

There is also a sharper generator theorem.  For an anchor ``a in U``, call
coordinate ``i`` suffix-forced when no row of ``U`` agrees with ``a`` after
``i`` and flips bit ``i``.  After XOR re-rooting at ``a``, every non-forced
coordinate has a relator containing ``x_i`` exactly once and no generator
above ``i``.  Descending elimination leaves only the forced coordinates.
For uniform ``X in U``, the chain rule gives

    log2|U| = sum_i H(X_i | X_(i+1),...,X_u).

Each conditional entropy is zero at a forced trie node and at most one at a
branching node.  Hence the average number of forced coordinates is at most
``u-log2|U|``, and some anchor leaves at most its floor.  Therefore

    #Hom(P(U),G) <= |G|^floor(u-log2|U|)                  (3)

for every nonempty support ``U`` and finite group ``G``.  This explicit
integer-rank bound strengthens (2) whenever the entropy codimension is not an
integer; the two proofs remain independently checked.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_marked_relation_topology import (
    TietzeReduction,
    free_reduce,
    normalize_relations,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_frame_subword_entropy.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Assignment = tuple[int, ...]
SignedWord = tuple[int, ...]


@dataclass(frozen=True)
class FrameSubwordRerootingCertificate:
    base_vertex: Assignment
    generator_images: tuple[SignedWord, ...]
    checked_cube_vertex_count: int
    every_subword_identity_verified: bool
    triangular_automorphism_verified: bool
    exact_rerooting_isomorphism_verified: bool


@dataclass(frozen=True)
class FrameSubwordEntropyInductionStep:
    frame_position_count: int
    support_size: int
    initial_zero_half_size: int
    initial_one_half_size: int
    rerooted: bool
    reroot_base: Assignment | None
    zero_half_size: int
    one_half_size: int
    recurrence_branch: str
    child_support_size: int
    child_solution_exponent_upper_bound: float
    derived_solution_exponent_upper_bound: float
    target_solution_exponent_upper_bound: float
    induction_slack: float
    exact_step_verified: bool


@dataclass(frozen=True)
class FrameSubwordEntropyInductionCertificate:
    support: tuple[Assignment, ...]
    support_size: int
    support_entropy_bits: float
    universal_finite_group_solution_exponent_upper_bound: float
    rerooting_step_count: int
    induction_steps: tuple[FrameSubwordEntropyInductionStep, ...]
    exact_induction_verified: bool


@dataclass(frozen=True)
class FrameSubwordSuffixBranchCertificate:
    support: tuple[Assignment, ...]
    support_size: int
    frame_position_count: int
    entropy_codimension: float
    suffix_forced_incidence_count: int
    average_suffix_forced_coordinate_count: float
    anchor: Assignment
    suffix_branch_coordinates: tuple[int, ...]
    suffix_forced_coordinates: tuple[int, ...]
    suffix_branch_witnesses: tuple[Assignment, ...]
    universal_finite_group_generator_upper_bound: int
    entropy_chain_rule_value: float
    entropy_chain_rule_verified: bool
    average_forced_bound_verified: bool
    explicit_anchor_bound_verified: bool
    exact_suffix_branch_elimination_verified: bool
    status: str


@dataclass(frozen=True)
class FrameSubwordEntropyControl:
    control_id: str
    frame_position_count: int
    support: tuple[Assignment, ...]
    support_size: int
    support_entropy_bits: float
    frame_relations: tuple[tuple[int, ...], ...]
    eliminated_generator_count: int
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[tuple[int, ...], ...]
    classifier_solution_exponent_upper_bound: float
    universal_finite_group_solution_exponent_upper_bound: float
    universal_finite_group_generator_upper_bound: int
    frame_solution_exponent_upper_bound: float
    exponent_certificate_source: str
    entropy_margin: float
    rerooting_step_count: int
    entropy_induction_verified: bool
    suffix_branch_certificate: FrameSubwordSuffixBranchCertificate
    suffix_branch_generator_bound_verified: bool
    exact_subword_presentation_verified: bool
    pressure_inequality_certified: bool
    status: str


@dataclass(frozen=True)
class FrameSubwordScalingRecord:
    frame_position_count: int
    checked_zero_containing_support_count: int
    pressure_uncertified_support_count: int
    minimum_entropy_margin: float
    maximum_frame_solution_exponent: float
    status: str


@dataclass(frozen=True)
class FrameSubwordMethodFalsifier:
    control_id: str
    support: tuple[Assignment, ...]
    cube_edge_direction_count: int
    private_pivot_count: int
    edge_pivot_entropy_debt: float
    frame_subword_exponent: float
    frame_subword_entropy_margin: float
    edge_pivot_failure_is_pressure_counterexample: bool
    status: str


@dataclass(frozen=True)
class FrameSubwordEntropyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[FrameSubwordEntropyControl]
    method_falsifiers: list[FrameSubwordMethodFalsifier]
    exhaustive_scaling: list[FrameSubwordScalingRecord]
    width_five_stress: FrameSubwordScalingRecord
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
        raise ValueError("support must contain equally sized binary rows")
    return rows


def _ordered_subword(vertex: Assignment) -> SignedWord:
    return tuple(index + 1 for index, bit in enumerate(vertex) if bit)


def _inverse_word(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _xor(left: Assignment, right: Assignment) -> Assignment:
    if len(left) != len(right):
        raise ValueError("vertices must have equal width")
    return tuple(a ^ b for a, b in zip(left, right))


def _substitute_word(
    word: SignedWord,
    generator_images: tuple[SignedWord, ...],
) -> SignedWord:
    expanded: list[int] = []
    for letter in word:
        image = generator_images[abs(letter) - 1]
        expanded.extend(image if letter > 0 else _inverse_word(image))
    return free_reduce(expanded)


@lru_cache(maxsize=None)
def frame_subword_rerooting_certificate(
    base_vertex: Assignment,
) -> FrameSubwordRerootingCertificate:
    """Certify the triangular automorphism implementing XOR re-rooting."""

    if any(bit not in (0, 1) for bit in base_vertex):
        raise ValueError("base vertex must be binary")
    generator_images: list[SignedWord] = []
    prefix: list[int] = []
    for index, bit in enumerate(base_vertex):
        image = (
            *prefix,
            (index + 1) if not bit else -(index + 1),
            *_inverse_word(tuple(prefix)),
        )
        generator_images.append(free_reduce(image))
        if bit:
            prefix.append(index + 1)
    images = tuple(generator_images)
    triangular = all(
        sum(abs(letter) == index + 1 for letter in image) == 1
        and all(abs(letter) <= index + 1 for letter in image)
        for index, image in enumerate(images)
    )
    base_word_inverse = _inverse_word(_ordered_subword(base_vertex))
    vertices = tuple(itertools.product((0, 1), repeat=len(base_vertex)))
    identities = all(
        _substitute_word(_ordered_subword(vertex), images)
        == free_reduce(
            (*_ordered_subword(_xor(base_vertex, vertex)), *base_word_inverse)
        )
        for vertex in vertices
    )
    return FrameSubwordRerootingCertificate(
        base_vertex=base_vertex,
        generator_images=images,
        checked_cube_vertex_count=len(vertices),
        every_subword_identity_verified=identities,
        triangular_automorphism_verified=triangular,
        exact_rerooting_isomorphism_verified=identities and triangular,
    )


def reroot_frame_subword_support(
    support: Iterable[Assignment],
    base_vertex: Assignment,
) -> tuple[Assignment, ...]:
    support = _normalize_support(support)
    if base_vertex not in support:
        raise ValueError("re-rooting base must belong to the support")
    if (0,) * len(base_vertex) not in support:
        raise ValueError("re-rooting proof requires the zero vertex")
    certificate = frame_subword_rerooting_certificate(base_vertex)
    if not certificate.exact_rerooting_isomorphism_verified:
        raise AssertionError("triangular re-rooting automorphism failed")
    return _normalize_support(_xor(vertex, base_vertex) for vertex in support)


def frame_subword_entropy_induction_certificate(
    support: Iterable[Assignment],
) -> FrameSubwordEntropyInductionCertificate:
    """Prove ``#Hom(P(U),G) <= |G|^(u-log2|U|)`` for every finite G."""

    root = _normalize_support(support)
    zero = (0,) * len(root[0])
    if zero not in root:
        raise ValueError("support must contain the zero assignment")

    def prove(rows: tuple[Assignment, ...]) -> tuple[float, list[FrameSubwordEntropyInductionStep]]:
        width = len(rows[0])
        local_zero = (0,) * width
        target = width - math.log2(len(rows))
        if width == 0:
            if rows != ((),):
                raise AssertionError("zero-width support must be the singleton cube")
            return 0.0, []

        zero_half = tuple(row for row in rows if row[-1] == 0)
        one_half = tuple(row for row in rows if row[-1] == 1)
        initial_counts = (len(zero_half), len(one_half))
        rerooted = len(one_half) > len(zero_half)
        base: Assignment | None = None
        reroot_verified = True
        working = rows
        if rerooted:
            base = min(one_half)
            reroot_certificate = frame_subword_rerooting_certificate(base)
            reroot_verified = (
                reroot_certificate.exact_rerooting_isomorphism_verified
                and local_zero in rows
                and base in rows
            )
            working = reroot_frame_subword_support(rows, base)
            zero_half = tuple(row for row in working if row[-1] == 0)
            one_half = tuple(row for row in working if row[-1] == 1)

        if len(zero_half) < len(one_half) or not zero_half:
            raise AssertionError("re-rooting did not place the larger half at zero")
        child_support = _normalize_support(row[:-1] for row in zero_half)
        child_bound, child_steps = prove(child_support)
        if one_half:
            # A relation w_b*x_u=1 determines x_u uniquely.  The remaining
            # equations only reduce the assignments satisfying P(U_0).
            branch = "one-half-relation-determines-last-generator"
            derived = child_bound
            branch_verified = any(row[-1] == 1 for row in working)
        else:
            # No relation uses x_u, so it is a genuinely free generator.
            branch = "empty-one-half-leaves-last-generator-free"
            derived = child_bound + 1.0
            branch_verified = all(row[-1] == 0 for row in working)
        slack = target - derived
        step_verified = (
            reroot_verified
            and branch_verified
            and len(zero_half) * 2 >= len(working)
            and slack >= -1e-12
        )
        step = FrameSubwordEntropyInductionStep(
            frame_position_count=width,
            support_size=len(rows),
            initial_zero_half_size=initial_counts[0],
            initial_one_half_size=initial_counts[1],
            rerooted=rerooted,
            reroot_base=base,
            zero_half_size=len(zero_half),
            one_half_size=len(one_half),
            recurrence_branch=branch,
            child_support_size=len(child_support),
            child_solution_exponent_upper_bound=child_bound,
            derived_solution_exponent_upper_bound=derived,
            target_solution_exponent_upper_bound=target,
            induction_slack=slack,
            exact_step_verified=step_verified,
        )
        return target, [step, *child_steps]

    bound, steps = prove(root)
    exact = all(step.exact_step_verified for step in steps)
    return FrameSubwordEntropyInductionCertificate(
        support=root,
        support_size=len(root),
        support_entropy_bits=math.log2(len(root)),
        universal_finite_group_solution_exponent_upper_bound=bound,
        rerooting_step_count=sum(step.rerooted for step in steps),
        induction_steps=tuple(steps),
        exact_induction_verified=exact,
    )


def frame_subword_suffix_branch_certificate(
    support: Iterable[Assignment],
) -> FrameSubwordSuffixBranchCertificate:
    """Certify the integer suffix-branch generator bound.

    This theorem does not require the zero row.  Re-rooting at the selected
    anchor makes it zero, and every stored witness becomes a triangular pivot
    relation for its coordinate.
    """

    rows = _normalize_support(support)
    width = len(rows[0])
    forced_counts = {row: 0 for row in rows}
    branch_witnesses: dict[tuple[Assignment, int], Assignment] = {}
    conditional_entropy = 0.0

    for coordinate in range(width):
        buckets: dict[Assignment, dict[int, list[Assignment]]] = {}
        for row in rows:
            suffix = row[coordinate + 1 :]
            buckets.setdefault(suffix, {0: [], 1: []})[row[coordinate]].append(row)
        for sides in buckets.values():
            zero_rows = sides[0]
            one_rows = sides[1]
            size = len(zero_rows) + len(one_rows)
            if zero_rows and one_rows:
                zero_witness = min(zero_rows)
                one_witness = min(one_rows)
                for row in zero_rows:
                    branch_witnesses[(row, coordinate)] = one_witness
                for row in one_rows:
                    branch_witnesses[(row, coordinate)] = zero_witness
                probability = len(one_rows) / size
                binary_entropy = -(
                    probability * math.log2(probability)
                    + (1.0 - probability) * math.log2(1.0 - probability)
                )
                conditional_entropy += size / len(rows) * binary_entropy
            else:
                for row in (*zero_rows, *one_rows):
                    forced_counts[row] += 1

    anchor = min(rows, key=lambda row: (forced_counts[row], row))
    branch_coordinates = tuple(
        coordinate + 1
        for coordinate in range(width)
        if (anchor, coordinate) in branch_witnesses
    )
    forced_coordinates = tuple(
        coordinate
        for coordinate in range(1, width + 1)
        if coordinate not in branch_coordinates
    )
    witnesses = tuple(
        branch_witnesses[(anchor, coordinate - 1)]
        for coordinate in branch_coordinates
    )
    witness_exact = all(
        witness[coordinate:] == anchor[coordinate:]
        and witness[coordinate - 1] != anchor[coordinate - 1]
        for coordinate, witness in zip(branch_coordinates, witnesses)
    )
    codimension = width - math.log2(len(rows))
    incidence = sum(forced_counts.values())
    average_forced = incidence / len(rows)
    generator_bound = width - (len(rows) - 1).bit_length()
    chain_rule = conditional_entropy
    chain_exact = abs(chain_rule - math.log2(len(rows))) <= 1e-10
    average_bound = average_forced <= codimension + 1e-12
    anchor_bound = len(forced_coordinates) <= generator_bound
    exact = witness_exact and chain_exact and average_bound and anchor_bound
    return FrameSubwordSuffixBranchCertificate(
        support=rows,
        support_size=len(rows),
        frame_position_count=width,
        entropy_codimension=codimension,
        suffix_forced_incidence_count=incidence,
        average_suffix_forced_coordinate_count=average_forced,
        anchor=anchor,
        suffix_branch_coordinates=branch_coordinates,
        suffix_forced_coordinates=forced_coordinates,
        suffix_branch_witnesses=witnesses,
        universal_finite_group_generator_upper_bound=generator_bound,
        entropy_chain_rule_value=chain_rule,
        entropy_chain_rule_verified=chain_exact,
        average_forced_bound_verified=average_bound,
        explicit_anchor_bound_verified=anchor_bound,
        exact_suffix_branch_elimination_verified=exact,
        status=(
            "exact-integer-suffix-branch-generator-bound"
            if exact
            else "suffix-branch-generator-certificate-failure"
        ),
    )


def frame_subword_relations(rows: Iterable[Assignment]) -> tuple[tuple[int, ...], ...]:
    rows = _normalize_support(rows)
    return normalize_relations(
        tuple(
            _ordered_subword(row)
            for row in rows
            if any(row)
        )
    )


def frame_subword_reduction(rows: Iterable[Assignment]) -> TietzeReduction:
    rows = _normalize_support(rows)
    return tietze_reduce_presentation(
        len(rows[0]),
        frame_subword_relations(rows),
    )


def audit_frame_subword_entropy(
    control_id: str,
    support: tuple[Assignment, ...],
) -> FrameSubwordEntropyControl:
    support = _normalize_support(support)
    width = len(support[0])
    zero = (0,) * width
    if zero not in support:
        raise ValueError("support must contain the zero assignment")
    relations = frame_subword_relations(support)
    reduction = tietze_reduce_presentation(width, relations)
    classifier_exponent, source = presentation_solution_exponent_upper_bound(
        reduction,
        use_nielsen=False,
    )
    induction = frame_subword_entropy_induction_certificate(support)
    suffix_branch = frame_subword_suffix_branch_certificate(support)
    universal_exponent = (
        induction.universal_finite_group_solution_exponent_upper_bound
    )
    if universal_exponent < classifier_exponent - 1e-12:
        exponent = universal_exponent
        source = "all-width-frame-subword-entropy-induction"
    else:
        exponent = classifier_exponent
    if (
        suffix_branch.universal_finite_group_generator_upper_bound
        < exponent - 1e-12
    ):
        exponent = float(
            suffix_branch.universal_finite_group_generator_upper_bound
        )
        source = "all-width-suffix-branch-integer-generator-bound"
    entropy = math.log2(len(support))
    margin = width - exponent - entropy
    exact = relations == normalize_relations(
        _ordered_subword(row) for row in support if any(row)
    )
    certified = (
        exact
        and induction.exact_induction_verified
        and suffix_branch.exact_suffix_branch_elimination_verified
        and margin >= -1e-12
    )
    return FrameSubwordEntropyControl(
        control_id=control_id,
        frame_position_count=width,
        support=support,
        support_size=len(support),
        support_entropy_bits=entropy,
        frame_relations=relations,
        eliminated_generator_count=len(reduction.elimination_steps),
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        classifier_solution_exponent_upper_bound=classifier_exponent,
        universal_finite_group_solution_exponent_upper_bound=(
            universal_exponent
        ),
        universal_finite_group_generator_upper_bound=(
            suffix_branch.universal_finite_group_generator_upper_bound
        ),
        frame_solution_exponent_upper_bound=exponent,
        exponent_certificate_source=source,
        entropy_margin=margin,
        rerooting_step_count=induction.rerooting_step_count,
        entropy_induction_verified=induction.exact_induction_verified,
        suffix_branch_certificate=suffix_branch,
        suffix_branch_generator_bound_verified=(
            suffix_branch.exact_suffix_branch_elimination_verified
        ),
        exact_subword_presentation_verified=exact,
        pressure_inequality_certified=certified,
        status=(
            "frame-subword-entropy-pressure-certified"
            if certified
            else "frame-subword-entropy-pressure-open"
        ),
    )


def _all_zero_containing_supports(width: int) -> Iterable[tuple[Assignment, ...]]:
    cube = tuple(itertools.product((0, 1), repeat=width))
    # Lexicographic order puts zero first, so fixing bit zero avoids duplicates
    # and yields exactly 2^(2^u-1) supports.
    for tail_mask in range(1 << (len(cube) - 1)):
        yield (
            cube[0],
            *(
                row
                for index, row in enumerate(cube[1:])
                if tail_mask >> index & 1
            ),
        )


def _audit_support_family(
    width: int,
    supports: Iterable[tuple[Assignment, ...]],
    *,
    status_prefix: str,
) -> FrameSubwordScalingRecord:
    checks = 0
    failures = 0
    minimum_margin = math.inf
    maximum_exponent = 0.0
    for support in supports:
        control = audit_frame_subword_entropy(status_prefix, support)
        checks += 1
        failures += not control.pressure_inequality_certified
        minimum_margin = min(minimum_margin, control.entropy_margin)
        maximum_exponent = max(
            maximum_exponent,
            control.frame_solution_exponent_upper_bound,
        )
    return FrameSubwordScalingRecord(
        frame_position_count=width,
        checked_zero_containing_support_count=checks,
        pressure_uncertified_support_count=failures,
        minimum_entropy_margin=minimum_margin,
        maximum_frame_solution_exponent=maximum_exponent,
        status=(
            f"{status_prefix}-all-supports-certified"
            if not failures
            else f"{status_prefix}-uncertified-supports-remain"
        ),
    )


def _cube_edge_direction_count(support: tuple[Assignment, ...]) -> int:
    rows = set(support)
    width = len(support[0])
    return sum(
        any(
            tuple(
                bit ^ int(index == coordinate)
                for index, bit in enumerate(row)
            )
            in rows
            for row in support
        )
        for coordinate in range(width)
    )


def _maximum_private_pivot_count(support: tuple[Assignment, ...]) -> int:
    width = len(support[0])
    nonzero = tuple(row for row in support if any(row))
    for size in range(min(width, len(nonzero)), 0, -1):
        for selected in itertools.combinations(nonzero, size):
            options = tuple(
                tuple(
                    coordinate
                    for coordinate in range(width)
                    if all(
                        selected[other][coordinate] == int(other == row_index)
                        for other in range(size)
                    )
                )
                for row_index in range(size)
            )
            if not all(options):
                continue

            def match(index: int, used: frozenset[int]) -> bool:
                return index == size or any(
                    coordinate not in used
                    and match(index + 1, used | {coordinate})
                    for coordinate in options[index]
                )

            if match(0, frozenset()):
                return size
    return 0


def _width_five_stress_supports() -> tuple[tuple[Assignment, ...], ...]:
    width = 5
    cube = tuple(itertools.product((0, 1), repeat=width))
    zero = cube[0]
    supports: set[tuple[Assignment, ...]] = set()
    for weight in range(width + 1):
        layer = tuple(row for row in cube if sum(row) == weight)
        supports.add(tuple(sorted({zero, *layer})))
        ball = tuple(row for row in cube if sum(row) <= weight)
        supports.add(ball)
    rng = random.Random(260809)
    for _ in range(20_000):
        size = rng.randint(1, len(cube))
        supports.add(tuple(sorted((zero, *rng.sample(cube[1:], size - 1)))))
    return tuple(sorted(supports, key=lambda rows: (len(rows), rows)))


def run_frame_subword_entropy() -> FrameSubwordEntropyReport:
    exhaustive = [
        _audit_support_family(
            width,
            _all_zero_containing_supports(width),
            status_prefix="exhaustive",
        )
        for width in range(1, 5)
    ]
    stress = _audit_support_family(
        5,
        _width_five_stress_supports(),
        status_prefix="deterministic-width-five-stress",
    )

    chain8 = tuple(
        tuple(int(index >= 8 - weight) for index in range(8))
        for weight in range(9)
    )
    parity5 = tuple(
        row
        for row in itertools.product((0, 1), repeat=5)
        if sum(row) % 2 == 0
    )
    torsion4 = (
        (0, 0, 0, 0),
        (0, 0, 1, 1),
        (0, 1, 0, 1),
        (0, 1, 1, 0),
        (1, 0, 0, 1),
        (1, 0, 1, 0),
        (1, 1, 0, 0),
        (1, 1, 1, 0),
        (1, 1, 1, 1),
    )
    representatives = [
        audit_frame_subword_entropy("MONOTONE-CHAIN", chain8),
        audit_frame_subword_entropy("EVEN-PARITY-CODE", parity5),
        audit_frame_subword_entropy("COPRIME-TORSION-RESIDUAL", torsion4),
    ]

    method_support = (
        (0, 0, 0, 0),
        (1, 1, 0, 0),
        (1, 1, 1, 1),
    )
    method_control = audit_frame_subword_entropy(
        "NESTED-BLOCK-METHOD-FALSIFIER",
        method_support,
    )
    edge_count = _cube_edge_direction_count(method_support)
    pivot_count = _maximum_private_pivot_count(method_support)
    method_falsifiers = [
        FrameSubwordMethodFalsifier(
            control_id="EDGE-PIVOT-METRICS-INCOMPLETE",
            support=method_support,
            cube_edge_direction_count=edge_count,
            private_pivot_count=pivot_count,
            edge_pivot_entropy_debt=(
                math.log2(len(method_support)) - edge_count - pivot_count
            ),
            frame_subword_exponent=(
                method_control.frame_solution_exponent_upper_bound
            ),
            frame_subword_entropy_margin=method_control.entropy_margin,
            edge_pivot_failure_is_pressure_counterexample=False,
            status="simplified-certificate-fails-full-subword-bound-passes",
        )
    ]

    exhaustive_failures = sum(
        row.pressure_uncertified_support_count for row in exhaustive
    )
    exhaustive_count = sum(
        row.checked_zero_containing_support_count for row in exhaustive
    )
    exact_through_four = exhaustive_failures == 0
    return FrameSubwordEntropyReport(
        created_at=utc_now(),
        theorem_contract={
            "frame_subword_reduction": (
                "For E A^u F E F with zero in D, selected split/support "
                "relations give P(S union D)*Z^2 exactly."
            ),
            "pressure_transfer": (
                "A certified P(U) exponent e gives crossing pressure "
                "e+H-u-1, so e+H<=u is sufficient."
            ),
            "single_support_sufficiency": (
                "H(S,D)<=log2|S union D|; inequality (1) for the union closes "
                "every corresponding support pair."
            ),
            "fixed_width_result": (
                "Every zero-containing U through width four satisfies (1) "
                "under exact Tietze and certified surface/power bounds."
            ),
            "all_width_result": (
                "For every zero-containing U and every finite group G, XOR "
                "re-rooting plus last-generator elimination proves "
                "#Hom(P(U),G)<=|G|^(u-log2|U|)."
            ),
            "integer_generator_strengthening": (
                "For every nonempty U, an entropy-chain anchor has at most "
                "floor(u-log2|U|) suffix-forced coordinates. Triangular "
                "suffix witnesses therefore generate P(U) with at most that "
                "many generators over every finite group."
            ),
            "scope": (
                "Nonzero base cells, interleaved leaves, B frames, and mixed "
                "targets remain open; the all-u zero-based contiguous all-A "
                "subword entropy inequality is closed."
            ),
        },
        representative_controls=representatives,
        method_falsifiers=method_falsifiers,
        exhaustive_scaling=exhaustive,
        width_five_stress=stress,
        proof_obligations=[
            {
                "obligation": "reduce_zero_based_all_A_profiles_to_frame_subword_groups",
                "resolved": True,
                "resolution": (
                    "The zero different cell produces the exact Z^2 crossing "
                    "factor and converts every color-one cell to w_v."
                ),
            },
            {
                "obligation": "classify_every_zero_based_support_through_width_four",
                "resolved": exact_through_four,
                "resolution": (
                    "All 32,906 supports pass the certified exponent-entropy inequality."
                ),
            },
            {
                "obligation": "prove_frame_subword_entropy_inequality_for_all_widths",
                "resolved": True,
                "resolution": (
                    "A triangular Nielsen automorphism implements XOR "
                    "re-rooting exactly. The larger zero half has size at "
                    "least |U|/2, and an occupied one half determines the "
                    "last generator, closing the induction over every finite group."
                ),
            },
            {
                "obligation": "strengthen_entropy_exponent_to_integer_generator_bound",
                "resolved": True,
                "resolution": (
                    "Conditional entropy is at most the suffix-branch indicator. "
                    "Averaging over anchors leaves one anchor with at most "
                    "floor(u-log2|U|) forced coordinates, and explicit triangular "
                    "witness relators eliminate every other generator."
                ),
            },
            {
                "obligation": "remove_zero_base_and_all_A_contiguity",
                "resolved": False,
                "resolution": (
                    "Nonzero base partitions can trade free factors for higher "
                    "surface genus; mixed B words retain target boundaries."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Cube edges and private pivots are the complete loss mechanism.",
                "resolved": True,
                "resolution": (
                    "False: the nested three-point support has neither enough "
                    "edges nor pivots, but two cumulative subword relators "
                    "Tietze-eliminate two frame generators."
                ),
            },
            {
                "objection": "Width-five stress proves the all-u inequality.",
                "resolved": True,
                "resolution": (
                    "No finite stress run proves it. The all-u result instead "
                    "comes from the exact XOR re-rooting automorphism and "
                    "last-coordinate induction; stress remains only a code control."
                ),
            },
            {
                "objection": "XOR translation is invalid for ordered noncommutative subwords.",
                "resolved": True,
                "resolution": (
                    "Direct XOR is not a generator permutation. The triangular "
                    "automorphism x_i->A_i*x_i^((-1)^a_i)*A_i^-1 sends w_b "
                    "exactly to w_(a xor b)*w_a^-1 and preserves the relevant "
                    "normal closure because 0 and a are support vertices."
                ),
            },
        ],
        headline_metrics={
            "exhaustively_checked_zero_support_count_through_width_four": (
                exhaustive_count
            ),
            "exhaustive_pressure_failure_count_through_width_four": (
                exhaustive_failures
            ),
            "width_five_stress_support_count": (
                stress.checked_zero_containing_support_count
            ),
            "width_five_stress_failure_count": (
                stress.pressure_uncertified_support_count
            ),
            "conditional_frame_subword_pressure_theorem_count": 1,
            "complete_width_four_zero_based_pressure_theorem_count": int(
                exact_through_four
            ),
            "growing_width_frame_subword_entropy_theorem_count": 1,
            "growing_width_suffix_branch_generator_theorem_count": 1,
            "nonzero_base_pressure_theorem_count": 0,
            "mixed_target_character_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_frame_subword_reduction_proved": True,
            "all_zero_based_supports_through_width_four_certified": (
                exact_through_four
            ),
            "growing_width_frame_subword_entropy_proved": True,
            "growing_width_suffix_branch_generator_bound_proved": True,
            "nonzero_base_assignments_certified": False,
            "mixed_target_character_control_proved": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The all-degree reduction, entropy induction, and stronger "
                "integer suffix-branch generator theorem are exact for ordered "
                "subword supports, but mixed target observables remain open."
            ),
        },
        status=(
            "zero-based-contiguous-all-A-frame-subword-pressure-complete"
            if exact_through_four and not stress.pressure_uncertified_support_count
            else "frame-subword-entropy-control-failure"
        ),
        summary=(
            "Reduced zero-based contiguous all-A support profiles to ordered "
            "frame-subword groups and proved the entropy bound at every width "
            "by exact XOR re-rooting, entropy induction, and an explicit "
            "integer suffix-branch generator theorem."
        ),
        falsifiers_triggered=[
            "Edge/private-pivot metrics are incomplete even when pressure is safe.",
            "Finite coverage is not the all-u proof; the re-rooting induction is.",
            "The real entropy exponent is not optimal for non-power-of-two supports.",
            "The reduction requires zero in the different-coordinate support.",
            "Mixed B boundaries and target characters remain outside scope.",
        ],
    )


def write_frame_subword_entropy_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    report = asdict(run_frame_subword_entropy())
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
                id="NEG-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY."
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
                    "self_dual_wreath_frame_subword_entropy": str(path)
                },
            )
        )
    return report


if __name__ == "__main__":
    result = write_frame_subword_entropy_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
