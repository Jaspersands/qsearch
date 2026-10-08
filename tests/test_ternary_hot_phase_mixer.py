from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_cyclic_extractor import random_even_source
from ternary_hot_phase_mixer import (
    DERIVATION, REPORT, HotPhaseMixer, ceil_cube_root, exact_pi_census,
    five_word_torsion_pi_census, one_layer_adaptive_angle_bound, one_layer_pi_population,
)


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


@pytest.fixture(scope="module")
def program():
    s = random_even_source(2, 4, 5, 89881)
    return HotPhaseMixer(s, (0, 0))


@pytest.mark.parametrize("v", [1, 2, 7, 8, 9, 27, 28, 9**128, 729**512])
def test_implicit_angle_net_cube_root_is_exact(v):
    c = ceil_cube_root(v)
    assert (c-1)**3 < v <= c**3


@pytest.mark.parametrize("v", [0, -1, True, 9.0])
def test_implicit_net_schema_rejects_invalid_integer(v):
    with pytest.raises(ValueError):
        ceil_cube_root(v)


@pytest.mark.parametrize("q,M,expected", [(3, 2, "665/2187"), (9, 1, "1625/6561")])
def test_composite_and_field_full_label_censuses_retain_empty_fibers(q, M, expected):
    result = exact_pi_census(q, M)
    assert result["entire_native_label_matrices"] == 81
    assert result["uniform_target_mean_success_exact"] == expected
    assert result["uniform_target_mean_success_exact"] == one_layer_pi_population(1, q, M)["uniform_target_population_success_exact"]
    assert result["Born_target_mean_success_exact"] != expected


@pytest.mark.parametrize("args", [(9, 3), (81, 2), (3, 4)])
def test_entire_population_caps_do_not_return_partial_means(args):
    with pytest.raises(ValueError):
        exact_pi_census(*args)


def test_cost_program_is_full_root_public_arithmetic_without_word_grid():
    p = HotPhaseMixer(random_even_source(8, 4, 128, 99317), (0,)*8)
    result = p.energy_program((0,)*128)
    assert result["original_public_row_evaluations_upper"] == 1024
    assert result["residual_energy"] == 0
    assert not result["whole_word_or_secret_grid_required"]
    assert not result["unknown_secret_or_unknown_state_inverse_used"]


@pytest.mark.parametrize("layers", [[(0.0, 0.0)], [(math.pi, math.pi)], [(math.pi/2, math.pi/3), (math.pi, math.pi/2)]])
def test_actual_coherent_program_normalization_membership_and_uniform_overlap(program, layers):
    r = program.reference(layers)
    amplitudes = np.array([complex(*a) for a in r["state_amplitudes_numeric"]])
    marked = r["marked_word_indices"]
    assert np.vdot(amplitudes, amplitudes).real == pytest.approx(1)
    membership = np.sum(abs(amplitudes[marked])**2)
    coherent = abs(np.sum(amplitudes[marked]))**2/len(marked)
    assert membership == pytest.approx(r["raw_fiber_membership_probability_numeric"])
    assert coherent == pytest.approx(r["normalized_uniform_fiber_overlap_squared_numeric"])
    assert coherent <= membership+1e-13
    assert r["fiber_membership_is_not_clean_uniform_fiber_erasure"]
    assert r["classical_reference_word_enumerations_charged"] == 243


def test_zero_angles_are_exactly_the_rejection_baseline(program):
    r = program.reference([(0, 0)])
    assert r["raw_fiber_membership_probability_numeric"] == pytest.approx(float(Fraction(r["classical_uniform_word_rejection_probability_exact"])))


def test_existing_grover_baseline_is_not_claimed_new(program):
    r = program.reference([(0, 0)])
    p = Fraction(r["classical_uniform_word_rejection_probability_exact"])
    assert Fraction(r["Grover_one_marked_reflection_probability_exact"]) == p*(3-4*p)**2


@pytest.mark.parametrize("layers", [[], [(float("nan"), 0)], [(0, float("inf"))], [(True, 0)]])
def test_invalid_or_unbounded_public_angles_are_rejected(program, layers):
    with pytest.raises(ValueError):
        program.reference(layers)


def test_preflight_caps_before_whole_word_enumeration():
    p = HotPhaseMixer(random_even_source(8, 4, 128, 99317), (0,)*8)
    with pytest.raises(ValueError):
        p.reference([(0, 0)])


