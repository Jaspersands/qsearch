from functools import lru_cache

import math

import pytest

from self_dual_wreath_interleaved_product_lift_no_go import (
    BASE_DIFFERENT_SUPPORT,
    STABLE_RELATIONS,
    STABLE_REMAINING_GENERATORS,
    STABLE_TARGET,
    audit_finite_hom_count,
    audit_product_lift,
    audit_sparse_seed_target,
    finite_target_distribution,
    product_lift_all_depth_certificate,
    product_lift_pattern,
    product_lift_supports,
    run_interleaved_product_lift_no_go,
    target_normal_closure_certificate,
)


@lru_cache(maxsize=1)
def _report():
    return run_interleaved_product_lift_no_go()


def test_sparse_seed_is_a_real_target_survivor_not_a_false_control():
    seed = audit_sparse_seed_target()
    assert seed.pattern == "EFEBAFAB"
    assert seed.solution_count == 1368
    assert seed.nonidentity_target_count == 48
    assert seed.finite_target_survival_verified


@pytest.mark.parametrize("depth", range(1, 9))
def test_every_positive_cube_lift_stabilizes_to_the_same_presentation(depth):
    control = audit_product_lift(depth)
    assert control.pattern == "EFEBAFAB" + "A" * depth
    assert control.same_support_size == (1 << (depth + 1)) - 1
    assert control.different_support_size == 1 << (depth + 1)
    assert control.projected_same_support == BASE_DIFFERENT_SUPPORT
    assert control.projected_different_support == BASE_DIFFERENT_SUPPORT
    assert control.every_appended_generator_forced_identity
    assert control.remaining_generators == STABLE_REMAINING_GENERATORS
    assert control.residual_relations == STABLE_RELATIONS
    assert control.residual_target_word == STABLE_TARGET
    assert control.stable_positive_depth_presentation_verified
    assert control.exact_control_verified


def test_support_family_has_exact_product_and_pruning_structure():
    for depth in range(5):
        same, different = product_lift_supports(depth)
        assert product_lift_pattern(depth).count("A") == 2 + depth
        assert len(same) + 1 == len(different) == 1 << (depth + 1)
        assert (0,) * (4 + depth) not in same
        assert (0,) * (4 + depth) in different


def test_target_has_an_exact_free_word_normal_closure_certificate():
    certificate = target_normal_closure_certificate()
    assert certificate.fourth_relator_factorization_verified
    assert certificate.commutator_from_second_and_fourth_verified
    assert certificate.inverse_replacement_from_third_verified
    assert certificate.target_after_commutator_relation == (
        certificate.final_inverse_second_relator
    )
    assert certificate.target_factorization_from_original_relators == STABLE_TARGET
    assert certificate.exact_free_word_normal_closure_certificate_verified
    assert certificate.all_group_target_identity_proved


def test_positive_lift_target_dies_in_exact_S3_enumeration():
    assert finite_target_distribution(0, 3) == (1368, 48)
    assert finite_target_distribution(1, 3) == (1320, 0)
    assert finite_target_distribution(4, 3) == (1320, 0)


@pytest.mark.parametrize(
    ("degree", "expected_count"),
    ((2, 32), (3, 1320), (4, 148320), (5, 23157120)),
)
def test_finite_hom_formula_obeys_matching_leading_bounds(degree, expected_count):
    control = audit_finite_hom_count(degree)
    assert control.exact_formula_solution_count == expected_count
    assert control.lower_bound_verified
    assert control.upper_bound_verified
    assert control.formula_matches_direct_enumeration is not False
    assert control.lower_bound == control.group_order**3
    assert control.upper_bound == (
        control.group_order**3 * control.conjugacy_class_count**2
    )


@pytest.mark.parametrize("depth", range(1, 9))
def test_exact_count_restores_a_uniform_full_pressure_exponent(depth):
    control = audit_product_lift(depth)
    expected_generic = -0.5 * math.log2(1.0 - 2.0 ** (-(depth + 1)))
    assert control.generic_solution_exponent_upper_bound == 4.0
    assert control.exact_symmetric_group_solution_exponent == 3.0
    assert control.generic_scalar_pressure_margin == pytest.approx(expected_generic)
    assert control.exact_scalar_pressure_margin == pytest.approx(
        1.0 + expected_generic
    )
    assert control.exact_scalar_pressure_margin > 1.0


def test_all_depth_theorem_uses_symbolic_stabilization_and_counting():
    theorem = product_lift_all_depth_certificate()
    assert theorem.arbitrary_positive_lift_depth
    assert theorem.exact_target_identity
    assert theorem.exact_leading_solution_exponent
    assert theorem.symmetric_group_solution_exponent == "3+o(1), exactly"
    assert theorem.uniform_pressure_margin_lower_bound == 1.0
    assert theorem.universal_product_lift_no_go_verified


def test_report_preserves_seed_falsifier_and_rejects_the_scalable_lift():
    report = _report()
    assert report.headline_metrics["all_depth_product_lift_no_go_theorem_count"] == 1
    assert report.headline_metrics["sparse_seed_S3_nonidentity_target_count"] == 48
    assert report.headline_metrics["positive_lift_S3_nonidentity_target_count"] == 0
    assert report.headline_metrics["positive_lift_control_failure_count"] == 0
    assert report.headline_metrics["normal_closure_certificate_failure_count"] == 0
    assert report.headline_metrics["exact_symmetric_group_solution_exponent"] == 3.0
    assert report.claim_gate["sparse_seed_finite_target_survival_verified"]
    assert report.claim_gate["positive_product_lift_target_identity_proved"]
    assert report.claim_gate["exact_symmetric_group_exponent_three_proved"]
    assert not report.claim_gate["positive_product_lift_escape_survives"]
    assert not report.claim_gate["all_nonlinear_near_threshold_supports_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
