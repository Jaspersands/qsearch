import pytest

from self_dual_wreath_target_survival_surface_seed import (
    audit_power_boundary_all_depth_certificate,
    audit_power_boundary_lift,
    audit_presentation_lift,
    audit_surface_seed,
    covering_partitions,
    integer_partitions,
    run_target_survival_surface_seed,
    standard_handle_character_average,
    symmetric_group_irrep_dimension,
)


def test_surface_seed_is_exact_genus_two_with_handle_target():
    seed = audit_surface_seed()
    assert seed.exact_surface_seed_verified
    assert len(seed.remaining_generators) == 4
    assert seed.residual_orientable_genus == 2
    assert seed.symmetric_group_solution_exponent == 3
    assert seed.target_orientable_genus == 1
    assert seed.exact_S3_solution_count == 486
    assert seed.exact_S3_sign_character_average == 1
    assert seed.exact_S3_standard_normalized_character_average == 0.5


def test_identity_frame_lifts_preserve_exact_seed_distribution():
    for depth in range(7):
        control = audit_presentation_lift(depth)
        assert control.exact_seed_distribution_preserved
        assert control.remaining_generator_count == 4
        assert control.residual_orientable_genus == 2
        assert control.symmetric_group_solution_exponent == 3
        assert control.exact_S3_solution_count == 486
        assert control.exact_S3_standard_normalized_character_average == 0.5


def test_power_boundary_pruning_is_surface_group_with_one_free_generator():
    controls = [audit_power_boundary_lift(depth) for depth in range(1, 9)]
    assert all(row.exact_power_boundary_lift_classified for row in controls)
    assert all(len(row.remaining_generators) == 5 for row in controls)
    assert all(row.residual_orientable_genus == 2 for row in controls)
    assert all(row.symmetric_group_solution_exponent == 4 for row in controls)
    assert all(
        row.exact_surface_free_product_factorization_verified
        and row.exact_target_modulo_relator_verified
        for row in controls
    )
    assert all(row.exact_S3_solution_count == 2916 for row in controls)
    assert all(
        row.exact_S3_standard_normalized_character_average == 0.5
        for row in controls
    )
    assert all(
        later.integer_suffix_branch_certificate_margin
        < earlier.integer_suffix_branch_certificate_margin
        for earlier, later in zip(controls, controls[1:])
    )
    assert all(row.true_scalar_crossing_pressure_margin > 1 for row in controls)


def test_power_boundary_all_depth_reduction_uses_full_suffix_cube():
    certificate = audit_power_boundary_all_depth_certificate()
    assert certificate.different_support_formula == "{0000} x {0,1}^k"
    assert certificate.appended_generators_forced_to_identity
    assert certificate.projected_same_support_equals_base
    assert certificate.projected_different_support_equals_base
    assert certificate.base_remaining_generator_count == 5
    assert certificate.base_solution_exponent == 4
    assert certificate.base_exact_S3_solution_count == 2916
    assert certificate.base_surface_free_product_factorization_verified
    assert certificate.base_target_modulo_relator_verified
    assert certificate.checked_lifts_match_base
    assert certificate.universal_all_depth_reduction_verified


def test_partition_dimensions_and_cover_branching_are_exact():
    assert integer_partitions(5) == (
        (5,),
        (4, 1),
        (3, 2),
        (3, 1, 1),
        (2, 2, 1),
        (2, 1, 1, 1),
        (1, 1, 1, 1, 1),
    )
    assert [symmetric_group_irrep_dimension(row) for row in integer_partitions(5)] == [
        1,
        4,
        5,
        6,
        5,
        4,
        1,
    ]
    assert covering_partitions((3, 1)) == ((4, 1), (3, 2), (3, 1, 1))


def test_standard_handle_formula_matches_S3_and_decays_quadratically():
    assert standard_handle_character_average(3) == pytest.approx(0.5)
    values = [standard_handle_character_average(n) for n in range(8, 21)]
    assert all(later < earlier for earlier, later in zip(values, values[1:]))
    scaled = [n * n * standard_handle_character_average(n) for n in range(15, 31)]
    assert scaled[-1] < scaled[0]
    assert 2.0 < scaled[-1] < 2.3


def test_uniform_nonsign_character_bound_decays_from_witten_zeta_remainder():
    report = run_target_survival_surface_seed()
    rows = report.standard_character_scaling
    bounds = [row.uniform_nonsign_character_expectation_upper_bound for row in rows]
    assert all(
        later < earlier
        for earlier, later in zip(bounds[1:], bounds[2:])
    )
    assert all(
        row.normalized_standard_character_average
        <= row.uniform_nonsign_character_expectation_upper_bound
        for row in rows
    )
    assert bounds[-1] < 0.08


def test_report_blocks_the_identity_frame_natural_signal():
    report = run_target_survival_surface_seed()
    metrics = report.headline_metrics
    assert metrics["exact_genus_two_surface_seed_theorem_count"] == 1
    assert metrics["exact_identity_frame_presentation_lift_count"] == 7
    assert metrics["presentation_lift_failure_count"] == 0
    assert metrics["exact_power_boundary_lift_count"] == 8
    assert metrics["all_depth_power_boundary_reduction_theorem_count"] == 1
    assert metrics["power_boundary_lift_failure_count"] == 0
    assert metrics["minimum_power_boundary_true_pressure_margin"] > 1
    assert metrics["standard_character_quadratic_decay_theorem_count"] == 1
    assert metrics["uniform_nonsign_irrep_decay_theorem_count"] == 1
    assert report.claim_gate["identity_frame_lift_presentation_classified"]
    assert report.claim_gate["power_boundary_identity_lift_classified"]
    assert report.claim_gate["power_boundary_generic_certificate_gap_falsified"]
    assert not report.claim_gate[
        "power_boundary_actual_presentation_gap_falsified"
    ]
    assert report.claim_gate["natural_standard_target_average_exactly_reduced"]
    assert not report.claim_gate[
        "natural_standard_target_signal_asymptotically_nonzero"
    ]
    assert report.claim_gate["all_nontrivial_nonsign_seed_targets_vanish"]
    assert report.claim_gate["trivial_and_sign_seed_targets_equal_one"]
    assert not report.claim_gate["speedup_claim_allowed"]
