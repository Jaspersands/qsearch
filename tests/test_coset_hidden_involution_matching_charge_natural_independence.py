from coset_hidden_involution_matching_charge_natural_independence import (
    audit_all_rank_defect_four_exclusion,
    audit_triangle_commutator_locality,
    build_matching_charge_natural_independence_report,
    exact_norm_from_local_decomposition,
    natural_independence_scaling_record,
    normalized_independence_commutator_squared_norm,
)


def test_matching_triangle_commutator_has_exact_five_pair_decomposition():
    control = audit_triangle_commutator_locality()
    assert control.four_pair_commutator_nonzero_count == 0
    assert control.five_pair_commutator_nonzero_count == 122880
    assert control.five_pair_positive_coefficient_count == 61440
    assert control.five_pair_negative_coefficient_count == 61440
    assert control.five_pair_coefficient_absolute_value == 12
    assert control.five_pair_unnormalized_squared_norm == 17694720
    assert control.every_term_touches_all_five_pair_labels
    assert control.six_pair_equals_sum_of_five_pair_embeddings
    assert control.exact_all_rank_five_pair_decomposition_proved


def test_triangle_charge_commutes_with_C_and_is_K_adapted():
    control = audit_triangle_commutator_locality()
    assert control.C_triangle_commutator_nonzero_count == 0
    assert control.triangle_K_commutator_failure_count == 0


def test_closed_commutator_norm_matches_local_counting():
    for half_degree in (5, 6, 7, 11, 32):
        assert abs(
            normalized_independence_commutator_squared_norm(half_degree)
            - exact_norm_from_local_decomposition(half_degree)
        ) < 1e-25


def test_hidden_source_parity_transfer_starts_at_eleven():
    for half_degree in (11, 12, 13, 32):
        record = natural_independence_scaling_record(half_degree)
        assert record.hidden_even_correction_coefficient == 0
        assert (
            record.hidden_even_source_expectation
            == record.normalized_commutator_squared_norm
        )
        assert record.hidden_source_good_mass_lower_bound > 0
        assert record.distance_from_C_K_center_algebra_squared_threshold > 0
        assert record.hidden_source_independence_certified


def test_defect_four_exclusion_is_uniform_from_thirteen():
    proof = audit_all_rank_defect_four_exclusion()
    assert proof["base_m13_delta_over_8_minus_fixed_defect_bound"] > 0
    assert proof["successive_fixed_over_delta_ratio_strictly_decreases"]
    assert all(
        coefficient > 0
        for coefficient in proof[
            "shifted_ratio_denominator_minus_numerator_coefficients"
        ]
    )
    assert proof["proved"]
    assert not natural_independence_scaling_record(
        12
    ).beyond_defect_four_independence_certified
    assert natural_independence_scaling_record(
        13
    ).beyond_defect_four_independence_certified


def test_report_keeps_hierarchy_likelihood_and_speedup_gates_closed():
    report = build_matching_charge_natural_independence_report()
    assert report.theorem.exact_all_rank_local_norm_proved
    assert (
        report.theorem.D_outside_C_K_center_algebra_on_inverse_polynomial_hidden_source_mass_proved
    )
    assert report.theorem.beyond_defect_four_hidden_source_mass_proved
    assert not report.theorem.complete_commuting_charge_hierarchy_constructed
    assert not report.theorem.conditional_joint_gap_theorem_proved
    assert not report.theorem.source_CS_likelihood_correlation_proved
    assert not report.theorem.coherent_subduction_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
