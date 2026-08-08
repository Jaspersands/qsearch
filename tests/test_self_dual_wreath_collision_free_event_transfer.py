import math

from self_dual_wreath_collision_free_event_transfer import (
    event_conditioning_bound,
    hierarchy_event_transfer_scaling_record,
    run_collision_free_event_transfer,
    stable_global_collision_free_probability,
)
from self_dual_wreath_global_collision_free_mass import (
    exact_global_collision_free_probability,
)


def test_event_conditioning_divides_failure_by_conditioning_mass() -> None:
    row = event_conditioning_bound(0.5, 100, 1e-5)

    assert math.isclose(row.unconditioned_union_failure_upper_bound, 1e-3)
    assert math.isclose(row.conditioned_union_failure_upper_bound, 2e-3)
    assert math.isclose(row.accepted_good_probability_lower_bound, 0.499)
    assert row.exact_event_transfer_inequality_verified


def test_stable_collision_probability_matches_exact_small_control() -> None:
    stable = stable_global_collision_free_probability(4, 2)
    exact = float(exact_global_collision_free_probability(4, 2))

    assert abs(stable - exact) < 1e-14


def test_full_hierarchy_cost_includes_every_node_and_target() -> None:
    row = hierarchy_event_transfer_scaling_record(20)
    leaves = int(row.orientation_leaf_count_decimal)
    nodes = int(row.hierarchy_node_target_count_upper_decimal)

    assert row.selected_copy_count == row.information_threshold_copy_count + 2
    assert nodes == 2 * leaves * row.target_count
    assert row.required_per_node_failure_upper_bound > 0
    assert row.log2_required_per_node_failure_upper_bound < -100
    assert row.event_level_conditioning_transfer_available
    assert not row.independent_uniform_spectral_event_proved


def test_conditioning_mass_cost_is_kept_in_finite_scaling_rows() -> None:
    early = hierarchy_event_transfer_scaling_record(20)
    late = hierarchy_event_transfer_scaling_record(48)

    assert 0 < early.global_distinct_probability < 1
    assert 0 < late.global_distinct_probability < 1
    assert late.global_distinct_probability > early.global_distinct_probability
    assert early.log2_global_distinct_probability < -100
    assert late.log2_global_distinct_probability < 0


def test_report_removes_mandatory_injective_gate_without_claiming_edge() -> None:
    report = run_collision_free_event_transfer()

    assert report.headline_metrics["generic_control_failure_count"] == 0
    assert report.claim_gate["event_level_collision_free_transfer_proved"]
    assert report.claim_gate["full_hierarchy_union_cost_quantified"]
    assert not report.claim_gate["injective_signed_moment_contraction_mandatory"]
    assert not report.claim_gate["independent_uniform_spectral_event_proved"]
    assert not report.claim_gate["globally_distinct_uniform_spectral_event_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
