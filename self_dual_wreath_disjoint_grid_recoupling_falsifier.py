"""Finite falsifier for scalar disjoint-pair waist composition.

The pair-core carrier factorization proves an exact scalar law when two pair
cores share an orientation.  For vertex-disjoint cores it gives only the
single-waist upper bound

    ||P_(K_ab) P_(K_cd)|| <= min_waist 1 / d_waist.       (1)

The first low-ambient controls happened to saturate (1).  That finite pattern
does not persist.  This module records a robust S_6 counterexample in which
all nine occupied cells of the row/column membership grid are individually
multiplicity-free, but

    best waist bound = 1/5,
    observed grid contraction = 1/15.                    (2)

Thus even a multiplicity-free symmetric-group 9j grid has coherent recoupling
data that are invisible to every one-waist dimension.  A second crossing of
the same grid has waist bound 1/9 and the same 1/15 contraction, showing that
the missing factor is not a monotone correction determined by the best waist.

The singular values are computed from the explicit parity-intertwiner bases.
The gap in (2) is more than eight orders of magnitude above the declared
numerical error budget, so it is a stable finite falsifier of exact waist
saturation.  The rational value 1/15 is reported as a reconstruction, not as
an all-n symbolic theorem.

This result does not obstruct the global PGM route.  Strict contraction is
helpful for conditioning.  It does prove that an asymptotic proof or coherent
compiler must retain the full row/column recoupling tensor (equivalently the
relevant symmetric-group 9j data); carrier dimensions or scalar pair angles
alone cannot determine disjoint-core overlaps.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_pair_core_carrier_factorization import (
    _dense_overlap_values,
    _multiplicity_table,
    disjoint_pair_waist_bound,
    membership_pattern_blocks,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_disjoint_grid_recoupling_falsifier.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-DISJOINT-GRID-RECOUPLING-FALSIFIER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]

TARGET: Partition = (6,)
LABELS: tuple[Label, ...] = (
    ((6,), (2, 1, 1, 1, 1)),
    ((5, 1), (1, 1, 1, 1, 1, 1)),
    ((4, 2), (2, 2, 2)),
    ((3, 3), (2, 2, 1, 1)),
)
FIRST_PAIR = (0, 15)
SECOND_PAIRS = ((5, 6), (5, 9))


@dataclass(frozen=True)
class GridCellRecord:
    membership_pattern: str
    partitions: tuple[Partition, ...]
    factor_dimension: int
    isotypic_support_size: int
    maximum_isotypic_multiplicity: int
    multiplicity_free: bool


@dataclass(frozen=True)
class DisjointGridRecouplingControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    first_pair: tuple[int, int]
    second_pair: tuple[int, int]
    occupied_grid_cell_count: int
    grid_cells: tuple[GridCellRecord, ...]
    every_occupied_cell_multiplicity_free: bool
    first_core_rank: int
    second_core_rank: int
    nonzero_overlap_rank: int
    best_waist_row: str
    best_waist_column: str
    waist_bound_numerator: int
    waist_bound_denominator: int
    waist_bound: float
    observed_operator_norm: float
    reconstructed_operator_norm: str
    rational_reconstruction_residual: float
    observed_squared_norm: float
    reconstructed_squared_norm: str
    squared_rational_reconstruction_residual: float
    strict_contraction_margin: float
    waist_to_observed_ratio: float
    numerical_error_budget: float
    strict_waist_saturation_falsifier: bool
    status: str


@dataclass(frozen=True)
class DisjointGridRecouplingFalsifierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[DisjointGridRecouplingControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _grid_cells(
    target: Partition,
    labels: tuple[Label, ...],
    first_pair: tuple[int, int],
    second_pair: tuple[int, int],
) -> tuple[GridCellRecord, ...]:
    n = sum(target)
    blocks = membership_pattern_blocks(
        target,
        labels,
        (*first_pair, *second_pair),
    )
    cells = []
    for pattern, partitions in blocks.items():
        table = _multiplicity_table(partitions, n)
        maximum = max(table.values(), default=0)
        cells.append(
            GridCellRecord(
                membership_pattern=f"{pattern:04b}",
                partitions=partitions,
                factor_dimension=int(
                    np.prod(
                        [hook_length_dimension(partition) for partition in partitions],
                        dtype=object,
                    )
                ),
                isotypic_support_size=len(table),
                maximum_isotypic_multiplicity=maximum,
                multiplicity_free=maximum <= 1,
            )
        )
    return tuple(cells)


def audit_disjoint_grid_recoupling(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    first_pair: tuple[int, int],
    second_pair: tuple[int, int],
    *,
    numerical_error_budget: float = 1e-9,
    rational_denominator_limit: int = 100_000,
) -> DisjointGridRecouplingControl:
    if len(set(first_pair) | set(second_pair)) != 4:
        raise ValueError("the two orientation pairs must be vertex-disjoint")
    bound, waist_row, waist_column = disjoint_pair_waist_bound(
        target,
        labels,
        first_pair,
        second_pair,
    )
    values, _ambient, first_rank, second_rank = _dense_overlap_values(
        target,
        labels,
        first_pair,
        second_pair,
    )
    nonzero = values[values > numerical_error_budget]
    observed = float(nonzero[0]) if len(nonzero) else 0.0
    reconstructed = Fraction(observed).limit_denominator(
        rational_denominator_limit
    )
    squared = observed * observed
    reconstructed_squared = Fraction(squared).limit_denominator(
        rational_denominator_limit
    )
    margin = float(bound) - observed
    cells = _grid_cells(target, labels, first_pair, second_pair)
    stable_falsifier = bool(
        len(cells) == 9
        and all(cell.multiplicity_free for cell in cells)
        and margin > 1_000_000 * numerical_error_budget
        and abs(observed - float(reconstructed)) < numerical_error_budget
        and abs(squared - float(reconstructed_squared)) < numerical_error_budget
    )
    return DisjointGridRecouplingControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        first_pair=first_pair,
        second_pair=second_pair,
        occupied_grid_cell_count=len(cells),
        grid_cells=cells,
        every_occupied_cell_multiplicity_free=all(
            cell.multiplicity_free for cell in cells
        ),
        first_core_rank=first_rank,
        second_core_rank=second_rank,
        nonzero_overlap_rank=len(nonzero),
        best_waist_row=waist_row,
        best_waist_column=waist_column,
        waist_bound_numerator=bound.numerator,
        waist_bound_denominator=bound.denominator,
        waist_bound=float(bound),
        observed_operator_norm=observed,
        reconstructed_operator_norm=str(reconstructed),
        rational_reconstruction_residual=abs(observed - float(reconstructed)),
        observed_squared_norm=squared,
        reconstructed_squared_norm=str(reconstructed_squared),
        squared_rational_reconstruction_residual=abs(
            squared - float(reconstructed_squared)
        ),
        strict_contraction_margin=margin,
        waist_to_observed_ratio=float(bound) / observed,
        numerical_error_budget=numerical_error_budget,
        strict_waist_saturation_falsifier=stable_falsifier,
        status=(
            "multiplicity-free-grid-strictly-below-waist-bound"
            if stable_falsifier
            else "disjoint-grid-falsifier-validation-failure"
        ),
    )


def run_disjoint_grid_recoupling_falsifier(
) -> DisjointGridRecouplingFalsifierReport:
    controls = [
        audit_disjoint_grid_recoupling(
            f"S6-MULTIPLICITY-FREE-GRID-{index}",
            TARGET,
            LABELS,
            FIRST_PAIR,
            second_pair,
        )
        for index, second_pair in enumerate(SECOND_PAIRS, start=1)
    ]
    verified = all(row.strict_waist_saturation_falsifier for row in controls)
    primary = controls[0]
    return DisjointGridRecouplingFalsifierReport(
        created_at=utc_now(),
        theorem_contract={
            "proved_input": (
                "The existing disjoint-pair theorem gives a one-waist upper "
                "bound on the pair-core product norm."
            ),
            "falsified_extension": (
                "That upper bound is always attained, or is determined by "
                "the best waist carrier dimension alone."
            ),
            "finite_witness": (
                "A fully explicit S_6 grid has nine multiplicity-free occupied "
                "cells, first/second core ranks 1 and 81, and product norm 1/15 "
                "against a best waist bound 1/5."
            ),
            "architectural_consequence": (
                "Disjoint-core analysis and compilation must retain the full "
                "row/column recoupling tensor, not just carrier dimensions or "
                "pairwise principal angles."
            ),
            "scope": (
                "This is a stable finite numerical counterexample. It is not "
                "an all-n norm formula, an asymptotic gap, or a circuit lower bound."
            ),
        },
        controls=controls,
        proof_obligations=[
            {
                "obligation": "derive_exact_disjoint_grid_recoupling_formula",
                "resolved": False,
                "resolution": (
                    "Express each block as a symmetric-group 9j contraction "
                    "with explicit multiplicity indices and normalization."
                ),
            },
            {
                "obligation": "prove_uniform_residual_pair_quotient_gap",
                "resolved": False,
                "resolution": (
                    "Strict finite contraction helps but does not bound natural "
                    "threshold-depth child spans uniformly in n."
                ),
            },
            {
                "obligation": "compile_coherent_grid_recoupling",
                "resolved": False,
                "resolution": (
                    "No polynomial circuit for the required 9j/Racah transport "
                    "or its source-weighted restriction is known."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Strictness requires a high-multiplicity cell.",
                "resolved": True,
                "resolution": (
                    "False. Every occupied cell in the explicit grid has "
                    "isotypic multiplicity at most one."
                ),
            },
            {
                "objection": "The discrepancy is floating-point noise.",
                "resolved": True,
                "resolution": (
                    f"The primary margin is {primary.strict_contraction_margin:.6g}, "
                    "over 10^8 times the declared numerical error budget."
                ),
            },
            {
                "objection": "Strict contraction kills the global algorithm.",
                "resolved": True,
                "resolution": (
                    "False. It can improve conditioning; what it kills is the "
                    "scalar-waist equality shortcut and any compiler based on it."
                ),
            },
            {
                "objection": "The reconstructed value 1/15 is already an exact all-n law.",
                "resolved": True,
                "resolution": (
                    "False. It is a finite rational reconstruction pending a "
                    "symbolic 9j derivation."
                ),
            },
        ],
        headline_metrics={
            "finite_disjoint_grid_control_count": len(controls),
            "strict_waist_saturation_falsifier_count": sum(
                row.strict_waist_saturation_falsifier for row in controls
            ),
            "primary_occupied_grid_cell_count": primary.occupied_grid_cell_count,
            "primary_first_core_rank": primary.first_core_rank,
            "primary_second_core_rank": primary.second_core_rank,
            "primary_waist_bound": primary.waist_bound,
            "primary_observed_operator_norm": primary.observed_operator_norm,
            "primary_waist_to_observed_ratio": primary.waist_to_observed_ratio,
            "all_n_disjoint_grid_formula_count": 0,
            "coherent_grid_recoupling_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "finite_multiplicity_free_strict_grid_contraction_verified": verified,
            "single_waist_bound_always_tight": False,
            "disjoint_overlap_determined_by_carrier_dimensions": False,
            "full_grid_recoupling_data_required": verified,
            "exact_all_n_grid_spectrum_proved": False,
            "uniform_residual_pair_quotient_gap_proved": False,
            "coherent_grid_recoupling_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The scalar equality shortcut is falsified. The surviving "
                "route requires an exact source-weighted 9j formula, asymptotic "
                "conditioning, and a coherent compiler."
            ),
        },
        status=(
            "scalar-disjoint-waist-equality-falsified-grid-recoupling-open"
            if verified
            else "disjoint-grid-falsifier-validation-failure"
        ),
        summary=(
            "Falsified exact single-waist saturation with a multiplicity-free "
            "S_6 grid: the disjoint pair-core norm is 1/15 while the best waist "
            "bound is 1/5. Full 9j/Racah coherence is indispensable."
        ),
        falsifiers_triggered=[
            "The first forty saturated waist controls were not representative.",
            "Multiplicity-free local cells do not make a disjoint grid scalar.",
            "Carrier dimensions alone do not determine disjoint pair-core overlap.",
        ],
    )


def write_disjoint_grid_recoupling_falsifier_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    del write_registry, registry_experiment_id, registry_candidate_id, registry_result_id
    payload = asdict(run_disjoint_grid_recoupling_falsifier(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_disjoint_grid_recoupling_falsifier_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
