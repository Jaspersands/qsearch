import math

from self_dual_wreath_coverage_welch_pressure import (
    _aligned_projectors,
    _random_projectors,
    _tight_coordinate_projectors,
    audit_fusion_coverage,
    natural_coverage_pressure_target,
    run_coverage_welch_pressure,
)


def test_tight_fusion_control_attains_welch_floor_exactly() -> None:
    record = audit_fusion_coverage(
        "TIGHT-Q8-R4",
        _tight_coordinate_projectors(8, 4),
    )
    assert math.isclose(record.redundancy, 4.0)
    assert math.isclose(record.fusion_potential, record.welch_floor)
    assert math.isclose(record.normalized_excess_fusion_potential, 0.0)
    assert record.observed_low_coverage_fraction == 0
    assert record.observed_high_coverage_fraction == 0
    assert record.welch_floor_respected
    assert record.coverage_tail_bound_respected


def test_aligned_pressure_has_large_excess_and_bad_coverage() -> None:
    record = audit_fusion_coverage(
        "ALIGNED-Q8-M32",
        _aligned_projectors(8, 32, 1),
    )
    assert record.redundancy == 4
    assert record.normalized_excess_fusion_potential > 1
    assert record.observed_low_coverage_fraction > 0.5
    assert record.welch_floor_respected
    assert record.coverage_tail_bound_respected


def test_random_projectors_respect_welch_and_tail_criterion() -> None:
    record = audit_fusion_coverage(
        "RANDOM-Q12-M48-R3",
        _random_projectors(12, 48, 3, 912),
    )
    assert record.welch_floor_respected
    assert record.normalized_excess_fusion_potential >= 0
    assert record.coverage_tail_bound_respected


def test_collision_free_pressure_forces_nonperturbative_overlap() -> None:
    records = [natural_coverage_pressure_target(n) for n in (24, 32, 40, 48)]
    assert records[-1].collision_free_redundancy_lower_bound_log2 > 80
    assert records[-1].forced_offdiagonal_over_trace_lower_bound_log2 > 80
    assert all(not record.raw_overlap_is_perturbative for record in records)
    assert all(not record.natural_tight_fusion_frame_proved for record in records)


def test_report_keeps_natural_fusion_potential_excess_open() -> None:
    report = run_coverage_welch_pressure()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["raw_interplane_overlap_must_be_large"]
    assert report.claim_gate[
        "fusion_potential_excess_is_correct_coverage_target"
    ]
    assert not report.claim_gate["support_pressure_implies_tight_coverage"]
    assert not report.claim_gate["natural_excess_fusion_potential_vanishes"]
    assert not report.claim_gate["natural_diagonal_coverage_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
