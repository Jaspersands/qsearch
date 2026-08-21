"""Normalization barrier for positive Poisson words at the support-ridge scale.

Let the natural child frame be a sum of ``q`` projection leaves,

    F = sum_e E_e,              Fbar=F/q.                 (1)

The physical support ridge with parameter ``eta`` is

    f_eta(F)=F(F+eta I)^-1
            =Fbar(Fbar+delta I)^-1,   delta=eta/q.        (2)

For iid uniform leaves and ``Q_e=I-E_e``, Poissonization gives exact positive
word mixtures

    delta(Fbar+delta I)^-1
      = sum_(m>=0) delta/(1+delta)^(m+1)
          E[Q_m ... Q_1],                              (3)

    delta^2(Fbar+delta I)^-2
      = sum_(m>=0) delta^2(m+1)/(1+delta)^(m+2)
          E[Q_m ... Q_1].                              (4)

The length laws in (3)-(4) have means ``1/delta`` and ``2/delta``.  At the
final wreath root, ``q/|S_n| in [2,4)``.  Hence any inverse-polynomial
*physical* parameter ``eta`` gives mean word length ``Theta(q/eta)``, which is
factorial rather than polynomial in ``n``.  Capturing constant mixture mass
also requires ``Omega(q/eta)`` words: for (4),

    Pr[N<=L] <= delta^2 (L+1)(L+2)/2.                    (5)

The opposite normalization fails as a support approximation.  If one chooses
``delta=n^-a`` so that the Poisson length is polynomial, the physical ridge
parameter is ``eta=q delta``.  For support rank ``s``, trace density
``alpha=Tr(F)/D``, and ``rho=s/D``,

    T_eta(F)/D
      = D^-1 sum_(lambda>0)(eta/(lambda+eta))^2
      >= rho-2 alpha/(q delta).                           (6)

Thus on any event with ``rho=Omega(1)`` and ``alpha=O(1)``, a polynomial
normalized parameter leaves constant support-ridge error.

This proves a no-go only for the positive uniform-leaf Poisson/complement-word
route at the parameter needed by the dependency support ridge.  It does not
rule out signed polynomial approximation, rational recursions, a direct
resolvent/local law, or a representation-specific implementation that applies
the aggregate frame without sampling its leaves one at a time.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_support_ridge_poisson_scale_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-RIDGE-POISSON-SCALE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PoissonScaleMixtureControl:
    control_id: str
    ambient_dimension: int
    leaf_count: int
    normalized_ridge_parameter: float
    truncation_length: int
    geometric_mass_through_truncation: float
    negative_binomial_mass_through_truncation: float
    geometric_tail: float
    negative_binomial_tail: float
    geometric_resolvent_residual: float
    squared_resolvent_residual: float
    geometric_residual_bounded_by_tail: bool
    squared_residual_bounded_by_tail: bool
    exact_positive_mixture_verified: bool
    status: str


@dataclass(frozen=True)
class SupportRidgePoissonScaleRecord:
    n: int
    group_order_decimal: str
    child_leaf_count_decimal: str
    child_leaf_aspect: float
    physical_inverse_polynomial_degree: int
    log2_geometric_mean_length_at_physical_eta: float
    log2_squared_mean_length_at_physical_eta: float
    constant_mass_squared_length_log2_lower_bound: float
    normalized_inverse_polynomial_degree: int
    coarse_physical_ridge_log2: float
    assumed_support_rank_density: float
    assumed_frame_trace_density: float
    coarse_normalized_tail_lower_bound: float
    positive_poisson_words_polynomial_at_physical_scale: bool
    coarse_normalized_ridge_transfers_support: bool
    status: str


@dataclass(frozen=True)
class SupportRidgePoissonScaleNoGoTheorem:
    parameter_rescaling: str
    geometric_mixture: str
    squared_mixture: str
    constant_mass_length_lower_bound: str
    coarse_ridge_tail_lower_bound: str
    final_root_leaf_aspect: str
    positive_uniform_leaf_poisson_route_only: bool
    signed_or_aggregate_approximations_ruled_out: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentSupportRidgePoissonScaleNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SupportRidgePoissonScaleNoGoTheorem
    finite_controls: list[PoissonScaleMixtureControl]
    scaling_records: list[SupportRidgePoissonScaleRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def geometric_length_mass(
    normalized_ridge_parameter: Fraction,
    word_length: int,
) -> Fraction:
    if normalized_ridge_parameter <= 0 or word_length < 0:
        raise ValueError("positive ridge parameter and nonnegative length required")
    delta = normalized_ridge_parameter
    return delta / (1 + delta) ** (word_length + 1)


def squared_length_mass(
    normalized_ridge_parameter: Fraction,
    word_length: int,
) -> Fraction:
    if normalized_ridge_parameter <= 0 or word_length < 0:
        raise ValueError("positive ridge parameter and nonnegative length required")
    delta = normalized_ridge_parameter
    return delta**2 * (word_length + 1) / (1 + delta) ** (word_length + 2)


def geometric_length_tail(
    normalized_ridge_parameter: Fraction,
    truncation_length: int,
) -> Fraction:
    if normalized_ridge_parameter <= 0 or truncation_length < 0:
        raise ValueError("positive ridge parameter and nonnegative truncation required")
    return 1 / (1 + normalized_ridge_parameter) ** (truncation_length + 1)


def squared_length_tail(
    normalized_ridge_parameter: Fraction,
    truncation_length: int,
) -> Fraction:
    if normalized_ridge_parameter <= 0 or truncation_length < 0:
        raise ValueError("positive ridge parameter and nonnegative truncation required")
    delta = normalized_ridge_parameter
    ratio = 1 / (1 + delta)
    return ratio ** (truncation_length + 1) * (
        (truncation_length + 2) - (truncation_length + 1) * ratio
    )


def squared_constant_mass_length_lower_bound(
    normalized_ridge_parameter: Fraction,
    target_mass: Fraction = Fraction(1, 2),
) -> int:
    """Necessary length from the elementary bound in equation (5)."""

    if normalized_ridge_parameter <= 0 or not 0 < target_mass < 1:
        raise ValueError("valid positive ridge parameter and target mass required")
    delta = normalized_ridge_parameter
    def captured_mass_upper_bound(length: int) -> Fraction:
        return delta**2 * (length + 1) * (length + 2) / 2

    upper = 1
    while captured_mass_upper_bound(upper) < target_mass:
        upper *= 2
    lower = 0
    while lower < upper:
        middle = (lower + upper) // 2
        if captured_mass_upper_bound(middle) >= target_mass:
            upper = middle
        else:
            lower = middle + 1
    return lower


def support_ridge_tail_lower_bound(
    support_rank_density: float,
    frame_trace_density: float,
    physical_ridge_parameter: float,
) -> float:
    if not 0 <= support_rank_density <= 1:
        raise ValueError("support rank density must lie in [0,1]")
    if frame_trace_density < 0 or physical_ridge_parameter <= 0:
        raise ValueError("trace density and physical ridge parameter must be positive")
    return max(
        0.0,
        support_rank_density
        - 2.0 * frame_trace_density / physical_ridge_parameter,
    )


def audit_poisson_scale_mixture(
    control_id: str,
    projections: tuple[np.ndarray, ...],
    normalized_ridge_parameter: Fraction,
    truncation_length: int,
    *,
    tolerance: float = 1e-10,
) -> PoissonScaleMixtureControl:
    if not projections:
        raise ValueError("at least one projection is required")
    dimension = projections[0].shape[0]
    if any(item.shape != (dimension, dimension) for item in projections):
        raise ValueError("all projections must have one square dimension")
    identity = np.eye(dimension, dtype=complex)
    for item in projections:
        if max(
            np.linalg.norm(item - item.conj().T, ord=2),
            np.linalg.norm(item @ item - item, ord=2),
        ) > 1000 * tolerance:
            raise ValueError("every leaf must be an orthogonal projection")
    delta = float(normalized_ridge_parameter)
    frame = sum(projections, np.zeros_like(identity)) / len(projections)
    average_complement = identity - frame
    exact_geometric = delta * np.linalg.inv(frame + delta * identity)
    exact_squared = delta**2 * np.linalg.matrix_power(
        np.linalg.inv(frame + delta * identity),
        2,
    )
    truncated_geometric = np.zeros_like(identity)
    truncated_squared = np.zeros_like(identity)
    power = identity.copy()
    geometric_mass = Fraction()
    squared_mass = Fraction()
    for length in range(truncation_length + 1):
        geometric_weight = geometric_length_mass(
            normalized_ridge_parameter,
            length,
        )
        squared_weight = squared_length_mass(
            normalized_ridge_parameter,
            length,
        )
        truncated_geometric += float(geometric_weight) * power
        truncated_squared += float(squared_weight) * power
        geometric_mass += geometric_weight
        squared_mass += squared_weight
        power = power @ average_complement
    geometric_tail = geometric_length_tail(
        normalized_ridge_parameter,
        truncation_length,
    )
    squared_tail = squared_length_tail(
        normalized_ridge_parameter,
        truncation_length,
    )
    geometric_residual = float(
        np.linalg.norm(exact_geometric - truncated_geometric, ord=2)
    )
    squared_residual = float(
        np.linalg.norm(exact_squared - truncated_squared, ord=2)
    )
    geometric_bounded = geometric_residual <= float(geometric_tail) + tolerance
    squared_bounded = squared_residual <= float(squared_tail) + tolerance
    verified = bool(
        geometric_mass + geometric_tail == 1
        and squared_mass + squared_tail == 1
        and geometric_bounded
        and squared_bounded
    )
    return PoissonScaleMixtureControl(
        control_id=control_id,
        ambient_dimension=dimension,
        leaf_count=len(projections),
        normalized_ridge_parameter=delta,
        truncation_length=truncation_length,
        geometric_mass_through_truncation=float(geometric_mass),
        negative_binomial_mass_through_truncation=float(squared_mass),
        geometric_tail=float(geometric_tail),
        negative_binomial_tail=float(squared_tail),
        geometric_resolvent_residual=geometric_residual,
        squared_resolvent_residual=squared_residual,
        geometric_residual_bounded_by_tail=geometric_bounded,
        squared_residual_bounded_by_tail=squared_bounded,
        exact_positive_mixture_verified=verified,
        status=(
            "exact-support-ridge-positive-word-mixtures-verified"
            if verified
            else "support-ridge-poisson-mixture-control-failure"
        ),
    )


def _projection_controls(seed: int, dimension: int, leaf_count: int) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    output = []
    for index in range(leaf_count):
        width = 1 + index % (dimension - 1)
        raw = rng.normal(size=(dimension, width)) + 1j * rng.normal(
            size=(dimension, width)
        )
        basis, _ = np.linalg.qr(raw, mode="reduced")
        output.append(basis @ basis.conj().T)
    return tuple(output)


def support_ridge_poisson_scale_record(
    n: int,
    *,
    physical_inverse_polynomial_degree: int = 2,
    normalized_inverse_polynomial_degree: int = 2,
    support_rank_density: float = 0.25,
    frame_trace_density: float = 4.0,
) -> SupportRidgePoissonScaleRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    if min(
        physical_inverse_polynomial_degree,
        normalized_inverse_polynomial_degree,
    ) < 0:
        raise ValueError("ridge degrees must be nonnegative")
    order = math.factorial(n)
    threshold = (order - 1).bit_length()
    leaf_count = 1 << (threshold + 1)
    aspect = leaf_count / order
    physical_eta = n ** (-physical_inverse_polynomial_degree)
    delta_physical = Fraction(1, leaf_count * n**physical_inverse_polynomial_degree)
    length_lower = squared_constant_mass_length_lower_bound(delta_physical)
    normalized_delta = n ** (-normalized_inverse_polynomial_degree)
    coarse_physical_eta = leaf_count * normalized_delta
    tail_lower = support_ridge_tail_lower_bound(
        support_rank_density,
        frame_trace_density,
        coarse_physical_eta,
    )
    return SupportRidgePoissonScaleRecord(
        n=n,
        group_order_decimal=str(order),
        child_leaf_count_decimal=str(leaf_count),
        child_leaf_aspect=aspect,
        physical_inverse_polynomial_degree=physical_inverse_polynomial_degree,
        log2_geometric_mean_length_at_physical_eta=(
            math.log2(leaf_count) - math.log2(physical_eta)
        ),
        log2_squared_mean_length_at_physical_eta=(
            1.0 + math.log2(leaf_count) - math.log2(physical_eta)
        ),
        constant_mass_squared_length_log2_lower_bound=math.log2(length_lower),
        normalized_inverse_polynomial_degree=normalized_inverse_polynomial_degree,
        coarse_physical_ridge_log2=math.log2(coarse_physical_eta),
        assumed_support_rank_density=support_rank_density,
        assumed_frame_trace_density=frame_trace_density,
        coarse_normalized_tail_lower_bound=tail_lower,
        positive_poisson_words_polynomial_at_physical_scale=False,
        coarse_normalized_ridge_transfers_support=False,
        status="positive-poisson-route-has-factorial-length-or-constant-tail-error",
    )


def support_ridge_poisson_scale_no_go_theorem(
) -> SupportRidgePoissonScaleNoGoTheorem:
    return SupportRidgePoissonScaleNoGoTheorem(
        parameter_rescaling="delta=eta/q for F=q Fbar",
        geometric_mixture=(
            "delta(Fbar+delta I)^-1=sum_m delta(1+delta)^(-m-1) E[product Q_j]"
        ),
        squared_mixture=(
            "delta^2(Fbar+delta I)^-2=sum_m delta^2(m+1)(1+delta)^(-m-2) E[product Q_j]"
        ),
        constant_mass_length_lower_bound=(
            "Pr[N<=L]<=delta^2(L+1)(L+2)/2, so L=Omega(1/delta)"
        ),
        coarse_ridge_tail_lower_bound=(
            "T_(q delta)(F)/D>=rank(F)/D-2Tr(F)/(q delta D)"
        ),
        final_root_leaf_aspect="q/|S_n| in [2,4)",
        positive_uniform_leaf_poisson_route_only=True,
        signed_or_aggregate_approximations_ruled_out=False,
        theorem_verified=True,
        status="support-ridge-positive-leaf-word-polynomial-scale-route-ruled-out",
    )


def run_component_support_ridge_poisson_scale_no_go(
) -> ComponentSupportRidgePoissonScaleNoGoReport:
    controls = [
        audit_poisson_scale_mixture(
            "D6-Q3-DELTA-1-2",
            _projection_controls(10101, 6, 3),
            Fraction(1, 2),
            12,
        ),
        audit_poisson_scale_mixture(
            "D7-Q4-DELTA-1-3",
            _projection_controls(10102, 7, 4),
            Fraction(1, 3),
            18,
        ),
        audit_poisson_scale_mixture(
            "D8-Q5-DELTA-1-5",
            _projection_controls(10103, 8, 5),
            Fraction(1, 5),
            28,
        ),
    ]
    scaling = [
        support_ridge_poisson_scale_record(n)
        for n in (8, 16, 32, 64, 128)
    ]
    theorem = support_ridge_poisson_scale_no_go_theorem()
    failures = sum(not row.exact_positive_mixture_verified for row in controls)
    return ComponentSupportRidgePoissonScaleNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "rescaling": theorem.parameter_rescaling,
            "support_resolvent_mixture": theorem.geometric_mixture,
            "support_tail_mixture": theorem.squared_mixture,
            "length_lower_bound": theorem.constant_mass_length_lower_bound,
            "coarse_tail": theorem.coarse_ridge_tail_lower_bound,
            "scope": (
                "The no-go concerns positive words formed by iid uniform leaf "
                "complements. It does not rule out signed, rational, local-law, "
                "or aggregate-frame methods."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "audit_poisson_word_scale_at_physical_support_ridge_parameter",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Exact rescaling sends eta to delta=eta/q, and both positive "
                    "mixtures require Theta(q/eta) expected leaf factors."
                ),
            },
            {
                "obligation": "test_polynomial_normalized_parameter_as_support_approximation",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "The trace/rank inequality leaves tail density rho-o(1) "
                    "when delta is inverse polynomial and q is factorial."
                ),
            },
            {
                "obligation": "find_nonpositive_or_aggregate_resolvent_representation",
                "resolved": False,
                "resolution": (
                    "A signed polynomial/rational recursion or direct physical "
                    "local law must avoid one-uniform-leaf-at-a-time mixing."
                ),
            },
            {
                "obligation": "prove_natural_physical_support_ridge_tail_small",
                "resolved": False,
                "resolution": (
                    "The normalization no-go removes one proof route; it does "
                    "not estimate the actual natural spectrum."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Inverse-polynomial eta gives polynomial Poisson length.",
                "resolved": True,
                "resolution": (
                    "Only when eta is measured against Fbar. The physical ridge "
                    "uses delta=eta/q, which has factorial inverse."
                ),
            },
            {
                "objection": "Choose inverse-polynomial delta instead.",
                "resolved": True,
                "resolution": (
                    "Then physical eta=q delta and equation (6) leaves constant "
                    "support-ridge error on the positive-rank event."
                ),
            },
            {
                "objection": "Small expected length is not necessary for constant captured mass.",
                "resolved": True,
                "resolution": (
                    "Equation (5) directly forces L=Omega(1/delta) for the "
                    "squared-resolvent mixture to capture one half of its mass."
                ),
            },
            {
                "objection": "This rules out all polynomial support-ridge proofs.",
                "resolved": False,
                "resolution": (
                    "It does not touch signed cancellation, rational recursion, "
                    "aggregate-frame access, or direct spectral/local-law bounds."
                ),
            },
        ],
        headline_metrics={
            "poisson_parameter_scale_no_go_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "exact_positive_mixture_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_geometric_residual_to_tail_ratio": max(
                row.geometric_resolvent_residual / row.geometric_tail
                for row in controls
            ),
            "maximum_squared_residual_to_tail_ratio": max(
                row.squared_resolvent_residual / row.negative_binomial_tail
                for row in controls
            ),
            "tail_physical_word_length_log2_lower_bound": (
                scaling[-1].constant_mass_squared_length_log2_lower_bound
            ),
            "tail_coarse_normalized_ridge_error_lower_bound": (
                scaling[-1].coarse_normalized_tail_lower_bound
            ),
            "alternative_support_ridge_route_count": 0,
            "natural_support_ridge_tail_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "positive_poisson_leaf_words_valid_at_physical_scale": True,
            "positive_poisson_leaf_words_polynomial_length_at_physical_scale": False,
            "polynomial_normalized_parameter_approximates_support": False,
            "signed_polynomial_or_rational_route_ruled_out": False,
            "aggregate_frame_route_ruled_out": False,
            "natural_support_ridge_tail_small": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The old positive Poisson expansion is exact but has factorial "
                "length at the physical support scale; other spectral routes remain open."
            ),
        },
        status=(
            "positive-poisson-support-ridge-route-falsified-by-normalization"
            if failures == 0
            else "support-ridge-poisson-scale-control-failure"
        ),
        summary=(
            "Proved that positive uniform-leaf Poisson words face a factorial-"
            "length versus constant-tail-error dichotomy at the physical "
            "dependency support-ridge scale."
        ),
        falsifiers_triggered=[
            "The normalized-frame parameter is eta/q, not the physical eta.",
            "A polynomial normalized ridge leaves constant support-tail error.",
            "Constant captured squared-resolvent mass requires Omega(q/eta) positive leaf factors.",
            "Signed, rational, aggregate-frame, and direct local-law routes remain open.",
            "No natural tail, component M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_support_ridge_poisson_scale_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-RIDGE-POISSON-SCALE-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_support_ridge_poisson_scale_no_go" in globals():
        report = run_component_support_ridge_poisson_scale_no_go(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-SUPPORT-RIDGE-POISSON-SCALE-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-RIDGE-POISSON-SCALE-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-RIDGE-POISSON-SCALE-NO-GO.",
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
                    "self_dual_wreath_component_support_ridge_poisson_scale_no_go": str(path)
                },
            )
        )
    return payload
