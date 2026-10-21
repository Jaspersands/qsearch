"""Unit tests for the DCP Reed-Muller parity phase-gadget synthesis bridge (Subsystem 122)."""

from __future__ import annotations

from theorems.dcp_reed_muller_boolean_polynomial_degree_cnot_depth_bridge import (
    evaluate_parity_gadget_monomial_decomposition,
    generate_dcp_reed_muller_boolean_polynomial_degree_cnot_depth_certificate,
)


def test_parity_gadget_monomial_decomposition() -> None:
    res3 = evaluate_parity_gadget_monomial_decomposition(3)
    assert res3["exact_decomposition_verified"] is True
    assert res3["parity_gadget_count_2d_minus_1"] == 7


def test_certificate_generation() -> None:
    cert = generate_dcp_reed_muller_boolean_polynomial_degree_cnot_depth_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
