"""No-go theorem for orthogonal affine-plane channel atomization.

The finite vertex audits show disjoint positive affine triangles.  That pattern
cannot persist at information-threshold width.

Let ``g=|S_n|``, ``N=2^K``, and fix the full orientation cube.  A rich affine
plane is one whose two direction vectors realize all four coordinate patterns.
The exact number through each vertex is

    R_K=(4^K-4*3^K+6*2^K-4)/6.                           (1)

For every vertex-plane, choose one of its shared-vertex star overlaps.  The
exact independent-Plancherel star law gives expected noncommon support rank,
relative to the physical ambient dimension,

    4 (Z_4(n)^2-4)/g^7,   Z_4=sum_alpha d_alpha^4.        (2)

The factor four is the isotype-bit pair; subtracting four removes the pairs
of one-dimensional carriers whose correlation is one.

There are ``N R_K`` vertex-planes.  The total expected support *demand* is
therefore

    D = N R_K 4(Z_4^2-4)/g^7.                            (3)

The total incident pair-core capacity counts every pair core at both
endpoints.  Non-antipodal pairs have exact expected relative rank ``2/g^3``.
Root antipodes contribute only for a one-dimensional target, so uniformly in
the target

    C <= 2N(N-2)/g^3 + N/g^2.                            (4)

If supports belonging to distinct affine planes were orthogonal inside every
incident pair core, deterministically ``D_sample<=C_sample``.  But the exact
annealed pressure ratio from (3)-(4) is

    P_n = 4 R_K (Z_4^2-4)
          / [g^4 (2(N-2)+g)],                            (5)

and ``Z_4/g^2>=1/p(n)``.  At
``K=ceil(log_2 g)+2``, equation (5) is
``Omega(g/p(n)^2)`` and diverges factorially.

This is not merely an artifact of repeated labels.  The existing star-channel
relative-concentration theorem transfers a density-one good-triple event to
the globally distinct law.  The total pair-core capacity has a conditional
one-sided Markov bound obtained by dividing (4) by ``P_cf=1-o(1)``.  Choosing
Markov slack ``sqrt(P_n)`` still leaves demand/capacity ratio
``sqrt(P_n)->infinity``.  Hence mutually orthogonal distinct-plane supports
fail with probability tending to one in the collision-free natural law.

The result does not imply a bad spectral edge.  Overlapping positive plane
channels may form a well-conditioned association scheme, expander, or
approximately free traffic law.  It only kills the simpler clique-atom proof
strategy and identifies matrix-valued overlap traffic as mandatory.
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


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_affine_plane_support_pressure_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RichAffinePlaneCountControl:
    copy_count: int
    orientation_count: int
    enumerated_rich_plane_count_per_vertex: int
    predicted_rich_plane_count_per_vertex: int
    exact_rich_plane_count_verified: bool
    status: str


@dataclass(frozen=True)
class AffinePlaneSupportPressureScalingRecord:
    n: int
    group_order_decimal: str
    partition_count: int
    selected_copy_count: int
    orientation_count_decimal: str
    rich_plane_count_per_vertex_decimal: str
    fourth_power_normalization_log2: float
    plancherel_collision_probability_log2: float
    annealed_noncommon_support_demand_log2: float
    worst_target_pair_core_capacity_log2: float
    exact_pressure_ratio: float
    exact_pressure_ratio_log2: float
    elementary_pressure_ratio_lower_bound: float
    elementary_pressure_ratio_lower_bound_log2: float
    markov_slack_log2: float
    residual_pressure_after_markov_slack_log2: float
    pressure_exceeds_capacity: bool
    asymptotic_collision_free_orthogonal_plane_atomization_falsified: bool
    overlapping_plane_traffic_controlled: bool
    status: str


@dataclass(frozen=True)
class AffinePlaneSupportPressureNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_plane_count_controls: list[RichAffinePlaneCountControl]
    scaling_records: list[AffinePlaneSupportPressureScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def rich_plane_count_per_vertex(copy_count: int) -> int:
    if copy_count < 2:
        return 0
    surjections = (
        4**copy_count
        - 4 * 3**copy_count
        + 6 * 2**copy_count
        - 4
    )
    if surjections % 6:
        raise ArithmeticError("ordered rich direction count must divide by six")
    return surjections // 6


def enumerate_rich_planes_through_zero(copy_count: int) -> int:
    if copy_count < 2:
        return 0
    orientations = range(1 << copy_count)
    planes: set[tuple[int, int, int, int]] = set()
    for first, second in itertools.combinations(orientations, 2):
        if first == 0 or second == 0 or first == second:
            continue
        plane = tuple(sorted((0, first, second, first ^ second)))
        if len(set(plane)) != 4:
            continue
        signatures = {
            ((first >> coordinate) & 1, (second >> coordinate) & 1)
            for coordinate in range(copy_count)
        }
        if len(signatures) == 4:
            planes.add(plane)
    return len(planes)


def audit_rich_affine_plane_count(
    copy_count: int,
) -> RichAffinePlaneCountControl:
    observed = enumerate_rich_planes_through_zero(copy_count)
    predicted = rich_plane_count_per_vertex(copy_count)
    verified = observed == predicted
    return RichAffinePlaneCountControl(
        copy_count=copy_count,
        orientation_count=1 << copy_count,
        enumerated_rich_plane_count_per_vertex=observed,
        predicted_rich_plane_count_per_vertex=predicted,
        exact_rich_plane_count_verified=verified,
        status=(
            "exact-rich-affine-plane-count-verified"
            if verified
            else "rich-affine-plane-count-control-failure"
        ),
    )


def fourth_power_normalization(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return sum(
        hook_length_dimension(partition) ** 4
        for partition in integer_partitions(n)
    )


def support_pressure_components(
    n: int,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Return demand, capacity, exact ratio, and elementary ratio lower bound."""

    if n < 3:
        raise ValueError("n must be at least three")
    group_order = math.factorial(n)
    partition_count = len(tuple(integer_partitions(n)))
    copy_count = (group_order - 1).bit_length() + 2
    orientation_count = 1 << copy_count
    rich_planes = rich_plane_count_per_vertex(copy_count)
    z4 = fourth_power_normalization(n)
    demand = Fraction(
        4 * orientation_count * rich_planes * (z4**2 - 4),
        group_order**7,
    )
    # Uniform target upper bound includes root antipodes for a 1D target.
    capacity = (
        Fraction(
            2 * orientation_count * (orientation_count - 2),
            group_order**3,
        )
        + Fraction(orientation_count, group_order**2)
    )
    ratio = demand / capacity
    lower_numerator = Fraction(1, partition_count**2) - Fraction(
        4,
        group_order**4,
    )
    lower = Fraction(
        4 * rich_planes,
        2 * (orientation_count - 2) + group_order,
    ) * lower_numerator
    return demand, capacity, ratio, lower


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def affine_plane_support_pressure_scaling_record(
    n: int,
) -> AffinePlaneSupportPressureScalingRecord:
    group_order = math.factorial(n)
    partitions = tuple(integer_partitions(n))
    partition_count = len(partitions)
    copy_count = (group_order - 1).bit_length() + 2
    orientation_count = 1 << copy_count
    rich_planes = rich_plane_count_per_vertex(copy_count)
    z4 = fourth_power_normalization(n)
    demand, capacity, ratio, lower = support_pressure_components(n)
    slack_log2 = _fraction_log2(lower) / 2
    return AffinePlaneSupportPressureScalingRecord(
        n=n,
        group_order_decimal=str(group_order),
        partition_count=partition_count,
        selected_copy_count=copy_count,
        orientation_count_decimal=str(orientation_count),
        rich_plane_count_per_vertex_decimal=str(rich_planes),
        fourth_power_normalization_log2=math.log2(z4),
        plancherel_collision_probability_log2=(
            math.log2(z4) - 2 * math.log2(group_order)
        ),
        annealed_noncommon_support_demand_log2=_fraction_log2(demand),
        worst_target_pair_core_capacity_log2=_fraction_log2(capacity),
        exact_pressure_ratio=float(ratio),
        exact_pressure_ratio_log2=_fraction_log2(ratio),
        elementary_pressure_ratio_lower_bound=float(lower),
        elementary_pressure_ratio_lower_bound_log2=_fraction_log2(lower),
        markov_slack_log2=slack_log2,
        residual_pressure_after_markov_slack_log2=slack_log2,
        pressure_exceeds_capacity=ratio > 1,
        asymptotic_collision_free_orthogonal_plane_atomization_falsified=True,
        overlapping_plane_traffic_controlled=False,
        status=(
            "affine-plane-orthogonal-support-pressure-no-go"
            if ratio > 1
            else "finite-pressure-below-capacity-asymptotic-no-go-proved"
        ),
    )


