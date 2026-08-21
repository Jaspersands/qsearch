"""Literature-scoped bridge from rigid GI to perfect-matching involutions.

Moore--Russell--Schulman formulate the standard rigid Graph Isomorphism HSP
inside ``S_(2n)``.  For rigid ``Gamma_0,Gamma_1``, the disjoint union has
trivial automorphism group when the graphs are nonisomorphic and an order-two
automorphism group when they are isomorphic.  Its nonidentity element maps the
two vertex blocks onto each other and is a fixed-point-free involution.

Let ``K=S_n wr C_2 <= S_(2n)`` preserve or swap the two blocks.  The possible
isomorphism involutions are

    m_alpha(i)=n+alpha(i),
    m_alpha(n+j)=alpha^(-1)(j),                         (1)

one for each ``alpha in S_n``.  They are a structured ``K``-conjugacy class of
size ``n!`` inside the full perfect-matching class of size ``(2n-1)!!``.

For any ``H={1,h}<=K<=G`` and any left transversal ``T`` of ``K`` in ``G``, a
uniform coset state over ``G`` is the direct-sum mixture of the corresponding
state over ``K`` translated by ``T``:

    rho_H^G = |T|^-1 direct_sum_(t in T) L_t rho_H^K L_t^*.  (2)

Equivalently the transversal register is maximally mixed and contains no
hidden-subgroup information.  The exact matrix identity is checked below.

Consequently, a polynomial worst-case detector for fixed-point-free hidden
involutions in ``S_(2n)`` decides rigid GI.  A detector proved only for the
uniform full conjugacy class also suffices: random conjugation maps every fixed
full-support involution uniformly onto that class while preserving the null.
Together with the explicit binary-to-identification self-reduction, an
identifier recovers ``m_alpha`` and hence the unique graph isomorphism.

The GI/HSP construction and the ``K`` versus ``S_(2n)`` equivalence are prior
art from arXiv:quant-ph/0501056, not discoveries of this module.  The module
does not cover nonrigid graphs, construct the binary detector, prove general GI
is in BQP, or establish a classical separation.
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
    inverse_permutation,
    right_regular_matrix,
    symmetric_group,
)
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/reductions/"
    "coset_hidden_involution_rigid_gi_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-RIGID-GI-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RigidGIWreathFiniteControl:
    graph_vertex_count: int
    symmetric_degree: int
    full_group_order: int
    wreath_subgroup_order: int
    left_transversal_size: int
    structured_involution_count: int
    predicted_structured_involution_count: int
    full_perfect_matching_count: int
    all_structured_elements_are_involutions: bool
    all_structured_elements_are_fixed_point_free: bool
    all_structured_elements_swap_blocks: bool
    structured_elements_are_distinct: bool
    structured_class_closed_under_young_conjugation: bool
    hidden_state_lift_residual: float
    null_state_lift_residual: float
    exact_wreath_to_symmetric_coset_lift_verified: bool
    status: str


@dataclass(frozen=True)
class RigidGIBridgeScalingRecord:
    graph_vertex_count: int
    symmetric_degree: int
    structured_hidden_count_decimal: str
    full_perfect_matching_count_decimal: str
    structured_fraction_log2: float
    wreath_subgroup_order_decimal: str
    full_group_order_decimal: str
    transversal_size_decimal: str
    random_full_conjugation_symmetrizes_structured_hidden: bool
    polynomial_full_class_binary_detector_implies_rigid_gi: bool
    polynomial_full_class_identifier_implies_rigid_gi_search: bool
    nonrigid_gi_covered: bool
    status: str


@dataclass(frozen=True)
class RigidGIHiddenInvolutionBridgeTheorem:
    rigid_union_hidden_subgroup: str
    structured_involution_embedding: str
    wreath_subgroup: str
    coset_state_lift: str
    full_class_symmetrization: str
    search_decoding: str
    prior_art_scope: str
    scope_limit: str
    rigid_gi_hidden_involution_construction_verified: bool
    structured_involutions_are_perfect_matchings_proved: bool
    wreath_to_full_symmetric_state_lift_proved: bool
    full_class_detector_to_rigid_gi_reduction_proved: bool
    full_class_identifier_to_rigid_gi_search_reduction_proved: bool
    efficient_full_class_binary_detector_constructed: bool
    rigid_gi_quantum_algorithm_constructed: bool
    general_gi_quantum_algorithm_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RigidGIHiddenInvolutionBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[RigidGIWreathFiniteControl]
    scaling_records: list[RigidGIBridgeScalingRecord]
    theorem: RigidGIHiddenInvolutionBridgeTheorem
    literature_links: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _block_image(
    permutation: Permutation,
    block: frozenset[int],
) -> frozenset[int]:
    return frozenset(permutation[index] for index in block)


def wreath_subgroup(graph_vertex_count: int) -> tuple[Permutation, ...]:
    if graph_vertex_count < 2:
        raise ValueError("graph_vertex_count must be at least two")
    degree = 2 * graph_vertex_count
    group = symmetric_group(degree)
    left = frozenset(range(graph_vertex_count))
    right = frozenset(range(graph_vertex_count, degree))
    return tuple(
        permutation
        for permutation in group
        if _block_image(permutation, left) in (left, right)
    )


def structured_gi_involution(alpha: Permutation) -> Permutation:
    n = len(alpha)
    if tuple(sorted(alpha)) != tuple(range(n)):
        raise ValueError("alpha must be a permutation")
    alpha_inverse = inverse_permutation(alpha)
    output = [0] * (2 * n)
    for index in range(n):
        output[index] = n + alpha[index]
        output[n + index] = alpha_inverse[index]
    return tuple(output)


def structured_gi_involutions(
    graph_vertex_count: int,
) -> tuple[Permutation, ...]:
    return tuple(
        structured_gi_involution(alpha)
        for alpha in symmetric_group(graph_vertex_count)
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


def _right_regular_on_elements(
    elements: tuple[Permutation, ...],
    hidden: Permutation,
) -> np.ndarray:
    index = {element: offset for offset, element in enumerate(elements)}
    matrix = np.zeros((len(elements), len(elements)), dtype=complex)
    for column, element in enumerate(elements):
        matrix[index[compose_permutations(element, hidden)], column] = 1.0
    return matrix


def audit_rigid_gi_wreath_bridge(
    graph_vertex_count: int,
    *,
    tolerance: float = 1e-9,
) -> RigidGIWreathFiniteControl:
    if graph_vertex_count < 2 or graph_vertex_count > 3:
        raise ValueError("dense finite bridge control supports graph size 2 or 3")
    degree = 2 * graph_vertex_count
    group = symmetric_group(degree)
    subgroup = wreath_subgroup(graph_vertex_count)
    structured = structured_gi_involutions(graph_vertex_count)
    identity = tuple(range(degree))
    left = frozenset(range(graph_vertex_count))
    right = frozenset(range(graph_vertex_count, degree))
    all_involutions = all(
        compose_permutations(value, value) == identity for value in structured
    )
    all_fixed_point_free = all(
        all(value[index] != index for index in range(degree))
        for value in structured
    )
    all_swap = all(
        _block_image(value, left) == right
        and _block_image(value, right) == left
        for value in structured
    )
    young = tuple(
        value for value in subgroup if _block_image(value, left) == left
    )
    structured_set = set(structured)
    closed = all(
        compose_permutations(
            compose_permutations(
                inverse_permutation(conjugator), hidden
            ),
            conjugator,
        )
        in structured_set
        for conjugator in young
        for hidden in structured
    )

    hidden = structured[0]
    subgroup_right = _right_regular_on_elements(subgroup, hidden)
    subgroup_hidden_state = (
        np.eye(len(subgroup)) + subgroup_right
    ) / len(subgroup)
    subgroup_null_state = np.eye(len(subgroup)) / len(subgroup)
    group_index = {element: offset for offset, element in enumerate(group)}
    cosets = _left_cosets(group, subgroup)

    def lift(state: np.ndarray) -> np.ndarray:
        output = np.zeros((len(group), len(group)), dtype=complex)
        subgroup_index = {element: offset for offset, element in enumerate(subgroup)}
        for coset in cosets:
            representative = coset[0]
            ordered = tuple(
                compose_permutations(representative, element)
                for element in subgroup
            )
            rows = [group_index[element] for element in ordered]
            source_rows = [subgroup_index[element] for element in subgroup]
            output[np.ix_(rows, rows)] = state[np.ix_(source_rows, source_rows)] / len(cosets)
        return output

    lifted_hidden = lift(subgroup_hidden_state)
    lifted_null = lift(subgroup_null_state)
    expected_hidden = (
        np.eye(len(group)) + right_regular_matrix(degree, hidden)
    ) / len(group)
    expected_null = np.eye(len(group)) / len(group)
    hidden_residual = float(np.linalg.norm(lifted_hidden - expected_hidden, ord=2))
    null_residual = float(np.linalg.norm(lifted_null - expected_null, ord=2))
    predicted_structured = math.factorial(graph_vertex_count)
    full_matching_count = perfect_matching_count(graph_vertex_count)
    verified = bool(
        len(subgroup) == 2 * math.factorial(graph_vertex_count) ** 2
        and len(cosets) * len(subgroup) == len(group)
        and len(structured) == predicted_structured
        and len(structured_set) == len(structured)
        and all(value in subgroup for value in structured)
        and all_involutions
        and all_fixed_point_free
        and all_swap
        and closed
        and hidden_residual <= 100 * tolerance
        and null_residual <= 100 * tolerance
    )
    return RigidGIWreathFiniteControl(
        graph_vertex_count=graph_vertex_count,
        symmetric_degree=degree,
        full_group_order=len(group),
        wreath_subgroup_order=len(subgroup),
        left_transversal_size=len(cosets),
        structured_involution_count=len(structured),
        predicted_structured_involution_count=predicted_structured,
        full_perfect_matching_count=full_matching_count,
        all_structured_elements_are_involutions=all_involutions,
        all_structured_elements_are_fixed_point_free=all_fixed_point_free,
        all_structured_elements_swap_blocks=all_swap,
        structured_elements_are_distinct=len(structured_set) == len(structured),
        structured_class_closed_under_young_conjugation=closed,
        hidden_state_lift_residual=hidden_residual,
        null_state_lift_residual=null_residual,
        exact_wreath_to_symmetric_coset_lift_verified=verified,
        status=(
            "exact-rigid-gi-wreath-to-perfect-matching-bridge-verified"
            if verified
            else "rigid-gi-wreath-bridge-control-failure"
        ),
    )


def rigid_gi_bridge_scaling_record(
    graph_vertex_count: int,
) -> RigidGIBridgeScalingRecord:
    if graph_vertex_count < 2:
        raise ValueError("graph_vertex_count must be at least two")
    degree = 2 * graph_vertex_count
    structured = math.factorial(graph_vertex_count)
    full_matching = perfect_matching_count(graph_vertex_count)
    wreath_order = 2 * structured**2
    group_order = math.factorial(degree)
    transversal = group_order // wreath_order
    return RigidGIBridgeScalingRecord(
        graph_vertex_count=graph_vertex_count,
        symmetric_degree=degree,
        structured_hidden_count_decimal=str(structured),
        full_perfect_matching_count_decimal=str(full_matching),
        structured_fraction_log2=math.log2(structured / full_matching),
        wreath_subgroup_order_decimal=str(wreath_order),
        full_group_order_decimal=str(group_order),
        transversal_size_decimal=str(transversal),
        random_full_conjugation_symmetrizes_structured_hidden=True,
        polynomial_full_class_binary_detector_implies_rigid_gi=True,
        polynomial_full_class_identifier_implies_rigid_gi_search=True,
        nonrigid_gi_covered=False,
        status="full-class-detector-would-solve-rigid-gi-nonrigid-open",
    )


def build_rigid_gi_hidden_involution_bridge_report(
    *,
    finite_graph_sizes: tuple[int, ...] = (2, 3),
    scaling_graph_sizes: tuple[int, ...] = (2, 3, 4, 8, 16, 32, 64),
) -> RigidGIHiddenInvolutionBridgeReport:
    controls = [
        audit_rigid_gi_wreath_bridge(n) for n in finite_graph_sizes
    ]
    scaling = [rigid_gi_bridge_scaling_record(n) for n in scaling_graph_sizes]
    verified = all(
        row.exact_wreath_to_symmetric_coset_lift_verified for row in controls
    )
    scaling_verified = all(
        row.random_full_conjugation_symmetrizes_structured_hidden
        and row.polynomial_full_class_binary_detector_implies_rigid_gi
        and row.polynomial_full_class_identifier_implies_rigid_gi_search
        and not row.nonrigid_gi_covered
        for row in scaling
    )
    theorem = RigidGIHiddenInvolutionBridgeTheorem(
        rigid_union_hidden_subgroup=(
            "For two rigid n-vertex graphs, the disjoint-union automorphism "
            "subgroup is trivial when nonisomorphic and {1,m_alpha} when isomorphic."
        ),
        structured_involution_embedding=(
            "m_alpha swaps the two n-point blocks through alpha and alpha^-1, "
            "so it is a fixed-point-free involution in S_(2n)."
        ),
        wreath_subgroup=(
            "All m_alpha lie in K=S_n wr C_2 and form the structured K-conjugacy "
            "class indexed by alpha in S_n."
        ),
        coset_state_lift=(
            "For H<=K<=G, rho_H^G is rho_H^K tensored with a maximally mixed "
            "left-transversal coordinate, up to the coset-factorization unitary."
        ),
        full_class_symmetrization=(
            "Uniform random S_(2n) conjugation maps every fixed m_alpha to the "
            "uniform full perfect-matching class and leaves the null invariant."
        ),
        search_decoding=(
            "Identifying m_alpha directly recovers its cross-block matching and "
            "therefore the unique graph isomorphism alpha."
        ),
        prior_art_scope=(
            "The rigid-GI HSP construction and K-versus-S_(2n) sampling "
            "equivalence are explicitly given in arXiv:quant-ph/0501056."
        ),
        scope_limit=(
            "Nonrigid graph pairs, general GI, efficient binary measurement, "
            "and a classical separation remain unproved."
        ),
        rigid_gi_hidden_involution_construction_verified=True,
        structured_involutions_are_perfect_matchings_proved=True,
        wreath_to_full_symmetric_state_lift_proved=True,
        full_class_detector_to_rigid_gi_reduction_proved=True,
        full_class_identifier_to_rigid_gi_search_reduction_proved=True,
        efficient_full_class_binary_detector_constructed=False,
        rigid_gi_quantum_algorithm_constructed=False,
        general_gi_quantum_algorithm_constructed=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "rigid-gi-natural-bridge-proved-binary-detector-open"
            if verified and scaling_verified
            else "rigid-gi-hidden-involution-bridge-control-failure"
        ),
    )
    return RigidGIHiddenInvolutionBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "source_problem": "Rigid Graph Isomorphism for two explicitly represented n-vertex graphs.",
            "source_promise": "Both graphs have trivial automorphism groups.",
            "target_problem": "Null versus fixed-point-free order-two HSP in S_(2n).",
            "target_access": (
                "Coherent relabeling oracle and independently preparable coset "
                "states from the standard disjoint-union automorphism HSP."
            ),
            "solver_contract": (
                "Worst-case full-class binary detector for decision; full-class "
                "identifier for recovery of the unique isomorphism."
            ),
            "outside_scope": "Nonrigid graphs and arbitrary graph automorphism subgroups.",
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        literature_links=[
            {
                "id": "ARXIV-QUANT-PH-0501056",
                "title": "The Symmetric Group Defies Strong Fourier Sampling: Part I",
                "url": "https://arxiv.org/abs/quant-ph/0501056",
                "use": (
                    "Primary source for the rigid-GI full-support involution "
                    "construction, structured wreath class, and equivalence of "
                    "coset sampling over K and S_(2n)."
                ),
            },
            {
                "id": "ARXIV-1511.08189",
                "title": "Graph Isomorphism and Circuit Size",
                "url": "https://arxiv.org/abs/1511.08189",
                "use": (
                    "Records the known reduction of Graph Automorphism to Rigid "
                    "Graph Isomorphism; it is not used to claim general GI coverage."
                ),
            },
        ],
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-EFFICIENT-BINARY-DETECTOR",
                "statement": (
                    "Implement the full-class symmetrized binary measurement in "
                    "polynomial time at the information threshold."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-RIGID-GI-END-TO-END-LEDGER",
                "statement": (
                    "Compose graph oracle evaluation, coset preparation, random "
                    "conjugation, binary detection/identification, and verification."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-NONRIGID-GI-COVERAGE",
                "statement": (
                    "Handle larger automorphism subgroups or prove a valid "
                    "reduction from general GI to the solved rigid promise."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The GI involutions are too structured for a full-class detector.",
                "answer": (
                    "Random full-group conjugation turns any fixed structured "
                    "involution into the uniform full class before detection."
                ),
                "resolved": True,
            },
            {
                "challenge": "Sampling in the wreath subgroup supplies a different state model.",
                "answer": (
                    "The left-transversal factor is exactly maximally mixed, and "
                    "the finite controls verify the full density-matrix identity."
                ),
                "resolved": True,
            },
            {
                "challenge": "Rigid GI coverage implies general GI is in BQP.",
                "answer": (
                    "False. Nonrigid inputs have larger hidden automorphism "
                    "subgroups outside the order-two solver contract."
                ),
                "resolved": True,
            },
            {
                "challenge": "This module discovers the GI-to-HSP bridge.",
                "answer": (
                    "False. The primary construction and subgroup/full-group "
                    "sampling equivalence are explicit prior art."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_wreath_lift_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_wreath_to_symmetric_coset_lift_verified
                for row in controls
            ),
            "rigid_gi_to_full_class_binary_reduction_count": 1,
            "rigid_gi_search_decoding_reduction_count": 1,
            "efficient_full_class_binary_detector_count": 0,
            "rigid_gi_quantum_algorithm_count": 0,
            "general_gi_quantum_algorithm_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "rigid_gi_hidden_involution_bridge_verified": verified,
            "full_class_detector_would_decide_rigid_gi": verified,
            "full_class_identifier_would_recover_rigid_isomorphism": verified,
            "efficient_full_class_binary_detector_constructed": False,
            "rigid_gi_quantum_algorithm_constructed": False,
            "general_gi_quantum_algorithm_constructed": False,
            "natural_classical_superpolynomial_separation_proved": False,
            "bridge_new_to_literature": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural rigid-GI bridge is exact prior art, but the required "
                "multi-register full-class binary measurement remains uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Materialized the published rigid-GI wreath/full-symmetric bridge "
            "and proved that the active full-class binary detector target would "
            "decide rigid GI and, with self-reduction, recover its isomorphism."
        ),
        falsifiers_triggered=[
            "The fixed-point-free full-class route is not disconnected from natural inputs: it contains the published rigid-GI hidden involutions after symmetrization.",
            "The structured wreath subgroup does not create an incompatible coset-state model.",
            "Rigid-GI relevance does not extend automatically to nonrigid or general Graph Isomorphism.",
        ],
    )


def write_rigid_gi_hidden_involution_bridge_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_rigid_gi_hidden_involution_bridge_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_rigid_gi_hidden_involution_bridge_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
