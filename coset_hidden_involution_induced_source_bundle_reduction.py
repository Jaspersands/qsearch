"""Induced-source bundle reduction for hidden-involution orbit synthesis.

Let ``P_0`` be the projector for a canonical hidden involution, let
``K=Stab(P_0)``, and put ``R=ran(P_0)``.  The branch-labeled source of the orbit
synthesis map is not an arbitrary collection of locally glued ranges.  It is
the associated homogeneous bundle

    E = direct_sum_(xK in G/K) ran(U_x P_0 U_x^*)
      ~= Ind_K^G R.                                      (1)

The synthesis map ``S:E->H``, ``S((v_x))=sum_x v_x``, is a ``G`` intertwiner.
Frobenius reciprocity therefore gives

    E ~= direct_sum_nu V_nu tensor Hom_K(V_nu,R),
    S  = direct_sum_nu I_(V_nu) tensor S_nu.             (2)

This absorbs branch permutation and stabilizer cocycles exactly.  It also
shows that gluing canonical pair-polar edges is the wrong global primitive:
on the minimal regular ``S_3`` chart, the stabilizer cocycle on ``R`` has
spectrum ``{1,1,-1}``, while the canonical pair-polar triangle has spectrum
``{1,-1,-1}``.

For ``k`` copies of that chart, the induced source multiplicities are

    mult_E(1)   = (3^k+1)/2,
    mult_E(sgn) = (3^k-1)/2,
    mult_E(std) = 3^k.                                  (3)

The synthesis is injective on the trivial and sign multiplicities and has
standard-block multiplicity rank ``3^k-(k+1)``.  Its entire kernel is exactly
``k+1`` standard copies, agreeing with the defect-weight Gram theorem.

When coherent coset factorization, uniform ``K`` preparation, controlled
``K`` action on ``R``, and a ``G`` QFT are efficient, the induced source can
be Fourier organized without resolving pair-polar paths.  For the symmetric/
hyperoctahedral pair those primitives are available on a branch-labeled
source.  This does not implement the physical-to-source analysis map, invert
the multiplicity intertwiners ``S_nu``, or erase the exponentially large
candidate label at polynomial normalization.  No hidden-involution algorithm
or speedup follows.
"""

