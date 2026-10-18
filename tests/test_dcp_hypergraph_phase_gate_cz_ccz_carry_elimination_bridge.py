"""Unit tests for the DCP hypergraph phase-gate (CZ / CCZ) carry elimination bridge (Subsystem 87)."""

from __future__ import annotations

from theorems.dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_bridge import (
    evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair,
    generate_dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_certificate,
)


def test_mod4_and_mod8_hypergraph_repair() -> None:
    res4 = evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair(t_bits=2, m_trees=3, col_dot_s=1)
    assert res4["exact_cutoff_and_repair_verified"] is True
    assert abs(res4["deg2_only_repaired_product_fidelity"] - 1.0) < 1e-12

    res8 = evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair(t_bits=3, m_trees=3, col_dot_s=1)
    assert res8["exact_cutoff_and_repair_verified"] is True
    assert abs(res8["deg2_only_repaired_product_fidelity"] - 9.0 / 16.0) < 1e-12
    assert abs(res8["full_hypergraph_repaired_product_fidelity"] - 1.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
