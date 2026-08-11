import pytest

from coset_multiplicity_whitening_copy_window import (
    build_coset_multiplicity_whitening_copy_window_report,
    copy_window_scaling_record,
    exact_expected_multiplicity_dimension_ratio,
    robinson_schensted_control,
    symmetric_group_involution_count,
    write_coset_multiplicity_whitening_copy_window_report,
)


def test_robinson_schensted_dimension_identity_controls():
    for n in range(1, 11):
        row = robinson_schensted_control(n)
        assert row.identity_verified
        assert row.involution_count == row.sum_irrep_dimensions
    assert symmetric_group_involution_count(5) == 26


def test_exact_natural_dimension_expectation_matches_small_controls():
    assert exact_expected_multiplicity_dimension_ratio(5, 1) == pytest.approx(
        52 / 120
    )
    assert exact_expected_multiplicity_dimension_ratio(5, 3) == pytest.approx(
        208 / 120
    )


def test_copy_window_has_rigorous_sqrt_n_bounds_and_constant_pgm_success():
    row = copy_window_scaling_record(256)
    assert row.lower_bound_below_exact
    assert row.exact_below_upper_bound
    assert row.window_is_sqrt_n_asymptotically
    assert row.copy_window_width > 10
    assert row.expected_raw_rank_upper_at_safe_width <= 1.0 + 1e-10
    assert row.pgm_success_lower_bound_at_pgm_width > 0.5
    assert row.expected_raw_rank_upper_at_pgm_width > 1.0


def test_copy_window_rejects_sizes_outside_elementary_certificate():
    with pytest.raises(ValueError, match="multiple of four"):
        copy_window_scaling_record(10)


def test_report_preserves_actual_rank_and_circuit_open_gates(tmp_path):
    report = build_coset_multiplicity_whitening_copy_window_report()
    assert report.theorem.theorem_verified
    assert report.theorem.exact_expected_multiplicity_dimension_identity_proved
    assert report.theorem.actual_support_rank_upper_bound_proved
    assert report.theorem.theta_sqrt_n_copy_window_proved
    assert not report.theorem.actual_multiplicity_rank_lower_bound_proved
    assert not report.theorem.polynomial_whitening_at_pgm_width_proved
    assert not report.theorem.polynomial_hidden_involution_algorithm_proved
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics[
        "maximum_finite_support_to_dimension_ratio"
    ] <= 1.0 + 1e-10

    payload = write_coset_multiplicity_whitening_copy_window_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "covariant-whitening-copy-window-sharp-actual-rank-open"
    )
