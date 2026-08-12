"""Scaling theorem for hidden-label orbit growth in the wreath carrier algebra.

A word of depth d in subset operators contains d bridge labels
(s_1,...,s_d).  Diagonal left-right wreath conjugation can set s_1=e; the
remaining d-1 relative permutations are then identified by simultaneous
S_n-conjugation.  Burnside's lemma gives the exact orbit count

    a_m(n) = sum_{lambda partition n} z_lambda^(m-1),

for m=d-1 relative permutations, where z_lambda is the centralizer order of a
permutation with cycle type lambda.

For depth two this is p(n).  At depth three it is sum z_lambda >= n!, because
the identity cycle type alone contributes n!.  The wreath swap/inversion can
merge at most pairs of these orbits, leaving at least n!/2 carrier types.
Depth four already has a lower bound (n!)^2/2.

Register-subset intersection profiles remain polynomial in k for each fixed
word depth, so the factorial obstruction comes from hidden-label carrier
orbits, not from subset-mask bookkeeping.  Explicit orbit tables are therefore
cut; any scalable frame transform must use a compressed harmonic or
representation-theoretic block encoding.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_hecke_audit import partition_number


SELF_DUAL_WREATH_CARRIER_ORBIT_GROWTH_PATH = Path(
    "research/representation/self_dual_wreath_carrier_orbit_growth.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WreathCarrierOrbitGrowthSpec:
    exact_n_values: tuple[int, ...] = (
        3,
        4,
        5,
        6,
        8,
        10,
        12,
        16,
        20,
        24,
        28,
        32,
    )
    tail_n_values: tuple[int, ...] = (48, 64)
    word_depth_values: tuple[int, ...] = (2, 3, 4)


@dataclass(frozen=True)
class CarrierOrbitGrowthRecord:
    n: int
    word_depth: int
    relative_permutation_tuple_count: int
    partition_count: int
    exact_simultaneous_conjugacy_orbit_count_decimal: str | None
    full_wreath_orbit_lower_bound_decimal: str
    full_wreath_orbit_upper_bound_decimal: str
    log2_full_wreath_orbit_lower_bound: float
    log2_full_wreath_orbit_upper_bound: float
    factorial_lower_bound: bool
    information_threshold_copy_count: int
    subset_intersection_profile_upper_bound_decimal: str
    log2_subset_intersection_profile_upper_bound: float
    subset_profile_count_polynomial_for_fixed_depth: bool
    explicit_carrier_orbit_table_polynomial: bool
    compressed_harmonic_block_transform_proved: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathCarrierOrbitGrowthReport:
    created_at: str
    spec: WreathCarrierOrbitGrowthSpec
    orbit_reduction: dict[str, Any]
    records: list[CarrierOrbitGrowthRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permutation_centralizer_order(cycle_type: tuple[int, ...]) -> int:
    multiplicities: dict[int, int] = {}
    for length in cycle_type:
        multiplicities[length] = multiplicities.get(length, 0) + 1
    order = 1
    for length, multiplicity in multiplicities.items():
        order *= (length**multiplicity) * math.factorial(multiplicity)
    return order


def simultaneous_conjugacy_orbit_count(
    n: int,
    tuple_count: int,
) -> int:
    """Exact Burnside count for ordered tuple_count-tuples in S_n."""

    if n < 1:
        raise ValueError("n must be positive")
    if tuple_count < 1:
        raise ValueError("tuple_count must be positive")
    return sum(
        permutation_centralizer_order(partition) ** (tuple_count - 1)
        for partition in integer_partitions(n)
    )


def subset_intersection_profile_upper_bound(
    copy_count: int,
    word_depth: int,
) -> int:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    if word_depth < 1:
        raise ValueError("word_depth must be positive")
    membership_patterns = 1 << word_depth
    return math.comb(
        copy_count + membership_patterns - 1,
        membership_patterns - 1,
    )


def _orbit_bounds(
    n: int,
    word_depth: int,
    exact: bool,
) -> tuple[int | None, int, int]:
    relative_count = word_depth - 1
    if relative_count < 1:
        raise ValueError("word_depth must be at least two")
    if exact:
        simultaneous = simultaneous_conjugacy_orbit_count(
            n,
            relative_count,
        )
        return simultaneous, (simultaneous + 1) // 2, simultaneous
    if relative_count == 1:
        simultaneous = partition_number(n)
        return simultaneous, (simultaneous + 1) // 2, simultaneous
    factorial = math.factorial(n)
    identity_contribution = factorial ** (relative_count - 1)
    return None, (identity_contribution + 1) // 2, (
        partition_number(n) * identity_contribution
    )


def audit_carrier_orbit_growth(
    n: int,
    word_depth: int,
    exact: bool = True,
) -> CarrierOrbitGrowthRecord:
    simultaneous, lower, upper = _orbit_bounds(
        n,
        word_depth,
        exact=exact,
    )
    factorial = math.factorial(n)
    copy_count = math.ceil(math.log2(factorial))
    subset_profiles = subset_intersection_profile_upper_bound(
        copy_count,
        word_depth,
    )
    factorial_lower = (
        word_depth >= 3 and lower >= max(1, factorial // 2)
    )
    return CarrierOrbitGrowthRecord(
        n=n,
        word_depth=word_depth,
        relative_permutation_tuple_count=word_depth - 1,
        partition_count=partition_number(n),
        exact_simultaneous_conjugacy_orbit_count_decimal=(
            str(simultaneous) if simultaneous is not None else None
        ),
        full_wreath_orbit_lower_bound_decimal=str(lower),
        full_wreath_orbit_upper_bound_decimal=str(upper),
        log2_full_wreath_orbit_lower_bound=round(math.log2(lower), 12),
        log2_full_wreath_orbit_upper_bound=round(math.log2(upper), 12),
        factorial_lower_bound=factorial_lower,
        information_threshold_copy_count=copy_count,
        subset_intersection_profile_upper_bound_decimal=str(subset_profiles),
        log2_subset_intersection_profile_upper_bound=round(
            math.log2(subset_profiles),
            12,
        ),
        subset_profile_count_polynomial_for_fixed_depth=True,
        explicit_carrier_orbit_table_polynomial=False,
        compressed_harmonic_block_transform_proved=False,
        status=(
            "exact-factorial-hidden-label-orbit-growth"
            if exact and factorial_lower
            else (
                "theorem-tail-factorial-hidden-label-orbit-growth"
                if factorial_lower
                else "depth-two-partition-orbit-control"
            )
        ),
    )


def run_self_dual_wreath_carrier_orbit_growth(
    spec: WreathCarrierOrbitGrowthSpec = WreathCarrierOrbitGrowthSpec(),
) -> SelfDualWreathCarrierOrbitGrowthReport:
    exact_records = [
        audit_carrier_orbit_growth(n, depth, exact=True)
        for n in spec.exact_n_values
        for depth in spec.word_depth_values
    ]
    tail_records = [
        audit_carrier_orbit_growth(n, depth, exact=False)
        for n in spec.tail_n_values
        if n not in spec.exact_n_values
        for depth in spec.word_depth_values
    ]
    records = exact_records + tail_records
    factorial_records = [
        record for record in records if record.factorial_lower_bound
    ]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "exact_record_count": len(exact_records),
        "maximum_n": max((record.n for record in records), default=0),
        "maximum_word_depth": max(
            (record.word_depth for record in records),
            default=0,
        ),
        "depth_two_partition_orbit_record_count": sum(
            record.word_depth == 2 for record in records
        ),
        "factorial_hidden_label_orbit_lower_bound_count": len(
            factorial_records
        ),
        "maximum_log2_full_wreath_orbit_lower_bound": max(
            (
                record.log2_full_wreath_orbit_lower_bound
                for record in records
            ),
            default=0.0,
        ),
        "maximum_log2_subset_profile_upper_bound": max(
            (
                record.log2_subset_intersection_profile_upper_bound
                for record in records
            ),
            default=0.0,
        ),
        "explicit_polynomial_carrier_orbit_table_count": 0,
        "compressed_harmonic_block_transform_count": 0,
        "uniform_noncommutative_carrier_block_transform_count": 0,
        "polynomial_structured_frame_preconditioner_count": 0,
        "polynomial_frame_inverse_count": 0,
        "carrier_sensitive_povm_circuit_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualWreathCarrierOrbitGrowthReport(
        created_at=utc_now(),
        spec=spec,
        orbit_reduction={
            "depth_d_labels": "(s_1,...,s_d) in S_n^d",
            "left_right_action": (
                "(a,b): s_i -> a s_i b^-1 for every i"
            ),
            "relative_tuple": (
                "After setting s_1=e, r_i=s_1^-1 s_i transforms by "
                "simultaneous conjugation r_i -> b r_i b^-1."
            ),
            "burnside_formula": (
                "orbits of m relative permutations = "
                "sum_{lambda partition n} z_lambda^(m-1)"
            ),
            "wreath_swap_effect": (
                "Swap/inversion is an additional involution on simultaneous "
                "conjugacy orbits, so it can reduce their count by at most two."
            ),
            "depth_three_lower_bound": (
                "The identity cycle type contributes z_(1^n)=n!, leaving at "
                "least n!/2 full-wreath carrier orbits."
            ),
            "depth_four_lower_bound": (
                "The identity cycle type contributes (n!)^2, leaving at least "
                "(n!)^2/2 full-wreath carrier orbits."
            ),
            "subset_profile_formula": (
                "d ordered subsets modulo register permutations have at most "
                "C(k+2^d-1,2^d-1) intersection profiles."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "fixed_depth_subset_profile_count_is_polynomial_in_copy_count": True,
            "depth_three_hidden_label_orbits_are_factorial": True,
            "explicit_carrier_orbit_table_is_polynomial": False,
            "finite_word_algebra_can_scale_by_orbit_enumeration": False,
            "compressed_harmonic_block_transform_proved": False,
            "uniform_noncommutative_carrier_block_transform_proved": False,
            "polynomial_structured_frame_preconditioner_proved": False,
            "polynomial_frame_inverse_proved": False,
            "carrier_sensitive_povm_circuit_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Register subset profiles are polynomial at each fixed word "
                "depth, but hidden-label carrier orbits are already factorial "
                "at depth three. Explicit orbit tables cannot scale; a "
                "compressed harmonic block transform is still missing."
            ),
        },
        status="factorial-carrier-orbit-table-cut-harmonic-transform-open",
        summary=(
            f"Audited {len(records)} carrier-orbit scaling rows through n="
            f"{metrics['maximum_n']} and word depth="
            f"{metrics['maximum_word_depth']}; "
            f"{metrics['factorial_hidden_label_orbit_lower_bound_count']} rows "
            "have factorial orbit lower bounds, while compressed harmonic "
            "block transforms remain zero."
        ),
        falsifiers_triggered=[
            "Polynomial subset-mask orbit counts do not control hidden-label carrier orbit counts.",
            "Depth-two relative labels have p(n) cycle-type orbits, but depth three already has at least n!/2.",
            "The wreath swap can merge at most pairs of simultaneous-conjugacy orbits.",
            "Explicit carrier-orbit coefficient tables are factorial before the information-threshold copy count.",
            "A scalable transform must encode these sectors harmonically rather than enumerate them.",
        ],
    )


def write_self_dual_wreath_carrier_orbit_growth(
    path: Path = SELF_DUAL_WREATH_CARRIER_ORBIT_GROWTH_PATH,
    spec: WreathCarrierOrbitGrowthSpec = WreathCarrierOrbitGrowthSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_carrier_orbit_growth(spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_carrier_orbit_growth()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
