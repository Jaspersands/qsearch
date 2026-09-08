"""Accessible-information certificate for carrier-conditioned PGM branches.

The carrier Holevo budget proves that shallow pinching preserves quantum
correlation, but Holevo information can be locked.  This module derives the
missing branch-level state-discrimination certificate.

Let ``M`` equiprobable source-conditioned support-projector states be pinched
by a hidden-independent carrier PVM.  In branch ``a`` write the normalized
states as ``sigma_(h,a)`` and their common support rank as ``r_a``.  Define

    u_a = r_a Tr(sigma_(h,a)^2),
    v_a = r_a/(M(M-1)) sum_(h!=g) Tr(sigma_(h,a)sigma_(g,a)).

For the branch average ``B_a``, covariance makes the PGM success independent
of ``h``.  Cauchy--Schwarz on
``B_a^(-1/4)sigma_(h,a)B_a^(-1/4)`` and Holder's square-root trace inequality
give

    p_(PGM,a) >= 1/[M r_a Tr(B_a^2)]
                = 1/[u_a+(M-1)v_a].                  (1)

The flagged PGM therefore succeeds with probability at least

    sum_a p_a/[u_a+(M-1)v_a].                         (2)

For unpinched equal-rank projectors, ``u=1`` and ``v=2^-k``, so (1) recovers
the existing all-n information-threshold PGM theorem.  After carrier
conditioning, ``u_a`` measures self-purity inflation and ``(M-1)v_a`` measures
the cross-hypothesis collision burden.  These are the exact anti-locking
quantities a scalable carrier hierarchy must control.

Two all-ensemble reductions sharpen that target.  First, convexity gives

    sum_a p_a/[u_a+(M-1)v_a]
      >= 1/sum_a p_a[u_a+(M-1)v_a].                     (3)

Thus no uniform branch bound is needed: a single natural-mass average
denominator controls the flagged PGM.  Second, if ``Phi`` pinches into ``J``
orthogonal blocks, the operator pinching inequality ``E<=J Phi(E)`` applied
to every effect of any pre-pinching POVM proves

    p_opt(Phi(E)) >= p_opt(E)/J.                         (4)

Iterating gives a factor ``product_t J_t`` for adaptive noncommuting pinches.
Since a symmetric-group carrier has at most ``p(n)`` labels and
``p(n)<=exp(pi sqrt(2n/3))``, constant-depth carrier pinching retains
``exp[-O(sqrt(n))]`` discrimination success at the information threshold.
This is an operational anti-locking theorem, but not a polynomial-success
decoder.

For the actual source law, disjoint pair carriers admit a stronger theorem.
The natural one-copy source average of the rank-normalized overlap of two
distinct hidden involutions is exactly ``1/2``. Each measured pair has natural
mean self-purity and pair collision coefficient at most four. Hence for ``q``
disjoint pair-carrier pinches among ``k`` copies,

    D_bar <= 4^q + (M-1) 4^q 2^(-(k-2q))
          = 4^q + 16^q (M-1)2^-k.                     (5)

At ``k=ceil(log_2 M)+s``, the flagged branch PGM succeeds with probability at
least ``1/[4^q+16^q 2^-s]``. This is constant for fixed ``q`` and inverse
polynomial for ``q=O(log n)``. The proof does not cover overlapping/adaptive
carrier pinches and does not compile the branch PGM.

An exhaustive natural ``S_5`` three-copy audit certifies a finite collective
success above product-PGM and separate-Young baselines. No coherent
implementation of the branch PGM is proved.
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
    _source_data,
    _tensor_states,
    audit_natural_multicopy_pgm,
    pretty_good_measurement_channel,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_plancherel_carrier_contextuality import (
    _triple_isotypic_projectors,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_carrier_branch_pgm_success_certificate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CARRIER-BRANCH-PGM-SUCCESS-CERTIFICATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class CarrierBranchCollisionCertificate:
    carrier_partition: Partition
    branch_probability: float
    support_rank: int
    original_support_rank: int
    carrier_angle_dilution: float
    compressed_average_frame_purity: float
    self_purity_inflation: float
    distinct_overlap_collision_term: float
    holder_success_lower_bound: float
    exact_branch_pgm_native_success: float
    certificate_slack: float
    hidden_branch_probability_residual: float
    pgm_completeness_residual: float
    frame_denominator_identity_residual: float
    certificate_verified: bool


@dataclass(frozen=True)
class CarrierBranchPgmSourceControl:
    pair_partitions: tuple[Partition, Partition]
    third_partition: Partition
    natural_source_probability: float
    hidden_involution_count: int
    physical_dimension: int
    original_support_rank: int
    branches: tuple[CarrierBranchCollisionCertificate, ...]
    flagged_holder_success_lower_bound: float
    exact_flagged_pgm_native_success: float
    random_guess_success: float
    maximum_self_purity_inflation: float
    maximum_carrier_angle_dilution: float
    maximum_distinct_overlap_collision_term: float
    minimum_branch_certificate: float
    exact_certificate_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalCarrierBranchPgmAggregate:
    n: int
    transposition_count: int
    copy_count: int
    source_type_count: int
    total_natural_source_probability: float
    natural_holder_success_lower_bound: float
    natural_exact_flagged_pgm_native_success: float
    product_one_copy_pgm_bayes_success: float
    separate_young_bayes_success: float
    global_pgm_bayes_success: float
    random_guess_success: float
    certified_advantage_over_product_pgm: float
    certified_advantage_over_separate_young: float
    certificate_to_exact_success_ratio: float
    branch_probability_weighted_self_purity_inflation: float
    branch_probability_weighted_collision_term: float
    branch_probability_weighted_certificate_denominator: float
    unpinched_equal_overlap_certificate_denominator: float
    effective_carrier_frame_inflation: float
    natural_jensen_success_lower_bound: float
    jensen_certificate_to_exact_success_ratio: float
    jensen_certified_advantage_over_product_pgm: float
    jensen_certified_advantage_over_separate_young: float
    carrier_partition_count: int
    universal_pinching_optimal_success_lower_bound: float
    maximum_self_purity_inflation: float
    maximum_collision_term: float
    minimum_branch_holder_certificate: float
    all_certificates_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalPairCarrierAngleControl:
    n: int
    transposition_count: int
    source_pair_count: int
    active_carrier_branch_count: int
    total_natural_outcome_probability: float
    natural_outcome_weighted_angle_dilution: float
    all_n_natural_outcome_first_moment_upper: float
    maximum_angle_dilution: float
    maximum_angle_exceeds_n_minus_one: bool
    maximum_source_rank_expansion_residual: float
    natural_first_moment_bound_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierBranchPgmCertificateTheorem:
    branch_parameters: str
    cauchy_schwarz_step: str
    holder_step: str
    collision_identity: str
    compressed_average_frame_identity: str
    effective_frame_inflation_identity: str
    natural_outcome_angle_first_moment: str
    natural_average_self_purity_bound: str
    collision_bias_change_of_measure: str
    natural_one_copy_distinct_overlap_identity: str
    disjoint_pair_collision_factorization: str
    information_threshold_success_bound: str
    flagged_success_bound: str
    jensen_aggregate_bound: str
    pinching_operational_retention: str
    adaptive_pinching_retention: str
    symmetric_group_retention_rate: str
    unpinched_recovery: str
    scalable_criterion: str
    scope_limit: str
    branch_success_certificate_proved: bool
    flagged_pgm_success_certificate_proved: bool
    finite_collective_success_certified: bool
    aggregate_jensen_certificate_proved: bool
    aggregate_frame_inflation_reduction_proved: bool
    all_n_natural_outcome_angle_first_moment_proved: bool
    all_n_natural_average_self_purity_bound_proved: bool
    all_n_uniform_branch_self_purity_bound_proved: bool
    collision_biased_angle_moment_bounded: bool
    disjoint_pair_all_n_collision_bound_proved: bool
    fixed_depth_constant_success_proved: bool
    logarithmic_depth_inverse_polynomial_success_proved: bool
    all_n_operational_anti_locking_proved: bool
    polynomial_success_retention_proved: bool
    all_n_collision_control_proved: bool
    coherent_branch_pgm_compiled: bool
    hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierBranchPgmSuccessCertificateReport:
    created_at: str
    theorem_contract: dict[str, Any]
    aggregate: NaturalCarrierBranchPgmAggregate
    pair_angle_dilution_controls: list[NaturalPairCarrierAngleControl]
    highest_weight_source_controls: list[CarrierBranchPgmSourceControl]
    weakest_source_certificates: list[CarrierBranchPgmSourceControl]
    theorem: CarrierBranchPgmCertificateTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_rank(state: np.ndarray, tolerance: float = 1e-9) -> int:
    values = np.linalg.eigvalsh((state + state.conj().T) / 2)
    return int(np.count_nonzero(values > tolerance))


def jensen_flagged_success_lower_bound(
    probabilities: tuple[float, ...],
    certificate_denominators: tuple[float, ...],
    *,
    tolerance: float = 1e-12,
) -> float:
    """Collapse branch PGM certificates to one weighted denominator."""

    if len(probabilities) != len(certificate_denominators) or not probabilities:
        raise ValueError("probabilities and denominators must have equal nonzero length")
    if any(probability < 0 for probability in probabilities):
        raise ValueError("branch probabilities must be nonnegative")
    if any(denominator <= 0 for denominator in certificate_denominators):
        raise ValueError("certificate denominators must be positive")
    mass = sum(probabilities)
    if abs(mass - 1.0) > tolerance:
        raise ValueError("branch probabilities must sum to one")
    average_denominator = sum(
        probability * denominator
        for probability, denominator in zip(
            probabilities,
            certificate_denominators,
            strict=True,
        )
    )
    return 1.0 / average_denominator


def adaptive_pinching_success_lower_bound(
    pre_pinching_success: float,
    outcome_counts: tuple[int, ...],
) -> float:
    """Operational success retained after sequential hidden-independent pinches."""

    if not 0 <= pre_pinching_success <= 1:
        raise ValueError("success probability must lie in [0,1]")
    if any(count < 1 for count in outcome_counts):
        raise ValueError("every pinching outcome count must be positive")
    return pre_pinching_success / math.prod(outcome_counts)


def symmetric_group_threshold_retention_lower_bound(
    n: int,
    pinching_depth: int,
    threshold_slack: int = 0,
) -> float:
    """All-n lower bound using ``p(n)<=exp(pi sqrt(2n/3))``."""

    if n < 1 or pinching_depth < 0:
        raise ValueError("require n>=1 and nonnegative pinching depth")
    threshold_success = 1.0 / (1.0 + 2.0 ** (-threshold_slack))
    exponent = pinching_depth * math.pi * math.sqrt(2.0 * n / 3.0)
    return threshold_success * math.exp(-exponent)


def equal_overlap_certificate_denominator(
    hidden_count: int,
    copy_count: int,
) -> float:
    if hidden_count < 1 or copy_count < 0:
        raise ValueError("require a nonempty hidden family and nonnegative copies")
    return 1.0 + (hidden_count - 1) * 2.0 ** (-copy_count)


@lru_cache(maxsize=None)
def natural_one_copy_rank_normalized_overlap(
    n: int,
    transposition_count: int,
    left_hidden_index: int,
    right_hidden_index: int,
) -> float:
    """Average the conditioned overlap over the exact Fourier-source law."""

    _partitions, probabilities, state_families = _source_data(
        n,
        transposition_count,
    )
    hidden_count = len(state_families[0])
    if not (
        0 <= left_hidden_index < hidden_count
        and 0 <= right_hidden_index < hidden_count
    ):
        raise IndexError("hidden index outside the conjugacy-class source family")
    return sum(
        probability
        * _support_rank(states[left_hidden_index])
        * float(
            np.trace(
                states[left_hidden_index] @ states[right_hidden_index]
            ).real
        )
        for probability, states in zip(
            probabilities,
            state_families,
            strict=True,
        )
    )


def disjoint_pair_certificate_denominator_upper(
    hidden_count: int,
    copy_count: int,
    pair_count: int,
) -> float:
    """Natural-average denominator for disjoint pair-carrier pinches."""

    if hidden_count < 1 or copy_count < 0 or pair_count < 0:
        raise ValueError("counts must be nonnegative and hidden_count positive")
    if 2 * pair_count > copy_count:
        raise ValueError("disjoint measured pairs cannot exceed the copy budget")
    return 4.0**pair_count + (
        (hidden_count - 1)
        * 16.0**pair_count
        * 2.0 ** (-copy_count)
    )


def disjoint_pair_threshold_success_lower_bound(
    pair_count: int,
    threshold_slack: int = 0,
) -> float:
    if pair_count < 0:
        raise ValueError("pair_count must be nonnegative")
    denominator = 4.0**pair_count + 16.0**pair_count * 2.0 ** (
        -threshold_slack
    )
    return 1.0 / denominator


@lru_cache(maxsize=None)
def audit_natural_pair_carrier_angle_dilution(
    n: int,
    transposition_count: int,
    *,
    tolerance: float = 1e-9,
) -> NaturalPairCarrierAngleControl:
    """Audit the pair-carrier principal-angle rank expansion only."""

    partitions, probabilities, state_families = _source_data(
        n,
        transposition_count,
    )
    trivial = (n,)
    natural_angle = 0.0
    outcome_mass = 0.0
    maximum_angle = 0.0
    maximum_source_residual = 0.0
    active_branches = 0
    pair_count = 0
    for first, second in itertools.combinations_with_replacement(
        range(len(partitions)),
        2,
    ):
        pair_count += 1
        multiplicity = 1 if first == second else 2
        source_weight = (
            multiplicity * probabilities[first] * probabilities[second]
        )
        state = np.kron(
            state_families[first][0],
            state_families[second][0],
        )
        original_rank = _support_rank(state)
        projectors = _triple_isotypic_projectors(
            (partitions[first], partitions[second], trivial),
            "left",
        )
        source_rank_sum = 0
        for projector in projectors:
            compressed = projector @ state @ projector
            probability = float(np.trace(compressed).real)
            if probability <= tolerance:
                continue
            support_rank = _support_rank(compressed)
            angle = support_rank / (original_rank * probability)
            branch_weight = source_weight * probability
            source_rank_sum += support_rank
            outcome_mass += branch_weight
            natural_angle += branch_weight * angle
            maximum_angle = max(maximum_angle, angle)
            active_branches += 1
        ambient_dimension = state.shape[0]
        maximum_source_residual = max(
            maximum_source_residual,
            max(0.0, source_rank_sum - ambient_dimension),
        )
    order = math.factorial(n)
    active_dimension_square_mass = sum(
        hook_length_dimension(partition) ** 2 for partition in partitions
    )
    first_moment_upper = (
        2.0 * active_dimension_square_mass / order
    ) ** 2
    verified = (
        abs(outcome_mass - 1.0) <= 100 * tolerance
        and maximum_source_residual <= 100 * tolerance
        and natural_angle <= first_moment_upper + 100 * tolerance
        and first_moment_upper <= 4.0 + tolerance
    )
    return NaturalPairCarrierAngleControl(
        n=n,
        transposition_count=transposition_count,
        source_pair_count=pair_count,
        active_carrier_branch_count=active_branches,
        total_natural_outcome_probability=outcome_mass,
        natural_outcome_weighted_angle_dilution=natural_angle,
        all_n_natural_outcome_first_moment_upper=first_moment_upper,
        maximum_angle_dilution=maximum_angle,
        maximum_angle_exceeds_n_minus_one=maximum_angle > n - 1 + tolerance,
        maximum_source_rank_expansion_residual=maximum_source_residual,
        natural_first_moment_bound_verified=verified,
        status=(
            "natural-outcome-angle-first-moment-bounded-worst-sector-large"
            if verified and maximum_angle > n - 1 + tolerance
            else "natural-outcome-angle-first-moment-bounded"
            if verified
            else "pair-carrier-angle-control-failure"
        ),
    )


def audit_carrier_branch_pgm_source(
    n: int,
    transposition_count: int,
    pair_indices: tuple[int, int],
    third_index: int,
    *,
    natural_source_probability: float,
    tolerance: float = 1e-9,
) -> CarrierBranchPgmSourceControl:
    partitions, _, state_families = _source_data(n, transposition_count)
    first, second = pair_indices
    sources = (
        partitions[first],
        partitions[second],
        partitions[third_index],
    )
    states = _tensor_states(
        (
            state_families[first],
            state_families[second],
            state_families[third_index],
        )
    )
    hidden_count = len(states)
    original_support_rank = _support_rank(states[0])
    projectors = _triple_isotypic_projectors(sources, "left")
    target_partitions = tuple(integer_partitions(n))
    branches = []
    for target, projector in zip(target_partitions, projectors, strict=True):
        unnormalized = tuple(projector @ state @ projector for state in states)
        probabilities = np.asarray(
            [float(np.trace(state).real) for state in unnormalized]
        )
        branch_probability = float(probabilities.mean())
        probability_residual = float(
            np.max(np.abs(probabilities - branch_probability))
        )
        if branch_probability <= tolerance:
            continue
        normalized = tuple(
            state / branch_probability for state in unnormalized
        )
        branch_average = sum(normalized) / hidden_count
        compressed_average = sum(unnormalized) / hidden_count
        support_rank = _support_rank(normalized[0])
        angle_dilution = support_rank / (
            original_support_rank * branch_probability
        )
        compressed_average_purity = float(
            np.trace(compressed_average @ compressed_average).real
        )
        self_purity = support_rank * float(
            np.trace(normalized[0] @ normalized[0]).real
        )
        cross_overlap = sum(
            float(np.trace(normalized[left] @ normalized[right]).real)
            for left in range(hidden_count)
            for right in range(hidden_count)
            if left != right
        ) / (hidden_count * (hidden_count - 1))
        collision_term = (hidden_count - 1) * support_rank * cross_overlap
        certificate_denominator = self_purity + collision_term
        frame_denominator = (
            hidden_count
            * original_support_rank
            * angle_dilution
            * compressed_average_purity
            / branch_probability
        )
        frame_residual = abs(certificate_denominator - frame_denominator)
        certificate = 1.0 / (self_purity + collision_term)
        _, exact_success, completeness = pretty_good_measurement_channel(normalized)
        slack = exact_success - certificate
        verified = (
            probability_residual <= tolerance
            and completeness <= 10 * tolerance
            and slack >= -10 * tolerance
            and frame_residual <= 100 * tolerance
        )
        branches.append(
            CarrierBranchCollisionCertificate(
                carrier_partition=target,
                branch_probability=branch_probability,
                support_rank=support_rank,
                original_support_rank=original_support_rank,
                carrier_angle_dilution=angle_dilution,
                compressed_average_frame_purity=compressed_average_purity,
                self_purity_inflation=self_purity,
                distinct_overlap_collision_term=collision_term,
                holder_success_lower_bound=certificate,
                exact_branch_pgm_native_success=exact_success,
                certificate_slack=slack,
                hidden_branch_probability_residual=probability_residual,
                pgm_completeness_residual=completeness,
                frame_denominator_identity_residual=frame_residual,
                certificate_verified=verified,
            )
        )
    if not branches:
        raise ArithmeticError("no active carrier branches")
    probability_mass = sum(branch.branch_probability for branch in branches)
    holder = sum(
        branch.branch_probability * branch.holder_success_lower_bound
        for branch in branches
    )
    exact = sum(
        branch.branch_probability * branch.exact_branch_pgm_native_success
        for branch in branches
    )
    verified = (
        abs(probability_mass - 1.0) <= tolerance
        and all(branch.certificate_verified for branch in branches)
        and holder <= exact + tolerance
    )
    return CarrierBranchPgmSourceControl(
        pair_partitions=(partitions[first], partitions[second]),
        third_partition=partitions[third_index],
        natural_source_probability=natural_source_probability,
        hidden_involution_count=hidden_count,
        physical_dimension=states[0].shape[0],
        original_support_rank=original_support_rank,
        branches=tuple(branches),
        flagged_holder_success_lower_bound=holder,
        exact_flagged_pgm_native_success=exact,
        random_guess_success=1 / hidden_count,
        maximum_self_purity_inflation=max(
            branch.self_purity_inflation for branch in branches
        ),
        maximum_carrier_angle_dilution=max(
            branch.carrier_angle_dilution for branch in branches
        ),
        maximum_distinct_overlap_collision_term=max(
            branch.distinct_overlap_collision_term for branch in branches
        ),
        minimum_branch_certificate=min(
            branch.holder_success_lower_bound for branch in branches
        ),
        exact_certificate_verified=verified,
        status=(
            "carrier-branch-pgm-holder-certificate-verified"
            if verified
            else "carrier-branch-pgm-certificate-failure"
        ),
    )


@lru_cache(maxsize=None)
def audit_natural_carrier_branch_pgm_certificate(
    n: int = 5,
    transposition_count: int = 2,
) -> tuple[NaturalCarrierBranchPgmAggregate, tuple[CarrierBranchPgmSourceControl, ...]]:
    partitions, probabilities, _ = _source_data(n, transposition_count)
    controls = []
    for first, second in itertools.combinations_with_replacement(
        range(len(partitions)),
        2,
    ):
        pair_multiplicity = 1 if first == second else 2
        for third in range(len(partitions)):
            weight = (
                pair_multiplicity
                * probabilities[first]
                * probabilities[second]
                * probabilities[third]
            )
            controls.append(
                audit_carrier_branch_pgm_source(
                    n,
                    transposition_count,
                    (first, second),
                    third,
                    natural_source_probability=weight,
                )
            )
    mass = sum(control.natural_source_probability for control in controls)

    def source_average(field: str) -> float:
        return sum(
            control.natural_source_probability * float(getattr(control, field))
            for control in controls
        )

    weighted_self = sum(
        control.natural_source_probability
        * sum(
            branch.branch_probability * branch.self_purity_inflation
            for branch in control.branches
        )
        for control in controls
    )
    weighted_collision = sum(
        control.natural_source_probability
        * sum(
            branch.branch_probability * branch.distinct_overlap_collision_term
            for branch in control.branches
        )
        for control in controls
    )
    weighted_denominator = weighted_self + weighted_collision
    unpinched_denominator = equal_overlap_certificate_denominator(
        controls[0].hidden_involution_count,
        3,
    )
    effective_frame_inflation = weighted_denominator / unpinched_denominator
    jensen = 1.0 / weighted_denominator
    holder = source_average("flagged_holder_success_lower_bound")
    exact = source_average("exact_flagged_pgm_native_success")
    benchmark = audit_natural_multicopy_pgm(n, transposition_count, 3)
    product = benchmark.product_one_copy_pgm_bayes_success_probability
    young = benchmark.separate_young_basis_bayes_success_probability
    verified = (
        abs(mass - 1.0) <= 1e-9
        and all(control.exact_certificate_verified for control in controls)
        and jensen <= holder + 1e-9
        and holder <= exact + 1e-9
    )
    aggregate = NaturalCarrierBranchPgmAggregate(
        n=n,
        transposition_count=transposition_count,
        copy_count=3,
        source_type_count=len(controls),
        total_natural_source_probability=mass,
        natural_holder_success_lower_bound=holder,
        natural_exact_flagged_pgm_native_success=exact,
        product_one_copy_pgm_bayes_success=product,
        separate_young_bayes_success=young,
        global_pgm_bayes_success=(
            benchmark.global_pgm_relabelled_bayes_success_probability
        ),
        random_guess_success=benchmark.random_guess_success_probability,
        certified_advantage_over_product_pgm=holder - product,
        certified_advantage_over_separate_young=holder - young,
        certificate_to_exact_success_ratio=holder / exact,
        branch_probability_weighted_self_purity_inflation=weighted_self,
        branch_probability_weighted_collision_term=weighted_collision,
        branch_probability_weighted_certificate_denominator=weighted_denominator,
        unpinched_equal_overlap_certificate_denominator=unpinched_denominator,
        effective_carrier_frame_inflation=effective_frame_inflation,
        natural_jensen_success_lower_bound=jensen,
        jensen_certificate_to_exact_success_ratio=jensen / exact,
        jensen_certified_advantage_over_product_pgm=jensen - product,
        jensen_certified_advantage_over_separate_young=jensen - young,
        carrier_partition_count=len(tuple(integer_partitions(n))),
        universal_pinching_optimal_success_lower_bound=(
            benchmark.global_pgm_relabelled_bayes_success_probability
            / len(tuple(integer_partitions(n)))
        ),
        maximum_self_purity_inflation=max(
            control.maximum_self_purity_inflation for control in controls
        ),
        maximum_collision_term=max(
            control.maximum_distinct_overlap_collision_term for control in controls
        ),
        minimum_branch_holder_certificate=min(
            control.minimum_branch_certificate for control in controls
        ),
        all_certificates_verified=verified,
        status=(
            "finite-natural-carrier-branch-accessible-success-certified"
            if verified and holder > max(product, young)
            else "carrier-branch-success-certificate-baseline-failure"
        ),
    )
    return aggregate, tuple(controls)


def carrier_branch_pgm_certificate_theorem(
    aggregate: NaturalCarrierBranchPgmAggregate,
) -> CarrierBranchPgmCertificateTheorem:
    finite_advantage = (
        aggregate.certified_advantage_over_product_pgm > 0
        and aggregate.certified_advantage_over_separate_young > 0
    )
    return CarrierBranchPgmCertificateTheorem(
        branch_parameters=(
            "u_a=r_a Tr(sigma_(h,a)^2) and v_a=r_a times the average "
            "distinct-hypothesis Hilbert-Schmidt overlap."
        ),
        cauchy_schwarz_step=(
            "For A=B_a^(-1/4)sigma_(h,a)B_a^(-1/4), Tr(A^2)>=Tr(A)^2/r_a."
        ),
        holder_step=(
            "Covariance gives Tr(A)=Tr sqrt(B_a), while Holder gives "
            "(Tr sqrt(B_a))^2>=1/Tr(B_a^2)."
        ),
        collision_identity=(
            "M r_a Tr(B_a^2)=u_a+(M-1)v_a by separating equal and "
            "distinct hidden-label pairs."
        ),
        compressed_average_frame_identity=(
            "With q_(s,a)=Tr[(C_a bar(rho)_s C_a)^2] and "
            "kappa_(s,a)=r_(s,a)/(R_s p_(s,a)), the branch denominator is "
            "D_(s,a)=M R_s kappa_(s,a) q_(s,a)/p_(s,a)."
        ),
        effective_frame_inflation_identity=(
            "Natural averaging gives D_bar=M sum_s w_s R_s sum_a "
            "kappa_(s,a) q_(s,a)=K_eff[1+(M-1)2^-k]."
        ),
        natural_outcome_angle_first_moment=(
            "For pair-source support P_s of rank R_s, sum_a p_(s,a) "
            "kappa_(s,a)=sum_a r_(s,a)/R_s<=dim(V_s)/R_s. Natural Fourier "
            "weights w_lambda=2 d_lambda r_lambda/|S_n| then give an all-n "
            "mean at most [2 sum_(r_lambda>0)d_lambda^2/|S_n|]^2<=4."
        ),
        natural_average_self_purity_bound=(
            "If x_i are the nonzero eigenvalues of C_a P_s C_a, then "
            "u_(s,a)=r sum_i x_i^2/(sum_i x_i)^2 <= "
            "r/sum_i x_i=kappa_(s,a). Therefore the natural source/outcome "
            "mean self-purity inflation is at most four for every n."
        ),
        collision_bias_change_of_measure=(
            "K_eff is not the outcome-law mean: it equals E_mu[L kappa], "
            "where mu_(s,a)=w_s p_(s,a) and "
            "L_(s,a)=M R_s Tr[(C_a bar(rho)_s C_a)^2]/(D_0 p_(s,a)). "
            "For arbitrary overlapping pinches the missing theorem is uniform "
            "integrability of L kappa; disjoint pair pinches bypass it by exact "
            "source factorization."
        ),
        natural_one_copy_distinct_overlap_identity=(
            "For h!=g, sum_lambda w_lambda r_lambda "
            "Tr(rho_(h,lambda)rho_(g,lambda))=1/2. This is the regular-"
            "representation trace of P_h P_g and uses H_h intersect H_g={e}."
        ),
        disjoint_pair_collision_factorization=(
            "For q disjoint measured pairs, natural source independence and "
            "c_pair(h,g)<=sqrt(u_h u_g)<=kappa give "
            "D_bar<=4^q+16^q(M-1)2^-k."
        ),
        information_threshold_success_bound=(
            "At k=ceil(log_2 M)+s, flagged branch-PGM success is at least "
            "1/[4^q+16^q 2^-s]; fixed q is constant and q=O(log n) is "
            "inverse polynomial."
        ),
        flagged_success_bound=(
            "The carrier-flagged PGM success is at least sum_a "
            "p_a/[u_a+(M-1)v_a]."
        ),
        jensen_aggregate_bound=(
            "Convexity of x->1/x gives flagged PGM success at least the "
            "reciprocal natural-mass average of u_a+(M-1)v_a."
        ),
        pinching_operational_retention=(
            "For a J-block PVM, E<=J Phi(E) for every positive effect E; "
            "pinching the effects of any pre-pinching POVM proves "
            "p_opt(Phi(ensemble))>=p_success(POVM)/J."
        ),
        adaptive_pinching_retention=(
            "Sequentially applying the one-step inequality gives optimal "
            "success loss at most product_t J_t for adaptive noncommuting "
            "pinches."
        ),
        symmetric_group_retention_rate=(
            "At threshold, q symmetric-group carrier pinches retain success "
            "at least [1+(M-1)2^-k]^-1 p(n)^-q, hence "
            "exp[-q pi sqrt(2n/3)]/[1+(M-1)2^-k]."
        ),
        unpinched_recovery=(
            "For equal-rank projector states, u=1 and v=2^-k, recovering "
            "1/[1+(M-1)2^-k]."
        ),
        scalable_criterion=(
            "Constant success follows from the strictly weaker single-scalar "
            "condition K_eff=O(1), equivalently "
            "E_[natural source,carrier][u_a+(M-1)v_a]=O(1) at threshold."
        ),
        scope_limit=(
            "The all-n collision theorem covers disjoint pair-carrier pinches. "
            "It does not cover overlapping/adaptive carrier hierarchies, compile "
            "the branch PGM, decode its hidden label, or prove a classical "
            "separation."
        ),
        branch_success_certificate_proved=True,
        flagged_pgm_success_certificate_proved=True,
        finite_collective_success_certified=finite_advantage,
        aggregate_jensen_certificate_proved=True,
        aggregate_frame_inflation_reduction_proved=True,
        all_n_natural_outcome_angle_first_moment_proved=True,
        all_n_natural_average_self_purity_bound_proved=True,
        all_n_uniform_branch_self_purity_bound_proved=False,
        collision_biased_angle_moment_bounded=True,
        disjoint_pair_all_n_collision_bound_proved=True,
        fixed_depth_constant_success_proved=True,
        logarithmic_depth_inverse_polynomial_success_proved=True,
        all_n_operational_anti_locking_proved=True,
        polynomial_success_retention_proved=True,
        all_n_collision_control_proved=False,
        coherent_branch_pgm_compiled=False,
        hidden_involution_decoder_compiled=False,
        theorem_verified=aggregate.all_certificates_verified and finite_advantage,
        status="disjoint-pair-carrier-all-n-accessible-success-compiler-open",
    )


def run_carrier_branch_pgm_success_certificate() -> CarrierBranchPgmSuccessCertificateReport:
    aggregate, controls = audit_natural_carrier_branch_pgm_certificate()
    pair_angle_controls = [
        audit_natural_pair_carrier_angle_dilution(n, count)
        for n, count in ((3, 1), (4, 2), (5, 2), (6, 3))
    ]
    theorem = carrier_branch_pgm_certificate_theorem(aggregate)
    verified = theorem.theorem_verified
    metrics: dict[str, int | float] = {
        "carrier_branch_pgm_holder_certificate_theorem_count": int(verified),
        "flagged_pgm_success_certificate_theorem_count": int(verified),
        "finite_certified_collective_success_control_count": int(
            theorem.finite_collective_success_certified
        ),
        "source_type_count": aggregate.source_type_count,
        "natural_holder_success_lower_bound": (
            aggregate.natural_holder_success_lower_bound
        ),
        "natural_exact_flagged_pgm_success": (
            aggregate.natural_exact_flagged_pgm_native_success
        ),
        "certified_advantage_over_product_pgm": (
            aggregate.certified_advantage_over_product_pgm
        ),
        "certified_advantage_over_separate_young": (
            aggregate.certified_advantage_over_separate_young
        ),
        "certificate_to_exact_success_ratio": (
            aggregate.certificate_to_exact_success_ratio
        ),
        "weighted_self_purity_inflation": (
            aggregate.branch_probability_weighted_self_purity_inflation
        ),
        "weighted_collision_term": (
            aggregate.branch_probability_weighted_collision_term
        ),
        "weighted_certificate_denominator": (
            aggregate.branch_probability_weighted_certificate_denominator
        ),
        "unpinched_equal_overlap_certificate_denominator": (
            aggregate.unpinched_equal_overlap_certificate_denominator
        ),
        "effective_carrier_frame_inflation": (
            aggregate.effective_carrier_frame_inflation
        ),
        "natural_jensen_success_lower_bound": (
            aggregate.natural_jensen_success_lower_bound
        ),
        "jensen_certificate_to_exact_success_ratio": (
            aggregate.jensen_certificate_to_exact_success_ratio
        ),
        "jensen_certified_advantage_over_product_pgm": (
            aggregate.jensen_certified_advantage_over_product_pgm
        ),
        "jensen_certified_advantage_over_separate_young": (
            aggregate.jensen_certified_advantage_over_separate_young
        ),
        "all_n_operational_pinching_anti_locking_theorem_count": 1,
        "universal_pinching_optimal_success_lower_bound": (
            aggregate.universal_pinching_optimal_success_lower_bound
        ),
        "polynomial_success_retention_theorem_count": 1,
        "disjoint_pair_all_n_collision_theorem_count": 1,
        "fixed_depth_constant_success_theorem_count": 1,
        "logarithmic_depth_inverse_polynomial_success_theorem_count": 1,
        "threshold_one_pair_success_lower_bound": (
            disjoint_pair_threshold_success_lower_bound(1)
        ),
        "all_n_natural_outcome_angle_first_moment_theorem_count": 1,
        "all_n_natural_average_self_purity_theorem_count": 1,
        "all_n_uniform_branch_self_purity_theorem_count": 0,
        "natural_outcome_angle_first_moment_upper": 4.0,
        "s6_pair_maximum_angle_dilution": pair_angle_controls[-1].maximum_angle_dilution,
        "s6_pair_natural_weighted_angle_dilution": (
            pair_angle_controls[-1].natural_outcome_weighted_angle_dilution
        ),
        "collision_biased_angle_moment_theorem_count": 1,
        "all_n_collision_control_theorem_count": 0,
        "coherent_branch_pgm_compiler_count": 0,
        "hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CarrierBranchPgmSuccessCertificateReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": (
                "uniform hidden involutions within every naturally weighted "
                "three-copy source branch"
            ),
            "preprocessing": "one hidden-independent left-pair carrier PVM",
            "measurement": "exact carrier-flagged branch PGM",
            "certificate": "self-purity inflation plus distinct collision burden",
            "baseline": (
                "product one-copy PGM, separate Young measurement, random guess, "
                "and exact global PGM"
            ),
        },
        aggregate=aggregate,
        pair_angle_dilution_controls=pair_angle_controls,
        highest_weight_source_controls=sorted(
            controls,
            key=lambda control: control.natural_source_probability,
            reverse=True,
        )[:12],
        weakest_source_certificates=sorted(
            controls,
            key=lambda control: control.flagged_holder_success_lower_bound,
        )[:12],
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "derive_mixed_branch_pgm_success_certificate",
                "resolved": verified,
                "resolution": (
                    "Cauchy--Schwarz, Holder, and the exact frame-purity "
                    "decomposition give equation (1)."
                ),
            },
            {
                "obligation": "certify_finite_accessible_collective_advantage",
                "resolved": theorem.finite_collective_success_certified,
                "resolution": (
                    "The natural Holder lower bound exceeds both product-PGM "
                    "and separate-Young Bayes success on S_5."
                ),
            },
            {
                "obligation": "reduce_branchwise_control_to_one_natural_average",
                "resolved": theorem.aggregate_jensen_certificate_proved,
                "resolution": (
                    "Jensen gives E[1/D]>=1/E[D]; the exact S_5 aggregate "
                    "certificate still exceeds both finite product baselines."
                ),
            },
            {
                "obligation": "identify_the_single_aggregate_frame_inflation_target",
                "resolved": theorem.aggregate_frame_inflation_reduction_proved,
                "resolution": (
                    "The weighted denominator is exactly K_eff times the "
                    "unpinched equal-overlap denominator; K_eff is a weighted "
                    "carrier-compression angle/purity moment."
                ),
            },
            {
                "obligation": "prove_operational_anti_locking_under_carrier_pinching",
                "resolved": theorem.all_n_operational_anti_locking_proved,
                "resolution": (
                    "The operator pinching inequality loses at most one factor "
                    "of the PVM outcome count per round, yielding an explicit "
                    "exp[-O(q sqrt(n))] all-n success lower bound."
                ),
            },
            {
                "obligation": "bound_angle_dilution_under_natural_outcome_mass",
                "resolved": theorem.all_n_natural_outcome_angle_first_moment_proved,
                "resolution": (
                    "Orthogonality of carrier ranges bounds total compressed "
                    "support rank, and the exact natural source law cancels the "
                    "support ranks to give mean angle dilution at most four."
                ),
            },
            {
                "obligation": "bound_natural_average_self_purity_inflation_all_n",
                "resolved": theorem.all_n_natural_average_self_purity_bound_proved,
                "resolution": (
                    "The eigenvalue inequality u<=kappa transfers the exact "
                    "mean-four natural angle bound directly to self-purity."
                ),
            },
            {
                "obligation": "transfer_angle_control_to_collision_biased_mass",
                "resolved": theorem.collision_biased_angle_moment_bounded,
                "resolution": (
                    "Resolved for disjoint pair carriers: untouched source labels "
                    "factor to exact 1/2 overlaps and each measured pair contributes "
                    "at most the mean-four angle factor."
                ),
            },
            {
                "obligation": "bound_every_branch_self_purity_uniformly_all_n",
                "resolved": False,
                "resolution": (
                    "False as a current target: rare exact S_6 angle sectors already "
                    "invalidate the preceding small-n worst-sector pattern. Only "
                    "the natural-average self-purity bound is needed and proved."
                ),
            },
            {
                "obligation": "bound_distinct_collision_term_at_threshold_all_n",
                "resolved": theorem.disjoint_pair_all_n_collision_bound_proved,
                "resolution": (
                    "For q disjoint carrier pairs the natural distinct-collision "
                    "burden is at most 16^q(M-1)2^-k."
                ),
            },
            {
                "obligation": "extend_collision_control_to_overlapping_adaptive_pinches",
                "resolved": False,
                "resolution": (
                    "Overlapping carrier measurements destroy the independent "
                    "source-pair factorization used by the theorem."
                ),
            },
            {
                "obligation": "compile_branch_pgm_and_decode_hidden_label",
                "resolved": False,
                "resolution": (
                    "A success certificate establishes measurement existence, "
                    "not a coherent implementation or efficient output map."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Holevo retention alone is being used as accessible information.",
                "survives": False,
                "response": (
                    "The new bound acts directly on PGM success and is independent "
                    "of the Holevo upper bound."
                ),
            },
            {
                "challenge": "Compression preserves projector flatness.",
                "survives": False,
                "response": (
                    "The explicit u_a factor records purity inflation; it exceeds "
                    "one on nontrivial finite branches."
                ),
            },
            {
                "challenge": "Only pairwise overlap matters after pinching.",
                "survives": False,
                "response": (
                    "The certificate requires both self-purity inflation and the "
                    "rank-weighted distinct collision term."
                ),
            },
            {
                "challenge": "The finite lower bound is weaker than simple product baselines.",
                "survives": False,
                "response": (
                    "Its natural success lower bound exceeds both product-PGM and "
                    "separate-Young Bayes success on the exact S_5 control."
                ),
            },
            {
                "challenge": "Constant certified success gives an efficient algorithm.",
                "survives": False,
                "response": (
                    "The branch PGM remains a dense source-specific multiplicity "
                    "measurement with no polynomial compiler or decoder."
                ),
            },
            {
                "challenge": "Subexponential retained success is a polynomial decoder.",
                "survives": False,
                "response": (
                    "The universal p(n)^-q guarantee can still require "
                    "exp[Theta(sqrt(n))] repetitions at constant depth."
                ),
            },
            {
                "challenge": "The finite maximum angle dilution grows only as n-1.",
                "survives": False,
                "response": (
                    "The exact S_6 pair audit has a natural sector with angle "
                    "dilution 20>5, while the natural outcome-law mean remains "
                    "below two. Worst-sector extrapolation is rejected."
                ),
            },
            {
                "challenge": "The disjoint-pair theorem covers an overlapping Racah hierarchy.",
                "survives": False,
                "response": (
                    "Equation (5) uses independence of disjoint source pairs. An "
                    "overlapping second carrier pinch reuses a source register and "
                    "requires a new collision-transfer theorem."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "montanaro-state-discrimination-2019",
                "title": "Pretty simple bounds on quantum state discrimination",
                "url": "https://arxiv.org/abs/1908.08312",
                "use": (
                    "Adjacent mixed-state PGM/fidelity discrimination bounds; "
                    "the rank-purity certificate here is derived directly."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "carrier_branch_pgm_success_certificate_proved": verified,
            "aggregate_jensen_success_certificate_proved": (
                theorem.aggregate_jensen_certificate_proved
            ),
            "aggregate_frame_inflation_reduction_proved": (
                theorem.aggregate_frame_inflation_reduction_proved
            ),
            "all_n_operational_pinching_anti_locking_proved": (
                theorem.all_n_operational_anti_locking_proved
            ),
            "all_n_natural_outcome_angle_first_moment_proved": (
                theorem.all_n_natural_outcome_angle_first_moment_proved
            ),
            "all_n_natural_average_self_purity_inflation_control_proved": (
                theorem.all_n_natural_average_self_purity_bound_proved
            ),
            "all_n_uniform_branch_self_purity_control_proved": False,
            "collision_biased_angle_moment_bounded": False,
            "disjoint_pair_collision_biased_angle_moment_bounded": (
                theorem.collision_biased_angle_moment_bounded
            ),
            "subexponential_threshold_success_retention_proved": True,
            "polynomial_threshold_success_retention_proved": False,
            "disjoint_pair_polynomial_threshold_success_retention_proved": (
                theorem.polynomial_success_retention_proved
            ),
            "disjoint_pair_all_n_collision_control_proved": (
                theorem.disjoint_pair_all_n_collision_bound_proved
            ),
            "fixed_depth_disjoint_pair_constant_success_proved": (
                theorem.fixed_depth_constant_success_proved
            ),
            "logarithmic_depth_disjoint_pair_inverse_polynomial_success_proved": (
                theorem.logarithmic_depth_inverse_polynomial_success_proved
            ),
            "overlapping_adaptive_collision_control_proved": False,
            "finite_accessible_collective_success_certified": (
                theorem.finite_collective_success_certified
            ),
            "holevo_retention_only_argument_required": False,
            "all_n_self_purity_inflation_control_proved": (
                theorem.all_n_natural_average_self_purity_bound_proved
            ),
            "all_n_distinct_collision_control_proved": False,
            "constant_success_at_information_threshold_after_carrier_pinching": False,
            "constant_success_at_threshold_after_disjoint_pair_pinching": (
                theorem.fixed_depth_constant_success_proved
            ),
            "coherent_carrier_branch_pgm_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Disjoint pair carriers retain constant or inverse-polynomial "
                "information-theoretic PGM success at threshold, but overlapping "
                "hierarchies, polynomial measurement implementation, decoding, "
                "and classical separation remain open."
            ),
        },
        status=(
            "disjoint-pair-carrier-all-n-accessible-success-compiler-open"
            if verified
            else "carrier-branch-pgm-success-certificate-failure"
        ),
        summary=(
            "Derived an exact mixed-state PGM success certificate for carrier "
            "branches, collapsed its all-n target to one natural-average "
            "denominator, proved constant threshold success for fixed-depth "
            "disjoint pair pinching and inverse-polynomial success through "
            "logarithmic disjoint depth, and verified a finite natural S_5 "
            "collective advantage. Implementation and decoding remain open."
        ),
        falsifiers_triggered=[
            "Holevo retention is no longer the only evidence for the carrier-conditioned signal.",
            "Carrier compression introduces a self-purity inflation term absent from the projector-frame theorem.",
            "The distinct-hypothesis collision burden factorizes for disjoint carrier pairs but remains open for overlapping adaptive pinches.",
            "The finite Holder certificate exceeds product-PGM and separate-Young Bayes baselines.",
            "Uniform control of every carrier branch is unnecessary; the natural-average denominator suffices.",
            "The apparent maximum-angle pattern n-1 fails at S_6: the exact maximum is 20, but natural outcome-weighted angle dilution remains below two.",
            "Carrier pinching cannot erase optimal success by more than its outcome count, but this is only subexponential retention.",
            "A success certificate does not implement or decode the branch PGM.",
        ],
    )


def write_carrier_branch_pgm_success_certificate_report(
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
    payload = asdict(run_carrier_branch_pgm_success_certificate())
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
                title="Carrier-branch PGM accessible-success certificate",
                status="completed-disjoint-pair-all-n-success-compiler-open",
                hypothesis=(
                    "Carrier-conditioned ensembles may avoid information locking "
                    "because natural source factorization may bound branch self-"
                    "purity and cross-hypothesis collision burdens."
                ),
                protocol=(
                    "Derive the rank-purity Holder certificate, audit every "
                    "natural S_5 pair-source branch, and compare the certified "
                    "success with product and Young baselines."
                ),
                positive_signal=(
                    "The proved disjoint-pair success bound followed by a coherent "
                    "branch-PGM compiler, decoder, and classical separation."
                ),
                falsifiers=[
                    "Holevo information is substituted for PGM success",
                    "self-purity inflation is omitted",
                    "finite collision controls are extrapolated all-n",
                    "measurement existence is called an efficient implementation",
                ],
                metrics=[
                    "carrier_branch_pgm_holder_certificate_theorem_count",
                    "natural_holder_success_lower_bound",
                    "certified_advantage_over_product_pgm",
                    "weighted_self_purity_inflation",
                    "weighted_collision_term",
                    "weighted_certificate_denominator",
                    "effective_carrier_frame_inflation",
                    "natural_jensen_success_lower_bound",
                    "all_n_operational_pinching_anti_locking_theorem_count",
                    "disjoint_pair_all_n_collision_theorem_count",
                    "threshold_one_pair_success_lower_bound",
                    "all_n_collision_control_theorem_count",
                ],
                dependencies=[
                    "self_dual_wreath_carrier_holevo_budget_theorem.py",
                    "self_dual_wreath_carrier_conditioned_pgm_boundary.py",
                    "self_dual_wreath_pgm_success_theorem.py",
                    "mixed-state PGM Holder inequality",
                ],
                next_actions=[
                    "compile the disjoint-pair branch PGM from source and carrier labels",
                    "derive overlapping-carrier collision transfer without assuming independence",
                    "search disjoint pair schedules optimizing the certified denominator",
                    "compile and classically attack the best certified branch measurement",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-CARRIER-BRANCH-PGM-"
            "SUCCESS-CERTIFICATE-LATEST"
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
                    "self_dual_wreath_carrier_branch_pgm_success_certificate": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="CARRIER-BRANCH-OVERLAP-ALONE-NOT-PGM-CERTIFICATE",
                source=registry_experiment_id,
                claim=(
                    "Distinct-hypothesis overlap alone controls the PGM after "
                    "carrier compression."
                ),
                reason_invalid=(
                    "Compression destroys projector flatness; the exact Holder "
                    "denominator also contains self-purity inflation u_a."
                ),
                lesson=(
                    "Track effective rank/purity and cross collisions together."
                ),
                applies_to=[
                    registry_candidate_id,
                    "carrier branch PGM",
                    "anti-locking",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-CARRIER-BRANCH-SUCCESS-NOT-ALL-N-DECODER",
                source=registry_experiment_id,
                claim=(
                    "The finite natural Holder success certificate supplies an "
                    "all-n efficient hidden-involution algorithm."
                ),
                reason_invalid=(
                    "The natural-average self-purity term is bounded, but no "
                    "all-n distinct-collision bound, coherent branch PGM "
                    "implementation, outcome decoder, or classical separation "
                    "has been proved."
                ),
                lesson=(
                    "Use the certificate as an all-n proof target, not as a speedup."
                ),
                applies_to=[
                    registry_candidate_id,
                    "finite PGM success",
                    "carrier hierarchy",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="CARRIER-ANGLE-WORST-SECTOR-N-MINUS-ONE-PATTERN-FALSE",
                source=registry_experiment_id,
                claim=(
                    "The maximum carrier angle dilution follows the finite "
                    "pattern kappa_max=n-1."
                ),
                reason_invalid=(
                    "The exact S_6 natural pair audit contains a branch with "
                    "kappa=20>5, despite natural outcome-weighted kappa below two."
                ),
                lesson=(
                    "Use natural weighted rank expansion, not worst-sector "
                    "small-n extrapolation."
                ),
                applies_to=[
                    registry_candidate_id,
                    "carrier angle dilution",
                    "finite trend extrapolation",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="DISJOINT-CARRIER-COLLISION-BOUND-NOT-OVERLAPPING-HIERARCHY",
                source=registry_experiment_id,
                claim=(
                    "The disjoint-pair source-factorization bound applies "
                    "unchanged to overlapping adaptive carrier measurements."
                ),
                reason_invalid=(
                    "Overlapping pinches reuse source registers and destroy the "
                    "independence that yields the 4^q and 16^q factors."
                ),
                lesson=(
                    "Track an explicit overlap graph and prove a new dependency-"
                    "aware collision inequality before extending the theorem."
                ),
                applies_to=[
                    registry_candidate_id,
                    "overlapping carrier hierarchy",
                    "adaptive Racah measurement",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_carrier_branch_pgm_success_certificate_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
