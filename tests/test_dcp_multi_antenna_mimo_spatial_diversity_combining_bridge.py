"""Unit tests for the DCP multi-antenna MIMO spatial diversity LLR combining bridge (Subsystem 110)."""

from __future__ import annotations

from theorems.dcp_multi_antenna_mimo_spatial_diversity_combining_bridge import (
    evaluate_heterogeneous_branch_combining,
    generate_dcp_multi_antenna_mimo_spatial_diversity_combining_certificate,
)


def test_heterogeneous_branch_combining() -> None:
    res = evaluate_heterogeneous_branch_combining([0.90, 0.25, 0.25])
    assert res["exact_bayes_optimality_verified"] is True
    assert res["optimal_llr_bayes_error"] < res["unweighted_majority_error"]


def test_certificate_generation() -> None:
    cert = generate_dcp_multi_antenna_mimo_spatial_diversity_combining_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
