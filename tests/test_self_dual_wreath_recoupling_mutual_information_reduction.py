from self_dual_wreath_recoupling_mutual_information_reduction import (
    audit_recoupling_mutual_information_finite,
    marginally_perfect_mutual_information_countermodel,
    recoupling_entropy_scaling_control,
    run_recoupling_mutual_information_reduction,
    write_recoupling_mutual_information_report,
)


def test_full_six_label_kl_has_exact_racah_information_chain() -> None:
    for n in range(3, 6):
        row = audit_recoupling_mutual_information_finite(n)
        assert row.full_kl_chain_residual_bits < 2e-9
        assert row.left_five_label_chain_residual_bits < 2e-9
        assert row.right_five_label_chain_residual_bits < 2e-9
        assert row.exact_non_mi_remainder_formula_residual_bits < 2e-9
        assert row.maximum_five_label_kl_bound_violation_bits < 2e-9
        assert row.full_to_coarse_kl_contraction_slack_bits > -2e-9
        assert row.exact_recoupling_mutual_information_reduction_verified


def test_non_mutual_information_remainder_bound_vanishes() -> None:
    rows = [
        recoupling_entropy_scaling_control(n)
        for n in (16, 20, 24, 30, 40, 50)
    ]

    assert all(row.remainder_asymptotically_vanishing for row in rows)
    assert [row.non_mutual_information_remainder_upper_bits for row in rows] == sorted(
        (row.non_mutual_information_remainder_upper_bits for row in rows),
        reverse=True,
    )
    assert not any(
        row.physical_average_racah_mutual_information_sublogarithmic_proved
        for row in rows
    )


def test_perfect_plancherel_marginals_can_have_large_mutual_information() -> None:
    rows = [
        marginally_perfect_mutual_information_countermodel(n)
        for n in (5, 10, 20, 30)
    ]

    assert all(row.row_marginal_kl_to_plancherel_bits == 0 for row in rows)
    assert all(row.column_marginal_kl_to_plancherel_bits == 0 for row in rows)
    assert all(
        row.identity_block_mutual_information_bits == row.plancherel_entropy_bits
        for row in rows
    )
    assert [row.plancherel_entropy_over_log2_n for row in rows] == sorted(
        row.plancherel_entropy_over_log2_n for row in rows
    )
    assert all(row.asymptotic_superlogarithmic_information_certified for row in rows)


def test_report_prefers_entropy_over_collision_when_tail_dominated(tmp_path) -> None:
    report = run_recoupling_mutual_information_reduction()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "six_label_kl_is_average_racah_mi_plus_o_one_proved"
    ]
    assert report.claim_gate[
        "coarse_rank_entropy_sublog_if_average_racah_mi_sublog_proved"
    ]
    assert not report.claim_gate[
        "subpolynomial_collision_required_for_rank_transfer"
    ]
    assert not report.claim_gate[
        "natural_physical_average_racah_mi_sublogarithmic_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "recoupling-mi.json"
    payload = write_recoupling_mutual_information_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
