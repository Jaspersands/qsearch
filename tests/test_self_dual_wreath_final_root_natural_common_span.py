from fractions import Fraction

import numpy as np
import pytest

from self_dual_wreath_final_root_natural_common_span import (
    asymptotic_final_root_corollary,
    audit_common_span_rank_bridge,
    final_root_natural_scaling_record,
    natural_aspect_bounds,
    run_final_root_natural_common_span,
)


def test_projector_control_saturates_common_span_rank_bridge() -> None:
    left = np.diag([1.0] * 8 + [0.0] * 4).astype(complex)
    right = np.diag([0.0] * 4 + [1.0] * 8).astype(complex)
    row = audit_common_span_rank_bridge("PROJECTOR-CONTROL", left, right)

    assert row.left_support_rank == 8
    assert row.right_support_rank == 8
    assert row.observed_common_span_dimension == 4
    assert row.observed_common_span_relative_rank == pytest.approx(1 / 3)
    assert row.cauchy_common_span_relative_lower_bound == pytest.approx(1 / 3)
    assert row.deterministic_rank_bridge_verified is True


def test_asymptotic_constants_are_exact() -> None:
    row = asymptotic_final_root_corollary()

    assert Fraction(row.conditioned_event_mass_lower_bound) == Fraction(1, 9)
    assert Fraction(row.common_span_relative_rank_lower_bound) == Fraction(19, 128)
    assert Fraction(row.common_fiber_to_coefficient_lower_bound) == Fraction(19, 520)
    assert Fraction(row.maximum_component_block_to_fiber_coefficient) == Fraction(520, 19)
    assert Fraction(row.conditional_defect_gap_limit_lower_bound) == Fraction(19, 1040)
    assert row.natural_component_positive_edge_proved is False


def test_rank_and_common_span_bounds_propagate_to_component_geometry() -> None:
    group_order = 1_000_000
    child_orientations = 3_000_000
    row = natural_aspect_bounds(
        group_order,
        child_orientations,
        relative_rank_tolerance=1 / 64,
        common_span_relative_rank_lower_bound=19 / 128,
    )

    assert row.child_orientation_aspect == pytest.approx(3.0)
    assert row.child_coefficient_to_carrier_lower_bound == pytest.approx(189 / 64)
    assert row.child_coefficient_to_carrier_upper_bound == pytest.approx(195 / 64)
    assert row.common_fiber_to_coefficient_lower_bound > 0.04
    assert row.maximum_component_block_to_fiber_upper_bound < 3e-5
    assert row.component_positive_edge_lower_bound > 0.02
    assert row.coordinate_defect_gap_lower_bound > 0.02


def test_finite_scaling_keeps_conditioning_and_edge_claims_separate() -> None:
    row = final_root_natural_scaling_record(16)

    assert 2.0 <= row.child_orientation_aspect < 4.0
    assert row.log2_conditioned_uniform_leaf_rank_failure_upper_bound < 0
    assert row.conditioned_bridge_event_mass_lower_bound > 0.1
    assert row.finite_positive_common_span_bound_certified is False
    assert row.natural_component_positive_edge_proved is False
    assert row.common_fiber_to_coefficient_lower_bound is None


def test_report_proves_dimensions_but_keeps_spectral_and_speedup_gates_closed() -> None:
    report = run_final_root_natural_common_span()

    assert report.status == (
        "natural-final-common-span-and-aspects-proved-component-edge-open"
    )
    assert report.claim_gate[
        "natural_final_common_span_has_constant_relative_rank_on_positive_mass"
    ] is True
    assert report.claim_gate[
        "natural_final_component_block_to_fiber_aspects_controlled_on_positive_mass"
    ] is True
    assert report.claim_gate["natural_final_component_positive_edge_proved"] is False
    assert report.claim_gate["natural_component_support_select_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
    assert report.headline_metrics[
        "natural_positive_mass_final_common_span_theorem_count"
    ] == 1


def test_invalid_common_span_premise_is_rejected() -> None:
    with pytest.raises(ValueError, match="common-span"):
        natural_aspect_bounds(16, 32, 0.1, 0.0)
