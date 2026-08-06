import pytest

from self_dual_wreath_level_three_flag_audit import (
    audit_level_three_flags,
    flag_leaf_order,
    ordered_f2_three_bases,
    run_level_three_flag_audit,
)


def test_every_ordered_f2_three_basis_is_enumerated():
    bases = ordered_f2_three_bases()

    assert len(bases) == 168
    assert len(set(bases)) == 168
    assert flag_leaf_order((1, 2, 4)) == tuple(range(8))


def test_label_distinct_triangle_has_only_half_fractional_channels():
    record = audit_level_three_flags(
        "distinct",
        3,
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
        (2, 1),
    )

    assert record.exact_finite_flag_audit_verified
    assert record.pairwise_distinct_physical_labels
    assert record.fractional_eigenvalue_occurrence_count > 0
    assert record.observed_fractional_eigenvalues == (0.5,)
    assert record.nonhalf_fractional_eigenvalue_occurrence_count == 0
    assert record.half_integral_on_every_linear_flag


def test_repeated_labels_falsify_universal_half_integrality():
    record = audit_level_three_flags(
        "repeated",
        3,
        (((3,), (2, 1)),) * 3,
        (2, 1),
    )

    assert record.exact_finite_flag_audit_verified
    assert not record.pairwise_distinct_physical_labels
    assert record.nonhalf_fractional_eigenvalue_occurrence_count > 0
    assert record.observed_fractional_eigenvalues == pytest.approx(
        (1 / 3, 4 / 9, 0.5, 5 / 9, 2 / 3)
    )
    assert not record.half_integral_on_every_linear_flag


def test_report_keeps_all_n_and_constructive_gates_open():
    report = run_level_three_flag_audit()

    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.claim_gate[
        "finite_label_simple_half_integral_pattern_observed"
    ]
    assert report.claim_gate[
        "universal_balanced_tree_half_integrality_falsified"
    ]
    assert not report.claim_gate[
        "collision_free_half_integrality_proved_all_n"
    ]
    assert not report.claim_gate[
        "polynomial_relative_eigenspace_projectors_proved"
    ]
    assert not report.claim_gate["hierarchical_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_dependent_flag_basis_is_rejected():
    with pytest.raises(ValueError, match="linearly independent"):
        flag_leaf_order((1, 2, 3))
