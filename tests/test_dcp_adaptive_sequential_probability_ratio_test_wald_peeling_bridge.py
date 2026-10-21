"""Unit tests for the DCP adaptive Wald SPRT bit-peeling bridge (Subsystem 123)."""

from __future__ import annotations

from theorems.dcp_adaptive_sequential_probability_ratio_test_wald_peeling_bridge import (
    evaluate_wald_sprt_vs_fixed_batch_peeling,
    generate_dcp_adaptive_sequential_probability_ratio_test_wald_peeling_certificate,
)


def test_wald_sprt_vs_fixed_batch() -> None:
    res = evaluate_wald_sprt_vs_fixed_batch_peeling(0.75, [2, 3])
    assert res["all_verified"] is True
    assert res["records"][1]["sample_savings_ratio_fixed_over_sprt"] > 2.20


def test_certificate_generation() -> None:
    cert = generate_dcp_adaptive_sequential_probability_ratio_test_wald_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
