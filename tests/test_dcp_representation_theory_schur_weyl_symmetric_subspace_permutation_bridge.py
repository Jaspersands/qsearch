"""Unit tests for Subsystem 154: Schur-Weyl Symmetric Subspace Dicke Compression Bridge."""

from theorems.dcp_representation_theory_schur_weyl_symmetric_subspace_permutation_bridge import (
    generate_dcp_representation_theory_schur_weyl_symmetric_subspace_permutation_certificate,
)


def test_schur_weyl_certificate():
    cert = generate_dcp_representation_theory_schur_weyl_symmetric_subspace_permutation_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_schur_weyl_certificate()
    print("Subsystem 154 tests PASSED")
