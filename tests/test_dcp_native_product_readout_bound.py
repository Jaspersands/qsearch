import math
from fractions import Fraction

import pytest

from dcp_native_product_readout_bound import (
    _adaptive_scope_countercontrol, _complete_native_source_controls, _povm,
    native_product_readout_certificate, run_controls,
)
from dcp_physical_phase_noise import read


def test_source_collision_formula_keeps_doubled_character_alias_term():
    row = native_product_readout_certificate(1, 2, 2)
    assert read(row["source_mean_uniform_secret_correct_probability_squared_upper_bound"]) == Fraction(25, 32)
    assert row["doubled_character_image_size"] == "2"
    assert not row["claim_is_pointwise_for_each_fixed_secret_or_label_matrix"]


def test_complete_native_source_census_matches_alias_corrected_formula():
    rows = _complete_native_source_controls()
    assert [r["complete_native_label_matrices"] for r in rows] == [16, 64, 256]
    assert [read(r["exact_rational_native_mean_collision_envelope"]) for r in rows] == [Fraction(25,8),Fraction(43,16),Fraction(43,16)]


def test_general_product_POVMs_and_unlimited_outcome_decoder_obey_pointwise_gate():
    rows = run_controls()["actual_arbitrary_product_POVM_controls"]
    assert len(rows) == 9
    for row in rows:
        assert row["actual_mean_weighted_likelihood_collision"] <= row["matrix_pointwise_collision_envelope"]+1e-9
        assert row["actual_optimal_decoder_correct_probability"] <= row["matrix_pointwise_correct_probability_upper_bound"]+1e-9
    assert {r["family"] for r in rows} == {"label_adaptive_projective", "trine", "tetrahedral"}


def test_near_entropy_width_bound_is_exponential_and_allows_label_adaptive_choices():
    rows = [native_product_readout_certificate(n,4*n+1,n*(4*n+1)+16) for n in (8,16,32)]
    assert [r["conservative_correct_probability_dyadic_exponent"] for r in rows] == [50,211,851]
    for row in rows:
        assert row["entire_public_label_matrix_may_choose_all_local_POVMs"]
        assert not row["adaptive_local_or_entangled_measurements_ruled_out"]


def test_order_two_and_excess_sample_regimes_do_not_produce_false_barriers():
    assert read(native_product_readout_certificate(8,1,8)["source_mean_uniform_secret_correct_probability_squared_upper_bound"]) == 1
    assert read(native_product_readout_certificate(1,3,20)["source_mean_uniform_secret_correct_probability_squared_upper_bound"]) == 1


def test_actual_adaptive_countercontrol_beats_nonadaptive_pointwise_bound():
    row = _adaptive_scope_countercontrol()
    assert all(p > 1-1e-10 for p in row["adaptive_every_secret_correct_probabilities"])
    assert row["nonadaptive_X_optimal_correct_probability"] == 0.75
    assert row["nonadaptive_matrix_pointwise_correct_probability_bound"] < 1
    assert not row["scalable_native_adaptive_label_selector_or_decoder_supplied"]


@pytest.mark.parametrize("bad", [[], [(1,2,0,0)], [(0.5,1,0,0)], [(1,math.nan,0,0)], [(0,0,0,0)], [(1,1,0,0)]])
def test_nonpositive_or_incomplete_POVMs_rejected(bad):
    with pytest.raises(ValueError):
        _povm(bad)


def test_invalid_source_parameters_rejected():
    for args in ((0,2,3),(1,0,3),(1,2,0),(True,2,3)):
        with pytest.raises(ValueError):
            native_product_readout_certificate(*args)
