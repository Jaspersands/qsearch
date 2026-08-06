from self_dual_wreath_canonical_coefficient_affine import (
    audit_canonical_coefficient_control,
    run_canonical_coefficient_affine,
)


def _distinct_triangle():
    return (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )


def test_distinct_w3_has_uniform_affine_coefficient_certificates() -> None:
    record = audit_canonical_coefficient_control(
        "distinct",
        3,
        (2, 1),
        _distinct_triangle(),
    )

    assert record.exact_canonical_coefficient_audit_verified
    assert record.fractional_merge_count == 9
    assert record.coefficient_affine_certificate_failure_count == 0
    assert record.every_fractional_merge_has_coefficient_affine_certificate
    assert record.observed_active_supports == ((0, 2, 5, 7),)
    assert all(row.active_support_is_affine for row in record.node_records)
    assert all(
        row.active_left_mask_count == row.active_right_mask_count
        for row in record.node_records
    )


def test_common_scalar_metric_is_normalized_before_transfer() -> None:
    record = audit_canonical_coefficient_control(
        "distinct",
        3,
        (2, 1),
        _distinct_triangle(),
    )
    scaled = [
        row
        for row in record.node_records
        if row.left_metric_scale > 1.5
    ]

    assert scaled
    assert all(abs(row.left_metric_scale - 2.0) < 1e-8 for row in scaled)
    assert all(abs(row.right_metric_scale - 2.0) < 1e-8 for row in scaled)
    assert all(row.child_metric_equality_residual < 1e-8 for row in scaled)
    assert all(
        row.coefficient_transfer_initial_projection_residual < 1e-8
        and row.coefficient_transfer_final_projection_residual < 1e-8
        for row in scaled
    )


def test_repeated_labels_break_the_coefficient_affine_normal_form() -> None:
    record = audit_canonical_coefficient_control(
        "repeated",
        3,
        (2, 1),
        (((3,), (2, 1)),) * 3,
    )

    assert record.exact_canonical_coefficient_audit_verified
    assert record.coefficient_affine_certificate_failure_count > 0
    assert record.nonscalar_or_unequal_metric_count > 0
    assert record.nonaffine_active_support_count > 0
    assert not record.every_fractional_merge_has_coefficient_affine_certificate


def test_report_keeps_recoupling_and_algorithm_claims_open() -> None:
    report = run_canonical_coefficient_affine()

    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.headline_metrics[
        "label_simple_coefficient_affine_certificate_failure_count"
    ] == 0
    assert report.claim_gate["canonical_minimum_norm_identities_proved"]
    assert report.claim_gate[
        "finite_label_simple_coefficient_affine_signal"
    ]
    assert report.claim_gate[
        "repeated_labels_falsify_universal_coefficient_affinity"
    ]
    assert not report.claim_gate[
        "all_n_collision_free_coefficient_affine_theorem_proved"
    ]
    assert not report.claim_gate[
        "multiplicity_free_recoupling_formula_proved"
    ]
    assert not report.claim_gate["coherent_minimum_norm_synthesis_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
