from coset_hidden_involution_diagonal_charge_bias_no_go import (
    audit_diagonal_element_bias,
    build_diagonal_charge_bias_no_go_report,
    diagonal_charge_scaling_record,
    write_diagonal_charge_bias_no_go_report,
)


def test_elementwise_diagonal_bias_formula_on_distinct_groups():
    controls = [
        audit_diagonal_element_bias(3, 1, 2),
        audit_diagonal_element_bias(4, 2, 2),
        audit_diagonal_element_bias(3, 1, 3),
    ]
    for control in controls:
        assert control.centralizer_element_count == control.centralizer_order
        assert (
            control.centralizer_element_count
            + control.noncentralizer_element_count
            == control.group_order
        )
        assert control.expected_inside_centralizer_weighted_trace == "1"
        assert control.expected_outside_centralizer_weighted_trace == (
            f"1/{2**control.copy_count}"
        )
        assert control.maximum_baseline_formula_residual == 0.0
        assert control.maximum_likelihood_formula_residual == 0.0
        assert control.exact_elementwise_bias_formula_verified


def test_natural_copy_normalized_bias_is_inverse_candidate_scale():
    for half_degree in (4, 8, 16, 32, 64):
        row = diagonal_charge_scaling_record(half_degree)
        candidates = int(row.conjugacy_class_size_decimal)
        assert row.unit_LCU_bias_upper_bound == 2.0 ** (-row.copy_count)
        assert row.unit_LCU_bias_upper_bound <= 1.0 / (64.0 * candidates)
        assert row.bound_at_most_inverse_64_candidates
        assert int(row.constant_bias_LCU_norm_lower_bound_decimal) == 2**row.copy_count
        assert not row.normalized_diagonal_LCU_has_constant_bias


def test_report_keeps_interleaved_and_nonlinear_escapes_open():
    report = build_diagonal_charge_bias_no_go_report()
    assert report.theorem.exact_all_finite_groups_elementwise_formula_proved
    assert report.theorem.unit_LCU_bias_upper_bound_proved
    assert report.theorem.natural_copy_bias_inverse_candidate_bound_proved
    assert report.theorem.normalized_diagonal_class_charge_detector_ruled_out
    assert not report.theorem.interleaved_recoupling_walk_ruled_out
    assert not report.theorem.nonlinear_spectral_decoder_constructed
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_live_report_is_json_serializable(tmp_path):
    output_path = tmp_path / "diagonal-charge-bias-no-go.json"
    payload = write_diagonal_charge_bias_no_go_report(output_path)
    assert output_path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"][
        "unit_normalized_diagonal_LCU_inverse_candidate_bias_proved"
    ]
