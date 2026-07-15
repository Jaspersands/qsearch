"""Audit 2-adic lifting structure in density-one modular subset sum.

For the power-of-two DCP modulus, a subset-sum witness can be viewed as a
sequence of lifts from congruence modulo 2^b to congruence modulo 2^(b+1).
This module asks whether those lift predicates admit genuinely compact affine
or bounded-degree descriptions.  Exact enumeration is used only as an audit;
it is never promoted as a solver for Regev's average-case contract.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_TWO_ADIC_PATH = Path("research/classical_baselines/dcp_subset_sum_two_adic_search.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-TWO-ADIC-SEARCH"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class TwoAdicLiftRow:
    n_bits: int
    register_count: int
    register_offset: int
    trial_index: int
    lift_bit: int
    prior_fiber_size: int
    lifted_fiber_size: int
    conditional_survival_rate: float
    lifted_affine_hull_dimension: int | None
    lifted_log2_size: float | None
    affine_hull_overcoverage_log2: float | None
    minimum_exact_boolean_degree_capped: int | None
    degree_cap: int
    feature_count_at_exact_degree: int | None
    degree_fit_nonvacuous: bool
    final_target_legal: bool


@dataclass(frozen=True)
class TwoAdicTrialSummary:
    n_bits: int
    register_count: int
    register_offset: int
    trial_index: int
    final_target_legal: bool
    final_solution_count: int
    all_lifts_affine: bool
    all_lifts_bounded_degree_within_cap: bool
    all_bounded_degree_fits_nonvacuous: bool
    maximum_observed_exact_degree_capped: int | None
    final_affine_hull_overcoverage_log2: float | None
    exact_enumeration_log2_cost: int
    polynomial_solver_constructed: bool


@dataclass(frozen=True)
class DCPSubsetSumTwoAdicReport:
    created_at: str
    solver_contract: dict[str, str]
    lift_rows: list[TwoAdicLiftRow]
    trial_summaries: list[TwoAdicTrialSummary]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def subset_sums_by_mask(labels: Sequence[int], modulus: int) -> list[int]:
    """Return all subset sums indexed by mask in O(2^r) exact operations."""
    if modulus < 2 or modulus & (modulus - 1):
        raise ValueError("modulus must be a power of two")
    if not labels:
        raise ValueError("labels must be nonempty")
    sums = [0] * (1 << len(labels))
    for mask in range(1, len(sums)):
        least = mask & -mask
        index = least.bit_length() - 1
        sums[mask] = (sums[mask ^ least] + int(labels[index])) % modulus
    return sums


def gf2_rank(bit_vectors: Sequence[int]) -> int:
    """Rank binary vectors represented as Python integers."""
    basis: dict[int, int] = {}
    for raw in bit_vectors:
        value = int(raw)
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def affine_hull_dimension(masks: Sequence[int]) -> int | None:
    if not masks:
        return None
    origin = int(masks[0])
    return gf2_rank([int(mask) ^ origin for mask in masks[1:]])


def _add_to_column_basis(basis: dict[int, int], vector: int) -> None:
    value = vector
    while value:
        pivot = value.bit_length() - 1
        if pivot in basis:
            value ^= basis[pivot]
        else:
            basis[pivot] = value
            return


def _in_column_span(basis: dict[int, int], vector: int) -> bool:
    value = vector
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            return False
        value ^= basis[pivot]
    return True


def minimum_boolean_degree_on_domain(
    domain_masks: Sequence[int],
    truth_values: Sequence[bool],
    variable_count: int,
    max_degree: int,
) -> tuple[int | None, int | None]:
    """Find the minimum ANF degree matching a predicate on a restricted domain.

    The computation is exact over GF(2).  A fit on a small restricted domain can
    be interpolation rather than structure, so callers separately compare the
    feature count with the domain size.
    """
    if len(domain_masks) != len(truth_values):
        raise ValueError("domain and truth values must have equal length")
    if not domain_masks:
        return None, None
    if max_degree < 0:
        raise ValueError("max_degree must be nonnegative")
    domain_size = len(domain_masks)
    all_points = (1 << domain_size) - 1
    target = 0
    variable_columns = [0] * variable_count
    for position, (mask, truth) in enumerate(zip(domain_masks, truth_values)):
        point_bit = 1 << position
        if truth:
            target |= point_bit
        active = int(mask)
        while active:
            least = active & -active
            variable_columns[least.bit_length() - 1] |= point_bit
            active ^= least

    basis: dict[int, int] = {}
    _add_to_column_basis(basis, all_points)
    feature_count = 1
    if _in_column_span(basis, target):
        return 0, feature_count
    for degree in range(1, min(max_degree, variable_count) + 1):
        for variables in itertools.combinations(range(variable_count), degree):
            column = all_points
            for variable in variables:
                column &= variable_columns[variable]
            _add_to_column_basis(basis, column)
            feature_count += 1
        if _in_column_span(basis, target):
            return degree, feature_count
    return None, None


def analyze_two_adic_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
    degree_cap: int = 3,
) -> tuple[list[TwoAdicLiftRow], TwoAdicTrialSummary]:
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
    final_masks = [mask for mask, value in enumerate(sums) if value == target]
    final_target_legal = bool(final_masks)
    rows: list[TwoAdicLiftRow] = []
    all_masks = list(range(1 << register_count))
    prior_masks = all_masks
    for lift_bit in range(1, n_bits + 1):
        bit_modulus = 1 << lift_bit
        target_residue = target & (bit_modulus - 1)
        truth = [(sums[mask] & (bit_modulus - 1)) == target_residue for mask in prior_masks]
        lifted_masks = [mask for mask, survives in zip(prior_masks, truth) if survives]
        affine_dimension = affine_hull_dimension(lifted_masks)
        lifted_log2_size = math.log2(len(lifted_masks)) if lifted_masks else None
        overcoverage = (
            float(affine_dimension) - lifted_log2_size
            if affine_dimension is not None and lifted_log2_size is not None
            else None
        )
        minimum_degree, feature_count = minimum_boolean_degree_on_domain(
            prior_masks,
            truth,
            register_count,
            degree_cap,
        )
        rows.append(
            TwoAdicLiftRow(
                n_bits=n_bits,
                register_count=register_count,
                register_offset=register_offset,
                trial_index=trial_index,
                lift_bit=lift_bit,
                prior_fiber_size=len(prior_masks),
                lifted_fiber_size=len(lifted_masks),
                conditional_survival_rate=len(lifted_masks) / len(prior_masks) if prior_masks else 0.0,
                lifted_affine_hull_dimension=affine_dimension,
                lifted_log2_size=lifted_log2_size,
                affine_hull_overcoverage_log2=overcoverage,
                minimum_exact_boolean_degree_capped=minimum_degree,
                degree_cap=degree_cap,
                feature_count_at_exact_degree=feature_count,
                degree_fit_nonvacuous=(
                    feature_count is not None and feature_count < len(prior_masks)
                ),
                final_target_legal=final_target_legal,
            )
        )
        prior_masks = lifted_masks
        if not prior_masks:
            break

    observed_degrees = [row.minimum_exact_boolean_degree_capped for row in rows]
    final_overcoverage = rows[-1].affine_hull_overcoverage_log2 if rows else None
    summary = TwoAdicTrialSummary(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        trial_index=trial_index,
        final_target_legal=final_target_legal,
        final_solution_count=len(final_masks),
        all_lifts_affine=len(rows) == n_bits and all(degree is not None and degree <= 1 for degree in observed_degrees),
        all_lifts_bounded_degree_within_cap=(
            len(rows) == n_bits and all(degree is not None for degree in observed_degrees)
        ),
        all_bounded_degree_fits_nonvacuous=(
            len(rows) == n_bits
            and all(row.degree_fit_nonvacuous for row in rows if row.minimum_exact_boolean_degree_capped is not None)
            and all(degree is not None for degree in observed_degrees)
        ),
        maximum_observed_exact_degree_capped=(
            max(int(degree) for degree in observed_degrees if degree is not None)
            if any(degree is not None for degree in observed_degrees)
            else None
        ),
        final_affine_hull_overcoverage_log2=final_overcoverage,
        exact_enumeration_log2_cost=register_count,
        polynomial_solver_constructed=False,
    )
    return rows, summary


def run_subset_sum_two_adic_search(
    n_values: Sequence[int] = (8, 10, 12),
    register_offsets: Sequence[int] = (2, 4),
    trials_per_row: int = 2,
    degree_cap: int = 3,
    seed: int = 0,
) -> DCPSubsetSumTwoAdicReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    if degree_cap < 1:
        raise ValueError("degree_cap must be positive")
    rows: list[TwoAdicLiftRow] = []
    summaries: list[TwoAdicTrialSummary] = []
    for n_index, n_bits in enumerate(n_values):
        for offset_index, register_offset in enumerate(register_offsets):
            for trial_index in range(trials_per_row):
                trial_rows, trial_summary = analyze_two_adic_trial(
                    n_bits=n_bits,
                    register_offset=register_offset,
                    trial_index=trial_index,
                    seed=seed + 1_000_003 * n_index + 10_007 * offset_index + trial_index,
                    degree_cap=degree_cap,
                )
                rows.extend(trial_rows)
                summaries.append(trial_summary)
    late_rows = [row for row in rows if row.lift_bit >= max(1, row.n_bits - 2)]
    legal_summaries = [summary for summary in summaries if summary.final_target_legal]
    overcoverage_values = [
        summary.final_affine_hull_overcoverage_log2
        for summary in legal_summaries
        if summary.final_affine_hull_overcoverage_log2 is not None
    ]
    metrics: dict[str, int | float] = {
        "trial_count": len(summaries),
        "legal_target_trial_count": len(legal_summaries),
        "lift_row_count": len(rows),
        "affine_exact_lift_count": sum(
            row.minimum_exact_boolean_degree_capped is not None
            and row.minimum_exact_boolean_degree_capped <= 1
            for row in rows
        ),
        "bounded_degree_exact_lift_count": sum(
            row.minimum_exact_boolean_degree_capped is not None for row in rows
        ),
        "degree_censored_lift_count": sum(
            row.minimum_exact_boolean_degree_capped is None for row in rows
        ),
        "nonvacuous_bounded_degree_lift_count": sum(
            row.minimum_exact_boolean_degree_capped is not None and row.degree_fit_nonvacuous
            for row in rows
        ),
        "late_lift_row_count": len(late_rows),
        "late_degree_censored_lift_count": sum(
            row.minimum_exact_boolean_degree_capped is None for row in late_rows
        ),
        "all_lifts_affine_trial_count": sum(summary.all_lifts_affine for summary in legal_summaries),
        "all_lifts_bounded_degree_trial_count": sum(
            summary.all_lifts_bounded_degree_within_cap for summary in legal_summaries
        ),
        "all_bounded_degree_fits_nonvacuous_trial_count": sum(
            summary.all_bounded_degree_fits_nonvacuous for summary in legal_summaries
        ),
        "mean_final_affine_hull_overcoverage_log2": (
            sum(overcoverage_values) / len(overcoverage_values) if overcoverage_values else 0.0
        ),
        "maximum_exact_enumeration_log2_cost": max(summary.exact_enumeration_log2_cost for summary in summaries),
        "proved_uniform_polynomial_two_adic_solver_count": 0,
        "proved_uniform_inverse_polynomial_coverage_count": 0,
        "proved_reversible_uniform_implementation_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumTwoAdicReport(
        created_at=utc_now(),
        solver_contract={
            "input": "uniform A in Z_(2^n)^(n+O(1)) and uniform target t, restricted to legal instances for coverage",
            "lifting_view": "solve <A,x>=t modulo 2, then lift the same binary witness through moduli 4,...,2^n",
            "audited_representation": "exact ANF degree of each lift predicate on the previous fiber, plus affine-hull overcoverage",
            "audit_cost": "Theta(2^(n+offset)) exact enumeration; this is an exponential structural microscope, not a candidate solver",
            "promotion_requirement": "uniform polynomial construction and solution method, inverse-polynomial legal coverage, verified witness, reversible interface",
        },
        lift_rows=rows,
        trial_summaries=summaries,
        headline_metrics=metrics,
        claim_gate={
            "power_of_two_structure_audited": True,
            "exact_lift_predicates_measured": True,
            "bounded_degree_fit_implies_polynomial_solver": False,
            "affine_hull_is_exact_fiber_representation": False,
            "uniform_polynomial_two_adic_solver_constructed": False,
            "uniform_inverse_polynomial_coverage_proved": False,
            "reversible_uniform_implementation_proved": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The audit can expose carry structure, but it enumerates every assignment. Bounded-degree predicates can be "
                "interpolation on shrinking fibers, and solving the resulting polynomial system is not known polynomial-time."
            ),
        },
        status="two-adic-carry-structure-audited-no-polynomial-solver",
        summary=(
            f"Audited {metrics['lift_row_count']} exact 2-adic lift rows across {metrics['trial_count']} random instances; "
            f"degree>{degree_cap} rows={metrics['degree_censored_lift_count']}, all-affine legal trials="
            f"{metrics['all_lifts_affine_trial_count']}, and source-contract rows=0."
        ),
        falsifiers_triggered=[
            "Exact enumeration costs 2^(n+O(1)) and is never evidence of a polynomial partial solver.",
            "An exact bounded-degree predicate on a shrinking fiber can be interpolation when feature count approaches domain size.",
            "A compact polynomial equation description does not imply that finding a satisfying binary witness is polynomial-time.",
            "Affine hulls can overcover a sparse exact fiber exponentially and therefore are not exact compressed representations.",
            "Any positive route still needs a uniform legal-coverage theorem and a reversible interface for Regev's matching routine.",
        ],
    )


def write_subset_sum_two_adic_search(
    path: Path = DCP_SUBSET_SUM_TWO_ADIC_PATH,
    n_values: Sequence[int] = (8, 10, 12),
    register_offsets: Sequence[int] = (2, 4),
    trials_per_row: int = 2,
    degree_cap: int = 3,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_two_adic_search(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=trials_per_row,
        degree_cap=degree_cap,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-TWO-ADIC-LOW-DEGREE-LIFTING-WITHOUT-SOLVER",
                source=str(path),
                claim="Low-degree or affine descriptions of finite 2-adic lift predicates establish a polynomial density-one subset-sum solver.",
                reason_invalid=(
                    "The descriptions were extracted by exponential enumeration, late fits may be interpolation on small fibers, "
                    "affine hulls overcover exact fibers, and no polynomial equation-solving or reversible coverage theorem follows."
                ),
                lesson=(
                    "Use the lift audit to identify a uniform algebraic invariant or exact compact representation. Reject mutations "
                    "that merely fit finite carry predicates without a solver and legal-input coverage proof."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "lift_row_count": payload["headline_metrics"]["lift_row_count"],
                    "degree_censored_lift_count": payload["headline_metrics"]["degree_censored_lift_count"],
                    "maximum_exact_enumeration_log2_cost": payload["headline_metrics"]["maximum_exact_enumeration_log2_cost"],
                    "source_contract_satisfying_row_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-TWO-ADIC"
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
                artifacts={"dcp_subset_sum_two_adic_search": str(path)},
            )
        )
    return payload
