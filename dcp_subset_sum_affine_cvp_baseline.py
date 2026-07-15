"""Marker-aware affine-CVP baselines for density-one modular subset sum.

The full embedding is split into its marker-zero kernel rows and target row.
LLL reduces the kernel, and exact-rational Babai nearest plane finds a kernel
vector near the target row.  Their difference lies in the marker-minus-one
affine coset by construction.  Standard and carry-sliced variants are compared
on uniform source targets with exact witness verification.

This is a serious classical baseline for the marker-coset theorem, not a solver
claim.  Finite success does not establish inverse-polynomial legal coverage;
failure does not prove an affine-CVP lower bound.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from sympy import Matrix

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
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


DCP_SUBSET_SUM_AFFINE_CVP_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_affine_cvp_baseline.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-BASELINE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class AffineCVPDiagnostics:
    vector: list[int]
    distance_squared: int
    witness_radius_squared: int
    within_witness_radius: bool
    constraint_coordinate_norm_squared: int
    binary_coordinate_defect: int
    marker_coordinate: int
    reduced_kernel_row_count: int
    maximum_babai_coefficient_bit_length: int


@dataclass(frozen=True)
class AffineCVPTrial:
    n_bits: int
    register_offset: int
    register_count: int
    constrained_low_bits: int
    trial_index: int
    target_legal: bool
    legal_witness_count: int
    standard_solved: bool
    standard_witness_valid: bool
    standard_diagnostics: AffineCVPDiagnostics
    reachable_carry_count: int
    carry_sliced_solved: bool
    carry_sliced_witness_valid: bool
    winning_carry: int | None
    carry_sliced_diagnostics: AffineCVPDiagnostics


@dataclass(frozen=True)
class AffineCVPScalingRow:
    n_bits: int
    register_offset: int
    trial_count: int
    legal_trial_count: int
    standard_success_count: int
    carry_sliced_success_count: int
    standard_legal_coverage: float | None
    carry_sliced_legal_coverage: float | None
    invalid_witness_count: int
    mean_standard_distance_ratio: float
    mean_carry_sliced_distance_ratio: float
    standard_zero_constraint_count: int
    carry_sliced_zero_constraint_count: int
    uniform_inverse_polynomial_coverage_proved: bool
    finite_row_is_scaling_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumAffineCVPReport:
    created_at: str
    baseline_contract: dict[str, str]
    rows: list[AffineCVPScalingRow]
    trials: list[AffineCVPTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _nearest_integer(value: Fraction) -> int:
    # Half-up is translation invariant: round(x+k)=round(x)+k for integral k.
    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def _dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def exact_gram_schmidt_rows(basis: Matrix) -> list[list[Fraction]]:
    """Return exact row-wise Gram-Schmidt vectors for a full-row-rank basis."""
    rows = [[Fraction(int(value)) for value in row] for row in basis.tolist()]
    if not rows:
        raise ValueError("basis must be nonempty")
    orthogonal: list[list[Fraction]] = []
    for row in rows:
        star = list(row)
        for prior in orthogonal:
            norm = _dot(prior, prior)
            if norm == 0:
                raise ValueError("basis rows are linearly dependent")
            projection = _dot(row, prior) / norm
            star = [value - projection * base for value, base in zip(star, prior)]
        if _dot(star, star) == 0:
            raise ValueError("basis rows are linearly dependent")
        orthogonal.append(star)
    return orthogonal


def exact_babai_nearest_plane(
    basis: Matrix,
    target: Sequence[int],
) -> tuple[list[int], list[int]]:
    """Return a row-lattice vector near target using exact Gram-Schmidt."""
    rows = [[Fraction(int(value)) for value in row] for row in basis.tolist()]
    if not rows or len(rows[0]) != len(target):
        raise ValueError("basis and target dimensions are incompatible")
    orthogonal = exact_gram_schmidt_rows(basis)

    residual = [Fraction(int(value)) for value in target]
    coefficients = [0] * len(rows)
    for index in range(len(rows) - 1, -1, -1):
        star = orthogonal[index]
        coefficient = _nearest_integer(_dot(residual, star) / _dot(star, star))
        coefficients[index] = coefficient
        residual = [
            value - coefficient * base for value, base in zip(residual, rows[index])
        ]
    closest = [Fraction(int(value)) - remainder for value, remainder in zip(target, residual)]
    if any(value.denominator != 1 for value in closest):
        raise ArithmeticError("Babai output left the integer lattice")
    return [int(value) for value in closest], coefficients


def babai_zero_cell_margin(
    basis: Matrix,
    error: Sequence[int],
) -> tuple[bool, float, float]:
    """Audit whether nearest plane maps an error to zero and its smallest half-cell margin."""
    rows = [[Fraction(int(value)) for value in row] for row in basis.tolist()]
    if not rows or len(rows[0]) != len(error):
        raise ValueError("basis and error dimensions are incompatible")
    orthogonal = exact_gram_schmidt_rows(basis)
    residual = [Fraction(int(value)) for value in error]
    margins: list[Fraction] = []
    returned_zero = True
    maximum_absolute_coordinate = Fraction(0)
    for index in range(len(rows) - 1, -1, -1):
        star = orthogonal[index]
        coordinate = _dot(residual, star) / _dot(star, star)
        maximum_absolute_coordinate = max(maximum_absolute_coordinate, abs(coordinate))
        margins.append(Fraction(1, 2) - abs(coordinate))
        coefficient = _nearest_integer(coordinate)
        if coefficient:
            returned_zero = False
            residual = [
                value - coefficient * base
                for value, base in zip(residual, rows[index])
            ]
    return returned_zero, float(min(margins)), float(maximum_absolute_coordinate)


def _diagnostics(
    vector: Sequence[int],
    register_count: int,
    constraint_coordinate_count: int,
    coefficients: Sequence[int],
    reduced_kernel_row_count: int,
) -> AffineCVPDiagnostics:
    distance = sum(int(value) ** 2 for value in vector)
    radius = register_count + 1
    binary = vector[:register_count]
    constraints = vector[register_count : register_count + constraint_coordinate_count]
    return AffineCVPDiagnostics(
        vector=[int(value) for value in vector],
        distance_squared=distance,
        witness_radius_squared=radius,
        within_witness_radius=distance <= radius,
        constraint_coordinate_norm_squared=sum(int(value) ** 2 for value in constraints),
        binary_coordinate_defect=sum(
            min(abs(int(value) - 1), abs(int(value) + 1)) for value in binary
        ),
        marker_coordinate=int(vector[-1]),
        reduced_kernel_row_count=reduced_kernel_row_count,
        maximum_babai_coefficient_bit_length=max(
            (abs(int(value)).bit_length() for value in coefficients), default=0
        ),
    )


def standard_affine_babai(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
) -> tuple[list[int] | None, AffineCVPDiagnostics]:
    full = modular_subset_sum_embedding(labels, target, 1 << n_bits, embedding_scale)
    rows = full.tolist()
    kernel = Matrix([row[:-1] for row in rows[:-1]])
    target_row = rows[-1][:-1]
    reduced = kernel.lll(delta=lll_delta)
    closest, coefficients = exact_babai_nearest_plane(reduced, target_row)
    vector = [value - int(base) for value, base in zip(closest, target_row)] + [-1]
    diagnostics = _diagnostics(vector, len(labels), 1, coefficients, reduced.rows)
    witness = decode_short_standard_marker_vector(
        vector, labels, target, 1 << n_bits
    )
    return witness, diagnostics


def carry_sliced_affine_babai(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    low_bits: int,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
) -> tuple[list[int] | None, int | None, int, AffineCVPDiagnostics]:
    carries = reachable_carries(labels, target, low_bits)
    best: AffineCVPDiagnostics | None = None
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
        )
        rows = full.tolist()
        kernel = Matrix([row[:-1] for row in rows[:-1]])
        target_row = rows[-1][:-1]
        reduced = kernel.lll(delta=lll_delta)
        closest, coefficients = exact_babai_nearest_plane(reduced, target_row)
        vector = [value - int(base) for value, base in zip(closest, target_row)] + [-1]
        diagnostics = _diagnostics(vector, len(labels), 2, coefficients, reduced.rows)
        witness = decode_carry_sliced_vector(
            vector, labels, target, n_bits, low_bits, carry
        )
        if witness is not None:
            return witness, carry, len(carries), diagnostics
        if best is None or diagnostics.distance_squared < best.distance_squared:
            best = diagnostics
            winning_carry = carry
    if best is None:
        empty = [3] * len(labels) + [0, 0, -1]
        best = _diagnostics(empty, len(labels), 2, [], 0)
    return None, winning_carry, len(carries), best


def run_affine_cvp_trial(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
    trial_index: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    seed: int,
) -> AffineCVPTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    legal_count = int(subset_sum_counts(n_bits, labels)[target])
    standard_witness, standard_diagnostics = standard_affine_babai(
        n_bits, labels, target, embedding_scale, lll_delta
    )
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    sliced_witness, winning_carry, carry_count, sliced_diagnostics = (
        carry_sliced_affine_babai(
            n_bits,
            labels,
            target,
            low_bits,
            embedding_scale,
            low_constraint_scale,
            lll_delta,
        )
    )
    standard_valid = standard_witness is not None and sum(
        label * bit for label, bit in zip(labels, standard_witness)
    ) % modulus == target
    sliced_valid = sliced_witness is not None and sum(
        label * bit for label, bit in zip(labels, sliced_witness)
    ) % modulus == target
    return AffineCVPTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        constrained_low_bits=low_bits,
        trial_index=trial_index,
        target_legal=legal_count > 0,
        legal_witness_count=legal_count,
        standard_solved=standard_witness is not None,
        standard_witness_valid=standard_valid,
        standard_diagnostics=standard_diagnostics,
        reachable_carry_count=carry_count,
        carry_sliced_solved=sliced_witness is not None,
        carry_sliced_witness_valid=sliced_valid,
        winning_carry=winning_carry,
        carry_sliced_diagnostics=sliced_diagnostics,
    )


def run_affine_cvp_baseline(
    n_values: Sequence[int] = (8, 10, 12, 14),
    register_offsets: Sequence[int] = (2,),
    log_multiplier: int = 1,
    trials_per_row: int = 3,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    seed: int = 0,
) -> DCPSubsetSumAffineCVPReport:
    if trials_per_row < 1:
        raise ValueError("trials per row must be positive")
    trials = [
        run_affine_cvp_trial(
            n_bits,
            offset,
            log_multiplier,
            trial_index,
            embedding_scale,
            low_constraint_scale,
            lll_delta,
            seed + 1_000_003 * n_index + 10_007 * offset_index + trial_index,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for trial_index in range(trials_per_row)
    ]
    rows: list[AffineCVPScalingRow] = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            legal = [trial for trial in group if trial.target_legal]
            standard_success = sum(trial.standard_solved for trial in legal)
            sliced_success = sum(trial.carry_sliced_solved for trial in legal)
            rows.append(
                AffineCVPScalingRow(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_count=len(group),
                    legal_trial_count=len(legal),
                    standard_success_count=standard_success,
                    carry_sliced_success_count=sliced_success,
                    standard_legal_coverage=(standard_success / len(legal) if legal else None),
                    carry_sliced_legal_coverage=(sliced_success / len(legal) if legal else None),
                    invalid_witness_count=sum(
                        trial.standard_solved and not trial.standard_witness_valid
                        or trial.carry_sliced_solved and not trial.carry_sliced_witness_valid
                        for trial in group
                    ),
                    mean_standard_distance_ratio=sum(
                        trial.standard_diagnostics.distance_squared
                        / trial.standard_diagnostics.witness_radius_squared
                        for trial in group
                    )
                    / len(group),
                    mean_carry_sliced_distance_ratio=sum(
                        trial.carry_sliced_diagnostics.distance_squared
                        / trial.carry_sliced_diagnostics.witness_radius_squared
                        for trial in group
                    )
                    / len(group),
                    standard_zero_constraint_count=sum(
                        trial.standard_diagnostics.constraint_coordinate_norm_squared == 0
                        for trial in group
                    ),
                    carry_sliced_zero_constraint_count=sum(
                        trial.carry_sliced_diagnostics.constraint_coordinate_norm_squared == 0
                        for trial in group
                    ),
                    uniform_inverse_polynomial_coverage_proved=False,
                    finite_row_is_scaling_theorem=False,
                )
            )
    legal_trials = [trial for trial in trials if trial.target_legal]
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "legal_trial_count": len(legal_trials),
        "standard_legal_success_count": sum(trial.standard_solved for trial in legal_trials),
        "carry_sliced_legal_success_count": sum(
            trial.carry_sliced_solved for trial in legal_trials
        ),
        "invalid_witness_count": sum(row.invalid_witness_count for row in rows),
        "marker_coset_enforced_trial_count": sum(
            trial.standard_diagnostics.marker_coordinate == -1
            and trial.carry_sliced_diagnostics.marker_coordinate == -1
            for trial in trials
        ),
        "tail_standard_success_count": sum(row.standard_success_count for row in tail),
        "tail_carry_sliced_success_count": sum(row.carry_sliced_success_count for row in tail),
        "proved_uniform_inverse_polynomial_coverage_count": 0,
        "proved_affine_cvp_scaling_advantage_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumAffineCVPReport(
        created_at=utc_now(),
        baseline_contract={
            "source": "independent uniform labels and independent uniform targets modulo 2^n",
            "algorithm": "exact-rational Babai nearest plane after LLL reduction of the marker-zero kernel",
            "models": "standard affine coset and every reachable logarithmic carry slice",
            "verification": "binary witness checked against the original full modular equation",
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "marker_coset_enforced": metrics["marker_coset_enforced_trial_count"] == len(trials),
            "finite_success_is_coverage_theorem": False,
            "inverse_polynomial_legal_coverage_proved": False,
            "scaling_advantage_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Babai is a legal marker-aware classical baseline, but finite exact trials neither prove coverage nor "
                "exclude stronger affine-CVP algorithms."
            ),
        },
        status="finite-affine-cvp-baseline-no-coverage-theorem",
        summary=(
            f"Ran {len(trials)} exact marker-coset Babai trials; standard/carry legal successes="
            f"{metrics['standard_legal_success_count']}/{metrics['carry_sliced_legal_success_count']}, tail="
            f"{metrics['tail_standard_success_count']}/{metrics['tail_carry_sliced_success_count']}; no scaling or "
            "inverse-polynomial coverage theorem."
        ),
        falsifiers_triggered=[
            "Marker-aware nearest plane has no proved inverse-polynomial legal coverage.",
            "Finite successes are not an asymptotic affine-CVP advantage.",
            "Finite failures are not a lower bound against stronger decoders.",
            "Every returned witness is checked against the original source equation.",
        ],
    )


def write_affine_cvp_baseline(
    path: Path = DCP_SUBSET_SUM_AFFINE_CVP_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs,
) -> dict:
    payload = asdict(run_affine_cvp_baseline(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-AFFINE-BABAI-FINITE-WITHOUT-COVERAGE",
                source=str(path),
                claim="Finite marker-aware Babai success establishes a density-one partial subset-sum solver.",
                reason_invalid=(
                    "The baseline has exact verification but no inverse-polynomial legal source-coverage or scaling theorem."
                ),
                lesson=(
                    "Use it as a classical attack and diagnostic. Require a source-conditioned BDD radius theorem before "
                    "promoting any affine-CVP mutation."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-AFFINE-CVP-BASELINE"
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
                artifacts={"dcp_subset_sum_affine_cvp_baseline": str(path)},
            )
        )
    return payload
