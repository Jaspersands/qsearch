import pytest

from self_dual_wreath_cayley_fiber_reduction import (
    _generic_controls,
    audit_cayley_fiber_control,
    run_cayley_fiber_reduction,
)


def _distinct_triangle():
    return (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )


def test_scalar_cayley_kernel_predicts_common_modes_and_half_balance() -> None:
    cayley, _ = _generic_controls()

    assert cayley.scalar_cayley_fiber_certificate
    assert cayley.exact_walsh_common_mode_prediction
    assert cayley.internal_fiber_dimension == 2
    assert cayley.predicted_common_range_dimension == 2
    assert cayley.actual_common_range_dimension == 2
    saturated = [mode for mode in cayley.character_modes if mode.saturated_common_mode]
    assert len(saturated) == 1
    assert saturated[0].predicted_shorted_metric_scale == pytest.approx(1.0)
    assert cayley.actual_fractional_eigenvalues == pytest.approx((0.5, 0.5))


def test_scalar_but_noncayley_fibers_do_not_force_balance() -> None:
    _, noncayley = _generic_controls()

    assert noncayley.maximum_component_effect_scalar_residual < 1e-8
    assert noncayley.maximum_scalar_cross_gram_residual < 1e-8
    assert noncayley.maximum_cayley_translation_residual > 1e-3
    assert not noncayley.scalar_cayley_fiber_certificate
    assert any(
        abs(value - 0.5) > 1e-3
        for value in noncayley.actual_fractional_eigenvalues
    )


def test_distinct_w3_fibers_are_scalar_cayley_and_use_standard_carrier() -> None:
    record = audit_cayley_fiber_control(
        "distinct",
        3,
        (2, 1),
        _distinct_triangle(),
    )

    assert record.fractional_merge_count == 9
    assert record.scalar_cayley_certificate_failure_count == 0
    assert record.exact_walsh_prediction_failure_count == 0
    assert record.observed_active_supports == ((0, 2, 5, 7),)
    assert record.observed_pair_carrier_dimensions == (2,)
    assert all(row.exact_walsh_common_mode_prediction for row in record.records)


def test_repeated_labels_break_scalar_cayley_normal_form() -> None:
    record = audit_cayley_fiber_control(
        "repeated",
        3,
        (2, 1),
        (((3,), (2, 1)),) * 3,
    )

    assert record.scalar_cayley_certificate_failure_count > 0
    assert record.exact_walsh_prediction_failure_count > 0


def test_report_does_not_promote_finite_cayley_signal_to_algorithm() -> None:
    report = run_cayley_fiber_reduction()

    assert report.headline_metrics["label_simple_fractional_merge_count"] == 20
    assert report.headline_metrics[
        "label_simple_scalar_cayley_failure_count"
    ] == 0
    assert report.headline_metrics[
        "label_simple_walsh_prediction_failure_count"
    ] == 0
    assert report.headline_metrics[
        "maximum_finite_candidate_pair_carrier_dimension"
    ] == 2
    assert report.claim_gate["scalar_cayley_walsh_balance_theorem_proved"]
    assert report.claim_gate["finite_label_simple_scalar_cayley_signal"]
    assert not report.claim_gate[
        "all_n_collision_free_scalar_cayley_fibers_proved"
    ]
    assert not report.claim_gate[
        "polynomial_dimension_candidate_carriers_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
