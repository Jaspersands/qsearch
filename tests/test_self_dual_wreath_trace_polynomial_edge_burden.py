import math

from self_dual_wreath_trace_polynomial_edge_burden import (
    carrier_dimension_scaling_record,
    minimum_chebyshev_degree,
    plancherel_dimension_tail_control,
    rank_one_outlier_control,
    run_trace_polynomial_edge_burden,
    trace_polynomial_burden_record,
)


def test_exact_plancherel_dimension_tail_bound() -> None:
    control = plancherel_dimension_tail_control(8)
    assert control.exact_bound_respected
    assert control.all_source_typical_probability_lower_bound == 0.5
    assert control.exact_single_source_bad_mass == "1/20160"


def test_natural_carrier_has_quadratic_log_group_dimension() -> None:
    record = carrier_dimension_scaling_record(48)
    assert record.selected_copy_count == 205
    assert record.log2_typical_carrier_dimension_lower_bound > 36_000
    assert record.log2_uniform_carrier_dimension_upper_bound > 41_000
    assert record.constant_probability_superlogarithmic_carrier_proved
    assert record.typical_log_dimension_to_copy_squared_ratio > 0.8


def test_chebyshev_degree_is_monotone_in_dimension_and_separation() -> None:
    easy = minimum_chebyshev_degree(100.0, -20.0, 2.0)
    larger_dimension = minimum_chebyshev_degree(200.0, -20.0, 2.0)
    closer_outlier = minimum_chebyshev_degree(100.0, -20.0, 1.1)
    assert larger_dimension > easy
    assert closer_outlier > easy


def test_trace_burden_excludes_fixed_and_log_group_word_regimes() -> None:
    record = trace_polynomial_burden_record(48)
    copies_squared = record.selected_copy_count**2
    assert record.typical_upper_edge_minimum_degree > 13_000
    assert record.typical_lower_edge_minimum_degree > 72_000
    assert record.typical_upper_edge_minimum_degree > record.selected_copy_count
    assert record.typical_lower_edge_minimum_degree > copies_squared
    assert not record.fixed_word_regime_sufficient
    assert not record.order_log_group_word_regime_sufficient
    assert not record.positive_word_moments_alone_control_lower_nonzero_edge


def test_rank_one_outliers_are_diluted_by_full_carrier_dimension() -> None:
    control = rank_one_outlier_control(65_536, 8)
    assert control.rank_one_outlier_dilution_verified
    assert control.positive_moment_lower_edge_blindness_verified
    assert control.lower_outlier_condition_number == 1000.0
    assert control.normalized_lower_monomial_moment_difference <= 1 / 65_536
    assert math.isclose(
        control.upper_difference_times_dimension,
        1.25**8 - 1.0,
    )


def test_report_blocks_edge_and_speedup_claims() -> None:
    report = run_trace_polynomial_edge_burden()
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.claim_gate["quadratic_log_group_trace_degree_burden_proved"]
    assert not report.claim_gate["natural_operator_valued_local_law_proved"]
    assert not report.claim_gate["natural_all_depth_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.status == (
        "trace-polynomial-burden-proved-structural-local-law-prioritized"
    )
