from fractions import Fraction

import pytest

from representation_obstruction import integer_partitions
from self_dual_wreath_sector_weight_concentration import (
    concentration_scaling_record,
    exhaustive_sector_weight_moments,
    generic_relative_variance_bound,
    portfolio_sector_weight,
    run_sector_weight_concentration,
    sector_weight_moment_record,
)


def test_fixed_portfolio_sector_weights_are_probabilities() -> None:
    source_pairs = (((3,), (2, 1)), ((2, 1), (1, 1, 1)))
    weights = [
        portfolio_sector_weight(3, target, source_pairs)
        for target in integer_partitions(3)
    ]

    assert all(weight >= 0 for weight in weights)
    assert sum(weights, Fraction()) == 1


@pytest.mark.parametrize("copy_count", [1, 2, 3])
@pytest.mark.parametrize("target", integer_partitions(3))
def test_exact_moment_formula_matches_exhaustive_iid_control(
    copy_count: int,
    target: tuple[int, ...],
) -> None:
    mean, variance = exhaustive_sector_weight_moments(
        3,
        target,
        copy_count,
    )
    record = sector_weight_moment_record(3, target, copy_count)

    assert mean == Fraction(record.exact_sector_weight_expectation)
    assert variance == Fraction(record.exact_sector_weight_variance)
    assert record.expectation_equals_plancherel
    assert record.exact_variance_bounded_by_generic


def test_generic_variance_bound_is_target_independent_and_valid() -> None:
    bound = generic_relative_variance_bound(5, 7)
    records = [
        sector_weight_moment_record(5, target, 7)
        for target in integer_partitions(5)
    ]

    assert bound > 0
    assert all(Fraction(record.exact_relative_variance) <= bound for record in records)
    assert all(record.generic_relative_variance_upper_bound == float(bound) for record in records)


def test_information_threshold_scaling_separates_without_sharp_class_bound() -> None:
    record = concentration_scaling_record(512)

    assert record.nonidentity_class_size_lower_bound == 2
    assert record.simultaneous_failure_bound_superpolynomial
    assert record.simultaneous_chebyshev_failure_log2_upper_bound < -1000
    assert record.filter_induced_total_variation_upper_bound < 1e-10
    assert record.sector_weight_only_fourier_success_lower_bound > 0.8
    assert not record.coherent_dual_row_extraction_proved
    assert not record.sector_schmidt_flattening_proved


def test_report_resolves_only_sector_weights() -> None:
    report = run_sector_weight_concentration()

    assert report.headline_metrics["exact_moment_failure_count"] == 0
    assert report.headline_metrics["brute_force_moment_control_verified"] == 1
    assert report.claim_gate["sector_weights_concentrate_around_plancherel"]
    assert report.claim_gate["coherent_fourier_sector_weight_condition_resolved"]
    assert not report.claim_gate["coherent_dual_row_extraction_proved"]
    assert not report.claim_gate["sector_schmidt_flattening_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_zero_copy_count_is_rejected() -> None:
    with pytest.raises(ValueError, match="copy count"):
        sector_weight_moment_record(3, (2, 1), 0)
