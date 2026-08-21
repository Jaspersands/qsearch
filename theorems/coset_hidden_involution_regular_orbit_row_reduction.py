"""Regular-orbit row normal form after trimmed source canonicalization.

On the trimmed source subspace, the canonical fiber is
``C[K] tensor C[O]`` as a ``K`` module.  Induction to the full candidate orbit
removes the stabilizer layer exactly:

    Ind_K^G(C[K] tensor C[O])
      ~= C[G] tensor C[O],                              (1)

via ``g tensor k -> gk`` (using the left-regular transporter convention).
Thus neither generic hyperoctahedral Clebsch--Gordan fusion nor a separate
``S_n down K`` multiplicity basis is required on the good source mass.

For a canonical orbit representative vector ``v_o``, synthesis has the exact
covariant row form

    W |g,o> = U_g |v_o>.                               (2)

Its source Gram is matrix-valued group convolution:

    <g,o|W^*W|g',o'> = <v_o|U_(g^-1 g')|v_o'>.          (3)

The ``G`` QFT diagonalizes the regular coordinate and gives
``direct_sum_nu I_(V_nu) tensor R_nu``.  All unresolved structure is now in
the orbit-representative row-frame operators ``R_nu``.  An efficient QFT does
not erase ``g,o`` or polar-normalize these rows.

An exact regular ``S_3`` control on free two-copy plus-coset orbits verifies
the intertwiner and convolution identities.  It also has nonzero cross-orbit
blocks and a proper source kernel, proving that canonicalization is not itself
the polar.

This is a representation reduction, not a hidden-involution algorithm.  A
useful next result must compile or falsify the source-specific row polar on
the high-mass orbit representatives, including physical label erasure and a
matched classical baseline.
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
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hyperoctahedral_trimmed_orbit_canonicalizer import (
    canonicalizer_scaling_record,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_regular_orbit_row_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-REGULAR-ORBIT-ROW-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RegularOrbitRowFiniteControl:
    group_order: int
    stabilizer_order: int
    one_copy_plus_basis_dimension: int
    copy_count: int
    free_fiber_tuple_count: int
    free_fiber_orbit_count: int
    regular_source_dimension: int
    physical_dimension: int
    synthesis_rank: int
    source_kernel_dimension: int
    maximum_column_norm_residual: float
    maximum_covariance_residual: float
    maximum_group_convolution_residual: float
    nonzero_cross_orbit_block_count: int
    maximum_cross_orbit_overlap: float
    minimum_positive_gram_eigenvalue: float
    maximum_gram_eigenvalue: float
    canonicalization_alone_is_polar: bool
    exact_regular_orbit_row_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class RegularOrbitRowScalingRecord:
    half_degree: int
    degree: int
    copy_count: int
    trimmed_alternative_success_lower_bound: float
    induced_regular_source_normal_form_available: bool
    symmetric_group_qft_available: bool
    hyperoctahedral_cg_required_on_trimmed_source: bool
    orbit_representative_row_frame_formalized: bool
    orbit_representative_row_polar_compiled: bool
    physical_label_erasure_compiled: bool
    status: str


@dataclass(frozen=True)
class RegularOrbitRowTheorem:
    induction_identity: str
    explicit_coordinate_map: str
    synthesis_row_form: str
    gram_convolution: str
    fourier_normal_form: str
    removed_obligations: str
    remaining_operator: str
    scope_limit: str
    induced_regular_identity_proved: bool
    regular_source_basis_compiled_on_trimmed_mass: bool
    hyperoctahedral_cg_required_on_trimmed_mass: bool
    matrix_group_convolution_reduction_proved: bool
    orbit_representative_row_polar_compiled: bool
    physical_label_erasure_compiled: bool
    hidden_involution_algorithm_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RegularOrbitRowReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_control: RegularOrbitRowFiniteControl
    scaling_records: list[RegularOrbitRowScalingRecord]
    theorem: RegularOrbitRowTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _conjugate(
    element: Permutation,
    value: Permutation,
) -> Permutation:
    return compose_permutations(
        compose_permutations(element, value), inverse_permutation(element)
    )


def _conjugation_matrix(
    group: tuple[Permutation, ...],
    element: Permutation,
) -> np.ndarray:
    index = {value: offset for offset, value in enumerate(group)}
    matrix = np.zeros((len(group), len(group)), dtype=complex)
    for column, value in enumerate(group):
        matrix[index[_conjugate(element, value)], column] = 1.0
    return matrix


def _canonical_coset(
    representative: Permutation,
    hidden: Permutation,
) -> Permutation:
    return min(representative, compose_permutations(representative, hidden))


def _act_on_coset_tuple(
    source_tuple: tuple[Permutation, ...],
    element: Permutation,
    hidden: Permutation,
) -> tuple[Permutation, ...]:
    return tuple(
        _canonical_coset(_conjugate(element, representative), hidden)
        for representative in source_tuple
    )


def _s3_free_fiber_orbit_representatives(
    copy_count: int,
) -> tuple[tuple[Permutation, ...], ...]:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    group = symmetric_group(3)
    hidden = involution_conjugacy_class(3, 1)[0]
    stabilizer = tuple(
        element for element in group if _conjugate(element, hidden) == hidden
    )
    cosets = tuple(
        sorted({_canonical_coset(element, hidden) for element in group})
    )
    free = tuple(
        source_tuple
        for source_tuple in itertools.product(cosets, repeat=copy_count)
        if sum(
            _act_on_coset_tuple(source_tuple, element, hidden) == source_tuple
            for element in stabilizer
        )
        == 1
    )
    unseen = set(free)
    representatives = []
    while unseen:
        representative = min(unseen)
        orbit = {
            _act_on_coset_tuple(representative, element, hidden)
            for element in stabilizer
        }
        representatives.append(min(orbit))
        unseen.difference_update(orbit)
    return tuple(representatives)


def audit_regular_orbit_row_reduction(
    copy_count: int = 2,
    *,
    tolerance: float = 1e-9,
) -> RegularOrbitRowFiniteControl:
    if copy_count < 1 or copy_count > 3:
        raise ValueError("S_3 finite control supports copy_count in [1,3]")
    group = symmetric_group(3)
    group_index = {element: offset for offset, element in enumerate(group)}
    hidden = involution_conjugacy_class(3, 1)[0]
    stabilizer = tuple(
        element for element in group if _conjugate(element, hidden) == hidden
    )
    cosets = tuple(
        sorted({_canonical_coset(element, hidden) for element in group})
    )
    orbit_representatives = _s3_free_fiber_orbit_representatives(copy_count)
    physical_actions = {
        element: _conjugation_matrix(group, element)
        for element in group
    }
    for copies in range(1, copy_count):
        physical_actions = {
            element: np.kron(
                physical_actions[element],
                _conjugation_matrix(group, element),
            )
            for element in group
        }

    def plus_vector(representative: Permutation) -> np.ndarray:
        vector = np.zeros(len(group), dtype=complex)
        vector[group_index[representative]] = 1.0 / math.sqrt(2.0)
        vector[
            group_index[compose_permutations(representative, hidden)]
        ] = 1.0 / math.sqrt(2.0)
        return vector

    representative_vectors = []
    for source_tuple in orbit_representatives:
        vector = plus_vector(source_tuple[0])
        for representative in source_tuple[1:]:
            vector = np.kron(vector, plus_vector(representative))
        representative_vectors.append(vector)

    columns = [
        physical_actions[element] @ vector
        for vector in representative_vectors
        for element in group
    ]
    synthesis = np.column_stack(columns)
    gram = synthesis.conj().T @ synthesis
    source_dimension = len(columns)
    physical_dimension = len(group) ** copy_count
    column_norm = max(
        abs(float(np.vdot(column, column).real) - 1.0) for column in columns
    )

    covariance_residual = 0.0
    for acting in group:
        regular = np.zeros((source_dimension, source_dimension), dtype=complex)
        for orbit_index in range(len(orbit_representatives)):
            offset = orbit_index * len(group)
            for group_element in group:
                source = offset + group_index[group_element]
                target_element = compose_permutations(acting, group_element)
                target = offset + group_index[target_element]
                regular[target, source] = 1.0
        covariance_residual = max(
            covariance_residual,
            float(
                np.linalg.norm(
                    physical_actions[acting] @ synthesis
                    - synthesis @ regular,
                    ord=2,
                )
            ),
        )

    convolution_residual = 0.0
    nonzero_cross_blocks = 0
    maximum_cross = 0.0
    for left_index, left_vector in enumerate(representative_vectors):
        for right_index, right_vector in enumerate(representative_vectors):
            block = gram[
                left_index * len(group) : (left_index + 1) * len(group),
                right_index * len(group) : (right_index + 1) * len(group),
            ]
            predicted = np.zeros_like(block)
            for left_group in group:
                for right_group in group:
                    relative = compose_permutations(
                        inverse_permutation(left_group), right_group
                    )
                    predicted[
                        group_index[left_group], group_index[right_group]
                    ] = np.vdot(
                        left_vector,
                        physical_actions[relative] @ right_vector,
                    )
            convolution_residual = max(
                convolution_residual,
                float(np.linalg.norm(block - predicted, ord=2)),
            )
            if left_index != right_index:
                cross_maximum = float(np.max(np.abs(block)))
                maximum_cross = max(maximum_cross, cross_maximum)
                nonzero_cross_blocks += cross_maximum > tolerance

    eigenvalues = np.linalg.eigvalsh((gram + gram.conj().T) / 2.0)
    positive = eigenvalues[eigenvalues > tolerance]
    rank = int(len(positive))
    free_tuple_count = len(orbit_representatives) * len(stabilizer)
    verified = bool(
        free_tuple_count
        == sum(
            sum(
                _act_on_coset_tuple(source_tuple, element, hidden)
                == source_tuple
                for element in stabilizer
            )
            == 1
            for source_tuple in itertools.product(cosets, repeat=copy_count)
        )
        and column_norm <= 100 * tolerance
        and covariance_residual <= 100 * tolerance
        and convolution_residual <= 100 * tolerance
        and nonzero_cross_blocks > 0
        and rank < source_dimension
    )
    return RegularOrbitRowFiniteControl(
        group_order=len(group),
        stabilizer_order=len(stabilizer),
        one_copy_plus_basis_dimension=len(cosets),
        copy_count=copy_count,
        free_fiber_tuple_count=free_tuple_count,
        free_fiber_orbit_count=len(orbit_representatives),
        regular_source_dimension=source_dimension,
        physical_dimension=physical_dimension,
        synthesis_rank=rank,
        source_kernel_dimension=source_dimension - rank,
        maximum_column_norm_residual=column_norm,
        maximum_covariance_residual=covariance_residual,
        maximum_group_convolution_residual=convolution_residual,
        nonzero_cross_orbit_block_count=nonzero_cross_blocks,
        maximum_cross_orbit_overlap=maximum_cross,
        minimum_positive_gram_eigenvalue=float(np.min(positive)),
        maximum_gram_eigenvalue=float(np.max(positive)),
        canonicalization_alone_is_polar=False,
        exact_regular_orbit_row_reduction_verified=verified,
        status=(
            "exact-regular-orbit-row-normal-form-verified"
            if verified
            else "regular-orbit-row-control-failure"
        ),
    )


def regular_orbit_row_scaling_record(
    half_degree: int,
) -> RegularOrbitRowScalingRecord:
    canonicalizer = canonicalizer_scaling_record(half_degree)
    return RegularOrbitRowScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        copy_count=canonicalizer.copy_count,
        trimmed_alternative_success_lower_bound=(
            canonicalizer.trimmed_alternative_success_lower_bound
        ),
        induced_regular_source_normal_form_available=True,
        symmetric_group_qft_available=True,
        hyperoctahedral_cg_required_on_trimmed_source=False,
        orbit_representative_row_frame_formalized=True,
        orbit_representative_row_polar_compiled=False,
        physical_label_erasure_compiled=False,
        status="regular-source-row-frame-formalized-row-polar-open",
    )


def build_regular_orbit_row_report(
    *,
    scaling_half_degrees: tuple[int, ...] = (3, 4, 8, 16, 32, 64, 128),
) -> RegularOrbitRowReport:
    finite = audit_regular_orbit_row_reduction(2)
    scaling = [
        regular_orbit_row_scaling_record(m) for m in scaling_half_degrees
    ]
    verified = finite.exact_regular_orbit_row_reduction_verified and all(
        row.induced_regular_source_normal_form_available
        and row.symmetric_group_qft_available
        and not row.hyperoctahedral_cg_required_on_trimmed_source
        and row.orbit_representative_row_frame_formalized
        and not row.orbit_representative_row_polar_compiled
        for row in scaling
    )
    theorem = RegularOrbitRowTheorem(
        induction_identity=(
            "Ind_K^G(C[K] tensor C[O]) is C[G] tensor C[O]."
        ),
        explicit_coordinate_map=(
            "After inverting the canonicalizer transporter to a left-regular "
            "K coordinate, g tensor k maps to the full group coordinate gk."
        ),
        synthesis_row_form="W|g,o>=U_g|v_o> for canonical representative v_o.",
        gram_convolution=(
            "The (o,o') Gram block is the G convolution kernel "
            "<v_o|U_(g^-1g')|v_o'>."
        ),
        fourier_normal_form=(
            "The G QFT diagonalizes the regular coordinate, leaving identity on "
            "carriers and a source-specific row-frame operator per irrep."
        ),
        removed_obligations=(
            "Generic hyperoctahedral CG and a separate S_n-to-K source "
            "multiplicity basis are unnecessary on trimmed good mass."
        ),
        remaining_operator=(
            "Compile the polar/support of the orbit-representative row frame and "
            "erase regular/orbit labels into the physical state."
        ),
        scope_limit=(
            "No row polar, label erasure, decoder, classical separation, or "
            "hidden-involution algorithm is supplied."
        ),
        induced_regular_identity_proved=True,
        regular_source_basis_compiled_on_trimmed_mass=True,
        hyperoctahedral_cg_required_on_trimmed_mass=False,
        matrix_group_convolution_reduction_proved=True,
        orbit_representative_row_polar_compiled=False,
        physical_label_erasure_compiled=False,
        hidden_involution_algorithm_constructed=False,
        theorem_verified=verified,
        status=(
            "regular-orbit-row-frame-reduced-physical-row-polar-open"
            if verified
            else "regular-orbit-row-reduction-control-failure"
        ),
    )
    return RegularOrbitRowReport(
        created_at=utc_now(),
        theorem_contract={
            "source_subspace": (
                "The free/transitively-seeded trimmed source on which the "
                "canonical representative/transporter map is reversible."
            ),
            "induction": (
                "Candidate branch induction from K=C_2 wr S_m to G=S_(2m)."
            ),
            "physical_action": "Diagonal conjugation on k regular registers.",
            "outside_scope": (
                "Bad trimmed mass, row-frame polar implementation, physical "
                "output decoding, and natural classical complexity."
            ),
        },
        finite_control=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ORBIT-ROW-SUCCINCTNESS",
                "statement": (
                    "Represent canonical orbit-copy labels and their overlap "
                    "kernels without enumerating exponentially many representatives."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ORBIT-ROW-POLAR",
                "statement": (
                    "Compile the row-frame support/polar at constant retained "
                    "alternative mass and inverse-polynomial error."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ORBIT-LABEL-ERASURE",
                "statement": (
                    "Erase the regular group and orbit-copy labels into physical "
                    "rows without sqrt(M) amplification."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The high-mass source still needs generic K fusion.",
                "answer": (
                    "False after canonicalization: regular K induction fuses "
                    "exactly into a regular G coordinate."
                ),
                "resolved": True,
            },
            {
                "challenge": "A regular G source makes synthesis unitary.",
                "answer": (
                    "False: different orbit copies have nonzero cross-Gram blocks, "
                    "and even the exact S_3 control has a proper source kernel."
                ),
                "resolved": True,
            },
            {
                "challenge": "The G QFT implements the row polar.",
                "answer": (
                    "False. It removes carrier convolution but leaves the full "
                    "orbit-copy row operator inside multiplicity."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_regular_orbit_control_count": 1,
            "finite_control_failure_count": int(not finite.exact_regular_orbit_row_reduction_verified),
            "induced_regular_source_theorem_count": 1,
            "hyperoctahedral_cg_required_count": 0,
            "matrix_group_convolution_reduction_count": 1,
            "finite_nonzero_cross_orbit_block_count": finite.nonzero_cross_orbit_block_count,
            "orbit_representative_row_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "trimmed_source_induces_to_regular_G_copies": verified,
            "generic_hyperoctahedral_cg_required_on_trimmed_source": False,
            "orbit_representative_row_frame_formalized": verified,
            "orbit_representative_row_polar_compiled": False,
            "physical_regular_and_orbit_labels_erased": False,
            "full_orbit_synthesis_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The source covariance and multiplicity basis reduce to regular "
                "G copies, but their coupled physical row-frame polar and label "
                "erasure remain the unresolved algorithmic operator."
            ),
        },
        status=theorem.status,
        summary=(
            "Fused the trimmed regular K source and candidate branch into exact "
            "regular S_n copies, derived the matrix group-convolution row frame, "
            "and removed generic hyperoctahedral fusion from the active path while "
            "isolating orbit-row polar synthesis and label erasure."
        ),
        falsifiers_triggered=[
            "Generic hyperoctahedral Clebsch-Gordan fusion is not required on the canonicalized high-mass source.",
            "Regular source covariance does not make the physical synthesis isometric across orbit copies.",
            "The symmetric-group QFT does not resolve orbit-representative row orientation or polar weights.",
        ],
    )


def write_regular_orbit_row_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_regular_orbit_row_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_regular_orbit_row_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
