"""Fourier obstruction and target-fiber balance audit for 2-adic transport.

Let C_r count assignments with subset sum r modulo M=2^(k+1).  Any
bijection of the entire Boolean cube satisfying S_A(Tx)=S_A(x)+M/2 forces
C_r=C_{r+M/2} for every r.  The first Fourier coefficient then vanishes, but

    sum_x omega^S_A(x) = product_j (1 + omega^A_j).

Hence some A_j=M/2 modulo M.  Conversely, flipping that coordinate is such a
bijection.  This exactly closes every total all-assignment transport class,
including nonlinear maps, at depths where the exact-valuation pivot is absent.

Target-dependent maps on one low-bit fiber are different.  A total bijection
between its two children exists exactly when their multiplicities agree; a
partial pairing can cover 2*min(C_t,C_{t+M/2}) assignments.  The finite audit
measures those quantities without claiming an efficient map or an asymptotic
anti-concentration theorem.
"""

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


DCP_FIBER_BALANCE_OBSTRUCTION_PATH = Path(
    "research/phase_workbench/dcp_fiber_balance_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-FIBER-BALANCE-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class GlobalTransportFourierTheorem:
    theorem_id: str
    statement: str
    forward_step: str
    factorization_step: str
    zero_factor_step: str
    converse: str
    necessary_and_sufficient: bool
    scope: str


@dataclass(frozen=True)
class FiberBalanceRow:
    n_bits: int
    register_count: int
    depth: int
    trial_index: int
    supported_low_target_count: int
    exactly_balanced_target_count: int
    uniform_supported_balanced_target_fraction: float
    subset_sample_weighted_balanced_target_fraction: float
    optimal_partial_pairing_mass_fraction: float
    minimum_supported_target_partial_pairing_fraction: float
    maximum_child_imbalance_fraction: float
    exact_valuation_pivot_present: bool
    all_supported_targets_balanced: bool
    total_global_transport_exists: bool
    polynomial_target_fiber_map_constructed: bool


@dataclass(frozen=True)
class FiberBalanceObstructionReport:
    created_at: str
    theorem: GlobalTransportFourierTheorem
    rows: list[FiberBalanceRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def subset_sum_multiplicities(labels: Sequence[int], depth: int) -> list[int]:
    modulus = 1 << (depth + 1)
    counts = [0] * modulus
    for assignment in range(1 << len(labels)):
        value = sum(
            label
            for index, label in enumerate(labels)
            if (assignment >> index) & 1
        )
        counts[value % modulus] += 1
    return counts


def pivot_present(labels: Sequence[int], depth: int) -> bool:
    modulus = 1 << (depth + 1)
    half = 1 << depth
    return any(label % modulus == half for label in labels)


def all_child_counts_balanced(counts: Sequence[int]) -> bool:
    if len(counts) < 2 or len(counts) & (len(counts) - 1):
        raise ValueError("count vector length must be a power of two")
    half = len(counts) // 2
    return all(counts[target] == counts[target + half] for target in range(half))


def total_global_transport_exists(labels: Sequence[int], depth: int) -> bool:
    """Exact Fourier classification, returned in its closed pivot form."""
    return pivot_present(labels, depth)


def target_fiber_pairing_fraction(
    counts: Sequence[int], low_target: int
) -> float:
    half = len(counts) // 2
    left = counts[low_target]
    right = counts[low_target + half]
    total = left + right
    return 2.0 * min(left, right) / total if total else 0.0


def build_fourier_theorem() -> GlobalTransportFourierTheorem:
    return GlobalTransportFourierTheorem(
        theorem_id="THEOREM-DCP-TOTAL-TRANSPORT-FOURIER-COLLAPSE",
        statement=(
            "A bijection T on {0,1}^m with S_A(Tx)=S_A(x)+2^k modulo 2^(k+1) for every x exists "
            "if and only if some A_j=2^k modulo 2^(k+1)."
        ),
        forward_step=(
            "The bijection pairs every residue r with r+2^k, so multiplicities satisfy C_r=C_{r+2^k}."
        ),
        factorization_step=(
            "For omega=exp(2*pi*i/2^(k+1)), half-periodicity gives sum_r C_r omega^r=0, while independent "
            "Boolean coordinates factor this sum as product_j(1+omega^A_j)."
        ),
        zero_factor_step=(
            "A finite complex product is zero only if one factor vanishes; 1+omega^A_j=0 exactly when "
            "A_j=2^k modulo 2^(k+1)."
        ),
        converse=(
            "If A_j=2^k, complementing coordinate j is a total involution and changes every subset sum by 2^k."
        ),
        necessary_and_sufficient=True,
        scope=(
            "All total bijections on the full Boolean cube, regardless of circuit class. Target-dependent maps on "
            "one fiber, partial maps, and non-bijective relation samplers are not covered."
        ),
    )


def analyze_fiber_balance(
    n_bits: int,
    register_offset: int,
    depth: int,
    trial_index: int,
    seed: int,
) -> FiberBalanceRow:
    if not 1 <= depth < n_bits:
        raise ValueError("depth must satisfy 1 <= depth < n_bits")
    register_count = n_bits + register_offset
    if register_count > 20:
        raise ValueError("exact multiplicity enumeration is capped at 20 registers")
    rng = random.Random(seed)
    labels = [rng.randrange(1 << n_bits) for _ in range(register_count)]
    counts = subset_sum_multiplicities(labels, depth)
    half = 1 << depth
    supported = [
        target
        for target in range(half)
        if counts[target] + counts[target + half] > 0
    ]
    balanced = [
        target
        for target in supported
        if counts[target] == counts[target + half]
    ]
    total_assignments = 1 << register_count
    weighted_balanced_mass = sum(
        counts[target] + counts[target + half] for target in balanced
    ) / total_assignments
    pairing_fractions = [target_fiber_pairing_fraction(counts, target) for target in supported]
    paired_mass = sum(
        2 * min(counts[target], counts[target + half]) for target in supported
    ) / total_assignments
    imbalance_fractions = [1.0 - value for value in pairing_fractions]
    pivot = pivot_present(labels, depth)
    all_balanced = all_child_counts_balanced(counts)
    return FiberBalanceRow(
        n_bits=n_bits,
        register_count=register_count,
        depth=depth,
        trial_index=trial_index,
        supported_low_target_count=len(supported),
        exactly_balanced_target_count=len(balanced),
        uniform_supported_balanced_target_fraction=(
            len(balanced) / len(supported) if supported else 0.0
        ),
        subset_sample_weighted_balanced_target_fraction=weighted_balanced_mass,
        optimal_partial_pairing_mass_fraction=paired_mass,
        minimum_supported_target_partial_pairing_fraction=min(
            pairing_fractions, default=0.0
        ),
        maximum_child_imbalance_fraction=max(imbalance_fractions, default=0.0),
        exact_valuation_pivot_present=pivot,
        all_supported_targets_balanced=all_balanced,
        total_global_transport_exists=total_global_transport_exists(labels, depth),
        polynomial_target_fiber_map_constructed=False,
    )


def _default_depths(n_bits: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                min(n_bits - 1, max(1, math.ceil(math.log2(n_bits)))),
                max(1, n_bits // 2),
                n_bits - 1,
            }
        )
    )


def run_fiber_balance_obstruction_audit(
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    register_offset: int = 2,
    trials_per_depth: int = 2,
    seed: int = 0,
) -> FiberBalanceObstructionReport:
    rows = [
        analyze_fiber_balance(
            n_bits,
            register_offset,
            depth,
            trial,
            seed + 1_000_003 * n_index + 10_007 * depth + trial,
        )
        for n_index, n_bits in enumerate(n_values)
        for depth in _default_depths(n_bits)
        for trial in range(trials_per_depth)
    ]
    theorem_mismatches = sum(
        row.exact_valuation_pivot_present != row.all_supported_targets_balanced
        or row.total_global_transport_exists != row.exact_valuation_pivot_present
        for row in rows
    )
    linear_rows = [row for row in rows if row.depth >= row.n_bits // 2]
    metrics: dict[str, int | float] = {
        "exact_total_transport_fourier_theorem_count": 1,
        "finite_theorem_mismatch_count": theorem_mismatches,
        "row_count": len(rows),
        "linear_depth_row_count": len(linear_rows),
        "linear_depth_pivot_row_count": sum(
            row.exact_valuation_pivot_present for row in linear_rows
        ),
        "maximum_linear_depth_uniform_balanced_target_fraction_without_pivot": max(
            (
                row.uniform_supported_balanced_target_fraction
                for row in linear_rows
                if not row.exact_valuation_pivot_present
            ),
            default=0.0,
        ),
        "minimum_linear_depth_optimal_partial_pairing_mass": min(
            (row.optimal_partial_pairing_mass_fraction for row in linear_rows),
            default=0.0,
        ),
        "maximum_linear_depth_optimal_partial_pairing_mass": max(
            (row.optimal_partial_pairing_mass_fraction for row in linear_rows),
            default=0.0,
        ),
        "proved_polynomial_target_fiber_map_count": 0,
        "proved_polynomial_relation_solver_count": 0,
    }
    return FiberBalanceObstructionReport(
        created_at=utc_now(),
        theorem=build_fourier_theorem(),
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "total_global_transport_class_closed_without_pivot": theorem_mismatches == 0,
            "target_fiber_partial_transport_route_alive": True,
            "set_theoretic_pairing_is_algorithmic_evidence": False,
            "polynomial_target_fiber_map_constructed": False,
            "polynomial_relation_solver_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The Fourier factorization closes every total full-cube transport beyond the exact-valuation pivot. "
                "Target-fiber partial pairing can retain large set-theoretic mass, but no efficient source-uniform map, "
                "state preparation, or classical separation is constructed."
            ),
        },
        status="total-global-transport-closed-target-fiber-partial-route-open",
        summary=(
            f"Proved the total-transport Fourier collapse and checked {len(rows)} exact source rows with "
            f"{theorem_mismatches} theorem mismatches. Linear-depth pivot rows="
            f"{metrics['linear_depth_pivot_row_count']}/{len(linear_rows)}; polynomial target-fiber maps=0."
        ),
        falsifiers_triggered=[
            "No nonlinear or otherwise implicit full-cube bijection can evade the exact-valuation pivot theorem.",
            "A balanced finite target fiber proves only set-theoretic bijection existence, not an efficient map.",
            "Large optimal partial-pairing mass does not provide a circuit for finding or pairing witnesses.",
            "Uniform-supported-target and subset-sample-weighted balance are recorded separately.",
            "The theorem does not close target-dependent partial maps or non-bijective relation samplers.",
        ],
    )


