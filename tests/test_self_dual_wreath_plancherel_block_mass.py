from fractions import Fraction
import math

from representation_obstruction import hook_length_dimension
from self_dual_wreath_plancherel_block_mass import (
    audit_plancherel_stationarity,
    expected_normalized_target_isotypic_fraction,
    expected_normalized_target_multiplicity,
    invariant_mass_scaling_record,
    run_plancherel_block_mass,
)


def test_exact_target_stationarity_is_independent_of_block_size() -> None:
    n = 8
    target = (4, 2, 1, 1)
    dimension = hook_length_dimension(target)
    for block_size in (1, 2, 3, 5, 12):
        assert expected_normalized_target_multiplicity(
            n,
            block_size,
            target,
        ) == Fraction(dimension, math.factorial(n))
        assert expected_normalized_target_isotypic_fraction(
            n,
            block_size,
            target,
        ) == Fraction(dimension * dimension, math.factorial(n))


def test_trivial_and_sign_invariant_fractions_are_one_over_factorial() -> None:
    for n in range(3, 11):
        expected = Fraction(1, math.factorial(n))
        for target in ((n,), (1,) * n):
            record = audit_plancherel_stationarity(n, 8, target)
            assert record.expected_normalized_multiplicity == str(expected)
            assert record.expected_normalized_isotypic_fraction == str(expected)
            assert record.exact_stationarity_verified


def test_markov_scaling_remains_factorial_after_polynomial_inflation() -> None:
    record = invariant_mass_scaling_record(128, markov_polynomial_power=6)
    assert record.single_sector_high_probability_upper_bound_log2 < -500
    assert record.matched_sector_high_probability_upper_bound_log2 < -1200
    assert record.markov_failure_probability_upper_bound == 128**-6
    assert not record.inverse_polynomial_direct_postselection_proved


def test_report_separates_support_mass_and_complement_projection() -> None:
    report = run_plancherel_block_mass()
    metrics = report.headline_metrics
    assert metrics["exact_stationarity_failure_count"] == 0
    assert metrics["plancherel_tensor_stationarity_theorem_count"] == 1
    assert report.claim_gate[
        "plancherel_tensor_isotypic_stationarity_proved"
    ]
    assert report.claim_gate[
        "trivial_and_sign_expected_fraction_one_over_factorial_proved"
    ]
    assert not report.claim_gate[
        "sellke_support_implies_inverse_polynomial_mass"
    ]
    assert not report.claim_gate[
        "direct_common_core_postselection_inverse_polynomial"
    ]
    assert not report.claim_gate[
        "efficient_common_core_complement_projection_proved"
    ]
    assert not report.claim_gate["high_dimensional_target_measurement_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
