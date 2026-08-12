from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_physical_row_copy_erasure_no_go import (
    audit_native_row_erasure,
    audit_row_copy_range,
    natural_row_erasure_scaling_record,
    run_physical_row_copy_erasure_no_go,
)


def _coordinate_projectors(count: int, rank: int) -> tuple[np.ndarray, ...]:
    dimension = count * rank
    output = []
    for branch in range(count):
        projector = np.zeros((dimension, dimension), dtype=complex)
        start = branch * rank
        projector[start : start + rank, start : start + rank] = np.eye(rank)
        output.append(projector)
    return tuple(output)


def _walsh_row(count: int, character: int = 0) -> tuple[complex, ...]:
    return tuple(
        (-1.0 if (index & character).bit_count() % 2 else 1.0)
        / math.sqrt(count)
        for index in range(count)
    )


def test_fixed_row_copy_range_is_exact_full_orientation_direct_sum() -> None:
    row = audit_row_copy_range(
        3,
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
        control_id="W3",
    )

    assert row.exact_full_direct_sum_range_verified
    assert row.active_sector_row_count > 0
    assert row.maximum_range_projector_residual < 1e-12
    assert row.maximum_range_rank_residual == 0
    assert row.maximum_invariant_range_leakage < 1e-12


@pytest.mark.parametrize(("count", "rank"), ((2, 1), (4, 1), (4, 2), (8, 1)))
def test_flat_native_row_copy_success_is_inverse_width(
    count: int,
    rank: int,
) -> None:
    row = audit_native_row_erasure(
        "FLAT",
        _coordinate_projectors(count, rank),
        _walsh_row(count),
    )

    assert row.native_one_pass_bound_verified
    assert row.row_copy_native_state_identity_residual < 1e-12
    assert row.exact_acceptance_probability == pytest.approx(1 / count)
    assert row.frame_second_moment_per_trace == pytest.approx(1.0)
    assert row.maximum_branch_rank == rank
    assert row.total_coefficient_rank == count * rank


def test_bound_allows_arbitrary_branch_controlled_carrier_unitaries() -> None:
    projectors = _coordinate_projectors(4, 2)
    dimension = projectors[0].shape[0]
    permutations = []
    for shift in range(4):
        permutation = np.roll(np.eye(dimension, dtype=complex), shift, axis=0)
        permutations.append(permutation)
    row = audit_native_row_erasure(
        "CONTROLLED",
        projectors,
        _walsh_row(4, character=3),
        block_unitaries=tuple(permutations),
    )

    assert row.native_one_pass_bound_verified
    assert row.support_trace_budget <= row.support_trace_budget_upper_bound + 1e-12
    assert row.exact_acceptance_probability <= row.optimized_acceptance_upper_bound


def test_overlapping_frame_obeys_second_moment_spectral_split_bound() -> None:
    vectors = (
        np.asarray((1.0, 0.0, 0.0, 0.0), complex),
        np.asarray((1.0, 1.0, 0.0, 0.0), complex) / math.sqrt(2),
        np.asarray((0.0, 1.0, 1.0, 0.0), complex) / math.sqrt(2),
        np.asarray((1.0, 0.0, 0.0, 0.0), complex),
    )
    projectors = tuple(np.outer(vector, vector.conj()) for vector in vectors)
    row = audit_native_row_erasure("OVERLAP", projectors, _walsh_row(4, 2))

    assert row.native_one_pass_bound_verified
    assert row.frame_rank < row.total_coefficient_rank
    assert row.frame_second_moment_per_trace > 1.0
    assert row.exact_acceptance_probability <= row.optimized_acceptance_upper_bound


def test_natural_scaling_eventually_beats_every_fixed_polynomial_benchmark() -> None:
    low = natural_row_erasure_scaling_record(32)
    high = natural_row_erasure_scaling_record(128)

    assert not low.one_pass_native_erasure_superpolynomial
    assert high.one_pass_native_erasure_superpolynomial
    assert high.one_pass_native_success_log2_upper_bound < -250
    assert (
        high.amplitude_amplification_query_log2_lower_bound
        > high.polynomial_benchmark_log2
    )
    assert not high.multi_round_source_adapted_transform_ruled_out


def test_report_rules_out_one_pass_but_preserves_multi_round_routes() -> None:
    report = run_physical_row_copy_erasure_no_go()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "fixed_row_copy_range_equals_full_orientation_direct_sum"
    ]
    assert report.claim_gate["physical_native_state_equals_RRstar_over_trace"]
    assert report.claim_gate["one_pass_native_erasure_moment_bound_proved"]
    assert report.claim_gate["natural_one_pass_erasure_superpolynomial"]
    assert not report.claim_gate["physical_interference_filter_refuted"]
    assert not report.claim_gate["multi_round_source_adapted_transform_ruled_out"]
    assert not report.claim_gate["arbitrary_physical_orientation_polar_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_row_copy_erasure_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        audit_row_copy_range(3, (), control_id="EMPTY")
    with pytest.raises(ValueError):
        audit_native_row_erasure("ONE", (_coordinate_projectors(2, 1)[0],), (1.0,))
    with pytest.raises(ValueError):
        audit_native_row_erasure(
            "BAD-ROW",
            _coordinate_projectors(2, 1),
            (1.0, 1.0),
        )
    with pytest.raises(ValueError):
        natural_row_erasure_scaling_record(8, fixed_jump_log2_arity=100)
