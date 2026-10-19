"""Unit tests for the DCP Bucket-Brigade vs. Fanout qRAM routing fault scaling bridge (Subsystem 137)."""

from __future__ import annotations

from theorems.dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_bridge import (
    evaluate_bucket_brigade_vs_fanout_qram_fidelity,
    generate_dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_certificate,
)


def test_bucket_brigade_vs_fanout_qram() -> None:
    res = evaluate_bucket_brigade_vs_fanout_qram_fidelity([1, 10], eps_active=1e-3, eps_wait=0.0)
    assert res["all_verified"] is True
    assert res["records"][1]["infidelity_reduction_ratio_fanout_over_bb"] > 64.0


def test_certificate_generation() -> None:
    cert = generate_dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
