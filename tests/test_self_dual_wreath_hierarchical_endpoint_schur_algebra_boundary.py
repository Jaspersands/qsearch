from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_hierarchical_endpoint_schur_algebra_boundary import (
    _schur_control_system,
    audit_conditional_endpoint_compiler,
    audit_full_matrix_algebra_counterfamily,
    audit_operator_schur_endpoint,
    embedded_rational_schur_short,
    endpoint_access_interface_inventory,
    endpoint_from_short_metrics,
    full_algebra_generators,
    hierarchical_endpoint_scaling_record,
    operator_schur_short,
    run_hierarchical_endpoint_schur_algebra_boundary,
    write_hierarchical_endpoint_schur_algebra_boundary_report,
)


def _control() -> tuple[np.ndarray, np.ndarray, int]:
    left, right = _schur_control_system(
        401,
        internal_dimension=2,
        crossing_dimension=3,
    )
    return left, right, 2


def test_operator_schur_short_matches_embedded_rational_formula() -> None:
    left, _, internal = _control()
    direct = operator_schur_short(left, internal)
    rational = embedded_rational_schur_short(left, internal)

    assert direct.shape == (3, 3)
    assert np.linalg.norm(direct - rational, ord=2) < 1e-12
    assert np.linalg.eigvalsh(direct)[0] > 0


def test_operator_schur_endpoint_normal_form_is_exact_and_noncommuting() -> None:
    left, right, internal = _control()
    row = audit_operator_schur_endpoint(
        "control",
        left,
        right,
        internal,
    )

    assert row.exact_operator_schur_endpoint_normal_form_verified
    assert row.internal_dimension == 2
    assert row.crossing_dimension == 3
    assert row.full_kernel_dimension == 5
    assert row.maximum_direct_to_rational_short_residual < 1e-12
    assert row.short_metric_commutator_norm > 3
    assert row.endpoint_effect_sum_residual < 1e-12
    assert row.endpoint_isometry_residual < 1e-12
    assert row.endpoint_effect_minimum_eigenvalue > 0.1
    assert row.endpoint_complement_minimum_eigenvalue > 0.3


def test_binary_endpoint_rows_and_effects_sum_to_identity() -> None:
    left, right, internal = _control()
    left_short = operator_schur_short(left, internal)
    right_short = operator_schur_short(right, internal)
    data = endpoint_from_short_metrics(left_short, right_short)
    identity = np.eye(3)

    assert np.linalg.norm(
        data["endpoint"].conj().T @ data["endpoint"] - identity,
        ord=2,
    ) < 1e-12
    assert np.linalg.norm(data["effects"][0] + data["effects"][1] - identity, ord=2) < 1e-12


def test_conditional_endpoint_compiler_has_sqrt_condition_normalization() -> None:
    left, right, internal = _control()
    left_short = operator_schur_short(left, internal)
    right_short = operator_schur_short(right, internal)
    upper = max(
        np.linalg.eigvalsh(left_short)[-1],
        np.linalg.eigvalsh(right_short)[-1],
    )
    row = audit_conditional_endpoint_compiler(
        "control",
        left_short,
        right_short,
        supplied_normalization=1.25 * upper,
    )

    assert row.exact_conditional_endpoint_compiler_verified
    assert row.compiled_signal_normalization == pytest.approx(
        row.predicted_signal_normalization
    )
    assert row.predicted_signal_normalization == pytest.approx(
        math.sqrt(row.short_metric_upper_bound / row.short_metric_lower_bound)
    )
    assert row.compiled_to_scaled_endpoint_residual < 1e-12
    assert row.direct_endpoint_isometry_residual < 1e-12
    assert row.parent_inverse_root_contraction_norm <= 1
    assert row.maximum_child_root_contraction_norm <= 1 + 1e-12
    assert row.binary_stack_contraction_norm <= 1
    assert not row.postselection_required_after_amplification


def test_conditional_endpoint_edge_is_at_least_a_over_2b() -> None:
    left, right, internal = _control()
    row = audit_conditional_endpoint_compiler(
        "edge",
        operator_schur_short(left, internal),
        operator_schur_short(right, internal),
    )

    assert row.endpoint_effect_lower_bound == pytest.approx(
        row.short_metric_lower_bound / (2 * row.short_metric_upper_bound)
    )
    assert row.observed_endpoint_effect_minimum >= row.endpoint_effect_lower_bound
    assert row.observed_endpoint_complement_minimum >= row.endpoint_effect_lower_bound


