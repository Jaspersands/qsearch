import math

from coset_hidden_involution_plancherel_local_commutant_certificate import (
    C_orbit,
    D_orbit,
    audit_local_commutator,
    audit_plancherel_irreps,
    build_plancherel_local_commutant_report,
    fixed_defect_plancherel_mass_upper_bound,
    hidden_even_correction_coefficient,
    natural_local_commutator_scaling_record,
    normalized_commutator_squared_norm,
    unnormalized_commutator_histogram,
)


def test_local_orbit_sizes_are_polynomial():
    for half_degree in range(3, 10):
        assert len(C_orbit(half_degree)) == 8 * math.comb(half_degree, 2)
        assert len(D_orbit(half_degree)) == 24 * math.comb(half_degree, 3)


def test_three_pair_terms_cancel_and_four_pair_boundary_is_exact():
    assert not unnormalized_commutator_histogram(3)
    certificate = audit_local_commutator()
    assert certificate.four_pair_commutator_nonzero_coefficient_count == 768
    assert certificate.four_pair_positive_coefficient_count == 384
    assert certificate.four_pair_negative_coefficient_count == 384
    assert certificate.four_pair_unnormalized_squared_norm == 768
    assert certificate.every_nonzero_term_touches_all_four_pairs
    assert certificate.local_decomposition_proved


def test_all_rank_normalized_norm_formula_matches_direct_rows():
    for half_degree in (4, 5, 6):
        histogram = unnormalized_commutator_histogram(half_degree)
        direct = sum(value**2 for value in histogram.values()) / (
            len(C_orbit(half_degree)) ** 2 * len(D_orbit(half_degree)) ** 2
        )
        assert math.isclose(
            direct,
            normalized_commutator_squared_norm(half_degree),
            rel_tol=1e-14,
            abs_tol=1e-18,
        )


def test_finite_fourier_controls_detect_exactly_repeated_branches():
    for half_degree, expected_count in ((4, 7), (5, 22)):
        control = audit_plancherel_irreps(half_degree)
        assert control.repeated_branch_partition_count == expected_count
        assert control.nonzero_local_commutator_partition_count == expected_count
        assert control.every_repeated_partition_detected
        assert control.no_multiplicity_free_partition_detected
        assert control.expectation_residual < 1e-12


def test_natural_transfer_becomes_positive_outside_fixed_defect():
    assert all(
        hidden_even_correction_coefficient(half_degree) == 0
        for half_degree in range(4, 12)
    )
    assert natural_local_commutator_scaling_record(
        4
    ).natural_inverse_polynomial_mass_certified
    assert not natural_local_commutator_scaling_record(
        10
    ).growing_defect_natural_mass_certified
    record = natural_local_commutator_scaling_record(11)
    assert record.natural_inverse_polynomial_mass_certified
    assert record.growing_defect_natural_mass_certified
    assert record.growing_defect_source_good_mass_lower_bound > 0
    assert record.copy_space_variance_threshold > 0
    assert record.copy_space_spectral_diameter_lower_bound > 0
    assert record.commutator_rank_fraction_lower_bound > 0
    assert 2 * fixed_defect_plancherel_mass_upper_bound(22, 4) < (
        record.plancherel_good_mass_lower_bound
    )


def test_report_keeps_gap_transform_and_speedup_gates_closed():
    report = build_plancherel_local_commutant_report()
    assert report.theorem.exact_all_rank_commutator_norm_proved
    assert report.theorem.inverse_polynomial_natural_noncommutative_mass_proved
    assert report.theorem.growing_defect_natural_noncommutative_mass_proved
    assert report.theorem.inverse_polynomial_copy_space_variance_proved
    assert report.theorem.inverse_polynomial_copy_space_spectral_diameter_proved
    assert not report.theorem.all_repeated_branches_detected_by_this_pair_proved
    assert not report.theorem.inverse_polynomial_copy_space_eigenvalue_gap_proved
    assert not report.theorem.coherent_missing_label_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
