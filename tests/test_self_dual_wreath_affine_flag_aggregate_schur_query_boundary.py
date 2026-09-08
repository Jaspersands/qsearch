from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_affine_flag_aggregate_schur_query_boundary import (
    _aggregate_search_kernel,
    _local_search_kernel,
    _positive_kernel_controls,
    affine_flag_aggregate_scaling_record,
    affine_flag_label,
    aggregate_schur_interface_inventory,
    audit_addressed_aggregate_search_reduction,
    audit_affine_flag_labeler,
    binary_rank,
    psd_schur_short,
    run_affine_flag_aggregate_schur_query_boundary,
    write_affine_flag_aggregate_schur_query_boundary_report,
)


def test_binary_rank_and_flag_labels_are_bijective() -> None:
    basis = (1, 3, 6, 12, 24)
    labels = {affine_flag_label(address, basis) for address in range(32)}

    assert binary_rank(basis) == 5
    assert len(labels) == 32


@pytest.mark.parametrize(
    ("control_id", "basis"),
    [
        ("standard", (1, 2, 4, 8, 16)),
        ("nonsystematic", (1, 3, 6, 12, 24)),
    ],
)
def test_affine_flag_labeler_is_table_free_and_classifies_crossings(
    control_id: str,
    basis: tuple[int, ...],
) -> None:
    row = audit_affine_flag_labeler(control_id, 5, basis)

    assert row.reversible_label_bijection_verified
    assert row.internal_crossing_classification_verified
    assert row.binary_rank == 5
    assert row.label_count == 32
    assert row.full_tree_node_count == 63
    assert row.audited_incident_pair_count > 0
    assert row.maximum_forward_cnot_count <= 25
    assert row.membership_workspace_bit_count == 5
    assert row.leaf_table_entry_count == 0


def test_affine_flag_labeler_rejects_invalid_basis() -> None:
    with pytest.raises(ValueError):
        audit_affine_flag_labeler("bad", 3, (1, 2))
    with pytest.raises(ValueError):
        audit_affine_flag_labeler("bad", 3, (1, 2, 8))


def test_local_kernel_has_prescribed_schur_short() -> None:
    for short_value in (0.05, 0.4, 1.2):
        kernel = _local_search_kernel(short_value, 0.31)
        short, range_residual = psd_schur_short(kernel, 1)

        assert range_residual < 1e-12
        assert short[0, 0].real == pytest.approx(short_value)
        assert np.linalg.eigvalsh(kernel)[0] > 0


def test_aggregate_kernel_short_is_sum_of_local_shorts() -> None:
    values = np.asarray([0.1, 0.2, 0.3, 0.4])
    kernel = _aggregate_search_kernel(values, 0.27)
    short, range_residual = psd_schur_short(kernel, len(values))

    assert range_residual < 1e-12
    assert short.shape == (1, 1)
    assert short[0, 0].real == pytest.approx(values.sum())


def test_psd_schur_short_rejects_invalid_elimination() -> None:
    with pytest.raises(ValueError):
        psd_schur_short(np.eye(2), 2)
    with pytest.raises(ValueError):
        psd_schur_short(np.ones((2, 3)), 1)


def test_nested_schur_short_is_associative_in_both_orders() -> None:
    controls = _positive_kernel_controls()

    assert len(controls) == 2
    assert all(row.exact_nested_schur_short_verified for row in controls)
    assert max(
        max(row.forward_composition_residual, row.reverse_composition_residual)
        for row in controls
    ) < 1e-12
    assert controls[1].singular_first_internal_block
    assert controls[1].kernel_rank < controls[1].total_dimension


@pytest.mark.parametrize("bit_count", [2, 3, 4, 5])
def test_addressed_aggregate_endpoint_embeds_search_with_constant_gap(
    bit_count: int,
) -> None:
    row = audit_addressed_aggregate_search_reduction(
        f"q{1 << bit_count}",
        bit_count,
    )

    assert row.exact_search_reduction_verified
    assert row.address_count == 1 << bit_count
    assert row.no_mark_aggregate_short == pytest.approx(1.0)
    assert row.one_mark_aggregate_short == pytest.approx(2.0)
    assert row.maximum_aggregate_short_residual < 1e-12
    assert row.no_mark_left_endpoint_probability == pytest.approx(0.5)
    assert row.one_mark_left_endpoint_probability == pytest.approx(2 / 3)
    assert row.endpoint_probability_gap == pytest.approx(1 / 6)
    assert row.endpoint_isometry_operator_gap > 0.16
    assert row.robust_probability_gap_lower_bound > 0.1
    assert row.minimum_endpoint_two_sided_edge == pytest.approx(1 / 3)
    assert row.aggregate_metric_condition_number == 1
    assert row.native_retained_mass == 1
    assert row.addressed_kernel_query_equivalent_to_search_bit_query
    assert row.bounded_error_query_lower_bound == "Omega(sqrt(q))"


