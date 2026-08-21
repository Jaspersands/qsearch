"""Haar rank-profile syndrome mixes under independent Plancherel labels.

For ``m`` independent Plancherel irreps of ``S_n``, define the normalized
tensor-multiplicity density

    Y_m(lambda_1,...,lambda_m)
      = n! <chi_1 ... chi_(m-1),chi_m> / product_i d_i
      = sum_(g in S_n) product_i r_i(g).                  (1)

Column orthogonality gives the exact moments

    E Y_m = 1,
    E(Y_m-1)^2 = sum_(C != e) |C|^(2-m).                  (2)

If the last diagram is transposed, its character is multiplied by sign, and

    E(Y_m-Y_m^sign)^2
      = 4 sum_(C odd) |C|^(2-m).                          (3)

For the parity Racah rank profile, four sign-twisted fusion densities use
``m=3`` and the final total-multiplicity density uses ``m=4``.  Let

    V_n=sum_(C!=e)|C|^-1,   W_n=sum_(C!=e)|C|^-2.

After cancelling the common dimension factor, the eight rank amplitudes are

    R_(g,h,k)=Y1_g Y2_(g xor k) Y3_h Y4_(h xor k)/Z_k.    (4)

Under six independent Plancherel labels, Chebyshev and a union bound imply
that all eight ``Y`` variables and both ``Z`` variables lie in
``[1-epsilon,1+epsilon]`` except with probability at most

    (8 V_n + 2 W_n)/epsilon^2.                            (5)

On this good event, every ``R_y`` lies between

    L=(1-epsilon)^4/(1+epsilon),
    U=(1+epsilon)^4/(1-epsilon).

Therefore the chi-square of the normalized rank channel from uniform is at
most ``(U/L-1)^2``.  On the bad event every eight-point channel has chi-square
at most seven.  Taking ``epsilon=(8V_n+2W_n)^(1/4)`` and using
``W_n<=V_n=o(1)`` proves

    E_(Plancherel^6) chi2(P_rank(.|labels)||U_3) -> 0.    (6)

The same follows for expected total variation and KL divergence.  Thus
Kronecker multiplicity geometry cannot retain asymptotic adaptive syndrome
information under the independent reference law.  On tuples where the total
multiplicity vanishes and no rank channel exists, define the reference channel
to be uniform; every such tuple lies outside the high-probability good event,
so this harmless convention does not affect the conclusion.

This is not yet a theorem under the physical six-label Racah law.  That law
reweights the reference by an unbounded tetrahedral likelihood whose low-tail
and uniform-integrability behavior on the canonical trim remain open.  Nor
does (6) control the irreducible non-Haar Racah CMI.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_parity_racah_rank_residual_decomposition import (
    audit_racah_rank_residual,
)
from self_dual_wreath_source_conditioned_channel_decoupling import (
    analytic_half_class_sum_upper_bound,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import transpose_partition
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_rank_profile_plancherel_mixing.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-PLANCHEREL-MIXING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class TensorMultiplicityMomentControl:
    n: int
    tensor_order: int
    partition_count: int
    exact_density_mean: str
    exact_density_variance: str
    exact_class_power_sum: str
    exact_sign_twist_difference_second_moment: str
    exact_odd_class_power_sum_times_four: str
    density_mean_identity_verified: bool
    density_variance_identity_verified: bool
    sign_twist_moment_identity_verified: bool
    status: str


@dataclass(frozen=True)
class RankProfileFactorizationControl:
    control_id: str
    n: int
    orbit_indices: tuple[int, ...]
    exact_rank_profile_from_module: tuple[float, ...]
    density_ratio_factorization: tuple[float, ...]
    maximum_factorization_residual: float
    exact_density_ratio_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class RankProfileMixingScalingRecord:
    n: int
    variance_source: str
    fusion_density_variance_upper: float
    total_density_variance_upper: float
    ten_density_union_variance_upper: float
    epsilon: float
    bad_event_probability_upper: float
    good_event_rank_chi_square_upper: float
    expected_rank_chi_square_upper: float
    expected_rank_total_variation_upper: float
    expected_rank_kl_upper_bits: float
    bound_numerically_nontrivial: bool
    bound_asymptotically_vanishing: bool
    physical_measure_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class ParityRankProfilePlancherelMixingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_moment_controls: list[TensorMultiplicityMomentControl]
    factorization_controls: list[RankProfileFactorizationControl]
    finite_scaling_records: list[RankProfileMixingScalingRecord]
    analytic_scaling_records: list[RankProfileMixingScalingRecord]
    asymptotic_proof: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def class_power_sum(
    n: int,
    power: int,
    *,
    odd_only: bool = False,
) -> Fraction:
    if n < 2 or power < 1:
        raise ValueError("require n>=2 and a positive reciprocal power")
    identity = (1,) * n
    return sum(
        (
            Fraction(1, conjugacy_class_size(cycle_type) ** power)
            for cycle_type in integer_partitions(n)
            if cycle_type != identity
            and (
                not odd_only
                or (n - len(cycle_type)) % 2 == 1
            )
        ),
        start=Fraction(),
    )


def normalized_tensor_multiplicity_density(
    labels: Iterable[Partition],
    *,
    transpose_last: bool = False,
) -> Fraction:
    partitions = tuple(labels)
    if len(partitions) < 2:
        raise ValueError("at least two tensor labels are required")
    n = sum(partitions[0])
    if any(sum(partition) != n for partition in partitions):
        raise ValueError("all partitions must have equal size")
    if transpose_last:
        partitions = (*partitions[:-1], transpose_partition(partitions[-1]))
    dimensions = tuple(hook_length_dimension(partition) for partition in partitions)
    return sum(
        (
            Fraction(
                conjugacy_class_size(cycle_type)
                * math.prod(
                    symmetric_character(partition, cycle_type)
                    for partition in partitions
                ),
                math.prod(dimensions),
            )
            for cycle_type in integer_partitions(n)
        ),
        start=Fraction(),
    )


def audit_tensor_multiplicity_moments(
    n: int,
    tensor_order: int,
) -> TensorMultiplicityMomentControl:
    if not 3 <= n <= 5 or tensor_order not in (3, 4):
        raise ValueError("exact controls require 3<=n<=5 and tensor order 3 or 4")
    partitions = tuple(integer_partitions(n))
    weights = dict(zip(partitions, plancherel_weights(n)))
    mean = Fraction()
    variance = Fraction()
    twist_difference = Fraction()
    for labels in itertools.product(partitions, repeat=tensor_order):
        probability = math.prod(weights[label] for label in labels)
        density = normalized_tensor_multiplicity_density(labels)
        twisted = normalized_tensor_multiplicity_density(
            labels, transpose_last=True
        )
        mean += probability * density
        variance += probability * (density - 1) ** 2
        twist_difference += probability * (density - twisted) ** 2
    expected_variance = class_power_sum(n, tensor_order - 2)
    expected_twist = 4 * class_power_sum(
        n, tensor_order - 2, odd_only=True
    )
    mean_verified = mean == 1
    variance_verified = variance == expected_variance
    twist_verified = twist_difference == expected_twist
    return TensorMultiplicityMomentControl(
        n=n,
        tensor_order=tensor_order,
        partition_count=len(partitions),
        exact_density_mean=str(mean),
        exact_density_variance=str(variance),
        exact_class_power_sum=str(expected_variance),
        exact_sign_twist_difference_second_moment=str(twist_difference),
        exact_odd_class_power_sum_times_four=str(expected_twist),
        density_mean_identity_verified=mean_verified,
        density_variance_identity_verified=variance_verified,
        sign_twist_moment_identity_verified=twist_verified,
        status=(
            "plancherel-tensor-density-moments-match-class-power-sums"
            if mean_verified and variance_verified and twist_verified
            else "tensor-multiplicity-moment-control-failure"
        ),
    )


def audit_rank_profile_density_factorization(
    control_id: str,
    n: int,
    orbit_indices: tuple[int, ...],
    *,
    tolerance: float = 1e-10,
) -> RankProfileFactorizationControl:
    control = audit_racah_rank_residual(control_id, n, orbit_indices)
    alpha, beta, gamma, mu, nu, lam = control.orbit_representatives
    faces = (
        (alpha, beta, mu),
        (mu, gamma, lam),
        (beta, gamma, nu),
        (alpha, nu, lam),
    )
    twisted_faces = tuple(
        (
            normalized_tensor_multiplicity_density(face),
            normalized_tensor_multiplicity_density(face, transpose_last=True),
        )
        for face in faces
    )
    totals = (
        normalized_tensor_multiplicity_density((alpha, beta, gamma, lam)),
        normalized_tensor_multiplicity_density(
            (alpha, beta, gamma, lam), transpose_last=True
        ),
    )
    common = math.prod(
        hook_length_dimension(partition)
        for partition in control.orbit_representatives
    ) / math.factorial(n) ** 3
    first, second, third, fourth = twisted_faces
    factorized = tuple(
        common
        * float(first[g] * second[g ^ k] * third[h] * fourth[h ^ k] / totals[k])
        if totals[k]
        else 0.0
        for g, h, k in itertools.product((0, 1), repeat=3)
    )
    observed = tuple(
        row.haar_rank_profile_benchmark for row in control.channels
    )
    residual = max(abs(left - right) for left, right in zip(observed, factorized))
    verified = residual <= tolerance
    return RankProfileFactorizationControl(
        control_id=control_id,
        n=n,
        orbit_indices=orbit_indices,
        exact_rank_profile_from_module=observed,
        density_ratio_factorization=factorized,
        maximum_factorization_residual=residual,
        exact_density_ratio_factorization_verified=verified,
        status=(
            "rank-profile-factorizes-into-four-fusion-densities-over-total-density"
            if verified
            else "rank-profile-density-factorization-control-failure"
        ),
    )


def _mixing_bound_from_variances(
    n: int,
    fusion_variance: float,
    total_variance: float,
    variance_source: str,
) -> RankProfileMixingScalingRecord:
    union_variance = 8.0 * fusion_variance + 2.0 * total_variance
    if union_variance <= 0:
        epsilon = 0.0
        bad = 0.0
        good_chi = 0.0
    elif union_variance < 1:
        epsilon = union_variance**0.25
        bad = min(1.0, union_variance / epsilon**2)
        lower = (1.0 - epsilon) ** 4 / (1.0 + epsilon)
        upper = (1.0 + epsilon) ** 4 / (1.0 - epsilon)
        good_chi = (upper / lower - 1.0) ** 2
    else:
        epsilon = 1.0
        bad = 1.0
        good_chi = 7.0
    expected_chi = min(7.0, good_chi + 7.0 * bad)
    return RankProfileMixingScalingRecord(
        n=n,
        variance_source=variance_source,
        fusion_density_variance_upper=fusion_variance,
        total_density_variance_upper=total_variance,
        ten_density_union_variance_upper=union_variance,
        epsilon=epsilon,
        bad_event_probability_upper=bad,
        good_event_rank_chi_square_upper=min(7.0, good_chi),
        expected_rank_chi_square_upper=expected_chi,
        expected_rank_total_variation_upper=min(
            1.0, 0.5 * math.sqrt(expected_chi)
        ),
        expected_rank_kl_upper_bits=math.log2(1.0 + expected_chi),
        bound_numerically_nontrivial=expected_chi < 7.0,
        bound_asymptotically_vanishing=True,
        physical_measure_transfer_proved=False,
        status=(
            "product-plancherel-rank-profile-mixing-bound-nontrivial"
            if expected_chi < 7.0
            else "product-plancherel-rank-profile-bound-asymptotic-only"
        ),
    )


def exact_rank_profile_mixing_record(n: int) -> RankProfileMixingScalingRecord:
    return _mixing_bound_from_variances(
        n,
        float(class_power_sum(n, 1)),
        float(class_power_sum(n, 2)),
        "exact conjugacy-class power sums",
    )


def analytic_rank_profile_mixing_record(n: int) -> RankProfileMixingScalingRecord:
    if n < 237:
        raise ValueError("analytic half-class-sum majorant requires n>=237")
    half_sum = (
        analytic_half_class_sum_upper_bound(n).analytic_half_reciprocal_sum_upper_bound
    )
    variance_upper = half_sum**2
    return _mixing_bound_from_variances(
        n,
        variance_upper,
        variance_upper,
        "analytic H_n^2 upper bound for both V_n and W_n",
    )


def run_parity_rank_profile_plancherel_mixing(
) -> ParityRankProfilePlancherelMixingReport:
    moments = [
        audit_tensor_multiplicity_moments(n, tensor_order)
        for n in (3, 4, 5)
        for tensor_order in (3, 4)
    ]
    factorizations = [
        audit_rank_profile_density_factorization("S4-FACTOR", 4, (1,) * 6),
        audit_rank_profile_density_factorization("S5-FACTOR-A", 5, (2,) * 6),
        audit_rank_profile_density_factorization(
            "S5-FACTOR-B", 5, (1, 2, 1, 2, 2, 2)
        ),
    ]
    finite_scaling = [
        exact_rank_profile_mixing_record(n) for n in (8, 12, 16, 20, 24, 30)
    ]
    analytic_scaling = [
        analytic_rank_profile_mixing_record(n)
        for n in (300, 1_000, 10_000, 100_000)
    ]
    failures = sum(
        not row.density_mean_identity_verified
        or not row.density_variance_identity_verified
        or not row.sign_twist_moment_identity_verified
        for row in moments
    ) + sum(
        not row.exact_density_ratio_factorization_verified
        for row in factorizations
    )
    verified = failures == 0
    return ParityRankProfilePlancherelMixingReport(
        created_at=utc_now(),
        theorem_contract={
            "tensor_density_moments": (
                "For m independent Plancherel labels, E Y_m=1 and "
                "Var(Y_m)=sum_(C!=e)|C|^(2-m)."
            ),
            "sign_twist_moment": (
                "E(Y_m-Y_m^sign)^2=4sum_(C odd)|C|^(2-m)."
            ),
            "rank_profile_factorization": (
                "After a common dimension factor cancels, R_ghk="
                "Y1_gY2_(g xor k)Y3_hY4_(h xor k)/Z_k."
            ),
            "concentration": (
                "All ten densities lie in [1-epsilon,1+epsilon] except with "
                "probability <=(8V_n+2W_n)/epsilon^2."
            ),
            "reference_mixing": (
                "E_(Pl^6)chi2(P_rank||U3)->0, hence expected TV and KL vanish; "
                "absent total-multiplicity sectors are assigned the uniform channel."
            ),
            "scope": (
                "The theorem is under independent Plancherel reference labels. "
                "Physical likelihood reweighting and irreducible Racah arithmetic "
                "are not controlled."
            ),
        },
        exact_moment_controls=moments,
        factorization_controls=factorizations,
        finite_scaling_records=finite_scaling,
        analytic_scaling_records=analytic_scaling,
        asymptotic_proof={
            "V_n_tends_to_zero": True,
            "W_n_leq_V_n": True,
            "ten_density_union_variance_tends_to_zero": True,
            "epsilon_choice": "epsilon_n=(8V_n+2W_n)^(1/4)",
            "bad_event_probability_tends_to_zero": True,
            "good_event_rank_chi_square_tends_to_zero": True,
            "universal_eight_channel_chi_square_upper": "7",
            "expected_product_plancherel_rank_chi_square_tends_to_zero": True,
            "expected_product_plancherel_rank_tv_tends_to_zero": True,
            "expected_product_plancherel_rank_kl_tends_to_zero": True,
            "physical_measure_transfer_proved": False,
        },
        proof_obligations=[
            {
                "obligation": "prove_rank_profile_mixing_under_independent_plancherel_reference",
                "resolved": verified,
                "resolution": (
                    "Exact class-power moments, ten-variable concentration, and the "
                    "universal chi-square bound seven prove mean mixing."
                ),
            },
            {
                "obligation": "transfer_rank_profile_mixing_to_physical_six_label_law",
                "resolved": False,
                "resolution": (
                    "Prove uniform integrability/change-of-measure control for the "
                    "tetrahedral physical likelihood on the canonical trim."
                ),
            },
            {
                "obligation": "bound_irreducible_racah_conditional_cumulants",
                "resolved": False,
                "resolution": (
                    "The rank theorem says nothing about deterministic 6j arithmetic; "
                    "use the two conditional cumulants from the companion module."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Kronecker multiplicities can have zeros, invalidating ratio concentration.",
                "resolved": True,
                "resolution": (
                    "On the high-probability good event every normalized density is at "
                    "least 1-epsilon>0; all zero/low-tail cases are charged to the bad event."
                ),
            },
            {
                "objection": "Convergence in probability does not imply expected chi-square mixing.",
                "resolved": True,
                "resolution": (
                    "Every distribution on eight points has chi-square from uniform at "
                    "most seven, so the bad event is uniformly bounded."
                ),
            },
            {
                "objection": "Reference-law mixing proves physical adaptive decoupling.",
                "resolved": True,
                "resolution": (
                    "False. The physical law multiplies by a correlated tetrahedral "
                    "likelihood whose uniform integrability is exactly the open gate."
                ),
            },
            {
                "objection": "Rank-profile mixing controls natural Racah CMI.",
                "resolved": True,
                "resolution": (
                    "False. Natural channels can leave the entire rank-compatible Markov "
                    "family through deterministic non-Haar conditional cumulants."
                ),
            },
        ],
        headline_metrics={
            "product_plancherel_rank_profile_mixing_theorem_count": int(verified),
            "tensor_density_moment_control_count": len(moments),
            "rank_density_factorization_control_count": len(factorizations),
            "finite_control_failure_count": failures,
            "maximum_factorization_residual": max(
                row.maximum_factorization_residual for row in factorizations
            ),
            "physical_measure_rank_profile_mixing_theorem_count": 0,
            "irreducible_racah_cumulant_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "tensor_multiplicity_class_power_moments_proved": verified,
            "rank_profile_density_ratio_factorization_proved": verified,
            "product_plancherel_expected_rank_chi_square_vanishes_proved": verified,
            "product_plancherel_expected_rank_kl_vanishes_proved": verified,
            "physical_measure_change_uniform_integrability_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "adaptive_syndrome_decouples_proved": False,
            "adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Multiplicity geometry mixes under independent Plancherel labels; "
                "physical likelihood reweighting and non-Haar Racah cumulants remain open."
            ),
        },
        status=(
            "rank-profile-mixes-under-product-plancherel-physical-transfer-open"
            if verified
            else "rank-profile-plancherel-mixing-control-failure"
        ),
        summary=(
            "Proved that Haar Kronecker rank-profile syndrome information vanishes "
            "under independent Plancherel reference labels."
        ),
        falsifiers_triggered=[
            "Typical Kronecker multiplicity rank geometry alone cannot retain adaptive syndrome information under the reference law.",
            "Finite rank-profile bias is compatible with asymptotic reference mixing.",
            "Physical source reweighting cannot be replaced by independent Plancherel averaging.",
            "Any surviving irreducible signal must come from non-Haar Racah arithmetic or a singular change of measure.",
        ],
    )


def write_parity_rank_profile_plancherel_mixing_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_rank_profile_plancherel_mixing())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_rank_profile_plancherel_mixing_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
