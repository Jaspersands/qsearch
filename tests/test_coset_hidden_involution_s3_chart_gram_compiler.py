import pytest

from coset_hidden_involution_s3_chart_gram_compiler import (
    audit_s3_chart_gram,
    build_s3_chart_gram_report,
    predicted_minimum_positive_eigenvalue,
    predicted_sector_eigenvalues,
    predicted_support_rank,
    s3_chart_scaling_record,
    write_s3_chart_gram_report,
)


def test_one_copy_sector_spectrum_matches_exact_s3_gram():
    spectrum = predicted_sector_eigenvalues(1)
    assert spectrum == pytest.approx((0.0, 0.0, 0.0, 0.0) + (1.5,) * 4 + (3.0,))
    assert predicted_support_rank(1) == 5
    assert predicted_minimum_positive_eigenvalue(1) == 1.5


@pytest.mark.parametrize("copy_count", (1, 2, 3, 4))
def test_exact_defect_weight_spectrum_and_rank(copy_count):
    control = audit_s3_chart_gram(copy_count)
    assert control.exact_sector_diagonalization_verified
    assert control.observed_source_gram_rank == predicted_support_rank(copy_count)
    assert control.observed_kernel_dimension == 2 * (copy_count + 1)
    assert control.maximum_predicted_spectrum_residual < 1e-9
    assert control.gram_connection_commutator_norm < 1e-9
    assert control.maximum_gram_eigenvalue == pytest.approx(3.0)
    assert control.synthesis_condition_number <= 2.0 + 1e-9


def test_chart_conditioning_stays_constant_but_global_compiler_is_open():
    rows = [s3_chart_scaling_record(k) for k in (1, 2, 8, 32, 128)]
    assert rows[0].minimum_positive_gram_eigenvalue == 1.5
    assert all(row.minimum_positive_gram_eigenvalue == 0.75 for row in rows[1:])
    assert all(row.synthesis_condition_number <= 2.0 for row in rows)
    assert all(row.chart_polar_polynomial_in_copy_count for row in rows)
    assert all(not row.full_class_polar_compiled for row in rows)
    assert rows[-1].kernel_fraction < rows[1].kernel_fraction
    assert rows[-1].holonomy_fixed_alternative_mass == pytest.approx(1 / 6)
    assert rows[-1].low_connection_sector_alternative_mass == pytest.approx(
        1 / 2
    )

    with pytest.raises(ValueError, match="positive"):
        s3_chart_scaling_record(0)
    with pytest.raises(ValueError, match="positive"):
        predicted_sector_eigenvalues(0)
    with pytest.raises(ValueError, match="positive"):
        predicted_support_rank(0)
    with pytest.raises(ValueError, match="positive"):
        predicted_minimum_positive_eigenvalue(0)


def test_report_compiles_only_the_three_branch_chart(tmp_path):
    report = build_s3_chart_gram_report(
        finite_copy_counts=(1, 2, 3),
        scaling_copy_counts=(1, 2, 8, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_sector_spectrum_proved
    assert report.theorem.exact_rank_formula_proved
    assert report.theorem.constant_conditioning_proved
    assert report.theorem.polynomial_three_branch_chart_polar_compiled
    assert not report.theorem.full_conjugacy_class_polar_compiled
    assert not report.theorem.branch_label_erasure_compiled
    assert not report.theorem.hidden_involution_algorithm_constructed
    assert report.claim_gate[
        "nonflat_holonomy_compatible_with_constant_conditioning"
    ]
    assert not report.claim_gate["matching_association_scheme_transform_compiled"]
    assert not report.claim_gate["full_orbit_synthesis_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_s3_chart_gram_report(
        tmp_path / "s3-chart.json",
        finite_copy_counts=(1, 2),
        scaling_copy_counts=(1, 2, 8),
    )
    assert payload["status"] == (
        "s3-chart-polar-compiled-global-chart-gluing-open"
    )
    assert payload["headline_metrics"][
        "polynomial_three_branch_chart_compiler_count"
    ] == 1
