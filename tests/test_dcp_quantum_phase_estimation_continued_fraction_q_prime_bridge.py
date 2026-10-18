"""Unit tests for the DCP odd-prime QFT 2-bin capture and rounding bridge (Subsystem 93)."""

from __future__ import annotations

from theorems.dcp_quantum_phase_estimation_continued_fraction_q_prime_bridge import (
    evaluate_odd_prime_qft_rounding_recovery,
    generate_dcp_quantum_phase_estimation_continued_fraction_q_prime_certificate,
)


def test_odd_prime_qft_rounding() -> None:
    res = evaluate_odd_prime_qft_rounding_recovery(q_prime=17, m_bits=6)
    assert res["exact_laws_verified"] is True
    assert res["both_nearest_bins_round_correctly_for_all_z"] is True
    assert res["min_2bin_capture_prob"] > 0.810569


def test_certificate_generation() -> None:
    cert = generate_dcp_quantum_phase_estimation_continued_fraction_q_prime_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
