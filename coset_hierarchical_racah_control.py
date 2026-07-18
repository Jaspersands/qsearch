"""Hierarchical finite Racah basis for every final sector of V_(4,2)^tensor3.

The first-stage orbit Hamiltonian resolves Kronecker multiplicity in the pair
V_(4,2) tensor V_(4,2).  A second bounded-support Hamiltonian applies the same
orbit rule between the diagonal action on that pair and the third copy.  The
two operators commute because they act on the first- and second-stage
multiplicity factors.  Together with pair central signatures, their joint
spectrum resolves every left- and right-coupling channel at n=6, including
second-stage multiplicities two and three.

This yields a complete finite S_6 Racah table.  It remains a dense control:
the joint gap needs a stable-n lower bound, the matrices need a compressed
formula and coherent implementation, and no hidden-involution decoder follows.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from coset_complete_racah_control import (
    _central_signature,
    _pair_class_sums,
    _triple_channels,
)
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    _oriented_three_cycles,
    _transpositions,
    transposition_three_cycle_intersection_operator,
)
from coset_restricted_racah_control import _total_encoded_yjm
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_HIERARCHICAL_RACAH_CONTROL_PATH = Path(
    "research/representation/coset_hierarchical_racah_control.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIERARCHICAL-RACAH-CONTROL"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HierarchicalRacahChannelRecord:
    intermediate_partition: tuple[int, ...]
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    pair_central_signature: int
    first_stage_hamiltonian_eigenvalue: float
    second_stage_hamiltonian_eigenvalue: float


@dataclass(frozen=True)
class HierarchicalRacahMatrixRecord:
    n: int
    source_partition: tuple[int, ...]
    final_partition: tuple[int, ...]
    final_irrep_dimension: int
    final_total_multiplicity: int
    final_tableau_count: int
    channels: list[HierarchicalRacahChannelRecord]
    signed_overlap_matrix: list[list[float]]
    absolute_overlap_matrix: list[list[float]]
    transition_probability_matrix: list[list[float]]
    unitarity_residual: float
    tableau_absolute_consistency_residual: float
    tableau_probability_consistency_residual: float
    left_right_joint_spectrum_residual: float
    minimum_first_stage_raw_gap: float
    minimum_second_stage_raw_gap: float
    second_stage_multiplicity_resolved: bool
    nontrivial_recoupling: bool
    complete_for_final_sector: bool
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class HierarchicalRacahControlReport:
    created_at: str
    operator_contract: dict[str, object]
    records: list[HierarchicalRacahMatrixRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _second_stage_hamiltonians(
    partition: tuple[int, ...], support_intersection: int = 2
) -> tuple[np.ndarray, np.ndarray, int]:
    dimension = hook_length_dimension(partition)
    left = np.zeros((dimension**3, dimension**3))
    right = np.zeros_like(left)
    term_count = 0
    for transposition_support, transposition in _transpositions(partition):
        transposition_set = set(transposition_support)
        for cycle_support, cycle in _oriented_three_cycles(partition):
            if len(transposition_set.intersection(cycle_support)) != support_intersection:
                continue
            left += np.kron(np.kron(transposition, transposition), cycle)
            right += np.kron(np.kron(cycle, transposition), transposition)
            term_count += 1
    return left, right, term_count


def _group_eigenvalues(
    eigenvalues: np.ndarray, tolerance: float = 1e-7
) -> list[list[int]]:
    groups: list[list[int]] = []
    for index, value in enumerate(eigenvalues):
        if not groups or abs(value - eigenvalues[groups[-1][0]]) > tolerance:
            groups.append([index])
        else:
            groups[-1].append(index)
    return groups


def _minimum_distinct_gap(values: np.ndarray, tolerance: float = 1e-7) -> float:
    distinct: list[float] = []
    for value in sorted(float(item) for item in values):
        if not distinct or abs(value - distinct[-1]) > tolerance:
            distinct.append(value)
    if len(distinct) <= 1:
        return math.inf
    return min(right - left for left, right in zip(distinct, distinct[1:]))


def _resolve_hierarchical_pair_basis(
    final_tableau_basis: np.ndarray,
    pair_signature_operator: np.ndarray,
    first_stage_hamiltonian: np.ndarray,
    second_stage_hamiltonian: np.ndarray,
    channel_specs: list[tuple[tuple[int, ...], int, int]],
) -> tuple[np.ndarray, list[HierarchicalRacahChannelRecord], float, float]:
    restricted_signature = final_tableau_basis.T @ pair_signature_operator @ final_tableau_basis
    signature_values, signature_vectors = np.linalg.eigh(
        (restricted_signature + restricted_signature.T) / 2
    )
    basis_columns: list[np.ndarray] = []
    channel_records: list[HierarchicalRacahChannelRecord] = []
    first_stage_gaps: list[float] = []
    second_stage_gaps: list[float] = []

    for intermediate, first_multiplicity, second_multiplicity in channel_specs:
        signature = _central_signature(intermediate)
        selected = np.where(np.abs(signature_values - signature) < 1e-7)[0]
        expected_dimension = first_multiplicity * second_multiplicity
        if len(selected) != expected_dimension:
            raise ArithmeticError(
                f"expected channel dimension {expected_dimension} for {intermediate}, observed {len(selected)}"
            )
        signature_basis = final_tableau_basis @ signature_vectors[:, selected]
        restricted_first = signature_basis.T @ first_stage_hamiltonian @ signature_basis
        first_values, first_vectors = np.linalg.eigh(
            (restricted_first + restricted_first.T) / 2
        )
        first_groups = _group_eigenvalues(first_values)
        if len(first_groups) != first_multiplicity:
            raise ArithmeticError(
                f"first-stage Hamiltonian does not split {intermediate}: expected {first_multiplicity}, observed {len(first_groups)}"
            )
        first_stage_gaps.append(_minimum_distinct_gap(first_values))
        for first_group in first_groups:
            if len(first_group) != second_multiplicity:
                raise ArithmeticError("first-stage eigenspace has the wrong residual multiplicity")
            first_basis = signature_basis @ first_vectors[:, first_group]
            restricted_second = first_basis.T @ second_stage_hamiltonian @ first_basis
            second_values, second_vectors = np.linalg.eigh(
                (restricted_second + restricted_second.T) / 2
            )
            if len(_group_eigenvalues(second_values)) != second_multiplicity:
                raise ArithmeticError(
                    f"second-stage Hamiltonian does not split multiplicity {second_multiplicity} for {intermediate}"
                )
            second_stage_gaps.append(_minimum_distinct_gap(second_values))
            resolved = first_basis @ second_vectors
            first_value = float(first_values[first_group[0]])
            for index, second_value in enumerate(second_values):
                basis_columns.append(resolved[:, index])
                channel_records.append(
                    HierarchicalRacahChannelRecord(
                        intermediate_partition=intermediate,
                        first_stage_multiplicity=first_multiplicity,
                        second_stage_multiplicity=second_multiplicity,
                        pair_central_signature=signature,
                        first_stage_hamiltonian_eigenvalue=first_value,
                        second_stage_hamiltonian_eigenvalue=float(second_value),
                    )
                )

    basis = np.column_stack(basis_columns)
    expected = sum(first * second for _, first, second in channel_specs)
    if basis.shape[1] != expected:
        raise ArithmeticError("hierarchical pair basis has the wrong dimension")
    if np.linalg.norm(basis.T @ basis - np.eye(expected)) > 1e-7:
        raise ArithmeticError("hierarchical pair basis is not orthonormal")
    finite_first_gaps = [gap for gap in first_stage_gaps if math.isfinite(gap)]
    finite_second_gaps = [gap for gap in second_stage_gaps if math.isfinite(gap)]
    return (
        basis,
        channel_records,
        min(finite_first_gaps, default=0.0),
        min(finite_second_gaps, default=0.0),
    )


@lru_cache(maxsize=1)
def _audit_hierarchical_racah_control_cached(
    n: int = 6,
) -> tuple[HierarchicalRacahMatrixRecord, ...]:
    if n != 6:
        raise ValueError(
            "the hierarchical dense Racah control is pinned to n=6; scaling requires a compressed construction"
        )
    source = (n - 2, 2)
    source_dimension = hook_length_dimension(source)
    identity = np.eye(source_dimension)

    total_yjm = _total_encoded_yjm(source)
    label_values, label_vectors = np.linalg.eigh(total_yjm)
    label_indices: dict[int, list[int]] = {}
    for index, value in enumerate(label_values):
        label_indices.setdefault(round(float(value)), []).append(index)
    target_by_label = _encoded_label_targets(n, 2 * n + 1)

    pair_transpositions, pair_three_cycles = _pair_class_sums(source)
    pair_signature = 100 * pair_transpositions + pair_three_cycles
    pair_hamiltonian, _ = transposition_three_cycle_intersection_operator(
        source, source, support_intersection=2
    )
    second_left, second_right, _ = _second_stage_hamiltonians(source)
    left_signature = np.kron(pair_signature, identity)
    right_signature = np.kron(identity, pair_signature)
    first_left = np.kron(pair_hamiltonian, identity)
    first_right = np.kron(identity, pair_hamiltonian)

    records: list[HierarchicalRacahMatrixRecord] = []
    for final in integer_partitions(n):
        channel_specs = _triple_channels(source, final)
        if not channel_specs:
            continue
        total_multiplicity = sum(first * second for _, first, second in channel_specs)
        signed_overlaps: list[np.ndarray] = []
        absolute_overlaps: list[np.ndarray] = []
        probability_matrices: list[np.ndarray] = []
        channel_rows: list[list[HierarchicalRacahChannelRecord]] = []
        joint_spectrum_residuals: list[float] = []
        first_gaps: list[float] = []
        second_gaps: list[float] = []

        for label, indices in label_indices.items():
            if target_by_label[label] != final:
                continue
            final_basis = label_vectors[:, indices]
            if final_basis.shape[1] != total_multiplicity:
                raise ArithmeticError("final-tableau multiplicity does not match characters")
            left_basis, left_channels, left_first_gap, left_second_gap = (
                _resolve_hierarchical_pair_basis(
                    final_basis,
                    left_signature,
                    first_left,
                    second_left,
                    channel_specs,
                )
            )
            right_basis, right_channels, right_first_gap, right_second_gap = (
                _resolve_hierarchical_pair_basis(
                    final_basis,
                    right_signature,
                    first_right,
                    second_right,
                    channel_specs,
                )
            )
            left_joint = np.asarray(
                [
                    (
                        channel.pair_central_signature,
                        channel.first_stage_hamiltonian_eigenvalue,
                        channel.second_stage_hamiltonian_eigenvalue,
                    )
                    for channel in left_channels
                ]
            )
            right_joint = np.asarray(
                [
                    (
                        channel.pair_central_signature,
                        channel.first_stage_hamiltonian_eigenvalue,
                        channel.second_stage_hamiltonian_eigenvalue,
                    )
                    for channel in right_channels
                ]
            )
            joint_spectrum_residuals.append(float(np.linalg.norm(left_joint - right_joint)))
            first_gaps.extend([left_first_gap, right_first_gap])
            second_gaps.extend([left_second_gap, right_second_gap])
            overlap = left_basis.T @ right_basis
            signed_overlaps.append(overlap)
            absolute_overlaps.append(np.abs(overlap))
            probability_matrices.append(overlap * overlap)
            channel_rows.append(left_channels)

        reference = signed_overlaps[0]
        absolute_reference = absolute_overlaps[0]
        probability_reference = probability_matrices[0]
        unitarity_residual = max(
            float(np.linalg.norm(matrix.T @ matrix - np.eye(total_multiplicity)))
            for matrix in signed_overlaps
        )
        absolute_consistency = max(
            float(np.linalg.norm(matrix - absolute_reference))
            for matrix in absolute_overlaps
        )
        probability_consistency = max(
            float(np.linalg.norm(matrix - probability_reference))
            for matrix in probability_matrices
        )
        off_diagonal = reference - np.diag(np.diag(reference))
        finite_first_gaps = [gap for gap in first_gaps if math.isfinite(gap)]
        finite_second_gaps = [gap for gap in second_gaps if math.isfinite(gap)]
        records.append(
            HierarchicalRacahMatrixRecord(
                n=n,
                source_partition=source,
                final_partition=final,
                final_irrep_dimension=hook_length_dimension(final),
                final_total_multiplicity=total_multiplicity,
                final_tableau_count=len(signed_overlaps),
                channels=channel_rows[0],
                signed_overlap_matrix=reference.tolist(),
                absolute_overlap_matrix=absolute_reference.tolist(),
                transition_probability_matrix=probability_reference.tolist(),
                unitarity_residual=unitarity_residual,
                tableau_absolute_consistency_residual=absolute_consistency,
                tableau_probability_consistency_residual=probability_consistency,
                left_right_joint_spectrum_residual=max(joint_spectrum_residuals),
                minimum_first_stage_raw_gap=min(finite_first_gaps, default=math.inf),
                minimum_second_stage_raw_gap=min(finite_second_gaps, default=math.inf),
                second_stage_multiplicity_resolved=True,
                nontrivial_recoupling=bool(np.linalg.norm(off_diagonal) > 1e-8),
                complete_for_final_sector=unitarity_residual < 1e-8,
                finite_dense_control_only=True,
                status=(
                    "complete-hierarchical-finite-racah-control"
                    if unitarity_residual < 1e-8
                    else "hierarchical-racah-control-failed-unitarity"
                ),
            )
        )
    return tuple(records)


def audit_hierarchical_racah_control(n: int = 6) -> list[HierarchicalRacahMatrixRecord]:
    return list(_audit_hierarchical_racah_control_cached(n))


def build_hierarchical_racah_control_report(
    n: int = 6,
) -> HierarchicalRacahControlReport:
    records = audit_hierarchical_racah_control(n=n)
    _, _, second_stage_term_count = _second_stage_hamiltonians((n - 2, 2))
    maximum_unitarity = max(
        (record.unitarity_residual for record in records), default=math.inf
    )
    maximum_consistency = max(
        (record.tableau_absolute_consistency_residual for record in records),
        default=math.inf,
    )
    finite_first_gaps = [
        record.minimum_first_stage_raw_gap
        for record in records
        if record.minimum_first_stage_raw_gap > 0
    ]
    finite_second_gaps = [
        record.minimum_second_stage_raw_gap
        for record in records
        if record.minimum_second_stage_raw_gap > 0
    ]
    metrics: dict[str, int | float] = {
        "final_target_count": len(records),
        "complete_hierarchical_finite_racah_matrix_count": sum(
            record.complete_for_final_sector for record in records
        ),
        "nontrivial_complete_finite_racah_matrix_count": sum(
            record.complete_for_final_sector and record.nontrivial_recoupling
            for record in records
        ),
        "second_stage_multiplicity_resolved_sector_count": sum(
            record.second_stage_multiplicity_resolved for record in records
        ),
        "unresolved_finite_sector_count": sum(
            not record.complete_for_final_sector for record in records
        ),
        "maximum_matrix_dimension": max(
            (record.final_total_multiplicity for record in records), default=0
        ),
        "maximum_second_stage_multiplicity": max(
            (
                channel.second_stage_multiplicity
                for record in records
                for channel in record.channels
            ),
            default=0,
        ),
        "second_stage_lcu_term_count": second_stage_term_count,
        "second_stage_term_count_formula": n * (n - 1) * (n - 2),
        "second_stage_term_count_formula_verified_count": int(
            second_stage_term_count == n * (n - 1) * (n - 2)
        ),
        "minimum_observed_first_stage_raw_gap": min(finite_first_gaps, default=0.0),
        "minimum_observed_second_stage_raw_gap": min(finite_second_gaps, default=0.0),
        "minimum_observed_second_stage_normalized_gap": (
            min(finite_second_gaps, default=0.0) / second_stage_term_count
        ),
        "maximum_unitarity_residual": maximum_unitarity,
        "maximum_tableau_absolute_consistency_residual": maximum_consistency,
        "stable_n_joint_gap_theorem_count": 0,
        "uniform_polynomial_racah_circuit_count": 0,
        "hidden_involution_decoder_count": 0,
        "maximum_dense_dimension": hook_length_dimension((n - 2, 2)) ** 3,
    }
    all_complete = bool(records) and all(
        record.complete_for_final_sector
        and record.second_stage_multiplicity_resolved
        for record in records
    )
    return HierarchicalRacahControlReport(
        created_at=utc_now(),
        operator_contract={
            "source": "three copies of V_(4,2) for S_6",
            "pair_partition_label": "transposition and 3-cycle central signature",
            "first_stage_hamiltonian": (
                "sum rho(tau) tensor rho(c) over transpositions contained in oriented 3-cycles"
            ),
            "second_stage_left_hamiltonian": (
                "sum rho(tau) tensor rho(tau) tensor rho(c) over the same support orbit"
            ),
            "second_stage_right_hamiltonian": (
                "sum rho(c) tensor rho(tau) tensor rho(tau) over the same support orbit"
            ),
            "joint_label": "intermediate partition, first-stage eigenvalue, second-stage eigenvalue",
            "reported_object": "complete signed S_6 left/right Racah controls for every final sector",
            "not_reported_as": "a stable-n gap theorem, uniform coherent circuit, or hidden-involution decoder",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_finite_final_sectors_resolved": all_complete,
            "complete_finite_s6_racah_table_verified": all_complete,
            "second_stage_multiplicity_resolved": all_complete,
            "stable_n_joint_gap_proved": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The hierarchical operator family resolves the complete n=6 table, but stable-n spectral gaps, "
                "compressed matrix formulas, coherent gate complexity, and decoding remain unproved."
            ),
        },
        status=(
            "complete-s6-hierarchical-racah-table-stable-n-circuit-open"
            if all_complete
            else "hierarchical-racah-control-incomplete"
        ),
        summary=(
            f"Resolved all {len(records)} final S_6 sectors with a two-level bounded-support commutant hierarchy; "
            "the finite Racah table is complete, while stable-n gaps, a circuit, and a decoder remain open."
        ),
        falsifiers_triggered=[
            "One pair Hamiltonian is insufficient in sectors with second-stage Kronecker multiplicity.",
            "A complete finite S_6 Racah table is not evidence of inverse-polynomial gaps at growing n.",
            "Dense joint diagonalization does not compile the basis into a uniform coherent circuit.",
            "Recoupling coordinates alone do not recover the hidden involution.",
        ],
    )


def write_hierarchical_racah_control_report(
    output_path: Path = COSET_HIERARCHICAL_RACAH_CONTROL_PATH,
    n: int = 6,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_hierarchical_racah_control_report(n=n))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-COMPLETE-S6-RACAH-AS-STABLE-N-CIRCUIT",
                source=str(output_path),
                claim=(
                    "A complete finite S_6 hierarchical Racah table establishes a uniform efficient associator."
                ),
                reason_invalid=(
                    "The table is obtained by dense 729-dimensional diagonalization; no stable-n joint-gap bound, "
                    "compressed formula, or coherent circuit is proved."
                ),
                lesson=(
                    "Promote the bounded-support operator hierarchy, not the dense matrices: derive its stable-n "
                    "multiplicity action and gap before making an algorithmic claim."
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
                artifacts={"coset_hierarchical_racah_control": str(output_path)},
            )
        )
    return payload
