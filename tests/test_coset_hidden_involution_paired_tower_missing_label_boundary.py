from fractions import Fraction

import pytest

from coset_hidden_involution_paired_tower_missing_label_boundary import (
    REPORT_PATH,
    audit_paired_tower_incidence,
    audit_plethysm_recurrence,
    bipartition_count,
    bipartitions,
    build_paired_tower_missing_label_report,
    down_incidence,
    harmonic_kernel_scaling_record,
    harmonic_residual,
    hyperoctahedral_branching_coefficient,
    plethystic_schur_power_sum,
    write_paired_tower_missing_label_report,
)


def test_symmetric_and_exterior_square_power_sum_expansions() -> None:
    assert plethystic_schur_power_sum(
        (1,), exterior_square=False
    ) == {(1, 1): Fraction(1, 2), (2,): Fraction(1, 2)}
    assert plethystic_schur_power_sum(
        (1,), exterior_square=True
    ) == {(1, 1): Fraction(1, 2), (2,): Fraction(-1, 2)}


@pytest.mark.parametrize("half_degree", (2, 3, 4, 5, 6, 8))
def test_bipartition_down_map_is_two_differential(half_degree: int) -> None:
    control = audit_paired_tower_incidence(half_degree)
    assert control.differential_poset_identity_verified
    assert control.full_row_rank_proved
    assert control.down_incidence_rank == control.lower_bipartition_count
    assert control.harmonic_nullity == (
        control.upper_bipartition_count - control.lower_bipartition_count
    )


def test_bipartition_counts_and_kernel_dimensions_match_closed_controls() -> None:
    assert [bipartition_count(rank) for rank in range(2, 7)] == [5, 10, 20, 36, 65]
    assert [
        harmonic_kernel_scaling_record(rank).harmonic_nullity
        for rank in (2, 3, 4, 5, 6)
    ] == [3, 5, 10, 16, 29]


def test_exact_plethysm_branching_contains_standard_plus_and_minus_parts() -> None:
    assert hyperoctahedral_branching_coefficient((7, 1), (3, 1), ()) == 1
    assert hyperoctahedral_branching_coefficient((7, 1), (3,), (1,)) == 1


@pytest.mark.parametrize("half_degree", (2, 3, 4))
def test_paired_tower_recurrence_and_dimensions_are_exact(half_degree: int) -> None:
    control = audit_plethysm_recurrence(half_degree)
    assert control.nonintegral_or_negative_coefficient_count == 0
    assert control.recurrence_failure_count == 0
    assert control.restriction_dimension_failure_count == 0
    assert control.exact_plethysm_recurrence_verified


@pytest.mark.parametrize("half_degree", (2, 3, 4))
def test_actual_restriction_vectors_use_the_harmonic_kernel(half_degree: int) -> None:
    control = audit_plethysm_recurrence(half_degree)
    assert control.irreps_with_zero_harmonic_residual == 0
    assert (
        control.irreps_with_nonzero_harmonic_residual
        == control.symmetric_partition_count
    )
    assert control.actual_branching_uses_harmonic_component


def test_harmonic_residual_is_annihilated_by_down_incidence() -> None:
    half_degree = 4
    vector = tuple(
        hyperoctahedral_branching_coefficient((7, 1), alpha, beta)
        for alpha, beta in bipartitions(half_degree)
    )
    residual, norm_squared = harmonic_residual(half_degree, vector)
    incidence = down_incidence(half_degree)
    assert norm_squared > 0
    assert all(
        sum(row[column] * residual[column] for column in range(len(residual))) == 0
        for row in incidence
    )


def test_scaling_kernel_is_large_but_not_promoted_to_hardness() -> None:
    row = harmonic_kernel_scaling_record(64)
    assert row.harmonic_nullity == 421_360_145
    assert row.harmonic_label_bits_lower_bound > 28
    assert not row.branching_recurrence_uniquely_determines_upper_vector


def test_report_kills_naive_recurrence_without_claiming_speedup() -> None:
    report = build_paired_tower_missing_label_report()
    assert report.headline_metrics["incidence_control_failure_count"] == 0
    assert report.headline_metrics["plethysm_recurrence_failure_count"] == 0
    assert report.claim_gate["exact_paired_branching_recurrence_proved"] is True
    assert report.claim_gate[
        "two_colour_differential_poset_underdetermination_proved"
    ] is True
    assert report.claim_gate["actual_branching_harmonic_component_verified"] is True
    assert report.claim_gate["natural_source_harmonic_mass_bounded"] is False
    assert report.claim_gate["paired_young_local_rotations_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_report_writer_materializes_research_artifact(tmp_path) -> None:
    output = tmp_path / REPORT_PATH.name
    payload = write_paired_tower_missing_label_report(output)
    assert output.exists()
    assert payload["status"] == (
        "paired-tower-recurrence-underdetermined-harmonic-plethysm-data-open"
    )
