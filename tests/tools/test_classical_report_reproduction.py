"""Regression tests for portable reproduction without weakening exact certificates."""
from fractions import Fraction
from types import SimpleNamespace

import pytest

from tests.tools.classical_report_reproduction import (
    fixed_weight_proposer,
    report_differences,
    reproduce,
)


def test_observed_linux_float_roundoff_is_accepted_with_nested_paths() -> None:
    # Actual maximum capacity-source drift and near-zero polar calibration drift.
    expected = {"controls": [0.04612887126924903, 6.661338147750939e-16]}
    actual = {"controls": [0.046128871269282445, 1.3877787807814457e-16]}
    assert report_differences(actual, expected) == []


def test_material_float_change_reports_the_leaf_and_error() -> None:
    differences = report_differences(
        {"controls": [{"probability": 0.7018402229530696}]},
        {"controls": [{"probability": 0.7018402228530696}]},
    )
    assert len(differences) == 1
    assert differences[0].startswith("$.controls[0].probability:")
    assert "absolute error" in differences[0] and "tolerance" in differences[0]


@pytest.mark.parametrize("actual,expected,path", [
    ({"v": 2**61 + 1}, {"v": 2**61}, "$.v"),
    ({"v": True}, {"v": 1}, "$.v"),
    ({"v": 1.0}, {"v": 1}, "$.v"),
    ({"v": "0.5000000000000001"}, {"v": "0.5"}, "$.v"),
    ({"v": "2/4"}, {"v": "1/2"}, "$.v"),
    ({"v": "10000000000000001/20000000000000000"}, {"v": "1/2"}, "$.v"),
    ({"v": "UNKNOWN"}, {"v": "CERTIFIED"}, "$.v"),
    ({}, {"v": None}, "$.v"),
    ({"v": None}, {}, "$.v"),
    ({"v": [1, 2]}, {"v": [1]}, "$.v"),
    ({"v": [2, 1]}, {"v": [1, 2]}, "$.v[0]"),
    ({"v": []}, {"v": {}}, "$.v"),
])
def test_only_floating_leaves_have_a_tolerance(actual, expected, path) -> None:
    differences = report_differences(actual, expected)
    assert differences and differences[0].startswith(path + ":")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_floats_are_rejected_even_when_both_reports_contain_them(value) -> None:
    assert "nonfinite" in report_differences({"v": value}, {"v": value})[0]


def _saved_readout(weight: str) -> dict:
    return {
        "fixed_input_profiles": [{"finite_readout": {
            "specification": {"positions": 127, "input_set_density": "1/2"},
            "ell": 0,
            "Rayleigh_certificate": {"radial_weights_exact": [weight]},
        }}],
        "unlicensed_degree_controls": [],
    }


def test_eigenvector_proposals_are_checked_then_saved_exact_inputs_are_replayed() -> None:
    # The largest observed Linux eigenvector component drift is about 1.54e-15.
    saved = Fraction("7706031343449883/72057594037927936")
    actual = Fraction("3853015671724997/36028797018963968")
    calls = []

    def propose(N, rho, ell):
        calls.append((N, rho, ell))
        return (actual,)

    replay = fixed_weight_proposer(propose, _saved_readout(str(saved)))
    assert replay(127, Fraction(1, 2), 0) == (saved,)
    assert calls == [(127, Fraction(1, 2), 0)]


def test_material_proposal_change_fails_before_replaying_saved_weights() -> None:
    replay = fixed_weight_proposer(lambda *args: (Fraction(1, 2) + Fraction(1, 10**10),),
                                  _saved_readout("1/2"))
    with pytest.raises(AssertionError, match=r"fixed_input_profiles\[0\].*radial_weights_exact\[0\]"):
        replay(127, Fraction(1, 2), 0)


def test_proposal_shape_and_exact_type_changes_are_not_hidden_by_replay() -> None:
    for proposed in [(Fraction(1, 2), Fraction(1, 2)), (0.5,), (True,)]:
        replay = fixed_weight_proposer(lambda *args: proposed, _saved_readout("1/2"))
        with pytest.raises(AssertionError):
            replay(127, Fraction(1, 2), 0)


def test_unexpected_proposal_inputs_are_not_silently_replaced() -> None:
    replay = fixed_weight_proposer(lambda *args: (Fraction(1, 2),), _saved_readout("1/2"))
    with pytest.raises(AssertionError, match="no saved exact weights"):
        replay(128, Fraction(1, 2), 0)


def test_replay_does_not_hide_a_changed_exact_certificate_and_restores_proposer() -> None:
    saved = _saved_readout("1/2")
    proposer = lambda *args: (Fraction(1, 2),)
    module = SimpleNamespace(__name__="qsearch_classical.prime_character_finite_readout",
                             propose_weights=proposer)

    def run_controls():
        weights = module.propose_weights(127, Fraction(1, 2), 0)
        # A changed rational result must fail even when its floating value rounds back.
        report = _saved_readout(str(weights[0] + Fraction(1, 10**30)))
        return report

    module.run_controls = run_controls
    fresh = reproduce(module, saved)
    assert module.propose_weights is proposer
    assert "radial_weights_exact[0]" in report_differences(fresh, saved)[0]
