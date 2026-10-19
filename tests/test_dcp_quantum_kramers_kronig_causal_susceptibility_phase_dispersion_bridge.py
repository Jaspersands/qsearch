"""Unit tests for Subsystem 153: Kramers-Kronig Causal Susceptibility & Dispersive Phase Bridge."""

from theorems.dcp_quantum_kramers_kronig_causal_susceptibility_phase_dispersion_bridge import (
    generate_dcp_quantum_kramers_kronig_causal_susceptibility_phase_dispersion_certificate,
)


def test_kramers_kronig_certificate():
    cert = generate_dcp_quantum_kramers_kronig_causal_susceptibility_phase_dispersion_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_kramers_kronig_certificate()
    print("Subsystem 153 tests PASSED")
