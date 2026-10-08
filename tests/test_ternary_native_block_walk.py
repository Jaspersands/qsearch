from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
import random
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_cyclic_extractor import random_even_source
from ternary_native_block_walk import (
    DERIVATION, REPORT, NativeBlockHeatbath, collision_population_bound,
    complete_signature_audit, quarter_distance_certificate, signature_count, transition_reference,
)


@pytest.fixture(scope="module")
def walk():
    return NativeBlockHeatbath(random_even_source(2, 4, 5, 89881))


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


@pytest.mark.parametrize("m,k", [(1, 1), (5, 1), (5, 2), (5, 3), (5, 5), (1000, 5)])
def test_opposite_signatures_are_one_zero_event(m, k):
    assert signature_count(m, k) == sum(math.comb(m, j)*6**j for j in range(1, k+1))//2
    if k == m:
        assert signature_count(m, k) == (7**m-1)//2


@pytest.mark.parametrize("args", [(True, 9, 5, 1), (2, 5, 5, 1), (2, 9.0, 5, 1), (2, 9, 5, 0), (2, 9, 5, 6), (2, 9, 5, True)])
def test_population_schema_retains_the_actual_root_and_support(args):
    with pytest.raises(ValueError):
        collision_population_bound(*args)


def test_global_small_support_obstruction_survives_polynomial_sample_surplus():
    result = collision_population_bound(128, 243, 648, 5)
    probability = Fraction(result["probability_any_nontrivial_small_support_fiber_collision_upper"])
    assert 0 < probability < Fraction(1, 2**900)
    assert result["label_and_word_adaptive_block_policies_covered"]
    assert not result["generic_quantum_receiver_lower_bound"]
    assert result["temporary_prefix_violations_or_nonlocal_macros_are_outside_scope"]


@pytest.mark.parametrize("n,q,c", [(8, 9, 0), (32, 81, 4), (128, 243, 8), (512, 729, 8)])
def test_near_entropy_native_fibers_require_extensive_collision_moves(n, q, c):
    result = quarter_distance_certificate(n, q, c)
    assert result["minimum_full_fiber_collision_distance_on_no_event"] == result["source_inputs"]//4+1
    exact = Fraction(result["exact_signature_population_ledger"]["probability_any_nontrivial_small_support_fiber_collision_upper"])
    bound = Fraction(result["simple_rational_collision_probability_upper"])
    assert exact <= bound <= 1
    assert Fraction(result["fourth_power_base_comparison_left"]) <= Fraction(result["fourth_power_base_comparison_right"])
    assert result["polynomial_gate_macros_with_many_changed_coordinates_not_excluded"]
    assert not result["distance_certificate_is_efficient_partner_finder"]
    if n >= 128:
        assert bound < Fraction(1, 2**60)


def test_simple_quarter_distance_envelope_is_not_extrapolated_to_an_arbitrary_batch():
    result = quarter_distance_certificate(8, 9, 1000)
    assert result["simple_rational_collision_probability_upper"] == "1"


def test_actual_one_site_frozen_source_has_many_nontrivial_fibers(walk):
    ref = transition_reference(walk, 1)
    audit = complete_signature_audit(walk, 1)
    assert audit["all_small_moves_frozen_certified"]
    assert len(ref["connected_components"]) == 243
    assert ref["raw_source_mass_in_nontrivial_FULL_frequency_fibers"] == "233/243"
    assert all(row == [[i, "1"]] for i, row in enumerate(ref["conditional_transition_rows"]))
    assert ref["full_native_source_family_stationary_certified"]
    assert all(f["fiber_mixing_gap_certified_lower"] == "0" for f in ref["prefix_fibers"] if len(f["word_indices"]) > 1)


def test_full_block_restores_gap_one_but_charges_exponential_local_table(walk):
    ref = transition_reference(walk, 5)
    assert all(f["fiber_mixing_gap_certified_lower"] == "1" for f in ref["prefix_fibers"])
    assert all(f["exact_gap_one_complete_heatbath"] for f in ref["prefix_fibers"])
    assert not ref["reference_is_scalable_walk_compiler"]
    step = walk.random_step((0,)*5, 5, random.Random(7))
    assert step["local_word_evaluations_charged"] == 243
    assert not step["quantum_state_preparation_implemented"]


