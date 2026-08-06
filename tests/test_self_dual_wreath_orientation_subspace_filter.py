import numpy as np

from self_dual_wreath_orientation_subspace_filter import (
    audit_orientation_subspace_filter,
    orientation_fourier_kraus,
    run_orientation_subspace_filter,
    synthetic_common_core_control,
)


def test_character_kraus_parseval_identity_for_noncommuting_projectors() -> None:
    control = synthetic_common_core_control()
    assert control.exact_filter_identity_verified
    assert control.common_range_dimension == 1
    assert control.common_range_annihilation_residual < 1e-12
    assert control.nontrivial_character_effect_top_eigenvalue <= 0.25 + 1e-12


def test_two_projector_filter_matches_squared_difference() -> None:
    first = np.diag([1.0, 1.0, 0.0])
    vector = np.asarray([1.0, 0.0, 1.0]) / np.sqrt(2)
    second = np.outer(vector, vector) + np.diag([0.0, 1.0, 0.0])
    kraus = orientation_fourier_kraus((first, second))
    expected = (first - second) @ (first - second) / 4
    assert np.allclose(kraus[1].T @ kraus[1], expected)
    control = audit_orientation_subspace_filter(
        (first, second),
        control_id="two-projector",
        source="unit-test",
    )
    assert control.exact_filter_identity_verified


def test_physical_wreath_controls_validate_filter_identity() -> None:
    report = run_orientation_subspace_filter()
    assert report.headline_metrics["physical_w4_control_count"] == 75
    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.headline_metrics["common_range_control_count"] > 0
    assert report.claim_gate["orientation_fourier_filter_identity_proved"]


def test_report_opens_implementation_but_keeps_information_and_decoder_closed() -> None:
    report = run_orientation_subspace_filter()
    assert report.claim_gate[
        "polynomial_controlled_invariant_projector_proved"
    ]
    assert not report.claim_gate["all_n_near_common_spectrum_controlled"]
    assert not report.claim_gate["end_to_end_hidden_label_measurement_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
