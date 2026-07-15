"""Search deterministic LLL embeddings for Regev's partial subset-sum contract."""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from sympy import Matrix

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_LATTICE_SEARCH_PATH = Path("research/classical_baselines/dcp_subset_sum_lattice_search.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-LATTICE-SEARCH"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class LatticeSolverTrial:
    n_bits: int
    register_count: int
    register_offset: int
    embedding_scale: int
    lll_delta: float
    combination_arity: int
    target_legal_exactly_known: bool
    target_legal: bool | None
    solved: bool
    returned_witness_valid: bool
    candidate_vectors_checked: int
    matrix_dimension: int
    maximum_entry_bit_length: int


@dataclass(frozen=True)
class LatticeSolverScalingRow:
    n_bits: int
    register_offset: int
    embedding_scale: int
    lll_delta: float
    combination_arity: int
    trial_count: int
    exact_legal_trial_count: int
    success_count: int
    invalid_witness_count: int
    overall_success_rate: float
    exact_legal_coverage: float | None
    zero_success_95pct_upper_bound: float | None
    polynomial_integer_bit_complexity: bool
    deterministic_solver: bool
    uniform_inverse_polynomial_coverage_proved: bool
    source_contract_satisfied: bool


@dataclass(frozen=True)
class LatticeEmbeddingRecord:
    component: str
    mathematical_role: str
    resource_class: str
    caveat: str


@dataclass(frozen=True)
class LLLEmbeddingDiagnostics:
    witness: list[int] | None
    candidate_vectors_checked: int
    maximum_entry_bit_length: int
    reduced_row_count: int
    ideal_witness_norm_squared: int
    minimum_reduced_row_norm_squared: int
    minimum_reduced_to_ideal_norm_ratio: float
    marker_row_count: int
    minimum_marker_modulus_coordinate: int | None
    minimum_binary_witness_defect: int


@dataclass(frozen=True)
class DCPSubsetSumLatticeSearchReport:
    created_at: str
    solver_contract: dict[str, str]
    rows: list[LatticeSolverScalingRow]
    embedding_records: list[LatticeEmbeddingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def modular_subset_sum_embedding(
    labels: Sequence[int],
    target: int,
    modulus: int,
    embedding_scale: int,
) -> Matrix:
    if embedding_scale < 1:
        raise ValueError("embedding_scale must be positive")
    register_count = len(labels)
    dimension = register_count + 2
    rows: list[list[int]] = []
    for index, label in enumerate(labels):
        row = [0] * dimension
        row[index] = 2
        row[register_count] = 2 * embedding_scale * (int(label) % modulus)
        rows.append(row)
    modulus_row = [0] * dimension
    modulus_row[register_count] = 2 * embedding_scale * modulus
    rows.append(modulus_row)
    target_row = [1] * register_count + [2 * embedding_scale * (target % modulus), 1]
    rows.append(target_row)
    return Matrix(rows)


def _candidate_vectors(reduced_rows: list[list[int]], combination_arity: int):
    checked = 0
    for row in reduced_rows:
        for sign in (-1, 1):
            checked += 1
            yield [sign * value for value in row], checked
    if combination_arity >= 2:
        for left_index, right_index in itertools.combinations(range(len(reduced_rows)), 2):
            for left_sign, right_sign in itertools.product((-1, 1), repeat=2):
                checked += 1
                yield [
                    left_sign * left + right_sign * right
                    for left, right in zip(reduced_rows[left_index], reduced_rows[right_index])
                ], checked


def _decode_embedding_vector(
    vector: Sequence[int],
    labels: Sequence[int],
    target: int,
    modulus: int,
) -> list[int] | None:
    oriented = list(vector)
    if oriented[-1] == 1:
        oriented = [-value for value in oriented]
    if oriented[-1] != -1 or oriented[-2] != 0:
        return None
    if any(value not in {-1, 1} for value in oriented[:-2]):
        return None
    witness = [(value + 1) // 2 for value in oriented[:-2]]
    if sum(label * bit for label, bit in zip(labels, witness)) % modulus != target % modulus:
        return None
    return witness


def solve_with_lll_embedding(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
) -> tuple[list[int] | None, int, int]:
    diagnostics = solve_with_lll_embedding_diagnostics(
        n_bits,
        labels,
        target,
        embedding_scale,
        lll_delta,
        combination_arity,
    )
    return (
        diagnostics.witness,
        diagnostics.candidate_vectors_checked,
        diagnostics.maximum_entry_bit_length,
    )


def solve_with_lll_embedding_diagnostics(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
) -> LLLEmbeddingDiagnostics:
    if combination_arity not in {1, 2}:
        raise ValueError("combination_arity must be 1 or 2")
    modulus = 1 << n_bits
    basis = modular_subset_sum_embedding(labels, target, modulus, embedding_scale)
    reduced = basis.lll(delta=lll_delta).tolist()
    register_count = len(labels)
    norms = [sum(int(value) ** 2 for value in row) for row in reduced]
    marker_rows = [row for row in reduced if abs(int(row[-1])) == 1]
    witness: list[int] | None = None
    checked = 0
    for vector, checked in _candidate_vectors(reduced, combination_arity):
        decoded = _decode_embedding_vector(vector, labels, target, modulus)
        if decoded is not None:
            witness = decoded
            break
    maximum_bits = max(abs(int(value)).bit_length() for value in basis)
    ideal_norm = register_count + 1
    minimum_norm = min(norms)
    minimum_defect = min(
        sum(min(abs(int(value) - 1), abs(int(value) + 1)) for value in row[:-2])
        + abs(int(row[-2]))
        + min(abs(int(row[-1]) - 1), abs(int(row[-1]) + 1))
        for row in reduced
    )
    return LLLEmbeddingDiagnostics(
        witness=witness,
        candidate_vectors_checked=checked,
        maximum_entry_bit_length=maximum_bits,
        reduced_row_count=len(reduced),
        ideal_witness_norm_squared=ideal_norm,
        minimum_reduced_row_norm_squared=minimum_norm,
        minimum_reduced_to_ideal_norm_ratio=minimum_norm / ideal_norm,
        marker_row_count=len(marker_rows),
        minimum_marker_modulus_coordinate=(
            min(abs(int(row[-2])) for row in marker_rows) if marker_rows else None
        ),
        minimum_binary_witness_defect=minimum_defect,
    )


def run_lattice_solver_trial(
    n_bits: int,
    register_offset: int,
    embedding_scale: int,
    lll_delta: float,
    combination_arity: int,
    seed: int,
    exact_legality_max_bits: int = 20,
) -> LatticeSolverTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    exact_known = n_bits <= exact_legality_max_bits
    target_legal: bool | None = None
    if exact_known:
        target_legal = bool(subset_sum_counts(n_bits, labels)[target])
    witness, checked, maximum_bits = solve_with_lll_embedding(
        n_bits,
        labels,
        target,
        embedding_scale,
        lll_delta,
        combination_arity,
    )
    valid = witness is not None and sum(label * bit for label, bit in zip(labels, witness)) % modulus == target
    return LatticeSolverTrial(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        embedding_scale=embedding_scale,
        lll_delta=lll_delta,
        combination_arity=combination_arity,
        target_legal_exactly_known=exact_known,
        target_legal=target_legal,
        solved=witness is not None,
        returned_witness_valid=valid,
        candidate_vectors_checked=checked,
        matrix_dimension=register_count + 2,
        maximum_entry_bit_length=maximum_bits,
    )


def _aggregate_trials(trials: Sequence[LatticeSolverTrial]) -> LatticeSolverScalingRow:
    first = trials[0]
    legal = [trial for trial in trials if trial.target_legal is True]
    successes = sum(trial.solved for trial in trials)
    zero_upper = 1.0 - 0.05 ** (1.0 / len(trials)) if successes == 0 else None
    return LatticeSolverScalingRow(
        n_bits=first.n_bits,
        register_offset=first.register_offset,
        embedding_scale=first.embedding_scale,
        lll_delta=first.lll_delta,
        combination_arity=first.combination_arity,
        trial_count=len(trials),
        exact_legal_trial_count=len(legal),
        success_count=successes,
        invalid_witness_count=sum(trial.solved and not trial.returned_witness_valid for trial in trials),
        overall_success_rate=successes / len(trials),
        exact_legal_coverage=(sum(trial.solved for trial in legal) / len(legal) if legal else None),
        zero_success_95pct_upper_bound=zero_upper,
        polynomial_integer_bit_complexity=max(trial.maximum_entry_bit_length for trial in trials) <= first.n_bits + 16,
        deterministic_solver=True,
        uniform_inverse_polynomial_coverage_proved=False,
        source_contract_satisfied=False,
    )


def _embedding_records() -> list[LatticeEmbeddingRecord]:
    return [
        LatticeEmbeddingRecord(
            component="binary-centered coordinates",
            mathematical_role="a solution is represented by first coordinates 2x_i-1 in {-1,+1}",
            resource_class="O(n)-dimensional integer lattice",
            caveat="LLL need not return a particular short solution when many unrelated short vectors compete.",
        ),
        LatticeEmbeddingRecord(
            component="modulus row",
            mathematical_role="allows sum_i x_i a_i-t to vanish modulo N rather than over the integers",
            resource_class="O(n)-bit entries",
            caveat="Polynomial bit complexity does not imply inverse-polynomial random-instance coverage.",
        ),
        LatticeEmbeddingRecord(
            component="target marker coordinate",
            mathematical_role="orients a reduced vector with target-row coefficient -1",
            resource_class="exact deterministic decoding check",
            caveat="Scanning one or two reduced-basis vectors is a restricted polynomial extraction class.",
        ),
        LatticeEmbeddingRecord(
            component="fixed-arity reduced-basis combinations",
            mathematical_role="searches cancellations missed by a single reduced basis row",
            resource_class="O(n^arity) for fixed arity 1 or 2",
            caveat="Growing arity would reintroduce superpolynomial enumeration and is not promoted.",
        ),
    ]


def run_subset_sum_lattice_search(
    n_values: Sequence[int] = (16, 20, 24, 28, 32, 40, 48),
    register_offsets: Sequence[int] = (2, 4, 8),
    embedding_scales: Sequence[int] = (1, 4, 16),
    lll_deltas: Sequence[float] = (0.75, 0.99),
    combination_arities: Sequence[int] = (1, 2),
    trials_per_row: int = 8,
    seed: int = 0,
) -> DCPSubsetSumLatticeSearchReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[LatticeSolverScalingRow] = []
    for n_index, n_bits in enumerate(n_values):
        for offset_index, offset in enumerate(register_offsets):
            for scale_index, scale in enumerate(embedding_scales):
                for delta_index, delta in enumerate(lll_deltas):
                    for arity_index, arity in enumerate(combination_arities):
                        trials = [
                            run_lattice_solver_trial(
                                n_bits,
                                offset,
                                scale,
                                delta,
                                arity,
                                seed=(
                                    seed
                                    + 100_000_007 * n_index
                                    + 1_000_003 * offset_index
                                    + 10_007 * scale_index
                                    + 101 * delta_index
                                    + 17 * arity_index
                                    + trial
                                ),
                            )
                            for trial in range(trials_per_row)
                        ]
                        rows.append(_aggregate_trials(trials))
    tail_threshold = max(n_values) - 8
    tail_rows = [row for row in rows if row.n_bits >= tail_threshold]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "trial_count": sum(row.trial_count for row in rows),
        "successful_trial_count": sum(row.success_count for row in rows),
        "invalid_witness_count": sum(row.invalid_witness_count for row in rows),
        "finite_success_row_count": sum(row.success_count > 0 for row in rows),
        "tail_row_count": len(tail_rows),
        "tail_success_row_count": sum(row.success_count > 0 for row in tail_rows),
        "maximum_tested_n_bits": max(n_values),
        "source_contract_satisfying_row_count": sum(row.source_contract_satisfied for row in rows),
        "proved_uniform_inverse_polynomial_coverage_count": sum(row.uniform_inverse_polynomial_coverage_proved for row in rows),
        "proved_reversible_uniform_implementation_count": 0,
        "proved_polynomial_dcp_decoder_count": 0,
    }
    return DCPSubsetSumLatticeSearchReport(
        created_at=utc_now(),
        solver_contract={
            "input": "uniform A in Z_N^(n+O(1)) and uniform target t",
            "output": "one binary witness x with <A,x>=t mod N, or error",
            "algorithm": "exact integer LLL on the modular target embedding, followed by fixed-arity reduced-basis scan",
            "polynomial_resource_scope": "dimension O(n), entry bit length O(n), fixed delta/scales/arity",
            "promotion_requirement": "uniform inverse-polynomial overall success implies inverse-polynomial legal-input coverage, plus a reversible implementation",
            "finite_evidence_rule": "no finite success rate is marked source-contract satisfying without a scaling theorem",
        },
        rows=rows,
        embedding_records=_embedding_records(),
        headline_metrics=metrics,
        claim_gate={
            "deterministic_polynomial_lattice_baseline_implemented": True,
            "all_returned_witnesses_verified": metrics["invalid_witness_count"] == 0,
            "uniform_inverse_polynomial_coverage_proved": False,
            "reversible_uniform_implementation_proved": False,
            "source_contract_satisfied": False,
            "polynomial_dcp_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The LLL embedding is a meaningful deterministic polynomial candidate, but finite recovery collapses in "
                "the tail and no inverse-polynomial coverage or reversible circuit theorem exists."
            ),
        },
        status="lll-density-one-finite-signal-tail-collapse-no-coverage-theorem",
        summary=(
            f"Ran {metrics['trial_count']} deterministic LLL partial-solver trials across {len(rows)} rows through "
            f"n={metrics['maximum_tested_n_bits']}. Finite success rows={metrics['finite_success_row_count']}; tail success "
            f"rows={metrics['tail_success_row_count']}/{metrics['tail_row_count']}; source-contract rows=0."
        ),
        falsifiers_triggered=[
            "High small-n LLL recovery near density one decays sharply and is not asymptotic evidence.",
            "Polynomial LLL bit complexity alone does not prove inverse-polynomial random legal-input coverage.",
            "Fixed-arity reduced-basis combinations remain polynomial but do not justify growing-arity enumeration.",
            "Every returned witness is checked exactly; solver failure is not confused with target illegality at large n.",
            "A source-contract claim still requires a uniform coverage theorem and reversible deterministic implementation.",
        ],
    )


def write_subset_sum_lattice_search(
    path: Path = DCP_SUBSET_SUM_LATTICE_SEARCH_PATH,
    n_values: Sequence[int] = (16, 20, 24, 28, 32, 40, 48),
    register_offsets: Sequence[int] = (2, 4, 8),
    embedding_scales: Sequence[int] = (1, 4, 16),
    lll_deltas: Sequence[float] = (0.75, 0.99),
    combination_arities: Sequence[int] = (1, 2),
    trials_per_row: int = 8,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_lattice_search(
        n_values,
        register_offsets,
        embedding_scales,
        lll_deltas,
        combination_arities,
        trials_per_row,
        seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-TESTED-LLL-DENSITY-ONE-PARTIAL-SOLVERS",
                source=str(path),
                claim="Small-n success of standard modular LLL embeddings establishes Regev's partial average-case subset-sum assumption.",
                reason_invalid=(
                    "Tested embedding/scaling/basis-combination rows lose success in the scaling tail and have no uniform "
                    "inverse-polynomial legal-input coverage or reversible implementation theorem."
                ),
                lesson=(
                    "Retain LLL as a serious baseline, not positive evidence. A mutation must change the asymptotic short-vector "
                    "geometry, use structural preprocessing, or prove coverage rather than tune finite embedding constants."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "row_count": payload["headline_metrics"]["row_count"],
                    "tail_success_row_count": payload["headline_metrics"]["tail_success_row_count"],
                    "proved_uniform_inverse_polynomial_coverage_count": 0,
                    "source_contract_satisfying_row_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-LATTICE"
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
                artifacts={"dcp_subset_sum_lattice_search": str(path)},
            )
        )
    return payload
