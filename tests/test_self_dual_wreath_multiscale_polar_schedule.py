import math
from fractions import Fraction

import numpy as np

from self_dual_wreath_multiscale_polar_schedule import (
    MIXED_SCHEDULE_CONDITION_UPPER,
    MIXED_SCHEDULE_EDGE_FLOOR,
    audit_multiway_polar_chain,
    binary_hard_edge_boundary_record,
    multiscale_gaussian_schedule_record,
    run_multiscale_polar_schedule,
)


def test_exact_multiway_chain_handles_rank_deficient_children() -> None:
    rng = np.random.default_rng(41)
    analyses = tuple(
        rng.normal(size=(2, 5)) + 1j * rng.normal(size=(2, 5))
        for _ in range(3)
    )
    row = audit_multiway_polar_chain("RANK-DEFICIENT-3-WAY", analyses)

    assert row.child_count == 3
    assert row.parent_support_rank == 5
    assert row.maximum_child_polar_residual < 1e-10
    assert row.merge_isometry_residual < 1e-10
    assert row.recursive_to_direct_polar_residual < 1e-10
    assert row.exact_multiway_polar_chain_verified


def test_binary_threshold_levels_have_no_interval_uniform_edge() -> None:
    near_one = binary_hard_edge_boundary_record(1.000001)
    near_two = binary_hard_edge_boundary_record(1.999999)

    assert near_one.threshold_nonzero_edge < 1e-10
    assert near_two.below_threshold_nonzero_edge < 1e-10
    assert not near_one.interval_uniform_binary_edge_exists
    assert not near_two.interval_uniform_binary_edge_exists


def test_mixed_schedule_skips_aspects_between_half_and_two() -> None:
    for n in range(3, 101):
        row = multiscale_gaussian_schedule_record(n)
        c = Fraction(row.threshold_ratio_exact)

        assert 1 < c < 2
        assert Fraction(1, 4) < c / 4 < Fraction(1, 2)
        assert 2 < 2 * c < 4
        assert 4 < 4 * c < 8
        assert row.maximum_merge_arity == 8
        assert row.selected_copy_count == row.information_threshold_copy_count + 2
        assert row.minimum_gaussian_nonzero_edge + 1e-13 >= MIXED_SCHEDULE_EDGE_FLOOR
        assert row.maximum_gaussian_support_condition_number <= MIXED_SCHEDULE_CONDITION_UPPER + 1e-10
        assert row.all_depth_gaussian_frame_edge_verified
        assert not row.natural_all_depth_frame_edge_proved
        assert not row.tight_node_frame_block_encoding_proved


def test_edge_and_condition_constants_are_exact_threshold_values() -> None:
    assert math.isclose(MIXED_SCHEDULE_EDGE_FLOOR, 1.5 - math.sqrt(2))
    assert math.isclose(
        MIXED_SCHEDULE_CONDITION_UPPER,
        17 + 12 * math.sqrt(2),
    )


def test_report_blocks_natural_and_access_overclaims() -> None:
    report = run_multiscale_polar_schedule()

    assert report.headline_metrics["multiway_control_failure_count"] == 0
    assert report.headline_metrics["mixed_schedule_failure_count"] == 0
    assert report.claim_gate["exact_constant_arity_polar_chain_proved"]
    assert not report.claim_gate[
        "binary_dyadic_gaussian_all_depth_uniform_edge_proved"
    ]
    assert report.claim_gate[
        "mixed_arity_gaussian_all_depth_uniform_edge_proved"
    ]
    assert not report.claim_gate[
        "binary_pairwise_pseudoinverse_comparability_mathematically_mandatory"
    ]
    assert not report.claim_gate["natural_all_depth_frame_edges_proved"]
    assert not report.claim_gate[
        "tight_coherent_node_frame_block_encodings_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
