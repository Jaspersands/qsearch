from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_physical_branch_erasure_boundary import (
    accepted_character_rank_control,
    audit_correlated_input_escape,
    audit_flat_polar_branch_erasure,
    physical_branch_erasure_scaling_record,
    robust_branch_erasure_bound,
    run_physical_branch_erasure_boundary,
    walsh_matrix,
)


@pytest.mark.parametrize("branch_count", (2, 4, 8, 16))
def test_walsh_matrix_is_unitary(branch_count: int) -> None:
    matrix = walsh_matrix(branch_count)

    assert np.linalg.norm(
        matrix.conj().T @ matrix - np.eye(branch_count),
        ord=2,
    ) < 1e-12


@pytest.mark.parametrize(
    ("branch_count", "block_dimension"),
    ((2, 1), (4, 1), (4, 3), (8, 2), (16, 1)),
)
def test_flat_polar_branch_erasure_has_exact_inverse_width_success(
    branch_count: int,
    block_dimension: int,
) -> None:
    row = audit_flat_polar_branch_erasure(branch_count, block_dimension)

    assert row.exact_inverse_width_boundary_verified
    assert row.flat_frame_gram_residual == pytest.approx(0.0)
    assert row.polar_isometry_residual == pytest.approx(0.0)
    assert row.postselected_scaled_polar_amplitude == pytest.approx(
        1 / math.sqrt(branch_count)
    )
    assert row.postselected_success_probability == pytest.approx(
        1 / branch_count
    )
    assert row.scaled_polar_residual == pytest.approx(0.0)


def test_robust_bound_forbids_constant_amplitude_small_error() -> None:
    q = 64
    row = robust_branch_erasure_bound(tuple(walsh_matrix(q)[0]), 2 / 3)

    assert row.bound_verified
    assert row.minimum_row_magnitude == pytest.approx(1 / math.sqrt(q))
    assert row.operator_error_lower_bound == pytest.approx(2 / 3 - 1 / math.sqrt(q))
    assert not row.constant_amplitude_vanishing_error_possible


def test_nonuniform_row_cannot_improve_its_smallest_branch() -> None:
    q = 8
    vector = np.zeros(q, dtype=complex)
    vector[0] = math.sqrt(0.75)
    vector[1:] = math.sqrt(0.25 / (q - 1))
    row = robust_branch_erasure_bound(tuple(vector), 0.5)

    assert row.bound_verified
    assert row.minimum_row_magnitude < 1 / math.sqrt(q)
    assert row.operator_error_lower_bound > 0.3


@pytest.mark.parametrize(
    ("branch_count", "accepted", "expected"),
    ((16, 1, 1 / 16), (16, 8, 1 / 2), (64, 8, 1 / 8)),
)
def test_accepting_rank_r_retains_r_over_q_but_does_not_erase(
    branch_count: int,
    accepted: int,
    expected: float,
) -> None:
    row = accepted_character_rank_control(branch_count, accepted)

    assert row.covariant_uniform_branch_acceptance == pytest.approx(expected)
    assert row.rank_fraction_upper_bound == pytest.approx(expected)
    assert row.branch_label_erased == (accepted == 1)
    if expected >= 0.1:
        assert row.constant_acceptance_requires_linear_rank


@pytest.mark.parametrize(
    ("branch_count", "carrier_dimension"),
    ((2, 5), (4, 3), (8, 2), (16, 1)),
)
def test_correlated_source_image_is_a_real_escape_from_the_no_go(
    branch_count: int,
    carrier_dimension: int,
) -> None:
    row = audit_correlated_input_escape(branch_count, carrier_dimension)

    assert row.deterministic_branch_erasure_verified
    assert row.diagonal_embedding_isometry_residual < 1e-12
    assert row.branch_erasure_residual < 1e-12
    assert not row.flat_orthogonal_full_direct_sum_input


def test_factorial_width_one_pass_erasure_becomes_superpolynomial() -> None:
    row = physical_branch_erasure_scaling_record(80)

    assert row.one_pass_erasure_amplification_superpolynomial
    assert (
        row.amplitude_amplification_query_log2_lower_bound
        > row.polynomial_benchmark_log2
    )
    assert not row.direct_source_correlated_transform_ruled_out


def test_report_closes_only_the_one_pass_physical_loophole() -> None:
    report = run_physical_branch_erasure_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["physical_branch_register_removes_preparation_cost"]
    assert not report.claim_gate["physical_branch_register_removes_erasure_width"]
    assert not report.claim_gate["one_pass_branch_fourier_erasure_polynomial"]
    assert report.claim_gate["source_correlated_escape_exists_abstractly"]
    assert not report.claim_gate[
        "actual_wreath_row_copy_correlated_factorization_proved"
    ]
    assert not report.claim_gate["arbitrary_direct_physical_router_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_branch_erasure_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        walsh_matrix(3)
    with pytest.raises(ValueError):
        accepted_character_rank_control(8, 9)
    with pytest.raises(ValueError):
        robust_branch_erasure_bound((1.0, 1.0), 0.5)
    with pytest.raises(ValueError):
        audit_flat_polar_branch_erasure(4, 1, output_character=4)
