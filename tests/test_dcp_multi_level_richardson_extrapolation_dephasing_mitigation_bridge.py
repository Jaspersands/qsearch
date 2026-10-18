"""Unit tests for the DCP multi-level Richardson extrapolation dephasing mitigation bridge (Subsystem 103)."""

from __future__ import annotations

from theorems.dcp_multi_level_richardson_extrapolation_dephasing_mitigation_bridge import (
    evaluate_richardson_zne_dephasing_mitigation,
    generate_dcp_multi_level_richardson_extrapolation_dephasing_mitigation_certificate,
)


def test_richardson_zne_dephasing_mitigation() -> None:
    res = evaluate_richardson_zne_dephasing_mitigation(alpha_h=0.10, theta=0.0, max_order_m=3)
    assert res["all_verified"] is True
    assert res["order_records"][2]["absolute_bias"] < 0.01 * res["order_records"][0]["absolute_bias"]


def test_certificate_generation() -> None:
    cert = generate_dcp_multi_level_richardson_extrapolation_dephasing_mitigation_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
