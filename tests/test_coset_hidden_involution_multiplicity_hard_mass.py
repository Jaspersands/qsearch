from fractions import Fraction

import pytest

from coset_hidden_involution_multiplicity_hard_mass import (
    audit_multiplicity_mass_control,
    build_multiplicity_hard_mass_report,
    multiplicity_hard_mass_scaling_record,
    threshold_mass_lower_bound,
    transferred_expectation_upper_bound,
    write_multiplicity_hard_mass_report,
)


def test_expectation_transfer_and_markov_helpers():
    assert transferred_expectation_upper_bound(0.25, 1 / 9) == pytest.approx(
        13 / 36
    )
    assert threshold_mass_lower_bound(13 / 36, 0.5) == pytest.approx(5 / 18)
    assert transferred_expectation_upper_bound(0.8, 0.4) == 1.0
    assert threshold_mass_lower_bound(0.8, 0.5) == 0.0

    with pytest.raises(ValueError, match="null_expectation"):
        transferred_expectation_upper_bound(-0.1, 0.2)
    with pytest.raises(ValueError, match="total_variation"):
        transferred_expectation_upper_bound(0.2, 1.1)
    with pytest.raises(ValueError, match="threshold"):
        threshold_mass_lower_bound(0.2, 0.0)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 2), (3, 1, 3), (4, 2, 2)),
)
def test_finite_sector_laws_obey_transfer_and_markov(
    n, transpositions, copies
):
    row = audit_multiplicity_mass_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.expectation_transfer_residual < 1e-10
    assert row.markov_bound_residual < 1e-10
    assert row.alternative_average_support_fraction <= (
        row.expectation_transfer_upper_bound + 1e-10
    )
    assert row.observed_alternative_mass_at_or_below_threshold >= (
        row.markov_lower_bound - 1e-10
    )


def test_all_n_constant_proper_and_low_spectrum_mass():
    rows = [
        multiplicity_hard_mass_scaling_record(n)
        for n in (6, 8, 16, 32, 64, 128)
    ]
    uniform_half = float(Fraction(5, 18))
    uniform_intersection = float(Fraction(1, 36))
    assert all(
        row.support_null_mass_upper_bound <= 0.25 for row in rows
    )
    assert all(
        row.alternative_mass_in_half_support_sectors_lower_bound
        >= uniform_half
        for row in rows
    )
    assert all(
        row.simultaneous_half_support_and_low_spectrum_mass_lower_bound
        >= uniform_intersection
        for row in rows
    )
    assert all(
        row.low_spectrum_eigenvalue_upper_bound_times_class_size == 5.0
        for row in rows
    )
    assert all(not row.negligible_proper_sector_escape_possible for row in rows)
    assert all(not row.fused_multiplicity_transform_ruled_out for row in rows)

    with pytest.raises(ValueError, match="even"):
        multiplicity_hard_mass_scaling_record(7)


def test_report_blocks_exceptional_sector_escape_only(tmp_path):
    report = build_multiplicity_hard_mass_report(
        finite_specs=((3, 1, 2), (3, 1, 3)),
        scaling_n_values=(6, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.constant_proper_sector_mass_proved
    assert report.theorem.constant_proper_low_spectrum_intersection_proved
    assert report.theorem.negligible_exceptional_sector_escape_refuted
    assert not report.theorem.fused_multiplicity_transform_refuted
    assert not report.theorem.arbitrary_circuit_lower_bound_proved
    assert report.claim_gate[
        "constant_alternative_mass_simultaneously_proper_and_low_spectrum_proved"
    ]
    assert not report.claim_gate[
        "fused_multiplicity_support_transform_refuted"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_multiplicity_hard_mass_report(
        tmp_path / "multiplicity-hard-mass.json",
        finite_specs=((3, 1, 2),),
        scaling_n_values=(6, 8),
    )
    assert payload["status"] == (
        "constant-multiplicity-hard-mass-proved-fused-transform-open"
    )
    assert payload["headline_metrics"][
        "constant_proper_low_spectrum_intersection_theorem_count"
    ] == 1
