from fractions import Fraction

import numpy as np
import pytest

from self_dual_wreath_component_diagonal_leakage_bridge import (
    _haar_isometry,
    _mutually_unbiased_isometry,
    _uniform_scalar_isometry,
    audit_diagonal_leakage_bridge,
    component_diagonal_leakage_theorem,
    natural_diagonal_leakage_target,
    run_component_diagonal_leakage_bridge,
)


def test_uniform_scalar_control_is_sharp_but_crossing_cancels() -> None:
    isometry, blocks = _uniform_scalar_isometry(4, 5)
    row = audit_diagonal_leakage_bridge(
        "SCALAR",
        isometry,
        blocks,
        threshold=1 / 5,
    )
    assert row.exact_diagonal_leakage_bridge_verified
    assert row.effects_pairwise_commute
    assert row.normalized_total_noncrossing_moment == pytest.approx(1 / 25)
    assert row.normalized_rank_cauchy_floor == pytest.approx(1 / 25)
    assert row.normalized_diagonal_fourth_moment == pytest.approx(1 / 125)
    assert row.normalized_diagonal_leakage_upper_bound == pytest.approx(1 / 125)
    assert row.normalized_component_M4 == pytest.approx(0.0, abs=1e-12)
    assert row.normalized_bridge_lower_bound == pytest.approx(0.0, abs=1e-12)


def test_mutually_unbiased_control_attains_positive_bridge() -> None:
    isometry, blocks = _mutually_unbiased_isometry(7)
    row = audit_diagonal_leakage_bridge(
        "MUB",
        isometry,
        blocks,
        threshold=0.5,
    )
    assert row.exact_diagonal_leakage_bridge_verified
    assert not row.effects_pairwise_commute
    assert row.normalized_rank_cauchy_floor == pytest.approx(1 / 4)
    assert row.normalized_diagonal_leakage_upper_bound == pytest.approx(1 / 8)
    assert row.normalized_component_M4 == pytest.approx((1 - 1 / 7) / 8)
    assert row.normalized_bridge_lower_bound == pytest.approx(
        row.normalized_component_M4
    )


def test_trace_tail_bound_allows_exceptional_effect_eigenvalues() -> None:
    isometry = _haar_isometry(80, 13, seed=2711)
    row = audit_diagonal_leakage_bridge(
        "TAIL",
        isometry,
        (1,) * 80,
        threshold=0.15,
    )
    assert row.maximum_effect_eigenvalue > row.threshold
    assert row.bad_eigenvalue_trace_fraction > 0
    assert row.normalized_diagonal_fourth_moment <= (
        row.normalized_diagonal_leakage_upper_bound + 1e-10
    )
    assert row.exact_diagonal_leakage_bridge_verified


def test_rank_excess_or_nonpartitioned_blocks_are_rejected() -> None:
    isometry = np.eye(4, dtype=complex)
    with pytest.raises(ValueError, match="partition"):
        audit_diagonal_leakage_bridge(
            "BAD-PARTITION",
            isometry,
            (1, 1, 1),
            threshold=1.0,
        )


def test_natural_target_has_strict_but_unproved_margin() -> None:
    target = natural_diagonal_leakage_target()
    assert target.target_has_positive_margin
    assert target.critical_uniform_cap > 0.226
    assert Fraction(target.normalized_conditional_fiber_M4_lower_bound) > 0
    assert Fraction(target.normalized_expected_physical_M4_lower_bound) > 0
    assert not target.natural_diagonal_tail_proved
    assert not target.natural_distinct_crossing_bound_proved
    assert not target.natural_component_M4_positive


def test_theorem_replaces_full_jacobi_law_by_two_scalar_debts() -> None:
    theorem = component_diagonal_leakage_theorem()
    assert theorem.theorem_verified
    assert not theorem.full_jacobi_law_required
    assert "zeta" in theorem.threshold_tail_bound
    assert "chi" in theorem.component_M4_bridge


def test_report_keeps_natural_claim_gate_closed() -> None:
    report = run_component_diagonal_leakage_bridge()
    assert report.headline_metrics["diagonal_leakage_bridge_theorem_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["positive_bridge_control_count"] >= 1
    assert not report.claim_gate["natural_component_diagonal_tail_controlled"]
    assert not report.claim_gate["natural_distinct_crossing_pressure_controlled"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
