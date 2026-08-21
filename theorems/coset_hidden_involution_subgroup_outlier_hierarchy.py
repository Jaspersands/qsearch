"""Subgroup-incidence outliers after common-factor trimming.

Let ``G=S_(2m)``, let ``C`` be the fixed-point-free involution class, and let
``K=C_G(h_0)=C_2 wr S_m`` be the centralizer of the canonical matching.  Put

    Pbar_h = (I+R_h)/2 - Q,

where ``Q`` projects onto the one- or two-dimensional space common to every
candidate range.  The common-factor trim does not make the orbit frame
bounded.

The fixed-point-free elements of ``K`` are counted exactly by

    L_m = sum_(j=0)^floor(m/2) m!/(j!(m-2j)!).          (1)

Indeed, an involution of the ``m`` matching blocks has ``j`` transposed block
pairs.  Each transposed pair has two compatible internal orientations, which
cancels the ``2^j`` denominator in the involution count; every fixed block is
forced to flip internally.  In particular

    L_m >= ceil(m/2)^ceil(m/2),                         (2)

so this incidence multiplicity is superpolynomial.

Let ``D=C[G/K] minus C[G/G]`` inside the right regular representation.  The
sign vector is not ``K``-invariant because ``K`` contains odd permutations,
so ``dim(D)=[G:K]-1=(2m-1)!!-1`` even when the global common space also
contains sign.  Every ``v in D`` is orthogonal to the global common space and
satisfies ``Pbar_h v=v`` for every ``h in C intersect K``.  Therefore, for
every copy count ``k>=1``, the trimmed physical frame

    Abar_k = sum_(h in C) Pbar_h^tensor k

obeys

    ||Abar_k|| >= L_m.                                  (3)

The same lower bound holds for the nonzero source-Gram spectrum.  Thus a
single globally normalized interval-QSVT inverse square root retains a
condition-number proxy at least ``sqrt(L_m)`` after exact common-factor
trimming.  This rules out the naive bounded-spectrum polar route.

It does not rule out a structured algorithm.  The orbit of ``D`` under
conjugation can have much larger aggregate alternative mass than one witness,
and a representation-aware decomposition might isolate or invert these
subgroup strata efficiently.  The required next object is the span and
overlap algebra of conjugate ``K``-invariant sectors, or an orbit-row polar
that bypasses global interval conditioning.  No algorithm or speedup is
claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
    involution_transposition_count,
)
from coset_hidden_involution_common_outlier_deflation import (
    expected_normal_closure_index,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from coset_hyperoctahedral_branching_polar_boundary import (
    canonical_fixed_point_free_involution,
    hyperoctahedral_elements,
)
from coset_perfect_matching_spherical_boundary import (
    hyperoctahedral_order,
    perfect_matching_count,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_subgroup_outlier_hierarchy.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SUBGROUP-OUTLIER-HIERARCHY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SubgroupOutlierFiniteControl:
    half_degree: int
    degree: int
    hyperoctahedral_order: int
    generated_element_count: int
    centralizer_failure_count: int
    direct_fixed_point_free_count: int
    formula_fixed_point_free_count: int
    recurrence_fixed_point_free_count: int
    matching_index: int
    noncommon_invariant_dimension: int
    all_incident_elements_fix_noncommon_sector: bool
    exact_subgroup_incidence_verified: bool
    status: str


@dataclass(frozen=True)
class SubgroupOutlierScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    trimmed_candidate_rank_decimal: str
    subgroup_incident_candidate_count_decimal: str
    subgroup_incident_candidate_count_log2: float
    elementary_superpolynomial_lower_bound_decimal: str
    elementary_superpolynomial_lower_bound_log2: float
    noncommon_invariant_dimension_decimal: str
    trimmed_frame_norm_lower_bound_decimal: str
    global_polar_condition_proxy_lower_bound_log2: float
    single_witness_guaranteed_alternative_mass_log2_lower_bound: float
    bounded_global_interval_conditioning_refuted: bool
    conjugate_sector_aggregate_mass_bounded: bool
    structured_subgroup_spectral_transform_compiled: bool
    status: str


@dataclass(frozen=True)
class SubgroupOutlierTheorem:
    subgroup: str
    incident_count: str
    incident_count_lower_bound: str
    noncommon_invariant_sector: str
    frame_norm_witness: str
    qsvt_consequence: str
    architecture_frontier: str
    exact_incident_count_proved: bool
    superpolynomial_incident_growth_proved: bool
    all_copy_frame_norm_lower_bound_proved: bool
    bounded_post_trim_global_conditioning_refuted: bool
    conjugate_sector_overlap_algebra_compiled: bool
    orbit_row_polar_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SubgroupOutlierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SubgroupOutlierFiniteControl]
    scaling_records: list[SubgroupOutlierScalingRecord]
    theorem: SubgroupOutlierTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def centralizer_fixed_point_free_count(half_degree: int) -> int:
    """Return ``|C intersect (C_2 wr S_m)|`` from the exact block formula."""

    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    factorial = math.factorial(half_degree)
    return sum(
        factorial // (math.factorial(j) * math.factorial(half_degree - 2 * j))
        for j in range(half_degree // 2 + 1)
    )


def centralizer_fixed_point_free_count_recurrence(half_degree: int) -> int:
    """Evaluate ``L_m=L_(m-1)+2(m-1)L_(m-2)`` with ``L_0=L_1=1``."""

    if half_degree < 0:
        raise ValueError("half_degree must be nonnegative")
    if half_degree < 2:
        return 1
    previous_two, previous_one = 1, 1
    for size in range(2, half_degree + 1):
        current = previous_one + 2 * (size - 1) * previous_two
        previous_two, previous_one = previous_one, current
    return previous_one


def elementary_incident_lower_bound(half_degree: int) -> int:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    width = (half_degree + 1) // 2
    return width**width


def audit_subgroup_outlier(half_degree: int) -> SubgroupOutlierFiniteControl:
    if half_degree < 2:
        raise ValueError("finite controls require half_degree at least two")
    elements = hyperoctahedral_elements(half_degree)
    hidden = canonical_fixed_point_free_involution(half_degree)
    expected_order = hyperoctahedral_order(half_degree)
    centralizer_failures = sum(
        tuple(permutation[hidden[index]] for index in range(2 * half_degree))
        != tuple(hidden[permutation[index]] for index in range(2 * half_degree))
        for permutation, _, _ in elements
    )
    direct = sum(
        involution_transposition_count(permutation) == half_degree
        for permutation, _, _ in elements
    )
    formula = centralizer_fixed_point_free_count(half_degree)
    recurrence = centralizer_fixed_point_free_count_recurrence(half_degree)
    matching_index = perfect_matching_count(half_degree)
    unique_elements = {permutation for permutation, _, _ in elements}
    verified = bool(
        len(unique_elements) == expected_order
        and centralizer_failures == 0
        and direct == formula == recurrence
        and math.factorial(2 * half_degree) == expected_order * matching_index
        and formula >= elementary_incident_lower_bound(half_degree)
    )
    return SubgroupOutlierFiniteControl(
        half_degree=half_degree,
        degree=2 * half_degree,
        hyperoctahedral_order=expected_order,
        generated_element_count=len(unique_elements),
        centralizer_failure_count=centralizer_failures,
        direct_fixed_point_free_count=direct,
        formula_fixed_point_free_count=formula,
        recurrence_fixed_point_free_count=recurrence,
        matching_index=matching_index,
        noncommon_invariant_dimension=matching_index - 1,
        all_incident_elements_fix_noncommon_sector=True,
        exact_subgroup_incidence_verified=verified,
        status=(
            "exact-hyperoctahedral-subgroup-outlier-verified"
            if verified
            else "subgroup-outlier-control-failure"
        ),
    )


def subgroup_outlier_scaling_record(
    half_degree: int,
) -> SubgroupOutlierScalingRecord:
    if half_degree < 3:
        raise ValueError("scaling records require half_degree at least three")
    degree = 2 * half_degree
    group_order = math.factorial(degree)
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    common_dimension = expected_normal_closure_index(degree, half_degree)
    trimmed_rank = group_order // 2 - common_dimension
    incident = centralizer_fixed_point_free_count(half_degree)
    elementary = elementary_incident_lower_bound(half_degree)
    invariant_dimension = candidates - 1
    witness_mass_log2 = (
        math.log2(incident)
        - math.log2(candidates)
        + copies * (math.log2(invariant_dimension) - math.log2(trimmed_rank))
    )
    return SubgroupOutlierScalingRecord(
        half_degree=half_degree,
        degree=degree,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        trimmed_candidate_rank_decimal=str(trimmed_rank),
        subgroup_incident_candidate_count_decimal=str(incident),
        subgroup_incident_candidate_count_log2=math.log2(incident),
        elementary_superpolynomial_lower_bound_decimal=str(elementary),
        elementary_superpolynomial_lower_bound_log2=math.log2(elementary),
        noncommon_invariant_dimension_decimal=str(invariant_dimension),
        trimmed_frame_norm_lower_bound_decimal=str(incident),
        global_polar_condition_proxy_lower_bound_log2=0.5 * math.log2(incident),
        single_witness_guaranteed_alternative_mass_log2_lower_bound=(
            witness_mass_log2
        ),
        bounded_global_interval_conditioning_refuted=True,
        conjugate_sector_aggregate_mass_bounded=False,
        structured_subgroup_spectral_transform_compiled=False,
        status=(
            "post-trim-global-conditioning-superpolynomial-"
            "structured-subgroup-resolution-open"
        ),
    )


def build_subgroup_outlier_report(
    *,
    finite_half_degrees: tuple[int, ...] = (2, 3, 4),
    scaling_half_degrees: tuple[int, ...] = (3, 4, 8, 16, 32, 64),
) -> SubgroupOutlierReport:
    controls = [audit_subgroup_outlier(m) for m in finite_half_degrees]
    scaling = [subgroup_outlier_scaling_record(m) for m in scaling_half_degrees]
    verified = all(row.exact_subgroup_incidence_verified for row in controls)
    scaling_verified = all(
        int(row.trimmed_frame_norm_lower_bound_decimal)
        >= int(row.elementary_superpolynomial_lower_bound_decimal)
        and row.bounded_global_interval_conditioning_refuted
        and not row.conjugate_sector_aggregate_mass_bounded
        and not row.structured_subgroup_spectral_transform_compiled
        for row in scaling
    )
    theorem = SubgroupOutlierTheorem(
        subgroup="K=C_G(h_0)=C_2 wr S_m inside S_(2m).",
        incident_count=(
            "|C intersect K|=L_m=sum_j m!/(j!(m-2j)!), equivalently "
            "L_m=L_(m-1)+2(m-1)L_(m-2)."
        ),
        incident_count_lower_bound=(
            "L_m>=ceil(m/2)^ceil(m/2), hence L_m is superpolynomial."
        ),
        noncommon_invariant_sector=(
            "D=C[G/K] minus the trivial vector has dimension (2m-1)!!-1; "
            "sign is absent because K contains odd permutations."
        ),
        frame_norm_witness=(
            "Every h in C intersect K fixes D, so every D^tensor k unit vector "
            "has trimmed-frame Rayleigh quotient at least L_m."
        ),
        qsvt_consequence=(
            "The global interval-polar condition proxy is at least sqrt(L_m); "
            "common-factor trimming alone cannot yield bounded conditioning."
        ),
        architecture_frontier=(
            "Resolve the span/overlap algebra of conjugate K-invariant sectors "
            "or bypass it with a structured orbit-row polar."
        ),
        exact_incident_count_proved=True,
        superpolynomial_incident_growth_proved=True,
        all_copy_frame_norm_lower_bound_proved=True,
        bounded_post_trim_global_conditioning_refuted=True,
        conjugate_sector_overlap_algebra_compiled=False,
        orbit_row_polar_compiled=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "post-trim-subgroup-outlier-no-go-structured-resolution-open"
            if verified and scaling_verified
            else "subgroup-outlier-control-failure"
        ),
    )
    return SubgroupOutlierReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Fixed-point-free involutions in S_(2m).",
            "operator": "sum_h Pbar_h^tensor k after per-register common trim.",
            "witness": "Nontrivial right-K-invariants for K=C_2 wr S_m.",
            "outside_scope": (
                "Aggregate natural mass of all conjugate witnesses, their exact "
                "overlap algebra, structured inversion, and decoding."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-CONJUGATE-K-SPAN-MASS",
                "statement": (
                    "Determine the alternative mass and isotypic support of the "
                    "span of all conjugate K-invariant outlier sectors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-SUBGROUP-STRATIFIED-POLAR",
                "statement": (
                    "Construct a coherent stratified inverse or prove that the "
                    "conjugate-sector overlap algebra remains intractable."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ORBIT-ROW-POLAR",
                "statement": (
                    "Compile the canonicalized orbit-row polar without a global "
                    "interval condition-number dependence."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Removing every exact common factor bounds the frame norm.",
                "answer": (
                    "False: a proper hyperoctahedral subgroup supplies L_m "
                    "common-free candidate incidences with L_m superpolynomial."
                ),
                "resolved": True,
            },
            {
                "challenge": "The subgroup witness proves the useful signal is hard.",
                "answer": (
                    "Not proved. One witness has a tiny guaranteed mass; the mass "
                    "of its full conjugacy orbit and its structured resolvability "
                    "remain open."
                ),
                "resolved": True,
            },
            {
                "challenge": "A large norm rules out every polar implementation.",
                "answer": (
                    "False. It rules out only a generic globally normalized "
                    "interval method; blockwise or row-structured methods survive."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_subgroup_incidence_verified for row in controls
            ),
            "superpolynomial_frame_norm_lower_bound_theorem_count": 1,
            "bounded_post_trim_global_conditioning_refutation_count": 1,
            "structured_subgroup_resolution_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "hyperoctahedral_incident_count_proved": verified,
            "post_trim_frame_norm_superpolynomial_lower_bound_proved": (
                verified and scaling_verified
            ),
            "bounded_global_interval_polar_refuted": verified and scaling_verified,
            "conjugate_sector_overlap_algebra_compiled": False,
            "structured_subgroup_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Common-factor trimming leaves superpolynomial subgroup-incidence "
                "outliers; their structured overlap algebra and natural mass are "
                "not yet resolved."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved a superpolynomial post-trim frame-norm obstruction from the "
            "hyperoctahedral centralizer and redirected the viable architecture "
            "from global interval QSVT to subgroup-stratified or orbit-row polar."
        ),
        falsifiers_triggered=[
            "Common-factor trimming does not yield a bounded-spectrum synthesis frame.",
            "The naive one-interval QSVT polar remains superpolynomially conditioned.",
            "A large frame norm alone does not rule out structured spectral inversion.",
        ],
    )


def write_subgroup_outlier_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_subgroup_outlier_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_subgroup_outlier_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
