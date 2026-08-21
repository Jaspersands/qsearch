"""Exact physical-law sampling of irreducible orientation-syndrome Racah CMI.

The full six-label physical law factors as

    P_outer(alpha,beta,gamma,lambda)
      =d_alpha d_beta d_gamma d_lambda M / |S_n|^3,

    pi_o(mu,nu)=x_(mu,nu)/M.                              (1)

Sampling three Plancherel source labels, then the final label with probability
``d_lambda M/(d_alpha d_beta d_gamma)``, and finally one complete Racah block
with probability ``x/M`` therefore samples the exact physical six-label law.

Map every non-self-conjugate sampled label to its canonical transpose-pair
representative.  For a fully paired tuple above a dimension trim, compile its
eight orientation syndrome blocks and record

    Z=I(Y_g;Y_h|Y_k) in [0,1].                            (2)

Set ``Z=0`` outside the retained paired event.  Then the sample mean is an
unbiased estimate of the retained physical-average irreducible Racah CMI, and
Hoeffding gives a rigorous confidence interval without extrapolating in ``n``.

This estimator is exact but remains exponential representation-space work.
It estimates measured-label information, not coherent accessibility or a
classical complexity separation.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_compressed_orientation_racah_cumulant_probe import (
    CompressedOrientationRacahControl,
    compile_orientation_racah_channel,
)
from self_dual_wreath_compressed_racah_coupling_probe import (
    CompleteCompressedRacahCoupling,
    compile_complete_racah_coupling,
)
from self_dual_wreath_parity_racah_information_projection import (
    audit_information_projection_aggregate,
)
from self_dual_wreath_physical_outer_racah_sampling import (
    conditional_final_distribution,
    plancherel_distribution,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import transpose_partition


Partition = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_physical_orientation_racah_sampling.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-RACAH-SAMPLING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PhysicalOrientationRacahSample:
    sample_index: int
    six_partitions: tuple[Partition, ...]
    base_sign_orbit_partitions: tuple[Partition, ...] | None
    all_labels_nonself_conjugate: bool
    all_label_dimensions_above_trim: bool
    retained_paired_event: bool
    sampled_outer_tuple_probability: float
    sampled_block_conditional_probability: float
    orientation_irreducible_cmi_bits: float
    retained_cmi_contribution_bits: float
    duplicate_outer_tuple: bool
    duplicate_sign_orbit_tuple: bool
    complete_coupling_verified: bool
    orientation_channel_verified: bool | None
    status: str


@dataclass(frozen=True)
class PhysicalOrientationRacahSamplingRecord:
    n: int
    sample_count: int
    random_seed: int
    minimum_dimension_exclusive: int
    confidence_level: float
    retained_paired_sample_count: int
    unpaired_or_trimmed_sample_count: int
    unique_outer_tuple_count: int
    unique_retained_sign_orbit_tuple_count: int
    sample_mean_retained_physical_cmi_bits: float
    sample_standard_error_bits: float
    cmi_hoeffding_radius_bits: float
    cmi_confidence_lower_bits: float
    cmi_confidence_upper_bits: float
    sample_retained_paired_mass: float
    paired_mass_hoeffding_radius: float
    conditional_mean_cmi_on_retained_samples_bits: float
    exact_finite_retained_physical_cmi_bits: float | None
    exact_finite_retained_physical_mass: float | None
    exact_cmi_inside_confidence_interval: bool | None
    exact_mass_inside_confidence_interval: bool | None
    maximum_complete_coupling_residual: float
    maximum_orientation_isometry_residual: float
    all_compiled_objects_verified: bool
    asymptotic_inference_allowed: bool
    status: str
    samples: list[PhysicalOrientationRacahSample]


@dataclass(frozen=True)
class PhysicalOrientationRacahSamplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    records: list[PhysicalOrientationRacahSamplingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def canonical_sign_orbit_tuple(
    labels: tuple[Partition, ...],
    minimum_dimension_exclusive: int,
) -> tuple[tuple[Partition, ...] | None, bool, bool]:
    if len(labels) != 6:
        raise ValueError("six labels are required")
    base: list[Partition] = []
    nonself = True
    above_trim = True
    for label in labels:
        partner = transpose_partition(label)
        if partner == label:
            nonself = False
        if hook_length_dimension(label) <= minimum_dimension_exclusive:
            above_trim = False
        base.append(min(label, partner))
    return (tuple(base) if nonself and above_trim else None, nonself, above_trim)


def sample_physical_orientation_racah_cmi(
    n: int,
    sample_count: int,
    *,
    random_seed: int = 271828,
    minimum_dimension_exclusive: int = 1,
    confidence_level: float = 0.95,
) -> PhysicalOrientationRacahSamplingRecord:
    if sample_count < 1:
        raise ValueError("positive sample count is required")
    if minimum_dimension_exclusive < 0:
        raise ValueError("dimension trim must be nonnegative")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence level must lie in (0,1)")
    partitions, plancherel = plancherel_distribution(n)
    rng = np.random.default_rng(random_seed)
    outer_cache: dict[
        tuple[Partition, Partition, Partition, Partition],
        CompleteCompressedRacahCoupling,
    ] = {}
    orbit_cache: dict[
        tuple[Partition, ...],
        CompressedOrientationRacahControl,
    ] = {}
    samples: list[PhysicalOrientationRacahSample] = []
    coupling_residuals: list[float] = []
    orientation_residuals: list[float] = []
    contributions: list[float] = []
    retained_indicators: list[float] = []
    for sample_index in range(sample_count):
        source_indices = rng.choice(
            len(partitions), size=3, replace=True, p=plancherel
        )
        alpha, beta, gamma = tuple(
            partitions[int(index)] for index in source_indices
        )
        finals, final_probabilities, multiplicities = conditional_final_distribution(
            alpha, beta, gamma
        )
        final_index = int(rng.choice(len(finals), p=final_probabilities))
        final = finals[final_index]
        outer = (alpha, beta, gamma, final)
        duplicate_outer = outer in outer_cache
        if not duplicate_outer:
            outer_cache[outer] = compile_complete_racah_coupling(outer)
        coupling = outer_cache[outer]
        entry_probabilities = np.asarray(
            [entry.physical_block_probability for entry in coupling.coupling_entries],
            dtype=float,
        )
        entry_probabilities /= float(np.sum(entry_probabilities))
        entry_index = int(
            rng.choice(len(coupling.coupling_entries), p=entry_probabilities)
        )
        entry = coupling.coupling_entries[entry_index]
        labels = (
            alpha,
            beta,
            gamma,
            entry.left_intermediate_partition,
            entry.right_intermediate_partition,
            final,
        )
        base, nonself, above_trim = canonical_sign_orbit_tuple(
            labels, minimum_dimension_exclusive
        )
        retained = base is not None
        duplicate_orbit = bool(retained and base in orbit_cache)
        orientation: CompressedOrientationRacahControl | None = None
        if retained and base is not None:
            if not duplicate_orbit:
                orbit_cache[base] = compile_orientation_racah_channel(
                    f"SAMPLED-S{n}-{len(orbit_cache)}", base
                )
            orientation = orbit_cache[base]
            cmi = orientation.irreducible_racah_cmi_bits
            contribution = cmi
            orientation_residuals.append(
                orientation.maximum_pair_embedding_isometry_residual
            )
        else:
            cmi = 0.0
            contribution = 0.0
        outer_probability = (
            hook_length_dimension(alpha)
            * hook_length_dimension(beta)
            * hook_length_dimension(gamma)
            * hook_length_dimension(final)
            * multiplicities[final_index]
            / math.factorial(n) ** 3
        )
        coupling_residuals.extend(
            (
                coupling.total_block_mass_residual,
                coupling.maximum_left_rank_marginal_residual,
                coupling.maximum_right_rank_marginal_residual,
                coupling.maximum_pair_embedding_isometry_residual,
            )
        )
        contributions.append(contribution)
        retained_indicators.append(float(retained))
        samples.append(
            PhysicalOrientationRacahSample(
                sample_index=sample_index,
                six_partitions=labels,
                base_sign_orbit_partitions=base,
                all_labels_nonself_conjugate=nonself,
                all_label_dimensions_above_trim=above_trim,
                retained_paired_event=retained,
                sampled_outer_tuple_probability=outer_probability,
                sampled_block_conditional_probability=float(
                    entry_probabilities[entry_index]
                ),
                orientation_irreducible_cmi_bits=cmi,
                retained_cmi_contribution_bits=contribution,
                duplicate_outer_tuple=duplicate_outer,
                duplicate_sign_orbit_tuple=duplicate_orbit,
                complete_coupling_verified=coupling.exact_complete_coupling_verified,
                orientation_channel_verified=(
                    orientation.compressed_orientation_channel_verified
                    if orientation is not None
                    else None
                ),
                status=(
                    "retained-physical-orientation-cmi-sample"
                    if retained
                    else "physical-sample-outside-retained-paired-sector"
                ),
            )
        )
    mean = float(np.mean(contributions))
    standard_error = (
        float(np.std(contributions, ddof=1) / math.sqrt(sample_count))
        if sample_count > 1
        else 0.0
    )
    delta = 1.0 - confidence_level
    radius = math.sqrt(math.log(2.0 / delta) / (2.0 * sample_count))
    retained_mass = float(np.mean(retained_indicators))
    retained_count = int(sum(retained_indicators))
    conditional_mean = (
        sum(contributions) / retained_count if retained_count else 0.0
    )
    exact_cmi: float | None = None
    exact_mass: float | None = None
    cmi_inside: bool | None = None
    mass_inside: bool | None = None
    if n <= 5:
        exact = audit_information_projection_aggregate(
            n, minimum_dimension_exclusive
        )
        exact_cmi = exact.physical_mass_weighted_irreducible_racah_cmi_bits
        exact_mass = exact.retained_physical_mass
        cmi_inside = max(0.0, mean - radius) <= exact_cmi <= min(1.0, mean + radius)
        mass_inside = (
            max(0.0, retained_mass - radius)
            <= exact_mass
            <= min(1.0, retained_mass + radius)
        )
    verified = bool(
        all(sample.complete_coupling_verified for sample in samples)
        and all(
            sample.orientation_channel_verified is not False for sample in samples
        )
        and max(coupling_residuals, default=0.0) <= 3e-6
        and max(orientation_residuals, default=0.0) <= 3e-6
        and (cmi_inside is not False)
        and (mass_inside is not False)
    )
    return PhysicalOrientationRacahSamplingRecord(
        n=n,
        sample_count=sample_count,
        random_seed=random_seed,
        minimum_dimension_exclusive=minimum_dimension_exclusive,
        confidence_level=confidence_level,
        retained_paired_sample_count=retained_count,
        unpaired_or_trimmed_sample_count=sample_count - retained_count,
        unique_outer_tuple_count=len(outer_cache),
        unique_retained_sign_orbit_tuple_count=len(orbit_cache),
        sample_mean_retained_physical_cmi_bits=mean,
        sample_standard_error_bits=standard_error,
        cmi_hoeffding_radius_bits=radius,
        cmi_confidence_lower_bits=max(0.0, mean - radius),
        cmi_confidence_upper_bits=min(1.0, mean + radius),
        sample_retained_paired_mass=retained_mass,
        paired_mass_hoeffding_radius=radius,
        conditional_mean_cmi_on_retained_samples_bits=conditional_mean,
        exact_finite_retained_physical_cmi_bits=exact_cmi,
        exact_finite_retained_physical_mass=exact_mass,
        exact_cmi_inside_confidence_interval=cmi_inside,
        exact_mass_inside_confidence_interval=mass_inside,
        maximum_complete_coupling_residual=max(coupling_residuals, default=0.0),
        maximum_orientation_isometry_residual=max(
            orientation_residuals, default=0.0
        ),
        all_compiled_objects_verified=verified,
        asymptotic_inference_allowed=False,
        status=(
            "exact-physical-orientation-cmi-sampler-verified"
            if verified
            else "physical-orientation-racah-sampling-control-failure"
        ),
        samples=samples,
    )


def run_physical_orientation_racah_sampling(
) -> PhysicalOrientationRacahSamplingReport:
    records = [
        sample_physical_orientation_racah_cmi(5, 24, random_seed=271828),
        sample_physical_orientation_racah_cmi(6, 6, random_seed=314159),
    ]
    failures = sum(not row.all_compiled_objects_verified for row in records)
    verified = failures == 0
    s6 = next(row for row in records if row.n == 6)
    return PhysicalOrientationRacahSamplingReport(
        created_at=utc_now(),
        theorem_contract={
            "outer_sampler": "alpha,beta,gamma iid Plancherel; lambda conditional proportional to d_lambda M",
            "block_sampler": "(mu,nu) conditional probability x_(mu,nu)/M",
            "joint_identity": "P_outer*pi=d_alpha d_beta d_gamma d_lambda x/|S_n|^3=P_6",
            "retained_statistic": "1[all six labels are nonself and dimension>D] I(Y_g;Y_h|Y_k)",
            "range": "the retained statistic lies in [0,1] bits",
            "confidence": "Hoeffding radius sqrt(log(2/delta)/(2N))",
            "scope": "finite exact-law Monte Carlo with exponential block compilation",
        },
        records=records,
        proof_obligations=[
            {
                "obligation": "sample_full_six_label_physical_racah_law",
                "resolved": verified,
                "resolution": "Sequential outer sampling followed by x/M block sampling multiplies to the exact P6 mass.",
            },
            {
                "obligation": "validate_orientation_cmi_monte_carlo_against_exact_finite_average",
                "resolved": records[0].exact_cmi_inside_confidence_interval is True,
                "resolution": "The exact S5 retained contribution lies in the rigorous finite-sample interval.",
            },
            {
                "obligation": "obtain_decisive_s6_or_larger_confidence_interval",
                "resolved": False,
                "resolution": "The live S6 sample is deliberately small and its Hoeffding interval is broad.",
            },
            {
                "obligation": "scale_to_s7_physical_average",
                "resolved": False,
                "resolution": "Requires caching/resume, Rao-Blackwell options, and a cheaper orientation block estimator.",
            },
            {
                "obligation": "compare_classical_word_map_and_coherent_estimation",
                "resolved": False,
                "resolution": "No query/sample complexity separation follows from measured-label CMI sampling.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Selected high-CMI tuples estimate the physical average.",
                "resolved": True,
                "resolution": "The estimator samples complete six-label tuples from P6 before evaluating their orbit CMI.",
            },
            {
                "objection": "Conditioning on the paired event can ignore its probability.",
                "resolved": True,
                "resolution": "The primary statistic is zero off-event, so its mean includes source mass; the conditional mean is reported separately.",
            },
            {
                "objection": "A low sample mean proves asymptotic decay.",
                "resolved": True,
                "resolution": "Each record has a finite Hoeffding interval and asymptotic_inference_allowed=false.",
            },
            {
                "objection": "Exact physical sampling is a polynomial classical algorithm.",
                "resolved": True,
                "resolution": "The current implementation compiles exponential representation-space Racah blocks.",
            },
        ],
        headline_metrics={
            "exact_physical_orientation_sampler_count": int(verified),
            "sampling_record_count": len(records),
            "finite_control_failure_count": failures,
            "S6_sample_count": s6.sample_count,
            "S6_retained_paired_sample_count": s6.retained_paired_sample_count,
            "S6_sample_mean_retained_physical_cmi_bits": s6.sample_mean_retained_physical_cmi_bits,
            "S6_cmi_hoeffding_radius_bits": s6.cmi_hoeffding_radius_bits,
            "S6_unique_sign_orbit_tuple_count": s6.unique_retained_sign_orbit_tuple_count,
            "decisive_asymptotic_orientation_cmi_estimate_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "full_six_label_sampler_exact_proved": verified,
            "finite_s5_exact_average_covered_by_interval": records[0].exact_cmi_inside_confidence_interval is True,
            "S6_confidence_interval_decisive": False,
            "physical_average_orientation_cmi_survives_proved": False,
            "physical_average_orientation_cmi_vanishes_proved": False,
            "polynomial_estimator_proved": False,
            "coherent_extraction_implemented": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The sampling law is exact, but the live higher-n interval is broad and every compiled statistic remains exponential-space.",
        },
        status=(
            "physical-orientation-cmi-now-has-unbiased-source-weighted-sampler"
            if verified
            else "physical-orientation-racah-sampling-control-failure"
        ),
        summary=(
            "Replaced selected orientation witnesses by an exact physical-law "
            "Monte Carlo estimator with source mass and rigorous confidence bounds."
        ),
        falsifiers_triggered=[
            "Large conditional CMI on a rare orbit cannot stand in for physical-average information.",
            "A finite sample mean without a range-based interval supports no scaling claim.",
            "Measured-label sampling does not establish coherent or classically exclusive access.",
        ],
    )


def write_physical_orientation_racah_sampling_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_physical_orientation_racah_sampling())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_physical_orientation_racah_sampling_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
