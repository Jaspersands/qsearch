"""Unit tests for the DCP symplectic Clifford stabilizer tableau witness compiler bridge (Subsystem 105)."""

from __future__ import annotations

from theorems.dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_bridge import (
    evaluate_symplectic_tableau_witness_compiler,
    generate_dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_certificate,
)


def test_symplectic_tableau_witness_compiler() -> None:
    a_disjoint = [[1, 3, 5, 7], [2, 4, 1, 3]]
    w_inv = [[1, 0, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 1, 0, 1]]
    res = evaluate_symplectic_tableau_witness_compiler(a_disjoint, 16, w_inv, m_witnesses=2)
    assert res["exact_tableau_laws_verified"] is True
    assert res["witness_supports_disjoint"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
