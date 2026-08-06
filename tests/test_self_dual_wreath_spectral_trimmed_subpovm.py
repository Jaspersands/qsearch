import pytest

from self_dual_wreath_spectral_trimmed_subpovm import (
    finite_trim_control,
    run_spectral_trimmed_subpovm,
    trimmed_correct_success_lower_bound,
    wreath_frame_second_moment_per_rank,
    wreath_trimmed_scaling_record,
)


def test_wreath_second_moment_specialization_is_exact() -> None:
    hidden_count = 120
    copies = 7
    expected = (2**copies + hidden_count - 1) / (
        hidden_count * 2**copies
    )
    assert wreath_frame_second_moment_per_rank(
        hidden_count,
        copies,
    ) == pytest.approx(expected)


def test_information_threshold_success_is_uniformly_constant() -> None:
    for n in (3, 4, 5, 8, 16, 32, 64, 128):
        record = wreath_trimmed_scaling_record(n)
        assert 1 < record.hidden_count_times_second_moment_scale <= 2
        assert record.retained_average_trace_fraction_lower_bound == 0.5
        assert record.correct_label_success_probability_lower_bound >= 1 / 16
        assert record.universal_one_sixteenth_bound_verified


def test_finite_control_actually_clips_a_high_frame_sector() -> None:
    record = finite_trim_control(
        5,
        2,
        ((3, 1, 1), (3, 1, 1)),
    )
    assert record.clipped_eigenvalue_count == 2
    assert record.retained_average_trace_fraction >= 0.5
    assert (
        record.correct_label_success_probability
        >= record.correct_label_success_lower_bound
    )
    assert record.maximum_effect_completeness_violation < 1e-10
    assert record.exact_finite_trimmed_subpovm_validation


def test_report_keeps_circuit_and_decoder_gates_closed() -> None:
    report = run_spectral_trimmed_subpovm()
    metrics = report.headline_metrics
    assert metrics["finite_trimmed_subpovm_validation_failure_count"] == 0
    assert metrics["finite_control_with_nonempty_clipped_spectrum_count"] >= 1
    assert metrics["universal_one_sixteenth_scaling_row_count"] == metrics[
        "information_threshold_scaling_record_count"
    ]
    assert report.claim_gate["spectral_trimmed_subpovm_theorem_proved"]
    assert report.claim_gate[
        "constant_information_theoretic_correct_success_at_threshold_proved"
    ]
    assert not report.claim_gate[
        "large_frame_norm_implies_information_theoretic_failure"
    ]
    assert not report.claim_gate["exact_spectral_projector_circuit_proved"]
    assert not report.claim_gate["polynomial_outcome_transform_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_success_bound_rejects_nontrimming_multiplier() -> None:
    with pytest.raises(ValueError):
        trimmed_correct_success_lower_bound(100, 0.02, 1.0)
