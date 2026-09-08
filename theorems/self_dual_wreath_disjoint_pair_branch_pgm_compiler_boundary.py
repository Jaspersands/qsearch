"""Compiler boundary for disjoint pair-carrier branch PGMs.

The disjoint-pair success theorem uses source independence to control the
*average collision denominator*.  That probabilistic factorization must not be
mistaken for a circuit factorization of the branch PGM.

For two disjoint carrier branches, conditioned states have the product form

    omega_h = sigma_h tensor tau_h.                              (1)

The same hidden label ``h`` occurs in both factors.  Consequently their
hypothesis-averaged frame is

    bar(omega) = bar(sigma) tensor bar(tau) + C,
    C = M^-1 sum_h (sigma_h-bar(sigma)) tensor
                     (tau_h-bar(tau)).                           (2)

The covariance ``C`` is generally nonzero.  The inverse square root in the
global PGM therefore does not split into the two pair-local inverse square
roots.  Even the tempting same-label product effects

    M E_h tensor F_h                                             (3)

need not sum to the support projector and can have sum eigenvalues above one.
They are not a POVM in general.

This module verifies (1)--(2), measures the failure of (3), and compares the
true branch PGM with a valid local alternative: measure the two pair PGMs
independently and classically make the maximum-posterior shared-label guess.
Exact natural S_3 and S_4 averages and selected S_5 controls falsify the naive
pair-local compiler.  They do not rule out a covariance-aware covariant polar,
nor do they prove a lower bound for quantum circuits.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_natural_multicopy_pgm_benchmark import (
    _channel_statistics,
    _rowwise_product_channel,
    _source_data,
)
from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_plancherel_carrier_contextuality import (
    _triple_isotypic_projectors,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-DISJOINT-PAIR-BRANCH-PGM-COMPILER-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class DisjointPairSourceCompilerControl:
    control_id: str
    n: int
    transposition_count: int
    left_pair_partitions: tuple[Partition, Partition]
    right_pair_partitions: tuple[Partition, Partition]
    natural_source_probability: float
    hidden_involution_count: int
    left_pair_dimension: int
    right_pair_dimension: int
    joint_dimension: int
    active_joint_carrier_branch_count: int
    total_joint_branch_probability: float
    global_branch_pgm_bayes_success: float
    pair_local_pgm_map_bayes_success: float
    global_advantage_over_pair_local_map: float
    weighted_frame_covariance_fraction: float
    maximum_frame_covariance_fraction: float
    weighted_scaled_diagonal_completeness_residual: float
    maximum_scaled_diagonal_completeness_residual: float
    weighted_scaled_diagonal_eigenvalue_excess: float
    maximum_scaled_diagonal_eigenvalue_excess: float
    weighted_global_effect_factorization_residual: float
    maximum_global_effect_factorization_residual: float
    maximum_covariance_identity_residual: float
    maximum_global_pgm_completeness_residual: float
    maximum_pair_pgm_completeness_residual: float
    maximum_channel_normalization_residual: float
    nonzero_shared_label_covariance_verified: bool
    scaled_diagonal_product_fails_povm_verified: bool
    global_pgm_differs_from_pair_local_map_verified: bool
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalDisjointPairCompilerAggregate:
    n: int
    transposition_count: int
    hidden_involution_count: int
    pair_source_type_count: int
    source_quadruple_type_count: int
    active_joint_carrier_branch_count: int
    total_natural_source_probability: float
    natural_global_branch_pgm_bayes_success: float
    natural_pair_local_pgm_map_bayes_success: float
    natural_global_advantage_over_pair_local_map: float
    natural_weighted_frame_covariance_fraction: float
    natural_weighted_scaled_diagonal_completeness_residual: float
    natural_weighted_scaled_diagonal_eigenvalue_excess: float
    natural_weighted_global_effect_factorization_residual: float
    maximum_frame_covariance_fraction: float
    maximum_scaled_diagonal_completeness_residual: float
    maximum_scaled_diagonal_eigenvalue_excess: float
    source_mass_with_nonzero_covariance: float
    source_mass_where_scaled_diagonal_product_fails_povm: float
    all_controls_verified: bool
    status: str


@dataclass(frozen=True)
class DisjointPairResidualCouplingScalingRecord:
    n: int
    hidden_involution_count_decimal: str
    hidden_involution_count_log2: float
    information_threshold_copy_count: int
    disjoint_pair_count: int
    residual_shared_hidden_label_block_count: int
    residual_block_fraction: float
    conditioned_state_tensor_factorization_proved: bool
    hypothesis_average_tensor_factorization_proved: bool
    bounded_residual_block_count_proved: bool
    status: str


@dataclass(frozen=True)
class DisjointPairBranchPgmCompilerTheorem:
    conditioned_state_factorization: str
    shared_label_covariance_identity: str
    pgm_factorization_boundary: str
    valid_pair_local_baseline: str
    diagonal_product_effect_boundary: str
    asymptotic_block_count: str
    surviving_compiler_target: str
    scope: str
    conditioned_state_factorization_proved: bool
    shared_label_covariance_identity_proved: bool
    finite_shared_label_covariance_nonzero_verified: bool
    pair_local_pgm_equals_global_branch_pgm: bool
    scaled_diagonal_product_is_povm: bool
    naive_pair_local_branch_pgm_compiler_falsified: bool
    covariance_aware_branch_pgm_compiled: bool
    hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DisjointPairBranchPgmCompilerBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DisjointPairBranchPgmCompilerTheorem
    natural_aggregates: list[NaturalDisjointPairCompilerAggregate]
    selected_growing_hypothesis_controls: list[DisjointPairSourceCompilerControl]
    worst_natural_controls: list[DisjointPairSourceCompilerControl]
    scaling_records: list[DisjointPairResidualCouplingScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class _PgmData:
    average: np.ndarray
    support_projector: np.ndarray
    effects: tuple[np.ndarray, ...]
    channel: np.ndarray
    completeness_residual: float


@dataclass(frozen=True)
class _PairCarrierBranch:
    carrier_partition: Partition
    probability: float
    states: tuple[np.ndarray, ...]
    pgm: _PgmData


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _pgm_data(
    states: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-11,
) -> _PgmData:
    if not states:
        raise ValueError("PGM requires a nonempty state ensemble")
    hidden_count = len(states)
    average = _hermitian(sum(states) / hidden_count)
    eigenvalues, eigenvectors = np.linalg.eigh(average)
    support = eigenvalues > tolerance
    if not np.any(support):
        raise ArithmeticError("average state has empty numerical support")
    vectors = eigenvectors[:, support]
    inverse_root = (
        vectors
        @ np.diag(1.0 / np.sqrt(eigenvalues[support]))
        @ vectors.conj().T
    )
    support_projector = vectors @ vectors.conj().T
    effects = tuple(
        _hermitian(inverse_root @ (state / hidden_count) @ inverse_root)
        for state in states
    )
    completeness = float(
        np.linalg.norm(sum(effects) - support_projector, ord=2)
    )
    channel = np.asarray(
        [
            [float(np.trace(effect @ state).real) for effect in effects]
            for state in states
        ]
    )
    return _PgmData(
        average=average,
        support_projector=support_projector,
        effects=effects,
        channel=channel,
        completeness_residual=completeness,
    )


@lru_cache(maxsize=None)
def _pair_carrier_branches(
    n: int,
    transposition_count: int,
    pair_indices: tuple[int, int],
    tolerance: float = 1e-10,
) -> tuple[tuple[Partition, Partition], tuple[_PairCarrierBranch, ...]]:
    partitions, _, state_families = _source_data(n, transposition_count)
    first, second = pair_indices
    if not (
        0 <= first < len(partitions) and 0 <= second < len(partitions)
    ):
        raise IndexError("pair source index outside the natural source family")
    source_partitions = (partitions[first], partitions[second])
    hidden_count = len(state_families[0])
    states = tuple(
        np.kron(
            state_families[first][hidden],
            state_families[second][hidden],
        )
        for hidden in range(hidden_count)
    )
    projectors = _triple_isotypic_projectors(
        (partitions[first], partitions[second], (n,)),
        "left",
    )
    branches: list[_PairCarrierBranch] = []
    for target, projector in zip(
        tuple(integer_partitions(n)),
        projectors,
        strict=True,
    ):
        unnormalized = tuple(projector @ state @ projector for state in states)
        probabilities = np.asarray(
            [float(np.trace(state).real) for state in unnormalized]
        )
        probability = float(probabilities.mean())
        if probability <= tolerance:
            continue
        if float(np.max(np.abs(probabilities - probability))) > 100 * tolerance:
            raise ArithmeticError("pair carrier probability depends on hidden label")
        normalized = tuple(state / probability for state in unnormalized)
        branches.append(
            _PairCarrierBranch(
                carrier_partition=target,
                probability=probability,
                states=normalized,
                pgm=_pgm_data(normalized),
            )
        )
    if abs(sum(branch.probability for branch in branches) - 1.0) > 100 * tolerance:
        raise ArithmeticError("active pair carrier probabilities do not sum to one")
    return source_partitions, tuple(branches)


def _pair_source_probability(
    probabilities: tuple[float, ...],
    pair_indices: tuple[int, int],
) -> float:
    first, second = pair_indices
    multiplicity = 1 if first == second else 2
    return multiplicity * probabilities[first] * probabilities[second]


@lru_cache(maxsize=None)
def audit_disjoint_pair_source_compiler(
    n: int,
    transposition_count: int,
    left_pair_indices: tuple[int, int],
    right_pair_indices: tuple[int, int],
    *,
    tolerance: float = 1e-9,
) -> DisjointPairSourceCompilerControl:
    """Audit one source quadruple and every active disjoint carrier branch."""

    _, source_probabilities, state_families = _source_data(
        n,
        transposition_count,
    )
    left_partitions, left_branches = _pair_carrier_branches(
        n,
        transposition_count,
        left_pair_indices,
    )
    right_partitions, right_branches = _pair_carrier_branches(
        n,
        transposition_count,
        right_pair_indices,
    )
    hidden_count = len(state_families[0])
    natural_probability = _pair_source_probability(
        source_probabilities,
        left_pair_indices,
    ) * _pair_source_probability(source_probabilities, right_pair_indices)
    left_dimension = left_branches[0].states[0].shape[0]
    right_dimension = right_branches[0].states[0].shape[0]

    totals = {
        "probability": 0.0,
        "global_bayes": 0.0,
        "local_bayes": 0.0,
        "covariance": 0.0,
        "diagonal_completeness": 0.0,
        "diagonal_excess": 0.0,
        "effect_factorization": 0.0,
    }
    maxima = {
        "covariance": 0.0,
        "diagonal_completeness": 0.0,
        "diagonal_excess": 0.0,
        "effect_factorization": 0.0,
        "covariance_identity": 0.0,
        "global_completeness": 0.0,
        "pair_completeness": 0.0,
        "channel_normalization": 0.0,
    }
    branch_count = 0
    for left, right in itertools.product(left_branches, right_branches):
        weight = left.probability * right.probability
        joint_states = tuple(
            np.kron(left.states[hidden], right.states[hidden])
            for hidden in range(hidden_count)
        )
        global_pgm = _pgm_data(joint_states)
        _, global_bayes, global_channel_residual = _channel_statistics(
            global_pgm.channel
        )
        local_channel = _rowwise_product_channel(
            (left.pgm.channel, right.pgm.channel)
        )
        _, local_bayes, local_channel_residual = _channel_statistics(local_channel)

        product_average = np.kron(left.pgm.average, right.pgm.average)
        covariance = global_pgm.average - product_average
        centered_covariance = sum(
            (
                np.kron(
                    left.states[hidden] - left.pgm.average,
                    right.states[hidden] - right.pgm.average,
                )
                for hidden in range(hidden_count)
            ),
            np.zeros_like(global_pgm.average),
        ) / hidden_count
        covariance_identity = float(
            np.linalg.norm(covariance - centered_covariance, ord="fro")
        )
        covariance_fraction = float(
            np.linalg.norm(covariance, ord="fro")
            / max(np.linalg.norm(global_pgm.average, ord="fro"), tolerance)
        )

        scaled_diagonal_sum = hidden_count * sum(
            (
                np.kron(left.pgm.effects[hidden], right.pgm.effects[hidden])
                for hidden in range(hidden_count)
            ),
            np.zeros_like(global_pgm.average),
        )
        diagonal_completeness = float(
            np.linalg.norm(
                scaled_diagonal_sum - global_pgm.support_projector,
                ord=2,
            )
        )
        diagonal_maximum = float(
            np.linalg.eigvalsh(_hermitian(scaled_diagonal_sum))[-1]
        )
        diagonal_excess = max(0.0, diagonal_maximum - 1.0)
        effect_factorization = sum(
            float(
                np.linalg.norm(
                    global_pgm.effects[hidden]
                    - hidden_count
                    * np.kron(
                        left.pgm.effects[hidden],
                        right.pgm.effects[hidden],
                    ),
                    ord="fro",
                )
            )
            for hidden in range(hidden_count)
        ) / hidden_count

        values = {
            "covariance": covariance_fraction,
            "diagonal_completeness": diagonal_completeness,
            "diagonal_excess": diagonal_excess,
            "effect_factorization": effect_factorization,
        }
        totals["probability"] += weight
        totals["global_bayes"] += weight * global_bayes
        totals["local_bayes"] += weight * local_bayes
        for key, value in values.items():
            totals[key] += weight * value
            maxima[key] = max(maxima[key], value)
        maxima["covariance_identity"] = max(
            maxima["covariance_identity"],
            covariance_identity,
        )
        maxima["global_completeness"] = max(
            maxima["global_completeness"],
            global_pgm.completeness_residual,
        )
        maxima["pair_completeness"] = max(
            maxima["pair_completeness"],
            left.pgm.completeness_residual,
            right.pgm.completeness_residual,
        )
        maxima["channel_normalization"] = max(
            maxima["channel_normalization"],
            global_channel_residual,
            local_channel_residual,
        )
        branch_count += 1

    probability = totals["probability"]
    covariance_nonzero = totals["covariance"] > 100 * tolerance
    diagonal_fails = (
        totals["diagonal_completeness"] > 100 * tolerance
        or totals["diagonal_excess"] > 100 * tolerance
    )
    global_differs = (
        totals["global_bayes"] - totals["local_bayes"] > 100 * tolerance
    )
    verified = (
        abs(probability - 1.0) <= 100 * tolerance
        and maxima["covariance_identity"] <= 100 * tolerance
        and maxima["global_completeness"] <= 1000 * tolerance
        and maxima["pair_completeness"] <= 1000 * tolerance
        and maxima["channel_normalization"] <= 1000 * tolerance
    )
    return DisjointPairSourceCompilerControl(
        control_id=(
            f"S{n}-L{left_pair_indices[0]}-{left_pair_indices[1]}-"
            f"R{right_pair_indices[0]}-{right_pair_indices[1]}"
        ),
        n=n,
        transposition_count=transposition_count,
        left_pair_partitions=left_partitions,
        right_pair_partitions=right_partitions,
        natural_source_probability=natural_probability,
        hidden_involution_count=hidden_count,
        left_pair_dimension=left_dimension,
        right_pair_dimension=right_dimension,
        joint_dimension=left_dimension * right_dimension,
        active_joint_carrier_branch_count=branch_count,
        total_joint_branch_probability=probability,
        global_branch_pgm_bayes_success=totals["global_bayes"],
        pair_local_pgm_map_bayes_success=totals["local_bayes"],
        global_advantage_over_pair_local_map=(
            totals["global_bayes"] - totals["local_bayes"]
        ),
        weighted_frame_covariance_fraction=totals["covariance"],
        maximum_frame_covariance_fraction=maxima["covariance"],
        weighted_scaled_diagonal_completeness_residual=totals[
            "diagonal_completeness"
        ],
        maximum_scaled_diagonal_completeness_residual=maxima[
            "diagonal_completeness"
        ],
        weighted_scaled_diagonal_eigenvalue_excess=totals["diagonal_excess"],
        maximum_scaled_diagonal_eigenvalue_excess=maxima["diagonal_excess"],
        weighted_global_effect_factorization_residual=totals[
            "effect_factorization"
        ],
        maximum_global_effect_factorization_residual=maxima[
            "effect_factorization"
        ],
        maximum_covariance_identity_residual=maxima["covariance_identity"],
        maximum_global_pgm_completeness_residual=maxima["global_completeness"],
        maximum_pair_pgm_completeness_residual=maxima["pair_completeness"],
        maximum_channel_normalization_residual=maxima["channel_normalization"],
        nonzero_shared_label_covariance_verified=covariance_nonzero,
        scaled_diagonal_product_fails_povm_verified=diagonal_fails,
        global_pgm_differs_from_pair_local_map_verified=global_differs,
        exact_control_verified=verified,
        status=(
            "shared-label-covariance-falsifies-pair-local-pgm-factorization"
            if verified and covariance_nonzero and diagonal_fails and global_differs
            else "disjoint-pair-compiler-control-degenerate"
            if verified
            else "disjoint-pair-compiler-control-failure"
        ),
    )


def _pair_source_types(source_count: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations_with_replacement(range(source_count), 2))


@lru_cache(maxsize=None)
def audit_natural_disjoint_pair_compiler(
    n: int,
    transposition_count: int,
    *,
    tolerance: float = 1e-9,
) -> tuple[
    NaturalDisjointPairCompilerAggregate,
    tuple[DisjointPairSourceCompilerControl, ...],
]:
    """Average the two-pair compiler boundary over the exact source law."""

    partitions, _, _ = _source_data(n, transposition_count)
    pair_types = _pair_source_types(len(partitions))
    controls = tuple(
        audit_disjoint_pair_source_compiler(
            n,
            transposition_count,
            left,
            right,
            tolerance=tolerance,
        )
        for left, right in itertools.product(pair_types, repeat=2)
    )
    mass = sum(control.natural_source_probability for control in controls)

    def weighted(field: str) -> float:
        return sum(
            control.natural_source_probability * float(getattr(control, field))
            for control in controls
        )

    covariance_mass = sum(
        control.natural_source_probability
        for control in controls
        if control.nonzero_shared_label_covariance_verified
    )
    diagonal_failure_mass = sum(
        control.natural_source_probability
        for control in controls
        if control.scaled_diagonal_product_fails_povm_verified
    )
    verified = (
        abs(mass - 1.0) <= 100 * tolerance
        and all(control.exact_control_verified for control in controls)
        and weighted("maximum_covariance_identity_residual") <= 100 * tolerance
    )
    aggregate = NaturalDisjointPairCompilerAggregate(
        n=n,
        transposition_count=transposition_count,
        hidden_involution_count=controls[0].hidden_involution_count,
        pair_source_type_count=len(pair_types),
        source_quadruple_type_count=len(controls),
        active_joint_carrier_branch_count=sum(
            control.active_joint_carrier_branch_count for control in controls
        ),
        total_natural_source_probability=mass,
        natural_global_branch_pgm_bayes_success=weighted(
            "global_branch_pgm_bayes_success"
        ),
        natural_pair_local_pgm_map_bayes_success=weighted(
            "pair_local_pgm_map_bayes_success"
        ),
        natural_global_advantage_over_pair_local_map=weighted(
            "global_advantage_over_pair_local_map"
        ),
        natural_weighted_frame_covariance_fraction=weighted(
            "weighted_frame_covariance_fraction"
        ),
        natural_weighted_scaled_diagonal_completeness_residual=weighted(
            "weighted_scaled_diagonal_completeness_residual"
        ),
        natural_weighted_scaled_diagonal_eigenvalue_excess=weighted(
            "weighted_scaled_diagonal_eigenvalue_excess"
        ),
        natural_weighted_global_effect_factorization_residual=weighted(
            "weighted_global_effect_factorization_residual"
        ),
        maximum_frame_covariance_fraction=max(
            control.maximum_frame_covariance_fraction for control in controls
        ),
        maximum_scaled_diagonal_completeness_residual=max(
            control.maximum_scaled_diagonal_completeness_residual
            for control in controls
        ),
        maximum_scaled_diagonal_eigenvalue_excess=max(
            control.maximum_scaled_diagonal_eigenvalue_excess
            for control in controls
        ),
        source_mass_with_nonzero_covariance=covariance_mass,
        source_mass_where_scaled_diagonal_product_fails_povm=(
            diagonal_failure_mass
        ),
        all_controls_verified=verified,
        status=(
            "natural-shared-label-pgm-nonfactorization-verified"
            if verified
            and covariance_mass > tolerance
            and diagonal_failure_mass > tolerance
            else "natural-disjoint-pair-compiler-boundary-failure"
        ),
    )
    return aggregate, controls


def perfect_matching_count(n: int) -> int:
    if n < 2 or n % 2:
        raise ValueError("perfect matchings require a positive even degree")
    half = n // 2
    return math.factorial(n) // (2**half * math.factorial(half))


def residual_coupling_scaling_record(
    n: int,
    *,
    threshold_slack: int = 0,
) -> DisjointPairResidualCouplingScalingRecord:
    hidden_count = perfect_matching_count(n)
    copy_count = math.ceil(math.log2(hidden_count)) + threshold_slack
    pair_count = min(math.ceil(math.log2(n)), copy_count // 2)
    residual_blocks = copy_count - pair_count
    return DisjointPairResidualCouplingScalingRecord(
        n=n,
        hidden_involution_count_decimal=str(hidden_count),
        hidden_involution_count_log2=math.log2(hidden_count),
        information_threshold_copy_count=copy_count,
        disjoint_pair_count=pair_count,
        residual_shared_hidden_label_block_count=residual_blocks,
        residual_block_fraction=residual_blocks / copy_count,
        conditioned_state_tensor_factorization_proved=True,
        hypothesis_average_tensor_factorization_proved=False,
        bounded_residual_block_count_proved=False,
        status="logarithmic-pair-depth-leaves-growing-shared-label-frame",
    )


def run_disjoint_pair_branch_pgm_compiler_boundary(
) -> DisjointPairBranchPgmCompilerBoundaryReport:
    natural_runs = [
        audit_natural_disjoint_pair_compiler(3, 1),
        audit_natural_disjoint_pair_compiler(4, 2),
    ]
    natural_aggregates = [item[0] for item in natural_runs]
    natural_controls = tuple(
        control for _, controls in natural_runs for control in controls
    )
    selected_s5 = [
        audit_disjoint_pair_source_compiler(5, 2, (0, 1), (0, 1)),
        audit_disjoint_pair_source_compiler(5, 2, (1, 1), (1, 1)),
    ]
    finite_controls = natural_controls + tuple(selected_s5)
    verified = all(
        aggregate.all_controls_verified for aggregate in natural_aggregates
    ) and all(control.exact_control_verified for control in selected_s5)
    nonfactorization = all(
        control.nonzero_shared_label_covariance_verified
        and control.scaled_diagonal_product_fails_povm_verified
        and control.global_pgm_differs_from_pair_local_map_verified
        for control in selected_s5
    ) and all(
        aggregate.natural_global_advantage_over_pair_local_map > 1e-9
        and aggregate.source_mass_with_nonzero_covariance > 0
        and aggregate.source_mass_where_scaled_diagonal_product_fails_povm > 0
        for aggregate in natural_aggregates
    )
    theorem = DisjointPairBranchPgmCompilerTheorem(
        conditioned_state_factorization=(
            "Disjoint carrier projectors act on separate source pairs, so each "
            "fixed-hidden, fixed-branch state is exactly sigma_h tensor tau_h."
        ),
        shared_label_covariance_identity=(
            "The common hidden label gives bar(omega)=bar(sigma) tensor "
            "bar(tau)+M^-1 sum_h Delta sigma_h tensor Delta tau_h."
        ),
        pgm_factorization_boundary=(
            "A nonzero shared-label covariance enters the global frame inverse "
            "square root, so disjoint physical support alone does not factor the PGM."
        ),
        valid_pair_local_baseline=(
            "Independent pair PGMs followed by maximum-posterior classical "
            "decoding form a valid POVM and are strictly weaker in every reported "
            "nondegenerate aggregate/control."
        ),
        diagonal_product_effect_boundary=(
            "The scaled same-label effects M E_h tensor F_h generally fail "
            "completeness and can sum to an operator with eigenvalue above one."
        ),
        asymptotic_block_count=(
            "At the perfect-matching information threshold, q=ceil(log2 n) "
            "disjoint pair pinches leave k-q=Theta(n log n) tensor blocks tied "
            "to the same hidden label."
        ),
        surviving_compiler_target=(
            "Compile the covariance-aware covariant inverse square root on the "
            "shared-label multiplicity frame, or find an equivalent structured "
            "measurement that retains the disjoint-pair success guarantee."
        ),
        scope=(
            "The exact controls falsify naive pair-local PGM factorization. They "
            "do not prove a quantum query/circuit lower bound and do not exclude "
            "a representation-specific global polar or another decoder."
        ),
        conditioned_state_factorization_proved=True,
        shared_label_covariance_identity_proved=True,
        finite_shared_label_covariance_nonzero_verified=nonfactorization,
        pair_local_pgm_equals_global_branch_pgm=False,
        scaled_diagonal_product_is_povm=False,
        naive_pair_local_branch_pgm_compiler_falsified=nonfactorization,
        covariance_aware_branch_pgm_compiled=False,
        hidden_involution_decoder_compiled=False,
        theorem_verified=verified and nonfactorization,
        status="naive-pair-local-pgm-falsified-covariance-aware-polar-open",
    )
    scaling = [
        residual_coupling_scaling_record(n)
        for n in (8, 16, 32, 64, 128)
    ]
    metrics: dict[str, int | float] = {
        "shared_hidden_label_covariance_identity_theorem_count": int(
            theorem.shared_label_covariance_identity_proved
        ),
        "naive_pair_local_branch_pgm_compiler_no_go_count": int(
            theorem.naive_pair_local_branch_pgm_compiler_falsified
        ),
        "natural_nonfactorization_control_count": len(natural_aggregates),
        "growing_hypothesis_nonfactorization_control_count": len(selected_s5),
        "maximum_control_hidden_involution_count": max(
            control.hidden_involution_count for control in finite_controls
        ),
        "s3_natural_global_branch_pgm_bayes_success": (
            natural_aggregates[0].natural_global_branch_pgm_bayes_success
        ),
        "s3_natural_pair_local_map_bayes_success": (
            natural_aggregates[0].natural_pair_local_pgm_map_bayes_success
        ),
        "s3_natural_global_pair_local_success_gap": (
            natural_aggregates[0].natural_global_advantage_over_pair_local_map
        ),
        "s4_natural_global_branch_pgm_bayes_success": (
            natural_aggregates[1].natural_global_branch_pgm_bayes_success
        ),
        "s4_natural_pair_local_map_bayes_success": (
            natural_aggregates[1].natural_pair_local_pgm_map_bayes_success
        ),
        "s4_natural_global_pair_local_success_gap": (
            natural_aggregates[1].natural_global_advantage_over_pair_local_map
        ),
        "s5_standard_global_pair_local_success_gap": (
            selected_s5[1].global_advantage_over_pair_local_map
        ),
        "s5_standard_weighted_frame_covariance_fraction": (
            selected_s5[1].weighted_frame_covariance_fraction
        ),
        "s5_standard_scaled_diagonal_completeness_residual": (
            selected_s5[1].weighted_scaled_diagonal_completeness_residual
        ),
        "covariance_aware_branch_pgm_compiler_count": 0,
        "hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DisjointPairBranchPgmCompilerBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": (
                "uniform hidden involutions with two disjoint pair-carrier "
                "branches and public Fourier source labels"
            ),
            "candidate_compiler": (
                "independent pair PGMs or scaled same-label tensor-product effects"
            ),
            "valid_baseline": (
                "independent pair-PGM outcomes followed by MAP shared-label decoding"
            ),
            "target": "exact carrier-flagged collective branch PGM",
        },
        theorem=theorem,
        natural_aggregates=natural_aggregates,
        selected_growing_hypothesis_controls=selected_s5,
        worst_natural_controls=sorted(
            natural_controls,
            key=lambda control: control.global_advantage_over_pair_local_map,
            reverse=True,
        )[:16],
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "separate_disjoint_state_factorization_from_pgm_factorization",
                "resolved": True,
                "resolution": "Equation (2) exposes the exact shared-label covariance term.",
            },
            {
                "obligation": "test_pair_local_pgm_as_a_branch_compiler",
                "resolved": True,
                "resolution": (
                    "Natural S3/S4 and selected M=15 S5 controls show nonzero "
                    "covariance, invalid diagonal effects, and a strict success gap."
                ),
            },
            {
                "obligation": "compile_covariance_aware_shared_label_polar",
                "resolved": False,
                "resolution": (
                    "The frame inverse square root remains a joint operation over "
                    "all source blocks sharing the hidden involution."
                ),
            },
            {
                "obligation": "decode_hidden_involution_without_factorial_search",
                "resolved": False,
                "resolution": "No polynomial coherent output map is constructed.",
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Disjoint carrier projectors imply independent hidden labels.",
                "survives": False,
                "response": "The sources are independent, but every factor carries the same h.",
            },
            {
                "challenge": "Tensor-product conditioned states imply a tensor-product PGM.",
                "survives": False,
                "response": "The hypothesis average contains the nonzero covariance in equation (2).",
            },
            {
                "challenge": "Multiplying same-label local PGM effects gives a POVM.",
                "survives": False,
                "response": "The scaled diagonal effect sum fails completeness and can exceed identity.",
            },
            {
                "challenge": "Finite nonfactorization proves every global compiler is hard.",
                "survives": False,
                "response": (
                    "Only the naive pair-local architecture is falsified; a "
                    "covariant representation-specific polar remains open."
                ),
            },
        ],
        primary_literature=[
            {
                "paper_id": "quek-rebentrost-pgm-polar-2021",
                "title": (
                    "Fast algorithm for quantum polar decomposition, pretty-good "
                    "measurements, and the Procrustes problem"
                ),
                "url": "https://arxiv.org/abs/2106.07634",
                "use": (
                    "Generic pure-state PGM/polar implementation benchmark; its "
                    "controlled state-preparation and condition assumptions do "
                    "not supply this mixed shared-label branch polar."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "disjoint_conditioned_state_factorization_proved": True,
            "shared_hidden_label_covariance_identity_proved": True,
            "naive_pair_local_branch_pgm_compiler_falsified": nonfactorization,
            "scaled_same_label_product_effects_form_povm": False,
            "pair_local_pgm_equals_global_branch_pgm": False,
            "covariance_aware_branch_pgm_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Disjoint carrier conditioning preserves information-theoretic "
                "success but leaves a shared-hidden-label covariance in the PGM "
                "frame. The naive local compiler is false and no covariance-aware "
                "polar or decoder is yet compiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved the exact shared-hidden-label covariance decomposition for "
            "disjoint carrier branches and falsified naive pair-local PGM "
            "factorization on natural S3/S4 and M=15 S5 controls. The surviving "
            "target is a covariance-aware covariant multiplicity polar."
        ),
        falsifiers_triggered=[
            "Disjoint carrier supports do not make the hidden labels independent.",
            "The branch-average frame does not generally tensor-factor across disjoint pairs.",
            "Scaled same-label products of pair-PGM effects need not form a POVM.",
            "Independent pair-PGM measurement plus MAP decoding is strictly weaker on the exact controls.",
            "The finite obstruction rules out only the naive local compiler, not every structured global polar.",
        ],
    )


def write_disjoint_pair_branch_pgm_compiler_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_disjoint_pair_branch_pgm_compiler_boundary())
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
                title="Disjoint pair-carrier branch-PGM compiler boundary",
                status="completed-naive-local-compiler-falsified-global-polar-open",
                hypothesis=(
                    "The disjoint-pair accessible-success theorem may admit a "
                    "compiler obtained by composing pair-local PGMs."
                ),
                protocol=(
                    "Derive the shared-label covariance identity, compare exact "
                    "global and pair-local PGM channels, and test normalization "
                    "of scaled same-label product effects."
                ),
                positive_signal=(
                    "A covariance-aware covariant polar or alternative structured "
                    "measurement with the proved disjoint-pair success guarantee."
                ),
                falsifiers=[
                    "disjoint source supports are called independent hypotheses",
                    "same-label product effects are used without a completeness test",
                    "finite PGM existence is called a coherent implementation",
                    "generic state-preparation access is assumed from mixed samples",
                ],
                metrics=[
                    "shared_hidden_label_covariance_identity_theorem_count",
                    "naive_pair_local_branch_pgm_compiler_no_go_count",
                    "s3_natural_global_pair_local_success_gap",
                    "s4_natural_global_pair_local_success_gap",
                    "s5_standard_global_pair_local_success_gap",
                    "covariance_aware_branch_pgm_compiler_count",
                ],
                dependencies=[
                    "self_dual_wreath_carrier_branch_pgm_success_certificate.py",
                    "self_dual_wreath_carrier_conditioned_pgm_boundary.py",
                    "coset_natural_multicopy_pgm_benchmark.py",
                    "mixed-state PGM frame inverse square root",
                ],
                next_actions=[
                    "derive a Fourier block form for the shared-label covariance operator",
                    "search low-rank or sparse covariance closures on natural carrier branches",
                    "compile a controlled multiplicity polar without hypothesis enumeration",
                    "attack any resulting output channel with classical representation algorithms",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-DISJOINT-PAIR-BRANCH-PGM-"
            "COMPILER-BOUNDARY-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary": str(
                        path
                    )
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="DISJOINT-CARRIER-BRANCH-PGM-NOT-PAIR-LOCAL",
                source=registry_experiment_id,
                claim=(
                    "Disjoint carrier projectors make the carrier-branch PGM a "
                    "composition of pair-local PGMs."
                ),
                reason_invalid=(
                    "The same hidden label appears in every factor, producing a "
                    "nonzero covariance in the average frame. Exact S3/S4/S5 "
                    "controls show a global/local success gap."
                ),
                lesson=(
                    "A compiler must implement or bypass the covariance-aware "
                    "shared-label frame inverse square root."
                ),
                applies_to=[
                    registry_candidate_id,
                    "disjoint pair carriers",
                    "branch PGM compiler",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="SCALED-DIAGONAL-PAIR-PGM-EFFECTS-NOT-A-POVM",
                source=registry_experiment_id,
                claim=(
                    "The effects M E_h tensor F_h obtained from two local PGMs "
                    "form the global shared-label PGM."
                ),
                reason_invalid=(
                    "Their sum fails the global support-projector completeness "
                    "condition and can have eigenvalue above one."
                ),
                lesson=(
                    "Retain all independent local outcomes with classical MAP as "
                    "the legal local baseline; do not keep only matching labels."
                ),
                applies_to=[
                    registry_candidate_id,
                    "tensor-product PGM effects",
                    "shared-label discrimination",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_disjoint_pair_branch_pgm_compiler_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
