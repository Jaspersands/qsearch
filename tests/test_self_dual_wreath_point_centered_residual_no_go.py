import math

from self_dual_wreath_point_centered_residual_no_go import (
    audit_mean_zero_character_control,
    build_point_centered_residual_report,
    mean_simplex_normalized_energy,
    mean_simplex_trace_excess,
    point_residual_bound,
    point_residual_scaling_record,
)


def test_plancherel_mean_z0_channel_and_operator_projection_are_exact():
    controls = [
        audit_mean_zero_character_control(3, 1),
        audit_mean_zero_character_control(3, 2),
    ]
    assert all(row.exact_mean_zero_character_simplex_verified for row in controls)
    assert max(row.maximum_mean_channel_formula_residual for row in controls) < 1e-9
    assert max(row.maximum_operator_mean_projection_residual for row in controls) < 1e-9


def test_mean_simplex_energy_and_trace_excess_have_expected_scaling():
    n = 8
    log_order = math.lgamma(n + 1) / math.log(2)
    copies = math.ceil(2 * log_order)
    energy = mean_simplex_normalized_energy(n, copies)
    excess = mean_simplex_trace_excess(n, copies)
    assert energy >= n - 1
    assert energy < 2 * (n - 1)
    assert excess < 1 / math.factorial(n)


def test_critical_residual_bound_closes_arbitrary_point_povms():
    records = [
        point_residual_scaling_record(n, "critical-two-log-factorial")
        for n in (24, 32, 64, 128)
    ]
    assert all(row.public_label_adaptive_measurements_covered for row in records)
    assert all(row.globally_distinct_conditioning_transfer_available for row in records)
    assert all(row.arbitrary_point_povm_excess_superpolynomially_small for row in records)
    assert all(
        right.arbitrary_point_povm_excess_log2_upper_bound
        < left.arbitrary_point_povm_excess_log2_upper_bound
        for left, right in zip(records, records[1:])
    )


def test_quartic_and_quintic_sample_schedules_remain_closed_asymptotically():
    quartic = point_residual_scaling_record(128, "quartic")
    quintic = point_residual_scaling_record(128, "quintic-sixteenth")
    assert quartic.arbitrary_point_povm_excess_superpolynomially_small
    assert quintic.arbitrary_point_povm_excess_superpolynomially_small
    assert not quartic.carrier_retaining_measurements_covered
    direct = point_residual_bound(128, quartic.copy_count)
    assert direct.residual_normalized_energy_log2_upper_bound < 0


def test_report_closes_point_route_without_overclaiming_global_carrier_no_go():
    report = build_point_centered_residual_report()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["public_label_adaptive_point_povm_no_go_proved"]
    assert report.claim_gate["all_fixed_log_factorial_copy_multipliers_closed"]
    assert not report.claim_gate["critical_copy_multiplier_two_point_route_viable"]
    assert not report.claim_gate["carrier_retaining_global_decoder_ruled_out"]
    assert not report.claim_gate["all_polynomial_sample_schedules_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
