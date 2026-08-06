import pytest

from self_dual_wreath_affine_core_flag_theorem import (
    audit_affine_core_matrices,
    audit_affine_flag_incidence,
    flag_leaf_order,
    is_affine_set,
    linear_span,
    run_affine_core_flag_theorem,
)


def test_affine_set_classifier_accepts_subspaces_and_cosets() -> None:
    subspace = linear_span((1, 2))
    coset = tuple(value ^ 1 for value in linear_span((2, 4)))

    assert is_affine_set(subspace, 3)
    assert is_affine_set(coset, 3)
    assert not is_affine_set((0, 1, 2), 3)


def test_every_affine_core_has_only_endpoint_or_half_flag_ratios() -> None:
    record = audit_affine_flag_incidence(
        "affine-control",
        3,
        (1, 2, 4),
        (
            linear_span((1, 2)),
            tuple(value ^ 1 for value in linear_span((2, 4))),
            linear_span((3, 5)),
        ),
    )

    assert record.exact_affine_flag_balance_verified
    assert record.other_ratio_count == 0
    assert set(record.observed_active_ratios) <= {0.0, 0.5, 1.0}


def test_nonaffine_three_point_core_produces_unbalanced_ratio() -> None:
    record = audit_affine_flag_incidence(
        "nonaffine-control",
        3,
        (1, 2, 4),
        ((0, 1, 2),),
    )

    assert not record.exact_affine_flag_balance_verified
    assert record.other_ratio_count > 0
    assert {1 / 3, 2 / 3} & set(record.observed_active_ratios)


def test_affine_core_operator_lift_survives_noncommuting_complements() -> None:
    record = audit_affine_core_matrices(
        "matrix-control",
        3,
        (1, 2, 4),
        (linear_span((1, 2)), linear_span((3, 5))),
        expect_affine=True,
    )

    assert record.noncommuting_leaf_pair_count > 0
    assert record.maximum_core_count_ratio_residual < 1e-9
    assert record.maximum_relative_isometry_residual < 1e-9
    assert record.exact_affine_core_matrix_theorem_verified


def test_report_does_not_promote_conditional_wreath_claims() -> None:
    report = run_affine_core_flag_theorem()

    assert report.claim_gate["affine_core_flag_balance_proved"]
    assert report.claim_gate["known_block_common_cores_covered"]
    assert report.claim_gate["nonaffine_membership_can_create_unbalanced_weights"]
    assert not report.claim_gate[
        "all_child_intersections_exhausted_by_affine_cores"
    ]
    assert not report.claim_gate["coherent_affine_core_projectors_compiled"]
    assert not report.claim_gate["hierarchical_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_flag_basis_is_rejected() -> None:
    with pytest.raises(ValueError, match="full binary basis"):
        flag_leaf_order(3, (1, 2, 3))
