"""Exact full-domain ANF audit for power-of-two subset-sum carry bits."""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_subset_sum_two_adic_search import subset_sums_by_mask
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_CARRY_ANF_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_anf.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-CARRY-ANF"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CarryANFRow:
    n_bits: int
    register_count: int
    register_offset: int
    trial_index: int
    output_bit: int
    exact_anf_degree: int
    monomial_count: int
    maximum_degree_monomial_count: int
    bounded_degree_at_most_three: bool
    polynomially_sparse_at_cubic_budget: bool
    full_domain_truth_table_log2_cost: int


@dataclass(frozen=True)
class CarryANFTrialSummary:
    n_bits: int
    register_count: int
    register_offset: int
    trial_index: int
    maximum_anf_degree: int
    final_bit_anf_degree: int
    maximum_monomial_count: int
    every_carry_bounded_degree: bool
    every_carry_cubic_sparse: bool
    polynomial_witness_solver_constructed: bool


@dataclass(frozen=True)
class DCPSubsetSumCarryANFReport:
    created_at: str
    algebraic_contract: dict[str, str]
    rows: list[CarryANFRow]
    trial_summaries: list[CarryANFTrialSummary]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def anf_coefficients(truth_table: Sequence[int | bool], variable_count: int) -> bytearray:
    expected = 1 << variable_count
    if len(truth_table) != expected:
        raise ValueError("truth table length must equal 2^variable_count")
    coefficients = bytearray(int(value) & 1 for value in truth_table)
    for variable in range(variable_count):
        bit = 1 << variable
        for mask in range(expected):
            if mask & bit:
                coefficients[mask] ^= coefficients[mask ^ bit]
    return coefficients


def anf_profile(truth_table: Sequence[int | bool], variable_count: int) -> tuple[int, int, int]:
    coefficients = anf_coefficients(truth_table, variable_count)
    active = [mask for mask, coefficient in enumerate(coefficients) if coefficient]
    if not active:
        return 0, 0, 0
    degree = max(mask.bit_count() for mask in active)
    top_count = sum(mask.bit_count() == degree for mask in active)
    return degree, len(active), top_count


def analyze_carry_anf_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
) -> tuple[list[CarryANFRow], CarryANFTrialSummary]:
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    register_count = n_bits + register_offset
    if register_count < 1:
        raise ValueError("register count must be positive")
    modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    sums = subset_sums_by_mask(labels, modulus)
    rows: list[CarryANFRow] = []
    for output_bit in range(n_bits):
        target_bit = (target >> output_bit) & 1
        truth = [((value >> output_bit) & 1) == target_bit for value in sums]
        degree, monomial_count, top_count = anf_profile(truth, register_count)
        rows.append(
            CarryANFRow(
                n_bits=n_bits,
                register_count=register_count,
                register_offset=register_offset,
                trial_index=trial_index,
                output_bit=output_bit,
                exact_anf_degree=degree,
                monomial_count=monomial_count,
                maximum_degree_monomial_count=top_count,
                bounded_degree_at_most_three=degree <= 3,
                polynomially_sparse_at_cubic_budget=monomial_count <= register_count**3,
                full_domain_truth_table_log2_cost=register_count,
            )
        )
    summary = CarryANFTrialSummary(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        trial_index=trial_index,
        maximum_anf_degree=max(row.exact_anf_degree for row in rows),
        final_bit_anf_degree=rows[-1].exact_anf_degree,
        maximum_monomial_count=max(row.monomial_count for row in rows),
        every_carry_bounded_degree=all(row.bounded_degree_at_most_three for row in rows),
        every_carry_cubic_sparse=all(row.polynomially_sparse_at_cubic_budget for row in rows),
        polynomial_witness_solver_constructed=False,
    )
    return rows, summary


def _linear_slope(points: Sequence[tuple[float, float]]) -> float:
    if len(points) < 2:
        return 0.0
    mean_x = sum(x for x, _ in points) / len(points)
    mean_y = sum(y for _, y in points) / len(points)
    denominator = sum((x - mean_x) ** 2 for x, _ in points)
    if denominator == 0.0:
        return 0.0
    return sum((x - mean_x) * (y - mean_y) for x, y in points) / denominator


