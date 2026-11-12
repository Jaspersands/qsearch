"""Polynomial symbolic third-moment contraction for one physical wreath sector.

Let U_n be the unequal-pair physical irrep induced from the trivial and
standard irreps of S_n. For k repeated copies, the third frame moment is

    Tr(B_{U_n^k}^3)
      = 4^-k E_{r,q}[
          n - 4 + fix(r) + fix(q) + fix(r^-1 q)
        ]^k.

The pair distribution is computed without enumerating (n!)^2 pairs. Fixing r,
the q-sum is a permanent of an all-ones matrix with weighted edges on the
identity and r matchings. Its rook polynomial factors over cycles of r.
Summing those factors over all r uses the symmetric-group cycle-index
recurrence

    A_m = sum_{l=1}^m (m-1)!/(m-l)! c_l A_{m-l}.

The resulting bivariate coefficient table has polynomially many states. This
proves an exact polynomial arithmetic contraction for the repeated
trivial-standard unequal sector. It does not cover equal-pair irreps, arbitrary
mixed tuples, support gaps, coherent pseudoinversion, or decoding.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
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
    exact_trace_moment,
    unequal_pair_descriptor,
)


SELF_DUAL_WREATH_THIRD_MOMENT_CONTRACTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_third_moment_contraction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
BivariatePolynomial = dict[tuple[int, int], int]


@dataclass(frozen=True)
class DistributionValidationRecord:
    n: int
    direct_pair_count: int
    recurrence_pair_count: int
    support_size: int
    exact_distribution_match: bool


@dataclass(frozen=True)
class MomentValidationRecord:
    n: int
    copy_count: int
    direct_character_moment: str
    contracted_moment: str
    exact_match: bool


@dataclass(frozen=True)
class ThirdMomentScalingRecord:
    n: int
    copy_count: int
    distribution_support_size: int
    bivariate_state_count: int
    maximum_intermediate_state_count: int
    exact_trace_third: str
    log2_block_dimension: float
    log2_normalized_third_moment: float
    explicit_pair_enumeration_count: int
    arithmetic_recurrence_polynomial_in_n_and_k: bool
    covered_physical_irrep_family_count: int
    all_physical_irrep_sectors_covered: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathThirdMomentContractionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    distribution_validations: list[DistributionValidationRecord]
    moment_validations: list[MomentValidationRecord]
    scaling_records: list[ThirdMomentScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _fixed_points(permutation: Permutation) -> int:
    return sum(index == value for index, value in enumerate(permutation))


def _inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for index, value in enumerate(permutation):
        result[value] = index
    return tuple(result)


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def cycle_rook_polynomial(cycle_length: int) -> BivariatePolynomial:
    """Return c_l(t,z), including the fixed-point z weight for l=1."""
    if cycle_length < 1:
        raise ValueError("cycle_length must be positive")
    if cycle_length == 1:
        return {
            (0, 1): 1,
            (1, 3): 1,
            (1, 1): -1,
        }
    polynomial: BivariatePolynomial = {}
    vertices = 2 * cycle_length
    for matching_size in range(cycle_length + 1):
        if matching_size == 0:
            matching_count = 1
        else:
            matching_count = (
                vertices
                * math.comb(vertices - matching_size - 1, matching_size - 1)
                // matching_size
            )
        for z_degree in range(matching_size + 1):
            coefficient = (
                matching_count
                * math.comb(matching_size, z_degree)
                * (-1) ** (matching_size - z_degree)
            )
            if coefficient:
                key = (matching_size, z_degree)
                polynomial[key] = polynomial.get(key, 0) + coefficient
    return {key: value for key, value in polynomial.items() if value}


def _add_scaled_product(
    target: BivariatePolynomial,
    left: BivariatePolynomial,
    right: BivariatePolynomial,
    scale: int,
) -> None:
    for (left_t, left_z), left_value in left.items():
        for (right_t, right_z), right_value in right.items():
            key = (left_t + right_t, left_z + right_z)
            target[key] = (
                target.get(key, 0)
                + scale * left_value * right_value
            )


def aggregate_rook_polynomial(
    n: int,
) -> tuple[BivariatePolynomial, list[int]]:
    """Compute A_n(t,z)=sum_r z^fix(r) R_r(t,z) by cycle index."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    aggregates: list[BivariatePolynomial] = [{(0, 0): 1}]
    state_counts = [1]
    cycle_polynomials = {
        length: cycle_rook_polynomial(length)
        for length in range(1, n + 1)
    }
    for size in range(1, n + 1):
        current: BivariatePolynomial = {}
        for cycle_length in range(1, size + 1):
            scale = math.factorial(size - 1) // math.factorial(
                size - cycle_length
            )
            _add_scaled_product(
                current,
                cycle_polynomials[cycle_length],
                aggregates[size - cycle_length],
                scale,
            )
        current = {
            key: value for key, value in current.items() if value
        }
        aggregates.append(current)
        state_counts.append(len(current))
    return aggregates[n], state_counts