def write_fiber_balance_obstruction_audit(
    path: Path = DCP_FIBER_BALANCE_OBSTRUCTION_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    register_offset: int = 2,
    trials_per_depth: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_fiber_balance_obstruction_audit(
            n_values=n_values,
            register_offset=register_offset,
            trials_per_depth=trials_per_depth,
            seed=seed,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-IMPLICIT-TOTAL-GLOBAL-TRANSPORT-BEYOND-PIVOT",
                "A nonlinear or implicit full-cube bijection can toggle the next subset-sum bit without an exact-valuation label.",
                "Half-periodicity forces the factored first Fourier coefficient to vanish, which is equivalent to an exact-valuation pivot.",
            ),
            (
                "NEG-DCP-SET-THEORETIC-FIBER-PAIRING-AS-EFFICIENT-MAP",
                "Large optimal cross-child matching mass on finite fibers is evidence for an efficient quantum transport.",
                "The multiplicity bound constructs no matching circuit, coherent state preparation, verified output routine, or classical separation.",
            ),
        )
        for negative_id, claim, reason in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson=(
                        "Delete total full-cube transports from the search space. Retain only target-fiber partial maps "
                        "or relation samplers and require explicit source coverage, efficient implementation, and classical baselines."
                    ),
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or (
            f"RESULT-{registry_experiment_id}-DCP-FIBER-BALANCE-OBSTRUCTION"
        )
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
                artifacts={"dcp_fiber_balance_obstruction": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_fiber_balance_obstruction_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
