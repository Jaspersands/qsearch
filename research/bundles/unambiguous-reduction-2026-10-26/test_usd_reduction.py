from fractions import Fraction

import pytest

from usd_reduction import repetition_control, transfer_bound, wrong_answer_countercontrol


@pytest.mark.parametrize("length", [1, 2, 3, 4])
def test_signed_pair_reduction_all_syndromes(length):
    result = repetition_control(length)
    p = Fraction(result["actual_decoder_success"])
    for sector in result["syndromes"]:
        if length == 1:
            assert sector["status"] == "NO_ACCEPTED_DECODER_BRANCH"
        else:
            lam = Fraction(sector["gram_eigenvalue"])
            assert Fraction(sector["proved_target_fidelity"]) == p/lam <= 1
            assert sector["direct_target_fidelity"] == pytest.approx(float(p/lam), abs=1e-12)
            assert sector["direct_valid_output_probability"]+1e-12 >= float(p/lam)
            assert float(p/lam) >= float(Fraction(result["refined_success_lower"]))


@pytest.mark.parametrize("length,lower", [(3, Fraction(1, 5)), (4, Fraction(5, 9))])
def test_refinement_is_nonvacuous_when_old_expression_is_vacuous(length, lower):
    result = repetition_control(length)
    assert Fraction(result["old_quantum_failure_expression"]) > 1
    assert Fraction(result["refined_success_lower"]) == lower
    assert result["hardness_evidence"] is False


def test_undetected_wrong_answers_destroy_the_claimed_bound():
    result = wrong_answer_countercontrol()
    assert result["actual_decoder_success"] == "5/8"
    assert result["actual_target_fidelity"] == "1/10"
    assert result["hypothesis_is_necessary"]
    assert not result["unambiguous"]


@pytest.mark.parametrize("error", [Fraction(0), Fraction(1, 4), Fraction(1), Fraction(2)])
def test_exact_bound_and_cost_are_not_an_admission_decision(error):
    result = transfer_bound(error)
    assert result["ideal_success_lower"] == max(0, (1-error)/(1+error))
    assert result["expected_trials_upper"] == (1/(1-error) if error < 1 else None)
    assert result["quantum_advantage_established"] is False


@pytest.mark.parametrize("bad", [-1, 0.25, True, "1/2"])
def test_inexact_or_invalid_bounds_are_rejected(bad):
    with pytest.raises(ValueError):
        transfer_bound(bad)


@pytest.mark.parametrize("length", [0, 5, True, 3.0])
def test_dense_controls_cannot_turn_into_scaling_search(length):
    with pytest.raises(ValueError):
        repetition_control(length)
