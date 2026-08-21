"""Exact Foulkes-support mass probe for imprimitive subgroup outliers.

For ``L=S_b wr S_a <= S_(ab)``, the conjugate span of right-``L`` invariants
is the isotypic support of the Foulkes module

    Ind_L^G(1),  ch(Ind_L^G(1)) = h_a[h_b].             (1)

This module compiles (1) exactly in the power-sum basis.  Using

    h_a = sum_(alpha partition a) p_alpha/z_alpha,
    p_r[h_b] = sum_(beta partition b) p_(r beta)/z_beta,

it obtains integer cycle counts for the wreath subgroup and then computes

    m_lambda = |L|^-1 sum_(g in L) chi_lambda(g).        (2)

No factorial-size group enumeration is used.

Let ``E_(a,b)`` be the union of nontrivial isotypic sectors with
``m_lambda>0``.  For a fixed-point-free involution ``h`` and the common-trimmed
candidate projector ``Pbar_h``, the exact one-register support probability is

    w_(a,b) = Tr(E_(a,b) Pbar_h)/(n!/2-c),              (3)

where each isotypic contribution is
``d_lambda(d_lambda+chi_lambda(h))/2``.  Because the candidate state is a
tensor power and ``E_(a,b)`` is central, the exact alternative mass of the
all-register event carrying every pure ``L``-invariant tensor witness is

    w_(a,b)^k.                                          (4)

The decisive asymptotic quantity is therefore ``k(1-w_(a,b))``: divergence
forces (4) to zero, while a bounded value leaves this deflation route
inconclusive.  Exact controls through ``h_10[h_3]`` show rapidly increasing
one-register support mass but still small all-register mass.  They are data,
not an asymptotic theorem.

General plethysm positivity is NP-hard and coefficient computation is #P-hard,
including fixed-inner-parameter regimes (Fischer--Ikenmeyer, 2020).  That does
not prove hardness of this one-row Foulkes slice or of coherent quantum
support access.  A useful next theorem must establish the asymptotic support
deficit or compile a support projector without a classical positivity table.
No speedup or residual frame-norm bound is claimed.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_common_outlier_deflation import (
    expected_normal_closure_index,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_foulkes_support_mass_probe.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-FOULKES-SUPPORT-MASS-PROBE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FoulkesSupportMassRecord:
    block_count: int
    block_size: int
    degree: int
    group_order_decimal: str
    wreath_order_decimal: str
    subgroup_index_decimal: str
    power_sum_cycle_type_count: int
    partition_count: int
    support_sector_count: int
    missing_sector_count: int
    maximum_support_partition_row_count: int
    induced_dimension_sum_decimal: str
    induced_dimension_identity_verified: bool
    hook_constituent_violation_count: int
    support_isotypic_dimension_decimal: str
    support_plancherel_mass: float
    exact_trimmed_candidate_support_probability: float
    support_deficit: float
    copy_count: int
    support_deficit_times_copy_count: float
    exact_all_register_support_mass_log2: float
    exact_all_register_support_mass: float
    all_register_support_mass_below_one_in_a_million: bool
    asymptotic_support_deficit_classified: bool
    coherent_support_projector_compiled: bool
    status: str


@dataclass(frozen=True)
class FoulkesSupportMassTheorem:
    power_sum_compiler: str
    multiplicity_formula: str
    support_probability: str
    tensor_mass_identity: str
    asymptotic_criterion: str
    finite_evidence: str
    complexity_boundary: str
    exact_power_sum_compiler_verified: bool
    exact_finite_support_mass_verified: bool
    asymptotic_support_deficit_classified: bool
    coherent_foulkes_support_projector_compiled: bool
    post_support_deflation_frame_norm_bounded: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FoulkesSupportMassReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    records: list[FoulkesSupportMassRecord]
    theorem: FoulkesSupportMassTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def partition_centralizer_order(partition: tuple[int, ...]) -> int:
    multiplicities: dict[int, int] = {}
    for part in partition:
        multiplicities[part] = multiplicities.get(part, 0) + 1
    output = 1
    for part, count in multiplicities.items():
        output *= part**count * math.factorial(count)
    return output


def _multiply_power_sums(
    left: dict[tuple[int, ...], Fraction],
    right: dict[tuple[int, ...], Fraction],
) -> dict[tuple[int, ...], Fraction]:
    output: defaultdict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for left_partition, left_coefficient in left.items():
        for right_partition, right_coefficient in right.items():
            partition = tuple(
                sorted(left_partition + right_partition, reverse=True)
            )
            output[partition] += left_coefficient * right_coefficient
    return dict(output)


def foulkes_power_sum_coefficients(
    block_count: int,
    block_size: int,
) -> dict[tuple[int, ...], Fraction]:
    """Return the exact power-sum coefficients of ``h_a[h_b]``."""

    if block_count < 1 or block_size < 2:
        raise ValueError("positive block_count and block_size>=2 are required")
    inner = {
        partition: Fraction(1, partition_centralizer_order(partition))
        for partition in integer_partitions(block_size)
    }
    output: defaultdict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for outer_partition in integer_partitions(block_count):
        term = {
            (): Fraction(1, partition_centralizer_order(outer_partition))
        }
        for scale in outer_partition:
            scaled_inner = {
                tuple(scale * part for part in partition): coefficient
                for partition, coefficient in inner.items()
            }
            term = _multiply_power_sums(term, scaled_inner)
        for cycle_type, coefficient in term.items():
            output[cycle_type] += coefficient
    return dict(output)


def foulkes_cycle_counts(
    block_count: int,
    block_size: int,
) -> dict[tuple[int, ...], int]:
    """Convert Frobenius coefficients into exact wreath cycle counts."""

    coefficients = foulkes_power_sum_coefficients(block_count, block_size)
    wreath_order = math.factorial(block_size) ** block_count * math.factorial(
        block_count
    )
    output = {}
    for cycle_type, coefficient in coefficients.items():
        count = coefficient * wreath_order
        if count.denominator != 1 or count < 0:
            raise ArithmeticError("power-sum coefficient is not a cycle count")
        output[cycle_type] = count.numerator
    if sum(output.values()) != wreath_order:
        raise ArithmeticError("wreath cycle counts do not sum to the group order")
    return output


def foulkes_multiplicities(
    block_count: int,
    block_size: int,
) -> dict[tuple[int, ...], int]:
    degree = block_count * block_size
    cycle_counts = foulkes_cycle_counts(block_count, block_size)
    wreath_order = sum(cycle_counts.values())
    output = {}
    for partition in integer_partitions(degree):
        numerator = sum(
            count * symmetric_character(partition, cycle_type)
            for cycle_type, count in cycle_counts.items()
        )
        if numerator % wreath_order:
            raise ArithmeticError("Foulkes multiplicity is not integral")
        multiplicity = numerator // wreath_order
        if multiplicity < 0:
            raise ArithmeticError("Foulkes multiplicity is negative")
        output[partition] = multiplicity
    return output


def foulkes_support_mass_record(
    block_count: int,
    block_size: int,
) -> FoulkesSupportMassRecord:
    degree = block_count * block_size
    if degree < 6 or degree % 2:
        raise ValueError("an even degree at least six is required")
    order = math.factorial(degree)
    wreath_order = math.factorial(block_size) ** block_count * math.factorial(
        block_count
    )
    index = order // wreath_order
    cycle_counts = foulkes_cycle_counts(block_count, block_size)
    multiplicities = foulkes_multiplicities(block_count, block_size)
    support = [
        partition for partition, multiplicity in multiplicities.items()
        if multiplicity > 0
    ]
    dimensions = {
        partition: hook_length_dimension(partition) for partition in multiplicities
    }
    induced_dimension = sum(
        dimensions[partition] * multiplicity
        for partition, multiplicity in multiplicities.items()
    )
    support_dimension = sum(dimensions[partition] ** 2 for partition in support)
    hidden_cycle = (2,) * (degree // 2)
    common_dimension = expected_normal_closure_index(degree, degree // 2)
    trimmed_rank = order // 2 - common_dimension
    support_plus_trace = sum(
        dimensions[partition]
        * (
            dimensions[partition]
            + symmetric_character(partition, hidden_cycle)
        )
        // 2
        for partition in support
    )
    # Trivial is the only global-common vector in the Foulkes support.  Sign is
    # absent because the wreath subgroup contains odd internal permutations.
    retained_support_trace = support_plus_trace - 1
    support_probability = retained_support_trace / trimmed_rank
    candidates = involution_class_size(degree, degree // 2)
    copies = flatness_copy_count(candidates)
    all_log2 = copies * math.log2(support_probability)
    all_mass = 2.0**all_log2 if all_log2 > -1074 else 0.0
    hook_violations = sum(
        multiplicities.get((degree - leg, *((1,) * leg)), 0) > 0
        for leg in range(1, degree)
    )
    return FoulkesSupportMassRecord(
        block_count=block_count,
        block_size=block_size,
        degree=degree,
        group_order_decimal=str(order),
        wreath_order_decimal=str(wreath_order),
        subgroup_index_decimal=str(index),
        power_sum_cycle_type_count=len(cycle_counts),
        partition_count=len(multiplicities),
        support_sector_count=len(support),
        missing_sector_count=len(multiplicities) - len(support),
        maximum_support_partition_row_count=max(len(partition) for partition in support),
        induced_dimension_sum_decimal=str(induced_dimension),
        induced_dimension_identity_verified=(induced_dimension == index),
        hook_constituent_violation_count=hook_violations,
        support_isotypic_dimension_decimal=str(support_dimension),
        support_plancherel_mass=support_dimension / order,
        exact_trimmed_candidate_support_probability=support_probability,
        support_deficit=1.0 - support_probability,
        copy_count=copies,
        support_deficit_times_copy_count=copies * (1.0 - support_probability),
        exact_all_register_support_mass_log2=all_log2,
        exact_all_register_support_mass=all_mass,
        all_register_support_mass_below_one_in_a_million=(all_log2 < -20.0),
        asymptotic_support_deficit_classified=False,
        coherent_support_projector_compiled=False,
        status=(
            "exact-foulkes-support-mass-small-at-finite-width-asymptotics-open"
            if all_log2 < -20.0
            else "finite-foulkes-support-mass-not-negligible"
        ),
    )


def build_foulkes_support_mass_report(
    *,
    specs: tuple[tuple[int, int], ...] = (
        (2, 3),
        (4, 3),
        (6, 3),
        (8, 3),
        (10, 3),
        (3, 4),
        (4, 4),
        (5, 4),
    ),
) -> FoulkesSupportMassReport:
    records = [foulkes_support_mass_record(a, b) for a, b in specs]
    finite_verified = all(
        row.induced_dimension_identity_verified
        and row.hook_constituent_violation_count == 0
        and 0.0 < row.exact_trimmed_candidate_support_probability < 1.0
        and not row.asymptotic_support_deficit_classified
        and not row.coherent_support_projector_compiled
        for row in records
    )
    theorem = FoulkesSupportMassTheorem(
        power_sum_compiler=(
            "Expand h_a[h_b] via h_a=sum p_alpha/z_alpha and "
            "p_r[h_b]=sum p_(r beta)/z_beta."
        ),
        multiplicity_formula=(
            "m_lambda=|S_b wr S_a|^-1 sum_g chi_lambda(g), evaluated from "
            "exact integer cycle counts."
        ),
        support_probability=(
            "w=Tr(E Pbar_h)/(n!/2-c), with exact isotypic plus-ranks "
            "d_lambda(d_lambda+chi_lambda(h))/2."
        ),
        tensor_mass_identity=(
            "The all-register Foulkes-support alternative mass is exactly w^k."
        ),
        asymptotic_criterion=(
            "k(1-w)->infinity suffices for vanishing support mass; bounded "
            "k(1-w) leaves deflation inconclusive."
        ),
        finite_evidence=(
            "For h_a[h_3], one-register mass rises through 0.1060, 0.1934, "
            "0.3810, and 0.6136 at a=4,6,8,10, while w^k remains below 2^-41."
        ),
        complexity_boundary=(
            "General fixed-inner plethysm hardness does not prove hardness for "
            "this one-row Foulkes support or coherent quantum access."
        ),
        exact_power_sum_compiler_verified=finite_verified,
        exact_finite_support_mass_verified=finite_verified,
        asymptotic_support_deficit_classified=False,
        coherent_foulkes_support_projector_compiled=False,
        post_support_deflation_frame_norm_bounded=False,
        theorem_verified=finite_verified,
        status=(
            "exact-foulkes-support-mass-probe-asymptotic-deficit-open"
            if finite_verified
            else "foulkes-support-mass-control-failure"
        ),
    )
    return FoulkesSupportMassReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "ARXIV-2002.00788",
                "url": "https://arxiv.org/abs/2002.00788",
                "use": (
                    "General plethysm positivity is NP-hard and coefficient "
                    "computation #P-hard, including fixed-inner regimes; not a "
                    "hardness theorem for this Foulkes slice."
                ),
            },
            {
                "id": "ARXIV-1207.6300",
                "url": "https://arxiv.org/abs/1207.6300",
                "use": (
                    "Foulkes-module vanishing criteria, including absence of "
                    "nontrivial hook constituents."
                ),
            },
        ],
        theorem_contract={
            "family": "Foulkes modules h_a[h_b] for imprimitive S_b wr S_a.",
            "measure": (
                "Exact Plancherel and common-trimmed hidden-involution candidate "
                "mass of the nonzero Foulkes isotypic support."
            ),
            "falsifier": (
                "If k(1-w_(a,b)) fails to diverge, all-support deflation is not "
                "information-theoretically negligible."
            ),
            "outside_scope": (
                "Asymptotic support deficit, coherent support projection, higher "
                "strata, residual norm, and decoding."
            ),
        },
        records=records,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-FOULKES-SUPPORT-DEFICIT",
                "statement": (
                    "Prove the asymptotic order of 1-w_(a,b), especially fixed "
                    "b>=3 with a growing."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-FOULKES-SUPPORT-PROJECTOR",
                "statement": (
                    "Compile a coherent projector onto nonzero h_a[h_b] support "
                    "without assuming a classical plethysm positivity table."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-POST-FOULKES-TRIM-NORM",
                "statement": (
                    "Bound or witness the frame norm after every negligible "
                    "Foulkes-support event is removed."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Finite support masses below one imply asymptotic deflation.",
                "answer": (
                    "False. The observed mass rises to 0.6136 by n=30; only the "
                    "asymptotic behavior of k(1-w) decides."
                ),
                "resolved": True,
            },
            {
                "challenge": "Classical plethysm hardness proves no efficient quantum trim.",
                "answer": (
                    "False. It motivates the obligation but is neither a quantum "
                    "circuit lower bound nor specific to this exact slice."
                ),
                "resolved": True,
            },
            {
                "challenge": "A small all-support event bounds the full residual frame.",
                "answer": (
                    "False. It only controls exact tensors contained in one "
                    "subgroup-induced support; other and approximate outliers remain."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_support_mass_record_count": len(records),
            "finite_identity_failure_count": sum(
                not row.induced_dimension_identity_verified for row in records
            ),
            "maximum_one_register_support_probability": max(
                row.exact_trimmed_candidate_support_probability for row in records
            ),
            "minimum_support_deficit_times_copy_count": min(
                row.support_deficit_times_copy_count for row in records
            ),
            "non_negligible_all_register_record_count": sum(
                not row.all_register_support_mass_below_one_in_a_million
                for row in records
            ),
            "asymptotic_support_deficit_theorem_count": 0,
            "coherent_support_projector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_foulkes_support_mass_compiler_verified": finite_verified,
            "finite_all_support_mass_measured": finite_verified,
            "asymptotic_support_deficit_classified": False,
            "coherent_foulkes_support_projector_compiled": False,
            "post_foulkes_trim_frame_norm_bounded": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact finite support masses are known, but their rising trend, "
                "asymptotic deficit, and coherent support projection remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Built an exact non-enumerative Foulkes support compiler and measured "
            "the actual hidden-involution mass, exposing k(1-w) as the asymptotic "
            "falsifier for imprimitive support deflation."
        ),
        falsifiers_triggered=[
            "The h_a[h_3] one-register support mass rises substantially through n=30.",
            "At all computed widths, tensor support mass is still below one in a million.",
            "General plethysm hardness cannot be promoted to a quantum lower bound.",
        ],
    )


def write_foulkes_support_mass_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_foulkes_support_mass_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_foulkes_support_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