def agreement_distribution(
    n: int,
) -> tuple[dict[int, int], int, int]:
    """Count pairs (r,q) by fix(r)+fix(q)+fix(r^-1 q)."""
    if n < 1:
        raise ValueError("n must be positive")
    aggregate, state_counts = aggregate_rook_polynomial(n)
    distribution: dict[int, int] = {}
    for (rook_degree, agreement_degree), coefficient in aggregate.items():
        distribution[agreement_degree] = (
            distribution.get(agreement_degree, 0)
            + coefficient * math.factorial(n - rook_degree)
        )
    distribution = {
        degree: count
        for degree, count in sorted(distribution.items())
        if count
    }
    if any(count < 0 for count in distribution.values()):
        raise ArithmeticError("agreement distribution has negative counts")
    expected = math.factorial(n) ** 2
    if sum(distribution.values()) != expected:
        raise ArithmeticError("agreement distribution has wrong total mass")
    return distribution, len(aggregate), max(state_counts)


def direct_agreement_distribution(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("n must be positive")
    permutations = tuple(itertools.permutations(range(n)))
    result: dict[int, int] = {}
    for left in permutations:
        left_inverse = _inverse(left)
        for right in permutations:
            relative = _compose(left_inverse, right)
            agreements = (
                _fixed_points(left)
                + _fixed_points(right)
                + _fixed_points(relative)
            )
            result[agreements] = result.get(agreements, 0) + 1
    return dict(sorted(result.items()))


def repeated_trivial_standard_third_moment(
    n: int,
    copy_count: int,
) -> tuple[Fraction, int, int, int]:
    if n < 2:
        raise ValueError("n must be at least two")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    distribution, states, maximum_states = agreement_distribution(n)
    numerator = sum(
        count * (n - 4 + agreements) ** copy_count
        for agreements, count in distribution.items()
    )
    denominator = (
        math.factorial(n) ** 2
        * 4 ** copy_count
    )
    return (
        Fraction(numerator, denominator),
        len(distribution),
        states,
        maximum_states,
    )


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def validate_distributions(
    maximum_n: int = 5,
) -> list[DistributionValidationRecord]:
    records = []
    for n in range(1, maximum_n + 1):
        direct = direct_agreement_distribution(n)
        recurrence, _, _ = agreement_distribution(n)
        records.append(
            DistributionValidationRecord(
                n=n,
                direct_pair_count=sum(direct.values()),
                recurrence_pair_count=sum(recurrence.values()),
                support_size=len(recurrence),
                exact_distribution_match=direct == recurrence,
            )
        )
    return records


def validate_moments(
    maximum_n: int = 3,
) -> list[MomentValidationRecord]:
    records = []
    for n in range(2, maximum_n + 1):
        descriptor = unequal_pair_descriptor((n,), (n - 1, 1))
        threshold = math.ceil(math.log2(math.factorial(n)))
        for copy_count in range(1, threshold + 1):
            contracted, _, _, _ = (
                repeated_trivial_standard_third_moment(n, copy_count)
            )
            direct = exact_trace_moment(
                (descriptor,) * copy_count,
                3,
            )
            records.append(
                MomentValidationRecord(
                    n=n,
                    copy_count=copy_count,
                    direct_character_moment=str(direct),
                    contracted_moment=str(contracted),
                    exact_match=direct == contracted,
                )
            )
    return records


def scaling_record(n: int) -> ThirdMomentScalingRecord:
    copy_count = math.ceil(math.log2(math.factorial(n)))
    moment, support_size, states, maximum_states = (
        repeated_trivial_standard_third_moment(n, copy_count)
    )
    dimension = (2 * (n - 1)) ** copy_count
    return ThirdMomentScalingRecord(
        n=n,
        copy_count=copy_count,
        distribution_support_size=support_size,
        bivariate_state_count=states,
        maximum_intermediate_state_count=maximum_states,
        exact_trace_third=str(moment),
        log2_block_dimension=round(math.log2(dimension), 12),
        log2_normalized_third_moment=round(
            _fraction_log2(moment) - math.log2(dimension),
            12,
        ),
        explicit_pair_enumeration_count=0,
        arithmetic_recurrence_polynomial_in_n_and_k=True,
        covered_physical_irrep_family_count=1,
        all_physical_irrep_sectors_covered=False,
        status="exact-special-sector-third-moment-contraction",
    )


def run_self_dual_wreath_third_moment_contraction() -> (
    SelfDualWreathThirdMomentContractionReport
):
    distribution_validations = validate_distributions()
    moment_validations = validate_moments()
    scaling = [
        scaling_record(n)
        for n in (3, 4, 5, 6, 8, 10, 12, 16, 20)
    ]
    failed_distributions = sum(
        not record.exact_distribution_match
        for record in distribution_validations
    )
    failed_moments = sum(
        not record.exact_match for record in moment_validations
    )
    metrics: dict[str, int | float] = {
        "distribution_validation_count": len(
            distribution_validations
        ),
        "failed_distribution_validation_count": failed_distributions,
        "moment_validation_count": len(moment_validations),
        "failed_moment_validation_count": failed_moments,
        "scaling_record_count": len(scaling),
        "maximum_scaling_n": max(record.n for record in scaling),
        "maximum_scaling_copy_count": max(
            record.copy_count for record in scaling
        ),
        "maximum_distribution_support_size": max(
            record.distribution_support_size for record in scaling
        ),
        "maximum_bivariate_state_count": max(
            record.bivariate_state_count for record in scaling
        ),
        "explicit_factorial_pair_enumeration_count": 0,
        "exact_polynomial_third_moment_contraction_count": 1,
        "covered_physical_irrep_family_count": 1,
        "all_physical_irrep_sector_contraction_count": 0,
        "support_gap_theorem_count": 0,
        "coherent_support_projector_count": 0,
        "coherent_blockwise_frame_pseudoinverse_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    validated = not failed_distributions and not failed_moments
    return SelfDualWreathThirdMomentContractionReport(
        created_at=utc_now(),
        theorem_contract={
            "covered_sector": (
                "k repeated copies of the unequal physical irrep induced "
                "from S_n trivial and standard irreps"
            ),
            "third_moment": (
                "Tr(B^3)=4^-k E_(r,q)[n-4+fix(r)+fix(q)+"
                "fix(r^-1 q)]^k"
            ),
            "rook_reduction": (
                "sum_q z^[fix(q)+fix(r^-1 q)] is the permanent "
                "of J plus the weighted identity/r matchings"
            ),
            "cycle_index_recurrence": (
                "A_m=sum_(l=1)^m (m-1)!/(m-l)! c_l A_(m-l)"
            ),
            "coefficient_state_bound": (
                "t-degree <= n and z-degree <= 3n, so each A_m "
                "has O(n^2) coefficient states"
            ),
            "arithmetic_complexity": (
                "polynomial in n and k using exact integer coefficient "
                "arithmetic; no permutation-pair enumeration"
            ),
        },
        distribution_validations=distribution_validations,
        moment_validations=moment_validations,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "exact_pair_agreement_distribution_recurrence_proved": validated,
            "exact_polynomial_third_moment_special_sector_proved": validated,
            "all_equal_and_unequal_physical_irreps_covered": False,
            "arbitrary_mixed_tuple_contraction_proved": False,
            "higher_moment_recurrence_proved": False,
            "third_moment_implies_support_gap": False,
            "coherent_support_projector_proved": False,
            "coherent_blockwise_frame_pseudoinverse_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The factorial third-moment sum is removed exactly for one "
                "repeated unequal sector. Equal-pair commutator terms, mixed "
                "tuples, support gaps, and coherent implementation remain open."
            ),
        },
        status=(
            "special-unequal-sector-third-moment-contraction-proved-"
            "general-sector-open"
        ),
        summary=(
            "Proved and validated a polynomial coefficient recurrence for "
            "the repeated trivial-standard unequal-sector third moment through "
            f"n={metrics['maximum_scaling_n']} without permutation-pair "
            "enumeration; all-sector contraction and decoding remain zero."
        ),
        falsifiers_triggered=[
            "The recurrence exactly matches direct pair distributions through n=5.",
            "The contracted third moment exactly matches the general wreath-character formula on finite controls.",
            "The result covers one repeated unequal physical-irrep family, not arbitrary mixed tuples.",
            "Equal-pair triple products introduce commutator characters absent from this sector.",
            "A third moment alone does not certify a support gap or coherent pseudoinverse.",
        ],
    )


def write_self_dual_wreath_third_moment_contraction(
    path: Path = SELF_DUAL_WREATH_THIRD_MOMENT_CONTRACTION_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_third_moment_contraction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-SELF-DUAL-WREATH-SPECIAL-THIRD-MOMENT-"
                    "NOT-ALL-SECTOR"
                ),
                source=str(path),
                claim=(
                    "A polynomial third-moment contraction for the repeated "
                    "trivial-standard unequal sector solves the complete "
                    "physical frame."
                ),
                reason_invalid=(
                    "Equal-pair sectors contain commutator characters and "
                    "general tuples mix irrep families. Neither is represented "
                    "by the pairwise-agreement recurrence."
                ),
                lesson=(
                    "Generalize the contraction through character/class "
                    "algebra while retaining explicit sector coverage."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
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
                    "self_dual_wreath_third_moment_contraction": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_third_moment_contraction()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
