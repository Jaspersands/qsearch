import math

import pytest

from coset_hidden_involution_natural_recoupling_boundary import (
    audit_coordinate_marginal,
    audit_hyperoctahedral_parity,
    build_natural_recoupling_boundary_report,
    hyperoctahedral_irrep_dimension,
    marginal_plancherel_total_variation,
    natural_recoupling_scaling_record,
    spherical_marginal_probabilities,
)


@pytest.mark.parametrize("copy_count", (1, 2))
def test_every_coordinate_is_a_repeated_H_spherical_module(copy_count: int) -> None:
    for coordinate in range(copy_count + 1):
        row = audit_coordinate_marginal(3, 1, copy_count, coordinate)
        assert row.minimum_coordinate_orbit_size == math.factorial(3) // 2
        assert row.maximum_coordinate_orbit_size == math.factorial(3) // 2
        assert row.coordinate_orbit_count == row.expected_coordinate_orbit_count
        assert row.marginal_probability_sum == pytest.approx(1.0)
        assert row.marginal_plancherel_total_variation <= row.theorem_total_variation_upper_bound
        assert row.induced_H_marginal_verified


def test_spherical_marginal_formula_is_exactly_normalized() -> None:
    probabilities = spherical_marginal_probabilities(6, 3)
    assert sum(probabilities.values()) == pytest.approx(1.0)
    assert all(probability >= 0 for probability in probabilities.values())
    assert marginal_plancherel_total_variation(6, 3) <= 1 / (2 * math.sqrt(15))


@pytest.mark.parametrize("half_degree", (2, 3, 4, 6, 8))
def test_hyperoctahedral_central_parities_split_regular_dimension(half_degree: int) -> None:
    row = audit_hyperoctahedral_parity(half_degree)
    assert row.even_central_parity_regular_dimension == row.group_order // 2
    assert row.odd_central_parity_regular_dimension == row.group_order // 2
    assert row.standard_plus_dimension == half_degree - 1
    assert row.standard_minus_dimension == half_degree
    assert row.parity_decomposition_verified


def test_bipartition_dimension_formula_handles_empty_sides() -> None:
    assert hyperoctahedral_irrep_dimension((4,), ()) == 1
    assert hyperoctahedral_irrep_dimension((), (4,)) == 1
    assert hyperoctahedral_irrep_dimension((3,), (1,)) == 4


def test_natural_scaling_becomes_jointly_plancherel_typical() -> None:
    earlier = natural_recoupling_scaling_record(8)
    later = natural_recoupling_scaling_record(32)
    assert later.retained_joint_typical_probability_lower_bound > 0.99
    assert later.retained_joint_typical_probability_lower_bound > earlier.retained_joint_typical_probability_lower_bound
    assert later.generic_projection_query_log2_lower_order > earlier.generic_projection_query_log2_lower_order
    assert later.actual_loop_parameter_log2 < later.published_partition_qft_loop_parameter_log2_lower_order
    assert later.exact_average_A_projection_probability == pytest.approx(
        1 / int(later.candidate_count_decimal)
    )
    assert not later.published_diagram_qft_regime_matches_natural_problem
    assert not later.source_aware_normalized_subduction_transform_compiled


def test_report_identifies_recoupling_without_claiming_normalized_access() -> None:
    report = build_natural_recoupling_boundary_report()
    assert report.headline_metrics["coordinate_marginal_control_failure_count"] == 0
    assert report.headline_metrics["hyperoctahedral_parity_control_failure_count"] == 0
    assert report.claim_gate["coordinate_marginals_plancherel_typical"] is True
    assert report.claim_gate["joint_even_carriers_macroscopic"] is True
    assert report.claim_gate["exact_natural_recoupling_target_identified"] is True
    assert report.claim_gate["known_qft_basis_changes_remove_sqrt_M_normalization"] is False
    assert report.claim_gate["published_diagram_qft_matches_natural_parameter_regime"] is False
    assert report.claim_gate["source_aware_normalized_subduction_transform_compiled"] is False
    assert report.claim_gate["binary_hidden_involution_detector_constructed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