from __future__ import annotations

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
    involution_transposition_count,
    right_regular_matrix,
    symmetric_group,
)
from coset_hidden_involution_pair_polar_holonomy_no_go import (
    audit_pair_polar_holonomy,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_induced_source_bundle_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-INDUCED-SOURCE-BUNDLE-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class InducedSourceFiniteControl:
    copy_count: int
    group_order: int
    stabilizer_order: int
    branch_count: int
    fiber_dimension: int
    source_dimension: int
    maximum_synthesis_equivariance_residual: float
    observed_source_character_identity: float
    observed_source_character_transposition: float
    observed_source_character_three_cycle: float
    predicted_source_character_identity: int
    predicted_source_character_transposition: int
    predicted_source_character_three_cycle: int
    observed_trivial_source_multiplicity: int
    observed_sign_source_multiplicity: int
    observed_standard_source_multiplicity: int
    predicted_trivial_source_multiplicity: int
    predicted_sign_source_multiplicity: int
    predicted_standard_source_multiplicity: int
    observed_trivial_synthesis_multiplicity_rank: int
    observed_sign_synthesis_multiplicity_rank: int
    observed_standard_synthesis_multiplicity_rank: int
    predicted_trivial_synthesis_multiplicity_rank: int
    predicted_sign_synthesis_multiplicity_rank: int
    predicted_standard_synthesis_multiplicity_rank: int
    observed_total_synthesis_rank: int
    predicted_total_synthesis_rank: int
    induced_source_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class PairConnectionCocycleControl:
    fiber_dimension: int
    stabilizer_cocycle_spectrum: tuple[int, int, int]
    canonical_pair_holonomy_spectrum: tuple[int, int, int]
    spectra_equal: bool
    pair_polar_connection_is_induced_bundle_cocycle: bool
    control_verified: bool
    status: str


@dataclass(frozen=True)
class InducedSourceScalingRecord:
    copy_count: int
    source_dimension_decimal: str
    trivial_source_multiplicity_decimal: str
    sign_source_multiplicity_decimal: str
    standard_source_multiplicity_decimal: str
    standard_synthesis_kernel_multiplicity: int
    standard_synthesis_rank_decimal: str
    total_synthesis_rank_decimal: str
    branch_covariance_fourier_transform_available: bool
    physical_to_source_analysis_compiled: bool
    multiplicity_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class InducedSourceBundleTheorem:
    associated_bundle_identity: str
    synthesis_equivariance: str
    frobenius_decomposition: str
    pair_connection_distinction: str
    s3_source_multiplicities: str
    s3_synthesis_ranks: str
    operational_branch_transform: str
    scope_limit: str
    induced_source_identity_proved: bool
    frobenius_block_reduction_proved: bool
    pair_polar_gluing_required_for_global_covariance: bool
    branch_covariance_fourier_transform_constructed: bool
    physical_to_source_analysis_compiled: bool
    multiplicity_support_polar_compiled: bool
    full_orbit_synthesis_polar_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class InducedSourceBundleReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[InducedSourceFiniteControl]
    pair_connection_control: PairConnectionCocycleControl
    scaling_records: list[InducedSourceScalingRecord]
    theorem: InducedSourceBundleTheorem
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


def _tensor_power(operator: np.ndarray, copy_count: int) -> np.ndarray:
    output = operator
    for _ in range(copy_count - 1):
        output = np.kron(output, operator)
    return output


def s3_induced_source_multiplicities(
    copy_count: int,
) -> tuple[int, int, int]:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    fiber = 3**copy_count
    return (fiber + 1) // 2, (fiber - 1) // 2, fiber


def s3_synthesis_multiplicity_ranks(
    copy_count: int,
) -> tuple[int, int, int]:
    trivial, sign, standard = s3_induced_source_multiplicities(copy_count)
    return trivial, sign, standard - (copy_count + 1)


def _s3_character(irrep: str, element: Permutation) -> int:
    if irrep == "trivial":
        return 1
    transpositions = involution_transposition_count(element)
    if irrep == "sign":
        return -1 if transpositions == 1 else 1
    if irrep == "standard":
        if element == tuple(range(3)):
            return 2
        return 0 if transpositions == 1 else -1
    raise ValueError("unknown S_3 irrep")


def audit_s3_induced_source(
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> InducedSourceFiniteControl:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    group = symmetric_group(3)
    candidates = involution_conjugacy_class(3, 1)
    candidate_index = {
        candidate: offset for offset, candidate in enumerate(candidates)
    }
    conjugation = {
        element: _conjugation_matrix(group, element) for element in group
    }
    bases: list[np.ndarray] = []
    for candidate in candidates:
        projector = (
            np.eye(len(group)) + right_regular_matrix(3, candidate)
        ) / 2.0
        values, vectors = np.linalg.eigh(projector)
        bases.append(_tensor_power(vectors[:, values > 0.5], copy_count))
    synthesis = np.concatenate(bases, axis=1)
    fiber_dimension = 3**copy_count
    source_dimension = 3 * fiber_dimension

    source_actions: dict[Permutation, np.ndarray] = {}
    physical_actions: dict[Permutation, np.ndarray] = {}
    maximum_equivariance = 0.0
    for element in group:
        physical = _tensor_power(conjugation[element], copy_count)
        physical_actions[element] = physical
        source = np.zeros(
            (source_dimension, source_dimension), dtype=complex
        )
        for left, candidate in enumerate(candidates):
            image = candidate_index[_conjugate(element, candidate)]
            source[
                image * fiber_dimension : (image + 1) * fiber_dimension,
                left * fiber_dimension : (left + 1) * fiber_dimension,
            ] = bases[image].conj().T @ physical @ bases[left]
        source_actions[element] = source
        maximum_equivariance = max(
            maximum_equivariance,
            float(np.linalg.norm(physical @ synthesis - synthesis @ source, ord=2)),
        )

    identity = tuple(range(3))
    transposition = candidates[0]
    three_cycle = next(
        element
        for element in group
        if element != identity
        and involution_transposition_count(element) is None
    )
    observed_characters = tuple(
        float(np.trace(source_actions[element]).real)
        for element in (identity, transposition, three_cycle)
    )
    predicted_characters = (source_dimension, 1, 0)

    observed_multiplicities = []
    observed_ranks = []
    irrep_dimensions = (1, 1, 2)
    for irrep, dimension in zip(
        ("trivial", "sign", "standard"), irrep_dimensions
    ):
        multiplicity = round(
            sum(
                _s3_character(irrep, element)
                * np.trace(source_actions[element]).real
                for element in group
            )
            / len(group)
        )
        observed_multiplicities.append(int(multiplicity))
        physical_projector = sum(
            _s3_character(irrep, element) * physical_actions[element]
            for element in group
        ) * (dimension / len(group))
        image_rank = int(
            np.linalg.matrix_rank(physical_projector @ synthesis, tol=tolerance)
        )
        observed_ranks.append(image_rank // dimension)

    predicted_multiplicities = s3_induced_source_multiplicities(copy_count)
    predicted_ranks = s3_synthesis_multiplicity_ranks(copy_count)
    observed_total_rank = int(np.linalg.matrix_rank(synthesis, tol=tolerance))
    predicted_total_rank = (
        predicted_ranks[0] + predicted_ranks[1] + 2 * predicted_ranks[2]
    )
    verified = bool(
        maximum_equivariance <= 100 * tolerance
        and all(
            abs(observed - predicted) <= 100 * tolerance
            for observed, predicted in zip(
                observed_characters, predicted_characters
            )
        )
        and tuple(observed_multiplicities) == predicted_multiplicities
        and tuple(observed_ranks) == predicted_ranks
        and observed_total_rank == predicted_total_rank
    )
    return InducedSourceFiniteControl(
        copy_count=copy_count,
        group_order=len(group),
        stabilizer_order=2,
        branch_count=3,
        fiber_dimension=fiber_dimension,
        source_dimension=source_dimension,
        maximum_synthesis_equivariance_residual=maximum_equivariance,
        observed_source_character_identity=observed_characters[0],
        observed_source_character_transposition=observed_characters[1],
        observed_source_character_three_cycle=observed_characters[2],
        predicted_source_character_identity=predicted_characters[0],
        predicted_source_character_transposition=predicted_characters[1],
        predicted_source_character_three_cycle=predicted_characters[2],
        observed_trivial_source_multiplicity=observed_multiplicities[0],
        observed_sign_source_multiplicity=observed_multiplicities[1],
        observed_standard_source_multiplicity=observed_multiplicities[2],
        predicted_trivial_source_multiplicity=predicted_multiplicities[0],
        predicted_sign_source_multiplicity=predicted_multiplicities[1],
        predicted_standard_source_multiplicity=predicted_multiplicities[2],
        observed_trivial_synthesis_multiplicity_rank=observed_ranks[0],
        observed_sign_synthesis_multiplicity_rank=observed_ranks[1],
        observed_standard_synthesis_multiplicity_rank=observed_ranks[2],
        predicted_trivial_synthesis_multiplicity_rank=predicted_ranks[0],
        predicted_sign_synthesis_multiplicity_rank=predicted_ranks[1],
        predicted_standard_synthesis_multiplicity_rank=predicted_ranks[2],
        observed_total_synthesis_rank=observed_total_rank,
        predicted_total_synthesis_rank=predicted_total_rank,
        induced_source_normal_form_verified=verified,
        status=(
            "exact-induced-source-and-synthesis-blocks-verified"
            if verified
            else "induced-source-control-failure"
        ),
    )


def audit_pair_connection_cocycle_distinction(
    *,
    tolerance: float = 1e-9,
) -> PairConnectionCocycleControl:
    group = symmetric_group(3)
    base = involution_conjugacy_class(3, 1)[0]
    stabilizer_generator = base
    projector = (
        np.eye(len(group)) + right_regular_matrix(3, base)
    ) / 2.0
    values, vectors = np.linalg.eigh(projector)
    basis = vectors[:, values > 0.5]
    cocycle = basis.conj().T @ _conjugation_matrix(
        group, stabilizer_generator
    ) @ basis
    cocycle_values = tuple(
        sorted(int(round(value.real)) for value in np.linalg.eigvals(cocycle))
    )
    pair_control = audit_pair_polar_holonomy(tolerance=tolerance)
    pair_values = tuple(
        sorted(
            (1,) * pair_control.positive_holonomy_multiplicity
            + (-1,) * pair_control.negative_holonomy_multiplicity
        )
    )
    distinct = cocycle_values != pair_values
    verified = bool(
        cocycle_values == (-1, 1, 1)
        and pair_values == (-1, -1, 1)
        and distinct
        and pair_control.nontrivial_holonomy_verified
    )
    return PairConnectionCocycleControl(
        fiber_dimension=3,
        stabilizer_cocycle_spectrum=cocycle_values,
        canonical_pair_holonomy_spectrum=pair_values,
        spectra_equal=not distinct,
        pair_polar_connection_is_induced_bundle_cocycle=False,
        control_verified=verified,
        status=(
            "pair-polar-connection-distinct-from-induced-cocycle"
            if verified
            else "connection-cocycle-control-failure"
        ),
    )


def induced_source_scaling_record(
    copy_count: int,
) -> InducedSourceScalingRecord:
    trivial, sign, standard = s3_induced_source_multiplicities(copy_count)
    _, _, standard_rank = s3_synthesis_multiplicity_ranks(copy_count)
    total_rank = trivial + sign + 2 * standard_rank
    return InducedSourceScalingRecord(
        copy_count=copy_count,
        source_dimension_decimal=str(3 ** (copy_count + 1)),
        trivial_source_multiplicity_decimal=str(trivial),
        sign_source_multiplicity_decimal=str(sign),
        standard_source_multiplicity_decimal=str(standard),
        standard_synthesis_kernel_multiplicity=copy_count + 1,
        standard_synthesis_rank_decimal=str(standard_rank),
        total_synthesis_rank_decimal=str(total_rank),
        branch_covariance_fourier_transform_available=True,
        physical_to_source_analysis_compiled=False,
        multiplicity_polar_compiled=False,
        status="branch-covariance-resolved-multiplicity-polar-open",
    )


def build_induced_source_bundle_report(
    *,
    finite_copy_counts: tuple[int, ...] = (1, 2, 3),
    scaling_copy_counts: tuple[int, ...] = (1, 2, 8, 32, 128),
) -> InducedSourceBundleReport:
    controls = [audit_s3_induced_source(k) for k in finite_copy_counts]
    connection = audit_pair_connection_cocycle_distinction()
    scaling = [induced_source_scaling_record(k) for k in scaling_copy_counts]
    verified = bool(
        all(row.induced_source_normal_form_verified for row in controls)
        and connection.control_verified
    )
    theorem = InducedSourceBundleTheorem(
        associated_bundle_identity=(
            "The orbit source direct sum is the associated bundle "
            "G times_K ran(P_0), equivalently Ind_K^G ran(P_0)."
        ),
        synthesis_equivariance=(
            "S((v_x))=sum_x v_x intertwines the induced source action with "
            "the physical G action."
        ),
        frobenius_decomposition=(
            "E=direct_sum_nu V_nu tensor Hom_K(V_nu,R), and S is identity on "
            "V_nu tensored with one multiplicity intertwiner S_nu."
        ),
        pair_connection_distinction=(
            "The canonical pair-polar connection is not the associated-bundle "
            "stabilizer cocycle: their one-copy S_3 spectra differ."
        ),
        s3_source_multiplicities=(
            "The trivial, sign, and standard multiplicities are respectively "
            "(3^k+1)/2, (3^k-1)/2, and 3^k."
        ),
        s3_synthesis_ranks=(
            "Trivial and sign blocks are injective; the standard multiplicity "
            "rank is 3^k-(k+1), so the kernel is k+1 standard copies."
        ),
        operational_branch_transform=(
            "Coset factorization, uniform K preparation, controlled K action, "
            "and the G QFT organize a branch-labeled induced source coherently."
        ),
        scope_limit=(
            "The transform begins with a branch-labeled source. It neither lifts "
            "an unknown physical state into that source nor inverts S_nu."
        ),
        induced_source_identity_proved=True,
        frobenius_block_reduction_proved=True,
        pair_polar_gluing_required_for_global_covariance=False,
        branch_covariance_fourier_transform_constructed=True,
        physical_to_source_analysis_compiled=False,
        multiplicity_support_polar_compiled=False,
        full_orbit_synthesis_polar_compiled=False,
        theorem_verified=verified,
        status=(
            "induced-branch-covariance-resolved-multiplicity-polar-open"
            if verified
            else "induced-source-bundle-control-failure"
        ),
    )
    return InducedSourceBundleReport(
        created_at=utc_now(),
        theorem_contract={
            "orbit": "A finite G orbit of a projector P_0 with stabilizer K.",
            "source": (
                "The direct sum of candidate ranges with its explicit branch label."
            ),
            "constructive_assumptions": (
                "Efficient coherent G/K factorization, uniform K preparation, "
                "controlled representation action, and G QFT."
            ),
            "outside_scope": (
                "Physical-to-source lifting, multiplicity support/polar, full-"
                "class normalization, dequantization, and hidden-element recovery."
            ),
        },
        finite_controls=controls,
        pair_connection_control=connection,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-INDUCED-MULTIPLICITY-BASIS",
                "statement": (
                    "Compile a uniform basis for Hom_K(V_nu,R) and the natural "
                    "multiplicity intertwiner S_nu in the k-copy S_n family."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-PHYSICAL-SOURCE-LIFT",
                "statement": (
                    "Apply the branch-source analysis map to physical input "
                    "without sqrt(M) amplification or equivalent normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-INDUCED-POLAR",
                "statement": (
                    "Compile the support/polar of every naturally occupied S_nu "
                    "with polynomial precision and retained alternative mass."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Pair-polar paths must be globally glued first.",
                "answer": (
                    "False for covariance organization: the induced bundle and "
                    "G Fourier transform absorb branch permutation/cocycles directly."
                ),
                "resolved": True,
            },
            {
                "challenge": "Canonical pair holonomy is the stabilizer cocycle.",
                "answer": (
                    "False already on regular S_3: spectra {1,-1,-1} and "
                    "{1,1,-1} differ."
                ),
                "resolved": True,
            },
            {
                "challenge": "Induced-source Fourier organization compiles the PGM polar.",
                "answer": (
                    "False. It exposes the multiplicity intertwiners but does not "
                    "invert, support-project, or physically access them."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_induced_source_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.induced_source_normal_form_verified for row in controls
            ),
            "pair_connection_cocycle_distinction_count": int(
                connection.control_verified
            ),
            "frobenius_block_reduction_theorem_count": 1,
            "branch_covariance_fourier_transform_count": 1,
            "physical_to_source_analysis_compiler_count": 0,
            "multiplicity_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orbit_source_is_induced_bundle": verified,
            "global_covariance_requires_pair_polar_gluing": False,
            "pair_polar_holonomy_equals_stabilizer_cocycle": False,
            "branch_labeled_induced_fourier_transform_available": verified,
            "physical_to_branch_source_lift_compiled": False,
            "uniform_multiplicity_support_projector_constructed": False,
            "full_orbit_synthesis_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Induction resolves branch covariance without pairwise gluing, "
                "but the source-specific multiplicity intertwiners and the costly "
                "physical-to-source normalization remain uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Identified the full orbit source as an induced homogeneous bundle, "
            "separated canonical pair holonomy from the stabilizer cocycle, and "
            "reduced global synthesis exactly to source-specific multiplicity "
            "intertwiners rather than a local chart-gluing problem."
        ),
        falsifiers_triggered=[
            "Canonical pair-polar transport is not the natural induced-bundle cocycle.",
            "Global branch covariance does not require pathwise pair-polar gluing.",
            "An efficient branch-labeled induced Fourier transform does not imply an efficient physical support measurement.",
        ],
    )


def write_induced_source_bundle_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_induced_source_bundle_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_induced_source_bundle_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
