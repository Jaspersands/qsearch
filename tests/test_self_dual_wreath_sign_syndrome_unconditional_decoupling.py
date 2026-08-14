import math

import pytest

from self_dual_wreath_sign_syndrome_unconditional_decoupling import (
    audit_sign_syndrome_marginal,
    orientation_section_value,
    run_sign_syndrome_unconditional_decoupling,
    sign_syndrome_scaling_record,
)


def test_orientation_section_is_antisymmetric_and_zero_on_fixed_orbits():
    assert orientation_section_value((3, 2)) == -orientation_section_value((2, 2, 1))
    assert orientation_section_value((4, 1)) == -orientation_section_value((2, 1, 1, 1))
    assert orientation_section_value((3, 1, 1)) == 0


def test_exact_finite_syndrome_fourier_inversion_and_marginal_bounds():
    rows = [audit_sign_syndrome_marginal(n) for n in range(3, 6)]
    assert all(row.finite_fourier_inversion_verified for row in rows)
    assert all(row.marginal_bounds_verified for row in rows)
    assert all(len(row.face_walsh_coefficients) == 4 for row in rows)
    assert all(len(row.opposite_complement_walsh_coefficients) == 3 for row in rows)
    assert all(row.probability_sum_residual < 1e-9 for row in rows)


def test_S5_raw_syndrome_is_much_weaker_than_conditioned_pair_control():
    row = audit_sign_syndrome_marginal(5)
    assert row.syndrome_total_variation == pytest.approx(0.07079166666666664)
    assert row.syndrome_total_variation < 8.0 / 17.0
    assert row.syndrome_kl_bits < 0.2


def test_asymptotic_bound_uses_no_self_conjugate_mass_assumption():
    rows = [sign_syndrome_scaling_record(n) for n in (20, 30, 40, 50)]
    assert all(not row.self_conjugate_mass_assumption_used for row in rows)
    assert rows[-1].syndrome_chi_square_upper_bound < rows[0].syndrome_chi_square_upper_bound
    assert rows[-1].syndrome_total_variation_upper_bound < rows[0].syndrome_total_variation_upper_bound
    assert all(
        row.syndrome_kl_upper_bound_bits
        == pytest.approx(math.log2(1 + row.syndrome_chi_square_upper_bound))
        for row in rows
    )


def test_report_keeps_orbit_adaptive_and_coherent_channels_open():
    report = run_sign_syndrome_unconditional_decoupling()
    assert report.headline_metrics["unconditional_syndrome_decoupling_theorem_count"] == 1
    assert report.headline_metrics["self_conjugate_mass_assumption_count"] == 0
    assert report.claim_gate["unconditional_sign_syndrome_information_vanishes_proved"]
    assert not report.claim_gate["self_conjugate_mass_decay_needed_for_unconditional_result"]
    assert not report.claim_gate["orbit_adaptive_syndrome_information_vanishes_proved"]
    assert not report.claim_gate["base_sign_orbit_law_is_product_proved"]
    assert not report.claim_gate["coherent_multiplicity_signal_absent_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
