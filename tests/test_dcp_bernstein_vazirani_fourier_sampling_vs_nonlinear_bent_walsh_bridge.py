"""Unit tests for Subsystem 156: Bernstein-Vazirani vs Nonlinear Carry Dilution Bridge."""

from theorems.dcp_bernstein_vazirani_fourier_sampling_vs_nonlinear_bent_walsh_bridge import (
    generate_dcp_bernstein_vazirani_fourier_sampling_vs_nonlinear_bent_walsh_certificate,
)


def test_bv_carry_dilution_certificate():
    cert = generate_dcp_bernstein_vazirani_fourier_sampling_vs_nonlinear_bent_walsh_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_bv_carry_dilution_certificate()
    print("Subsystem 156 tests PASSED")
