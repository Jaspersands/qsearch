"""Unit tests for the DCP Walsh-Hadamard bent-function carry spectrum bridge (Subsystem 109)."""

from __future__ import annotations

from theorems.dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge import (
    evaluate_quadratic_carry_walsh_spectrum,
    generate_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_certificate,
)


def test_quadratic_carry_walsh_spectrum() -> None:
    even_res = evaluate_quadratic_carry_walsh_spectrum(4)
    odd_res = evaluate_quadratic_carry_walsh_spectrum(5)
    assert even_res["exact_bent_or_semibent_law_verified"] is True
    assert odd_res["exact_bent_or_semibent_law_verified"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
