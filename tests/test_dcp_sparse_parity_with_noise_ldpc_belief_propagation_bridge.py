"""Unit tests for the DCP sparse parity-with-noise LDPC belief propagation bridge (Subsystem 92)."""

from __future__ import annotations

from theorems.dcp_sparse_parity_with_noise_ldpc_belief_propagation_bridge import (
    evaluate_ldpc_star_check_belief_propagation,
    generate_dcp_sparse_parity_with_noise_ldpc_belief_propagation_certificate,
)


def test_ldpc_star_check_bp_exactness() -> None:
    res0 = evaluate_ldpc_star_check_belief_propagation(0.5, 0.7, 0.7, l_checks=0)
    res3 = evaluate_ldpc_star_check_belief_propagation(0.5, 0.7, 0.7, l_checks=3)
    assert res0["exact_bp_bayes_equivalence_verified"] is True
    assert res3["exact_bp_bayes_equivalence_verified"] is True
    assert res3["bp_map_error_prob"] < res0["bp_map_error_prob"]


def test_certificate_generation() -> None:
    cert = generate_dcp_sparse_parity_with_noise_ldpc_belief_propagation_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
