"""Unit tests for the DCP quadratic residue Legendre-Gauss sum phase oracle bridge (Subsystem 104)."""

from __future__ import annotations

from theorems.dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_bridge import (
    evaluate_prime_gauss_sum_and_legendre_kickback,
    generate_dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_certificate,
)


def test_prime_gauss_sum_and_legendre_kickback() -> None:
    res5 = evaluate_prime_gauss_sum_and_legendre_kickback(5)
    res7 = evaluate_prime_gauss_sum_and_legendre_kickback(7)
    assert res5["exact_laws_verified"] is True
    assert res7["exact_laws_verified"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
