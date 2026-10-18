"""Unit tests for the DCP multi-secret block-matrix simultaneous peeling bridge (Subsystem 94)."""

from __future__ import annotations

from theorems.dcp_multi_secret_block_matrix_simultaneous_peeling_bridge import (
    evaluate_cross_packet_cnot_secret_difference_and_sum,
    generate_dcp_multi_secret_block_matrix_simultaneous_peeling_certificate,
)


def test_cross_packet_cnot_sum_and_diff() -> None:
    res = evaluate_cross_packet_cnot_secret_difference_and_sum(q_mod=8, a_label=2, s1=5, s2=5, gamma=0.85)
    assert res["exact_sum_and_diff_law_verified"] is True
    assert abs(res["x_expectation_b1_diff"] - (0.85 ** 2)) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_multi_secret_block_matrix_simultaneous_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
