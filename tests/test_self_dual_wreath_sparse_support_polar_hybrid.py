from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_sparse_support_polar_hybrid import (
    _random_unitary,
    _support_projector,
    audit_low_singular_native_mass,
    audit_native_polar_perturbation,
    audit_same_gram_child_hybrid,
    natural_sparse_hybrid_schedule_record,
    run_sparse_support_polar_hybrid,
)
from self_dual_wreath_sparse_support_polar_schedule import _random_projector


def _frame(
    dimension: int,
    leaf_count: int,
    rank: int,
    rng: np.random.Generator,
) -> np.ndarray:
    return sum(
        (_random_projector(dimension, rank, rng) for _ in range(leaf_count)),
        np.zeros((dimension, dimension), complex),
    )


@pytest.mark.parametrize(
    ("dimension", "leaf_count", "rank"),
    [(10, 2, 2), (14, 3, 2), (18, 4, 2)],
)
def test_gap_free_native_polar_bound_holds_for_projector_frames(
    dimension: int,
    leaf_count: int,
    rank: int,
) -> None:
    rng = np.random.default_rng(6400 + dimension)
    control = audit_native_polar_perturbation(
        "NATIVE",
        _frame(dimension, leaf_count, rank, rng),
        _frame(dimension, leaf_count, rank, rng),
        left_coefficient_trace=leaf_count * rank,
        right_coefficient_trace=leaf_count * rank,
    )

    assert control.gap_free_native_polar_bound_verified
    assert control.initial_supports_match
    assert (
        control.exact_native_rms_polar_error
        <= control.native_rms_polar_error_upper_bound + 1e-8
    )
    assert (
        control.square_root_trace_distance
        <= control.square_root_trace_distance_upper_bound + 1e-8
    )


def test_projection_frames_have_zero_support_replacement_error() -> None:
    rng = np.random.default_rng(6401)
    left = _random_projector(12, 3, rng)
    right = _random_projector(12, 3, rng)
    control = audit_native_polar_perturbation("ZERO", left, right)

    assert control.normalized_pressure == pytest.approx(0.0, abs=1e-10)
    assert control.exact_native_rms_polar_error == pytest.approx(0.0, abs=1e-8)
    assert control.native_rms_polar_error_upper_bound == pytest.approx(0.0)


def test_same_support_child_replacement_has_exact_parent_hybrid_identity() -> None:
    rng = np.random.default_rng(6402)
    left = _frame(14, 3, 2, rng)
    right = _frame(14, 3, 2, rng)
    left_support = _support_projector(left)
    right_support = _support_projector(right)
    control = audit_same_gram_child_hybrid(
        "HYBRID",
        left,
        right,
        _random_unitary(14, rng) @ left_support,
        _random_unitary(14, rng) @ right_support,
        _random_unitary(14, rng) @ left_support,
        _random_unitary(14, rng) @ right_support,
    )

    assert control.exact_same_gram_hybrid_identity_verified
    assert control.gram_matrix_difference_norm == pytest.approx(0.0, abs=1e-8)
    assert control.parent_native_error_squared == pytest.approx(
        control.weighted_child_error_squared,
        abs=1e-7,
    )


def test_low_singular_support_modes_have_controlled_native_mass() -> None:
    correlations = (0.9, 0.65, 0.2)
    left_basis = np.eye(6, dtype=complex)[:, :3]
    right_basis = np.column_stack(
        [
            correlations[index] * np.eye(6)[:, index]
            + np.sqrt(1.0 - correlations[index] ** 2) * np.eye(6)[:, index + 3]
            for index in range(3)
        ]
    )
    left_support = left_basis @ left_basis.conj().T
    right_support = right_basis @ right_basis.conj().T
    left = left_support + np.outer(left_basis[:, 0], left_basis[:, 0].conj())
    right = right_support + np.outer(right_basis[:, 0], right_basis[:, 0].conj())
    control = audit_low_singular_native_mass(
        "LOW",
        left,
        right,
        principal_correlation_threshold=0.5,
        left_coefficient_trace=4,
        right_coefficient_trace=4,
    )

    assert control.low_singular_rank == 2
    assert control.low_singular_rank_and_native_mass_bounds_verified
    assert control.low_singular_rank <= control.low_singular_rank_upper_bound + 1e-8
    assert control.exact_native_state_mass <= control.native_state_mass_upper_bound + 1e-8


def test_tunable_hybrid_and_low_mode_bounds_decrease_with_fixed_arity() -> None:
    rows = [
        natural_sparse_hybrid_schedule_record(bits)
        for bits in (8, 16, 24, 32, 40)
    ]

    assert all(
        right.aggregate_native_rms_polar_error_upper_bound
        < left.aggregate_native_rms_polar_error_upper_bound
        for left, right in zip(rows, rows[1:])
    )
    assert all(
        right.aggregate_low_singular_native_mass_upper_bound
        < left.aggregate_low_singular_native_mass_upper_bound
        for left, right in zip(rows, rows[1:])
    )
    assert rows[-1].aggregate_native_rms_polar_error_upper_bound < 0.1
    assert rows[-1].aggregate_low_singular_native_mass_upper_bound < 0.01
    assert all(row.jump_arity_fixed_before_n_limit for row in rows)
    assert all(not row.coherent_support_reflection_compiler_proved for row in rows)


def test_invalid_hybrid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        natural_sparse_hybrid_schedule_record(2)
    with pytest.raises(ValueError):
        natural_sparse_hybrid_schedule_record(
            8, principal_correlation_threshold=0.0
        )
    with pytest.raises(ValueError):
        audit_native_polar_perturbation(
            "BAD", np.eye(2), np.eye(3)
        )


def test_report_resolves_state_error_but_keeps_coherent_access_open() -> None:
    report = run_sparse_support_polar_hybrid()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["gap_free_native_state_polar_perturbation_proved"]
    assert report.claim_gate["exact_same_support_recursive_hybrid_proved"]
    assert report.claim_gate["annealed_sparse_hierarchy_error_tunable"]
    assert report.claim_gate["low_singular_native_mass_tunable"]
    assert not report.claim_gate["coherent_recursive_support_reflections_proved"]
    assert not report.claim_gate["fixed_R_endpoint_measurement_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
