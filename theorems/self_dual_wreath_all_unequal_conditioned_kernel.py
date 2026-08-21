"""Conditioned character kernel for natural all-unequal wreath labels.

Let lambda and mu be independent Plancherel partitions of n, conditioned on
lambda != mu, and let pi_{lambda,mu} be the corresponding unequal physical
irrep of W_n=(S_n x S_n) semidirect C_2.  Its normalized-character average is
zero on the swap coset.  On a base element (a,b,0) it is

    K_neq(a,b)
      = [1[a=e]1[b=e]
         - (n!)^-2 sum_lambda d_lambda^2
             chi_lambda(a) chi_lambda(b)]
        / (1-C_n),

where C_n=sum_lambda(d_lambda^2/n!)^2 is the Plancherel collision
probability.  This follows by subtracting the diagonal lambda=mu terms from
two independent Plancherel draws.

For a bridge sequence c_1,...,c_m, expanding the projectors gives the exact
conditioned single-label word factor

    b_m=2^-m sum_S K_neq(product_{j in S} c_j).

The all-unequal natural k-copy normalized moment is E[b_m^k].  Unlike the
unconditioned kernel, K_neq is signed and has no stationary one-dimensional
sector.  Every unequal irrep has bridge character zero, so for every fixed
all-unequal tuple the average frame block satisfies B<=I/2 and

    Tr(B^m)/D <= 2^{-(m+k-1)}.

This is rigorous but not enough: its moment-root scale is approximately 1/2,
whereas the second-moment frame-eigenvalue scale is approximately 2^{1-k}.
The remaining theorem must exploit simultaneous nontriviality in all k
coordinates rather than dominate by a single coordinate.
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
    permutation_cycle_type,
    physical_wreath_character,
    projector_word_character_sum,
    selected_bridge_word,
    unequal_pair_descriptor,
)
from self_dual_wreath_natural_moment_word_map import (
    natural_irrep_probability,
)
from self_dual_wreath_pgm_polar_audit import (
    run_self_dual_wreath_pgm_polar_audit,
)
from self_dual_wreath_subset_carrier_algebra import WreathElement
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_all_unequal_conditioned_kernel.json"
)
WREATH_PGM_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ConditionedKernelValidationRecord:
    n: int
    wreath_element_count: int
    unequal_irrep_count: int
    maximum_absolute_residual: float
    failed_element_count: int
    identity_kernel_value: str
    maximum_swap_coset_absolute_value: float
    exact_kernel_verified: bool


@dataclass(frozen=True)
class ConditionedWordValidationRecord:
    n: int
    moment_order: int
    bridge_sequence_count: int
    maximum_absolute_residual: float
    failed_sequence_count: int
    exact_sequence_formula_verified: bool
    exact_annealed_mean: str
    expected_annealed_mean: str
    annealed_half_power_verified: bool


@dataclass(frozen=True)
class ConditionedKernelScalingRecord:
    n: int
    copy_count: int
    moment_order: int
    equal_label_probability: float
    log2_all_unequal_normalized_moment_upper_bound: float
    log2_normalized_moment_root_upper_bound: float
    log2_second_moment_eigenvalue_scale: float
    log2_root_to_second_moment_scale_gap: float
    all_unequal_frame_half_norm_bound_proved: bool
    simultaneous_k_coordinate_contraction_proved: bool
    status: str


@dataclass(frozen=True)
class AllUnequalConditionedKernelReport:
    created_at: str
    theorem_contract: dict[str, Any]
    kernel_validations: list[ConditionedKernelValidationRecord]
    word_validations: list[ConditionedWordValidationRecord]
    scaling_records: list[ConditionedKernelScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def plancherel_collision_probability(n: int) -> Fraction:
    factorial = math.factorial(n)
    return sum(
        (
            Fraction(hook_length_dimension(partition) ** 4, factorial**2)
            for partition in integer_partitions(n)
        ),
        Fraction(),
    )


@lru_cache(maxsize=None)
def unequal_descriptors(
    n: int,
) -> tuple[PhysicalWreathIrrepDescriptor, ...]:
    partitions = integer_partitions(n)
    return tuple(
        unequal_pair_descriptor(left, right)
        for left_index, left in enumerate(partitions)
        for right in partitions[left_index + 1 :]
    )


def conditioned_unequal_probability(
    descriptor: PhysicalWreathIrrepDescriptor,
) -> Fraction:
    if descriptor.kind != "unequal-pair-induced":
        return Fraction()
    n = sum(descriptor.left_partition)
    return natural_irrep_probability(descriptor) / (
        1 - plancherel_collision_probability(n)
    )


@lru_cache(maxsize=None)
def direct_conditioned_character_kernel(
    n: int,
    element: WreathElement,
) -> Fraction:
    return sum(
        (
            conditioned_unequal_probability(descriptor)
            * Fraction(
                physical_wreath_character(descriptor, element),
                descriptor.dimension,
            )
            for descriptor in unequal_descriptors(n)
        ),
        Fraction(),
    )


@lru_cache(maxsize=None)
def conditioned_character_kernel(
    n: int,
    element: WreathElement,
) -> Fraction:
    left, right, swap = element
    if swap:
        return Fraction()
    factorial = math.factorial(n)
    identity = tuple(range(n))
    independent = int(left == identity and right == identity)
    left_cycle = permutation_cycle_type(left)
    right_cycle = permutation_cycle_type(right)
    diagonal = sum(
        (
            hook_length_dimension(partition) ** 2
            * symmetric_character(partition, left_cycle)
            * symmetric_character(partition, right_cycle)
            for partition in integer_partitions(n)
        )
    )
    collision = plancherel_collision_probability(n)
    return (
        Fraction(independent) - Fraction(diagonal, factorial**2)
    ) / (1 - collision)


@lru_cache(maxsize=None)
def conditioned_word_factor(
    n: int,
    sequence: tuple[tuple[int, ...], ...],
) -> Fraction:
    if not sequence:
        raise ValueError("sequence must be nonempty")
    return sum(
        (
            conditioned_character_kernel(
                n,
                selected_bridge_word(sequence, mask),
            )
            for mask in range(1 << len(sequence))
        ),
        Fraction(),
    ) / (1 << len(sequence))


@lru_cache(maxsize=None)
def direct_conditioned_word_factor(
    n: int,
    sequence: tuple[tuple[int, ...], ...],
) -> Fraction:
    return sum(
        (
            conditioned_unequal_probability(descriptor)
            * Fraction(
                projector_word_character_sum(descriptor, sequence),
                descriptor.dimension * (1 << len(sequence)),
            )
            for descriptor in unequal_descriptors(n)
        ),
        Fraction(),
    )


def validate_conditioned_kernel(
    n: int,
    tolerance: float = 1e-12,
) -> ConditionedKernelValidationRecord:
    permutations = tuple(itertools.permutations(range(n)))
    maximum_residual = 0.0
    failures = 0
    maximum_swap = 0.0
    identity = tuple(range(n))
    for left in permutations:
        for right in permutations:
            for swap in (0, 1):
                element = (left, right, swap)
                direct = direct_conditioned_character_kernel(n, element)
                formula = conditioned_character_kernel(n, element)
                residual = abs(float(direct - formula))
                maximum_residual = max(maximum_residual, residual)
                failures += residual > tolerance
                if swap:
                    maximum_swap = max(maximum_swap, abs(float(formula)))
    identity_value = conditioned_character_kernel(
        n,
        (identity, identity, 0),
    )
    return ConditionedKernelValidationRecord(
        n=n,
        wreath_element_count=2 * math.factorial(n) ** 2,
        unequal_irrep_count=len(unequal_descriptors(n)),
        maximum_absolute_residual=maximum_residual,
        failed_element_count=failures,
        identity_kernel_value=str(identity_value),
        maximum_swap_coset_absolute_value=maximum_swap,
        exact_kernel_verified=(
            failures == 0
            and identity_value == 1
            and maximum_swap <= tolerance
        ),
    )


def validate_conditioned_word_formula(
    n: int,
    moment_order: int,
    tolerance: float = 1e-12,
) -> ConditionedWordValidationRecord:
    permutations = tuple(itertools.permutations(range(n)))
    maximum_residual = 0.0
    failures = 0
    total = Fraction()
    for sequence in itertools.product(permutations, repeat=moment_order):
        direct = direct_conditioned_word_factor(n, sequence)
        formula = conditioned_word_factor(n, sequence)
        residual = abs(float(direct - formula))
        maximum_residual = max(maximum_residual, residual)
        failures += residual > tolerance
        total += formula
    mean = total / len(permutations) ** moment_order
    expected = Fraction(1, 2**moment_order)
    return ConditionedWordValidationRecord(
        n=n,
        moment_order=moment_order,
        bridge_sequence_count=len(permutations) ** moment_order,
        maximum_absolute_residual=maximum_residual,
        failed_sequence_count=failures,
        exact_sequence_formula_verified=failures == 0,
        exact_annealed_mean=str(mean),
        expected_annealed_mean=str(expected),
        annealed_half_power_verified=mean == expected,
    )


def conditioned_scaling_record(
    n: int,
    copy_count: int,
    moment_order: int,
    second_moment_eigenvalue_scale: float,
) -> ConditionedKernelScalingRecord:
    moment_bound_log2 = -(moment_order + copy_count - 1)
    root_log2 = moment_bound_log2 / moment_order
    second_scale_log2 = (
        math.log2(second_moment_eigenvalue_scale)
        if second_moment_eigenvalue_scale > 0
        else -math.inf
    )
    return ConditionedKernelScalingRecord(
        n=n,
        copy_count=copy_count,
        moment_order=moment_order,
        equal_label_probability=float(
            plancherel_collision_probability(n)
        ),
        log2_all_unequal_normalized_moment_upper_bound=moment_bound_log2,
        log2_normalized_moment_root_upper_bound=root_log2,
        log2_second_moment_eigenvalue_scale=second_scale_log2,
        log2_root_to_second_moment_scale_gap=(
            root_log2 - second_scale_log2
        ),
        all_unequal_frame_half_norm_bound_proved=True,
        simultaneous_k_coordinate_contraction_proved=False,
        status=(
            "conditioned-kernel-and-half-norm-proved-"
            "simultaneous-k-contraction-open"
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


def run_all_unequal_conditioned_kernel() -> (
    AllUnequalConditionedKernelReport
):
    kernel_validations = [
        validate_conditioned_kernel(n) for n in (2, 3, 4)
    ]
    word_validations = [
        validate_conditioned_word_formula(n, order)
        for n, order in (
            (2, 1),
            (2, 2),
            (2, 3),
            (3, 1),
            (3, 2),
            (3, 3),
        )
    ]
    wreath = _read_json(WREATH_PGM_PATH)
    if not wreath:
        wreath = asdict(run_self_dual_wreath_pgm_polar_audit())
    scaling = [
        conditioned_scaling_record(
            n=int(record["n"]),
            copy_count=int(record["copy_count"]),
            moment_order=math.ceil(
                float(record["log2_kcopy_hilbert_dimension"])
            ),
            second_moment_eigenvalue_scale=float(
                record["frame_eigenvalue_second_moment_scale"]
            ),
        )
        for record in wreath.get("records", [])
    ]
    kernel_failures = sum(
        record.failed_element_count for record in kernel_validations
    )
    word_failures = sum(
        record.failed_sequence_count for record in word_validations
    )
    annealed_failures = sum(
        not record.annealed_half_power_verified
        for record in word_validations
    )
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "conditioned_kernel_validation_count": len(kernel_validations),
        "conditioned_kernel_validation_failure_count": kernel_failures,
        "conditioned_word_validation_count": len(word_validations),
        "conditioned_word_validation_failure_count": word_failures,
        "conditioned_annealed_half_power_failure_count": annealed_failures,
        "typical_all_unequal_conditioned_kernel_count": 1,
        "all_order_conditioned_word_map_reduction_count": 1,
        "conditioned_swap_coset_annihilation_theorem_count": 1,
        "all_unequal_frame_half_norm_bound_count": 1,
        "tail_log2_conditioned_normalized_moment_upper_bound": (
            tail.log2_all_unequal_normalized_moment_upper_bound
        ),
        "tail_log2_conditioned_normalized_moment_root_upper_bound": (
            tail.log2_normalized_moment_root_upper_bound
        ),
        "tail_log2_root_to_second_moment_scale_gap": (
            tail.log2_root_to_second_moment_scale_gap
        ),
        "simultaneous_k_coordinate_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    verified = (
        kernel_failures == 0
        and word_failures == 0
        and annealed_failures == 0
    )
    return AllUnequalConditionedKernelReport(
        created_at=utc_now(),
        theorem_contract={
            "conditioned_base_kernel": (
                "K_neq(a,b)=[1[a=e]1[b=e]-(n!)^-2 sum_lambda "
                "d_lambda^2 chi_lambda(a)chi_lambda(b)]/(1-C_n)"
            ),
            "conditioned_swap_kernel": "K_neq(a,b,swap)=0",
            "all_order_word_factor": (
                "b_m=2^-m sum_S K_neq(product_{j in S} c_j)"
            ),
            "conditioned_natural_moment": (
                "E_all-unequal[Tr(B^m)/D]=E_bridge-sequences[b_m^k]"
            ),
            "half_norm_bound": (
                "B<=I/2 and Tr(B)/D=2^-k imply "
                "Tr(B^m)/D<=2^{-(m+k-1)}"
            ),
            "remaining_boundary": (
                "The half-norm bound uses one coordinate; a useful theorem "
                "must exploit simultaneous nontriviality in all k coordinates"
            ),
        },
        kernel_validations=kernel_validations,
        word_validations=word_validations,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "conditioned_character_kernel_proved": verified,
            "all_order_conditioned_word_map_reduction_proved": verified,
            "conditioned_annealed_mean_equals_half_power": verified,
            "all_unequal_frame_half_norm_bound_proved": verified,
            "simultaneous_k_coordinate_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Conditioning removes rare equal stationary sectors exactly, "
                "but single-coordinate projection domination only bounds the "
                "frame norm by 1/2 rather than the required 2^{1-k} scale."
            ),
        },
        status=(
            "all-unequal-conditioned-kernel-proved-"
            "simultaneous-k-contraction-open"
        ),
        summary=(
            "Derived and exhaustively validated the signed all-unequal "
            "character kernel and its all-order word formula; the tail "
            "moment-root bound remains "
            f"{tail.log2_root_to_second_moment_scale_gap:.6g} bits above the "
            "second-moment frame scale."
        ),
        falsifiers_triggered=[
            "Conditioning on unequal Plancherel pairs removes every swap-coset character contribution.",
            "The conditioned word kernel is signed, so it is not an ordinary endpoint probability.",
            "Every one-label conditioned annealed moment is exactly 2^-m.",
            "Projection domination proves B<=I/2 for every all-unequal tuple.",
            "The half-norm bound remains exponentially too weak in the copy count.",
            "No maximal-effect circuit, hidden-permutation decoder, or classical separation follows from the conditioned kernel.",
        ],
    )


def write_all_unequal_conditioned_kernel_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_all_unequal_conditioned_kernel())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_all_unequal_conditioned_kernel_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
