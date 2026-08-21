"""Convex separation test for adaptive MRS transcript POVMs.

For a fixed measured sieve policy, let ``{E_t}`` be the POVM of complete
classical transcripts.  A binary final guess based only on that transcript has
decision effect

    N_f = sum_t f_t E_t,                 0 <= f_t <= 1.    (1)

Randomized postprocessing is included by allowing fractional ``f_t``.  Hence
the exact transcript-only effect set is a compact convex zonotope

    Z(E) = {sum_t f_t E_t : f in [0,1]^T}.                (2)

A physical decision effect ``M`` is simulable by this fixed transcript POVM
iff its distance from ``Z(E)`` is zero.  Hilbert--Schmidt projection is a
box-constrained least-squares problem.  If ``N`` is the closest point and
``R=M-N``, projection optimality gives the exact dual witness

    <R,M> - sup_(Q in Z(E)) <R,Q> = ||R||_2^2,            (3)

where

    sup_(Q in Z(E)) <R,Q> = sum_t max(0,<R,E_t>).         (4)

After normalizing ``R``, equations (3)-(4) certify separation by exactly the
Hilbert--Schmidt distance.  The extremal eigenstate of ``R`` also gives an
explicit decision-probability discrepancy against the closest transcript
postprocessing.

This module compiles a two-stage adaptive measurement into its transcript
POVM and validates classical, off-diagonal, within-isotype, and genuinely
nonprojective sequential controls.  It does not construct the transcript POVM
of the repository's proposed physical PGM compiler, nor does separation from
one fixed policy establish separation from every policy allowed by the MRS
algorithm class.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import lsq_linear

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_mrs_transcript_povm_separation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PRIMARY_SOURCE_URL = "https://arxiv.org/abs/quant-ph/0612089"


@dataclass(frozen=True)
class TranscriptPovmSeparationControl:
    control_id: str
    hilbert_dimension: int
    transcript_outcome_count: int
    optimal_postprocessing_coefficients: tuple[float, ...]
    coefficient_minimum: float
    coefficient_maximum: float
    transcript_povm_completeness_residual: float
    candidate_effect_validity_residual: float
    hilbert_schmidt_separation_distance: float
    operator_norm_separation_from_hs_projection: float
    dual_witness_support_gap: float
    dual_witness_distance_identity_residual: float
    extremal_state_decision_probability_difference: float
    candidate_in_fixed_transcript_postprocessing_zonotope: bool
    exact_convex_separation_certificate_verified: bool
    status: str


@dataclass(frozen=True)
class AdaptiveTranscriptPovmControl:
    control_id: str
    hilbert_dimension: int
    first_stage_outcome_count: int
    second_stage_outcome_counts: tuple[int, ...]
    transcript_outcome_count: int
    first_stage_completeness_residual: float
    maximum_conditional_povm_completeness_residual: float
    compiled_transcript_povm_completeness_residual: float
    exact_adaptive_transcript_povm_compilation_verified: bool
    status: str


@dataclass(frozen=True)
class MrsTranscriptPovmSeparationReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    separation_controls: list[TranscriptPovmSeparationControl]
    adaptive_control: AdaptiveTranscriptPovmControl
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian_real_vector(matrix: np.ndarray) -> np.ndarray:
    """Real vectorization preserving the Hilbert--Schmidt inner product."""

    return np.concatenate((matrix.real.reshape(-1), matrix.imag.reshape(-1)))


def _effect_validity_residual(effect: np.ndarray) -> float:
    hermitian = (effect + effect.conj().T) / 2.0
    values = np.linalg.eigvalsh(hermitian)
    hermitian_residual = float(np.linalg.norm(effect - effect.conj().T, ord=2))
    lower = max(0.0, -float(values[0]))
    upper = max(0.0, float(values[-1]) - 1.0)
    return max(hermitian_residual, lower, upper)


def _validate_transcript_povm(
    effects: tuple[np.ndarray, ...],
) -> tuple[int, float, float]:
    if not effects:
        raise ValueError("at least one transcript effect is required")
    dimension = effects[0].shape[0]
    if any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("all transcript effects must share one square shape")
    identity = np.eye(dimension, dtype=complex)
    completeness = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    validity = max(_effect_validity_residual(effect) for effect in effects)
    return dimension, completeness, validity


def audit_transcript_povm_separation(
    control_id: str,
    transcript_effects: tuple[np.ndarray, ...],
    candidate_effect: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> TranscriptPovmSeparationControl:
    dimension, completeness, transcript_validity = _validate_transcript_povm(
        transcript_effects
    )
    if candidate_effect.shape != (dimension, dimension):
        raise ValueError("candidate effect and transcript POVM dimensions differ")
    candidate_validity = _effect_validity_residual(candidate_effect)
    validity = max(transcript_validity, candidate_validity)
    if max(completeness, validity) > 1000 * tolerance:
        raise ValueError("invalid transcript POVM or candidate decision effect")

    columns = np.column_stack(
        tuple(_hermitian_real_vector(effect) for effect in transcript_effects)
    )
    target = _hermitian_real_vector(candidate_effect)
    solution = lsq_linear(
        columns,
        target,
        bounds=(0.0, 1.0),
        tol=1e-13,
        lsmr_tol=1e-13,
        max_iter=10_000,
    )
    if not solution.success:
        raise ArithmeticError("box-constrained transcript projection failed")
    coefficients = np.clip(solution.x, 0.0, 1.0)
    approximation = sum(
        (
            coefficient * effect
            for coefficient, effect in zip(coefficients, transcript_effects)
        ),
        np.zeros_like(candidate_effect),
    )
    residual = (candidate_effect - approximation)
    residual = (residual + residual.conj().T) / 2.0
    hs_distance = float(np.linalg.norm(residual, ord="fro"))
    operator_distance = float(np.linalg.norm(residual, ord=2))
    if hs_distance > 100 * tolerance:
        witness = residual / hs_distance
        support = sum(
            max(0.0, float(np.trace(witness @ effect).real))
            for effect in transcript_effects
        )
        gap = float(np.trace(witness @ candidate_effect).real) - support
    else:
        gap = 0.0
    dual_residual = abs(gap - hs_distance)
    values = np.linalg.eigvalsh(residual)
    extremal_difference = max(abs(float(values[0])), abs(float(values[-1])))
    inside = hs_distance <= 1000 * tolerance
    verified = bool(
        dual_residual <= 10_000 * tolerance
        and abs(extremal_difference - operator_distance) <= 1000 * tolerance
    )
    return TranscriptPovmSeparationControl(
        control_id=control_id,
        hilbert_dimension=dimension,
        transcript_outcome_count=len(transcript_effects),
        optimal_postprocessing_coefficients=tuple(float(value) for value in coefficients),
        coefficient_minimum=float(coefficients.min()),
        coefficient_maximum=float(coefficients.max()),
        transcript_povm_completeness_residual=completeness,
        candidate_effect_validity_residual=validity,
        hilbert_schmidt_separation_distance=hs_distance,
        operator_norm_separation_from_hs_projection=operator_distance,
        dual_witness_support_gap=gap,
        dual_witness_distance_identity_residual=dual_residual,
        extremal_state_decision_probability_difference=extremal_difference,
        candidate_in_fixed_transcript_postprocessing_zonotope=inside,
        exact_convex_separation_certificate_verified=verified,
        status=(
            "exact-fixed-transcript-postprocessing-simulation"
            if verified and inside
            else "exact-fixed-transcript-povm-separation-witness"
            if verified
            else "transcript-povm-separation-control-failure"
        ),
    )


def compile_two_stage_adaptive_transcript_povm(
    first_stage_kraus: tuple[np.ndarray, ...],
    conditional_second_stage_effects: tuple[tuple[np.ndarray, ...], ...],
    *,
    tolerance: float = 1e-9,
) -> tuple[tuple[np.ndarray, ...], AdaptiveTranscriptPovmControl]:
    if not first_stage_kraus:
        raise ValueError("at least one first-stage outcome is required")
    if len(first_stage_kraus) != len(conditional_second_stage_effects):
        raise ValueError("each first-stage outcome needs one conditional POVM")
    dimension = first_stage_kraus[0].shape[1]
    if any(kraus.shape != (dimension, dimension) for kraus in first_stage_kraus):
        raise ValueError("square equal-dimension Kraus controls are required")
    identity = np.eye(dimension, dtype=complex)
    first_residual = float(
        np.linalg.norm(
            sum(
                (kraus.conj().T @ kraus for kraus in first_stage_kraus),
                np.zeros_like(identity),
            )
            - identity,
            ord=2,
        )
    )
    conditional_residual = 0.0
    transcript = []
    for kraus, conditional in zip(
        first_stage_kraus,
        conditional_second_stage_effects,
    ):
        _, completeness, validity = _validate_transcript_povm(conditional)
        conditional_residual = max(
            conditional_residual,
            completeness,
            validity,
        )
        transcript.extend(
            kraus.conj().T @ effect @ kraus
            for effect in conditional
        )
    transcript_tuple = tuple(transcript)
    _, compiled_residual, compiled_validity = _validate_transcript_povm(
        transcript_tuple
    )
    verified = max(
        first_residual,
        conditional_residual,
        compiled_residual,
        compiled_validity,
    ) <= 1000 * tolerance
    return transcript_tuple, AdaptiveTranscriptPovmControl(
        control_id="TWO-STAGE-WEAK-Z-THEN-ADAPTIVE-X-TRANSCRIPT",
        hilbert_dimension=dimension,
        first_stage_outcome_count=len(first_stage_kraus),
        second_stage_outcome_counts=tuple(
            len(conditional) for conditional in conditional_second_stage_effects
        ),
        transcript_outcome_count=len(transcript_tuple),
        first_stage_completeness_residual=first_residual,
        maximum_conditional_povm_completeness_residual=conditional_residual,
        compiled_transcript_povm_completeness_residual=compiled_residual,
        exact_adaptive_transcript_povm_compilation_verified=verified,
        status=(
            "exact-two-stage-adaptive-transcript-povm-compiled"
            if verified
            else "adaptive-transcript-povm-control-failure"
        ),
    )


def _projective_controls() -> list[TranscriptPovmSeparationControl]:
    first = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    second = np.eye(4, dtype=complex) - first
    transcript = (first, second)
    classical = 0.8 * first + 0.2 * second
    within_block = np.diag([1.0, 0.0, 0.5, 0.5]).astype(complex)

    zero = np.asarray([[1.0], [0.0]], dtype=complex)
    one = np.asarray([[0.0], [1.0]], dtype=complex)
    plus = (zero + one) / math.sqrt(2.0)
    qubit_transcript = (zero @ zero.conj().T, one @ one.conj().T)
    coherent = plus @ plus.conj().T
    return [
        audit_transcript_povm_separation(
            "PROJECTIVE-BLOCK-SCALAR-CLASSICAL-CONTROL",
            transcript,
            classical,
        ),
        audit_transcript_povm_separation(
            "PROJECTIVE-WITHIN-BLOCK-QUANTUM-WITNESS",
            transcript,
            within_block,
        ),
        audit_transcript_povm_separation(
            "PROJECTIVE-OFFDIAGONAL-COHERENCE-WITNESS",
            qubit_transcript,
            coherent,
        ),
    ]


def _adaptive_control() -> tuple[
    AdaptiveTranscriptPovmControl,
    TranscriptPovmSeparationControl,
]:
    first_kraus = (
        np.diag(np.sqrt([0.8, 0.2])).astype(complex),
        np.diag(np.sqrt([0.2, 0.8])).astype(complex),
    )
    plus = np.asarray([[1.0], [1.0]], dtype=complex) / math.sqrt(2.0)
    minus = np.asarray([[1.0], [-1.0]], dtype=complex) / math.sqrt(2.0)
    x_povm = (plus @ plus.conj().T, minus @ minus.conj().T)
    transcript, control = compile_two_stage_adaptive_transcript_povm(
        first_kraus,
        (x_povm, x_povm),
    )
    sigma_y = np.asarray([[0.0, -1j], [1j, 0.0]], dtype=complex)
    y_effect = (np.eye(2, dtype=complex) + sigma_y) / 2.0
    separation = audit_transcript_povm_separation(
        "ADAPTIVE-REAL-TRANSCRIPT-VERSUS-Y-EFFECT",
        transcript,
        y_effect,
    )
    return control, separation


def run_mrs_transcript_povm_separation() -> MrsTranscriptPovmSeparationReport:
    controls = _projective_controls()
    adaptive, adaptive_separation = _adaptive_control()
    controls.append(adaptive_separation)
    failures = sum(
        not row.exact_convex_separation_certificate_verified
        for row in controls
    ) + int(not adaptive.exact_adaptive_transcript_povm_compilation_verified)
    classical = controls[0]
    within = controls[1]
    coherent = controls[2]
    sequential = controls[3]
    exact = failures == 0
    return MrsTranscriptPovmSeparationReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "MRS-2007-QUANTUM-SIEVE-NO-GO",
                "title": "On the impossibility of a quantum sieve algorithm for graph isomorphism: unconditional results",
                "url": PRIMARY_SOURCE_URL,
                "scope": "Section 3 defines the adaptive measured pair-combination sieve whose complete irrep-labeled forest is a classical transcript.",
            }
        ],
        theorem_contract={
            "fixed_transcript_effect_set": (
                "All binary decisions obtained from a fixed transcript POVM "
                "are exactly the zonotope {sum_t f_t E_t:0<=f_t<=1}."
            ),
            "convex_projection_test": (
                "Membership is equivalent to zero box-constrained least-squares "
                "distance in Hermitian effect space."
            ),
            "dual_witness": (
                "The normalized projection residual has support-function gap "
                "equal to the Hilbert--Schmidt distance and is an exact "
                "separating witness."
            ),
            "adaptive_transcript_compilation": (
                "A two-stage adaptive measurement with first Kraus K_a and "
                "conditional effects F_(b|a) has transcript effects "
                "E_(a,b)=K_a^*F_(b|a)K_a."
            ),
            "scope": (
                "The criterion is exact for one specified transcript POVM. "
                "The physical PGM transcript effect and separation from every "
                "allowed adaptive MRS policy remain unconstructed."
            ),
        },
        separation_controls=controls,
        adaptive_control=adaptive,
        proof_obligations=[
            {
                "obligation": "exact_fixed_transcript_postprocessing_criterion",
                "resolved": exact,
                "resolution": "Classical randomized decisions give the effect zonotope exactly; convex projection and its support-function dual certify membership or separation."
            },
            {
                "obligation": "compile_adaptive_measurement_tree_to_transcript_povm",
                "resolved": adaptive.exact_adaptive_transcript_povm_compilation_verified,
                "resolution": "The Kraus pullback formula compiles every terminal branch and the finite weak-Z/X control sums to identity."
            },
            {
                "obligation": "construct_physical_recursive_pgm_decision_effect_and_mrs_transcript_povm",
                "resolved": False,
                "resolution": "Specify one complete physical compiler and an allowed measured-sieve policy on the same input space before running the separation optimization."
            },
            {
                "obligation": "separate_physical_effect_from_all_allowed_mrs_policies_on_positive_mass",
                "resolved": False,
                "resolution": "One fixed-policy witness is insufficient; need a structural invariant or optimization over the full adaptive policy class, with accepted-state weighting."
            },
        ],
        adversarial_audit=[
            {
                "objection": "A nonzero off-diagonal block is the only possible MRS transcript separation witness.",
                "resolved": True,
                "resolution": "False. The within-block projective control has no cross-block coherence but lies a positive distance from the block-scalar transcript zonotope."
            },
            {
                "objection": "Projective block tests cover adaptive nonprojective transcripts.",
                "resolved": True,
                "resolution": "False in general. The sequential Kraus pullback produces a nonprojective POVM, whose postprocessing zonotope must be tested directly."
            },
            {
                "objection": "Separation from one selected adaptive transcript proves escape from the MRS theorem.",
                "resolved": False,
                "resolution": "A different allowed sieve policy may realize the same decision effect. Full model separation needs a policy-independent obstruction."
            },
            {
                "objection": "Effect-space separation proves an efficient quantum algorithm.",
                "resolved": True,
                "resolution": "False. It addresses only simulation by one classical transcript POVM, not implementation, correctness, accepted mass, decoding, or classical hardness."
            },
        ],
        headline_metrics={
            "fixed_transcript_zonotope_criterion_theorem_count": int(exact),
            "dual_separation_witness_theorem_count": int(exact),
            "adaptive_transcript_povm_compiler_theorem_count": int(adaptive.exact_adaptive_transcript_povm_compilation_verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "classical_simulable_control_count": int(classical.candidate_in_fixed_transcript_postprocessing_zonotope),
            "within_block_separation_control_count": int(not within.candidate_in_fixed_transcript_postprocessing_zonotope),
            "offdiagonal_separation_control_count": int(not coherent.candidate_in_fixed_transcript_postprocessing_zonotope),
            "adaptive_nonprojective_separation_control_count": int(not sequential.candidate_in_fixed_transcript_postprocessing_zonotope),
            "physical_pgm_fixed_policy_separation_count": 0,
            "physical_pgm_full_mrs_model_separation_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_fixed_transcript_postprocessing_separation_test_proved": exact,
            "adaptive_transcript_povm_compilation_proved": adaptive.exact_adaptive_transcript_povm_compilation_verified,
            "offdiagonal_coherence_required_for_separation": False,
            "projective_dephasing_test_sufficient_for_general_adaptive_mrs": False,
            "current_physical_pgm_effect_constructed": False,
            "current_physical_pgm_outside_one_fixed_mrs_policy": False,
            "current_physical_pgm_outside_full_mrs_algorithm_class": False,
            "mrs_lower_bound_avoided": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact convex test now exists, but neither the complete "
                "physical decision effect nor a policy-independent separation "
                "from the adaptive MRS class has been supplied."
            ),
        },
        status=(
            "mrs-transcript-povm-zonotope-separation-proved-physical-model-separation-open"
            if exact
            else "mrs-transcript-povm-separation-control-failure"
        ),
        summary=(
            "Converted the MRS model boundary into an executable convex effect-"
            "space separation problem with exact dual witnesses and adaptive "
            "transcript-POVM compilation, while keeping every physical escape "
            "claim closed."
        ),
        falsifiers_triggered=[
            "Off-diagonal coherence is sufficient but not necessary for transcript-only separation.",
            "A fixed projective dephasing test is not the full adaptive MRS criterion.",
            "Separation from one fixed transcript policy is not separation from the whole MRS algorithm class.",
            "Effect-space separation would not itself prove an efficient algorithm or speedup.",
        ],
    )


def write_mrs_transcript_povm_separation_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_mrs_transcript_povm_separation())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_mrs_transcript_povm_separation_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
