"""Unit tests for the DCP cyclotomic Ring-LWE negacyclic CNOT shift-invariance bridge (Subsystem 97)."""

from __future__ import annotations

from theorems.dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_bridge import (
    evaluate_negacyclic_shift_orbit_witnesses,
    generate_dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_certificate,
)


def test_negacyclic_shift_orbit_invariance() -> None:
    res = evaluate_negacyclic_shift_orbit_witnesses(4, 8, [1, 2, 3, 0], [2, 1, 4, 3])
    assert res["all_shifts_preserve_mod2_kernel"] is True
    assert res["all_shifts_equivariant_under_pauli_x_wrap_frame"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
