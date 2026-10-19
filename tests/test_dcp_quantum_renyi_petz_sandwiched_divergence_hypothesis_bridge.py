"""Unit tests for Subsystem 151: Petz vs Sandwiched Quantum Renyi Divergence Bridge."""

from theorems.dcp_quantum_renyi_petz_sandwiched_divergence_hypothesis_bridge import (
    generate_dcp_quantum_renyi_petz_sandwiched_divergence_hypothesis_certificate,
)


def test_renyi_certificate():
    cert = generate_dcp_quantum_renyi_petz_sandwiched_divergence_hypothesis_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_renyi_certificate()
    print("Subsystem 151 tests PASSED")
