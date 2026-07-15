"""Carry-sliced LLL baseline for density-one modular subset sum."""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator, Sequence

from sympy import Matrix

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from dcp_subset_sum_lattice_search import solve_with_lll_embedding
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CarrySliceLatticeTrial:
    n_bits: int
    register_count: int
    register_offset: int
    constrained_low_bits: int
    embedding_scale: int
    low_constraint_scale: int
    lll_delta: float
    combination_arity: int
    target_legal: bool
    reachable_carry_count: int
    carry_count_upper_bound: int
    carry_enumeration_polynomial: bool
    baseline_solved: bool
    carry_sliced_solved: bool
    carry_sliced_witness_valid: bool
    winning_carry: int | None
    candidate_vectors_checked: int
    maximum_entry_bit_length: int


@dataclass(frozen=True)
class CarrySliceLatticeScalingRow:
    n_bits: int
    register_offset: int
    log_multiplier: int
    embedding_scale: int
    low_constraint_scale: int
    lll_delta: float
    combination_arity: int
    trial_count: int
    legal_trial_count: int
    baseline_success_count: int
    carry_sliced_success_count: int
    carry_sliced_only_success_count: int
    baseline_only_success_count: int
    invalid_witness_count: int
    carry_sliced_legal_coverage: float | None
    mean_reachable_carry_count: float
    polynomial_carry_enumeration_proved: bool
    uniform_inverse_polynomial_coverage_proved: bool
    source_contract_satisfied: bool


