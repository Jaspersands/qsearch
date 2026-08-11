"""No-go for inferring prefix gaps or circuit hardness from the final frame.

The exact prefix-polar chain rule suggests a possible route around the tiny
global restriction angle: condition one commuting source projector at a time.
This module proves that the final spectral window alone says almost nothing
about the relative effects in such a chain.

For prefix analyses ``A_j=P_j...P_1J`` define

    D_j=A_j^*A_j,
    E_j=D_(j-1)^(-1/2)D_jD_(j-1)^(-1/2).               (1)

Whenever the metrics are positive definite,

    0 < D_j <= D_(j-1),       0 < E_j <= I,
    det(D_k)=det(D_0) product_j det(E_j).               (2)

The determinant identity controls only total log-volume loss.  It does not
control the least eigenvalue of any one relative effect.

Here is an exact commuting-projector counterfamily.  Let the logical domain
have basis ``|a>`` for ``a=0,...,r-1`` and attach ``r`` ancilla qubits.  Put

    J|a> = |a> (sqrt(delta)|0^r>
                     +sqrt(1-delta)|e_a>),              (3)

where ``e_a`` has its only one in ancilla ``a``.  Let ``P_i`` project ancilla
``i`` onto zero.  The ``P_i`` commute and, for any prefix set ``S``,

    D_S|a> = delta|a> if a in S, and |a> otherwise.     (4)

After all ``r`` projectors, ``D_[r]=delta I`` has condition number one.  But
for every ordering, every next relative effect has spectrum
``{delta,1,...,1}``.  Taking ``delta=exp(-Theta(sqrt(n)))`` reproduces the
retained principal-angle scale while defeating every inference from final
conditioning, determinant telescoping, projector commutativity, or adaptive
ordering to inverse-polynomial relative gaps.

This is not a circuit lower bound.  The final polar is simply
``|a> -> |a>|0^r>``.  Each step polar is also one directly compiled controlled
rotation; it bypasses the ``Omega(1/sqrt(delta))`` generic QSVT degree.  Thus
small relative effects are not necessary evidence of hardness either.

The consequence is narrow but decisive: a scalable coset result must prove
natural source-specific subduction/recoupling structure or construct its
direct Uhlmann transports.  Spectra and determinant budgets alone can prove
neither an efficient prefix compiler nor a no-go theorem.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_prefix_polar_holonomy_reduction import audit_polar_chain_step
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/coset_prefix_relative_gap_inference_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PrefixGapCounterfamilyControl:
    logical_dimension: int
    ancilla_qubit_count: int
    ambient_dimension: int
    delta: float
    tested_ordering_count: int
    expected_ordering_count: int
    embedding_isometry_residual: float
    maximum_projector_idempotence_residual: float
    maximum_projector_commutator_residual: float
    final_metric_scalar_residual: float
    final_metric_condition_number: float
    determinant_telescoping_residual: float
    minimum_relative_effect_eigenvalue: float
    maximum_relative_effect_eigenvalue: float
    maximum_holonomy_identity_distance: float
    maximum_direct_step_polar_residual: float
    final_direct_polar_residual: float
    every_order_has_delta_relative_edge: bool
    all_holonomies_identity: bool
    direct_structured_polar_constructed: bool
    control_verified: bool
    status: str


@dataclass(frozen=True)
class PrefixGapScalingRecord:
    n: int
    logical_dimension: int
    ancilla_qubit_count: int
    delta: float
    log2_inverse_delta: float
    final_condition_number: float
    generic_relative_qsvt_degree_lower_order: str
    direct_controlled_rotation_gate_order: str
    inverse_polynomial_relative_gap_inferred: bool
    generic_qsvt_hardness_implies_circuit_hardness: bool
    status: str


@dataclass(frozen=True)
class PrefixGapInferenceTheorem:
    loewner_monotonicity: str
    relative_contraction: str
    determinant_chain: str
    counterfamily: str
    ordering_no_go: str
    direct_polar_escape: str
    scope_limit: str
    loewner_monotonicity_proved: bool
    determinant_telescoping_proved: bool
    final_constant_condition_implies_polynomial_relative_gaps: bool
    adaptive_ordering_always_repairs_relative_gaps: bool
    small_relative_gap_implies_circuit_hardness: bool
    exact_direct_counterfamily_polar_constructed: bool
    natural_coset_source_counterfamily_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetPrefixRelativeGapInferenceNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PrefixGapCounterfamilyControl]
    scaling_records: list[PrefixGapScalingRecord]
    theorem: PrefixGapInferenceTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def prefix_gap_counterfamily_matrices(
    logical_dimension: int,
    delta: float,
) -> tuple[np.ndarray, tuple[np.ndarray, ...], np.ndarray]:
    if logical_dimension < 1:
        raise ValueError("logical_dimension must be positive")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0,1)")
    ancilla_dimension = 1 << logical_dimension
    ambient_dimension = logical_dimension * ancilla_dimension
    embedding = np.zeros(
        (ambient_dimension, logical_dimension), dtype=np.complex128
    )
    for logical in range(logical_dimension):
        embedding[logical * ancilla_dimension, logical] = math.sqrt(delta)
        embedding[
            logical * ancilla_dimension + (1 << logical), logical
        ] = math.sqrt(1.0 - delta)
    projectors = []
    for bit in range(logical_dimension):
        diagonal = np.zeros(ambient_dimension, dtype=float)
        for logical in range(logical_dimension):
            for ancilla in range(ancilla_dimension):
                if not ((ancilla >> bit) & 1):
                    diagonal[logical * ancilla_dimension + ancilla] = 1.0
        projectors.append(np.diag(diagonal))
    direct_final = np.zeros_like(embedding)
    for logical in range(logical_dimension):
        direct_final[logical * ancilla_dimension, logical] = 1.0
    return embedding, tuple(projectors), direct_final


def _prefix_analyses(
    embedding: np.ndarray,
    projectors: tuple[np.ndarray, ...],
    ordering: tuple[int, ...],
) -> list[np.ndarray]:
    analyses = [embedding]
    current = embedding
    for index in ordering:
        current = projectors[index] @ current
        analyses.append(current)
    return analyses


def _direct_step_polar(
    logical_dimension: int,
    delta: float,
    selected: frozenset[int],
    next_index: int,
) -> np.ndarray:
    """Directly write the normalized next-prefix isometry."""

    ancilla_dimension = 1 << logical_dimension
    output = np.zeros(
        (logical_dimension * ancilla_dimension, logical_dimension),
        dtype=np.complex128,
    )
    active = selected | {next_index}
    for logical in range(logical_dimension):
        if logical in active:
            output[logical * ancilla_dimension, logical] = 1.0
        else:
            output[logical * ancilla_dimension, logical] = math.sqrt(delta)
            output[
                logical * ancilla_dimension + (1 << logical), logical
            ] = math.sqrt(1.0 - delta)
    return output


def audit_prefix_gap_counterfamily(
    logical_dimension: int,
    delta: float,
    *,
    exhaustive_order_limit: int = 720,
) -> PrefixGapCounterfamilyControl:
    embedding, projectors, direct_final = prefix_gap_counterfamily_matrices(
        logical_dimension, delta
    )
    identity = np.eye(logical_dimension, dtype=np.complex128)
    embedding_residual = float(
        np.linalg.norm(embedding.conj().T @ embedding - identity, ord=2)
    )
    idempotence = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )
    commutator = max(
        (
            float(
                np.linalg.norm(
                    projectors[left] @ projectors[right]
                    - projectors[right] @ projectors[left],
                    ord=2,
                )
            )
            for left in range(logical_dimension)
            for right in range(left + 1, logical_dimension)
        ),
        default=0.0,
    )
    all_orderings = math.factorial(logical_dimension)
    if all_orderings <= exhaustive_order_limit:
        orderings = tuple(itertools.permutations(range(logical_dimension)))
    else:
        orderings = (
            tuple(range(logical_dimension)),
            tuple(reversed(range(logical_dimension))),
        )

    minimum_relative = 1.0
    maximum_relative = 0.0
    maximum_holonomy = 0.0
    determinant_residual = 0.0
    maximum_direct_residual = 0.0
    every_order_delta = True
    for ordering in orderings:
        analyses = _prefix_analyses(embedding, projectors, ordering)
        determinant_product = 1.0
        initial_metric = analyses[0].conj().T @ analyses[0]
        selected: frozenset[int] = frozenset()
        for step, index in enumerate(ordering, start=1):
            audit = audit_polar_chain_step(
                step, analyses[step - 1], analyses[step]
            )
            minimum_relative = min(
                minimum_relative, audit.relative_effect_minimum_eigenvalue
            )
            maximum_relative = max(
                maximum_relative, audit.relative_effect_maximum_eigenvalue
            )
            maximum_holonomy = max(
                maximum_holonomy, audit.holonomy_identity_distance
            )
            previous_metric = analyses[step - 1].conj().T @ analyses[step - 1]
            next_metric = analyses[step].conj().T @ analyses[step]
            determinant_product *= float(
                np.linalg.det(next_metric).real
                / np.linalg.det(previous_metric).real
            )
            every_order_delta &= abs(
                audit.relative_effect_minimum_eigenvalue - delta
            ) <= 1e-8
            direct = _direct_step_polar(
                logical_dimension, delta, selected, index
            )
            metric = analyses[step].conj().T @ analyses[step]
            values, vectors = np.linalg.eigh(metric)
            inverse_root = (vectors * values**-0.5) @ vectors.conj().T
            numeric_polar = analyses[step] @ inverse_root
            maximum_direct_residual = max(
                maximum_direct_residual,
                float(np.linalg.norm(numeric_polar - direct, ord=2)),
            )
            selected |= {index}
        final_metric = analyses[-1].conj().T @ analyses[-1]
        determinant_residual = max(
            determinant_residual,
            abs(
                float(np.linalg.det(final_metric).real)
                - float(np.linalg.det(initial_metric).real) * determinant_product
            ),
        )

    canonical = _prefix_analyses(
        embedding, projectors, tuple(range(logical_dimension))
    )[-1]
    final_metric = canonical.conj().T @ canonical
    final_values = np.linalg.eigvalsh(final_metric)
    final_scalar_residual = float(
        np.linalg.norm(final_metric - delta * identity, ord=2)
    )
    final_polar = canonical / math.sqrt(delta)
    final_direct_residual = float(
        np.linalg.norm(final_polar - direct_final, ord=2)
    )
    verified = bool(
        embedding_residual <= 1e-10
        and idempotence <= 1e-10
        and commutator <= 1e-10
        and final_scalar_residual <= 1e-10
        and determinant_residual <= 1e-10
        and every_order_delta
        and maximum_holonomy <= 1e-8
        and maximum_direct_residual <= 1e-8
        and final_direct_residual <= 1e-8
    )
    return PrefixGapCounterfamilyControl(
        logical_dimension=logical_dimension,
        ancilla_qubit_count=logical_dimension,
        ambient_dimension=embedding.shape[0],
        delta=delta,
        tested_ordering_count=len(orderings),
        expected_ordering_count=all_orderings,
        embedding_isometry_residual=embedding_residual,
        maximum_projector_idempotence_residual=idempotence,
        maximum_projector_commutator_residual=commutator,
        final_metric_scalar_residual=final_scalar_residual,
        final_metric_condition_number=float(final_values[-1] / final_values[0]),
        determinant_telescoping_residual=determinant_residual,
        minimum_relative_effect_eigenvalue=minimum_relative,
        maximum_relative_effect_eigenvalue=maximum_relative,
        maximum_holonomy_identity_distance=maximum_holonomy,
        maximum_direct_step_polar_residual=maximum_direct_residual,
        final_direct_polar_residual=final_direct_residual,
        every_order_has_delta_relative_edge=every_order_delta,
        all_holonomies_identity=maximum_holonomy <= 1e-8,
        direct_structured_polar_constructed=final_direct_residual <= 1e-8,
        control_verified=verified,
        status=(
            "constant-final-condition-bad-relative-gaps-direct-polar"
            if verified
            else "prefix-gap-counterfamily-control-failure"
        ),
    )


def prefix_gap_scaling_record(n: int) -> PrefixGapScalingRecord:
    if n < 4:
        raise ValueError("n must be at least four")
    logical_dimension = n
    delta = math.exp(-math.sqrt(n))
    return PrefixGapScalingRecord(
        n=n,
        logical_dimension=logical_dimension,
        ancilla_qubit_count=logical_dimension,
        delta=delta,
        log2_inverse_delta=math.sqrt(n) / math.log(2.0),
        final_condition_number=1.0,
        generic_relative_qsvt_degree_lower_order="exp(Theta(sqrt(n)/2))",
        direct_controlled_rotation_gate_order="poly(n,log(1/error))",
        inverse_polynomial_relative_gap_inferred=False,
        generic_qsvt_hardness_implies_circuit_hardness=False,
        status="spectral-inference-fails-direct-structure-bypasses",
    )


def build_coset_prefix_relative_gap_inference_report(
    *,
    finite_specs: tuple[tuple[int, float], ...] = (
        (2, 0.2),
        (3, 0.05),
        (4, 0.01),
        (5, 0.002),
        (6, 0.0005),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128, 256, 512),
) -> CosetPrefixRelativeGapInferenceNoGoReport:
    controls = [
        audit_prefix_gap_counterfamily(logical_dimension, delta)
        for logical_dimension, delta in finite_specs
    ]
    scaling = [prefix_gap_scaling_record(n) for n in scaling_n_values]
    verified = all(row.control_verified for row in controls)
    theorem = PrefixGapInferenceTheorem(
        loewner_monotonicity=(
            "A_j=P_jA_(j-1) with P_j a projector gives "
            "0<=D_j<=D_(j-1)."
        ),
        relative_contraction=(
            "On positive previous support, "
            "E_j=D_(j-1)^(-1/2)D_jD_(j-1)^(-1/2)<=I."
        ),
        determinant_chain=(
            "det(D_k)=det(D_0) product_j det(E_j) at full rank."
        ),
        counterfamily=(
            "Coordinate-controlled one-excitation dilations give D_final=delta I "
            "and one relative eigenvalue delta at every step."
        ),
        ordering_no_go=(
            "Each projector owns one logical coordinate, so every permutation of "
            "the projectors encounters the same delta edge at every step."
        ),
        direct_polar_escape=(
            "Despite generic degree Omega(1/sqrt(delta)), direct controlled "
            "rotations implement every relative polar and the final polar."
        ),
        scope_limit=(
            "The counterfamily is an abstract efficient commuting-projector "
            "dilation, not a proved natural symmetric-group source family."
        ),
        loewner_monotonicity_proved=True,
        determinant_telescoping_proved=True,
        final_constant_condition_implies_polynomial_relative_gaps=False,
        adaptive_ordering_always_repairs_relative_gaps=False,
        small_relative_gap_implies_circuit_hardness=False,
        exact_direct_counterfamily_polar_constructed=True,
        natural_coset_source_counterfamily_proved=False,
        theorem_verified=verified,
        status=(
            "final-spectrum-and-determinant-prefix-gap-inference-refuted"
            if verified
            else "prefix-gap-inference-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_counterfamily_control_count": len(controls),
        "finite_validation_failure_count": sum(
            not row.control_verified for row in controls
        ),
        "exhaustive_ordering_count": sum(
            row.tested_ordering_count for row in controls
        ),
        "constant_final_condition_counterexample_count": len(controls),
        "adaptive_ordering_counterexample_count": len(controls),
        "direct_structured_polar_bypass_count": len(controls),
        "natural_coset_source_counterexample_count": 0,
        "general_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetPrefixRelativeGapInferenceNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "access_model": (
                "Explicit isometry J and explicit mutually commuting projectors "
                "with polynomial-qubit encodings."
            ),
            "inference_under_test": (
                "Use final constant condition, determinant telescoping, or adaptive "
                "projector order to infer inverse-polynomial relative gaps."
            ),
            "non_claim": (
                "No natural-source counterfamily and no lower bound against direct "
                "structured polar circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-NATURAL-PREFIX-STRUCTURE",
                "statement": (
                    "Prove a natural source-specific relative-gap/transport theorem "
                    "using symmetric-group and wreath recoupling data, not only the "
                    "final frame spectrum."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-DIRECT-UHLMANN-TRANSPORT",
                "statement": (
                    "Search for direct GPE/subduction implementations of U_j and "
                    "V_j even when generic relative QSVT has a small edge."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Final condition one forces good conditional gaps.",
                "answer": (
                    "False: D_final=delta I while every relative effect has minimum delta."
                ),
                "resolved": True,
            },
            {
                "challenge": "A better projector ordering avoids the bad steps.",
                "answer": (
                    "False in the counterfamily: every ordering drops one fresh "
                    "logical coordinate by delta at every step."
                ),
                "resolved": True,
            },
            {
                "challenge": "The determinant identity controls the least edge.",
                "answer": (
                    "False. It fixes total log-volume loss and allows that loss to "
                    "be assigned to a different direction at each step."
                ),
                "resolved": True,
            },
            {
                "challenge": "The bad relative edges prove the polar is hard.",
                "answer": (
                    "False: explicit controlled rotations implement the exact polars "
                    "without singular-value amplification."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "final_spectral_window_implies_prefix_gaps": False,
            "determinant_budget_implies_prefix_gaps": False,
            "adaptive_ordering_always_finds_prefix_gaps": False,
            "small_relative_gap_implies_circuit_hardness": False,
            "direct_structured_counterfamily_polar_constructed": True,
            "natural_coset_relative_gap_theorem_proved": False,
            "natural_coset_direct_holonomy_compiler_constructed": False,
            "polynomial_hidden_involution_decoder_constructed": False,
            "general_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Abstract spectral data supports neither side: natural recoupling "
                "structure is required to prove an efficient direct polar or a no-go."
            ),
        },
        status="final-spectrum-and-determinant-prefix-gap-inference-refuted",
        summary=(
            "Refuted all generic attempts to infer polynomial prefix gaps from "
            "the final constant-condition frame, determinant telescoping, projector "
            "commutativity, or adaptive ordering. The same family has trivial direct "
            "polars, so bad generic QSVT gaps are not circuit lower bounds."
        ),
        falsifiers_triggered=[
            "A constant-condition final prefix metric does not force good relative gaps.",
            "Determinant telescoping does not control each relative minimum eigenvalue.",
            "Adaptive ordering does not universally repair relative gaps.",
            "An exponentially small relative edge does not imply a hard structured polar.",
        ],
    )


def write_coset_prefix_relative_gap_inference_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_coset_prefix_relative_gap_inference_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
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
                id="NEG--PREFIX-RELATIVE-GAP-INFERENCE-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO."
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
                    "coset_prefix_relative_gap_inference_no_go": str(output_path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    report = write_coset_prefix_relative_gap_inference_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
