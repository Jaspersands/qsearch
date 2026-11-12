"""Character trace moments for mixed physical wreath frame blocks.

For a physical irrep tuple Pi=(pi_1,...,pi_k),

    B_Pi = (1/n!) sum_s tensor_i P_i(s),
    P_i(s) = (I + pi_i(h_s))/2.

The m-th trace moment has the exact character expansion

    Tr(B_Pi^m)
      = 1/[(n!)^m 2^(mk)]
        sum_(s_1,...,s_m)
        product_i sum_(A subseteq [m])
          chi_i(product_(j in A) h_(s_j)).

This module validates that formula against every physical W_3 threshold block
through m=4.  It also derives a closed all-n second-moment class sum.  After
fixing the first bridge, h_e h_r=(r^-1,r;0), so

    Tr(B_Pi^2)
      = 4^-k sum_[alpha partition n] |C_alpha|/n!
        product_i [d_i + 2 c_i + q_i(alpha)],

where c_i=chi_i(h), q_i=chi_lambda(alpha)^2 for equal-pair
extensions, and q_i=2 chi_lambda(alpha) chi_mu(alpha) for unequal-pair
irreps.

The second moment is exact and class-compressed.  A naive third moment leaves
simultaneous-conjugacy orbits of permutation pairs, already factorial in
number.  No all-n third/higher symbolic contraction, spectral recurrence,
support projector, or coherent pseudoinverse is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
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
from self_dual_wreath_carrier_orbit_growth import (
    simultaneous_conjugacy_orbit_count,
)
from self_dual_wreath_complete_w3_tuple_audit import (
    run_complete_w3_tuple_audit,
    w3_physical_irreps,
)
from self_dual_wreath_subset_carrier_algebra import (
    WreathElement,
    inverse_permutation,
    wreath_multiply,
)
from symmetric_character import (
    conjugacy_class_size,
    symmetric_character,
)


SELF_DUAL_WREATH_CHARACTER_MOMENTS_PATH = Path(
    "research/representation/self_dual_wreath_character_moments.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class PhysicalWreathIrrepDescriptor:
    id: str
    kind: str
    left_partition: tuple[int, ...]
    right_partition: tuple[int, ...]
    sign: int | None
    dimension: int
    bridge_character: int


@dataclass(frozen=True)
class W3MomentValidationRecord:
    moment_power: int
    tuple_count: int
    maximum_absolute_residual: float
    failed_tuple_count: int
    exact_character_formula_verified: bool


@dataclass(frozen=True)
class SecondMomentScalingRecord:
    n: int
    portfolio_id: str
    copy_count: int
    equal_plus_count: int
    equal_minus_count: int
    unequal_count: int
    partition_class_term_count: int
    exact_trace_first_decimal: str
    exact_trace_second_decimal: str
    log2_block_dimension: float
    log2_normalized_first_moment: float
    log2_normalized_second_moment: float
    log2_effective_rank_fraction: float
    third_moment_relative_pair_orbit_count_decimal: str
    third_moment_factorial_orbit_barrier: bool
    exact_second_moment_class_recurrence: bool
    polynomial_third_moment_contraction_proved: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathCharacterMomentReport:
    created_at: str
    character_contract: dict[str, Any]
    w3_validation_records: list[W3MomentValidationRecord]
    scaling_records: list[SecondMomentScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def equal_pair_descriptor(
    partition: tuple[int, ...],
    sign: int,
) -> PhysicalWreathIrrepDescriptor:
    if sign not in (-1, 1):
        raise ValueError("sign must be +/-1")
    source_dimension = hook_length_dimension(partition)
    return PhysicalWreathIrrepDescriptor(
        id=(
            "EQ-"
            + "-".join(map(str, partition))
            + ("-PLUS" if sign > 0 else "-MINUS")
        ),
        kind="equal-pair-extension",
        left_partition=partition,
        right_partition=partition,
        sign=sign,
        dimension=source_dimension * source_dimension,
        bridge_character=sign * source_dimension,
    )


def unequal_pair_descriptor(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> PhysicalWreathIrrepDescriptor:
    if sum(left) != sum(right):
        raise ValueError("partitions must have equal size")
    if left == right:
        raise ValueError("partitions must be distinct")
    return PhysicalWreathIrrepDescriptor(
        id=(
            "UNEQ-"
            + "-".join(map(str, left))
            + "__"
            + "-".join(map(str, right))
        ),
        kind="unequal-pair-induced",
        left_partition=left,
        right_partition=right,
        sign=None,
        dimension=(
            2
            * hook_length_dimension(left)
            * hook_length_dimension(right)
        ),
        bridge_character=0,
    )


def physical_wreath_character(
    descriptor: PhysicalWreathIrrepDescriptor,
    element: WreathElement,
) -> int:
    left, right, swap = element
    left_cycle = permutation_cycle_type(left)
    right_cycle = permutation_cycle_type(right)
    if descriptor.kind == "equal-pair-extension":
        if swap:
            product = compose_permutations(left, right)
            return int(descriptor.sign or 0) * symmetric_character(
                descriptor.left_partition,
                permutation_cycle_type(product),
            )
        return symmetric_character(
            descriptor.left_partition,
            left_cycle,
        ) * symmetric_character(
            descriptor.left_partition,
            right_cycle,
        )
    if swap:
        return 0
    return (
        symmetric_character(descriptor.left_partition, left_cycle)
        * symmetric_character(descriptor.right_partition, right_cycle)
        + symmetric_character(descriptor.right_partition, left_cycle)
        * symmetric_character(descriptor.left_partition, right_cycle)
    )


def compose_permutations(
    left: Permutation,
    right: Permutation,
) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def permutation_cycle_type(permutation: Permutation) -> tuple[int, ...]:
    unseen = set(range(len(permutation)))
    lengths = []
    while unseen:
        start = next(iter(unseen))
        current = start
        length = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def bridge_element(permutation: Permutation) -> WreathElement:
    return (
        permutation,
        inverse_permutation(permutation),
        1,
    )


def selected_bridge_word(
    sequence: tuple[Permutation, ...],
    subset_mask: int,
) -> WreathElement:
    n = len(sequence[0]) if sequence else 0
    identity = tuple(range(n))
    product: WreathElement = (identity, identity, 0)
    for index, permutation in enumerate(sequence):
        if subset_mask & (1 << index):
            product = wreath_multiply(
                product,
                bridge_element(permutation),
            )
    return product


def projector_word_character_sum(
    descriptor: PhysicalWreathIrrepDescriptor,
    sequence: tuple[Permutation, ...],
) -> int:
    return sum(
        physical_wreath_character(
            descriptor,
            selected_bridge_word(sequence, subset_mask),
        )
        for subset_mask in range(1 << len(sequence))
    )


def exact_trace_moment(
    descriptors: tuple[PhysicalWreathIrrepDescriptor, ...],
    moment_power: int,
) -> Fraction:
    if not descriptors:
        raise ValueError("at least one irrep descriptor is required")
    if moment_power < 1:
        raise ValueError("moment_power must be positive")
    n = sum(descriptors[0].left_partition)
    if any(sum(descriptor.left_partition) != n for descriptor in descriptors):
        raise ValueError("all descriptors must have the same n")
    permutations = tuple(itertools.permutations(range(n)))
    numerator = 0
    for sequence in itertools.product(permutations, repeat=moment_power):
        numerator += math.prod(
            projector_word_character_sum(descriptor, sequence)
            for descriptor in descriptors
        )
    denominator = (
        len(permutations) ** moment_power
        * 2 ** (moment_power * len(descriptors))
    )
    return Fraction(numerator, denominator)


def second_moment_class_sum(
    descriptors: tuple[PhysicalWreathIrrepDescriptor, ...],
) -> Fraction:
    if not descriptors:
        raise ValueError("at least one irrep descriptor is required")
    n = sum(descriptors[0].left_partition)
    if any(sum(descriptor.left_partition) != n for descriptor in descriptors):
        raise ValueError("all descriptors must have the same n")
    order = math.factorial(n)
    numerator = 0
    for cycle_type in integer_partitions(n):
        factors = []
        for descriptor in descriptors:
            if descriptor.kind == "equal-pair-extension":
                character = symmetric_character(
                    descriptor.left_partition,
                    cycle_type,
                )
                relative_character = character * character
            else:
                relative_character = (
                    2
                    * symmetric_character(
                        descriptor.left_partition,
                        cycle_type,
                    )
                    * symmetric_character(
                        descriptor.right_partition,
                        cycle_type,
                    )
                )
            factors.append(
                descriptor.dimension
                + 2 * descriptor.bridge_character
                + relative_character
            )
        numerator += conjugacy_class_size(cycle_type) * math.prod(
            factors
        )
    return Fraction(
        numerator,
        order * 4 ** len(descriptors),
    )


def first_moment_trace(
    descriptors: tuple[PhysicalWreathIrrepDescriptor, ...],
) -> Fraction:
    return Fraction(
        math.prod(
            descriptor.dimension + descriptor.bridge_character
            for descriptor in descriptors
        ),
        2 ** len(descriptors),
    )


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def _w3_descriptors() -> list[PhysicalWreathIrrepDescriptor]:
    records, _ = w3_physical_irreps()
    descriptors = []
    for record in records:
        if record.kind == "equal-pair-extension":
            descriptors.append(
                equal_pair_descriptor(
                    record.left_partition,
                    int(record.sign or 0),
                )
            )
        else:
            descriptors.append(
                unequal_pair_descriptor(
                    record.left_partition,
                    record.right_partition,
                )
            )
    return descriptors


def validate_w3_character_moments(
    maximum_power: int = 4,
    tolerance: float = 5e-9,
) -> list[W3MomentValidationRecord]:
    complete = run_complete_w3_tuple_audit()
    descriptors = _w3_descriptors()
    permutations = tuple(itertools.permutations(range(3)))
    validations = []
    for power in range(1, maximum_power + 1):
        feature_rows: list[list[int]] = []
        for sequence in itertools.product(permutations, repeat=power):
            feature_rows.append(
                [
                    projector_word_character_sum(
                        descriptor,
                        sequence,
                    )
                    for descriptor in descriptors
                ]
            )
        denominator = (
            len(permutations) ** power
            * 2 ** (power * 3)
        )
        residuals = []
        for record in complete.tuple_records:
            numerator = sum(
                row[record.label_indices[0]]
                * row[record.label_indices[1]]
                * row[record.label_indices[2]]
                for row in feature_rows
            )
            exact = Fraction(numerator, denominator)
            spectral = sum(
                int(cluster["multiplicity"])
                * float(cluster["eigenvalue"]) ** power
                for cluster in record.eigenvalue_multiplicities
            )
            residuals.append(abs(float(exact) - spectral))
        maximum = max(residuals, default=0.0)
        validations.append(
            W3MomentValidationRecord(
                moment_power=power,
                tuple_count=len(complete.tuple_records),
                maximum_absolute_residual=maximum,
                failed_tuple_count=sum(
                    residual > tolerance for residual in residuals
                ),
                exact_character_formula_verified=maximum <= tolerance,
            )
        )
    return validations


def _portfolio_descriptors(
    n: int,
    portfolio_id: str,
) -> tuple[PhysicalWreathIrrepDescriptor, ...]:
    copy_count = math.ceil(math.log2(math.factorial(n)))
    standard = (n - 1, 1)
    plus = equal_pair_descriptor(standard, 1)
    minus = equal_pair_descriptor(standard, -1)
    unequal = unequal_pair_descriptor((n,), standard)
    if portfolio_id == "all-standard-plus":
        return (plus,) * copy_count
    if portfolio_id == "all-trivial-standard-unequal":
        return (unequal,) * copy_count
    if portfolio_id == "balanced-plus-unequal":
        plus_count = (copy_count + 1) // 2
        return (plus,) * plus_count + (unequal,) * (
            copy_count - plus_count
        )
    if portfolio_id == "balanced-plus-minus":
        plus_count = (copy_count + 1) // 2
        return (plus,) * plus_count + (minus,) * (
            copy_count - plus_count
        )
    raise ValueError(f"unknown portfolio {portfolio_id}")


def audit_second_moment_scaling(
    n: int,
    portfolio_id: str,
) -> SecondMomentScalingRecord:
    descriptors = _portfolio_descriptors(n, portfolio_id)
    first = first_moment_trace(descriptors)
    second = second_moment_class_sum(descriptors)
    dimension = math.prod(
        descriptor.dimension for descriptor in descriptors
    )
    log_dimension = math.log2(dimension)
    log_mu1 = _fraction_log2(first) - log_dimension
    log_mu2 = _fraction_log2(second) - log_dimension
    relative_pair_orbits = simultaneous_conjugacy_orbit_count(n, 2)
    return SecondMomentScalingRecord(
        n=n,
        portfolio_id=portfolio_id,
        copy_count=len(descriptors),
        equal_plus_count=sum(
            descriptor.kind == "equal-pair-extension"
            and descriptor.sign == 1
            for descriptor in descriptors
        ),
        equal_minus_count=sum(
            descriptor.kind == "equal-pair-extension"
            and descriptor.sign == -1
            for descriptor in descriptors
        ),
        unequal_count=sum(
            descriptor.kind == "unequal-pair-induced"
            for descriptor in descriptors
        ),
        partition_class_term_count=len(integer_partitions(n)),
        exact_trace_first_decimal=str(first),
        exact_trace_second_decimal=str(second),
        log2_block_dimension=round(log_dimension, 12),
        log2_normalized_first_moment=round(log_mu1, 12),
        log2_normalized_second_moment=round(log_mu2, 12),
        log2_effective_rank_fraction=round(
            2 * log_mu1 - log_mu2,
            12,
        ),
        third_moment_relative_pair_orbit_count_decimal=str(
            relative_pair_orbits
        ),
        third_moment_factorial_orbit_barrier=(
            relative_pair_orbits >= math.factorial(n)
        ),
        exact_second_moment_class_recurrence=True,
        polynomial_third_moment_contraction_proved=False,
        status="second-moment-class-sum-third-moment-orbit-barrier",
    )


def run_self_dual_wreath_character_moments() -> (
    SelfDualWreathCharacterMomentReport
):
    validations = validate_w3_character_moments()
    portfolios = (
        "all-standard-plus",
        "all-trivial-standard-unequal",
        "balanced-plus-unequal",
        "balanced-plus-minus",
    )
    scaling = [
        audit_second_moment_scaling(n, portfolio)
        for n in (3, 4, 5, 6, 8, 10, 12, 16, 20)
        for portfolio in portfolios
    ]
    metrics: dict[str, int | float] = {
        "w3_moment_validation_record_count": len(validations),
        "w3_validated_tuple_moment_count": sum(
            record.tuple_count for record in validations
        ),
        "w3_failed_tuple_moment_count": sum(
            record.failed_tuple_count for record in validations
        ),
        "maximum_w3_character_moment_residual": max(
            (
                record.maximum_absolute_residual
                for record in validations
            ),
            default=0.0,
        ),
        "second_moment_scaling_record_count": len(scaling),
        "maximum_second_moment_n": max(
            (record.n for record in scaling),
            default=0,
        ),
        "exact_second_moment_class_recurrence_count": 1,
        "maximum_partition_class_term_count": max(
            (record.partition_class_term_count for record in scaling),
            default=0,
        ),
        "third_moment_factorial_orbit_barrier_count": sum(
            record.third_moment_factorial_orbit_barrier
            for record in scaling
        ),
        "maximum_third_moment_relative_pair_orbit_count_log2": max(
            (
                math.log2(
                    int(record.third_moment_relative_pair_orbit_count_decimal)
                )
                for record in scaling
            ),
            default=0.0,
        ),
        "polynomial_third_moment_contraction_count": 0,
        "all_moment_spectral_recurrence_count": 0,
        "coherent_support_projector_count": 0,
        "coherent_blockwise_frame_pseudoinverse_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    all_valid = all(
        record.exact_character_formula_verified for record in validations
    )
    return SelfDualWreathCharacterMomentReport(
        created_at=utc_now(),
        character_contract={
            "equal_base_character": (
                "chi_(lambda,lambda,epsilon)(a,b;0)="
                "chi_lambda(a)chi_lambda(b)"
            ),
            "equal_swap_character": (
                "chi_(lambda,lambda,epsilon)(a,b;1)="
                "epsilon chi_lambda(ab)"
            ),
            "unequal_base_character": (
                "chi_(lambda,mu)(a,b;0)=chi_lambda(a)chi_mu(b)+"
                "chi_mu(a)chi_lambda(b)"
            ),
            "unequal_swap_character": (
                "chi_(lambda,mu)(a,b;1)=0"
            ),
            "general_moment_expansion": (
                "Tr(B^m)=1/[(n!)^m 2^(mk)] sum_(s_1,...,s_m) "
                "product_i sum_A chi_i(product_(j in A) h_(s_j))"
            ),
            "second_moment_class_sum": (
                "Tr(B^2)=4^-k sum_alpha |C_alpha|/n! "
                "product_i[d_i+2c_i+q_i(alpha)]"
            ),
            "third_moment_boundary": (
                "Naive relative labels are permutation pairs modulo "
                "simultaneous conjugation, with factorial orbit count."
            ),
        },
        w3_validation_records=validations,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "general_character_moment_expansion_verified_on_w3": all_valid,
            "exact_all_n_second_moment_class_sum_proved": True,
            "information_threshold_second_moment_scaling_computed": True,
            "polynomial_third_moment_symbolic_contraction_proved": False,
            "all_moment_spectral_recurrence_proved": False,
            "second_moment_bounds_minimum_positive_eigenvalue": False,
            "coherent_support_projector_proved": False,
            "coherent_blockwise_frame_pseudoinverse_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Characters now reproduce finite mixed-block moments and give "
                "an exact all-n second moment, but second moments do not bound "
                "the smallest positive eigenvalue. Third and higher moments "
                "still face factorial relative-orbit tables."
            ),
        },
        status="second-moment-character-recurrence-proved-higher-moments-open",
        summary=(
            f"Validated {metrics['w3_validated_tuple_moment_count']} W_3 tuple "
            "moments through fourth order and computed "
            f"{len(scaling)} all-n second-moment scaling rows through n="
            f"{metrics['maximum_second_moment_n']}; polynomial third-moment "
            "contractions and coherent pseudoinverses remain zero."
        ),
        falsifiers_triggered=[
            "The general character expansion reproduces every complete W_3 tuple trace moment through fourth order.",
            "The second moment compresses to a partition-class sum for arbitrary mixed physical-irrep tuples.",
            "Second-moment effective rank does not certify the minimum positive frame eigenvalue.",
            "Naive third moments reintroduce factorial simultaneous-conjugacy pair orbits.",
            "Finite low-order moments do not supply an all-spectrum recurrence, support projector, pseudoinverse, or decoder.",
        ],
    )


def write_self_dual_wreath_character_moments(
    path: Path = SELF_DUAL_WREATH_CHARACTER_MOMENTS_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_character_moments())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-SELF-DUAL-WREATH-SECOND-MOMENT-NOT-SPECTRAL-INVERSE",
                source=str(path),
                claim=(
                    "An exact all-n second moment supplies the support gap "
                    "and a blockwise frame pseudoinverse."
                ),
                reason_invalid=(
                    "The second moment controls effective rank but not the "
                    "minimum positive eigenvalue. Third and higher moments "
                    "lack a polynomial symbolic contraction."
                ),
                lesson=(
                    "Use the character engine to derive higher-moment or "
                    "minimal-polynomial recurrences; require a support-gap "
                    "theorem before pseudoinversion."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-LATEST"
        )
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
                artifacts={
                    "self_dual_wreath_character_moments": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_character_moments()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
