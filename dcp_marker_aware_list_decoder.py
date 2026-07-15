"""Polynomial fixed-depth marker-aware nearest-plane list decoder.

The marker-coset reduction turns a legal density-one subset-sum target into an
affine coset of the marker-zero relation lattice.  One Babai output tests only
one nearest-plane cell.  This module branches at a fixed number of
Gram-Schmidt rounding decisions and tests the resulting target-dependent list.

For kernel rank ``d`` and branch depth ``k``, the standard list contains

    sum_{j=0}^k 2^j binom(d,j)

vectors.  Trying every reachable low carry adds only a factor ``O(n)``.  Thus
every fixed-depth decoder is polynomial in ``n``.  This is a materially stronger
classical baseline than a single Babai output, but finite recovery is not an
inverse-polynomial source-coverage theorem and fixed-depth failure is not a
lower bound against general affine-CVP algorithms.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Callable, Sequence

from sympy import Matrix

from dcp_subset_sum_affine_cvp_baseline import exact_gram_schmidt_rows
from dcp_subset_sum_affine_cvp_scaling import exact_mitm_witness_count
from dcp_subset_sum_carry_slice_lattice import (
    carry_sliced_embedding,
    constrained_low_bits,
    decode_carry_sliced_vector,
    reachable_carries,
)
from dcp_subset_sum_lattice_search import modular_subset_sum_embedding
from dcp_subset_sum_marker_coset_theorem import decode_short_standard_marker_vector
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_MARKER_AWARE_LIST_DECODER_PATH = Path(
    "research/classical_baselines/dcp_marker_aware_list_decoder.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-MARKER-AWARE-LIST-DECODER"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class NearestPlaneListCandidate:
    lattice_vector: list[int]
    coefficients: list[int]
    deviation_count: int
    distance_squared: int


@dataclass(frozen=True)
class MarkerListOutcome:
    branch_depth: int
    candidate_count: int
    theoretical_candidate_count: int
    candidate_count_matches_theorem: bool
    valid_witness_candidate_count: int
    solved: bool
    minimum_distance_squared: int
    minimum_constraint_norm_squared: int
    minimum_binary_defect: int
    winning_carry: int | None


@dataclass(frozen=True)
class MarkerListTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    target_legal: bool
    exact_legal_witness_count: int
    constrained_low_bits: int
    reachable_carry_count: int
    standard_outcomes: list[MarkerListOutcome]
    carry_sliced_outcomes: list[MarkerListOutcome]
    invalid_witness_count: int
    source_is_independent_uniform_target: bool


@dataclass(frozen=True)
class MarkerListScalingRow:
    n_bits: int
    register_offset: int
    branch_depth: int
    trial_count: int
    legal_trial_count: int
    standard_success_count: int
    carry_sliced_success_count: int
    standard_strict_improvement_count: int
    carry_sliced_strict_improvement_count: int
    standard_legal_coverage: float | None
    carry_sliced_legal_coverage: float | None
    mean_standard_candidate_count: float
    mean_carry_sliced_candidate_count: float
    fixed_depth_candidate_family_polynomial: bool
    empirical_row_is_coverage_theorem: bool


@dataclass(frozen=True)
class DCPMarkerAwareListDecoderReport:
    created_at: str
    decoder_contract: dict[str, str]
    rows: list[MarkerListScalingRow]
    trials: list[MarkerListTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def fixed_depth_candidate_count(rank: int, branch_depth: int) -> int:
    if rank < 1 or branch_depth < 0 or branch_depth > rank:
        raise ValueError("requires rank>=1 and 0<=branch_depth<=rank")
    return sum(
        (2**deviations) * math.comb(rank, deviations)
        for deviations in range(branch_depth + 1)
    )


def _dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _nearest_integer(value: Fraction) -> int:
    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def exact_bounded_nearest_plane_list(
    basis: Matrix,
    target: Sequence[int],
    maximum_deviations: int,
) -> list[NearestPlaneListCandidate]:
    """Enumerate all nearest-plane paths with at most fixed rounding deviations."""
    rows = [[Fraction(int(value)) for value in row] for row in basis.tolist()]
    if not rows or len(rows[0]) != len(target):
        raise ValueError("basis and target dimensions are incompatible")
    if maximum_deviations < 0 or maximum_deviations > len(rows):
        raise ValueError("invalid maximum deviation count")
    orthogonal = exact_gram_schmidt_rows(basis)
    target_fraction = [Fraction(int(value)) for value in target]
    candidates: list[NearestPlaneListCandidate] = []

    def recurse(
        index: int,
        residual: list[Fraction],
        coefficients: list[int],
        deviations: int,
    ) -> None:
        if index < 0:
            lattice_vector = [base - remainder for base, remainder in zip(target_fraction, residual)]
            if any(value.denominator != 1 for value in lattice_vector):
                raise ArithmeticError("nearest-plane list left the integer lattice")
            vector = [int(value) for value in lattice_vector]
            candidates.append(
                NearestPlaneListCandidate(
                    lattice_vector=vector,
                    coefficients=list(coefficients),
                    deviation_count=deviations,
                    distance_squared=sum(
                        (int(base) - value) ** 2 for base, value in zip(target, vector)
                    ),
                )
            )
            return

        star = orthogonal[index]
        coordinate = _dot(residual, star) / _dot(star, star)
        nearest = _nearest_integer(coordinate)
        choices = [(nearest, 0)]
        if deviations < maximum_deviations:
            choices.extend(((nearest - 1, 1), (nearest + 1, 1)))
        for coefficient, added_deviation in choices:
            next_coefficients = list(coefficients)
            next_coefficients[index] = coefficient
            next_residual = [
                value - coefficient * base
                for value, base in zip(residual, rows[index])
            ]
            recurse(
                index - 1,
                next_residual,
                next_coefficients,
                deviations + added_deviation,
            )

    recurse(
        len(rows) - 1,
        target_fraction,
        [0] * len(rows),
        0,
    )
    candidates.sort(
        key=lambda item: (
            item.distance_squared,
            item.deviation_count,
            tuple(item.coefficients),
        )
    )
    expected = fixed_depth_candidate_count(len(rows), maximum_deviations)
    if len(candidates) != expected:
        raise AssertionError(f"generated {len(candidates)} candidates, expected {expected}")
    return candidates


def _vector_diagnostics(
    vector: Sequence[int],
    register_count: int,
    constraint_coordinate_count: int,
) -> tuple[int, int, int]:
    distance = sum(int(value) ** 2 for value in vector)
    constraints = vector[
        register_count : register_count + constraint_coordinate_count
    ]
    binary = vector[:register_count]
    return (
        distance,
        sum(int(value) ** 2 for value in constraints),
        sum(min(abs(int(value) - 1), abs(int(value) + 1)) for value in binary),
    )


def _outcomes_from_affine_candidates(
    candidates: Sequence[tuple[NearestPlaneListCandidate, list[int], int | None]],
    rank: int,
    maximum_deviations: int,
    register_count: int,
    constraint_coordinate_count: int,
    carry_factor: int,
    decode: Callable[[list[int], int | None], list[int] | None],
    labels: Sequence[int],
    target: int,
    modulus: int,
) -> tuple[list[MarkerListOutcome], int]:
    outcomes: list[MarkerListOutcome] = []
    invalid = 0
    for depth in range(maximum_deviations + 1):
        selected = [item for item in candidates if item[0].deviation_count <= depth]
        valid = 0
        winning_carry: int | None = None
        diagnostics = [
            _vector_diagnostics(vector, register_count, constraint_coordinate_count)
            for _, vector, _ in selected
        ]
        for _, vector, carry in selected:
            witness = decode(vector, carry)
            if witness is None:
                continue
            if sum(label * bit for label, bit in zip(labels, witness)) % modulus != target:
                invalid += 1
                continue
            valid += 1
            if winning_carry is None:
                winning_carry = carry
        theoretical = fixed_depth_candidate_count(rank, depth) * carry_factor
        outcomes.append(
            MarkerListOutcome(
                branch_depth=depth,
                candidate_count=len(selected),
                theoretical_candidate_count=theoretical,
                candidate_count_matches_theorem=len(selected) == theoretical,
                valid_witness_candidate_count=valid,
                solved=valid > 0,
                minimum_distance_squared=min(item[0] for item in diagnostics),
                minimum_constraint_norm_squared=min(item[1] for item in diagnostics),
                minimum_binary_defect=min(item[2] for item in diagnostics),
                winning_carry=winning_carry,
            )
        )
    return outcomes, invalid


def standard_marker_list_decode(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    maximum_deviations: int = 2,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
) -> tuple[list[MarkerListOutcome], int]:
    modulus = 1 << n_bits
    full = modular_subset_sum_embedding(labels, target, modulus, embedding_scale)
    rows = full.tolist()
    kernel = Matrix([row[:-1] for row in rows[:-1]])
    target_row = [int(value) for value in rows[-1][:-1]]
    reduced = kernel.lll(delta=lll_delta)
    nearest = exact_bounded_nearest_plane_list(reduced, target_row, maximum_deviations)
    candidates = [
        (
            item,
            [value - base for value, base in zip(item.lattice_vector, target_row)]
            + [-1],
            None,
        )
        for item in nearest
    ]
    return _outcomes_from_affine_candidates(
        candidates,
        reduced.rows,
        maximum_deviations,
        len(labels),
        1,
        1,
        lambda vector, _carry: decode_short_standard_marker_vector(
            vector, labels, target, modulus
        ),
        labels,
        target,
        modulus,
    )


def carry_sliced_marker_list_decode(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    low_bits: int,
    maximum_deviations: int = 2,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
) -> tuple[list[MarkerListOutcome], int, int]:
    modulus = 1 << n_bits
    carries = reachable_carries(labels, target, low_bits)
    all_candidates: list[tuple[NearestPlaneListCandidate, list[int], int | None]] = []
    rank: int | None = None
    for carry in carries:
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
        kernel = Matrix([row[:-1] for row in rows[:-1]])
        target_row = [int(value) for value in rows[-1][:-1]]
        reduced = kernel.lll(delta=lll_delta)
        rank = reduced.rows
        nearest = exact_bounded_nearest_plane_list(
            reduced, target_row, maximum_deviations
        )
        all_candidates.extend(
            (
                item,
                [value - base for value, base in zip(item.lattice_vector, target_row)]
                + [-1],
                carry,
            )
            for item in nearest
        )
    if rank is None:
        raise AssertionError("reachable carry set must be nonempty")
    outcomes, invalid = _outcomes_from_affine_candidates(
        all_candidates,
        rank,
        maximum_deviations,
        len(labels),
        2,
        len(carries),
        lambda vector, carry: decode_carry_sliced_vector(
            vector,
            labels,
            target,
            n_bits,
            low_bits,
            int(carry),
        ),
        labels,
        target,
        modulus,
    )
    return outcomes, invalid, len(carries)


def run_marker_list_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    maximum_deviations: int,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    seed: int,
) -> MarkerListTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    witness_count = exact_mitm_witness_count(labels, target, modulus)
    standard, standard_invalid = standard_marker_list_decode(
        n_bits,
        labels,
        target,
        maximum_deviations,
        embedding_scale,
        lll_delta,
    )
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    carry, carry_invalid, carry_count = carry_sliced_marker_list_decode(
        n_bits,
        labels,
        target,
        low_bits,
        maximum_deviations,
        embedding_scale,
        low_constraint_scale,
        lll_delta,
    )
    return MarkerListTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        target_legal=witness_count > 0,
        exact_legal_witness_count=witness_count,
        constrained_low_bits=low_bits,
        reachable_carry_count=carry_count,
        standard_outcomes=standard,
        carry_sliced_outcomes=carry,
        invalid_witness_count=standard_invalid + carry_invalid,
        source_is_independent_uniform_target=True,
    )


def run_marker_aware_list_decoder(
    n_values: Sequence[int] = (10, 12, 14, 16),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 2,
    maximum_deviations: int = 2,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    seed: int = 0,
) -> DCPMarkerAwareListDecoderReport:
    if trials_per_row < 1 or maximum_deviations not in (0, 1, 2):
        raise ValueError("requires positive trials and maximum deviations in {0,1,2}")
    trials = [
        run_marker_list_trial(
            n_bits,
            offset,
            trial_index,
            maximum_deviations,
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
    rows: list[MarkerListScalingRow] = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            legal = [trial for trial in group if trial.target_legal]
            for depth in range(maximum_deviations + 1):
                standard_success = sum(
                    trial.standard_outcomes[depth].solved for trial in legal
                )
                carry_success = sum(
                    trial.carry_sliced_outcomes[depth].solved for trial in legal
                )
                standard_previous = sum(
                    trial.standard_outcomes[depth - 1].solved for trial in legal
                ) if depth else standard_success
                carry_previous = sum(
                    trial.carry_sliced_outcomes[depth - 1].solved for trial in legal
                ) if depth else carry_success
                rows.append(
                    MarkerListScalingRow(
                        n_bits=n_bits,
                        register_offset=offset,
                        branch_depth=depth,
                        trial_count=len(group),
                        legal_trial_count=len(legal),
                        standard_success_count=standard_success,
                        carry_sliced_success_count=carry_success,
                        standard_strict_improvement_count=standard_success - standard_previous,
                        carry_sliced_strict_improvement_count=carry_success - carry_previous,
                        standard_legal_coverage=(standard_success / len(legal) if legal else None),
                        carry_sliced_legal_coverage=(carry_success / len(legal) if legal else None),
                        mean_standard_candidate_count=sum(
                            trial.standard_outcomes[depth].candidate_count for trial in group
                        ) / len(group),
                        mean_carry_sliced_candidate_count=sum(
                            trial.carry_sliced_outcomes[depth].candidate_count for trial in group
                        ) / len(group),
                        fixed_depth_candidate_family_polynomial=True,
                        empirical_row_is_coverage_theorem=False,
                    )
                )
    tail_n = max(n_values)
    tail = [
        row
        for row in rows
        if row.n_bits == tail_n and row.branch_depth == maximum_deviations
    ]
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "maximum_n_bits": tail_n,
        "maximum_branch_depth": maximum_deviations,
        "exact_mitm_legality_trial_count": len(trials),
        "legal_trial_count": sum(trial.target_legal for trial in trials),
        "invalid_witness_count": sum(trial.invalid_witness_count for trial in trials),
        "candidate_count_theorem_failure_count": sum(
            not outcome.candidate_count_matches_theorem
            for trial in trials
            for outcome in (*trial.standard_outcomes, *trial.carry_sliced_outcomes)
        ),
        "fixed_depth_polynomial_list_theorem_count": 1,
        "standard_depth_zero_legal_success_count": sum(
            trial.target_legal and trial.standard_outcomes[0].solved for trial in trials
        ),
        "standard_max_depth_legal_success_count": sum(
            trial.target_legal and trial.standard_outcomes[-1].solved for trial in trials
        ),
        "carry_depth_zero_legal_success_count": sum(
            trial.target_legal and trial.carry_sliced_outcomes[0].solved for trial in trials
        ),
        "carry_max_depth_legal_success_count": sum(
            trial.target_legal and trial.carry_sliced_outcomes[-1].solved for trial in trials
        ),
        "strict_standard_list_improvement_count": sum(
            row.standard_strict_improvement_count for row in rows if row.branch_depth > 0
        ),
        "strict_carry_list_improvement_count": sum(
            row.carry_sliced_strict_improvement_count for row in rows if row.branch_depth > 0
        ),
        "tail_standard_success_count": sum(row.standard_success_count for row in tail),
        "tail_carry_success_count": sum(row.carry_sliced_success_count for row in tail),
        "tail_legal_trial_count": sum(row.legal_trial_count for row in tail),
        "fixed_depth_tail_collapse_observed_count": int(
            sum(row.standard_success_count for row in tail) == 0
            and sum(row.carry_sliced_success_count for row in tail) == 0
        ),
        "proved_inverse_polynomial_uniform_legal_coverage_count": 0,
        "proved_general_affine_cvp_lower_bound_count": 0,
    }
    finite_pressure = (
        metrics["standard_max_depth_legal_success_count"]
        + metrics["carry_max_depth_legal_success_count"]
        > 0
    )
    tail_collapse = bool(metrics["fixed_depth_tail_collapse_observed_count"])
    return DCPMarkerAwareListDecoderReport(
        created_at=utc_now(),
        decoder_contract={
            "source": "independent uniform labels and independent uniform target; condition on exact MITM legality only after sampling",
            "basis": "fixed standard and logarithmic-low-bit carry-sliced marker-zero kernels",
            "decoder": "LLL followed by every nearest-plane path with at most k in {0,1,2} one-step rounding deviations",
            "resource": "sum_{j<=k} 2^j binom(m,j), multiplied by O(n) reachable carries; polynomial for fixed k",
            "output": "every candidate is decoded and verified against the original modular equation",
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "source_contract_satisfied": True,
            "fixed_depth_candidate_family_polynomial": True,
            "every_returned_witness_verified": metrics["invalid_witness_count"] == 0,
            "finite_list_recovery_is_coverage_theorem": False,
            "fixed_depth_failure_is_general_affine_cvp_lower_bound": False,
            "inverse_polynomial_coverage_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The decoder is a legal polynomial classical attack for each fixed depth. Finite success is "
                "dequantization pressure; finite failure closes only this bounded-cell list, not marker-aware affine CVP."
            ),
        },
        status=(
            "fixed-depth-marker-list-tail-collapse-general-affine-route-open"
            if tail_collapse
            else "fixed-depth-marker-list-finite-classical-pressure-no-coverage-theorem"
            if finite_pressure
            else "fixed-depth-marker-list-no-finite-recovery-general-affine-route-open"
        ),
        summary=(
            f"Ran {len(trials)} exact-legality source trials through n={tail_n}; max-depth standard/carry successes="
            f"{metrics['standard_max_depth_legal_success_count']}/{metrics['carry_max_depth_legal_success_count']}, "
            f"strict list improvements={metrics['strict_standard_list_improvement_count']}/"
            f"{metrics['strict_carry_list_improvement_count']}, candidate-count theorem failures="
            f"{metrics['candidate_count_theorem_failure_count']}, tail standard/carry="
            f"{metrics['tail_standard_success_count']}/{metrics['tail_carry_success_count']} over "
            f"{metrics['tail_legal_trial_count']} legal trials; no source-coverage theorem."
        ),
        falsifiers_triggered=[
            "All targets are sampled independently before exact legality conditioning; no planted witness is used.",
            "Depth-zero reproduces the single-cell Babai baseline and deeper outcomes are nested.",
            "Every returned witness is checked against the original modulus and target.",
            "A fixed-depth list has polynomial size but is not automatically inverse-polynomially successful.",
            "Failure of depths one and two is not promoted to a lower bound against growing-depth or other affine-CVP decoders.",
        ],
    )


def register_marker_aware_list_decoder_payload(
    payload: dict,
    path: Path = DCP_MARKER_AWARE_LIST_DECODER_PATH,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> None:
    upsert_negative_result(
        NegativeResultRecord(
            id="NEG-DCP-FIXED-DEPTH-MARKER-LIST-IS-NOT-COVERAGE",
            source=str(path),
            claim=(
                "Polynomial size of a fixed-depth marker-aware nearest-plane list, or finite recovery within it, "
                "already proves inverse-polynomial uniform-legal subset-sum coverage."
            ),
            reason_invalid=(
                "The list-size theorem is deterministic, while source coverage remains an unproved probability "
                "statement; finite failures also say nothing about general affine-CVP decoders."
            ),
            lesson=(
                "Use the bounded list as a stronger classical falsifier, then derive a source-conditioned cell-mass "
                "theorem or change the decoder mechanism."
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
            artifacts={"dcp_marker_aware_list_decoder": str(path)},
        )
    )


def load_and_register_marker_aware_list_decoder(
    path: Path = DCP_MARKER_AWARE_LIST_DECODER_PATH,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    """Register an expensive existing sweep after deriving current headline fields."""
    payload = json.loads(path.read_text())
    metrics = payload["headline_metrics"]
    maximum_n = int(metrics["maximum_n_bits"])
    maximum_depth = int(metrics["maximum_branch_depth"])
    tail = [
        row
        for row in payload["rows"]
        if int(row["n_bits"]) == maximum_n
        and int(row["branch_depth"]) == maximum_depth
    ]
    tail_standard = sum(int(row["standard_success_count"]) for row in tail)
    tail_carry = sum(int(row["carry_sliced_success_count"]) for row in tail)
    tail_legal = sum(int(row["legal_trial_count"]) for row in tail)
    metrics["tail_standard_success_count"] = tail_standard
    metrics["tail_carry_success_count"] = tail_carry
    metrics["tail_legal_trial_count"] = tail_legal
    metrics["fixed_depth_tail_collapse_observed_count"] = int(
        tail_standard == 0 and tail_carry == 0
    )
    if metrics["fixed_depth_tail_collapse_observed_count"]:
        payload["status"] = "fixed-depth-marker-list-tail-collapse-general-affine-route-open"
    payload["summary"] = (
        f"Ran {metrics['trial_count']} exact-legality source trials through n={maximum_n}; max-depth standard/carry "
        f"successes={metrics['standard_max_depth_legal_success_count']}/"
        f"{metrics['carry_max_depth_legal_success_count']}, strict list improvements="
        f"{metrics['strict_standard_list_improvement_count']}/"
        f"{metrics['strict_carry_list_improvement_count']}, candidate-count theorem failures="
        f"{metrics['candidate_count_theorem_failure_count']}, tail standard/carry={tail_standard}/{tail_carry} "
        f"over {tail_legal} legal trials; no source-coverage theorem."
    )
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    register_marker_aware_list_decoder_payload(
        payload,
        path,
        registry_experiment_id,
        registry_candidate_id,
        registry_result_id,
    )
    return payload


def write_marker_aware_list_decoder(
    path: Path = DCP_MARKER_AWARE_LIST_DECODER_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict:
    payload = asdict(run_marker_aware_list_decoder(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        register_marker_aware_list_decoder_payload(
            payload,
            path,
            registry_experiment_id,
            registry_candidate_id,
            registry_result_id,
        )
    return payload


if __name__ == "__main__":
    print(json.dumps(write_marker_aware_list_decoder()["headline_metrics"], indent=2, sort_keys=True))
