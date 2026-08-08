"""Factorially small rank budget for every pair-common hierarchy sector.

Fix ``K`` source pairs and the coordinate dyadic hierarchy on the orientation
cube ``F_2^K``.  A level-``d`` node is a coset of the first ``d`` coordinate
directions, so it has width ``2^d`` and there are ``2^(K-d)`` such nodes.

For a non-antipodal orientation pair, the shared, left-only, and right-only
source blocks are all nonempty.  Under independent Plancherel source labels,
the exact pair-carrier law gives expected ambient-relative common rank

    2/|S_n|^3,                                             (1)

one contribution from each one-dimensional carrier.  The span of arbitrarily
coherent pair-common ranges has rank at most the sum of their ranks, so no
triangle or cycle independence is needed for this exact-common sector.

Writing ``N=2^K``, the hierarchy contains

    N(2N-K-3)/2                                           (2)

non-antipodal pair incidences.  At the root there are ``N/2`` antipodal
pairs.  Their shared block is only the fixed target, so their common rank is
zero unless the target is trivial or sign; for either one-dimensional target
the expected relative rank per pair is ``1/|S_n|^2``.  Consequently, for a
fixed target ``tau``,

    E rank(common hierarchy span)/D_tau
      <= N(2N-K-3)/|S_n|^3
         + 1[dim(tau)=1] N/(2|S_n|^2).                    (3)

Summing (3) over all ``p(n)`` targets gives the unweighted target-union budget

    p(n)N(2N-K-3)/|S_n|^3 + N/|S_n|^2.                   (4)

At ``K=ceil(log_2 |S_n|)+2``, ``4|S_n|<=N<8|S_n|``, so
(4) is ``O(p(n)/|S_n|)``.  Conditioning all ``2K`` source labels to be
distinct divides the expectation by ``P_cf(n,K)=1-o(1)``.  Markov applied to
the target sum then gives simultaneous factorially small exact-common rank.

This is a trimming theorem, not a spectral-edge theorem.  Small rank does not
bound the eigenvalues on the trimmed sector, and the vast noncommon carrier
space can still accumulate through recoupling maps.  The result assumes the
independent Plancherel source law before global-distinct conditioning and says
nothing about arbitrary source couplings, PGM state mass, or a speedup.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_event_transfer import (
    stable_global_collision_free_probability,
)
from self_dual_wreath_natural_pair_carrier_law import (
    exact_expected_normalized_block_multiplicity,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_hierarchy_pair_common_rank_budget.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class HierarchyPairIncidenceControl:
    copy_count: int
    orientation_count: int
    enumerated_lower_level_pair_incidence_count: int
    predicted_lower_level_pair_incidence_count: int
    enumerated_root_nonantipodal_pair_count: int
    predicted_root_nonantipodal_pair_count: int
    enumerated_root_antipodal_pair_count: int
    predicted_root_antipodal_pair_count: int
    enumerated_total_nonantipodal_pair_incidence_count: int
    predicted_total_nonantipodal_pair_incidence_count: int
    exact_hierarchy_pair_count_verified: bool
    status: str


@dataclass(frozen=True)
class ExactPairCommonMassControl:
    n: int
    target_partition: Partition
    target_dimension: int
    random_factor_count_per_nonempty_block: int
    observed_nonantipodal_expected_relative_common_rank: str
    predicted_nonantipodal_expected_relative_common_rank: str
    observed_root_antipodal_expected_relative_common_rank: str
    predicted_root_antipodal_expected_relative_common_rank: str
    exact_nonantipodal_mass_verified: bool
    exact_root_antipodal_mass_verified: bool
    status: str


@dataclass(frozen=True)
class HierarchyPairCommonRankScalingRecord:
    n: int
    partition_count: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    orientation_count_decimal: str
    orientation_to_group_order_ratio: float
    nonantipodal_pair_incidence_count_decimal: str
    root_antipodal_pair_count_decimal: str
    unconditioned_one_dimensional_target_expected_relative_rank_upper_bound: float
    unconditioned_one_dimensional_target_bound_log2: float
    unconditioned_all_target_union_expected_rank_upper_bound: float
    unconditioned_all_target_union_bound_log2: float
    global_distinct_probability: float
    global_distinct_probability_log2: float
    conditioned_all_target_union_expected_rank_upper_bound: float
    conditioned_all_target_union_bound_log2: float
    simultaneous_relative_rank_threshold: float
    simultaneous_failure_probability_upper_bound: float
    finite_simultaneous_rank_trim_certified: bool
    asymptotic_conditioned_all_target_rank_budget_vanishes: bool
    full_noncommon_frame_edge_proved: bool
    status: str


@dataclass(frozen=True)
class HierarchyPairCommonRankBudgetReport:
    created_at: str
    theorem_contract: dict[str, Any]
    pair_incidence_controls: list[HierarchyPairIncidenceControl]
    exact_mass_controls: list[ExactPairCommonMassControl]
    scaling_records: list[HierarchyPairCommonRankScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def hierarchy_pair_incidence_formula(copy_count: int) -> tuple[int, int, int]:
    """Return lower, root-nonantipodal, and root-antipodal pair counts."""

    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    orientation_count = 1 << copy_count
    lower = orientation_count * (orientation_count - copy_count - 1) // 2
    root_nonantipodal = orientation_count * (orientation_count - 2) // 2
    root_antipodal = orientation_count // 2
    return lower, root_nonantipodal, root_antipodal


def enumerate_hierarchy_pair_incidence(
    copy_count: int,
) -> tuple[int, int, int]:
    """Enumerate the same counts directly for small exact controls."""

    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    orientation_count = 1 << copy_count
    antipodal_mask = orientation_count - 1
    lower = 0
    root_nonantipodal = 0
    root_antipodal = 0
    for dimension in range(1, copy_count + 1):
        node_width = 1 << dimension
        for node in range(orientation_count // node_width):
            orientations = range(node * node_width, (node + 1) * node_width)
            for left, right in itertools.combinations(orientations, 2):
                if dimension < copy_count:
                    lower += 1
                elif left ^ right == antipodal_mask:
                    root_antipodal += 1
                else:
                    root_nonantipodal += 1
    return lower, root_nonantipodal, root_antipodal


def audit_hierarchy_pair_incidence(
    copy_count: int,
) -> HierarchyPairIncidenceControl:
    observed = enumerate_hierarchy_pair_incidence(copy_count)
    predicted = hierarchy_pair_incidence_formula(copy_count)
    verified = observed == predicted
    return HierarchyPairIncidenceControl(
        copy_count=copy_count,
        orientation_count=1 << copy_count,
        enumerated_lower_level_pair_incidence_count=observed[0],
        predicted_lower_level_pair_incidence_count=predicted[0],
        enumerated_root_nonantipodal_pair_count=observed[1],
        predicted_root_nonantipodal_pair_count=predicted[1],
        enumerated_root_antipodal_pair_count=observed[2],
        predicted_root_antipodal_pair_count=predicted[2],
        enumerated_total_nonantipodal_pair_incidence_count=(
            observed[0] + observed[1]
        ),
        predicted_total_nonantipodal_pair_incidence_count=(
            predicted[0] + predicted[1]
        ),
        exact_hierarchy_pair_count_verified=verified,
        status=(
            "exact-hierarchy-pair-incidence-count-verified"
            if verified
            else "hierarchy-pair-incidence-control-failure"
        ),
    )


def exact_nonantipodal_pair_common_expectation(
    n: int,
    target: Partition,
    random_factor_count_per_block: int = 1,
) -> Fraction:
    """Enumerate the trivial/sign common-carrier mass for three random blocks."""

    if sum(target) != n or random_factor_count_per_block < 1:
        raise ValueError("invalid target or random block size")
    total = Fraction()
    for carrier in ((n,), (1,) * n):
        shared = exact_expected_normalized_block_multiplicity(
            n,
            carrier,
            random_factor_count_per_block,
            (target,),
        )
        exclusive = exact_expected_normalized_block_multiplicity(
            n,
            carrier,
            random_factor_count_per_block,
        )
        total += shared * exclusive * exclusive
    return total


def exact_root_antipodal_pair_common_expectation(
    n: int,
    target: Partition,
    exclusive_random_factor_count: int = 1,
) -> Fraction:
    """Enumerate the root exception, whose shared block is only ``target``."""

    if sum(target) != n or exclusive_random_factor_count < 1:
        raise ValueError("invalid target or random block size")
    if hook_length_dimension(target) != 1:
        return Fraction()
    exclusive = exact_expected_normalized_block_multiplicity(
        n,
        target,
        exclusive_random_factor_count,
    )
    return exclusive * exclusive


def audit_exact_pair_common_mass(
    n: int,
    target: Partition,
    random_factor_count_per_block: int = 1,
) -> ExactPairCommonMassControl:
    order = math.factorial(n)
    dimension = hook_length_dimension(target)
    observed_nonantipodal = exact_nonantipodal_pair_common_expectation(
        n,
        target,
        random_factor_count_per_block,
    )
    predicted_nonantipodal = Fraction(2, order**3)
    observed_antipodal = exact_root_antipodal_pair_common_expectation(
        n,
        target,
        random_factor_count_per_block,
    )
    predicted_antipodal = Fraction(int(dimension == 1), order**2)
    nonantipodal_verified = observed_nonantipodal == predicted_nonantipodal
    antipodal_verified = observed_antipodal == predicted_antipodal
    return ExactPairCommonMassControl(
        n=n,
        target_partition=target,
        target_dimension=dimension,
        random_factor_count_per_nonempty_block=random_factor_count_per_block,
        observed_nonantipodal_expected_relative_common_rank=str(
            observed_nonantipodal
        ),
        predicted_nonantipodal_expected_relative_common_rank=str(
            predicted_nonantipodal
        ),
        observed_root_antipodal_expected_relative_common_rank=str(
            observed_antipodal
        ),
        predicted_root_antipodal_expected_relative_common_rank=str(
            predicted_antipodal
        ),
        exact_nonantipodal_mass_verified=nonantipodal_verified,
        exact_root_antipodal_mass_verified=antipodal_verified,
        status=(
            "exact-pair-common-mass-and-root-exception-verified"
            if nonantipodal_verified and antipodal_verified
            else "pair-common-mass-control-failure"
        ),
    )


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def hierarchy_pair_common_rank_scaling_record(
    n: int,
) -> HierarchyPairCommonRankScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    information_threshold = (order - 1).bit_length()
    copy_count = information_threshold + 2
    orientation_count = 1 << copy_count
    partition_count = len(tuple(integer_partitions(n)))
    lower, root_nonantipodal, root_antipodal = hierarchy_pair_incidence_formula(
        copy_count
    )
    nonantipodal_count = lower + root_nonantipodal
    one_dimensional_target_bound = (
        Fraction(2 * nonantipodal_count, order**3)
        + Fraction(root_antipodal, order**2)
    )
    all_target_bound = (
        Fraction(2 * partition_count * nonantipodal_count, order**3)
        + Fraction(2 * root_antipodal, order**2)
    )
    collision_free_probability = stable_global_collision_free_probability(
        n,
        copy_count,
    )
    if collision_free_probability <= 0:
        raise ArithmeticError("selected scaling n has zero global-distinct mass")
    conditioned_bound = float(all_target_bound) / collision_free_probability
    if conditioned_bound < 1:
        simultaneous_threshold = math.sqrt(conditioned_bound)
        simultaneous_failure = simultaneous_threshold
        finite_certified = True
    else:
        simultaneous_threshold = 1.0
        simultaneous_failure = 1.0
        finite_certified = False
    return HierarchyPairCommonRankScalingRecord(
        n=n,
        partition_count=partition_count,
        group_order_decimal=str(order),
        information_threshold_copy_count=information_threshold,
        selected_copy_count=copy_count,
        orientation_count_decimal=str(orientation_count),
        orientation_to_group_order_ratio=orientation_count / order,
        nonantipodal_pair_incidence_count_decimal=str(nonantipodal_count),
        root_antipodal_pair_count_decimal=str(root_antipodal),
        unconditioned_one_dimensional_target_expected_relative_rank_upper_bound=float(
            one_dimensional_target_bound
        ),
        unconditioned_one_dimensional_target_bound_log2=_fraction_log2(
            one_dimensional_target_bound
        ),
        unconditioned_all_target_union_expected_rank_upper_bound=float(
            all_target_bound
        ),
        unconditioned_all_target_union_bound_log2=_fraction_log2(
            all_target_bound
        ),
        global_distinct_probability=collision_free_probability,
        global_distinct_probability_log2=math.log2(collision_free_probability),
        conditioned_all_target_union_expected_rank_upper_bound=conditioned_bound,
        conditioned_all_target_union_bound_log2=math.log2(conditioned_bound),
        simultaneous_relative_rank_threshold=simultaneous_threshold,
        simultaneous_failure_probability_upper_bound=simultaneous_failure,
        finite_simultaneous_rank_trim_certified=finite_certified,
        asymptotic_conditioned_all_target_rank_budget_vanishes=True,
        full_noncommon_frame_edge_proved=False,
        status=(
            "finite-conditioned-pair-common-rank-trim-certified"
            if finite_certified
            else "finite-conditioning-bound-vacuous-asymptotic-trim-proved"
        ),
    )


def run_hierarchy_pair_common_rank_budget(
) -> HierarchyPairCommonRankBudgetReport:
    incidence_controls = [
        audit_hierarchy_pair_incidence(copy_count)
        for copy_count in range(1, 8)
    ]
    exact_mass_controls = [
        audit_exact_pair_common_mass(n, target, random_count)
        for n, target, random_count in (
            (3, (3,), 1),
            (3, (2, 1), 1),
            (4, (1, 1, 1, 1), 2),
            (4, (2, 2), 2),
        )
    ]
    scaling = [
        hierarchy_pair_common_rank_scaling_record(n)
        for n in (20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(
        not row.exact_hierarchy_pair_count_verified
        for row in incidence_controls
    ) + sum(
        not row.exact_nonantipodal_mass_verified
        or not row.exact_root_antipodal_mass_verified
        for row in exact_mass_controls
    )
    tail = scaling[-1]
    conditioned_tail = [
        row.conditioned_all_target_union_bound_log2 for row in scaling[-5:]
    ]
    tail_decreasing = all(
        right < left
        for left, right in zip(conditioned_tail, conditioned_tail[1:])
    )
    return HierarchyPairCommonRankBudgetReport(
        created_at=utc_now(),
        theorem_contract={
            "pair_common_mass": (
                "Every non-antipodal hierarchy pair has exact expected "
                "ambient-relative common rank 2/|S_n|^3 under independent "
                "Plancherel source labels."
            ),
            "hierarchy_pair_count": (
                "The coordinate dyadic hierarchy has exactly "
                "N(2N-K-3)/2 non-antipodal pair incidences and N/2 root "
                "antipodal pairs."
            ),
            "root_exception": (
                "A root antipodal pair has expected relative common rank "
                "1/|S_n|^2 for a trivial or sign target and zero for every "
                "higher-dimensional target."
            ),
            "coherence_free_rank_bound": (
                "The rank of the span of all pair-common ranges is at most "
                "their rank sum, so arbitrary triangle/cycle alignment cannot "
                "invalidate the exact-common rank budget."
            ),
            "collision_free_transfer": (
                "Conditioning on global source distinctness divides the "
                "expected target-union budget by P_cf(n,K); since P_cf tends "
                "to one, the bound remains O(p(n)/|S_n|)."
            ),
            "scope_exclusion": (
                "The theorem trims only singular-value-one pair-common "
                "directions. It does not control noncommon carriers, near "
                "outliers, recoupling holonomy, the full node edge, PGM mass, "
                "or algorithmic success."
            ),
        },
        pair_incidence_controls=incidence_controls,
        exact_mass_controls=exact_mass_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "count_all_pair_incidences_in_coordinate_hierarchy",
                "resolved": failures == 0,
                "resolution": (
                    "A geometric level sum gives N(2N-K-3)/2 "
                    "non-antipodal incidences plus N/2 root antipodes."
                ),
            },
            {
                "obligation": "bound_arbitrarily_coherent_exact_common_span_rank",
                "resolved": True,
                "resolution": (
                    "Subadditivity of rank converts the exact annealed pair "
                    "law directly into a hierarchy-wide span budget."
                ),
            },
            {
                "obligation": "transfer_exact_common_rank_trim_to_global_distinct_law",
                "resolved": True,
                "resolution": (
                    "Conditional expectation is at most the independent "
                    "expectation divided by P_cf; Markov controls all targets."
                ),
            },
            {
                "obligation": "control_noncommon_collision_free_return_operator",
                "resolved": False,
                "resolution": (
                    "Carrier dimensions above one have correlations below one "
                    "but may accumulate coherently through long words."
                ),
            },
            {
                "obligation": "prove_natural_complete_node_frame_edge",
                "resolved": False,
                "resolution": (
                    "A small exceptional rank does not bound the operator on "
                    "its complement or the eigenvalues inside the trimmed span."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Pair-common ranges recur at constant Hamming radius.",
                "resolved": True,
                "resolution": (
                    "Recurrence is typical in support but each common range has "
                    "expected relative rank 2/|S_n|^3; only O(N^2) pair "
                    "incidences occur across the nested hierarchy."
                ),
            },
            {
                "objection": "Coherent alignment can make the common span larger than the sum bound.",
                "resolved": True,
                "resolution": (
                    "Alignment can only reduce the dimension of a span relative "
                    "to the sum of constituent dimensions."
                ),
            },
            {
                "objection": "A factorially small common rank proves a small frame norm.",
                "resolved": False,
                "resolution": (
                    "Low rank permits arbitrarily large exceptional eigenvalues, "
                    "and says nothing about noncommon bulk accumulation."
                ),
            },
            {
                "objection": "The all-target sum is a naturally weighted direct-sum rank.",
                "resolved": False,
                "resolution": (
                    "It is deliberately an unweighted target-union budget for a "
                    "simultaneous Markov bound, not PGM state mass."
                ),
            },
            {
                "objection": "The independent law automatically covers arbitrary source coupling.",
                "resolved": False,
                "resolution": (
                    "Only conditioning on the explicit global-distinct event is "
                    "transferred; no arbitrary-coupling theorem is claimed."
                ),
            },
        ],
        headline_metrics={
            "exact_hierarchy_pair_count_control_count": len(incidence_controls),
            "exact_pair_common_mass_control_count": len(exact_mass_controls),
            "finite_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "finite_conditioned_rank_trim_record_count": sum(
                row.finite_simultaneous_rank_trim_certified for row in scaling
            ),
            "conditioned_tail_bound_strictly_decreasing_count": int(
                tail_decreasing
            ),
            "tail_n": tail.n,
            "tail_conditioned_all_target_union_bound_log2": (
                tail.conditioned_all_target_union_bound_log2
            ),
            "tail_simultaneous_relative_rank_threshold_log2": math.log2(
                tail.simultaneous_relative_rank_threshold
            ),
            "exact_common_hierarchy_rank_budget_theorem_count": 1,
            "noncommon_collision_free_return_theorem_count": 0,
            "natural_node_frame_edge_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_hierarchy_pair_incidence_formula_proved": failures == 0,
            "exact_nonantipodal_pair_common_mass_proved": failures == 0,
            "root_antipodal_exception_classified": failures == 0,
            "arbitrarily_coherent_exact_common_span_rank_bounded": True,
            "collision_free_all_target_exact_common_rank_trim_proved": True,
            "arbitrary_source_coupling_covered": False,
            "noncommon_collision_free_return_bound_proved": False,
            "near_outlier_accumulation_controlled": False,
            "natural_complete_node_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact pair-common directions occupy factorially small natural "
                "rank, but the noncommon collision-free return operator remains "
                "the dominant unresolved spectral problem."
            ),
        },
        status="hierarchy-exact-common-rank-trim-proved-noncommon-edge-open",
        summary=(
            "Proved an all-depth, all-target factorial rank budget for exact "
            "pair-common directions and isolated the noncommon return operator "
            "as the remaining frame-edge obstruction."
        ),
        falsifiers_triggered=[
            (
                "Typical recurrence of pair-common support does not imply "
                "macroscopic common rank at information-threshold width."
            ),
            (
                "Triangle and cycle alignment cannot defeat the scalar rank "
                "budget for exact common directions, although it remains "
                "decisive on the noncommon complement."
            ),
            (
                "Unconditioned regular stationary outliers must be trimmed; "
                "their existence is not representative of collision-free "
                "physical rank."
            ),
        ],
    )


def write_hierarchy_pair_common_rank_budget_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_hierarchy_pair_common_rank_budget())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_hierarchy_pair_common_rank_budget_report()
    print(json.dumps(report, indent=2, sort_keys=True))
