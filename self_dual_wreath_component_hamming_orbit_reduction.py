"""Annealed Hamming-orbit reduction of final-root component commutator M4.

Exact orientation translation covariance is false inside a generic unequal-
source block.  The independent-Plancherel law nevertheless has an exact
relabeling covariance that is sufficient for the scalar component moment.

For ``K`` ordered source pairs, swapping the two irreps in pairs selected by
``a in F_2^K`` and applying the corresponding tensor-factor flips gives

    S_a E_e(Lambda) S_a^* = E_(e xor a)(Lambda^a).        (1)

Permuting source pairs gives the analogous coordinate-permutation identity.
Functional calculus, child support intersection, Green/ridge normalization,
and commutators all preserve (1).  The iid Plancherel law is invariant under
both relabelings.  So is the event that all ``2K`` source partitions are
distinct.

At the final root, one child is a cube of size

    q = 2^m,       m=K-1.

For either the independent or globally-distinct source law, define

    c_w = E[ Tr([H_e,H_f]^*[H_e,H_f]) / D_phys ]

for any child pair at Hamming distance ``w``.  Equivariance makes ``c_w``
well defined.  Counting unordered cube pairs gives the exact identity

    M4 = (q/2) sum_(w=1)^m binom(m,w) c_w                 (2)
       = (1/2) E_(W~Bin(m,1/2)) [g_W],

where ``g_w=q^2 c_w`` and ``g_0=0``.  Thus the exponentially large leaf-pair
sum is neither a ``q^2`` computational target nor an arbitrary pair average.
It is one binomially weighted profile with only ``m`` Hamming strata.

In particular, if a set of Hamming weights has binomial mass at least ``rho``
and ``q^2 c_w >= kappa`` on that set, then

    M4 >= rho kappa / 2.                                  (3)

A constant or inverse-polynomial lower bound on the rescaled pair gap at
typical distance therefore proves the same scale of independent M4.  The
collision-free transfer theorem then preserves it asymptotically.

This module proves the reduction, not the typical-pair gap.  A single fixed
block need not be Hamming covariant, and finite repeated-label controls below
are algebraic checks rather than natural asymptotic evidence.  The next
representation-theoretic target is now precise: evaluate one bounded-ridge
pair commutator at ``W=K/2+O(sqrt(K))`` under iid Plancherel sources and prove
its ``q^{-2}``-rescaled expectation is nonnegligible.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_povm_regular_master_reduction import (
    canonical_component_effects,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_hamming_orbit_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PhysicalHammingOrbitControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    copy_count: int
    child_cube_dimension: int
    child_leaf_count: int
    ambient_physical_dimension: int
    common_fiber_dimension: int
    normalized_pair_gap_by_hamming_weight: dict[str, float]
    maximum_within_hamming_orbit_residual: float
    direct_normalized_component_M4: float
    hamming_profile_component_M4: float
    binomial_rescaled_profile_component_M4: float
    maximum_M4_identity_residual: float
    exact_hamming_orbit_counting_verified: bool
    status: str


@dataclass(frozen=True)
class SourceRelabelingEquivarianceControl:
    control_id: str
    n: int
    target_partition: Partition
    base_labels: tuple[Label, ...]
    base_pair: tuple[int, int]
    source_pair_flip_count: int
    source_pair_permutation_count: int
    maximum_flip_equivariance_residual: float
    maximum_permutation_equivariance_residual: float
    exact_scalar_component_pair_equivariance_verified: bool
    status: str


@dataclass(frozen=True)
class TypicalHammingPairScalingRecord:
    n: int
    information_threshold_copy_count: int
    child_cube_dimension: int
    child_leaf_count_log2: int
    typical_window_lower_weight: int
    typical_window_upper_weight: int
    typical_window_binomial_mass: float
    target_rescaled_pair_gap_polynomial_degree: int
    target_rescaled_pair_gap_lower_bound: float
    equivalent_pair_gap_log2_lower_bound: float
    resulting_M4_lower_bound: float
    typical_hamming_profile_suffices_for_M4: bool
    natural_typical_ridge_pair_gap_proved: bool
    status: str


@dataclass(frozen=True)
class ComponentHammingOrbitReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    physical_controls: list[PhysicalHammingOrbitControl]
    relabeling_controls: list[SourceRelabelingEquivarianceControl]
    scaling_records: list[TypicalHammingPairScalingRecord]
    regular_master_reduction: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _pair_commutator_trace(left: np.ndarray, right: np.ndarray) -> float:
    commutator = left @ right - right @ left
    return float(np.trace(commutator.conj().T @ commutator).real)


def component_M4_from_hamming_profile(
    child_cube_dimension: int,
    pair_gap_by_weight: dict[int, float],
) -> tuple[float, float]:
    """Return both equal forms in equation (2)."""

    if child_cube_dimension < 1:
        raise ValueError("child cube dimension must be positive")
    if set(pair_gap_by_weight) != set(range(1, child_cube_dimension + 1)):
        raise ValueError("one pair gap is required for every nonzero Hamming weight")
    if any(value < 0 for value in pair_gap_by_weight.values()):
        raise ValueError("pair commutator gaps must be nonnegative")
    m = child_cube_dimension
    q = 1 << m
    direct = (q / 2) * sum(
        math.comb(m, weight) * pair_gap_by_weight[weight]
        for weight in range(1, m + 1)
    )
    binomial = 0.5 * sum(
        math.comb(m, weight)
        / q
        * q**2
        * pair_gap_by_weight[weight]
        for weight in range(1, m + 1)
    )
    return direct, binomial


def audit_physical_hamming_orbit(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> PhysicalHammingOrbitControl:
    copy_count = len(labels)
    if copy_count < 2:
        raise ValueError("a final-root child requires at least two source pairs")
    m = copy_count - 1
    q = 1 << m
    left_masks = tuple(range(q))
    right_masks = tuple(range(q, 2 * q))
    ambient, fiber, sides = canonical_component_effects(
        target,
        labels,
        left_masks,
        right_masks,
        tolerance=tolerance,
    )
    if not fiber:
        raise ValueError("the selected final-root children have zero common span")
    effects = sides[0]
    by_weight: dict[int, list[float]] = {
        weight: [] for weight in range(1, m + 1)
    }
    direct = 0.0
    for left in range(q):
        for right in range(left + 1, q):
            value = _pair_commutator_trace(effects[left], effects[right]) / ambient
            by_weight[(left ^ right).bit_count()].append(value)
            direct += value
    profile = {
        weight: sum(values) / len(values)
        for weight, values in by_weight.items()
    }
    orbit_residual = max(
        abs(value - profile[weight])
        for weight, values in by_weight.items()
        for value in values
    )
    formula, binomial = component_M4_from_hamming_profile(m, profile)
    identity_residual = max(abs(direct - formula), abs(direct - binomial))
    exact = identity_residual <= 1000 * tolerance
    return PhysicalHammingOrbitControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        copy_count=copy_count,
        child_cube_dimension=m,
        child_leaf_count=q,
        ambient_physical_dimension=ambient,
        common_fiber_dimension=fiber,
        normalized_pair_gap_by_hamming_weight={
            str(weight): value for weight, value in profile.items()
        },
        maximum_within_hamming_orbit_residual=orbit_residual,
        direct_normalized_component_M4=direct,
        hamming_profile_component_M4=formula,
        binomial_rescaled_profile_component_M4=binomial,
        maximum_M4_identity_residual=identity_residual,
        exact_hamming_orbit_counting_verified=exact,
        status=(
            "exact-physical-component-hamming-profile-counting-verified"
            if exact
            else "physical-component-hamming-profile-control-failure"
        ),
    )


def _flipped_labels(labels: tuple[Label, ...], mask: int) -> tuple[Label, ...]:
    return tuple(
        (right, left) if mask & (1 << index) else (left, right)
        for index, (left, right) in enumerate(labels)
    )


def _permuted_mask(mask: int, permutation: tuple[int, ...]) -> int:
    output = 0
    for new_index, old_index in enumerate(permutation):
        output |= ((mask >> old_index) & 1) << new_index
    return output


def _normalized_child_pair_gap(
    target: Partition,
    labels: tuple[Label, ...],
    pair: tuple[int, int],
    *,
    tolerance: float,
) -> float:
    m = len(labels) - 1
    q = 1 << m
    ambient, fiber, sides = canonical_component_effects(
        target,
        labels,
        tuple(range(q)),
        tuple(range(q, 2 * q)),
        tolerance=tolerance,
    )
    if not fiber:
        raise ValueError("zero common span in relabeling control")
    left, right = (sides[0][index] for index in pair)
    return _pair_commutator_trace(left, right) / ambient


def audit_source_relabeling_equivariance(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    pair: tuple[int, int],
    *,
    tolerance: float = 1e-9,
) -> SourceRelabelingEquivarianceControl:
    copy_count = len(labels)
    m = copy_count - 1
    q = 1 << m
    if copy_count < 2 or pair[0] == pair[1] or any(
        not 0 <= index < q for index in pair
    ):
        raise ValueError("invalid final-child pair")
    base = _normalized_child_pair_gap(
        target,
        labels,
        pair,
        tolerance=tolerance,
    )
    flip_residuals = []
    for flip in range(q):
        transformed = _flipped_labels(labels, flip)
        transformed_pair = pair[0] ^ flip, pair[1] ^ flip
        value = _normalized_child_pair_gap(
            target,
            transformed,
            transformed_pair,
            tolerance=tolerance,
        )
        flip_residuals.append(abs(value - base))

    permutation_residuals = []
    for first_coordinates in itertools.permutations(range(m)):
        permutation = (*first_coordinates, m)
        transformed_labels = tuple(labels[index] for index in permutation)
        transformed_pair = tuple(
            _permuted_mask(index, permutation) for index in pair
        )
        value = _normalized_child_pair_gap(
            target,
            transformed_labels,
            transformed_pair,
            tolerance=tolerance,
        )
        permutation_residuals.append(abs(value - base))
    maximum_flip = max(flip_residuals, default=0.0)
    maximum_permutation = max(permutation_residuals, default=0.0)
    exact = max(maximum_flip, maximum_permutation) <= 1000 * tolerance
    return SourceRelabelingEquivarianceControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        base_labels=labels,
        base_pair=pair,
        source_pair_flip_count=len(flip_residuals),
        source_pair_permutation_count=len(permutation_residuals),
        maximum_flip_equivariance_residual=maximum_flip,
        maximum_permutation_equivariance_residual=maximum_permutation,
        exact_scalar_component_pair_equivariance_verified=exact,
        status=(
            "exact-source-relabeling-component-pair-equivariance-verified"
            if exact
            else "source-relabeling-component-pair-equivariance-control-failure"
        ),
    )


def typical_hamming_pair_scaling_record(
    n: int,
    *,
    target_rescaled_gap_polynomial_degree: int = 2,
) -> TypicalHammingPairScalingRecord:
    if n < 3 or target_rescaled_gap_polynomial_degree < 0:
        raise ValueError("invalid scaling parameters")
    copies = (math.factorial(n) - 1).bit_length() + 2
    m = copies - 1
    radius = math.ceil(math.sqrt(m * math.log(max(n, 3))))
    lower = max(1, m // 2 - radius)
    upper = min(m, math.ceil(m / 2) + radius)
    mass = sum(math.comb(m, weight) for weight in range(lower, upper + 1)) / 2**m
    kappa = n ** (-target_rescaled_gap_polynomial_degree)
    log2_pair = -2 * m - target_rescaled_gap_polynomial_degree * math.log2(n)
    return TypicalHammingPairScalingRecord(
        n=n,
        information_threshold_copy_count=copies - 2,
        child_cube_dimension=m,
        child_leaf_count_log2=m,
        typical_window_lower_weight=lower,
        typical_window_upper_weight=upper,
        typical_window_binomial_mass=mass,
        target_rescaled_pair_gap_polynomial_degree=(
            target_rescaled_gap_polynomial_degree
        ),
        target_rescaled_pair_gap_lower_bound=kappa,
        equivalent_pair_gap_log2_lower_bound=log2_pair,
        resulting_M4_lower_bound=mass * kappa / 2,
        typical_hamming_profile_suffices_for_M4=True,
        natural_typical_ridge_pair_gap_proved=False,
        status="typical-hamming-rescaled-pair-gap-target-quantified",
    )


def run_component_hamming_orbit_reduction(
) -> ComponentHammingOrbitReductionReport:
    standard = (2, 1)
    repeated_labels: tuple[Label, ...] = ((standard, standard),) * 3
    physical = [
        audit_physical_hamming_orbit(
            "S3-REPEATED-STANDARD-TRIVIAL-TARGET",
            (3,),
            repeated_labels,
        ),
        audit_physical_hamming_orbit(
            "S3-REPEATED-STANDARD-STANDARD-TARGET",
            standard,
            repeated_labels,
        ),
    ]
    trivial = (3,)
    sign = (1, 1, 1)
    nonidentical_labels: tuple[Label, ...] = (
        (trivial, standard),
        (trivial, standard),
        (standard, sign),
    )
    relabeling = [
        audit_source_relabeling_equivariance(
            "S3-NONIDENTICAL-SOURCE-ORBIT",
            standard,
            nonidentical_labels,
            (0, 1),
        )
    ]
    physical_failures = sum(
        not row.exact_hamming_orbit_counting_verified for row in physical
    )
    relabeling_failures = sum(
        not row.exact_scalar_component_pair_equivariance_verified
        for row in relabeling
    )
    exact = physical_failures == 0 and relabeling_failures == 0
    scaling = [
        typical_hamming_pair_scaling_record(n)
        for n in (16, 24, 32, 48, 64, 96, 128, 256)
    ]
    return ComponentHammingOrbitReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "source_relabeling_covariance": (
                "Pair flips and copy-pair permutations conjugate orientation "
                "projectors, child frames, common spans, exact/ridge component "
                "effects, and their pair commutators as in equation (1)."
            ),
            "annealed_hamming_profile": (
                "The iid Plancherel and globally-distinct conditioned laws are "
                "invariant under those relabelings, so expected pair gaps in a "
                "final-root child depend only on Hamming distance."
            ),
            "binomial_M4_identity": (
                "For q=2^m child leaves, M4=(q/2)sum_w binom(m,w)c_w="
                "(1/2)E_W[q^2 c_W] exactly."
            ),
            "typical_pair_sufficiency": (
                "If q^2 c_w>=kappa on Hamming weights of binomial mass rho, "
                "then M4>=rho*kappa/2."
            ),
            "scope": (
                "The reduction does not prove a nonzero natural typical-pair "
                "gap. Blockwise Hamming covariance is neither assumed nor true."
            ),
        },
        physical_controls=physical,
        relabeling_controls=relabeling,
        scaling_records=scaling,
        regular_master_reduction={
            "exponential_leaf_pair_enumeration_required": False,
            "number_of_annealed_hamming_strata": "K-1",
            "decisive_pair_distance": "W~Bin(K-1,1/2)",
            "decisive_rescaling": "q^2 times normalized pair commutator trace",
            "applies_to_exact_green_effects": True,
            "applies_to_normalized_ridge_effects": True,
            "survives_global_distinct_conditioning": True,
            "natural_typical_pair_gap_proved": False,
        },
        proof_obligations=[
            {
                "obligation": "reduce_annealed_component_pair_sum_to_hamming_orbits",
                "resolved": exact,
                "resolution": "Source-pair flips and coordinate permutations preserve both source laws and collapse all pair expectations to K-1 strata.",
            },
            {
                "obligation": "identify_the_pair_gap_scale_needed_for_nonvanishing_M4",
                "resolved": exact,
                "resolution": "Equation (2) shows the exact scale is c_w=q^-2 times a nonnegligible rescaled profile at typical Hamming distance.",
            },
            {
                "obligation": "evaluate_typical_hamming_ridge_pair_gap_under_independent_plancherel",
                "resolved": False,
                "resolution": "Need a leaf-marked bounded Green/heat-kernel calculation for one pair with distance K/2+O(sqrt K).",
            },
            {
                "obligation": "transfer_ridge_pair_profile_to_exact_green_profile",
                "resolved": False,
                "resolution": "Use the trace-weighted polar ratio from the Green-ridge stability theorem.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A generic unequal-source block is exactly translation covariant.",
                "resolved": True,
                "resolution": "False. Covariance maps the block to a relabeled source block; only the iid or all-distinct conditioned ensemble is invariant.",
            },
            {
                "objection": "The q^2 leaf pairs make direct natural M4 analysis intrinsically exponential.",
                "resolved": True,
                "resolution": "False at the scalar annealed level: equation (2) has only K-1 Hamming strata and is dominated by typical binomial distance.",
            },
            {
                "objection": "A fixed pair gap of order q^-2 is too small to matter.",
                "resolved": True,
                "resolution": "False when it holds on typical Hamming mass; the q^2 pair multiplicity makes the total M4 constant-scale.",
            },
            {
                "objection": "Hamming symmetry itself proves the rescaled pair gap is positive.",
                "resolved": False,
                "resolution": "Commuting ensemble-covariant POVMs exist. Positivity requires the natural recoupling/return calculation.",
            },
        ],
        headline_metrics={
            "annealed_component_hamming_orbit_reduction_theorem_count": int(exact),
            "binomial_rescaled_pair_M4_identity_theorem_count": int(exact),
            "global_distinct_hamming_profile_transfer_theorem_count": int(exact),
            "physical_control_count": len(physical),
            "physical_control_failure_count": physical_failures,
            "relabeling_control_count": len(relabeling),
            "relabeling_control_failure_count": relabeling_failures,
            "natural_typical_hamming_pair_gap_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "annealed_pair_gap_depends_only_on_hamming_distance": exact,
            "exponential_pair_sum_reduced_to_binomial_profile": exact,
            "q_inverse_two_typical_pair_scale_suffices_for_M4": exact,
            "natural_typical_hamming_ridge_pair_gap_positive": False,
            "natural_independent_plancherel_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural M4 calculation now needs one typical-Hamming "
                "rescaled ridge pair profile rather than all leaf pairs, but "
                "that profile has not been evaluated or lower-bounded."
            ),
        },
        status=(
            "component-M4-reduced-to-typical-hamming-ridge-pair-gap"
            if exact
            else "component-hamming-orbit-reduction-control-failure"
        ),
        summary=(
            "Used exact source-relabeling symmetry to collapse the annealed "
            "final-root component M4 to a binomial average of q^2-rescaled "
            "typical-Hamming pair commutators."
        ),
        falsifiers_triggered=[
            "Blockwise orientation translation covariance is false and is not needed for the annealed scalar reduction.",
            "The exponential leaf-pair count collapses to K-1 Hamming strata under the natural source law.",
            "The decisive individual pair scale is q^-2, not constant or q^-1.",
            "No positive typical-pair gap, exact natural M4, compiler, decoder, or speedup is proved.",
        ],
    )


def write_component_hamming_orbit_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_hamming_orbit_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_component_hamming_orbit_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
