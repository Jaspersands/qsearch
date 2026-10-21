"""Unit tests for the DCP Slepian DPSS vs. Dirichlet-sine window bridge (Subsystem 125)."""

from __future__ import annotations

from theorems.dcp_quantum_slepian_prolate_spheroidal_discrete_window_bridge import (
    evaluate_dpss_slepian_vs_sine_window_pareto_duality,
    generate_dcp_quantum_slepian_prolate_spheroidal_discrete_window_certificate,
)


def test_dpss_slepian_vs_sine_window() -> None:
    res = evaluate_dpss_slepian_vs_sine_window_pareto_duality(16, half_band_b=1)
    assert res["exact_pareto_duality_verified"] is True
    assert res["leakage_dpss_optimal"] < res["leakage_sine"]


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_slepian_prolate_spheroidal_discrete_window_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
