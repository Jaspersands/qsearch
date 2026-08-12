from fractions import Fraction

import pytest

from self_dual_wreath_final_root_joint_aspect_sharpening import (
    ASYMPTOTIC_OPTIMAL_COMMON_CARRIER_ASPECT,
    ASYMPTOTIC_OPTIMAL_EVENT_MASS,
    ASYMPTOTIC_OPTIMAL_FIBER_COEFFICIENT_ASPECT,
    ASYMPTOTIC_OPTIMAL_MARKOV_FACTOR,
    FOURTH_MOMENT_OPTIMAL_COMMON_CARRIER_ASPECT,
    FOURTH_MOMENT_OPTIMAL_EVENT_MASS,
    FOURTH_MOMENT_OPTIMAL_FIBER_COEFFICIENT_ASPECT,
    FOURTH_MOMENT_OPTIMAL_MARKOV_FACTOR,
    OLD_DECOUPLED_FIBER_COEFFICIENT_ASPECT,
    SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT,
    audit_joint_aspect,
    asymptotic_optimized_fourth_moment_event,
    common_span_carrier_lower_bound,
    joint_aspect_corollary,
    joint_aspect_theorem,
    joint_fiber_coefficient_lower_bound,
    optimized_fourth_moment_event,
    run_final_root_joint_aspect_sharpening,
)


def test_exact_endpoint_values_and_factor_two_improvement() -> None:
    assert common_span_carrier_lower_bound(Fraction(2)) == Fraction(19, 128)
    assert joint_fiber_coefficient_lower_bound(Fraction(2)) == Fraction(19, 260)
    assert joint_fiber_coefficient_lower_bound(Fraction(4)) == Fraction(121, 1300)
    assert (
        SHARPENED_JOINT_FIBER_COEFFICIENT_ASPECT
        / OLD_DECOUPLED_FIBER_COEFFICIENT_ASPECT
        == 2
    )


def test_joint_bound_holds_across_dyadic_aspect_interval() -> None:
    rows = [
        audit_joint_aspect(Fraction(numerator, 64))
        for numerator in range(128, 257)
    ]
    assert all(row.joint_bound_verified for row in rows)
    minimum = min(
        Fraction(row.joint_fiber_to_coefficient_lower_bound) for row in rows
    )
    assert minimum == Fraction(19, 260)


def test_dyadic_aspect_outside_interval_is_rejected() -> None:
    with pytest.raises(ValueError, match=r"\[2,4\]"):
        joint_fiber_coefficient_lower_bound(Fraction(3, 2))
    with pytest.raises(ValueError, match=r"\[2,4\]"):
        common_span_carrier_lower_bound(Fraction(9, 2))


def test_theorem_keeps_extrema_coupled() -> None:
    theorem = joint_aspect_theorem()
    assert theorem.theorem_verified
    assert theorem.same_positive_mass_event
    assert theorem.dyadic_extrema_must_remain_coupled
    assert theorem.sharp_uniform_bound == "r/N>=19/260-o(1)"


def test_corollary_improves_block_ratio_but_not_M4_gate() -> None:
    row = joint_aspect_corollary()
    assert row.maximum_component_block_to_fiber_coefficient == "260/19"
    assert row.fiber_aspect_improvement_factor == "2"
    assert row.fourth_moment_floor_improvement_factor == "4"
    assert not row.natural_component_diagonal_tail_proved
    assert not row.natural_distinct_crossing_bound_proved


def test_vanishing_tolerance_reaches_clean_asymptotic_optimum() -> None:
    row = asymptotic_optimized_fourth_moment_event()
    assert row.theorem_verified
    assert row.conditioned_uniform_rank_failure_tends_to_zero
    assert row.optimal_markov_factor == str(ASYMPTOTIC_OPTIMAL_MARKOV_FACTOR)
    assert row.conditioned_event_mass_lower_bound == str(
        ASYMPTOTIC_OPTIMAL_EVENT_MASS
    )
    assert row.common_fiber_to_physical_carrier_lower_bound == str(
        ASYMPTOTIC_OPTIMAL_COMMON_CARRIER_ASPECT
    )
    assert row.common_fiber_to_coefficient_lower_bound == str(
        ASYMPTOTIC_OPTIMAL_FIBER_COEFFICIENT_ASPECT
    )
    assert row.maximum_component_block_to_fiber_coefficient == "8"
    assert row.critical_uniform_component_cap == "1/4"
    assert row.guaranteed_physical_noncrossing_floor == "1/4096"
    assert row.improvement_over_fixed_one_over_64_optimum > 1.6
    assert not row.natural_component_M4_positive
    assert not row.natural_component_M4_positive


def test_fourth_moment_event_has_exact_optimal_cutoff() -> None:
    row = optimized_fourth_moment_event()
    assert row.optimization_verified
    assert row.endpoint_a_two_is_uniform_worst_case
    assert row.unique_optimal_markov_factor == str(
        FOURTH_MOMENT_OPTIMAL_MARKOV_FACTOR
    )
    assert row.conditioned_event_mass_lower_bound == str(
        FOURTH_MOMENT_OPTIMAL_EVENT_MASS
    )
    assert row.common_fiber_to_physical_carrier_lower_bound == str(
        FOURTH_MOMENT_OPTIMAL_COMMON_CARRIER_ASPECT
    )
    assert row.common_fiber_to_coefficient_lower_bound == str(
        FOURTH_MOMENT_OPTIMAL_FIBER_COEFFICIENT_ASPECT
    )
    assert row.critical_uniform_component_cap > 0.226
    assert row.improvement_over_nine_eighths_schedule > 1.6
    assert not row.natural_component_diagonal_tail_proved
    assert not row.natural_distinct_crossing_bound_proved


def test_report_claims_only_the_dimension_sharpening() -> None:
    report = run_final_root_joint_aspect_sharpening()
    assert report.headline_metrics["joint_aspect_sharpening_theorem_count"] == 1
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.headline_metrics["fiber_aspect_improvement_factor"] == 2.0
    assert (
        report.headline_metrics[
            "rank_cauchy_fourth_moment_floor_improvement_factor"
        ]
        == 4.0
    )
    assert report.claim_gate[
        "natural_final_fiber_coefficient_aspect_at_least_19_over_260"
    ]
    assert report.claim_gate["fourth_moment_positive_mass_event_optimized"]
    assert report.claim_gate["vanishing_rank_tolerance_schedule_proved"]
    assert report.headline_metrics["vanishing_tolerance_control_failure_count"] == 0
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
