"""Exact dephasing criterion for escaping the MRS sieve model.

Moore, Russell, and Sniady define a Clebsch--Gordan sieve that weakly Fourier
samples each coset state and then repeatedly selects two current states,
measures an irrep in their tensor-product decomposition, destroys the inputs,
and adaptively continues using the classical forest transcript.  Their lower
bound applies to that measured-transcript class, not automatically to every
coherent multiregister measurement.

Deferred measurement alone does not create an escape.  Let ``{P_t}`` be the
orthogonal projectors onto all internal transcript labels of a fixed binary
combination tree and define transcript dephasing

    Delta(X) = sum_t P_t X P_t.                            (1)

For a final decision effect ``M`` and input state ``rho``, measuring the
transcript first changes the probability by

    tr(M rho) - tr(M Delta(rho))
      = tr((M-Delta(M)) rho).                              (2)

Therefore the decision statistics are invariant under transcript measurement
for every input iff

    M = Delta(M).                                         (3)

Equation (3) is only the exact *coherence-loss* gate.  A circuit that merely stores
irrep labels coherently but subsequently uses only label-controlled unitaries
and label-diagonal measurements remains dephasing invariant and is still
compatible with measuring the label early.

The MRS algorithm makes its final guess from the classical transcript itself.
For an orthogonal projective transcript, define the block-scalar conditional
expectation

    C(X) = sum_t tr(P_t X)/tr(P_t) P_t.                    (4)

The decision probability depends only on the classical block probabilities
``tr(P_t rho)`` for every input iff ``M=C(M)``.  Thus an off-diagonal block is
a sufficient but not necessary escape witness: a block-diagonal effect that is
nonscalar inside one transcript block also uses quantum information absent
from the classical transcript.  For a general sequential transcript POVM
``{E_t}``, the exact simulable decision effects are ``sum_t f_t E_t`` with
``0<=f_t<=1``.  The projective test here is the fixed-tree special case, not a
complete analysis of the adaptive MRS transcript POVM.  The companion
``self_dual_wreath_mrs_transcript_povm_separation`` module turns this general
criterion into a box-constrained convex projection with an exact dual witness.

Different GPE recoupling trees can in principle generate such blocks because
isotypic projectors for different associations need not commute.  Pair GPE by
itself is block diagonal in its carrier label and is not an off-diagonal
witness.  The
repository's finite S6 noncommuting component effects are a structural signal,
not yet a formal witness in the MRS transcript projectors.  No claim that the
current architecture escapes the lower bound is made.

Primary source: Moore, Russell, Sniady, arXiv:quant-ph/0612089, Section 3.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_mrs_coherence_escape_criterion.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PRIMARY_SOURCE_URL = "https://arxiv.org/abs/quant-ph/0612089"


@dataclass(frozen=True)
class TranscriptCoherenceControl:
    control_id: str
    hilbert_dimension: int
    transcript_block_dimensions: tuple[int, ...]
    decision_effect_dephasing_residual: float
    decision_effect_transcript_algebra_residual: float
    decision_effect_maximum_offdiagonal_block_norm: float
    coherent_decision_probability: float
    transcript_dephased_decision_probability: float
    transcript_classicalized_decision_probability: float
    decision_probability_difference: float
    transcript_only_probability_difference: float
    trace_identity_residual: float
    transcript_measurement_changes_statistics: bool
    transcript_measurement_preserves_statistics_for_all_inputs: bool
    transcript_only_simulation_valid_for_all_inputs: bool
    exact_dephasing_identity_verified: bool
    status: str


@dataclass(frozen=True)
class MrsCoherenceEscapeCriterionReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    controls: list[TranscriptCoherenceControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def transcript_dephase(
    matrix: np.ndarray,
    block_dimensions: tuple[int, ...],
) -> np.ndarray:
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    if not block_dimensions or any(dimension < 1 for dimension in block_dimensions):
        raise ValueError("positive transcript block dimensions are required")
    if sum(block_dimensions) != matrix.shape[0]:
        raise ValueError("transcript blocks must partition the matrix dimension")
    output = np.zeros_like(matrix)
    offset = 0
    for dimension in block_dimensions:
        block = slice(offset, offset + dimension)
        output[block, block] = matrix[block, block]
        offset += dimension
    return output


def transcript_classicalize(
    matrix: np.ndarray,
    block_dimensions: tuple[int, ...],
) -> np.ndarray:
    """Project an effect onto the block-scalar classical transcript algebra."""

    dephased = transcript_dephase(matrix, block_dimensions)
    output = np.zeros_like(matrix)
    offset = 0
    for dimension in block_dimensions:
        block = slice(offset, offset + dimension)
        scalar = np.trace(dephased[block, block]) / dimension
        output[block, block] = scalar * np.eye(dimension, dtype=matrix.dtype)
        offset += dimension
    return output


def _maximum_offdiagonal_block_norm(
    matrix: np.ndarray,
    block_dimensions: tuple[int, ...],
) -> float:
    offsets = np.cumsum((0, *block_dimensions))
    return max(
        (
            float(
                np.linalg.norm(
                    matrix[
                        offsets[left] : offsets[left + 1],
                        offsets[right] : offsets[right + 1],
                    ],
                    ord=2,
                )
            )
            for left in range(len(block_dimensions))
            for right in range(len(block_dimensions))
            if left != right
        ),
        default=0.0,
    )


def audit_transcript_coherence(
    control_id: str,
    decision_effect: np.ndarray,
    input_state: np.ndarray,
    block_dimensions: tuple[int, ...],
    *,
    tolerance: float = 1e-10,
) -> TranscriptCoherenceControl:
    if decision_effect.shape != input_state.shape:
        raise ValueError("decision effect and state must share one shape")
    if np.linalg.norm(input_state - input_state.conj().T, ord=2) > 100 * tolerance:
        raise ValueError("input state must be Hermitian")
    dephased_effect = transcript_dephase(decision_effect, block_dimensions)
    classical_effect = transcript_classicalize(decision_effect, block_dimensions)
    dephased_state = transcript_dephase(input_state, block_dimensions)
    coherent = float(np.trace(decision_effect @ input_state).real)
    measured = float(np.trace(decision_effect @ dephased_state).real)
    dual = float(np.trace(dephased_effect @ input_state).real)
    classical = float(np.trace(classical_effect @ input_state).real)
    residual = float(np.linalg.norm(decision_effect - dephased_effect, ord=2))
    algebra_residual = float(
        np.linalg.norm(decision_effect - classical_effect, ord=2)
    )
    difference = coherent - measured
    transcript_difference = coherent - classical
    identity_residual = abs((coherent - measured) - (coherent - dual))
    changes = abs(difference) > 100 * tolerance
    invariant = residual <= 100 * tolerance
    transcript_only = algebra_residual <= 100 * tolerance
    verified = identity_residual <= 1000 * tolerance
    return TranscriptCoherenceControl(
        control_id=control_id,
        hilbert_dimension=decision_effect.shape[0],
        transcript_block_dimensions=block_dimensions,
        decision_effect_dephasing_residual=residual,
        decision_effect_transcript_algebra_residual=algebra_residual,
        decision_effect_maximum_offdiagonal_block_norm=_maximum_offdiagonal_block_norm(
            decision_effect,
            block_dimensions,
        ),
        coherent_decision_probability=coherent,
        transcript_dephased_decision_probability=measured,
        transcript_classicalized_decision_probability=classical,
        decision_probability_difference=difference,
        transcript_only_probability_difference=transcript_difference,
        trace_identity_residual=identity_residual,
        transcript_measurement_changes_statistics=changes,
        transcript_measurement_preserves_statistics_for_all_inputs=invariant,
        transcript_only_simulation_valid_for_all_inputs=transcript_only,
        exact_dephasing_identity_verified=verified,
        status=(
            "exact-classical-transcript-only-control"
            if verified and transcript_only
            else "exact-offdiagonal-transcript-coherence-witness"
            if verified and changes
            else "exact-within-block-quantum-information-witness"
            if verified and invariant
            else "offdiagonal-effect-selected-state-insensitive"
            if verified
            else "transcript-dephasing-identity-failure"
        ),
    )


def _controls() -> list[TranscriptCoherenceControl]:
    zero = np.asarray([[1.0], [0.0]], dtype=complex)
    plus = np.asarray([[1.0], [1.0]], dtype=complex) / np.sqrt(2)
    rho_plus = plus @ plus.conj().T
    diagonal_effect = zero @ zero.conj().T
    coherent_effect = plus @ plus.conj().T

    # A label-controlled unitary can be fully coherent internally and still
    # have a label-diagonal pulled-back decision effect.
    controlled_phase = np.diag([1.0, -1.0]).astype(complex)
    pulled_back_diagonal = (
        controlled_phase.conj().T @ diagonal_effect @ controlled_phase
    )

    angle = np.pi / 6
    rotated = np.asarray(
        [[np.cos(angle)], [np.sin(angle)]],
        dtype=complex,
    )
    recoupled_effect = rotated @ rotated.conj().T
    within_block_effect = np.diag([1.0, 0.0, 0.5, 0.5]).astype(complex)
    within_block_state = np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex)
    return [
        audit_transcript_coherence(
            "MEASURED-TRANSCRIPT-DIAGONAL-EFFECT",
            diagonal_effect,
            rho_plus,
            (1, 1),
        ),
        audit_transcript_coherence(
            "COHERENT-HADAMARD-RECOMBINATION-WITNESS",
            coherent_effect,
            rho_plus,
            (1, 1),
        ),
        audit_transcript_coherence(
            "UNMEASURED-LABEL-CONTROL-WITHOUT-RECOMBINATION",
            pulled_back_diagonal,
            rho_plus,
            (1, 1),
        ),
        audit_transcript_coherence(
            "NONCOMMUTING-RECOUPLED-ISOTYPIC-EFFECT",
            recoupled_effect,
            rho_plus,
            (1, 1),
        ),
        audit_transcript_coherence(
            "BLOCK-DIAGONAL-WITHIN-ISOTYPE-QUANTUM-WITNESS",
            within_block_effect,
            within_block_state,
            (2, 2),
        ),
    ]


def run_mrs_coherence_escape_criterion() -> MrsCoherenceEscapeCriterionReport:
    controls = _controls()
    failures = sum(not row.exact_dephasing_identity_verified for row in controls)
    diagonal = controls[0]
    coherent = controls[1]
    controlled = controls[2]
    recoupled = controls[3]
    within_block = controls[4]
    verified = failures == 0
    return MrsCoherenceEscapeCriterionReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "MRS-2007-QUANTUM-SIEVE-NO-GO",
                "title": "On the impossibility of a quantum sieve algorithm for graph isomorphism: unconditional results",
                "url": PRIMARY_SOURCE_URL,
                "scope": "Section 3 defines adaptive pairwise combine-and-isotypic-measure sieves whose usable output is the classical irrep-labeled forest transcript.",
            }
        ],
        theorem_contract={
            "dephasing_duality": (
                "For transcript dephasing Delta, tr(M rho)-tr(M Delta(rho)) "
                "equals tr((M-Delta(M))rho)."
            ),
            "universal_invariance_criterion": (
                "Transcript measurement preserves the decision distribution "
                "for every input iff the pulled-back decision effect satisfies "
                "M=Delta(M)."
            ),
            "projective_transcript_only_criterion": (
                "For orthogonal transcript blocks, a decision depends only on "
                "the classical block probabilities for every input iff M equals "
                "its block-scalar conditional expectation C(M)."
            ),
            "mrs_model_boundary": (
                "The MRS sieve measures every internal isotypic label and uses "
                "only the resulting classical forest transcript for its guess. "
                "For the full sequential process, simulable effects are classical "
                "postprocessings sum_t f_t E_t of the transcript POVM."
            ),
            "escape_witness": (
                "A nonnegligible off-diagonal internal-label block is sufficient "
                "but not necessary: a nonscalar within-block effect also uses "
                "quantum information absent from a projective transcript."
            ),
            "scope": (
                "The block tests are exact for one projective transcript. A full "
                "MRS audit must construct the adaptive sequential transcript POVM. "
                "The companion zonotope solver tests any specified POVM, but no "
                "physical GPE/POVM or all-policy separation is proved."
            ),
        },
        controls=controls,
        proof_obligations=[
            {
                "obligation": "exact_measured_transcript_dephasing_criterion",
                "resolved": verified,
                "resolution": "Self-adjointness of block dephasing gives the trace identity, and invariance for all states is equivalent to zero off-diagonal effect blocks.",
            },
            {
                "obligation": "exact_projective_transcript_only_effect_criterion",
                "resolved": verified,
                "resolution": "Dependence only on block probabilities is equivalent by trace duality to a scalar decision coefficient on every transcript block.",
            },
            {
                "obligation": "show_current_physical_pgm_effect_outside_mrs_transcript_povm_postprocessing",
                "resolved": False,
                "resolution": "Construct the allowed adaptive transcript POVM {E_t} and lower-bound the distance of the physical decision effect from {sum_t f_t E_t:0<=f_t<=1} on positive accepted-state mass.",
            },
            {
                "obligation": "show_pair_gpe_alone_escapes_mrs_sieve",
                "resolved": True,
                "resolution": "Rejected as a sufficient argument: pair GPE is carrier-label block diagonal. It is not an off-diagonal witness, and no within-block or full transcript-POVM separation is proved.",
            },
            {
                "obligation": "separate_complete_recursive_compiler_from_mrs_formal_algorithm_class",
                "resolved": False,
                "resolution": "Need an explicit complete circuit first, then separate its decision POVM from all classical postprocessings of an allowed MRS transcript POVM or give a simulation.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Not measuring intermediate irrep labels automatically avoids the MRS theorem.",
                "resolved": True,
                "resolution": "False whenever the final effect is a classical postprocessing of the transcript POVM. Dephasing invariance alone is necessary but not sufficient for that simulation.",
            },
            {
                "objection": "Any noncommuting recoupling projector proves a useful model escape.",
                "resolved": False,
                "resolution": "It is only a candidate witness. Separation from the complete adaptive transcript-POVM postprocessing set must survive on nonnegligible accepted-state mass.",
            },
            {
                "objection": "The finite S6 component-effect commutator is already an MRS transcript witness.",
                "resolved": False,
                "resolution": "Those component effects have not been identified with the paper's internal isotypic transcript projectors, and their direct source mechanism is asymptotically negligible.",
            },
            {
                "objection": "Dephasing invariance proves classical transcript-only simulation.",
                "resolved": True,
                "resolution": "False for blocks of dimension greater than one. The within-isotype control is block diagonal but nonscalar, so early label measurement preserves it while the classical label alone does not simulate it.",
            },
            {
                "objection": "A dephasing witness proves a speedup.",
                "resolved": True,
                "resolution": "False. It only proves that one lower-bound model does not simulate the measurement; efficiency, correctness, and classical hardness remain separate."
            },
        ],
        headline_metrics={
            "transcript_dephasing_identity_theorem_count": int(verified),
            "universal_measured_transcript_invariance_criterion_count": int(verified),
            "projective_transcript_only_criterion_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "offdiagonal_coherence_witness_control_count": sum(
                row.transcript_measurement_changes_statistics for row in controls
            ),
            "within_block_quantum_witness_control_count": sum(
                row.transcript_measurement_preserves_statistics_for_all_inputs
                and not row.transcript_only_simulation_valid_for_all_inputs
                for row in controls
            ),
            "deferred_measurement_non_escape_control_count": int(
                controlled.transcript_only_simulation_valid_for_all_inputs
            ),
            "hadamard_witness_probability_difference": coherent.decision_probability_difference,
            "recoupled_witness_probability_difference": recoupled.decision_probability_difference,
            "within_block_transcript_only_probability_difference": (
                within_block.transcript_only_probability_difference
            ),
            "current_physical_pgm_transcript_povm_separation_count": 0,
            "mrs_model_escape_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_transcript_dephasing_criterion_proved": verified,
            "exact_projective_transcript_only_criterion_proved": verified,
            "offdiagonal_coherence_is_sufficient_not_necessary": (
                coherent.transcript_measurement_changes_statistics
                and within_block.transcript_measurement_preserves_statistics_for_all_inputs
                and not within_block.transcript_only_simulation_valid_for_all_inputs
            ),
            "measured_projective_transcript_control_is_classical": (
                diagonal.transcript_only_simulation_valid_for_all_inputs
            ),
            "deferred_measurement_alone_escapes_mrs": False,
            "pair_gpe_alone_proves_mrs_escape": False,
            "noncommuting_recoupling_can_create_abstract_witness": recoupled.transcript_measurement_changes_statistics,
            "current_physical_pgm_outside_mrs_transcript_postprocessing": False,
            "complete_recursive_compiler_outside_mrs_class_proved": False,
            "mrs_lower_bound_avoided": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The fixed-projective criteria are exact, but the physical PGM "
                "effect has not been separated from classical postprocessings "
                "of the full adaptive MRS transcript POVM on nonnegligible mass."
            ),
        },
        status=(
            "projective-transcript-criteria-proved-adaptive-mrs-separation-open"
            if verified
            else "mrs-coherence-escape-criterion-control-failure"
        ),
        summary=(
            "Corrected the MRS audit: dephasing invariance characterizes only "
            "whether early projective transcript measurement changes statistics; "
            "classical transcript-only simulation requires block-scalar effects, "
            "and full adaptive MRS separation remains open."
        ),
        falsifiers_triggered=[
            "Leaving intermediate irrep labels unmeasured is not by itself outside the measured-sieve model.",
            "Label-controlled coherent computation with a label-diagonal final effect is transcript-dephasing invariant.",
            "Dephasing invariance does not imply transcript-only simulation when an isotypic transcript block has dimension greater than one.",
            "Pair GPE is carrier-block diagonal and cannot alone witness cross-transcript interference.",
            "A finite noncommuting effect is not a useful escape until it changes the physical decision probability on positive mass.",
            "Avoiding the MRS model would not prove an efficient algorithm or quantum speedup.",
        ],
    )


def write_mrs_coherence_escape_criterion_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_mrs_coherence_escape_criterion())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_mrs_coherence_escape_criterion_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
