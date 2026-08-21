"""Postselection lower bound for class-uniform commutator signal.

The class-uniform commutator moment module proves

    E_{rho~Plancherel} A_rho = (1/p(n)) sum_C 1/|C|.

The elementary ``min |C|`` bound only gives ``O(n^-2)``.  Here the entire
reciprocal-class sum is bounded uniformly.  Write a conjugacy type as
``1^(n-m) mu``, where ``mu`` has no parts equal to one, and set

    b_m = sum_{mu partition m, 1 not in mu} z_mu.

Then

    sum_C 1/|C| = 1 + sum_{m=2}^n b_m/(n)_m.

Exact checks give ``b_m<=m!/2`` for ``5<=m<=22``.  For ``m>=23``, the same
inequality follows from

    z_mu <= m^(m/2),
    p(m) < exp(pi sqrt(2m/3)),
    m! >= (m/e)^m.

Using ``b_2=2``, ``b_3=3``, ``b_4=12`` and elementary reciprocal-binomial
bounds yields, for every ``n>=5``,

    sum_C 1/|C| <= 7/4,
    E_Plancherel A_rho <= 7/(4 p(n)).

Consequently, for any source law pointwise dominated by ``kappa`` times
Plancherel and any public central filter with acceptance weights in ``[0,1]``,

    success * E[A_rho | accept] <= 7 kappa/(4 p(n)).

The same bound gains only a factor ``K`` when a filter scans ``K`` independent
labels for one high-moment sector.  The involution weak-Fourier law has
``kappa<=2``.  An explicit subset injection gives ``p(n)>=2^r`` for the largest
``r`` satisfying ``r(r+3)/2<=n``.  Thus inverse-polynomial conditional signal
and polynomially many labels force ``exp(-Omega(sqrt(n)))`` acceptance, while
generic amplitude amplification still costs ``exp(Omega(sqrt(n)))``.

This is a lower bound for label-diagonal central filtering and high-score
selection.  It does not cover a coherent transform that creates a collective
observable not reducible to retaining one source-label commutator moment.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_class_uniform_commutator_moment import (
    irrep_class_moment,
    reciprocal_class_average,
)
from symmetric_character import conjugacy_class_size


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_commutator_sector_filter_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMMUTATOR-SECTOR-FILTER-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Partition = tuple[int, ...]


@dataclass(frozen=True)
class DerangementCentralizerControl:
    moved_support_size: int
    no_fixed_point_partition_count: int | None
    exact_centralizer_sum: int | None
    half_factorial_bound: int
    exact_finite_bound_verified: bool
    analytic_log_upper_bound: float
    analytic_log_half_factorial_lower_bound: float
    analytic_tail_bound_verified: bool
    certificate_source: str
    status: str


@dataclass(frozen=True)
class ReciprocalClassSumControl:
    symmetric_group_degree: int
    conjugacy_class_count: int
    exact_reciprocal_class_sum: str
    reciprocal_class_sum: float
    exact_nonidentity_sum: str
    nonidentity_sum: float
    exact_derived_nonidentity_upper_bound: str
    derived_nonidentity_upper_bound: float
    three_fourths_nonidentity_bound_verified: bool
    seven_fourths_bound_verified: bool
    exact_plancherel_moment_average: str
    exact_plancherel_average_bound: str
    plancherel_average_bound_verified: bool
    status: str


@dataclass(frozen=True)
class OptimalCentralFilterControl:
    symmetric_group_degree: int
    threshold: str
    exact_optimal_plancherel_success: str
    optimal_plancherel_success: float
    exact_moment_budget_bound: str
    moment_budget_bound: float
    accepted_full_sector_count: int
    accepted_fractional_sector: Partition | None
    conditional_moment_at_optimum: float
    exact_linear_program_verified: bool
    status: str


@dataclass(frozen=True)
class SectorFilterScalingRecord:
    n_description: str
    symmetric_group_degree: int
    source_domination_factor: int
    source_label_count: int
    inverse_polynomial_signal_degree: int
    partition_count: int
    subset_injection_exponent: int
    partition_injection_bound_verified: bool
    log2_filter_success_upper_bound: float
    filter_success_upper_bound_below_one: bool
    log2_amplitude_amplification_cost_lower_bound: float
    polynomial_filter_success_ruled_out_at_finite_scale: bool
    status: str


@dataclass(frozen=True)
class CommutatorSectorFilterTheorem:
    derangement_centralizer_formula: str
    derangement_centralizer_bound: str
    reciprocal_class_sum_bound: str
    plancherel_moment_bound: str
    dominated_source_filter_tradeoff: str
    polynomial_label_extension: str
    involution_weak_fourier_domination: str
    partition_injection_lower_bound: str
    asymptotic_consequence: str
    architecture_scope: str
    all_n_from_degree_five: bool
    generic_amplitude_amplification_escape: bool
    coherent_collective_escape_ruled_out: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CommutatorSectorFilterNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    centralizer_controls: list[DerangementCentralizerControl]
    reciprocal_class_controls: list[ReciprocalClassSumControl]
    optimal_filter_controls: list[OptimalCentralFilterControl]
    scaling_records: list[SectorFilterScalingRecord]
    theorem: CommutatorSectorFilterTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def cycle_centralizer_size(cycle_type: Partition) -> int:
    multiplicities: dict[int, int] = {}
    for part in cycle_type:
        multiplicities[part] = multiplicities.get(part, 0) + 1
    return math.prod(
        length**count * math.factorial(count)
        for length, count in multiplicities.items()
    )


@lru_cache(maxsize=None)
def derangement_centralizer_sum(moved_support_size: int) -> int:
    if moved_support_size < 2:
        return 0
    return sum(
        cycle_centralizer_size(row)
        for row in integer_partitions(moved_support_size)
        if 1 not in row
    )


def _analytic_derangement_log_upper(moved_support_size: int) -> float:
    m = moved_support_size
    return math.pi * math.sqrt(2.0 * m / 3.0) + 0.5 * m * math.log(m)


def _analytic_half_factorial_log_lower(moved_support_size: int) -> float:
    m = moved_support_size
    return m * (math.log(m) - 1.0) - math.log(2.0)


def derangement_centralizer_control(
    moved_support_size: int,
) -> DerangementCentralizerControl:
    if moved_support_size < 5:
        raise ValueError("half-factorial control starts at moved support five")
    half_factorial = math.factorial(moved_support_size) // 2
    analytic_upper = _analytic_derangement_log_upper(moved_support_size)
    analytic_lower = _analytic_half_factorial_log_lower(moved_support_size)
    analytic = moved_support_size >= 23 and analytic_upper <= analytic_lower
    if moved_support_size <= 22:
        exact_sum: int | None = derangement_centralizer_sum(moved_support_size)
        no_fixed_count: int | None = sum(
            1
            for row in integer_partitions(moved_support_size)
            if 1 not in row
        )
        exact = exact_sum <= half_factorial
    else:
        exact_sum = None
        no_fixed_count = None
        exact = analytic
    source = (
        "exact-partition-enumeration"
        if moved_support_size <= 22
        else "partition-count-centralizer-factorial-inequality"
    )
    verified = exact and (moved_support_size <= 22 or analytic)
    return DerangementCentralizerControl(
        moved_support_size=moved_support_size,
        no_fixed_point_partition_count=no_fixed_count,
        exact_centralizer_sum=exact_sum,
        half_factorial_bound=half_factorial,
        exact_finite_bound_verified=exact,
        analytic_log_upper_bound=analytic_upper,
        analytic_log_half_factorial_lower_bound=analytic_lower,
        analytic_tail_bound_verified=analytic,
        certificate_source=source,
        status=(
            "derangement-centralizer-half-factorial-bound-verified"
            if verified
            else "derangement-centralizer-bound-certificate-failure"
        ),
    )


def reciprocal_class_sum(degree: int) -> Fraction:
    if degree < 1:
        raise ValueError("degree must be positive")
    return sum(
        (
            Fraction(1, conjugacy_class_size(row))
            for row in integer_partitions(degree)
        ),
        start=Fraction(0),
    )


def nonidentity_reciprocal_upper_bound(degree: int) -> Fraction:
    """Derived bound from ``b_2,b_3,b_4`` and ``b_m<=m!/2``.

    For ``m>=5``, ``(m!/2)/(n)_m=1/(2*binom(n,m))``.  The endpoint
    binomial coefficients are one and ``n``; every remaining coefficient is
    at least ``binom(n,2)``.  This returns the resulting all-depth bound.
    """

    if degree < 5:
        raise ValueError("uniform reciprocal-class theorem starts at n=5")
    falling_two = degree * (degree - 1)
    falling_three = falling_two * (degree - 2)
    falling_four = falling_three * (degree - 3)
    small_support = (
        Fraction(2, falling_two)
        + Fraction(3, falling_three)
        + Fraction(12, falling_four)
    )
    if degree == 5:
        reciprocal_binomial_tail = Fraction(1)
    else:
        reciprocal_binomial_tail = (
            Fraction(1)
            + Fraction(1, degree)
            + Fraction(2 * max(0, degree - 6), degree * (degree - 1))
        )
    return small_support + reciprocal_binomial_tail / 2


def reciprocal_class_sum_control(degree: int) -> ReciprocalClassSumControl:
    if degree < 5:
        raise ValueError("uniform reciprocal-class theorem starts at n=5")
    class_count = len(integer_partitions(degree))
    total = reciprocal_class_sum(degree)
    nonidentity = total - 1
    derived_nonidentity = nonidentity_reciprocal_upper_bound(degree)
    plancherel = reciprocal_class_average(degree)
    total_bound = Fraction(7, 4)
    average_bound = total_bound / class_count
    return ReciprocalClassSumControl(
        symmetric_group_degree=degree,
        conjugacy_class_count=class_count,
        exact_reciprocal_class_sum=str(total),
        reciprocal_class_sum=float(total),
        exact_nonidentity_sum=str(nonidentity),
        nonidentity_sum=float(nonidentity),
        exact_derived_nonidentity_upper_bound=str(derived_nonidentity),
        derived_nonidentity_upper_bound=float(derived_nonidentity),
        three_fourths_nonidentity_bound_verified=(
            nonidentity <= derived_nonidentity <= Fraction(3, 4)
        ),
        seven_fourths_bound_verified=total <= total_bound,
        exact_plancherel_moment_average=str(plancherel),
        exact_plancherel_average_bound=str(average_bound),
        plancherel_average_bound_verified=plancherel <= average_bound,
        status=(
            "uniform-reciprocal-class-bound-verified"
            if (
                nonidentity <= derived_nonidentity <= Fraction(3, 4)
                and total <= total_bound
                and plancherel <= average_bound
            )
            else "uniform-reciprocal-class-bound-failure"
        ),
    )


def optimal_central_filter_control(
    degree: int,
    threshold: Fraction,
) -> OptimalCentralFilterControl:
    """Solve the exact label-diagonal acceptance linear program."""

    if degree < 3:
        raise ValueError("degree must be at least three")
    if not 0 < threshold <= 1:
        raise ValueError("threshold must lie in (0,1]")
    order = math.factorial(degree)
    rows: list[tuple[Fraction, Fraction, Partition]] = []
    for partition in integer_partitions(degree):
        moment = Fraction(irrep_class_moment(partition).exact_normalized_moment)
        dimension = irrep_class_moment(partition).dimension
        source_mass = Fraction(dimension * dimension, order)
        rows.append((moment, source_mass, partition))
    rows.sort(reverse=True)

    success = Fraction(0)
    weighted_moment = Fraction(0)
    surplus = Fraction(0)
    full_count = 0
    fractional: Partition | None = None
    for moment, source_mass, partition in rows:
        if moment >= threshold:
            success += source_mass
            weighted_moment += source_mass * moment
            surplus += source_mass * (moment - threshold)
            full_count += 1
            continue
        deficit = source_mass * (threshold - moment)
        if deficit <= surplus:
            success += source_mass
            weighted_moment += source_mass * moment
            surplus -= deficit
            full_count += 1
            continue
        if surplus:
            fraction = surplus / deficit
            success += source_mass * fraction
            weighted_moment += source_mass * fraction * moment
            fractional = partition
            surplus = Fraction(0)
        break

    conditional = weighted_moment / success if success else Fraction(0)
    budget = Fraction(7, 4 * len(integer_partitions(degree))) / threshold
    verified = conditional >= threshold and success <= budget
    return OptimalCentralFilterControl(
        symmetric_group_degree=degree,
        threshold=str(threshold),
        exact_optimal_plancherel_success=str(success),
        optimal_plancherel_success=float(success),
        exact_moment_budget_bound=str(budget),
        moment_budget_bound=float(budget),
        accepted_full_sector_count=full_count,
        accepted_fractional_sector=fractional,
        conditional_moment_at_optimum=float(conditional),
        exact_linear_program_verified=verified,
        status=(
            "optimal-central-filter-below-moment-budget"
            if verified
            else "central-filter-linear-program-certificate-failure"
        ),
    )


@lru_cache(maxsize=None)
def partition_number(degree: int) -> int:
    if degree < 0:
        return 0
    counts = [0] * (degree + 1)
    counts[0] = 1
    for part in range(1, degree + 1):
        for total in range(part, degree + 1):
            counts[total] += counts[total - part]
    return counts[degree]


def subset_partition_injection_exponent(degree: int) -> int:
    """Largest r with 2+3+...+(r+1)=r(r+3)/2 at most n."""

    if degree < 0:
        raise ValueError("degree must be nonnegative")
    return max(0, (math.isqrt(9 + 8 * degree) - 3) // 2)


def sector_filter_scaling_record(
    degree: int,
    *,
    source_domination_factor: int = 2,
    source_label_count: int = 1,
    inverse_polynomial_signal_degree: int = 1,
    n_description: str | None = None,
) -> SectorFilterScalingRecord:
    if degree < 5:
        raise ValueError("scaling theorem starts at degree five")
    if source_domination_factor < 1 or source_label_count < 1:
        raise ValueError("domination factor and label count must be positive")
    if inverse_polynomial_signal_degree < 0:
        raise ValueError("signal degree must be nonnegative")
    partitions = partition_number(degree)
    injection = subset_partition_injection_exponent(degree)
    injection_verified = partitions >= 1 << injection
    log2_bound = (
        math.log2(7.0 * source_domination_factor * source_label_count / 4.0)
        + inverse_polynomial_signal_degree * math.log2(degree)
        - math.log2(partitions)
    )
    below_one = log2_bound < 0.0
    amplification_log = max(0.0, -0.5 * log2_bound)
    return SectorFilterScalingRecord(
        n_description=n_description or str(degree),
        symmetric_group_degree=degree,
        source_domination_factor=source_domination_factor,
        source_label_count=source_label_count,
        inverse_polynomial_signal_degree=inverse_polynomial_signal_degree,
        partition_count=partitions,
        subset_injection_exponent=injection,
        partition_injection_bound_verified=injection_verified,
        log2_filter_success_upper_bound=log2_bound,
        filter_success_upper_bound_below_one=below_one,
        log2_amplitude_amplification_cost_lower_bound=amplification_log,
        polynomial_filter_success_ruled_out_at_finite_scale=below_one,
        status=(
            "stretched-exponential-filter-cost-visible"
            if below_one
            else "finite-scale-filter-bound-not-yet-subunit"
        ),
    )


def commutator_sector_filter_theorem() -> CommutatorSectorFilterTheorem:
    return CommutatorSectorFilterTheorem(
        derangement_centralizer_formula=(
            "sum_C 1/|C|=1+sum_{m=2}^n b_m/(n)_m, "
            "b_m=sum_{mu partition m, m_1(mu)=0} z_mu"
        ),
        derangement_centralizer_bound="b_m<=m!/2 for every m>=5",
        reciprocal_class_sum_bound="sum_C 1/|C|<=7/4 for every n>=5",
        plancherel_moment_bound="E_Plancherel A_rho<=7/(4p(n))",
        dominated_source_filter_tradeoff=(
            "success*E[A_rho|accept]<=7*kappa/(4p(n))"
        ),
        polynomial_label_extension=(
            "For K labels and score max_i A_{rho_i}, replace kappa by K*kappa"
        ),
        involution_weak_fourier_domination=(
            "P_h(rho)=P_Plancherel(rho)*(1+chi_rho(h)/d_rho)<=2P_Plancherel(rho)"
        ),
        partition_injection_lower_bound=(
            "p(n)>=2^r for max r with r(r+3)/2<=n"
        ),
        asymptotic_consequence=(
            "Polynomial K,kappa,1/tau imply exp(-Omega(sqrt(n))) acceptance; "
            "generic amplitude amplification costs exp(Omega(sqrt(n)))."
        ),
        architecture_scope=(
            "Public label-diagonal central filters selecting one high-moment "
            "source sector; new collective observables are outside scope."
        ),
        all_n_from_degree_five=True,
        generic_amplitude_amplification_escape=False,
        coherent_collective_escape_ruled_out=False,
        theorem_verified=True,
        status="central-sector-postselection-stretched-exponential-no-go",
    )


def run_commutator_sector_filter_no_go() -> CommutatorSectorFilterNoGoReport:
    centralizers = [
        derangement_centralizer_control(moved) for moved in range(5, 31)
    ]
    reciprocal = [
        reciprocal_class_sum_control(degree) for degree in range(5, 41)
    ]
    optimal = [
        optimal_central_filter_control(degree, Fraction(1, degree))
        for degree in range(5, 19)
    ]
    scaling = [
        sector_filter_scaling_record(
            degree,
            source_domination_factor=2,
            source_label_count=degree * degree,
            inverse_polynomial_signal_degree=1,
            n_description=f"n={degree}, K=n^2 weak-Fourier labels, tau=1/n",
        )
        for degree in (20, 50, 100, 200, 500, 1000, 2000)
    ]
    theorem = commutator_sector_filter_theorem()
    centralizer_verified = all(
        row.exact_finite_bound_verified
        and (
            row.moved_support_size <= 22
            or row.analytic_tail_bound_verified
        )
        for row in centralizers
    )
    reciprocal_verified = all(
        row.three_fourths_nonidentity_bound_verified
        and
        row.seven_fourths_bound_verified
        and row.plancherel_average_bound_verified
        for row in reciprocal
    )
    optimal_verified = all(row.exact_linear_program_verified for row in optimal)
    exact = theorem.theorem_verified and centralizer_verified and reciprocal_verified
    return CommutatorSectorFilterNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "kappa-dominated Plancherel label law",
            "filter": "public central acceptance weights 0<=w_rho<=1",
            "score": "class-uniform commutator moment A_rho",
            "tradeoff": theorem.dominated_source_filter_tradeoff,
            "scope": theorem.architecture_scope,
        },
        centralizer_controls=centralizers,
        reciprocal_class_controls=reciprocal,
        optimal_filter_controls=optimal,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "uniformly_bound_reciprocal_class_sum",
                "resolved": True,
                "resolution": (
                    "Moved-support decomposition, exact m<=22 controls, and the "
                    "partition/centralizer/factorial tail prove the 7/4 bound."
                ),
            },
            {
                "obligation": "charge_arbitrary_central_acceptance_weights",
                "resolved": True,
                "resolution": (
                    "Since 0<=w<=1, accepted unnormalized score is at most the "
                    "source expectation; division by success gives the tradeoff."
                ),
            },
            {
                "obligation": "cover_involution_weak_fourier_sources",
                "resolved": True,
                "resolution": (
                    "The normalized character ratio lies in [-1,1], giving "
                    "pointwise domination factor kappa=2."
                ),
            },
            {
                "obligation": "exclude_generic_amplitude_amplification",
                "resolved": True,
                "resolution": (
                    "The subset injection proves p(n)>=2^Omega(sqrt(n)); the "
                    "square root of the reciprocal acceptance is still superpolynomial."
                ),
            },
            {
                "obligation": "exclude_new_collective_noncentral_observable",
                "resolved": False,
                "resolution": (
                    "A coherent transform may combine typical sectors into a new "
                    "observable rather than selecting a high-A source label."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The earlier O(n^-2) average permits polynomial filtering.",
                "resolved": True,
                "resolution": (
                    "Summing reciprocal class sizes before bounding them sharpens "
                    "the average to at most 7/(4p(n))."
                ),
            },
            {
                "objection": "A soft filter can beat hard threshold postselection.",
                "resolved": True,
                "resolution": (
                    "The moment-budget inequality holds for every fractional "
                    "weight in [0,1]; exact finite linear programs audit this."
                ),
            },
            {
                "objection": "Polynomially many source labels repair the rarity.",
                "resolved": True,
                "resolution": (
                    "The maximum-score expectation gains only the union factor K, "
                    "which cannot overcome p(n)=2^Omega(sqrt(n))."
                ),
            },
            {
                "objection": "Every coherent collective strategy is a central filter.",
                "resolved": False,
                "resolution": (
                    "No. The theorem does not cover interference that builds a new "
                    "multi-sector statistic without accepting one high-score label."
                ),
            },
        ],
        headline_metrics={
            "commutator_sector_filter_no_go_theorem_count": int(exact),
            "centralizer_control_failure_count": sum(
                not (
                    row.exact_finite_bound_verified
                    and (
                        row.moved_support_size <= 22
                        or row.analytic_tail_bound_verified
                    )
                )
                for row in centralizers
            ),
            "reciprocal_class_control_failure_count": sum(
                not (
                    row.seven_fourths_bound_verified
                    and row.three_fourths_nonidentity_bound_verified
                    and row.plancherel_average_bound_verified
                )
                for row in reciprocal
            ),
            "optimal_filter_control_failure_count": sum(
                not row.exact_linear_program_verified for row in optimal
            ),
            "maximum_exact_reciprocal_class_sum": max(
                row.reciprocal_class_sum for row in reciprocal
            ),
            "largest_scaling_degree": scaling[-1].symmetric_group_degree,
            "largest_scale_log2_success_upper_bound": (
                scaling[-1].log2_filter_success_upper_bound
            ),
            "largest_scale_log2_amplification_cost_lower_bound": (
                scaling[-1].log2_amplitude_amplification_cost_lower_bound
            ),
            "coherent_collective_escape_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "central_high_moment_postselection_viable": False,
            "polynomial_label_catalog_viable": False,
            "generic_amplitude_amplification_viable": False,
            "weak_fourier_domination_charged": True,
            "new_collective_observable_ruled_out": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Any label-diagonal route to inverse-polynomial commutator signal "
                "has stretched-exponentially small success, even after polynomial "
                "source multiplicity; a viable route must create a new collective "
                "observable on typical sectors."
            ),
        },
        status=(
            "central-commutator-sector-filter-falsified-collective-open"
            if exact and optimal_verified
            else "commutator-sector-filter-certificate-failure"
        ),
        summary=(
            "Closed central postselection onto rare commutator-sensitive sectors; "
            "only genuinely collective typical-sector interference remains open."
        ),
        falsifiers_triggered=[
            "The O(n^-2) class-size bound was far too weak for filter accounting.",
            "Soft central weights do not evade the unnormalized moment budget.",
            "Generic amplitude amplification cannot remove a partition-number cost.",
            "The theorem does not justify rejecting new collective observables.",
        ],
    )


def write_commutator_sector_filter_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMMUTATOR-SECTOR-FILTER-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_commutator_sector_filter_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_commutator_sector_filter_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
