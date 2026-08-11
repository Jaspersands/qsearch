import math

import pytest

from dcp_polynomial_feature_contraction_no_go import (
    audit_feature_rank_trace_control,
    polynomial_feature_contraction_theorem,
    polynomial_feature_record_lower_bound,
    run_polynomial_feature_contraction_no_go,
    scaling_record,
    trace_rank_frobenius_lower_bound,
)


def test_trace_rank_bound_uses_diagonal_mass() -> None:
    assert trace_rank_frobenius_lower_bound([2.0, 2.0, 2.0], 2) == pytest.approx(18.0)
    with pytest.raises(ValueError, match="nonempty"):
        trace_rank_frobenius_lower_bound([], 2)
    with pytest.raises(ValueError, match="nonnegative"):
        trace_rank_frobenius_lower_bound([1.0, -1.0], 2)


def test_record_lower_bound_recovers_rank_one_formula() -> None:
    assert polynomial_feature_record_lower_bound(64, 3, 1) == 12 * 64 * 9
    assert polynomial_feature_record_lower_bound(64, 3, 4) == 12 * 64 * 9 / 4
    with pytest.raises(ValueError, match="positive"):
        polynomial_feature_record_lower_bound(0, 3, 1)


def test_finite_controls_verify_euler_rank_and_covariance_steps() -> None:
    for feature_rank, degree in ((2, 2), (3, 3), (5, 4)):
        control = audit_feature_rank_trace_control(
            f"rank-{feature_rank}-degree-{degree}",
            hidden_count=4 * feature_rank,
            feature_rank=feature_rank,
            degree=degree,
            response_support_size=2 * feature_rank,
            seed=100 + feature_rank,
        )
        assert control.response_gradient_euler_residual < 1e-9
        assert control.gradient_response_matrix_rank <= feature_rank
        assert control.trace_rank_inequality_verified
        assert control.first_projection_inequality_verified
        assert control.covariance_minimum_eigenvalue >= -1e-9


def test_inverse_polynomial_coverage_still_forces_exponential_records() -> None:
    row = scaling_record(
        n_bits=512,
        degree_power=1,
        feature_rank_power=8,
        response_coverage_power=8,
        polynomial_record_budget_power=20,
    )
    assert row.response_support_log2_lower_bound == pytest.approx(
        512 - 8 * math.log2(512)
    )
    assert row.log2_record_lower_bound > row.log2_polynomial_record_budget
    assert not row.polynomial_records_possible


def test_theorem_closes_polynomial_rank_but_not_adaptive_or_collective() -> None:
    theorem = polynomial_feature_contraction_theorem()
    assert theorem.arbitrary_symmetric_multilinear_form
    assert theorem.arbitrary_signed_coefficients
    assert theorem.polynomial_rank_component_cancellation_covered
    assert theorem.inverse_polynomial_response_support_closed
    assert not theorem.adaptive_estimators_closed
    assert not theorem.collective_quantum_measurements_closed


def test_report_keeps_speedup_gate_closed() -> None:
    report = run_polynomial_feature_contraction_no_go(n_values=(64, 128))
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "proved_polynomial_rank_signed_contraction_lower_bound_count"
    ] == 1
    assert report.claim_gate[
        "polynomial_rank_signed_contractions_closed_under_mse_contract"
    ]
    assert not report.claim_gate["adaptive_estimators_closed"]
    assert not report.claim_gate["collective_quantum_measurements_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
