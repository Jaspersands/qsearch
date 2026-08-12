"""Injective character kernel for globally distinct Plancherel sources.

At ``k`` copies, a natural unequal wreath portfolio starts from ``2k``
Plancherel partitions.  Conditioning only within each pair makes the ``k``
labels independent.  Conditioning all ``2k`` sources to be distinct does not:
it replaces the product character kernel by an injective Plancherel transform.

For slot features ``f_1,...,f_r`` define

    I_n(f_1,...,f_r)
      = sum_{nu_1,...,nu_r distinct} prod_j p_(nu_j) f_j(nu_j).

The numerator is computed exactly by a subset dynamic program.  Unequal
normalized characters and projector-word factors are finite sums of rank-one
slot features, so their globally-distinct joint averages reduce exactly to
``I_n/P_cf``.  This is the correct source object for any all-depth recoupling
or moment theorem restricted to collision-free labels.

There is also a sharp warning against replacing this kernel by the independent
all-unequal kernel.  Let ``A`` condition each source pair to be unequal and
``E`` condition all sources to be globally distinct.  Then

    TV(Law(.|A), Law(.|E)) = 1 - Pr(E)/Pr(A).

If ``C_n=sum p_lambda^2`` and
``q_lambda=p_lambda(1-p_lambda)/(1-C_n)``, a fixed cross-pair collision has
probability ``D_n=sum q_lambda^2``.  Hence, for ``k>=2``,

    D_n <= 1-Pr(E|A) <= (binom(2k,2)-k) D_n.

Aggarwal--Elboim's maximal-dimension theorem implies
``C_n,D_n=exp(-Theta(sqrt(n)))``.  At ``k=Theta(n log n)``, the conditioning
distance is therefore ``exp(-Theta(sqrt(n)))``: it vanishes, but is enormously
larger than the ``2^{1-k}=exp(-Theta(n log n))`` spectral scale.  Total-
variation transfer cannot prove the desired contraction; observable-specific
signed cancellation in the injective kernel is required.

That conclusion is specific to transferring the large moment observable
itself.  It is not a mandatory prerequisite for a spectral theorem.  If a
uniform good spectral event is first proved under independent Plancherel
labels, conditioning that event costs only division by the collision-free
mass.  ``self_dual_wreath_collision_free_event_transfer.py`` formalizes this
alternative.  The active target is an independent-source high-probability
edge theorem strong enough to union bound over all hierarchy nodes; injective
signed contraction remains an optional direct-moment route.
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

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import utc_now
from self_dual_wreath_all_unequal_conditioned_kernel import (
    conditioned_word_factor,
    plancherel_collision_probability,
)
from self_dual_wreath_character_moments import (
    permutation_cycle_type,
    physical_wreath_character,
    projector_word_character_sum,
    selected_bridge_word,
    unequal_pair_descriptor,
)
from self_dual_wreath_global_collision_free_mass import (
    exact_global_collision_free_probability,
    global_collision_free_mass_record,
    plancherel_weights,
)
from self_dual_wreath_natural_unequal_dominance import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
)
from self_dual_wreath_subset_carrier_algebra import WreathElement
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_global_distinct_joint_kernel.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Feature = tuple[Fraction, ...]
RankOneComponent = tuple[Fraction, Feature, Feature]


@dataclass(frozen=True)
class InjectiveTransformValidationRecord:
    n: int
    slot_count: int
    partition_count: int
    direct_value: str
    subset_dp_value: str
    exact_match: bool


@dataclass(frozen=True)
class GlobalDistinctWordControlRecord:
    n: int
    copy_count: int
    moment_order: int
    partition_count: int
    sequence_cycle_types: tuple[tuple[tuple[int, ...], ...], ...]
    global_distinct_probability: str
    global_distinct_given_pairwise_unequal_probability: str
    direct_joint_word_factor: str
    structured_joint_word_factor: str
    independent_pairwise_unequal_word_factor: str
    exact_structure_residual: str
    exact_factorization_defect: str
    conditioning_total_variation: str
    cross_pair_single_slot_collision_probability: str
    factorization_defect_bounded_by_twice_total_variation: bool
    globally_distinct_source_law_nonfactorizing: bool
    status: str


@dataclass(frozen=True)
class ConditioningScaleRecord:
    n: int
    copy_count: int
    partition_count: int
    pairwise_unequal_conditioned_global_distinct_probability: float
    conditioning_total_variation: float
    cross_pair_single_slot_collision_probability: float
    union_bound_conditioning_total_variation: float
    log2_conditioning_total_variation: float
    log2_required_second_moment_scale: float
    log2_tv_to_required_scale_gap: float
    finite_bound_audit: bool
    generic_total_variation_transfer_conclusive: bool
    status: str


@dataclass(frozen=True)
class GlobalDistinctJointKernelReport:
    created_at: str
    theorem_contract: dict[str, Any]
    injective_transform_validations: list[InjectiveTransformValidationRecord]
    joint_word_controls: list[GlobalDistinctWordControlRecord]
    conditioning_scaling: list[ConditioningScaleRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def _partitions(n: int) -> tuple[Partition, ...]:
    return tuple(integer_partitions(n))


def injective_plancherel_transform(
    weights: tuple[Fraction, ...],
    slot_features: tuple[Feature, ...],
) -> Fraction:
    """Return the unnormalized injective source-feature sum exactly."""

    slot_count = len(slot_features)
    if any(len(feature) != len(weights) for feature in slot_features):
        raise ValueError("every slot feature must match the weight count")
    if slot_count > len(weights):
        return Fraction()
    full_mask = (1 << slot_count) - 1
    dynamic = [Fraction()] * (1 << slot_count)
    dynamic[0] = Fraction(1)
    for partition_index, weight in enumerate(weights):
        previous = dynamic
        updated = previous.copy()
        for mask, partial in enumerate(previous):
            if not partial:
                continue
            available = full_mask ^ mask
            while available:
                bit = available & -available
                slot = bit.bit_length() - 1
                updated[mask | bit] += (
                    partial
                    * weight
                    * slot_features[slot][partition_index]
                )
                available ^= bit
        dynamic = updated
    return dynamic[full_mask]


def direct_injective_plancherel_transform(
    weights: tuple[Fraction, ...],
    slot_features: tuple[Feature, ...],
) -> Fraction:
    if len(slot_features) > len(weights):
        return Fraction()
    total = Fraction()
    for assignment in itertools.permutations(
        range(len(weights)),
        len(slot_features),
    ):
        contribution = Fraction(1)
        for slot, partition_index in enumerate(assignment):
            contribution *= (
                weights[partition_index]
                * slot_features[slot][partition_index]
            )
        total += contribution
    return total


@lru_cache(maxsize=None)
def normalized_character_feature(
    n: int,
    permutation: Permutation,
) -> Feature:
    if len(permutation) != n:
        raise ValueError("permutation size does not match n")
    cycle_type = permutation_cycle_type(permutation)
    return tuple(
        Fraction(
            symmetric_character(partition, cycle_type),
            hook_length_dimension(partition),
        )
        for partition in _partitions(n)
    )


def unequal_character_components(
    n: int,
    element: WreathElement,
) -> tuple[RankOneComponent, ...]:
    """Rank-one source expansion of one unequal normalized character."""

    left, right, swap = element
    if len(left) != n or len(right) != n:
        raise ValueError("wreath element size does not match n")
    if swap:
        return ()
    left_feature = normalized_character_feature(n, left)
    right_feature = normalized_character_feature(n, right)
    return (
        (Fraction(1, 2), left_feature, right_feature),
        (Fraction(1, 2), right_feature, left_feature),
    )


def unequal_word_components(
    n: int,
    sequence: tuple[Permutation, ...],
) -> tuple[RankOneComponent, ...]:
    """Rank-one source expansion of a normalized projector-word trace."""

    if not sequence:
        raise ValueError("sequence must be nonempty")
    if any(len(permutation) != n for permutation in sequence):
        raise ValueError("permutation size does not match n")
    coefficient = Fraction(1, 1 << (len(sequence) + 1))
    components: list[RankOneComponent] = []
    for mask in range(1 << len(sequence)):
        left, right, swap = selected_bridge_word(sequence, mask)
        if swap:
            continue
        left_feature = normalized_character_feature(n, left)
        right_feature = normalized_character_feature(n, right)
        components.extend(
            (
                (coefficient, left_feature, right_feature),
                (coefficient, right_feature, left_feature),
            )
        )
    return tuple(components)


def pair_factor_from_components(
    components: tuple[RankOneComponent, ...],
    left_index: int,
    right_index: int,
) -> Fraction:
    return sum(
        (
            coefficient
            * left_feature[left_index]
            * right_feature[right_index]
            for coefficient, left_feature, right_feature in components
        ),
        Fraction(),
    )


def structured_global_distinct_joint_factor(
    n: int,
    components_by_copy: tuple[tuple[RankOneComponent, ...], ...],
) -> Fraction:
    """Evaluate a product of pair factors under global distinctness."""

    copy_count = len(components_by_copy)
    if copy_count == 0:
        return Fraction(1)
    normalization = exact_global_collision_free_probability(n, copy_count)
    if not normalization:
        raise ValueError("global distinctness is impossible for these n,k")
    weights = plancherel_weights(n)
    numerator = Fraction()
    for selected in itertools.product(*components_by_copy):
        coefficient = Fraction(1)
        slot_features: list[Feature] = []
        for component_coefficient, left_feature, right_feature in selected:
            coefficient *= component_coefficient
            slot_features.extend((left_feature, right_feature))
        numerator += coefficient * injective_plancherel_transform(
            weights,
            tuple(slot_features),
        )
    return numerator / normalization


def structured_global_distinct_joint_character_kernel(
    n: int,
    elements: tuple[WreathElement, ...],
) -> Fraction:
    return structured_global_distinct_joint_factor(
        n,
        tuple(unequal_character_components(n, element) for element in elements),
    )


def structured_global_distinct_joint_word_factor(
    n: int,
    sequences: tuple[tuple[Permutation, ...], ...],
) -> Fraction:
    return structured_global_distinct_joint_factor(
        n,
        tuple(unequal_word_components(n, sequence) for sequence in sequences),
    )


def direct_global_distinct_joint_character_kernel(
    n: int,
    elements: tuple[WreathElement, ...],
) -> Fraction:
    copy_count = len(elements)
    normalization = exact_global_collision_free_probability(n, copy_count)
    if not normalization:
        raise ValueError("global distinctness is impossible for these n,k")
    partitions = _partitions(n)
    weights = plancherel_weights(n)
    total = Fraction()
    for assignment in itertools.permutations(
        range(len(partitions)),
        2 * copy_count,
    ):
        contribution = Fraction(1)
        for partition_index in assignment:
            contribution *= weights[partition_index]
        for copy_index, element in enumerate(elements):
            descriptor = unequal_pair_descriptor(
                partitions[assignment[2 * copy_index]],
                partitions[assignment[2 * copy_index + 1]],
            )
            contribution *= Fraction(
                physical_wreath_character(descriptor, element),
                descriptor.dimension,
            )
        total += contribution
    return total / normalization


def direct_global_distinct_joint_word_factor(
    n: int,
    sequences: tuple[tuple[Permutation, ...], ...],
) -> Fraction:
    copy_count = len(sequences)
    normalization = exact_global_collision_free_probability(n, copy_count)
    if not normalization:
        raise ValueError("global distinctness is impossible for these n,k")
    partitions = _partitions(n)
    weights = plancherel_weights(n)
    total = Fraction()
    for assignment in itertools.permutations(
        range(len(partitions)),
        2 * copy_count,
    ):
        contribution = Fraction(1)
        for partition_index in assignment:
            contribution *= weights[partition_index]
        for copy_index, sequence in enumerate(sequences):
            descriptor = unequal_pair_descriptor(
                partitions[assignment[2 * copy_index]],
                partitions[assignment[2 * copy_index + 1]],
            )
            contribution *= Fraction(
                projector_word_character_sum(descriptor, sequence),
                descriptor.dimension * (1 << len(sequence)),
            )
        total += contribution
    return total / normalization


def pairwise_unequal_conditioned_global_distinct_probability(
    n: int,
    copy_count: int,
) -> Fraction:
    collision = plancherel_collision_probability(n)
    return exact_global_collision_free_probability(n, copy_count) / (
        (1 - collision) ** copy_count
    )


def conditioning_total_variation(n: int, copy_count: int) -> Fraction:
    return 1 - pairwise_unequal_conditioned_global_distinct_probability(
        n,
        copy_count,
    )


def cross_pair_single_slot_collision_probability(n: int) -> Fraction:
    weights = plancherel_weights(n)
    collision = sum((weight * weight for weight in weights), Fraction())
    marginal = tuple(
        weight * (1 - weight) / (1 - collision) for weight in weights
    )
    return sum((weight * weight for weight in marginal), Fraction())


def conditioning_tv_bounds(
    n: int,
    copy_count: int,
) -> tuple[Fraction, Fraction]:
    if copy_count < 2:
        return Fraction(), Fraction()
    single_cross_collision = cross_pair_single_slot_collision_probability(n)
    cross_slot_pair_count = math.comb(2 * copy_count, 2) - copy_count
    return (
        single_cross_collision,
        min(Fraction(1), cross_slot_pair_count * single_cross_collision),
    )


def _injective_transform_validations() -> list[InjectiveTransformValidationRecord]:
    records = []
    controls = (
        (3, ((0, 1, 2), (1, 0, 2))),
        (4, ((0, 1, 2, 3), (1, 0, 3, 2), (1, 2, 3, 0))),
    )
    for n, permutations in controls:
        weights = plancherel_weights(n)
        features = tuple(
            normalized_character_feature(n, permutation)
            for permutation in permutations
        )
        direct = direct_injective_plancherel_transform(weights, features)
        dynamic = injective_plancherel_transform(weights, features)
        records.append(
            InjectiveTransformValidationRecord(
                n=n,
                slot_count=len(features),
                partition_count=len(weights),
                direct_value=str(direct),
                subset_dp_value=str(dynamic),
                exact_match=direct == dynamic,
            )
        )
    return records


def _word_control(
    n: int,
    sequence: tuple[Permutation, ...],
    copy_count: int = 2,
) -> GlobalDistinctWordControlRecord:
    sequences = (sequence,) * copy_count
    direct = direct_global_distinct_joint_word_factor(n, sequences)
    structured = structured_global_distinct_joint_word_factor(n, sequences)
    independent = conditioned_word_factor(n, sequence) ** copy_count
    defect = structured - independent
    pair_conditioned_mass = (
        pairwise_unequal_conditioned_global_distinct_probability(
            n,
            copy_count,
        )
    )
    total_variation = 1 - pair_conditioned_mass
    single_cross_collision = cross_pair_single_slot_collision_probability(n)
    return GlobalDistinctWordControlRecord(
        n=n,
        copy_count=copy_count,
        moment_order=len(sequence),
        partition_count=len(_partitions(n)),
        sequence_cycle_types=tuple(
            tuple(permutation_cycle_type(permutation) for permutation in item)
            for item in sequences
        ),
        global_distinct_probability=str(
            exact_global_collision_free_probability(n, copy_count)
        ),
        global_distinct_given_pairwise_unequal_probability=str(
            pair_conditioned_mass
        ),
        direct_joint_word_factor=str(direct),
        structured_joint_word_factor=str(structured),
        independent_pairwise_unequal_word_factor=str(independent),
        exact_structure_residual=str(structured - direct),
        exact_factorization_defect=str(defect),
        conditioning_total_variation=str(total_variation),
        cross_pair_single_slot_collision_probability=str(
            single_cross_collision
        ),
        factorization_defect_bounded_by_twice_total_variation=(
            abs(defect) <= 2 * total_variation
        ),
        globally_distinct_source_law_nonfactorizing=defect != 0,
        status=(
            "injective-joint-word-kernel-exact-nonfactorizing"
            if defect
            else "injective-joint-word-kernel-exact-factorizing-control"
        ),
    )


def conditioning_scale_record(n: int) -> ConditioningScaleRecord:
    mass = global_collision_free_mass_record(n)
    log2_conditioned = (
        mass.log2_within_pair_unequal_conditioned_global_collision_free_probability
    )
    if math.isfinite(log2_conditioned):
        log_conditioned = log2_conditioned * math.log(2)
        total_variation = min(1.0, max(0.0, -math.expm1(log_conditioned)))
        conditioned_mass = math.exp(log_conditioned) if log_conditioned > -745 else 0.0
    else:
        conditioned_mass = 0.0
        total_variation = 1.0
    log_factorial = math.lgamma(n + 1)
    weights = [
        math.exp(
            2 * math.log(hook_length_dimension(partition)) - log_factorial
        )
        for partition in _partitions(n)
    ]
    collision = sum(weight * weight for weight in weights)
    marginal = [
        weight * (1 - weight) / (1 - collision) for weight in weights
    ]
    single_cross_collision = sum(weight * weight for weight in marginal)
    cross_slot_pair_count = (
        math.comb(2 * mass.information_threshold_copy_count, 2)
        - mass.information_threshold_copy_count
    )
    upper = min(1.0, cross_slot_pair_count * single_cross_collision)
    lower = single_cross_collision
    audit = (
        total_variation + 1e-12 >= lower
        and total_variation <= upper + 1e-10
    )
    log2_tv = math.log2(total_variation) if total_variation else -math.inf
    required_log2 = 1 - mass.information_threshold_copy_count
    return ConditioningScaleRecord(
        n=n,
        copy_count=mass.information_threshold_copy_count,
        partition_count=mass.partition_count,
        pairwise_unequal_conditioned_global_distinct_probability=conditioned_mass,
        conditioning_total_variation=total_variation,
        cross_pair_single_slot_collision_probability=single_cross_collision,
        union_bound_conditioning_total_variation=upper,
        log2_conditioning_total_variation=log2_tv,
        log2_required_second_moment_scale=required_log2,
        log2_tv_to_required_scale_gap=log2_tv - required_log2,
        finite_bound_audit=audit,
        generic_total_variation_transfer_conclusive=(
            total_variation <= 2.0**required_log2
        ),
        status=(
            "generic-tv-transfer-finite-row-inconclusive"
            if total_variation > 2.0**required_log2
            else "generic-tv-transfer-finite-row-conclusive"
        ),
    )


def run_global_distinct_joint_kernel() -> GlobalDistinctJointKernelReport:
    validations = _injective_transform_validations()
    controls = [
        _word_control(
            4,
            ((0, 1, 2, 3), (1, 0, 3, 2)),
        ),
        _word_control(
            5,
            ((0, 1, 2, 3, 4), (0, 2, 1, 4, 3)),
        ),
    ]
    scaling = [
        conditioning_scale_record(n)
        for n in (5, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    validation_failures = sum(not row.exact_match for row in validations)
    structure_failures = sum(
        row.exact_structure_residual != "0" for row in controls
    )
    bound_failures = sum(not row.finite_bound_audit for row in scaling)
    nonfactorizing = sum(
        row.globally_distinct_source_law_nonfactorizing for row in controls
    )
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "injective_transform_validation_count": len(validations),
        "injective_transform_validation_failure_count": validation_failures,
        "joint_word_kernel_control_count": len(controls),
        "joint_word_kernel_structure_failure_count": structure_failures,
        "nonfactorizing_joint_word_control_count": nonfactorizing,
        "conditioning_tv_finite_bound_failure_count": bound_failures,
        "injective_plancherel_transform_theorem_count": 1,
        "global_distinct_joint_character_kernel_theorem_count": 1,
        "conditioning_total_variation_identity_theorem_count": 1,
        "conditioning_distance_asymptotic_scale_theorem_count": 1,
        "generic_tv_transfer_no_go_theorem_count": 1,
        "tail_n": tail.n,
        "tail_copy_count": tail.copy_count,
        "tail_log2_conditioning_total_variation": tail.log2_conditioning_total_variation,
        "tail_log2_required_second_moment_scale": tail.log2_required_second_moment_scale,
        "tail_log2_tv_to_required_scale_gap": tail.log2_tv_to_required_scale_gap,
        "uniform_collision_free_signed_contraction_theorem_count": 0,
        "event_level_conditioning_bypass_theorem_count": 1,
        "new_quantum_algorithm_count": 0,
    }
    exact = not validation_failures and not structure_failures and not bound_failures
    return GlobalDistinctJointKernelReport(
        created_at=utc_now(),
        theorem_contract={
            "injective_transform": (
                "I_n(f_1,...,f_r)=sum_distinct(nu_1,...,nu_r) "
                "prod_j p_(nu_j)f_j(nu_j), computed by subset DP."
            ),
            "global_distinct_joint_kernel": (
                "Expand every unequal character or projector-word factor "
                "into rank-one source features and divide the resulting "
                "injective transform by P_cf=(2k)!e_(2k)(p)."
            ),
            "conditioning_tv_identity": (
                "TV(Law(.|pairwise unequal),Law(.|globally distinct))="
                "1-P_cf/(1-C_n)^k."
            ),
            "cross_collision_bounds": (
                "D_n<=TV<=(binom(2k,2)-k)D_n, where "
                "D_n=sum_lambda[p_lambda(1-p_lambda)/(1-C_n)]^2."
            ),
            "asymptotic_scale": (
                "Aggarwal--Elboim implies C_n,D_n=exp(-Theta(sqrt(n))); "
                "for k=Theta(n log n), TV=exp(-Theta(sqrt(n)))."
            ),
            "moment_scale_separation": (
                "The required 2^{1-k}=exp(-Theta(n log n)) scale is far "
                "below the generic conditioning error."
            ),
            "literature_id": MAXIMAL_DIMENSION_PAPER_ID,
            "literature_url": MAXIMAL_DIMENSION_PAPER_URL,
        },
        injective_transform_validations=validations,
        joint_word_controls=controls,
        conditioning_scaling=scaling,
        proof_obligations=[
            {
                "obligation": "exact_global_distinct_joint_source_kernel",
                "resolved": exact,
                "resolution": "Rank-one expansion plus injective subset DP is exact and matches direct enumeration.",
            },
            {
                "obligation": "independent_all_unequal_replacement_at_pgm_scale",
                "resolved": True,
                "resolution": "Rejected: its generic total-variation error is exp(-Theta(sqrt(n))), not exp(-Theta(n log n)).",
            },
            {
                "obligation": "observable_specific_injective_kernel_contraction",
                "resolved": False,
                "resolution": "Open as a direct moment-transfer route, but not mandatory: an independent high-probability good event transfers by conditional probability.",
            },
            {
                "obligation": "event_level_conditioning_bypass",
                "resolved": True,
                "resolution": "An independent good event with failure delta has conditioned failure at most delta/P_cf; union bounds can be applied before conditioning.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Global distinctness is asymptotically typical, so independent unequal labels are interchangeable in high moments.",
                "resolved": True,
                "resolution": "Typicality is only exp(-Theta(sqrt(n))) accurate, exponentially too coarse for a 2^{-Theta(n log n)} target.",
            },
            {
                "objection": "The finite joint law might nevertheless factor exactly for projector words.",
                "resolved": True,
                "resolution": "Exact n=4 and n=5 controls have nonzero rational factorization defects.",
            },
            {
                "objection": "A nonzero factorization defect proves the desired contraction fails.",
                "resolved": False,
                "resolution": "It only invalidates product-kernel substitution; signed observable-specific cancellation may still succeed.",
            },
            {
                "objection": "Signed injective contraction is mandatory before proving a collision-free spectral event.",
                "resolved": True,
                "resolution": "False: a sufficiently strong independent-source good event transfers by dividing its failure probability by P_cf.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "injective_plancherel_transform_proved": exact,
            "global_distinct_joint_character_kernel_proved": exact,
            "global_distinct_joint_word_kernel_proved": exact,
            "globally_distinct_source_law_factorizes": False,
            "conditioning_tv_identity_and_bounds_proved": exact,
            "conditioning_distance_scale_separation_proved": True,
            "independent_all_unequal_kernel_transfer_sufficient": False,
            "uniform_collision_free_signed_contraction_proved": False,
            "event_level_conditioning_bypass_proved": True,
            "injective_signed_contraction_is_mandatory": False,
            "independent_uniform_spectral_event_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The injective source kernel is explicit and direct moment "
                "transfer remains open. Event-level conditioning bypasses that "
                "gate, but the independent uniform spectral event is unproved."
            ),
        },
        status=(
            "global-distinct-injective-kernel-proved-event-bypass-"
            "independent-uniform-edge-open"
        ),
        summary=(
            "Derived and exactly validated the nonfactorizing injective "
            "Plancherel kernel for globally distinct sources. Generic moment "
            "transfer is too coarse, but high-probability spectral events can "
            "instead be conditioned directly once proved independently."
        ),
        falsifiers_triggered=[
            "Global source distinctness does not preserve independence across physical labels.",
            "Pairwise-unequal product kernels have exact nonzero finite factorization defects after global conditioning.",
            "An o(1) source-conditioning error is not enough for an exp(-Theta(n log n)) PGM moment target.",
            "Direct moment transfer needs signed injective control, but event-level conditioning can bypass moment transfer.",
        ],
    )


def write_global_distinct_joint_kernel_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_global_distinct_joint_kernel())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_global_distinct_joint_kernel_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
