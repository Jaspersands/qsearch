from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_final_root_state_preparation_oracle_query_boundary import (
    _minimal_state_rotation,
    _program_reflection,
    _unitary_contraction_dilation,
    _unitary_mapping_anchor_to_state,
    audit_canonical_endpoint_oracle_hard_pair,
    audit_preparation_extension_gauge,
    canonical_endpoint_oracle_hard_pair,
    natural_state_preparation_oracle_scaling_record,
    run_final_root_state_preparation_oracle_query_boundary,
    write_final_root_state_preparation_oracle_query_boundary_report,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    weyl_unitary_error_basis,
)


@pytest.mark.parametrize("dimension", [2, 3, 4, 5, 8])
def test_canonical_hard_pair_has_inverse_sqrt_program_distance_and_constant_target_distance(
    dimension: int,
) -> None:
    row = audit_canonical_endpoint_oracle_hard_pair(dimension)

    assert row.exact_canonical_hard_pair_verified
    assert row.endpoint_isometry_residual < 1e-10
    assert row.canonical_endpoint_formula_residual < 1e-10
    assert row.normalized_program_state_distance == pytest.approx(
        row.changed_endpoint_column_distance / math.sqrt(dimension)
    )
    assert row.fixed_weyl_byproduct_separation == pytest.approx(
        row.changed_endpoint_column_distance
    )
    assert row.reflection_oracle_distance == pytest.approx(
        row.predicted_reflection_oracle_distance
    )
    assert row.close_preparation_oracle_distance == pytest.approx(
        row.predicted_close_preparation_oracle_distance
    )


@pytest.mark.parametrize("dimension", [2, 3, 5, 8, 13])
def test_hybrid_query_bounds_scale_as_square_root_dimension(dimension: int) -> None:
    row = audit_canonical_endpoint_oracle_hard_pair(
        dimension,
        block_normalization=2.0,
        relative_separation_error=0.2,
    )

    assert row.constant_normalization_reflection_query_is_omega_sqrt_dimension
    assert row.all_extension_robust_preparation_query_is_omega_sqrt_dimension
    assert row.exact_reflection_query_lower_bound >= (
        0.8 * math.sqrt(dimension) / 4.0 - 1e-12
    )
    assert row.exact_robust_preparation_query_lower_bound == pytest.approx(
        0.8 * math.sqrt(dimension) / 2.0
    )


def test_hard_pair_remains_inside_positive_canonical_endpoint_family() -> None:
    effect_zero, effect_one, endpoint_zero, endpoint_one = (
        canonical_endpoint_oracle_hard_pair(4)
    )

    assert np.all(np.linalg.eigvalsh(effect_zero) > 0)
    assert np.all(np.linalg.eigvalsh(effect_one) > 0)
    assert np.all(np.linalg.eigvalsh(np.eye(4) - effect_zero) > 0)
    assert np.all(np.linalg.eigvalsh(np.eye(4) - effect_one) > 0)
    assert np.linalg.norm(endpoint_zero[:, 1:] - endpoint_one[:, 1:], ord=2) < 1e-12


def test_close_preparation_extensions_are_valid_unitaries() -> None:
    _, _, endpoint_zero, endpoint_one = canonical_endpoint_oracle_hard_pair(3)
    first = (endpoint_zero / math.sqrt(3)).reshape(-1)
    second = (endpoint_one / math.sqrt(3)).reshape(-1)
    preparation = _unitary_mapping_anchor_to_state(first)
    rotation = _minimal_state_rotation(first, second)
    other = rotation @ preparation

    identity = np.eye(first.size, dtype=complex)
    assert np.linalg.norm(preparation.conj().T @ preparation - identity, ord=2) < 1e-10
    assert np.linalg.norm(other.conj().T @ other - identity, ord=2) < 1e-10
    assert np.linalg.norm(preparation[:, 0] - first) < 1e-10
    assert np.linalg.norm(other[:, 0] - second) < 1e-10
    assert np.linalg.norm(preparation - other, ord=2) == pytest.approx(
        np.linalg.norm(first - second)
    )


