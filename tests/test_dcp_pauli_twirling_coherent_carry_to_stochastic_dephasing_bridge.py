"""Unit tests for the DCP Pauli twirling coherent-to-stochastic carry error bridge (Subsystem 121)."""

from __future__ import annotations

from theorems.dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_bridge import (
    evaluate_coherent_vs_pauli_twirled_carry_error,
    generate_dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_certificate,
)


def test_coherent_vs_twirled_carry_error() -> None:
    res = evaluate_coherent_vs_pauli_twirled_carry_error([0.10])
    assert res["all_verified"] is True
    assert res["records"][0]["error_suppression_ratio_coh_over_twirl"] > 20.0


def test_certificate_generation() -> None:
    cert = generate_dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
