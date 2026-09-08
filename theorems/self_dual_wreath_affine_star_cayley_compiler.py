"""Normalization-one Cayley compiler for label-resolved affine-star channels.

The physical global-channel extractor finds flat scalar carrier channels whose
orientation graph is a star on an affine support.  For a balanced sibling
split, write ``p`` for the number of vertices in each child, place the star
center in the left child, and let ``gamma`` be the scalar carrier overlap.
After quotienting the left-internal star edges, the crossing-edge effects are

    E_R = I,
    E_L = (1-gamma) I + gamma q J_p,
    q = (2-gamma) / (2(1-gamma)+p gamma).                 (1)

The canonical Cayley contraction therefore has only two Walsh eigenvalues,

    d_perp = -gamma/(2-gamma),
    d_0    = (t_p-1)/(t_p+1),
    t_p    = 1-gamma+p gamma q.                           (2)

Thus

    D = d_perp (I-|u><u|) + d_0 |u><u|,                  (3)

where ``|u>`` is the uniform crossing-edge state.  Walsh transform, one
all-zero predicate, and two branch rotations implement both a normalization-
one block encoding of ``D`` and the exact binary Naimark column.  There is no
QSVT degree or amplitude-amplification cost when ``gamma`` is supplied as a
coherent classical carrier label.

There is an exact commuting operator-valued extension.  Replace ``gamma`` by
one Hermitian contraction ``Gamma`` shared by every edge.  Equations (1)-(3)
become matrix functions of ``Gamma`` on the uniform and orthogonal address
sectors.  This observation does *not* make a generic QSVT compiler efficient.
The uniform-sector eigenvalue changes by a constant between ``Gamma=0`` and
``Gamma=I/p``.  Markov's polynomial inequality therefore forces degree
``Omega(sqrt(p))`` for a spectrum-only polynomial uniformly covering
``[0,1/2]``.  An explicit carrier label can bypass this edge; an opaque matrix
fiber cannot.

A merged two-center graph has more than the two Walsh eigenvalues in (2), so
the same one-predicate compiler fails by constant operator norm.  The theorem
is consequently a real normalized oracle for label-resolved scalar stars, not
an all-depth natural-channel classifier or a matrix-Racah compiler.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_star_channel_gap import affine_star_graph
from self_dual_wreath_global_carrier_channel_extractor import (
    run_global_carrier_channel_extractor,
)
from self_dual_wreath_graded_channel_graph_reduction import (
    child_endpoint_effects,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_affine_star_cayley_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CAYLEY-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ScalarAffineStarCompilerControl:
    side_width: int
    address_qubit_count: int
    correlation: float
    orthogonal_cayley_eigenvalue: float
    uniform_cayley_eigenvalue: float
    cayley_contraction_norm: float
    endpoint_gap: float
    walsh_hadamard_gate_count: int
    all_zero_predicate_count: int
    branch_rotation_count: int
    block_encoding_normalization: float
    dense_graph_cayley_residual: float
    signal_block_encoding_residual: float
    signal_unitarity_residual: float
    naimark_isometry_residual: float
    left_branch_effect_residual: float
    right_branch_effect_residual: float
    exact_label_resolved_compiler_verified: bool
    status: str


@dataclass(frozen=True)
class OperatorAffineStarControl:
    side_width: int
    address_qubit_count: int
    fiber_dimension: int
    gamma_eigenvalues: tuple[float, ...]
    minimum_denominator_eigenvalue: float
    cayley_contraction_norm: float
    endpoint_gap: float
    functional_cayley_residual: float
    address_sector_commutator_residual: float
    naimark_isometry_residual: float
    operator_functional_reduction_verified: bool
    normalized_gamma_block_encoding_assumed: bool
    coherent_gamma_eigenlabel_supplied: bool
    uniform_polylogarithmic_qsvt_degree_proved: bool
    status: str


@dataclass(frozen=True)
class SpectrumOnlyDegreeBoundary:
    side_width: int
    address_qubit_count: int
    requested_uniform_error: float
    zero_eigenvalue_target: float
    inverse_width_eigenvalue_target: float
    target_jump: float
    markov_degree_lower_bound: int
    degree_lower_bound_over_sqrt_width: float
    polynomial_in_address_bits: bool
    exact_carrier_label_bypasses_uniform_polynomial: bool
    status: str


@dataclass(frozen=True)
class ExtractedPhysicalStarCompilerSummary:
    physical_control_count: int
    extracted_channel_count: int
    affine_star_channel_count: int
    distinct_correlations: tuple[float, ...]
    distinct_coefficient_multiplicities: tuple[int, ...]
    maximum_predicted_defect_residual: float
    every_extracted_channel_is_label_resolved_scalar_star: bool
    finite_physical_compiler_coverage_verified: bool
    status: str


@dataclass(frozen=True)
class MergedCenterCounterexample:
    side_width: int
    crossing_edge_count: int
    correlation: float
    cayley_eigenvalues: tuple[float, ...]
    distinct_cayley_eigenvalue_count: int
    uniform_address_projector_commutator_norm: float
    best_uniform_vs_orthogonal_fit_residual: float
    endpoint_gap: float
    one_predicate_affine_star_compiler_applies: bool
    counterexample_verified: bool
    status: str


@dataclass(frozen=True)
class AffineStarCayleyCompilerTheorem:
    scalar_normal_form: str
    direct_signal_compiler: str
    direct_naimark_compiler: str
    commuting_operator_extension: str
    spectrum_only_degree_boundary: str
    physical_scope: str
    surviving_target: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AffineStarCayleyCompilerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: AffineStarCayleyCompilerTheorem
    scalar_controls: list[ScalarAffineStarCompilerControl]
    operator_controls: list[OperatorAffineStarControl]
    degree_boundaries: list[SpectrumOnlyDegreeBoundary]
    physical_summary: ExtractedPhysicalStarCompilerSummary
    merged_center_counterexample: MergedCenterCounterexample
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2


def _positive_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float = 1e-12,
) -> np.ndarray:
    matrix = _hermitian(np.asarray(matrix, dtype=complex))
    values, vectors = np.linalg.eigh(matrix)
    if len(values) and values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    powered = np.zeros_like(values)
    keep = values > tolerance
    if exponent < 0 and not np.all(keep):
        raise ValueError("negative powers require positive definiteness")
    powered[keep] = values[keep] ** exponent
    return _hermitian((vectors * powered) @ vectors.conj().T)


def _require_power_of_two(value: int) -> int:
    if value < 2 or value & (value - 1):
        raise ValueError("side width must be a power of two at least two")
    return value.bit_length() - 1


@lru_cache(maxsize=32)
def walsh_matrix(size: int) -> np.ndarray:
    """Return the normalized XOR Walsh matrix on ``log2(size)`` qubits."""

    bits = _require_power_of_two(size)
    matrix = np.ones((1, 1))
    for _ in range(bits):
        matrix = np.block([[matrix, matrix], [matrix, -matrix]]) / math.sqrt(2)
    return matrix


def scalar_affine_star_cayley_values(
    side_width: int,
    correlation: float,
) -> tuple[float, float, float]:
    """Return ``(d_perp, d_uniform, endpoint_gap)`` from (1)-(2)."""

    _require_power_of_two(side_width)
    if not 0 < correlation <= 0.5:
        raise ValueError("correlation must lie in (0, 1/2]")
    denominator = 2 * (1 - correlation) + side_width * correlation
    q = (2 - correlation) / denominator
    constant_effect = 1 - correlation + side_width * correlation * q
    orthogonal = -correlation / (2 - correlation)
    uniform = (constant_effect - 1) / (constant_effect + 1)
    defect = max(abs(orthogonal), abs(uniform))
    return orthogonal, uniform, (1 - defect) / 2


def scalar_affine_star_cayley_matrix(
    side_width: int,
    correlation: float,
) -> np.ndarray:
    orthogonal, uniform, _gap = scalar_affine_star_cayley_values(
        side_width,
        correlation,
    )
    ones = np.ones((side_width, 1)) / math.sqrt(side_width)
    projector = ones @ ones.T
    return _hermitian(
        orthogonal * (np.eye(side_width) - projector) + uniform * projector
    )


def scalar_affine_star_signal_block_encoding(
    side_width: int,
    correlation: float,
) -> np.ndarray:
    """Return an exact normalization-one signal unitary for the scalar ``D``."""

    orthogonal, uniform, _gap = scalar_affine_star_cayley_values(
        side_width,
        correlation,
    )
    values = np.asarray([uniform] + [orthogonal] * (side_width - 1))
    diagonal = np.diag(values)
    complement = np.diag(np.sqrt(1 - values**2))
    signal = np.block(
        [[diagonal, complement], [complement, -diagonal]]
    )
    walsh = walsh_matrix(side_width)
    conjugator = np.block(
        [
            [walsh, np.zeros_like(walsh)],
            [np.zeros_like(walsh), walsh],
        ]
    )
    return conjugator @ signal @ conjugator


def scalar_affine_star_naimark(
    side_width: int,
    correlation: float,
) -> np.ndarray:
    """Return the exact branch-address Naimark column for the scalar star."""

    orthogonal, uniform, _gap = scalar_affine_star_cayley_values(
        side_width,
        correlation,
    )
    values = np.asarray([uniform] + [orthogonal] * (side_width - 1))
    walsh = walsh_matrix(side_width)
    left = walsh @ np.diag(np.sqrt((1 + values) / 2)) @ walsh
    right = walsh @ np.diag(np.sqrt((1 - values) / 2)) @ walsh
    return np.vstack((left, right))


def audit_scalar_affine_star_compiler(
    side_width: int,
    correlation: float,
    *,
    tolerance: float = 1e-9,
) -> ScalarAffineStarCompilerControl:
    address_bits = _require_power_of_two(side_width)
    vertices, edges, left_vertices = affine_star_graph(side_width)
    left, right, _counts = child_endpoint_effects(
        vertices,
        edges,
        left_vertices,
        correlation,
    )
    metric = left + right
    inverse_root = _positive_power(metric, -0.5)
    dense_cayley = _hermitian(inverse_root @ (left - right) @ inverse_root)
    predicted = scalar_affine_star_cayley_matrix(side_width, correlation)
    signal = scalar_affine_star_signal_block_encoding(side_width, correlation)
    naimark = scalar_affine_star_naimark(side_width, correlation)
    identity = np.eye(side_width)
    left_effect = _hermitian(inverse_root @ left @ inverse_root)
    right_effect = _hermitian(inverse_root @ right @ inverse_root)
    encoded = signal[:side_width, :side_width]
    orthogonal, uniform, gap = scalar_affine_star_cayley_values(
        side_width,
        correlation,
    )
    residuals = {
        "dense": float(np.linalg.norm(dense_cayley - predicted, ord=2)),
        "block": float(np.linalg.norm(encoded - predicted, ord=2)),
        "unitary": float(
            np.linalg.norm(signal.conj().T @ signal - np.eye(2 * side_width), ord=2)
        ),
        "naimark": float(
            np.linalg.norm(naimark.conj().T @ naimark - identity, ord=2)
        ),
        "left": float(
            np.linalg.norm(
                naimark[:side_width].conj().T @ naimark[:side_width]
                - left_effect,
                ord=2,
            )
        ),
        "right": float(
            np.linalg.norm(
                naimark[side_width:].conj().T @ naimark[side_width:]
                - right_effect,
                ord=2,
            )
        ),
    }
    verified = max(residuals.values()) <= 100 * tolerance
    return ScalarAffineStarCompilerControl(
        side_width=side_width,
        address_qubit_count=address_bits,
        correlation=correlation,
        orthogonal_cayley_eigenvalue=orthogonal,
        uniform_cayley_eigenvalue=uniform,
        cayley_contraction_norm=max(abs(orthogonal), abs(uniform)),
        endpoint_gap=gap,
        walsh_hadamard_gate_count=2 * address_bits,
        all_zero_predicate_count=1,
        branch_rotation_count=2,
        block_encoding_normalization=1.0,
        dense_graph_cayley_residual=residuals["dense"],
        signal_block_encoding_residual=residuals["block"],
        signal_unitarity_residual=residuals["unitary"],
        naimark_isometry_residual=residuals["naimark"],
        left_branch_effect_residual=residuals["left"],
        right_branch_effect_residual=residuals["right"],
        exact_label_resolved_compiler_verified=verified,
        status=(
            "normalization-one-label-resolved-affine-star-compiler-verified"
            if verified
            else "affine-star-cayley-compiler-validation-failure"
        ),
    )


def operator_affine_star_data(
    side_width: int,
    gamma_operator: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> dict[str, np.ndarray | float]:
    """Return the exact commuting operator-valued extension of (1)-(3)."""

    _require_power_of_two(side_width)
    gamma = _hermitian(np.asarray(gamma_operator, dtype=complex))
    if gamma.ndim != 2 or gamma.shape[0] != gamma.shape[1]:
        raise ValueError("gamma operator must be square")
    gamma_values = np.linalg.eigvalsh(gamma)
    if gamma_values[0] < -100 * tolerance or gamma_values[-1] > 0.5 + 100 * tolerance:
        raise ValueError("gamma spectrum must lie in [0,1/2]")
    dimension = gamma.shape[0]
    identity_fiber = np.eye(dimension, dtype=complex)
    denominator = 2 * (identity_fiber - gamma) + side_width * gamma
    q = (2 * identity_fiber - gamma) @ np.linalg.inv(denominator)
    constant_effect = (
        identity_fiber
        - gamma
        + side_width * gamma @ q
    )
    orthogonal = -gamma @ np.linalg.inv(2 * identity_fiber - gamma)
    uniform = (
        (constant_effect - identity_fiber)
        @ np.linalg.inv(constant_effect + identity_fiber)
    )
    uniform_address = np.ones((side_width, 1)) / math.sqrt(side_width)
    projector = uniform_address @ uniform_address.T
    predicted = _hermitian(
        np.kron(np.eye(side_width) - projector, orthogonal)
        + np.kron(projector, uniform)
    )
    left = _hermitian(
        np.kron(np.eye(side_width), identity_fiber - gamma)
        + np.kron(np.ones((side_width, side_width)), gamma @ q)
    )
    right = np.eye(side_width * dimension, dtype=complex)
    metric = left + right
    inverse_root = _positive_power(metric, -0.5)
    direct = _hermitian(inverse_root @ (left - right) @ inverse_root)
    naimark = np.vstack(
        (
            _positive_power((np.eye(direct.shape[0]) + predicted) / 2, 0.5),
            _positive_power((np.eye(direct.shape[0]) - predicted) / 2, 0.5),
        )
    )
    return {
        "gamma": gamma,
        "denominator": denominator,
        "orthogonal": orthogonal,
        "uniform": uniform,
        "predicted_cayley": predicted,
        "direct_cayley": direct,
        "naimark": naimark,
        "uniform_projector": np.kron(projector, identity_fiber),
    }


def audit_operator_affine_star(
    side_width: int,
    gamma_operator: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> OperatorAffineStarControl:
    data = operator_affine_star_data(side_width, gamma_operator)
    gamma = np.asarray(data["gamma"])
    direct = np.asarray(data["direct_cayley"])
    predicted = np.asarray(data["predicted_cayley"])
    naimark = np.asarray(data["naimark"])
    projector = np.asarray(data["uniform_projector"])
    residual = float(np.linalg.norm(direct - predicted, ord=2))
    commutator = float(np.linalg.norm(direct @ projector - projector @ direct, ord=2))
    isometry = float(
        np.linalg.norm(naimark.conj().T @ naimark - np.eye(direct.shape[0]), ord=2)
    )
    defect = float(np.linalg.norm(predicted, ord=2))
    verified = max(residual, commutator, isometry) <= 100 * tolerance
    return OperatorAffineStarControl(
        side_width=side_width,
        address_qubit_count=_require_power_of_two(side_width),
        fiber_dimension=gamma.shape[0],
        gamma_eigenvalues=tuple(
            round(float(value), 12) for value in np.linalg.eigvalsh(gamma)
        ),
        minimum_denominator_eigenvalue=float(
            np.linalg.eigvalsh(np.asarray(data["denominator"])).min()
        ),
        cayley_contraction_norm=defect,
        endpoint_gap=(1 - defect) / 2,
        functional_cayley_residual=residual,
        address_sector_commutator_residual=commutator,
        naimark_isometry_residual=isometry,
        operator_functional_reduction_verified=verified,
        normalized_gamma_block_encoding_assumed=True,
        coherent_gamma_eigenlabel_supplied=False,
        uniform_polylogarithmic_qsvt_degree_proved=False,
        status=(
            "operator-affine-star-functional-reduction-verified-degree-open"
            if verified
            else "operator-affine-star-functional-reduction-failure"
        ),
    )


def spectrum_only_degree_boundary(
    side_width: int,
    requested_error: float = 1 / 64,
) -> SpectrumOnlyDegreeBoundary:
    """Apply Markov's inequality to the uniform-sector Cayley function."""

    bits = _require_power_of_two(side_width)
    if not 0 < requested_error < 1 / 16:
        raise ValueError("requested error must lie in (0,1/16)")
    zero = 0.0
    _orthogonal, inverse_width, _gap = scalar_affine_star_cayley_values(
        side_width,
        1 / side_width,
    )
    jump = abs(inverse_width - zero)
    effective = jump - 2 * requested_error
    if effective <= 0:
        raise ValueError("error is too large to certify a degree boundary")
    # On [0,1/2], Markov gives ||P'|| <= 4 degree^2 ||P||.  A QSVT
    # polynomial has ||P|| <= 1, while the mean-value theorem gives a
    # derivative at least p(jump-2 epsilon).
    lower = math.ceil(math.sqrt(side_width * effective / 4))
    return SpectrumOnlyDegreeBoundary(
        side_width=side_width,
        address_qubit_count=bits,
        requested_uniform_error=requested_error,
        zero_eigenvalue_target=zero,
        inverse_width_eigenvalue_target=inverse_width,
        target_jump=jump,
        markov_degree_lower_bound=lower,
        degree_lower_bound_over_sqrt_width=lower / math.sqrt(side_width),
        polynomial_in_address_bits=False,
        exact_carrier_label_bypasses_uniform_polynomial=True,
        status="spectrum-only-affine-star-qsvt-degree-omega-sqrt-width",
    )


