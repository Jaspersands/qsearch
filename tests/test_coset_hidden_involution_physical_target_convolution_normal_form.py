from coset_hidden_involution_binary_decision_reduction import symmetric_group
from coset_hidden_involution_matching_charge_target_gauge_trivialization import (
    quotient_relative_coordinates,
)
from coset_hidden_involution_physical_target_convolution_normal_form import (
    audit_likelihood_expansion,
    audit_quotient_convolution_action,
    build_physical_target_convolution_report,
    direct_relative_convolution_action,
    quotient_left_convolution_action,
    shared_conjugation_scaling_record,
    write_physical_target_convolution_report,
)


def test_target_changing_left_convolution_has_shared_relative_right_action():
    group = symmetric_group(4)
    sources = (group[5], group[9], group[13])
    target = group[7]
    relative = quotient_relative_coordinates(sources, target)
    for offset, target_multiplier in enumerate(group[:8]):
        multipliers = tuple(group[offset + index + 1] for index in range(3))
        acted_sources, acted_target = quotient_left_convolution_action(
            sources,
            target,
            multipliers,
            target_multiplier,
        )
        observed = quotient_relative_coordinates(acted_sources, acted_target)
        expected = direct_relative_convolution_action(
            relative,
            multipliers,
            target_multiplier,
        )
        assert observed == expected


def test_finite_quotient_action_controls_have_no_formula_failures():
    for degree, copies in ((3, 2), (4, 2), (4, 3)):
        row = audit_quotient_convolution_action(degree, copies)
        assert row.quotient_action_formula_failure_count == 0
        assert row.exact_quotient_action_verified


def test_likelihood_expansion_has_conditioned_L1_one_and_full_L1_M():
    for degree, transpositions, copies in ((3, 1, 2), (3, 1, 3), (4, 2, 2)):
        row = audit_likelihood_expansion(degree, transpositions, copies)
        assert row.every_conditioned_Q_has_L1_one
        assert row.Z_equals_M_times_uniform_Q_average
        assert int(row.positive_group_basis_L1_norm) == row.conjugacy_class_size
        assert row.inside_K_conditioned_distinct_term_count_minimum == 2**copies
        assert row.outside_K_conditioned_distinct_term_count_minimum == 4**copies
        assert row.exact_expansion_verified


def test_scaling_keeps_local_channel_normalized_and_global_factor_M():
    for half_degree, copies in ((4, 20), (8, 40), (16, 80), (32, 160)):
        row = shared_conjugation_scaling_record(half_degree, copies)
        assert row.conditioned_Q_L1_norm == 1.0
        assert row.generic_normalization_is_candidate_count
        assert row.full_Z_positive_L1_norm_decimal == (
            row.generic_uniform_group_block_encoding_normalization_decimal
        )


def test_report_is_architecture_reduction_not_fast_forward_claim():
    report = build_physical_target_convolution_report()
    theorem = report.theorem
    assert theorem.exact_all_finite_groups_quotient_action_proved
    assert theorem.exact_shared_conjugation_likelihood_expansion_proved
    assert theorem.conditioned_Q_normalization_one_proved
    assert theorem.full_Z_positive_L1_equals_candidate_count_proved
    assert not theorem.generic_PREP_SELECT_fast_forward_compiled
    assert not theorem.structured_shared_orbit_fast_forward_compiled
    assert not theorem.matched_classical_separation_proved
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_live_physical_target_normal_form_is_json_serializable(tmp_path):
    output = tmp_path / "physical-target-normal-form.json"
    payload = write_physical_target_convolution_report(output)
    assert output.exists()
    assert payload["status"] == (
        "physical-shared-conjugation-normal-form-proved-fast-forward-open"
    )
    assert payload["claim_gate"][
        "likelihood_is_shared_conjugation_average_proved"
    ]
    assert not payload["claim_gate"][
        "structured_shared_orbit_fast_forward_compiled"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
