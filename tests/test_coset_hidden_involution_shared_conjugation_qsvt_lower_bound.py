import math

from coset_hidden_involution_shared_conjugation_qsvt_lower_bound import (
    QSVT_degree_scaling_record,
    bounded_polynomial_degree_lower_bound,
    build_shared_conjugation_QSVT_report,
    write_shared_conjugation_QSVT_report,
)


def test_degree_bound_scales_as_square_root_candidate_count():
    for candidates in (1, 16, 10_000, 10**12):
        for variation in (0.1, 0.5, 1.0):
            observed = bounded_polynomial_degree_lower_bound(
                candidates,
                variation,
            )
            assert observed == math.sqrt(candidates * variation)


def test_natural_bulk_edges_are_inverse_candidate_scale():
    for half_degree in (4, 8, 16, 32, 64):
        row = QSVT_degree_scaling_record(half_degree)
        candidates = int(row.hidden_matching_count_decimal)
        assert row.normalized_bulk_eigenvalue_lower == 1 / (2 * candidates)
        assert row.normalized_bulk_eigenvalue_upper == 3 / (2 * candidates)
        assert row.polynomial_degree_lower_bound == math.sqrt(
            candidates * row.required_response_variation
        )
        assert not row.single_operator_QSVT_polynomial_time


def test_log_degree_is_half_candidate_log_up_to_response_constant():
    rows = [QSVT_degree_scaling_record(value) for value in (8, 16, 32, 64)]
    for row in rows:
        expected = 0.5 * (
            row.hidden_matching_count_log2
            + math.log2(row.required_response_variation)
        )
        assert abs(row.polynomial_degree_log2_lower_bound - expected) < 1e-12


def test_report_closes_single_operator_but_not_matrix_recoupling():
    report = build_shared_conjugation_QSVT_report()
    theorem = report.theorem
    assert theorem.exact_polynomial_degree_lower_bound_proved
    assert theorem.constant_bulk_response_single_operator_QSVT_superpolynomial_proved
    assert theorem.generic_alternating_reflection_cost_recovered
    assert theorem.low_degree_kernel_suppression_ruled_out
    assert not theorem.multioperator_matrix_CS_transform_ruled_out
    assert not theorem.rational_postselected_filter_ruled_out
    assert not theorem.integrable_recoupling_fast_forward_ruled_out
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_preserves_direct_basis_transform_escape():
    report = build_shared_conjugation_QSVT_report()
    assert report.claim_gate[
        "single_operator_shared_average_QSVT_no_go_proved"
    ]
    assert not report.claim_gate["multioperator_matrix_CS_transform_ruled_out"]
    assert not report.claim_gate["integrable_recoupling_fast_forward_ruled_out"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_shared_QSVT_report_is_json_serializable(tmp_path):
    output = tmp_path / "shared-QSVT.json"
    payload = write_shared_conjugation_QSVT_report(output)
    assert output.exists()
    assert payload["status"] == (
        "shared-conjugation-single-operator-QSVT-sqrt-M-no-go"
    )
    assert payload["claim_gate"][
        "single_operator_shared_average_QSVT_no_go_proved"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