def _is_star(edges: tuple[tuple[int, int], ...]) -> bool:
    vertices = sorted({vertex for edge in edges for vertex in edge})
    degrees = {
        vertex: sum(vertex in edge for edge in edges) for vertex in vertices
    }
    return bool(
        len(vertices) >= 3
        and len(edges) == len(vertices) - 1
        and sorted(degrees.values()) == [1] * (len(vertices) - 1) + [len(vertices) - 1]
    )


@lru_cache(maxsize=1)
def audit_extracted_physical_stars() -> ExtractedPhysicalStarCompilerSummary:
    extraction = run_global_carrier_channel_extractor()
    channels = [channel for control in extraction.controls for channel in control.channels]
    star_channels = [channel for channel in channels if _is_star(channel.edge_support)]
    residuals = []
    correlations = []
    multiplicities = []
    for control in extraction.controls:
        correlations.append(control.residual_correlation)
        for channel in control.channels:
            multiplicities.append(channel.coefficient_multiplicity)
            side_width = len(channel.orientation_support) // 2
            _orthogonal, _uniform, gap = scalar_affine_star_cayley_values(
                side_width,
                control.residual_correlation,
            )
            residuals.append(
                abs(channel.maximum_grading_defect_norm - (1 - 2 * gap))
            )
    scalar_stars = bool(
        channels
        and len(star_channels) == len(channels)
        and all(channel.orientation_support_is_affine for channel in channels)
    )
    verified = bool(
        extraction.claim_gate["physical_global_channel_extractor_verified"]
        and scalar_stars
        and max(residuals, default=0.0) <= 1e-8
    )
    return ExtractedPhysicalStarCompilerSummary(
        physical_control_count=len(extraction.controls),
        extracted_channel_count=len(channels),
        affine_star_channel_count=len(star_channels),
        distinct_correlations=tuple(
            sorted({round(float(value), 12) for value in correlations})
        ),
        distinct_coefficient_multiplicities=tuple(sorted(set(multiplicities))),
        maximum_predicted_defect_residual=max(residuals, default=0.0),
        every_extracted_channel_is_label_resolved_scalar_star=scalar_stars,
        finite_physical_compiler_coverage_verified=verified,
        status=(
            "all-extracted-w6-scalar-stars-covered-by-normalized-compiler"
            if verified
            else "extracted-physical-star-compiler-coverage-failure"
        ),
    )


