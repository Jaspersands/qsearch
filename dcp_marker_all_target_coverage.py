"""Exact all-target coverage census for marker-aware nearest-plane lists.

The standard and logarithmic carry-sliced marker-zero kernels depend on public
labels but not on the target or witness carry.  If ``e_x=(1-2x,0,...)`` is the
error of a Boolean witness and ``b_i*`` are exact Gram-Schmidt rows of a fixed
reduced kernel, replaying the witness path gives

    witness_offset_i = -round(<e_x,b_i*> / ||b_i*||^2).

Thus every assignment can be classified without solving a target-specific CVP.
This module Gray-code enumerates the full Boolean cube, groups assignments by
their exact modular target, and computes exact legal-target coverage for each
fixed branch depth.  It removes target-sampling noise, but random-label scaling
remains empirical and is not an asymptotic source theorem.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from statistics import median
from typing import Sequence

from sympy import Matrix

from dcp_subset_sum_affine_cvp_baseline import exact_gram_schmidt_rows
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


DCP_MARKER_ALL_TARGET_COVERAGE_PATH = Path(
    "research/classical_baselines/dcp_marker_all_target_coverage.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-MARKER-ALL-TARGET-COVERAGE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class IntegerProjectionRow:
    integer_vector: list[int]
    common_denominator: int
    integer_norm_squared: int


@dataclass(frozen=True)
class AllTargetCoverageTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    constrained_low_bits: int
    assignment_count: int
    target_count: int
    legal_target_count: int
    mean_witness_multiplicity_over_legal_targets: float
    maximum_branch_depth: int
    standard_covered_target_count_by_depth: list[int]
    carry_covered_target_count_by_depth: list[int]
    standard_legal_coverage_by_depth: list[float]
    carry_legal_coverage_by_depth: list[float]
    standard_no_one_step_witness_target_count: int
    carry_no_one_step_witness_target_count: int
    standard_median_minimum_deviation_depth: float | None
    carry_median_minimum_deviation_depth: float | None
    target_independent_kernel_verified: bool
    full_boolean_cube_enumerated: bool


@dataclass(frozen=True)
class AllTargetCoverageScalingRow:
    n_bits: int
    register_offset: int
    trial_count: int
    exact_assignment_count: int
    exact_legal_target_count: int
    mean_standard_legal_coverage_by_depth: list[float]
    mean_carry_legal_coverage_by_depth: list[float]
    minimum_standard_max_depth_coverage: float
    maximum_standard_max_depth_coverage: float
    minimum_carry_max_depth_coverage: float
    maximum_carry_max_depth_coverage: float
    mean_standard_no_one_step_target_fraction: float
    mean_carry_no_one_step_target_fraction: float
    finite_row_is_asymptotic_coverage_theorem: bool


@dataclass(frozen=True)
class DCPMarkerAllTargetCoverageReport:
    created_at: str
    census_contract: dict[str, str]
    theorem: dict[str, bool | str]
    rows: list[AllTargetCoverageScalingRow]
    trials: list[AllTargetCoverageTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _lcm(values: Sequence[int]) -> int:
    result = 1
    for value in values:
        result = math.lcm(result, int(value))
    return result


def integer_projection_rows(basis: Matrix) -> list[IntegerProjectionRow]:
    """Scale each exact Gram-Schmidt row to a primitive integer projection."""
    rows: list[IntegerProjectionRow] = []
    for star in exact_gram_schmidt_rows(basis):
        denominator = _lcm([value.denominator for value in star])
        integers = [int(value * denominator) for value in star]
        norm = sum(value * value for value in integers)
        if norm == 0:
            raise ArithmeticError("zero Gram-Schmidt projection row")
        rows.append(
            IntegerProjectionRow(
                integer_vector=integers,
                common_denominator=denominator,
                integer_norm_squared=norm,
            )
        )
    return rows


def _nearest_integer_ratio(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    return (2 * int(numerator) + int(denominator)) // (2 * int(denominator))


def profile_from_integer_projection_dots(
    projections: Sequence[IntegerProjectionRow],
    dots: Sequence[int],
) -> tuple[int | None, int]:
    if len(projections) != len(dots):
        raise ValueError("projection and dot counts differ")
    deviations = 0
    maximum_offset = 0
    for projection, dot in zip(projections, dots):
        rounded = _nearest_integer_ratio(
            projection.common_denominator * int(dot),
            projection.integer_norm_squared,
        )
        offset = -rounded
        maximum_offset = max(maximum_offset, abs(offset))
        deviations += offset != 0
    return (deviations if maximum_offset <= 1 else None), maximum_offset


def _reduced_projection_families(
    n_bits: int,
    labels: Sequence[int],
    low_bits: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
) -> tuple[list[IntegerProjectionRow], list[IntegerProjectionRow], bool]:
    standard_zero = modular_subset_sum_embedding(
        labels, 0, 1 << n_bits, embedding_scale
    ).tolist()
    standard_one = modular_subset_sum_embedding(
        labels, 1, 1 << n_bits, embedding_scale
    ).tolist()
    standard_kernel_zero = Matrix(
        [row[:-1] for row in standard_zero[:-1]]
    )
    standard_kernel_one = Matrix(
        [row[:-1] for row in standard_one[:-1]]
    )

    carry_zero = carry_sliced_embedding(
        labels, 0, n_bits, low_bits, 0, embedding_scale, low_constraint_scale
    ).tolist()
    carry_one = carry_sliced_embedding(
        labels, 1, n_bits, low_bits, 1, embedding_scale, low_constraint_scale
    ).tolist()
    carry_kernel_zero = Matrix([row[:-1] for row in carry_zero[:-1]])
    carry_kernel_one = Matrix([row[:-1] for row in carry_one[:-1]])
    independent = (
        standard_kernel_zero == standard_kernel_one
        and carry_kernel_zero == carry_kernel_one
    )
    standard_reduced = standard_kernel_zero.lll(delta=lll_delta)
    carry_reduced = carry_kernel_zero.lll(delta=lll_delta)
    return (
        integer_projection_rows(standard_reduced),
        integer_projection_rows(carry_reduced),
        independent,
    )


def all_target_coverage_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    maximum_branch_depth: int,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    seed: int,
) -> AllTargetCoverageTrial:
    if n_bits < 2 or maximum_branch_depth < 0:
        raise ValueError("invalid census parameters")
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    standard, carry, independent = _reduced_projection_families(
        n_bits,
        labels,
        low_bits,
        embedding_scale,
        low_constraint_scale,
        lll_delta,
    )
    standard_dots = [
        sum(row.integer_vector[:register_count]) for row in standard
    ]
    carry_dots = [sum(row.integer_vector[:register_count]) for row in carry]
    unset = register_count + 1
    standard_best = [unset] * modulus
    carry_best = [unset] * modulus
    legal = [False] * modulus
    target = 0
    assignment_count = 1 << register_count
    gray = 0
    for step in range(assignment_count):
        legal[target] = True
        standard_depth, _ = profile_from_integer_projection_dots(
            standard, standard_dots
        )
        carry_depth, _ = profile_from_integer_projection_dots(carry, carry_dots)
        if standard_depth is not None and standard_depth < standard_best[target]:
            standard_best[target] = standard_depth
        if carry_depth is not None and carry_depth < carry_best[target]:
            carry_best[target] = carry_depth
        if step + 1 == assignment_count:
            continue
        next_gray = (step + 1) ^ ((step + 1) >> 1)
        changed = gray ^ next_gray
        bit = changed.bit_length() - 1
        new_bit = (next_gray >> bit) & 1
        error_delta = -2 if new_bit else 2
        target = (target + (labels[bit] if new_bit else -labels[bit])) % modulus
        for index, row in enumerate(standard):
            standard_dots[index] += error_delta * row.integer_vector[bit]
        for index, row in enumerate(carry):
            carry_dots[index] += error_delta * row.integer_vector[bit]
        gray = next_gray

    legal_targets = [index for index, value in enumerate(legal) if value]
    standard_counts = [
        sum(standard_best[target] <= depth for target in legal_targets)
        for depth in range(maximum_branch_depth + 1)
    ]
    carry_counts = [
        sum(carry_best[target] <= depth for target in legal_targets)
        for depth in range(maximum_branch_depth + 1)
    ]
    standard_depths = [
        standard_best[target]
        for target in legal_targets
        if standard_best[target] != unset
    ]
    carry_depths = [
        carry_best[target]
        for target in legal_targets
        if carry_best[target] != unset
    ]
    legal_count = len(legal_targets)
    return AllTargetCoverageTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        constrained_low_bits=low_bits,
        assignment_count=assignment_count,
        target_count=modulus,
        legal_target_count=legal_count,
        mean_witness_multiplicity_over_legal_targets=assignment_count / legal_count,
        maximum_branch_depth=maximum_branch_depth,
        standard_covered_target_count_by_depth=standard_counts,
        carry_covered_target_count_by_depth=carry_counts,
        standard_legal_coverage_by_depth=[count / legal_count for count in standard_counts],
        carry_legal_coverage_by_depth=[count / legal_count for count in carry_counts],
        standard_no_one_step_witness_target_count=legal_count - len(standard_depths),
        carry_no_one_step_witness_target_count=legal_count - len(carry_depths),
        standard_median_minimum_deviation_depth=(
            float(median(standard_depths)) if standard_depths else None
        ),
        carry_median_minimum_deviation_depth=(
            float(median(carry_depths)) if carry_depths else None
        ),
        target_independent_kernel_verified=independent,
        full_boolean_cube_enumerated=True,
    )


def run_marker_all_target_coverage(
    n_values: Sequence[int] = (14, 16, 18, 20),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 3,
    maximum_branch_depth: int = 2,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    seed: int = 0,
) -> DCPMarkerAllTargetCoverageReport:
    if trials_per_row < 1:
        raise ValueError("trials per row must be positive")
    trials = [
        all_target_coverage_trial(
            n_bits,
            offset,
            trial_index,
            maximum_branch_depth,
            log_multiplier,
            embedding_scale,
            low_constraint_scale,
            lll_delta,
            seed + 1_000_003 * ni + 10_007 * oi + trial_index,
        )
        for ni, n_bits in enumerate(n_values)
        for oi, offset in enumerate(register_offsets)
        for trial_index in range(trials_per_row)
    ]
    rows: list[AllTargetCoverageScalingRow] = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            standard_means = [
                sum(trial.standard_legal_coverage_by_depth[depth] for trial in group)
                / len(group)
                for depth in range(maximum_branch_depth + 1)
            ]
            carry_means = [
                sum(trial.carry_legal_coverage_by_depth[depth] for trial in group)
                / len(group)
                for depth in range(maximum_branch_depth + 1)
            ]
            rows.append(
                AllTargetCoverageScalingRow(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_count=len(group),
                    exact_assignment_count=sum(trial.assignment_count for trial in group),
                    exact_legal_target_count=sum(trial.legal_target_count for trial in group),
                    mean_standard_legal_coverage_by_depth=standard_means,
                    mean_carry_legal_coverage_by_depth=carry_means,
                    minimum_standard_max_depth_coverage=min(
                        trial.standard_legal_coverage_by_depth[-1] for trial in group
                    ),
                    maximum_standard_max_depth_coverage=max(
                        trial.standard_legal_coverage_by_depth[-1] for trial in group
                    ),
                    minimum_carry_max_depth_coverage=min(
                        trial.carry_legal_coverage_by_depth[-1] for trial in group
                    ),
                    maximum_carry_max_depth_coverage=max(
                        trial.carry_legal_coverage_by_depth[-1] for trial in group
                    ),
                    mean_standard_no_one_step_target_fraction=sum(
                        trial.standard_no_one_step_witness_target_count
                        / trial.legal_target_count
                        for trial in group
                    )
                    / len(group),
                    mean_carry_no_one_step_target_fraction=sum(
                        trial.carry_no_one_step_witness_target_count
                        / trial.legal_target_count
                        for trial in group
                    )
                    / len(group),
                    finite_row_is_asymptotic_coverage_theorem=False,
                )
            )
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "maximum_n_bits": tail_n,
        "maximum_branch_depth": maximum_branch_depth,
        "exact_assignment_count": sum(trial.assignment_count for trial in trials),
        "exact_legal_target_count": sum(trial.legal_target_count for trial in trials),
        "target_independent_kernel_failure_count": sum(
            not trial.target_independent_kernel_verified for trial in trials
        ),
        "full_boolean_cube_failure_count": sum(
            not trial.full_boolean_cube_enumerated for trial in trials
        ),
        "target_independent_rounding_identity_theorem_count": 1,
        "exact_all_target_coverage_census_count": len(trials),
        "tail_mean_standard_max_depth_coverage": sum(
            row.mean_standard_legal_coverage_by_depth[-1] for row in tail
        )
        / len(tail),
        "tail_mean_carry_max_depth_coverage": sum(
            row.mean_carry_legal_coverage_by_depth[-1] for row in tail
        )
        / len(tail),
        "tail_mean_standard_no_one_step_target_fraction": sum(
            row.mean_standard_no_one_step_target_fraction for row in tail
        )
        / len(tail),
        "tail_mean_carry_no_one_step_target_fraction": sum(
            row.mean_carry_no_one_step_target_fraction for row in tail
        )
        / len(tail),
        "proved_asymptotic_fixed_depth_coverage_bound_count": 0,
        "polynomial_marker_aware_decoder_count": 0,
    }
    return DCPMarkerAllTargetCoverageReport(
        created_at=utc_now(),
        census_contract={
            "labels": "independent uniform public labels for each census row",
            "targets": "every target modulo 2^n, with exact legal-target conditioning",
            "assignments": "the entire Boolean cube in Gray-code order",
            "geometry": "exact integer-scaled Gram-Schmidt projections of target-independent reduced kernels",
            "coverage": "a target is covered iff at least one of all its witnesses lies in the fixed-depth one-step tree",
        },
        theorem={
            "target_independent_kernel": True,
            "witness_offset_identity": "offset_i=-round(<1-2x,b_i*>/||b_i*||^2)",
            "all_target_census_exact_for_each_label_row": True,
            "random_label_scaling_theorem": False,
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "target_sampling_noise_eliminated": True,
            "all_legal_targets_exact_for_each_label_row": True,
            "random_label_scaling_is_asymptotic_theorem": False,
            "fixed_depth_source_coverage_bound_proved": False,
            "general_affine_cvp_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Each finite label row has exact all-target coverage. Extrapolation over random labels and growing n "
                "still requires a theorem and says nothing about other affine decoders."
            ),
        },
        status="exact-all-target-fixed-depth-coverage-census-asymptotic-label-law-open",
        summary=(
            f"Enumerated {metrics['exact_assignment_count']} assignments and {metrics['exact_legal_target_count']} legal "
            f"targets across {len(trials)} label rows through n={tail_n}; tail depth-{maximum_branch_depth} standard/carry "
            f"coverage={metrics['tail_mean_standard_max_depth_coverage']:.6g}/"
            f"{metrics['tail_mean_carry_max_depth_coverage']:.6g}; no random-label scaling theorem."
        ),
        falsifiers_triggered=[
            "Every target and every witness assignment is included for each sampled label row.",
            "Target independence of both kernel matrices is checked directly.",
            "Exact rational Gram-Schmidt rows are converted to equivalent integer projection tests.",
            "A target counts as solved only when at least one actual witness satisfies the branch grammar.",
            "Finite exact coverage over targets is not promoted to an asymptotic law over random labels.",
        ],
    )


def write_marker_all_target_coverage(
    path: Path = DCP_MARKER_ALL_TARGET_COVERAGE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict:
    payload = asdict(run_marker_all_target_coverage(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-FINITE-ALL-TARGET-COVERAGE-IS-NOT-RANDOM-LABEL-THEOREM",
                source=str(path),
                claim=(
                    "Exact fixed-depth coverage over every target for finitely many label sets proves an asymptotic "
                    "coverage law or lower bound under random labels."
                ),
                reason_invalid=(
                    "Target sampling is eliminated, but the remaining label-dependent LLL geometry is sampled at "
                    "finite n and has no concentration theorem."
                ),
                lesson=(
                    "Use the census to identify the right label statistic, then prove its source law or abandon the "
                    "fixed-depth branching mechanism."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id or f"RESULT-{registry_experiment_id}-LATEST",
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_marker_all_target_coverage": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(json.dumps(write_marker_all_target_coverage()["headline_metrics"], indent=2, sort_keys=True))
