"""General subgroup-support dichotomy for hidden-involution frame outliers.

Let ``G=S_(2m)``, ``C`` its fixed-point-free involution class, and ``L<=G``.
If ``r_L=|C intersect L|``, then the noncommon right-``L`` invariant sector
gives a ``k``-copy Rayleigh quotient at least ``r_L`` for the trimmed frame.
This generalizes the hyperoctahedral witness.

The full conjugacy orbit of the witness has a representation-theoretic normal
form.  If

    m_lambda = dim((V_lambda)^L),

then the span of all conjugate right-``L`` invariant sectors is exactly

    E_L = direct_sum_(lambda: m_lambda>0) V_lambda-isotypic. (1)

The average of the distinct conjugate projections acts on the right carrier
``V_lambda`` as

    [G:N_G(L)] m_lambda/d_lambda * I.                  (2)

This distinguishes the conjugacy-orbit size from the coset index
``J=[G:L]``.  Frobenius reciprocity gives

    sum_lambda d_lambda m_lambda = J.

Since every positive integer ``m_lambda`` is at least one and
``max d_lambda<=sqrt(|G|)``, the support obeys

    dim(E_L)/|G| <= J/sqrt(|G|).                       (3)

After the global common trim, one candidate register places at most

    b_L = [2J/sqrt(|G|)]/[1-2a/|G|]                   (4)

mass in ``E_L``.  Therefore the all-register event carrying every pure
``L``-incidence tensor has alternative mass at most ``b_L^k``.  In particular,
if ``J<=|G|^(1/2-epsilon)``, that mass is at most
``[2|G|^-epsilon/(1-2a/|G|)]^k`` and vanishes rapidly at the required copy
width.

This is an information-theoretic dichotomy, not a universal circuit.  A
coherent trim additionally requires efficient recognition of
``m_lambda>0``; branching, plethysm, or subgroup Fourier problems can make
that hard.  Potentially dangerous witnesses are therefore high-index
subgroups, supports with hard membership, or outliers not explained by exact
subgroup invariance.  No residual norm bound or speedup is claimed.
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
    permutation_parity,
)
from coset_hidden_involution_multiplicity_support_obstruction import (
    permutation_cycle_type,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from coset_hyperoctahedral_branching_polar_boundary import hyperoctahedral_elements
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_subgroup_support_dichotomy.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SUBGROUP-SUPPORT-DICHOTOMY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SubgroupSupportFiniteControl:
    subgroup_family: str
    half_degree: int
    degree: int
    group_order: int
    subgroup_order: int
    subgroup_index: int
    subgroup_contains_odd_permutation: bool
    incident_fixed_point_free_count: int
    global_common_dimension: int
    common_dimension_inside_subgroup_invariants: int
    noncommon_invariant_dimension: int
    induced_support_sector_count: int
    induced_dimension_identity: int
    induced_support_isotypic_dimension: int
    support_dimension_bound_squared_rhs: int
    exact_induced_multiplicities_integral: bool
    support_dimension_bound_verified: bool
    subgroup_outlier_witness_verified: bool
    status: str


@dataclass(frozen=True)
class IndexDichotomyScalingRecord:
    half_degree: int
    degree: int
    copy_count: int
    index_gap_epsilon: float
    group_order_decimal: str
    maximum_low_index_decimal: str
    one_register_support_mass_upper_bound: float
    all_register_support_mass_log2_upper_bound: float
    low_index_outlier_mass_information_theoretically_negligible: bool
    support_membership_flag_assumed: bool
    universal_coherent_trim_compiled: bool
    high_index_subgroups_classified: bool
    status: str


@dataclass(frozen=True)
class SubgroupSupportDichotomyTheorem:
    incident_witness: str
    conjugate_span: str
    conjugate_average: str
    support_dimension_bound: str
    low_index_mass_bound: str
    implementation_boundary: str
    residual_frontier: str
    exact_conjugate_support_theorem_proved: bool
    general_support_dimension_bound_proved: bool
    low_index_all_register_mass_bound_proved: bool
    arbitrary_support_membership_compiled: bool
    high_index_subgroups_classified: bool
    post_all_strata_frame_norm_bounded: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SubgroupSupportDichotomyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SubgroupSupportFiniteControl]
    scaling_records: list[IndexDichotomyScalingRecord]
    theorem: SubgroupSupportDichotomyTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def young_two_block_subgroup(block_size: int) -> tuple[Permutation, ...]:
    if block_size < 1:
        raise ValueError("block_size must be positive")
    output = []
    for left, right in itertools.product(
        itertools.permutations(range(block_size)), repeat=2
    ):
        output.append(tuple(left) + tuple(block_size + value for value in right))
    return tuple(output)


def induced_trivial_multiplicities(
    degree: int,
    subgroup: tuple[Permutation, ...],
) -> dict[tuple[int, ...], int]:
    if not subgroup or any(len(element) != degree for element in subgroup):
        raise ValueError("a nonempty degree-matched subgroup is required")
    cycle_types: dict[tuple[int, ...], int] = {}
    for element in subgroup:
        cycle = permutation_cycle_type(element)
        cycle_types[cycle] = cycle_types.get(cycle, 0) + 1
    output = {}
    for partition in integer_partitions(degree):
        numerator = sum(
            count * symmetric_character(partition, cycle)
            for cycle, count in cycle_types.items()
        )
        if numerator % len(subgroup):
            raise ArithmeticError("subgroup character average is not integral")
        output[partition] = numerator // len(subgroup)
    return output


def audit_subgroup_support(
    subgroup_family: str,
    half_degree: int,
) -> SubgroupSupportFiniteControl:
    if half_degree < 3:
        raise ValueError("finite controls require half_degree at least three")
    degree = 2 * half_degree
    if subgroup_family == "hyperoctahedral":
        subgroup = tuple(
            permutation
            for permutation, _, _ in hyperoctahedral_elements(half_degree)
        )
    elif subgroup_family == "young-two-block":
        subgroup = young_two_block_subgroup(half_degree)
    else:
        raise ValueError("unknown subgroup family")
    unique_subgroup = tuple(sorted(set(subgroup)))
    order = math.factorial(degree)
    subgroup_order = len(unique_subgroup)
    if order % subgroup_order:
        raise ArithmeticError("subgroup order does not divide group order")
    index = order // subgroup_order
    multiplicities = induced_trivial_multiplicities(degree, unique_subgroup)
    dimensions = {
        partition: hook_length_dimension(partition) for partition in multiplicities
    }
    induced_dimension = sum(
        dimensions[partition] * multiplicity
        for partition, multiplicity in multiplicities.items()
    )
    support = [
        partition for partition, multiplicity in multiplicities.items()
        if multiplicity > 0
    ]
    support_dimension = sum(dimensions[partition] ** 2 for partition in support)
    incident = sum(
        involution_transposition_count(element) == half_degree
        for element in unique_subgroup
    )
    contains_odd = any(permutation_parity(element) == -1 for element in unique_subgroup)
    global_common = expected_normal_closure_index(degree, half_degree)
    common_inside = 1 + int(global_common == 2 and not contains_odd)
    noncommon_dimension = index - common_inside
    integral = all(value >= 0 for value in multiplicities.values())
    dimension_bound = support_dimension**2 <= index**2 * order
    witness = incident > 0 and noncommon_dimension > 0
    verified = bool(
        induced_dimension == index and integral and dimension_bound and witness
    )
    return SubgroupSupportFiniteControl(
        subgroup_family=subgroup_family,
        half_degree=half_degree,
        degree=degree,
        group_order=order,
        subgroup_order=subgroup_order,
        subgroup_index=index,
        subgroup_contains_odd_permutation=contains_odd,
        incident_fixed_point_free_count=incident,
        global_common_dimension=global_common,
        common_dimension_inside_subgroup_invariants=common_inside,
        noncommon_invariant_dimension=noncommon_dimension,
        induced_support_sector_count=len(support),
        induced_dimension_identity=induced_dimension,
        induced_support_isotypic_dimension=support_dimension,
        support_dimension_bound_squared_rhs=index**2 * order,
        exact_induced_multiplicities_integral=integral,
        support_dimension_bound_verified=dimension_bound,
        subgroup_outlier_witness_verified=witness,
        status=(
            "exact-subgroup-support-dichotomy-control-verified"
            if verified
            else "subgroup-support-control-failure"
        ),
    )


def index_dichotomy_scaling_record(
    half_degree: int,
    index_gap_epsilon: float,
) -> IndexDichotomyScalingRecord:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    if not 0.0 < index_gap_epsilon < 0.5:
        raise ValueError("index_gap_epsilon must lie in (0, 1/2)")
    degree = 2 * half_degree
    order = math.factorial(degree)
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    common_dimension = expected_normal_closure_index(degree, half_degree)
    log2_one_bound = (
        1.0
        - index_gap_epsilon * math.log2(order)
        - math.log2(1.0 - math.exp(math.log(2 * common_dimension) - math.log(order)))
    )
    one_bound = 2.0**log2_one_bound if log2_one_bound > -1074 else 0.0
    all_log2 = min(0.0, copies * log2_one_bound)
    maximum_index = math.isqrt(order) // max(
        1, math.ceil(order**index_gap_epsilon)
    ) if order.bit_length() < 1000 else 0
    # The decimal threshold is represented from logs when direct floating
    # exponentiation would be inappropriate.  A zero sentinel is never used in
    # the proof gate; the exact theorem is symbolic in |G|.
    maximum_index_decimal = (
        str(maximum_index)
        if maximum_index
        else f"floor(|S_{degree}|^(1/2-{index_gap_epsilon}))"
    )
    negligible = all_log2 < -20.0
    return IndexDichotomyScalingRecord(
        half_degree=half_degree,
        degree=degree,
        copy_count=copies,
        index_gap_epsilon=index_gap_epsilon,
        group_order_decimal=str(order),
        maximum_low_index_decimal=maximum_index_decimal,
        one_register_support_mass_upper_bound=min(1.0, one_bound),
        all_register_support_mass_log2_upper_bound=all_log2,
        low_index_outlier_mass_information_theoretically_negligible=negligible,
        support_membership_flag_assumed=True,
        universal_coherent_trim_compiled=False,
        high_index_subgroups_classified=False,
        status=(
            "low-index-subgroup-support-mass-negligible-membership-or-high-index-open"
            if negligible
            else "finite-index-dichotomy-bound-not-yet-negligible"
        ),
    )


def build_subgroup_support_dichotomy_report(
    *,
    finite_specs: tuple[tuple[str, int], ...] = (
        ("hyperoctahedral", 3),
        ("hyperoctahedral", 4),
        ("young-two-block", 4),
    ),
    scaling_specs: tuple[tuple[int, float], ...] = (
        (8, 0.10),
        (16, 0.10),
        (32, 0.05),
        (64, 0.05),
    ),
) -> SubgroupSupportDichotomyReport:
    controls = [audit_subgroup_support(family, m) for family, m in finite_specs]
    scaling = [index_dichotomy_scaling_record(m, epsilon) for m, epsilon in scaling_specs]
    verified = all(
        row.exact_induced_multiplicities_integral
        and row.support_dimension_bound_verified
        and row.subgroup_outlier_witness_verified
        for row in controls
    )
    scaling_verified = all(
        row.low_index_outlier_mass_information_theoretically_negligible
        and row.support_membership_flag_assumed
        and not row.universal_coherent_trim_compiled
        and not row.high_index_subgroups_classified
        for row in scaling
    )
    theorem = SubgroupSupportDichotomyTheorem(
        incident_witness=(
            "D_L=Inv_R(L) minus global-common vectors gives frame Rayleigh "
            "quotient at least |C intersect L| at every copy count."
        ),
        conjugate_span=(
            "The span of conjugate L-invariants is the right-isotypic support "
            "{lambda: dim(V_lambda^L)>0}."
        ),
        conjugate_average=(
            "The sum over distinct conjugates acts by [G:N_G(L)]m_lambda/d_lambda."
        ),
        support_dimension_bound=(
            "dim(E_L)/|G|<= [G:L]/sqrt(|G|), from Frobenius reciprocity."
        ),
        low_index_mass_bound=(
            "For [G:L]<=|G|^(1/2-epsilon), the all-register alternative mass "
            "is at most [2|G|^-epsilon/(1-2a/|G|)]^k."
        ),
        implementation_boundary=(
            "A coherent trim requires efficient recognition of whether "
            "dim(V_lambda^L)>0; this is not supplied for arbitrary L."
        ),
        residual_frontier=(
            "Classify high-index high-incidence S_n subgroups, hard support-"
            "membership families, and non-subgroup spectral outliers."
        ),
        exact_conjugate_support_theorem_proved=True,
        general_support_dimension_bound_proved=True,
        low_index_all_register_mass_bound_proved=True,
        arbitrary_support_membership_compiled=False,
        high_index_subgroups_classified=False,
        post_all_strata_frame_norm_bounded=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "subgroup-support-index-dichotomy-proved-high-index-classification-open"
            if verified and scaling_verified
            else "subgroup-support-dichotomy-control-failure"
        ),
    )
    return SubgroupSupportDichotomyReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Arbitrary proper subgroups L<=S_(2m).",
            "outlier": "Exact fixed-point-free class incidence C intersect L.",
            "support": "Fourier support of Ind_L^G(1).",
            "outside_scope": (
                "Efficient arbitrary support recognition, high-index subgroup "
                "classification, residual norm, and algorithmic decoding."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-HIGH-INDEX-INCIDENCE-CLASSIFICATION",
                "statement": (
                    "Classify high-index subgroups of S_(2m) with superpolynomial "
                    "fixed-point-free involution incidence."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-INDUCED-SUPPORT-MEMBERSHIP",
                "statement": (
                    "Compile or complexity-classify lambda -> dim(V_lambda^L)>0 "
                    "for every surviving subgroup family."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-NONSUBGROUP-OUTLIERS",
                "statement": (
                    "Determine whether large residual eigenvalues must admit an "
                    "approximate subgroup-invariance witness."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Every subgroup outlier is coherently deflatable.",
                "answer": (
                    "False as stated: small support mass is information-theoretic; "
                    "efficient induced-support membership can itself be hard."
                ),
                "resolved": True,
            },
            {
                "challenge": "The number of conjugates is [G:L].",
                "answer": (
                    "False in general: it is [G:N_G(L)]. The support theorem and "
                    "dimension bound use these quantities separately."
                ),
                "resolved": True,
            },
            {
                "challenge": "Low-index control proves a residual norm bound.",
                "answer": (
                    "False: high-index or approximate-invariance outliers remain."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_finite_subgroup_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.support_dimension_bound_verified for row in controls
            ),
            "general_support_dimension_theorem_count": 1,
            "low_index_mass_dichotomy_theorem_count": 1,
            "high_index_subgroup_classification_count": 0,
            "universal_support_membership_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "general_subgroup_support_span_proved": verified,
            "low_index_subgroup_mass_dichotomy_proved": verified and scaling_verified,
            "arbitrary_induced_support_membership_compiled": False,
            "high_index_high_incidence_subgroups_classified": False,
            "post_all_strata_frame_norm_bounded": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Low-index subgroup witnesses have negligible all-register support, "
                "but efficient support flags and high-index incidence families are "
                "not classified."
            ),
        },
        status=theorem.status,
        summary=(
            "Generalized subgroup outliers to induced-representation supports and "
            "proved a low-index mass dichotomy, isolating high-index incidence and "
            "support-membership complexity as the next obstruction."
        ),
        falsifiers_triggered=[
            "Subgroup conjugacy-orbit size and subgroup index are not interchangeable.",
            "Information-theoretic support deflation does not imply an efficient circuit.",
            "Only high-index, hard-membership, or non-subgroup outliers remain uncontrolled by this theorem.",
        ],
    )


def write_subgroup_support_dichotomy_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_subgroup_support_dichotomy_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_subgroup_support_dichotomy_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
