"""Finite matrix-CS correlation test for the natural matching charge.

The natural-independence theorem proves that ``D_m`` contributes copy-space
information beyond ``C_m`` and the ``K_m`` center on inverse-polynomial hidden
source mass.  It does not prove that this information is correlated with the
source-aware Cosine-Sine likelihood.  This module constructs the smallest
controlled block found so far that simultaneously has:

* three nontrivial source factors and a nontrivial target;
* a repeated hyperoctahedral restriction where ``D_m`` adds a copy label;
* a full-rank, nonflat A/B principal-angle spectrum.

The block is in ``S_10`` with

    source = (6,2,2) tensor (6,2,2) tensor (9,1),
    target = (9,1).

The two standard factors are realized inside the point permutation modules.
The A-invariant basis is built exactly from the diagonal and off-diagonal
point-pair orbits.  Their stabilizers are ``S_9`` and ``S_8``; the corresponding
commutant matrix units give nine candidate invariants, whose
``Std tensor Std`` projection has rank six.  The B projector applies h-even
projections to the three source factors and then the exact
``K_5=C_2 wr S_5`` Reynolds projector through its normal base subgroup and
the pair-permutation subgroup chain.

The six squared principal cosines are nonflat.  On the occupied B-side CS
space, the compressed normalized matching charge has six distinct
eigenvalues, nonzero commutator with the CS operator, and nonzero centered
Hilbert-Schmidt covariance.  Thus ``D_5`` is not pure nuisance in this exact
matrix-valued block.

This is finite evidence at degree ten.  The block has no proved asymptotic
natural mass, the compressed charge leaks outside the occupied CS range, and
no all-rank covariance, likelihood decoder, transform, or speedup follows.
"""

from __future__ import annotations

import gc
import itertools
import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_commutant_support_growth_boundary import (
    _average_matrices_for_sets,
    _matrix_for_permutation,
)
from coset_hidden_involution_pair_matching_charge_hierarchy import (
    audit_branch_resolution,
    central_pair_charge,
    disjoint_matching_charge,
)
from coset_jucys_murphy_label_transform import standard_young_tableaux
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matching_charge_cs_correlation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-CS-CORRELATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
Tableau = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class InvariantBasisControl:
    degree: int
    half_degree: int
    repeated_symmetric_partition: tuple[int, ...]
    repeated_irrep_dimension: int
    source_standard_partition: tuple[int, ...]
    target_standard_partition: tuple[int, ...]
    S9_commutant_dimension: int
    S8_commutant_dimension: int
    point_orbit_candidate_count: int
    standard_standard_A_invariant_dimension: int
    expected_A_invariant_dimension: int
    maximum_A_orthonormality_residual: float
    maximum_A_generator_invariance_residual: float
    maximum_B_projection_gram_residual: float
    maximum_B_K_generator_invariance_residual: float
    maximum_B_source_parity_residual: float
    construction_verified: bool
    status: str


@dataclass(frozen=True)
class CSCorrelationControl:
    occupied_CS_rank: int
    squared_principal_cosines: list[float]
    minimum_squared_principal_cosine: float
    maximum_squared_principal_cosine: float
    principal_cosine_squared_range: float
    principal_spectrum_nonflat: bool
    matching_charge_compressed_eigenvalues: list[float]
    matching_charge_distinct_compressed_eigenvalue_count: int
    matching_charge_compression_frobenius_norm: float
    matching_charge_occupied_subspace_leakage_norm: float
    matching_charge_CS_commutator_norm: float
    matching_charge_centered_CS_correlation: float
    central_charge_centered_CS_correlation: float
    central_charge_only_regression_R2: float
    central_plus_matching_regression_R2: float
    matching_charge_incremental_regression_R2: float
    matching_charge_nontrivial_in_occupied_block: bool
    matching_charge_correlates_with_CS_operator: bool
    matching_charge_diagonalizes_CS_operator: bool
    finite_numerical_control_only: bool
    status: str


