"""Unit tests for the DCP non-stationary drifting secret tracking bridge (Subsystem 114)."""

from __future__ import annotations

from theorems.dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge import (
    evaluate_drifting_secret_velocity_locking,
    generate_dcp_non_stationary_markov_drift_secret_tracking_kalman_certificate,
)


def test_drifting_secret_velocity_locking() -> None:
    res = evaluate_drifting_secret_velocity_locking(8, 1, 0, 1, gamma=0.9)
    assert res["exact_drift_tracking_verified"] is True
    assert abs(res["static_time_averaged_x"]) < 1e-12
    assert abs(res["velocity_tracked_time_averaged_x"] - 0.9) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_non_stationary_markov_drift_secret_tracking_kalman_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
