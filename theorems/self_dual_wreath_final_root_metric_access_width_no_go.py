"""Raw child-frame access retains a square-root-width charge at the final root.

Let ``R_L,R_R`` be the two final child analyses, each with ``q`` orientation
leaves, and put

    A=R_L^*R_L,       B=R_R^*R_R,       S=A+B.             (1)

Uniform PREPARE/SELECT exposes ``R_s/sqrt(q)``.  Suppose the child polar
circuits have already been compiled:

    Q_s=R_s A_s^(-1/2).

They recover the positive metric square root only at the inherited raw
normalization,

    Q_L^* R_L/sqrt(q)=sqrt(A)/sqrt(q),
    Q_R^* R_R/sqrt(q)=sqrt(B)/sqrt(q).                       (2)

A binary branch LCU therefore exposes the exact node-local signal

    T = [sqrt(A); sqrt(B)]/sqrt(w),       w=2q,              (3)

with

    T^*T=S/w,
    polar(T)=[sqrt(A);sqrt(B)]S^(-1/2).                      (4)

The left effect of (4) is precisely
``C=S^(-1/2)AS^(-1/2)``.  Thus (2)--(4) are the desired metric-access
reduction, but not a polynomial-normalization compiler.

On the existing retained final-root parent window

    0.5 I <= S <= 16 I,

every signal singular value in (3) lies in

    [sqrt(0.5/w), 4/sqrt(w)].                                (5)

The endpoint itself is well conditioned; the access signal is uniformly
small.  If a bounded degree-``d`` QSVT polynomial implements the polar with
error ``epsilon<1`` at a signal singular value ``sigma``, parity gives the
target values ``+1`` and ``-1`` at ``+sigma`` and ``-sigma``.  The mean-value
theorem and Bernstein's polynomial inequality imply

    d >= (1-epsilon) sqrt(1-sigma^2)/sigma.

Using the upper edge in (5), every uniform retained-window compiler obeys

    d >= (1-epsilon) sqrt(1-16/w) sqrt(w)/4 = Omega(sqrt(w)). (6)

The same charge appears operationally.  On the native parent state
``rho=S/Tr(S)``, selecting the signal block of (3) succeeds with probability

    p_good = Tr(S^2)/(w Tr(S)).                              (7)

The proved free-MP sibling law has child rate ``alpha in [2,4]``, hence

    p_good = (2 alpha+1+o(1))/w.                            (8)

Quantum rejection sampling makes the corresponding black-box state-
conversion cost ``Theta(sqrt(w))``.  Since the selected schedule has
``q=Theta(n!)``, both (6) and (8) are superpolynomial.

This is the width/normalization charge requested by the hierarchical audit.
It falsifies the canonical construction from normalized raw child analyses,
compiled child polars, binary LCU, and generic QSVT or rejection sampling.
It does not rule out a representation-specific metric oracle, a direct
matrix-POVM Naimark dilation, nonlinear multi-query structure outside this
black-box model, an earlier-level recursive cancellation, or a quantum
speedup.  The flat control is deliberately retained: when the endpoint is
known to be a Hadamard it can be implemented directly, showing that (6) is an
access-model lower bound rather than an arbitrary-circuit lower bound.
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
    "self_dual_wreath_final_root_metric_access_width_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-METRIC-ACCESS-WIDTH-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-FINAL-ROOT-RAW-METRIC-ACCESS-SQRT-WIDTH"
)
QSVT_PAPER_ID = "gilyen-su-low-wiebe-qsvt-2019"
QSVT_PAPER_URL = "https://arxiv.org/abs/1806.01838"
QRS_PAPER_ID = "ozols-roetteler-roland-qrs-2013"
QRS_PAPER_URL = "https://arxiv.org/abs/1103.2774"
PARENT_WINDOW_LOWER = 0.5
PARENT_WINDOW_UPPER = 16.0
DEFAULT_POLAR_ERROR = 0.1


@dataclass(frozen=True)
class MetricAccessWidthControl:
    control_id: str
    dimension: int
    child_orientation_width: int
    parent_orientation_width: int
    parent_minimum_eigenvalue: float
    parent_maximum_eigenvalue: float
    signal_minimum_singular_value: float
    signal_maximum_singular_value: float
    native_signal_success_probability: float
    native_rejection_sampling_factor: float
    qsvt_polar_error: float
    bernstein_qsvt_degree_lower_bound: float
    left_child_polar_isometry_residual: float
    right_child_polar_isometry_residual: float
    left_metric_square_root_composition_residual: float
    right_metric_square_root_composition_residual: float
    signal_gram_residual: float
    endpoint_polar_residual: float
    endpoint_effect_residual: float
    native_success_identity_residual: float
    exact_metric_access_factorization_verified: bool
    square_root_width_charge_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalMetricAccessWidthScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    child_orientation_width_decimal: str
    parent_orientation_width_decimal: str
    child_aspect: float
    retained_signal_minimum_singular_value: float
    retained_signal_maximum_singular_value: float
    limiting_native_signal_success_probability: float
    native_rejection_sampling_factor_log2: float
    bernstein_qsvt_degree_lower_bound: float
    bernstein_qsvt_degree_lower_bound_log2: float
    raw_metric_access_superpolynomial: bool
    matrix_endpoint_bulk_well_conditioned: bool
    representation_specific_metric_oracle_ruled_out: bool
    status: str


@dataclass(frozen=True)
class FinalRootMetricAccessWidthTheorem:
    raw_child_interface: str
    child_polar_composition: str
    binary_node_signal: str
    exact_endpoint_polar: str
    retained_signal_window: str
    qsvt_degree_lower_bound: str
    native_success_probability: str
    natural_scaling: str
    physical_relevance: str
    surviving_target: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootMetricAccessWidthReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FinalRootMetricAccessWidthTheorem
    exact_controls: list[MetricAccessWidthControl]
    scaling_records: list[NaturalMetricAccessWidthScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_power(matrix: np.ndarray, exponent: float, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if float(np.min(values)) < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** exponent
    return (vectors * transformed) @ vectors.conj().T


def bernstein_sign_degree_lower_bound(
    signal_singular_value: float,
    approximation_error: float = DEFAULT_POLAR_ERROR,
) -> float:
    """Lower-bound a bounded sign polynomial at ``+-signal_singular_value``."""

    if not math.isfinite(signal_singular_value) or not 0 < signal_singular_value < 1:
        raise ValueError("signal_singular_value must lie in (0,1)")
    if not math.isfinite(approximation_error) or not 0 <= approximation_error < 1:
        raise ValueError("approximation_error must lie in [0,1)")
    return (
        (1.0 - approximation_error)
        * math.sqrt(1.0 - signal_singular_value**2)
        / signal_singular_value
    )


def audit_metric_access_width(
    control_id: str,
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    child_orientation_width: int,
    *,
    approximation_error: float = DEFAULT_POLAR_ERROR,
    tolerance: float = 1e-9,
) -> MetricAccessWidthControl:
    """Verify (2)--(7) on an exact finite positive-metric control."""

    if left_metric.shape != right_metric.shape:
        raise ValueError("child metric shape mismatch")
    if len(left_metric.shape) != 2 or left_metric.shape[0] != left_metric.shape[1]:
        raise ValueError("child metrics must be square")
    if child_orientation_width < 2:
        raise ValueError("child_orientation_width must be at least two")
    dimension = left_metric.shape[0]
    identity = np.eye(dimension, dtype=complex)
    left = _hermitian(left_metric)
    right = _hermitian(right_metric)
    parent = _hermitian(left + right)
    parent_values = np.linalg.eigvalsh(parent)
    if float(np.min(parent_values)) <= 100 * tolerance:
        raise ValueError("the parent metric must be positive definite")
    left_values = np.linalg.eigvalsh(left)
    right_values = np.linalg.eigvalsh(right)
    if min(float(np.min(left_values)), float(np.min(right_values))) <= 100 * tolerance:
        raise ValueError("finite controls require positive-definite child metrics")

    left_sqrt = _psd_power(left, 0.5, tolerance)
    right_sqrt = _psd_power(right, 0.5, tolerance)
    left_inverse_sqrt = _psd_power(left, -0.5, tolerance)
    right_inverse_sqrt = _psd_power(right, -0.5, tolerance)
    parent_inverse_sqrt = _psd_power(parent, -0.5, tolerance)
    left_polar = left_sqrt @ left_inverse_sqrt
    right_polar = right_sqrt @ right_inverse_sqrt

    q = child_orientation_width
    w = 2 * q
    left_raw = left_sqrt / math.sqrt(q)
    right_raw = right_sqrt / math.sqrt(q)
    left_composed = left_polar.conj().T @ left_raw
    right_composed = right_polar.conj().T @ right_raw
    signal = np.vstack((left_composed, right_composed)) / math.sqrt(2.0)
    unnormalized_stack = np.vstack((left_sqrt, right_sqrt))
    endpoint = unnormalized_stack @ parent_inverse_sqrt
    singular_left, _, singular_right = np.linalg.svd(signal, full_matrices=False)
    signal_polar = singular_left @ singular_right
    signal_values = np.linalg.svd(signal, compute_uv=False)
    effect = parent_inverse_sqrt @ left @ parent_inverse_sqrt
    endpoint_effect = endpoint[:dimension].conj().T @ endpoint[:dimension]

    native_probability = float(
        np.trace(parent @ signal.conj().T @ signal).real
        / np.trace(parent).real
    )
    native_probability_expected = float(
        np.trace(parent @ parent).real / (w * np.trace(parent).real)
    )
    degree_lower = bernstein_sign_degree_lower_bound(
        float(np.max(signal_values)),
        approximation_error,
    )

    left_polar_residual = float(
        np.linalg.norm(left_polar.conj().T @ left_polar - identity, ord=2)
    )
    right_polar_residual = float(
        np.linalg.norm(right_polar.conj().T @ right_polar - identity, ord=2)
    )
    left_composition_residual = float(
        np.linalg.norm(left_composed - left_sqrt / math.sqrt(q), ord=2)
    )
    right_composition_residual = float(
        np.linalg.norm(right_composed - right_sqrt / math.sqrt(q), ord=2)
    )
    gram_residual = float(
        np.linalg.norm(signal.conj().T @ signal - parent / w, ord=2)
    )
    polar_residual = float(np.linalg.norm(signal_polar - endpoint, ord=2))
    effect_residual = float(np.linalg.norm(endpoint_effect - effect, ord=2))
    native_residual = abs(native_probability - native_probability_expected)
    exact = bool(
        left_polar_residual <= 100 * tolerance
        and right_polar_residual <= 100 * tolerance
        and left_composition_residual <= 100 * tolerance
        and right_composition_residual <= 100 * tolerance
        and gram_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
        and effect_residual <= 100 * tolerance
        and native_residual <= 100 * tolerance
    )
    width_charge = bool(
        float(np.max(signal_values))
        <= math.sqrt(float(np.max(parent_values)) / w) + 100 * tolerance
        and degree_lower > 1.0
        and native_probability <= float(np.max(parent_values)) / w + 100 * tolerance
    )
    verified = exact and width_charge
    return MetricAccessWidthControl(
        control_id=control_id,
        dimension=dimension,
        child_orientation_width=q,
        parent_orientation_width=w,
        parent_minimum_eigenvalue=float(np.min(parent_values)),
        parent_maximum_eigenvalue=float(np.max(parent_values)),
        signal_minimum_singular_value=float(np.min(signal_values)),
        signal_maximum_singular_value=float(np.max(signal_values)),
        native_signal_success_probability=native_probability,
        native_rejection_sampling_factor=1.0 / math.sqrt(native_probability),
        qsvt_polar_error=float(approximation_error),
        bernstein_qsvt_degree_lower_bound=degree_lower,
        left_child_polar_isometry_residual=left_polar_residual,
        right_child_polar_isometry_residual=right_polar_residual,
        left_metric_square_root_composition_residual=left_composition_residual,
        right_metric_square_root_composition_residual=right_composition_residual,
        signal_gram_residual=gram_residual,
        endpoint_polar_residual=polar_residual,
        endpoint_effect_residual=effect_residual,
        native_success_identity_residual=native_residual,
        exact_metric_access_factorization_verified=exact,
        square_root_width_charge_verified=width_charge,
        status=(
            "raw-child-metric-access-sqrt-width-charge-verified"
            if verified
            else "metric-access-width-control-failure"
        ),
    )


def _selected_final_root_parameters(n: int) -> tuple[int, int, int, int, float]:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    information_copies = (order - 1).bit_length()
    selected_copies = information_copies + 2
    q = 1 << (selected_copies - 1)
    return order, information_copies, selected_copies, q, q / order


def natural_metric_access_width_scaling_record(
    n: int,
    *,
    approximation_error: float = DEFAULT_POLAR_ERROR,
) -> NaturalMetricAccessWidthScalingRecord:
    order, information_copies, selected_copies, q, alpha = (
        _selected_final_root_parameters(n)
    )
    w = 2 * q
    signal_minimum = math.sqrt(PARENT_WINDOW_LOWER / w)
    signal_maximum = math.sqrt(PARENT_WINDOW_UPPER / w)
    degree_lower = bernstein_sign_degree_lower_bound(
        signal_maximum,
        approximation_error,
    )
    success = (2.0 * alpha + 1.0) / w
    rejection_factor_log2 = -0.5 * math.log2(success)
    return NaturalMetricAccessWidthScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=information_copies,
        selected_copy_count=selected_copies,
        child_orientation_width_decimal=str(q),
        parent_orientation_width_decimal=str(w),
        child_aspect=alpha,
        retained_signal_minimum_singular_value=signal_minimum,
        retained_signal_maximum_singular_value=signal_maximum,
        limiting_native_signal_success_probability=success,
        native_rejection_sampling_factor_log2=rejection_factor_log2,
        bernstein_qsvt_degree_lower_bound=degree_lower,
        bernstein_qsvt_degree_lower_bound_log2=math.log2(degree_lower),
        raw_metric_access_superpolynomial=True,
        matrix_endpoint_bulk_well_conditioned=True,
        representation_specific_metric_oracle_ruled_out=False,
        status="canonical-final-root-raw-metric-access-superpolynomial",
    )


def _rotated_effect_pair(angle: float = 0.37) -> tuple[np.ndarray, np.ndarray]:
    rotation = np.array(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ],
        dtype=complex,
    )
    left = rotation @ np.diag([0.2, 0.8]) @ rotation.conj().T
    return left, np.eye(2, dtype=complex) - left


def run_final_root_metric_access_width_no_go() -> FinalRootMetricAccessWidthReport:
    rotated_left, rotated_right = _rotated_effect_pair()
    noncommuting_left = np.array([[2.0, 0.4], [0.4, 1.0]], dtype=complex)
    noncommuting_right = np.array(
        [[1.0, -0.2j], [0.2j, 2.5]],
        dtype=complex,
    )
    controls = [
        audit_metric_access_width(
            "known-flat-hadamard-bypass-control",
            0.5 * np.eye(2),
            0.5 * np.eye(2),
            32,
        ),
        audit_metric_access_width(
            "diagonal-matrix-endpoint-control",
            np.diag([0.25, 0.75]),
            np.diag([0.75, 0.25]),
            64,
        ),
        audit_metric_access_width(
            "rotated-unknown-eigenbasis-control",
            rotated_left,
            rotated_right,
            64,
        ),
        audit_metric_access_width(
            "noncommuting-child-metric-control",
            noncommuting_left,
            noncommuting_right,
            64,
        ),
    ]
    scaling = [
        natural_metric_access_width_scaling_record(n)
        for n in (16, 24, 32, 40, 48)
    ]
    failures = sum(row.status.endswith("failure") for row in controls)
    verified = failures == 0
    tail = scaling[-1]
    theorem = FinalRootMetricAccessWidthTheorem(
        raw_child_interface=(
            "Each q-leaf child PREPARE/SELECT interface exposes R_s/sqrt(q)."
        ),
        child_polar_composition=(
            "The compiled child polar gives Q_s^*R_s/sqrt(q)=sqrt(A_s)/sqrt(q) exactly."
        ),
        binary_node_signal=(
            "A binary branch LCU exposes T=[sqrt(A);sqrt(B)]/sqrt(w), w=2q, with T^*T=(A+B)/w."
        ),
        exact_endpoint_polar=(
            "polar(T)=[sqrt(A);sqrt(B)](A+B)^-1/2 and its left effect is C=(A+B)^-1/2 A (A+B)^-1/2."
        ),
        retained_signal_window=(
            "The fixed parent trim 0.5I<=A+B<=16I becomes singular window [sqrt(0.5/w),4/sqrt(w)] for T."
        ),
        qsvt_degree_lower_bound=(
            "Bernstein's inequality forces every bounded QSVT polar polynomial of constant error to have degree Omega(sqrt(w))."
        ),
        native_success_probability=(
            "On rho proportional to S, raw signal selection succeeds with Tr(S^2)/(w Tr(S))."
        ),
        natural_scaling=(
            "The natural free-MP sibling law gives success (2alpha+1+o(1))/w with alpha in [2,4] and w=Theta(n!)."
        ),
        physical_relevance=(
            "The trace-weighted PGM bridge identifies the same native state weighting with physical sector-average polar mass."
        ),
        surviving_target=(
            "A representation-specific metric-magnitude oracle or direct matrix-POVM Naimark dilation that does not first expose the uniformly normalized raw analysis signal."
        ),
        scope=(
            "A lower bound for the canonical raw-analysis/child-polar/binary-LCU/QSVT or rejection-sampling access architecture, not for arbitrary structured circuits or the PGM itself."
        ),
        theorem_verified=verified,
        status=(
            "final-root-canonical-metric-access-sqrt-width-falsified"
            if verified
            else "final-root-metric-access-width-validation-failure"
        ),
    )
    return FinalRootMetricAccessWidthReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "Compiled child polars convert normalized raw child-frame access into a polynomially normalized final-root metric oracle, after which the constant Jacobi bulk edge makes the matrix endpoint efficient."
            ),
            "verdict": "falsified-for-canonical-raw-access-composition",
            "assumptions": [
                "Uniform q-leaf PREPARE/SELECT child analyses R_s/sqrt(q).",
                "Exact compiled child polar circuits Q_s.",
                "Binary LCU stacking followed by generic QSVT polar extraction or black-box quantum rejection sampling.",
                "The existing final-root parent trim 0.5I<=S<=16I on all but o(1) annealed native mass.",
            ],
            "normalization": (
                "The exact binary signal is [sqrt(A);sqrt(B)]/sqrt(w) with total parent width w=2q."
            ),
            "failure_modes": [
                "A known flat endpoint can be implemented directly without querying the suppressed raw signal.",
                "The theorem does not cover a new representation-specific oracle exposing positive metrics at constant normalization.",
                "The theorem does not exclude direct POVM state preparation or nonlinear structure outside the black-box signal model.",
                "Earlier nodes may have additional algebraic cancellations not present in this final-root composition.",
            ],
            "success_criterion": (
                "A polynomial compiler required inverse-polynomial signal singular values or subpolynomial-degree polar extraction; the exact signal has Theta(w^-1/2) singular values and Omega(sqrt(w)) degree."
            ),
            "speedup_claim_allowed": False,
        },
        theorem=theorem,
        exact_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_child_polar_metric_signal",
                "resolved": verified,
                "evidence": (
                    "Q_s^*R_s/sqrt(q)=sqrt(A_s)/sqrt(q), and binary stacking gives T^*T=S/w exactly in every control."
                ),
            },
            {
                "obligation": "recover_exact_matrix_endpoint_as_signal_polar",
                "resolved": verified,
                "evidence": (
                    "The finite SVD polar agrees with [sqrt(A);sqrt(B)]S^-1/2 and reproduces C as its left effect."
                ),
            },
            {
                "obligation": "charge_generic_qsvt_polar_degree",
                "resolved": True,
                "evidence": (
                    "Mean value plus Bernstein bounds a bounded sign polynomial by degree Omega(1/sigma); sigma<=4/sqrt(w) on the retained window."
                ),
            },
            {
                "obligation": "charge_native_black_box_success",
                "resolved": True,
                "evidence": (
                    "The exact success identity is Tr(S^2)/(wTr(S)); joint free-MP moments give coefficient 2alpha+1."
                ),
            },
            {
                "obligation": "construct_representation_specific_metric_magnitude_oracle",
                "resolved": False,
                "evidence": (
                    "No circuit bypassing normalized raw analysis is known. Child polars and GPE support transports discard the required positive magnitude."
                ),
            },
            {
                "obligation": "propagate_metric_access_through_all_tree_levels",
                "resolved": False,
                "evidence": "Only the selected final-root composition is covered.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The common factor 1/sqrt(w) cancels algebraically in the polar.",
                "resolved": True,
                "resolution": (
                    "It cancels in the mathematical polar but remains the queried signal amplitude. QSVT must transform values at +-Theta(w^-1/2), forcing Omega(sqrt(w)) degree."
                ),
            },
            {
                "objection": "The constant Jacobi edge makes raw metric access efficient.",
                "resolved": True,
                "resolution": (
                    "The edge is constant for C and unnormalized S. The available signal is S/w, whose singular scale is still w^-1/2."
                ),
            },
            {
                "objection": "Only exponentially small bad modes cause the charge.",
                "resolved": True,
                "resolution": (
                    "False. Every retained singular value is at most 4/sqrt(w); even a perfectly flat retained frame has the same access suppression."
                ),
            },
            {
                "objection": "The flat Hadamard control proves the endpoint itself is hard.",
                "resolved": True,
                "resolution": (
                    "False. A known Hadamard is direct. The control proves only that the specified black-box raw-signal extraction wastes sqrt(w) queries."
                ),
            },
            {
                "objection": "This rules out every representation-specific metric compiler.",
                "resolved": False,
                "resolution": (
                    "A direct structured Naimark dilation or new constant-normalization metric oracle lies outside the access model."
                ),
            },
        ],
        primary_literature=[
            {
                "paper_id": QSVT_PAPER_ID,
                "url": QSVT_PAPER_URL,
                "scope": (
                    "Bounded polynomial singular-value transformation and query-degree correspondence."
                ),
            },
            {
                "paper_id": QRS_PAPER_ID,
                "url": QRS_PAPER_URL,
                "scope": (
                    "Tight black-box query complexity for coherent amplitude/state resampling."
                ),
            },
        ],
        headline_metrics={
            "exact_final_root_metric_signal_factorization_count": int(verified),
            "canonical_raw_metric_qsvt_sqrt_width_no_go_count": int(verified),
            "native_raw_metric_success_inverse_width_theorem_count": int(verified),
            "exact_control_count": len(controls),
            "exact_control_failure_count": failures,
            "tail_qsvt_degree_lower_bound_log2": (
                tail.bernstein_qsvt_degree_lower_bound_log2
            ),
            "tail_native_rejection_sampling_factor_log2": (
                tail.native_rejection_sampling_factor_log2
            ),
            "representation_specific_metric_oracle_count": 0,
            "direct_matrix_povm_dilation_count": 0,
            "all_depth_metric_access_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "child_polar_recovers_metric_sqrt_at_raw_normalization": verified,
            "exact_final_root_endpoint_is_polar_of_binary_metric_signal": verified,
            "retained_endpoint_matrix_bulk_has_constant_edge": True,
            "retained_raw_metric_signal_has_inverse_sqrt_width_scale": verified,
            "generic_qsvt_polar_requires_sqrt_width_degree": verified,
            "native_raw_metric_selection_probability_is_inverse_width": verified,
            "canonical_raw_child_metric_access_is_polynomial": False,
            "representation_specific_metric_magnitude_oracle_proved": False,
            "direct_matrix_povm_naimark_dilation_proved": False,
            "arbitrary_hierarchical_global_polar_ruled_out": False,
            "all_depth_metric_access_compiler_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Child polars expose sqrt(A_s) only through the inherited R_s/sqrt(q) signal. Binary stacking exactly recovers the desired endpoint polar but leaves all retained signal singular values Theta(w^-1/2), forcing Omega(sqrt(w)) generic QSVT or rejection-sampling cost at w=Theta(n!)."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact final-root metric signal from raw child analyses and compiled child polars, then proved that its inherited square-root-width normalization makes generic QSVT and black-box state conversion superpolynomial despite the constant Jacobi endpoint edge."
        ),
        falsifiers_triggered=[
            "Algebraic cancellation of a common normalization in the polar does not cancel its query complexity.",
            "A binary hierarchical merge does not erase the square-root width already present inside each normalized child analysis.",
            "The constant free-Jacobi endpoint edge does not make the canonically exposed S/w signal inverse-polynomial.",
            "Compiled child polars plus raw child PREPARE/SELECT do not provide polynomial final-root metric access through generic QSVT or rejection sampling.",
        ],
    )


def write_final_root_metric_access_width_no_go_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_metric_access_width_no_go())
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
                title="Final-root metric-access width no-go",
                status="completed-negative-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Compose normalized raw child analyses with exact child polars, derive the binary endpoint signal and its native success identity, apply Bernstein's bounded-polynomial lower bound and quantum rejection sampling, and verify flat, diagonal, rotated, and noncommuting metric controls."
                ),
                positive_signal=(
                    "A polynomial-normalization final-root matrix-effect oracle obtained from raw child PREPARE/SELECT plus compiled child polars."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_native_frame_access_boundary.py",
                    "self_dual_wreath_gpe_recursive_node_compiler.py",
                    "self_dual_wreath_final_root_relative_jacobi_transfer.py",
                    "self_dual_wreath_final_root_scalar_mixer_no_go.py",
                ],
                next_actions=[
                    "Search only for representation-specific metric-magnitude preparation or direct matrix-POVM Naimark dilation that bypasses normalized raw child analysis; do not reapply generic QSVT to S/w."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Exact child polars convert normalized raw child analyses into polynomially usable final-root metric access because the common 1/sqrt(w) factor cancels from the endpoint polar."
                ),
                reason_invalid=(
                    "The factor cancels algebraically but not operationally. The exact signal T has T^*T=S/w; on the retained parent window all singular values are O(w^-1/2), so bounded QSVT polar degree and black-box state-conversion queries are Omega(sqrt(w)) with w=Theta(n!)."
                ),
                lesson=(
                    "Do not feed the normalized raw child analysis back through generic polar extraction. A viable hierarchy now requires representation-specific positive-metric preparation or a direct matrix-POVM Naimark dilation at constant/inverse-polynomial normalization."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "exact_binary_metric_signal": (
                        "T=[sqrt(A);sqrt(B)]/sqrt(w), T^*T=(A+B)/w"
                    ),
                    "retained_signal_singular_scale": "Theta(w^-1/2)",
                    "qsvt_degree_lower_bound": "Omega(sqrt(w))",
                    "native_signal_success_probability": (
                        "(2alpha+1+o(1))/w"
                    ),
                    "parent_width": "Theta(n!)",
                    "representation_specific_metric_oracle_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_metric_access_width_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
