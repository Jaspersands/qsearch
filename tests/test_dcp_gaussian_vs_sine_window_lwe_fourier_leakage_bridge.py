"""Unit tests for the DCP discrete Gaussian vs. sine vs. box window bridge (Subsystem 89)."""

from __future__ import annotations

from theorems.dcp_gaussian_vs_sine_window_lwe_fourier_leakage_bridge import (
    evaluate_window_family_comparison,
    generate_dcp_gaussian_vs_sine_window_lwe_fourier_leakage_certificate,
)


def test_window_family_comparison() -> None:
    res = evaluate_window_family_comparison(p_len=16, gaussian_sigma_ratio=0.45)
    assert res["exact_optimality_verified"] is True
    assert res["gamma1_box"] < res["gamma1_truncated_gaussian"] < res["gamma1_sine_optimal_closed_form"]


def test_certificate_generation() -> None:
    cert = generate_dcp_gaussian_vs_sine_window_lwe_fourier_leakage_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
