import math

from coset_hidden_involution_normalized_likelihood_charge_commutator_no_go import (
    audit_likelihood_commutator_bound,
    build_normalized_likelihood_charge_no_go_report,
    normalized_commutator_scaling_record,
    write_normalized_likelihood_charge_no_go_report,
)


def test_finite_incidence_controls_match_exact_centered_second_moment():
    for degree, transpositions, copies in ((3, 1, 1), (3, 1, 2), (4, 2, 1)):
        row = audit_likelihood_commutator_bound(
            degree,
            transpositions,
            copies,
        )
        assert abs(row.normalized_source_mean_Z - 1.0) < 1e-12
        assert abs(
            row.normalized_source_centered_second_moment - row.predicted_eta
        ) < 1e-12
        assert row.exact_synthesis_moment_verified


def test_universal_contraction_commutator_bound_holds_in_finite_controls():
    for degree, transpositions, copies in ((3, 1, 1), (3, 1, 2), (4, 2, 1)):
        row = audit_likelihood_commutator_bound(
            degree,
            transpositions,
            copies,
        )
        assert row.maximum_random_contraction_commutator_energy <= (
            row.universal_commutator_energy_upper_bound + 1e-12
        )
        assert row.maximum_bound_residual == 0
        assert row.universal_contraction_commutator_bound_verified


def test_natural_normalized_commutator_mass_is_factorially_small():
    rows = [
        normalized_commutator_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    assert all(row.eta <= 1 / 64 for row in rows)
    assert all(
        row.normalized_A_charge_commutator_energy_log2_upper_bound
        <= -4 - 2 * math.log2(int(row.hidden_matching_count_decimal))
        for row in rows
    )
    assert all(
        math.isfinite(row.normalized_A_charge_commutator_energy_log2_upper_bound)
        for row in rows
    )
    assert all(not row.inverse_polynomial_commutator_mass_possible for row in rows)
    assert all(
        right.source_mass_above_threshold_log2_upper_bound
        < left.source_mass_above_threshold_log2_upper_bound
        for left, right in zip(rows, rows[1:])
    )


def test_report_kills_normalized_third_operator_criterion_without_overclaim():
    report = build_normalized_likelihood_charge_no_go_report()
    theorem = report.theorem
    assert theorem.exact_source_centered_second_moment_proved
    assert theorem.charge_spectral_conditional_expectation_of_Z_is_identity_proved
    assert theorem.normalized_A_D_commutator_energy_inverse_candidate_squared_proved
    assert theorem.inverse_polynomial_A_D_energy_on_inverse_polynomial_mass_ruled_out
    assert not theorem.finite_conditioned_charge_covariance_promotes_to_natural_matrix_signal
    assert not theorem.unnormalized_Z_structured_fast_forward_compiled
    assert not theorem.direct_non_black_box_matrix_transform_ruled_out
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_preserves_unnormalized_or_direct_transform_escape():
    report = build_normalized_likelihood_charge_no_go_report()
    assert report.claim_gate[
        "inverse_polynomial_normalized_commutator_mass_ruled_out"
    ]
    assert not report.claim_gate["unnormalized_Z_structured_fast_forward_compiled"]
    assert not report.claim_gate["direct_non_black_box_matrix_transform_ruled_out"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_normalized_commutator_report_is_json_serializable(tmp_path):
    output = tmp_path / "normalized-commutator.json"
    payload = write_normalized_likelihood_charge_no_go_report(output)
    assert output.exists()
    assert payload["status"] == (
        "normalized-likelihood-charge-commutator-natural-mass-no-go"
    )
    assert payload["claim_gate"][
        "normalized_A_D_commutator_energy_at_most_4eta_over_M2"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
