from fractions import Fraction

import pytest

from dcp_subset_sum_cube_section_gap_theorem import (
    cube_section_gap_theorem,
    functional_control,
    integer_functional_census,
    log2_bad_contribution_upper_bound,
    logarithmic_moment_order,
    normalized_path_overhead,
    run_cube_section_gap_theorem,
    two_coordinate_boolean_hit_count,
    valid_boolean_functional_count,
)


def test_two_coordinate_square_has_at_most_three_boolean_hits() -> None:
    values = [Fraction(value, 3) for value in range(-6, 7)]
    for offset in values:
        for left in values:
            for right in values:
                if left == 0 or right == 0:
                    continue
                assert two_coordinate_boolean_hit_count(offset, left, right) <= 3


def test_rank_three_bound_is_sharp_and_contains_all_ones() -> None:
    control = functional_control((1, 1, -1))
    assert control.coefficient_sum == "1"
    assert control.valid_boolean_input_count == 6
    assert control.boolean_input_count == 8
    assert control.valid_fraction == pytest.approx(0.75)
    assert control.sharp_three_quarter_example
    assert control.three_quarter_bound_verified


def test_noncoordinate_functionals_obey_constant_gap() -> None:
    assert valid_boolean_functional_count((Fraction(1, 2), Fraction(1, 2))) == 2
    for rank in range(2, 7):
        census = integer_functional_census(rank, coefficient_radius=2)
        assert census.tested_noncoordinate_function_count > 0
        assert census.three_quarter_bound_failure_count == 0
        assert census.maximum_valid_fraction <= 0.75


def test_invalid_functional_contracts_are_rejected() -> None:
    with pytest.raises(ValueError, match="two coefficients"):
        valid_boolean_functional_count((1,))
    with pytest.raises(ValueError, match="sum one"):
        functional_control((1, 1))
    with pytest.raises(ValueError, match="must not be"):
        functional_control((1, 0))
    with pytest.raises(ValueError, match="nonzero"):
        two_coordinate_boolean_hit_count(0, 1, 0)


def test_constant_gap_closes_logarithmic_orders_asymptotically() -> None:
    multiplier = 2.0
    smaller = 1 << 32
    larger = 1 << 64
    small_order = logarithmic_moment_order(smaller, multiplier)
    large_order = logarithmic_moment_order(larger, multiplier)
    assert large_order == 2 * small_order
    assert normalized_path_overhead(
        larger, large_order
    ) < normalized_path_overhead(smaller, small_order)
    assert log2_bad_contribution_upper_bound(larger, large_order) < 0


def test_report_preserves_signed_and_geometric_escape_routes() -> None:
    theorem = cube_section_gap_theorem()
    assert theorem.constant_bad_state_contraction_proved
    assert theorem.all_logarithmic_nonnegative_moment_orders_closed
    assert not theorem.signed_statistics_closed
    assert not theorem.reduced_basis_geometry_closed
    assert not theorem.polynomial_subset_sum_solver_eliminated

    report = run_cube_section_gap_theorem(
        n_values=(1 << 24, 1 << 32),
        moment_order_multipliers=(0.5, 1.0, 2.0),
    )
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "proved_final_near_log_window_obstruction_count"
    ] == 1
    assert report.claim_gate["all_logarithmic_nonnegative_moment_orders_closed"]
    assert not report.claim_gate["signed_statistics_closed"]
    assert not report.claim_gate["joint_low_high_basis_geometry_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
