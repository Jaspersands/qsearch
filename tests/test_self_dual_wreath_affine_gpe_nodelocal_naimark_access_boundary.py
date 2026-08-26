from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_affine_gpe_nodelocal_naimark_access_boundary import (
    _flat_components,
    _matrix_components,
    _selected_parameters,
    audit_affine_transport_circuit,
    audit_endpoint_scalar_access,
    audit_metric_blind_transport_indeterminacy,
    audit_nested_naimark_circuit,
    audit_parent_trim_propagation,
    audit_scalar_prepare_select,
    companion_natural_matrix_support_record,
    natural_nodelocal_naimark_scaling_record,
    run_affine_gpe_nodelocal_naimark_access_boundary,
    write_affine_gpe_nodelocal_naimark_access_boundary_report,
)


def test_scalar_prepare_select_exactly_compiles_flat_full_fiber_effects() -> None:
    row = audit_scalar_prepare_select(
        "flat",
        _flat_components(),
        (0.5, 0.5),
    )

    assert row.exact_scalar_prepare_select_criterion_verified
    assert row.scalar_prepare_select_compiles_target
    assert row.every_effect_scalar_on_its_support_with_selected_probability
    assert row.outcome_support_ranks == (2, 2)
    assert row.target_component_effect_sum_residual < 1e-12
    assert row.target_embedding_isometry_residual < 1e-12
    assert row.scalar_prepare_select_isometry_residual < 1e-12
    assert row.maximum_scalar_on_support_effect_residual < 1e-12
    assert row.target_to_scalar_prepare_select_operator_error < 1e-12


def test_scalar_prepare_select_does_not_compile_matrix_component_effects() -> None:
    row = audit_scalar_prepare_select(
        "matrix",
        _matrix_components(),
        (0.5, 0.5),
    )

    assert row.exact_scalar_prepare_select_criterion_verified
    assert not row.scalar_prepare_select_compiles_target
    assert not row.every_effect_scalar_on_its_support_with_selected_probability
    assert row.target_embedding_isometry_residual < 1e-12
    assert row.scalar_prepare_select_isometry_residual < 1e-12
    assert row.maximum_scalar_on_support_effect_residual == pytest.approx(0.25)
    assert row.target_to_scalar_prepare_select_operator_error == pytest.approx(
        0.26105238444010315
    )


def test_affine_hadamards_and_generator_transports_have_normalization_one() -> None:
    row = audit_affine_transport_circuit()

    assert row.exact_normalization_one_affine_transport_circuit_verified
    assert row.active_masks == (1, 3, 8, 10)
    assert row.orientation_label_bit_count == 4
    assert row.affine_address_qubit_count == 2
    assert row.controlled_generator_transport_stage_count == 2
    assert row.hadamard_layer_count == 1
    assert row.path_workspace_uncomputed
    assert row.output_address_retained
    assert not row.postselection_required
    assert row.block_encoding_normalization == pytest.approx(1.0)
    assert row.direct_to_compiled_operator_residual < 1e-12
    assert row.compiled_isometry_residual < 1e-12


def test_equal_short_metrics_give_scalar_hadamard_endpoint() -> None:
    identity = np.eye(2, dtype=complex)
    row = audit_endpoint_scalar_access("equal", identity, identity)

    assert row.exact_endpoint_scalar_criterion_verified
    assert row.proportional_metrics
    assert row.scalar_endpoint_prepare_compiles_target
    assert row.best_scalar_left_probability == pytest.approx(0.5)
    assert row.endpoint_effect_minimum_eigenvalue == pytest.approx(0.5)
    assert row.endpoint_effect_maximum_eigenvalue == pytest.approx(0.5)
    assert row.best_scalar_effect_residual < 1e-12
    assert row.target_to_best_scalar_endpoint_operator_error < 1e-12
    assert row.endpoint_column_isometry_residual < 1e-12


def test_nonproportional_short_metrics_require_matrix_endpoint_dilation() -> None:
    row = audit_endpoint_scalar_access(
        "matrix",
        np.diag((1.0, 4.0)),
        np.diag((4.0, 1.0)),
    )

    assert row.exact_endpoint_scalar_criterion_verified
    assert not row.proportional_metrics
    assert not row.scalar_endpoint_prepare_compiles_target
    assert row.endpoint_effect_minimum_eigenvalue == pytest.approx(0.2)
    assert row.endpoint_effect_maximum_eigenvalue == pytest.approx(0.8)
    assert row.best_scalar_left_probability == pytest.approx(0.5)
    assert row.best_scalar_effect_residual == pytest.approx(0.3)
    assert row.target_to_best_scalar_endpoint_operator_error == pytest.approx(
        0.3203644860139346
    )


def test_gpe_support_polar_transport_oracles_do_not_determine_endpoint_metric() -> None:
    row = audit_metric_blind_transport_indeterminacy()

    assert row.exact_metric_blind_indeterminacy_verified
    assert row.maximum_child_support_projector_residual == pytest.approx(0.0)
    assert row.maximum_child_polar_residual == pytest.approx(0.0)
    assert row.maximum_pair_transport_residual == pytest.approx(0.0)
    assert row.endpoint_target_operator_gap == pytest.approx(0.32036448601393447)
    assert row.common_transport_only_worst_instance_error_lower_bound == pytest.approx(
        row.endpoint_target_operator_gap / 2
    )
    assert not row.support_polar_transport_oracles_determine_endpoint_mixer


