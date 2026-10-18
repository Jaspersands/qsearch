"""Unit tests for the DCP noisy syndrome measurement readout bit-flip bridge (Subsystem 88)."""

from __future__ import annotations

from theorems.dcp_noisy_syndrome_measurement_readout_bitflip_bridge import (
    evaluate_syndrome_readout_bitflip_and_parity_verification,
    generate_dcp_noisy_syndrome_measurement_readout_bitflip_certificate,
)


def test_readout_bitflip_and_parity_verification() -> None:
    res = evaluate_syndrome_readout_bitflip_and_parity_verification([0.0, 0.05, 0.50], gamma=0.9)
    assert res["all_verified"] is True
    rec05 = res["records"][1]
    assert rec05["error_rate_reduction_factor"] > 18.0


def test_certificate_generation() -> None:
    cert = generate_dcp_noisy_syndrome_measurement_readout_bitflip_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
