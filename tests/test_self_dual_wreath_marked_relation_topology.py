from functools import lru_cache

import pytest

from self_dual_wreath_marked_relation_topology import (
    audit_fixed_degree_pressure,
    audit_relation_topology,
    audit_support_expansion,
    bounded_nielsen_one_relator_certificate,
    centralized_primitive_power_certificate,
    frame_assignments,
    free_basis_commutator_certificate,
    marked_support_presentation,
    nonorientable_quadratic_genus,
    onto_function_count,
    orientable_quadratic_genus,
    presentation_solution_count,
    presentation_solution_exponent_upper_bound,
    power_conjugacy_certificate,
    pure_power_gcd_collapse_certificate,
    relation_topology_scaling_record,
    run_marked_relation_topology,
    support_expansion_sum,
    tietze_reduce_presentation,
    whitehead_primitive_certificate,
    whitehead_one_relator_certificate,
)


@lru_cache(maxsize=1)
def _report():
    return run_marked_relation_topology()


def test_onto_coefficients_reconstruct_assignment_powers():
    assert onto_function_count(0, 0) == 1
    assert onto_function_count(4, 2) == 14
    assert onto_function_count(4, 3) == 36
    for valid_count in range(9):
        for power in range(7):
            assert support_expansion_sum(valid_count, power) == valid_count**power


def test_support_expansion_is_exact_for_four_frame_positions():
    control = audit_support_expansion(4, 6)
    assert control.assignment_type_count == 16
    assert control.maximum_identity_residual == 0
    assert control.exact_support_profile_expansion_verified


def test_noncrossing_leaf_order_reduces_to_two_free_generators():
    relations = marked_support_presentation("EEFF", (), ((),))
    reduction = tietze_reduce_presentation(4, relations)
    assert reduction.residual_topology == "free-group"
    assert reduction.free_generator_count == 2
    assert not reduction.residual_relations


def test_crossing_leaf_order_reduces_to_one_commutator():
    relations = marked_support_presentation("EFEF", (), ((),))
    reduction = tietze_reduce_presentation(4, relations)
    assert reduction.residual_topology == "rank-two-torus-commutator"
    assert len(reduction.remaining_generators) == 2
    assert len(reduction.residual_relations) == 1
    assert reduction.orientable_surface_genus == 1
    assert reduction.classified_solution_exponent == 1


def test_quadratic_polygon_classifier_detects_genus_one_with_extra_generator():
    relation = (-5, -4, -3, 4, 5, 3)
    assert orientable_quadratic_genus(relation) == 1


def test_nonorientable_quadratic_polygon_classifier_detects_crosscap_number():
    assert nonorientable_quadratic_genus((-1, -1)) == 1
    assert nonorientable_quadratic_genus((-1, -1, -2, -2)) == 2
    assert nonorientable_quadratic_genus((-1, -2, -1, -2)) == 1
    assert nonorientable_quadratic_genus((-1, -2, 1, 2)) is None


def test_projective_plane_word_has_involution_count_exponent():
    reduction = tietze_reduce_presentation(1, ((-1, -1),))
    assert reduction.residual_topology == "nonorientable-surface-genus-1"
    assert reduction.nonorientable_surface_genus == 1
    assert reduction.classified_solution_exponent == 0.5


def test_last_two_token_relator_has_an_exact_free_basis_commutator_certificate():
    relation = (-6, -5, -5, -3, 5, 6, 3, 5)
    certificate = free_basis_commutator_certificate(relation, (3, 5, 6))
    assert certificate is not None
    assert certificate.exact_commutator_identity_verified
    assert certificate.exact_free_basis_verified
    assert presentation_solution_count(3, (3, 5, 6), (relation,)) == 108


def test_hidden_genus_two_word_has_an_exact_nielsen_certificate():
    relation = (-7, -6, 7, -6, -4, -3, 4, 6, 3, 6)
    certificate = bounded_nielsen_one_relator_certificate(
        relation,
        (3, 4, 6, 7),
    )
    assert certificate is not None
    assert certificate.exact_automorphism_chain_verified
    assert certificate.orientable_surface_genus == 2
    assert len(certificate.moves) == 1