@pytest.mark.parametrize("dimension", [3, 4, 5])
def test_friendly_preparation_extension_can_leak_target_in_one_query(
    dimension: int,
) -> None:
    row = audit_preparation_extension_gauge(dimension)

    assert row.one_query_leaky_extension_verified
    assert row.preparation_state_residual < 1e-9
    assert row.preparation_unitarity_residual < 1e-8
    assert row.leaked_block_encoding_residual < 1e-8
    assert row.leaked_block_normalization == pytest.approx(1.0)
    assert row.leaked_block_query_count == 1
    assert row.same_prepared_state_extension_distance > 1e-3
    assert not row.bare_first_column_promise_defines_extension_independent_query_complexity


def test_julia_dilation_has_requested_top_left_block() -> None:
    dimension = 3
    contraction = np.diag([0.2, 0.5, 0.9]).astype(complex)
    dilation = _unitary_contraction_dilation(contraction)

    assert np.linalg.norm(dilation[:dimension, :dimension] - contraction, ord=2) < 1e-12
    assert np.linalg.norm(
        dilation.conj().T @ dilation - np.eye(2 * dimension),
        ord=2,
    ) < 1e-10


def test_reflection_helper_and_input_guards() -> None:
    state = np.array([1.0, 1.0j]) / math.sqrt(2)
    reflection = _program_reflection(state)

    assert np.linalg.norm(reflection.conj().T @ reflection - np.eye(2), ord=2) < 1e-12
    assert np.linalg.norm(reflection @ state + state) < 1e-12
    with pytest.raises(ValueError):
        _program_reflection(np.ones(2))
    with pytest.raises(ValueError):
        canonical_endpoint_oracle_hard_pair(1)
    with pytest.raises(ValueError):
        canonical_endpoint_oracle_hard_pair(2, perturbed_effect=0.5)
    with pytest.raises(ValueError):
        audit_canonical_endpoint_oracle_hard_pair(2, block_normalization=0.5)
    with pytest.raises(ValueError):
        audit_canonical_endpoint_oracle_hard_pair(2, relative_separation_error=1.0)
    with pytest.raises(ValueError):
        audit_preparation_extension_gauge(2)
    with pytest.raises(ValueError):
        _unitary_contraction_dilation(2 * np.eye(2))
    with pytest.raises(ValueError):
        natural_state_preparation_oracle_scaling_record(3)


@pytest.mark.parametrize("n", [8, 12, 16, 24, 32, 48])
def test_natural_oracle_query_lower_bounds_are_superpolynomial(n: int) -> None:
    row = natural_state_preparation_oracle_scaling_record(n)
    dimension = int(row.natural_high_row_irrep_dimension_lower_bound_decimal)

    assert row.reflection_query_lower_bound == pytest.approx(
        0.9 * math.sqrt(dimension) / 2
    )
    assert row.robust_preparation_query_lower_bound == pytest.approx(
        0.9 * math.sqrt(dimension)
    )
    assert row.reflection_query_lower_bound_log2_leading_term == pytest.approx(
        0.5 * math.log2(dimension)
    )
    assert (
        row.uniform_reflection_compiler_worst_case_superpolynomial_at_natural_dimension_scale
    )
    assert (
        row.uniform_robust_preparation_compiler_worst_case_superpolynomial_at_natural_dimension_scale
    )
    assert not row.particular_structured_preparation_circuit_lower_bound_proved


def test_report_keeps_structured_preparation_circuit_outside_black_box_lower_bound() -> None:
    report = run_final_root_state_preparation_oracle_query_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["hard_pair_control_failure_count"] == 0
    assert report.headline_metrics["extension_gauge_control_failure_count"] == 0
    assert report.claim_gate[
        "constant_normalization_reflection_only_query_complexity_is_omega_sqrt_D"
    ]
    assert report.claim_gate[
        "all_extension_robust_preparation_query_complexity_is_omega_sqrt_D"
    ]
    assert not report.claim_gate[
        "bare_first_column_preparation_promise_defines_query_complexity"
    ]
    assert report.claim_gate["friendly_preparation_extension_can_leak_target_in_one_query"]
    assert not report.claim_gate[
        "particular_structured_schur_qft_gpe_preparation_lower_bound_proved"
    ]
    assert not report.claim_gate[
        "typical_natural_endpoint_oracle_query_lower_bound_proved"
    ]
    assert not report.claim_gate["arbitrary_coherent_processor_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "state-preparation-oracle-query-boundary.json"
    payload = write_final_root_state_preparation_oracle_query_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"][
        "reflection_oracle_sqrt_dimension_query_no_go_count"
    ] == 1
