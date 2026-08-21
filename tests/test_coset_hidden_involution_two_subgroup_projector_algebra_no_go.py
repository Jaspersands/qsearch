import itertools

from coset_hidden_involution_two_subgroup_projector_algebra_no_go import (
    audit_two_projector_word_normal_form,
    build_two_projector_algebra_report,
    compressed_word_power,
    reduce_idempotent_word,
    two_projector_scaling_record,
    write_two_projector_algebra_report,
)


def test_symbolic_Q_compressed_words_reduce_to_powers_of_QPQ():
    for length in range(11):
        for letters in itertools.product("PQ", repeat=length):
            word = "".join(letters)
            power = compressed_word_power(word)
            reduced = reduce_idempotent_word("Q" + word + "Q")
            expected = "Q" if power == 0 else "Q" + "PQ" * power
            assert reduced == expected


def test_dense_projector_controls_match_exact_word_power_normal_form():
    for parameters in ((7, 4, 3, 8), (9, 6, 5, 9)):
        row = audit_two_projector_word_normal_form(*parameters)
        assert row.maximum_matrix_residual < 1e-12
        assert row.every_Q_compressed_word_is_A_power
        assert row.exact_symbolic_normal_form_verified


def test_two_projector_query_lower_bound_is_square_root_candidate_count():
    for half_degree in (4, 8, 16, 32, 64):
        row = two_projector_scaling_record(half_degree)
        candidates = int(row.hidden_matching_count_decimal)
        assert row.subgroup_projector_query_lower_bound == (
            candidates * row.required_response_variation
        ) ** 0.5
        assert not row.two_projector_query_algorithm_polynomial_time


def test_report_extends_QSVT_bound_to_entire_two_projector_query_algebra():
    report = build_two_projector_algebra_report()
    theorem = report.theorem
    assert theorem.exact_all_word_Q_compression_normal_form_proved
    assert theorem.two_projector_B_to_B_algebra_is_univariate_proved
    assert theorem.ancilla_controlled_two_projector_query_bound_proved
    assert theorem.two_projector_constant_bulk_response_requires_sqrt_M_queries
    assert not theorem.third_operator_matrix_recoupling_ruled_out
    assert not theorem.direct_non_black_box_basis_transform_ruled_out
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_keeps_third_operator_escape_open():
    report = build_two_projector_algebra_report()
    assert report.claim_gate["Q_compressed_two_projector_algebra_is_univariate"]
    assert report.claim_gate["two_projector_black_box_fast_forward_ruled_out"]
    assert not report.claim_gate["third_operator_matrix_recoupling_ruled_out"]
    assert not report.claim_gate["direct_non_black_box_basis_transform_ruled_out"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_two_projector_report_is_json_serializable(tmp_path):
    output = tmp_path / "two-projector.json"
    payload = write_two_projector_algebra_report(output)
    assert output.exists()
    assert payload["status"] == (
        "two-subgroup-projector-algebra-sqrt-M-no-go-third-operator-open"
    )
    assert payload["claim_gate"][
        "two_projector_black_box_fast_forward_ruled_out"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
