"""Unit tests for the DCP composite CRT coprime modulus factorization bridge (Subsystem 108)."""

from __future__ import annotations

from theorems.dcp_composite_crt_coprime_modulus_tensor_factorization_bridge import (
    evaluate_crt_composite_modulus_factor_annihilation,
    generate_dcp_composite_crt_coprime_modulus_tensor_factorization_certificate,
)


def test_crt_composite_factor_annihilation() -> None:
    res = evaluate_crt_composite_modulus_factor_annihilation(t_bits=3, p_prime=3)
    assert res["exact_crt_laws_verified"] is True
    assert res["q_composite"] == 24


def test_certificate_generation() -> None:
    cert = generate_dcp_composite_crt_coprime_modulus_tensor_factorization_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
