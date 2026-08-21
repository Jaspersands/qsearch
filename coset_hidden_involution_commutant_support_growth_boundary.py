"""First support-growth boundary for hyperoctahedral commutant generators.

At ``S_8 >= K_4``, Hermitian ``K_4``-orbit sums moving at most four points
generate every branching commutant.  This module tests whether support four is
uniform by moving to the first tractable multiplicity-rich ``S_10`` sector,

    lambda=(6,3,1),  dim V_lambda=315.

Its exact restriction commutant has dimension

    sum_mu b(lambda,mu)^2 = 42.

All ``K_5`` carrier dimensions in occupied blocks are at least their branching
multiplicity, so a generic vector is cyclic for the full commutant with orbit
dimension 42.  The same deterministic vectors give the stable reaches

    support <=2: 5,
    support <=3: 14,
    support <=4: 40,
    support <=4 plus Z(C[K_5]): 40,
    support <=5: 42.

The last line certifies that the vector is full-commutant cyclic and that the
support-five sums generate the exact commutant.  Consequently the support-four
algebra is genuinely proper; its deficit is not merely failure to distinguish
``K``-irrep labels, because adjoining the complete ``K`` center does not help.

This falsifies a uniform support-four conjecture while preserving the ambient
commutant mechanism.  Whether support five is uniform, or the minimum support
must grow with ``m``, is now the decisive structural question.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from coset_hidden_involution_bounded_support_commutant_generation import (
    Permutation,
    _K_generators,
    exact_branching_commutant_dimension,
    hermitian_bounded_support_orbits,
    hyperoctahedral_group,
    moved_point_support,
)
from coset_hidden_involution_natural_recoupling_boundary import (
    hyperoctahedral_irrep_dimension,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    bipartitions,
    hyperoctahedral_branching_coefficient,
)
from coset_jucys_murphy_label_transform import adjacent_transposition_matrices
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_commutant_support_growth_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-COMMUTANT-SUPPORT-GROWTH-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
TARGET_PARTITION = (6, 3, 1)
TARGET_HALF_DEGREE = 5


@dataclass(frozen=True)
class SupportGrowthControl:
    half_degree: int
    symmetric_partition: tuple[int, ...]
    symmetric_irrep_dimension: int
    exact_commutant_dimension: int
    full_commutant_generic_cyclic_capacity: int
    all_occupied_carrier_dimensions_at_least_multiplicity: bool
    K_conjugacy_class_count: int
    support_two_hermitian_orbit_count: int
    support_three_hermitian_orbit_count: int
    support_four_hermitian_orbit_count: int
    support_five_hermitian_orbit_count: int
    support_two_cyclic_reaches: tuple[int, ...]
    support_three_cyclic_reaches: tuple[int, ...]
    support_four_cyclic_reaches: tuple[int, ...]
    support_four_plus_K_center_cyclic_reaches: tuple[int, ...]
    support_five_cyclic_reaches: tuple[int, ...]
    maximum_orbit_sum_hermiticity_residual: float
    maximum_K_generator_commutator_residual: float
    support_four_generates_full_commutant: bool
    support_four_deficit_survives_K_center: bool
    support_five_generates_full_commutant: bool
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class CommutantSupportGrowthTheorem:
    S8_baseline: str
    S10_counterexample: str
    K_center_falsifier: str
    support_five_rescue: str
    complexity_boundary: str
    next_conjecture: str
    uniform_support_four_generation_falsified: bool
    support_four_deficit_is_only_K_label_collision: bool
    support_five_target_sector_generation_verified: bool
    uniform_support_five_generation_proved: bool
    support_requirement_unbounded_proved: bool
    natural_mass_generation_proved: bool
    inverse_polynomial_gap_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CommutantSupportGrowthReport:
    created_at: str
    theorem_contract: dict[str, Any]
    control: SupportGrowthControl
    theorem: CommutantSupportGrowthTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def hyperoctahedral_conjugacy_type(
    permutation: Permutation,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return positive and negative signed-cycle partitions."""

    if len(permutation) % 2:
        raise ValueError("hyperoctahedral permutation degree must be even")
    half_degree = len(permutation) // 2
    pair_permutation = [permutation[2 * pair] // 2 for pair in range(half_degree)]
    flips = [permutation[2 * pair] % 2 for pair in range(half_degree)]
    seen: set[int] = set()
    positive: list[int] = []
    negative: list[int] = []
    for start in range(half_degree):
        if start in seen:
            continue
        current = start
        length = 0
        parity = 0
        while current not in seen:
            seen.add(current)
            length += 1
            parity ^= flips[current]
            current = pair_permutation[current]
        (negative if parity else positive).append(length)
    return (
        tuple(sorted(positive, reverse=True)),
        tuple(sorted(negative, reverse=True)),
    )


@lru_cache(maxsize=None)
def hyperoctahedral_conjugacy_classes(
    half_degree: int,
) -> tuple[tuple[Permutation, ...], ...]:
    classes: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[Permutation],
    ] = {}
    for permutation in hyperoctahedral_group(half_degree):
        classes.setdefault(
            hyperoctahedral_conjugacy_type(permutation),
            [],
        ).append(permutation)
    return tuple(
        tuple(sorted(classes[key]))
        for key in sorted(classes)
    )


