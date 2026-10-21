"""Unit tests for the DCP radix-4 quaternary QFT butterfly bridge (Subsystem 119)."""

from __future__ import annotations

from theorems.dcp_radix_4_quaternary_qft_butterfly_depth_halving_bridge import (
    evaluate_radix4_vs_radix2_qft_butterfly_and_truncation,
    generate_dcp_radix_4_quaternary_qft_butterfly_depth_halving_certificate,
)


def test_radix4_butterfly_and_truncation() -> None:
    res = evaluate_radix4_vs_radix2_qft_butterfly_and_truncation(2, target_freq_y=4)
    assert res["exact_laws_verified"] is True
    assert abs(res["prob_radix4_band1_local_qft4_blocks"] - 1.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_radix_4_quaternary_qft_butterfly_depth_halving_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
