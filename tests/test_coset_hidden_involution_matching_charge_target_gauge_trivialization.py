from coset_hidden_involution_binary_decision_reduction import symmetric_group
from coset_hidden_involution_matching_charge_target_gauge_trivialization import (
    audit_quotient_gauge_trivialization,
    build_target_gauge_trivialization_report,
    direct_relative_source_action,
    gauge_change_representative,
    quotient_relative_coordinates,
    representative_covariant_source_action,
    write_target_gauge_trivialization_report,
)


def test_relative_coordinates_are_invariant_under_diagonal_gauge_change():
    group = symmetric_group(4)
    sources = (group[3], group[7], group[11])
    target = group[5]
    expected = quotient_relative_coordinates(sources, target)
    for gauge in group:
        changed_sources, changed_target = gauge_change_representative(
            sources,
            target,
            gauge,
        )
        assert quotient_relative_coordinates(
            changed_sources,
            changed_target,
        ) == expected


def test_target_controlled_conjugation_becomes_direct_relative_right_action():
    group = symmetric_group(4)
    sources = (group[4], group[9])
    for target in group[:8]:
        relative = quotient_relative_coordinates(sources, target)
        for charge_term in group[:8]:
            for source_index in range(len(sources)):
                acted_sources, acted_target = representative_covariant_source_action(
                    sources,
                    target,
                    charge_term,
                    source_index,
                )
                observed = quotient_relative_coordinates(
                    acted_sources,
                    acted_target,
                )
                expected = direct_relative_source_action(
                    relative,
                    charge_term,
                    source_index,
                )
                assert observed == expected


def test_finite_controls_verify_gauge_covariance_and_trivialization():
    for degree, copies in ((3, 2), (4, 2), (4, 3)):
        row = audit_quotient_gauge_trivialization(degree, copies)
        assert row.quotient_coordinate_gauge_failure_count == 0
        assert row.controlled_action_gauge_covariance_failure_count == 0
        assert row.relative_source_action_failure_count == 0
        assert not row.target_coordinate_changed_by_controlled_action
        assert row.exact_gauge_trivialization_verified


def test_report_kills_physical_target_control_but_not_external_orbit():
    report = build_target_gauge_trivialization_report()
    theorem = report.theorem
    assert theorem.exact_all_finite_groups_gauge_trivialization_proved
    assert not theorem.target_diagonal_charge_control_is_genuinely_target_coupled
    assert not theorem.coherent_D_phase_label_from_physical_target_is_detector
    assert not theorem.external_candidate_charge_orbit_invalidated
    assert not theorem.target_changing_convolution_route_ruled_out
    assert not theorem.all_copy_target_recoupling_compiled
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_preserves_target_changing_escape():
    report = build_target_gauge_trivialization_report()
    assert report.claim_gate[
        "target_diagonal_conjugated_charge_is_source_local_after_gauge_fixing"
    ]
    assert report.claim_gate["external_candidate_charge_orbit_remains_valid"]
    assert not report.claim_gate["target_changing_convolution_route_ruled_out"]
    assert not report.claim_gate["all_copy_target_recoupling_compiled"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_target_gauge_report_is_json_serializable(tmp_path):
    output = tmp_path / "target-gauge.json"
    payload = write_target_gauge_trivialization_report(output)
    assert output.exists()
    assert payload["status"] == (
        "physical-target-controlled-charge-gauge-trivialized"
    )
    assert payload["claim_gate"][
        "target_diagonal_conjugated_charge_is_source_local_after_gauge_fixing"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
