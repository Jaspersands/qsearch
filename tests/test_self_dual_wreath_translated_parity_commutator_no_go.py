from functools import lru_cache

import math

import pytest

from self_dual_wreath_translated_parity_commutator_no_go import (
    abstract_normal_form,
    audit_symmetric_group_hom_count,
    audit_translated_parity_presentation,
    even_parity_core,
    run_translated_parity_commutator_no_go,
    standard_character_scaling_control,
    translated_parity_all_depth_certificate,
    translated_parity_pattern,
    translated_parity_supports,
)


@lru_cache(maxsize=1)
def _report():
    return run_translated_parity_commutator_no_go()


def test_abstract_free_product_normal_form_enforces_only_stated_relations():
    assert not abstract_normal_form((2, 2))
    assert not abstract_normal_form((-3, -1, 3, 1))
    assert abstract_normal_form((-3, -4, 3, 4))
    assert abstract_normal_form((1, 2, -1, -2))


@pytest.mark.parametrize("width", range(3, 11))
def test_translated_parity_supports_and_patterns_scale_exactly(width):
    same, different, removed = translated_parity_supports(width)
    assert translated_parity_pattern(width) == "EFE" + "A" * width + "BFB"
    assert len(even_parity_core(width)) == 1 << (width - 1)
    assert len(same) == (1 << (width - 1)) - 1
    assert len(different) == 1 << (width - 1)
    assert removed == (1, 1, *((0,) * (width - 2)))
    assert all(row[-2:] == (1, 1) for row in same)
    assert all(row[-2:] == (0, 0) for row in different)


@pytest.mark.parametrize("width", range(3, 11))
def test_every_depth_has_the_same_abstract_group_and_commutator_target(width):
    control = audit_translated_parity_presentation(width)
    assert control.parity == width % 2
    assert control.every_source_relation_holds_in_abstract_group
    assert control.source_images_generate_abstract_group
    assert control.every_residual_relation_holds_in_abstract_group
    assert control.abstract_target_normal_form == (
        control.expected_commutator_target_normal_form
    )
    assert control.exact_abstract_presentation_verified
    assert control.exact_control_verified


@pytest.mark.parametrize("width", range(3, 11))
def test_target_survives_but_true_scalar_margin_exceeds_three_halves(width):
    control = audit_translated_parity_presentation(width)
    expected_extra = -0.5 * math.log2(1.0 - 2.0 ** (-(width - 1)))
    assert control.exact_S3_solution_count == 432
    assert control.exact_S3_nonidentity_target_count == 168
    assert control.exact_S3_standard_character_average == pytest.approx(5.0 / 12.0)
    assert control.finite_target_survival_verified
    assert control.reducer_solution_exponent_upper_bound == 3.0
    assert control.exact_solution_exponent == 2.5
    assert control.generic_scalar_pressure_margin == pytest.approx(1.0 + expected_extra)
    assert control.exact_scalar_pressure_margin == pytest.approx(1.5 + expected_extra)
    assert control.exact_scalar_pressure_margin > 1.5


@pytest.mark.parametrize(
    ("degree", "expected"),
    ((2, 16), (3, 432), (4, 28800), (5, 2620800), (6, 433382400)),
)
def test_exact_hom_count_is_involution_times_commuting_pairs(degree, expected):
    control = audit_symmetric_group_hom_count(degree)
    assert control.exact_abstract_homomorphism_count == expected
    assert control.expected_formula_count == expected
    assert control.exact_formula_verified


def test_standard_character_class_moment_matches_S3_and_decays_inverse_linearly():
    s3 = standard_character_scaling_control(3)
    assert s3.class_second_moment_sum == 5
    assert s3.exact_standard_target_average == pytest.approx(5.0 / 12.0)
    large = standard_character_scaling_control(1000)
    assert large.exact_partition_formula_verified
    assert large.exact_standard_target_average < 0.002
    assert large.n_scaled_average == pytest.approx(
        large.asymptotic_scaled_limit, abs=0.06
    )


def test_all_depth_theorem_keeps_target_and_scalar_gates_separate():
    theorem = translated_parity_all_depth_certificate()
    assert theorem.arbitrary_core_width
    assert theorem.nontrivial_target_survives
    assert theorem.exact_leading_solution_exponent
    assert theorem.symmetric_group_solution_exponent == "5/2+o(1), exactly"
    assert theorem.standard_character_asymptotic == "12/(pi^2*n)+o(1/n)"
    assert theorem.universal_translated_parity_no_go_verified


def test_report_rejects_persistent_target_bias_on_insufficient_scalar_mass():
    report = _report()
    assert report.headline_metrics[
        "all_depth_translated_parity_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["presentation_control_failure_count"] == 0
    assert report.headline_metrics["finite_hom_count_failure_count"] == 0
    assert report.headline_metrics["S3_nonidentity_target_count"] == 168
    assert report.headline_metrics["S3_standard_character_average"] == pytest.approx(
        5.0 / 12.0
    )
    assert report.headline_metrics["exact_symmetric_group_solution_exponent"] == 2.5
    assert report.claim_gate["translated_parity_target_survives"]
    assert report.claim_gate["translated_parity_exact_presentation_classified"]
    assert not report.claim_gate["translated_parity_scalar_pressure_survives"]
    assert not report.claim_gate["standard_target_character_is_constant"]
    assert not report.claim_gate["speedup_claim_allowed"]