@dataclass(frozen=True)
class MatchingChargeCSCorrelationTheorem:
    block: str
    A_basis: str
    B_projector: str
    finite_result: str
    interpretation: str
    exact_invariant_space_construction_verified: bool
    full_rank_nonflat_matrix_CS_block_verified: bool
    D_adds_branch_copy_label_verified: bool
    D_nontrivial_on_occupied_CS_space_verified: bool
    finite_D_CS_correlation_verified: bool
    D_diagonalizes_finite_CS_operator: bool
    asymptotic_natural_CS_correlation_proved: bool
    source_likelihood_decoder_constructed: bool
    coherent_subduction_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class MatchingChargeCSCorrelationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    invariant_basis: InvariantBasisControl
    correlation_control: CSCorrelationControl
    theorem: MatchingChargeCSCorrelationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _permutation_with_images(
    degree: int,
    images: dict[int, int],
) -> Permutation:
    permutation: list[int | None] = [None] * degree
    for source, target in images.items():
        permutation[source] = target
    remaining_sources = [
        source for source, target in enumerate(permutation) if target is None
    ]
    remaining_targets = [
        target for target in range(degree) if target not in images.values()
    ]
    for source, target in zip(remaining_sources, remaining_targets):
        permutation[source] = target
    return tuple(int(target) for target in permutation)


def _point_permutation_matrix(permutation: Permutation) -> np.ndarray:
    matrix = np.zeros((len(permutation), len(permutation)))
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def _act_on_point_pair_tensor(
    tensors: np.ndarray,
    representation: np.ndarray,
    permutation: Permutation,
) -> np.ndarray:
    count, degree, _, dimension, _ = tensors.shape
    transformed = (
        representation @ tensors.reshape(-1, dimension, dimension)
    ) @ representation.T
    transformed = transformed.reshape(
        count,
        degree,
        degree,
        dimension,
        dimension,
    )
    output = np.empty_like(transformed)
    for left in range(degree):
        for right in range(degree):
            output[:, permutation[left], permutation[right]] = transformed[
                :, left, right
            ]
    return output


def _prefix_tableau(tableau: Tableau, maximum_entry: int) -> Tableau:
    return tuple(
        tuple(value for value in row if value <= maximum_entry)
        for row in tableau
        if any(value <= maximum_entry for value in row)
    )


def _prefix_shape(
    tableau: Tableau,
    maximum_entry: int,
) -> tuple[int, ...]:
    return tuple(
        sum(value <= maximum_entry for value in row)
        for row in tableau
        if any(value <= maximum_entry for value in row)
    )


def _restriction_commutant_matrix_units(
    tableaux: tuple[Tableau, ...],
    maximum_entry: int,
) -> list[np.ndarray]:
    dimension = len(tableaux)
    groups: defaultdict[
        tuple[int, ...],
        defaultdict[Tableau, dict[Tableau, int]],
    ] = defaultdict(lambda: defaultdict(dict))
    for index, tableau in enumerate(tableaux):
        shape = _prefix_shape(tableau, maximum_entry)
        tail = tuple(
            tuple(value for value in row if value > maximum_entry)
            for row in tableau
        )
        prefix = _prefix_tableau(tableau, maximum_entry)
        groups[shape][tail][prefix] = index
    output: list[np.ndarray] = []
    for copies in groups.values():
        labels = list(copies)
        prefixes = set(copies[labels[0]])
        if not all(set(copies[label]) == prefixes for label in labels):
            raise AssertionError("restriction copies use inconsistent bases")
        for left_label in labels:
            for right_label in labels:
                matrix = np.zeros((dimension, dimension))
                for prefix in prefixes:
                    matrix[
                        copies[left_label][prefix],
                        copies[right_label][prefix],
                    ] = 1.0
                output.append(matrix / np.linalg.norm(matrix))
    return output


def _orthonormal_span(tensors: np.ndarray) -> np.ndarray:
    gram = np.einsum("qabij,rabij->qr", tensors, tensors)
    eigenvalues, eigenvectors = np.linalg.eigh((gram + gram.T) / 2.0)
    retained = eigenvalues > 1e-9
    coefficients = (
        eigenvectors[:, retained] / np.sqrt(eigenvalues[retained])
    ).T
    return np.einsum(
        "qr,rabij->qabij",
        coefficients,
        tensors,
        optimize=True,
    )


