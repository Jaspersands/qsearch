"""Exact marginal short-word profile for bridge subset products.

Fix a nonempty even subset of a random bridge sequence.  The selected bridge
word lies in the base subgroup.  Conditioning on all but one selected uniform
permutation shows that each base permutation component is exactly uniform on
S_n.  Hence its transposition length L=n-number_of_cycles has the exact
unsigned-Stirling distribution.

This gives a scalable exact marginal bound for every fixed subset mask.  At
the growing moment order, independently chosen nonempty even masks for the k
source coordinates are also pairwise distinct with overwhelming probability:

    Pr(mask collision) <= binom(k,2)/(2^{m-1}-1).

Neither fact proves the needed joint character-product bound.  Distinct masks
remain correlated because they reuse the same random bridge generators.  The
remaining theorem is non-diagonal joint word-map anti-concentration.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_character_moments import (
    permutation_cycle_type,
    selected_bridge_word,
)
from self_dual_wreath_pgm_polar_audit import (
    run_self_dual_wreath_pgm_polar_audit,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_short_word_profile.json"
)
WREATH_PGM_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SHORT-WORD-PROFILE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FixedMaskUniformityValidationRecord:
    n: int
    moment_order: int
    subset_mask: int
    selected_bridge_count: int
    bridge_sequence_count: int
    distinct_left_output_count: int
    distinct_right_output_count: int
    expected_permutation_count: int
    maximum_left_multiplicity_deviation: int
    maximum_right_multiplicity_deviation: int
    exact_uniform_marginals_verified: bool


@dataclass(frozen=True)
class ShortLengthProbabilityRecord:
    n: int
    maximum_transposition_length: int
    threshold_fraction: float
    exact_short_probability: str
    log2_short_probability: float
    exact_long_probability: str
    uniform_permutation_marginal_theorem_applies: bool
    joint_distinct_mask_theorem_applies: bool
    joint_word_anticoncentration_proved: bool
    status: str


@dataclass(frozen=True)
class MaskCollisionScalingRecord:
    n: int
    copy_count: int
    required_moment_order: int
    log2_nonempty_even_mask_count: float
    log2_pairwise_mask_collision_union_bound: float
    pairwise_mask_distinct_with_overwhelming_probability: bool
    non_diagonal_shared_generator_correlation_proved_small: bool
    status: str


@dataclass(frozen=True)
class ShortWordProfileReport:
    created_at: str
    theorem_contract: dict[str, Any]
    uniformity_validations: list[FixedMaskUniformityValidationRecord]
    short_length_records: list[ShortLengthProbabilityRecord]
    mask_collision_scaling: list[MaskCollisionScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def unsigned_stirling_first_kind_row(n: int) -> tuple[int, ...]:
    """Return counts indexed by cycle count for permutations of n."""

    if n < 0:
        raise ValueError("n must be nonnegative")
    row = [1]
    for size in range(1, n + 1):
        next_row = [0] * (size + 1)
        for cycles, count in enumerate(row):
            next_row[cycles] += (size - 1) * count
            next_row[cycles + 1] += count
        row = next_row
    return tuple(row)


def short_transposition_length_probability(
    n: int,
    maximum_length: int,
) -> Fraction:
    if n < 1:
        raise ValueError("n must be positive")
    if maximum_length < 0:
        return Fraction()
    maximum_length = min(maximum_length, n - 1)
    row = unsigned_stirling_first_kind_row(n)
    minimum_cycles = n - maximum_length
    count = sum(row[minimum_cycles:])
    return Fraction(count, math.factorial(n))


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def validate_fixed_even_mask_uniformity(
    n: int,
    moment_order: int,
    subset_mask: int,
) -> FixedMaskUniformityValidationRecord:
    selected = subset_mask.bit_count()
    if selected == 0 or selected % 2:
        raise ValueError("subset mask must have positive even Hamming weight")
    if subset_mask >= 1 << moment_order:
        raise ValueError("subset mask exceeds moment order")
    permutations = tuple(itertools.permutations(range(n)))
    left_counts: dict[tuple[int, ...], int] = {}
    right_counts: dict[tuple[int, ...], int] = {}
    for sequence in itertools.product(permutations, repeat=moment_order):
        left, right, swap = selected_bridge_word(sequence, subset_mask)
        if swap:
            raise ArithmeticError("even bridge word unexpectedly swapped")
        left_counts[left] = left_counts.get(left, 0) + 1
        right_counts[right] = right_counts.get(right, 0) + 1
    expected_multiplicity = (
        len(permutations) ** moment_order // len(permutations)
    )
    left_deviation = max(
        abs(count - expected_multiplicity)
        for count in left_counts.values()
    )
    right_deviation = max(
        abs(count - expected_multiplicity)
        for count in right_counts.values()
    )
    return FixedMaskUniformityValidationRecord(
        n=n,
        moment_order=moment_order,
        subset_mask=subset_mask,
        selected_bridge_count=selected,
        bridge_sequence_count=len(permutations) ** moment_order,
        distinct_left_output_count=len(left_counts),
        distinct_right_output_count=len(right_counts),
        expected_permutation_count=len(permutations),
        maximum_left_multiplicity_deviation=left_deviation,
        maximum_right_multiplicity_deviation=right_deviation,
        exact_uniform_marginals_verified=(
            len(left_counts) == len(permutations)
            and len(right_counts) == len(permutations)
            and left_deviation == 0
            and right_deviation == 0
        ),
    )


def short_length_record(
    n: int,
    threshold_fraction: float,
) -> ShortLengthProbabilityRecord:
    maximum_length = math.floor(threshold_fraction * n)
    short = short_transposition_length_probability(n, maximum_length)
    return ShortLengthProbabilityRecord(
        n=n,
        maximum_transposition_length=maximum_length,
        threshold_fraction=threshold_fraction,
        exact_short_probability=str(short),
        log2_short_probability=_fraction_log2(short),
        exact_long_probability=str(1 - short),
        uniform_permutation_marginal_theorem_applies=True,
        joint_distinct_mask_theorem_applies=True,
        joint_word_anticoncentration_proved=False,
        status="exact-marginal-short-length-joint-correlation-open",
    )


def mask_collision_scaling_record(
    n: int,
    copy_count: int,
    moment_order: int,
) -> MaskCollisionScalingRecord:
    log2_mask_count = math.log2(2 ** (moment_order - 1) - 1)
    if copy_count < 2:
        collision_log2 = -math.inf
    else:
        collision_log2 = (
            math.log2(math.comb(copy_count, 2)) - log2_mask_count
        )
    return MaskCollisionScalingRecord(
        n=n,
        copy_count=copy_count,
        required_moment_order=moment_order,
        log2_nonempty_even_mask_count=log2_mask_count,
        log2_pairwise_mask_collision_union_bound=collision_log2,
        pairwise_mask_distinct_with_overwhelming_probability=(
            collision_log2 <= -40
        ),
        non_diagonal_shared_generator_correlation_proved_small=False,
        status=(
            "mask-diagonal-negligible-"
            "non-diagonal-word-correlation-open"
        ),
    )


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def run_short_word_profile() -> ShortWordProfileReport:
    validations = [
        validate_fixed_even_mask_uniformity(n, order, mask)
        for n, order, mask in (
            (2, 2, 0b11),
            (2, 3, 0b101),
            (3, 2, 0b11),
            (3, 3, 0b101),
            (3, 4, 0b1111),
        )
    ]
    short_records = [
        short_length_record(n, fraction)
        for n in (8, 16, 32, 64)
        for fraction in (0.25, 0.5, 0.75)
    ]
    wreath = _read_json(WREATH_PGM_PATH)
    if not wreath:
        wreath = asdict(run_self_dual_wreath_pgm_polar_audit())
    scaling = [
        mask_collision_scaling_record(
            n=int(record["n"]),
            copy_count=int(record["copy_count"]),
            moment_order=math.ceil(
                float(record["log2_kcopy_hilbert_dimension"])
            ),
        )
        for record in wreath.get("records", [])
    ]
    failures = sum(
        not record.exact_uniform_marginals_verified
        for record in validations
    )
    tail_short = next(
        record
        for record in short_records
        if record.n == 64 and record.threshold_fraction == 0.5
    )
    tail_scaling = scaling[-1]
    metrics: dict[str, int | float] = {
        "fixed_mask_uniformity_validation_count": len(validations),
        "fixed_mask_uniformity_failure_count": failures,
        "fixed_even_mask_uniform_marginal_theorem_count": 1,
        "unsigned_stirling_short_length_formula_count": 1,
        "short_length_scaling_record_count": len(short_records),
        "tail_half_n_log2_short_probability": (
            tail_short.log2_short_probability
        ),
        "mask_collision_scaling_record_count": len(scaling),
        "pairwise_mask_distinct_scaling_row_count": sum(
            record.pairwise_mask_distinct_with_overwhelming_probability
            for record in scaling
        ),
        "tail_log2_pairwise_mask_collision_union_bound": (
            tail_scaling.log2_pairwise_mask_collision_union_bound
        ),
        "non_diagonal_shared_generator_correlation_theorem_count": 0,
        "joint_short_word_anticoncentration_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
        "collision_free_growing_moment_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
    }
    verified = failures == 0
    return ShortWordProfileReport(
        created_at=utc_now(),
        theorem_contract={
            "fixed_mask_marginal": (
                "Every nonempty even fixed subset bridge word has each base "
                "permutation component exactly uniform on S_n"
            ),
            "short_length_distribution": (
                "Pr(L<=t)=n!^-1 sum_{cycles>=n-t} "
                "unsigned_stirling_first_kind(n,cycles)"
            ),
            "mask_collision_bound": (
                "Pr(any repeated nonempty even mask)<="
                "binom(k,2)/(2^{m-1}-1)"
            ),
            "remaining_boundary": (
                "Distinct masks share bridge generators; prove joint "
                "non-diagonal word-map anti-concentration and character-sign "
                "cancellation"
            ),
        },
        uniformity_validations=validations,
        short_length_records=short_records,
        mask_collision_scaling=scaling,
        headline_metrics=metrics,
        claim_gate={
            "fixed_even_mask_uniform_marginal_proved": verified,
            "exact_short_length_distribution_computed": True,
            "pairwise_mask_collisions_negligible_at_target_order": (
                tail_scaling.pairwise_mask_distinct_with_overwhelming_probability
            ),
            "non_diagonal_shared_generator_correlation_bound_proved": False,
            "joint_short_word_anticoncentration_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "collision_free_growing_moment_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Fixed-mask marginals are uniform and mask diagonals vanish, "
                "but distinct masks remain correlated through shared bridge "
                "generators; no joint character-product tail is proved."
            ),
        },
        status=(
            "short-word-marginals-and-mask-diagonal-closed-"
            "non-diagonal-correlation-open"
        ),
        summary=(
            "Proved exact uniform fixed-mask marginals and negligible mask "
            "collisions; at n=64 the probability that a uniform permutation "
            "has transposition length at most n/2 has log2 "
            f"{tail_short.log2_short_probability:.6g}, while joint distinct-"
            "mask word correlations remain open."
        ),
        falsifiers_triggered=[
            "Every fixed nonempty even subset word has uniform base-component marginals.",
            "Short transposition-length probabilities are exact Stirling tails, not fitted trends.",
            "Repeated subset masks are negligible at the certificate moment order.",
            "Distinct masks can remain correlated through shared bridge generators.",
            "Marginal anti-concentration does not imply a joint character-product moment bound.",
            "No frame-norm theorem, coherent measurement, decoder, or classical separation is claimed.",
        ],
    )


def write_short_word_profile_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_short_word_profile())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-WREATH-MARGINAL-SHORT-WORD-"
                    "NOT-JOINT-TAIL"
                ),
                source=str(path),
                claim=(
                    "Uniform fixed-mask bridge-word marginals prove the joint "
                    "short-word anti-concentration needed by the frame moment."
                ),
                reason_invalid=(
                    "Different subset masks reuse the same bridge generators. "
                    "Mask inequality removes only the diagonal and does not "
                    "bound non-diagonal word correlations or character signs."
                ),
                lesson=(
                    "Classify joint word maps by mask incidence rank or "
                    "overlap hypergraph and prove product mixing on every "
                    "non-diagonal class."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
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
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_short_word_profile": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_short_word_profile_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