def test_primitive_cube_relation_loses_one_third_group_exponent():
    reduction = tietze_reduce_presentation(1, ((-1, -1, -1),))
    upper_bound, source = presentation_solution_exponent_upper_bound(reduction)
    assert upper_bound == pytest.approx(2 / 3)
    assert source == "single-primitive-power-degree-3"


def test_adversarial_cube_is_centralized_torsion_not_coprime_collapse():
    residual_relations = (
        (-5, -5, -5),
        (-7, -5, -5, 7, -5),
        (-7, -6, -5, -5, 7, -5, 6),
        (-7, -6, -5, 7, -5, -5, 6),
    )
    certificate = centralized_primitive_power_certificate(residual_relations)
    assert certificate is not None
    assert certificate.power_generator == 5
    assert certificate.central_generator == 7
    assert certificate.free_product_generator == 6
    assert certificate.power_centralizer_relation_indices == (2,)
    assert certificate.central_commutator_relation_indices == (3, 4)
    assert certificate.exact_presentation_equivalence_verified
    assert certificate.symmetric_group_solution_exponent == pytest.approx(5 / 3)

    simple_relations = (
        (-5, -5, -5),
        (-7, -5, 7, 5),
        (-7, -6, 7, 6),
    )
    assert presentation_solution_count(2, (5, 6, 7), residual_relations) == 4
    assert presentation_solution_count(3, (5, 6, 7), residual_relations) == 42
    assert presentation_solution_count(
        3, (5, 6, 7), simple_relations
    ) == 42

    reduction = tietze_reduce_presentation(
        7,
        marked_support_presentation(
            "EAFAAEF",
            ((0, 0, 0), (1, 0, 1), (1, 1, 0)),
            ((0, 1, 1), (1, 0, 0)),
        ),
    )
    upper_bound, source = presentation_solution_exponent_upper_bound(reduction)
    assert upper_bound == pytest.approx(5 / 3)
    assert source == "multi-relator-centralized-primitive-power-degree-3"


def test_literal_coprime_pure_powers_force_identity_exactly():
    relations = ((-1, -1), (-1, -1, -1))
    certificate = pure_power_gcd_collapse_certificate(relations)
    assert certificate is not None
    assert certificate.power_generator == 1
    assert certificate.pure_power_degrees == (2, 3)
    assert certificate.power_degree_gcd == 1
    assert certificate.exact_forced_identity_verified
    assert presentation_solution_count(3, (1,), relations) == 1
    reduction = tietze_reduce_presentation(1, relations)
    upper_bound, source = presentation_solution_exponent_upper_bound(reduction)
    assert upper_bound == 0
    assert source == "multi-relator-coprime-pure-power-collapse"


def test_unit_power_conjugacy_relation_loses_one_group_exponent():
    relation = (-1, -1, -2, -1, 2)
    certificate = power_conjugacy_certificate(relation)
    assert certificate is not None
    assert certificate.unit_power_present
    assert sorted((abs(certificate.left_power), abs(certificate.right_power))) == [1, 2]
    assert presentation_solution_count(3, (1, 2), (relation,)) == 12
    reduction = tietze_reduce_presentation(2, (relation,))
    upper_bound, source = presentation_solution_exponent_upper_bound(reduction)
    assert upper_bound == 1
    assert source == "single-unit-power-conjugacy-degree-2"


def test_whitehead_certificate_reduces_degree_four_relator_to_a_generator():
    relation = (-4, -3, -2, -4, -3, 2, 3)
    certificate = whitehead_primitive_certificate(relation, (1, 2, 3, 4))
    assert certificate is not None
    assert certificate.exact_automorphism_chain_verified
    assert len(certificate.moves) == 4
    assert len(certificate.transformed_relation) == 1
    assert presentation_solution_count(3, (1, 2, 3, 4), (relation,)) == 6**3
    reduction = tietze_reduce_presentation(4, (relation,))
    upper_bound, source = presentation_solution_exponent_upper_bound(reduction)
    assert upper_bound == 3
    assert source == "single-whitehead-primitive"