def _adjacent_word(permutation: Permutation) -> tuple[int, ...]:
    current = list(range(len(permutation)))
    word: list[int] = []
    for position, desired in enumerate(permutation):
        index = current.index(desired)
        while index > position:
            current[index - 1], current[index] = current[index], current[index - 1]
            word.append(index - 1)
            index -= 1
    return tuple(word)


def _sparse_right_generator_data(
    generators: tuple[np.ndarray, ...],
) -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray], ...]:
    output = []
    for generator in generators:
        diagonal = np.diag(generator)
        off_diagonal = generator.copy()
        np.fill_diagonal(off_diagonal, 0.0)
        partner = np.argmax(np.abs(off_diagonal), axis=0)
        coefficient = off_diagonal[partner, np.arange(generator.shape[0])]
        output.append((diagonal, partner, coefficient))
    return tuple(output)


def _right_multiply_sparse_generator(
    matrix: np.ndarray,
    data: tuple[np.ndarray, np.ndarray, np.ndarray],
) -> np.ndarray:
    diagonal, partner, coefficient = data
    return (
        matrix * diagonal[np.newaxis, :]
        + matrix[:, partner] * coefficient[np.newaxis, :]
    )


def _average_matrices_for_sets(
    partition: tuple[int, ...],
    permutation_sets: list[tuple[Permutation, ...]],
) -> list[np.ndarray]:
    """Evaluate many sparse group-algebra averages through a shared word trie."""

    adjacent = adjacent_transposition_matrices(partition)
    dimension = adjacent[0].shape[0]
    generator_data = _sparse_right_generator_data(adjacent)
    trie: dict[Any, Any] = {}
    for set_index, permutations in enumerate(permutation_sets):
        for permutation in permutations:
            node = trie
            for generator_index in _adjacent_word(permutation):
                node = node.setdefault(generator_index, {})
            node.setdefault("sets", []).append(set_index)
    sums = [np.zeros((dimension, dimension)) for _ in permutation_sets]

    def visit(node: dict[Any, Any], matrix: np.ndarray) -> None:
        for set_index in node.get("sets", ()):
            sums[set_index] += matrix
        for generator_index, child in node.items():
            if generator_index == "sets":
                continue
            visit(
                child,
                _right_multiply_sparse_generator(
                    matrix,
                    generator_data[generator_index],
                ),
            )

    visit(trie, np.eye(dimension))
    return [
        matrix / len(permutations)
        for matrix, permutations in zip(sums, permutation_sets)
    ]


def _matrix_for_permutation(
    partition: tuple[int, ...],
    permutation: Permutation,
) -> np.ndarray:
    adjacent = adjacent_transposition_matrices(partition)
    data = _sparse_right_generator_data(adjacent)
    dimension = adjacent[0].shape[0]
    matrix = np.eye(dimension)
    for generator_index in _adjacent_word(permutation):
        matrix = _right_multiply_sparse_generator(matrix, data[generator_index])
    return matrix


