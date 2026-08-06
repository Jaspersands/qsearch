import math

import pytest

from self_dual_wreath_matrix_cayley_boundary import (
    _matrix_cayley_control,
    run_matrix_cayley_boundary,
)


def test_commuting_matrix_cayley_saturation_remains_balanced() -> None:
    record = _matrix_cayley_control("commuting", nonorthogonal=False)

    assert record.matrix_cayley_boundary_theorem_verified
    assert not record.scalar_cayley_kernel
    assert record.all_character_operators_commute
    assert record.opposite_saturation_spaces_orthogonal
    assert record.maximum_opposite_saturation_overlap < 1e-8
    assert record.actual_common_range_dimension == 2
    assert record.predicted_common_range_dimension == 2
    assert record.actual_fractional_eigenvalues == pytest.approx((0.5, 0.5))


def test_noncommuting_matrix_cayley_covariance_can_be_nonneutral() -> None:
    record = _matrix_cayley_control("counter", nonorthogonal=True)

    assert record.matrix_cayley_boundary_theorem_verified
    assert record.maximum_matrix_cayley_translation_residual < 1e-8
    assert record.maximum_leaf_isometry_residual < 1e-8
    assert not record.scalar_cayley_kernel
    assert not record.all_character_operators_commute
    assert not record.opposite_saturation_spaces_orthogonal
    assert not record.all_fractional_channels_half
    assert record.maximum_opposite_saturation_overlap == pytest.approx(
        1 / math.sqrt(2)
    )
    assert record.grading_neutrality_residual == pytest.approx(
        1 / math.sqrt(2)
    )


def test_saturation_overlap_formula_predicts_every_nonhalf_channel() -> None:
    record = _matrix_cayley_control("counter", nonorthogonal=True)
    expected = (
        (1 - 1 / math.sqrt(2)) / 2,
        (1 + 1 / math.sqrt(2)) / 2,
    )

    assert record.actual_fractional_eigenvalues == pytest.approx(expected)
    assert record.predicted_fractional_eigenvalues == pytest.approx(expected)
    assert record.maximum_fractional_spectrum_residual < 1e-8


def test_report_keeps_natural_wreath_and_circuit_claims_open() -> None:
    report = run_matrix_cayley_boundary()

    assert report.headline_metrics["matrix_cayley_boundary_theorem_count"] == 1
    assert report.headline_metrics["theorem_validation_failure_count"] == 0
    assert report.headline_metrics[
        "noncommuting_nonneutral_counterexample_count"
    ] == 1
    assert report.claim_gate["matrix_cayley_saturation_boundary_proved"]
    assert not report.claim_gate[
        "matrix_cayley_covariance_alone_suffices_for_balance"
    ]
    assert not report.claim_gate[
        "natural_collision_free_saturation_orthogonality_proved"
    ]
    assert not report.claim_gate["coherent_internal_saturation_projectors_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