def run_affine_plane_support_pressure_no_go(
) -> AffinePlaneSupportPressureNoGoReport:
    plane_controls = [
        audit_rich_affine_plane_count(copy_count)
        for copy_count in range(2, 9)
    ]
    scaling = [
        affine_plane_support_pressure_scaling_record(n)
        for n in (5, 6, 7, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48)
    ]
    failures = sum(
        not row.exact_rich_plane_count_verified for row in plane_controls
    )
    pressure_failures = sum(not row.pressure_exceeds_capacity for row in scaling)
    tail = scaling[-1]
    return AffinePlaneSupportPressureNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "rich_plane_count": (
                "Each vertex lies in exactly "
                "(4^K-4*3^K+6*2^K-4)/6 affine planes whose four coordinate "
                "patterns are all nonempty."
            ),
            "noncommon_plane_demand": (
                "One rich vertex-plane star overlap has exact annealed "
                "noncommon support rank 4(Z4^2-4)/|S_n|^7 relative to ambient."
            ),
            "incident_core_capacity": (
                "The expected total incident pair-core capacity is at most "
                "2N(N-2)/|S_n|^3+N/|S_n|^2 for every fixed target."
            ),
            "pressure_no_go": (
                "Demand/capacity is Omega(N/p(n)^2) and diverges at threshold "
                "width, so distinct affine-plane supports cannot remain "
                "orthogonal."
            ),
            "collision_free_transfer": (
                "Star multiplicity relative concentration supplies a "
                "density-one conditioned demand lower bound; conditional "
                "Markov controls capacity with sqrt(pressure) slack, leaving "
                "a divergent residual ratio."
            ),
            "scope_exclusion": (
                "The theorem falsifies orthogonal plane atomization, not the "
                "natural frame edge. Overlapping channels may still have "
                "favorable signed traffic or resolvent comparison."
            ),
        },
        exact_plane_count_controls=plane_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "count_pattern_rich_affine_planes_exactly",
                "resolved": failures == 0,
                "resolution": (
                    "Inclusion-exclusion counts ordered surjections onto four "
                    "coordinate signatures; divide by six ordered plane bases."
                ),
            },
            {
                "obligation": "compare_plane_support_demand_to_pair_core_capacity",
                "resolved": pressure_failures == 0,
                "resolution": (
                    "Exact star and pair-core annealed rank laws give equation "
                    "(5), already above one in every scaling row."
                ),
            },
            {
                "obligation": "transfer_support_pressure_to_collision_free_natural_law",
                "resolved": True,
                "resolution": (
                    "Use the proved relative multiplicity event for density-one "
                    "triples and a one-sided conditional Markov capacity bound."
                ),
            },
            {
                "obligation": "control_overlapping_affine_plane_channel_traffic",
                "resolved": False,
                "resolution": (
                    "The no-go proves overlap is extensive but does not classify "
                    "the resulting matrix-valued association scheme."
                ),
            },
            {
                "obligation": "prove_collision_free_noncommon_frame_edge",
                "resolved": False,
                "resolution": (
                    "Need a center-valued return, traffic, or resolvent theorem "
                    "for the necessarily overlapping high-carrier channels."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Finite S6 and S7 affine triangles support disjoint atomization all-depth.",
                "resolved": True,
                "resolution": (
                    "Their regime is pre-asymptotic. Exact threshold support "
                    "demand exceeds available pair-core dimension by a "
                    "factor growing at least as n!/p(n)^2."
                ),
            },
            {
                "objection": "The pressure is caused only by repeated source labels.",
                "resolved": True,
                "resolution": (
                    "The star relative-concentration event and portfolio "
                    "conversion hold after global-distinct conditioning."
                ),
            },
            {
                "objection": "Pairwise support ranks can be summed even when the supports overlap.",
                "resolved": True,
                "resolution": (
                    "They are summed as demand precisely to contradict the "
                    "hypothesis that distinct-plane supports are orthogonal; "
                    "no rank claim is made after overlap is forced."
                ),
            },
            {
                "objection": "Extensive channel overlap implies bad conditioning.",
                "resolved": False,
                "resolution": (
                    "Random frames and association schemes can be well "
                    "conditioned despite extensive overlap; phases and traffic decide."
                ),
            },
            {
                "objection": "The local positive affine-plane holonomy theorem is falsified.",
                "resolved": False,
                "resolution": (
                    "Each scalar plane remains positive; the no-go concerns "
                    "simultaneous support organization across many planes."
                ),
            },
        ],
        literature_links=[
            {
                "title": "Covering Irrep(S_n) With Tensor Products and Powers",
                "url": "https://arxiv.org/abs/2004.05283",
                "role": (
                    "Context for typical broad Kronecker support; the pressure "
                    "proof itself uses exact Plancherel multiplicity moments."
                ),
                "directly_proves_support_pressure_no_go": False,
            }
        ],
        headline_metrics={
            "exact_rich_plane_count_control_count": len(plane_controls),
            "finite_plane_count_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "finite_pressure_capacity_failure_count": pressure_failures,
            "orthogonal_affine_plane_atomization_no_go_theorem_count": 1,
            "collision_free_pressure_transfer_theorem_count": 1,
            "tail_n": tail.n,
            "tail_exact_pressure_ratio_log2": tail.exact_pressure_ratio_log2,
            "tail_elementary_pressure_lower_bound_log2": (
                tail.elementary_pressure_ratio_lower_bound_log2
            ),
            "tail_residual_pressure_after_markov_slack_log2": (
                tail.residual_pressure_after_markov_slack_log2
            ),
            "overlapping_plane_traffic_theorem_count": 0,
            "natural_node_frame_edge_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_rich_affine_plane_count_proved": failures == 0,
            "annealed_plane_support_pressure_diverges": pressure_failures == 0,
            "universal_orthogonal_plane_atomization_falsified": True,
            "collision_free_orthogonal_plane_atomization_asymptotically_falsified": True,
            "local_scalar_affine_plane_holonomy_remains_positive": True,
            "overlapping_plane_matrix_traffic_controlled": False,
            "global_carrier_groupoid_proved": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Affine-plane channels are locally positive but must overlap "
                "extensively at threshold width; the unresolved object is "
                "their matrix-valued signed traffic, not disjoint clique atoms."
            ),
        },
        status="orthogonal-affine-plane-atomization-falsified-overlap-traffic-open",
        summary=(
            "Proved that affine-plane channel support demand exceeds incident "
            "pair-core capacity by a factorially divergent factor, forcing "
            "extensive overlap in the collision-free natural law."
        ),
        falsifiers_triggered=[
            (
                "The complete S6 and sampled S7 disjoint affine triangles do "
                "not extrapolate to threshold-scale orthogonal atoms."
            ),
            (
                "A global proof cannot allocate a separate coefficient "
                "subspace to every positive affine-plane triangle."
            ),
            (
                "The remaining mechanism must exploit structured overlap, "
                "matrix recoupling, association-scheme spectra, or traffic cancellation."
            ),
            (
                "Support-pressure failure is not itself evidence of a bad "
                "frame edge or against a quantum speedup."
            ),
        ],
    )


def write_affine_plane_support_pressure_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_affine_plane_support_pressure_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Disjoint affine triangles extrapolate to threshold-scale orthogonal atoms."
                ),
                reason_invalid=(
                    "Support pressure theorem proves affine-plane channel support demand exceeds pair-core capacity by a factorially divergent factor."
                ),
                lesson=(
                    "Orthogonal affine-plane atomization is asymptotically impossible; future mechanisms must use structured overlap, matrix recoupling, or traffic cancellation."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_affine_plane_support_pressure_no_go": str(
                        path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_affine_plane_support_pressure_no_go_report()
    print(json.dumps(report, indent=2, sort_keys=True))
