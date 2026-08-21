"""Biregular incidence-walk boundary for orbit-synthesis label erasure.

For a hidden involution ``h`` and one right-``<h>`` coset tuple ``c``, the
normalized source column is

    |v_(h,c)> = 2^(-k/2) sum_(z in {0,1}^k) |c h^z>.    (1)

Let ``B`` be the unnormalized ``0/1`` incidence matrix from source columns to
physical group tuples.  Every source column has degree ``2^k`` and every
physical tuple has degree ``M``, one column for each candidate involution.
For distinct candidates, two columns intersect in at most one physical tuple,
so their normalized overlap is either zero or ``2^-k``.  Consequently

    S = B/sqrt(2^k),
    S^*S = I + 2^-k A,                                 (2)

where ``A`` is the clique graph of a linear ``M``-uniform hypergraph, regular
of degree ``(M-1)2^k``.  Equivalently, on the physical side,

    BB^* = sum_(h in C) tensor_i(I+R_h),                (3)

the adjacency-plus-diagonal operator of an explicit Cayley-type graph on
``G^k`` whose generators apply one common involution to a nonempty register
subset.

Standard source/physical neighbor-state preparation gives the Szegedy
discriminant

    D_walk = B/sqrt(M 2^k) = S/sqrt(M).                (4)

The orbit-flatness theorem says at least ``29/32`` of alternative mass has
``S`` singular value in ``[1/sqrt(2),sqrt(3/2)]`` at six-copy overhead.  The
same mass therefore lies at ``Theta(M^-1/2)`` in ``D_walk``.  A globally
bounded generic polynomial/QSVT polar with ``p(0)=0`` and constant response on
that interval needs degree ``Omega(sqrt(M))`` by Bernstein's inequality.

Thus canonicalizing source multiplicities does not make ordinary local
incidence walks or generic singular-value amplification efficient.  This does
not rule out a structured symmetric-group Fourier row transform, exact
fast-forwarding, or another natural-input circuit.  Black-box Index Erasure
also has a tight square-root lower bound, but that result is cited only as an
analogy: the natural incidence family is highly structured and no reduction
to the black-box oracle problem is proved here.
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
    involution_class_size,
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_incidence_walk_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-INCIDENCE-WALK-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class IncidenceWalkFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    group_order: int
    candidate_count: int
    physical_vertex_count: int
    source_vertex_count: int
    source_column_degree: int
    physical_row_degree: int
    minimum_source_column_degree: int
    maximum_source_column_degree: int
    minimum_physical_row_degree: int
    maximum_physical_row_degree: int
    maximum_distinct_candidate_column_intersection: int
    maximum_same_candidate_distinct_column_intersection: int
    source_gram_formula_residual: float
    physical_cayley_formula_residual: float
    discriminant_top_singular_value: float
    source_gram_top_eigenvalue: float
    normalized_source_gram_variance: float
    predicted_normalized_source_gram_variance: float
    exact_incidence_model_verified: bool
    status: str


@dataclass(frozen=True)
class IncidenceWalkScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    source_column_degree_decimal: str
    physical_row_degree_decimal: str
    retained_alternative_mass: float
    retained_walk_singular_lower: float
    retained_walk_singular_upper: float
    generic_bounded_polar_degree_lower_order: str
    generic_polar_superpolynomial: bool
    local_neighbor_oracle_available: bool
    structured_fourier_row_escape_ruled_out: bool
    status: str


@dataclass(frozen=True)
class IncidenceWalkTheorem:
    incidence_degrees: str
    linear_intersections: str
    source_gram: str
    physical_graph: str
    walk_discriminant: str
    flatness_transfer: str
    bernstein_obstruction: str
    index_erasure_scope: str
    constructive_frontier: str
    exact_incidence_normal_form_proved: bool
    normalized_local_walk_access_constructed: bool
    generic_incidence_qsvt_sqrt_M_obstruction_proved: bool
    black_box_index_erasure_reduction_proved: bool
    structured_fourier_row_transform_ruled_out: bool
    full_orbit_synthesis_polar_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class IncidenceWalkReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[IncidenceWalkFiniteControl]
    scaling_records: list[IncidenceWalkScalingRecord]
    theorem: IncidenceWalkTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _coset_representatives(
    group: tuple[Permutation, ...],
    hidden: Permutation,
) -> tuple[Permutation, ...]:
    return tuple(
        sorted(
            {
                min(element, compose_permutations(element, hidden))
                for element in group
            }
        )
    )


def incidence_matrix(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[np.ndarray, tuple[Permutation, ...]]:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    group = symmetric_group(n)
    group_index = {element: offset for offset, element in enumerate(group)}
    candidates = involution_conjugacy_class(n, transposition_count)
    physical_tuples = tuple(itertools.product(group, repeat=copy_count))
    physical_index = {value: offset for offset, value in enumerate(physical_tuples)}
    columns: list[tuple[int, ...]] = []
    column_candidates: list[Permutation] = []
    for hidden in candidates:
        cosets = _coset_representatives(group, hidden)
        for representatives in itertools.product(cosets, repeat=copy_count):
            support = []
            for mask in range(2**copy_count):
                physical = tuple(
                    compose_permutations(representative, hidden)
                    if (mask >> coordinate) & 1
                    else representative
                    for coordinate, representative in enumerate(representatives)
                )
                support.append(physical_index[physical])
            columns.append(tuple(support))
            column_candidates.append(hidden)
    incidence = np.zeros((len(physical_tuples), len(columns)), dtype=float)
    for column, support in enumerate(columns):
        incidence[list(support), column] = 1.0
    return incidence, tuple(column_candidates)


def _right_regular_matrix(
    group: tuple[Permutation, ...],
    element: Permutation,
) -> np.ndarray:
    index = {value: offset for offset, value in enumerate(group)}
    matrix = np.zeros((len(group), len(group)), dtype=float)
    for column, value in enumerate(group):
        matrix[index[compose_permutations(value, element)], column] = 1.0
    return matrix


def audit_incidence_walk(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> IncidenceWalkFiniteControl:
    incidence, column_candidates = incidence_matrix(
        n, transposition_count, copy_count
    )
    group = symmetric_group(n)
    candidates = involution_conjugacy_class(n, transposition_count)
    subset_count = 2**copy_count
    candidate_count = len(candidates)
    source_gram = incidence.T @ incidence / subset_count
    adjacency = incidence.T @ incidence - subset_count * np.eye(incidence.shape[1])
    source_formula = np.eye(incidence.shape[1]) + adjacency / subset_count
    source_residual = float(np.linalg.norm(source_gram - source_formula, ord=2))

    physical_formula = np.zeros(
        (len(group) ** copy_count, len(group) ** copy_count), dtype=float
    )
    identity = np.eye(len(group))
    for hidden in candidates:
        one_copy = identity + _right_regular_matrix(group, hidden)
        tensor = one_copy
        for _ in range(copy_count - 1):
            tensor = np.kron(tensor, one_copy)
        physical_formula += tensor
    physical_residual = float(
        np.linalg.norm(incidence @ incidence.T - physical_formula, ord=2)
    )

    column_degrees = incidence.sum(axis=0)
    row_degrees = incidence.sum(axis=1)
    maximum_distinct = 0
    maximum_same = 0
    raw_gram = incidence.T @ incidence
    for left in range(incidence.shape[1]):
        for right in range(left + 1, incidence.shape[1]):
            overlap = int(round(raw_gram[left, right]))
            if column_candidates[left] == column_candidates[right]:
                maximum_same = max(maximum_same, overlap)
            else:
                maximum_distinct = max(maximum_distinct, overlap)
    discriminant = incidence / math.sqrt(candidate_count * subset_count)
    singular_values = np.linalg.svd(discriminant, compute_uv=False)
    gram_eigenvalues = np.linalg.eigvalsh(source_gram)
    normalized_variance = float(np.mean((gram_eigenvalues - 1.0) ** 2))
    predicted_variance = (candidate_count - 1) / subset_count
    verified = bool(
        np.all(column_degrees == subset_count)
        and np.all(row_degrees == candidate_count)
        and maximum_distinct <= 1
        and maximum_same == 0
        and source_residual <= 100 * tolerance
        and physical_residual <= 100 * tolerance
        and abs(float(singular_values[0]) - 1.0) <= 100 * tolerance
        and abs(float(gram_eigenvalues[-1]) - candidate_count) <= 100 * tolerance
        and abs(normalized_variance - predicted_variance) <= 100 * tolerance
    )
    return IncidenceWalkFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        group_order=len(group),
        candidate_count=candidate_count,
        physical_vertex_count=incidence.shape[0],
        source_vertex_count=incidence.shape[1],
        source_column_degree=subset_count,
        physical_row_degree=candidate_count,
        minimum_source_column_degree=int(np.min(column_degrees)),
        maximum_source_column_degree=int(np.max(column_degrees)),
        minimum_physical_row_degree=int(np.min(row_degrees)),
        maximum_physical_row_degree=int(np.max(row_degrees)),
        maximum_distinct_candidate_column_intersection=maximum_distinct,
        maximum_same_candidate_distinct_column_intersection=maximum_same,
        source_gram_formula_residual=source_residual,
        physical_cayley_formula_residual=physical_residual,
        discriminant_top_singular_value=float(singular_values[0]),
        source_gram_top_eigenvalue=float(gram_eigenvalues[-1]),
        normalized_source_gram_variance=normalized_variance,
        predicted_normalized_source_gram_variance=predicted_variance,
        exact_incidence_model_verified=verified,
        status=(
            "exact-biregular-linear-incidence-model-verified"
            if verified
            else "incidence-walk-control-failure"
        ),
    )


def incidence_walk_scaling_record(
    half_degree: int,
) -> IncidenceWalkScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    candidates = perfect_matching_count(half_degree)
    copies = flatness_copy_count(candidates)
    return IncidenceWalkScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        source_column_degree_decimal=str(2**copies),
        physical_row_degree_decimal=str(candidates),
        retained_alternative_mass=29.0 / 32.0,
        retained_walk_singular_lower=1.0 / math.sqrt(2.0 * candidates),
        retained_walk_singular_upper=math.sqrt(3.0 / (2.0 * candidates)),
        generic_bounded_polar_degree_lower_order="Omega(sqrt(M))",
        generic_polar_superpolynomial=True,
        local_neighbor_oracle_available=True,
        structured_fourier_row_escape_ruled_out=False,
        status="local-incidence-walk-normalized-too-small-structured-row-escape-open",
    )


def build_incidence_walk_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (4, 2, 1),
    ),
    scaling_half_degrees: tuple[int, ...] = (3, 4, 8, 16, 32, 64),
) -> IncidenceWalkReport:
    controls = [audit_incidence_walk(*spec) for spec in finite_specs]
    scaling = [incidence_walk_scaling_record(m) for m in scaling_half_degrees]
    verified = all(row.exact_incidence_model_verified for row in controls)
    theorem = IncidenceWalkTheorem(
        incidence_degrees=(
            "Every source column has 2^k physical neighbors and every physical "
            "tuple has one incident column per candidate, hence degree M."
        ),
        linear_intersections=(
            "Columns for one candidate are disjoint; columns for distinct "
            "candidates intersect in at most one physical tuple."
        ),
        source_gram=(
            "S^*S=I+2^-k A for the regular clique graph of the linear incidence hypergraph."
        ),
        physical_graph=(
            "BB^*=sum_h tensor_i(I+R_h), the subset-common-involution Cayley-type operator on G^k."
        ),
        walk_discriminant=(
            "Standard two-sided neighbor-state preparation yields D=B/sqrt(M2^k)=S/sqrt(M)."
        ),
        flatness_transfer=(
            "At least 29/32 alternative mass has D singular value between "
            "1/sqrt(2M) and sqrt(3/(2M))."
        ),
        bernstein_obstruction=(
            "A globally bounded generic polar polynomial responding constantly "
            "from zero over this scale has degree Omega(sqrt(M))."
        ),
        index_erasure_scope=(
            "Black-box coherent and noncoherent Index Erasure have tight "
            "square-root query lower bounds, but no natural-family reduction is claimed."
        ),
        constructive_frontier=(
            "Exploit symmetric-group row convolution, fast-forwarding, or another "
            "structured operation not expressible as generic local-walk QSVT."
        ),
        exact_incidence_normal_form_proved=True,
        normalized_local_walk_access_constructed=True,
        generic_incidence_qsvt_sqrt_M_obstruction_proved=True,
        black_box_index_erasure_reduction_proved=False,
        structured_fourier_row_transform_ruled_out=False,
        full_orbit_synthesis_polar_compiled=False,
        theorem_verified=verified,
        status=(
            "incidence-walk-sqrt-M-obstruction-structured-row-transform-open"
            if verified
            else "incidence-walk-control-failure"
        ),
    )
    return IncidenceWalkReport(
        created_at=utc_now(),
        theorem_contract={
            "access_model": (
                "Prepare uniform physical neighbors of a source column and "
                "uniform candidate/source neighbors of a physical tuple."
            ),
            "polynomial_model": (
                "Globally norm-bounded generic singular-value polynomial/QSVT "
                "on the normalized Szegedy discriminant."
            ),
            "retained_mass": (
                "The 29/32 alternative-mass relative-flatness window at "
                "k=ceil(log2(64M))."
            ),
            "outside_scope": (
                "Representation-specific rescaling, exact Fourier row transforms, "
                "fast-forwarding, and arbitrary natural-input circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-INCIDENCE-FAST-FORWARD",
                "statement": (
                    "Determine whether the subset-common-involution graph admits "
                    "structured fast-forwarding or an exact spectral transform."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ROW-CONVOLUTION-PRECONDITIONER",
                "statement": (
                    "Construct a Fourier/orbit-row preconditioner that changes the "
                    "effective normalization on constant alternative mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-NATURAL-INDEX-ERASURE-BOUNDARY",
                "statement": (
                    "Either reduce a valid natural access model to symmetric state "
                    "generation adversaries or exhibit the structure that evades them."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Source canonicalization normalizes the incidence walk at O(1).",
                "answer": (
                    "False for standard local neighbor access: the discriminant is "
                    "still S/sqrt(M) on the canonicalized coordinates."
                ),
                "resolved": True,
            },
            {
                "challenge": "Relative flatness makes generic QSVT efficient.",
                "answer": (
                    "False after legal walk normalization: the flat singular window "
                    "is centered at Theta(M^-1/2)."
                ),
                "resolved": True,
            },
            {
                "challenge": "Index Erasure lower bounds prove the natural no-go.",
                "answer": (
                    "False. Those are black-box state-generation results; the "
                    "natural symmetric incidence family may admit extra transforms."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "paper_id": "arxiv:1012.2112",
                "title": "Symmetry-assisted adversaries for quantum state generation",
                "url": "https://arxiv.org/abs/1012.2112",
                "use": "Tight coherent black-box Index Erasure lower bound; analogy only.",
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "arxiv:1902.07336",
                "title": "A Tight Lower Bound for Non-coherent Index Erasure",
                "url": "https://arxiv.org/abs/1902.07336",
                "use": "Tight noncoherent black-box bound; not transferred to the natural family.",
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics={
            "exact_incidence_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_incidence_model_verified for row in controls
            ),
            "local_neighbor_access_construction_count": 1,
            "generic_incidence_qsvt_sqrt_M_obstruction_count": 1,
            "black_box_index_erasure_reduction_count": 0,
            "structured_fourier_row_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_biregular_incidence_model_proved": verified,
            "standard_local_walk_discriminant_available": verified,
            "generic_local_walk_polar_polynomial": False,
            "generic_local_walk_sqrt_M_obstruction_proved": verified,
            "natural_problem_index_erasure_lower_bound_proved": False,
            "structured_fourier_row_escape_ruled_out": False,
            "full_orbit_synthesis_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Local incidence access retains a Theta(M^-1/2) singular scale on "
                "constant alternative mass. Only a representation-specific row "
                "transform or other non-generic mechanism can bypass it."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact linear biregular incidence graph behind source "
            "label erasure and proved that its standard Szegedy/QSVT access still "
            "costs Omega(sqrt(M)), preserving structured Fourier row synthesis as "
            "the sole positive escape rather than overclaiming black-box hardness."
        ),
        falsifiers_triggered=[
            "Source canonicalization does not improve the normalization of standard local incidence-walk access.",
            "Relative flatness before legal block-encoding normalization does not imply an efficient generic polar.",
            "Black-box Index Erasure lower bounds are not natural hidden-involution lower bounds.",
        ],
    )


def write_incidence_walk_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_incidence_walk_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_incidence_walk_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