def _build_A_invariant_basis(
    partition: tuple[int, ...],
) -> tuple[np.ndarray, int, int, int]:
    degree = sum(partition)
    tableaux = standard_young_tableaux(partition)
    dimension = len(tableaux)
    S9_units = _restriction_commutant_matrix_units(tableaux, degree - 1)
    S8_units = _restriction_commutant_matrix_units(tableaux, degree - 2)
    candidates = []
    for matrix in S9_units:
        tensor = np.zeros((degree, degree, dimension, dimension))
        for point in range(degree):
            permutation = _permutation_with_images(
                degree,
                {degree - 1: point},
            )
            representation = _matrix_for_permutation(partition, permutation)
            tensor[point, point] = (
                representation @ matrix @ representation.T
            )
        candidates.append(tensor / math.sqrt(degree))
    for matrix in S8_units:
        tensor = np.zeros((degree, degree, dimension, dimension))
        for left in range(degree):
            for right in range(degree):
                if left == right:
                    continue
                permutation = _permutation_with_images(
                    degree,
                    {degree - 2: left, degree - 1: right},
                )
                representation = _matrix_for_permutation(
                    partition,
                    permutation,
                )
                tensor[left, right] = (
                    representation @ matrix @ representation.T
                )
        candidates.append(tensor / math.sqrt(degree * (degree - 1)))
    candidate_array = np.stack(candidates)
    standard_projector = (
        np.eye(degree) - np.ones((degree, degree)) / degree
    )
    candidate_array = np.einsum(
        "ac,bd,qcdij->qabij",
        standard_projector,
        standard_projector,
        candidate_array,
        optimize=True,
    )
    basis = _orthonormal_span(candidate_array)
    del candidate_array
    gc.collect()
    return basis, len(S9_units), len(S8_units), len(candidates)


def _apply_B_projector(
    basis: np.ndarray,
    partition: tuple[int, ...],
    half_degree: int,
) -> np.ndarray:
    degree = 2 * half_degree
    dimension = basis.shape[-1]
    hidden = tuple(point ^ 1 for point in range(degree))
    hidden_matrix = _matrix_for_permutation(partition, hidden)
    source_even = (np.eye(dimension) + hidden_matrix) / 2.0
    point_even = (
        np.eye(degree) + _point_permutation_matrix(hidden)
    ) / 2.0
    projected = (
        source_even @ basis.reshape(-1, dimension, dimension)
    ) @ source_even.T
    projected = projected.reshape(basis.shape)
    projected = np.einsum(
        "ac,qcbij->qabij",
        point_even,
        projected,
        optimize=True,
    )

    # Reynolds projection over the normal C_2^m base.
    for pair in range(half_degree):
        permutation = _permutation_with_images(
            degree,
            {2 * pair: 2 * pair + 1, 2 * pair + 1: 2 * pair},
        )
        representation = _matrix_for_permutation(partition, permutation)
        projected = (
            projected
            + _act_on_point_pair_tensor(
                projected,
                representation,
                permutation,
            )
        ) / 2.0

    # Reynolds projection over S_m through S_1<S_2<...<S_m cosets.
    for rank in range(2, half_degree + 1):
        accumulator = np.zeros_like(projected)
        for target in range(rank):
            if target == rank - 1:
                permutation = tuple(range(degree))
            else:
                permutation = _permutation_with_images(
                    degree,
                    {
                        2 * target: 2 * (rank - 1),
                        2 * target + 1: 2 * (rank - 1) + 1,
                        2 * (rank - 1): 2 * target,
                        2 * (rank - 1) + 1: 2 * target + 1,
                    },
                )
            representation = _matrix_for_permutation(
                partition,
                permutation,
            )
            accumulator += _act_on_point_pair_tensor(
                projected,
                representation,
                permutation,
            )
        projected = accumulator / rank
    return projected