def merged_center_counterexample(
    correlation: float = 1 / 5,
    *,
    tolerance: float = 1e-9,
) -> MergedCenterCounterexample:
    """Return a scalar two-center graph outside the one-predicate star form."""

    vertices = tuple(range(8))
    left_vertices = (0, 1, 2, 3)
    edges = ((0, 1), (0, 4), (0, 5), (1, 6), (1, 7))
    left, right, counts = child_endpoint_effects(
        vertices,
        edges,
        left_vertices,
        correlation,
    )
    inverse_root = _positive_power(left + right, -0.5)
    cayley = _hermitian(inverse_root @ (left - right) @ inverse_root)
    values = np.linalg.eigvalsh(cayley)
    dimension = cayley.shape[0]
    uniform = np.ones((dimension, 1)) / math.sqrt(dimension)
    projector = uniform @ uniform.T
    orthogonal_scalar = float(
        np.trace((np.eye(dimension) - projector) @ cayley).real / (dimension - 1)
    )
    uniform_scalar = float(np.trace(projector @ cayley).real)
    fit = (
        orthogonal_scalar * (np.eye(dimension) - projector)
        + uniform_scalar * projector
    )
    fit_residual = float(np.linalg.norm(cayley - fit, ord=2))
    commutator = float(np.linalg.norm(cayley @ projector - projector @ cayley, ord=2))
    distinct = tuple(sorted({round(float(value), 10) for value in values}))
    defect = float(np.max(np.abs(values)))
    verified = bool(
        counts["crossing_edge_count"] == 4
        and len(distinct) > 2
        and fit_residual > 1e-2
        and commutator <= 100 * tolerance
    )
    return MergedCenterCounterexample(
        side_width=4,
        crossing_edge_count=counts["crossing_edge_count"],
        correlation=correlation,
        cayley_eigenvalues=tuple(round(float(value), 12) for value in values),
        distinct_cayley_eigenvalue_count=len(distinct),
        uniform_address_projector_commutator_norm=commutator,
        best_uniform_vs_orthogonal_fit_residual=fit_residual,
        endpoint_gap=(1 - defect) / 2,
        one_predicate_affine_star_compiler_applies=False,
        counterexample_verified=verified,
        status="merged-two-center-channel-rejects-one-predicate-star-compiler",
    )


