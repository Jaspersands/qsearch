"""Unit tests for Subsystem 149: Distributed Quantum Network Teleportation CNOT Peeling Bridge."""

from theorems.dcp_quantum_network_distributed_teleportation_bell_pair_cnot_peeling_bridge import (
    bbpssw_distill_fidelity,
    generate_dcp_quantum_network_distributed_teleportation_bell_pair_cnot_peeling_certificate,
)


def test_bbpssw_fixed_points():
    assert abs(bbpssw_distill_fidelity(0.5)["output_fidelity"] - 0.5) < 1e-12
    assert abs(bbpssw_distill_fidelity(1.0)["output_fidelity"] - 1.0) < 1e-12
    assert abs(bbpssw_distill_fidelity(0.25)["output_fidelity"] - 0.25) < 1e-12


def test_distributed_cnot_certificate():
    cert = generate_dcp_quantum_network_distributed_teleportation_bell_pair_cnot_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_bbpssw_fixed_points()
    test_distributed_cnot_certificate()
    print("Subsystem 149 tests PASSED")
