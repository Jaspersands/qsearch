"""Exact low-bit decision-diagram workbench for modular subset sum."""

from __future__ import annotations

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


DCP_SUBSET_SUM_LOW_BIT_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_low_bit_bdd.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-LOW-BIT-BDD"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class LowBitBDDRow:
    n_bits: int
    register_count: int
    register_offset: int
    log_multiplier: int
    constrained_low_bits: int
    trial_index: int
    modulus_state_count: int
    maximum_reachable_width: int
    final_reachable_residue_count: int
    accepted_assignment_count: int
    accepted_assignment_log2: float | None
    expected_assignment_log2: float
    acceptance_log2_ratio_to_uniform: float | None
    representation_polynomial_in_n: bool
    exact_completion_count_bit_length: int
    residual_witness_entropy_is_linear: bool
    source_contract_satisfied: bool


@dataclass(frozen=True)
class LowBitBDDTheoremCertificate:
    n_bits: int
    register_offset: int
    log_multiplier: int
    constrained_low_bits: int
    width_upper_bound: int
    polynomial_width_upper_bound: int
    residual_assignment_log2_expectation: float
    residual_entropy_linear: bool
    exact_bdd_polynomial_size_proved: bool
    exact_uniform_low_fiber_state_preparation_polynomial_proved: bool
    full_subset_sum_solver_implied: bool
    statement: str


