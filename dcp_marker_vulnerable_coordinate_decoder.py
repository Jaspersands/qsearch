"""Growing-depth polynomial marker decoder on vulnerable LLL coordinates.

Fixed-depth nearest-plane lists allow rounding deviations at any constant
number of Gram-Schmidt coordinates.  This module tests a different polynomial
class: rank the coordinates by a public, target-independent Rademacher-risk
score, retain ``c ceil(log2 n)`` coordinates, and branch by a bounded amount at
every retained coordinate.  For constant ``c`` and offset radius ``q`` the
list has

    (2q + 1) ** (c ceil(log2 n)) = poly(n)

paths.  Carry slicing adds at most a linear factor.

The selector can absorb a growing number of rounding deviations, but only
inside a logarithmic-dimensional public subspace.  The report therefore
measures both assignment-weighted witness coverage and exact uniform-legal
target coverage.  These are linked, for every fixed label row, by the
deterministic sandwich

    max(0, 1 - mu (1-q)) <= p <= min(1, mu q),

where ``q`` is the fraction of Boolean assignments accepted by the selected
cell union, ``p`` is the fraction of legal targets covered, and
``mu = 2^m / |legal targets|`` is the mean legal-fiber multiplicity.

Finite decay is a falsifier for this decoder class, not a lower bound against
general affine-CVP or quantum subset-sum algorithms.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from sympy import Matrix

from dcp_marker_all_target_coverage import (
    IntegerProjectionRow,
    _nearest_integer_ratio,
    _reduced_projection_families,
    integer_projection_rows,
)
from dcp_marker_aware_list_decoder import NearestPlaneListCandidate
from dcp_subset_sum_affine_cvp_baseline import exact_gram_schmidt_rows
from dcp_subset_sum_carry_slice_lattice import (
    carry_sliced_embedding,
    constrained_low_bits,
    decode_carry_sliced_vector,
    reachable_carries,
)
from dcp_subset_sum_lattice_search import modular_subset_sum_embedding
from dcp_subset_sum_marker_coset_theorem import (
    decode_short_standard_marker_vector,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_MARKER_VULNERABLE_COORDINATE_PATH = Path(
    "research/classical_baselines/dcp_marker_vulnerable_coordinate_decoder.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-MARKER-VULNERABLE-COORDINATE-DECODER"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class VulnerableCoordinateTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    selector_multiplier: int
    maximum_offset: int
    standard_rank: int
    carry_rank: int
    standard_selected_coordinates: list[int]
    carry_selected_coordinates: list[int]
    standard_selected_risk_scores: list[float]
    carry_selected_risk_scores: list[float]
    standard_candidate_count: int
    carry_candidate_count: int
    carry_factor_upper_bound: int
    total_candidate_count_upper_bound: int
    assignment_sample_count: int
    standard_sampled_assignment_coverage: float
    carry_sampled_assignment_coverage: float
    standard_sampled_fixed_depth_coverage: float
    carry_sampled_fixed_depth_coverage: float
    standard_sampled_offset_escape_fraction: float
    carry_sampled_offset_escape_fraction: float
    exact_full_cube_enumerated: bool
    exact_assignment_count: int
    exact_legal_target_count: int
    mean_legal_fiber_multiplicity: float | None
    standard_exact_assignment_coverage: float | None
    carry_exact_assignment_coverage: float | None
    standard_exact_uniform_legal_target_coverage: float | None
    carry_exact_uniform_legal_target_coverage: float | None
    standard_exact_fixed_depth_target_coverage: float | None
    carry_exact_fixed_depth_target_coverage: float | None
    standard_transfer_lower_bound: float | None
    standard_transfer_upper_bound: float | None
    carry_transfer_lower_bound: float | None
    carry_transfer_upper_bound: float | None
    transfer_sandwich_verified: bool | None
    source_is_independent_uniform_target_when_exact: bool


@dataclass(frozen=True)
class VulnerableCoordinateDecodeOutcome:
    selected_coordinate_count: int
    candidate_count: int
    theoretical_candidate_count: int
    candidate_count_matches_theorem: bool
    valid_witness_candidate_count: int
    invalid_witness_count: int
    solved: bool
    reachable_carry_count: int


@dataclass(frozen=True)
class VulnerableCoordinateScalingRow:
    n_bits: int
    register_offset: int
    trial_count: int
    selected_coordinate_count: int
    mean_standard_sampled_assignment_coverage: float
    mean_carry_sampled_assignment_coverage: float
    minimum_standard_sampled_assignment_coverage: float
    maximum_standard_sampled_assignment_coverage: float
    minimum_carry_sampled_assignment_coverage: float
    maximum_carry_sampled_assignment_coverage: float
    mean_standard_sampled_fixed_depth_coverage: float
    mean_carry_sampled_fixed_depth_coverage: float
    mean_standard_offset_escape_fraction: float
    mean_carry_offset_escape_fraction: float
    exact_trial_count: int
    mean_standard_exact_uniform_legal_target_coverage: float | None
    mean_carry_exact_uniform_legal_target_coverage: float | None
    maximum_total_candidate_count_upper_bound: int
    finite_row_is_asymptotic_source_law: bool


@dataclass(frozen=True)
class DCPMarkerVulnerableCoordinateReport:
    created_at: str
    decoder_contract: dict[str, str]
    transfer_theorem: dict[str, str | bool]
    rows: list[VulnerableCoordinateScalingRow]
    trials: list[VulnerableCoordinateTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def vulnerable_coordinate_count(n_bits: int, multiplier: int, rank: int) -> int:
    if n_bits < 2 or multiplier < 1 or rank < 1:
        raise ValueError("requires n_bits>=2, multiplier>=1, and rank>=1")
    return min(rank, multiplier * math.ceil(math.log2(n_bits)))


def vulnerable_list_candidate_count(
    n_bits: int,
    multiplier: int,
    rank: int,
    maximum_offset: int,
) -> int:
    if maximum_offset < 0:
        raise ValueError("maximum_offset must be nonnegative")
    selected = vulnerable_coordinate_count(n_bits, multiplier, rank)
    return (2 * maximum_offset + 1) ** selected


def coordinate_risk_score(
    projection: IntegerProjectionRow,
    register_count: int,
) -> float:
    """Return variance divided by squared nearest-plane rounding margin."""
    if register_count < 1 or register_count > len(projection.integer_vector):
        raise ValueError("invalid register count")
    register_variance = sum(
        value * value
        for value in projection.integer_vector[:register_count]
    )
    norm = projection.integer_norm_squared
    denominator = projection.common_denominator
    if norm <= 0 or denominator <= 0:
        raise ValueError("projection normalization must be positive")
    return 4.0 * denominator * denominator * register_variance / (norm * norm)


def select_vulnerable_coordinates(
    projections: Sequence[IntegerProjectionRow],
    n_bits: int,
    multiplier: int,
    register_count: int,
) -> list[int]:
    selected_count = vulnerable_coordinate_count(
        n_bits, multiplier, len(projections)
    )
    ranking = sorted(
        range(len(projections)),
        key=lambda index: (
            -coordinate_risk_score(projections[index], register_count),
            index,
        ),
    )
    return sorted(ranking[:selected_count])


def _dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _nearest_integer(value: Fraction) -> int:
    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def exact_selected_nearest_plane_list(
    basis: Matrix,
    target: Sequence[int],
    selected_coordinates: Sequence[int],
    maximum_offset: int = 1,
) -> list[NearestPlaneListCandidate]:
    """Enumerate bounded deviations only on a fixed public coordinate set."""
    rows = [[Fraction(int(value)) for value in row] for row in basis.tolist()]
    if not rows or len(rows[0]) != len(target):
        raise ValueError("basis and target dimensions are incompatible")
    if maximum_offset < 0:
        raise ValueError("maximum_offset must be nonnegative")
    selected = set(int(index) for index in selected_coordinates)
    if any(index < 0 or index >= len(rows) for index in selected):
        raise ValueError("selected coordinate lies outside the basis")
    if len(selected) != len(selected_coordinates):
        raise ValueError("selected coordinates must be unique")

    orthogonal = exact_gram_schmidt_rows(basis)
    target_fraction = [Fraction(int(value)) for value in target]
    candidates: list[NearestPlaneListCandidate] = []

    def recurse(
        index: int,
        residual: list[Fraction],
        coefficients: list[int],
        deviation_count: int,
    ) -> None:
        if index < 0:
            lattice_vector = [
                base - remainder
                for base, remainder in zip(target_fraction, residual)
            ]
            if any(value.denominator != 1 for value in lattice_vector):
                raise ArithmeticError("selected nearest-plane list left the lattice")
            vector = [int(value) for value in lattice_vector]
            candidates.append(
                NearestPlaneListCandidate(
                    lattice_vector=vector,
                    coefficients=list(coefficients),
                    deviation_count=deviation_count,
                    distance_squared=sum(
                        (int(base) - value) ** 2
                        for base, value in zip(target, vector)
                    ),
                )
            )
            return

        star = orthogonal[index]
        coordinate = _dot(residual, star) / _dot(star, star)
        nearest = _nearest_integer(coordinate)
        deltas = (
            range(-maximum_offset, maximum_offset + 1)
            if index in selected
            else (0,)
        )
        for delta in deltas:
            coefficient = nearest + delta
            next_coefficients = list(coefficients)
            next_coefficients[index] = coefficient
            next_residual = [
                value - coefficient * base
                for value, base in zip(residual, rows[index])
            ]
            recurse(
                index - 1,
                next_residual,
                next_coefficients,
                deviation_count + (delta != 0),
            )

    recurse(len(rows) - 1, target_fraction, [0] * len(rows), 0)
    expected = (2 * maximum_offset + 1) ** len(selected)
    if len(candidates) != expected:
        raise AssertionError(f"generated {len(candidates)} paths, expected {expected}")
    candidates.sort(
        key=lambda item: (
            item.distance_squared,
            item.deviation_count,
            tuple(item.coefficients),
        )
    )
    return candidates


def standard_vulnerable_coordinate_decode(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    selector_multiplier: int = 2,
    maximum_offset: int = 1,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
) -> VulnerableCoordinateDecodeOutcome:
    modulus = 1 << n_bits
    full = modular_subset_sum_embedding(
        labels, target, modulus, embedding_scale
    ).tolist()
    kernel = Matrix([row[:-1] for row in full[:-1]])
    target_row = [int(value) for value in full[-1][:-1]]
    reduced = kernel.lll(delta=lll_delta)
    projections = integer_projection_rows(reduced)
    selected = select_vulnerable_coordinates(
        projections, n_bits, selector_multiplier, len(labels)
    )
    candidates = exact_selected_nearest_plane_list(
        reduced, target_row, selected, maximum_offset
    )
    valid = 0
    invalid = 0
    for candidate in candidates:
        vector = [
            value - base
            for value, base in zip(candidate.lattice_vector, target_row)
        ] + [-1]
        witness = decode_short_standard_marker_vector(
            vector, labels, target, modulus
        )
        if witness is None:
            continue
        if sum(
            label * bit for label, bit in zip(labels, witness)
        ) % modulus != target:
            invalid += 1
        else:
            valid += 1
    theoretical = (2 * maximum_offset + 1) ** len(selected)
    return VulnerableCoordinateDecodeOutcome(
        selected_coordinate_count=len(selected),
        candidate_count=len(candidates),
        theoretical_candidate_count=theoretical,
        candidate_count_matches_theorem=len(candidates) == theoretical,
        valid_witness_candidate_count=valid,
        invalid_witness_count=invalid,
        solved=valid > 0,
        reachable_carry_count=1,
    )


def carry_vulnerable_coordinate_decode(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    low_bits: int,
    selector_multiplier: int = 2,
    maximum_offset: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
) -> VulnerableCoordinateDecodeOutcome:
    carries = reachable_carries(labels, target, low_bits)
    selected_count: int | None = None
    candidate_count = 0
    valid = 0
    invalid = 0
    for carry in carries:
        full = carry_sliced_embedding(
            labels,
            target,
            n_bits,
            low_bits,
            carry,
            embedding_scale,
            low_constraint_scale,
        ).tolist()
        kernel = Matrix([row[:-1] for row in full[:-1]])
        target_row = [int(value) for value in full[-1][:-1]]
        reduced = kernel.lll(delta=lll_delta)
        projections = integer_projection_rows(reduced)
        selected = select_vulnerable_coordinates(
            projections, n_bits, selector_multiplier, len(labels)
        )
        if selected_count is None:
            selected_count = len(selected)
        elif selected_count != len(selected):
            raise AssertionError("carry kernels have inconsistent selected rank")
        candidates = exact_selected_nearest_plane_list(
            reduced, target_row, selected, maximum_offset
        )
        candidate_count += len(candidates)
        for candidate in candidates:
            vector = [
                value - base
                for value, base in zip(candidate.lattice_vector, target_row)
            ] + [-1]
            witness = decode_carry_sliced_vector(
                vector,
                labels,
                target,
                n_bits,
                low_bits,
                carry,
            )
            if witness is None:
                continue
            if sum(
                label * bit for label, bit in zip(labels, witness)
            ) % (1 << n_bits) != target:
                invalid += 1
            else:
                valid += 1
    if selected_count is None:
        raise AssertionError("reachable carry set must be nonempty")
    theoretical = (
        len(carries) * (2 * maximum_offset + 1) ** selected_count
    )
    return VulnerableCoordinateDecodeOutcome(
        selected_coordinate_count=selected_count,
        candidate_count=candidate_count,
        theoretical_candidate_count=theoretical,
        candidate_count_matches_theorem=candidate_count == theoretical,
        valid_witness_candidate_count=valid,
        invalid_witness_count=invalid,
        solved=valid > 0,
        reachable_carry_count=len(carries),
    )


def projection_offsets(
    projections: Sequence[IntegerProjectionRow],
    dots: Sequence[int],
) -> list[int]:
    if len(projections) != len(dots):
        raise ValueError("projection and dot counts differ")
    return [
        -_nearest_integer_ratio(
            projection.common_denominator * int(dot),
            projection.integer_norm_squared,
        )
        for projection, dot in zip(projections, dots)
    ]


def selected_path_accepts(
    offsets: Sequence[int],
    selected_coordinates: Sequence[int],
    maximum_offset: int,
) -> bool:
    selected = set(selected_coordinates)
    return all(
        abs(offset) <= maximum_offset and (offset == 0 or index in selected)
        for index, offset in enumerate(offsets)
    )


def fixed_depth_path_accepts(
    offsets: Sequence[int],
    maximum_deviations: int,
    maximum_offset: int,
) -> bool:
    return (
        max((abs(offset) for offset in offsets), default=0) <= maximum_offset
        and sum(offset != 0 for offset in offsets) <= maximum_deviations
    )


def target_coverage_transfer_bounds(
    assignment_coverage: float,
    mean_legal_fiber_multiplicity: float,
) -> tuple[float, float]:
    if not 0.0 <= assignment_coverage <= 1.0:
        raise ValueError("assignment coverage must lie in [0,1]")
    if mean_legal_fiber_multiplicity < 1.0:
        raise ValueError("mean legal fiber multiplicity must be at least one")
    lower = max(
        0.0,
        1.0
        - mean_legal_fiber_multiplicity * (1.0 - assignment_coverage),
    )
    upper = min(
        1.0,
        mean_legal_fiber_multiplicity * assignment_coverage,
    )
    return lower, upper


def _offsets_for_signs(
    projections: Sequence[IntegerProjectionRow],
    signs: Sequence[int],
) -> list[int]:
    register_count = len(signs)
    dots = [
        sum(
            coefficient * sign
            for coefficient, sign in zip(
                projection.integer_vector[:register_count], signs
            )
        )
        for projection in projections
    ]
    return projection_offsets(projections, dots)


def _sample_assignment_coverage(
    projections: Sequence[IntegerProjectionRow],
    selected: Sequence[int],
    register_count: int,
    sample_count: int,
    maximum_offset: int,
    fixed_depth: int,
    rng: random.Random,
) -> tuple[float, float, float]:
    selected_success = 0
    fixed_success = 0
    offset_escape = 0
    for _ in range(sample_count):
        signs = [1 if rng.getrandbits(1) == 0 else -1 for _ in range(register_count)]
        offsets = _offsets_for_signs(projections, signs)
        selected_success += selected_path_accepts(
            offsets, selected, maximum_offset
        )
        fixed_success += fixed_depth_path_accepts(
            offsets, fixed_depth, maximum_offset
        )
        offset_escape += (
            max((abs(offset) for offset in offsets), default=0) > maximum_offset
        )
    return (
        selected_success / sample_count,
        fixed_success / sample_count,
        offset_escape / sample_count,
    )


def _exact_target_census(
    labels: Sequence[int],
    modulus: int,
    standard: Sequence[IntegerProjectionRow],
    carry: Sequence[IntegerProjectionRow],
    standard_selected: Sequence[int],
    carry_selected: Sequence[int],
    maximum_offset: int,
    fixed_depth: int,
) -> dict[str, int | float | bool]:
    register_count = len(labels)
    assignment_count = 1 << register_count
    standard_dots = [
        sum(row.integer_vector[:register_count]) for row in standard
    ]
    carry_dots = [
        sum(row.integer_vector[:register_count]) for row in carry
    ]
    legal = bytearray(modulus)
    standard_covered = bytearray(modulus)
    carry_covered = bytearray(modulus)
    standard_fixed_covered = bytearray(modulus)
    carry_fixed_covered = bytearray(modulus)
    standard_assignment_success = 0
    carry_assignment_success = 0
    target = 0
    gray = 0

    for step in range(assignment_count):
        legal[target] = 1
        standard_offsets = projection_offsets(standard, standard_dots)
        carry_offsets = projection_offsets(carry, carry_dots)
        standard_good = selected_path_accepts(
            standard_offsets, standard_selected, maximum_offset
        )
        carry_good = selected_path_accepts(
            carry_offsets, carry_selected, maximum_offset
        )
        standard_assignment_success += standard_good
        carry_assignment_success += carry_good
        if standard_good:
            standard_covered[target] = 1
        if carry_good:
            carry_covered[target] = 1
        if fixed_depth_path_accepts(
            standard_offsets, fixed_depth, maximum_offset
        ):
            standard_fixed_covered[target] = 1
        if fixed_depth_path_accepts(carry_offsets, fixed_depth, maximum_offset):
            carry_fixed_covered[target] = 1
        if step + 1 == assignment_count:
            continue
        next_gray = (step + 1) ^ ((step + 1) >> 1)
        changed = gray ^ next_gray
        bit = changed.bit_length() - 1
        new_bit = (next_gray >> bit) & 1
        error_delta = -2 if new_bit else 2
        target = (
            target + (labels[bit] if new_bit else -labels[bit])
        ) % modulus
        for index, row in enumerate(standard):
            standard_dots[index] += (
                error_delta * row.integer_vector[bit]
            )
        for index, row in enumerate(carry):
            carry_dots[index] += error_delta * row.integer_vector[bit]
        gray = next_gray

    legal_count = sum(legal)
    mean_multiplicity = assignment_count / legal_count
    standard_assignment_coverage = standard_assignment_success / assignment_count
    carry_assignment_coverage = carry_assignment_success / assignment_count
    standard_target_coverage = sum(standard_covered) / legal_count
    carry_target_coverage = sum(carry_covered) / legal_count
    standard_lower, standard_upper = target_coverage_transfer_bounds(
        standard_assignment_coverage, mean_multiplicity
    )
    carry_lower, carry_upper = target_coverage_transfer_bounds(
        carry_assignment_coverage, mean_multiplicity
    )
    tolerance = 1e-15
    verified = (
        standard_lower - tolerance
        <= standard_target_coverage
        <= standard_upper + tolerance
        and carry_lower - tolerance
        <= carry_target_coverage
        <= carry_upper + tolerance
    )
    return {
        "assignment_count": assignment_count,
        "legal_target_count": legal_count,
        "mean_multiplicity": mean_multiplicity,
        "standard_assignment_coverage": standard_assignment_coverage,
        "carry_assignment_coverage": carry_assignment_coverage,
        "standard_target_coverage": standard_target_coverage,
        "carry_target_coverage": carry_target_coverage,
        "standard_fixed_target_coverage": sum(standard_fixed_covered) / legal_count,
        "carry_fixed_target_coverage": sum(carry_fixed_covered) / legal_count,
        "standard_lower": standard_lower,
        "standard_upper": standard_upper,
        "carry_lower": carry_lower,
        "carry_upper": carry_upper,
        "verified": verified,
    }


def run_vulnerable_coordinate_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    selector_multiplier: int,
    maximum_offset: int,
    assignment_sample_count: int,
    fixed_depth: int,
    exact_full_cube: bool,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    seed: int,
) -> VulnerableCoordinateTrial:
    if assignment_sample_count < 1 or fixed_depth < 0:
        raise ValueError("sample count must be positive and fixed depth nonnegative")
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    standard, carry, independent = _reduced_projection_families(
        n_bits,
        labels,
        constrained_low_bits(n_bits, log_multiplier),
        embedding_scale,
        low_constraint_scale,
        lll_delta,
    )
    if not independent:
        raise AssertionError("marker-zero kernels unexpectedly depend on target")
    standard_selected = select_vulnerable_coordinates(
        standard, n_bits, selector_multiplier, register_count
    )
    carry_selected = select_vulnerable_coordinates(
        carry, n_bits, selector_multiplier, register_count
    )
    standard_sampled, standard_fixed, standard_escape = (
        _sample_assignment_coverage(
            standard,
            standard_selected,
            register_count,
            assignment_sample_count,
            maximum_offset,
            fixed_depth,
            rng,
        )
    )
    carry_sampled, carry_fixed, carry_escape = _sample_assignment_coverage(
        carry,
        carry_selected,
        register_count,
        assignment_sample_count,
        maximum_offset,
        fixed_depth,
        rng,
    )
    exact = (
        _exact_target_census(
            labels,
            modulus,
            standard,
            carry,
            standard_selected,
            carry_selected,
            maximum_offset,
            fixed_depth,
        )
        if exact_full_cube
        else None
    )
    standard_count = (2 * maximum_offset + 1) ** len(standard_selected)
    carry_count = (2 * maximum_offset + 1) ** len(carry_selected)
    carry_factor = register_count + 1
    return VulnerableCoordinateTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        selector_multiplier=selector_multiplier,
        maximum_offset=maximum_offset,
        standard_rank=len(standard),
        carry_rank=len(carry),
        standard_selected_coordinates=standard_selected,
        carry_selected_coordinates=carry_selected,
        standard_selected_risk_scores=[
            coordinate_risk_score(standard[index], register_count)
            for index in standard_selected
        ],
        carry_selected_risk_scores=[
            coordinate_risk_score(carry[index], register_count)
            for index in carry_selected
        ],
        standard_candidate_count=standard_count,
        carry_candidate_count=carry_count,
        carry_factor_upper_bound=carry_factor,
        total_candidate_count_upper_bound=max(
            standard_count, carry_factor * carry_count
        ),
        assignment_sample_count=assignment_sample_count,
        standard_sampled_assignment_coverage=standard_sampled,
        carry_sampled_assignment_coverage=carry_sampled,
        standard_sampled_fixed_depth_coverage=standard_fixed,
        carry_sampled_fixed_depth_coverage=carry_fixed,
        standard_sampled_offset_escape_fraction=standard_escape,
        carry_sampled_offset_escape_fraction=carry_escape,
        exact_full_cube_enumerated=exact is not None,
        exact_assignment_count=(
            int(exact["assignment_count"]) if exact is not None else 0
        ),
        exact_legal_target_count=(
            int(exact["legal_target_count"]) if exact is not None else 0
        ),
        mean_legal_fiber_multiplicity=(
            float(exact["mean_multiplicity"]) if exact is not None else None
        ),
        standard_exact_assignment_coverage=(
            float(exact["standard_assignment_coverage"])
            if exact is not None
            else None
        ),
        carry_exact_assignment_coverage=(
            float(exact["carry_assignment_coverage"])
            if exact is not None
            else None
        ),
        standard_exact_uniform_legal_target_coverage=(
            float(exact["standard_target_coverage"])
            if exact is not None
            else None
        ),
        carry_exact_uniform_legal_target_coverage=(
            float(exact["carry_target_coverage"])
            if exact is not None
            else None
        ),
        standard_exact_fixed_depth_target_coverage=(
            float(exact["standard_fixed_target_coverage"])
            if exact is not None
            else None
        ),
        carry_exact_fixed_depth_target_coverage=(
            float(exact["carry_fixed_target_coverage"])
            if exact is not None
            else None
        ),
        standard_transfer_lower_bound=(
            float(exact["standard_lower"]) if exact is not None else None
        ),
        standard_transfer_upper_bound=(
            float(exact["standard_upper"]) if exact is not None else None
        ),
        carry_transfer_lower_bound=(
            float(exact["carry_lower"]) if exact is not None else None
        ),
        carry_transfer_upper_bound=(
            float(exact["carry_upper"]) if exact is not None else None
        ),
        transfer_sandwich_verified=(
            bool(exact["verified"]) if exact is not None else None
        ),
        source_is_independent_uniform_target_when_exact=True,
    )


def _log2_slope(rows: Sequence[VulnerableCoordinateScalingRow], carry: bool) -> float:
    values = [
        (
            row.n_bits,
            row.mean_carry_sampled_assignment_coverage
            if carry
            else row.mean_standard_sampled_assignment_coverage,
        )
        for row in rows
        if (
            row.mean_carry_sampled_assignment_coverage
            if carry
            else row.mean_standard_sampled_assignment_coverage
        )
        > 0.0
    ]
    if len(values) < 2:
        return 0.0
    mean_n = sum(item[0] for item in values) / len(values)
    logs = [math.log2(item[1]) for item in values]
    mean_log = sum(logs) / len(logs)
    denominator = sum((item[0] - mean_n) ** 2 for item in values)
    if denominator == 0.0:
        return 0.0
    return sum(
        (n_bits - mean_n) * (log_value - mean_log)
        for (n_bits, _), log_value in zip(values, logs)
    ) / denominator


def run_marker_vulnerable_coordinate_decoder(
    n_values: Sequence[int] = (14, 18, 22, 26, 30, 36, 42, 48, 56),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 3,
    selector_multiplier: int = 2,
    maximum_offset: int = 1,
    assignment_sample_count: int = 8192,
    fixed_depth: int = 2,
    exact_target_max_n: int = 18,
    exact_trials_per_row: int = 1,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    seed: int = 0,
) -> DCPMarkerVulnerableCoordinateReport:
    if not n_values or not register_offsets or trials_per_row < 1:
        raise ValueError("nonempty scaling ranges and positive trials are required")
    if exact_trials_per_row < 0 or exact_trials_per_row > trials_per_row:
        raise ValueError("exact trial count must lie between zero and trials per row")
    trials = [
        run_vulnerable_coordinate_trial(
            n_bits=n_bits,
            register_offset=offset,
            trial_index=trial_index,
            selector_multiplier=selector_multiplier,
            maximum_offset=maximum_offset,
            assignment_sample_count=assignment_sample_count,
            fixed_depth=fixed_depth,
            exact_full_cube=(
                n_bits <= exact_target_max_n
                and trial_index < exact_trials_per_row
            ),
            log_multiplier=log_multiplier,
            embedding_scale=embedding_scale,
            low_constraint_scale=low_constraint_scale,
            lll_delta=lll_delta,
            seed=seed + 1_000_003 * ni + 10_007 * oi + trial_index,
        )
        for ni, n_bits in enumerate(n_values)
        for oi, offset in enumerate(register_offsets)
        for trial_index in range(trials_per_row)
    ]
    rows: list[VulnerableCoordinateScalingRow] = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            exact_group = [
                trial for trial in group if trial.exact_full_cube_enumerated
            ]
            rows.append(
                VulnerableCoordinateScalingRow(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_count=len(group),
                    selected_coordinate_count=len(
                        group[0].carry_selected_coordinates
                    ),
                    mean_standard_sampled_assignment_coverage=sum(
                        trial.standard_sampled_assignment_coverage
                        for trial in group
                    )
                    / len(group),
                    mean_carry_sampled_assignment_coverage=sum(
                        trial.carry_sampled_assignment_coverage
                        for trial in group
                    )
                    / len(group),
                    minimum_standard_sampled_assignment_coverage=min(
                        trial.standard_sampled_assignment_coverage
                        for trial in group
                    ),
                    maximum_standard_sampled_assignment_coverage=max(
                        trial.standard_sampled_assignment_coverage
                        for trial in group
                    ),
                    minimum_carry_sampled_assignment_coverage=min(
                        trial.carry_sampled_assignment_coverage
                        for trial in group
                    ),
                    maximum_carry_sampled_assignment_coverage=max(
                        trial.carry_sampled_assignment_coverage
                        for trial in group
                    ),
                    mean_standard_sampled_fixed_depth_coverage=sum(
                        trial.standard_sampled_fixed_depth_coverage
                        for trial in group
                    )
                    / len(group),
                    mean_carry_sampled_fixed_depth_coverage=sum(
                        trial.carry_sampled_fixed_depth_coverage
                        for trial in group
                    )
                    / len(group),
                    mean_standard_offset_escape_fraction=sum(
                        trial.standard_sampled_offset_escape_fraction
                        for trial in group
                    )
                    / len(group),
                    mean_carry_offset_escape_fraction=sum(
                        trial.carry_sampled_offset_escape_fraction
                        for trial in group
                    )
                    / len(group),
                    exact_trial_count=len(exact_group),
                    mean_standard_exact_uniform_legal_target_coverage=(
                        sum(
                            float(
                                trial.standard_exact_uniform_legal_target_coverage
                            )
                            for trial in exact_group
                        )
                        / len(exact_group)
                        if exact_group
                        else None
                    ),
                    mean_carry_exact_uniform_legal_target_coverage=(
                        sum(
                            float(
                                trial.carry_exact_uniform_legal_target_coverage
                            )
                            for trial in exact_group
                        )
                        / len(exact_group)
                        if exact_group
                        else None
                    ),
                    maximum_total_candidate_count_upper_bound=max(
                        trial.total_candidate_count_upper_bound for trial in group
                    ),
                    finite_row_is_asymptotic_source_law=False,
                )
            )
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    standard_slope = _log2_slope(rows, carry=False)
    carry_slope = _log2_slope(rows, carry=True)
    tail_standard = sum(
        row.mean_standard_sampled_assignment_coverage for row in tail
    ) / len(tail)
    tail_carry = sum(
        row.mean_carry_sampled_assignment_coverage for row in tail
    ) / len(tail)
    tail_max_carry = max(
        row.maximum_carry_sampled_assignment_coverage for row in tail
    )
    finite_collapse = int(carry_slope < -0.05 and tail_max_carry < 0.01)
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "maximum_n_bits": tail_n,
        "selector_multiplier": selector_multiplier,
        "maximum_offset": maximum_offset,
        "assignment_sample_count": sum(
            trial.assignment_sample_count for trial in trials
        ),
        "exact_full_cube_trial_count": sum(
            trial.exact_full_cube_enumerated for trial in trials
        ),
        "exact_assignment_count": sum(
            trial.exact_assignment_count for trial in trials
        ),
        "exact_legal_target_count": sum(
            trial.exact_legal_target_count for trial in trials
        ),
        "transfer_sandwich_theorem_count": 1,
        "transfer_sandwich_failure_count": sum(
            trial.transfer_sandwich_verified is False for trial in trials
        ),
        "polynomial_selected_coordinate_list_theorem_count": 1,
        "maximum_total_candidate_count_upper_bound": max(
            trial.total_candidate_count_upper_bound for trial in trials
        ),
        "tail_standard_sampled_assignment_coverage": tail_standard,
        "tail_carry_sampled_assignment_coverage": tail_carry,
        "tail_maximum_carry_sampled_assignment_coverage": tail_max_carry,
        "standard_log2_coverage_slope_per_n": standard_slope,
        "carry_log2_coverage_slope_per_n": carry_slope,
        "finite_tail_collapse_observed_count": finite_collapse,
        "proved_inverse_polynomial_uniform_legal_coverage_count": 0,
        "proved_exponential_assignment_decay_count": 0,
        "polynomial_marker_aware_decoder_count": 0,
    }
    falsifiers = [
        (
            "The preregistered carry-sliced logarithmic-coordinate cell union has "
            f"held-out witness coverage {tail_carry:.6g} at n={tail_n} and log2 slope "
            f"{carry_slope:.6g} per n; this is finite decay, not an asymptotic theorem."
        )
    ] if finite_collapse else []
    return DCPMarkerVulnerableCoordinateReport(
        created_at=utc_now(),
        decoder_contract={
            "input": (
                "independent uniform DCP labels and an independent uniform subset-sum "
                "target conditioned on existence of a Boolean witness"
            ),
            "selector": (
                "rank exact target-independent LLL Gram-Schmidt rows by public "
                "Rademacher variance divided by squared rounding margin"
            ),
            "branching": (
                f"allow offsets in [-{maximum_offset},{maximum_offset}] on "
                f"{selector_multiplier} ceil(log2 n) selected coordinates and zero elsewhere"
            ),
            "list_size": (
                "(2q+1)^(c ceil(log2 n)); carry slicing adds at most n+O(1)"
            ),
            "output": (
                "enumerate selected nearest-plane paths, decode each marker-one vector, "
                "and verify the original modular subset-sum equation"
            ),
            "finite_controls": (
                "larger-n random-witness sweeps plus exact full-Boolean-cube uniform-legal "
                "target censuses on preregistered smaller rows"
            ),
        },
        transfer_theorem={
            "statement": (
                "For every fixed label row, if q is accepted-assignment mass, p is "
                "uniform-legal covered-target mass, and mu is mean legal-fiber "
                "multiplicity, then max(0,1-mu(1-q)) <= p <= min(1,mu q)."
            ),
            "proof": (
                "Each uncovered legal target contains at least one rejected assignment, "
                "and each covered target contains at least one accepted assignment; count "
                "targets against assignments and divide by the legal-target count."
            ),
            "source_models_separated": True,
            "asymptotic_assignment_law_proved": False,
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "public_target_independent_selector": True,
            "candidate_family_polynomial": True,
            "uniform_legal_target_source_audited_exactly_at_finite_n": (
                metrics["exact_full_cube_trial_count"] > 0
            ),
            "assignment_to_target_transfer_proved": True,
            "inverse_polynomial_uniform_legal_coverage_proved": False,
            "finite_decay_is_lower_bound_against_general_affine_cvp": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The decoder class is explicit and polynomial, but neither inverse-polynomial "
                "uniform-legal target coverage nor exponential assignment decay is proved."
            ),
        },
        status=(
            "polynomial-log-coordinate-decoder-finite-tail-collapse-source-law-open"
            if finite_collapse
            else "polynomial-log-coordinate-decoder-finite-signal-source-law-open"
        ),
        summary=(
            f"Tested {len(trials)} public-risk-selected logarithmic-coordinate decoders "
            f"through n={tail_n}; tail witness coverage standard/carry="
            f"{tail_standard:.6g}/{tail_carry:.6g}, carry log2 slope={carry_slope:.6g}. "
            "The list-size and source-transfer theorems are proved; asymptotic coverage is open."
        ),
        falsifiers_triggered=falsifiers,
    )


def _register_vulnerable_coordinate_payload(
    payload: dict[str, object],
    path: Path,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    metrics = payload["headline_metrics"]
    if not isinstance(metrics, dict):
        raise ValueError("vulnerable-coordinate artifact lacks headline metrics")
    if int(metrics["finite_tail_collapse_observed_count"]) > 0:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-MARKER-LOG-COORDINATE-FINITE-TAIL-DECAY",
                source=str(path),
                claim=(
                    "A public risk-ranked O(log n)-coordinate nearest-plane cell union "
                    "already has evidence of inverse-polynomial uniform-legal target coverage."
                ),
                reason_invalid=(
                    "The preregistered assignment-weighted held-out tail decays, and no "
                    "random-label theorem transfers finite target censuses asymptotically."
                ),
                lesson=(
                    "Prove concentration of accepted assignment mass or redesign the "
                    "selector; do not tune coordinate bands on the exact target rows."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=metrics,
            )
        )
    upsert_experiment_result(
        ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}-LATEST",
            experiment_id=registry_experiment_id,
            candidate_id=registry_candidate_id,
            created_at=str(payload["created_at"]),
            status=str(payload["status"]),
            summary=str(payload["summary"]),
            metrics=metrics,
            falsifiers_triggered=list(payload["falsifiers_triggered"]),
            artifacts={"dcp_marker_vulnerable_coordinate_decoder": str(path)},
        )
    )
    return payload


def load_and_register_marker_vulnerable_coordinate_decoder(
    path: Path = DCP_MARKER_VULNERABLE_COORDINATE_PATH,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError("vulnerable-coordinate artifact must be a JSON object")
    return _register_vulnerable_coordinate_payload(
        payload,
        path,
        registry_experiment_id,
        registry_candidate_id,
        registry_result_id,
    )


def write_marker_vulnerable_coordinate_decoder(
    path: Path = DCP_MARKER_VULNERABLE_COORDINATE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict[str, object]:
    payload = asdict(run_marker_vulnerable_coordinate_decoder(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _register_vulnerable_coordinate_payload(
            payload,
            path,
            registry_experiment_id,
            registry_candidate_id,
            registry_result_id,
        )
    return payload


if __name__ == "__main__":
    report = write_marker_vulnerable_coordinate_decoder()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
