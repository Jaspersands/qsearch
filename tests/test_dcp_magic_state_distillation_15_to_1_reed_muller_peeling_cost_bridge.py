"""Unit tests for the DCP 15-to-1 magic state distillation factory cost bridge (Subsystem 128)."""

from __future__ import annotations

from theorems.dcp_magic_state_distillation_15_to_1_reed_muller_peeling_cost_bridge import (
    evaluate_magic_state_factory_footprint,
    generate_dcp_magic_state_distillation_15_to_1_reed_muller_peeling_cost_certificate,
)


def test_magic_state_factory_footprint() -> None:
    res = evaluate_magic_state_factory_footprint(32, 1e-3, 1e-4)
    assert res["exact_factory_laws_verified"] is True
    assert res["raw_magic_state_reduction_factor"] > 450.0


def test_certificate_generation() -> None:
    cert = generate_dcp_magic_state_distillation_15_to_1_reed_muller_peeling_cost_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