def run_subset_sum_carry_anf_audit(
    n_values: Sequence[int] = (6, 8, 10, 12),
    register_offsets: Sequence[int] = (2, 4),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPSubsetSumCarryANFReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[CarryANFRow] = []
    summaries: list[CarryANFTrialSummary] = []
    for n_index, n_bits in enumerate(n_values):
        for offset_index, offset in enumerate(register_offsets):
            for trial_index in range(trials_per_row):
                trial_rows, trial_summary = analyze_carry_anf_trial(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_index=trial_index,
                    seed=seed + 1_000_003 * n_index + 10_007 * offset_index + trial_index,
                )
                rows.extend(trial_rows)
                summaries.append(trial_summary)
    tail_rows = [row for row in rows if row.output_bit >= max(1, row.n_bits - 3)]
    degree_slope = _linear_slope(
        [(float(summary.n_bits), float(summary.final_bit_anf_degree)) for summary in summaries]
    )
    metrics: dict[str, int | float] = {
        "trial_count": len(summaries),
        "carry_row_count": len(rows),
        "bounded_degree_row_count": sum(row.bounded_degree_at_most_three for row in rows),
        "cubic_sparse_row_count": sum(row.polynomially_sparse_at_cubic_budget for row in rows),
        "tail_carry_row_count": len(tail_rows),
        "tail_bounded_degree_row_count": sum(row.bounded_degree_at_most_three for row in tail_rows),
        "all_carries_bounded_degree_trial_count": sum(summary.every_carry_bounded_degree for summary in summaries),
        "all_carries_cubic_sparse_trial_count": sum(summary.every_carry_cubic_sparse for summary in summaries),
        "maximum_observed_anf_degree": max(summary.maximum_anf_degree for summary in summaries),
        "maximum_observed_monomial_count": max(summary.maximum_monomial_count for summary in summaries),
        "fitted_final_bit_degree_slope_per_n": degree_slope,
        "maximum_full_domain_enumeration_log2_cost": max(summary.register_count for summary in summaries),
        "proved_uniform_bounded_degree_carry_family_count": 0,
        "proved_polynomial_algebraic_witness_solver_count": 0,
        "proved_uniform_inverse_polynomial_coverage_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumCarryANFReport(
        created_at=utc_now(),
        algebraic_contract={
            "function": "for every output bit b, x maps to [bit_b(sum_i a_i x_i)=bit_b(t)] on the full Boolean cube",
            "representation": "exact algebraic normal form over F_2 via the Boolean Mobius transform",
            "audit_cost": "Theta(n r 2^r) over r=n+O(1) variables; exponential and never a solver",
            "positive_requirement": "uniform bounded-size symbolic construction plus polynomial solution of all carry equations and legal coverage",
            "scope_limit": "high ANF degree rejects low-degree algebraic reconstruction only; it is not a subset-sum lower bound",
        },
        rows=rows,
        trial_summaries=summaries,
        headline_metrics=metrics,
        claim_gate={
            "full_domain_anf_exactly_computed": True,
            "restricted_domain_interpolation_removed": True,
            "high_anf_degree_implies_subset_sum_hardness": False,
            "uniform_bounded_degree_carry_family_proved": False,
            "polynomial_algebraic_witness_solver_constructed": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact full-domain carry ANFs measure algebraic growth without restricted-fiber interpolation, but the "
                "audit is exponential and no uniform bounded-degree representation or polynomial witness solver follows."
            ),
        },
        status="full-domain-carry-anf-growth-audited-no-algebraic-solver",
        summary=(
            f"Computed {metrics['carry_row_count']} exact full-domain carry ANFs across {metrics['trial_count']} instances. "
            f"Tail bounded-degree rows={metrics['tail_bounded_degree_row_count']}/{metrics['tail_carry_row_count']}; "
            f"maximum degree={metrics['maximum_observed_anf_degree']}; source-contract rows=0."
        ),
        falsifiers_triggered=[
            "The first parity constraint is affine, but later carry constraints must be audited separately.",
            "Restricted-fiber low-degree interpolation is removed by evaluating ANF on the full Boolean cube.",
            "Exact Mobius transformation costs 2^(n+O(1)) and supplies no polynomial witness algorithm.",
            "High finite ANF degree blocks only bounded-degree algebraic reconstruction, not unknown structural algorithms.",
            "Any surviving algebraic route needs a uniform symbolic construction, polynomial solving theorem, legal coverage, and reversibility.",
        ],
    )


def write_subset_sum_carry_anf_audit(
    path: Path = DCP_SUBSET_SUM_CARRY_ANF_PATH,
    n_values: Sequence[int] = (6, 8, 10, 12),
    register_offsets: Sequence[int] = (2, 4),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_carry_anf_audit(n_values, register_offsets, trials_per_row, seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-FINITE-FULL-DOMAIN-CARRY-ANF-WITHOUT-SOLVER",
                source=str(path),
                claim="Exact finite carry ANF profiles establish a polynomial algebraic density-one subset-sum solver.",
                reason_invalid=(
                    "The truth tables and Mobius transforms are exponential, finite degree trends are not uniform theorems, "
                    "and even compact polynomial systems require a separate polynomial witness-finding algorithm."
                ),
                lesson=(
                    "Use full-domain ANF as a rejection test for bounded-degree carry hypotheses. Keep other symbolic, "
                    "lattice, representation, and non-algebraic solver classes open."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "carry_row_count": payload["headline_metrics"]["carry_row_count"],
                    "tail_bounded_degree_row_count": payload["headline_metrics"]["tail_bounded_degree_row_count"],
                    "maximum_observed_anf_degree": payload["headline_metrics"]["maximum_observed_anf_degree"],
                    "source_contract_satisfying_row_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-CARRY-ANF"
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
                artifacts={"dcp_subset_sum_carry_anf": str(path)},
            )
        )
    return payload
