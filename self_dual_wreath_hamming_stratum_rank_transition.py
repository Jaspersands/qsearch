"""Sharp natural Hamming-stratum transition for pair-common ranks.

For an orientation pair at Hamming distance ``h``, divide its exact common
rank by the full physical carrier dimension.  The three independent source
membership blocks (left-only, right-only, and shared-with-target) give

    R_(e,f) = X_L^+ X_R^+ X_S^+ + X_L^- X_R^- X_S^-,     (1)

where every ``X`` is a normalized trivial/sign multiplicity.  If a block has
``q>=3`` independent Plancherel source factors, the extended-Kronecker theorem
gives

    |S_n| X -> 1 in probability,
    E[(|S_n|X-1)^2] <= B_q(n),

    B_q(n)=sum_(C!=1)|C|^(2-q)=o(1).                       (2)

Fix ``h>=3`` and assume ``K-h>=3``.  If all six factors in (1) have relative
error at most ``epsilon``, then

    2(1-epsilon)^3 <= |S_n|^3 R_(e,f)
                    <= 2(1+epsilon)^3.                    (3)

A union bound gives pointwise failure at most

    [4 B_h(n) + 2 B_(K-h)(n)] / epsilon^2.                (4)

Now average the bad indicator over every coordinate ``h``-subset and local
orientation choice.  Its expectation obeys (4), regardless of the number of
pairs.  Markov therefore proves that the bad *fraction* of the Hamming-``h``
stratum tends to zero in probability.  Conditioning all source labels
distinct divides the failure by ``P_cf(n,K)=1-o(1)``.

Together with the local transversality theorem, this yields a sharp pair
phase diagram for the independent natural source law:

* Hamming one and two: every pair-common range is absent with probability
  ``1-o(1)`` simultaneously over the source-coordinate relations.
* Every fixed Hamming ``h>=3``: a ``1-o(1)`` fraction of pairs is live and has
  relative rank ``(2+o(1))/|S_n|^3``.
* Balanced Hamming distances: the older pair-core theorem gives the stronger
  simultaneous all-pair concentration with superpolynomially small failure.

The result is a rank-density law, not coherent incidence control.  It does not
bound how the live common spaces align across pairs, the spectrum of the full
projector sum, or the central support of a bad full-node eigenspace.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_pair_common_covering_transition import (
    audit_covering_common_range,
)
from self_dual_wreath_plancherel_kronecker_positivity import centralizer_order


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_hamming_stratum_rank_transition.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HammingStratumScalingRecord:
    n: int
    information_threshold_copy_count: int
    hamming_distance: int
    shared_random_factor_count: int
    relative_error_tolerance: float
    exclusive_block_variance_upper_bound: float
    shared_block_variance_upper_bound: float
    expected_bad_pair_fraction_upper_bound: float
    bad_fraction_markov_threshold: float
    bad_fraction_exceeds_threshold_probability_upper_bound_before_conditioning: float
    conditioned_probability_formula: str
    normalized_pair_rank_lower_bound_on_good_pairs: float
    normalized_pair_rank_upper_bound_on_good_pairs: float
    asymptotic_live_pair_fraction: str
    simultaneous_every_pair_control_proved: bool
    full_frame_edge_proved: bool
    status: str


@dataclass(frozen=True)
class HammingStratumRankTransitionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[dict[str, Any]]
    scaling_records: list[HammingStratumScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def class_variance_upper_bound(n: int, factor_count: int) -> Fraction:
    if n < 3 or factor_count < 3:
        raise ValueError("the variance threshold requires n,q>=3")
    order = math.factorial(n)
    return sum(
        (
            Fraction(
                1,
                (order // centralizer_order(cycle_type))
                ** (factor_count - 2),
            )
            for cycle_type in integer_partitions(n)
            if cycle_type != (1,) * n
        ),
        start=Fraction(),
    )


@lru_cache(maxsize=None)
def _nonidentity_class_sizes(n: int) -> tuple[int, ...]:
    order = math.factorial(n)
    return tuple(
        order // centralizer_order(cycle_type)
        for cycle_type in integer_partitions(n)
        if cycle_type != (1,) * n
    )


def class_variance_upper_bound_float(n: int, factor_count: int) -> float:
    if n < 3 or factor_count < 3:
        raise ValueError("the variance threshold requires n,q>=3")
    exponent = 2 - factor_count
    return math.fsum(
        math.exp(exponent * math.log(class_size))
        for class_size in _nonidentity_class_sizes(n)
    )


def hamming_stratum_scaling_record(
    n: int,
    hamming_distance: int,
    relative_error_tolerance: float = 0.25,
) -> HammingStratumScalingRecord:
    if n < 5 or hamming_distance < 3:
        raise ValueError("scaling requires n>=5 and h>=3")
    if not 0 < relative_error_tolerance < 1:
        raise ValueError("relative error tolerance must lie in (0,1)")
    copy_count = math.ceil(math.lgamma(n + 1) / math.log(2))
    shared_count = copy_count - hamming_distance
    if shared_count < 3:
        raise ValueError("the shared block must have at least three random factors")
    exclusive = class_variance_upper_bound_float(n, hamming_distance)
    shared = class_variance_upper_bound_float(n, shared_count)
    epsilon = relative_error_tolerance
    expected_bad = min(1.0, (4 * exclusive + 2 * shared) / epsilon**2)
    threshold = math.sqrt(expected_bad)
    markov = threshold
    return HammingStratumScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        hamming_distance=hamming_distance,
        shared_random_factor_count=shared_count,
        relative_error_tolerance=epsilon,
        exclusive_block_variance_upper_bound=exclusive,
        shared_block_variance_upper_bound=shared,
        expected_bad_pair_fraction_upper_bound=expected_bad,
        bad_fraction_markov_threshold=threshold,
        bad_fraction_exceeds_threshold_probability_upper_bound_before_conditioning=markov,
        conditioned_probability_formula=(
            "sqrt([4 B_h(n)+2 B_(K-h)(n)]/epsilon^2) / P_cf(n,K)"
        ),
        normalized_pair_rank_lower_bound_on_good_pairs=2 * (1 - epsilon) ** 3,
        normalized_pair_rank_upper_bound_on_good_pairs=2 * (1 + epsilon) ** 3,
        asymptotic_live_pair_fraction="1-o(1)",
        simultaneous_every_pair_control_proved=False,
        full_frame_edge_proved=False,
        status="fixed-hamming-rank-density-one-proved-incidence-open",
    )


def _finite_covering_control() -> dict[str, Any]:
    control = audit_covering_common_range()
    return {
        "n": control.n,
        "hamming_distance": control.hamming_distance,
        "globally_distinct_source_count": control.globally_distinct_source_count,
        "target_count": control.target_count,
        "target_with_common_range_count": control.target_with_common_range_count,
        "minimum_common_range_dimension": control.minimum_common_range_dimension,
        "exact_globally_distinct_hamming_three_witness_verified": (
            control.exact_covering_to_common_range_verified
        ),
    }


def run_hamming_stratum_rank_transition() -> HammingStratumRankTransitionReport:
    controls = [_finite_covering_control()]
    scaling = [
        hamming_stratum_scaling_record(n, distance)
        for n in (10, 20, 30, 40, 50)
        for distance in (3, 4, 5)
    ]
    failures = sum(
        not row["exact_globally_distinct_hamming_three_witness_verified"]
        for row in controls
    )
    verified = failures == 0
    tail_h3 = next(
        row for row in scaling if row.n == 50 and row.hamming_distance == 3
    )
    metrics: dict[str, int | float] = {
        "fixed_hamming_stratum_rank_density_theorem_count": 1,
        "sharp_hamming_pair_support_transition_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "maximum_scaling_n": max(row.n for row in scaling),
        "n50_h3_expected_bad_fraction_upper_bound": (
            tail_h3.expected_bad_pair_fraction_upper_bound
        ),
        "simultaneous_all_fixed_hamming_pair_theorem_count": 0,
        "coherent_incidence_theorem_count": 0,
        "natural_node_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return HammingStratumRankTransitionReport(
        created_at=utc_now(),
        theorem_contract={
            "pair_rank_factorization": (
                "R_ef is the sum of products of six normalized trivial/sign "
                "multiplicity factors over left, right, and shared blocks."
            ),
            "fixed_hamming_density": (
                "For every fixed h>=3 and K-h>=3, a 1-o(1) fraction of the "
                "Hamming-h stratum has |S_n|^3 R_ef=2+o(1)."
            ),
            "sharp_transition": (
                "Hamming one and two are simultaneously transverse with high "
                "probability; every fixed h>=3 is live at density 1-o(1)."
            ),
            "global_distinct_transfer": (
                "Expected bad-fraction Markov bounds divide by P_cf(n,K)=1-o(1)."
            ),
            "scope": (
                "Density-one rank control is not simultaneous every-pair control, "
                "coherent incidence, central-support control, or a frame edge."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "upgrade_fixed_pair_multiplicity_to_hamming_stratum_density",
                "resolved": True,
                "resolution": (
                    "Average the bad indicator before applying Markov; no union "
                    "over exponentially many orientation pairs is needed."
                ),
            },
            {
                "obligation": "locate_sharp_independent_natural_pair_support_transition",
                "resolved": True,
                "resolution": (
                    "The radius-two no-common theorem and q=3 multiplicity law "
                    "place the transition exactly between distances two and three."
                ),
            },
            {
                "obligation": "control_coherent_incidence_of_live_pair_cores",
                "resolved": False,
                "resolution": (
                    "Rank density does not identify principal directions, "
                    "higher intersections, or channel alignment."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Pointwise o(1) failure cannot say anything about a stratum containing exponentially many pairs.",
                "resolved": True,
                "resolution": (
                    "It cannot prove every pair is good, but expectation plus "
                    "Markov proves the bad fraction is o(1)."
                ),
            },
            {
                "objection": "Density-one common ranks force a large projector-sum eigenvalue.",
                "resolved": False,
                "resolution": (
                    "False without alignment: the common ranks are only "
                    "Theta(|S_n|^-3) and may occupy incoherent directions."
                ),
            },
            {
                "objection": "The theorem gives simultaneous control of all Hamming-three pairs.",
                "resolved": False,
                "resolution": (
                    "Only the bad fraction vanishes; rare exceptional pairs are allowed."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "sharp_hamming_one_two_vs_three_support_transition_proved": True,
            "fixed_hamming_at_least_three_live_pair_density_one_proved": True,
            "fixed_hamming_pair_rank_scale_two_over_group_cubed_proved": True,
            "simultaneous_every_fixed_hamming_pair_controlled": False,
            "coherent_pair_core_incidence_controlled": False,
            "full_node_bad_projection_central_support_controlled": False,
            "natural_all_depth_node_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The pair-rank phase diagram is sharp, but the coherent geometry "
                "of the density-one live cores remains unbounded."
            ),
        },
        status=(
            "sharp-hamming-rank-transition-proved-coherent-incidence-open"
            if verified
            else "hamming-stratum-rank-control-failure"
        ),
        summary=(
            "Proved a sharp transition from transverse Hamming radii one/two "
            "to rank-concentrated live strata at every fixed radius at least three."
        ),
        falsifiers_triggered=[
            "Exponential stratum size blocks all-pair union bounds but not density statements.",
            "Pair-common rank density does not determine coherent incidence or a frame edge.",
            "The natural independent support threshold is exactly three, not an unspecified covering radius.",
        ],
    )


def write_hamming_stratum_rank_transition_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_hamming_stratum_rank_transition())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    return payload


if __name__ == "__main__":
    report = write_hamming_stratum_rank_transition_report()
    print(json.dumps(report, indent=2))
