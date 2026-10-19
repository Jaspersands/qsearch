"""Unit tests for the DCP prime-field Cayley-Hamilton / Hankel recurrence peeling bridge (Subsystem 131)."""

from __future__ import annotations

from theorems.dcp_prime_field_f_p_berlekamp_massey_linear_recurrence_peeling_bridge import (
    evaluate_cayley_hamilton_hankel_recurrence_extrapolation,
    generate_dcp_prime_field_f_p_berlekamp_massey_linear_recurrence_peeling_certificate,
)


def test_cayley_hamilton_hankel_extrapolation() -> None:
    m_3d = [[2, 1, 0], [0, 3, 1], [5, 4, 6]]
    res = evaluate_cayley_hamilton_hankel_recurrence_extrapolation(17, m_3d, [1, 0, 0], [4, 11, 7], 20)
    assert res["exact_extrapolation_verified"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_prime_field_f_p_berlekamp_massey_linear_recurrence_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
