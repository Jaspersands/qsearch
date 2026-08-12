import math

import pytest

from self_dual_wreath_component_dependency_ridge_moment_method_bridge import (
    audit_vanishing_fraction_hard_edge,
    dependency_ridge_moment_method_bridge_theorem,
    fixed_moment_tail_scaling_record,
    marchenko_pastur_lower_edge,
    marchenko_pastur_moment,
    narayana_number,
    run_component_dependency_ridge_moment_method_bridge,
)


def test_narayana_formula_recovers_first_four_mp_moments() -> None:
    assert [narayana_number(4, blocks) for blocks in range(1, 5)] == [1, 6, 6, 1]
    alpha = 2.0
    assert marchenko_pastur_moment(1, alpha) == pytest.approx(2.0)
    assert marchenko_pastur_moment(2, alpha) == pytest.approx(6.0)
    assert marchenko_pastur_moment(3, alpha) == pytest.approx(22.0)
    assert marchenko_pastur_moment(4, alpha) == pytest.approx(90.0)


def test_final_root_mp_family_has_uniform_positive_lower_edge() -> None:
    edge = marchenko_pastur_lower_edge(2.0)
    assert edge == pytest.approx((math.sqrt(2) - 1) ** 2)
    assert edge > 0.17
    assert marchenko_pastur_lower_edge(3.9) > edge


def test_vanishing_fraction_tiny_eigenvalues_do_not_prevent_trace_tail() -> None:
    row = audit_vanishing_fraction_hard_edge(
        "OUTLIERS",
        4096,
        64,
        4096**-6,
        4096**-4,
    )
    assert row.minimum_edge_vanishes
    assert row.tail_bound_verified
    assert row.normalized_tail_vanishes_with_contamination_fraction
    assert row.exact_normalized_support_ridge_tail <= 2 / math.sqrt(4096)


def test_fixed_threshold_and_inverse_polynomial_eta_give_tail_split() -> None:
    row = fixed_moment_tail_scaling_record(
        1024,
        3.0,
        assumed_expected_small_eigenvalue_density=1e-3,
    )
    assert row.chosen_fixed_threshold < row.uniform_mp_lower_edge
    assert row.ridge_to_fixed_threshold_squared < 1e-20
    assert row.resulting_single_frame_tail_upper_bound == pytest.approx(1e-3)
    assert not row.growing_moment_edge_required
    assert not row.global_distinct_raw_moment_transfer_required


def test_report_keeps_all_fixed_moment_and_ridge_curl_premises_open() -> None:
    report = run_component_dependency_ridge_moment_method_bridge()
    assert report.headline_metrics[
        "all_fixed_moment_to_tail_bridge_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["all_fixed_moments_would_suffice_for_trace_tail"]
    assert not report.claim_gate[
        "growing_moment_spectral_edge_required_for_trace_tail"
    ]
    assert not report.claim_gate["globally_distinct_raw_moment_control_required"]
    assert report.claim_gate["independent_moments_through_order_four_proved"]
    assert not report.claim_gate["all_fixed_independent_moments_proved"]
    assert not report.claim_gate["natural_child_frame_weak_mp_law_proved"]
    assert not report.claim_gate["natural_ridge_curl_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_scope_is_constant_signal_without_moment_rate() -> None:
    theorem = dependency_ridge_moment_method_bridge_theorem()
    assert theorem.theorem_verified
    assert theorem.constant_signal_only_without_rate
    assert not theorem.growing_moment_edge_required
    assert "every fixed k" in theorem.all_fixed_moment_premise
    assert "n^-a" in theorem.inverse_polynomial_ridge_consequence
