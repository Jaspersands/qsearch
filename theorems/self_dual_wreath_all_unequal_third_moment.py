"""Exact class-algebra third moments for arbitrary unequal physical irreps.

For an unequal-pair physical irrep i=(lambda_i,mu_i), the bridge character
vanishes and its third projector-word character is

    d_i + q_i(r) + q_i(q) + q_i(r^-1 q),
    q_i(alpha)=2 chi_lambda_i(alpha) chi_mu_i(alpha).

Therefore every mixed tuple containing only unequal-pair irreps contracts over
the conjugacy classes alpha,beta,gamma of r,q,r^-1 q. The exact pair count is

    N(alpha,beta,gamma)
      = |C_alpha||C_beta||C_gamma|/|S_n|
        sum_nu chi_nu(alpha)chi_nu(beta)chi_nu(gamma)/d_nu.

This replaces permutation-pair enumeration by p(n)^3 class triples and
p(n)^4 character-kernel terms. It is exact and subfactorial, but not
polynomial in n.

Equal-pair physical irreps add epsilon chi_lambda([r,q]). Starting at S_4,
the class of [r,q] is not determined by the three classes above. Thus the
class-triple contraction is provably incomplete for equal-pair or general
mixed sectors; recoupling or richer simultaneous-conjugacy data is required.
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

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_character_moments import (
    PhysicalWreathIrrepDescriptor,
    exact_trace_moment,
    permutation_cycle_type,
    unequal_pair_descriptor,
)
from symmetric_character import (
    conjugacy_class_size,
    symmetric_character,
)


SELF_DUAL_WREATH_ALL_UNEQUAL_THIRD_MOMENT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_all_unequal_third_moment.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class ClassKernelValidationRecord:
    n: int
    partition_count: int
    class_triple_count: int
    nonzero_class_triple_count: int
    direct_pair_count: int
    contracted_pair_count: int
    exact_match: bool


@dataclass(frozen=True)
class UnequalMomentValidationRecord:
    n: int
    copy_count: int
    descriptor_ids: tuple[str, ...]
    direct_character_moment: str
    class_contracted_moment: str
    exact_match: bool


@dataclass(frozen=True)
class UnequalScalingRecord:
    n: int
    copy_count: int
    partition_count: int
    class_triple_count: int
    nonzero_class_triple_count: int
    character_kernel_term_bound: int
    exact_trace_third: str
    explicit_permutation_pair_count: int
    exact_subfactorial_class_contraction: bool
    polynomial_in_n_contraction: bool
    arbitrary_mixed_unequal_tuple_covered: bool
    equal_pair_commutator_terms_covered: bool
    status: str


@dataclass(frozen=True)
class CommutatorClassCounterexample:
    n: int
    left_cycle_type: tuple[int, ...]
    right_cycle_type: tuple[int, ...]
    relative_cycle_type: tuple[int, ...]
    first_commutator_cycle_type: tuple[int, ...]
    second_commutator_cycle_type: tuple[int, ...]
    left_permutation: Permutation
    first_right_permutation: Permutation
    second_right_permutation: Permutation


@dataclass(frozen=True)
class SelfDualWreathAllUnequalThirdMomentReport:
    created_at: str
    class_algebra_contract: dict[str, Any]
    class_kernel_validations: list[ClassKernelValidationRecord]
    moment_validations: list[UnequalMomentValidationRecord]
    scaling_records: list[UnequalScalingRecord]
    commutator_counterexample: CommutatorClassCounterexample
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for index, value in enumerate(permutation):
        result[value] = index
    return tuple(result)


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _commutator(left: Permutation, right: Permutation) -> Permutation:
    return _compose(
        _compose(_compose(_inverse(left), right), left),
        _inverse(right),
    )


@lru_cache(maxsize=None)
def class_triple_pair_count(
    n: int,
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    gamma: tuple[int, ...],
) -> int:
    order = math.factorial(n)
    character_sum = sum(
        Fraction(
            symmetric_character(nu, alpha)
            * symmetric_character(nu, beta)
            * symmetric_character(nu, gamma),
            hook_length_dimension(nu),
        )
        for nu in integer_partitions(n)
    )
    pair_count = (
        Fraction(
            conjugacy_class_size(alpha)
            * conjugacy_class_size(beta)
            * conjugacy_class_size(gamma),
            order,
        )
        * character_sum
    )
    if pair_count.denominator != 1:
        raise ArithmeticError("class connection coefficient is not integral")
    if pair_count < 0:
        raise ArithmeticError("class connection coefficient is negative")
    return pair_count.numerator


@lru_cache(maxsize=None)
def class_triple_kernel(
    n: int,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], int], ...]:
    partitions = integer_partitions(n)
    records = []
    for alpha in partitions:
        for beta in partitions:
            for gamma in partitions:
                count = class_triple_pair_count(
                    n, alpha, beta, gamma
                )
                if count:
                    records.append((alpha, beta, gamma, count))
    if sum(record[3] for record in records) != math.factorial(n) ** 2:
        raise ArithmeticError("class triple kernel has wrong total mass")
    return tuple(records)


def direct_class_triple_kernel(
    n: int,
) -> dict[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]], int]:
    permutations = tuple(itertools.permutations(range(n)))
    result: dict[
        tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
        int,
    ] = {}
    for left in permutations:
        left_inverse = _inverse(left)
        for right in permutations:
            key = (
                permutation_cycle_type(left),
                permutation_cycle_type(right),
                permutation_cycle_type(
                    _compose(left_inverse, right)
                ),
            )
            result[key] = result.get(key, 0) + 1
    return result


def unequal_relative_character(
    descriptor: PhysicalWreathIrrepDescriptor,
    cycle_type: tuple[int, ...],
) -> int:
    if descriptor.kind != "unequal-pair-induced":
        raise ValueError("descriptor must be unequal-pair induced")
    return (
        2
        * symmetric_character(
            descriptor.left_partition, cycle_type
        )
        * symmetric_character(
            descriptor.right_partition, cycle_type
        )
    )


def all_unequal_third_moment(
    descriptors: tuple[PhysicalWreathIrrepDescriptor, ...],
) -> Fraction:
    if not descriptors:
        raise ValueError("at least one descriptor is required")
    if any(
        descriptor.kind != "unequal-pair-induced"
        for descriptor in descriptors
    ):
        raise ValueError("all descriptors must be unequal-pair induced")
    n = sum(descriptors[0].left_partition)
    if any(
        sum(descriptor.left_partition) != n
        for descriptor in descriptors
    ):
        raise ValueError("all descriptors must have the same n")
    numerator = 0
    for alpha, beta, gamma, pair_count in class_triple_kernel(n):
        factors = [
            descriptor.dimension
            + unequal_relative_character(descriptor, alpha)
            + unequal_relative_character(descriptor, beta)
            + unequal_relative_character(descriptor, gamma)
            for descriptor in descriptors
        ]
        numerator += pair_count * math.prod(factors)
    return Fraction(
        numerator,
        math.factorial(n) ** 2 * 8 ** len(descriptors),
    )


def unequal_descriptors(n: int) -> list[PhysicalWreathIrrepDescriptor]:
    partitions = integer_partitions(n)
    return [
        unequal_pair_descriptor(left, right)
        for left_index, left in enumerate(partitions)
        for right in partitions[left_index + 1 :]
    ]


def validate_class_kernels(
    maximum_n: int = 5,
) -> list[ClassKernelValidationRecord]:
    records = []
    for n in range(1, maximum_n + 1):
        direct = direct_class_triple_kernel(n)
        contracted = {
            (alpha, beta, gamma): count
            for alpha, beta, gamma, count in class_triple_kernel(n)
        }
        records.append(
            ClassKernelValidationRecord(
                n=n,
                partition_count=len(integer_partitions(n)),
                class_triple_count=len(integer_partitions(n)) ** 3,
                nonzero_class_triple_count=len(contracted),
                direct_pair_count=sum(direct.values()),
                contracted_pair_count=sum(contracted.values()),
                exact_match=direct == contracted,
            )
        )
    return records


def validate_unequal_moments() -> list[UnequalMomentValidationRecord]:
    records = []
    n = 3
    descriptors = unequal_descriptors(n)
    for indices in itertools.combinations_with_replacement(
        range(len(descriptors)), 3
    ):
        selected = tuple(descriptors[index] for index in indices)
        direct = exact_trace_moment(selected, 3)
        contracted = all_unequal_third_moment(selected)
        records.append(
            UnequalMomentValidationRecord(
                n=n,
                copy_count=len(selected),
                descriptor_ids=tuple(item.id for item in selected),
                direct_character_moment=str(direct),
                class_contracted_moment=str(contracted),
                exact_match=direct == contracted,
            )
        )
    return records


def find_commutator_class_counterexample(
    maximum_n: int = 5,
) -> CommutatorClassCounterexample:
    for n in range(2, maximum_n + 1):
        permutations = tuple(itertools.permutations(range(n)))
        seen: dict[
            tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
            tuple[tuple[int, ...], Permutation, Permutation],
        ] = {}
        for left in permutations:
            left_inverse = _inverse(left)
            for right in permutations:
                key = (
                    permutation_cycle_type(left),
                    permutation_cycle_type(right),
                    permutation_cycle_type(
                        _compose(left_inverse, right)
                    ),
                )
                commutator_type = permutation_cycle_type(
                    _commutator(left, right)
                )
                previous = seen.get(key)
                if previous and previous[0] != commutator_type:
                    return CommutatorClassCounterexample(
                        n=n,
                        left_cycle_type=key[0],
                        right_cycle_type=key[1],
                        relative_cycle_type=key[2],
                        first_commutator_cycle_type=previous[0],
                        second_commutator_cycle_type=commutator_type,
                        left_permutation=left,
                        first_right_permutation=previous[2],
                        second_right_permutation=right,
                    )
                seen[key] = (commutator_type, left, right)
    raise ValueError("no commutator-class counterexample found")


def _scaling_descriptors(
    n: int,
) -> tuple[PhysicalWreathIrrepDescriptor, ...]:
    available = unequal_descriptors(n)
    copy_count = math.ceil(math.log2(math.factorial(n)))
    selected = available[: min(3, len(available))]
    return tuple(
        selected[index % len(selected)]
        for index in range(copy_count)
    )


def scaling_record(n: int) -> UnequalScalingRecord:
    descriptors = _scaling_descriptors(n)
    partitions = integer_partitions(n)
    kernel = class_triple_kernel(n)
    moment = all_unequal_third_moment(descriptors)
    return UnequalScalingRecord(
        n=n,
        copy_count=len(descriptors),
        partition_count=len(partitions),
        class_triple_count=len(partitions) ** 3,
        nonzero_class_triple_count=len(kernel),
        character_kernel_term_bound=len(partitions) ** 4,
        exact_trace_third=str(moment),
        explicit_permutation_pair_count=0,
        exact_subfactorial_class_contraction=True,
        polynomial_in_n_contraction=False,
        arbitrary_mixed_unequal_tuple_covered=True,
        equal_pair_commutator_terms_covered=False,
        status="exact-all-unequal-class-contraction-equal-sector-open",
    )


def run_self_dual_wreath_all_unequal_third_moment() -> (
    SelfDualWreathAllUnequalThirdMomentReport
):
    kernel_validations = validate_class_kernels()
    moment_validations = validate_unequal_moments()
    scaling = [
        scaling_record(n)
        for n in (3, 4, 5, 6, 8)
    ]
    counterexample = find_commutator_class_counterexample()
    failed_kernels = sum(
        not record.exact_match for record in kernel_validations
    )
    failed_moments = sum(
        not record.exact_match for record in moment_validations
    )
    metrics: dict[str, int | float] = {
        "class_kernel_validation_count": len(kernel_validations),
        "failed_class_kernel_validation_count": failed_kernels,
        "unequal_moment_validation_count": len(moment_validations),
        "failed_unequal_moment_validation_count": failed_moments,
        "scaling_record_count": len(scaling),
        "maximum_class_contraction_n": max(
            record.n for record in scaling
        ),
        "maximum_partition_count": max(
            record.partition_count for record in scaling
        ),
        "maximum_class_triple_count": max(
            record.class_triple_count for record in scaling
        ),
        "maximum_character_kernel_term_bound": max(
            record.character_kernel_term_bound for record in scaling
        ),
        "explicit_factorial_pair_enumeration_count": 0,
        "exact_subfactorial_class_contraction_count": 1,
        "polynomial_in_n_all_unequal_contraction_count": 0,
        "arbitrary_mixed_unequal_tuple_contraction_count": 1,
        "equal_pair_commutator_contraction_count": 0,
        "all_physical_irrep_sector_contraction_count": 0,
        "commutator_class_counterexample_count": 1,
        "minimum_commutator_counterexample_n": counterexample.n,
        "support_gap_theorem_count": 0,
        "coherent_blockwise_frame_pseudoinverse_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    validated = not failed_kernels and not failed_moments
    return SelfDualWreathAllUnequalThirdMomentReport(
        created_at=utc_now(),
        class_algebra_contract={
            "unequal_projector_word_character": (
                "d_i+q_i(alpha)+q_i(beta)+q_i(gamma), "
                "q_i=2 chi_lambda_i chi_mu_i"
            ),
            "class_triple_pair_count": (
                "|C_alpha||C_beta||C_gamma|/n! sum_nu "
                "chi_nu(alpha)chi_nu(beta)chi_nu(gamma)/d_nu"
            ),
            "class_contraction_size": (
                "p(n)^3 class triples and at most p(n)^4 "
                "character-kernel terms"
            ),
            "complexity_boundary": (
                "exact and exp(O(sqrt(n))) rather than factorial, "
                "but not polynomial in n"
            ),
            "equal_pair_boundary": (
                "equal extensions add epsilon chi_lambda([r,q]); "
                "the commutator class is not determined by "
                "alpha,beta,gamma from n=4 onward"
            ),
        },
        class_kernel_validations=kernel_validations,
        moment_validations=moment_validations,
        scaling_records=scaling,
        commutator_counterexample=counterexample,
        headline_metrics=metrics,
        claim_gate={
            "exact_class_connection_kernel_verified": validated,
            "arbitrary_mixed_unequal_tuple_third_moment_proved": validated,
            "factorial_permutation_pair_sum_removed": validated,
            "polynomial_in_n_contraction_proved": False,
            "equal_pair_commutator_contraction_proved": False,
            "all_physical_irrep_sectors_covered": False,
            "support_gap_theorem_proved": False,
            "coherent_blockwise_frame_pseudoinverse_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All unequal-only tuples now have an exact subfactorial "
                "class contraction. Equal-pair commutator characters require "
                "strictly richer data, and p(n)^4 is not polynomial."
            ),
        },
        status=(
            "all-unequal-third-moment-class-contraction-proved-"
            "equal-commutator-open"
        ),
        summary=(
            "Proved and validated exact class-algebra third moments for "
            "arbitrary mixed unequal physical irreps, removing factorial pair "
            f"enumeration through n={metrics['maximum_class_contraction_n']}; "
            "an S_4 counterexample proves class triples cannot cover equal "
            "commutator terms."
        ),
        falsifiers_triggered=[
            "Class connection coefficients match direct permutation-pair counts through n=5.",
            "All unequal W_3 threshold tuples match the general wreath-character third moment.",
            "The contraction is subfactorial exp(O(sqrt(n))), not polynomial in n.",
            "An explicit S_4 witness has identical r, q, and r^-1 q classes but different commutator classes.",
            "Equal-pair sectors, support gaps, coherent pseudoinversion, and decoding remain unresolved.",
        ],
    )


def write_self_dual_wreath_all_unequal_third_moment(
    path: Path = SELF_DUAL_WREATH_ALL_UNEQUAL_THIRD_MOMENT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_all_unequal_third_moment())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-SELF-DUAL-WREATH-CLASS-TRIPLES-"
                    "MISS-EQUAL-COMMUTATORS"
                ),
                source=str(path),
                claim=(
                    "The classes of r, q, and r^-1 q suffice for every "
                    "physical-irrep third moment."
                ),
                reason_invalid=(
                    "Equal-pair extensions depend on the commutator class. "
                    "The registered S_4 witness holds all three class labels "
                    "fixed while changing that commutator class."
                ),
                lesson=(
                    "Introduce recoupling or richer simultaneous-conjugacy "
                    "coordinates for equal-pair sectors."
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
                    "self_dual_wreath_all_unequal_third_moment": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_all_unequal_third_moment()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
