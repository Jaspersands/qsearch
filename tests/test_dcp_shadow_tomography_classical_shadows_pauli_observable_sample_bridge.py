"""Unit tests for the DCP Classical Shadows vs. commuting X^K derandomization bridge (Subsystem 140)."""

from __future__ import annotations

from theorems.dcp_shadow_tomography_classical_shadows_pauli_observable_sample_bridge import (
    evaluate_classical_shadows_vs_commuting_x_derandomization,
    generate_dcp_shadow_tomography_classical_shadows_pauli_observable_sample_certificate,
)


def test_classical_shadows_vs_derandomization() -> None:
    res = evaluate_classical_shadows_vs_commuting_x_derandomization([3, 4], 0.25)
    assert res["all_verified"] is True
    assert res["records"][1]["sample_reduction_ratio_shadow_over_derand"] > 86.0


def test_certificate_generation() -> None:
    cert = generate_dcp_shadow_tomography_classical_shadows_pauli_observable_sample_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
