import math

import pytest

from self_dual_wreath_pgm_truncation_robustness import (
    audit_physical_truncation,
    pgm_truncation_scaling_record,
    robust_cutoff,
    run_pgm_truncation_robustness,
    truncation_success_lower_bound,
)


THREE_UNEQUAL_TYPES = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_robust_cutoff_has_inverse_hypothesis_scale() -> None:
    hidden_count = math.factorial(12)
    cutoff = robust_cutoff(hidden_count, 0.1)

    assert cutoff == pytest.approx(0.01 / (4 * hidden_count))
    assert truncation_success_lower_bound(
        hidden_count,
        math.ceil(math.log2(hidden_count)),
        0.1,
    ) > 0.4


def test_physical_w3_truncation_obeys_rank_and_gentle_bounds() -> None:
    record = audit_physical_truncation(
        "test",
        THREE_UNEQUAL_TYPES,
        loss_budget_eta=0.5,
    )

    assert record.exact_truncation_robustness_verified
    assert record.discarded_average_input_mass <= record.discarded_mass_rank_upper_bound + 1e-10
    assert record.truncated_pgm_success_probability >= record.gentle_success_lower_bound - 1e-10
    assert record.maximum_effect_completeness_violation < 1e-9


def test_tail_scaling_removes_lambda_min_but_not_raw_normalization() -> None:
    record = pgm_truncation_scaling_record(512)

    assert record.cutoff_log2 < -3800
    assert record.truncated_pgm_success_lower_bound > 0.4
    assert not record.minimum_eigenvalue_required
    assert not record.normalization_one_qsvt_polynomial
    assert not record.polynomial_rescaled_frame_encoding_proved


def test_report_keeps_algorithm_gate_closed() -> None:
    report = run_pgm_truncation_robustness()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["inverse_label_scale_cutoff_suffices"]
    assert report.claim_gate["constant_truncated_pgm_success_proved"]
    assert not report.claim_gate["polynomial_rescaled_frame_encoding_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_loss_budget_is_rejected() -> None:
    with pytest.raises(ValueError, match="loss budget"):
        robust_cutoff(8, 1.0)
