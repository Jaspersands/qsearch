import math
from fractions import Fraction

import pytest

from coset_hidden_involution_support_filter_no_go import (
    alternative_mean_eigenvalue,
    audit_support_spectrum_control,
    bounded_error_polynomial_degree_lower_bound,
    build_support_filter_no_go_report,
    exact_normalized_moments,
    support_filter_scaling_record,
    support_rank_fraction_upper_bound,
    write_support_filter_no_go_report,
)


def test_exact_moment_formulas_are_rational_and_consistent():
    first, second = exact_normalized_moments(15, 6)
    assert first == Fraction(1, 64)
    assert second == Fraction(15 + 64 - 1, 15 * 64 * 64)
    assert alternative_mean_eigenvalue(15, 6) == 64 * second

    with pytest.raises(ValueError, match="positive"):
        exact_normalized_moments(0, 2)
    with pytest.raises(ValueError, match="positive"):
        exact_normalized_moments(3, 0)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 1), (3, 1, 2), (4, 1, 2), (4, 2, 2)),
)
def test_dense_controls_verify_exact_moments_and_gap_bound(
    n, transpositions, copies
):
    row = audit_support_spectrum_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.trace_identity_residual < 1e-10
    assert row.second_moment_identity_residual < 1e-10
    assert row.effective_rank_bound_verified
    assert row.smallest_eigenvalue_bound_verified
    assert row.smallest_positive_eigenvalue <= (
        row.smallest_eigenvalue_upper_bound + 1e-9
    )


def test_useful_copy_count_forces_low_spectral_mass_scale():
    row = support_filter_scaling_record(16)
    assert row.copy_count == math.ceil(
        math.log2(4 * row.conjugacy_class_size)
    )
    assert row.support_rank_fraction_upper_bound <= 0.25
    assert row.low_spectrum_threshold <= 5 / row.conjugacy_class_size
    assert row.alternative_mass_below_threshold_lower_bound == 0.75
    assert row.polynomial_degree_lower_bound > row.copy_count
    assert not row.inverse_polynomial_spectral_filter_possible
    assert not row.arbitrary_structured_compiler_ruled_out


def test_polynomial_degree_lower_bound_scales_as_sqrt_class_size():
    rows = [support_filter_scaling_record(n) for n in (16, 32, 64, 128)]
    assert all(row.degree_over_sqrt_class_size > 0.09 for row in rows)
    assert all(row.degree_over_sqrt_class_size < 0.12 for row in rows)
    assert all(
        later.polynomial_degree_lower_bound
        > earlier.polynomial_degree_lower_bound
        for earlier, later in zip(rows, rows[1:])
    )

    with pytest.raises(ValueError, match="three-quarter"):
        bounded_error_polynomial_degree_lower_bound(15, 5)
    assert support_rank_fraction_upper_bound(15, 6) == Fraction(15, 64)


def test_report_blocks_only_generic_filter_and_preserves_structured_escape(
    tmp_path,
):
    report = build_support_filter_no_go_report(
        finite_specs=((3, 1, 1), (3, 1, 2), (4, 2, 2)),
        scaling_n_values=(16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.low_spectrum_mass_proved
    assert report.theorem.generic_qsvt_support_filter_ruled_out
    assert not report.theorem.arbitrary_circuit_lower_bound_proved
    assert not report.theorem.structured_support_compiler_constructed
    assert not report.claim_gate["source_conditioned_rescaling_refuted"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_support_filter_no_go_report(
        tmp_path / "support-filter.json",
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_n_values=(16, 32),
    )
    assert payload["status"] == (
        "generic-support-spectral-filter-refuted-structured-block-rescaling-open"
    )
