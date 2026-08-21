"""Exact physical-outer sampling for compressed Racah coupling experiments.

For the physical four-label marginal,

    P(alpha,beta,gamma,lambda)
      = d_alpha d_beta d_gamma d_lambda
        M(alpha,beta,gamma,lambda)/|S_n|^3,                (1)

where ``M`` is the triple Kronecker multiplicity.  The dimension identity

    sum_lambda d_lambda M(alpha,beta,gamma,lambda)
      = d_alpha d_beta d_gamma                            (2)

gives an exact sequential sampler:

1. draw ``alpha,beta,gamma`` independently from Plancherel measure;
2. draw ``lambda`` with probability
   ``d_lambda M/(d_alpha d_beta d_gamma)``.

For each sampled outer tuple, the complete compressed Racah coupling supplies
``I(mu;nu|outer)`` and fractional dependence moments.  Hoeffding intervals use
the deterministic bound ``I<=log2 p(n)``.  The sampler therefore estimates the
correct physical average without selecting favorable outer sectors.

This is finite classical evidence, not an asymptotic theorem or an efficient
quantum implementation.  Pairwise representation spaces are still exponential
for Plancherel-shaped partitions, and useful confidence can require many full
coupling compilations.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_triangle_barrier import partition_number
from self_dual_wreath_compressed_racah_coupling_probe import (
    CompleteCompressedRacahCoupling,
    compile_complete_racah_coupling,
)
from self_dual_wreath_recoupling_mutual_information_reduction import (
    audit_recoupling_mutual_information_finite,
)
from self_dual_wreath_recoupling_haar_gap_reduction import (
    orthogonal_haar_expected_chi_square,
)
from symmetric_character import kronecker_coefficient


Partition = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/self_dual_wreath_physical_outer_racah_sampling.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-OUTER-RACAH-SAMPLING"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PhysicalOuterNormalizationControl:
    n: int
    partition_count: int
    source_triple_count: int
    maximum_dimension_identity_residual: int
    minimum_positive_conditional_probability: float
    maximum_conditional_probability_sum_residual: float
    exact_sequential_sampler_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalOuterRacahSample:
    sample_index: int
    outer_partitions: tuple[Partition, Partition, Partition, Partition]
    outer_tuple_probability: float
    final_conditional_probability: float
    total_multiplicity_dimension: int
    conditional_racah_mutual_information_bits: float
    fractional_order_theta: float
    conditional_fractional_dependence_moment: float
    natural_dependence_chi_square: float
    orthogonal_haar_expected_chi_square: float
    natural_to_orthogonal_haar_chi_ratio: float
    natural_fractional_dependence_excess: float
    fractional_excess_to_theta_haar_chi_upper_ratio: float
    complete_block_count: int
    complete_coupling_verified: bool
    duplicate_outer_tuple: bool


@dataclass(frozen=True)
class PhysicalOuterRacahSamplingRecord:
    n: int
    sample_count: int
    random_seed: int
    confidence_level: float
    fractional_order_theta: float
    unique_outer_tuple_count: int
    duplicate_sample_count: int
    sample_mean_racah_mutual_information_bits: float
    sample_standard_error_bits: float
    mutual_information_hoeffding_radius_bits: float
    mutual_information_confidence_lower_bits: float
    mutual_information_confidence_upper_bits: float
    mutual_information_range_upper_bits: float
    sample_mean_fractional_dependence_moment: float
    median_natural_to_orthogonal_haar_chi_ratio: float
    maximum_natural_to_orthogonal_haar_chi_ratio: float
    positive_natural_chi_sample_count: int
    median_fractional_excess_to_theta_haar_upper_ratio: float
    maximum_fractional_excess_to_theta_haar_upper_ratio: float
    global_maximum_total_multiplicity: int
    fractional_moment_range_upper: float
    fractional_moment_hoeffding_radius: float
    exact_finite_physical_average_mi_bits: float | None
    exact_average_inside_mi_confidence_interval: bool | None
    maximum_complete_coupling_residual: float
    all_sampled_couplings_verified: bool
    asymptotic_inference_allowed: bool
    status: str
    samples: list[PhysicalOuterRacahSample]


@dataclass(frozen=True)
class PhysicalOuterRacahSamplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    normalization_controls: list[PhysicalOuterNormalizationControl]
    sampling_records: list[PhysicalOuterRacahSamplingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def plancherel_distribution(
    n: int,
) -> tuple[tuple[Partition, ...], tuple[float, ...]]:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    probabilities = tuple(
        hook_length_dimension(partition) ** 2 / order
        for partition in partitions
    )
    if not math.isclose(sum(probabilities), 1.0, rel_tol=0.0, abs_tol=1e-14):
        raise ArithmeticError("Plancherel probabilities do not normalize")
    return partitions, probabilities


@lru_cache(maxsize=None)
def triple_multiplicity(
    alpha: Partition,
    beta: Partition,
    gamma: Partition,
    final: Partition,
) -> int:
    n = sum(alpha)
    if any(sum(partition) != n for partition in (beta, gamma, final)):
        raise ValueError("partitions must have common size n")
    return sum(
        kronecker_coefficient(alpha, beta, intermediate)
        * kronecker_coefficient(intermediate, gamma, final)
        for intermediate in integer_partitions(n)
    )


@lru_cache(maxsize=None)
def conditional_final_distribution(
    alpha: Partition,
    beta: Partition,
    gamma: Partition,
) -> tuple[tuple[Partition, ...], tuple[float, ...], tuple[int, ...]]:
    n = sum(alpha)
    if sum(beta) != n or sum(gamma) != n:
        raise ValueError("source partitions must have common size n")
    partitions = tuple(integer_partitions(n))
    denominator = (
        hook_length_dimension(alpha)
        * hook_length_dimension(beta)
        * hook_length_dimension(gamma)
    )
    multiplicities = tuple(
        triple_multiplicity(alpha, beta, gamma, final)
        for final in partitions
    )
    numerators = tuple(
        hook_length_dimension(final) * multiplicity
        for final, multiplicity in zip(partitions, multiplicities)
    )
    if sum(numerators) != denominator:
        raise ArithmeticError("triple tensor dimension identity failed")
    probabilities = tuple(numerator / denominator for numerator in numerators)
    return partitions, probabilities, multiplicities


def audit_physical_outer_sampler_normalization(
    n: int,
    *,
    tolerance: float = 1e-14,
) -> PhysicalOuterNormalizationControl:
    partitions, _plancherel = plancherel_distribution(n)
    maximum_identity_residual = 0
    maximum_probability_residual = 0.0
    positive_probabilities: list[float] = []
    for alpha in partitions:
        for beta in partitions:
            for gamma in partitions:
                finals, probabilities, multiplicities = conditional_final_distribution(
                    alpha,
                    beta,
                    gamma,
                )
                denominator = (
                    hook_length_dimension(alpha)
                    * hook_length_dimension(beta)
                    * hook_length_dimension(gamma)
                )
                observed = sum(
                    hook_length_dimension(final) * multiplicity
                    for final, multiplicity in zip(finals, multiplicities)
                )
                maximum_identity_residual = max(
                    maximum_identity_residual,
                    abs(observed - denominator),
                )
                maximum_probability_residual = max(
                    maximum_probability_residual,
                    abs(sum(probabilities) - 1.0),
                )
                positive_probabilities.extend(
                    probability for probability in probabilities if probability > 0
                )
    exact = bool(
        maximum_identity_residual == 0
        and maximum_probability_residual <= tolerance
    )
    return PhysicalOuterNormalizationControl(
        n=n,
        partition_count=len(partitions),
        source_triple_count=len(partitions) ** 3,
        maximum_dimension_identity_residual=maximum_identity_residual,
        minimum_positive_conditional_probability=min(positive_probabilities),
        maximum_conditional_probability_sum_residual=maximum_probability_residual,
        exact_sequential_sampler_verified=exact,
        status=(
            "physical-outer-sequential-sampler-exactly-normalized"
            if exact
            else "physical-outer-sampler-normalization-failure"
        ),
    )


@lru_cache(maxsize=None)
def maximum_total_multiplicity(n: int) -> int:
    partitions = tuple(integer_partitions(n))
    return max(
        triple_multiplicity(alpha, beta, gamma, final)
        for alpha in partitions
        for beta in partitions
        for gamma in partitions
        for final in partitions
    )


def sample_physical_outer_racah_couplings(
    n: int,
    sample_count: int,
    *,
    random_seed: int = 1729,
    confidence_level: float = 0.95,
    fractional_order_theta: float = 0.5,
) -> PhysicalOuterRacahSamplingRecord:
    if sample_count < 1 or not 0 < confidence_level < 1:
        raise ValueError("positive sample count and confidence in (0,1) are required")
    if not 0 < fractional_order_theta <= 1:
        raise ValueError("fractional order theta must lie in (0,1]")
    partitions, plancherel = plancherel_distribution(n)
    rng = np.random.default_rng(random_seed)
    cache: dict[
        tuple[Partition, Partition, Partition, Partition],
        CompleteCompressedRacahCoupling,
    ] = {}
    samples: list[PhysicalOuterRacahSample] = []
    residuals: list[float] = []
    for sample_index in range(sample_count):
        source_indices = rng.choice(
            len(partitions),
            size=3,
            replace=True,
            p=plancherel,
        )
        alpha, beta, gamma = (
            partitions[int(index)] for index in source_indices
        )
        finals, final_probabilities, multiplicities = conditional_final_distribution(
            alpha,
            beta,
            gamma,
        )
        final_index = int(
            rng.choice(len(finals), p=final_probabilities)
        )
        final = finals[final_index]
        outer = (alpha, beta, gamma, final)
        duplicate = outer in cache
        if not duplicate:
            cache[outer] = compile_complete_racah_coupling(outer)
        coupling = cache[outer]
        moment = sum(
            entry.physical_block_probability
            * entry.relative_block_overlap**fractional_order_theta
            for entry in coupling.coupling_entries
            if entry.physical_block_probability > 0
        )
        outer_probability = (
            hook_length_dimension(alpha)
            * hook_length_dimension(beta)
            * hook_length_dimension(gamma)
            * hook_length_dimension(final)
            * multiplicities[final_index]
            / math.factorial(n) ** 3
        )
        natural_chi = max(0.0, coupling.dependence_collision_moment - 1.0)
        haar_chi = orthogonal_haar_expected_chi_square(
            coupling.total_multiplicity_dimension,
            coupling.left_channel_count,
            coupling.right_channel_count,
        )
        enhancement = natural_chi / haar_chi if haar_chi > 0 else 0.0
        fractional_excess = max(0.0, moment - 1.0)
        fractional_enhancement = (
            fractional_excess / (fractional_order_theta * haar_chi)
            if haar_chi > 0
            else 0.0
        )
        residuals.extend(
            (
                coupling.total_block_mass_residual,
                coupling.maximum_left_rank_marginal_residual,
                coupling.maximum_right_rank_marginal_residual,
                coupling.maximum_pair_embedding_isometry_residual,
            )
        )
        samples.append(
            PhysicalOuterRacahSample(
                sample_index=sample_index,
                outer_partitions=outer,
                outer_tuple_probability=outer_probability,
                final_conditional_probability=final_probabilities[final_index],
                total_multiplicity_dimension=coupling.total_multiplicity_dimension,
                conditional_racah_mutual_information_bits=(
                    coupling.conditional_racah_mutual_information_bits
                ),
                fractional_order_theta=fractional_order_theta,
                conditional_fractional_dependence_moment=moment,
                natural_dependence_chi_square=natural_chi,
                orthogonal_haar_expected_chi_square=haar_chi,
                natural_to_orthogonal_haar_chi_ratio=enhancement,
                natural_fractional_dependence_excess=fractional_excess,
                fractional_excess_to_theta_haar_chi_upper_ratio=(
                    fractional_enhancement
                ),
                complete_block_count=coupling.block_count,
                complete_coupling_verified=coupling.exact_complete_coupling_verified,
                duplicate_outer_tuple=duplicate,
            )
        )

    information = np.asarray(
        [sample.conditional_racah_mutual_information_bits for sample in samples]
    )
    moments = np.asarray(
        [sample.conditional_fractional_dependence_moment for sample in samples]
    )
    enhancements = np.asarray(
        [sample.natural_to_orthogonal_haar_chi_ratio for sample in samples]
    )
    fractional_enhancements = np.asarray(
        [
            sample.fractional_excess_to_theta_haar_chi_upper_ratio
            for sample in samples
        ]
    )
    mean_information = float(np.mean(information))
    standard_error = float(np.std(information, ddof=1) / math.sqrt(sample_count)) if sample_count > 1 else 0.0
    failure_probability = 1.0 - confidence_level
    information_upper = math.log2(partition_number(n))
    information_radius = information_upper * math.sqrt(
        math.log(2.0 / failure_probability) / (2.0 * sample_count)
    )
    maximum_multiplicity = maximum_total_multiplicity(n)
    moment_range_upper = maximum_multiplicity**fractional_order_theta
    moment_radius = (moment_range_upper - 1.0) * math.sqrt(
        math.log(2.0 / failure_probability) / (2.0 * sample_count)
    )
    exact_average = (
        audit_recoupling_mutual_information_finite(n)
        .physical_average_recoupling_mutual_information_bits
        if n <= 5
        else None
    )
    confidence_lower = max(0.0, mean_information - information_radius)
    confidence_upper = min(
        information_upper,
        mean_information + information_radius,
    )
    exact_inside = (
        confidence_lower <= exact_average <= confidence_upper
        if exact_average is not None
        else None
    )
    all_verified = all(sample.complete_coupling_verified for sample in samples)
    maximum_residual = max(residuals, default=0.0)
    return PhysicalOuterRacahSamplingRecord(
        n=n,
        sample_count=sample_count,
        random_seed=random_seed,
        confidence_level=confidence_level,
        fractional_order_theta=fractional_order_theta,
        unique_outer_tuple_count=len(cache),
        duplicate_sample_count=sum(sample.duplicate_outer_tuple for sample in samples),
        sample_mean_racah_mutual_information_bits=mean_information,
        sample_standard_error_bits=standard_error,
        mutual_information_hoeffding_radius_bits=information_radius,
        mutual_information_confidence_lower_bits=confidence_lower,
        mutual_information_confidence_upper_bits=confidence_upper,
        mutual_information_range_upper_bits=information_upper,
        sample_mean_fractional_dependence_moment=float(np.mean(moments)),
        median_natural_to_orthogonal_haar_chi_ratio=float(np.median(enhancements)),
        maximum_natural_to_orthogonal_haar_chi_ratio=float(np.max(enhancements)),
        positive_natural_chi_sample_count=sum(
            sample.natural_dependence_chi_square > 1e-12 for sample in samples
        ),
        median_fractional_excess_to_theta_haar_upper_ratio=float(
            np.median(fractional_enhancements)
        ),
        maximum_fractional_excess_to_theta_haar_upper_ratio=float(
            np.max(fractional_enhancements)
        ),
        global_maximum_total_multiplicity=maximum_multiplicity,
        fractional_moment_range_upper=moment_range_upper,
        fractional_moment_hoeffding_radius=moment_radius,
        exact_finite_physical_average_mi_bits=exact_average,
        exact_average_inside_mi_confidence_interval=exact_inside,
        maximum_complete_coupling_residual=maximum_residual,
        all_sampled_couplings_verified=all_verified,
        asymptotic_inference_allowed=False,
        status=(
            "physical-outer-racah-monte-carlo-complete-couplings-verified"
            if all_verified and (exact_inside is not False)
            else "physical-outer-racah-sampling-control-failure"
        ),
        samples=samples,
    )


def build_physical_outer_racah_sampling_report(
    n5_sample_count: int = 24,
    n6_sample_count: int = 12,
) -> PhysicalOuterRacahSamplingReport:
    normalizations = [
        audit_physical_outer_sampler_normalization(n) for n in (3, 4, 5, 6)
    ]
    records = [
        sample_physical_outer_racah_couplings(
            5,
            n5_sample_count,
            random_seed=20260813,
        ),
        sample_physical_outer_racah_couplings(
            6,
            n6_sample_count,
            random_seed=20260814,
        ),
    ]
    failures = sum(not row.exact_sequential_sampler_verified for row in normalizations)
    failures += sum(
        not row.all_sampled_couplings_verified
        or row.exact_average_inside_mi_confidence_interval is False
        for row in records
    )
    verified = failures == 0
    n6 = next(row for row in records if row.n == 6)
    return PhysicalOuterRacahSamplingReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_outer_law": (
                "P_outer=d_alpha d_beta d_gamma d_lambda M/|S_n|^3"
            ),
            "sequential_sampler": (
                "alpha,beta,gamma iid Plancherel; lambda conditional proportional to d_lambda M"
            ),
            "normalization_identity": (
                "sum_lambda d_lambda M=d_alpha d_beta d_gamma"
            ),
            "estimated_quantity": "E_(P_outer) I_pi(mu;nu|outer)",
            "nonhaar_target": (
                "(S_1(outer)-1)/E_Haar[S_1(outer)-1] for every sampled outer tuple"
            ),
            "rigorous_mi_range": "0<=I<=log2 p(n)",
            "confidence_method": "two-sided Hoeffding interval",
            "scope": (
                "finite classical Monte Carlo with exact conditional couplings; "
                "no asymptotic extrapolation"
            ),
        },
        normalization_controls=normalizations,
        sampling_records=records,
        proof_obligations=[
            {
                "obligation": "derive_and_validate_exact_physical_outer_sampler",
                "resolved": verified,
                "resolution": (
                    "The triple tensor dimension identity normalizes every conditional final-label law through S6."
                ),
            },
            {
                "obligation": "remove_selected_outer_sector_bias",
                "resolved": verified,
                "resolution": (
                    "Outer tuples are sampled from the exact physical marginal before their coupling is compiled."
                ),
            },
            {
                "obligation": "obtain_asymptotically_decisive_confidence",
                "resolved": False,
                "resolution": (
                    "Finite S6 intervals and an exponential representation cost cannot prove an all-n rate."
                ),
            },
            {
                "obligation": "importance_sample_fractional_moment_tails",
                "resolved": False,
                "resolution": (
                    "Worst-case multiplicity makes the current fractional-moment Hoeffding radius broad."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Uniformly sampling four partitions estimates the physical law.",
                "resolved": True,
                "resolution": (
                    "It does not; equation (1) requires Plancherel source weights and multiplicity-biased final labels."
                ),
            },
            {
                "objection": "A low sample mean is sufficient evidence of decay.",
                "resolved": True,
                "resolution": (
                    "The report includes a support-size Hoeffding radius and forbids asymptotic inference."
                ),
            },
            {
                "objection": "Mutual-information confidence also controls fractional moments.",
                "resolved": True,
                "resolution": (
                    "Fractional moments have a larger multiplicity-dependent range and receive a separate radius."
                ),
            },
            {
                "objection": "Classical compilation of the statistic demonstrates a quantum primitive.",
                "resolved": True,
                "resolution": (
                    "It is a dephased diagnostic only and supplies no coherent associator or decoder."
                ),
            },
        ],
        headline_metrics={
            "exact_outer_sampler_normalization_count": len(normalizations),
            "physical_outer_sampling_run_count": len(records),
            "total_complete_coupling_sample_count": sum(row.sample_count for row in records),
            "sampling_control_failure_count": failures,
            "n6_sample_count": n6.sample_count,
            "n6_sample_mean_racah_mi_bits": n6.sample_mean_racah_mutual_information_bits,
            "n6_mi_hoeffding_radius_bits": n6.mutual_information_hoeffding_radius_bits,
            "n6_median_natural_to_haar_chi_ratio": (
                n6.median_natural_to_orthogonal_haar_chi_ratio
            ),
            "n6_maximum_natural_to_haar_chi_ratio": (
                n6.maximum_natural_to_orthogonal_haar_chi_ratio
            ),
            "n6_median_fractional_excess_to_theta_haar_upper_ratio": (
                n6.median_fractional_excess_to_theta_haar_upper_ratio
            ),
            "n6_maximum_fractional_excess_to_theta_haar_upper_ratio": (
                n6.maximum_fractional_excess_to_theta_haar_upper_ratio
            ),
            "asymptotically_decisive_sampling_run_count": 0,
            "natural_racah_mi_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_physical_outer_sampler_verified": verified,
            "sampled_complete_couplings_verified": verified,
            "selected_outer_bias_removed_for_finite_runs": verified,
            "finite_n6_interval_is_asymptotic_evidence": False,
            "physical_average_racah_mi_sublogarithmic_proved": False,
            "coherent_racah_transform_polynomial_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The finite estimator now targets the correct physical average, but its "
                "confidence and representation cost do not establish a growing-n theorem."
            ),
        },
        status=(
            "physical-outer-racah-sampler-verified-asymptotic-rate-open"
            if verified
            else "physical-outer-racah-sampling-control-failure"
        ),
        summary=(
            "Replaced selected-sector Racah diagnostics by exact physical-law outer sampling with complete couplings."
        ),
        falsifiers_triggered=[
            "Uniform partition sampling is not the physical outer-label law.",
            "A favorable maximal-dimension sector does not estimate the physical average.",
            "Finite low means without confidence radii are not evidence of asymptotic delocalization.",
        ],
    )


def write_physical_outer_racah_sampling_report(
    path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_physical_outer_racah_sampling_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_physical_outer_racah_sampling_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
