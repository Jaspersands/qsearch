"""Unit tests for Subsystem 146: Majorana Fermionic Gaussian Matchgate Parity Peeling Bridge."""

from theorems.dcp_majorana_fermionic_gaussian_matchgate_parity_peeling_bridge import (
    generate_dcp_majorana_fermionic_gaussian_matchgate_parity_peeling_certificate,
)


def test_matchgate_certificate():
    cert = generate_dcp_majorana_fermionic_gaussian_matchgate_parity_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_matchgate_certificate()
    print("Subsystem 146 tests PASSED")
