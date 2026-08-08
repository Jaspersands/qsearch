import math

import pytest

from self_dual_wreath_partial_support_source_mass_boundary import (
    exact_single_draw_low_dimension_probability,
    low_dimension_source_control,
    partial_support_source_mass_scaling_record,
    run_partial_support_source_mass_boundary,
)


def test_one_dimensional_plancherel_mass_is_exactly_two_over_factorial() -> None:
    for n in (3, 6, 10, 14):
        assert exact_single_draw_low_dimension_probability(n, 1) == pytest.approx(
            2 / math.factorial(n),
            abs=1e-16,
        )


def test_partition_count_low_dimension_bound_holds() -> None:
    for n, cutoff in ((6, 1), (8, 8), (10, 100), (12, 144)):
        control = low_dimension_source_control(n, cutoff)
        assert control.exact_probability_below_bound
        assert (
            control.exact_single_draw_low_dimension_probability
            <= control.partition_count_bound + 1e-15
        )


def test_collision_free_conditioned_bounds_decay_at_large_n() -> None:
    rows = [
        partial_support_source_mass_scaling_record(n)
        for n in (32, 40, 48)
    ]
    assert all(row.global_collision_free_probability > 0 for row in rows)
    assert all(
        right.log2_collision_free_conditioned_trivial_and_sign_upper_bound
        < left.log2_collision_free_conditioned_trivial_and_sign_upper_bound
        for left, right in zip(rows, rows[1:])
    )
    assert all(
        right.log2_collision_free_conditioned_any_polynomial_dimension_upper_bound
        < left.log2_collision_free_conditioned_any_polynomial_dimension_upper_bound
        for left, right in zip(rows[1:], rows[2:])
    )
    assert rows[-1].direct_s6_mechanism_conditioned_mass_superpolynomially_small
    assert rows[-1].polynomial_dimension_anchor_conditioned_mass_superpolynomially_small


def test_report_excludes_only_low_dimension_anchor_mechanisms() -> None:
    report = run_partial_support_source_mass_boundary()
    assert report.headline_metrics[
        "low_dimension_plancherel_counting_bound_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "direct_s6_trivial_sign_mass_boundary_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "polynomial_dimension_anchor_mass_boundary_theorem_count"
    ] == 1
    assert report.claim_gate[
        "direct_s6_low_dimension_mechanism_has_vanishing_natural_mass"
    ]
    assert report.claim_gate[
        "all_polynomial_dimension_anchor_mechanisms_have_vanishing_natural_mass"
    ]
    assert not report.claim_gate[
        "scalar_affine_behavior_holds_on_positive_native_bulk"
    ]
    assert not report.claim_gate[
        "high_dimension_matrix_partial_support_mass_controlled"
    ]
    assert not report.claim_gate["matrix_partial_support_gpe_compiler_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
