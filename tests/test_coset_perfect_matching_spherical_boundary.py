import math

from coset_perfect_matching_spherical_boundary import (
    audit_perfect_matching_character,
    brauer_regular_dimension,
    brauer_regular_sector_count,
    fixed_perfect_matching_count,
    perfect_matching_count,
    run_perfect_matching_spherical_boundary,
)
from representation_obstruction import integer_partitions


def test_fixed_matching_character_has_exact_identity_and_small_controls():
    assert fixed_perfect_matching_count((1, 1, 1, 1, 1, 1)) == 15
    assert fixed_perfect_matching_count((6,)) == 1
    assert fixed_perfect_matching_count((3, 3)) == 3
    assert fixed_perfect_matching_count((3, 1, 1, 1)) == 0


def test_thrall_even_row_decomposition_is_exact_through_degree_fourteen():
    for half_degree in range(1, 8):
        row = audit_perfect_matching_character(half_degree)
        assert row.exact_thrall_decomposition_verified
        assert row.maximum_constituent_multiplicity == 1
        assert row.permutation_character_inner_product_sector_count == len(
            integer_partitions(half_degree)
        )
        assert row.constituent_dimension_sum == perfect_matching_count(half_degree)
        assert (
            row.symmetric_group_order
            // row.hyperoctahedral_stabilizer_order
            == row.perfect_matching_count
        )


def test_brauer_regular_dimension_matches_basis_but_sector_profile_does_not():
    for diagram_order in range(1, 9):
        assert brauer_regular_dimension(diagram_order) == perfect_matching_count(
            diagram_order
        )
    for diagram_order in range(2, 9):
        assert brauer_regular_sector_count(diagram_order) > len(
            integer_partitions(diagram_order)
        )


def test_scaling_records_resolve_basis_sampling_not_row_verification():
    report = run_perfect_matching_spherical_boundary()
    for row in report.scaling_records:
        assert row.efficient_matching_coset_embedding
        assert row.efficient_symmetric_group_qft_available
        assert row.uniform_homogeneous_fourier_basis_sampler_constructed
        assert not row.brauer_and_homogeneous_sector_profiles_equal
        assert row.canonical_purification_multiplicity_ratio == math.factorial(
            row.degree
        )
        assert not row.arbitrary_measurement_row_state_verifier_constructed
        assert not row.polynomial_hidden_involution_decoder_constructed


def test_report_keeps_every_algorithm_gate_closed():
    report = run_perfect_matching_spherical_boundary()
    assert report.headline_metrics["finite_character_control_failure_count"] == 0
    assert report.headline_metrics["brauer_regular_dimension_failure_count"] == 0
    assert (
        report.headline_metrics[
            "brauer_profile_collision_count_beyond_trivial_m1"
        ]
        == 0
    )
    assert report.claim_gate[
        "uniform_homogeneous_fourier_basis_sampler_constructed"
    ]
    assert not report.claim_gate[
        "row_state_is_classically_verifiable_hidden_involution_witness"
    ]
    assert not report.claim_gate["polynomial_hidden_involution_decoder_constructed"]
    assert not report.claim_gate["speedup_claim_allowed"]
