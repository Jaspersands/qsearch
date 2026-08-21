"""Pairwise succinctness and the true trimmed row-polar boundary.

The asymptotically full free source fiber has already been canonically reduced
to regular ``G=S_(2m)`` copies:

    Ind_K^G(C[K] tensor C[O]) ~= C[G] tensor C[O].

Consequently a generic ``S_(2m) down K_m`` subduction transform is not the
remaining operation on that mass.  After the ``G`` QFT, the unresolved blocks
are the orbit-copy Fourier kernels

    R_lambda(o,o') = sum_(g in G) kappa_(o,o')(g) rho_lambda(g),
    kappa_(o,o')(g) = <v_o|U_g|v_o'>.

For product plus-coset representatives ``o=(x_i H)`` and ``o'=(y_i H)``,

    kappa_(o,o')(g)
      = product_i |{x_i,x_i h} intersect
                     g {y_i,y_i h} g^-1| / 2.          (1)

Suppose two coordinates of ``o'`` are robustly transitive: each of the four
oriented pairs ``(y_i h^a,y_j h^b)`` generates a transitive action.  Every
nonzero term in (1) then chooses one endpoint equality in each seed
coordinate.  There are 16 orientation choices.  For each choice a conjugator
between the two ordered transitive permutation pairs is determined by the
image of one root, hence there are at most ``n``.  Therefore

    |support(kappa_(o,o'))| <= 16 n.                   (2)

The conjugators are reconstructed by rooted propagation in polynomial time;
the remaining coordinates only filter the list.  Thus every pairwise kernel
and every matrix-valued Fourier entry is a sum of at most ``16n`` efficiently
computable Young representation matrices.  Pairwise entry estimation is not
the quantum bottleneck and should be treated as classically dequantized.

This does not compile the exponentially wide operator on the orbit-copy
register.  Coherent row preparation, global singular-vector structure,
physical label erasure, and removal of the ``1/M`` likelihood normalization
remain open.  A dense matrix can have polynomial-time entry access and still
lack a polynomial polar transform.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    symmetric_group,
)
from coset_hyperoctahedral_free_orbit_canonicalization_boundary import (
    canonical_plus_cosets,
)
from coset_hyperoctahedral_trimmed_orbit_canonicalizer import (
    canonicalizer_scaling_record,
    transitivity_failure_upper_bound,
)
from coset_hyperoctahedral_source_plancherel_typicality import (
    nonidentity_character_bound,
)
from coset_hyperoctahedral_trivial_color_mass_no_go import (
    canonical_matching_involution,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_trimmed_row_kernel_succinctness.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-TRIMMED-ROW-KERNEL-SUCCINCTNESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RootedConjugatorControl:
    half_degree: int
    degree: int
    control_pair_count: int
    robust_right_seed_count: int
    maximum_bruteforce_support_size: int
    maximum_polynomial_support_size: int
    theorem_support_upper_bound: int
    maximum_support_set_mismatch_count: int
    maximum_rooted_conjugator_count_per_orientation: int
    maximum_fourier_matrix_residual: float
    factorial_group_enumeration_needed_for_pairwise_kernel: bool
    rooted_pairwise_kernel_reconstruction_verified: bool
    status: str


@dataclass(frozen=True)
class RobustSeedScalingRecord:
    half_degree: int
    degree: int
    copy_count: int
    disjoint_seed_pair_count: int
    one_orientation_intransitivity_upper_bound: float
    one_pair_not_robust_upper_bound: float
    all_pairs_not_robust_upper_bound: float
    all_pairs_not_robust_log2_upper_bound: float
    nonfree_source_fraction_upper_bound: float
    nonfree_source_fraction_log2_upper_bound: float
    total_robust_trim_failure_upper_bound: float
    total_robust_trim_failure_log2_upper_bound: float
    robust_trim_alternative_failure_upper_bound: float
    robust_trim_alternative_failure_log2_upper_bound: float
    robust_trim_alternative_success_lower_bound: float
    pairwise_conjugator_support_upper_bound: int
    pairwise_kernel_classically_polynomial: bool
    global_orbit_row_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class TrimmedRowKernelTheorem:
    architecture_correction: str
    product_overlap: str
    rooted_conjugator_bound: str
    natural_robust_mass: str
    pairwise_fourier_kernel: str
    dequantization_consequence: str
    remaining_global_operator: str
    regular_G_reduction_supersedes_generic_K_subduction_on_trimmed_mass: bool
    exact_product_overlap_formula_proved: bool
    polynomial_pairwise_conjugator_reconstruction_proved: bool
    asymptotically_full_robust_trimmed_mass_proved: bool
    pairwise_fourier_kernel_succinct: bool
    global_orbit_copy_transform_compiled: bool
    unnormalized_likelihood_fast_forward_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class TrimmedRowKernelReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[RootedConjugatorControl]
    scaling_records: list[RobustSeedScalingRecord]
    theorem: TrimmedRowKernelTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _conjugate(
    conjugator: Permutation,
    value: Permutation,
) -> Permutation:
    return compose_permutations(
        compose_permutations(conjugator, value),
        inverse_permutation(conjugator),
    )


def _oriented(
    representative: Permutation,
    hidden: Permutation,
    orientation: int,
) -> Permutation:
    return (
        compose_permutations(representative, hidden)
        if orientation
        else representative
    )


def generated_action_is_transitive(
    generators: tuple[Permutation, ...],
) -> bool:
    if not generators:
        raise ValueError("at least one generator is required")
    degree = len(generators[0])
    if any(len(item) != degree for item in generators):
        raise ValueError("generator degrees differ")
    moves = (*generators, *(inverse_permutation(item) for item in generators))
    reached = {0}
    frontier = [0]
    for vertex in frontier:
        for generator in moves:
            image = generator[vertex]
            if image not in reached:
                reached.add(image)
                frontier.append(image)
    return len(reached) == degree


def robust_transitive_seed(
    source_tuple: tuple[Permutation, ...],
    hidden: Permutation,
    seed_coordinates: tuple[int, int] = (0, 1),
) -> bool:
    left, right = seed_coordinates
    if left == right or min(seed_coordinates) < 0 or max(seed_coordinates) >= len(source_tuple):
        raise ValueError("invalid seed coordinates")
    return all(
        generated_action_is_transitive(
            (
                _oriented(source_tuple[left], hidden, first_orientation),
                _oriented(source_tuple[right], hidden, second_orientation),
            )
        )
        for first_orientation, second_orientation in itertools.product(
            (0, 1), repeat=2
        )
    )


def plus_coset_overlap(
    left: Permutation,
    right: Permutation,
    conjugator: Permutation,
    hidden: Permutation,
) -> float:
    left_endpoints = {
        left,
        compose_permutations(left, hidden),
    }
    right_endpoints = {
        _conjugate(conjugator, right),
        _conjugate(
            conjugator,
            compose_permutations(right, hidden),
        ),
    }
    return len(left_endpoints.intersection(right_endpoints)) / 2.0


def product_plus_overlap(
    left_tuple: tuple[Permutation, ...],
    right_tuple: tuple[Permutation, ...],
    conjugator: Permutation,
    hidden: Permutation,
) -> float:
    if len(left_tuple) != len(right_tuple) or not left_tuple:
        raise ValueError("source tuples must have equal positive length")
    value = 1.0
    for left, right in zip(left_tuple, right_tuple):
        value *= plus_coset_overlap(left, right, conjugator, hidden)
        if value == 0.0:
            break
    return value


def rooted_ordered_pair_conjugators(
    source_pair: tuple[Permutation, Permutation],
    target_pair: tuple[Permutation, Permutation],
) -> tuple[Permutation, ...]:
    """Construct every conjugator from root images for a transitive source."""

    degree = len(source_pair[0])
    if any(len(item) != degree for item in (*source_pair, *target_pair)):
        raise ValueError("permutation degrees differ")
    if not generated_action_is_transitive(source_pair):
        raise ValueError("source pair must generate a transitive action")
    source_moves = (
        *source_pair,
        *(inverse_permutation(item) for item in source_pair),
    )
    target_moves = (
        *target_pair,
        *(inverse_permutation(item) for item in target_pair),
    )
    output: set[Permutation] = set()
    for root_image in range(degree):
        mapping = [-1] * degree
        mapping[0] = root_image
        frontier = [0]
        consistent = True
        for vertex in frontier:
            for source, target in zip(source_moves, target_moves):
                source_image = source[vertex]
                required = target[mapping[vertex]]
                if mapping[source_image] < 0:
                    mapping[source_image] = required
                    frontier.append(source_image)
                elif mapping[source_image] != required:
                    consistent = False
                    break
            if not consistent:
                break
        if (
            consistent
            and len(frontier) == degree
            and len(set(mapping)) == degree
        ):
            candidate = tuple(mapping)
            if all(
                _conjugate(candidate, source) == target
                for source, target in zip(source_pair, target_pair)
            ):
                output.add(candidate)
    return tuple(sorted(output))


def polynomial_pairwise_kernel_support(
    left_tuple: tuple[Permutation, ...],
    right_tuple: tuple[Permutation, ...],
    hidden: Permutation,
    seed_coordinates: tuple[int, int] = (0, 1),
) -> tuple[Permutation, ...]:
    if len(left_tuple) != len(right_tuple) or len(left_tuple) < 2:
        raise ValueError("equal source tuples with at least two coordinates required")
    if not robust_transitive_seed(right_tuple, hidden, seed_coordinates):
        raise ValueError("right tuple lacks a robust transitive seed")
    first, second = seed_coordinates
    candidates: set[Permutation] = set()
    for orientations in itertools.product((0, 1), repeat=4):
        left_first, right_first, left_second, right_second = orientations
        source_pair = (
            _oriented(right_tuple[first], hidden, right_first),
            _oriented(right_tuple[second], hidden, right_second),
        )
        target_pair = (
            _oriented(left_tuple[first], hidden, left_first),
            _oriented(left_tuple[second], hidden, left_second),
        )
        candidates.update(
            rooted_ordered_pair_conjugators(source_pair, target_pair)
        )
    return tuple(
        candidate
        for candidate in sorted(candidates)
        if product_plus_overlap(
            left_tuple,
            right_tuple,
            candidate,
            hidden,
        )
        > 0.0
    )


def brute_force_pairwise_kernel_support(
    left_tuple: tuple[Permutation, ...],
    right_tuple: tuple[Permutation, ...],
    hidden: Permutation,
) -> tuple[Permutation, ...]:
    return tuple(
        conjugator
        for conjugator in symmetric_group(len(hidden))
        if product_plus_overlap(
            left_tuple,
            right_tuple,
            conjugator,
            hidden,
        )
        > 0.0
    )


def _standard_representation_basis(degree: int) -> np.ndarray:
    spanning = np.column_stack(
        [
            np.eye(degree)[:, index] - np.eye(degree)[:, degree - 1]
            for index in range(degree - 1)
        ]
    )
    basis, _ = np.linalg.qr(spanning)
    return basis


def _standard_representation_matrix(
    permutation: Permutation,
    basis: np.ndarray,
) -> np.ndarray:
    permutation_matrix = np.zeros((len(permutation), len(permutation)))
    for source, target in enumerate(permutation):
        permutation_matrix[target, source] = 1.0
    return basis.T @ permutation_matrix @ basis


def audit_rooted_pairwise_kernel(
    half_degree: int,
    *,
    control_pair_count: int = 8,
    seed: int = 20260821,
) -> RootedConjugatorControl:
    if half_degree not in (2, 3):
        raise ValueError("dense controls are restricted to half_degree 2 or 3")
    degree = 2 * half_degree
    hidden = canonical_matching_involution(half_degree)
    cosets = canonical_plus_cosets(half_degree)
    generator = random.Random(seed + half_degree)
    robust_right: list[tuple[Permutation, Permutation]] = []
    attempts = 0
    while len(robust_right) < control_pair_count and attempts < 10000:
        attempts += 1
        candidate = (generator.choice(cosets), generator.choice(cosets))
        if robust_transitive_seed(candidate, hidden):
            robust_right.append(candidate)
    if len(robust_right) < control_pair_count:
        raise ArithmeticError("failed to sample enough robust source pairs")

    standard_basis = _standard_representation_basis(degree)
    maximum_brute = 0
    maximum_poly = 0
    maximum_mismatch = 0
    maximum_orientation_count = 0
    maximum_fourier_residual = 0.0
    group = symmetric_group(degree)
    for control_index, right_tuple in enumerate(robust_right):
        planted_conjugator = group[
            (1 + 17 * control_index) % len(group)
        ]
        left_tuple = tuple(
            _conjugate(planted_conjugator, item) for item in right_tuple
        )
        polynomial = polynomial_pairwise_kernel_support(
            left_tuple,
            right_tuple,
            hidden,
        )
        brute = brute_force_pairwise_kernel_support(
            left_tuple,
            right_tuple,
            hidden,
        )
        maximum_brute = max(maximum_brute, len(brute))
        maximum_poly = max(maximum_poly, len(polynomial))
        maximum_mismatch = max(
            maximum_mismatch,
            len(set(polynomial).symmetric_difference(brute)),
        )
        for orientations in itertools.product((0, 1), repeat=4):
            source_pair = (
                _oriented(right_tuple[0], hidden, orientations[1]),
                _oriented(right_tuple[1], hidden, orientations[3]),
            )
            target_pair = (
                _oriented(left_tuple[0], hidden, orientations[0]),
                _oriented(left_tuple[1], hidden, orientations[2]),
            )
            maximum_orientation_count = max(
                maximum_orientation_count,
                len(rooted_ordered_pair_conjugators(source_pair, target_pair)),
            )
        full_fourier = sum(
            (
                product_plus_overlap(
                    left_tuple,
                    right_tuple,
                    item,
                    hidden,
                )
                * _standard_representation_matrix(item, standard_basis)
                for item in symmetric_group(degree)
            ),
            np.zeros((degree - 1, degree - 1)),
        )
        sparse_fourier = sum(
            (
                product_plus_overlap(
                    left_tuple,
                    right_tuple,
                    item,
                    hidden,
                )
                * _standard_representation_matrix(item, standard_basis)
                for item in polynomial
            ),
            np.zeros((degree - 1, degree - 1)),
        )
        maximum_fourier_residual = max(
            maximum_fourier_residual,
            float(np.linalg.norm(full_fourier - sparse_fourier, ord=2)),
        )
    bound = 16 * degree
    verified = bool(
        maximum_mismatch == 0
        and maximum_brute > 0
        and maximum_brute <= bound
        and maximum_poly <= bound
        and maximum_orientation_count <= degree
        and maximum_fourier_residual < 1e-10
    )
    return RootedConjugatorControl(
        half_degree=half_degree,
        degree=degree,
        control_pair_count=control_pair_count,
        robust_right_seed_count=len(robust_right),
        maximum_bruteforce_support_size=maximum_brute,
        maximum_polynomial_support_size=maximum_poly,
        theorem_support_upper_bound=bound,
        maximum_support_set_mismatch_count=maximum_mismatch,
        maximum_rooted_conjugator_count_per_orientation=maximum_orientation_count,
        maximum_fourier_matrix_residual=maximum_fourier_residual,
        factorial_group_enumeration_needed_for_pairwise_kernel=False,
        rooted_pairwise_kernel_reconstruction_verified=verified,
        status=(
            "rooted-pairwise-row-kernel-reconstruction-verified"
            if verified
            else "rooted-pairwise-row-kernel-control-failure"
        ),
    )


def robust_seed_scaling_record(
    half_degree: int,
) -> RobustSeedScalingRecord:
    if half_degree < 5:
        raise ValueError("robust asymptotic scaling starts at half_degree five")
    canonicalizer = canonicalizer_scaling_record(half_degree)
    degree = 2 * half_degree
    one_orientation = transitivity_failure_upper_bound(degree)
    one_pair_failure = min(1.0, 4.0 * one_orientation)
    all_pairs_log2 = (
        canonicalizer.disjoint_seed_pair_count * math.log2(one_pair_failure)
    )
    all_pairs_failure = (
        math.exp2(all_pairs_log2) if all_pairs_log2 > -1074.0 else 0.0
    )
    centralizer_order = (2**half_degree) * math.factorial(half_degree)
    nonfree_log2 = math.log2(centralizer_order - 1) + (
        canonicalizer.copy_count
        * math.log2(nonidentity_character_bound(half_degree))
    )
    nonfree = math.exp2(nonfree_log2) if nonfree_log2 > -1074.0 else 0.0
    larger_log2 = max(all_pairs_log2, nonfree_log2)
    total_log2 = min(
        0.0,
        larger_log2
        + math.log2(
            math.exp2(all_pairs_log2 - larger_log2)
            + math.exp2(nonfree_log2 - larger_log2)
        ),
    )
    total_failure = math.exp2(total_log2) if total_log2 > -1074.0 else 0.0
    matchings = int(canonicalizer.perfect_matching_count_decimal)
    eta = (matchings - 1) / (2**canonicalizer.copy_count)
    alternative_log2 = min(
        0.0,
        0.5 * (math.log2(1.0 + eta) + total_log2),
    )
    alternative_failure = (
        math.exp2(alternative_log2) if alternative_log2 > -1074.0 else 0.0
    )
    return RobustSeedScalingRecord(
        half_degree=half_degree,
        degree=degree,
        copy_count=canonicalizer.copy_count,
        disjoint_seed_pair_count=canonicalizer.disjoint_seed_pair_count,
        one_orientation_intransitivity_upper_bound=one_orientation,
        one_pair_not_robust_upper_bound=one_pair_failure,
        all_pairs_not_robust_upper_bound=all_pairs_failure,
        all_pairs_not_robust_log2_upper_bound=all_pairs_log2,
        nonfree_source_fraction_upper_bound=nonfree,
        nonfree_source_fraction_log2_upper_bound=nonfree_log2,
        total_robust_trim_failure_upper_bound=total_failure,
        total_robust_trim_failure_log2_upper_bound=total_log2,
        robust_trim_alternative_failure_upper_bound=alternative_failure,
        robust_trim_alternative_failure_log2_upper_bound=alternative_log2,
        robust_trim_alternative_success_lower_bound=1.0 - alternative_failure,
        pairwise_conjugator_support_upper_bound=16 * degree,
        pairwise_kernel_classically_polynomial=True,
        global_orbit_row_polar_compiled=False,
        status="robust-trimmed-pairwise-kernel-succinct-global-polar-open",
    )


def build_trimmed_row_kernel_report() -> TrimmedRowKernelReport:
    controls = [
        audit_rooted_pairwise_kernel(2, control_pair_count=6),
        audit_rooted_pairwise_kernel(3, control_pair_count=8),
    ]
    scaling = [
        robust_seed_scaling_record(value)
        for value in (5, 8, 16, 32, 64, 128)
    ]
    exact = all(
        row.rooted_pairwise_kernel_reconstruction_verified for row in controls
    )
    natural = all(
        row.pairwise_kernel_classically_polynomial
        and not row.global_orbit_row_polar_compiled
        for row in scaling
    ) and scaling[-1].robust_trim_alternative_failure_upper_bound < 1e-40
    theorem = TrimmedRowKernelTheorem(
        architecture_correction=(
            "The free-fiber canonicalizer and Ind_K^G(C[K] tensor C[O])="
            "C[G] tensor C[O] remove generic K-subduction from the active "
            "trimmed architecture; only orbit-copy row polar remains."
        ),
        product_overlap=(
            "kappa_(o,o')(g) is exactly the product of endpoint-set "
            "intersection sizes divided by two."
        ),
        rooted_conjugator_bound=(
            "A robust two-coordinate seed gives 16 endpoint orientations; "
            "each ordered transitive pair has at most n conjugators, reconstructed "
            "from the image of one root."
        ),
        natural_robust_mass=(
            "One seed-pair failure is at most four times the transitivity union "
            "bound; disjoint coordinate pairs amplify, and the source second "
            "moment transfers the trim to alternative contribution."
        ),
        pairwise_fourier_kernel=(
            "Every R_lambda(o,o') is a sum of at most 16n efficiently "
            "computable representation matrices."
        ),
        dequantization_consequence=(
            "Pairwise scalar or matrix kernel evaluation is classically "
            "polynomial and cannot itself be claimed as quantum leverage."
        ),
        remaining_global_operator=(
            "Compile the coherent exponentially wide orbit-copy polar and label "
            "erasure while factoring out the M likelihood scale analytically."
        ),
        regular_G_reduction_supersedes_generic_K_subduction_on_trimmed_mass=True,
        exact_product_overlap_formula_proved=True,
        polynomial_pairwise_conjugator_reconstruction_proved=exact,
        asymptotically_full_robust_trimmed_mass_proved=natural,
        pairwise_fourier_kernel_succinct=exact and natural,
        global_orbit_copy_transform_compiled=False,
        unnormalized_likelihood_fast_forward_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and natural,
        status=(
            "regular-row-pairwise-kernel-succinct-global-polar-open"
            if exact and natural
            else "trimmed-row-kernel-succinctness-control-failure"
        ),
    )
    return TrimmedRowKernelReport(
        created_at=utc_now(),
        theorem_contract={
            "source_mass": (
                "Free canonical source tuples with at least one robustly "
                "transitive disjoint coordinate pair"
            ),
            "kernel": "<v_o|U_g|v_o'> after regular-G induction",
            "finite_control": "Exact S_4 and S_6 enumeration",
            "claim_boundary": (
                "Pairwise kernel succinctness and architecture correction, not "
                "a coherent global transform or hidden-involution detector."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-ORBIT-ROW-COHERENT-INDEX",
                "statement": (
                    "Construct a reversible index and row-state preparation for "
                    "canonical orbit copies without factorial enumeration or QRAM."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-ORBIT-ROW-GLOBAL-POLAR",
                "statement": (
                    "Exploit structure beyond pairwise entry access to compile the "
                    "global R_lambda polar on constant alternative mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-ORBIT-ROW-M-SCALE",
                "statement": (
                    "Factor the candidate count M analytically; black-box use of "
                    "A=Z/M remains subject to the square-root-M lower bound."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-ORBIT-ROW-CLASSICAL-BASELINE",
                "statement": (
                    "Compare any global spectral statistic with classical kernel "
                    "methods using the polynomial pairwise evaluator proved here."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Natural hyperoctahedral multiplicities still force a K-subduction compiler.",
                "answer": (
                    "Not on the canonical free mass: regular K induction fuses "
                    "exactly into a regular G coordinate before the G QFT."
                ),
                "resolved": True,
            },
            {
                "challenge": "The orbit-row Fourier entries require summing over n! conjugators.",
                "answer": (
                    "False on robust mass: endpoint orientations and rooted "
                    "transitive propagation leave at most 16n terms."
                ),
                "resolved": True,
            },
            {
                "challenge": "Polynomial entry access gives an efficient polar transform.",
                "answer": (
                    "False: the orbit-copy matrix is exponentially wide, and no "
                    "coherent row transform, conditioning theorem, or normalization "
                    "bypass follows from entry access."
                ),
                "resolved": True,
            },
            {
                "challenge": "The theorem removes the candidate normalization.",
                "answer": (
                    "False: it removes factorial pairwise summation, while the "
                    "global A=Z/M fast-forward remains exactly open."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "arXiv:2302.11454",
                "role": (
                    "Generalized phase estimation efficiently measures symmetric-group "
                    "Kronecker projectors, but does not provide the present relative polar."
                ),
            },
            {
                "id": "arXiv:quant-ph/0304064",
                "role": (
                    "Bratteli-path QFT framework; motivates separating regular carrier "
                    "Fourier structure from unresolved orbit-copy multiplicity."
                ),
            },
        ],
        headline_metrics={
            "exact_rooted_kernel_control_count": len(controls),
            "maximum_finite_pairwise_support": max(
                row.maximum_polynomial_support_size for row in controls
            ),
            "maximum_theorem_pairwise_support": max(
                row.theorem_support_upper_bound for row in controls
            ),
            "tail_robust_alternative_success_lower_bound": (
                scaling[-1].robust_trim_alternative_success_lower_bound
            ),
            "generic_K_subduction_required_on_trimmed_mass_count": 0,
            "pairwise_kernel_classical_evaluator_count": int(exact and natural),
            "global_orbit_row_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "regular_G_architecture_is_active_on_trimmed_mass": True,
            "generic_K_subduction_required_on_trimmed_mass": False,
            "pairwise_row_kernel_has_at_most_16n_terms": exact,
            "pairwise_row_kernel_classically_polynomial": exact and natural,
            "pairwise_kernel_evaluation_is_quantum_advantage": False,
            "global_orbit_copy_polar_compiled": False,
            "unnormalized_Z_scale_fast_forward_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct residual matrix has succinct pairwise entries, but "
                "its coherent global orbit-copy transform and M-scale normalization "
                "remain unresolved."
            ),
        },
        status=theorem.status,
        summary=(
            "Redirected the trimmed hidden-involution architecture from generic "
            "hyperoctahedral subduction to the regular-G orbit-row polar and proved "
            "that every pairwise Fourier kernel has a polynomial rooted-conjugator description."
        ),
        falsifiers_triggered=[
            "Generic S_(2m)-to-K_m subduction is not the active high-mass bottleneck after free-fiber canonicalization.",
            "Factorial enumeration is unnecessary for individual orbit-row Fourier kernels.",
            "Pairwise kernel estimation is classically dequantized and cannot support a quantum-advantage claim.",
            "Succinct dense entries do not compile the global row polar or remove candidate normalization.",
        ],
    )


def write_trimmed_row_kernel_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_trimmed_row_kernel_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_trimmed_row_kernel_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
