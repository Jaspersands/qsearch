"""Unit tests for the DCP non-abelian wreath-product (S_2 wr S_M) pair-swap commutant bridge (Subsystem 90)."""

from __future__ import annotations

from theorems.dcp_non_abelian_wreath_product_pair_swap_commutant_bridge import (
    evaluate_wreath_product_sectors_and_singlet_vs_sym2m,
    generate_dcp_non_abelian_wreath_product_pair_swap_commutant_certificate,
)


def test_wreath_product_sectors_and_sym2m() -> None:
    res = evaluate_wreath_product_sectors_and_singlet_vs_sym2m(m_pairs=3, gamma=0.6)
    assert res["exact_laws_verified"] is True
    assert res["total_hilbert_dimension"] == 64
    assert res["tv_global_sym2m"] > res["tv_binomial_singlet"]


def test_certificate_generation() -> None:
    cert = generate_dcp_non_abelian_wreath_product_pair_swap_commutant_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
