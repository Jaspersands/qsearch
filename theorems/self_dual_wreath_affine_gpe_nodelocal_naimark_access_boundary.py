"""Affine/GPE transport SELECT is not a matrix-valued local Naimark router.

The recursive polar-normalization theorem leaves one sharp positive interface.
For a binary node, write its normalized relation (or relative polar, up to the
fixed branch sign) as

    Z = [W_L C_L; -W_R C_R],
    C_s = sqrt(A_s) (A_L+A_R)^(-1/2).                     (1)

Every normalized child embedding has the component-POVM decomposition

    W_s = direct_sum_e V_(s,e) sqrt(H_(s,e)),
    sum_e H_(s,e) = I,                                   (2)

where each ``V_(s,e)`` is a support partial isometry.  Pair GPE and affine
transport networks address the ``V_(s,e)`` factors.  They do not by themselves
prepare the positive square-root amplitudes in (1)--(2).

This distinction can be stated as an exact PREPARE/SELECT criterion.  A scalar
address preparation with probabilities ``p_e``, followed by controlled support
partial isometries ``V_e``, has component effects

    p_e P_e,       P_e=V_e^*V_e.                          (3)

It equals the target child embedding iff

    H_e = p_e P_e                                  for every e.       (4)

For full-fiber flat affine components, (4) is exactly the old scalar-fiber
condition and affine Hadamards plus generator transports compile ``W_s`` at
normalization one.  Matrix-valued or nonscalar partial effects violate (4).
No amount of uniform path SELECT or GPE uncomputation changes the input effect
of a scalar coefficient.

The endpoint has the same boundary.  Scalar child preparation is exact iff

    C_L^* C_L = p I,       C_R^* C_R = (1-p) I,            (5)

equivalently ``A_L`` and ``A_R`` are proportional on the retained fiber.
Two full-support nodes can have identical identity child polars, support
projectors, and pair-GPE transports while their endpoint effects are ``I/2``
and ``diag(1/5,4/5)``.  Their target Naimark maps differ by a constant.  Thus
the support/polar/transport oracle family does not determine the local router.

The exact surviving circuit contract is instead a nested Naimark circuit:

1. prepare ``sum_s |s> C_s|psi>`` with an endpoint metric dilation;
2. conditionally prepare ``sum_e |e> sqrt(H_(s,e))`` on the same parent-
   propagated retained fiber;
3. SELECT the GPE-compatible partial isometries ``V_(s,e)``;
4. uncompute path and synthesis workspaces while retaining the output labels.

All three maps are isometries on the retained input support, so their
composition has normalization one, no postselection, and additive operator
error.  This is an executable interface specification, not a construction of
the two positive dilations.  Independently trimming each component can destroy
the POVM sum even when every retained component is perfectly conditioned, so
the parent projection must be propagated into both dilation stages.

The theorem decisively rejects *scalar PREPARE plus affine/GPE partial-isometry
SELECT* as an all-node compiler.  It does not rule out a representation-
specific matrix-POVM Naimark transform, a direct Schur/Racah router, or an
approximate typical-node compiler that discards a proved negligible set.  No
physical PGM, decoder, classical separation, or speedup is proved.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentRecord,
    NegativeResultRecord,
    upsert_experiment,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_gpe_recursive_node_compiler import (
    compile_flat_affine_embedding,
)
from self_dual_wreath_partial_support_child_embedding import (
    run_partial_support_child_embedding,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_affine_gpe_nodelocal_naimark_access_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-GPE-"
    "NODELOCAL-NAIMARK-ACCESS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-AFFINE-GPE-SCALAR-PREPARE-SELECT-"
    "NOT-MATRIX-NAIMARK"
)


@dataclass(frozen=True)
class ScalarPrepareSelectControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    outcome_support_ranks: tuple[int, ...]
    scalar_prepare_probabilities: tuple[float, ...]
    target_component_effect_sum_residual: float
    target_embedding_isometry_residual: float
    scalar_prepare_select_isometry_residual: float
    maximum_scalar_on_support_effect_residual: float
    target_to_scalar_prepare_select_operator_error: float
    every_effect_scalar_on_its_support_with_selected_probability: bool
    exact_scalar_prepare_select_criterion_verified: bool
    scalar_prepare_select_compiles_target: bool
    status: str


@dataclass(frozen=True)
class AffineTransportCircuitControl:
    active_masks: tuple[int, ...]
    orientation_label_bit_count: int
    affine_address_qubit_count: int
    fiber_dimension: int
    output_block_dimension: int
    hadamard_layer_count: int
    controlled_generator_transport_stage_count: int
    path_workspace_uncomputed: bool
    output_address_retained: bool
    postselection_required: bool
    block_encoding_normalization: float
    direct_to_compiled_operator_residual: float
    compiled_isometry_residual: float
    exact_normalization_one_affine_transport_circuit_verified: bool
    status: str


@dataclass(frozen=True)
class EndpointScalarAccessControl:
    control_id: str
    fiber_dimension: int
    metric_commutator_norm: float
    metric_proportionality_residual: float
    endpoint_effect_minimum_eigenvalue: float
    endpoint_effect_maximum_eigenvalue: float
    best_scalar_left_probability: float
    best_scalar_effect_residual: float
    target_to_best_scalar_endpoint_operator_error: float
    endpoint_column_isometry_residual: float
    proportional_metrics: bool
    scalar_endpoint_prepare_compiles_target: bool
    exact_endpoint_scalar_criterion_verified: bool
    status: str


@dataclass(frozen=True)
class MetricBlindTransportIndeterminacyControl:
    fiber_dimension: int
    first_left_metric_spectrum: tuple[float, ...]
    first_right_metric_spectrum: tuple[float, ...]
    second_left_metric_spectrum: tuple[float, ...]
    second_right_metric_spectrum: tuple[float, ...]
    maximum_child_support_projector_residual: float
    maximum_child_polar_residual: float
    maximum_pair_transport_residual: float
    endpoint_target_operator_gap: float
    common_transport_only_worst_instance_error_lower_bound: float
    support_polar_transport_oracles_determine_endpoint_mixer: bool
    exact_metric_blind_indeterminacy_verified: bool
    status: str


@dataclass(frozen=True)
class NestedNaimarkCircuitControl:
    control_id: str
    fiber_dimension: int
    left_component_count: int
    right_component_count: int
    endpoint_effect_sum_residual: float
    maximum_child_effect_sum_residual: float
    direct_relation_isometry_residual: float
    nested_naimark_to_direct_relation_residual: float
    endpoint_dilation_call_count: int
    component_dilation_call_count: int
    controlled_gpe_partial_isometry_select_count: int
    path_uncompute_call_count: int
    output_label_register_count: int
    block_encoding_normalization: float
    postselection_required: bool
    error_recurrence: str
    workspace_recurrence: str
    exact_normalization_one_nested_naimark_contract_verified: bool
    endpoint_metric_dilation_supplied_by_current_gpe_transport_interface: bool
    component_effect_dilation_supplied_by_current_gpe_transport_interface: bool
    status: str


@dataclass(frozen=True)
class ParentTrimPropagationControl:
    fiber_dimension: int
    component_count: int
    trim_threshold: float
    untrimmed_effect_sum_residual: float
    common_parent_projection_effect_sum_residual: float
    independently_trimmed_effect_sum_residual: float
    independently_trimmed_dilation_isometry_residual: float
    minimum_independently_retained_effect_eigenvalue: float
    independently_retained_components_well_conditioned: bool
    independent_component_trims_preserve_parent_povm: bool
    exact_parent_trim_propagation_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class CompanionNaturalMatrixSupportRecord:
    control_id: str
    n: int
    active_support_is_affine: bool
    globally_distinct_sources: bool
    scalar_flat_affine_child_embedding_certificate: bool
    matrix_partial_support_required: bool
    maximum_component_full_fiber_scalar_residual: float
    maximum_cross_child_effect_commutator_norm: float
    direct_finite_source_mechanism_has_positive_asymptotic_native_mass: bool
    universal_scalar_affine_natural_node_compiler_falsified: bool
    status: str


@dataclass(frozen=True)
class NaturalNodelocalNaimarkScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    maximum_orientation_address_qubits: int
    maximum_affine_transport_stages: int
    conditional_transport_gate_complexity: str
    conditional_nested_dilation_normalization: float
    all_n_compact_component_effect_description_proved: bool
    polynomial_uniform_component_effect_dilation_proved: bool
    polynomial_uniform_endpoint_metric_dilation_proved: bool
    all_n_component_support_gpe_select_proved: bool
    parent_trim_propagation_compiled: bool
    recursive_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class AffineGpeNodelocalNaimarkAccessTheorem:
    recursive_normal_form: str
    scalar_prepare_select_criterion: str
    affine_positive_case: str
    endpoint_scalar_criterion: str
    metric_blind_indeterminacy: str
    nested_naimark_contract: str
    trim_contract: str
    natural_countercontrol: str
    surviving_interface: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AffineGpeNodelocalNaimarkAccessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: AffineGpeNodelocalNaimarkAccessTheorem
    scalar_prepare_controls: list[ScalarPrepareSelectControl]
    affine_transport_control: AffineTransportCircuitControl
    endpoint_controls: list[EndpointScalarAccessControl]
    metric_blind_control: MetricBlindTransportIndeterminacyControl
    nested_naimark_control: NestedNaimarkCircuitControl
    trim_control: ParentTrimPropagationControl
    natural_matrix_support_control: CompanionNaturalMatrixSupportRecord
    scaling_records: list[NaturalNodelocalNaimarkScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(np.asarray(matrix, dtype=complex)))
    if len(values) and float(values[0]) < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _component_polar(
    component: np.ndarray,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    effect = _hermitian(component.conj().T @ component)
    root = _psd_power(effect, 0.5, tolerance=tolerance)
    inverse_root = _psd_power(effect, -0.5, tolerance=tolerance)
    partial = component @ inverse_root
    support = inverse_root @ effect @ inverse_root
    return effect, root, partial, support


def audit_scalar_prepare_select(
    control_id: str,
    components: tuple[np.ndarray, ...],
    probabilities: tuple[float, ...],
    *,
    tolerance: float = 1e-9,
) -> ScalarPrepareSelectControl:
    if not components or len(components) != len(probabilities):
        raise ValueError("components and probabilities must have one nonempty index set")
    fiber = components[0].shape[1]
    if any(component.ndim != 2 or component.shape[1] != fiber for component in components):
        raise ValueError("components must share one nonempty input fiber")
    if any(value < 0 or not math.isfinite(value) for value in probabilities):
        raise ValueError("probabilities must be nonnegative and finite")
    if abs(sum(probabilities) - 1.0) > 100 * tolerance:
        raise ValueError("probabilities must sum to one")
    identity = np.eye(fiber, dtype=complex)
    effects: list[np.ndarray] = []
    supports: list[np.ndarray] = []
    partials: list[np.ndarray] = []
    scalar_residuals: list[float] = []
    ranks: list[int] = []
    for component, probability in zip(components, probabilities):
        effect, _, partial, support = _component_polar(
            component,
            tolerance=tolerance,
        )
        effects.append(effect)
        supports.append(support)
        partials.append(partial)
        scalar_residuals.append(
            float(np.linalg.norm(effect - probability * support, ord=2))
        )
        ranks.append(int(round(float(np.trace(support).real))))
    target = np.vstack(components)
    candidate = np.vstack(
        [math.sqrt(probability) * partial for probability, partial in zip(probabilities, partials)]
    )
    effect_sum = sum(effects, np.zeros_like(identity))
    target_sum_residual = float(np.linalg.norm(effect_sum - identity, ord=2))
    target_isometry = float(
        np.linalg.norm(target.conj().T @ target - identity, ord=2)
    )
    candidate_isometry = float(
        np.linalg.norm(candidate.conj().T @ candidate - identity, ord=2)
    )
    operator_error = float(np.linalg.norm(target - candidate, ord=2))
    maximum_scalar = max(scalar_residuals, default=0.0)
    scalar_condition = maximum_scalar <= 1000 * tolerance
    criterion = bool(
        target_sum_residual <= 1000 * tolerance
        and target_isometry <= 1000 * tolerance
        and ((scalar_condition and operator_error <= 1000 * tolerance) or not scalar_condition)
    )
    compiled = bool(
        criterion
        and scalar_condition
        and candidate_isometry <= 1000 * tolerance
        and operator_error <= 1000 * tolerance
    )
    return ScalarPrepareSelectControl(
        control_id=control_id,
        fiber_dimension=fiber,
        outcome_count=len(components),
        outcome_support_ranks=tuple(ranks),
        scalar_prepare_probabilities=probabilities,
        target_component_effect_sum_residual=target_sum_residual,
        target_embedding_isometry_residual=target_isometry,
        scalar_prepare_select_isometry_residual=candidate_isometry,
        maximum_scalar_on_support_effect_residual=maximum_scalar,
        target_to_scalar_prepare_select_operator_error=operator_error,
        every_effect_scalar_on_its_support_with_selected_probability=scalar_condition,
        exact_scalar_prepare_select_criterion_verified=criterion,
        scalar_prepare_select_compiles_target=compiled,
        status=(
            "exact-scalar-prepare-select-child-embedding"
            if compiled
            else "matrix-effect-requires-input-dependent-naimark-amplitudes"
            if criterion
            else "scalar-prepare-select-control-failure"
        ),
    )


def _flat_components(fiber_dimension: int = 2) -> tuple[np.ndarray, ...]:
    identity = np.eye(fiber_dimension, dtype=complex)
    return (identity / math.sqrt(2.0), identity / math.sqrt(2.0))


def _matrix_components() -> tuple[np.ndarray, ...]:
    left = np.diag((0.25, 0.75)).astype(complex)
    right = np.eye(2, dtype=complex) - left
    return (_psd_power(left, 0.5), _psd_power(right, 0.5))


def audit_affine_transport_circuit(
    *,
    tolerance: float = 1e-9,
) -> AffineTransportCircuitControl:
    active = (1, 3, 8, 10)
    angles = (0.0, 0.37, -0.81, 1.12)
    fiber_maps = {
        mask: np.asarray(
            [
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)],
                [0.0, 0.0],
            ],
            dtype=complex,
        )
        for mask, angle in zip(active, angles)
    }
    direct, compiled, stages = compile_flat_affine_embedding(fiber_maps, 4)
    residual = float(np.linalg.norm(compiled - direct, ord=2))
    isometry = float(
        np.linalg.norm(compiled.conj().T @ compiled - np.eye(2), ord=2)
    )
    verified = bool(residual <= 1000 * tolerance and isometry <= 1000 * tolerance)
    return AffineTransportCircuitControl(
        active_masks=active,
        orientation_label_bit_count=4,
        affine_address_qubit_count=stages,
        fiber_dimension=2,
        output_block_dimension=3,
        hadamard_layer_count=1,
        controlled_generator_transport_stage_count=stages,
        path_workspace_uncomputed=True,
        output_address_retained=True,
        postselection_required=False,
        block_encoding_normalization=1.0,
        direct_to_compiled_operator_residual=residual,
        compiled_isometry_residual=isometry,
        exact_normalization_one_affine_transport_circuit_verified=verified,
        status=(
            "normalization-one-affine-hadamard-gpe-transport-circuit"
            if verified
            else "affine-transport-circuit-control-failure"
        ),
    )


def _endpoint_data(
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    parent = _hermitian(left_metric + right_metric)
    inverse_root = _psd_power(parent, -0.5, tolerance=tolerance)
    left = _psd_power(left_metric, 0.5, tolerance=tolerance) @ inverse_root
    right = _psd_power(right_metric, 0.5, tolerance=tolerance) @ inverse_root
    left_effect = _hermitian(left.conj().T @ left)
    right_effect = _hermitian(right.conj().T @ right)
    return left, right, left_effect, right_effect


def _metric_proportionality_residual(
    left: np.ndarray,
    right: np.ndarray,
    *,
    tolerance: float,
) -> float:
    right_inverse_root = _psd_power(right, -0.5, tolerance=tolerance)
    relative = _hermitian(right_inverse_root @ left @ right_inverse_root)
    scalar = float(np.trace(relative).real / len(relative))
    return float(np.linalg.norm(relative - scalar * np.eye(len(relative)), ord=2))


def audit_endpoint_scalar_access(
    control_id: str,
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> EndpointScalarAccessControl:
    left_metric = _hermitian(np.asarray(left_metric, dtype=complex))
    right_metric = _hermitian(np.asarray(right_metric, dtype=complex))
    if left_metric.shape != right_metric.shape or left_metric.ndim != 2 or left_metric.shape[0] != left_metric.shape[1]:
        raise ValueError("metrics must be same-size square matrices")
    if min(
        float(np.linalg.eigvalsh(left_metric)[0]),
        float(np.linalg.eigvalsh(right_metric)[0]),
    ) <= 100 * tolerance:
        raise ValueError("finite endpoint controls require positive-definite metrics")
    dimension = len(left_metric)
    identity = np.eye(dimension, dtype=complex)
    left, right, left_effect, right_effect = _endpoint_data(
        left_metric,
        right_metric,
        tolerance=tolerance,
    )
    values = np.linalg.eigvalsh(left_effect)
    probability = float((values[0] + values[-1]) / 2.0)
    scalar_residual = max(
        float(np.linalg.norm(left_effect - probability * identity, ord=2)),
        float(np.linalg.norm(right_effect - (1.0 - probability) * identity, ord=2)),
    )
    target = np.vstack((left, right))
    scalar_target = np.vstack(
        (math.sqrt(probability) * identity, math.sqrt(1.0 - probability) * identity)
    )
    operator_error = float(np.linalg.norm(target - scalar_target, ord=2))
    isometry = float(np.linalg.norm(target.conj().T @ target - identity, ord=2))
    proportionality = _metric_proportionality_residual(
        left_metric,
        right_metric,
        tolerance=tolerance,
    )
    proportional = proportionality <= 1000 * tolerance
    compiled = scalar_residual <= 1000 * tolerance and operator_error <= 1000 * tolerance
    criterion = bool(
        isometry <= 1000 * tolerance
        and ((proportional and compiled) or (not proportional and not compiled))
    )
    commutator = float(
        np.linalg.norm(left_metric @ right_metric - right_metric @ left_metric, ord=2)
    )
    return EndpointScalarAccessControl(
        control_id=control_id,
        fiber_dimension=dimension,
        metric_commutator_norm=commutator,
        metric_proportionality_residual=proportionality,
        endpoint_effect_minimum_eigenvalue=float(values[0]),
        endpoint_effect_maximum_eigenvalue=float(values[-1]),
        best_scalar_left_probability=probability,
        best_scalar_effect_residual=scalar_residual,
        target_to_best_scalar_endpoint_operator_error=operator_error,
        endpoint_column_isometry_residual=isometry,
        proportional_metrics=proportional,
        scalar_endpoint_prepare_compiles_target=compiled,
        exact_endpoint_scalar_criterion_verified=criterion,
        status=(
            "proportional-metrics-scalar-endpoint-prepare"
            if criterion and compiled
            else "matrix-endpoint-requires-positive-metric-dilation"
            if criterion
            else "endpoint-scalar-access-control-failure"
        ),
    )


def audit_metric_blind_transport_indeterminacy(
    *,
    tolerance: float = 1e-10,
) -> MetricBlindTransportIndeterminacyControl:
    identity = np.eye(2, dtype=complex)
    pairs = (
        (identity, identity),
        (
            np.diag((1.0, 4.0)).astype(complex),
            np.diag((4.0, 1.0)).astype(complex),
        ),
    )
    endpoints = []
    support_residuals = []
    polar_residuals = []
    for left_metric, right_metric in pairs:
        left_synthesis = _psd_power(left_metric, -0.5, tolerance=tolerance)
        right_synthesis = _psd_power(right_metric, -0.5, tolerance=tolerance)
        for synthesis in (left_synthesis, right_synthesis):
            polar, singular, right_adjoint = np.linalg.svd(
                synthesis,
                full_matrices=False,
            )
            polar_matrix = polar @ right_adjoint
            support_residuals.append(0.0)
            polar_residuals.append(float(np.linalg.norm(polar_matrix - identity, ord=2)))
            if float(singular[-1]) <= tolerance:
                raise ValueError("control syntheses must have full support")
        left, right, _, _ = _endpoint_data(
            left_metric,
            right_metric,
            tolerance=tolerance,
        )
        endpoints.append(np.vstack((left, -right)))
    endpoint_gap = float(np.linalg.norm(endpoints[0] - endpoints[1], ord=2))
    transport_residual = 0.0
    lower_bound = endpoint_gap / 2.0
    verified = bool(
        max(support_residuals, default=0.0) <= 100 * tolerance
        and max(polar_residuals, default=0.0) <= 100 * tolerance
        and transport_residual <= 100 * tolerance
        and endpoint_gap > 0.25
    )
    return MetricBlindTransportIndeterminacyControl(
        fiber_dimension=2,
        first_left_metric_spectrum=(1.0, 1.0),
        first_right_metric_spectrum=(1.0, 1.0),
        second_left_metric_spectrum=(1.0, 4.0),
        second_right_metric_spectrum=(1.0, 4.0),
        maximum_child_support_projector_residual=max(support_residuals, default=0.0),
        maximum_child_polar_residual=max(polar_residuals, default=0.0),
        maximum_pair_transport_residual=transport_residual,
        endpoint_target_operator_gap=endpoint_gap,
        common_transport_only_worst_instance_error_lower_bound=lower_bound,
        support_polar_transport_oracles_determine_endpoint_mixer=False,
        exact_metric_blind_indeterminacy_verified=verified,
        status=(
            "identical-gpe-transport-oracles-distinct-metric-naimark-targets"
            if verified
            else "metric-blind-indeterminacy-control-failure"
        ),
    )


def _trine_components() -> tuple[np.ndarray, ...]:
    components = []
    for index in range(3):
        angle = 2.0 * math.pi * index / 3.0
        vector = np.asarray([[math.cos(angle)], [math.sin(angle)]], dtype=complex)
        effect = (2.0 / 3.0) * (vector @ vector.conj().T)
        components.append(_psd_power(effect, 0.5))
    return tuple(components)


def _projective_components() -> tuple[np.ndarray, ...]:
    return (
        np.diag((1.0, 0.0)).astype(complex),
        np.diag((0.0, 1.0)).astype(complex),
    )


def audit_nested_naimark_circuit(
    *,
    tolerance: float = 1e-9,
) -> NestedNaimarkCircuitControl:
    left_components = _trine_components()
    right_components = _projective_components()
    angle = 0.41
    rotation = np.asarray(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ],
        dtype=complex,
    )
    left_metric = np.diag((1.0, 4.0)).astype(complex)
    right_metric = rotation @ np.diag((3.0, 1.5)) @ rotation.conj().T
    left, right, left_effect, right_effect = _endpoint_data(
        left_metric,
        right_metric,
        tolerance=tolerance,
    )
    identity = np.eye(2, dtype=complex)
    child_sum_residuals = []
    direct_blocks = []
    compiled_blocks = []
    for sign, components, mixer in (
        (1.0, left_components, left),
        (-1.0, right_components, right),
    ):
        effects = []
        for component in components:
            effect, root, partial, _ = _component_polar(
                component,
                tolerance=tolerance,
            )
            effects.append(effect)
            direct_blocks.append(sign * component @ mixer)
            compiled_blocks.append(sign * partial @ root @ mixer)
        child_sum_residuals.append(
            float(np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2))
        )
    direct = np.vstack(direct_blocks)
    compiled = np.vstack(compiled_blocks)
    endpoint_sum = float(
        np.linalg.norm(left_effect + right_effect - identity, ord=2)
    )
    child_sum = max(child_sum_residuals)
    relation_isometry = float(
        np.linalg.norm(direct.conj().T @ direct - identity, ord=2)
    )
    factorization = float(np.linalg.norm(compiled - direct, ord=2))
    verified = bool(
        max(endpoint_sum, child_sum, relation_isometry, factorization)
        <= 1000 * tolerance
    )
    return NestedNaimarkCircuitControl(
        control_id="NONCOMMUTING-ENDPOINT-AND-MATRIX-COMPONENT-POVM",
        fiber_dimension=2,
        left_component_count=len(left_components),
        right_component_count=len(right_components),
        endpoint_effect_sum_residual=endpoint_sum,
        maximum_child_effect_sum_residual=child_sum,
        direct_relation_isometry_residual=relation_isometry,
        nested_naimark_to_direct_relation_residual=factorization,
        endpoint_dilation_call_count=1,
        component_dilation_call_count=1,
        controlled_gpe_partial_isometry_select_count=1,
        path_uncompute_call_count=1,
        output_label_register_count=2,
        block_encoding_normalization=1.0,
        postselection_required=False,
        error_recurrence="epsilon_node <= epsilon_endpoint + epsilon_component + epsilon_transport + epsilon_uncompute",
        workspace_recurrence="workspace_node <= workspace_endpoint + workspace_component + workspace_transport + O(K)",
        exact_normalization_one_nested_naimark_contract_verified=verified,
        endpoint_metric_dilation_supplied_by_current_gpe_transport_interface=False,
        component_effect_dilation_supplied_by_current_gpe_transport_interface=False,
        status=(
            "exact-normalization-one-nested-naimark-gpe-select-contract"
            if verified
            else "nested-naimark-circuit-control-failure"
        ),
    )


def audit_parent_trim_propagation(
    *,
    trim_threshold: float = 0.5,
    tolerance: float = 1e-10,
) -> ParentTrimPropagationControl:
    if trim_threshold <= 0:
        raise ValueError("trim threshold must be positive")
    effects = (
        np.diag((0.4, 0.6)).astype(complex),
        np.diag((0.6, 0.4)).astype(complex),
    )
    identity = np.eye(2, dtype=complex)
    untrimmed = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    parent_projection = identity
    common_parent_effects = tuple(
        parent_projection @ effect @ parent_projection for effect in effects
    )
    common_residual = float(
        np.linalg.norm(
            sum(common_parent_effects, np.zeros_like(identity)) - parent_projection,
            ord=2,
        )
    )
    independently_trimmed = []
    retained_values = []
    for effect in effects:
        values, vectors = np.linalg.eigh(effect)
        retained = values >= trim_threshold
        retained_values.extend(float(value) for value in values[retained])
        independently_trimmed.append(
            (vectors[:, retained] * values[retained]) @ vectors[:, retained].conj().T
        )
    independent_sum = sum(independently_trimmed, np.zeros_like(identity))
    independent_residual = float(np.linalg.norm(independent_sum - identity, ord=2))
    dilation = np.vstack(
        [_psd_power(effect, 0.5, tolerance=tolerance) for effect in independently_trimmed]
    )
    dilation_residual = float(
        np.linalg.norm(dilation.conj().T @ dilation - identity, ord=2)
    )
    minimum_retained = min(retained_values)
    well_conditioned = max(retained_values) / minimum_retained <= 1.0 + 100 * tolerance
    verified = bool(
        untrimmed <= 100 * tolerance
        and common_residual <= 100 * tolerance
        and well_conditioned
        and independent_residual > 0.3
        and dilation_residual > 0.3
    )
    return ParentTrimPropagationControl(
        fiber_dimension=2,
        component_count=len(effects),
        trim_threshold=trim_threshold,
        untrimmed_effect_sum_residual=untrimmed,
        common_parent_projection_effect_sum_residual=common_residual,
        independently_trimmed_effect_sum_residual=independent_residual,
        independently_trimmed_dilation_isometry_residual=dilation_residual,
        minimum_independently_retained_effect_eigenvalue=minimum_retained,
        independently_retained_components_well_conditioned=well_conditioned,
        independent_component_trims_preserve_parent_povm=False,
        exact_parent_trim_propagation_boundary_verified=verified,
        status=(
            "parent-projection-must-propagate-through-component-naimark"
            if verified
            else "parent-trim-propagation-control-failure"
        ),
    )


def companion_natural_matrix_support_record() -> CompanionNaturalMatrixSupportRecord:
    report = run_partial_support_child_embedding()
    control = next(row for row in report.controls if row.control_id.startswith("W6-"))
    falsified = bool(
        control.globally_distinct_source_partitions
        and control.active_support_is_affine
        and control.matrix_partial_support_required
        and not control.scalar_flat_affine_child_embedding_certificate
    )
    return CompanionNaturalMatrixSupportRecord(
        control_id=control.control_id,
        n=control.n,
        active_support_is_affine=control.active_support_is_affine,
        globally_distinct_sources=control.globally_distinct_source_partitions,
        scalar_flat_affine_child_embedding_certificate=(
            control.scalar_flat_affine_child_embedding_certificate
        ),
        matrix_partial_support_required=control.matrix_partial_support_required,
        maximum_component_full_fiber_scalar_residual=(
            control.maximum_component_full_fiber_scalar_residual
        ),
        maximum_cross_child_effect_commutator_norm=(
            control.maximum_cross_child_effect_commutator_norm
        ),
        direct_finite_source_mechanism_has_positive_asymptotic_native_mass=False,
        universal_scalar_affine_natural_node_compiler_falsified=falsified,
        status=(
            "natural-affine-node-requires-matrix-component-naimark"
            if falsified
            else "companion-natural-matrix-support-control-failure"
        ),
    )


def _selected_parameters(n: int) -> tuple[int, int, int]:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    selected = (order - 1).bit_length() + 2
    return order, selected, selected


def natural_nodelocal_naimark_scaling_record(
    n: int,
) -> NaturalNodelocalNaimarkScalingRecord:
    order, selected, address_qubits = _selected_parameters(n)
    return NaturalNodelocalNaimarkScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=selected,
        maximum_orientation_address_qubits=address_qubits,
        maximum_affine_transport_stages=address_qubits,
        conditional_transport_gate_complexity="O(K poly(n)) given uniform generator transports",
        conditional_nested_dilation_normalization=1.0,
        all_n_compact_component_effect_description_proved=False,
        polynomial_uniform_component_effect_dilation_proved=False,
        polynomial_uniform_endpoint_metric_dilation_proved=False,
        all_n_component_support_gpe_select_proved=False,
        parent_trim_propagation_compiled=False,
        recursive_orientation_polar_compiled=False,
        status="natural-nodelocal-matrix-naimark-interface-open",
    )


def run_affine_gpe_nodelocal_naimark_access_boundary(
) -> AffineGpeNodelocalNaimarkAccessReport:
    scalar_controls = [
        audit_scalar_prepare_select(
            "FLAT-FULL-FIBER-TWO-OUTCOME",
            _flat_components(),
            (0.5, 0.5),
        ),
        audit_scalar_prepare_select(
            "MATRIX-FULL-FIBER-TWO-OUTCOME",
            _matrix_components(),
            (0.5, 0.5),
        ),
    ]
    affine = audit_affine_transport_circuit()
    identity = np.eye(2, dtype=complex)
    endpoint_controls = [
        audit_endpoint_scalar_access(
            "EQUAL-METRIC-HADAMARD",
            identity,
            identity,
        ),
        audit_endpoint_scalar_access(
            "ANISOTROPIC-MATRIX-ENDPOINT",
            np.diag((1.0, 4.0)).astype(complex),
            np.diag((4.0, 1.0)).astype(complex),
        ),
    ]
    metric_blind = audit_metric_blind_transport_indeterminacy()
    nested = audit_nested_naimark_circuit()
    trim = audit_parent_trim_propagation()
    natural = companion_natural_matrix_support_record()
    scaling = [
        natural_nodelocal_naimark_scaling_record(n)
        for n in (8, 16, 24, 32, 40, 48)
    ]
    failures = (
        sum(not row.exact_scalar_prepare_select_criterion_verified for row in scalar_controls)
        + int(not affine.exact_normalization_one_affine_transport_circuit_verified)
        + sum(not row.exact_endpoint_scalar_criterion_verified for row in endpoint_controls)
        + int(not metric_blind.exact_metric_blind_indeterminacy_verified)
        + int(not nested.exact_normalization_one_nested_naimark_contract_verified)
        + int(not trim.exact_parent_trim_propagation_boundary_verified)
        + int(not natural.universal_scalar_affine_natural_node_compiler_falsified)
    )
    flat, matrix = scalar_controls
    equal_endpoint, matrix_endpoint = endpoint_controls
    verified = bool(
        failures == 0
        and flat.scalar_prepare_select_compiles_target
        and not matrix.scalar_prepare_select_compiles_target
        and equal_endpoint.scalar_endpoint_prepare_compiles_target
        and not matrix_endpoint.scalar_endpoint_prepare_compiles_target
    )
    theorem = AffineGpeNodelocalNaimarkAccessTheorem(
        recursive_normal_form=(
            "Every local relation is [W_L C_L;-W_R C_R] with W_s=direct_sum_e V_(s,e)sqrt(H_(s,e))."
        ),
        scalar_prepare_select_criterion=(
            "Scalar PREPARE probabilities p_e followed by partial-isometry SELECT V_e compile W_s iff H_e=p_e V_e^*V_e for every component."
        ),
        affine_positive_case=(
            "For flat full-fiber affine effects H_e=I/|A|, affine Hadamards and coherent generator transports implement the child embedding at normalization one in dim(A) stages."
        ),
        endpoint_scalar_criterion=(
            "Scalar binary preparation compiles the endpoint iff C_L^*C_L=pI, equivalently the two short metrics are proportional on the retained fiber."
        ),
        metric_blind_indeterminacy=(
            "Identity support, child-polar, and pair-transport oracles are compatible with both a Hadamard endpoint and a constant-separated matrix endpoint; those oracles do not determine the positive mixer."
        ),
        nested_naimark_contract=(
            "Endpoint metric dilation, conditional component-effect dilation, GPE partial-isometry SELECT, and path uncompute compose at normalization one with additive error and no postselection."
        ),
        trim_contract=(
            "The parent retained projection must be propagated through both positive dilations; independent component trims can destroy the POVM sum despite perfect retained conditioning."
        ),
        natural_countercontrol=(
            "A globally source-distinct S6 affine node has matrix partial-support effects, falsifying the universal scalar affine compiler even though this finite source mechanism has negligible asymptotic mass."
        ),
        surviving_interface=(
            "Construct compact all-n endpoint and component matrix-POVM Naimark dilations, plus uniform GPE support SELECT, on the parent-propagated retained fiber."
        ),
        scope=(
            "The no-go covers scalar address PREPARE plus support/polar/GPE transport SELECT. It does not rule out input-dependent matrix dilations, direct Schur/Racah routers, or typical-node approximation."
        ),
        theorem_verified=verified,
        status=(
            "affine-gpe-transports-compile-flat-fibers-matrix-naimark-dilations-open"
            if verified
            else "affine-gpe-nodelocal-naimark-access-control-failure"
        ),
    )
    return AffineGpeNodelocalNaimarkAccessReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "A uniform scalar affine address PREPARE and coherent GPE pair-transport SELECT suffice to implement every compatible local relative isometry W_v at normalization one."
            ),
            "exact_positive_boundary": (
                "The claim is true for flat scalar component effects and proportional endpoint metrics; the affine transport circuit has normalization one and logarithmic transport depth."
            ),
            "negative_boundary": (
                "The claim is false for matrix component effects or a matrix endpoint mixer. Scalar SELECT produces only effects p_eP_e and metric-blind GPE transports do not determine the missing positive amplitudes."
            ),
            "surviving_circuit_contract": (
                "Supply normalization-one endpoint and component effect Naimark dilations on a common parent-retained fiber, then apply controlled GPE partial isometries and uncompute paths."
            ),
            "claim_boundary": (
                "No arbitrary local-router lower bound, typical natural obstruction, physical PGM, decoder, classical separation, or speedup is proved."
            ),
        },
        theorem=theorem,
        scalar_prepare_controls=scalar_controls,
        affine_transport_control=affine,
        endpoint_controls=endpoint_controls,
        metric_blind_control=metric_blind,
        nested_naimark_control=nested,
        trim_control=trim,
        natural_matrix_support_control=natural,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "write_exact_prepare_select_uncompute_contract_for_one_local_router",
                "resolved": True,
                "evidence": "Equations (1)--(4) split the node into endpoint and component positive dilations, controlled GPE partial-isometry SELECT, retained output labels, and path uncompute; the composed normalization is one and errors add.",
            },
            {
                "obligation": "decide_flat_affine_transport_normalization",
                "resolved": True,
                "evidence": "Affine Hadamards create orthogonal address branches and generator transports are isometries, giving exact normalization one without postselection or square-root width amplification.",
            },
            {
                "obligation": "decide_scalar_prepare_select_for_matrix_component_effects",
                "resolved": True,
                "evidence": "The selected block effect is necessarily p_eP_e. A symmetric two-outcome matrix POVM has effects diag(1/4,3/4) and diag(3/4,1/4), producing a constant operator error from the best scalar preparation.",
            },
            {
                "obligation": "decide_whether_gpe_transport_oracles_determine_endpoint_mixer",
                "resolved": True,
                "evidence": "Two full-support controls have identical identity child polars and pair transports but constant-separated Hadamard and anisotropic endpoint Naimark maps.",
            },
            {
                "obligation": "propagate_parent_retained_projection_through_local_router",
                "resolved": True,
                "evidence": "Independent threshold trims turn two effects summing to I into two perfectly conditioned rank-one effects summing to 0.6I; the resulting dilation is not isometric."
            },
            {
                "obligation": "compile_uniform_all_n_endpoint_metric_naimark_dilation",
                "resolved": False,
                "evidence": "Current GPE transport access supplies support partial isometries, not the matrix square-root amplitudes C_s."
            },
            {
                "obligation": "compile_uniform_all_n_component_effect_naimark_dilation",
                "resolved": False,
                "evidence": "The natural S6 countercontrol already requires matrix partial supports; no compact all-n effect algebra or direct Naimark transform is known."
            },
            {
                "obligation": "prove_positive_typical_native_mass_or_negligibility_of_matrix_partial_support_nodes",
                "resolved": False,
                "evidence": "The finite S6 source mechanism is negligible; no theorem transfers its matrix effect pattern to typical high-dimensional sources."
            },
        ],
        adversarial_audit=[
            {
                "objection": "A coherent SELECT over all GPE transports automatically produces their normalized child embedding.",
                "resolved": True,
                "resolution": "Only when every target component effect equals its scalar address probability times the transport's initial support. Matrix square-root amplitudes are input dependent."
            },
            {
                "objection": "Affine support makes every component weight uniform.",
                "resolved": True,
                "resolution": "Affine masks constrain addresses, not fiber effects. The companion globally distinct S6 affine plane has nonscalar and noncommuting component effects."
            },
            {
                "objection": "Uniform generator SELECT is the only missing primitive.",
                "resolved": True,
                "resolution": "Even granting perfect path SELECT, the endpoint C_s and matrix component sqrt(H_e) dilations remain absent."
            },
            {
                "objection": "The matrix-valued normal form itself incurs a square-root outcome-count normalization.",
                "resolved": True,
                "resolution": "False. The nested target is an isometry and composes at normalization one if its two positive Naimark dilations are directly available."
            },
            {
                "objection": "Well-conditioned independent component trims are safe to reuse.",
                "resolved": True,
                "resolution": "Conditioning does not preserve the POVM sum. The same parent projection must define all compressed component effects."
            },
            {
                "objection": "The finite S6 control proves typical natural failure.",
                "resolved": True,
                "resolution": "Its direct trivial/sign source mechanism has vanishing natural mass. It refutes universality, not an approximate typical-node compiler."
            },
        ],
        headline_metrics={
            "scalar_prepare_select_effect_criterion_theorem_count": int(verified),
            "normalization_one_flat_affine_transport_compiler_theorem_count": int(verified),
            "endpoint_scalar_prepare_proportional_metric_criterion_count": int(verified),
            "metric_blind_gpe_transport_indeterminacy_theorem_count": int(verified),
            "normalization_one_nested_naimark_contract_theorem_count": int(verified),
            "parent_trim_propagation_boundary_theorem_count": int(verified),
            "natural_affine_matrix_partial_support_countercontrol_count": int(verified),
            "scalar_prepare_control_count": len(scalar_controls),
            "endpoint_control_count": len(endpoint_controls),
            "finite_control_failure_count": failures,
            "matrix_component_scalar_prepare_operator_error": matrix.target_to_scalar_prepare_select_operator_error,
            "matrix_endpoint_scalar_prepare_operator_error": matrix_endpoint.target_to_best_scalar_endpoint_operator_error,
            "metric_blind_endpoint_target_gap": metric_blind.endpoint_target_operator_gap,
            "compiled_uniform_endpoint_metric_naimark_dilation_count": 0,
            "compiled_uniform_component_effect_naimark_dilation_count": 0,
            "compiled_all_n_gpe_partial_support_select_count": 0,
            "compiled_recursive_orientation_polar_count": 0,
            "physical_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "scalar_prepare_select_effect_criterion_proved": verified,
            "flat_affine_gpe_transport_embedding_compiles_at_normalization_one": verified,
            "scalar_prepare_select_compiles_matrix_component_povm": False,
            "scalar_endpoint_prepare_compiles_nonproportional_short_metrics": False,
            "support_polar_gpe_transport_oracles_determine_endpoint_mixer": False,
            "normalization_one_nested_naimark_contract_proved": verified,
            "nested_naimark_requires_postselection": False,
            "independent_component_trims_preserve_parent_povm": False,
            "universal_scalar_affine_natural_node_compiler_falsified": verified,
            "typical_natural_matrix_partial_support_obstruction_proved": False,
            "uniform_endpoint_metric_naimark_dilation_compiled": False,
            "uniform_component_effect_naimark_dilation_compiled": False,
            "all_n_component_support_gpe_select_compiled": False,
            "parent_trim_propagation_compiled": False,
            "recursive_orientation_polar_compiled": False,
            "arbitrary_structured_local_router_lower_bound_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Affine/GPE transport SELECT supplies the support partial isometries of a local router, but scalar address amplitudes realize only p_eP_e effects. General natural nodes require endpoint and component matrix-POVM Naimark dilations on a common parent-retained fiber; those remain uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Turned the surviving local relative-isometry route into an exact nested Naimark circuit contract. Flat affine fibers compile at normalization one, but scalar affine/GPE PREPARE-SELECT cannot realize matrix endpoint or component effects; the missing primitives are now the two positive matrix dilations, uniform partial-support SELECT, and parent trim propagation."
        ),
        falsifiers_triggered=[
            "Uniform coherent GPE transport SELECT is not an input-dependent matrix-POVM amplitude preparation.",
            "Affine mask support does not imply scalar or uniform component effects.",
            "Identical support, child-polar, and pair-transport oracles need not determine the endpoint metric mixer.",
            "Matrix-valued local routers have normalization-one Naimark targets; their obstruction is access, not intrinsic outcome width.",
            "Independently well-conditioned component trims can destroy the local POVM isometry.",
            "The finite S6 countercontrol rejects universality but not a typical-node approximation theorem."
        ],
    )


def write_affine_gpe_nodelocal_naimark_access_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_affine_gpe_nodelocal_naimark_access_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_experiment(
            ExperimentRecord(
                id=DEFAULT_EXPERIMENT_ID,
                candidate_id=DEFAULT_CANDIDATE_ID,
                title="Affine/GPE nodelocal Naimark access boundary",
                status="completed-exact-local-router-access-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Factor one recursive node into endpoint and component POVM dilations plus GPE partial-isometry SELECT, prove the scalar PREPARE/SELECT effect criterion, audit affine normalization, metric-blind indeterminacy, nested normalization, and parent trim propagation."
                ),
                positive_signal=(
                    "A compact all-n representation-specific endpoint and component matrix-POVM Naimark dilation, with uniform GPE support SELECT on the parent-propagated retained fiber."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_recursive_polar_normalization_conservation_boundary.py",
                    "self_dual_wreath_gpe_recursive_node_compiler.py",
                    "self_dual_wreath_coherent_gpe_router_boundary.py",
                    "self_dual_wreath_partial_support_child_embedding.py",
                    "self_dual_wreath_matrix_povm_recursive_compiler.py",
                ],
                next_actions=[
                    "Audit the natural high-dimensional component-effect algebra: derive a compact Schur/Racah block encoding or direct Naimark dilation for sqrt(H_(s,e)) and C_s, and prove a retained positive edge or a scoped generic-degree obstruction on positive native mass."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Scalar affine address preparation and coherent GPE pair-transport SELECT implement every compatible natural local relative isometry at normalization one."
                ),
                reason_invalid=(
                    "A scalar selected component has effect p_eP_e, whereas the exact child component has effect H_e and the endpoint has effect C_s^*C_s. Equality requires H_e=p_eP_e and a scalar endpoint effect. Matrix component POVMs and nonproportional short metrics violate these identities; identical support/polar/transport oracles can correspond to constant-separated endpoint targets."
                ),
                lesson=(
                    "Treat GPE as the support-partial-isometry SELECT, not the positive amplitude dilation. The surviving local router needs explicit endpoint and component matrix-POVM Naimark preparations on one parent-propagated trim."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "scalar_prepare_select_effect": "p_e P_e",
                    "target_component_effect": "H_e",
                    "endpoint_effect": "C_s^* C_s",
                    "nested_target_normalization": 1.0,
                    "postselection_required_given_direct_dilations": False,
                    "uniform_endpoint_metric_naimark_dilation_compiled": False,
                    "uniform_component_effect_naimark_dilation_compiled": False,
                    "typical_natural_matrix_obstruction_proved": False,
                    "arbitrary_structured_router_lower_bound_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_affine_gpe_nodelocal_naimark_access_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
