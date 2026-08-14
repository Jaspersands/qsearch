from self_dual_wreath_recoupling_collision_channel_reduction import (
    audit_full_to_coarse_trim,
    audit_recoupling_collision_channel,
    plancherel_marginal_identity_countermodel,
    run_recoupling_collision_channel_reduction,
    write_recoupling_collision_channel_report,
)


def test_physical_likelihood_is_exact_racah_collision_density() -> None:
    controls = (
        audit_recoupling_collision_channel(
            "S4", 4, ((3, 1),) * 4, 1
        ),
        audit_recoupling_collision_channel(
            "S5", 5, ((3, 2),) * 4, 1
        ),
        audit_recoupling_collision_channel(
            "S5-MIXED",
            5,
            ((4, 1), (3, 2), (4, 1), (3, 2)),
            1,
        ),
    )

    for row in controls:
        assert abs(row.coupling_probability_sum - 1.0) < 2e-9
        assert row.maximum_row_marginal_residual < 2e-9
        assert row.maximum_column_marginal_residual < 2e-9
        assert row.maximum_likelihood_factorization_residual < 2e-9
        assert row.retained_second_moment_identity_residual < 2e-9
        assert row.exact_recoupling_collision_channel_verified


def test_full_trimmed_collision_dominates_coarse_orbit_moment() -> None:
    for n, threshold in ((3, 1), (4, 1), (4, 2), (5, 1), (5, 4), (5, 5)):
        row = audit_full_to_coarse_trim(n, threshold)
        assert row.full_collision_decomposition_residual < 2e-8
        assert row.coarse_graining_slack > -2e-8
        assert row.transpose_orbit_data_processing_verified


def test_exact_plancherel_marginals_do_not_control_joint_collision() -> None:
    rows = [plancherel_marginal_identity_countermodel(n) for n in (5, 10, 20)]

    assert all(row.exact_plancherel_row_marginals for row in rows)
    assert all(row.exact_plancherel_column_marginals for row in rows)
    assert all(row.independent_coupling_collision == 1.0 for row in rows)
    assert all(
        row.identity_block_coupling_collision == row.partition_count
        for row in rows
    )
    assert [row.collision_inflation for row in rows] == sorted(
        row.collision_inflation for row in rows
    )


def test_report_keeps_growing_row_delocalization_open(tmp_path) -> None:
    report = run_recoupling_collision_channel_reduction()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "physical_likelihood_recoupling_collision_factorization_proved"
    ]
    assert report.claim_gate[
        "coarse_trimmed_moment_bounded_by_full_collision_proved"
    ]
    assert not report.claim_gate[
        "rank_marginals_suffice_for_joint_recoupling_mixing"
    ]
    assert not report.claim_gate[
        "fixed_row_recoupling_theorem_applies_to_plancherel_shapes"
    ]
    assert not report.claim_gate[
        "natural_plancherel_racah_collision_subpolynomial_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "recoupling-collision.json"
    payload = write_recoupling_collision_channel_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
