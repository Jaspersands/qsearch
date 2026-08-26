from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_positive_naimark_access_equivalence_boundary import (
    _component_system,
    audit_endpoint_positive_amplitudes,
    audit_pair_local_component_indeterminacy,
    audit_physical_component_positive_amplitudes,
    audit_scalar_address_extraction,
    component_positive_normal_form,
    endpoint_positive_normal_form,
    natural_positive_access_scaling_record,
    positive_access_interface_inventory,
    run_positive_naimark_access_equivalence_boundary,
    write_positive_naimark_access_equivalence_boundary_report,
)


def _control_system() -> tuple[tuple[np.ndarray, ...], np.ndarray]:
    return _component_system(
        731,
        physical_dimension=5,
        leaf_widths=(2, 2, 1, 2),
        common_dimension=3,
    )


def test_physical_component_effect_formula_and_restricted_polar_are_exact() -> None:
    leaves, common = _control_system()
    row = audit_physical_component_positive_amplitudes(
        "control",
        leaves,
        common,
    )

    assert row.exact_physical_positive_amplitude_equivalence_verified
    assert row.physical_dimension == 5
    assert row.common_fiber_dimension == 3
    assert row.leaf_count == 4
    assert row.active_component_count == 4
    assert row.child_frame_minimum_positive_eigenvalue > 0
    assert row.common_metric_minimum_eigenvalue > 0
    assert row.common_metric_embedding_isometry_residual < 1e-12
    assert row.restricted_polar_isometry_residual < 1e-12
    assert row.restricted_polar_factorization_residual < 1e-12
    assert row.maximum_physical_effect_formula_residual < 1e-12
    assert row.component_effect_sum_residual < 1e-12


def test_direct_component_naimark_and_restricted_polar_interconvert() -> None:
    leaves, common = _control_system()
    row = audit_physical_component_positive_amplitudes(
        "control",
        leaves,
        common,
    )

    assert row.canonical_naimark_isometry_residual < 1e-12
    assert row.maximum_component_polar_residual < 1e-12
    assert row.direct_naimark_to_restricted_polar_residual < 1e-12
    assert row.restricted_polar_to_direct_naimark_residual < 1e-12


def test_component_normal_form_exposes_global_whitening_factors() -> None:
    leaves, common = _control_system()
    data = component_positive_normal_form(leaves, common)

    assert data["frame"].shape == (5, 5)
    assert data["metric"].shape == (3, 3)
    assert data["orientation_polar"].shape == (7, 5)
    assert data["direct_embedding"].shape == (7, 3)
    assert data["canonical_naimark"].shape == (12, 3)
    assert len(data["effects"]) == 4
    assert np.linalg.norm(
        data["direct_embedding"] - data["gauge"] @ data["canonical_naimark"],
        ord=2,
    ) < 1e-12


def test_endpoint_short_metric_effect_and_naimark_gauge_are_exact() -> None:
    row = audit_endpoint_positive_amplitudes()

    assert row.exact_endpoint_positive_amplitude_equivalence_verified
    assert row.fiber_dimension == 3
    assert row.metric_commutator_norm > 0.2
    assert row.endpoint_effect_sum_residual < 1e-12
    assert row.endpoint_isometry_residual < 1e-12
    assert row.canonical_endpoint_naimark_isometry_residual < 1e-12
    assert row.maximum_endpoint_effect_formula_residual < 1e-12
    assert row.maximum_endpoint_polar_residual < 1e-12
    assert row.canonical_to_physical_endpoint_residual < 1e-12
    assert row.physical_to_canonical_endpoint_residual < 1e-12


def test_scalar_address_extraction_has_sharp_sqrt_active_width() -> None:
    leaves, common = _control_system()
    row = audit_scalar_address_extraction(leaves, common)

    assert row.exact_scalar_address_width_boundary_verified
    assert row.active_component_count == 4
    assert row.sharp_scalar_extraction_normalization == pytest.approx(2.0)
    assert row.uniform_address_probability == pytest.approx(0.25)
    assert row.extracted_success_probability == pytest.approx(0.25)
    assert row.matrix_naimark_success_probability == pytest.approx(1.0)
    assert row.uniform_selected_signal_norm == pytest.approx(0.5)
    assert row.uniform_selected_to_scaled_target_residual < 1e-12
    assert row.normalized_target_isometry_residual < 1e-12
    assert row.nonuniform_selected_to_any_equal_coefficient_residual > 0.1
    assert row.coefficient_only_normalization_lower_bound_saturated
    assert row.whitening_granted_for_free


