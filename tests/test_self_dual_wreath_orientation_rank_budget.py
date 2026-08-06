from self_dual_wreath_orientation_rank_budget import (
    audit_trace_rank_control,
    rank_budget_scaling_record,
    run_orientation_rank_budget,
    trace_high_spectrum_count_bound,
)


def test_trace_bound_and_orientation_rank_capacity_match() -> None:
    eigenvalues = (0.45, 0.25, 0.1, 0.08, 0.05, 0.03, 0.02, 0.02)
    control = audit_trace_rank_control(
        eigenvalues,
        1,
        control_id="TRACE-RANK",
    )
    assert trace_high_spectrum_count_bound(8, 2) == 4
    assert control.high_eigenvalue_count == 1
    assert control.orientation_rejection_rank == 4
    assert control.rank_capacity_covers_high_spectrum
    assert control.trace_count_bound_verified


def test_logarithmic_subspace_balances_rank_and_retention() -> None:
    record = rank_budget_scaling_record(512)
    assert record.orientation_subspace_dimension == 72
    assert record.orientation_subspace_dimension < record.information_threshold_copy_count
    assert record.rejected_hilbert_fraction_log2 == -72
    assert record.trace_high_spectrum_fraction_upper_bound_log2 == -72
    assert record.rejection_rank_matches_trace_bound
    assert record.high_probability_retention_certified
    assert record.markov_failure_probability_log2_upper_bound < -30
    assert not record.legacy_rank_budget_covers_same_polynomial_tail_from_trace_alone
    assert not record.source_adapted_alignment_proved


def test_report_changes_default_regime_without_opening_claim_gate() -> None:
    report = run_orientation_rank_budget()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["separated_logarithmic_window_count"] == 7
    assert report.headline_metrics[
        "legacy_linear_rank_insufficient_from_trace_only_count"
    ] == 4
    assert report.claim_gate["trace_rank_calibration_proved"]
    assert not report.claim_gate["linear_dimension_subspace_is_default_choice"]
    assert not report.claim_gate["source_adapted_high_spectrum_alignment_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
