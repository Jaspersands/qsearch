"""Unit tests for the DCP coherent Grover-BHMT syndrome amplification bridge (Subsystem 117)."""

from __future__ import annotations

from theorems.dcp_quantum_amplitude_amplification_grover_reflection_witness_bridge import (
    evaluate_coherent_grover_syndrome_amplification,
    generate_dcp_quantum_amplitude_amplification_grover_reflection_witness_certificate,
)


def test_weight3_deterministic_amplification() -> None:
    res = evaluate_coherent_grover_syndrome_amplification(5, [1, 1, 1], 3, [0, 1], k_steps=1)
    assert res["exact_laws_verified"] is True
    assert abs(res["amplified_syndrome_prob_explicit"] - 1.0) < 1e-12
    assert abs(res["conditional_survivor_state_fidelity"] - 1.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_amplitude_amplification_grover_reflection_witness_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
