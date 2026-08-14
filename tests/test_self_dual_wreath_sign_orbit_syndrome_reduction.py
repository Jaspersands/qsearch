import pytest

from self_dual_wreath_sign_orbit_syndrome_reduction import (
    audit_retained_sign_orbit_sector,
    audit_sign_orbit_fourier_control,
    orientation_syndrome,
    run_sign_orbit_syndrome_reduction,
    self_conjugate_mass_scaling_record,
    sign_frequency,
    sign_orbits,
    transpose_partition,
)


def test_word_parity_map_has_eight_frequencies_and_eight_orientation_cosets():
    frequencies = {
        sign_frequency(bits)
        for bits in __import__("itertools").product((0, 1), repeat=3)
    }
    syndrome_fibers = {}
    for orientation in __import__("itertools").product((0, 1), repeat=6):
        syndrome_fibers.setdefault(orientation_syndrome(orientation), 0)
        syndrome_fibers[orientation_syndrome(orientation)] += 1
    assert len(frequencies) == 8
    assert len(syndrome_fibers) == 8
    assert set(syndrome_fibers.values()) == {8}


def test_partition_transpose_and_sign_orbit_split_are_exact():
    assert transpose_partition((4, 1)) == (2, 1, 1, 1)
    assert transpose_partition((3, 2)) == (2, 2, 1)
    pairs, fixed = sign_orbits(5, 1)
    assert pairs == (
        ((2, 2, 1), (3, 2)),
        ((2, 1, 1, 1), (4, 1)),
    )
    assert fixed == ((3, 1, 1),)


def test_fourier_controls_reduce_64_orientations_to_three_syndrome_bits():
    uniform = audit_sign_orbit_fourier_control(
        "S4-standard",
        4,
        ((3, 1),) * 6,
    )
    nonuniform = audit_sign_orbit_fourier_control(
        "S5-two-row",
        5,
        ((3, 2),) * 6,
    )
    assert uniform.exact_three_bit_syndrome_reduction_verified
    assert nonuniform.exact_three_bit_syndrome_reduction_verified
    assert uniform.conditional_orientation_kl_bits == pytest.approx(0.0, abs=1e-12)
    assert nonuniform.conditional_orientation_total_variation == pytest.approx(
        8.0 / 17.0
    )
    assert nonuniform.conditional_orientation_kl_bits > 0.9
    assert set(nonuniform.walsh_support).issubset(
        set(nonuniform.expected_walsh_support)
    )
    assert nonuniform.maximum_outside_support_coefficient < 1e-12


def test_retained_conditional_kl_splits_into_base_and_syndrome_terms():
    row = audit_retained_sign_orbit_sector(5, 1)
    assert row.retained_sign_pair_count == 2
    assert row.nonself_orbit_tuple_count == 64
    assert row.nonself_product_sector_mass == pytest.approx(
        row.retained_paired_plancherel_mass**6
    )
    assert row.exact_conditional_kl_decomposition_verified
    assert row.kl_chain_rule_residual < 1e-10
    assert row.conditional_kl_bits == pytest.approx(
        row.conditional_base_orbit_kl_bits + row.conditional_syndrome_kl_bits
    )
    assert 0.0 < row.conditional_syndrome_kl_bits <= 3.0


def test_self_conjugate_mass_is_recorded_without_an_asymptotic_claim():
    row = self_conjugate_mass_scaling_record(5)
    assert row.self_conjugate_partition_count == 1
    assert row.self_conjugate_plancherel_mass == pytest.approx(0.3)
    assert not row.asymptotic_vanishing_proved


def test_report_rejects_algorithmic_overclaim():
    report = run_sign_orbit_syndrome_reduction()
    assert report.headline_metrics["exact_sign_orbit_syndrome_theorem_count"] == 1
    assert report.headline_metrics["effective_syndrome_bit_count"] == 3
    assert report.headline_metrics["finite_non_one_dimensional_syndrome_signal_count"] == 1
    assert report.claim_gate["exact_three_bit_orientation_reduction_proved"]
    assert not report.claim_gate["canonical_high_dimension_syndrome_kl_vanishes_proved"]
    assert not report.claim_gate["canonical_high_dimension_syndrome_survives_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
