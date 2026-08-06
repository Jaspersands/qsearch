from self_dual_wreath_collision_free_frame_probe import (
    audit_collision_free_frame_tuple,
    perfect_matchings,
    run_collision_free_frame_probe,
)


def test_six_source_partitions_have_fifteen_perfect_matchings() -> None:
    partitions = (
        (5,),
        (4, 1),
        (3, 2),
        (2, 2, 1),
        (2, 1, 1, 1),
        (1, 1, 1, 1, 1),
    )
    matchings = perfect_matchings(partitions)
    assert len(matchings) == 15
    assert len(set(matchings)) == 15


def test_collision_free_w4_pairing_reaches_two_copy_scale() -> None:
    record = audit_collision_free_frame_tuple(
        4,
        (
            ((4,), (2, 2)),
            ((3, 1), (2, 1, 1)),
        ),
    )
    assert record.all_source_partitions_distinct
    assert record.copy_count == 2
    assert record.top_eigenpair_residual < 1e-7
    assert record.factor_two_target_bound_satisfied


def test_exact_target_is_slightly_violated_by_collision_free_w5_tuple() -> None:
    record = audit_collision_free_frame_tuple(
        5,
        (
            ((5,), (4, 1)),
            ((3, 2), (2, 2, 1)),
            ((2, 1, 1, 1), (1, 1, 1, 1, 1)),
        ),
    )
    assert record.all_source_partitions_distinct
    assert record.top_eigenpair_residual < 1e-7
    assert record.top_eigenvalue > 0.25
    assert not record.exact_target_bound_satisfied
    assert record.factor_two_target_bound_satisfied


def test_report_preserves_polynomial_factor_conjecture_only() -> None:
    report = run_collision_free_frame_probe()
    assert report.headline_metrics[
        "w5_exact_two_to_one_minus_k_violation_count"
    ] > 0
    assert report.claim_gate[
        "factor_two_target_bound_survives_finite_probes"
    ]
    assert not report.claim_gate[
        "collision_free_polynomial_factor_norm_bound_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
