"""Unit tests for the DCP fixed-point pi/3 Grover syndrome amplification bridge (Subsystem 118)."""

from __future__ import annotations

from theorems.dcp_fixed_point_pi_over_3_grover_syndrome_amplification_bridge import (
    evaluate_pi_over_3_fixed_point_amplification,
    generate_dcp_fixed_point_pi_over_3_grover_syndrome_amplification_certificate,
)


def test_pi_over_3_weight2_amplification() -> None:
    res = evaluate_pi_over_3_fixed_point_amplification([0.50, 0.75])
    assert res["all_verified"] is True
    assert abs(res["records"][0]["p1_pi_over_3_explicit"] - 0.875) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_fixed_point_pi_over_3_grover_syndrome_amplification_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
