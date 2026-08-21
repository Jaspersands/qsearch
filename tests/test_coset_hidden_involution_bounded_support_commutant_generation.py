import math

import pytest

from coset_hidden_involution_bounded_support_commutant_generation import (
    REPORT_PATH,
    audit_bounded_support_commutant,
    build_bounded_support_commutant_report,
    exact_branching_commutant_dimension,
    hermitian_bounded_support_orbits,
    hyperoctahedral_group,
    moved_point_support,
    write_bounded_support_commutant_report,
)
from representation_obstruction import integer_partitions


def test_hyperoctahedral_group_has_the_expected_order() -> None:
    for half_degree in range(2, 5):
        group = hyperoctahedral_group(half_degree)
        assert len(group) == 2**half_degree * math.factorial(half_degree)
        assert len(set(group)) == len(group)


def test_hermitian_orbit_inventory_is_exact_at_S8() -> None:
    assert [
        len(hermitian_bounded_support_orbits(4, cutoff))
        for cutoff in (0, 2, 3, 4)
    ] == [1, 3, 5, 15]
    for orbit in hermitian_bounded_support_orbits(4, 4):
        assert {moved_point_support(element) for element in orbit} == {
            moved_point_support(orbit[0])
        }
        assert {tuple(element.index(index) for index in range(8)) for element in orbit} == set(orbit)


@pytest.mark.parametrize(
    ("partition", "expected_dimension", "expected_blocks", "expected_maximum"),
    (
        ((4, 2, 2), 14, 11, 2),
        ((5, 2, 1), 14, 11, 2),
        ((4, 3, 1), 16, 13, 2),
        ((4, 2, 1, 1), 26, 11, 2),
    ),
)
def test_exact_commutant_dimensions_match_plethysm(
    partition: tuple[int, ...],
    expected_dimension: int,
    expected_blocks: int,
    expected_maximum: int,
) -> None:
    blocks, dimension, maximum, repeated = exact_branching_commutant_dimension(
        partition,
        4,
    )
    assert dimension == expected_dimension
    assert blocks == expected_blocks
    assert maximum == expected_maximum
    assert repeated > 0


@pytest.mark.parametrize(
    "partition",
    ((4, 2, 2), (3, 3, 1, 1), (5, 2, 1), (4, 3, 1), (3, 2, 2, 1), (4, 2, 1, 1)),
)
def test_support_four_first_closes_every_repeated_S8_commutant(
    partition: tuple[int, ...],
) -> None:
    control = audit_bounded_support_commutant(partition)
    dimensions = {
        step.maximum_moved_points: step.generated_algebra_dimension_tolerance_1e8
        for step in control.support_steps
    }
    assert dimensions[2] < control.exact_commutant_dimension
    assert dimensions[3] < control.exact_commutant_dimension
    assert dimensions[4] == control.exact_commutant_dimension
    assert all(step.dimension_stable for step in control.support_steps)
    assert control.support_four_generates_full_commutant
    assert control.maximum_K_generator_commutator_residual < 1e-9
    assert control.maximum_character_trace_residual < 1e-9


def test_support_four_generates_every_S8_irrep_commutant() -> None:
    controls = [
        audit_bounded_support_commutant(partition)
        for partition in integer_partitions(8)
    ]
    assert len(controls) == 22
    assert all(row.support_four_generates_full_commutant for row in controls)
    assert sum(row.repeated_branch_count > 0 for row in controls) == 7


def test_report_promotes_mechanism_without_promoting_speedup() -> None:
    report = build_bounded_support_commutant_report()
    assert report.headline_metrics["S8_irrep_control_count"] == 22
    assert report.headline_metrics["S8_support_four_full_commutant_count"] == 22
    assert report.headline_metrics["S8_repeated_branch_irrep_count"] == 7
    assert report.headline_metrics["S8_repeated_support_two_full_count"] == 0
    assert report.headline_metrics["S8_repeated_support_three_full_count"] == 0
    assert report.headline_metrics["S8_repeated_support_four_full_count"] == 7
    assert report.claim_gate["exact_orbit_sum_commutant_identity_proved"] is True
    assert report.claim_gate[
        "all_S8_irrep_commutants_generated_by_support_four"
    ] is True
    assert report.claim_gate["uniform_all_rank_generation_proved"] is False
    assert report.claim_gate["inverse_polynomial_spectral_gap_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_report_writer_materializes_research_artifact(tmp_path) -> None:
    output = tmp_path / REPORT_PATH.name
    payload = write_bounded_support_commutant_report(output)
    assert output.exists()
    assert payload["status"] == (
        "bounded-support-four-generates-all-S8-hyperoctahedral-commutants-uniform-theorem-open"
    )
