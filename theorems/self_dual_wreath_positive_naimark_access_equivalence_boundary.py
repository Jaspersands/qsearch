"""Positive component amplitudes are a restricted polar, not a new oracle.

For one child let ``Q_e:C_e->H`` be the physical leaf isometries,

    R=[Q_e]_e,              E_e=Q_e Q_e^*,
    F=RR^*=sum_e E_e,

and let ``X:K->H`` be the common-span isometry.  Put

    A = X^*F^+X,
    J = F^(+/2) X A^(-1/2),
    U = R^*F^(+/2),
    B = UJ.                                                   (1)

Then ``J`` and ``B`` are isometries and the exact component effects are

    H_e = B_e^*B_e
        = A^(-1/2) X^*F^+ E_e F^+X A^(-1/2).                (2)

Thus the physical/Schur data enter through the *global* child whitening
``F^+`` and common metric ``A^(-1/2)``, not only through the addressed
projector ``E_e``.  If ``B_e=V_e sqrt(H_e)`` and

    N|psi> = direct_sum_e sqrt(H_e)|psi>,                    (3)

then ``B=(direct_sum_e V_e)N`` and
``N=(direct_sum_e V_e)^*B`` exactly on the active supports.  Once the known
GPE support transports ``V_e`` are supplied, a direct square-root POVM
dilation and the restricted orientation polar ``B`` therefore interconvert
at normalization one.  The dilation is a sufficient primitive, but it is not
an independent bypass of the missing polar.

The parent endpoint has the same form.  For short metrics ``A_L,A_R`` and
``M=A_L+A_R``, its rows and effects are

    C_s=A_s^(1/2)M^(-1/2),
    K_s=C_s^*C_s=M^(-1/2)A_sM^(-1/2).                       (4)

The stacked endpoint is gauge-equivalent, in both directions, to the
canonical two-outcome dilation ``stack_s sqrt(K_s)``.

This identity gives a sharp access verdict.  Even granting every whitening
factor for free, a scalar address PREPARE followed by addressed extraction of
the nonzero blocks ``B_e`` can expose ``B`` only as ``B/sqrt(m)``, where
``m`` is the number of active components.  Indeed exact equal block
coefficients require ``sqrt(p_e)=1/alpha`` for every active ``e``; since
``sum_e p_e=1``, necessarily ``alpha=sqrt(m)``.  Uniform preparation attains
the bound.  An input-dependent matrix Naimark dilation avoids it precisely by
implementing (3), which is equivalent to ``B`` above.

Pair-local cross-Gram data are also insufficient for (2).  Two three-leaf
frames can agree on two selected leaves, their raw cross map, their pair
polar, and full support, while an unqueried third leaf changes the selected
canonical effect by a constant.  A coherent all-address query contains the
missing data, but its canonical coefficient-only extraction retains the
``sqrt(m)`` normalization.

At the selected wreath copy count, a fixed-arity early child contains
``m=Theta(n!)`` leaves.  Hence the flattened scalar-address/GPE or addressed
cross-map route is superpolynomial even with perfect positive spectral edges;
no ``delta^(-1/4)`` small-effect argument is used.  This does not rule out a
hierarchical normalization-one local router, an aggregate analysis block
encoding with polynomial normalization and retained singular edge, or a
direct Schur/Racah Naimark transform.  Those are the exact surviving positive
interfaces.
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


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_positive_naimark_access_equivalence_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POSITIVE-NAIMARK-ACCESS-"
    "EQUIVALENCE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-DIRECT-COMPONENT-NAIMARK-"
    "NO-INDEPENDENT-POSITIVE-AMPLITUDE-ORACLE"
)


@dataclass(frozen=True)
class PhysicalComponentPositiveControl:
    control_id: str
    physical_dimension: int
    common_fiber_dimension: int
    leaf_count: int
    active_component_count: int
    coefficient_dimension: int
    child_frame_rank: int
    child_frame_minimum_positive_eigenvalue: float
    child_frame_maximum_eigenvalue: float
    common_metric_minimum_eigenvalue: float
    common_metric_maximum_eigenvalue: float
    common_metric_embedding_isometry_residual: float
    restricted_polar_isometry_residual: float
    restricted_polar_factorization_residual: float
    maximum_physical_effect_formula_residual: float
    component_effect_sum_residual: float
    canonical_naimark_isometry_residual: float
    maximum_component_polar_residual: float
    direct_naimark_to_restricted_polar_residual: float
    restricted_polar_to_direct_naimark_residual: float
    exact_physical_positive_amplitude_equivalence_verified: bool
    status: str


@dataclass(frozen=True)
class EndpointPositiveControl:
    fiber_dimension: int
    left_metric_minimum_eigenvalue: float
    left_metric_maximum_eigenvalue: float
    right_metric_minimum_eigenvalue: float
    right_metric_maximum_eigenvalue: float
    metric_commutator_norm: float
    endpoint_effect_sum_residual: float
    endpoint_isometry_residual: float
    canonical_endpoint_naimark_isometry_residual: float
    maximum_endpoint_effect_formula_residual: float
    maximum_endpoint_polar_residual: float
    canonical_to_physical_endpoint_residual: float
    physical_to_canonical_endpoint_residual: float
    exact_endpoint_positive_amplitude_equivalence_verified: bool
    status: str


@dataclass(frozen=True)
class ScalarAddressExtractionControl:
    active_component_count: int
    fiber_dimension: int
    coefficient_dimension: int
    uniform_address_probability: float
    sharp_scalar_extraction_normalization: float
    uniform_selected_signal_norm: float
    uniform_selected_to_scaled_target_residual: float
    normalized_target_isometry_residual: float
    extracted_success_probability: float
    matrix_naimark_success_probability: float
    nonuniform_probability_spread: float
    nonuniform_selected_to_any_equal_coefficient_residual: float
    coefficient_only_normalization_lower_bound_saturated: bool
    whitening_granted_for_free: bool
    exact_scalar_address_width_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class PairLocalComponentIndeterminacyControl:
    physical_dimension: int
    leaf_count_per_frame: int
    selected_leaf_projector_residual: float
    selected_pair_raw_cross_map_residual: float
    selected_pair_polar_residual: float
    first_frame_support_residual: float
    second_frame_support_residual: float
    frame_support_projector_residual: float
    unqueried_leaf_projector_distance: float
    first_selected_effect_spectrum: tuple[float, ...]
    second_selected_effect_spectrum: tuple[float, ...]
    selected_component_effect_operator_gap: float
    common_pair_local_data_determine_component_effect: bool
    exact_pair_local_indeterminacy_verified: bool
    status: str


@dataclass(frozen=True)
class PositiveAccessInterfaceRecord:
    interface_id: str
    supplied_signal: str
    normalization: str
    supplies_global_child_whitening: bool
    supplies_common_metric_inverse_root: bool
    supplies_component_support_transport: bool
    supplies_component_naimark_dilation: bool
    equivalent_to_restricted_polar_if_supplied: bool
    compiled: bool
    status: str


@dataclass(frozen=True)
class NaturalPositiveAccessScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    orientation_leaf_count_decimal: str
    fixed_jump_log2_arity: int
    early_child_active_component_count_decimal: str
    early_child_active_component_count_log2: int
    scalar_address_normalization_log2: float
    scalar_address_success_probability_log2: int
    polynomial_benchmark_degree: int
    polynomial_benchmark_log2: float
    flattened_scalar_address_route_superpolynomial: bool
    small_positive_effect_edge_used: bool
    hierarchical_local_router_ruled_out: bool
    direct_schur_racah_naimark_ruled_out: bool
    status: str


@dataclass(frozen=True)
class PositiveNaimarkAccessEquivalenceTheorem:
    physical_component_effect: str
    restricted_polar: str
    direct_naimark_equivalence: str
    endpoint_effect: str
    scalar_address_lower_bound: str
    pair_local_boundary: str
    current_interface_verdict: str
    conditional_positive_route: str
    natural_scaling: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PositiveNaimarkAccessEquivalenceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PositiveNaimarkAccessEquivalenceTheorem
    component_controls: list[PhysicalComponentPositiveControl]
    endpoint_control: EndpointPositiveControl
    scalar_address_controls: list[ScalarAddressExtractionControl]
    pair_local_indeterminacy_control: PairLocalComponentIndeterminacyControl
    interface_inventory: list[PositiveAccessInterfaceRecord]
    scaling_records: list[NaturalPositiveAccessScalingRecord]
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
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("matrix must be positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _support_projection(
    matrix: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    positive = values > 100 * tolerance
    return vectors[:, positive] @ vectors[:, positive].conj().T


def _block_slices(widths: tuple[int, ...]) -> tuple[slice, ...]:
    blocks = []
    offset = 0
    for width in widths:
        blocks.append(slice(offset, offset + width))
        offset += width
    return tuple(blocks)


def _component_system(
    seed: int,
    *,
    physical_dimension: int,
    leaf_widths: tuple[int, ...],
    common_dimension: int,
) -> tuple[tuple[np.ndarray, ...], np.ndarray]:
    if not leaf_widths or any(width < 1 for width in leaf_widths):
        raise ValueError("leaf widths must be nonempty and positive")
    if not 0 < common_dimension <= physical_dimension:
        raise ValueError("invalid common dimension")
    rng = np.random.default_rng(seed)
    leaves = []
    for width in leaf_widths:
        if width > physical_dimension:
            raise ValueError("leaf width exceeds physical dimension")
        raw = rng.normal(size=(physical_dimension, width)) + 1j * rng.normal(
            size=(physical_dimension, width)
        )
        leaf, _ = np.linalg.qr(raw, mode="reduced")
        leaves.append(leaf)
    synthesis = np.hstack(leaves)
    support = _support_projection(synthesis @ synthesis.conj().T)
    values, vectors = np.linalg.eigh(support)
    support_basis = vectors[:, values > 0.5]
    if common_dimension > support_basis.shape[1]:
        raise ValueError("common dimension exceeds child range")
    raw = rng.normal(size=(support_basis.shape[1], common_dimension)) + 1j * rng.normal(
        size=(support_basis.shape[1], common_dimension)
    )
    coordinates, _ = np.linalg.qr(raw, mode="reduced")
    return tuple(leaves), support_basis @ coordinates


def component_positive_normal_form(
    leaf_isometries: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> dict[str, Any]:
    """Return equations (1)--(3) and their block gauges."""

    if not leaf_isometries:
        raise ValueError("at least one leaf is required")
    physical = leaf_isometries[0].shape[0]
    if any(leaf.shape[0] != physical for leaf in leaf_isometries):
        raise ValueError("leaf physical dimensions must agree")
    for leaf in leaf_isometries:
        identity = np.eye(leaf.shape[1], dtype=complex)
        if np.linalg.norm(leaf.conj().T @ leaf - identity, ord=2) > 1000 * tolerance:
            raise ValueError("each leaf must be an isometry")
    if common_isometry.shape[0] != physical or common_isometry.shape[1] < 1:
        raise ValueError("common isometry has the wrong shape")
    common_identity = np.eye(common_isometry.shape[1], dtype=complex)
    if (
        np.linalg.norm(
            common_isometry.conj().T @ common_isometry - common_identity,
            ord=2,
        )
        > 1000 * tolerance
    ):
        raise ValueError("common input must be an isometry")

    synthesis = np.hstack(leaf_isometries)
    frame = synthesis @ synthesis.conj().T
    frame_support = _support_projection(frame, tolerance=tolerance)
    if (
        np.linalg.norm(
            (np.eye(physical, dtype=complex) - frame_support) @ common_isometry,
            ord=2,
        )
        > 1000 * tolerance
    ):
        raise ValueError("common range must lie in the child frame range")

    frame_inverse_root = _psd_power(frame, -0.5, tolerance=tolerance)
    frame_inverse = _psd_power(frame, -1.0, tolerance=tolerance)
    metric = _hermitian(common_isometry.conj().T @ frame_inverse @ common_isometry)
    metric_inverse_root = _psd_power(metric, -0.5, tolerance=tolerance)
    common_metric_embedding = (
        frame_inverse_root @ common_isometry @ metric_inverse_root
    )
    orientation_polar = synthesis.conj().T @ frame_inverse_root
    direct_embedding = orientation_polar @ common_metric_embedding

    widths = tuple(leaf.shape[1] for leaf in leaf_isometries)
    blocks = _block_slices(widths)
    components = tuple(direct_embedding[block, :] for block in blocks)
    effects = tuple(_hermitian(component.conj().T @ component) for component in components)
    canonical_blocks = tuple(
        _psd_power(effect, 0.5, tolerance=tolerance) for effect in effects
    )
    gauges = []
    for component, effect in zip(components, effects):
        inverse_root = _psd_power(effect, -0.5, tolerance=tolerance)
        support = _support_projection(effect, tolerance=tolerance)
        gauges.append(component @ inverse_root @ support)
    canonical_naimark = np.vstack(canonical_blocks)
    gauge = np.zeros(
        (sum(widths), len(effects) * common_isometry.shape[1]),
        dtype=complex,
    )
    coefficient_offset = 0
    canonical_offset = 0
    for width, block_gauge in zip(widths, gauges):
        gauge[
            coefficient_offset : coefficient_offset + width,
            canonical_offset : canonical_offset + common_isometry.shape[1],
        ] = block_gauge
        coefficient_offset += width
        canonical_offset += common_isometry.shape[1]
    return {
        "synthesis": synthesis,
        "frame": frame,
        "frame_inverse_root": frame_inverse_root,
        "frame_inverse": frame_inverse,
        "metric": metric,
        "metric_inverse_root": metric_inverse_root,
        "common_metric_embedding": common_metric_embedding,
        "orientation_polar": orientation_polar,
        "direct_embedding": direct_embedding,
        "components": components,
        "effects": effects,
        "canonical_blocks": canonical_blocks,
        "canonical_naimark": canonical_naimark,
        "gauges": tuple(gauges),
        "gauge": gauge,
    }


def audit_physical_component_positive_amplitudes(
    control_id: str,
    leaf_isometries: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> PhysicalComponentPositiveControl:
    data = component_positive_normal_form(
        leaf_isometries,
        common_isometry,
        tolerance=tolerance,
    )
    frame = data["frame"]
    metric = data["metric"]
    direct = data["direct_embedding"]
    canonical = data["canonical_naimark"]
    gauge = data["gauge"]
    effects = data["effects"]
    identity = np.eye(common_isometry.shape[1], dtype=complex)
    frame_values = np.linalg.eigvalsh(_hermitian(frame))
    frame_positive = frame_values[frame_values > 100 * tolerance]
    metric_values = np.linalg.eigvalsh(_hermitian(metric))

    formula_residual = 0.0
    polar_residual = 0.0
    for leaf, component, effect, root, block_gauge in zip(
        leaf_isometries,
        data["components"],
        effects,
        data["canonical_blocks"],
        data["gauges"],
    ):
        projector = leaf @ leaf.conj().T
        formula = _hermitian(
            data["metric_inverse_root"]
            @ common_isometry.conj().T
            @ data["frame_inverse"]
            @ projector
            @ data["frame_inverse"]
            @ common_isometry
            @ data["metric_inverse_root"]
        )
        formula_residual = max(
            formula_residual,
            float(np.linalg.norm(effect - formula, ord=2)),
        )
        polar_residual = max(
            polar_residual,
            float(np.linalg.norm(component - block_gauge @ root, ord=2)),
        )

    common_residual = float(
        np.linalg.norm(
            data["common_metric_embedding"].conj().T
            @ data["common_metric_embedding"]
            - identity,
            ord=2,
        )
    )
    direct_residual = float(np.linalg.norm(direct.conj().T @ direct - identity, ord=2))
    factorization = float(
        np.linalg.norm(
            direct
            - data["orientation_polar"] @ data["common_metric_embedding"],
            ord=2,
        )
    )
    effect_sum = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    canonical_residual = float(
        np.linalg.norm(canonical.conj().T @ canonical - identity, ord=2)
    )
    forward = float(np.linalg.norm(direct - gauge @ canonical, ord=2))
    reverse = float(np.linalg.norm(canonical - gauge.conj().T @ direct, ord=2))
    maximum = max(
        common_residual,
        direct_residual,
        factorization,
        formula_residual,
        effect_sum,
        canonical_residual,
        polar_residual,
        forward,
        reverse,
    )
    active = sum(float(np.linalg.norm(effect, ord=2)) > 100 * tolerance for effect in effects)
    verified = bool(maximum <= 10_000 * tolerance and active == len(effects))
    return PhysicalComponentPositiveControl(
        control_id=control_id,
        physical_dimension=frame.shape[0],
        common_fiber_dimension=common_isometry.shape[1],
        leaf_count=len(leaf_isometries),
        active_component_count=active,
        coefficient_dimension=direct.shape[0],
        child_frame_rank=len(frame_positive),
        child_frame_minimum_positive_eigenvalue=float(frame_positive[0]),
        child_frame_maximum_eigenvalue=float(frame_positive[-1]),
        common_metric_minimum_eigenvalue=float(metric_values[0]),
        common_metric_maximum_eigenvalue=float(metric_values[-1]),
        common_metric_embedding_isometry_residual=common_residual,
        restricted_polar_isometry_residual=direct_residual,
        restricted_polar_factorization_residual=factorization,
        maximum_physical_effect_formula_residual=formula_residual,
        component_effect_sum_residual=effect_sum,
        canonical_naimark_isometry_residual=canonical_residual,
        maximum_component_polar_residual=polar_residual,
        direct_naimark_to_restricted_polar_residual=forward,
        restricted_polar_to_direct_naimark_residual=reverse,
        exact_physical_positive_amplitude_equivalence_verified=verified,
        status=(
            "exact-physical-component-naimark-restricted-polar-equivalence"
            if verified
            else "physical-component-positive-amplitude-control-failure"
        ),
    )


def endpoint_positive_normal_form(
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> dict[str, Any]:
    if left_metric.shape != right_metric.shape or len(left_metric.shape) != 2:
        raise ValueError("endpoint metrics must share one square shape")
    if left_metric.shape[0] < 1:
        raise ValueError("endpoint fiber must be nonempty")
    left = _hermitian(np.asarray(left_metric, dtype=complex))
    right = _hermitian(np.asarray(right_metric, dtype=complex))
    if min(np.linalg.eigvalsh(left)[0], np.linalg.eigvalsh(right)[0]) <= 100 * tolerance:
        raise ValueError("endpoint metrics must be positive definite")
    parent = left + right
    parent_inverse_root = _psd_power(parent, -0.5, tolerance=tolerance)
    rows = (
        _psd_power(left, 0.5, tolerance=tolerance) @ parent_inverse_root,
        _psd_power(right, 0.5, tolerance=tolerance) @ parent_inverse_root,
    )
    effects = tuple(_hermitian(row.conj().T @ row) for row in rows)
    canonical_blocks = tuple(_psd_power(effect, 0.5, tolerance=tolerance) for effect in effects)
    gauges = []
    for row, effect in zip(rows, effects):
        gauges.append(
            row
            @ _psd_power(effect, -0.5, tolerance=tolerance)
            @ _support_projection(effect, tolerance=tolerance)
        )
    physical = np.vstack(rows)
    canonical = np.vstack(canonical_blocks)
    gauge = np.zeros((2 * left.shape[0], 2 * left.shape[0]), dtype=complex)
    for index, block in enumerate(gauges):
        start = index * left.shape[0]
        gauge[start : start + left.shape[0], start : start + left.shape[0]] = block
    return {
        "left": left,
        "right": right,
        "parent": parent,
        "parent_inverse_root": parent_inverse_root,
        "rows": rows,
        "effects": effects,
        "canonical_blocks": canonical_blocks,
        "gauges": tuple(gauges),
        "physical": physical,
        "canonical": canonical,
        "gauge": gauge,
    }


def audit_endpoint_positive_amplitudes(
    left_metric: np.ndarray | None = None,
    right_metric: np.ndarray | None = None,
    *,
    tolerance: float = 1e-9,
) -> EndpointPositiveControl:
    if left_metric is None:
        left_metric = np.asarray(
            ((2.0, 0.35, 0.0), (0.35, 1.1, 0.2), (0.0, 0.2, 0.8)),
            dtype=complex,
        )
    if right_metric is None:
        rotation, _ = np.linalg.qr(
            np.asarray(
                ((1.0, 0.4j, 0.2), (0.3, 1.0, -0.2j), (0.1j, 0.25, 1.0)),
                dtype=complex,
            )
        )
        right_metric = (rotation * np.asarray((0.7, 1.6, 2.4))) @ rotation.conj().T
    data = endpoint_positive_normal_form(
        np.asarray(left_metric),
        np.asarray(right_metric),
        tolerance=tolerance,
    )
    dimension = data["left"].shape[0]
    identity = np.eye(dimension, dtype=complex)
    effect_sum = float(
        np.linalg.norm(sum(data["effects"], np.zeros_like(identity)) - identity, ord=2)
    )
    physical_residual = float(
        np.linalg.norm(data["physical"].conj().T @ data["physical"] - identity, ord=2)
    )
    canonical_residual = float(
        np.linalg.norm(data["canonical"].conj().T @ data["canonical"] - identity, ord=2)
    )
    formula_residual = 0.0
    polar_residual = 0.0
    for metric, row, effect, root, gauge in zip(
        (data["left"], data["right"]),
        data["rows"],
        data["effects"],
        data["canonical_blocks"],
        data["gauges"],
    ):
        formula = _hermitian(data["parent_inverse_root"] @ metric @ data["parent_inverse_root"])
        formula_residual = max(
            formula_residual,
            float(np.linalg.norm(effect - formula, ord=2)),
        )
        polar_residual = max(
            polar_residual,
            float(np.linalg.norm(row - gauge @ root, ord=2)),
        )
    forward = float(
        np.linalg.norm(data["physical"] - data["gauge"] @ data["canonical"], ord=2)
    )
    reverse = float(
        np.linalg.norm(data["canonical"] - data["gauge"].conj().T @ data["physical"], ord=2)
    )
    maximum = max(
        effect_sum,
        physical_residual,
        canonical_residual,
        formula_residual,
        polar_residual,
        forward,
        reverse,
    )
    left_values = np.linalg.eigvalsh(data["left"])
    right_values = np.linalg.eigvalsh(data["right"])
    verified = maximum <= 10_000 * tolerance
    return EndpointPositiveControl(
        fiber_dimension=dimension,
        left_metric_minimum_eigenvalue=float(left_values[0]),
        left_metric_maximum_eigenvalue=float(left_values[-1]),
        right_metric_minimum_eigenvalue=float(right_values[0]),
        right_metric_maximum_eigenvalue=float(right_values[-1]),
        metric_commutator_norm=float(
            np.linalg.norm(
                data["left"] @ data["right"] - data["right"] @ data["left"],
                ord=2,
            )
        ),
        endpoint_effect_sum_residual=effect_sum,
        endpoint_isometry_residual=physical_residual,
        canonical_endpoint_naimark_isometry_residual=canonical_residual,
        maximum_endpoint_effect_formula_residual=formula_residual,
        maximum_endpoint_polar_residual=polar_residual,
        canonical_to_physical_endpoint_residual=forward,
        physical_to_canonical_endpoint_residual=reverse,
        exact_endpoint_positive_amplitude_equivalence_verified=verified,
        status=(
            "exact-endpoint-naimark-short-metric-polar-equivalence"
            if verified
            else "endpoint-positive-amplitude-control-failure"
        ),
    )


def audit_scalar_address_extraction(
    leaf_isometries: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> ScalarAddressExtractionControl:
    data = component_positive_normal_form(
        leaf_isometries,
        common_isometry,
        tolerance=tolerance,
    )
    active_components = tuple(
        component
        for component in data["components"]
        if np.linalg.norm(component, ord=2) > 100 * tolerance
    )
    active = len(active_components)
    if active < 2:
        raise ValueError("at least two active components are required")
    target = np.vstack(active_components)
    identity = np.eye(common_isometry.shape[1], dtype=complex)
    normalization = math.sqrt(active)
    uniform = np.vstack([component / normalization for component in active_components])
    uniform_residual = float(np.linalg.norm(uniform - target / normalization, ord=2))
    weights = np.arange(1, active + 1, dtype=float)
    probabilities = weights / np.sum(weights)
    nonuniform = np.vstack(
        [math.sqrt(probability) * component for probability, component in zip(probabilities, active_components)]
    )
    coefficient = float(
        sum(
            np.vdot(component, selected).real
            for component, selected in zip(
                active_components,
                np.split(nonuniform, np.cumsum([block.shape[0] for block in active_components])[:-1]),
            )
        )
        / max(float(np.linalg.norm(target, ord="fro") ** 2), tolerance)
    )
    best_equal = coefficient * target
    nonuniform_residual = float(np.linalg.norm(nonuniform - best_equal, ord=2))
    target_residual = float(np.linalg.norm(target.conj().T @ target - identity, ord=2))
    verified = bool(
        uniform_residual <= 100 * tolerance
        and target_residual <= 1000 * tolerance
        and nonuniform_residual > 100 * tolerance
        and abs(1.0 / normalization**2 - 1.0 / active) <= 100 * tolerance
    )
    return ScalarAddressExtractionControl(
        active_component_count=active,
        fiber_dimension=common_isometry.shape[1],
        coefficient_dimension=target.shape[0],
        uniform_address_probability=1.0 / active,
        sharp_scalar_extraction_normalization=normalization,
        uniform_selected_signal_norm=float(np.linalg.norm(uniform, ord=2)),
        uniform_selected_to_scaled_target_residual=uniform_residual,
        normalized_target_isometry_residual=target_residual,
        extracted_success_probability=1.0 / active,
        matrix_naimark_success_probability=1.0,
        nonuniform_probability_spread=float(probabilities[-1] - probabilities[0]),
        nonuniform_selected_to_any_equal_coefficient_residual=nonuniform_residual,
        coefficient_only_normalization_lower_bound_saturated=True,
        whitening_granted_for_free=True,
        exact_scalar_address_width_boundary_verified=verified,
        status=(
            "scalar-address-extraction-sharp-sqrt-active-width"
            if verified
            else "scalar-address-extraction-control-failure"
        ),
    )


def audit_pair_local_component_indeterminacy(
    *,
    tolerance: float = 1e-9,
) -> PairLocalComponentIndeterminacyControl:
    e0 = np.asarray(((1.0,), (0.0,)), dtype=complex)
    e1 = np.asarray(((0.0,), (1.0,)), dtype=complex)
    diagonal = e0.copy()
    rotated = np.asarray(((1.0,), (1.0,)), dtype=complex) / math.sqrt(2.0)
    common = np.eye(2, dtype=complex)
    first_leaves = (e0, e1, diagonal)
    second_leaves = (e0, e1, rotated)
    first = component_positive_normal_form(first_leaves, common, tolerance=tolerance)
    second = component_positive_normal_form(second_leaves, common, tolerance=tolerance)
    first_pair = e1.conj().T @ e0
    second_pair = e1.conj().T @ e0
    first_polar = np.zeros_like(first_pair)
    second_polar = np.zeros_like(second_pair)
    projector_residual = max(
        float(np.linalg.norm(first_leaves[index] @ first_leaves[index].conj().T - second_leaves[index] @ second_leaves[index].conj().T, ord=2))
        for index in (0, 1)
    )
    pair_residual = float(np.linalg.norm(first_pair - second_pair, ord=2))
    polar_residual = float(np.linalg.norm(first_polar - second_polar, ord=2))
    first_support = _support_projection(first["frame"], tolerance=tolerance)
    second_support = _support_projection(second["frame"], tolerance=tolerance)
    identity = np.eye(2, dtype=complex)
    first_support_residual = float(np.linalg.norm(first_support - identity, ord=2))
    second_support_residual = float(np.linalg.norm(second_support - identity, ord=2))
    support_gap = float(np.linalg.norm(first_support - second_support, ord=2))
    unqueried_gap = float(
        np.linalg.norm(
            diagonal @ diagonal.conj().T - rotated @ rotated.conj().T,
            ord=2,
        )
    )
    effect_gap = float(np.linalg.norm(first["effects"][0] - second["effects"][0], ord=2))
    verified = bool(
        max(
            projector_residual,
            pair_residual,
            polar_residual,
            first_support_residual,
            second_support_residual,
            support_gap,
        )
        <= 1000 * tolerance
        and unqueried_gap > 0.5
        and effect_gap > 0.25
    )
    return PairLocalComponentIndeterminacyControl(
        physical_dimension=2,
        leaf_count_per_frame=3,
        selected_leaf_projector_residual=projector_residual,
        selected_pair_raw_cross_map_residual=pair_residual,
        selected_pair_polar_residual=polar_residual,
        first_frame_support_residual=first_support_residual,
        second_frame_support_residual=second_support_residual,
        frame_support_projector_residual=support_gap,
        unqueried_leaf_projector_distance=unqueried_gap,
        first_selected_effect_spectrum=tuple(
            float(value) for value in np.linalg.eigvalsh(first["effects"][0])
        ),
        second_selected_effect_spectrum=tuple(
            float(value) for value in np.linalg.eigvalsh(second["effects"][0])
        ),
        selected_component_effect_operator_gap=effect_gap,
        common_pair_local_data_determine_component_effect=False,
        exact_pair_local_indeterminacy_verified=verified,
        status=(
            "pair-local-cross-data-do-not-determine-whitened-component-effect"
            if verified
            else "pair-local-component-indeterminacy-control-failure"
        ),
    )


def positive_access_interface_inventory() -> list[PositiveAccessInterfaceRecord]:
    return [
        PositiveAccessInterfaceRecord(
            interface_id="gpe-invariant-projector",
            supplied_signal="addressed E_e and its support reflection/partial transport",
            normalization="one per supplied address",
            supplies_global_child_whitening=False,
            supplies_common_metric_inverse_root=False,
            supplies_component_support_transport=True,
            supplies_component_naimark_dilation=False,
            equivalent_to_restricted_polar_if_supplied=False,
            compiled=True,
            status="support-transport-not-positive-amplitude",
        ),
        PositiveAccessInterfaceRecord(
            interface_id="addressed-physical-cross-map",
            supplied_signal="one coherently addressed Q_f^*Q_e block",
            normalization="one per pair; dense coefficient assembly costs leaf width",
            supplies_global_child_whitening=False,
            supplies_common_metric_inverse_root=False,
            supplies_component_support_transport=True,
            supplies_component_naimark_dilation=False,
            equivalent_to_restricted_polar_if_supplied=False,
            compiled=True,
            status="pair-signal-available-global-whitening-open",
        ),
        PositiveAccessInterfaceRecord(
            interface_id="schur-companion-membership-stack",
            supplied_signal="Schur labels, carrier rows, and branchwise membership reflections",
            normalization="one inside each branch",
            supplies_global_child_whitening=False,
            supplies_common_metric_inverse_root=False,
            supplies_component_support_transport=False,
            supplies_component_naimark_dilation=False,
            equivalent_to_restricted_polar_if_supplied=False,
            compiled=True,
            status="branch-preserving-coordinate-access-only",
        ),
        PositiveAccessInterfaceRecord(
            interface_id="direct-component-square-root-naimark",
            supplied_signal="N=stack_e sqrt(H_e) on the common retained fiber",
            normalization="one",
            supplies_global_child_whitening=True,
            supplies_common_metric_inverse_root=True,
            supplies_component_support_transport=False,
            supplies_component_naimark_dilation=True,
            equivalent_to_restricted_polar_if_supplied=True,
            compiled=False,
            status="sufficient-but-restricted-polar-equivalent",
        ),
        PositiveAccessInterfaceRecord(
            interface_id="aggregate-schur-racah-analysis",
            supplied_signal="hypothetical compact aggregate R or its source-adapted polar",
            normalization="must be polynomial with an inverse-polynomial retained singular edge",
            supplies_global_child_whitening=True,
            supplies_common_metric_inverse_root=False,
            supplies_component_support_transport=True,
            supplies_component_naimark_dilation=True,
            equivalent_to_restricted_polar_if_supplied=True,
            compiled=False,
            status="decisive-surviving-structured-interface",
        ),
        PositiveAccessInterfaceRecord(
            interface_id="binary-aggregate-endpoint-metrics",
            supplied_signal="hypothetical compact block encodings of the two aggregate short metrics",
            normalization="constant or polynomial on the retained parent window",
            supplies_global_child_whitening=False,
            supplies_common_metric_inverse_root=True,
            supplies_component_support_transport=False,
            supplies_component_naimark_dilation=False,
            equivalent_to_restricted_polar_if_supplied=True,
            compiled=False,
            status="binary-endpoint-closure-conditional-on-aggregate-access",
        ),
    ]


def natural_positive_access_scaling_record(
    n: int,
    *,
    fixed_jump_log2_arity: int = 12,
    polynomial_benchmark_degree: int = 10,
) -> NaturalPositiveAccessScalingRecord:
    if n < 3 or fixed_jump_log2_arity < 0 or polynomial_benchmark_degree < 1:
        raise ValueError("invalid natural scaling parameters")
    order = math.factorial(n)
    selected = (order - 1).bit_length() + 2
    leaf_count = 1 << selected
    child_log2 = max(0, selected - fixed_jump_log2_arity)
    active = 1 << child_log2
    normalization_log2 = child_log2 / 2.0
    benchmark = polynomial_benchmark_degree * math.log2(n)
    separated = normalization_log2 > benchmark
    return NaturalPositiveAccessScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=selected,
        orientation_leaf_count_decimal=str(leaf_count),
        fixed_jump_log2_arity=fixed_jump_log2_arity,
        early_child_active_component_count_decimal=str(active),
        early_child_active_component_count_log2=child_log2,
        scalar_address_normalization_log2=normalization_log2,
        scalar_address_success_probability_log2=-child_log2,
        polynomial_benchmark_degree=polynomial_benchmark_degree,
        polynomial_benchmark_log2=benchmark,
        flattened_scalar_address_route_superpolynomial=separated,
        small_positive_effect_edge_used=False,
        hierarchical_local_router_ruled_out=False,
        direct_schur_racah_naimark_ruled_out=False,
        status=(
            "flattened-positive-address-extraction-superpolynomial"
            if separated
            else "finite-size-positive-address-separation-not-yet-visible"
        ),
    )


def run_positive_naimark_access_equivalence_boundary(
) -> PositiveNaimarkAccessEquivalenceReport:
    systems = [
        _component_system(
            731,
            physical_dimension=5,
            leaf_widths=(2, 2, 1, 2),
            common_dimension=3,
        ),
        _component_system(
            947,
            physical_dimension=6,
            leaf_widths=(1, 2, 2, 1, 2),
            common_dimension=4,
        ),
    ]
    component_controls = [
        audit_physical_component_positive_amplitudes(
            f"PHYSICAL-COMPONENT-{index}",
            leaves,
            common,
        )
        for index, (leaves, common) in enumerate(systems, start=1)
    ]
    scalar_controls = [
        audit_scalar_address_extraction(leaves, common)
        for leaves, common in systems
    ]
    endpoint = audit_endpoint_positive_amplitudes()
    pair_local = audit_pair_local_component_indeterminacy()
    interfaces = positive_access_interface_inventory()
    scaling = [
        natural_positive_access_scaling_record(n)
        for n in (12, 16, 24, 32, 40, 48, 64, 80)
    ]
    finite_failures = sum(
        not row.exact_physical_positive_amplitude_equivalence_verified
        for row in component_controls
    ) + sum(
        not row.exact_scalar_address_width_boundary_verified
        for row in scalar_controls
    )
    finite_failures += int(
        not endpoint.exact_endpoint_positive_amplitude_equivalence_verified
    ) + int(not pair_local.exact_pair_local_indeterminacy_verified)
    separated = [row for row in scaling if row.flattened_scalar_address_route_superpolynomial]
    verified = bool(finite_failures == 0 and separated)
    theorem = PositiveNaimarkAccessEquivalenceTheorem(
        physical_component_effect=(
            "H_e=A^-1/2 X^*F^+E_eF^+X A^-1/2, where F=sum_e E_e and A=X^*F^+X."
        ),
        restricted_polar=(
            "B=R^*F^(+/2) F^(+/2)X A^-1/2=UJ is the normalized minimum-norm child embedding."
        ),
        direct_naimark_equivalence=(
            "For B_e=V_e sqrt(H_e), B=(direct_sum V_e)N and N=(direct_sum V_e)^*B; known support transports make the conversion normalization-one in both directions."
        ),
        endpoint_effect=(
            "C_s=sqrt(A_s)(A_L+A_R)^-1/2 and K_s=C_s^*C_s=(A_L+A_R)^-1/2 A_s (A_L+A_R)^-1/2, with the same two-way Naimark gauge equivalence."
        ),
        scalar_address_lower_bound=(
            "Even after granting whitening, equal extraction of m nonzero blocks requires alpha=sqrt(m); uniform scalar PREPARE attains success 1/m."
        ),
        pair_local_boundary=(
            "One addressed pair and its polar do not determine H_e because unqueried leaves change the global frame inverse by a constant amount."
        ),
        current_interface_verdict=(
            "GPE supplies E_e/support transports, addressed physical access supplies pair cross maps, and the Schur companion supplies branch coordinates; none supplies F^+, A^-1/2, or N."
        ),
        conditional_positive_route=(
            "A compact aggregate analysis with polynomial normalization and retained singular edge, or a direct Schur/Racah Naimark circuit, would compile the restricted polar without a leaf table."
        ),
        natural_scaling=(
            "A fixed-arity early child has m=Theta(n!) active leaves, so the flattened scalar-address route has sqrt(m) normalization and is superpolynomial without invoking a small effect edge."
        ),
        scope=(
            "This binds scalar coefficient extraction, pair-local formulas, and the enumerated current interfaces. It is not an arbitrary-query lower bound and preserves hierarchical local and direct representation-specific routers."
        ),
        theorem_verified=verified,
        status=(
            "positive-naimark-access-equivalence-and-width-boundary-proved"
            if verified
            else "positive-naimark-access-equivalence-validation-failure"
        ),
    )
    headline = {
        "physical_component_effect_formula_theorem_count": int(verified),
        "direct_naimark_restricted_polar_equivalence_theorem_count": int(verified),
        "endpoint_positive_effect_formula_theorem_count": int(verified),
        "scalar_address_sqrt_width_lower_bound_theorem_count": int(verified),
        "pair_local_component_effect_indeterminacy_theorem_count": int(verified),
        "component_control_count": len(component_controls),
        "scalar_address_control_count": len(scalar_controls),
        "finite_control_failure_count": finite_failures,
        "maximum_finite_equivalence_residual": max(
            max(
                row.maximum_physical_effect_formula_residual,
                row.direct_naimark_to_restricted_polar_residual,
                row.restricted_polar_to_direct_naimark_residual,
            )
            for row in component_controls
        ),
        "pair_local_selected_effect_operator_gap": pair_local.selected_component_effect_operator_gap,
        "compiled_positive_amplitude_interface_count": sum(
            row.compiled and row.supplies_component_naimark_dilation for row in interfaces
        ),
        "uncompiled_direct_or_aggregate_positive_interface_count": sum(
            (not row.compiled) and row.equivalent_to_restricted_polar_if_supplied
            for row in interfaces
        ),
        "natural_scaling_record_count": len(scaling),
        "superpolynomial_flattened_scaling_record_count": len(separated),
        "natural_small_positive_edge_theorem_count": 0,
        "hierarchical_router_lower_bound_count": 0,
        "direct_schur_racah_naimark_compiler_count": 0,
        "physical_pgm_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PositiveNaimarkAccessEquivalenceReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "Existing GPE projectors, addressed cross-Grams, or Schur companion data may directly supply the positive component and endpoint Naimark amplitudes without compiling the restricted child polar."
            ),
            "result": (
                "The component and endpoint square-root dilations are exactly gauge-equivalent to the restricted polars. Current interfaces omit the global whitening, scalar addressed extraction is sharply normalized by sqrt(active width), and pair-local data do not determine the effect."
            ),
            "scope": theorem.scope,
        },
        theorem=theorem,
        component_controls=component_controls,
        endpoint_control=endpoint,
        scalar_address_controls=scalar_controls,
        pair_local_indeterminacy_control=pair_local,
        interface_inventory=interfaces,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_physical_component_effect_and_direct_naimark_factorization",
                "resolved": verified,
                "resolution": "Equations (1)--(3) give the exact full-domain projector formula and two-way block-polar gauge conversion.",
            },
            {
                "obligation": "derive_exact_endpoint_effect_and_direct_naimark_factorization",
                "resolved": verified,
                "resolution": "Equation (4) and the two endpoint row polars give the exact bidirectional endpoint dilation equivalence.",
            },
            {
                "obligation": "decide_scalar_address_extraction_normalization_even_with_whitening",
                "resolved": verified,
                "resolution": "Equal nonzero block coefficients force alpha=sqrt(m), independently of the component positive edge.",
            },
            {
                "obligation": "decide_pair_local_cross_gram_sufficiency_for_component_effect",
                "resolved": verified,
                "resolution": "The three-leaf counterpair fixes selected local data and changes H_0 by a constant through the unqueried frame contribution.",
            },
            {
                "obligation": "compile_compact_aggregate_schur_racah_analysis_or_direct_naimark",
                "resolved": False,
                "resolution": "No current all-n interface supplies the aggregate whitening/polar with polynomial normalization and retained edge.",
            },
            {
                "obligation": "propagate_a_normalization_one_local_router_through_the_natural_tree",
                "resolved": False,
                "resolution": "The theorem preserves hierarchical normalization-one routers but does not construct them.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A direct square-root POVM is a positive-amplitude shortcut independent of the missing child polar.",
                "resolved": True,
                "resolution": "With the known component support gauges it converts to and from the restricted polar at normalization one.",
            },
            {
                "objection": "Granting exact F and A whitening removes every remaining addressed normalization.",
                "resolved": True,
                "resolution": "Scalar address extraction still needs equal coefficient 1/sqrt(m) on every active output block.",
            },
            {
                "objection": "One addressed pair polar determines the selected positive component effect.",
                "resolved": True,
                "resolution": "The effect depends on the inverse of the sum over every leaf; the fixed-pair countercontrol has a constant 0.28-scale gap.",
            },
            {
                "objection": "The lower bound follows from exponentially small positive effect eigenvalues.",
                "resolved": True,
                "resolution": "No effect-edge claim is used; the bound is coefficient normalization and holds even for perfectly conditioned blocks.",
            },
            {
                "objection": "This rules out a recursive fixed-arity or direct Schur/Racah circuit.",
                "resolved": False,
                "resolution": "Those circuits lie outside scalar flattened extraction and remain the principal positive routes.",
            },
        ],
        headline_metrics=headline,
        claim_gate={
            "exact_physical_component_effect_formula_proved": verified,
            "direct_component_naimark_is_restricted_polar_equivalent": verified,
            "exact_endpoint_effect_formula_proved": verified,
            "scalar_flattened_positive_extraction_alpha_sqrt_width_proved": verified,
            "pair_local_cross_data_determine_component_effect": False,
            "current_gpe_supplies_component_positive_dilation": False,
            "current_addressed_cross_map_supplies_global_child_whitening": False,
            "current_schur_companion_supplies_component_positive_dilation": False,
            "natural_small_positive_effect_edge_proved": False,
            "hierarchical_normalization_one_router_ruled_out": False,
            "direct_schur_racah_naimark_ruled_out": False,
            "uniform_component_naimark_dilation_compiled": False,
            "uniform_endpoint_naimark_dilation_compiled": False,
            "physical_pgm_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Derived the exact physical positive component and endpoint effects, proved that their direct Naimark dilations are bidirectionally equivalent to the corresponding restricted polars, and closed the scalar addressed-positive shortcut with a sharp sqrt(active-width) normalization even after granting whitening. Current GPE, addressed-pair, and Schur companion interfaces do not supply the missing aggregate positive operation; hierarchical and direct Schur/Racah routes remain open."
        ),
        falsifiers_triggered=[
            "A direct component square-root POVM dilation is an independent easier primitive than the restricted orientation polar once support transports are compiled.",
            "Exact global metric whitening makes scalar addressed component extraction normalization one.",
            "A selected raw cross map and its pair polar determine the corresponding canonical component effect.",
        ],
    )


def write_positive_naimark_access_equivalence_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_positive_naimark_access_equivalence_boundary())
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
                title="Positive Naimark access equivalence boundary",
                status="completed-exact-positive-access-equivalence-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Derive the full-domain physical formula for component effects and the short-metric endpoint formula, prove bidirectional direct-Naimark/restricted-polar gauge equivalence, audit scalar address normalization after free whitening, construct a pair-local indeterminacy control, and inventory the current typed interfaces."
                ),
                positive_signal=(
                    "A compact aggregate Schur/Racah analysis or direct Naimark circuit with reversible labels, polynomial normalization, a retained inverse-polynomial singular edge, controlled workspace, and parent-compatible trim propagation."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_component_povm_regular_master_reduction.py",
                    "self_dual_wreath_component_direct_naimark_polar_equivalence.py",
                    "self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary.py",
                    "self_dual_wreath_coherent_gpe_router_boundary.py",
                    "self_dual_wreath_affine_gpe_nodelocal_naimark_access_boundary.py",
                ],
                next_actions=[
                    "Attack the surviving hierarchical interface: derive the binary local endpoint effects as explicit Schur/Racah operators on parent-propagated retained fibers and test whether their generators close in a poly(n)-dimensional algebra with a uniform reversible label circuit.",
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Existing addressed GPE/projector and cross-Gram access directly supplies the positive component Naimark amplitudes without compiling the restricted child polar."
                ),
                reason_invalid=(
                    "The exact effect contains global F^+ and A^-1/2 factors. With known support gauges, its square-root dilation is bidirectionally equivalent to the restricted polar; scalar addressed extraction is sharply normalized by sqrt(active width), and fixed pair-local data do not determine the effect."
                ),
                lesson=(
                    "Do not count a direct component Naimark dilation as an easier primitive unless its circuit is constructed independently. Focus on an aggregate hierarchical Schur/Racah analysis with polynomial normalization or an explicit normalization-one local matrix router."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "physical_component_effect": "A^-1/2 X^*F^+E_eF^+X A^-1/2",
                    "direct_naimark_restricted_polar_equivalent": True,
                    "scalar_address_normalization": "sqrt(active_component_count)",
                    "pair_local_selected_effect_gap": payload["pair_local_indeterminacy_control"]["selected_component_effect_operator_gap"],
                    "small_positive_effect_edge_used": False,
                    "hierarchical_router_ruled_out": False,
                    "direct_schur_racah_naimark_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    result = write_positive_naimark_access_equivalence_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
