import math

import pytest

from self_dual_wreath_dyadic_modular_fiber_torsion_no_go import (
    audit_modular_fiber_presentation,
    modular_fiber_scaling_record,
    modular_zero_fiber_size,
    roots_of_unity_density_deviation_bound,
    run_dyadic_modular_fiber_torsion_no_go,
)


def test_modular_fiber_size_and_density_bound_are_exact():
    assert modular_zero_fiber_size(5, 4) == 6
    assert modular_zero_fiber_size(8, 4) == 72
    for modulus in (2, 3, 4, 5):
        for width in (modulus + 1, 2 * modulus, 4 * modulus):
            density = modular_zero_fiber_size(width, modulus) / 2**width
            assert abs(density - 1 / modulus) <= (
                roots_of_unity_density_deviation_bound(width, modulus) + 1e-15
            )


def test_all_width_cyclic_proof_has_exact_finite_tietze_fingerprints():
    for modulus in (2, 3, 4, 5):
        row = audit_modular_fiber_presentation(modulus)
        assert row.adjacent_cancellation_witness_count == row.adjacent_pair_count
        assert row.tietze_remaining_generator_count == 1
        assert len(row.tietze_residual_relations) == 1
        assert len(row.tietze_residual_relations[0]) == modulus
        assert row.exact_cyclic_presentation_verified


def test_dyadic_modular_fibers_have_positive_true_pressure_gap():
    for modulus in (2, 4, 8, 16):
        row = modular_fiber_scaling_record(modulus, 8 * modulus)
        assert row.modulus_is_power_of_two
        assert row.true_scalar_pressure_margin > 0
        assert row.limiting_true_scalar_pressure_margin == pytest.approx(
            math.log2(modulus) - 1 + 1 / modulus
        )
        assert row.true_symmetric_group_frame_solution_exponent == pytest.approx(
            1 - 1 / modulus
        )


def test_entropy_rank_is_not_mistaken_for_true_modular_presentation_rank():
    row = modular_fiber_scaling_record(8, 64)
    assert row.generic_suffix_generator_upper_bound <= 3
    assert row.generic_suffix_generator_upper_bound > (
        row.true_symmetric_group_frame_solution_exponent
    )
    assert row.true_symmetric_group_frame_solution_exponent == pytest.approx(7 / 8)
    assert row.limiting_true_scalar_pressure_margin == pytest.approx(17 / 8)


def test_report_kills_only_cyclic_dyadic_route():
    report = run_dyadic_modular_fiber_torsion_no_go()
    assert report.headline_metrics["all_width_cyclic_presentation_theorem_count"] == 1
    assert report.headline_metrics["dyadic_modular_no_go_theorem_count"] == 1
    assert report.claim_gate["cyclic_modular_fiber_presentation_classified"]
    assert report.claim_gate["cyclic_dyadic_scalar_saturation_falsified"]
    assert not report.claim_gate["all_dyadic_automata_eliminated"]
    assert not report.claim_gate["nonabelian_dyadic_automata_eliminated"]
    assert not report.claim_gate["speedup_claim_allowed"]
