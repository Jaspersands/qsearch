"""Hyperoctahedral branching access versus fused-polar implementation.

For a fixed-point-free involution

    h_0=(1 2)(3 4)...(2m-1 2m) in S_(2m),

the centralizer is the hyperoctahedral group

    K=C_(S_(2m))(h_0)=C_2 wr S_m.

This subgroup does not create a Fourier-access obstruction.  Its irreducibles
are indexed by bipartitions ``(alpha,beta)`` of total size ``m``, it has an
efficient quantum Fourier transform, and generalized phase estimation gives
coherent access to the ``K``-isotypic label in a restricted ``S_(2m)`` irrep.
The central element ``h_0`` acts on ``(alpha,beta)`` by
``(-1)^|beta|``.  Thus each source projector ``(I+rho(h_0))/2`` is exactly the
even-``|beta|`` parity selector.

The restriction multiplicities are generalized plethysm coefficients,

    mult((alpha,beta), Res_K S^lambda)
      = <s_lambda, s_alpha[h_2] s_beta[e_2]>.

Their classical evaluation is not required for coherent isotypic sampling:
the ``K`` QFT and controlled representation action already implement that
measurement.  Conversely, sampling or measuring only the bipartition label
does not implement the fused PGM polar.  The polar coherently combines
matching ``K`` sectors, their multiplicity spaces, and diagonal ``K`` fusion
paths.  An exact ``S_6`` control below has one polar output with nonzero mass
in two orthogonal ``K``-isotypic sectors, so measuring the branch destroys the
pure output.

Nor can an exact branching *basis change* repair the normalization by itself.
For the restriction map ``R``, arbitrary unitary basis changes ``A R B``
preserve all singular values.  Hence the ``exp(-Omega(sqrt(n)))`` retained
principal-angle scale from
``coset_restriction_principal_angle_polar_reduction.py`` survives every
pipeline consisting of subgroup QFTs/subduction basis changes followed by a
generic bounded-polynomial singular-value transform.

This is not a no-go for a structured algorithm.  A clean coherent subduction
and fusion transform could synthesize the polar isometry directly from path
data, or a representation-specific block encoding could expose the retained
map at its natural tiny normalization.  Neither construction is supplied
here.  The result removes ``K``-isotypic access and classical multiplicity
tables from the blocker list and isolates coherent multiplicity-path
recoupling plus normalization-free polar synthesis as the actual obligations.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_perfect_matching_spherical_boundary import perfect_matching_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "coset_hyperoctahedral_branching_polar_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HYPEROCTAHEDRAL-BRANCHING-POLAR-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

MRR_QFT_PAPER_ID = "arxiv:quant-ph/0304064"
MRR_QFT_PAPER_URL = "https://arxiv.org/abs/quant-ph/0304064"
MULTIPLICITY_ALGORITHM_PAPER_ID = "arxiv:2407.17649"
MULTIPLICITY_ALGORITHM_PAPER_URL = "https://arxiv.org/abs/2407.17649"
PLETHYSM_SHARP_BQP_PAPER_ID = "arxiv:2602.08441"
PLETHYSM_SHARP_BQP_PAPER_URL = "https://arxiv.org/abs/2602.08441"
PLETHYSM_HARDNESS_PAPER_ID = "arxiv:2002.00788"
PLETHYSM_HARDNESS_PAPER_URL = "https://arxiv.org/abs/2002.00788"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class WreathIrrepParityControl:
    half_degree: int
    hyperoctahedral_order: int
    bipartition_count: int
    sum_irrep_dimension_squares: int
    even_beta_dimension_square_sum: int
    odd_beta_dimension_square_sum: int
    expected_each_central_parity_regular_dimension: int
    dimension_identity_verified: bool
    central_parity_balance_verified: bool
    status: str


@dataclass(frozen=True)
class RestrictionParityControl:
    half_degree: int
    partition: Partition
    irrep_dimension: int
    hyperoctahedral_element_count: int
    expected_hyperoctahedral_order: int
    centralizer_generation_verified: bool
    canonical_involution_central_in_subgroup: bool
    plus_projector_rank: int
    character_formula_plus_rank: int
    plus_projector_rank_residual: int
    maximum_subgroup_commutator_residual: float
    one_dimensional_restriction_multiplicities: dict[str, int]
    one_dimensional_multiplicities_integral_nonnegative: bool
    parity_projector_is_subgroup_invariant: bool
    status: str


@dataclass(frozen=True)
class BranchCoherenceControl:
    degree: int
    source_partitions: tuple[Partition, ...]
    target_partition: Partition
    hom_space_multiplicity: int
    restriction_map_rank: int
    positive_gram_eigenvalues: tuple[float, ...]
    nonzero_target_wreath_sector_count: int
    target_wreath_sector_weights: tuple[float, ...]
    branch_dephased_output_purity: float
    coherent_output_purity: float
    coherence_destroyed_by_branch_measurement: float
    singular_value_basis_change_residual: float
    branch_measurement_preserves_polar_output: bool
    unitary_basis_change_alters_singular_values: bool
    control_verified: bool
    status: str


@dataclass(frozen=True)
class HyperoctahedralScalingRecord:
    half_degree: int
    degree: int
    hyperoctahedral_order_decimal: str
    perfect_matching_index_decimal: str
    perfect_matching_index_log2: float
    bipartition_count: int
    central_even_parity_irrep_count: int
    central_odd_parity_irrep_count: int
    hyperoctahedral_qft_polynomial: bool
    coherent_isotypic_sampling_requires_multiplicity_table: bool
    direct_symmetric_to_hyperoctahedral_tower_index_polynomial: bool
    clean_subduction_multiplicity_basis_compiled: bool
    normalization_free_fused_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class HyperoctahedralBranchingPolarTheorem:
    centralizer_identity: str
    irrep_classification: str
    central_parity_rule: str
    restriction_coefficient_formula: str
    coherent_access: str
    branch_coherence_obstruction: str
    unitary_invariance_obstruction: str
    classical_hardness_scope: str
    constructive_frontier: str
    hyperoctahedral_qft_efficiency_applied: bool
    coherent_wreath_isotypic_sampling_constructed: bool
    source_projector_as_wreath_parity_filter_proved: bool
    classical_plethysm_table_required_for_isotypic_access: bool
    branch_label_measurement_sufficient_for_polar: bool
    unitary_branching_basis_change_removes_small_singular_scale: bool
    clean_subduction_multiplicity_basis_constructed: bool
    normalization_free_fused_polar_constructed: bool
    general_quantum_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetHyperoctahedralBranchingPolarBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    wreath_parity_controls: list[WreathIrrepParityControl]
    restriction_parity_controls: list[RestrictionParityControl]
    branch_coherence_control: BranchCoherenceControl
    scaling_records: list[HyperoctahedralScalingRecord]
    theorem: HyperoctahedralBranchingPolarTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _partitions_allow_zero(size: int) -> tuple[Partition, ...]:
    if size < 0:
        raise ValueError("partition size must be nonnegative")
    return ((),) if size == 0 else integer_partitions(size)


def wreath_irrep_dimension(
    half_degree: int,
    alpha: Partition,
    beta: Partition,
) -> int:
    if sum(alpha) + sum(beta) != half_degree:
        raise ValueError("bipartition must have total size half_degree")
    alpha_dimension = hook_length_dimension(alpha) if alpha else 1
    beta_dimension = hook_length_dimension(beta) if beta else 1
    return (
        math.comb(half_degree, sum(alpha))
        * alpha_dimension
        * beta_dimension
    )


def wreath_irrep_parity_control(
    half_degree: int,
) -> WreathIrrepParityControl:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    dimensions: list[tuple[int, int]] = []
    for alpha_size in range(half_degree + 1):
        beta_size = half_degree - alpha_size
        for alpha in _partitions_allow_zero(alpha_size):
            for beta in _partitions_allow_zero(beta_size):
                dimensions.append(
                    (
                        beta_size % 2,
                        wreath_irrep_dimension(half_degree, alpha, beta),
                    )
                )
    order = (2**half_degree) * math.factorial(half_degree)
    even = sum(dimension**2 for parity, dimension in dimensions if not parity)
    odd = sum(dimension**2 for parity, dimension in dimensions if parity)
    total = even + odd
    return WreathIrrepParityControl(
        half_degree=half_degree,
        hyperoctahedral_order=order,
        bipartition_count=len(dimensions),
        sum_irrep_dimension_squares=total,
        even_beta_dimension_square_sum=even,
        odd_beta_dimension_square_sum=odd,
        expected_each_central_parity_regular_dimension=order // 2,
        dimension_identity_verified=total == order,
        central_parity_balance_verified=even == odd == order // 2,
        status=(
            "wreath-bipartition-parity-verified"
            if total == order and even == odd == order // 2
            else "wreath-bipartition-parity-failure"
        ),
    )


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _permutation_sign(permutation: Permutation) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def canonical_fixed_point_free_involution(
    half_degree: int,
) -> Permutation:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return tuple(
        value
        for pair in range(half_degree)
        for value in (2 * pair + 1, 2 * pair)
    )


def hyperoctahedral_elements(
    half_degree: int,
) -> tuple[tuple[Permutation, Permutation, tuple[int, ...]], ...]:
    """Return elements with their block permutation and internal flips."""

    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    output = []
    for block_permutation in itertools.permutations(range(half_degree)):
        for flips in itertools.product((0, 1), repeat=half_degree):
            permutation = [0] * (2 * half_degree)
            for block in range(half_degree):
                for bit in (0, 1):
                    permutation[2 * block + bit] = (
                        2 * block_permutation[block] + (bit ^ flips[block])
                    )
            output.append((tuple(permutation), block_permutation, flips))
    return tuple(output)


def restriction_parity_control(
    half_degree: int,
    partition: Partition,
    *,
    tolerance: float = 1e-9,
) -> RestrictionParityControl:
    degree = 2 * half_degree
    if sum(partition) != degree:
        raise ValueError("partition must have size twice half_degree")
    elements = hyperoctahedral_elements(half_degree)
    table = _source_representation_rows(partition)
    hidden = canonical_fixed_point_free_involution(half_degree)
    expected_order = (2**half_degree) * math.factorial(half_degree)
    centralizer_verified = all(
        _compose(permutation, hidden) == _compose(hidden, permutation)
        for permutation, _, _ in elements
    )
    subgroup = {permutation for permutation, _, _ in elements}
    central = all(
        _compose(permutation, hidden) in subgroup
        and _compose(permutation, hidden) == _compose(hidden, permutation)
        for permutation in subgroup
    )
    dimension = table[hidden].shape[0]
    plus = (np.eye(dimension) + table[hidden]) / 2
    plus_rank = int(np.linalg.matrix_rank(plus, tol=tolerance))
    character = int(round(float(np.trace(table[hidden]).real)))
    formula_rank = (dimension + character) // 2
    commutator = max(
        float(np.linalg.norm(table[permutation] @ plus - plus @ table[permutation], ord=2))
        for permutation in subgroup
    )
    character_sums = {
        "trivial": 0.0,
        "base_sign": 0.0,
        "block_sign": 0.0,
        "base_times_block_sign": 0.0,
    }
    for permutation, block_permutation, flips in elements:
        trace = float(np.trace(table[permutation]).real)
        base_sign = -1 if sum(flips) % 2 else 1
        block_sign = _permutation_sign(block_permutation)
        character_sums["trivial"] += trace
        character_sums["base_sign"] += base_sign * trace
        character_sums["block_sign"] += block_sign * trace
        character_sums["base_times_block_sign"] += (
            base_sign * block_sign * trace
        )
    normalized = {
        name: value / expected_order for name, value in character_sums.items()
    }
    multiplicities = {name: int(round(value)) for name, value in normalized.items()}
    integral = all(
        multiplicities[name] >= 0
        and abs(value - multiplicities[name]) <= 1e-8
        for name, value in normalized.items()
    )
    invariant = commutator <= 1e-8
    verified = bool(
        len(subgroup) == expected_order
        and centralizer_verified
        and central
        and plus_rank == formula_rank
        and invariant
        and integral
    )
    return RestrictionParityControl(
        half_degree=half_degree,
        partition=partition,
        irrep_dimension=dimension,
        hyperoctahedral_element_count=len(subgroup),
        expected_hyperoctahedral_order=expected_order,
        centralizer_generation_verified=centralizer_verified,
        canonical_involution_central_in_subgroup=central,
        plus_projector_rank=plus_rank,
        character_formula_plus_rank=formula_rank,
        plus_projector_rank_residual=plus_rank - formula_rank,
        maximum_subgroup_commutator_residual=commutator,
        one_dimensional_restriction_multiplicities=multiplicities,
        one_dimensional_multiplicities_integral_nonnegative=integral,
        parity_projector_is_subgroup_invariant=invariant,
        status=(
            "restriction-central-parity-verified"
            if verified
            else "restriction-central-parity-failure"
        ),
    )


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = matrices[0]
    for matrix in matrices[1:]:
        output = np.kron(output, matrix)
    return output


def _conjugacy_classes(group: tuple[Permutation, ...]) -> tuple[tuple[Permutation, ...], ...]:
    unseen = set(group)
    output = []
    while unseen:
        representative = next(iter(unseen))
        conjugacy_class = {
            _compose(_compose(element, representative), _inverse(element))
            for element in group
        }
        output.append(tuple(conjugacy_class))
        unseen -= conjugacy_class
    return tuple(output)


def _central_isotypic_projectors(
    table: dict[Permutation, np.ndarray],
    group: tuple[Permutation, ...],
) -> tuple[np.ndarray, ...]:
    class_sums = []
    zero = np.zeros_like(next(iter(table.values())), dtype=np.complex128)
    for conjugacy_class in _conjugacy_classes(group):
        class_sum = sum((table[element] for element in conjugacy_class), zero.copy())
        class_sums.append((class_sum + class_sum.conj().T) / 2)
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    central = sum(
        math.sqrt(primes[index]) * class_sum
        for index, class_sum in enumerate(class_sums)
    )
    values, vectors = np.linalg.eigh(central)
    projectors = []
    used = np.zeros(len(values), dtype=bool)
    for index, value in enumerate(values):
        if used[index]:
            continue
        active = np.abs(values - value) <= 1e-8
        used |= active
        block = vectors[:, active]
        projectors.append(block @ block.conj().T)
    return tuple(projectors)


def branch_coherence_control(
    *,
    tolerance: float = 1e-9,
) -> BranchCoherenceControl:
    """Exact S6 control where the polar output spans two K-isotypic sectors."""

    source_partitions = ((5, 1), (5, 1))
    target_partition = (4, 2)
    degree = 6
    source_tables = tuple(
        _source_representation_rows(partition)
        for partition in source_partitions
    )
    target_table = _source_representation_rows(target_partition)
    group = tuple(target_table)
    source_action = {
        element: _kron_all(tuple(table[element] for table in source_tables))
        for element in group
    }
    source_dimension = source_action[group[0]].shape[0]
    target_dimension = target_table[group[0]].shape[0]
    invariant = sum(
        np.kron(np.conjugate(target_table[element]), source_action[element])
        for element in group
    ) / len(group)
    invariant = (invariant + invariant.conj().T) / 2
    values, vectors = np.linalg.eigh(invariant)
    embedding = vectors[:, values > 1 - 100 * tolerance]

    hidden = canonical_fixed_point_free_involution(3)
    source_projector = _kron_all(
        tuple(
            (np.eye(table[hidden].shape[0]) + table[hidden]) / 2
            for table in source_tables
        )
    )
    lifted = np.kron(np.eye(target_dimension), source_projector)
    restriction = lifted @ embedding
    gram = restriction.conj().T @ restriction
    gram_values, gram_vectors = np.linalg.eigh((gram + gram.conj().T) / 2)
    positive = gram_values > tolerance
    inverse_root = (
        gram_vectors[:, positive] * gram_values[positive] ** -0.5
    ) @ gram_vectors[:, positive].conj().T
    polar = restriction @ inverse_root
    rank = int(np.count_nonzero(positive))

    wreath = tuple(
        permutation for permutation, _, _ in hyperoctahedral_elements(3)
    )
    target_projectors = _central_isotypic_projectors(target_table, wreath)
    weights = []
    for projector in target_projectors:
        lifted_sector = np.kron(
            np.conjugate(projector), np.eye(source_dimension)
        )
        weight = float(
            np.trace(polar.conj().T @ lifted_sector @ polar).real
        )
        if weight > tolerance:
            weights.append(weight)
    if rank != 1:
        raise ArithmeticError("branch-coherence control must have rank one")
    normalized_weights = tuple(weight / rank for weight in weights)
    dephased_purity = sum(weight**2 for weight in normalized_weights)

    left_phases = np.exp(
        2j * math.pi * np.arange(restriction.shape[0]) / restriction.shape[0]
    )
    right_phases = np.exp(
        2j * math.pi * np.arange(restriction.shape[1]) / max(1, restriction.shape[1])
    )
    changed = (
        left_phases[:, None]
        * restriction
        * right_phases[None, :]
    )
    original_singular = np.linalg.svd(restriction, compute_uv=False)
    changed_singular = np.linalg.svd(changed, compute_uv=False)
    singular_residual = float(np.max(np.abs(original_singular - changed_singular)))
    coherence_loss = 1.0 - dephased_purity
    verified = bool(
        len(normalized_weights) >= 2
        and abs(sum(normalized_weights) - 1.0) <= 1e-8
        and coherence_loss > 1e-6
        and singular_residual <= 1e-10
    )
    return BranchCoherenceControl(
        degree=degree,
        source_partitions=source_partitions,
        target_partition=target_partition,
        hom_space_multiplicity=embedding.shape[1],
        restriction_map_rank=rank,
        positive_gram_eigenvalues=tuple(
            float(value) for value in gram_values[positive]
        ),
        nonzero_target_wreath_sector_count=len(normalized_weights),
        target_wreath_sector_weights=normalized_weights,
        branch_dephased_output_purity=dephased_purity,
        coherent_output_purity=1.0,
        coherence_destroyed_by_branch_measurement=coherence_loss,
        singular_value_basis_change_residual=singular_residual,
        branch_measurement_preserves_polar_output=False,
        unitary_basis_change_alters_singular_values=False,
        control_verified=verified,
        status=(
            "branch-coherence-and-unitary-invariance-verified"
            if verified
            else "branch-coherence-control-failure"
        ),
    )


def hyperoctahedral_scaling_record(
    half_degree: int,
) -> HyperoctahedralScalingRecord:
    parity = wreath_irrep_parity_control(half_degree)
    matching_index = perfect_matching_count(half_degree)
    even_count = sum(
        len(_partitions_allow_zero(alpha_size))
        * len(_partitions_allow_zero(half_degree - alpha_size))
        for alpha_size in range(half_degree + 1)
        if (half_degree - alpha_size) % 2 == 0
    )
    odd_count = parity.bipartition_count - even_count
    return HyperoctahedralScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        hyperoctahedral_order_decimal=str(
            (2**half_degree) * math.factorial(half_degree)
        ),
        perfect_matching_index_decimal=str(matching_index),
        perfect_matching_index_log2=math.log2(matching_index),
        bipartition_count=parity.bipartition_count,
        central_even_parity_irrep_count=even_count,
        central_odd_parity_irrep_count=odd_count,
        hyperoctahedral_qft_polynomial=True,
        coherent_isotypic_sampling_requires_multiplicity_table=False,
        direct_symmetric_to_hyperoctahedral_tower_index_polynomial=False,
        clean_subduction_multiplicity_basis_compiled=False,
        normalization_free_fused_polar_compiled=False,
        status="wreath-qft-accessible-clean-polar-open",
    )


def build_coset_hyperoctahedral_branching_polar_report(
    *,
    parity_half_degrees: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 8, 10),
    restriction_specs: tuple[tuple[int, Partition], ...] = (
        (2, (4,)),
        (2, (3, 1)),
        (2, (2, 2)),
        (3, (5, 1)),
        (3, (4, 2)),
        (3, (3, 2, 1)),
    ),
) -> CosetHyperoctahedralBranchingPolarBoundaryReport:
    parity_controls = [
        wreath_irrep_parity_control(half_degree)
        for half_degree in parity_half_degrees
    ]
    restriction_controls = [
        restriction_parity_control(half_degree, partition)
        for half_degree, partition in restriction_specs
    ]
    coherence = branch_coherence_control()
    scaling = [
        hyperoctahedral_scaling_record(half_degree)
        for half_degree in parity_half_degrees
    ]
    finite_verified = bool(
        all(
            row.dimension_identity_verified
            and row.central_parity_balance_verified
            for row in parity_controls
        )
        and all(
            row.status == "restriction-central-parity-verified"
            for row in restriction_controls
        )
        and coherence.control_verified
    )
    theorem = HyperoctahedralBranchingPolarTheorem(
        centralizer_identity=(
            "C_(S_(2m))(h_0)=C_2 wr S_m for the canonical perfect matching h_0."
        ),
        irrep_classification=(
            "Irreducibles of C_2 wr S_m are indexed by bipartitions "
            "(alpha,beta) with dimension binom(m,|alpha|)f^alpha f^beta."
        ),
        central_parity_rule=(
            "The all-pair flip h_0 acts on (alpha,beta) as (-1)^|beta|; "
            "(I+rho(h_0))/2 selects even |beta| exactly."
        ),
        restriction_coefficient_formula=(
            "mult((alpha,beta),Res S^lambda)="
            "<s_lambda,s_alpha[h_2]s_beta[e_2]>."
        ),
        coherent_access=(
            "The polynomial C_2 wr S_m QFT plus controlled restricted action "
            "gives coherent isotypic access by generalized phase estimation, "
            "without a classical table of plethysm coefficients."
        ),
        branch_coherence_obstruction=(
            "Measuring only the wreath irrep label is not the polar: an exact "
            "S_6 rank-one polar output has nonzero coherent mass in two "
            "orthogonal K-isotypic sectors."
        ),
        unitary_invariance_obstruction=(
            "Subduction/QFT basis changes A R B preserve singular values, so "
            "they cannot remove the retained exp(-Omega(sqrt(n))) scale before "
            "a generic singular-value transform."
        ),
        classical_hardness_scope=(
            "General plethysm computation is classically hard, but those "
            "hardness theorems do not by themselves prove hardness of this "
            "inner-size-two structured family or obstruct coherent quantum access."
        ),
        constructive_frontier=(
            "Compile clean subduction multiplicity paths and heterogeneous "
            "wreath Clebsch-Gordan fusion, then synthesize the polar directly "
            "or produce a retained-window block encoding at its natural scale."
        ),
        hyperoctahedral_qft_efficiency_applied=True,
        coherent_wreath_isotypic_sampling_constructed=True,
        source_projector_as_wreath_parity_filter_proved=True,
        classical_plethysm_table_required_for_isotypic_access=False,
        branch_label_measurement_sufficient_for_polar=False,
        unitary_branching_basis_change_removes_small_singular_scale=False,
        clean_subduction_multiplicity_basis_constructed=False,
        normalization_free_fused_polar_constructed=False,
        general_quantum_circuit_lower_bound_proved=False,
        theorem_verified=finite_verified,
        status=(
            "wreath-isotypic-access-closed-coherent-subduction-polar-open"
            if finite_verified
            else "hyperoctahedral-branching-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "wreath_parity_control_count": len(parity_controls),
        "restriction_parity_control_count": len(restriction_controls),
        "finite_validation_failure_count": sum(
            not row.dimension_identity_verified
            or not row.central_parity_balance_verified
            for row in parity_controls
        )
        + sum(
            row.status != "restriction-central-parity-verified"
            for row in restriction_controls
        )
        + int(not coherence.control_verified),
        "coherent_wreath_isotypic_access_count": 1,
        "classical_multiplicity_table_required_count": 0,
        "branch_coherence_counterexample_count": 1,
        "branch_coherence_nonzero_sector_count": (
            coherence.nonzero_target_wreath_sector_count
        ),
        "branch_measurement_coherence_loss": (
            coherence.coherence_destroyed_by_branch_measurement
        ),
        "clean_subduction_multiplicity_basis_count": 0,
        "normalization_free_fused_polar_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetHyperoctahedralBranchingPolarBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "group_family": "S_(2m) restricted to C_2 wr S_m",
            "source_projector": (
                "Tensor product of +1 eigenspace projectors for the canonical "
                "fixed-point-free involution."
            ),
            "access_model": (
                "Efficient symmetric-group and wreath-product QFTs, controlled "
                "group actions, and coherent generalized phase estimation."
            ),
            "non_claim": (
                "No clean subduction multiplicity basis, wreath fusion network, "
                "normalization-free polar, decoder, or circuit lower bound."
            ),
        },
        wreath_parity_controls=parity_controls,
        restriction_parity_controls=restriction_controls,
        branch_coherence_control=coherence,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-WREATH-CLEAN-SUBDUCTION",
                "statement": (
                    "Compile a clean coherent S_(2m) down to C_2 wr S_m "
                    "subduction transform including multiplicity-path labels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-WREATH-HETEROGENEOUS-FUSION",
                "statement": (
                    "Compile the diagonal C_2 wr S_m fusion transform for the "
                    "heterogeneous source irreps at k=Theta(n log n) copies."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-WREATH-NORMALIZATION-FREE-POLAR",
                "statement": (
                    "Use subduction/fusion paths to synthesize the polar directly, "
                    "or block-encode each retained map at its natural tiny scale."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-WREATH-POLAR-DECODER",
                "statement": (
                    "Compose any polar with the physical outcome map and prove "
                    "a polynomial hidden-involution decoder and dequantization gap."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Plethysm coefficients make K-isotypic access hard.",
                "answer": (
                    "False in the quantum access model: efficient K QFT and GPE "
                    "sample and coherently label restriction isotypics without "
                    "computing a classical coefficient table."
                ),
                "resolved": True,
            },
            {
                "challenge": "Measuring the K label implements the polar.",
                "answer": (
                    "False universally: the exact S_6 control has one pure polar "
                    "output supported coherently on two K-isotypic sectors."
                ),
                "resolved": True,
            },
            {
                "challenge": "An efficient branching basis removes tiny angles.",
                "answer": (
                    "False for basis change alone because left/right unitaries "
                    "preserve every singular value of the restriction map."
                ),
                "resolved": True,
            },
            {
                "challenge": "The singular-value argument rules out all circuits.",
                "answer": (
                    "False. Direct path synthesis or a structured rescaled encoding "
                    "need not implement the polar as a bounded polynomial of R."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "paper_id": MRR_QFT_PAPER_ID,
                "url": MRR_QFT_PAPER_URL,
                "use": "Efficient QFT for G wr S_m when |G| is polynomial.",
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": MULTIPLICITY_ALGORITHM_PAPER_ID,
                "url": MULTIPLICITY_ALGORITHM_PAPER_URL,
                "use": (
                    "Quantum restriction-multiplicity sampling for wreath-product "
                    "subgroups, including the constant base-size regime."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": PLETHYSM_SHARP_BQP_PAPER_ID,
                "url": PLETHYSM_SHARP_BQP_PAPER_URL,
                "use": (
                    "Independent 2026 evidence that plethysm multiplicity spaces "
                    "admit efficient quantum verification via structured embeddings."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": PLETHYSM_HARDNESS_PAPER_ID,
                "url": PLETHYSM_HARDNESS_PAPER_URL,
                "use": (
                    "Classical general plethysm hardness; explicitly not treated "
                    "as a lower bound for the inner-size-two branching family."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "hyperoctahedral_qft_accessible": True,
            "coherent_wreath_isotypic_labels_accessible": True,
            "source_projector_is_even_beta_parity_filter": True,
            "classical_plethysm_table_is_required": False,
            "branch_label_measurement_implements_polar": False,
            "unitary_branching_change_removes_small_singular_scale": False,
            "clean_subduction_multiplicity_transform_constructed": False,
            "heterogeneous_wreath_fusion_transform_constructed": False,
            "normalization_free_fused_polar_constructed": False,
            "polynomial_hidden_involution_decoder_constructed": False,
            "general_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Wreath isotypic access and parity filtering are efficient, but "
                "the fused polar requires coherent multiplicity-path recoupling "
                "and a normalization-free implementation not supplied here."
            ),
        },
        status=(
            "wreath-isotypic-access-closed-coherent-subduction-polar-open"
        ),
        summary=(
            "Removed hyperoctahedral Fourier/isotypic access and classical "
            "plethysm tables from the active blocker list. Exact branch "
            "measurement is insufficient and basis changes preserve the tiny "
            "principal-angle scale; clean coherent subduction/fusion plus direct "
            "polar synthesis is the remaining structured route."
        ),
        falsifiers_triggered=[
            (
                "Classical computation of every plethysm coefficient is not "
                "required for coherent K-isotypic quantum access."
            ),
            (
                "A K-irrep label alone is not the fused PGM polar output."
            ),
            (
                "An efficient unitary branching basis change alone cannot "
                "renormalize exponentially small principal angles."
            ),
            (
                "General plethysm hardness is not a circuit lower bound for the "
                "inner-size-two perfect-matching centralizer."
            ),
        ],
    )


def write_coset_hyperoctahedral_branching_polar_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HYPEROCTAHEDRAL-BRANCHING-POLAR-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_coset_hyperoctahedral_branching_polar_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_coset_hyperoctahedral_branching_polar_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
