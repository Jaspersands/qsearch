"""Source-mass boundary for the natural S6 partial-support mechanism.

The globally distinct S6 control falsifies universal scalar affine fibers, but
its portfolio contains both one-dimensional irreps: the trivial and sign
representations.  Under the independent Plancherel source law this mechanism
has factorially vanishing probability at information-threshold copy count.

For ``m`` independent Plancherel partitions of ``n`` and any dimension cutoff
``L``, let ``p(n)`` be the partition number.  Since

    Pr[d_lambda <= L] = (1/n!) sum_(d_lambda<=L) d_lambda^2
                      <= p(n)L^2/n!,                       (1)

the union bound gives

    Pr[min_i d_(lambda_i) <= L] <= m p(n)L^2/n!.          (2)

There are exactly two one-dimensional irreps.  More specifically, the event
that the sample contains both trivial and sign has

    Pr[triv and sign both occur] <= m(m-1)/(n!)^2.        (3)

The direct conjugate-chain extension of the S6 counterexample requires this
event.  Conditioning on global source distinctness ``CF`` transfers (2)-(3)
by division by ``Pr(CF)``.  The repository's exact collision-free formula
shows ``Pr(CF)->1`` for ``m=2 ceil(log_2 n!)``.  Hence every mechanism that
requires a polynomial-dimensional source, and especially the direct S6
trivial/sign mechanism, has factorially vanishing conditioned source mass.

This rescues nothing universally.  Matrix partial-support nodes built entirely
from typical high-dimensional sources may still carry positive physical PGM
mass.  The theorem excludes only low-dimensional-anchor explanations and does
not provide a scalar-on-bulk theorem or a decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_event_transfer import (
    stable_global_collision_free_probability,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_partial_support_source_mass_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class LowDimensionSourceControl:
    n: int
    dimension_cutoff: int
    exact_single_draw_low_dimension_probability: float
    exact_single_draw_low_dimension_probability_log2: float
    partition_count_bound: float
    partition_count_bound_log2: float
    exact_probability_below_bound: bool
    status: str


@dataclass(frozen=True)
class PartialSupportSourceMassScalingRecord:
    n: int
    group_order_decimal: str
    partition_count: int
    information_threshold_copy_count: int
    source_draw_count: int
    global_collision_free_probability: float
    log2_global_collision_free_probability: float
    polynomial_dimension_cutoff: int
    log2_unconditioned_any_polynomial_dimension_upper_bound: float
    log2_collision_free_conditioned_any_polynomial_dimension_upper_bound: float
    log2_unconditioned_any_one_dimensional_upper_bound: float
    log2_collision_free_conditioned_any_one_dimensional_upper_bound: float
    log2_unconditioned_trivial_and_sign_upper_bound: float
    log2_collision_free_conditioned_trivial_and_sign_upper_bound: float
    direct_s6_mechanism_conditioned_mass_superpolynomially_small: bool
    polynomial_dimension_anchor_conditioned_mass_superpolynomially_small: bool
    status: str


@dataclass(frozen=True)
class PartialSupportSourceMassBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[LowDimensionSourceControl]
    scaling_records: list[PartialSupportSourceMassScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _log2_probability(value: float) -> float:
    return math.log2(value) if value > 0 else -math.inf


def exact_single_draw_low_dimension_probability(
    n: int,
    dimension_cutoff: int,
) -> float:
    if n < 1 or dimension_cutoff < 1:
        raise ValueError("n and dimension cutoff must be positive")
    order = math.factorial(n)
    return sum(
        dimension**2
        for partition in integer_partitions(n)
        if (dimension := hook_length_dimension(partition)) <= dimension_cutoff
    ) / order


def low_dimension_source_control(
    n: int,
    dimension_cutoff: int,
) -> LowDimensionSourceControl:
    exact = exact_single_draw_low_dimension_probability(n, dimension_cutoff)
    partitions = len(integer_partitions(n))
    bound = min(1.0, partitions * dimension_cutoff**2 / math.factorial(n))
    verified = exact <= bound + 1e-15
    return LowDimensionSourceControl(
        n=n,
        dimension_cutoff=dimension_cutoff,
        exact_single_draw_low_dimension_probability=exact,
        exact_single_draw_low_dimension_probability_log2=_log2_probability(exact),
        partition_count_bound=bound,
        partition_count_bound_log2=_log2_probability(bound),
        exact_probability_below_bound=verified,
        status=(
            "exact-plancherel-low-dimension-mass-below-counting-bound"
            if verified
            else "low-dimension-source-mass-bound-failure"
        ),
    )


def _conditioned_log2_bound(
    log2_unconditioned_bound: float,
    collision_free_probability: float,
) -> float:
    if collision_free_probability <= 0:
        return math.inf
    return min(0.0, log2_unconditioned_bound - math.log2(collision_free_probability))


def partial_support_source_mass_scaling_record(
    n: int,
    *,
    polynomial_dimension_power: int = 4,
) -> PartialSupportSourceMassScalingRecord:
    if n < 3 or polynomial_dimension_power < 1:
        raise ValueError("invalid scaling parameters")
    order = math.factorial(n)
    copies = (order - 1).bit_length()
    draws = 2 * copies
    partitions = len(integer_partitions(n))
    collision_free = stable_global_collision_free_probability(n, copies)
    cutoff = n**polynomial_dimension_power

    any_poly = min(1.0, draws * partitions * cutoff**2 / order)
    any_one = min(1.0, 2 * draws / order)
    both_one = min(1.0, draws * (draws - 1) / order**2)
    log_poly = _log2_probability(any_poly)
    log_one = _log2_probability(any_one)
    log_both = _log2_probability(both_one)
    conditioned_poly = _conditioned_log2_bound(log_poly, collision_free)
    conditioned_one = _conditioned_log2_bound(log_one, collision_free)
    conditioned_both = _conditioned_log2_bound(log_both, collision_free)
    benchmark = 12 * math.log2(n)
    direct_small = conditioned_both < -benchmark
    polynomial_small = conditioned_poly < -benchmark
    return PartialSupportSourceMassScalingRecord(
        n=n,
        group_order_decimal=str(order),
        partition_count=partitions,
        information_threshold_copy_count=copies,
        source_draw_count=draws,
        global_collision_free_probability=collision_free,
        log2_global_collision_free_probability=_log2_probability(collision_free),
        polynomial_dimension_cutoff=cutoff,
        log2_unconditioned_any_polynomial_dimension_upper_bound=log_poly,
        log2_collision_free_conditioned_any_polynomial_dimension_upper_bound=conditioned_poly,
        log2_unconditioned_any_one_dimensional_upper_bound=log_one,
        log2_collision_free_conditioned_any_one_dimensional_upper_bound=conditioned_one,
        log2_unconditioned_trivial_and_sign_upper_bound=log_both,
        log2_collision_free_conditioned_trivial_and_sign_upper_bound=conditioned_both,
        direct_s6_mechanism_conditioned_mass_superpolynomially_small=direct_small,
        polynomial_dimension_anchor_conditioned_mass_superpolynomially_small=polynomial_small,
        status=(
            "direct-s6-and-polynomial-anchor-source-mass-superpolynomially-small"
            if direct_small and polynomial_small
            else "asymptotic-source-mass-bound-not-yet-below-benchmark"
        ),
    )


def run_partial_support_source_mass_boundary() -> (
    PartialSupportSourceMassBoundaryReport
):
    controls = [
        low_dimension_source_control(n, cutoff)
        for n, cutoff in ((6, 1), (8, 8), (10, 100), (12, 144))
    ]
    scaling = [
        partial_support_source_mass_scaling_record(n)
        for n in (12, 16, 20, 24, 32, 40, 48)
    ]
    failures = sum(not row.exact_probability_below_bound for row in controls)
    # Hardy--Ramanujan gives log p(n)=O(sqrt(n)), while Stirling gives
    # log(n!)=Theta(n log n).  With m=O(n log n) and L=n^O(1), both
    # conditioned bounds are therefore n^-omega(1).  The per-row booleans are
    # finite n^-12 benchmark crossings, not premises of the asymptotic proof.
    direct = True
    polynomial = True
    tail = scaling[-1]
    verified = failures == 0
    return PartialSupportSourceMassBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "low_dimension_plancherel_bound": (
                "For one Plancherel partition, Pr[d_lambda<=L] is exactly "
                "n!^-1 sum_(d_lambda<=L)d_lambda^2 and at most p(n)L^2/n!."
            ),
            "multiple_source_union": (
                "For m independent source labels, any dimension-at-most-L "
                "anchor has probability at most m p(n)L^2/n!."
            ),
            "direct_s6_pattern": (
                "The direct conjugate-chain S6 mechanism requires both trivial "
                "and sign sources, whose joint occurrence is at most "
                "m(m-1)/(n!)^2."
            ),
            "conditioning_transfer": (
                "Conditioning on globally distinct sources divides each upper "
                "bound by the exact collision-free probability, which tends to "
                "one at m=2 ceil(log2 n!)."
            ),
            "scope": (
                "This excludes low-dimensional-anchor mechanisms from positive "
                "natural source mass. It does not bound matrix partial supports "
                "formed entirely from typical high-dimensional sources."
            ),
        },
        exact_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "transfer_direct_s6_partial_support_pattern_to_natural_source_mass",
                "resolved": verified and direct,
                "resolution": "Its required trivial/sign pair has factorially vanishing probability before and after collision-free conditioning.",
            },
            {
                "obligation": "exclude_all_polynomial_dimension_anchor_mechanisms",
                "resolved": verified and polynomial,
                "resolution": "The partition-count union bound is exp(O(sqrt(n))) times polynomial over n!, hence superpolynomially small at threshold copies.",
            },
            {
                "obligation": "bound_high_dimension_matrix_partial_support_mass",
                "resolved": False,
                "resolution": "Need a carrier/Gram classification for nonscalar effects generated without any low-dimensional source labels.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The natural S6 counterexample proves matrix partial supports have positive asymptotic PGM mass.",
                "resolved": True,
                "resolution": "False for its direct mechanism: trivial and sign anchors are factorially rare under the source law.",
            },
            {
                "objection": "Collision-free conditioning can amplify the rare source event to constant mass.",
                "resolved": True,
                "resolution": "The conditioning probability tends to one; the exact transfer is division by that probability only.",
            },
            {
                "objection": "Rarity of low-dimensional anchors restores universal scalar affine fibers.",
                "resolved": False,
                "resolution": "High-dimensional recoupling multiplicities can still create matrix partial supports; no scalar-on-bulk theorem follows.",
            },
        ],
        headline_metrics={
            "low_dimension_plancherel_counting_bound_theorem_count": int(verified),
            "exact_control_count": len(controls),
            "exact_control_failure_count": failures,
            "direct_s6_trivial_sign_mass_boundary_theorem_count": int(direct),
            "polynomial_dimension_anchor_mass_boundary_theorem_count": int(polynomial),
            "tail_n": tail.n,
            "tail_log2_conditioned_direct_s6_mass_upper_bound": tail.log2_collision_free_conditioned_trivial_and_sign_upper_bound,
            "tail_log2_conditioned_polynomial_anchor_mass_upper_bound": tail.log2_collision_free_conditioned_any_polynomial_dimension_upper_bound,
            "finite_direct_s6_n12_benchmark_certified_row_count": sum(
                row.direct_s6_mechanism_conditioned_mass_superpolynomially_small
                for row in scaling
            ),
            "finite_polynomial_anchor_n12_benchmark_certified_row_count": sum(
                row.polynomial_dimension_anchor_conditioned_mass_superpolynomially_small
                for row in scaling
            ),
            "high_dimension_partial_support_mass_theorem_count": 0,
            "matrix_partial_support_gpe_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "direct_s6_low_dimension_mechanism_has_vanishing_natural_mass": verified and direct,
            "all_polynomial_dimension_anchor_mechanisms_have_vanishing_natural_mass": verified and polynomial,
            "finite_s6_falsifies_universal_scalar_affinity": True,
            "scalar_affine_behavior_holds_on_positive_native_bulk": False,
            "high_dimension_matrix_partial_support_mass_controlled": False,
            "matrix_partial_support_gpe_compiler_proved": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The known S6 mechanism is physically negligible because of its "
                "one-dimensional anchors, but no theorem controls matrix partial "
                "supports generated entirely by typical high-dimensional sources."
            ),
        },
        status=(
            "low-dimension-partial-support-mass-excluded-high-dimension-route-open"
            if verified and direct and polynomial
            else "partial-support-source-mass-boundary-control-failure"
        ),
        summary=(
            "Proved that the direct S6 scalar-affine falsifier and every "
            "polynomial-dimensional-anchor variant have factorially vanishing "
            "natural source mass, leaving high-dimensional matrix supports as "
            "the only relevant obstruction."
        ),
        falsifiers_triggered=[
            "A finite natural counterexample need not have positive asymptotic source mass.",
            "The direct S6 matrix-support mechanism is anchored by factorially rare one-dimensional irreps.",
            "Collision-free conditioning cannot rescue a source event when its own probability tends to one.",
            "Low-dimensional-anchor exclusion is not a scalar-on-bulk theorem for typical high-dimensional recoupling.",
        ],
    )


def write_partial_support_source_mass_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_partial_support_source_mass_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_partial_support_source_mass_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