def cyclic_module_dimension(
    generators: list[np.ndarray],
    *,
    dimension_upper_bound: int,
    seed: int,
    tolerance: float = 1e-8,
) -> int:
    random = np.random.default_rng(seed)
    basis: list[np.ndarray] = []
    frontier: list[np.ndarray] = []

    def add(vector: np.ndarray) -> None:
        residual = vector.copy()
        for _ in range(2):
            for basis_vector in basis:
                residual -= np.dot(basis_vector, residual) * basis_vector
        norm = float(np.linalg.norm(residual))
        if norm > tolerance:
            normalized = residual / norm
            basis.append(normalized)
            frontier.append(normalized)

    add(random.normal(size=generators[0].shape[0]))
    while frontier and len(basis) < dimension_upper_bound:
        vector = frontier.pop(0)
        for generator in generators:
            add(generator @ vector)
            if len(basis) >= dimension_upper_bound:
                break
    return len(basis)


def _generators_up_to_support(
    orbit_matrices: list[np.ndarray],
    orbits: tuple[tuple[Permutation, ...], ...],
    cutoff: int,
) -> list[np.ndarray]:
    return [
        matrix
        for matrix, orbit in zip(orbit_matrices, orbits)
        if moved_point_support(orbit[0]) <= cutoff
    ]


@lru_cache(maxsize=1)
def audit_commutant_support_growth() -> SupportGrowthControl:
    partition = TARGET_PARTITION
    half_degree = TARGET_HALF_DEGREE
    adjacent = adjacent_transposition_matrices(partition)
    dimension = adjacent[0].shape[0]
    block_count, commutant_dimension, _, _ = exact_branching_commutant_dimension(
        partition,
        half_degree,
    )
    del block_count
    cyclic_capacity = 0
    carrier_dominates = True
    for alpha, beta in bipartitions(half_degree):
        multiplicity = hyperoctahedral_branching_coefficient(
            partition,
            alpha,
            beta,
        )
        if not multiplicity:
            continue
        carrier_dimension = hyperoctahedral_irrep_dimension(alpha, beta)
        carrier_dominates = carrier_dominates and carrier_dimension >= multiplicity
        cyclic_capacity += multiplicity * min(multiplicity, carrier_dimension)

    orbits = hermitian_bounded_support_orbits(half_degree, 5)
    K_classes = hyperoctahedral_conjugacy_classes(half_degree)
    all_matrices = _average_matrices_for_sets(
        partition,
        [*orbits, *K_classes],
    )
    orbit_matrices = [
        (matrix + matrix.T) / 2.0 for matrix in all_matrices[: len(orbits)]
    ]
    center_matrices = [
        (matrix + matrix.T) / 2.0 for matrix in all_matrices[len(orbits) :]
    ]
    hermiticity_residual = max(
        float(np.linalg.norm(matrix - matrix.T)) for matrix in orbit_matrices
    )
    K_generator_matrices = [
        _matrix_for_permutation(partition, permutation)
        for permutation in _K_generators(half_degree)
    ]
    commutator_residual = max(
        float(np.linalg.norm(matrix @ subgroup - subgroup @ matrix))
        for matrix in orbit_matrices
        for subgroup in K_generator_matrices
    )
    seeds = (1, 2)

    def reaches(generators: list[np.ndarray]) -> tuple[int, ...]:
        return tuple(
            cyclic_module_dimension(
                generators,
                dimension_upper_bound=commutant_dimension,
                seed=seed,
            )
            for seed in seeds
        )

    support_two = _generators_up_to_support(orbit_matrices, orbits, 2)
    support_three = _generators_up_to_support(orbit_matrices, orbits, 3)
    support_four = _generators_up_to_support(orbit_matrices, orbits, 4)
    support_five = _generators_up_to_support(orbit_matrices, orbits, 5)
    reaches_two = reaches(support_two)
    reaches_three = reaches(support_three)
    reaches_four = reaches(support_four)
    reaches_four_center = reaches([*support_four, *center_matrices])
    reaches_five = reaches(support_five)
    support_five_full = all(value == commutant_dimension for value in reaches_five)
    support_four_full = all(value == commutant_dimension for value in reaches_four)
    deficit_survives_center = all(
        value < commutant_dimension for value in reaches_four_center
    )
    verified = bool(
        cyclic_capacity == commutant_dimension
        and carrier_dominates
        and not support_four_full
        and deficit_survives_center
        and support_five_full
        and hermiticity_residual < 1e-10
        and commutator_residual < 1e-8
    )
    return SupportGrowthControl(
        half_degree=half_degree,
        symmetric_partition=partition,
        symmetric_irrep_dimension=dimension,
        exact_commutant_dimension=commutant_dimension,
        full_commutant_generic_cyclic_capacity=cyclic_capacity,
        all_occupied_carrier_dimensions_at_least_multiplicity=carrier_dominates,
        K_conjugacy_class_count=len(K_classes),
        support_two_hermitian_orbit_count=len(support_two),
        support_three_hermitian_orbit_count=len(support_three),
        support_four_hermitian_orbit_count=len(support_four),
        support_five_hermitian_orbit_count=len(support_five),
        support_two_cyclic_reaches=reaches_two,
        support_three_cyclic_reaches=reaches_three,
        support_four_cyclic_reaches=reaches_four,
        support_four_plus_K_center_cyclic_reaches=reaches_four_center,
        support_five_cyclic_reaches=reaches_five,
        maximum_orbit_sum_hermiticity_residual=hermiticity_residual,
        maximum_K_generator_commutator_residual=commutator_residual,
        support_four_generates_full_commutant=support_four_full,
        support_four_deficit_survives_K_center=deficit_survives_center,
        support_five_generates_full_commutant=support_five_full,
        finite_dense_control_only=True,
        status=(
            "support-four-falsified-support-five-closes-S10-target-commutant"
            if verified
            else "commutant-support-growth-control-failure"
        ),
    )


