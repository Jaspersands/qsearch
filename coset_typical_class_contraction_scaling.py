"""Class-compressed scaling audit for the primary typical commutant observable.

The primary observable is the normalized simultaneous-conjugacy average of a
transposition and an oriented 3-cycle sharing two support points.  Its first
and second multiplicity-space moments were previously available only by
enumerating every element of ``S_n``.  This module replaces that factorial
enumeration by:

* exact marked-support injection counts inside each conjugacy class; and
* a 17-state simultaneous-conjugacy classification of the relative orbit
  products appearing in the second moment.

The resulting evaluator reaches typical maximum-dimension sources through
``n=10`` exactly.  It is a structural microscope, not a circuit: iterating all
integer partitions and marked injections is not promoted to an efficient
quantum transform or a bit-complexity theorem.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

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
from symmetric_marked_class_contraction import (
    PairKey,
    canonical_pair_key,
    class_compressed_signature_counts,
    compose,
    pair_support_size,
)


COSET_TYPICAL_CLASS_CONTRACTION_PATH = Path(
    "research/representation/coset_typical_class_contraction_scaling.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-CLASS-CONTRACTION-SCALING"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
GENERATOR_ID = "ORB-TC-INTERSECTION-2"
SHARED_TRANSPOSITION_GENERATOR_ID = "ORB-TT-INTERSECTION-1"


@dataclass(frozen=True)
class ClassContractionScalingRecord:
    n: int
    source_partition: tuple[int, ...]
    source_dimension: int
    partition_count: int
    orbit_size: int
    relative_pair_type_count: int
    relative_pair_support_profile: dict[str, int]
    first_moment_signature_count: int
    second_moment_signature_count: int
    first_signature_total_verified: bool
    second_signature_total_verified: bool
    factorial_signature_verification_performed: bool
    factorial_first_signature_verified: bool
    factorial_second_signature_verified: bool
    nontrivial_multiplicity_block_count: int
    non_scalar_block_count: int
    exact_scalar_block_count: int
    exact_scalar_targets: list[tuple[int, ...]]
    exact_scalar_target_multiplicities: list[int]
    minimum_positive_variance: float
    maximum_variance: float
    maximum_kronecker_multiplicity: int
    finite_exact_character_contraction_only: bool
    status: str


@dataclass(frozen=True)
class ClassContractionPortfolioRecord:
    n: int
    source_partition: tuple[int, ...]
    source_dimension: int
    nontrivial_multiplicity_block_count: int
    primary_scalar_targets: list[tuple[int, ...]]
    shared_transposition_scalar_targets: list[tuple[int, ...]]
    both_generators_scalar_targets: list[tuple[int, ...]]
    finite_portfolio_non_scalar_covered_count: int
    centered_covariance_rank_two_count: int
    centered_covariance_rank_one_targets: list[tuple[int, ...]]
    minimum_positive_covariance_determinant: float
    primary_shared_cross_signature_count: int
    primary_shared_relative_pair_type_count: int
    shared_self_relative_pair_type_count: int
    finite_two_generator_moment_only: bool
    status: str


@dataclass(frozen=True)
class ClassContractionScalingReport:
    created_at: str
    contraction_contract: dict[str, object]
    records: list[ClassContractionScalingRecord]
    portfolio_records: list[ClassContractionPortfolioRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


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


def primary_generator_orbit(
    n: int,
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
]:
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


def shared_transposition_generator_orbit(
    n: int,
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
]:
    base_left = _transposition(n, 0, 1)
    base_right = _transposition(n, 0, 2)
    orbit = tuple(
        (
            _transposition(n, common, left),
            _transposition(n, common, right),
        )
        for common in range(n)
        for left in range(n)
        if left != common
        for right in range(n)
        if right != common and right != left
    )
    return base_left, base_right, orbit


@lru_cache(maxsize=None)
def relative_pair_type_counts(n: int) -> tuple[tuple[PairKey, int], ...]:
    base_left, base_right, orbit = primary_generator_orbit(n)
    counts = Counter(
        canonical_pair_key(
            compose(base_left, orbit_left),
            compose(base_right, orbit_right),
        )
        for orbit_left, orbit_right in orbit
    )
    return tuple(sorted(counts.items(), key=lambda item: (pair_support_size(item[0]), item[0])))


@lru_cache(maxsize=None)
def primary_class_signature_counts(
    n: int,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, np.ndarray, int]:
    base_left, base_right, orbit = primary_generator_orbit(n)
    cycle_types, first_counts = class_compressed_signature_counts(
        n, canonical_pair_key(base_left, base_right)
    )
    second_counts = np.zeros_like(first_counts)
    for key, weight in relative_pair_type_counts(n):
        relative_cycle_types, relative_counts = class_compressed_signature_counts(
            n, key
        )
        if relative_cycle_types != cycle_types:
            raise ArithmeticError("cycle-type order changed across contractions")
        second_counts += weight * relative_counts
    if int(first_counts.sum()) != math.factorial(n):
        raise ArithmeticError("first signatures do not sum to |S_n|")
    if int(second_counts.sum()) != math.factorial(n) * len(orbit):
        raise ArithmeticError("second signatures do not sum to |S_n||O|")
    return cycle_types, first_counts, second_counts, len(orbit)


def _weighted_relative_signature_counts(
    n: int,
    base_left: tuple[int, ...],
    base_right: tuple[int, ...],
    orbit: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, int, dict[str, int]]:
    relative_counts = Counter(
        canonical_pair_key(
            compose(base_left, orbit_left),
            compose(base_right, orbit_right),
        )
        for orbit_left, orbit_right in orbit
    )
    cycle_types: tuple[tuple[int, ...], ...] | None = None
    counts: np.ndarray | None = None
    for key, weight in relative_counts.items():
        key_cycle_types, key_counts = class_compressed_signature_counts(n, key)
        if counts is None:
            cycle_types = key_cycle_types
            counts = np.zeros_like(key_counts)
        elif key_cycle_types != cycle_types:
            raise ArithmeticError("cycle-type order changed across relative pairs")
        counts += weight * key_counts
    if cycle_types is None or counts is None:
        raise ArithmeticError("generator orbit is empty")
    if int(counts.sum()) != math.factorial(n) * len(orbit):
        raise ArithmeticError("weighted signatures do not sum to |S_n||O|")
    support_profile = Counter(pair_support_size(key) for key in relative_counts)
    return (
        cycle_types,
        counts,
        len(relative_counts),
        {str(support): count for support, count in sorted(support_profile.items())},
    )


@lru_cache(maxsize=None)
def shared_transposition_class_signature_counts(
    n: int,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, np.ndarray, int, int]:
    base_left, base_right, orbit = shared_transposition_generator_orbit(n)
    cycle_types, first_counts = class_compressed_signature_counts(
        n, canonical_pair_key(base_left, base_right)
    )
    second_types, second_counts, relative_type_count, _ = (
        _weighted_relative_signature_counts(n, base_left, base_right, orbit)
    )
    if second_types != cycle_types:
        raise ArithmeticError("shared-transposition cycle-type order changed")
    return cycle_types, first_counts, second_counts, len(orbit), relative_type_count


@lru_cache(maxsize=None)
def primary_shared_cross_signature_counts(
    n: int,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, int, int]:
    base_left, base_right, _ = primary_generator_orbit(n)
    _, _, shared_orbit = shared_transposition_generator_orbit(n)
    cycle_types, counts, relative_type_count, _ = (
        _weighted_relative_signature_counts(
            n, base_left, base_right, shared_orbit
        )
    )
    return cycle_types, counts, len(shared_orbit), relative_type_count


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


def _maximum_dimension_partition(n: int) -> tuple[int, ...]:
    return max(
        integer_partitions(n),
        key=lambda partition: (hook_length_dimension(partition), partition),
    )


@lru_cache(maxsize=None)
def audit_class_contraction_scaling(n: int) -> ClassContractionScalingRecord:
    cycle_types, first_counts, second_counts, orbit_size = (
        primary_class_signature_counts(n)
    )
    factorial_first_verified = False
    factorial_second_verified = False
    factorial_verification_performed = n <= 8
    if factorial_verification_performed:
        from coset_typical_commutant_moment_audit import moment_signature_counts

        direct_types, direct_first, direct_second, direct_orbit_size = (
            moment_signature_counts(n, GENERATOR_ID)
        )
        factorial_first_verified = (
            direct_types == cycle_types
            and direct_orbit_size == orbit_size
            and np.array_equal(direct_first, first_counts)
        )
        factorial_second_verified = np.array_equal(direct_second, second_counts)
        if not factorial_first_verified or not factorial_second_verified:
            raise ArithmeticError("class-compressed signatures disagree with factorial control")

    source = _maximum_dimension_partition(n)
    source_dimension = hook_length_dimension(source)
    rows: list[tuple[tuple[int, ...], int, Fraction]] = []
    for target in integer_partitions(n):
        multiplicity = kronecker_coefficient(source, source, target)
        if multiplicity <= 1:
            continue
        trace = Fraction(
            _character_contraction(first_counts, cycle_types, source, target),
            math.factorial(n),
        )
        trace_square = Fraction(
            _character_contraction(second_counts, cycle_types, source, target),
            math.factorial(n) * orbit_size,
        )
        mean = trace / multiplicity
        variance = trace_square / multiplicity - mean * mean
        if variance < 0:
            raise ArithmeticError("exact class-compressed variance is negative")
        rows.append((target, multiplicity, variance))
    scalar = [row for row in rows if row[2] == 0]
    positive = [row for row in rows if row[2] > 0]
    support_profile = Counter(
        pair_support_size(key) for key, _ in relative_pair_type_counts(n)
    )
    return ClassContractionScalingRecord(
        n=n,
        source_partition=source,
        source_dimension=source_dimension,
        partition_count=len(cycle_types),
        orbit_size=orbit_size,
        relative_pair_type_count=len(relative_pair_type_counts(n)),
        relative_pair_support_profile={
            str(support): count for support, count in sorted(support_profile.items())
        },
        first_moment_signature_count=int(np.count_nonzero(first_counts)),
        second_moment_signature_count=int(np.count_nonzero(second_counts)),
        first_signature_total_verified=True,
        second_signature_total_verified=True,
        factorial_signature_verification_performed=factorial_verification_performed,
        factorial_first_signature_verified=factorial_first_verified,
        factorial_second_signature_verified=factorial_second_verified,
        nontrivial_multiplicity_block_count=len(rows),
        non_scalar_block_count=len(positive),
        exact_scalar_block_count=len(scalar),
        exact_scalar_targets=[row[0] for row in scalar],
        exact_scalar_target_multiplicities=[row[1] for row in scalar],
        minimum_positive_variance=float(
            min((row[2] for row in positive), default=Fraction())
        ),
        maximum_variance=float(
            max((row[2] for row in positive), default=Fraction())
        ),
        maximum_kronecker_multiplicity=max(
            (row[1] for row in rows), default=0
        ),
        finite_exact_character_contraction_only=True,
        status=(
            "primary-generator-exact-scalar-blocks-found"
            if scalar
            else "primary-generator-finite-non-scalar-all-blocks"
        ),
    )


@lru_cache(maxsize=None)
def audit_class_contraction_portfolio(
    n: int,
) -> ClassContractionPortfolioRecord:
    cycle_types, primary_first, primary_second, primary_orbit_size = (
        primary_class_signature_counts(n)
    )
    (
        shared_cycle_types,
        shared_first,
        shared_second,
        shared_orbit_size,
        shared_relative_type_count,
    ) = shared_transposition_class_signature_counts(n)
    (
        cross_cycle_types,
        cross_counts,
        cross_orbit_size,
        cross_relative_type_count,
    ) = primary_shared_cross_signature_counts(n)
    if cycle_types != shared_cycle_types or cycle_types != cross_cycle_types:
        raise ArithmeticError("portfolio cycle-type orders disagree")
    source = _maximum_dimension_partition(n)
    source_dimension = hook_length_dimension(source)
    primary_scalar: list[tuple[int, ...]] = []
    shared_scalar: list[tuple[int, ...]] = []
    both_scalar: list[tuple[int, ...]] = []
    rank_one: list[tuple[int, ...]] = []
    positive_determinants: list[Fraction] = []
    block_count = 0
    rank_two_count = 0
    for target in integer_partitions(n):
        multiplicity = kronecker_coefficient(source, source, target)
        if multiplicity <= 1:
            continue
        block_count += 1
        denominator = math.factorial(n) * multiplicity
        primary_mean = Fraction(
            _character_contraction(
                primary_first, cycle_types, source, target
            ),
            denominator,
        )
        primary_variance = Fraction(
            _character_contraction(
                primary_second, cycle_types, source, target
            ),
            denominator * primary_orbit_size,
        ) - primary_mean * primary_mean
        shared_mean = Fraction(
            _character_contraction(shared_first, cycle_types, source, target),
            denominator,
        )
        shared_variance = Fraction(
            _character_contraction(shared_second, cycle_types, source, target),
            denominator * shared_orbit_size,
        ) - shared_mean * shared_mean
        covariance = Fraction(
            _character_contraction(cross_counts, cycle_types, source, target),
            denominator * cross_orbit_size,
        ) - primary_mean * shared_mean
        determinant = primary_variance * shared_variance - covariance * covariance
        if primary_variance < 0 or shared_variance < 0 or determinant < 0:
            raise ArithmeticError("portfolio covariance matrix is not positive semidefinite")
        if primary_variance == 0:
            primary_scalar.append(target)
        if shared_variance == 0:
            shared_scalar.append(target)
        if primary_variance == 0 and shared_variance == 0:
            both_scalar.append(target)
        if determinant > 0:
            rank_two_count += 1
            positive_determinants.append(determinant)
        elif primary_variance > 0 or shared_variance > 0:
            rank_one.append(target)
    covered = block_count - len(both_scalar)
    return ClassContractionPortfolioRecord(
        n=n,
        source_partition=source,
        source_dimension=source_dimension,
        nontrivial_multiplicity_block_count=block_count,
        primary_scalar_targets=primary_scalar,
        shared_transposition_scalar_targets=shared_scalar,
        both_generators_scalar_targets=both_scalar,
        finite_portfolio_non_scalar_covered_count=covered,
        centered_covariance_rank_two_count=rank_two_count,
        centered_covariance_rank_one_targets=rank_one,
        minimum_positive_covariance_determinant=float(
            min(positive_determinants, default=Fraction())
        ),
        primary_shared_cross_signature_count=int(np.count_nonzero(cross_counts)),
        primary_shared_relative_pair_type_count=cross_relative_type_count,
        shared_self_relative_pair_type_count=shared_relative_type_count,
        finite_two_generator_moment_only=True,
        status=(
            "finite-low-support-portfolio-non-scalar-covered-joint-gap-open"
            if not both_scalar
            else "finite-low-support-portfolio-has-common-scalar-blocks"
        ),
    )


@lru_cache(maxsize=1)
def build_class_contraction_scaling_report(
    n_values: tuple[int, ...] = (6, 7, 8, 9, 10),
) -> ClassContractionScalingReport:
    records = [audit_class_contraction_scaling(n) for n in n_values]
    portfolio_records = [audit_class_contraction_portfolio(n) for n in n_values]
    scalar_records = [record for record in records if record.exact_scalar_block_count]
    scalar_total = sum(record.exact_scalar_block_count for record in records)
    metrics: dict[str, int | float] = {
        "class_compressed_record_count": len(records),
        "maximum_n": max(n_values),
        "factorial_signature_verification_count": sum(
            record.factorial_first_signature_verified
            and record.factorial_second_signature_verified
            for record in records
        ),
        "fixed_relative_pair_type_count": max(
            record.relative_pair_type_count for record in records
        ),
        "total_nontrivial_multiplicity_block_count": sum(
            record.nontrivial_multiplicity_block_count for record in records
        ),
        "total_exact_scalar_block_count": scalar_total,
        "maximum_exact_scalar_block_count_per_n": max(
            record.exact_scalar_block_count for record in records
        ),
        "first_scalar_n": min(
            (record.n for record in scalar_records), default=0
        ),
        "single_primary_generator_uniformity_falsification_count": int(
            bool(scalar_records)
        ),
        "all_n_symbolic_class_contraction_formula_count": 0,
        "uniform_primary_generator_non_scalar_theorem_count": 0,
        "uniform_portfolio_joint_gap_theorem_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
        "finite_portfolio_block_count": sum(
            record.nontrivial_multiplicity_block_count
            for record in portfolio_records
        ),
        "finite_portfolio_non_scalar_covered_count": sum(
            record.finite_portfolio_non_scalar_covered_count
            for record in portfolio_records
        ),
        "finite_portfolio_common_scalar_block_count": sum(
            len(record.both_generators_scalar_targets)
            for record in portfolio_records
        ),
        "finite_portfolio_covariance_rank_two_count": sum(
            record.centered_covariance_rank_two_count
            for record in portfolio_records
        ),
        "finite_portfolio_rank_one_block_count": sum(
            len(record.centered_covariance_rank_one_targets)
            for record in portfolio_records
        ),
        "shared_transposition_single_generator_scalar_block_count": sum(
            len(record.shared_transposition_scalar_targets)
            for record in portfolio_records
        ),
    }
    return ClassContractionScalingReport(
        created_at=utc_now(),
        contraction_contract={
            "first_moment_method": (
                "Enumerate marked-support injections into one canonical representative of each S_n conjugacy class."
            ),
            "second_moment_method": (
                "Classify O^-1 O relative products into 17 simultaneous-conjugacy pair types, then reuse the marked-class contraction."
            ),
            "maximum_marked_support": 6,
            "finite_evaluator_cost": "O(p(n) n^6) for the primary second moment, excluding character evaluation",
            "factorial_enumeration_used_above_n8": False,
            "bit_polynomial_circuit_claimed": False,
            "next_symbolic_target": (
                "Derive character-polynomial or partition-algebra recurrences for the 17 relative pair types and extend the fixed generator portfolio."
            ),
        },
        records=records,
        portfolio_records=portfolio_records,
        headline_metrics=metrics,
        claim_gate={
            "factorial_enumeration_removed_for_primary_moments": True,
            "single_primary_generator_uniformly_non_scalar": False,
            "fixed_portfolio_uniform_joint_spectrum_proved": False,
            "finite_low_support_portfolio_non_scalar_coverage": all(
                not record.both_generators_scalar_targets
                for record in portfolio_records
            ),
            "finite_portfolio_non_scalar_coverage_is_joint_spectrum_proof": False,
            "inverse_polynomial_joint_gap_proved": False,
            "coherent_label_adaptive_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Class compression extends exact moments to n=10 and finds recurring scalar blocks, falsifying the "
                "single-generator route. A two-generator support-three portfolio repairs finite scalar coverage but "
                "still lacks all-n joint-spectrum, gap, circuit, and decoder theorems."
            ),
        },
        status="single-primary-generator-falsified-portfolio-class-algebra-open",
        summary=(
            f"Class-compressed exact moments audited {metrics['total_nontrivial_multiplicity_block_count']} typical "
            f"multiplicity blocks through n={metrics['maximum_n']} and found {scalar_total} exact scalar blocks; "
            f"the single primary generator is not uniform. The low-support portfolio covers "
            f"{metrics['finite_portfolio_non_scalar_covered_count']}/"
            f"{metrics['finite_portfolio_block_count']} finite blocks without common scalar action."
        ),
        falsifiers_triggered=[
            "The primary intersection-two orbit average splits all n=7 blocks but has exact scalar targets at n=6, n=8, n=9, and n=10.",
            "Finite simple spectrum at one size does not extrapolate even to non-scalarity at the next size.",
            "Removing factorial group enumeration does not construct a coherent multiplicity transform.",
            "A fixed portfolio needs joint-spectrum and minimum-gap control, not separate nonzero variances.",
            "The shared-point transposition generator has its own scalar hook targets, so it is not a replacement single generator.",
            "No hidden-involution information theorem follows from class-compressed character moments.",
        ],
    )


def write_class_contraction_scaling_report(
    output_path: Path = COSET_TYPICAL_CLASS_CONTRACTION_PATH,
    n_values: tuple[int, ...] = (6, 7, 8, 9, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_class_contraction_scaling_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-SINGLE-TC2-GENERATOR-UNIFORMITY",
                source=str(output_path),
                claim=(
                    "The normalized transposition/3-cycle intersection-two orbit average alone resolves every typical Kronecker multiplicity block uniformly."
                ),
                reason_invalid=(
                    "Class-compressed exact second moments find zero variance on two n=6 targets, two n=8 targets, one n=9 target, and two n=10 targets despite full n=7 splitting."
                ),
                lesson=(
                    "Reject one-generator extrapolation. Search a fixed portfolio only under all-n joint-spectrum, gap, natural-access, and decoder obligations."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-SINGLE-TT1-GENERATOR-UNIFORMITY",
                source=str(output_path),
                claim=(
                    "The shared-point transposition-pair orbit average alone resolves every typical Kronecker multiplicity block uniformly."
                ),
                reason_invalid=(
                    "Its exact variance vanishes on hook and conjugate-hook targets throughout the audited scaling rows, although it repairs the primary generator's scalar blocks."
                ),
                lesson=(
                    "Retain both support-three generators only as a finite portfolio. Require joint algebra generation and all-n gap control."
                ),
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
                artifacts={"coset_typical_class_contraction_scaling": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_class_contraction_scaling_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
