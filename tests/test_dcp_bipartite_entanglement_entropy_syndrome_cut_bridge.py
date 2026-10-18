"""Unit tests for the DCP bipartite entanglement entropy across the survivor-syndrome cut bridge (Subsystem 99)."""

from __future__ import annotations

from theorems.dcp_bipartite_entanglement_entropy_syndrome_cut_bridge import (
    evaluate_bipartite_survivor_syndrome_entanglement,
    generate_dcp_bipartite_entanglement_entropy_syndrome_cut_certificate,
)


def test_survivor_syndrome_purity() -> None:
    sep = evaluate_bipartite_survivor_syndrome_entanglement(8, [3, 4, 0])
    assert sep["exact_purity_law_verified"] is True
    assert abs(sep["purity_closed_form"] - 1.0) < 1e-12

    bell = evaluate_bipartite_survivor_syndrome_entanglement(8, [1, 2, 3])
    assert bell["exact_purity_law_verified"] is True
    assert abs(bell["purity_closed_form"] - 0.5) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_bipartite_entanglement_entropy_syndrome_cut_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
