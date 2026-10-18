"""Unit tests for the DCP QSVT PGM Chebyshev equalization bridge (Subsystem 101)."""

from __future__ import annotations

from theorems.dcp_quantum_singular_value_transformation_pgm_chebyshev_bridge import (
    evaluate_qsvt_fiber_equalization,
    generate_dcp_quantum_singular_value_transformation_pgm_chebyshev_certificate,
)


def test_qsvt_fiber_equalization() -> None:
    res = evaluate_qsvt_fiber_equalization([[1, 1, 2]], q_mod=8)
    assert res["exact_hierarchy_verified"] is True
    assert res["deg1_linear"]["conditional_qft_success"] < res["deg3_qsvt"]["conditional_qft_success"] < res["deg5_qsvt"]["conditional_qft_success"]


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_singular_value_transformation_pgm_chebyshev_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