@lru_cache(maxsize=1)
def run_affine_star_cayley_compiler() -> AffineStarCayleyCompilerReport:
    scalar = [
        audit_scalar_affine_star_compiler(width, gamma)
        for width in (2, 4, 8, 16)
        for gamma in (1 / 5, 1 / 9, 1 / 10)
    ]
    angle = 0.43
    rotation = np.asarray(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
    )
    operator = [
        audit_operator_affine_star(
            4,
            rotation @ np.diag((0.05, 0.31)) @ rotation.T,
        ),
        audit_operator_affine_star(
            8,
            np.asarray(
                [
                    [0.18, 0.04j, 0.0],
                    [-0.04j, 0.27, 0.03],
                    [0.0, 0.03, 0.11],
                ],
                dtype=complex,
            ),
        ),
    ]
    degrees = [
        spectrum_only_degree_boundary(1 << bits)
        for bits in (4, 8, 12, 16, 20)
    ]
    physical = audit_extracted_physical_stars()
    merged = merged_center_counterexample()
    failures = sum(not row.exact_label_resolved_compiler_verified for row in scalar)
    failures += sum(not row.operator_functional_reduction_verified for row in operator)
    verified = bool(
        failures == 0
        and physical.finite_physical_compiler_coverage_verified
        and merged.counterexample_verified
        and degrees[-1].markov_degree_lower_bound
        > degrees[0].markov_degree_lower_bound
    )
    theorem = AffineStarCayleyCompilerTheorem(
        scalar_normal_form=(
            "A flat scalar affine star has D=d_perp(I-|u><u|)+d_0|u><u| "
            "with the two rational eigenvalues in equations (1)-(2)."
        ),
        direct_signal_compiler=(
            "Walsh conjugation and one all-zero-controlled signal rotation "
            "give a normalization-one block encoding of D."
        ),
        direct_naimark_compiler=(
            "Two label-computed branch rotations give sqrt((I+D)/2) and "
            "sqrt((I-D)/2) directly, without QSVT or width amplification."
        ),
        commuting_operator_extension=(
            "A shared Hermitian edge operator Gamma yields the same address-sector "
            "decomposition with matrix rational functions of Gamma."
        ),
        spectrum_only_degree_boundary=(
            "Without a Gamma eigenlabel, uniform polynomial access over [0,1/2] "
            "requires degree Omega(sqrt(p)) by Markov's inequality."
        ),
        physical_scope=(
            "The compiler covers every scalar affine-star channel in the current "
            "W6 global extraction, conditional on coherent channel/carrier labels."
        ),
        surviving_target=(
            "Prove an all-depth label-resolved star decomposition or compile the "
            "noncommuting matrix-valued Racah fibers without spectrum-only inversion."
        ),
        theorem_verified=verified,
        status=(
            "label-resolved-affine-star-cayley-compiler-proved"
            if verified
            else "affine-star-cayley-compiler-validation-failure"
        ),
    )
    return AffineStarCayleyCompilerReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "A balanced power-of-two affine-star channel, its coherent scalar "
                "carrier overlap label, and the crossing-edge address register."
            ),
            "exact_output": (
                "A normalization-one canonical-D block encoding and exact binary "
                "Cayley Naimark column."
            ),
            "operator_extension": (
                "Exact algebra for one commuting Gamma shared by all star edges; "
                "efficient compilation still needs eigenlabels or a favorable spectrum."
            ),
            "excluded_claims": (
                "No all-depth star classification, coherent natural carrier labeler, "
                "noncommuting Racah compiler, root anchor, PGM, decoder, or speedup."
            ),
        },
        theorem=theorem,
        scalar_controls=scalar,
        operator_controls=operator,
        degree_boundaries=degrees,
        physical_summary=physical,
        merged_center_counterexample=merged,
        proof_obligations=[
            {
                "obligation": "compile_label_resolved_scalar_affine_star_cayley_at_normalization_one",
                "resolved": verified,
                "resolution": (
                    "The exact two-Walsh-eigenvalue form gives both signal and "
                    "branch rotations with one address predicate."
                ),
            },
            {
                "obligation": "cover_current_physical_extracted_channels",
                "resolved": physical.finite_physical_compiler_coverage_verified,
                "resolution": (
                    "All eight channels from seven physical W6 controls are scalar "
                    "affine stars and reproduce the predicted Cayley defect."
                ),
            },
            {
                "obligation": "compile_opaque_operator_gamma_by_uniform_polylog_qsvt",
                "resolved": False,
                "resolution": (
                    "The uniform-sector function changes by a constant over width "
                    "1/p, forcing QSVT polynomial degree Omega(sqrt(p))."
                ),
            },
            {
                "obligation": "prove_natural_channels_remain_label_resolved_stars_all_depth",
                "resolved": False,
                "resolution": (
                    "Higher multiplicity may merge centers or create noncommuting "
                    "matrix fibers; the finite W6 extraction cannot exclude either."
                ),
            },
            {
                "obligation": "anchor_root_and_transfer_parent_native_mass",
                "resolved": False,
                "resolution": (
                    "The local endpoint compiler still requires the physical root "
                    "coordinate map and an all-depth retained-mass recurrence."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Normalization-one D still requires generic QSVT for scalar stars.",
                "resolved": True,
                "resolution": (
                    "False with a carrier label: compute two angles and apply one "
                    "Walsh-sector predicate."
                ),
            },
            {
                "objection": "The commuting matrix formula automatically gives a polylogarithmic compiler.",
                "resolved": True,
                "resolution": (
                    "False without eigenlabels: Markov's inequality exposes an "
                    "Omega(sqrt(p)) spectrum-only degree edge."
                ),
            },
            {
                "objection": "Any sparse affine channel uses the same two-angle compiler.",
                "resolved": True,
                "resolution": (
                    "The merged two-center scalar graph has more than two distinct Cayley eigenvalues "
                    "and constant residual from the one-predicate ansatz."
                ),
            },
            {
                "objection": "Finite physical coverage proves the natural all-depth oracle.",
                "resolved": False,
                "resolution": (
                    "The controls do not include growing Kronecker multiplicity or "
                    "a coherent channel-label extraction circuit."
                ),
            },
        ],
        headline_metrics={
            "normalization_one_scalar_star_cayley_compiler_count": int(verified),
            "direct_scalar_star_naimark_compiler_count": int(verified),
            "commuting_operator_star_functional_reduction_count": int(verified),
            "spectrum_only_qsvt_sqrt_width_degree_lower_bound_count": int(verified),
            "finite_scalar_control_count": len(scalar),
            "finite_operator_control_count": len(operator),
            "finite_control_failure_count": failures,
            "physical_w6_control_count": physical.physical_control_count,
            "physical_w6_channel_count": physical.extracted_channel_count,
            "physical_w6_compiler_covered_channel_count": physical.affine_star_channel_count,
            "maximum_physical_defect_residual": physical.maximum_predicted_defect_residual,
            "tail_side_width": degrees[-1].side_width,
            "tail_markov_degree_lower_bound": degrees[-1].markov_degree_lower_bound,
            "merged_center_star_fit_residual": merged.best_uniform_vs_orthogonal_fit_residual,
            "natural_all_depth_channel_classification_count": 0,
            "coherent_natural_carrier_labeler_count": 0,
            "noncommuting_matrix_racah_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "label_resolved_scalar_affine_star_cayley_compiled_at_normalization_one": verified,
            "label_resolved_scalar_affine_star_naimark_compiled_directly": verified,
            "all_current_extracted_w6_channels_covered": physical.finite_physical_compiler_coverage_verified,
            "commuting_operator_affine_star_formula_proved": verified,
            "opaque_operator_gamma_has_uniform_polylog_qsvt_compiler": False,
            "one_predicate_compiler_covers_merged_center_channels": False,
            "natural_all_depth_channels_classified": False,
            "coherent_natural_channel_and_carrier_labels_compiled": False,
            "noncommuting_matrix_valued_channels_compiled": False,
            "physical_root_anchor_compiled": False,
            "all_depth_parent_native_mass_recurrence_proved": False,
            "physical_pgm_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The canonical D access bottleneck is solved exactly for the finite "
                "physically observed label-resolved scalar-star family. Natural "
                "all-depth channel classification, coherent labels, matrix-valued "
                "Racah fibers, root anchoring, and mass propagation remain open."
            ),
        },
        status=(
            "label-resolved-affine-star-normalized-cayley-compiler-proved-"
            "natural-matrix-channel-boundary-open"
            if verified
            else "affine-star-cayley-compiler-validation-failure"
        ),
        summary=(
            "Compiled canonical D and its binary Naimark endpoint at normalization "
            "one for label-resolved scalar affine stars, covering all eight current "
            "physical W6 channels. The operator-valued formula is exact, but an "
            "Omega(sqrt(width)) spectrum-only degree boundary and a merged-center "
            "counterexample isolate the missing coherent labels and matrix-Racah law."
        ),
        falsifiers_triggered=[
            "Generic QSVT is unnecessary for a scalar affine star once its carrier overlap is coherently labeled.",
            "Normalization one does not imply low degree for an opaque operator-valued overlap spectrum.",
            "Affine orientation support does not make a one-center compiler universal across sparse channel graphs.",
            "Finite W6 coverage is not an all-depth natural-channel theorem.",
        ],
    )