def test_whitehead_minimization_exposes_hidden_genus_two_at_rank_six():
    relation = (
        -6, -5, -4, -3, -4, -3, -2, -1,
        2, 3, 4, 6, 1, 3, 4, 5,
    )
    certificate = whitehead_one_relator_certificate(
        relation,
        (1, 2, 3, 4, 5, 6),
    )
    assert certificate is not None
    assert certificate.exact_automorphism_chain_verified
    assert certificate.orientable_surface_genus == 2
    assert len(certificate.moves) == 3
    assert len(certificate.transformed_relation) == 8
    reduction = tietze_reduce_presentation(6, (relation,))
    upper_bound, source = presentation_solution_exponent_upper_bound(reduction)
    assert upper_bound == 5
    assert source == "whitehead-orientable-surface-genus-2"


def test_tietze_reduction_preserves_mixed_profile_solution_counts():
    controls = [
        audit_relation_topology(
            "TEST-MIXED-" + "".join(map(str, assignment)),
            "EAFB",
            (),
            (assignment,),
        )
        for assignment in frame_assignments("EAFB")
    ]
    assert all(row.exact_solution_preservation_verified for row in controls)


def test_fixed_degree_profile_bound_is_independent_of_copy_depth():
    small = relation_topology_scaling_record(8, 4)
    large = relation_topology_scaling_record(64, 4)
    assert small.log2_support_profile_upper_bound == 32
    assert large.log2_support_profile_upper_bound == 32
    assert large.log2_raw_coordinate_assignment_terms > small.log2_raw_coordinate_assignment_terms
    assert large.fixed_degree_copy_depth_growth_removed
    assert not large.growing_degree_profile_classification_proved


def test_every_zero_and_one_frame_profile_has_the_expected_pressure_gap():
    zero = audit_fixed_degree_pressure(0)
    one = audit_fixed_degree_pressure(1)
    two = audit_fixed_degree_pressure(2)
    assert zero.expected_pressure_separation_verified
    assert one.expected_pressure_separation_verified
    assert one.maximum_noncrossing_rescaled_pressure == 0
    assert one.maximum_crossing_rescaled_pressure == -1
    assert two.unclassified_support_profile_count > 0
    assert two.pressure_uncertified_support_profile_count == 0
    assert two.free_basis_commutator_bound_profile_count >= 1
    assert two.maximum_noncrossing_rescaled_pressure == 0
    assert two.maximum_crossing_rescaled_pressure == -1
    assert two.expected_pressure_separation_verified


def test_report_recovers_exact_free_vs_commutator_counts_without_overclaiming():
    report = _report()
    metrics = report.headline_metrics
    assert metrics["noncrossing_S3_solution_count"] == 36
    assert metrics["crossing_S3_solution_count"] == 18
    assert metrics["relation_topology_control_failure_count"] == 0
    assert metrics[
        "one_frame_token_complete_pressure_separation_theorem_count"
    ] == 1
    assert metrics["two_frame_token_pressure_separation_theorem_count"] == 1
    assert metrics["two_frame_token_pressure_uncertified_profile_count"] == 0
    assert metrics["degree_three_adversarial_pressure_control_count"] == 4
    assert metrics["degree_three_adversarial_pressure_failure_count"] == 0
    assert {
        row.exponent_certificate_source for row in report.adversarial_pressure_controls
    } == {
        "whitehead-orientable-surface-genus-2",
        "single-free-basis-commutator",
        "multi-relator-centralized-primitive-power-degree-3",
    }
    assert metrics["centralized_primitive_cube_presentation_theorem_count"] == 1
    assert report.claim_gate["fixed_degree_copy_depth_growth_removed"]
    assert report.claim_gate["degree_three_adversarial_obstructions_resolved"]
    assert not report.claim_gate["degree_three_complete_pressure_separation_proved"]
    assert not report.claim_gate["growing_degree_profile_classification_proved"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
