"""Black-box access boundary after trace-weighted polar truncation.

Let ``R^*R=S`` be an orientation analysis with ``w`` leaves.  Generic coherent
PREPARE/SELECT access exposes the contraction ``R/sqrt(w)``.  On an eigenvector
of ``S`` with eigenvalue ``lambda_i`` its singular amplitude is
``sqrt(lambda_i/w)``.

Trace-weighted truncation removes modes with ``lambda_i<tau`` at small native
frame mass, but this does not remove the ``sqrt(w)`` subnormalisation.  The
sharp stress case is already the perfectly conditioned frame ``S=I``.  Every
singular amplitude is then ``1/sqrt(w)`` and there is no low mode to discard.
In the unknown-state resampling oracle model of Ozols--Roetteler--Roland,
preparing the polar output with constant success requires
``Theta(sqrt(w))`` queries.  Thus no theorem about the spectrum of ``S`` alone
can make generic normalized-analysis access polynomial.

For a nonflat retained spectrum, the source and target amplitude vectors after
successful normalized analysis are explicit:

    pi_i    = lambda_i / sqrt(sum_j lambda_j^2),
    sigma_i = sqrt(lambda_i / sum_j lambda_j).                 (1)

The initial good-component probability on the native frame state is

    a^2 = sum_i lambda_i^2 / (w sum_i lambda_i).                (2)

Equation (1) can be fed directly to the water-filling theorem.  At exact
fidelity its resampling factor is

    max_i sigma_i/pi_i
      = sqrt(sum lambda^2 / sum lambda) / sqrt(lambda_min),

and multiplying by ``1/a`` gives ``sqrt(w/lambda_min)``.  At bounded fidelity,
water filling can remove spectral skew but not the flat-frame ``sqrt(w)``
case.

Variable-time amplification reaches the same boundary on the native retained
distribution.  Its l2 inverse-singular scale is

    [sum_i (lambda_i/sum lambda) (w/lambda_i)]^(1/2)
      = sqrt(w rank(S)/tr(S)).                                 (3)

For a flat O(1)-scale frame this is ``sqrt(w)``.  Equations (1)--(3) do not
rule out a representation-specific direct polar transform.  They prove that
the next mechanism must use more than normalized black-box frame access.
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
    "self_dual_wreath_native_frame_access_boundary.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
QRS_URL = "https://arxiv.org/abs/1103.2774"
VTAA_URL = "https://arxiv.org/abs/1010.4458"


@dataclass(frozen=True)
class WaterFillingProfile:
    requested_fidelity: float
    direct_source_target_fidelity: float
    water_level: float
    filled_vector_norm: float
    qrs_query_factor: float
    achieved_fidelity: float
    saturated_coordinate_count: int
    exact_target_requested: bool


@dataclass(frozen=True)
class NativeFrameAccessControl:
    control_id: str
    orientation_count: int
    original_positive_rank: int
    retained_rank: int
    truncation_threshold: float
    original_frame_trace: float
    retained_frame_trace: float
    retained_native_frame_mass: float
    retained_minimum_eigenvalue: float
    retained_maximum_eigenvalue: float
    normalized_analysis_minimum_singular_value: float
    normalized_analysis_good_probability_on_retained_native_state: float
    initial_good_component_amplification_factor: float
    source_amplitudes: tuple[float, ...]
    target_amplitudes: tuple[float, ...]
    water_filling: WaterFillingProfile
    two_stage_water_filling_query_factor: float
    exact_qrs_query_factor: float
    variable_time_l2_inverse_singular_scale: float
    variable_time_identity_residual: float
    flat_retained_spectrum: bool
    flat_frame_black_box_sqrt_width_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class NativeFrameAccessScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    orientation_count_decimal: str
    flat_frame_qrs_lower_bound_log2: float
    flat_frame_variable_time_scale_log2: float
    polynomial_query_benchmark_degree: int
    polynomial_query_benchmark_log2: float
    black_box_access_superpolynomial: bool
    trace_weighted_truncation_changes_flat_control: bool
    representation_specific_direct_transform_required: bool
    status: str


@dataclass(frozen=True)
class NativeFrameAccessBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[NativeFrameAccessControl]
    scaling_records: list[NativeFrameAccessScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _normalized_positive(vector: np.ndarray, name: str) -> np.ndarray:
    if vector.ndim != 1 or len(vector) == 0:
        raise ValueError(f"{name} must be a nonempty vector")
    if np.any(vector <= 0):
        raise ValueError(f"{name} must be strictly positive")
    norm = float(np.linalg.norm(vector))
    if norm <= 0:
        raise ValueError(f"{name} has zero norm")
    return vector / norm


def water_filling_profile(
    source_amplitudes: tuple[float, ...],
    target_amplitudes: tuple[float, ...],
    requested_fidelity: float,
    *,
    tolerance: float = 1e-12,
) -> WaterFillingProfile:
    """Evaluate the Ozols--Roetteler--Roland water-filling vector.

    Both vectors are normalized and have common positive support.  The returned
    query factor suppresses universal constants in the theorem's ``Theta``.
    """

    if len(source_amplitudes) != len(target_amplitudes):
        raise ValueError("source and target vectors must have equal length")
    if not 0 < requested_fidelity <= 1:
        raise ValueError("requested_fidelity must lie in (0,1]")
    source = _normalized_positive(np.asarray(source_amplitudes, dtype=float), "source")
    target = _normalized_positive(np.asarray(target_amplitudes, dtype=float), "target")
    direct = float(np.dot(source, target) ** 2)
    ratios = source / target
    gamma_min = float(np.min(ratios))
    gamma_max = float(np.max(ratios))

    def evaluate(gamma: float) -> tuple[np.ndarray, float]:
        filled = np.minimum(source, gamma * target)
        norm = float(np.linalg.norm(filled))
        fidelity = float((np.dot(target, filled) / norm) ** 2)
        return filled, fidelity

    if requested_fidelity <= direct + tolerance:
        filled = source
        gamma = gamma_max
        achieved = direct
        factor = 1.0
    elif requested_fidelity >= 1 - tolerance:
        gamma = gamma_min
        filled, achieved = evaluate(gamma)
        factor = 1 / float(np.linalg.norm(filled))
    else:
        low = gamma_min
        high = gamma_max
        for _ in range(100):
            middle = (low + high) / 2
            _, fidelity = evaluate(middle)
            if fidelity > requested_fidelity:
                low = middle
            else:
                high = middle
        gamma = (low + high) / 2
        filled, achieved = evaluate(gamma)
        factor = 1 / float(np.linalg.norm(filled))
    filled_norm = float(np.linalg.norm(filled))
    saturated = int(np.count_nonzero(source <= gamma * target + tolerance))
    return WaterFillingProfile(
        requested_fidelity=requested_fidelity,
        direct_source_target_fidelity=direct,
        water_level=gamma,
        filled_vector_norm=filled_norm,
        qrs_query_factor=factor,
        achieved_fidelity=achieved,
        saturated_coordinate_count=saturated,
        exact_target_requested=requested_fidelity >= 1 - tolerance,
    )


def audit_native_frame_access(
    control_id: str,
    eigenvalues: tuple[float, ...],
    orientation_count: int,
    truncation_threshold: float,
    *,
    requested_fidelity: float = 2 / 3,
    tolerance: float = 1e-12,
) -> NativeFrameAccessControl:
    if orientation_count < 2 or truncation_threshold <= 0:
        raise ValueError("invalid orientation count or threshold")
    values = np.asarray(eigenvalues, dtype=float)
    if values.ndim != 1 or len(values) == 0 or np.any(values <= 0):
        raise ValueError("eigenvalues must be a nonempty positive vector")
    if np.any(values > orientation_count + tolerance):
        raise ValueError("a sum of w projectors cannot have eigenvalue above w")
    retained = values[values >= truncation_threshold]
    if len(retained) == 0:
        raise ValueError("truncation removed the entire frame")

    full_trace = float(np.sum(values))
    retained_trace = float(np.sum(retained))
    retained_square_trace = float(np.sum(retained**2))
    retained_mass = retained_trace / full_trace
    source = retained / math.sqrt(retained_square_trace)
    target = np.sqrt(retained / retained_trace)
    profile = water_filling_profile(
        tuple(float(value) for value in source),
        tuple(float(value) for value in target),
        requested_fidelity,
        tolerance=tolerance,
    )
    good_probability = retained_square_trace / (
        orientation_count * retained_trace
    )
    initial_factor = 1 / math.sqrt(good_probability)
    exact_factor = math.sqrt(orientation_count / float(np.min(retained)))
    conditional_variable_time = math.sqrt(
        orientation_count * len(retained) / retained_trace
    )
    direct_variable_time = math.sqrt(
        sum(
            (value / retained_trace) * (orientation_count / value)
            for value in retained
        )
    )
    identity_residual = abs(conditional_variable_time - direct_variable_time)
    flat = bool(np.max(retained) - np.min(retained) <= 100 * tolerance)
    flat_boundary = bool(
        flat
        and abs(profile.qrs_query_factor - 1) <= 100 * tolerance
        and abs(initial_factor - exact_factor) <= 100 * tolerance
        and identity_residual <= 100 * tolerance
    )
    return NativeFrameAccessControl(
        control_id=control_id,
        orientation_count=orientation_count,
        original_positive_rank=len(values),
        retained_rank=len(retained),
        truncation_threshold=truncation_threshold,
        original_frame_trace=full_trace,
        retained_frame_trace=retained_trace,
        retained_native_frame_mass=retained_mass,
        retained_minimum_eigenvalue=float(np.min(retained)),
        retained_maximum_eigenvalue=float(np.max(retained)),
        normalized_analysis_minimum_singular_value=math.sqrt(
            float(np.min(retained)) / orientation_count
        ),
        normalized_analysis_good_probability_on_retained_native_state=(
            good_probability
        ),
        initial_good_component_amplification_factor=initial_factor,
        source_amplitudes=tuple(float(value) for value in source),
        target_amplitudes=tuple(float(value) for value in target),
        water_filling=profile,
        two_stage_water_filling_query_factor=(
            initial_factor * profile.qrs_query_factor
        ),
        exact_qrs_query_factor=exact_factor,
        variable_time_l2_inverse_singular_scale=conditional_variable_time,
        variable_time_identity_residual=identity_residual,
        flat_retained_spectrum=flat,
        flat_frame_black_box_sqrt_width_boundary_verified=flat_boundary,
        status=(
            "flat-frame-sqrt-width-black-box-boundary"
            if flat_boundary
            else "nonflat-frame-water-filling-profile"
        ),
    )


def native_frame_access_scaling_record(
    n: int,
    *,
    extra_copies: int = 2,
    polynomial_benchmark_degree: int = 10,
) -> NativeFrameAccessScalingRecord:
    if n < 3 or extra_copies < 0 or polynomial_benchmark_degree < 1:
        raise ValueError("invalid scaling parameters")
    order = math.factorial(n)
    copies = (order - 1).bit_length() + extra_copies
    log2_cost = copies / 2
    benchmark = polynomial_benchmark_degree * math.log2(n)
    return NativeFrameAccessScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=copies,
        orientation_count_decimal=str(1 << copies),
        flat_frame_qrs_lower_bound_log2=log2_cost,
        flat_frame_variable_time_scale_log2=log2_cost,
        polynomial_query_benchmark_degree=polynomial_benchmark_degree,
        polynomial_query_benchmark_log2=benchmark,
        black_box_access_superpolynomial=log2_cost > benchmark,
        trace_weighted_truncation_changes_flat_control=False,
        representation_specific_direct_transform_required=True,
        status=(
            "flat-frame-black-box-access-superpolynomial"
            if log2_cost > benchmark
            else "finite-size-benchmark-not-yet-separated"
        ),
    )


def _finite_controls() -> list[NativeFrameAccessControl]:
    return [
        audit_native_frame_access(
            "FLAT-W16-R8",
            (1.0,) * 8,
            16,
            0.25,
        ),
        audit_native_frame_access(
            "FLAT-W256-R32",
            (1.0,) * 32,
            256,
            0.25,
        ),
        audit_native_frame_access(
            "SKEWED-LOW-MODE-TRUNCATED",
            (1e-8, 0.25, 0.5, 1.0, 2.0),
            64,
            0.1,
        ),
        audit_native_frame_access(
            "W4-TWO-ROW-SPECTRUM",
            (0.5, 0.5, 1.0, 1.0, 1.0, 1.5, 1.5),
            4,
            0.25,
        ),
    ]


def run_native_frame_access_boundary() -> NativeFrameAccessBoundaryReport:
    controls = _finite_controls()
    scaling = [
        native_frame_access_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    flat_controls = [row for row in controls if row.flat_retained_spectrum]
    flat_failures = sum(
        not row.flat_frame_black_box_sqrt_width_boundary_verified
        for row in flat_controls
    )
    identity_failures = sum(
        row.variable_time_identity_residual > 1e-10 for row in controls
    )
    separated = [row for row in scaling if row.black_box_access_superpolynomial]
    verified = bool(flat_controls and flat_failures == identity_failures == 0)
    tail = scaling[-1]
    return NativeFrameAccessBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "normalized_analysis": (
                "Generic PREPARE/SELECT exposes R/sqrt(w), whose singular "
                "amplitudes are sqrt(lambda_i/w)."
            ),
            "qrs_source_target_vectors": (
                "After successful analysis on the retained native frame, "
                "pi_i=lambda_i/sqrt(sum lambda^2) and "
                "sigma_i=sqrt(lambda_i/sum lambda)."
            ),
            "exact_qrs_cost": (
                "Initial good-component amplification times exact resampling "
                "is sqrt(w/lambda_min) up to universal constants."
            ),
            "variable_time_native_scale": (
                "The retained native l2 inverse-singular scale is exactly "
                "sqrt(w rank(S_ret)/tr(S_ret))."
            ),
            "flat_frame_lower_bound": (
                "For S=I, trace truncation removes nothing and the ORR unknown-"
                "state resampling lower bound is Theta(sqrt(w))."
            ),
            "scope": (
                "This is a normalized black-box access boundary. It does not "
                "rule out a direct representation-specific polar transform."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "compute_explicit_qrs_amplitude_pair",
                "resolved": verified,
                "resolution": (
                    "The source and target vectors are equation (1), with the "
                    "initial good probability in equation (2)."
                ),
            },
            {
                "obligation": "test_variable_time_amplification_as_width_bypass",
                "resolved": verified,
                "resolution": (
                    "Resolved negatively for generic access: native weighting "
                    "gives sqrt(w rank/tr), equal to sqrt(w) on a flat frame."
                ),
            },
            {
                "obligation": "construct_representation_specific_direct_polar",
                "resolved": False,
                "resolution": (
                    "The black-box lower bound makes this the only surviving "
                    "route; no such transform is constructed here."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Trace-weighted truncation makes generic QSVT polynomial.",
                "resolved": True,
                "resolution": (
                    "False. S=I has no discarded spectrum, but normalized access "
                    "still has singular amplitude 1/sqrt(w) everywhere."
                ),
            },
            {
                "objection": "Variable-time amplification averages away the width factor.",
                "resolved": True,
                "resolution": (
                    "False on the native distribution: the lambda_i weights "
                    "cancel the inverse lambda_i costs and leave w rank/tr(S)."
                ),
            },
            {
                "objection": "The lower bound kills the wreath-product route.",
                "resolved": False,
                "resolution": (
                    "It kills only normalized black-box analysis. A recoupling, "
                    "covariant, or other direct structured polar may evade the oracle model."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Quantum rejection sampling",
                "url": QRS_URL,
                "used_for": "Tight unknown-state resampling query bound and water filling",
                "representation_specific_no_go": False,
            },
            {
                "paper": "Variable time amplitude amplification and a faster quantum algorithm for solving systems of linear equations",
                "url": VTAA_URL,
                "used_for": "Input-weighted l2 stopping-time comparison",
                "representation_specific_no_go": False,
            },
        ],
        headline_metrics={
            "flat_frame_black_box_lower_bound_theorem_count": int(verified),
            "explicit_qrs_amplitude_pair_theorem_count": int(verified),
            "variable_time_native_scale_identity_count": int(verified),
            "finite_control_count": len(controls),
            "flat_control_count": len(flat_controls),
            "finite_control_failure_count": flat_failures + identity_failures,
            "superpolynomial_scaling_row_count": len(separated),
            "tail_n": tail.n,
            "tail_copy_count": tail.selected_copy_count,
            "tail_flat_qrs_lower_bound_log2": tail.flat_frame_qrs_lower_bound_log2,
            "tail_polynomial_benchmark_log2": tail.polynomial_query_benchmark_log2,
            "representation_specific_polar_transform_count": 0,
            "companion_gpe_pair_polar_transform_count": 1,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "explicit_orr_water_filling_vectors_derived": verified,
            "flat_frame_normalized_access_sqrt_width_lower_bound_proved": verified,
            "variable_time_generic_width_bypass_available": False,
            "trace_weighted_truncation_suffices_for_generic_qsvt": False,
            "representation_specific_direct_polar_ruled_out": False,
            "companion_pair_level_gpe_direct_polar_proved": True,
            "tightly_normalized_orientation_polar_access_proved": False,
            "polynomial_physical_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct average-state truncation is now known, but every "
                "generic normalized-analysis route retains a sqrt(w) barrier. "
                "Only a representation-specific direct polar can bypass this "
                "access model. The companion GPE module now supplies that bypass "
                "for pair transport, while the complete frame remains open."
            ),
        },
        status=(
            "black-box-width-bypass-refuted-pair-gpe-bypass-separate"
            if verified
            else "native-frame-access-boundary-validation-failure"
        ),
        summary=(
            "Computed the exact resampling amplitude pair and proved that even "
            "a perfectly conditioned frame requires square-root orientation "
            "queries under generic normalized access."
        ),
        falsifiers_triggered=[
            "A hard lower edge plus trace truncation is insufficient for generic polynomial QSVT.",
            "Variable-time amplification does not remove orientation width on native frame inputs.",
            "The companion GPE pair polar confirms that a representation-specific direct transform can bypass this generic width barrier.",
        ],
    )


def write_native_frame_access_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_native_frame_access_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_native_frame_access_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
