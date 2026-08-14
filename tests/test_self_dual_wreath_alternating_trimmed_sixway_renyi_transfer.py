from self_dual_wreath_alternating_trimmed_sixway_renyi_transfer import (
    audit_trimmed_sixway_renyi,
    canonical_trim_scaling_control,
    run_alternating_trimmed_sixway_renyi_transfer,
    write_alternating_trimmed_sixway_renyi_transfer_report,
)


def test_nontrivial_label_sector_exactly_equals_order_six_anova_energy() -> None:
    for n in range(2, 6):
        row = audit_trimmed_sixway_renyi(n, 1)
        assert row.nontrivial_fourier_sector_identity_residual is not None
        assert row.nontrivial_fourier_sector_identity_residual < 2e-8
        assert row.exact_trimmed_renyi_control_verified


def test_retained_signed_kl_obeys_second_moment_jensen_bound() -> None:
    for n, threshold in ((4, 1), (4, 2), (5, 1), (5, 4), (5, 5)):
        row = audit_trimmed_sixway_renyi(n, threshold)
        assert row.jensen_bound_violation < 2e-8
        assert row.retained_likelihood_second_moment >= 0
        assert row.exact_trimmed_renyi_control_verified


def test_finite_higher_dimension_cut_removes_most_a5_sixway_energy() -> None:
    untrimmed = audit_trimmed_sixway_renyi(5, 1)
    dimension_five = audit_trimmed_sixway_renyi(5, 5)

    assert untrimmed.untrimmed_nontrivial_sixway_energy > 1
    assert dimension_five.retained_fraction_of_untrimmed_sixway_energy < 1e-3
    assert dimension_five.retained_physical_mass < 1e-3


def test_synthetic_subpolynomial_trimmed_moment_has_sublog_entropy_bound() -> None:
    rows = [canonical_trim_scaling_control(n) for n in (12, 20, 30, 50)]

    assert all(row.subpolynomial_second_moment_hypothesis_satisfied for row in rows)
    assert [row.synthetic_retained_kl_over_log2_n_upper for row in rows] == sorted(
        (row.synthetic_retained_kl_over_log2_n_upper for row in rows), reverse=True
    )


def test_report_prefers_trimmed_over_untrimmed_renyi_target(tmp_path) -> None:
    report = run_alternating_trimmed_sixway_renyi_transfer()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "sixway_anova_is_nontrivial_coarse_label_fourier_sector_proved"
    ]
    assert report.claim_gate["canonical_trimmed_renyi_to_sublog_entropy_proved"]
    assert not report.claim_gate["untrimmed_sixway_subpolynomial_required"]
    assert not report.claim_gate[
        "canonical_trimmed_sixway_subpolynomial_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "trimmed-sixway.json"
    payload = write_alternating_trimmed_sixway_renyi_transfer_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
