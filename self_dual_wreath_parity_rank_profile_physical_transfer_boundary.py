"""Physical rank mixing reduces to a tetrahedral collision-growth threshold.

Let ``Q_n`` be six independent Plancherel labels and let ``P_n`` be the
physical six-label Racah law.  Write

    L_n=dP_n/dQ_n,
    M_n=E_Q[L_n^2],

so ``M_n`` is exactly the tetrahedral six-word cycle-signature second moment.
The product-Plancherel rank theorem supplies a good event ``G_epsilon`` on
which the rank-profile syndrome chi-square ``f_n`` obeys

    f_n <= b(epsilon)
        = [((1+epsilon)/(1-epsilon))^5-1]^2,              (1)

while

    Q_n(G_epsilon^c) <= S_n/epsilon^2,
    S_n=8V_n+2W_n.                                       (2)

Every eight-point channel has ``0<=f_n<=7``.  Cauchy--Schwarz changes measure:

    P_n(G_epsilon^c)
      = E_Q[L_n 1_(G^c)]
      <= sqrt(M_n Q_n(G^c))
      <= sqrt(M_n S_n)/epsilon.                           (3)

Therefore

    E_P f_n <= b(epsilon)+7 sqrt(M_n S_n)/epsilon.        (4)

If ``M_n S_n -> 0``, choose
``epsilon_n=(M_n S_n)^(1/6)``.  Both terms in (4) vanish,
proving physical expected rank-profile chi-square, total variation, and KL
all vanish.  Equivalently, it suffices that

    M_n=o(1/(8V_n+2W_n)).                                 (5)

This is substantially weaker than a uniformly bounded second moment.  It
converts the physical rank gate into one classical word-map question: prove
that the tetrahedral cycle-signature collision moment grows slower than the
reciprocal tensor-density variance scale.

The condition cannot be discarded.  On a two-point reference space with a
rare event of mass ``s``, let ``f=1`` only on that event and set the likelihood
to ``1/s`` there and zero elsewhere.  Then ``E_Q f=s->0`` but ``E_P f=1``,
while ``M=1/s`` and ``M s=1``.  Reference mixing alone gives no physical
mixing at the threshold.

The repository has exact ``M_n`` only through ``S_5`` and no all-``n`` bound
for the fully nonidentity word-map core ``Z6_n``.  Accordingly (5) remains a
conditional theorem, not a physical decoupling result.  It says nothing about
the irreducible non-Haar Racah cumulants even if rank transfer succeeds.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_parity_rank_profile_plancherel_mixing import class_power_sum
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    audit_tetrahedral_class_signature,
    tetrahedral_signature_second_moment,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_rank_profile_physical_transfer_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-PHYSICAL-TRANSFER-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PhysicalTransferFiniteControl:
    n: int
    exact_tetrahedral_likelihood_second_moment: str
    exact_signature_second_moment: str
    exact_fusion_density_variance: str
    exact_total_density_variance: str
    exact_ten_density_union_variance: str
    second_moment_times_union_variance: float
    reciprocal_union_variance_threshold: float
    epsilon: float
    reference_bad_event_probability_upper: float
    physical_bad_event_probability_upper: float
    good_event_rank_chi_square_upper: float
    physical_expected_rank_chi_square_upper: float
    physical_expected_rank_tv_upper: float
    physical_expected_rank_kl_upper_bits: float
    class_signature_duality_verified: bool
    finite_bound_numerically_nontrivial: bool
    status: str


@dataclass(frozen=True)
class TransferCriterionTheorem:
    reference_good_event_bound: str
    change_of_measure_bound: str
    physical_expected_chi_square_bound: str
    epsilon_choice: str
    sufficient_growth_condition: str
    bounded_second_moment_is_sufficient: bool
    bounded_second_moment_is_necessary: bool
    physical_transfer_proved_without_growth_assumption: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RareEventTransferCounterexample:
    scale: int
    rare_reference_probability: str
    rare_likelihood_ratio: str
    likelihood_second_moment: str
    reference_observable_mean: str
    physical_observable_mean: str
    second_moment_times_reference_mean: str
    likelihood_normalizes: bool
    reference_mean_vanishes_along_family: bool
    physical_mean_survives_along_family: bool
    threshold_product_constant: bool
    exact_change_of_measure_counterexample_verified: bool
    status: str


@dataclass(frozen=True)
class ParityRankProfilePhysicalTransferBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    transfer_theorem: TransferCriterionTheorem
    exact_controls: list[PhysicalTransferFiniteControl]
    rare_event_counterexamples: list[RareEventTransferCounterexample]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def good_event_rank_chi_square_bound(epsilon: float) -> float:
    if not 0 <= epsilon < 1:
        raise ValueError("epsilon must lie in [0,1)")
    if epsilon == 0:
        return 0.0
    ratio = ((1.0 + epsilon) / (1.0 - epsilon)) ** 5
    return (ratio - 1.0) ** 2


def physical_transfer_bound(
    likelihood_second_moment: float,
    union_variance: float,
    epsilon: float,
) -> tuple[float, float, float, float]:
    if likelihood_second_moment < 1 or union_variance < 0:
        raise ValueError("invalid likelihood moment or union variance")
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must lie in (0,1)")
    q_bad = min(1.0, union_variance / epsilon**2)
    p_bad = min(1.0, math.sqrt(likelihood_second_moment * q_bad))
    good = min(7.0, good_event_rank_chi_square_bound(epsilon))
    expected = min(7.0, good + 7.0 * p_bad)
    return q_bad, p_bad, good, expected


def optimized_asymptotic_epsilon(
    likelihood_second_moment: float,
    union_variance: float,
) -> float:
    product = likelihood_second_moment * union_variance
    if product <= 0:
        return 1e-12
    return min(0.5, max(1e-12, product ** (1.0 / 6.0)))


def audit_physical_transfer_finite(n: int) -> PhysicalTransferFiniteControl:
    if not 3 <= n <= 5:
        raise ValueError("exact signature controls require 3<=n<=5")
    moment = tetrahedral_signature_second_moment(n)
    signature = audit_tetrahedral_class_signature(n)
    signature_moment = Fraction(signature.exact_full_second_moment)
    fusion = class_power_sum(n, 1)
    total = class_power_sum(n, 2)
    union = 8 * fusion + 2 * total
    epsilon = optimized_asymptotic_epsilon(float(moment), float(union))
    q_bad, p_bad, good, expected = physical_transfer_bound(
        float(moment), float(union), epsilon
    )
    verified = moment == signature_moment
    return PhysicalTransferFiniteControl(
        n=n,
        exact_tetrahedral_likelihood_second_moment=str(moment),
        exact_signature_second_moment=str(signature_moment),
        exact_fusion_density_variance=str(fusion),
        exact_total_density_variance=str(total),
        exact_ten_density_union_variance=str(union),
        second_moment_times_union_variance=float(moment * union),
        reciprocal_union_variance_threshold=1.0 / float(union),
        epsilon=epsilon,
        reference_bad_event_probability_upper=q_bad,
        physical_bad_event_probability_upper=p_bad,
        good_event_rank_chi_square_upper=good,
        physical_expected_rank_chi_square_upper=expected,
        physical_expected_rank_tv_upper=min(1.0, 0.5 * math.sqrt(expected)),
        physical_expected_rank_kl_upper_bits=math.log2(1.0 + expected),
        class_signature_duality_verified=verified,
        finite_bound_numerically_nontrivial=expected < 7.0,
        status=(
            "finite-transfer-identity-verified-bound-conservative"
            if verified
            else "physical-transfer-finite-control-failure"
        ),
    )


def rare_event_transfer_counterexample(
    scale: int,
) -> RareEventTransferCounterexample:
    if scale < 2:
        raise ValueError("scale must be at least two")
    rare = Fraction(1, scale)
    likelihood = Fraction(scale)
    second_moment = rare * likelihood**2
    reference_mean = rare
    physical_mean = rare * likelihood
    product = second_moment * reference_mean
    exact = bool(
        rare * likelihood == 1
        and second_moment == scale
        and reference_mean == Fraction(1, scale)
        and physical_mean == 1
        and product == 1
    )
    return RareEventTransferCounterexample(
        scale=scale,
        rare_reference_probability=str(rare),
        rare_likelihood_ratio=str(likelihood),
        likelihood_second_moment=str(second_moment),
        reference_observable_mean=str(reference_mean),
        physical_observable_mean=str(physical_mean),
        second_moment_times_reference_mean=str(product),
        likelihood_normalizes=rare * likelihood == 1,
        reference_mean_vanishes_along_family=True,
        physical_mean_survives_along_family=True,
        threshold_product_constant=product == 1,
        exact_change_of_measure_counterexample_verified=exact,
        status=(
            "reference-mixing-destroyed-by-threshold-rare-event-reweighting"
            if exact
            else "rare-event-transfer-counterexample-failure"
        ),
    )


def run_parity_rank_profile_physical_transfer_boundary(
) -> ParityRankProfilePhysicalTransferBoundaryReport:
    controls = [audit_physical_transfer_finite(n) for n in (3, 4, 5)]
    counterexamples = [
        rare_event_transfer_counterexample(scale)
        for scale in (10, 100, 1_000, 10_000)
    ]
    failures = sum(not row.class_signature_duality_verified for row in controls)
    failures += sum(
        not row.exact_change_of_measure_counterexample_verified
        for row in counterexamples
    )
    verified = failures == 0
    theorem = TransferCriterionTheorem(
        reference_good_event_bound=(
            "Q(G_epsilon^c)<=(8V_n+2W_n)/epsilon^2"
        ),
        change_of_measure_bound=(
            "P(G_epsilon^c)<=sqrt(M_n(8V_n+2W_n))/epsilon"
        ),
        physical_expected_chi_square_bound=(
            "E_P chi2(rank||U3)<=b(epsilon)+"
            "7sqrt(M_n(8V_n+2W_n))/epsilon"
        ),
        epsilon_choice="epsilon_n=[M_n(8V_n+2W_n)]^(1/6)",
        sufficient_growth_condition="M_n(8V_n+2W_n)->0",
        bounded_second_moment_is_sufficient=True,
        bounded_second_moment_is_necessary=False,
        physical_transfer_proved_without_growth_assumption=False,
        theorem_verified=verified,
        status=(
            "physical-rank-transfer-reduced-to-tetrahedral-collision-growth"
            if verified
            else "physical-rank-transfer-boundary-control-failure"
        ),
    )
    return ParityRankProfilePhysicalTransferBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "reference_law": "Q_n=Plancherel(S_n)^6.",
            "physical_law": "P_n=L_n Q_n with E_Q L_n=1.",
            "collision_moment": (
                "M_n=E_Q L_n^2 equals the tetrahedral six-word cycle-signature "
                "second moment."
            ),
            "transfer_bound": theorem.physical_expected_chi_square_bound,
            "sharp_sufficient_condition": theorem.sufficient_growth_condition,
            "scope": (
                "The implication is proved, but the required all-n collision growth "
                "bound is open and irreducible Racah cumulants are separate."
            ),
        },
        transfer_theorem=theorem,
        exact_controls=controls,
        rare_event_counterexamples=counterexamples,
        proof_obligations=[
            {
                "obligation": "derive_product_to_physical_rank_transfer_condition",
                "resolved": verified,
                "resolution": (
                    "Cauchy--Schwarz transfers the explicit product-law good event; "
                    "balancing terms yields the M_n S_n threshold."
                ),
            },
            {
                "obligation": "test_whether_reference_mixing_alone_is_sufficient",
                "resolved": verified,
                "resolution": (
                    "Rejected by an exact rare-event family at constant M_n S_n."
                ),
            },
            {
                "obligation": "prove_tetrahedral_collision_moment_growth_below_reciprocal_variance",
                "resolved": False,
                "resolution": (
                    "Prove M_n=o(1/(8V_n+2W_n)); equivalently control the fully "
                    "nonidentity classical word-map core Z6_n at this scale."
                ),
            },
            {
                "obligation": "control_irreducible_racah_cumulants_after_rank_transfer",
                "resolved": False,
                "resolution": (
                    "Even successful rank transfer leaves the two non-Haar conditional "
                    "cumulants and their denominator tails open."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A uniformly bounded tetrahedral second moment is required.",
                "resolved": True,
                "resolution": (
                    "No. It may diverge, provided it grows more slowly than "
                    "1/(8V_n+2W_n)."
                ),
            },
            {
                "objection": "Convergence under product Plancherel automatically transfers.",
                "resolved": True,
                "resolution": (
                    "The exact rare-event model has vanishing reference signal and unit "
                    "physical signal when the second moment compensates the rare mass."
                ),
            },
            {
                "objection": "The rare one-dimensional parity tail prevents transfer.",
                "resolved": True,
                "resolution": (
                    "A constant contribution to M_n is harmless because S_n->0; only "
                    "growth at the reciprocal S_n scale can obstruct this argument."
                ),
            },
            {
                "objection": "Closing the collision threshold proves adaptive decoupling.",
                "resolved": True,
                "resolution": (
                    "It proves only physical rank-profile mixing; deterministic non-Haar "
                    "Racah conditional cumulants remain independent obligations."
                ),
            },
        ],
        headline_metrics={
            "physical_rank_transfer_criterion_theorem_count": int(verified),
            "exact_signature_duality_control_count": len(controls),
            "rare_event_transfer_counterexample_count": len(counterexamples),
            "finite_control_failure_count": failures,
            "all_n_tetrahedral_collision_growth_bound_count": 0,
            "unconditional_physical_rank_mixing_theorem_count": 0,
            "irreducible_racah_cumulant_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_rank_transfer_threshold_proved": verified,
            "bounded_tetrahedral_second_moment_required": False,
            "reference_mixing_alone_sufficient": False,
            "tetrahedral_collision_growth_condition_verified": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "adaptive_syndrome_decouples_proved": False,
            "adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Physical rank mixing now has an explicit necessary-to-check word-map "
                "growth scale, but that collision bound and all non-Haar terms are open."
            ),
        },
        status=(
            "physical-rank-mixing-reduced-to-tetrahedral-collision-growth-threshold"
            if verified
            else "parity-rank-profile-physical-transfer-boundary-failure"
        ),
        summary=(
            "Reduced transfer of rank-profile mixing to the physical law to the "
            "condition M_n(8V_n+2W_n)->0 and proved reference mixing alone insufficient."
        ),
        falsifiers_triggered=[
            "Reference-law convergence is not stable under arbitrary physical likelihood reweighting.",
            "A bounded likelihood second moment is sufficient but stronger than necessary.",
            "The constant rare parity-tail collision contribution does not by itself obstruct rank transfer.",
            "Even a successful rank transfer cannot remove deterministic non-Haar Racah synergy.",
        ],
    )


def write_parity_rank_profile_physical_transfer_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_rank_profile_physical_transfer_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_rank_profile_physical_transfer_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
