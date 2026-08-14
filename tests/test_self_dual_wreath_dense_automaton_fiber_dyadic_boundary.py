import math

import pytest

from self_dual_wreath_dense_automaton_fiber_dyadic_boundary import (
    audit_dense_fiber_rank,
    audit_periodic_mixing_certificate,
    density_generator_upper_bound,
    exact_dyadic_full_fiber_dichotomy_control,
    modular_weight_fiber,
    periodic_generic_pressure_scaling,
    pressure_margin_from_fiber_sizes,
    run_dense_automaton_fiber_dyadic_boundary,
    uniform_class_pressure_control,
)


def test_density_bound_is_exact_integer_codimension_bound():
    assert density_generator_upper_bound(10, 2**9) == 1
    assert density_generator_upper_bound(10, 342) == 1
    assert density_generator_upper_bound(10, 256) == 2
    with pytest.raises(ValueError):
        density_generator_upper_bound(3, 0)


def test_dense_modular_automaton_fibers_have_constant_suffix_rank():
    parity = audit_dense_fiber_rank(
        "parity",
        modular_weight_fiber(10, 2, 0),
    )
    mod_three = audit_dense_fiber_rank(
        "mod-three",
        modular_weight_fiber(10, 3, 0),
    )
    assert parity.exact_density_rank_identity_verified
    assert mod_three.exact_density_rank_identity_verified
    assert parity.theorem_generator_upper_bound == 1
    assert mod_three.theorem_generator_upper_bound <= 2
    assert len(parity.explicit_suffix_forced_coordinates) <= 1


def test_uniform_non_dyadic_classes_have_gap_but_dyadic_classes_can_saturate():
    dyadic = uniform_class_pressure_control(
        "dyadic",
        2,
        10,
        2**9,
        2**9,
    )
    non_dyadic = uniform_class_pressure_control(
        "non-dyadic",
        3,
        20,
        round(2**20 / 3),
        round(2**20 / 3),
    )
    assert dyadic.class_size_is_power_of_two
    assert dyadic.scalar_pressure_margin_lower_bound == pytest.approx(0.0)
    assert not non_dyadic.class_size_is_power_of_two
    assert non_dyadic.scalar_pressure_margin_lower_bound == pytest.approx(
        math.log2(3) - 1,
        rel=2e-5,
    )
    assert not non_dyadic.target_character_can_repair_scalar_loss


def test_pressure_margin_uses_denser_fiber_integer_rank():
    rank, margin = pressure_margin_from_fiber_sizes(10, 300, 400)
    assert rank == density_generator_upper_bound(10, 400)
    assert margin == pytest.approx(
        10 - 0.5 * math.log2(300 * 400) - rank
    )


def test_periodic_S3_transfer_gives_generic_constant_rank_and_positive_gap():
    mixing = audit_periodic_mixing_certificate()
    rows = periodic_generic_pressure_scaling(6)
    assert mixing.exact_transfer_certificate_imported
    assert mixing.leading_communicating_class_size == 18
    assert mixing.subleading_to_leading_eigenvalue_ratio == pytest.approx(0.5)
    assert all(row.denser_fiber_generator_upper_bound <= 4 for row in rows)
    assert all(row.scalar_pressure_margin_lower_bound > 0 for row in rows)
    assert rows[-1].scalar_pressure_margin_lower_bound == pytest.approx(
        math.log2(18) - 4,
        abs=2e-11,
    )


def test_exact_balanced_dyadic_full_fibers_obey_target_scalar_dichotomy():
    identity_fiber = exact_dyadic_full_fiber_dichotomy_control(
        "identity",
        12,
        9,
        zero_in_same_fiber=True,
    )
    nonidentity_fiber = exact_dyadic_full_fiber_dichotomy_control(
        "nonidentity",
        12,
        9,
        zero_in_same_fiber=False,
    )
    assert identity_fiber.scalar_pressure_margin == pytest.approx(0.0)
    assert identity_fiber.residual_target_forced_to_identity
    assert not identity_fiber.target_survival_blocked_by_scalar_loss
    assert nonidentity_fiber.scalar_pressure_margin == pytest.approx(1.0)
    assert not nonidentity_fiber.residual_target_forced_to_identity
    assert nonidentity_fiber.target_survival_blocked_by_scalar_loss
    assert identity_fiber.exact_dichotomy_verified
    assert nonidentity_fiber.exact_dichotomy_verified


def test_report_keeps_dyadic_and_growing_state_routes_open():
    report = run_dense_automaton_fiber_dyadic_boundary()
    assert report.headline_metrics["dense_constant_state_rank_theorem_count"] == 1
    assert report.headline_metrics["non_dyadic_uniform_class_no_go_theorem_count"] == 1
    assert report.headline_metrics["dyadic_saturation_boundary_count"] == 2
    assert report.claim_gate["every_dense_constant_state_fiber_has_O1_rank_proved"]
    assert report.claim_gate["non_dyadic_uniform_mixing_scalar_suppression_proved"]
    assert report.claim_gate["exact_balanced_dyadic_full_fibers_eliminated"]
    assert not report.claim_gate["all_constant_state_automata_eliminated"]
    assert not report.claim_gate["dyadic_target_survival_eliminated"]
    assert not report.claim_gate["near_uniform_dyadic_target_survival_eliminated"]
    assert not report.claim_gate["growing_state_automata_eliminated"]
    assert not report.claim_gate["speedup_claim_allowed"]
