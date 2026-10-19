"""Unit tests for Subsystem 147: Quantum Wasserstein W_1 Distance & Cooling Bridge."""

from theorems.dcp_quantum_wasserstein_ornstein_uhlenbeck_cooling_dissipative_peeling_bridge import (
    generate_dcp_quantum_wasserstein_ornstein_uhlenbeck_cooling_dissipative_peeling_certificate,
)


def test_w1_cooling_certificate():
    cert = generate_dcp_quantum_wasserstein_ornstein_uhlenbeck_cooling_dissipative_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_w1_cooling_certificate()
    print("Subsystem 147 tests PASSED")
