"""Unit tests for the DCP logarithmic binary tree vs. linear chain CNOT depth bridge (Subsystem 130)."""

from __future__ import annotations

from theorems.dcp_clifford_cnot_depth_logarithmic_tree_vs_linear_chain_bridge import (
    evaluate_log_tree_vs_linear_chain_cnot_compression,
    generate_dcp_clifford_cnot_depth_logarithmic_tree_vs_linear_chain_certificate,
)


def test_log_tree_vs_linear_chain() -> None:
    res = evaluate_log_tree_vs_linear_chain_cnot_compression([4, 16])
    assert res["all_verified"] is True
    assert res["records"][1]["visibility_gain_tree_over_chain"] > 5.80


def test_certificate_generation() -> None:
    cert = generate_dcp_clifford_cnot_depth_logarithmic_tree_vs_linear_chain_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
