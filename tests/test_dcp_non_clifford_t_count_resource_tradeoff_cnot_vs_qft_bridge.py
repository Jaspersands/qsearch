"""Unit tests for the DCP non-Clifford T-count resource tradeoff bridge (Subsystem 124)."""

from __future__ import annotations

from theorems.dcp_non_clifford_t_count_resource_tradeoff_cnot_vs_qft_bridge import (
    evaluate_qft_vs_adaptive_peeling_non_clifford_resources,
    generate_dcp_non_clifford_t_count_resource_tradeoff_cnot_vs_qft_certificate,
)


def test_non_clifford_resource_tradeoff() -> None:
    res = evaluate_qft_vs_adaptive_peeling_non_clifford_resources([8, 32])
    assert res["all_verified"] is True
    assert abs(res["records"][1]["fine_rotation_reduction_factor"] - 31.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_non_clifford_t_count_resource_tradeoff_cnot_vs_qft_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
