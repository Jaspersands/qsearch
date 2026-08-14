import pytest

from coset_hidden_involution_spherical_outlier_deflation import (
    audit_spherical_outlier_deflation,
    build_spherical_outlier_report,
    even_row_partitions,
    spherical_outlier_scaling_record,
    write_spherical_outlier_report,
)


@pytest.mark.parametrize("half_degree", (3, 4, 5))
def test_thrall_support_and_exact_candidate_mass_control(half_degree):
    control = audit_spherical_outlier_deflation(half_degree)
    assert control.thrall_dimension_identity_verified
    assert control.probability_bound_verified
    assert control.even_row_dimension_sum == control.matching_count
    assert control.exact_trimmed_even_row_probability <= (
        control.dimension_probability_upper_bound
    )
    assert control.dimension_probability_upper_bound <= (
        control.central_binomial_probability_upper_bound + 1e-12
    )


def test_even_row_partition_schema():
    assert even_row_partitions(3) == ((6,), (4, 2), (2, 2, 2))
    with pytest.raises(ValueError, match="positive"):
        even_row_partitions(0)


def test_all_register_spherical_mass_vanishes_at_scaling_width():
    rows = [spherical_outlier_scaling_record(m) for m in (8, 16, 32, 64, 128)]
    assert all(row.upper_bound_informative for row in rows)
    assert all(row.conjugate_outlier_span_qft_flag_available for row in rows)
    assert rows[-1].all_register_spherical_mass_log2_upper_bound < -100
    assert all(not row.post_deflation_frame_norm_bounded for row in rows)
    assert all(not row.all_subgroup_strata_classified for row in rows)
    with pytest.raises(ValueError, match="at least three"):
        spherical_outlier_scaling_record(2)


def test_report_deflates_only_hyperoctahedral_orbit(tmp_path):
    report = build_spherical_outlier_report(
        finite_half_degrees=(3, 4, 5),
        scaling_half_degrees=(8, 16, 32, 64, 128),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_conjugate_span_proved
    assert report.theorem.coherent_even_row_flag_available
    assert report.theorem.vanishing_all_register_mass_proved
    assert report.theorem.hyperoctahedral_outlier_orbit_deflated
    assert not report.theorem.all_subgroup_outliers_classified
    assert not report.theorem.post_deflation_frame_norm_bounded
    assert report.claim_gate["spherical_outlier_orbit_negligible_and_deflatable"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_spherical_outlier_report(
        tmp_path / "spherical-deflation.json",
        finite_half_degrees=(3, 4),
        scaling_half_degrees=(8, 16, 32, 64, 128),
    )
    assert payload["status"] == (
        "spherical-outlier-orbit-deflated-subgroup-hierarchy-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
