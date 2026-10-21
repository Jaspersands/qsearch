"""Unit tests for Subsystem 145: Quantum Stein's Lemma & Umegaki Relative Entropy Bridge."""

from theorems.dcp_quantum_sanov_theorem_large_deviations_kl_syndrome_hypothesis_bridge import (
    umegaki_relative_entropy_qubit,
    quantum_pinsker_lower_bound,
    generate_dcp_quantum_sanov_theorem_large_deviations_kl_syndrome_hypothesis_certificate,
)


def test_umegaki_and_pinsker():
    assert abs(umegaki_relative_entropy_qubit(0.6, 0.6, 0.0)) < 1e-15
    d_val = umegaki_relative_entropy_qubit(0.9, 0.2, 0.0)
    p_lb = quantum_pinsker_lower_bound(0.9, 0.2, 0.0)
    assert d_val > p_lb > 0.0


def test_stein_certificate():
    cert = generate_dcp_quantum_sanov_theorem_large_deviations_kl_syndrome_hypothesis_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_umegaki_and_pinsker()
    test_stein_certificate()
    print("Subsystem 145 tests PASSED")
