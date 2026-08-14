import pytest

from self_dual_wreath_sign_orbit_kl_chain_reduction import (
    audit_sign_orbit_kl_chain,
    partition_sign_orbits,
    run_sign_orbit_kl_chain_reduction,
)


def test_partition_sign_orbits_include_pairs_and_fixed_points():
    orbits = partition_sign_orbits(
        ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1))
    )
    assert len(orbits) == 4
    assert sum(len(orbit) == 2 for orbit in orbits) == 3
    assert ((3, 1, 1),) in orbits


def test_exact_kl_chain_holds_through_S5():
    rows = [audit_sign_orbit_kl_chain(n) for n in range(2, 6)]
    assert all(row.exact_lossless_orientation_reduction_verified for row in rows)
    assert all(row.augmented_probability_sum_residual < 1e-8 for row in rows)
    assert all(row.augmented_product_sum_residual < 1e-8 for row in rows)
    assert all(row.kl_chain_rule_residual < 1e-8 for row in rows)
    assert all(
        row.conditional_syndrome_information_identity_residual < 1e-8
        for row in rows
    )


def test_orientation_channel_never_exceeds_three_bits():
    rows = [audit_sign_orbit_kl_chain(n) for n in range(2, 6)]
    assert all(row.expected_conditional_syndrome_kl_bits <= 3 + 1e-9 for row in rows)
    assert all(row.maximum_orbit_conditional_syndrome_kl_bits <= 3 + 1e-9 for row in rows)


def test_S5_finite_synergy_has_both_base_and_adaptive_components():
    row = audit_sign_orbit_kl_chain(5)
    assert row.base_sign_orbit_kl_bits > 0
    assert row.expected_conditional_syndrome_kl_bits > 0
    assert row.orbit_syndrome_mutual_information_bits > 0
    assert row.full_six_label_kl_bits == pytest.approx(
        row.base_sign_orbit_kl_bits + row.expected_conditional_syndrome_kl_bits
    )
    assert row.expected_conditional_syndrome_kl_bits == pytest.approx(
        row.unconditional_syndrome_kl_bits
        + row.orbit_syndrome_mutual_information_bits
    )


def test_report_keeps_both_asymptotic_terms_and_classical_gate_open():
    report = run_sign_orbit_kl_chain_reduction()
    assert report.headline_metrics["lossless_sign_orbit_kl_chain_theorem_count"] == 1
    assert report.headline_metrics["discarded_ancillary_orientation_bit_count"] == 3
    assert report.claim_gate["orientation_information_reduces_losslessly_to_three_bits"]
    assert report.claim_gate["full_six_label_kl_chain_decomposition_proved"]
    assert not report.claim_gate["base_sign_orbit_kl_vanishes_proved"]
    assert not report.claim_gate["orbit_syndrome_mutual_information_vanishes_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
