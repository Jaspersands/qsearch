"""Unit tests for the DCP Fano-Holevo mutual information sample lower bound bridge (Subsystem 126)."""

from __future__ import annotations

from theorems.dcp_quantum_fano_holevo_mutual_information_sample_lower_bound_bridge import (
    evaluate_fano_holevo_sample_lower_bound,
    generate_dcp_quantum_fano_holevo_mutual_information_sample_lower_bound_certificate,
)


def test_fano_holevo_lower_bound() -> None:
    res = evaluate_fano_holevo_sample_lower_bound(8, 16, 0.01, [0.50, 1.00])
    assert res["all_verified"] is True
    assert res["records"][1]["min_quantum_copies_integer_ceil"] == 32


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_fano_holevo_mutual_information_sample_lower_bound_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
