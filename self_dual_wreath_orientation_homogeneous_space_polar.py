r"""Homogeneous-space flattening of the complete orientation polar.

Let ``G=S_n``, ``Gamma=G^(2K+1)``, and let ``B=C_2^K`` swap the two
source coordinates in each of the ``K`` pairs.  Form

    Omega = Gamma semidirect B.

For the zero orientation, let ``D`` be the diagonal copy of ``G`` acting on
the target and the zero-selected coordinate of every source pair.  Its
conjugates by ``B`` are exactly the orientation subgroups ``H_e``.  There are
canonical identifications

    Omega / D = disjoint_union_e Gamma / H_e,
    Omega / B = Gamma.

If ``J_H`` denotes the normalized right-coset embedding into ``C[Omega]``, the
orientation synthesis is therefore the single equivariant incidence map

    T = sqrt(|B|) J_B^* J_D.                              (1)

Its columns are the normalized ``H_e`` coset states.  Consequently the polar
of ``T`` is the direct sum, with regular multiplicities, of all natural
orientation polars.  Equation (1) removes explicit enumeration of a
factorial-width candidate list from the *description* of the transform; it
does not implement the polar.

Fourier transformation over ``Omega`` reduces (1) in every irrep ``rho`` to

    I_(V_rho) tensor sqrt(|B|) [Fix_D(rho) -> Fix_B(rho)],

so the missing operation is a matrix Cosine--Sine/subduction polar between
the two fixed spaces.  The outer group transform is structured because

    Omega is isomorphic to G times ((G x G) semidirect C_2)^K.

It is not a scalar spherical transform.  Writing ``g=|S_n|``, ``p=p(n)``, and
``I_n=sum_lambda d_lambda`` (the number of involutions in ``S_n``),

    #Irr(Omega) = p [p(p+3)/2]^K,
    # (B\Omega/B) = g [(g^2+g)/2]^K,
    sum_(rho in Irr(Omega)) d_rho = I_n (I_n^2+g)^K.      (2)

For the physical permutation module ``Ind_B^Omega(1)``, the dimension fraction
in blocks with ``m_B(rho)=dim Fix_B(rho) <= L`` is at most

    L I_n (I_n^2+g)^K / g^(2K+1).                         (3)

The analogous source fraction replaces the denominator by ``2^K g^(2K)``.
At ``K=ceil(log_2 g)+2`` and ``L=g^(K/4)``, both bounds are already tiny and
decay superpolynomially.  Thus merely applying the efficient outer QFT cannot
turn the natural transform into scalar filtering: matrix multiplicity is the
typical dimension regime on both quotient spaces.

Large multiplicity is not a hardness theorem.  The occupied overlap may have
a succinct basis or fast transform.  However, the exact incidence moments

    Tr(F)   = (2^K/g) dim(C[Gamma]),
    Tr(F^2) = [1+(2^K-1)/g] Tr(F),             F=TT^*,    (4)

do transfer (2) to the native regular-master frame law.  If ``r_rho`` is the
occupied rank of the fixed-space overlap in block ``rho``, the total ambient
rank of blocks with ``r_rho<=R`` is at most

    R sum_rho d_rho.

Hilbert--Schmidt Cauchy--Schwarz therefore bounds their native frame mass by

    sqrt((gamma/c) R I_n(I_n^2+g)^K / g^(2K+1)),          (5)

where ``c=2^K/g`` and ``gamma=1+(2^K-1)/g``.  Taking
``R=g^(K/4)`` makes (5) negligible.  Thus the occupied matrix-CS rank is huge
on nearly all native regular-master frame mass.  This still is not a hardness
theorem: a huge occupied overlap can have a succinct basis or fast transform.
The surviving high-value task is an explicit
normalization-one polar for the ``D``-fixed to ``B``-fixed subduction map, or a
proof that its natural occupied part retains unrestricted Kronecker
recoupling.  No circuit, decoder, classical separation, or speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_natural_matrix_multiplicity import (
    symmetric_group_involution_count,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_homogeneous_space_polar.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-HOMOGENEOUS-SPACE-POLAR"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
GammaElement = tuple[Permutation, ...]
OmegaElement = tuple[GammaElement, int]


@dataclass(frozen=True)
class HomogeneousIncidenceControl:
    n: int
    copy_count: int
    symmetric_group_order: int
    orientation_count: int
    gamma_order: int
    omega_order: int
    source_quotient_dimension: int
    physical_quotient_dimension: int
    direct_orientation_synthesis_dimension: tuple[int, int]
    maximum_homogeneous_incidence_residual: float
    maximum_left_equivariance_residual: float
    left_frame_projection_identity_residual: float
    right_gram_projection_identity_residual: float
    frame_trace: float
    predicted_frame_trace: float
    frame_second_moment: float
    predicted_frame_second_moment: float
    maximum_frame_moment_residual: float
    polar_initial_support_residual: float
    polar_final_support_residual: float
    exact_homogeneous_space_polar_verified: bool
    status: str


@dataclass(frozen=True)
class MatrixMultiplicityScalingRecord:
    n: int
    symmetric_group_order_log2: float
    partition_count: int
    involution_dimension_sum_log2: float
    copy_count: int
    orientation_count_log2: int
    omega_irrep_count_log2: float
    physical_hecke_dimension_log2: float
    maximum_fixed_multiplicity_log2_lower_bound: float
    multiplicity_threshold_log2: float
    low_multiplicity_physical_dimension_fraction_log2_upper_bound: float
    low_multiplicity_source_dimension_fraction_log2_upper_bound: float
    low_multiplicity_physical_dimension_fraction_upper_bound: float
    low_multiplicity_source_dimension_fraction_upper_bound: float
    matrix_multiplicity_typical_on_both_quotients: bool
    occupied_overlap_rank_lower_bound_proved: bool
    native_size_biased_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class NativeOccupiedRankScalingRecord:
    n: int
    copy_count: int
    orientation_to_group_ratio: float
    frame_second_to_first_moment_ratio: float
    total_support_rank_fraction_lower_bound: float
    occupied_rank_threshold_log2: float
    low_occupied_rank_ambient_fraction_log2_upper_bound: float
    low_occupied_rank_native_frame_mass_log2_upper_bound: float
    low_occupied_rank_native_frame_mass_upper_bound: float
    high_occupied_rank_native_frame_mass_lower_bound: float
    native_regular_master_large_occupied_rank_proved: bool
    physical_conditioned_size_biased_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class OrientationHomogeneousSpacePolarTheorem:
    group: str
    quotient_identification: str
    incidence: str
    frame_identities: str
    fourier_block: str
    outer_qft_factorization: str
    multiplicity_obstruction: str
    native_occupied_rank: str
    compiler_target: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationHomogeneousSpacePolarReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: OrientationHomogeneousSpacePolarTheorem
    finite_controls: list[HomogeneousIncidenceControl]
    scaling_records: list[MatrixMultiplicityScalingRecord]
    native_occupied_rank_records: list[NativeOccupiedRankScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _identity(n: int) -> Permutation:
    return tuple(range(n))


def symmetric_group(n: int) -> tuple[Permutation, ...]:
    if n < 1:
        raise ValueError("n must be positive")
    return tuple(itertools.permutations(range(n)))


def _gamma_multiply(left: GammaElement, right: GammaElement) -> GammaElement:
    return tuple(_compose(a, b) for a, b in zip(left, right))


def branch_action(gamma: GammaElement, branch_mask: int) -> GammaElement:
    if len(gamma) % 2 != 1:
        raise ValueError("Gamma must have one target and paired source coordinates")
    copy_count = (len(gamma) - 1) // 2
    if not 0 <= branch_mask < 1 << copy_count:
        raise ValueError("invalid branch mask")
    output = [gamma[0]]
    for pair_index in range(copy_count):
        left = gamma[1 + 2 * pair_index]
        right = gamma[2 + 2 * pair_index]
        output.extend(
            (right, left)
            if branch_mask & (1 << pair_index)
            else (left, right)
        )
    return tuple(output)


def omega_multiply(left: OmegaElement, right: OmegaElement) -> OmegaElement:
    left_gamma, left_branch = left
    right_gamma, right_branch = right
    return (
        _gamma_multiply(left_gamma, branch_action(right_gamma, left_branch)),
        left_branch ^ right_branch,
    )


def orientation_embedding(
    element: Permutation,
    copy_count: int,
    orientation_mask: int,
) -> GammaElement:
    if copy_count < 1 or not 0 <= orientation_mask < 1 << copy_count:
        raise ValueError("invalid copy count or orientation")
    identity = _identity(len(element))
    output = [element]
    for pair_index in range(copy_count):
        selected = int(bool(orientation_mask & (1 << pair_index)))
        output.extend(
            element if slot == selected else identity for slot in (0, 1)
        )
    return tuple(output)


def _group_data(
    n: int,
    copy_count: int,
) -> tuple[
    tuple[Permutation, ...],
    tuple[GammaElement, ...],
    tuple[OmegaElement, ...],
    tuple[OmegaElement, ...],
    tuple[OmegaElement, ...],
]:
    group = symmetric_group(n)
    gamma = tuple(itertools.product(group, repeat=2 * copy_count + 1))
    omega = tuple(
        (point, branch)
        for branch in range(1 << copy_count)
        for point in gamma
    )
    identity_gamma = tuple(_identity(n) for _ in range(2 * copy_count + 1))
    branch_subgroup = tuple(
        (identity_gamma, branch) for branch in range(1 << copy_count)
    )
    diagonal_subgroup = tuple(
        (orientation_embedding(element, copy_count, 0), 0)
        for element in group
    )
    return group, gamma, omega, branch_subgroup, diagonal_subgroup


def _right_coset_embedding(
    elements: tuple[OmegaElement, ...],
    subgroup: tuple[OmegaElement, ...],
) -> tuple[np.ndarray, tuple[OmegaElement, ...], dict[OmegaElement, int]]:
    index = {element: position for position, element in enumerate(elements)}
    element_to_coset: dict[OmegaElement, int] = {}
    representatives: list[OmegaElement] = []
    cosets: list[tuple[int, ...]] = []
    for representative in elements:
        if representative in element_to_coset:
            continue
        coset_elements = tuple(
            omega_multiply(representative, member) for member in subgroup
        )
        coset_indices = tuple(sorted(index[element] for element in coset_elements))
        column = len(representatives)
        representatives.append(representative)
        cosets.append(coset_indices)
        for element in coset_elements:
            element_to_coset[element] = column
    embedding = np.zeros((len(elements), len(representatives)), dtype=float)
    amplitude = 1.0 / math.sqrt(len(subgroup))
    for column, coset in enumerate(cosets):
        embedding[list(coset), column] = amplitude
    return embedding, tuple(representatives), element_to_coset


def _gamma_right_coset_labels(
    gamma: tuple[GammaElement, ...],
    subgroup: tuple[GammaElement, ...],
) -> tuple[tuple[int, ...], dict[GammaElement, int]]:
    index = {element: position for position, element in enumerate(gamma)}
    labels: list[int] = []
    point_to_label: dict[GammaElement, int] = {}
    for representative in gamma:
        if representative in point_to_label:
            continue
        coset = tuple(_gamma_multiply(representative, member) for member in subgroup)
        label = min(index[element] for element in coset)
        labels.append(label)
        for element in coset:
            point_to_label[element] = label
    return tuple(sorted(labels)), point_to_label


def direct_orientation_synthesis(
    n: int,
    copy_count: int,
) -> tuple[np.ndarray, tuple[tuple[int, int], ...], tuple[GammaElement, ...]]:
    group = symmetric_group(n)
    gamma = tuple(itertools.product(group, repeat=2 * copy_count + 1))
    gamma_index = {point: index for index, point in enumerate(gamma)}
    columns: list[np.ndarray] = []
    labels: list[tuple[int, int]] = []
    amplitude = 1.0 / math.sqrt(len(group))
    for orientation in range(1 << copy_count):
        subgroup = tuple(
            orientation_embedding(element, copy_count, orientation)
            for element in group
        )
        coset_labels, point_to_label = _gamma_right_coset_labels(gamma, subgroup)
        for label in coset_labels:
            column = np.zeros(len(gamma), dtype=float)
            members = [
                point
                for point in gamma
                if point_to_label[point] == label
            ]
            column[[gamma_index[point] for point in members]] = amplitude
            columns.append(column)
            labels.append((orientation, label))
    return np.column_stack(columns), tuple(labels), gamma


def _support(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    basis = vectors[:, values > tolerance]
    return basis @ basis.conj().T


def _polar(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, right_star = np.linalg.svd(matrix, full_matrices=False)
    retained = singular_values > tolerance
    return left[:, retained] @ right_star[retained, :]


def _left_action_matrix(
    generator: OmegaElement,
    representatives: tuple[OmegaElement, ...],
    element_to_coset: dict[OmegaElement, int],
) -> np.ndarray:
    output = np.zeros((len(representatives), len(representatives)), dtype=float)
    for column, representative in enumerate(representatives):
        image = omega_multiply(generator, representative)
        output[element_to_coset[image], column] = 1.0
    return output


def audit_homogeneous_incidence(
    n: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> HomogeneousIncidenceControl:
    if n < 2 or copy_count < 1:
        raise ValueError("n>=2 and positive copy count are required")
    group, gamma, omega, branch_subgroup, diagonal_subgroup = _group_data(
        n,
        copy_count,
    )
    j_branch, branch_representatives, branch_coset_map = _right_coset_embedding(
        omega,
        branch_subgroup,
    )
    j_diagonal, diagonal_representatives, diagonal_coset_map = (
        _right_coset_embedding(omega, diagonal_subgroup)
    )
    orientation_count = 1 << copy_count
    homogeneous = math.sqrt(orientation_count) * j_branch.T @ j_diagonal

    direct, direct_labels, direct_gamma = direct_orientation_synthesis(n, copy_count)
    gamma_index = {point: index for index, point in enumerate(direct_gamma)}
    direct_label_index = {label: index for index, label in enumerate(direct_labels)}
    aligned = np.zeros_like(direct)
    for branch_column, (point, _branch) in enumerate(branch_representatives):
        row = gamma_index[point]
        for diagonal_column, (representative, orientation) in enumerate(
            diagonal_representatives
        ):
            subgroup = tuple(
                orientation_embedding(element, copy_count, orientation)
                for element in group
            )
            _, point_to_label = _gamma_right_coset_labels(gamma, subgroup)
            label = (orientation, point_to_label[representative])
            aligned[row, direct_label_index[label]] = homogeneous[
                branch_column,
                diagonal_column,
            ]

    p_diagonal = j_diagonal @ j_diagonal.T
    p_branch = j_branch @ j_branch.T
    left_identity = float(
        np.linalg.norm(
            homogeneous @ homogeneous.T
            - orientation_count * j_branch.T @ p_diagonal @ j_branch,
            ord=2,
        )
    )
    right_identity = float(
        np.linalg.norm(
            homogeneous.T @ homogeneous
            - orientation_count * j_diagonal.T @ p_branch @ j_diagonal,
            ord=2,
        )
    )
    frame = homogeneous @ homogeneous.T
    frame_trace = float(np.trace(frame).real)
    frame_second = float(np.trace(frame @ frame).real)
    predicted_trace = orientation_count * len(gamma) / len(group)
    predicted_second = predicted_trace * (
        1.0 + (orientation_count - 1) / len(group)
    )
    moment_residual = max(
        abs(frame_trace - predicted_trace),
        abs(frame_second - predicted_second),
    )

    identity_gamma = tuple(_identity(n) for _ in range(2 * copy_count + 1))
    generators: list[OmegaElement] = [
        (identity_gamma, 1 << index) for index in range(copy_count)
    ]
    for coordinate in range(2 * copy_count + 1):
        adjacent = list(range(n))
        adjacent[0], adjacent[1] = adjacent[1], adjacent[0]
        point = list(identity_gamma)
        point[coordinate] = tuple(adjacent)
        generators.append((tuple(point), 0))
    equivariance = 0.0
    for generator in generators:
        left_branch = _left_action_matrix(
            generator,
            branch_representatives,
            branch_coset_map,
        )
        left_diagonal = _left_action_matrix(
            generator,
            diagonal_representatives,
            diagonal_coset_map,
        )
        equivariance = max(
            equivariance,
            float(np.linalg.norm(left_branch @ homogeneous - homogeneous @ left_diagonal, ord=2)),
        )

    polar = _polar(homogeneous, tolerance)
    initial_support = _support(homogeneous.T @ homogeneous, tolerance)
    final_support = _support(homogeneous @ homogeneous.T, tolerance)
    initial_residual = float(
        np.linalg.norm(polar.T @ polar - initial_support, ord=2)
    )
    final_residual = float(
        np.linalg.norm(polar @ polar.T - final_support, ord=2)
    )
    incidence_residual = float(np.linalg.norm(aligned - direct, ord=2))
    verified = bool(
        incidence_residual <= tolerance
        and equivariance <= tolerance
        and left_identity <= tolerance
        and right_identity <= tolerance
        and moment_residual <= 100 * tolerance
        and initial_residual <= 100 * tolerance
        and final_residual <= 100 * tolerance
    )
    return HomogeneousIncidenceControl(
        n=n,
        copy_count=copy_count,
        symmetric_group_order=len(group),
        orientation_count=orientation_count,
        gamma_order=len(gamma),
        omega_order=len(omega),
        source_quotient_dimension=len(diagonal_representatives),
        physical_quotient_dimension=len(branch_representatives),
        direct_orientation_synthesis_dimension=direct.shape,
        maximum_homogeneous_incidence_residual=incidence_residual,
        maximum_left_equivariance_residual=equivariance,
        left_frame_projection_identity_residual=left_identity,
        right_gram_projection_identity_residual=right_identity,
        frame_trace=frame_trace,
        predicted_frame_trace=predicted_trace,
        frame_second_moment=frame_second,
        predicted_frame_second_moment=predicted_second,
        maximum_frame_moment_residual=moment_residual,
        polar_initial_support_residual=initial_residual,
        polar_final_support_residual=final_residual,
        exact_homogeneous_space_polar_verified=verified,
        status=(
            "exact-single-homogeneous-incidence-polar"
            if verified
            else "homogeneous-incidence-control-failure"
        ),
    )


def _probability_from_log2(log2_value: float) -> float:
    if log2_value >= 0:
        return 1.0
    if log2_value < -1074:
        return 0.0
    return 2.0**log2_value


def partition_number(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


def matrix_multiplicity_scaling_record(
    n: int,
    *,
    extra_copies: int = 2,
) -> MatrixMultiplicityScalingRecord:
    if n < 3 or extra_copies < 0:
        raise ValueError("n>=3 and a nonnegative copy offset are required")
    group_order = math.factorial(n)
    group_log2 = math.log2(group_order)
    partition_count = partition_number(n)
    involution_sum = symmetric_group_involution_count(n)
    involution_log2 = math.log2(involution_sum)
    copy_count = (group_order - 1).bit_length() + extra_copies
    q_log2 = copy_count

    wreath_irrep_count = partition_count * (partition_count + 3) // 2
    omega_irrep_count_log2 = math.log2(partition_count) + copy_count * math.log2(
        wreath_irrep_count
    )
    local_hecke_count = group_order * (group_order + 1) // 2
    physical_hecke_log2 = group_log2 + copy_count * math.log2(local_hecke_count)
    maximum_multiplicity_log2_lower = max(
        0.0,
        0.5 * (physical_hecke_log2 - omega_irrep_count_log2),
    )

    irrep_dimension_sum_log2 = involution_log2 + copy_count * math.log2(
        involution_sum * involution_sum + group_order
    )
    threshold_log2 = copy_count * group_log2 / 4.0
    physical_dimension_log2 = (2 * copy_count + 1) * group_log2
    source_dimension_log2 = q_log2 + 2 * copy_count * group_log2
    physical_low_log2 = (
        threshold_log2 + irrep_dimension_sum_log2 - physical_dimension_log2
    )
    source_low_log2 = (
        threshold_log2 + irrep_dimension_sum_log2 - source_dimension_log2
    )
    physical_bound = _probability_from_log2(physical_low_log2)
    source_bound = _probability_from_log2(source_low_log2)
    typical = bool(
        physical_low_log2 <= -8.0
        and source_low_log2 <= -8.0
        and physical_hecke_log2 > omega_irrep_count_log2
    )
    return MatrixMultiplicityScalingRecord(
        n=n,
        symmetric_group_order_log2=group_log2,
        partition_count=partition_count,
        involution_dimension_sum_log2=involution_log2,
        copy_count=copy_count,
        orientation_count_log2=q_log2,
        omega_irrep_count_log2=omega_irrep_count_log2,
        physical_hecke_dimension_log2=physical_hecke_log2,
        maximum_fixed_multiplicity_log2_lower_bound=(
            maximum_multiplicity_log2_lower
        ),
        multiplicity_threshold_log2=threshold_log2,
        low_multiplicity_physical_dimension_fraction_log2_upper_bound=(
            physical_low_log2
        ),
        low_multiplicity_source_dimension_fraction_log2_upper_bound=source_low_log2,
        low_multiplicity_physical_dimension_fraction_upper_bound=physical_bound,
        low_multiplicity_source_dimension_fraction_upper_bound=source_bound,
        matrix_multiplicity_typical_on_both_quotients=typical,
        occupied_overlap_rank_lower_bound_proved=False,
        native_size_biased_transfer_proved=False,
        status=(
            "uniform-quotient-dimension-concentrates-on-huge-matrix-blocks"
            if typical
            else "matrix-multiplicity-asymptotic-bound-not-yet-decisive"
        ),
    )


def native_occupied_rank_scaling_record(
    n: int,
    *,
    extra_copies: int = 2,
) -> NativeOccupiedRankScalingRecord:
    multiplicity = matrix_multiplicity_scaling_record(
        n,
        extra_copies=extra_copies,
    )
    group_order = math.factorial(n)
    copy_count = multiplicity.copy_count
    orientation_count = 1 << copy_count
    ratio = orientation_count / group_order
    second_to_first = 1.0 + (orientation_count - 1) / group_order
    ambient_log2 = (
        multiplicity.low_multiplicity_physical_dimension_fraction_log2_upper_bound
    )
    native_log2 = 0.5 * (
        math.log2(second_to_first / ratio) + ambient_log2
    )
    native_upper = _probability_from_log2(native_log2)
    proved = native_log2 <= -4.0
    return NativeOccupiedRankScalingRecord(
        n=n,
        copy_count=copy_count,
        orientation_to_group_ratio=ratio,
        frame_second_to_first_moment_ratio=second_to_first,
        total_support_rank_fraction_lower_bound=ratio / second_to_first,
        occupied_rank_threshold_log2=multiplicity.multiplicity_threshold_log2,
        low_occupied_rank_ambient_fraction_log2_upper_bound=ambient_log2,
        low_occupied_rank_native_frame_mass_log2_upper_bound=native_log2,
        low_occupied_rank_native_frame_mass_upper_bound=native_upper,
        high_occupied_rank_native_frame_mass_lower_bound=max(0.0, 1.0 - native_upper),
        native_regular_master_large_occupied_rank_proved=proved,
        physical_conditioned_size_biased_transfer_proved=False,
        status=(
            "native-regular-master-mass-concentrates-on-huge-occupied-cs-rank"
            if proved
            else "native-occupied-rank-bound-not-yet-decisive"
        ),
    )


def run_orientation_homogeneous_space_polar() -> (
    OrientationHomogeneousSpacePolarReport
):
    controls = [
        audit_homogeneous_incidence(2, 1),
        audit_homogeneous_incidence(2, 2),
        audit_homogeneous_incidence(3, 1),
    ]
    scaling = [
        matrix_multiplicity_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    occupied = [
        native_occupied_rank_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(not row.exact_homogeneous_space_polar_verified for row in controls)
    typical = all(row.matrix_multiplicity_typical_on_both_quotients for row in scaling)
    occupied_verified = all(
        row.native_regular_master_large_occupied_rank_proved for row in occupied
    )
    verified = failures == 0 and typical and occupied_verified
    theorem = OrientationHomogeneousSpacePolarTheorem(
        group="Omega=S_n x (((S_n x S_n) semidirect C_2)^K)",
        quotient_identification=(
            "Omega/D is the disjoint union of Gamma/H_e and Omega/B is Gamma."
        ),
        incidence="T=sqrt(2^K) J_B^* J_D is the complete orientation synthesis.",
        frame_identities=(
            "TT*=2^K J_B^* P_D J_B and T*T=2^K J_D^* P_B J_D."
        ),
        fourier_block=(
            "Each Omega irrep carries identity on its row space tensor the "
            "matrix overlap Fix_D(rho)->Fix_B(rho)."
        ),
        outer_qft_factorization=(
            "Omega is a direct product of one S_n and K two-factor wreath "
            "groups, so its outer Fourier transform reduces to S_n QFTs and "
            "local swap-orbit resolution."
        ),
        multiplicity_obstruction=(
            "Exact double-coset and irrep-dimension sums show that low fixed-"
            "space multiplicity has negligible uniform dimension mass at the "
            "information width."
        ),
        native_occupied_rank=(
            "Exact first/second frame moments and Hilbert--Schmidt Cauchy--"
            "Schwarz show that occupied CS rank at most g^(K/4) carries "
            "negligible native regular-master frame mass."
        ),
        compiler_target=(
            "Construct a normalization-one coherent polar for the occupied "
            "D-fixed/B-fixed subduction overlap, preserving all multiplicity gauges."
        ),
        scope=(
            "No conditioned physical-sector transfer, subduction circuit, "
            "complete polar, classical separation, or speedup."
        ),
        theorem_verified=verified,
        status=(
            "orientation-polar-flattened-to-matrix-fixed-space-cs-transform"
            if verified
            else "orientation-homogeneous-space-control-failure"
        ),
    )
    return OrientationHomogeneousSpacePolarReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        native_occupied_rank_records=occupied,
        proof_obligations=[
            {
                "obligation": "flatten_all_orientations_to_one_homogeneous_incidence",
                "resolved": failures == 0,
                "resolution": (
                    "The quotient identifications and T=sqrt(2^K)J_B^*J_D "
                    "match direct coset synthesis exactly in three controls."
                ),
            },
            {
                "obligation": "localize_the_polar_to_fixed_space_cs_blocks",
                "resolved": True,
                "resolution": (
                    "Left Omega equivariance makes every Fourier block identity "
                    "on rows tensor the polar of Fix_D(rho)->Fix_B(rho)."
                ),
            },
            {
                "obligation": "rule_out_scalar_outer_label_filtering_on_typical_dimension_mass",
                "resolved": typical,
                "resolution": (
                    "The low-multiplicity dimension bounds are below 2^-8 from "
                    "n=5 onward and then decay rapidly on both quotient modules."
                ),
            },
            {
                "obligation": "prove_large_occupied_overlap_on_native_regular_master_mass",
                "resolved": occupied_verified,
                "resolution": (
                    "The exact first and second frame moments transfer the irrep-"
                    "dimension sum through Cauchy--Schwarz: blocks of occupied "
                    "rank at most g^(K/4) have negligible native frame mass."
                ),
            },
            {
                "obligation": "transfer_native_rank_to_conditioned_physical_sector_law",
                "resolved": False,
                "resolution": (
                    "The regular-master theorem is an annealed Plancherel trace "
                    "statement. A central-support/conditioning transfer is still "
                    "required for stronger per-sector claims."
                ),
            },
            {
                "obligation": "compile_normalization_one_fixed_space_cs_transform",
                "resolved": False,
                "resolution": (
                    "Need a coherent subduction/recoupling basis and direct polar, "
                    "not generic alternating reflections at inverse-factorial angle."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A product-group Fourier transform already diagonalizes the orientation polar.",
                "resolved": True,
                "resolution": (
                    "It removes the row action but leaves matrix fixed-space "
                    "overlaps; low multiplicity is negligible in uniform dimension."
                ),
            },
            {
                "objection": "Huge multiplicity proves that the polar is computationally hard.",
                "resolved": True,
                "resolution": (
                    "False. QFTs act on huge spaces. A succinct subduction basis "
                    "or fast CS transform remains possible."
                ),
            },
            {
                "objection": "The semidirect reformulation removes the square-root-width normalization by itself.",
                "resolved": True,
                "resolution": (
                    "False. It gives a flattened representation-specific target, "
                    "but generic projection/reflection methods still resolve the "
                    "small principal angles."
                ),
            },
            {
                "objection": "Uniform quotient dimension is automatically the native hidden-state law.",
                "resolved": True,
                "resolution": (
                    "False by itself. The separate exact frame-moment argument "
                    "does transfer to native regular-master mass, but not to a "
                    "conditioned per-sector central-support theorem."
                ),
            },
            {
                "objection": "Huge occupied CS rank proves circuit hardness.",
                "resolved": True,
                "resolution": (
                    "False. The occupied block can still admit a succinct "
                    "subduction basis and normalization-one transform."
                ),
            },
        ],
        headline_metrics={
            "single_homogeneous_incidence_theorem_count": int(failures == 0),
            "matrix_fixed_space_fourier_reduction_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_incidence_residual": max(
                row.maximum_homogeneous_incidence_residual for row in controls
            ),
            "maximum_equivariance_residual": max(
                row.maximum_left_equivariance_residual for row in controls
            ),
            "maximum_frame_moment_residual": max(
                row.maximum_frame_moment_residual for row in controls
            ),
            "matrix_multiplicity_scaling_record_count": len(scaling),
            "native_occupied_rank_scaling_record_count": len(occupied),
            "minimum_low_multiplicity_physical_log2_bound": min(
                row.low_multiplicity_physical_dimension_fraction_log2_upper_bound
                for row in scaling
            ),
            "minimum_low_multiplicity_source_log2_bound": min(
                row.low_multiplicity_source_dimension_fraction_log2_upper_bound
                for row in scaling
            ),
            "native_regular_master_occupied_rank_theorem_count": int(
                occupied_verified
            ),
            "minimum_high_occupied_rank_native_mass_lower_bound": min(
                row.high_occupied_rank_native_frame_mass_lower_bound
                for row in occupied
            ),
            "conditioned_physical_occupied_rank_theorem_count": 0,
            "normalization_one_fixed_space_cs_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orientation_family_is_one_semidirect_homogeneous_incidence": failures == 0,
            "complete_regular_master_polar_reduces_to_fixed_space_cs_blocks": failures == 0,
            "outer_semidirect_qft_scalarizes_fixed_space_overlap": False,
            "matrix_multiplicity_typical_in_uniform_quotient_dimension": typical,
            "occupied_overlap_high_rank_on_native_regular_master_mass": (
                occupied_verified
            ),
            "occupied_overlap_high_rank_on_native_pgm_mass": False,
            "normalization_one_fixed_space_cs_transform_compiled": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "mrs_escape_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The factorial orientation list is flattened to one structured "
                "matrix CS transform. Huge occupied rank is now proved on native "
                "regular-master mass, but the hard subduction polar, conditioned "
                "physical transfer, and every algorithmic gate remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Replaced the complete orientation list by one semidirect-product "
            "homogeneous incidence polar and isolated the only remaining quantum "
            "operation as a matrix fixed-space subduction/CS transform."
        ),
        falsifiers_triggered=[
            "The outer product/wreath Fourier transform does not reduce the natural polar to scalar eigenvalue filtering.",
            "Large fixed-space multiplicity is typical in uniform quotient dimension but is not a circuit lower bound.",
            "Low occupied CS rank has negligible native regular-master frame mass at information width.",
            "The homogeneous-space description removes explicit width enumeration, not the polar normalization problem.",
        ],
    )


def write_orientation_homogeneous_space_polar_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_orientation_homogeneous_space_polar())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_orientation_homogeneous_space_polar_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