def test_canonical_sum_normalization_grows_with_address_count() -> None:
    small = audit_addressed_aggregate_search_reduction("small", 3)
    large = audit_addressed_aggregate_search_reduction("large", 5)

    assert large.canonical_sum_block_encoding_normalization > 3 * (
        small.canonical_sum_block_encoding_normalization
    )
    assert large.maximum_local_kernel_norm < 3


def test_interface_inventory_separates_labels_from_metric_responses() -> None:
    rows = {row.interface_id: row for row in aggregate_schur_interface_inventory()}

    labels = rows["AFFINE-FLAG-NODE-LABEL"]
    addressed = rows["ADDRESSED-LOCAL-KERNEL-QUERY"]
    response = rows["STRUCTURED-RACAH-RESPONSE-ORACLE"]
    mass = rows["ALL-DEPTH-NATIVE-MASS-RECURRENCE"]

    assert labels.supplied_by_current_stack
    assert not labels.sufficient_for_endpoint_compiler
    assert addressed.supplied_by_current_stack
    assert not addressed.sufficient_for_endpoint_compiler
    assert response.sufficient_for_endpoint_compiler
    assert not response.supplied_by_current_stack
    assert mass.sufficient_for_endpoint_compiler
    assert not mass.supplied_by_current_stack


@pytest.mark.parametrize("bit_count", [8, 16, 24, 32, 48, 64])
def test_scaling_separates_polynomial_label_cost_from_search_query_cost(
    bit_count: int,
) -> None:
    row = affine_flag_aggregate_scaling_record(bit_count)

    assert row.address_count == 1 << bit_count
    assert row.reversible_label_gate_upper_bound == bit_count**2
    assert row.reversible_label_workspace_upper_bound == bit_count
    assert row.search_query_lower_bound_log2 == pytest.approx(bit_count / 2)
    assert row.search_query_lower_bound_proxy == pytest.approx(
        math.sqrt(1 << bit_count)
    )
    assert not row.polynomial_in_address_bit_count
    assert not row.natural_schur_racah_realizability_proved


def test_report_closes_generic_addressed_aggregation_but_preserves_racah_route() -> None:
    report = run_affine_flag_aggregate_schur_query_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "reversible_affine_flag_node_labeler_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "nested_psd_schur_short_associativity_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "addressed_local_kernel_aggregate_search_lower_bound_theorem_count"
    ] == 1
    assert report.claim_gate["reversible_affine_flag_node_labeler_compiled"]
    assert report.claim_gate["nested_psd_schur_short_associativity_proved"]
    assert report.claim_gate[
        "addressed_aggregate_endpoint_query_lower_bound_sqrt_q"
    ]
    assert not report.claim_gate["affine_labels_determine_metric_amplitudes"]
    assert not report.claim_gate[
        "addressed_local_kernel_queries_compile_aggregate_short_in_polylog_q"
    ]
    assert not report.claim_gate["structured_racah_response_oracle_compiled"]
    assert not report.claim_gate["direct_local_schur_racah_naimark_ruled_out"]
    assert not report.claim_gate[
        "all_depth_parent_compatible_native_mass_recurrence_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert len(report.falsifiers_triggered) == 3


def test_report_writer_round_trip(tmp_path) -> None:
    path = tmp_path / "affine-flag-aggregate-schur.json"
    payload = write_affine_flag_aggregate_schur_query_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["primary_literature"][
        "quantum_unstructured_search_lower_bound"
    ].endswith("quant-ph/9701001")
    assert payload["status"] == (
        "affine-label-and-schur-recursion-proved-addressed-aggregate-query-boundary"
    )
