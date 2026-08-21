"""Scalarization of trimmed natural component supports.

The natural size-biased effect law says that, with
``gamma_n=1/alpha_n in (1/4,1/2]``, the POVM-trace-weighted spectrum of the
exact component effects converges to ``delta_(gamma_n)``.  This module turns
that spectral statement into the compiler normal form it actually supports.

Fix ``theta<1/4`` and define

    K_e = H_e 1_[theta,1](H_e),       Q_e=supp(K_e).       (1)

Let

    v = r^-1 sum_e Tr(H_e(H_e-gamma I)^2),                (2)

the size-biased variance.  The point-mass law gives ``E v->0`` and the
discarded POVM trace ``delta->0``.  On every retained eigenvalue
``lambda>=theta``,

    (lambda-gamma)^2
      <= theta^-1 lambda(lambda-gamma)^2,

    (sqrt(lambda)-sqrt(gamma))^2
      <= (gamma theta)^-1 lambda(lambda-gamma)^2.          (3)

Therefore

    r^-1 sum_e ||K_e-gamma Q_e||_F^2 <= v/theta -> 0,

    r^-1 sum_e ||sqrt(K_e)-sqrt(gamma)Q_e||_F^2
      <= v/(gamma theta) -> 0.                             (4)

If ``W_e=V_e sqrt(H_e)`` is the exact component polar decomposition, the
trimmed Naimark dilation is consequently close, in normalized Hilbert--Schmidt
mean square, to

    |psi> -> sqrt(gamma) sum_e |e> V_e Q_e |psi>.          (5)

The matrix square-root amplitudes have scalarized.  Moreover, the total
retained support rank obeys

    r^-1 sum_e rank(Q_e) -> 1/gamma=alpha,                 (6)

because ``lambda>=theta`` converts the size-biased variance into an unweighted
rank error.  Thus the retained support has only constant aggregate rank
relative to the fiber even though it is distributed over factorially many
leaf labels.

This is an average geometric normal form, not an operator-norm compiler.
Equation (5) still requires coherent support-projector SELECT and compatible
partial isometries ``V_e``.  Pair GPE supplies individual compatible
transports, but no all-leaf support classifier, uniform controlled transport,
or label-sensitive decoder is known.  The theorem redirects the final-root
compiler effort from generic matrix square roots to structured support access.
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
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_trimmed_support_scalarization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-TRIMMED-SUPPORT-SCALARIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TrimmedSupportScalarizationControl:
    control_id: str
    fiber_dimension: int
    leaf_count: int
    target_support_scalar: float
    trim_threshold: float
    normalized_discarded_trace: float
    normalized_size_biased_variance: float
    normalized_effect_support_scalar_error: float
    effect_error_upper_bound: float
    normalized_square_root_support_scalar_error: float
    square_root_error_upper_bound: float
    aggregate_retained_support_rank: int
    normalized_aggregate_retained_support_rank: float
    target_normalized_aggregate_support_rank: float
    normalized_support_rank_error: float
    support_rank_error_upper_bound: float
    maximum_effect_commutator_norm: float
    scalarization_bounds_verified: bool
    status: str


@dataclass(frozen=True)
class SupportScalarizationScalingRecord:
    child_aspect: float
    target_support_scalar: float
    fixed_trim_threshold: float
    assumed_size_biased_variance: float
    effect_support_scalar_error_upper_bound: float
    square_root_dilation_error_upper_bound: float
    aggregate_support_rank_to_fiber_target: float
    matrix_square_root_amplitude_required_asymptotically: bool
    coherent_support_projector_select_proved: bool
    uniform_partial_isometry_transport_proved: bool
    status: str


@dataclass(frozen=True)
class TrimmedSupportScalarizationTheorem:
    variance: str
    effect_scalarization: str
    root_scalarization: str
    naimark_normal_form: str
    aggregate_support_rank: str
    exact_dependency_scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentTrimmedSupportScalarizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: TrimmedSupportScalarizationTheorem
    finite_controls: list[TrimmedSupportScalarizationControl]
    scaling_records: list[SupportScalarizationScalingRecord]
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
        raise ValueError("effects must have one nonzero square dimension")
    total = np.zeros((dimension, dimension), dtype=complex)
    for effect in effects:
        if np.linalg.eigvalsh(_hermitian(effect))[0] < -100 * tolerance:
            raise ValueError("effects must be positive semidefinite")
        total += effect
    if np.linalg.norm(total - np.eye(dimension), ord=2) > 1000 * tolerance:
        raise ValueError("effects must sum to identity")
    return dimension


def support_scalarization_bounds(
    normalized_size_biased_variance: float,
    support_scalar: float,
    trim_threshold: float,
) -> tuple[float, float]:
    if normalized_size_biased_variance < 0:
        raise ValueError("variance must be nonnegative")
    if not 0 < support_scalar <= 1 or not 0 < trim_threshold < support_scalar:
        raise ValueError("require 0<threshold<support scalar<=1")
    return (
        normalized_size_biased_variance / trim_threshold,
        normalized_size_biased_variance / (support_scalar * trim_threshold),
    )


def support_rank_error_bound(
    normalized_size_biased_variance: float,
    support_scalar: float,
    trim_threshold: float,
) -> float:
    if normalized_size_biased_variance < 0:
        raise ValueError("variance must be nonnegative")
    if not 0 < support_scalar <= 1 or not 0 < trim_threshold < support_scalar:
        raise ValueError("require 0<threshold<support scalar<=1")
    return math.sqrt(normalized_size_biased_variance) / (
        support_scalar * trim_threshold
    )


def _two_frame_weighted_povm(weight: float) -> tuple[np.ndarray, ...]:
    if not 0 < weight < 1:
        raise ValueError("weight must lie in (0,1)")
    dimension = 4
    base = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    identity = np.eye(dimension, dtype=complex)
    cosine = math.cos(math.pi / 8)
    sine = math.sin(math.pi / 8)
    rotation = np.asarray(
        [
            [cosine, 0.0, -sine, 0.0],
            [0.0, cosine, 0.0, -sine],
            [sine, 0.0, cosine, 0.0],
            [0.0, sine, 0.0, cosine],
        ],
        dtype=complex,
    )
    moved = rotation @ base @ rotation.conj().T
    return (
        weight * base,
        weight * (identity - base),
        (1.0 - weight) * moved,
        (1.0 - weight) * (identity - moved),
    )


def audit_trimmed_support_scalarization(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    support_scalar: float,
    trim_threshold: float,
    *,
    tolerance: float = 1e-9,
) -> TrimmedSupportScalarizationControl:
    dimension = _validate_povm(effects, tolerance=tolerance)
    if not 0 < trim_threshold < support_scalar <= 1:
        raise ValueError("require 0<threshold<support scalar<=1")

    variance = 0.0
    discarded = 0.0
    effect_error = 0.0
    root_error = 0.0
    aggregate_rank = 0
    for effect in effects:
        values, vectors = np.linalg.eigh(_hermitian(effect))
        positive = values > 100 * tolerance
        variance += float(
            np.sum(values[positive] * (values[positive] - support_scalar) ** 2)
        )
        retained = values >= trim_threshold
        discarded += float(np.sum(values[positive & ~retained]))
        retained_values = values[retained]
        aggregate_rank += int(np.count_nonzero(retained))
        effect_error += float(np.sum((retained_values - support_scalar) ** 2))
        root_error += float(
            np.sum((np.sqrt(retained_values) - math.sqrt(support_scalar)) ** 2)
        )

    variance /= dimension
    discarded /= dimension
    effect_error /= dimension
    root_error /= dimension
    effect_bound, root_bound = support_scalarization_bounds(
        variance,
        support_scalar,
        trim_threshold,
    )
    rank_ratio = aggregate_rank / dimension
    rank_target = 1.0 / support_scalar
    rank_error = abs(rank_ratio - rank_target)
    rank_bound = discarded / support_scalar + support_rank_error_bound(
        variance,
        support_scalar,
        trim_threshold,
    )
    commutator = max(
        float(np.linalg.norm(left @ right - right @ left, ord=2))
        for left in effects
        for right in effects
    )
    verified = bool(
        effect_error <= effect_bound + 1000 * tolerance
        and root_error <= root_bound + 1000 * tolerance
        and rank_error <= rank_bound + 1000 * tolerance
        and commutator > 1000 * tolerance
    )
    return TrimmedSupportScalarizationControl(
        control_id=control_id,
        fiber_dimension=dimension,
        leaf_count=len(effects),
        target_support_scalar=support_scalar,
        trim_threshold=trim_threshold,
        normalized_discarded_trace=discarded,
        normalized_size_biased_variance=variance,
        normalized_effect_support_scalar_error=effect_error,
        effect_error_upper_bound=effect_bound,
        normalized_square_root_support_scalar_error=root_error,
        square_root_error_upper_bound=root_bound,
        aggregate_retained_support_rank=aggregate_rank,
        normalized_aggregate_retained_support_rank=rank_ratio,
        target_normalized_aggregate_support_rank=rank_target,
        normalized_support_rank_error=rank_error,
        support_rank_error_upper_bound=rank_bound,
        maximum_effect_commutator_norm=commutator,
        scalarization_bounds_verified=verified,
        status=(
            "trimmed-support-and-square-root-scalarization-verified"
            if verified
            else "trimmed-support-scalarization-control-failure"
        ),
    )


def support_scalarization_scaling_record(
    child_aspect: float,
    assumed_size_biased_variance: float,
) -> SupportScalarizationScalingRecord:
    if not 2 <= child_aspect <= 4:
        raise ValueError("the natural final-root aspect lies in [2,4]")
    if assumed_size_biased_variance < 0:
        raise ValueError("variance must be nonnegative")
    gamma = 1.0 / child_aspect
    effect, root = support_scalarization_bounds(
        assumed_size_biased_variance,
        gamma,
        UNIFORM_EFFECT_EDGE_THRESHOLD,
    )
    return SupportScalarizationScalingRecord(
        child_aspect=child_aspect,
        target_support_scalar=gamma,
        fixed_trim_threshold=UNIFORM_EFFECT_EDGE_THRESHOLD,
        assumed_size_biased_variance=assumed_size_biased_variance,
        effect_support_scalar_error_upper_bound=effect,
        square_root_dilation_error_upper_bound=root,
        aggregate_support_rank_to_fiber_target=child_aspect,
        matrix_square_root_amplitude_required_asymptotically=False,
        coherent_support_projector_select_proved=False,
        uniform_partial_isometry_transport_proved=False,
        status="matrix-amplitudes-scalarized-support-select-and-transport-open",
    )


def trimmed_support_scalarization_theorem() -> TrimmedSupportScalarizationTheorem:
    return TrimmedSupportScalarizationTheorem(
        variance=(
            "v_n=r_n^-1 sum_e Tr(H_e(H_e-gamma_n I)^2)->0 from the first "
            "three size-biased moments"
        ),
        effect_scalarization=(
            "sum_e||K_e-gamma_n Q_e||F^2/r_n<=v_n/theta"
        ),
        root_scalarization=(
            "sum_e||sqrt(K_e)-sqrt(gamma_n)Q_e||F^2/r_n"
            "<=v_n/(gamma_n theta)"
        ),
        naimark_normal_form=(
            "the trimmed component dilation is normalized-Frobenius close to "
            "sqrt(gamma_n) stack_e V_e Q_e"
        ),
        aggregate_support_rank=(
            "sum_e rank(Q_e)/r_n->1/gamma_n=alpha_n"
        ),
        exact_dependency_scope=(
            "all statements are annealed after exact dependency compression and "
            "global-distinct conditioning; no operator-norm or sourcewise claim"
        ),
        theorem_verified=True,
        status="natural-trimmed-component-support-scalarization-proved",
    )


def run_component_trimmed_support_scalarization(
) -> ComponentTrimmedSupportScalarizationReport:
    controls = [
        audit_trimmed_support_scalarization(
            "EXACT-BALANCED-TWO-FRAME",
            _two_frame_weighted_povm(0.5),
            0.5,
            0.2,
        ),
        audit_trimmed_support_scalarization(
            "PERTURBED-TWO-FRAME-0.55-0.45",
            _two_frame_weighted_povm(0.55),
            0.5,
            0.2,
        ),
        audit_trimmed_support_scalarization(
            "PERTURBED-TWO-FRAME-0.60-0.40",
            _two_frame_weighted_povm(0.60),
            0.5,
            0.2,
        ),
    ]
    scaling = [
        support_scalarization_scaling_record(
            alpha,
            1.0 / n,
        )
        for n, alpha in (
            (32, 2.0),
            (64, 2.25),
            (128, 2.5),
            (256, 3.0),
            (512, 3.5),
            (1024, 4.0),
        )
    ]
    theorem = trimmed_support_scalarization_theorem()
    failures = sum(not row.scalarization_bounds_verified for row in controls)
    verified = theorem.theorem_verified and failures == 0
    tail = scaling[-1]
    return ComponentTrimmedSupportScalarizationReport(
        created_at=utc_now(),
        theorem_contract={
            "variance": theorem.variance,
            "effects": theorem.effect_scalarization,
            "square_roots": theorem.root_scalarization,
            "dilation": theorem.naimark_normal_form,
            "rank": theorem.aggregate_support_rank,
            "scope": theorem.exact_dependency_scope,
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "convert_size_biased_point_mass_law_to_effect_scalarization",
                "resolved": verified,
                "resolution": (
                    "The first three size-biased moments make v_n vanish, and "
                    "the fixed retained threshold removes the missing lambda factor."
                ),
            },
            {
                "obligation": "scalarize_component_square_root_amplitudes",
                "resolved": verified,
                "resolution": (
                    "The scalar square-root inequality in (3) controls the full "
                    "stacked Naimark map in normalized Frobenius mean square."
                ),
            },
            {
                "obligation": "bound_total_retained_support_rank",
                "resolved": verified,
                "resolution": (
                    "The retained threshold converts weighted variance to an "
                    "unweighted support-count error, yielding total rank alpha*r."
                ),
            },
            {
                "obligation": "compile_coherent_support_projector_select",
                "resolved": False,
                "resolution": (
                    "Need a reversible classifier or direct representation circuit "
                    "for Q_e on a superposition of factorially many leaf labels."
                ),
            },
            {
                "obligation": "compile_uniform_partial_isometry_transport",
                "resolved": False,
                "resolution": (
                    "Pair GPE proves individual compatible transports, not a "
                    "global controlled support/gauge network on natural mass."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Trace-weighted convergence cannot control unweighted supports.",
                "resolved": True,
                "resolution": (
                    "It cannot near zero. After retaining lambda>=theta, division "
                    "by the fixed theta converts the weighted variance exactly."
                ),
            },
            {
                "objection": "Noncommuting effects require non-scalar eigenvalue amplitudes.",
                "resolved": True,
                "resolution": (
                    "False. The finite fusion controls are noncommuting while every "
                    "positive effect eigenvalue is the same scalar; geometry sits "
                    "in the support projectors and partial isometries."
                ),
            },
            {
                "objection": "Aggregate Frobenius scalarization is operator-norm access.",
                "resolved": True,
                "resolution": (
                    "No. Exceptional source blocks and eigenchannels may remain; "
                    "the theorem controls only annealed normalized mean square."
                ),
            },
            {
                "objection": "Scalar amplitudes make a mask-Hadamard circuit sufficient.",
                "resolved": False,
                "resolution": (
                    "The supports Q_e are sparse, noncommuting, and mask dependent. "
                    "Their SELECT and the V_e transports carry the hard geometry."
                ),
            },
        ],
        headline_metrics={
            "trimmed_effect_support_scalarization_theorem_count": int(verified),
            "trimmed_square_root_dilation_scalarization_theorem_count": int(verified),
            "aggregate_retained_support_rank_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "uniform_trim_threshold": UNIFORM_EFFECT_EDGE_THRESHOLD,
            "tail_assumed_variance": tail.assumed_size_biased_variance,
            "tail_square_root_error_upper_bound": tail.square_root_dilation_error_upper_bound,
            "matrix_square_root_amplitude_gate_count": 0,
            "coherent_support_projector_select_count": 0,
            "uniform_partial_isometry_transport_count": 0,
            "component_povm_dilation_circuit_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_trimmed_effects_support_scalar_in_aggregate": verified,
            "natural_trimmed_square_roots_support_scalar_in_aggregate": verified,
            "aggregate_retained_support_rank_is_alpha_times_fiber": verified,
            "generic_matrix_square_root_amplitudes_are_final_root_bottleneck": False,
            "operator_norm_support_scalarization_proved": False,
            "sourcewise_support_scalarization_proved": False,
            "coherent_support_projector_select_proved": False,
            "uniform_gpe_support_transport_proved": False,
            "component_povm_dilation_compiled": False,
            "decoder_information_gain_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The retained matrix amplitudes become scalar, but their sparse "
                "noncommuting supports and controlled partial-isometry gauges are "
                "still not coherently accessible."
            ),
        },
        status=(
            theorem.status
            if verified
            else "component-trimmed-support-scalarization-control-failure"
        ),
        summary=(
            "Reduced the retained natural component dilation to scalar amplitudes "
            "on sparse support projectors with total rank alpha times the fiber."
        ),
        falsifiers_triggered=[
            "Natural noncommutativity can reside entirely in support geometry while positive effect amplitudes scalarize.",
            "Generic matrix square-root synthesis is not the final-root bottleneck after constant trace trim.",
            "Factorially many labels do not imply factorial aggregate retained support rank.",
            "Average support scalarization does not provide coherent support SELECT or a decoder.",
        ],
    )


def write_component_trimmed_support_scalarization_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-TRIMMED-SUPPORT-SCALARIZATION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_trimmed_support_scalarization" in globals():
        report = run_component_trimmed_support_scalarization(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-TRIMMED-SUPPORT-SCALARIZATION",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-TRIMMED-SUPPORT-SCALARIZATION.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-TRIMMED-SUPPORT-SCALARIZATION.",
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
                    "self_dual_wreath_component_trimmed_support_scalarization": str(path)
                },
            )
        )
    return payload
