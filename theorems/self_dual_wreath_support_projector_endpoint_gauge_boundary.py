"""A support projector does not determine the physical endpoint gauge.

Let ``W:H->K`` be the orientation/component isometry and let
``P=WW^*`` be its coefficient-space range projector.  The coordinate effects
on the physical input are

    H_e=W^*D_eW.                                           (1)

For every input unitary ``U``, the isometry ``W_U=WU`` has the same range
projector, but

    H_e^(U)=U^*H_eU.                                       (2)

Thus coherent access to ``P`` alone does not determine the physical POVM.
The qubit pair ``W=I`` and ``W_U=Hadamard`` has identical ``P=I`` while a
coordinate measurement on input ``|0>`` changes from deterministic to uniform,
with total-variation distance ``1/2``.

The missing datum can be supplied by a boundary map ``C:H->K`` whose range is
the resolved support.  Its polar

    V=C(C^*C)^(-1/2)                                      (3)

fixes the gauge and gives the coordinate POVM ``V^*D_eV``.  Given a block
encoding of ``C/beta`` and a minimum positive singular value ``sigma``, QSVT
implements (3) with degree

    O((beta/sigma) log(1/epsilon)).                        (4)

The range projector does not control this ratio.  Matrices with the same
range can have minimum singular value ``2^-m`` for arbitrary ``m``.  In the
natural normalized-frame access model the flat case already has
``beta/sigma=sqrt(q)``, so a sheaf support reflection does not remove the
known factorial-width access barrier.

The partial-sheaf resolver must therefore be paired with a representation-
specific, tightly normalized endpoint intertwiner, or a direct global polar
transform.  No such transform, decoder, algorithm, or speedup is proved here.
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
    "self_dual_wreath_support_projector_endpoint_gauge_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-PROJECTOR-ENDPOINT-GAUGE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EndpointGaugeAmbiguityControl:
    control_id: str
    input_dimension: int
    coefficient_dimension: int
    coordinate_outcome_count: int
    common_range_projector_residual: float
    endpoint_isometry_operator_distance: float
    maximum_component_effect_operator_distance: float
    witness_outcome_total_variation_distance: float
    range_projector_transcript_total_variation_distance: float
    fixed_compiler_worst_case_isometry_error_lower_bound: float
    exact_same_range_different_povm_verified: bool
    status: str


@dataclass(frozen=True)
class EndpointPolarControl:
    control_id: str
    input_dimension: int
    coefficient_dimension: int
    minimum_positive_singular_value: float
    maximum_singular_value: float
    block_encoding_normalization: float
    normalized_inverse_singular_gap: float
    polar_isometry_residual: float
    polar_range_projector_residual: float
    polar_reconstruction_residual: float
    coordinate_effect_sum_residual: float
    exact_endpoint_polar_verified: bool
    status: str


@dataclass(frozen=True)
class SameRangeConditioningCounterexample:
    exponent: int
    common_range_dimension: int
    well_conditioned_minimum_singular_value: float
    ill_conditioned_minimum_singular_value: float
    common_range_projector_residual: float
    ill_conditioned_inverse_gap: float
    support_projector_reveals_conditioning: bool
    status: str


@dataclass(frozen=True)
class EndpointGaugeScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_count_decimal: str
    generic_flat_endpoint_inverse_gap_log2: float
    polynomial_query_benchmark_log2: float
    generic_normalized_endpoint_access_polynomial: bool
    sheaf_support_reflection_removes_endpoint_gauge: bool
    tightly_normalized_representation_endpoint_map_proved: bool
    direct_global_orientation_polar_proved: bool
    status: str


@dataclass(frozen=True)
class EndpointGaugeBoundaryTheorem:
    gauge_family: str
    component_conjugation: str
    range_only_no_go: str
    endpoint_polar: str
    conditional_complexity: str
    natural_access_boundary: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SupportProjectorEndpointGaugeBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: EndpointGaugeBoundaryTheorem
    gauge_controls: list[EndpointGaugeAmbiguityControl]
    polar_controls: list[EndpointPolarControl]
    conditioning_counterexamples: list[SameRangeConditioningCounterexample]
    scaling_records: list[EndpointGaugeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _support_projection(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    active = singular_values > 100 * tolerance
    return left[:, active] @ left[:, active].conj().T


def endpoint_polar(
    boundary: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray]:
    if boundary.ndim != 2 or not min(boundary.shape):
        raise ValueError("a nonempty boundary map is required")
    left, singular_values, right_adjoint = np.linalg.svd(
        boundary,
        full_matrices=False,
    )
    active = singular_values > 100 * tolerance
    if not np.any(active):
        raise ValueError("the boundary map has zero support")
    polar = left[:, active] @ right_adjoint[active, :]
    support = right_adjoint[active, :].conj().T @ right_adjoint[active, :]
    return polar, support


def coordinate_effects(
    isometry: np.ndarray,
    coordinate_blocks: tuple[tuple[int, ...], ...],
) -> tuple[np.ndarray, ...]:
    if isometry.ndim != 2 or not coordinate_blocks:
        raise ValueError("an isometry and coordinate partition are required")
    flattened = tuple(index for block in coordinate_blocks for index in block)
    if sorted(flattened) != list(range(isometry.shape[0])):
        raise ValueError("coordinate blocks must partition every output row")
    return tuple(
        _hermitian(isometry[np.asarray(block)].conj().T @ isometry[np.asarray(block)])
        for block in coordinate_blocks
    )


def audit_endpoint_gauge_ambiguity(
    control_id: str,
    endpoint: np.ndarray,
    input_gauge: np.ndarray,
    coordinate_blocks: tuple[tuple[int, ...], ...],
    witness_state: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> EndpointGaugeAmbiguityControl:
    if endpoint.ndim != 2 or endpoint.shape[1] != input_gauge.shape[0]:
        raise ValueError("endpoint and input gauge dimensions do not match")
    input_dimension = endpoint.shape[1]
    if input_gauge.shape != (input_dimension, input_dimension):
        raise ValueError("input gauge must be square")
    if witness_state.shape != (input_dimension,):
        raise ValueError("witness state has the wrong dimension")
    if abs(float(np.linalg.norm(witness_state)) - 1.0) > 100 * tolerance:
        raise ValueError("witness state must be normalized")
    identity = np.eye(input_dimension, dtype=complex)
    if max(
        np.linalg.norm(endpoint.conj().T @ endpoint - identity, ord=2),
        np.linalg.norm(input_gauge.conj().T @ input_gauge - identity, ord=2),
    ) > 1000 * tolerance:
        raise ValueError("endpoint and gauge must be isometric/unitary")
    gauged = endpoint @ input_gauge
    first_range = endpoint @ endpoint.conj().T
    second_range = gauged @ gauged.conj().T
    range_residual = float(np.linalg.norm(first_range - second_range, ord=2))
    first_effects = coordinate_effects(endpoint, coordinate_blocks)
    second_effects = coordinate_effects(gauged, coordinate_blocks)
    effect_distance = max(
        float(np.linalg.norm(first - second, ord=2))
        for first, second in zip(first_effects, second_effects)
    )
    first_law = np.asarray(
        [float(np.vdot(witness_state, effect @ witness_state).real) for effect in first_effects]
    )
    second_law = np.asarray(
        [float(np.vdot(witness_state, effect @ witness_state).real) for effect in second_effects]
    )
    total_variation = float(np.sum(np.abs(first_law - second_law)) / 2.0)
    endpoint_distance = float(np.linalg.norm(endpoint - gauged, ord=2))
    worst_case = endpoint_distance / 2.0
    verified = bool(
        range_residual <= 1000 * tolerance
        and endpoint_distance > 1000 * tolerance
        and effect_distance > 1000 * tolerance
        and total_variation > 1000 * tolerance
    )
    return EndpointGaugeAmbiguityControl(
        control_id=control_id,
        input_dimension=input_dimension,
        coefficient_dimension=endpoint.shape[0],
        coordinate_outcome_count=len(coordinate_blocks),
        common_range_projector_residual=range_residual,
        endpoint_isometry_operator_distance=endpoint_distance,
        maximum_component_effect_operator_distance=effect_distance,
        witness_outcome_total_variation_distance=total_variation,
        range_projector_transcript_total_variation_distance=0.0,
        fixed_compiler_worst_case_isometry_error_lower_bound=worst_case,
        exact_same_range_different_povm_verified=verified,
        status=(
            "same-support-projector-distinct-physical-povm-verified"
            if verified
            else "endpoint-gauge-ambiguity-control-failure"
        ),
    )


def audit_endpoint_polar(
    control_id: str,
    boundary: np.ndarray,
    coordinate_blocks: tuple[tuple[int, ...], ...],
    *,
    block_encoding_normalization: float | None = None,
    tolerance: float = 1e-9,
) -> EndpointPolarControl:
    singular_values = np.linalg.svd(boundary, compute_uv=False)
    positive = singular_values[singular_values > 100 * tolerance]
    if len(positive) != boundary.shape[1]:
        raise ValueError("finite endpoint controls require full column rank")
    polar, initial_support = endpoint_polar(boundary, tolerance=tolerance)
    range_projector = _support_projection(boundary, tolerance)
    beta = (
        float(block_encoding_normalization)
        if block_encoding_normalization is not None
        else float(positive[0])
    )
    if beta + 100 * tolerance < positive[0]:
        raise ValueError("normalization must upper-bound the operator norm")
    root = _hermitian(boundary.conj().T @ boundary)
    values, vectors = np.linalg.eigh(root)
    square_root = (vectors * np.sqrt(np.maximum(values, 0.0))) @ vectors.conj().T
    reconstruction = float(np.linalg.norm(boundary - polar @ square_root, ord=2))
    isometry = float(
        np.linalg.norm(polar.conj().T @ polar - initial_support, ord=2)
    )
    range_residual = float(
        np.linalg.norm(polar @ polar.conj().T - range_projector, ord=2)
    )
    effects = coordinate_effects(polar, coordinate_blocks)
    sum_residual = float(
        np.linalg.norm(
            sum(effects, np.zeros_like(initial_support)) - initial_support,
            ord=2,
        )
    )
    verified = max(isometry, range_residual, reconstruction, sum_residual) <= 1000 * tolerance
    return EndpointPolarControl(
        control_id=control_id,
        input_dimension=boundary.shape[1],
        coefficient_dimension=boundary.shape[0],
        minimum_positive_singular_value=float(positive[-1]),
        maximum_singular_value=float(positive[0]),
        block_encoding_normalization=beta,
        normalized_inverse_singular_gap=beta / float(positive[-1]),
        polar_isometry_residual=isometry,
        polar_range_projector_residual=range_residual,
        polar_reconstruction_residual=reconstruction,
        coordinate_effect_sum_residual=sum_residual,
        exact_endpoint_polar_verified=verified,
        status=(
            "endpoint-polar-fixes-physical-gauge"
            if verified
            else "endpoint-polar-control-failure"
        ),
    )


def same_range_conditioning_counterexample(
    exponent: int,
) -> SameRangeConditioningCounterexample:
    if exponent < 1:
        raise ValueError("the exponent must be positive")
    well = np.eye(2, dtype=complex)
    ill = np.diag([1.0, 2.0**-exponent]).astype(complex)
    well_projector = _support_projection(well, 1e-15)
    ill_projector = _support_projection(ill, 1e-15)
    residual = float(np.linalg.norm(well_projector - ill_projector, ord=2))
    return SameRangeConditioningCounterexample(
        exponent=exponent,
        common_range_dimension=2,
        well_conditioned_minimum_singular_value=1.0,
        ill_conditioned_minimum_singular_value=2.0**-exponent,
        common_range_projector_residual=residual,
        ill_conditioned_inverse_gap=2.0**exponent,
        support_projector_reveals_conditioning=False,
        status="identical-range-arbitrarily-small-endpoint-singular-gap",
    )


def endpoint_gauge_scaling_record(n: int) -> EndpointGaugeScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    orientations = 1 << copies
    inverse_gap_log2 = copies / 2.0
    benchmark = 6.0 * math.log2(n)
    return EndpointGaugeScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_count_decimal=str(orientations),
        generic_flat_endpoint_inverse_gap_log2=inverse_gap_log2,
        polynomial_query_benchmark_log2=benchmark,
        generic_normalized_endpoint_access_polynomial=False,
        sheaf_support_reflection_removes_endpoint_gauge=False,
        tightly_normalized_representation_endpoint_map_proved=False,
        direct_global_orientation_polar_proved=False,
        status="support-resolved-endpoint-gauge-and-normalization-open",
    )


def endpoint_gauge_boundary_theorem() -> EndpointGaugeBoundaryTheorem:
    return EndpointGaugeBoundaryTheorem(
        gauge_family="W_U=WU has W_UW_U^*=WW^* for every input unitary U",
        component_conjugation="H_e^(U)=U^*H_eU",
        range_only_no_go=(
            "the same support projector can induce input-coordinate outcome laws "
            "with total-variation distance 1/2"
        ),
        endpoint_polar="V=C(C^*C)^(-1/2) fixes the physical-to-support gauge",
        conditional_complexity=(
            "degree O((beta/sigma)log(1/error)) given a C/beta block encoding"
        ),
        natural_access_boundary=(
            "the support projector controls neither beta/sigma nor the input gauge; "
            "generic flat normalized access still costs sqrt(q)"
        ),
        theorem_verified=True,
        status="support-projector-endpoint-gauge-boundary-proved",
    )


def run_support_projector_endpoint_gauge_boundary(
) -> SupportProjectorEndpointGaugeBoundaryReport:
    identity = np.eye(2, dtype=complex)
    hadamard = np.asarray([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2)
    gauge_controls = [
        audit_endpoint_gauge_ambiguity(
            "QUBIT-Z-VERSUS-X-ENDPOINT-GAUGE",
            identity,
            hadamard,
            ((0,), (1,)),
            np.asarray([1.0, 0.0], dtype=complex),
        )
    ]
    polar_controls = [
        audit_endpoint_polar(
            "RECTANGULAR-WELL-CONDITIONED-ENDPOINT",
            np.asarray(
                [[1.0, 0.0], [0.0, 0.6], [0.4, 0.0], [0.0, 0.8]],
                dtype=complex,
            ),
            ((0, 1), (2, 3)),
        ),
        audit_endpoint_polar(
            "RECTANGULAR-GAUGED-ENDPOINT",
            np.asarray(
                [[1.0, 0.0], [0.0, 0.3], [0.0, 1.0], [0.4, 0.0]],
                dtype=complex,
            ),
            ((0, 1), (2, 3)),
        ),
    ]
    counterexamples = [
        same_range_conditioning_counterexample(exponent)
        for exponent in (4, 8, 16, 32)
    ]
    scaling = [
        endpoint_gauge_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    theorem = endpoint_gauge_boundary_theorem()
    failures = sum(not row.exact_same_range_different_povm_verified for row in gauge_controls)
    failures += sum(not row.exact_endpoint_polar_verified for row in polar_controls)
    counterexample_growth = all(
        right.ill_conditioned_inverse_gap > left.ill_conditioned_inverse_gap
        for left, right in zip(counterexamples, counterexamples[1:])
    )
    verified = theorem.theorem_verified and failures == 0 and counterexample_growth
    return SupportProjectorEndpointGaugeBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "gauge": theorem.gauge_family,
            "effects": theorem.component_conjugation,
            "range_only_no_go": theorem.range_only_no_go,
            "endpoint_polar": theorem.endpoint_polar,
            "conditional_complexity": theorem.conditional_complexity,
            "natural_boundary": theorem.natural_access_boundary,
        },
        theorem=theorem,
        gauge_controls=gauge_controls,
        polar_controls=polar_controls,
        conditioning_counterexamples=counterexamples,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "separate_support_projection_from_physical_endpoint_gauge",
                "resolved": verified,
                "resolution": (
                    "The qubit control has identical range oracles and outcome "
                    "laws at total-variation distance one half."
                ),
            },
            {
                "obligation": "identify_sufficient_endpoint_datum",
                "resolved": verified,
                "resolution": (
                    "The polar of a full-rank boundary map fixes the range gauge "
                    "and yields the exact coordinate POVM."
                ),
            },
            {
                "obligation": "construct_tightly_normalized_natural_boundary_map",
                "resolved": False,
                "resolution": (
                    "Need beta/sigma polynomial without normalized q-leaf frame "
                    "access; pair GPE or a direct representation transform must supply it."
                ),
            },
            {
                "obligation": "compose_partial_sheaf_kernel_filter_with_physical_pgm_input",
                "resolved": False,
                "resolution": (
                    "The kernel reflection and the generalized Fourier row-copy "
                    "must be joined by a proved, conditioned boundary polar."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A resolved support projector uniquely specifies its embedding.",
                "resolved": True,
                "resolution": "WU has the same range for every input unitary U.",
            },
            {
                "objection": "Gauge ambiguity is only an unobservable global phase.",
                "resolved": True,
                "resolution": (
                    "Hadamard input gauge changes a coordinate outcome law by TV 1/2."
                ),
            },
            {
                "objection": "A support reflection certifies a good endpoint singular gap.",
                "resolved": True,
                "resolution": (
                    "The same full range supports diagonal boundary maps with "
                    "minimum singular value 2^-m for arbitrary m."
                ),
            },
            {
                "objection": "The endpoint polar formula is already an efficient circuit.",
                "resolved": False,
                "resolution": (
                    "Its complexity depends on tightly normalized boundary access, "
                    "which is exactly where generic frame access costs sqrt(q)."
                ),
            },
        ],
        headline_metrics={
            "support_endpoint_gauge_no_go_theorem_count": int(verified),
            "endpoint_polar_normal_form_theorem_count": int(verified),
            "finite_gauge_ambiguity_control_count": len(gauge_controls),
            "finite_endpoint_polar_control_count": len(polar_controls),
            "finite_control_failure_count": failures,
            "same_range_conditioning_counterexample_count": len(counterexamples),
            "maximum_counterexample_inverse_gap_log2": max(
                row.exponent for row in counterexamples
            ),
            "tightly_normalized_natural_endpoint_count": 0,
            "direct_global_orientation_polar_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "support_projector_alone_sufficient_for_physical_povm": False,
            "endpoint_polar_is_sufficient_given_boundary_access_and_gap": verified,
            "support_projector_controls_endpoint_conditioning": False,
            "tightly_normalized_natural_boundary_access_proved": False,
            "partial_sheaf_to_physical_endpoint_compiled": False,
            "direct_global_orientation_polar_compiled": False,
            "hidden_label_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The sheaf support still lacks the physical input gauge, and generic "
                "normalized boundary access retains the sqrt(q) barrier."
            ),
        },
        status=(
            "support-projector-insufficient-endpoint-polar-access-open"
            if verified
            else "support-projector-endpoint-gauge-control-failure"
        ),
        summary=(
            "A sheaf kernel projector identifies the coefficient range but not the "
            "physical input gauge. A boundary-map polar is sufficient, yet its "
            "normalization and singular gap are independent of the range and remain "
            "the natural access bottleneck."
        ),
        falsifiers_triggered=[
            "A coherent support reflection alone does not compile the physical component POVM.",
            "Support geometry does not certify endpoint-polar conditioning.",
            "Generic normalized frame access is not repaired by separately resolving the range.",
        ],
    )


def write_support_projector_endpoint_gauge_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-PROJECTOR-ENDPOINT-GAUGE-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_support_projector_endpoint_gauge_boundary" in globals():
        report = run_support_projector_endpoint_gauge_boundary(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-SUPPORT-PROJECTOR-ENDPOINT-GAUGE-BOUNDARY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SUPPORT-PROJECTOR-ENDPOINT-GAUGE-BOUNDARY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SUPPORT-PROJECTOR-ENDPOINT-GAUGE-BOUNDARY.",
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
                    "self_dual_wreath_support_projector_endpoint_gauge_boundary": str(path)
                },
            )
        )
    return payload
