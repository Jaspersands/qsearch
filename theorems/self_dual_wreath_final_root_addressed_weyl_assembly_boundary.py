"""Addressed pair access does not remove final-root parent whitening.

Let the two final child analyses be

    R_s:H->K_s,       A_s=R_s^*R_s,       S=A_0+A_1,       s in {0,1}.

After factoring the child polars ``R_s=Q_s sqrt(A_s)``, the final endpoint is
the polar of the stacked positive child map,

    T = [sqrt(A_0);sqrt(A_1)] S^(-1/2).                    (1)

For a logical unitary ``U``, its exact positive-coordinate byproduct has
four child blocks

    (T U T^*)_(s,t)
      = sqrt(A_s) S^(-1/2) U S^(-1/2) sqrt(A_t).           (2)

Put ``C=S^(-1/2)A_0S^(-1/2)``.  The polar decompositions of the two rows of
(1) are branchwise gauges taking (1) to
``V_C=[sqrt(C);sqrt(I-C)]``.  Thus (2) is exactly the positive-child-metric
form of the previously proved canonical four-block Weyl formula, not a new
endpoint ansatz.

Now expose the leaf addresses.  For isometric inclusions ``J_e:M_e->H`` and
child address sets ``E_0,E_1``, let

    R_s x = direct_sum_(e in E_s) J_e^*x,
    A_s   = sum_(e in E_s) J_eJ_e^*.

The available normalization-one addressed oracle supplies the raw blocks

    (R_s R_t^*)_(f,e)=J_f^*J_e.                            (3)

But the desired Weyl block on leaf addresses is

    (R S^(-1/2) U S^(-1/2) R^*)_(f,e)
      = J_f^* S^(-1/2) U S^(-1/2) J_e.                    (4)

Equations (3) and (4) differ by the shared *global parent whitening*.  Taking
pair polars or applying functional calculus separately to every (3) cannot
create ``S^(-1/2)``.  Even a fixed addressed pair is not locally sufficient:
two frames can agree on that pair and its pair polar while unqueried leaves
change (4) by a constant.

A coherent query over all ``w=|E_0|+|E_1|`` leaves does contain the missing
metric information, but only in the normalized signals

    R/sqrt(w),       G/w=RR^*/w,       S/w=R^*R/w.          (5)

Uniform address preparation/erasure has sharp dense normalization ``w``.
On the retained parent window ``0.5I<=S<=16I``, the singular values of the
analysis signal in (5) lie in

    [sqrt(0.5/w), 4/sqrt(w)].                              (6)

Consequently a bounded QSVT polar polynomial of constant error has degree
``Omega(sqrt(w))`` by the Bernstein sign bound.  At the selected natural
copy count, ``w=Theta(n!)``.  Therefore ``O(1)`` coherent addressed queries
plus pair-local functional calculus do not assemble either endpoint Weyl
generator through this canonical uniform route.

The binary top node itself is not costly.  Conditional on constant-
normalization block encodings of the two *aggregate* maps ``sqrt(A_s)``, a
binary LCU has normalization at most ``4sqrt(2)`` on the retained window;
its minimum signal is at least ``1/8``.  QSVT then compiles (1), and hence
``T X T^*`` and ``T Z T^*``, in ``O(log(1/epsilon))`` aggregate queries.
The unresolved operation is precisely obtaining those aggregate child maps,
or an equivalent direct global polar, from the leaf-addressed interface.

This is a sharp boundary for uniform linear address assembly followed by
bounded singular-value transformation and for pair-local metric formulas.
It is not an arbitrary quantum-query lower bound: a hierarchical nonlinear
compiler, representation-specific global polar, or earlier-level
normalization cancellation remains possible.  It proves no physical PGM,
decoder, classical separation, or speedup.
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
from self_dual_wreath_final_root_metric_access_width_no_go import (
    PARENT_WINDOW_LOWER,
    PARENT_WINDOW_UPPER,
    bernstein_sign_degree_lower_bound,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_addressed_weyl_assembly_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-"
    "ADDRESSED-WEYL-ASSEMBLY-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-FINAL-ROOT-ADDRESSED-PAIR-WEYL-"
    "MISSING-GLOBAL-WHITENING"
)
DEFAULT_POLAR_ERROR = 0.1


@dataclass(frozen=True)
class TwoChildWeylFactorizationControl:
    control_id: str
    logical_dimension: int
    parent_minimum_eigenvalue: float
    parent_maximum_eigenvalue: float
    relative_effect_minimum_eigenvalue: float
    relative_effect_maximum_eigenvalue: float
    child_metric_commutator_norm: float
    parent_reconstruction_residual: float
    positive_endpoint_isometry_residual: float
    canonical_endpoint_isometry_residual: float
    maximum_positive_four_block_residual: float
    maximum_branch_gauge_endpoint_residual: float
    maximum_canonical_four_block_residual: float
    shift_byproduct_operator_norm: float
    clock_byproduct_operator_norm: float
    exact_two_child_weyl_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class AddressedWhitenedBlockControl:
    control_id: str
    logical_dimension: int
    leaves_per_child: int
    total_leaf_count: int
    parent_minimum_eigenvalue: float
    parent_maximum_eigenvalue: float
    child_metric_commutator_norm: float
    maximum_addressed_raw_cross_map_residual: float
    maximum_addressed_whitened_weyl_block_residual: float
    full_leaf_byproduct_factorization_residual: float
    maximum_raw_to_whitened_weyl_block_gap: float
    raw_addressed_cross_maps_equal_target_blocks: bool
    exact_addressed_whitened_formula_verified: bool
    status: str


@dataclass(frozen=True)
class PairLocalIndeterminacyControl:
    logical_dimension: int
    total_leaf_count_per_frame: int
    selected_pair_raw_cross_map_residual: float
    selected_pair_polar_residual: float
    first_parent_minimum_eigenvalue: float
    first_parent_maximum_eigenvalue: float
    second_parent_minimum_eigenvalue: float
    second_parent_maximum_eigenvalue: float
    parent_metric_operator_distance: float
    first_selected_shift_block: float
    second_selected_shift_block: float
    selected_whitened_shift_block_gap: float
    pair_local_data_determine_whitened_weyl_block: bool
    exact_pair_local_indeterminacy_verified: bool
    status: str


@dataclass(frozen=True)
class AddressedWidthControl:
    total_leaf_count: int
    leaves_per_child: int
    logical_dimension: int
    addressed_entry_query_normalization: float
    dense_gram_linear_assembly_normalization: float
    normalized_parent_metric_eigenvalue: float
    normalized_analysis_singular_value: float
    qsvt_polar_error: float
    bernstein_qsvt_degree_lower_bound: float
    analysis_gram_residual: float
    dense_gram_residual: float
    sharp_width_normalization_verified: bool
    known_structure_specific_identity_bypass: bool
    status: str


@dataclass(frozen=True)
class ConditionalAggregateCompilerRecord:
    retained_parent_lower_edge: float
    retained_parent_upper_edge: float
    maximum_child_square_root_normalization: float
    binary_lcu_normalization: float
    minimum_binary_lcu_signal: float
    maximum_binary_lcu_signal: float
    fixed_error_query_dependence: str
    inverse_polynomial_error_query_dependence: str
    endpoint_weyl_byproduct_uses_two_endpoint_calls: bool
    width_independent_given_aggregate_access: bool
    aggregate_child_access_supplied_by_addressed_oracle: bool
    status: str


@dataclass(frozen=True)
class NaturalAddressedWeylScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    child_leaf_width_decimal: str
    total_leaf_width_decimal: str
    total_leaf_width_log2: float
    retained_signal_maximum_singular_value_log2: float
    bernstein_degree_lower_bound_log2: float
    canonical_uniform_assembly_superpolynomial: bool
    final_binary_lcu_additional_width_charge: bool
    representation_specific_global_polar_ruled_out: bool
    status: str


@dataclass(frozen=True)
class FinalRootAddressedWeylAssemblyTheorem:
    two_child_endpoint: str
    positive_metric_four_blocks: str
    canonical_gauge: str
    addressed_raw_interface: str
    addressed_target_blocks: str
    shared_global_operation: str
    coherent_uniform_assembly: str
    retained_window_cost: str
    conditional_binary_closure: str
    labelled_weyl_rigidity: str
    surviving_route: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootAddressedWeylAssemblyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FinalRootAddressedWeylAssemblyTheorem
    two_child_controls: list[TwoChildWeylFactorizationControl]
    addressed_controls: list[AddressedWhitenedBlockControl]
    pair_local_control: PairLocalIndeterminacyControl
    width_controls: list[AddressedWidthControl]
    conditional_aggregate_compiler: ConditionalAggregateCompilerRecord
    scaling_records: list[NaturalAddressedWeylScalingRecord]
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
    if float(values[0]) < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** exponent
    return (vectors * transformed) @ vectors.conj().T


def _weyl_generators(dimension: int) -> tuple[np.ndarray, np.ndarray]:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    shift = np.zeros((dimension, dimension), dtype=complex)
    for source in range(dimension):
        shift[(source + 1) % dimension, source] = 1.0
    omega = np.exp(2j * np.pi / dimension)
    clock = np.diag(omega ** np.arange(dimension)).astype(complex)
    return shift, clock


def _polar_unitary(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular, right_adjoint = np.linalg.svd(matrix, full_matrices=False)
    if float(singular[-1]) <= 100 * tolerance:
        raise ValueError("finite positive-coordinate controls require full rank")
    return left @ right_adjoint


def _deterministic_unitary(dimension: int, phase: float) -> np.ndarray:
    indices = np.arange(dimension, dtype=float)
    fourier = np.exp(
        2j * np.pi * np.outer(indices, indices) / dimension
    ) / math.sqrt(dimension)
    diagonal = np.diag(np.exp(1j * phase * (indices + 1) ** 2))
    return fourier @ diagonal @ fourier.conj().T


def deterministic_child_metrics(dimension: int) -> tuple[np.ndarray, np.ndarray]:
    """Return noncommuting positive child metrics with retained parent window."""

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    parent_basis = _deterministic_unitary(dimension, 0.173)
    effect_basis = _deterministic_unitary(dimension, 0.419)
    parent = parent_basis @ np.diag(np.linspace(1.0, 3.0, dimension)) @ parent_basis.conj().T
    effect = effect_basis @ np.diag(np.linspace(0.2, 0.8, dimension)) @ effect_basis.conj().T
    parent_sqrt = _psd_power(parent, 0.5)
    left = _hermitian(parent_sqrt @ effect @ parent_sqrt)
    right = _hermitian(parent_sqrt @ (np.eye(dimension) - effect) @ parent_sqrt)
    return left, right


def audit_two_child_weyl_factorization(
    control_id: str,
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> TwoChildWeylFactorizationControl:
    """Verify (1)--(2) and the branchwise gauge to the canonical endpoint."""

    left = _hermitian(np.asarray(left_metric, dtype=complex))
    right = _hermitian(np.asarray(right_metric, dtype=complex))
    if left.shape != right.shape or left.ndim != 2 or left.shape[0] != left.shape[1]:
        raise ValueError("child metrics must be same-size square matrices")
    dimension = len(left)
    identity = np.eye(dimension, dtype=complex)
    parent = _hermitian(left + right)
    parent_values = np.linalg.eigvalsh(parent)
    if float(parent_values[0]) <= 100 * tolerance:
        raise ValueError("parent metric must be positive definite")
    if min(float(np.linalg.eigvalsh(left)[0]), float(np.linalg.eigvalsh(right)[0])) <= 100 * tolerance:
        raise ValueError("finite controls require positive-definite child metrics")

    parent_inverse_sqrt = _psd_power(parent, -0.5, tolerance=tolerance)
    left_sqrt = _psd_power(left, 0.5, tolerance=tolerance)
    right_sqrt = _psd_power(right, 0.5, tolerance=tolerance)
    top = left_sqrt @ parent_inverse_sqrt
    bottom = right_sqrt @ parent_inverse_sqrt
    positive_endpoint = np.vstack((top, bottom))
    effect = _hermitian(top.conj().T @ top)
    complement = _hermitian(bottom.conj().T @ bottom)
    effect_sqrt = _psd_power(effect, 0.5, tolerance=tolerance)
    complement_sqrt = _psd_power(complement, 0.5, tolerance=tolerance)
    canonical = np.vstack((effect_sqrt, complement_sqrt))
    top_polar = _polar_unitary(top, tolerance)
    bottom_polar = _polar_unitary(bottom, tolerance)
    zero = np.zeros((dimension, dimension), dtype=complex)
    gauge = np.block(
        [[top_polar.conj().T, zero], [zero, bottom_polar.conj().T]]
    )

    parent_reconstruction = float(
        np.linalg.norm(
            parent_inverse_sqrt @ parent @ parent_inverse_sqrt - identity,
            ord=2,
        )
    )
    positive_isometry = float(
        np.linalg.norm(positive_endpoint.conj().T @ positive_endpoint - identity, ord=2)
    )
    canonical_isometry = float(
        np.linalg.norm(canonical.conj().T @ canonical - identity, ord=2)
    )
    gauge_residual = float(np.linalg.norm(gauge @ positive_endpoint - canonical, ord=2))
    maximum_positive_block = 0.0
    maximum_canonical_block = 0.0
    byproduct_norms: list[float] = []
    for logical in _weyl_generators(dimension):
        direct = positive_endpoint @ logical @ positive_endpoint.conj().T
        expected = np.block(
            [
                [
                    left_sqrt @ parent_inverse_sqrt @ logical @ parent_inverse_sqrt @ left_sqrt,
                    left_sqrt @ parent_inverse_sqrt @ logical @ parent_inverse_sqrt @ right_sqrt,
                ],
                [
                    right_sqrt @ parent_inverse_sqrt @ logical @ parent_inverse_sqrt @ left_sqrt,
                    right_sqrt @ parent_inverse_sqrt @ logical @ parent_inverse_sqrt @ right_sqrt,
                ],
            ]
        )
        maximum_positive_block = max(
            maximum_positive_block,
            float(np.linalg.norm(direct - expected, ord=2)),
        )
        canonical_direct = canonical @ logical @ canonical.conj().T
        canonical_expected = np.block(
            [
                [effect_sqrt @ logical @ effect_sqrt, effect_sqrt @ logical @ complement_sqrt],
                [complement_sqrt @ logical @ effect_sqrt, complement_sqrt @ logical @ complement_sqrt],
            ]
        )
        maximum_canonical_block = max(
            maximum_canonical_block,
            float(np.linalg.norm(canonical_direct - canonical_expected, ord=2)),
            float(np.linalg.norm(gauge @ direct @ gauge.conj().T - canonical_direct, ord=2)),
        )
        byproduct_norms.append(float(np.linalg.norm(direct, ord=2)))

    effect_values = np.linalg.eigvalsh(effect)
    commutator = float(np.linalg.norm(left @ right - right @ left, ord=2))
    verified = bool(
        parent_reconstruction <= 100 * tolerance
        and positive_isometry <= 100 * tolerance
        and canonical_isometry <= 100 * tolerance
        and gauge_residual <= 100 * tolerance
        and maximum_positive_block <= 100 * tolerance
        and maximum_canonical_block <= 100 * tolerance
        and float(effect_values[0]) >= -100 * tolerance
        and float(effect_values[-1]) <= 1 + 100 * tolerance
    )
    return TwoChildWeylFactorizationControl(
        control_id=control_id,
        logical_dimension=dimension,
        parent_minimum_eigenvalue=float(parent_values[0]),
        parent_maximum_eigenvalue=float(parent_values[-1]),
        relative_effect_minimum_eigenvalue=float(effect_values[0]),
        relative_effect_maximum_eigenvalue=float(effect_values[-1]),
        child_metric_commutator_norm=commutator,
        parent_reconstruction_residual=parent_reconstruction,
        positive_endpoint_isometry_residual=positive_isometry,
        canonical_endpoint_isometry_residual=canonical_isometry,
        maximum_positive_four_block_residual=maximum_positive_block,
        maximum_branch_gauge_endpoint_residual=gauge_residual,
        maximum_canonical_four_block_residual=maximum_canonical_block,
        shift_byproduct_operator_norm=byproduct_norms[0],
        clock_byproduct_operator_norm=byproduct_norms[1],
        exact_two_child_weyl_factorization_verified=verified,
        status=(
            "exact-positive-child-and-canonical-weyl-factorization"
            if verified
            else "two-child-weyl-factorization-control-failure"
        ),
    )


def addressed_leaf_frame(dimension: int) -> tuple[tuple[np.ndarray, ...], tuple[np.ndarray, ...]]:
    """Return two overcomplete unit-vector child frames with noncommuting metrics."""

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    computational = tuple(
        np.eye(dimension, dtype=complex)[:, index : index + 1]
        for index in range(dimension)
    )
    fourier = _deterministic_unitary(dimension, 0.237)
    rotated = tuple(fourier[:, index : index + 1] for index in range(dimension))
    left_extra = np.arange(1, dimension + 1, dtype=float)[:, None].astype(complex)
    left_extra /= np.linalg.norm(left_extra)
    right_extra = (
        np.arange(dimension, 0, -1, dtype=float)[:, None]
        + 1j * np.arange(1, dimension + 1, dtype=float)[:, None] / 3.0
    )
    right_extra /= np.linalg.norm(right_extra)
    return computational + (left_extra,), rotated + (right_extra,)


def audit_addressed_whitened_blocks(
    control_id: str,
    left_leaves: tuple[np.ndarray, ...],
    right_leaves: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> AddressedWhitenedBlockControl:
    """Verify raw (3) and globally whitened Weyl blocks (4)."""

    if not left_leaves or len(left_leaves) != len(right_leaves):
        raise ValueError("controls require equal nonempty child leaf sets")
    dimension = left_leaves[0].shape[0]
    leaves = left_leaves + right_leaves
    if any(leaf.shape != (dimension, 1) for leaf in leaves):
        raise ValueError("every leaf must be a single-column inclusion")
    if any(abs(float(np.vdot(leaf, leaf).real) - 1.0) > 100 * tolerance for leaf in leaves):
        raise ValueError("leaf inclusions must be isometric")

    analysis = np.vstack([leaf.conj().T for leaf in leaves])
    left_analysis = np.vstack([leaf.conj().T for leaf in left_leaves])
    right_analysis = np.vstack([leaf.conj().T for leaf in right_leaves])
    left_metric = _hermitian(left_analysis.conj().T @ left_analysis)
    right_metric = _hermitian(right_analysis.conj().T @ right_analysis)
    parent = _hermitian(left_metric + right_metric)
    parent_values = np.linalg.eigvalsh(parent)
    if float(parent_values[0]) <= 100 * tolerance:
        raise ValueError("leaf frame must span the parent")
    parent_inverse_sqrt = _psd_power(parent, -0.5, tolerance=tolerance)
    raw_gram = analysis @ analysis.conj().T
    maximum_raw_residual = 0.0
    for target, target_leaf in enumerate(leaves):
        for source, source_leaf in enumerate(leaves):
            expected = target_leaf.conj().T @ source_leaf
            maximum_raw_residual = max(
                maximum_raw_residual,
                abs(complex(raw_gram[target, source]) - complex(expected[0, 0])),
            )

    maximum_whitened_residual = 0.0
    maximum_gap = 0.0
    full_residual = 0.0
    for logical in _weyl_generators(dimension):
        full = analysis @ parent_inverse_sqrt @ logical @ parent_inverse_sqrt @ analysis.conj().T
        assembled = np.zeros_like(full)
        for target, target_leaf in enumerate(leaves):
            for source, source_leaf in enumerate(leaves):
                expected = target_leaf.conj().T @ parent_inverse_sqrt @ logical @ parent_inverse_sqrt @ source_leaf
                assembled[target, source] = expected[0, 0]
                maximum_whitened_residual = max(
                    maximum_whitened_residual,
                    abs(complex(full[target, source]) - complex(expected[0, 0])),
                )
                maximum_gap = max(
                    maximum_gap,
                    abs(complex(expected[0, 0]) - complex(raw_gram[target, source])),
                )
        full_residual = max(full_residual, float(np.linalg.norm(full - assembled, ord=2)))

    commutator = float(
        np.linalg.norm(left_metric @ right_metric - right_metric @ left_metric, ord=2)
    )
    verified = bool(
        maximum_raw_residual <= 100 * tolerance
        and maximum_whitened_residual <= 100 * tolerance
        and full_residual <= 100 * tolerance
        and maximum_gap > 1000 * tolerance
        and commutator > 1000 * tolerance
    )
    return AddressedWhitenedBlockControl(
        control_id=control_id,
        logical_dimension=dimension,
        leaves_per_child=len(left_leaves),
        total_leaf_count=len(leaves),
        parent_minimum_eigenvalue=float(parent_values[0]),
        parent_maximum_eigenvalue=float(parent_values[-1]),
        child_metric_commutator_norm=commutator,
        maximum_addressed_raw_cross_map_residual=maximum_raw_residual,
        maximum_addressed_whitened_weyl_block_residual=maximum_whitened_residual,
        full_leaf_byproduct_factorization_residual=full_residual,
        maximum_raw_to_whitened_weyl_block_gap=maximum_gap,
        raw_addressed_cross_maps_equal_target_blocks=maximum_gap <= 100 * tolerance,
        exact_addressed_whitened_formula_verified=verified,
        status=(
            "raw-addressed-versus-global-whitened-weyl-blocks-separated"
            if verified
            else "addressed-whitened-block-control-failure"
        ),
    )


def audit_pair_local_indeterminacy(
    tolerance: float = 1e-10,
) -> PairLocalIndeterminacyControl:
    """Hold one addressed pair fixed while other leaves change its Weyl block."""

    first = np.asarray([[1.0], [0.0]], dtype=complex)
    second = np.asarray([[0.0], [1.0]], dtype=complex)
    frame_zero = (first, second, first, second)
    frame_one = (first, second, first, first)
    shift, _ = _weyl_generators(2)

    parents = []
    selected_blocks = []
    for frame in (frame_zero, frame_one):
        parent = sum(leaf @ leaf.conj().T for leaf in frame)
        inverse_sqrt = _psd_power(parent, -0.5, tolerance=tolerance)
        parents.append(parent)
        selected_blocks.append(
            float(
                np.real(
                    (first.conj().T @ inverse_sqrt @ shift @ inverse_sqrt @ second)[0, 0]
                )
            )
        )
    raw_zero = first.conj().T @ second
    raw_one = first.conj().T @ second
    raw_residual = float(np.linalg.norm(raw_zero - raw_one, ord=2))
    polar_zero = np.zeros_like(raw_zero)
    polar_one = np.zeros_like(raw_one)
    polar_residual = float(np.linalg.norm(polar_zero - polar_one, ord=2))
    gap = abs(selected_blocks[0] - selected_blocks[1])
    values_zero = np.linalg.eigvalsh(parents[0])
    values_one = np.linalg.eigvalsh(parents[1])
    parent_distance = float(np.linalg.norm(parents[0] - parents[1], ord=2))
    verified = bool(
        raw_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
        and parent_distance > 0.9
        and gap > 0.05
    )
    return PairLocalIndeterminacyControl(
        logical_dimension=2,
        total_leaf_count_per_frame=4,
        selected_pair_raw_cross_map_residual=raw_residual,
        selected_pair_polar_residual=polar_residual,
        first_parent_minimum_eigenvalue=float(values_zero[0]),
        first_parent_maximum_eigenvalue=float(values_zero[-1]),
        second_parent_minimum_eigenvalue=float(values_one[0]),
        second_parent_maximum_eigenvalue=float(values_one[-1]),
        parent_metric_operator_distance=parent_distance,
        first_selected_shift_block=selected_blocks[0],
        second_selected_shift_block=selected_blocks[1],
        selected_whitened_shift_block_gap=gap,
        pair_local_data_determine_whitened_weyl_block=False,
        exact_pair_local_indeterminacy_verified=verified,
        status=(
            "fixed-pair-data-global-whitening-indeterminate"
            if verified
            else "pair-local-indeterminacy-control-failure"
        ),
    )


def audit_addressed_width_control(
    total_leaf_count: int,
    *,
    approximation_error: float = DEFAULT_POLAR_ERROR,
    tolerance: float = 1e-12,
) -> AddressedWidthControl:
    """Use an orthogonal frame to verify the sharp uniform width signal."""

    if total_leaf_count < 4 or total_leaf_count % 2:
        raise ValueError("total_leaf_count must be even and at least four")
    analysis = np.eye(total_leaf_count, dtype=complex)
    normalized_analysis = analysis / math.sqrt(total_leaf_count)
    normalized_parent = normalized_analysis.conj().T @ normalized_analysis
    normalized_gram = normalized_analysis @ normalized_analysis.conj().T
    target = np.eye(total_leaf_count, dtype=complex) / total_leaf_count
    analysis_residual = float(np.linalg.norm(normalized_parent - target, ord=2))
    gram_residual = float(np.linalg.norm(normalized_gram - target, ord=2))
    signal = 1.0 / math.sqrt(total_leaf_count)
    degree = bernstein_sign_degree_lower_bound(signal, approximation_error)
    verified = bool(
        analysis_residual <= 100 * tolerance
        and gram_residual <= 100 * tolerance
        and abs(degree - (1.0 - approximation_error) * math.sqrt(total_leaf_count - 1))
        <= 100 * tolerance * total_leaf_count
    )
    return AddressedWidthControl(
        total_leaf_count=total_leaf_count,
        leaves_per_child=total_leaf_count // 2,
        logical_dimension=total_leaf_count,
        addressed_entry_query_normalization=1.0,
        dense_gram_linear_assembly_normalization=float(total_leaf_count),
        normalized_parent_metric_eigenvalue=1.0 / total_leaf_count,
        normalized_analysis_singular_value=signal,
        qsvt_polar_error=approximation_error,
        bernstein_qsvt_degree_lower_bound=degree,
        analysis_gram_residual=analysis_residual,
        dense_gram_residual=gram_residual,
        sharp_width_normalization_verified=verified,
        known_structure_specific_identity_bypass=True,
        status=(
            "uniform-address-width-charge-sharp-architecture-control"
            if verified
            else "addressed-width-control-failure"
        ),
    )


def conditional_aggregate_compiler_record() -> ConditionalAggregateCompilerRecord:
    child_alpha = math.sqrt(PARENT_WINDOW_UPPER)
    binary_alpha = math.sqrt(2.0) * child_alpha
    minimum_signal = math.sqrt(PARENT_WINDOW_LOWER) / binary_alpha
    maximum_signal = math.sqrt(PARENT_WINDOW_UPPER) / binary_alpha
    return ConditionalAggregateCompilerRecord(
        retained_parent_lower_edge=PARENT_WINDOW_LOWER,
        retained_parent_upper_edge=PARENT_WINDOW_UPPER,
        maximum_child_square_root_normalization=child_alpha,
        binary_lcu_normalization=binary_alpha,
        minimum_binary_lcu_signal=minimum_signal,
        maximum_binary_lcu_signal=maximum_signal,
        fixed_error_query_dependence="O(1) aggregate-child queries",
        inverse_polynomial_error_query_dependence="O(log(1/epsilon)) aggregate-child queries",
        endpoint_weyl_byproduct_uses_two_endpoint_calls=True,
        width_independent_given_aggregate_access=True,
        aggregate_child_access_supplied_by_addressed_oracle=False,
        status="binary-top-merge-conditionally-constant-aggregate-access-open",
    )


def _selected_final_root_parameters(n: int) -> tuple[int, int, int, int, float]:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    information_copies = (order - 1).bit_length()
    selected_copies = information_copies + 2
    child_width = 1 << (selected_copies - 1)
    return order, information_copies, selected_copies, child_width, child_width / order


def natural_addressed_weyl_scaling_record(
    n: int,
    *,
    approximation_error: float = DEFAULT_POLAR_ERROR,
) -> NaturalAddressedWeylScalingRecord:
    order, information, selected, child_width, _ = _selected_final_root_parameters(n)
    total_width = 2 * child_width
    log_width = math.log2(total_width)
    signal_log2 = 2.0 - 0.5 * log_width
    ratio = 2.0 ** (4.0 - log_width)
    degree_log2 = (
        math.log2(1.0 - approximation_error)
        + 0.5 * math.log2(max(1e-300, 1.0 - ratio))
        + 0.5 * log_width
        - 2.0
    )
    return NaturalAddressedWeylScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=information,
        selected_copy_count=selected,
        child_leaf_width_decimal=str(child_width),
        total_leaf_width_decimal=str(total_width),
        total_leaf_width_log2=log_width,
        retained_signal_maximum_singular_value_log2=signal_log2,
        bernstein_degree_lower_bound_log2=degree_log2,
        canonical_uniform_assembly_superpolynomial=True,
        final_binary_lcu_additional_width_charge=False,
        representation_specific_global_polar_ruled_out=False,
        status="uniform-addressed-weyl-assembly-sqrt-factorial-boundary",
    )


def run_final_root_addressed_weyl_assembly_boundary(
) -> FinalRootAddressedWeylAssemblyReport:
    two_child_controls = [
        audit_two_child_weyl_factorization(
            f"noncommuting-positive-metrics-d{dimension}",
            *deterministic_child_metrics(dimension),
        )
        for dimension in (2, 3, 4)
    ]
    addressed_controls = [
        audit_addressed_whitened_blocks(
            f"overcomplete-addressed-frame-d{dimension}",
            *addressed_leaf_frame(dimension),
        )
        for dimension in (2, 3, 4)
    ]
    pair_local = audit_pair_local_indeterminacy()
    width_controls = [
        audit_addressed_width_control(width) for width in (4, 8, 16, 32, 64)
    ]
    conditional = conditional_aggregate_compiler_record()
    scaling = [
        natural_addressed_weyl_scaling_record(n)
        for n in (8, 16, 24, 32, 40, 48)
    ]
    failures = (
        sum(not row.exact_two_child_weyl_factorization_verified for row in two_child_controls)
        + sum(not row.exact_addressed_whitened_formula_verified for row in addressed_controls)
        + int(not pair_local.exact_pair_local_indeterminacy_verified)
        + sum(not row.sharp_width_normalization_verified for row in width_controls)
    )
    verified = failures == 0
    theorem = FinalRootAddressedWeylAssemblyTheorem(
        two_child_endpoint=(
            "After child polars, T=[sqrt(A_0);sqrt(A_1)]S^(-1/2), S=A_0+A_1."
        ),
        positive_metric_four_blocks=(
            "(TUT^*)_(s,t)=sqrt(A_s)S^(-1/2)US^(-1/2)sqrt(A_t) for U=X,Z."
        ),
        canonical_gauge=(
            "Branchwise row polars take T to V_C=[sqrt(C);sqrt(I-C)] with C=S^(-1/2)A_0S^(-1/2), so the positive and canonical four-block formulas are unitarily equivalent."
        ),
        addressed_raw_interface=(
            "For R_s x=direct_sum_e J_e^*x, the alpha-one pair oracle supplies (R_sR_t^*)_(f,e)=J_f^*J_e."
        ),
        addressed_target_blocks=(
            "The required leaf block is J_f^*S^(-1/2)US^(-1/2)J_e, not the raw cross map or its pair polar."
        ),
        shared_global_operation=(
            "All four child blocks share the same parent inverse metric S^(-1/2); local functional calculus on separate addressed pairs cannot replace it."
        ),
        coherent_uniform_assembly=(
            "One coherent prepare/query/erase call assembles G/w and R/sqrt(w), but equal-coefficient contractivity makes the dense normalization w sharp."
        ),
        retained_window_cost=(
            "On 0.5I<=S<=16I, analysis signals lie in [sqrt(0.5/w),4/sqrt(w)], and Bernstein forces bounded-QSVT polar degree Omega(sqrt(w))."
        ),
        conditional_binary_closure=(
            "If sqrt(A_0),sqrt(A_1) are already block encoded at constant normalization, binary LCU plus QSVT compiles T and both Weyl byproducts in O(log(1/epsilon)) aggregate queries; the top binary merge adds no width charge."
        ),
        labelled_weyl_rigidity=(
            "The predecessor rigidity theorem shows the labelled conjugated shift and clock determine the endpoint up to global phase, so compiling both is not weaker endpoint data than compiling the polar."
        ),
        surviving_route=(
            "Compile constant-normalization aggregate child analyses, a hierarchical normalization cancellation, or a direct representation-specific global orientation polar."
        ),
        scope=(
            "The no-go covers pair-local formulas and canonical uniform linear address assembly followed by bounded QSVT. It is not an arbitrary multi-query or representation-specific circuit lower bound."
        ),
        theorem_verified=verified,
        status=(
            "final-root-addressed-weyl-requires-global-whitening-binary-merge-conditional"
            if verified
            else "final-root-addressed-weyl-assembly-control-failure"
        ),
    )
    return FinalRootAddressedWeylAssemblyReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "Normalization-one coherent access to every addressed J_f^*J_e, together with direct pair polars and local functional calculus, assembles the final two-child conjugated Weyl shift and clock with O(1) coherent pair queries."
            ),
            "exact_reduction": (
                "Every positive-coordinate child block equals sqrt(A_s)S^(-1/2)US^(-1/2)sqrt(A_t), and every leaf block equals J_f^*S^(-1/2)US^(-1/2)J_e."
            ),
            "negative_boundary": (
                "The addressed oracle supplies raw pair blocks but not the shared parent whitening. Uniform global assembly exposes only R/sqrt(w) or G/w and bounded QSVT costs Omega(sqrt(w))."
            ),
            "positive_boundary": (
                "Given constant-normalization aggregate child square-root maps, the final binary merge and both Weyl byproducts are width independent and polynomial."
            ),
            "claim_boundary": (
                "No arbitrary-query lower bound, natural decoder, physical PGM, classical separation, or speedup is proved."
            ),
        },
        theorem=theorem,
        two_child_controls=two_child_controls,
        addressed_controls=addressed_controls,
        pair_local_control=pair_local,
        width_controls=width_controls,
        conditional_aggregate_compiler=conditional,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "rewrite_final_two_child_weyl_blocks_with_positive_metrics",
                "resolved": True,
                "evidence": "Equation (2) follows by direct multiplication of T=[sqrt(A_0);sqrt(A_1)]S^(-1/2); three noncommuting controls verify shift and clock blocks and the canonical branch gauge.",
            },
            {
                "obligation": "translate_each_target_block_to_addressed_leaf_language",
                "resolved": True,
                "evidence": "For R_sx=direct_sum_eJ_e^*x, the raw oracle block is J_f^*J_e while the target is J_f^*S^(-1/2)US^(-1/2)J_e.",
            },
            {
                "obligation": "decide_pair_local_functional_calculus",
                "resolved": True,
                "evidence": "A fixed pair and its pair polar remain identical in two exact frames while other leaves change its whitened shift block by a constant; pair-local data are insufficient.",
            },
            {
                "obligation": "decide_constant_coherent_uniform_pair_query_route",
                "resolved": True,
                "evidence": "Coherent global access forms the exact normalized analysis, but its signal is O(w^-1/2); the sharp coefficient normalization and Bernstein bound force Omega(sqrt(w)) bounded-QSVT degree.",
            },
            {
                "obligation": "separate_final_binary_cost_from_child_aggregation_cost",
                "resolved": True,
                "evidence": "Conditional constant-normalization sqrt(A_s) access gives binary normalization at most 4sqrt(2), minimum retained signal 1/8, and logarithmic precision dependence independent of w.",
            },
            {
                "obligation": "compile_constant_normalization_aggregate_child_maps",
                "resolved": False,
                "evidence": "The addressed leaf oracle supplies only the q-normalized aggregate route; no hierarchical cancellation or direct representation-specific child analysis compiler is constructed.",
            },
            {
                "obligation": "implement_physical_pgm_and_hidden_involution_decoder",
                "resolved": False,
                "evidence": "The theorem ends at the orientation polar/byproduct access boundary and proves neither measurement implementation nor decoding success.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "There are only two final children, so four addressed pair blocks suffice at constant cost.",
                "resolved": True,
                "resolution": "The two child labels hide q leaf addresses each. The four aggregate blocks contain sqrt(A_s) and the shared S^(-1/2); the alpha-one oracle addresses leaves, not normalization-one aggregate children.",
            },
            {
                "objection": "Taking the polar of every J_f^*J_e performs the required whitening locally.",
                "resolved": True,
                "resolution": "The target leaf blocks contain S^(-1/2) on the common parent. Pair polar discards positive correlations and the predecessor holonomy theorem shows its global phase-only kernel can be indefinite.",
            },
            {
                "objection": "One coherent superposition query means the global metric is available at alpha one.",
                "resolved": True,
                "resolution": "It produces G/w or R/sqrt(w). Uniform equal-coefficient assembly has sharp alpha=w, and the retained absolute parent window therefore appears at O(1/w) metric scale or O(1/sqrt(w)) analysis scale.",
            },
            {
                "objection": "The Omega(sqrt(w)) bound proves every quantum circuit is superpolynomial.",
                "resolved": True,
                "resolution": "It applies to bounded QSVT on the uniformly normalized analysis signal. Direct structured polars, nonlinear recursion, and normalization cancellation are outside its scope.",
            },
            {
                "objection": "The binary endpoint itself necessarily pays the full orientation width.",
                "resolved": True,
                "resolution": "False conditionally: constant-normalization aggregate sqrt(A_s) access makes the binary LCU and retained-window polar width independent. The charge lies in producing those aggregate maps from leaf access.",
            },
            {
                "objection": "Compiling only the shift and clock may be easier than compiling the endpoint polar.",
                "resolved": True,
                "resolution": "The labelled-Weyl rigidity identity determines the endpoint up to global phase from the two conjugated generators; no information-level shortcut is gained.",
            },
        ],
        headline_metrics={
            "exact_positive_child_weyl_four_block_theorem_count": int(verified),
            "exact_addressed_leaf_whitened_block_theorem_count": int(verified),
            "pair_local_global_metric_indeterminacy_theorem_count": int(verified),
            "uniform_address_width_qsvt_lower_bound_theorem_count": int(verified),
            "conditional_constant_cost_binary_merge_theorem_count": int(verified),
            "two_child_control_count": len(two_child_controls),
            "addressed_control_count": len(addressed_controls),
            "width_control_count": len(width_controls),
            "finite_control_failure_count": failures,
            "minimum_conditional_binary_signal": conditional.minimum_binary_lcu_signal,
            "largest_finite_width_degree_lower_bound": width_controls[-1].bernstein_qsvt_degree_lower_bound,
            "compiled_constant_normalization_aggregate_child_map_count": 0,
            "compiled_endpoint_weyl_pair_count": 0,
            "physical_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "positive_child_metric_four_block_formula_proved": verified,
            "canonical_and_positive_child_formulas_branchwise_unitarily_equivalent": verified,
            "addressed_raw_cross_map_normalization_one_available": True,
            "target_leaf_blocks_require_shared_parent_inverse_metric": verified,
            "pair_local_functional_calculus_suffices": False,
            "uniform_coherent_address_assembly_signal_is_R_over_sqrt_w": verified,
            "uniform_coherent_dense_gram_assembly_normalization_is_w": verified,
            "bounded_qsvt_uniform_assembly_degree_omega_sqrt_w": verified,
            "final_binary_merge_width_independent_given_aggregate_access": verified,
            "addressed_leaf_oracle_supplies_constant_normalization_aggregate_child_maps": False,
            "endpoint_weyl_shift_compiled": False,
            "endpoint_weyl_clock_compiled": False,
            "orientation_polar_Q_R_compiled": False,
            "arbitrary_multi_query_lower_bound_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact Weyl blocks retain the shared global parent whitening. Alpha-one leaf-pair access assembles it only through width-normalized global signals in the canonical route; constant-cost binary closure is conditional on the still-missing aggregate child access."
            ),
        },
        status=theorem.status,
        summary=(
            "Rewrote the final Weyl pair in positive-child and addressed-leaf coordinates, proving that all four blocks share the missing parent inverse metric. The binary top merge is conditionally constant, but the available leaf oracle reaches it only through a sharp width-normalized global signal."
        ),
        falsifiers_triggered=[
            "Two final child labels do not turn alpha-one leaf-pair queries into alpha-one aggregate child access.",
            "Raw J_f^*J_e blocks and their pair polars are not the globally whitened Weyl blocks J_f^*S^(-1/2)US^(-1/2)J_e.",
            "One coherent uniform pair query assembles G/w, not G at normalization one.",
            "The obstruction is not the binary top node: supplied aggregate child square-root maps would close it at constant retained-window condition number.",
            "The scoped QSVT width lower bound does not rule out hierarchical or representation-specific global polar circuits.",
        ],
    )


def write_final_root_addressed_weyl_assembly_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_addressed_weyl_assembly_boundary())
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
                title="Final-root addressed Weyl assembly boundary",
                status="completed-exact-assembly-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Factor the final two-child endpoint through positive child metrics, expand both Weyl generators into child and leaf-addressed blocks, audit pair-local indeterminacy, and apply the sharp uniform-address normalization plus Bernstein polar-degree bound."
                ),
                positive_signal=(
                    "A constant-normalization compiler for the aggregate child analyses or square-root metrics, a hierarchical cancellation of their inherited q normalization, or a direct representation-specific global orientation polar."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary.py",
                    "self_dual_wreath_addressed_cross_map_linear_assembly_normalization_boundary.py",
                    "self_dual_wreath_final_root_metric_access_width_no_go.py",
                    "self_dual_wreath_final_root_byproduct_covariance_no_go.py",
                    "self_dual_wreath_final_root_physical_preparation_extension_scope_boundary.py",
                ],
                next_actions=[
                    "Audit the recursive hierarchy for an exact normalization cancellation: determine whether child shorted metrics can be carried upward as constant-normalization block encodings without reassembling q leaf addresses."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Normalization-one coherent J_f^*J_e queries and pair-local functional calculus assemble the final two-child conjugated Weyl shift and clock with O(1) pair queries."
                ),
                reason_invalid=(
                    "The exact target leaf block is J_f^*S^(-1/2)US^(-1/2)J_e. The shared S^(-1/2) depends on all leaves. Uniform coherent assembly exposes R/sqrt(w) or G/w, and the retained parent window then forces Omega(sqrt(w)) bounded-QSVT polar degree. Pair polars discard the positive metric and cannot supply this whitening."
                ),
                lesson=(
                    "Treat the binary top merge as conditionally easy and target the real missing primitive: constant-normalization aggregate child analysis/metric access, hierarchical normalization cancellation, or a direct global orientation polar."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "addressed_entry_query_normalization": 1.0,
                    "target_leaf_block": "J_f^* S^(-1/2) U S^(-1/2) J_e",
                    "uniform_analysis_signal": "R/sqrt(w)",
                    "uniform_dense_gram_signal": "G/w",
                    "bounded_qsvt_degree_lower_bound": "Omega(sqrt(w))",
                    "natural_total_width": "Theta(n!)",
                    "conditional_binary_lcu_normalization": 4.0 * math.sqrt(2.0),
                    "arbitrary_multi_query_lower_bound_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_addressed_weyl_assembly_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
