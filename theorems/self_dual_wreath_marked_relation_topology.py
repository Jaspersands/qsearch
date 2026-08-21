"""Relation-topology compression for leaf-marked Green word moments.

The leaf-marked word normal form contains powers

    Q_0(x)^r0 Q_1(x)^r1,

where each ``Q`` counts assignments to the ``u`` unmarked frame positions of
one source coordinate.  Expanding these powers naively introduces
``2^(u(r0+r1))`` coordinate assignments.  The equations imposed by repeated
assignment types are duplicates, so the expansion has an exact support
compression.

Let ``Omega={0,1}^u`` and let ``onto(r,s)`` be the number of onto maps from an
``r``-element ordered set to an ``s``-element set.  For every group tuple,

    Q(x)^r = sum_(S subset Omega) onto(r,|S|)
                 1[all assignment constraints in S hold],               (1)

with the empty-support term interpreted as one only when ``r=0``.  Therefore
the pair ``Q_0^r0 Q_1^r1`` depends on two support subsets of ``Omega``.  For
fixed marked-word degree this removes all growth with the copy count.  The
remaining profile count is at most ``2^(2^(u+1))``; this is still prohibitive
when the Green approximant degree ``u`` grows.

Every support profile defines a finite group presentation.  There is one
generator ``x_t`` per trace-word position.  The final split contributes the
ordered products on left- and right-child positions, and every assignment in
the two supports contributes its two color-product relations.  Elementary
Tietze elimination of a generator occurring once in a relator preserves the
solution set over every finite group.

For the uncompressed pair words this automatically recovers the topology:

* ``EEFF`` reduces to two free generators and no relation, giving ``g^2``
  solutions;
* ``EFEF`` reduces to two generators with one commutator relation, giving
  ``g p(n)`` solutions for ``S_n``.

Their difference is exactly the carrier trace formula already proved.  The
new point is architectural: polynomial Green terms can now be classified by
support-profile presentations instead of source-coordinate sequences.

For zero, one, and two frame tokens, every support profile now has a certified
leading ``log_|S_n|`` pressure upper bound.  The two-token proof does not need
to classify all residual groups: dropping relators, surface-word formulas,
explicit free-basis commutators, primitive-power cycle counts, and one exact
centralized-torsion presentation suffice.
Bounded Nielsen certificates also kill the first four entropy-heavy
degree-three obstructions found by the deterministic probe.

This module does not exhaust all degree-three profiles, classify the profiles
produced by growing-degree Green approximants, control mixed target character
observables, or prove a positive component moment.  A finite pressure screen
is not an asymptotic word-rigidity theorem.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import deque
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_leaf_marked_green_word_normal_form import _validate_pattern
from self_dual_wreath_sibling_word_map_normal_form import _compose


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_marked_relation_topology.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
SignedWord = tuple[int, ...]
Assignment = tuple[int, ...]


@dataclass(frozen=True)
class TietzeStep:
    eliminated_generator: int
    solving_relation: SignedWord
    replacement_word: SignedWord
    remaining_relation_count: int


@dataclass(frozen=True)
class TietzeReduction:
    initial_generator_count: int
    initial_relation_count: int
    remaining_generators: tuple[int, ...]
    free_generator_count: int
    residual_relations: tuple[SignedWord, ...]
    elimination_steps: tuple[TietzeStep, ...]
    residual_topology: str
    orientable_surface_genus: int | None
    nonorientable_surface_genus: int | None
    classified_solution_exponent: float | None


@dataclass(frozen=True)
class FreeBasisCommutatorCertificate:
    relation: SignedWord
    generators: tuple[int, ...]
    left_factor: SignedWord
    right_factor: SignedWord
    basis_complement: tuple[SignedWord, ...]
    inverse_basis_words: tuple[SignedWord, ...]
    exact_commutator_identity_verified: bool
    exact_free_basis_verified: bool


@dataclass(frozen=True)
class PowerConjugacyCertificate:
    relation: SignedWord
    power_generator: int
    conjugator_generator: int
    left_power: int
    right_power: int
    unit_power_present: bool
    exact_cyclic_factorization_verified: bool


@dataclass(frozen=True)
class CentralizedPrimitivePowerCertificate:
    power_generator: int
    pure_power_degree: int
    pure_power_relation_index: int
    central_generator: int
    free_product_generator: int
    power_centralizer_relation_indices: tuple[int, ...]
    central_commutator_relation_indices: tuple[int, ...]
    relations_modulo_power: tuple[SignedWord, ...]
    relations_modulo_power_and_power_centralizer: tuple[SignedWord, ...]
    exact_presentation_equivalence_verified: bool
    symmetric_group_root_exponent: float
    symmetric_group_solution_exponent: float


@dataclass(frozen=True)
class PurePowerGcdCollapseCertificate:
    power_generator: int
    pure_power_relation_indices: tuple[int, ...]
    pure_power_degrees: tuple[int, ...]
    power_degree_gcd: int
    relations_after_forced_identity: tuple[SignedWord, ...]
    exact_forced_identity_verified: bool


@dataclass(frozen=True)
class WhiteheadMove:
    multiplier: int
    subset: tuple[int, ...]
    generator_images: tuple[SignedWord, ...]
    inverse_basis_words: tuple[SignedWord, ...]
    transformed_relation: SignedWord


@dataclass(frozen=True)
class WhiteheadPrimitiveCertificate:
    relation: SignedWord
    generators: tuple[int, ...]
    moves: tuple[WhiteheadMove, ...]
    transformed_relation: SignedWord
    exact_automorphism_chain_verified: bool


@dataclass(frozen=True)
class WhiteheadOneRelatorCertificate:
    relation: SignedWord
    generators: tuple[int, ...]
    moves: tuple[WhiteheadMove, ...]
    transformed_relation: SignedWord
    primitive_generator_relation: bool
    orientable_surface_genus: int | None
    nonorientable_surface_genus: int | None
    primitive_power_degree: int | None
    exact_automorphism_chain_verified: bool


@dataclass(frozen=True)
class NielsenMove:
    target_generator: int
    replacement_word: SignedWord
    transformed_relation: SignedWord


@dataclass(frozen=True)
class NielsenOneRelatorCertificate:
    relation: SignedWord
    generators: tuple[int, ...]
    transformed_relation: SignedWord
    moves: tuple[NielsenMove, ...]
    orientable_surface_genus: int | None
    nonorientable_surface_genus: int | None
    primitive_power_degree: int | None
    exact_automorphism_chain_verified: bool


@dataclass(frozen=True)
class SupportExpansionControl:
    frame_position_count: int
    assignment_type_count: int
    maximum_coordinate_power: int
    checked_valid_assignment_counts: int
    maximum_identity_residual: int
    exact_support_profile_expansion_verified: bool
    status: str


@dataclass(frozen=True)
class RelationTopologyControl:
    control_id: str
    pattern: str
    same_assignment_support: tuple[Assignment, ...]
    different_assignment_support: tuple[Assignment, ...]
    initial_generator_count: int
    initial_relations: tuple[SignedWord, ...]
    eliminated_generator_count: int
    remaining_generators: tuple[int, ...]
    free_generator_count: int
    residual_relations: tuple[SignedWord, ...]
    residual_topology: str
    orientable_surface_genus: int | None
    nonorientable_surface_genus: int | None
    classified_solution_exponent: float | None
    symmetric_group_degree: int
    initial_presentation_solution_count: int
    reduced_presentation_solution_count: int
    expected_solution_count: int | None
    exact_solution_preservation_verified: bool
    expected_topology_verified: bool
    status: str


@dataclass(frozen=True)
class RelationTopologyScalingRecord:
    n: int
    selected_copy_count: int
    remaining_source_coordinate_count: int
    frame_position_count: int
    assignment_type_count: int
    log2_raw_coordinate_assignment_terms: int
    log2_support_profile_upper_bound: int
    support_profile_bound_independent_of_copy_count: bool
    fixed_degree_copy_depth_growth_removed: bool
    growing_degree_profile_classification_proved: bool
    status: str


@dataclass(frozen=True)
class FixedDegreePressureControl:
    frame_position_count: int
    marked_word_placement_count: int
    assignment_type_count: int
    total_support_profile_count: int
    classified_support_profile_count: int
    unclassified_support_profile_count: int
    pressure_certified_support_profile_count: int
    pressure_uncertified_support_profile_count: int
    single_relator_surface_bound_profile_count: int
    nielsen_surface_bound_profile_count: int
    primitive_power_bound_profile_count: int
    free_basis_commutator_bound_profile_count: int
    maximum_noncrossing_rescaled_pressure: float
    maximum_crossing_rescaled_pressure: float
    expected_noncrossing_pressure: float
    expected_crossing_pressure: float
    every_profile_topologically_classified: bool
    every_profile_pressure_certified: bool
    expected_pressure_separation_verified: bool
    finite_degree_only: bool
    status: str


@dataclass(frozen=True)
class AdversarialPressureControl:
    control_id: str
    frame_position_count: int
    pattern: str
    crossing: bool
    same_assignment_support: tuple[Assignment, ...]
    different_assignment_support: tuple[Assignment, ...]
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    trivial_solution_exponent: float
    trivial_rescaled_pressure: float
    certified_solution_exponent_upper_bound: float
    exponent_certificate_source: str
    certified_rescaled_pressure_upper_bound: float
    required_pressure_upper_bound: float
    exact_certificate_verified: bool
    status: str


@dataclass(frozen=True)
class MarkedRelationTopologyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    support_expansion_controls: list[SupportExpansionControl]
    relation_topology_controls: list[RelationTopologyControl]
    fixed_degree_pressure_controls: list[FixedDegreePressureControl]
    adversarial_pressure_controls: list[AdversarialPressureControl]
    scaling_records: list[RelationTopologyScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def onto_function_count(domain_size: int, image_size: int) -> int:
    """Return the number of onto functions ``[domain_size] -> [image_size]``."""

    if domain_size < 0 or image_size < 0:
        raise ValueError("set sizes must be nonnegative")
    if domain_size == 0:
        return int(image_size == 0)
    if image_size == 0 or image_size > domain_size:
        return 0
    return sum(
        (-1) ** (image_size - retained)
        * math.comb(image_size, retained)
        * retained**domain_size
        for retained in range(image_size + 1)
    )


def support_expansion_sum(
    valid_assignment_count: int,
    coordinate_power: int,
) -> int:
    """Evaluate the right side of (1) after only the valid types remain."""

    if valid_assignment_count < 0 or coordinate_power < 0:
        raise ValueError("counts must be nonnegative")
    return sum(
        math.comb(valid_assignment_count, support_size)
        * onto_function_count(coordinate_power, support_size)
        for support_size in range(valid_assignment_count + 1)
    )


def audit_support_expansion(
    frame_position_count: int,
    maximum_coordinate_power: int,
) -> SupportExpansionControl:
    if frame_position_count < 0 or maximum_coordinate_power < 0:
        raise ValueError("invalid support-expansion parameters")
    assignment_count = 1 << frame_position_count
    maximum = 0
    checks = 0
    for valid in range(assignment_count + 1):
        for power in range(maximum_coordinate_power + 1):
            expected = valid**power
            actual = support_expansion_sum(valid, power)
            maximum = max(maximum, abs(actual - expected))
            checks += 1
    exact = maximum == 0
    return SupportExpansionControl(
        frame_position_count=frame_position_count,
        assignment_type_count=assignment_count,
        maximum_coordinate_power=maximum_coordinate_power,
        checked_valid_assignment_counts=checks,
        maximum_identity_residual=maximum,
        exact_support_profile_expansion_verified=exact,
        status=(
            "exact-onto-support-profile-expansion-verified"
            if exact
            else "support-profile-expansion-control-failure"
        ),
    )


def inverse_word(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def free_reduce(word: Iterable[int]) -> SignedWord:
    stack: list[int] = []
    for letter in word:
        if not letter:
            raise ValueError("zero is not a signed generator")
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def cyclic_reduce(word: SignedWord) -> SignedWord:
    reduced = list(free_reduce(word))
    while len(reduced) >= 2 and reduced[0] == -reduced[-1]:
        reduced = list(free_reduce(reduced[1:-1]))
    return tuple(reduced)


def canonical_relator(word: SignedWord) -> SignedWord:
    reduced = cyclic_reduce(word)
    if not reduced:
        return ()
    inverse = inverse_word(reduced)
    rotations = tuple(
        reduced[index:] + reduced[:index] for index in range(len(reduced))
    ) + tuple(
        inverse[index:] + inverse[:index] for index in range(len(inverse))
    )
    return min(rotations)


def normalize_relations(relations: Iterable[SignedWord]) -> tuple[SignedWord, ...]:
    return tuple(
        sorted(
            {
                normalized
                for relation in relations
                if (normalized := canonical_relator(relation))
            },
            key=lambda word: (len(word), word),
        )
    )


def _substitute_generator(
    word: SignedWord,
    generator: int,
    replacement: SignedWord,
) -> SignedWord:
    output: list[int] = []
    for letter in word:
        if letter == generator:
            output.extend(replacement)
        elif letter == -generator:
            output.extend(inverse_word(replacement))
        else:
            output.append(letter)
    return free_reduce(output)


def _solve_single_occurrence(
    relation: SignedWord,
    generator: int,
) -> SignedWord:
    occurrences = [
        index for index, letter in enumerate(relation) if abs(letter) == generator
    ]
    if len(occurrences) != 1:
        raise ValueError("generator must occur exactly once in the solving relator")
    index = occurrences[0]
    prefix = relation[:index]
    suffix = relation[index + 1 :]
    if relation[index] == generator:
        return free_reduce((*inverse_word(prefix), *inverse_word(suffix)))
    return free_reduce((*suffix, *prefix))


def _is_single_commutator_relation(
    relations: tuple[SignedWord, ...],
    remaining_generators: tuple[int, ...],
) -> bool:
    if len(relations) != 1:
        return False
    relation = cyclic_reduce(relations[0])
    if len(relation) != 4:
        return False
    generators = {abs(letter) for letter in relation}
    if len(generators) != 2 or not generators.issubset(remaining_generators):
        return False
    for generator in generators:
        signs = [
            1 if letter > 0 else -1
            for letter in relation
            if abs(letter) == generator
        ]
        if sorted(signs) != [-1, 1]:
            return False
    return abs(relation[0]) == abs(relation[2]) and abs(relation[1]) == abs(
        relation[3]
    )


def orientable_quadratic_genus(relation: SignedWord) -> int | None:
    """Return the genus of an orientable quadratic cyclic relator.

    Every active generator must occur exactly twice with opposite signs.  The
    polygon-edge pairing then has Euler characteristic ``V-E+1`` and genus
    ``(1+E-V)/2``.
    """

    word = cyclic_reduce(relation)
    generators = sorted({abs(letter) for letter in word})
    if len(word) != 2 * len(generators) or not generators:
        return None
    occurrences: dict[int, list[int]] = {generator: [] for generator in generators}
    for index, letter in enumerate(word):
        occurrences[abs(letter)].append(index)
    for generator, positions in occurrences.items():
        if len(positions) != 2:
            return None
        if sorted(1 if word[index] > 0 else -1 for index in positions) != [-1, 1]:
            return None

    parent = list(range(len(word)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    size = len(word)
    for generator, positions in occurrences.items():
        positive = next(index for index in positions if word[index] == generator)
        negative = next(index for index in positions if word[index] == -generator)
        union(positive, (negative + 1) % size)
        union((positive + 1) % size, negative)
    vertex_count = len({find(index) for index in range(size)})
    numerator = 1 + len(generators) - vertex_count
    if numerator < 0 or numerator % 2:
        return None
    return numerator // 2


def nonorientable_quadratic_genus(relation: SignedWord) -> int | None:
    """Return the crosscap number of a nonorientable quadratic relator."""

    word = cyclic_reduce(relation)
    generators = sorted({abs(letter) for letter in word})
    if len(word) != 2 * len(generators) or not generators:
        return None
    occurrences: dict[int, list[int]] = {generator: [] for generator in generators}
    for index, letter in enumerate(word):
        occurrences[abs(letter)].append(index)
    if any(len(positions) != 2 for positions in occurrences.values()):
        return None
    # If every pair has opposite signs, the surface is orientable and belongs
    # to orientable_quadratic_genus instead.
    if all(
        word[positions[0]] == -word[positions[1]]
        for positions in occurrences.values()
    ):
        return None

    parent = list(range(len(word)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    size = len(word)
    for positions in occurrences.values():
        left, right = positions
        if word[left] == -word[right]:
            positive = left if word[left] > 0 else right
            negative = right if word[left] > 0 else left
            union(positive, (negative + 1) % size)
            union((positive + 1) % size, negative)
        else:
            union(left, right)
            union((left + 1) % size, (right + 1) % size)
    vertex_count = len({find(index) for index in range(size)})
    crosscap = 1 + len(generators) - vertex_count
    return crosscap if crosscap >= 1 else None


@lru_cache(maxsize=None)
def _reduced_words(
    generators: tuple[int, ...],
    maximum_length: int,
) -> tuple[SignedWord, ...]:
    words: list[SignedWord] = []
    signed = tuple(generators) + tuple(-generator for generator in generators)
    frontier: list[SignedWord] = [()]
    for _ in range(maximum_length):
        next_frontier: list[SignedWord] = []
        for prefix in frontier:
            for letter in signed:
                if prefix and prefix[-1] == -letter:
                    continue
                word = (*prefix, letter)
                words.append(word)
                next_frontier.append(word)
        frontier = next_frontier
    return tuple(words)


def _substitute_word_images(
    word: SignedWord,
    images: dict[int, SignedWord],
) -> SignedWord:
    output: list[int] = []
    for letter in word:
        image = images[abs(letter)]
        output.extend(image if letter > 0 else inverse_word(image))
    return free_reduce(output)


def primitive_power_degree(relation: SignedWord) -> int | None:
    """Return ``k`` when the cyclic relator is literally ``x^k``."""

    word = cyclic_reduce(relation)
    if len(word) < 2 or any(letter != word[0] for letter in word[1:]):
        return None
    return len(word)


def power_conjugacy_certificate(
    relation: SignedWord,
) -> PowerConjugacyCertificate | None:
    """Recognize ``y x^a y^-1 x^b`` with ``|a|=1`` or ``|b|=1``.

    The equation says that ``x`` is conjugate to a fixed nonzero power of
    itself.  In ``S_n`` this forces every cycle length of ``x`` to be coprime
    to that power.  For each admissible conjugacy class there are exactly
    ``|S_n|`` pairs ``(x,y)``, so the pair count is
    ``|S_n| p_allowed(n)=|S_n|^(1+o(1))``.
    """

    word = cyclic_reduce(relation)
    generators = sorted({abs(letter) for letter in word})
    if len(generators) != 2:
        return None
    variants = []
    for base in (word, inverse_word(word)):
        variants.extend(base[index:] + base[:index] for index in range(len(base)))
    for power_generator in generators:
        conjugator = next(
            generator for generator in generators if generator != power_generator
        )
        for variant in variants:
            if abs(variant[0]) != conjugator:
                continue
            conjugator_positions = [
                index
                for index, letter in enumerate(variant)
                if abs(letter) == conjugator
            ]
            if len(conjugator_positions) != 2 or conjugator_positions[0] != 0:
                continue
            split = conjugator_positions[1]
            if variant[split] != -variant[0]:
                continue
            left = variant[1:split]
            right = variant[split + 1 :]
            if not left or not right:
                continue
            if any(abs(letter) != power_generator for letter in (*left, *right)):
                continue
            if len({1 if letter > 0 else -1 for letter in left}) != 1:
                continue
            if len({1 if letter > 0 else -1 for letter in right}) != 1:
                continue
            left_power = sum(1 if letter > 0 else -1 for letter in left)
            right_power = sum(1 if letter > 0 else -1 for letter in right)
            if min(abs(left_power), abs(right_power)) != 1:
                continue
            return PowerConjugacyCertificate(
                relation=canonical_relator(relation),
                power_generator=power_generator,
                conjugator_generator=conjugator,
                left_power=left_power,
                right_power=right_power,
                unit_power_present=True,
                exact_cyclic_factorization_verified=True,
            )
    return None


def _power_centralizer_normal_form(
    word: SignedWord,
    power_generator: int,
    degree: int,
    central_generator: int | None = None,
) -> SignedWord:
    """Normal form in ``(C_degree x Z) * F`` (or ``C_degree * F``).

    The optional central generator spans the infinite cyclic factor commuting
    with the finite-order generator.  Every other generator belongs to the
    free factor.  Alternating factor normal forms make the reduction exact,
    including cancellations that expose two previously separated blocks.
    """

    if degree < 2:
        raise ValueError("degree must be at least two")
    if central_generator == power_generator:
        raise ValueError("central and power generators must differ")

    # Stack entries are (factor, value), where H is represented by
    # (central exponent, power residue) and F by a freely reduced word.
    stack: list[tuple[str, tuple[int, int] | SignedWord]] = []

    def combine(
        factor: str,
        left: tuple[int, int] | SignedWord,
        right: tuple[int, int] | SignedWord,
    ) -> tuple[int, int] | SignedWord:
        if factor == "H":
            left_central, left_power = left
            right_central, right_power = right
            return (
                left_central + right_central,
                (left_power + right_power) % degree,
            )
        return free_reduce((*left, *right))

    def is_identity(factor: str, value: tuple[int, int] | SignedWord) -> bool:
        return value == (0, 0) if factor == "H" else not value

    def push(factor: str, value: tuple[int, int] | SignedWord) -> None:
        if is_identity(factor, value):
            return
        if stack and stack[-1][0] == factor:
            _, previous = stack.pop()
            push(factor, combine(factor, previous, value))
            return
        stack.append((factor, value))

    for letter in word:
        generator = abs(letter)
        sign = 1 if letter > 0 else -1
        if generator == power_generator:
            push("H", (0, sign % degree))
        elif central_generator is not None and generator == central_generator:
            push("H", (sign, 0))
        else:
            push("F", (letter,))

    output: list[int] = []
    for factor, value in stack:
        if factor == "F":
            output.extend(value)
            continue
        central_exponent, power_residue = value
        if central_exponent:
            assert central_generator is not None
            output.extend(
                (central_generator if central_exponent > 0 else -central_generator,)
                * abs(central_exponent)
            )
        if power_residue > degree // 2:
            power_residue -= degree
        if power_residue:
            output.extend(
                (power_generator if power_residue > 0 else -power_generator,)
                * abs(power_residue)
            )
    return tuple(output)


def _rank_two_commutator(first: int, second: int) -> SignedWord:
    return canonical_relator((-first, -second, first, second))


def centralized_primitive_power_certificate(
    relations: tuple[SignedWord, ...],
) -> CentralizedPrimitivePowerCertificate | None:
    """Recognize ``<x,y,z | x^k,[x,z],[y,z]>`` exactly.

    This is ``(C_k * Z) x Z``.  For every finite group ``G`` its homomorphism
    count is

        |G| sum_[z] |{x in C_G(z): x^k=1}|,

    where the sum is over conjugacy classes.  In ``S_n`` the number of
    ``k``-torsion elements is ``|S_n|^(1-1/k+o(1))`` and the partition count
    is subexponential, so the three-generator solution exponent is
    ``2-1/k``.  Extra unused generators each add one exponent.
    """

    for pure_index, pure_relation in enumerate(relations):
        degree = primitive_power_degree(pure_relation)
        if degree is None:
            continue
        power_generator = abs(cyclic_reduce(pure_relation)[0])
        modulo_power = tuple(
            canonical_relator(
                _power_centralizer_normal_form(
                    relation,
                    power_generator,
                    degree,
                )
            )
            for relation in relations
        )
        other_generators = sorted(
            {
                abs(letter)
                for relation in modulo_power
                for letter in relation
                if abs(letter) != power_generator
            }
        )
        for central_generator in other_generators:
            power_commutator = _rank_two_commutator(
                power_generator,
                central_generator,
            )
            power_centralizer_indices = tuple(
                index + 1
                for index, relation in enumerate(modulo_power)
                if relation == power_commutator
            )
            if not power_centralizer_indices:
                continue
            modulo_centralizer = tuple(
                canonical_relator(
                    _power_centralizer_normal_form(
                        relation,
                        power_generator,
                        degree,
                        central_generator,
                    )
                )
                for relation in relations
            )
            nontrivial = tuple(
                (index, relation)
                for index, relation in enumerate(modulo_centralizer)
                if relation
            )
            if not nontrivial:
                continue
            candidate_generators = {
                generator
                for _, relation in nontrivial
                for generator in {abs(letter) for letter in relation}
                if generator != central_generator
            }
            for free_generator in sorted(candidate_generators):
                central_commutator = _rank_two_commutator(
                    free_generator,
                    central_generator,
                )
                if any(
                    relation != central_commutator
                    for _, relation in nontrivial
                ):
                    continue
                central_indices = tuple(index + 1 for index, _ in nontrivial)
                return CentralizedPrimitivePowerCertificate(
                    power_generator=power_generator,
                    pure_power_degree=degree,
                    pure_power_relation_index=pure_index + 1,
                    central_generator=central_generator,
                    free_product_generator=free_generator,
                    power_centralizer_relation_indices=(
                        power_centralizer_indices
                    ),
                    central_commutator_relation_indices=central_indices,
                    relations_modulo_power=modulo_power,
                    relations_modulo_power_and_power_centralizer=(
                        modulo_centralizer
                    ),
                    exact_presentation_equivalence_verified=True,
                    symmetric_group_root_exponent=1.0 - 1.0 / degree,
                    symmetric_group_solution_exponent=2.0 - 1.0 / degree,
                )
    return None


def pure_power_gcd_collapse_certificate(
    relations: tuple[SignedWord, ...],
) -> PurePowerGcdCollapseCertificate | None:
    """Certify ``x=1`` from literal powers whose degrees have gcd one.

    If the presentation contains ``x^a=1`` for every degree in a set with
    gcd one, Bezout's identity forces ``x=1`` in every group.  This detector
    deliberately accepts only literal one-generator power relators; it does
    not infer powers from equal-context or sign-sensitive relations.
    """

    generators = sorted(
        {abs(letter) for relation in relations for letter in relation}
    )
    for generator in generators:
        indexed_degrees = tuple(
            (index, degree)
            for index, relation in enumerate(relations)
            if (degree := primitive_power_degree(relation)) is not None
            and {abs(letter) for letter in cyclic_reduce(relation)} == {generator}
        )
        if len(indexed_degrees) < 2:
            continue
        degree_gcd = math.gcd(*(degree for _, degree in indexed_degrees))
        if degree_gcd != 1:
            continue
        substituted = normalize_relations(
            _substitute_generator(relation, generator, ())
            for relation in relations
        )
        return PurePowerGcdCollapseCertificate(
            power_generator=generator,
            pure_power_relation_indices=tuple(
                index + 1 for index, _ in indexed_degrees
            ),
            pure_power_degrees=tuple(degree for _, degree in indexed_degrees),
            power_degree_gcd=degree_gcd,
            relations_after_forced_identity=substituted,
            exact_forced_identity_verified=True,
        )
    return None


def _one_relator_signature(
    relation: SignedWord,
) -> tuple[int | None, int | None, int | None]:
    orientable = orientable_quadratic_genus(relation)
    nonorientable = nonorientable_quadratic_genus(relation)
    power = primitive_power_degree(relation)
    if orientable is not None and orientable < 1:
        orientable = None
    return orientable, nonorientable, power


def _apply_nielsen_replacement(
    relation: SignedWord,
    generators: tuple[int, ...],
    target_generator: int,
    replacement_word: SignedWord,
) -> SignedWord:
    images = {
        generator: (
            replacement_word if generator == target_generator else (generator,)
        )
        for generator in generators
    }
    return canonical_relator(_substitute_word_images(relation, images))


@lru_cache(maxsize=None)
def bounded_nielsen_one_relator_certificate(
    relation: SignedWord,
    generators: tuple[int, ...],
    maximum_states: int = 20_000,
) -> NielsenOneRelatorCertificate | None:
    """Search a non-length-increasing Nielsen orbit for a known relator.

    Every move replaces one free generator by its left or right product with
    a different signed generator.  This is an explicit free-group
    automorphism.  The search is only a certificate finder: failure to find a
    path has no mathematical meaning.
    """

    generators = tuple(sorted(generators))
    start = canonical_relator(relation)
    queue: deque[SignedWord] = deque([start])
    predecessor: dict[SignedWord, SignedWord | None] = {start: None}
    incoming: dict[SignedWord, NielsenMove] = {}
    while queue and len(predecessor) <= maximum_states:
        current = queue.popleft()
        orientable, nonorientable, power = _one_relator_signature(current)
        if orientable is not None or nonorientable is not None or power is not None:
            moves: list[NielsenMove] = []
            cursor = current
            while predecessor[cursor] is not None:
                moves.append(incoming[cursor])
                cursor = predecessor[cursor]  # type: ignore[assignment]
            moves.reverse()
            replay = start
            for move in moves:
                replay = _apply_nielsen_replacement(
                    replay,
                    generators,
                    move.target_generator,
                    move.replacement_word,
                )
            return NielsenOneRelatorCertificate(
                relation=start,
                generators=generators,
                transformed_relation=current,
                moves=tuple(moves),
                orientable_surface_genus=orientable,
                nonorientable_surface_genus=nonorientable,
                primitive_power_degree=power,
                exact_automorphism_chain_verified=replay == current,
            )
        for target in generators:
            for helper in generators:
                if helper == target:
                    continue
                for signed_helper in (helper, -helper):
                    for replacement in (
                        (target, signed_helper),
                        (signed_helper, target),
                    ):
                        transformed = _apply_nielsen_replacement(
                            current,
                            generators,
                            target,
                            replacement,
                        )
                        if len(transformed) > len(start) or transformed in predecessor:
                            continue
                        predecessor[transformed] = current
                        incoming[transformed] = NielsenMove(
                            target_generator=target,
                            replacement_word=replacement,
                            transformed_relation=transformed,
                        )
                        queue.append(transformed)
    return None


def _free_basis_inverse_words(
    generators: tuple[int, ...],
    images: tuple[SignedWord, ...],
    maximum_inverse_length: int,
) -> tuple[SignedWord, ...] | None:
    """Certify that ``images`` are a free basis by constructing its inverse."""

    if len(generators) != len(images):
        return None
    abstract = tuple(range(1, len(images) + 1))
    new_to_old = dict(zip(abstract, images))
    inverse_by_old: dict[int, SignedWord] = {}
    for candidate in _reduced_words(abstract, maximum_inverse_length):
        value = _substitute_word_images(candidate, new_to_old)
        if len(value) == 1 and value[0] in generators:
            inverse_by_old.setdefault(value[0], candidate)
        if len(inverse_by_old) == len(generators):
            break
    if len(inverse_by_old) != len(generators):
        return None
    old_to_new = {
        generator: inverse_by_old[generator] for generator in generators
    }
    inverse_tuple = tuple(old_to_new[generator] for generator in generators)
    if any(
        _substitute_word_images(word, new_to_old) != (generator,)
        for generator, word in zip(generators, inverse_tuple)
    ):
        return None
    if any(
        _substitute_word_images(image, old_to_new) != (index,)
        for index, image in enumerate(images, start=1)
    ):
        return None
    return inverse_tuple


def _whitehead_images(
    generators: tuple[int, ...],
    multiplier: int,
    subset: set[int],
) -> tuple[SignedWord, ...]:
    images: list[SignedWord] = []
    for generator in generators:
        if generator == abs(multiplier):
            image = (generator,)
        elif generator in subset and -generator not in subset:
            image = (generator, multiplier)
        elif generator not in subset and -generator in subset:
            image = (-multiplier, generator)
        elif generator in subset and -generator in subset:
            image = (-multiplier, generator, multiplier)
        else:
            image = (generator,)
        images.append(free_reduce(image))
    return tuple(images)


@lru_cache(maxsize=None)
def whitehead_one_relator_certificate(
    relation: SignedWord,
    generators: tuple[int, ...],
    maximum_rank: int = 6,
) -> WhiteheadOneRelatorCertificate | None:
    """Minimize a relator and certify a primitive, surface, or power form.

    Each selected move is verified independently by constructing a two-sided
    inverse basis map.  Failure to reach a recognized minimum has no
    mathematical meaning.
    """

    generators = tuple(sorted(generators))
    if not generators or len(generators) > maximum_rank:
        return None
    start = canonical_relator(relation)
    current = start
    signed = tuple(generators) + tuple(-generator for generator in generators)
    moves: list[WhiteheadMove] = []
    while len(current) > 1:
        best: tuple[int, int, tuple[int, ...], tuple[SignedWord, ...], SignedWord] | None = None
        for multiplier in signed:
            optional = tuple(
                letter for letter in signed if letter not in (multiplier, -multiplier)
            )
            for mask in range(1 << len(optional)):
                subset = {multiplier}
                subset.update(
                    letter
                    for index, letter in enumerate(optional)
                    if mask >> index & 1
                )
                images = _whitehead_images(generators, multiplier, subset)
                image_map = dict(zip(generators, images))
                transformed = canonical_relator(
                    _substitute_word_images(current, image_map)
                )
                if len(transformed) >= len(current):
                    continue
                candidate = (
                    len(transformed),
                    multiplier,
                    tuple(sorted(subset)),
                    images,
                    transformed,
                )
                if best is None or candidate < best:
                    best = candidate
        if best is None:
            break
        _, multiplier, subset_tuple, images, transformed = best
        inverse_basis = _free_basis_inverse_words(
            generators,
            images,
            maximum_inverse_length=4,
        )
        if inverse_basis is None:
            raise AssertionError("Whitehead generator images failed basis verification")
        moves.append(
            WhiteheadMove(
                multiplier=multiplier,
                subset=subset_tuple,
                generator_images=images,
                inverse_basis_words=inverse_basis,
                transformed_relation=transformed,
            )
        )
        current = transformed
    replay = start
    for move in moves:
        replay = canonical_relator(
            _substitute_word_images(
                replay,
                dict(zip(generators, move.generator_images)),
            )
        )
    primitive = len(current) == 1
    orientable = orientable_quadratic_genus(current)
    if orientable is not None and orientable < 1:
        orientable = None
    nonorientable = nonorientable_quadratic_genus(current)
    power = primitive_power_degree(current)
    if not primitive and orientable is None and nonorientable is None and power is None:
        return None
    return WhiteheadOneRelatorCertificate(
        relation=start,
        generators=generators,
        moves=tuple(moves),
        transformed_relation=current,
        primitive_generator_relation=primitive,
        orientable_surface_genus=orientable,
        nonorientable_surface_genus=nonorientable,
        primitive_power_degree=power,
        exact_automorphism_chain_verified=(
            replay == current
        ),
    )


@lru_cache(maxsize=None)
def whitehead_primitive_certificate(
    relation: SignedWord,
    generators: tuple[int, ...],
    maximum_rank: int = 6,
) -> WhiteheadPrimitiveCertificate | None:
    certificate = whitehead_one_relator_certificate(
        relation,
        generators,
        maximum_rank,
    )
    if certificate is None or not certificate.primitive_generator_relation:
        return None
    return WhiteheadPrimitiveCertificate(
        relation=certificate.relation,
        generators=certificate.generators,
        moves=certificate.moves,
        transformed_relation=certificate.transformed_relation,
        exact_automorphism_chain_verified=(
            certificate.exact_automorphism_chain_verified
        ),
    )


def _commutator_word(left: SignedWord, right: SignedWord) -> SignedWord:
    return canonical_relator(
        (*inverse_word(left), *inverse_word(right), *left, *right)
    )


@lru_cache(maxsize=None)
def free_basis_commutator_certificate(
    relation: SignedWord,
    generators: tuple[int, ...],
    maximum_factor_length: int = 3,
    maximum_inverse_length: int = 4,
) -> FreeBasisCommutatorCertificate | None:
    """Find an exact automorphic commutator certificate for one relator.

    The returned factors, followed by the singleton complement, are verified
    to be a free basis by an explicit two-sided inverse word map.  Hence the
    equation has exactly ``g^(r-2)`` times the number of commuting pairs over
    every finite group of order ``g``.
    """

    generators = tuple(sorted(generators))
    if len(generators) < 2:
        return None
    target = canonical_relator(relation)
    factors = _reduced_words(generators, maximum_factor_length)
    complement_size = len(generators) - 2
    complements = tuple(itertools.combinations(generators, complement_size))
    for left in factors:
        for right in factors:
            if _commutator_word(left, right) != target:
                continue
            for complement_generators in complements:
                complement = tuple((generator,) for generator in complement_generators)
                images = (left, right, *complement)
                inverse_basis = _free_basis_inverse_words(
                    generators,
                    images,
                    maximum_inverse_length,
                )
                if inverse_basis is None:
                    continue
                return FreeBasisCommutatorCertificate(
                    relation=target,
                    generators=generators,
                    left_factor=left,
                    right_factor=right,
                    basis_complement=complement,
                    inverse_basis_words=inverse_basis,
                    exact_commutator_identity_verified=(
                        _commutator_word(left, right) == target
                    ),
                    exact_free_basis_verified=True,
                )
    return None


def presentation_solution_exponent_upper_bound(
    reduction: TietzeReduction,
    *,
    stop_at: float | None = None,
    use_free_basis_commutator: bool = True,
    use_nielsen: bool = True,
    maximum_nielsen_states: int = 20_000,
) -> tuple[float, str]:
    """Certify the leading ``log_|S_n|`` exponent using one relator.

    Dropping all but one residual equation only enlarges the solution set.
    Orientable surface words cost one group exponent.  A nonorientable
    crosscap-one word costs one half exponent via the involution asymptotic;
    higher crosscap costs one.  An automorphic commutator also costs one.
    Partition-number and Witten-zeta factors are ``|S_n|^o(1)`` and are not
    included in this leading exponent.
    """

    generator_count = len(reduction.remaining_generators)
    best = float(generator_count)
    source = "trivial-assignment-bound"
    if stop_at is not None and best <= stop_at + 1e-12:
        return best, source
    power_gcd = pure_power_gcd_collapse_certificate(
        reduction.residual_relations
    )
    if power_gcd is not None:
        best = float(generator_count - 1)
        source = "multi-relator-coprime-pure-power-collapse"
        if stop_at is not None and best <= stop_at + 1e-12:
            return best, source
    centralized_power = centralized_primitive_power_certificate(
        reduction.residual_relations
    )
    if centralized_power is not None:
        best = float(
            generator_count
            - 3
            + centralized_power.symmetric_group_solution_exponent
        )
        source = (
            "multi-relator-centralized-primitive-power-degree-"
            f"{centralized_power.pure_power_degree}"
        )
        if stop_at is not None and best <= stop_at + 1e-12:
            return best, source
    for relation in reduction.residual_relations:
        orientable_genus = orientable_quadratic_genus(relation)
        if orientable_genus is not None and orientable_genus >= 1:
            candidate = float(generator_count - 1)
            if candidate < best:
                best = candidate
                source = f"single-orientable-surface-genus-{orientable_genus}"
            if stop_at is not None and best <= stop_at + 1e-12:
                return best, source
            continue
        nonorientable_genus = nonorientable_quadratic_genus(relation)
        if nonorientable_genus is not None:
            loss = 0.5 if nonorientable_genus == 1 else 1.0
            candidate = generator_count - loss
            if candidate < best:
                best = candidate
                source = (
                    f"single-nonorientable-surface-genus-{nonorientable_genus}"
                )
            if stop_at is not None and best <= stop_at + 1e-12:
                return best, source
            continue
        power_conjugacy = power_conjugacy_certificate(relation)
        if power_conjugacy is not None:
            candidate = float(generator_count - 1)
            if candidate < best:
                nonunit = max(
                    abs(power_conjugacy.left_power),
                    abs(power_conjugacy.right_power),
                )
                best = candidate
                source = f"single-unit-power-conjugacy-degree-{nonunit}"
            if stop_at is not None and best <= stop_at + 1e-12:
                return best, source
            continue
        power_degree = primitive_power_degree(relation)
        if power_degree is not None:
            candidate = generator_count - 1.0 / power_degree
            if candidate < best:
                best = candidate
                source = f"single-primitive-power-degree-{power_degree}"
            if stop_at is not None and best <= stop_at + 1e-12:
                return best, source
            continue
        if use_free_basis_commutator and best > generator_count - 1:
            certificate = free_basis_commutator_certificate(
                relation,
                reduction.remaining_generators,
            )
            if certificate is not None:
                best = float(generator_count - 1)
                source = "single-free-basis-commutator"
                if stop_at is not None and best <= stop_at + 1e-12:
                    return best, source
                continue
        if best > generator_count - 1:
            whitehead = whitehead_one_relator_certificate(
                relation,
                reduction.remaining_generators,
            )
            if whitehead is not None:
                if whitehead.primitive_generator_relation:
                    loss = 1.0
                    label = "single-whitehead-primitive"
                elif whitehead.orientable_surface_genus is not None:
                    loss = 1.0
                    label = (
                        "whitehead-orientable-surface-genus-"
                        f"{whitehead.orientable_surface_genus}"
                    )
                elif whitehead.nonorientable_surface_genus is not None:
                    genus = whitehead.nonorientable_surface_genus
                    loss = 0.5 if genus == 1 else 1.0
                    label = f"whitehead-nonorientable-surface-genus-{genus}"
                else:
                    degree = whitehead.primitive_power_degree
                    if degree is None:
                        raise AssertionError("Whitehead certificate has no known form")
                    loss = 1.0 / degree
                    label = f"whitehead-primitive-power-degree-{degree}"
                best = generator_count - loss
                source = label
                if stop_at is not None and best <= stop_at + 1e-12:
                    return best, source
                continue
        nielsen = (
            bounded_nielsen_one_relator_certificate(
                relation,
                reduction.remaining_generators,
                maximum_nielsen_states,
            )
            if use_nielsen
            else None
        )
        if nielsen is not None:
            if nielsen.orientable_surface_genus is not None:
                loss = 1.0
                label = (
                    "nielsen-orientable-surface-genus-"
                    f"{nielsen.orientable_surface_genus}"
                )
            elif nielsen.nonorientable_surface_genus is not None:
                genus = nielsen.nonorientable_surface_genus
                loss = 0.5 if genus == 1 else 1.0
                label = f"nielsen-nonorientable-surface-genus-{genus}"
            else:
                degree = nielsen.primitive_power_degree
                if degree is None:
                    raise AssertionError("Nielsen certificate has no known topology")
                loss = 1.0 / degree
                label = f"nielsen-primitive-power-degree-{degree}"
            candidate = generator_count - loss
            if candidate < best:
                best = candidate
                source = label
            if stop_at is not None and best <= stop_at + 1e-12:
                return best, source
            if best <= generator_count - 1:
                continue
    return best, source


def tietze_reduce_presentation(
    generator_count: int,
    relations: Iterable[SignedWord],
) -> TietzeReduction:
    """Eliminate generators that occur once in one relator.

    Each step is an exact Tietze move: assignments of the remaining
    generators satisfying the substituted relations extend uniquely to the
    eliminated generator over every group.
    """

    if generator_count < 0:
        raise ValueError("generator count must be nonnegative")
    current = normalize_relations(relations)
    initial_count = len(current)
    remaining = set(range(1, generator_count + 1))
    steps: list[TietzeStep] = []
    while True:
        choice: tuple[int, int, SignedWord] | None = None
        for relation_index, relation in enumerate(current):
            for generator in sorted({abs(letter) for letter in relation}):
                if sum(abs(letter) == generator for letter in relation) == 1:
                    choice = relation_index, generator, relation
                    break
            if choice is not None:
                break
        if choice is None:
            break
        relation_index, generator, solving = choice
        replacement = _solve_single_occurrence(solving, generator)
        substituted = [
            _substitute_generator(relation, generator, replacement)
            for index, relation in enumerate(current)
            if index != relation_index
        ]
        current = normalize_relations(substituted)
        remaining.remove(generator)
        steps.append(
            TietzeStep(
                eliminated_generator=generator,
                solving_relation=solving,
                replacement_word=replacement,
                remaining_relation_count=len(current),
            )
        )
    active = {abs(letter) for relation in current for letter in relation}
    free_count = len(remaining - active)
    remaining_tuple = tuple(sorted(remaining))
    surface_genus: int | None = None
    nonorientable_genus: int | None = None
    solution_exponent: float | None = None
    if not current:
        topology = "free-group"
        solution_exponent = free_count
    elif _is_single_commutator_relation(current, remaining_tuple):
        topology = "rank-two-torus-commutator"
        surface_genus = 1
        active_count = len({abs(letter) for letter in current[0]})
        solution_exponent = free_count + active_count - 1
    elif len(current) == 1 and (
        surface_genus := orientable_quadratic_genus(current[0])
    ) is not None:
        topology = f"orientable-surface-genus-{surface_genus}"
        active_count = len({abs(letter) for letter in current[0]})
        solution_exponent = free_count + active_count - 1
    elif len(current) == 1 and (
        nonorientable_genus := nonorientable_quadratic_genus(current[0])
    ) is not None:
        topology = f"nonorientable-surface-genus-{nonorientable_genus}"
        active_count = len({abs(letter) for letter in current[0]})
        # Frobenius--Schur gives g^(r-1) sum d^(2-h).  For S_n the h=1
        # sum of dimensions is the involution count g^(1/2+o(1)); h>=2
        # contributes only g^o(1).
        solution_exponent = (
            free_count
            + active_count
            - 1
            + (0.5 if nonorientable_genus == 1 else 0.0)
        )
    else:
        topology = "residual-word-system"
    return TietzeReduction(
        initial_generator_count=generator_count,
        initial_relation_count=initial_count,
        remaining_generators=remaining_tuple,
        free_generator_count=free_count,
        residual_relations=current,
        elimination_steps=tuple(steps),
        residual_topology=topology,
        orientable_surface_genus=surface_genus,
        nonorientable_surface_genus=nonorientable_genus,
        classified_solution_exponent=solution_exponent,
    )


def frame_assignments(pattern: str) -> tuple[Assignment, ...]:
    _validate_pattern(pattern)
    frame_count = sum(token in "AB" for token in pattern)
    return tuple(itertools.product((0, 1), repeat=frame_count))


def _coordinate_bits(
    pattern: str,
    assignment: Assignment,
    differing_coordinate: bool,
) -> tuple[int, ...]:
    frame_count = sum(token in "AB" for token in pattern)
    if len(assignment) != frame_count or any(bit not in (0, 1) for bit in assignment):
        raise ValueError("assignment must specify every frame-token bit")
    iterator = iter(assignment)
    return tuple(
        next(iterator)
        if token in "AB"
        else (1 if token == "F" and differing_coordinate else 0)
        for token in pattern
    )


def _relations_from_bits(bits: tuple[int, ...]) -> tuple[SignedWord, ...]:
    return tuple(
        tuple(index + 1 for index, value in enumerate(bits) if value == bit)
        for bit in (0, 1)
        if any(value == bit for value in bits)
    )


def marked_support_presentation(
    pattern: str,
    same_assignment_support: Iterable[Assignment],
    different_assignment_support: Iterable[Assignment],
) -> tuple[SignedWord, ...]:
    """Build the split and nonsplit relation union for one support profile."""

    _validate_pattern(pattern)
    split_bits = tuple(1 if token == "B" else 0 for token in pattern)
    relations: list[SignedWord] = list(_relations_from_bits(split_bits))
    for assignment in same_assignment_support:
        relations.extend(
            _relations_from_bits(
                _coordinate_bits(pattern, assignment, False)
            )
        )
    for assignment in different_assignment_support:
        relations.extend(
            _relations_from_bits(
                _coordinate_bits(pattern, assignment, True)
            )
        )
    return normalize_relations(relations)


def _compose_general(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _evaluate_signed_word(
    word: SignedWord,
    assignment: dict[int, Permutation],
) -> Permutation:
    identity = tuple(range(len(next(iter(assignment.values())))))
    output = identity
    for letter in word:
        value = assignment[abs(letter)]
        if letter < 0:
            value = _inverse_permutation(value)
        output = _compose_general(output, value)
    return output


def presentation_solution_count(
    n: int,
    generators: Iterable[int],
    relations: Iterable[SignedWord],
) -> int:
    generator_tuple = tuple(sorted(generators))
    relation_tuple = tuple(relations)
    if n < 2:
        raise ValueError("n must be at least two")
    group = tuple(itertools.permutations(range(n)))
    identity = tuple(range(n))
    if not generator_tuple:
        return int(all(not relation for relation in relation_tuple))
    count = 0
    for values in itertools.product(group, repeat=len(generator_tuple)):
        assignment = dict(zip(generator_tuple, values))
        count += all(
            _evaluate_signed_word(relation, assignment) == identity
            for relation in relation_tuple
        )
    return count


def audit_relation_topology(
    control_id: str,
    pattern: str,
    same_assignment_support: tuple[Assignment, ...],
    different_assignment_support: tuple[Assignment, ...],
    *,
    symmetric_group_degree: int = 3,
    expected_solution_count: int | None = None,
    expected_topology: str | None = None,
) -> RelationTopologyControl:
    relations = marked_support_presentation(
        pattern,
        same_assignment_support,
        different_assignment_support,
    )
    reduction = tietze_reduce_presentation(len(pattern), relations)
    initial_count = presentation_solution_count(
        symmetric_group_degree,
        range(1, len(pattern) + 1),
        relations,
    )
    reduced_count = presentation_solution_count(
        symmetric_group_degree,
        reduction.remaining_generators,
        reduction.residual_relations,
    )
    preserved = initial_count == reduced_count
    topology_ok = expected_topology is None or reduction.residual_topology == expected_topology
    count_ok = expected_solution_count is None or initial_count == expected_solution_count
    exact = preserved and topology_ok and count_ok
    return RelationTopologyControl(
        control_id=control_id,
        pattern=pattern,
        same_assignment_support=same_assignment_support,
        different_assignment_support=different_assignment_support,
        initial_generator_count=len(pattern),
        initial_relations=relations,
        eliminated_generator_count=len(reduction.elimination_steps),
        remaining_generators=reduction.remaining_generators,
        free_generator_count=reduction.free_generator_count,
        residual_relations=reduction.residual_relations,
        residual_topology=reduction.residual_topology,
        orientable_surface_genus=reduction.orientable_surface_genus,
        nonorientable_surface_genus=reduction.nonorientable_surface_genus,
        classified_solution_exponent=reduction.classified_solution_exponent,
        symmetric_group_degree=symmetric_group_degree,
        initial_presentation_solution_count=initial_count,
        reduced_presentation_solution_count=reduced_count,
        expected_solution_count=expected_solution_count,
        exact_solution_preservation_verified=preserved,
        expected_topology_verified=topology_ok and count_ok,
        status=(
            "exact-marked-relation-topology-control-verified"
            if exact
            else "marked-relation-topology-control-failure"
        ),
    )


def relation_topology_scaling_record(
    n: int,
    frame_position_count: int,
) -> RelationTopologyScalingRecord:
    if n < 5 or frame_position_count < 0:
        raise ValueError("invalid scaling parameters")
    order = math.factorial(n)
    copies = (order - 1).bit_length() + 2
    remaining = copies - 1
    assignment_types = 1 << frame_position_count
    return RelationTopologyScalingRecord(
        n=n,
        selected_copy_count=copies,
        remaining_source_coordinate_count=remaining,
        frame_position_count=frame_position_count,
        assignment_type_count=assignment_types,
        log2_raw_coordinate_assignment_terms=frame_position_count * remaining,
        log2_support_profile_upper_bound=2 * assignment_types,
        support_profile_bound_independent_of_copy_count=True,
        fixed_degree_copy_depth_growth_removed=True,
        growing_degree_profile_classification_proved=False,
        status="fixed-degree-copy-growth-compressed-growing-degree-open",
    )


def _weak_compositions(total: int, parts: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        values
        for values in itertools.product(range(total + 1), repeat=parts)
        if sum(values) == total
    )


def _pair_word_pattern(
    powers: tuple[int, int, int, int],
    *,
    crossing: bool,
) -> str:
    leaves = "EFEF" if crossing else "EEFF"
    return "".join(leaf + "A" * power for leaf, power in zip(leaves, powers))


def _nonempty_assignment_supports(pattern: str) -> tuple[tuple[Assignment, ...], ...]:
    assignments = frame_assignments(pattern)
    return tuple(
        tuple(
            assignment
            for index, assignment in enumerate(assignments)
            if mask & (1 << index)
        )
        for mask in range(1, 1 << len(assignments))
    )


def audit_fixed_degree_pressure(
    frame_position_count: int,
) -> FixedDegreePressureControl:
    """Classify the typical-Hamming pressure for one fixed total frame degree."""

    if frame_position_count < 0:
        raise ValueError("frame position count must be nonnegative")
    placements = _weak_compositions(frame_position_count, 4)
    assignment_types = 1 << frame_position_count
    total_profiles = 0
    classified_profiles = 0
    pressure_certified_profiles = 0
    surface_bound_profiles = 0
    nielsen_surface_bound_profiles = 0
    primitive_power_bound_profiles = 0
    commutator_bound_profiles = 0
    maximum = {False: -math.inf, True: -math.inf}
    for powers in placements:
        for crossing in (False, True):
            pattern = _pair_word_pattern(powers, crossing=crossing)
            supports = _nonempty_assignment_supports(pattern)
            for same_support in supports:
                for different_support in supports:
                    total_profiles += 1
                    reduction = tietze_reduce_presentation(
                        len(pattern),
                        marked_support_presentation(
                            pattern,
                            same_support,
                            different_support,
                        ),
                    )
                    exponent = reduction.classified_solution_exponent
                    if exponent is not None:
                        classified_profiles += 1
                    support_entropy = (
                        0.5 * math.log2(len(same_support))
                        + 0.5 * math.log2(len(different_support))
                    )
                    target = -1.0 if crossing else 0.0
                    required_exponent = (
                        target - support_entropy + len(pattern) - 2
                    )
                    exponent_upper_bound, source = (
                        presentation_solution_exponent_upper_bound(
                            reduction,
                            stop_at=required_exponent,
                        )
                    )
                    if source.startswith("nielsen-") and "surface" in source:
                        nielsen_surface_bound_profiles += 1
                    elif "surface" in source:
                        surface_bound_profiles += 1
                    elif "primitive-power" in source:
                        primitive_power_bound_profiles += 1
                    elif source == "single-free-basis-commutator":
                        commutator_bound_profiles += 1
                    pressure = (
                        exponent_upper_bound
                        + support_entropy
                        - len(pattern)
                        + 2
                    )
                    maximum[crossing] = max(maximum[crossing], pressure)
                    pressure_certified_profiles += pressure <= target + 1e-12
    unclassified = total_profiles - classified_profiles
    pressure_uncertified = total_profiles - pressure_certified_profiles
    complete = unclassified == 0
    separation = bool(
        pressure_uncertified == 0
        and abs(maximum[False]) <= 1e-12
        and abs(maximum[True] + 1) <= 1e-12
    )
    return FixedDegreePressureControl(
        frame_position_count=frame_position_count,
        marked_word_placement_count=len(placements),
        assignment_type_count=assignment_types,
        total_support_profile_count=total_profiles,
        classified_support_profile_count=classified_profiles,
        unclassified_support_profile_count=unclassified,
        pressure_certified_support_profile_count=pressure_certified_profiles,
        pressure_uncertified_support_profile_count=pressure_uncertified,
        single_relator_surface_bound_profile_count=surface_bound_profiles,
        nielsen_surface_bound_profile_count=nielsen_surface_bound_profiles,
        primitive_power_bound_profile_count=primitive_power_bound_profiles,
        free_basis_commutator_bound_profile_count=commutator_bound_profiles,
        maximum_noncrossing_rescaled_pressure=maximum[False],
        maximum_crossing_rescaled_pressure=maximum[True],
        expected_noncrossing_pressure=0.0,
        expected_crossing_pressure=-1.0,
        every_profile_topologically_classified=complete,
        every_profile_pressure_certified=pressure_uncertified == 0,
        expected_pressure_separation_verified=separation,
        finite_degree_only=True,
        status=(
            "complete-fixed-degree-certified-pressure-separation"
            if separation
            else "fixed-degree-pressure-has-uncertified-profiles"
        ),
    )


def audit_adversarial_pressure(
    control_id: str,
    pattern: str,
    same_support: tuple[Assignment, ...],
    different_support: tuple[Assignment, ...],
    *,
    crossing: bool,
) -> AdversarialPressureControl:
    """Certify one pressure profile selected to defeat literal classifiers."""

    relations = marked_support_presentation(pattern, same_support, different_support)
    reduction = tietze_reduce_presentation(len(pattern), relations)
    entropy = (
        0.5 * math.log2(len(same_support))
        + 0.5 * math.log2(len(different_support))
    )
    target = -1.0 if crossing else 0.0
    required_exponent = target - entropy + len(pattern) - 2
    trivial_exponent = float(len(reduction.remaining_generators))
    trivial_pressure = trivial_exponent + entropy - len(pattern) + 2
    exponent, source = presentation_solution_exponent_upper_bound(
        reduction,
        stop_at=required_exponent,
    )
    pressure = exponent + entropy - len(pattern) + 2
    if source == "trivial-assignment-bound":
        certificate_verified = True
    elif source == "single-free-basis-commutator":
        certificate_verified = any(
            free_basis_commutator_certificate(
                relation,
                reduction.remaining_generators,
            )
            is not None
            for relation in reduction.residual_relations
        )
    elif source.startswith("nielsen-"):
        certificate_verified = any(
            (certificate := bounded_nielsen_one_relator_certificate(
                relation,
                reduction.remaining_generators,
            ))
            is not None
            and certificate.exact_automorphism_chain_verified
            for relation in reduction.residual_relations
        )
    elif source.startswith("whitehead-") or source == "single-whitehead-primitive":
        certificate_verified = any(
            (certificate := whitehead_one_relator_certificate(
                relation,
                reduction.remaining_generators,
            ))
            is not None
            and certificate.exact_automorphism_chain_verified
            for relation in reduction.residual_relations
        )
    elif source.startswith(
        "multi-relator-centralized-primitive-power-degree-"
    ):
        certificate = centralized_primitive_power_certificate(
            reduction.residual_relations
        )
        certificate_verified = (
            certificate is not None
            and certificate.exact_presentation_equivalence_verified
        )
    elif source == "multi-relator-coprime-pure-power-collapse":
        certificate = pure_power_gcd_collapse_certificate(
            reduction.residual_relations
        )
        certificate_verified = (
            certificate is not None
            and certificate.exact_forced_identity_verified
        )
    else:
        certificate_verified = any(
            orientable_quadratic_genus(relation) is not None
            or nonorientable_quadratic_genus(relation) is not None
            or primitive_power_degree(relation) is not None
            for relation in reduction.residual_relations
        )
    passed = certificate_verified and pressure <= target + 1e-12
    return AdversarialPressureControl(
        control_id=control_id,
        frame_position_count=sum(token in "AB" for token in pattern),
        pattern=pattern,
        crossing=crossing,
        same_assignment_support=same_support,
        different_assignment_support=different_support,
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        trivial_solution_exponent=trivial_exponent,
        trivial_rescaled_pressure=trivial_pressure,
        certified_solution_exponent_upper_bound=exponent,
        exponent_certificate_source=source,
        certified_rescaled_pressure_upper_bound=pressure,
        required_pressure_upper_bound=target,
        exact_certificate_verified=certificate_verified,
        status=(
            "adversarial-profile-pressure-certified"
            if passed
            else "adversarial-profile-pressure-obstruction-open"
        ),
    )


def _degree_three_adversarial_pressure_controls() -> list[AdversarialPressureControl]:
    rows = (
        (
            "DEGREE-THREE-HIDDEN-GENUS-TWO-LEFT",
            "EFEFAAA",
            ((0, 0, 0),),
            ((0, 1, 0), (1, 0, 1)),
        ),
        (
            "DEGREE-THREE-HIDDEN-GENUS-TWO-RIGHT",
            "EFEAAAF",
            ((0, 0, 0),),
            ((1, 0, 1), (1, 1, 0)),
        ),
        (
            "DEGREE-THREE-FREE-BASIS-COMMUTATOR",
            "EAFEAAF",
            ((0, 0, 0),),
            ((1, 0, 1), (1, 1, 0)),
        ),
        (
            "DEGREE-THREE-PRIMITIVE-CUBE",
            "EAFAAEF",
            ((0, 0, 0), (1, 0, 1), (1, 1, 0)),
            ((0, 1, 1), (1, 0, 0)),
        ),
    )
    return [
        audit_adversarial_pressure(
            control_id,
            pattern,
            same_support,
            different_support,
            crossing=True,
        )
        for control_id, pattern, same_support, different_support in rows
    ]


def _topology_controls() -> list[RelationTopologyControl]:
    order = math.factorial(3)
    partitions = 3
    controls = [
        audit_relation_topology(
            "UNCOMPRESSED-NONCROSSING-FREE-PAIR",
            "EEFF",
            (),
            ((),),
            expected_solution_count=order**2,
            expected_topology="free-group",
        ),
        audit_relation_topology(
            "UNCOMPRESSED-CROSSING-COMMUTING-PAIR",
            "EFEF",
            (),
            ((),),
            expected_solution_count=order * partitions,
            expected_topology="rank-two-torus-commutator",
        ),
    ]
    for assignment in frame_assignments("EAFB"):
        controls.append(
            audit_relation_topology(
                "MIXED-EAFB-DIFFERING-" + "".join(map(str, assignment)),
                "EAFB",
                (),
                (assignment,),
            )
        )
    return controls


def run_marked_relation_topology() -> MarkedRelationTopologyReport:
    support_controls = [
        audit_support_expansion(frame_count, 6)
        for frame_count in range(5)
    ]
    topology_controls = _topology_controls()
    pressure_controls = [
        audit_fixed_degree_pressure(frame_count) for frame_count in range(3)
    ]
    adversarial_pressure_controls = _degree_three_adversarial_pressure_controls()
    scaling = [
        relation_topology_scaling_record(n, frame_count)
        for n in (8, 16, 32, 64)
        for frame_count in (2, 4, 8)
    ]
    support_failures = sum(
        not row.exact_support_profile_expansion_verified
        for row in support_controls
    )
    topology_failures = sum(
        not row.exact_solution_preservation_verified
        or not row.expected_topology_verified
        for row in topology_controls
    )
    adversarial_pressure_failures = sum(
        row.status != "adversarial-profile-pressure-certified"
        for row in adversarial_pressure_controls
    )
    exact = support_failures == topology_failures == adversarial_pressure_failures == 0
    noncrossing, crossing = topology_controls[:2]
    return MarkedRelationTopologyReport(
        created_at=utc_now(),
        theorem_contract={
            "support_profile_expansion": (
                "Equation (1) groups source-coordinate assignment sequences "
                "by their exact support with coefficient onto(r,|S|)."
            ),
            "copy_depth_compression": (
                "For u frame positions the two Q powers require at most "
                "2^(2^(u+1)) support profiles, independent of K."
            ),
            "presentation_extraction": (
                "Each support profile gives an exact finite-group presentation "
                "whose relators are the split and two-color ordered products."
            ),
            "tietze_preservation": (
                "Eliminating a generator that occurs once in a relator is a "
                "solution-preserving bijection over every finite group."
            ),
            "uncompressed_topology": (
                "EEFF reduces to a free rank-two presentation; EFEF reduces "
                "to one rank-two commutator relation."
            ),
            "one_relator_pressure_bound": (
                "Dropping residual equations gives a rigorous upper bound. "
                "A retained orientable surface or free-basis commutator "
                "relator loses one leading |S_n| exponent; a projective-plane "
                "relator loses one half via the involution asymptotic."
            ),
            "nielsen_and_power_certificates": (
                "A bounded chain of elementary Nielsen automorphisms can expose "
                "a hidden surface relator without changing its solution count. "
                "A primitive x^k relator costs 1/k of a leading |S_n| exponent, "
                "from the cycle-index count for permutations with cycle lengths "
                "dividing k."
            ),
            "centralized_primitive_power_count": (
                "The residual presentation <x,y,z | x^k,[x,z],[y,z]> is "
                "(C_k * Z) x Z. Its exact finite-group solution count is |G| "
                "times the sum, over conjugacy classes [z], of the k-torsion "
                "count in C_G(z); for S_n its exponent is 2-1/k."
            ),
            "primary_surface_count_reference": "https://arxiv.org/abs/2106.11089",
            "scope": (
                "Growing-degree support-profile classification, mixed target "
                "character sums, positive Green M4, and speedup remain open."
            ),
        },
        support_expansion_controls=support_controls,
        relation_topology_controls=topology_controls,
        fixed_degree_pressure_controls=pressure_controls,
        adversarial_pressure_controls=adversarial_pressure_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_copy_depth_from_fixed_degree_marked_word_expansion",
                "resolved": support_failures == 0,
                "resolution": (
                    "Onto-function coefficients group repeated coordinate "
                    "assignment types exactly by support."
                ),
            },
            {
                "obligation": "extract_and_reduce_group_presentations_for_support_profiles",
                "resolved": topology_failures == 0,
                "resolution": (
                    "The presentation builder and Tietze moves preserve every "
                    "complete S3 solution count in the controls."
                ),
            },
            {
                "obligation": "recover_crossing_commutator_topology",
                "resolved": crossing.residual_topology == "rank-two-torus-commutator",
                "resolution": (
                    "The crossing leaf order leaves one commutator relator and "
                    "therefore g p(n), rather than g^2, S_n solutions."
                ),
            },
            {
                "obligation": "classify_dominant_support_profiles_at_growing_green_degree",
                "resolved": False,
                "resolution": (
                    "The profile bound is independent of K but double exponential "
                    "in u; exploit topology, symmetry, or a transfer matrix as u grows."
                ),
            },
            {
                "obligation": "identify_the_first_fixed_degree_pressure_separation",
                "resolved": pressure_controls[1].expected_pressure_separation_verified,
                "resolution": (
                    "For every placement of zero or one frame token and every "
                    "typical-Hamming support profile, Tietze reduction gives "
                    "noncrossing pressure zero and crossing pressure minus one."
                ),
            },
            {
                "obligation": "certify_two_frame_token_pressure_separation",
                "resolved": pressure_controls[2].expected_pressure_separation_verified,
                "resolution": (
                    "Every two-token profile is bounded by the trivial count, "
                    "one retained surface relator, or an explicitly certified "
                    "free-basis commutator. Exact classification of the full "
                    "116 residual systems is unnecessary for this bound."
                ),
            },
            {
                "obligation": "kill_first_degree_three_literal_classifier_obstructions",
                "resolved": adversarial_pressure_failures == 0,
                "resolution": (
                    "The four entropy-heavy profiles found by the deterministic "
                    "degree-three probe reduce to hidden genus-two, free-basis "
                    "commutator, or an exact centralized primitive-cube "
                    "presentation. This is not an exhaustive degree-three census."
                ),
            },
            {
                "obligation": "bound_mixed_profile_target_character_observables",
                "resolved": False,
                "resolution": (
                    "Track the full-product observable through Tietze elimination "
                    "and prove uniform character suppression or cancellation."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Growing copy count alone makes every fixed-degree marked moment intractable.",
                "resolved": True,
                "resolution": (
                    "False: repeated coordinate types impose duplicate equations; "
                    "the exact support-profile sum is independent of K."
                ),
            },
            {
                "objection": "Abelian relation rank is enough to identify crossing suppression.",
                "resolved": True,
                "resolution": (
                    "False: the EFEF residual has zero abelian obstruction but a "
                    "nontrivial commutator relation detected by free-group reduction."
                ),
            },
            {
                "objection": "Fixed-degree support compression closes the Green problem.",
                "resolved": False,
                "resolution": (
                    "The polynomial degree needed for the exact common projection "
                    "and pseudoinverse grows; the profile alphabet then grows exponentially."
                ),
            },
        ],
        headline_metrics={
            "exact_support_profile_expansion_theorem_count": int(exact),
            "fixed_degree_copy_depth_compression_theorem_count": int(exact),
            "solution_preserving_tietze_reduction_theorem_count": int(exact),
            "uncompressed_noncrossing_free_pair_topology_theorem_count": int(
                noncrossing.residual_topology == "free-group"
            ),
            "uncompressed_crossing_commutator_topology_theorem_count": int(
                crossing.residual_topology == "rank-two-torus-commutator"
            ),
            "support_expansion_control_count": len(support_controls),
            "support_expansion_control_failure_count": support_failures,
            "relation_topology_control_count": len(topology_controls),
            "relation_topology_control_failure_count": topology_failures,
            "fixed_degree_pressure_control_count": len(pressure_controls),
            "one_frame_token_complete_pressure_separation_theorem_count": int(
                pressure_controls[1].expected_pressure_separation_verified
            ),
            "two_frame_token_unclassified_profile_count": (
                pressure_controls[2].unclassified_support_profile_count
            ),
            "two_frame_token_pressure_uncertified_profile_count": (
                pressure_controls[2].pressure_uncertified_support_profile_count
            ),
            "two_frame_token_pressure_separation_theorem_count": int(
                pressure_controls[2].expected_pressure_separation_verified
            ),
            "two_frame_token_free_basis_commutator_certificate_count": (
                pressure_controls[2].free_basis_commutator_bound_profile_count
            ),
            "degree_three_adversarial_pressure_control_count": len(
                adversarial_pressure_controls
            ),
            "degree_three_adversarial_pressure_failure_count": (
                adversarial_pressure_failures
            ),
            "centralized_primitive_cube_presentation_theorem_count": int(
                any(
                    row.exponent_certificate_source
                    == "multi-relator-centralized-primitive-power-degree-3"
                    for row in adversarial_pressure_controls
                )
            ),
            "noncrossing_S3_solution_count": noncrossing.initial_presentation_solution_count,
            "crossing_S3_solution_count": crossing.initial_presentation_solution_count,
            "growing_degree_profile_classification_theorem_count": 0,
            "natural_positive_green_pair_gap_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "fixed_degree_copy_depth_growth_removed": exact,
            "support_profiles_have_exact_group_presentations": exact,
            "tietze_reduction_preserves_finite_group_solution_counts": exact,
            "crossing_commutator_topology_recovered": (
                crossing.residual_topology == "rank-two-torus-commutator"
            ),
            "one_frame_token_pressure_separation_proved": (
                pressure_controls[1].expected_pressure_separation_verified
            ),
            "two_frame_token_pressure_separation_proved": (
                pressure_controls[2].expected_pressure_separation_verified
            ),
            "degree_three_adversarial_obstructions_resolved": (
                adversarial_pressure_failures == 0
            ),
            "degree_three_complete_pressure_separation_proved": False,
            "growing_degree_profile_classification_proved": False,
            "mixed_target_character_control_proved": False,
            "natural_typical_hamming_green_pair_gap_positive": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pressure separation is certified through two frame tokens, "
                "but the Green approximation requires growing degree and a "
                "growing assignment alphabet whose dominant profiles and "
                "target-character observables remain uncontrolled."
            ),
        },
        status=(
            "fixed-degree-marked-topology-compressed-growing-degree-open"
            if exact
            else "marked-relation-topology-control-failure"
        ),
        summary=(
            "Compressed fixed-degree marked moments from source-coordinate "
            "sequences to support-profile group presentations, recovered the "
            "free-versus-commutator crossing topology exactly, and certified "
            "the expected pressure gap for every profile through degree two."
        ),
        falsifiers_triggered=[
            "Copy-depth growth is not the remaining combinatorial bottleneck at fixed marked-word degree.",
            "The crossing correction is nonabelian: abelianized relation rank misses its commutator residual.",
            "Support-profile compression remains double exponential in growing frame-token degree.",
            "The first degree-three literal-classifier failures are hidden surface, commutator, or centralized-torsion presentations, not pressure counterexamples.",
            "Those four degree-three controls are adversarial witnesses, not an exhaustive degree-three theorem.",
            "No positive Green pair gap, component M4, compiler, decoder, or speedup is proved.",
        ],
    )


def write_marked_relation_topology_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_marked_relation_topology())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_marked_relation_topology_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
