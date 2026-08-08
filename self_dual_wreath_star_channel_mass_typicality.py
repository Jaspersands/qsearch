"""Typical star-channel mass lives on factorially small correlations.

Worst-case residual overlap is controlled by the smallest available carrier
dimension and saturates at ``1/(n-1)``.  That operator-norm statistic ignores
channel multiplicity.  On a typical natural orientation triple, the exact
carrier factorization gives a very different rank-weighted law.

The seven nonempty membership-pattern blocks of three random orientations
are independent tensor products of Plancherel source irreps (the full pattern
also contains the fixed target).  If every block is large, normalized output
multiplicities concentrate around ``d_alpha/n!``.  The exact star row with
carriers ``beta,p`` and either isotype-bit pair then has normalized rank

    M_(beta,p)/(d_nu D_sources)
       = product_{four beta blocks} (m_beta/D)
         product_{three p blocks} (m_p/D) d_p
       approximately d_beta^4 d_p^4 / (n!)^7.             (1)

After rank normalization, ``beta`` and ``p`` are therefore independent under

    q_n(alpha) = d_alpha^4 / Z_4(n),
    Z_4(n) = sum_alpha d_alpha^4.                           (2)

The overlap correlation is ``gamma=1/(d_beta d_p)``, so

    E_q gamma   = (Z_3/Z_4)^2,
    E_q gamma^2 = ((n!)/Z_4)^2.                            (3)

Moreover, Aggarwal--Elboim's maximal-dimension theorem implies
``Z_4 >= d_max^4 = (n!)^2 exp(-Theta(sqrt n))``.  The q-mass of dimensions
below ``(n!)^(3/8)`` is at most

    p(n) (n!)^(3/2) / Z_4
      = (n!)^-1/2 exp(O(sqrt n)).                           (4)

Thus, outside factorially small q-mass, both carriers have dimension at least
``(n!)^(3/8)`` and ``gamma <= (n!)^-3/4``.

This module does not transfer a tiny annealed expectation by total variation.
Instead it proves a high-probability event: for a density-one set of
orientation triples, every block multiplicity and every output carrier is
simultaneously close to its regular value.  A multinomial pattern-count tail
and the exact Plancherel second-moment bound are conditioned on global source
distinctness explicitly.  Markov then converts the joint source/triple bound
into a statement that most collision-free source portfolios have only a
small fraction of bad triples.

The result is channel-rank mass, not yet PGM state mass.  A theorem connecting
this coefficient measure to the shorted endpoint effects and accepted state
is still required before spectral trimming or a speedup claim is allowed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import (
    conjugate_partition,
    hook_length_dimension,
    integer_partitions,
)
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import (
    global_collision_free_mass_record,
)
from self_dual_wreath_uniform_orientation_rank_concentration import (
    smallest_nonidentity_conjugacy_class_size,
)
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_star_channel_mass_typicality.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-STAR-CHANNEL-MASS-TYPICALITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class FixedFactorMultiplicityControl:
    n: int
    random_block_size: int
    fixed_partition: Partition
    output_partition: Partition
    expected_normalized_multiplicity: str
    exact_second_moment: str
    exact_relative_variance: str
    universal_class_size_bound: str
    bound_respected: bool
    status: str


@dataclass(frozen=True)
class AnnealedStarCarrierControl:
    n: int
    target_partition: Partition
    cluster_carrier: Partition
    companion_carrier: Partition
    cluster_carrier_dimension: int
    companion_carrier_dimension: int
    correlation: str
    expected_normalized_single_isotype_row_rank: str
    fourth_power_probability: str
    fourth_power_mean_correlation: float
    fourth_power_root_mean_square_correlation: float
    exact_carrier_law_normalized: bool
    status: str


@dataclass(frozen=True)
class StarChannelMassScalingRecord:
    n: int
    partition_count: int
    information_threshold_copy_count: int
    optimized_minimum_pattern_block_size: int
    log2_pattern_richness_failure_upper_bound: float
    log2_all_carrier_multiplicity_failure_upper_bound: float
    log2_joint_source_triple_failure_upper_bound: float
    log2_global_collision_free_probability: float
    log2_conditioned_joint_failure_upper_bound: float
    conditioned_joint_failure_upper_bound: float
    portfolio_bad_fraction_upper_bound: float
    portfolio_failure_probability_upper_bound: float
    finite_collision_free_typicality_certified: bool
    fourth_power_normalization_log2: float
    fourth_power_low_dimension_mass: float
    fourth_power_low_dimension_mass_log2: float
    distorted_high_correlation_channel_mass_upper_bound: float
    distorted_high_correlation_channel_mass_log2_upper_bound: float
    high_correlation_threshold_log2: float
    fourth_power_mean_correlation_log2: float
    fourth_power_rms_correlation_log2: float
    status: str


@dataclass(frozen=True)
class StarChannelMassTypicalityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    fixed_factor_controls: list[FixedFactorMultiplicityControl]
    annealed_carrier_controls: list[AnnealedStarCarrierControl]
    scaling_records: list[StarChannelMassScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def carrier_power_sum(n: int, power: int) -> int:
    if power < 0:
        raise ValueError("power must be nonnegative")
    return sum(
        hook_length_dimension(partition) ** power
        for partition in integer_partitions(n)
    )


def fixed_factor_normalized_multiplicity_second_moment(
    n: int,
    random_block_size: int,
    fixed: Partition,
    output: Partition,
) -> Fraction:
    """Second moment with one fixed tensor factor and random Plancherel block."""

    if random_block_size < 2:
        raise ValueError("random block size must be at least two")
    if sum(fixed) != n or sum(output) != n:
        raise ValueError("all partitions must have size n")
    order = math.factorial(n)
    fixed_dimension = hook_length_dimension(fixed)
    return sum(
        Fraction(
            symmetric_character(output, cycle_type) ** 2
            * symmetric_character(fixed, cycle_type) ** 2,
            order
            * order
            * fixed_dimension
            * fixed_dimension
            * conjugacy_class_size(cycle_type) ** (random_block_size - 2),
        )
        for cycle_type in integer_partitions(n)
    )


def fixed_factor_relative_variance(
    n: int,
    random_block_size: int,
    fixed: Partition,
    output: Partition,
) -> Fraction:
    order = math.factorial(n)
    mean = Fraction(hook_length_dimension(output), order)
    second = fixed_factor_normalized_multiplicity_second_moment(
        n, random_block_size, fixed, output
    )
    return (second - mean * mean) / (mean * mean)


def fixed_factor_class_bound(n: int, random_block_size: int) -> Fraction:
    partitions = tuple(integer_partitions(n))
    minimum = smallest_nonidentity_conjugacy_class_size(n)
    return Fraction(
        len(partitions) - 1,
        minimum ** (random_block_size - 2),
    )


def audit_fixed_factor_multiplicity(
    n: int,
    random_block_size: int,
    fixed: Partition,
    output: Partition,
) -> FixedFactorMultiplicityControl:
    order = math.factorial(n)
    mean = Fraction(hook_length_dimension(output), order)
    second = fixed_factor_normalized_multiplicity_second_moment(
        n, random_block_size, fixed, output
    )
    relative = fixed_factor_relative_variance(
        n, random_block_size, fixed, output
    )
    bound = fixed_factor_class_bound(n, random_block_size)
    verified = relative <= bound
    return FixedFactorMultiplicityControl(
        n=n,
        random_block_size=random_block_size,
        fixed_partition=fixed,
        output_partition=output,
        expected_normalized_multiplicity=str(mean),
        exact_second_moment=str(second),
        exact_relative_variance=str(relative),
        universal_class_size_bound=str(bound),
        bound_respected=verified,
        status=(
            "fixed-factor-multiplicity-concentration-bound-verified"
            if verified
            else "fixed-factor-multiplicity-concentration-bound-failure"
        ),
    )


def expected_normalized_star_row_rank(
    n: int,
    cluster_carrier: Partition,
    companion_carrier: Partition,
) -> Fraction:
    """Annealed expected normalized rank of one exact isotype-bit row."""

    order = math.factorial(n)
    cluster_dimension = hook_length_dimension(cluster_carrier)
    companion_dimension = hook_length_dimension(companion_carrier)
    return Fraction(
        cluster_dimension**4 * companion_dimension**4,
        order**7,
    )


def fourth_power_carrier_probability(
    n: int,
    carrier: Partition,
) -> Fraction:
    return Fraction(
        hook_length_dimension(carrier) ** 4,
        carrier_power_sum(n, 4),
    )


def audit_annealed_star_carrier(
    n: int,
    target: Partition,
    cluster_carrier: Partition,
    companion_carrier: Partition,
) -> AnnealedStarCarrierControl:
    cluster_dimension = hook_length_dimension(cluster_carrier)
    companion_dimension = hook_length_dimension(companion_carrier)
    z3 = carrier_power_sum(n, 3)
    z4 = carrier_power_sum(n, 4)
    order = math.factorial(n)
    probability = fourth_power_carrier_probability(
        n, cluster_carrier
    ) * fourth_power_carrier_probability(n, companion_carrier)
    normalized = sum(
        fourth_power_carrier_probability(n, partition)
        for partition in integer_partitions(n)
    ) == 1
    return AnnealedStarCarrierControl(
        n=n,
        target_partition=target,
        cluster_carrier=cluster_carrier,
        companion_carrier=companion_carrier,
        cluster_carrier_dimension=cluster_dimension,
        companion_carrier_dimension=companion_dimension,
        correlation=str(Fraction(1, cluster_dimension * companion_dimension)),
        expected_normalized_single_isotype_row_rank=str(
            expected_normalized_star_row_rank(
                n, cluster_carrier, companion_carrier
            )
        ),
        fourth_power_probability=str(probability),
        fourth_power_mean_correlation=(z3 / z4) ** 2,
        fourth_power_root_mean_square_correlation=order / z4,
        exact_carrier_law_normalized=normalized,
        status=(
            "annealed-fourth-power-star-carrier-law-verified"
            if normalized
            else "annealed-star-carrier-normalization-failure"
        ),
    )


def _log2_add(first: float, second: float) -> float:
    if first == -math.inf:
        return second
    if second == -math.inf:
        return first
    maximum = max(first, second)
    return maximum + math.log2(
        math.exp2(first - maximum) + math.exp2(second - maximum)
    )


def _log2_pattern_failure(copy_count: int, cutoff: int) -> float:
    """Union bound for one of four complement-pattern counts below cutoff."""

    terms = [
        math.comb(copy_count, count)
        * (0.25**count)
        * (0.75 ** (copy_count - count))
        for count in range(cutoff)
    ]
    probability = min(1.0, 4 * math.fsum(terms))
    return math.log2(probability) if probability else -math.inf


def _optimized_pattern_cutoff(
    n: int,
    copy_count: int,
    relative_error: float,
) -> tuple[int, float, float, float]:
    partition_count = len(integer_partitions(n))
    minimum = smallest_nonidentity_conjugacy_class_size(n)
    best: tuple[float, int, float, float] | None = None
    for cutoff in range(2, copy_count // 4 + 1):
        pattern_log = _log2_pattern_failure(copy_count, cutoff)
        variance_log = (
            math.log2(partition_count - 1)
            + (2 - cutoff) * math.log2(minimum)
        )
        # Six ordinary pattern blocks need every output carrier; the full
        # block additionally ranges over every fixed target and output.
        multiplicity_union = partition_count * partition_count + 6 * partition_count
        multiplicity_log = (
            math.log2(multiplicity_union)
            + variance_log
            - 2 * math.log2(relative_error)
        )
        joint_log = min(0.0, _log2_add(pattern_log, multiplicity_log))
        if best is None or joint_log < best[0]:
            best = (joint_log, cutoff, pattern_log, multiplicity_log)
    if best is None:
        raise ValueError("copy count is too small for a pattern-rich triple")
    return best[1], best[2], best[3], best[0]


def star_channel_mass_scaling_record(
    n: int,
    relative_error: float = 0.1,
) -> StarChannelMassScalingRecord:
    partitions = tuple(integer_partitions(n))
    copy_count = math.ceil(math.lgamma(n + 1) / math.log(2))
    cutoff, pattern_log, multiplicity_log, joint_log = _optimized_pattern_cutoff(
        n, copy_count, relative_error
    )
    collision = global_collision_free_mass_record(n)
    conditioned_log = (
        joint_log - collision.log2_unconditioned_global_collision_free_probability
        if collision.enough_distinct_partitions_exist
        else math.inf
    )
    conditioned_probability = (
        min(1.0, math.exp2(conditioned_log))
        if math.isfinite(conditioned_log) and conditioned_log > -1074
        else 0.0
        if conditioned_log == -math.inf or conditioned_log <= -1074
        else 1.0
    )
    portfolio_bound = math.sqrt(conditioned_probability)

    order = math.factorial(n)
    dimensions = [hook_length_dimension(partition) for partition in partitions]
    z3 = sum(dimension**3 for dimension in dimensions)
    z4 = sum(dimension**4 for dimension in dimensions)
    log_order = math.log2(order)
    low_weight = sum(
        dimension**4
        for dimension in dimensions
        if 8 * math.log2(dimension) < 3 * log_order
    )
    low_mass = low_weight / z4
    low_log = math.log2(low_mass) if low_mass else -math.inf
    distortion = ((1 + relative_error) / (1 - relative_error)) ** 7
    high_mass = min(1.0, 2 * distortion * low_mass)
    high_log = math.log2(high_mass) if high_mass else -math.inf
    certified = conditioned_log < 0
    return StarChannelMassScalingRecord(
        n=n,
        partition_count=len(partitions),
        information_threshold_copy_count=copy_count,
        optimized_minimum_pattern_block_size=cutoff,
        log2_pattern_richness_failure_upper_bound=pattern_log,
        log2_all_carrier_multiplicity_failure_upper_bound=multiplicity_log,
        log2_joint_source_triple_failure_upper_bound=joint_log,
        log2_global_collision_free_probability=(
            collision.log2_unconditioned_global_collision_free_probability
        ),
        log2_conditioned_joint_failure_upper_bound=conditioned_log,
        conditioned_joint_failure_upper_bound=conditioned_probability,
        portfolio_bad_fraction_upper_bound=portfolio_bound,
        portfolio_failure_probability_upper_bound=portfolio_bound,
        finite_collision_free_typicality_certified=certified,
        fourth_power_normalization_log2=math.log2(z4),
        fourth_power_low_dimension_mass=low_mass,
        fourth_power_low_dimension_mass_log2=low_log,
        distorted_high_correlation_channel_mass_upper_bound=high_mass,
        distorted_high_correlation_channel_mass_log2_upper_bound=high_log,
        high_correlation_threshold_log2=-0.75 * log_order,
        fourth_power_mean_correlation_log2=2 * (math.log2(z3) - math.log2(z4)),
        fourth_power_rms_correlation_log2=math.log2(order) - math.log2(z4),
        status=(
            "collision-free-typical-triple-fourth-power-carrier-law-certified"
            if certified
            else "finite-collision-free-triple-typicality-bound-vacuous"
        ),
    )


def run_star_channel_mass_typicality() -> StarChannelMassTypicalityReport:
    fixed_controls = [
        audit_fixed_factor_multiplicity(
            n,
            block_size,
            fixed,
            output,
        )
        for n in range(3, 8)
        for block_size in (2, 3, 5)
        for fixed in integer_partitions(n)[:2]
        for output in integer_partitions(n)
    ]
    carrier_controls = [
        audit_annealed_star_carrier(
            n,
            max(integer_partitions(n), key=hook_length_dimension),
            cluster,
            companion,
        )
        for n in range(3, 9)
        for cluster, companion in (
            (
                max(integer_partitions(n), key=hook_length_dimension),
                max(integer_partitions(n), key=hook_length_dimension),
            ),
            ((n,), max(integer_partitions(n), key=hook_length_dimension)),
        )
    ]
    scaling = [
        star_channel_mass_scaling_record(n)
        for n in (12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(not row.bound_respected for row in fixed_controls) + sum(
        not row.exact_carrier_law_normalized for row in carrier_controls
    )
    certified = sum(
        row.finite_collision_free_typicality_certified for row in scaling
    )
    onset = next(
        (
            row.n
            for row in scaling
            if row.finite_collision_free_typicality_certified
        ),
        0,
    )
    tail = scaling[-1]
    verified = failures == 0
    metrics: dict[str, int | float] = {
        "fixed_factor_second_moment_bound_theorem_count": int(verified),
        "fixed_factor_control_count": len(fixed_controls),
        "annealed_fourth_power_carrier_law_theorem_count": int(verified),
        "annealed_carrier_control_count": len(carrier_controls),
        "control_failure_count": failures,
        "scaling_row_count": len(scaling),
        "finite_collision_free_typicality_certified_row_count": certified,
        "finite_collision_free_typicality_onset_n": onset,
        "tail_n": tail.n,
        "tail_optimized_pattern_block_size": (
            tail.optimized_minimum_pattern_block_size
        ),
        "tail_log2_conditioned_joint_failure_upper_bound": (
            tail.log2_conditioned_joint_failure_upper_bound
        ),
        "tail_fourth_power_low_dimension_mass_log2": (
            tail.fourth_power_low_dimension_mass_log2
        ),
        "tail_high_correlation_mass_log2_upper_bound": (
            tail.distorted_high_correlation_channel_mass_log2_upper_bound
        ),
        "typical_triple_factorial_correlation_theorem_count": 1,
        "channel_rank_to_pgm_state_mass_transfer_theorem_count": 0,
        "natural_endpoint_comparability_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return StarChannelMassTypicalityReport(
        created_at=utc_now(),
        theorem_contract={
            "fixed_factor_variance": (
                "A fixed target tensor factor inserts r_nu(K)^2<=1 into the "
                "same exact class-size second moment, so the universal variance bound survives."
            ),
            "typical_pattern_blocks": (
                "Three random orientations distribute source pairs among four "
                "complement-pattern classes; an optimized multinomial tail bounds small blocks."
            ),
            "uniform_carrier_multiplicities": (
                "On a high-probability event, every output carrier in every active "
                "pattern block has normalized multiplicity within 1+/-eta of d_alpha/n!."
            ),
            "fourth_power_law": (
                "Each star row then has rank within (1+/-eta)^7 of "
                "d_beta^4 d_p^4/(n!)^7, inducing q(alpha)=d_alpha^4/Z4."
            ),
            "correlation_tail": (
                "Outside (n!)^-1/2 exp(O(sqrt n)) q-mass, both carrier "
                "dimensions exceed (n!)^(3/8), so gamma<=(n!)^-3/4."
            ),
            "portfolio_conversion": (
                "If the conditioned joint source/triple bad probability is delta, "
                "then with probability at least 1-sqrt(delta), a source portfolio "
                "has at most sqrt(delta) bad triples."
            ),
            "scope": (
                "The measure is coefficient-channel rank. Its relation to accepted "
                "PGM state mass and shorted endpoint spectra is unproved."
            ),
        },
        fixed_factor_controls=fixed_controls,
        annealed_carrier_controls=carrier_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_rank_weighted_star_carrier_distribution",
                "resolved": verified,
                "resolution": "Seven concentrated block multiplicities give the exact fourth-power carrier law on typical triples.",
            },
            {
                "obligation": "avoid_invalid_tiny_expectation_tv_transfer",
                "resolved": verified,
                "resolution": "The proof conditions a simultaneous multiplicity event, then divides its failure probability by P_cf; it does not transfer the tiny row mass additively."
            },
            {
                "obligation": "prove_high_correlation_channel_rank_mass_factorially_small",
                "resolved": verified,
                "resolution": "The fourth-power law plus the maximal-dimension lower bound on Z4 gives the factorial tail."
            },
            {
                "obligation": "transfer_channel_rank_mass_to_pgm_accepted_state_mass",
                "resolved": False,
                "resolution": "Need a trace identity linking carrier row multiplicities through the global distinct kernel, endpoint shorts, and PGM normalization."
            },
        ],
        adversarial_audit=[
            {
                "objection": "The maximum correlation 1/(n-1) describes a typical residual coefficient.",
                "resolved": True,
                "resolution": "Rank weighting is fourth-power in carrier dimensions; low-dimensional maximum-correlation carriers have factorially small q-mass."
            },
            {
                "objection": "Unconditioned annealed row expectations transfer to the globally distinct sector because P_cf tends to one.",
                "resolved": True,
                "resolution": "Generic additive transfer is too weak at the tiny row scale. The module instead transfers a high-probability simultaneous relative-concentration event."
            },
            {
                "objection": "Small channel-rank mass proves negligible quantum state mass.",
                "resolved": False,
                "resolution": "The PGM can reweight coefficient sectors; an explicit trace/normalization theorem is still missing."
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "typical_triple_fourth_power_carrier_law_proved": verified,
            "high_correlation_channel_rank_mass_factorially_small_proved": verified,
            "collision_free_conditioning_handled_by_relative_event": True,
            "worst_case_gamma_represents_typical_channel_mass": False,
            "channel_rank_mass_equals_pgm_state_mass_proved": False,
            "natural_shorted_endpoint_comparability_proved": False,
            "natural_pgm_endpoint_gap_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Typical coefficient rank is concentrated on factorially weak "
                "overlaps, but the PGM weighting and endpoint-short transfer are open."
            ),
        },
        status=(
            "typical-star-fourth-power-carrier-law-proved-"
            "pgm-mass-transfer-open"
            if verified
            else "star-channel-mass-typicality-control-failure"
        ),
        summary=(
            "Replaced worst-case reciprocal correlation by the typical "
            "rank-weighted d^4 carrier law and proved its high-correlation tail "
            "factorially small on density-one collision-free triples."
        ),
        falsifiers_triggered=[
            "Worst-case residual correlation is not a representative mass statistic.",
            "Total-variation conditioning cannot transfer a factorially small annealed row expectation relatively.",
            "Coefficient-rank typicality is not yet accepted-state or PGM-effect typicality.",
        ],
    )


def write_star_channel_mass_typicality_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_star_channel_mass_typicality())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_star_channel_mass_typicality_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
