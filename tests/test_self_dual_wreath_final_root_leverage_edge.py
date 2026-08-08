import math

import pytest
from scipy.stats import beta

from self_dual_wreath_final_root_leverage_edge import (
    audit_haar_leverage_control,
    beta_lower_tail_union_log2_bound,
    final_root_leverage_scaling_record,
    run_final_root_leverage_edge,
)


def test_beta_chernoff_union_bound_dominates_exact_marginal_union_bound() -> None:
    coefficient_dimension = 64
    fiber_dimension = 24
    alpha = fiber_dimension / coefficient_dimension
    threshold = alpha / 2
    theorem_log2 = beta_lower_tail_union_log2_bound(
        coefficient_dimension,
        fiber_dimension,
        threshold,
    )
    exact_union = min(
        1.0,
        coefficient_dimension
        * beta.cdf(
            threshold,
            fiber_dimension,
            coefficient_dimension - fiber_dimension,
        ),
    )
    assert math.log2(exact_union) <= theorem_log2 + 1e-12
    assert theorem_log2 < 0


def test_k_plus_two_final_root_has_uniform_component_aspect() -> None:
    for n in (3, 4, 6, 8, 12, 20, 32, 48):
        row = final_root_leverage_scaling_record(n)
        assert row.selected_copy_count == row.information_threshold_copy_count + 2
        assert 2 <= row.final_child_coefficient_to_physical_aspect < 4
        assert 0.25 < row.common_fiber_aspect <= 0.5
        if n >= 4:
            assert row.positive_defect_gap_on_edge_event


def test_finite_haar_control_has_exact_povm_and_observed_edge_event() -> None:
    control = audit_haar_leverage_control(
        "test",
        64,
        24,
        seed=301,
    )
    assert control.exact_component_povm_verified
    assert control.component_effect_sum_identity_residual < 1e-12
    assert control.every_component_above_half_mean
    assert control.minimum_row_leverage > control.half_mean_edge_threshold
    assert control.aggregate_defect_minimum_eigenvalue >= (
        control.aggregate_defect_theorem_lower_bound - 1e-12
    )


def test_report_keeps_natural_transfer_and_algorithm_gates_closed() -> None:
    report = run_final_root_leverage_edge()
    assert report.claim_gate[
        "existing_k_plus_two_schedule_bounds_surrogate_final_root_component_aspect"
    ]
    assert report.claim_gate[
        "haar_final_root_minimum_component_edge_is_constant_with_high_probability"
    ]
    assert report.claim_gate[
        "haar_final_root_aggregate_defect_has_constant_gap"
    ]
    assert not report.claim_gate["natural_final_root_component_edge_proved"]
    assert not report.claim_gate[
        "natural_all_relation_node_component_edges_proved"
    ]
    assert not report.claim_gate["regular_master_central_support_controlled"]
    assert not report.claim_gate["natural_component_support_select_compiled"]
    assert not report.claim_gate["recursive_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
