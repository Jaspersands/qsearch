"""Matrix-free multiplicity-fiber trace for hyperoctahedral orbit sums.

On a repeated restriction block

    V_lambda[(alpha,beta)] ~= C^b tensor W_(alpha,beta),

the full ``K=C_2 wr S_m`` conjugation twirl of an ambient operator has the
form ``B tensor I``.  The copy matrix ``B`` is the normalized carrier partial
trace.  Constructing the whole ``b dim(W)`` isotypic block is unnecessary:

* project random columns directly onto one signed-weight YJM tableau fiber;
* propagate the remaining ``V_alpha tensor V_beta`` tableau fibers by exact
  Young-seminormal edge recurrences;
* transport those fibers across the equal-weight ``C_2^m`` characters; and
* contract the representative over this orthonormal carrier basis.

The root has width ``b``; batched contractions have width ``b f_alpha f_beta``
and cache all stabilizer-tableau fibers. The method is
validated against both an explicit full ``K_4`` twirl and the independent
commutant-projection implementation.  It remains a classical exponential-
ambient diagnostic, not a coherent quantum transform.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
)
from coset_hidden_involution_commutant_support_growth_boundary import (
    _matrix_for_permutation,
    hyperoctahedral_group,
)
from coset_hidden_involution_multiplicity_twirl_projection import (
    Permutation,
    _apply_representation_sparse,
    _isotypic_basis,
    _pair_flip,
    _pair_transposition,
    _projected_hermitian_orbit_matrix,
    _restricted_pair_generators,
    _seminormal_sparse_data,
    _signed_weight_transports,
    _signed_weight_workspace,
    _symmetric_commutant_basis,
    hermitian_bounded_support_orbit_representatives,
    moved_point_support,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    hyperoctahedral_branching_coefficient,
)
from coset_jucys_murphy_label_transform import (
    adjacent_transposition_matrices,
    standard_young_tableaux,
    tableau_content_vector,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_multiplicity_fiber_trace.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-FIBER-TRACE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class RootMultiplicityFiber:
    half_degree: int
    symmetric_partition: Partition
    hyperoctahedral_partition: Partition
    negative_hyperoctahedral_partition: Partition
    symmetric_irrep_dimension: int
    branching_multiplicity: int
    root_fiber_dimension: int
    carrier_weight_dimension: int
    maximum_signed_weight_residual: float
    maximum_yjm_content_residual: float
    orthonormality_residual: float
    projector_application_count: int
    fiber: np.ndarray


@dataclass(frozen=True)
class FiberTraceValidation:
    control_id: str
    half_degree: int
    symmetric_partition: Partition
    hyperoctahedral_partition: Partition
    negative_hyperoctahedral_partition: Partition
    branching_multiplicity: int
    carrier_weight_dimension: int
    equal_weight_character_count: int
    full_carrier_dimension: int
    maximum_tableau_propagation_residual: float
    maximum_carrier_orthogonality_residual: float
    exact_reference_residual: float
    validation_passed: bool
    status: str


@dataclass(frozen=True)
class FiberTraceTheorem:
    direct_root_fiber_projection: str
    tableau_propagation: str
    carrier_partial_trace: str
    width_reduction: str
    direct_root_fiber_projection_verified: bool
    tableau_propagation_verified: bool
    carrier_partial_trace_matches_full_twirl: bool
    carrier_partial_trace_matches_commutant_projection: bool
    polynomial_ambient_compression_proved: bool
    coherent_multiplicity_transform_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FiberTraceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FiberTraceTheorem
    validations: list[FiberTraceValidation]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def _possible_jm_contents(component_size: int, local_label: int) -> tuple[int, ...]:
    if not 2 <= local_label <= component_size:
        raise ValueError("local YJM label must lie in 2..component_size")
    return tuple(
        sorted(
            {
                tableau_content_vector(tableau)[local_label - 1]
                for partition in integer_partitions(component_size)
                for tableau in standard_young_tableaux(partition)
            }
        )
    )


def _apply_pair_jm(
    half_degree: int,
    component_start: int,
    local_label: int,
    vectors: np.ndarray,
    sparse_data: tuple[Any, ...],
) -> np.ndarray:
    target = component_start + local_label - 1
    return sum(
        (
            _apply_representation_sparse(
                _pair_transposition(
                    half_degree,
                    component_start + earlier,
                    target,
                ),
                vectors,
                sparse_data,
            )
            for earlier in range(local_label - 1)
        ),
        np.zeros_like(vectors),
    )


def _project_yjm_content(
    half_degree: int,
    component_start: int,
    component_size: int,
    local_label: int,
    target_content: int,
    vectors: np.ndarray,
    sparse_data: tuple[Any, ...],
) -> tuple[np.ndarray, int]:
    output = vectors
    applications = 0
    for competing_content in _possible_jm_contents(component_size, local_label):
        if competing_content == target_content:
            continue
        output = (
            _apply_pair_jm(
                half_degree,
                component_start,
                local_label,
                output,
                sparse_data,
            )
            - competing_content * output
        ) / (target_content - competing_content)
        applications += 1
    return output, applications


@lru_cache(maxsize=2)
def isolate_root_multiplicity_fiber(
    half_degree: int,
    symmetric_partition: Partition,
    hyperoctahedral_partition: Partition,
    negative_hyperoctahedral_partition: Partition = (),
    *,
    tolerance: float = 1e-7,
) -> RootMultiplicityFiber:
    beta_size = sum(negative_hyperoctahedral_partition)
    alpha_size = sum(hyperoctahedral_partition)
    if alpha_size + beta_size != half_degree:
        raise ValueError("bipartition has the wrong rank")
    multiplicity = hyperoctahedral_branching_coefficient(
        symmetric_partition,
        hyperoctahedral_partition,
        negative_hyperoctahedral_partition,
    )
    if multiplicity < 2:
        raise ValueError("a repeated hyperoctahedral branch is required")
    dimension = hook_length_dimension(symmetric_partition)
    sparse_data = _seminormal_sparse_data(symmetric_partition)
    seed = (
        20260903
        + 101 * half_degree
        + 1009 * beta_size
        + sum((index + 1) * value for index, value in enumerate(symmetric_partition))
    )
    random = np.random.default_rng(seed)
    projected = random.normal(size=(dimension, multiplicity))
    applications = 0
    for pair in range(half_degree):
        acted = _apply_representation_sparse(
            _pair_flip(half_degree, pair),
            projected,
            sparse_data,
        )
        sign = 1.0 if pair < alpha_size else -1.0
        projected = (projected + sign * acted) / 2.0
        applications += 1

    target_tableaux = (
        standard_young_tableaux(hyperoctahedral_partition)[0],
        standard_young_tableaux(negative_hyperoctahedral_partition)[0],
    )
    for start, size, tableau in (
        (0, alpha_size, target_tableaux[0]),
        (alpha_size, beta_size, target_tableaux[1]),
    ):
        if size <= 1:
            continue
        contents = tableau_content_vector(tableau)
        for local_label in range(2, size + 1):
            projected, count = _project_yjm_content(
                half_degree,
                start,
                size,
                local_label,
                contents[local_label - 1],
                projected,
                sparse_data,
            )
            applications += count
    fiber, triangular = np.linalg.qr(projected, mode="reduced")
    if fiber.shape[1] != multiplicity or np.min(
        np.abs(np.diag(triangular))
    ) <= 1e-12:
        raise ArithmeticError("direct YJM projector lost multiplicity-fiber rank")
    signed_residual = max(
        float(
            np.linalg.norm(
                _apply_representation_sparse(
                    _pair_flip(half_degree, pair),
                    fiber,
                    sparse_data,
                )
                - (1.0 if pair < alpha_size else -1.0) * fiber
            )
        )
        for pair in range(half_degree)
    )
    yjm_residual = 0.0
    for start, size, tableau in (
        (0, alpha_size, target_tableaux[0]),
        (alpha_size, beta_size, target_tableaux[1]),
    ):
        contents = tableau_content_vector(tableau)
        for local_label in range(2, size + 1):
            yjm_residual = max(
                yjm_residual,
                float(
                    np.linalg.norm(
                        _apply_pair_jm(
                            half_degree,
                            start,
                            local_label,
                            fiber,
                            sparse_data,
                        )
                        - contents[local_label - 1] * fiber
                    )
                ),
            )
    orthogonality = float(np.linalg.norm(fiber.T @ fiber - np.eye(multiplicity)))
    if max(signed_residual, yjm_residual, orthogonality) > 1000 * tolerance:
        raise ArithmeticError("direct multiplicity-fiber projection failed residual checks")
    return RootMultiplicityFiber(
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        hyperoctahedral_partition=hyperoctahedral_partition,
        negative_hyperoctahedral_partition=negative_hyperoctahedral_partition,
        symmetric_irrep_dimension=dimension,
        branching_multiplicity=multiplicity,
        root_fiber_dimension=multiplicity,
        carrier_weight_dimension=(
            hook_length_dimension(hyperoctahedral_partition)
            * hook_length_dimension(negative_hyperoctahedral_partition)
        ),
        maximum_signed_weight_residual=signed_residual,
        maximum_yjm_content_residual=yjm_residual,
        orthonormality_residual=orthogonality,
        projector_application_count=applications,
        fiber=fiber,
    )


@lru_cache(maxsize=2)
def propagate_stabilizer_tableau_fibers(
    half_degree: int,
    symmetric_partition: Partition,
    hyperoctahedral_partition: Partition,
    negative_hyperoctahedral_partition: Partition = (),
) -> tuple[tuple[np.ndarray, ...], float, float]:
    root = isolate_root_multiplicity_fiber(
        half_degree,
        symmetric_partition,
        hyperoctahedral_partition,
        negative_hyperoctahedral_partition,
    )
    sparse_data = _seminormal_sparse_data(symmetric_partition)
    alpha_size = sum(hyperoctahedral_partition)
    alpha_tableaux = standard_young_tableaux(hyperoctahedral_partition)
    beta_tableaux = standard_young_tableaux(negative_hyperoctahedral_partition)
    alpha_generators = adjacent_transposition_matrices(hyperoctahedral_partition)
    beta_generators = adjacent_transposition_matrices(
        negative_hyperoctahedral_partition
    )
    nodes = [
        (alpha_index, beta_index)
        for alpha_index in range(len(alpha_tableaux))
        for beta_index in range(len(beta_tableaux))
    ]
    root_node = (0, 0)
    fibers = {root_node: root.fiber}
    pending = [root_node]
    propagation_residual = 0.0
    while pending:
        node = pending.pop(0)
        fiber = fibers[node]
        for component, tableau_index, generators, offset in (
            (0, node[0], alpha_generators, 0),
            (1, node[1], beta_generators, alpha_size),
        ):
            for generator_index, generator in enumerate(generators):
                column = generator[:, tableau_index]
                neighbors = np.flatnonzero(np.abs(column) > 1e-12)
                neighbors = neighbors[neighbors != tableau_index]
                if len(neighbors) == 0:
                    continue
                if len(neighbors) != 1:
                    raise ArithmeticError("seminormal generator has multiple neighbors")
                neighbor_index = int(neighbors[0])
                neighbor = (
                    (neighbor_index, node[1])
                    if component == 0
                    else (node[0], neighbor_index)
                )
                diagonal = float(column[tableau_index])
                off_diagonal = float(column[neighbor_index])
                acted = _apply_representation_sparse(
                    _pair_transposition(
                        half_degree,
                        offset + generator_index,
                        offset + generator_index + 1,
                    ),
                    fiber,
                    sparse_data,
                )
                candidate = (acted - diagonal * fiber) / off_diagonal
                if neighbor in fibers:
                    propagation_residual = max(
                        propagation_residual,
                        float(np.linalg.norm(candidate - fibers[neighbor])),
                    )
                else:
                    fibers[neighbor] = candidate
                    pending.append(neighbor)
    if len(fibers) != len(nodes):
        raise ArithmeticError("stabilizer tableau propagation was incomplete")
    ordered = tuple(fibers[node] for node in nodes)
    gram = np.block(
        [[left.T @ right for right in ordered] for left in ordered]
    )
    orthogonality = float(np.linalg.norm(gram - np.eye(gram.shape[0])))
    return ordered, propagation_residual, orthogonality


def copy_matrix_for_orbit_representative(
    half_degree: int,
    symmetric_partition: Partition,
    hyperoctahedral_partition: Partition,
    representative: Permutation,
    negative_hyperoctahedral_partition: Partition = (),
) -> tuple[np.ndarray, dict[str, int | float]]:
    root = isolate_root_multiplicity_fiber(
        half_degree,
        symmetric_partition,
        hyperoctahedral_partition,
        negative_hyperoctahedral_partition,
    )
    fibers, propagation_residual, orthogonality = (
        propagate_stabilizer_tableau_fibers(
            half_degree,
            symmetric_partition,
            hyperoctahedral_partition,
            negative_hyperoctahedral_partition,
        )
    )
    sparse_data = _seminormal_sparse_data(symmetric_partition)
    transports = _signed_weight_transports(
        half_degree,
        sum(negative_hyperoctahedral_partition),
    )
    carrier = np.concatenate(fibers, axis=1)
    carrier_tensor = carrier.reshape(
        carrier.shape[0],
        len(fibers),
        root.branching_multiplicity,
    )
    block = np.zeros((root.branching_multiplicity,) * 2)
    sparse_action_count = 0
    for transport in transports:
        inverse_transport = inverse_permutation(transport)
        conjugated = compose_permutations(
            compose_permutations(transport, representative),
            inverse_transport,
        )
        forward = _apply_representation_sparse(
            conjugated,
            carrier,
            sparse_data,
        ).reshape(carrier_tensor.shape)
        sparse_action_count += 1
        forward_block = np.einsum(
            "dfi,dfj->ij",
            carrier_tensor,
            forward,
            optimize=True,
        )
        inverse = inverse_permutation(conjugated)
        if inverse == conjugated:
            block += forward_block
        else:
            backward = _apply_representation_sparse(
                inverse,
                carrier,
                sparse_data,
            ).reshape(carrier_tensor.shape)
            sparse_action_count += 1
            block += (
                forward_block
                + np.einsum(
                    "dfi,dfj->ij",
                    carrier_tensor,
                    backward,
                    optimize=True,
                )
            ) / 2.0
    contraction_count = len(transports) * len(fibers)
    block /= contraction_count
    block = (block + block.T) / 2.0
    return block, {
        "branching_multiplicity": root.branching_multiplicity,
        "carrier_weight_dimension": len(fibers),
        "equal_weight_character_count": len(transports),
        "full_carrier_dimension": len(fibers) * len(transports),
        "root_fiber_column_width": root.branching_multiplicity,
        "batched_action_column_width": root.branching_multiplicity * len(fibers),
        "full_isotypic_column_width": (
            root.branching_multiplicity * len(fibers) * len(transports)
        ),
        "column_width_reduction_factor": len(transports),
        "maximum_tableau_propagation_residual": propagation_residual,
        "maximum_carrier_orthogonality_residual": orthogonality,
        "carrier_contraction_count": contraction_count,
        "batched_sparse_representation_action_count": sparse_action_count,
    }


def _validate_against_full_k4_twirl() -> FiberTraceValidation:
    half_degree = 4
    symmetric_partition = (4, 2, 2)
    alpha = (2,)
    beta = (2,)
    representative = _pair_transposition(half_degree, 0, 2)
    block, metrics = copy_matrix_for_orbit_representative(
        half_degree,
        symmetric_partition,
        alpha,
        representative,
        beta,
    )
    root = isolate_root_multiplicity_fiber(
        half_degree,
        symmetric_partition,
        alpha,
        beta,
    )
    operator = _matrix_for_permutation(symmetric_partition, representative)
    exact = np.zeros_like(operator)
    group = hyperoctahedral_group(half_degree)
    for element in group:
        representation = _matrix_for_permutation(symmetric_partition, element)
        exact += representation @ operator @ representation.T
    exact /= len(group)
    reference = root.fiber.T @ exact @ root.fiber
    residual = float(np.linalg.norm(block - reference))
    passed = bool(
        residual <= 1e-9
        and metrics["maximum_tableau_propagation_residual"] <= 1e-9
        and metrics["maximum_carrier_orthogonality_residual"] <= 1e-9
    )
    return FiberTraceValidation(
        control_id="EXACT-K4-SIGNED-FULL-TWIRL",
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        hyperoctahedral_partition=alpha,
        negative_hyperoctahedral_partition=beta,
        branching_multiplicity=root.branching_multiplicity,
        carrier_weight_dimension=int(metrics["carrier_weight_dimension"]),
        equal_weight_character_count=int(metrics["equal_weight_character_count"]),
        full_carrier_dimension=int(metrics["full_carrier_dimension"]),
        maximum_tableau_propagation_residual=float(
            metrics["maximum_tableau_propagation_residual"]
        ),
        maximum_carrier_orthogonality_residual=float(
            metrics["maximum_carrier_orthogonality_residual"]
        ),
        exact_reference_residual=residual,
        validation_passed=passed,
        status=(
            "fiber-trace-matches-exact-full-twirl"
            if passed
            else "fiber-trace-full-twirl-validation-failed"
        ),
    )


def _validate_against_commutant_projection() -> FiberTraceValidation:
    half_degree = 7
    symmetric_partition = (10, 2, 2)
    alpha = (4, 1)
    beta = (2,)
    representative = next(
        item
        for item in hermitian_bounded_support_orbit_representatives(half_degree, 4)
        if moved_point_support(item) == 4
    )
    block, metrics = copy_matrix_for_orbit_representative(
        half_degree,
        symmetric_partition,
        alpha,
        representative,
        beta,
    )
    isotypic, multiplicity, _, _ = _isotypic_basis(
        half_degree,
        symmetric_partition,
        alpha,
        beta,
        tolerance=1e-7,
    )
    _, _, _, sparse_data, _ = _signed_weight_workspace(
        half_degree,
        symmetric_partition,
        sum(beta),
    )
    generators, swaps, order = _restricted_pair_generators(
        half_degree,
        sum(beta),
        isotypic,
        sparse_data,
    )
    commutant, _, _ = _symmetric_commutant_basis(
        half_degree,
        generators,
        swaps,
        order,
        multiplicity,
        tolerance=1e-7,
    )
    projected, _ = _projected_hermitian_orbit_matrix(
        symmetric_partition,
        representative,
        isotypic,
        commutant,
        sparse_data,
        _signed_weight_transports(half_degree, sum(beta)),
    )
    carrier_weight_dimension = (
        hook_length_dimension(alpha) * hook_length_dimension(beta)
    )
    expected = np.repeat(np.linalg.eigvalsh(block), carrier_weight_dimension)
    observed = np.linalg.eigvalsh(projected)
    residual = float(np.linalg.norm(np.sort(expected) - np.sort(observed)))
    passed = bool(
        residual <= 1e-8
        and metrics["maximum_tableau_propagation_residual"] <= 1e-9
        and metrics["maximum_carrier_orthogonality_residual"] <= 1e-9
    )
    return FiberTraceValidation(
        control_id="S14-SIGNED-COMMUTANT-PROJECTION",
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        hyperoctahedral_partition=alpha,
        negative_hyperoctahedral_partition=beta,
        branching_multiplicity=multiplicity,
        carrier_weight_dimension=int(metrics["carrier_weight_dimension"]),
        equal_weight_character_count=int(metrics["equal_weight_character_count"]),
        full_carrier_dimension=int(metrics["full_carrier_dimension"]),
        maximum_tableau_propagation_residual=float(
            metrics["maximum_tableau_propagation_residual"]
        ),
        maximum_carrier_orthogonality_residual=float(
            metrics["maximum_carrier_orthogonality_residual"]
        ),
        exact_reference_residual=residual,
        validation_passed=passed,
        status=(
            "fiber-trace-matches-independent-commutant-projection"
            if passed
            else "fiber-trace-commutant-validation-failed"
        ),
    )


@lru_cache(maxsize=1)
def run_multiplicity_fiber_trace() -> FiberTraceReport:
    validations = [
        _validate_against_full_k4_twirl(),
        _validate_against_commutant_projection(),
    ]
    verified = all(item.validation_passed for item in validations)
    theorem = FiberTraceTheorem(
        direct_root_fiber_projection=(
            "Commuting pair-flip and YJM spectral projectors isolate one signed "
            "tableau fiber of exact dimension b(lambda;alpha,beta)."
        ),
        tableau_propagation=(
            "Young-seminormal adjacent-edge recurrences propagate the root fiber "
            "through every V_alpha tensor V_beta tableau with a common copy gauge."
        ),
        carrier_partial_trace=(
            "Averaging the representative contraction over propagated tableaux and "
            "equal-weight sign characters equals the copy matrix of the full K twirl."
        ),
        width_reduction=(
            "The root width is b, but batched actions and cached tableau fibers use b f_alpha f_beta columns; the "
            "ambient Specht dimension remains exponential on typical partitions."
        ),
        direct_root_fiber_projection_verified=verified,
        tableau_propagation_verified=verified,
        carrier_partial_trace_matches_full_twirl=validations[0].validation_passed,
        carrier_partial_trace_matches_commutant_projection=(
            validations[1].validation_passed
        ),
        polynomial_ambient_compression_proved=False,
        coherent_multiplicity_transform_compiled=False,
        theorem_verified=verified,
        status=(
            "matrix-free-copy-fiber-trace-validated-typical-ambient-scaling-open"
            if verified
            else "multiplicity-fiber-trace-validation-failed"
        ),
    )
    metrics: dict[str, int | float] = {
        "direct_root_multiplicity_fiber_projection_theorem_count": int(verified),
        "tableau_fiber_propagation_theorem_count": int(verified),
        "carrier_partial_trace_full_twirl_validation_count": int(
            validations[0].validation_passed
        ),
        "independent_commutant_projection_validation_count": int(
            validations[1].validation_passed
        ),
        "maximum_validated_branching_multiplicity": max(
            item.branching_multiplicity for item in validations
        ),
        "maximum_validated_full_carrier_dimension": max(
            item.full_carrier_dimension for item in validations
        ),
        "polynomial_typical_ambient_compression_theorem_count": 0,
        "coherent_multiplicity_transform_count": 0,
        "hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return FiberTraceReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "a repeated hyperoctahedral branch, one bounded-support ambient "
                "permutation, and sparse Young-seminormal generator actions"
            ),
            "output": (
                "the exact b-by-b copy matrix of its K-conjugation orbit average"
            ),
            "non_claim": (
                "No polynomial compression of typical ambient Specht spaces, coherent "
                "isotypic transform, normalized gap theorem, decoder, or speedup."
            ),
        },
        theorem=theorem,
        validations=validations,
        proof_obligations=[
            {
                "obligation": "run_highest_natural_mass_s14_block",
                "resolved": False,
                "resolution": (
                    "Use the fiber-width reduction on the ranked multiplicity-26 "
                    "block and search support cutoffs four through six."
                ),
            },
            {
                "obligation": "remove_exponential_ambient_specht_dimension",
                "resolved": False,
                "resolution": (
                    "Derive a symbolic occupancy, partition-algebra, or tensor-network "
                    "contraction before claiming polynomial typical-block access."
                ),
            },
            {
                "obligation": "measure_normalized_copy_space_gaps",
                "resolved": False,
                "resolution": (
                    "Generation alone is insufficient; exact or certified spectra of "
                    "succinct separator combinations are required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A single tableau fiber loses the carrier trace.",
                "survives": False,
                "response": (
                    "Seminormal propagation reconstructs an aligned orthonormal carrier "
                    "basis, and the result matches a full K_4 twirl."
                ),
            },
            {
                "challenge": "Signed beta sectors invalidate tableau propagation.",
                "survives": False,
                "response": (
                    "Independent S_|alpha| and S_|beta| recurrences plus sign-character "
                    "transport match the separate commutant-projection implementation."
                ),
            },
            {
                "challenge": "Column-width reduction makes the method polynomial.",
                "survives": True,
                "response": (
                    "Every fiber still has one row per ambient standard tableau, which "
                    "is exponential for natural typical partitions."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_copy_fiber_trace_verified": verified,
            "full_k_twirl_validation_passed": validations[0].validation_passed,
            "independent_commutant_projection_validation_passed": (
                validations[1].validation_passed
            ),
            "polynomial_typical_ambient_compression_proved": False,
            "coherent_multiplicity_transform_compiled": False,
            "normalized_gap_on_natural_mass_proved": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact classical contraction removes carrier column width but not "
                "the exponential ambient Specht basis, and it supplies no coherent "
                "transform, typical gap theorem, or decoder."
            ),
        },
        status=theorem.status,
        summary=(
            "Validated direct signed-YJM multiplicity fibers and carrier partial "
            "traces against a full K_4 twirl and an independent S_14 commutant projection."
        ),
        falsifiers_triggered=[
            "Full isotypic commutant matrices are unnecessary for exact classical copy-space contraction.",
            "Carrier-width reduction does not remove exponential ambient Specht dimension.",
            "Exact finite copy matrices do not provide a coherent transform, normalized gap theorem, or decoder.",
        ],
    )


def write_multiplicity_fiber_trace_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_multiplicity_fiber_trace())
    for validation in payload["validations"]:
        validation.pop("fiber", None)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Hyperoctahedral multiplicity-fiber partial trace",
                status="completed-exact-fiber-trace-validated-ambient-scaling-open",
                hypothesis=(
                    "One signed YJM multiplicity fiber and carrier propagation can "
                    "replace full isotypic commutant matrices in orbit-sum audits."
                ),
                protocol=(
                    "Project a root fiber, propagate stabilizer tableaux, transport sign "
                    "characters, contract representative copy matrices, and compare with "
                    "a full K_4 twirl and independent S_14 commutant projection."
                ),
                positive_signal=(
                    "Matrix-free access to high-natural-mass blocks followed by a "
                    "uniform normalized-gap theorem and coherent implementation."
                ),
                falsifiers=[
                    "fiber trace disagrees with a full group twirl",
                    "signed tableau propagation loses a common copy gauge",
                    "column-width reduction is called polynomial ambient compression",
                    "finite exact matrices are called a quantum decoder",
                ],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "coset_hidden_involution_multiplicity_twirl_projection.py",
                    "Young-seminormal YJM projectors",
                    "hyperoctahedral signed-weight decomposition",
                ],
                next_actions=[
                    "run the multiplicity-26 highest-mass S_14 target",
                    "stream support-four through support-six orbit representatives",
                    "certify normalized spectra of succinct separator combinations",
                    "derive symbolic typical-shape contraction",
                ],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "coset_hidden_involution_multiplicity_fiber_trace": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="MULTIPLICITY-FIBER-WIDTH-REDUCTION-NOT-POLYNOMIAL-AMBIENT-COMPRESSION",
                source=registry_experiment_id,
                claim=(
                    "Reducing batched isotypic columns from b dim(W_mu) to b f_alpha f_beta makes the "
                    "typical-block commutant audit polynomial."
                ),
                reason_invalid=(
                    "Each fiber still has dim(V_lambda) rows, exponential on typical "
                    "partitions, and no symbolic or tensor-network compression is known."
                ),
                lesson=(
                    "Use the fiber trace to extend finite falsification reach while "
                    "keeping typical-shape ambient compression as an explicit blocker."
                ),
                applies_to=[
                    registry_candidate_id,
                    "multiplicity-fiber trace",
                    "typical hyperoctahedral branches",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_multiplicity_fiber_trace_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
