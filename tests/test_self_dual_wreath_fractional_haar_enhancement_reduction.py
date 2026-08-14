import math

from self_dual_wreath_fractional_haar_enhancement_reduction import (
    audit_fractional_haar_finite,
    fractional_collision_interpolation_upper,
    fractional_haar_scaling_record,
    good_set_information_upper_bits,
    run_fractional_haar_enhancement_reduction,
)


def test_fractional_collision_interpolation_is_tail_tolerant() -> None:
    assert math.isclose(fractional_collision_interpolation_upper(4.0, 0.5), 2.0)
    assert 4.0**0.25 < 4.0


def test_complete_natural_couplings_obey_fractional_interpolation() -> None:
    for n in (4, 5, 6):
        for theta in (0.25, 0.5, 1.0):
            row = audit_fractional_haar_finite(n, theta)
            assert row.collision_interpolation_violation < 1e-9
            assert row.fractional_excess_to_theta_haar_upper_ratio >= 0
            assert row.exact_fractional_interpolation_verified
            assert row.finite_natural_ratio_is_asymptotic_evidence is False


def test_good_set_jensen_cancels_fractional_order_at_linear_scale() -> None:
    theta = 0.1
    haar = 1e-8
    enhancement = 1e3
    excess = enhancement * theta * haar
    upper = good_set_information_upper_bits(0.9, excess, theta)
    assert upper <= enhancement * haar / math.log(2.0) + 1e-14


def test_subfactorial_synthetic_enhancement_is_overwhelmed_by_haar_gap() -> None:
    early = fractional_haar_scaling_record(50)
    late = fractional_haar_scaling_record(10_000)
    assert early.synthetic_enhancement_is_subfactorial
    assert late.synthetic_enhancement_is_subfactorial
    assert late.synthetic_total_information_upper_bits < early.synthetic_total_information_upper_bits
    assert late.natural_enhancement_bound_proved is False


def test_report_keeps_natural_enhancement_and_speedup_gates_closed() -> None:
    report = run_fractional_haar_enhancement_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["fractional_haar_excess_bound_proved"] is True
    assert report.claim_gate["collision_enhancement_bound_required"] is False
    assert report.claim_gate["natural_fractional_enhancement_subfactorial_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
