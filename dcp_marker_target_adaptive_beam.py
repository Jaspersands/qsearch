"""Target-adaptive polynomial beam search for marker-aware subset sum.

Public coordinate charts are not the strongest legal nearest-plane baseline.
The target is part of Regev's random subset-sum instance, so a classical
algorithm may use it while deciding which partial lattice paths to retain.
This module implements a K-best nearest-plane beam:

* every nearest-integer decision is exact;
* each retained path branches by a fixed offset radius;
* only ``n**a`` paths survive each level;
* every returned marker-minus-one vector is decoded and verified exactly.

For fixed ``a`` and offset radius, the standard search expands at most

    rank * (2q + 1) * n**a

states.  Carry slicing adds the explicitly charged number of reachable carries,
which is polynomial for ``O(log n)`` exposed low bits.

The experiment samples independent uniform labels and targets.  It does not
plant a witness.  Finite success or failure is not an asymptotic source law.
"""

from __future__ import annotations

import heapq
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from sympy import Matrix

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from dcp_marker_all_target_coverage import (
    IntegerProjectionRow,
    _nearest_integer_ratio,
    integer_projection_rows,
)
from dcp_subset_sum_carry_slice_lattice import (
    carry_sliced_embedding,
    constrained_low_bits,
    decode_carry_sliced_vector,
    reachable_carries,
)
from dcp_subset_sum_lattice_search import modular_subset_sum_embedding
from dcp_subset_sum_marker_coset_theorem import (
    decode_short_standard_marker_vector,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH = Path(
    "research/classical_baselines/dcp_marker_target_adaptive_beam.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-MARKER-TARGET-ADAPTIVE-BEAM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class BeamModel:
    reduced_rows: tuple[tuple[int, ...], ...]
    projections: tuple[IntegerProjectionRow, ...]


@dataclass(frozen=True)
class BeamSearchOutcome:
    solved: bool
    valid_witness_count: int
    invalid_marker_candidate_count: int
    beam_width: int
    maximum_offset: int
    rank: int
    branch_factor: int
    expanded_state_count: int
    expansion_upper_bound: int
    peak_retained_state_count: int
    final_state_count: int
    exact_nearest_integer_decisions: bool
    floating_priority_only: bool
    state_bound_verified: bool
    reachable_carry_count: int
    winning_carry: int | None


@dataclass(frozen=True)
class TargetAdaptiveBeamTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    decoder_variant: str
    width_power: int
    beam_width: int
    maximum_offset: int
    target_sampled_independently_uniform: bool
    target_legality_exactly_known: bool
    target_legal: bool | None
    solved: bool
    valid_witness_count: int
    invalid_marker_candidate_count: int
    expanded_state_count: int
    expansion_upper_bound: int
    peak_retained_state_count: int
    final_state_count: int
    reachable_carry_count: int
    winning_carry: int | None
    exact_nearest_integer_decisions: bool
    floating_priority_only: bool
    state_bound_verified: bool


@dataclass(frozen=True)
class TargetAdaptiveBeamScalingRow:
    n_bits: int
    register_offset: int
    decoder_variant: str
    width_power: int
    beam_width: int
    trial_count: int
    exact_legality_trial_count: int
    exact_legal_trial_count: int
    success_count: int
    unconditional_uniform_source_success_rate: float
    uniform_source_success_wilson_95_lower: float
    uniform_source_success_wilson_95_upper: float
    exact_legal_coverage: float | None
    invalid_marker_candidate_count: int
    total_expanded_state_count: int
    maximum_expansion_upper_bound: int
    state_bound_failure_count: int
    finite_row_is_inverse_polynomial_source_theorem: bool


@dataclass(frozen=True)
class DCPMarkerTargetAdaptiveBeamReport:
    created_at: str
    decoder_contract: dict[str, str]
    polynomial_bound: dict[str, str | bool]
    rows: list[TargetAdaptiveBeamScalingRow]
    trials: list[TargetAdaptiveBeamTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def polynomial_beam_width(n_bits: int, width_power: int) -> int:
    if n_bits < 2 or width_power < 0:
        raise ValueError("requires n_bits>=2 and a nonnegative width power")
    return n_bits**width_power


def beam_expansion_upper_bound(
    rank: int,
    beam_width: int,
    maximum_offset: int,
    outer_factor: int = 1,
) -> int:
    if min(rank, beam_width, outer_factor) < 1 or maximum_offset < 0:
        raise ValueError("invalid beam-bound parameters")
    return (
        outer_factor
        * rank
        * beam_width
        * (2 * maximum_offset + 1)
    )


def _prepare_model(kernel: Matrix, lll_delta: float) -> BeamModel:
    reduced = kernel.lll(delta=lll_delta)
    return BeamModel(
        reduced_rows=tuple(
            tuple(int(value) for value in row)
            for row in reduced.tolist()
        ),
        projections=tuple(integer_projection_rows(reduced)),
    )


def prepare_standard_beam_model(
    n_bits: int,
    labels: Sequence[int],
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
) -> BeamModel:
    rows = modular_subset_sum_embedding(
        labels, 0, 1 << n_bits, embedding_scale
    ).tolist()
    return _prepare_model(
        Matrix([row[:-1] for row in rows[:-1]]),
        lll_delta,
    )


def prepare_carry_beam_model(
    n_bits: int,
    labels: Sequence[int],
    low_bits: int,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
) -> BeamModel:
    rows = carry_sliced_embedding(
        labels,
        0,
        n_bits,
        low_bits,
        0,
        embedding_scale,
        low_constraint_scale,
    ).tolist()
    return _prepare_model(
        Matrix([row[:-1] for row in rows[:-1]]),
        lll_delta,
    )


def _projection_priority_increment(
    remainder_numerator: int,
    projection: IntegerProjectionRow,
) -> float:
    denominator = (
        projection.integer_norm_squared
        * projection.common_denominator
        * projection.common_denominator
    )
    try:
        return (remainder_numerator * remainder_numerator) / denominator
    except OverflowError:
        if remainder_numerator == 0:
            return 0.0
        log2_value = (
            2.0 * math.log2(abs(remainder_numerator))
            - math.log2(denominator)
        )
        return math.exp2(min(log2_value, 1023.0))


def target_adaptive_beam_residuals(
    model: BeamModel,
    target_row: Sequence[int],
    beam_width: int,
    maximum_offset: int = 1,
) -> tuple[list[tuple[float, tuple[int, ...]]], int, int]:
    """Return K-best final residuals with exact rounding and float priorities."""
    if beam_width < 1 or maximum_offset < 0:
        raise ValueError("beam width must be positive and offset nonnegative")
    if not model.reduced_rows or len(target_row) != len(model.reduced_rows[0]):
        raise ValueError("target row and beam model dimensions differ")
    if len(model.reduced_rows) != len(model.projections):
        raise ValueError("beam model rank and projection count differ")

    states: list[tuple[float, tuple[int, ...]]] = [
        (0.0, tuple(int(value) for value in target_row))
    ]
    expanded = 0
    peak = 1
    for index in range(len(model.reduced_rows) - 1, -1, -1):
        row = model.reduced_rows[index]
        projection = model.projections[index]
        candidates: dict[tuple[int, ...], float] = {}
        for score, residual in states:
            dot = sum(
                value * coefficient
                for value, coefficient in zip(
                    residual, projection.integer_vector
                )
            )
            coordinate_numerator = projection.common_denominator * dot
            nearest = _nearest_integer_ratio(
                coordinate_numerator,
                projection.integer_norm_squared,
            )
            for delta in range(-maximum_offset, maximum_offset + 1):
                coefficient = nearest + delta
                next_residual = tuple(
                    value - coefficient * base
                    for value, base in zip(residual, row)
                )
                remainder = (
                    coordinate_numerator
                    - coefficient * projection.integer_norm_squared
                )
                next_score = score + _projection_priority_increment(
                    remainder, projection
                )
                previous = candidates.get(next_residual)
                if previous is None or next_score < previous:
                    candidates[next_residual] = next_score
                expanded += 1
        states = heapq.nsmallest(
            beam_width,
            (
                (score, residual)
                for residual, score in candidates.items()
            ),
            key=lambda item: (item[0], item[1]),
        )
        peak = max(peak, len(states))
    return states, expanded, peak


def _marker_shaped_standard(vector: Sequence[int]) -> bool:
    return (
        len(vector) >= 2
        and vector[-1] == -1
        and vector[-2] == 0
        and all(value in {-1, 1} for value in vector[:-2])
    )


def _marker_shaped_carry(vector: Sequence[int]) -> bool:
    return (
        len(vector) >= 3
        and vector[-1] == -1
        and vector[-2] == 0
        and vector[-3] == 0
        and all(value in {-1, 1} for value in vector[:-3])
    )


def standard_target_adaptive_beam_decode(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    width_power: int = 2,
    maximum_offset: int = 1,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    model: BeamModel | None = None,
) -> BeamSearchOutcome:
    modulus = 1 << n_bits
    prepared = model or prepare_standard_beam_model(
        n_bits, labels, embedding_scale, lll_delta
    )
    full = modular_subset_sum_embedding(
        labels, target, modulus, embedding_scale
    ).tolist()
    target_row = [int(value) for value in full[-1][:-1]]
    width = polynomial_beam_width(n_bits, width_power)
    states, expanded, peak = target_adaptive_beam_residuals(
        prepared, target_row, width, maximum_offset
    )
    valid = 0
    invalid = 0
    for _, residual in states:
        vector = [-value for value in residual] + [-1]
        witness = decode_short_standard_marker_vector(
            vector, labels, target, modulus
        )
        if witness is not None:
            valid += 1
        elif _marker_shaped_standard(vector):
            invalid += 1
    bound = beam_expansion_upper_bound(
        len(prepared.reduced_rows), width, maximum_offset
    )
    return BeamSearchOutcome(
        solved=valid > 0,
        valid_witness_count=valid,
        invalid_marker_candidate_count=invalid,
        beam_width=width,
        maximum_offset=maximum_offset,
        rank=len(prepared.reduced_rows),
        branch_factor=2 * maximum_offset + 1,
        expanded_state_count=expanded,
        expansion_upper_bound=bound,
        peak_retained_state_count=peak,
        final_state_count=len(states),
        exact_nearest_integer_decisions=True,
        floating_priority_only=True,
        state_bound_verified=expanded <= bound,
        reachable_carry_count=1,
        winning_carry=None,
    )


def carry_target_adaptive_beam_decode(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    low_bits: int,
    width_power: int = 2,
    maximum_offset: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    model: BeamModel | None = None,
) -> BeamSearchOutcome:
    prepared = model or prepare_carry_beam_model(
        n_bits,
        labels,
        low_bits,
        embedding_scale,
        low_constraint_scale,
        lll_delta,
    )
    carries = reachable_carries(labels, target, low_bits)
    width = polynomial_beam_width(n_bits, width_power)
    expanded = 0
    peak = 0
    final_count = 0
    valid = 0
    invalid = 0
    winning_carry: int | None = None
    for carry in carries:
        full = carry_sliced_embedding(
            labels,
            target,
            n_bits,
            low_bits,
            carry,
            embedding_scale,
            low_constraint_scale,
        ).tolist()
        target_row = [int(value) for value in full[-1][:-1]]
        states, carry_expanded, carry_peak = target_adaptive_beam_residuals(
            prepared, target_row, width, maximum_offset
        )
        expanded += carry_expanded
        peak = max(peak, carry_peak)
        final_count += len(states)
        for _, residual in states:
            vector = [-value for value in residual] + [-1]
            witness = decode_carry_sliced_vector(
                vector,
                labels,
                target,
                n_bits,
                low_bits,
                carry,
            )
            if witness is not None:
                valid += 1
                winning_carry = carry
            elif _marker_shaped_carry(vector):
                invalid += 1
        if valid:
            break
    bound = beam_expansion_upper_bound(
        len(prepared.reduced_rows),
        width,
        maximum_offset,
        outer_factor=len(carries),
    )
    return BeamSearchOutcome(
        solved=valid > 0,
        valid_witness_count=valid,
        invalid_marker_candidate_count=invalid,
        beam_width=width,
        maximum_offset=maximum_offset,
        rank=len(prepared.reduced_rows),
        branch_factor=2 * maximum_offset + 1,
        expanded_state_count=expanded,
        expansion_upper_bound=bound,
        peak_retained_state_count=peak,
        final_state_count=final_count,
        exact_nearest_integer_decisions=True,
        floating_priority_only=True,
        state_bound_verified=expanded <= bound,
        reachable_carry_count=len(carries),
        winning_carry=winning_carry,
    )


def _trial_from_outcome(
    *,
    n_bits: int,
    register_offset: int,
    trial_index: int,
    decoder_variant: str,
    width_power: int,
    target_legality_exactly_known: bool,
    target_legal: bool | None,
    outcome: BeamSearchOutcome,
) -> TargetAdaptiveBeamTrial:
    return TargetAdaptiveBeamTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=n_bits + register_offset,
        trial_index=trial_index,
        decoder_variant=decoder_variant,
        width_power=width_power,
        beam_width=outcome.beam_width,
        maximum_offset=outcome.maximum_offset,
        target_sampled_independently_uniform=True,
        target_legality_exactly_known=target_legality_exactly_known,
        target_legal=target_legal,
        solved=outcome.solved,
        valid_witness_count=outcome.valid_witness_count,
        invalid_marker_candidate_count=outcome.invalid_marker_candidate_count,
        expanded_state_count=outcome.expanded_state_count,
        expansion_upper_bound=outcome.expansion_upper_bound,
        peak_retained_state_count=outcome.peak_retained_state_count,
        final_state_count=outcome.final_state_count,
        reachable_carry_count=outcome.reachable_carry_count,
        winning_carry=outcome.winning_carry,
        exact_nearest_integer_decisions=(
            outcome.exact_nearest_integer_decisions
        ),
        floating_priority_only=outcome.floating_priority_only,
        state_bound_verified=outcome.state_bound_verified,
    )


def wilson_interval(
    success_count: int,
    trial_count: int,
    z_score: float = 1.959963984540054,
) -> tuple[float, float]:
    if trial_count < 1 or not 0 <= success_count <= trial_count:
        raise ValueError("invalid binomial counts")
    if z_score <= 0:
        raise ValueError("z score must be positive")
    rate = success_count / trial_count
    z_squared = z_score * z_score
    denominator = 1.0 + z_squared / trial_count
    center = (
        rate + z_squared / (2.0 * trial_count)
    ) / denominator
    radius = (
        z_score
        * math.sqrt(
            rate * (1.0 - rate) / trial_count
            + z_squared / (4.0 * trial_count * trial_count)
        )
        / denominator
    )
    lower = 0.0 if success_count == 0 else max(0.0, center - radius)
    upper = 1.0 if success_count == trial_count else min(1.0, center + radius)
    return lower, upper


def _scaling_rows(
    trials: Sequence[TargetAdaptiveBeamTrial],
) -> list[TargetAdaptiveBeamScalingRow]:
    keys = sorted(
        {
            (
                trial.n_bits,
                trial.register_offset,
                trial.decoder_variant,
                trial.width_power,
            )
            for trial in trials
        }
    )
    rows = []
    for n_bits, offset, variant, power in keys:
        group = [
            trial
            for trial in trials
            if (
                trial.n_bits,
                trial.register_offset,
                trial.decoder_variant,
                trial.width_power,
            )
            == (n_bits, offset, variant, power)
        ]
        exact = [
            trial for trial in group if trial.target_legality_exactly_known
        ]
        legal = [trial for trial in exact if trial.target_legal]
        success_count = sum(trial.solved for trial in group)
        lower, upper = wilson_interval(success_count, len(group))
        rows.append(
            TargetAdaptiveBeamScalingRow(
                n_bits=n_bits,
                register_offset=offset,
                decoder_variant=variant,
                width_power=power,
                beam_width=n_bits**power,
                trial_count=len(group),
                exact_legality_trial_count=len(exact),
                exact_legal_trial_count=len(legal),
                success_count=success_count,
                unconditional_uniform_source_success_rate=(
                    success_count / len(group)
                ),
                uniform_source_success_wilson_95_lower=lower,
                uniform_source_success_wilson_95_upper=upper,
                exact_legal_coverage=(
                    sum(trial.solved for trial in legal) / len(legal)
                    if legal
                    else None
                ),
                invalid_marker_candidate_count=sum(
                    trial.invalid_marker_candidate_count for trial in group
                ),
                total_expanded_state_count=sum(
                    trial.expanded_state_count for trial in group
                ),
                maximum_expansion_upper_bound=max(
                    trial.expansion_upper_bound for trial in group
                ),
                state_bound_failure_count=sum(
                    not trial.state_bound_verified for trial in group
                ),
                finite_row_is_inverse_polynomial_source_theorem=False,
            )
        )
    return rows


def run_target_adaptive_beam_audit(
    n_values: Sequence[int] = (12, 16, 20, 24, 32, 40, 48),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 2,
    standard_width_powers: Sequence[int] = (1, 2),
    carry_width_powers: Sequence[int] = (1, 2),
    maximum_offset: int = 1,
    exact_legality_max_n: int = 20,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    seed: int = 0,
) -> DCPMarkerTargetAdaptiveBeamReport:
    if (
        not n_values
        or not register_offsets
        or trials_per_row < 1
        or not standard_width_powers
    ):
        raise ValueError("nonempty ranges and positive trials are required")
    if maximum_offset < 0 or exact_legality_max_n < 0:
        raise ValueError("invalid offset or exact-legality limit")

    trials: list[TargetAdaptiveBeamTrial] = []
    for n_index, n_bits in enumerate(n_values):
        for offset_index, offset in enumerate(register_offsets):
            for trial_index in range(trials_per_row):
                rng = random.Random(
                    seed
                    + 1_000_003 * n_index
                    + 10_007 * offset_index
                    + trial_index
                )
                modulus = 1 << n_bits
                labels = [
                    rng.randrange(modulus)
                    for _ in range(n_bits + offset)
                ]
                target = rng.randrange(modulus)
                exact_known = n_bits <= exact_legality_max_n
                target_legal = (
                    bool(subset_sum_counts(n_bits, labels)[target])
                    if exact_known
                    else None
                )
                standard_model = prepare_standard_beam_model(
                    n_bits, labels, embedding_scale, lll_delta
                )
                for power in standard_width_powers:
                    outcome = standard_target_adaptive_beam_decode(
                        n_bits,
                        labels,
                        target,
                        power,
                        maximum_offset,
                        embedding_scale,
                        lll_delta,
                        standard_model,
                    )
                    trials.append(
                        _trial_from_outcome(
                            n_bits=n_bits,
                            register_offset=offset,
                            trial_index=trial_index,
                            decoder_variant="standard",
                            width_power=power,
                            target_legality_exactly_known=exact_known,
                            target_legal=target_legal,
                            outcome=outcome,
                        )
                    )

                if carry_width_powers:
                    low_bits = constrained_low_bits(
                        n_bits, log_multiplier
                    )
                    carry_model = prepare_carry_beam_model(
                        n_bits,
                        labels,
                        low_bits,
                        embedding_scale,
                        low_constraint_scale,
                        lll_delta,
                    )
                    for power in carry_width_powers:
                        outcome = carry_target_adaptive_beam_decode(
                            n_bits,
                            labels,
                            target,
                            low_bits,
                            power,
                            maximum_offset,
                            embedding_scale,
                            low_constraint_scale,
                            lll_delta,
                            carry_model,
                        )
                        trials.append(
                            _trial_from_outcome(
                                n_bits=n_bits,
                                register_offset=offset,
                                trial_index=trial_index,
                                decoder_variant="carry-sliced",
                                width_power=power,
                                target_legality_exactly_known=exact_known,
                                target_legal=target_legal,
                                outcome=outcome,
                            )
                        )

    rows = _scaling_rows(trials)
    tail_n = max(n_values)
    standard_max_power = max(standard_width_powers)
    carry_max_power = max(carry_width_powers, default=-1)

    def tail_rate(variant: str, power: int) -> float:
        relevant = [
            row.unconditional_uniform_source_success_rate
            for row in rows
            if row.n_bits == tail_n
            and row.decoder_variant == variant
            and row.width_power == power
        ]
        return sum(relevant) / len(relevant) if relevant else 0.0

    standard_tail = tail_rate("standard", standard_max_power)
    carry_tail = (
        tail_rate("carry-sliced", carry_max_power)
        if carry_width_powers
        else 0.0
    )

    def tail_interval(variant: str, power: int) -> tuple[float, float]:
        relevant = [
            trial
            for trial in trials
            if trial.n_bits == tail_n
            and trial.decoder_variant == variant
            and trial.width_power == power
        ]
        return (
            wilson_interval(
                sum(trial.solved for trial in relevant),
                len(relevant),
            )
            if relevant
            else (0.0, 1.0)
        )

    standard_tail_lower, standard_tail_upper = tail_interval(
        "standard", standard_max_power
    )
    carry_tail_lower, carry_tail_upper = (
        tail_interval("carry-sliced", carry_max_power)
        if carry_width_powers
        else (0.0, 1.0)
    )
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "source_instance_count": len(
            {
                (
                    trial.n_bits,
                    trial.register_offset,
                    trial.trial_index,
                )
                for trial in trials
            }
        ),
        "independent_uniform_target_trial_count": sum(
            trial.target_sampled_independently_uniform for trial in trials
        ),
        "exact_legality_trial_count": sum(
            trial.target_legality_exactly_known for trial in trials
        ),
        "exact_legality_source_instance_count": len(
            {
                (
                    trial.n_bits,
                    trial.register_offset,
                    trial.trial_index,
                )
                for trial in trials
                if trial.target_legality_exactly_known
            }
        ),
        "maximum_n_bits": tail_n,
        "maximum_standard_width_power": standard_max_power,
        "maximum_carry_width_power": carry_max_power,
        "maximum_beam_width": max(
            (trial.beam_width for trial in trials), default=0
        ),
        "total_expanded_state_count": sum(
            trial.expanded_state_count for trial in trials
        ),
        "exact_rounding_failure_count": sum(
            not trial.exact_nearest_integer_decisions for trial in trials
        ),
        "state_bound_failure_count": sum(
            not trial.state_bound_verified for trial in trials
        ),
        "invalid_marker_candidate_count": sum(
            trial.invalid_marker_candidate_count for trial in trials
        ),
        "polynomial_state_bound_theorem_count": 1,
        "tail_standard_max_power_source_success_rate": standard_tail,
        "tail_standard_max_power_wilson_95_lower": standard_tail_lower,
        "tail_standard_max_power_wilson_95_upper": standard_tail_upper,
        "tail_carry_max_power_source_success_rate": carry_tail,
        "tail_carry_max_power_wilson_95_lower": carry_tail_lower,
        "tail_carry_max_power_wilson_95_upper": carry_tail_upper,
        "largest_n_with_standard_success": max(
            (
                trial.n_bits
                for trial in trials
                if trial.decoder_variant == "standard" and trial.solved
            ),
            default=0,
        ),
        "largest_n_with_carry_success": max(
            (
                trial.n_bits
                for trial in trials
                if trial.decoder_variant == "carry-sliced" and trial.solved
            ),
            default=0,
        ),
        "proved_inverse_polynomial_uniform_source_success_count": 0,
        "source_contract_satisfying_row_count": 0,
        "polynomial_verified_decoder_family_count": 1,
        "polynomial_witness_decoder_count": 0,
    }
    finite_survivor = standard_tail > 0.0 or carry_tail > 0.0
    return DCPMarkerTargetAdaptiveBeamReport(
        created_at=utc_now(),
        decoder_contract={
            "instance_source": (
                "independent uniform labels A in Z_(2^n)^(n+c) and "
                "independent uniform target t; no witness is planted"
            ),
            "search": (
                "K-best nearest-plane expansion ordered by accumulated "
                "orthogonal residual energy"
            ),
            "rounding": (
                "nearest-integer coefficients are exact rational decisions; "
                "floating point is used only to prioritize retained paths"
            ),
            "output": (
                "a marker-minus-one vector is accepted only after exact "
                "binary subset-sum verification"
            ),
            "carry": (
                "all reachable O(log n)-bit carry slices are explicitly "
                "enumerated and charged"
            ),
        },
        polynomial_bound={
            "standard": "rank*(2q+1)*n^a expanded states",
            "carry_sliced": (
                "|reachable carries|*rank*(2q+1)*n^a expanded states"
            ),
            "fixed_parameters_are_polynomial": True,
            "bound_verified_on_every_trial": (
                metrics["state_bound_failure_count"] == 0
            ),
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "target_adaptation_is_legal_under_source_model": True,
            "targets_sampled_independently_uniform": True,
            "exact_nearest_integer_decisions": (
                metrics["exact_rounding_failure_count"] == 0
            ),
            "all_outputs_exactly_verified": (
                metrics["invalid_marker_candidate_count"] == 0
            ),
            "polynomial_state_bound_proved": (
                metrics["state_bound_failure_count"] == 0
            ),
            "finite_target_adaptive_beam_survivor": finite_survivor,
            "inverse_polynomial_uniform_source_success_proved": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "This is a stronger legal classical baseline. Its finite "
                "success frontier neither proves inverse-polynomial source "
                "coverage nor establishes an asymptotic failure law."
            ),
        },
        status=(
            "target-adaptive-polynomial-beam-finite-survivor-proof-debt"
            if finite_survivor
            else "target-adaptive-polynomial-beam-finite-tail-collapse"
        ),
        summary=(
            f"Ran {len(trials)} source-native target-adaptive beam trials "
            f"through n={tail_n}. Maximum-power tail success was "
            f"{standard_tail:.6g} standard and {carry_tail:.6g} carry-sliced; "
            "no inverse-polynomial source theorem follows."
        ),
        falsifiers_triggered=[
            "Public, target-independent coordinate charts are not the strongest legal classical nearest-plane baseline.",
            "A finite width-power improvement is not an inverse-polynomial source-coverage theorem.",
            "A finite tail collapse is not a lower bound against larger fixed polynomial powers or non-beam affine-CVP algorithms.",
            "Floating priorities cannot be cited as exact ordering certificates, although all rounding and output checks are exact.",
        ],
    )


