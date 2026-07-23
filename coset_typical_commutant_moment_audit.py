"""Character-only moment audit for bounded-support typical-irrep commutants.

Let ``A_O`` be the normalized simultaneous-conjugacy orbit average of
``rho_lambda(a) tensor rho_mu(b)``.  It commutes with the diagonal ``S_n``
action, so on the ``nu`` isotypic component it has the form
``I_nu tensor M_nu``.  Character projection gives exact formulas

    Tr(M_nu) = |G|^-1 sum_g chi_nu(g) chi_lambda(ga) chi_mu(gb)

and

    Tr(M_nu^2) = (|O||G|)^-1 sum_y sum_g
        chi_nu(g) chi_lambda(g a a_y) chi_mu(g b b_y).

The variance of the multiplicity-space eigenvalues is therefore available
without constructing representation matrices.  Positive variance proves only
that an orbit average is non-scalar in that finite block.  It does not prove a
simple spectrum, a minimum eigenvalue gap, a uniform circuit, or a decoder.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient, symmetric_character


COSET_TYPICAL_COMMUTANT_MOMENT_PATH = Path(
    "research/representation/coset_typical_commutant_moment_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-COMMUTANT-MOMENT-AUDIT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

TC_INTERSECTION_TWO = "ORB-TC-INTERSECTION-2"
TC_INTERSECTION_ONE = "ORB-TC-INTERSECTION-1"
TT_DISJOINT = "ORB-TT-DISJOINT"
DEFAULT_GENERATORS = (TC_INTERSECTION_TWO, TT_DISJOINT, TC_INTERSECTION_ONE)


@dataclass(frozen=True)
class GeneratorMomentRecord:
    generator_id: str
    orbit_size: int
    first_moment_signature_count: int
    second_moment_signature_count: int
    exact_mean_eigenvalue: str
    mean_eigenvalue: float
    exact_second_moment: str
    second_moment: float
    exact_eigenvalue_variance: str
    eigenvalue_variance: float
    spectral_diameter_lower_bound: float
    non_scalar_proved: bool


@dataclass(frozen=True)
class TypicalCommutantTargetRecord:
    n: int
    source_partition: tuple[int, ...]
    source_dimension: int
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    generator_moments: list[GeneratorMomentRecord]
    exact_centered_covariance_matrix: list[list[str]]
    centered_covariance_rank: int
    non_scalar_generator_ids: list[str]
    best_generator_id: str | None
    maximum_eigenvalue_variance: float
    maximum_spectral_diameter_lower_bound: float
    finite_non_scalar_covered: bool
    finite_simple_spectrum_proved: bool
    finite_character_moment_only: bool
    status: str


@dataclass(frozen=True)
class TypicalCommutantMomentReport:
    created_at: str
    theorem_contract: dict[str, object]
    generator_contract: dict[str, object]
    records: list[TypicalCommutantTargetRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def _transposition(n: int, first: int, second: int) -> tuple[int, ...]:
    permutation = list(range(n))
    permutation[first], permutation[second] = permutation[second], permutation[first]
    return tuple(permutation)


def _three_cycle(n: int, first: int, second: int, third: int) -> tuple[int, ...]:
    permutation = list(range(n))
    permutation[first] = second
    permutation[second] = third
    permutation[third] = first
    return tuple(permutation)


def _cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    visited = [False] * len(permutation)
    lengths: list[int] = []
    for start in range(len(permutation)):
        if visited[start]:
            continue
        current = start
        length = 0
        while not visited[current]:
            visited[current] = True
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


@lru_cache(maxsize=None)
def _group_workspace(
    n: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    dict[tuple[int, ...], int],
    np.ndarray,
]:
    if n > 8:
        raise ValueError(
            "exact permutation enumeration is deliberately capped at n=8; "
            "larger n requires a class-algebra contraction"
        )
    cycle_types = tuple(integer_partitions(n))
    cycle_type_ids = {cycle_type: index for index, cycle_type in enumerate(cycle_types)}
    permutations = tuple(itertools.permutations(range(n)))
    permutation_type_ids = np.fromiter(
        (cycle_type_ids[_cycle_type(permutation)] for permutation in permutations),
        dtype=np.int16,
        count=len(permutations),
    )
    return cycle_types, permutations, cycle_type_ids, permutation_type_ids


@lru_cache(maxsize=None)
def _right_product_type_ids(n: int, right: tuple[int, ...]) -> np.ndarray:
    _, permutations, cycle_type_ids, _ = _group_workspace(n)
    return np.fromiter(
        (
            cycle_type_ids[
                _cycle_type(tuple(permutation[right[index]] for index in range(n)))
            ]
            for permutation in permutations
        ),
        dtype=np.int16,
        count=len(permutations),
    )


def _generator_orbit(
    n: int, generator_id: str
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
]:
    if generator_id == TC_INTERSECTION_TWO:
        base_left = _transposition(n, 0, 1)
        base_right = _three_cycle(n, 0, 1, 2)
        orbit = tuple(
            (
                _transposition(n, first, second),
                _three_cycle(n, first, second, third),
            )
            for first in range(n)
            for second in range(n)
            if second != first
            for third in range(n)
            if third != first and third != second
        )
        return base_left, base_right, orbit
    if generator_id == TC_INTERSECTION_ONE:
        base_left = _transposition(n, 0, 1)
        base_right = _three_cycle(n, 0, 2, 3)
        rows = []
        for support in itertools.combinations(range(n), 3):
            first, second, third = support
            cycles = (
                _three_cycle(n, first, second, third),
                _three_cycle(n, first, third, second),
            )
            support_set = set(support)
            for cycle in cycles:
                for shared in support:
                    for outside in range(n):
                        if outside not in support_set:
                            rows.append(
                                (_transposition(n, shared, outside), cycle)
                            )
        return base_left, base_right, tuple(rows)
    if generator_id == TT_DISJOINT:
        if n < 4:
            raise ValueError("disjoint transpositions require n>=4")
        base_left = _transposition(n, 0, 1)
        base_right = _transposition(n, 2, 3)
        rows = []
        for left_support in itertools.combinations(range(n), 2):
            remaining = tuple(
                value for value in range(n) if value not in left_support
            )
            for right_support in itertools.combinations(remaining, 2):
                rows.append(
                    (
                        _transposition(n, *left_support),
                        _transposition(n, *right_support),
                    )
                )
        return base_left, base_right, tuple(rows)
    raise ValueError(f"unsupported orbit generator: {generator_id}")


@lru_cache(maxsize=None)
def moment_signature_counts(
    n: int, generator_id: str
) -> tuple[tuple[int, ...], np.ndarray, np.ndarray, int]:
    """Return exact first/second character-signature counts for one orbit."""

    cycle_types, permutations, _, group_type_ids = _group_workspace(n)
    base_left, base_right, orbit = _generator_orbit(n, generator_id)
    type_count = len(cycle_types)
    code_count = type_count**3
    first_codes = (
        group_type_ids.astype(np.int64) * type_count * type_count
        + _right_product_type_ids(n, base_left).astype(np.int64) * type_count
        + _right_product_type_ids(n, base_right).astype(np.int64)
    )
    first_counts = np.bincount(first_codes, minlength=code_count).astype(np.int64)
    second_counts = np.zeros(code_count, dtype=np.int64)
    for orbit_left, orbit_right in orbit:
        relative_left = _compose(base_left, orbit_left)
        relative_right = _compose(base_right, orbit_right)
        second_codes = (
            group_type_ids.astype(np.int64) * type_count * type_count
            + _right_product_type_ids(n, relative_left).astype(np.int64) * type_count
            + _right_product_type_ids(n, relative_right).astype(np.int64)
        )
        second_counts += np.bincount(second_codes, minlength=code_count)
    if int(first_counts.sum()) != len(permutations):
        raise ArithmeticError("first-moment signature count does not sum to |S_n|")
    if int(second_counts.sum()) != len(permutations) * len(orbit):
        raise ArithmeticError("second-moment signature count does not sum to |S_n||O|")
    return cycle_types, first_counts, second_counts, len(orbit)


@lru_cache(maxsize=None)
def cross_moment_signature_counts(
    n: int,
    left_generator_id: str,
    right_generator_id: str,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, int]:
    """Return signatures for Tr(M_left M_right) after orbit normalization."""

    if left_generator_id == right_generator_id:
        cycle_types, _, second_counts, orbit_size = moment_signature_counts(
            n, left_generator_id
        )
        return cycle_types, second_counts, orbit_size
    cycle_types, permutations, _, group_type_ids = _group_workspace(n)
    base_left, base_right, _ = _generator_orbit(n, left_generator_id)
    _, _, right_orbit = _generator_orbit(n, right_generator_id)
    type_count = len(cycle_types)
    code_count = type_count**3
    group_codes = group_type_ids.astype(np.int64) * type_count * type_count
    counts = np.zeros(code_count, dtype=np.int64)
    for orbit_left, orbit_right in right_orbit:
        relative_left = _compose(base_left, orbit_left)
        relative_right = _compose(base_right, orbit_right)
        codes = (
            group_codes
            + _right_product_type_ids(n, relative_left).astype(np.int64)
            * type_count
            + _right_product_type_ids(n, relative_right).astype(np.int64)
        )
        counts += np.bincount(codes, minlength=code_count)
    if int(counts.sum()) != len(permutations) * len(right_orbit):
        raise ArithmeticError("cross-moment signatures do not sum to |S_n||O|")
    return cycle_types, counts, len(right_orbit)


def _character_contraction(
    counts: np.ndarray,
    cycle_types: tuple[tuple[int, ...], ...],
    source: tuple[int, ...],
    target: tuple[int, ...],
) -> int:
    type_count = len(cycle_types)
    source_characters = tuple(
        symmetric_character(source, cycle_type) for cycle_type in cycle_types
    )
    target_characters = tuple(
        symmetric_character(target, cycle_type) for cycle_type in cycle_types
    )
    total = 0
    for code in np.flatnonzero(counts):
        group_index, remainder = divmod(int(code), type_count * type_count)
        left_index, right_index = divmod(remainder, type_count)
        total += (
            int(counts[code])
            * target_characters[group_index]
            * source_characters[left_index]
            * source_characters[right_index]
        )
    return total


@lru_cache(maxsize=None)
def audit_generator_moment(
    n: int,
    source: tuple[int, ...],
    target: tuple[int, ...],
    generator_id: str,
) -> GeneratorMomentRecord:
    multiplicity = kronecker_coefficient(source, source, target)
    if multiplicity <= 1:
        raise ValueError("moment audit requires a nontrivial multiplicity block")
    cycle_types, first_counts, second_counts, orbit_size = moment_signature_counts(
        n, generator_id
    )
    group_order = math.factorial(n)
    trace = Fraction(
        _character_contraction(first_counts, cycle_types, source, target),
        group_order,
    )
    trace_square = Fraction(
        _character_contraction(second_counts, cycle_types, source, target),
        group_order * orbit_size,
    )
    mean = trace / multiplicity
    second_moment = trace_square / multiplicity
    variance = second_moment - mean * mean
    if variance < 0:
        raise ArithmeticError("exact Hermitian eigenvalue variance is negative")
    return GeneratorMomentRecord(
        generator_id=generator_id,
        orbit_size=orbit_size,
        first_moment_signature_count=int(np.count_nonzero(first_counts)),
        second_moment_signature_count=int(np.count_nonzero(second_counts)),
        exact_mean_eigenvalue=str(mean),
        mean_eigenvalue=float(mean),
        exact_second_moment=str(second_moment),
        second_moment=float(second_moment),
        exact_eigenvalue_variance=str(variance),
        eigenvalue_variance=float(variance),
        spectral_diameter_lower_bound=2 * math.sqrt(float(variance)),
        non_scalar_proved=variance > 0,
    )


@lru_cache(maxsize=None)
def audit_cross_moment(
    n: int,
    source: tuple[int, ...],
    target: tuple[int, ...],
    left_generator_id: str,
    right_generator_id: str,
) -> Fraction:
    """Return the exact mean eigenvalue product Tr(M_left M_right)/g."""

    multiplicity = kronecker_coefficient(source, source, target)
    if multiplicity <= 1:
        raise ValueError("cross-moment audit requires nontrivial multiplicity")
    cycle_types, counts, orbit_size = cross_moment_signature_counts(
        n, left_generator_id, right_generator_id
    )
    return Fraction(
        _character_contraction(counts, cycle_types, source, target),
        math.factorial(n) * orbit_size * multiplicity,
    )


def _fraction_matrix_rank(matrix: list[list[Fraction]]) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(rank, row_count) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for index in range(row_count):
            if index == rank or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(rows[index], rows[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def _maximum_dimension_partition(n: int) -> tuple[int, ...]:
    return max(
        integer_partitions(n),
        key=lambda partition: (hook_length_dimension(partition), partition),
    )


@lru_cache(maxsize=None)
def audit_typical_commutant_moments(
    n: int,
    generator_ids: tuple[str, ...] = DEFAULT_GENERATORS,
) -> tuple[TypicalCommutantTargetRecord, ...]:
    source = _maximum_dimension_partition(n)
    source_dimension = hook_length_dimension(source)
    records = []
    for target in integer_partitions(n):
        multiplicity = kronecker_coefficient(source, source, target)
        if multiplicity <= 1:
            continue
        moments = [
            audit_generator_moment(n, source, target, generator_id)
            for generator_id in generator_ids
        ]
        non_scalar = [
            moment.generator_id for moment in moments if moment.non_scalar_proved
        ]
        means = [Fraction(moment.exact_mean_eigenvalue) for moment in moments]
        covariance: list[list[Fraction]] = [
            [Fraction() for _ in moments] for _ in moments
        ]
        for left_index, left_moment in enumerate(moments):
            covariance[left_index][left_index] = Fraction(
                left_moment.exact_eigenvalue_variance
            )
            for right_index in range(left_index + 1, len(moments)):
                cross = audit_cross_moment(
                    n,
                    source,
                    target,
                    left_moment.generator_id,
                    moments[right_index].generator_id,
                )
                centered = cross - means[left_index] * means[right_index]
                covariance[left_index][right_index] = centered
                covariance[right_index][left_index] = centered
        covariance_rank = _fraction_matrix_rank(covariance)
        best = max(moments, key=lambda moment: moment.eigenvalue_variance)
        records.append(
            TypicalCommutantTargetRecord(
                n=n,
                source_partition=source,
                source_dimension=source_dimension,
                target_partition=target,
                target_dimension=hook_length_dimension(target),
                kronecker_multiplicity=multiplicity,
                generator_moments=moments,
                exact_centered_covariance_matrix=[
                    [str(value) for value in row] for row in covariance
                ],
                centered_covariance_rank=covariance_rank,
                non_scalar_generator_ids=non_scalar,
                best_generator_id=best.generator_id if best.non_scalar_proved else None,
                maximum_eigenvalue_variance=best.eigenvalue_variance,
                maximum_spectral_diameter_lower_bound=(
                    best.spectral_diameter_lower_bound
                ),
                finite_non_scalar_covered=bool(non_scalar),
                finite_simple_spectrum_proved=(
                    multiplicity == 2 and bool(non_scalar)
                ),
                finite_character_moment_only=True,
                status=(
                    "finite-non-scalar-witness-gap-open"
                    if non_scalar
                    else "bounded-support-portfolio-scalar-negative-result"
                ),
            )
        )
    return tuple(records)


@lru_cache(maxsize=1)
def build_typical_commutant_moment_report(
    n_values: tuple[int, ...] = (7, 8),
    generator_ids: tuple[str, ...] = DEFAULT_GENERATORS,
) -> TypicalCommutantMomentReport:
    records = [
        record
        for n in n_values
        for record in audit_typical_commutant_moments(n, generator_ids)
    ]
    covered = [record for record in records if record.finite_non_scalar_covered]
    uncovered = [record for record in records if not record.finite_non_scalar_covered]
    primary_scalar_count = sum(
        1
        for record in records
        if record.generator_moments
        and not record.generator_moments[0].non_scalar_proved
    )
    rank_two_count = sum(record.centered_covariance_rank >= 2 for record in records)
    multiplicity_two_simple_count = sum(
        record.finite_simple_spectrum_proved for record in records
    )
    finite_covariance_or_simple_count = sum(
        record.centered_covariance_rank >= 2
        or record.finite_simple_spectrum_proved
        for record in records
    )
    metrics: dict[str, int | float] = {
        "finite_n_count": len(n_values),
        "bounded_support_generator_count": len(generator_ids),
        "nontrivial_multiplicity_block_count": len(records),
        "finite_non_scalar_covered_count": len(covered),
        "finite_uncovered_count": len(uncovered),
        "primary_generator_exact_scalar_block_count": primary_scalar_count,
        "finite_centered_covariance_rank_two_count": rank_two_count,
        "finite_multiplicity_two_simple_spectrum_count": (
            multiplicity_two_simple_count
        ),
        "finite_covariance_rank_two_or_simple_multiplicity_two_count": (
            finite_covariance_or_simple_count
        ),
        "finite_higher_multiplicity_joint_simple_spectrum_count": 0,
        "maximum_kronecker_multiplicity": max(
            (record.kronecker_multiplicity for record in records), default=0
        ),
        "minimum_positive_variance": min(
            (
                record.maximum_eigenvalue_variance
                for record in covered
                if record.maximum_eigenvalue_variance > 0
            ),
            default=0.0,
        ),
        "minimum_finite_spectral_diameter_lower_bound": min(
            (
                record.maximum_spectral_diameter_lower_bound for record in covered
            ),
            default=0.0,
        ),
        "uniform_typical_commutant_non_scalar_theorem_count": 0,
        "uniform_typical_commutant_gap_theorem_count": 0,
        "uniform_typical_commutant_simple_spectrum_theorem_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    all_covered = bool(records) and not uncovered
    return TypicalCommutantMomentReport(
        created_at=utc_now(),
        theorem_contract={
            "decomposition": (
                "A_O commutes with diagonal S_n and acts as I_nu tensor M_nu on each nu multiplicity block."
            ),
            "first_moment_identity": (
                "Tr(M_nu)=|S_n|^-1 sum_g chi_nu(g) chi_lambda(ga) chi_mu(gb)."
            ),
            "second_moment_identity": (
                "Tr(M_nu^2)=(|O||S_n|)^-1 sum_y sum_g chi_nu(g) "
                "chi_lambda(g a a_y) chi_mu(g b b_y)."
            ),
            "non_scalar_certificate": (
                "Tr(M_nu^2)/g_nu-(Tr(M_nu)/g_nu)^2>0 exactly iff the finite Hermitian block is non-scalar."
            ),
            "diameter_consequence": (
                "Popoviciu's inequality gives spectral diameter at least 2*sqrt(variance)."
            ),
            "enumeration_cap": (
                "The current exact permutation contraction is capped at n=8. Extending it requires a class-algebra formula, not factorial enumeration."
            ),
        },
        generator_contract={
            TC_INTERSECTION_TWO: {
                "left": "transposition",
                "right": "oriented 3-cycle",
                "support_intersection": 2,
                "orbit_size": "n(n-1)(n-2)",
                "normalized_operator_norm_bound": 1,
            },
            TC_INTERSECTION_ONE: {
                "left": "transposition",
                "right": "oriented 3-cycle",
                "support_intersection": 1,
                "orbit_size": "n(n-1)(n-2)(n-3)",
                "normalized_operator_norm_bound": 1,
            },
            TT_DISJOINT: {
                "left": "transposition",
                "right": "transposition",
                "support_intersection": 0,
                "orbit_size": "6*binomial(n,4)",
                "normalized_operator_norm_bound": 1,
            },
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "finite_typical_non_scalar_coverage": all_covered,
            "finite_centered_covariance_rank_is_joint_spectrum_proof": False,
            "finite_non_scalar_coverage_is_asymptotic_theorem": False,
            "uniform_typical_non_scalarity_proved": False,
            "inverse_polynomial_eigenvalue_gap_proved": False,
            "simple_spectrum_proved": False,
            "label_adaptive_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact finite character moments transfer non-scalar bounded-support action to the audited typical blocks, "
                "and mixed moments certify independent traceless directions in many blocks, but they do not control "
                "noncommutation, all-n eigenvalue collisions, minimum gaps, circuit synthesis, or decoding."
            ),
        },
        status=(
            "finite-typical-non-scalar-transfer-signal-gap-and-decoder-open"
            if all_covered
            else "finite-bounded-support-portfolio-has-scalar-blocks"
        ),
        summary=(
            f"Exact character moments audited {len(records)} nontrivial typical multiplicity blocks at n={n_values}. "
            f"The bounded-support portfolio is non-scalar on {len(covered)} and scalar on {len(uncovered)}; "
            f"{rank_two_count} have at least two independent traceless directions and {multiplicity_two_simple_count} "
            "additional two-dimensional blocks have finite simple spectrum. No uniform gap, transform, or decoder follows."
        ),
        falsifiers_triggered=[
            "One transposition/3-cycle orbit average is scalar on two audited n=8 multiplicity blocks.",
            "Adding a second bounded-support observable repairs finite non-scalarity but does not prove simple joint spectrum.",
            "A positive centered covariance rank proves linear independence, not noncommutation or algebra generation.",
            "Positive finite variance supplies no lower bound on the minimum eigenvalue gap.",
            "Factorial exact character enumeration is not an efficient quantum or classical implementation.",
            "No outcome-information or hidden-involution decoding theorem is implied by multiplicity-space non-scalarity.",
        ],
    )


def write_typical_commutant_moment_report(
    output_path: Path = COSET_TYPICAL_COMMUTANT_MOMENT_PATH,
    n_values: tuple[int, ...] = (7, 8),
    generator_ids: tuple[str, ...] = DEFAULT_GENERATORS,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        build_typical_commutant_moment_report(
            n_values=n_values,
            generator_ids=generator_ids,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-FINITE-NONSCALAR-NOT-GAP",
                source=str(output_path),
                claim=(
                    "Finite nonzero multiplicity-space variance of a bounded-support orbit average establishes an efficient typical-irrep resolving measurement."
                ),
                reason_invalid=(
                    "Variance proves only non-scalarity. It does not prove simple spectrum, a minimum inverse-polynomial gap, a uniform circuit, or a decoder."
                ),
                lesson=(
                    "Use exact moments as a cheap transfer filter, then require all-n class-algebra formulas, joint-spectrum separation, gap bounds, and outcome information."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        if payload["headline_metrics"][
            "primary_generator_exact_scalar_block_count"
        ]:
            upsert_negative_result(
                NegativeResultRecord(
                    id="NEG-COSET-TYPICAL-SINGLE-TC2-GENERATOR-UNIFORMITY",
                    source=str(output_path),
                    claim=(
                        "The normalized transposition/3-cycle intersection-two orbit average alone resolves every typical Kronecker multiplicity block uniformly."
                    ),
                    reason_invalid=(
                        "Its exact multiplicity-space variance is zero on the n=8 targets (4,4) and (2,2,2,2), despite splitting every audited n=7 block."
                    ),
                    lesson=(
                        "Reject one-generator extrapolation. Require a fixed portfolio, all-n joint-spectrum control, and an inverse-polynomial separation theorem."
                    ),
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        if payload["headline_metrics"]["finite_uncovered_count"]:
            upsert_negative_result(
                NegativeResultRecord(
                    id="NEG-COSET-TYPICAL-BOUNDED-SUPPORT-SCALAR-BLOCKS",
                    source=str(output_path),
                    claim=(
                        "The audited bounded-support orbit portfolio acts non-scalarly on every tested typical multiplicity block."
                    ),
                    reason_invalid="At least one audited block has exactly zero eigenvalue variance for every searched generator.",
                    lesson="Mutate the generator portfolio before any gap search and retain exact scalar blocks as regression tests.",
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_typical_commutant_moment_audit": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_typical_commutant_moment_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
