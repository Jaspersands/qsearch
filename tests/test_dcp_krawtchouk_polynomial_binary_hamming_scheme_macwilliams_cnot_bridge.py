"""Unit tests for the DCP Krawtchouk polynomial binary Hamming scheme bridge (Subsystem 134)."""

from __future__ import annotations

from theorems.dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_bridge import (
    evaluate_krawtchouk_radial_hadamard_and_roots,
    generate_dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_certificate,
)


def test_krawtchouk_radial_hadamard_and_roots() -> None:
    res4 = evaluate_krawtchouk_radial_hadamard_and_roots(4)
    assert res4["exact_krawtchouk_laws_verified"] is True
    assert res4["k2_integer_root_weights"] == [1, 3]


def test_certificate_generation() -> None:
    cert = generate_dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
