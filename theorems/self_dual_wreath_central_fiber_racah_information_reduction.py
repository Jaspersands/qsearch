"""Resolve the exact information debt hidden by coarse central features.

Let ``O`` be the four outer labels of the physical Racah law, let ``X,Y`` be
the two intermediate partition labels, and define deterministic central
features ``U=F_s(X)``, ``V=F_s(Y)``.  Entropy chain rules give

    I(X;Y|O) = I(U;V|O)
               + H(X|U,O) + H(Y|V,O)
               - H(X,Y|U,V,O).                            (1)

The nonnegative difference between the first and second mutual information
is the central-fiber resolution debt.  Since the unconditional intermediate
labels are Plancherel,

    I(X;Y|O) <= I(U;V|O) + 2 H_Plancherel(Lambda|F_s).     (2)

Consequently a central-moment proof route needs both coarse-feature Racah
independence and either near-projector resolution or a direct natural bound
on the debt inside unresolved fibers.  The companion projector-resolution
boundary proves that the crude entropy term remains ``Theta(sqrt(n))`` for
``s=o((log n)^2)``.  Fixed-degree freeness therefore cannot close (2).

This does not lower-bound natural Racah information.  A cross-swapped exact
countermodel saturates the two-fiber entropy budget, while a product coupling
has zero debt with equally large fibers.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_free_probability_projector_resolution_boundary import (
    central_class_sum_feature,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_central_fiber_racah_information_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CENTRAL-FIBER-RACAH-INFORMATION-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CentralFiberRacahFiniteControl:
    n: int
    maximum_moved_support: int
    partition_count: int
    distinct_central_feature_count: int
    physical_average_full_racah_mi_bits: float
    physical_average_central_feature_mi_bits: float
    physical_average_fiber_resolution_debt_bits: float
    physical_average_left_hidden_entropy_bits: float
    physical_average_right_hidden_entropy_bits: float
    physical_average_joint_hidden_entropy_bits: float
    plancherel_hidden_entropy_bits: float
    exact_information_decomposition_residual_bits: float
    maximum_intermediate_plancherel_marginal_residual: float
    fiber_entropy_upper_bound_slack_bits: float
    exact_central_fiber_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class CrossSwappedFiberCountermodel:
    visible_feature_count: int
    total_label_count: int
    visible_feature_mutual_information_bits: float
    full_label_mutual_information_bits: float
    left_hidden_entropy_bits: float
    right_hidden_entropy_bits: float
    joint_hidden_entropy_bits: float
    fiber_resolution_debt_bits: float
    entropy_budget_slack_bits: float
    maximum_uniform_marginal_residual: float
    exact_two_fiber_budget_saturation_verified: bool
    status: str


@dataclass(frozen=True)
class CentralFiberRacahInformationTheorem:
    exact_decomposition: str
    plancherel_entropy_upper: str
    sufficient_condition: str
    fixed_degree_route_closes_rank_mi_proved: bool
    natural_within_fiber_delocalization_proved: bool
    status: str


@dataclass(frozen=True)
class CentralFiberRacahInformationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CentralFiberRacahInformationTheorem
    finite_controls: list[CentralFiberRacahFiniteControl]
    countermodels: list[CrossSwappedFiberCountermodel]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _entropy_bits(probability: np.ndarray) -> float:
    positive = probability > 0
    return float(-np.sum(probability[positive] * np.log2(probability[positive])))


def _aggregate_feature_coupling(
    coupling: np.ndarray,
    feature_indices: np.ndarray,
    feature_count: int,
) -> np.ndarray:
    coarse = np.zeros((feature_count, feature_count), dtype=float)
    for x, y in np.ndindex(coupling.shape):
        coarse[feature_indices[x], feature_indices[y]] += coupling[x, y]
    return coarse


def audit_central_fiber_racah_information(
    n: int,
    maximum_support: int,
    *,
    tolerance: float = 3e-9,
) -> CentralFiberRacahFiniteControl:
    if not 3 <= n <= 5:
        raise ValueError("exact physical controls require 3<=n<=5")
    if not 2 <= maximum_support <= n:
        raise ValueError("require 2<=support<=n")
    partitions, _likelihood, reference, physical = finite_physical_likelihood_arrays(n)
    q = np.sum(reference, axis=(1, 2, 3, 4, 5))
    features = [central_class_sum_feature(partition, maximum_support) for partition in partitions]
    feature_values = {feature: index for index, feature in enumerate(sorted(set(features)))}
    feature_indices = np.array([feature_values[feature] for feature in features], dtype=int)
    feature_count = len(feature_values)

    q_feature = np.zeros(feature_count, dtype=float)
    for index, mass in enumerate(q):
        q_feature[feature_indices[index]] += mass
    plancherel_hidden = _entropy_bits(q) - _entropy_bits(q_feature)

    outer = np.sum(physical, axis=(3, 4))
    full_mi = 0.0
    feature_mi = 0.0
    left_hidden = 0.0
    right_hidden = 0.0
    joint_hidden = 0.0
    maximum_local_residual = 0.0
    for outer_index in np.ndindex(outer.shape):
        outer_mass = float(outer[outer_index])
        if outer_mass <= 0:
            continue
        alpha, beta, gamma, final = outer_index
        coupling = physical[alpha, beta, gamma, :, :, final] / outer_mass
        left = np.sum(coupling, axis=1)
        right = np.sum(coupling, axis=0)
        coarse = _aggregate_feature_coupling(coupling, feature_indices, feature_count)
        coarse_left = np.sum(coarse, axis=1)
        coarse_right = np.sum(coarse, axis=0)

        local_full = _entropy_bits(left) + _entropy_bits(right) - _entropy_bits(coupling)
        local_feature = (
            _entropy_bits(coarse_left)
            + _entropy_bits(coarse_right)
            - _entropy_bits(coarse)
        )
        local_left_hidden = _entropy_bits(left) - _entropy_bits(coarse_left)
        local_right_hidden = _entropy_bits(right) - _entropy_bits(coarse_right)
        local_joint_hidden = _entropy_bits(coupling) - _entropy_bits(coarse)
        local_decomposition = (
            local_feature
            + local_left_hidden
            + local_right_hidden
            - local_joint_hidden
        )
        maximum_local_residual = max(
            maximum_local_residual,
            abs(local_full - local_decomposition),
        )
        full_mi += outer_mass * local_full
        feature_mi += outer_mass * local_feature
        left_hidden += outer_mass * local_left_hidden
        right_hidden += outer_mass * local_right_hidden
        joint_hidden += outer_mass * local_joint_hidden

    debt = full_mi - feature_mi
    decomposition_residual = abs(
        full_mi - feature_mi - left_hidden - right_hidden + joint_hidden
    )
    left_marginal = np.sum(physical, axis=(0, 1, 2, 4, 5))
    right_marginal = np.sum(physical, axis=(0, 1, 2, 3, 5))
    marginal_residual = max(
        float(np.max(np.abs(left_marginal - q))),
        float(np.max(np.abs(right_marginal - q))),
    )
    upper_slack = 2.0 * plancherel_hidden - debt
    verified = bool(
        maximum_local_residual <= tolerance
        and decomposition_residual <= tolerance
        and marginal_residual <= tolerance
        and debt >= -tolerance
        and left_hidden <= plancherel_hidden + tolerance
        and right_hidden <= plancherel_hidden + tolerance
        and upper_slack >= -tolerance
    )
    return CentralFiberRacahFiniteControl(
        n=n,
        maximum_moved_support=maximum_support,
        partition_count=len(partitions),
        distinct_central_feature_count=feature_count,
        physical_average_full_racah_mi_bits=full_mi,
        physical_average_central_feature_mi_bits=feature_mi,
        physical_average_fiber_resolution_debt_bits=debt,
        physical_average_left_hidden_entropy_bits=left_hidden,
        physical_average_right_hidden_entropy_bits=right_hidden,
        physical_average_joint_hidden_entropy_bits=joint_hidden,
        plancherel_hidden_entropy_bits=plancherel_hidden,
        exact_information_decomposition_residual_bits=max(
            maximum_local_residual, decomposition_residual
        ),
        maximum_intermediate_plancherel_marginal_residual=marginal_residual,
        fiber_entropy_upper_bound_slack_bits=upper_slack,
        exact_central_fiber_reduction_verified=verified,
        status=(
            "exact-central-fiber-racah-information-reduction-verified"
            if verified
            else "central-fiber-racah-information-control-failure"
        ),
    )


def cross_swapped_fiber_countermodel(
    visible_feature_count: int,
    *,
    tolerance: float = 1e-12,
) -> CrossSwappedFiberCountermodel:
    """Return ``X=(A,B), Y=(B,A)`` with features ``U=A,V=B``."""
    k = visible_feature_count
    if k < 1:
        raise ValueError("visible feature count must be positive")
    joint = np.zeros((k, k, k, k), dtype=float)
    for a in range(k):
        for b in range(k):
            joint[a, b, b, a] = 1.0 / (k * k)
    left = np.sum(joint, axis=(2, 3))
    right = np.sum(joint, axis=(0, 1))
    expected = np.full((k, k), 1.0 / (k * k))
    visible = np.sum(joint, axis=(1, 3))
    visible_left = np.sum(visible, axis=1)
    visible_right = np.sum(visible, axis=0)
    full_mi = _entropy_bits(left) + _entropy_bits(right) - _entropy_bits(joint)
    visible_mi = (
        _entropy_bits(visible_left)
        + _entropy_bits(visible_right)
        - _entropy_bits(visible)
    )
    left_hidden = _entropy_bits(left) - _entropy_bits(visible_left)
    right_hidden = _entropy_bits(right) - _entropy_bits(visible_right)
    joint_hidden = _entropy_bits(joint) - _entropy_bits(visible)
    debt = full_mi - visible_mi
    slack = left_hidden + right_hidden - debt
    marginal_residual = max(
        float(np.max(np.abs(left - expected))),
        float(np.max(np.abs(right - expected))),
    )
    verified = bool(
        marginal_residual <= tolerance
        and abs(visible_mi) <= tolerance
        and abs(full_mi - 2.0 * math.log2(k)) <= tolerance
        and abs(joint_hidden) <= tolerance
        and abs(slack) <= tolerance
    )
    return CrossSwappedFiberCountermodel(
        visible_feature_count=k,
        total_label_count=k * k,
        visible_feature_mutual_information_bits=visible_mi,
        full_label_mutual_information_bits=full_mi,
        left_hidden_entropy_bits=left_hidden,
        right_hidden_entropy_bits=right_hidden,
        joint_hidden_entropy_bits=joint_hidden,
        fiber_resolution_debt_bits=debt,
        entropy_budget_slack_bits=slack,
        maximum_uniform_marginal_residual=marginal_residual,
        exact_two_fiber_budget_saturation_verified=verified,
        status=(
            "two-unresolved-fibers-can-hide-the-entire-information-budget"
            if verified
            else "cross-swapped-fiber-countermodel-control-failure"
        ),
    )


def run_central_fiber_racah_information_reduction(
) -> CentralFiberRacahInformationReport:
    finite = [
        audit_central_fiber_racah_information(n, support)
        for n in (3, 4, 5)
        for support in range(2, min(n, 3) + 1)
    ]
    countermodels = [cross_swapped_fiber_countermodel(k) for k in (2, 4, 8, 16)]
    failures = sum(not row.exact_central_fiber_reduction_verified for row in finite)
    failures += sum(
        not row.exact_two_fiber_budget_saturation_verified for row in countermodels
    )
    verified = failures == 0
    theorem = CentralFiberRacahInformationTheorem(
        exact_decomposition=(
            "I(X;Y|O)=I(F_s(X);F_s(Y)|O)+H(X|F_s(X),O)+H(Y|F_s(Y),O)-H(X,Y|F_s(X),F_s(Y),O)"
        ),
        plancherel_entropy_upper=(
            "I(X;Y|O)<=I(F_s(X);F_s(Y)|O)+2 H_Plancherel(Lambda|F_s)"
        ),
        sufficient_condition=(
            "coarse feature MI=o(log n) and the physical-average fiber-resolution debt=o(log n)"
        ),
        fixed_degree_route_closes_rank_mi_proved=False,
        natural_within_fiber_delocalization_proved=False,
        status=(
            "central-feature-route-reduced-to-growing-resolution-or-within-fiber-delocalization"
            if verified
            else "central-fiber-racah-information-control-failure"
        ),
    )
    return CentralFiberRacahInformationReport(
        created_at=utc_now(),
        theorem_contract={
            "outer_label": "O=(alpha,beta,gamma,lambda)",
            "intermediate_labels": "X=mu and Y=nu under the natural squared Racah coupling",
            "features": "U=F_s(X), V=F_s(Y) are deterministic central class-sum vectors",
            "marginal_input": "unconditional X and Y are exactly Plancherel",
            "scope": "rank-label information only; orientation-syndrome CMI remains separate",
        },
        theorem=theorem,
        finite_controls=finite,
        countermodels=countermodels,
        proof_obligations=[
            {
                "obligation": "derive_exact_central_fiber_information_chain",
                "resolved": verified,
                "resolution": "Apply H(X)=H(U)+H(X|U) and its joint analogue conditionally on O.",
            },
            {
                "obligation": "bound_coarse_growing_support_racah_information",
                "resolved": False,
                "resolution": "Needs same-n mixed central-character control at support at least logarithmic-squared in n.",
            },
            {
                "obligation": "bound_natural_fiber_resolution_debt",
                "resolved": False,
                "resolution": "Need conditional delocalization inside central-feature fibers; large fiber entropy alone gives no bound.",
            },
            {
                "obligation": "translate_rank_no_go_to_orientation_syndrome_channel",
                "resolved": False,
                "resolution": "This reduction does not touch the two irreducible non-Haar parity cumulants.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Coarse central-feature independence implies label independence.",
                "resolved": True,
                "resolution": "The cross-swapped model has zero coarse MI and saturates both hidden-entropy terms.",
            },
            {
                "objection": "Large unresolved fibers force natural Racah dependence.",
                "resolved": True,
                "resolution": "A product label coupling has zero debt regardless of fiber size; a natural lower bound is not proved.",
            },
            {
                "objection": "The two marginal hidden entropies can be replaced by their minimum.",
                "resolved": True,
                "resolution": "The cross-swapped model has debt equal to their sum, so the factor-two budget is sharp in general.",
            },
            {
                "objection": "Fixed-degree asymptotic freeness can close the coarse route.",
                "resolved": True,
                "resolution": "The projector-resolution theorem leaves Theta(sqrt(n)) Plancherel entropy unresolved below the log-squared scale.",
            },
        ],
        headline_metrics={
            "exact_central_fiber_information_reduction_count": int(verified),
            "finite_natural_racah_control_count": len(finite),
            "tight_two_fiber_countermodel_count": len(countermodels),
            "finite_control_failure_count": failures,
            "natural_within_fiber_delocalization_theorem_count": 0,
            "growing_support_coarse_mi_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_information_decomposition_proved": verified,
            "plancherel_fiber_entropy_upper_proved": verified,
            "fixed_degree_free_probability_closes_rank_mi": False,
            "natural_racah_rank_mi_vanishes_proved": False,
            "natural_racah_rank_mi_survives_proved": False,
            "orientation_syndrome_signal_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "Both growing-support coarse dependence and natural within-fiber delocalization remain unproved.",
        },
        status=(
            "natural-racah-rank-information-split-into-coarse-and-fiber-debt"
            if verified
            else "central-fiber-racah-information-control-failure"
        ),
        summary=(
            "Reduced central-moment approaches to an exact coarse Racah term plus a "
            "fiber-resolution debt, and proved that both unresolved sides can matter."
        ),
        falsifiers_triggered=[
            "Coarse feature independence alone does not control fine Racah labels.",
            "Plancherel marginal stationarity does not control dependence inside feature fibers.",
            "Fixed-degree central moments remain below the required projector-resolution scale.",
        ],
    )


def write_central_fiber_racah_information_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_central_fiber_racah_information_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_central_fiber_racah_information_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
