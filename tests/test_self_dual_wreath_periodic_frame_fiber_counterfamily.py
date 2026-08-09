import pytest

from self_dual_wreath_periodic_frame_fiber_counterfamily import (
    audit_presentation_control,
    audit_subsequence_certificate,
    audit_transfer_certificate,
    periodic_scaling_records,
    run_periodic_frame_fiber_counterfamily,
)


def test_transfer_matrix_has_exact_five_root_annihilator_and_uniform_class():
    certificate = audit_transfer_certificate()
    assert certificate.state_count == 36
    assert certificate.transition_row_sum == 32
    assert certificate.transition_column_sum == 32
    assert certificate.transition_rank == 18
    assert certificate.annihilating_polynomial_roots == (0, 32, -16, 2, -1)
    assert certificate.exact_annihilating_polynomial_verified
    assert certificate.leading_projector_nonzero_entry_count == 18
    assert certificate.leading_projector_nonzero_entry == "1/18"
    assert certificate.exact_leading_projector_verified


def test_k_6m_plus_1_subsequence_has_exact_positive_fiber_excess():
    certificate = audit_subsequence_certificate()
    assert certificate.exact_krylov_recurrence_verified
    assert certificate.exact_closed_form_verified
    assert certificate.nonidentity_target_verified
    assert certificate.outer_valid_different_state_verified
    assert certificate.checked_fiber_excesses[:4] == (1, 43, 2731, 174763)
    assert certificate.checked_fiber_excesses == certificate.predicted_fiber_excesses


def test_periodic_nonidentity_margin_controls_decay_without_identity_padding():
    records = periodic_scaling_records(13)
    selected = [row for row in records if row.vanishing_margin_support_pair_exists]
    assert selected
    assert all(row.target_is_nonidentity for row in selected)
    assert all(
        row.selected_different_support_size == row.same_fiber_size + 1
        for row in selected
    )
    residue_one = [row for row in selected if row.period_count % 6 == 1]
    assert [row.period_count for row in residue_one] == [1, 7, 13]
    assert all(
        later.scalar_certificate_pressure_margin
        < earlier.scalar_certificate_pressure_margin
        for earlier, later in zip(residue_one, residue_one[1:])
    )
    assert residue_one[-1].same_fiber_density == pytest.approx(1 / 18, rel=1e-3)


def test_first_four_full_presentations_have_extra_pressure_loss():
    first = audit_presentation_control(1)
    second = audit_presentation_control(2)
    third = audit_presentation_control(3)
    fourth = audit_presentation_control(4)
    assert (first.same_support_size, first.different_support_size) == (2, 3)
    assert (second.same_support_size, second.different_support_size) == (43, 44)
    assert (third.same_support_size, third.different_support_size) == (1366, 1367)
    assert (fourth.same_support_size, fourth.different_support_size) == (
        54610,
        54611,
    )
    assert first.remaining_generator_count == 4
    assert second.remaining_generator_count == 5
    assert third.remaining_generator_count == 4
    assert fourth.remaining_generator_count == 3
    assert first.exact_S3_solution_count == 324
    assert second.exact_S3_solution_count == 396
    assert third.exact_S3_solution_count == 342
    assert fourth.exact_S3_solution_count == 126
    assert first.exact_S3_standard_normalized_character_average == pytest.approx(0.5)
    assert second.exact_S3_standard_normalized_character_average == pytest.approx(
        13 / 22
    )
    assert fourth.exact_S3_standard_normalized_character_average == pytest.approx(
        5 / 14
    )
    assert not first.support_size_bound_is_tight
    assert not second.support_size_bound_is_tight
    assert not third.support_size_bound_is_tight
    assert not fourth.support_size_bound_is_tight
    assert all(
        control.certified_extra_pressure_loss > 0
        for control in (first, second, third, fourth)
    )


def test_report_keeps_Sn_mass_and_speedup_gates_closed():
    report = run_periodic_frame_fiber_counterfamily()
    metrics = report.headline_metrics
    assert metrics["exact_periodic_transfer_theorem_count"] == 1
    assert metrics["infinite_nonidentity_margin_vanishing_counterfamily_count"] == 1
    assert metrics["support_bound_tight_presentation_count"] == 0
    assert metrics["asymptotic_Sn_mass_theorem_count"] == 0
    assert metrics["all_period_frame_rank_collapse_theorem_count"] == 1
    assert metrics["uniform_subleading_Sn_mass_theorem_count"] == 1
    assert report.claim_gate["nonidentity_periodic_counterfamily_constructed"]
    assert report.claim_gate[
        "uniform_support_certificate_gap_falsified_without_identity_padding"
    ]
    assert not report.claim_gate["leading_Sn_homomorphism_mass_proved"]
    assert not report.claim_gate[
        "nonvanishing_normalized_Sn_target_character_proved"
    ]
    assert report.claim_gate["periodic_family_uniformly_subleading_in_Sn"]
    assert not report.claim_gate["periodic_family_survives"]
    assert not report.claim_gate["speedup_claim_allowed"]