@pytest.mark.parametrize("dimension", [2, 4, 8, 16])
def test_two_well_conditioned_generators_produce_full_matrix_algebra(
    dimension: int,
) -> None:
    row = audit_full_matrix_algebra_counterfamily(dimension)

    assert row.exact_full_matrix_algebra_counterfamily_verified
    assert row.generator_count == 2
    assert row.maximum_generator_condition_number <= 1.5 + 1e-12
    assert row.generator_commutator_norm > 0
    assert row.constructed_matrix_unit_count == dimension**2
    assert row.generated_algebra_dimension == dimension**2
    assert row.full_matrix_algebra_dimension == dimension**2
    assert row.maximum_matrix_unit_reconstruction_residual < 1e-12
    assert row.endpoint_two_sided_edge > 0.4
    assert not row.fixed_arity_well_conditioned_implies_small_algebra


def test_full_algebra_generators_have_the_promised_spectra() -> None:
    first, second = full_algebra_generators(8)

    assert np.linalg.eigvalsh(first)[0] == pytest.approx(1.0)
    assert np.linalg.eigvalsh(first)[-1] == pytest.approx(1.5)
    assert np.linalg.eigvalsh(second)[0] == pytest.approx(1.0)
    assert np.linalg.eigvalsh(second)[-1] == pytest.approx(1.4)


def test_interface_inventory_isolates_the_missing_aggregate_metric_oracle() -> None:
    inventory = endpoint_access_interface_inventory()
    aggregate = next(
        row
        for row in inventory
        if row.interface_id == "aggregate-short-metric-block-encoding"
    )
    direct = next(
        row
        for row in inventory
        if row.interface_id == "direct-local-schur-racah-naimark"
    )
    current = [row for row in inventory if row.compiled]

    assert all(
        not row.supplies_aggregate_short_metric_block_encoding
        for row in current
    )
    assert aggregate.supplies_aggregate_short_metric_block_encoding
    assert aggregate.compiles_binary_endpoint_given_contract
    assert not aggregate.compiled
    assert direct.compiles_binary_endpoint_given_contract
    assert not direct.compiled
    assert not direct.supplies_aggregate_short_metric_block_encoding


@pytest.mark.parametrize("n", [12, 16, 24, 32, 40, 48, 64, 80])
def test_natural_scaling_keeps_binary_compiler_conditional(n: int) -> None:
    row = hierarchical_endpoint_scaling_record(n)

    assert row.group_order_decimal == str(math.factorial(n))
    assert row.orientation_leaf_count_decimal == str(1 << row.selected_copy_count)
    assert row.binary_tree_depth == row.selected_copy_count
    assert row.canonical_uniform_frame_normalization_log2 == (
        row.early_child_leaf_width_log2
    )
    assert row.conditional_endpoint_signal_normalization == pytest.approx(10.0)
    assert row.per_level_operator_error_budget == pytest.approx(
        0.01 / row.binary_tree_depth
    )
    assert not row.compact_aggregate_metric_oracle_proved
    assert not row.all_depth_parent_trim_recurrence_proved
    assert row.conditional_binary_compiler_polynomial_given_metric_oracles
    assert not row.direct_schur_racah_naimark_ruled_out


def test_input_validation() -> None:
    left, right, internal = _control()
    with pytest.raises(ValueError):
        operator_schur_short(left, left.shape[0])
    with pytest.raises(ValueError):
        endpoint_from_short_metrics(np.eye(2), np.eye(3))
    with pytest.raises(ValueError):
        audit_conditional_endpoint_compiler(
            "bad-normalization",
            operator_schur_short(left, internal),
            operator_schur_short(right, internal),
            supplied_normalization=0.1,
        )
    with pytest.raises(ValueError):
        full_algebra_generators(1)
    with pytest.raises(ValueError):
        hierarchical_endpoint_scaling_record(2)


def test_report_proves_conditional_compiler_and_refutes_small_algebra_shortcut() -> None:
    report = run_hierarchical_endpoint_schur_algebra_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "operator_valued_schur_short_normal_form_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "conditional_binary_endpoint_block_compiler_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "fixed_arity_small_algebra_implication_refutation_count"
    ] == 1
    assert report.headline_metrics["largest_full_algebra_dimension"] == 256
    assert report.headline_metrics[
        "compiled_aggregate_short_metric_interface_count"
    ] == 0
    assert report.claim_gate[
        "binary_endpoint_compiles_given_aggregate_metric_block_encodings"
    ]
    assert not report.claim_gate[
        "fixed_arity_and_conditioning_imply_poly_dimensional_endpoint_algebra"
    ]
    assert not report.claim_gate[
        "full_matrix_algebra_dimension_is_quantum_circuit_lower_bound"
    ]
    assert not report.claim_gate["all_depth_native_mass_recurrence_proved"]
    assert not report.claim_gate["direct_local_schur_racah_naimark_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert len(report.falsifiers_triggered) == 3


def test_report_writer_round_trip(tmp_path) -> None:
    path = tmp_path / "hierarchical-endpoint.json"
    payload = write_hierarchical_endpoint_schur_algebra_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["status"] == (
        "hierarchical-endpoint-schur-compiler-reduction-and-full-algebra-boundary-proved"
    )
