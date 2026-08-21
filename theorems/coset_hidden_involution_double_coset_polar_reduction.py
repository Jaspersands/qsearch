"""Double-coset normal form for the hidden-involution row polar.

Let ``G`` be a finite group, ``h`` an involution, ``H=<h>``, and
``K=C_G(h)``.  For ``k`` coset-state copies put ``L=G^k x G`` and define

    A = {(r,...,r;r): r in G},
    B = {(eps_1 r,...,eps_k r;r): r in K, eps_i in H}.

The physical tuples are the homogeneous space ``L/A``.  The source columns,
consisting of a conjugate of ``h`` and one right coset in every register, are
``L/B``.  A physical tuple occurs in a source column exactly when the two
right cosets of ``A`` and ``B`` intersect.

If ``V_A`` and ``V_B`` embed normalized right-coset states into ``C[L]``, the
normalized biregular incidence discriminant is therefore exactly

    D = V_A^* V_B = I / sqrt(2^k [G:K]).

Consequently the unresolved row polar is the Cosine-Sine alignment between
the right-``A`` and right-``B`` invariant subspaces of the regular
representation of ``L``.  Both subgroup reflections are efficiently
preparable for symmetric groups, but generic alternating-reflection phase
estimation still costs ``Omega(sqrt([G:K]))`` on the natural bulk because its
principal cosines are ``Theta([G:K]^-1/2)``.

This reduction also identifies why a scalar spherical transform is
insufficient.  In an ``L`` Fourier block
``nu_1 tensor ... tensor nu_k tensor tau``, the ``A``-fixed multiplicity is
``dim Inv_G(nu_1 tensor ... tensor nu_k tensor tau)``.  Already the fourth
tensor power of the standard ``S_n`` representation has fixed multiplicity
four for ``n>=4``; at the natural copy scale an even tensor power has the
identity-term lower bound ``(n-1)^r/n!``.  The required transform is genuinely
matrix-valued.

Large multiplicity is not a circuit lower bound.  A direct matrix
Cosine-Sine transform, partition-algebra fast transform, or structured
fast-forward could still compile the polar.  No detector or speedup is
claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    involution_class_size,
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_double_coset_polar_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-DOUBLE-COSET-POLAR-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

ProductElement = tuple[Permutation, ...]
Coset = frozenset[ProductElement]


@dataclass(frozen=True)
class DoubleCosetFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    group_order: int
    candidate_count: int
    ambient_product_group_order: int
    diagonal_subgroup_order: int
    source_stabilizer_order: int
    subgroup_intersection_order: int
    physical_coset_count: int
    source_coset_count: int
    predicted_physical_coset_count: int
    predicted_source_coset_count: int
    physical_incidence_degree: int
    source_incidence_degree: int
    nonzero_coset_overlap: float
    predicted_nonzero_coset_overlap: float
    maximum_coset_embedding_residual: float
    maximum_incidence_formula_residual: float
    discriminant_top_singular_value: float
    exact_homogeneous_space_bijections_verified: bool
    exact_double_coset_incidence_verified: bool
    status: str


@dataclass(frozen=True)
class DiagonalMultiplicityControl:
    n: int
    tensor_order: int
    standard_dimension: int
    exact_diagonal_invariant_multiplicity: int
    identity_term_multiplicity_lower_bound: float
    scalar_gelfand_multiplicity_free: bool
    exact_character_average_verified: bool
    status: str


@dataclass(frozen=True)
class DoubleCosetScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    matrix_tensor_order: int
    even_standard_tensor_order: int
    log2_identity_term_invariant_multiplicity_lower_bound: float
    retained_alternative_mass: float
    retained_principal_cosine_lower: float
    retained_principal_cosine_upper: float
    generic_reflection_phase_query_log2_lower_order: float
    efficient_subgroup_reflections_available: bool
    scalar_spherical_transform_sufficient: bool
    matrix_cosine_sine_transform_compiled: bool
    status: str


@dataclass(frozen=True)
class DoubleCosetPolarTheorem:
    ambient_group: str
    physical_stabilizer: str
    source_stabilizer: str
    homogeneous_spaces: str
    coset_embedding_identity: str
    principal_angle_form: str
    subgroup_reflection_access: str
    generic_phase_boundary: str
    fourier_multiplicity: str
    remaining_transform: str
    exact_double_coset_normal_form_proved: bool
    efficient_subgroup_reflections_available: bool
    generic_alternating_reflection_polar_polynomial: bool
    scalar_spherical_transform_sufficient: bool
    matrix_cosine_sine_transform_compiled: bool
    binary_hidden_involution_detector_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DoubleCosetPolarReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[DoubleCosetFiniteControl]
    multiplicity_controls: list[DiagonalMultiplicityControl]
    scaling_records: list[DoubleCosetScalingRecord]
    theorem: DoubleCosetPolarTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _identity(n: int) -> Permutation:
    return tuple(range(n))


def _conjugate(element: Permutation, value: Permutation) -> Permutation:
    return compose_permutations(
        compose_permutations(element, value), inverse_permutation(element)
    )


def _product_multiply(left: ProductElement, right: ProductElement) -> ProductElement:
    return tuple(
        compose_permutations(first, second)
        for first, second in zip(left, right)
    )


def _right_cosets(
    ambient: Iterable[ProductElement],
    subgroup: tuple[ProductElement, ...],
) -> tuple[Coset, ...]:
    unseen = set(ambient)
    output: list[Coset] = []
    while unseen:
        representative = min(unseen)
        coset = frozenset(
            _product_multiply(representative, element) for element in subgroup
        )
        output.append(coset)
        unseen.difference_update(coset)
    return tuple(sorted(output, key=min))


def hidden_involution_product_subgroups(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[
    tuple[ProductElement, ...],
    tuple[ProductElement, ...],
    tuple[ProductElement, ...],
    Permutation,
    tuple[Permutation, ...],
]:
    """Return ``(L,A,B,h,K)`` from the theorem statement."""

    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    group = symmetric_group(n)
    hidden = involution_conjugacy_class(n, transposition_count)[0]
    identity = _identity(n)
    order_two = (identity, hidden)
    centralizer = tuple(
        element for element in group if _conjugate(element, hidden) == hidden
    )
    ambient = tuple(itertools.product(group, repeat=copy_count + 1))
    diagonal = tuple((element,) * (copy_count + 1) for element in group)
    source_stabilizer = tuple(
        tuple(
            compose_permutations(epsilon, element) for epsilon in epsilons
        )
        + (element,)
        for element in centralizer
        for epsilons in itertools.product(order_two, repeat=copy_count)
    )
    return ambient, diagonal, source_stabilizer, hidden, centralizer


def _physical_key(coset: Coset) -> tuple[Permutation, ...]:
    representative = min(coset)
    *left, right = representative
    right_inverse = inverse_permutation(right)
    return tuple(
        compose_permutations(element, right_inverse) for element in left
    )


def _source_key(
    coset: Coset,
    hidden: Permutation,
) -> tuple[Permutation, tuple[Permutation, ...]]:
    representative = min(coset)
    *left, right = representative
    right_inverse = inverse_permutation(right)
    conjugate = _conjugate(right, hidden)
    coset_representatives = tuple(
        min(
            value,
            compose_permutations(value, conjugate),
        )
        for value in (
            compose_permutations(element, right_inverse) for element in left
        )
    )
    return conjugate, coset_representatives


def audit_double_coset_incidence(
    n: int = 3,
    transposition_count: int = 1,
    copy_count: int = 2,
    *,
    tolerance: float = 1e-10,
) -> DoubleCosetFiniteControl:
    if n > 3 or copy_count > 2:
        raise ValueError("explicit product-group controls require n<=3 and k<=2")
    ambient, diagonal, source_stabilizer, hidden, centralizer = (
        hidden_involution_product_subgroups(
            n, transposition_count, copy_count
        )
    )
    physical_cosets = _right_cosets(ambient, diagonal)
    source_cosets = _right_cosets(ambient, source_stabilizer)
    ambient_index = {element: index for index, element in enumerate(ambient)}

    physical_embedding = np.zeros((len(ambient), len(physical_cosets)))
    for column, coset in enumerate(physical_cosets):
        physical_embedding[
            [ambient_index[element] for element in coset], column
        ] = 1.0 / math.sqrt(len(diagonal))
    source_embedding = np.zeros((len(ambient), len(source_cosets)))
    for column, coset in enumerate(source_cosets):
        source_embedding[
            [ambient_index[element] for element in coset], column
        ] = 1.0 / math.sqrt(len(source_stabilizer))

    overlap = physical_embedding.T @ source_embedding
    intersection_formula = np.array(
        [
            [
                len(physical.intersection(source))
                / math.sqrt(len(diagonal) * len(source_stabilizer))
                for source in source_cosets
            ]
            for physical in physical_cosets
        ]
    )
    embedding_residual = float(np.max(np.abs(overlap - intersection_formula)))

    physical_keys = tuple(_physical_key(coset) for coset in physical_cosets)
    source_keys = tuple(_source_key(coset, hidden) for coset in source_cosets)
    homogeneous_bijections = (
        len(set(physical_keys)) == len(physical_keys)
        and len(set(source_keys)) == len(source_keys)
    )
    incidence = np.zeros_like(overlap)
    for row, physical in enumerate(physical_keys):
        for column, (candidate, representatives) in enumerate(source_keys):
            incidence[row, column] = all(
                value
                in (
                    representative,
                    compose_permutations(representative, candidate),
                )
                for value, representative in zip(physical, representatives)
            )

    candidate_count = involution_class_size(n, transposition_count)
    predicted_overlap = 1.0 / math.sqrt((2**copy_count) * candidate_count)
    predicted = incidence * predicted_overlap
    incidence_residual = float(np.max(np.abs(overlap - predicted)))
    nonzero_values = overlap[np.abs(overlap) > tolerance]
    top_singular = float(np.linalg.svd(overlap, compute_uv=False)[0])
    subgroup_intersection = len(set(diagonal).intersection(source_stabilizer))
    exact = bool(
        homogeneous_bijections
        and len(physical_cosets) == len(symmetric_group(n)) ** copy_count
        and len(source_cosets)
        == candidate_count * (len(symmetric_group(n)) // 2) ** copy_count
        and np.all(incidence.sum(axis=0) == 2**copy_count)
        and np.all(incidence.sum(axis=1) == candidate_count)
        and subgroup_intersection == len(centralizer)
        and embedding_residual <= tolerance
        and incidence_residual <= tolerance
        and abs(top_singular - 1.0) <= 100 * tolerance
    )
    return DoubleCosetFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        group_order=len(symmetric_group(n)),
        candidate_count=candidate_count,
        ambient_product_group_order=len(ambient),
        diagonal_subgroup_order=len(diagonal),
        source_stabilizer_order=len(source_stabilizer),
        subgroup_intersection_order=subgroup_intersection,
        physical_coset_count=len(physical_cosets),
        source_coset_count=len(source_cosets),
        predicted_physical_coset_count=len(symmetric_group(n)) ** copy_count,
        predicted_source_coset_count=(
            candidate_count * (len(symmetric_group(n)) // 2) ** copy_count
        ),
        physical_incidence_degree=int(incidence.sum(axis=1)[0]),
        source_incidence_degree=int(incidence.sum(axis=0)[0]),
        nonzero_coset_overlap=float(nonzero_values[0]),
        predicted_nonzero_coset_overlap=predicted_overlap,
        maximum_coset_embedding_residual=embedding_residual,
        maximum_incidence_formula_residual=incidence_residual,
        discriminant_top_singular_value=top_singular,
        exact_homogeneous_space_bijections_verified=homogeneous_bijections,
        exact_double_coset_incidence_verified=exact,
        status=(
            "exact-double-coset-incidence-normal-form-verified"
            if exact
            else "double-coset-incidence-control-failure"
        ),
    )


def standard_diagonal_invariant_multiplicity(
    n: int,
    tensor_order: int,
) -> int:
    """Multiplicity of the trivial irrep in ``Std_n^tensor_order``."""

    if n < 2 or tensor_order < 1:
        raise ValueError("n>=2 and positive tensor order are required")
    group = symmetric_group(n)
    numerator = sum(
        (sum(element[index] == index for index in range(n)) - 1)
        ** tensor_order
        for element in group
    )
    if numerator % len(group):
        raise AssertionError("character average is not integral")
    return numerator // len(group)


def audit_diagonal_multiplicity(
    n: int,
    tensor_order: int = 4,
) -> DiagonalMultiplicityControl:
    multiplicity = standard_diagonal_invariant_multiplicity(n, tensor_order)
    lower = (
        (n - 1) ** tensor_order / math.factorial(n)
        if tensor_order % 2 == 0
        else 0.0
    )
    expected = {3: 3, 4: 4}.get(n) if tensor_order == 4 else None
    verified = expected is None or multiplicity == expected
    return DiagonalMultiplicityControl(
        n=n,
        tensor_order=tensor_order,
        standard_dimension=n - 1,
        exact_diagonal_invariant_multiplicity=multiplicity,
        identity_term_multiplicity_lower_bound=lower,
        scalar_gelfand_multiplicity_free=multiplicity <= 1,
        exact_character_average_verified=verified,
        status=(
            "diagonal-invariant-multiplicity-is-matrix-valued"
            if verified and multiplicity > 1
            else "diagonal-multiplicity-control-failure"
        ),
    )


def double_coset_scaling_record(half_degree: int) -> DoubleCosetScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    tensor_order = copies + 1
    even_order = tensor_order if tensor_order % 2 == 0 else tensor_order - 1
    log2_multiplicity_lower = (
        even_order * math.log2(degree - 1)
        - math.lgamma(degree + 1) / math.log(2)
    )
    return DoubleCosetScalingRecord(
        half_degree=half_degree,
        degree=degree,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        matrix_tensor_order=tensor_order,
        even_standard_tensor_order=even_order,
        log2_identity_term_invariant_multiplicity_lower_bound=(
            log2_multiplicity_lower
        ),
        retained_alternative_mass=29.0 / 32.0,
        retained_principal_cosine_lower=1.0 / math.sqrt(2.0 * candidates),
        retained_principal_cosine_upper=math.sqrt(3.0 / (2.0 * candidates)),
        generic_reflection_phase_query_log2_lower_order=(
            0.5 * math.log2(candidates) - 0.5 * math.log2(3.0 / 2.0)
        ),
        efficient_subgroup_reflections_available=True,
        scalar_spherical_transform_sufficient=False,
        matrix_cosine_sine_transform_compiled=False,
        status="matrix-double-coset-polar-open-generic-reflections-superpolynomial",
    )


def build_double_coset_polar_report(
    *,
    scaling_half_degrees: tuple[int, ...] = (2, 3, 4, 8, 16, 32, 64),
) -> DoubleCosetPolarReport:
    finite = [
        audit_double_coset_incidence(3, 1, copy_count)
        for copy_count in (1, 2)
    ]
    multiplicities = [
        audit_diagonal_multiplicity(n, 4) for n in (3, 4)
    ]
    scaling = [
        double_coset_scaling_record(value) for value in scaling_half_degrees
    ]
    exact = all(row.exact_double_coset_incidence_verified for row in finite)
    matrix_valued = all(
        row.exact_character_average_verified
        and not row.scalar_gelfand_multiplicity_free
        for row in multiplicities
    )
    theorem = DoubleCosetPolarTheorem(
        ambient_group="L=G^k x G with componentwise multiplication.",
        physical_stabilizer="A=Delta(G)={(r,...,r;r)}.",
        source_stabilizer=(
            "B={(eps_1 r,...,eps_k r;r): r in C_G(h), eps_i in <h>}"
        ),
        homogeneous_spaces=(
            "L/A is the physical G^k basis and L/B is the full hidden-"
            "involution/coset-tuple source basis."
        ),
        coset_embedding_identity=(
            "For normalized right-coset embeddings V_A,V_B, "
            "V_A^*V_B=I_incidence/sqrt(2^k [G:C_G(h)])."
        ),
        principal_angle_form=(
            "The row polar is the Cosine-Sine alignment of the right-A and "
            "right-B invariant subspaces in C[L]."
        ),
        subgroup_reflection_access=(
            "Uniform A and B preparation gives exact invariant-subspace "
            "reflections for the symmetric/hyperoctahedral family."
        ),
        generic_phase_boundary=(
            "Natural-bulk principal cosines are Theta(M^-1/2), so generic "
            "alternating-reflection phase resolution costs Omega(sqrt(M))."
        ),
        fourier_multiplicity=(
            "The L-Fourier A-fixed block is Inv_G(nu_1 tensor ... tensor "
            "nu_k tensor tau), which is already non-multiplicity-free on "
            "four standard factors and grows rapidly at natural k."
        ),
        remaining_transform=(
            "Construct a direct matrix Cosine-Sine/partition-algebra transform "
            "with physical normalization, or prove a natural-model obstruction."
        ),
        exact_double_coset_normal_form_proved=exact,
        efficient_subgroup_reflections_available=True,
        generic_alternating_reflection_polar_polynomial=False,
        scalar_spherical_transform_sufficient=False,
        matrix_cosine_sine_transform_compiled=False,
        binary_hidden_involution_detector_constructed=False,
        theorem_verified=exact and matrix_valued,
        status=(
            "double-coset-cosine-sine-normal-form-proved-matrix-polar-open"
            if exact and matrix_valued
            else "double-coset-polar-reduction-control-failure"
        ),
    )
    return DoubleCosetPolarReport(
        created_at=utc_now(),
        theorem_contract={
            "input_model": (
                "Fresh right-coset states for a uniformly conjugated involution; "
                "no evaluator or chosen hidden label access."
            ),
            "normalization": (
                "The source synthesis is sqrt(M) times V_A^*V_B; scalar "
                "rescaling does not change its polar."
            ),
            "scope": (
                "The reduction covers the full untrimmed incidence operator. "
                "Trimmed orbit canonicalization is a source reindexing on its "
                "good subspace, not a different polar normalization."
            ),
            "claim_boundary": (
                "Exact homogeneous-space structure and generic-reflection no-go; "
                "no arbitrary-circuit lower bound or algorithm."
            ),
        },
        finite_controls=finite,
        multiplicity_controls=multiplicities,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-MATRIX-CS-TRANSFORM",
                "statement": (
                    "Construct the matrix Cosine-Sine transform between A- and "
                    "B-fixed multiplicity spaces without enumerating tensor "
                    "invariants."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-STRUCTURED-FAST-FORWARD",
                "statement": (
                    "Fast-forward the subgroup-reflection product near phase pi, "
                    "or expose a direct normalization that avoids sqrt(M)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-NATURAL-CLASSICAL-SEPARATION",
                "statement": (
                    "After any positive compiler, compare against matched "
                    "query/sample-limited classical access on rigid GI or code "
                    "equivalence instances."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Efficient subgroup reflections compile the polar.",
                "answer": (
                    "False generically: kernel phase pi is separated from the "
                    "natural bulk by Theta(M^-1/2)."
                ),
                "resolved": True,
            },
            {
                "challenge": "The tensor G QFT makes the double-coset transform scalar.",
                "answer": (
                    "False: diagonal invariant multiplicities exceed one already "
                    "for four standard factors."
                ),
                "resolved": True,
            },
            {
                "challenge": "Large invariant multiplicity proves computational hardness.",
                "answer": (
                    "False: partition-algebra or other structured transforms can "
                    "act on large multiplicity spaces succinctly."
                ),
                "resolved": True,
            },
            {
                "challenge": "The homogeneous-space reformulation is itself a detector.",
                "answer": (
                    "False: it isolates the exact matrix transform and preserves "
                    "all normalization and label-erasure debt."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_double_coset_finite_control_count": len(finite),
            "finite_control_failure_count": sum(
                not row.exact_double_coset_incidence_verified for row in finite
            ),
            "matrix_multiplicity_control_count": len(multiplicities),
            "matrix_multiplicity_failure_count": sum(
                row.scalar_gelfand_multiplicity_free for row in multiplicities
            ),
            "maximum_finite_diagonal_standard_multiplicity": max(
                row.exact_diagonal_invariant_multiplicity
                for row in multiplicities
            ),
            "tail_log2_standard_invariant_multiplicity_lower_bound": (
                scaling[-1].log2_identity_term_invariant_multiplicity_lower_bound
            ),
            "tail_generic_reflection_query_log2_lower_order": (
                scaling[-1].generic_reflection_phase_query_log2_lower_order
            ),
            "matrix_cosine_sine_transform_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "double_coset_incidence_normal_form_proved": exact,
            "row_polar_is_subgroup_cosine_sine_alignment": exact,
            "efficient_subgroup_reflections_available": True,
            "generic_alternating_reflection_polar_polynomial": False,
            "scalar_spherical_transform_sufficient": False,
            "matrix_cosine_sine_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "natural_problem_speedup_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The row polar is now an exact two-subgroup matrix Cosine-Sine "
                "problem, but neither its matrix multiplicity transform nor a "
                "normalization-preserving fast-forward is compiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Converted the hidden-involution row frame into an exact double-"
            "coset overlap between diagonal and source stabilizers, exposing "
            "the required matrix Cosine-Sine transform and preserving the "
            "sqrt(M) generic phase barrier."
        ),
        falsifiers_triggered=[
            "The row-frame operator is not an unstructured list of orbit representatives; it is one homogeneous double-coset incidence operator.",
            "Efficient preparation of both subgroup projectors does not remove the natural principal-angle scale.",
            "A scalar perfect-matching spherical transform cannot represent the growing diagonal tensor multiplicities.",
            "The remaining positive escape must be a direct matrix transform or structured fast-forward, not generic QSVT under a new name.",
        ],
    )


def write_double_coset_polar_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_double_coset_polar_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_double_coset_polar_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
