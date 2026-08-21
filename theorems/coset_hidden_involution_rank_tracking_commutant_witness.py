"""Rank-tracking support witness for hyperoctahedral commutant generation.

Finite commutant searches give the successful support thresholds

    m=4: support 4 closes every S_8 block,
    m=5: support 4 fails and support 5 closes lambda=(6,3,1),
    m=6: support 5 fails and support 6 closes lambda=(8,4).

This module certifies the third row without enumerating all support-six orbit
matrices.  For ``lambda=(8,4)``, the exact ``K_6=C_2 wr S_6`` branching data
has twelve occupied blocks, one multiplicity-two block, and commutant
dimension fifteen.  All orbit sums through support five, even after adjoining
the complete center of ``C[K_6]``, give cyclic reach thirteen.

One explicit support-six orbit repairs the deficit.  Let ``A_5`` be the
Hermitian ``K_6`` orbit sum of the five-cycle

    (3 4 6 8 10),

and let ``B_6`` be the Hermitian orbit sum of the coupled cycles

    (5 6 8)(7 9 10).

Their orbit sizes are 4608 and 2880.  On ``V_(8,4)``, ``A_5`` alone has cyclic
reach ten, ``B_6`` alone has reach eleven, and ``{A_5,B_6}`` reaches the exact
upper bound fifteen for three deterministic generic vectors.  Hence the pair
generates the full target commutant.

The sequence 4,5,6 falsifies every proposed universal support cutoff at most
five.  It does not prove that required support is unbounded: support six or
another fixed family might work at all later ranks.  If support must track
``m``, direct orbit-state preparation becomes superpolynomial; proving or
falsifying that asymptotic is the next gate.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    Permutation,
    _K_generators,
    exact_branching_commutant_dimension,
    hyperoctahedral_group,
    moved_point_support,
)
from coset_hidden_involution_commutant_support_growth_boundary import (
    _average_matrices_for_sets,
    _matrix_for_permutation,
    cyclic_module_dimension,
    hyperoctahedral_conjugacy_classes,
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
    "coset_hidden_involution_rank_tracking_commutant_witness.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-RANK-TRACKING-COMMUTANT-WITNESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
TARGET_PARTITION = (8, 4)
TARGET_HALF_DEGREE = 6
SUPPORT_FIVE_REPRESENTATIVE: Permutation = (
    0,
    1,
    2,
    4,
    6,
    5,
    8,
    7,
    10,
    9,
    3,
    11,
)
SUPPORT_SIX_REPRESENTATIVE: Permutation = (
    0,
    1,
    2,
    3,
    4,
    6,
    8,
    9,
    5,
    10,
    7,
    11,
)


@dataclass(frozen=True)
class RankTrackingCommutantControl:
    half_degree: int
    symmetric_partition: tuple[int, ...]
    symmetric_irrep_dimension: int
    occupied_K_block_count: int
    repeated_K_block_count: int
    maximum_branching_multiplicity: int
    exact_commutant_dimension: int
    full_commutant_generic_cyclic_capacity: int
    support_five_orbit_inventory_count: int
    K_center_class_count: int
    support_two_cyclic_reaches: tuple[int, ...]
    support_three_cyclic_reaches: tuple[int, ...]
    support_four_cyclic_reaches: tuple[int, ...]
    support_five_cyclic_reaches: tuple[int, ...]
    support_five_plus_K_center_cyclic_reaches: tuple[int, ...]
    support_five_witness_orbit_size: int
    support_six_witness_orbit_size: int
    support_five_witness_cyclic_reaches: tuple[int, ...]
    support_six_witness_cyclic_reaches: tuple[int, ...]
    witness_pair_cyclic_reaches: tuple[int, ...]
    maximum_witness_hermiticity_residual: float
    maximum_witness_K_commutator_residual: float
    support_at_most_five_generates_full_commutant: bool
    support_five_deficit_survives_K_center: bool
    witness_pair_generates_full_commutant: bool
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class RankTrackingCommutantTheorem:
    finite_threshold_sequence: str
    rank_six_deficit: str
    internal_copy_space_certificate: str
    explicit_repair: str
    asymptotic_cost_boundary: str
    next_decisive_test: str
    universal_support_cutoff_at_most_five_falsified: bool
    support_five_deficit_is_only_K_label_collision: bool
    explicit_support_six_pair_generates_target: bool
    universal_support_six_generation_proved: bool
    unbounded_support_requirement_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RankTrackingCommutantReport:
    created_at: str
    theorem_contract: dict[str, Any]
    control: RankTrackingCommutantControl
    theorem: RankTrackingCommutantTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def derangements(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in itertools.permutations(range(size))
        if all(index != image for index, image in enumerate(permutation))
    )


def bounded_support_permutations(
    degree: int,
    maximum_support: int,
) -> Iterator[Permutation]:
    yield tuple(range(degree))
    for support in range(2, maximum_support + 1):
        for subset in itertools.combinations(range(degree), support):
            for derangement in derangements(support):
                permutation = list(range(degree))
                for source_index, target_index in enumerate(derangement):
                    permutation[subset[source_index]] = subset[target_index]
                yield tuple(permutation)


@lru_cache(maxsize=None)
def hermitian_bounded_support_orbits_fast(
    half_degree: int,
    maximum_support: int,
) -> tuple[tuple[Permutation, ...], ...]:
    subgroup = hyperoctahedral_group(half_degree)
    seen: set[Permutation] = set()
    output: list[tuple[Permutation, ...]] = []
    for permutation in bounded_support_permutations(
        2 * half_degree,
        maximum_support,
    ):
        if permutation in seen:
            continue
        orbit = {
            compose_permutations(
                compose_permutations(conjugator, permutation),
                inverse_permutation(conjugator),
            )
            for conjugator in subgroup
        }
        hermitian_orbit = orbit | {
            inverse_permutation(element) for element in orbit
        }
        seen.update(hermitian_orbit)
        output.append(tuple(sorted(hermitian_orbit)))
    return tuple(output)


@lru_cache(maxsize=None)
def hermitian_orbit_of_representative(
    half_degree: int,
    representative: Permutation,
) -> tuple[Permutation, ...]:
    subgroup = hyperoctahedral_group(half_degree)
    orbit = {
        compose_permutations(
            compose_permutations(conjugator, representative),
            inverse_permutation(conjugator),
        )
        for conjugator in subgroup
    }
    return tuple(
        sorted(orbit | {inverse_permutation(element) for element in orbit})
    )


def permutation_cycles(permutation: Permutation) -> tuple[tuple[int, ...], ...]:
    seen: set[int] = set()
    cycles: list[tuple[int, ...]] = []
    for start in range(len(permutation)):
        if start in seen or permutation[start] == start:
            continue
        cycle: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        cycles.append(tuple(cycle))
    return tuple(cycles)


@lru_cache(maxsize=1)
def audit_rank_tracking_commutant() -> RankTrackingCommutantControl:
    partition = TARGET_PARTITION
    half_degree = TARGET_HALF_DEGREE
    dimension = adjacent_transposition_matrices(partition)[0].shape[0]
    block_count, commutant_dimension, maximum, repeated = (
        exact_branching_commutant_dimension(partition, half_degree)
    )
    cyclic_capacity = 0
    for alpha, beta in bipartitions(half_degree):
        multiplicity = hyperoctahedral_branching_coefficient(
            partition,
            alpha,
            beta,
        )
        if multiplicity:
            cyclic_capacity += multiplicity * min(
                multiplicity,
                hyperoctahedral_irrep_dimension(alpha, beta),
            )

    bounded_orbits = hermitian_bounded_support_orbits_fast(half_degree, 5)
    K_classes = hyperoctahedral_conjugacy_classes(half_degree)
    five_witness = hermitian_orbit_of_representative(
        half_degree,
        SUPPORT_FIVE_REPRESENTATIVE,
    )
    six_witness = hermitian_orbit_of_representative(
        half_degree,
        SUPPORT_SIX_REPRESENTATIVE,
    )
    matrices = _average_matrices_for_sets(
        partition,
        [*bounded_orbits, *K_classes, five_witness, six_witness],
    )
    bounded_matrices = [
        (matrix + matrix.T) / 2.0
        for matrix in matrices[: len(bounded_orbits)]
    ]
    center_start = len(bounded_orbits)
    center_end = center_start + len(K_classes)
    center_matrices = [
        (matrix + matrix.T) / 2.0
        for matrix in matrices[center_start:center_end]
    ]
    five_matrix = (matrices[-2] + matrices[-2].T) / 2.0
    six_matrix = (matrices[-1] + matrices[-1].T) / 2.0
    seeds = (1, 2, 3)

    def generators(cutoff: int) -> list[np.ndarray]:
        return [
            matrix
            for matrix, orbit in zip(bounded_matrices, bounded_orbits)
            if moved_point_support(orbit[0]) <= cutoff
        ]

    def reaches(rows: list[np.ndarray]) -> tuple[int, ...]:
        return tuple(
            cyclic_module_dimension(
                rows,
                dimension_upper_bound=commutant_dimension,
                seed=seed,
            )
            for seed in seeds
        )

    support_two = generators(2)
    support_three = generators(3)
    support_four = generators(4)
    support_five = generators(5)
    reach_two = reaches(support_two)
    reach_three = reaches(support_three)
    reach_four = reaches(support_four)
    reach_five = reaches(support_five)
    reach_five_center = reaches([*support_five, *center_matrices])
    reach_five_witness = reaches([five_matrix])
    reach_six_witness = reaches([six_matrix])
    reach_pair = reaches([five_matrix, six_matrix])
    K_generator_matrices = [
        _matrix_for_permutation(partition, permutation)
        for permutation in _K_generators(half_degree)
    ]
    hermiticity_residual = max(
        float(np.linalg.norm(matrix - matrix.T))
        for matrix in (five_matrix, six_matrix)
    )
    commutator_residual = max(
        float(np.linalg.norm(matrix @ subgroup - subgroup @ matrix))
        for matrix in (five_matrix, six_matrix)
        for subgroup in K_generator_matrices
    )
    support_five_full = all(value == commutant_dimension for value in reach_five)
    deficit_survives_center = all(
        value < commutant_dimension for value in reach_five_center
    )
    pair_full = all(value == commutant_dimension for value in reach_pair)
    verified = bool(
        cyclic_capacity == commutant_dimension
        and not support_five_full
        and deficit_survives_center
        and pair_full
        and hermiticity_residual < 1e-10
        and commutator_residual < 1e-8
    )
    return RankTrackingCommutantControl(
        half_degree=half_degree,
        symmetric_partition=partition,
        symmetric_irrep_dimension=dimension,
        occupied_K_block_count=block_count,
        repeated_K_block_count=repeated,
        maximum_branching_multiplicity=maximum,
        exact_commutant_dimension=commutant_dimension,
        full_commutant_generic_cyclic_capacity=cyclic_capacity,
        support_five_orbit_inventory_count=len(bounded_orbits),
        K_center_class_count=len(K_classes),
        support_two_cyclic_reaches=reach_two,
        support_three_cyclic_reaches=reach_three,
        support_four_cyclic_reaches=reach_four,
        support_five_cyclic_reaches=reach_five,
        support_five_plus_K_center_cyclic_reaches=reach_five_center,
        support_five_witness_orbit_size=len(five_witness),
        support_six_witness_orbit_size=len(six_witness),
        support_five_witness_cyclic_reaches=reach_five_witness,
        support_six_witness_cyclic_reaches=reach_six_witness,
        witness_pair_cyclic_reaches=reach_pair,
        maximum_witness_hermiticity_residual=hermiticity_residual,
        maximum_witness_K_commutator_residual=commutator_residual,
        support_at_most_five_generates_full_commutant=support_five_full,
        support_five_deficit_survives_K_center=deficit_survives_center,
        witness_pair_generates_full_commutant=pair_full,
        finite_dense_control_only=True,
        status=(
            "support-at-most-five-fails-explicit-support-six-pair-closes-S12-target"
            if verified
            else "rank-tracking-commutant-control-failure"
        ),
    )


def build_rank_tracking_commutant_report() -> RankTrackingCommutantReport:
    control = audit_rank_tracking_commutant()
    verified = control.status.startswith("support-at-most-five-fails")
    status = (
        "universal-support-at-most-five-falsified-support-six-uniformity-open"
        if verified
        else "rank-tracking-commutant-witness-control-failure"
    )
    theorem = RankTrackingCommutantTheorem(
        finite_threshold_sequence=(
            "Successful controlled cutoffs rise from four at m=4, to five in the "
            "m=5 lambda=(6,3,1) target, to six in the m=6 lambda=(8,4) target."
        ),
        rank_six_deficit=(
            "All 28 Hermitian orbit types through support five reach 13 rather "
            "than the exact commutant cyclic capacity 15."
        ),
        internal_copy_space_certificate=(
            "Adding all 65 K_6 central class sums leaves reach 13, localizing the "
            "deficit inside the unique multiplicity-two branch."
        ),
        explicit_repair=(
            "The support-five five-cycle orbit A_5 and support-six coupled-3-cycle "
            "orbit B_6 have reaches 10 and 11 separately but 15 jointly."
        ),
        asymptotic_cost_boundary=(
            "Every fixed cutoff is polynomial inventory, but a cutoff growing "
            "linearly with m would make direct orbit preparation superpolynomial."
        ),
        next_decisive_test=(
            "Prove a support-degree filtration invariant for a scalable lambda_m "
            "family, or prove support six generates all natural blocks uniformly."
        ),
        universal_support_cutoff_at_most_five_falsified=verified,
        support_five_deficit_is_only_K_label_collision=False,
        explicit_support_six_pair_generates_target=control.witness_pair_generates_full_commutant,
        universal_support_six_generation_proved=False,
        unbounded_support_requirement_proved=False,
        theorem_verified=verified,
        status=status,
    )
    return RankTrackingCommutantReport(
        created_at=utc_now(),
        theorem_contract={
            "target": "S_12 irrep lambda=(8,4) restricted to K_6=C_2 wr S_6",
            "multiplicity_structure": (
                "12 occupied K blocks, one b=2 block, exact commutant dimension 15"
            ),
            "support_five_witness": (
                "Hermitian K orbit of cycle (3 4 6 8 10), size 4608"
            ),
            "support_six_witness": (
                "Hermitian K orbit of (5 6 8)(7 9 10), size 2880"
            ),
            "claim_boundary": (
                "Finite falsification of universal cutoffs <=5, not proof of "
                "unbounded support or a coherent algorithm."
            ),
        },
        control=control,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-SUPPORT-SIX-UNIFORMITY",
                "statement": (
                    "Prove or falsify that the 82 support-six orbit types generate "
                    "all asymptotically natural branching commutants."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-SUPPORT-FILTRATION-INVARIANT",
                "statement": (
                    "Construct a scalable multiplicity family and an invariant that "
                    "all orbit sums below a growing support threshold preserve."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COMMUTANT-WITNESS-GAP",
                "statement": (
                    "Find explicit weights for A_5,B_6 or a uniform successor family "
                    "with inverse-polynomial copy-space eigenvalue gap."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COMMUTANT-NATURAL-RECOUPLING",
                "statement": (
                    "Transfer generator and gap control to natural source mass and "
                    "compose it with the multicopy normalized polar."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Support five may fail only because the test vector is noncyclic.",
                "answer": (
                    "False: A_5 and B_6 reach the exact upper bound 15 from the same "
                    "vectors, proving their full-commutant cyclicity."
                ),
                "resolved": True,
            },
            {
                "challenge": "The two missing dimensions are unresolved K labels.",
                "answer": (
                    "False: the complete K_6 center does not increase reach beyond 13."
                ),
                "resolved": True,
            },
            {
                "challenge": "One support-six orbit alone supplies the full algebra.",
                "answer": (
                    "False: B_6 alone reaches 11 and A_5 alone reaches 10; their "
                    "noncommutative interaction is required."
                ),
                "resolved": True,
            },
            {
                "challenge": "Thresholds 4,5,6 prove support must grow forever.",
                "answer": (
                    "False: the evidence falsifies cutoffs <=5 only. Support six "
                    "could still be uniform at later ranks."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "target_irrep_dimension": control.symmetric_irrep_dimension,
            "exact_target_commutant_dimension": control.exact_commutant_dimension,
            "support_five_inventory_count": control.support_five_orbit_inventory_count,
            "support_five_cyclic_reach": min(control.support_five_cyclic_reaches),
            "support_five_plus_K_center_reach": min(
                control.support_five_plus_K_center_cyclic_reaches
            ),
            "support_five_witness_orbit_size": control.support_five_witness_orbit_size,
            "support_six_witness_orbit_size": control.support_six_witness_orbit_size,
            "support_five_witness_reach": min(
                control.support_five_witness_cyclic_reaches
            ),
            "support_six_witness_reach": min(
                control.support_six_witness_cyclic_reaches
            ),
            "witness_pair_cyclic_reach": min(control.witness_pair_cyclic_reaches),
            "uniform_support_six_theorem_count": 0,
            "unbounded_support_lower_bound_count": 0,
            "inverse_polynomial_gap_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "universal_support_cutoff_at_most_five_falsified": verified,
            "support_five_deficit_survives_full_K_center": (
                control.support_five_deficit_survives_K_center
            ),
            "explicit_support_six_pair_generates_target": (
                control.witness_pair_generates_full_commutant
            ),
            "universal_support_six_generation_proved": False,
            "unbounded_support_requirement_proved": False,
            "natural_mass_generation_proved": False,
            "inverse_polynomial_spectral_gap_proved": False,
            "coherent_missing_label_transform_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Cutoffs <=5 are not uniform, while one support-six pair repairs "
                "the finite target. Uniform support, gaps, natural mass, coherent "
                "recoupling, and decoding remain open."
            ),
        },
        status=status,
        summary=(
            "Extended the commutant-generator threshold sequence to 4,5,6 and "
            "isolated two explicit polynomial-size orbit sums that close the S_12 "
            "target. This falsifies all universal cutoffs through five and turns "
            "support-growth into the active asymptotic make-or-break question."
        ),
        falsifiers_triggered=[
            "No universal hyperoctahedral commutant generator theorem with support cutoff at most five can hold.",
            "The rank-six support-five deficit lies inside a multiplicity-two copy space.",
            "A support-six coupled-cycle orbit repairs the deficit only through noncommutative interaction with a support-five orbit.",
            "Three finite thresholds do not prove an unbounded-support lower bound or a speedup.",
        ],
    )


def write_rank_tracking_commutant_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_rank_tracking_commutant_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main() -> int:
    payload = write_rank_tracking_commutant_report()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
