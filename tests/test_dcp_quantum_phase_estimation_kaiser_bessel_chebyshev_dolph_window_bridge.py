"""Unit tests for the DCP Dolph-Chebyshev minimax equiripple window bridge (Subsystem 133)."""

from __future__ import annotations

from theorems.dcp_quantum_phase_estimation_kaiser_bessel_chebyshev_dolph_window_bridge import (
    evaluate_dolph_chebyshev_vs_sine_and_box_sidelobes,
    generate_dcp_quantum_phase_estimation_kaiser_bessel_chebyshev_dolph_window_certificate,
)


def test_dolph_chebyshev_sidelobes() -> None:
    res = evaluate_dolph_chebyshev_vs_sine_and_box_sidelobes(16, 30.0)
    assert res["exact_minimax_laws_verified"] is True
    assert res["peak_stopband_power_dolph_chebyshev"] < res["peak_stopband_power_sine"]


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_phase_estimation_kaiser_bessel_chebyshev_dolph_window_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
