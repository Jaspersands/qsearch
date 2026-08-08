from fractions import Fraction
import math

from self_dual_wreath_two_color_return_walk import (
    audit_return_identity,
    audit_return_walk_spectrum,
    audit_source_only_generated_subgroup,
    run_two_color_return_walk,
    source_only_generated_subgroup_order,
    source_only_incidence_rows,
    stationary_moment_obstruction_record,
    two_color_identity_count,
)


def test_two_color_count_handles_noncommuting_ordered_products() -> None:
    count = two_color_identity_count(
        ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0))
    )
    assert count == 4


def test_word_count_moment_equals_return_probability_exactly() -> None:
    controls = [
        audit_return_identity(2, 2, 4),
        audit_return_identity(3, 2, 3),
    ]
    assert all(row.exact_return_identity_verified for row in controls)
    assert all(
        Fraction(row.exact_word_count_moment)
        == Fraction(row.exact_walk_return_probability)
        for row in controls
    )


def test_source_only_subgroup_order_and_sign_rank() -> None:
    for copies in (1, 2):
        control = audit_source_only_generated_subgroup(3, copies)
        assert control.incidence_rank_over_f2 == copies + 1
        assert control.exact_generated_subgroup_formula_verified
        assert source_only_generated_subgroup_order(
            math.factorial(3), copies
        ) == control.exact_generated_subgroup_order
        assert len(source_only_incidence_rows(copies)) == 1 << copies


def test_global_spectrum_is_coarse_and_has_expected_stationary_mass() -> None:
    s2 = audit_return_walk_spectrum(2, 2)
    s3 = audit_return_walk_spectrum(3, 2)
    assert s2.exact_spectrum_control_verified
    assert s3.exact_spectrum_control_verified
    assert abs(s2.largest_nonstationary_eigenvalue - 0.5) < 1e-10
    assert abs(s3.largest_nonstationary_eigenvalue - 0.75) < 1e-10
    assert not s3.global_gap_is_natural_scale_edge


def test_stationary_outliers_dominate_regular_growing_moments_near_two_k() -> None:
    records = [stationary_moment_obstruction_record(n) for n in (12, 24, 48)]
    for record in records:
        assert record.log2_stationary_lower_bound_at_copy_degree < 0
        assert record.log2_stationary_lower_bound_at_four_times_copy_degree > 0
        assert 1.8 < record.critical_degree_to_copy_count_ratio < 2.1
        assert record.globally_distinct_stationary_support_is_empty
        assert not record.collision_free_central_return_bound_proved


def test_report_keeps_central_return_and_edge_gates_closed() -> None:
    report = run_two_color_return_walk()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["all_order_two_color_return_walk_identity_proved"]
    assert report.claim_gate["source_only_generated_subgroup_order_proved"]
    assert report.claim_gate[
        "unconditioned_regular_growing_moment_route_falsified"
    ]
    assert not report.claim_gate["collision_free_central_return_bound_proved"]
    assert not report.claim_gate["natural_complete_node_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
