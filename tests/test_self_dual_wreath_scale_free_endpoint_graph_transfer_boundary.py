from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_scale_free_endpoint_graph_transfer_boundary import (
    _abstract_controls,
    audit_common_scale_cancellation,
    audit_physical_affine_graph_reduction,
    audit_response_short_graph_duality,
    audit_support_blind_transfer_counterexample,
    endpoint_graph_data,
    relative_transfer_compiler_record,
    run_scale_free_endpoint_graph_transfer_boundary,
    write_scale_free_endpoint_graph_transfer_boundary_report,
)


def test_endpoint_graph_data_rejects_nonpositive_or_mismatched_metrics() -> None:
    with pytest.raises(ValueError):
        endpoint_graph_data(np.eye(2), np.eye(3))
    with pytest.raises(ValueError):
        endpoint_graph_data(np.diag((1.0, 0.0)), np.eye(2))
    with pytest.raises(ValueError):
        endpoint_graph_data(np.diag((1.0, -0.1)), np.eye(2))


def test_response_and_short_endpoints_are_exact_complementary_columns() -> None:
    left = np.asarray([[1.7, 0.2j], [-0.2j, 0.9]], dtype=complex)
    right = np.asarray([[0.8, 0.21], [0.21, 1.4]], dtype=complex)
    row = audit_response_short_graph_duality("complex", left, right)

    assert row.exact_response_short_graph_duality_verified
    assert row.short_endpoint_isometry_residual < 1e-12
    assert row.response_relation_isometry_residual < 1e-12
    assert row.endpoint_relation_orthogonality_residual < 1e-12
    assert row.dual_unitary_residual < 1e-12


def test_relative_graph_cs_unitary_matches_endpoint_and_relation_subspaces() -> None:
    left = np.diag((0.7, 1.3, 2.1)).astype(complex)
    angle = 0.43
    rotation = np.asarray(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
        dtype=complex,
    )
    right = np.eye(3, dtype=complex)
    right[:2, :2] = rotation @ np.diag((0.9, 1.8)) @ rotation.conj().T
    row = audit_response_short_graph_duality("noncommuting", left, right)

    assert row.exact_response_short_graph_duality_verified
    assert row.short_metric_commutator_norm > 0.01
    assert row.graph_cs_unitary_residual < 1e-12
    assert row.graph_to_short_endpoint_gauge_residual < 1e-12
    assert row.graph_complement_to_response_gauge_residual < 1e-12
    assert row.short_endpoint_gauge_unitarity_residual < 1e-12
    assert row.response_relation_gauge_unitarity_residual < 1e-12
    assert row.positive_root_graph_column_operator_gap > 1e-4


def test_commuting_metrics_have_trivial_positive_root_graph_gauge() -> None:
    rows = {row.control_id: row for row in _abstract_controls()}

    assert rows["COMMUTING-DIAGONAL"].positive_root_graph_column_operator_gap < 1e-12
    assert rows["NONCOMMUTING-ROTATED"].positive_root_graph_column_operator_gap > 1e-3
    assert rows["RANDOM-COMPLEX-D4"].positive_root_graph_column_operator_gap > 1e-3


def test_common_exponential_scale_cancels_but_absolute_inverse_does_not() -> None:
    rows = [audit_common_scale_cancellation(bits) for bits in (8, 16, 32, 48)]

    assert all(row.common_scale_cancels_from_relative_graph_exactly for row in rows)
    assert max(row.relative_transfer_residual for row in rows) < 1e-12
    assert max(row.graph_projector_scale_residual for row in rows) < 1e-12
    assert rows[-1].separate_absolute_inverse_resolution_proxy == pytest.approx(2**48)
    assert rows[-1].separate_absolute_inverse_resolution_proxy > 10**14


def test_physical_affine_node_has_exact_shorted_graph_reduction() -> None:
    row = audit_physical_affine_graph_reduction()

    assert row.exact_physical_affine_graph_reduction_verified
    assert row.child_width == 4
    assert row.common_fiber_dimension == 5
    assert row.physical_short_formula_residual < 1e-12
    assert row.graph_cs_unitary_residual < 1e-12
    assert 1.0 < row.relative_transfer_norm < 2.0
    assert 1.0 < row.relative_transfer_inverse_norm < 2.0


def test_support_pair_polars_do_not_determine_positive_relative_transfer() -> None:
    row = audit_support_blind_transfer_counterexample()

    assert row.exact_metric_blind_counterexample_verified
    assert row.maximum_support_projector_gap == 0
    assert row.maximum_support_polar_transport_gap == 0
    assert row.relative_transfer_operator_gap > 0.5
    assert row.graph_endpoint_projector_gap > 0.2
    assert not row.support_pair_polars_determine_relative_transfer


@pytest.mark.parametrize("bound", [1.0, 2.0, 4.0, 8.0, 16.0])
def test_conditional_graph_compiler_needs_no_lower_singular_cutoff(bound: float) -> None:
    row = relative_transfer_compiler_record(bound, requested_error=1e-7)

    assert row.scalar_rotation_identity_residual < 1e-12
    assert row.cosine_function_maximum == pytest.approx(1.0)
    assert row.sine_function_maximum < 1.0
    assert row.conditional_graph_cs_compiler_polynomial
    assert not row.requires_lower_singular_value_bound
    assert not row.requires_absolute_child_frame_scale
    assert row.requires_relative_transfer_block_encoding
    assert not row.relative_transfer_block_encoding_supplied_by_current_stack


def test_compiler_record_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError):
        relative_transfer_compiler_record(0.5)
    with pytest.raises(ValueError):
        relative_transfer_compiler_record(2.0, 0.0)


def test_report_narrows_the_open_oracle_without_claiming_speedup() -> None:
    report = run_scale_free_endpoint_graph_transfer_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "response_short_complementarity_theorem_count"
    ] == 1
    assert report.headline_metrics["relative_graph_cs_normal_form_theorem_count"] == 1
    assert report.headline_metrics["common_scale_cancellation_theorem_count"] == 1
    assert report.headline_metrics[
        "conditional_relative_transfer_compiler_theorem_count"
    ] == 1
    assert report.headline_metrics["compiled_representation_relative_transfer_oracle_count"] == 0
    assert report.claim_gate["scale_free_relative_graph_cs_normal_form_proved"]
    assert report.claim_gate[
        "conditional_qsvt_graph_cs_compiler_given_relative_transfer"
    ]
    assert not report.claim_gate["support_pair_polars_determine_positive_relative_transfer"]
    assert not report.claim_gate["representation_specific_relative_transfer_oracle_compiled"]
    assert not report.claim_gate["recursive_endpoint_gauge_covariance_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_round_trip(tmp_path) -> None:
    path = tmp_path / "scale-free-graph-transfer.json"
    payload = write_scale_free_endpoint_graph_transfer_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["status"] == (
        "scale-free-relative-graph-endpoint-exact-access-oracle-open"
    )
    assert all(row["url"].startswith("https://") for row in payload["primary_literature"])
