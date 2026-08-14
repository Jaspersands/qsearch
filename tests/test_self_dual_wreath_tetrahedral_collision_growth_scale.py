from fractions import Fraction

import pytest

from self_dual_wreath_parity_rank_profile_plancherel_mixing import class_power_sum
from self_dual_wreath_tetrahedral_collision_growth_scale import (
    analytic_remainder_bounds,
    audit_support_expansion,
    audit_tail_bounds,
    centralizer_order,
    falling_factorial,
    reciprocal_class_support_expansion,
    run_tetrahedral_collision_growth_scale,
    support_centralizer_power_sum,
    write_tetrahedral_collision_growth_scale_report,
)


def test_support_coefficients_match_first_fixed_point_free_cycle_types() -> None:
    assert support_centralizer_power_sum(2, 1) == 2
    assert support_centralizer_power_sum(3, 1) == 3
    assert support_centralizer_power_sum(4, 1) == 12
    assert support_centralizer_power_sum(2, 2) == 4
    assert support_centralizer_power_sum(3, 2) == 9
    assert centralizer_order((2, 2)) == 8
    assert falling_factorial(8, 3) == 8 * 7 * 6


def test_support_expansion_exactly_recovers_both_class_power_sums() -> None:
    for n in range(2, 13):
        for power in (1, 2):
            assert reciprocal_class_support_expansion(n, power) == class_power_sum(
                n, power
            )


def test_certified_tail_bounds_cover_exact_remainders() -> None:
    for n in (30, 36, 40):
        row = audit_tail_bounds(n)
        assert row.v_tail_bound_verified
        assert row.w_tail_bound_verified
        assert row.exact_v_remainder_after_support_three >= 0
        assert row.exact_w_remainder_after_support_two >= 0
        assert row.exact_v_remainder_after_support_three <= row.analytic_v_remainder_upper
        assert row.exact_w_remainder_after_support_two <= row.analytic_w_remainder_upper

    with pytest.raises(ValueError):
        analytic_remainder_bounds(29)


def test_scaled_exact_sums_approach_the_proved_leading_constants() -> None:
    rows = [audit_support_expansion(n) for n in (8, 12, 20, 30)]

    assert [row.n_squared_scaled_reciprocal_sum for row in rows] == sorted(
        (row.n_squared_scaled_reciprocal_sum for row in rows), reverse=True
    )
    assert rows[-1].n_squared_scaled_reciprocal_sum < 2.2
    assert rows[-1].n_fourth_scaled_inverse_square_sum < 4.4
    assert rows[-1].n_squared_scaled_reference_union_variance < 17.7
    assert all(row.exact_support_expansions_verified for row in rows)


def test_report_sharpens_target_without_claiming_collision_bound(tmp_path) -> None:
    report = run_tetrahedral_collision_growth_scale()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.theorem.transfer_condition_equivalent == "M_n=o(n^2)"
    assert report.claim_gate["reference_variance_asymptotic_scale_proved"]
    assert report.claim_gate[
        "physical_transfer_equivalent_to_subquadratic_collision_growth"
    ]
    assert not report.claim_gate["tetrahedral_collision_moment_subquadratic_proved"]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "collision-scale.json"
    payload = write_tetrahedral_collision_growth_scale_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