def test_unqueried_leaf_changes_effect_while_selected_pair_data_stay_fixed() -> None:
    row = audit_pair_local_component_indeterminacy()

    assert row.exact_pair_local_indeterminacy_verified
    assert row.selected_leaf_projector_residual == pytest.approx(0.0)
    assert row.selected_pair_raw_cross_map_residual == pytest.approx(0.0)
    assert row.selected_pair_polar_residual == pytest.approx(0.0)
    assert row.frame_support_projector_residual < 1e-12
    assert row.unqueried_leaf_projector_distance == pytest.approx(1 / math.sqrt(2))
    assert row.first_selected_effect_spectrum[-1] == pytest.approx(0.5)
    assert row.second_selected_effect_spectrum[-1] == pytest.approx(0.75)
    assert row.selected_component_effect_operator_gap == pytest.approx(
        0.2873216088614294
    )
    assert not row.common_pair_local_data_determine_component_effect


def test_current_interface_inventory_has_no_compiled_positive_dilation() -> None:
    inventory = positive_access_interface_inventory()
    compiled_positive = [
        row
        for row in inventory
        if row.compiled and row.supplies_component_naimark_dilation
    ]
    direct = next(
        row
        for row in inventory
        if row.interface_id == "direct-component-square-root-naimark"
    )
    aggregate = next(
        row
        for row in inventory
        if row.interface_id == "aggregate-schur-racah-analysis"
    )

    assert compiled_positive == []
    assert direct.supplies_component_naimark_dilation
    assert direct.equivalent_to_restricted_polar_if_supplied
    assert not direct.compiled
    assert aggregate.supplies_global_child_whitening
    assert aggregate.equivalent_to_restricted_polar_if_supplied
    assert not aggregate.compiled


@pytest.mark.parametrize("n", [12, 16, 24, 32, 40, 48, 64, 80])
def test_natural_scaling_uses_width_not_a_small_positive_edge(n: int) -> None:
    row = natural_positive_access_scaling_record(n)

    assert row.group_order_decimal == str(math.factorial(n))
    assert row.orientation_leaf_count_decimal == str(1 << row.selected_copy_count)
    assert row.scalar_address_normalization_log2 == pytest.approx(
        row.early_child_active_component_count_log2 / 2
    )
    assert row.scalar_address_success_probability_log2 == (
        -row.early_child_active_component_count_log2
    )
    assert not row.small_positive_effect_edge_used
    assert not row.hierarchical_local_router_ruled_out
    assert not row.direct_schur_racah_naimark_ruled_out


def test_input_validation() -> None:
    leaves, common = _control_system()
    with pytest.raises(ValueError):
        component_positive_normal_form((), common)
    with pytest.raises(ValueError):
        component_positive_normal_form(leaves, np.eye(4))
    with pytest.raises(ValueError):
        endpoint_positive_normal_form(np.eye(2), np.eye(3))
    with pytest.raises(ValueError):
        endpoint_positive_normal_form(np.eye(2), np.diag((1.0, 0.0)))
    with pytest.raises(ValueError):
        natural_positive_access_scaling_record(2)


def test_report_closes_direct_positive_shortcut_but_preserves_structured_routes() -> None:
    report = run_positive_naimark_access_equivalence_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "physical_component_effect_formula_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "direct_naimark_restricted_polar_equivalence_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "scalar_address_sqrt_width_lower_bound_theorem_count"
    ] == 1
    assert report.headline_metrics["compiled_positive_amplitude_interface_count"] == 0
    assert report.headline_metrics["natural_small_positive_edge_theorem_count"] == 0
    assert report.claim_gate[
        "direct_component_naimark_is_restricted_polar_equivalent"
    ]
    assert not report.claim_gate["current_gpe_supplies_component_positive_dilation"]
    assert not report.claim_gate["hierarchical_normalization_one_router_ruled_out"]
    assert not report.claim_gate["direct_schur_racah_naimark_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert len(report.falsifiers_triggered) == 3


def test_report_writer_round_trip(tmp_path) -> None:
    path = tmp_path / "positive-naimark.json"
    payload = write_positive_naimark_access_equivalence_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["status"] == (
        "positive-naimark-access-equivalence-and-width-boundary-proved"
    )
