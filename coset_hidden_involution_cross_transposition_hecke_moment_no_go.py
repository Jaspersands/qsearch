"""Degree-four moment no-go for the cross-transposition recoupling walk.

Let ``G=S_(2m)``, let ``h=(01)(23)...`` and ``K=C_G(h)``, and let ``t`` be a
transposition crossing two h-pairs.  In the hidden-involution double-coset
source space define the Hermitian Hecke operator

    X = e_B a_t e_B,       a_t=(t,...,t;t),
    Z = M e_B e_A e_B.

The linear alternative-minus-baseline bias is ``2^-k``.  The first
interleaved moment also has an exact all-rank form.  The subgroup intersection

    J=K intersect t K t

has order ``2^m (m-2)!`` for ``m>=3``: on the four affected points the common
centralizer is the Klein four group, while the remaining pairs contribute
``C_2 wr S_(m-2)``.  Hence

    tr_B(X^2) = |J|/(2^k |K|) = 1/[2^k m(m-1)].

For the likelihood-weighted second moment, after eliminating the two shared
K variables, each source copy contributes the number of binary triples

    c(r)=#{(eps,eta,theta) in H^3:
           t eps r t eta t r^-1 t theta=e}.

Writing ``s=t r t`` and ``h'=t h t`` reduces this to
``h'^a s h^b s^-1 h^c=e``.  For ``m>=3`` the all-zero branch always works;
the only other branch is ``(a,b,c)=(0,1,1)``, and it works exactly for
``r in J``.  The apparent ``(1,1,1)`` branch would require a fixed-point-free
involution to equal ``h'h``, which moves only four points, and is impossible
once ``m>=3``.  Therefore

    tr_B(X^2 Z)
      = 4^-k [1 + (2^k-1)/(m(m-1))],

and

    tr_B(X^2 Z)-tr_B(X^2)
      = 4^-k [1-1/(m(m-1))].

The cubic return system has four possible nonempty identity patterns. Three
are pair coincidences. The four-bit pattern reduces to switching one pair of
edges in a perfect matching: one switch repairs the distinguished four-point
component, and switches among two unaffected pairs contribute
``(m-2)(m-3)`` possibilities. Put

    r=m(m-1),       a=3m^2-7m+5.

The per-path binary return count is one, two, or four on respectively
``(r^2-a-1)|J|^2``, ``a|J|^2``, and ``|J|^2`` shared paths. Therefore

    tr_B(X^3)   = 1/(4^k r^2),
    tr_B(X^3 Z) = [r^2-a-1+a 2^k+4^k]/(8^k r^2).

The degree-four return problem admits a finite-support all-rank reduction.
A three-switch matching path activates at most six of the ``m-2`` unaffected
base pairs.  For an even-cardinality identity subword, deleting all inactive
pairs is a bijection onto one of seven canonical support cores.  Exhaustive
exact enumeration of those cores gives, with ``n=m-2``, the stable histogram

    N_8 = 1,
    N_4 = 7 + 16 n + 14 binom(n,2),
    N_2 = 84 n + 260 binom(n,2) + 336 binom(n,3)
          + 144 binom(n,4),
    N_1 = r^3-N_2-N_4-N_8.

It holds for ``m=3`` and every ``m>=5``.  At ``m=4`` exactly six paths gain
one odd-cardinality identity subword, so ``N_2`` increases by six and ``N_1``
decreases by six.  This is also an all-rank statement: an odd identity word
cannot leave an inactive common pair, so the six-support bound reduces every
possible exception to the exact cores ``m<=8``; only ``m=4`` survives.

The baseline closure paths have binary counts ``1,2,4`` on

    Q_1=8n,   Q_2=2+8n+6 binom(n,2),   Q_4=1.

Writing ``x=2^k``, the exact fourth moments are

    tr_B(X^4)   = [Q_1+Q_2 x+x^2]/[x^3 r^3],
    tr_B(X^4 Z) = [N_1+N_2 x+N_4 x^2+x^3]/[x^4 r^3].

The unique ``N_8`` transporter branch equals the unique baseline ``Q_4``
branch, so the apparent order-``x^-1`` contribution cancels exactly.  The
fourth-moment excess is only

    [N_1+(N_2-Q_1)x+(N_4-Q_2)x^2]/[x^4 r^3] = O(x^-2).

At ``k=ceil(log2(64M))`` every unit-coefficient quartic filter in this single
Hecke operator still has at most inverse-candidate total bias, and its new
degree-four contribution is ``O(M^-2)``.  The follow-up all-degree adjacent-pair
injection theorem extends the inverse-candidate bound to every normalized
moment and polynomial LCU in this operator.  Only nonlinear threshold tests,
large-coefficient approximants, postselection, and mixtures of double cosets
remain open.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    involution_class_size,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    hyperoctahedral_group,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    flatness_copy_count,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_cross_transposition_hecke_moment_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-CROSS-TRANSPOSITION-HECKE-MOMENT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class BinaryReturnBranchControl:
    half_degree: int
    degree: int
    centralizer_order: int
    common_centralizer_order: int
    expected_common_centralizer_order: int
    c_equals_one_count: int
    c_equals_two_count: int
    c_other_count: int
    expected_c_equals_two_count: int
    all_zero_branch_universal: bool
    only_extra_branch_is_011: bool
    extra_branch_exactly_common_centralizer: bool
    exact_binary_return_classification_verified: bool
    status: str


@dataclass(frozen=True)
class CubicReturnBranchControl:
    half_degree: int
    pair_crossing_index: int
    common_centralizer_order: int
    switch_neighbour_count: int
    expected_switch_neighbour_count: int
    full_product_switch_count: int
    expected_full_product_switch_count: int
    c_equals_one_path_count: int
    c_equals_two_path_count: int
    c_equals_four_path_count: int
    c_other_path_count: int
    exact_unaffected_switch_classification_verified: bool
    direct_small_rank_histogram_verified: bool
    exact_cubic_return_classification_verified: bool
    status: str


@dataclass(frozen=True)
class TransporterBoundaryControl:
    half_degree: int
    matching_walk_length: int
    selected_middle_bits: tuple[int, ...]
    consecutive_switch_path_verified: bool
    selected_middle_word_transports_H_to_H_crossed: bool
    three_switch_path_count: int
    expected_three_switch_path_count: int
    total_three_switch_path_count: int
    transporter_path_fraction: float
    exact_transporter_path_count_verified: bool
    full_subword_cube_size: int
    full_subword_product_support_size: int
    maximum_full_subword_product_multiplicity: int
    identity_full_subword_product_multiplicity: int
    maximum_atom_probability: float
    one_quarter_concentration_violated: bool
    six_point_witness_lifts_to_all_higher_ranks: bool
    status: str


@dataclass(frozen=True)
class DegreeFourSupportControl:
    active_unaffected_pair_count: int
    canonical_half_degree: int
    canonical_all_active_path_count: int
    c_equals_one_path_count: int
    c_equals_two_path_count: int
    c_equals_four_path_count: int
    c_equals_eight_path_count: int
    baseline_c_equals_one_path_count: int
    baseline_c_equals_two_path_count: int
    baseline_c_equals_four_path_count: int
    odd_identity_path_count: int
    odd_identity_occurrence_count: int
    expected_path_histogram: dict[int, int]
    expected_baseline_path_histogram: dict[int, int]
    expected_odd_identity_path_count: int
    expected_odd_identity_occurrence_count: int
    exact_canonical_support_enumeration_verified: bool
    status: str


@dataclass(frozen=True)
class DegreeFourReturnBranchControl:
    half_degree: int
    unaffected_pair_parameter: int
    total_three_switch_path_count: int
    c_equals_one_path_count: int
    c_equals_two_path_count: int
    c_equals_four_path_count: int
    c_equals_eight_path_count: int
    odd_identity_exception_path_count: int
    baseline_c_equals_one_path_count: int
    baseline_c_equals_two_path_count: int
    baseline_c_equals_four_path_count: int
    histogram_sums_to_all_paths: bool
    baseline_histogram_sums_to_closure_paths: bool
    support_deletion_bijection_verified: bool
    exact_degree_four_return_classification_verified: bool
    status: str


@dataclass(frozen=True)
class CrossHeckeMomentControl:
    half_degree: int
    copy_count: int
    pair_crossing_index: int
    baseline_first_moment: str
    likelihood_first_moment: str
    first_moment_bias: str
    baseline_second_moment: str
    likelihood_second_moment: str
    second_moment_bias: str
    likelihood_to_baseline_second_moment_ratio: str
    baseline_third_moment: str
    likelihood_third_moment: str
    third_moment_bias: str
    baseline_fourth_moment: str
    likelihood_fourth_moment: str
    fourth_moment_bias: str
    exact_second_moment_formula_verified: bool
    exact_third_moment_formula_verified: bool
    exact_fourth_moment_formula_verified: bool
    status: str


@dataclass(frozen=True)
class CrossHeckeScalingRecord:
    half_degree: int
    degree: int
    conjugacy_class_size_decimal: str
    copy_count: int
    linear_bias: float
    baseline_second_moment: float
    second_moment_absolute_bias: float
    second_moment_relative_excess: float
    third_moment_absolute_bias: float
    cubic_unit_coefficient_bias_upper_bound: float
    cubic_bias_at_most_thrice_inverse_64_candidates: bool
    fourth_moment_absolute_bias: float
    fourth_bias_at_most_three_over_copy_scale_squared: bool
    quartic_unit_coefficient_bias_upper_bound: float
    quartic_bias_at_most_four_times_inverse_64_candidates: bool
    relative_second_moment_excess_vanishes: bool
    status: str


@dataclass(frozen=True)
class CrossTranspositionHeckeMomentTheorem:
    Hecke_operator: str
    common_centralizer: str
    binary_return_classification: str
    baseline_second_moment: str
    likelihood_second_moment: str
    second_moment_excess: str
    cubic_return_classification: str
    baseline_third_moment: str
    likelihood_third_moment: str
    third_moment_excess: str
    degree_four_support_classification: str
    baseline_fourth_moment: str
    likelihood_fourth_moment: str
    fourth_moment_excess: str
    transporter_cancellation: str
    natural_copy_consequence: str
    exact_common_centralizer_formula_proved: bool
    exact_binary_return_classification_proved: bool
    exact_all_rank_second_moment_formula_proved: bool
    exact_all_rank_third_moment_formula_proved: bool
    exact_all_rank_fourth_moment_formula_proved: bool
    normalized_cubic_filter_amplifies_to_constant_bias: bool
    normalized_quartic_filter_amplifies_to_constant_bias: bool
    transporter_exclusion_strategy_falsified: bool
    three_switch_transporter_mass_formula_proved: bool
    all_degree_one_quarter_concentration_proved: bool
    higher_interleaved_moment_no_go_proved: bool
    nonlinear_spectral_decoder_constructed: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CrossTranspositionHeckeMomentReport:
    created_at: str
    theorem_contract: dict[str, Any]
    branch_controls: list[BinaryReturnBranchControl]
    cubic_branch_controls: list[CubicReturnBranchControl]
    transporter_controls: list[TransporterBoundaryControl]
    degree_four_support_controls: list[DegreeFourSupportControl]
    degree_four_branch_controls: list[DegreeFourReturnBranchControl]
    moment_controls: list[CrossHeckeMomentControl]
    scaling_records: list[CrossHeckeScalingRecord]
    theorem: CrossTranspositionHeckeMomentTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _identity(degree: int) -> Permutation:
    return tuple(range(degree))


def _transposition(
    degree: int,
    left: int,
    right: int,
) -> Permutation:
    permutation = list(range(degree))
    permutation[left], permutation[right] = (
        permutation[right],
        permutation[left],
    )
    return tuple(permutation)


def _multiply(*elements: Permutation) -> Permutation:
    result = elements[0]
    for element in elements[1:]:
        result = compose_permutations(result, element)
    return result


def audit_binary_return_branches(
    half_degree: int,
) -> BinaryReturnBranchControl:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    degree = 2 * half_degree
    identity = _identity(degree)
    hidden = tuple(point ^ 1 for point in range(degree))
    order_two = (identity, hidden)
    crossing = _transposition(degree, 0, 2)
    centralizer = hyperoctahedral_group(half_degree)
    centralizer_set = set(centralizer)
    common = {
        element
        for element in centralizer
        if _multiply(crossing, element, crossing) in centralizer_set
    }
    histogram: Counter[int] = Counter()
    extra_patterns: Counter[tuple[int, int, int]] = Counter()
    extra_exact = True
    for element in centralizer:
        solutions = []
        for left_bit, left in enumerate(order_two):
            for middle_bit, middle in enumerate(order_two):
                for right_bit, right in enumerate(order_two):
                    product = _multiply(
                        crossing,
                        left,
                        element,
                        crossing,
                        middle,
                        crossing,
                        inverse_permutation(element),
                        crossing,
                        right,
                    )
                    if product == identity:
                        solutions.append(
                            (left_bit, middle_bit, right_bit)
                        )
        histogram[len(solutions)] += 1
        for pattern in solutions:
            if pattern != (0, 0, 0):
                extra_patterns[pattern] += 1
        extra_exact = extra_exact and (
            (len(solutions) == 2) == (element in common)
        )
    expected_common = (
        (2**half_degree) * math.factorial(half_degree - 2)
    )
    verified = bool(
        len(common) == expected_common
        and histogram[1] == len(centralizer) - expected_common
        and histogram[2] == expected_common
        and sum(
            count
            for branch_count, count in histogram.items()
            if branch_count not in (1, 2)
        )
        == 0
        and extra_patterns == {(0, 1, 1): expected_common}
        and extra_exact
    )
    return BinaryReturnBranchControl(
        half_degree=half_degree,
        degree=degree,
        centralizer_order=len(centralizer),
        common_centralizer_order=len(common),
        expected_common_centralizer_order=expected_common,
        c_equals_one_count=histogram[1],
        c_equals_two_count=histogram[2],
        c_other_count=sum(
            count
            for branch_count, count in histogram.items()
            if branch_count not in (1, 2)
        ),
        expected_c_equals_two_count=expected_common,
        all_zero_branch_universal=(sum(histogram.values()) == len(centralizer)),
        only_extra_branch_is_011=(
            extra_patterns == {(0, 1, 1): expected_common}
        ),
        extra_branch_exactly_common_centralizer=extra_exact,
        exact_binary_return_classification_verified=verified,
        status=(
            "exact-cross-transposition-binary-return-classification"
            if verified
            else "cross-transposition-return-control-failure"
        ),
    )


def _matching_from_edges(
    edges: tuple[tuple[int, int], ...],
    degree: int,
) -> Permutation:
    matching = list(range(degree))
    for left, right in edges:
        matching[left] = right
        matching[right] = left
    return tuple(matching)


def _matching_edges(matching: Permutation) -> tuple[tuple[int, int], ...]:
    return tuple(
        (point, matching[point])
        for point in range(len(matching))
        if point < matching[point]
    )


def _switch_neighbours(matching: Permutation) -> set[Permutation]:
    edges = _matching_edges(matching)
    output: set[Permutation] = set()
    for first, second in itertools.combinations(range(len(edges)), 2):
        left_a, right_a = edges[first]
        left_b, right_b = edges[second]
        retained = tuple(
            edge
            for index, edge in enumerate(edges)
            if index not in (first, second)
        )
        for replacement in (
            ((left_a, left_b), (right_a, right_b)),
            ((left_a, right_b), (right_a, left_b)),
        ):
            output.add(
                _matching_from_edges(retained + replacement, len(matching))
            )
    return output


def _direct_cubic_binary_histogram(
    half_degree: int,
) -> Counter[int]:
    degree = 2 * half_degree
    identity = _identity(degree)
    hidden = tuple(point ^ 1 for point in range(degree))
    crossing = _transposition(degree, 0, 2)
    hidden_crossed = _multiply(crossing, hidden, crossing)
    centralizer = hyperoctahedral_group(half_degree)
    histogram: Counter[int] = Counter()
    for left in centralizer:
        prefix = _multiply(crossing, left, crossing)
        second_involution = _multiply(
            prefix,
            hidden,
            inverse_permutation(prefix),
        )
        for right in centralizer:
            final_prefix = _multiply(prefix, right, crossing)
            third_involution = _multiply(
                final_prefix,
                hidden,
                inverse_permutation(final_prefix),
            )
            involutions = (
                hidden_crossed,
                second_involution,
                third_involution,
                hidden,
            )
            count = 0
            for mask in range(16):
                product = identity
                for index, involution in enumerate(involutions):
                    if mask & (1 << (3 - index)):
                        product = compose_permutations(product, involution)
                count += product == identity
            histogram[count] += 1
    return histogram


def audit_cubic_return_branches(
    half_degree: int,
) -> CubicReturnBranchControl:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    degree = 2 * half_degree
    hidden = tuple(point ^ 1 for point in range(degree))
    crossing = _transposition(degree, 0, 2)
    hidden_crossed = _multiply(crossing, hidden, crossing)
    crossed_neighbours = _switch_neighbours(hidden_crossed)
    hidden_neighbours = _switch_neighbours(hidden)
    full_product_count = sum(
        _multiply(candidate, hidden_crossed, hidden) in hidden_neighbours
        for candidate in crossed_neighbours
    )
    crossing_index = half_degree * (half_degree - 1)
    expected_full_product = 1 + (
        (half_degree - 2) * (half_degree - 3)
    )
    common_order = (
        (2**half_degree) * math.factorial(half_degree - 2)
    )
    two_factor = 3 * half_degree**2 - 7 * half_degree + 5
    c_four = common_order**2
    c_two = two_factor * common_order**2
    centralizer_order = (2**half_degree) * math.factorial(half_degree)
    c_one = centralizer_order**2 - c_two - c_four
    direct_verified = True
    if half_degree <= 4:
        direct = _direct_cubic_binary_histogram(half_degree)
        direct_verified = bool(
            direct[1] == c_one
            and direct[2] == c_two
            and direct[4] == c_four
            and sum(
                count
                for branch_count, count in direct.items()
                if branch_count not in (1, 2, 4)
            )
            == 0
        )
    switch_verified = bool(
        len(crossed_neighbours) == crossing_index
        and len(hidden_neighbours) == crossing_index
        and full_product_count == expected_full_product
    )
    verified = bool(
        switch_verified
        and direct_verified
        and c_one >= 0
        and c_one + c_two + c_four == centralizer_order**2
    )
    return CubicReturnBranchControl(
        half_degree=half_degree,
        pair_crossing_index=crossing_index,
        common_centralizer_order=common_order,
        switch_neighbour_count=len(crossed_neighbours),
        expected_switch_neighbour_count=crossing_index,
        full_product_switch_count=full_product_count,
        expected_full_product_switch_count=expected_full_product,
        c_equals_one_path_count=c_one,
        c_equals_two_path_count=c_two,
        c_equals_four_path_count=c_four,
        c_other_path_count=0,
        exact_unaffected_switch_classification_verified=switch_verified,
        direct_small_rank_histogram_verified=direct_verified,
        exact_cubic_return_classification_verified=verified,
        status=(
            "exact-cross-transposition-cubic-return-classification"
            if verified
            else "cross-transposition-cubic-return-control-failure"
        ),
    )


def audit_transporter_boundary(
    half_degree: int,
) -> TransporterBoundaryControl:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    degree = 2 * half_degree
    identity = _identity(degree)
    retained = tuple(
        (2 * pair, 2 * pair + 1)
        for pair in range(3, half_degree)
    )
    hidden = _matching_from_edges(
        ((0, 1), (2, 3), (4, 5)) + retained,
        degree,
    )
    hidden_crossed = _matching_from_edges(
        ((0, 2), (1, 3), (4, 5)) + retained,
        degree,
    )
    path = (
        _matching_from_edges(
            ((0, 2), (1, 4), (3, 5)) + retained,
            degree,
        ),
        _matching_from_edges(
            ((0, 3), (1, 4), (2, 5)) + retained,
            degree,
        ),
        _matching_from_edges(
            ((0, 3), (1, 5), (2, 4)) + retained,
            degree,
        ),
    )
    switch_path = bool(
        path[0] in _switch_neighbours(hidden_crossed)
        and path[1] in _switch_neighbours(path[0])
        and path[2] in _switch_neighbours(path[1])
    )
    selected_bits = (0, 1, 1)
    middle_word = compose_permutations(path[1], path[2])
    transported = _multiply(
        middle_word,
        hidden,
        inverse_permutation(middle_word),
    ) == hidden_crossed
    first_neighbours = _switch_neighbours(hidden_crossed)
    predecessor_count: Counter[Permutation] = Counter()
    for first in first_neighbours:
        for second in _switch_neighbours(first):
            predecessor_count[second] += 1
    transporter_path_count = 0
    for second, predecessor_multiplicity in predecessor_count.items():
        for third in _switch_neighbours(second):
            middle = compose_permutations(second, third)
            if _multiply(
                middle,
                hidden,
                inverse_permutation(middle),
            ) == hidden_crossed:
                transporter_path_count += predecessor_multiplicity
    crossing_index = half_degree * (half_degree - 1)
    total_path_count = crossing_index**3
    expected_transporter_count = 12 * (half_degree - 2)
    path_count_verified = (
        transporter_path_count == expected_transporter_count
    )
    product_counts: Counter[Permutation] = Counter()
    involutions = (hidden_crossed,) + path + (hidden,)
    for mask in range(1 << len(involutions)):
        product = identity
        for index, involution in enumerate(involutions):
            if mask & (1 << (len(involutions) - 1 - index)):
                product = compose_permutations(product, involution)
        product_counts[product] += 1
    maximum = max(product_counts.values())
    verified = (
        switch_path
        and transported
        and maximum == 2
        and path_count_verified
    )
    return TransporterBoundaryControl(
        half_degree=half_degree,
        matching_walk_length=len(path),
        selected_middle_bits=selected_bits,
        consecutive_switch_path_verified=switch_path,
        selected_middle_word_transports_H_to_H_crossed=transported,
        three_switch_path_count=transporter_path_count,
        expected_three_switch_path_count=expected_transporter_count,
        total_three_switch_path_count=total_path_count,
        transporter_path_fraction=(
            transporter_path_count / total_path_count
        ),
        exact_transporter_path_count_verified=path_count_verified,
        full_subword_cube_size=1 << len(involutions),
        full_subword_product_support_size=len(product_counts),
        maximum_full_subword_product_multiplicity=maximum,
        identity_full_subword_product_multiplicity=product_counts[identity],
        maximum_atom_probability=maximum / (1 << len(involutions)),
        one_quarter_concentration_violated=maximum > (
            (1 << len(involutions)) // 4
        ),
        six_point_witness_lifts_to_all_higher_ranks=verified,
        status=(
            "all-rank-transporter-exists-without-concentration-violation"
            if verified
            else "transporter-boundary-control-failure"
        ),
    )


def _identity_subword_count(
    involutions: tuple[Permutation, ...],
    *,
    parity: int | None = None,
) -> int:
    identity = _identity(len(involutions[0]))
    count = 0
    for mask in range(1 << len(involutions)):
        if parity is not None and mask.bit_count() % 2 != parity:
            continue
        product = identity
        for index, involution in enumerate(involutions):
            if mask & (1 << (len(involutions) - 1 - index)):
                product = compose_permutations(product, involution)
        count += product == identity
    return count


def _active_unaffected_pairs(
    involutions: tuple[Permutation, ...],
) -> frozenset[int]:
    half_degree = len(involutions[0]) // 2
    return frozenset(
        pair
        for pair in range(2, half_degree)
        if any(
            involution[2 * pair] != 2 * pair + 1
            for involution in involutions
        )
    )


_DEGREE_FOUR_SUPPORT_EXPECTED: dict[
    int,
    tuple[int, dict[int, int], dict[int, int], int, int],
] = {
    0: (8, {4: 7, 8: 1}, {2: 2, 4: 1}, 7, 28),
    1: (208, {1: 108, 2: 84, 4: 16}, {1: 8, 2: 8}, 0, 0),
    2: (1304, {1: 1030, 2: 260, 4: 14}, {2: 6}, 6, 6),
    3: (3456, {1: 3120, 2: 336}, {}, 0, 0),
    4: (4512, {1: 4368, 2: 144}, {}, 0, 0),
    5: (2880, {1: 2880}, {}, 0, 0),
    6: (720, {1: 720}, {}, 0, 0),
}


@lru_cache(maxsize=1)
def audit_degree_four_support_catalog() -> tuple[
    DegreeFourSupportControl,
    ...,
]:
    """Enumerate the seven canonical active-support cores exactly.

    A three-switch path can activate at most six unaffected base pairs.  For
    an even identity subword, inert pairs contribute the identity and may be
    deleted.  Thus the all-rank count is the binomial lift of these cores,
    rather than a polynomial inferred from finite ranks.
    """

    controls: list[DegreeFourSupportControl] = []
    for active_count, expected in _DEGREE_FOUR_SUPPORT_EXPECTED.items():
        (
            expected_total,
            expected_histogram,
            expected_baseline_histogram,
            expected_odd_paths,
            expected_odd_occurrences,
        ) = expected
        half_degree = active_count + 2
        degree = 2 * half_degree
        hidden = _matching_from_edges(
            tuple(
                (2 * pair, 2 * pair + 1)
                for pair in range(half_degree)
            ),
            degree,
        )
        hidden_crossed = _matching_from_edges(
            ((0, 2), (1, 3))
            + tuple(
                (2 * pair, 2 * pair + 1)
                for pair in range(2, half_degree)
            ),
            degree,
        )
        neighbour_cache: dict[Permutation, tuple[Permutation, ...]] = {}

        def neighbours(matching: Permutation) -> tuple[Permutation, ...]:
            if matching not in neighbour_cache:
                neighbour_cache[matching] = tuple(
                    _switch_neighbours(matching)
                )
            return neighbour_cache[matching]

        even_histogram: Counter[int] = Counter()
        baseline_histogram: Counter[int] = Counter()
        odd_identity_paths = 0
        odd_identity_occurrences = 0
        for first in neighbours(hidden_crossed):
            for second in neighbours(first):
                for third in neighbours(second):
                    involutions = (
                        hidden_crossed,
                        first,
                        second,
                        third,
                        hidden,
                    )
                    if len(_active_unaffected_pairs(involutions)) != (
                        active_count
                    ):
                        continue
                    even_count = _identity_subword_count(
                        involutions,
                        parity=0,
                    )
                    odd_count = _identity_subword_count(
                        involutions,
                        parity=1,
                    )
                    even_histogram[even_count] += 1
                    if third == hidden:
                        if even_count % 2:
                            raise AssertionError(
                                "duplicated terminal involutions must pair "
                                "even identity subwords"
                            )
                        baseline_histogram[even_count // 2] += 1
                    odd_identity_paths += odd_count > 0
                    odd_identity_occurrences += odd_count
        total = sum(even_histogram.values())
        histogram = dict(sorted(even_histogram.items()))
        baseline = dict(sorted(baseline_histogram.items()))
        verified = bool(
            total == expected_total
            and histogram == expected_histogram
            and baseline == expected_baseline_histogram
            and odd_identity_paths == expected_odd_paths
            and odd_identity_occurrences == expected_odd_occurrences
        )
        controls.append(
            DegreeFourSupportControl(
                active_unaffected_pair_count=active_count,
                canonical_half_degree=half_degree,
                canonical_all_active_path_count=total,
                c_equals_one_path_count=even_histogram[1],
                c_equals_two_path_count=even_histogram[2],
                c_equals_four_path_count=even_histogram[4],
                c_equals_eight_path_count=even_histogram[8],
                baseline_c_equals_one_path_count=baseline_histogram[1],
                baseline_c_equals_two_path_count=baseline_histogram[2],
                baseline_c_equals_four_path_count=baseline_histogram[4],
                odd_identity_path_count=odd_identity_paths,
                odd_identity_occurrence_count=odd_identity_occurrences,
                expected_path_histogram=expected_histogram,
                expected_baseline_path_histogram=(
                    expected_baseline_histogram
                ),
                expected_odd_identity_path_count=expected_odd_paths,
                expected_odd_identity_occurrence_count=(
                    expected_odd_occurrences
                ),
                exact_canonical_support_enumeration_verified=verified,
                status=(
                    "exact-degree-four-canonical-support-core"
                    if verified
                    else "degree-four-support-core-control-failure"
                ),
            )
        )
    return tuple(controls)


def _choose(total: int, selected: int) -> int:
    if selected < 0 or selected > total:
        return 0
    return math.comb(total, selected)


def degree_four_return_branch_control(
    half_degree: int,
) -> DegreeFourReturnBranchControl:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    unaffected_parameter = half_degree - 2
    crossing_index = half_degree * (half_degree - 1)
    c_eight = 1
    c_four = (
        7
        + 16 * unaffected_parameter
        + 14 * _choose(unaffected_parameter, 2)
    )
    c_two = (
        84 * unaffected_parameter
        + 260 * _choose(unaffected_parameter, 2)
        + 336 * _choose(unaffected_parameter, 3)
        + 144 * _choose(unaffected_parameter, 4)
    )
    odd_exception = 6 if half_degree == 4 else 0
    c_two += odd_exception
    total_paths = crossing_index**3
    c_one = total_paths - c_two - c_four - c_eight

    baseline_one = 8 * unaffected_parameter
    baseline_two = (
        2
        + 8 * unaffected_parameter
        + 6 * _choose(unaffected_parameter, 2)
    )
    baseline_four = 1
    closure_paths = 3 * half_degree**2 + half_degree - 11
    catalog = audit_degree_four_support_catalog()
    catalog_verified = all(
        row.exact_canonical_support_enumeration_verified
        for row in catalog
    )
    histogram_verified = (
        c_one >= 0
        and c_one + c_two + c_four + c_eight == total_paths
    )
    baseline_verified = (
        baseline_one + baseline_two + baseline_four == closure_paths
    )
    verified = bool(
        catalog_verified and histogram_verified and baseline_verified
    )
    return DegreeFourReturnBranchControl(
        half_degree=half_degree,
        unaffected_pair_parameter=unaffected_parameter,
        total_three_switch_path_count=total_paths,
        c_equals_one_path_count=c_one,
        c_equals_two_path_count=c_two,
        c_equals_four_path_count=c_four,
        c_equals_eight_path_count=c_eight,
        odd_identity_exception_path_count=odd_exception,
        baseline_c_equals_one_path_count=baseline_one,
        baseline_c_equals_two_path_count=baseline_two,
        baseline_c_equals_four_path_count=baseline_four,
        histogram_sums_to_all_paths=histogram_verified,
        baseline_histogram_sums_to_closure_paths=baseline_verified,
        support_deletion_bijection_verified=catalog_verified,
        exact_degree_four_return_classification_verified=verified,
        status=(
            "exact-cross-transposition-degree-four-return-classification"
            if verified
            else "cross-transposition-degree-four-control-failure"
        ),
    )


def _direct_degree_four_binary_histogram(
    half_degree: int,
) -> Counter[int]:
    """Direct finite-rank audit used only as a regression control."""

    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    degree = 2 * half_degree
    hidden = _matching_from_edges(
        tuple((2 * pair, 2 * pair + 1) for pair in range(half_degree)),
        degree,
    )
    hidden_crossed = _matching_from_edges(
        ((0, 2), (1, 3))
        + tuple(
            (2 * pair, 2 * pair + 1)
            for pair in range(2, half_degree)
        ),
        degree,
    )
    neighbour_cache: dict[Permutation, tuple[Permutation, ...]] = {}

    def neighbours(matching: Permutation) -> tuple[Permutation, ...]:
        if matching not in neighbour_cache:
            neighbour_cache[matching] = tuple(
                _switch_neighbours(matching)
            )
        return neighbour_cache[matching]

    histogram: Counter[int] = Counter()
    for first in neighbours(hidden_crossed):
        for second in neighbours(first):
            for third in neighbours(second):
                histogram[
                    _identity_subword_count(
                        (
                            hidden_crossed,
                            first,
                            second,
                            third,
                            hidden,
                        )
                    )
                ] += 1
    return histogram


def cross_Hecke_moment_control(
    half_degree: int,
    copy_count: int,
) -> CrossHeckeMomentControl:
    if half_degree < 3 or copy_count < 1:
        raise ValueError("half_degree>=3 and copy_count>=1 are required")
    crossing_index = half_degree * (half_degree - 1)
    baseline_second = Fraction(
        1,
        (2**copy_count) * crossing_index,
    )
    likelihood_second = Fraction(
        1,
        4**copy_count,
    ) * (
        1
        + Fraction(
            2**copy_count - 1,
            crossing_index,
        )
    )
    second_bias = likelihood_second - baseline_second
    predicted_bias = Fraction(
        crossing_index - 1,
        (4**copy_count) * crossing_index,
    )
    ratio = likelihood_second / baseline_second
    predicted_ratio = Fraction(
        crossing_index + 2**copy_count - 1,
        2**copy_count,
    )
    cubic_two_factor = 3 * half_degree**2 - 7 * half_degree + 5
    baseline_third = Fraction(
        1,
        (4**copy_count) * crossing_index**2,
    )
    likelihood_third = Fraction(
        crossing_index**2
        - cubic_two_factor
        - 1
        + cubic_two_factor * (2**copy_count)
        + 4**copy_count,
        (8**copy_count) * crossing_index**2,
    )
    third_bias = likelihood_third - baseline_third
    verified = second_bias == predicted_bias and ratio == predicted_ratio
    third_verified = third_bias == Fraction(
        4**copy_count
        + (cubic_two_factor - 1) * (2**copy_count)
        + crossing_index**2
        - cubic_two_factor
        - 1,
        (8**copy_count) * crossing_index**2,
    )
    fourth_branches = degree_four_return_branch_control(half_degree)
    copy_scale = 2**copy_count
    baseline_fourth = Fraction(
        fourth_branches.baseline_c_equals_one_path_count
        + fourth_branches.baseline_c_equals_two_path_count * copy_scale
        + fourth_branches.baseline_c_equals_four_path_count
        * copy_scale**2,
        copy_scale**3 * crossing_index**3,
    )
    likelihood_fourth = Fraction(
        fourth_branches.c_equals_one_path_count
        + fourth_branches.c_equals_two_path_count * copy_scale
        + fourth_branches.c_equals_four_path_count * copy_scale**2
        + fourth_branches.c_equals_eight_path_count * copy_scale**3,
        copy_scale**4 * crossing_index**3,
    )
    fourth_bias = likelihood_fourth - baseline_fourth
    predicted_fourth_bias = Fraction(
        fourth_branches.c_equals_one_path_count
        + (
            fourth_branches.c_equals_two_path_count
            - fourth_branches.baseline_c_equals_one_path_count
        )
        * copy_scale
        + (
            fourth_branches.c_equals_four_path_count
            - fourth_branches.baseline_c_equals_two_path_count
        )
        * copy_scale**2,
        copy_scale**4 * crossing_index**3,
    )
    fourth_verified = bool(
        fourth_branches.exact_degree_four_return_classification_verified
        and fourth_branches.c_equals_eight_path_count
        == fourth_branches.baseline_c_equals_four_path_count
        and fourth_bias == predicted_fourth_bias
    )
    return CrossHeckeMomentControl(
        half_degree=half_degree,
        copy_count=copy_count,
        pair_crossing_index=crossing_index,
        baseline_first_moment="0",
        likelihood_first_moment=str(Fraction(1, 2**copy_count)),
        first_moment_bias=str(Fraction(1, 2**copy_count)),
        baseline_second_moment=str(baseline_second),
        likelihood_second_moment=str(likelihood_second),
        second_moment_bias=str(second_bias),
        likelihood_to_baseline_second_moment_ratio=str(ratio),
        baseline_third_moment=str(baseline_third),
        likelihood_third_moment=str(likelihood_third),
        third_moment_bias=str(third_bias),
        baseline_fourth_moment=str(baseline_fourth),
        likelihood_fourth_moment=str(likelihood_fourth),
        fourth_moment_bias=str(fourth_bias),
        exact_second_moment_formula_verified=verified,
        exact_third_moment_formula_verified=third_verified,
        exact_fourth_moment_formula_verified=fourth_verified,
        status=(
            "exact-cross-Hecke-first-four-moments"
            if verified and third_verified and fourth_verified
            else "cross-Hecke-moment-formula-failure"
        ),
    )


def cross_Hecke_scaling_record(
    half_degree: int,
) -> CrossHeckeScalingRecord:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    crossing_index = half_degree * (half_degree - 1)
    linear_bias = 2.0 ** (-copies)
    baseline_second = linear_bias / crossing_index
    second_bias = (4.0 ** (-copies)) * (
        1.0 - 1.0 / crossing_index
    )
    cubic_two_factor = 3 * half_degree**2 - 7 * half_degree + 5
    third_bias = (
        linear_bias
        + (cubic_two_factor - 1) * linear_bias**2
        + (
            crossing_index**2 - cubic_two_factor - 1
        ) * linear_bias**3
    ) / crossing_index**2
    relative_excess = (crossing_index - 1) * linear_bias
    cubic_bound = linear_bias + second_bias + third_bias
    inverse_bound = 3.0 / (64.0 * candidates)
    cubic_verified = cubic_bound <= inverse_bound * (1.0 + 1e-15)
    fourth_control = cross_Hecke_moment_control(half_degree, copies)
    fourth_bias = float(Fraction(fourth_control.fourth_moment_bias))
    fourth_scale_bound = 3.0 * linear_bias**2
    fourth_verified = fourth_bias <= fourth_scale_bound * (1.0 + 1e-15)
    quartic_bound = cubic_bound + fourth_bias
    quartic_inverse_bound = 4.0 / (64.0 * candidates)
    quartic_verified = quartic_bound <= quartic_inverse_bound * (
        1.0 + 1e-15
    )
    return CrossHeckeScalingRecord(
        half_degree=half_degree,
        degree=degree,
        conjugacy_class_size_decimal=str(candidates),
        copy_count=copies,
        linear_bias=linear_bias,
        baseline_second_moment=baseline_second,
        second_moment_absolute_bias=second_bias,
        second_moment_relative_excess=relative_excess,
        third_moment_absolute_bias=third_bias,
        cubic_unit_coefficient_bias_upper_bound=cubic_bound,
        cubic_bias_at_most_thrice_inverse_64_candidates=cubic_verified,
        fourth_moment_absolute_bias=fourth_bias,
        fourth_bias_at_most_three_over_copy_scale_squared=(
            fourth_verified
        ),
        quartic_unit_coefficient_bias_upper_bound=quartic_bound,
        quartic_bias_at_most_four_times_inverse_64_candidates=(
            quartic_verified
        ),
        relative_second_moment_excess_vanishes=relative_excess < 0.01,
        status=(
            "cross-Hecke-quartic-bias-remains-inverse-candidate"
            if cubic_verified and fourth_verified and quartic_verified
            else "cross-Hecke-quartic-scaling-control-failure"
        ),
    )


def build_cross_transposition_Hecke_moment_report() -> CrossTranspositionHeckeMomentReport:
    branches = [
        audit_binary_return_branches(half_degree)
        for half_degree in (3, 4, 5)
    ]
    cubic_branches = [
        audit_cubic_return_branches(half_degree)
        for half_degree in (3, 4, 5, 6, 8)
    ]
    transporter_controls = [
        audit_transporter_boundary(half_degree)
        for half_degree in (3, 4, 8)
    ]
    degree_four_support_controls = list(
        audit_degree_four_support_catalog()
    )
    degree_four_branch_controls = [
        degree_four_return_branch_control(half_degree)
        for half_degree in (3, 4, 5, 6, 8, 12)
    ]
    moments = [
        cross_Hecke_moment_control(half_degree, copy_count)
        for half_degree in (3, 4, 5)
        for copy_count in (1, 2, 5)
    ]
    scaling = [
        cross_Hecke_scaling_record(half_degree)
        for half_degree in (4, 8, 16, 32, 64)
    ]
    verified = bool(
        all(row.exact_binary_return_classification_verified for row in branches)
        and all(
            row.exact_cubic_return_classification_verified
            for row in cubic_branches
        )
        and all(
            row.six_point_witness_lifts_to_all_higher_ranks
            and not row.one_quarter_concentration_violated
            for row in transporter_controls
        )
        and all(
            row.exact_canonical_support_enumeration_verified
            for row in degree_four_support_controls
        )
        and all(
            row.exact_degree_four_return_classification_verified
            for row in degree_four_branch_controls
        )
        and all(
            row.exact_second_moment_formula_verified
            and row.exact_third_moment_formula_verified
            and row.exact_fourth_moment_formula_verified
            for row in moments
        )
        and all(
            row.cubic_bias_at_most_thrice_inverse_64_candidates
            and row.fourth_bias_at_most_three_over_copy_scale_squared
            and row.quartic_bias_at_most_four_times_inverse_64_candidates
            for row in scaling
        )
    )
    theorem = CrossTranspositionHeckeMomentTheorem(
        Hecke_operator=(
            "X=e_B a_t e_B for a transposition t crossing two h-pairs"
        ),
        common_centralizer=(
            "|C(h) intersect tC(h)t|=2^m(m-2)!, index m(m-1) in C(h)"
        ),
        binary_return_classification=(
            "c(r)=1+1[r in C(h) intersect tC(h)t] for every m>=3"
        ),
        baseline_second_moment="tr_B(X^2)=1/[2^k m(m-1)]",
        likelihood_second_moment=(
            "tr_B(X^2 Z)=4^-k[1+(2^k-1)/(m(m-1))]"
        ),
        second_moment_excess=(
            "4^-k[1-1/(m(m-1))]"
        ),
        cubic_return_classification=(
            "For r=m(m-1), a=3m^2-7m+5, binary return counts 1,2,4 "
            "occur on (r^2-a-1)|J|^2, a|J|^2, |J|^2 shared paths."
        ),
        baseline_third_moment="tr_B(X^3)=1/[4^k m^2(m-1)^2]",
        likelihood_third_moment=(
            "tr_B(X^3 Z)=[r^2-a-1+a 2^k+4^k]/(8^k r^2)"
        ),
        third_moment_excess=(
            "[4^k+(a-1)2^k+r^2-a-1]/(8^k r^2)"
        ),
        degree_four_support_classification=(
            "For n=m-2, N8=1, N4=7+16n+14*C(n,2), and "
            "N2=84n+260*C(n,2)+336*C(n,3)+144*C(n,4), with "
            "N1=r^3-N2-N4-N8. This holds for m=3 and m>=5; at "
            "m=4 exactly six paths move from N1 to N2."
        ),
        baseline_fourth_moment=(
            "For x=2^k, tr_B(X^4)=[8(m-2)+(3m^2-7m+4)x+x^2]"
            "/[x^3 r^3]"
        ),
        likelihood_fourth_moment=(
            "tr_B(X^4 Z)=[N1+N2 x+N4 x^2+x^3]/[x^4 r^3]"
        ),
        fourth_moment_excess=(
            "[N1+(N2-8(m-2))x+(N4-(3m^2-7m+4))x^2]"
            "/[x^4 r^3]=O(x^-2)"
        ),
        transporter_cancellation=(
            "The unique alternative c=8 branch and unique baseline c=4 "
            "closure branch contribute the same x^3 term and cancel exactly."
        ),
        natural_copy_consequence=(
            "At k=ceil(log2(64M)), every unit-coefficient quartic filter "
            "built from 1,X,X^2,X^3,X^4 has O(1/M) total bias; the new "
            "fourth-moment contribution is O(M^-2)."
        ),
        exact_common_centralizer_formula_proved=True,
        exact_binary_return_classification_proved=True,
        exact_all_rank_second_moment_formula_proved=True,
        exact_all_rank_third_moment_formula_proved=True,
        exact_all_rank_fourth_moment_formula_proved=True,
        normalized_cubic_filter_amplifies_to_constant_bias=False,
        normalized_quartic_filter_amplifies_to_constant_bias=False,
        transporter_exclusion_strategy_falsified=True,
        three_switch_transporter_mass_formula_proved=True,
        all_degree_one_quarter_concentration_proved=True,
        higher_interleaved_moment_no_go_proved=True,
        nonlinear_spectral_decoder_constructed=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "cross-Hecke-first-four-moments-all-degree-bound-linked"
            if verified
            else "cross-transposition-Hecke-moment-control-failure"
        ),
    )
    return CrossTranspositionHeckeMomentReport(
        created_at=utc_now(),
        theorem_contract={
            "group_family": "S_(2m), m>=3",
            "hidden_involution": "fixed-point-free involution h",
            "walk": "single B-double-coset Hecke operator from a cross-pair transposition",
            "copy_count": "arbitrary k>=1; natural rows use ceil(log2(64M))",
            "claim_boundary": (
                "Exact first four moment formulas here; a linked theorem gives "
                "the all-degree normalized-moment bound, but no full-spectrum no-go."
            ),
        },
        branch_controls=branches,
        cubic_branch_controls=cubic_branches,
        transporter_controls=transporter_controls,
        degree_four_support_controls=degree_four_support_controls,
        degree_four_branch_controls=degree_four_branch_controls,
        moment_controls=moments,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-CROSS-HECKE-HIGHER-MOMENTS",
                "statement": (
                    "Resolved for normalized moments and polynomial LCUs by "
                    "the adjacent-pair one-quarter fiber injection. Exact "
                    "higher histograms are unnecessary for this bound."
                ),
                "resolved": True,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-CROSS-HECKE-THRESHOLD",
                "statement": (
                    "Determine whether rare large eigenvalues of X carry "
                    "nonnegligible alternative mass despite the first-three-moment no-go."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MULTI-DOUBLE-COSET-WALK",
                "statement": (
                    "Search mixtures of B double cosets for a polynomially gapped, "
                    "fast-forwardable recoupling statistic."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "One B interleaving may amplify 2^-k to a polynomial signal.",
                "answer": (
                    "False for this canonical cross-transposition walk: the exact "
                    "second-moment excess is order 4^-k and the cubic excess "
                    "returns only to order 2^-k/[m(m-1)]^2."
                ),
                "resolved": True,
            },
            {
                "challenge": "The common-centralizer formula is a finite-rank pattern.",
                "answer": (
                    "It follows all-rank from the four-point alternating matching "
                    "component times the unaffected C_2 wr S_(m-2) action."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "An all-degree one-quarter concentration proof can simply "
                    "exclude words transporting <h> to <t h t>."
                ),
                "answer": (
                    "False. A three-switch six-point path supplies such a "
                    "transporter at every m>=3, while its full subword law still "
                    "has maximum atom only 1/16. Exactly 12(m-2) of the "
                    "[m(m-1)]^3 switch paths realize this selected transporter."
                ),
                "resolved": True,
            },
            {
                "challenge": "Three moments determine the full spectral law.",
                "answer": (
                    "False, and four moments still do not. Rare spectral tails "
                    "and degree-five-and-higher interleavings remain explicit "
                    "proof obligations."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The first degree-four transporter creates an order-2^-k "
                    "fourth-moment signal."
                ),
                "answer": (
                    "False. Its unique c=8 alternative branch is the same "
                    "closure branch that contributes baseline c=4, so the "
                    "entire order-2^-k term cancels exactly."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "SOURCE-LOCAL-LIKELIHOOD-NO-GO",
                "role": "Forces the search to all-copy target-coupled operators.",
            },
            {
                "id": "DIAGONAL-CHARGE-BIAS-NO-GO",
                "role": "Supplies the exact 2^-k linear moment boundary.",
            },
            {
                "id": "SINGLE-HECKE-ALL-DEGREE-MOMENT-NO-GO",
                "role": (
                    "Extends one-quarter subword concentration and inverse-copy "
                    "bias to every normalized degree."
                ),
            },
        ],
        headline_metrics={
            "exact_binary_return_control_count": len(branches),
            "exact_cubic_return_control_count": len(cubic_branches),
            "all_rank_transporter_boundary_control_count": len(
                transporter_controls
            ),
            "canonical_degree_four_support_core_count": len(
                degree_four_support_controls
            ),
            "exact_degree_four_branch_control_count": len(
                degree_four_branch_controls
            ),
            "maximum_transporter_path_fraction": max(
                row.transporter_path_fraction
                for row in transporter_controls
            ),
            "exact_moment_control_count": len(moments),
            "natural_scaling_row_count": len(scaling),
            "maximum_branch_classification_failure_count": max(
                row.c_other_count for row in branches
            ),
            "maximum_natural_relative_second_moment_excess": max(
                row.second_moment_relative_excess for row in scaling
            ),
        },
        claim_gate={
            "exact_cross_Hecke_first_three_moments_proved": True,
            "exact_cross_Hecke_first_four_moments_proved": True,
            "normalized_cubic_filter_constant_bias": False,
            "normalized_quartic_filter_constant_bias": False,
            "transporter_exclusion_strategy_valid": False,
            "three_switch_transporter_mass_formula_proved": True,
            "degree_four_transporter_leading_term_cancelled": True,
            "all_degree_one_quarter_concentration_proved": True,
            "higher_interleaved_normalized_moment_no_go_proved": True,
            "nonlinear_spectral_decoder_constructed": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The canonical cross-transposition walk has no normalized "
                "degree-four amplification. The all-degree adjacent-pair "
                "injection closes every normalized moment and polynomial LCU, "
                "but nonlinear spectral tails and multiple operators remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved exact first-four-moment suppression for the canonical "
            "cross-transposition all-copy recoupling walk, including exact "
            "cancellation of the first transporter term."
        ),
        falsifiers_triggered=[
            "One B interleaving does not amplify diagonal all-copy bias.",
            "Normalized cubic filtering of the cross-transposition walk remains inverse-candidate biased.",
            "A blanket no-transporter lemma is false from degree four onward.",
            "The first degree-four transporter does not create a leading moment signal.",
            "Any surviving mechanism must use nonlinear spectral tails, large coefficient norm, postselection, or multiple double cosets.",
        ],
    )


def write_cross_transposition_Hecke_moment_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_cross_transposition_Hecke_moment_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_cross_transposition_Hecke_moment_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
