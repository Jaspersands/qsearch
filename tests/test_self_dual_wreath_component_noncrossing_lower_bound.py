from fractions import Fraction
from functools import lru_cache

import numpy as np

from self_dual_wreath_component_noncrossing_lower_bound import (
    _orthogonal_projective_isometry,
    _random_isometry,
    _uniform_scalar_isometry,
    audit_coordinate_compression_noncrossing,
    component_noncrossing_lower_bound_theorem,
    natural_noncrossing_corollary,
    run_component_noncrossing_lower_bound,
)


@lru_cache(maxsize=1)
def _report():
    return run_component_noncrossing_lower_bound()


def test_uniform_scalar_coordinate_compression_saturates_bound_and_commutes():
    isometry, blocks = _uniform_scalar_isometry(5, 7)
    row = audit_coordinate_compression_noncrossing("scalar", isometry, blocks)
    assert row.deterministic_chain_verified
    assert row.lower_bound_tight
    assert row.effects_pairwise_commute
    assert row.distinct_outcome_noncrossing_moment > 0
    assert abs(row.commutator_fourth_moment_gap) <= 1e-12
    np.testing.assert_allclose(
        row.observed_second_power_trace,
        5 / 7,
        atol=1e-12,
    )


def test_orthogonal_projective_coordinate_compression_saturates_bound():
    isometry, blocks = _orthogonal_projective_isometry(6, 2)
    row = audit_coordinate_compression_noncrossing("pvm", isometry, blocks)
    assert row.deterministic_chain_verified
    assert row.lower_bound_tight
    assert row.effects_pairwise_commute
    assert row.observed_noncrossing_fourth_moment == 12
    assert abs(row.distinct_outcome_noncrossing_moment) <= 1e-12
    assert abs(row.commutator_fourth_moment_gap) <= 1e-12


def test_random_unequal_coordinate_blocks_respect_rank_cauchy_chain():
    isometry = _random_isometry(37, 13, seed=1901)
    row = audit_coordinate_compression_noncrossing(
        "random",
        isometry,
        (2, 4, 6, 10, 15),
    )
    assert row.maximum_effect_rank_excess <= 0
    assert row.observed_second_power_trace >= 13**2 / 37 - 1e-12
    assert row.observed_noncrossing_fourth_moment >= 13**3 / 37**2 - 1e-12
    assert row.deterministic_chain_verified
    assert not row.effects_pairwise_commute


def test_natural_corollary_uses_existing_exact_aspect_constants():
    row = natural_noncrossing_corollary()
    assert Fraction(row.conditioned_source_event_mass_lower_bound) == Fraction(1, 9)
    assert Fraction(row.common_fiber_to_physical_carrier_lower_bound) == Fraction(
        19, 128
    )
    assert Fraction(row.common_fiber_to_child_coefficient_lower_bound) == Fraction(
        19, 520
    )
    assert Fraction(row.conditional_noncrossing_physical_mass_lower_bound) == Fraction(
        6859, 34_611_200
    )
    assert Fraction(row.expected_noncrossing_physical_mass_lower_bound) == Fraction(
        6859, 311_500_800
    )
    assert row.natural_noncrossing_lower_bound_proved
    assert not row.natural_distinct_outcome_noncrossing_lower_bound_proved
    assert not row.natural_crossing_upper_bound_proved
    assert not row.natural_component_M4_positive


def test_theorem_is_edge_free_but_does_not_claim_M4():
    theorem = component_noncrossing_lower_bound_theorem()
    assert theorem.arbitrary_block_dimensions
    assert theorem.arbitrary_coordinate_compression
    assert theorem.edge_free
    assert theorem.theorem_verified


def test_report_closes_total_scale_not_distinct_pair_gate():
    report = _report()
    assert report.headline_metrics[
        "coordinate_noncrossing_lower_bound_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "natural_noncrossing_lower_bound_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["sharp_commuting_control_count"] >= 2
    assert report.claim_gate[
        "natural_component_total_noncrossing_moment_lower_bounded"
    ]
    assert not report.claim_gate[
        "natural_component_distinct_noncrossing_moment_lower_bounded"
    ]
    assert not report.claim_gate["natural_normalized_crossing_moment_controlled"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
