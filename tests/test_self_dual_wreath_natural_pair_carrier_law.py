from fractions import Fraction
import math

from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_natural_pair_carrier_law import (
    carrier_power_sum,
    exact_annealed_pair_carrier_control,
    expected_pair_carrier_relative_mass,
    natural_pair_carrier_scaling_record,
    pair_schatten_moment_expectation,
    run_natural_pair_carrier_law,
)


def test_exact_annealed_carrier_mass_matches_fourth_power_law() -> None:
    n = 4
    target = (3, 1)
    control = exact_annealed_pair_carrier_control(n, target)
    assert control.maximum_exact_carrier_mass_residual == "0"
    assert control.exact_fourth_power_carrier_law_verified
    assert control.exact_schatten_moments_verified
    order = math.factorial(n)
    for carrier in integer_partitions(n):
        dimension = hook_length_dimension(carrier)
        assert expected_pair_carrier_relative_mass(n, carrier) == Fraction(
            dimension**4,
            order**3,
        )


def test_exact_pair_schatten_moment_identities() -> None:
    for n in range(3, 9):
        order = math.factorial(n)
        partition_count = len(integer_partitions(n))
        assert pair_schatten_moment_expectation(n, 0) == (
            carrier_power_sum(n, 4) / order**3
        )
        assert pair_schatten_moment_expectation(n, 1) == Fraction(1, order**2)
        assert pair_schatten_moment_expectation(n, 2) == Fraction(
            partition_count,
            order**3,
        )


def test_fourth_power_low_dimension_and_rms_bounds_hold() -> None:
    for n in (8, 12, 16, 20):
        record = natural_pair_carrier_scaling_record(n)
        assert record.quadratic_dimension_mass_log2 <= (
            record.quadratic_dimension_mass_theorem_upper_bound_log2 + 1e-12
        )
        assert record.fourth_power_rms_correlation_log2 <= (
            (math.log2(record.partition_count) - math.log2(math.factorial(n))) / 2
            + 1e-12
        )


def test_quenched_carrier_law_bound_improves_with_n() -> None:
    records = [natural_pair_carrier_scaling_record(n) for n in (8, 12, 16, 20)]
    assert all(record.carrier_law_concentration_certified for record in records)
    assert all(
        right.expected_weighted_l1_error_upper_bound
        < left.expected_weighted_l1_error_upper_bound
        for left, right in zip(records, records[1:])
    )


def test_report_keeps_higher_incidence_and_speedup_gates_closed() -> None:
    report = run_natural_pair_carrier_law()
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.claim_gate[
        "exact_annealed_fourth_power_pair_carrier_law_proved"
    ]
    assert report.claim_gate[
        "quenched_pair_carrier_total_variation_convergence_proved"
    ]
    assert report.claim_gate[
        "conditional_active_pair_native_mass_transfer_proved"
    ]
    assert not report.claim_gate[
        "complete_many_orientation_pgm_mass_transfer_proved"
    ]
    assert not report.claim_gate["coherent_triangle_cycle_incidence_controlled"]
    assert not report.claim_gate["natural_complete_node_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
