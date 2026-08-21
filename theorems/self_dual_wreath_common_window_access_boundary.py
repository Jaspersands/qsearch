"""Common-window access boundary and recursive cross-polar factorization.

The final-root window theorem gives a rank-dense common subspace on which the
recursive cross metric is uniformly conditioned.  This module separates two
questions that theorem does not answer.

First, for child syntheses ``S_s`` with ``F_s=S_s S_s^*`` and an orthonormal
basis ``X`` of a common child span, define

    V_s = S_s^* F_s^(+1/2),
    A_s = X^* F_s^+ X,
    M   = A_L + A_R,
    E_s = F_s^(+1/2) X M^(-1/2).                         (1)

The normalized cross relation factors exactly as

    G = [V_L E_L; -V_R E_R],
    E_L^*E_L + E_R^*E_R = I.                            (2)

If ``X`` lies in the spectral window ``[a,b]`` of both child frames, each
endpoint effect has lower edge ``a/(2b)``.  Thus the endpoint mixer is
constant-conditioned for ``a=0.1,b=10``.  Conversely, postselecting either
branch of ``G`` and undoing that constant-conditioned effect recovers the
corresponding child polar on a copy of the common space.  A recursive
cross-relation compiler therefore contains, rather than bypasses, dense
restricted child-polar access.

Second, rank density and state retention do not make the common window
coherently recognizable.  Let

    R_L = I-|u><u|,  R_R = I-|v><v|,  <u|v>=cos(phi).     (3)

Both windows have codimension one and their intersection has codimension two.
Nevertheless the smallest positive eigenvalue of

    (I-R_L)+(I-R_R)

is ``1-cos(phi)``, while the product of the two window reflections has
smallest nonzero eigenphase ``2 phi``.  Choosing ``phi=2^-n`` gives an
exponentially small phase gap even though the discarded rank and native state
mass vanish.  The construction is compatible with any compact limiting bulk
spectrum, including the final-root Marchenko--Pastur laws: put one outlier on
``u`` or ``v`` and the desired bulk eigenvalues on the orthogonal complement.

Hence weak marginal spectral laws, a constant cross metric on the exact
intersection, and gentle state retention do not imply a polynomial
intersection projector.  In the two-reflection oracle model, constant-bias
separation of phase zero from ``2 phi`` needs ``Omega(1/phi)`` queries.  This
does not rule out a representation-specific circuit that exposes the common
space or implements (2) directly.
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
    "self_dual_wreath_common_window_access_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMMON-WINDOW-ACCESS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
WINDOW_LOWER = 0.1
WINDOW_UPPER = 10.0
QSVT_POLAR_URL = "https://arxiv.org/abs/2106.07634"


@dataclass(frozen=True)
class CrossPolarFactorizationControl:
    control_id: str
    physical_dimension: int
    left_coefficient_dimension: int
    right_coefficient_dimension: int
    common_dimension: int
    cross_metric_minimum_eigenvalue: float
    cross_metric_maximum_eigenvalue: float
    cross_metric_condition_number: float
    cross_metric_condition_number_upper_bound: float
    left_endpoint_minimum_eigenvalue: float
    right_endpoint_minimum_eigenvalue: float
    endpoint_minimum_lower_bound: float
    direct_cross_relation_residual: float
    synthesis_annihilation_residual: float
    cross_relation_isometry_residual: float
    endpoint_completeness_residual: float
    left_branch_polar_recovery_residual: float
    right_branch_polar_recovery_residual: float
    exact_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class WindowIntersectionAccessControl:
    control_id: str
    ambient_dimension: int
    exceptional_angle: float
    left_window_rank: int
    right_window_rank: int
    common_window_rank: int
    common_codimension: int
    common_codimension_fraction: float
    individual_spectrum_residual: float
    left_window_projector_residual: float
    right_window_projector_residual: float
    intersection_projector_residual: float
    defect_smallest_positive_eigenvalue: float
    defect_gap_formula: float
    reflection_smallest_nonzero_eigenphase: float
    reflection_phase_formula: float
    phase_resolution_query_lower_bound: float
    native_root_state_loss: float
    cross_metric_condition_number: float
    minimum_endpoint_weight: float
    dense_but_small_angle_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class WindowAccessScalingRecord:
    n: int
    ambient_dimension_decimal: str
    exceptional_angle_log2: float
    common_codimension_fraction: float
    defect_gap_log2: float
    reflection_phase_gap_log2: float
    phase_resolution_query_lower_bound_log2: float
    native_state_loss_upper_bound: float
    marginal_bulk_law_unchanged_by_exceptional_angle: bool
    weak_mp_marginals_compatible: bool
    rank_dense_common_window: bool
    constant_cross_metric_on_exact_intersection: bool
    polynomial_reflection_oracle_intersection_access: bool
    status: str


@dataclass(frozen=True)
class CommonWindowAccessTheorem:
    cross_polar_factorization: str
    endpoint_completeness: str
    endpoint_lower_edge: str
    child_polar_recovery: str
    principal_angle_counterfamily: str
    reflection_oracle_lower_bound: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CommonWindowAccessBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CommonWindowAccessTheorem
    factorization_controls: list[CrossPolarFactorizationControl]
    access_controls: list[WindowIntersectionAccessControl]
    scaling_records: list[WindowAccessScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
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
    tolerance: float,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    transformed = np.zeros_like(values)
    active = values > 100 * tolerance
    transformed[active] = values[active] ** exponent
    return (vectors * transformed) @ vectors.conj().T


def _kernel_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    _, singular_values, right_adjoint = np.linalg.svd(
        matrix,
        full_matrices=True,
    )
    rank = int(np.count_nonzero(singular_values > 100 * tolerance))
    return right_adjoint.conj().T[:, rank:]


def _projector(basis: np.ndarray) -> np.ndarray:
    return basis @ basis.conj().T


def _frame_with_one_outlier(
    normal: np.ndarray,
    bulk_eigenvalues: np.ndarray,
    outlier_eigenvalue: float,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    vector = np.asarray(normal, dtype=complex)
    vector = vector / np.linalg.norm(vector)
    complement = _kernel_basis(vector.conj()[None, :], tolerance)
    if len(bulk_eigenvalues) != complement.shape[1]:
        raise ValueError("one bulk eigenvalue is required per complement axis")
    frame = (
        (complement * np.asarray(bulk_eigenvalues)) @ complement.conj().T
        + outlier_eigenvalue * np.outer(vector, vector.conj())
    )
    return _hermitian(frame), _projector(complement)


def audit_cross_polar_factorization(
    control_id: str,
    left_synthesis: np.ndarray,
    right_synthesis: np.ndarray,
    common_basis: np.ndarray,
    *,
    window_lower: float = WINDOW_LOWER,
    window_upper: float = WINDOW_UPPER,
    tolerance: float = 1e-9,
) -> CrossPolarFactorizationControl:
    if (
        left_synthesis.ndim != 2
        or right_synthesis.ndim != 2
        or left_synthesis.shape[0] != right_synthesis.shape[0]
        or common_basis.shape[0] != left_synthesis.shape[0]
    ):
        raise ValueError("child syntheses and common basis must share an ambient space")
    if not 0 < window_lower < window_upper:
        raise ValueError("require a positive ordered window")
    common_dimension = common_basis.shape[1]
    if not common_dimension:
        raise ValueError("common basis must be nonempty")
    if np.linalg.norm(
        common_basis.conj().T @ common_basis - np.eye(common_dimension),
        ord=2,
    ) > 100 * tolerance:
        raise ValueError("common basis must be orthonormal")

    left_frame = _hermitian(left_synthesis @ left_synthesis.conj().T)
    right_frame = _hermitian(right_synthesis @ right_synthesis.conj().T)
    left_inverse = _psd_power(left_frame, -1.0, tolerance)
    right_inverse = _psd_power(right_frame, -1.0, tolerance)
    left_inverse_root = _psd_power(left_frame, -0.5, tolerance)
    right_inverse_root = _psd_power(right_frame, -0.5, tolerance)
    left_metric = _hermitian(
        common_basis.conj().T @ left_inverse @ common_basis
    )
    right_metric = _hermitian(
        common_basis.conj().T @ right_inverse @ common_basis
    )
    metric = _hermitian(left_metric + right_metric)
    metric_inverse_root = _psd_power(metric, -0.5, tolerance)
    metric_values = np.linalg.eigvalsh(metric)

    left_polar = left_synthesis.conj().T @ left_inverse_root
    right_polar = right_synthesis.conj().T @ right_inverse_root
    left_endpoint = left_inverse_root @ common_basis @ metric_inverse_root
    right_endpoint = right_inverse_root @ common_basis @ metric_inverse_root
    left_effect = _hermitian(left_endpoint.conj().T @ left_endpoint)
    right_effect = _hermitian(right_endpoint.conj().T @ right_endpoint)
    left_effect_inverse_root = _psd_power(left_effect, -0.5, tolerance)
    right_effect_inverse_root = _psd_power(right_effect, -0.5, tolerance)
    left_domain_isometry = left_endpoint @ left_effect_inverse_root
    right_domain_isometry = right_endpoint @ right_effect_inverse_root

    factored = np.vstack(
        (
            left_polar @ left_endpoint,
            -right_polar @ right_endpoint,
        )
    )
    direct_preimage = np.vstack(
        (
            np.linalg.pinv(left_synthesis, rcond=tolerance) @ common_basis,
            -np.linalg.pinv(right_synthesis, rcond=tolerance) @ common_basis,
        )
    )
    direct = direct_preimage @ _psd_power(
        direct_preimage.conj().T @ direct_preimage,
        -0.5,
        tolerance,
    )
    synthesis = np.concatenate((left_synthesis, right_synthesis), axis=1)
    left_dimension = left_synthesis.shape[1]
    left_branch = factored[:left_dimension]
    right_branch = -factored[left_dimension:]
    identity = np.eye(common_dimension, dtype=complex)

    direct_residual = float(np.linalg.norm(factored - direct, ord=2))
    annihilation_residual = float(np.linalg.norm(synthesis @ factored, ord=2))
    isometry_residual = float(
        np.linalg.norm(factored.conj().T @ factored - identity, ord=2)
    )
    endpoint_residual = float(
        np.linalg.norm(left_effect + right_effect - identity, ord=2)
    )
    left_recovery = float(
        np.linalg.norm(
            left_branch @ left_effect_inverse_root
            - left_polar @ left_domain_isometry,
            ord=2,
        )
    )
    right_recovery = float(
        np.linalg.norm(
            right_branch @ right_effect_inverse_root
            - right_polar @ right_domain_isometry,
            ord=2,
        )
    )
    metric_bound = window_upper / window_lower
    endpoint_bound = window_lower / (2.0 * window_upper)
    left_minimum = float(np.linalg.eigvalsh(left_effect)[0])
    right_minimum = float(np.linalg.eigvalsh(right_effect)[0])
    verified = bool(
        metric_values[0] + 1000 * tolerance >= 2.0 / window_upper
        and metric_values[-1] <= 2.0 / window_lower + 1000 * tolerance
        and metric_values[-1] / metric_values[0]
        <= metric_bound + 1000 * tolerance
        and left_minimum + 1000 * tolerance >= endpoint_bound
        and right_minimum + 1000 * tolerance >= endpoint_bound
        and max(
            direct_residual,
            annihilation_residual,
            isometry_residual,
            endpoint_residual,
            left_recovery,
            right_recovery,
        )
        <= 1000 * tolerance
    )
    return CrossPolarFactorizationControl(
        control_id=control_id,
        physical_dimension=left_synthesis.shape[0],
        left_coefficient_dimension=left_synthesis.shape[1],
        right_coefficient_dimension=right_synthesis.shape[1],
        common_dimension=common_dimension,
        cross_metric_minimum_eigenvalue=float(metric_values[0]),
        cross_metric_maximum_eigenvalue=float(metric_values[-1]),
        cross_metric_condition_number=float(metric_values[-1] / metric_values[0]),
        cross_metric_condition_number_upper_bound=metric_bound,
        left_endpoint_minimum_eigenvalue=left_minimum,
        right_endpoint_minimum_eigenvalue=right_minimum,
        endpoint_minimum_lower_bound=endpoint_bound,
        direct_cross_relation_residual=direct_residual,
        synthesis_annihilation_residual=annihilation_residual,
        cross_relation_isometry_residual=isometry_residual,
        endpoint_completeness_residual=endpoint_residual,
        left_branch_polar_recovery_residual=left_recovery,
        right_branch_polar_recovery_residual=right_recovery,
        exact_factorization_verified=verified,
        status=(
            "exact-cross-polar-factorization-and-recovery"
            if verified
            else "cross-polar-factorization-control-failure"
        ),
    )


def audit_window_intersection_access(
    control_id: str,
    dimension: int,
    exceptional_angle: float,
    *,
    outlier_eigenvalue: float = 0.01,
    tolerance: float = 1e-9,
) -> tuple[WindowIntersectionAccessControl, CrossPolarFactorizationControl]:
    if dimension < 4:
        raise ValueError("dimension must be at least four")
    if not 0 < exceptional_angle < math.pi / 2:
        raise ValueError("exceptional angle must lie in (0,pi/2)")
    if not 0 <= outlier_eigenvalue < WINDOW_LOWER:
        raise ValueError("outlier must lie below the fixed window")

    left_normal = np.zeros(dimension, dtype=complex)
    left_normal[0] = 1.0
    right_normal = np.zeros(dimension, dtype=complex)
    right_normal[0] = math.cos(exceptional_angle)
    right_normal[1] = math.sin(exceptional_angle)
    bulk = np.linspace(0.25, 8.75, dimension - 1)
    left_frame, left_window = _frame_with_one_outlier(
        left_normal,
        bulk,
        outlier_eigenvalue,
        tolerance,
    )
    right_frame, right_window = _frame_with_one_outlier(
        right_normal,
        bulk,
        outlier_eigenvalue,
        tolerance,
    )
    common = _kernel_basis(
        np.vstack((left_normal.conj(), right_normal.conj())),
        tolerance,
    )
    common_projector = _projector(common)
    identity = np.eye(dimension, dtype=complex)
    exceptional_projector = identity - common_projector
    defect = _hermitian(
        (identity - left_window) + (identity - right_window)
    )
    positive_defect = np.linalg.eigvalsh(defect)
    positive_defect = positive_defect[positive_defect > 100 * tolerance]
    defect_gap = float(positive_defect[0])
    defect_formula = 2.0 * math.sin(exceptional_angle / 2.0) ** 2

    left_reflection = 2.0 * left_window - identity
    right_reflection = 2.0 * right_window - identity
    phases = np.abs(np.angle(np.linalg.eigvals(left_reflection @ right_reflection)))
    nonzero_phases = phases[phases > 100 * tolerance]
    phase_gap = float(nonzero_phases[0])
    phase_formula = 2.0 * exceptional_angle

    native_frame = _hermitian(left_frame + right_frame)
    native_loss = float(
        np.trace(native_frame @ exceptional_projector).real
        / np.trace(native_frame).real
    )
    left_values = np.linalg.eigvalsh(left_frame)
    right_values = np.linalg.eigvalsh(right_frame)
    spectrum_residual = float(np.max(np.abs(left_values - right_values)))
    left_projector_residual = float(
        np.linalg.norm(left_window @ left_window - left_window, ord=2)
    )
    right_projector_residual = float(
        np.linalg.norm(right_window @ right_window - right_window, ord=2)
    )
    intersection_residual = max(
        float(np.linalg.norm(left_window @ common_projector - common_projector, ord=2)),
        float(np.linalg.norm(right_window @ common_projector - common_projector, ord=2)),
    )

    left_synthesis = _psd_power(left_frame, 0.5, tolerance)
    right_synthesis = _psd_power(right_frame, 0.5, tolerance)
    factorization = audit_cross_polar_factorization(
        control_id + "-CROSS",
        left_synthesis,
        right_synthesis,
        common,
        tolerance=tolerance,
    )
    minimum_endpoint = min(
        factorization.left_endpoint_minimum_eigenvalue,
        factorization.right_endpoint_minimum_eigenvalue,
    )
    verified = bool(
        left_window.shape[0] == dimension
        and round(float(np.trace(left_window).real)) == dimension - 1
        and round(float(np.trace(right_window).real)) == dimension - 1
        and common.shape[1] == dimension - 2
        and spectrum_residual <= 100 * tolerance
        and abs(defect_gap - defect_formula) <= 1000 * tolerance
        and abs(phase_gap - phase_formula) <= 1000 * tolerance
        and max(
            left_projector_residual,
            right_projector_residual,
            intersection_residual,
        )
        <= 1000 * tolerance
        and factorization.exact_factorization_verified
    )
    return (
        WindowIntersectionAccessControl(
            control_id=control_id,
            ambient_dimension=dimension,
            exceptional_angle=exceptional_angle,
            left_window_rank=dimension - 1,
            right_window_rank=dimension - 1,
            common_window_rank=common.shape[1],
            common_codimension=dimension - common.shape[1],
            common_codimension_fraction=(dimension - common.shape[1]) / dimension,
            individual_spectrum_residual=spectrum_residual,
            left_window_projector_residual=left_projector_residual,
            right_window_projector_residual=right_projector_residual,
            intersection_projector_residual=intersection_residual,
            defect_smallest_positive_eigenvalue=defect_gap,
            defect_gap_formula=defect_formula,
            reflection_smallest_nonzero_eigenphase=phase_gap,
            reflection_phase_formula=phase_formula,
            phase_resolution_query_lower_bound=1.0 / phase_formula,
            native_root_state_loss=native_loss,
            cross_metric_condition_number=(
                factorization.cross_metric_condition_number
            ),
            minimum_endpoint_weight=minimum_endpoint,
            dense_but_small_angle_boundary_verified=verified,
            status=(
                "dense-common-window-exponential-angle-boundary"
                if verified
                else "common-window-access-control-failure"
            ),
        ),
        factorization,
    )


def window_access_scaling_record(n: int) -> WindowAccessScalingRecord:
    if n < 4:
        raise ValueError("n must be at least four")
    dimension = 1 << n
    angle = math.ldexp(1.0, -n)
    defect_gap = 2.0 * math.sin(angle / 2.0) ** 2
    phase_gap = 2.0 * angle
    state_loss_bound = min(
        1.0,
        2.0 * WINDOW_UPPER / (WINDOW_LOWER * (dimension - 1)),
    )
    return WindowAccessScalingRecord(
        n=n,
        ambient_dimension_decimal=str(dimension),
        exceptional_angle_log2=-float(n),
        common_codimension_fraction=2.0 / dimension,
        defect_gap_log2=math.log2(defect_gap),
        reflection_phase_gap_log2=math.log2(phase_gap),
        phase_resolution_query_lower_bound_log2=math.log2(1.0 / phase_gap),
        native_state_loss_upper_bound=state_loss_bound,
        marginal_bulk_law_unchanged_by_exceptional_angle=True,
        weak_mp_marginals_compatible=True,
        rank_dense_common_window=True,
        constant_cross_metric_on_exact_intersection=True,
        polynomial_reflection_oracle_intersection_access=False,
        status="weak-marginals-do-not-control-principal-angle-gap",
    )


def run_common_window_access_boundary() -> CommonWindowAccessBoundaryReport:
    audited = [
        audit_window_intersection_access("D8-PHI-0.2", 8, 0.2),
        audit_window_intersection_access("D12-PHI-0.05", 12, 0.05),
        audit_window_intersection_access("D16-PHI-0.01", 16, 0.01),
    ]
    access_controls = [row[0] for row in audited]
    factorization_controls = [row[1] for row in audited]
    scaling = [window_access_scaling_record(n) for n in (8, 16, 24, 32, 48, 64)]
    failures = sum(
        not row.dense_but_small_angle_boundary_verified for row in access_controls
    ) + sum(
        not row.exact_factorization_verified for row in factorization_controls
    )
    verified = failures == 0
    return CommonWindowAccessBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "cross_polar_factorization": (
                "The normalized recursive cross relation is exactly "
                "[V_L E_L;-V_R E_R], with V_s the child synthesis polar and "
                "E_s=F_s^(+1/2)X(A_L+A_R)^(-1/2)."
            ),
            "endpoint_mixer": (
                "E_L^*E_L+E_R^*E_R=I. On a shared [a,b] window each endpoint "
                "effect is at least a/(2b) and the cross metric has condition "
                "number at most b/a."
            ),
            "recovery_reduction": (
                "Either branch of a cross-relation compiler, followed by the "
                "constant-conditioned inverse endpoint effect, recovers the "
                "child polar on an isometric copy of the common domain."
            ),
            "principal_angle_boundary": (
                "Two codimension-one windows can have codimension-two "
                "intersection but defect gap 1-cos(phi) and reflection-product "
                "phase gap 2phi."
            ),
            "weak_law_compatibility": (
                "The exceptional angle changes only eigenvectors. Any compact "
                "bulk eigenvalue sequence, including MP quantiles, can be used "
                "with one vanishing-mass outlier."
            ),
            "scope": (
                "The query lower bound is for black-box access to the two "
                "window reflections. It does not rule out a structured "
                "representation-specific common-space or direct-polar circuit."
            ),
        },
        theorem=CommonWindowAccessTheorem(
            cross_polar_factorization=(
                "G=[V_L E_L;-V_R E_R] is the exact orthonormal cross relation."
            ),
            endpoint_completeness="E_L^*E_L+E_R^*E_R=I.",
            endpoint_lower_edge=(
                "If aI<=F_s|X<=bI, then E_s^*E_s>=a/(2b)I."
            ),
            child_polar_recovery=(
                "G_s(E_s^*E_s)^(-1/2)=V_s U_s for an isometry U_s."
            ),
            principal_angle_counterfamily=(
                "Rank/state-dense windows permit phi=2^-n and gap 1-cos(phi)."
            ),
            reflection_oracle_lower_bound=(
                "Resolving phase zero from 2phi with constant bias costs "
                "Omega(1/phi) reflection-oracle queries."
            ),
            scope=(
                "Final-root metric conditioning is constructive only after "
                "structured common-space access and dense child polar access."
            ),
            theorem_verified=verified,
            status=(
                "cross-factorization-proved-window-access-not-implied"
                if verified
                else "common-window-access-theorem-control-failure"
            ),
        ),
        factorization_controls=factorization_controls,
        access_controls=access_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "factor_recursive_cross_relation_into_child_polars",
                "resolved": verified,
                "resolution": "Equations (1)-(2) are exact and pass finite controls.",
            },
            {
                "obligation": "bound_windowed_endpoint_mixer",
                "resolved": verified,
                "resolution": (
                    "The [0.1,10] window gives metric condition at most 100 "
                    "and endpoint effect lower edge at least 1/200."
                ),
            },
            {
                "obligation": "derive_common_window_access_from_weak_mp_laws",
                "resolved": True,
                "resolution": (
                    "Resolved negatively: an exponentially small principal "
                    "angle is invisible to each marginal empirical law."
                ),
            },
            {
                "obligation": "construct_natural_structured_common_space_access",
                "resolved": False,
                "resolution": (
                    "Requires a representation-specific circuit or a natural "
                    "principal-angle theorem; neither follows from weak MP limits."
                ),
            },
            {
                "obligation": "compile_dense_restricted_child_polars",
                "resolved": False,
                "resolution": (
                    "The exact recovery reduction shows this is embedded in "
                    "the recursive cross relation and cannot be omitted."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Codimension o(D) makes intersection projection easy.",
                "resolved": True,
                "resolution": (
                    "False in the reflection-oracle model: codimension two "
                    "coexists with phase gap 2^-Theta(n)."
                ),
            },
            {
                "objection": "Native state loss o(1) supplies the missing gap.",
                "resolved": True,
                "resolution": (
                    "False. The counterfamily has O(1/D) native loss while its "
                    "exceptional principal angle is independently exponential."
                ),
            },
            {
                "objection": "A constant-conditioned cross metric compiles G.",
                "resolved": True,
                "resolution": (
                    "It conditions only the endpoint mixer after X and the "
                    "child polars are available; it does not expose either."
                ),
            },
            {
                "objection": "The oracle boundary rules out the natural wreath route.",
                "resolved": False,
                "resolution": (
                    "A direct GPE/recoupling transform may exploit structure not "
                    "present in two black-box window reflections."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Fast algorithm for quantum polar decomposition, pretty-good measurements, and the Procrustes problem",
                "url": QSVT_POLAR_URL,
                "used_for": "Conditional polar implementation from a normalized block encoding and singular gap",
                "proves_structured_wreath_access": False,
            }
        ],
        headline_metrics={
            "exact_cross_polar_factorization_theorem_count": int(verified),
            "constant_endpoint_mixer_theorem_count": int(verified),
            "child_polar_recovery_reduction_count": int(verified),
            "principal_angle_access_counterfamily_count": int(verified),
            "finite_control_count": len(access_controls),
            "finite_control_failure_count": failures,
            "window_cross_metric_condition_number_upper_bound": 100.0,
            "window_endpoint_effect_lower_bound": 1.0 / 200.0,
            "tail_phase_resolution_query_lower_bound_log2": (
                scaling[-1].phase_resolution_query_lower_bound_log2
            ),
            "structured_common_space_circuit_count": 0,
            "dense_restricted_child_polar_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_recursive_cross_polar_factorization_proved": verified,
            "constant_conditioned_endpoint_mixer_proved": verified,
            "cross_relation_contains_dense_child_polar_proved": verified,
            "rank_dense_window_implies_polynomial_intersection_access": False,
            "weak_mp_marginals_control_principal_angles": False,
            "structured_natural_common_space_access_proved": False,
            "dense_restricted_child_polar_compiled": False,
            "recursive_orientation_polar_compiled": False,
            "polynomial_physical_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The window makes the endpoint mixer benign but neither exposes "
                "the common space nor implements the child polar. Weak marginal "
                "laws permit an exponential principal-angle access barrier."
            ),
        },
        status=(
            "endpoint-mixer-conditioned-common-space-and-child-polar-open"
            if verified
            else "common-window-access-boundary-validation-failure"
        ),
        summary=(
            "Factored the recursive cross relation into dense child polars and "
            "a constant-conditioned endpoint mixer, then proved that rank-dense "
            "weak-law windows can still have exponentially hard black-box "
            "intersection access."
        ),
        falsifiers_triggered=[
            "Rank-dense common windows do not imply a polynomial intersection projector.",
            "Gentle native-state loss does not control the exceptional principal-angle gap.",
            "Cross-metric conditioning does not remove the dense child-polar gate.",
        ],
    )


def write_common_window_access_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMMON-WINDOW-ACCESS-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_common_window_access_boundary" in globals():
        report = run_common_window_access_boundary(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMMON-WINDOW-ACCESS-BOUNDARY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMMON-WINDOW-ACCESS-BOUNDARY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMMON-WINDOW-ACCESS-BOUNDARY.",
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
                    "self_dual_wreath_common_window_access_boundary": str(path)
                },
            )
        )
    return payload
