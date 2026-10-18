"""Unit tests for the DCP adaptive Bayesian posterior phase-feedforward alignment bridge (Subsystem 86)."""

from __future__ import annotations

from theorems.dcp_adaptive_bayesian_posterior_phase_alignment_bridge import (
    evaluate_stage_r_phase_alignment,
    generate_dcp_adaptive_bayesian_posterior_phase_alignment_certificate,
)


def test_stage_r_phase_alignment_laws() -> None:
    res = evaluate_stage_r_phase_alignment(t_bits=3, stage_r=1, u_odd=1, gamma=0.8)
    assert res["exact_laws_verified"] is True
    assert res["min_fixed_x_tv"] < 1e-12
    assert abs(res["min_adaptive_feedforward_tv"] - 0.8) < 1e-12
    assert abs(res["min_random_xy_tv"] - 0.4) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_adaptive_bayesian_posterior_phase_alignment_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