def test_one_layer_continuous_angle_tuning_is_exponentially_small_in_population():
    c = one_layer_adaptive_angle_bound(128, 243, 648)
    assert Fraction(c["best_label_and_target_adaptive_angles_uniform_population_success_upper"]) < Fraction(1, 2**320)
    assert Fraction(c["best_label_and_target_adaptive_angles_Born_population_success_upper"]) < Fraction(1, 2**160)
    assert c["labels_and_target_may_select_continuous_angles"]
    assert c["net_is_mathematical_certificate_not_executed_optimizer"]
    assert c["multiple_layers_or_label_adaptive_mixer_shapes_are_not_covered"]


def test_label_adaptive_born_policy_is_not_given_uniform_target_weighting():
    c = one_layer_adaptive_angle_bound(32, 81, 136)
    s = Fraction(c["best_label_and_target_adaptive_angles_uniform_population_success_upper"])
    born = Fraction(c["best_label_and_target_adaptive_angles_Born_population_success_upper"])
    G, D = 81**32, 3**136
    assert born >= s
    assert (born-s)**2 >= Fraction(G-1, D)*s


def test_native_field_root_positive_control_prevents_generic_hot_no_go():
    s = native_source(((inverse_frequency_coordinates(1, 2, 2),),), 2)
    r = HotPhaseMixer(s, (1,)).reference([(2*math.pi/3, 2*math.pi/3)])
    assert r["raw_fiber_membership_probability_numeric"] == pytest.approx(1)


def test_reference_layer_count_and_fiber_phases_are_not_erasure_flags(artifact):
    assert len(artifact["two_layer_open_scope_control"]["layers"]) == 2
    assert artifact["multiple_layers_are_not_excluded"]
    assert artifact["finite_menu_selection_uses_charged_classical_statevector_enumeration"]
    assert not artifact["efficient_clean_fiber_preparation_supplied"]


@pytest.mark.parametrize("q,expected", [(3, "11/27"), (9, "811/2187")])
def test_actual_five_word_native_torsion_prevents_false_many_layer_independence(q, expected):
    from sympy import Matrix
    r = five_word_torsion_pi_census(q)
    assert Matrix(r["pointed_first_row_coefficient_matrix"]).det() == -3
    assert r["actual_four_phase_pi_moment_exact"] == expected
    assert Fraction(expected) != Fraction(r["false_full_independence_prediction_exact"])
    assert r["unused_second_native_rows_integrated_out_not_assumed_fixed_in_population"]
    assert not r["correlation_is_an_executed_two_layer_advantage"]
    eta2 = Fraction(1+(q-1)**2, q*q)
    assert Fraction(r["mixed_quarter_phase_moment_exact"]) == eta2**2+2*Fraction(2, q*q)**2
    assert r["mixed_quarter_phase_imaginary_part_exact"] == "0"


@pytest.mark.parametrize("q", [3, 9])
def test_five_word_full_root_annihilator_is_exactly_three_characters(q):
    kernel = [nu for nu in product(range(q), repeat=4)
              if all((sum(nu)-nu[j]) % q == 0 for j in range(4))]
    assert kernel == [tuple([k*(q//3)]*4) for k in range(3)]


def test_derivation_hash_and_false_claim_guards(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    for flag in ("arbitrary_quantum_receiver_lower_bound", "efficient_clean_fiber_preparation_supplied", "quantum_speedup_proved", "candidate_record_accepted", "novelty_claim"):
        assert artifact[flag] is False


def test_independent_checker():
    r = subprocess.run(["node", "research/certificates/ternary_hot_phase_mixer_crosscheck.js"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["status"] == "PASS"


@pytest.mark.parametrize("case", ["population", "layer", "scope", "net", "coherence"])
def test_independent_checker_rejects_tampering(artifact, tmp_path, case):
    r = deepcopy(artifact)
    if case == "population":
        r["exact_native_population_censuses"][0]["uniform_target_mean_success_exact"] = "0"
    elif case == "layer":
        r["one_layer_public_angle_menu"][0]["state_amplitudes_numeric"][0] = [2.0, 0.0]
    elif case == "scope":
        r["multiple_layers_are_not_excluded"] = False
    elif case == "net":
        r["one_layer_adaptive_scaling_ledgers"][-1]["implicit_angle_net_points_total"] = "1"
    else:
        r["one_layer_public_angle_menu"][0]["normalized_uniform_fiber_overlap_squared_numeric"] = 1.0
    f = tmp_path/"bad.json"; f.write_text(json.dumps(r))
    result = subprocess.run(["node", "research/certificates/ternary_hot_phase_mixer_crosscheck.js", str(f)], capture_output=True, text=True)
    assert result.returncode != 0
