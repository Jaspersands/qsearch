"""Gaussian benchmark for simultaneous parent and relative conditioning.

The Jacobi surrogate module controls the fractional relative effect of sibling
frames.  A hierarchical polar merge also needs the parent synthesis frame
``A+B`` to have a nonzero singular edge.  These are different hard edges.

For independent Gaussian ``D x m`` matrices, put ``beta=m/D>1/2``.  The
parent frame ``A+B`` is Wishart with aspect ``2 beta`` and support

    [(sqrt(2 beta)-1)^2, (sqrt(2 beta)+1)^2].               (1)

The sibling relative effect has fractional support

    [(sqrt(2 beta-1)-1)^2/(4 beta),
     (sqrt(2 beta-1)+1)^2/(4 beta)].                        (2)

At threshold ``K=ceil(log2 |G|)``, the child aspect ``beta_0`` is in
``[1/2,1)``.  A rule restricted to ``K`` or ``K+1`` cannot certify both hard
edges uniformly from this interval: as ``beta_0 -> 1/2``, equation (1) is
hard at ``beta_0`` while equation (2) is hard at ``2 beta_0 -> 1``.

Using exactly ``K+2`` copies gives ``beta=4 beta_0 in [2,4)``.  Both edges are
then uniformly controlled.  In fact, the relative edge is the bottleneck and

    parent lower edge >= 1,
    parent condition number <= 9,
    relative endpoint gap >= (2-sqrt(3))/4 > 0.0669.        (3)

The upper parent edge is below ``9+4sqrt(2)``.  Thus two extra copies give a
constant-conditioned Gaussian benchmark for both operations at every group
order, without an arithmetic assumption about the fractional part of
``log2 |G|``.

This is a theorem for the selected top sibling split only.  A binary tree
still contains older internal widths whose parent aspect can approach one;
``self_dual_wreath_multiscale_polar_schedule.py`` supplies the separate
mixed-arity Gaussian all-depth schedule.  Neither module proves a natural
Plancherel-frame edge, coherent transform, or algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_sibling_frame_jacobi_surrogate import (
    jacobi_fractional_edges,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sibling_frame_joint_conditioning_surrogate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
TWO_EXTRA_COPY_RELATIVE_GAP_FLOOR = (2.0 - math.sqrt(3.0)) / 4.0
TWO_EXTRA_COPY_PARENT_CONDITION_UPPER = 9.0
TWO_EXTRA_COPY_PARENT_UPPER_EDGE = 9.0 + 4.0 * math.sqrt(2.0)


@dataclass(frozen=True)
class GaussianJointConditioningRecord:
    child_aspect_ratio: float
    parent_aspect_ratio: float
    parent_frame_edge_lower: float
    parent_frame_edge_upper: float
    parent_frame_condition_number: float
    parent_analysis_singular_gap: float
    relative_effect_edge_lower: float
    relative_effect_edge_upper: float
    relative_effect_endpoint_gap: float
    joint_conditioning_score: float
    status: str


@dataclass(frozen=True)
class TwoChoiceFailureBoundaryRecord:
    threshold_aspect_ratio: float
    threshold_parent_edge: float
    threshold_relative_gap: float
    one_extra_parent_edge: float
    one_extra_relative_gap: float
    best_threshold_or_one_extra_joint_score: float
    tends_to_zero_near_threshold_half: bool
    status: str


@dataclass(frozen=True)
class TwoExtraCopyScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    threshold_child_aspect_exact: str
    threshold_child_aspect: float
    selected_copy_count: int
    extra_copy_count: int
    selected_child_aspect_exact: str
    selected_child_aspect: float
    parent_frame_edge_lower: float
    parent_frame_edge_upper: float
    parent_frame_condition_number: float
    relative_effect_endpoint_gap: float
    uniform_parent_edge_verified: bool
    uniform_parent_condition_verified: bool
    uniform_relative_gap_verified: bool
    natural_joint_conditioning_proved: bool
    status: str


@dataclass(frozen=True)
class SiblingFrameJointConditioningSurrogateReport:
    created_at: str
    theorem_contract: dict[str, Any]
    gaussian_aspect_controls: list[GaussianJointConditioningRecord]
    threshold_or_one_extra_failure_boundary: list[TwoChoiceFailureBoundaryRecord]
    two_extra_copy_scaling: list[TwoExtraCopyScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def gaussian_joint_conditioning_record(
    beta: float,
) -> GaussianJointConditioningRecord:
    if not math.isfinite(beta) or beta <= 0.5:
        raise ValueError("the Gaussian parent must span: beta > 1/2")
    parent_root = math.sqrt(2.0 * beta)
    parent_lower = (parent_root - 1.0) ** 2
    parent_upper = (parent_root + 1.0) ** 2
    relative_lower, relative_upper = jacobi_fractional_edges(beta)
    relative_gap = min(relative_lower, 1.0 - relative_upper)
    return GaussianJointConditioningRecord(
        child_aspect_ratio=beta,
        parent_aspect_ratio=2.0 * beta,
        parent_frame_edge_lower=parent_lower,
        parent_frame_edge_upper=parent_upper,
        parent_frame_condition_number=(
            math.inf if parent_lower == 0.0 else parent_upper / parent_lower
        ),
        parent_analysis_singular_gap=parent_root - 1.0,
        relative_effect_edge_lower=relative_lower,
        relative_effect_edge_upper=relative_upper,
        relative_effect_endpoint_gap=relative_gap,
        joint_conditioning_score=min(parent_lower, relative_gap),
        status=(
            "gaussian-parent-and-relative-edges-positive"
            if parent_lower > 0.0 and relative_gap > 0.0
            else "gaussian-hard-edge"
        ),
    )


def two_choice_failure_boundary_record(
    threshold_aspect: float,
) -> TwoChoiceFailureBoundaryRecord:
    if not 0.5 < threshold_aspect < 1.0:
        raise ValueError("threshold aspect must lie strictly between 1/2 and 1")
    threshold = gaussian_joint_conditioning_record(threshold_aspect)
    one_extra = gaussian_joint_conditioning_record(2.0 * threshold_aspect)
    best = max(threshold.joint_conditioning_score, one_extra.joint_conditioning_score)
    return TwoChoiceFailureBoundaryRecord(
        threshold_aspect_ratio=threshold_aspect,
        threshold_parent_edge=threshold.parent_frame_edge_lower,
        threshold_relative_gap=threshold.relative_effect_endpoint_gap,
        one_extra_parent_edge=one_extra.parent_frame_edge_lower,
        one_extra_relative_gap=one_extra.relative_effect_endpoint_gap,
        best_threshold_or_one_extra_joint_score=best,
        tends_to_zero_near_threshold_half=True,
        status="k-or-k-plus-one-has-no-interval-uniform-joint-certificate",
    )


def two_extra_copy_scaling_record(n: int) -> TwoExtraCopyScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    threshold_copies = (order - 1).bit_length()
    threshold_aspect = Fraction(1 << (threshold_copies - 1), order)
    selected_aspect = 4 * threshold_aspect
    gaussian = gaussian_joint_conditioning_record(float(selected_aspect))
    parent_edge_ok = gaussian.parent_frame_edge_lower + 1e-13 >= 1.0
    parent_condition_ok = (
        gaussian.parent_frame_condition_number
        <= TWO_EXTRA_COPY_PARENT_CONDITION_UPPER + 1e-13
    )
    relative_ok = (
        gaussian.relative_effect_endpoint_gap + 1e-13
        >= TWO_EXTRA_COPY_RELATIVE_GAP_FLOOR
    )
    return TwoExtraCopyScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=threshold_copies,
        threshold_child_aspect_exact=str(threshold_aspect),
        threshold_child_aspect=float(threshold_aspect),
        selected_copy_count=threshold_copies + 2,
        extra_copy_count=2,
        selected_child_aspect_exact=str(selected_aspect),
        selected_child_aspect=float(selected_aspect),
        parent_frame_edge_lower=gaussian.parent_frame_edge_lower,
        parent_frame_edge_upper=gaussian.parent_frame_edge_upper,
        parent_frame_condition_number=gaussian.parent_frame_condition_number,
        relative_effect_endpoint_gap=gaussian.relative_effect_endpoint_gap,
        uniform_parent_edge_verified=parent_edge_ok,
        uniform_parent_condition_verified=parent_condition_ok,
        uniform_relative_gap_verified=relative_ok,
        natural_joint_conditioning_proved=False,
        status=(
            "two-extra-copy-gaussian-joint-gap-certified-natural-transfer-open"
            if parent_edge_ok and parent_condition_ok and relative_ok
            else "two-extra-copy-gaussian-joint-bound-failed"
        ),
    )


def run_sibling_frame_joint_conditioning_surrogate() -> (
    SiblingFrameJointConditioningSurrogateReport
):
    aspects = [
        gaussian_joint_conditioning_record(beta)
        for beta in (0.5001, 0.625, 0.75, 0.9999, 1.0001, 1.5, 2.0, 3.0, 4.0)
    ]
    failure_boundary = [
        two_choice_failure_boundary_record(0.5 + epsilon)
        for epsilon in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5)
    ]
    scaling = [
        two_extra_copy_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(
        not (
            row.uniform_parent_edge_verified
            and row.uniform_parent_condition_verified
            and row.uniform_relative_gap_verified
        )
        for row in scaling
    )
    verified = failures == 0
    metrics: dict[str, int | float] = {
        "gaussian_parent_mp_edge_theorem_count": 1,
        "gaussian_relative_jacobi_edge_theorem_count": 1,
        "k_or_k_plus_one_interval_uniform_no_certificate_theorem_count": 1,
        "two_extra_copy_joint_conditioning_theorem_count": 1,
        "failure_boundary_row_count": len(failure_boundary),
        "last_two_choice_joint_score": failure_boundary[-1].best_threshold_or_one_extra_joint_score,
        "two_extra_copy_scaling_row_count": len(scaling),
        "two_extra_copy_scaling_failure_count": failures,
        "uniform_parent_edge_lower_bound": 1.0,
        "uniform_parent_condition_number_upper_bound": TWO_EXTRA_COPY_PARENT_CONDITION_UPPER,
        "uniform_parent_upper_edge_bound": TWO_EXTRA_COPY_PARENT_UPPER_EDGE,
        "uniform_relative_endpoint_gap_lower_bound": TWO_EXTRA_COPY_RELATIVE_GAP_FLOOR,
        "natural_joint_conditioning_theorem_count": 0,
        "coherent_hierarchical_merge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SiblingFrameJointConditioningSurrogateReport(
        created_at=utc_now(),
        theorem_contract={
            "parent_wishart_edge": (
                "The Gaussian parent A+B has MP edges "
                "(sqrt(2beta)+-1)^2."
            ),
            "relative_jacobi_edge": (
                "The Gaussian sibling relative effect has fractional edges "
                "(1+-sqrt(2beta-1))^2/(4beta)."
            ),
            "two_choice_boundary": (
                "From beta_0 in [1/2,1) alone, K or K+1 cannot uniformly "
                "avoid both the parent edge at 1/2 and relative edge at 1."
            ),
            "two_extra_copy_schedule": (
                "K+2 puts beta in [2,4), giving parent lower edge at least 1, "
                "condition number at most 9, and relative gap at least "
                "(2-sqrt(3))/4."
            ),
            "scope": (
                "Every conditioning statement is Gaussian-surrogate and for "
                "the selected top split only. No binary all-depth guarantee, "
                "natural universality, or coherent implementation follows."
            ),
        },
        gaussian_aspect_controls=aspects,
        threshold_or_one_extra_failure_boundary=failure_boundary,
        two_extra_copy_scaling=scaling,
        proof_obligations=[
            {
                "obligation": "control_gaussian_parent_and_relative_hard_edges_simultaneously",
                "resolved": verified,
                "resolution": (
                    "Exactly two extra copies place every possible threshold "
                    "aspect in the uniformly conditioned interval [2,4)."
                ),
            },
            {
                "obligation": "prove_same_joint_edges_for_natural_independent_plancherel_frames",
                "resolved": False,
                "resolution": (
                    "Degree-four joint freeness is insufficient for extreme "
                    "edges; growing-word or resolvent control is required."
                ),
            },
            {
                "obligation": "transfer_natural_edges_to_global_distinct_sources",
                "resolved": False,
                "resolution": (
                    "The injective Plancherel conditioning correction remains uncontrolled."
                ),
            },
            {
                "obligation": "compile_coherent_parent_polar_and_common_span_transforms",
                "resolved": False,
                "resolution": (
                    "The surrogate has no circuit-level access model."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A constant relative Jacobi gap is enough for a hierarchical merge.",
                "resolved": True,
                "resolution": (
                    "False: the parent synthesis singular edge is an independent gate."
                ),
            },
            {
                "objection": "Selecting between K and K+1 uniformly controls both Gaussian gates.",
                "resolved": True,
                "resolution": (
                    "False from the threshold interval alone; near beta_0=1/2 "
                    "the two choices approach different hard edges."
                ),
            },
            {
                "objection": "Two extra copies change the asymptotic copy complexity.",
                "resolved": True,
                "resolution": (
                    "The overhead is exactly two copies and leaves K=Theta(log |G|)."
                ),
            },
            {
                "objection": "Uniform Gaussian joint conditioning proves natural-frame conditioning.",
                "resolved": False,
                "resolution": (
                    "Natural projectors are structured and globally conditioned; "
                    "the required universality theorem is open."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "gaussian_parent_mp_edge_proved": True,
            "gaussian_relative_jacobi_edge_proved": True,
            "k_or_k_plus_one_interval_uniform_joint_certificate_rejected": True,
            "two_extra_copy_gaussian_joint_conditioning_proved": verified,
            "binary_all_depth_gaussian_joint_conditioning_proved": False,
            "natural_independent_joint_spectral_edges_proved": False,
            "globally_distinct_joint_spectral_edges_proved": False,
            "coherent_hierarchical_merge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "K+2 is the correct uniformly conditioned Gaussian benchmark; "
                "natural-frame edge universality and coherent access remain open."
            ),
        },
        status=(
            "two-extra-copy-gaussian-joint-conditioning-proved-natural-transfer-open"
            if verified
            else "two-extra-copy-gaussian-joint-conditioning-control-failure"
        ),
        summary=(
            "Added the missing parent-frame hard edge, rejected a uniform "
            "K-or-K+1 joint certificate, and proved K+2 uniformly conditions "
            "both Gaussian benchmark gates."
        ),
        falsifiers_triggered=[
            "Relative-effect conditioning alone does not certify parent polar conditioning.",
            "K or K+1 has no deterministic interval-uniform certificate for both hard edges.",
            "The Gaussian K+2 theorem does not transfer to structured natural frames automatically.",
        ],
    )


def write_sibling_frame_joint_conditioning_surrogate_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_sibling_frame_joint_conditioning_surrogate())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_sibling_frame_joint_conditioning_surrogate_report()
    print(json.dumps(report, indent=2))
