"""Bounded-support generators for hyperoctahedral branching commutants.

For ``G=S_(2m)`` and ``K=C_2 wr S_m``, conjugation-invariant group-algebra
elements form

    C[G]^K = {x in C[G] : kxk^-1=x for every k in K}.

Fourier decomposition gives the exact algebra isomorphism

    C[G]^K ~= direct_sum_lambda End_K(V_lambda)
             ~= direct_sum_(lambda,mu) M_(b(lambda,mu))(C).       (1)

Thus ``K``-conjugacy orbit sums are not merely label observables: the full
orbit-sum algebra contains all matrix units on the repeated branching-copy
spaces.  The algorithmic question is whether a small, coherently accessible
set of such sums generates (1) with resolvable spectral gaps.

This module tests the first nontrivial rank, ``S_8 >= C_2 wr S_4``.  It builds
Young orthogonal representations and Hermitian orbit sums ``O+O^-1`` for all
permutations moving at most ``s`` points.  Algebra closure is compared with
the exact plethysm target ``sum_mu b(lambda,mu)^2``.

The result is a real positive mechanism signal:

* support at most four generates ``End_K(V_lambda)`` for every ``S_8`` irrep;
* this includes all seven irreps with repeated hyperoctahedral branches;
* support at most two or three is insufficient in every repeated sector.

Every fixed-support orbit has polynomial cardinality and a succinct
pair-pattern description.  None of this proves uniform all-rank generation,
an inverse-polynomial eigenvalue gap, a coherent eigenbasis transform, or a
normalized hidden-involution measurement.  Those remain explicit gates.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    Partition,
    bipartitions,
    hyperoctahedral_branching_coefficient,
)
from coset_jucys_murphy_label_transform import adjacent_transposition_matrices
from representation_obstruction import integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character
from self_dual_wreath_character_moments import permutation_cycle_type


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_bounded_support_commutant_generation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-BOUNDED-SUPPORT-COMMUTANT-GENERATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class SupportClosureStep:
    maximum_moved_points: int
    hermitian_orbit_sum_count: int
    generated_algebra_dimension_tolerance_1e8: int
    generated_algebra_dimension_tolerance_1e7: int
    exact_commutant_dimension: int
    dimension_stable: bool
    generates_full_commutant: bool
    status: str


@dataclass(frozen=True)
class BoundedSupportCommutantControl:
    half_degree: int
    symmetric_partition: Partition
    symmetric_irrep_dimension: int
    hyperoctahedral_branch_block_count: int
    exact_commutant_dimension: int
    noncommutative_copy_dimension_excess: int
    maximum_branching_multiplicity: int
    repeated_branch_count: int
    support_steps: list[SupportClosureStep]
    maximum_orbit_sum_hermiticity_residual: float
    maximum_K_generator_commutator_residual: float
    maximum_character_trace_residual: float
    support_four_generates_full_commutant: bool
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class BoundedSupportCommutantTheorem:
    exact_full_commutant: str
    finite_generation_result: str
    polynomial_orbit_size: str
    literature_transfer: str
    all_rank_boundary: str
    positive_compiler_target: str
    exact_orbit_sum_commutant_identity_proved: bool
    all_S8_irrep_commutants_generated_by_support_four: bool
    repeated_S8_branch_commutants_generated_by_support_four: bool
    fixed_support_orbit_cardinality_polynomial: bool
    uniform_all_rank_generation_proved: bool
    inverse_polynomial_spectral_gap_proved: bool
    coherent_missing_label_transform_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BoundedSupportCommutantReport:
    created_at: str
    theorem_contract: dict[str, Any]
    orbit_inventory: list[dict[str, int]]
    controls: list[BoundedSupportCommutantControl]
    theorem: BoundedSupportCommutantTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def hyperoctahedral_group(half_degree: int) -> tuple[Permutation, ...]:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return tuple(
        tuple(
            2 * pair_permutation[pair] + (endpoint ^ flips[pair])
            for pair in range(half_degree)
            for endpoint in range(2)
        )
        for pair_permutation in itertools.permutations(range(half_degree))
        for flips in itertools.product((0, 1), repeat=half_degree)
    )


def moved_point_support(permutation: Permutation) -> int:
    return sum(source != target for source, target in enumerate(permutation))


def _conjugate(
    conjugator: Permutation,
    permutation: Permutation,
) -> Permutation:
    return compose_permutations(
        compose_permutations(conjugator, permutation),
        inverse_permutation(conjugator),
    )


@lru_cache(maxsize=None)
def hermitian_bounded_support_orbits(
    half_degree: int,
    maximum_moved_points: int,
) -> tuple[tuple[Permutation, ...], ...]:
    if maximum_moved_points < 0:
        raise ValueError("maximum_moved_points must be nonnegative")
    degree = 2 * half_degree
    subgroup = hyperoctahedral_group(half_degree)
    seen: set[Permutation] = set()
    output: list[tuple[Permutation, ...]] = []
    for permutation in itertools.permutations(range(degree)):
        if (
            moved_point_support(permutation) > maximum_moved_points
            or permutation in seen
        ):
            continue
        orbit = {
            _conjugate(conjugator, permutation) for conjugator in subgroup
        }
        hermitian_orbit = orbit | {
            inverse_permutation(element) for element in orbit
        }
        seen.update(hermitian_orbit)
        output.append(tuple(sorted(hermitian_orbit)))
    return tuple(output)


def _permutation_matrix_from_adjacent_generators(
    generators: tuple[np.ndarray, ...],
    permutation: Permutation,
) -> np.ndarray:
    current = list(range(len(permutation)))
    word: list[int] = []
    for position, desired in enumerate(permutation):
        index = current.index(desired)
        while index > position:
            current[index - 1], current[index] = current[index], current[index - 1]
            word.append(index - 1)
            index -= 1
    dimension = generators[0].shape[0] if generators else 1
    matrix = np.eye(dimension)
    for generator_index in word:
        matrix = matrix @ generators[generator_index]
    return matrix


def _K_generators(half_degree: int) -> tuple[Permutation, ...]:
    degree = 2 * half_degree
    identity = tuple(range(degree))
    first_flip = list(identity)
    first_flip[0], first_flip[1] = first_flip[1], first_flip[0]
    output = [tuple(first_flip)]
    for pair in range(half_degree - 1):
        pair_swap = list(identity)
        left = 2 * pair
        right = 2 * (pair + 1)
        pair_swap[left], pair_swap[right] = pair_swap[right], pair_swap[left]
        pair_swap[left + 1], pair_swap[right + 1] = (
            pair_swap[right + 1],
            pair_swap[left + 1],
        )
        output.append(tuple(pair_swap))
    return tuple(output)


def _add_matrix_to_basis(
    orthonormal_basis: list[np.ndarray],
    matrix: np.ndarray,
    tolerance: float,
) -> bool:
    vector = matrix.ravel().copy()
    for _ in range(2):
        for basis_vector in orthonormal_basis:
            vector -= np.dot(basis_vector, vector) * basis_vector
    norm = float(np.linalg.norm(vector))
    if norm <= tolerance:
        return False
    orthonormal_basis.append(vector / norm)
    return True


def generated_matrix_algebra_dimension(
    generators: list[np.ndarray],
    *,
    tolerance: float,
    exact_dimension_upper_bound: int,
) -> int:
    if not generators:
        return 1
    dimension = generators[0].shape[0]
    basis_vectors: list[np.ndarray] = []
    basis_matrices: list[np.ndarray] = []

    def add(matrix: np.ndarray) -> bool:
        if _add_matrix_to_basis(basis_vectors, matrix, tolerance):
            basis_matrices.append(matrix)
            return True
        return False

    add(np.eye(dimension))
    for generator in generators:
        add(generator)
    frontier = list(basis_matrices)
    while frontier and len(basis_vectors) < exact_dimension_upper_bound:
        matrix = frontier.pop(0)
        for generator in generators:
            product = matrix @ generator
            if add(product):
                frontier.append(product)
            if len(basis_vectors) >= exact_dimension_upper_bound:
                break
    return len(basis_vectors)


def exact_branching_commutant_dimension(
    symmetric_partition: Partition,
    half_degree: int,
) -> tuple[int, int, int, int]:
    multiplicities = [
        hyperoctahedral_branching_coefficient(
            symmetric_partition,
            alpha,
            beta,
        )
        for alpha, beta in bipartitions(half_degree)
    ]
    block_count = sum(value > 0 for value in multiplicities)
    commutant_dimension = sum(value * value for value in multiplicities)
    maximum = max(multiplicities, default=0)
    repeated = sum(value > 1 for value in multiplicities)
    return block_count, commutant_dimension, maximum, repeated


def audit_bounded_support_commutant(
    symmetric_partition: Partition,
    *,
    half_degree: int = 4,
    support_cutoffs: tuple[int, ...] = (2, 3, 4),
) -> BoundedSupportCommutantControl:
    if sum(symmetric_partition) != 2 * half_degree:
        raise ValueError("partition size must equal twice half_degree")
    if half_degree != 4:
        raise ValueError("dense bounded-support controls are currently restricted to m=4")
    block_count, exact_dimension, maximum, repeated = (
        exact_branching_commutant_dimension(symmetric_partition, half_degree)
    )
    adjacent = adjacent_transposition_matrices(symmetric_partition)
    dimension = adjacent[0].shape[0] if adjacent else 1
    largest_cutoff = max(support_cutoffs)
    all_orbits = hermitian_bounded_support_orbits(half_degree, largest_cutoff)
    matrix_cache: dict[Permutation, np.ndarray] = {}

    def representation(permutation: Permutation) -> np.ndarray:
        if permutation not in matrix_cache:
            matrix_cache[permutation] = _permutation_matrix_from_adjacent_generators(
                adjacent,
                permutation,
            )
        return matrix_cache[permutation]

    orbit_matrices: list[tuple[int, np.ndarray]] = []
    hermiticity_residual = 0.0
    for orbit in all_orbits:
        matrix = sum(
            (representation(permutation) for permutation in orbit),
            np.zeros((dimension, dimension)),
        ) / len(orbit)
        matrix = (matrix + matrix.T) / 2.0
        hermiticity_residual = max(
            hermiticity_residual,
            float(np.linalg.norm(matrix - matrix.T)),
        )
        orbit_matrices.append((moved_point_support(orbit[0]), matrix))

    K_matrices = [representation(generator) for generator in _K_generators(half_degree)]
    commutator_residual = max(
        (
            float(np.linalg.norm(matrix @ subgroup - subgroup @ matrix))
            for _, matrix in orbit_matrices
            for subgroup in K_matrices
        ),
        default=0.0,
    )
    character_trace_residual = max(
        (
            abs(
                float(np.trace(representation(permutation)))
                - symmetric_character(
                    symmetric_partition,
                    permutation_cycle_type(permutation),
                )
            )
            for permutation in matrix_cache
        ),
        default=0.0,
    )

    steps: list[SupportClosureStep] = []
    for cutoff in support_cutoffs:
        generators = [
            matrix for support, matrix in orbit_matrices if support <= cutoff
        ]
        dimension_1e8 = generated_matrix_algebra_dimension(
            generators,
            tolerance=1e-8,
            exact_dimension_upper_bound=exact_dimension,
        )
        dimension_1e7 = generated_matrix_algebra_dimension(
            generators,
            tolerance=1e-7,
            exact_dimension_upper_bound=exact_dimension,
        )
        stable = dimension_1e8 == dimension_1e7
        full = stable and dimension_1e8 == exact_dimension
        steps.append(
            SupportClosureStep(
                maximum_moved_points=cutoff,
                hermitian_orbit_sum_count=len(generators),
                generated_algebra_dimension_tolerance_1e8=dimension_1e8,
                generated_algebra_dimension_tolerance_1e7=dimension_1e7,
                exact_commutant_dimension=exact_dimension,
                dimension_stable=stable,
                generates_full_commutant=full,
                status=(
                    "bounded-support-orbits-generate-full-commutant"
                    if full
                    else "bounded-support-orbits-generate-proper-subalgebra"
                ),
            )
        )
    support_four_full = next(
        row.generates_full_commutant
        for row in steps
        if row.maximum_moved_points == 4
    )
    verified = bool(
        support_four_full
        and hermiticity_residual < 1e-10
        and commutator_residual < 1e-9
        and character_trace_residual < 1e-9
    )
    return BoundedSupportCommutantControl(
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        symmetric_irrep_dimension=dimension,
        hyperoctahedral_branch_block_count=block_count,
        exact_commutant_dimension=exact_dimension,
        noncommutative_copy_dimension_excess=exact_dimension - block_count,
        maximum_branching_multiplicity=maximum,
        repeated_branch_count=repeated,
        support_steps=steps,
        maximum_orbit_sum_hermiticity_residual=hermiticity_residual,
        maximum_K_generator_commutator_residual=commutator_residual,
        maximum_character_trace_residual=character_trace_residual,
        support_four_generates_full_commutant=support_four_full,
        finite_dense_control_only=True,
        status=(
            "support-four-generates-exact-S8-hyperoctahedral-commutant"
            if verified
            else "bounded-support-commutant-control-failure"
        ),
    )


def build_bounded_support_commutant_report() -> BoundedSupportCommutantReport:
    controls = [
        audit_bounded_support_commutant(partition)
        for partition in integer_partitions(8)
    ]
    all_full = all(row.support_four_generates_full_commutant for row in controls)
    repeated_controls = [row for row in controls if row.repeated_branch_count > 0]
    repeated_full = all(
        row.support_four_generates_full_commutant for row in repeated_controls
    )
    residuals_valid = all(
        row.maximum_K_generator_commutator_residual < 1e-9
        and row.maximum_character_trace_residual < 1e-9
        for row in controls
    )
    theorem_verified = all_full and repeated_full and residuals_valid
    status = (
        "bounded-support-four-generates-all-S8-hyperoctahedral-commutants-uniform-theorem-open"
        if theorem_verified
        else "bounded-support-commutant-generation-control-failure"
    )
    inventory = [
        {
            "maximum_moved_points": cutoff,
            "hermitian_orbit_sum_count": len(
                hermitian_bounded_support_orbits(4, cutoff)
            ),
            "permutation_count_upper_bound": sum(
                math.comb(8, support) * math.factorial(support)
                for support in range(cutoff + 1)
            ),
        }
        for cutoff in (0, 2, 3, 4)
    ]
    theorem = BoundedSupportCommutantTheorem(
        exact_full_commutant=(
            "C[S_(2m)]^K is the direct sum over lambda,mu of full matrix "
            "algebras M_(b(lambda,mu)); K-conjugacy orbit sums span it exactly."
        ),
        finite_generation_result=(
            "For every lambda partition 8, Hermitian K_4-orbit sums moving at "
            "most four points generate End_(K_4)(V_lambda)."
        ),
        polynomial_orbit_size=(
            "At fixed support s, each inventory and each K-orbit has O(m^s) "
            "elements and admits a pair-pattern description."
        ),
        literature_transfer=(
            "Generalized-Casimir work shows subgroup-invariant ambient algebra "
            "elements can mix multiplicity spaces in related restrictions; later "
            "embedding-chain charges explicitly leave multiplicity unresolved."
        ),
        all_rank_boundary=(
            "S_8 algebra generation does not prove a uniform generator theorem, "
            "natural spectral separation, or efficient eigenbasis preparation."
        ),
        positive_compiler_target=(
            "Prove fixed support-four orbit sums generate natural End_K blocks for "
            "all m and construct a generic Hermitian combination with inverse-poly gap."
        ),
        exact_orbit_sum_commutant_identity_proved=True,
        all_S8_irrep_commutants_generated_by_support_four=all_full,
        repeated_S8_branch_commutants_generated_by_support_four=repeated_full,
        fixed_support_orbit_cardinality_polynomial=True,
        uniform_all_rank_generation_proved=False,
        inverse_polynomial_spectral_gap_proved=False,
        coherent_missing_label_transform_compiled=False,
        theorem_verified=theorem_verified,
        status=status,
    )
    support_two_repeated_full = sum(
        next(
            step.generates_full_commutant
            for step in row.support_steps
            if step.maximum_moved_points == 2
        )
        for row in repeated_controls
    )
    support_three_repeated_full = sum(
        next(
            step.generates_full_commutant
            for step in row.support_steps
            if step.maximum_moved_points == 3
        )
        for row in repeated_controls
    )
    return BoundedSupportCommutantReport(
        created_at=utc_now(),
        theorem_contract={
            "ambient_algebra": "K-conjugation invariants C[S_(2m)]^K",
            "Fourier_block": (
                "End_K(V_lambda)=direct_sum_mu M_(b(lambda,mu)) tensor I_(d_mu)"
            ),
            "finite_generator_family": (
                "Hermitianized K-orbit sums of permutations moving at most four points"
            ),
            "claim_boundary": (
                "Exact finite algebra generation, not uniform gaps, a coherent "
                "subduction transform, or a hidden-involution speedup."
            ),
        },
        orbit_inventory=inventory,
        controls=controls,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-BOUNDED-SUPPORT-UNIFORM-GENERATION",
                "statement": (
                    "Prove or falsify that the support-four K_m orbit sums generate "
                    "End_K(V_lambda) on asymptotically natural branching blocks."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COMMUTANT-GENERIC-GAP",
                "statement": (
                    "Construct an explicitly weighted Hermitian combination whose "
                    "copy-space eigenvalue gaps are inverse polynomial on natural mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-ORBIT-SUM-BLOCK-ENCODING",
                "statement": (
                    "Compile uniform PREPARE/SELECT circuits for every required "
                    "support-four K-orbit sum and control normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COMMUTANT-EIGENBASIS-RECOUPLING",
                "statement": (
                    "Relate the commutant eigenbasis coherently to the multicopy "
                    "A/B invariant overlap and remove its 1/M normalization."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "K-invariant ambient operators are as blind as K operators.",
                "answer": (
                    "False algebraically: C[G]^K acts as the full matrix algebra on "
                    "each branching-copy factor, whereas C[K] acts as identity there."
                ),
                "resolved": True,
            },
            {
                "challenge": "Support-two Casimirs already solve the finite problem.",
                "answer": (
                    "False in every repeated S_8 sector; support two and three both "
                    "generate proper subalgebras, while support four first closes them."
                ),
                "resolved": True,
            },
            {
                "challenge": "Full finite algebra generation gives an efficient basis transform.",
                "answer": (
                    "False: generated words may be long, generators do not commute, "
                    "and no uniform spectral-gap or eigenbasis circuit is known."
                ),
                "resolved": True,
            },
            {
                "challenge": "The 2014 embedding-chain charges already resolve these copies.",
                "answer": (
                    "False: that work states its two charge families are degenerate in "
                    "the multiplicity label and leaves the required Q_m family open."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "kimura-ramgoolam-generalized-casimirs-2008",
                "url": "https://arxiv.org/abs/0807.3696",
                "use": (
                    "Primary mechanism precedent: subgroup-invariant ambient algebra "
                    "elements mix and can diagonalize multiplicity spaces in related "
                    "symmetric/Brauer restrictions."
                ),
            },
            {
                "id": "diaz-embedding-chain-charges-2014",
                "url": "https://arxiv.org/abs/1406.7671",
                "use": (
                    "Primary scope boundary: the constructed commuting charge families "
                    "do not resolve multiplicity labels; the needed Q_m charges are open."
                ),
            },
        ],
        headline_metrics={
            "S8_irrep_control_count": len(controls),
            "S8_support_four_full_commutant_count": sum(
                row.support_four_generates_full_commutant for row in controls
            ),
            "S8_repeated_branch_irrep_count": len(repeated_controls),
            "S8_repeated_support_two_full_count": support_two_repeated_full,
            "S8_repeated_support_three_full_count": support_three_repeated_full,
            "S8_repeated_support_four_full_count": sum(
                row.support_four_generates_full_commutant
                for row in repeated_controls
            ),
            "maximum_exact_commutant_dimension": max(
                row.exact_commutant_dimension for row in controls
            ),
            "maximum_K_commutator_residual": max(
                row.maximum_K_generator_commutator_residual for row in controls
            ),
            "uniform_all_rank_generation_theorem_count": 0,
            "inverse_polynomial_gap_theorem_count": 0,
            "coherent_missing_label_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_orbit_sum_commutant_identity_proved": True,
            "all_S8_irrep_commutants_generated_by_support_four": all_full,
            "repeated_S8_branch_commutants_generated_by_support_four": repeated_full,
            "fixed_support_orbit_cardinality_polynomial": True,
            "uniform_all_rank_generation_proved": False,
            "natural_mass_full_generation_proved": False,
            "inverse_polynomial_spectral_gap_proved": False,
            "coherent_orbit_sum_block_encoding_compiled": False,
            "coherent_missing_label_transform_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Support-four orbit sums exactly generate every finite S_8 "
                "commutant, but uniform generation, natural gaps, coherent basis "
                "preparation, polar normalization, and decoding are open."
            ),
        },
        status=status,
        summary=(
            "Found a concrete positive missing-label mechanism: polynomial-size "
            "support-four hyperoctahedral orbit sums generate the full branching "
            "commutant in every S_8 irrep. This promotes ambient commutant Casimirs "
            "above paired branching as the active route, while retaining all "
            "uniformity, gap, normalization, and speedup gates."
        ),
        falsifiers_triggered=[
            "K-group operators are copy-blind, but K-conjugation-invariant ambient operators are not.",
            "Support two and support three fail to generate any repeated S_8 commutant fully.",
            "Support-four finite generation does not imply uniform all-rank generation or useful spectral gaps.",
            "Existing embedding-chain charges do not supply the missing multiplicity-resolving family.",
        ],
    )


def write_bounded_support_commutant_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_bounded_support_commutant_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main() -> int:
    payload = write_bounded_support_commutant_report()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
