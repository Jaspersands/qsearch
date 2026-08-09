import math

import pytest

from self_dual_wreath_component_commutator_collision_free_transfer import (
    additive_sharpness_control,
    collision_free_moment_scaling_record,
    conditional_moment_transfer_bound,
    run_component_commutator_collision_free_transfer,
    sharpness_control,
)


def test_sharp_lower_bound_has_vacuous_and_positive_branches() -> None:
    vacuous = conditional_moment_transfer_bound(0.6, 0.2)
    positive = conditional_moment_transfer_bound(0.6, 0.75)

    assert vacuous.sharp_conditioned_moment_lower_bound == 0
    assert vacuous.lower_bound_nonvacuous is False
    assert positive.sharp_conditioned_moment_lower_bound == pytest.approx(7 / 12)
    assert positive.conditioned_physical_support_mass_lower_bound == pytest.approx(7 / 24)
    assert positive.conditioned_source_block_probability_lower_bound == pytest.approx(7 / 24)
    assert positive.additive_expectation_change_upper_bound == pytest.approx(0.4)


@pytest.mark.parametrize(
    ("probability", "mean"),
    [(0.6, 0.2), (0.6, 0.75), (0.9, 0.99), (1.0, 0.37)],
)
def test_two_atom_distributions_saturate_the_sharp_lower_envelope(
    probability: float,
    mean: float,
) -> None:
    row = sharpness_control("CONTROL", probability, mean)

    assert row.status == "sharp-bounded-variable-conditioning-control-verified"
    assert row.reconstructed_unconditioned_mean == pytest.approx(mean)
    assert row.value_on_conditioning_event == pytest.approx(row.sharp_lower_bound)
    assert row.lower_bound_saturated is True
    assert row.absolute_conditional_mean_change <= row.additive_change_upper_bound + 1e-12


def test_additive_bound_is_itself_sharp() -> None:
    row = additive_sharpness_control("ADDITIVE", 0.6)

    assert row.value_on_conditioning_event == pytest.approx(1.0)
    assert row.value_off_conditioning_event == pytest.approx(0.0)
    assert row.absolute_conditional_mean_change == pytest.approx(0.4)
    assert row.additive_bound_saturated is True
    assert row.status == "sharp-additive-conditioning-control-verified"


@pytest.mark.parametrize(
    ("probability", "moment"),
    [(0.0, 0.1), (1.1, 0.1), (0.5, -0.1), (0.5, 1.1)],
)
def test_invalid_probability_or_moment_is_rejected(
    probability: float,
    moment: float,
) -> None:
    with pytest.raises(ValueError):
        conditional_moment_transfer_bound(probability, moment)


def test_actual_collision_free_rows_improve_but_remain_preasymptotic() -> None:
    early = collision_free_moment_scaling_record(20)
    late = collision_free_moment_scaling_record(48)

    assert 0 < early.global_distinct_probability < late.global_distinct_probability < 1
    assert early.selected_copy_count == early.information_threshold_copy_count + 2
    assert late.selected_copy_count == late.information_threshold_copy_count + 2
    assert early.finite_transfer_nonvacuous is False
    assert late.finite_transfer_nonvacuous is False
    assert late.sharp_conditioned_moment_lower_bound == 0
    assert late.inverse_polynomial_independent_moment_transfers_asymptotically is True
    assert late.natural_independent_moment_lower_bound_proved is False


def test_asymptotic_transfer_requires_collision_error_smaller_than_signal() -> None:
    for n in (10, 100, 10_000):
        eta = 1 / math.sqrt(n)
        collision_error = eta / n
        row = conditional_moment_transfer_bound(1 - collision_error, eta)

        assert row.lower_bound_nonvacuous is True
        assert row.sharp_conditioned_moment_lower_bound / eta == pytest.approx(
            (1 - 1 / n) / (1 - eta / n)
        )


def test_report_closes_conditioning_without_claiming_independent_gap() -> None:
    report = run_component_commutator_collision_free_transfer()

    assert report.status == (
        "collision-free-component-M4-transfer-proved-independent-gap-open"
    )
    assert report.headline_metrics[
        "sharp_bounded_variable_conditioning_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "inverse_polynomial_M4_collision_free_transfer_theorem_count"
    ] == 1
    assert report.headline_metrics["sharpness_control_failure_count"] == 0
    assert report.headline_metrics["finite_nonvacuous_transfer_row_count"] == 0
    assert report.claim_gate[
        "sharp_component_M4_conditioning_transfer_proved"
    ] is True
    assert report.claim_gate[
        "inverse_polynomial_independent_M4_survives_conditioning"
    ] is True
    assert report.claim_gate["natural_independent_plancherel_M4_positive"] is False
    assert report.claim_gate["globally_distinct_natural_component_M4_positive"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
