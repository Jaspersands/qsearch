import numpy as np
import pytest

from self_dual_wreath_component_green_ridge_stability import (
    _random_projection_frame,
    audit_green_ridge_stability,
    audit_povm_commutator_stability,
    green_and_ridge_syntheses,
    polynomial_ridge_schedule_record,
    run_component_green_ridge_stability,
)


def test_ridge_normalization_produces_two_exact_povms() -> None:
    leaves, common = _random_projection_frame(809)
    *_, exact, ridge = green_and_ridge_syntheses(leaves, common, 1e-4)
    identity = np.eye(common.shape[1])

    assert sum(exact) == pytest.approx(identity, abs=1e-9)
    assert sum(ridge) == pytest.approx(identity, abs=1e-9)


def test_outcome_count_free_povm_commutator_stability() -> None:
    leaves, common = _random_projection_frame(
        817,
        ambient_dimension=9,
        common_fiber_dimension=4,
        leaf_count=8,
        leaf_rank=3,
    )
    *_, exact, ridge = green_and_ridge_syntheses(leaves, common, 2e-5)
    row = audit_povm_commutator_stability("EIGHT-OUTCOMES", exact, ridge)

    assert row.outcome_count == 8
    assert row.stability_bound_verified is True
    assert row.normalized_commutator_moment_difference <= (
        row.outcome_count_free_stability_upper_bound
    )


def test_complete_ridge_perturbation_chain_holds() -> None:
    leaves, common = _random_projection_frame(809)
    row = audit_green_ridge_stability(
        "RIDGE-CONTROL",
        leaves,
        common,
        1e-4,
    )

    assert row.perturbation_premise_satisfied is True
    assert row.exact_ridge_operator_error == pytest.approx(
        row.ridge_operator_error_formula,
        rel=1e-8,
    )
    assert row.common_metric_perturbation <= (
        row.common_metric_perturbation_upper_bound
    )
    assert row.exact_synthesis_operator_error <= (
        row.synthesis_operator_error_upper_bound
    )
    assert row.summed_effect_hilbert_schmidt_error <= (
        row.synthesis_to_effect_error_upper_bound
    )
    assert row.normalized_commutator_moment_difference <= row.povm_stability_upper_bound
    assert row.normalized_commutator_moment_difference <= (
        row.synthesis_stability_upper_bound
    )
    assert row.summed_effect_hilbert_schmidt_error <= (
        row.frame_weighted_effect_error_upper_bound
    )
    assert row.normalized_commutator_moment_difference <= (
        row.frame_weighted_commutator_stability_upper_bound
    )
    assert row.exact_prepolar_ridge_frobenius_error == pytest.approx(
        row.trace_formula_prepolar_ridge_frobenius_error,
        rel=1e-8,
    )
    assert row.frame_weighted_synthesis_frobenius_error <= (
        row.polar_factor_frobenius_error_upper_bound
    )
    assert row.normalized_commutator_moment_difference <= (
        row.trace_weighted_commutator_transfer_upper_bound
    )
    assert row.complete_ridge_stability_chain_verified is True


def test_ridge_synthesis_and_moment_converge_as_eta_decreases() -> None:
    leaves, common = _random_projection_frame(823)
    coarse = audit_green_ridge_stability(
        "COARSE",
        leaves,
        common,
        1e-4,
    )
    fine = audit_green_ridge_stability(
        "FINE",
        leaves,
        common,
        2e-5,
    )

    assert fine.exact_synthesis_operator_error < coarse.exact_synthesis_operator_error
    assert fine.normalized_commutator_moment_difference < (
        coarse.normalized_commutator_moment_difference
    )


def test_polynomial_schedule_exposes_required_edge_exponents() -> None:
    row = polynomial_ridge_schedule_record(2, 1, 2, 3)

    assert row.regularization_exponent_must_exceed == pytest.approx(6.5)
    assert row.polynomial_ridge_schedule_exists_conditionally is True
    assert row.natural_frame_edge_proved is False
    assert row.natural_common_metric_edge_proved is False
    assert row.natural_average_synthesis_error_proved is False


def test_report_keeps_both_natural_ridge_obligations_open() -> None:
    report = run_component_green_ridge_stability()

    assert report.status == (
        "green-ridge-M4-stability-proved-natural-ridge-correlations-open"
    )
    assert report.headline_metrics[
        "outcome_count_free_component_M4_stability_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "green_ridge_synthesis_perturbation_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "average_ridge_to_exact_M4_transfer_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "trace_weighted_polar_ridge_transfer_theorem_count"
    ] == 1
    assert report.headline_metrics["povm_control_failure_count"] == 0
    assert report.headline_metrics["ridge_control_failure_count"] == 0
    assert report.claim_gate[
        "average_error_route_avoids_uniform_edge_requirement"
    ] is True
    assert report.claim_gate[
        "trace_weighted_polar_ratio_is_exact_remaining_approximation_target"
    ] is True
    assert report.claim_gate["natural_average_green_to_ridge_error_small"] is False
    assert report.claim_gate["natural_leaf_marked_ridge_gap_positive"] is False
    assert report.claim_gate["natural_independent_plancherel_M4_positive"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
