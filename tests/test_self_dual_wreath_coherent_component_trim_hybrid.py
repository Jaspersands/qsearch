import math

import numpy as np
import pytest

from self_dual_wreath_coherent_component_trim_hybrid import (
    NATURAL_FINAL_FIBER_ASPECT_LOWER,
    audit_coherent_branch_trim,
    coherent_trim_scaling_record,
    natural_final_root_branch_averaged_threshold,
    postselection_flatness_counterexample,
    run_coherent_component_trim_hybrid,
    write_coherent_component_trim_hybrid_report,
)


def _low_edge_povm():
    low = np.diag([0.03, 0.0]).astype(complex)
    return low, np.eye(2, dtype=complex) - low


def test_exact_branch_error_identity_uses_unnormalized_child_states():
    identity = np.eye(2, dtype=complex)
    endpoints = (identity / math.sqrt(2), identity / math.sqrt(2))
    control = audit_coherent_branch_trim(
        "DIRECT",
        endpoints,
        (_low_edge_povm(), _low_edge_povm()),
        identity / 2,
        (0.1, 0.1),
    )
    assert control.exact_control_verified
    assert control.exact_error_identity_verified
    assert control.conditional_and_parent_bounds_verified
    assert not control.child_postselection_flatness_required
    assert control.exact_branch_averaged_failure == pytest.approx(0.015)
    assert control.exact_branch_averaged_failure == pytest.approx(
        control.exact_ideal_to_trimmed_mean_square_error
    )
    assert control.exact_branch_averaged_failure <= (
        control.endpoint_weighted_parent_bound
    )


def test_parent_flatness_bound_allows_unequal_output_dimensions():
    first = np.asarray([[1.0, 0.0]], dtype=complex)
    second = np.asarray([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    first_povm = (np.asarray([[0.04]], dtype=complex), np.asarray([[0.96]], dtype=complex))
    second_povm = _low_edge_povm()
    control = audit_coherent_branch_trim(
        "RECTANGULAR",
        (first, second),
        (first_povm, second_povm),
        np.eye(2, dtype=complex) / 2,
        (0.1, 0.1),
    )
    assert control.exact_control_verified
    assert tuple(row.output_dimension for row in control.branch_details) == (1, 2)
    assert control.endpoint_column_isometry_residual == pytest.approx(0.0)


@pytest.mark.parametrize("dimension", (2, 4, 16, 256, 1024))
def test_postselection_can_create_linear_flatness_from_isotropic_parent(dimension):
    row = postselection_flatness_counterexample(dimension)
    assert row.conditional_child_flatness > dimension - 1
    assert row.rare_branch_probability < 2 / dimension
    assert row.branch_probability_times_conditional_flatness == pytest.approx(1.0)
    assert row.endpoint_column_isometry_exact


def test_final_root_branch_averaged_cutoff_is_constant_for_isotropic_parent():
    eta = 0.1
    threshold = natural_final_root_branch_averaged_threshold(eta, 1.0)
    assert threshold == pytest.approx(
        eta * float(NATURAL_FINAL_FIBER_ASPECT_LOWER) / 2
    )
    aggregate_budget_ratio = 2 / float(NATURAL_FINAL_FIBER_ASPECT_LOWER)
    assert threshold * aggregate_budget_ratio == pytest.approx(eta)
    with pytest.raises(ValueError, match="flatness"):
        natural_final_root_branch_averaged_threshold(eta, 0.5)


def test_level_hybrid_uses_inverse_polynomial_threshold_conditionally():
    row = coherent_trim_scaling_record(32)
    assert row.inverse_polynomial_threshold_conditional_on_level_budget
    assert row.hybrid_total_mean_square_error_upper_bound == pytest.approx(
        row.total_mean_square_error_target
    )
    assert not row.natural_root_flatness_proved
    assert not row.polynomial_all_level_rank_budget_proved
    assert not row.coherent_recursive_trim_compiled


def test_report_replaces_only_the_child_flatness_gate(tmp_path):
    report = run_coherent_component_trim_hybrid()
    assert report.theorem.theorem_verified
    assert report.theorem.child_postselection_flatness_eliminated
    assert report.theorem.ideal_isometric_prefix_hybrid_proved
    assert not report.theorem.natural_root_flatness_proved
    assert not report.theorem.polynomial_all_level_rank_budget_proved
    assert not report.theorem.recursive_component_compiler_proved
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert not report.claim_gate["postselected_child_flatness_required"]
    assert not report.claim_gate["natural_root_state_polynomially_flat"]
    assert not report.claim_gate[
        "polynomial_all_level_component_rank_budget_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coherent_component_trim_hybrid_report(
        tmp_path / "coherent-trim.json"
    )
    assert payload["status"] == (
        "child-flatness-gate-replaced-by-root-and-level-rank-budgets"
    )
