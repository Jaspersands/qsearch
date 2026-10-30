from fractions import Fraction as F
from itertools import product
import math

import pytest

import coherent_contract as work


@pytest.mark.parametrize("m", range(6))
def test_mass_by_independent_enumeration(m):
    t = F(2, 5)
    direct = sum(((t/2)**sum(x != 0 for x in y)*(1-t)**sum(x == 0 for x in y)
                  for y in product((-1, 0, 1), repeat=m)
                  if y.count(1) <= 1 and y.count(-1) <= 1), F(0))
    assert work.box_mass(m, 1, 1, t) == direct


def test_native_source_constants_and_complete_instrument_budget():
    cert = work.source_certificate(6000, 420, 209, F(13, 200))
    assert cert["mass"] > F(7, 10)
    assert cert["mean_lower"] > F(342, 1000)
    assert cert["mean_upper"]-cert["mean_lower"] < F(1, 10**40)
    plan = work.success_plan(F(7, 10), F(342, 1000))
    assert plan["verified_success_per_round_lower"] > F(1, 20)
    assert plan["round_cap"] == 800
    assert plan["raw_preparation_cap"] == 1600
    p = plan["verified_success_per_round_lower"]
    assert (1-p)**plan["round_cap"] <= F(1, 2**40)
    resources = work.resource_contract(6000, 420, 13, 209, plan)
    assert resources["logical_data_qubits_without_workspace"] == 17460
    assert resources["modular_constant_add_subtracts_per_round"] == 5040000
    total_error = (12000*resources["max_operator_error_per_source_rotation"]
                   + 12000*resources["max_operator_error_per_center_phase"]
                   + 420*resources["max_operator_error_per_QFT"])
    assert total_error == F(1, 1000)
    assert resources["synthesized_gate_count"] is None


def test_error_applies_before_success_conditioning():
    plan = work.success_plan(F(1, 2), F(3, 5), source_tries=1)
    p = plan["verified_success_per_round_lower"]
    tail = plan["ideal_score_tail_lower"]
    assert p == F(1, 2)*tail-F(1, 1000)
    assert p < F(1, 2)*(tail-F(1, 1000))


@pytest.mark.parametrize("changes", [
    {"instrument_error": F(1, 2)}, {"score_error": F(1, 10)},
    {"source_tries": 0}, {"failure_bits": 0}, {"source_tries": True},
])
def test_invalid_or_unproved_budget_rejected(changes):
    with pytest.raises(ValueError):
        work.success_plan(F(7, 10), F(342, 1000), **changes)


def test_source_and_resource_guard():
    with pytest.raises(ValueError, match="separation"):
        work.source_certificate(4, 3, 1, F(1, 3))
    with pytest.raises(ValueError):
        work.box_mass(4, 1, 1, 0.3)
    plan = work.success_plan(F(7, 10), F(342, 1000))
    with pytest.raises(ValueError):
        work.resource_contract(6000, 420, 8, 209, plan)


def test_finite_decoder_is_total_on_padded_bitstrings():
    _, patterns, codebook = work.fixture()
    valid_count = 0
    for words in product(range(16), repeat=4):
        valid, value = work.finite_decoder(words, codebook)
        valid_count += valid
        assert value in patterns
        if not valid:
            assert value == (0,)*4
    assert valid_count == 21
    assert work.finite_decoder((15, 0, 0, 0), codebook) == (False, (0,)*4)
    with pytest.raises(ValueError):
        work.finite_decoder((16, 0, 0, 0), codebook)


def test_interference_and_non_power_of_two_fourier_falsifiers():
    result = work.instrument_control()
    cert = work.source_certificate(4, 4, 1, F(1, 3))
    assert result["correct_norm"] == pytest.approx(1, abs=2e-14)
    assert result["correct_mean"] == pytest.approx(float(cert["mean_lower"]), abs=2e-14)
    assert abs(result["count_record_retained_mean"]) < 2e-14
    assert result["count_record_retained_TV_from_correct"] > 0.1
    assert result["wrong_power_of_two_QFT_invalid_output_mass"] > 0.05
    assert result["wrong_power_of_two_QFT_TV_including_abort"] > 0.1


@pytest.mark.parametrize("order", [7, 15, 31])
def test_rational_cosine_intervals(order):
    for residue in range(order):
        lo, hi = work.cosine_interval(residue, order, F(1, 10**8))
        reference = math.cos(2*math.pi*residue/order)
        assert float(lo)-2e-15 <= reference <= float(hi)+2e-15
        assert hi-lo <= F(2, 10**8)


def test_verified_score_never_accepts_by_midpoint_only():
    matrix, centers = [[1]], [0]
    score = work.verified_score(matrix, centers, [2], 7, threshold=F(-223, 1000))
    actual = math.cos(4*math.pi/7)
    assert float(score["lower"]) <= actual <= float(score["upper"])
    ambiguous = work.verified_score(matrix, centers, [2], 7,
                                    threshold=(score["lower"]+score["upper"])/2)
    assert not ambiguous["accepted"]
    assert work.verified_score(matrix, centers, [0], 7)["accepted"]
    with pytest.raises(ValueError, match="canonical"):
        work.verified_score(matrix, centers, [7], 7)


def test_existing_rational_decoder_does_not_need_a_full_log_table():
    from decoder_replay import replay
    result = replay()
    assert result["field_bits"] == 64
    assert result["licensed_patterns_decoded"] == 21
    assert result["field_power_evaluations"] == 88
    assert result["outside_box_rejected"]
    assert result["full_field_log_table_entries"] == 0
    assert not result["changed_decoder_body"]
