"""Unit tests for the DCP quantum rejection sampling box-to-sine window bridge (Subsystem 98)."""

from __future__ import annotations

from theorems.dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_bridge import (
    evaluate_quantum_rejection_sampling_box_to_target,
    generate_dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_certificate,
)


def test_box_to_sine_acceptance() -> None:
    res = evaluate_quantum_rejection_sampling_box_to_target(p_len=15, lorentzian_width_ratio=0.20)
    assert res["exact_laws_verified"] is True
    assert abs(res["p_accept_sine_explicit"] - 16.0 / 30.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
