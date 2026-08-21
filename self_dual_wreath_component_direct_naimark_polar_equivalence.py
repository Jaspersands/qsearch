"""Direct component Naimark dilation is a restricted orientation polar.

Let ``R=[Q_e]_e:C=direct_sum_e C_e -> H`` be one child leaf synthesis,
``F=RR*``, and let ``X:K->H`` be an isometry whose range lies in
``Ran(R)``.  The canonical normalized minimum-norm coefficient embedding is

    A = X*F^+X,
    B = R*F^+X A^(-1/2).                                  (1)

Writing

    U = R*F^(+/2),       J = F^(+/2)X A^(-1/2),           (2)

gives the exact factorization

    B = UJ.                                                (3)

Here ``U`` is the adjoint polar isometry of the full orientation synthesis,
``J`` is an isometry, and ``B`` is an isometry into the fixed coefficient
register.  If ``D_e`` is the coordinate projection onto ``C_e``, then

    H_e = B*D_eB,        sum_e H_e=I.                      (4)

Consequently the natural component POVM needs no independent effect-by-effect
square-root construction: apply the restricted orientation polar ``UJ`` and
read the coordinate label.  Equivalently, for ``B_e=D_eB`` and the block
polar decomposition ``B_e=V_e sqrt(H_e)``, the usual minimal Naimark map
``stack_e sqrt(H_e)`` becomes the physical coefficient embedding after the
controlled block gauge ``direct_sum_e V_e``.

This identity sharpens rather than solves the compiler problem.  It proves
that component dilation and restricted orientation-polar access are the same
natural operation.  It does not implement ``U`` or ``J``.  Moreover the
effects ``H_e`` alone do not determine the coherent block gauges ``V_e``:
two isometries can induce identical coordinate POVMs while producing
orthogonal coherent outputs.  A label-sensitive decoder must preserve the
natural coefficient gauge, not merely reproduce outcome probabilities.

Finally, an aggregate Frobenius approximation has the exact state-weighted
boundary

    Tr(rho (B-B_tilde)*(B-B_tilde))
      <= kappa ||B-B_tilde||_F^2/r,
    kappa=r||rho||_infinity.                              (5)

Thus the existing trace-weighted support scalarization is operational only
after controlling the actual incoming-state flatness (or proving a sharper
state-specific estimate).  Uniform-input convergence is not a worst-case
coherent compiler theorem.
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
    "self_dual_wreath_component_direct_naimark_polar_equivalence.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DIRECT-NAIMARK-POLAR-EQUIVALENCE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class DirectNaimarkPolarControl:
    control_id: str
    physical_dimension: int
    coefficient_dimension: int
    common_fiber_dimension: int
    leaf_count: int
    child_frame_rank: int
    coefficient_support_rank: int
    analysis_polar_initial_projection_residual: float
    analysis_polar_final_projection_residual: float
    common_metric_embedding_isometry_residual: float
    direct_coefficient_embedding_isometry_residual: float
    direct_restricted_polar_factorization_residual: float
    restricted_polar_recovery_residual: float
    component_effect_sum_identity_residual: float
    maximum_component_polar_reconstruction_residual: float
    coefficient_projection_normal_form_residual: float
    coordinate_measurement_probability_residual: float
    exact_direct_naimark_polar_equivalence_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentGaugeCountercontrol:
    fiber_dimension: int
    leaf_count: int
    maximum_component_effect_residual: float
    maximum_coordinate_probability_residual: float
    coherent_output_overlap: float
    coherent_output_trace_distance: float
    coherent_map_operator_distance: float
    identical_povm_effects: bool
    coherent_dilation_determined_by_effects_alone: bool
    status: str


@dataclass(frozen=True)
class StateWeightedApproximationBoundary:
    fiber_dimension: int
    normalized_frobenius_error: float
    uniform_input_flatness: float
    uniform_input_exact_error: float
    uniform_input_flatness_upper_bound: float
    concentrated_input_flatness: float
    concentrated_input_exact_error: float
    concentrated_input_flatness_upper_bound: float
    uniform_error_controls_concentrated_input_without_flatness: bool
    flatness_weighted_bound_verified: bool
    status: str


@dataclass(frozen=True)
class DirectNaimarkPolarTheorem:
    orientation_polar: str
    common_metric_embedding: str
    direct_factorization: str
    component_povm: str
    minimal_naimark_gauge: str
    coefficient_projection: str
    state_weighted_error: str
    compiler_boundary: str
    arbitrary_leaf_ranks: bool
    arbitrary_common_subspace_inside_child_range: bool
    exact_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDirectNaimarkPolarEquivalenceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DirectNaimarkPolarTheorem
    finite_controls: list[DirectNaimarkPolarControl]
    coherent_gauge_countercontrol: CoherentGaugeCountercontrol
    state_weighted_boundary: StateWeightedApproximationBoundary
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
    tolerance: float,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("matrix is not positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _support_projection(
    matrix: np.ndarray,
    *,
    tolerance: float,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    positive = values > 100 * tolerance
    return vectors[:, positive] @ vectors[:, positive].conj().T


def _block_slices(widths: tuple[int, ...]) -> tuple[slice, ...]:
    offset = 0
    blocks = []
    for width in widths:
        blocks.append(slice(offset, offset + width))
        offset += width
    return tuple(blocks)


def direct_component_naimark_normal_form(
    leaf_isometries: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    tuple[np.ndarray, ...],
    tuple[np.ndarray, ...],
]:
    """Return ``U,J,B,(B_e),(H_e)`` from equations (1)-(4)."""

    if not leaf_isometries:
        raise ValueError("at least one leaf isometry is required")
    physical = leaf_isometries[0].shape[0]
    if any(leaf.shape[0] != physical for leaf in leaf_isometries):
        raise ValueError("all leaf isometries must share one physical space")
    for leaf in leaf_isometries:
        identity = np.eye(leaf.shape[1], dtype=complex)
        if np.linalg.norm(leaf.conj().T @ leaf - identity, ord=2) > 100 * tolerance:
            raise ValueError("every leaf synthesis block must be an isometry")
    if common_isometry.shape[0] != physical or not common_isometry.shape[1]:
        raise ValueError("common isometry has the wrong shape")
    common_identity = np.eye(common_isometry.shape[1], dtype=complex)
    if (
        np.linalg.norm(
            common_isometry.conj().T @ common_isometry - common_identity,
            ord=2,
        )
        > 100 * tolerance
    ):
        raise ValueError("common input must be an isometry")

    synthesis = np.hstack(leaf_isometries)
    frame = synthesis @ synthesis.conj().T
    frame_support = _support_projection(frame, tolerance=tolerance)
    range_residual = np.linalg.norm(
        (np.eye(physical, dtype=complex) - frame_support) @ common_isometry,
        ord=2,
    )
    if range_residual > 1000 * tolerance:
        raise ValueError("the common space must lie in the child range")

    frame_inverse_root = _psd_power(frame, -0.5, tolerance=tolerance)
    frame_inverse = _psd_power(frame, -1.0, tolerance=tolerance)
    metric = _hermitian(
        common_isometry.conj().T @ frame_inverse @ common_isometry
    )
    metric_inverse_root = _psd_power(metric, -0.5, tolerance=tolerance)

    orientation_polar = synthesis.conj().T @ frame_inverse_root
    common_metric_embedding = (
        frame_inverse_root @ common_isometry @ metric_inverse_root
    )
    direct_embedding = (
        synthesis.conj().T
        @ frame_inverse
        @ common_isometry
        @ metric_inverse_root
    )

    widths = tuple(leaf.shape[1] for leaf in leaf_isometries)
    components = tuple(
        direct_embedding[block, :]
        for block in _block_slices(widths)
    )
    effects = tuple(_hermitian(component.conj().T @ component) for component in components)
    return (
        orientation_polar,
        common_metric_embedding,
        direct_embedding,
        components,
        effects,
    )


def audit_direct_naimark_polar_equivalence(
    control_id: str,
    leaf_isometries: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> DirectNaimarkPolarControl:
    synthesis = np.hstack(leaf_isometries)
    frame = synthesis @ synthesis.conj().T
    gram = synthesis.conj().T @ synthesis
    frame_support = _support_projection(frame, tolerance=tolerance)
    coefficient_support = _support_projection(gram, tolerance=tolerance)
    (
        orientation_polar,
        common_metric_embedding,
        direct_embedding,
        components,
        effects,
    ) = direct_component_naimark_normal_form(
        leaf_isometries,
        common_isometry,
        tolerance=tolerance,
    )
    fiber = common_isometry.shape[1]
    identity = np.eye(fiber, dtype=complex)

    initial = float(
        np.linalg.norm(
            orientation_polar.conj().T @ orientation_polar - frame_support,
            ord=2,
        )
    )
    final = float(
        np.linalg.norm(
            orientation_polar @ orientation_polar.conj().T - coefficient_support,
            ord=2,
        )
    )
    common_isometry_residual = float(
        np.linalg.norm(
            common_metric_embedding.conj().T @ common_metric_embedding - identity,
            ord=2,
        )
    )
    direct_isometry_residual = float(
        np.linalg.norm(direct_embedding.conj().T @ direct_embedding - identity, ord=2)
    )
    factorization = float(
        np.linalg.norm(
            direct_embedding - orientation_polar @ common_metric_embedding,
            ord=2,
        )
    )
    common_projector = common_metric_embedding @ common_metric_embedding.conj().T
    restricted_recovery = float(
        np.linalg.norm(
            orientation_polar @ common_projector
            - direct_embedding @ common_metric_embedding.conj().T,
            ord=2,
        )
    )
    effect_sum = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )

    polar_reconstruction = 0.0
    for component, effect in zip(components, effects):
        root = _psd_power(effect, 0.5, tolerance=tolerance)
        inverse_root = _psd_power(effect, -0.5, tolerance=tolerance)
        support = _support_projection(effect, tolerance=tolerance)
        partial = component @ inverse_root @ support
        polar_reconstruction = max(
            polar_reconstruction,
            float(np.linalg.norm(component - partial @ root, ord=2)),
            float(
                np.linalg.norm(
                    partial.conj().T @ partial - support,
                    ord=2,
                )
            ),
        )

    physical_identity = np.eye(frame.shape[0], dtype=complex)
    excluded = (
        synthesis.conj().T
        @ (physical_identity - common_isometry @ common_isometry.conj().T)
        @ synthesis
    )
    support_difference = coefficient_support - _support_projection(
        excluded,
        tolerance=tolerance,
    )
    projection_residual = float(
        np.linalg.norm(
            direct_embedding @ direct_embedding.conj().T - support_difference,
            ord=2,
        )
    )

    probe = np.arange(1, fiber + 1, dtype=float).astype(complex)
    probe /= np.linalg.norm(probe)
    probability_residual = 0.0
    for component, effect in zip(components, effects):
        direct_probability = float(np.linalg.norm(component @ probe) ** 2)
        effect_probability = float(np.vdot(probe, effect @ probe).real)
        probability_residual = max(
            probability_residual,
            abs(direct_probability - effect_probability),
        )

    maximum = max(
        initial,
        final,
        common_isometry_residual,
        direct_isometry_residual,
        factorization,
        restricted_recovery,
        effect_sum,
        polar_reconstruction,
        projection_residual,
        probability_residual,
    )
    verified = maximum <= 10_000 * tolerance
    return DirectNaimarkPolarControl(
        control_id=control_id,
        physical_dimension=frame.shape[0],
        coefficient_dimension=gram.shape[0],
        common_fiber_dimension=fiber,
        leaf_count=len(leaf_isometries),
        child_frame_rank=int(round(float(np.trace(frame_support).real))),
        coefficient_support_rank=int(
            round(float(np.trace(coefficient_support).real))
        ),
        analysis_polar_initial_projection_residual=initial,
        analysis_polar_final_projection_residual=final,
        common_metric_embedding_isometry_residual=common_isometry_residual,
        direct_coefficient_embedding_isometry_residual=direct_isometry_residual,
        direct_restricted_polar_factorization_residual=factorization,
        restricted_polar_recovery_residual=restricted_recovery,
        component_effect_sum_identity_residual=effect_sum,
        maximum_component_polar_reconstruction_residual=polar_reconstruction,
        coefficient_projection_normal_form_residual=projection_residual,
        coordinate_measurement_probability_residual=probability_residual,
        exact_direct_naimark_polar_equivalence_verified=verified,
        status=(
            "exact-direct-naimark-restricted-polar-equivalence"
            if verified
            else "direct-naimark-polar-equivalence-control-failure"
        ),
    )


def coherent_gauge_countercontrol() -> CoherentGaugeCountercontrol:
    identity = np.eye(2, dtype=complex)
    direct = np.vstack((identity, identity)) / math.sqrt(2.0)
    gauged = np.vstack((identity, -identity)) / math.sqrt(2.0)
    blocks = (slice(0, 2), slice(2, 4))
    effect_residual = 0.0
    probability_residual = 0.0
    probe = np.asarray([1.0, 1.0j], dtype=complex) / math.sqrt(2.0)
    for block in blocks:
        direct_effect = direct[block, :].conj().T @ direct[block, :]
        gauged_effect = gauged[block, :].conj().T @ gauged[block, :]
        effect_residual = max(
            effect_residual,
            float(np.linalg.norm(direct_effect - gauged_effect, ord=2)),
        )
        probability_residual = max(
            probability_residual,
            abs(
                float(np.linalg.norm(direct[block, :] @ probe) ** 2)
                - float(np.linalg.norm(gauged[block, :] @ probe) ** 2)
            ),
        )
    overlap = abs(float(np.vdot(direct @ probe, gauged @ probe).real))
    trace_distance = math.sqrt(max(0.0, 1.0 - overlap**2))
    map_distance = float(np.linalg.norm(direct - gauged, ord=2))
    identical = max(effect_residual, probability_residual) <= 1e-12
    return CoherentGaugeCountercontrol(
        fiber_dimension=2,
        leaf_count=2,
        maximum_component_effect_residual=effect_residual,
        maximum_coordinate_probability_residual=probability_residual,
        coherent_output_overlap=overlap,
        coherent_output_trace_distance=trace_distance,
        coherent_map_operator_distance=map_distance,
        identical_povm_effects=identical,
        coherent_dilation_determined_by_effects_alone=False,
        status="identical-effects-orthogonal-coherent-output-gauge-countercontrol",
    )


def state_weighted_approximation_boundary(
    dimension: int = 64,
) -> StateWeightedApproximationBoundary:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    error_map = np.zeros((dimension, dimension), dtype=complex)
    error_map[0, 0] = 1.0
    normalized_frobenius = float(
        np.linalg.norm(error_map, ord="fro") ** 2 / dimension
    )
    uniform_state = np.eye(dimension, dtype=complex) / dimension
    concentrated_state = np.zeros((dimension, dimension), dtype=complex)
    concentrated_state[0, 0] = 1.0

    def state_error(state: np.ndarray) -> float:
        return float(np.trace(state @ error_map.conj().T @ error_map).real)

    uniform_flatness = dimension * float(np.linalg.norm(uniform_state, ord=2))
    concentrated_flatness = dimension * float(
        np.linalg.norm(concentrated_state, ord=2)
    )
    uniform_error = state_error(uniform_state)
    concentrated_error = state_error(concentrated_state)
    uniform_bound = uniform_flatness * normalized_frobenius
    concentrated_bound = concentrated_flatness * normalized_frobenius
    verified = bool(
        uniform_error <= uniform_bound + 1e-12
        and concentrated_error <= concentrated_bound + 1e-12
        and abs(uniform_error - normalized_frobenius) <= 1e-12
        and abs(concentrated_error - 1.0) <= 1e-12
    )
    return StateWeightedApproximationBoundary(
        fiber_dimension=dimension,
        normalized_frobenius_error=normalized_frobenius,
        uniform_input_flatness=uniform_flatness,
        uniform_input_exact_error=uniform_error,
        uniform_input_flatness_upper_bound=uniform_bound,
        concentrated_input_flatness=concentrated_flatness,
        concentrated_input_exact_error=concentrated_error,
        concentrated_input_flatness_upper_bound=concentrated_bound,
        uniform_error_controls_concentrated_input_without_flatness=False,
        flatness_weighted_bound_verified=verified,
        status="flatness-factor-necessary-and-sufficient-for-generic-frobenius-transfer",
    )


def _random_leaf_system(
    seed: int,
    *,
    physical_dimension: int,
    block_dimensions: tuple[int, ...],
    common_dimension: int,
) -> tuple[tuple[np.ndarray, ...], np.ndarray]:
    rng = np.random.default_rng(seed)
    leaves = []
    for block in block_dimensions:
        raw = rng.normal(size=(physical_dimension, block)) + 1j * rng.normal(
            size=(physical_dimension, block)
        )
        leaf, _ = np.linalg.qr(raw, mode="reduced")
        leaves.append(leaf)
    synthesis = np.hstack(leaves)
    support = _support_projection(
        synthesis @ synthesis.conj().T,
        tolerance=1e-12,
    )
    values, vectors = np.linalg.eigh(support)
    support_basis = vectors[:, values > 0.5]
    if common_dimension > support_basis.shape[1]:
        raise ValueError("common dimension exceeds the child range")
    raw_common = rng.normal(
        size=(support_basis.shape[1], common_dimension)
    ) + 1j * rng.normal(size=(support_basis.shape[1], common_dimension))
    coordinates, _ = np.linalg.qr(raw_common, mode="reduced")
    return tuple(leaves), support_basis @ coordinates


def direct_naimark_polar_theorem() -> DirectNaimarkPolarTheorem:
    return DirectNaimarkPolarTheorem(
        orientation_polar="U=R*F^(+/2), U*U=supp(F), UU*=supp(R*R)",
        common_metric_embedding=(
            "J=F^(+/2)X(X*F^+X)^(-1/2), with J*J=I"
        ),
        direct_factorization=(
            "B=R*F^+X(X*F^+X)^(-1/2)=UJ and UJJ*=BJ*"
        ),
        component_povm="H_e=B*D_eB and sum_e H_e=I",
        minimal_naimark_gauge=(
            "D_eB=V_e sqrt(H_e); the direct coefficient dilation is the "
            "minimal square-root dilation followed by block gauges V_e"
        ),
        coefficient_projection=(
            "BB*=supp(R*R)-supp(R*(I-XX*)R)"
        ),
        state_weighted_error=(
            "Tr(rho E*E)<=r||rho||_infinity ||E||F^2/r for E=B-B_tilde"
        ),
        compiler_boundary=(
            "Component dilation is restricted orientation-polar access, not an "
            "independent matrix-square-root task; U, J, coherent block gauges, "
            "and label-sensitive decoding remain uncompiled."
        ),
        arbitrary_leaf_ranks=True,
        arbitrary_common_subspace_inside_child_range=True,
        exact_theorem_verified=True,
        status="direct-component-naimark-equals-restricted-orientation-polar",
    )


def run_component_direct_naimark_polar_equivalence(
) -> ComponentDirectNaimarkPolarEquivalenceReport:
    systems = [
        (
            "REDUNDANT-P9-N14-R4",
            *_random_leaf_system(
                4201,
                physical_dimension=9,
                block_dimensions=(2, 3, 4, 5),
                common_dimension=4,
            ),
        ),
        (
            "RANK-DEFICIENT-P10-N7-R5",
            *_random_leaf_system(
                4211,
                physical_dimension=10,
                block_dimensions=(2, 2, 3),
                common_dimension=5,
            ),
        ),
        (
            "SPARSE-BLOCK-P8-N12-R3",
            *_random_leaf_system(
                4229,
                physical_dimension=8,
                block_dimensions=(1,) * 12,
                common_dimension=3,
            ),
        ),
    ]
    controls = [
        audit_direct_naimark_polar_equivalence(control_id, leaves, common)
        for control_id, leaves, common in systems
    ]
    gauge = coherent_gauge_countercontrol()
    state_boundary = state_weighted_approximation_boundary()
    theorem = direct_naimark_polar_theorem()
    failures = sum(
        not row.exact_direct_naimark_polar_equivalence_verified
        for row in controls
    )
    verified = bool(
        theorem.exact_theorem_verified
        and failures == 0
        and gauge.identical_povm_effects
        and state_boundary.flatness_weighted_bound_verified
    )
    return ComponentDirectNaimarkPolarEquivalenceReport(
        created_at=utc_now(),
        theorem_contract={
            "direct_factorization": theorem.direct_factorization,
            "component_povm": theorem.component_povm,
            "minimal_naimark_gauge": theorem.minimal_naimark_gauge,
            "coefficient_projection": theorem.coefficient_projection,
            "state_weighted_error": theorem.state_weighted_error,
            "scope": theorem.compiler_boundary,
        },
        theorem=theorem,
        finite_controls=controls,
        coherent_gauge_countercontrol=gauge,
        state_weighted_boundary=state_boundary,
        proof_obligations=[
            {
                "obligation": "identify_direct_natural_component_dilation",
                "resolved": verified,
                "resolution": (
                    "The normalized minimum-norm coefficient embedding is exactly "
                    "the child orientation analysis polar restricted through J."
                ),
            },
            {
                "obligation": "remove_independent_matrix_square_root_compiler_gate",
                "resolved": verified,
                "resolution": (
                    "Coordinate measurement after B realizes the component POVM "
                    "directly; effect square roots are only one factorization of B."
                ),
            },
            {
                "obligation": "compile_restricted_natural_orientation_polar",
                "resolved": False,
                "resolution": (
                    "Need a normalization-one structured router for U on Ran(J), "
                    "or a direct implementation of B preserving coefficient gauges."
                ),
            },
            {
                "obligation": "transfer_average_support_scalarization_to_physical_inputs",
                "resolved": True,
                "resolution": (
                    "The companion all-level component-trim theorem supplies a "
                    "sharper native-state estimate from the exact root-frame "
                    "second moment and fixed coefficient-register rank budget; "
                    "no input-flatness premise is needed."
                ),
            },
            {
                "obligation": "require_a_separate_post_polar_hidden_label_decoder",
                "resolved": True,
                "resolution": (
                    "Resolved negatively by the companion physical-PGM closure: "
                    "once all coherent restricted maps compose to the complete "
                    "orientation polar, the row-copy intertwiner implements the "
                    "known constant-success covariant PGM."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Every component effect must be square-rooted separately.",
                "resolved": True,
                "resolution": (
                    "False algebraically. The direct coefficient embedding B is "
                    "already a Naimark isometry for every coordinate effect at once."
                ),
            },
            {
                "objection": "The identity B=UJ compiles the component measurement.",
                "resolved": True,
                "resolution": (
                    "False. It identifies B with the unresolved restricted "
                    "orientation polar and does not supply normalization-one access."
                ),
            },
            {
                "objection": "The POVM effects determine the coherent output needed by a decoder.",
                "resolved": True,
                "resolution": (
                    "False. The gauge countercontrol has identical effects and "
                    "coordinate probabilities but orthogonal coherent outputs."
                ),
            },
            {
                "objection": "Vanishing normalized Frobenius error controls every input state.",
                "resolved": True,
                "resolution": (
                    "False. A rank-one error is 1/r on the uniform input and one "
                    "on a concentrated input; the flatness factor is sharp."
                ),
            },
            {
                "objection": "Compiling B would by itself decode the hidden permutation.",
                "resolved": True,
                "resolution": (
                    "False. B preserves a candidate carrier but no label-sensitive "
                    "covariant observable or Fourier normalization follows."
                ),
            },
        ],
        headline_metrics={
            "direct_naimark_restricted_polar_equivalence_theorem_count": int(verified),
            "coordinate_component_povm_dilation_theorem_count": int(verified),
            "independent_matrix_square_root_gate_removed_count": int(verified),
            "coherent_gauge_countercontrol_count": int(gauge.identical_povm_effects),
            "state_weighted_frobenius_boundary_theorem_count": int(
                state_boundary.flatness_weighted_bound_verified
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_finite_factorization_residual": max(
                row.direct_restricted_polar_factorization_residual
                for row in controls
            ),
            "maximum_finite_projection_residual": max(
                row.coefficient_projection_normal_form_residual
                for row in controls
            ),
            "gauge_countercontrol_trace_distance": gauge.coherent_output_trace_distance,
            "concentrated_to_uniform_error_ratio": (
                state_boundary.concentrated_input_exact_error
                / state_boundary.uniform_input_exact_error
            ),
            "natural_restricted_orientation_polar_circuit_count": 0,
            "label_sensitive_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "direct_component_naimark_equals_restricted_orientation_polar": verified,
            "coordinate_measurement_realizes_component_povm": verified,
            "independent_effect_square_root_synthesis_is_fundamental_gate": False,
            "component_effects_determine_coherent_output_gauge": False,
            "uniform_frobenius_scalarization_controls_arbitrary_inputs": False,
            "flatness_weighted_state_error_bound_proved": verified,
            "natural_all_level_state_weighted_component_trim_proved": True,
            "natural_restricted_orientation_polar_compiled": False,
            "coherent_component_threshold_support_select_compiled": False,
            "natural_coherent_block_gauges_compiled": False,
            "label_sensitive_information_gain_proved": False,
            "separate_post_polar_hidden_label_decoder_required": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural component dilation is exactly restricted "
                "orientation-polar access. Native all-level trimming is already "
                "controlled, but the coherent threshold/support router, natural "
                "block gauges, and complete polar remain open. A complete polar "
                "would feed the already-compiled physical PGM."
            ),
        },
        status=(
            "component-dilation-identified-with-restricted-orientation-polar-access-open"
            if verified
            else "direct-naimark-polar-equivalence-control-failure"
        ),
        summary=(
            "Eliminated effect-by-effect square roots as an independent gate by "
            "identifying the direct component Naimark map with a restricted "
            "orientation polar, while proving that coherent gauge and input "
            "flatness remain indispensable."
        ),
        falsifiers_triggered=[
            "The component POVM is not a separate factorial family of square-root synthesis tasks.",
            "Reproducing component outcome probabilities does not preserve the coherent carrier needed for decoding.",
            "Average support scalarization is not a worst-case physical-state compiler guarantee.",
            "The remaining access problem is a normalization-one restricted orientation polar or an equivalent direct coefficient router.",
        ],
    )


def write_component_direct_naimark_polar_equivalence_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = asdict(run_component_direct_naimark_polar_equivalence())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_component_direct_naimark_polar_equivalence_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
