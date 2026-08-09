import numpy as np
import pytest

from self_dual_wreath_component_aggregate_frame_indeterminacy import (
    aggregate_frame_indeterminacy_scaling_record,
    aggregate_indeterminacy_projection_frames,
    audit_aggregate_frame_indeterminacy,
    computational_and_fourier_projectors,
    run_component_aggregate_frame_indeterminacy,
)


@pytest.mark.parametrize("dimension", [2, 3, 4, 5, 8])
def test_identical_aggregate_frames_have_zero_versus_constant_component_gap(
    dimension: int,
) -> None:
    row = audit_aggregate_frame_indeterminacy(dimension)

    assert row.exact_all_order_aggregate_indeterminacy_verified is True
    assert row.aggregate_frame_difference_norm < 1e-12
    assert row.maximum_normalized_aggregate_moment_residual < 1e-10
    assert row.maximum_resolvent_residual < 1e-12
    assert row.commuting_normalized_commutator_trace == pytest.approx(0.0)
    assert row.noncommuting_normalized_commutator_trace == pytest.approx(
        (1 - 1 / dimension) / 8
    )
    assert row.noncommuting_commutator_defect_minimum_eigenvalue == pytest.approx(
        (1 - 1 / dimension) / 8
    )
    assert row.noncommuting_commutator_defect_maximum_eigenvalue == pytest.approx(
        (1 - 1 / dimension) / 8
    )


def test_computational_and_fourier_bases_are_mutually_unbiased() -> None:
    dimension = 7
    computational, fourier = computational_and_fourier_projectors(dimension)

    for left in computational:
        for right in fourier:
            assert np.trace(left @ right).real == pytest.approx(1 / dimension)


def test_both_projection_families_sum_to_two_identity() -> None:
    dimension = 6
    commuting, noncommuting = aggregate_indeterminacy_projection_frames(dimension)

    assert sum(commuting) == pytest.approx(2 * np.eye(dimension))
    assert sum(noncommuting) == pytest.approx(2 * np.eye(dimension))
    for leaf in (*commuting, *noncommuting):
        assert leaf @ leaf == pytest.approx(leaf)


def test_noncommuting_gap_survives_dimension_growth() -> None:
    row = aggregate_frame_indeterminacy_scaling_record(256)

    assert row.aggregate_frame_condition_number == pytest.approx(1.0)
    assert row.commuting_normalized_commutator_trace == pytest.approx(0.0)
    assert row.noncommuting_normalized_commutator_trace > 0.124
    assert row.limiting_noncommuting_normalized_commutator_trace == pytest.approx(
        1 / 8
    )
    assert row.identical_all_order_aggregate_frame_data is True
    assert row.natural_leaf_resolved_transfer_proved is False


def test_report_requires_leaf_resolved_green_moments() -> None:
    report = run_component_aggregate_frame_indeterminacy()

    assert report.status == (
        "aggregate-frame-route-falsified-leaf-resolved-green-moments-required"
    )
    assert report.headline_metrics[
        "aggregate_frame_all_order_indeterminacy_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "mutually_unbiased_constant_component_gap_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "aggregate_sibling_frame_data_determine_component_M4"
    ] is False
    assert report.claim_gate["leaf_resolved_green_function_moments_required"] is True
    assert report.claim_gate["natural_compressed_component_M4_positive"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
