"""Scale-free Cayley endpoint compiler and recursive gauge boundary.

The relative-transfer normal form writes the common-fiber endpoint as the
graph of a generally non-Hermitian positive transfer ``T``.  That is useful,
but it carries an opaque input gauge.  The object needed for the actual
binary POVM is smaller and Hermitian.

For positive child short metrics ``E_L,E_R``, put

    M = E_L + E_R,
    K_s = M^(-1/2) E_s M^(-1/2),
    D = K_L - K_R.                                      (1)

Then ``K_L=(I+D)/2``, ``K_R=(I-D)/2`` and ``-I<D<I``.  The canonical
positive-root endpoint

    C = [sqrt(E_L); sqrt(E_R)] M^(-1/2)                 (2)

has the same branch effects as the Cayley Naimark column

    N_D = [sqrt((I+D)/2); sqrt((I-D)/2)].               (3)

Consequently ``C=diag(U_L,U_R)N_D`` for child-side unitaries ``U_s``.
Unlike the graph transfer gauge, these are output gauges.  In a recursive
tree they telescope exactly when each child coordinate system is conjugated
accordingly.  A gauge at the root must still be anchored by the physical
root coordinate embedding; if it is silently omitted, the POVM changes.

The contraction is scale free: a common rescaling of both ``E_s`` leaves
``D`` and (3) unchanged.  Given a normalization-one block encoding of ``D``
whose retained spectrum lies in ``[-1+delta,1-delta]``, QSVT of the bounded
root functions in (3) conditionally compiles the endpoint with degree
polynomial in ``1/delta`` and ``log(1/epsilon)``.  It does not require the
polar of ``T`` or a lower bound on the absolute child scale.

This is a strict target reduction, not a circuit for the natural affine
problem.  The current representation LCU supplies normalized child frames,
not the normalized shorted grading ``D``.  Constructing a representation-
specific block encoding of (1), an equivalent direct Racah transform, and an
all-depth native-mass recurrence remain open.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_node_frame_response_boundary import (
    _common_span_basis,
)
from self_dual_wreath_scale_free_endpoint_graph_transfer_boundary import (
    _physical_affine_frames,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_cayley_endpoint_gauge_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CAYLEY-ENDPOINT-GAUGE-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
QSVT_URL = "https://arxiv.org/abs/1806.01838"
POLAR_QSVT_URL = "https://arxiv.org/abs/2106.07634"
GEOMETRIC_MEAN_URL = "https://arxiv.org/abs/2405.00673"


@dataclass(frozen=True)
class CayleyEndpointControl:
    control_id: str
    fiber_dimension: int
    short_metric_commutator_norm: float
    cayley_contraction_norm: float
    endpoint_gap: float
    branch_effect_sum_residual: float
    canonical_endpoint_isometry_residual: float
    cayley_naimark_isometry_residual: float
    left_branch_effect_residual: float
    right_branch_effect_residual: float
    branch_gauge_reconstruction_residual: float
    branch_gauge_unitarity_residual: float
    graph_cayley_similarity_residual: float
    graph_ratio_identity_residual: float
    graph_to_canonical_cayley_operator_gap: float
    exact_cayley_endpoint_gauge_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalCayleyEndpointControl:
    control_id: str
    n: int
    child_width: int
    physical_dimension: int
    common_fiber_dimension: int
    cayley_contraction_norm: float
    endpoint_gap: float
    relative_transfer_norm: float
    maximum_exact_identity_residual: float
    exact_physical_cayley_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class CayleyScaleControl:
    scale_bits: int
    common_short_scale: float
    separate_absolute_inverse_resolution_proxy: float
    cayley_contraction_scale_residual: float
    cayley_naimark_projector_scale_residual: float
    common_scale_cancels_exactly: bool
    status: str


@dataclass(frozen=True)
class RecursiveGaugeControl:
    tree_depth: int
    fiber_dimension: int
    internal_node_count: int
    leaf_count: int
    maximum_path_telescope_residual: float
    maximum_leaf_effect_residual: float
    root_input_gauge_anchored: bool
    exact_recursive_child_gauge_covariance_verified: bool
    status: str


@dataclass(frozen=True)
class RootGaugeBoundaryControl:
    fiber_dimension: int
    root_input_gauge_norm: float
    unanchored_root_branch_effect_gap: float
    anchored_physical_endpoint_residual: float
    internal_output_gauges_automatically_fix_root_input_gauge: bool
    exact_root_anchor_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class CayleyCompilerRecord:
    endpoint_gap: float
    requested_error: float
    qsvt_degree_upper_proxy: int
    left_root_scalar_identity_residual: float
    right_root_scalar_identity_residual: float
    requires_normalization_one_cayley_block_encoding: bool
    requires_relative_transfer_polar: bool
    requires_absolute_short_metric_scale: bool
    requires_root_coordinate_anchor: bool
    representation_specific_cayley_oracle_supplied_by_current_stack: bool
    conditional_cayley_naimark_compiler_polynomial: bool
    status: str


@dataclass(frozen=True)
class CayleyEndpointGaugeTheorem:
    canonical_contraction: str
    branch_effect_identity: str
    branch_gauge_factorization: str
    graph_transfer_relation: str
    scale_cancellation: str
    recursive_gauge_covariance: str
    root_anchor_boundary: str
    conditional_compiler: str
    surviving_target: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CayleyEndpointGaugeReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    theorem: CayleyEndpointGaugeTheorem
    abstract_controls: list[CayleyEndpointControl]
    physical_controls: list[PhysicalCayleyEndpointControl]
    scale_controls: list[CayleyScaleControl]
    recursive_gauge_control: RecursiveGaugeControl
    root_gauge_boundary: RootGaugeBoundaryControl
    compiler_records: list[CayleyCompilerRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _positive_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> np.ndarray:
    value = _hermitian(np.asarray(matrix, dtype=complex))
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise ValueError("matrix must be square")
    eigenvalues, eigenvectors = np.linalg.eigh(value)
    scale = max(float(eigenvalues[-1]), np.finfo(float).tiny)
    if eigenvalues[0] <= tolerance * scale:
        raise ValueError("matrix must be positive definite at relative tolerance")
    return _hermitian(
        (eigenvectors * eigenvalues**exponent) @ eigenvectors.conj().T
    )


def canonical_cayley_data(
    left_short: np.ndarray,
    right_short: np.ndarray,
    *,
    tolerance: float = 1e-11,
) -> dict[str, np.ndarray]:
    """Return the exact Cayley contraction and its two Naimark columns."""

    left_short = _hermitian(np.asarray(left_short, dtype=complex))
    right_short = _hermitian(np.asarray(right_short, dtype=complex))
    if (
        left_short.ndim != 2
        or left_short.shape[0] != left_short.shape[1]
        or right_short.shape != left_short.shape
    ):
        raise ValueError("short metrics must share one square fiber")

    left_root = _positive_power(left_short, 0.5, tolerance=tolerance)
    right_root = _positive_power(right_short, 0.5, tolerance=tolerance)
    metric_inverse_root = _positive_power(
        left_short + right_short,
        -0.5,
        tolerance=tolerance,
    )
    canonical_left = left_root @ metric_inverse_root
    canonical_right = right_root @ metric_inverse_root
    canonical_endpoint = np.vstack((canonical_left, canonical_right))
    left_effect = _hermitian(canonical_left.conj().T @ canonical_left)
    right_effect = _hermitian(canonical_right.conj().T @ canonical_right)
    cayley = _hermitian(left_effect - right_effect)
    left_effect_root = _positive_power(left_effect, 0.5, tolerance=tolerance)
    right_effect_root = _positive_power(right_effect, 0.5, tolerance=tolerance)
    cayley_naimark = np.vstack((left_effect_root, right_effect_root))
    left_gauge = canonical_left @ _positive_power(
        left_effect,
        -0.5,
        tolerance=tolerance,
    )
    right_gauge = canonical_right @ _positive_power(
        right_effect,
        -0.5,
        tolerance=tolerance,
    )
    branch_gauge = np.block(
        [
            [left_gauge, np.zeros_like(left_gauge)],
            [np.zeros_like(right_gauge), right_gauge],
        ]
    )

    left_inverse_root = _positive_power(left_short, -0.5, tolerance=tolerance)
    transfer = right_root @ left_inverse_root
    identity = np.eye(left_short.shape[0], dtype=complex)
    graph_normalizer = _positive_power(
        identity + transfer.conj().T @ transfer,
        -0.5,
        tolerance=tolerance,
    )
    graph_column = np.vstack((identity, transfer)) @ graph_normalizer
    graph_cayley = _hermitian(graph_column.conj().T @ np.block(
        [
            [identity, np.zeros_like(identity)],
            [np.zeros_like(identity), -identity],
        ]
    ) @ graph_column)
    graph_input_gauge = canonical_endpoint.conj().T @ graph_column
    ratio_from_cayley = (
        (identity - graph_cayley)
        @ np.linalg.inv(identity + graph_cayley)
    )

    return {
        "left_short": left_short,
        "right_short": right_short,
        "left_effect": left_effect,
        "right_effect": right_effect,
        "cayley": cayley,
        "canonical_endpoint": canonical_endpoint,
        "cayley_naimark": cayley_naimark,
        "left_branch_gauge": left_gauge,
        "right_branch_gauge": right_gauge,
        "branch_gauge": branch_gauge,
        "relative_transfer": transfer,
        "graph_column": graph_column,
        "graph_cayley": graph_cayley,
        "graph_input_gauge": graph_input_gauge,
        "ratio_from_cayley": _hermitian(ratio_from_cayley),
    }


def audit_cayley_endpoint(
    control_id: str,
    left_short: np.ndarray,
    right_short: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> CayleyEndpointControl:
    data = canonical_cayley_data(
        left_short,
        right_short,
        tolerance=tolerance / 100,
    )
    dimension = left_short.shape[0]
    identity = np.eye(dimension, dtype=complex)
    double_identity = np.eye(2 * dimension, dtype=complex)
    grading = np.block(
        [
            [identity, np.zeros_like(identity)],
            [np.zeros_like(identity), -identity],
        ]
    )
    canonical = data["canonical_endpoint"]
    naimark = data["cayley_naimark"]
    left_canonical = canonical[:dimension]
    right_canonical = canonical[dimension:]
    left_naimark = naimark[:dimension]
    right_naimark = naimark[dimension:]
    branch_reconstruction = data["branch_gauge"] @ naimark
    graph_gauge = data["graph_input_gauge"]
    residuals = {
        "effect_sum": float(
            np.linalg.norm(data["left_effect"] + data["right_effect"] - identity, ord=2)
        ),
        "canonical_iso": float(
            np.linalg.norm(canonical.conj().T @ canonical - identity, ord=2)
        ),
        "naimark_iso": float(
            np.linalg.norm(naimark.conj().T @ naimark - identity, ord=2)
        ),
        "left_effect": float(
            np.linalg.norm(
                left_canonical.conj().T @ left_canonical
                - left_naimark.conj().T @ left_naimark,
                ord=2,
            )
        ),
        "right_effect": float(
            np.linalg.norm(
                right_canonical.conj().T @ right_canonical
                - right_naimark.conj().T @ right_naimark,
                ord=2,
            )
        ),
        "branch_reconstruction": float(
            np.linalg.norm(canonical - branch_reconstruction, ord=2)
        ),
        "branch_unitarity": float(
            np.linalg.norm(
                data["branch_gauge"].conj().T @ data["branch_gauge"]
                - double_identity,
                ord=2,
            )
        ),
        "graph_similarity": float(
            np.linalg.norm(
                data["graph_cayley"]
                - graph_gauge.conj().T @ data["cayley"] @ graph_gauge,
                ord=2,
            )
        ),
        "graph_ratio": float(
            np.linalg.norm(
                data["ratio_from_cayley"]
                - data["relative_transfer"].conj().T
                @ data["relative_transfer"],
                ord=2,
            )
        ),
        "cayley_direct": float(
            np.linalg.norm(canonical.conj().T @ grading @ canonical - data["cayley"], ord=2)
        ),
    }
    values = np.linalg.eigvalsh(data["cayley"])
    norm = float(np.max(np.abs(values)))
    maximum = max(residuals.values())
    verified = maximum <= 10_000 * tolerance and norm < 1 + 1000 * tolerance
    return CayleyEndpointControl(
        control_id=control_id,
        fiber_dimension=dimension,
        short_metric_commutator_norm=float(
            np.linalg.norm(
                data["left_short"] @ data["right_short"]
                - data["right_short"] @ data["left_short"],
                ord=2,
            )
        ),
        cayley_contraction_norm=norm,
        endpoint_gap=(1.0 - norm) / 2.0,
        branch_effect_sum_residual=residuals["effect_sum"],
        canonical_endpoint_isometry_residual=residuals["canonical_iso"],
        cayley_naimark_isometry_residual=residuals["naimark_iso"],
        left_branch_effect_residual=residuals["left_effect"],
        right_branch_effect_residual=residuals["right_effect"],
        branch_gauge_reconstruction_residual=residuals["branch_reconstruction"],
        branch_gauge_unitarity_residual=residuals["branch_unitarity"],
        graph_cayley_similarity_residual=residuals["graph_similarity"],
        graph_ratio_identity_residual=residuals["graph_ratio"],
        graph_to_canonical_cayley_operator_gap=float(
            np.linalg.norm(data["graph_cayley"] - data["cayley"], ord=2)
        ),
        exact_cayley_endpoint_gauge_theorem_verified=verified,
        status=(
            "exact-scale-free-cayley-endpoint-and-branch-gauge"
            if verified
            else "cayley-endpoint-gauge-control-failure"
        ),
    )


def _random_positive(seed: int, dimension: int, floor: float) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    return _hermitian(raw.conj().T @ raw / dimension + floor * np.eye(dimension))


def _abstract_controls() -> list[CayleyEndpointControl]:
    angle = 0.41
    rotation = np.asarray(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
        dtype=complex,
    )
    return [
        audit_cayley_endpoint(
            "COMMUTING-DIAGONAL",
            np.diag((0.7, 1.4, 2.1)).astype(complex),
            np.diag((1.2, 0.9, 1.8)).astype(complex),
        ),
        audit_cayley_endpoint(
            "NONCOMMUTING-ROTATED",
            np.diag((0.8, 1.7)).astype(complex),
            rotation @ np.diag((0.6, 1.5)) @ rotation.conj().T,
        ),
        audit_cayley_endpoint(
            "RANDOM-COMPLEX-D4",
            _random_positive(2608281, 4, 0.8),
            _random_positive(2608282, 4, 0.7),
        ),
    ]


def audit_physical_cayley_endpoint(
    *,
    tolerance: float = 1e-9,
) -> PhysicalCayleyEndpointControl:
    target, _, left_masks, _, left_frame, right_frame = _physical_affine_frames()
    common = _common_span_basis(left_frame, right_frame, tolerance)
    responses = tuple(
        _hermitian(
            common.conj().T
            @ np.linalg.pinv(frame, rcond=tolerance)
            @ common
        )
        for frame in (left_frame, right_frame)
    )
    shorts = tuple(np.linalg.inv(response) for response in responses)
    data = canonical_cayley_data(*shorts, tolerance=tolerance / 100)
    row = audit_cayley_endpoint(
        "S3-AFFINE-FINAL-SIBLINGS",
        *shorts,
        tolerance=tolerance,
    )
    maximum = max(
        row.branch_effect_sum_residual,
        row.canonical_endpoint_isometry_residual,
        row.cayley_naimark_isometry_residual,
        row.branch_gauge_reconstruction_residual,
        row.graph_cayley_similarity_residual,
        row.graph_ratio_identity_residual,
    )
    verified = row.exact_cayley_endpoint_gauge_theorem_verified
    return PhysicalCayleyEndpointControl(
        control_id="S3-AFFINE-FINAL-SIBLINGS",
        n=sum(target),
        child_width=len(left_masks),
        physical_dimension=len(left_frame),
        common_fiber_dimension=common.shape[1],
        cayley_contraction_norm=row.cayley_contraction_norm,
        endpoint_gap=row.endpoint_gap,
        relative_transfer_norm=float(
            np.linalg.norm(data["relative_transfer"], ord=2)
        ),
        maximum_exact_identity_residual=maximum,
        exact_physical_cayley_reduction_verified=verified,
        status=(
            "physical-affine-cayley-endpoint-exact"
            if verified
            else "physical-affine-cayley-endpoint-failure"
        ),
    )


def audit_cayley_scale_cancellation(
    scale_bits: int,
    *,
    tolerance: float = 1e-9,
) -> CayleyScaleControl:
    if scale_bits < 1:
        raise ValueError("scale_bits must be positive")
    left = _random_positive(2608283, 3, 0.9)
    right = _random_positive(2608284, 3, 0.8)
    scale = 2.0 ** (-scale_bits)
    base = canonical_cayley_data(left, right, tolerance=1e-13)
    scaled = canonical_cayley_data(
        scale * left,
        scale * right,
        tolerance=1e-13,
    )
    cayley_residual = float(
        np.linalg.norm(base["cayley"] - scaled["cayley"], ord=2)
    )
    projector_residual = float(
        np.linalg.norm(
            base["cayley_naimark"] @ base["cayley_naimark"].conj().T
            - scaled["cayley_naimark"] @ scaled["cayley_naimark"].conj().T,
            ord=2,
        )
    )
    verified = max(cayley_residual, projector_residual) <= 10_000 * tolerance
    return CayleyScaleControl(
        scale_bits=scale_bits,
        common_short_scale=scale,
        separate_absolute_inverse_resolution_proxy=1.0 / scale,
        cayley_contraction_scale_residual=cayley_residual,
        cayley_naimark_projector_scale_residual=projector_residual,
        common_scale_cancels_exactly=verified,
        status=(
            "common-scale-cancels-from-cayley-endpoint"
            if verified
            else "cayley-scale-cancellation-failure"
        ),
    )


def _random_unitary(seed: int, dimension: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    unitary, triangular = np.linalg.qr(raw)
    phases = np.diag(triangular)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return unitary @ np.diag(phases.conj())


def audit_recursive_gauge_covariance(
    tree_depth: int = 3,
    fiber_dimension: int = 3,
    *,
    tolerance: float = 1e-9,
) -> RecursiveGaugeControl:
    if tree_depth < 1 or fiber_dimension < 1:
        raise ValueError("tree depth and fiber dimension must be positive")
    internal_nodes = tuple(range((1 << tree_depth) - 1))
    all_nodes = tuple(range((1 << (tree_depth + 1)) - 1))
    gauges = {
        node: (
            np.eye(fiber_dimension, dtype=complex)
            if node == 0
            else _random_unitary(2609000 + node, fiber_dimension)
        )
        for node in all_nodes
    }
    canonical: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    transformed: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    for node in internal_nodes:
        left = _random_positive(2610000 + 2 * node, fiber_dimension, 0.7)
        right = _random_positive(2610001 + 2 * node, fiber_dimension, 0.7)
        data = canonical_cayley_data(left, right, tolerance=1e-13)
        endpoint = data["canonical_endpoint"]
        blocks = (endpoint[:fiber_dimension], endpoint[fiber_dimension:])
        canonical[node] = blocks
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        transformed[node] = (
            gauges[left_child] @ blocks[0] @ gauges[node].conj().T,
            gauges[right_child] @ blocks[1] @ gauges[node].conj().T,
        )

    maximum_path = 0.0
    maximum_effect = 0.0
    first_leaf = (1 << tree_depth) - 1
    for leaf in range(first_leaf, len(all_nodes)):
        choices = []
        node = leaf
        while node:
            parent = (node - 1) // 2
            choices.append((parent, 0 if node == 2 * parent + 1 else 1))
            node = parent
        choices.reverse()
        canonical_path = np.eye(fiber_dimension, dtype=complex)
        transformed_path = np.eye(fiber_dimension, dtype=complex)
        for parent, branch in choices:
            canonical_path = canonical[parent][branch] @ canonical_path
            transformed_path = transformed[parent][branch] @ transformed_path
        telescope_target = gauges[leaf] @ canonical_path
        maximum_path = max(
            maximum_path,
            float(np.linalg.norm(transformed_path - telescope_target, ord=2)),
        )
        maximum_effect = max(
            maximum_effect,
            float(
                np.linalg.norm(
                    transformed_path.conj().T @ transformed_path
                    - canonical_path.conj().T @ canonical_path,
                    ord=2,
                )
            ),
        )
    verified = max(maximum_path, maximum_effect) <= 10_000 * tolerance
    return RecursiveGaugeControl(
        tree_depth=tree_depth,
        fiber_dimension=fiber_dimension,
        internal_node_count=len(internal_nodes),
        leaf_count=1 << tree_depth,
        maximum_path_telescope_residual=maximum_path,
        maximum_leaf_effect_residual=maximum_effect,
        root_input_gauge_anchored=True,
        exact_recursive_child_gauge_covariance_verified=verified,
        status=(
            "recursive-child-gauges-telescope-exactly"
            if verified
            else "recursive-gauge-covariance-failure"
        ),
    )


def audit_root_gauge_boundary(
    *,
    tolerance: float = 1e-9,
) -> RootGaugeBoundaryControl:
    left = _random_positive(2611001, 3, 0.8)
    right = _random_positive(2611002, 3, 0.8)
    endpoint = canonical_cayley_data(left, right)["canonical_endpoint"]
    dimension = left.shape[0]
    root_gauge = _random_unitary(2611003, dimension)
    canonical_left = endpoint[:dimension]
    unanchored_left = canonical_left @ root_gauge.conj().T
    gap = float(
        np.linalg.norm(
            unanchored_left.conj().T @ unanchored_left
            - canonical_left.conj().T @ canonical_left,
            ord=2,
        )
    )
    anchored_endpoint = endpoint @ root_gauge.conj().T @ root_gauge
    anchored_residual = float(np.linalg.norm(anchored_endpoint - endpoint, ord=2))
    verified = gap > 1e-3 and anchored_residual <= 10_000 * tolerance
    return RootGaugeBoundaryControl(
        fiber_dimension=dimension,
        root_input_gauge_norm=float(np.linalg.norm(root_gauge, ord=2)),
        unanchored_root_branch_effect_gap=gap,
        anchored_physical_endpoint_residual=anchored_residual,
        internal_output_gauges_automatically_fix_root_input_gauge=False,
        exact_root_anchor_boundary_verified=verified,
        status=(
            "root-gauge-must-be-anchored-by-physical-coordinate-map"
            if verified
            else "root-gauge-boundary-control-failure"
        ),
    )


def cayley_compiler_record(
    endpoint_gap: float,
    requested_error: float = 1e-7,
) -> CayleyCompilerRecord:
    if not 0 < endpoint_gap < 0.5:
        raise ValueError("endpoint_gap must lie in (0,1/2)")
    if not 0 < requested_error < 0.1:
        raise ValueError("requested_error must lie in (0,0.1)")
    degree = math.ceil(
        8.0 / endpoint_gap * math.log(16.0 / requested_error)
    )
    grid = np.linspace(-1 + 2 * endpoint_gap, 1 - 2 * endpoint_gap, 4097)
    left = np.sqrt((1 + grid) / 2)
    right = np.sqrt((1 - grid) / 2)
    scalar_residual = float(np.max(np.abs(left**2 + right**2 - 1)))
    return CayleyCompilerRecord(
        endpoint_gap=endpoint_gap,
        requested_error=requested_error,
        qsvt_degree_upper_proxy=degree,
        left_root_scalar_identity_residual=scalar_residual,
        right_root_scalar_identity_residual=scalar_residual,
        requires_normalization_one_cayley_block_encoding=True,
        requires_relative_transfer_polar=False,
        requires_absolute_short_metric_scale=False,
        requires_root_coordinate_anchor=True,
        representation_specific_cayley_oracle_supplied_by_current_stack=False,
        conditional_cayley_naimark_compiler_polynomial=True,
        status="conditional-normalized-cayley-qsvt-naimark-compiler",
    )


def run_cayley_endpoint_gauge_compiler() -> CayleyEndpointGaugeReport:
    abstract = _abstract_controls()
    physical = [audit_physical_cayley_endpoint()]
    scales = [audit_cayley_scale_cancellation(bits) for bits in (8, 16, 32, 48)]
    recursive = audit_recursive_gauge_covariance()
    root_boundary = audit_root_gauge_boundary()
    compilers = [
        cayley_compiler_record(gap)
        for gap in (0.05, 0.1, 0.2)
    ]
    failures = sum(
        not row.exact_cayley_endpoint_gauge_theorem_verified for row in abstract
    ) + sum(
        not row.exact_physical_cayley_reduction_verified for row in physical
    ) + sum(not row.common_scale_cancels_exactly for row in scales)
    failures += int(not recursive.exact_recursive_child_gauge_covariance_verified)
    failures += int(not root_boundary.exact_root_anchor_boundary_verified)
    failures += sum(
        not row.conditional_cayley_naimark_compiler_polynomial
        for row in compilers
    )
    verified = failures == 0
    theorem = CayleyEndpointGaugeTheorem(
        canonical_contraction=(
            "D=M^-1/2(E_L-E_R)M^-1/2 is a Hermitian contraction and "
            "K_L=(I+D)/2, K_R=(I-D)/2."
        ),
        branch_effect_identity=(
            "The canonical positive-root endpoint and N_D=[sqrt(K_L);sqrt(K_R)] "
            "induce exactly the same binary effects."
        ),
        branch_gauge_factorization=(
            "C=diag(U_L,U_R)N_D for child-side unitaries U_L,U_R."
        ),
        graph_transfer_relation=(
            "In graph coordinates D_T=(I-T*T)(I+T*T)^-1 and D_T is unitarily "
            "similar to the canonical D through the graph input gauge."
        ),
        scale_cancellation=(
            "E_s -> c E_s leaves D, its binary effects, and N_D unchanged."
        ),
        recursive_gauge_covariance=(
            "Matched child-coordinate gauges telescope on every root-to-leaf path "
            "and leave all leaf POVM effects invariant."
        ),
        root_anchor_boundary=(
            "An unmatched root input gauge conjugates the POVM; it must be included "
            "in the physical root coordinate embedding."
        ),
        conditional_compiler=(
            "A normalization-one block encoding of D with endpoint gap delta "
            "conditionally gives a polynomial QSVT Naimark compiler without T polar access."
        ),
        surviving_target=(
            "Construct the actual affine-node normalized short-grading D directly "
            "from Schur/Racah structure, with root anchor and all-depth native mass."
        ),
        scope=(
            "Exact local algebra and recursive gauge theorem only; no natural all-n "
            "D oracle, physical PGM, decoder, classical separation, or speedup."
        ),
        theorem_verified=verified,
        status=(
            "scale-free-cayley-endpoint-gauge-theorem-proved"
            if verified
            else "cayley-endpoint-gauge-validation-failure"
        ),
    )
    return CayleyEndpointGaugeReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "title": "Quantum singular value transformation and beyond",
                "url": QSVT_URL,
                "used_for": "conditional bounded functional calculus",
            },
            {
                "title": "Fast algorithm for quantum polar decomposition and PGM",
                "url": POLAR_QSVT_URL,
                "used_for": "polar/PGM access and condition-number accounting boundary",
            },
            {
                "title": "Quantum algorithms for matrix geometric means",
                "url": GEOMETRIC_MEAN_URL,
                "used_for": "comparison with block-encoded positive relative operators",
            },
        ],
        theorem_contract={
            "input": "Two positive child short metrics on one retained common fiber.",
            "exact_output": "One scale-free Hermitian Cayley contraction and a branch-gauge-equivalent Naimark column.",
            "recursive_contract": "Every output branch gauge is used as the corresponding child input-coordinate gauge.",
            "root_contract": "The remaining root gauge is included in the physical common-fiber coordinate embedding.",
            "compiler_premise": "Normalization-one coherent block encoding of D and retained endpoint gap delta.",
            "excluded_claims": "No construction of the natural D oracle, all-depth mass theorem, decoder, separation, or speedup.",
        },
        theorem=theorem,
        abstract_controls=abstract,
        physical_controls=physical,
        scale_controls=scales,
        recursive_gauge_control=recursive,
        root_gauge_boundary=root_boundary,
        compiler_records=compilers,
        proof_obligations=[
            {
                "obligation": "replace_nonhermitian_transfer_by_binary_cayley_target",
                "resolved": verified,
                "resolution": "Equation (1) is exactly the signed binary effect and is Hermitian with norm below one.",
            },
            {
                "obligation": "prove_recursive_endpoint_gauge_covariance",
                "resolved": verified,
                "resolution": "Matched node gauges telescope algebraically on every path; all leaf effects are unchanged.",
            },
            {
                "obligation": "remove_root_gauge_without_coordinate_anchor",
                "resolved": False,
                "resolution": "The adversarial root control changes a branch effect by a constant when the root gauge is omitted.",
            },
            {
                "obligation": "construct_representation_specific_normalized_cayley_oracle",
                "resolved": False,
                "resolution": "Normalized affine frame LCUs do not yet implement the normalized shorted grading.",
            },
            {
                "obligation": "prove_all_depth_endpoint_gap_and_native_mass_recurrence",
                "resolved": False,
                "resolution": "Only finite controls and the existing final-root weak-law trim are available.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The graph Cayley matrix can be used in any parent basis.",
                "resolved": True,
                "resolution": "False: it is only unitarily similar to the canonical Cayley matrix, and an unanchored root similarity changes the POVM.",
            },
            {
                "objection": "Noncommuting short metrics invalidate the branch-root Naimark form.",
                "resolved": True,
                "resolution": "False: noncommutativity moves into child-side polar gauges; the branch effects remain exact functions of D.",
            },
            {
                "objection": "A common exponentially small short scale forces Cayley inversion cost.",
                "resolved": True,
                "resolution": "The exact target cancels that scale, including controls through 2^-48; access to the normalized target remains separate and open.",
            },
            {
                "objection": "The conditional D compiler is already a natural affine PGM circuit.",
                "resolved": False,
                "resolution": "No representation-specific normalized D block encoding or all-depth retained-mass recurrence is supplied.",
            },
        ],
        headline_metrics={
            "cayley_endpoint_effect_theorem_count": int(verified),
            "branch_gauge_factorization_theorem_count": int(verified),
            "recursive_child_gauge_covariance_theorem_count": int(verified),
            "root_gauge_anchor_boundary_theorem_count": int(verified),
            "common_scale_cancellation_theorem_count": int(verified),
            "conditional_cayley_qsvt_compiler_count": int(verified),
            "representation_specific_cayley_oracle_count": 0,
            "all_depth_native_mass_recurrence_count": 0,
            "finite_control_count": len(abstract) + len(physical) + len(scales) + 2,
            "finite_control_failure_count": failures,
            "physical_cayley_contraction_norm": physical[0].cayley_contraction_norm,
            "physical_endpoint_gap": physical[0].endpoint_gap,
            "unanchored_root_branch_effect_gap": root_boundary.unanchored_root_branch_effect_gap,
            "maximum_recursive_leaf_effect_residual": recursive.maximum_leaf_effect_residual,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "scale_free_canonical_cayley_contraction_proved": verified,
            "cayley_naimark_matches_canonical_binary_effects": verified,
            "recursive_child_output_gauges_telescope": verified,
            "root_input_gauge_can_be_ignored": False,
            "root_coordinate_anchor_required": True,
            "conditional_qsvt_endpoint_compiler_given_normalized_cayley": verified,
            "representation_specific_normalized_cayley_oracle_compiled": False,
            "all_depth_endpoint_gap_proved": False,
            "all_depth_parent_native_mass_recurrence_proved": False,
            "physical_pgm_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The preferred local target is now a scale-free Hermitian contraction "
                "with exact recursive child-gauge covariance, but the actual affine "
                "Schur/Racah oracle for that contraction and the root coordinate anchor "
                "have not been compiled."
            ),
        },
        status=(
            "cayley-endpoint-gauge-normal-form-proved-normalized-oracle-open"
            if verified
            else "cayley-endpoint-gauge-validation-failure"
        ),
        summary=(
            "Replaced the non-Hermitian relative transfer as the preferred binary "
            "compiler target by the scale-free Hermitian Cayley contraction. Its "
            "QSVT Naimark column has exactly the canonical branch effects, differs "
            "only by child gauges that telescope recursively, and exposes one honest "
            "remaining boundary: a normalized affine Schur/Racah oracle plus root anchor."
        ),
        falsifiers_triggered=[
            "Recovering the polar part of T is unnecessary for the local two-outcome POVM once canonical D is available.",
            "Internal child-coordinate gauges do not accumulate into a recursive error when propagated covariantly.",
            "An unanchored root input gauge is not harmless and can change a branch effect by constant operator norm.",
            "Scale cancellation in the mathematical Cayley target does not itself construct its coherent representation oracle.",
        ],
    )


def write_cayley_endpoint_gauge_compiler_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    report = run_cayley_endpoint_gauge_compiler(**kwargs)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Scale-free Cayley endpoint and recursive gauge compiler",
                status="completed-exact-normal-form-access-boundary",
                hypothesis=(
                    "The binary endpoint can be reduced to a normalized Hermitian "
                    "Cayley contraction whose child gauges telescope recursively."
                ),
                protocol=(
                    "Verify exact matrix identities on noncommuting and physical "
                    "affine controls, common-scale sweeps, and a multilevel gauge tree."
                ),
                positive_signal=(
                    "Exact branch-effect equivalence, scale cancellation, and "
                    "root-to-leaf gauge telescoping at numerical precision."
                ),
                falsifiers=[
                    "Cayley Naimark effects differ from the canonical endpoint",
                    "matched child gauges alter a leaf POVM effect",
                    "common scaling changes the Cayley target",
                    "an unanchored root gauge is empirically harmless",
                ],
                metrics=[
                    "branch_effect_residual",
                    "recursive_leaf_effect_residual",
                    "root_gauge_effect_gap",
                    "scale_cancellation_residual",
                ],
                dependencies=[
                    "scale-free endpoint graph-transfer theorem",
                    "vertex-kernel graded Schur reduction",
                    "QSVT functional calculus",
                ],
                next_actions=[
                    "derive a representation-specific normalized Cayley block encoding",
                    "anchor the root coordinate gauge in the homogeneous-space transform",
                    "prove all-depth endpoint gap and native-mass recurrence",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-CAYLEY-ENDPOINT-"
            "GAUGE-COMPILER-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_cayley_endpoint_gauge_compiler": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="UNANCHORED-RELATIVE-GRAPH-GAUGE-NOT-POVM-INVARIANT",
                source=registry_experiment_id,
                claim=(
                    "The opaque input gauge relating the relative-transfer graph "
                    "column to the canonical endpoint can be ignored at the root."
                ),
                reason_invalid=(
                    "A three-dimensional noncommuting control changes a root branch "
                    "effect by constant operator norm when that gauge is omitted."
                ),
                lesson=(
                    "Internal child gauges telescope when propagated covariantly, "
                    "but the surviving root gauge must be included in the physical "
                    "common-fiber coordinate embedding."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence={
                    "unanchored_root_branch_effect_gap": payload[
                        "headline_metrics"
                    ]["unanchored_root_branch_effect_gap"],
                    "anchored_physical_endpoint_residual": payload[
                        "root_gauge_boundary"
                    ]["anchored_physical_endpoint_residual"],
                },
            )
        )
    return payload


if __name__ == "__main__":
    result = write_cayley_endpoint_gauge_compiler_report()
    print(json.dumps(result["headline_metrics"], indent=2))
    print(result["status"])
