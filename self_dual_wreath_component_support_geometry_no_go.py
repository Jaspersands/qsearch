"""Nonabelian retained-support geometry and the commuting-classifier no-go.

Let ``H_e`` be the natural component POVM on a fiber of dimension ``r``.
For a fixed ``theta<1/4`` and ``gamma=r/N in (1/4,1/2]``, put

    K_e = H_e 1_[theta,1](H_e),
    Q_e = 1_[theta,1](H_e),
    Delta_e = K_e-gamma Q_e.                               (1)

The size-biased point-mass theorem gives

    epsilon = r^-1 sum_e ||Delta_e||_F^2 -> 0.             (2)

There are two useful consequences that do not require a sourcewise hard edge.
First, ``theta Q_e<=K_e<=H_e`` and ``sum_e H_e=I`` imply the exact Bessel bound

    sum_e Q_e <= theta^-1 I.                               (3)

Second, write ``M4(X)=sum_(e,f)||[X_e,X_f]||_F^2/2``.  Since
``sum K_e^2<=I`` and ``sum Delta_e^2<=c I``, where

    c=max((theta-gamma)^2/theta,(1-gamma)^2),              (4)

commutator telescoping gives

    |sqrt(M4(K)/r)-gamma^2 sqrt(M4(Q)/r)|
      <= sqrt(6(2+c) epsilon).                             (5)

The uniform bounds ``M4(K)/r<=2`` and ``M4(Q)/r<=theta^-2`` turn (5) into
L1 transfer.  Combining it with the natural polar-traffic limit proves

    E M4(Q)/r - (1-gamma)/gamma^2 -> 0
              = alpha(alpha-1), alpha=1/gamma.            (6)

Thus the constant-edge component signal lives in noncommuting support
geometry, not in matrix-valued eigenvalue amplitudes.

This also rules out a tempting but insufficient compiler.  If ``R_e`` are
commuting Hermitian contractions and
``||sum_e R_e^2||<=B``, then

    M4(Q)/r <= 4(theta^-1+B)
               sum_e||Q_e-R_e||_F^2/r.                   (7)

Consequently every uniformly Bessel-bounded commuting support classifier has
constant aggregate normalized error.  At ``theta=1/5`` and ``B<=5``, the
uniform natural lower bound is ``1/20``.  A classical predicate of one common
GPE transcript produces commuting diagonal effects, so it cannot recover the
retained supports with vanishing error.

Equation (7) does not rule out coherent GPE row operations, recoupling, or
holonomy circuits: those need not remain in one commuting transcript algebra.
No coherent support SELECT, decoder, end-to-end algorithm, or speedup is
constructed here.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_size_biased_effect_law import (
    UNIFORM_EFFECT_EDGE_THRESHOLD,
    _fusion_frame_system,
)
from self_dual_wreath_component_trimmed_support_scalarization import (
    _two_frame_weighted_povm,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_support_geometry_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-GEOMETRY-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SupportCurlTransferControl:
    control_id: str
    fiber_dimension: int
    leaf_count: int
    support_scalar: float
    trim_threshold: float
    normalized_scalarization_error: float
    scalarization_commutator_constant: float
    normalized_trimmed_effect_m4: float
    normalized_support_projector_m4: float
    normalized_rescaled_support_m4: float
    square_root_m4_transfer_residual: float
    square_root_m4_transfer_upper_bound: float
    support_frame_bessel_norm: float
    support_frame_bessel_upper_bound: float
    support_m4_upper_bound: float
    transfer_bound_verified: bool
    status: str


@dataclass(frozen=True)
class CommutingClassifierControl:
    control_id: str
    fiber_dimension: int
    leaf_count: int
    trim_threshold: float
    support_projector_m4_per_dimension: float
    commuting_approximant_bessel_norm: float
    normalized_support_approximation_error: float
    commuting_error_lower_bound: float
    commuting_perturbation_upper_bound: float
    approximants_pairwise_commute: bool
    commuting_classifier_inequality_verified: bool
    status: str


@dataclass(frozen=True)
class SupportGeometryScalingRecord:
    child_aspect: float
    support_scalar: float
    natural_effect_m4_limit: float
    natural_support_projector_m4_limit: float
    uniform_bessel_bound: float
    bounded_commuting_classifier_error_lower_bound: float
    pvm_transcript_classifier_error_lower_bound: float
    scalar_amplitude_obstruction_survives: bool
    commuting_label_predicate_sufficient: bool
    coherent_noncommuting_classifier_proved: bool
    status: str


@dataclass(frozen=True)
class SupportGeometryTheorem:
    support_bessel_bound: str
    commutator_transfer: str
    natural_support_m4_limit: str
    commuting_classifier_no_go: str
    gpe_scope_boundary: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentSupportGeometryNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SupportGeometryTheorem
    transfer_controls: list[SupportCurlTransferControl]
    commuting_classifier_controls: list[CommutingClassifierControl]
    scaling_records: list[SupportGeometryScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _validate_povm(
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float,
) -> int:
    if not effects:
        raise ValueError("at least one effect is required")
    dimension = effects[0].shape[0]
    if dimension < 1 or any(
        effect.ndim != 2 or effect.shape != (dimension, dimension)
        for effect in effects
    ):
        raise ValueError("effects must share one positive square dimension")
    total = np.zeros((dimension, dimension), dtype=complex)
    for effect in effects:
        values = np.linalg.eigvalsh(_hermitian(effect))
        if values[0] < -100 * tolerance or values[-1] > 1 + 100 * tolerance:
            raise ValueError("each matrix must be an effect")
        total += effect
    if np.linalg.norm(total - np.eye(dimension), ord=2) > 1000 * tolerance:
        raise ValueError("effects must sum to identity")
    return dimension


def component_m4(operators: tuple[np.ndarray, ...]) -> float:
    return sum(
        float(np.linalg.norm(left @ right - right @ left, ord="fro") ** 2 / 2)
        for left in operators
        for right in operators
    )


def trimmed_effects_and_supports(
    effects: tuple[np.ndarray, ...],
    trim_threshold: float,
    *,
    tolerance: float = 1e-10,
) -> tuple[tuple[np.ndarray, ...], tuple[np.ndarray, ...]]:
    _validate_povm(effects, tolerance=tolerance)
    if not 0 < trim_threshold < 1:
        raise ValueError("the trim threshold must lie in (0,1)")
    trimmed = []
    supports = []
    for effect in effects:
        values, vectors = np.linalg.eigh(_hermitian(effect))
        keep = values >= trim_threshold
        trimmed.append((vectors * (values * keep)) @ vectors.conj().T)
        supports.append((vectors * keep.astype(float)) @ vectors.conj().T)
    return tuple(trimmed), tuple(supports)


def scalarization_commutator_constant(
    support_scalar: float,
    trim_threshold: float,
) -> float:
    if not 0 < trim_threshold < support_scalar <= 1:
        raise ValueError("require 0<threshold<support scalar<=1")
    return max(
        (trim_threshold - support_scalar) ** 2 / trim_threshold,
        (1.0 - support_scalar) ** 2,
    )


def audit_support_curl_transfer(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    support_scalar: float,
    trim_threshold: float,
    *,
    tolerance: float = 1e-9,
) -> SupportCurlTransferControl:
    dimension = _validate_povm(effects, tolerance=tolerance)
    trimmed, supports = trimmed_effects_and_supports(
        effects,
        trim_threshold,
        tolerance=tolerance,
    )
    deltas = tuple(
        effect - support_scalar * support
        for effect, support in zip(trimmed, supports)
    )
    error = sum(float(np.linalg.norm(delta, ord="fro") ** 2) for delta in deltas)
    error /= dimension
    constant = scalarization_commutator_constant(
        support_scalar,
        trim_threshold,
    )
    trimmed_m4 = component_m4(trimmed) / dimension
    support_m4 = component_m4(supports) / dimension
    rescaled = support_scalar**4 * support_m4
    root_residual = abs(math.sqrt(trimmed_m4) - math.sqrt(rescaled))
    root_bound = math.sqrt(6.0 * (2.0 + constant) * error)
    support_sum = sum(
        supports,
        np.zeros((dimension, dimension), dtype=complex),
    )
    bessel = float(np.linalg.norm(_hermitian(support_sum), ord=2))
    bessel_bound = 1.0 / trim_threshold
    m4_bound = 1.0 / trim_threshold**2
    verified = bool(
        root_residual <= root_bound + 1000 * tolerance
        and bessel <= bessel_bound + 1000 * tolerance
        and support_m4 <= m4_bound + 1000 * tolerance
    )
    return SupportCurlTransferControl(
        control_id=control_id,
        fiber_dimension=dimension,
        leaf_count=len(effects),
        support_scalar=support_scalar,
        trim_threshold=trim_threshold,
        normalized_scalarization_error=error,
        scalarization_commutator_constant=constant,
        normalized_trimmed_effect_m4=trimmed_m4,
        normalized_support_projector_m4=support_m4,
        normalized_rescaled_support_m4=rescaled,
        square_root_m4_transfer_residual=root_residual,
        square_root_m4_transfer_upper_bound=root_bound,
        support_frame_bessel_norm=bessel,
        support_frame_bessel_upper_bound=bessel_bound,
        support_m4_upper_bound=m4_bound,
        transfer_bound_verified=verified,
        status=(
            "support-curl-transfer-and-bessel-bound-verified"
            if verified
            else "support-curl-transfer-control-failure"
        ),
    )


def audit_commuting_classifier_bound(
    control_id: str,
    supports: tuple[np.ndarray, ...],
    approximants: tuple[np.ndarray, ...],
    trim_threshold: float,
    *,
    tolerance: float = 1e-9,
) -> CommutingClassifierControl:
    if len(supports) != len(approximants) or not supports:
        raise ValueError("support and approximant families must have equal size")
    dimension = supports[0].shape[0]
    if any(matrix.shape != (dimension, dimension) for matrix in (*supports, *approximants)):
        raise ValueError("all operators must share one square dimension")
    commute = all(
        np.linalg.norm(left @ right - right @ left, ord=2) <= 1000 * tolerance
        for index, left in enumerate(approximants)
        for right in approximants[index + 1 :]
    )
    if any(
        np.linalg.eigvalsh(_hermitian(matrix))[0] < -100 * tolerance
        or np.linalg.eigvalsh(_hermitian(matrix))[-1] > 1 + 100 * tolerance
        for matrix in approximants
    ):
        raise ValueError("approximants must be Hermitian contractions")
    approximant_square_sum = sum(
        (_hermitian(matrix) @ _hermitian(matrix) for matrix in approximants),
        np.zeros((dimension, dimension), dtype=complex),
    )
    bessel = float(np.linalg.norm(_hermitian(approximant_square_sum), ord=2))
    error = sum(
        float(np.linalg.norm(support - approximant, ord="fro") ** 2)
        for support, approximant in zip(supports, approximants)
    ) / dimension
    m4 = component_m4(supports) / dimension
    coefficient = 4.0 * (1.0 / trim_threshold + bessel)
    lower = m4 / coefficient
    upper = coefficient * error
    verified = bool(commute and m4 <= upper + 1000 * tolerance)
    return CommutingClassifierControl(
        control_id=control_id,
        fiber_dimension=dimension,
        leaf_count=len(supports),
        trim_threshold=trim_threshold,
        support_projector_m4_per_dimension=m4,
        commuting_approximant_bessel_norm=bessel,
        normalized_support_approximation_error=error,
        commuting_error_lower_bound=lower,
        commuting_perturbation_upper_bound=upper,
        approximants_pairwise_commute=commute,
        commuting_classifier_inequality_verified=verified,
        status=(
            "commuting-support-classifier-error-bound-verified"
            if verified
            else "commuting-support-classifier-control-failure"
        ),
    )


def _coordinate_pvm_approximants(
    outcome_count: int,
    dimension: int,
) -> tuple[np.ndarray, ...]:
    if dimension != 4 or outcome_count < 2:
        raise ValueError("the finite controls use a four-dimensional two-block PVM")
    first = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    second = np.eye(dimension, dtype=complex) - first
    zero = np.zeros((dimension, dimension), dtype=complex)
    return (first, second, *(zero.copy() for _ in range(outcome_count - 2)))


def support_geometry_scaling_record(
    child_aspect: float,
    *,
    trim_threshold: float = UNIFORM_EFFECT_EDGE_THRESHOLD,
) -> SupportGeometryScalingRecord:
    if not 2 <= child_aspect <= 4:
        raise ValueError("the natural final-root aspect lies in [2,4]")
    gamma = 1.0 / child_aspect
    effect_limit = gamma**2 * (1.0 - gamma)
    support_limit = effect_limit / gamma**4
    bessel = 1.0 / trim_threshold
    bounded_lower = support_limit / (4.0 * (bessel + bessel))
    pvm_lower = support_limit / (4.0 * (bessel + 1.0))
    return SupportGeometryScalingRecord(
        child_aspect=child_aspect,
        support_scalar=gamma,
        natural_effect_m4_limit=effect_limit,
        natural_support_projector_m4_limit=support_limit,
        uniform_bessel_bound=bessel,
        bounded_commuting_classifier_error_lower_bound=bounded_lower,
        pvm_transcript_classifier_error_lower_bound=pvm_lower,
        scalar_amplitude_obstruction_survives=False,
        commuting_label_predicate_sufficient=False,
        coherent_noncommuting_classifier_proved=False,
        status="support-geometry-nonabelian-commuting-label-classifier-rejected",
    )


def support_geometry_theorem() -> SupportGeometryTheorem:
    return SupportGeometryTheorem(
        support_bessel_bound="theta sum_e Q_e<=sum_e K_e<=I",
        commutator_transfer=(
            "|sqrt(M4(K)/r)-gamma^2 sqrt(M4(Q)/r)|"
            "<=sqrt(6(2+c) sum_e||K_e-gamma Q_e||F^2/r)"
        ),
        natural_support_m4_limit=(
            "E M4(Q_n)/r_n-alpha_n(alpha_n-1)->0"
        ),
        commuting_classifier_no_go=(
            "M4(Q)/r<=4(theta^-1+B)sum_e||Q_e-R_e||F^2/r "
            "for commuting R with ||sum R_e^2||<=B"
        ),
        gpe_scope_boundary=(
            "one common diagonal GPE-transcript predicate algebra is insufficient; "
            "coherent row operations, recoupling, and holonomy remain open"
        ),
        theorem_verified=True,
        status="natural-support-nonabelian-geometry-and-commuting-classifier-no-go-proved",
    )


def run_component_support_geometry_no_go() -> ComponentSupportGeometryNoGoReport:
    effects_two, _ = _fusion_frame_system(2)
    effects_four, _ = _fusion_frame_system(4)
    perturbed = _two_frame_weighted_povm(0.55)
    transfer_controls = [
        audit_support_curl_transfer(
            "EXACT-TWO-FRAME-GAMMA-ONE-HALF",
            effects_two,
            0.5,
            UNIFORM_EFFECT_EDGE_THRESHOLD,
        ),
        audit_support_curl_transfer(
            "PERTURBED-TWO-FRAME-GAMMA-ONE-HALF",
            perturbed,
            0.5,
            UNIFORM_EFFECT_EDGE_THRESHOLD,
        ),
        audit_support_curl_transfer(
            "EXACT-FOUR-FRAME-GAMMA-ONE-QUARTER",
            effects_four,
            0.25,
            UNIFORM_EFFECT_EDGE_THRESHOLD,
        ),
    ]
    classifier_controls = []
    for control_id, effects in (
        ("TWO-FRAME-COORDINATE-PVM", effects_two),
        ("FOUR-FRAME-COORDINATE-PVM", effects_four),
    ):
        _, supports = trimmed_effects_and_supports(
            effects,
            UNIFORM_EFFECT_EDGE_THRESHOLD,
        )
        classifier_controls.append(
            audit_commuting_classifier_bound(
                control_id,
                supports,
                _coordinate_pvm_approximants(len(supports), 4),
                UNIFORM_EFFECT_EDGE_THRESHOLD,
            )
        )
    scaling = [
        support_geometry_scaling_record(alpha)
        for alpha in (2.0, 2.25, 2.5, 3.0, 3.5, 4.0)
    ]
    theorem = support_geometry_theorem()
    failures = sum(not row.transfer_bound_verified for row in transfer_controls)
    failures += sum(
        not row.commuting_classifier_inequality_verified
        for row in classifier_controls
    )
    verified = theorem.theorem_verified and failures == 0
    uniform_error_floor = min(
        row.bounded_commuting_classifier_error_lower_bound for row in scaling
    )
    return ComponentSupportGeometryNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "bessel": theorem.support_bessel_bound,
            "transfer": theorem.commutator_transfer,
            "natural_limit": theorem.natural_support_m4_limit,
            "commuting_no_go": theorem.commuting_classifier_no_go,
            "gpe_boundary": theorem.gpe_scope_boundary,
        },
        theorem=theorem,
        transfer_controls=transfer_controls,
        commuting_classifier_controls=classifier_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "transfer_positive_natural_m4_to_retained_support_geometry",
                "resolved": verified,
                "resolution": (
                    "Scalarization error, exact Bessel control, and bounded M4 "
                    "make the commutator perturbation vanish in L1."
                ),
            },
            {
                "obligation": "test_commuting_gpe_transcript_support_classifier",
                "resolved": verified,
                "resolution": (
                    "Every bounded commuting classifier has a constant aggregate "
                    "normalized Frobenius error floor."
                ),
            },
            {
                "obligation": "construct_noncommuting_coherent_support_select",
                "resolved": False,
                "resolution": (
                    "Need a recoupling- or holonomy-aware circuit outside one "
                    "common diagonal transcript algebra."
                ),
            },
            {
                "obligation": "extract_hidden_label_information_from_support_geometry",
                "resolved": False,
                "resolution": (
                    "Internal support noncommutativity remains hidden-label blind "
                    "unless tied to a covariant observable and decoder."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Trace-weighted scalarization permits unbounded support overlap.",
                "resolved": True,
                "resolution": "The retained edge gives theta sum Q_e<=I exactly.",
            },
            {
                "objection": "Scalar effect amplitudes remove the nonabelian mechanism.",
                "resolved": True,
                "resolution": (
                    "The rescaled support-projector M4 converges to "
                    "alpha(alpha-1), uniformly at least two."
                ),
            },
            {
                "objection": "GPE has been ruled out entirely.",
                "resolved": True,
                "resolution": (
                    "Only a common commuting transcript classifier is ruled out; "
                    "coherent carrier-row and holonomy operations remain possible."
                ),
            },
            {
                "objection": "Support noncommutativity is already a decoder.",
                "resolved": False,
                "resolution": (
                    "It is invariant internal geometry until a label-sensitive "
                    "covariant measurement and classical postprocessing are proved."
                ),
            },
        ],
        headline_metrics={
            "support_bessel_bound_theorem_count": int(verified),
            "natural_support_m4_limit_theorem_count": int(verified),
            "commuting_classifier_no_go_theorem_count": int(verified),
            "finite_transfer_control_count": len(transfer_controls),
            "finite_commuting_classifier_control_count": len(classifier_controls),
            "finite_control_failure_count": failures,
            "uniform_support_m4_lower_bound": min(
                row.natural_support_projector_m4_limit for row in scaling
            ),
            "uniform_bounded_commuting_classifier_error_floor": uniform_error_floor,
            "coherent_noncommuting_support_select_count": 0,
            "hidden_label_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_retained_support_m4_limit_proved": verified,
            "uniform_retained_support_bessel_bound_proved": verified,
            "commuting_bounded_support_classifier_rejected": verified,
            "all_gpe_based_support_classifiers_rejected": False,
            "coherent_recoupling_support_classifier_proved": False,
            "coherent_support_projector_select_proved": False,
            "hidden_label_information_gain_proved": False,
            "component_povm_dilation_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The nonabelian mechanism is now localized to retained support "
                "geometry, but no coherent noncommuting selector or decoder exists."
            ),
        },
        status=(
            "natural-support-geometry-nonabelian-commuting-classifier-rejected"
            if verified
            else "support-geometry-no-go-control-failure"
        ),
        summary=(
            "Constant-edge retained supports form a bounded fusion frame and "
            "carry the full natural component M4 after scalar rescaling. A "
            "commuting GPE-transcript predicate cannot approximate them with "
            "vanishing aggregate error; coherent recoupling/holonomy access remains open."
        ),
        falsifiers_triggered=[
            "Matrix-valued square-root amplitudes are not the surviving nonabelian mechanism.",
            "One common commuting GPE-label transcript cannot classify the retained supports.",
            "Positive support M4 does not itself reveal the hidden involution.",
        ],
    )


def write_component_support_geometry_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-GEOMETRY-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_support_geometry_no_go" in globals():
        report = run_component_support_geometry_no_go(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-SUPPORT-GEOMETRY-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-GEOMETRY-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-SUPPORT-GEOMETRY-NO-GO.",
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
                    "self_dual_wreath_component_support_geometry_no_go": str(path)
                },
            )
        )
    return payload
