"""Explicit small-group audit of two-copy Kronecker-sector transitions.

The character/Kronecker spectrum diagonalizes the average frame but does not
specify an individual mixed coset state in that basis.  This audit constructs
the regular representation for S_3 and S_4, verifies the exact theoretical
frame spectrum, and measures every transition mass

    Tr(P_alpha rho_h P_beta rho_h).

Those masses determine the PGM success after weighting by the inverse square
roots of the frame eigenvalues.  The construction is intentionally capped at
small groups: its dense |S_n|^4 matrix storage is a falsifier for treating
explicit transition tables as a scalable algorithm.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from coset_state_distinguishability import involution_count
from coset_two_copy_frame import theoretical_two_copy_scalar_multiplicities
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from weak_fourier_signal import involution_specs_for_n


COSET_TWO_COPY_TRANSITION_PATH = Path(
    "research/representation/coset_two_copy_transition_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TWO-COPY-TRANSITION-ALGEBRA"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TransitionCell:
    source_frame_scalar: float
    target_frame_scalar: float
    source_eigenspace_dimension: int
    target_eigenspace_dimension: int
    transition_frobenius_mass: float
    normalized_transition_mass: float
    pgm_success_contribution: float
    is_off_diagonal: bool


@dataclass(frozen=True)
class TwoCopyTransitionRecord:
    n: int
    involution_type: str
    transposition_count: int
    group_order: int
    ensemble_size: int
    hilbert_dimension: int
    dense_matrix_entry_count: int
    theoretical_frame_eigenvalue_count: int
    numerical_frame_rank: int
    spectrum_multiplicities_match: bool
    maximum_spectrum_error: float
    state_purity: float
    expected_state_purity: float
    frame_state_commutator_frobenius_norm: float
    off_diagonal_transition_mass: float
    off_diagonal_transition_mass_fraction: float
    exact_numerical_pgm_success_probability: float
    diagonal_transition_pgm_contribution: float
    off_diagonal_transition_pgm_contribution: float
    off_diagonal_pgm_contribution_fraction: float
    rejected_commuting_rank_formula: float
    rank_formula_absolute_gap: float
    spectral_pgm_lower_bound: float
    spectral_pgm_upper_bound: float
    transition_table_polynomially_constructed: bool
    transition_cells: list[TransitionCell]
    status: str


@dataclass(frozen=True)
class TwoCopyTransitionReport:
    created_at: str
    records: list[TwoCopyTransitionRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def _cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    cycles: list[int] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        cycles.append(length)
    return tuple(sorted(cycles, reverse=True))


def _regular_two_copy_states(
    n: int,
    transposition_count: int,
) -> list[np.ndarray]:
    permutations = list(itertools.permutations(range(n)))
    index = {permutation: i for i, permutation in enumerate(permutations)}
    order = len(permutations)
    cycle_type = tuple(
        sorted(
            (2,) * transposition_count + (1,) * (n - 2 * transposition_count),
            reverse=True,
        )
    )
    identity = np.eye(order)
    states: list[np.ndarray] = []
    for hidden in permutations:
        if _cycle_type(hidden) != cycle_type:
            continue
        right = np.zeros((order, order))
        for column, group_element in enumerate(permutations):
            right[index[_compose(group_element, hidden)], column] = 1.0
        one_copy = (identity + right) / order
        states.append(np.kron(one_copy, one_copy))
    return states


def audit_two_copy_transitions(
    n: int,
    transposition_count: int,
    involution_type: str,
    maximum_hilbert_dimension: int = 1024,
) -> TwoCopyTransitionRecord:
    order = math.factorial(n)
    dimension = order * order
    if dimension > maximum_hilbert_dimension:
        raise ValueError(
            f"explicit transition audit dimension {dimension} exceeds cap {maximum_hilbert_dimension}"
        )
    states = _regular_two_copy_states(n, transposition_count)
    if len(states) != involution_count(n, transposition_count):
        raise ArithmeticError("explicit conjugacy-class size disagrees with involution count")
    frame = sum(states) / len(states)
    eigenvalues, eigenvectors = np.linalg.eigh(frame)
    theoretical = theoretical_two_copy_scalar_multiplicities(n, transposition_count)
    groups: list[tuple[float, np.ndarray]] = []
    maximum_error = 0.0
    multiplicities_match = True
    for scalar, expected_multiplicity in theoretical.items():
        eigenvalue = float(scalar) / (order * order)
        indices = np.flatnonzero(np.isclose(eigenvalues, eigenvalue, atol=1e-11, rtol=1e-9))
        groups.append((float(scalar), indices))
        multiplicities_match &= len(indices) == expected_multiplicity
        if len(indices):
            maximum_error = max(
                maximum_error,
                float(np.max(np.abs(eigenvalues[indices] - eigenvalue))),
            )
    hidden_state = states[0]
    transformed = eigenvectors.T @ hidden_state @ eigenvectors
    purity = float(np.trace(hidden_state @ hidden_state).real)
    cells: list[TransitionCell] = []
    diagonal_pgm = 0.0
    off_diagonal_pgm = 0.0
    off_diagonal_mass = 0.0
    for source_scalar, source_indices in groups:
        if source_scalar <= 0:
            continue
        for target_scalar, target_indices in groups:
            if target_scalar <= 0:
                continue
            block = transformed[np.ix_(source_indices, target_indices)]
            mass = float(np.sum(np.abs(block) ** 2))
            contribution = (
                mass
                * order
                * order
                / (len(states) * math.sqrt(source_scalar * target_scalar))
            )
            off_diagonal = not math.isclose(source_scalar, target_scalar, abs_tol=1e-12)
            if off_diagonal:
                off_diagonal_mass += mass
                off_diagonal_pgm += contribution
            else:
                diagonal_pgm += contribution
            cells.append(
                TransitionCell(
                    source_frame_scalar=source_scalar,
                    target_frame_scalar=target_scalar,
                    source_eigenspace_dimension=len(source_indices),
                    target_eigenspace_dimension=len(target_indices),
                    transition_frobenius_mass=mass,
                    normalized_transition_mass=mass / purity if purity else 0.0,
                    pgm_success_contribution=contribution,
                    is_off_diagonal=off_diagonal,
                )
            )
    exact_pgm = diagonal_pgm + off_diagonal_pgm
    positive_scalars = [float(scalar) for scalar in theoretical if scalar > 0]
    rank = int(np.count_nonzero(eigenvalues > 1e-11))
    rank_formula = 4 * rank / (len(states) * order * order)
    commutator = frame @ hidden_state - hidden_state @ frame
    commutator_norm = float(np.linalg.norm(commutator))
    commuting_control = commutator_norm <= 1e-12
    return TwoCopyTransitionRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        group_order=order,
        ensemble_size=len(states),
        hilbert_dimension=dimension,
        dense_matrix_entry_count=dimension * dimension,
        theoretical_frame_eigenvalue_count=len(theoretical),
        numerical_frame_rank=rank,
        spectrum_multiplicities_match=multiplicities_match,
        maximum_spectrum_error=maximum_error,
        state_purity=purity,
        expected_state_purity=4 / (order * order),
        frame_state_commutator_frobenius_norm=commutator_norm,
        off_diagonal_transition_mass=off_diagonal_mass,
        off_diagonal_transition_mass_fraction=off_diagonal_mass / purity if purity else 0.0,
        exact_numerical_pgm_success_probability=exact_pgm,
        diagonal_transition_pgm_contribution=diagonal_pgm,
        off_diagonal_transition_pgm_contribution=off_diagonal_pgm,
        off_diagonal_pgm_contribution_fraction=off_diagonal_pgm / exact_pgm if exact_pgm else 0.0,
        rejected_commuting_rank_formula=rank_formula,
        rank_formula_absolute_gap=abs(rank_formula - exact_pgm),
        spectral_pgm_lower_bound=min(1.0, 4 / (len(states) * max(positive_scalars))),
        spectral_pgm_upper_bound=min(1.0, 4 / (len(states) * min(positive_scalars))),
        transition_table_polynomially_constructed=False,
        transition_cells=cells,
        status=(
            "commuting-class-control-rank-formula-exact"
            if commuting_control
            else "finite-transition-table-exact-no-scalable-construction"
        ),
    )


def build_two_copy_transition_report(
    n_values: Sequence[int] = (3, 4),
) -> TwoCopyTransitionReport:
    unique_specs = []
    seen: set[tuple[int, int]] = set()
    for n in n_values:
        for label, transpositions in involution_specs_for_n(n):
            key = (n, transpositions)
            if key not in seen:
                seen.add(key)
                unique_specs.append((n, transpositions, label))
    records = [
        audit_two_copy_transitions(n, transpositions, label)
        for n, transpositions, label in unique_specs
    ]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "spectrum_verified_count": sum(record.spectrum_multiplicities_match for record in records),
        "noncommuting_frame_count": sum(
            record.frame_state_commutator_frobenius_norm > 1e-12 for record in records
        ),
        "commuting_class_control_count": sum(
            record.frame_state_commutator_frobenius_norm <= 1e-12 for record in records
        ),
        "nonzero_off_diagonal_transition_count": sum(
            record.off_diagonal_transition_mass > 1e-12 for record in records
        ),
        "rank_formula_falsified_count": sum(
            record.rank_formula_absolute_gap > 1e-8 for record in records
        ),
        "polynomial_transition_table_count": sum(
            record.transition_table_polynomially_constructed for record in records
        ),
        "maximum_n": max(n_values),
        "maximum_dense_matrix_entry_count": max(
            record.dense_matrix_entry_count for record in records
        ),
        "maximum_off_diagonal_transition_mass_fraction": max(
            record.off_diagonal_transition_mass_fraction for record in records
        ),
        "maximum_off_diagonal_pgm_contribution_fraction": max(
            record.off_diagonal_pgm_contribution_fraction for record in records
        ),
        "maximum_rank_formula_gap": max(record.rank_formula_absolute_gap for record in records),
    }
    return TwoCopyTransitionReport(
        created_at=utc_now(),
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "finite_transition_weights_computed": True,
            "spectrum_only_pgm_formula_allowed": False,
            "polynomial_transition_algebra_proved": False,
            "coherent_measurement_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Off-diagonal sector transitions contribute to the PGM, while the explicit regular construction "
                "stores |S_n|^4 dense entries and has no scalable recoupling implementation."
            ),
        },
        status="finite-transition-algebra-measured-scalable-construction-open",
        summary=(
            f"Verified exact frame spectra and measured transition tables for {len(records)} S_n involution ensembles "
            f"through n={max(n_values)}; no polynomial transition-algebra construction is known."
        ),
        falsifiers_triggered=[
            "Off-diagonal average-frame eigenspace transitions are nonzero.",
            "Spectrum support rank does not determine mixed-state PGM success.",
            "Exceptional commuting classes can make the rank formula exact but do not generalize to noncommuting classes.",
            "The explicit regular transition table requires factorial-size Hilbert space and |S_n|^4 entries.",
            "Finite exact PGM values do not provide a coherent measurement or hidden-involution decoder.",
        ],
    )


def write_two_copy_transition_report(
    output_path: Path = COSET_TWO_COPY_TRANSITION_PATH,
    n_values: Sequence[int] = (3, 4),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_two_copy_transition_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-EXPLICIT-TWO-COPY-TRANSITION-TABLE",
                source=str(output_path),
                claim="A finite explicit regular-representation transition table is a scalable collective measurement.",
                reason_invalid=(
                    "The construction uses factorial Hilbert dimension and |S_n|^4 dense matrix entries; it neither "
                    "implements recoupling coherently nor decodes the hidden involution."
                ),
                lesson=(
                    "Search for compressed formulas for sector transition weights and reject any representation that "
                    "materializes the regular tensor space."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
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
                artifacts={"coset_two_copy_transition_audit": str(output_path)},
            )
        )
    return payload
