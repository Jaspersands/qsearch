"""Unit tests for the DCP Roetteler bent-function hidden-shift carry-cancellation bridge (Subsystem 136)."""

from __future__ import annotations

from theorems.dcp_hidden_shift_bent_function_roetteler_involutory_dual_bridge import (
    evaluate_roetteler_bent_carry_hidden_shift,
    generate_dcp_hidden_shift_bent_function_roetteler_involutory_dual_certificate,
)


def test_roetteler_bent_carry_hidden_shift() -> None:
    res = evaluate_roetteler_bent_carry_hidden_shift(2, "maiorana_mcfarland")
    assert res["exact_roetteler_laws_verified"] is True
    assert abs(res["min_2query_roetteler_success_prob_across_all_shifts"] - 1.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_hidden_shift_bent_function_roetteler_involutory_dual_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
