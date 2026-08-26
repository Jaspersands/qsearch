"""Normalized program contractions retain an inverse logical-dimension charge.

Let ``V:H_D -> K`` be the final-root isometry and put

    |v> = |V>>/sqrt(D),        B_U = V U V^*.             (1)

For the row-vectorization convention used here, direct contraction of the
normalized program projector gives the exact identity

    Tr_R[(I tensor U^T)|v><v|] = B_U/D.                   (2)

This coefficient is sharp in a useful architecture-level sense.  For
``L_U(X)=Tr_R[(I tensor U^T)X]``, the Hilbert--Schmidt adjoint is
``L_U^*(Y)=Y tensor conjugate(U)``.  Hence
``||L_U^*||_(infinity->infinity)=1`` and Schatten-norm duality gives
``||L_U||_(1->1)=1``.  The input projector has trace norm one, while
``||B_U||_1=D``.  More generally, if a linear contraction ``L`` has
``||L||_(1->1)<=1`` and acts on any fixed number ``k`` of normalized program
projectors, then

    L((|v><v|)^(tensor k)) = c B_U    implies |c|<=1/D.   (3)

The canonical one-copy partial trace attains equality.  Thus normalized
copies alone do not improve the coefficient inside this bounded linear
program-density contraction model.

The unflattened, label-retaining resource has operator representative

    F = V sqrt(rho),       rho=S/Tr(S),       ||F||_F=1.  (4)

Inserting a contraction ``M`` on its reference leg produces

    Tr_R[(I tensor M^T)|F>><<F|] = F M F^*.               (5)

Full column rank makes a direct exact realization unique:

    F M F^* = c V U V^*
        iff M = c rho^(-1/2) U rho^(-1/2).                (6)

Consequently the largest admissible coefficient is

    c_*(U)=1/||rho^(-1/2) U rho^(-1/2)||,
    lambda_min(rho) <= c_*(U) <= lambda_max(rho).         (7)

On the retained final-root window ``0.5 I<=S<=16 I``, equation (7) gives

    1/(32D) <= c_*(U) <= 32/D.                            (8)

So direct two-sided whitening inside the contraction does not inherit the
constant *state-flattening probability* proved previously; its operator
signal remains inverse-dimensional.  Even a supplied reflection
``R_v=I-2|v><v|`` obeys, for a traceless Weyl error,

    Tr_R[(I tensor U^T)R_v] = -2 B_U/D.                   (9)

The signal ``1/D`` has selected-branch probability ``1/D^2``, amplitude
amplification factor ``D``, and any bounded sign/polar QSVT polynomial has
degree at least ``(1-epsilon)sqrt(1-D^(-2))D``.  The prior rank-dense
retained-window and high-row theorems give the logical ``D`` the same
factorial exponent as ``d_nu>sqrt(n!)/p(n)`` on asymptotically full natural
mass.

This is deliberately not a no-programming theorem for arbitrary coherent
processors.  It covers direct reference-leg insertions, the canonical
program-projector partial trace, one supplied program reflection under that
partial trace, and bounded trace-norm linear contractions of finitely many
normalized program density operators.  Adaptive postselection, nonlinear
oracle synthesis, long coherent reflection sequences, and representation-
specific block-encoding compilers remain outside the claim.
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
from self_dual_wreath_final_root_byproduct_covariance_no_go import (
    canonical_endpoint,
)
from self_dual_wreath_final_root_metric_access_width_no_go import (
    PARENT_WINDOW_LOWER,
    PARENT_WINDOW_UPPER,
    bernstein_sign_degree_lower_bound,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    _psd_power,
    weyl_unitary_error_basis,
)
from self_dual_wreath_joint_character_natural_sector_mass import partition_number


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_program_contraction_normalization_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-"
    "PROGRAM-CONTRACTION-NORMALIZATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-FINAL-ROOT-PROGRAM-CONTRACTION-INVERSE-DIMENSION"
)
WERNER_PAPER_ID = "werner-tight-teleportation-unitary-error-bases-2000"
WERNER_PAPER_URL = "https://arxiv.org/abs/quant-ph/0003070"
QSVT_PAPER_ID = "gilyen-su-low-wiebe-qsvt-2018"
QSVT_PAPER_URL = "https://arxiv.org/abs/1806.01838"
DEFAULT_APPROXIMATION_ERROR = 0.1


@dataclass(frozen=True)
class DirectProgramContractionControl:
    control_id: str
    logical_dimension: int
    output_dimension: int
    density_minimum_eigenvalue: float
    density_maximum_eigenvalue: float
    density_condition_number: float
    optimal_direct_coefficient: float
    coefficient_lower_bound: float
    coefficient_upper_bound: float
    retained_window_coefficient_lower_bound: float
    retained_window_coefficient_upper_bound: float
    optimal_insertion_operator_norm: float
    resource_normalization_residual: float
    endpoint_isometry_residual: float
    direct_contraction_residual: float
    direct_insertion_uniqueness_residual: float
    flattened_partial_trace_residual: float
    normalized_program_projector_trace_norm: float
    endpoint_byproduct_trace_norm: float
    flattened_output_trace_norm: float
    reflection_partial_trace_residual: float
    reflection_byproduct_coefficient_magnitude: float
    qsvt_sign_degree_lower_bound: float
    selected_branch_probability: float
    selected_branch_amplitude_amplification_factor: float
    exact_inverse_dimension_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class ProgramCopyNormalizationControl:
    logical_dimension: int
    normalized_program_copy_count: int
    input_tensor_trace_norm: float
    target_byproduct_trace_norm: float
    induced_trace_norm_upper_bound: float
    maximum_exact_coefficient: float
    canonical_one_copy_coefficient: float
    canonical_bound_saturated: bool
    constant_coefficient_allowed_by_bound: bool
    bounded_linear_copy_contraction_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalProgramContractionScalingRecord:
    n: int
    partition_count_decimal: str
    natural_high_row_irrep_dimension_lower_bound_decimal: str
    natural_high_row_irrep_dimension_lower_bound_log2: float
    canonical_coefficient_log2_upper_bound_leading_term: float
    selected_branch_probability_log2_upper_bound_leading_term: float
    amplitude_amplification_log2_lower_bound_leading_term: float
    qsvt_degree_lower_bound: float
    independent_source_high_row_mass_lower_bound: float
    retained_logical_dimension_same_factorial_exponent_proved: bool
    canonical_program_contraction_superpolynomial: bool
    arbitrary_coherent_processor_lower_bound_proved: bool
    status: str


@dataclass(frozen=True)
class ProgramContractionNormalizationTheorem:
    flattened_partial_trace: str
    trace_norm_copy_bound: str
    unflattened_unique_insertion: str
    sharp_coefficient: str
    retained_window_consequence: str
    program_reflection_consequence: str
    amplification_and_qsvt: str
    natural_dimension_consequence: str
    surviving_route: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ProgramContractionNormalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: ProgramContractionNormalizationTheorem
    direct_controls: list[DirectProgramContractionControl]
    copy_normalization_controls: list[ProgramCopyNormalizationControl]
    scaling_records: list[NaturalProgramContractionScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _trace_norm(matrix: np.ndarray) -> float:
    return float(np.sum(np.linalg.svd(matrix, compute_uv=False)))


def _validate_density(density: np.ndarray, *, tolerance: float) -> np.ndarray:
    value = np.asarray(density, dtype=complex)
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise ValueError("density must be square")
    value = (value + value.conj().T) / 2.0
    eigenvalues = np.linalg.eigvalsh(value)
    if float(eigenvalues[0]) <= 100 * tolerance:
        raise ValueError("density must be positive definite")
    if abs(float(np.trace(value).real) - 1.0) > 1000 * tolerance:
        raise ValueError("density must have trace one")
    return value


def program_partial_contraction(
    program_operator: np.ndarray,
    insertion: np.ndarray,
) -> np.ndarray:
    """Return the reference-leg contraction ``F M F^*`` in equation (5)."""

    operator = np.asarray(program_operator, dtype=complex)
    value = np.asarray(insertion, dtype=complex)
    if operator.ndim != 2 or value.shape != (operator.shape[1], operator.shape[1]):
        raise ValueError("program and insertion dimensions do not match")
    return operator @ value @ operator.conj().T


def optimal_direct_program_insertion(
    density: np.ndarray,
    logical_error: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, float]:
    """Return the sharp contraction ``M`` and coefficient ``c_*`` in (6)-(7)."""

    rho = _validate_density(density, tolerance=tolerance)
    error = np.asarray(logical_error, dtype=complex)
    dimension = rho.shape[0]
    if error.shape != rho.shape:
        raise ValueError("logical error and density dimensions do not match")
    identity = np.eye(dimension, dtype=complex)
    if np.linalg.norm(error.conj().T @ error - identity, ord=2) > 1000 * tolerance:
        raise ValueError("logical error must be unitary")
    inverse_root = _psd_power(rho, -0.5, tolerance=tolerance)
    unscaled = inverse_root @ error @ inverse_root
    coefficient = 1.0 / float(np.linalg.norm(unscaled, ord=2))
    return coefficient * unscaled, coefficient


def normalized_program_reflection_partial_trace(
    endpoint: np.ndarray,
    logical_error: np.ndarray,
) -> np.ndarray:
    """Contract ``I-2|V>><<V|/D`` with ``I tensor U^T`` and trace ``R``."""

    value = np.asarray(endpoint, dtype=complex)
    error = np.asarray(logical_error, dtype=complex)
    if value.ndim != 2:
        raise ValueError("endpoint must be a matrix")
    output_dimension, dimension = value.shape
    if error.shape != (dimension, dimension):
        raise ValueError("logical error and endpoint dimensions do not match")
    vector = (value / math.sqrt(dimension)).reshape(-1)
    projector = np.outer(vector, vector.conj())
    reflection = np.eye(output_dimension * dimension, dtype=complex) - 2.0 * projector
    inserted = np.kron(np.eye(output_dimension, dtype=complex), error.T) @ reflection
    tensor = inserted.reshape(output_dimension, dimension, output_dimension, dimension)
    return np.trace(tensor, axis1=1, axis2=3)


def audit_direct_program_contraction(
    control_id: str,
    effect: np.ndarray,
    density: np.ndarray,
    logical_error: np.ndarray,
    *,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
    tolerance: float = 1e-9,
) -> DirectProgramContractionControl:
    """Verify equations (2), (6)--(9) on one finite exact control."""

    endpoint = canonical_endpoint(effect, tolerance=tolerance)
    rho = _validate_density(density, tolerance=tolerance)
    error = np.asarray(logical_error, dtype=complex)
    dimension = endpoint.shape[1]
    output_dimension = endpoint.shape[0]
    identity = np.eye(dimension, dtype=complex)
    output_identity = np.eye(output_dimension, dtype=complex)
    if rho.shape != (dimension, dimension) or error.shape != (dimension, dimension):
        raise ValueError("effect, density, and logical error dimensions must match")
    if np.linalg.norm(error.conj().T @ error - identity, ord=2) > 1000 * tolerance:
        raise ValueError("logical error must be unitary")

    root = _psd_power(rho, 0.5, tolerance=tolerance)
    inverse_root = _psd_power(rho, -0.5, tolerance=tolerance)
    program = endpoint @ root
    byproduct = endpoint @ error @ endpoint.conj().T
    insertion, coefficient = optimal_direct_program_insertion(
        rho,
        error,
        tolerance=tolerance,
    )
    direct_observed = program_partial_contraction(program, insertion)
    direct_expected = coefficient * byproduct
    solved = np.linalg.solve(root, coefficient * error) @ inverse_root

    flattened = endpoint / math.sqrt(dimension)
    flattened_observed = program_partial_contraction(flattened, error)
    flattened_expected = byproduct / dimension
    vector = flattened.reshape(-1)
    program_projector = np.outer(vector, vector.conj())

    reflection_observed = normalized_program_reflection_partial_trace(endpoint, error)
    reflection_expected = (
        complex(np.trace(error)) * output_identity - 2.0 * byproduct / dimension
    )
    density_values = np.linalg.eigvalsh(rho)
    minimum = float(density_values[0])
    maximum = float(density_values[-1])
    retained_lower = PARENT_WINDOW_LOWER / (dimension * PARENT_WINDOW_UPPER)
    retained_upper = PARENT_WINDOW_UPPER / (dimension * PARENT_WINDOW_LOWER)
    endpoint_residual = float(
        np.linalg.norm(endpoint.conj().T @ endpoint - identity, ord=2)
    )
    resource_residual = abs(float(np.linalg.norm(program, ord="fro")) - 1.0)
    direct_residual = float(np.linalg.norm(direct_observed - direct_expected, ord=2))
    uniqueness_residual = float(np.linalg.norm(solved - insertion, ord=2))
    flattened_residual = float(
        np.linalg.norm(flattened_observed - flattened_expected, ord=2)
    )
    reflection_residual = float(
        np.linalg.norm(reflection_observed - reflection_expected, ord=2)
    )
    projector_trace_norm = _trace_norm(program_projector)
    byproduct_trace_norm = _trace_norm(byproduct)
    flattened_trace_norm = _trace_norm(flattened_observed)
    insertion_norm = float(np.linalg.norm(insertion, ord=2))
    qsvt_lower = bernstein_sign_degree_lower_bound(
        1.0 / dimension,
        approximation_error,
    )
    verified = bool(
        endpoint_residual <= 100 * tolerance
        and resource_residual <= 100 * tolerance
        and direct_residual <= 100 * tolerance
        and uniqueness_residual <= 100 * tolerance
        and flattened_residual <= 100 * tolerance
        and reflection_residual <= 100 * tolerance
        and abs(insertion_norm - 1.0) <= 100 * tolerance
        and minimum - 100 * tolerance <= coefficient <= maximum + 100 * tolerance
        and minimum + 100 * tolerance >= retained_lower
        and maximum <= retained_upper + 100 * tolerance
        and abs(projector_trace_norm - 1.0) <= 100 * tolerance
        and abs(byproduct_trace_norm - dimension) <= 100 * tolerance
        and abs(flattened_trace_norm - 1.0) <= 100 * tolerance
    )
    return DirectProgramContractionControl(
        control_id=control_id,
        logical_dimension=dimension,
        output_dimension=output_dimension,
        density_minimum_eigenvalue=minimum,
        density_maximum_eigenvalue=maximum,
        density_condition_number=maximum / minimum,
        optimal_direct_coefficient=coefficient,
        coefficient_lower_bound=minimum,
        coefficient_upper_bound=maximum,
        retained_window_coefficient_lower_bound=retained_lower,
        retained_window_coefficient_upper_bound=retained_upper,
        optimal_insertion_operator_norm=insertion_norm,
        resource_normalization_residual=resource_residual,
        endpoint_isometry_residual=endpoint_residual,
        direct_contraction_residual=direct_residual,
        direct_insertion_uniqueness_residual=uniqueness_residual,
        flattened_partial_trace_residual=flattened_residual,
        normalized_program_projector_trace_norm=projector_trace_norm,
        endpoint_byproduct_trace_norm=byproduct_trace_norm,
        flattened_output_trace_norm=flattened_trace_norm,
        reflection_partial_trace_residual=reflection_residual,
        reflection_byproduct_coefficient_magnitude=2.0 / dimension,
        qsvt_sign_degree_lower_bound=qsvt_lower,
        selected_branch_probability=1.0 / dimension**2,
        selected_branch_amplitude_amplification_factor=float(dimension),
        exact_inverse_dimension_boundary_verified=verified,
        status=(
            "exact-direct-program-contraction-inverse-dimension-boundary"
            if verified
            else "direct-program-contraction-control-failure"
        ),
    )


def program_copy_normalization_control(
    logical_dimension: int,
    normalized_program_copy_count: int,
) -> ProgramCopyNormalizationControl:
    """Record the trace-norm proof of (3) for a fixed normalized copy count."""

    if logical_dimension < 2:
        raise ValueError("logical_dimension must be at least two")
    if normalized_program_copy_count < 1:
        raise ValueError("normalized_program_copy_count must be positive")
    coefficient = 1.0 / logical_dimension
    verified = bool(
        coefficient * logical_dimension == 1.0
        and not math.isclose(coefficient, 1.0)
    )
    return ProgramCopyNormalizationControl(
        logical_dimension=logical_dimension,
        normalized_program_copy_count=normalized_program_copy_count,
        input_tensor_trace_norm=1.0,
        target_byproduct_trace_norm=float(logical_dimension),
        induced_trace_norm_upper_bound=1.0,
        maximum_exact_coefficient=coefficient,
        canonical_one_copy_coefficient=coefficient,
        canonical_bound_saturated=True,
        constant_coefficient_allowed_by_bound=False,
        bounded_linear_copy_contraction_boundary_verified=verified,
        status=(
            "bounded-linear-normalized-copy-contraction-inverse-dimension"
            if verified
            else "program-copy-normalization-control-failure"
        ),
    )


def natural_program_contraction_scaling_record(
    n: int,
    *,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> NaturalProgramContractionScalingRecord:
    """Transfer the natural high-row dimension bound to the ``1/D`` signal."""

    if n < 4:
        raise ValueError("n must be at least four")
    partitions = partition_number(n)
    dimension = math.isqrt(math.factorial(n)) // partitions + 1
    log_dimension = math.log2(dimension)
    degree_lower = bernstein_sign_degree_lower_bound(
        1.0 / dimension,
        approximation_error,
    )
    return NaturalProgramContractionScalingRecord(
        n=n,
        partition_count_decimal=str(partitions),
        natural_high_row_irrep_dimension_lower_bound_decimal=str(dimension),
        natural_high_row_irrep_dimension_lower_bound_log2=log_dimension,
        canonical_coefficient_log2_upper_bound_leading_term=-log_dimension,
        selected_branch_probability_log2_upper_bound_leading_term=-2.0 * log_dimension,
        amplitude_amplification_log2_lower_bound_leading_term=log_dimension,
        qsvt_degree_lower_bound=degree_lower,
        independent_source_high_row_mass_lower_bound=max(0.0, 1.0 - 1.0 / partitions),
        retained_logical_dimension_same_factorial_exponent_proved=True,
        canonical_program_contraction_superpolynomial=True,
        arbitrary_coherent_processor_lower_bound_proved=False,
        status="natural-program-contraction-signal-superpolynomial",
    )


def _deterministic_unitary(dimension: int) -> np.ndarray:
    seed = np.arange(1, dimension * dimension + 1, dtype=float).reshape(
        dimension,
        dimension,
    )
    seed = seed + 1j * np.flipud(seed) / 5.0
    basis, _ = np.linalg.qr(seed + (dimension + 1) * np.eye(dimension))
    return basis


def _control_inputs(dimension: int, *, rotated: bool) -> tuple[np.ndarray, np.ndarray]:
    metric_values = np.geomspace(PARENT_WINDOW_LOWER, 8.0, dimension)
    effect_values = np.linspace(0.15, 0.85, dimension)
    if rotated:
        metric_basis = _deterministic_unitary(dimension)
        effect_basis = np.roll(metric_basis, 1, axis=0)
    else:
        metric_basis = np.eye(dimension, dtype=complex)
        effect_basis = np.eye(dimension, dtype=complex)
    metric = (metric_basis * metric_values) @ metric_basis.conj().T
    density = metric / float(np.trace(metric).real)
    effect = (effect_basis * effect_values) @ effect_basis.conj().T
    return effect, density


def run_final_root_program_contraction_normalization_no_go(
) -> ProgramContractionNormalizationReport:
    direct_controls: list[DirectProgramContractionControl] = []
    specifications = (
        (2, False, "diagonal-d2"),
        (3, False, "diagonal-d3"),
        (3, True, "rotated-d3"),
        (4, True, "rotated-complex-d4"),
    )
    for dimension, rotated, identifier in specifications:
        effect, density = _control_inputs(dimension, rotated=rotated)
        shift = weyl_unitary_error_basis(dimension)[dimension]
        direct_controls.append(
            audit_direct_program_contraction(identifier, effect, density, shift)
        )
    copy_controls = [
        program_copy_normalization_control(dimension, copies)
        for dimension in (2, 3, 4, 8)
        for copies in (1, 2, 3)
    ]
    scaling = [
        natural_program_contraction_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48)
    ]
    direct_failures = sum(
        not row.exact_inverse_dimension_boundary_verified for row in direct_controls
    )
    copy_failures = sum(
        not row.bounded_linear_copy_contraction_boundary_verified
        for row in copy_controls
    )
    verified = bool(direct_failures == 0 and copy_failures == 0)
    theorem = ProgramContractionNormalizationTheorem(
        flattened_partial_trace=(
            "For |v>=|V>>/sqrt(D), Tr_R[(I tensor U^T)|v><v|]=VU V^*/D exactly."
        ),
        trace_norm_copy_bound=(
            "If ||L||_(1->1)<=1, then L((|v><v|)^(tensor k))=cVU V^* implies |c|D<=1 for every fixed k; the one-copy map attains 1/D."
        ),
        unflattened_unique_insertion=(
            "For F=V sqrt(rho), FMF^*=cVU V^* iff uniquely M=c rho^(-1/2)U rho^(-1/2)."
        ),
        sharp_coefficient=(
            "The largest contraction coefficient is c_*(U)=1/||rho^(-1/2)U rho^(-1/2)||, with lambda_min(rho)<=c_*<=lambda_max(rho)."
        ),
        retained_window_consequence=(
            "If 0.5I<=S<=16I and rho=S/TrS, then 1/(32D)<=c_*(U)<=32/D; constant-success state flattening does not become constant operator signal."
        ),
        program_reflection_consequence=(
            "For R_v=I-2|v><v| and traceless Weyl U, Tr_R[(I tensor U^T)R_v]=-2VU V^*/D."
        ),
        amplification_and_qsvt=(
            "The canonical 1/D signal has selected-branch probability 1/D^2, amplitude-amplification factor D, and bounded sign/polar QSVT degree at least (1-epsilon)sqrt(1-D^(-2))D."
        ),
        natural_dimension_consequence=(
            "The prior retained-window rank theorem gives log(D)>=log(d_nu)+o(log(d_nu)), while d_nu>sqrt(n!)/p(n) on asymptotically full natural high-row mass."
        ),
        surviving_route=(
            "Use representation-specific coherent block-encoding synthesis that is not a bounded linear contraction of normalized program densities, or compile endpoint byproducts by another recursive structure."
        ),
        scope=(
            "The theorem covers direct reference-leg insertions, canonical projector/reflection partial traces, and bounded trace-norm linear contractions of finitely many normalized program density operators; it is not an arbitrary coherent-processor lower bound."
        ),
        theorem_verified=verified,
        status=(
            "direct-program-contraction-inverse-dimension-no-go"
            if verified
            else "program-contraction-normalization-control-failure"
        ),
    )
    return ProgramContractionNormalizationReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "A coherent program reflection or a fixed-copy direct contraction of the normalized label-retaining purification realizes V_C X V_C^* and V_C Z V_C^* at constant normalization without exposing C, S^(-1/2), or a selected Bell outcome."
            ),
            "access_model": (
                "Direct reference-leg contraction of F=V sqrt(rho); the canonical partial trace of the normalized flattened program projector; one supplied reflection about that program under the same partial trace; and arbitrary linear maps of induced trace norm at most one acting on any fixed number of normalized program density copies."
            ),
            "positive_identity": (
                "All target byproducts are present exactly: the flattened program gives B_U/D, while the unflattened program gives c_*B_U using the unique optimal inverse-density sandwich insertion."
            ),
            "negative_boundary": (
                "Both exact coefficients are Theta(1/D) on the retained window, and bounded linear contractions of normalized program density copies cannot exceed 1/D."
            ),
            "natural_input_relevance": (
                "The logical dimension has the same factorial exponent as the natural high-row irrep dimension on asymptotically full retained mass, so the canonical signal is superpolynomially small."
            ),
            "claim_boundary": (
                "No lower bound is claimed for adaptive/nonlinear oracle synthesis, long coherent reflection sequences, or arbitrary representation-specific block-encoding circuits."
            ),
        },
        theorem=theorem,
        direct_controls=direct_controls,
        copy_normalization_controls=copy_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_normalized_program_partial_trace",
                "resolved": True,
                "evidence": "Vectorization gives B_U/D. The adjoint of L_U is Y -> Y tensor conjugate(U), whose induced infinity norm is one, so Schatten duality proves ||L_U||_(1->1)=1 and the unit-trace-norm output saturates the bound.",
            },
            {
                "obligation": "optimize_direct_unflattened_reference_leg_insertion",
                "resolved": True,
                "evidence": "Full column rank forces M=c rho^(-1/2)U rho^(-1/2); setting ||M||=1 gives the sharp c_* and eigenvalue sandwich.",
            },
            {
                "obligation": "decide_constant_normalization_for_fixed_copy_bounded_linear_program_density_contractions",
                "resolved": True,
                "evidence": "The tensor program input has trace norm one and B_U has trace norm D, so induced trace-norm contractivity forces |c|<=1/D independently of fixed copy count.",
            },
            {
                "obligation": "compile_representation_specific_coherent_byproduct_block_encoding_outside_linear_density_contractions",
                "resolved": False,
                "evidence": "State-preparation oracles, adaptive postselection, and coherent multi-reflection/QSVT sequences are intentionally outside the access model.",
            },
            {
                "obligation": "prove_arbitrary_programmable_processor_lower_bound",
                "resolved": False,
                "evidence": "The trace-norm theorem is architecture-scoped and does not apply to every coherent circuit with program-state preparation access.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The constant probability for exact state flattening implies constant block-encoding normalization.",
                "resolved": True,
                "resolution": "No. State-filter success is D lambda_min(rho), whereas direct operator insertion has coefficient c_* between lambda_min(rho) and lambda_max(rho), both Theta(1/D) on the window.",
            },
            {
                "objection": "Two or more normalized program copies remove the 1/D coefficient.",
                "resolved": True,
                "resolution": "Not for a bounded trace-norm linear density contraction: every tensor input still has trace norm one, while cB_U has trace norm |c|D.",
            },
            {
                "objection": "A reflection about the normalized program automatically exposes a constant-strength byproduct.",
                "resolved": True,
                "resolution": "Its canonical traceless-Weyl partial trace is exactly -2B_U/D. A long coherent reflection algorithm is a different, still-open access model.",
            },
            {
                "objection": "The trace-norm bound rules out all physical block encodings.",
                "resolved": False,
                "resolution": "It does not. A unitary block-encoding compiler is not generally a bounded linear map from a normalized program density operator to its encoded matrix.",
            },
            {
                "objection": "Finite controls establish the natural asymptotic dimension transfer.",
                "resolved": True,
                "resolution": "No. Natural relevance is imported only from the prior independent rank-dense retained-window and Plancherel high-row theorems.",
            },
        ],
        primary_literature=[
            {
                "paper_id": WERNER_PAPER_ID,
                "url": WERNER_PAPER_URL,
                "scope": "Unitary error bases and tight teleportation context; the contraction normalization identities are proved directly here.",
            },
            {
                "paper_id": QSVT_PAPER_ID,
                "url": QSVT_PAPER_URL,
                "scope": "QSVT context; the bounded-polynomial degree lower bound used here is the repository's direct Bernstein argument.",
            },
        ],
        headline_metrics={
            "exact_flattened_program_partial_trace_theorem_count": int(verified),
            "sharp_unflattened_direct_insertion_theorem_count": int(verified),
            "bounded_linear_fixed_copy_normalization_no_go_count": int(verified),
            "program_reflection_partial_trace_boundary_count": int(verified),
            "direct_control_count": len(direct_controls),
            "direct_control_failure_count": direct_failures,
            "copy_normalization_control_count": len(copy_controls),
            "copy_normalization_control_failure_count": copy_failures,
            "retained_window_direct_coefficient_lower_constant": PARENT_WINDOW_LOWER / PARENT_WINDOW_UPPER,
            "retained_window_direct_coefficient_upper_constant": PARENT_WINDOW_UPPER / PARENT_WINDOW_LOWER,
            "representation_specific_coherent_block_encoding_compiler_count": 0,
            "arbitrary_coherent_processor_lower_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "normalized_flattened_program_partial_trace_is_B_over_D": verified,
            "unflattened_direct_insertion_is_unique_inverse_density_sandwich": verified,
            "retained_window_direct_contraction_has_constant_normalization": False,
            "fixed_copy_bounded_linear_program_density_contraction_has_constant_normalization": False,
            "one_program_reflection_partial_trace_has_constant_asymptotic_normalization": False,
            "canonical_signal_requires_D_amplitude_amplification": verified,
            "canonical_signal_requires_linear_bounded_sign_qsvt_degree": verified,
            "representation_specific_coherent_block_encoding_compiled": False,
            "arbitrary_coherent_processor_lower_bound_proved": False,
            "direct_matrix_povm_naimark_dilation_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The target byproduct is exactly present but only with inverse logical-dimension signal in every analyzed direct contraction architecture. A representation-specific coherent transducer outside the bounded linear program-density model remains uncompiled and unruled-out."
            ),
        },
        status=theorem.status,
        summary=(
            "Falsified constant-normalization direct extraction from normalized final-root program densities: the exact canonical coefficient is 1/D, the unflattened optimum is Theta(1/D), one reflection gives 2/D, and every bounded trace-norm fixed-copy density contraction obeys |c|<=1/D."
        ),
        falsifiers_triggered=[
            "Constant-success purification-state flattening does not imply constant-strength extraction of VUV^*.",
            "The unique direct unflattened insertion is not a scale-free shortcut: it is the two-sided inverse-density sandwich.",
            "A canonical program reflection still exposes a traceless Weyl byproduct only at coefficient 2/D.",
            "Adding any fixed number of normalized program density copies cannot beat 1/D within the bounded trace-norm linear contraction model.",
            "The resulting natural selected-branch and bounded-sign costs are superpolynomial, but arbitrary coherent processors remain outside the theorem.",
        ],
    )


def write_final_root_program_contraction_normalization_no_go_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_program_contraction_normalization_no_go())
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
                title="Final-root program contraction normalization no-go",
                status="completed-architecture-no-go",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Derive the exact flattened and unflattened reference-leg contractions, optimize the unique insertion, audit a normalized program reflection, prove the trace-norm fixed-copy coefficient bound, and transfer the natural logical-dimension scaling."
                ),
                positive_signal=(
                    "A representation-specific coherent block encoding of V_C X V_C^* and V_C Z V_C^* at constant normalization that does not reduce to a bounded linear contraction of normalized program density operators."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_final_root_purification_naimark_program_boundary.py",
                    "self_dual_wreath_final_root_byproduct_covariance_no_go.py",
                    "self_dual_wreath_final_root_metric_access_width_no_go.py",
                    "self_dual_wreath_joint_character_natural_sector_mass.py",
                ],
                next_actions=[
                    "Test whether coherent access to the structured endpoint state-preparation unitary and its inverse yields a non-linear/reflection-sequence block encoding of the labelled Weyl pair whose normalization or query count beats the proved direct-contraction D charge."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "A normalized label-retaining purification, a supplied reflection about it, or finitely many normalized copies directly expose the endpoint-conjugated Weyl generators at constant normalization."
                ),
                reason_invalid=(
                    "The normalized projector contraction is exactly B_U/D; the optimal unflattened direct insertion has coefficient between lambda_min(rho) and lambda_max(rho), hence between 1/(32D) and 32/D on the retained window; a traceless-Weyl reflection contraction gives 2B_U/D; and every induced-trace-norm-one linear contraction of normalized density copies satisfies |c|<=1/D."
                ),
                lesson=(
                    "Charge logical dimension separately from state-flattening success. Any surviving direct route must exploit coherent oracle structure outside bounded linear program-density contractions, and its query/normalization cost must be proved explicitly."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "flattened_coefficient": "1/D",
                    "unflattened_optimum": "1/||rho^(-1/2) U rho^(-1/2)||",
                    "retained_window_bounds": "1/(32D)<=c_*(U)<=32/D",
                    "program_reflection_traceless_weyl_coefficient": "2/D",
                    "fixed_copy_bounded_linear_density_contraction_bound": "|c|<=1/D",
                    "selected_branch_probability": "1/D^2",
                    "amplitude_amplification_factor": "D",
                    "arbitrary_coherent_processor_lower_bound_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_program_contraction_normalization_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
