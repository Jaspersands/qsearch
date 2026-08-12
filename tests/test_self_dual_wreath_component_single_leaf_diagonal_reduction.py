from fractions import Fraction

import pytest

from self_dual_wreath_component_single_leaf_diagonal_reduction import (
    audit_source_flip_diagonal_orbit,
    run_component_single_leaf_diagonal_reduction,
    single_leaf_diagonal_budget,
    single_leaf_diagonal_reduction_theorem,
)


def test_repeated_source_orbit_reduces_diagonal_sum_to_one_leaf() -> None:
    standard = (2, 1)
    row = audit_source_flip_diagonal_orbit(
        "REPEATED",
        (3,),
        ((standard, standard),) * 3,
    )
    assert row.exact_single_leaf_diagonal_orbit_reduction_verified
    assert row.child_leaf_count == 4
    assert row.source_flip_count == 4
    assert row.maximum_flip_covariance_residual < 1e-10
    assert row.annealed_single_leaf_identity_residual < 1e-10


def test_nonidentical_source_block_uses_orbit_average_not_blockwise_equality() -> None:
    standard = (2, 1)
    row = audit_source_flip_diagonal_orbit(
        "NONIDENTICAL",
        standard,
        (
            ((3,), standard),
            ((3,), standard),
            (standard, (1, 1, 1)),
        ),
    )
    assert row.exact_single_leaf_diagonal_orbit_reduction_verified
    assert row.common_fiber_dimension_orbit_range == 0
    assert row.annealed_single_leaf_identity_residual < 1e-10


def test_single_source_pair_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least two"):
        audit_source_flip_diagonal_orbit(
            "TOO-SMALL",
            (3,),
            (((3,), (1, 1, 1)),),
        )


def test_budget_partitions_optimized_physical_floor() -> None:
    row = single_leaf_diagonal_budget()
    assert Fraction(row.optimized_physical_total_noncrossing_floor) == Fraction(
        1, 4096
    )
    assert Fraction(row.proposed_physical_diagonal_budget) == Fraction(1, 8192)
    assert Fraction(row.proposed_physical_distinct_crossing_budget) == Fraction(
        1, 16_384
    )
    assert Fraction(row.resulting_physical_component_M4_margin) == Fraction(
        1, 16_384
    )
    assert row.budget_has_positive_margin
    assert not row.natural_fixed_leaf_green_moment_bound_proved
    assert not row.natural_component_M4_positive


def test_theorem_requires_only_law_level_flip_invariance() -> None:
    theorem = single_leaf_diagonal_reduction_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_flip_invariant_source_law
    assert theorem.arbitrary_flip_invariant_event
    assert not theorem.uniform_outcome_bound_required
    assert "Tr(H_0^4)" in theorem.fixed_leaf_green_word


def test_report_keeps_natural_moment_and_speedup_gates_closed() -> None:
    report = run_component_single_leaf_diagonal_reduction()
    assert report.headline_metrics[
        "single_leaf_diagonal_orbit_reduction_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "annealed_diagonal_sum_reduced_to_one_fixed_leaf"
    ]
    assert not report.claim_gate[
        "natural_fixed_leaf_fourth_green_moment_controlled"
    ]
    assert not report.claim_gate["natural_distinct_crossing_pressure_controlled"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
