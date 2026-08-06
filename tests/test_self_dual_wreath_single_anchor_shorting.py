from functools import lru_cache

import numpy as np

from self_dual_wreath_single_anchor_shorting import (
    audit_single_anchor_side,
    run_single_anchor_shorting,
)


def _projector(columns: np.ndarray) -> np.ndarray:
    basis, _ = np.linalg.qr(columns)
    return basis @ basis.T


@lru_cache(maxsize=1)
def _report():
    return run_single_anchor_shorting()


def test_transverse_noncommuting_leaf_preserves_anchor_shorting() -> None:
    e0 = np.asarray([1.0, 0.0, 0.0])
    e1 = np.asarray([0.0, 1.0, 0.0])
    e2 = np.asarray([0.0, 0.0, 1.0])
    anchor = _projector(np.column_stack((e0, e1)))
    transverse = _projector((e1 + e2)[:, None])

    record = audit_single_anchor_side(
        "transverse",
        (anchor, transverse),
        (0, 1),
        0,
        e0[:, None],
    )

    assert np.linalg.norm(anchor @ transverse - transverse @ anchor, ord=2) > 0
    assert record.single_anchor_orthogonality_premise_verified
    assert record.exact_single_anchor_shorting_verified
    assert record.shorted_metric_identity_residual < 1e-8
    assert record.minimum_synthesis_anchor_route_residual < 1e-8
    assert record.maximum_other_leaf_minimum_coefficient_norm < 1e-8


def test_duplicate_core_leaf_falsifies_anchor_premise() -> None:
    core = np.asarray([[1.0], [0.0]])
    anchor = core @ core.T

    record = audit_single_anchor_side(
        "duplicate",
        (anchor, anchor),
        (0, 1),
        0,
        core,
    )

    assert not record.single_anchor_orthogonality_premise_verified
    assert not record.exact_single_anchor_shorting_verified
    assert abs(record.shorted_metric_identity_residual - 0.5) < 1e-8


def test_w5_fractional_merges_are_all_isolated_single_anchor_controls() -> None:
    report = _report()

    assert len(report.wreath_controls) == 11
    assert all(
        row.child_intersection_equals_anchor_core
        and row.exact_single_anchor_balanced_merge_verified
        for row in report.wreath_controls
    )
    assert {
        tuple(sorted((row.left_anchor_mask, row.right_anchor_mask)))
        for row in report.wreath_controls
    } == {(3, 6)}
    assert {
        row.anchor_common_core_dimension for row in report.wreath_controls
    } == {5}


def test_report_keeps_global_anchor_and_sampler_claims_closed() -> None:
    report = _report()

    assert report.claim_gate["single_anchor_shorted_identity_proved"]
    assert report.claim_gate["selected_w5_fractional_merges_explained"]
    assert report.claim_gate["duplicate_anchor_core_breaks_identity"]
    assert not report.claim_gate[
        "all_n_overlap_decomposes_into_isolated_anchors"
    ]
    assert not report.claim_gate[
        "polynomial_coherent_anchor_pair_resolver_proved"
    ]
    assert not report.claim_gate["linear_width_overlap_controlled"]
    assert not report.claim_gate["hierarchical_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
