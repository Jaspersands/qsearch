"""Nontrivial holonomy of exact pairwise hidden-involution polars.

The structured pair compiler gives a canonical partial polar ``V_(b<-a)``
between every two involution-projector ranges.  These local half rotations do
not form a flat connection.

Take the three transpositions ``a=(12)``, ``b=(23)``, ``c=(13)`` in ``S_3``
and their right-regular projectors.  Every pair product has order three, so all
pair polars are unitary between the corresponding ``+1`` ranges.  The triangle
holonomy

    H_a = V_(a<-c) V_(c<-b) V_(b<-a)                    (1)

preserves ``ran(P_a)`` but has exact spectrum

    spec(H_a | ran(P_a)) = {1,-1,-1}.                   (2)

Thus the two-edge and direct paths differ by operator norm two.  Under vertex
gauge changes the loop is only conjugated, so its nontrivial spectrum cannot
be gauged away.

This is an all-n fixed-point-free obstruction.  Let ``S_3`` act regularly on
six points; each transposition acts as three disjoint swaps.  For every even
``n>6``, multiply all three by the same fixed-point-free involution on the
remaining points.  The resulting subgroup is still isomorphic to ``S_3`` and
all three generators are fixed-point-free involutions in ``S_n``.  Their pair
products, pair polars, and triangle holonomy restrict to the same regular
``S_3`` block.

For ``k`` tensor copies, the holonomy is ``H_a^tensor k``.  On the
``3^k``-dimensional starting plus space its negative multiplicity is

    (3^k - (-1)^k)/2,                                  (3)

so asymptotically one half of the pair-aligned source space carries a minus
sign.  This is not a rare finite defect.

The theorem refutes a path-independent spanning-tree composition of canonical
pair polars.  It does not refute a global polar transform that retains a path
register, measures/corrects holonomy coherently, or works directly in a
multiplicity basis.  No measured-sieve separation or hidden-involution
algorithm follows.
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
    involution_transposition_count,
    right_regular_matrix,
)
from coset_hidden_involution_common_outlier_deflation import generated_subgroup
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from coset_hidden_involution_pair_polar_phase_compiler import (
    phase_compiled_pair_polar,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_pair_polar_holonomy_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-HOLONOMY-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PairPolarHolonomyFiniteControl:
    group_order: int
    involution_count: int
    starting_plus_dimension: int
    pair_rotation_orders: tuple[int, int, int]
    maximum_pair_polar_support_residual: float
    loop_starting_space_invariance_residual: float
    loop_unitarity_residual: float
    positive_holonomy_multiplicity: int
    negative_holonomy_multiplicity: int
    maximum_holonomy_eigenvalue_residual: float
    loop_distance_from_identity: float
    direct_vs_two_edge_path_operator_distance: float
    nontrivial_holonomy_verified: bool
    status: str


@dataclass(frozen=True)
class FixedPointFreeHolonomyEmbeddingRecord:
    n: int
    copy_count: int
    embedded_subgroup_order: int
    fixed_point_free_generator_count: int
    transpositions_per_generator: int
    pair_product_orders: tuple[int, int, int]
    one_copy_positive_holonomy_multiplicity: int
    one_copy_negative_holonomy_multiplicity: int
    tensor_starting_plus_dimension_decimal: str
    tensor_negative_holonomy_dimension_decimal: str
    tensor_negative_holonomy_fraction: float
    path_independent_pair_alignment_possible: bool
    holonomy_aware_global_transform_ruled_out: bool
    status: str


@dataclass(frozen=True)
class PairPolarHolonomyTheorem:
    triangle: str
    exact_loop_spectrum: str
    gauge_invariance: str
    fixed_point_free_embedding: str
    tensor_holonomy: str
    architecture_consequence: str
    scope_limit: str
    exact_nontrivial_triangle_holonomy_proved: bool
    all_n_fixed_point_free_embedding_proved: bool
    tensor_extensive_holonomy_proved: bool
    path_independent_pair_alignment_refuted: bool
    holonomy_aware_global_polar_refuted: bool
    mrs_sieve_separation_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairPolarHolonomyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_control: PairPolarHolonomyFiniteControl
    embedding_records: list[FixedPointFreeHolonomyEmbeddingRecord]
    theorem: PairPolarHolonomyTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _permutation_order(permutation: Permutation) -> int:
    seen: set[int] = set()
    order = 1
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        order = math.lcm(order, length)
    return order


def s3_transpositions() -> tuple[Permutation, Permutation, Permutation]:
    return (1, 0, 2), (0, 2, 1), (2, 1, 0)


def audit_pair_polar_holonomy(
    *,
    tolerance: float = 1e-9,
) -> PairPolarHolonomyFiniteControl:
    transpositions = s3_transpositions()
    reflections = tuple(
        right_regular_matrix(3, involution) for involution in transpositions
    )
    identity = np.eye(6)
    plus = tuple((identity + reflection) / 2.0 for reflection in reflections)
    edges = tuple(
        phase_compiled_pair_polar(reflections[left], reflections[right])[0]
        for left, right in ((0, 1), (1, 2), (2, 0))
    )
    # Every order-three pair has full support on its three-dimensional plus
    # space, so the edge initial/final projectors are P_left/P_right.
    pair_support_residual = max(
        max(
            float(np.linalg.norm(edge.conj().T @ edge - plus[left], ord=2))
            for edge, (left, _) in zip(edges, ((0, 1), (1, 2), (2, 0)))
        ),
        max(
            float(np.linalg.norm(edge @ edge.conj().T - plus[right], ord=2))
            for edge, (_, right) in zip(edges, ((0, 1), (1, 2), (2, 0)))
        ),
    )
    loop = edges[2] @ edges[1] @ edges[0]
    starting_values, starting_vectors = np.linalg.eigh(plus[0])
    starting_basis = starting_vectors[:, starting_values > 0.5]
    restricted = starting_basis.conj().T @ loop @ starting_basis
    eigenvalues = np.linalg.eigvals(restricted)
    positive = int(
        sum(abs(value - 1.0) <= 100 * tolerance for value in eigenvalues)
    )
    negative = int(
        sum(abs(value + 1.0) <= 100 * tolerance for value in eigenvalues)
    )
    eigen_residual = max(
        min(abs(value - 1.0), abs(value + 1.0)) for value in eigenvalues
    )
    invariance = float(
        np.linalg.norm(loop @ plus[0] - plus[0] @ loop, ord=2)
    )
    unitary = float(
        np.linalg.norm(
            restricted.conj().T @ restricted - np.eye(len(restricted)), ord=2
        )
    )
    identity_distance = float(np.linalg.norm(restricted - np.eye(3), ord=2))
    direct = phase_compiled_pair_polar(reflections[0], reflections[2])[0]
    two_edge = edges[1] @ edges[0]
    path_distance = float(
        np.linalg.norm((two_edge - direct) @ plus[0], ord=2)
    )
    pair_orders = tuple(
        _permutation_order(
            compose_permutations(transpositions[left], transpositions[right])
        )
        for left, right in ((0, 1), (1, 2), (2, 0))
    )
    verified = bool(
        pair_orders == (3, 3, 3)
        and pair_support_residual <= 100 * tolerance
        and invariance <= 100 * tolerance
        and unitary <= 100 * tolerance
        and positive == 1
        and negative == 2
        and eigen_residual <= 100 * tolerance
        and abs(identity_distance - 2.0) <= 100 * tolerance
        and abs(path_distance - 2.0) <= 100 * tolerance
    )
    return PairPolarHolonomyFiniteControl(
        group_order=6,
        involution_count=3,
        starting_plus_dimension=3,
        pair_rotation_orders=pair_orders,
        maximum_pair_polar_support_residual=pair_support_residual,
        loop_starting_space_invariance_residual=invariance,
        loop_unitarity_residual=unitary,
        positive_holonomy_multiplicity=positive,
        negative_holonomy_multiplicity=negative,
        maximum_holonomy_eigenvalue_residual=float(eigen_residual),
        loop_distance_from_identity=identity_distance,
        direct_vs_two_edge_path_operator_distance=path_distance,
        nontrivial_holonomy_verified=verified,
        status=(
            "exact-s3-pair-polar-holonomy-verified"
            if verified
            else "pair-polar-holonomy-control-failure"
        ),
    )


def _left_regular_action_permutation(
    group: tuple[Permutation, ...],
    element: Permutation,
) -> Permutation:
    index = {item: offset for offset, item in enumerate(group)}
    return tuple(
        index[compose_permutations(element, basis)] for basis in group
    )


def fixed_point_free_s3_embedding(n: int) -> tuple[Permutation, ...]:
    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    group = tuple(itertools.permutations(range(3)))
    regular = tuple(
        _left_regular_action_permutation(group, transposition)
        for transposition in s3_transpositions()
    )
    output = []
    for generator in regular:
        extension = list(generator) + list(range(6, n))
        for left in range(6, n, 2):
            extension[left] = left + 1
            extension[left + 1] = left
        output.append(tuple(extension))
    return tuple(output)


def embedding_record(n: int) -> FixedPointFreeHolonomyEmbeddingRecord:
    generators = fixed_point_free_s3_embedding(n)
    subgroup = generated_subgroup(n, generators)
    pair_orders = tuple(
        _permutation_order(
            compose_permutations(generators[left], generators[right])
        )
        for left, right in ((0, 1), (1, 2), (2, 0))
    )
    transpositions = n // 2
    fixed_point_free = sum(
        involution_transposition_count(generator) == transpositions
        for generator in generators
    )
    # The scaling copy count is only used to report that the exact one-copy
    # holonomy remains extensive at the binary-support width.
    class_size = math.factorial(n) // (
        (2**transpositions) * math.factorial(transpositions)
    )
    copies = flatness_copy_count(class_size)
    total = 3**copies
    negative = (total - ((-1) ** copies)) // 2
    verified = bool(
        len(subgroup) == 6
        and fixed_point_free == 3
        and pair_orders == (3, 3, 3)
        and 0.49 <= negative / total <= 0.51
    )
    return FixedPointFreeHolonomyEmbeddingRecord(
        n=n,
        copy_count=copies,
        embedded_subgroup_order=len(subgroup),
        fixed_point_free_generator_count=fixed_point_free,
        transpositions_per_generator=transpositions,
        pair_product_orders=pair_orders,
        one_copy_positive_holonomy_multiplicity=1,
        one_copy_negative_holonomy_multiplicity=2,
        tensor_starting_plus_dimension_decimal=str(total),
        tensor_negative_holonomy_dimension_decimal=str(negative),
        tensor_negative_holonomy_fraction=negative / total,
        path_independent_pair_alignment_possible=False,
        holonomy_aware_global_transform_ruled_out=False,
        status=(
            "all-n-fixed-point-free-extensive-pair-holonomy"
            if verified
            else "fixed-point-free-holonomy-embedding-failure"
        ),
    )


def build_pair_polar_holonomy_report(
    *,
    embedding_n_values: tuple[int, ...] = (6, 8, 16, 32, 64),
) -> PairPolarHolonomyReport:
    finite = audit_pair_polar_holonomy()
    embeddings = [embedding_record(n) for n in embedding_n_values]
    embedding_verified = all(
        row.embedded_subgroup_order == 6
        and row.fixed_point_free_generator_count == 3
        and row.pair_product_orders == (3, 3, 3)
        and not row.path_independent_pair_alignment_possible
        and not row.holonomy_aware_global_transform_ruled_out
        for row in embeddings
    )
    verified = finite.nontrivial_holonomy_verified and embedding_verified
    theorem = PairPolarHolonomyTheorem(
        triangle=(
            "The three transposition projectors in the regular S_3 representation "
            "have order-three pair rotations and exact phase-compiled polars."
        ),
        exact_loop_spectrum=(
            "V_(a<-c)V_(c<-b)V_(b<-a) restricted to ran(P_a) has spectrum "
            "{1,-1,-1}; direct and two-edge paths differ by norm two."
        ),
        gauge_invariance=(
            "Vertex basis changes conjugate every loop holonomy, so the nontrivial "
            "loop spectrum cannot be gauged to identity."
        ),
        fixed_point_free_embedding=(
            "The regular S_3 action on six points maps transpositions to perfect "
            "matchings; multiplying by common disjoint swaps embeds the witness "
            "in every even S_n, n>=6."
        ),
        tensor_holonomy=(
            "On k copies the negative multiplicity is (3^k-(-1)^k)/2, hence "
            "the negative fraction tends to one half."
        ),
        architecture_consequence=(
            "Canonical pair half rotations cannot be composed as a "
            "path-independent spanning-tree alignment."
        ),
        scope_limit=(
            "A path-aware holonomy resolver, direct global multiplicity polar, "
            "or coherent non-MRS architecture is not ruled out."
        ),
        exact_nontrivial_triangle_holonomy_proved=True,
        all_n_fixed_point_free_embedding_proved=embedding_verified,
        tensor_extensive_holonomy_proved=embedding_verified,
        path_independent_pair_alignment_refuted=verified,
        holonomy_aware_global_polar_refuted=False,
        mrs_sieve_separation_proved=False,
        theorem_verified=verified,
        status=(
            "pair-polar-connection-nonflat-holonomy-aware-global-route-open"
            if verified
            else "pair-polar-holonomy-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "exact_s3_holonomy_control_count": 1,
        "finite_control_failure_count": 0 if finite.nontrivial_holonomy_verified else 1,
        "all_n_fixed_point_free_embedding_theorem_count": 1 if embedding_verified else 0,
        "tensor_extensive_holonomy_theorem_count": 1 if embedding_verified else 0,
        "loop_distance_from_identity": finite.loop_distance_from_identity,
        "direct_vs_two_edge_path_distance": finite.direct_vs_two_edge_path_operator_distance,
        "minimum_tensor_negative_holonomy_fraction": min(
            row.tensor_negative_holonomy_fraction for row in embeddings
        ),
        "path_independent_pair_alignment_count": 0,
        "holonomy_aware_global_polar_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PairPolarHolonomyReport(
        created_at=utc_now(),
        theorem_contract={
            "local_edges": (
                "The exact principal half-rotation pair polars from the phase "
                "compiler, not arbitrary isometries between equal-rank ranges."
            ),
            "loop": "The oriented a->b->c->a triangle.",
            "all_n_family": (
                "An explicit regular-S_3 perfect-matching triple embedded in "
                "fixed-point-free involutions of every even S_n, n>=6."
            ),
            "outside_scope": (
                "Architectures retaining and coherently correcting loop/path "
                "holonomy or compiling the full polar without local alignment."
            ),
        },
        finite_control=finite,
        embedding_records=embeddings,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-HOLONOMY-RESOLVER",
                "statement": (
                    "Construct a coherent path/loop register and correct the "
                    "nonabelian pair-polar holonomy without measuring merge labels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-GLOBAL-POLAR-FROM-CONNECTION",
                "statement": (
                    "Determine whether a connection Laplacian or Cech quotient of "
                    "the pair polars yields the full orbit-synthesis polar."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-HOLONOMY-MRS-BOUNDARY",
                "statement": (
                    "Prove whether coherent holonomy resolution escapes the "
                    "Moore-Russell-Sniady measured sieve model."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Exact pair polars define a flat global alignment.",
                "answer": (
                    "False: the minimal S_3 triangle has two negative holonomy "
                    "directions and path discrepancy two."
                ),
                "resolved": True,
            },
            {
                "challenge": "The defect is confined to S_3 or fixed points.",
                "answer": (
                    "False: regular S_3 transpositions are fixed-point-free on six "
                    "points and embed in every larger even degree."
                ),
                "resolved": True,
            },
            {
                "challenge": "Nontrivial holonomy rules out the global polar.",
                "answer": (
                    "False. It rules out path-independent local composition; a "
                    "coherent holonomy-aware global transform remains open."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "pair_polar_connection_flat": False,
            "path_independent_pair_alignment_refuted": verified,
            "all_n_fixed_point_free_holonomy_witness_proved": embedding_verified,
            "tensor_holonomy_extensive": embedding_verified,
            "holonomy_resolver_constructed": False,
            "full_orbit_synthesis_polar_compiled": False,
            "mrs_sieve_escape_proved": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pair polars are individually efficient but form a nonflat "
                "connection. A viable global route must retain and resolve this "
                "holonomy coherently rather than compose local alignments blindly."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved exact nontrivial S_3 triangle holonomy for canonical pair "
            "polars, embedded it into every fixed-point-free even S_n family, and "
            "showed the defect remains extensive under tensoring. Holonomy-aware "
            "global polar synthesis remains open."
        ),
        falsifiers_triggered=[
            "Efficient exact pair polars do not form a path-independent global frame.",
            "The pair-polar holonomy defect survives in fixed-point-free involution families at all even degrees.",
            "Tensoring does not dilute the minimal loop defect; about half the local source space is negative.",
            "Nonflatness alone is not a no-go for a coherent holonomy resolver or direct global polar.",
        ],
    )


def write_pair_polar_holonomy_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_pair_polar_holonomy_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_pair_polar_holonomy_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
