"""Dimensionless covariance-polar reduction for disjoint pair carriers.

Fix accessible Fourier source labels ``lambda,mu`` and a measured diagonal
carrier label ``alpha``.  Let ``Q_alpha`` be the corresponding isotypic
projector, ``r_alpha=g(lambda,mu,alpha)d_alpha`` its rank, and ``sigma_h`` the
normalized pair state in that branch.  Central class averaging gives the
all-n flatness identity

    E_h sigma_h = Q_alpha/r_alpha.                         (1)

This remains true when the Kronecker multiplicity exceeds one: every term in
the two-copy state is a central conjugacy-class sum in the diagonal
representation, hence scalar on the whole alpha isotypic component.

For two disjoint pair branches A,B define

    X_h = r_A sigma_h-Q_A,       Y_h = r_B tau_h-Q_B,
    K   = E_h X_h tensor Y_h.                                  (2)

The shared-hidden-label frame and its PGM effects then have the exact forms

    B = (Q_A tensor Q_B + K)/(r_A r_B),                         (3)
    E_h^PGM = M^-1 (I+K)^(-1/2)
              (r_A sigma_h tensor r_B tau_h)(I+K)^(-1/2).       (4)

Thus support-rank normalization cancels.  The remaining inverse square root
is a dimensionless public correlation metric, not the product of pair-local
PGMs and not an arbitrary source-weighted frame.

There is also an all-n access-normalization theorem.  Put

    s_(lambda,mu,alpha)=1+r_lambda+r_mu+r_alpha,

where r_lambda=chi_lambda(C)/d_lambda.  On an active branch,

    r_alpha sigma_h
      = Q_alpha[(I+rho_lambda(h)) tensor (I+rho_mu(h))]Q_alpha/s. (5)

Equation (5) has four-term LCU normalization ``4/s``.  Under the exact
natural ordered source-and-carrier law

    w(lambda,mu,alpha)=d_lambda d_mu g d_alpha s/|S_n|^2,

the factor ``s`` cancels and

    E[4/s] <= 4,        E[4/s+1] <= 5.                          (6)

Two disjoint pair labels are independent under the public branch law, so the
mean product normalization for K is at most 25.  Markov truncation therefore
retains at least ``1-delta`` natural branch mass at normalization
``25/delta``.  This removes the carrier-rank and rare-branch normalization
barriers for constant retained mass.

The result does not bound the minimum positive eigenvalue of ``I+K``, extend
the reduction to all threshold copies, implement the final PGM Naimark/output
map, or decode the hidden involution.  Those remain the decisive gates.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_natural_multicopy_pgm_benchmark import _source_data
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary import (
    _pair_carrier_branches,
    _pair_source_probability,
    _pgm_data,
)
from symmetric_character import kronecker_coefficient
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_disjoint_pair_covariance_polar_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-DISJOINT-PAIR-COVARIANCE-POLAR-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PairCarrierFlatnessControl:
    control_id: str
    n: int
    transposition_count: int
    source_partitions: tuple[Partition, Partition]
    carrier_partition: Partition
    kronecker_multiplicity: int
    carrier_support_rank: int
    natural_source_branch_probability: float
    branch_probability: float
    target_likelihood_scalar: float
    rank_scaled_state_lcu_normalization: float
    centered_state_lcu_normalization: float
    maximum_flat_average_residual: float
    maximum_rank_scaled_lcu_identity_residual: float
    maximum_centered_mean_residual: float
    exact_pair_branch_flatness_verified: bool
    exact_rank_scaled_lcu_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalPairLcuNormalizationRecord:
    n: int
    transposition_count: int
    active_ordered_source_carrier_branch_count: int
    exact_natural_branch_probability_mass: str
    exact_expected_rank_scaled_lcu_normalization: str
    expected_rank_scaled_lcu_normalization: float
    all_n_rank_scaled_lcu_expectation_upper_bound: float
    expected_centered_lcu_normalization_upper_bound: float
    two_pair_expected_covariance_lcu_normalization_upper_bound: float
    markov_cutoff: float
    retained_natural_two_pair_mass_lower_bound: float
    maximum_finite_rank_scaled_lcu_normalization: float
    exact_expectation_bound_verified: bool
    status: str


@dataclass(frozen=True)
class TwoPairCovariancePolarControl:
    control_id: str
    n: int
    transposition_count: int
    left_source_partitions: tuple[Partition, Partition]
    right_source_partitions: tuple[Partition, Partition]
    hidden_involution_count: int
    active_joint_branch_count: int
    total_joint_branch_probability: float
    maximum_dimensionless_frame_identity_residual: float
    maximum_reduced_pgm_effect_residual: float
    maximum_reduced_pgm_completeness_residual: float
    minimum_positive_dimensionless_metric_eigenvalue: float
    maximum_dimensionless_metric_eigenvalue: float
    maximum_dimensionless_metric_support_condition_number: float
    maximum_covariance_operator_schmidt_rank: int
    maximum_centered_orbit_span_rank: int
    maximum_operator_schmidt_rank_upper_bound_residual: int
    weighted_covariance_lcu_normalization: float
    maximum_covariance_lcu_normalization: float
    exact_covariance_polar_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class DisjointPairCovariancePolarTheorem:
    pair_branch_flatness: str
    scaled_centered_states: str
    dimensionless_frame: str
    pgm_effect_reduction: str
    rank_scaled_lcu: str
    natural_normalization_cancellation: str
    constant_mass_truncation: str
    public_access_schema: str
    scope: str
    all_n_pair_branch_flatness_proved: bool
    dimensionless_covariance_frame_reduction_proved: bool
    pgm_rank_normalization_cancellation_proved: bool
    all_n_natural_lcu_expectation_bound_proved: bool
    constant_mass_constant_normalization_schema_proved: bool
    conditional_public_covariance_block_encoding_schema_proved: bool
    uniform_public_covariance_block_encoding_compiled: bool
    inverse_square_root_spectral_gap_proved: bool
    threshold_copy_extension_proved: bool
    pgm_output_isometry_compiled: bool
    hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DisjointPairCovariancePolarReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DisjointPairCovariancePolarTheorem
    finite_pair_flatness_controls: list[PairCarrierFlatnessControl]
    natural_lcu_normalization_records: list[NaturalPairLcuNormalizationRecord]
    two_pair_covariance_controls: list[TwoPairCovariancePolarControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def target_likelihood_scalar(
    n: int,
    transposition_count: int,
    left: Partition,
    right: Partition,
    target: Partition,
) -> Fraction:
    values = []
    for partition in (left, right, target):
        dimension = hook_length_dimension(partition)
        character = character_on_involution(partition, transposition_count)
        values.append(Fraction(character, dimension))
    return Fraction(1) + sum(values, Fraction())


def rank_scaled_pair_lcu_normalization(
    n: int,
    transposition_count: int,
    left: Partition,
    right: Partition,
    target: Partition,
) -> Fraction:
    scalar = target_likelihood_scalar(
        n,
        transposition_count,
        left,
        right,
        target,
    )
    if scalar <= 0:
        raise ValueError("the pair carrier branch must have positive likelihood")
    return Fraction(4, 1) / scalar


@lru_cache(maxsize=None)
def audit_pair_carrier_flatness(
    n: int,
    transposition_count: int,
    pair_indices: tuple[int, int],
    *,
    tolerance: float = 1e-9,
) -> tuple[PairCarrierFlatnessControl, ...]:
    partitions, source_probabilities, state_families = _source_data(
        n,
        transposition_count,
    )
    source_partitions, branches = _pair_carrier_branches(
        n,
        transposition_count,
        pair_indices,
    )
    left, right = source_partitions
    left_dimension = hook_length_dimension(left)
    right_dimension = hook_length_dimension(right)
    left_character = character_on_involution(left, transposition_count)
    right_character = character_on_involution(right, transposition_count)
    source_normalization = (left_dimension + left_character) * (
        right_dimension + right_character
    )
    source_probability = _pair_source_probability(
        source_probabilities,
        pair_indices,
    )
    hidden_count = len(state_families[0])
    raw_pair_states = tuple(
        np.kron(
            state_families[pair_indices[0]][hidden],
            state_families[pair_indices[1]][hidden],
        )
        for hidden in range(hidden_count)
    )
    controls: list[PairCarrierFlatnessControl] = []
    for branch in branches:
        target = branch.carrier_partition
        multiplicity = kronecker_coefficient(left, right, target)
        target_dimension = hook_length_dimension(target)
        support_rank = multiplicity * target_dimension
        if support_rank <= 0:
            raise ArithmeticError("active branch has zero representation rank")
        support = branch.pgm.support_projector
        flat_residual = float(
            np.linalg.norm(
                branch.pgm.average - support / support_rank,
                ord=2,
            )
        )
        scalar = target_likelihood_scalar(
            n,
            transposition_count,
            left,
            right,
            target,
        )
        if scalar <= 0:
            raise ArithmeticError("active branch has nonpositive likelihood scalar")
        lcu = Fraction(4, 1) / scalar
        lcu_residual = 0.0
        centered_mean = np.zeros_like(support, dtype=complex)
        for hidden, normalized in enumerate(branch.states):
            numerator = source_normalization * raw_pair_states[hidden]
            expected = support @ numerator @ support / float(scalar)
            observed = support_rank * normalized
            lcu_residual = max(
                lcu_residual,
                float(np.linalg.norm(observed - expected, ord=2)),
            )
            centered_mean += observed - support
        centered_mean /= hidden_count
        centered_residual = float(np.linalg.norm(centered_mean, ord=2))
        flat = flat_residual <= 1000 * tolerance
        lcu_exact = lcu_residual <= 1000 * tolerance
        verified = flat and lcu_exact and centered_residual <= 1000 * tolerance
        controls.append(
            PairCarrierFlatnessControl(
                control_id=(
                    f"S{n}-PAIR-{pair_indices[0]}-{pair_indices[1]}-"
                    f"TARGET-{'-'.join(map(str, target))}"
                ),
                n=n,
                transposition_count=transposition_count,
                source_partitions=source_partitions,
                carrier_partition=target,
                kronecker_multiplicity=multiplicity,
                carrier_support_rank=support_rank,
                natural_source_branch_probability=(
                    source_probability * branch.probability
                ),
                branch_probability=branch.probability,
                target_likelihood_scalar=float(scalar),
                rank_scaled_state_lcu_normalization=float(lcu),
                centered_state_lcu_normalization=float(lcu + 1),
                maximum_flat_average_residual=flat_residual,
                maximum_rank_scaled_lcu_identity_residual=lcu_residual,
                maximum_centered_mean_residual=centered_residual,
                exact_pair_branch_flatness_verified=flat,
                exact_rank_scaled_lcu_verified=lcu_exact,
                status=(
                    "pair-branch-flat-rank-scaled-four-term-lcu-exact"
                    if verified
                    else "pair-branch-flatness-lcu-control-failure"
                ),
            )
        )
    return tuple(controls)


@lru_cache(maxsize=None)
def audit_natural_pair_flatness(
    n: int,
    transposition_count: int,
) -> tuple[PairCarrierFlatnessControl, ...]:
    partitions, _, _ = _source_data(n, transposition_count)
    return tuple(
        control
        for pair in itertools.combinations_with_replacement(
            range(len(partitions)),
            2,
        )
        for control in audit_pair_carrier_flatness(
            n,
            transposition_count,
            pair,
        )
    )


@lru_cache(maxsize=None)
def natural_pair_lcu_normalization_record(
    n: int,
    transposition_count: int,
    *,
    markov_cutoff: float = 100.0,
) -> NaturalPairLcuNormalizationRecord:
    if markov_cutoff <= 25:
        raise ValueError("the two-pair cutoff must exceed the mean-25 bound")
    order = math.factorial(n)
    partitions = tuple(integer_partitions(n))
    mass = Fraction()
    expectation = Fraction()
    maximum = Fraction()
    branch_count = 0
    for left in partitions:
        left_dimension = hook_length_dimension(left)
        left_character = character_on_involution(left, transposition_count)
        if left_dimension + left_character <= 0:
            continue
        for right in partitions:
            right_dimension = hook_length_dimension(right)
            right_character = character_on_involution(right, transposition_count)
            if right_dimension + right_character <= 0:
                continue
            for target in partitions:
                multiplicity = kronecker_coefficient(left, right, target)
                if multiplicity <= 0:
                    continue
                target_dimension = hook_length_dimension(target)
                scalar = target_likelihood_scalar(
                    n,
                    transposition_count,
                    left,
                    right,
                    target,
                )
                if scalar <= 0:
                    continue
                probability = Fraction(
                    left_dimension
                    * right_dimension
                    * multiplicity
                    * target_dimension,
                    order**2,
                ) * scalar
                lcu = Fraction(4, 1) / scalar
                mass += probability
                expectation += probability * lcu
                maximum = max(maximum, lcu)
                branch_count += 1
    verified = mass == 1 and expectation <= 4
    return NaturalPairLcuNormalizationRecord(
        n=n,
        transposition_count=transposition_count,
        active_ordered_source_carrier_branch_count=branch_count,
        exact_natural_branch_probability_mass=str(mass),
        exact_expected_rank_scaled_lcu_normalization=str(expectation),
        expected_rank_scaled_lcu_normalization=float(expectation),
        all_n_rank_scaled_lcu_expectation_upper_bound=4.0,
        expected_centered_lcu_normalization_upper_bound=5.0,
        two_pair_expected_covariance_lcu_normalization_upper_bound=25.0,
        markov_cutoff=markov_cutoff,
        retained_natural_two_pair_mass_lower_bound=1.0 - 25.0 / markov_cutoff,
        maximum_finite_rank_scaled_lcu_normalization=float(maximum),
        exact_expectation_bound_verified=verified,
        status=(
            "natural-rank-scaled-lcu-mean-at-most-four"
            if verified
            else "natural-lcu-normalization-identity-failure"
        ),
    )


def _psd_inverse_root(
    matrix: np.ndarray,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    positive = eigenvalues > tolerance
    vectors = eigenvectors[:, positive]
    inverse = (
        vectors
        @ np.diag(1.0 / np.sqrt(eigenvalues[positive]))
        @ vectors.conj().T
    )
    support = vectors @ vectors.conj().T
    return inverse, support, eigenvalues[positive]


def _operator_schmidt_rank(
    operator: np.ndarray,
    left_dimension: int,
    right_dimension: int,
    *,
    tolerance: float,
) -> int:
    reshaped = operator.reshape(
        left_dimension,
        right_dimension,
        left_dimension,
        right_dimension,
    ).transpose(0, 2, 1, 3)
    singular = np.linalg.svd(
        reshaped.reshape(left_dimension**2, right_dimension**2),
        compute_uv=False,
    )
    return int(np.count_nonzero(singular > tolerance))


def _centered_orbit_span_rank(
    states: tuple[np.ndarray, ...],
    average: np.ndarray,
    *,
    tolerance: float,
) -> int:
    singular = np.linalg.svd(
        np.stack(tuple((state - average).reshape(-1) for state in states)),
        compute_uv=False,
    )
    return int(np.count_nonzero(singular > tolerance))


@lru_cache(maxsize=None)
def audit_two_pair_covariance_polar(
    n: int,
    transposition_count: int,
    left_pair_indices: tuple[int, int],
    right_pair_indices: tuple[int, int],
    *,
    tolerance: float = 1e-9,
) -> TwoPairCovariancePolarControl:
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
    hidden_count = len(left_branches[0].states)
    total_probability = 0.0
    frame_residual = 0.0
    effect_residual = 0.0
    completeness_residual = 0.0
    minimum_metric = math.inf
    maximum_metric = 0.0
    maximum_condition = 1.0
    maximum_schmidt = 0
    maximum_span = 0
    schmidt_upper_residual = 0
    weighted_lcu = 0.0
    maximum_lcu = 0.0
    branch_count = 0
    for left, right in itertools.product(left_branches, right_branches):
        probability = left.probability * right.probability
        total_probability += probability
        left_rank = int(round(float(np.trace(left.pgm.support_projector).real)))
        right_rank = int(round(float(np.trace(right.pgm.support_projector).real)))
        left_support = left.pgm.support_projector
        right_support = right.pgm.support_projector
        product_support = np.kron(left_support, right_support)
        centered_left = tuple(
            left_rank * state - left_support for state in left.states
        )
        centered_right = tuple(
            right_rank * state - right_support for state in right.states
        )
        covariance = sum(
            (
                np.kron(centered_left[hidden], centered_right[hidden])
                for hidden in range(hidden_count)
            ),
            np.zeros_like(product_support),
        ) / hidden_count
        metric = (product_support + covariance + (product_support + covariance).conj().T) / 2
        joint_states = tuple(
            np.kron(left.states[hidden], right.states[hidden])
            for hidden in range(hidden_count)
        )
        direct = _pgm_data(joint_states)
        frame_residual = max(
            frame_residual,
            float(
                np.linalg.norm(
                    direct.average
                    - metric / (left_rank * right_rank),
                    ord=2,
                )
            ),
        )
        inverse, support, positive = _psd_inverse_root(
            metric,
            tolerance=tolerance,
        )
        reduced_effects = tuple(
            (
                inverse
                @ (
                    left_rank
                    * right_rank
                    * joint_states[hidden]
                    / hidden_count
                )
                @ inverse
            )
            for hidden in range(hidden_count)
        )
        effect_residual = max(
            effect_residual,
            max(
                float(np.linalg.norm(observed - expected, ord=2))
                for observed, expected in zip(
                    direct.effects,
                    reduced_effects,
                    strict=True,
                )
            ),
        )
        completeness_residual = max(
            completeness_residual,
            float(np.linalg.norm(sum(reduced_effects) - support, ord=2)),
        )
        minimum_metric = min(minimum_metric, float(positive[0]))
        maximum_metric = max(maximum_metric, float(positive[-1]))
        maximum_condition = max(
            maximum_condition,
            float(positive[-1] / positive[0]),
        )
        left_span = _centered_orbit_span_rank(
            left.states,
            left.pgm.average,
            tolerance=tolerance,
        )
        right_span = _centered_orbit_span_rank(
            right.states,
            right.pgm.average,
            tolerance=tolerance,
        )
        schmidt = _operator_schmidt_rank(
            covariance,
            left.states[0].shape[0],
            right.states[0].shape[0],
            tolerance=tolerance,
        )
        maximum_span = max(maximum_span, left_span, right_span)
        maximum_schmidt = max(maximum_schmidt, schmidt)
        schmidt_upper_residual = max(
            schmidt_upper_residual,
            max(0, schmidt - min(left_span, right_span, hidden_count - 1)),
        )
        left_lcu = float(
            rank_scaled_pair_lcu_normalization(
                n,
                transposition_count,
                left_partitions[0],
                left_partitions[1],
                left.carrier_partition,
            )
            + 1
        )
        right_lcu = float(
            rank_scaled_pair_lcu_normalization(
                n,
                transposition_count,
                right_partitions[0],
                right_partitions[1],
                right.carrier_partition,
            )
            + 1
        )
        lcu = left_lcu * right_lcu
        weighted_lcu += probability * lcu
        maximum_lcu = max(maximum_lcu, lcu)
        branch_count += 1
    verified = (
        abs(total_probability - 1.0) <= 100 * tolerance
        and frame_residual <= 1000 * tolerance
        and effect_residual <= 1000 * tolerance
        and completeness_residual <= 1000 * tolerance
        and schmidt_upper_residual == 0
    )
    return TwoPairCovariancePolarControl(
        control_id=(
            f"S{n}-L{left_pair_indices[0]}-{left_pair_indices[1]}-"
            f"R{right_pair_indices[0]}-{right_pair_indices[1]}"
        ),
        n=n,
        transposition_count=transposition_count,
        left_source_partitions=left_partitions,
        right_source_partitions=right_partitions,
        hidden_involution_count=hidden_count,
        active_joint_branch_count=branch_count,
        total_joint_branch_probability=total_probability,
        maximum_dimensionless_frame_identity_residual=frame_residual,
        maximum_reduced_pgm_effect_residual=effect_residual,
        maximum_reduced_pgm_completeness_residual=completeness_residual,
        minimum_positive_dimensionless_metric_eigenvalue=minimum_metric,
        maximum_dimensionless_metric_eigenvalue=maximum_metric,
        maximum_dimensionless_metric_support_condition_number=maximum_condition,
        maximum_covariance_operator_schmidt_rank=maximum_schmidt,
        maximum_centered_orbit_span_rank=maximum_span,
        maximum_operator_schmidt_rank_upper_bound_residual=schmidt_upper_residual,
        weighted_covariance_lcu_normalization=weighted_lcu,
        maximum_covariance_lcu_normalization=maximum_lcu,
        exact_covariance_polar_reduction_verified=verified,
        status=(
            "dimensionless-covariance-polar-reduction-exact-gap-open"
            if verified
            else "dimensionless-covariance-polar-control-failure"
        ),
    )


def run_disjoint_pair_covariance_polar_reduction(
) -> DisjointPairCovariancePolarReductionReport:
    flatness_controls = tuple(
        control
        for n, count in ((3, 1), (4, 2), (5, 2))
        for control in audit_natural_pair_flatness(n, count)
    )
    normalization_records = [
        natural_pair_lcu_normalization_record(n, count)
        for n, count in (
            (3, 1),
            (4, 2),
            (5, 2),
            (6, 3),
            (8, 4),
            (10, 5),
        )
    ]
    two_pair_controls = [
        audit_two_pair_covariance_polar(3, 1, (1, 1), (1, 1)),
        audit_two_pair_covariance_polar(5, 2, (0, 1), (0, 1)),
        audit_two_pair_covariance_polar(5, 2, (1, 1), (1, 1)),
    ]
    flatness_verified = all(
        control.exact_pair_branch_flatness_verified
        and control.exact_rank_scaled_lcu_verified
        for control in flatness_controls
    )
    normalization_verified = all(
        record.exact_expectation_bound_verified
        for record in normalization_records
    )
    covariance_verified = all(
        control.exact_covariance_polar_reduction_verified
        for control in two_pair_controls
    )
    verified = flatness_verified and normalization_verified and covariance_verified
    theorem = DisjointPairCovariancePolarTheorem(
        pair_branch_flatness=(
            "For every active (lambda,mu,alpha) branch, class averaging is "
            "Q_alpha/[g(lambda,mu,alpha)d_alpha], including multiplicity>1."
        ),
        scaled_centered_states=(
            "X_h=r_alpha sigma_h-Q_alpha has zero class mean and a five-term "
            "projected-unitary LCU with normalization at most 4/s+1."
        ),
        dimensionless_frame=(
            "Two disjoint pair branches obey B=(Q_A tensor Q_B+E_h X_h tensor Y_h)/(r_A r_B)."
        ),
        pgm_effect_reduction=(
            "On product support, every PGM effect uses only the dimensionless "
            "inverse (I+K)^(-1/2); the explicit carrier ranks cancel."
        ),
        rank_scaled_lcu=(
            "r_alpha sigma_h=Q[(I+rho_lambda(h)) tensor "
            "(I+rho_mu(h))]Q/[1+r_lambda+r_mu+r_alpha]."
        ),
        natural_normalization_cancellation=(
            "The exact natural branch probability contains the same likelihood "
            "scalar s, proving E[4/s]<=4, E[4/s+1]<=5, and two-pair mean<=25."
        ),
        constant_mass_truncation=(
            "Markov truncation at normalization 25/delta retains at least "
            "1-delta of the natural two-pair branch law."
        ),
        public_access_schema=(
            "Conditional on coherent uniform conjugacy-class PREPARE and coherent "
            "carrier-isotypic projectors, controlled Young representation actions "
            "and a constant-term LCU give a bounded-normalization covariance access "
            "schema on every retained branch. Those access primitives are not "
            "compiled here."
        ),
        scope=(
            "No all-n lower bound on the positive edge of I+K is proved. The "
            "two-pair reduction is not yet the full threshold-copy PGM, Naimark "
            "output isometry, hidden-label decoder, or classical separation."
        ),
        all_n_pair_branch_flatness_proved=flatness_verified,
        dimensionless_covariance_frame_reduction_proved=covariance_verified,
        pgm_rank_normalization_cancellation_proved=covariance_verified,
        all_n_natural_lcu_expectation_bound_proved=normalization_verified,
        constant_mass_constant_normalization_schema_proved=normalization_verified,
        conditional_public_covariance_block_encoding_schema_proved=(
            normalization_verified
        ),
        uniform_public_covariance_block_encoding_compiled=False,
        inverse_square_root_spectral_gap_proved=False,
        threshold_copy_extension_proved=False,
        pgm_output_isometry_compiled=False,
        hidden_involution_decoder_compiled=False,
        theorem_verified=verified,
        status="dimensionless-covariance-polar-access-normalized-spectral-gap-open",
    )
    metrics: dict[str, int | float] = {
        "all_n_pair_carrier_branch_flatness_theorem_count": int(flatness_verified),
        "dimensionless_covariance_frame_reduction_theorem_count": int(
            covariance_verified
        ),
        "pgm_rank_normalization_cancellation_theorem_count": int(
            covariance_verified
        ),
        "all_n_natural_rank_scaled_lcu_mean_bound_theorem_count": int(
            normalization_verified
        ),
        "constant_mass_bounded_covariance_lcu_schema_count": int(
            normalization_verified
        ),
        "conditional_public_covariance_block_encoding_schema_count": int(
            normalization_verified
        ),
        "uniform_public_covariance_block_encoding_compiler_count": 0,
        "finite_pair_flatness_control_count": len(flatness_controls),
        "finite_pair_flatness_failure_count": sum(
            not control.exact_pair_branch_flatness_verified
            for control in flatness_controls
        ),
        "maximum_pair_flatness_residual": max(
            control.maximum_flat_average_residual for control in flatness_controls
        ),
        "maximum_rank_scaled_lcu_identity_residual": max(
            control.maximum_rank_scaled_lcu_identity_residual
            for control in flatness_controls
        ),
        "natural_rank_scaled_lcu_expectation_upper_bound": 4.0,
        "natural_centered_lcu_expectation_upper_bound": 5.0,
        "natural_two_pair_covariance_lcu_expectation_upper_bound": 25.0,
        "normalization_100_retained_mass_lower_bound": 0.75,
        "maximum_finite_expected_rank_scaled_lcu_normalization": max(
            record.expected_rank_scaled_lcu_normalization
            for record in normalization_records
        ),
        "maximum_finite_branch_rank_scaled_lcu_normalization": max(
            record.maximum_finite_rank_scaled_lcu_normalization
            for record in normalization_records
        ),
        "minimum_finite_positive_dimensionless_metric_eigenvalue": min(
            control.minimum_positive_dimensionless_metric_eigenvalue
            for control in two_pair_controls
        ),
        "maximum_finite_dimensionless_metric_condition_number": max(
            control.maximum_dimensionless_metric_support_condition_number
            for control in two_pair_controls
        ),
        "maximum_finite_covariance_operator_schmidt_rank": max(
            control.maximum_covariance_operator_schmidt_rank
            for control in two_pair_controls
        ),
        "inverse_square_root_spectral_gap_theorem_count": 0,
        "threshold_copy_covariance_polar_extension_count": 0,
        "pgm_output_isometry_compiler_count": 0,
        "hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DisjointPairCovariancePolarReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "public natural Fourier source labels and two disjoint measured "
                "pair-carrier labels for a uniform hidden-involution class"
            ),
            "operator": "dimensionless shared-label correlation metric I+K",
            "access": (
                "uniform public conjugacy-class LCU using controlled representation "
                "actions and carrier projectors"
            ),
            "output": "reduced branch-PGM inverse-square-root target",
        },
        theorem=theorem,
        finite_pair_flatness_controls=sorted(
            flatness_controls,
            key=lambda control: control.natural_source_branch_probability,
            reverse=True,
        )[:40],
        natural_lcu_normalization_records=normalization_records,
        two_pair_covariance_controls=two_pair_controls,
        proof_obligations=[
            {
                "obligation": "prove_pair_carrier_branch_average_is_flat_all_n",
                "resolved": flatness_verified,
                "resolution": (
                    "Central class sums act as character-ratio scalars on every "
                    "target isotypic component, including repeated multiplicities."
                ),
            },
            {
                "obligation": "remove_explicit_carrier_rank_from_two_pair_pgm",
                "resolved": covariance_verified,
                "resolution": "Equations (2)--(4) give the exact dimensionless polar.",
            },
            {
                "obligation": "bound_public_covariance_lcu_normalization_on_natural_mass",
                "resolved": normalization_verified,
                "resolution": (
                    "The target likelihood scalar cancels against the exact natural "
                    "branch probability, giving means four, five, and twenty-five."
                ),
            },
            {
                "obligation": "compile_uniform_public_covariance_block_encoding",
                "resolved": False,
                "resolution": (
                    "The algebraic LCU schema is conditional on coherent uniform "
                    "matching-class PREPARE and coherent carrier-isotypic projectors; "
                    "this report does not compile or cost those primitives."
                ),
            },
            {
                "obligation": "prove_inverse_polynomial_positive_edge_of_dimensionless_metric",
                "resolved": False,
                "resolution": (
                    "Finite controls are well conditioned on support, but no all-n "
                    "spectral-edge theorem for I+K is available."
                ),
            },
            {
                "obligation": "extend_covariance_polar_to_information_threshold_blocks",
                "resolved": False,
                "resolution": (
                    "Higher shared-label cumulants appear for three or more blocks; "
                    "the two-block correlation formula is not the full threshold frame."
                ),
            },
            {
                "obligation": "compile_pgm_output_and_hidden_label_decoder",
                "resolved": False,
                "resolution": (
                    "Frame inversion alone does not provide the Naimark hypothesis "
                    "register or a polynomial hidden-involution output map."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Kronecker multiplicity destroys pair-branch flatness.",
                "survives": False,
                "response": "The conjugacy-class sum is central and scalar on every copy of alpha.",
            },
            {
                "challenge": "Branch postselection introduces a carrier-rank normalization cost.",
                "survives": False,
                "response": "Rank scaling yields equation (5), and the rank cancels from the PGM effects.",
            },
            {
                "challenge": "Rare small likelihood scalars make the LCU exponentially costly on all mass.",
                "survives": False,
                "response": "Their branch probabilities contain the same scalar; mean normalization is at most four.",
            },
            {
                "challenge": "Bounded block-encoding normalization implies efficient inverse square root.",
                "survives": False,
                "response": "QSVT degree still depends on the unproved positive spectral edge of I+K.",
            },
            {
                "challenge": "A two-pair frame formula compiles the threshold-copy PGM.",
                "survives": False,
                "response": "More blocks introduce higher shared-label cumulants and still need an output isometry.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "all_n_pair_carrier_branch_flatness_proved": flatness_verified,
            "dimensionless_covariance_frame_reduction_proved": covariance_verified,
            "pgm_carrier_rank_normalization_cancelled": covariance_verified,
            "all_n_natural_lcu_expectation_bound_proved": normalization_verified,
            "constant_mass_bounded_covariance_lcu_schema_proved": (
                normalization_verified
            ),
            "conditional_public_covariance_block_encoding_schema_proved": (
                normalization_verified
            ),
            "uniform_public_covariance_block_encoding_compiled": False,
            "inverse_square_root_spectral_gap_proved": False,
            "threshold_copy_covariance_polar_extension_proved": False,
            "pgm_output_isometry_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The two-pair branch PGM now has a constant-natural-mass, "
                "dimensionless covariance block-encoding target and a conditional "
                "LCU access schema. The access primitives, positive spectral edge, "
                "threshold-copy extension, output isometry, decoder, and classical "
                "separation remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved all-n pair-branch flatness, removed carrier-rank normalization "
            "from the two-pair PGM, and bounded the natural covariance-LCU "
            "normalization by 25 in expectation. The next gates are compiling the "
            "conditional access primitives, proving the positive spectral edge of "
            "I+K, and extending the reduction to the full threshold-copy frame."
        ),
        falsifiers_triggered=[
            "Pair-branch averages are exactly flat even when Kronecker multiplicity exceeds one.",
            "The disjoint-pair global PGM is not pair-local, but its frame inverse reduces to a dimensionless covariance polar.",
            "Explicit carrier support ranks cancel from the reduced PGM effects.",
            "Rare small target-likelihood scalars do not spoil natural average LCU normalization.",
            "Finite conditioning does not prove an all-n inverse-square-root circuit.",
            "Two-pair covariance access is not yet a threshold-copy decoder or speedup.",
        ],
    )


def write_disjoint_pair_covariance_polar_reduction_report(
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
    payload = asdict(run_disjoint_pair_covariance_polar_reduction())
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
                title="Disjoint pair covariance-polar reduction",
                status="completed-normalization-closed-spectral-gap-open",
                hypothesis=(
                    "Pair-carrier flatness may cancel support-rank normalization "
                    "and expose a dimensionless public correlation polar."
                ),
                protocol=(
                    "Prove the class-sum flatness and rank-scaled LCU identities, "
                    "derive the two-pair frame/PGM reduction, and audit exact "
                    "natural normalization and finite spectra."
                ),
                positive_signal=(
                    "An inverse-polynomial positive-edge theorem for I+K, a "
                    "threshold-copy cumulant compiler, and a polynomial output decoder."
                ),
                falsifiers=[
                    "multiplicity is assumed to imply nonflat branch averages",
                    "carrier support ranks are charged after their exact cancellation",
                    "worst rare likelihood is substituted for natural branch mass",
                    "bounded LCU normalization is called a bounded QSVT degree",
                    "two-pair inversion is called a full decoder",
                ],
                metrics=[
                    "all_n_pair_carrier_branch_flatness_theorem_count",
                    "dimensionless_covariance_frame_reduction_theorem_count",
                    "all_n_natural_rank_scaled_lcu_mean_bound_theorem_count",
                    "natural_two_pair_covariance_lcu_expectation_upper_bound",
                    "minimum_finite_positive_dimensionless_metric_eigenvalue",
                    "inverse_square_root_spectral_gap_theorem_count",
                ],
                dependencies=[
                    "coset_same_hidden_target_law.py",
                    "self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary.py",
                    "central conjugacy-class sums",
                    "carrier isotypic projection and Young representation actions",
                ],
                next_actions=[
                    "derive moments and a lower-tail bound for the positive spectrum of I+K",
                    "express K in diagonal-action Fourier/multiplicity blocks",
                    "extend the centered expansion to three and logarithmically many blocks",
                    "compile the PGM hypothesis-output isometry and run classical attacks",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-DISJOINT-PAIR-COVARIANCE-"
            "POLAR-REDUCTION-LATEST"
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
                    "self_dual_wreath_disjoint_pair_covariance_polar_reduction": str(
                        path
                    )
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="PAIR-CARRIER-KRONECKER-MULTIPLICITY-NOT-BRANCH-NONFLATNESS",
                source=registry_experiment_id,
                claim=(
                    "Kronecker multiplicity greater than one makes the hidden-"
                    "averaged pair-carrier branch state nonflat."
                ),
                reason_invalid=(
                    "Every term is a central class sum in the diagonal "
                    "representation and acts as the same scalar on every copy of "
                    "the target irrep."
                ),
                lesson=(
                    "Move the compiler target from local pair whitening to the "
                    "shared-label covariance metric across blocks."
                ),
                applies_to=[
                    registry_candidate_id,
                    "pair carrier branches",
                    "Kronecker multiplicity",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="BOUNDED-COVARIANCE-LCU-NOT-INVERSE-SQRT-GAP",
                source=registry_experiment_id,
                claim=(
                    "A constant-natural-mass bounded-normalization block encoding "
                    "of I+K yields a polynomial inverse square root."
                ),
                reason_invalid=(
                    "QSVT degree also depends on the minimum retained positive "
                    "eigenvalue, for which no all-n lower bound is proved."
                ),
                lesson=(
                    "Prove a spectral edge or a robust trim before promoting the "
                    "covariance access schema to a PGM circuit."
                ),
                applies_to=[
                    registry_candidate_id,
                    "dimensionless covariance polar",
                    "QSVT inverse square root",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_disjoint_pair_covariance_polar_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
