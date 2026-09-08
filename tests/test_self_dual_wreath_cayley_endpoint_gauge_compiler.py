from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_cayley_endpoint_gauge_compiler import (
    _abstract_controls,
    audit_cayley_endpoint,
    audit_cayley_scale_cancellation,
    audit_physical_cayley_endpoint,
    audit_recursive_gauge_covariance,
    audit_root_gauge_boundary,
    canonical_cayley_data,
    cayley_compiler_record,
    run_cayley_endpoint_gauge_compiler,
    write_cayley_endpoint_gauge_compiler_report,
)


def test_cayley_data_rejects_mismatched_or_singular_metrics() -> None:
    with pytest.raises(ValueError):
        canonical_cayley_data(np.eye(2), np.eye(3))
    with pytest.raises(ValueError):
        canonical_cayley_data(np.diag((1.0, 0.0)), np.eye(2))
    with pytest.raises(ValueError):
        canonical_cayley_data(np.diag((1.0, -0.1)), np.eye(2))


def test_canonical_endpoint_is_branch_gauge_of_cayley_naimark() -> None:
    left = np.asarray([[1.7, 0.2j], [-0.2j, 0.9]], dtype=complex)
    right = np.asarray([[0.8, 0.21], [0.21, 1.4]], dtype=complex)
    row = audit_cayley_endpoint("complex", left, right)

    assert row.exact_cayley_endpoint_gauge_theorem_verified
    assert row.cayley_contraction_norm < 1
    assert row.endpoint_gap > 0
    assert row.branch_effect_sum_residual < 1e-12
    assert row.canonical_endpoint_isometry_residual < 1e-12
    assert row.cayley_naimark_isometry_residual < 1e-12
    assert row.branch_gauge_reconstruction_residual < 1e-12
    assert row.branch_gauge_unitarity_residual < 1e-12


def test_graph_cayley_is_similar_but_not_equal_for_noncommuting_metrics() -> None:
    rows = {row.control_id: row for row in _abstract_controls()}

    assert rows["COMMUTING-DIAGONAL"].graph_to_canonical_cayley_operator_gap < 1e-12
    noncommuting = rows["NONCOMMUTING-ROTATED"]
    assert noncommuting.short_metric_commutator_norm > 0.01
    assert noncommuting.graph_to_canonical_cayley_operator_gap > 1e-3
    assert noncommuting.graph_cayley_similarity_residual < 1e-12
    assert noncommuting.graph_ratio_identity_residual < 1e-12


def test_common_scale_cancels_from_cayley_through_two_to_minus_48() -> None:
    rows = [audit_cayley_scale_cancellation(bits) for bits in (8, 16, 32, 48)]

    assert all(row.common_scale_cancels_exactly for row in rows)
    assert max(row.cayley_contraction_scale_residual for row in rows) < 1e-11
    assert max(row.cayley_naimark_projector_scale_residual for row in rows) < 1e-11
    assert rows[-1].separate_absolute_inverse_resolution_proxy == pytest.approx(2**48)


def test_physical_affine_sibling_has_exact_cayley_reduction() -> None:
    row = audit_physical_cayley_endpoint()

    assert row.exact_physical_cayley_reduction_verified
    assert row.child_width == 4
    assert row.physical_dimension == 8
    assert row.common_fiber_dimension == 5
    assert row.cayley_contraction_norm == pytest.approx(1 / 3)
    assert row.endpoint_gap == pytest.approx(1 / 3)
    assert row.relative_transfer_norm == pytest.approx(np.sqrt(5) / 2)
    assert row.maximum_exact_identity_residual < 1e-12


def test_matched_internal_gauges_telescope_across_tree() -> None:
    row = audit_recursive_gauge_covariance(tree_depth=4, fiber_dimension=3)

    assert row.exact_recursive_child_gauge_covariance_verified
    assert row.root_input_gauge_anchored
    assert row.internal_node_count == 15
    assert row.leaf_count == 16
    assert row.maximum_path_telescope_residual < 1e-12
    assert row.maximum_leaf_effect_residual < 1e-12


def test_unanchored_root_gauge_changes_the_povm() -> None:
    row = audit_root_gauge_boundary()

    assert row.exact_root_anchor_boundary_verified
    assert row.unanchored_root_branch_effect_gap > 0.1
    assert row.anchored_physical_endpoint_residual < 1e-12
    assert not row.internal_output_gauges_automatically_fix_root_input_gauge


@pytest.mark.parametrize("gap", [0.05, 0.1, 0.2, 0.3])
def test_conditional_cayley_compiler_avoids_transfer_polar_and_absolute_scale(
    gap: float,
) -> None:
    row = cayley_compiler_record(gap, requested_error=1e-7)

    assert row.conditional_cayley_naimark_compiler_polynomial
    assert row.qsvt_degree_upper_proxy > 0
    assert row.left_root_scalar_identity_residual < 1e-12
    assert row.right_root_scalar_identity_residual < 1e-12
    assert row.requires_normalization_one_cayley_block_encoding
    assert not row.requires_relative_transfer_polar
    assert not row.requires_absolute_short_metric_scale
    assert row.requires_root_coordinate_anchor
    assert not row.representation_specific_cayley_oracle_supplied_by_current_stack


def test_cayley_compiler_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError):
        cayley_compiler_record(0.0)
    with pytest.raises(ValueError):
        cayley_compiler_record(0.5)
    with pytest.raises(ValueError):
        cayley_compiler_record(0.1, requested_error=0.0)


def test_report_resolves_internal_gauge_but_not_normalized_oracle() -> None:
    report = run_cayley_endpoint_gauge_compiler()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["cayley_endpoint_effect_theorem_count"] == 1
    assert report.headline_metrics[
        "recursive_child_gauge_covariance_theorem_count"
    ] == 1
    assert report.headline_metrics["representation_specific_cayley_oracle_count"] == 0
    assert report.claim_gate["scale_free_canonical_cayley_contraction_proved"]
    assert report.claim_gate["recursive_child_output_gauges_telescope"]
    assert not report.claim_gate["root_input_gauge_can_be_ignored"]
    assert report.claim_gate["root_coordinate_anchor_required"]
    assert not report.claim_gate[
        "representation_specific_normalized_cayley_oracle_compiled"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_round_trip(tmp_path) -> None:
    path = tmp_path / "cayley-endpoint-gauge.json"
    payload = write_cayley_endpoint_gauge_compiler_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["status"] == (
        "cayley-endpoint-gauge-normal-form-proved-normalized-oracle-open"
    )
    assert all(row["url"].startswith("https://") for row in payload["primary_literature"])
