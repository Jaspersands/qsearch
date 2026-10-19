"""Unit tests for Subsystem 148: Galois Ring GR(4, m) Teichmuller Carry Bridge."""

from theorems.dcp_galois_ring_gr_4_m_nechaev_kloosterman_hensel_carry_bridge import (
    verify_gr4_2_teichmuller_carry_identity,
    generate_dcp_galois_ring_gr_4_m_nechaev_kloosterman_hensel_carry_certificate,
)


def test_gr4_2_teichmuller_carry():
    res = verify_gr4_2_teichmuller_carry_identity()
    assert res["unique_2adic_bijection_all_16_elements"] is True
    assert res["frobenius_carry_c1_sq_equals_ab_exact"] is True


def test_gr4_2_certificate():
    cert = generate_dcp_galois_ring_gr_4_m_nechaev_kloosterman_hensel_carry_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_gr4_2_teichmuller_carry()
    test_gr4_2_certificate()
    print("Subsystem 148 tests PASSED")
