import pytest

from coset_hidden_involution_common_factor_trim import (
    audit_common_factor_trim,
    build_common_factor_trim_report,
    common_factor_parameters,
    common_factor_scaling_record,
    write_common_factor_trim_report,
)


@pytest.mark.parametrize(
    ("n", "transpositions", "common_dimension"),
    ((5, 1, 1), (5, 2, 2), (6, 3, 1)),
)
def test_exact_common_factor_rank_and_pair_overlap(
    n, transpositions, common_dimension
):
    control = audit_common_factor_trim(n, transpositions)
    assert control.exact_common_factor_decomposition_verified
    assert control.common_factor_dimension == common_dimension
    assert control.plus_projector_rank == control.group_order // 2
    assert control.trimmed_projector_rank == (
        control.plus_projector_rank - common_dimension
    )
    assert control.trimmed_distinct_pair_overlap_trace == (
        control.distinct_pair_overlap_trace - common_dimension
    )
    assert control.original_normalized_pair_overlap == 0.5
    assert control.trimmed_normalized_pair_overlap < 0.5
    assert control.trimmed_overlap_strictly_improved
    assert control.common_factor_qft_flag_available


def test_common_factor_parameters_validate_inputs():
    order, common, plus_rank, trimmed = common_factor_parameters(6, 3)
    assert order == 720
    assert common == 1
    assert plus_rank == 360
    assert trimmed == 359
    with pytest.raises(ValueError, match="invalid"):
        common_factor_parameters(4, 1)


def test_per_register_trim_loses_negligible_mass_and_preserves_flatness():
    rows = [common_factor_scaling_record(n) for n in (6, 8, 16, 32, 64, 128)]
    assert all(row.every_register_common_free for row in rows)
    assert all(row.trimmed_overlap_strictly_below_half for row in rows)
    assert all(
        2 * int(row.trimmed_overlap_numerator_decimal)
        < int(row.trimmed_overlap_denominator_decimal)
        for row in rows
    )
    assert rows[0].exact_retained_candidate_mass > 0.97
    assert all(row.exact_retained_candidate_mass > 0.99 for row in rows[1:])
    assert rows[0].candidate_mass_loss_upper_bound < 0.03
    assert all(row.candidate_mass_loss_upper_bound < 0.01 for row in rows[1:])
    assert all(row.retained_relative_flatness_mass_lower_bound > 0.9 for row in rows)
    assert all(not row.trimmed_operator_norm_bounded for row in rows)
    assert all(not row.trimmed_orbit_row_polar_compiled for row in rows)

    with pytest.raises(ValueError, match="even"):
        common_factor_scaling_record(7)


def test_report_removes_all_common_factors_not_remaining_spectrum(tmp_path):
    report = build_common_factor_trim_report(
        finite_specs=((5, 1), (5, 2), (6, 3)),
        scaling_n_values=(6, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_per_register_decomposition_proved
    assert report.theorem.coherent_common_factor_trim_available
    assert report.theorem.negligible_alternative_loss_proved
    assert report.theorem.trimmed_relative_flatness_proved
    assert report.theorem.all_common_factor_excitation_outliers_removed
    assert not report.theorem.trimmed_operator_norm_bound_proved
    assert not report.theorem.trimmed_orbit_row_polar_compiled
    assert report.claim_gate["per_register_common_factor_trim_compiled"]
    assert not report.claim_gate["common_free_operator_norm_bounded"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_common_factor_trim_report(
        tmp_path / "common-factor-trim.json",
        finite_specs=((5, 1), (6, 3)),
        scaling_n_values=(6, 8),
    )
    assert payload["status"] == (
        "per-register-common-factor-trim-compiled-common-free-polar-open"
    )
    assert payload["headline_metrics"]["trimmed_operator_norm_bound_count"] == 0
