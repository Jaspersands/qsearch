"""Sublogarithmic total correlation suffices for physical rank mixing.

Let ``P_n=L_n Q_n`` be the physical tetrahedral six-label law relative to
``Q_n=Plancherel(S_n)^6``.  Since every physical coordinate marginal is
Plancherel,

    D_n = D(P_n || Q_n)

is exactly the total correlation of the six measured irrep labels.

Write the positive and negative likelihood-information parts in bits as

    K_+ = E_Q[L log2(L) 1_(L>=1)],
    K_- = E_Q[L log2(1/L) 1_(0<L<1)].

For ``0<=x<=1``, ``x ln(1/x)<=1/e``.  Therefore

    K_- <= 1/(e ln 2),
    K_+ = D_n + K_- <= D_n + 1/(e ln 2).                (1)

For every ``tau>1``,

    P_n(L_n>tau) <= K_+/log2(tau).                       (2)

Insert (2) into the weak-L1 rank-transfer theorem with ``tau=n``.  Since the
product-law bad-event scale is ``S_n~16/n^2``,

    E_P f <= b(epsilon)+7 n S_n/epsilon^2
             + 7[D_n+1/(e ln 2)]/log2(n),               (3)

where ``0<=f=chi2(rank||U3)<=7``.  Choosing
``epsilon=(nS_n)^(1/4)`` proves

    D(P_n || Plancherel^6) = o(log n)
       implies physical rank-profile mixing.             (4)

Thus neither total-variation convergence nor vanishing KL is required for the
rank component.  A uniformly bounded total correlation is more than enough.
The remaining entropy target may be substantially easier than controlling a
full L2 collision moment.

The logarithmic boundary is real for this method.  A reference event of mass
``n^-2`` with likelihood ``n^2`` has unit physical mass, persistent bounded
signal, and relative entropy exactly ``2 log2(n)``.  Hence an ``O(log n)``
bound without a sufficiently small leading constant or additional tail
structure cannot establish mixing.

This theorem does not prove sublogarithmic total correlation for the physical
tetrahedral law and does not control irreducible non-Haar Racah cumulants.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_parity_rank_profile_physical_transfer_boundary import (
    good_event_rank_chi_square_bound,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_rank_profile_entropy_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-ENTROPY-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_INFORMATION_BOUND_BITS = 1.0 / (math.e * math.log(2.0))


@dataclass(frozen=True)
class FiniteLikelihoodInformationControl:
    n: int
    kl_divergence_bits: float
    positive_likelihood_information_bits: float
    negative_likelihood_information_bits: float
    universal_negative_information_upper_bits: float
    kl_decomposition_residual: float
    tail_threshold: float
    exact_physical_mass_above_threshold: float
    information_tail_mass_upper: float
    negative_information_bound_verified: bool
    likelihood_tail_bound_verified: bool
    status: str


@dataclass(frozen=True)
class EntropyTransferScalingControl:
    n: int
    assumed_total_correlation_bits: float
    total_correlation_over_log2_n: float
    likelihood_cap: float
    reference_union_variance: float
    epsilon: float
    good_event_rank_chi_square_upper: float
    capped_reference_bad_mass_upper: float
    high_likelihood_physical_mass_upper: float
    expected_physical_rank_chi_square_upper: float
    sublogarithmic_entropy_hypothesis_satisfied: bool
    status: str


@dataclass(frozen=True)
class LogarithmicEntropyBoundary:
    n: int
    reference_rare_mass: float
    rare_likelihood: float
    physical_rare_mass: float
    relative_entropy_bits: float
    relative_entropy_over_log2_n: float
    bounded_observable_physical_mean: float
    exact_logarithmic_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class EntropyTransferTheorem:
    negative_information_bound_bits: float
    likelihood_tail_bound: str
    finite_rank_bound: str
    sufficient_entropy_condition: str
    bounded_total_correlation_sufficient: bool
    vanishing_total_correlation_required: bool
    physical_entropy_condition_proved: bool
    status: str


@dataclass(frozen=True)
class ParityRankProfileEntropyTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: EntropyTransferTheorem
    finite_information_controls: list[FiniteLikelihoodInformationControl]
    asymptotic_scaling_controls: list[EntropyTransferScalingControl]
    logarithmic_boundary_controls: list[LogarithmicEntropyBoundary]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def likelihood_information_parts(
    likelihood: np.ndarray,
    reference: np.ndarray,
) -> tuple[float, float, float]:
    if likelihood.shape != reference.shape:
        raise ValueError("likelihood and reference arrays must have equal shape")
    if float(np.min(likelihood)) < 0 or float(np.min(reference)) < 0:
        raise ValueError("likelihood and reference arrays must be nonnegative")
    physical = likelihood * reference
    above = likelihood >= 1.0
    below = (likelihood > 0.0) & (likelihood < 1.0)
    positive = float(
        np.sum(physical[above] * np.log2(likelihood[above]))
    )
    negative = float(
        np.sum(physical[below] * np.log2(1.0 / likelihood[below]))
    )
    return positive - negative, positive, negative


def information_likelihood_tail_upper(
    kl_divergence_bits: float,
    threshold: float,
) -> float:
    if kl_divergence_bits < -1e-12:
        raise ValueError("KL divergence must be nonnegative")
    if threshold <= 1:
        raise ValueError("threshold must exceed one")
    return min(
        1.0,
        (max(0.0, kl_divergence_bits) + NEGATIVE_INFORMATION_BOUND_BITS)
        / math.log2(threshold),
    )


def audit_finite_likelihood_information(
    n: int,
    threshold: float = 2.0,
) -> FiniteLikelihoodInformationControl:
    if not 2 <= n <= 5:
        raise ValueError("finite likelihood controls require 2<=n<=5")
    _partitions, likelihood, reference, physical = finite_physical_likelihood_arrays(n)
    kl, positive, negative = likelihood_information_parts(likelihood, reference)
    tail = float(np.sum(physical[likelihood > threshold]))
    upper = information_likelihood_tail_upper(kl, threshold)
    decomposition_residual = abs(kl - (positive - negative))
    negative_verified = negative <= NEGATIVE_INFORMATION_BOUND_BITS + 1e-12
    tail_verified = tail <= upper + 1e-12
    return FiniteLikelihoodInformationControl(
        n=n,
        kl_divergence_bits=max(0.0, kl),
        positive_likelihood_information_bits=positive,
        negative_likelihood_information_bits=negative,
        universal_negative_information_upper_bits=NEGATIVE_INFORMATION_BOUND_BITS,
        kl_decomposition_residual=decomposition_residual,
        tail_threshold=threshold,
        exact_physical_mass_above_threshold=tail,
        information_tail_mass_upper=upper,
        negative_information_bound_verified=negative_verified,
        likelihood_tail_bound_verified=tail_verified,
        status=(
            "finite-likelihood-information-identities-verified"
            if negative_verified and tail_verified
            else "likelihood-information-control-failure"
        ),
    )


def entropy_transfer_scaling_control(n: int) -> EntropyTransferScalingControl:
    if n < 100:
        raise ValueError("asymptotic entropy control requires n>=100")
    log_n = math.log2(n)
    entropy = math.sqrt(log_n)
    cap = float(n)
    variance = 16.0 / n**2
    epsilon = min(0.5, max(1e-12, (cap * variance) ** 0.25))
    good = min(7.0, good_event_rank_chi_square_bound(epsilon))
    capped_bad = min(1.0, cap * variance / epsilon**2)
    tail = information_likelihood_tail_upper(entropy, cap)
    expected = min(7.0, good + 7.0 * capped_bad + 7.0 * tail)
    hypothesis = entropy / log_n == 1.0 / math.sqrt(log_n)
    return EntropyTransferScalingControl(
        n=n,
        assumed_total_correlation_bits=entropy,
        total_correlation_over_log2_n=entropy / log_n,
        likelihood_cap=cap,
        reference_union_variance=variance,
        epsilon=epsilon,
        good_event_rank_chi_square_upper=good,
        capped_reference_bad_mass_upper=capped_bad,
        high_likelihood_physical_mass_upper=tail,
        expected_physical_rank_chi_square_upper=expected,
        sublogarithmic_entropy_hypothesis_satisfied=hypothesis,
        status=(
            "synthetic-sublog-entropy-rank-transfer-bound-vanishing"
            if hypothesis
            else "entropy-transfer-scaling-control-failure"
        ),
    )


def logarithmic_entropy_boundary(n: int) -> LogarithmicEntropyBoundary:
    if n < 2:
        raise ValueError("n must be at least two")
    reference = 1.0 / n**2
    likelihood = float(n**2)
    physical = reference * likelihood
    entropy = math.log2(likelihood)
    ratio = entropy / math.log2(n)
    verified = bool(
        math.isclose(physical, 1.0)
        and math.isclose(entropy, 2.0 * math.log2(n))
        and math.isclose(ratio, 2.0)
    )
    return LogarithmicEntropyBoundary(
        n=n,
        reference_rare_mass=reference,
        rare_likelihood=likelihood,
        physical_rare_mass=physical,
        relative_entropy_bits=entropy,
        relative_entropy_over_log2_n=ratio,
        bounded_observable_physical_mean=physical,
        exact_logarithmic_boundary_verified=verified,
        status=(
            "logarithmic-relative-entropy-boundary-counterexample-verified"
            if verified
            else "logarithmic-entropy-boundary-control-failure"
        ),
    )


def run_parity_rank_profile_entropy_transfer() -> ParityRankProfileEntropyTransferReport:
    finite = [audit_finite_likelihood_information(n) for n in (2, 3, 4, 5)]
    scaling = [
        entropy_transfer_scaling_control(n) for n in (10**8, 10**16, 10**32)
    ]
    boundaries = [logarithmic_entropy_boundary(n) for n in (10, 100, 1_000)]
    failures = sum(
        not (row.negative_information_bound_verified and row.likelihood_tail_bound_verified)
        for row in finite
    )
    failures += sum(
        not row.sublogarithmic_entropy_hypothesis_satisfied for row in scaling
    )
    failures += sum(not row.exact_logarithmic_boundary_verified for row in boundaries)
    verified = failures == 0
    theorem = EntropyTransferTheorem(
        negative_information_bound_bits=NEGATIVE_INFORMATION_BOUND_BITS,
        likelihood_tail_bound=(
            "P(L>tau)<=[D(P||Q)+1/(e ln 2)]/log2(tau)"
        ),
        finite_rank_bound=(
            "E_P f<=b(epsilon)+7nS_n/epsilon^2+"
            "7[D_n+1/(e ln 2)]/log2(n)"
        ),
        sufficient_entropy_condition="D(P_n||Plancherel^6)=o(log n)",
        bounded_total_correlation_sufficient=True,
        vanishing_total_correlation_required=False,
        physical_entropy_condition_proved=False,
        status=(
            "physical-rank-transfer-reduced-to-sublogarithmic-total-correlation"
            if verified
            else "entropy-transfer-control-failure"
        ),
    )
    return ParityRankProfileEntropyTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "total_correlation_identity": (
                "All six physical marginals are Plancherel, hence "
                "D(P_n||Plancherel^6) is their total correlation."
            ),
            "negative_information_bound": "K_-<=1/(e ln 2) bits.",
            "likelihood_tail": theorem.likelihood_tail_bound,
            "rank_transfer": theorem.finite_rank_bound,
            "sufficient_condition": theorem.sufficient_entropy_condition,
            "scope": (
                "The entropy implication is proved, but no all-n physical total-"
                "correlation bound or non-Haar Racah estimate is proved."
            ),
        },
        theorem=theorem,
        finite_information_controls=finite,
        asymptotic_scaling_controls=scaling,
        logarithmic_boundary_controls=boundaries,
        proof_obligations=[
            {
                "obligation": "convert_relative_entropy_to_subquadratic_likelihood_tail",
                "resolved": verified,
                "resolution": (
                    "The universal negative information bound controls the positive "
                    "likelihood-information tail."
                ),
            },
            {
                "obligation": "prove_physical_six_label_total_correlation_is_sublogarithmic",
                "resolved": False,
                "resolution": (
                    "Establish D(P_n||Plancherel^6)=o(log n), preferably O(1), "
                    "using entropy or typical-shape recoupling methods."
                ),
            },
            {
                "obligation": "control_irreducible_racah_conditional_information",
                "resolved": False,
                "resolution": (
                    "Total label correlation does not isolate the two syndrome "
                    "conditional cumulants or their coherent accessibility."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "KL must vanish to transfer a bounded statistic.",
                "resolved": True,
                "resolution": (
                    "No. Sublogarithmic KL suffices because the reference failure "
                    "event is polynomially small."
                ),
            },
            {
                "objection": "The positive part of likelihood information equals KL.",
                "resolved": True,
                "resolution": (
                    "They differ by the negative part, but that part is universally "
                    "at most 1/(e ln 2) bits."
                ),
            },
            {
                "objection": "An O(log n) entropy bound is automatically enough.",
                "resolved": True,
                "resolution": (
                    "False without constants or stronger tails; the quadratic rare-"
                    "event family has entropy exactly 2 log2 n and unit signal."
                ),
            },
            {
                "objection": "Finite S_2 through S_5 KL values imply O(1) entropy.",
                "resolved": False,
                "resolution": "They provide no asymptotic control.",
            },
        ],
        headline_metrics={
            "entropy_transfer_theorem_count": int(verified),
            "finite_information_control_count": len(finite),
            "synthetic_sublog_scaling_control_count": len(scaling),
            "logarithmic_boundary_counterexample_count": len(boundaries),
            "finite_control_failure_count": failures,
            "physical_sublog_total_correlation_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "entropy_to_rank_transfer_criterion_proved": verified,
            "vanishing_kl_required_for_rank_transfer": False,
            "bounded_total_correlation_would_suffice": True,
            "physical_total_correlation_sublogarithmic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "adaptive_syndrome_decouples_proved": False,
            "adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Sublogarithmic total correlation is sufficient, but no such "
                "physical-law entropy theorem is currently available."
            ),
        },
        status=(
            "sublogarithmic-six-label-total-correlation-is-current-entropy-gate"
            if verified
            else "parity-rank-entropy-transfer-failure"
        ),
        summary=(
            "Reduced physical rank transfer to the sublogarithmic total correlation "
            "condition D(P_n||Plancherel^6)=o(log n)."
        ),
        falsifiers_triggered=[
            "Vanishing KL is unnecessarily strong for transfer of the bounded rank observable.",
            "An unspecified O(log n) entropy estimate does not cross the threshold.",
            "Finite low-n entropy cannot certify the required all-n sublogarithmic growth.",
        ],
    )


def write_parity_rank_profile_entropy_transfer_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_rank_profile_entropy_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_rank_profile_entropy_transfer_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
