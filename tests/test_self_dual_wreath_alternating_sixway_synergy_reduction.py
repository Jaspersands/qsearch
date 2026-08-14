from self_dual_wreath_alternating_sixway_synergy_reduction import (
    audit_sixway_synergy_finite,
    proper_marginal_scaling_control,
    run_alternating_sixway_synergy_reduction,
    write_alternating_sixway_synergy_reduction_report,
)


def test_thirteen_proper_anova_blocks_are_bounded_by_five_label_theorem() -> None:
    for n in (3, 4, 5):
        row = audit_sixway_synergy_finite(n)
        assert row.lower_anova_bound_verified
        assert row.lower_anova_energy <= row.thirteen_five_label_upper_bound + 1e-9


def test_exact_basis_change_identity_holds_but_finite_equality_fails() -> None:
    rows = [audit_sixway_synergy_finite(n) for n in (3, 4, 5)]

    assert all(row.exact_basis_change_identity_residual < 2e-9 for row in rows)
    assert rows[0].finite_order_six_equals_core
    assert all(not row.finite_order_six_equals_core for row in rows[1:])


def test_proper_marginal_and_identity_support_errors_decay_in_controls() -> None:
    rows = [proper_marginal_scaling_control(n) for n in (5, 8, 12, 16)]

    assert all(row.both_error_terms_asymptotically_vanishing for row in rows)
    assert [row.full_five_label_chi_square for row in rows] == sorted(
        (row.full_five_label_chi_square for row in rows), reverse=True
    )
    assert [row.even_lower_identity_support_contribution for row in rows] == sorted(
        (row.even_lower_identity_support_contribution for row in rows), reverse=True
    )


def test_report_leaves_exactly_one_renyi_block_open(tmp_path) -> None:
    report = run_alternating_sixway_synergy_reduction()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["proper_anova_block_count"] == 13
    assert report.headline_metrics["remaining_sixway_block_count"] == 1
    assert report.claim_gate["all_proper_anova_blocks_vanish_proved"]
    assert report.claim_gate[
        "unique_sixway_anova_block_is_only_collision_obstruction"
    ]
    assert report.claim_gate[
        "sixway_anova_and_z6_asymptotically_equivalent_proved"
    ]
    assert not report.claim_gate["sixway_anova_block_subpolynomial_proved"]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "sixway.json"
    payload = write_alternating_sixway_synergy_reduction_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