def test_nested_positive_dilations_and_gpe_select_compose_at_normalization_one() -> None:
    row = audit_nested_naimark_circuit()

    assert row.exact_normalization_one_nested_naimark_contract_verified
    assert row.left_component_count == 3
    assert row.right_component_count == 2
    assert row.endpoint_effect_sum_residual < 1e-12
    assert row.maximum_child_effect_sum_residual < 1e-12
    assert row.direct_relation_isometry_residual < 1e-12
    assert row.nested_naimark_to_direct_relation_residual < 1e-12
    assert row.endpoint_dilation_call_count == 1
    assert row.component_dilation_call_count == 1
    assert row.controlled_gpe_partial_isometry_select_count == 1
    assert row.path_uncompute_call_count == 1
    assert row.block_encoding_normalization == pytest.approx(1.0)
    assert not row.postselection_required
    assert not row.endpoint_metric_dilation_supplied_by_current_gpe_transport_interface
    assert not row.component_effect_dilation_supplied_by_current_gpe_transport_interface
    assert "epsilon_endpoint" in row.error_recurrence
    assert "workspace_component" in row.workspace_recurrence


def test_independent_component_trims_destroy_parent_povm_sum() -> None:
    row = audit_parent_trim_propagation()

    assert row.exact_parent_trim_propagation_boundary_verified
    assert row.untrimmed_effect_sum_residual == pytest.approx(0.0)
    assert row.common_parent_projection_effect_sum_residual == pytest.approx(0.0)
    assert row.independently_trimmed_effect_sum_residual == pytest.approx(0.4)
    assert row.independently_trimmed_dilation_isometry_residual == pytest.approx(0.4)
    assert row.minimum_independently_retained_effect_eigenvalue == pytest.approx(0.6)
    assert row.independently_retained_components_well_conditioned
    assert not row.independent_component_trims_preserve_parent_povm


def test_companion_natural_affine_node_requires_matrix_partial_support() -> None:
    row = companion_natural_matrix_support_record()

    assert row.n == 6
    assert row.active_support_is_affine
    assert row.globally_distinct_sources
    assert not row.scalar_flat_affine_child_embedding_certificate
    assert row.matrix_partial_support_required
    assert row.maximum_component_full_fiber_scalar_residual > 0.7
    assert row.maximum_cross_child_effect_commutator_norm > 1e-3
    assert not row.direct_finite_source_mechanism_has_positive_asymptotic_native_mass
    assert row.universal_scalar_affine_natural_node_compiler_falsified


@pytest.mark.parametrize("n", [8, 16, 24, 32, 40, 48])
def test_natural_scaling_keeps_nested_normalization_one_but_oracles_open(
    n: int,
) -> None:
    row = natural_nodelocal_naimark_scaling_record(n)
    order, selected, address = _selected_parameters(n)

    assert row.group_order_decimal == str(order)
    assert row.selected_copy_count == selected
    assert row.maximum_orientation_address_qubits == address
    assert row.maximum_affine_transport_stages == address
    assert row.conditional_nested_dilation_normalization == pytest.approx(1.0)
    assert not row.all_n_compact_component_effect_description_proved
    assert not row.polynomial_uniform_component_effect_dilation_proved
    assert not row.polynomial_uniform_endpoint_metric_dilation_proved
    assert not row.all_n_component_support_gpe_select_proved
    assert not row.parent_trim_propagation_compiled
    assert not row.recursive_orientation_polar_compiled


def test_input_validation() -> None:
    with pytest.raises(ValueError):
        audit_scalar_prepare_select("empty", (), ())
    with pytest.raises(ValueError):
        audit_scalar_prepare_select("probability", _flat_components(), (0.4, 0.4))
    with pytest.raises(ValueError):
        audit_scalar_prepare_select("negative", _flat_components(), (-0.1, 1.1))
    with pytest.raises(ValueError):
        audit_endpoint_scalar_access("shape", np.eye(2), np.eye(3))
    with pytest.raises(ValueError):
        audit_endpoint_scalar_access("singular", np.eye(2), np.diag((1.0, 0.0)))
    with pytest.raises(ValueError):
        audit_parent_trim_propagation(trim_threshold=0.0)
    with pytest.raises(ValueError):
        natural_nodelocal_naimark_scaling_record(2)


def test_report_rejects_scalar_gpe_route_but_preserves_matrix_naimark_route() -> None:
    report = run_affine_gpe_nodelocal_naimark_access_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "scalar_prepare_select_effect_criterion_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "normalization_one_nested_naimark_contract_theorem_count"
    ] == 1
    assert report.claim_gate[
        "flat_affine_gpe_transport_embedding_compiles_at_normalization_one"
    ]
    assert not report.claim_gate[
        "scalar_prepare_select_compiles_matrix_component_povm"
    ]
    assert not report.claim_gate[
        "support_polar_gpe_transport_oracles_determine_endpoint_mixer"
    ]
    assert report.claim_gate["normalization_one_nested_naimark_contract_proved"]
    assert not report.claim_gate["nested_naimark_requires_postselection"]
    assert not report.claim_gate["typical_natural_matrix_partial_support_obstruction_proved"]
    assert not report.claim_gate["uniform_endpoint_metric_naimark_dilation_compiled"]
    assert not report.claim_gate["uniform_component_effect_naimark_dilation_compiled"]
    assert not report.claim_gate["arbitrary_structured_local_router_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "nodelocal-naimark.json"
    payload = write_affine_gpe_nodelocal_naimark_access_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["status"] == (
        "affine-gpe-transports-compile-flat-fibers-matrix-naimark-dilations-open"
    )
    assert payload["headline_metrics"]["finite_control_failure_count"] == 0

