from fractions import Fraction

from self_dual_wreath_star_channel_mass_typicality import (
    audit_annealed_star_carrier,
    audit_fixed_factor_multiplicity,
    carrier_power_sum,
    expected_normalized_star_row_rank,
    fourth_power_carrier_probability,
    run_star_channel_mass_typicality,
    star_channel_mass_scaling_record,
)


def test_fixed_target_factor_preserves_the_universal_variance_bound() -> None:
    record = audit_fixed_factor_multiplicity(
        7, 5, (4, 2, 1), (3, 2, 1, 1)
    )

    assert record.bound_respected
    assert Fraction(record.exact_relative_variance) >= 0


def test_annealed_star_row_has_the_fourth_power_carrier_law() -> None:
    row = expected_normalized_star_row_rank(6, (5, 1), (4, 2))
    expected = Fraction(5**4 * 9**4, 720**7)
    control = audit_annealed_star_carrier(
        6, (6,), (5, 1), (4, 2)
    )

    assert row == expected
    assert control.exact_carrier_law_normalized
    assert Fraction(control.correlation) == Fraction(1, 45)


def test_fourth_power_probabilities_and_correlation_second_moment_are_exact() -> None:
    n = 8
    probabilities = [
        fourth_power_carrier_probability(n, partition)
        for partition in __import__(
            "representation_obstruction"
        ).integer_partitions(n)
    ]
    z4 = carrier_power_sum(n, 4)

    assert sum(probabilities, Fraction()) == 1
    assert carrier_power_sum(n, 2) == __import__("math").factorial(n)
    assert z4 > carrier_power_sum(n, 3)


def test_high_correlation_rank_mass_becomes_tiny() -> None:
    early = star_channel_mass_scaling_record(16)
    late = star_channel_mass_scaling_record(48)

    assert late.fourth_power_low_dimension_mass < early.fourth_power_low_dimension_mass
    assert late.distorted_high_correlation_channel_mass_upper_bound < 1e-6
    assert late.fourth_power_rms_correlation_log2 < -100


def test_report_blocks_pgm_mass_transfer() -> None:
    report = run_star_channel_mass_typicality()

    assert report.claim_gate[
        "typical_triple_fourth_power_carrier_law_proved"
    ]
    assert report.claim_gate[
        "high_correlation_channel_rank_mass_factorially_small_proved"
    ]
    assert not report.claim_gate[
        "channel_rank_mass_equals_pgm_state_mass_proved"
    ]
    assert not report.claim_gate["natural_shorted_endpoint_comparability_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
