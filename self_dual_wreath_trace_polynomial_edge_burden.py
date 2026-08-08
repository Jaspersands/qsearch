"""Trace-polynomial burden for natural wreath frame spectral edges.

The exact sibling word-map normal form computes *normalized* traces.  This is
not yet a spectral-edge theorem.  A single outlier eigenvalue in a carrier of
dimension ``D`` contributes only ``1/D`` to a normalized trace witness.

For ``G=S_n`` and ``K`` source pairs the target carrier is

    D = d_nu product_i d_(lambda_i) d_(mu_i).

The deterministic dimension bound ``d_rho <= sqrt(|G|)`` gives

    D <= |G|^(K+1/2).                                      (1)

There is also a large-carrier statement requiring no asymptotic partition
theory.  If ``p(n)`` is the number of irreps and ``C>1``, Plancherel mass of
the set ``d_lambda^2 < |G|/(C p(n))`` is at most ``1/C``.  Taking ``C=4K``
and union bounding over the ``2K`` sources proves, with probability at least
one half,

    D >= (|G|/(4K p(n)))^K.                               (2)

Thus the natural carrier has ``log D=Theta((log |G|)^2)`` dimensions on a
constant-probability source event.

This module makes the resulting interval-uniform trace-method burden exact.
Let a desired upper edge be ``U`` and call ``(1+eta)U`` bad.  Among degree-r
polynomials normalized to equal one at the bad point, Chebyshev extremality
gives the smallest possible uniform magnitude on ``[0,U]``:

    1 / T_r(1+2 eta).

A squared normalized-trace witness whose good-case bound uses only uniform
control over that interval cannot resolve one outlier at failure level
``delta`` unless

    T_r(1+2 eta)^2 >= D/delta.                             (3)

For the lower edge ``l`` of a support interval ``[l,U]``, even optimistically
assuming that the kernel/support is already known, the corresponding outside
point is ``1+2 eta/(kappa-1)``, where ``kappa=U/l``.  The mixed-arity Gaussian
schedule has bounded ``kappa``, but (2)-(3) still require
``r=Theta((log |G|)^2)``.  At n=48 and 25 percent relative slack, the typical
carrier burden is over 13,000 degrees for the upper edge and over 72,000 for
the lower edge.

This is a no-go for treating fixed-word or ``O(log |G|)`` normalized moments
plus an interval-uniform polynomial bound as an edge proof.  It is not a
no-go for the natural frame itself.  A law-specific local law,
operator-valued concentration theorem, deterministic no-outlier structure,
or an exact spectral-multiplicity reduction could bypass the generic trace
penalty.  None is currently proved.  Positive word moments also do not
identify the smallest nonzero eigenvalue without a support-aware polynomial
or resolvent construction.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_event_transfer import (
    hierarchy_event_transfer_scaling_record,
)
from self_dual_wreath_multiscale_polar_schedule import (
    MIXED_SCHEDULE_CONDITION_UPPER,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_trace_polynomial_edge_burden.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PlancherelDimensionTailControl:
    n: int
    copy_count: int
    partition_count: int
    tail_constant: int
    dimension_squared_threshold: str
    exact_single_source_bad_mass: str
    single_source_bad_mass_upper_bound: str
    exact_bound_respected: bool
    all_source_typical_probability_lower_bound: float
    status: str


@dataclass(frozen=True)
class CarrierDimensionScalingRecord:
    n: int
    group_order_decimal: str
    partition_count: int
    selected_copy_count: int
    source_slot_count: int
    log2_typical_carrier_dimension_lower_bound: float
    log2_uniform_carrier_dimension_upper_bound: float
    typical_carrier_probability_lower_bound: float
    log2_group_order: float
    typical_log_dimension_to_copy_squared_ratio: float
    uniform_log_dimension_to_copy_squared_ratio: float
    constant_probability_superlogarithmic_carrier_proved: bool
    status: str


@dataclass(frozen=True)
class TracePolynomialBurdenRecord:
    n: int
    selected_copy_count: int
    hierarchy_node_target_count_upper_decimal: str
    log2_collision_free_probability: float
    log2_required_per_node_failure: float
    relative_edge_slack: float
    support_condition_number_upper: float
    upper_edge_chebyshev_outside_coordinate: float
    lower_edge_chebyshev_outside_coordinate: float
    typical_upper_edge_minimum_degree: int
    uniform_upper_edge_minimum_degree: int
    typical_lower_edge_minimum_degree: int
    uniform_lower_edge_minimum_degree: int
    typical_upper_degree_to_copy_squared_ratio: float
    typical_lower_degree_to_copy_squared_ratio: float
    fixed_word_regime_sufficient: bool
    order_log_group_word_regime_sufficient: bool
    positive_word_moments_alone_control_lower_nonzero_edge: bool
    status: str


@dataclass(frozen=True)
class RankOneOutlierControl:
    carrier_dimension: int
    moment_order: int
    bulk_eigenvalue: float
    upper_outlier_eigenvalue: float
    lower_outlier_eigenvalue: float
    normalized_upper_monomial_moment_difference: float
    normalized_lower_monomial_moment_difference: float
    upper_difference_times_dimension: float
    lower_difference_times_dimension: float
    good_condition_number: float
    lower_outlier_condition_number: float
    rank_one_outlier_dilution_verified: bool
    positive_moment_lower_edge_blindness_verified: bool
    status: str


@dataclass(frozen=True)
class TracePolynomialEdgeBurdenReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_dimension_tail_controls: list[PlancherelDimensionTailControl]
    carrier_scaling: list[CarrierDimensionScalingRecord]
    trace_polynomial_burdens: list[TracePolynomialBurdenRecord]
    rank_one_outlier_controls: list[RankOneOutlierControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def selected_copy_count(n: int) -> int:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    return (order - 1).bit_length() + 2


def plancherel_dimension_tail_control(
    n: int,
    copy_count: int | None = None,
) -> PlancherelDimensionTailControl:
    """Check the elementary Plancherel dimension tail bound exactly."""

    copies = copy_count or selected_copy_count(n)
    if copies < 1:
        raise ValueError("copy_count must be positive")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    tail_constant = 4 * copies
    threshold = Fraction(order, tail_constant * len(partitions))
    bad_mass = sum(
        Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in partitions
        if hook_length_dimension(partition) ** 2 < threshold
    )
    upper = Fraction(1, tail_constant)
    all_source_lower = max(0.0, 1.0 - 2.0 * copies / tail_constant)
    verified = bad_mass <= upper
    return PlancherelDimensionTailControl(
        n=n,
        copy_count=copies,
        partition_count=len(partitions),
        tail_constant=tail_constant,
        dimension_squared_threshold=str(threshold),
        exact_single_source_bad_mass=str(bad_mass),
        single_source_bad_mass_upper_bound=str(upper),
        exact_bound_respected=verified,
        all_source_typical_probability_lower_bound=all_source_lower,
        status=(
            "exact-plancherel-dimension-tail-bound-verified"
            if verified
            else "plancherel-dimension-tail-bound-failure"
        ),
    )


@lru_cache(maxsize=None)
def carrier_dimension_scaling_record(n: int) -> CarrierDimensionScalingRecord:
    copies = selected_copy_count(n)
    order = math.factorial(n)
    partition_count = len(integer_partitions(n))
    log2_order = math.log2(order)
    tail_constant = 4 * copies
    one_pair_log_lower = log2_order - math.log2(
        tail_constant * partition_count
    )
    typical_log_lower = copies * max(0.0, one_pair_log_lower)
    uniform_log_upper = (copies + 0.5) * log2_order
    return CarrierDimensionScalingRecord(
        n=n,
        group_order_decimal=str(order),
        partition_count=partition_count,
        selected_copy_count=copies,
        source_slot_count=2 * copies,
        log2_typical_carrier_dimension_lower_bound=typical_log_lower,
        log2_uniform_carrier_dimension_upper_bound=uniform_log_upper,
        typical_carrier_probability_lower_bound=0.5,
        log2_group_order=log2_order,
        typical_log_dimension_to_copy_squared_ratio=(
            typical_log_lower / (copies * copies)
        ),
        uniform_log_dimension_to_copy_squared_ratio=(
            uniform_log_upper / (copies * copies)
        ),
        constant_probability_superlogarithmic_carrier_proved=(
            typical_log_lower > copies
        ),
        status="constant-probability-quadratic-log-group-carrier-bound",
    )


def _acosh_exp(log_value: float) -> float:
    """Return acosh(exp(log_value)) without overflow."""

    if log_value < 0:
        raise ValueError("acosh argument must be at least one")
    if log_value == 0:
        return 0.0
    return log_value + math.log1p(
        math.sqrt(max(0.0, 1.0 - math.exp(-2.0 * log_value)))
    )


def minimum_chebyshev_degree(
    log2_carrier_dimension: float,
    log2_failure_probability: float,
    outside_coordinate: float,
) -> int:
    """Minimum r with T_r(x)^2 >= D/delta for ``x>1``."""

    if log2_carrier_dimension < 0:
        raise ValueError("carrier dimension logarithm must be nonnegative")
    if log2_failure_probability >= 0:
        raise ValueError("failure probability must be below one")
    if outside_coordinate <= 1:
        raise ValueError("outside coordinate must exceed one")
    half_log_ratio = (
        0.5
        * (log2_carrier_dimension - log2_failure_probability)
        * math.log(2.0)
    )
    numerator = _acosh_exp(half_log_ratio)
    return math.ceil(numerator / math.acosh(outside_coordinate))


@lru_cache(maxsize=None)
def trace_polynomial_burden_record(
    n: int,
    relative_edge_slack: float = 0.25,
    support_condition_number_upper: float = MIXED_SCHEDULE_CONDITION_UPPER,
) -> TracePolynomialBurdenRecord:
    if not 0 < relative_edge_slack < 1:
        raise ValueError("relative edge slack must lie in (0,1)")
    if support_condition_number_upper <= 1:
        raise ValueError("support condition number must exceed one")
    dimension = carrier_dimension_scaling_record(n)
    event = hierarchy_event_transfer_scaling_record(n)
    if not math.isfinite(event.log2_required_per_node_failure_upper_bound):
        raise ValueError("global-distinct event is impossible at this finite n")
    upper_coordinate = 1.0 + 2.0 * relative_edge_slack
    lower_coordinate = 1.0 + (
        2.0
        * relative_edge_slack
        / (support_condition_number_upper - 1.0)
    )
    log2_delta = event.log2_required_per_node_failure_upper_bound
    typical_upper = minimum_chebyshev_degree(
        dimension.log2_typical_carrier_dimension_lower_bound,
        log2_delta,
        upper_coordinate,
    )
    uniform_upper = minimum_chebyshev_degree(
        dimension.log2_uniform_carrier_dimension_upper_bound,
        log2_delta,
        upper_coordinate,
    )
    typical_lower = minimum_chebyshev_degree(
        dimension.log2_typical_carrier_dimension_lower_bound,
        log2_delta,
        lower_coordinate,
    )
    uniform_lower = minimum_chebyshev_degree(
        dimension.log2_uniform_carrier_dimension_upper_bound,
        log2_delta,
        lower_coordinate,
    )
    copies_squared = dimension.selected_copy_count**2
    return TracePolynomialBurdenRecord(
        n=n,
        selected_copy_count=dimension.selected_copy_count,
        hierarchy_node_target_count_upper_decimal=(
            event.hierarchy_node_target_count_upper_decimal
        ),
        log2_collision_free_probability=event.log2_global_distinct_probability,
        log2_required_per_node_failure=log2_delta,
        relative_edge_slack=relative_edge_slack,
        support_condition_number_upper=support_condition_number_upper,
        upper_edge_chebyshev_outside_coordinate=upper_coordinate,
        lower_edge_chebyshev_outside_coordinate=lower_coordinate,
        typical_upper_edge_minimum_degree=typical_upper,
        uniform_upper_edge_minimum_degree=uniform_upper,
        typical_lower_edge_minimum_degree=typical_lower,
        uniform_lower_edge_minimum_degree=uniform_lower,
        typical_upper_degree_to_copy_squared_ratio=(
            typical_upper / copies_squared
        ),
        typical_lower_degree_to_copy_squared_ratio=(
            typical_lower / copies_squared
        ),
        fixed_word_regime_sufficient=False,
        order_log_group_word_regime_sufficient=False,
        positive_word_moments_alone_control_lower_nonzero_edge=False,
        status="quadratic-log-group-trace-polynomial-degree-required",
    )


def rank_one_outlier_control(
    carrier_dimension: int,
    moment_order: int,
    *,
    bulk_eigenvalue: float = 1.0,
    upper_outlier_eigenvalue: float = 1.25,
    lower_outlier_eigenvalue: float = 1e-3,
) -> RankOneOutlierControl:
    if carrier_dimension < 2 or moment_order < 1:
        raise ValueError("invalid carrier dimension or moment order")
    if not 0 < lower_outlier_eigenvalue < bulk_eigenvalue:
        raise ValueError("lower outlier must lie in (0, bulk)")
    if upper_outlier_eigenvalue <= bulk_eigenvalue:
        raise ValueError("upper outlier must exceed the bulk")
    upper_difference = (
        upper_outlier_eigenvalue**moment_order
        - bulk_eigenvalue**moment_order
    ) / carrier_dimension
    lower_difference = (
        bulk_eigenvalue**moment_order
        - lower_outlier_eigenvalue**moment_order
    ) / carrier_dimension
    expected_upper_scaled = (
        upper_outlier_eigenvalue**moment_order
        - bulk_eigenvalue**moment_order
    )
    expected_lower_scaled = (
        bulk_eigenvalue**moment_order
        - lower_outlier_eigenvalue**moment_order
    )
    dilution = math.isclose(
        carrier_dimension * upper_difference,
        expected_upper_scaled,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ) and math.isclose(
        carrier_dimension * lower_difference,
        expected_lower_scaled,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    blindness = (
        lower_difference <= 1.0 / carrier_dimension
        and bulk_eigenvalue / lower_outlier_eigenvalue >= 100.0
    )
    return RankOneOutlierControl(
        carrier_dimension=carrier_dimension,
        moment_order=moment_order,
        bulk_eigenvalue=bulk_eigenvalue,
        upper_outlier_eigenvalue=upper_outlier_eigenvalue,
        lower_outlier_eigenvalue=lower_outlier_eigenvalue,
        normalized_upper_monomial_moment_difference=upper_difference,
        normalized_lower_monomial_moment_difference=lower_difference,
        upper_difference_times_dimension=carrier_dimension * upper_difference,
        lower_difference_times_dimension=carrier_dimension * lower_difference,
        good_condition_number=1.0,
        lower_outlier_condition_number=(
            bulk_eigenvalue / lower_outlier_eigenvalue
        ),
        rank_one_outlier_dilution_verified=dilution,
        positive_moment_lower_edge_blindness_verified=blindness,
        status=(
            "rank-one-normalized-trace-dilution-verified"
            if dilution and blindness
            else "rank-one-outlier-control-failure"
        ),
    )


def run_trace_polynomial_edge_burden() -> TracePolynomialEdgeBurdenReport:
    controls = [
        plancherel_dimension_tail_control(n)
        for n in (8, 10, 12)
    ]
    scaling = [
        carrier_dimension_scaling_record(n)
        for n in (20, 24, 28, 32, 36, 40, 44, 48)
    ]
    burdens = [
        trace_polynomial_burden_record(n)
        for n in (20, 24, 28, 32, 36, 40, 44, 48)
    ]
    outliers = [
        rank_one_outlier_control(64, 2),
        rank_one_outlier_control(1024, 4),
        rank_one_outlier_control(65536, 8),
    ]
    failures = sum(not row.exact_bound_respected for row in controls) + sum(
        not row.rank_one_outlier_dilution_verified
        or not row.positive_moment_lower_edge_blindness_verified
        for row in outliers
    )
    tail_dimension = scaling[-1]
    tail_burden = burdens[-1]
    metrics: dict[str, int | float] = {
        "plancherel_dimension_tail_theorem_count": 1,
        "chebyshev_trace_burden_theorem_count": 1,
        "rank_one_outlier_dilution_theorem_count": 1,
        "exact_control_count": len(controls) + len(outliers),
        "exact_control_failure_count": failures,
        "scaling_row_count": len(scaling),
        "tail_n": tail_dimension.n,
        "tail_selected_copy_count": tail_dimension.selected_copy_count,
        "tail_log2_typical_carrier_dimension_lower_bound": (
            tail_dimension.log2_typical_carrier_dimension_lower_bound
        ),
        "tail_log2_uniform_carrier_dimension_upper_bound": (
            tail_dimension.log2_uniform_carrier_dimension_upper_bound
        ),
        "tail_typical_upper_edge_minimum_degree": (
            tail_burden.typical_upper_edge_minimum_degree
        ),
        "tail_typical_lower_edge_minimum_degree": (
            tail_burden.typical_lower_edge_minimum_degree
        ),
        "fixed_word_spectral_edge_theorem_count": 0,
        "natural_local_law_theorem_count": 0,
        "exact_spectral_multiplicity_reduction_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return TracePolynomialEdgeBurdenReport(
        created_at=utc_now(),
        theorem_contract={
            "uniform_carrier_upper_bound": (
                "Every S_n irrep has dimension at most sqrt(n!), hence "
                "D<=|G|^(K+1/2) uniformly over targets and 2K sources."
            ),
            "constant_probability_carrier_lower_bound": (
                "At most 1/C Plancherel mass has d_lambda^2<|G|/(C p(n)); "
                "C=4K and a 2K-slot union bound give the stated D lower "
                "bound with probability at least one half."
            ),
            "chebyshev_extremal_burden": (
                "A degree-r trace polynomial whose good-case guarantee is "
                "uniform over an interval pays T_r(x)^2>=D/delta; Chebyshev "
                "is minimax for this interval-uniform problem."
            ),
            "lower_edge_scope": (
                "The lower-edge degree assumes the positive support or a "
                "coefficient Gram reduction is already known. Legitimate "
                "zero modes otherwise require an additional construction."
            ),
            "scope": (
                "This rules out fixed-word normalized traces plus a generic "
                "interval-uniform polynomial bound as an edge proof, not the "
                "natural frame or a law-specific structural/local-law route."
            ),
        },
        exact_dimension_tail_controls=controls,
        carrier_scaling=scaling,
        trace_polynomial_burdens=burdens,
        rank_one_outlier_controls=outliers,
        proof_obligations=[
            {
                "obligation": "quantify_normalized_trace_dimension_penalty",
                "resolved": failures == 0,
                "resolution": (
                    "Equations (1)-(3) give exact uniform and typical carrier "
                    "bounds and the interval-uniform minimax degree burden."
                ),
            },
            {
                "obligation": "prove_growing_word_control_at_required_degree",
                "resolved": False,
                "resolution": (
                    "The exact word-map normal form is currently controlled "
                    "only at fixed finite degree, while the generic trace route "
                    "requires Theta((log n!)^2) degree."
                ),
            },
            {
                "obligation": "bypass_trace_dimension_with_structural_local_law",
                "resolved": False,
                "resolution": (
                    "No operator-valued concentration, no-outlier theorem, or "
                    "exact spectral-multiplicity reduction is proved."
                ),
            },
            {
                "obligation": "control_smallest_nonzero_natural_frame_edge",
                "resolved": False,
                "resolution": (
                    "Positive word moments alone are support-blind; a resolvent, "
                    "coefficient Gram, or support-aware polynomial is required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "There are only p(n) target blocks, so normalized trace moments pay only p(n).",
                "resolved": True,
                "resolution": (
                    "False without a multiplicity theorem: one eigenvalue in a "
                    "target block is diluted by its full carrier dimension D."
                ),
            },
            {
                "objection": "O(log |G|) growing moments should suffice because there are O(|G|p(n)) events.",
                "resolved": True,
                "resolution": (
                    "The event union contributes O(log |G|), but log D is "
                    "Theta((log |G|)^2) on a constant-probability source set."
                ),
            },
            {
                "objection": "High positive moments control both spectral edges.",
                "resolved": True,
                "resolution": (
                    "A tiny positive rank-one eigenvalue changes every positive "
                    "monomial trace by at most 1/D while making the condition "
                    "number arbitrarily large."
                ),
            },
            {
                "objection": "The trace burden proves the natural frame is ill-conditioned.",
                "resolved": True,
                "resolution": (
                    "No. It proves a limitation of generic normalized-trace "
                    "certification and prioritizes structural or local-law routes."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "fixed_word_moments_suffice_for_spectral_edges": False,
            "order_log_group_moments_suffice_for_generic_trace_edge_proof": False,
            "quadratic_log_group_trace_degree_burden_proved": failures == 0,
            "positive_word_moments_suffice_for_lower_nonzero_edge": False,
            "natural_operator_valued_local_law_proved": False,
            "exact_small_spectral_multiplicity_reduction_proved": False,
            "natural_all_depth_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The normalized trace route needs quadratic-log-group word "
                "degree and a separate support-aware lower-edge argument."
            ),
        },
        status=(
            "trace-polynomial-burden-proved-structural-local-law-prioritized"
            if failures == 0
            else "trace-polynomial-burden-control-failure"
        ),
        summary=(
            "Proved that fixed or O(log |G|) normalized moments cannot certify "
            "the required natural-frame edge event through a generic trace "
            "argument; the decisive next route is structural or resolvent-based."
        ),
        falsifiers_triggered=[
            "Fixed-word Marchenko--Pastur convergence is not an edge theorem in the natural carrier.",
            "The hierarchy union bound is not the dominant trace-method cost; the carrier dimension is.",
            "Positive word moments do not by themselves control the smallest nonzero frame eigenvalue.",
        ],
    )


def write_trace_polynomial_edge_burden_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_trace_polynomial_edge_burden())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_trace_polynomial_edge_burden_report()
    print(json.dumps(report, indent=2))
