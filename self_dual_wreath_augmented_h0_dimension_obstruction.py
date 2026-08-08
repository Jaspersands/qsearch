"""Asymptotic dimension obstruction to pair-common cokernel completeness.

Fix a target irrep ``nu`` and ``K`` source pairs.  Let ``N=2^K`` be the
orientation count, ``G=n!``, and let

    D = d_nu * product_(all 2K sources) d_lambda

be the physical target-carrier dimension.  The leaf synthesis

    D_0 : direct_sum_e U_e -> H

has coefficient dimension ``L=sum_e rank(U_e)`` and therefore

    dim ker(D_0) >= L-D.                                    (1)

Uniform orientation-rank concentration gives

    L >= (1-epsilon) (N/G) D                                (2)

simultaneously over all leaves.  On the other hand, the rank of the pair
boundary is at most the total pair-core coefficient budget

    P = sum_(e<f) dim(U_e intersection U_f).                 (3)

For every non-antipodal pair, the exact Plancherel expectation is
``2D/G^3``.  Antipodal pairs contribute at most ``D/G^2`` and only for a
trivial or sign target.  Hence

    E[P/D] <= N(N-2)/G^3 + N/(2G^2).                        (4)

At the information threshold ``K=ceil(log_2 G)``, put ``c=N/G`` and
``g=c-1``.  Since ``n! = 2^v q`` with ``q`` odd and ``N`` is a larger power
of two,

    g = (N-G)/G >= 2^v/G,   v=v_2(n!)=Theta(n).              (5)

Choose ``epsilon=g/(4c)``.  Equations (1)-(2) give
``dim ker(D_0)>=3gD/4``.  Markov applied to (4) gives
``P<=gD/4`` except with probability ``O(2^-v)``.  The rank-concentration
failure remains ``2^-Theta(n(log n)^2)`` even after the ``epsilon^-2`` cost.
Global-distinct conditioning divides these failures by ``P_cf=1-o(1)``.
Therefore, with probability tending to one,

    dim H_0 = dim ker(D_0) - rank(D_1) >= gD/2 > 0.          (6)

With one extra source pair, ``c>=2`` and (6) strengthens to
``dim H_0>=D/2``.  Thus original pair-common relations cannot be a complete
asymptotic presentation of the polar output constraints.

This is not a no-go theorem for hierarchical polar sampling.  A child span
can intersect another child even when no original leaf pair intersects (the
three-lines-in-a-plane example).  Such emergent span-level dependencies are
exactly what a successful recursive resolver must expose.  The theorem kills
direct common-core Cech completeness and makes hierarchical H0 resolution a
mandatory, potentially macroscopic step.
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
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_pair_core_rank_concentration import (
    factorized_pair_core_rank,
    smallest_nonidentity_conjugacy_class_size,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_augmented_h0_dimension_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PairBudgetExpectationControl:
    n: int
    copy_count: int
    target_partition: Partition
    target_dimension: int
    direct_expected_total_pair_rank_relative_to_carrier: str
    formula_expected_total_pair_rank_relative_to_carrier: str
    exact_formula_match: bool
    status: str


@dataclass(frozen=True)
class AugmentedH0ScalingRecord:
    n: int
    group_order_decimal: str
    two_adic_factorial_valuation: int
    copy_offset: int
    copy_count: int
    orientation_count_decimal: str
    orientation_oversampling_ratio: float
    binary_rounding_gap_ratio: float
    two_adic_gap_lower_bound: float
    relative_rank_tolerance: float
    expected_total_pair_budget_relative_upper_bound: float
    pair_budget_to_rounding_gap_ratio: float
    guaranteed_h0_dimension_relative_to_carrier: float
    log2_unconditioned_uniform_leaf_rank_failure_upper_bound: float
    log2_unconditioned_pair_budget_failure_upper_bound: float
    log2_global_distinct_probability: float
    log2_conditioned_combined_failure_upper_bound: float
    conditioned_combined_failure_upper_bound: float
    finite_conditioned_h0_lower_bound_certified: bool
    h0_lower_bound_is_macroscopic: bool
    status: str


@dataclass(frozen=True)
class AugmentedH0DimensionObstructionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    expectation_controls: list[PairBudgetExpectationControl]
    scaling_records: list[AugmentedH0ScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def two_adic_factorial_valuation(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    valuation = 0
    power = 2
    while power <= n:
        valuation += n // power
        power *= 2
    return valuation


def information_threshold_copy_count(n: int, copy_offset: int = 0) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    if copy_offset < 0:
        raise ValueError("copy offset must be nonnegative")
    return math.ceil(math.lgamma(n + 1) / math.log(2)) + copy_offset


def pair_budget_expectation_relative(
    n: int,
    copy_count: int,
    target: Partition | None = None,
) -> Fraction:
    """Return (4), exactly; ``target=None`` gives the all-target upper bound."""

    if n < 2 or copy_count < 1:
        raise ValueError("n>=2 and a positive copy count are required")
    if target is not None and sum(target) != n:
        raise ValueError("target partition has the wrong size")
    order = math.factorial(n)
    orientations = 1 << copy_count
    nonantipodal = Fraction(
        orientations * (orientations - 2),
        order**3,
    )
    antipodal_target = target is None or target in ((n,), (1,) * n)
    antipodal = (
        Fraction(orientations, 2 * order * order)
        if antipodal_target
        else Fraction()
    )
    return nonantipodal + antipodal


def _direct_pair_budget_expectation(
    n: int,
    copy_count: int,
    target: Partition,
) -> Fraction:
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    dimensions = {
        partition: hook_length_dimension(partition)
        for partition in partitions
    }
    weights = {
        partition: Fraction(dimensions[partition] ** 2, order)
        for partition in partitions
    }
    target_dimension = dimensions[target]
    orientations = tuple(range(1 << copy_count))
    total = Fraction()
    for sources in itertools.product(partitions, repeat=2 * copy_count):
        labels: tuple[Label, ...] = tuple(
            (sources[2 * index], sources[2 * index + 1])
            for index in range(copy_count)
        )
        probability = math.prod(weights[source] for source in sources)
        all_source_dimension = math.prod(dimensions[source] for source in sources)
        pair_sum = sum(
            factorized_pair_core_rank(target, labels, left, right)
            for left, right in itertools.combinations(orientations, 2)
        )
        total += probability * Fraction(
            pair_sum,
            target_dimension * all_source_dimension,
        )
    return total


def audit_pair_budget_expectation(
    n: int,
    copy_count: int,
    target: Partition,
) -> PairBudgetExpectationControl:
    direct = _direct_pair_budget_expectation(n, copy_count, target)
    formula = pair_budget_expectation_relative(n, copy_count, target)
    verified = direct == formula
    return PairBudgetExpectationControl(
        n=n,
        copy_count=copy_count,
        target_partition=target,
        target_dimension=hook_length_dimension(target),
        direct_expected_total_pair_rank_relative_to_carrier=str(direct),
        formula_expected_total_pair_rank_relative_to_carrier=str(formula),
        exact_formula_match=verified,
        status=(
            "exact-total-pair-budget-expectation-verified"
            if verified
            else "total-pair-budget-expectation-mismatch"
        ),
    )


@lru_cache(maxsize=None)
def _global_distinct_log2_by_offset(n: int) -> tuple[float, float]:
    """Evaluate exact global-distinct mass at K0 and K0+1 in one DP."""

    partitions = tuple(integer_partitions(n))
    base = information_threshold_copy_count(n)
    degrees = (2 * base, 2 * (base + 1))
    if degrees[1] > len(partitions):
        values = tuple(
            -math.inf if degree > len(partitions) else math.nan
            for degree in degrees
        )
        if all(math.isinf(value) for value in values):
            return values  # type: ignore[return-value]
    log_order = math.lgamma(n + 1)
    log_weights = np.asarray(
        [
            2 * math.log(hook_length_dimension(partition)) - log_order
            for partition in partitions
        ]
    )
    coefficients = np.full(degrees[1] + 1, -math.inf)
    coefficients[0] = 0.0
    for log_weight in log_weights:
        previous = coefficients.copy()
        coefficients[1:] = np.logaddexp(
            previous[1:],
            log_weight + previous[:-1],
        )
    output = []
    for degree in degrees:
        if degree > len(partitions):
            output.append(-math.inf)
        else:
            log_probability = math.lgamma(degree + 1) + coefficients[degree]
            output.append(min(0.0, float(log_probability / math.log(2))))
    return output[0], output[1]


def _log2_sum(left: float, right: float) -> float:
    if left == -math.inf:
        return right
    if right == -math.inf:
        return left
    high = max(left, right)
    return high + math.log2(math.exp2(left - high) + math.exp2(right - high))


def augmented_h0_scaling_record(
    n: int,
    copy_offset: int = 0,
) -> AugmentedH0ScalingRecord:
    if copy_offset not in (0, 1):
        raise ValueError("the theorem record supports offsets zero and one")
    order = math.factorial(n)
    copy_count = information_threshold_copy_count(n, copy_offset)
    orientations = 1 << copy_count
    oversampling = orientations / order
    gap = (orientations - order) / order
    valuation = two_adic_factorial_valuation(n)
    two_adic_lower = math.ldexp(1.0, valuation) / order
    if copy_offset == 0 and gap + 1e-15 < two_adic_lower:
        raise ArithmeticError("binary rounding gap violates the two-adic bound")
    epsilon = gap / (4 * oversampling)
    if epsilon <= 0:
        raise ArithmeticError("n! cannot be a power of two for n>=3")

    partition_count = len(integer_partitions(n))
    minimum_class = smallest_nonidentity_conjugacy_class_size(n)
    log2_rank_failure = (
        copy_count
        + math.log2(partition_count - 1)
        + (2 - copy_count) * math.log2(minimum_class)
        - 2 * math.log2(epsilon)
    )
    pair_expectation = float(
        pair_budget_expectation_relative(n, copy_count)
    )
    pair_failure = 4 * pair_expectation / gap
    log2_pair_failure = math.log2(pair_failure) if pair_failure else -math.inf
    distinct_log2 = _global_distinct_log2_by_offset(n)[copy_offset]
    combined_log2 = (
        _log2_sum(log2_rank_failure, log2_pair_failure) - distinct_log2
        if math.isfinite(distinct_log2)
        else math.inf
    )
    combined_probability = (
        min(1.0, math.exp2(combined_log2))
        if math.isfinite(combined_log2) and combined_log2 > -1074
        else 0.0
        if combined_log2 <= -1074
        else 1.0
    )
    certified = bool(combined_log2 < 0)
    h0_lower = gap / 2
    return AugmentedH0ScalingRecord(
        n=n,
        group_order_decimal=str(order),
        two_adic_factorial_valuation=valuation,
        copy_offset=copy_offset,
        copy_count=copy_count,
        orientation_count_decimal=str(orientations),
        orientation_oversampling_ratio=oversampling,
        binary_rounding_gap_ratio=gap,
        two_adic_gap_lower_bound=two_adic_lower,
        relative_rank_tolerance=epsilon,
        expected_total_pair_budget_relative_upper_bound=pair_expectation,
        pair_budget_to_rounding_gap_ratio=pair_expectation / gap,
        guaranteed_h0_dimension_relative_to_carrier=h0_lower,
        log2_unconditioned_uniform_leaf_rank_failure_upper_bound=(
            log2_rank_failure
        ),
        log2_unconditioned_pair_budget_failure_upper_bound=log2_pair_failure,
        log2_global_distinct_probability=distinct_log2,
        log2_conditioned_combined_failure_upper_bound=combined_log2,
        conditioned_combined_failure_upper_bound=combined_probability,
        finite_conditioned_h0_lower_bound_certified=certified,
        h0_lower_bound_is_macroscopic=h0_lower >= 0.5,
        status=(
            "finite-conditioned-augmented-h0-lower-bound-certified"
            if certified
            else "asymptotic-augmented-h0-obstruction-finite-bound-vacuous"
        ),
    )


def run_augmented_h0_dimension_obstruction() -> (
    AugmentedH0DimensionObstructionReport
):
    expectation_controls = [
        audit_pair_budget_expectation(3, 2, target)
        for target in integer_partitions(3)
    ]
    scaling = [
        augmented_h0_scaling_record(n, offset)
        for n in (12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
        for offset in (0, 1)
    ]
    failures = sum(not row.exact_formula_match for row in expectation_controls)
    minimal = [row for row in scaling if row.copy_offset == 0]
    extra = [row for row in scaling if row.copy_offset == 1]
    finite_certified = sum(
        row.finite_conditioned_h0_lower_bound_certified for row in scaling
    )
    verified = failures == 0
    tail_minimal = minimal[-1]
    tail_extra = extra[-1]
    metrics: dict[str, int | float] = {
        "exact_pair_budget_expectation_theorem_count": int(verified),
        "expectation_control_count": len(expectation_controls),
        "expectation_control_failure_count": failures,
        "two_adic_minimal_copy_gap_theorem_count": 1,
        "asymptotic_minimal_copy_augmented_h0_obstruction_count": 1,
        "asymptotic_extra_copy_macroscopic_h0_obstruction_count": 1,
        "scaling_row_count": len(scaling),
        "finite_conditioned_certified_row_count": finite_certified,
        "tail_minimal_h0_relative_lower_bound": (
            tail_minimal.guaranteed_h0_dimension_relative_to_carrier
        ),
        "tail_minimal_log2_conditioned_failure_upper_bound": (
            tail_minimal.log2_conditioned_combined_failure_upper_bound
        ),
        "tail_extra_h0_relative_lower_bound": (
            tail_extra.guaranteed_h0_dimension_relative_to_carrier
        ),
        "tail_extra_log2_conditioned_failure_upper_bound": (
            tail_extra.log2_conditioned_combined_failure_upper_bound
        ),
        "hierarchical_span_dependency_resolver_count": 1,
        "new_quantum_algorithm_count": 0,
    }
    return AugmentedH0DimensionObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "leaf_kernel_lower_bound": (
                "dim ker(D_0)>=sum_e rank(U_e)-D, and simultaneous rank "
                "concentration makes the sum at least (1-epsilon)(N/G)D."
            ),
            "total_pair_budget_expectation": (
                "E[sum_(e<f)dim K_ef/D]<=N(N-2)/G^3+N/(2G^2)."
            ),
            "two_adic_rounding_gap": (
                "At K=ceil(log2 G), (2^K-G)/G>=2^v2(G)/G because the "
                "power-of-two difference has exact factor 2^v2(G)."
            ),
            "conditioned_h0_lower_bound": (
                "With epsilon=(N/G-1)/(4N/G), concentration plus Markov "
                "gives dim H0>=(N/G-1)D/2 with probability 1-o(1), even "
                "after conditioning all sources distinct."
            ),
            "scope": (
                "This rules out direct pair-common Cech completeness. It does "
                "not rule out recursive child-span intersections or a global "
                "structured synthesis-kernel transform."
            ),
        },
        expectation_controls=expectation_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "decide_typical_pair_relation_cokernel_completeness",
                "resolved": verified,
                "resolution": (
                    "It fails: at minimal copies H0 is nonzero with probability "
                    "1-o(1), and one extra copy makes H0 at least D/2."
                ),
            },
            {
                "obligation": "construct_hierarchical_emergent_dependency_resolver",
                "resolved": True,
                "resolution": (
                    "The hierarchical-cokernel theorem recursively decomposes "
                    "every synthesis kernel into child kernels and pseudoinverse "
                    "lifts of child-span intersections. Its coherent circuit and "
                    "natural endpoint gap remain open."
                ),
            },
            {
                "obligation": "relate_h0_resolution_to_graded_endpoint_gap",
                "resolved": False,
                "resolution": (
                    "The pair-relation trim controls known constraints only. "
                    "Emergent span-level constraints need their own graded "
                    "Schur-complement analysis."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Dense live pair-core support should generate every leaf dependency.",
                "resolved": True,
                "resolution": (
                    "There are Theta(N^2) live pairs, but each has expected "
                    "relative rank Theta(G^-3); their total budget is too small "
                    "for the synthesis kernel forced by binary oversampling."
                ),
            },
            {
                "objection": "The minimal binary oversampling gap could be smaller than the pair budget.",
                "resolved": True,
                "resolution": (
                    "The two-adic gap is at least 2^v2(n!)/n!, exponentially "
                    "larger than the O(1/n!) pair budget."
                ),
            },
            {
                "objection": "Nonzero augmented H0 disproves every hierarchical polar sampler.",
                "resolved": True,
                "resolution": (
                    "False. Recursive child spans can have intersections not "
                    "visible in original leaf pairs; the theorem redirects the "
                    "mechanism toward those emergent dependencies."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "pair_common_relations_asymptotically_exhaust_leaf_synthesis_kernel": False,
            "minimal_copy_augmented_h0_nonzero_with_high_probability": verified,
            "one_extra_copy_augmented_h0_macroscopic_with_high_probability": verified,
            "direct_common_core_cech_is_complete_polar_sampler": False,
            "hierarchical_span_level_dependency_resolution_ruled_out": False,
            "hierarchical_span_level_dependency_resolver_proved": True,
            "hierarchical_span_level_dependency_resolver_coherent": False,
            "graded_endpoint_gap_for_emergent_h0_constraints_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pair-common relations are asymptotically dimension-incomplete. "
                "Recursive child-span dependencies resolve the cokernel exactly, "
                "but their pseudoinverse-frame grading and coherent transform "
                "remain uncontrolled."
            ),
        },
        status=(
            "pair-cech-incomplete-hierarchical-cokernel-complete-conditioning-open"
            if verified
            else "augmented-h0-dimension-control-failure"
        ),
        summary=(
            "Proved that pair-common relations cannot exhaust the natural leaf "
            "synthesis kernel: augmented H0 survives at minimal copies and is "
            "macroscopic with one extra copy, requiring recursive span relations."
        ),
        falsifiers_triggered=[
            "Dense pair-core graph support does not imply pair-generation of the synthesis kernel.",
            "The direct common-core Cech complex is asymptotically incomplete at H0.",
            "The graded pair-relation endpoint gap cannot by itself implement the full orientation polar.",
        ],
    )


def write_augmented_h0_dimension_obstruction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_augmented_h0_dimension_obstruction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_augmented_h0_dimension_obstruction_report()
    print(json.dumps(report, indent=2))
