"""Unit tests for the DCP grand synthesis 50-subsystem taxonomy and frontier bridge (Subsystem 116)."""

from __future__ import annotations

from theorems.dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge import (
    generate_dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_certificate,
)


def test_grand_synthesis_certificate() -> None:
    cert = generate_dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
    assert cert["six_core_laws_summary"]["law_6_newton_hensel_end_to_end_receiver"]["total_secrets_reconstructed_100pct"] == 128
