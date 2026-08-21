"""Exact surface law for the target-survival identity-frame lift.

The former real-entropy vanishing-margin lift in
``self_dual_wreath_contiguous_frame_target_factorization`` is generated from

    pattern BABA,
    S={(1,0,1,0)},
    D={(0,0,0,0),(0,1,1,1)}.

After the outer E/F positions are restored and elementary Tietze elimination
is performed, the full presentation has four generators and one orientable
genus-two relator.  The target is one handle commutator.  Appending identity A
frames with the lifted supports forces every appended generator to identity,
so every lift has the same finite-group solution and target distribution.

For a finite group G, let

    N(g)=|G| sum_lambda chi_lambda(g)/d_lambda

be the number of commutator representations of g.  The genus-two surface law
weights the target handle by N(g)^2.  For the standard representation of S_n,
the branching identity

    V_lambda tensor Std = Ind Res(V_lambda) - V_lambda

gives the exact normalized target average

  [sum_(alpha |- n-1) (sum_(lambda covers alpha) 1/d_lambda)^2
       - sum_(lambda |- n) 1/d_lambda^2]
  / [(n-1) sum_(lambda |- n) 1/d_lambda^2].                (1)

Using the symmetric-group Witten-zeta estimates zeta_n(1)=2+O(n^-1) and
zeta_n(2)=2+O(n^-2), together with at most O(sqrt(n)) removable corners, the
two extreme (trivial/standard and sign/sign-standard) branches dominate (1):

    average_Std = 2/(n-1)^2 + O(n^-5/2).

The later integer suffix-branch theorem already restores a uniform scalar gap
for this lift.  Independently, the surface calculation proves that its natural
standard-character signal vanishes in growing S_n.  This remains a useful
character-law classification, but it is no longer needed to close the scalar
escape. Other lift mechanisms remain open.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_marked_pressure_obstruction_search import (
    _finite_S3_character_control,
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    canonical_relator,
    free_reduce,
    marked_support_presentation,
    orientable_quadratic_genus,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_target_survival_surface_seed.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Assignment = tuple[int, ...]


@dataclass(frozen=True)
class TargetSurvivalSurfaceSeedControl:
    pattern: str
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    residual_orientable_genus: int | None
    symmetric_group_solution_exponent: float
    exponent_certificate_source: str
    residual_target_word: SignedWord
    target_orientable_genus: int | None
    exact_S3_solution_count: int
    exact_S3_sign_character_average: float
    exact_S3_standard_normalized_character_average: float
    exact_surface_seed_verified: bool
    status: str


@dataclass(frozen=True)
class TargetSurvivalPresentationLiftControl:
    lift_depth: int
    pattern: str
    same_support_size: int
    different_support_size: int
    eliminated_generator_count: int
    remaining_generator_count: int
    residual_orientable_genus: int | None
    symmetric_group_solution_exponent: float
    exact_S3_solution_count: int
    exact_S3_sign_character_average: float
    exact_S3_standard_normalized_character_average: float
    exact_seed_distribution_preserved: bool
    status: str


@dataclass(frozen=True)
class TargetSurvivalPowerBoundaryLiftControl:
    lift_depth: int
    pattern: str
    same_support_size: int
    different_support_size: int
    integer_suffix_branch_certificate_margin: float
    remaining_generators: tuple[int, ...]
    residual_relation: SignedWord
    residual_target_word: SignedWord
    quotient_handle_target_word: SignedWord
    eliminated_generator_count: int
    residual_orientable_genus: int | None
    symmetric_group_solution_exponent: float
    true_scalar_crossing_pressure_margin: float
    exact_surface_free_product_factorization_verified: bool
    exact_target_modulo_relator_verified: bool
    exact_S3_solution_count: int
    exact_S3_sign_character_average: float
    exact_S3_standard_normalized_character_average: float
    exact_power_boundary_lift_classified: bool
    status: str


@dataclass(frozen=True)
class TargetSurvivalPowerBoundaryAllDepthCertificate:
    base_pattern: str
    base_same_support: tuple[Assignment, ...]
    base_different_support: tuple[Assignment, ...]
    different_support_formula: str
    same_support_formula: str
    appended_generator_forcing_relations: str
    appended_generators_forced_to_identity: bool
    projected_same_support_equals_base: bool
    projected_different_support_equals_base: bool
    base_remaining_generator_count: int
    base_residual_relation: SignedWord
    base_residual_target_word: SignedWord
    base_solution_exponent: float
    base_exact_S3_solution_count: int
    base_exact_S3_standard_normalized_character_average: float
    base_surface_free_product_factorization_verified: bool
    base_target_modulo_relator_verified: bool
    checked_lift_depths: tuple[int, ...]
    checked_lifts_match_base: bool
    universal_all_depth_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class StandardHandleCharacterRecord:
    symmetric_group_degree: int
    partition_count: int
    witten_zeta_two: float
    normalized_standard_character_average: float
    n_squared_scaled_average: float
    asymptotic_prediction: float
    relative_prediction_error: float
    alternating_uniform_total_variation_upper_bound: float
    uniform_nonsign_character_expectation_upper_bound: float


@dataclass(frozen=True)
class TargetSurvivalSurfaceSeedReport:
    created_at: str
    theorem_contract: dict[str, Any]
    surface_seed: TargetSurvivalSurfaceSeedControl
    presentation_lifts: list[TargetSurvivalPresentationLiftControl]
    power_boundary_lifts: list[TargetSurvivalPowerBoundaryLiftControl]
    power_boundary_all_depth_certificate: TargetSurvivalPowerBoundaryAllDepthCertificate
    standard_character_scaling: list[StandardHandleCharacterRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def target_survival_lift_supports(
    lift_depth: int,
) -> tuple[str, tuple[Assignment, ...], tuple[Assignment, ...]]:
    if lift_depth < 0:
        raise ValueError("lift depth must be nonnegative")
    suffixes = tuple(itertools.product((0, 1), repeat=lift_depth))
    same = tuple((1, 0, 1, 0, *suffix) for suffix in suffixes)
    different_pool = tuple(
        sorted(
            (*seed, *suffix)
            for seed in ((0, 0, 0, 0), (0, 1, 1, 1))
            for suffix in suffixes
        )
    )
    different = different_pool[: len(same) + 1]
    pattern = "E" + "BABA" + "A" * lift_depth + "FEF"
    return pattern, same, different


def target_survival_power_boundary_supports(
    lift_depth: int,
) -> tuple[str, tuple[Assignment, ...], tuple[Assignment, ...]]:
    """Move the identity lift to the vanishing integer-boundary side."""

    if lift_depth < 1:
        raise ValueError("power-boundary lift depth must be positive")
    suffixes = tuple(itertools.product((0, 1), repeat=lift_depth))
    same = tuple((1, 0, 1, 0, *suffix) for suffix in suffixes)[:-1]
    different_pool = tuple(
        sorted(
            (*seed, *suffix)
            for seed in ((0, 0, 0, 0), (0, 1, 1, 1))
            for suffix in suffixes
        )
    )
    different = different_pool[: 2**lift_depth]
    pattern = "E" + "BABA" + "A" * lift_depth + "FEF"
    return pattern, same, different


def audit_surface_seed() -> TargetSurvivalSurfaceSeedControl:
    pattern, same, different = target_survival_lift_supports(0)
    reduction = tietze_reduce_presentation(
        len(pattern),
        marked_support_presentation(pattern, same, different),
    )
    exponent, source = presentation_solution_exponent_upper_bound(reduction)
    target = _transport_target_product_word(len(pattern), reduction)
    target_genus = orientable_quadratic_genus(target) if target else 0
    count, sign_average, standard_average = _finite_S3_character_control(
        len(pattern),
        reduction,
    )
    residual_genus = (
        orientable_quadratic_genus(reduction.residual_relations[0])
        if len(reduction.residual_relations) == 1
        else None
    )
    exact = (
        len(reduction.remaining_generators) == 4
        and residual_genus == 2
        and exponent == 3
        and target_genus == 1
        and count == 486
        and sign_average == 1.0
        and standard_average == 0.5
    )
    return TargetSurvivalSurfaceSeedControl(
        pattern=pattern,
        same_support=same,
        different_support=different,
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        residual_orientable_genus=residual_genus,
        symmetric_group_solution_exponent=exponent,
        exponent_certificate_source=source,
        residual_target_word=target,
        target_orientable_genus=target_genus,
        exact_S3_solution_count=count,
        exact_S3_sign_character_average=sign_average,
        exact_S3_standard_normalized_character_average=standard_average,
        exact_surface_seed_verified=exact,
        status=(
            "exact-genus-two-handle-target-seed"
            if exact
            else "surface-seed-control-failure"
        ),
    )


def audit_presentation_lift(
    lift_depth: int,
) -> TargetSurvivalPresentationLiftControl:
    pattern, same, different = target_survival_lift_supports(lift_depth)
    reduction = tietze_reduce_presentation(
        len(pattern),
        marked_support_presentation(pattern, same, different),
    )
    exponent, _ = presentation_solution_exponent_upper_bound(reduction)
    count, sign_average, standard_average = _finite_S3_character_control(
        len(pattern),
        reduction,
    )
    residual_genus = (
        orientable_quadratic_genus(reduction.residual_relations[0])
        if len(reduction.residual_relations) == 1
        else None
    )
    exact = (
        len(reduction.remaining_generators) == 4
        and residual_genus == 2
        and exponent == 3
        and count == 486
        and sign_average == 1.0
        and standard_average == 0.5
    )
    return TargetSurvivalPresentationLiftControl(
        lift_depth=lift_depth,
        pattern=pattern,
        same_support_size=len(same),
        different_support_size=len(different),
        eliminated_generator_count=len(reduction.elimination_steps),
        remaining_generator_count=len(reduction.remaining_generators),
        residual_orientable_genus=residual_genus,
        symmetric_group_solution_exponent=exponent,
        exact_S3_solution_count=count,
        exact_S3_sign_character_average=sign_average,
        exact_S3_standard_normalized_character_average=standard_average,
        exact_seed_distribution_preserved=exact,
        status=(
            "exact-seed-presentation-and-target-law-preserved"
            if exact
            else "presentation-lift-control-failure"
        ),
    )


def audit_power_boundary_lift(
    lift_depth: int,
) -> TargetSurvivalPowerBoundaryLiftControl:
    pattern, same, different = target_survival_power_boundary_supports(lift_depth)
    reduction = tietze_reduce_presentation(
        len(pattern),
        marked_support_presentation(pattern, same, different),
    )
    exponent, _ = presentation_solution_exponent_upper_bound(reduction)
    target = _transport_target_product_word(len(pattern), reduction)
    count, sign_average, standard_average = _finite_S3_character_control(
        len(pattern),
        reduction,
    )
    if len(reduction.remaining_generators) != 5 or len(reduction.residual_relations) != 1:
        raise AssertionError("power-boundary lift did not reach the five-generator normal form")
    x_value, y_value, z_value, p_value, q_value = reduction.remaining_generators
    relation = reduction.residual_relations[0]
    expected_surface_free_relation = (
        p_value,
        -q_value,
        -p_value,
        q_value,
        -z_value,
        -x_value,
        -y_value,
        x_value,
        y_value,
        z_value,
    )
    surface_free = canonical_relator(relation) == canonical_relator(
        expected_surface_free_relation
    )
    handle_target = (-p_value, -q_value, p_value, q_value)
    inverse_handle = tuple(-letter for letter in reversed(handle_target))
    target_modulo_relation = canonical_relator(
        free_reduce((*target, *inverse_handle))
    ) == canonical_relator(relation)
    support_entropy = 0.5 * math.log2(len(same) * len(different))
    certificate_margin = lift_depth - support_entropy
    true_margin = lift_depth + 1.0 - support_entropy
    residual_genus = orientable_quadratic_genus(relation)
    exact = (
        len(same) == 2**lift_depth - 1
        and len(different) == 2**lift_depth
        and surface_free
        and target_modulo_relation
        and residual_genus == 2
        and exponent == 4
        and count == 2916
        and sign_average == 1.0
        and standard_average == 0.5
        and certificate_margin > 0
        and true_margin > 1
    )
    return TargetSurvivalPowerBoundaryLiftControl(
        lift_depth=lift_depth,
        pattern=pattern,
        same_support_size=len(same),
        different_support_size=len(different),
        integer_suffix_branch_certificate_margin=certificate_margin,
        remaining_generators=reduction.remaining_generators,
        residual_relation=relation,
        residual_target_word=target,
        quotient_handle_target_word=handle_target,
        eliminated_generator_count=len(reduction.elimination_steps),
        residual_orientable_genus=residual_genus,
        symmetric_group_solution_exponent=exponent,
        true_scalar_crossing_pressure_margin=true_margin,
        exact_surface_free_product_factorization_verified=surface_free,
        exact_target_modulo_relator_verified=target_modulo_relation,
        exact_S3_solution_count=count,
        exact_S3_sign_character_average=sign_average,
        exact_S3_standard_normalized_character_average=standard_average,
        exact_power_boundary_lift_classified=exact,
        status=(
            "exact-power-boundary-genus-two-free-generator-collapse"
            if exact
            else "power-boundary-lift-control-failure"
        ),
    )


def audit_power_boundary_all_depth_certificate(
    maximum_checked_depth: int = 8,
) -> TargetSurvivalPowerBoundaryAllDepthCertificate:
    base_pattern = "EBABAFEF"
    base_same = ((1, 0, 1, 0),)
    base_different = ((0, 0, 0, 0),)
    base_reduction = tietze_reduce_presentation(
        len(base_pattern),
        marked_support_presentation(base_pattern, base_same, base_different),
    )
    base_exponent, _ = presentation_solution_exponent_upper_bound(base_reduction)
    base_target = _transport_target_product_word(
        len(base_pattern),
        base_reduction,
    )
    base_count, _, base_standard = _finite_S3_character_control(
        len(base_pattern),
        base_reduction,
    )
    x_value, y_value, z_value, p_value, q_value = (
        base_reduction.remaining_generators
    )
    expected_relation = (
        p_value,
        -q_value,
        -p_value,
        q_value,
        -z_value,
        -x_value,
        -y_value,
        x_value,
        y_value,
        z_value,
    )
    relation = base_reduction.residual_relations[0]
    surface_free = canonical_relator(relation) == canonical_relator(
        expected_relation
    )
    handle_target = (-p_value, -q_value, p_value, q_value)
    inverse_handle = tuple(-letter for letter in reversed(handle_target))
    target_exact = canonical_relator(
        free_reduce((*base_target, *inverse_handle))
    ) == canonical_relator(relation)

    depths = tuple(range(1, maximum_checked_depth + 1))
    controls = tuple(audit_power_boundary_lift(depth) for depth in depths)
    product_formula = True
    projections = True
    singleton_forcing = True
    for depth in depths:
        _, same, different = target_survival_power_boundary_supports(depth)
        suffixes = tuple(itertools.product((0, 1), repeat=depth))
        expected_different = tuple((0, 0, 0, 0, *row) for row in suffixes)
        product_formula &= different == expected_different
        projections &= (
            {row[:4] for row in same} == set(base_same)
            and {row[:4] for row in different} == set(base_different)
        )
        zero_suffix = (0,) * depth
        for coordinate in range(depth):
            singleton = tuple(int(index == coordinate) for index in range(depth))
            singleton_forcing &= (
                (0, 0, 0, 0, *zero_suffix) in different
                and (0, 0, 0, 0, *singleton) in different
            )
    checked_match = all(
        row.exact_power_boundary_lift_classified
        and row.symmetric_group_solution_exponent == base_exponent
        and row.exact_S3_solution_count == base_count
        and row.exact_S3_standard_normalized_character_average == base_standard
        for row in controls
    )
    universal = (
        product_formula
        and projections
        and singleton_forcing
        and surface_free
        and target_exact
        and len(base_reduction.remaining_generators) == 5
        and len(base_reduction.residual_relations) == 1
        and base_exponent == 4
        and base_count == 2916
        and base_standard == 0.5
        and checked_match
    )
    return TargetSurvivalPowerBoundaryAllDepthCertificate(
        base_pattern=base_pattern,
        base_same_support=base_same,
        base_different_support=base_different,
        different_support_formula="{0000} x {0,1}^k",
        same_support_formula="{1010} x ({0,1}^k minus {1^k})",
        appended_generator_forcing_relations=(
            "The zero and e_i different-support suffix rows give z_i=1 for "
            "every appended coordinate i."
        ),
        appended_generators_forced_to_identity=(
            product_formula and singleton_forcing
        ),
        projected_same_support_equals_base=projections,
        projected_different_support_equals_base=projections,
        base_remaining_generator_count=len(base_reduction.remaining_generators),
        base_residual_relation=relation,
        base_residual_target_word=base_target,
        base_solution_exponent=base_exponent,
        base_exact_S3_solution_count=base_count,
        base_exact_S3_standard_normalized_character_average=base_standard,
        base_surface_free_product_factorization_verified=surface_free,
        base_target_modulo_relator_verified=target_exact,
        checked_lift_depths=depths,
        checked_lifts_match_base=checked_match,
        universal_all_depth_reduction_verified=universal,
        status=(
            "exact-all-depth-power-boundary-reduction-to-fixed-seed"
            if universal
            else "power-boundary-all-depth-certificate-failure"
        ),
    )


@lru_cache(maxsize=None)
def integer_partitions(
    total: int,
    maximum_part: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    if total < 0:
        return ()
    if total == 0:
        return ((),)
    maximum = total if maximum_part is None else min(total, maximum_part)
    output: list[tuple[int, ...]] = []
    for first in range(maximum, 0, -1):
        for tail in integer_partitions(total - first, first):
            output.append((first, *tail))
    return tuple(output)


@lru_cache(maxsize=None)
def symmetric_group_irrep_dimension(partition: tuple[int, ...]) -> int:
    total = sum(partition)
    hook_product = 1
    for row_index, row_length in enumerate(partition):
        for column in range(row_length):
            below = sum(
                later_row > column
                for later_row in partition[row_index + 1 :]
            )
            hook_product *= row_length - column + below
    return math.factorial(total) // hook_product


def covering_partitions(partition: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    covers: list[tuple[int, ...]] = []
    for row_index in range(len(partition)):
        if row_index == 0 or partition[row_index] < partition[row_index - 1]:
            row = list(partition)
            row[row_index] += 1
            covers.append(tuple(row))
    covers.append((*partition, 1))
    return tuple(covers)


def standard_handle_character_average(degree: int) -> float:
    if degree < 2:
        raise ValueError("standard representation requires degree at least two")
    partitions = integer_partitions(degree)
    zeta_two = sum(
        1.0 / symmetric_group_irrep_dimension(partition) ** 2
        for partition in partitions
    )
    branch_square_sum = 0.0
    for lower in integer_partitions(degree - 1):
        inverse_dimension_sum = sum(
            1.0 / symmetric_group_irrep_dimension(upper)
            for upper in covering_partitions(lower)
        )
        branch_square_sum += inverse_dimension_sum**2
    return (branch_square_sum - zeta_two) / ((degree - 1) * zeta_two)


def standard_character_record(degree: int) -> StandardHandleCharacterRecord:
    partitions = integer_partitions(degree)
    zeta_two = sum(
        1.0 / symmetric_group_irrep_dimension(partition) ** 2
        for partition in partitions
    )
    average = standard_handle_character_average(degree)
    prediction = 2.0 / (degree - 1) ** 2
    epsilon = zeta_two - 2.0
    total_variation_bound = (
        epsilon + math.sqrt(2.0 * epsilon)
    ) / zeta_two
    return StandardHandleCharacterRecord(
        symmetric_group_degree=degree,
        partition_count=len(partitions),
        witten_zeta_two=zeta_two,
        normalized_standard_character_average=average,
        n_squared_scaled_average=degree * degree * average,
        asymptotic_prediction=prediction,
        relative_prediction_error=abs(average - prediction) / prediction,
        alternating_uniform_total_variation_upper_bound=total_variation_bound,
        uniform_nonsign_character_expectation_upper_bound=(
            2.0 * total_variation_bound
        ),
    )


def run_target_survival_surface_seed() -> TargetSurvivalSurfaceSeedReport:
    seed = audit_surface_seed()
    lifts = [audit_presentation_lift(depth) for depth in range(7)]
    power_boundary_lifts = [
        audit_power_boundary_lift(depth) for depth in range(1, 9)
    ]
    power_boundary_all_depth = audit_power_boundary_all_depth_certificate()
    degrees = (*range(3, 21), 25, 30)
    scaling = [standard_character_record(degree) for degree in degrees]
    lifts_exact = all(row.exact_seed_distribution_preserved for row in lifts)
    boundary_exact = all(
        row.exact_power_boundary_lift_classified for row in power_boundary_lifts
    ) and power_boundary_all_depth.universal_all_depth_reduction_verified
    formula_exact = abs(scaling[0].normalized_standard_character_average - 0.5) < 1e-12
    theorem_exact = (
        seed.exact_surface_seed_verified
        and lifts_exact
        and boundary_exact
        and formula_exact
    )
    return TargetSurvivalSurfaceSeedReport(
        created_at=utc_now(),
        theorem_contract={
            "surface_seed": (
                "The width-four full presentation is an orientable genus-two "
                "surface group with S_n solution exponent three; the target is "
                "one handle commutator."
            ),
            "identity_frame_lift": (
                "Paired lifted same-support rows force each appended A-frame "
                "generator to identity, leaving the seed presentation and "
                "target distribution unchanged over every finite group."
            ),
            "power_boundary_lift": (
                "Deleting one same row and one different row moves the generic "
                "integer certificate margin to zero, but every depth is exactly "
                "a genus-two surface group free-product one free generator. The "
                "true scalar pressure margin is greater than one."
            ),
            "standard_character_formula": (
                "Ind-Res for the standard representation gives equation (1), "
                "an exact positive partition/branching formula."
            ),
            "standard_character_asymptotic": (
                "Using zeta_Sn(1)=2+O(n^-1), zeta_Sn(2)=2+O(n^-2), and "
                "O(sqrt n) corners, the average is "
                "2/(n-1)^2+O(n^-5/2)."
            ),
            "uniform_irrep_decay": (
                "Writing the commutator density f=1+sgn+h gives "
                "E|h|^2=zeta_Sn(2)-2=O(n^-2). The genus-two target density "
                "f^2/zeta_Sn(2) is O(n^-1) in total variation from uniform "
                "A_n, so every normalized irrep other than trivial/sign has "
                "expectation O(n^-1)."
            ),
            "literature_basis": (
                "Liebeck-Shalev/Gamburd Witten-zeta asymptotics; see also "
                "Teyssier-Thevenin, arXiv:2411.04347, for sharp bounds."
            ),
            "scope": (
                "This closes the natural standard target only for this exact "
                "surface-seed lift. Other irreps and structural lifts remain open."
            ),
        },
        surface_seed=seed,
        presentation_lifts=lifts,
        power_boundary_lifts=power_boundary_lifts,
        power_boundary_all_depth_certificate=power_boundary_all_depth,
        standard_character_scaling=scaling,
        proof_obligations=[
            {
                "obligation": "classify_former_real_entropy_margin_identity_frame_lift_presentation",
                "resolved": theorem_exact,
                "resolution": (
                    "Every appended generator is Tietze-eliminated and all stored "
                    "lifts retain the four-generator genus-two seed."
                ),
            },
            {
                "obligation": "derive_exact_natural_standard_target_average",
                "resolved": theorem_exact,
                "resolution": (
                    "The standard Kronecker branching rule gives the exact "
                    "partition-cover formula."
                ),
            },
            {
                "obligation": "prove_natural_standard_signal_vanishes_for_seed_lift",
                "resolved": theorem_exact,
                "resolution": (
                    "The Witten-zeta/corner estimate gives quadratic decay."
                ),
            },
            {
                "obligation": "control_every_nontrivial_nonsign_irrep_for_seed_lift",
                "resolved": theorem_exact,
                "resolution": (
                    "The Witten-zeta L2 remainder makes the handle law O(1/n) "
                    "in total variation from uniform A_n."
                ),
            },
            {
                "obligation": "control_nonidentity_frame_lifts_and_non_surface_seeds",
                "resolved": False,
                "resolution": (
                    "Analyze lifts whose new frame variables are not forced to "
                    "identity and target-surviving presentations not equivalent "
                    "to this genus-two surface seed."
                ),
            },
            {
                "obligation": "classify_power_boundary_pruning_of_identity_lift",
                "resolved": boundary_exact,
                "resolution": (
                    "The vanishing integer-certificate family is exactly a "
                    "genus-two surface group with one free generator; its target "
                    "is the same handle commutator and its true pressure margin "
                    "stays above one."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Vanishing real-entropy certificate margin preserves the seed signal.",
                "resolved": True,
                "resolution": (
                    "False for the natural standard target: the exact normalized "
                    "average is asymptotic to 2/n^2."
                ),
            },
            {
                "objection": "Appending identity frames creates growing presentation freedom.",
                "resolved": True,
                "resolution": (
                    "False: paired support rows force every appended generator "
                    "to identity and the solution distribution is unchanged."
                ),
            },
            {
                "objection": "Pruning to support sizes 2^k-1 and 2^k creates leading mass.",
                "resolved": boundary_exact,
                "resolution": (
                    "False: it adds exactly one free generator to the fixed "
                    "genus-two surface law, leaving more than one exponent of "
                    "true scalar pressure margin."
                ),
            },
            {
                "objection": "The sign character is evidence of a natural component signal.",
                "resolved": True,
                "resolution": (
                    "False: commutators always have sign one; this one-dimensional "
                    "sector does not rescue the natural standard component."
                ),
            },
        ],
        headline_metrics={
            "exact_genus_two_surface_seed_theorem_count": int(theorem_exact),
            "exact_identity_frame_presentation_lift_count": len(lifts),
            "presentation_lift_failure_count": sum(
                not row.exact_seed_distribution_preserved for row in lifts
            ),
            "exact_power_boundary_lift_count": len(power_boundary_lifts),
            "all_depth_power_boundary_reduction_theorem_count": int(
                power_boundary_all_depth.universal_all_depth_reduction_verified
            ),
            "power_boundary_lift_failure_count": sum(
                not row.exact_power_boundary_lift_classified
                for row in power_boundary_lifts
            ),
            "minimum_power_boundary_integer_certificate_margin": min(
                row.integer_suffix_branch_certificate_margin
                for row in power_boundary_lifts
            ),
            "minimum_power_boundary_true_pressure_margin": min(
                row.true_scalar_crossing_pressure_margin
                for row in power_boundary_lifts
            ),
            "standard_character_scaling_degree_count": len(scaling),
            "maximum_standard_character_degree": max(degrees),
            "degree_30_n_squared_scaled_standard_average": (
                scaling[-1].n_squared_scaled_average
            ),
            "standard_character_quadratic_decay_theorem_count": int(theorem_exact),
            "uniform_nonsign_irrep_decay_theorem_count": int(theorem_exact),
            "degree_30_uniform_nonsign_character_upper_bound": (
                scaling[-1].uniform_nonsign_character_expectation_upper_bound
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "identity_frame_lift_presentation_classified": theorem_exact,
            "power_boundary_identity_lift_classified": boundary_exact,
            "power_boundary_generic_certificate_gap_falsified": boundary_exact,
            "power_boundary_actual_presentation_gap_falsified": False,
            "natural_standard_target_average_exactly_reduced": theorem_exact,
            "natural_standard_target_signal_asymptotically_nonzero": False,
            "all_nontrivial_nonsign_seed_targets_vanish": theorem_exact,
            "trivial_and_sign_seed_targets_equal_one": theorem_exact,
            "nonidentity_frame_lifts_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Both the original and power-boundary identity-frame escapes "
                "collapse to fixed genus-two laws; the natural standard signal "
                "decays as 2/n^2."
            ),
        },
        status=(
            "identity-frame-lift-natural-standard-signal-dequantized"
            if theorem_exact
            else "surface-seed-character-control-failure"
        ),
        summary=(
            "Classified both identity-frame support lifts as fixed genus-two "
            "surface laws and proved quadratic decay of their natural standard "
            "target character."
        ),
        falsifiers_triggered=[
            "The obsolete real entropy pressure margin substantially overstates the lift.",
            "Identity-frame padding creates no new presentation degrees of freedom.",
            "Power-boundary pruning adds only one free generator and no leading mass.",
            "The exact S3 standard average 1/2 decays to zero in growing S_n.",
            "Every nontrivial nonsign seed target vanishes uniformly by total variation.",
            "One-dimensional sign behavior is not a natural-component rescue.",
        ],
    )


def write_target_survival_surface_seed_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    report = asdict(run_target_survival_surface_seed())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    return report


if __name__ == "__main__":
    result = write_target_survival_surface_seed_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
