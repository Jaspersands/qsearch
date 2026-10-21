"""Unit tests for the DCP finite-Z_q GKP modular grid stabilizer bridge (Subsystem 139)."""

from __future__ import annotations

from theorems.dcp_continuous_variable_gkp_modular_grid_stabilizer_peeling_bridge import (
    evaluate_finite_gkp_dual_comb_and_error_correction,
    generate_dcp_continuous_variable_gkp_modular_grid_stabilizer_peeling_certificate,
)


def test_finite_gkp_dual_comb() -> None:
    res = evaluate_finite_gkp_dual_comb_and_error_correction(4, 5)
    assert res["exact_gkp_laws_verified"] is True
    assert res["successful_error_correction_trials"] == 20


def test_certificate_generation() -> None:
    cert = generate_dcp_continuous_variable_gkp_modular_grid_stabilizer_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
