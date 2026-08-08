"""All-hierarchy low-carrier trim and the quarter-factorial tradeoff.

The natural pair-carrier law assigns expected ambient-relative active rank

    d_alpha^4/|S_n|^3                                    (1)

to carrier ``alpha`` for every non-antipodal orientation pair.  Its principal
correlation is exactly ``1/d_alpha``.  For a cutoff ``L``, remove from every
leaf range the left and right singular spaces belonging to carriers with
``d_alpha<=L``.  Rank subadditivity permits arbitrary coherent alignment and
costs at most twice the sum of the active pair ranks.

For the coordinate dyadic hierarchy with ``N=2^K`` orientations, let

    C_non = N(2N-K-3)/2,   C_anti=N/2.

Writing ``Z_4(L)=sum_(d_alpha<=L)d_alpha^4``, the independent-Plancherel
expected trim budget, summed *without target weights* for a simultaneous
target union bound, is

    B_L = 2 p(n) C_non Z_4(L)/|S_n|^3
          + 2 C_anti sum_(d_tau<=L)d_tau^2/|S_n|^2.       (2)

The second term is the root-antipodal exception: its only carrier is the
fixed target.  After this trim, every pair cross map between the surviving
leaf subspaces has norm at most ``1/(L+1)``.

Choose

    L=floor(|S_n|^(1/4)/p(n)).                            (3)

Since ``N<8|S_n|``, ``Z_4(L)<=p(n)L^4``, and
``sum_(d_tau<=L)d_tau^2<=p(n)L^2``, equations (2)-(3) give

    B_L <= 128/p(n)^2 + 8/(p(n)sqrt(|S_n|)) = o(1),       (4)

while the surviving pair correlation is
``O(p(n)/|S_n|^(1/4))``.  Conditioning all source labels to be distinct
divides (2) by ``P_cf(n,K)=1-o(1)``; Markov then makes the trim simultaneous
over all targets with high probability.

This is a rank--correlation tradeoff, not an edge theorem.  There are
``Theta(|S_n|)`` leaves, so even the factorially small surviving pair bound
is far too weak under a row-sum argument.  Signed Racah/return incidence on
the high-carrier complement remains completely open.  The all-target sum is
not PGM state mass or a naturally weighted direct-sum rank.
"""

