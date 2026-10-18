"""Unit tests for the DCP cyclotomic Galois automorphism prime-power peeling bridge (Subsystem 102)."""

from __future__ import annotations

from theorems.dcp_galois_frobenius_automorphism_prime_power_peeling_bridge import (
    evaluate_galois_group_witness_equivariance_and_conjugation_peeling,
    generate_dcp_galois_frobenius_automorphism_prime_power_peeling_certificate,
)


def test_galois_group_and_conjugation_peeling() -> None:
    res = evaluate_galois_group_witness_equivariance_and_conjugation_peeling(4, 16, [5, 3, 11, 7])
    assert res["all_verified"] is True
    assert res["midpoint_degree_n_over_2_annihilated"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_galois_frobenius_automorphism_prime_power_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