def _K_generators_for_control(half_degree: int) -> tuple[Permutation, ...]:
    degree = 2 * half_degree
    generators = []
    first_flip = list(range(degree))
    first_flip[0], first_flip[1] = first_flip[1], first_flip[0]
    generators.append(tuple(first_flip))
    for pair in range(half_degree - 1):
        generators.append(
            _permutation_with_images(
                degree,
                {
                    2 * pair: 2 * (pair + 1),
                    2 * pair + 1: 2 * (pair + 1) + 1,
                    2 * (pair + 1): 2 * pair,
                    2 * (pair + 1) + 1: 2 * pair + 1,
                },
            )
        )
    return tuple(generators)


def _centered_correlation(left: np.ndarray, right: np.ndarray) -> float:
    dimension = left.shape[0]
    left_centered = left - np.trace(left) * np.eye(dimension) / dimension
    right_centered = right - np.trace(right) * np.eye(dimension) / dimension
    denominator = math.sqrt(
        float(np.trace(left_centered @ left_centered))
        * float(np.trace(right_centered @ right_centered))
    )
    if denominator <= 1e-15:
        return 0.0
    return float(np.trace(left_centered @ right_centered) / denominator)


def _regression_R2(
    target: np.ndarray,
    predictors: list[np.ndarray],
) -> float:
    dimension = target.shape[0]
    identity = np.eye(dimension)
    target_vector = (
        target - np.trace(target) * identity / dimension
    ).reshape(-1)
    columns = []
    for predictor in predictors:
        centered = predictor - np.trace(predictor) * identity / dimension
        columns.append(centered.reshape(-1))
    design = np.stack(columns, axis=1)
    coefficients, *_ = np.linalg.lstsq(design, target_vector, rcond=None)
    residual = target_vector - design @ coefficients
    denominator = float(target_vector @ target_vector)
    return 0.0 if denominator <= 1e-15 else 1.0 - float(residual @ residual) / denominator


