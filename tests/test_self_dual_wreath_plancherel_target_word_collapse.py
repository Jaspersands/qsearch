from fractions import Fraction
from functools import lru_cache

import pytest

from representation_obstruction import integer_partitions
from self_dual_wreath_interleaved_product_lift_no_go import (
    product_lift_pattern,
    product_lift_supports,
)
from self_dual_wreath_plancherel_target_word_collapse import (
    audit_character_column_collapse,
    audit_marked_presentation_target_collapse,
    audit_target_law_stability,
    plancherel_normalized_character_average,
    plancherel_target_word_collapse_theorem,
    run_plancherel_target_word_collapse,
)
from self_dual_wreath_translated_parity_commutator_no_go import (
    translated_parity_pattern,
    translated_parity_supports,
)


@lru_cache(maxsize=1)
def _report():
    return run_plancherel_target_word_collapse()


@pytest.mark.parametrize("n", range(2, 13))
def test_plancherel_normalized_character_is_regular_identity_indicator(n):
    identity = (1,) * n
    for target in integer_partitions(n):
        assert plancherel_normalized_character_average(n, target) == int(
            target == identity
        )
    control = audit_character_column_collapse(n)
    assert Fraction(control.maximum_exact_identity_indicator_residual) == 0
    assert control.exact_regular_character_collapse_verified


def test_sparse_seed_keeps_pointwise_targets_but_plancherel_keeps_only_identity():
    same, different = product_lift_supports(0)
    control = audit_marked_presentation_target_collapse(
        "sparse-seed",
        product_lift_pattern(0),
        same,
        different,
    )
    assert control.exact_S3_nonidentity_target_count == 48
    assert control.exact_S3_identity_target_count < control.exact_S3_solution_count
    assert Fraction(control.exact_plancherel_weighted_character_sum) == (
        control.exact_S3_identity_target_count
    )
    assert control.target_collapse_verified


def test_positive_product_lift_has_universally_trivial_target_control():
    same, different = product_lift_supports(1)
    control = audit_marked_presentation_target_collapse(
        "positive-lift",
        product_lift_pattern(1),
        same,
        different,
    )
    assert control.exact_S3_nonidentity_target_count == 0
    assert control.exact_S3_identity_target_count == control.exact_S3_solution_count
    assert control.target_collapse_verified


def test_translated_parity_pointwise_commutator_signal_does_not_rescue_average():
    same, different, _ = translated_parity_supports(3)
    control = audit_marked_presentation_target_collapse(
        "translated-parity",
        translated_parity_pattern(3),
        same,
        different,
    )
    assert control.exact_S3_solution_count == 432
    assert control.exact_S3_nonidentity_target_count == 168
    assert control.exact_S3_identity_target_count == 264
    assert Fraction(control.exact_plancherel_weighted_character_sum) == 264
    assert control.target_collapse_verified


@pytest.mark.parametrize(
    ("n", "target"),
    ((4, (4,)), (4, (2, 2)), (5, (3, 2)), (6, (3, 2, 1))),
)
def test_near_plancherel_target_law_has_uniform_two_tv_stability(n, target):
    control = audit_target_law_stability(
        "stability",
        n,
        target,
        Fraction(1, 100),
    )
    assert Fraction(control.exact_character_expectation_error) <= Fraction(
        control.exact_two_tv_upper_bound
    )
    assert control.two_tv_stability_verified


def test_theorem_closes_signed_target_but_not_green_coefficient_burden():
    theorem = plancherel_target_word_collapse_theorem()
    assert theorem.arbitrary_finite_group
    assert theorem.arbitrary_target_word
    assert theorem.natural_signed_target_loophole_closed
    assert theorem.theorem_verified
    assert not theorem.green_coefficient_burden_resolved
    assert not theorem.positive_component_M4_proved


def test_report_updates_exact_remaining_M4_boundary():
    report = _report()
    assert report.headline_metrics[
        "plancherel_target_word_collapse_theorem_count"
    ] == 1
    assert report.headline_metrics["character_column_control_failure_count"] == 0
    assert report.headline_metrics["marked_presentation_control_failure_count"] == 0
    assert report.headline_metrics["stability_control_failure_count"] == 0
    assert report.headline_metrics[
        "natural_signed_target_pressure_loophole_count"
    ] == 0
    assert not report.claim_gate[
        "natural_plancherel_target_character_can_rescue_crossing_pressure"
    ]
    assert report.claim_gate[
        "all_four_leaf_scalar_pressure_transfers_to_natural_target_average"
    ]
    assert not report.claim_gate["green_polynomial_coefficient_burden_controlled"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
