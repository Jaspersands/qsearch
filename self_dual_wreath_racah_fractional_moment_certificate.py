"""Fractional-moment certificates for physical-average Racah information.

For an outer-label tuple ``o``, let ``pi_o`` be the natural Racah coupling,
``sigma_o=p_o tensor r_o`` its rank-product coupling, and
``a_o=pi_o/sigma_o``.  For every ``theta>0`` define

    S_theta(o) = sum_(mu,nu) pi_o a_o^theta
               = sum sigma_o a_o^(1+theta).               (1)

Monotonicity of Renyi divergence and Jensen's inequality give

    E_o I(pi_o)
      <= (1/theta) E_o log2 S_theta(o)
      <= (1/theta) log2 E_o S_theta(o).                   (2)

Thus, for a possibly vanishing sequence ``theta_n``, it is sufficient that

    log E_o S_(theta_n)(o) = o(theta_n log n).             (3)

This is strictly more tail-tolerant than requiring a subpolynomial collision
moment ``S_1``.  It is not free: taking ``theta_n`` too small simply makes
the ``1/theta_n`` prefactor expose the original Shannon-information problem.

The same moment controls the relative-overlap tail.  For ``K>=1``,

    E_o pi_o{a_o>K} <= K^-theta E_o S_theta(o).            (4)

Combining (4) with the entropic tail certificate provides an independent
check that the support entropy ``2 log p(n)`` has been paid.

For Racah blocks of Hilbert--Schmidt mass ``x_(mu,nu)``, ranks ``l_mu,r_nu``
and total multiplicity ``M``, the exact representation-theoretic target is

    S_theta(o)
      = M^(theta-1) sum_(mu,nu)
          x_(mu,nu)^(1+theta)/(l_mu r_nu)^theta.           (5)

No natural growing-row bound on (5) is proved here.
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
from self_dual_wreath_character_triangle_barrier import partition_number
from self_dual_wreath_racah_entropic_delocalization_certificate import (
    entropic_tail_upper_bits,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_racah_fractional_moment_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-RACAH-FRACTIONAL-MOMENT-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PhysicalAverageFractionalMomentControl:
    n: int
    fractional_order_theta: float
    relative_overlap_threshold: float
    positive_outer_tuple_count: int
    physical_outer_probability_sum: float
    physical_average_racah_mutual_information_bits: float
    physical_average_fractional_moment: float
    averaged_fractional_renyi_upper_bits: float
    renyi_upper_violation_bits: float
    physical_average_actual_bad_mass: float
    moment_bad_mass_upper: float
    bad_mass_bound_violation: float
    actual_tail_entropy_upper_bits: float
    moment_tail_entropy_upper_bits: float
    exact_fractional_certificate_verified: bool
    status: str


@dataclass(frozen=True)
class IdentityCouplingFractionalCountermodel:
    n: int
    fractional_order_theta: float
    partition_count: int
    plancherel_entropy_bits: float
    exact_fractional_dependence_moment: float
    fractional_renyi_upper_bits: float
    exact_collision_moment: float
    perfect_marginals_imply_fractional_bound: bool
    status: str


@dataclass(frozen=True)
class SyntheticFractionalScalingControl:
    n: int
    fractional_order_theta: float
    synthetic_average_fractional_moment: float
    synthetic_fractional_renyi_upper_bits: float
    upper_over_log2_n: float
    sufficient_rate_verified: bool
    natural_fractional_moment_bound_proved: bool
    status: str


@dataclass(frozen=True)
class RacahFractionalMomentTheorem:
    conditional_moment: str
    averaged_renyi_bound: str
    averaged_tail_bound: str
    block_mass_formula: str
    sufficient_asymptotic_condition: str
    natural_condition_proved: bool
    status: str


@dataclass(frozen=True)
class RacahFractionalMomentReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: RacahFractionalMomentTheorem
    finite_physical_average_controls: list[PhysicalAverageFractionalMomentControl]
    identity_coupling_countermodels: list[IdentityCouplingFractionalCountermodel]
    synthetic_scaling_controls: list[SyntheticFractionalScalingControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def averaged_fractional_renyi_upper_bits(
    average_fractional_moment: float,
    theta: float,
) -> float:
    if theta <= 0 or average_fractional_moment < 1:
        raise ValueError("require theta>0 and a dependence moment at least one")
    return math.log2(average_fractional_moment) / theta


def fractional_moment_bad_mass_upper(
    average_fractional_moment: float,
    theta: float,
    relative_overlap_threshold: float,
) -> float:
    if theta <= 0 or relative_overlap_threshold < 1:
        raise ValueError("require theta>0 and K>=1")
    if average_fractional_moment < 1:
        raise ValueError("a dependence moment must be at least one")
    return min(
        1.0,
        average_fractional_moment / relative_overlap_threshold**theta,
    )


def audit_physical_average_fractional_moment(
    n: int,
    theta: float,
    relative_overlap_threshold: float,
    *,
    tolerance: float = 3e-9,
) -> PhysicalAverageFractionalMomentControl:
    if not 3 <= n <= 5 or theta <= 0 or relative_overlap_threshold < 1:
        raise ValueError("finite controls require 3<=n<=5, theta>0 and K>=1")
    partitions, _likelihood, _reference, physical = (
        finite_physical_likelihood_arrays(n)
    )
    outer_physical = np.sum(physical, axis=(3, 4))
    average_information = 0.0
    average_moment = 0.0
    average_bad = 0.0
    positive_outer = 0
    for outer_indices in np.ndindex(outer_physical.shape):
        outer_mass = float(outer_physical[outer_indices])
        if outer_mass <= 0:
            continue
        positive_outer += 1
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
        product = np.einsum("m,n->mn", left, right)
        positive = coupling > 0
        ratio = np.zeros_like(coupling)
        ratio[positive] = coupling[positive] / product[positive]
        average_information += outer_mass * float(
            np.sum(coupling[positive] * np.log2(ratio[positive]))
        )
        average_moment += outer_mass * float(
            np.sum(coupling[positive] * ratio[positive] ** theta)
        )
        average_bad += outer_mass * float(
            np.sum(coupling[ratio > relative_overlap_threshold])
        )
    average_probability = float(np.sum(outer_physical))
    renyi_upper = averaged_fractional_renyi_upper_bits(average_moment, theta)
    moment_bad_upper = fractional_moment_bad_mass_upper(
        average_moment,
        theta,
        relative_overlap_threshold,
    )
    actual_tail_upper = entropic_tail_upper_bits(
        len(partitions),
        relative_overlap_threshold,
        average_bad,
    )
    moment_tail_upper = entropic_tail_upper_bits(
        len(partitions),
        relative_overlap_threshold,
        moment_bad_upper,
    )
    renyi_violation = max(0.0, average_information - renyi_upper)
    bad_violation = max(0.0, average_bad - moment_bad_upper)
    exact = bool(
        abs(average_probability - 1.0) <= tolerance
        and average_moment >= 1 - tolerance
        and renyi_violation <= tolerance
        and bad_violation <= tolerance
        and average_information <= actual_tail_upper + tolerance
        and average_information <= moment_tail_upper + tolerance
    )
    return PhysicalAverageFractionalMomentControl(
        n=n,
        fractional_order_theta=theta,
        relative_overlap_threshold=relative_overlap_threshold,
        positive_outer_tuple_count=positive_outer,
        physical_outer_probability_sum=average_probability,
        physical_average_racah_mutual_information_bits=average_information,
        physical_average_fractional_moment=average_moment,
        averaged_fractional_renyi_upper_bits=renyi_upper,
        renyi_upper_violation_bits=renyi_violation,
        physical_average_actual_bad_mass=average_bad,
        moment_bad_mass_upper=moment_bad_upper,
        bad_mass_bound_violation=bad_violation,
        actual_tail_entropy_upper_bits=actual_tail_upper,
        moment_tail_entropy_upper_bits=moment_tail_upper,
        exact_fractional_certificate_verified=exact,
        status=(
            "physical-average-racah-information-obeys-fractional-moment-certificate"
            if exact
            else "racah-fractional-moment-control-failure"
        ),
    )


def identity_coupling_fractional_countermodel(
    n: int,
    theta: float,
) -> IdentityCouplingFractionalCountermodel:
    if n < 2 or not 0 < theta <= 1:
        raise ValueError("countermodel requires n>=2 and 0<theta<=1")
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
    moment = sum(probability ** (1.0 - theta) for probability in probabilities)
    upper = math.log2(moment) / theta
    return IdentityCouplingFractionalCountermodel(
        n=n,
        fractional_order_theta=theta,
        partition_count=len(probabilities),
        plancherel_entropy_bits=entropy,
        exact_fractional_dependence_moment=moment,
        fractional_renyi_upper_bits=upper,
        exact_collision_moment=float(partition_number(n)),
        perfect_marginals_imply_fractional_bound=False,
        status="perfect-plancherel-marginals-permit-large-fractional-moments",
    )


def synthetic_fractional_scaling_control(
    n: int,
) -> SyntheticFractionalScalingControl:
    if n < 16:
        raise ValueError("synthetic scaling control requires n>=16")
    log_n = math.log2(n)
    theta = 1.0 / math.sqrt(log_n)
    moment = 2.0
    upper = averaged_fractional_renyi_upper_bits(moment, theta)
    ratio = upper / log_n
    sufficient = bool(
        math.isclose(upper, math.sqrt(log_n), rel_tol=1e-14)
        and ratio < 1
    )
    return SyntheticFractionalScalingControl(
        n=n,
        fractional_order_theta=theta,
        synthetic_average_fractional_moment=moment,
        synthetic_fractional_renyi_upper_bits=upper,
        upper_over_log2_n=ratio,
        sufficient_rate_verified=sufficient,
        natural_fractional_moment_bound_proved=False,
        status=(
            "synthetic-fractional-moment-rate-implies-sublog-racah-information"
            if sufficient
            else "synthetic-fractional-moment-rate-control-failure"
        ),
    )


def run_racah_fractional_moment_certificate() -> RacahFractionalMomentReport:
    finite = [
        audit_physical_average_fractional_moment(n, theta, threshold)
        for n, theta, threshold in (
            (3, 0.25, 2.0),
            (3, 0.5, 2.0),
            (4, 0.25, 2.0),
            (4, 0.5, 4.0),
            (5, 0.25, 2.0),
            (5, 0.5, 4.0),
            (5, 1.0, 4.0),
        )
    ]
    countermodels = [
        identity_coupling_fractional_countermodel(n, theta)
        for n in (10, 20, 30)
        for theta in (0.25, 0.5, 1.0)
    ]
    scaling = [
        synthetic_fractional_scaling_control(n)
        for n in (20, 50, 100, 1_000, 10_000, 1_000_000)
    ]
    failures = sum(not row.exact_fractional_certificate_verified for row in finite)
    failures += sum(not row.sufficient_rate_verified for row in scaling)
    verified = failures == 0
    theorem = RacahFractionalMomentTheorem(
        conditional_moment="S_theta(o)=sum pi_o(pi_o/(p_o tensor r_o))^theta",
        averaged_renyi_bound=(
            "E_o I(pi_o)<=theta^-1 log2(E_o S_theta(o))"
        ),
        averaged_tail_bound=(
            "E_o pi_o{a_o>K}<=K^-theta E_o S_theta(o)"
        ),
        block_mass_formula=(
            "S_theta=M^(theta-1)sum x_(mu,nu)^(1+theta)/(l_mu r_nu)^theta"
        ),
        sufficient_asymptotic_condition=(
            "there exists theta_n>0 with log(E S_theta_n)=o(theta_n log n)"
        ),
        natural_condition_proved=False,
        status=(
            "racah-rank-transfer-has-fractional-moment-certificate"
            if verified
            else "racah-fractional-moment-certificate-failure"
        ),
    )
    return RacahFractionalMomentReport(
        created_at=utc_now(),
        theorem_contract={
            "outer_law": "physical four-label marginal P_outer",
            "reference_coupling": "product of exact conditional rank marginals",
            "renyi_order": "1+theta, with theta allowed to depend on n",
            "collision_special_case": "theta=1",
            "shannon_limit_warning": (
                "theta->0 does not help unless log E S_theta=o(theta log n)"
            ),
            "scope": (
                "sufficient rank-entropy certificate; no natural moment estimate, "
                "orientation-syndrome theorem, compiler, or algorithm"
            ),
        },
        theorem=theorem,
        finite_physical_average_controls=finite,
        identity_coupling_countermodels=countermodels,
        synthetic_scaling_controls=scaling,
        proof_obligations=[
            {
                "obligation": "derive_physical_average_fractional_renyi_bound",
                "resolved": verified,
                "resolution": (
                    "Apply D_1<=D_(1+theta) conditionally and Jensen over physical outer labels."
                ),
            },
            {
                "obligation": "connect_fractional_moment_to_racah_block_masses",
                "resolved": verified,
                "resolution": (
                    "Substitute pi=x/M and p r=l r/M^2 into the dependence moment."
                ),
            },
            {
                "obligation": "bound_natural_growing_row_fractional_moment",
                "resolved": False,
                "resolution": (
                    "Prove the physical-average block-mass moment rate for some useful theta_n."
                ),
            },
            {
                "obligation": "control_fractional_moment_estimator_tail",
                "resolved": False,
                "resolution": (
                    "Any numerical estimator must report truncation, coverage, and confidence under rare large a."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Taking theta arbitrarily close to zero makes the theorem easy.",
                "resolved": True,
                "resolution": (
                    "False. The 1/theta factor requires the moment logarithm to shrink proportionally faster."
                ),
            },
            {
                "objection": "Perfect Plancherel rank marginals bound every fractional moment.",
                "resolved": True,
                "resolution": (
                    "The identity coupling has exact marginals and moment sum q_lambda^(1-theta)."
                ),
            },
            {
                "objection": "A finite estimate of S_theta is robust to missed blocks.",
                "resolved": True,
                "resolution": (
                    "Rare high-a blocks are amplified by a^theta; omitted physical mass needs an explicit upper bound."
                ),
            },
            {
                "objection": "Rank-information control resolves the full quantum signal.",
                "resolved": True,
                "resolution": (
                    "Orientation-syndrome conditional information remains a separate obligation."
                ),
            },
        ],
        headline_metrics={
            "fractional_moment_certificate_theorem_count": int(verified),
            "finite_physical_average_control_count": len(finite),
            "finite_control_failure_count": failures,
            "identity_coupling_countermodel_count": len(countermodels),
            "natural_fractional_moment_bound_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_average_fractional_renyi_certificate_proved": verified,
            "fractional_moment_tail_bound_proved": verified,
            "collision_subpolynomial_required": False,
            "natural_growing_row_fractional_moment_bound_proved": False,
            "natural_physical_average_racah_mi_sublogarithmic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_orientation_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A weaker continuum of sufficient moments is now exact, but no natural "
                "Plancherel-growing-row estimate is available at any useful order."
            ),
        },
        status=(
            "natural-racah-search-target-is-fractional-block-mass-moment"
            if verified
            else "racah-fractional-moment-certificate-failure"
        ),
        summary=(
            "Replaced collision-only rank transfer by an exact physical-average "
            "order-1+theta moment criterion with explicit tail accounting."
        ),
        falsifiers_triggered=[
            "Collision growth alone no longer kills the rank-mixing route if lower moments remain controlled.",
            "Vanishing Renyi order is not a loophole because its reciprocal enters the entropy bound.",
            "Marginal Plancherel mixing permits exponentially broad dependence moments.",
        ],
    )


def write_racah_fractional_moment_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_racah_fractional_moment_certificate())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_racah_fractional_moment_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
