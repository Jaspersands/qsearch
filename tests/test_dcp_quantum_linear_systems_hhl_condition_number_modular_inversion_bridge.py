"""Unit tests for Subsystem 143: HHL Condition Number vs Modular Z_q Inversion Bridge."""

import math
from theorems.dcp_quantum_linear_systems_hhl_condition_number_modular_inversion_bridge import (
    analyze_2x2_real_vs_modular_inversion,
    generate_dcp_quantum_linear_systems_hhl_condition_number_modular_inversion_certificate,
)


def test_hhl_vs_modular_inversion():
    res = analyze_2x2_real_vs_modular_inversion([[1, 1], [0, 1]], q=8)
    phi_sq = ((1.0 + math.sqrt(5.0)) / 2.0) ** 2
    assert abs(res["condition_number_kappa"] - phi_sq) < 1e-9
    assert res["modular_unitary_recovery_fraction"] == 1.0


def test_hhl_certificate():
    cert = generate_dcp_quantum_linear_systems_hhl_condition_number_modular_inversion_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_hhl_vs_modular_inversion()
    test_hhl_certificate()
    print("Subsystem 143 tests PASSED")
