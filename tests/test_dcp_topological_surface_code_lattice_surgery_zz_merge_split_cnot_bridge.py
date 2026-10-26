"""Unit tests for Subsystem 155: Surface Code Lattice Surgery CNOT Bridge."""

import numpy as np
from theorems.dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_bridge import (
    generate_dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_certificate,
    verify_lattice_surgery_pauli_byproduct_truth_table,
)


def test_lattice_surgery_three_bit_kraus_and_byproduct():
    byproduct = verify_lattice_surgery_pauli_byproduct_truth_table()
    assert byproduct["outcomes_checked"] == 8
    assert byproduct["byproduct_law"] == "Z_C^{m_XX} X_T^{m_ZZ xor m_Z}"
    assert byproduct["byproduct_sign_cancellation_exact"] is True
    assert byproduct["kraus_completeness_residual"] < 1e-12
    # Naive two-bit correction Z_C^{m_ZZ} X_T^{m_XX} fails on 6 of 8 branches
    assert byproduct["naive_two_bit_formula_failing_branches"] == 6
    for row in byproduct["branches"]:
        assert abs(row["branch_probability"] - 0.125) < 1e-12
        assert row["kraus_operator_residual"] < 1e-12
        assert row["entangled_choi_residual"] < 1e-12


def test_lattice_surgery_certificate():
    cert = generate_dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())
    assert cert["falsification_status"]["accepted_speedup_candidate"] is False
    assert cert["falsification_status"]["novelty_claim"] is False


if __name__ == "__main__":
    test_lattice_surgery_three_bit_kraus_and_byproduct()
    test_lattice_surgery_certificate()
    print("Subsystem 155 tests PASSED")
