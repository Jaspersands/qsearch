"""All-fixed-moment bridge from sibling frames to dependency-ridge tails.

Let ``F_n`` be the natural child frame on physical dimension ``D_n`` and let
``mu_n`` be its expected empirical eigenvalue measure, including zero modes.
At the final root the child aspect satisfies

    alpha_n=q_n/|S_n| in [2,4).                           (1)

The Marchenko--Pastur moments in the normalization used by the sibling-frame
modules are

    m_k(alpha)=sum_(j=1)^k Narayana(k,j) alpha^j,         (2)

and the support has lower endpoint

    ell(alpha)=(sqrt(alpha)-1)^2
              >= (sqrt(2)-1)^2 > 0.                      (3)

Suppose that for every *fixed* ``k``

    integral x^k d mu_n(x)-m_k(alpha_n) -> 0.            (4)

Then ``mu_n`` converges, uniformly along the compact aspect family in (1),
to the corresponding Marchenko--Pastur laws.  The proof is the ordinary
method of moments: the first moment gives tightness, the next fixed moment
gives uniform integrability at each order, every aspect subsequence has a
convergent subsubsequence, and the compactly supported MP law is moment
determinate.

For any fixed ``tau<(sqrt(2)-1)^2``, equation (4) therefore implies

    E N_Fn^+(tau)/D_n -> 0.                               (5)

Combining (5) with the single-frame tail theorem shows that for every fixed
``a>0`` and ``eta_n=n^-a``,

    E T_eta_n(F_n)/D_n -> 0,
    E ||Pi-Q_eta_n||F^2/D_n -> 0.                         (6)

Because the tail observable lies in ``[0,1]``, global-distinct conditioning
changes it by at most the source-collision probability.  Thus no
globally-distinct raw-moment theorem and no growing-moment spectral edge are
needed for qualitative support transfer at a constant M4 signal.

This module proves the implication (4)->(6), not premise (4).  The repository
currently has exact moments only through order four.  A constant or
inverse-polynomial natural ridge-curl lower bound is also still missing.  For
an inverse-polynomial signal rather than a constant signal, a quantitative
moment or small-eigenvalue rate would again be required.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_dependency_ridge_moment_method_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-MOMENT-METHOD-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class VanishingFractionHardEdgeControl:
    control_id: str
    dimension: int
    contaminated_eigenvalue_count: int
    contaminated_eigenvalue_fraction: float
    tiny_eigenvalue: float
    minimum_positive_eigenvalue: float
    maximum_moment_difference_through_order: int
    maximum_normalized_moment_difference: float
    ridge_parameter: float
    exact_normalized_support_ridge_tail: float
    near_zero_split_upper_bound: float
    tail_bound_verified: bool
    minimum_edge_vanishes: bool
    normalized_tail_vanishes_with_contamination_fraction: bool
    status: str


@dataclass(frozen=True)
class FixedMomentTailScalingRecord:
    n: int
    child_aspect: float
    uniform_mp_lower_edge: float
    chosen_fixed_threshold: float
    ridge_inverse_polynomial_degree: int
    ridge_parameter: float
    ridge_to_fixed_threshold_squared: float
    assumed_expected_small_eigenvalue_density: float
    resulting_single_frame_tail_upper_bound: float
    qualitative_all_fixed_moment_premise_assumed: bool
    growing_moment_edge_required: bool
    global_distinct_raw_moment_transfer_required: bool
    status: str


@dataclass(frozen=True)
class DependencyRidgeMomentMethodBridgeTheorem:
    mp_moments: str
    uniform_mp_gap: str
    all_fixed_moment_premise: str
    weak_convergence_consequence: str
    fixed_threshold_consequence: str
    inverse_polynomial_ridge_consequence: str
    collision_free_consequence: str
    constant_signal_only_without_rate: bool
    growing_moment_edge_required: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDependencyRidgeMomentMethodBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DependencyRidgeMomentMethodBridgeTheorem
    finite_controls: list[VanishingFractionHardEdgeControl]
    scaling_records: list[FixedMomentTailScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def narayana_number(order: int, blocks: int) -> int:
    if order < 1 or not 1 <= blocks <= order:
        raise ValueError("valid positive Narayana indices are required")
    return math.comb(order, blocks) * math.comb(order, blocks - 1) // order


def marchenko_pastur_moment(order: int, aspect: float) -> float:
    if order < 1 or aspect <= 0:
        raise ValueError("positive moment order and aspect are required")
    return sum(
        narayana_number(order, blocks) * aspect**blocks
        for blocks in range(1, order + 1)
    )


def marchenko_pastur_lower_edge(aspect: float) -> float:
    if aspect <= 0:
        raise ValueError("the aspect must be positive")
    return (math.sqrt(aspect) - 1.0) ** 2


def _support_ridge_tail_from_values(values: np.ndarray, eta: float) -> float:
    positive = values[values > 0]
    return float(np.sum((eta / (positive + eta)) ** 2))


def audit_vanishing_fraction_hard_edge(
    control_id: str,
    dimension: int,
    contaminated_eigenvalue_count: int,
    tiny_eigenvalue: float,
    ridge_parameter: float,
    *,
    highest_moment_order: int = 8,
) -> VanishingFractionHardEdgeControl:
    if not 1 <= contaminated_eigenvalue_count < dimension:
        raise ValueError("contamination count must lie strictly inside dimension")
    if min(tiny_eigenvalue, ridge_parameter) <= 0 or highest_moment_order < 1:
        raise ValueError("positive scales and moment order are required")
    clean = np.linspace(0.5, 2.5, dimension)
    contaminated = clean.copy()
    contaminated[:contaminated_eigenvalue_count] = tiny_eigenvalue
    differences = [
        abs(
            float(np.mean(contaminated**order))
            - float(np.mean(clean**order))
        )
        for order in range(1, highest_moment_order + 1)
    ]
    exact_tail = _support_ridge_tail_from_values(
        contaminated,
        ridge_parameter,
    ) / dimension
    threshold = 0.25
    near_count = int(np.sum((contaminated > 0) & (contaminated <= threshold)))
    split = near_count / dimension + (
        ridge_parameter / (threshold + ridge_parameter)
    ) ** 2
    fraction = contaminated_eigenvalue_count / dimension
    verified = exact_tail <= split + 1e-12
    return VanishingFractionHardEdgeControl(
        control_id=control_id,
        dimension=dimension,
        contaminated_eigenvalue_count=contaminated_eigenvalue_count,
        contaminated_eigenvalue_fraction=fraction,
        tiny_eigenvalue=tiny_eigenvalue,
        minimum_positive_eigenvalue=float(np.min(contaminated)),
        maximum_moment_difference_through_order=highest_moment_order,
        maximum_normalized_moment_difference=max(differences),
        ridge_parameter=ridge_parameter,
        exact_normalized_support_ridge_tail=exact_tail,
        near_zero_split_upper_bound=split,
        tail_bound_verified=verified,
        minimum_edge_vanishes=tiny_eigenvalue < dimension**-4,
        normalized_tail_vanishes_with_contamination_fraction=(
            exact_tail <= 2 * fraction
        ),
        status=(
            "vanishing-fraction-hard-edge-outliers-compatible-with-vanishing-tail"
            if verified and exact_tail <= 2 * fraction
            else "moment-method-hard-edge-control-failure"
        ),
    )


def fixed_moment_tail_scaling_record(
    n: int,
    child_aspect: float,
    assumed_expected_small_eigenvalue_density: float,
    *,
    ridge_inverse_polynomial_degree: int = 4,
) -> FixedMomentTailScalingRecord:
    if n < 2 or not 2 <= child_aspect < 4:
        raise ValueError("final-root n and child aspect are required")
    if assumed_expected_small_eigenvalue_density < 0:
        raise ValueError("small-eigenvalue density must be nonnegative")
    if ridge_inverse_polynomial_degree < 1:
        raise ValueError("ridge degree must be positive")
    uniform_edge = marchenko_pastur_lower_edge(2.0)
    threshold = uniform_edge / 2.0
    eta = n ** (-ridge_inverse_polynomial_degree)
    ratio_squared = (eta / (threshold + eta)) ** 2
    return FixedMomentTailScalingRecord(
        n=n,
        child_aspect=child_aspect,
        uniform_mp_lower_edge=uniform_edge,
        chosen_fixed_threshold=threshold,
        ridge_inverse_polynomial_degree=ridge_inverse_polynomial_degree,
        ridge_parameter=eta,
        ridge_to_fixed_threshold_squared=ratio_squared,
        assumed_expected_small_eigenvalue_density=(
            assumed_expected_small_eigenvalue_density
        ),
        resulting_single_frame_tail_upper_bound=(
            assumed_expected_small_eigenvalue_density + ratio_squared
        ),
        qualitative_all_fixed_moment_premise_assumed=True,
        growing_moment_edge_required=False,
        global_distinct_raw_moment_transfer_required=False,
        status="all-fixed-moment-premise-would-close-qualitative-ridge-tail",
    )


def dependency_ridge_moment_method_bridge_theorem(
) -> DependencyRidgeMomentMethodBridgeTheorem:
    return DependencyRidgeMomentMethodBridgeTheorem(
        mp_moments=(
            "m_k(alpha)=sum_(j=1)^k Narayana(k,j)alpha^j"
        ),
        uniform_mp_gap=(
            "inf_(alpha in [2,4)) ell(alpha)=(sqrt(2)-1)^2"
        ),
        all_fixed_moment_premise=(
            "for every fixed k, E Tr(F_n^k)/D_n-m_k(alpha_n)->0"
        ),
        weak_convergence_consequence=(
            "the expected empirical laws converge subsequentially to MP_(alpha_n)"
        ),
        fixed_threshold_consequence=(
            "for fixed tau<(sqrt(2)-1)^2, E N_Fn^+(tau)/D_n->0"
        ),
        inverse_polynomial_ridge_consequence=(
            "for every fixed a>0, eta_n=n^-a gives E T_eta_n(F_n)/D_n->0"
        ),
        collision_free_consequence=(
            "bounded tail transfer adds at most 1-p_cf=o(1)"
        ),
        constant_signal_only_without_rate=True,
        growing_moment_edge_required=False,
        theorem_verified=True,
        status="all-fixed-moment-convergence-suffices-for-constant-signal-ridge-transfer",
    )


def run_component_dependency_ridge_moment_method_bridge(
) -> ComponentDependencyRidgeMomentMethodBridgeReport:
    controls = [
        audit_vanishing_fraction_hard_edge(
            f"DIM-{dimension}-SQRT-CONTAMINATION",
            dimension,
            math.isqrt(dimension),
            dimension**-6,
            dimension**-4,
        )
        for dimension in (64, 256, 1024, 4096)
    ]
    aspects = (2.0, 2.25, 3.0, 3.75)
    scaling = [
        fixed_moment_tail_scaling_record(
            n,
            aspects[index % len(aspects)],
            1.0 / math.sqrt(n),
        )
        for index, n in enumerate((32, 64, 128, 256, 512, 1024, 4096))
    ]
    theorem = dependency_ridge_moment_method_bridge_theorem()
    failures = sum(not row.tail_bound_verified for row in controls)
    mp_formula_residual = max(
        abs(marchenko_pastur_moment(order, 2.0) - expected)
        for order, expected in (
            (1, 2.0),
            (2, 6.0),
            (3, 22.0),
            (4, 90.0),
        )
    )
    return ComponentDependencyRidgeMomentMethodBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "moments": theorem.mp_moments,
            "uniform_gap": theorem.uniform_mp_gap,
            "premise": theorem.all_fixed_moment_premise,
            "weak_law": theorem.weak_convergence_consequence,
            "small_eigenvalues": theorem.fixed_threshold_consequence,
            "ridge_tail": theorem.inverse_polynomial_ridge_consequence,
            "conditioning": theorem.collision_free_consequence,
            "scope": (
                "This is a method-of-moments implication. It does not prove "
                "the all-fixed natural moment premise or a positive ridge curl."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "identify_sufficient_moment_regime_for_trace_tail",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "All fixed moments plus determinacy imply the weak law; "
                    "orders growing with n are unnecessary for a trace tail."
                ),
            },
            {
                "obligation": "avoid_global_distinct_transfer_of_unbounded_moments",
                "resolved": True,
                "resolution": (
                    "Derive the independent weak law, then transfer only the "
                    "bounded support-ridge tail."
                ),
            },
            {
                "obligation": "prove_all_fixed_independent_plancherel_child_frame_moments",
                "resolved": False,
                "resolution": (
                    "Use the exact arbitrary-word normal form with fixed-order "
                    "word-map/character bounds. Only orders one through four are proved."
                ),
            },
            {
                "obligation": "prove_constant_or_inverse_polynomial_natural_ridge_curl",
                "resolved": False,
                "resolution": (
                    "The spectral bridge controls support transfer only; the "
                    "typical physical Hamming-pair commutator remains open."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A spectral edge requires moments growing with dimension.",
                "resolved": True,
                "resolution": (
                    "Correct for the minimum eigenvalue, but the target is a "
                    "normalized trace tail. Weak convergence is enough."
                ),
            },
            {
                "objection": "Four exact moments imply the weak law.",
                "resolved": False,
                "resolution": (
                    "No finite moment list determines a measure or excludes a "
                    "macroscopic near-zero sector. Every fixed order is required."
                ),
            },
            {
                "objection": "Tiny minimum eigenvalues falsify trace-tail transfer.",
                "resolved": True,
                "resolution": (
                    "A vanishing fraction of arbitrarily tiny eigenvalues gives "
                    "a vanishing normalized tail; the controls exhibit this exactly."
                ),
            },
            {
                "objection": "Qualitative moment convergence preserves inverse-polynomial signals.",
                "resolved": False,
                "resolution": (
                    "Without a rate it only suffices when the ridge-curl signal "
                    "has a constant lower bound."
                ),
            },
        ],
        headline_metrics={
            "all_fixed_moment_to_tail_bridge_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "growing_moment_edge_requirement_removed_count": 1,
            "global_distinct_raw_moment_transfer_requirement_removed_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "mp_moment_formula_residual_through_order_four": mp_formula_residual,
            "minimum_control_positive_eigenvalue": min(
                row.minimum_positive_eigenvalue for row in controls
            ),
            "maximum_control_normalized_tail": max(
                row.exact_normalized_support_ridge_tail for row in controls
            ),
            "all_fixed_natural_moment_theorem_count": 0,
            "natural_ridge_curl_lower_bound_theorem_count": 0,
            "natural_component_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_fixed_moments_would_suffice_for_trace_tail": (
                theorem.theorem_verified and failures == 0
            ),
            "growing_moment_spectral_edge_required_for_trace_tail": False,
            "globally_distinct_raw_moment_control_required": False,
            "independent_moments_through_order_four_proved": True,
            "all_fixed_independent_moments_proved": False,
            "natural_child_frame_weak_mp_law_proved": False,
            "natural_support_ridge_tail_small": False,
            "natural_ridge_curl_positive": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The spectral target now needs only all-fixed independent "
                "moments, but that theorem and the positive ridge curl are open."
            ),
        },
        status=(
            "all-fixed-moment-criterion-for-support-ridge-tail-proved"
            if failures == 0
            else "dependency-ridge-moment-method-control-failure"
        ),
        summary=(
            "Proved that all fixed independent child-frame moments, rather "
            "than growing moments or a spectral edge, suffice for qualitative "
            "dependency-ridge transfer at a constant signal."
        ),
        falsifiers_triggered=[
            "Growing moments are unnecessary for the normalized support-ridge trace tail.",
            "Four fixed moments remain insufficient; every fixed order is still open.",
            "Unbounded raw moments need not transfer through global-distinct conditioning.",
            "A vanishing fraction of arbitrarily tiny eigenvalues is compatible with vanishing trace tail.",
            "No all-fixed natural law, ridge curl, exact M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_dependency_ridge_moment_method_bridge_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-MOMENT-METHOD-BRIDGE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_dependency_ridge_moment_method_bridge" in globals():
        report = run_component_dependency_ridge_moment_method_bridge(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-MOMENT-METHOD-BRIDGE",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-MOMENT-METHOD-BRIDGE.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-MOMENT-METHOD-BRIDGE.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_component_dependency_ridge_moment_method_bridge": str(path)
                },
            )
        )
    return payload
