"""Finite scaling audit for the second-stage hierarchical Racah Hamiltonian.

For source W_n=(n-2,2), final target xi_n=(n-3,2,1), and every intermediate
alpha in W_n tensor W_n, the second-stage Hamiltonian is the bounded-support
orbit sum on V_alpha tensor W_n.  This module extracts its exact finite
multiplicity blocks using diagonal Young--Jucys--Murphy labels and measures
whether all residual Kronecker copies split with a visible normalized gap.

Finite splitting is only a theorem target.  A uniform Racah circuit requires
an inverse-polynomial all-n lower bound for every source-relevant channel, not
an extrapolation from dense matrices.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import numpy as np

from coset_jucys_murphy_label_transform import (
    diagonal_jucys_murphy_operators,
    encoded_jucys_murphy_operator,
)
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    transposition_three_cycle_intersection_operator,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_HIERARCHICAL_GAP_SCALING_PATH = Path(
    "research/representation/coset_hierarchical_gap_scaling.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIERARCHICAL-GAP-SCALING"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SecondStageGapRecord:
    intermediate_partition: tuple[int, ...]
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    intermediate_irrep_dimension: int
    tensor_dimension: int
    tableau_block_count: int
    eigenvalues: tuple[float, ...]
    integer_characteristic_polynomial: tuple[int, ...]
    integer_polynomial_reconstruction_residual: float
    exact_integer_polynomial_candidate: bool
    raw_gap: float
    lcu_normalized_gap: float
    tableau_spectrum_consistency_residual: float
    multiplicity_fully_split: bool
    finite_dense_verification_only: bool


@dataclass(frozen=True)
class HierarchicalGapScalingRecord:
    n: int
    source_partition: tuple[int, ...]
    final_partition: tuple[int, ...]
    source_irrep_dimension: int
    final_total_multiplicity: int
    maximum_second_stage_multiplicity: int
    lcu_term_count: int
    lcu_term_count_formula: int
    term_count_formula_verified: bool
    nontrivial_second_stage_channel_count: int
    channels: list[SecondStageGapRecord]
    minimum_raw_gap: float
    minimum_lcu_normalized_gap: float
    all_second_stage_blocks_split: bool
    finite_dense_verification_only: bool
    status: str


@dataclass(frozen=True)
class HierarchicalGapScalingReport:
    created_at: str
    family_contract: dict[str, object]
    records: list[HierarchicalGapScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def audit_hierarchical_gap_scaling(n: int) -> HierarchicalGapScalingRecord:
    if n < 6:
        raise ValueError("the audited stable family starts at n=6")
    source = (n - 2, 2)
    final = (n - 3, 2, 1)
    base = 2 * n + 1
    target_by_label = _encoded_label_targets(n, base)
    channels: list[SecondStageGapRecord] = []
    total_multiplicity = 0
    maximum_second = 0
    reference_term_count: int | None = None

    for intermediate in integer_partitions(n):
        first_multiplicity = kronecker_coefficient(source, source, intermediate)
        second_multiplicity = kronecker_coefficient(intermediate, source, final)
        if not first_multiplicity or not second_multiplicity:
            continue
        total_multiplicity += first_multiplicity * second_multiplicity
        maximum_second = max(maximum_second, second_multiplicity)
        if second_multiplicity <= 1:
            continue

        hamiltonian, term_count = transposition_three_cycle_intersection_operator(
            intermediate, source, support_intersection=2
        )
        if reference_term_count is None:
            reference_term_count = term_count
        elif term_count != reference_term_count:
            raise ArithmeticError("orbit term count depends on the intermediate partition")
        encoded_yjm = encoded_jucys_murphy_operator(
            diagonal_jucys_murphy_operators(intermediate, source), base, n
        )
        label_values, label_vectors = np.linalg.eigh(encoded_yjm)
        label_indices: dict[int, list[int]] = {}
        for index, value in enumerate(label_values):
            label_indices.setdefault(round(float(value)), []).append(index)
        spectra: list[np.ndarray] = []
        for label, indices in label_indices.items():
            if target_by_label[label] != final:
                continue
            if len(indices) != second_multiplicity:
                raise ArithmeticError("YJM block dimension disagrees with Kronecker multiplicity")
            basis = label_vectors[:, indices]
            block = basis.T @ hamiltonian @ basis
            spectra.append(np.linalg.eigvalsh((block + block.T) / 2))
        if not spectra:
            raise ArithmeticError(f"no target-tableau blocks found for {intermediate}")
        reference = spectra[0]
        consistency = max(
            float(np.linalg.norm(spectrum - reference)) for spectrum in spectra
        )
        polynomial = np.poly(reference)
        rounded_polynomial = np.rint(polynomial)
        polynomial_residual = float(np.max(np.abs(polynomial - rounded_polynomial)))
        raw_gap = float(min(np.diff(reference)))
        channels.append(
            SecondStageGapRecord(
                intermediate_partition=intermediate,
                first_stage_multiplicity=first_multiplicity,
                second_stage_multiplicity=second_multiplicity,
                intermediate_irrep_dimension=hook_length_dimension(intermediate),
                tensor_dimension=(
                    hook_length_dimension(intermediate)
                    * hook_length_dimension(source)
                ),
                tableau_block_count=len(spectra),
                eigenvalues=tuple(float(value) for value in reference),
                integer_characteristic_polynomial=tuple(
                    int(value) for value in rounded_polynomial
                ),
                integer_polynomial_reconstruction_residual=polynomial_residual,
                exact_integer_polynomial_candidate=polynomial_residual < 1e-6,
                raw_gap=raw_gap,
                lcu_normalized_gap=raw_gap / term_count,
                tableau_spectrum_consistency_residual=consistency,
                multiplicity_fully_split=raw_gap > 1e-8,
                finite_dense_verification_only=True,
            )
        )

    term_count_formula = n * (n - 1) * (n - 2)
    lcu_term_count = reference_term_count or term_count_formula
    minimum_raw_gap = min((channel.raw_gap for channel in channels), default=0.0)
    minimum_normalized_gap = min(
        (channel.lcu_normalized_gap for channel in channels), default=0.0
    )
    all_split = bool(channels) and all(
        channel.multiplicity_fully_split for channel in channels
    )
    return HierarchicalGapScalingRecord(
        n=n,
        source_partition=source,
        final_partition=final,
        source_irrep_dimension=hook_length_dimension(source),
        final_total_multiplicity=total_multiplicity,
        maximum_second_stage_multiplicity=maximum_second,
        lcu_term_count=lcu_term_count,
        lcu_term_count_formula=term_count_formula,
        term_count_formula_verified=lcu_term_count == term_count_formula,
        nontrivial_second_stage_channel_count=len(channels),
        channels=channels,
        minimum_raw_gap=minimum_raw_gap,
        minimum_lcu_normalized_gap=minimum_normalized_gap,
        all_second_stage_blocks_split=all_split,
        finite_dense_verification_only=True,
        status=(
            "all-second-stage-blocks-finite-split"
            if all_split
            else "second-stage-gap-counterexample-found"
        ),
    )


def build_hierarchical_gap_scaling_report(
    n_values: Sequence[int] = (6, 7, 8),
) -> HierarchicalGapScalingReport:
    records = [audit_hierarchical_gap_scaling(n) for n in n_values]
    all_split = all(record.all_second_stage_blocks_split for record in records)
    log_n = np.log(np.asarray([record.n for record in records], dtype=float))
    log_gap = np.log(
        np.asarray([record.minimum_lcu_normalized_gap for record in records], dtype=float)
    )
    slope = float(np.polyfit(log_n, log_gap, 1)[0]) if len(records) > 1 else 0.0
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "minimum_n": min(n_values),
        "maximum_n": max(n_values),
        "finite_all_blocks_split_count": sum(
            record.all_second_stage_blocks_split for record in records
        ),
        "audited_nontrivial_channel_count": sum(
            record.nontrivial_second_stage_channel_count for record in records
        ),
        "maximum_second_stage_multiplicity": max(
            record.maximum_second_stage_multiplicity for record in records
        ),
        "maximum_final_total_multiplicity": max(
            record.final_total_multiplicity for record in records
        ),
        "minimum_observed_raw_gap": min(record.minimum_raw_gap for record in records),
        "minimum_observed_normalized_gap": min(
            record.minimum_lcu_normalized_gap for record in records
        ),
        "maximum_tableau_spectrum_consistency_residual": max(
            channel.tableau_spectrum_consistency_residual
            for record in records
            for channel in record.channels
        ),
        "integer_characteristic_polynomial_candidate_count": sum(
            channel.exact_integer_polynomial_candidate
            for record in records
            for channel in record.channels
        ),
        "maximum_integer_polynomial_reconstruction_residual": max(
            channel.integer_polynomial_reconstruction_residual
            for record in records
            for channel in record.channels
        ),
        "empirical_log_log_normalized_gap_slope": slope,
        "all_n_second_stage_gap_theorem_count": 0,
        "uniform_polynomial_racah_circuit_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return HierarchicalGapScalingReport(
        created_at=utc_now(),
        family_contract={
            "source": "W_n=(n-2,2)",
            "final_target": "xi_n=(n-3,2,1)",
            "intermediates": "every alpha with g(W_n,W_n,alpha) g(alpha,W_n,xi_n)>0",
            "second_stage_hamiltonian": (
                "H_(alpha,W)=sum rho_alpha(tau) tensor rho_W(c) for tau contained in oriented 3-cycle c"
            ),
            "lcu_term_count": "n(n-1)(n-2)",
            "finite_extraction": "dense diagonal YJM target-tableau blocks",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_audited_second_stage_blocks_split": all_split,
            "multiplicity_four_audited": metrics["maximum_second_stage_multiplicity"] >= 4,
            "integer_characteristic_polynomials_reconstructed": (
                metrics["integer_characteristic_polynomial_candidate_count"]
                == metrics["audited_nontrivial_channel_count"]
            ),
            "all_n_second_stage_gap_proved": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Finite splitting through n=8 does not prove an inverse-polynomial all-n gap, cover every final "
                "family, compile phase estimation, or decode the hidden involution."
            ),
        },
        status=(
            "hierarchical-gap-finite-scaling-survives-all-n-proof-open"
            if all_split
            else "hierarchical-gap-family-falsified"
        ),
        summary=(
            f"Audited {metrics['audited_nontrivial_channel_count']} second-stage multiplicity blocks over "
            f"n={min(n_values)}..{max(n_values)}; all split finitely, with minimum normalized gap "
            f"{metrics['minimum_observed_normalized_gap']:.6g}, but no all-n theorem or circuit follows."
        ),
        falsifiers_triggered=[
            "Finite nonzero gaps cannot be extrapolated into an inverse-polynomial all-n theorem.",
            "The empirical gap slope is descriptive and is not a complexity proof.",
            "One stable final-target family does not cover all source-relevant sectors.",
            "A gapped multiplicity label does not by itself implement Racah amplitudes or hidden-involution decoding.",
        ],
    )


def write_hierarchical_gap_scaling_report(
    output_path: Path = COSET_HIERARCHICAL_GAP_SCALING_PATH,
    n_values: Sequence[int] = (6, 7, 8),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_hierarchical_gap_scaling_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FINITE-HIERARCHICAL-GAP-SCALING-AS-THEOREM",
                source=str(output_path),
                claim=(
                    "Nonzero hierarchical Racah gaps through n=8 establish an efficient all-n multiplicity transform."
                ),
                reason_invalid=(
                    "The evidence is finite dense diagonalization on one final-target family and contains no "
                    "inverse-polynomial lower bound or coherent circuit."
                ),
                lesson=(
                    "Use the observed spectra to conjecture exact stable formulas, then prove them with character-orbit "
                    "or partition-algebra methods before algorithmic promotion."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_hierarchical_gap_scaling": str(output_path)},
            )
        )
    return payload