def write_target_adaptive_beam_audit(
    path: Path = DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict[str, object]:
    payload = asdict(run_target_adaptive_beam_audit(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-MARKER-TARGET-ADAPTIVE-BEAM-FINITE-NOT-SOURCE-THEOREM",
                source=str(path),
                claim=(
                    "Finite success or failure of an n^a target-adaptive "
                    "nearest-plane beam establishes its asymptotic random-source coverage."
                ),
                reason_invalid=(
                    "Every tested width is polynomial and source-native, but "
                    "the sweep supplies neither an inverse-polynomial success "
                    "lower bound nor an all-fixed-powers failure theorem."
                ),
                lesson=(
                    "Use target-adaptive K-best search as the minimum classical "
                    "marker baseline. Promote it only with a uniform source law, "
                    "and do not infer quantum advantage from finite collapse."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-TARGET-ADAPTIVE-BEAM"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=payload["headline_metrics"],
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={
                    "dcp_marker_target_adaptive_beam": str(path)
                },
            )
        )
    return payload


def load_and_register_target_adaptive_beam_audit(
    path: Path = DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH,
    **registry_kwargs: object,
) -> dict[str, object]:
    payload = json.loads(path.read_text())
    upsert_negative_result(
        NegativeResultRecord(
            id="NEG-DCP-MARKER-TARGET-ADAPTIVE-BEAM-FINITE-NOT-SOURCE-THEOREM",
            source=str(path),
            claim=(
                "Finite target-adaptive beam scaling establishes an "
                "asymptotic source theorem."
            ),
            reason_invalid=(
                "The stored sweep has exact output verification and polynomial "
                "state accounting but no uniform asymptotic success or failure law."
            ),
            lesson=(
                "Retain the beam as a classical baseline and keep source-law "
                "proof debt explicit."
            ),
            applies_to=[
                str(registry_kwargs.get("registry_candidate_id", DEFAULT_CANDIDATE_ID)),
                str(registry_kwargs.get("registry_experiment_id", DEFAULT_EXPERIMENT_ID)),
            ],
            evidence=payload["headline_metrics"],
        )
    )
    experiment_id = str(
        registry_kwargs.get("registry_experiment_id", DEFAULT_EXPERIMENT_ID)
    )
    candidate_id = str(
        registry_kwargs.get("registry_candidate_id", DEFAULT_CANDIDATE_ID)
    )
    result_id = str(
        registry_kwargs.get(
            "registry_result_id",
            f"RESULT-{experiment_id}-TARGET-ADAPTIVE-BEAM",
        )
    )
    upsert_experiment_result(
        ExperimentResultRecord(
            id=result_id,
            experiment_id=experiment_id,
            candidate_id=candidate_id,
            created_at=str(payload["created_at"]),
            status=str(payload["status"]),
            summary=str(payload["summary"]),
            metrics=payload["headline_metrics"],
            falsifiers_triggered=list(payload["falsifiers_triggered"]),
            artifacts={"dcp_marker_target_adaptive_beam": str(path)},
        )
    )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_target_adaptive_beam_audit()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
