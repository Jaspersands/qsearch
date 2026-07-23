"""Bounded-support commutant search inside Kronecker multiplicity spaces.

After diagonal Young--Jucys--Murphy (YJM) label extraction, each target
tableau eigenspace has residual dimension g(lambda, mu, nu).  Operators formed
by summing rho_lambda(a) tensor rho_mu(b) over simultaneous-conjugacy orbits
commute with the diagonal S_n action and therefore act only on these
multiplicity registers.

This workbench searches a polynomial-description family built from disjoint
transposition pairs and transposition/3-cycle pairs classified by support
intersection.  It asks whether a small-integer Hermitian combination has
simple spectrum in every finite multiplicity block.  Every block-encoding term
and its LCU normalization is charged.  A finite simple spectrum is not promoted
to a polynomial transform: the minimum normalized eigenvalue gap still needs
an inverse-polynomial all-n lower bound, and recoupling associators and decoding
remain separate obligations.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import numpy as np

from coset_jucys_murphy_label_transform import (
    adjacent_transposition_matrices,
    diagonal_jucys_murphy_operators,
    encoded_jucys_murphy_operator,
    select_audit_sectors,
    standard_young_tableaux,
    tableau_content_vector,
    transposition_matrix,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_MULTIPLICITY_COMMUTANT_PATH = Path(
    "research/representation/coset_multiplicity_commutant_search.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrbitGeneratorRecord:
    id: str
    left_cycle_type: str
    right_cycle_type: str
    support_intersection: int
    maximum_union_support: int
    term_count: int
    term_count_polynomial_bound: str
    hermiticity_residual: float
    diagonal_action_commutator_residual: float


@dataclass(frozen=True)
class MultiplicityCommutantSectorRecord:
    n: int
    left_partition: tuple[int, ...]
    right_partition: tuple[int, ...]
    tensor_dimension: int
    nontrivial_multiplicity_label_count: int
    nontrivial_multiplicity_target_count: int
    maximum_kronecker_multiplicity: int
    generators: list[OrbitGeneratorRecord]
    noncommuting_generator_pair_count: int
    maximum_generator_commutator_norm: float
    low_support_portfolio_noncommuting_label_count: int
    low_support_portfolio_noncommuting_target_count: int
    minimum_positive_low_support_portfolio_commutator_norm: float
    low_support_portfolio_best_coefficients: dict[str, int]
    low_support_portfolio_lcu_normalization: int
    low_support_portfolio_fully_split_label_count: int
    low_support_portfolio_fully_split_target_count: int
    low_support_portfolio_all_blocks_split: bool
    low_support_portfolio_minimum_raw_gap: float
    low_support_portfolio_minimum_lcu_normalized_gap: float
    low_support_fully_splitting_candidate_normalized_gaps: dict[str, float]
    low_support_uniform_formula_coefficients: dict[str, int]
    low_support_uniform_formula_lcu_normalization: int
    low_support_uniform_formula_fully_split_label_count: int
    low_support_uniform_formula_all_blocks_split: bool
    low_support_uniform_formula_minimum_lcu_normalized_gap: float
    coefficient_candidate_count: int
    best_coefficients: dict[str, int]
    best_lcu_normalization: int
    fully_split_label_count: int
    fully_split_target_count: int
    minimum_raw_eigenvalue_gap: float
    minimum_lcu_normalized_eigenvalue_gap: float
    uniform_formula_coefficients: dict[str, int]
    uniform_formula_lcu_normalization: int
    uniform_formula_fully_split_label_count: int
    uniform_formula_all_blocks_split: bool
    uniform_formula_minimum_raw_gap: float
    uniform_formula_minimum_lcu_normalized_gap: float
    target_tableau_spectrum_consistency_residual: float
    all_finite_multiplicity_blocks_split: bool
    inverse_polynomial_gap_proved: bool
    coherent_polynomial_multiplicity_transform_proved: bool
    finite_matrix_search_only: bool
    status: str


@dataclass(frozen=True)
class MultiplicityCommutantReport:
    created_at: str
    theorem_contract: dict[str, object]
    circuit_contract: dict[str, object]
    records: list[MultiplicityCommutantSectorRecord]
    finite_common_low_support_coefficients: list[dict[str, int]]
    best_finite_common_low_support_coefficients: dict[str, int]
    best_finite_common_low_support_minimum_normalized_gap: float
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def _transpositions(partition: tuple[int, ...]) -> tuple[tuple[tuple[int, int], np.ndarray], ...]:
    return tuple(
        ((left, right), transposition_matrix(partition, left, right))
        for left, right in itertools.combinations(range(1, sum(partition) + 1), 2)
    )


@lru_cache(maxsize=None)
def _oriented_three_cycles(
    partition: tuple[int, ...],
) -> tuple[tuple[tuple[int, int, int], np.ndarray], ...]:
    cycles: list[tuple[tuple[int, int, int], np.ndarray]] = []
    for first, second, third in itertools.combinations(range(1, sum(partition) + 1), 3):
        forward = (
            transposition_matrix(partition, first, second)
            @ transposition_matrix(partition, second, third)
        )
        cycles.append(((first, second, third), forward))
        cycles.append(((first, third, second), forward.T))
    return tuple(cycles)


def _orbit_sum(
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
    generator_id: str,
    support_intersection: int,
) -> tuple[np.ndarray, int, str, str, int, str]:
    dimension = hook_length_dimension(left_partition) * hook_length_dimension(right_partition)
    operator = np.zeros((dimension, dimension))
    term_count = 0
    if generator_id.startswith("ORB-TT-"):
        left_rows = _transpositions(left_partition)
        right_rows = _transpositions(right_partition)
        left_type, right_type, support_bound = "2", "2", 4
        polynomial_bound = "O(n^4)"
    else:
        left_rows = _transpositions(left_partition)
        right_rows = _oriented_three_cycles(right_partition)
        left_type, right_type, support_bound = "2", "3", 5
        polynomial_bound = "O(n^5)"
    for left_support, left_matrix in left_rows:
        left_set = set(left_support)
        for right_support, right_matrix in right_rows:
            if len(left_set.intersection(right_support)) != support_intersection:
                continue
            operator += np.kron(left_matrix, right_matrix)
            term_count += 1
    return operator, term_count, left_type, right_type, support_bound, polynomial_bound


def bounded_support_orbit_generators(
    left_partition: tuple[int, ...], right_partition: tuple[int, ...]
) -> tuple[list[str], list[np.ndarray], list[OrbitGeneratorRecord]]:
    n = sum(left_partition)
    if n != sum(right_partition):
        raise ValueError("partitions must have equal size")
    specifications = [
        ("ORB-TT-DISJOINT", 0),
        ("ORB-TT-INTERSECTION-1", 1),
        ("ORB-TC-INTERSECTION-0", 0),
        ("ORB-TC-INTERSECTION-1", 1),
        ("ORB-TC-INTERSECTION-2", 2),
    ]
    names: list[str] = []
    operators: list[np.ndarray] = []
    records: list[OrbitGeneratorRecord] = []
    diagonal_generators = [
        np.kron(left, right)
        for left, right in zip(
            adjacent_transposition_matrices(left_partition),
            adjacent_transposition_matrices(right_partition),
        )
    ]
    for generator_id, intersection in specifications:
        operator, term_count, left_type, right_type, support_bound, polynomial_bound = _orbit_sum(
            left_partition, right_partition, generator_id, intersection
        )
        if term_count == 0:
            continue
        names.append(generator_id)
        operators.append(operator)
        records.append(
            OrbitGeneratorRecord(
                id=generator_id,
                left_cycle_type=left_type,
                right_cycle_type=right_type,
                support_intersection=intersection,
                maximum_union_support=support_bound - intersection,
                term_count=term_count,
                term_count_polynomial_bound=polynomial_bound,
                hermiticity_residual=float(np.linalg.norm(operator - operator.T)),
                diagonal_action_commutator_residual=float(
                    max(
                        (
                            np.linalg.norm(operator @ diagonal - diagonal @ operator)
                            for diagonal in diagonal_generators
                        ),
                        default=0.0,
                    )
                ),
            )
        )
    return names, operators, records


def transposition_three_cycle_intersection_operator(
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
    support_intersection: int = 2,
) -> tuple[np.ndarray, int]:
    """Return the fixed transposition/3-cycle orbit sum used by gap scaling."""

    operator, term_count, _, _, _, _ = _orbit_sum(
        left_partition,
        right_partition,
        f"ORB-TC-INTERSECTION-{support_intersection}",
        support_intersection,
    )
    return operator, term_count


def _encoded_label_targets(n: int, base: int) -> dict[int, tuple[int, ...]]:
    labels: dict[int, tuple[int, ...]] = {}
    for target in integer_partitions(n):
        for tableau in standard_young_tableaux(target):
            content = tableau_content_vector(tableau)
            encoded = sum((value + n) * base**index for index, value in enumerate(content[1:]))
            if encoded in labels:
                raise ArithmeticError("content vector encoding is not injective")
            labels[encoded] = target
    return labels


def _coefficient_candidates(generator_count: int, bound: int = 2):
    for coefficients in itertools.product(range(-bound, bound + 1), repeat=generator_count):
        if not any(coefficients):
            continue
        first = next(value for value in coefficients if value)
        if first < 0:
            continue
        yield coefficients


def audit_multiplicity_commutant_sector(
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
    coefficient_bound: int = 2,
) -> MultiplicityCommutantSectorRecord:
    n = sum(left_partition)
    names, operators, generator_records = bounded_support_orbit_generators(
        left_partition, right_partition
    )
    yjm = diagonal_jucys_murphy_operators(left_partition, right_partition)
    base = 2 * n + 1
    encoded = encoded_jucys_murphy_operator(yjm, base, n)
    eigenvalues, eigenvectors = np.linalg.eigh(encoded)
    label_indices: dict[int, list[int]] = {}
    for index, value in enumerate(eigenvalues):
        label_indices.setdefault(round(float(value)), []).append(index)
    target_by_label = _encoded_label_targets(n, base)
    nontrivial = {label: indices for label, indices in label_indices.items() if len(indices) > 1}
    restricted = {
        label: [eigenvectors[:, indices].T @ operator @ eigenvectors[:, indices] for operator in operators]
        for label, indices in nontrivial.items()
    }
    target_by_label = _encoded_label_targets(n, base)
    term_counts = [record.term_count for record in generator_records]
    candidates = list(_coefficient_candidates(len(operators), coefficient_bound))
    best_score: tuple[int, float, int] | None = None
    best_coefficients: tuple[int, ...] = tuple(0 for _ in operators)
    best_gaps: dict[int, float] = {}
    best_spectra: dict[int, np.ndarray] = {}
    best_alpha = 0
    for coefficients in candidates:
        alpha = sum(abs(value) * term_count for value, term_count in zip(coefficients, term_counts))
        split_count = 0
        gaps: dict[int, float] = {}
        spectra: dict[int, np.ndarray] = {}
        normalized_minimum = math.inf
        for label, blocks in restricted.items():
            spectrum = np.linalg.eigvalsh(
                sum(value * block for value, block in zip(coefficients, blocks))
            )
            gap = float(min(np.diff(spectrum), default=math.inf))
            gaps[label] = gap
            spectra[label] = spectrum
            if gap > 1e-7:
                split_count += 1
            normalized_minimum = min(normalized_minimum, gap / alpha)
        score = (split_count, normalized_minimum, -sum(abs(value) for value in coefficients))
        if best_score is None or score > best_score:
            best_score = score
            best_coefficients = coefficients
            best_gaps = gaps
            best_spectra = spectra
            best_alpha = alpha

    uniform_coefficients = tuple(
        1 if name == "ORB-TC-INTERSECTION-2" else 0 for name in names
    )
    uniform_alpha = sum(
        abs(value) * term_count
        for value, term_count in zip(uniform_coefficients, term_counts)
    )
    uniform_gaps: dict[int, float] = {}
    for label, blocks in restricted.items():
        spectrum = np.linalg.eigvalsh(
            sum(value * block for value, block in zip(uniform_coefficients, blocks))
        )
        uniform_gaps[label] = float(min(np.diff(spectrum), default=math.inf))
    uniform_split_count = sum(gap > 1e-7 for gap in uniform_gaps.values())
    uniform_minimum_raw_gap = min(uniform_gaps.values(), default=0.0)
    uniform_minimum_normalized_gap = (
        uniform_minimum_raw_gap / uniform_alpha if uniform_alpha else 0.0
    )

    target_spectra: dict[tuple[int, ...], np.ndarray] = {}
    consistency_residual = 0.0
    split_targets: set[tuple[int, ...]] = set()
    for label, spectrum in best_spectra.items():
        target = target_by_label[label]
        if best_gaps[label] > 1e-7:
            split_targets.add(target)
        if target in target_spectra:
            consistency_residual = max(
                consistency_residual,
                float(np.linalg.norm(spectrum - target_spectra[target])),
            )
        else:
            target_spectra[target] = spectrum

    pair_commutators = [
        float(np.linalg.norm(operators[left] @ operators[right] - operators[right] @ operators[left]))
        for left in range(len(operators))
        for right in range(left + 1, len(operators))
    ]
    low_support_names = ("ORB-TC-INTERSECTION-2", "ORB-TT-INTERSECTION-1")
    low_support_indices = [names.index(name) for name in low_support_names]
    low_support_commutators = {
        label: float(
            np.linalg.norm(
                blocks[low_support_indices[0]] @ blocks[low_support_indices[1]]
                - blocks[low_support_indices[1]] @ blocks[low_support_indices[0]]
            )
        )
        for label, blocks in restricted.items()
    }
    low_support_noncommuting_labels = {
        label for label, norm in low_support_commutators.items() if norm > 1e-7
    }
    low_support_candidates = list(_coefficient_candidates(2, coefficient_bound))
    low_support_term_counts = [term_counts[index] for index in low_support_indices]
    low_support_best_score: tuple[int, float, int] | None = None
    low_support_best_coefficients = (0, 0)
    low_support_best_gaps: dict[int, float] = {}
    low_support_best_alpha = 0
    low_support_splitting_candidates: dict[str, float] = {}
    for coefficients in low_support_candidates:
        alpha = sum(
            abs(value) * term_count
            for value, term_count in zip(coefficients, low_support_term_counts)
        )
        gaps: dict[int, float] = {}
        normalized_minimum = math.inf
        for label, blocks in restricted.items():
            spectrum = np.linalg.eigvalsh(
                sum(
                    value * blocks[index]
                    for value, index in zip(coefficients, low_support_indices)
                )
            )
            gap = float(min(np.diff(spectrum), default=math.inf))
            gaps[label] = gap
            normalized_minimum = min(normalized_minimum, gap / alpha)
        split_count = sum(gap > 1e-7 for gap in gaps.values())
        if split_count == len(restricted):
            low_support_splitting_candidates[
                f"{coefficients[0]},{coefficients[1]}"
            ] = normalized_minimum
        score = (
            split_count,
            normalized_minimum,
            -sum(abs(value) for value in coefficients),
        )
        if low_support_best_score is None or score > low_support_best_score:
            low_support_best_score = score
            low_support_best_coefficients = coefficients
            low_support_best_gaps = gaps
            low_support_best_alpha = alpha
    low_support_split_targets = {
        target_by_label[label]
        for label, gap in low_support_best_gaps.items()
        if gap > 1e-7
    }
    low_support_uniform_coefficients = (1, 1)
    low_support_uniform_alpha = sum(low_support_term_counts)
    low_support_uniform_gaps: dict[int, float] = {}
    for label, blocks in restricted.items():
        spectrum = np.linalg.eigvalsh(
            sum(
                value * blocks[index]
                for value, index in zip(
                    low_support_uniform_coefficients, low_support_indices
                )
            )
        )
        low_support_uniform_gaps[label] = float(
            min(np.diff(spectrum), default=math.inf)
        )
    multiplicities = [
        kronecker_coefficient(left_partition, right_partition, target)
        for target in integer_partitions(n)
    ]
    fully_split = bool(nontrivial) and all(gap > 1e-7 for gap in best_gaps.values())
    minimum_raw_gap = min(best_gaps.values(), default=0.0)
    minimum_normalized_gap = minimum_raw_gap / best_alpha if best_alpha else 0.0
    return MultiplicityCommutantSectorRecord(
        n=n,
        left_partition=left_partition,
        right_partition=right_partition,
        tensor_dimension=hook_length_dimension(left_partition) * hook_length_dimension(right_partition),
        nontrivial_multiplicity_label_count=len(nontrivial),
        nontrivial_multiplicity_target_count=len({target_by_label[label] for label in nontrivial}),
        maximum_kronecker_multiplicity=max(multiplicities),
        generators=generator_records,
        noncommuting_generator_pair_count=sum(value > 1e-7 for value in pair_commutators),
        maximum_generator_commutator_norm=max(pair_commutators, default=0.0),
        low_support_portfolio_noncommuting_label_count=len(
            low_support_noncommuting_labels
        ),
        low_support_portfolio_noncommuting_target_count=len(
            {target_by_label[label] for label in low_support_noncommuting_labels}
        ),
        minimum_positive_low_support_portfolio_commutator_norm=min(
            (
                norm
                for norm in low_support_commutators.values()
                if norm > 1e-7
            ),
            default=0.0,
        ),
        low_support_portfolio_best_coefficients=dict(
            zip(low_support_names, low_support_best_coefficients)
        ),
        low_support_portfolio_lcu_normalization=low_support_best_alpha,
        low_support_portfolio_fully_split_label_count=sum(
            gap > 1e-7 for gap in low_support_best_gaps.values()
        ),
        low_support_portfolio_fully_split_target_count=len(
            low_support_split_targets
        ),
        low_support_portfolio_all_blocks_split=(
            bool(nontrivial)
            and all(gap > 1e-7 for gap in low_support_best_gaps.values())
        ),
        low_support_portfolio_minimum_raw_gap=min(
            low_support_best_gaps.values(), default=0.0
        ),
        low_support_portfolio_minimum_lcu_normalized_gap=(
            min(low_support_best_gaps.values(), default=0.0)
            / low_support_best_alpha
            if low_support_best_alpha
            else 0.0
        ),
        low_support_fully_splitting_candidate_normalized_gaps=(
            low_support_splitting_candidates
        ),
        low_support_uniform_formula_coefficients=dict(
            zip(low_support_names, low_support_uniform_coefficients)
        ),
        low_support_uniform_formula_lcu_normalization=low_support_uniform_alpha,
        low_support_uniform_formula_fully_split_label_count=sum(
            gap > 1e-7 for gap in low_support_uniform_gaps.values()
        ),
        low_support_uniform_formula_all_blocks_split=(
            bool(nontrivial)
            and all(gap > 1e-7 for gap in low_support_uniform_gaps.values())
        ),
        low_support_uniform_formula_minimum_lcu_normalized_gap=(
            min(low_support_uniform_gaps.values(), default=0.0)
            / low_support_uniform_alpha
            if low_support_uniform_alpha
            else 0.0
        ),
        coefficient_candidate_count=len(candidates),
        best_coefficients=dict(zip(names, best_coefficients)),
        best_lcu_normalization=best_alpha,
        fully_split_label_count=sum(gap > 1e-7 for gap in best_gaps.values()),
        fully_split_target_count=len(split_targets),
        minimum_raw_eigenvalue_gap=minimum_raw_gap,
        minimum_lcu_normalized_eigenvalue_gap=minimum_normalized_gap,
        uniform_formula_coefficients=dict(zip(names, uniform_coefficients)),
        uniform_formula_lcu_normalization=uniform_alpha,
        uniform_formula_fully_split_label_count=uniform_split_count,
        uniform_formula_all_blocks_split=(
            bool(nontrivial) and uniform_split_count == len(nontrivial)
        ),
        uniform_formula_minimum_raw_gap=uniform_minimum_raw_gap,
        uniform_formula_minimum_lcu_normalized_gap=uniform_minimum_normalized_gap,
        target_tableau_spectrum_consistency_residual=consistency_residual,
        all_finite_multiplicity_blocks_split=fully_split,
        inverse_polynomial_gap_proved=False,
        coherent_polynomial_multiplicity_transform_proved=False,
        finite_matrix_search_only=True,
        status=(
            "finite-simple-commutant-spectrum-gap-theorem-open"
            if fully_split
            else "bounded-support-commutant-leaves-finite-degeneracy"
        ),
    )


def build_multiplicity_commutant_report(
    n_values: Sequence[int] = (5, 6, 7), coefficient_bound: int = 2
) -> MultiplicityCommutantReport:
    records = []
    for n in n_values:
        sectors = select_audit_sectors(n)
        # The maximum-dimension and maximum-multiplicity selectors often agree.
        for left, right in sectors:
            records.append(
                audit_multiplicity_commutant_sector(
                    left, right, coefficient_bound=coefficient_bound
                )
            )
    all_split = all(record.all_finite_multiplicity_blocks_split for record in records)
    common_low_support_keys = set(
        records[0].low_support_fully_splitting_candidate_normalized_gaps
    )
    for record in records[1:]:
        common_low_support_keys.intersection_update(
            record.low_support_fully_splitting_candidate_normalized_gaps
        )
    common_low_support_gaps = {
        key: min(
            record.low_support_fully_splitting_candidate_normalized_gaps[key]
            for record in records
        )
        for key in common_low_support_keys
    }
    best_common_key = max(
        common_low_support_gaps,
        key=lambda key: (common_low_support_gaps[key], key),
        default=None,
    )
    common_low_support_coefficients = [
        dict(zip(("ORB-TC-INTERSECTION-2", "ORB-TT-INTERSECTION-1"), map(int, key.split(","))))
        for key in sorted(common_low_support_keys)
    ]
    best_common_coefficients = (
        dict(
            zip(
                ("ORB-TC-INTERSECTION-2", "ORB-TT-INTERSECTION-1"),
                map(int, best_common_key.split(",")),
            )
        )
        if best_common_key is not None
        else {}
    )
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "maximum_n": max(n_values),
        "bounded_support_commutant_block_encoding_count": 1,
        "finite_all_block_split_count": sum(
            record.all_finite_multiplicity_blocks_split for record in records
        ),
        "inverse_polynomial_gap_theorem_count": 0,
        "coherent_polynomial_multiplicity_transform_count": 0,
        "kcopy_associator_count": 0,
        "hidden_involution_decoder_count": 0,
        "maximum_kronecker_multiplicity": max(
            record.maximum_kronecker_multiplicity for record in records
        ),
        "maximum_tensor_dimension": max(record.tensor_dimension for record in records),
        "minimum_observed_lcu_normalized_gap": min(
            record.minimum_lcu_normalized_eigenvalue_gap for record in records
        ),
        "uniform_formula_all_block_split_count": sum(
            record.uniform_formula_all_blocks_split for record in records
        ),
        "minimum_uniform_formula_lcu_normalized_gap": min(
            record.uniform_formula_minimum_lcu_normalized_gap for record in records
        ),
        "maximum_target_tableau_spectrum_consistency_residual": max(
            record.target_tableau_spectrum_consistency_residual for record in records
        ),
        "maximum_noncommuting_generator_pair_count": max(
            record.noncommuting_generator_pair_count for record in records
        ),
        "maximum_finite_typical_source_dimension": max(
            hook_length_dimension(record.left_partition) for record in records
        ),
        "maximum_nontrivial_multiplicity_label_count": max(
            record.nontrivial_multiplicity_label_count for record in records
        ),
        "finite_low_support_portfolio_all_block_split_count": sum(
            record.low_support_portfolio_all_blocks_split for record in records
        ),
        "maximum_low_support_portfolio_noncommuting_target_count": max(
            record.low_support_portfolio_noncommuting_target_count
            for record in records
        ),
        "minimum_finite_low_support_portfolio_lcu_normalized_gap": min(
            record.low_support_portfolio_minimum_lcu_normalized_gap
            for record in records
        ),
        "finite_low_support_uniform_formula_all_block_split_count": sum(
            record.low_support_uniform_formula_all_blocks_split
            for record in records
        ),
        "minimum_finite_low_support_uniform_formula_lcu_normalized_gap": min(
            record.low_support_uniform_formula_minimum_lcu_normalized_gap
            for record in records
        ),
        "finite_common_low_support_coefficient_rule_count": len(
            common_low_support_keys
        ),
        "best_finite_common_low_support_minimum_normalized_gap": (
            common_low_support_gaps.get(best_common_key, 0.0)
        ),
    }
    return MultiplicityCommutantReport(
        created_at=utc_now(),
        theorem_contract={
            "commutant_operator": (
                "A_O=sum_(a,b in simultaneous-conjugacy orbit O) rho_lambda(a) tensor rho_mu(b)"
            ),
            "diagonal_action_commutation": (
                "Conjugation by rho_lambda(g) tensor rho_mu(g) permutes orbit terms, so [A_O,rho_diag(g)]=0."
            ),
            "multiplicity_action": (
                "By Schur's lemma A_O=direct_sum_nu I_(V_nu) tensor M_(O,nu)."
            ),
            "searched_support": (
                "disjoint and shared-point (2,2), plus support-intersection-stratified (2,3) permutation pairs"
            ),
            "uniform_formula": "H_n=ORB-TC-INTERSECTION-2 with coefficient one for every n and sector",
            "orbit_term_bound": "O(n^5)",
            "simple_finite_spectrum_is_asymptotic_gap_theorem": False,
        },
        circuit_contract={
            "block_encoding": (
                "Enumerate O(n^5) bounded-support orbit terms and SELECT controlled Young-basis group actions via "
                "the S_n QFT and reversible multiplication."
            ),
            "lcu_normalization_charged": True,
            "phase_estimation_cost": "polynomial only if the LCU-normalized multiplicity eigenvalue gap is inverse polynomial",
            "finite_dense_diagonalization_used_by_uniform_circuit": False,
            "unproved_requirement": "all-n inverse-polynomial normalized gap on every reduction-relevant sector",
        },
        records=records,
        finite_common_low_support_coefficients=common_low_support_coefficients,
        best_finite_common_low_support_coefficients=best_common_coefficients,
        best_finite_common_low_support_minimum_normalized_gap=(
            common_low_support_gaps.get(best_common_key, 0.0)
        ),
        headline_metrics=metrics,
        claim_gate={
            "bounded_support_commutant_block_encoding_polynomial": True,
            "finite_all_multiplicity_blocks_split": all_split,
            "inverse_polynomial_normalized_gap_proved": False,
            "coherent_polynomial_multiplicity_transform_proved": False,
            "kcopy_associator_polynomial_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Bounded-support commutant Hamiltonians split every audited finite multiplicity block, but no all-n "
                "inverse-polynomial normalized gap, associator, transition filter, or decoder theorem is known."
            ),
        },
        status=(
            "finite-multiplicity-basis-witness-gap-and-decoder-open"
            if all_split
            else "bounded-support-commutant-family-incomplete"
        ),
        summary=(
            f"Searched polynomial-description commutant Hamiltonians on {len(records)} sectors through n={max(n_values)}; "
            f"{sum(record.all_finite_multiplicity_blocks_split for record in records)} split every finite multiplicity block."
        ),
        falsifiers_triggered=[
            "Finite simple multiplicity spectra do not prove an inverse-polynomial all-n spectral gap.",
            "Noncommuting commutant generators require one explicit combined Hamiltonian rather than simultaneous measurement.",
            "A multiplicity basis for one coupling does not implement overlapping Racah associators.",
            "No hidden-involution decoder follows from a basis construction alone.",
        ],
    )


def write_multiplicity_commutant_report(
    output_path: Path = COSET_MULTIPLICITY_COMMUTANT_PATH,
    n_values: Sequence[int] = (5, 6, 7),
    coefficient_bound: int = 2,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        build_multiplicity_commutant_report(
            n_values=n_values, coefficient_bound=coefficient_bound
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FINITE-COMMUTANT-SPLITTING-AS-POLY-TRANSFORM",
                source=str(output_path),
                claim=(
                    "A finite simple spectrum of a bounded-support commutant Hamiltonian proves a scalable polynomial "
                    "Kronecker multiplicity transform."
                ),
                reason_invalid=(
                    "Phase-estimation complexity depends on the LCU-normalized minimum eigenvalue gap. The finite "
                    "search supplies no inverse-polynomial all-n lower bound on reduction-relevant sectors."
                ),
                lesson=(
                    "Search for an exactly solvable commutant algebra or prove normalized gap concentration before "
                    "treating finite multiplicity splitting as a circuit primitive."
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
                artifacts={"coset_multiplicity_commutant_search": str(output_path)},
            )
        )
    return payload
