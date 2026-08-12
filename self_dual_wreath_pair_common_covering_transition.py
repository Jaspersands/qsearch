"""Constant-Hamming transition from transversality to common ranges.

The local-pair theorem proves natural transversality at Hamming distances one
and two.  It cannot extend through every fixed radius.

Sellke proves that there is a fixed integer ``k_cov`` such that the tensor
product of ``k_cov`` arbitrarily coupled Plancherel-random ``S_n`` irreps
covers every irrep with probability ``1-o(1)``.  Consider a fixed orientation
pair at Hamming distance ``h`` with

    h >= k_cov,   K-h >= k_cov.

The left-only, right-only, and shared source clusters each contain a
``k_cov``-factor subproduct.  With high probability all three cover every
irrep.  Tensoring extra factors, including the fixed target irrep in the
shared cluster, preserves covering.  Hence the common-range formula has both
trivial- and sign-mediated contributions.  Global-distinct conditioning
preserves the result because its probability tends to one.

Distance three is the first nontrivial boundary.  An exclusive three-label
cluster contains the trivial representation exactly when its ordinary
Kronecker coefficient is positive.  The later
``self_dual_wreath_plancherel_kronecker_positivity`` theorem proves this with
probability ``1-o(1)`` for *independent Plancherel* triples by an exact
character-variance argument.  Sellke's stronger arbitrarily coupled
Plancherel and uniformly random partition versions remain open.

An exact globally distinct ``S_7`` control shows the mechanism is nonvacuous.
Nine distinct source irreps split into three disjoint triples, each of whose
tensor product covers all fifteen irreps of ``S_7``.  Using them as left-only,
right-only, and shared clusters yields a Hamming-three common range for every
target, with both trivial and sign contributions.

Pair-common ranges returning at constant radius do not imply a large averaged
frame norm.  Random-subspace Marchenko--Pastur behavior itself permits many
low-rank intersections.  This theorem cuts only strategies requiring all
fixed-radius pair products to be small and redirects the edge problem toward
higher-order incidence, central support, and multiplicity/rank distribution.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_orientation_common_range import (
    common_range_multiplicity_components,
)
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_common_covering_transition.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SELLKE_COVERING_URL = "https://arxiv.org/abs/2004.05283"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class CoveringCommonRangeControl:
    n: int
    copy_count: int
    hamming_distance: int
    globally_distinct_source_count: int
    partition_count: int
    left_only_cluster_covers_all_irreps: bool
    right_only_cluster_covers_all_irreps: bool
    shared_source_cluster_covers_all_irreps: bool
    target_count: int
    target_with_common_range_count: int
    target_with_trivial_contribution_count: int
    target_with_sign_contribution_count: int
    minimum_common_range_dimension: int
    exact_covering_to_common_range_verified: bool
    status: str


@dataclass(frozen=True)
class PairCommonCoveringTransitionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CoveringCommonRangeControl]
    asymptotic_transition: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support(n: int, factors: tuple[Partition, ...]) -> set[Partition]:
    return {
        partition
        for partition, multiplicity in tensor_product_multiplicities(factors, n)
        if multiplicity
    }


def _s7_covering_control_labels() -> tuple[tuple[Label, ...], tuple[Partition, ...]]:
    left_only = ((6, 1), (5, 1, 1), (4, 1, 1, 1))
    right_only = ((5, 2), (4, 3), (4, 2, 1))
    shared = ((3, 3, 1), (3, 2, 2), (3, 2, 1, 1))
    used = set(left_only + right_only + shared)
    companions = tuple(
        partition for partition in integer_partitions(7) if partition not in used
    )[:3]
    labels: tuple[Label, ...] = (
        *tuple(zip(left_only, right_only)),
        *tuple(zip(shared, companions)),
    )
    return labels, companions


def audit_covering_common_range() -> CoveringCommonRangeControl:
    n = 7
    partitions = tuple(integer_partitions(n))
    full = set(partitions)
    labels, _ = _s7_covering_control_labels()
    source = tuple(partition for label in labels for partition in label)
    if len(source) != len(set(source)):
        raise ArithmeticError("the S7 covering control must be globally distinct")
    left_only = tuple(label[0] for label in labels[:3])
    right_only = tuple(label[1] for label in labels[:3])
    shared = tuple(label[0] for label in labels[3:])
    left_covers = _support(n, left_only) == full
    right_covers = _support(n, right_only) == full
    shared_covers = _support(n, shared) == full
    totals = []
    trivial_count = 0
    sign_count = 0
    for target in partitions:
        total, trivial, sign = common_range_multiplicity_components(
            target,
            labels,
            0,
            0b111,
        )
        totals.append(total)
        trivial_count += trivial > 0
        sign_count += sign > 0
    verified = bool(
        left_covers
        and right_covers
        and shared_covers
        and all(total > 0 for total in totals)
        and trivial_count == len(partitions)
        and sign_count == len(partitions)
    )
    return CoveringCommonRangeControl(
        n=n,
        copy_count=len(labels),
        hamming_distance=3,
        globally_distinct_source_count=len(source),
        partition_count=len(partitions),
        left_only_cluster_covers_all_irreps=left_covers,
        right_only_cluster_covers_all_irreps=right_covers,
        shared_source_cluster_covers_all_irreps=shared_covers,
        target_count=len(partitions),
        target_with_common_range_count=sum(total > 0 for total in totals),
        target_with_trivial_contribution_count=trivial_count,
        target_with_sign_contribution_count=sign_count,
        minimum_common_range_dimension=min(totals),
        exact_covering_to_common_range_verified=verified,
        status=(
            "exact-globally-distinct-covering-common-range-verified"
            if verified
            else "covering-common-range-control-failure"
        ),
    )


def run_pair_common_covering_transition() -> PairCommonCoveringTransitionReport:
    controls = [audit_covering_common_range()]
    failures = sum(
        not row.exact_covering_to_common_range_verified for row in controls
    )
    verified = failures == 0
    control = controls[0]
    metrics: dict[str, int | float] = {
        "sellke_constant_covering_transition_theorem_count": 1,
        "hamming_three_kronecker_positivity_reduction_theorem_count": 1,
        "finite_covering_control_count": len(controls),
        "finite_covering_control_failure_count": failures,
        "finite_target_with_common_range_count": (
            control.target_with_common_range_count
        ),
        "independent_plancherel_hamming_three_positivity_theorem_count": 1,
        "arbitrarily_coupled_hamming_three_positivity_theorem_count": 0,
        "natural_node_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PairCommonCoveringTransitionReport(
        created_at=utc_now(),
        theorem_contract={
            "covering_transition": (
                "Sellke's fixed k_cov covering theorem implies common ranges "
                "with probability 1-o(1) at every fixed h>=k_cov with K-h>=k_cov."
            ),
            "global_distinct_transfer": (
                "The conclusion survives conditioning because P_cf(n,K)=1-o(1)."
            ),
            "hamming_three_boundary": (
                "At h=3, each exclusive trivial sector is an ordinary "
                "Kronecker coefficient; independent Plancherel positivity is "
                "proved by the later variance module, while stronger laws remain open."
            ),
            "finite_witness": (
                "Three disjoint globally distinct S7 triples each cover all "
                "irreps and give common ranges for all targets."
            ),
            "scope": (
                "Pair-common recurrence does not prove a large frame norm, "
                "a failed local law, or the absence/presence of a speedup."
            ),
        },
        finite_controls=controls,
        asymptotic_transition={
            "hamming_one_natural_common_range_probability": "o(1)",
            "hamming_two_natural_common_range_probability": "o(1)",
            "hamming_three_natural_common_range_probability": (
                "1-o(1) for independent Plancherel sources; arbitrary coupling open"
            ),
            "some_fixed_hamming_radius_common_range_probability": "1-o(1)",
            "sellke_covering_constant_explicitly_needed_for_logic": False,
            "all_fixed_radius_pair_products_small": False,
        },
        proof_obligations=[
            {
                "obligation": "show_pair_common_ranges_return_at_constant_hamming_radius",
                "resolved": True,
                "resolution": (
                    "Apply Sellke covering independently to left-only, right-only, "
                    "and a fixed-size subproduct of the shared source cluster."
                ),
            },
            {
                "obligation": "identify_the_first_unresolved_hamming_stratum",
                "resolved": True,
                "resolution": (
                    "Distance three is governed by positivity of ordinary "
                    "Kronecker coefficients for random Plancherel triples."
                ),
            },
            {
                "obligation": "resolve_independent_plancherel_ordinary_kronecker_positivity",
                "resolved": True,
                "resolution": (
                    "The later Plancherel Kronecker module bounds zero probability "
                    "by a vanishing reciprocal conjugacy-class sum."
                ),
            },
            {
                "obligation": "extend_hamming_three_positivity_to_arbitrary_coupling_or_uniform_partitions",
                "resolved": False,
                "resolution": (
                    "The variance proof requires independent Plancherel character moments."
                ),
            },
            {
                "obligation": "control_rank_and_incidence_of_returning_pair_common_sectors",
                "resolved": False,
                "resolution": (
                    "Need multiplicity/rank distributions and higher-order "
                    "overlap geometry, not merely support positivity."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Radius-two transversality should extend to every fixed radius.",
                "resolved": True,
                "resolution": (
                    "False: Sellke covering forces common ranges by some fixed radius."
                ),
            },
            {
                "objection": "Sellke alone proves typical Hamming-three common ranges.",
                "resolved": True,
                "resolution": (
                    "False: the independent Plancherel case needs the later "
                    "variance theorem; stronger coupling laws remain open."
                ),
            },
            {
                "objection": "Common pair ranges imply the average projector has a macroscopic edge.",
                "resolved": False,
                "resolution": (
                    "No: support, rank, alignment across pairs, and higher "
                    "incidence determine the frame edge."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Sellke, Covering Irrep(S_n) With Tensor Products and Powers",
                "url": SELLKE_COVERING_URL,
                "directly_applies": True,
                "reason": (
                    "Theorem 1.2 supplies a fixed covering radius; the paper "
                    "also explicitly identifies ordinary typical Kronecker positivity as open."
                ),
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "constant_hamming_pair_common_recurrence_proved": True,
            "hamming_three_reduced_to_typical_kronecker_positivity": True,
            "independent_plancherel_hamming_three_common_range_proved": True,
            "arbitrarily_coupled_hamming_three_common_range_proved": False,
            "pair_common_rank_distribution_proved": False,
            "higher_order_incidence_controlled": False,
            "natural_all_depth_node_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pair support undergoes a constant-radius transition, but its "
                "rank and coherent higher-order incidence remain unknown."
            ),
        },
        status=(
            "independent-plancherel-hamming-three-and-constant-radius-common-proved"
            if verified
            else "pair-common-covering-control-failure"
        ),
        summary=(
            "Proved that pair-common ranges return at a fixed Hamming radius; "
            "the later variance theorem resolves distance three for independent Plancherel sources."
        ),
        falsifiers_triggered=[
            "Natural pairwise transversality cannot hold through every fixed Hamming radius.",
            "Sellke's theorem alone does not resolve ordinary three-factor Kronecker positivity; the independent Plancherel variance theorem does.",
            "Pair-common support alone is not a spectral-edge obstruction.",
        ],
    )


def write_pair_common_covering_transition_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_pair_common_covering_transition())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    return payload


if __name__ == "__main__":
    report = write_pair_common_covering_transition_report()
    print(json.dumps(report, indent=2))
