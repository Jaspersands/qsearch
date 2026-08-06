import numpy as np
import pytest

from self_dual_wreath_shorted_overlap_balance import (
    audit_shorted_overlap_node,
    audit_wreath_shorted_overlap,
    run_shorted_overlap_balance,
    unique_affine_flag_merges,
)


def test_shorted_metric_pencil_reproduces_fractional_spectrum() -> None:
    left = np.diag((2.0, 1.0))
    right = np.diag((1.0, 2.0))

    record = audit_shorted_overlap_node(
        "unequal-positive-control",
        (left, right),
        (0,),
        (1,),
    )

    assert record.exact_shorted_overlap_spectrum_verified
    assert record.actual_fractional_eigenvalues == pytest.approx((
        1 / 3,
        2 / 3,
    ))
    assert record.metric_predicted_fractional_eigenvalues == pytest.approx((
        1 / 3,
        2 / 3,
    ))
    assert not record.balanced_shorted_overlap


def test_all_unique_three_bit_affine_merges_are_enumerated() -> None:
    merges = unique_affine_flag_merges()

    assert len(merges) == 77
    assert len(set(merges)) == 77
    assert {len(left) for left, _ in merges} == {1, 2, 4}


def test_distinct_w3_balance_is_emergent_and_nonreducing() -> None:
    labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    record = audit_wreath_shorted_overlap(
        "distinct",
        3,
        (2, 1),
        labels,
        compute_pairwise_generation=True,
    )

    assert record.exact_shorted_overlap_theorem_verified
    assert record.fractional_merge_count == 9
    assert record.all_fractional_merges_balanced
    assert record.observed_fractional_eigenvalues == (0.5,)
    assert record.nonreducing_fractional_merge_count == 9
    assert record.emergent_fractional_merge_count == 9
    assert record.reducing_affine_core_exhaustion_falsified


def test_repeated_labels_violate_shorted_metric_balance() -> None:
    labels = (((3,), (2, 1)),) * 3
    record = audit_wreath_shorted_overlap(
        "repeated",
        3,
        (2, 1),
        labels,
        compute_pairwise_generation=True,
    )

    assert record.exact_shorted_overlap_theorem_verified
    assert record.unbalanced_fractional_merge_count > 0
    assert not record.all_fractional_merges_balanced
    assert record.observed_fractional_eigenvalues == pytest.approx((
        1 / 3,
        4 / 9,
        0.5,
        5 / 9,
        2 / 3,
    ))


def test_report_keeps_all_n_and_constructive_claims_closed() -> None:
    report = run_shorted_overlap_balance()

    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.claim_gate["exact_shorted_overlap_criterion_proved"]
    assert report.claim_gate[
        "affine_core_exhaustion_necessity_falsified"
    ]
    assert report.claim_gate[
        "finite_label_simple_shorted_balance_observed"
    ]
    assert report.claim_gate["repeated_labels_falsify_universal_balance"]
    assert not report.claim_gate[
        "collision_free_shorted_metric_equality_proved_all_n"
    ]
    assert not report.claim_gate[
        "coherent_compressed_metric_transform_proved"
    ]
    assert not report.claim_gate["hierarchical_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
