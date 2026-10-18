"""Unit tests for the DCP end-to-end hybrid CNOT + Pauli-X + Hensel + R_Z feedforward receiver bridge (Subsystem 100)."""

from __future__ import annotations

from theorems.dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_bridge import (
    run_end_to_end_hybrid_receiver_exhaustively,
    generate_dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_certificate,
)


def test_end_to_end_hybrid_receiver() -> None:
    res = run_end_to_end_hybrid_receiver_exhaustively([[1, 3], [2, 5]], t_bits=4, gamma=0.85)
    assert res["exact_end_to_end_verified"] is True
    assert res["reconstruction_accuracy"] == 1.0


def test_certificate_generation() -> None:
    cert = generate_dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
