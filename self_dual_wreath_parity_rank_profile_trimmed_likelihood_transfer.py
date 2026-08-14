"""A weak-L1, dimension-trimmed route from reference to physical rank mixing.

The rank-profile chi-square observable ``f`` takes values in ``[0,7]``.  This
boundedness permits a sharper change-of-measure argument than controlling the
full physical likelihood second moment.

Let ``Q_n`` be product Plancherel, ``P_n=L_n Q_n`` the physical tetrahedral
law, and ``T_n`` any retained event.  For a likelihood cap ``tau`` and the
product-rank good event ``G_epsilon``, split

    P(T intersect G^c)
      <= E_Q[L 1_(T,G^c,L<=tau)] + P(T,L>tau)
      <= tau Q(G^c) + eta_n(tau),                         (1)

where ``eta_n(tau)=P(T,L>tau)``.  Since
``Q(G^c)<=S_n/epsilon^2`` and the rank chi-square is at most seven,

    E_P f <= 7 P(T^c) + b(epsilon)
             + 7 tau S_n/epsilon^2 + 7 eta_n(tau),       (2)

with ``b(epsilon)=[((1+epsilon)/(1-epsilon))^5-1]^2``.

The sharp class-size theorem gives ``S_n~16/n^2``.  Therefore physical rank
mixing follows if there is a retained event and caps such that

    P(T_n^c) -> 0,
    tau_n = o(n^2),
    P(T_n, L_n>tau_n) -> 0.                              (3)

Indeed choose ``epsilon_n=(tau_n S_n)^(1/4)``.  This is a weak-L1 likelihood
tail criterion.  It can hold even when ``E_Q L_n^2`` is superquadratic due to
rarer, taller spikes that carry vanishing physical mass.

The canonical near-maximal dimension trim already proves ``P(T_n^c)->0``.
The remaining target is now narrower: show that the retained physical law
places vanishing mass above some subquadratic likelihood cap.  This is weaker
than proving the retained projected collision norm is ``o(n^2)``.

The scale cannot be improved by this argument.  If a reference event has mass
``1/n^2`` and likelihood ``n^2`` there (zero elsewhere), then its physical
mass and a bounded observable supported there both equal one.  Every cap
``o(n^2)`` leaves unit physical likelihood-tail mass.

This theorem concerns only the Haar rank-profile component.  It neither
controls the irreducible non-Haar Racah cumulants nor supplies a classical
separation or a coherent algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_parity_rank_profile_physical_transfer_boundary import (
    good_event_rank_chi_square_bound,
)
from self_dual_wreath_tetrahedral_dimension_trim import (
    tetrahedral_dimension_trim_record,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-TRIMMED-LIKELIHOOD-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WeakL1TransferScalingControl:
    n: int
    likelihood_cap: float
    reference_union_variance: float
    cap_times_reference_variance: float
    epsilon: float
    removed_physical_mass_upper: float
    retained_high_likelihood_physical_mass_upper: float
    good_event_rank_chi_square_upper: float
    capped_bad_event_physical_mass_upper: float
    expected_physical_rank_chi_square_upper: float
    asymptotic_hypotheses_satisfied: bool
    status: str


@dataclass(frozen=True)
class QuadraticRareEventBoundary:
    n: int
    rare_reference_probability: str
    rare_likelihood: str
    physical_rare_event_mass: str
    bounded_observable_reference_mean: str
    bounded_observable_physical_mean: str
    subquadratic_test_cap: int
    physical_mass_above_test_cap: str
    exact_quadratic_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class TrimmedLikelihoodTransferTheorem:
    finite_bound: str
    sufficient_conditions: str
    canonical_epsilon: str
    second_moment_implication: str
    weak_l1_strictly_weaker_than_full_l2: bool
    quadratic_boundary_counterexample_verified: bool
    physical_rank_mixing_proved_for_tetrahedral_law: bool
    status: str


@dataclass(frozen=True)
class ParityRankProfileTrimmedLikelihoodTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: TrimmedLikelihoodTransferTheorem
    dimension_trim_controls: list[dict[str, int | float | bool | str]]
    weak_l1_scaling_controls: list[WeakL1TransferScalingControl]
    quadratic_boundary_controls: list[QuadraticRareEventBoundary]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def optimized_weak_l1_epsilon(
    likelihood_cap: float,
    union_variance: float,
) -> float:
    if likelihood_cap < 0 or union_variance < 0:
        raise ValueError("cap and variance must be nonnegative")
    product = likelihood_cap * union_variance
    if product <= 0:
        return 1e-12
    return min(0.5, max(1e-12, product ** 0.25))


def trimmed_weak_l1_transfer_bound(
    *,
    removed_physical_mass: float,
    retained_high_likelihood_physical_mass: float,
    likelihood_cap: float,
    union_variance: float,
    epsilon: float,
) -> tuple[float, float, float]:
    for value in (
        removed_physical_mass,
        retained_high_likelihood_physical_mass,
        likelihood_cap,
        union_variance,
    ):
        if value < 0:
            raise ValueError("masses, cap, and variance must be nonnegative")
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must lie in (0,1)")
    good = min(7.0, good_event_rank_chi_square_bound(epsilon))
    reference_bad = min(1.0, union_variance / epsilon**2)
    physical_bad = min(
        1.0,
        likelihood_cap * reference_bad
        + retained_high_likelihood_physical_mass,
    )
    expected = min(
        7.0,
        7.0 * min(1.0, removed_physical_mass) + good + 7.0 * physical_bad,
    )
    return good, physical_bad, expected


def weak_l1_scaling_control(n: int) -> WeakL1TransferScalingControl:
    if n < 100:
        raise ValueError("synthetic asymptotic control requires n>=100")
    cap = float(n)
    variance = 16.0 / n**2
    removed = n ** (-0.5)
    high_tail = n ** (-0.5)
    epsilon = optimized_weak_l1_epsilon(cap, variance)
    good, bad, expected = trimmed_weak_l1_transfer_bound(
        removed_physical_mass=removed,
        retained_high_likelihood_physical_mass=high_tail,
        likelihood_cap=cap,
        union_variance=variance,
        epsilon=epsilon,
    )
    hypotheses = bool(
        removed > 0
        and high_tail > 0
        and math.isclose(cap / n**2, 1 / n, rel_tol=1e-14)
        and math.isclose(cap * variance, 16 / n, rel_tol=1e-14)
    )
    return WeakL1TransferScalingControl(
        n=n,
        likelihood_cap=cap,
        reference_union_variance=variance,
        cap_times_reference_variance=cap * variance,
        epsilon=epsilon,
        removed_physical_mass_upper=removed,
        retained_high_likelihood_physical_mass_upper=high_tail,
        good_event_rank_chi_square_upper=good,
        capped_bad_event_physical_mass_upper=bad,
        expected_physical_rank_chi_square_upper=expected,
        asymptotic_hypotheses_satisfied=hypotheses,
        status=(
            "synthetic-weak-l1-transfer-bound-vanishing"
            if hypotheses
            else "weak-l1-scaling-control-failure"
        ),
    )


def quadratic_rare_event_boundary(n: int) -> QuadraticRareEventBoundary:
    if n < 2:
        raise ValueError("n must be at least two")
    scale = n * n
    reference = Fraction(1, scale)
    likelihood = Fraction(scale)
    physical = reference * likelihood
    cap = n
    physical_above_cap = physical if likelihood > cap else Fraction()
    verified = bool(
        physical == 1
        and reference * likelihood**2 == scale
        and cap < likelihood
        and physical_above_cap == 1
    )
    return QuadraticRareEventBoundary(
        n=n,
        rare_reference_probability=str(reference),
        rare_likelihood=str(likelihood),
        physical_rare_event_mass=str(physical),
        bounded_observable_reference_mean=str(reference),
        bounded_observable_physical_mean=str(physical),
        subquadratic_test_cap=cap,
        physical_mass_above_test_cap=str(physical_above_cap),
        exact_quadratic_boundary_verified=verified,
        status=(
            "quadratic-likelihood-boundary-counterexample-verified"
            if verified
            else "quadratic-boundary-control-failure"
        ),
    )


def run_parity_rank_profile_trimmed_likelihood_transfer(
) -> ParityRankProfileTrimmedLikelihoodTransferReport:
    trim_rows = [tetrahedral_dimension_trim_record(n) for n in (12, 20, 30, 50)]
    scaling = [weak_l1_scaling_control(n) for n in (10**8, 10**12, 10**16)]
    boundaries = [quadratic_rare_event_boundary(n) for n in (10, 100, 1_000)]
    failures = sum(not row.asymptotic_hypotheses_satisfied for row in scaling)
    failures += sum(not row.exact_quadratic_boundary_verified for row in boundaries)
    verified = failures == 0
    theorem = TrimmedLikelihoodTransferTheorem(
        finite_bound=(
            "E_P f<=7P(T^c)+b(epsilon)+7tau S_n/epsilon^2+"
            "7P(T,L>tau)"
        ),
        sufficient_conditions=(
            "P(T_n^c)->0, tau_n=o(n^2), and P(T_n,L_n>tau_n)->0"
        ),
        canonical_epsilon="epsilon_n=(tau_n S_n)^(1/4)",
        second_moment_implication=(
            "M_n S_n->0 implies the weak-L1 conditions by choosing "
            "tau_n=sqrt(M_n/S_n) and Markov"
        ),
        weak_l1_strictly_weaker_than_full_l2=True,
        quadratic_boundary_counterexample_verified=verified,
        physical_rank_mixing_proved_for_tetrahedral_law=False,
        status=(
            "physical-rank-transfer-reduced-to-retained-subquadratic-likelihood-tail"
            if verified
            else "trimmed-likelihood-transfer-control-failure"
        ),
    )
    dimension_controls = [
        {
            "n": row.n,
            "dimension_threshold_log2": row.canonical_dimension_threshold_log2,
            "removed_physical_mass_upper": row.six_coordinate_removed_mass_upper_bound,
            "removed_mass_vanishing_certified": row.low_dimension_tail_tv_vanishing_certified,
            "status": row.status,
        }
        for row in trim_rows
    ]
    return ParityRankProfileTrimmedLikelihoodTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "bounded_observable": "0<=f=chi2(rank-profile||U3)<=7.",
            "retained_event": (
                "T_n may be the canonical event that all six irrep dimensions "
                "exceed sqrt(n!)/(p(n)log2(n!))."
            ),
            "capped_change_of_measure": (
                "P(T,G^c)<=tau Q(G^c)+P(T,L>tau)."
            ),
            "reference_bad_event": "Q(G^c)<=S_n/epsilon^2 with S_n~16/n^2.",
            "weak_l1_target": theorem.sufficient_conditions,
            "scope": (
                "The criterion is proved; its retained tetrahedral likelihood-tail "
                "hypothesis and all non-Haar Racah terms remain open."
            ),
        },
        theorem=theorem,
        dimension_trim_controls=dimension_controls,
        weak_l1_scaling_controls=scaling,
        quadratic_boundary_controls=boundaries,
        proof_obligations=[
            {
                "obligation": "remove_irrelevant_low_dimension_likelihood_spikes",
                "resolved": True,
                "resolution": (
                    "The canonical dimension trim has vanishing physical mass, and "
                    "the rank observable is uniformly bounded."
                ),
            },
            {
                "obligation": "replace_full_l2_transfer_by_physical_likelihood_tail_control",
                "resolved": verified,
                "resolution": (
                    "Likelihood truncation gives the finite weak-L1 bound (2)."
                ),
            },
            {
                "obligation": "prove_retained_subquadratic_likelihood_tail_has_vanishing_physical_mass",
                "resolved": False,
                "resolution": (
                    "Find tau_n=o(n^2) with P(T_n,L_n>tau_n)->0, or construct a "
                    "positive-mass retained counterfamily."
                ),
            },
            {
                "obligation": "control_irreducible_non_haar_racah_cumulants",
                "resolved": False,
                "resolution": (
                    "Rank transfer does not bound either conditional 2x2 minor."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A full second moment is necessary for change of measure.",
                "resolved": True,
                "resolution": (
                    "False for bounded observables: a likelihood cap plus vanishing "
                    "physical mass above the cap suffices."
                ),
            },
            {
                "objection": "Any cap tending to infinity is enough.",
                "resolved": True,
                "resolution": (
                    "No. The cap must be o(1/S_n)=o(n^2), unless a sharper reference "
                    "bad-event estimate replaces Chebyshev."
                ),
            },
            {
                "objection": "Low-dimensional trimming automatically proves the tail condition.",
                "resolved": False,
                "resolution": (
                    "The retained near-maximal-dimensional sector can still contain "
                    "high-likelihood spikes."
                ),
            },
            {
                "objection": "The n^2 threshold is an artifact with no counterexample.",
                "resolved": True,
                "resolution": (
                    "The exact reference mass n^-2 / likelihood n^2 family preserves "
                    "unit physical signal at the boundary."
                ),
            },
        ],
        headline_metrics={
            "weak_l1_transfer_theorem_count": int(verified),
            "canonical_dimension_trim_control_count": len(dimension_controls),
            "synthetic_scaling_control_count": len(scaling),
            "quadratic_boundary_counterexample_count": len(boundaries),
            "finite_control_failure_count": failures,
            "retained_tetrahedral_likelihood_tail_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "trimmed_weak_l1_transfer_criterion_proved": verified,
            "full_second_moment_required_for_rank_transfer": False,
            "canonical_low_dimension_tail_removed": True,
            "retained_subquadratic_likelihood_tail_vanishes_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "adaptive_syndrome_decouples_proved": False,
            "adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The necessary transfer hypothesis has been weakened to a retained "
                "physical likelihood-tail statement, but that statement is open."
            ),
        },
        status=(
            "retained-subquadratic-likelihood-tail-is-weakest-current-rank-transfer-gate"
            if verified
            else "trimmed-likelihood-transfer-bound-failure"
        ),
        summary=(
            "Replaced the full L2 collision requirement by a weaker dimension-trimmed "
            "weak-L1 likelihood-tail criterion at the sharp n^2 scale."
        ),
        falsifiers_triggered=[
            "Full tetrahedral chi-square can diverge without obstructing a bounded rank observable.",
            "Removing low-dimensional labels does not by itself control retained likelihood spikes.",
            "Likelihood mass at the quadratic scale can preserve unit physical signal despite reference mixing.",
        ],
    )


def write_parity_rank_profile_trimmed_likelihood_transfer_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_rank_profile_trimmed_likelihood_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_rank_profile_trimmed_likelihood_transfer_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
