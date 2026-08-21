"""Linear covariant point POVM and stable-rank decoder criterion.

For the point quotient states ``omega_j``, put

    bar = n^-1 sum_j omega_j,
    Delta_j = omega_j-bar,
    beta = ||Delta_j||_infinity.

Covariance makes ``beta`` independent of ``j``.  The effects

    M_j = I/n + Delta_j/(n beta)                           (1)

form an exact POVM on the full retained register: ``sum_j M_j=I`` and
``M_j>=0`` because ``||Delta_j||_infinity=beta``.  Its uniform-prior success is

    P_lin = 1/n + ||Delta_j||_2^2/(n beta).                (2)

Writing ``r_eff=||Delta||_2^2/beta^2`` gives excess
``beta r_eff/n``.  Thus a polynomial weak point decoder follows if the
standard-harmonic centered operator has inverse-polynomial operator norm times
effective rank.

This decoder does not require the full average-state inverse used by the PGM.
However, equation (1) is an operator specification, not an implementation.
One still needs coherent signed access to the subgroup-twirled state
``Delta_j=T_Stab(j)(tau)-T_G(tau)``, an inverse-polynomial normalization, and a
block-measurement compiler.  Density-matrix exponentiation from copies alone
does not automatically implement an affine POVM effect with the required
precision.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_point_stabilizer_quotient import (
    _pretty_good_success,
    point_quotient_states,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_point_linear_povm.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-POINT-LINEAR-POVM"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PointLinearPOVMControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    register_dimension: int
    centered_hilbert_schmidt_norm_squared: float
    centered_operator_norm: float
    centered_effective_rank: float
    minimum_effect_eigenvalue: float
    maximum_effect_eigenvalue: float
    povm_completeness_residual: float
    covariance_norm_residual: float
    predicted_linear_success: float
    observed_linear_success: float
    linear_success_formula_residual: float
    pretty_good_success: float
    linear_minus_pretty_good_success: float
    random_guess_success: float
    linear_success_excess: float
    exact_linear_point_povm_verified: bool
    status: str


@dataclass(frozen=True)
class LinearPOVMScalingRecord:
    n: int
    point_hypothesis_count: int
    sufficient_operator_norm_times_effective_rank: str
    point_success_excess: str
    pgm_average_inverse_required: bool
    signed_centered_state_access_required: bool
    operator_norm_estimation_required: bool
    coherent_affine_effect_compiler_proved: bool
    inverse_polynomial_natural_success_excess_proved: bool
    status: str


@dataclass(frozen=True)
class PointLinearPOVMTheorem:
    effects: str
    positivity: str
    success: str
    stable_rank_criterion: str
    access_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointLinearPOVMReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointLinearPOVMTheorem
    finite_controls: list[PointLinearPOVMControl]
    scaling_records: list[LinearPOVMScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def linear_point_effects(
    states: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-12,
) -> tuple[tuple[np.ndarray, ...], float, float, float]:
    if len(states) < 2:
        raise ValueError("at least two point states are required")
    if any(state.shape != states[0].shape for state in states):
        raise ValueError("all point states must have the same shape")
    count = len(states)
    average = sum(states) / count
    centered = tuple(state - average for state in states)
    norms = tuple(float(np.linalg.norm(delta, ord=2)) for delta in centered)
    beta = max(norms)
    if beta <= tolerance:
        raise ValueError("point ensemble has zero centered signal")
    identity = np.eye(states[0].shape[0], dtype=states[0].dtype)
    effects = tuple(identity / count + delta / (count * beta) for delta in centered)
    signal = float(np.trace(centered[0].conj().T @ centered[0]).real)
    effective_rank = signal / beta**2
    return effects, beta, signal, effective_rank


def audit_linear_point_povm(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> PointLinearPOVMControl:
    states = point_quotient_states(labels)
    effects, beta, signal, effective_rank = linear_point_effects(states)
    identity = np.eye(states[0].shape[0])
    completeness = float(np.linalg.norm(sum(effects) - identity))
    eigenvalues = tuple(
        np.linalg.eigvalsh((effect + effect.conj().T) / 2) for effect in effects
    )
    minimum = min(float(values[0]) for values in eigenvalues)
    maximum = max(float(values[-1]) for values in eigenvalues)
    average = sum(states) / n
    norm_residual = max(
        abs(float(np.linalg.norm(state - average, ord=2)) - beta)
        for state in states
    )
    predicted = 1 / n + signal / (n * beta)
    observed = sum(
        float(np.trace(effect @ state).real)
        for effect, state in zip(effects, states)
    ) / n
    pgm, _, _ = _pretty_good_success(states, tolerance)
    verified = bool(
        minimum >= -100 * tolerance
        and maximum <= 2 / n + 100 * tolerance
        and completeness <= 100 * tolerance
        and norm_residual <= 100 * tolerance
        and abs(predicted - observed) <= 100 * tolerance
        and observed > 1 / n + 100 * tolerance
    )
    return PointLinearPOVMControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        register_dimension=states[0].shape[0],
        centered_hilbert_schmidt_norm_squared=signal,
        centered_operator_norm=beta,
        centered_effective_rank=effective_rank,
        minimum_effect_eigenvalue=minimum,
        maximum_effect_eigenvalue=maximum,
        povm_completeness_residual=completeness,
        covariance_norm_residual=norm_residual,
        predicted_linear_success=predicted,
        observed_linear_success=observed,
        linear_success_formula_residual=abs(predicted - observed),
        pretty_good_success=pgm,
        linear_minus_pretty_good_success=observed - pgm,
        random_guess_success=1 / n,
        linear_success_excess=observed - 1 / n,
        exact_linear_point_povm_verified=verified,
        status=(
            "exact-linear-covariant-point-povm"
            if verified
            else "linear-point-povm-validation-failure"
        ),
    )


def linear_povm_scaling_record(n: int) -> LinearPOVMScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    return LinearPOVMScalingRecord(
        n=n,
        point_hypothesis_count=n,
        sufficient_operator_norm_times_effective_rank=(
            "||Delta||_infinity r_eff >= n^-O(1)"
        ),
        point_success_excess=(
            "delta_n=||Delta||_2^2/(n||Delta||_infinity)="
            "||Delta||_infinity r_eff/n"
        ),
        pgm_average_inverse_required=False,
        signed_centered_state_access_required=True,
        operator_norm_estimation_required=True,
        coherent_affine_effect_compiler_proved=False,
        inverse_polynomial_natural_success_excess_proved=False,
        status="linear-point-povm-criterion-proved-physical-effect-access-open",
    )


def run_point_linear_povm() -> PointLinearPOVMReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_linear_point_povm(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_linear_point_povm(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_linear_point_povm(
            4,
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [linear_povm_scaling_record(n) for n in (16, 64, 256, 1024)]
    failures = sum(not row.exact_linear_point_povm_verified for row in controls)
    verified = failures == 0
    theorem = PointLinearPOVMTheorem(
        effects="M_j=I/n+Delta_j/(n||Delta_j||_infinity).",
        positivity=(
            "sum_j M_j=I and M_j>=0 because sum_j Delta_j=0 and "
            "spectrum(Delta_j) lies in [-beta,beta]."
        ),
        success=(
            "P_lin=1/n+||Delta||_2^2/(n||Delta||_infinity)."
        ),
        stable_rank_criterion=(
            "Success excess is ||Delta||_infinity r_eff/n, where "
            "r_eff=||Delta||_2^2/||Delta||_infinity^2."
        ),
        access_boundary=(
            "Unlike the PGM, no average-state inverse is needed; coherent signed "
            "access to Delta and its norm is still required."
        ),
        scope=(
            "The POVM is exact as an operator identity. No block encoding, Naimark "
            "dilation, efficient norm estimate, or natural stable-rank bound is proved."
        ),
        theorem_verified=verified,
        status=(
            "linear-point-povm-criterion-proved-effect-access-open"
            if verified
            else "linear-point-povm-validation-failure"
        ),
    )
    return PointLinearPOVMReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "construct_point_measurement_without_pgm_inverse",
                "resolved": verified,
                "resolution": (
                    "The isotropic centered ensemble yields an affine covariant POVM "
                    "with exact success controlled by two Schatten norms."
                ),
            },
            {
                "obligation": "prove_natural_linear_povm_success_excess",
                "resolved": False,
                "resolution": (
                    "Neither collision-free ||Delta||_2^2 nor ||Delta||_infinity has "
                    "an all-n bound strong enough to control their ratio."
                ),
            },
            {
                "obligation": "compile_signed_centered_state_effect",
                "resolved": False,
                "resolution": (
                    "Preparing tau and subgroup twirls does not by itself implement "
                    "the signed affine effect or its Naimark dilation."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The PGM multiplicity inverse is necessary for any nontrivial point decoder.",
                "resolved": True,
                "resolution": (
                    "False at the operator level. The linear POVM has positive finite "
                    "excess and in two controls exceeds the implemented PGM success."
                ),
            },
            {
                "objection": "The linear POVM is automatically implementable from copies of tau.",
                "resolved": False,
                "resolution": (
                    "No known generic procedure turns state preparation into the signed "
                    "effect Delta/beta at inverse-polynomial cost."
                ),
            },
            {
                "objection": "Hilbert--Schmidt energy alone lower-bounds success excess.",
                "resolved": False,
                "resolution": (
                    "Equation (2) also depends on the operator norm. A concentrated "
                    "standard harmonic may have poor effective rank."
                ),
            },
        ],
        headline_metrics={
            "exact_linear_point_povm_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "linear_beats_pgm_control_count": sum(
                row.linear_minus_pretty_good_success > 0 for row in controls
            ),
            "minimum_finite_linear_success_excess": min(
                row.linear_success_excess for row in controls
            ),
            "physical_affine_effect_compiler_count": 0,
            "natural_inverse_polynomial_success_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "linear_covariant_point_povm_proved": verified,
            "pgm_average_inverse_required_for_point_decoding": False,
            "natural_stable_rank_success_bound_proved": False,
            "signed_centered_state_block_encoding_proved": False,
            "coherent_linear_point_measurement_compiled": False,
            "inverse_polynomial_point_decoder_excess_proved": False,
            "polynomial_full_hidden_shift_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "An exact inverse-free POVM exists, but its natural norm ratio and "
                "physical signed-effect implementation are unproved."
            ),
        },
        status=theorem.status,
        summary=(
            "Replaced the PGM inverse as a logical necessity with a simpler affine "
            "point POVM. The active gates are now standard-harmonic stable rank and "
            "coherent signed-effect access."
        ),
        falsifiers_triggered=[
            (
                "Point decoding does not intrinsically require whitening the full "
                "average state; an exact linear covariant POVM can perform better."
            ),
            (
                "An operator-level POVM formula is not a circuit and does not resolve "
                "the physical access problem."
            ),
            (
                "Positive standard energy alone is insufficient without operator-norm "
                "or effective-rank control."
            ),
        ],
    )


def write_point_linear_povm_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POINT-LINEAR-POVM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_point_linear_povm" in globals():
        report = run_point_linear_povm(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-POINT-LINEAR-POVM",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POINT-LINEAR-POVM.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POINT-LINEAR-POVM.",
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
                    "self_dual_wreath_point_linear_povm": str(path)
                },
            )
        )
    return payload
