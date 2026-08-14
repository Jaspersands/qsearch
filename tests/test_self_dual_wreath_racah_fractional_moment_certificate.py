import math

from self_dual_wreath_racah_fractional_moment_certificate import (
    audit_physical_average_fractional_moment,
    averaged_fractional_renyi_upper_bits,
    fractional_moment_bad_mass_upper,
    identity_coupling_fractional_countermodel,
    run_racah_fractional_moment_certificate,
    synthetic_fractional_scaling_control,
)


def test_finite_physical_average_obeys_fractional_renyi_and_tail_bounds() -> None:
    for n, theta, threshold in (
        (3, 0.25, 2.0),
        (4, 0.5, 2.0),
        (5, 0.25, 4.0),
        (5, 1.0, 4.0),
    ):
        row = audit_physical_average_fractional_moment(n, theta, threshold)
        assert row.physical_average_fractional_moment >= 1 - 1e-10
        assert row.renyi_upper_violation_bits < 1e-9
        assert row.bad_mass_bound_violation < 1e-9
        assert row.exact_fractional_certificate_verified


def test_fractional_helpers_reject_fake_moments_and_apply_markov() -> None:
    assert math.isclose(averaged_fractional_renyi_upper_bits(2.0, 0.5), 2.0)
    assert math.isclose(fractional_moment_bad_mass_upper(2.0, 0.5, 16.0), 0.5)
    try:
        averaged_fractional_renyi_upper_bits(0.9, 0.5)
    except ValueError:
        pass
    else:
        raise AssertionError("a dependence moment below one must be rejected")


def test_perfect_marginals_do_not_control_fractional_dependence() -> None:
    row = identity_coupling_fractional_countermodel(20, 0.5)
    assert row.exact_fractional_dependence_moment > 1
    assert row.fractional_renyi_upper_bits >= row.plancherel_entropy_bits - 1e-10
    assert row.exact_collision_moment == row.partition_count
    assert row.perfect_marginals_imply_fractional_bound is False


def test_synthetic_vanishing_order_schedule_is_sublogarithmic() -> None:
    rows = [synthetic_fractional_scaling_control(n) for n in (20, 100, 10_000)]
    assert all(row.sufficient_rate_verified for row in rows)
    assert rows[-1].upper_over_log2_n < rows[0].upper_over_log2_n
    assert all(not row.natural_fractional_moment_bound_proved for row in rows)


def test_report_keeps_natural_and_speedup_gates_closed() -> None:
    report = run_racah_fractional_moment_certificate()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["physical_average_fractional_renyi_certificate_proved"] is True
    assert report.claim_gate["collision_subpolynomial_required"] is False
    assert report.claim_gate["natural_growing_row_fractional_moment_bound_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