@dataclass(frozen=True)
class DCPSubsetSumCarrySliceLatticeReport:
    created_at: str
    solver_contract: dict[str, str]
    rows: list[CarrySliceLatticeScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def constrained_low_bits(n_bits: int, log_multiplier: int) -> int:
    if n_bits < 4:
        raise ValueError("n_bits must be at least 4")
    if log_multiplier < 1:
        raise ValueError("log_multiplier must be positive")
    return min(n_bits - 1, max(1, math.ceil(log_multiplier * math.log2(n_bits))))


def reachable_carries(labels: Sequence[int], target: int, low_bits: int) -> list[int]:
    """Return exact low-sum carry slices using a polynomial pseudopolynomial DP."""
    low_modulus = 1 << low_bits
    low_labels = [int(label) & (low_modulus - 1) for label in labels]
    maximum_sum = sum(low_labels)
    reachable = bytearray(maximum_sum + 1)
    reachable[0] = 1
    current_maximum = 0
    for label in low_labels:
        for value in range(current_maximum, -1, -1):
            if reachable[value]:
                reachable[value + label] = 1
        current_maximum += label
    target_low = int(target) & (low_modulus - 1)
    if target_low > maximum_sum:
        return []
    return [
        carry
        for carry in range((maximum_sum - target_low) // low_modulus + 1)
        if reachable[target_low + carry * low_modulus]
    ]


def carry_sliced_embedding(
    labels: Sequence[int],
    target: int,
    n_bits: int,
    low_bits: int,
    carry: int,
    embedding_scale: int,
    low_constraint_scale: int,
) -> Matrix:
    if embedding_scale < 1 or low_constraint_scale < 1:
        raise ValueError("embedding scales must be positive")
    modulus = 1 << n_bits
    low_modulus = 1 << low_bits
    high_modulus = modulus // low_modulus
    register_count = len(labels)
    dimension = register_count + 3
    low_labels = [int(label) & (low_modulus - 1) for label in labels]
    high_labels = [(int(label) % modulus) >> low_bits for label in labels]
    target_low_sum = (int(target) & (low_modulus - 1)) + carry * low_modulus
    target_high_residue = ((int(target) >> low_bits) - carry) % high_modulus
    rows: list[list[int]] = []
    for index, (high_label, low_label) in enumerate(zip(high_labels, low_labels)):
        row = [0] * dimension
        row[index] = 2
        row[register_count] = 2 * embedding_scale * high_label
        row[register_count + 1] = 2 * low_constraint_scale * low_label
        rows.append(row)
    modulus_row = [0] * dimension
    modulus_row[register_count] = 2 * embedding_scale * high_modulus
    rows.append(modulus_row)
    target_row = [1] * register_count + [
        2 * embedding_scale * target_high_residue,
        2 * low_constraint_scale * target_low_sum,
        1,
    ]
    rows.append(target_row)
    return Matrix(rows)


def _candidate_vectors(
    reduced_rows: list[list[int]], combination_arity: int
) -> Iterator[list[int]]:
    for row in reduced_rows:
        for sign in (-1, 1):
            yield [sign * value for value in row]
    if combination_arity >= 2:
        for left_index, right_index in itertools.combinations(range(len(reduced_rows)), 2):
            for left_sign, right_sign in itertools.product((-1, 1), repeat=2):
                yield [
                    left_sign * left + right_sign * right
                    for left, right in zip(reduced_rows[left_index], reduced_rows[right_index])
                ]


def decode_carry_sliced_vector(
    vector: Sequence[int],
    labels: Sequence[int],
    target: int,
    n_bits: int,
    low_bits: int,
    carry: int,
) -> list[int] | None:
    oriented = list(vector)
    if oriented[-1] == 1:
        oriented = [-value for value in oriented]
    if oriented[-1] != -1 or oriented[-2] != 0 or oriented[-3] != 0:
        return None
    if any(value not in {-1, 1} for value in oriented[:-3]):
        return None
    witness = [(value + 1) // 2 for value in oriented[:-3]]
    modulus = 1 << n_bits
    if sum(label * bit for label, bit in zip(labels, witness)) % modulus != target % modulus:
        return None
    low_modulus = 1 << low_bits
    low_sum = sum((int(label) & (low_modulus - 1)) * bit for label, bit in zip(labels, witness))
    target_low = int(target) & (low_modulus - 1)
    if low_sum != target_low + carry * low_modulus:
        return None
    return witness


def solve_with_carry_sliced_lll(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    low_bits: int,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
) -> tuple[list[int] | None, int, int | None, int, int]:
    if combination_arity not in {1, 2}:
        raise ValueError("combination_arity must be 1 or 2")
    carries = reachable_carries(labels, target, low_bits)
    checked = 0
    maximum_bits = 0
    for carry in carries:
        basis = carry_sliced_embedding(
            labels,
            target,
            n_bits,
            low_bits,
            carry,
            embedding_scale,
            low_constraint_scale,
        )
        maximum_bits = max(maximum_bits, max(abs(int(value)).bit_length() for value in basis))
        reduced = basis.lll(delta=lll_delta).tolist()
        for vector in _candidate_vectors(reduced, combination_arity):
            checked += 1
            witness = decode_carry_sliced_vector(
                vector, labels, target, n_bits, low_bits, carry
            )
            if witness is not None:
                return witness, checked, carry, len(carries), maximum_bits
    return None, checked, None, len(carries), maximum_bits


def run_carry_slice_lattice_trial(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    combination_arity: int,
    seed: int,
) -> CarrySliceLatticeTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    target_legal = bool(subset_sum_counts(n_bits, labels)[target])
    baseline, _, _ = solve_with_lll_embedding(
        n_bits, labels, target, embedding_scale, lll_delta, combination_arity
    )
    witness, checked, winning_carry, carry_count, maximum_bits = solve_with_carry_sliced_lll(
        n_bits,
        labels,
        target,
        low_bits,
        embedding_scale,
        low_constraint_scale,
        lll_delta,
        combination_arity,
    )
    valid = witness is not None and sum(
        label * bit for label, bit in zip(labels, witness)
    ) % modulus == target
    return CarrySliceLatticeTrial(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        constrained_low_bits=low_bits,
        embedding_scale=embedding_scale,
        low_constraint_scale=low_constraint_scale,
        lll_delta=lll_delta,
        combination_arity=combination_arity,
        target_legal=target_legal,
        reachable_carry_count=carry_count,
        carry_count_upper_bound=register_count,
        carry_enumeration_polynomial=carry_count <= register_count,
        baseline_solved=baseline is not None,
        carry_sliced_solved=witness is not None,
        carry_sliced_witness_valid=valid,
        winning_carry=winning_carry,
        candidate_vectors_checked=checked,
        maximum_entry_bit_length=maximum_bits,
    )


def _aggregate(trials: Sequence[CarrySliceLatticeTrial], log_multiplier: int) -> CarrySliceLatticeScalingRow:
    first = trials[0]
    legal = [trial for trial in trials if trial.target_legal]
    return CarrySliceLatticeScalingRow(
        n_bits=first.n_bits,
        register_offset=first.register_offset,
        log_multiplier=log_multiplier,
        embedding_scale=first.embedding_scale,
        low_constraint_scale=first.low_constraint_scale,
        lll_delta=first.lll_delta,
        combination_arity=first.combination_arity,
        trial_count=len(trials),
        legal_trial_count=len(legal),
        baseline_success_count=sum(trial.baseline_solved for trial in trials),
        carry_sliced_success_count=sum(trial.carry_sliced_solved for trial in trials),
        carry_sliced_only_success_count=sum(
            trial.carry_sliced_solved and not trial.baseline_solved for trial in trials
        ),
        baseline_only_success_count=sum(
            trial.baseline_solved and not trial.carry_sliced_solved for trial in trials
        ),
        invalid_witness_count=sum(
            trial.carry_sliced_solved and not trial.carry_sliced_witness_valid for trial in trials
        ),
        carry_sliced_legal_coverage=(
            sum(trial.carry_sliced_solved for trial in legal) / len(legal) if legal else None
        ),
        mean_reachable_carry_count=sum(trial.reachable_carry_count for trial in trials) / len(trials),
        polynomial_carry_enumeration_proved=all(trial.carry_enumeration_polynomial for trial in trials),
        uniform_inverse_polynomial_coverage_proved=False,
        source_contract_satisfied=False,
    )


def run_carry_slice_lattice_search(
    n_values: Sequence[int] = (10, 12, 14, 16),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    embedding_scales: Sequence[int] = (4,),
    low_constraint_scales: Sequence[int] = (4,),
    lll_deltas: Sequence[float] = (0.75, 0.99),
    combination_arities: Sequence[int] = (1,),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPSubsetSumCarrySliceLatticeReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[CarrySliceLatticeScalingRow] = []
    for ni, n_bits in enumerate(n_values):
        for oi, offset in enumerate(register_offsets):
            for mi, multiplier in enumerate(log_multipliers):
                for si, scale in enumerate(embedding_scales):
                    for li, low_scale in enumerate(low_constraint_scales):
                        for di, delta in enumerate(lll_deltas):
                            for ai, arity in enumerate(combination_arities):
                                trials = [
                                    run_carry_slice_lattice_trial(
                                        n_bits,
                                        offset,
                                        multiplier,
                                        scale,
                                        low_scale,
                                        delta,
                                        arity,
                                        seed + 1_000_003 * ni + 100_003 * oi + 10_007 * mi
                                        + 1_009 * si + 101 * li + 17 * di + 3 * ai + trial,
                                    )
                                    for trial in range(trials_per_row)
                                ]
                                rows.append(_aggregate(trials, multiplier))
    tail_n = max(n_values)
    tail_rows = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "trial_count": sum(row.trial_count for row in rows),
        "baseline_success_count": sum(row.baseline_success_count for row in rows),
        "carry_sliced_success_count": sum(row.carry_sliced_success_count for row in rows),
        "carry_sliced_only_success_count": sum(row.carry_sliced_only_success_count for row in rows),
        "baseline_only_success_count": sum(row.baseline_only_success_count for row in rows),
        "tail_row_count": len(tail_rows),
        "tail_baseline_success_count": sum(row.baseline_success_count for row in tail_rows),
        "tail_carry_sliced_success_count": sum(row.carry_sliced_success_count for row in tail_rows),
        "invalid_witness_count": sum(row.invalid_witness_count for row in rows),
        "polynomial_carry_enumeration_certificate_count": sum(
            row.polynomial_carry_enumeration_proved for row in rows
        ),
        "proved_uniform_inverse_polynomial_coverage_count": 0,
        "proved_reversible_uniform_implementation_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumCarrySliceLatticeReport(
        created_at=utc_now(),
        solver_contract={
            "decomposition": (
                "write a_i=l_i+2^b h_i and enumerate carry k with sum l_i x_i=t_low+k2^b"
            ),
            "carry_bound": "0<=k<=m-1, so all carry slices are polynomially enumerable",
            "slice_embedding": (
                "LLL embedding enforces the exact low-sum equation and high modular equation "
                "sum h_i x_i=t_high-k mod 2^(n-b)"
            ),
            "comparison": "unsliced and carry-sliced LLL use identical labels, targets, delta, scale, and extraction arity",
            "promotion_requirement": (
                "uniform inverse-polynomial legal-input coverage plus deterministic reversible polynomial implementation"
            ),
        },
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "polynomial_carry_decomposition_proved": (
                metrics["polynomial_carry_enumeration_certificate_count"] == len(rows)
            ),
            "all_returned_witnesses_verified": metrics["invalid_witness_count"] == 0,
            "finite_improvement_is_coverage_theorem": False,
            "uniform_inverse_polynomial_coverage_proved": False,
            "reversible_uniform_implementation_proved": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Carry slicing is a new deterministic polynomial LLL class, but finite paired success does not establish "
                "inverse-polynomial coverage or reversible composition with Regev's matching theorem."
            ),
        },
        status="carry-sliced-lll-audited-no-coverage-theorem",
        summary=(
            f"Compared unsliced and carry-sliced LLL on {metrics['trial_count']} paired trials through n={tail_n}. "
            f"Carry-sliced-only successes={metrics['carry_sliced_only_success_count']}, baseline-only successes="
            f"{metrics['baseline_only_success_count']}, tail sliced successes="
            f"{metrics['tail_carry_sliced_success_count']}, and source-contract rows=0."
        ),
        falsifiers_triggered=[
            "Every carry slice is charged; no favorable carry is supplied as advice.",
            "Exact low-sum reachability is computed by a polynomial DP because b=O(log n).",
            "Unsliced and sliced solvers are compared on the same random instances and extraction class.",
            "Every returned vector is decoded and verified against the original modulus.",
            "Finite improvement cannot replace an asymptotic legal-coverage theorem.",
        ],
    )


def write_carry_slice_lattice_search(
    path: Path = DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH,
    n_values: Sequence[int] = (10, 12, 14, 16),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    embedding_scales: Sequence[int] = (4,),
    low_constraint_scales: Sequence[int] = (4,),
    lll_deltas: Sequence[float] = (0.75, 0.99),
    combination_arities: Sequence[int] = (1,),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_carry_slice_lattice_search(
        n_values,
        register_offsets,
        log_multipliers,
        embedding_scales,
        low_constraint_scales,
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
                id="NEG-DCP-CARRY-SLICED-LLL-FINITE-WITHOUT-COVERAGE-THEOREM",
                source=str(path),
                claim=(
                    "Finite success of a low-carry-sliced LLL embedding proves a polynomial partial density-one "
                    "subset-sum solver."
                ),
                reason_invalid=(
                    "The paired finite audit has no uniform inverse-polynomial legal-input coverage or reversible "
                    "composition theorem, regardless of whether it improves the unsliced baseline at tested sizes."
                ),
                lesson=(
                    "Retain carry slicing as a serious polynomial solver class. Next prove or falsify its average-case "
                    "short-vector separation and tail coverage instead of tuning finite scales."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "carry_sliced_only_success_count": payload["headline_metrics"]["carry_sliced_only_success_count"],
                    "tail_carry_sliced_success_count": payload["headline_metrics"]["tail_carry_sliced_success_count"],
                    "proved_uniform_inverse_polynomial_coverage_count": 0,
                    "source_contract_satisfying_row_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE"
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
                artifacts={"dcp_subset_sum_carry_slice_lattice": str(path)},
            )
        )
    return payload