def test_low_prefix_kernel_cannot_be_substituted_for_full_root(walk):
    low = NativeBlockHeatbath(walk.source, 3)
    ref = transition_reference(low, 2)
    assert ref["prefix"] == 3
    assert not ref["full_native_source_family_stationary_certified"]
    values = ref["full_frequency_values"]
    assert any(values[i] != values[j] for i, row in enumerate(ref["conditional_transition_rows"]) for j, _ in row)


@pytest.mark.parametrize("support", [1, 2, 3])
def test_complete_signature_witnesses_are_actual_native_collisions(walk, support):
    audit = complete_signature_audit(walk, support)
    assert int(audit["unoriented_signatures_checked"]) == signature_count(5, support)
    for witness in audit["zero_signatures"]:
        assert walk.source.value(witness["first_word"]) == walk.source.value(witness["second_word"])
        assert sum(a != b for a, b in zip(witness["first_word"], witness["second_word"])) <= support


def test_global_no_move_flag_never_comes_from_a_partial_signature_scan(walk):
    result = complete_signature_audit(walk, 5, max_signatures=100)
    assert result["status"] == "UNKNOWN_COMPLETE_SIGNATURE_CAP"
    assert not result["complete_vocabulary_checked"]
    assert not result["all_small_moves_frozen_certified"]


@pytest.mark.parametrize("cap", [0, True, 26])
def test_local_conditionals_reject_invalid_or_partial_tables(walk, cap):
    with pytest.raises(ValueError):
        walk.compatible_assignments((0,)*5, (0, 1, 2), max_local_words=cap)


@pytest.mark.parametrize("block", [(), (1, 0), (0, 0), (0, 5), (True,), (1.0,)])
def test_update_block_is_a_canonical_set_of_native_coordinates(walk, block):
    with pytest.raises(ValueError):
        walk.step((0,)*5, block)


@pytest.mark.parametrize("word", [(0,)*4, (0, 0, 0, 0, 3), (0, 0, 0, 0, True)])
def test_native_word_schema_is_not_a_binary_shadow(walk, word):
    with pytest.raises(ValueError):
        walk.step(word, (0,))


@pytest.mark.parametrize("prefix", [1, 5, 27, 9.0, True])
def test_prefix_must_be_a_real_divisor_of_original_native_root(walk, prefix):
    with pytest.raises(ValueError):
        NativeBlockHeatbath(walk.source, prefix)


def test_random_step_selects_one_block_not_the_exponential_block_menu(monkeypatch):
    source = random_even_source(8, 4, 128, 89883)
    program = NativeBlockHeatbath(source)
    monkeypatch.setattr("ternary_native_block_walk.combinations", lambda *_: pytest.fail("block menu was enumerated"))
    monkeypatch.setattr("ternary_native_block_walk.bounded_fibers", lambda *_: pytest.fail("whole native cube was enumerated"))
    step = program.random_step((0,)*128, 3, random.Random(5))
    assert step["local_word_evaluations_charged"] == 27
    assert source.value(step["initial_word"]) == source.value(step["word"])
    assert not step["full_fiber_count_oracle_used"]


def test_complete_reference_caps_checked_before_materializing_blocks(monkeypatch):
    source = random_even_source(8, 4, 128, 89883)
    program = NativeBlockHeatbath(source)
    monkeypatch.setattr("ternary_native_block_walk.combinations", lambda *_: pytest.fail("uncapped huge block list was materialized"))
    with pytest.raises(ValueError):
        transition_reference(program, 64)


@pytest.mark.parametrize("kwargs", [{"max_words": 242}, {"max_work": 100}, {"max_work": True}])
def test_complete_transition_kernel_cannot_hide_partial_rows(walk, kwargs):
    with pytest.raises(ValueError):
        transition_reference(walk, 3, **kwargs)


def test_every_full_prefix_kernel_is_PSD_and_stationary_on_native_secret_states(artifact):
    for trial in artifact["live_trials"][:4]:
        ref = trial["reference"]
        P = np.zeros((243, 243))
        for i, row in enumerate(ref["conditional_transition_rows"]):
            for j, w in row:
                P[i, j] = float(Fraction(w))
        assert np.allclose(P, P.T)
        assert np.linalg.eigvalsh(P).min() > -1e-12
        values = np.array(ref["full_frequency_values"])
        for s in ((0, 0), (1, 0), (1, 3), (8, 8)):
            psi = np.exp(2j*np.pi*(values@np.array(s))/9)/np.sqrt(243)
            assert np.linalg.norm(P@psi-psi) < 1e-12


