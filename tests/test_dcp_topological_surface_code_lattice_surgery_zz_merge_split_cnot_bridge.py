"""Unit tests for Subsystem 155: Surface Code Lattice Surgery CNOT Bridge."""

from theorems.dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_bridge import (
    generate_dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_certificate,
)


def test_lattice_surgery_certificate():
    cert = generate_dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_lattice_surgery_certificate()
    print("Subsystem 155 tests PASSED")
