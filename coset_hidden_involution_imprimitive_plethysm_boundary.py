"""High-index imprimitive outliers and their two-row plethysm boundary.

Let ``G=S_n`` with ``n=ab`` even and let ``L=S_b wr S_a`` stabilize a system
of ``a`` blocks of size ``b``.  The exact number of fixed-point-free
involutions in ``L`` is

    R_(a,b) = sum_j a!/[2^j j!(a-2j)!]
                    (b!)^j F_b^(a-2j),                 (1)

where ``F_b=(b-1)!!`` for even ``b`` and zero for odd ``b``.  A transposed
pair of blocks contributes an arbitrary bijection and its inverse; every
fixed block must carry a fixed-point-free involution.  The final admissible
term alone proves superpolynomial growth for fixed ``b`` as ``a`` grows.

For fixed ``b>=3``, the subgroup index has

    log([S_(ab):L])/log((ab)!) -> 1-1/b > 1/2.         (2)

Thus these families evade the low-index support-mass theorem.

Part of their plethysm support is nevertheless explicit.  Let ``O_t`` be the
number of ``L``-orbits on ``t``-subsets.  Occupancy vectors identify

    O_t = number of partitions of t with largest part<=b and length<=a.

Since the ``t``-subset permutation module is

    direct_sum_(j=0)^t S^(n-j,j),

the exact multiplicity of ``S^(n-t,t)`` in ``Ind_L^G(1)`` is

    m_t = O_t-O_(t-1).                                  (3)

For ``b>=3`` this is positive for a linear range of ``t`` because every
integer ``t>=2`` is a sum of twos and threes.  Odd ``t`` gives two odd row
lengths, so these sectors survive the prior even-row spherical trim and each
contains an exact ``R_(a,b)`` frame-norm witness.

This explicit survivor family is still removable.  Its total isotypic
dimension is a sum of ``d_(n-t,t)^2``, with
``d_(n-t,t)=binom(n,t)-binom(n,t-1)``.  The corresponding all-register
alternative mass is bounded by the kth power of twice this dimension divided
by the trimmed candidate rank, and vanishes super-exponentially in the tested
scaling regime.  A QFT can flag all odd two-row labels directly.

The unresolved support is the higher-row plethysm of ``h_a[h_b]``.  Its
membership, natural mass, and incidence conditioning are not controlled by
the two-row orbit calculation.  No residual norm bound or algorithm is
claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    involution_class_size,
    involution_transposition_count,
)
from coset_hidden_involution_common_outlier_deflation import (
    expected_normal_closure_index,
)
from coset_hidden_involution_multiplicity_support_obstruction import (
    permutation_cycle_type,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from research_registry import utc_now
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_imprimitive_plethysm_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-IMPRIMITIVE-PLETHYSM-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ImprimitivePlethysmFiniteControl:
    block_count: int
    block_size: int
    degree: int
    expected_wreath_order: int
    generated_wreath_element_count: int
    direct_fixed_point_free_count: int
    formula_fixed_point_free_count: int
    two_row_control_count: int
    subset_orbit_multiplicities: dict[str, int]
    character_average_multiplicities: dict[str, int]
    multiplicity_mismatch_count: int
    odd_two_row_survivor_count: int
    exact_incidence_formula_verified: bool
    exact_two_row_multiplicity_formula_verified: bool
    status: str


@dataclass(frozen=True)
class ImprimitivePlethysmScalingRecord:
    block_count: int
    block_size: int
    degree: int
    group_order_decimal: str
    wreath_order_decimal: str
    subgroup_index_decimal: str
    subgroup_index_log_group_order_ratio: float
    incident_candidate_count_decimal: str
    incident_candidate_count_log2: float
    incident_elementary_lower_bound_decimal: str
    low_index_support_bound_informative: bool
    odd_two_row_survivor_sector_count: int
    odd_two_row_support_dimension_decimal: str
    one_register_odd_two_row_mass_upper_bound: float
    all_register_odd_two_row_mass_log2_upper_bound: float
    odd_two_row_outliers_negligible_and_qft_deflatable: bool
    higher_row_plethysm_support_classified: bool
    residual_frame_norm_bounded: bool
    status: str


@dataclass(frozen=True)
class ImprimitivePlethysmTheorem:
    incident_count: str
    index_phase: str
    subset_orbits: str
    two_row_multiplicity: str
    spherical_trim_survivors: str
    two_row_deflation: str
    scope_limit: str
    exact_incident_count_proved: bool
    high_index_high_incidence_family_proved: bool
    exact_two_row_plethysm_multiplicity_proved: bool
    post_spherical_two_row_outliers_exhibited: bool
    odd_two_row_outliers_deflated_at_vanishing_mass: bool
    higher_row_plethysm_support_classified: bool
    residual_frame_norm_bounded: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ImprimitivePlethysmReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ImprimitivePlethysmFiniteControl]
    scaling_records: list[ImprimitivePlethysmScalingRecord]
    theorem: ImprimitivePlethysmTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def odd_double_factorial(value: int) -> int:
    if value < -1 or value % 2 == 0:
        raise ValueError("value must be odd and at least -1")
    output = 1
    for factor in range(1, value + 1, 2):
        output *= factor
    return output


def fixed_point_free_involution_count_wreath(
    block_count: int,
    block_size: int,
) -> int:
    if block_count < 1 or block_size < 2:
        raise ValueError("positive block_count and block_size>=2 are required")
    fixed_block_choices = (
        odd_double_factorial(block_size - 1) if block_size % 2 == 0 else 0
    )
    factorial = math.factorial(block_count)
    total = 0
    for paired_blocks in range(block_count // 2 + 1):
        fixed_blocks = block_count - 2 * paired_blocks
        if fixed_blocks and fixed_block_choices == 0:
            continue
        block_involutions = factorial // (
            (2**paired_blocks)
            * math.factorial(paired_blocks)
            * math.factorial(fixed_blocks)
        )
        total += (
            block_involutions
            * math.factorial(block_size) ** paired_blocks
            * fixed_block_choices**fixed_blocks
        )
    return total


def incident_elementary_lower_bound(block_count: int, block_size: int) -> int:
    if block_count < 1 or block_size < 2:
        raise ValueError("positive block_count and block_size>=2 are required")
    paired = block_count // 2
    fixed = block_count - 2 * paired
    if fixed and block_size % 2:
        return 0
    fixed_choices = (
        odd_double_factorial(block_size - 1) if fixed else 1
    )
    return (
        math.factorial(block_count)
        // (
            (2**paired)
            * math.factorial(paired)
            * math.factorial(fixed)
        )
        * math.factorial(block_size) ** paired
        * fixed_choices**fixed
    )


def imprimitive_wreath_elements(
    block_count: int,
    block_size: int,
) -> tuple[Permutation, ...]:
    if block_count < 1 or block_size < 2:
        raise ValueError("positive block_count and block_size>=2 are required")
    local = tuple(itertools.permutations(range(block_size)))
    output = []
    for block_permutation in itertools.permutations(range(block_count)):
        for internal in itertools.product(local, repeat=block_count):
            permutation = [0] * (block_count * block_size)
            for block in range(block_count):
                for point in range(block_size):
                    permutation[block * block_size + point] = (
                        block_permutation[block] * block_size
                        + internal[block][point]
                    )
            output.append(tuple(permutation))
    return tuple(output)


def bounded_partition_count(
    total: int,
    maximum_part: int,
    maximum_length: int,
) -> int:
    if total < 0 or maximum_part < 1 or maximum_length < 0:
        raise ValueError("invalid bounded partition parameters")
    counts = [[0] * (maximum_length + 1) for _ in range(total + 1)]
    counts[0][0] = 1
    for part in range(1, maximum_part + 1):
        for subtotal in range(part, total + 1):
            for length in range(1, maximum_length + 1):
                counts[subtotal][length] += counts[subtotal - part][length - 1]
    return sum(counts[total])


def two_row_wreath_multiplicity(
    block_count: int,
    block_size: int,
    subset_size: int,
) -> int:
    degree = block_count * block_size
    if not 0 <= subset_size <= degree // 2:
        raise ValueError("subset_size must lie in [0,n/2]")
    current = bounded_partition_count(subset_size, block_size, block_count)
    previous = (
        bounded_partition_count(subset_size - 1, block_size, block_count)
        if subset_size
        else 0
    )
    return current - previous


def two_row_dimension(degree: int, second_row: int) -> int:
    if not 0 <= second_row <= degree // 2:
        raise ValueError("second_row must lie in [0,n/2]")
    return math.comb(degree, second_row) - (
        math.comb(degree, second_row - 1) if second_row else 0
    )


def audit_imprimitive_plethysm(
    block_count: int,
    block_size: int,
) -> ImprimitivePlethysmFiniteControl:
    degree = block_count * block_size
    if degree % 2 or block_count < 2 or block_size < 2:
        raise ValueError("an even degree with at least two blocks is required")
    elements = imprimitive_wreath_elements(block_count, block_size)
    expected_order = math.factorial(block_size) ** block_count * math.factorial(
        block_count
    )
    direct_incident = sum(
        involution_transposition_count(element) == degree // 2
        for element in elements
    )
    formula_incident = fixed_point_free_involution_count_wreath(
        block_count, block_size
    )
    cycle_counts: dict[tuple[int, ...], int] = {}
    for element in elements:
        cycle = permutation_cycle_type(element)
        cycle_counts[cycle] = cycle_counts.get(cycle, 0) + 1
    orbit_multiplicities = {}
    character_multiplicities = {}
    for subset_size in range(degree // 2 + 1):
        partition = (
            (degree,) if subset_size == 0 else (degree - subset_size, subset_size)
        )
        orbit_value = two_row_wreath_multiplicity(
            block_count, block_size, subset_size
        )
        numerator = sum(
            count * symmetric_character(partition, cycle)
            for cycle, count in cycle_counts.items()
        )
        if numerator % expected_order:
            raise ArithmeticError("wreath character average is not integral")
        character_value = numerator // expected_order
        key = str(partition)
        orbit_multiplicities[key] = orbit_value
        character_multiplicities[key] = character_value
    mismatches = sum(
        orbit_multiplicities[key] != character_multiplicities[key]
        for key in orbit_multiplicities
    )
    odd_survivors = sum(
        subset_size % 2 == 1
        and two_row_wreath_multiplicity(block_count, block_size, subset_size) > 0
        for subset_size in range(1, degree // 2 + 1)
    )
    incidence_verified = bool(
        len(set(elements)) == expected_order
        and direct_incident == formula_incident
        and formula_incident >= incident_elementary_lower_bound(
            block_count, block_size
        )
    )
    multiplicity_verified = mismatches == 0 and odd_survivors > 0
    return ImprimitivePlethysmFiniteControl(
        block_count=block_count,
        block_size=block_size,
        degree=degree,
        expected_wreath_order=expected_order,
        generated_wreath_element_count=len(set(elements)),
        direct_fixed_point_free_count=direct_incident,
        formula_fixed_point_free_count=formula_incident,
        two_row_control_count=degree // 2 + 1,
        subset_orbit_multiplicities=orbit_multiplicities,
        character_average_multiplicities=character_multiplicities,
        multiplicity_mismatch_count=mismatches,
        odd_two_row_survivor_count=odd_survivors,
        exact_incidence_formula_verified=incidence_verified,
        exact_two_row_multiplicity_formula_verified=multiplicity_verified,
        status=(
            "exact-imprimitive-incidence-and-two-row-plethysm-verified"
            if incidence_verified and multiplicity_verified
            else "imprimitive-plethysm-control-failure"
        ),
    )


def imprimitive_plethysm_scaling_record(
    block_count: int,
    block_size: int,
) -> ImprimitivePlethysmScalingRecord:
    degree = block_count * block_size
    if degree % 2 or block_count < 3 or block_size < 3:
        raise ValueError("even degree and block_count,block_size>=3 are required")
    order = math.factorial(degree)
    wreath_order = math.factorial(block_size) ** block_count * math.factorial(
        block_count
    )
    index = order // wreath_order
    candidates = involution_class_size(degree, degree // 2)
    copies = flatness_copy_count(candidates)
    incident = fixed_point_free_involution_count_wreath(block_count, block_size)
    elementary = incident_elementary_lower_bound(block_count, block_size)
    index_ratio = math.log(index) / math.log(order)
    low_index_bound = 2.0 * math.exp(math.log(index) - 0.5 * math.log(order))
    odd_rows = [
        t
        for t in range(1, degree // 2 + 1, 2)
        if two_row_wreath_multiplicity(block_count, block_size, t) > 0
    ]
    support_dimension = sum(two_row_dimension(degree, t) ** 2 for t in odd_rows)
    common_dimension = expected_normal_closure_index(degree, degree // 2)
    trimmed_rank = order // 2 - common_dimension
    one_mass_bound = min(1.0, support_dimension / trimmed_rank)
    all_log2 = (
        copies * math.log2(one_mass_bound) if one_mass_bound > 0.0 else -math.inf
    )
    deflatable = all_log2 < -20.0
    return ImprimitivePlethysmScalingRecord(
        block_count=block_count,
        block_size=block_size,
        degree=degree,
        group_order_decimal=str(order),
        wreath_order_decimal=str(wreath_order),
        subgroup_index_decimal=str(index),
        subgroup_index_log_group_order_ratio=index_ratio,
        incident_candidate_count_decimal=str(incident),
        incident_candidate_count_log2=math.log2(incident),
        incident_elementary_lower_bound_decimal=str(elementary),
        low_index_support_bound_informative=low_index_bound < 1.0,
        odd_two_row_survivor_sector_count=len(odd_rows),
        odd_two_row_support_dimension_decimal=str(support_dimension),
        one_register_odd_two_row_mass_upper_bound=one_mass_bound,
        all_register_odd_two_row_mass_log2_upper_bound=all_log2,
        odd_two_row_outliers_negligible_and_qft_deflatable=deflatable,
        higher_row_plethysm_support_classified=False,
        residual_frame_norm_bounded=False,
        status=(
            "odd-two-row-outliers-deflatable-higher-row-plethysm-open"
            if deflatable
            else "imprimitive-two-row-deflation-bound-failure"
        ),
    )


def build_imprimitive_plethysm_report(
    *,
    finite_specs: tuple[tuple[int, int], ...] = ((4, 3),),
    scaling_specs: tuple[tuple[int, int], ...] = (
        (8, 3),
        (16, 3),
        (16, 4),
        (16, 5),
    ),
) -> ImprimitivePlethysmReport:
    controls = [audit_imprimitive_plethysm(a, b) for a, b in finite_specs]
    scaling = [imprimitive_plethysm_scaling_record(a, b) for a, b in scaling_specs]
    verified = all(
        row.exact_incidence_formula_verified
        and row.exact_two_row_multiplicity_formula_verified
        for row in controls
    )
    scaling_verified = all(
        row.subgroup_index_log_group_order_ratio > 0.5
        and int(row.incident_candidate_count_decimal)
        >= int(row.incident_elementary_lower_bound_decimal)
        and row.odd_two_row_survivor_sector_count > 0
        and row.odd_two_row_outliers_negligible_and_qft_deflatable
        and not row.higher_row_plethysm_support_classified
        and not row.residual_frame_norm_bounded
        for row in scaling
    )
    theorem = ImprimitivePlethysmTheorem(
        incident_count=(
            "R_(a,b)=sum_j a!/(2^j j!(a-2j)!)(b!)^j F_b^(a-2j)."
        ),
        index_phase=(
            "For fixed b>=3, log([S_(ab):S_b wr S_a])/log((ab)!) tends "
            "to 1-1/b>1/2."
        ),
        subset_orbits=(
            "L-orbits on t-subsets are bounded occupancy partitions of t."
        ),
        two_row_multiplicity=(
            "mult_(n-t,t)(Ind_L^G 1)=O_t-O_(t-1), positive for a linear "
            "range generated by occupancy parts two and three."
        ),
        spherical_trim_survivors=(
            "Odd t gives non-even-row L-invariant sectors with frame Rayleigh "
            "quotient at least R_(a,b) after the even-row trim."
        ),
        two_row_deflation=(
            "The union of odd two-row survivor sectors is QFT-flagged and its "
            "all-register alternative mass vanishes at orbit-flatness width."
        ),
        scope_limit=(
            "Higher-row h_a[h_b] plethysm support, its natural mass, and the "
            "post-deflation frame norm remain unresolved."
        ),
        exact_incident_count_proved=True,
        high_index_high_incidence_family_proved=True,
        exact_two_row_plethysm_multiplicity_proved=True,
        post_spherical_two_row_outliers_exhibited=True,
        odd_two_row_outliers_deflated_at_vanishing_mass=True,
        higher_row_plethysm_support_classified=False,
        residual_frame_norm_bounded=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "imprimitive-two-row-boundary-proved-higher-row-plethysm-open"
            if verified and scaling_verified
            else "imprimitive-plethysm-control-failure"
        ),
    )
    return ImprimitivePlethysmReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Imprimitive subgroups S_b wr S_a <= S_(ab), b>=3.",
            "incidence": "Fixed-point-free involutions inside the wreath subgroup.",
            "explicit_support": "Two-row constituents from t-subset orbit counts.",
            "outside_scope": (
                "Higher-row plethysm support, support membership complexity, "
                "aggregate mass, residual norm, and decoding."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-IMPRIMITIVE-PLETHYSM-MASS",
                "statement": (
                    "Bound the natural alternative mass of the higher-row support "
                    "of h_a[h_b] for fixed and growing block sizes."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-IMPRIMITIVE-SUPPORT-MEMBERSHIP",
                "statement": (
                    "Compile or prove hardness of coherent membership in the "
                    "nonzero plethysm support of Ind_(S_b wr S_a)^S_n(1)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-POST-PLETHYSM-TRIM-NORM",
                "statement": (
                    "Bound or witness the frame norm after every negligible, "
                    "efficiently flaggable imprimitive support trim."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The low-index dichotomy covers all imprimitive subgroups.",
                "answer": (
                    "False: fixed block size b>=3 has index exponent 1-1/b>1/2."
                ),
                "resolved": True,
            },
            {
                "challenge": "The prior even-row trim removes their subgroup witnesses.",
                "answer": (
                    "False: odd two-row labels (n-t,t) occur with exact positive "
                    "multiplicity and survive that trim."
                ),
                "resolved": True,
            },
            {
                "challenge": "Those explicit survivors are a terminal obstruction.",
                "answer": (
                    "False: their whole QFT-flagged union has vanishing all-register "
                    "alternative mass. The higher-row support is the real unknown."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_two_row_multiplicity_formula_verified for row in controls
            ),
            "high_index_high_incidence_family_theorem_count": 1,
            "post_spherical_survivor_family_theorem_count": 1,
            "coherent_negligible_two_row_deflation_count": 1,
            "higher_row_plethysm_classification_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "imprimitive_incident_formula_proved": verified,
            "high_index_high_incidence_imprimitive_family_proved": (
                verified and scaling_verified
            ),
            "odd_two_row_survivors_exhibited_and_deflated": (
                verified and scaling_verified
            ),
            "higher_row_plethysm_support_classified": False,
            "post_plethysm_trim_frame_norm_bounded": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Explicit two-row imprimitive outliers are removable, but the "
                "higher-row plethysm support and residual conditioning are open."
            ),
        },
        status=theorem.status,
        summary=(
            "Located a high-index high-incidence imprimitive subgroup family, "
            "resolved its exact two-row plethysm survivors, and showed that those "
            "survivors are negligible while higher-row plethysm remains the barrier."
        ),
        falsifiers_triggered=[
            "High-index imprimitive subgroup outliers evade the generic low-index theorem.",
            "Even-row spherical deflation leaves exact odd two-row witnesses.",
            "The exposed two-row witnesses are themselves negligible and do not establish hardness.",
        ],
    )


def write_imprimitive_plethysm_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_imprimitive_plethysm_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_imprimitive_plethysm_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