def test_reference_gap_lower_bound_is_conservative_against_numeric_spectrum(artifact):
    for trial in artifact["live_trials"]:
        ref = trial["reference"]
        P = np.zeros((243, 243))
        for i, row in enumerate(ref["conditional_transition_rows"]):
            for j, w in row:
                P[i, j] = float(Fraction(w))
        for fiber in ref["prefix_fibers"]:
            indices = fiber["word_indices"]
            if len(indices) == 1:
                continue
            eigen = np.linalg.eigvalsh(P[np.ix_(indices, indices)])
            gap = max(0., 1-eigen[-2])
            assert float(Fraction(fiber["fiber_mixing_gap_certified_lower"])) <= gap+1e-12
            if fiber["exact_gap_zero_certified"]:
                assert gap < 1e-12


def test_a_frozen_walk_is_not_a_general_receiver_no_go():
    label = inverse_frequency_coordinates(1, 2, 2)
    source = native_source(((label,),), 2)
    walk = NativeBlockHeatbath(source)
    ref = transition_reference(walk, 1)
    assert complete_signature_audit(walk, 1)["all_small_moves_frozen_certified"]
    assert ref["raw_source_mass_in_nontrivial_FULL_frequency_fibers"] == "0"
    # This known field-root native instance has an exact Fourier decoder.
    omega = np.exp(2j*np.pi/3)
    QFT = np.array([[omega**(-a*b) for b in range(3)] for a in range(3)])/np.sqrt(3)
    for s in range(3):
        psi = np.array([omega**(s*source.value((x,))[0]) for x in range(3)])/np.sqrt(3)
        assert abs((QFT@psi)[s])**2 > 1-1e-12


def test_live_rows_and_signature_atlases_reproduce_exactly(walk, artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    for trial in artifact["live_trials"]:
        ref = trial["reference"]
        program = NativeBlockHeatbath(walk.source, ref["prefix"])
        assert json.loads(json.dumps(transition_reference(program, ref["support"]))) == ref
        assert json.loads(json.dumps(complete_signature_audit(program, ref["support"]))) == trial["signature_audit"]
    assert not artifact["efficient_fiber_eraser_supplied"]
    assert not artifact["candidate_record_accepted"]


def test_independent_block_walk_checker_replays_every_transition_and_signature():
    checker = REPORT.parents[1]/"certificates/ternary_native_block_walk_crosscheck.js"
    completed = subprocess.run(["node", str(checker)], check=True, capture_output=True, text=True)
    result = json.loads(completed.stdout)
    assert result["status"] == "PASS"
    assert result["exact_native_transition_rows"] == 1215
    assert result["unoriented_difference_signatures"] == 10083
    assert result["disconnected_fiber_gap_certificates"] == 151


@pytest.mark.parametrize("mutation", ["receiver_no_go", "prefix", "gap", "transition", "omit_signature", "population", "free_compiler"])
def test_independent_checker_rejects_fake_evidence_and_inflated_scope(artifact, tmp_path, mutation):
    report = deepcopy(artifact)
    trial = report["live_trials"][0]
    if mutation == "receiver_no_go":
        report["generic_quantum_receiver_lower_bound"] = True
    elif mutation == "prefix":
        trial["reference"]["prefix"] = 3
    elif mutation == "gap":
        f = next(f for f in trial["reference"]["prefix_fibers"] if f["exact_gap_zero_certified"])
        f["fiber_mixing_gap_certified_lower"] = "1"
    elif mutation == "transition":
        trial["reference"]["conditional_transition_rows"][0] = [[0, "1/2"]]
    elif mutation == "omit_signature":
        report["live_trials"][1]["signature_audit"]["zero_signatures"].pop()
    elif mutation == "population":
        report["global_small_move_population_ledgers"][0]["probability_any_nontrivial_small_support_fiber_collision_upper"] = "0"
    else:
        report["efficient_fiber_eraser_supplied"] = True
    path = tmp_path/"bad.json"
    path.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_native_block_walk_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(path)], capture_output=True, text=True)
    assert result.returncode != 0 and not result.stdout