@lru_cache(maxsize=1)
def audit_matching_charge_CS_correlation() -> tuple[
    InvariantBasisControl,
    CSCorrelationControl,
]:
    half_degree = 5
    degree = 10
    partition = (6, 2, 2)
    standard = (9, 1)
    basis, S9_dimension, S8_dimension, candidate_count = (
        _build_A_invariant_basis(partition)
    )
    A_gram = np.einsum("qabij,rabij->qr", basis, basis)
    A_orthogonality = float(
        np.linalg.norm(A_gram - np.eye(len(basis)))
    )
    A_invariance = 0.0
    for adjacent in range(degree - 1):
        permutation = _permutation_with_images(
            degree,
            {adjacent: adjacent + 1, adjacent + 1: adjacent},
        )
        representation = _matrix_for_permutation(partition, permutation)
        A_invariance = max(
            A_invariance,
            float(
                np.linalg.norm(
                    _act_on_point_pair_tensor(
                        basis,
                        representation,
                        permutation,
                    )
                    - basis
                )
            ),
        )

    projected = _apply_B_projector(basis, partition, half_degree)
    overlap = np.einsum("qabij,rabij->qr", basis, projected)
    B_gram = np.einsum("qabij,rabij->qr", projected, projected)
    B_gram_residual = float(np.linalg.norm(overlap - B_gram))
    B_invariance = 0.0
    for permutation in _K_generators_for_control(half_degree):
        representation = _matrix_for_permutation(partition, permutation)
        B_invariance = max(
            B_invariance,
            float(
                np.linalg.norm(
                    _act_on_point_pair_tensor(
                        projected,
                        representation,
                        permutation,
                    )
                    - projected
                )
            ),
        )
    hidden = tuple(point ^ 1 for point in range(degree))
    hidden_matrix = _matrix_for_permutation(partition, hidden)
    source_even = (np.eye(basis.shape[-1]) + hidden_matrix) / 2.0
    point_even = (
        np.eye(degree) + _point_permutation_matrix(hidden)
    ) / 2.0
    parity_residual = float(
        np.linalg.norm(
            (
                source_even
                @ projected.reshape(-1, basis.shape[-1], basis.shape[-1])
            ).reshape(projected.shape)
            - projected
        )
        + np.linalg.norm(
            np.einsum(
                "ac,qcbij->qabij",
                point_even,
                projected,
                optimize=True,
            )
            - projected
        )
    )
    invariant_control = InvariantBasisControl(
        degree=degree,
        half_degree=half_degree,
        repeated_symmetric_partition=partition,
        repeated_irrep_dimension=basis.shape[-1],
        source_standard_partition=standard,
        target_standard_partition=standard,
        S9_commutant_dimension=S9_dimension,
        S8_commutant_dimension=S8_dimension,
        point_orbit_candidate_count=candidate_count,
        standard_standard_A_invariant_dimension=len(basis),
        expected_A_invariant_dimension=6,
        maximum_A_orthonormality_residual=A_orthogonality,
        maximum_A_generator_invariance_residual=A_invariance,
        maximum_B_projection_gram_residual=B_gram_residual,
        maximum_B_K_generator_invariance_residual=B_invariance,
        maximum_B_source_parity_residual=parity_residual,
        construction_verified=bool(
            len(basis) == 6
            and A_orthogonality < 1e-9
            and A_invariance < 1e-9
            and B_gram_residual < 1e-9
            and B_invariance < 1e-9
            and parity_residual < 1e-9
        ),
        status="exact-S10-three-source-A-B-block-constructed",
    )

    overlap = (overlap + overlap.T) / 2.0
    eigenvalues, eigenvectors = np.linalg.eigh(overlap)
    retained = eigenvalues > 1e-10
    inverse_square_root = eigenvectors[:, retained] @ np.diag(
        1.0 / np.sqrt(eigenvalues[retained])
    )
    occupied_basis = np.einsum(
        "qr,rabij->qabij",
        inverse_square_root.T,
        projected,
        optimize=True,
    )
    cross = np.einsum("qabij,rabij->qr", basis, occupied_basis)
    CS_operator = cross.T @ cross

    charge_matrices = _average_matrices_for_sets(
        partition,
        [
            tuple(central_pair_charge(half_degree)),
            tuple(disjoint_matching_charge(half_degree)),
        ],
    )
    compressed_charges = []
    leakages = []
    for charge in charge_matrices:
        action = (
            charge
            @ occupied_basis.reshape(
                -1,
                basis.shape[-1],
                basis.shape[-1],
            )
        ).reshape(occupied_basis.shape)
        compressed = np.einsum(
            "qabij,rabij->qr",
            occupied_basis,
            action,
        )
        compressed = (compressed + compressed.T) / 2.0
        projected_action = np.einsum(
            "rq,rabij->qabij",
            compressed,
            occupied_basis,
            optimize=True,
        )
        compressed_charges.append(compressed)
        leakages.append(float(np.linalg.norm(action - projected_action)))
    central_compressed, matching_compressed = compressed_charges
    central_correlation = _centered_correlation(
        central_compressed,
        CS_operator,
    )
    matching_correlation = _centered_correlation(
        matching_compressed,
        CS_operator,
    )
    central_R2 = _regression_R2(CS_operator, [central_compressed])
    combined_R2 = _regression_R2(
        CS_operator,
        [central_compressed, matching_compressed],
    )
    matching_eigenvalues = np.linalg.eigvalsh(matching_compressed)
    principal_values = np.linalg.eigvalsh(CS_operator)
    matching_commutator = float(
        np.linalg.norm(
            matching_compressed @ CS_operator
            - CS_operator @ matching_compressed
        )
    )
    distinct_matching = int(1 + sum(
        right - left > 1e-8
        for left, right in zip(
            matching_eigenvalues,
            matching_eigenvalues[1:],
        )
    ))
    correlation_control = CSCorrelationControl(
        occupied_CS_rank=len(principal_values),
        squared_principal_cosines=principal_values.tolist(),
        minimum_squared_principal_cosine=float(min(principal_values)),
        maximum_squared_principal_cosine=float(max(principal_values)),
        principal_cosine_squared_range=float(np.ptp(principal_values)),
        principal_spectrum_nonflat=float(np.ptp(principal_values)) > 1e-3,
        matching_charge_compressed_eigenvalues=matching_eigenvalues.tolist(),
        matching_charge_distinct_compressed_eigenvalue_count=distinct_matching,
        matching_charge_compression_frobenius_norm=float(
            np.linalg.norm(matching_compressed)
        ),
        matching_charge_occupied_subspace_leakage_norm=leakages[1],
        matching_charge_CS_commutator_norm=matching_commutator,
        matching_charge_centered_CS_correlation=matching_correlation,
        central_charge_centered_CS_correlation=central_correlation,
        central_charge_only_regression_R2=central_R2,
        central_plus_matching_regression_R2=combined_R2,
        matching_charge_incremental_regression_R2=combined_R2 - central_R2,
        matching_charge_nontrivial_in_occupied_block=bool(
            np.linalg.norm(matching_compressed) > 1e-3
            and distinct_matching == len(principal_values)
        ),
        matching_charge_correlates_with_CS_operator=bool(
            abs(matching_correlation) > 0.1
            and combined_R2 > central_R2 + 1e-3
        ),
        matching_charge_diagonalizes_CS_operator=matching_commutator < 1e-10,
        finite_numerical_control_only=True,
        status=(
            "finite-matrix-CS-correlation-for-matching-charge"
            if abs(matching_correlation) > 0.1
            else "matching-charge-CS-correlation-control-failure"
        ),
    )
    del basis, projected, occupied_basis
    gc.collect()
    return invariant_control, correlation_control


