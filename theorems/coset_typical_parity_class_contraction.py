"""Exact all-source moments for the parity-complete coset separator.

The finite separator

    H_pc = TC2 + CT1 - 2 CT2

uses three normalized simultaneous-conjugacy orbit averages.  Dense Young
matrices found no collision through n=7, but that evidence was numerical.
This module contracts the first two moments against symmetric-group
characters after compressing every bounded-support product by simultaneous
conjugacy class.  It therefore tests every ordered source pair and every
nontrivial Kronecker target without enumerating S_n.

Zero variance is an exact scalar obstruction.  Positive variance proves a
simple spectrum only for multiplicity two; higher-multiplicity square-free
spectra, inverse-polynomial gaps, coherent implementation, and decoding remain
separate obligations.
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

from coset_typical_parity_complete_separator import (
    DISCOVERY_COEFFICIENTS,
    GENERATOR_NAMES,
    _oriented_orbit,
    exact_portfolio_mean_variance,
)
from representation_obstruction import integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient, symmetric_character
from symmetric_marked_class_contraction import (
    canonical_pair_key,
    class_compressed_signature_counts,
    compose,
    pair_support_size,
)


REPORT_PATH = Path(
    "research/representation/"
    "coset_typical_parity_class_contraction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-TYPICAL-PARITY-CLASS-CONTRACTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
def active_coefficients(
    coefficients: tuple[int, ...] = DISCOVERY_COEFFICIENTS,
) -> tuple[tuple[str, int], ...]:
    if len(coefficients) != len(GENERATOR_NAMES):
        raise ValueError("coefficient vector has the wrong length")
    return tuple(
        (name, coefficient)
        for name, coefficient in zip(GENERATOR_NAMES, coefficients)
        if coefficient
    )


ACTIVE_COEFFICIENTS = active_coefficients()


@dataclass(frozen=True)
class ScalarObstructionRecord:
    n: int
    left_source: tuple[int, ...]
    right_source: tuple[int, ...]
    target: tuple[int, ...]
    kronecker_multiplicity: int
    exact_mean: str
    exact_variance: str
    status: str


@dataclass(frozen=True)
class ParityClassContractionSizeRecord:
    n: int
    partition_count: int
    ordered_source_pair_count: int
    nontrivial_kronecker_block_count: int
    maximum_kronecker_multiplicity: int
    exact_non_scalar_block_count: int
    exact_scalar_block_count: int
    multiplicity_two_block_count: int
    exact_multiplicity_two_simple_spectrum_count: int
    higher_multiplicity_non_scalar_but_square_free_open_count: int
    minimum_positive_exact_variance: str
    minimum_multiplicity_two_raw_gap_lower_bound: float
    maximum_relative_pair_support: int
    relative_pair_type_count: int
    class_signature_nonzero_count: int
    factorial_control_count: int
    scalar_obstructions: list[ScalarObstructionRecord]
    status: str


@dataclass(frozen=True)
class ParityClassContractionReport:
    created_at: str
    contraction_contract: dict[str, object]
    obstruction_symmetry: dict[str, object]
    records: list[ParityClassContractionSizeRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def conjugate_partition(
    partition: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        sum(row >= column for row in partition)
        for column in range(1, partition[0] + 1)
    )


def even_sign_twists(
    block: tuple[
        tuple[int, ...], tuple[int, ...], tuple[int, ...]
    ],
) -> tuple[
    tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
    ...,
]:
    left, right, target = block
    return (
        (
            conjugate_partition(left),
            conjugate_partition(right),
            target,
        ),
        (
            conjugate_partition(left),
            right,
            conjugate_partition(target),
        ),
        (
            left,
            conjugate_partition(right),
            conjugate_partition(target),
        ),
    )


def analyze_obstruction_symmetry(
    scalar_blocks: set[
        tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
    ],
) -> dict[str, object]:
    unseen = set(scalar_blocks)
    symmetry_orbits: list[
        set[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]]
    ] = []
    while unseen:
        seed = next(iter(unseen))
        orbit: set[
            tuple[
                tuple[int, ...],
                tuple[int, ...],
                tuple[int, ...],
            ]
        ] = set()
        pending = [seed]
        while pending:
            block = pending.pop()
            if block in orbit:
                continue
            orbit.add(block)
            pending.extend(
                twisted
                for twisted in even_sign_twists(block)
                if twisted in scalar_blocks
            )
        unseen.difference_update(orbit)
        symmetry_orbits.append(orbit)
    sign_twist_closed = all(
        twisted in scalar_blocks
        for block in scalar_blocks
        for twisted in even_sign_twists(block)
    )
    source_swap_closed = all(
        (right, left, target) in scalar_blocks
        for left, right, target in scalar_blocks
    )
    return {
        "even_sign_twist_action": (
            "Conjugate any two of (left source, right source, target); "
            "the Kronecker multiplicity is unchanged."
        ),
        "closed_under_even_sign_twists": sign_twist_closed,
        "orbit_count": len(symmetry_orbits),
        "orbit_sizes": sorted(
            (len(orbit) for orbit in symmetry_orbits),
            reverse=True,
        ),
        "closed_under_source_swap": source_swap_closed,
        "interpretation": (
            "The exact obstructions form representation-theoretic "
            "families rather than isolated numerical failures. Source "
            "swap fails because the frozen TC/CT coefficients are "
            "orientation-asymmetric."
        ),
    }


def _weighted_class_counts(
    n: int,
    base_left: tuple[int, ...],
    base_right: tuple[int, ...],
    orbit: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
) -> tuple[
    tuple[tuple[int, ...], ...],
    np.ndarray,
    int,
    int,
]:
    relative = Counter(
        canonical_pair_key(
            compose(base_left, orbit_left),
            compose(base_right, orbit_right),
        )
        for orbit_left, orbit_right in orbit
    )
    cycle_types: tuple[tuple[int, ...], ...] | None = None
    counts: np.ndarray | None = None
    maximum_support = 0
    for key, weight in relative.items():
        key_cycle_types, key_counts = class_compressed_signature_counts(
            n, key
        )
        if counts is None:
            cycle_types = key_cycle_types
            counts = np.zeros_like(key_counts)
        elif cycle_types != key_cycle_types:
            raise ArithmeticError("cycle-type order changed")
        counts += weight * key_counts
        maximum_support = max(maximum_support, pair_support_size(key))
    if cycle_types is None or counts is None:
        raise ArithmeticError("oriented generator orbit is empty")
    if int(counts.sum()) != math.factorial(n) * len(orbit):
        raise ArithmeticError("class counts do not sum to |S_n||O|")
    return cycle_types, counts, len(relative), maximum_support


@lru_cache(maxsize=None)
def oriented_first_class_counts(
    n: int, generator_name: str
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray]:
    base_left, base_right, _ = _oriented_orbit(n, generator_name)
    return class_compressed_signature_counts(
        n, canonical_pair_key(base_left, base_right)
    )


@lru_cache(maxsize=None)
def oriented_cross_class_counts(
    n: int,
    left_generator_name: str,
    right_generator_name: str,
) -> tuple[
    tuple[tuple[int, ...], ...],
    np.ndarray,
    int,
    int,
    int,
]:
    base_left, base_right, _ = _oriented_orbit(
        n, left_generator_name
    )
    _, _, right_orbit = _oriented_orbit(
        n, right_generator_name
    )
    cycle_types, counts, type_count, maximum_support = (
        _weighted_class_counts(
            n, base_left, base_right, right_orbit
        )
    )
    return (
        cycle_types,
        counts,
        len(right_orbit),
        type_count,
        maximum_support,
    )


@lru_cache(maxsize=None)
def _character_vector(
    partition: tuple[int, ...],
    cycle_types: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    return tuple(
        symmetric_character(partition, cycle_type)
        for cycle_type in cycle_types
    )


def _bicharacter_contraction(
    counts: np.ndarray,
    cycle_types: tuple[tuple[int, ...], ...],
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
) -> int:
    type_count = len(cycle_types)
    left_characters = _character_vector(left_source, cycle_types)
    right_characters = _character_vector(right_source, cycle_types)
    target_characters = _character_vector(target, cycle_types)
    total = 0
    for code in np.flatnonzero(counts):
        group_index, remainder = divmod(
            int(code), type_count * type_count
        )
        left_index, right_index = divmod(remainder, type_count)
        total += (
            int(counts[code])
            * target_characters[group_index]
            * left_characters[left_index]
            * right_characters[right_index]
        )
    return total


@lru_cache(maxsize=None)
def exact_class_portfolio_mean_variance(
    n: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
    coefficients: tuple[int, ...] = DISCOVERY_COEFFICIENTS,
) -> tuple[Fraction, Fraction]:
    multiplicity = kronecker_coefficient(
        left_source, right_source, target
    )
    if multiplicity <= 1:
        raise ValueError("nontrivial Kronecker multiplicity required")
    group_order = math.factorial(n)
    trace = Fraction()
    active = active_coefficients(coefficients)
    for generator_name, coefficient in active:
        cycle_types, counts = oriented_first_class_counts(
            n, generator_name
        )
        trace += coefficient * Fraction(
            _bicharacter_contraction(
                counts,
                cycle_types,
                left_source,
                right_source,
                target,
            ),
            group_order,
        )

    trace_square = Fraction()
    for left_index, (
        left_name,
        left_coefficient,
    ) in enumerate(active):
        for right_index in range(
            left_index, len(active)
        ):
            right_name, right_coefficient = active[
                right_index
            ]
            (
                cycle_types,
                counts,
                orbit_size,
                _,
                _,
            ) = oriented_cross_class_counts(
                n, left_name, right_name
            )
            cross_trace = Fraction(
                _bicharacter_contraction(
                    counts,
                    cycle_types,
                    left_source,
                    right_source,
                    target,
                ),
                group_order * orbit_size,
            )
            symmetry_factor = (
                1 if left_index == right_index else 2
            )
            trace_square += (
                symmetry_factor
                * left_coefficient
                * right_coefficient
                * cross_trace
            )

    mean = trace / multiplicity
    variance = trace_square / multiplicity - mean * mean
    if variance < 0:
        raise ArithmeticError(
            "exact parity-complete variance is negative"
        )
    return mean, variance


@lru_cache(maxsize=None)
def audit_parity_class_contraction_size(
    n: int,
) -> ParityClassContractionSizeRecord:
    if n < 5:
        raise ValueError("parity contraction audit requires n>=5")
    partitions = integer_partitions(n)
    scalar: list[ScalarObstructionRecord] = []
    nontrivial_count = 0
    multiplicity_two_count = 0
    multiplicity_two_simple = 0
    higher_non_scalar = 0
    maximum_multiplicity = 0
    positive_variances: list[Fraction] = []
    multiplicity_two_gaps: list[float] = []
    factorial_controls = 0

    for left_source in partitions:
        for right_source in partitions:
            for target in partitions:
                multiplicity = kronecker_coefficient(
                    left_source, right_source, target
                )
                if multiplicity <= 1:
                    continue
                nontrivial_count += 1
                maximum_multiplicity = max(
                    maximum_multiplicity, multiplicity
                )
                mean, variance = (
                    exact_class_portfolio_mean_variance(
                        n, left_source, right_source, target
                    )
                )
                if n <= 7 and factorial_controls < 12:
                    direct_mean, direct_variance = (
                        exact_portfolio_mean_variance(
                            n,
                            left_source,
                            right_source,
                            target,
                        )
                    )
                    if (mean, variance) != (
                        direct_mean,
                        direct_variance,
                    ):
                        raise ArithmeticError(
                            "class contraction disagrees with factorial control"
                        )
                    factorial_controls += 1
                if multiplicity == 2:
                    multiplicity_two_count += 1
                if variance == 0:
                    scalar.append(
                        ScalarObstructionRecord(
                            n=n,
                            left_source=left_source,
                            right_source=right_source,
                            target=target,
                            kronecker_multiplicity=multiplicity,
                            exact_mean=str(mean),
                            exact_variance=str(variance),
                            status="exact-scalar-obstruction",
                        )
                    )
                    continue
                positive_variances.append(variance)
                if multiplicity == 2:
                    multiplicity_two_simple += 1
                    multiplicity_two_gaps.append(
                        2 * math.sqrt(float(variance))
                    )
                else:
                    higher_non_scalar += 1

    relative_type_count = 0
    maximum_support = 0
    signature_nonzero_count = 0
    for left_index, (left_name, _) in enumerate(
        ACTIVE_COEFFICIENTS
    ):
        first_types, first_counts = oriented_first_class_counts(
            n, left_name
        )
        signature_nonzero_count += int(
            np.count_nonzero(first_counts)
        )
        if len(first_types) != len(partitions):
            raise ArithmeticError("partition count changed")
        for right_index in range(
            left_index, len(ACTIVE_COEFFICIENTS)
        ):
            right_name = ACTIVE_COEFFICIENTS[right_index][0]
            (
                _,
                cross_counts,
                _,
                pair_type_count,
                pair_support,
            ) = oriented_cross_class_counts(
                n, left_name, right_name
            )
            relative_type_count += pair_type_count
            maximum_support = max(maximum_support, pair_support)
            signature_nonzero_count += int(
                np.count_nonzero(cross_counts)
            )

    return ParityClassContractionSizeRecord(
        n=n,
        partition_count=len(partitions),
        ordered_source_pair_count=len(partitions) ** 2,
        nontrivial_kronecker_block_count=nontrivial_count,
        maximum_kronecker_multiplicity=maximum_multiplicity,
        exact_non_scalar_block_count=(
            nontrivial_count - len(scalar)
        ),
        exact_scalar_block_count=len(scalar),
        multiplicity_two_block_count=multiplicity_two_count,
        exact_multiplicity_two_simple_spectrum_count=(
            multiplicity_two_simple
        ),
        higher_multiplicity_non_scalar_but_square_free_open_count=(
            higher_non_scalar
        ),
        minimum_positive_exact_variance=str(
            min(positive_variances, default=Fraction())
        ),
        minimum_multiplicity_two_raw_gap_lower_bound=min(
            multiplicity_two_gaps, default=0.0
        ),
        maximum_relative_pair_support=maximum_support,
        relative_pair_type_count=relative_type_count,
        class_signature_nonzero_count=signature_nonzero_count,
        factorial_control_count=factorial_controls,
        scalar_obstructions=scalar,
        status=(
            "exact-scalar-obstruction-found"
            if scalar
            else "all-blocks-exactly-non-scalar-square-free-open"
        ),
    )


def build_parity_class_contraction_report(
    n_values: tuple[int, ...] = (5, 6, 7, 8),
) -> ParityClassContractionReport:
    records = [
        audit_parity_class_contraction_size(n)
        for n in n_values
    ]
    scalar_count = sum(
        record.exact_scalar_block_count for record in records
    )
    nontrivial_count = sum(
        record.nontrivial_kronecker_block_count
        for record in records
    )
    multiplicity_two_count = sum(
        record.multiplicity_two_block_count
        for record in records
    )
    multiplicity_two_simple = sum(
        record.exact_multiplicity_two_simple_spectrum_count
        for record in records
    )
    scalar_blocks = {
        (
            obstruction.left_source,
            obstruction.right_source,
            obstruction.target,
        )
        for record in records
        for obstruction in record.scalar_obstructions
    }

    obstruction_symmetry = analyze_obstruction_symmetry(
        scalar_blocks
    )
    metrics: dict[str, int | float] = {
        "finite_n_count": len(records),
        "maximum_n": max(n_values),
        "all_source_exact_block_count": nontrivial_count,
        "exact_non_scalar_block_count": (
            nontrivial_count - scalar_count
        ),
        "exact_scalar_obstruction_count": scalar_count,
        "exact_scalar_obstruction_symmetry_orbit_count": len(
            obstruction_symmetry["orbit_sizes"]
        ),
        "even_sign_twist_closure_verified_count": int(
            obstruction_symmetry[
                "closed_under_even_sign_twists"
            ]
        ),
        "source_swap_closure_verified_count": int(
            obstruction_symmetry["closed_under_source_swap"]
        ),
        "multiplicity_two_block_count": multiplicity_two_count,
        "exact_multiplicity_two_simple_spectrum_count": (
            multiplicity_two_simple
        ),
        "higher_multiplicity_square_free_theorem_count": 0,
        "maximum_kronecker_multiplicity": max(
            record.maximum_kronecker_multiplicity
            for record in records
        ),
        "maximum_relative_pair_support": max(
            record.maximum_relative_pair_support
            for record in records
        ),
        "factorial_control_count": sum(
            record.factorial_control_count for record in records
        ),
        "all_n_square_free_theorem_count": 0,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
        "coherent_internal_eigenbasis_transform_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return ParityClassContractionReport(
        created_at=utc_now(),
        contraction_contract={
            "operator": "TC2+CT1-2*CT2",
            "source_scope": (
                "Every ordered source-partition pair."
            ),
            "target_scope": (
                "Every target with Kronecker multiplicity above one."
            ),
            "group_enumeration": (
                "Removed: bounded-support products are compressed by "
                "conjugacy class and marked injections."
            ),
            "exact_certificate": (
                "Zero variance proves scalar action. Positive variance "
                "proves simple spectrum only at multiplicity two."
            ),
            "remaining_cost": (
                "Partition enumeration, Kronecker coefficients, and "
                "marked injections; no polynomial bit-complexity claim."
            ),
        },
        obstruction_symmetry=obstruction_symmetry,
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "factorial_group_enumeration_removed": True,
            "finite_all_source_scalar_obstruction_absent": (
                scalar_count == 0
            ),
            "all_multiplicity_two_blocks_exactly_split": (
                multiplicity_two_count == multiplicity_two_simple
            ),
            "higher_multiplicity_square_free_proved": False,
            "all_n_square_free_proved": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "coherent_internal_eigenbasis_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact class contractions can kill the finite separator "
                "if any scalar block appears. Surviving second moments "
                "still cannot certify square-free spectra in "
                "higher-multiplicity blocks or any asymptotic decoder."
            ),
        },
        status=(
            "parity-complete-exact-scalar-obstruction-found"
            if scalar_count
            else (
                "parity-complete-exactly-nonscalar-through-"
                f"n{max(n_values)}-higher-moments-required"
            )
        ),
        summary=(
            f"Audited {nontrivial_count} all-source nontrivial blocks "
            f"through n={max(n_values)} by exact class contraction; "
            f"found {scalar_count} exact scalar obstructions and proved "
            f"{multiplicity_two_simple}/{multiplicity_two_count} "
            "multiplicity-two spectra simple."
        ),
        falsifiers_triggered=[
            *(
                [
                    "The parity-complete separator has an exact scalar block in the audited range."
                ]
                if scalar_count
                else []
            ),
            "Positive second-moment variance does not prove a square-free spectrum above multiplicity two.",
            "Finite exact non-scalarity does not prove an all-n normalized gap, coherent transform, or decoder.",
        ],
    )


def write_parity_class_contraction_report(
    output_path: Path = REPORT_PATH,
    n_values: tuple[int, ...] = (5, 6, 7, 8),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(
        build_parity_class_contraction_report(n_values=n_values)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    if write_registry:
        negative_id = (
            "NEG-COSET-PARITY-COMPLETE-EXACT-SCALAR-OBSTRUCTION"
            if payload["headline_metrics"][
                "exact_scalar_obstruction_count"
            ]
            else "NEG-COSET-PARITY-SECOND-MOMENT-NOT-SQUARE-FREE"
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=negative_id,
                source=str(output_path),
                claim=(
                    (
                        "The frozen TC2+CT1-2CT2 separator remains "
                        "non-scalar on the independent all-source holdout."
                    )
                    if payload["headline_metrics"][
                        "exact_scalar_obstruction_count"
                    ]
                    else (
                        "Exact positive second-moment variance of the "
                        "parity-complete separator supplies a uniform "
                        "Kronecker multiplicity decoder."
                    )
                ),
                reason_invalid=(
                    (
                        "Ten multiplicity-two n=8 blocks have exact zero "
                        "variance, directly falsifying the frozen rule."
                    )
                    if payload["headline_metrics"][
                        "exact_scalar_obstruction_count"
                    ]
                    else (
                        "Higher-multiplicity blocks require characteristic "
                        "polynomials or enough exact moments; all-n gaps and "
                        "coherent diagonalization are also unresolved."
                    )
                ),
                lesson=(
                    "Do not refit bounded finite separator coefficients "
                    "without an all-n algebraic construction; prioritize "
                    "growing-width carrier-sensitive outcomes."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                ],
                evidence=payload["headline_metrics"],
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
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload[
                    "falsifiers_triggered"
                ],
                artifacts={
                    "coset_typical_parity_class_contraction": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_parity_class_contraction_report()
    print(
        json.dumps(
            report["headline_metrics"], indent=2, sort_keys=True
        )
    )
