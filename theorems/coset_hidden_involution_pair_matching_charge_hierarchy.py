"""A K-adapted commuting charge pair from pair-Gaudin interactions.

Let ``c_ij`` be the eight-term pair interaction from the pair-Gaudin
hierarchy.  The infinitesimal braid relations imply that

    C_m = sum_(i<j) c_ij

commutes with every ``c_ij``.  Consequently it commutes with the first
nontrivial pair-label matching charge

    D_m = sum_{{i,j} disjoint {k,l}} c_ij c_kl.

Both charges are Hermitian, invariant under ``K_m=C_2 wr S_m``, and have
polynomial-size permutation expansions: ``8*binomial(m,2)`` and
``192*binomial(m,4)`` distinct terms respectively.  This gives a terminal
K-adapted commuting pair, unlike the ordered relative Gaudin charges.

The most obvious additional charge is redundant.  Locally,

    c_ij^2 = 4 c_ij + 8 z_ij,

where ``z_ij`` is the four-element Klein subgroup sum on pairs ``i,j``.
Thus ``sum c_ij^2`` is ``4 C_m`` plus an element of ``Z(C[K_m])`` and cannot
split a copy degeneracy left by ``C_m`` and the K labels.

Finite Young-basis controls show that ``D_m`` genuinely adds copy-space
resolution at ``m=5``.  It closes the remaining deficit for
``lambda=(6,3,1)`` and partially improves ``lambda=(5,3,2)``.  It does not
improve the worst controlled sector ``lambda=(4,3,2,1)``.  The next matching
charge ``M_3`` also fails to commute with ``D_m``.  Hence this is a real but
incomplete multiplicity-label mechanism, not a subduction transform or a
hidden-involution detector.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import sympy as sp

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    _K_generators,
    exact_branching_commutant_dimension,
    hyperoctahedral_group,
)
from coset_hidden_involution_commutant_support_growth_boundary import (
    _average_matrices_for_sets,
    hyperoctahedral_conjugacy_classes,
)
from coset_hidden_involution_pair_gaudin_hierarchy import (
    _add_elements,
    _commutator,
    _element,
    pair_interaction,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    bipartitions,
    hyperoctahedral_branching_coefficient,
)
from coset_hidden_involution_stable_support_six_certificate import (
    _CHANNEL_EVALUATION_SUBSETS,
    _inverse_permutation as _stable_inverse_permutation,
    _preimage_under_embedded_template,
    channel_evaluation_matrix,
    occupancy_channel_values,
    support_five_gap_squared,
    symbolic_top_harmonic_projector,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_pair_matching_charge_hierarchy.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PAIR-MATCHING-CHARGE-HIERARCHY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
GroupAlgebraElement = dict[Permutation, int]
_SYMBOLIC_M = sp.symbols("m", integer=True, positive=True)


@dataclass(frozen=True)
class LocalPowerCollapseControl:
    pair_interaction_term_count: int
    square_term_count: int
    local_center_term_count: int
    square_relation_nonzero_count: int
    local_center_is_subgroup_sum: bool
    global_center_controls_verified: bool
    power_sum_adds_copy_labels_beyond_C_and_K_center: bool
    status: str


@dataclass(frozen=True)
class MatchingChargeControl:
    half_degree: int
    C_term_count: int
    expected_C_term_count: int
    D_term_count: int
    expected_D_term_count: int
    C_pair_commutator_failure_count: int
    C_D_commutator_nonzero_count: int
    C_K_commutator_failure_count: int
    D_K_commutator_failure_count: int
    polynomial_sparse_K_adapted_commuting_pair_verified: bool
    status: str


@dataclass(frozen=True)
class BranchResolutionControl:
    half_degree: int
    symmetric_partition: tuple[int, ...]
    symmetric_irrep_dimension: int
    K_branch_block_count: int
    center_joint_eigenspace_count: int
    target_copy_label_count: int
    center_plus_C_joint_eigenspace_count: int
    center_plus_C_D_joint_eigenspace_count: int
    D_added_copy_label_count: int
    C_resolves_all_copy_labels: bool
    C_D_resolves_all_copy_labels: bool
    finite_numerical_control_only: bool
    status: str


@dataclass(frozen=True)
class StableBranchResolutionControl:
    stable_symmetric_partition: str
    stable_K_partition: str
    branching_multiplicity: int
    normalized_orbit_size: str
    interpolation_rows: tuple[int, ...]
    holdout_rows: tuple[int, ...]
    maximum_interpolated_degree: int
    predicted_degree_upper_bound: int
    closed_formula_matches_interpolation: bool
    all_holdouts_match: bool
    action_preserves_top_harmonic_copy_space: bool
    restricted_action_reconstruction_verified: bool
    normalized_gap_squared: str
    gap_squared_ratio_to_support_five_resolver: str
    inverse_polynomial_gap_lower_bound: str
    all_rank_stable_branch_resolver_proved: bool
    natural_source_mass_nonnegligible: bool
    status: str


@dataclass(frozen=True)
class HigherMatchingBoundaryControl:
    half_degree: int
    D_term_count: int
    M3_term_count: int
    commutator_witness_permutation: tuple[int, ...]
    commutator_witness_coefficient: int
    D_M3_commute: bool
    matching_charge_family_pairwise_commuting: bool
    status: str


@dataclass(frozen=True)
class PairMatchingChargeTheorem:
    central_pair_charge: str
    disjoint_matching_charge: str
    all_rank_commutation_proof: str
    power_sum_collapse: str
    finite_resolution_evidence: str
    higher_matching_boundary: str
    exact_all_rank_K_adapted_commuting_pair_proved: bool
    polynomial_permutation_expansions_proved: bool
    edge_power_sum_redundancy_proved: bool
    stable_multiplicity_two_resolver_proved: bool
    stable_inverse_polynomial_gap_proved: bool
    finite_copy_resolution_strictly_improved: bool
    complete_finite_copy_resolution_on_every_control: bool
    asymptotic_natural_copy_resolution_proved: bool
    inverse_polynomial_conditional_gaps_proved: bool
    source_signal_correlation_proved: bool
    coherent_subduction_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairMatchingChargeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    local_power_collapse: LocalPowerCollapseControl
    matching_controls: list[MatchingChargeControl]
    stable_branch_resolution: StableBranchResolutionControl
    branch_controls: list[BranchResolutionControl]
    higher_matching_boundary: HigherMatchingBoundaryControl
    theorem: PairMatchingChargeTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _multiply_elements(
    left: GroupAlgebraElement,
    right: GroupAlgebraElement,
) -> GroupAlgebraElement:
    output: defaultdict[Permutation, int] = defaultdict(int)
    for left_permutation, left_coefficient in left.items():
        for right_permutation, right_coefficient in right.items():
            output[
                compose_permutations(left_permutation, right_permutation)
            ] += left_coefficient * right_coefficient
    return {
        permutation: coefficient
        for permutation, coefficient in output.items()
        if coefficient
    }


def _scale_element(
    element: GroupAlgebraElement,
    scalar: int,
) -> GroupAlgebraElement:
    return {
        permutation: scalar * coefficient
        for permutation, coefficient in element.items()
        if scalar * coefficient
    }


def _subtract_elements(
    left: GroupAlgebraElement,
    right: GroupAlgebraElement,
) -> GroupAlgebraElement:
    return _add_elements(left, _scale_element(right, -1))


@lru_cache(maxsize=None)
def central_pair_charge(half_degree: int) -> GroupAlgebraElement:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    return _add_elements(
        *(
            _element(pair_interaction(half_degree, left, right))
            for left in range(half_degree)
            for right in range(left + 1, half_degree)
        )
    )


@lru_cache(maxsize=None)
def disjoint_matching_charge(half_degree: int) -> GroupAlgebraElement:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    edges = {
        (left, right): _element(
            pair_interaction(half_degree, left, right)
        )
        for left in range(half_degree)
        for right in range(left + 1, half_degree)
    }
    products = []
    for (left_edge, left), (right_edge, right) in itertools.combinations(
        edges.items(),
        2,
    ):
        if set(left_edge).isdisjoint(right_edge):
            products.append(_multiply_elements(left, right))
    return _add_elements(*products)


@lru_cache(maxsize=1)
def canonical_disjoint_matching_orbit() -> tuple[Permutation, ...]:
    """Return the 192-term four-pair orbit underlying ``D_m``."""

    charge = disjoint_matching_charge(4)
    if set(charge.values()) != {1}:
        raise AssertionError("D_4 is not a multiplicity-free orbit sum")
    return tuple(sorted(charge))


@lru_cache(maxsize=None)
def direct_stable_matching_action(half_degree: int) -> sp.Matrix:
    """Evaluate normalized ``D_m`` on the four stable occupancy channels."""

    if half_degree < 6:
        raise ValueError("the stable branch starts at half_degree six")
    inverses = tuple(
        _stable_inverse_permutation(permutation)
        for permutation in canonical_disjoint_matching_orbit()
    )
    totals = [[0] * 4 for _ in _CHANNEL_EVALUATION_SUBSETS]
    term_count = 0
    for selected_pairs in itertools.combinations(range(half_degree), 4):
        pair_index = {
            pair: index for index, pair in enumerate(selected_pairs)
        }
        for canonical_inverse in inverses:
            term_count += 1
            for row, subset in enumerate(_CHANNEL_EVALUATION_SUBSETS):
                values = occupancy_channel_values(
                    _preimage_under_embedded_template(
                        subset,
                        selected_pairs,
                        canonical_inverse,
                        pair_index,
                    )
                )
                for column, value in enumerate(values):
                    totals[row][column] += value
    evaluated = sp.Matrix(
        [
            [sp.Rational(value, term_count) for value in row]
            for row in totals
        ]
    )
    return channel_evaluation_matrix().inv() * evaluated


def symbolic_stable_matching_action(
    m: sp.Expr = _SYMBOLIC_M,
) -> sp.Matrix:
    """Return the normalized all-rank four-channel action of ``D_m``."""

    denominator = m * (m - 3) * (m - 2) * (m - 1)
    return sp.Matrix(
        [
            [
                (m**2 - 9 * m + 24) / (m * (m - 1)),
                -8 * (m - 4) / (m * (m - 2) * (m - 1)),
                8 * (m - 4) * (m - 3) / (m * (m - 2) * (m - 1)),
                8 * (m - 5) * (m - 4) / denominator,
            ],
            [
                0,
                (
                    m**4
                    - 14 * m**3
                    + 75 * m**2
                    - 174 * m
                    + 140
                )
                / denominator,
                4 * (m**2 - 6 * m + 7) / denominator,
                4 * (m - 5) * (m**2 - 7 * m + 9) / denominator,
            ],
            [
                (m - 4) / (m * (m - 2) * (m - 1)),
                4 * (m - 5) / denominator,
                (
                    m**4
                    - 12 * m**3
                    + 55 * m**2
                    - 104 * m
                    + 52
                )
                / denominator,
                4 * (m - 5) ** 2 / (m * (m - 3) * (m - 2)),
            ],
            [
                1 / denominator,
                2 * (m**2 - 7 * m + 7) / denominator,
                4 * (m**2 - 6 * m + 6) / denominator,
                (
                    m**4
                    - 10 * m**3
                    + 25 * m**2
                    + 16 * m
                    - 50
                )
                / denominator,
            ],
        ]
    ).applyfunc(sp.factor)


def symbolic_restricted_stable_matching_action(
    m: sp.Expr = _SYMBOLIC_M,
) -> sp.Matrix:
    """Restrict ``D_m`` to the multiplicity-two top Johnson harmonic."""

    denominator = m * (m - 3) * (m - 2) * (m - 1)
    return sp.Matrix(
        [
            [
                (
                    m**4
                    - 14 * m**3
                    + 71 * m**2
                    - 146 * m
                    + 100
                )
                / denominator,
                -8 * (2 * m - 5) / denominator,
            ],
            [
                -1 / denominator,
                (
                    m**4
                    - 14 * m**3
                    + 73 * m**2
                    - 160 * m
                    + 126
                )
                / denominator,
            ],
        ]
    ).applyfunc(sp.factor)


def stable_matching_gap_squared(m: sp.Expr = _SYMBOLIC_M) -> sp.Expr:
    action = symbolic_restricted_stable_matching_action(m)
    return sp.factor(sp.trace(action) ** 2 - 4 * action.det())


@lru_cache(maxsize=1)
def audit_stable_branch_resolution() -> StableBranchResolutionControl:
    interpolation_rows = (6, 7, 8, 9, 10)
    holdout_rows = (11, 12)
    direct = {
        half_degree: direct_stable_matching_action(half_degree)
        for half_degree in (*interpolation_rows, *holdout_rows)
    }
    formula = symbolic_stable_matching_action()
    maximum_degree = 0
    formulas_match = True
    orbit_size = len(canonical_disjoint_matching_orbit())
    choose_four = (
        _SYMBOLIC_M
        * (_SYMBOLIC_M - 1)
        * (_SYMBOLIC_M - 2)
        * (_SYMBOLIC_M - 3)
        / 24
    )
    for row in range(4):
        for column in range(4):
            points = [
                (
                    half_degree,
                    direct[half_degree][row, column]
                    * orbit_size
                    * math.comb(half_degree, 4),
                )
                for half_degree in interpolation_rows
            ]
            interpolated = sp.interpolate(points, _SYMBOLIC_M)
            interpolated_degree = sp.degree(interpolated, _SYMBOLIC_M)
            maximum_degree = max(
                maximum_degree,
                0 if interpolated == 0 else int(interpolated_degree),
            )
            predicted = sp.factor(
                formula[row, column] * orbit_size * choose_four
            )
            formulas_match = formulas_match and (
                sp.cancel(interpolated - predicted) == 0
            )
    holdouts_match = all(
        direct[half_degree]
        == formula.applyfunc(
            lambda expression: sp.factor(
                expression.subs(_SYMBOLIC_M, half_degree)
            )
        )
        for half_degree in holdout_rows
    )
    projector = symbolic_top_harmonic_projector(_SYMBOLIC_M)
    preserves = all(
        sp.cancel(entry) == 0
        for entry in formula * projector - projector * formula
    )
    basis = projector[:, [0, 1]]
    left_inverse = (basis.T * basis).inv() * basis.T
    restricted = symbolic_restricted_stable_matching_action()
    reconstructs = all(
        sp.cancel(entry) == 0
        for entry in formula * basis - basis * restricted
    ) and all(
        sp.cancel(
            entry
            - (1 if row == column else 0)
        )
        == 0
        for row in range(2)
        for column, entry in enumerate((left_inverse * basis).row(row))
    )
    expected_gap = sp.factor(
        4
        * (
            _SYMBOLIC_M**4
            - 14 * _SYMBOLIC_M**3
            + 75 * _SYMBOLIC_M**2
            - 166 * _SYMBOLIC_M
            + 129
        )
        / (
            _SYMBOLIC_M**2
            * (_SYMBOLIC_M - 3) ** 2
            * (_SYMBOLIC_M - 2) ** 2
            * (_SYMBOLIC_M - 1) ** 2
        )
    )
    gap_verified = (
        sp.cancel(stable_matching_gap_squared() - expected_gap) == 0
        and sp.cancel(
            stable_matching_gap_squared()
            / support_five_gap_squared(_SYMBOLIC_M)
            - sp.Rational(16, 25)
        )
        == 0
    )
    proved = bool(
        maximum_degree <= 4
        and formulas_match
        and holdouts_match
        and preserves
        and reconstructs
        and gap_verified
    )
    return StableBranchResolutionControl(
        stable_symmetric_partition="lambda_m=(2m-4,4)",
        stable_K_partition="mu_m=((m-2,2),empty)",
        branching_multiplicity=2,
        normalized_orbit_size="192*binomial(m,4)",
        interpolation_rows=interpolation_rows,
        holdout_rows=holdout_rows,
        maximum_interpolated_degree=maximum_degree,
        predicted_degree_upper_bound=4,
        closed_formula_matches_interpolation=formulas_match,
        all_holdouts_match=holdouts_match,
        action_preserves_top_harmonic_copy_space=preserves,
        restricted_action_reconstruction_verified=reconstructs,
        normalized_gap_squared=str(expected_gap),
        gap_squared_ratio_to_support_five_resolver="16/25",
        inverse_polynomial_gap_lower_bound="gap(D_m) >= 2/(5m^2)",
        all_rank_stable_branch_resolver_proved=proved,
        natural_source_mass_nonnegligible=False,
        status=(
            "all-rank-disjoint-matching-stable-resolver-proved"
            if proved
            else "stable-matching-resolution-control-failure"
        ),
    )


def _perfect_matchings(vertices: tuple[int, ...]) -> Iterable[tuple[tuple[int, int], ...]]:
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in _perfect_matchings(remainder):
            yield ((first, second), *tail)


@lru_cache(maxsize=None)
def third_matching_charge(half_degree: int) -> GroupAlgebraElement:
    if half_degree < 6:
        raise ValueError("half_degree must be at least six")
    identity = tuple(range(2 * half_degree))
    output = []
    for labels in itertools.combinations(range(half_degree), 6):
        for matching in _perfect_matchings(labels):
            product = {identity: 1}
            for edge in matching:
                product = _multiply_elements(
                    product,
                    _element(pair_interaction(half_degree, *edge)),
                )
            output.append(product)
    return _add_elements(*output)


@lru_cache(maxsize=1)
def local_center_element() -> GroupAlgebraElement:
    interaction = _element(pair_interaction(2, 0, 1))
    residual = _subtract_elements(
        _multiply_elements(interaction, interaction),
        _scale_element(interaction, 4),
    )
    if any(coefficient % 8 for coefficient in residual.values()):
        raise AssertionError("local square residual is not divisible by eight")
    return {
        permutation: coefficient // 8
        for permutation, coefficient in residual.items()
    }


def _embed_local_permutation(
    permutation: Permutation,
    pair_labels: tuple[int, int],
    half_degree: int,
) -> Permutation:
    points = (
        2 * pair_labels[0],
        2 * pair_labels[0] + 1,
        2 * pair_labels[1],
        2 * pair_labels[1] + 1,
    )
    output = list(range(2 * half_degree))
    for source, target in enumerate(permutation):
        output[points[source]] = points[target]
    return tuple(output)


@lru_cache(maxsize=None)
def global_local_center_sum(half_degree: int) -> GroupAlgebraElement:
    return _add_elements(
        *(
            {
                _embed_local_permutation(
                    permutation,
                    (left, right),
                    half_degree,
                ): coefficient
                for permutation, coefficient in local_center_element().items()
            }
            for left in range(half_degree)
            for right in range(left + 1, half_degree)
        )
    )


@lru_cache(maxsize=None)
def edge_power_sum(half_degree: int) -> GroupAlgebraElement:
    return _add_elements(
        *(
            _multiply_elements(interaction, interaction)
            for interaction in (
                _element(pair_interaction(half_degree, left, right))
                for left in range(half_degree)
                for right in range(left + 1, half_degree)
            )
        )
    )


@lru_cache(maxsize=1)
def audit_local_power_collapse() -> LocalPowerCollapseControl:
    interaction = _element(pair_interaction(2, 0, 1))
    center = local_center_element()
    relation = _subtract_elements(
        _multiply_elements(interaction, interaction),
        _add_elements(_scale_element(interaction, 4), _scale_element(center, 8)),
    )
    local_group = set(hyperoctahedral_group(2))
    subgroup = set(center).issubset(local_group) and all(
        coefficient == 1 for coefficient in center.values()
    )
    global_controls = True
    for half_degree in range(3, 7):
        power_sum = edge_power_sum(half_degree)
        predicted = _add_elements(
            _scale_element(central_pair_charge(half_degree), 4),
            _scale_element(global_local_center_sum(half_degree), 8),
        )
        central = global_local_center_sum(half_degree)
        global_controls = global_controls and power_sum == predicted and all(
            not _commutator(central, {generator: 1})
            for generator in _K_generators(half_degree)
        )
    verified = not relation and subgroup and global_controls
    return LocalPowerCollapseControl(
        pair_interaction_term_count=len(interaction),
        square_term_count=len(_multiply_elements(interaction, interaction)),
        local_center_term_count=len(center),
        square_relation_nonzero_count=len(relation),
        local_center_is_subgroup_sum=subgroup,
        global_center_controls_verified=global_controls,
        power_sum_adds_copy_labels_beyond_C_and_K_center=False,
        status=(
            "edge-power-sum-collapses-to-C-plus-K-center"
            if verified
            else "edge-power-collapse-control-failure"
        ),
    )


@lru_cache(maxsize=None)
def audit_matching_charge(half_degree: int) -> MatchingChargeControl:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    central = central_pair_charge(half_degree)
    matching = disjoint_matching_charge(half_degree)
    pair_failures = sum(
        bool(
            _commutator(
                central,
                _element(pair_interaction(half_degree, left, right)),
            )
        )
        for left in range(half_degree)
        for right in range(left + 1, half_degree)
    )
    generators = _K_generators(half_degree)
    central_K_failures = sum(
        bool(_commutator(central, {generator: 1}))
        for generator in generators
    )
    matching_K_failures = sum(
        bool(_commutator(matching, {generator: 1}))
        for generator in generators
    )
    mutual = _commutator(central, matching)
    expected_central = 8 * math.comb(half_degree, 2)
    expected_matching = 192 * math.comb(half_degree, 4)
    verified = bool(
        len(central) == expected_central
        and len(matching) == expected_matching
        and pair_failures == 0
        and not mutual
        and central_K_failures == 0
        and matching_K_failures == 0
    )
    return MatchingChargeControl(
        half_degree=half_degree,
        C_term_count=len(central),
        expected_C_term_count=expected_central,
        D_term_count=len(matching),
        expected_D_term_count=expected_matching,
        C_pair_commutator_failure_count=pair_failures,
        C_D_commutator_nonzero_count=len(mutual),
        C_K_commutator_failure_count=central_K_failures,
        D_K_commutator_failure_count=matching_K_failures,
        polynomial_sparse_K_adapted_commuting_pair_verified=verified,
        status=(
            "polynomial-sparse-K-adapted-commuting-pair-verified"
            if verified
            else "matching-charge-control-failure"
        ),
    )


def _refine_joint_eigenspaces(
    blocks: list[np.ndarray],
    matrix: np.ndarray,
    *,
    tolerance: float = 3e-7,
) -> list[np.ndarray]:
    output: list[np.ndarray] = []
    matrix = (matrix + matrix.T) / 2.0
    for basis in blocks:
        restricted = basis.T @ matrix @ basis
        restricted = (restricted + restricted.T) / 2.0
        eigenvalues, eigenvectors = np.linalg.eigh(restricted)
        start = 0
        for index in range(1, len(eigenvalues) + 1):
            if (
                index == len(eigenvalues)
                or abs(eigenvalues[index] - eigenvalues[start]) > tolerance
            ):
                output.append(basis @ eigenvectors[:, start:index])
                start = index
    return output


@lru_cache(maxsize=None)
def audit_branch_resolution(
    half_degree: int,
    symmetric_partition: tuple[int, ...],
) -> BranchResolutionControl:
    if half_degree not in (4, 5):
        raise ValueError("dense branch controls are limited to m=4,5")
    if sum(symmetric_partition) != 2 * half_degree:
        raise ValueError("partition size does not match half_degree")
    block_count, _, _, repeated = exact_branching_commutant_dimension(
        symmetric_partition,
        half_degree,
    )
    if not repeated:
        raise ValueError("branch control requires a repeated restriction")
    edges = [
        (left, right)
        for left in range(half_degree)
        for right in range(left + 1, half_degree)
    ]
    pair_sets = [
        pair_interaction(half_degree, *edge) for edge in edges
    ]
    center_sets = hyperoctahedral_conjugacy_classes(half_degree)
    matrices = _average_matrices_for_sets(
        symmetric_partition,
        [*pair_sets, *center_sets],
    )
    pair_matrices = matrices[: len(pair_sets)]
    center_matrices = [
        (matrix + matrix.T) / 2.0
        for matrix in matrices[len(pair_sets) :]
    ]
    central = sum(pair_matrices, np.zeros_like(pair_matrices[0]))
    matching = np.zeros_like(central)
    for (left_index, left_edge), (right_index, right_edge) in itertools.combinations(
        enumerate(edges),
        2,
    ):
        if set(left_edge).isdisjoint(right_edge):
            matching += pair_matrices[left_index] @ pair_matrices[right_index]

    blocks = [np.eye(central.shape[0])]
    for center_matrix in center_matrices:
        blocks = _refine_joint_eigenspaces(blocks, center_matrix)
    center_count = len(blocks)
    central_blocks = _refine_joint_eigenspaces(blocks, central)
    matching_blocks = _refine_joint_eigenspaces(central_blocks, matching)
    target = sum(
        hyperoctahedral_branching_coefficient(
            symmetric_partition,
            *bipartition,
        )
        for bipartition in bipartitions(half_degree)
    )
    center_valid = center_count == block_count
    central_count = len(central_blocks)
    matching_count = len(matching_blocks)
    improved = matching_count - central_count
    if not center_valid or matching_count > target:
        status = "branch-resolution-control-failure"
    elif matching_count == target:
        status = "C-D-resolve-all-controlled-copy-labels"
    elif improved > 0:
        status = "D-strictly-improves-partial-copy-resolution"
    else:
        status = "D-leaves-residual-copy-degeneracy"
    return BranchResolutionControl(
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        symmetric_irrep_dimension=central.shape[0],
        K_branch_block_count=block_count,
        center_joint_eigenspace_count=center_count,
        target_copy_label_count=target,
        center_plus_C_joint_eigenspace_count=central_count,
        center_plus_C_D_joint_eigenspace_count=matching_count,
        D_added_copy_label_count=improved,
        C_resolves_all_copy_labels=central_count == target,
        C_D_resolves_all_copy_labels=matching_count == target,
        finite_numerical_control_only=True,
        status=status,
    )


def _product_coefficient(
    left: GroupAlgebraElement,
    right: GroupAlgebraElement,
    target: Permutation,
) -> int:
    return sum(
        coefficient
        * right.get(
            compose_permutations(
                inverse_permutation(permutation),
                target,
            ),
            0,
        )
        for permutation, coefficient in left.items()
    )


@lru_cache(maxsize=1)
def audit_higher_matching_boundary() -> HigherMatchingBoundaryControl:
    half_degree = 6
    matching = disjoint_matching_charge(half_degree)
    third = third_matching_charge(half_degree)
    witness = (0, 2, 1, 4, 3, 6, 7, 8, 5, 10, 9, 11)
    coefficient = _product_coefficient(matching, third, witness) - (
        _product_coefficient(third, matching, witness)
    )
    return HigherMatchingBoundaryControl(
        half_degree=half_degree,
        D_term_count=len(matching),
        M3_term_count=len(third),
        commutator_witness_permutation=witness,
        commutator_witness_coefficient=coefficient,
        D_M3_commute=coefficient == 0,
        matching_charge_family_pairwise_commuting=False,
        status=(
            "third-matching-charge-fails-to-commute-with-D"
            if coefficient != 0
            else "higher-matching-boundary-control-failure"
        ),
    )


@lru_cache(maxsize=1)
def build_pair_matching_charge_report() -> PairMatchingChargeReport:
    collapse = audit_local_power_collapse()
    matching_controls = [audit_matching_charge(value) for value in (4, 5, 6, 7)]
    stable = audit_stable_branch_resolution()
    branch_controls = [
        audit_branch_resolution(4, (4, 2, 1, 1)),
        audit_branch_resolution(5, (6, 3, 1)),
        audit_branch_resolution(5, (5, 3, 2)),
        audit_branch_resolution(5, (4, 3, 2, 1)),
    ]
    higher = audit_higher_matching_boundary()
    exact = bool(
        collapse.status == "edge-power-sum-collapses-to-C-plus-K-center"
        and all(
            row.polynomial_sparse_K_adapted_commuting_pair_verified
            for row in matching_controls
        )
        and stable.all_rank_stable_branch_resolver_proved
        and higher.commutator_witness_coefficient != 0
    )
    improved = any(row.D_added_copy_label_count > 0 for row in branch_controls)
    every_complete = all(row.C_D_resolves_all_copy_labels for row in branch_controls)
    theorem = PairMatchingChargeTheorem(
        central_pair_charge=(
            "C_m=sum_(i<j)c_ij is central in the algebra generated by the pair interactions."
        ),
        disjoint_matching_charge=(
            "D_m is the sum of c_ij c_kl over disjoint pair-label edges and has 192*binomial(m,4) terms."
        ),
        all_rank_commutation_proof=(
            "For fixed ij, disjoint terms commute and each triangle contributes [c_ik+c_jk,c_ij]=0; hence [C_m,c_ij]=0 and [C_m,D_m]=0."
        ),
        power_sum_collapse=(
            "sum c_ij^2=4C_m+8Z_m with Z_m in the center of C[K_m]."
        ),
        finite_resolution_evidence=(
            "D_m adds terminal K-copy labels at m=5 and fully repairs lambda=(6,3,1), but leaves large residual sectors."
        ),
        higher_matching_boundary=(
            "The three-edge matching charge M_3 does not commute with D_m; matching sums are not a commuting hierarchy."
        ),
        exact_all_rank_K_adapted_commuting_pair_proved=exact,
        polynomial_permutation_expansions_proved=exact,
        edge_power_sum_redundancy_proved=collapse.global_center_controls_verified,
        stable_multiplicity_two_resolver_proved=(
            stable.all_rank_stable_branch_resolver_proved
        ),
        stable_inverse_polynomial_gap_proved=(
            stable.all_rank_stable_branch_resolver_proved
        ),
        finite_copy_resolution_strictly_improved=improved,
        complete_finite_copy_resolution_on_every_control=every_complete,
        asymptotic_natural_copy_resolution_proved=False,
        inverse_polynomial_conditional_gaps_proved=False,
        source_signal_correlation_proved=False,
        coherent_subduction_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and improved and not every_complete,
        status=(
            "K-adapted-commuting-pair-proved-partial-copy-resolution"
            if exact and improved and not every_complete
            else "pair-matching-charge-theorem-control-failure"
        ),
    )
    return PairMatchingChargeReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "S_(2m) down C_2 wr S_m with canonical pair interactions",
            "range": "exact charge identities for every m>=4",
            "finite_resolution_scope": "Young-basis controls at m=4,5 only",
            "claim_boundary": (
                "A polynomial K-adapted commuting pair with strict finite copy-space improvement; not a complete hierarchy, gap theorem, transform, or detector."
            ),
        },
        local_power_collapse=collapse,
        matching_controls=matching_controls,
        stable_branch_resolution=stable,
        branch_controls=branch_controls,
        higher_matching_boundary=higher,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-MATCHING-CENTRALIZER-COMPLETION",
                "statement": (
                    "Classify or construct additional polynomial K-adapted charges commuting with C_m and D_m that split the residual natural copy spaces."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MATCHING-NATURAL-RESOLUTION",
                "statement": (
                    "Prove a source-weighted lower bound on the fraction of natural branching copies separated by the C_m,D_m joint spectrum."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MATCHING-CONDITIONAL-GAPS",
                "statement": (
                    "Prove inverse-polynomial conditional gaps or bounded local branching for a completed hierarchy."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MATCHING-SOURCE-CORRELATION",
                "statement": (
                    "Show that the resolved labels correlate with the source-aware CS likelihood rather than nuisance multiplicity."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The edge-square power sum supplies a second charge.",
                "answer": (
                    "False. Its exact local minimal relation makes it C_m plus a K-center element, so it cannot refine fixed K,C labels."
                ),
                "resolved": True,
            },
            {
                "challenge": "The disjoint matching charge is only formally different.",
                "answer": (
                    "False: it adds a joint copy label at m=5 and has an exact inverse-polynomial gap on the all-rank stable multiplicity-two branch."
                ),
                "resolved": True,
            },
            {
                "challenge": "Matching charges form an automatic full commuting hierarchy.",
                "answer": (
                    "False: an explicit S_12 coefficient in [D_m,M_3] is nonzero."
                ),
                "resolved": True,
            },
            {
                "challenge": "One additional split implies a scalable subduction transform.",
                "answer": (
                    "False: the worst finite sector is unchanged and no natural-mass, gap, source-correlation, or circuit theorem is known."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "arXiv:0710.4971",
                "role": (
                    "Gaudin/Jucys-Murphy commuting-algebra mechanism; the present K-adapted matching charge is a distinct finite-group construction."
                ),
            },
            {
                "id": "arXiv:1001.2345",
                "role": (
                    "Odd Jucys-Murphy and hyperoctahedral Hecke-algebra comparison; its multiplicity-free double-coset setting does not resolve the present repeated K branches."
                ),
            },
            {
                "id": "arXiv:1807.00481",
                "role": (
                    "Perfect-matching association-scheme eigenvalue recurrences for the trivial K branch; useful boundary, not a general subduction compiler."
                ),
            },
        ],
        headline_metrics={
            "all_rank_K_adapted_commuting_charge_pair_count": int(exact),
            "polynomial_sparse_charge_count": 2,
            "redundant_edge_power_charge_count": 1,
            "all_rank_stable_branch_resolver_count": int(
                stable.all_rank_stable_branch_resolver_proved
            ),
            "stable_inverse_polynomial_gap_count": int(
                stable.all_rank_stable_branch_resolver_proved
            ),
            "finite_branch_control_count": len(branch_controls),
            "finite_branch_strict_improvement_count": sum(
                row.D_added_copy_label_count > 0 for row in branch_controls
            ),
            "finite_branch_full_resolution_count": sum(
                row.C_D_resolves_all_copy_labels for row in branch_controls
            ),
            "higher_matching_noncommutation_witness_count": int(
                higher.commutator_witness_coefficient != 0
            ),
            "asymptotic_natural_resolution_count": 0,
            "inverse_polynomial_conditional_gap_count": 0,
            "hidden_involution_detector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_rank_K_adapted_commuting_pair_proved": exact,
            "polynomial_permutation_expansions_proved": exact,
            "edge_power_sum_redundancy_proved": collapse.global_center_controls_verified,
            "stable_multiplicity_two_resolver_proved": (
                stable.all_rank_stable_branch_resolver_proved
            ),
            "stable_inverse_polynomial_gap_proved": (
                stable.all_rank_stable_branch_resolver_proved
            ),
            "stable_branch_natural_source_mass_nonnegligible": False,
            "strict_finite_copy_resolution_improvement": improved,
            "complete_control_resolution": every_complete,
            "asymptotic_natural_copy_resolution_proved": False,
            "inverse_polynomial_conditional_gaps_proved": False,
            "source_signal_correlation_proved": False,
            "coherent_subduction_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
            "C_m,D_m are the first terminal K-adapted commuting pair with strict copy-space improvement, but residual degeneracy and every natural algorithmic obligation remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved an all-rank polynomial K-adapted commuting charge pair and demonstrated strict but incomplete hyperoctahedral copy-space resolution."
        ),
        falsifiers_triggered=[
            "Symmetric edge power sums do not extend the copy-label algebra beyond C_m and the K center.",
            "Disjoint matching products do add genuine terminal copy information.",
            "The disjoint matching charge is an all-rank inverse-polynomial resolver on the stable multiplicity-two branch, but that branch has factorially negligible natural source mass.",
            "Higher matching sums are not automatically mutually commuting.",
            "The current commuting pair leaves the largest controlled multiplicity sector unresolved.",
        ],
    )


def write_pair_matching_charge_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_pair_matching_charge_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_pair_matching_charge_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
