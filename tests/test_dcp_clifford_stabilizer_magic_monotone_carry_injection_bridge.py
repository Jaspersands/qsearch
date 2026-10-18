"""Unit tests for the DCP Clifford stabilizer Renyi-2 magic carry injection bridge (Subsystem 95)."""

from __future__ import annotations

from theorems.dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge import (
    evaluate_carry_magic_across_levels,
    generate_dcp_clifford_stabilizer_magic_monotone_carry_injection_certificate,
)


def test_carry_magic_levels() -> None:
    res = evaluate_carry_magic_across_levels(m_qubits=3)
    assert res["exact_magic_laws_verified"] is True
    assert res["level_t1_mod2"]["stabilizer_renyi_2_magic_bits"] == 0.0
    assert res["level_t2_mod4_cz_graph"]["stabilizer_renyi_2_magic_bits"] == 0.0
    assert res["level_t3_mod8_xor"]["stabilizer_renyi_2_magic_bits"] > 0.415


def test_certificate_generation() -> None:
    cert = generate_dcp_clifford_stabilizer_magic_monotone_carry_injection_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
