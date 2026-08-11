"""Outcome-Gram blindness to physical rows in Gelfand measurement reductions.

For a multiplicity-free homogeneous outcome representation and an arbitrary
physical representation, every intertwiner block has the form

    K_nu = sqrt(alpha_nu) I_(V_nu) tensor <a_nu|,

where ``a_nu`` is a unit vector in the physical multiplicity space.  Therefore

    K K^* = direct_sum_nu alpha_nu I_(V_nu)

is independent of every row orientation.  Even the complete singular spectrum
and every output Hecke/association-scheme moment know only ``alpha_nu``.  If a
physical multiplicity has dimension at least two, orthogonal choices of
``a_nu`` give orthogonal inverse-prepared row states with exactly the same
outcome Gram data.

This closes a tempting but invalid route after the arbitrary covariant
measurement reduction: commutative perfect-matching spectra cannot by
themselves provide the missing row-state verifier.  The result does not say
that arbitrary orientations arise from the natural hidden-involution PGM or
from a fixed coset-state source.  Source effects, a circuit dilation, or the PGM
polar factor can impose additional structure, and that is now the live target.
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
    "research/representation/coset_gelfand_row_orientation_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RowOrientationControl:
    control_id: str
    carrier_dimension: int
    physical_multiplicity: int
    singular_value_squared: float
    intertwiner_residual_left: float
    intertwiner_residual_right: float
    shared_output_gram_residual: float
    shared_singular_spectrum_residual: float
    inverse_row_overlap: float
    physical_support_operator_distance: float
    output_moment_residual: float
    carrier_algebra_observable_residual: float
    commutant_orientation_witness_gap: float
    orientation_blindness_verified: bool
    status: str


@dataclass(frozen=True)
class PerfectMatchingOrientationScaling:
    degree: int
    half_degree: int
    minimum_physical_multiplicity_decimal: str
    minimum_physical_multiplicity_log2: float
    minimum_row_orientation_real_dimension_decimal: str
    outcome_hecke_sector_count_upper_bound_decimal: str
    outcome_gram_determines_row_orientation: bool
    source_specific_row_constraint_derived: bool
    classically_checkable_row_observable_constructed: bool
    polynomial_hidden_involution_decoder_constructed: bool
    status: str


@dataclass(frozen=True)
class GelfandRowOrientationTheorem:
    block_family: str
    common_output_gram: str
    common_singular_data: str
    group_action_algebra_blindness: str
    orthogonal_row_counterexample: str
    universal_blindness_scope: str
    natural_source_scope_limit: str
    output_gram_orientation_blindness_proved: bool
    singular_value_orientation_blindness_proved: bool
    group_action_algebra_orientation_blindness_proved: bool
    natural_pgm_orientation_classified: bool
    row_state_verifier_constructed: bool
    polynomial_decoder_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class GelfandRowOrientationNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[RowOrientationControl]
    scaling_records: list[PerfectMatchingOrientationScaling]
    theorem: GelfandRowOrientationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _random_unitary(dimension: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0.0, phases / np.abs(phases), 1.0)
    return q @ np.diag(np.conjugate(phases))


def gelfand_row_intertwiner(
    carrier_dimension: int,
    physical_multiplicity: int,
    alpha: float,
    row: np.ndarray,
) -> np.ndarray:
    if carrier_dimension < 1 or physical_multiplicity < 1:
        raise ValueError("dimensions must be positive")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must lie in [0,1]")
    vector = np.asarray(row, dtype=np.complex128).reshape(-1)
    if vector.shape != (physical_multiplicity,):
        raise ValueError("row has the wrong multiplicity dimension")
    norm = np.linalg.norm(vector)
    if norm <= 0.0:
        raise ValueError("row must be nonzero")
    vector = vector / norm
    return math.sqrt(alpha) * np.kron(
        np.eye(carrier_dimension, dtype=np.complex128),
        np.conjugate(vector).reshape(1, -1),
    )


def row_orientation_control(
    control_id: str,
    carrier_dimension: int,
    physical_multiplicity: int,
    alpha: float,
    seed: int,
) -> RowOrientationControl:
    if physical_multiplicity < 2:
        raise ValueError("an orthogonal-row control needs multiplicity at least two")
    basis = _random_unitary(physical_multiplicity, seed)
    row_left = basis[:, 0]
    row_right = basis[:, 1]
    k_left = gelfand_row_intertwiner(
        carrier_dimension, physical_multiplicity, alpha, row_left
    )
    k_right = gelfand_row_intertwiner(
        carrier_dimension, physical_multiplicity, alpha, row_right
    )

    carrier_action = _random_unitary(carrier_dimension, seed + 1009)
    physical_action = np.kron(
        carrier_action,
        np.eye(physical_multiplicity, dtype=np.complex128),
    )
    intertwiner_left = np.linalg.norm(
        carrier_action @ k_left - k_left @ physical_action,
        ord=2,
    )
    intertwiner_right = np.linalg.norm(
        carrier_action @ k_right - k_right @ physical_action,
        ord=2,
    )

    output_left = k_left @ np.conjugate(k_left.T)
    output_right = k_right @ np.conjugate(k_right.T)
    shared_gram = np.linalg.norm(output_left - output_right, ord=2)
    singular_residual = float(
        np.max(
            np.abs(
                np.linalg.svd(k_left, compute_uv=False)
                - np.linalg.svd(k_right, compute_uv=False)
            )
        )
    )
    inverse_left = np.conjugate(k_left.T)[:, 0]
    inverse_right = np.conjugate(k_right.T)[:, 0]
    inverse_overlap = abs(
        np.vdot(inverse_left, inverse_right)
    ) / (np.linalg.norm(inverse_left) * np.linalg.norm(inverse_right))
    physical_distance = np.linalg.norm(
        np.conjugate(k_left.T) @ k_left
        - np.conjugate(k_right.T) @ k_right,
        ord=2,
    )
    moment_residual = max(
        abs(
            np.trace(np.linalg.matrix_power(output_left, power))
            - np.trace(np.linalg.matrix_power(output_right, power))
        )
        for power in range(1, 7)
    )
    rng = np.random.default_rng(seed + 2017)
    carrier_raw = rng.normal(
        size=(carrier_dimension, carrier_dimension)
    ) + 1j * rng.normal(size=(carrier_dimension, carrier_dimension))
    carrier_observable = (carrier_raw + np.conjugate(carrier_raw.T)) / 2.0
    physical_carrier_observable = np.kron(
        carrier_observable,
        np.eye(physical_multiplicity, dtype=np.complex128),
    )
    normalized_left = inverse_left / np.linalg.norm(inverse_left)
    normalized_right = inverse_right / np.linalg.norm(inverse_right)
    carrier_observable_residual = abs(
        np.vdot(
            normalized_left,
            physical_carrier_observable @ normalized_left,
        )
        - np.vdot(
            normalized_right,
            physical_carrier_observable @ normalized_right,
        )
    )
    multiplicity_witness = np.outer(row_left, np.conjugate(row_left)) - np.outer(
        row_right, np.conjugate(row_right)
    )
    commutant_witness = np.kron(
        np.eye(carrier_dimension, dtype=np.complex128),
        multiplicity_witness,
    )
    commutant_gap = abs(
        np.vdot(normalized_left, commutant_witness @ normalized_left)
        - np.vdot(normalized_right, commutant_witness @ normalized_right)
    )
    verified = bool(
        intertwiner_left < 1e-11
        and intertwiner_right < 1e-11
        and shared_gram < 1e-11
        and singular_residual < 1e-11
        and inverse_overlap < 1e-11
        and abs(physical_distance - alpha) < 1e-11
        and moment_residual < 1e-11
        and carrier_observable_residual < 1e-11
        and abs(commutant_gap - 2.0) < 1e-11
    )
    return RowOrientationControl(
        control_id=control_id,
        carrier_dimension=carrier_dimension,
        physical_multiplicity=physical_multiplicity,
        singular_value_squared=alpha,
        intertwiner_residual_left=float(intertwiner_left),
        intertwiner_residual_right=float(intertwiner_right),
        shared_output_gram_residual=float(shared_gram),
        shared_singular_spectrum_residual=singular_residual,
        inverse_row_overlap=float(inverse_overlap),
        physical_support_operator_distance=float(physical_distance),
        output_moment_residual=float(abs(moment_residual)),
        carrier_algebra_observable_residual=float(carrier_observable_residual),
        commutant_orientation_witness_gap=float(commutant_gap),
        orientation_blindness_verified=verified,
        status=(
            "identical-output-gram-orthogonal-physical-rows"
            if verified
            else "row-orientation-control-failure"
        ),
    )


def _partition_number(value: int) -> int:
    counts = [0] * (value + 1)
    counts[0] = 1
    for part in range(1, value + 1):
        for total in range(part, value + 1):
            counts[total] += counts[total - part]
    return counts[value]


def perfect_matching_orientation_scaling(
    degree: int,
) -> PerfectMatchingOrientationScaling:
    if degree < 4 or degree % 2:
        raise ValueError("degree must be even and at least four")
    half_degree = degree // 2
    group_order = math.factorial(degree)
    minimum_orientation_dimension = 2 * (group_order - 1)
    return PerfectMatchingOrientationScaling(
        degree=degree,
        half_degree=half_degree,
        minimum_physical_multiplicity_decimal=str(group_order),
        minimum_physical_multiplicity_log2=math.lgamma(degree + 1)
        / math.log(2.0),
        minimum_row_orientation_real_dimension_decimal=str(
            minimum_orientation_dimension
        ),
        outcome_hecke_sector_count_upper_bound_decimal=str(
            _partition_number(half_degree)
        ),
        outcome_gram_determines_row_orientation=False,
        source_specific_row_constraint_derived=False,
        classically_checkable_row_observable_constructed=False,
        polynomial_hidden_involution_decoder_constructed=False,
        status="outcome-spectrum-blind-source-specific-row-structure-open",
    )


def gelfand_row_orientation_theorem() -> GelfandRowOrientationTheorem:
    return GelfandRowOrientationTheorem(
        block_family=(
            "K_nu=sqrt(alpha_nu) I_(V_nu) tensor <a_nu| for arbitrary "
            "unit a_nu in the physical multiplicity space"
        ),
        common_output_gram=(
            "K K^*=direct_sum_nu alpha_nu I_(V_nu), independent of a_nu"
        ),
        common_singular_data=(
            "Each alpha_nu occurs dim(V_nu) times, so all singular values, "
            "ranks, Schatten norms, and output Hecke moments are orientation blind."
        ),
        group_action_algebra_blindness=(
            "On V_nu tensor M_nu, every operator generated by the G action is "
            "in End(V_nu) tensor I_(M_nu), so all of its outcome statistics "
            "are independent of a_nu. Orientation-sensitive observables must "
            "come from the commutant or additional source structure."
        ),
        orthogonal_row_counterexample=(
            "When dim(M_nu)>=2, orthogonal a_nu and b_nu produce orthogonal "
            "inverse row states but identical output Gram data."
        ),
        universal_blindness_scope=(
            "No statistic determined only by K K^*, its spherical spectrum, "
            "or singular values can recover or verify the physical row direction."
        ),
        natural_source_scope_limit=(
            "The theorem ranges over abstract intertwiners. It does not prove "
            "that all orientations arise from one fixed coset-state ensemble, "
            "the natural PGM, or a polynomial circuit family."
        ),
        output_gram_orientation_blindness_proved=True,
        singular_value_orientation_blindness_proved=True,
        group_action_algebra_orientation_blindness_proved=True,
        natural_pgm_orientation_classified=False,
        row_state_verifier_constructed=False,
        polynomial_decoder_constructed=False,
        theorem_verified=True,
        status="gelfand-output-gram-row-orientation-blindness-proved",
    )


def run_gelfand_row_orientation_no_go() -> GelfandRowOrientationNoGoReport:
    controls = [
        row_orientation_control("STD-M2", 2, 2, 0.73, 3101),
        row_orientation_control("STD-M3", 2, 3, 0.41, 6203),
        row_orientation_control("CARRIER3-M4", 3, 4, 0.89, 9301),
    ]
    scaling = [
        perfect_matching_orientation_scaling(degree)
        for degree in (8, 16, 32, 64, 128)
    ]
    theorem = gelfand_row_orientation_theorem()
    failures = sum(not row.orientation_blindness_verified for row in controls)
    verified = failures == 0 and theorem.theorem_verified
    metrics: dict[str, int | float] = {
        "output_gram_orientation_blindness_theorem_count": int(verified),
        "singular_spectrum_orientation_blindness_theorem_count": int(verified),
        "group_action_algebra_orientation_blindness_theorem_count": int(verified),
        "orthogonal_row_counterexample_count": sum(
            row.inverse_row_overlap < 1e-11 for row in controls
        ),
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "maximum_shared_output_gram_residual": max(
            row.shared_output_gram_residual for row in controls
        ),
        "maximum_shared_singular_spectrum_residual": max(
            row.shared_singular_spectrum_residual for row in controls
        ),
        "maximum_inverse_row_overlap": max(
            row.inverse_row_overlap for row in controls
        ),
        "maximum_carrier_algebra_observable_residual": max(
            row.carrier_algebra_observable_residual for row in controls
        ),
        "minimum_commutant_orientation_witness_gap": min(
            row.commutant_orientation_witness_gap for row in controls
        ),
        "maximum_scaling_minimum_physical_multiplicity_log2": max(
            row.minimum_physical_multiplicity_log2 for row in scaling
        ),
        "natural_pgm_orientation_classification_count": 0,
        "row_state_verifier_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return GelfandRowOrientationNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "outcome_representation": (
                "multiplicity-free direct sum of finite-group irreps"
            ),
            "physical_representation": (
                "same carrier irreps with arbitrary multiplicity spaces"
            ),
            "data_declared_blind": (
                "K K^*, spherical eigenvalues, singular values, ranks, and "
                "unitarily invariant output moments"
            ),
            "data_not_declared_blind": (
                "source-specific physical observables, circuit dilation, PGM "
                "polar factors, and K^*K in a known physical basis"
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "classify_multiplicity_free_intertwiner_blocks",
                "resolved": verified,
                "resolution": (
                    "Schur's lemma leaves one row vector a_nu for each live "
                    "physical multiplicity block."
                ),
            },
            {
                "obligation": "prove_output_gram_orientation_blindness",
                "resolved": verified,
                "resolution": (
                    "Direct multiplication removes a_nu because it has unit norm."
                ),
            },
            {
                "obligation": "construct_same_spectrum_orthogonal_rows",
                "resolved": verified,
                "resolution": (
                    "Choose orthogonal unit vectors in any multiplicity space "
                    "of dimension at least two."
                ),
            },
            {
                "obligation": "test_full_group_action_algebra_as_row_verifier",
                "resolved": verified,
                "resolution": (
                    "The group algebra is identity on physical multiplicity, "
                    "while an explicit commutant projector separates the rows."
                ),
            },
            {
                "obligation": "classify_natural_hidden_involution_pgm_rows",
                "resolved": False,
                "resolution": (
                    "This requires the source-specific k-copy frame or polar "
                    "factor and is not implied by covariance."
                ),
            },
            {
                "obligation": "derive_independent_row_state_verifier",
                "resolved": False,
                "resolution": (
                    "Outcome Hecke data are now proved insufficient; a physical "
                    "source relation or observable is required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The full scalar Hecke spectrum identifies the physical row.",
                "survives": False,
                "response": (
                    "Orthogonal rows give exactly the same scalar spectrum and "
                    "all of its moments."
                ),
            },
            {
                "challenge": "Adding all singular values fixes the ambiguity.",
                "survives": False,
                "response": (
                    "The singular spectrum is also independent of row orientation."
                ),
            },
            {
                "challenge": "Strong Fourier sampling or arbitrary group-action observables recover the row.",
                "survives": False,
                "response": (
                    "The represented group algebra acts trivially on the "
                    "multiplicity factor. Only commutant/source operations can "
                    "distinguish row orientations."
                ),
            },
            {
                "challenge": "The theorem rules out a PGM-specific verifier.",
                "survives": False,
                "response": (
                    "The natural PGM may constrain a_nu through its physical "
                    "frame; that structure is explicitly outside this theorem."
                ),
            },
            {
                "challenge": "The large orientation manifold proves a gate lower bound.",
                "survives": False,
                "response": (
                    "No circuit lower bound follows from Hilbert-space dimension."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "MALEKI-RAZAFIMAHATRATRA-2023",
                "title": (
                    "On cocliques in commutative Schurian association schemes "
                    "of the symmetric group"
                ),
                "url": "https://arxiv.org/abs/2307.02844",
                "use": "Perfect-matching Gelfand-pair setting",
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "outcome_gram_can_determine_physical_row_orientation": False,
            "spherical_singular_data_can_verify_inverse_row_state": False,
            "group_action_algebra_can_verify_inverse_row_orientation": False,
            "commutant_or_source_specific_operation_required": True,
            "source_specific_pgm_row_structure_still_open": True,
            "natural_pgm_row_orientation_classified": False,
            "row_state_verifier_constructed": False,
            "polynomial_hidden_involution_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
            "All commutative outcome-side data are exactly blind to the "
                "physical row orientation, and the full represented group "
                "algebra is identity on multiplicity. Only commutant or "
                "source-specific structure can support the missing verifier."
            ),
        },
        status=(
            "gelfand-output-gram-row-blind-source-structure-open"
            if verified
            else "gelfand-row-orientation-control-failure"
        ),
        summary=(
            "Proved that multiplicity-free outcome spectra and all singular "
            "data cannot identify the inverse-prepared physical row; the "
            "remaining route must exploit the natural PGM/source frame rather "
            "than the perfect-matching association scheme alone."
        ),
        falsifiers_triggered=[
            "Complete spherical eigenvalue data do not determine physical row orientation.",
            "Complete singular-value data do not determine physical row orientation.",
            "The full represented group-action algebra is blind to physical multiplicity-row orientation.",
            "Orthogonal inverse row states can share identical outcome Gram and Hecke moments.",
            "The orientation ambiguity is not by itself a circuit lower bound.",
            "Only source-specific PGM or dilation structure remains a possible verifier route.",
            "No hidden-involution decoder or speedup is implied.",
        ],
    )


def write_gelfand_row_orientation_no_go(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_gelfand_row_orientation_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG--GELFAND-ROW-ORIENTATION-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "coset_gelfand_row_orientation_no_go": str(path)
                },
            )
        )
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG--GELFAND-ROW-ORIENTATION-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "coset_gelfand_row_orientation_no_go": str(path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    output = write_gelfand_row_orientation_no_go()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
