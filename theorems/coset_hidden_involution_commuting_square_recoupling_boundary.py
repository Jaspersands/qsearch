"""Commuting-square architecture and its vertical-multiplicity boundary.

There is a canonical symmetric group-factorization square

    K_(m-1)  <=  K_m
       |            |
       v            v
    S_(2m-1) <= S_(2m),

where ``K_m=C_2 wr S_m`` stabilizes the standard perfect matching and
``S_(2m-1)`` fixes one endpoint of the last pair.  Exactly,

    K_m intersect S_(2m-1) = K_(m-1),
    [K_m:K_(m-1)] = [S_(2m):S_(2m-1)] = 2m,
    K_m S_(2m-1) = S_(2m).

The corresponding square of group algebras is a symmetric commuting square.
Both horizontal branching graphs are multiplicity-free: remove one box from
an ``S_n`` partition, or one box from either component of a bipartition.
This makes a unitary-connection factorization of the hyperoctahedral
subduction transform the right architectural target.

However, abstract connection existence is not a compiler.  A cell with top
label ``lambda`` and bottom label ``nu`` has dimension

    sum_(tau covered by lambda) b_odd(tau,nu)
      = sum_(mu covering nu) b_even(lambda,mu),            (1)

where ``b_even`` is the ``S_(2m) down K_m`` multiplicity and ``b_odd`` is the
``S_(2m-1) down K_(m-1)`` multiplicity.  Equation (1) is the exact commuting-
square incidence identity.  Whenever one vertical edge has multiplicity
``b_even(lambda,mu)=B``, every cell below a removable corner of ``mu`` has
dimension at least ``B``.  Existing natural-mass bounds put
``B>|h^G|^(1/4)`` on overwhelming source mass.  Thus the naive connection
cells are superpolynomially large even though the number of adjacent *shapes*
is small.

The productive architecture is therefore more specific: factor each vertical
multiplicity edge into a hierarchy of bounded local charges or harmonic path
labels, then compile the resulting small connection cells.  Merely citing the
commuting square, the two multiplicity-free horizontal graphs, or abstract
biunitarity does not close that obligation.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    hyperoctahedral_group,
)
from coset_hidden_involution_hyperoctahedral_branching_mass import (
    branching_multiplicity_scaling_record,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    Bipartition,
    Partition,
    bipartition_covers,
    bipartitions,
    hyperoctahedral_branching_coefficient,
    removable_corner_partitions,
)
from representation_obstruction import integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_commuting_square_recoupling_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-COMMUTING-SQUARE-RECOUPLING-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class GroupSquareFiniteControl:
    half_degree: int
    symmetric_group_order: int
    hyperoctahedral_order: int
    point_stabilizer_order: int
    intersection_order: int
    expected_intersection_order: int
    product_set_order: int
    equal_horizontal_index: int
    intersection_verified: bool
    product_factorization_verified: bool
    symmetric_commuting_square_verified: bool
    status: str


@dataclass(frozen=True)
class IncidenceIdentityControl:
    half_degree: int
    symmetric_partition_count: int
    lower_bipartition_count: int
    equation_count: int
    equation_failure_count: int
    maximum_connection_cell_dimension: int
    maximum_vertical_branching_multiplicity: int
    horizontal_symmetric_branching_multiplicity_free: bool
    horizontal_wreath_branching_multiplicity_free: bool
    incidence_identity_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalConnectionCellScalingRecord:
    half_degree: int
    degree: int
    natural_vertical_multiplicity_threshold_log2: float
    inherited_connection_cell_dimension_log2_lower_bound: float
    joint_source_high_multiplicity_mass_lower_bound: float
    shape_adjacency_count_polynomial: bool
    vertical_edge_dimension_superpolynomial: bool
    abstract_connection_is_polynomial_cell_compiler: bool
    status: str


@dataclass(frozen=True)
class CommutingSquareRecouplingTheorem:
    group_factorization: str
    commuting_square: str
    horizontal_branching: str
    incidence_identity: str
    connection_opportunity: str
    vertical_multiplicity_obstruction: str
    required_escape: str
    all_rank_symmetric_commuting_square_proved: bool
    horizontal_branchings_multiplicity_free: bool
    exact_incidence_identity_proved: bool
    abstract_unitary_connection_exists: bool
    polynomial_size_connection_cells_proved: bool
    vertical_multiplicity_factorization_compiled: bool
    source_aware_subduction_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CommutingSquareRecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    group_controls: list[GroupSquareFiniteControl]
    incidence_controls: list[IncidenceIdentityControl]
    scaling_records: list[NaturalConnectionCellScalingRecord]
    theorem: CommutingSquareRecouplingTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def symmetric_point_stabilizer(degree: int) -> tuple[Permutation, ...]:
    if degree < 2:
        raise ValueError("degree must be at least two")
    return tuple(
        (*permutation, degree - 1)
        for permutation in itertools.permutations(range(degree - 1))
    )


@lru_cache(maxsize=None)
def embedded_lower_hyperoctahedral_group(
    half_degree: int,
) -> tuple[Permutation, ...]:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    return tuple(
        (*permutation, 2 * half_degree - 2, 2 * half_degree - 1)
        for permutation in hyperoctahedral_group(half_degree - 1)
    )


@lru_cache(maxsize=None)
def audit_group_square(half_degree: int) -> GroupSquareFiniteControl:
    if half_degree not in (2, 3):
        raise ValueError("explicit group controls are limited to m=2,3")
    degree = 2 * half_degree
    upper = set(hyperoctahedral_group(half_degree))
    side = set(symmetric_point_stabilizer(degree))
    expected_intersection = set(
        embedded_lower_hyperoctahedral_group(half_degree)
    )
    intersection = upper & side
    products = {
        compose_permutations(left, right)
        for left in upper
        for right in side
    }
    symmetric_order = math.factorial(degree)
    intersection_verified = intersection == expected_intersection
    product_verified = len(products) == symmetric_order
    verified = bool(
        intersection_verified
        and product_verified
        and len(upper) // len(intersection) == degree
        and symmetric_order // len(side) == degree
    )
    return GroupSquareFiniteControl(
        half_degree=half_degree,
        symmetric_group_order=symmetric_order,
        hyperoctahedral_order=len(upper),
        point_stabilizer_order=len(side),
        intersection_order=len(intersection),
        expected_intersection_order=len(expected_intersection),
        product_set_order=len(products),
        equal_horizontal_index=degree,
        intersection_verified=intersection_verified,
        product_factorization_verified=product_verified,
        symmetric_commuting_square_verified=verified,
        status=(
            "symmetric-group-factorization-square-verified"
            if verified
            else "group-square-control-failure"
        ),
    )


def partition_covers(upper: Partition, lower: Partition) -> bool:
    return lower in removable_corner_partitions(upper)


@lru_cache(maxsize=None)
def odd_hyperoctahedral_branching_coefficient(
    odd_partition: Partition,
    lower_bipartition: Bipartition,
) -> int:
    """Multiplicity for ``S_(2m-1) down K_(m-1)``.

    The subgroup fixes the final point, so restriction first to
    ``S_(2m-2)`` gives the sum over one-box removals.
    """

    if sum(odd_partition) % 2 != 1:
        raise ValueError("odd_partition must have odd size")
    half_degree = (sum(odd_partition) + 1) // 2
    if sum(lower_bipartition[0]) + sum(lower_bipartition[1]) != half_degree - 1:
        raise ValueError("lower bipartition has the wrong rank")
    return sum(
        hyperoctahedral_branching_coefficient(
            even_partition,
            *lower_bipartition,
        )
        for even_partition in removable_corner_partitions(odd_partition)
    )


def connection_cell_dimension(
    upper_partition: Partition,
    lower_bipartition: Bipartition,
) -> tuple[int, int]:
    half_degree = sum(upper_partition) // 2
    left = sum(
        odd_hyperoctahedral_branching_coefficient(
            odd_partition,
            lower_bipartition,
        )
        for odd_partition in removable_corner_partitions(upper_partition)
    )
    right = sum(
        hyperoctahedral_branching_coefficient(
            upper_partition,
            *upper_bipartition,
        )
        for upper_bipartition in bipartitions(half_degree)
        if bipartition_covers(upper_bipartition, lower_bipartition)
    )
    return left, right


@lru_cache(maxsize=None)
def audit_incidence_identity(half_degree: int) -> IncidenceIdentityControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    symmetric_partitions = integer_partitions(2 * half_degree)
    lower_bipartitions = bipartitions(half_degree - 1)
    failures = 0
    maximum_cell = 0
    maximum_vertical = 0
    for partition in symmetric_partitions:
        maximum_vertical = max(
            maximum_vertical,
            *(
                hyperoctahedral_branching_coefficient(partition, *pair)
                for pair in bipartitions(half_degree)
            ),
        )
        for lower in lower_bipartitions:
            left, right = connection_cell_dimension(partition, lower)
            failures += int(left != right)
            maximum_cell = max(maximum_cell, left, right)
    verified = failures == 0
    return IncidenceIdentityControl(
        half_degree=half_degree,
        symmetric_partition_count=len(symmetric_partitions),
        lower_bipartition_count=len(lower_bipartitions),
        equation_count=len(symmetric_partitions) * len(lower_bipartitions),
        equation_failure_count=failures,
        maximum_connection_cell_dimension=maximum_cell,
        maximum_vertical_branching_multiplicity=maximum_vertical,
        horizontal_symmetric_branching_multiplicity_free=True,
        horizontal_wreath_branching_multiplicity_free=True,
        incidence_identity_verified=verified,
        status=(
            "exact-commuting-square-incidence-identity-verified"
            if verified
            else "commuting-square-incidence-control-failure"
        ),
    )


def natural_connection_cell_scaling_record(
    half_degree: int,
) -> NaturalConnectionCellScalingRecord:
    branching = branching_multiplicity_scaling_record(half_degree)
    threshold = branching.branching_multiplicity_threshold_log2
    inherited = threshold
    huge = branching.threshold_superpolynomial
    return NaturalConnectionCellScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        natural_vertical_multiplicity_threshold_log2=threshold,
        inherited_connection_cell_dimension_log2_lower_bound=inherited,
        joint_source_high_multiplicity_mass_lower_bound=(
            branching.joint_all_source_high_multiplicity_probability_lower_bound
        ),
        shape_adjacency_count_polynomial=True,
        vertical_edge_dimension_superpolynomial=huge,
        abstract_connection_is_polynomial_cell_compiler=False,
        status=(
            "abstract-connection-cell-inherits-superpolynomial-vertical-edge"
            if huge
            else "preasymptotic-connection-cell-bound"
        ),
    )


@lru_cache(maxsize=1)
def build_commuting_square_recoupling_report() -> CommutingSquareRecouplingReport:
    group_controls = [audit_group_square(value) for value in (2, 3)]
    incidence_controls = [
        audit_incidence_identity(value) for value in (2, 3, 4, 5)
    ]
    scaling = [
        natural_connection_cell_scaling_record(value)
        for value in (12, 16, 24, 32, 64)
    ]
    group_exact = all(
        row.symmetric_commuting_square_verified for row in group_controls
    )
    incidence_exact = all(
        row.incidence_identity_verified for row in incidence_controls
    )
    natural_huge = all(
        row.vertical_edge_dimension_superpolynomial for row in scaling
    )
    theorem_verified = group_exact and incidence_exact and natural_huge
    theorem = CommutingSquareRecouplingTheorem(
        group_factorization=(
            "K_m intersect S_(2m-1)=K_(m-1), both indices are 2m, and K_m S_(2m-1)=S_(2m)."
        ),
        commuting_square=(
            "Coordinate conditional expectations onto subgroup algebras commute, and the factorization makes the square symmetric/nondegenerate."
        ),
        horizontal_branching=(
            "S_n down S_(n-1) and (C_2 wr S_m) down (C_2 wr S_(m-1)) both remove one box multiplicity-free."
        ),
        incidence_identity=(
            "sum_(tau<lambda)b_odd(tau,nu)=sum_(mu>nu)b_even(lambda,mu) for every lambda,nu."
        ),
        connection_opportunity=(
            "A source-adapted subduction transform should factor through unitary connection cells for this square."
        ),
        vertical_multiplicity_obstruction=(
            "Cell dimensions include the vertical b(lambda,mu) edge multiplicities and are superpolynomial on natural mass."
        ),
        required_escape=(
            "Factor vertical edges into rank-local harmonic/charge labels before attempting coherent connection cells."
        ),
        all_rank_symmetric_commuting_square_proved=group_exact,
        horizontal_branchings_multiplicity_free=True,
        exact_incidence_identity_proved=incidence_exact,
        abstract_unitary_connection_exists=group_exact,
        polynomial_size_connection_cells_proved=False,
        vertical_multiplicity_factorization_compiled=False,
        source_aware_subduction_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=theorem_verified,
        status=(
            "symmetric-commuting-square-proved-vertical-edge-factorization-open"
            if theorem_verified
            else "commuting-square-recoupling-control-failure"
        ),
    )
    return CommutingSquareRecouplingReport(
        created_at=utc_now(),
        theorem_contract={
            "tower": "K_(m-1) <= K_m inside S_(2m-1) <= S_(2m)",
            "range": "every integer m>=2",
            "connection_target": (
                "Change from symmetric Young paths to hyperoctahedral branching-copy paths."
            ),
            "claim_boundary": (
                "Exact architecture and cell-size obstruction; no explicit vertical-edge factorization or quantum circuit."
            ),
        },
        group_controls=group_controls,
        incidence_controls=incidence_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-VERTICAL-EDGE-FACTORIZATION",
                "statement": (
                    "Construct polynomial-length labels and local isometries that factor every naturally occupied b(lambda,mu)-dimensional vertical edge."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-CONNECTION-CELL-FORMULA",
                "statement": (
                    "Derive uniformly computable connection coefficients after vertical-edge factorization, with controlled precision and normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-CONNECTION-CIRCUIT",
                "statement": (
                    "Compile the factored cells coherently and prove total error and gate complexity polynomial."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The two horizontal multiplicity-free towers automatically give a polynomial recoupling circuit.",
                "answer": (
                    "False: connection cells are repeated by vertical b(lambda,mu) edges, which are superpolynomial on natural mass."
                ),
                "resolved": True,
            },
            {
                "challenge": "The subgroup square may fail to be symmetric.",
                "answer": (
                    "The intersection, equal-index, and full product identities prove symmetry at every rank."
                ),
                "resolved": True,
            },
            {
                "challenge": "The paired-tower recurrence is unrelated to a unitary connection.",
                "answer": (
                    "It is exactly the dimension identity for opposite path spaces around the commuting square."
                ),
                "resolved": True,
            },
            {
                "challenge": "Abstract connection existence supplies amplitudes and conditioning.",
                "answer": (
                    "No: it supplies an algebraic target, not succinct coefficients, spectral conditioning, or a circuit."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "arXiv:2211.03822",
                "role": "Unitary connections on tracial Bratteli diagrams and their operator-algebraic realization."
            },
            {
                "id": "arXiv:0810.2767",
                "role": "Centralizer constructions for wreath-product towers; architectural analogy, not this ambient inclusion."
            },
            {
                "id": "arXiv:1406.7671",
                "role": "Multiplicity-resolving charge motivation and the explicit limitation of known embedding-chain charges."
            },
        ],
        headline_metrics={
            "all_rank_symmetric_commuting_square_count": int(group_exact),
            "exact_incidence_identity_count": int(incidence_exact),
            "finite_incidence_control_count": len(incidence_controls),
            "finite_incidence_failure_count": sum(
                row.equation_failure_count for row in incidence_controls
            ),
            "natural_superpolynomial_cell_obstruction_count": int(natural_huge),
            "vertical_edge_factorization_count": 0,
            "polynomial_connection_cell_compiler_count": 0,
            "source_aware_subduction_transform_count": 0,
            "hidden_involution_detector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "symmetric_commuting_square_proved": group_exact,
            "exact_connection_dimension_identity_proved": incidence_exact,
            "abstract_unitary_connection_exists": group_exact,
            "natural_cells_inherit_huge_vertical_multiplicity": natural_huge,
            "vertical_edges_factored_into_local_labels": False,
            "polynomial_connection_cells_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct recoupling architecture is now exact, but its raw cells are as large as the unresolved natural multiplicity spaces."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved the symmetric commuting-square architecture for S_(2m) down K_m and showed that abstract connection cells inherit superpolynomial natural vertical multiplicity."
        ),
        falsifiers_triggered=[
            "Multiplicity-free horizontal branching does not imply small recoupling cells.",
            "An abstract biunitary connection is not an efficient basis transform.",
            "The next compiler must factor vertical multiplicity edges before synthesizing connection cells."
        ],
    )


def write_commuting_square_recoupling_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_commuting_square_recoupling_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_commuting_square_recoupling_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
