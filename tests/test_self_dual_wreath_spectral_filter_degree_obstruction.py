import math

import pytest

from self_dual_wreath_spectral_filter_degree_obstruction import (
    eigenvalue_filter_degree_lower_bound,
    run_spectral_filter_degree_obstruction,
    singular_filter_degree_lower_bound,
    spectral_filter_degree_scaling_record,
)


def test_bernstein_bounds_have_expected_cutoff_exponents() -> None:
    threshold = 2**-40
    eigen = eigenvalue_filter_degree_lower_bound(threshold)
    singular = singular_filter_degree_lower_bound(threshold)
    eigen_shifted = eigenvalue_filter_degree_lower_bound(threshold / 16)
    singular_shifted = singular_filter_degree_lower_bound(threshold / 16)
    assert math.log2(eigen_shifted / eigen) == pytest.approx(4.0)
    assert math.log2(singular_shifted / singular) == pytest.approx(2.0)


def test_factorial_scaling_beats_every_declared_polynomial_benchmark() -> None:
    record = spectral_filter_degree_scaling_record(128)
    assert record.eigenvalue_encoding_superpolynomial
    assert record.singular_value_encoding_superpolynomial
    assert (
        record.eigenvalue_encoding_degree_lower_bound_log2
        > record.singular_value_encoding_degree_lower_bound_log2
        > record.polynomial_degree_benchmark_log2
    )


def test_report_closes_only_generic_qsvt_route() -> None:
    report = run_spectral_filter_degree_obstruction(
        n_values=(64, 96, 128, 192),
    )
    metrics = report.headline_metrics
    assert metrics["bounded_polynomial_bernstein_theorem_count"] == 1
    assert metrics["eigenvalue_encoding_superpolynomial_row_count"] == 4
    assert metrics["singular_value_encoding_superpolynomial_row_count"] == 4
    assert report.claim_gate[
        "generic_eigenvalue_polynomial_filter_superpolynomial"
    ]
    assert report.claim_gate[
        "generic_singular_value_polynomial_filter_superpolynomial"
    ]
    assert not report.claim_gate["normalization_one_qsvt_route_viable"]
    assert not report.claim_gate[
        "instance_specific_natural_spectral_gap_ruled_out"
    ]
    assert not report.claim_gate[
        "representation_structured_transform_ruled_out"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_filter_bounds_reject_invalid_cutoffs() -> None:
    with pytest.raises(ValueError):
        eigenvalue_filter_degree_lower_bound(0.0)
    with pytest.raises(ValueError):
        singular_filter_degree_lower_bound(0.6)