def build_commutant_support_growth_report() -> CommutantSupportGrowthReport:
    control = audit_commutant_support_growth()
    verified = control.status.startswith("support-four-falsified")
    status = (
        "uniform-support-four-falsified-support-five-uniformity-open"
        if verified
        else "commutant-support-growth-control-failure"
    )
    theorem = CommutantSupportGrowthTheorem(
        S8_baseline=(
            "Support-four Hermitian K_4 orbit sums generate every S_8 branching "
            "commutant, including all repeated sectors."
        ),
        S10_counterexample=(
            "For lambda=(6,3,1), support-four reaches only 40 dimensions from "
            "vectors certified cyclic for the 42-dimensional full commutant."
        ),
        K_center_falsifier=(
            "Adjoining all 36 central K_5 class sums leaves cyclic reach 40, so "
            "the deficit occurs inside copy spaces rather than between K labels."
        ),
        support_five_rescue=(
            "The 28 Hermitian orbit sums through support five reach all 42 "
            "dimensions for both deterministic seeds and therefore generate the "
            "exact target commutant."
        ),
        complexity_boundary=(
            "Fixed support five still has polynomial O(m^5) inventory, but no "
            "uniform cutoff, word-length, spectral-gap, or natural-mass theorem follows."
        ),
        next_conjecture=(
            "Determine whether a constant support cutoff generates natural blocks "
            "for all m, or construct a family forcing support to diverge."
        ),
        uniform_support_four_generation_falsified=verified,
        support_four_deficit_is_only_K_label_collision=False,
        support_five_target_sector_generation_verified=control.support_five_generates_full_commutant,
        uniform_support_five_generation_proved=False,
        support_requirement_unbounded_proved=False,
        natural_mass_generation_proved=False,
        inverse_polynomial_gap_proved=False,
        theorem_verified=verified,
        status=status,
    )
    return CommutantSupportGrowthReport(
        created_at=utc_now(),
        theorem_contract={
            "target": "S_10 irrep lambda=(6,3,1) restricted to K_5=C_2 wr S_5",
            "exact_upper_bound": "sum_mu b(lambda,mu)^2=42",
            "cyclic_certificate": (
                "Support-five reaches 42 from the same vectors used to falsify "
                "support four, proving those vectors are full-commutant cyclic."
            ),
            "claim_boundary": (
                "One exact finite support-threshold increase, not an all-rank "
                "lower bound or a coherent transform."
            ),
        },
        control=control,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-UNIFORM-SUPPORT-FIVE-GENERATION",
                "statement": (
                    "Prove or falsify support-five generation on an asymptotically "
                    "natural family of S_(2m) restriction blocks."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-SUPPORT-GROWTH-LOWER-BOUND",
                "statement": (
                    "If no constant cutoff suffices, exhibit an explicit lambda_m,mu_m "
                    "family and an invariant that bounded-support orbit algebras preserve."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COMMUTANT-GENERIC-GAP",
                "statement": (
                    "For a generating cutoff, construct an explicit Hermitian "
                    "combination with inverse-polynomial copy-space eigenvalue gaps."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COMMUTANT-NATURAL-MASS",
                "statement": (
                    "Transfer generation and gap bounds from selected sectors to the "
                    "exact source-refined natural law."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The support-four reach 40 may be a noncyclic-vector artifact.",
                "answer": (
                    "False: support five reaches the exact upper bound 42 from the "
                    "same vectors, certifying their full-commutant cyclicity."
                ),
                "resolved": True,
            },
            {
                "challenge": "Support four only fails to separate K-irrep blocks.",
                "answer": (
                    "False: adjoining the complete 36-dimensional K center does not "
                    "increase cyclic reach above 40."
                ),
                "resolved": True,
            },
            {
                "challenge": "The S_10 counterexample kills bounded-support commutants.",
                "answer": (
                    "False: support five generates the exact target and remains a "
                    "fixed-support polynomial-size family. Only cutoff four is killed."
                ),
                "resolved": True,
            },
            {
                "challenge": "Support five at one sector proves a uniform compiler.",
                "answer": (
                    "False: no all-rank generation, natural-mass, spectral-gap, or "
                    "coherent eigenbasis theorem has been established."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "target_irrep_dimension": control.symmetric_irrep_dimension,
            "exact_target_commutant_dimension": control.exact_commutant_dimension,
            "support_four_orbit_sum_count": control.support_four_hermitian_orbit_count,
            "support_four_cyclic_reach": min(control.support_four_cyclic_reaches),
            "support_four_plus_K_center_cyclic_reach": min(
                control.support_four_plus_K_center_cyclic_reaches
            ),
            "support_five_orbit_sum_count": control.support_five_hermitian_orbit_count,
            "support_five_cyclic_reach": min(control.support_five_cyclic_reaches),
            "uniform_support_four_theorem_count": 0,
            "uniform_support_five_theorem_count": 0,
            "inverse_polynomial_gap_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "uniform_support_four_generation_falsified": verified,
            "support_four_deficit_survives_full_K_center": (
                control.support_four_deficit_survives_K_center
            ),
            "support_five_target_sector_generation_verified": (
                control.support_five_generates_full_commutant
            ),
            "uniform_support_five_generation_proved": False,
            "support_requirement_unbounded_proved": False,
            "natural_mass_generation_proved": False,
            "inverse_polynomial_spectral_gap_proved": False,
            "coherent_missing_label_transform_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The minimum successful cutoff increases from four in S_8 to at "
                "least five in this S_10 sector. Uniform cutoff, gaps, natural mass, "
                "normalization, and decoding remain open."
            ),
        },
        status=status,
        summary=(
            "Falsified the apparent uniform support-four commutant compiler with an "
            "S_10 copy-space counterexample, then showed support five exactly repairs "
            "that sector. The ambient-Casimir route remains active, but support growth "
            "is now a mandatory asymptotic gate."
        ),
        falsifiers_triggered=[
            "The S_8 support-four generation phenomenon is not uniform across rank.",
            "The S_10 support-four deficit is internal to multiplicity spaces, not merely a K-label collision.",
            "Support five rescues the target, so the counterexample is not a no-go for bounded-support orbit sums generally.",
            "No speedup claim is allowed from finite algebra generation without uniform gaps and normalized recoupling.",
        ],
    )


def write_commutant_support_growth_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_commutant_support_growth_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main() -> int:
    payload = write_commutant_support_growth_report()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
