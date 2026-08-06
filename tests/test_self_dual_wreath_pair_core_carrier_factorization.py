from fractions import Fraction

import pytest

from self_dual_wreath_pair_core_carrier_factorization import (
    _selected_star_controls,
    disjoint_pair_waist_bound,
    exact_star_overlap_spectrum,
    maximum_off_common_correlation,
    membership_pattern_blocks,
    off_common_star_bound,
    run_pair_core_carrier_factorization,
    screen_disjoint_waists,
    screen_star_law,
    star_channel_sectors_are_separated,
    validate_star_control,
)


D5_LABELS = (
    ((6,), (2, 2, 2)),
    ((5, 1), (4, 1, 1)),
    ((4, 2), (3, 1, 1, 1)),
    ((3, 3), (1, 1, 1, 1, 1, 1)),
)
D9_LABELS = (
    ((6,), (4, 2)),
    ((5, 1), (2, 2, 2)),
    ((3, 3), (2, 1, 1, 1, 1)),
    ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
)
D10_LABELS = (
    ((6,), (3, 1, 1, 1)),
    ((5, 1), (3, 3)),
    ((4, 2), (2, 2, 2)),
    ((4, 1, 1), (1, 1, 1, 1, 1, 1)),
)


def test_membership_blocks_are_complementary_and_hold_the_target() -> None:
    blocks = membership_pattern_blocks((6,), D5_LABELS, (14, 0, 7))

    assert (6,) in blocks[7]
    factors = [partition for group in blocks.values() for partition in group]
    assert len(factors) == 2 * len(D5_LABELS) + 1
    for index, (left, right) in enumerate(D5_LABELS):
        right_pattern = sum(
            1 << position
            for position, mask in enumerate((14, 0, 7))
            if mask & (1 << index)
        )
        assert right in blocks[right_pattern]
        assert left in blocks[7 ^ right_pattern]


def test_star_spectrum_is_a_reciprocal_carrier_product() -> None:
    rows = exact_star_overlap_spectrum((6,), D5_LABELS, 14, 0, 7)

    assert rows
    for row in rows:
        assert row.correlation == Fraction(
            1,
            row.cluster_carrier_dimension * row.companion_carrier_dimension,
        )
        assert row.multiplicity > 0
    assert maximum_off_common_correlation(rows) == Fraction(1, 5)
    assert star_channel_sectors_are_separated(rows)


def test_selected_carrier_five_nine_and_ten_stars_match_dense_spectra() -> None:
    controls = _selected_star_controls()

    assert [control.control_id for control in controls] == [
        "W6-OPEN-STAR-CARRIER-5",
        "W6-CLOSED-STAR-CARRIER-9",
        "W6-OPEN-STAR-CARRIER-10",
    ]
    assert all(control.verified for control in controls)
    assert all(control.predicted_rank == control.observed_rank for control in controls)
    assert all(
        control.maximum_spectrum_residual < 1e-12 for control in controls
    )
    assert [
        control.maximum_off_common_correlation for control in controls
    ] == pytest.approx([1 / 5, 1 / 9, 1 / 10])
    assert all(control.off_common_bound_respected for control in controls)


def test_off_common_bound_is_the_minimal_nontrivial_irrep_reciprocal() -> None:
    assert off_common_star_bound(5) == Fraction(1, 4)
    assert off_common_star_bound(12) == Fraction(1, 11)
    with pytest.raises(ValueError):
        off_common_star_bound(4)
    for n in (5, 6, 8, 16, 512):
        bound = off_common_star_bound(n)
        assert 4 * bound * bound <= bound


def test_repeated_source_labels_obey_the_same_closed_form() -> None:
    labels = (
        ((5,), (2, 1, 1, 1)),
        ((5,), (3, 2)),
        ((4, 1), (1, 1, 1, 1, 1)),
    )
    screen = screen_star_law(5, 3, 20_000, 6, repeated=True)

    assert screen.label_regime == "repeated-source-partitions"
    assert screen.audited_control_count > 0
    assert screen.validation_failure_count == 0
    assert screen.off_common_violation_count == 0
    assert screen.maximum_spectrum_residual < 1e-12
    # the closed form does not read label distinctness anywhere
    assert exact_star_overlap_spectrum((5,), labels, 0, 1, 2) is not None


def test_small_star_screen_reproduces_every_dense_singular_value() -> None:
    screen = screen_star_law(6, 4, 200_000, 12)

    assert screen.audited_control_count == 12
    assert screen.validation_failure_count == 0
    assert screen.off_common_violation_count == 0
    assert screen.maximum_spectrum_residual < 1e-12
    assert screen.maximum_off_common_correlation <= float(off_common_star_bound(6))
    assert screen.multi_isotype_channel_control_count == 0


def test_disjoint_pair_waist_bound_is_respected_and_finitely_tight() -> None:
    records = screen_disjoint_waists(6, 4, 200_000, 8)

    assert records
    assert all(record.bound_respected for record in records)
    assert all(record.bound_tight for record in records)
    with pytest.raises(ValueError):
        disjoint_pair_waist_bound((6,), D9_LABELS, (2, 5), (5, 12))


def test_star_law_needs_three_distinct_orientations() -> None:
    with pytest.raises(ValueError):
        exact_star_overlap_spectrum((6,), D10_LABELS, 14, 0, 14)


def test_report_proves_factorization_and_keeps_degree_gate_open() -> None:
    report = run_pair_core_carrier_factorization(
        s5_control_cap=4,
        s6_control_cap=6,
        repeated_control_cap=4,
        disjoint_control_cap=4,
    )

    assert report.claim_gate["star_carrier_factorization_proved"]
    assert report.claim_gate["off_common_star_bound_proved"]
    assert report.claim_gate["disjoint_waist_bound_proved"]
    assert not report.claim_gate["disjoint_pair_closed_form_proved"]
    assert not report.claim_gate["all_depth_multistar_conditioning_proved"]
    assert not report.claim_gate["coherent_recoupling_block_transform_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["screened_star_failure_count"] == 0
    assert report.headline_metrics["disjoint_waist_violation_count"] == 0
    assert report.headline_metrics["new_quantum_algorithm_count"] == 0
    assert all(
        row["carrier_factorization_proved"]
        and not row["multistar_weighted_degree_bounded"]
        for row in report.scaling_records
    )


def test_selected_control_ranks_are_the_carrier_dimensions() -> None:
    control = validate_star_control(
        "W6-OPEN-STAR-CARRIER-5-REPEAT",
        (6,),
        D5_LABELS,
        14,
        0,
        7,
    )

    assert control.predicted_rank == 5
    assert control.observed_rank == 5
    assert control.labels_are_distinct
    assert control.verified


def test_report_writer_can_skip_the_registry(tmp_path) -> None:
    from self_dual_wreath_pair_core_carrier_factorization import (
        write_pair_core_carrier_factorization_report,
    )

    path = tmp_path / "carrier.json"
    payload = write_pair_core_carrier_factorization_report(
        path=path,
        write_registry=False,
        s5_control_cap=4,
        s6_control_cap=4,
        repeated_control_cap=4,
        disjoint_control_cap=4,
    )

    assert path.exists()
    assert payload["claim_gate"]["speedup_claim_allowed"] is False
    assert payload["headline_metrics"]["screened_star_failure_count"] == 0

