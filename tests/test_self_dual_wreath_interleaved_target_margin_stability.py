import math

import pytest

from self_dual_wreath_interleaved_target_margin_stability import (
    audit_target_margin_census,
    build_target_margin_stability_report,
    half_cube_boundary_margin,
    local_power_boundary_margin,
    nonidentity_target_margin,
    target_margin_scaling_record,
    write_target_margin_stability_report,
)


def test_nonidentity_margin_uses_augmented_same_support():
    margin, power, effective = nonidentity_target_margin(5, 15, 16)
    assert effective == 16
    assert power == 4
    assert margin == pytest.approx(local_power_boundary_margin(4))

    with pytest.raises(ValueError, match="nonidentity"):
        nonidentity_target_margin(5, 32, 16)
    with pytest.raises(ValueError, match="nonidentity"):
        nonidentity_target_margin(5, 16, 17)


def test_local_power_boundary_bound_holds_for_every_support_size_pair():
    width = 6
    half_cube_size = 1 << (width - 1)
    for same_size in range(1, half_cube_size + 1):
        for different_size in range(1, half_cube_size + 1):
            margin, power, _ = nonidentity_target_margin(
                width,
                same_size,
                different_size,
            )
            assert margin + 1e-12 >= local_power_boundary_margin(power)
            assert margin + 1e-12 >= half_cube_boundary_margin(width)


@pytest.mark.parametrize("width", range(1, 9))
def test_density_boundary_pair_is_unique_global_margin_minimizer(width):
    row = audit_target_margin_census(width)
    half_cube_size = 1 << (width - 1)
    predicted = (
        (1, 1)
        if width == 1
        else (half_cube_size - 1, half_cube_size)
    )
    assert row.exact_minimum_verified
    assert row.maximum_nonidentity_support_size == half_cube_size
    assert row.minimizing_support_size_pairs == (predicted,)
    assert row.minimum_exact_margin == pytest.approx(
        half_cube_boundary_margin(width)
    )
    assert row.local_power_boundary_failure_count == 0
    assert row.global_power_boundary_failure_count == 0


def test_half_log_width_margin_dominates_partition_prefactor():
    for degree in (1 << 16, 1 << 20, 1 << 24):
        row = target_margin_scaling_record(degree, 0.5)
        assert row.frame_position_count == math.floor(
            0.5 * math.log2(degree)
        )
        assert row.negative_log_relative_magnitude_lower_bound > 0
        assert row.relative_magnitude_log_upper_bound < 0
        assert row.partition_prefactor_dominated


def test_larger_width_is_left_open_when_generic_bound_loses():
    rows = [
        target_margin_scaling_record(degree, 0.65)
        for degree in (1 << 16, 1 << 20, 1 << 24)
    ]
    assert any(not row.partition_prefactor_dominated for row in rows)
    assert all(not row.finite_row_is_asymptotic_theorem for row in rows)


def test_report_closes_only_the_proved_width_schedule(tmp_path):
    report = build_target_margin_stability_report()
    assert len(report.dense_support_controls) == 10
    assert all(
        row.exact_target_collapse_verified
        and row.every_coordinate_has_support_edge
        and row.every_frame_generator_forced_to_identity
        and row.projected_target_is_marked_relator
        for row in report.dense_support_controls
    )
    assert all(
        row.dense_support_excludes_zero_same_cell
        for row in report.dense_support_controls
        if row.dense_support_kind == "same"
    )
    assert report.theorem.theorem_verified
    assert report.theorem.dense_support_target_collapse_proved
    assert report.theorem.half_cube_support_bound_proved
    assert report.theorem.exact_integer_margin_minimum_proved
    assert report.theorem.density_boundary_sharpness_proved
    assert report.theorem.sub_half_log_width_nonidentity_suppression_proved
    assert not report.theorem.all_growing_widths_suppressed
    assert not report.theorem.higher_multi_boundary_words_covered
    assert not report.claim_gate["dense_support_nonidentity_target_route_alive"]
    assert not report.claim_gate["sub_half_log_nonidentity_target_route_alive"]
    assert report.claim_gate["super_half_log_nonidentity_target_route_alive"]
    assert report.claim_gate["higher_multi_boundary_target_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_target_margin_stability_report(
        tmp_path / "target-margin.json"
    )
    assert payload["status"] == (
        "sub-half-log-interleaved-nonidentity-targets-suppressed"
    )
