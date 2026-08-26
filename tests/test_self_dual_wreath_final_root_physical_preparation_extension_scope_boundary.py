from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_final_root_physical_preparation_extension_scope_boundary import (
    _cyclic_branch_representation_rows,
    _fourier_unitary,
    _rotated_effect,
    _uniform_preparation_extensions,
    audit_endpoint_byproduct_branch_separation,
    audit_full_row_copy_unitary,
    full_generalized_row_copy_unitary,
    physical_preparation_interface_inventory,
    physical_preparation_scaling_record,
    run_final_root_physical_preparation_extension_scope_boundary,
    write_final_root_physical_preparation_extension_scope_boundary_report,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    weyl_unitary_error_basis,
)


@pytest.mark.parametrize(
    ("group_dimension", "logical_dimension"),
    [(2, 2), (3, 2), (3, 3), (4, 3), (5, 4)],
)
def test_full_row_copy_unitary_and_every_ancilla_block_are_branch_preserving(
    group_dimension: int,
    logical_dimension: int,
) -> None:
    row = audit_full_row_copy_unitary(
        f"g{group_dimension}-d{logical_dimension}",
        group_dimension,
        logical_dimension,
    )

    assert row.exact_full_row_copy_extension_scope_verified
    assert row.maximum_full_row_copy_unitarity_residual < 1e-10
    assert row.maximum_seeded_row_copy_isometry_residual < 1e-10
    assert row.seeded_row_copy_extension_invariance_residual < 1e-10
    assert row.maximum_full_unitary_branch_commutator_norm < 1e-10
    assert row.maximum_selected_ancilla_block_branch_commutator_norm < 1e-10
    assert row.maximum_composed_stack_branch_commutator_norm < 1e-10
    assert row.uniform_preparation_extension_distance > 0.1
    assert row.every_nonprogram_ancilla_block_branch_preserving


def test_inequivalent_uniform_preparation_extensions_have_same_seed_column() -> None:
    group_dimension = 4
    logical_dimension = 3
    rows = _cyclic_branch_representation_rows(group_dimension, logical_dimension)
    preparation_zero, preparation_one = _uniform_preparation_extensions(group_dimension)
    row_zero = full_generalized_row_copy_unitary(rows, preparation_zero)
    row_one = full_generalized_row_copy_unitary(rows, preparation_one)
    seed = np.zeros(group_dimension, dtype=complex)
    seed[0] = 1.0
    embedding = np.kron(seed[:, None], np.eye(2 * logical_dimension))

    assert np.linalg.norm(preparation_zero - preparation_one, ord=2) > 0.1
    assert np.linalg.norm(row_zero @ embedding - row_one @ embedding, ord=2) < 1e-10
    assert np.linalg.norm(row_zero - row_one, ord=2) > 0.1


@pytest.mark.parametrize("dimension", [2, 3, 4])
@pytest.mark.parametrize("error_index", [1, "shift"])
def test_endpoint_weyl_byproduct_is_uniformly_outside_branch_algebra(
    dimension: int,
    error_index: int | str,
) -> None:
    effect = _rotated_effect(dimension)
    errors = weyl_unitary_error_basis(dimension)
    error = errors[dimension] if error_index == "shift" else errors[error_index]
    row = audit_endpoint_byproduct_branch_separation(
        f"d{dimension}-{error_index}",
        effect,
        error,
    )

    assert row.exact_branch_separation_verified
    assert row.endpoint_isometry_residual < 1e-10
    assert row.byproduct_operator_norm == pytest.approx(1.0)
    assert row.left_to_right_block_minimum_singular_value >= (
        row.strict_effect_window_delta - 1e-10
    )
    assert row.certified_distance_from_branch_preserving_algebra >= (
        row.strict_effect_window_delta - 1e-10
    )
    assert not row.row_copy_selected_block_can_equal_byproduct


def test_diagonal_effect_has_same_strict_window_separation() -> None:
    effect = np.diag([0.25, 0.5, 0.75]).astype(complex)
    shift = weyl_unitary_error_basis(3)[3]
    row = audit_endpoint_byproduct_branch_separation("diagonal", effect, shift)

    assert row.exact_branch_separation_verified
    assert row.strict_effect_window_delta == pytest.approx(0.25)
    assert row.left_to_right_block_minimum_singular_value >= 0.25 - 1e-10


