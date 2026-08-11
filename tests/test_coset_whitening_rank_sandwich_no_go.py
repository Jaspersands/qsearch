import pytest

from coset_whitening_rank_sandwich_no_go import (
    build_coset_whitening_rank_sandwich_report,
    finite_whitening_rank_control,
    maximum_irrep_dimension,
    multiplicity_rank_effective_lower_bound,
    whitening_rank_scaling_record,
    write_coset_whitening_rank_sandwich_report,
)


def test_maximum_dimension_and_effective_rank_formula():
    partition, dimension = maximum_irrep_dimension(5)
    assert dimension == 6
    assert sum(partition) == 5
    lower = multiplicity_rank_effective_lower_bound(5, 15, 3)
    assert lower == pytest.approx(15 / (6 * (1 + 14 / 8)))


def test_finite_natural_multiplicity_moment_obeys_rank_sandwich():
    for copy_count in (1, 2, 3):
        row = finite_whitening_rank_control(5, 2, copy_count)
        assert row.finite_sandwich_verified
        assert row.lower_bound_residual < 1e-10
        assert row.upper_bound_residual < 1e-10
        assert row.effective_rank_lower_bound <= (
            row.observed_average_multiplicity_rank_ratio + 1e-10
        )


def test_exact_scaling_rows_link_constant_pgm_success_to_rank_lower_bound():
    row = whitening_rank_scaling_record(32)
    assert row.pgm_success_lower_bound > 0.5
    assert row.exact_effective_rank_lower_bound > 2.0
    assert row.exact_source_inverse_rms_lower_bound > 1.0
    assert row.lower_below_upper


def test_scaling_rejects_non_even_degree():
    with pytest.raises(ValueError, match="even"):
        whitening_rank_scaling_record(9)


def test_report_closes_only_standalone_whitening(tmp_path):
    report = build_coset_whitening_rank_sandwich_report()
    assert report.theorem.theorem_verified
    assert report.theorem.exact_finite_group_lower_bound_proved
    assert report.theorem.maximal_dimension_theorem_applied
    assert report.theorem.exp_theta_sqrt_n_actual_moment_at_pgm_width_proved
    assert not report.theorem.polynomial_standalone_multiplicity_whitening_possible
    assert not report.theorem.fused_polar_isometry_ruled_out
    assert not report.theorem.alternative_collective_measurement_ruled_out
    assert not report.theorem.general_quantum_circuit_lower_bound_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_whitening_rank_sandwich_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "standalone-multiplicity-whitening-subexponential-no-go-fused-polar-open"
    )
