"""Unit tests for the DCP multiparameter QFIM Cramer-Rao and tight-frame bridge (Subsystem 135)."""

from __future__ import annotations

from theorems.dcp_quantum_fisher_information_matrix_multiparameter_cramer_rao_bridge import (
    evaluate_multiparameter_qfim_and_frame_optimality,
    generate_dcp_quantum_fisher_information_matrix_multiparameter_cramer_rao_certificate,
)


def test_multiparameter_qfim_tight_frame() -> None:
    cols = [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    res = evaluate_multiparameter_qfim_and_frame_optimality(cols, [0.85] * 4)
    assert res["exact_qcrb_laws_verified"] is True
    assert res["is_isotropic_tight_frame"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_fisher_information_matrix_multiparameter_cramer_rao_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
