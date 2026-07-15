"""Exact Babai-cell geometry audit for marker-aware subset-sum witnesses.

For each independent uniform source instance, meet in the middle enumerates all
binary witnesses (up to an explicit cap).  A witness determines an error vector
of ``+/-1`` binary coordinates and zero constraint coordinates between the
target row and its marker-zero kernel lattice point.  Exact Gram-Schmidt then
tests whether this error lies in the Babai zero cell of the LLL-reduced kernel.

This directly explains nearest-plane success or failure.  It also checks the
strong global BDD condition ``min_i ||b_i*||^2 > 4m``.  Finite cell membership
is not a source-coverage theorem, and failure is not a lower bound against
enumeration or stronger affine-CVP algorithms.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from sympy import Matrix

from dcp_subset_sum_affine_cvp_baseline import (
    babai_zero_cell_margin,
    carry_sliced_affine_babai,
    exact_gram_schmidt_rows,
    standard_affine_babai,
)
from dcp_subset_sum_affine_cvp_scaling import exact_mitm_witnesses
from dcp_subset_sum_carry_slice_lattice import (
    carry_sliced_embedding,
    constrained_low_bits,
)
from dcp_subset_sum_lattice_search import modular_subset_sum_embedding
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_AFFINE_BDD_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_affine_bdd_geometry.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-AFFINE-BDD-GEOMETRY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class AffineBDDGeometryTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    exact_witness_count: int
    enumerated_witness_count: int
    witness_enumeration_truncated: bool
    target_legal: bool
    standard_babai_solved: bool
    standard_witness_cell_count: int
    standard_maximum_cell_margin: float | None
    standard_minimum_gram_schmidt_squared: float
    standard_minimum_gram_schmidt_to_four_m_ratio: float
    standard_global_bdd_condition_satisfied: bool
    standard_cell_prediction_consistent: bool
    constrained_low_bits: int
    carry_sliced_babai_solved: bool
    carry_sliced_witness_cell_count: int
    carry_sliced_maximum_cell_margin: float | None
    carry_sliced_minimum_gram_schmidt_squared: float
    carry_sliced_minimum_gram_schmidt_to_four_m_ratio: float
    carry_sliced_global_bdd_condition_satisfied: bool
    carry_sliced_cell_prediction_consistent: bool


@dataclass(frozen=True)
class AffineBDDGeometryScalingRow:
    n_bits: int
    register_offset: int
    trial_count: int
    legal_trial_count: int
    complete_witness_enumeration_count: int
    standard_positive_cell_trial_count: int
    carry_sliced_positive_cell_trial_count: int
    standard_global_bdd_trial_count: int
    carry_sliced_global_bdd_trial_count: int
    mean_standard_maximum_margin: float | None
    mean_carry_sliced_maximum_margin: float | None
    standard_prediction_inconsistency_count: int
    carry_sliced_prediction_inconsistency_count: int
    empirical_row_is_source_coverage_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumAffineBDDGeometryReport:
    created_at: str
    geometry_contract: dict[str, str]
    rows: list[AffineBDDGeometryScalingRow]
    trials: list[AffineBDDGeometryTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _minimum_gram_schmidt_squared(basis: Matrix) -> float:
    orthogonal = exact_gram_schmidt_rows(basis)
    return min(float(sum(value * value for value in row)) for row in orthogonal)


def _standard_reduced_kernel(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    embedding_scale: int,
    lll_delta: float,
) -> Matrix:
    full = modular_subset_sum_embedding(labels, target, 1 << n_bits, embedding_scale)
    rows = full.tolist()
    return Matrix([row[:-1] for row in rows[:-1]]).lll(delta=lll_delta)


def _carry_reduced_kernel(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    low_bits: int,
    carry: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
) -> Matrix:
    full = carry_sliced_embedding(
        labels,
        target,
        n_bits,
        low_bits,
        carry,
        embedding_scale,
        low_constraint_scale,
    )
    rows = full.tolist()
    return Matrix([row[:-1] for row in rows[:-1]]).lll(delta=lll_delta)


def run_affine_bdd_geometry_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    witness_cap: int,
    seed: int,
) -> AffineBDDGeometryTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    witness_count, witnesses, truncated = exact_mitm_witnesses(
        labels, target, modulus, witness_cap
    )

    _, standard_diagnostics = standard_affine_babai(
        n_bits, labels, target, embedding_scale, lll_delta
    )
    standard_solved = standard_diagnostics.within_witness_radius
    standard_basis = _standard_reduced_kernel(
        n_bits, labels, target, embedding_scale, lll_delta
    )
    standard_margins: list[float] = []
    standard_cells = 0
    for witness in witnesses:
        error = [1 - 2 * bit for bit in witness] + [0]
        returned_zero, margin, _ = babai_zero_cell_margin(standard_basis, error)
        standard_cells += returned_zero
        standard_margins.append(margin)
    standard_gs = _minimum_gram_schmidt_squared(standard_basis)

    low_bits = constrained_low_bits(n_bits, log_multiplier)
    low_modulus = 1 << low_bits
    sliced_witness, _, _, sliced_diagnostics = carry_sliced_affine_babai(
        n_bits,
        labels,
        target,
        low_bits,
        embedding_scale,
        low_constraint_scale,
        lll_delta,
    )
    sliced_solved = sliced_witness is not None
    sliced_basis_cache: dict[int, Matrix] = {}
    sliced_gs_values: list[float] = []
    sliced_margins: list[float] = []
    sliced_cells = 0
    target_low = target % low_modulus
    for witness in witnesses:
        low_sum = sum(
            (label % low_modulus) * bit for label, bit in zip(labels, witness)
        )
        carry = (low_sum - target_low) // low_modulus
        if carry not in sliced_basis_cache:
            sliced_basis_cache[carry] = _carry_reduced_kernel(
                n_bits,
                labels,
                target,
                low_bits,
                carry,
                embedding_scale,
                low_constraint_scale,
                lll_delta,
            )
            sliced_gs_values.append(
                _minimum_gram_schmidt_squared(sliced_basis_cache[carry])
            )
        error = [1 - 2 * bit for bit in witness] + [0, 0]
        returned_zero, margin, _ = babai_zero_cell_margin(
            sliced_basis_cache[carry], error
        )
        sliced_cells += returned_zero
        sliced_margins.append(margin)
    sliced_gs = min(sliced_gs_values) if sliced_gs_values else 0.0
    complete = not truncated
    return AffineBDDGeometryTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        exact_witness_count=witness_count,
        enumerated_witness_count=len(witnesses),
        witness_enumeration_truncated=truncated,
        target_legal=witness_count > 0,
        standard_babai_solved=standard_solved,
        standard_witness_cell_count=standard_cells,
        standard_maximum_cell_margin=max(standard_margins) if standard_margins else None,
        standard_minimum_gram_schmidt_squared=standard_gs,
        standard_minimum_gram_schmidt_to_four_m_ratio=standard_gs / (4 * register_count),
        standard_global_bdd_condition_satisfied=standard_gs > 4 * register_count,
        standard_cell_prediction_consistent=(
            not complete or standard_solved == (standard_cells > 0)
        ),
        constrained_low_bits=low_bits,
        carry_sliced_babai_solved=sliced_solved,
        carry_sliced_witness_cell_count=sliced_cells,
        carry_sliced_maximum_cell_margin=max(sliced_margins) if sliced_margins else None,
        carry_sliced_minimum_gram_schmidt_squared=sliced_gs,
        carry_sliced_minimum_gram_schmidt_to_four_m_ratio=(
            sliced_gs / (4 * register_count) if sliced_gs else 0.0
        ),
        carry_sliced_global_bdd_condition_satisfied=sliced_gs > 4 * register_count,
        carry_sliced_cell_prediction_consistent=(
            not complete or sliced_solved == (sliced_cells > 0)
        ),
    )


def run_affine_bdd_geometry(
    n_values: Sequence[int] = (12, 16, 20, 24, 28, 32),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 2,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    witness_cap: int = 256,
    seed: int = 0,
) -> DCPSubsetSumAffineBDDGeometryReport:
    if trials_per_row < 1:
        raise ValueError("trials per row must be positive")
    trials = [
        run_affine_bdd_geometry_trial(
            n_bits,
            offset,
            trial_index,
            log_multiplier,
            embedding_scale,
            low_constraint_scale,
            lll_delta,
            witness_cap,
            seed + 1_000_003 * n_index + 10_007 * offset_index + trial_index,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for trial_index in range(trials_per_row)
    ]
    rows: list[AffineBDDGeometryScalingRow] = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            legal = [trial for trial in group if trial.target_legal]
            standard_margins = [
                trial.standard_maximum_cell_margin
                for trial in legal
                if trial.standard_maximum_cell_margin is not None
            ]
            sliced_margins = [
                trial.carry_sliced_maximum_cell_margin
                for trial in legal
                if trial.carry_sliced_maximum_cell_margin is not None
            ]
            rows.append(
                AffineBDDGeometryScalingRow(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_count=len(group),
                    legal_trial_count=len(legal),
                    complete_witness_enumeration_count=sum(
                        not trial.witness_enumeration_truncated for trial in group
                    ),
                    standard_positive_cell_trial_count=sum(
                        trial.standard_witness_cell_count > 0 for trial in legal
                    ),
                    carry_sliced_positive_cell_trial_count=sum(
                        trial.carry_sliced_witness_cell_count > 0 for trial in legal
                    ),
                    standard_global_bdd_trial_count=sum(
                        trial.standard_global_bdd_condition_satisfied for trial in legal
                    ),
                    carry_sliced_global_bdd_trial_count=sum(
                        trial.carry_sliced_global_bdd_condition_satisfied for trial in legal
                    ),
                    mean_standard_maximum_margin=(
                        sum(standard_margins) / len(standard_margins)
                        if standard_margins
                        else None
                    ),
                    mean_carry_sliced_maximum_margin=(
                        sum(sliced_margins) / len(sliced_margins)
                        if sliced_margins
                        else None
                    ),
                    standard_prediction_inconsistency_count=sum(
                        not trial.standard_cell_prediction_consistent for trial in group
                    ),
                    carry_sliced_prediction_inconsistency_count=sum(
                        not trial.carry_sliced_cell_prediction_consistent for trial in group
                    ),
                    empirical_row_is_source_coverage_theorem=False,
                )
            )
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "exact_witness_enumeration_trial_count": sum(
            not trial.witness_enumeration_truncated for trial in trials
        ),
        "legal_trial_count": sum(trial.target_legal for trial in trials),
        "standard_positive_babai_cell_trial_count": sum(
            trial.target_legal and trial.standard_witness_cell_count > 0 for trial in trials
        ),
        "carry_sliced_positive_babai_cell_trial_count": sum(
            trial.target_legal and trial.carry_sliced_witness_cell_count > 0 for trial in trials
        ),
        "standard_global_bdd_condition_trial_count": sum(
            trial.standard_global_bdd_condition_satisfied for trial in trials
        ),
        "carry_sliced_global_bdd_condition_trial_count": sum(
            trial.carry_sliced_global_bdd_condition_satisfied for trial in trials
        ),
        "cell_prediction_inconsistency_count": sum(
            not trial.standard_cell_prediction_consistent
            or not trial.carry_sliced_cell_prediction_consistent
            for trial in trials
        ),
        "tail_standard_positive_cell_trial_count": sum(
            row.standard_positive_cell_trial_count for row in tail
        ),
        "tail_carry_sliced_positive_cell_trial_count": sum(
            row.carry_sliced_positive_cell_trial_count for row in tail
        ),
        "maximum_n_bits": tail_n,
        "proved_source_bdd_coverage_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumAffineBDDGeometryReport(
        created_at=utc_now(),
        geometry_contract={
            "source": "independent uniform labels and targets with exact MITM witness enumeration",
            "error": "+/-1 binary coordinates and zero constraint coordinates for each exact witness",
            "cell_test": "exact-rational reverse Gram-Schmidt Babai zero-cell membership",
            "global_sufficient_condition": "min Gram-Schmidt squared length > 4m",
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "exact_cell_prediction_consistent": metrics["cell_prediction_inconsistency_count"] == 0,
            "global_bdd_condition_observed": (
                metrics["standard_global_bdd_condition_trial_count"]
                + metrics["carry_sliced_global_bdd_condition_trial_count"]
                > 0
            ),
            "finite_cell_frequency_is_source_theorem": False,
            "source_bdd_coverage_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact cell membership diagnoses nearest-plane behavior, but only a source-distribution theorem for "
                "positive margins could establish inverse-polynomial decoding coverage."
            ),
        },
        status="exact-affine-babai-cell-audit-no-source-bdd-theorem",
        summary=(
            f"Audited all materialized witnesses in {len(trials)} source trials through n={tail_n}; standard/carry "
            f"positive-cell trials={metrics['standard_positive_babai_cell_trial_count']}/"
            f"{metrics['carry_sliced_positive_babai_cell_trial_count']}, tail="
            f"{metrics['tail_standard_positive_cell_trial_count']}/"
            f"{metrics['tail_carry_sliced_positive_cell_trial_count']}; no source BDD theorem."
        ),
        falsifiers_triggered=[
            "Positive Babai-cell membership is checked against every materialized legal witness, not inferred from output.",
            "The strong global Gram-Schmidt BDD condition is recorded separately from witness-specific cells.",
            "Tail cell disappearance falsifies small-n nearest-plane geometry.",
            "Finite cell frequencies are not promoted to source-coverage theorems.",
        ],
    )


def write_affine_bdd_geometry(
    path: Path = DCP_SUBSET_SUM_AFFINE_BDD_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs,
) -> dict:
    payload = asdict(run_affine_bdd_geometry(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-FINITE-BABAI-CELLS-NOT-SOURCE-BDD-THEOREM",
                source=str(path),
                claim="Finite exact Babai-cell membership proves inverse-polynomial affine decoding coverage.",
                reason_invalid=(
                    "Cell membership exactly explains sampled runs but has no analytic lower bound over the source distribution."
                ),
                lesson=(
                    "Derive a source law for witness-specific Gram-Schmidt coordinates or abandon nearest plane as the "
                    "asymptotic decoder."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-AFFINE-BDD-GEOMETRY"
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
                artifacts={"dcp_subset_sum_affine_bdd_geometry": str(path)},
            )
        )
    return payload
