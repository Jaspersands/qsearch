from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_final_root_program_contraction_normalization_no_go import (
    _control_inputs,
    audit_direct_program_contraction,
    natural_program_contraction_scaling_record,
    normalized_program_reflection_partial_trace,
    optimal_direct_program_insertion,
    program_copy_normalization_control,
    program_partial_contraction,
    run_final_root_program_contraction_normalization_no_go,
    write_final_root_program_contraction_normalization_no_go_report,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    _psd_power,
    weyl_unitary_error_basis,
)


@pytest.mark.parametrize("dimension", [2, 3, 4])
@pytest.mark.parametrize("rotated", [False, True])
def test_direct_program_contraction_has_exact_inverse_dimension_boundary(
    dimension: int,
    rotated: bool,
) -> None:
    effect, density = _control_inputs(dimension, rotated=rotated)
    shift = weyl_unitary_error_basis(dimension)[dimension]
    row = audit_direct_program_contraction(
        f"d{dimension}-r{int(rotated)}",
        effect,
        density,
        shift,
    )

    assert row.exact_inverse_dimension_boundary_verified
    assert row.direct_contraction_residual < 1e-10
    assert row.direct_insertion_uniqueness_residual < 1e-10
    assert row.flattened_partial_trace_residual < 1e-10
    assert row.reflection_partial_trace_residual < 1e-10
    assert row.normalized_program_projector_trace_norm == pytest.approx(1.0)
    assert row.endpoint_byproduct_trace_norm == pytest.approx(dimension)
    assert row.flattened_output_trace_norm == pytest.approx(1.0)
    assert row.reflection_byproduct_coefficient_magnitude == pytest.approx(
        2 / dimension
    )
    assert row.selected_branch_probability == pytest.approx(1 / dimension**2)
    assert row.selected_branch_amplitude_amplification_factor == dimension


def test_flat_density_optimum_is_exactly_one_over_dimension() -> None:
    dimension = 5
    density = np.eye(dimension, dtype=complex) / dimension
    error = weyl_unitary_error_basis(dimension)[dimension]
    insertion, coefficient = optimal_direct_program_insertion(density, error)

    assert coefficient == pytest.approx(1 / dimension)
    assert np.linalg.norm(insertion, ord=2) == pytest.approx(1.0)
    assert np.linalg.norm(insertion - error, ord=2) < 1e-10


def test_direct_insertion_is_uniquely_the_inverse_density_sandwich() -> None:
    density = np.diag([0.1, 0.3, 0.6]).astype(complex)
    error = weyl_unitary_error_basis(3)[3]
    insertion, coefficient = optimal_direct_program_insertion(density, error)
    root = _psd_power(density, 0.5, tolerance=1e-12)

    assert np.linalg.norm(
        root @ insertion @ root - coefficient * error,
        ord=2,
    ) < 1e-10
    assert np.linalg.norm(insertion, ord=2) == pytest.approx(1.0)
    assert 0.1 <= coefficient <= 0.6


@pytest.mark.parametrize("dimension", [2, 3, 8])
@pytest.mark.parametrize("copies", [1, 2, 5])
def test_fixed_normalized_copy_count_cannot_beat_trace_norm_bound(
    dimension: int,
    copies: int,
) -> None:
    row = program_copy_normalization_control(dimension, copies)

    assert row.bounded_linear_copy_contraction_boundary_verified
    assert row.input_tensor_trace_norm == pytest.approx(1.0)
    assert row.target_byproduct_trace_norm == dimension
    assert row.maximum_exact_coefficient == pytest.approx(1 / dimension)
    assert row.canonical_bound_saturated
    assert not row.constant_coefficient_allowed_by_bound


def test_program_reflection_includes_only_trace_background_and_two_over_d_signal() -> None:
    dimension = 3
    endpoint = np.vstack(
        (
            math.sqrt(0.4) * np.eye(dimension),
            math.sqrt(0.6) * np.eye(dimension),
        )
    )
    shift = weyl_unitary_error_basis(dimension)[dimension]
    byproduct = endpoint @ shift @ endpoint.conj().T
    observed = normalized_program_reflection_partial_trace(endpoint, shift)

    assert abs(np.trace(shift)) < 1e-12
    assert np.linalg.norm(observed + 2 * byproduct / dimension, ord=2) < 1e-10


def test_input_validation_rejects_invalid_direct_contractions() -> None:
    unitary = np.eye(2, dtype=complex)
    with pytest.raises(ValueError):
        optimal_direct_program_insertion(np.eye(2), unitary)
    with pytest.raises(ValueError):
        optimal_direct_program_insertion(np.diag([1.0, 0.0]), unitary)
    with pytest.raises(ValueError):
        optimal_direct_program_insertion(np.eye(2) / 2, 2 * unitary)
    with pytest.raises(ValueError):
        program_partial_contraction(np.eye(3, 2), np.eye(3))
    with pytest.raises(ValueError):
        program_copy_normalization_control(1, 1)
    with pytest.raises(ValueError):
        program_copy_normalization_control(2, 0)
    with pytest.raises(ValueError):
        natural_program_contraction_scaling_record(3)


@pytest.mark.parametrize("n", [8, 12, 16, 24, 32, 48])
def test_natural_program_signal_is_superpolynomial(n: int) -> None:
    row = natural_program_contraction_scaling_record(n)
    dimension = int(row.natural_high_row_irrep_dimension_lower_bound_decimal)

    assert row.canonical_coefficient_log2_upper_bound_leading_term == pytest.approx(
        -math.log2(dimension)
    )
    assert row.selected_branch_probability_log2_upper_bound_leading_term == pytest.approx(
        -2 * math.log2(dimension)
    )
    assert row.amplitude_amplification_log2_lower_bound_leading_term == pytest.approx(
        math.log2(dimension)
    )
    assert row.qsvt_degree_lower_bound > 0
    assert row.retained_logical_dimension_same_factorial_exponent_proved
    assert row.canonical_program_contraction_superpolynomial
    assert not row.arbitrary_coherent_processor_lower_bound_proved


def test_report_scopes_no_go_to_direct_program_contraction_architecture() -> None:
    report = run_final_root_program_contraction_normalization_no_go()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["direct_control_failure_count"] == 0
    assert report.headline_metrics["copy_normalization_control_failure_count"] == 0
    assert report.claim_gate["normalized_flattened_program_partial_trace_is_B_over_D"]
    assert report.claim_gate[
        "unflattened_direct_insertion_is_unique_inverse_density_sandwich"
    ]
    assert not report.claim_gate[
        "retained_window_direct_contraction_has_constant_normalization"
    ]
    assert not report.claim_gate[
        "fixed_copy_bounded_linear_program_density_contraction_has_constant_normalization"
    ]
    assert not report.claim_gate["representation_specific_coherent_block_encoding_compiled"]
    assert not report.claim_gate["arbitrary_coherent_processor_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "program-contraction-normalization.json"
    payload = write_final_root_program_contraction_normalization_no_go_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"][
        "bounded_linear_fixed_copy_normalization_no_go_count"
    ] == 1