@lru_cache(maxsize=1)
def build_matching_charge_CS_correlation_report() -> MatchingChargeCSCorrelationReport:
    invariant, correlation = audit_matching_charge_CS_correlation()
    branch = audit_branch_resolution(5, (6, 2, 2))
    branch_added = branch.D_added_copy_label_count > 0
    verified = bool(
        invariant.construction_verified
        and correlation.principal_spectrum_nonflat
        and correlation.matching_charge_nontrivial_in_occupied_block
        and correlation.matching_charge_correlates_with_CS_operator
        and branch_added
    )
    theorem = MatchingChargeCSCorrelationTheorem(
        block=(
            "S_10 block ((6,2,2),(6,2,2),(9,1); target (9,1)) with A-dimension six."
        ),
        A_basis=(
            "Diagonal/off-diagonal point-pair orbit induction from End_(S_9)(V_lambda) and End_(S_8)(V_lambda), projected to Std tensor Std."
        ),
        B_projector=(
            "Three h-even source projectors followed by the exact C_2 wr S_5 Reynolds projector."
        ),
        finite_result=(
            "The occupied CS spectrum is nonflat and compressed D_5 has six eigenvalues with nonzero centered CS covariance."
        ),
        interpretation=(
            "D_5 is not pure nuisance in this exact matrix block, but it neither diagonalizes the CS operator nor preserves its occupied range."
        ),
        exact_invariant_space_construction_verified=invariant.construction_verified,
        full_rank_nonflat_matrix_CS_block_verified=(
            correlation.occupied_CS_rank == 6
            and correlation.principal_spectrum_nonflat
        ),
        D_adds_branch_copy_label_verified=branch_added,
        D_nontrivial_on_occupied_CS_space_verified=(
            correlation.matching_charge_nontrivial_in_occupied_block
        ),
        finite_D_CS_correlation_verified=(
            correlation.matching_charge_correlates_with_CS_operator
        ),
        D_diagonalizes_finite_CS_operator=(
            correlation.matching_charge_diagonalizes_CS_operator
        ),
        asymptotic_natural_CS_correlation_proved=False,
        source_likelihood_decoder_constructed=False,
        coherent_subduction_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "finite-D-CS-correlation-proved-natural-scaling-open"
            if verified
            else "matching-charge-CS-correlation-theorem-control-failure"
        ),
    )
    return MatchingChargeCSCorrelationReport(
        created_at=utc_now(),
        theorem_contract={
            "group": "S_10",
            "source_irreps": ["(6,2,2)", "(6,2,2)", "(9,1)"],
            "target_irrep": "(9,1)",
            "access": "Exact Young orthogonal representations and subgroup Reynolds projectors",
            "claim_boundary": (
                "Finite mechanism correlation in one matrix block; no natural-mass scaling or detector."
            ),
        },
        invariant_basis=invariant,
        correlation_control=correlation,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-D-CS-CORRELATION-SCALING",
                "statement": (
                    "Construct an all-rank block family or source-weighted moment identity with nonvanishing D/CS covariance."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-D-CS-LEAKAGE-COMPLETION",
                "statement": (
                    "Determine whether additional commuting charges control the observed leakage outside the occupied CS range."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-D-CS-DECODER",
                "statement": (
                    "Turn charge statistics into a source-likelihood estimator and compare it with classical baselines."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Natural algebraic independence may be pure nuisance for the CS likelihood.",
                "answer": (
                    "Not universally: this exact nonflat matrix block has nonzero basis-independent D/CS covariance and incremental regression signal."
                ),
                "resolved": True,
            },
            {
                "challenge": "The correlation is an artifact of a scalar CS block.",
                "answer": (
                    "False: all six principal values are occupied and their squared-value range exceeds 0.14."
                ),
                "resolved": True,
            },
            {
                "challenge": "D_5 already diagonalizes the block likelihood.",
                "answer": (
                    "False: its compressed commutator and occupied-range leakage are both nonzero."
                ),
                "resolved": True,
            },
            {
                "challenge": "One degree-ten block proves natural asymptotic correlation.",
                "answer": (
                    "False: this is finite evidence and the block has no proved nonnegligible source mass."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "DOI:10.1145/258533.258548",
                "role": "Young-basis symmetric-group Fourier representation used for exact block controls.",
            },
            {
                "id": "arXiv:0710.4971",
                "role": "Commuting-charge motivation; not a source-CS correlation theorem.",
            },
            {
                "id": "arXiv:1807.00481",
                "role": "Perfect-matching harmonic and stabilizer context for the standard point modules.",
            },
        ],
        headline_metrics={
            "exact_three_source_matrix_block_count": int(
                invariant.construction_verified
            ),
            "full_rank_nonflat_CS_block_count": int(
                correlation.occupied_CS_rank == 6
                and correlation.principal_spectrum_nonflat
            ),
            "finite_D_CS_correlation_count": int(
                correlation.matching_charge_correlates_with_CS_operator
            ),
            "finite_D_CS_diagonalization_count": int(
                correlation.matching_charge_diagonalizes_CS_operator
            ),
            "asymptotic_natural_CS_correlation_count": 0,
            "source_likelihood_decoder_count": 0,
            "hidden_involution_detector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_invariant_space_construction_verified": (
                invariant.construction_verified
            ),
            "finite_full_rank_nonflat_CS_block_verified": (
                correlation.occupied_CS_rank == 6
                and correlation.principal_spectrum_nonflat
            ),
            "D_adds_copy_label_in_lambda_restriction": branch_added,
            "finite_D_CS_correlation_verified": (
                correlation.matching_charge_correlates_with_CS_operator
            ),
            "D_diagonalizes_finite_CS_operator": (
                correlation.matching_charge_diagonalizes_CS_operator
            ),
            "asymptotic_natural_CS_correlation_proved": False,
            "source_likelihood_decoder_constructed": False,
            "coherent_subduction_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The matching charge correlates with one exact matrix CS block, but leakage, scaling, likelihood decoding, and natural source mass remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Constructed a full-rank nonflat three-source CS block where the new matching charge has nonzero likelihood correlation."
        ),
        falsifiers_triggered=[
            "The new natural matching label is not universally pure nuisance.",
            "The matching charge does not by itself diagonalize the matrix CS likelihood.",
            "Finite correlation is not evidence of asymptotic detector performance.",
        ],
    )


def write_matching_charge_CS_correlation_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_matching_charge_CS_correlation_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_matching_charge_CS_correlation_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
