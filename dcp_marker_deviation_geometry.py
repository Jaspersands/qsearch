"""Exact witness-path geometry for marker-aware nearest-plane decoding.

For every exactly enumerated Boolean witness, this module expresses the
corresponding marker-zero lattice point in the LLL-reduced kernel basis and
replays nearest plane using those true coefficients.  At each Gram-Schmidt
level it records the difference between the witness coefficient and the
nearest rounding decision.

A witness belongs to the one-step branch tree at depth ``k`` exactly when every
offset has magnitude at most one and at most ``k`` offsets are nonzero.  This
provides a witness-complete explanation of bounded-list success or failure
without enumerating every list candidate.  Finite deviation growth is not an
asymptotic lower bound; a theorem would need to control these source-dependent
coordinates under LLL reduction.
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


DCP_MARKER_DEVIATION_GEOMETRY_PATH = Path(
    "research/classical_baselines/dcp_marker_deviation_geometry.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-MARKER-DEVIATION-GEOMETRY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class WitnessDeviationProfile:
    nonzero_rounding_deviation_count: int
    maximum_absolute_rounding_offset: int
    total_absolute_rounding_offset: int
    one_step_branch_tree_eligible: bool
    minimum_one_step_branch_depth: int | None
    normalized_deviation_depth: float | None
    exact_replay_verified: bool


@dataclass(frozen=True)
class MarkerDeviationTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    target_legal: bool
    exact_witness_count: int
    enumerated_witness_count: int
    witness_enumeration_truncated: bool
    constrained_low_bits: int
    standard_profiles: list[WitnessDeviationProfile]
    carry_sliced_profiles: list[WitnessDeviationProfile]
    standard_minimum_one_step_depth: int | None
    carry_minimum_one_step_depth: int | None
    standard_minimum_maximum_offset: int | None
    carry_minimum_maximum_offset: int | None
    standard_depth_two_predicted_solved: bool
    carry_depth_two_predicted_solved: bool
    source_is_independent_uniform_target: bool


@dataclass(frozen=True)
class MarkerDeviationScalingRow:
    n_bits: int
    register_offset: int
    trial_count: int
    legal_trial_count: int
    complete_witness_enumeration_count: int
    standard_depth_zero_predicted_success_count: int
    standard_depth_one_predicted_success_count: int
    standard_depth_two_predicted_success_count: int
    carry_depth_zero_predicted_success_count: int
    carry_depth_one_predicted_success_count: int
    carry_depth_two_predicted_success_count: int
    standard_one_step_tree_escape_trial_count: int
    carry_one_step_tree_escape_trial_count: int
    median_standard_minimum_deviation_depth: float | None
    median_carry_minimum_deviation_depth: float | None
    median_standard_minimum_maximum_offset: float | None
    median_carry_minimum_maximum_offset: float | None
    finite_row_is_deviation_growth_theorem: bool


@dataclass(frozen=True)
class DCPMarkerDeviationGeometryReport:
    created_at: str
    geometry_contract: dict[str, str]
    rows: list[MarkerDeviationScalingRow]
    trials: list[MarkerDeviationTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _nearest_integer(value: Fraction) -> int:
    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def witness_rounding_deviation_profile(
    reduced_basis: Matrix,
    target_row: Sequence[int],
    witness_error: Sequence[int],
) -> WitnessDeviationProfile:
    """Replay the exact nearest-plane path to one known witness lattice point."""
    if reduced_basis.rows > reduced_basis.cols:
        raise ValueError("reduced kernel basis cannot have more rows than ambient columns")
    if len(target_row) != reduced_basis.cols or len(witness_error) != reduced_basis.cols:
        raise ValueError("basis, target, and witness error dimensions differ")
    lattice_point = Matrix(
        [int(target) - int(error) for target, error in zip(target_row, witness_error)]
    )
    row_gram = reduced_basis * reduced_basis.T
    solved = row_gram.inv() * reduced_basis * lattice_point
    if any(value.q != 1 for value in solved):
        raise ArithmeticError("witness lattice point has nonintegral reduced-basis coordinates")
    coefficients = [int(value) for value in solved]
    rows = [[Fraction(int(value)) for value in row] for row in reduced_basis.tolist()]
    orthogonal = exact_gram_schmidt_rows(reduced_basis)
    residual = [Fraction(int(value)) for value in target_row]
    offsets: list[int] = []
    for index in range(len(rows) - 1, -1, -1):
        star = orthogonal[index]
        coordinate = _dot(residual, star) / _dot(star, star)
        nearest = _nearest_integer(coordinate)
        true_coefficient = coefficients[index]
        offsets.append(true_coefficient - nearest)
        residual = [
            value - true_coefficient * base
            for value, base in zip(residual, rows[index])
        ]
    expected_error = [Fraction(int(value)) for value in witness_error]
    replay_verified = residual == expected_error
    maximum = max((abs(value) for value in offsets), default=0)
    nonzero = sum(value != 0 for value in offsets)
    eligible = maximum <= 1
    return WitnessDeviationProfile(
        nonzero_rounding_deviation_count=nonzero,
        maximum_absolute_rounding_offset=maximum,
        total_absolute_rounding_offset=sum(abs(value) for value in offsets),
        one_step_branch_tree_eligible=eligible,
        minimum_one_step_branch_depth=nonzero if eligible else None,
        normalized_deviation_depth=(nonzero / reduced_basis.rows if eligible else None),
        exact_replay_verified=replay_verified,
    )


def _standard_basis_and_target(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    embedding_scale: int,
    lll_delta: float,
) -> tuple[Matrix, list[int]]:
    full = modular_subset_sum_embedding(labels, target, 1 << n_bits, embedding_scale)
    rows = full.tolist()
    basis = Matrix([row[:-1] for row in rows[:-1]]).lll(delta=lll_delta)
    return basis, [int(value) for value in rows[-1][:-1]]


def _carry_basis_and_target(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    low_bits: int,
    carry: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
) -> tuple[Matrix, list[int]]:
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
    basis = Matrix([row[:-1] for row in rows[:-1]]).lll(delta=lll_delta)
    return basis, [int(value) for value in rows[-1][:-1]]


def _minimum_depth(profiles: Sequence[WitnessDeviationProfile]) -> int | None:
    values = [
        profile.minimum_one_step_branch_depth
        for profile in profiles
        if profile.minimum_one_step_branch_depth is not None
    ]
    return min(values) if values else None


def _minimum_maximum_offset(
    profiles: Sequence[WitnessDeviationProfile],
) -> int | None:
    return min(
        (profile.maximum_absolute_rounding_offset for profile in profiles),
        default=None,
    )


def run_marker_deviation_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    witness_cap: int,
    seed: int,
) -> MarkerDeviationTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    witness_count, witnesses, truncated = exact_mitm_witnesses(
        labels, target, modulus, witness_cap
    )
    standard_basis, standard_target = _standard_basis_and_target(
        n_bits, labels, target, embedding_scale, lll_delta
    )
    standard_profiles = [
        witness_rounding_deviation_profile(
            standard_basis,
            standard_target,
            [1 - 2 * bit for bit in witness] + [0],
        )
        for witness in witnesses
    ]

    low_bits = constrained_low_bits(n_bits, log_multiplier)
    low_modulus = 1 << low_bits
    target_low = target % low_modulus
    carry_cache: dict[int, tuple[Matrix, list[int]]] = {}
    carry_profiles: list[WitnessDeviationProfile] = []
    for witness in witnesses:
        low_sum = sum(
            (label % low_modulus) * bit for label, bit in zip(labels, witness)
        )
        carry = (low_sum - target_low) // low_modulus
        if carry not in carry_cache:
            carry_cache[carry] = _carry_basis_and_target(
                n_bits,
                labels,
                target,
                low_bits,
                carry,
                embedding_scale,
                low_constraint_scale,
                lll_delta,
            )
        basis, target_row = carry_cache[carry]
        carry_profiles.append(
            witness_rounding_deviation_profile(
                basis,
                target_row,
                [1 - 2 * bit for bit in witness] + [0, 0],
            )
        )

    standard_depth = _minimum_depth(standard_profiles)
    carry_depth = _minimum_depth(carry_profiles)
    return MarkerDeviationTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        target_legal=witness_count > 0,
        exact_witness_count=witness_count,
        enumerated_witness_count=len(witnesses),
        witness_enumeration_truncated=truncated,
        constrained_low_bits=low_bits,
        standard_profiles=standard_profiles,
        carry_sliced_profiles=carry_profiles,
        standard_minimum_one_step_depth=standard_depth,
        carry_minimum_one_step_depth=carry_depth,
        standard_minimum_maximum_offset=_minimum_maximum_offset(standard_profiles),
        carry_minimum_maximum_offset=_minimum_maximum_offset(carry_profiles),
        standard_depth_two_predicted_solved=(
            standard_depth is not None and standard_depth <= 2
        ),
        carry_depth_two_predicted_solved=(
            carry_depth is not None and carry_depth <= 2
        ),
        source_is_independent_uniform_target=True,
    )


def _predicted_at_depth(
    trial: MarkerDeviationTrial,
    depth: int,
    carry: bool,
) -> bool:
    value = (
        trial.carry_minimum_one_step_depth
        if carry
        else trial.standard_minimum_one_step_depth
    )
    return value is not None and value <= depth


def _median_optional(values: Sequence[int | None]) -> float | None:
    present = [value for value in values if value is not None]
    return float(median(present)) if present else None


def run_marker_deviation_geometry(
    n_values: Sequence[int] = (20, 24, 28, 32, 36),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 4,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    witness_cap: int = 256,
    seed: int = 0,
) -> DCPMarkerDeviationGeometryReport:
    if trials_per_row < 1 or witness_cap < 1:
        raise ValueError("trials and witness cap must be positive")
    trials = [
        run_marker_deviation_trial(
            n_bits,
            offset,
            trial_index,
            log_multiplier,
            embedding_scale,
            low_constraint_scale,
            lll_delta,
            witness_cap,
            seed + 1_000_003 * ni + 10_007 * oi + trial_index,
        )
        for ni, n_bits in enumerate(n_values)
        for oi, offset in enumerate(register_offsets)
        for trial_index in range(trials_per_row)
    ]
    rows: list[MarkerDeviationScalingRow] = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            legal = [trial for trial in group if trial.target_legal]
            complete = [trial for trial in legal if not trial.witness_enumeration_truncated]
            rows.append(
                MarkerDeviationScalingRow(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_count=len(group),
                    legal_trial_count=len(legal),
                    complete_witness_enumeration_count=len(complete),
                    standard_depth_zero_predicted_success_count=sum(
                        _predicted_at_depth(trial, 0, False) for trial in complete
                    ),
                    standard_depth_one_predicted_success_count=sum(
                        _predicted_at_depth(trial, 1, False) for trial in complete
                    ),
                    standard_depth_two_predicted_success_count=sum(
                        _predicted_at_depth(trial, 2, False) for trial in complete
                    ),
                    carry_depth_zero_predicted_success_count=sum(
                        _predicted_at_depth(trial, 0, True) for trial in complete
                    ),
                    carry_depth_one_predicted_success_count=sum(
                        _predicted_at_depth(trial, 1, True) for trial in complete
                    ),
                    carry_depth_two_predicted_success_count=sum(
                        _predicted_at_depth(trial, 2, True) for trial in complete
                    ),
                    standard_one_step_tree_escape_trial_count=sum(
                        trial.standard_minimum_one_step_depth is None for trial in complete
                    ),
                    carry_one_step_tree_escape_trial_count=sum(
                        trial.carry_minimum_one_step_depth is None for trial in complete
                    ),
                    median_standard_minimum_deviation_depth=_median_optional(
                        [trial.standard_minimum_one_step_depth for trial in complete]
                    ),
                    median_carry_minimum_deviation_depth=_median_optional(
                        [trial.carry_minimum_one_step_depth for trial in complete]
                    ),
                    median_standard_minimum_maximum_offset=_median_optional(
                        [trial.standard_minimum_maximum_offset for trial in complete]
                    ),
                    median_carry_minimum_maximum_offset=_median_optional(
                        [trial.carry_minimum_maximum_offset for trial in complete]
                    ),
                    finite_row_is_deviation_growth_theorem=False,
                )
            )
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    complete_profiles = [
        profile
        for trial in trials
        if not trial.witness_enumeration_truncated
        for profile in (*trial.standard_profiles, *trial.carry_sliced_profiles)
    ]
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "maximum_n_bits": tail_n,
        "legal_trial_count": sum(trial.target_legal for trial in trials),
        "complete_witness_enumeration_trial_count": sum(
            trial.target_legal and not trial.witness_enumeration_truncated
            for trial in trials
        ),
        "exact_replay_failure_count": sum(
            not profile.exact_replay_verified for profile in complete_profiles
        ),
        "tail_complete_legal_trial_count": sum(
            row.complete_witness_enumeration_count for row in tail
        ),
        "tail_standard_depth_two_predicted_success_count": sum(
            row.standard_depth_two_predicted_success_count for row in tail
        ),
        "tail_carry_depth_two_predicted_success_count": sum(
            row.carry_depth_two_predicted_success_count for row in tail
        ),
        "tail_standard_one_step_tree_escape_count": sum(
            row.standard_one_step_tree_escape_trial_count for row in tail
        ),
        "tail_carry_one_step_tree_escape_count": sum(
            row.carry_one_step_tree_escape_trial_count for row in tail
        ),
        "witness_complete_deviation_profile_theorem_count": 1,
        "proved_asymptotic_deviation_growth_count": 0,
        "proved_fixed_depth_source_coverage_upper_bound_count": 0,
        "polynomial_marker_aware_decoder_count": 0,
    }
    return DCPMarkerDeviationGeometryReport(
        created_at=utc_now(),
        geometry_contract={
            "source": "independent uniform labels and target with exact post-sampling legality and witness enumeration",
            "coordinate_map": "solve each witness lattice point exactly in the LLL-reduced marker-zero row basis",
            "path_replay": "use true later coefficients when recomputing every nearest-plane rounding decision",
            "list_equivalence": "one-step tree depth k iff all offsets have magnitude <=1 and at most k are nonzero",
            "claim_rule": "finite deviation growth or tree escape is not an asymptotic source bound",
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "witness_paths_replayed_exactly": metrics["exact_replay_failure_count"] == 0,
            "bounded_list_membership_characterized_exactly": True,
            "finite_deviation_growth_is_asymptotic_theorem": False,
            "fixed_depth_source_coverage_upper_bound_proved": False,
            "general_affine_cvp_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact witness paths explain finite bounded-list failure, but LLL-dependent coordinate growth still "
                "needs a source theorem and does not constrain different affine decoders."
            ),
        },
        status="exact-witness-deviation-geometry-measured-asymptotic-law-open",
        summary=(
            f"Profiled exact nearest-plane paths for {metrics['complete_witness_enumeration_trial_count']} complete legal "
            f"trials through n={tail_n}; tail depth-two standard/carry predictions="
            f"{metrics['tail_standard_depth_two_predicted_success_count']}/"
            f"{metrics['tail_carry_depth_two_predicted_success_count']} over "
            f"{metrics['tail_complete_legal_trial_count']} trials, tree escapes="
            f"{metrics['tail_standard_one_step_tree_escape_count']}/"
            f"{metrics['tail_carry_one_step_tree_escape_count']}; no asymptotic source theorem."
        ),
        falsifiers_triggered=[
            "Every witness coordinate vector and nearest-plane replay is exact rational/integer arithmetic.",
            "Targets are independent uniform and legality is determined only after sampling.",
            "Witness truncation is explicit and excluded from witness-complete conclusions.",
            "One-step tree escape does not rule out larger offsets, growing depth, or another affine decoder.",
            "Finite deviation trends are not promoted to source-probability bounds.",
        ],
    )


def write_marker_deviation_geometry(
    path: Path = DCP_MARKER_DEVIATION_GEOMETRY_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict:
    payload = asdict(run_marker_deviation_geometry(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-FINITE-MARKER-DEVIATION-GROWTH-IS-NOT-A-LOWER-BOUND",
                source=str(path),
                claim=(
                    "Observed growth or one-step-tree escape of exact witness rounding deviations proves that every "
                    "polynomial marker-aware affine decoder has negligible source coverage."
                ),
                reason_invalid=(
                    "The audit characterizes one LLL basis and one nearest-plane branching grammar on finite inputs; "
                    "it supplies no distributional theorem or reduction from general affine decoding."
                ),
                lesson=(
                    "Use exact profiles to formulate a source theorem or design a qualitatively different decoder, "
                    "not to claim an affine-CVP lower bound."
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
                artifacts={"dcp_marker_deviation_geometry": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(json.dumps(write_marker_deviation_geometry()["headline_metrics"], indent=2, sort_keys=True))
