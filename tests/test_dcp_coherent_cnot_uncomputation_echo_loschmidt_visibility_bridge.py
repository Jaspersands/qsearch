"""Unit tests for the DCP coherent CNOT uncomputation echo visibility bridge (Subsystem 106)."""

from __future__ import annotations

import math
from theorems.dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_bridge import (
    evaluate_cnot_uncomputation_echo_vs_syndrome_readout,
    generate_dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_certificate,
)


def test_cnot_uncomputation_echo() -> None:
    res = evaluate_cnot_uncomputation_echo_vs_syndrome_readout([0.0, math.pi / 2.0], gamma=0.9)
    assert res["all_verified"] is True
    assert abs(res["records"][1]["x0_expectation_uncomputed_explicit"]) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
