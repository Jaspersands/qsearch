"""Unit tests for the DCP 2-adic Newton-Hensel matrix inversion bridge (Subsystem 91)."""

from __future__ import annotations

from theorems.dcp_modular_inversion_newton_hensel_lifting_quantum_bridge import (
    evaluate_newton_hensel_matrix_lifting_and_decoupling,
    generate_dcp_modular_inversion_newton_hensel_lifting_quantum_certificate,
)


def test_newton_hensel_lifting_3x3() -> None:
    u_3x3 = [[1, 2, 3], [0, 1, 5], [2, 4, 1]]
    res = evaluate_newton_hensel_matrix_lifting_and_decoupling(u_3x3, m_bits=8, test_secret_s=[137, 42, 219])
    assert res["all_verified"] is True
    assert res["num_newton_steps"] == 3
    assert abs(res["decoupled_state_fidelity"] - 1.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_modular_inversion_newton_hensel_lifting_quantum_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
