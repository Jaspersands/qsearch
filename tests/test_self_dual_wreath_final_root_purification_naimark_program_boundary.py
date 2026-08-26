from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    PARENT_WINDOW_LOWER,
    PARENT_WINDOW_UPPER,
    _rotated_metric_pair,
    audit_bell_transduction,
    audit_metric_only_correction_obstruction,
    audit_purification_flattening,
    final_root_endpoint,
    natural_program_scaling_record,
    optimal_purification_flattening_filter,
    run_final_root_purification_naimark_program_boundary,
    weyl_unitary_error_basis,
    write_final_root_purification_naimark_program_boundary_report,
)


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_exact_purification_flattening_has_no_width_charge(dimension: int) -> None:
    left, right = _rotated_metric_pair(dimension)
    row = audit_purification_flattening(f"rotated-{dimension}", left, right)

    assert row.constant_success_without_width_charge_verified
    assert row.exact_unique_whitening_filter_verified
    assert row.exact_flattening_residual < 1e-10
    assert row.endpoint_isometry_residual < 1e-10
    assert row.optimal_flattening_success_probability >= (
        row.metric_ratio_success_lower_bound - 1e-10
    )
    assert row.optimal_filter_operator_norm == pytest.approx(1.0)


def test_flat_resource_is_already_maximally_entangled() -> None:
    row = audit_purification_flattening(
        "flat",
        0.5 * np.eye(3),
        0.5 * np.eye(3),
    )

    assert row.optimal_flattening_success_probability == pytest.approx(1.0)
    assert row.metric_condition_number == pytest.approx(1.0)
    assert row.resource_minimum_schmidt_probability == pytest.approx(1 / 3)


def test_optimal_filter_rejects_singular_or_unnormalized_density() -> None:
    with pytest.raises(ValueError):
        optimal_purification_flattening_filter(np.diag([1.0, 0.0]))
    with pytest.raises(ValueError):
        optimal_purification_flattening_filter(np.eye(2))
    with pytest.raises(ValueError):
        final_root_endpoint(np.eye(2), -np.eye(2))


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_weyl_bell_link_and_all_byproduct_corrections(dimension: int) -> None:
    left, right = _rotated_metric_pair(dimension)
    _, _, endpoint, _ = final_root_endpoint(left, right)
    psi = np.arange(1, dimension + 1, dtype=complex)
    psi /= np.linalg.norm(psi)
    row = audit_bell_transduction(f"bell-{dimension}", endpoint, psi)

    assert row.exact_bell_program_boundary_verified
    assert row.unitary_error_basis_size == dimension**2
    assert row.selected_clean_outcome_probability == pytest.approx(1 / dimension**2)
    assert row.selected_clean_outcome_amplitude_amplification_factor == dimension
    assert row.maximum_byproduct_correction_residual < 1e-10
    assert row.discarded_label_depolarizing_residual < 1e-10


def test_weyl_basis_validation_and_dimension_guard() -> None:
    errors = weyl_unitary_error_basis(5)
    assert len(errors) == 25
    assert max(
        abs(np.trace(left.conj().T @ right) - (5 if i == j else 0))
        for i, left in enumerate(errors)
        for j, right in enumerate(errors)
    ) < 1e-10
    with pytest.raises(ValueError):
        weyl_unitary_error_basis(1)


def test_same_metric_and_schmidt_law_do_not_determine_corrections() -> None:
    row = audit_metric_only_correction_obstruction()

    assert row.same_metric_does_not_determine_byproduct_correction_verified
    assert row.common_metric_residual < 1e-12
    assert row.common_schmidt_spectrum_residual < 1e-12
    assert row.endpoint_program_overlap > 0
    assert row.shared_correction_gram_obstruction > 1e-3


@pytest.mark.parametrize("n", [8, 12, 16, 24, 32, 48])
def test_natural_selected_bell_outcome_is_superpolynomial(n: int) -> None:
    row = natural_program_scaling_record(n)
    dimension = int(row.natural_high_row_irrep_dimension_lower_bound_decimal)

    assert dimension >= 2
    assert row.selected_bell_success_log2_upper_bound_leading_term == pytest.approx(
        -2 * math.log2(dimension)
    )
    assert row.selected_bell_amplification_log2_lower_bound_leading_term == pytest.approx(
        math.log2(dimension)
    )
    assert row.retained_logical_dimension_same_factorial_exponent_proved
    assert row.selected_outcome_transduction_superpolynomial
    assert not row.all_outcome_byproduct_correction_compiled
    with pytest.raises(ValueError):
        natural_program_scaling_record(3)


def test_report_keeps_state_conversion_and_gate_compilation_separate() -> None:
    report = run_final_root_purification_naimark_program_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["flattening_control_failure_count"] == 0
    assert report.headline_metrics["bell_control_failure_count"] == 0
    assert report.claim_gate[
        "label_retaining_purification_state_has_constant_success_flattening"
    ]
    assert not report.claim_gate[
        "inverse_width_overlap_unavoidable_for_purification_state"
    ]
    assert report.claim_gate[
        "exact_one_sided_flattening_filter_is_unique_whitening"
    ]
    assert not report.claim_gate["scale_free_whitening_filter_compiled"]
    assert not report.claim_gate[
        "flattened_choi_state_is_an_executable_isometry_oracle"
    ]
    assert report.claim_gate[
        "canonical_selected_bell_outcome_probability_is_inverse_dimension_squared"
    ]
    assert not report.claim_gate["arbitrary_choi_to_channel_processor_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics[
        "retained_window_flattening_success_lower_bound"
    ] == pytest.approx(PARENT_WINDOW_LOWER / PARENT_WINDOW_UPPER)


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "purification-naimark-program.json"
    payload = write_final_root_purification_naimark_program_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"]["direct_matrix_povm_naimark_circuit_count"] == 0
