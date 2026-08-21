from fractions import Fraction

from coset_hidden_involution_all_copy_target_lcu_no_go import (
    all_copy_LCU_scaling_record,
    audit_all_copy_basis_formula,
    build_all_copy_target_LCU_no_go_report,
    local_double_coset_multiplicity,
    write_all_copy_target_LCU_no_go_report,
)
from coset_hidden_involution_source_local_likelihood_no_go import _subgroups


def test_local_HtH_multiplicity_is_two_inside_K_and_one_outside():
    group, centralizer, _, _, hidden = _subgroups(4, 2, 2)
    centralizer_set = set(centralizer)
    inside = centralizer[0]
    outside = next(value for value in group if value not in centralizer_set)
    inside_multiplicities = {
        local_double_coset_multiplicity(value, inside, hidden)
        for value in group
        if local_double_coset_multiplicity(value, inside, hidden)
    }
    outside_multiplicities = {
        local_double_coset_multiplicity(value, outside, hidden)
        for value in group
        if local_double_coset_multiplicity(value, outside, hidden)
    }
    assert inside_multiplicities == {2}
    assert outside_multiplicities == {1}


def test_every_all_copy_basis_element_has_zero_or_exact_two_to_minus_k_bias():
    controls = [
        audit_all_copy_basis_formula(3, 1, 2),
        audit_all_copy_basis_formula(3, 1, 3),
        audit_all_copy_basis_formula(4, 2, 2),
    ]
    for row in controls:
        assert row.maximum_baseline_formula_residual == 0
        assert row.maximum_likelihood_formula_residual == 0
        assert row.maximum_bias_formula_residual == 0
        assert row.outside_K_local_double_coset_multiplicity_always_one
        assert row.all_basis_elements_have_zero_or_two_to_minus_k_bias
        assert row.exact_basis_formula_verified
        assert row.zero_bias_basis_element_count + (
            row.exact_two_to_minus_k_bias_basis_element_count
        ) == row.product_basis_element_count


def test_natural_copy_unit_L1_bound_is_at_most_inverse_64_candidates():
    for half_degree in (4, 8, 16, 32, 64, 128):
        row = all_copy_LCU_scaling_record(half_degree)
        assert row.unit_L1_bias_upper_bound <= row.inverse_64_candidates
        assert int(row.constant_bias_L1_norm_lower_bound_decimal) == 2**row.copy_count
        assert row.coefficient_weight_classically_computable_in_copy_linear_time
        assert not row.normalized_LCU_has_useful_linear_bias


def test_report_extends_beyond_diagonal_and_mixed_Hecke_LCUs():
    report = build_all_copy_target_LCU_no_go_report()
    theorem = report.theorem
    assert theorem.exact_all_finite_groups_basis_formula_proved
    assert theorem.arbitrary_all_copy_target_L1_LCU_bound_proved
    assert theorem.normalized_sparse_target_recoupling_linear_detector_ruled_out
    assert theorem.efficiently_sampleable_LCU_expectation_classically_estimable
    assert not theorem.nonlinear_spectral_function_no_go_proved
    assert not theorem.bounded_operator_large_L1_no_go_proved
    assert not theorem.matrix_CS_polar_no_go_proved
    assert not theorem.adaptive_postselection_no_go_proved
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_preserves_the_nonlinear_operator_boundary():
    report = build_all_copy_target_LCU_no_go_report()
    assert report.claim_gate[
        "arbitrary_all_copy_target_unit_L1_bias_no_go_proved"
    ]
    assert not report.claim_gate["nonlinear_spectral_function_no_go_proved"]
    assert not report.claim_gate["bounded_operator_large_L1_no_go_proved"]
    assert not report.claim_gate["matrix_CS_polar_no_go_proved"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_all_copy_target_LCU_report_is_json_serializable(tmp_path):
    output = tmp_path / "all-copy-target-LCU.json"
    payload = write_all_copy_target_LCU_no_go_report(output)
    assert output.exists()
    assert payload["status"] == (
        "all-copy-target-normalized-LCU-no-go-proved-nonlinear-polar-open"
    )
    assert payload["claim_gate"][
        "arbitrary_all_copy_target_unit_L1_bias_no_go_proved"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