from __future__ import annotations

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
from self_dual_wreath_hierarchy_pair_common_rank_budget import (
    exact_root_antipodal_pair_common_expectation,
    hierarchy_pair_incidence_formula,
)
from self_dual_wreath_natural_pair_carrier_law import (
    exact_expected_normalized_block_multiplicity,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_hierarchy_low_carrier_trim.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class ExactLowCarrierMassControl:
    n: int
    target_partition: Partition
    target_dimension: int
    carrier_dimension_cutoff: int
    low_carrier_count: int
    random_factor_count_per_nonempty_block: int
    observed_nonantipodal_low_carrier_relative_rank: str
    predicted_nonantipodal_low_carrier_relative_rank: str
    observed_root_antipodal_low_carrier_relative_rank: str
    predicted_root_antipodal_low_carrier_relative_rank: str
    exact_nonantipodal_low_carrier_law_verified: bool
    exact_root_antipodal_low_carrier_law_verified: bool
    residual_pair_correlation_upper_bound: float
    status: str


@dataclass(frozen=True)
class HierarchyLowCarrierTrimScalingRecord:
    n: int
    partition_count: int
    group_order_decimal: str
    selected_copy_count: int
    orientation_count_decimal: str
    carrier_dimension_cutoff_decimal: str
    carrier_dimension_cutoff_log2: float
    low_carrier_count: int
    low_carrier_fourth_power_sum_log2: float
    low_target_second_power_sum_log2: float
    unconditioned_all_target_trim_rank_upper_bound: float
    unconditioned_all_target_trim_rank_log2: float
    elementary_asymptotic_upper_bound: float
    elementary_asymptotic_upper_bound_log2: float
    global_distinct_probability: float
    global_distinct_probability_log2: float
    conditioned_all_target_trim_rank_upper_bound: float
    conditioned_all_target_trim_rank_log2: float
    simultaneous_relative_trim_threshold: float
    simultaneous_failure_probability_upper_bound: float
    residual_pair_correlation_upper_bound: float
    residual_pair_correlation_log2: float
    finite_simultaneous_trim_certified: bool
    asymptotic_vanishing_rank_and_pair_correlation_proved: bool
    high_carrier_frame_edge_proved: bool
    status: str


@dataclass(frozen=True)
class HierarchyLowCarrierTrimReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_mass_controls: list[ExactLowCarrierMassControl]
    scaling_records: list[HierarchyLowCarrierTrimScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def low_carrier_power_sums(
    n: int,
    cutoff: int,
) -> tuple[int, int, int]:
    if n < 1 or cutoff < 1:
        raise ValueError("n and cutoff must be positive")
    dimensions = tuple(
        hook_length_dimension(partition) for partition in integer_partitions(n)
    )
    selected = tuple(dimension for dimension in dimensions if dimension <= cutoff)
    return len(selected), sum(dimension**2 for dimension in selected), sum(
        dimension**4 for dimension in selected
    )


def canonical_carrier_cutoff(n: int) -> int:
    """Integer cutoff no larger than ``|S_n|^(1/4)/p(n)``."""

    if n < 1:
        raise ValueError("n must be positive")
    order = math.factorial(n)
    partition_count = len(tuple(integer_partitions(n)))
    integer_fourth_root = math.isqrt(math.isqrt(order))
    return max(1, integer_fourth_root // partition_count)


def exact_nonantipodal_low_carrier_expectation(
    n: int,
    target: Partition,
    cutoff: int,
    random_factor_count_per_block: int = 1,
) -> Fraction:
    if sum(target) != n or cutoff < 1 or random_factor_count_per_block < 1:
        raise ValueError("invalid target, cutoff, or random block size")
    total = Fraction()
    for carrier in integer_partitions(n):
        dimension = hook_length_dimension(carrier)
        if dimension > cutoff:
            continue
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
        total += dimension * shared * exclusive * exclusive
    return total


def exact_root_antipodal_low_carrier_expectation(
    n: int,
    target: Partition,
    cutoff: int,
    exclusive_random_factor_count: int = 1,
) -> Fraction:
    if sum(target) != n or cutoff < 1:
        raise ValueError("invalid target or cutoff")
    dimension = hook_length_dimension(target)
    if dimension > cutoff:
        return Fraction()
    if dimension == 1:
        return exact_root_antipodal_pair_common_expectation(
            n,
            target,
            exclusive_random_factor_count,
        )
    normalized_multiplicity = exact_expected_normalized_block_multiplicity(
        n,
        target,
        exclusive_random_factor_count,
    )
    return normalized_multiplicity * normalized_multiplicity


def audit_exact_low_carrier_mass(
    n: int,
    target: Partition,
    cutoff: int,
    random_factor_count_per_block: int = 1,
) -> ExactLowCarrierMassControl:
    order = math.factorial(n)
    dimension = hook_length_dimension(target)
    low_count, _, low_z4 = low_carrier_power_sums(n, cutoff)
    observed_nonantipodal = exact_nonantipodal_low_carrier_expectation(
        n,
        target,
        cutoff,
        random_factor_count_per_block,
    )
    predicted_nonantipodal = Fraction(low_z4, order**3)
    observed_antipodal = exact_root_antipodal_low_carrier_expectation(
        n,
        target,
        cutoff,
        random_factor_count_per_block,
    )
    predicted_antipodal = Fraction(
        dimension**2 if dimension <= cutoff else 0,
        order**2,
    )
    nonantipodal_verified = observed_nonantipodal == predicted_nonantipodal
    antipodal_verified = observed_antipodal == predicted_antipodal
    return ExactLowCarrierMassControl(
        n=n,
        target_partition=target,
        target_dimension=dimension,
        carrier_dimension_cutoff=cutoff,
        low_carrier_count=low_count,
        random_factor_count_per_nonempty_block=random_factor_count_per_block,
        observed_nonantipodal_low_carrier_relative_rank=str(
            observed_nonantipodal
        ),
        predicted_nonantipodal_low_carrier_relative_rank=str(
            predicted_nonantipodal
        ),
        observed_root_antipodal_low_carrier_relative_rank=str(
            observed_antipodal
        ),
        predicted_root_antipodal_low_carrier_relative_rank=str(
            predicted_antipodal
        ),
        exact_nonantipodal_low_carrier_law_verified=nonantipodal_verified,
        exact_root_antipodal_low_carrier_law_verified=antipodal_verified,
        residual_pair_correlation_upper_bound=1 / (cutoff + 1),
        status=(
            "exact-low-carrier-pair-mass-and-root-law-verified"
            if nonantipodal_verified and antipodal_verified
            else "low-carrier-mass-control-failure"
        ),
    )


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def hierarchy_low_carrier_trim_scaling_record(
    n: int,
) -> HierarchyLowCarrierTrimScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    partitions = tuple(integer_partitions(n))
    partition_count = len(partitions)
    copy_count = (order - 1).bit_length() + 2
    orientation_count = 1 << copy_count
    cutoff = canonical_carrier_cutoff(n)
    low_count, low_z2, low_z4 = low_carrier_power_sums(n, cutoff)
    lower, root_nonantipodal, root_antipodal = hierarchy_pair_incidence_formula(
        copy_count
    )
    nonantipodal_count = lower + root_nonantipodal
    unconditioned = (
        Fraction(
            2 * partition_count * nonantipodal_count * low_z4,
            order**3,
        )
        + Fraction(2 * root_antipodal * low_z2, order**2)
    )
    elementary_bound = Fraction(128, partition_count**2) + Fraction(
        8,
        partition_count * math.isqrt(order),
    )
    collision_free_probability = stable_global_collision_free_probability(
        n,
        copy_count,
    )
    if collision_free_probability <= 0:
        raise ArithmeticError("selected scaling n has zero global-distinct mass")
    conditioned = float(unconditioned) / collision_free_probability
    if conditioned < 1:
        simultaneous_threshold = math.sqrt(conditioned)
        simultaneous_failure = simultaneous_threshold
        finite_certified = True
    else:
        simultaneous_threshold = 1.0
        simultaneous_failure = 1.0
        finite_certified = False
    residual_correlation = 1 / (cutoff + 1)
    return HierarchyLowCarrierTrimScalingRecord(
        n=n,
        partition_count=partition_count,
        group_order_decimal=str(order),
        selected_copy_count=copy_count,
        orientation_count_decimal=str(orientation_count),
        carrier_dimension_cutoff_decimal=str(cutoff),
        carrier_dimension_cutoff_log2=math.log2(cutoff),
        low_carrier_count=low_count,
        low_carrier_fourth_power_sum_log2=math.log2(low_z4),
        low_target_second_power_sum_log2=math.log2(low_z2),
        unconditioned_all_target_trim_rank_upper_bound=float(unconditioned),
        unconditioned_all_target_trim_rank_log2=_fraction_log2(unconditioned),
        elementary_asymptotic_upper_bound=float(elementary_bound),
        elementary_asymptotic_upper_bound_log2=_fraction_log2(
            elementary_bound
        ),
        global_distinct_probability=collision_free_probability,
        global_distinct_probability_log2=math.log2(collision_free_probability),
        conditioned_all_target_trim_rank_upper_bound=conditioned,
        conditioned_all_target_trim_rank_log2=math.log2(conditioned),
        simultaneous_relative_trim_threshold=simultaneous_threshold,
        simultaneous_failure_probability_upper_bound=simultaneous_failure,
        residual_pair_correlation_upper_bound=residual_correlation,
        residual_pair_correlation_log2=math.log2(residual_correlation),
        finite_simultaneous_trim_certified=finite_certified,
        asymptotic_vanishing_rank_and_pair_correlation_proved=True,
        high_carrier_frame_edge_proved=False,
        status=(
            "finite-conditioned-low-carrier-trim-certified-high-carrier-edge-open"
            if finite_certified
            else "finite-conditioning-vacuous-asymptotic-tradeoff-proved"
        ),
    )


def run_hierarchy_low_carrier_trim() -> HierarchyLowCarrierTrimReport:
    exact_controls = [
        audit_exact_low_carrier_mass(n, target, cutoff, random_count)
        for n, target, cutoff, random_count in (
            (3, (2, 1), 1, 1),
            (3, (2, 1), 2, 1),
            (4, (3, 1), 2, 2),
            (4, (2, 2), 3, 2),
        )
    ]
    scaling = [
        hierarchy_low_carrier_trim_scaling_record(n)
        for n in (20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(
        not row.exact_nonantipodal_low_carrier_law_verified
        or not row.exact_root_antipodal_low_carrier_law_verified
        for row in exact_controls
    )
    tail = scaling[-1]
    finite = [row for row in scaling if row.finite_simultaneous_trim_certified]
    return HierarchyLowCarrierTrimReport(
        created_at=utc_now(),
        theorem_contract={
            "generic_cutoff_budget": (
                "For any integer L, trimming both endpoint singular spaces "
                "with carrier dimension at most L costs expected all-target "
                "relative rank 2p(n)C_non Z4(L)/|S_n|^3 plus "
                "2C_anti Z2(L)/|S_n|^2."
            ),
            "residual_pair_bound": (
                "Every pair cross map between the surviving leaf subspaces "
                "has norm at most 1/(L+1) by the exact pair-angle spectrum."
            ),
            "canonical_cutoff": (
                "L=floor(|S_n|^(1/4)/p(n)) gives unconditional trim at most "
                "128/p(n)^2+8/(p(n)sqrt(|S_n|)) and residual correlation "
                "O(p(n)/|S_n|^(1/4))."
            ),
            "collision_free_transfer": (
                "Divide the expected target-union trim by P_cf(n,K), then "
                "apply Markov; P_cf tends to one at threshold copy count."
            ),
            "scope_exclusion": (
                "The theorem is a rank--correlation trim. It does not control "
                "signed high-carrier incidence, row sums, spectral edges, PGM "
                "state mass, arbitrary source coupling, or algorithmic success."
            ),
        },
        exact_mass_controls=exact_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "extend_exact_common_trim_to_low_dimensional_carriers",
                "resolved": failures == 0,
                "resolution": (
                    "Sum the exact d_alpha^4/|S_n|^3 active-rank law and "
                    "trim both endpoint singular spaces."
                ),
            },
            {
                "obligation": "classify_root_antipodal_low_carrier_cost",
                "resolved": failures == 0,
                "resolution": (
                    "The root antipode has only carrier alpha=tau and exact "
                    "expected active rank d_tau^2/|S_n|^2."
                ),
            },
            {
                "obligation": "prove_simultaneous_vanishing_rank_and_pair_correlation",
                "resolved": True,
                "resolution": (
                    "The quarter-factorial cutoff makes both the Markov trim "
                    "budget and the residual pair correlation vanish."
                ),
            },
            {
                "obligation": "control_high_carrier_signed_racah_incidence",
                "resolved": False,
                "resolution": (
                    "There are Theta(|S_n|) leaves, so magnitude-only row sums "
                    "remain enormous despite the residual pair bound."
                ),
            },
            {
                "obligation": "prove_collision_free_noncommon_frame_edge",
                "resolved": False,
                "resolution": (
                    "A traffic, center-valued return, or deterministic "
                    "high-carrier cancellation theorem is still required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Trimming only exact common carriers leaves polynomial correlations.",
                "resolved": True,
                "resolution": (
                    "The generalized cutoff removes every carrier through a "
                    "factorial dimension scale while losing vanishing rank."
                ),
            },
            {
                "objection": "Each pair needs a different trim, so coherent overlap invalidates the budget.",
                "resolved": True,
                "resolution": (
                    "The codimension of the intersection of all endpoint "
                    "complements is at most the sum of endpoint dimensions; "
                    "no independence or generic position is assumed."
                ),
            },
            {
                "objection": "The residual pair bound proves the whole frame edge by Gershgorin.",
                "resolved": False,
                "resolution": (
                    "Multiplying O(p(n)/|S_n|^(1/4)) by Theta(|S_n|) leaves "
                    "a divergent magnitude-only row-sum bound."
                ),
            },
            {
                "objection": "The target-union trim is accepted quantum state mass.",
                "resolved": False,
                "resolution": (
                    "It is an unweighted simultaneous-rank device and has no "
                    "proved conversion to PGM probability."
                ),
            },
            {
                "objection": "The quarter exponent is known to be optimal for the natural law.",
                "resolved": False,
                "resolution": (
                    "It is only the limit of the elementary Z4(L)<=p(n)L^4 "
                    "bound; sharper dimension-tail information may improve it."
                ),
            },
        ],
        headline_metrics={
            "exact_low_carrier_mass_control_count": len(exact_controls),
            "finite_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "finite_conditioned_trim_record_count": len(finite),
            "first_finite_conditioned_trim_n": finite[0].n if finite else 0,
            "tail_n": tail.n,
            "tail_cutoff_dimension_log2": tail.carrier_dimension_cutoff_log2,
            "tail_low_carrier_count": tail.low_carrier_count,
            "tail_conditioned_trim_rank_log2": (
                tail.conditioned_all_target_trim_rank_log2
            ),
            "tail_residual_pair_correlation_log2": (
                tail.residual_pair_correlation_log2
            ),
            "all_hierarchy_low_carrier_tradeoff_theorem_count": 1,
            "high_carrier_incidence_theorem_count": 0,
            "natural_node_frame_edge_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_low_carrier_active_rank_law_proved": failures == 0,
            "all_hierarchy_low_carrier_rank_budget_proved": True,
            "quarter_factorial_cutoff_tradeoff_proved": True,
            "collision_free_simultaneous_low_carrier_trim_proved": True,
            "residual_pair_correlation_vanishes": True,
            "arbitrary_source_coupling_covered": False,
            "high_carrier_signed_incidence_controlled": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Low and moderately dimensional carriers can be removed at "
                "vanishing natural rank, but the exponentially wide "
                "high-carrier recoupling problem remains open."
            ),
        },
        status="low-carrier-hierarchy-trim-proved-high-carrier-edge-open",
        summary=(
            "Proved a quarter-factorial rank--correlation tradeoff that trims "
            "all low-dimensional pair carriers throughout the hierarchy."
        ),
        falsifiers_triggered=[
            (
                "Exact-common carriers are not the only sectors that admit a "
                "vanishing-rank hierarchy trim."
            ),
            (
                "Worst-case inverse-(n-1) pair correlations can be removed on "
                "all but vanishing natural rank; they are not the remaining edge bottleneck."
            ),
            (
                "Vanishing pair correlations still do not imply an exponentially "
                "wide frame edge without signed high-order incidence control."
            ),
        ],
    )


def write_hierarchy_low_carrier_trim_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_hierarchy_low_carrier_trim())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_hierarchy_low_carrier_trim_report()
    print(json.dumps(report, indent=2, sort_keys=True))
