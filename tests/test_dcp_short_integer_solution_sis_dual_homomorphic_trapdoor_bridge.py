"""Unit tests for the DCP SIS dual gadget trapdoor binary witness compilation bridge (Subsystem 115)."""

from __future__ import annotations

from theorems.dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge import (
    evaluate_sis_gadget_trapdoor_witness_compilation,
    generate_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_certificate,
)


def test_sis_gadget_trapdoor_witness_compilation() -> None:
    r_trap = [[1, 0], [1, 0], [1, 0], [0, 1], [0, 1], [0, 1]]
    res = evaluate_sis_gadget_trapdoor_witness_compilation(2, 3, r_trap)
    assert res["all_verified"] is True


def test_certificate_generation() -> None:
    cert = generate_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16
