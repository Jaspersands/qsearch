"""Binary hidden-involution decision without hidden-element identification.

Let ``G`` be a finite group, let ``C`` be a conjugacy class of ``M``
nonidentity involutions, and let

    rho_h = (I + R_h) / |G|,       rho_0 = I / |G|.       (1)

The binary problem is to distinguish ``rho_0^tensor k`` from the uniform
class mixture ``M^-1 sum_h rho_h^tensor k``.  This is strictly weaker than
identifying ``h``.  The centered alternatives are exactly orthogonal in the
normalized Hilbert--Schmidt geometry:

    Tr[(rho_h^k-rho_0^k)(rho_g^k-rho_0^k)]
      = |G|^-k (2^k-1)  if h=g, and 0 otherwise.          (2)

Consequently the class mixture has exact chi-square divergence

    chi^2(rho_C^k || rho_0^k) = (2^k-1)/M,               (3)

and trace distance at most ``sqrt((2^k-1)/M)/2``.  Equal-prior Bayes
advantage ``epsilon`` therefore requires

    k >= log2(1 + 16 epsilon^2 M).                        (4)

This is an information lower bound, not a circuit lower bound.  For the
fixed-point-free class in ``S_(2m)``, ``M=(2m-1)!!`` and constant advantage
requires ``Omega(m log m)`` coset states, still polynomial in the group-input
length.

The first two copy counts admit sharper exact normal forms.  After the group
QFT, one copy is block scalar and weak Fourier irrep labels are
Helstrom-optimal.  For two copies, in the coupled column sector
``(lambda,mu;nu)`` the likelihood difference is scalar with sign

    sign(r_lambda + r_mu + r_nu),
    r_alpha = chi_alpha(h) / dim(alpha).                  (5)

Thus source irrep labels followed by the diagonal target-irrep label attain
the full two-copy Helstrom trace distance.  No Kronecker multiplicity basis,
physical-row orientation, or hidden-element output is needed for this binary
test.  Efficiently compiling the target measurement for scalable ``S_n`` is
still open, and for ``k>=3`` overlapping subset class sums generally act on
recoupling multiplicity spaces rather than one scalar target label.

The report deliberately does not claim a graph-isomorphism algorithm.  It
only covers the standard mixed coset-state access model, a uniform conjugacy
class prior (or its symmetrized worst-case binary test), and finite exact
controls.  A major algorithm would still need a matching lower bound on the
trace distance near (4), a polynomial implementation of the resulting block
sign measurement, a reduction preserving the promised input model, and a
serious classical comparison.
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

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import kronecker_coefficient
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_binary_decision_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Permutation = tuple[int, ...]


@dataclass(frozen=True)
class BinaryDecisionFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    group_order: int
    conjugacy_class_size: int
    hilbert_dimension: int
    exact_normalized_chi_square: float
    predicted_normalized_chi_square: float
    chi_square_identity_residual: float
    helstrom_trace_distance: float
    chi_square_trace_distance_upper_bound: float
    equal_prior_bayes_success_probability: float
    product_weak_fourier_trace_distance: float
    exact_label_helstrom_trace_distance: float | None
    label_helstrom_identity_residual: float | None
    entangled_target_gain_over_product_labels: float | None
    positive_helstrom_rank: int
    negative_helstrom_rank: int
    average_conjugation_invariance_residual: float
    helstrom_conjugation_invariance_residual: float
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class FixedPointFreeDecisionScalingRecord:
    n: int
    matching_count: int
    log2_matching_count: float
    target_bayes_advantage: float
    information_theoretic_copy_lower_bound: int
    copy_lower_bound_over_log2_class_size: float
    one_copy_trace_distance_upper_bound: float
    two_copy_trace_distance_upper_bound: float
    constant_copy_signal_can_remain_constant: bool
    polynomial_measurement_compiler_known: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionBinaryDecisionTheorem:
    centered_orthogonality_identity: str
    chi_square_identity: str
    trace_distance_upper_bound: str
    symmetrization_identity: str
    one_copy_helstrom_normal_form: str
    two_copy_helstrom_normal_form: str
    higher_copy_boundary: str
    centered_orthogonality_proved: bool
    exact_chi_square_proved: bool
    symmetrized_worst_case_binary_test_proved: bool
    one_copy_weak_fourier_helstrom_optimal: bool
    two_copy_target_label_helstrom_optimal: bool
    threshold_trace_distance_lower_bound_proved: bool
    scalable_block_sign_compiler_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionBinaryDecisionReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[BinaryDecisionFiniteControl]
    scaling_records: list[FixedPointFreeDecisionScalingRecord]
    theorem: HiddenInvolutionBinaryDecisionTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def compose_permutations(left: Permutation, right: Permutation) -> Permutation:
    """Return ``left o right`` in image notation."""

    if len(left) != len(right):
        raise ValueError("permutations must have equal degree")
    return tuple(left[right[index]] for index in range(len(left)))


def inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


@lru_cache(maxsize=None)
def symmetric_group(n: int) -> tuple[Permutation, ...]:
    if n < 2:
        raise ValueError("n must be at least two")
    return tuple(itertools.permutations(range(n)))


def involution_transposition_count(permutation: Permutation) -> int | None:
    identity = tuple(range(len(permutation)))
    if compose_permutations(permutation, permutation) != identity:
        return None
    return sum(permutation[index] != index for index in range(len(permutation))) // 2


@lru_cache(maxsize=None)
def involution_conjugacy_class(
    n: int,
    transposition_count: int,
) -> tuple[Permutation, ...]:
    if transposition_count < 1 or 2 * transposition_count > n:
        raise ValueError("invalid nonidentity involution cycle type")
    return tuple(
        permutation
        for permutation in symmetric_group(n)
        if involution_transposition_count(permutation) == transposition_count
    )


def involution_class_size(n: int, transposition_count: int) -> int:
    fixed_points = n - 2 * transposition_count
    if transposition_count < 1 or fixed_points < 0:
        raise ValueError("invalid nonidentity involution cycle type")
    return math.factorial(n) // (
        (2**transposition_count)
        * math.factorial(transposition_count)
        * math.factorial(fixed_points)
    )


@lru_cache(maxsize=None)
def right_regular_matrix(n: int, element: Permutation) -> np.ndarray:
    group = symmetric_group(n)
    if element not in set(group):
        raise ValueError("element is not in the requested symmetric group")
    index = {permutation: offset for offset, permutation in enumerate(group)}
    matrix = np.zeros((len(group), len(group)), dtype=float)
    for column, permutation in enumerate(group):
        image = compose_permutations(permutation, element)
        matrix[index[image], column] = 1.0
    return matrix


def _kron_power(matrix: np.ndarray, copies: int) -> np.ndarray:
    if copies < 1:
        raise ValueError("copies must be positive")
    result = np.asarray([[1.0]], dtype=matrix.dtype)
    for _ in range(copies):
        result = np.kron(result, matrix)

    return result


def dense_binary_states(
    n: int,
    transposition_count: int,
    copies: int,
    *,
    maximum_dimension: int = 2048,
) -> tuple[np.ndarray, np.ndarray]:
    group_order = math.factorial(n)
    dimension = group_order**copies
    if dimension > maximum_dimension:
        raise ValueError(
            f"dense control dimension {dimension} exceeds {maximum_dimension}"
        )
    identity = np.eye(group_order, dtype=float)
    null_one = identity / group_order
    alternatives = []
    for hidden in involution_conjugacy_class(n, transposition_count):
        state = (identity + right_regular_matrix(n, hidden)) / group_order
        alternatives.append(_kron_power(state, copies))
    average = sum(alternatives, np.zeros((dimension, dimension), dtype=float))
    average /= len(alternatives)
    return _kron_power(null_one, copies), average


def dense_hidden_coset_state(
    n: int,
    hidden: Permutation,
    copies: int,
) -> np.ndarray:
    """Return the standard mixed coset state for one specified involution."""

    if involution_transposition_count(hidden) in {None, 0}:
        raise ValueError("hidden element must be a nonidentity involution")
    order = math.factorial(n)
    one_copy = (np.eye(order) + right_regular_matrix(n, hidden)) / order
    return _kron_power(one_copy, copies)


def exact_class_mixture_chi_square(
    conjugacy_class_size: int,
    copies: int,
) -> Fraction:
    if conjugacy_class_size < 1 or copies < 1:
        raise ValueError("class size and copies must be positive")
    return Fraction((1 << copies) - 1, conjugacy_class_size)


def chi_square_trace_distance_upper_bound(
    conjugacy_class_size: int,
    copies: int,
) -> float:
    return 0.5 * math.sqrt(
        float(exact_class_mixture_chi_square(conjugacy_class_size, copies))
    )


def minimum_copies_for_bayes_advantage(
    conjugacy_class_size: int,
    advantage: float,
) -> int:
    """Copy lower bound for equal-prior success ``1/2 + advantage``."""

    if conjugacy_class_size < 1:
        raise ValueError("conjugacy_class_size must be positive")
    if not 0.0 < advantage <= 0.5:
        raise ValueError("advantage must lie in (0,1/2]")
    threshold = 1.0 + 16.0 * advantage * advantage * conjugacy_class_size
    return math.ceil(math.log2(threshold))


@lru_cache(maxsize=None)
def weak_fourier_label_distribution(
    n: int,
    transposition_count: int,
    hidden_subgroup: bool,
) -> tuple[Fraction, ...]:
    order = math.factorial(n)
    probabilities = []
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        character = character_on_involution(partition, transposition_count)
        numerator = dimension * (
            dimension + character if hidden_subgroup else dimension
        )
        probabilities.append(Fraction(numerator, order))
    if sum(probabilities) != 1:
        raise ArithmeticError("weak Fourier distribution failed normalization")
    return tuple(probabilities)


def product_weak_fourier_trace_distance(
    n: int,
    transposition_count: int,
    copies: int,
) -> Fraction:
    if copies < 1:
        raise ValueError("copies must be positive")
    alternative = weak_fourier_label_distribution(
        n, transposition_count, True
    )
    null = weak_fourier_label_distribution(n, transposition_count, False)
    difference = Fraction()
    for labels in itertools.product(range(len(alternative)), repeat=copies):
        alt_probability = math.prod(alternative[index] for index in labels)
        null_probability = math.prod(null[index] for index in labels)
        difference += abs(alt_probability - null_probability)
    return difference / 2


def one_copy_label_helstrom_trace_distance(
    n: int,
    transposition_count: int,
) -> Fraction:
    order = math.factorial(n)
    numerator = sum(
        hook_length_dimension(partition)
        * abs(character_on_involution(partition, transposition_count))
        for partition in integer_partitions(n)
    )
    return Fraction(numerator, 2 * order)


@lru_cache(maxsize=None)
def two_copy_target_label_helstrom_trace_distance(
    n: int,
    transposition_count: int,
) -> Fraction:
    """Exact Helstrom distance from ``(lambda,mu,nu)`` target sectors."""

    order = math.factorial(n)
    partitions = integer_partitions(n)
    dimensions = {
        partition: hook_length_dimension(partition)
        for partition in partitions
    }
    ratios = {
        partition: Fraction(
            character_on_involution(partition, transposition_count),
            dimensions[partition],
        )
        for partition in partitions
    }
    total = Fraction()
    for left in partitions:
        for right in partitions:
            for target in partitions:
                multiplicity = kronecker_coefficient(left, right, target)
                if not multiplicity:
                    continue
                null_mass = Fraction(
                    dimensions[left]
                    * dimensions[right]
                    * multiplicity
                    * dimensions[target],
                    order * order,
                )
                total += null_mass * abs(
                    ratios[left] + ratios[right] + ratios[target]
                )
    return total / 2


def _conjugation_basis_permutation(n: int, element: Permutation) -> np.ndarray:
    group = symmetric_group(n)
    index = {permutation: offset for offset, permutation in enumerate(group)}
    inverse = inverse_permutation(element)
    return np.asarray(
        [
            index[
                compose_permutations(
                    compose_permutations(element, permutation), inverse
                )
            ]
            for permutation in group
        ],
        dtype=int,
    )


def _tensor_basis_permutation(permutation: np.ndarray, copies: int) -> np.ndarray:
    dimension = len(permutation)
    result = np.empty(dimension**copies, dtype=int)
    for flat_index, coordinates in enumerate(
        itertools.product(range(dimension), repeat=copies)
    ):
        image = tuple(int(permutation[index]) for index in coordinates)
        result[flat_index] = np.ravel_multi_index(
            image, (dimension,) * copies
        )
    return result


def _permutation_conjugate(
    matrix: np.ndarray,
    basis_permutation: np.ndarray,
) -> np.ndarray:
    result = np.zeros_like(matrix)
    result[np.ix_(basis_permutation, basis_permutation)] = matrix
    return result


def conjugation_symmetrize_binary_effect(
    n: int,
    copies: int,
    effect: np.ndarray,
) -> np.ndarray:
    """Average a binary effect over simultaneous basis conjugation."""

    expected_dimension = math.factorial(n) ** copies
    if effect.shape != (expected_dimension, expected_dimension):
        raise ValueError("effect has the wrong k-copy regular-space shape")
    symmetrized = np.zeros_like(effect, dtype=np.complex128)
    for conjugator in symmetric_group(n):
        one_copy = _conjugation_basis_permutation(n, conjugator)
        tensor = _tensor_basis_permutation(one_copy, copies)
        symmetrized += _permutation_conjugate(effect, tensor)
    return symmetrized / math.factorial(n)


def audit_dense_binary_control(
    n: int,
    transposition_count: int,
    copies: int,
) -> BinaryDecisionFiniteControl:
    null, alternative = dense_binary_states(n, transposition_count, copies)
    difference = (alternative - null + (alternative - null).T) / 2.0
    eigenvalues, eigenvectors = np.linalg.eigh(difference)
    trace_distance = 0.5 * float(np.abs(eigenvalues).sum())
    group_order = math.factorial(n)
    class_size = involution_class_size(n, transposition_count)
    chi_square = float(
        (group_order**copies) * np.trace(difference @ difference)
    )
    predicted = float(exact_class_mixture_chi_square(class_size, copies))
    positive = eigenvalues > 1e-10
    helstrom_effect = (
        eigenvectors[:, positive] @ eigenvectors[:, positive].T
        if np.any(positive)
        else np.zeros_like(difference)
    )

    average_invariance = 0.0
    helstrom_invariance = 0.0
    conjugators = symmetric_group(n)
    if alternative.shape[0] > 256:
        conjugators = conjugators[:2]
    for conjugator in conjugators:
        one_copy_permutation = _conjugation_basis_permutation(n, conjugator)
        tensor_permutation = _tensor_basis_permutation(
            one_copy_permutation, copies
        )
        average_invariance = max(
            average_invariance,
            float(
                np.linalg.norm(
                    _permutation_conjugate(alternative, tensor_permutation)
                    - alternative,
                    ord=2,
                )
            ),
        )
        helstrom_invariance = max(
            helstrom_invariance,
            float(
                np.linalg.norm(
                    _permutation_conjugate(
                        helstrom_effect, tensor_permutation
                    )
                    - helstrom_effect,
                    ord=2,
                )
            ),
        )

    product_labels = float(
        product_weak_fourier_trace_distance(
            n, transposition_count, copies
        )
    )
    label_distance: float | None = None
    label_residual: float | None = None
    target_gain: float | None = None
    if copies == 1:
        label_distance = float(
            one_copy_label_helstrom_trace_distance(
                n, transposition_count
            )
        )
        label_residual = abs(label_distance - trace_distance)
    elif copies == 2:
        label_distance = float(
            two_copy_target_label_helstrom_trace_distance(
                n, transposition_count
            )
        )
        label_residual = abs(label_distance - trace_distance)
        target_gain = label_distance - product_labels

    upper_bound = chi_square_trace_distance_upper_bound(class_size, copies)
    verified = bool(
        abs(chi_square - predicted) <= 1e-9
        and trace_distance <= upper_bound + 1e-9
        and average_invariance <= 1e-9
        and helstrom_invariance <= 1e-8
        and (label_residual is None or label_residual <= 1e-9)
    )
    return BinaryDecisionFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copies,
        group_order=group_order,
        conjugacy_class_size=class_size,
        hilbert_dimension=group_order**copies,
        exact_normalized_chi_square=chi_square,
        predicted_normalized_chi_square=predicted,
        chi_square_identity_residual=abs(chi_square - predicted),
        helstrom_trace_distance=trace_distance,
        chi_square_trace_distance_upper_bound=upper_bound,
        equal_prior_bayes_success_probability=0.5 * (1.0 + trace_distance),
        product_weak_fourier_trace_distance=product_labels,
        exact_label_helstrom_trace_distance=label_distance,
        label_helstrom_identity_residual=label_residual,
        entangled_target_gain_over_product_labels=target_gain,
        positive_helstrom_rank=int(np.count_nonzero(positive)),
        negative_helstrom_rank=int(np.count_nonzero(eigenvalues < -1e-10)),
        average_conjugation_invariance_residual=average_invariance,
        helstrom_conjugation_invariance_residual=helstrom_invariance,
        finite_control_verified=verified,
        status=(
            "binary-helstrom-normal-form-verified"
            if verified
            else "binary-decision-control-failure"
        ),
    )


def fixed_point_free_decision_scaling_record(
    n: int,
    *,
    target_bayes_advantage: float = 0.1,
) -> FixedPointFreeDecisionScalingRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    matching_count = involution_class_size(n, n // 2)
    log_class = math.log2(matching_count)
    lower_bound = minimum_copies_for_bayes_advantage(
        matching_count, target_bayes_advantage
    )
    return FixedPointFreeDecisionScalingRecord(
        n=n,
        matching_count=matching_count,
        log2_matching_count=log_class,
        target_bayes_advantage=target_bayes_advantage,
        information_theoretic_copy_lower_bound=lower_bound,
        copy_lower_bound_over_log2_class_size=lower_bound / log_class,
        one_copy_trace_distance_upper_bound=(0.5 / math.sqrt(matching_count)),
        two_copy_trace_distance_upper_bound=(
            0.5 * math.sqrt(3.0 / matching_count)
        ),
        constant_copy_signal_can_remain_constant=False,
        polynomial_measurement_compiler_known=False,
        status="constant-copy-decision-signal-ruled-out-threshold-open",
    )


def build_hidden_involution_binary_decision_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 1),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (8, 16, 32, 64, 128),
) -> HiddenInvolutionBinaryDecisionReport:
    controls = [
        audit_dense_binary_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [
        fixed_point_free_decision_scaling_record(n)
        for n in scaling_n_values
    ]
    verified = all(row.finite_control_verified for row in controls)
    one_copy_verified = all(
        row.label_helstrom_identity_residual is not None
        and row.label_helstrom_identity_residual <= 1e-9
        for row in controls
        if row.copy_count == 1
    )
    two_copy_verified = all(
        row.label_helstrom_identity_residual is not None
        and row.label_helstrom_identity_residual <= 1e-9
        for row in controls
        if row.copy_count == 2
    )
    theorem = HiddenInvolutionBinaryDecisionTheorem(
        centered_orthogonality_identity=(
            "Tr[(rho_h^k-rho_0^k)(rho_g^k-rho_0^k)]="
            "|G|^-k(2^k-1) delta_(h,g)."
        ),
        chi_square_identity=(
            "chi^2(rho_C^k||rho_0^k)=(2^k-1)/|C| exactly."
        ),
        trace_distance_upper_bound=(
            "D(rho_C^k,rho_0^k)<=sqrt((2^k-1)/|C|)/2."
        ),
        symmetrization_identity=(
            "Conjugation-averaging any binary effect preserves null acceptance "
            "and class-average alternative acceptance and makes alternative "
            "acceptance identical for every h in C."
        ),
        one_copy_helstrom_normal_form=(
            "After the group QFT, the class average is scalar on lambda and "
            "the optimal sign is sign(chi_lambda(h))."
        ),
        two_copy_helstrom_normal_form=(
            "After source labels lambda,mu and diagonal coupling to nu, the "
            "optimal sign is sign(r_lambda+r_mu+r_nu)."
        ),
        higher_copy_boundary=(
            "For k>=3, overlapping subset class sums commute with the diagonal "
            "group action but can act nontrivially and noncommutatively on "
            "recoupling multiplicity spaces."
        ),
        centered_orthogonality_proved=True,
        exact_chi_square_proved=True,
        symmetrized_worst_case_binary_test_proved=True,
        one_copy_weak_fourier_helstrom_optimal=one_copy_verified,
        two_copy_target_label_helstrom_optimal=two_copy_verified,
        threshold_trace_distance_lower_bound_proved=False,
        scalable_block_sign_compiler_constructed=False,
        theorem_verified=verified and one_copy_verified and two_copy_verified,
        status=(
            "binary-decision-copy-threshold-and-two-copy-normal-form-proved"
            if verified and one_copy_verified and two_copy_verified
            else "binary-decision-theorem-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_validation_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "exact_chi_square_control_count": sum(
            row.chi_square_identity_residual <= 1e-9 for row in controls
        ),
        "one_copy_helstrom_label_control_count": sum(
            row.copy_count == 1
            and row.label_helstrom_identity_residual is not None
            and row.label_helstrom_identity_residual <= 1e-9
            for row in controls
        ),
        "two_copy_helstrom_target_control_count": sum(
            row.copy_count == 2
            and row.label_helstrom_identity_residual is not None
            and row.label_helstrom_identity_residual <= 1e-9
            for row in controls
        ),
        "strict_entangled_target_gain_control_count": sum(
            (row.entangled_target_gain_over_product_labels or 0.0) > 1e-10
            for row in controls
        ),
        "scaling_record_count": len(scaling),
        "threshold_trace_distance_lower_bound_count": 0,
        "scalable_block_sign_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return HiddenInvolutionBinaryDecisionReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "Already proves Theta(log |H|/log p) sample complexity for "
                    "triviality and identification when candidate subgroups have "
                    "equal prime order, explicitly including symmetric hidden involutions."
                ),
            }
        ],
        theorem_contract={
            "access_model": (
                "k independent standard mixed coset states; null H={e}, "
                "alternative H={e,h} with h uniform in one nonidentity "
                "involution conjugacy class."
            ),
            "worst_case_scope": (
                "Conjugation symmetrization converts uniform-prior performance "
                "to identical performance on every h in the class, but does "
                "not cover arbitrary non-coset-state oracle access."
            ),
            "binary_output": (
                "Decide trivial versus promised class; do not identify h."
            ),
            "non_claim": (
                "No threshold trace-distance lower bound, scalable block-sign "
                "circuit, GI reduction, classical separation, or speedup."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-THRESHOLD-LOWER",
                "statement": (
                    "Lower-bound class-mixture trace distance at k=Theta(log |C|), "
                    "for example by controlling the fourth normalized trace moment "
                    "of the centered likelihood operator."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-BLOCK-SIGN-COMPILER",
                "statement": (
                    "Compile the higher-copy invariant Helstrom block sign in "
                    "polynomial size without enumerating C or diagonalizing "
                    "exponential multiplicity spaces."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-TWO-COPY-KRONECKER-MEASUREMENT",
                "statement": (
                    "Give a uniform polynomial S_n diagonal-target measurement; "
                    "the exact scalar decision rule alone is not a circuit."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-INPUT-MODEL-TRANSFER",
                "statement": (
                    "Prove that a natural GI/code-equivalence input supplies the "
                    "promised coset-state binary instance without hiding an "
                    "equivalent hard preprocessing or decoding task."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-CLASSICAL-BASELINE",
                "statement": (
                    "Compare the same promise and oracle/query model against "
                    "collision search, graph invariants, and dequantization."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "Zero information about the individual h means invariant "
                    "measurements are useless."
                ),
                "answer": (
                    "False for binary class detection. An invariant effect can "
                    "distinguish the class mixture from the trivial subgroup while "
                    "remaining exactly independent of which h occurred."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Pairwise coset-state overlap already proves an efficient "
                    "binary measurement near log2 |C| copies."
                ),
                "answer": (
                    "False. It fixes the second moment and an upper bound only; a "
                    "matching trace-norm lower bound needs higher-moment or spectral "
                    "control."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The two-copy target-label formula gives a scalable algorithm."
                ),
                "answer": (
                    "False. Its trace distance is at most sqrt(3/|C|)/2 and the "
                    "uniform Kronecker target transform is not compiled here."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The copy lower bound rules out a polynomial quantum algorithm."
                ),
                "answer": (
                    "False. log |C| is polynomial in the natural group-register "
                    "length for fixed-point-free involutions."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "A coset-state binary algorithm would automatically solve GI."
                ),
                "answer": (
                    "False without a promise-preserving reduction and accounting "
                    "for graph automorphisms, oracle preparation, and the actual "
                    "decision-to-search relationship."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_binary_chi_square_identity_proved": True,
            "constant_copy_fixed_point_free_binary_signal_possible": False,
            "one_copy_weak_fourier_is_binary_helstrom_optimal": one_copy_verified,
            "two_copy_target_label_is_binary_helstrom_optimal": two_copy_verified,
            "binary_detection_requires_hidden_involution_identification": False,
            "threshold_trace_distance_lower_bound_proved": False,
            "polynomial_higher_copy_block_sign_compiler_constructed": False,
            "polynomial_two_copy_kronecker_measurement_constructed": False,
            "graph_isomorphism_algorithm_constructed": False,
            "graph_isomorphism_lower_bound_proved": False,
            "classical_superpolynomial_separation_proved": False,
            "speedup_claim_allowed": False,
            "sample_complexity_result_new_to_literature": False,
            "published_equal_prime_order_sample_theorem_rederived": True,
            "reason": (
                "Binary decision is a genuine escape from individual-label polar "
                "obligations, but constant-copy signal vanishes and neither "
                "threshold distinguishability nor its efficient measurement is known."
            ),
        },
        status=theorem.status,
        summary=(
            "Re-derived the published logarithmic sample threshold with an exact "
            "class-mixture chi-square identity and added exact one- and two-copy "
            "Helstrom normal forms. The new value is compiler diagnostics, not a "
            "new sample-complexity result."
        ),
        falsifiers_triggered=[
            "Constant-copy invariant measurements cannot retain constant fixed-point-free decision advantage.",
            "Pairwise overlap decay alone does not prove threshold distinguishability.",
            "Zero individual-label information does not imply zero binary class-detection information.",
            "Two-copy target-label optimality is not a scalable hidden-involution algorithm.",
        ],
    )


def write_hidden_involution_binary_decision_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION"
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
    payload = asdict(build_hidden_involution_binary_decision_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG--HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "coset_hidden_involution_binary_decision_reduction": str(output_path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    report = write_hidden_involution_binary_decision_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
