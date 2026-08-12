"""Point-stabilizer quotient of the retained joint-character state.

The carrier-traced joint register ``tau_g`` contains only subextensive
one-block information for natural threshold sources.  Subextensive information
could nevertheless be useful if one block predicts one image ``g(0)`` and the
procedure can be repeated down the stabilizer chain

    S_n > S_(n-1) > ... > S_2.

This module identifies the exact representation-theoretic target for that
strategy.  Put ``H=Stab(0)`` and

    omega_j = |H|^-1 sum_(g:g(0)=j) tau_g.

The family is ``S_n``-covariant and its centered linear span is either zero or
one copy of the standard representation.  Consequently its Hilbert--Schmidt
Gram matrix is exactly isotropic:

    <Delta_j,Delta_l> = d                         if j=l,
                       -d/(n-1)                  otherwise,

where ``Delta_j=omega_j-bar(omega)``.  This does *not* mean that the density
operators occupy only the standard Fourier irrep.  In the group Fourier basis,
the seed is an ``H``-twirl.  Young branching gives the correct locality rule:
the ``(nu,mu)`` Fourier block vanishes unless ``nu`` and ``mu`` share a child
partition of ``n-1``.  Thus point information is an operator-valued standard
harmonic spread over a sparse Young-graph neighborhood.

The module also derives an exact overlap kernel.  For fixed source pairs let
``r_lambda`` denote normalized characters and define

    Q_i(s,t,u) = r_l(s^-1 t)^2 + r_m(s^-1 t)^2
      + r_l(s)r_m(t)r_l(u^-1 s)r_m(t^-1 u)
      + r_m(s)r_l(t)r_m(u^-1 s)r_l(t^-1 u).

Then

    K(u)=Tr(tau_e tau_u)
        = |G|^-2 4^-k sum_(s,t) product_i Q_i(s,t,u).       (1)

For unrestricted independent Plancherel labels, character column orthogonality
replaces the cross character product by

    c(x,y)=1[x and y are conjugate]/|Cl(x)|,

and gives

    E K(u)=|G|^-2 2^-k sum_(s,t)
      [a_(s^-1t)+c(s,u^-1s)c(t,t^-1u)]^k,                 (2)

where ``a_x=1/|Cl(x)|``.  The point signal is exactly the standard-character
coefficient

    E ||omega_0-bar(omega)||_2^2
      = |G|^-1 sum_u (fix(u)-1) E K(u).                    (3)

Small exact controls through ``S_6`` show rapid decay of the normalized signal,
but that is evidence rather than an asymptotic theorem.  The formula is not a
collision-free conditional average.  Although collision failure has vanishing
probability, that only gives additive control and cannot preserve a lower bound
that may itself be much smaller than the failure probability.

Finally, an ``S_m``-covariant point decoder with success
``1/m+delta_m`` has uniform wrong-output probability and plurality margin at
least ``delta_m``.  Independent repetition therefore amplifies it using
``O(delta_m^-2 log(m/epsilon))`` fresh blocks.  If such a decoder and fresh
subgroup-native state preparation are efficient at every stabilizer level,
full hidden permutation recovery is polynomial.  Those hypotheses, especially
an inverse-polynomial natural ``delta_m`` and coherent multiplicity whitening,
remain open.  No algorithmic speedup is claimed.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_coherent_fourier_decoder import symmetric_group_fourier_matrix
from self_dual_wreath_joint_character_correlation_decoder import (
    _partial_trace_character,
    _partial_trace_group,
    _permutations,
    _pretty_good_success,
    _von_neumann_entropy,
    inverse_permutation,
    joint_character_state,
    left_covariant_state,
)
from self_dual_wreath_joint_character_purity_decoupling import normalized_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_point_stabilizer_quotient.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POINT-STABILIZER-QUOTIENT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PointQuotientControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    point_stabilizer_order: int
    copy_count: int
    orientation_count: int
    quotient_hypothesis_count: int
    maximum_covariance_residual: float
    maximum_group_marginal_variation: float
    maximum_character_marginal_variation: float
    centered_hilbert_schmidt_norm_squared: float
    centered_gram_isotropy_residual: float
    centered_state_span_rank: int
    expected_standard_span_rank: int
    allowed_young_irrep_pair_count: int
    active_allowed_young_irrep_pair_count: int
    active_nonstandard_young_irrep_pair_count: int
    maximum_forbidden_young_block_norm: float
    point_holevo_information_bits: float
    hidden_point_entropy_bits: float
    point_pretty_good_success: float
    random_guess_success: float
    pretty_good_excess: float
    wrong_output_probability: float
    covariance_error_law_residual: float
    fixed_tuple_overlap_formula_residual: float
    fixed_tuple_overlap_class_residual: float
    exact_point_quotient_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalPointSignalControl:
    n: int
    copy_count: int
    group_order: int
    orientation_count: int
    partition_count: int
    expected_native_state_purity: float
    expected_point_state_purity: float
    expected_average_state_purity: float
    expected_centered_hilbert_schmidt_norm_squared: float
    normalized_expected_centered_signal: float
    expected_pair_hilbert_schmidt_distance_squared: float
    expected_success_excess_trace_norm_upper_bound: float
    subgroup_average_standard_coefficient_residual: float
    nonnegative_signal_verified: bool
    collision_free_conditioned_signal_formula_proved: bool
    asymptotic_inverse_polynomial_signal_proved: bool
    status: str


@dataclass(frozen=True)
class YoungEdgeScalingRecord:
    n: int
    irrep_count: int
    young_child_count: int
    allowed_ordered_irrep_pair_count: int
    maximum_allowed_neighbor_count: int
    total_ordered_irrep_pair_count: int
    allowed_pair_fraction: float
    maximum_removable_corner_count: int
    maximum_addable_parent_count: int
    local_young_edge_navigation_polynomial: bool
    simultaneous_multiplicity_whitening_proved: bool
    status: str


@dataclass(frozen=True)
class StabilizerChainReductionRecord:
    n: int
    stabilizer_stage_count: int
    required_point_success: str
    covariant_wrong_output_law: str
    plurality_margin: str
    repetitions_per_stage: str
    fresh_subgroup_native_blocks_required: bool
    public_oracle_restriction_required: bool
    inverse_polynomial_point_excess_suffices: bool
    recursive_full_recovery_reduction_proved: bool
    inverse_polynomial_natural_point_excess_proved: bool
    efficient_point_measurement_proved: bool
    polynomial_full_hidden_shift_algorithm_proved: bool
    status: str


@dataclass(frozen=True)
class PointStabilizerQuotientTheorem:
    quotient_state: str
    isotropic_standard_geometry: str
    young_edge_fourier_locality: str
    fixed_tuple_overlap: str
    natural_overlap: str
    standard_signal_coefficient: str
    recursive_reduction: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointStabilizerQuotientReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointStabilizerQuotientTheorem
    finite_controls: list[PointQuotientControl]
    natural_signal_controls: list[NaturalPointSignalControl]
    young_edge_scaling_records: list[YoungEdgeScalingRecord]
    stabilizer_chain_reductions: list[StabilizerChainReductionRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def removable_children(partition: Partition) -> tuple[Partition, ...]:
    """Return the Young diagrams obtained by removing one corner box."""

    if not partition or any(part <= 0 for part in partition):
        raise ValueError("partition must contain positive parts")
    children = []
    for row, length in enumerate(partition):
        next_length = partition[row + 1] if row + 1 < len(partition) else 0
        if length <= next_length:
            continue
        child = list(partition)
        child[row] -= 1
        if child[row] == 0:
            child.pop(row)
        children.append(tuple(child))
    return tuple(children)


def share_young_child(left: Partition, right: Partition) -> bool:
    if sum(left) != sum(right):
        return False
    return bool(set(removable_children(left)) & set(removable_children(right)))


def point_quotient_states(
    labels: tuple[Label, ...],
    *,
    point: int = 0,
) -> tuple[np.ndarray, ...]:
    """Return ``omega_j`` for all possible images of ``point``."""

    if not labels:
        raise ValueError("at least one source pair is required")
    n = sum(labels[0][0])
    if point < 0 or point >= n:
        raise ValueError("point out of range")
    if any(sum(left) != n or sum(right) != n for left, right in labels):
        raise ValueError("all source partitions must have the same degree")
    permutations = _permutations(n)
    character_count = 1 << len(labels)
    base = joint_character_state(labels, tuple(range(n)))
    states = tuple(
        left_covariant_state(base, permutations, hidden, character_count)
        for hidden in permutations
    )
    zero = np.zeros_like(base)
    subgroup_order = math.factorial(n - 1)
    return tuple(
        sum(
            (
                states[index]
                for index, hidden in enumerate(permutations)
                if hidden[point] == image
            ),
            zero.copy(),
        )
        / subgroup_order
        for image in range(n)
    )


def point_centered_gram(states: tuple[np.ndarray, ...]) -> np.ndarray:
    if len(states) < 2:
        raise ValueError("at least two point states are required")
    average = sum(states) / len(states)
    centered = tuple(state - average for state in states)
    return np.asarray(
        [
            [float(np.trace(left @ right).real) for right in centered]
            for left in centered
        ]
    )


def _pretty_good_confusion(
    states: tuple[np.ndarray, ...],
    tolerance: float,
) -> np.ndarray:
    count = len(states)
    average = sum(states) / count
    eigenvalues, eigenvectors = np.linalg.eigh(
        (average + average.conj().T) / 2
    )
    positive = eigenvalues > tolerance
    inverse = (
        eigenvectors[:, positive] * eigenvalues[positive] ** -0.5
    ) @ eigenvectors[:, positive].conj().T
    effects = tuple(inverse @ state @ inverse / count for state in states)
    return np.asarray(
        [
            [float(np.trace(effect @ state).real) for effect in effects]
            for state in states
        ]
    )


@lru_cache(maxsize=None)
def _group_combinatorics(
    n: int,
) -> tuple[
    tuple[Permutation, ...],
    dict[Permutation, int],
    tuple[Permutation, ...],
    tuple[Partition, ...],
    dict[Partition, int],
    np.ndarray,
]:
    permutations = _permutations(n)
    index = {permutation: position for position, permutation in enumerate(permutations)}
    inverses = tuple(inverse_permutation(permutation) for permutation in permutations)
    cycle_types = tuple(permutation_cycle_type(permutation) for permutation in permutations)
    class_sizes = dict(Counter(cycle_types))
    relative = np.empty((len(permutations), len(permutations)), dtype=np.int32)
    for left, inverse in enumerate(inverses):
        relative[left] = [
            index[compose_permutations(inverse, right)]
            for right in permutations
        ]
    return permutations, index, inverses, cycle_types, class_sizes, relative


def fixed_tuple_overlap_kernel(
    n: int,
    labels: tuple[Label, ...],
) -> dict[Partition, float]:
    """Evaluate (1), one representative per conjugacy class."""

    if not labels or any(
        sum(left) != n or sum(right) != n for left, right in labels
    ):
        raise ValueError("source labels must be nonempty partition pairs of n")
    permutations, index, inverses, cycles, _, relative = _group_combinatorics(n)
    representatives: dict[Partition, int] = {}
    for position, cycle in enumerate(cycles):
        representatives.setdefault(cycle, position)
    character_ratios = {
        partition: np.asarray(
            [normalized_character(partition, cycle) for cycle in cycles],
            dtype=float,
        )
        for pair in labels
        for partition in pair
    }
    order = len(permutations)
    values: dict[Partition, float] = {}
    for cycle, position in representatives.items():
        hidden = permutations[position]
        inverse_hidden = inverses[position]
        inverse_hidden_left = np.asarray(
            [
                index[compose_permutations(inverse_hidden, source)]
                for source in permutations
            ]
        )
        inverse_right_hidden = np.asarray(
            [
                index[compose_permutations(inverse, hidden)]
                for inverse in inverses
            ]
        )
        local_product = np.ones((order, order), dtype=float)
        for left, right in labels:
            left_ratio = character_ratios[left]
            right_ratio = character_ratios[right]
            diagonal = (
                left_ratio[relative] ** 2 + right_ratio[relative] ** 2
            )
            cross = (
                left_ratio[:, None]
                * right_ratio[None, :]
                * left_ratio[inverse_hidden_left, None]
                * right_ratio[None, inverse_right_hidden]
                + right_ratio[:, None]
                * left_ratio[None, :]
                * right_ratio[inverse_hidden_left, None]
                * left_ratio[None, inverse_right_hidden]
            )
            local_product *= diagonal + cross
        values[cycle] = float(
            np.sum(local_product) / (order * order * 4 ** len(labels))
        )
    return values


def natural_annealed_overlap_kernel(
    n: int,
    copy_count: int,
) -> dict[Partition, float]:
    """Evaluate the Plancherel expectation (2) by conjugacy class."""

    if n < 2 or copy_count < 1:
        raise ValueError("invalid degree or copy count")
    permutations, index, inverses, cycles, class_sizes, relative = (
        _group_combinatorics(n)
    )
    order = len(permutations)
    inverse_class_sizes = np.asarray(
        [1 / class_sizes[cycle] for cycle in cycles],
        dtype=float,
    )
    base = inverse_class_sizes[relative]
    representatives: dict[Partition, int] = {}
    for position, cycle in enumerate(cycles):
        representatives.setdefault(cycle, position)
    values: dict[Partition, float] = {}
    for cycle, position in representatives.items():
        hidden = permutations[position]
        inverse_hidden = inverses[position]
        left_correlation = np.zeros(order)
        right_correlation = np.zeros(order)
        for source_index, source in enumerate(permutations):
            product = compose_permutations(inverse_hidden, source)
            product_index = index[product]
            if cycles[source_index] == cycles[product_index]:
                left_correlation[source_index] = inverse_class_sizes[source_index]
        for target_index, inverse in enumerate(inverses):
            product = compose_permutations(inverse, hidden)
            product_index = index[product]
            if cycles[target_index] == cycles[product_index]:
                right_correlation[target_index] = inverse_class_sizes[target_index]
        local = base + left_correlation[:, None] * right_correlation[None, :]
        values[cycle] = float(
            np.sum(np.power(local, copy_count))
            / (order * order * 2**copy_count)
        )
    return values


def _class_centralizer_size(cycle_type: Partition) -> int:
    multiplicities = Counter(cycle_type)
    return math.prod(
        length**count * math.factorial(count)
        for length, count in multiplicities.items()
    )


def audit_natural_point_signal(
    n: int,
    copy_count: int | None = None,
    *,
    tolerance: float = 1e-12,
) -> NaturalPointSignalControl:
    copies = copy_count or math.ceil(math.lgamma(n + 1) / math.log(2))
    kernel = natural_annealed_overlap_kernel(n, copies)
    order = math.factorial(n)
    orientation_count = 1 << copies
    group_average = sum(
        (order // _class_centralizer_size(cycle)) * value
        for cycle, value in kernel.items()
    ) / order
    subgroup_order = math.factorial(n - 1)
    subgroup_average = sum(
        (subgroup_order // _class_centralizer_size(child))
        * kernel[tuple(sorted((*child, 1), reverse=True))]
        for child in integer_partitions(n - 1)
    ) / subgroup_order
    standard_coefficient = sum(
        (order // _class_centralizer_size(cycle))
        * (cycle.count(1) - 1)
        * value
        for cycle, value in kernel.items()
    ) / order
    centered = subgroup_average - group_average
    pair_distance = 2 * n * centered / (n - 1)
    normalized = order * orientation_count * centered
    trace_bound = min(1.0, 0.5 * math.sqrt(max(0.0, normalized)))
    residual = abs(centered - standard_coefficient)
    return NaturalPointSignalControl(
        n=n,
        copy_count=copies,
        group_order=order,
        orientation_count=orientation_count,
        partition_count=len(tuple(integer_partitions(n))),
        expected_native_state_purity=kernel[(1,) * n],
        expected_point_state_purity=subgroup_average,
        expected_average_state_purity=group_average,
        expected_centered_hilbert_schmidt_norm_squared=centered,
        normalized_expected_centered_signal=normalized,
        expected_pair_hilbert_schmidt_distance_squared=pair_distance,
        expected_success_excess_trace_norm_upper_bound=trace_bound,
        subgroup_average_standard_coefficient_residual=residual,
        nonnegative_signal_verified=(centered >= -tolerance and residual <= 100 * tolerance),
        collision_free_conditioned_signal_formula_proved=False,
        asymptotic_inverse_polynomial_signal_proved=False,
        status=(
            "exact-natural-point-standard-coefficient-finite-control"
            if centered >= -tolerance and residual <= 100 * tolerance
            else "natural-point-signal-validation-failure"
        ),
    )


def _fourier_irrep_slices(
    n: int,
    character_count: int,
) -> tuple[np.ndarray, tuple[Partition, ...], dict[Partition, slice]]:
    fourier, _, partitions = symmetric_group_fourier_matrix(n)
    slices: dict[Partition, slice] = {}
    offset = 0
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        slices[partition] = slice(
            offset * character_count,
            (offset + dimension * dimension) * character_count,
        )
        offset += dimension * dimension
    return fourier, partitions, slices


def _fixed_tuple_direct_overlap_residuals(
    n: int,
    labels: tuple[Label, ...],
    states: tuple[np.ndarray, ...],
) -> tuple[float, float]:
    permutations = _permutations(n)
    identity_index = permutations.index(tuple(range(n)))
    base = states[identity_index]
    predicted = fixed_tuple_overlap_kernel(n, labels)
    direct_by_class: dict[Partition, list[float]] = defaultdict(list)
    formula_residual = 0.0
    for hidden, state in zip(permutations, states):
        direct = float(np.einsum("ij,ji->", base, state).real)
        cycle = permutation_cycle_type(hidden)
        direct_by_class[cycle].append(direct)
        formula_residual = max(formula_residual, abs(direct - predicted[cycle]))
    class_residual = max(
        max(values) - min(values) for values in direct_by_class.values()
    )
    return formula_residual, class_residual


def audit_point_quotient(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> PointQuotientControl:
    permutations = _permutations(n)
    character_count = 1 << len(labels)
    base = joint_character_state(labels, tuple(range(n)))
    full_states = tuple(
        left_covariant_state(base, permutations, hidden, character_count)
        for hidden in permutations
    )
    quotient = point_quotient_states(labels)
    average = sum(quotient) / n

    covariance_residual = 0.0
    for hidden in permutations:
        for point_state, image in zip(quotient, range(n)):
            transformed = left_covariant_state(
                point_state,
                permutations,
                hidden,
                character_count,
            )
            covariance_residual = max(
                covariance_residual,
                float(np.linalg.norm(transformed - quotient[hidden[image]])),
            )

    group_marginals = tuple(
        _partial_trace_character(state, len(permutations), character_count)
        for state in quotient
    )
    character_marginals = tuple(
        _partial_trace_group(state, len(permutations), character_count)
        for state in quotient
    )
    group_variation = max(
        float(np.linalg.norm(state - group_marginals[0]))
        for state in group_marginals
    )
    character_variation = max(
        float(np.linalg.norm(state - character_marginals[0]))
        for state in character_marginals
    )

    gram = point_centered_gram(quotient)
    diagonal = float(gram[0, 0])
    expected_gram = np.full((n, n), -diagonal / (n - 1))
    np.fill_diagonal(expected_gram, diagonal)
    gram_residual = float(np.linalg.norm(gram - expected_gram))
    span_rank = int(np.linalg.matrix_rank(gram, tol=tolerance))

    fourier, partitions, slices = _fourier_irrep_slices(n, character_count)
    transform = np.kron(fourier.T.conj(), np.eye(character_count))
    transformed = transform @ quotient[0] @ transform.conj().T
    allowed_count = 0
    active_allowed = 0
    active_nonstandard = 0
    forbidden_norm = 0.0
    standard = (n - 1, 1)
    for left in partitions:
        for right in partitions:
            block_norm = float(
                np.linalg.norm(transformed[slices[left], slices[right]])
            )
            if share_young_child(left, right):
                allowed_count += 1
                if block_norm > 100 * tolerance:
                    active_allowed += 1
                    if left != standard or right != standard:
                        active_nonstandard += 1
            else:
                forbidden_norm = max(forbidden_norm, block_norm)

    success, _, _ = _pretty_good_success(quotient, tolerance)
    confusion = _pretty_good_confusion(quotient, tolerance)
    expected_wrong = (1 - success) / (n - 1)
    error_law_residual = max(
        max(abs(confusion[row, row] - success) for row in range(n)),
        max(
            abs(confusion[row, column] - expected_wrong)
            for row in range(n)
            for column in range(n)
            if row != column
        ),
    )
    holevo = _von_neumann_entropy(average, tolerance) - _von_neumann_entropy(
        quotient[0], tolerance
    )
    overlap_formula, overlap_class = _fixed_tuple_direct_overlap_residuals(
        n,
        labels,
        full_states,
    )
    verified = bool(
        covariance_residual <= 100 * tolerance
        and group_variation <= 100 * tolerance
        and character_variation <= 100 * tolerance
        and diagonal > 100 * tolerance
        and gram_residual <= 100 * tolerance
        and span_rank == n - 1
        and forbidden_norm <= 100 * tolerance
        and active_nonstandard > 0
        and holevo > 100 * tolerance
        and success > 1 / n + 100 * tolerance
        and error_law_residual <= 100 * tolerance
        and overlap_formula <= 100 * tolerance
        and overlap_class <= 100 * tolerance
    )
    return PointQuotientControl(
        control_id=control_id,
        n=n,
        labels=labels,
        group_order=len(permutations),
        point_stabilizer_order=math.factorial(n - 1),
        copy_count=len(labels),
        orientation_count=character_count,
        quotient_hypothesis_count=n,
        maximum_covariance_residual=covariance_residual,
        maximum_group_marginal_variation=group_variation,
        maximum_character_marginal_variation=character_variation,
        centered_hilbert_schmidt_norm_squared=diagonal,
        centered_gram_isotropy_residual=gram_residual,
        centered_state_span_rank=span_rank,
        expected_standard_span_rank=n - 1,
        allowed_young_irrep_pair_count=allowed_count,
        active_allowed_young_irrep_pair_count=active_allowed,
        active_nonstandard_young_irrep_pair_count=active_nonstandard,
        maximum_forbidden_young_block_norm=forbidden_norm,
        point_holevo_information_bits=holevo,
        hidden_point_entropy_bits=math.log2(n),
        point_pretty_good_success=success,
        random_guess_success=1 / n,
        pretty_good_excess=success - 1 / n,
        wrong_output_probability=expected_wrong,
        covariance_error_law_residual=error_law_residual,
        fixed_tuple_overlap_formula_residual=overlap_formula,
        fixed_tuple_overlap_class_residual=overlap_class,
        exact_point_quotient_theorem_verified=verified,
        status=(
            "exact-point-quotient-young-edge-mechanism"
            if verified
            else "point-quotient-validation-failure"
        ),
    )


def young_edge_scaling_record(n: int) -> YoungEdgeScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    children_to_parents: dict[Partition, set[Partition]] = defaultdict(set)
    for partition in partitions:
        for child in removable_children(partition):
            children_to_parents[child].add(partition)
    neighbors = {partition: set() for partition in partitions}
    for parents in children_to_parents.values():
        for parent in parents:
            neighbors[parent].update(parents)
    allowed = sum(len(values) for values in neighbors.values())
    total = len(partitions) ** 2
    return YoungEdgeScalingRecord(
        n=n,
        irrep_count=len(partitions),
        young_child_count=len(children_to_parents),
        allowed_ordered_irrep_pair_count=allowed,
        maximum_allowed_neighbor_count=max(map(len, neighbors.values())),
        total_ordered_irrep_pair_count=total,
        allowed_pair_fraction=allowed / total,
        maximum_removable_corner_count=max(
            len(removable_children(partition)) for partition in partitions
        ),
        maximum_addable_parent_count=max(
            len(parents) for parents in children_to_parents.values()
        ),
        local_young_edge_navigation_polynomial=True,
        simultaneous_multiplicity_whitening_proved=False,
        status="young-edge-local-point-decoder-whitening-open",
    )


def stabilizer_chain_reduction_record(n: int) -> StabilizerChainReductionRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    return StabilizerChainReductionRecord(
        n=n,
        stabilizer_stage_count=n - 1,
        required_point_success="p_m=1/m+delta_m with delta_m>=m^-O(1)",
        covariant_wrong_output_law="Pr[wrong label]=(1-p_m)/(m-1)",
        plurality_margin="p_m-(1-p_m)/(m-1)=m delta_m/(m-1)>=delta_m",
        repetitions_per_stage="T_m>=2 delta_m^-2 ln((m-1)/epsilon_m)",
        fresh_subgroup_native_blocks_required=True,
        public_oracle_restriction_required=True,
        inverse_polynomial_point_excess_suffices=True,
        recursive_full_recovery_reduction_proved=True,
        inverse_polynomial_natural_point_excess_proved=False,
        efficient_point_measurement_proved=False,
        polynomial_full_hidden_shift_algorithm_proved=False,
        status="conditional-stabilizer-chain-reduction-point-decoder-open",
    )


def run_point_stabilizer_quotient() -> PointStabilizerQuotientReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_point_quotient(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_point_quotient(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_point_quotient(
            4,
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    natural = [audit_natural_point_signal(n) for n in range(3, 7)]
    scaling = [young_edge_scaling_record(n) for n in (8, 12, 16, 20)]
    reductions = [stabilizer_chain_reduction_record(n) for n in (16, 64, 256)]
    failures = sum(
        not control.exact_point_quotient_theorem_verified for control in controls
    ) + sum(not control.nonnegative_signal_verified for control in natural)
    verified = failures == 0
    theorem = PointStabilizerQuotientTheorem(
        quotient_state=(
            "omega_j=(n-1)!^-1 sum_(g:g(0)=j) tau_g; omega_(xj)=L_x omega_j L_x^*."
        ),
        isotropic_standard_geometry=(
            "Delta_j=omega_j-bar spans zero or V_(n-1,1), with Gram diagonal d "
            "and off-diagonal -d/(n-1)."
        ),
        young_edge_fourier_locality=(
            "The (nu,mu) Fourier block of omega_0 vanishes unless nu and mu "
            "share a child alpha partitioning n-1."
        ),
        fixed_tuple_overlap=(
            "K(u)=|G|^-2 4^-k sum_(s,t) product_i Q_i(s,t,u)."
        ),
        natural_overlap=(
            "E K(u)=|G|^-2 2^-k sum_(s,t) "
            "[a_(s^-1t)+c(s,u^-1s)c(t,t^-1u)]^k."
        ),
        standard_signal_coefficient=(
            "E||omega_0-bar||_2^2=|G|^-1 sum_u (fix(u)-1) E K(u)."
        ),
        recursive_reduction=(
            "Efficient covariant point decoders with inverse-polynomial excess and "
            "fresh subgroup-native blocks imply polynomial full recovery by the "
            "S_n>S_(n-1)>... stabilizer chain."
        ),
        scope=(
            "The exact quotient reduction and finite signal do not prove an all-n "
            "inverse-polynomial excess, a collision-free conditional signal formula, "
            "efficient multiplicity whitening, fresh subgroup-state access for every "
            "problem encoding, or classical separation."
        ),
        theorem_verified=verified,
        status=(
            "point-quotient-reduction-proved-asymptotic-signal-and-decoder-open"
            if verified
            else "point-stabilizer-quotient-validation-failure"
        ),
    )
    return PointStabilizerQuotientReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        natural_signal_controls=natural,
        young_edge_scaling_records=scaling,
        stabilizer_chain_reductions=reductions,
        proof_obligations=[
            {
                "obligation": "derive_point_quotient_representation_geometry",
                "resolved": verified,
                "resolution": (
                    "Covariance and two-transitivity force the centered quotient "
                    "family to be an isotropic copy of the standard module."
                ),
            },
            {
                "obligation": "identify_point_signal_fourier_support",
                "resolved": verified,
                "resolution": (
                    "The S_(n-1) Reynolds operator and multiplicity-free Young "
                    "branching restrict nonzero blocks to shared-child pairs."
                ),
            },
            {
                "obligation": "derive_natural_point_signal",
                "resolved": verified,
                "resolution": (
                    "The relative overlap kernel and Plancherel two-character moment "
                    "give an exact finite class formula and standard coefficient."
                ),
            },
            {
                "obligation": "prove_inverse_polynomial_natural_point_advantage",
                "resolved": False,
                "resolution": (
                    "Exact S_3--S_6 normalized Hilbert--Schmidt controls decay rapidly; "
                    "no lower bound prevents factorial or exponential collapse."
                ),
            },
            {
                "obligation": "transfer_point_signal_to_collision_free_sources",
                "resolved": False,
                "resolution": (
                    "The exact natural formula averages unrestricted independent "
                    "Plancherel pairs. Vanishing collision probability gives only an "
                    "additive comparison and need not preserve a tiny signal lower bound."
                ),
            },
            {
                "obligation": "compile_efficient_point_measurement",
                "resolved": False,
                "resolution": (
                    "Young-edge locality is sparse, but every active irrep still carries "
                    "an orientation multiplicity kernel requiring coherent whitening."
                ),
            },
            {
                "obligation": "lift_point_decoder_down_stabilizer_chain",
                "resolved": True,
                "resolution": (
                    "Under fresh subgroup-native access, covariance gives a uniform "
                    "error law and inverse-polynomial excess amplifies by plurality."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Point averaging leaves only the standard Fourier irrep.",
                "resolved": True,
                "resolution": (
                    "False. The centered operator family transforms as standard, but "
                    "finite controls have nonzero blocks outside (n-1,1); the correct "
                    "support rule is shared-child Young-edge locality."
                ),
            },
            {
                "objection": "Positive point Holevo information implies a scalable weak learner.",
                "resolved": False,
                "resolution": (
                    "Finite point PGM excess is positive, while the exact natural "
                    "normalized Hilbert--Schmidt signal falls sharply through S_6."
                ),
            },
            {
                "objection": "High-probability collision freedom automatically transfers the natural signal.",
                "resolved": False,
                "resolution": (
                    "Not at the needed relative scale. The unrestricted signal may be "
                    "smaller than the excluded event probability, so a conditioned "
                    "lower bound needs a separate argument."
                ),
            },
            {
                "objection": "An inverse-polynomial excess cannot be amplified because there are m labels.",
                "resolved": True,
                "resolution": (
                    "For an S_m-covariant decoder all wrong labels are equiprobable. "
                    "The correct-label plurality margin is at least delta_m."
                ),
            },
            {
                "objection": "The point decoder automatically recurses on arbitrary coset states.",
                "resolved": False,
                "resolution": (
                    "Recursion needs fresh states native to each restricted subgroup and "
                    "known-translation oracle reindexing; inherited S_n states do not "
                    "supply this for free."
                ),
            },
        ],
        headline_metrics={
            "exact_point_quotient_geometry_theorem_count": 1,
            "young_edge_fourier_locality_theorem_count": 1,
            "exact_relative_overlap_kernel_theorem_count": 1,
            "exact_natural_standard_signal_theorem_count": 1,
            "conditional_stabilizer_chain_reduction_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "minimum_finite_point_pgm_excess": min(
                control.pretty_good_excess for control in controls
            ),
            "minimum_natural_normalized_point_signal": min(
                control.normalized_expected_centered_signal for control in natural
            ),
            "inverse_polynomial_point_signal_theorem_count": 0,
            "efficient_point_measurement_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "point_quotient_isotropic_standard_geometry_proved": verified,
            "point_quotient_young_edge_locality_proved": verified,
            "point_signal_confined_to_standard_fourier_irrep": False,
            "exact_natural_point_signal_formula_proved": verified,
            "collision_free_conditioned_point_signal_formula_proved": False,
            "inverse_polynomial_natural_point_signal_proved": False,
            "efficient_point_measurement_proved": False,
            "fresh_subgroup_native_state_access_proved_for_target_problem": False,
            "conditional_stabilizer_chain_recovery_reduction_proved": verified,
            "polynomial_full_hidden_shift_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The quotient and recursive reduction are exact, but the natural "
                "point signal may collapse and the Young-edge multiplicity inverse "
                "has no efficient coherent implementation."
            ),
        },
        status=theorem.status,
        summary=(
            "Point-image extraction is now an exact Young-edge-local weak-learning "
            "target with a stabilizer-chain payoff. Finite signal is real, but its "
            "rapid natural decay and unresolved multiplicity whitening block any "
            "polynomial decoder or speedup claim."
        ),
        falsifiers_triggered=[
            (
                "The operator-valued point signal is not confined to the standard "
                "Fourier irrep; a standard-sector-only decoder discards real signal."
            ),
            (
                "Positive S_3 and S_4 point PGM excess does not establish asymptotic "
                "weak learnability; normalized natural signal drops sharply through S_6."
            ),
            (
                "Young-edge sparsity localizes irrep coupling but does not remove the "
                "orientation-kernel whitening problem."
            ),
        ],
    )


def write_point_stabilizer_quotient_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POINT-STABILIZER-QUOTIENT"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_point_stabilizer_quotient" in globals():
        report = run_point_stabilizer_quotient(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-POINT-STABILIZER-QUOTIENT",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POINT-STABILIZER-QUOTIENT.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POINT-STABILIZER-QUOTIENT.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_point_stabilizer_quotient": str(path)
                },
            )
        )
    return payload
