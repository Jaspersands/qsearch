"""Unit tests for theorems/product_channel_erasure_ceiling.py."""
from __future__ import annotations

from fractions import Fraction
import pytest

from theorems.product_channel_erasure_ceiling import (
    binary_code_information_controls,
    coordinate_recipe,
    correlated_countercontrol,
    distribution,
    entropy_box,
    finite_affine_duals,
    helstrom_hard_decision,
    profile,
)


def test_distribution_and_coordinate_recipe():
    q = distribution(("3/4", "1/4"))
    assert len(q) == 2
    rec = coordinate_recipe(("3/4", "1/4"))
    assert rec["minimum_symbol"] == 1
    assert rec["uniform_branch_weight"] == "1/2"
    assert rec["optimal_revealed_symbols"] == "1/2"
    assert rec["optimal_unknown_symbols"] == "1/2"

    with pytest.raises(ValueError):
        distribution(("1/4", "1/4", "1/4", "1/4"))


def test_entropy_box_and_helstrom_hard_decision():
    ent = entropy_box(("1/2", "1/2"), 2, bits=64)
    assert Fraction(ent["lower"]) <= 1 <= Fraction(ent["upper"])

    hel = helstrom_hard_decision(("3/4", "1/4"), bits=64)
    assert hel["binary_overlap"] == "1/2"
    assert Fraction(hel["named_hard_decision_rate_lower"]) <= Fraction(hel["named_hard_decision_rate_upper"])
    assert hel["efficient_code_decoder_supplied"] is False


def test_profile_and_finite_affine_duals():
    prof = profile(("3/4", "1/4"), 64, 48)
    assert prof["prime"] == 2
    assert prof["efficient_decoder_supplied"] is False
    assert prof["new_quantum_speedup_established"] is False

    non_term = profile(("3/4", "1/4"), 64, 48, protocol="retained_coherent_branches")
    assert non_term["status"] == "ERASURE_CEILING_NOT_APPLICABLE_TO_COHERENT_OR_MINIMUM_ERROR_POSTPROCESSING"

    duals = finite_affine_duals(("3/4", "1/4"), 2)
    assert duals["prime"] == 2
    assert duals["width"] == 2
    assert duals["dual_expectation"] == duals["factored_primal_expected_unknown_symbols"]
    assert duals["all_quantum_measurements_excluded"] is False


def test_binary_code_and_correlated_countercontrols():
    code_ctrls = binary_code_information_controls()
    assert len(code_ctrls) == 16
    corr = correlated_countercontrol()
    assert corr["product_assumption_satisfied"] is False
    assert corr["marginal_lower_bound_is_always_achievable"] is False