def write_affine_star_cayley_compiler_report(
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
    payload = asdict(run_affine_star_cayley_compiler(**kwargs))
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
                title="Label-resolved affine-star Cayley compiler",
                status="completed-exact-scoped-normalized-compiler",
                hypothesis=(
                    "Physical scalar affine-star channels admit a direct "
                    "normalization-one canonical-D and Naimark compiler."
                ),
                protocol=(
                    "Derive the Walsh-sector formulas, compare against dense graph "
                    "Schur quotients, audit operator fibers, and attack scope with "
                    "polynomial-degree and merged-center counterexamples."
                ),
                positive_signal=(
                    "Exact branch effects and signal blocks at normalization one for "
                    "every scalar control and every extracted physical W6 channel."
                ),
                falsifiers=[
                    "dense graph Cayley differs from the two-sector formula",
                    "the direct Naimark column changes a branch effect",
                    "an opaque Gamma spectrum has polylogarithmic uniform degree",
                    "a merged-center channel still has only two Cayley eigenvalues",
                ],
                metrics=[
                    "signal_block_encoding_residual",
                    "branch_effect_residual",
                    "physical_channel_coverage",
                    "markov_degree_lower_bound",
                    "merged_center_fit_residual",
                ],
                dependencies=[
                    "global physical carrier-channel extractor",
                    "affine-star graded-gap theorem",
                    "canonical Cayley endpoint theorem",
                ],
                next_actions=[
                    "derive an all-depth coherent scalar-star channel labeler",
                    "classify or falsify merged centers at growing multiplicity",
                    "compile noncommuting matrix-valued Racah fibers",
                    "anchor the physical root coordinate and propagate native mass",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CAYLEY-COMPILER-LATEST"
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
                    "self_dual_wreath_affine_star_cayley_compiler": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="OPAQUE-AFFINE-STAR-GAMMA-QSVT-NOT-POLYLOG-WIDTH",
                source=registry_experiment_id,
                claim=(
                    "The commuting operator-valued affine-star formula gives a "
                    "uniform polylogarithmic-degree spectrum-only QSVT compiler."
                ),
                reason_invalid=(
                    "The uniform-sector Cayley eigenvalue changes by a constant "
                    "between gamma=0 and gamma=1/p; Markov's inequality forces "
                    "degree Omega(sqrt(p))."
                ),
                lesson=(
                    "Use coherent carrier labels and reversible angle arithmetic, "
                    "or derive additional spectral promises. Normalization one alone "
                    "does not remove polynomial degree."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence={
                    "tail_side_width": payload["headline_metrics"]["tail_side_width"],
                    "tail_markov_degree_lower_bound": payload["headline_metrics"][
                        "tail_markov_degree_lower_bound"
                    ],
                    "merged_center_fit_residual": payload["headline_metrics"][
                        "merged_center_star_fit_residual"
                    ],
                },
            )
        )
    return payload


if __name__ == "__main__":
    result = write_affine_star_cayley_compiler_report()
    print(json.dumps(result["headline_metrics"], indent=2))
    print(result["status"])
