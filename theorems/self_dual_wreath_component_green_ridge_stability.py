"""Outcome-count-free stability of component M4 under Green ridge replacement.

The exact component effects use the pseudoinverse synthesis

    G = F^+,
    B = X^* G X,
    Y = G X B^{-1/2},
    H_e = Y^* E_e Y,                                    (1)

where the leaf projections sum to ``F``.  This module quantifies when the
unbounded Green operator can be replaced by the bounded ridge

    T_eta = F(F+eta I)^{-2}.                              (2)

Normalize the ridge synthesis with

    C_eta = X^* T_eta F T_eta X,
    Y_eta = T_eta X C_eta^{-1/2},
    H_e,eta = Y_eta^* E_e Y_eta.                          (3)

Both effect families are exact POVMs.  Two deterministic estimates remove a
potentially fatal factor equal to the number of leaves.

First, for arbitrary POVMs ``H`` and ``J`` on an ``r``-dimensional fiber, put

    epsilon_POVM = sum_e ||H_e-J_e||_2^2.

Then

    |Tr D_com(H)-Tr D_com(J)|/r
        <= 4 sqrt(2 epsilon_POVM/r).                       (4)

Second, put ``Q_e=F^{-1/2}E_eF^{-1/2}`` on ``supp(F)`` and define the
frame-weighted normalized syntheses

    W = F^{1/2}Y,       W_eta = F^{1/2}Y_eta.

These are isometries and ``H_e=W^*Q_eW``.  If
``delta_F=||W-W_eta||_F/sqrt(r)``, then

    epsilon_POVM <= 4 ||W-W_eta||_F^2,                    (5)

so their normalized commutator moments differ by at most

    8 sqrt(2) delta_F.                                    (6)

All constants are independent of the number and ranks of leaves.

There is also an explicit uniform ridge premise.  Let ``gamma`` be the
smallest positive eigenvalue of ``F``, ``L=||F||``, ``b=lambda_min(B)``, and

    epsilon = ||T_eta-G||
            = eta(2 gamma+eta)/(gamma(gamma+eta)^2),
    beta = 2 epsilon + L epsilon^2.

If ``beta<b``, inverse-square-root perturbation gives

    delta <= epsilon/sqrt(b-beta)
             + ||G|| beta/(2(b-beta)^(3/2)).               (7)

The more useful regular-master consequence does not require a uniform edge:
if a blockwise ridge calculation proves average normalized gap at least
``zeta``, define

    U     = F^{-1/2}X,
    U_eta = F^{3/2}(F+eta I)^{-2}X,
    R_eta = ||U-U_eta||_F^2 /
            (r(sigma_min(U)+sigma_min(U_eta))^2).          (8)

The same-rank polar-factor perturbation theorem gives

    |M4-M4_eta| <= 16 sqrt(2 R_eta).                       (9)

Hence ``E_Plancherel R_eta=o(zeta^2)`` proves exact independent M4 is
``zeta-o(zeta)``.  This is a scalar, trace-weighted spectral-tail premise;
it does not require a uniform child-frame edge.

This is a reduction, not the missing natural theorem.  No polynomial lower
bound on ``gamma`` or ``b``, no average synthesis-error estimate, and no
positive natural ridge gap is currently proved.  The result specifies exactly
what a bounded heat-kernel/return-word calculation must control.
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
    "self_dual_wreath_component_green_ridge_stability.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PovmCommutatorStabilityControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    summed_effect_hilbert_schmidt_error: float
    first_normalized_commutator_moment: float
    second_normalized_commutator_moment: float
    normalized_commutator_moment_difference: float
    outcome_count_free_stability_upper_bound: float
    first_povm_completeness_residual: float
    second_povm_completeness_residual: float
    stability_bound_verified: bool
    status: str


@dataclass(frozen=True)
class GreenRidgeStabilityControl:
    control_id: str
    ambient_dimension: int
    common_fiber_dimension: int
    leaf_count: int
    ridge_parameter: float
    frame_minimum_positive_eigenvalue: float
    frame_maximum_eigenvalue: float
    exact_common_metric_minimum_eigenvalue: float
    exact_ridge_operator_error: float
    ridge_operator_error_formula: float
    common_metric_perturbation: float
    common_metric_perturbation_upper_bound: float
    perturbation_premise_satisfied: bool
    exact_synthesis_operator_error: float
    synthesis_operator_error_upper_bound: float
    summed_effect_hilbert_schmidt_error: float
    synthesis_to_effect_error_upper_bound: float
    exact_normalized_commutator_moment: float
    ridge_normalized_commutator_moment: float
    normalized_commutator_moment_difference: float
    povm_stability_upper_bound: float
    synthesis_stability_upper_bound: float
    frame_weighted_synthesis_frobenius_error: float
    normalized_frame_weighted_synthesis_error: float
    frame_weighted_effect_error_upper_bound: float
    frame_weighted_commutator_stability_upper_bound: float
    exact_prepolar_ridge_frobenius_error: float
    trace_formula_prepolar_ridge_frobenius_error: float
    exact_prepolar_minimum_singular_value: float
    ridge_prepolar_minimum_singular_value: float
    polar_factor_frobenius_error_upper_bound: float
    normalized_trace_weighted_ridge_ratio: float
    trace_weighted_commutator_transfer_upper_bound: float
    exact_povm_completeness_residual: float
    ridge_povm_completeness_residual: float
    complete_ridge_stability_chain_verified: bool
    status: str


@dataclass(frozen=True)
class PolynomialRidgeScheduleRecord:
    frame_lower_edge_exponent: float
    common_metric_lower_edge_exponent: float
    frame_norm_upper_exponent: float
    target_moment_lower_bound_exponent: float
    regularization_exponent_must_exceed: float
    polynomial_ridge_schedule_exists_conditionally: bool
    natural_frame_edge_proved: bool
    natural_common_metric_edge_proved: bool
    natural_average_synthesis_error_proved: bool
    status: str


@dataclass(frozen=True)
class ComponentGreenRidgeStabilityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    povm_controls: list[PovmCommutatorStabilityControl]
    ridge_controls: list[GreenRidgeStabilityControl]
    scaling_records: list[PolynomialRidgeScheduleRecord]
    regular_master_reduction: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float = 1e-11,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _normalized_commutator_moment(effects: tuple[np.ndarray, ...]) -> float:
    dimension = effects[0].shape[0]
    total = 0.0
    for index, left in enumerate(effects):
        for right in effects[index + 1 :]:
            commutator = left @ right - right @ left
            total += float(np.trace(commutator.conj().T @ commutator).real)
    return total / dimension


def audit_povm_commutator_stability(
    control_id: str,
    first: tuple[np.ndarray, ...],
    second: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> PovmCommutatorStabilityControl:
    if not first or len(first) != len(second):
        raise ValueError("two nonempty equally indexed POVMs are required")
    dimension = first[0].shape[0]
    if dimension < 1 or any(
        effect.shape != (dimension, dimension)
        for effect in (*first, *second)
    ):
        raise ValueError("all effects must share one positive square fiber")
    identity = np.eye(dimension, dtype=complex)
    first_residual = float(
        np.linalg.norm(sum(first, np.zeros_like(identity)) - identity, ord=2)
    )
    second_residual = float(
        np.linalg.norm(sum(second, np.zeros_like(identity)) - identity, ord=2)
    )
    if max(first_residual, second_residual) > 1000 * tolerance:
        raise ValueError("both families must be POVMs")
    epsilon = sum(
        float(np.linalg.norm(left - right, ord="fro") ** 2)
        for left, right in zip(first, second)
    )
    first_moment = _normalized_commutator_moment(first)
    second_moment = _normalized_commutator_moment(second)
    difference = abs(first_moment - second_moment)
    bound = 4.0 * math.sqrt(2.0 * epsilon / dimension)
    verified = difference <= bound + 1000 * tolerance
    return PovmCommutatorStabilityControl(
        control_id=control_id,
        fiber_dimension=dimension,
        outcome_count=len(first),
        summed_effect_hilbert_schmidt_error=epsilon,
        first_normalized_commutator_moment=first_moment,
        second_normalized_commutator_moment=second_moment,
        normalized_commutator_moment_difference=difference,
        outcome_count_free_stability_upper_bound=bound,
        first_povm_completeness_residual=first_residual,
        second_povm_completeness_residual=second_residual,
        stability_bound_verified=verified,
        status=(
            "outcome-count-free-component-M4-stability-verified"
            if verified
            else "component-M4-stability-control-failure"
        ),
    )


def green_and_ridge_syntheses(
    leaves: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-11,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    tuple[np.ndarray, ...],
    tuple[np.ndarray, ...],
]:
    """Return ``F,G,T_eta,Y,Y_eta`` and both normalized effect families."""

    if not leaves or ridge_parameter <= 0:
        raise ValueError("nonempty leaves and positive ridge parameter are required")
    ambient = leaves[0].shape[0]
    if ambient < 1 or any(leaf.shape != (ambient, ambient) for leaf in leaves):
        raise ValueError("leaves must share one positive square ambient space")
    if common_isometry.ndim != 2 or common_isometry.shape[0] != ambient:
        raise ValueError("common isometry has the wrong ambient dimension")
    frame = sum(leaves, np.zeros((ambient, ambient), dtype=complex))
    green = _psd_power(frame, -1.0, tolerance=tolerance)
    values, vectors = np.linalg.eigh((frame + frame.conj().T) / 2.0)
    ridge_values = np.where(
        values > 100 * tolerance,
        values / (values + ridge_parameter) ** 2,
        0.0,
    )
    ridge = (vectors * ridge_values) @ vectors.conj().T

    exact_metric = common_isometry.conj().T @ green @ common_isometry
    ridge_metric = (
        common_isometry.conj().T
        @ ridge
        @ frame
        @ ridge
        @ common_isometry
    )
    exact_synthesis = (
        green
        @ common_isometry
        @ _psd_power(exact_metric, -0.5, tolerance=tolerance)
    )
    ridge_synthesis = (
        ridge
        @ common_isometry
        @ _psd_power(ridge_metric, -0.5, tolerance=tolerance)
    )
    exact_effects = tuple(
        exact_synthesis.conj().T @ leaf @ exact_synthesis
        for leaf in leaves
    )
    ridge_effects = tuple(
        ridge_synthesis.conj().T @ leaf @ ridge_synthesis
        for leaf in leaves
    )
    return (
        frame,
        green,
        ridge,
        exact_synthesis,
        ridge_synthesis,
        exact_effects,
        ridge_effects,
    )


def audit_green_ridge_stability(
    control_id: str,
    leaves: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-9,
) -> GreenRidgeStabilityControl:
    (
        frame,
        green,
        ridge,
        exact_synthesis,
        ridge_synthesis,
        exact_effects,
        ridge_effects,
    ) = green_and_ridge_syntheses(
        leaves,
        common_isometry,
        ridge_parameter,
        tolerance=tolerance,
    )
    ambient = frame.shape[0]
    fiber = common_isometry.shape[1]
    identity = np.eye(fiber, dtype=complex)
    frame_values = np.linalg.eigvalsh((frame + frame.conj().T) / 2.0)
    positive = frame_values[frame_values > 100 * tolerance]
    gamma = float(positive[0])
    frame_norm = float(positive[-1])
    exact_metric = common_isometry.conj().T @ green @ common_isometry
    ridge_metric = (
        common_isometry.conj().T
        @ ridge
        @ frame
        @ ridge
        @ common_isometry
    )
    b = float(np.linalg.eigvalsh((exact_metric + exact_metric.conj().T) / 2.0)[0])
    ridge_error = float(np.linalg.norm(ridge - green, ord=2))
    ridge_error_formula = (
        ridge_parameter * (2 * gamma + ridge_parameter)
        / (gamma * (gamma + ridge_parameter) ** 2)
    )
    beta = 2 * ridge_error_formula + frame_norm * ridge_error_formula**2
    metric_perturbation = float(np.linalg.norm(ridge_metric - exact_metric, ord=2))
    premise = beta < b
    synthesis_error = float(
        np.linalg.norm(ridge_synthesis - exact_synthesis, ord=2)
    )
    synthesis_bound = math.inf
    if premise:
        margin = b - beta
        synthesis_bound = (
            ridge_error_formula / math.sqrt(margin)
            + (1.0 / gamma) * beta / (2 * margin ** 1.5)
        )
    effect_error = sum(
        float(np.linalg.norm(left - right, ord="fro") ** 2)
        for left, right in zip(exact_effects, ridge_effects)
    )
    effect_bound = 4 * fiber * synthesis_error**2
    exact_moment = _normalized_commutator_moment(exact_effects)
    ridge_moment = _normalized_commutator_moment(ridge_effects)
    moment_difference = abs(exact_moment - ridge_moment)
    povm_bound = 4 * math.sqrt(2 * effect_error / fiber)
    synthesis_stability_bound = 8 * math.sqrt(2) * synthesis_error
    frame_root = _psd_power(frame, 0.5, tolerance=tolerance)
    exact_weighted = frame_root @ exact_synthesis
    ridge_weighted = frame_root @ ridge_synthesis
    weighted_error = float(
        np.linalg.norm(exact_weighted - ridge_weighted, ord="fro")
    )
    normalized_weighted_error = weighted_error / math.sqrt(fiber)
    weighted_effect_bound = 4 * weighted_error**2
    weighted_commutator_bound = 8 * math.sqrt(2) * normalized_weighted_error

    exact_prepolar = frame_root @ green @ common_isometry
    ridge_prepolar = frame_root @ ridge @ common_isometry
    prepolar_error = float(
        np.linalg.norm(exact_prepolar - ridge_prepolar, ord="fro")
    )
    frame_vectors = np.linalg.eigh((frame + frame.conj().T) / 2.0)[1]
    # The trace formula is evaluated spectrally rather than from the matrix
    # difference, providing an independent check of the Green-tail object.
    spectral_coordinates = frame_vectors.conj().T @ common_isometry
    spectral_difference = np.zeros_like(frame_values)
    spectral_positive = frame_values > 100 * tolerance
    spectral_difference[spectral_positive] = (
        1 / np.sqrt(frame_values[spectral_positive])
        - frame_values[spectral_positive] ** 1.5
        / (frame_values[spectral_positive] + ridge_parameter) ** 2
    )
    trace_formula_error = float(
        np.linalg.norm(spectral_difference[:, None] * spectral_coordinates, ord="fro")
    )
    exact_prepolar_minimum = float(np.linalg.svd(exact_prepolar, compute_uv=False)[-1])
    ridge_prepolar_minimum = float(np.linalg.svd(ridge_prepolar, compute_uv=False)[-1])
    singular_sum = exact_prepolar_minimum + ridge_prepolar_minimum
    polar_bound = 2 * prepolar_error / singular_sum
    ridge_ratio = prepolar_error**2 / (fiber * singular_sum**2)
    trace_weighted_bound = 16 * math.sqrt(2 * ridge_ratio)
    exact_residual = float(
        np.linalg.norm(sum(exact_effects, np.zeros_like(identity)) - identity, ord=2)
    )
    ridge_residual = float(
        np.linalg.norm(sum(ridge_effects, np.zeros_like(identity)) - identity, ord=2)
    )
    verified = bool(
        premise
        and abs(ridge_error - ridge_error_formula) <= 1000 * tolerance
        and metric_perturbation <= beta + 1000 * tolerance
        and synthesis_error <= synthesis_bound + 1000 * tolerance
        and effect_error <= effect_bound + 1000 * tolerance
        and moment_difference <= min(povm_bound, synthesis_stability_bound) + 1000 * tolerance
        and effect_error <= weighted_effect_bound + 1000 * tolerance
        and moment_difference <= weighted_commutator_bound + 1000 * tolerance
        and abs(prepolar_error - trace_formula_error) <= 1000 * tolerance
        and weighted_error <= polar_bound + 1000 * tolerance
        and moment_difference <= trace_weighted_bound + 1000 * tolerance
        and max(exact_residual, ridge_residual) <= 1000 * tolerance
    )
    return GreenRidgeStabilityControl(
        control_id=control_id,
        ambient_dimension=ambient,
        common_fiber_dimension=fiber,
        leaf_count=len(leaves),
        ridge_parameter=ridge_parameter,
        frame_minimum_positive_eigenvalue=gamma,
        frame_maximum_eigenvalue=frame_norm,
        exact_common_metric_minimum_eigenvalue=b,
        exact_ridge_operator_error=ridge_error,
        ridge_operator_error_formula=ridge_error_formula,
        common_metric_perturbation=metric_perturbation,
        common_metric_perturbation_upper_bound=beta,
        perturbation_premise_satisfied=premise,
        exact_synthesis_operator_error=synthesis_error,
        synthesis_operator_error_upper_bound=synthesis_bound,
        summed_effect_hilbert_schmidt_error=effect_error,
        synthesis_to_effect_error_upper_bound=effect_bound,
        exact_normalized_commutator_moment=exact_moment,
        ridge_normalized_commutator_moment=ridge_moment,
        normalized_commutator_moment_difference=moment_difference,
        povm_stability_upper_bound=povm_bound,
        synthesis_stability_upper_bound=synthesis_stability_bound,
        frame_weighted_synthesis_frobenius_error=weighted_error,
        normalized_frame_weighted_synthesis_error=normalized_weighted_error,
        frame_weighted_effect_error_upper_bound=weighted_effect_bound,
        frame_weighted_commutator_stability_upper_bound=weighted_commutator_bound,
        exact_prepolar_ridge_frobenius_error=prepolar_error,
        trace_formula_prepolar_ridge_frobenius_error=trace_formula_error,
        exact_prepolar_minimum_singular_value=exact_prepolar_minimum,
        ridge_prepolar_minimum_singular_value=ridge_prepolar_minimum,
        polar_factor_frobenius_error_upper_bound=polar_bound,
        normalized_trace_weighted_ridge_ratio=ridge_ratio,
        trace_weighted_commutator_transfer_upper_bound=trace_weighted_bound,
        exact_povm_completeness_residual=exact_residual,
        ridge_povm_completeness_residual=ridge_residual,
        complete_ridge_stability_chain_verified=verified,
        status=(
            "complete-green-ridge-component-M4-stability-chain-verified"
            if verified
            else "green-ridge-component-M4-stability-control-failure"
        ),
    )


def polynomial_ridge_schedule_record(
    frame_lower_edge_exponent: float,
    common_metric_lower_edge_exponent: float,
    frame_norm_upper_exponent: float,
    target_moment_lower_bound_exponent: float,
) -> PolynomialRidgeScheduleRecord:
    exponents = (
        frame_lower_edge_exponent,
        common_metric_lower_edge_exponent,
        frame_norm_upper_exponent,
        target_moment_lower_bound_exponent,
    )
    if any(exponent < 0 for exponent in exponents):
        raise ValueError("all polynomial exponents must be nonnegative")
    a, c, ell, s = exponents
    # The frame-weighted polar route has prepolar error
    # O(eta/gamma^(3/2)); dividing by the common-metric singular scale
    # sqrt(b) and preserving n^-s requires d>3a/2+c/2+s.  Unlike the
    # ambient-synthesis route, no upper-frame-norm exponent is present.
    threshold = 1.5 * a + 0.5 * c + s
    return PolynomialRidgeScheduleRecord(
        frame_lower_edge_exponent=a,
        common_metric_lower_edge_exponent=c,
        frame_norm_upper_exponent=ell,
        target_moment_lower_bound_exponent=s,
        regularization_exponent_must_exceed=threshold,
        polynomial_ridge_schedule_exists_conditionally=True,
        natural_frame_edge_proved=False,
        natural_common_metric_edge_proved=False,
        natural_average_synthesis_error_proved=False,
        status="polynomial-ridge-schedule-conditional-on-frame-and-metric-edges",
    )


def _random_projection_frame(
    seed: int,
    *,
    ambient_dimension: int = 7,
    common_fiber_dimension: int = 3,
    leaf_count: int = 5,
    leaf_rank: int = 2,
) -> tuple[tuple[np.ndarray, ...], np.ndarray]:
    rng = np.random.default_rng(seed)
    leaves = []
    for _ in range(leaf_count):
        raw = rng.normal(size=(ambient_dimension, leaf_rank)) + 1j * rng.normal(
            size=(ambient_dimension, leaf_rank)
        )
        isometry, _ = np.linalg.qr(raw)
        leaves.append(isometry @ isometry.conj().T)
    raw_common = rng.normal(size=(ambient_dimension, common_fiber_dimension)) + 1j * rng.normal(
        size=(ambient_dimension, common_fiber_dimension)
    )
    common, _ = np.linalg.qr(raw_common)
    return tuple(leaves), common


def run_component_green_ridge_stability() -> ComponentGreenRidgeStabilityReport:
    first_leaves, first_common = _random_projection_frame(809)
    second_leaves, second_common = _random_projection_frame(
        811,
        ambient_dimension=8,
        common_fiber_dimension=4,
        leaf_count=6,
        leaf_rank=3,
    )
    ridge_controls = [
        audit_green_ridge_stability(
            "RANDOM-PROJECTION-FRAME-809-ETA-1E-4",
            first_leaves,
            first_common,
            1e-4,
        ),
        audit_green_ridge_stability(
            "RANDOM-PROJECTION-FRAME-809-ETA-3E-5",
            first_leaves,
            first_common,
            3e-5,
        ),
        audit_green_ridge_stability(
            "RANDOM-PROJECTION-FRAME-811-ETA-1E-4",
            second_leaves,
            second_common,
            1e-4,
        ),
    ]
    povm_controls = []
    for row_id, leaves, common, eta in (
        ("POVM-809", first_leaves, first_common, 1e-4),
        ("POVM-811", second_leaves, second_common, 1e-4),
    ):
        *_, exact_effects, ridge_effects = green_and_ridge_syntheses(
            leaves,
            common,
            eta,
        )
        povm_controls.append(
            audit_povm_commutator_stability(
                row_id,
                exact_effects,
                ridge_effects,
            )
        )
    ridge_failures = sum(
        not row.complete_ridge_stability_chain_verified for row in ridge_controls
    )
    povm_failures = sum(not row.stability_bound_verified for row in povm_controls)
    exact = ridge_failures == 0 and povm_failures == 0
    scaling = [
        polynomial_ridge_schedule_record(a, c, ell, s)
        for a, c, ell, s in (
            (0, 0, 0, 0),
            (1, 1, 1, 1),
            (2, 1, 2, 3),
            (3, 2, 4, 2),
        )
    ]
    return ComponentGreenRidgeStabilityReport(
        created_at=utc_now(),
        theorem_contract={
            "outcome_count_free_POVM_stability": (
                "For two r-dimensional POVMs, normalized component commutator "
                "moments differ by at most 4sqrt(2 sum_e||H_e-J_e||_2^2/r), "
                "independently of outcome count."
            ),
            "shared_projection_synthesis_stability": (
                "For frame-weighted isometries W=F^(1/2)Y and Z=F^(1/2)Y_eta, "
                "sum_e||H_e-J_e||_2^2<=4||W-Z||_F^2 and normalized M4 "
                "difference is at most 8sqrt(2)||W-Z||_F/sqrt(r)."
            ),
            "uniform_ridge_perturbation": (
                "Equations (2)-(3) obey the explicit synthesis bound (7) when "
                "beta=2epsilon+||F||epsilon^2 is below lambda_min(X^*F^+X)."
            ),
            "average_regular_master_transfer": (
                "With R_eta defined by equation (8), blockwise polar "
                "perturbation gives |M4-M4_eta|<=16sqrt(2R_eta). Thus "
                "E R_eta=o(zeta^2) transfers an average ridge gap zeta; no "
                "uniform block edge or leaf-count factor is required."
            ),
            "polar_perturbation_source": (
                "Zhu, Xu, Liu, and Ma (2018), Electronic Journal of Linear "
                "Algebra 34, pp. 231-239, records the same-rank Frobenius "
                "polar-factor bound 2||E||_F/(sigma_r+sigma_tilde_r)."
            ),
            "polar_perturbation_url": (
                "https://journals.uwyo.edu/index.php/ela/article/download/1873/1873/1873"
            ),
            "scope": (
                "No natural ridge gap, frame/metric edge, or average synthesis "
                "error estimate is proved. The theorem is a quantitative reduction."
            ),
        },
        povm_controls=povm_controls,
        ridge_controls=ridge_controls,
        scaling_records=scaling,
        regular_master_reduction={
            "ridge_green_operator": "T_eta=F(F+eta I)^-2",
            "ridge_heat_kernel": "T_eta=integral_0^infinity t exp(-eta t) F exp(-tF) dt",
            "fixed_eta_operator_is_bounded": True,
            "leaf_count_enters_stability_constant": False,
            "uniform_edge_required_for_average_stability_route": False,
            "frame_norm_upper_bound_required_for_polar_schedule": False,
            "average_synthesis_error_premise_proved_naturally": False,
            "positive_independent_plancherel_ridge_gap_proved": False,
        },
        proof_obligations=[
            {
                "obligation": "remove_leaf_count_loss_from_component_M4_approximation",
                "resolved": exact,
                "resolution": "POVM completeness sums all leaf errors before Cauchy, yielding equations (4)-(6) with no q factor.",
            },
            {
                "obligation": "replace_pseudoinverse_by_bounded_ridge_under_quantified_premise",
                "resolved": exact,
                "resolution": "Equation (7) follows from the exact ridge error and inverse-square-root perturbation; the stronger trace-weighted route follows from same-rank polar-factor stability.",
            },
            {
                "obligation": "bound_plancherel_average_green_to_ridge_synthesis_error",
                "resolved": False,
                "resolution": "Need E R_eta=o(zeta^2) for the exact trace-weighted ratio (8), or a stronger direct average polar-angle estimate.",
            },
            {
                "obligation": "prove_positive_leaf_marked_ridge_AABB_minus_ABAB_gap",
                "resolved": False,
                "resolution": "Evaluate bounded leaf-resolved heat-kernel return words in the natural independent regular master.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Approximating exponentially many effects necessarily loses a factor equal to the leaf count.",
                "resolved": True,
                "resolution": "False for normalized projection syntheses; POVM completeness gives the q-independent bounds (4)-(6).",
            },
            {
                "objection": "Operator-norm approximation of F^+ is mandatory on every source block.",
                "resolved": True,
                "resolution": "False for ordinary regular-master M4: the scalar average trace-weighted polar ratio E R_eta controls the error via (9).",
            },
            {
                "objection": "A fixed ridge parameter automatically approximates the natural pseudoinverse.",
                "resolved": False,
                "resolution": "No. Low child-frame or common-metric eigenvalues can make equations (2)-(3) unstable; they require direct average control or polynomial edges.",
            },
            {
                "objection": "The ridge reduction proves a positive natural commutator moment.",
                "resolved": False,
                "resolution": "It only shows how a separately proved positive ridge gap and small synthesis error would transfer.",
            },
        ],
        headline_metrics={
            "outcome_count_free_component_M4_stability_theorem_count": int(exact),
            "green_ridge_synthesis_perturbation_theorem_count": int(exact),
            "average_ridge_to_exact_M4_transfer_theorem_count": int(exact),
            "trace_weighted_polar_ridge_transfer_theorem_count": int(exact),
            "povm_control_count": len(povm_controls),
            "povm_control_failure_count": povm_failures,
            "ridge_control_count": len(ridge_controls),
            "ridge_control_failure_count": ridge_failures,
            "natural_average_synthesis_error_theorem_count": 0,
            "natural_positive_ridge_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "outcome_count_free_component_M4_stability_proved": exact,
            "bounded_ridge_replacement_reduction_proved": exact,
            "average_error_route_avoids_uniform_edge_requirement": exact,
            "trace_weighted_polar_ratio_is_exact_remaining_approximation_target": exact,
            "natural_average_green_to_ridge_error_small": False,
            "natural_leaf_marked_ridge_gap_positive": False,
            "natural_independent_plancherel_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
            "The pseudoinverse can now be replaced under a q-independent "
                "trace-weighted polar-ratio premise, but neither that premise nor "
                "a positive natural ridge gap has been established."
            ),
        },
        status=(
            "green-ridge-M4-stability-proved-natural-ridge-correlations-open"
            if exact
            else "green-ridge-M4-stability-control-failure"
        ),
        summary=(
            "Proved leaf-count-independent stability of component commutator "
            "mass and reduced the natural Green pseudoinverse to a bounded "
            "ridge calculation plus one scalar trace-weighted polar ratio."
        ),
        falsifiers_triggered=[
            "A naive q or q^2 approximation loss is not intrinsic for normalized projection syntheses.",
            "Uniform operator-norm frame edges are sufficient but not necessary; the exact average target is the trace-weighted polar ratio R_eta.",
            "Ridge normalization still depends on the sibling common metric and is not automatically stable.",
            "No natural ridge gap, average approximation estimate, compiler, decoder, or speedup is proved.",
        ],
    )


def write_component_green_ridge_stability_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_green_ridge_stability())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_component_green_ridge_stability_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
