import math

import pytest

from coset_hidden_involution_colour_resolved_paired_tower_boundary import (
    REPORT_PATH,
    audit_colour_resolved_kernel,
    audit_colour_resolved_plethysm,
    build_colour_resolved_paired_tower_report,
    colour_down_incidence,
    joint_primitive_dimension,
    joint_primitive_scaling_record,
    two_box_strip_indicators,
    write_colour_resolved_paired_tower_report,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    down_incidence,
)


def test_colour_down_maps_sum_to_the_unsplit_down_map() -> None:
    alpha, beta = colour_down_incidence(6)
    unsplit = down_incidence(6)
    assert tuple(
        tuple(a + b for a, b in zip(alpha_row, beta_row))
        for alpha_row, beta_row in zip(alpha, beta)
    ) == unsplit


def test_two_box_strip_indicators_resolve_path_multiplicity() -> None:
    assert two_box_strip_indicators((4, 2), (3, 1)) == (1, 1)
    assert two_box_strip_indicators((4, 2), (2, 2)) == (1, 0)
    assert two_box_strip_indicators((2, 2), (1, 1)) == (0, 1)


@pytest.mark.parametrize(
    ("half_degree", "expected_nullity"),
    ((2, 2), (3, 2), (4, 5), (5, 6), (6, 13), (8, 30), (10, 66)),
)
def test_colour_resolved_map_has_exact_joint_primitive_kernel(
    half_degree: int,
    expected_nullity: int,
) -> None:
    control = audit_colour_resolved_kernel(half_degree)
    assert control.stacked_rank_formula_verified
    assert control.joint_primitive_nullity == expected_nullity
    assert control.joint_primitive_nullity == control.primitive_convolution_count
    assert not control.colour_resolved_recurrence_is_injective


def test_joint_primitive_second_difference_formula() -> None:
    assert [joint_primitive_dimension(rank) for rank in range(2, 9)] == [
        2,
        2,
        5,
        6,
        13,
        16,
        30,
    ]


@pytest.mark.parametrize("half_degree", (2, 3, 4, 5, 6))
def test_horizontal_and_vertical_plethysm_recurrences_are_exact(
    half_degree: int,
) -> None:
    control = audit_colour_resolved_plethysm(half_degree)
    assert control.horizontal_recurrence_failure_count == 0
    assert control.vertical_recurrence_failure_count == 0
    assert control.split_recurrence_verified


def test_controlled_source_mass_really_uses_joint_primitives() -> None:
    controls = [audit_colour_resolved_plethysm(rank) for rank in range(2, 7)]
    assert [row.exact_spherical_source_mass for row in controls] == [
        "1",
        "31/40",
        "251/315",
        "1",
        "1901/1925",
    ]
    assert all(row.controlled_source_uses_joint_primitive_space for row in controls)


def test_joint_primitive_fraction_tracks_partition_asymptotic() -> None:
    rows = [joint_primitive_scaling_record(rank) for rank in (32, 64, 128)]
    assert rows[-1].joint_primitive_dimension == 3_083_028_152_791
    assert rows[-1].primitive_label_bits > 41
    assert rows[-1].joint_primitive_fraction < rows[0].joint_primitive_fraction
    assert rows[-1].half_degree_times_primitive_fraction > 2.4
    assert rows[-1].half_degree_times_primitive_fraction < math.pi**2 / 3


def test_report_preserves_the_source_mass_and_circuit_boundaries() -> None:
    report = build_colour_resolved_paired_tower_report()
    assert report.headline_metrics["kernel_control_failure_count"] == 0
    assert report.headline_metrics["split_recurrence_failure_count"] == 0
    assert report.headline_metrics["minimum_controlled_source_primitive_occupancy"] == pytest.approx(31 / 40)
    assert report.claim_gate["colour_resolved_split_recurrence_proved"] is True
    assert report.claim_gate["exact_joint_primitive_kernel_proved"] is True
    assert report.claim_gate[
        "asymptotic_natural_source_primitive_mass_bounded"
    ] is False
    assert report.claim_gate["primitive_commutant_generators_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_report_writer_materializes_research_artifact(tmp_path) -> None:
    output = tmp_path / REPORT_PATH.name
    payload = write_colour_resolved_paired_tower_report(output)
    assert output.exists()
    assert payload["status"] == (
        "last-pair-colour-resolution-insufficient-joint-primitive-data-open"
    )
