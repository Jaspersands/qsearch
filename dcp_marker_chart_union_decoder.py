"""Polynomial unions of learned logarithmic marker-decoding charts.

A single public ``O(log n)`` coordinate chart can miss deviations that move
among many LLL Gram-Schmidt coordinates.  This module learns up to ``n^a``
target-independent charts from random public sign probes.  Every chart has
``c ceil(log2 n)`` coordinates and branches by a fixed offset radius, so the
complete union remains polynomial:

    n^a (2q+1) ** (c ceil(log2 n)).

Training probes depend only on public labels and fresh classical randomness.
Evaluation uses disjoint probes, and small instances additionally enumerate
the entire Boolean cube and every legal target.  A finite collapse closes only
this chart learner and parameter family; it is not an affine-CVP lower bound.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_marker_all_target_coverage import (
    IntegerProjectionRow,
    _reduced_projection_families,
)
from dcp_marker_vulnerable_coordinate_decoder import (
    exact_selected_nearest_plane_list,
    projection_offsets,
    select_vulnerable_coordinates,
    target_coverage_transfer_bounds,
    vulnerable_coordinate_count,
)
from dcp_subset_sum_carry_slice_lattice import constrained_low_bits
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_MARKER_CHART_UNION_PATH = Path(
    "research/classical_baselines/dcp_marker_chart_union_decoder.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-MARKER-CHART-UNION-DECODER"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ChartLearningResult:
    supports: list[int]
    selected_coordinate_count: int
    chart_budget: int
    eligible_training_mask_count: int
    unique_training_mask_count: int
    unique_padded_support_count: int
    training_coverage: float
    training_oracle_representable_fraction: float


@dataclass(frozen=True)
class MarkerChartTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    selector_multiplier: int
    chart_budget_power: int
    maximum_offset: int
    training_sample_count: int
    heldout_sample_count: int
    standard_chart_count: int
    carry_chart_count: int
    standard_unique_training_mask_count: int
    carry_unique_training_mask_count: int
    standard_training_coverage: float
    carry_training_coverage: float
    standard_heldout_coverage: float
    carry_heldout_coverage: float
    standard_heldout_single_risk_chart_coverage: float
    carry_heldout_single_risk_chart_coverage: float
    standard_heldout_oracle_representable_fraction: float
    carry_heldout_oracle_representable_fraction: float
    standard_generalization_gap: float
    carry_generalization_gap: float
    candidate_count_upper_bound: int
    exact_full_cube_enumerated: bool
    exact_assignment_count: int
    exact_legal_target_count: int
    standard_exact_uniform_legal_target_coverage: float | None
    carry_exact_uniform_legal_target_coverage: float | None
    standard_transfer_sandwich_verified: bool | None
    carry_transfer_sandwich_verified: bool | None
    training_and_heldout_sources_disjoint: bool
    selector_is_target_independent: bool


@dataclass(frozen=True)
class MarkerChartScalingRow:
    n_bits: int
    register_offset: int
    trial_count: int
    mean_standard_heldout_coverage: float
    mean_carry_heldout_coverage: float
    minimum_carry_heldout_coverage: float
    maximum_carry_heldout_coverage: float
    mean_standard_single_chart_coverage: float
    mean_carry_single_chart_coverage: float
    mean_standard_oracle_representable_fraction: float
    mean_carry_oracle_representable_fraction: float
    mean_standard_generalization_gap: float
    mean_carry_generalization_gap: float
    maximum_chart_count: int
    maximum_candidate_count_upper_bound: int
    exact_trial_count: int
    mean_standard_exact_uniform_legal_target_coverage: float | None
    mean_carry_exact_uniform_legal_target_coverage: float | None
    finite_row_is_asymptotic_source_law: bool


@dataclass(frozen=True)
class DCPMarkerChartUnionReport:
    created_at: str
    decoder_contract: dict[str, str]
    polynomial_bound: dict[str, str | bool]
    rows: list[MarkerChartScalingRow]
    trials: list[MarkerChartTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def chart_union_candidate_upper_bound(
    n_bits: int,
    selector_multiplier: int,
    rank: int,
    maximum_offset: int,
    chart_budget_power: int,
    carry_factor: int = 1,
) -> int:
    if chart_budget_power < 0 or carry_factor < 1:
        raise ValueError("invalid chart budget or carry factor")
    selected = vulnerable_coordinate_count(
        n_bits, selector_multiplier, rank
    )
    return (
        (n_bits**chart_budget_power)
        * (2 * maximum_offset + 1) ** selected
        * carry_factor
    )


def _active_mask(
    projections: Sequence[IntegerProjectionRow],
    signs: Sequence[int],
    maximum_offset: int,
) -> int | None:
    dots = [
        sum(
            coefficient * sign
            for coefficient, sign in zip(
                projection.integer_vector[: len(signs)], signs
            )
        )
        for projection in projections
    ]
    offsets = projection_offsets(projections, dots)
    if max((abs(offset) for offset in offsets), default=0) > maximum_offset:
        return None
    mask = 0
    for index, offset in enumerate(offsets):
        if offset:
            mask |= 1 << index
    return mask


def _sample_masks(
    projections: Sequence[IntegerProjectionRow],
    register_count: int,
    sample_count: int,
    maximum_offset: int,
    rng: random.Random,
) -> list[int | None]:
    return [
        _active_mask(
            projections,
            [
                1 if rng.getrandbits(1) == 0 else -1
                for _ in range(register_count)
            ],
            maximum_offset,
        )
        for _ in range(sample_count)
    ]


def chart_union_accepts(mask: int | None, supports: Sequence[int]) -> bool:
    return mask is not None and any((mask & ~support) == 0 for support in supports)


def chart_union_coverage(
    masks: Sequence[int | None],
    supports: Sequence[int],
) -> float:
    if not masks:
        raise ValueError("coverage requires at least one mask")
    return sum(chart_union_accepts(mask, supports) for mask in masks) / len(masks)


def learn_coordinate_charts(
    projections: Sequence[IntegerProjectionRow],
    n_bits: int,
    selector_multiplier: int,
    chart_budget_power: int,
    register_count: int,
    training_masks: Sequence[int | None],
) -> ChartLearningResult:
    selected_count = vulnerable_coordinate_count(
        n_bits, selector_multiplier, len(projections)
    )
    chart_budget = n_bits**chart_budget_power
    eligible = [
        mask
        for mask in training_masks
        if mask is not None and mask.bit_count() <= selected_count
    ]
    counts = Counter(eligible)
    marginal = [0] * len(projections)
    for mask, multiplicity in counts.items():
        for index in range(len(projections)):
            if (mask >> index) & 1:
                marginal[index] += multiplicity
    ranking = sorted(
        range(len(projections)),
        key=lambda index: (-marginal[index], index),
    )
    padded: set[int] = set()
    for mask in counts:
        support = mask
        for index in ranking:
            if support.bit_count() >= selected_count:
                break
            support |= 1 << index
        padded.add(support)
    risk_support = sum(
        1 << index
        for index in select_vulnerable_coordinates(
            projections,
            n_bits,
            selector_multiplier,
            register_count,
        )
    )
    padded.add(risk_support)
    def support_score(support: int) -> int:
        score = 0
        subset = support
        while True:
            score += counts.get(subset, 0)
            if subset == 0:
                return score
            subset = (subset - 1) & support

    scored = sorted(
        (
            (
                support_score(support),
                support,
            )
            for support in padded
        ),
        key=lambda item: (-item[0], item[1]),
    )
    supports = [support for _, support in scored[:chart_budget]]
    return ChartLearningResult(
        supports=supports,
        selected_coordinate_count=selected_count,
        chart_budget=chart_budget,
        eligible_training_mask_count=len(eligible),
        unique_training_mask_count=len(counts),
        unique_padded_support_count=len(padded),
        training_coverage=chart_union_coverage(training_masks, supports),
        training_oracle_representable_fraction=len(eligible)
        / len(training_masks),
    )


def exact_chart_union_nearest_plane_list(
    basis,
    target: Sequence[int],
    support_masks: Sequence[int],
    maximum_offset: int,
):
    """Materialize and deduplicate a chart union for small executable controls."""
    by_coefficients = {}
    for support in support_masks:
        selected = [
            index for index in range(basis.rows) if (support >> index) & 1
        ]
        for candidate in exact_selected_nearest_plane_list(
            basis, target, selected, maximum_offset
        ):
            by_coefficients[tuple(candidate.coefficients)] = candidate
    return sorted(
        by_coefficients.values(),
        key=lambda candidate: (
            candidate.distance_squared,
            candidate.deviation_count,
            tuple(candidate.coefficients),
        ),
    )


def _exact_target_census(
    labels: Sequence[int],
    modulus: int,
    standard: Sequence[IntegerProjectionRow],
    carry: Sequence[IntegerProjectionRow],
    standard_supports: Sequence[int],
    carry_supports: Sequence[int],
    maximum_offset: int,
) -> dict[str, int | float | bool]:
    register_count = len(labels)
    assignment_count = 1 << register_count
    standard_dots = [
        sum(row.integer_vector[:register_count]) for row in standard
    ]
    carry_dots = [
        sum(row.integer_vector[:register_count]) for row in carry
    ]
    legal = bytearray(modulus)
    standard_covered = bytearray(modulus)
    carry_covered = bytearray(modulus)
    standard_good_count = 0
    carry_good_count = 0
    target = 0
    gray = 0
    for step in range(assignment_count):
        legal[target] = 1
        standard_offsets = projection_offsets(standard, standard_dots)
        carry_offsets = projection_offsets(carry, carry_dots)
        standard_mask = (
            None
            if max(map(abs, standard_offsets), default=0) > maximum_offset
            else sum(
                1 << index
                for index, offset in enumerate(standard_offsets)
                if offset
            )
        )
        carry_mask = (
            None
            if max(map(abs, carry_offsets), default=0) > maximum_offset
            else sum(
                1 << index
                for index, offset in enumerate(carry_offsets)
                if offset
            )
        )
        standard_good = chart_union_accepts(
            standard_mask, standard_supports
        )
        carry_good = chart_union_accepts(carry_mask, carry_supports)
        standard_good_count += standard_good
        carry_good_count += carry_good
        if standard_good:
            standard_covered[target] = 1
        if carry_good:
            carry_covered[target] = 1
        if step + 1 == assignment_count:
            continue
        next_gray = (step + 1) ^ ((step + 1) >> 1)
        changed = gray ^ next_gray
        bit = changed.bit_length() - 1
        new_bit = (next_gray >> bit) & 1
        error_delta = -2 if new_bit else 2
        target = (
            target + (labels[bit] if new_bit else -labels[bit])
        ) % modulus
        for index, row in enumerate(standard):
            standard_dots[index] += error_delta * row.integer_vector[bit]
        for index, row in enumerate(carry):
            carry_dots[index] += error_delta * row.integer_vector[bit]
        gray = next_gray
    legal_count = sum(legal)
    mean_multiplicity = assignment_count / legal_count
    standard_assignment = standard_good_count / assignment_count
    carry_assignment = carry_good_count / assignment_count
    standard_target = sum(standard_covered) / legal_count
    carry_target = sum(carry_covered) / legal_count
    standard_bounds = target_coverage_transfer_bounds(
        standard_assignment, mean_multiplicity
    )
    carry_bounds = target_coverage_transfer_bounds(
        carry_assignment, mean_multiplicity
    )
    tolerance = 1e-15
    return {
        "assignment_count": assignment_count,
        "legal_target_count": legal_count,
        "standard_target": standard_target,
        "carry_target": carry_target,
        "standard_verified": (
            standard_bounds[0] - tolerance
            <= standard_target
            <= standard_bounds[1] + tolerance
        ),
        "carry_verified": (
            carry_bounds[0] - tolerance
            <= carry_target
            <= carry_bounds[1] + tolerance
        ),
    }


def run_marker_chart_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    selector_multiplier: int,
    chart_budget_power: int,
    maximum_offset: int,
    training_sample_count: int,
    heldout_sample_count: int,
    exact_full_cube: bool,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    seed: int,
) -> MarkerChartTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    standard, carry, independent = _reduced_projection_families(
        n_bits,
        labels,
        constrained_low_bits(n_bits, log_multiplier),
        embedding_scale,
        low_constraint_scale,
        lll_delta,
    )
    if not independent:
        raise AssertionError("marker-zero kernels unexpectedly depend on target")
    standard_training = _sample_masks(
        standard,
        register_count,
        training_sample_count,
        maximum_offset,
        rng,
    )
    carry_training = _sample_masks(
        carry,
        register_count,
        training_sample_count,
        maximum_offset,
        rng,
    )
    standard_learning = learn_coordinate_charts(
        standard,
        n_bits,
        selector_multiplier,
        chart_budget_power,
        register_count,
        standard_training,
    )
    carry_learning = learn_coordinate_charts(
        carry,
        n_bits,
        selector_multiplier,
        chart_budget_power,
        register_count,
        carry_training,
    )
    standard_heldout = _sample_masks(
        standard,
        register_count,
        heldout_sample_count,
        maximum_offset,
        rng,
    )
    carry_heldout = _sample_masks(
        carry,
        register_count,
        heldout_sample_count,
        maximum_offset,
        rng,
    )
    standard_coverage = chart_union_coverage(
        standard_heldout, standard_learning.supports
    )
    carry_coverage = chart_union_coverage(
        carry_heldout, carry_learning.supports
    )
    standard_risk = sum(
        1 << index
        for index in select_vulnerable_coordinates(
            standard, n_bits, selector_multiplier, register_count
        )
    )
    carry_risk = sum(
        1 << index
        for index in select_vulnerable_coordinates(
            carry, n_bits, selector_multiplier, register_count
        )
    )
    selected_count = standard_learning.selected_coordinate_count
    standard_oracle = sum(
        mask is not None and mask.bit_count() <= selected_count
        for mask in standard_heldout
    ) / heldout_sample_count
    carry_oracle = sum(
        mask is not None and mask.bit_count() <= selected_count
        for mask in carry_heldout
    ) / heldout_sample_count
    exact = (
        _exact_target_census(
            labels,
            modulus,
            standard,
            carry,
            standard_learning.supports,
            carry_learning.supports,
            maximum_offset,
        )
        if exact_full_cube
        else None
    )
    candidate_upper = max(
        chart_union_candidate_upper_bound(
            n_bits,
            selector_multiplier,
            len(standard),
            maximum_offset,
            chart_budget_power,
        ),
        chart_union_candidate_upper_bound(
            n_bits,
            selector_multiplier,
            len(carry),
            maximum_offset,
            chart_budget_power,
            carry_factor=register_count + 1,
        ),
    )
    return MarkerChartTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        selector_multiplier=selector_multiplier,
        chart_budget_power=chart_budget_power,
        maximum_offset=maximum_offset,
        training_sample_count=training_sample_count,
        heldout_sample_count=heldout_sample_count,
        standard_chart_count=len(standard_learning.supports),
        carry_chart_count=len(carry_learning.supports),
        standard_unique_training_mask_count=(
            standard_learning.unique_training_mask_count
        ),
        carry_unique_training_mask_count=(
            carry_learning.unique_training_mask_count
        ),
        standard_training_coverage=standard_learning.training_coverage,
        carry_training_coverage=carry_learning.training_coverage,
        standard_heldout_coverage=standard_coverage,
        carry_heldout_coverage=carry_coverage,
        standard_heldout_single_risk_chart_coverage=chart_union_coverage(
            standard_heldout, [standard_risk]
        ),
        carry_heldout_single_risk_chart_coverage=chart_union_coverage(
            carry_heldout, [carry_risk]
        ),
        standard_heldout_oracle_representable_fraction=standard_oracle,
        carry_heldout_oracle_representable_fraction=carry_oracle,
        standard_generalization_gap=(
            standard_learning.training_coverage - standard_coverage
        ),
        carry_generalization_gap=(
            carry_learning.training_coverage - carry_coverage
        ),
        candidate_count_upper_bound=candidate_upper,
        exact_full_cube_enumerated=exact is not None,
        exact_assignment_count=(
            int(exact["assignment_count"]) if exact is not None else 0
        ),
        exact_legal_target_count=(
            int(exact["legal_target_count"]) if exact is not None else 0
        ),
        standard_exact_uniform_legal_target_coverage=(
            float(exact["standard_target"]) if exact is not None else None
        ),
        carry_exact_uniform_legal_target_coverage=(
            float(exact["carry_target"]) if exact is not None else None
        ),
        standard_transfer_sandwich_verified=(
            bool(exact["standard_verified"]) if exact is not None else None
        ),
        carry_transfer_sandwich_verified=(
            bool(exact["carry_verified"]) if exact is not None else None
        ),
        training_and_heldout_sources_disjoint=True,
        selector_is_target_independent=True,
    )


def _slope(rows: Sequence[MarkerChartScalingRow], carry: bool) -> float:
    values = [
        (
            row.n_bits,
            row.mean_carry_heldout_coverage
            if carry
            else row.mean_standard_heldout_coverage,
        )
        for row in rows
    ]
    positive = [(n, value) for n, value in values if value > 0.0]
    if len(positive) < 2:
        return 0.0
    mean_n = sum(n for n, _ in positive) / len(positive)
    logs = [math.log2(value) for _, value in positive]
    mean_log = sum(logs) / len(logs)
    denominator = sum((n - mean_n) ** 2 for n, _ in positive)
    return (
        sum(
            (n - mean_n) * (log_value - mean_log)
            for (n, _), log_value in zip(positive, logs)
        )
        / denominator
        if denominator
        else 0.0
    )


def run_marker_chart_union_decoder(
    n_values: Sequence[int] = (14, 24, 30, 36, 42, 48, 56, 64),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 2,
    selector_multiplier: int = 2,
    chart_budget_power: int = 2,
    maximum_offset: int = 1,
    training_sample_count: int = 0,
    heldout_sample_count: int = 0,
    training_samples_per_n_squared: int = 16,
    heldout_samples_per_n_squared: int = 8,
    exact_target_max_n: int = 14,
    exact_trials_per_row: int = 1,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    seed: int = 0,
) -> DCPMarkerChartUnionReport:
    if not n_values or not register_offsets or trials_per_row < 1:
        raise ValueError("nonempty ranges and positive trials are required")
    if exact_trials_per_row < 0 or exact_trials_per_row > trials_per_row:
        raise ValueError("invalid exact trial count")
    if (
        training_sample_count < 0
        or heldout_sample_count < 0
        or training_samples_per_n_squared < 0
        or heldout_samples_per_n_squared < 0
    ):
        raise ValueError("sample budgets must be nonnegative")
    trials = [
        run_marker_chart_trial(
            n_bits,
            offset,
            trial_index,
            selector_multiplier,
            chart_budget_power,
            maximum_offset,
            max(
                training_sample_count,
                training_samples_per_n_squared * n_bits * n_bits,
                1,
            ),
            max(
                heldout_sample_count,
                heldout_samples_per_n_squared * n_bits * n_bits,
                1,
            ),
            n_bits <= exact_target_max_n
            and trial_index < exact_trials_per_row,
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
    rows = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            exact_group = [
                trial for trial in group if trial.exact_full_cube_enumerated
            ]
            rows.append(
                MarkerChartScalingRow(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_count=len(group),
                    mean_standard_heldout_coverage=sum(
                        trial.standard_heldout_coverage for trial in group
                    )
                    / len(group),
                    mean_carry_heldout_coverage=sum(
                        trial.carry_heldout_coverage for trial in group
                    )
                    / len(group),
                    minimum_carry_heldout_coverage=min(
                        trial.carry_heldout_coverage for trial in group
                    ),
                    maximum_carry_heldout_coverage=max(
                        trial.carry_heldout_coverage for trial in group
                    ),
                    mean_standard_single_chart_coverage=sum(
                        trial.standard_heldout_single_risk_chart_coverage
                        for trial in group
                    )
                    / len(group),
                    mean_carry_single_chart_coverage=sum(
                        trial.carry_heldout_single_risk_chart_coverage
                        for trial in group
                    )
                    / len(group),
                    mean_standard_oracle_representable_fraction=sum(
                        trial.standard_heldout_oracle_representable_fraction
                        for trial in group
                    )
                    / len(group),
                    mean_carry_oracle_representable_fraction=sum(
                        trial.carry_heldout_oracle_representable_fraction
                        for trial in group
                    )
                    / len(group),
                    mean_standard_generalization_gap=sum(
                        trial.standard_generalization_gap for trial in group
                    )
                    / len(group),
                    mean_carry_generalization_gap=sum(
                        trial.carry_generalization_gap for trial in group
                    )
                    / len(group),
                    maximum_chart_count=max(
                        max(trial.standard_chart_count, trial.carry_chart_count)
                        for trial in group
                    ),
                    maximum_candidate_count_upper_bound=max(
                        trial.candidate_count_upper_bound for trial in group
                    ),
                    exact_trial_count=len(exact_group),
                    mean_standard_exact_uniform_legal_target_coverage=(
                        sum(
                            float(
                                trial.standard_exact_uniform_legal_target_coverage
                            )
                            for trial in exact_group
                        )
                        / len(exact_group)
                        if exact_group
                        else None
                    ),
                    mean_carry_exact_uniform_legal_target_coverage=(
                        sum(
                            float(
                                trial.carry_exact_uniform_legal_target_coverage
                            )
                            for trial in exact_group
                        )
                        / len(exact_group)
                        if exact_group
                        else None
                    ),
                    finite_row_is_asymptotic_source_law=False,
                )
            )
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    tail_carry = sum(row.mean_carry_heldout_coverage for row in tail) / len(tail)
    tail_max = max(row.maximum_carry_heldout_coverage for row in tail)
    standard_slope = _slope(rows, carry=False)
    carry_slope = _slope(rows, carry=True)
    finite_collapse = int(carry_slope < -0.05 and tail_max < 0.01)
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "maximum_n_bits": tail_n,
        "selector_multiplier": selector_multiplier,
        "chart_budget_power": chart_budget_power,
        "training_samples_per_n_squared": training_samples_per_n_squared,
        "heldout_samples_per_n_squared": heldout_samples_per_n_squared,
        "training_sample_count": sum(
            trial.training_sample_count for trial in trials
        ),
        "heldout_sample_count": sum(
            trial.heldout_sample_count for trial in trials
        ),
        "maximum_chart_count": max(
            max(trial.standard_chart_count, trial.carry_chart_count)
            for trial in trials
        ),
        "maximum_candidate_count_upper_bound": max(
            trial.candidate_count_upper_bound for trial in trials
        ),
        "polynomial_chart_union_theorem_count": 1,
        "target_independent_selector_failure_count": sum(
            not trial.selector_is_target_independent for trial in trials
        ),
        "disjoint_train_test_failure_count": sum(
            not trial.training_and_heldout_sources_disjoint for trial in trials
        ),
        "exact_full_cube_trial_count": sum(
            trial.exact_full_cube_enumerated for trial in trials
        ),
        "exact_assignment_count": sum(
            trial.exact_assignment_count for trial in trials
        ),
        "exact_legal_target_count": sum(
            trial.exact_legal_target_count for trial in trials
        ),
        "transfer_sandwich_failure_count": sum(
            trial.standard_transfer_sandwich_verified is False
            or trial.carry_transfer_sandwich_verified is False
            for trial in trials
        ),
        "tail_carry_heldout_coverage": tail_carry,
        "tail_maximum_carry_heldout_coverage": tail_max,
        "standard_log2_heldout_coverage_slope_per_n": standard_slope,
        "carry_log2_heldout_coverage_slope_per_n": carry_slope,
        "finite_tail_collapse_observed_count": finite_collapse,
        "proved_inverse_polynomial_uniform_legal_coverage_count": 0,
        "proved_exponential_chart_union_decay_count": 0,
        "polynomial_marker_aware_decoder_count": 0,
    }
    falsifiers = (
        [
            (
                f"The preregistered n^{chart_budget_power}-chart carry union has "
                f"held-out coverage {tail_carry:.6g} at n={tail_n} with maximum "
                f"label-row coverage {tail_max:.6g} and log2 slope {carry_slope:.6g}."
            )
        ]
        if finite_collapse
        else []
    )
    return DCPMarkerChartUnionReport(
        created_at=utc_now(),
        decoder_contract={
            "input": (
                "independent uniform DCP labels and an independent uniform target "
                "conditioned on a Boolean subset-sum witness"
            ),
            "training": (
                "fresh target-independent random sign probes; no target, planted "
                "witness, or held-out assignment enters chart selection; default "
                "sample budgets scale quadratically with n"
            ),
            "chart": (
                f"at most {selector_multiplier} ceil(log2 n) public coordinates "
                f"with offsets in [-{maximum_offset},{maximum_offset}]"
            ),
            "union": (
                f"at most n^{chart_budget_power} learned padded active-mask charts"
            ),
            "evaluation": (
                "disjoint held-out sign probes and complete small-n uniform-legal "
                "target censuses"
            ),
        },
        polynomial_bound={
            "statement": (
                "For fixed a,c,q, n^a charts with c ceil(log2 n) coordinates "
                "and radius q contain at most n^a(2q+1)^(c ceil(log2 n)) paths."
            ),
            "carry_factor": "at most n+O(1) reachable low-bit carries",
            "training_runtime": (
                "polynomial in n, training sample count, chart candidates, and chart budget"
            ),
            "proved": True,
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "candidate_union_polynomial": True,
            "training_target_independent": True,
            "heldout_evaluation_disjoint": True,
            "uniform_legal_targets_checked_exactly_at_finite_n": (
                metrics["exact_full_cube_trial_count"] > 0
            ),
            "inverse_polynomial_uniform_legal_coverage_proved": False,
            "finite_collapse_is_general_affine_cvp_lower_bound": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The chart union is an explicit polynomial classical attack, but "
                "finite held-out decay is neither an asymptotic theorem nor a lower "
                "bound against other affine or quantum decoders."
            ),
        },
        status=(
            "polynomial-chart-union-finite-tail-collapse-source-law-open"
            if finite_collapse
            else "polynomial-chart-union-finite-signal-source-law-open"
        ),
        summary=(
            f"Tested n^{chart_budget_power} learned logarithmic marker-chart unions "
            f"through n={tail_n}; tail carry held-out coverage={tail_carry:.6g}, "
            f"log2 slope={carry_slope:.6g}. Polynomiality is proved; the random-label "
            "coverage law remains open."
        ),
        falsifiers_triggered=falsifiers,
    )


def _register(
    payload: dict[str, object],
    path: Path,
    experiment_id: str,
    candidate_id: str,
    result_id: str | None,
) -> None:
    metrics = payload["headline_metrics"]
    if not isinstance(metrics, dict):
        raise ValueError("chart-union artifact lacks metrics")
    if int(metrics["finite_tail_collapse_observed_count"]) > 0:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-MARKER-POLYNOMIAL-CHART-UNION-FINITE-DECAY",
                source=str(path),
                claim=(
                    "A polynomial union of learned logarithmic LLL-coordinate charts "
                    "already has evidence of inverse-polynomial source coverage."
                ),
                reason_invalid=(
                    "Disjoint held-out coverage decays in the preregistered scaling "
                    "sweep, and no random-label concentration theorem is supplied."
                ),
                lesson=(
                    "Prove a different chart distribution or move beyond coordinate-cell "
                    "unions; do not tune on held-out labels or call finite decay a lower bound."
                ),
                applies_to=[candidate_id, experiment_id],
                evidence=metrics,
            )
        )
    upsert_experiment_result(
        ExperimentResultRecord(
            id=result_id or f"RESULT-{experiment_id}-LATEST",
            experiment_id=experiment_id,
            candidate_id=candidate_id,
            created_at=str(payload["created_at"]),
            status=str(payload["status"]),
            summary=str(payload["summary"]),
            metrics=metrics,
            falsifiers_triggered=list(payload["falsifiers_triggered"]),
            artifacts={"dcp_marker_chart_union_decoder": str(path)},
        )
    )


def write_marker_chart_union_decoder(
    path: Path = DCP_MARKER_CHART_UNION_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict[str, object]:
    payload = asdict(run_marker_chart_union_decoder(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _register(
            payload,
            path,
            registry_experiment_id,
            registry_candidate_id,
            registry_result_id,
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_marker_chart_union_decoder()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
