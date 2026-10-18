"""Unit tests for the DCP Haar-random vs. dihedral 2-design second frame potential bridge (Subsystem 112)."""

from __future__ import annotations

from theorems.dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge import (
    evaluate_dihedral_second_frame_potential_and_additive_energy,
    generate_dcp_haar_random_vs_dihedral_2_design_frame_potential_certificate,
)


def test_dihedral_second_frame_potential() -> None:
    res = evaluate_dihedral_second_frame_potential_and_additive_energy([[1, 2, 4]], q_mod=8)
    assert res["exact_identity_verified"] is True
    assert res["additive_energy_E4"] == 512


def test_certificate_generation() -> None:
    cert = generate_dcp_haar_random_vs_dihedral_2_design_frame_potential_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
