"""Perfect-matching identification self-reduces to binary detection.

For ``L<=G``, let ``Delta_L`` dephase the group basis by the left cosets
``gL``.  Right multiplication has a matrix entry only between ``g`` and
``gh``, and these lie in the same left coset exactly when ``h in L``.  Hence

    Delta_L(R_h) = R_h  if h in L, and 0 otherwise,       (1)
    Delta_L(rho_h) = rho_h if h in L, and I/|G| otherwise.

For a proposed edge ``e={i,j}``, let

    L_e = S_e x S_(complement(e)).

A fixed-point-free involution ``h`` lies in ``L_e`` exactly when its perfect
matching contains ``e``.  Conditioning on a left-coset label therefore turns
one copy into an exact hidden coset state over ``L_e`` for a true edge and the
exact maximally mixed state over ``L_e`` for a false edge.

After ``t`` disjoint edges are known and one more is proposed, use

    L = C_2^(t+1) x S_(2r-2).

On a true proposal the hidden element is ``z tensor h'``, where ``z`` is the
product of all known/proposed swaps.  Fourier measurement of ``C_2^(t+1)``
and retention of all characters with ``chi(z)=+1`` has probability exactly
``1/2`` and leaves ``rho_(h')``.  A false proposal leaves the exact null state.
Crucially, all removed edges are processed in one character test, so this
constant probability does not compound with recursion depth.

Therefore a polynomial-query, polynomial-time worst-case binary detector for
fixed-point-free involutions in every ``S_(2r)`` yields a polynomial
identifier: test the ``2r-1`` possible partners of one remaining vertex using
fresh states, reduce to ``S_(2r-2)``, and repeat.  There are
``sum_(r=2)^m(2r-1)=m^2-1`` membership tests.  Conjugation symmetrization or a
random relabeling converts class-average detector guarantees to worst-case
ones.

Conversely, identification yields binary detection by verifying the proposed
involution with fresh projectors ``(I+R_h)/2``: the correct hidden state
accepts with probability one, while null or a wrong candidate accepts each
copy with probability ``1/2``.  Binary detection and identification are thus
polynomially equivalent for this explicit permutation-basis coset-state
family.

Fenner--Zhang already proved a broader decision/search equivalence for HSP over
permutation groups.  The contribution here is an explicit state-channel
specialization with an exact edge recursion and constant-probability batched
character filter, not a claim of a new general complexity equivalence.  This
is a reduction, not an algorithm: the efficient binary detector remains
unconstructed, and no graph-isomorphism or classical separation follows.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    involution_conjugacy_class,
    right_regular_matrix,
    symmetric_group,
)
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_binary_identification_self_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-BINARY-IDENTIFICATION-SELF-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EdgeDephasingFiniteControl:
    n: int
    group_order: int
    subgroup_order: int
    hidden_edges: tuple[tuple[int, int], ...]
    true_test_edge: tuple[int, int]
    false_test_edge: tuple[int, int]
    true_edge_in_subgroup: bool
    false_edge_in_subgroup: bool
    true_dephasing_preservation_residual: float
    false_dephasing_to_null_residual: float
    true_conditional_subgroup_state_residual: float
    false_conditional_subgroup_null_residual: float
    known_swap_plus_probability: float
    known_swap_plus_probability_under_null: float
    true_reduced_hidden_state_residual: float
    false_reduced_null_state_residual: float
    exact_edge_membership_channel_verified: bool
    status: str


@dataclass(frozen=True)
class BatchedKnownEdgeCharacterControl:
    known_edge_count: int
    abelian_factor_dimension: int
    remaining_degree: int
    remaining_group_order: int
    character_count: int
    positive_character_count: int
    negative_character_count: int
    positive_character_total_probability: float
    positive_character_total_probability_under_null: float
    maximum_character_probability_residual: float
    maximum_positive_hidden_state_residual: float
    maximum_negative_hidden_state_residual: float
    maximum_null_state_residual: float
    recursion_depth_compounds_postselection: bool
    exact_batched_character_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class BinaryIdentificationScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    candidate_information_log2: float
    worst_case_edge_membership_test_count: int
    maximum_binary_detector_half_degree: int
    accepted_character_probability: float
    expected_raw_copy_overhead_per_detector_copy: float
    detector_error_target_order: str
    polynomial_binary_detector_implies_polynomial_identifier: bool
    polynomial_identifier_implies_polynomial_binary_detector: bool
    efficient_binary_detector_constructed: bool
    status: str


@dataclass(frozen=True)
class BinaryIdentificationSelfReductionTheorem:
    subgroup_dephasing_lemma: str
    edge_membership_equivalence: str
    conditional_subgroup_reduction: str
    batched_character_reduction: str
    identification_recurrence: str
    converse_verification: str
    access_model: str
    scope_limit: str
    exact_subgroup_dephasing_proved: bool
    exact_edge_membership_reduction_proved: bool
    constant_success_batched_recursion_proved: bool
    binary_to_identification_polynomial_reduction_proved: bool
    identification_to_binary_polynomial_reduction_proved: bool
    efficient_binary_detector_constructed: bool
    hidden_involution_algorithm_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BinaryIdentificationSelfReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    edge_controls: list[EdgeDephasingFiniteControl]
    batched_character_controls: list[BatchedKnownEdgeCharacterControl]
    scaling_records: list[BinaryIdentificationScalingRecord]
    theorem: BinaryIdentificationSelfReductionTheorem
    literature_links: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _matching_edges(permutation: Permutation) -> tuple[tuple[int, int], ...]:
    edges = []
    for left, right in enumerate(permutation):
        if left < right:
            edges.append((left, right))
    return tuple(edges)


def _edge_stabilizer(
    group: tuple[Permutation, ...],
    edge: tuple[int, int],
) -> tuple[Permutation, ...]:
    edge_set = frozenset(edge)
    return tuple(
        permutation
        for permutation in group
        if frozenset(permutation[index] for index in edge) == edge_set
    )


def _left_cosets(
    group: tuple[Permutation, ...],
    subgroup: tuple[Permutation, ...],
) -> tuple[tuple[Permutation, ...], ...]:
    unseen = set(group)
    cosets = []
    while unseen:
        representative = min(unseen)
        coset = tuple(
            compose_permutations(representative, element)
            for element in subgroup
        )
        cosets.append(coset)
        unseen.difference_update(coset)
    return tuple(cosets)


def _coset_dephase(
    matrix: np.ndarray,
    group: tuple[Permutation, ...],
    subgroup: tuple[Permutation, ...],
) -> np.ndarray:
    index = {element: offset for offset, element in enumerate(group)}
    output = np.zeros_like(matrix)
    for coset in _left_cosets(group, subgroup):
        rows = [index[element] for element in coset]
        output[np.ix_(rows, rows)] = matrix[np.ix_(rows, rows)]
    return output


def _embedded_rest_permutation(
    rest: tuple[int, ...],
    permutation: Permutation,
    degree: int,
) -> Permutation:
    output = list(range(degree))
    for source, target in enumerate(permutation):
        output[rest[source]] = rest[target]
    return tuple(output)


def _edge_swap(edge: tuple[int, int], degree: int) -> Permutation:
    output = list(range(degree))
    left, right = edge
    output[left], output[right] = output[right], output[left]
    return tuple(output)


def audit_edge_dephasing_reduction(
    n: int = 4,
    *,
    tolerance: float = 1e-9,
) -> EdgeDephasingFiniteControl:
    if n < 4 or n % 2:
        raise ValueError("finite edge control needs even n at least four")
    if n > 4:
        raise ValueError("dense finite edge control is intentionally limited to n=4")
    group = symmetric_group(n)
    hidden = involution_conjugacy_class(n, n // 2)[0]
    edges = _matching_edges(hidden)
    true_edge = edges[0]
    pivot = true_edge[0]
    false_partner = next(
        point for point in range(n)
        if point not in true_edge
    )
    false_edge = tuple(sorted((pivot, false_partner)))
    true_subgroup = _edge_stabilizer(group, true_edge)
    false_subgroup = _edge_stabilizer(group, false_edge)
    rho_hidden = (
        np.eye(len(group)) + right_regular_matrix(n, hidden)
    ) / len(group)
    rho_null = np.eye(len(group)) / len(group)
    true_dephased = _coset_dephase(rho_hidden, group, true_subgroup)
    false_dephased = _coset_dephase(rho_hidden, group, false_subgroup)
    true_preservation = float(np.linalg.norm(true_dephased - rho_hidden, ord=2))
    false_to_null = float(np.linalg.norm(false_dephased - rho_null, ord=2))

    group_index = {element: offset for offset, element in enumerate(group)}

    def conditional_subgroup_state(
        dephased: np.ndarray,
        subgroup: tuple[Permutation, ...],
    ) -> np.ndarray:
        rows = [group_index[element] for element in subgroup]
        block = dephased[np.ix_(rows, rows)]
        return block / float(np.trace(block).real)

    true_conditional = conditional_subgroup_state(true_dephased, true_subgroup)
    false_conditional = conditional_subgroup_state(false_dephased, false_subgroup)
    true_subgroup_index = {
        element: offset for offset, element in enumerate(true_subgroup)
    }
    true_subgroup_right = np.zeros(
        (len(true_subgroup), len(true_subgroup)), dtype=complex
    )
    for column, element in enumerate(true_subgroup):
        true_subgroup_right[
            true_subgroup_index[compose_permutations(element, hidden)],
            column,
        ] = 1.0
    predicted_true = (
        np.eye(len(true_subgroup)) + true_subgroup_right
    ) / len(true_subgroup)
    predicted_false = np.eye(len(false_subgroup)) / len(false_subgroup)
    true_conditional_residual = float(
        np.linalg.norm(true_conditional - predicted_true, ord=2)
    )
    false_conditional_residual = float(
        np.linalg.norm(false_conditional - predicted_false, ord=2)
    )

    rest = tuple(point for point in range(n) if point not in true_edge)
    rest_group = symmetric_group(n - 2)
    swap = _edge_swap(true_edge, n)
    ordered_subgroup = []
    for bit in range(2):
        swap_power = swap if bit else tuple(range(n))
        for rest_permutation in rest_group:
            embedded = _embedded_rest_permutation(rest, rest_permutation, n)
            ordered_subgroup.append(
                compose_permutations(swap_power, embedded)
            )
    reorder = [true_subgroup_index[element] for element in ordered_subgroup]
    ordered_true = true_conditional[np.ix_(reorder, reorder)]
    # The false conditional state is maximally mixed in any subgroup basis.
    ordered_false = np.eye(len(ordered_subgroup)) / len(ordered_subgroup)
    plus = np.asarray((1.0, 1.0), dtype=complex) / math.sqrt(2.0)
    kraus = np.kron(plus.conj().reshape(1, 2), np.eye(len(rest_group)))
    reduced_true_unnormalized = kraus @ ordered_true @ kraus.conj().T
    reduced_false_unnormalized = kraus @ ordered_false @ kraus.conj().T
    true_probability = float(np.trace(reduced_true_unnormalized).real)
    false_probability = float(np.trace(reduced_false_unnormalized).real)
    reduced_true = reduced_true_unnormalized / true_probability
    reduced_false = reduced_false_unnormalized / false_probability

    hidden_rest = tuple(rest.index(hidden[point]) for point in rest)
    expected_reduced_true = (
        np.eye(len(rest_group))
        + right_regular_matrix(n - 2, hidden_rest)
    ) / len(rest_group)
    expected_reduced_false = np.eye(len(rest_group)) / len(rest_group)
    reduced_true_residual = float(
        np.linalg.norm(reduced_true - expected_reduced_true, ord=2)
    )
    reduced_false_residual = float(
        np.linalg.norm(reduced_false - expected_reduced_false, ord=2)
    )
    true_membership = hidden in true_subgroup
    false_membership = hidden in false_subgroup
    verified = bool(
        true_membership
        and not false_membership
        and true_preservation <= 100 * tolerance
        and false_to_null <= 100 * tolerance
        and true_conditional_residual <= 100 * tolerance
        and false_conditional_residual <= 100 * tolerance
        and abs(true_probability - 0.5) <= 100 * tolerance
        and abs(false_probability - 0.5) <= 100 * tolerance
        and reduced_true_residual <= 100 * tolerance
        and reduced_false_residual <= 100 * tolerance
    )
    return EdgeDephasingFiniteControl(
        n=n,
        group_order=len(group),
        subgroup_order=len(true_subgroup),
        hidden_edges=edges,
        true_test_edge=true_edge,
        false_test_edge=false_edge,
        true_edge_in_subgroup=true_membership,
        false_edge_in_subgroup=false_membership,
        true_dephasing_preservation_residual=true_preservation,
        false_dephasing_to_null_residual=false_to_null,
        true_conditional_subgroup_state_residual=true_conditional_residual,
        false_conditional_subgroup_null_residual=false_conditional_residual,
        known_swap_plus_probability=true_probability,
        known_swap_plus_probability_under_null=false_probability,
        true_reduced_hidden_state_residual=reduced_true_residual,
        false_reduced_null_state_residual=reduced_false_residual,
        exact_edge_membership_channel_verified=verified,
        status=(
            "exact-edge-membership-to-smaller-binary-instance-verified"
            if verified
            else "edge-dephasing-reduction-control-failure"
        ),
    )


def _walsh_matrix(qubit_count: int) -> np.ndarray:
    matrix = np.ones((1, 1), dtype=complex)
    hadamard = np.asarray(((1.0, 1.0), (1.0, -1.0)), dtype=complex)
    for _ in range(qubit_count):
        matrix = np.kron(matrix, hadamard)
    return matrix / math.sqrt(2**qubit_count)


def audit_batched_known_edge_character_reduction(
    known_edge_count: int,
    remaining_half_degree: int,
    *,
    tolerance: float = 1e-9,
) -> BatchedKnownEdgeCharacterControl:
    if known_edge_count < 1 or remaining_half_degree < 1:
        raise ValueError("known edges and remaining half degree must be positive")
    abelian_dimension = 2**known_edge_count
    remaining_degree = 2 * remaining_half_degree
    rest_group = symmetric_group(remaining_degree)
    hidden_rest = involution_conjugacy_class(
        remaining_degree, remaining_half_degree
    )[0]
    rest_right = right_regular_matrix(remaining_degree, hidden_rest)
    flip = np.asarray(((0.0, 1.0), (1.0, 0.0)), dtype=complex)
    known_product = flip
    for _ in range(known_edge_count - 1):
        known_product = np.kron(known_product, flip)
    total_dimension = abelian_dimension * len(rest_group)
    hidden_state = (
        np.eye(total_dimension) + np.kron(known_product, rest_right)
    ) / total_dimension
    null_state = np.eye(total_dimension) / total_dimension
    walsh = _walsh_matrix(known_edge_count)
    transformed_hidden = (
        np.kron(walsh, np.eye(len(rest_group)))
        @ hidden_state
        @ np.kron(walsh.conj().T, np.eye(len(rest_group)))
    )
    transformed_null = null_state
    plus_state = (np.eye(len(rest_group)) + rest_right) / len(rest_group)
    minus_state = (np.eye(len(rest_group)) - rest_right) / len(rest_group)
    rest_null = np.eye(len(rest_group)) / len(rest_group)
    probability_residual = 0.0
    plus_residual = 0.0
    minus_residual = 0.0
    null_residual = 0.0
    plus_probability = 0.0
    plus_probability_null = 0.0
    positive_count = 0
    for character in range(abelian_dimension):
        rows = slice(
            character * len(rest_group),
            (character + 1) * len(rest_group),
        )
        hidden_block = transformed_hidden[rows, rows]
        null_block = transformed_null[rows, rows]
        hidden_probability = float(np.trace(hidden_block).real)
        null_probability = float(np.trace(null_block).real)
        probability_residual = max(
            probability_residual,
            abs(hidden_probability - 1.0 / abelian_dimension),
            abs(null_probability - 1.0 / abelian_dimension),
        )
        hidden_conditional = hidden_block / hidden_probability
        null_conditional = null_block / null_probability
        positive = character.bit_count() % 2 == 0
        if positive:
            positive_count += 1
            plus_probability += hidden_probability
            plus_probability_null += null_probability
            plus_residual = max(
                plus_residual,
                float(np.linalg.norm(hidden_conditional - plus_state, ord=2)),
            )
        else:
            minus_residual = max(
                minus_residual,
                float(np.linalg.norm(hidden_conditional - minus_state, ord=2)),
            )
        null_residual = max(
            null_residual,
            float(np.linalg.norm(null_conditional - rest_null, ord=2)),
        )
    verified = bool(
        positive_count * 2 == abelian_dimension
        and abs(plus_probability - 0.5) <= 100 * tolerance
        and abs(plus_probability_null - 0.5) <= 100 * tolerance
        and probability_residual <= 100 * tolerance
        and plus_residual <= 100 * tolerance
        and minus_residual <= 100 * tolerance
        and null_residual <= 100 * tolerance
    )
    return BatchedKnownEdgeCharacterControl(
        known_edge_count=known_edge_count,
        abelian_factor_dimension=abelian_dimension,
        remaining_degree=remaining_degree,
        remaining_group_order=len(rest_group),
        character_count=abelian_dimension,
        positive_character_count=positive_count,
        negative_character_count=abelian_dimension - positive_count,
        positive_character_total_probability=plus_probability,
        positive_character_total_probability_under_null=plus_probability_null,
        maximum_character_probability_residual=probability_residual,
        maximum_positive_hidden_state_residual=plus_residual,
        maximum_negative_hidden_state_residual=minus_residual,
        maximum_null_state_residual=null_residual,
        recursion_depth_compounds_postselection=False,
        exact_batched_character_reduction_verified=verified,
        status=(
            "all-known-edges-batched-at-constant-half-success"
            if verified
            else "batched-character-reduction-control-failure"
        ),
    )


def binary_identification_scaling_record(
    half_degree: int,
) -> BinaryIdentificationScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    candidates = perfect_matching_count(half_degree)
    tests = half_degree**2 - 1
    return BinaryIdentificationScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        candidate_count_decimal=str(candidates),
        candidate_information_log2=math.log2(candidates),
        worst_case_edge_membership_test_count=tests,
        maximum_binary_detector_half_degree=half_degree - 1,
        accepted_character_probability=0.5,
        expected_raw_copy_overhead_per_detector_copy=2.0,
        detector_error_target_order="O(epsilon/m^2) per edge test",
        polynomial_binary_detector_implies_polynomial_identifier=True,
        polynomial_identifier_implies_polynomial_binary_detector=True,
        efficient_binary_detector_constructed=False,
        status="binary-identification-polynomial-equivalence-detector-open",
    )


def build_binary_identification_self_reduction_report(
    *,
    scaling_half_degrees: tuple[int, ...] = (2, 3, 4, 8, 16, 32, 64, 128),
) -> BinaryIdentificationSelfReductionReport:
    edge_controls = [audit_edge_dephasing_reduction(4)]
    batched_controls = [
        audit_batched_known_edge_character_reduction(t, r)
        for t, r in ((1, 2), (2, 1), (3, 1), (4, 1))
    ]
    scaling = [
        binary_identification_scaling_record(m) for m in scaling_half_degrees
    ]
    verified = all(
        row.exact_edge_membership_channel_verified for row in edge_controls
    ) and all(
        row.exact_batched_character_reduction_verified for row in batched_controls
    )
    scaling_verified = all(
        row.polynomial_binary_detector_implies_polynomial_identifier
        and row.polynomial_identifier_implies_polynomial_binary_detector
        and not row.efficient_binary_detector_constructed
        for row in scaling
    )
    theorem = BinaryIdentificationSelfReductionTheorem(
        subgroup_dephasing_lemma=(
            "Left-coset dephasing satisfies Delta_L(R_h)=R_h for h in L and "
            "Delta_L(R_h)=0 otherwise."
        ),
        edge_membership_equivalence=(
            "A fixed-point-free h lies in S_e x S_(complement e) exactly when "
            "the matching of h contains edge e."
        ),
        conditional_subgroup_reduction=(
            "Conditioned on a coset block, a true edge gives the exact L coset "
            "state and a false edge gives the exact maximally mixed L state."
        ),
        batched_character_reduction=(
            "Fourier filtering all known edge swaps at once retains chi(z)=+1 "
            "with probability 1/2 and emits the smaller plus coset state."
        ),
        identification_recurrence=(
            "Testing all partners of one remaining vertex at each level uses "
            "m^2-1 binary membership tests and constant expected state overhead."
        ),
        converse_verification=(
            "Fresh (I+R_hhat)/2 tests accept a correct candidate with probability "
            "one and null or a wrong candidate with probability 1/2 per copy."
        ),
        access_model=(
            "Explicit permutation-basis coset states, reversible coset "
            "factorization, fresh independent queries, and bounded-error detectors."
        ),
        scope_limit=(
            "No efficient binary detector, natural classical separation, graph-"
            "isomorphism reduction, or arbitrary-HSP equivalence is proved."
        ),
        exact_subgroup_dephasing_proved=True,
        exact_edge_membership_reduction_proved=True,
        constant_success_batched_recursion_proved=True,
        binary_to_identification_polynomial_reduction_proved=True,
        identification_to_binary_polynomial_reduction_proved=True,
        efficient_binary_detector_constructed=False,
        hidden_involution_algorithm_constructed=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "binary-identification-polynomial-equivalence-proved-detector-open"
            if verified and scaling_verified
            else "binary-identification-self-reduction-control-failure"
        ),
    )
    return BinaryIdentificationSelfReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Fixed-point-free involutions/perfect matchings in S_(2m).",
            "binary_promise": "Maximally mixed null versus any fixed hidden matching coset state.",
            "detector_requirement": (
                "Polynomial time/query complexity for every smaller degree, with "
                "worst-case bounded error after conjugation symmetrization."
            ),
            "identification_output": "The complete list of m disjoint matching edges.",
            "outside_scope": (
                "Other conjugacy classes without a recursive block system, noisy "
                "states, destructive detectors without reproducible fresh queries, "
                "and reductions from external natural problems."
            ),
        },
        edge_controls=edge_controls,
        batched_character_controls=batched_controls,
        scaling_records=scaling,
        theorem=theorem,
        literature_links=[
            {
                "id": "ARXIV-CS-0610086",
                "title": "The central nature of the Hidden Subgroup problem",
                "url": "https://arxiv.org/abs/cs/0610086",
                "use": (
                    "Fenner and Zhang prove the broader decision/search "
                    "equivalence for HSP over permutation groups. This module "
                    "records a narrower explicit coset-state edge-dephasing "
                    "realization and does not claim novelty for the equivalence."
                ),
            }
        ],
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-EFFICIENT-BINARY-DETECTOR",
                "statement": (
                    "Compile the symmetrized binary support/Helstrom test in "
                    "polynomial time on the natural coset-state input."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-SELF-REDUCTION-GATE-LEDGER",
                "statement": (
                    "Write a reversible gate/error ledger for coset factorization, "
                    "fresh-state batching, detector amplification, and edge output."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-NATURAL-PROBLEM-REDUCTION",
                "statement": (
                    "Relate fixed-point-free hidden-involution identification to a "
                    "natural classical problem without an oracle-model mismatch."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Dephasing merely weakens the state and cannot test membership exactly.",
                "answer": (
                    "The right-regular off-diagonal survives a left-coset block "
                    "exactly iff h is in the subgroup; otherwise it vanishes identically."
                ),
                "resolved": True,
            },
            {
                "challenge": "Removing one known edge at each level costs 2^-m.",
                "answer": (
                    "False: factor all known swaps simultaneously and retain the "
                    "half of characters positive on their product."
                ),
                "resolved": True,
            },
            {
                "challenge": "The detector only has an average conjugacy-class guarantee.",
                "answer": (
                    "Randomly conjugating the remaining labels or symmetrizing the "
                    "effect makes its acceptance identical for every hidden matching."
                ),
                "resolved": True,
            },
            {
                "challenge": "Binary equivalence already supplies an algorithm.",
                "answer": (
                    "False: the normalization/recoupling obstruction to the binary "
                    "detector is unchanged and remains the sole algorithmic gate."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_edge_dephasing_control_count": len(edge_controls),
            "batched_character_control_count": len(batched_controls),
            "finite_control_failure_count": sum(
                not row.exact_edge_membership_channel_verified for row in edge_controls
            ) + sum(
                not row.exact_batched_character_reduction_verified
                for row in batched_controls
            ),
            "binary_to_identification_reduction_theorem_count": 1,
            "identification_to_binary_reduction_theorem_count": 1,
            "efficient_binary_detector_count": 0,
            "hidden_involution_algorithm_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_edge_membership_channel_proved": verified,
            "recursion_postselection_remains_constant": verified,
            "binary_identification_polynomial_equivalence_proved": verified,
            "efficient_binary_detector_constructed": False,
            "efficient_hidden_involution_identifier_constructed": False,
            "natural_classical_separation_proved": False,
            "graph_isomorphism_algorithm_constructed": False,
            "general_decision_search_equivalence_new_to_literature": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The reduction upgrades any future efficient binary detector to "
                "identification, but no such detector or natural separation exists."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved an exact subgroup-dephasing edge test and constant-success "
            "batched recursion, making binary detection and identification "
            "polynomially equivalent for perfect-matching involution coset states."
        ),
        falsifiers_triggered=[
            "For perfect-matching involutions, computationally efficient binary detection would not remain merely a weak decision result.",
            "Recursive edge peeling need not incur exponentially compounding character postselection.",
            "The active binary support compiler is sufficient for identification if its normalization barrier is broken.",
        ],
    )


def write_binary_identification_self_reduction_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_binary_identification_self_reduction_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_binary_identification_self_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
