"""Source-conditioned measured Racah channels decouple before the final label.

Let ``alpha,beta,gamma`` be independent Plancherel irreps of ``S_n``.  On the
maximally mixed space ``V_alpha tensor V_beta tensor V_gamma``, measure the
overlapping intermediate labels ``mu`` in ``alpha tensor beta`` and ``nu`` in
``beta tensor gamma``.  If ``q_rho=d_rho^2/n!`` and
``r_rho(g)=chi_rho(g)/d_rho``, the exact conditional law is

    P(mu,nu | alpha,beta,gamma)
      = q_mu q_nu [1 + X(alpha,beta,gamma,mu,nu)],          (1)

    1+X = sum_(g,h in S_n)
            r_alpha(g) r_beta(gh) r_gamma(h) r_mu(g) r_nu(h).

This law sums over the final Racah label.  Averaging its chi-square divergence
from ``q tensor q`` over the three source labels gives

    V5_n = E_Pl[(1+T_lambda)^2]-1
         = 2 V_n + E_Pl[T_lambda^2],                       (2)

where

    T_lambda = sum_(C != e) r_lambda(C)^2,
    V_n       = sum_(C != e) 1/|C|.

The fourth moment has a representation-free convolution form.  For ``u_C``
the uniform probability measure on a conjugacy class,

    E_Pl[T_lambda^2]
      = sum_(A,B != e) ||u_A * u_B||_2^2
      <= [sum_(C != e) |C|^(-1/2)]^2.                     (3)

Young's convolution inequality proves the bound.  The half-reciprocal class
sum tends to zero for ``S_n``.  Write a class as ``1^(n-m) union rho`` with
``rho`` fixed-point-free and centralizer order ``z_rho``.  Then

    |C|=(n)_m/z_rho,  z_rho<=m^(m/2),  q_fp-free(m)<=2^m.

Splitting at ``m=n/2`` gives explicit geometric majorants and proves

    H_n := sum_(C != e)|C|^(-1/2) = o(1),
    V5_n <= 2V_n + H_n^2 <= 3H_n^2 = o(1).                (4)

Consequently the five measured labels ``alpha,beta,gamma,mu,nu`` approach
five independent Plancherel labels in total variation.  Their average
source-conditioned channel mutual information also vanishes.  This closes
every dephased route that discards the final label before exploiting channel
correlation.

The scope boundary is essential: finite Racah channel correlations condition
on the final label ``lambda``.  Equations (1)-(4) sum that label out.  They do
not bound six-label tetrahedral synergy, final-label-conditioned correlations,
or coherent multiplicity phases, and they imply no algorithm or speedup.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_plancherel_kronecker_positivity import (
    reciprocal_nonidentity_class_sum,
)
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_source_conditioned_channel_decoupling.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SOURCE-CONDITIONED-CHANNEL-DECOUPLING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SourceConditionedChannelControl:
    n: int
    partition_count: int
    exact_reciprocal_class_variance: str
    exact_mean_character_energy: str
    exact_character_energy_second_moment: str
    exact_source_averaged_conditional_chi_square: str
    exact_nonidentity_class_convolution_energy: str | None
    exact_direct_five_character_variance: str | None
    exact_first_moment_identity_verified: bool
    exact_variance_decomposition_verified: bool
    exact_convolution_identity_verified: bool | None
    exact_direct_five_character_identity_verified: bool | None
    half_reciprocal_class_sum: float
    convolution_contraction_upper_bound: float
    source_averaged_chi_square_upper_bound: float
    average_total_variation_upper_bound: float
    average_conditional_mutual_information_upper_bound_bits: float
    maximum_character_energy: float
    maximum_character_energy_partition: Partition
    maximum_nonlinear_character_energy: float
    maximum_nonlinear_character_energy_partition: Partition
    uniform_character_energy_bound_falsified: bool
    status: str


@dataclass(frozen=True)
class SourceConditionedChannelScalingRecord:
    n: int
    conjugacy_class_count: int
    reciprocal_class_variance: float
    half_reciprocal_class_sum: float
    source_averaged_chi_square_upper_bound: float
    average_total_variation_upper_bound: float
    average_conditional_mutual_information_upper_bound_bits: float
    typical_source_bad_probability_upper_at_tv_0_1: float
    exact_source_averaged_chi_square_computed: bool
    status: str


@dataclass(frozen=True)
class HalfClassSumAsymptoticRecord:
    n: int
    small_support_geometric_ratio: float
    large_support_geometric_ratio: float
    analytic_half_reciprocal_sum_upper_bound: float
    analytic_source_averaged_chi_square_upper_bound: float
    geometric_majorants_valid: bool
    status: str


@dataclass(frozen=True)
class SourceConditionedChannelDecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[SourceConditionedChannelControl]
    scaling_records: list[SourceConditionedChannelScalingRecord]
    asymptotic_records: list[HalfClassSumAsymptoticRecord]
    asymptotic_proof: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalized_character_ratio(
    partition: Partition,
    cycle_type: Partition,
) -> Fraction:
    return Fraction(
        symmetric_character(partition, cycle_type),
        hook_length_dimension(partition),
    )


def character_ratio_energy(partition: Partition) -> Fraction:
    """Return ``T_lambda=sum_(C!=e) r_lambda(C)^2`` exactly."""

    n = sum(partition)
    identity = (1,) * n
    return sum(
        (
            normalized_character_ratio(partition, cycle_type) ** 2
            for cycle_type in integer_partitions(n)
            if cycle_type != identity
        ),
        start=Fraction(),
    )


def plancherel_character_energy_moments(n: int) -> tuple[Fraction, Fraction]:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    weights = dict(zip(partitions, plancherel_weights(n)))
    energies = {
        partition: character_ratio_energy(partition) for partition in partitions
    }
    first = sum(
        (weights[partition] * energies[partition] for partition in partitions),
        start=Fraction(),
    )
    second = sum(
        (
            weights[partition] * energies[partition] ** 2
            for partition in partitions
        ),
        start=Fraction(),
    )
    return first, second


def source_averaged_conditional_chi_square(n: int) -> Fraction:
    """Exact annealed chi-square in equation (2)."""

    first, second = plancherel_character_energy_moments(n)
    return 2 * first + second


@lru_cache(maxsize=None)
def exact_direct_five_character_variance(n: int) -> Fraction:
    """Directly average equation (1) for tiny theorem controls."""

    if not 2 <= n <= 4:
        raise ValueError("direct five-character controls require 2<=n<=4")
    partitions = tuple(integer_partitions(n))
    group = tuple(itertools.permutations(range(n)))
    weights = dict(zip(partitions, plancherel_weights(n)))
    ratios = {
        (partition, element): normalized_character_ratio(
            partition,
            permutation_cycle_type(element),
        )
        for partition in partitions
        for element in group
    }
    total = Fraction()
    for alpha, beta, gamma, mu, nu in itertools.product(partitions, repeat=5):
        likelihood = sum(
            (
                ratios[alpha, g]
                * ratios[beta, compose_permutations(g, h)]
                * ratios[gamma, h]
                * ratios[mu, g]
                * ratios[nu, h]
                for g in group
                for h in group
            ),
            start=Fraction(),
        )
        remainder = likelihood - 1
        total += (
            weights[alpha]
            * weights[beta]
            * weights[gamma]
            * weights[mu]
            * weights[nu]
            * remainder**2
        )
    return total


def half_reciprocal_class_sum(n: int) -> float:
    if n < 2:
        raise ValueError("n must be at least two")
    identity = (1,) * n
    return math.fsum(
        math.exp(-0.5 * math.log(conjugacy_class_size(cycle_type)))
        for cycle_type in integer_partitions(n)
        if cycle_type != identity
    )


@lru_cache(maxsize=None)
def exact_nonidentity_class_convolution_energy(n: int) -> Fraction:
    """Evaluate the right side of (3) directly for small ``S_n``.

    The routine enumerates ``(n!)^2`` products and is intentionally restricted
    to finite theorem controls.  The asymptotic proof does not enumerate group
    elements.
    """

    if not 2 <= n <= 6:
        raise ValueError("direct class-convolution controls require 2<=n<=6")
    group = tuple(itertools.permutations(range(n)))
    classes: dict[Partition, list[tuple[int, ...]]] = defaultdict(list)
    for element in group:
        classes[permutation_cycle_type(element)].append(element)
    identity = (1,) * n
    nonidentity = tuple(label for label in classes if label != identity)
    total = Fraction()
    for left_label in nonidentity:
        left = classes[left_label]
        for right_label in nonidentity:
            right = classes[right_label]
            products = Counter(
                permutation_cycle_type(compose_permutations(g, h))
                for g in left
                for h in right
            )
            denominator = len(left) ** 2 * len(right) ** 2
            total += sum(
                (
                    Fraction(count * count, denominator * len(classes[target]))
                    for target, count in products.items()
                ),
                start=Fraction(),
            )
    return total


def analytic_half_class_sum_upper_bound(n: int) -> HalfClassSumAsymptoticRecord:
    """Explicit geometric majorant from the moved-support proof.

    There are at most ``2^m`` fixed-point-free cycle types on moved support
    ``m`` and each has centralizer order at most ``m^(m/2)``.  The two ratios
    below majorize the support ranges ``2<=m<=n/2`` and ``n/2<m<=n``.
    """

    if n < 237:
        raise ValueError("the explicit geometric majorants require n>=237")
    small_ratio = 2.0 * (2.0 / n) ** 0.25
    large_ratio = 2.0 * (2.0 * math.e**2 / n) ** 0.25
    valid = small_ratio < 1 and large_ratio < 1
    if not valid:
        raise ValueError("geometric ratios must be below one")
    small = small_ratio**2 / (1.0 - small_ratio)
    first_large_support = n // 2 + 1
    large_log = first_large_support * math.log(large_ratio)
    large = (
        0.0
        if large_log < -745
        else math.exp(large_log) / (1.0 - large_ratio)
    )
    bound = small + large
    return HalfClassSumAsymptoticRecord(
        n=n,
        small_support_geometric_ratio=small_ratio,
        large_support_geometric_ratio=large_ratio,
        analytic_half_reciprocal_sum_upper_bound=bound,
        analytic_source_averaged_chi_square_upper_bound=3.0 * bound * bound,
        geometric_majorants_valid=valid,
        status="half-reciprocal-class-sum-geometric-majorant-verified",
    )


def source_conditioned_channel_control(
    n: int,
    *,
    validate_convolution: bool = False,
    validate_direct: bool = False,
) -> SourceConditionedChannelControl:
    if not 3 <= n <= 20:
        raise ValueError("exact character controls require 3<=n<=20")
    partitions = tuple(integer_partitions(n))
    first, second = plancherel_character_energy_moments(n)
    variance = reciprocal_nonidentity_class_sum(n)
    chi_square = 2 * first + second
    direct = (
        exact_nonidentity_class_convolution_energy(n)
        if validate_convolution
        else None
    )
    five_character = (
        exact_direct_five_character_variance(n) if validate_direct else None
    )
    half_sum = half_reciprocal_class_sum(n)
    convolution_bound = half_sum * half_sum
    chi_upper = 2 * float(variance) + convolution_bound
    energies = [
        (character_ratio_energy(partition), partition, hook_length_dimension(partition))
        for partition in partitions
    ]
    maximum = max(energies)
    maximum_nonlinear = max(row for row in energies if row[2] > 1)
    first_verified = first == variance
    decomposition_verified = chi_square == 2 * variance + second
    convolution_verified = direct == second if direct is not None else None
    direct_verified = (
        five_character == chi_square if five_character is not None else None
    )
    verified = bool(
        first_verified
        and decomposition_verified
        and (convolution_verified is not False)
        and (direct_verified is not False)
        and float(second) <= convolution_bound + 1e-12
        and float(chi_square) <= chi_upper + 1e-12
    )
    return SourceConditionedChannelControl(
        n=n,
        partition_count=len(partitions),
        exact_reciprocal_class_variance=str(variance),
        exact_mean_character_energy=str(first),
        exact_character_energy_second_moment=str(second),
        exact_source_averaged_conditional_chi_square=str(chi_square),
        exact_nonidentity_class_convolution_energy=(
            str(direct) if direct is not None else None
        ),
        exact_direct_five_character_variance=(
            str(five_character) if five_character is not None else None
        ),
        exact_first_moment_identity_verified=first_verified,
        exact_variance_decomposition_verified=decomposition_verified,
        exact_convolution_identity_verified=convolution_verified,
        exact_direct_five_character_identity_verified=direct_verified,
        half_reciprocal_class_sum=half_sum,
        convolution_contraction_upper_bound=convolution_bound,
        source_averaged_chi_square_upper_bound=chi_upper,
        average_total_variation_upper_bound=0.5 * math.sqrt(float(chi_square)),
        average_conditional_mutual_information_upper_bound_bits=math.log2(
            1.0 + float(chi_square)
        ),
        maximum_character_energy=float(maximum[0]),
        maximum_character_energy_partition=maximum[1],
        maximum_nonlinear_character_energy=float(maximum_nonlinear[0]),
        maximum_nonlinear_character_energy_partition=maximum_nonlinear[1],
        uniform_character_energy_bound_falsified=maximum_nonlinear[0] > 1,
        status=(
            "exact-source-conditioned-channel-variance-identity-verified"
            if verified
            else "source-conditioned-channel-control-failure"
        ),
    )


def source_conditioned_channel_scaling_record(
    n: int,
) -> SourceConditionedChannelScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    variance = float(reciprocal_nonidentity_class_sum(n))
    half_sum = half_reciprocal_class_sum(n)
    chi_upper = 2.0 * variance + half_sum * half_sum
    tv_upper = 0.5 * math.sqrt(chi_upper)
    return SourceConditionedChannelScalingRecord(
        n=n,
        conjugacy_class_count=len(integer_partitions(n)),
        reciprocal_class_variance=variance,
        half_reciprocal_class_sum=half_sum,
        source_averaged_chi_square_upper_bound=chi_upper,
        average_total_variation_upper_bound=tv_upper,
        average_conditional_mutual_information_upper_bound_bits=math.log2(
            1.0 + chi_upper
        ),
        typical_source_bad_probability_upper_at_tv_0_1=min(
            1.0,
            chi_upper / (4.0 * 0.1**2),
        ),
        exact_source_averaged_chi_square_computed=False,
        status="source-conditioned-channel-information-upper-bound-vanishing",
    )


def run_source_conditioned_channel_decoupling(
) -> SourceConditionedChannelDecouplingReport:
    controls = [
        source_conditioned_channel_control(
            n,
            validate_convolution=n <= 6,
            validate_direct=n <= 4,
        )
        for n in range(3, 15)
    ]
    scaling = [
        source_conditioned_channel_scaling_record(n)
        for n in (16, 20, 24, 30, 40, 50)
    ]
    asymptotic = [
        analytic_half_class_sum_upper_bound(n)
        for n in (300, 1_000, 10_000, 100_000)
    ]
    failures = sum(
        row.status != "exact-source-conditioned-channel-variance-identity-verified"
        for row in controls
    )
    verified = failures == 0 and all(
        row.geometric_majorants_valid for row in asymptotic
    )
    tail = scaling[-1]
    return SourceConditionedChannelDecouplingReport(
        created_at=utc_now(),
        theorem_contract={
            "conditional_channel_law": (
                "P(mu,nu|alpha,beta,gamma)=q_mu q_nu[1+X], with 1+X the "
                "five-character sum over (g,h)."
            ),
            "annealed_chi_square": (
                "E_source chi^2(P(.|source)||Plancherel^2)="
                "2V_n+E_Pl[T_lambda^2]."
            ),
            "convolution_identity": (
                "E_Pl[T_lambda^2]=sum_(A,B!=e)||u_A*u_B||_2^2."
            ),
            "convolution_contraction": (
                "Young contraction bounds the fourth moment by "
                "[sum_(C!=e)|C|^-1/2]^2."
            ),
            "symmetric_group_asymptotic": (
                "Moved-support centralizer bounds prove the half-reciprocal "
                "class sum is o(1)."
            ),
            "five_label_consequence": (
                "The physical law of alpha,beta,gamma,mu,nu approaches five "
                "independent Plancherel labels in total variation."
            ),
            "scope": (
                "The final label is summed out. Six-label synergy, lambda-conditioned "
                "channel information, and coherent multiplicity phases remain open."
            ),
        },
        exact_controls=controls,
        scaling_records=scaling,
        asymptotic_records=asymptotic,
        asymptotic_proof={
            "half_reciprocal_support_decomposition": (
                "H_n=sum_(m=2)^n sum_(rho no ones) sqrt(z_rho/(n)_m)"
            ),
            "centralizer_bound": "z_rho<=m^(m/2)",
            "type_count_bound": "q_fixed_point_free(m)<=2^m",
            "small_support_ratio": "a_n=2(2/n)^(1/4)",
            "large_support_ratio": "b_n=2(2e^2/n)^(1/4)",
            "geometric_bound": (
                "H_n<=a_n^2/(1-a_n)+b_n^(floor(n/2)+1)/(1-b_n)"
            ),
            "half_reciprocal_sum_tends_to_zero": True,
            "source_averaged_chi_square_tends_to_zero": True,
            "five_label_total_variation_tends_to_zero": True,
            "average_source_conditioned_mutual_information_tends_to_zero": True,
        },
        proof_obligations=[
            {
                "obligation": "derive_exact_source_conditioned_channel_law",
                "resolved": True,
                "resolution": (
                    "Expand the two overlapping central isotypic projectors on "
                    "V_alpha tensor V_beta tensor V_gamma."
                ),
            },
            {
                "obligation": "bound_source_averaged_channel_information_without_final_label",
                "resolved": True,
                "resolution": (
                    "The exact fourth moment is a sum of class-convolution L2 "
                    "energies controlled by a vanishing half-reciprocal class sum."
                ),
            },
            {
                "obligation": "bound_final_label_conditioned_channel_information",
                "resolved": False,
                "resolution": (
                    "Finite S6 sectors show that revealing lambda can unlock "
                    "correlation; an all-n tetrahedral estimate is still required."
                ),
            },
            {
                "obligation": "bound_coherent_multiplicity_phase_information",
                "resolved": False,
                "resolution": (
                    "All calculations dephase intermediate labels and discard "
                    "Racah matrix phases."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A uniform bound on T_lambda is needed.",
                "resolved": True,
                "resolution": (
                    "False. Low-dimensional irreps have growing T_lambda; the "
                    "Plancherel fourth moment is instead controlled after class convolution."
                ),
            },
            {
                "objection": "Finite nonzero Racah channel mutual information contradicts decoupling.",
                "resolved": True,
                "resolution": (
                    "The finite channel observable conditions on lambda; this theorem "
                    "sums lambda out and identifies that conditioning as essential."
                ),
            },
            {
                "objection": "An annealed bound proves every source triple is good.",
                "resolved": False,
                "resolution": (
                    "It proves average and high-probability control by Markov, not a "
                    "uniform statement over exponentially many source triples."
                ),
            },
            {
                "objection": "Measured-label decoupling rules out coherent recoupling algorithms.",
                "resolved": False,
                "resolution": (
                    "Coherent multiplicity indices and phases are absent from the law."
                ),
            },
        ],
        headline_metrics={
            "exact_source_conditioned_variance_identity_theorem_count": 1,
            "class_convolution_fourth_moment_theorem_count": 1,
            "half_reciprocal_class_sum_asymptotic_theorem_count": 1,
            "five_label_plancherel_decoupling_theorem_count": 1,
            "final_label_necessity_reduction_count": 1,
            "exact_control_count": len(controls),
            "exact_control_failure_count": failures,
            "maximum_exact_control_n": max(row.n for row in controls),
            "tail_scaling_n": tail.n,
            "tail_source_averaged_chi_square_upper_bound": (
                tail.source_averaged_chi_square_upper_bound
            ),
            "tail_average_total_variation_upper_bound": (
                tail.average_total_variation_upper_bound
            ),
            "final_conditioned_channel_theorem_count": 0,
            "coherent_phase_no_go_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_source_conditioned_channel_law_proved": verified,
            "source_averaged_channel_chi_square_vanishes_proved": verified,
            "five_label_plancherel_product_law_in_total_variation_proved": verified,
            "average_source_conditioned_channel_mutual_information_vanishes_proved": verified,
            "dephased_channel_route_without_final_label_closed": verified,
            "final_label_conditioned_channel_information_vanishes_proved": False,
            "full_six_label_product_law_proved": False,
            "coherent_multiplicity_phase_signal_absent_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All pre-final measured-label dependence vanishes, but the final "
                "label can unlock tetrahedral synergy and coherent phases are untouched."
            ),
        },
        status=(
            "source-conditioned-measured-channels-decouple-final-label-open"
            if verified
            else "source-conditioned-channel-decoupling-control-failure"
        ),
        summary=(
            "Proved that source-conditioned intermediate labels decouple after "
            "summing the final irrep, isolating final-label synergy and coherent "
            "multiplicity phase as the only surviving recoupling targets."
        ),
        falsifiers_triggered=[
            "Large character-ratio energy in low-dimensional irreps does not survive Plancherel convolution averaging.",
            "Measured intermediate labels without the final irrep have vanishing average correlation.",
            "Finite S6 nonflatness cannot justify an asymptotic channel signal unless final-label conditioning survives.",
        ],
    )


def write_source_conditioned_channel_decoupling_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_source_conditioned_channel_decoupling())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_source_conditioned_channel_decoupling_report()
    print(json.dumps(report, indent=2))
