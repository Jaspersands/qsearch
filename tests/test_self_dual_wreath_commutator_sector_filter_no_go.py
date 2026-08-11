from fractions import Fraction
from functools import lru_cache

import pytest

from self_dual_wreath_commutator_sector_filter_no_go import (
    commutator_sector_filter_theorem,
    derangement_centralizer_control,
    derangement_centralizer_sum,
    nonidentity_reciprocal_upper_bound,
    optimal_central_filter_control,
    partition_number,
    reciprocal_class_sum_control,
    run_commutator_sector_filter_no_go,
    sector_filter_scaling_record,
    subset_partition_injection_exponent,
)


@lru_cache(maxsize=1)
def _report():
    return run_commutator_sector_filter_no_go()


def test_small_moved_support_centralizer_sums_are_exact():
    assert derangement_centralizer_sum(2) == 2
    assert derangement_centralizer_sum(3) == 3
    assert derangement_centralizer_sum(4) == 12
    assert derangement_centralizer_sum(5) == 11
    assert derangement_centralizer_sum(6) == 80


@pytest.mark.parametrize("moved", range(5, 23))
def test_exact_half_factorial_bound_covers_finite_prefix(moved):
    control = derangement_centralizer_control(moved)
    assert control.exact_centralizer_sum <= control.half_factorial_bound
    assert control.exact_finite_bound_verified
    assert control.certificate_source == "exact-partition-enumeration"


@pytest.mark.parametrize("moved", (23, 24, 30, 50, 100, 1000))
def test_analytic_partition_centralizer_bound_covers_infinite_tail(moved):
    control = derangement_centralizer_control(moved)
    assert control.exact_finite_bound_verified
    assert control.analytic_tail_bound_verified
    assert control.analytic_log_upper_bound <= (
        control.analytic_log_half_factorial_lower_bound
    )


@pytest.mark.parametrize("degree", range(5, 41))
def test_reciprocal_class_sum_has_uniform_seven_fourths_bound(degree):
    control = reciprocal_class_sum_control(degree)
    assert Fraction(control.exact_nonidentity_sum) <= Fraction(
        control.exact_derived_nonidentity_upper_bound
    )
    assert Fraction(control.exact_derived_nonidentity_upper_bound) <= Fraction(3, 4)
    assert control.three_fourths_nonidentity_bound_verified
    assert Fraction(control.exact_reciprocal_class_sum) <= Fraction(7, 4)
    assert Fraction(control.exact_plancherel_moment_average) <= Fraction(
        control.exact_plancherel_average_bound
    )
    assert control.seven_fourths_bound_verified
    assert control.plancherel_average_bound_verified


@pytest.mark.parametrize("degree", (5, 6, 7, 8, 12, 13, 100, 1000, 10_000))
def test_symbolic_all_n_nonidentity_bound_never_exceeds_three_fourths(degree):
    assert nonidentity_reciprocal_upper_bound(degree) <= Fraction(3, 4)


@pytest.mark.parametrize("degree", range(5, 15))
def test_subset_injection_proves_partition_number_lower_bound(degree):
    exponent = subset_partition_injection_exponent(degree)
    assert exponent * (exponent + 3) // 2 <= degree
    assert (exponent + 1) * (exponent + 4) // 2 > degree
    assert partition_number(degree) >= 1 << exponent


@pytest.mark.parametrize("degree", range(5, 13))
def test_exact_soft_filter_linear_program_obeys_moment_budget(degree):
    control = optimal_central_filter_control(degree, Fraction(1, degree))
    assert control.conditional_moment_at_optimum >= 1.0 / degree
    assert control.optimal_plancherel_success <= control.moment_budget_bound
    assert control.exact_linear_program_verified


def test_polynomially_many_weak_fourier_labels_remain_asymptotically_rare():
    moderate = sector_filter_scaling_record(
        100,
        source_domination_factor=2,
        source_label_count=100**2,
        inverse_polynomial_signal_degree=1,
    )
    large = sector_filter_scaling_record(
        2000,
        source_domination_factor=2,
        source_label_count=2000**2,
        inverse_polynomial_signal_degree=1,
    )
    assert large.partition_injection_bound_verified
    assert large.log2_filter_success_upper_bound < moderate.log2_filter_success_upper_bound
    assert large.filter_success_upper_bound_below_one
    assert large.log2_amplitude_amplification_cost_lower_bound > 20.0


def test_theorem_keeps_collective_noncentral_boundary_open():
    theorem = commutator_sector_filter_theorem()
    assert theorem.all_n_from_degree_five
    assert theorem.theorem_verified
    assert not theorem.generic_amplitude_amplification_escape
    assert not theorem.coherent_collective_escape_ruled_out


def test_report_closes_central_filter_without_claiming_global_no_go():
    report = _report()
    assert report.headline_metrics[
        "commutator_sector_filter_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["centralizer_control_failure_count"] == 0
    assert report.headline_metrics["reciprocal_class_control_failure_count"] == 0
    assert report.headline_metrics["optimal_filter_control_failure_count"] == 0
    assert not report.claim_gate["central_high_moment_postselection_viable"]
    assert not report.claim_gate["polynomial_label_catalog_viable"]
    assert not report.claim_gate["generic_amplitude_amplification_viable"]
    assert not report.claim_gate["new_collective_observable_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
