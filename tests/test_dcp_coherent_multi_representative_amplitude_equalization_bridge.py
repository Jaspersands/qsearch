"""Unit tests for the DCP coherent M-representative fiber concentration bridge (Subsystem 85)."""

from __future__ import annotations

from theorems.dcp_coherent_multi_representative_amplitude_equalization_bridge import (
    evaluate_m_representative_fiber_concentration,
    generate_dcp_coherent_multi_representative_amplitude_equalization_certificate,
)


def test_multiplicity_4_staircase() -> None:
    for m_val in (1, 2, 3, 4, 5):
        res = evaluate_m_representative_fiber_concentration([[1, 1, 2, 2]], q_mod=4, m_cap=m_val)
        assert res["exact_match_verified"] is True
        assert abs(res["closed_form_m_rep_success"] - min(m_val, 4) / 4.0) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_coherent_multi_representative_amplitude_equalization_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