@dataclass(frozen=True)
class DCPSubsetSumLowBitBDDReport:
    created_at: str
    representation_contract: dict[str, str]
    rows: list[LowBitBDDRow]
    theorem_certificates: list[LowBitBDDTheoremCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def subset_sum_residue_counts(labels: Sequence[int], modulus: int) -> tuple[list[int], list[int]]:
    if modulus < 2 or modulus & (modulus - 1):
        raise ValueError("modulus must be a power of two")
    if not labels:
        raise ValueError("labels must be nonempty")
    counts = [0] * modulus
    counts[0] = 1
    widths: list[int] = []
    for label in labels:
        shift = int(label) % modulus
        updated = counts.copy()
        for residue, count in enumerate(counts):
            if count:
                updated[(residue + shift) % modulus] += count
        counts = updated
        widths.append(sum(count > 0 for count in counts))
    return counts, widths


def _constrained_bits(n_bits: int, multiplier: int) -> int:
    return min(n_bits, max(1, math.ceil(multiplier * math.log2(max(2, n_bits)))))


def low_bit_bdd_theorem_certificate(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
) -> LowBitBDDTheoremCertificate:
    constrained = _constrained_bits(n_bits, log_multiplier)
    width = 1 << constrained
    polynomial_bound = 2 * n_bits**log_multiplier
    residual = n_bits + register_offset - constrained
    return LowBitBDDTheoremCertificate(
        n_bits=n_bits,
        register_offset=register_offset,
        log_multiplier=log_multiplier,
        constrained_low_bits=constrained,
        width_upper_bound=width,
        polynomial_width_upper_bound=polynomial_bound,
        residual_assignment_log2_expectation=float(residual),
        residual_entropy_linear=residual >= n_bits / 2,
        exact_bdd_polynomial_size_proved=width <= polynomial_bound,
        exact_uniform_low_fiber_state_preparation_polynomial_proved=width <= polynomial_bound,
        full_subset_sum_solver_implied=False,
        statement=(
            "Tracking the running residue modulo 2^b gives an exact ordered branching program of width at most 2^b. "
            "For b=ceil(c log2 n), width <=2 n^c and forward/backward completion counts have O(n) bits, so exact "
            "conditional sampling or reversible state preparation is polynomial. The remaining fiber has expected "
            "2^(n+offset-b) assignments and this theorem alone gives no high-bit witness algorithm."
        ),
    )


def analyze_low_bit_bdd_instance(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
    trial_index: int,
    seed: int,
) -> LowBitBDDRow:
    register_count = n_bits + register_offset
    constrained = _constrained_bits(n_bits, log_multiplier)
    low_modulus = 1 << constrained
    full_modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [rng.randrange(full_modulus) for _ in range(register_count)]
    target = rng.randrange(full_modulus)
    counts, widths = subset_sum_residue_counts(labels, low_modulus)
    accepted = counts[target % low_modulus]
    accepted_log2 = math.log2(accepted) if accepted else None
    expected_log2 = register_count - constrained
    ratio = accepted_log2 - expected_log2 if accepted_log2 is not None else None
    certificate = low_bit_bdd_theorem_certificate(n_bits, register_offset, log_multiplier)
    return LowBitBDDRow(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        log_multiplier=log_multiplier,
        constrained_low_bits=constrained,
        trial_index=trial_index,
        modulus_state_count=low_modulus,
        maximum_reachable_width=max(widths),
        final_reachable_residue_count=widths[-1],
        accepted_assignment_count=accepted,
        accepted_assignment_log2=accepted_log2,
        expected_assignment_log2=float(expected_log2),
        acceptance_log2_ratio_to_uniform=ratio,
        representation_polynomial_in_n=certificate.exact_bdd_polynomial_size_proved,
        exact_completion_count_bit_length=max(counts).bit_length(),
        residual_witness_entropy_is_linear=certificate.residual_entropy_linear,
        source_contract_satisfied=False,
    )


def run_subset_sum_low_bit_bdd_audit(
    n_values: Sequence[int] = (16, 32, 64, 128),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1, 2),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPSubsetSumLowBitBDDReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    certificates = [
        low_bit_bdd_theorem_certificate(n_bits, offset, multiplier)
        for n_bits in n_values
        for offset in register_offsets
        for multiplier in log_multipliers
    ]
    rows = [
        analyze_low_bit_bdd_instance(
            n_bits,
            offset,
            multiplier,
            trial,
            seed + 1_000_003 * n_index + 10_007 * offset_index + 101 * multiplier_index + trial,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for multiplier_index, multiplier in enumerate(log_multipliers)
        for trial in range(trials_per_row)
    ]
    ratios = [row.acceptance_log2_ratio_to_uniform for row in rows if row.acceptance_log2_ratio_to_uniform is not None]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "theorem_certificate_count": len(certificates),
        "polynomial_width_certificate_count": sum(item.exact_bdd_polynomial_size_proved for item in certificates),
        "polynomial_state_preparation_certificate_count": sum(
            item.exact_uniform_low_fiber_state_preparation_polynomial_proved for item in certificates
        ),
        "linear_residual_entropy_certificate_count": sum(item.residual_entropy_linear for item in certificates),
        "zero_accepted_fiber_row_count": sum(row.accepted_assignment_count == 0 for row in rows),
        "mean_acceptance_log2_ratio_to_uniform": sum(ratios) / len(ratios) if ratios else 0.0,
        "maximum_reachable_width": max(row.maximum_reachable_width for row in rows),
        "maximum_completion_count_bit_length": max(row.exact_completion_count_bit_length for row in rows),
        "proved_high_bit_geometry_improvement_count": 0,
        "proved_polynomial_witness_solver_count": 0,
        "proved_uniform_inverse_polynomial_coverage_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumLowBitBDDReport(
        created_at=utc_now(),
        representation_contract={
            "constraint": "sum_i a_i x_i = t modulo 2^b for b=ceil(c log2 n)",
            "state": "running low-bit residue; transition either keeps residue or adds public a_i",
            "size": "O(n 2^b) states and O(n)-bit exact completion counts",
            "quantum_use": "backward completion counts permit reversible conditional branch rotations to prepare the uniform low-bit-valid fiber",
            "remaining_problem": "find a witness satisfying the remaining n-b high bits without enumerating 2^(n-O(log n)) assignments",
        },
        rows=rows,
        theorem_certificates=certificates,
        headline_metrics=metrics,
        claim_gate={
            "exact_polynomial_low_bit_bdd_proved": metrics["polynomial_width_certificate_count"] == len(certificates),
            "exact_polynomial_low_fiber_state_preparation_proved": (
                metrics["polynomial_state_preparation_certificate_count"] == len(certificates)
            ),
            "low_bit_conditioning_improves_high_bit_lattice_geometry_proved": False,
            "full_subset_sum_solver_constructed": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The O(log n)-bit congruence fiber has an exact polynomial branching program and state-preparation route, "
                "but expected residual witness entropy remains Theta(n) and no high-bit solver or geometry theorem exists."
            ),
        },
        status="polynomial-low-bit-fiber-representation-proved-high-bit-solver-open",
        summary=(
            f"Built {len(rows)} low-bit BDD instances and {len(certificates)} theorem certificates; polynomial width/state "
            f"preparation certificates={metrics['polynomial_width_certificate_count']}/"
            f"{metrics['polynomial_state_preparation_certificate_count']}, linear-residual certificates="
            f"{metrics['linear_residual_entropy_certificate_count']}, and source-contract rows=0."
        ),
        falsifiers_triggered=[
            "Low-bit BDD compactness is a proved positive representation result, not a full subset-sum algorithm.",
            "Constraining O(log n) bits leaves 2^(n-O(log n)) expected valid assignments before high-bit solving.",
            "Polynomial conditional state preparation does not imply a polynomial measurement or witness decoder.",
            "Any preconditioned lattice claim must prove changed average-case short-vector geometry and tail coverage.",
            "Taking b=Theta(n) restores exponential width and is not a polynomial extension of this theorem.",
        ],
    )


def write_subset_sum_low_bit_bdd_audit(
    path: Path = DCP_SUBSET_SUM_LOW_BIT_BDD_PATH,
    n_values: Sequence[int] = (16, 32, 64, 128),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1, 2),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_low_bit_bdd_audit(
        n_values, register_offsets, log_multipliers, trials_per_row, seed
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-POLYNOMIAL-LOW-BIT-BDD-AS-FULL-SUBSET-SUM-SOLVER",
                source=str(path),
                claim="A polynomial BDD for O(log n) low subset-sum bits is already a polynomial density-one witness solver.",
                reason_invalid="The exact representation leaves Theta(n) residual witness entropy and no high-bit geometry or decoding theorem.",
                lesson="Retain the low-bit BDD as a proved preconditioning/state-preparation primitive. Demand a separate high-bit solver and coverage theorem.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "polynomial_width_certificate_count": payload["headline_metrics"]["polynomial_width_certificate_count"],
                    "linear_residual_entropy_certificate_count": payload["headline_metrics"]["linear_residual_entropy_certificate_count"],
                    "proved_polynomial_witness_solver_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-LOW-BIT-BDD"
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
                artifacts={"dcp_subset_sum_low_bit_bdd": str(path)},
            )
        )
    return payload
