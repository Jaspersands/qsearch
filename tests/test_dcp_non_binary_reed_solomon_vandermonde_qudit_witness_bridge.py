"""Unit tests for the DCP Reed-Solomon Vandermonde qudit witness bridge (Subsystem 127)."""

from __future__ import annotations

from theorems.dcp_non_binary_reed_solomon_vandermonde_qudit_witness_bridge import (
    evaluate_reed_solomon_barycentric_witness,
    generate_dcp_non_binary_reed_solomon_vandermonde_qudit_witness_certificate,
)


def test_reed_solomon_barycentric_witness() -> None:
    res = evaluate_reed_solomon_barycentric_witness(5, 2, [0, 1, 2, 3])
    assert res["exact_barycentric_laws_verified"] is True
    assert res["degree_le_d_annihilated_count"] == 125


def test_certificate_generation() -> None:
    cert = generate_dcp_non_binary_reed_solomon_vandermonde_qudit_witness_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
