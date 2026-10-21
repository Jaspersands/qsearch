"""Unit tests for Subsystem 144: Dynamical Decoupling CPMG vs UDD Filter Function Bridge."""

from theorems.dcp_floquet_dynamical_decoupling_carr_purcell_udds_carry_filter_bridge import (
    pulse_times_cpmg,
    pulse_times_udd,
    generate_dcp_floquet_dynamical_decoupling_carr_purcell_udds_carry_filter_certificate,
)


def test_pulse_time_identities():
    assert abs(pulse_times_udd(1)[0] - 0.5) < 1e-12
    assert abs(pulse_times_udd(2)[0] - 0.25) < 1e-12
    assert abs(pulse_times_udd(2)[1] - 0.75) < 1e-12
    assert abs(pulse_times_cpmg(2)[0] - 0.25) < 1e-12


def test_dd_filter_certificate():
    cert = generate_dcp_floquet_dynamical_decoupling_carr_purcell_udds_carry_filter_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_pulse_time_identities()
    test_dd_filter_certificate()
    print("Subsystem 144 tests PASSED")
