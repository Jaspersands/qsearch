"""Fourier deflation of the hyperoctahedral subgroup-outlier orbit.

The post-common-trim frame has a superpolynomial norm witness from
``D_K=C[G/K] minus 1``, where ``K=C_2 wr S_m``.  This module determines the
entire conjugacy orbit of that witness and tests whether it carries natural
alternative mass.

For ``K_x=xKx^-1`` let ``Q_x`` project onto right ``K_x`` invariants.  Averaging
the conjugate projections and using the multiplicity-free Thrall decomposition

    Ind_K^G(1) = direct_sum_(lambda partition m) S^(2 lambda)

gives the exact operator identity

    sum_(xK in G/K) Q_x
      = direct_sum_(lambda=2 mu) (M/d_lambda) I_lambda,  (1)

on every right-regular carrier, where ``M=[G:K]=(2m-1)!!``.  After subtracting
the trivial vector, the span of all ``D_(K_x)`` is exactly the sum ``E`` of
the nontrivial even-row isotypic sectors.  A symmetric-group QFT flags ``E``
from the partition label alone.

Every subgroup-outlier tensor ``D_(K_x)^tensor k`` lies in ``E^tensor k``.
The alternative probability of this all-register event is ``w_m^k``.  If
``d=(2m)!``, ``a`` is the global common dimension, and ``r=d/2-a``, then

    w_m <= dim(E)/r
        <= M sqrt(d)/r
        = [2 M/sqrt(d)]/[1-2a/d].                       (2)

The middle inequality uses ``sum_(lambda=2mu)d_lambda=M`` and
``max d_lambda<=sqrt(d)``.  Moreover

    M/sqrt(d)=sqrt(binomial(2m,m)/4^m)<=(pi m)^(-1/4). (3)

At the orbit-flatness copy count, (2) raised to ``k`` vanishes
superpolynomially once the one-copy bound drops below one.  Thus the complete
hyperoctahedral subgroup-outlier orbit is coherently deflatable at vanishing
alternative loss.

This does not bound the frame after deflation.  Other proper subgroups can
produce their own incidence sectors, and mixed representation supports can
remain.  The result replaces one apparent global-conditioning obstruction by
a general subgroup-support stratification problem; it is not an algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import involution_class_size
from coset_hidden_involution_common_outlier_deflation import (
    expected_normal_closure_index,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_spherical_outlier_deflation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SPHERICAL-OUTLIER-DEFLATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SphericalOutlierFiniteControl:
    half_degree: int
    degree: int
    group_order: int
    matching_count: int
    even_row_sector_count: int
    even_row_dimension_sum: int
    expected_dimension_sum: int
    even_row_isotypic_dimension: int
    common_dimension: int
    trimmed_candidate_rank: int
    exact_trimmed_even_row_probability: float
    dimension_probability_upper_bound: float
    central_binomial_probability_upper_bound: float
    thrall_dimension_identity_verified: bool
    probability_bound_verified: bool
    status: str


@dataclass(frozen=True)
class SphericalOutlierScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    central_binomial_ratio: float
    one_register_spherical_mass_upper_bound: float
    all_register_spherical_mass_log2_upper_bound: float
    all_register_spherical_mass_upper_bound: float
    upper_bound_informative: bool
    conjugate_outlier_span_qft_flag_available: bool
    hyperoctahedral_outlier_orbit_removed: bool
    post_deflation_frame_norm_bounded: bool
    all_subgroup_strata_classified: bool
    status: str


@dataclass(frozen=True)
class SphericalOutlierTheorem:
    conjugate_projection_average: str
    span_support: str
    coherent_flag: str
    source_mass_bound: str
    central_binomial_bound: str
    tensor_deflation: str
    scope_limit: str
    exact_conjugate_span_proved: bool
    coherent_even_row_flag_available: bool
    vanishing_all_register_mass_proved: bool
    hyperoctahedral_outlier_orbit_deflated: bool
    all_subgroup_outliers_classified: bool
    post_deflation_frame_norm_bounded: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SphericalOutlierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SphericalOutlierFiniteControl]
    scaling_records: list[SphericalOutlierScalingRecord]
    theorem: SphericalOutlierTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def even_row_partitions(half_degree: int) -> tuple[tuple[int, ...], ...]:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return tuple(
        tuple(2 * part for part in partition)
        for partition in integer_partitions(half_degree)
    )


def _common_fraction(common_dimension: int, group_order: int) -> float:
    """Evaluate ``2a/|G|`` without converting a huge factorial to binary64."""

    return math.exp(math.log(2 * common_dimension) - math.log(group_order))


def audit_spherical_outlier_deflation(
    half_degree: int,
) -> SphericalOutlierFiniteControl:
    if half_degree < 2:
        raise ValueError("finite controls require half_degree at least two")
    degree = 2 * half_degree
    order = math.factorial(degree)
    matching_count = perfect_matching_count(half_degree)
    partitions = even_row_partitions(half_degree)
    dimensions = [hook_length_dimension(partition) for partition in partitions]
    dimension_sum = sum(dimensions)
    isotypic_dimension = sum(dimension * dimension for dimension in dimensions)
    common_dimension = expected_normal_closure_index(degree, half_degree)
    trimmed_rank = order // 2 - common_dimension
    plus_ranks = [
        (
            dimension
            + character_on_involution(partition, half_degree)
        )
        // 2
        for partition, dimension in zip(partitions, dimensions)
    ]
    # The trivial even-row sector is removed by the common-factor trim.  Sign,
    # when common, is not an even-row partition and needs no second subtraction.
    retained_trace = sum(
        dimension * plus_rank
        for dimension, plus_rank in zip(dimensions, plus_ranks)
    ) - 1
    exact_probability = retained_trace / trimmed_rank
    dimension_bound = (isotypic_dimension - 1) / trimmed_rank
    central_ratio = math.comb(degree, half_degree) / (4**half_degree)
    analytic_bound = (
        2.0 * math.sqrt(central_ratio)
        / (1.0 - _common_fraction(common_dimension, order))
    )
    thrall_verified = bool(
        dimension_sum == matching_count
        and order == matching_count * (2**half_degree) * math.factorial(half_degree)
    )
    probability_verified = bool(
        0.0 <= exact_probability <= dimension_bound <= analytic_bound + 1e-12
    )
    return SphericalOutlierFiniteControl(
        half_degree=half_degree,
        degree=degree,
        group_order=order,
        matching_count=matching_count,
        even_row_sector_count=len(partitions),
        even_row_dimension_sum=dimension_sum,
        expected_dimension_sum=matching_count,
        even_row_isotypic_dimension=isotypic_dimension,
        common_dimension=common_dimension,
        trimmed_candidate_rank=trimmed_rank,
        exact_trimmed_even_row_probability=exact_probability,
        dimension_probability_upper_bound=dimension_bound,
        central_binomial_probability_upper_bound=analytic_bound,
        thrall_dimension_identity_verified=thrall_verified,
        probability_bound_verified=probability_verified,
        status=(
            "exact-spherical-outlier-span-mass-control-verified"
            if thrall_verified and probability_verified
            else "spherical-outlier-control-failure"
        ),
    )


def spherical_outlier_scaling_record(
    half_degree: int,
) -> SphericalOutlierScalingRecord:
    if half_degree < 3:
        raise ValueError("scaling records require half_degree at least three")
    degree = 2 * half_degree
    order = math.factorial(degree)
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    common_dimension = expected_normal_closure_index(degree, half_degree)
    central_ratio = math.comb(degree, half_degree) / (4**half_degree)
    one_register_bound = (
        2.0 * math.sqrt(central_ratio)
        / (1.0 - _common_fraction(common_dimension, order))
    )
    informative = one_register_bound < 1.0
    log2_bound = (
        copies * math.log2(one_register_bound) if informative else 0.0
    )
    mass_bound = 2.0**log2_bound if log2_bound > -1074 else 0.0
    removed = informative and log2_bound < -10.0
    return SphericalOutlierScalingRecord(
        half_degree=half_degree,
        degree=degree,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        central_binomial_ratio=central_ratio,
        one_register_spherical_mass_upper_bound=one_register_bound,
        all_register_spherical_mass_log2_upper_bound=log2_bound,
        all_register_spherical_mass_upper_bound=mass_bound,
        upper_bound_informative=informative,
        conjugate_outlier_span_qft_flag_available=True,
        hyperoctahedral_outlier_orbit_removed=removed,
        post_deflation_frame_norm_bounded=False,
        all_subgroup_strata_classified=False,
        status=(
            "hyperoctahedral-outlier-orbit-negligible-deflatable-"
            "other-subgroups-open"
            if removed
            else "finite-spherical-deflation-bound-not-yet-negligible"
        ),
    )


def build_spherical_outlier_report(
    *,
    finite_half_degrees: tuple[int, ...] = (3, 4, 5),
    scaling_half_degrees: tuple[int, ...] = (8, 16, 32, 64, 128),
) -> SphericalOutlierReport:
    controls = [
        audit_spherical_outlier_deflation(m) for m in finite_half_degrees
    ]
    scaling = [
        spherical_outlier_scaling_record(m) for m in scaling_half_degrees
    ]
    verified = all(
        row.thrall_dimension_identity_verified and row.probability_bound_verified
        for row in controls
    )
    # Keep the all-record check separate from the asymptotic theorem: m=8 is
    # informative but its elementary upper bound is not yet below 2^-10.
    vanishing_verified = bool(
        scaling
        and all(row.upper_bound_informative for row in scaling)
        and scaling[-1].all_register_spherical_mass_log2_upper_bound < -100.0
    )
    theorem = SphericalOutlierTheorem(
        conjugate_projection_average=(
            "sum_(xK) Q_(xKx^-1) acts by M/d_(2mu) on each even-row "
            "right carrier and by zero off the Thrall support."
        ),
        span_support=(
            "The span of all noncommon conjugate K-invariant sectors is exactly "
            "the nontrivial even-row right-isotypic support E."
        ),
        coherent_flag="The S_(2m) QFT flags E from the partition label.",
        source_mass_bound=(
            "The one-register trimmed candidate mass in E is at most "
            "2M/sqrt((2m)!)/(1-2a/(2m)!)."
        ),
        central_binomial_bound=(
            "M/sqrt((2m)!)=sqrt(binomial(2m,m)/4^m)<=(pi m)^(-1/4)."
        ),
        tensor_deflation=(
            "Every D_(K_x)^tensor k lies in E^tensor k, whose alternative mass "
            "is bounded by the kth power of the one-register bound."
        ),
        scope_limit=(
            "Only the hyperoctahedral subgroup orbit is removed; other subgroup "
            "incidence strata and the post-deflation frame norm remain open."
        ),
        exact_conjugate_span_proved=True,
        coherent_even_row_flag_available=True,
        vanishing_all_register_mass_proved=vanishing_verified,
        hyperoctahedral_outlier_orbit_deflated=vanishing_verified,
        all_subgroup_outliers_classified=False,
        post_deflation_frame_norm_bounded=False,
        theorem_verified=verified and vanishing_verified,
        status=(
            "spherical-outlier-orbit-deflated-subgroup-hierarchy-open"
            if verified and vanishing_verified
            else "spherical-outlier-deflation-control-failure"
        ),
    )
    return SphericalOutlierReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Hyperoctahedral centralizers of perfect matchings.",
            "span": "Conjugate right-K invariant sectors in C[S_(2m)].",
            "trim": "Reject the all-register nontrivial even-row Fourier event.",
            "outside_scope": (
                "Other subgroup incidence sectors, mixed supports, final frame "
                "norm, row-polar implementation, and decoding."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-SUBGROUP-STRATA-CLASSIFICATION",
                "statement": (
                    "Classify proper subgroups containing many fixed-point-free "
                    "involutions and their induced Fourier supports."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-POST-SPHERICAL-TRIM-NORM",
                "statement": (
                    "Bound or witness the frame norm after common and all-register "
                    "even-row outlier deflation."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ORBIT-ROW-POLAR",
                "statement": (
                    "Compile the orbit-row polar on the retained natural mass."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A superpolynomial subgroup outlier kills the architecture.",
                "answer": (
                    "Not for K=C_2 wr S_m: its complete conjugacy orbit has an "
                    "even-row Fourier flag and vanishing all-register mass."
                ),
                "resolved": True,
            },
            {
                "challenge": "One small witness mass bounds the full conjugate orbit.",
                "answer": (
                    "False in general. Here the exact Thrall span identity is what "
                    "permits a uniform bound on the entire orbit."
                ),
                "resolved": True,
            },
            {
                "challenge": "Deflating even-row tensors bounds the remaining norm.",
                "answer": (
                    "Unproved. Other subgroup supports and mixed-sector incidence "
                    "can still create large eigenvalues."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.probability_bound_verified for row in controls
            ),
            "exact_conjugate_span_theorem_count": 1,
            "coherent_spherical_outlier_deflation_count": 1,
            "all_subgroup_strata_classification_count": 0,
            "post_deflation_frame_norm_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "conjugate_hyperoctahedral_span_compiled": verified,
            "spherical_outlier_orbit_negligible_and_deflatable": (
                verified and vanishing_verified
            ),
            "all_subgroup_incidence_strata_classified": False,
            "post_spherical_trim_frame_norm_bounded": False,
            "orbit_row_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The hyperoctahedral outlier orbit is removable, but no theorem "
                "controls all proper-subgroup strata or the retained frame norm."
            ),
        },
        status=theorem.status,
        summary=(
            "Identified the full hyperoctahedral outlier orbit with nontrivial "
            "even-row Fourier support and proved that its all-register natural "
            "mass vanishes at the required copy width."
        ),
        falsifiers_triggered=[
            "The hyperoctahedral norm witness is not a terminal obstruction.",
            "Its conjugate span, not one selected witness, is the correct trim target.",
            "Removing that span does not establish a bounded residual frame.",
        ],
    )


def write_spherical_outlier_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_spherical_outlier_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_spherical_outlier_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
