import math

from self_dual_wreath_trace_weighted_pgm_bridge import (
    audit_physical_trace_weighted_bridge,
    run_trace_weighted_pgm_bridge,
)


W3_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_physical_average_error_is_discarded_rescaled_frame_mass() -> None:
    controls = audit_physical_trace_weighted_bridge(
        3,
        W3_LABELS,
        1.5,
        control_prefix="TEST-W3",
    )
    assert controls
    assert any(row.discarded_rescaled_frame_mass > 0 for row in controls)
    for row in controls:
        assert row.exact_physical_trace_weighted_bridge_verified
        assert math.isclose(
            row.physical_average_polar_error,
            row.discarded_rescaled_frame_mass,
            abs_tol=1e-8,
        )
        assert math.isclose(
            row.physical_average_failure_probability,
            row.discarded_rescaled_frame_mass,
            abs_tol=1e-8,
        )


def test_raw_frame_cutoff_scale_includes_orientation_count() -> None:
    controls = audit_physical_trace_weighted_bridge(
        3,
        W3_LABELS,
        1.5,
        control_prefix="TEST-SCALE",
    )
    for row in controls:
        assert math.isclose(
            row.corresponding_raw_frame_threshold,
            row.truncation_threshold / row.orientation_count,
        )
        assert math.isclose(
            row.minimum_positive_raw_frame_eigenvalue,
            row.minimum_positive_rescaled_frame_eigenvalue / row.orientation_count,
            abs_tol=1e-8,
        )


def test_bridge_report_closes_only_the_physical_weighting_gate() -> None:
    report = run_trace_weighted_pgm_bridge()
    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.headline_metrics["finite_nonzero_discard_control_count"] > 0
    assert report.claim_gate["physical_average_state_bridge_proved"]
    assert report.claim_gate["pointwise_fourier_sector_bridge_proved"]
    assert not report.claim_gate["same_absolute_cutoff_on_raw_pgm_frame_allowed"]
    assert not report.claim_gate[
        "tightly_normalized_orientation_polar_access_proved"
    ]
    assert not report.claim_gate["polynomial_physical_pgm_circuit_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
