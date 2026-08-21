"""Six-label entropy is natural Racah mutual information plus ``o(1)``.

Use the recoupling coupling ``pi(mu,nu|alpha,beta,gamma,lambda)`` from the
collision-channel reduction.  Its marginals are ``p(mu|outer)`` and
``r(nu|outer)``.  With ``q`` denoting Plancherel measure and

    P_outer = q^4 Z,
    P_6 = P_outer pi,

the KL chain rule and the information projection onto product couplings give
the exact identity

    D(P_6 || q^6)
      = D(P_outer || q^4)
        + E_(P_outer)[
            I_pi(mu;nu) + D(p||q) + D(r||q)
          ].                                               (1)

Each five-label marginal is a tetrahedral edge deletion.  If ``V5_n`` is the
proved common five-label chi-square divergence, then

    D(P_outer,mu || q^5), D(P_outer,nu || q^5)
      <= log2(1+V5_n).

Since these two divergences equal ``D_outer+E D(p||q)`` and
``D_outer+E D(r||q)``, respectively, (1) yields

    E I_pi <= D(P_6||q^6)
      <= E I_pi + 2 log2(1+V5_n).                         (2)

The repository already proves ``V5_n=o(1)``.  Therefore

    D(P_6||q^6) = E_(P_outer) I_pi(mu;nu) + o(1).          (3)

Transpose-orbit aggregation contracts KL, so the coarse alternating entropy
needed for physical rank-profile mixing is sublogarithmic whenever

    E_(P_outer) I_pi(mu;nu) = o(log n).                   (4)

Condition (4) is strictly weaker than subpolynomial Racah collision.  It is
the preferred rank-transfer target if the Renyi norm is tail-dominated.

Rank marginals and unitarity still do not imply (4).  The abstract identity
orthogonal matrix with block sizes ``d_lambda^2`` induces
``pi(lambda,nu)=q_lambda 1[lambda=nu]``.  Its marginals are exactly
Plancherel but its mutual information is the Plancherel entropy.  The known
maximal-irrep bound makes that entropy ``Omega(sqrt(n))``, far above
``o(log n)``.  Natural growing-row 6j delocalization remains the only missing
rank-level theorem.  Non-Haar syndrome CMI is a separate obligation.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
)
from self_dual_wreath_source_conditioned_channel_decoupling import (
    source_averaged_conditional_chi_square,
    source_conditioned_channel_scaling_record,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_recoupling_mutual_information_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-MUTUAL-INFORMATION-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RecouplingMutualInformationFiniteControl:
    n: int
    full_six_label_kl_bits: float
    outer_four_label_kl_bits: float
    physical_average_recoupling_mutual_information_bits: float
    physical_average_left_marginal_kl_bits: float
    physical_average_right_marginal_kl_bits: float
    full_kl_chain_residual_bits: float
    left_five_label_kl_bits: float
    right_five_label_kl_bits: float
    left_five_label_chain_residual_bits: float
    right_five_label_chain_residual_bits: float
    exact_five_label_chi_square: float
    five_label_kl_upper_bits: float
    maximum_five_label_kl_bound_violation_bits: float
    non_mutual_information_remainder_bits: float
    exact_non_mi_remainder_formula_residual_bits: float
    coarse_transpose_orbit_kl_bits: float
    full_to_coarse_kl_contraction_slack_bits: float
    exact_recoupling_mutual_information_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class RecouplingEntropyScalingControl:
    n: int
    five_label_chi_square_upper: float
    non_mutual_information_remainder_upper_bits: float
    remainder_asymptotically_vanishing: bool
    physical_average_racah_mutual_information_sublogarithmic_proved: bool
    status: str


@dataclass(frozen=True)
class MarginallyPerfectMutualInformationCountermodel:
    n: int
    partition_count: int
    plancherel_entropy_bits: float
    plancherel_entropy_over_log2_n: float
    row_marginal_kl_to_plancherel_bits: float
    column_marginal_kl_to_plancherel_bits: float
    identity_block_mutual_information_bits: float
    asymptotic_superlogarithmic_information_certified: bool
    status: str


@dataclass(frozen=True)
class RecouplingMutualInformationTheorem:
    exact_kl_chain: str
    five_label_remainder_bound: str
    asymptotic_identity: str
    sufficient_rank_transfer_condition: str
    condition_weaker_than_subpolynomial_collision: bool
    natural_racah_mutual_information_sublogarithmic_proved: bool
    status: str


@dataclass(frozen=True)
class RecouplingMutualInformationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: RecouplingMutualInformationTheorem
    exact_controls: list[RecouplingMutualInformationFiniteControl]
    scaling_controls: list[RecouplingEntropyScalingControl]
    marginal_countermodels: list[MarginallyPerfectMutualInformationCountermodel]
    literature_basis: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def relative_entropy_bits(
    probability: np.ndarray,
    reference: np.ndarray,
) -> float:
    positive = probability > 0
    if np.any(reference[positive] <= 0):
        return math.inf
    return float(
        np.sum(
            probability[positive]
            * np.log2(probability[positive] / reference[positive])
        )
    )


def audit_recoupling_mutual_information_finite(
    n: int,
    *,
    tolerance: float = 2e-9,
) -> RecouplingMutualInformationFiniteControl:
    if not 3 <= n <= 5:
        raise ValueError("exact entropy controls require 3<=n<=5")
    _partitions, _likelihood, reference, physical = (
        finite_physical_likelihood_arrays(n)
    )
    one_label_reference = np.sum(reference, axis=(1, 2, 3, 4, 5))
    outer_reference = np.einsum(
        "a,b,c,l->abcl",
        one_label_reference,
        one_label_reference,
        one_label_reference,
        one_label_reference,
    )
    outer_physical = np.sum(physical, axis=(3, 4))
    outer_kl = relative_entropy_bits(outer_physical, outer_reference)

    average_mi = 0.0
    average_left = 0.0
    average_right = 0.0
    q_product = np.einsum(
        "m,n->mn", one_label_reference, one_label_reference
    )
    for outer_indices in np.ndindex(outer_physical.shape):
        outer_mass = float(outer_physical[outer_indices])
        if outer_mass <= 0:
            continue
        alpha, beta, gamma, final = outer_indices
        coupling = physical[
            alpha,
            beta,
            gamma,
            :,
            :,
            final,
        ] / outer_mass
        left = np.sum(coupling, axis=1)
        right = np.sum(coupling, axis=0)
        product_marginals = np.einsum("m,n->mn", left, right)
        average_mi += outer_mass * relative_entropy_bits(
            coupling, product_marginals
        )
        average_left += outer_mass * relative_entropy_bits(
            left, one_label_reference
        )
        average_right += outer_mass * relative_entropy_bits(
            right, one_label_reference
        )
        # This direct identity catches axis-order mistakes locally.
        joint_kl = relative_entropy_bits(coupling, q_product)
        local_chain = (
            relative_entropy_bits(coupling, product_marginals)
            + relative_entropy_bits(left, one_label_reference)
            + relative_entropy_bits(right, one_label_reference)
        )
        if abs(joint_kl - local_chain) > 100 * tolerance:
            raise AssertionError("conditional Racah KL chain failed")

    full_kl = relative_entropy_bits(physical, reference)
    full_residual = abs(
        full_kl - outer_kl - average_mi - average_left - average_right
    )
    left_five_physical = np.sum(physical, axis=4)
    left_five_reference = np.sum(reference, axis=4)
    right_five_physical = np.sum(physical, axis=3)
    right_five_reference = np.sum(reference, axis=3)
    left_five_kl = relative_entropy_bits(
        left_five_physical, left_five_reference
    )
    right_five_kl = relative_entropy_bits(
        right_five_physical, right_five_reference
    )
    left_chain_residual = abs(left_five_kl - outer_kl - average_left)
    right_chain_residual = abs(right_five_kl - outer_kl - average_right)
    five_chi = float(source_averaged_conditional_chi_square(n))
    five_upper = math.log2(1.0 + five_chi)
    five_violation = max(
        0.0,
        left_five_kl - five_upper,
        right_five_kl - five_upper,
    )
    remainder = full_kl - average_mi
    remainder_formula = left_five_kl + right_five_kl - outer_kl
    remainder_residual = abs(remainder - remainder_formula)
    _orbits, _coarse_likelihood, coarse_reference, coarse_physical = (
        aggregate_sign_orbit_law(n)
    )
    coarse_kl = relative_entropy_bits(coarse_physical, coarse_reference)
    coarse_slack = full_kl - coarse_kl
    exact = bool(
        full_residual <= tolerance
        and left_chain_residual <= tolerance
        and right_chain_residual <= tolerance
        and five_violation <= tolerance
        and remainder_residual <= tolerance
        and coarse_slack >= -tolerance
    )
    return RecouplingMutualInformationFiniteControl(
        n=n,
        full_six_label_kl_bits=full_kl,
        outer_four_label_kl_bits=outer_kl,
        physical_average_recoupling_mutual_information_bits=average_mi,
        physical_average_left_marginal_kl_bits=average_left,
        physical_average_right_marginal_kl_bits=average_right,
        full_kl_chain_residual_bits=full_residual,
        left_five_label_kl_bits=left_five_kl,
        right_five_label_kl_bits=right_five_kl,
        left_five_label_chain_residual_bits=left_chain_residual,
        right_five_label_chain_residual_bits=right_chain_residual,
        exact_five_label_chi_square=five_chi,
        five_label_kl_upper_bits=five_upper,
        maximum_five_label_kl_bound_violation_bits=five_violation,
        non_mutual_information_remainder_bits=remainder,
        exact_non_mi_remainder_formula_residual_bits=remainder_residual,
        coarse_transpose_orbit_kl_bits=coarse_kl,
        full_to_coarse_kl_contraction_slack_bits=coarse_slack,
        exact_recoupling_mutual_information_reduction_verified=exact,
        status=(
            "six-label-entropy-is-racah-mutual-information-plus-five-label-remainder"
            if exact
            else "recoupling-mutual-information-control-failure"
        ),
    )


def recoupling_entropy_scaling_control(n: int) -> RecouplingEntropyScalingControl:
    if n < 16:
        raise ValueError("scaling control uses the n>=16 five-label bound")
    five = source_conditioned_channel_scaling_record(n)
    chi_upper = five.source_averaged_chi_square_upper_bound
    remainder_upper = 2.0 * math.log2(1.0 + chi_upper)
    return RecouplingEntropyScalingControl(
        n=n,
        five_label_chi_square_upper=chi_upper,
        non_mutual_information_remainder_upper_bits=remainder_upper,
        remainder_asymptotically_vanishing=True,
        physical_average_racah_mutual_information_sublogarithmic_proved=False,
        status="non-racah-six-label-entropy-remainder-vanishing",
    )


def marginally_perfect_mutual_information_countermodel(
    n: int,
) -> MarginallyPerfectMutualInformationCountermodel:
    if n < 2:
        raise ValueError("countermodel requires n>=2")
    order = math.factorial(n)
    probabilities = [
        hook_length_dimension(partition) ** 2 / order
        for partition in integer_partitions(n)
    ]
    entropy = -sum(
        probability * math.log2(probability)
        for probability in probabilities
        if probability > 0
    )
    return MarginallyPerfectMutualInformationCountermodel(
        n=n,
        partition_count=len(probabilities),
        plancherel_entropy_bits=entropy,
        plancherel_entropy_over_log2_n=entropy / math.log2(n),
        row_marginal_kl_to_plancherel_bits=0.0,
        column_marginal_kl_to_plancherel_bits=0.0,
        identity_block_mutual_information_bits=entropy,
        asymptotic_superlogarithmic_information_certified=True,
        status="perfect-plancherel-marginals-permit-superlog-racah-information",
    )


def run_recoupling_mutual_information_reduction(
) -> RecouplingMutualInformationReport:
    controls = [
        audit_recoupling_mutual_information_finite(n) for n in range(3, 6)
    ]
    scaling = [
        recoupling_entropy_scaling_control(n)
        for n in (16, 20, 24, 30, 40, 50)
    ]
    countermodels = [
        marginally_perfect_mutual_information_countermodel(n)
        for n in (5, 10, 20, 30, 40, 50)
    ]
    failures = sum(
        not row.exact_recoupling_mutual_information_reduction_verified
        for row in controls
    )
    exact = failures == 0 and all(
        row.remainder_asymptotically_vanishing for row in scaling
    )
    theorem = RecouplingMutualInformationTheorem(
        exact_kl_chain=(
            "D(P6||q6)=D(Pouter||q4)+E[I_pi+D(p||q)+D(r||q)]"
        ),
        five_label_remainder_bound=(
            "0<=D(P6||q6)-E I_pi<=2log2(1+V5_n)=o(1)"
        ),
        asymptotic_identity="D(P6||q6)=E_(Pouter)I_pi(mu;nu)+o(1)",
        sufficient_rank_transfer_condition="E_(Pouter)I_pi(mu;nu)=o(log n)",
        condition_weaker_than_subpolynomial_collision=True,
        natural_racah_mutual_information_sublogarithmic_proved=False,
        status=(
            "physical-rank-entropy-reduced-to-natural-racah-mutual-information"
            if exact
            else "recoupling-mutual-information-reduction-failure"
        ),
    )
    return RecouplingMutualInformationReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_chain": theorem.exact_kl_chain,
            "vanishing_remainder": theorem.five_label_remainder_bound,
            "asymptotic_target": theorem.asymptotic_identity,
            "rank_sufficient_condition": theorem.sufficient_rank_transfer_condition,
            "coarse_transfer": (
                "D(coarse transpose-orbit law)<=D(full six-partition law)."
            ),
            "scope": (
                "This is a rank-entropy reduction. It does not control conditional "
                "orientation-syndrome Racah CMI or construct a measurement."
            ),
        },
        theorem=theorem,
        exact_controls=controls,
        scaling_controls=scaling,
        marginal_countermodels=countermodels,
        literature_basis=[
            {
                "id": "source-conditioned-five-label-decoupling",
                "applicable": True,
                "precise_use": (
                    "Every tetrahedral edge-deleted five-label marginal has common "
                    "chi-square V5_n=o(1)."
                ),
            },
            {
                "id": "vershik-kerov-maximal-irrep-dimension",
                "applicable": True,
                "precise_use": (
                    "The maximal Plancherel atom is exp(-Omega(sqrt(n))), so the "
                    "identity-block countermodel has entropy Omega(sqrt(n))."
                ),
            },
            {
                "id": "christandl-sahinoglu-walter-recoupling-2016",
                "url": "https://arxiv.org/abs/1210.0463",
                "applicable": False,
                "precise_use": (
                    "Its bounded-row asymptotics do not prove the required average "
                    "mutual-information estimate for Plancherel shapes."
                ),
            },
        ],
        proof_obligations=[
            {
                "obligation": "derive_exact_racah_mutual_information_kl_chain",
                "resolved": exact,
                "resolution": (
                    "Condition on outer labels and apply the KL product-family "
                    "information projection to the recoupling coupling."
                ),
            },
            {
                "obligation": "prove_all_non_mi_entropy_terms_vanish",
                "resolved": exact,
                "resolution": (
                    "Two five-label KL bounds dominate the outer and marginal terms."
                ),
            },
            {
                "obligation": "prove_physical_average_natural_racah_mi_sublogarithmic",
                "resolved": False,
                "resolution": (
                    "Establish growing-row 6j entropic delocalization under the "
                    "physical outer-label law, allowing collision-heavy rare tails."
                ),
            },
            {
                "obligation": "separate_any_surviving_racah_mi_from_classical_access",
                "resolved": False,
                "resolution": (
                    "A positive lower bound must be paired with a coherent estimator "
                    "and same-access classical baseline."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The Renyi collision target is necessary for rank transfer.",
                "resolved": True,
                "resolution": (
                    "False. Direct entropy needs only average Racah MI=o(log n), even "
                    "when the collision norm has rare large spikes."
                ),
            },
            {
                "objection": "Five-label mixing already makes mu and nu independent.",
                "resolved": True,
                "resolution": (
                    "It fixes each marginal after outer averaging; dependence can "
                    "survive after conditioning on all four outer labels."
                ),
            },
            {
                "objection": "Exact Plancherel marginals force small mutual information.",
                "resolved": True,
                "resolution": (
                    "The identity-block coupling has exact marginals and mutual "
                    "information equal to the superlogarithmic Plancherel entropy."
                ),
            },
            {
                "objection": "Sublogarithmic full-label entropy proves an algorithm.",
                "resolved": True,
                "resolution": (
                    "It removes a rank-only signal and leaves coherent non-Haar Racah "
                    "syndrome information unresolved."
                ),
            },
        ],
        headline_metrics={
            "racah_mutual_information_kl_chain_theorem_count": int(exact),
            "non_mi_entropy_remainder_decay_theorem_count": int(exact),
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "rank_marginal_mi_counterexample_count": len(countermodels),
            "natural_racah_mi_sublogarithmic_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "six_label_kl_is_average_racah_mi_plus_o_one_proved": exact,
            "coarse_rank_entropy_sublog_if_average_racah_mi_sublog_proved": exact,
            "subpolynomial_collision_required_for_rank_transfer": False,
            "natural_physical_average_racah_mi_sublogarithmic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_orientation_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All rank-entropy terms except growing-row natural recoupling mutual "
                "information vanish, but that average has no asymptotic bound."
            ),
        },
        status=(
            "rank-entropy-target-is-sublog-natural-racah-mutual-information"
            if exact
            else "recoupling-mutual-information-control-failure"
        ),
        summary=(
            "Reduced full six-label entropy, up to o(1), to mutual information in "
            "the squared natural Racah block coupling."
        ),
        falsifiers_triggered=[
            "Collision-heavy tails need not block the weaker direct-entropy route.",
            "Five-label decoupling does not imply outer-conditioned recoupling independence.",
            "Perfect Plancherel marginals can coexist with superlogarithmic coupling information.",
        ],
    )


def write_recoupling_mutual_information_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_recoupling_mutual_information_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_recoupling_mutual_information_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
