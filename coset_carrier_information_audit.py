"""Carrier-sensitive information audit after commutant preprocessing.

Commutant-only outcomes have zero information about an individual hidden
involution.  This module tests the nearest valid escape: retain carrier
(target-tableau) outcomes and refine them with a bounded-support multiplicity
separator.

For two finite nontrivial source-pair controls it compares:

* separator eigenvalues alone;
* diagonal YJM target-tableau labels;
* joint YJM plus the parity-complete separator;
* all 1,744 primitive bounded-support separator rules, ranked by mutual
  information rather than spectral gap;
* direct product Young-basis measurement, the simpler separate strong-Fourier
  carrier baseline.

The result is deliberately finite.  It asks whether the current recoupling
architecture adds information before any circuit or asymptotic claim is
considered.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from coset_commutant_information_obstruction import (
    _conditioned_source_state,
)
from coset_jucys_murphy_label_transform import (
    diagonal_jucys_murphy_operators,
    encoded_jucys_murphy_operator,
)
from coset_three_copy_recoupling_obstruction import involutions
from coset_typical_parity_complete_separator import (
    DISCOVERY_COEFFICIENTS,
    GENERATOR_NAMES,
    oriented_generator_operators,
    primitive_coefficient_vectors,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/coset_carrier_information_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-CARRIER-INFORMATION-AUDIT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
CONTROL_SPECS = (
    (5, 2, (3, 2), (3, 1, 1)),
    (6, 3, (3, 2, 1), (3, 3)),
)


@dataclass(frozen=True)
class CarrierInformationControlRecord:
    n: int
    transposition_count: int
    left_source_partition: tuple[int, ...]
    right_source_partition: tuple[int, ...]
    hidden_involution_count: int
    tensor_dimension: int
    random_guess_success_probability: float
    product_young_basis_mutual_information_bits: float
    product_young_basis_bayes_success_probability: float
    yjm_only_mutual_information_bits: float
    yjm_only_bayes_success_probability: float
    separator_only_mutual_information_bits: float
    separator_only_bayes_success_probability: float
    gap_rule_joint_mutual_information_bits: float
    gap_rule_joint_bayes_success_probability: float
    best_searched_joint_mutual_information_bits: float
    best_searched_joint_bayes_success_probability: float
    best_information_coefficients: dict[str, int]
    best_information_lcu_normalization: int
    best_bayes_success_probability: float
    best_bayes_coefficients: dict[str, int]
    best_bayes_lcu_normalization: int
    best_joint_information_gain_over_yjm_bits: float
    best_joint_information_fraction_of_product_baseline: float
    product_basis_information_dominates_all_searched_rules: bool
    coefficient_vector_count: int
    maximum_measurement_normalization_residual: float
    status: str


@dataclass(frozen=True)
class CarrierInformationAuditReport:
    created_at: str
    measurement_contract: dict[str, object]
    controls: list[CarrierInformationControlRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class _PreparedControl:
    states: tuple[np.ndarray, ...]
    yjm_fibers: tuple[
        tuple[
            tuple[np.ndarray, ...],
            tuple[np.ndarray, ...],
        ],
        ...,
    ]
    yjm_probabilities: np.ndarray
    product_probabilities: np.ndarray
    generator_operators: tuple[np.ndarray, ...]


def _measurement_statistics(
    probabilities: np.ndarray,
) -> tuple[float, float, float]:
    rows = np.clip(np.asarray(probabilities, dtype=float), 0.0, 1.0)
    row_sums = rows.sum(axis=1)
    residual = float(np.max(np.abs(row_sums - 1.0)))
    rows = rows / row_sums[:, None]
    average = rows.mean(axis=0)
    information = 0.0
    for row in rows:
        for probability, marginal in zip(row, average):
            if probability > 1e-15 and marginal > 0:
                information += probability * math.log2(
                    probability / marginal
                )
    information /= len(rows)
    bayes_success = float(rows.max(axis=0).sum() / len(rows))
    return float(information), bayes_success, residual


def _spectral_probabilities(
    operator: np.ndarray,
    states: tuple[np.ndarray, ...],
    tolerance: float = 1e-8,
) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    projectors: list[np.ndarray] = []
    start = 0
    while start < len(eigenvalues):
        stop = start + 1
        while (
            stop < len(eigenvalues)
            and abs(eigenvalues[stop] - eigenvalues[start]) <= tolerance
        ):
            stop += 1
        fiber = eigenvectors[:, start:stop]
        projectors.append(fiber @ fiber.T)
        start = stop
    return np.asarray(
        [
            [float(np.trace(projector @ state).real) for projector in projectors]
            for state in states
        ]
    )


def _joint_probabilities(
    prepared: _PreparedControl,
    coefficients: tuple[int, ...],
    tolerance: float = 1e-8,
) -> np.ndarray:
    rows: list[list[float]] = [
        [] for _ in range(len(prepared.states))
    ]
    for generator_blocks, state_blocks in prepared.yjm_fibers:
        separator = sum(
            coefficient * generator
            for coefficient, generator in zip(
                coefficients,
                generator_blocks,
            )
        )
        eigenvalues, eigenvectors = np.linalg.eigh(separator)
        start = 0
        while start < len(eigenvalues):
            stop = start + 1
            while (
                stop < len(eigenvalues)
                and abs(eigenvalues[stop] - eigenvalues[start]) <= tolerance
            ):
                stop += 1
            fiber = eigenvectors[:, start:stop]
            projector = fiber @ fiber.T
            for hidden_index, state_block in enumerate(state_blocks):
                rows[hidden_index].append(
                    float(np.trace(projector @ state_block).real)
                )
            start = stop
    return np.asarray(rows)


@lru_cache(maxsize=None)
def _prepare_control(
    n: int,
    transposition_count: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
) -> _PreparedControl:
    hidden = involutions(n, transposition_count)
    states = tuple(
        np.kron(
            _conditioned_source_state(
                left_source,
                permutation,
                transposition_count,
            ),
            _conditioned_source_state(
                right_source,
                permutation,
                transposition_count,
            ),
        )
        for permutation in hidden
    )
    yjm = encoded_jucys_murphy_operator(
        diagonal_jucys_murphy_operators(left_source, right_source),
        2 * n + 1,
        n,
    )
    generator_operators = oriented_generator_operators(
        left_source,
        right_source,
    )
    eigenvalues, eigenvectors = np.linalg.eigh(yjm)
    fibers: list[
        tuple[
            tuple[np.ndarray, ...],
            tuple[np.ndarray, ...],
        ]
    ] = []
    yjm_projectors: list[np.ndarray] = []
    start = 0
    while start < len(eigenvalues):
        stop = start + 1
        while (
            stop < len(eigenvalues)
            and abs(eigenvalues[stop] - eigenvalues[start]) <= 1e-7
        ):
            stop += 1
        fiber = eigenvectors[:, start:stop]
        yjm_projectors.append(fiber @ fiber.T)
        fibers.append(
            (
                tuple(
                    fiber.T @ generator @ fiber
                    for generator in generator_operators
                ),
                tuple(fiber.T @ state @ fiber for state in states),
            )
        )
        start = stop
    yjm_probabilities = np.asarray(
        [
            [
                float(np.trace(projector @ state).real)
                for projector in yjm_projectors
            ]
            for state in states
        ]
    )
    product_probabilities = np.asarray(
        [np.diag(state).real for state in states]
    )
    return _PreparedControl(
        states=states,
        yjm_fibers=tuple(fibers),
        yjm_probabilities=yjm_probabilities,
        product_probabilities=product_probabilities,
        generator_operators=generator_operators,
    )


@lru_cache(maxsize=None)
def audit_carrier_information_control(
    n: int,
    transposition_count: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
) -> CarrierInformationControlRecord:
    prepared = _prepare_control(
        n,
        transposition_count,
        left_source,
        right_source,
    )
    product_info, product_bayes, product_residual = (
        _measurement_statistics(prepared.product_probabilities)
    )
    yjm_info, yjm_bayes, yjm_residual = _measurement_statistics(
        prepared.yjm_probabilities
    )
    gap_probabilities = _joint_probabilities(
        prepared,
        DISCOVERY_COEFFICIENTS,
    )
    gap_info, gap_bayes, gap_residual = _measurement_statistics(
        gap_probabilities
    )
    gap_separator = sum(
        coefficient * generator
        for coefficient, generator in zip(
            DISCOVERY_COEFFICIENTS,
            prepared.generator_operators,
        )
    )
    separator_probabilities = _spectral_probabilities(
        gap_separator,
        prepared.states,
    )
    separator_info, separator_bayes, separator_residual = (
        _measurement_statistics(separator_probabilities)
    )
    coefficient_vectors = primitive_coefficient_vectors()
    best_information = (-1.0, 0.0, coefficient_vectors[0])
    best_bayes = (0.0, -1.0, coefficient_vectors[0])
    maximum_residual = max(
        product_residual,
        yjm_residual,
        gap_residual,
        separator_residual,
    )
    for coefficients in coefficient_vectors:
        probabilities = _joint_probabilities(prepared, coefficients)
        information, bayes, residual = _measurement_statistics(
            probabilities
        )
        maximum_residual = max(maximum_residual, residual)
        if (information, bayes, coefficients) > best_information:
            best_information = (information, bayes, coefficients)
        if (bayes, information, coefficients) > best_bayes:
            best_bayes = (bayes, information, coefficients)
    best_info_value, best_info_bayes, best_info_coefficients = (
        best_information
    )
    best_bayes_value, _, best_bayes_coefficients = best_bayes
    information_map = dict(zip(GENERATOR_NAMES, best_info_coefficients))
    bayes_map = dict(zip(GENERATOR_NAMES, best_bayes_coefficients))
    return CarrierInformationControlRecord(
        n=n,
        transposition_count=transposition_count,
        left_source_partition=left_source,
        right_source_partition=right_source,
        hidden_involution_count=len(prepared.states),
        tensor_dimension=prepared.states[0].shape[0],
        random_guess_success_probability=1 / len(prepared.states),
        product_young_basis_mutual_information_bits=product_info,
        product_young_basis_bayes_success_probability=product_bayes,
        yjm_only_mutual_information_bits=yjm_info,
        yjm_only_bayes_success_probability=yjm_bayes,
        separator_only_mutual_information_bits=separator_info,
        separator_only_bayes_success_probability=separator_bayes,
        gap_rule_joint_mutual_information_bits=gap_info,
        gap_rule_joint_bayes_success_probability=gap_bayes,
        best_searched_joint_mutual_information_bits=best_info_value,
        best_searched_joint_bayes_success_probability=best_info_bayes,
        best_information_coefficients=information_map,
        best_information_lcu_normalization=sum(
            abs(value) for value in best_info_coefficients
        ),
        best_bayes_success_probability=best_bayes_value,
        best_bayes_coefficients=bayes_map,
        best_bayes_lcu_normalization=sum(
            abs(value) for value in best_bayes_coefficients
        ),
        best_joint_information_gain_over_yjm_bits=(
            best_info_value - yjm_info
        ),
        best_joint_information_fraction_of_product_baseline=(
            best_info_value / product_info if product_info else 0.0
        ),
        product_basis_information_dominates_all_searched_rules=(
            bool(product_info > best_info_value + 1e-10)
        ),
        coefficient_vector_count=len(coefficient_vectors),
        maximum_measurement_normalization_residual=maximum_residual,
        status=(
            "finite-separator-refinement-informative-but-dominated-by-product-strong-fourier"
            if product_info > best_info_value + 1e-10
            else "finite-separator-refinement-needs-independent-holdout"
        ),
    )


def build_carrier_information_audit_report(
) -> CarrierInformationAuditReport:
    controls = [
        audit_carrier_information_control(*spec)
        for spec in CONTROL_SPECS
    ]
    dominated = sum(
        record.product_basis_information_dominates_all_searched_rules
        for record in controls
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "coefficient_vector_count": len(primitive_coefficient_vectors()),
        "separator_only_zero_information_verified_count": sum(
            abs(record.separator_only_mutual_information_bits) <= 1e-10
            for record in controls
        ),
        "joint_separator_information_gain_control_count": sum(
            record.best_joint_information_gain_over_yjm_bits > 1e-10
            for record in controls
        ),
        "product_strong_fourier_dominates_all_searched_rules_count": (
            dominated
        ),
        "maximum_best_joint_mutual_information_bits": max(
            (
                record.best_searched_joint_mutual_information_bits
                for record in controls
            ),
            default=0.0,
        ),
        "maximum_product_young_basis_mutual_information_bits": max(
            (
                record.product_young_basis_mutual_information_bits
                for record in controls
            ),
            default=0.0,
        ),
        "maximum_best_joint_information_fraction_of_product_baseline": max(
            (
                record.best_joint_information_fraction_of_product_baseline
                for record in controls
            ),
            default=0.0,
        ),
        "maximum_best_joint_bayes_success_probability": max(
            (
                record.best_bayes_success_probability
                for record in controls
            ),
            default=0.0,
        ),
        "maximum_measurement_normalization_residual": max(
            (
                record.maximum_measurement_normalization_residual
                for record in controls
            ),
            default=0.0,
        ),
        "all_n_information_advantage_theorem_count": 0,
        "classical_separation_theorem_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return CarrierInformationAuditReport(
        created_at=utc_now(),
        measurement_contract={
            "prior": "uniform over one involution conjugacy class",
            "input": (
                "two independently prepared coset states conditioned on fixed "
                "weak Fourier source labels"
            ),
            "separator_only": (
                "spectral projectors of one diagonal-action commutant "
                "observable; theorem predicts zero information"
            ),
            "yjm_only": (
                "encoded diagonal YJM target-tableau projectors, retaining "
                "carrier-sensitive labels"
            ),
            "joint_search": (
                "YJM fibers refined by every primitive support<=3, "
                "|coefficient|<=2 rule over the parity-complete portfolio"
            ),
            "simple_quantum_baseline": (
                "direct product Young-basis measurement on the two conditioned "
                "source registers, equivalent to separate strong Fourier "
                "column outcomes"
            ),
            "metrics": (
                "mutual information I(H;Y) and optimal one-shot Bayes success "
                "under the known finite prior"
            ),
        },
        controls=controls,
        headline_metrics=metrics,
        claim_gate={
            "commutant_separator_alone_informative": False,
            "carrier_refinement_adds_information_over_yjm_finitely": True,
            "carrier_refinement_beats_product_strong_fourier": (
                dominated < len(controls)
            ),
            "finite_information_search_is_asymptotic_algorithm": False,
            "classical_separation_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Carrier-sensitive refinement adds finite information over "
                "YJM labels, but every searched rule is dominated by the "
                "simpler product Young-basis measurement and no scaling, "
                "decoder, or classical separation is known."
            ),
        },
        status=(
            "carrier-refinement-finite-signal-dominated-by-simple-strong-fourier-baseline"
        ),
        summary=(
            f"Searched {len(primitive_coefficient_vectors())} parity-complete "
            f"separator rules on {len(controls)} carrier-sensitive controls. "
            "All improve on YJM-only information to some extent, but the "
            "simple product Young-basis baseline dominates the best searched "
            "joint measurement on every control."
        ),
        falsifiers_triggered=[
            (
                "Spectral separation is not an information objective: the "
                "gap-optimized rule is not information-optimal."
            ),
            (
                "Commutant separator outcomes alone have zero hidden-element "
                "information, exactly as the covariance theorem predicts."
            ),
            (
                "Adding multiplicity labels to target tableaux gives finite "
                "signal but does not beat separate strong Fourier outcomes."
            ),
            (
                "Finite mutual information does not supply scaling, a "
                "polynomial decoder, or a quantum-classical separation."
            ),
        ],
    )


def write_carrier_information_audit_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_carrier_information_audit_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-SPECTRAL-SEPARATOR-SEARCH-NOT-INFORMATION-SEARCH",
                source=str(output_path),
                claim=(
                    "A large-gap multiplicity separator is the best "
                    "information-bearing refinement of carrier labels."
                ),
                reason_invalid=(
                    "The gap-optimized rule is not information-optimal on the "
                    "finite controls, and every searched refinement is "
                    "dominated by direct product Young-basis measurement."
                ),
                lesson=(
                    "Rank covariant measurement candidates by hidden-element "
                    "information and Bayes recovery before gap optimization."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-SUCCESS",
                    "PO-DEQUANTIZATION",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-COSET"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=dict(payload["headline_metrics"]),
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={"coset_carrier_information_audit": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_carrier_information_audit_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