def test_interface_inventory_finds_cross_maps_but_no_full_endpoint_preparation() -> None:
    inventory = physical_preparation_interface_inventory()
    by_id = {row.primitive_id: row for row in inventory}

    assert len(inventory) == 8
    assert by_id["generalized-fourier-row-copy"].full_domain_unitary_or_block_encoding_specified
    assert by_id["generalized-fourier-row-copy"].branch_preserving_by_typed_interface
    assert not by_id["generalized-fourier-row-copy"].supplies_endpoint_program_column
    assert by_id["addressed-physical-cross-map"].supplies_addressed_cross_branch_signal
    assert by_id["addressed-physical-cross-map"].compiled
    assert not by_id["addressed-physical-cross-map"].supplies_assembled_endpoint_weyl_byproduct
    assert by_id["final-root-label-retaining-program"].supplies_endpoint_program_column
    assert not by_id["final-root-label-retaining-program"].full_domain_unitary_or_block_encoding_specified
    assert not by_id["orientation-polar-Q_R"].compiled
    assert not any(
        row.compiled
        and row.supplies_endpoint_program_column
        and row.full_domain_unitary_or_block_encoding_specified
        for row in inventory
    )


def test_full_row_copy_input_validation() -> None:
    with pytest.raises(ValueError):
        _fourier_unitary(1)
    with pytest.raises(ValueError):
        _cyclic_branch_representation_rows(1, 2)
    rows = _cyclic_branch_representation_rows(2, 2)
    with pytest.raises(ValueError):
        full_generalized_row_copy_unitary(rows, np.eye(3))
    bad_rows = (2 * np.eye(4), np.eye(4))
    with pytest.raises(ValueError):
        full_generalized_row_copy_unitary(bad_rows, np.eye(2))
    with pytest.raises(ValueError):
        audit_endpoint_byproduct_branch_separation(
            "edge",
            np.diag([0.0, 0.5]),
            np.eye(2),
        )
    with pytest.raises(ValueError):
        physical_preparation_scaling_record(2)


@pytest.mark.parametrize("n", [3, 4, 8, 16, 32, 64, 128, 256])
def test_scaling_keeps_row_copy_and_endpoint_preparation_separate(n: int) -> None:
    row = physical_preparation_scaling_record(n)

    assert row.generalized_row_copy_full_unitary_polynomial
    assert row.generalized_row_copy_all_columns_branch_preserving
    assert row.addressed_cross_map_block_encoding_normalization == pytest.approx(1.0)
    assert not row.full_endpoint_preparation_unitary_compiled
    assert not row.endpoint_weyl_pair_compiled
    assert not row.typical_natural_effect_branch_separation_proved
    assert row.permutation_register_log2_dimension == pytest.approx(
        math.log2(math.factorial(n))
    )


def test_report_routes_next_pass_to_available_cross_map_primitive() -> None:
    report = run_final_root_physical_preparation_extension_scope_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["row_copy_control_failure_count"] == 0
    assert report.headline_metrics["byproduct_separation_control_failure_count"] == 0
    assert report.headline_metrics["compiled_full_endpoint_preparation_unitary_count"] == 0
    assert report.headline_metrics["compiled_addressed_cross_branch_signal_count"] == 1
    assert report.headline_metrics["compiled_assembled_endpoint_weyl_byproduct_count"] == 0
    assert report.claim_gate["complete_full_domain_generalized_row_copy_unitary_typed"]
    assert report.claim_gate["every_row_copy_nonprogram_ancilla_block_branch_preserving"]
    assert not report.claim_gate["row_copy_nonprogram_columns_supply_endpoint_weyl_byproduct"]
    assert not report.claim_gate["compiled_full_domain_endpoint_preparation_A_V_exists"]
    assert report.claim_gate["addressed_cross_map_signal_normalization_one_available"]
    assert not report.claim_gate["addressed_cross_maps_assembled_into_endpoint_weyl_pair"]
    assert not report.claim_gate["typical_natural_effect_branch_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "physical-preparation-extension-scope.json"
    payload = write_final_root_physical_preparation_extension_scope_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"][
        "all_row_copy_columns_branch_preserving_theorem_count"
    ] == 1
