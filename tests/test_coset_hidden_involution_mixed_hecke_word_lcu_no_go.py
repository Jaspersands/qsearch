from coset_hidden_involution_mixed_hecke_word_lcu_no_go import (
    audit_mixed_word_fiber,
    build_mixed_word_LCU_report,
    mixed_word_LCU_bound_control,
    mixed_word_scaling_record,
    write_mixed_word_LCU_report,
)


def test_mixed_word_fiber_bound_uses_any_nontrivial_transition():
    for half_degree in (3, 4, 5, 8):
        for word_degree in (2, 3, 5, 8, 10):
            for transition in range(word_degree):
                row = audit_mixed_word_fiber(
                    half_degree,
                    word_degree,
                    transition,
                )
                assert row.selected_adjacent_involutions_distinct
                assert row.selected_four_bit_products_pairwise_distinct
                assert row.later_repeated_involutions_present
                assert row.maximum_product_fiber_size <= row.one_quarter_bound
                assert row.mixed_word_fiber_bound_verified


def test_repeated_and_noncommuting_word_context_does_not_change_injection_bound():
    for transition in (0, 2, 5):
        row = audit_mixed_word_fiber(5, 6, transition)
        assert row.subword_cube_size == 2**7
        assert row.maximum_product_fiber_size <= 2**5


def test_normalized_word_lcu_bound_is_independent_of_word_count():
    for word_count in (1, 10, 10**6, 10**18):
        row = mixed_word_LCU_bound_control(
            word_degree=64,
            copy_count=17,
            mixed_operator_count=32,
            word_count=word_count,
        )
        assert row.individual_word_bias_upper_bound == f"1/{2**17}"
        assert row.mixed_word_LCU_bias_upper_bound == f"1.0/{2**17}"
        assert row.bound_independent_of_word_degree
        assert row.bound_independent_of_operator_count
        assert row.normalized_LCU_bound_verified


def test_normalized_commutator_coefficients_do_not_amplify():
    row = mixed_word_LCU_bound_control(
        word_degree=2,
        copy_count=11,
        mixed_operator_count=2,
        word_count=2,
        coefficient_l1_norm_upper_bound=1.0,
    )
    assert row.mixed_word_LCU_bias_upper_bound == f"1.0/{2**11}"
    assert row.normalized_LCU_bound_verified


def test_natural_mixed_word_bound_is_inverse_candidate():
    for half_degree in (4, 8, 16, 32, 64):
        row = mixed_word_scaling_record(half_degree)
        assert row.normalized_mixed_word_bias_upper_bound <= (
            row.inverse_64_candidates
        )
        assert row.normalized_mixed_word_LCU_bias_upper_bound <= (
            row.inverse_64_candidates
        )
        assert row.bound_at_most_inverse_64_candidates


def test_report_closes_normalized_mixtures_but_not_matrix_Hecke_polar():
    report = build_mixed_word_LCU_report()
    assert report.theorem.adjacent_pair_injection_extends_to_mixed_words
    assert report.theorem.all_degree_mixed_word_trace_no_go_proved
    assert report.theorem.normalized_mixed_word_LCU_no_go_proved
    assert not report.theorem.large_word_l1_bounded_operator_no_go_proved
    assert not report.theorem.matrix_Hecke_polar_no_go_proved
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_live_mixed_word_report_is_json_serializable(tmp_path):
    output = tmp_path / "mixed-word.json"
    payload = write_mixed_word_LCU_report(output)
    assert output.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"]["normalized_mixed_word_LCU_no_go_proved"]
    assert not payload["claim_gate"]["matrix_Hecke_polar_no_go_proved"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
