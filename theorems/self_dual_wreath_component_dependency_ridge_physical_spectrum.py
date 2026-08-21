"""Physical spectral form of the dependency-ridge error.

Let the child synthesis and sibling-common isometry be

    R: K_coeff -> H_phys,          X:C^r -> Ran(R),

and define

    L=R^*R,
    M=R^*(I-XX^*)R,
    F=RR^*,
    F_perp=(I-XX^*)F(I-XX^*).                         (1)

The nonzero spectra of ``L`` and ``F`` coincide.  Likewise ``M=T^*T`` and
``F_perp=TT^*`` for ``T=(I-XX^*)R``, so their nonzero spectra coincide.
Moreover

    rank(L)-rank(M)=r.                                  (2)

For ``f_eta(a)=a/(a+eta)`` define the support-ridge tail

    T_eta(A)=sum_(lambda in spec+(A)) (eta/(lambda+eta))^2
            = rank(A)-2 Tr f_eta(A)+Tr f_eta(A)^2.       (3)

The dependency support ridge from the companion theorem therefore obeys

    ||Pi-Q_eta||_F^2 <= T_eta(F)+T_eta(F_perp).           (4)

Equation (4) is entirely physical.  It replaces a coefficient-space support
question by two scalar spectral statistics of the child frame and its sibling-
excluded compression.  The functions in (3) are resolvent/heat-kernel
functions, so existing regular-master frame-word machinery can target them.

Under any accepted source event,

    R_eta = E[1_E ||Pi-Q_eta||_F^2/D_phys]
      <= E[1_E (T_eta(F)+T_eta(F_perp))/D_phys].          (5)

Combining (5) with parity-ridge stability transfers a positive bounded-ridge
curl to exact natural M4 once the right-hand side is ``o(signal^2)``.  This
module proves the spectral reduction, not that natural tail estimate or a
positive ridge curl.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_dependency_ridge_parity_stability import (
    dependency_projection_and_ridge,
    dependency_ridge_spectral_tail_upper_bound,
    physical_parity_curl_transfer_bound,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_dependency_ridge_physical_spectrum.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-SPECTRUM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class DependencyPhysicalSpectrumControl:
    control_id: str
    physical_dimension: int
    coefficient_dimension: int
    child_synthesis_rank: int
    common_fiber_dimension: int
    excluded_synthesis_rank: int
    ridge_parameter: float
    maximum_full_nonzero_spectrum_residual: float
    maximum_excluded_nonzero_spectrum_residual: float
    rank_difference_residual: int
    coefficient_full_support_ridge_tail: float
    physical_full_support_ridge_tail: float
    coefficient_excluded_support_ridge_tail: float
    physical_excluded_support_ridge_tail: float
    exact_dependency_ridge_error_squared: float
    coefficient_spectral_tail_upper_bound: float
    physical_spectral_tail_upper_bound: float
    physical_tail_bound_slack: float
    support_ridge_tail_trace_formula_residual: float
    exact_physical_spectral_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalTailTransferScalingRecord:
    target_exact_physical_M4: float
    assumed_normalized_physical_spectral_tail: float
    exact_M4_transfer_error_upper_bound: float
    required_bounded_ridge_physical_curl: float
    transfer_can_preserve_target_signal: bool
    uniform_minimum_frame_eigenvalue_required: bool
    coefficient_space_analysis_required: bool
    status: str


@dataclass(frozen=True)
class DependencyRidgePhysicalSpectrumTheorem:
    full_spectrum_transfer: str
    excluded_spectrum_transfer: str
    rank_identity: str
    tail_trace_identity: str
    dependency_error_bound: str
    physical_annealed_bound: str
    arbitrary_child_synthesis: bool
    arbitrary_common_subspace_inside_child_range: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDependencyRidgePhysicalSpectrumReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DependencyRidgePhysicalSpectrumTheorem
    finite_controls: list[DependencyPhysicalSpectrumControl]
    scaling_records: list[PhysicalTailTransferScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _positive_eigenvalues(
    matrix: np.ndarray,
    *,
    tolerance: float,
) -> np.ndarray:
    values = np.linalg.eigvalsh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("the spectral-tail input must be positive semidefinite")
    return values[values > 100 * tolerance]


def support_ridge_tail(
    matrix: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-10,
) -> float:
    if ridge_parameter <= 0:
        raise ValueError("the ridge parameter must be positive")
    positive = _positive_eigenvalues(matrix, tolerance=tolerance)
    return float(
        np.sum((ridge_parameter / (positive + ridge_parameter)) ** 2)
    )


def support_ridge_tail_trace_formula(
    matrix: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-10,
) -> float:
    positive = _positive_eigenvalues(matrix, tolerance=tolerance)
    transformed = positive / (positive + ridge_parameter)
    return float(len(positive) - 2 * np.sum(transformed) + np.sum(transformed**2))


def dependency_physical_frames(
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if synthesis.ndim != 2 or min(synthesis.shape) < 1:
        raise ValueError("a nonempty child synthesis is required")
    physical = synthesis.shape[0]
    if (
        common_isometry.ndim != 2
        or common_isometry.shape[0] != physical
        or common_isometry.shape[1] < 1
    ):
        raise ValueError("the common isometry has the wrong physical shape")
    identity = np.eye(common_isometry.shape[1], dtype=complex)
    if np.linalg.norm(
        common_isometry.conj().T @ common_isometry - identity,
        ord=2,
    ) > 1000 * tolerance:
        raise ValueError("the common matrix must be an isometry")
    frame = _hermitian(synthesis @ synthesis.conj().T)
    frame_support_values, frame_support_vectors = np.linalg.eigh(frame)
    support = frame_support_vectors[:, frame_support_values > 100 * tolerance]
    if np.linalg.norm(
        support @ support.conj().T @ common_isometry - common_isometry,
        ord=2,
    ) > 1000 * tolerance:
        raise ValueError("the common subspace must lie inside the child range")
    common_projection = common_isometry @ common_isometry.conj().T
    complement = np.eye(physical, dtype=complex) - common_projection
    gram = _hermitian(synthesis.conj().T @ synthesis)
    excluded_gram = _hermitian(synthesis.conj().T @ complement @ synthesis)
    excluded_frame = _hermitian(complement @ frame @ complement)
    return gram, excluded_gram, frame, excluded_frame


def audit_dependency_physical_spectrum(
    control_id: str,
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-9,
) -> DependencyPhysicalSpectrumControl:
    gram, excluded_gram, frame, excluded_frame = dependency_physical_frames(
        synthesis,
        common_isometry,
        tolerance=tolerance,
    )
    projection, ridge, _ = dependency_projection_and_ridge(
        gram,
        excluded_gram,
        ridge_parameter,
        tolerance=tolerance,
    )
    full_coefficient = _positive_eigenvalues(gram, tolerance=tolerance)
    full_physical = _positive_eigenvalues(frame, tolerance=tolerance)
    excluded_coefficient = _positive_eigenvalues(
        excluded_gram,
        tolerance=tolerance,
    )
    excluded_physical = _positive_eigenvalues(
        excluded_frame,
        tolerance=tolerance,
    )
    full_residual = float(np.max(np.abs(full_coefficient - full_physical)))
    excluded_residual = float(
        np.max(np.abs(excluded_coefficient - excluded_physical))
    ) if len(excluded_coefficient) else 0.0
    rank_difference = (
        len(full_coefficient)
        - len(excluded_coefficient)
        - common_isometry.shape[1]
    )
    full_coefficient_tail = support_ridge_tail(
        gram,
        ridge_parameter,
        tolerance=tolerance,
    )
    full_physical_tail = support_ridge_tail(
        frame,
        ridge_parameter,
        tolerance=tolerance,
    )
    excluded_coefficient_tail = support_ridge_tail(
        excluded_gram,
        ridge_parameter,
        tolerance=tolerance,
    )
    excluded_physical_tail = support_ridge_tail(
        excluded_frame,
        ridge_parameter,
        tolerance=tolerance,
    )
    exact_error = float(np.linalg.norm(projection - ridge, ord="fro") ** 2)
    coefficient_bound = dependency_ridge_spectral_tail_upper_bound(
        gram,
        excluded_gram,
        ridge_parameter,
        tolerance=tolerance,
    )
    physical_bound = full_physical_tail + excluded_physical_tail
    trace_residual = max(
        abs(
            support_ridge_tail_trace_formula(
                matrix,
                ridge_parameter,
                tolerance=tolerance,
            )
            - support_ridge_tail(
                matrix,
                ridge_parameter,
                tolerance=tolerance,
            )
        )
        for matrix in (gram, excluded_gram, frame, excluded_frame)
    )
    slack = physical_bound - exact_error
    exact = bool(
        max(full_residual, excluded_residual, trace_residual) <= 5000 * tolerance
        and rank_difference == 0
        and abs(coefficient_bound - physical_bound) <= 5000 * tolerance
        and slack >= -5000 * tolerance
    )
    return DependencyPhysicalSpectrumControl(
        control_id=control_id,
        physical_dimension=synthesis.shape[0],
        coefficient_dimension=synthesis.shape[1],
        child_synthesis_rank=len(full_coefficient),
        common_fiber_dimension=common_isometry.shape[1],
        excluded_synthesis_rank=len(excluded_coefficient),
        ridge_parameter=ridge_parameter,
        maximum_full_nonzero_spectrum_residual=full_residual,
        maximum_excluded_nonzero_spectrum_residual=excluded_residual,
        rank_difference_residual=rank_difference,
        coefficient_full_support_ridge_tail=full_coefficient_tail,
        physical_full_support_ridge_tail=full_physical_tail,
        coefficient_excluded_support_ridge_tail=excluded_coefficient_tail,
        physical_excluded_support_ridge_tail=excluded_physical_tail,
        exact_dependency_ridge_error_squared=exact_error,
        coefficient_spectral_tail_upper_bound=coefficient_bound,
        physical_spectral_tail_upper_bound=physical_bound,
        physical_tail_bound_slack=slack,
        support_ridge_tail_trace_formula_residual=trace_residual,
        exact_physical_spectral_reduction_verified=exact,
        status=(
            "dependency-ridge-error-reduced-to-physical-frame-spectral-tails"
            if exact
            else "dependency-ridge-physical-spectrum-control-failure"
        ),
    )


def _random_synthesis_with_common_subspace(
    physical_dimension: int,
    coefficient_dimension: int,
    synthesis_rank: int,
    common_dimension: int,
    *,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    if not (
        1 <= common_dimension <= synthesis_rank
        <= min(physical_dimension, coefficient_dimension)
    ):
        raise ValueError("invalid synthesis and common dimensions")
    rng = np.random.default_rng(seed)
    left_raw = rng.normal(size=(physical_dimension, synthesis_rank)) + 1j * rng.normal(
        size=(physical_dimension, synthesis_rank)
    )
    left, _ = np.linalg.qr(left_raw, mode="reduced")
    right_raw = rng.normal(size=(coefficient_dimension, synthesis_rank)) + 1j * rng.normal(
        size=(coefficient_dimension, synthesis_rank)
    )
    right, _ = np.linalg.qr(right_raw, mode="reduced")
    singular = np.linspace(0.45, 1.75, synthesis_rank)
    synthesis = (left * singular) @ right.conj().T
    mixing_raw = rng.normal(size=(synthesis_rank, synthesis_rank)) + 1j * rng.normal(
        size=(synthesis_rank, synthesis_rank)
    )
    mixing, _ = np.linalg.qr(mixing_raw)
    common = left @ mixing[:, :common_dimension]
    return synthesis, common


def physical_tail_transfer_scaling_record(
    target_exact_physical_M4: float,
    assumed_normalized_physical_spectral_tail: float,
) -> PhysicalTailTransferScalingRecord:
    if target_exact_physical_M4 < 0 or assumed_normalized_physical_spectral_tail < 0:
        raise ValueError("targets and tails must be nonnegative")
    transfer = physical_parity_curl_transfer_bound(
        assumed_normalized_physical_spectral_tail
    )
    required = target_exact_physical_M4 + transfer
    return PhysicalTailTransferScalingRecord(
        target_exact_physical_M4=target_exact_physical_M4,
        assumed_normalized_physical_spectral_tail=(
            assumed_normalized_physical_spectral_tail
        ),
        exact_M4_transfer_error_upper_bound=transfer,
        required_bounded_ridge_physical_curl=required,
        transfer_can_preserve_target_signal=required <= 1.0,
        uniform_minimum_frame_eigenvalue_required=False,
        coefficient_space_analysis_required=False,
        status=(
            "physical-frame-tail-permits-exact-M4-transfer"
            if required <= 1.0
            else "physical-frame-tail-too-large-for-unit-scale-transfer"
        ),
    )


def dependency_ridge_physical_spectrum_theorem(
) -> DependencyRidgePhysicalSpectrumTheorem:
    return DependencyRidgePhysicalSpectrumTheorem(
        full_spectrum_transfer="spec+(R*R)=spec+(RR*) with multiplicity",
        excluded_spectrum_transfer=(
            "spec+(R*(I-XX*)R)=spec+((I-XX*)RR*(I-XX*))"
        ),
        rank_identity="rank(L)-rank(M)=rank(X)=r",
        tail_trace_identity=(
            "T_eta(A)=rank(A)-2Tr f_eta(A)+Tr f_eta(A)^2"
        ),
        dependency_error_bound=(
            "||Pi-Q_eta||F^2<=T_eta(F)+T_eta(F_perp)"
        ),
        physical_annealed_bound=(
            "E[1_E||Pi-Q_eta||F^2/D]<=E[1_E(T_eta(F)+T_eta(F_perp))/D]"
        ),
        arbitrary_child_synthesis=True,
        arbitrary_common_subspace_inside_child_range=True,
        theorem_verified=True,
        status="dependency-ridge-error-is-two-physical-frame-spectral-tails",
    )


def run_component_dependency_ridge_physical_spectrum(
) -> ComponentDependencyRidgePhysicalSpectrumReport:
    controls = []
    for control_id, dimensions, seed, eta in (
        ("FULL-ROW-RANK-D12-N16-R5", (12, 16, 12, 5), 7101, 1e-2),
        ("RANK-DEFICIENT-D14-N18-S10-R4", (14, 18, 10, 4), 7102, 3e-3),
        ("TALL-D16-N12-S12-R6", (16, 12, 12, 6), 7103, 1e-3),
    ):
        synthesis, common = _random_synthesis_with_common_subspace(
            *dimensions,
            seed=seed,
        )
        controls.append(
            audit_dependency_physical_spectrum(
                control_id,
                synthesis,
                common,
                eta,
            )
        )
    scaling = [
        physical_tail_transfer_scaling_record(1e-4, tail)
        for tail in (1e-14, 1e-12, 1e-10, 1e-8, 1e-6)
    ]
    theorem = dependency_ridge_physical_spectrum_theorem()
    failures = sum(
        not row.exact_physical_spectral_reduction_verified for row in controls
    )
    return ComponentDependencyRidgePhysicalSpectrumReport(
        created_at=utc_now(),
        theorem_contract={
            "full_spectrum": theorem.full_spectrum_transfer,
            "excluded_spectrum": theorem.excluded_spectrum_transfer,
            "rank": theorem.rank_identity,
            "tail_trace": theorem.tail_trace_identity,
            "dependency_error": theorem.dependency_error_bound,
            "physical_average": theorem.physical_annealed_bound,
            "scope": (
                "This is an exact singular-value reduction. It does not bound "
                "the natural physical frame tails or positive ridge curl."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_coefficient_space_from_dependency_ridge_error",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "The two coefficient Grams share nonzero spectra with the "
                    "child frame and sibling-excluded physical frame."
                ),
            },
            {
                "obligation": "express_support_ridge_tail_as_resolvent_trace",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Equation (3) uses only rank, Tr f_eta, and Tr f_eta^2."
                ),
            },
            {
                "obligation": "bound_natural_child_and_excluded_physical_frame_tails",
                "resolved": False,
                "resolution": (
                    "Use regular-master heat/resolvent word moments to prove "
                    "E[1_E(T_eta(F)+T_eta(F_perp))/D]=o(signal^2)."
                ),
            },
            {
                "obligation": "prove_positive_bounded_ridge_parity_curl",
                "resolved": False,
                "resolution": (
                    "The spectral reduction controls transfer error only; a "
                    "natural typical-stratum ridge signal is still required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The coefficient Gram has extra zero eigenvalues that spoil physical transfer.",
                "resolved": True,
                "resolution": (
                    "The tail sums only positive eigenvalues; all nonzero "
                    "singular values transfer with multiplicity."
                ),
            },
            {
                "objection": "Projecting away X changes the nonzero singular-value correspondence.",
                "resolved": True,
                "resolution": (
                    "Set T=(I-XX*)R. Then M=T*T and F_perp=TT* exactly."
                ),
            },
            {
                "objection": "The ridge error needs a uniform hard edge.",
                "resolved": True,
                "resolution": (
                    "No. Equation (5) is a trace-weighted physical spectral-tail premise."
                ),
            },
            {
                "objection": "Physical accessibility of the tail proves it is small.",
                "resolved": True,
                "resolution": (
                    "It does not; natural representation-theoretic resolvent "
                    "estimates remain the hard theorem."
                ),
            },
        ],
        headline_metrics={
            "dependency_ridge_physical_spectrum_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_nonzero_spectrum_residual": max(
                max(
                    row.maximum_full_nonzero_spectrum_residual,
                    row.maximum_excluded_nonzero_spectrum_residual,
                )
                for row in controls
            ),
            "maximum_tail_trace_formula_residual": max(
                row.support_ridge_tail_trace_formula_residual for row in controls
            ),
            "minimum_physical_tail_bound_slack": min(
                row.physical_tail_bound_slack for row in controls
            ),
            "scaling_record_count": len(scaling),
            "scaling_transfer_survival_count": sum(
                row.transfer_can_preserve_target_signal for row in scaling
            ),
            "natural_physical_spectral_tail_theorem_count": 0,
            "natural_bounded_ridge_parity_curl_lower_bound_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "coefficient_dependency_ridge_error_reduced_to_physical_spectra": (
                theorem.theorem_verified and failures == 0
            ),
            "uniform_minimum_frame_eigenvalue_required": False,
            "common_coefficient_metric_required": False,
            "natural_physical_frame_resolvent_tail_small": False,
            "natural_bounded_ridge_parity_curl_positive": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The ridge transfer premise is now a physical frame spectral "
                "statistic, but no natural tail or positive ridge signal is proved."
            ),
        },
        status=(
            "dependency-ridge-error-reduced-to-two-physical-frame-tails"
            if failures == 0
            else "dependency-ridge-physical-spectrum-control-failure"
        ),
        summary=(
            "Transferred the dependency support-ridge error exactly from two "
            "coefficient Grams to the child and sibling-excluded physical frame "
            "spectra, exposing a scalar resolvent-tail target."
        ),
        falsifiers_triggered=[
            "Coefficient-space zero modes do not enter the support-ridge tail.",
            "The sibling-excluded Gram has an exact physical TT* counterpart.",
            "Uniform hard edges are stronger than the physical trace-tail premise needed.",
            "No natural physical tail, ridge curl, exact M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_dependency_ridge_physical_spectrum_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-SPECTRUM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_dependency_ridge_physical_spectrum" in globals():
        report = run_component_dependency_ridge_physical_spectrum(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-SPECTRUM",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-SPECTRUM.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-SPECTRUM.",
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
                    "self_dual_wreath_component_dependency_ridge_physical_spectrum": str(path)
                },
            )
        )
    return payload
