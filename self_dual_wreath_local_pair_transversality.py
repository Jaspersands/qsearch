"""Natural source-level transversality through Hamming radius two.

For two orientation projectors at Hamming distance ``h``, their common range
is controlled by the tensor products of the source irreps selected only on
the left and only on the right.

At ``h=1`` those two membership blocks are singleton irreps.  A common range
therefore forces the two labels of that source pair to be the one-dimensional
trivial and sign irreps under global distinctness.  Across ``K`` source pairs,
the independent Plancherel numerator is at most

    2K / |S_n|^2.                                          (1)

At ``h=2`` each exclusive membership block contains two irreps.  For
irreducible ``S_n`` modules,

    mult_1(lambda tensor mu)   = 1[mu=lambda],
    mult_sgn(lambda tensor mu) = 1[mu=lambda^t].

Global distinctness removes the first case.  The second case requires the
four labels in the two source pairs to form two conjugate matches, in one of
two alignments.  If

    C_n = sum_lambda p_lambda^2

is the Plancherel collision probability, the all-coordinate numerator is at
most

    2 binom(K,2) C_n^2.                                    (2)

Conditioning on global distinctness divides (1) and (2) by ``P_cf(n,K)``.
The maximal-dimension theorem implies ``C_n<=max p_lambda =
exp(-Theta(sqrt(n)))``, while ``K=Theta(n log n)`` and ``P_cf=1-o(1)``.
Consequently, with probability ``1-o(1)``, every physical orientation pair
at Hamming distance one or two has zero common range.  The exact wreath
pair-angle theorem then bounds its projector-product norm by ``1/(n-1)`` for
``n>=5``.

This is only local geometry.  Radius-two transversality does not bound the
sum of exponentially many projectors: distant orientation pairs can have
large common ranges, and abstract parity/code constructions can have perfect
local transversality but a macroscopic average-projector norm.  A viable next
step needs a higher-order/nonbacktracking theorem using the tensor-product
structure, not a claim that (1)-(2) prove the natural frame edge.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import perfect_matchings
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_natural_unequal_dominance import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
)
from self_dual_wreath_orientation_common_range import (
    common_range_multiplicity_components,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_local_pair_transversality.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class LocalPairFormulaControl:
    n: int
    globally_distinct_label_tuple_count: int
    target_count: int
    orientation_pair_count: int
    hamming_one_pair_count: int
    hamming_two_pair_count: int
    common_hamming_one_pair_count: int
    common_hamming_two_pair_count: int
    hamming_one_necessity_violation_count: int
    hamming_two_necessity_violation_count: int
    exact_local_necessity_verified: bool
    status: str


@dataclass(frozen=True)
class LocalTransversalityScalingRecord:
    n: int
    group_order_log2: float
    information_threshold_copy_count: int
    plancherel_collision_probability: float
    hamming_one_any_coordinate_numerator_upper_bound: float
    hamming_one_any_coordinate_numerator_log2: float
    hamming_two_any_coordinate_numerator_upper_bound: float
    hamming_two_any_coordinate_numerator_log2: float
    conditioned_union_bound_formula: str
    asymptotic_hamming_radius_two_transversality: bool
    noncommon_pair_product_norm_upper_bound: float
    full_node_frame_edge_proved: bool
    status: str


@dataclass(frozen=True)
class LocalPairTransversalityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[LocalPairFormulaControl]
    scaling_records: list[LocalTransversalityScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hamming_distance(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def _one_dimensional_pair_condition(label: Label, n: int) -> bool:
    return set(label) == {(n,), (1,) * n}


def _conjugate(partition: Partition) -> Partition:
    return tuple(
        sum(row > column for row in partition)
        for column in range(partition[0])
    )


def _two_pair_conjugate_matching_condition(
    labels: tuple[Label, Label],
) -> bool:
    (left_a, left_b), (right_a, right_b) = labels
    return (
        _conjugate(left_a) == right_a
        and _conjugate(left_b) == right_b
    ) or (
        _conjugate(left_a) == right_b
        and _conjugate(left_b) == right_a
    )


def audit_local_pair_formula(n: int = 4) -> LocalPairFormulaControl:
    if n != 4:
        raise ValueError("the complete formula control uses S4")
    partitions = tuple(integer_partitions(n))
    label_tuples = tuple(
        labels
        for subset in itertools.combinations(partitions, 4)
        for labels in perfect_matchings(subset)
    )
    orientations = tuple(range(4))
    pair_count = 0
    hamming_one = 0
    hamming_two = 0
    common_one = 0
    common_two = 0
    violations_one = 0
    violations_two = 0
    for labels in label_tuples:
        for target in partitions:
            for left, right in itertools.combinations(orientations, 2):
                distance = _hamming_distance(left, right)
                common, _, _ = common_range_multiplicity_components(
                    target,
                    labels,
                    left,
                    right,
                )
                pair_count += 1
                if distance == 1:
                    coordinate = (left ^ right).bit_length() - 1
                    condition = _one_dimensional_pair_condition(
                        labels[coordinate], n
                    )
                    hamming_one += 1
                    common_one += common > 0
                    violations_one += bool(common > 0 and not condition)
                elif distance == 2:
                    condition = _two_pair_conjugate_matching_condition(labels)
                    hamming_two += 1
                    common_two += common > 0
                    violations_two += bool(common > 0 and not condition)
                else:
                    raise ArithmeticError("the two-cube has only distances one and two")
    verified = violations_one == 0 and violations_two == 0
    return LocalPairFormulaControl(
        n=n,
        globally_distinct_label_tuple_count=len(label_tuples),
        target_count=len(partitions),
        orientation_pair_count=pair_count,
        hamming_one_pair_count=hamming_one,
        hamming_two_pair_count=hamming_two,
        common_hamming_one_pair_count=common_one,
        common_hamming_two_pair_count=common_two,
        hamming_one_necessity_violation_count=violations_one,
        hamming_two_necessity_violation_count=violations_two,
        exact_local_necessity_verified=verified,
        status=(
            "exact-radius-two-common-range-necessity-verified"
            if verified
            else "radius-two-common-range-necessity-failure"
        ),
    )


def local_transversality_scaling_record(n: int) -> LocalTransversalityScalingRecord:
    if n < 5:
        raise ValueError("the pair-angle corollary uses n>=5")
    group_order = math.factorial(n)
    log2_group = math.lgamma(n + 1) / math.log(2)
    copy_count = math.ceil(log2_group)
    weights = plancherel_weights(n)
    collision = float(sum(weight * weight for weight in weights))
    hamming_one_log2 = math.log2(2 * copy_count) - 2 * log2_group
    hamming_one = 2.0**hamming_one_log2
    hamming_two = 2 * math.comb(copy_count, 2) * collision**2
    hamming_two_log2 = math.log2(hamming_two) if hamming_two else -math.inf
    return LocalTransversalityScalingRecord(
        n=n,
        group_order_log2=log2_group,
        information_threshold_copy_count=copy_count,
        plancherel_collision_probability=collision,
        hamming_one_any_coordinate_numerator_upper_bound=hamming_one,
        hamming_one_any_coordinate_numerator_log2=hamming_one_log2,
        hamming_two_any_coordinate_numerator_upper_bound=hamming_two,
        hamming_two_any_coordinate_numerator_log2=hamming_two_log2,
        conditioned_union_bound_formula=(
            "[2K/|S_n|^2 + 2 binom(K,2) C_n^2] / P_cf(n,K)"
        ),
        asymptotic_hamming_radius_two_transversality=True,
        noncommon_pair_product_norm_upper_bound=1 / (n - 1),
        full_node_frame_edge_proved=False,
        status="radius-two-natural-transversality-proved-global-edge-open",
    )


def run_local_pair_transversality() -> LocalPairTransversalityReport:
    controls = [audit_local_pair_formula()]
    scaling = [
        local_transversality_scaling_record(n) for n in (5, 8, 12, 16, 20)
    ]
    failures = sum(not row.exact_local_necessity_verified for row in controls)
    verified = failures == 0
    metrics: dict[str, int | float] = {
        "hamming_one_common_range_necessity_theorem_count": 1,
        "hamming_two_common_range_necessity_theorem_count": 1,
        "asymptotic_radius_two_transversality_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "maximum_scaling_n": max(row.n for row in scaling),
        "higher_order_incidence_theorem_count": 0,
        "natural_node_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return LocalPairTransversalityReport(
        created_at=utc_now(),
        theorem_contract={
            "hamming_one": (
                "Global-distinct common range forces the varying pair to be "
                "the ordered trivial/sign labels; all-coordinate numerator <=2K/|S_n|^2."
            ),
            "hamming_two": (
                "Global-distinct common range forces two conjugate matchings; "
                "all-coordinate numerator <=2 binom(K,2) C_n^2."
            ),
            "asymptotic": (
                "C_n<=exp(-Theta(sqrt(n))), K=Theta(n log n), and P_cf=1-o(1) "
                "give simultaneous radius-two transversality with probability 1-o(1)."
            ),
            "pair_norm": (
                "On that event the exact noncommon pair-angle theorem gives "
                "||E_e E_f||<=1/(n-1) for Hamming distance at most two."
            ),
            "scope": (
                "No distant-pair, higher-order incidence, full-frame edge, "
                "center-valued local law, or speedup theorem follows."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "classify_global_distinct_common_ranges_at_hamming_one_and_two",
                "resolved": verified,
                "resolution": (
                    "One-factor invariants force trivial/sign; two-factor "
                    "invariants force equality or conjugacy, and distinctness removes equality."
                ),
            },
            {
                "obligation": "prove_simultaneous_natural_radius_two_transversality",
                "resolved": verified,
                "resolution": (
                    "Union over source coordinates, not orientation pairs, gives "
                    "the stated factorial and collision-probability bounds."
                ),
            },
            {
                "obligation": "convert_local_transversality_to_natural_full_frame_edge",
                "resolved": False,
                "resolution": (
                    "Need a higher-order/nonbacktracking theorem that uses the "
                    "specific tensor representation and controls distant common sectors."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "There are exponentially many orientation pairs, so the union bound is useless.",
                "resolved": True,
                "resolution": (
                    "The bad conditions are source-coordinate relations shared "
                    "by all such pairs; only K and binom(K,2) events are unioned."
                ),
            },
            {
                "objection": "Radius-two transversality proves the full average-projector norm.",
                "resolved": False,
                "resolution": (
                    "False: distant pairs are uncontrolled, and local overlap "
                    "graphs alone admit macroscopic coherent sectors."
                ),
            },
            {
                "objection": "The finite S4 formula screen proves the asymptotic probability bound.",
                "resolved": True,
                "resolution": (
                    "The probability theorem is analytic from Plancherel weights, "
                    "conjugacy, the maximal-dimension bound, and P_cf=1-o(1)."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "directly_applies": True,
                "reason": (
                    "Its maximal Plancherel atom bound implies C_n is "
                    "exp(-Theta(sqrt(n))), making the Hamming-two union vanish."
                ),
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "radius_two_common_range_conditions_classified": verified,
            "natural_global_distinct_radius_two_transversality_proved": verified,
            "radius_two_noncommon_pair_norm_bound_proved": verified,
            "distant_pair_common_support_controlled": False,
            "higher_order_incidence_expansion_proved": False,
            "natural_all_depth_node_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural blocks are locally transverse through radius two, but "
                "the exponentially large distant-pair geometry remains open."
            ),
        },
        status=(
            "natural-radius-two-transversality-proved-global-edge-open"
            if verified
            else "local-pair-transversality-control-failure"
        ),
        summary=(
            "Proved that globally distinct natural source blocks are "
            "simultaneously transverse through Hamming radius two with high probability."
        ),
        falsifiers_triggered=[
            "Unioning over orientation pairs ignores that common-range conditions are shared source-label relations.",
            "The full regular pair-common obstruction is not typical at Hamming radii one and two.",
            "Local transversality alone does not control the full orientation-frame edge.",
        ],
    )


def write_local_pair_transversality_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_local_pair_transversality())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_local_pair_transversality_report()
    print(json.dumps(report, indent=2))
