"""Exact group-algebra traces from a diagonal YJM tableau projector.

For a standard tableau ``T`` with content vector ``c(T)``, the product of
Lagrange projectors in the commuting diagonal Jucys-Murphy elements selects
one copy of the ``T`` tableau line from every copy of its irrep.  Therefore

    Tr(P_T H^k) = Tr(M_nu^k),

where ``M_nu`` is the Kronecker multiplicity block of any diagonal-commutant
operator ``H``.  The implementation below expands the rational group algebra
exactly.  It is intended for controls: the explicit pair state space has size
``(n!)^2`` and is not a scalable evaluator.
"""

from __future__ import annotations

import math
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache

from coset_jucys_murphy_label_transform import (
    standard_young_tableaux,
    tableau_content_vector,
)
from coset_typical_class_contraction_scaling import (
    shared_transposition_generator_orbit,
)
from coset_typical_commutant_moment_audit import (
    TC_INTERSECTION_ONE,
    _cycle_type,
    _generator_orbit,
)
from representation_obstruction import integer_partitions
from symmetric_character import symmetric_character


Permutation = tuple[int, ...]
Pair = tuple[Permutation, Permutation]
Distribution = dict[Pair, Fraction]
WeightedTerm = tuple[Pair, Fraction]


def identity_permutation(n: int) -> Permutation:
    return tuple(range(n))


def compose(left: Permutation, right: Permutation) -> Permutation:
    if len(left) != len(right):
        raise ValueError("permutations must have equal degree")
    return tuple(left[right[index]] for index in range(len(left)))


def transposition(n: int, first: int, second: int) -> Permutation:
    if not 0 <= first < second < n:
        raise ValueError("expected 0 <= first < second < n")
    result = list(range(n))
    result[first], result[second] = result[second], result[first]
    return tuple(result)


@lru_cache(maxsize=None)
def possible_yjm_contents(label: int) -> tuple[int, ...]:
    """Return the exact spectrum of J_label across all S_label irreps."""

    if label < 1:
        raise ValueError("YJM labels must be positive")
    values = {
        tableau_content_vector(tableau)[-1]
        for partition in integer_partitions(label)
        for tableau in standard_young_tableaux(partition)
    }
    return tuple(sorted(values))


def multiply_distribution_by_terms(
    distribution: Distribution,
    terms: tuple[WeightedTerm, ...],
) -> Distribution:
    """Right-multiply a rational pair-group-algebra distribution."""

    if not distribution or not terms:
        raise ValueError("distribution and terms must not be empty")
    output: defaultdict[Pair, Fraction] = defaultdict(Fraction)
    for (left, right), weight in distribution.items():
        for (term_left, term_right), term_weight in terms:
            output[
                (
                    compose(left, term_left),
                    compose(right, term_right),
                )
            ] += weight * term_weight
    return {
        pair: weight for pair, weight in output.items() if weight
    }


def yjm_tableau_projector_distribution(
    n: int,
    target_partition: tuple[int, ...],
    *,
    tableau_index: int = 0,
) -> tuple[Distribution, tuple[int, ...], tuple[int, ...]]:
    """Expand the exact joint-content projector for one target tableau."""

    if sum(target_partition) != n:
        raise ValueError("target partition must have size n")
    tableaux = standard_young_tableaux(target_partition)
    if not 0 <= tableau_index < len(tableaux):
        raise ValueError("tableau index is out of range")
    content = tableau_content_vector(tableaux[tableau_index])
    identity = identity_permutation(n)
    distribution: Distribution = {(identity, identity): Fraction(1)}
    state_counts = [1]
    for label in range(2, n + 1):
        chosen = content[label - 1]
        diagonal_yjm = tuple(
            (
                (
                    transposition(n, index, label - 1),
                    transposition(n, index, label - 1),
                ),
                Fraction(1),
            )
            for index in range(label - 1)
        )
        for alternative in possible_yjm_contents(label):
            if alternative == chosen:
                continue
            denominator = Fraction(chosen - alternative)
            factor = (
                *(
                    (pair, weight / denominator)
                    for pair, weight in diagonal_yjm
                ),
                (
                    (identity, identity),
                    Fraction(-alternative, chosen - alternative),
                ),
            )
            distribution = multiply_distribution_by_terms(
                distribution,
                tuple(factor),
            )
        state_counts.append(len(distribution))
    return distribution, content, tuple(state_counts)


@lru_cache(maxsize=None)
def separator_terms(n: int) -> tuple[WeightedTerm, ...]:
    """Return exact terms of average(TT1)+average(TC1)."""

    _, _, tt_orbit = shared_transposition_generator_orbit(n)
    _, _, tc_orbit = _generator_orbit(n, TC_INTERSECTION_ONE)
    return (
        *(
            (pair, Fraction(1, len(tt_orbit)))
            for pair in tt_orbit
        ),
        *(
            (pair, Fraction(1, len(tc_orbit)))
            for pair in tc_orbit
        ),
    )


def representation_trace(
    distribution: Distribution,
    source_partition: tuple[int, ...],
) -> Fraction:
    """Trace a pair-group-algebra element on V_lambda tensor V_lambda."""

    if sum(source_partition) != len(next(iter(distribution))[0]):
        raise ValueError("source partition and distribution degree differ")
    return sum(
        weight
        * symmetric_character(source_partition, _cycle_type(left))
        * symmetric_character(source_partition, _cycle_type(right))
        for (left, right), weight in distribution.items()
    )


def exact_yjm_projector_power_traces(
    source_partition: tuple[int, ...],
    target_partition: tuple[int, ...],
    maximum_degree: int,
    *,
    tableau_index: int = 0,
) -> dict[str, object]:
    """Compute exact multiplicity-block traces with explicit pair expansion."""

    n = sum(source_partition)
    if sum(target_partition) != n:
        raise ValueError("source and target must partition the same n")
    if maximum_degree < 0:
        raise ValueError("maximum degree must be nonnegative")
    distribution, content, projector_state_counts = (
        yjm_tableau_projector_distribution(
            n,
            target_partition,
            tableau_index=tableau_index,
        )
    )
    projector_trace = representation_trace(
        distribution,
        source_partition,
    )
    traces: list[Fraction] = []
    power_state_counts: list[int] = []
    terms = separator_terms(n)
    for _ in range(maximum_degree):
        distribution = multiply_distribution_by_terms(
            distribution,
            terms,
        )
        traces.append(
            representation_trace(distribution, source_partition)
        )
        power_state_counts.append(len(distribution))
    return {
        "n": n,
        "source_partition": source_partition,
        "target_partition": target_partition,
        "tableau_index": tableau_index,
        "tableau_content_vector": content,
        "projector_trace": projector_trace,
        "projector_state_counts_by_label": projector_state_counts,
        "projector_state_count": projector_state_counts[-1],
        "power_traces": tuple(traces),
        "power_state_counts": tuple(power_state_counts),
        "explicit_pair_state_space_size": math.factorial(n) ** 2,
        "separator_term_count": len(terms),
    }
