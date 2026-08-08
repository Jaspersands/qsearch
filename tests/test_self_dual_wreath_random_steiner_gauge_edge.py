import math

import numpy as np

from self_dual_wreath_random_steiner_gauge_edge import (
    audit_balanced_line_moments,
    audit_random_signed_gram,
    point_degrees,
    random_steiner_gauge_scaling_record,
    run_random_steiner_gauge_edge,
)


def test_balanced_line_gauge_has_exact_centered_second_moment() -> None:
    record = audit_balanced_line_moments()
    assert record.mean_residual == 0
    assert record.second_moment_residual == 0
    assert math.isclose(record.maximum_operator_norm, 2.0, abs_tol=1e-12)
    assert record.exact_balanced_line_moments_verified


def test_full_and_rich_degree_scales_match_the_theorem() -> None:
    for copy_count in range(4, 11):
        orientation_count = 1 << copy_count
        full = point_degrees(copy_count, "all")
        assert np.all(full == (orientation_count - 2) // 2)

        rich = point_degrees(copy_count, "pattern-rich")
        active = rich[rich > 0]
        assert int(active.min()) == 2 ** (copy_count - 2) - 2
        assert int(active.max()) <= 2 ** (copy_count - 1)
        assert int(np.sum(rich == 0)) == 2 * copy_count + 1


def test_matrix_bernstein_bound_becomes_nonvacuous_and_relative_error_vanishes() -> None:
    full = [
        random_steiner_gauge_scaling_record(copy_count, "all")
        for copy_count in (8, 12, 16, 20)
    ]
    rich = [
        random_steiner_gauge_scaling_record(copy_count, "pattern-rich")
        for copy_count in (10, 12, 16, 20)
    ]
    assert all(row.bound_nonvacuous for row in full)
    assert all(row.bound_nonvacuous for row in rich)
    assert all(
        later.asymptotic_relative_radius < earlier.asymptotic_relative_radius
        for earlier, later in zip(full, full[1:])
    )
    assert all(
        later.asymptotic_relative_radius < earlier.asymptotic_relative_radius
        for earlier, later in zip(rich, rich[1:])
    )


def test_seeded_random_controls_are_nonsingular_and_inside_proved_interval() -> None:
    for family, copy_count, seed in (
        ("all", 4, 104),
        ("all", 6, 106),
        ("all", 8, 108),
        ("pattern-rich", 5, 205),
        ("pattern-rich", 7, 207),
        ("pattern-rich", 8, 208),
    ):
        record = audit_random_signed_gram(copy_count, family, seed)
        assert record.observed_minimum_eigenvalue > 0
        assert record.exact_nullity == 0
        assert record.observed_inside_bernstein_interval


def test_report_keeps_natural_mixing_and_matrix_weights_open() -> None:
    report = run_random_steiner_gauge_edge()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["balanced_line_moments_exact"]
    assert report.claim_gate["independent_scalar_gauge_edge_proved"]
    assert report.claim_gate["gauge_entropy_intrinsic_obstruction_falsified"]
    assert not report.claim_gate["natural_line_gauges_independent"]
    assert not report.claim_gate["natural_cycle_mixing_bound_proved"]
    assert not report.claim_gate["weighted_matrix_traffic_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
