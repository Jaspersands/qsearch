"""Unit tests for the DCP Kitaev X/Y vs. coherent R_Z feedforward bridge (Subsystem 111)."""

from __future__ import annotations

from theorems.dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge import (
    evaluate_kitaev_xy_vs_coherent_feedforward,
    generate_dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_certificate,
)


def test_kitaev_vs_coherent_feedforward() -> None:
    res = evaluate_kitaev_xy_vs_coherent_feedforward(gamma=0.8)
    assert res["all_verified"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
