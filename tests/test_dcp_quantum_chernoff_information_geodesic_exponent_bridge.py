"""Unit tests for the DCP Quantum Chernoff Information geodesic exponent bridge (Subsystem 120)."""

from __future__ import annotations

import math
from theorems.dcp_quantum_chernoff_information_geodesic_exponent_bridge import (
    evaluate_quantum_vs_separable_chernoff_exponents,
    generate_dcp_quantum_chernoff_information_geodesic_exponent_certificate,
)


def test_quantum_vs_separable_chernoff() -> None:
    res = evaluate_quantum_vs_separable_chernoff_exponents([math.pi / 2.0, math.pi], gamma=0.85)
    assert res["all_verified"] is True
    assert res["records"][0]["quantum_chernoff_exponent_xi_QCB"] > res["records"][0]["separable_helstrom_exponent_xi_sep"]


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_chernoff_information_geodesic_exponent_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
