"""Unit tests for the DCP [[2m + 2, 2m, 2]] Iceberg stabilizer code bridge (Subsystem 113)."""

from __future__ import annotations

from theorems.dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge import (
    evaluate_iceberg_code_z_fault_suppression,
    generate_dcp_quantum_z_error_detection_stabilizer_iceberg_code_certificate,
)


def test_iceberg_code_z_fault_suppression() -> None:
    res = evaluate_iceberg_code_z_fault_suppression(2, [0.0, 0.01])
    assert res["all_verified"] is True
    assert res["records"][1]["error_suppression_factor"] > 25.0


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_z_error_detection_stabilizer_iceberg_code_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
