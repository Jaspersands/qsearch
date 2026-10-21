"""Unit tests for Subsystem 141: Quantum Ziv-Zakai Phase Estimation Lower Bound Bridge."""

import math
from theorems.dcp_quantum_ziv_zakai_bellman_minimax_phase_lower_bound_bridge import (
    qubit_dephased_fidelity,
    helstrom_min_error_bound,
    evaluate_quantum_ziv_zakai_vs_qcrb,
    generate_dcp_quantum_ziv_zakai_bellman_minimax_phase_lower_bound_certificate,
)


def test_qubit_dephased_fidelity_identities():
    assert abs(qubit_dephased_fidelity(0.0, 0.85) - 1.0) < 1e-12
    assert abs(qubit_dephased_fidelity(math.pi, 1.0) - 0.0) < 1e-12
    assert abs(qubit_dephased_fidelity(math.pi, 0.6) - (1.0 - 0.36)) < 1e-12
    assert abs(helstrom_min_error_bound(math.pi, 1, 1.0) - 0.0) < 1e-12


def test_quantum_ziv_zakai_certificate():
    cert = generate_dcp_quantum_ziv_zakai_bellman_minimax_phase_lower_bound_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_qubit_dephased_fidelity_identities()
    test_quantum_ziv_zakai_certificate()
    print("Subsystem 141 tests PASSED")
