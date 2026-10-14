"""Actual-source local tests, classical precision and false-prefix falsifiers."""
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
import json
import subprocess

import numpy as np
import pytest

from theorems import native_word_local_decision as L
from native_full_root_slice import source_data
from native_word_frame_access import finite_frame


def stored(): return json.loads(L.REPORT.read_text())


def source(n=1, r=2, M=4, seed=101001):
    raw, mask, truth, errors = source_data(n, r, M, False, seed)
    return raw, mask, truth, errors, L.PairedWordSource(L.public_family(raw, 1, M))


@pytest.mark.parametrize("r", (1, 2, 16, 64))
def test_original_pair_frequency_adapter_preserves_actual_word_map(r):
    raw, _, _, _, s = source(r=r, M=3)
    base = tuple(sum(pair[0][i] for pair in s.family.paired_labels[0]) % s.modulus for i in range(s.dimension))
    for w in product(range(3), repeat=3):
        shifted = tuple((b+sum(s.frequencies[j][t-1][i] if t else 0 for j, t in enumerate(w))) % s.modulus for i, b in enumerate(base))
        assert shifted == s.value(w)
    assert len(raw) == 2*s.inputs


def test_offset_chart_is_not_jointly_uniform_even_with_uniform_original_pairs():
    q = 9
    counts = {}
    for a, c in product(range(q), repeat=2):
        pair = ((c-2*a) % q, (-c-a) % q)
        counts[pair] = counts.get(pair, 0)+1
    assert len(counts) == q*q//3 and set(counts.values()) == {3}
    for u, v in ((2, -1), (1, 1), (-1, 2)):
        population = [((u*a+v*c) % q) for a, c in product(range(q), repeat=2)]
        assert all(population.count(x) == q for x in range(q))


def test_frozen_small_move_control_has_null_one_despite_large_nontrivial_fibres():
    c = stored()["actual_paired_source_controls"][0]
    assert c["full_fibre_span_rank"] == 9 and c["ground_rank"] == 81
    assert c["whole_small_signature_audit"]["all_small_moves_frozen_certified"]
    assert c["exact_ground_IID_null_acceptance"] == "1"
    assert c["Hamiltonian_identically_zero"] and c["positive_Hamiltonian_gap_lower"] is None
    assert c["exact_ground_acceptance_polynomial"] == ["1"]


def test_partial_connectivity_has_more_ground_components_than_frequency_fibres():
    c = stored()["actual_paired_source_controls"][1]
    assert c["ground_rank"] == 13 > c["full_fibre_span_rank"] == 9
    assert c["exact_ground_IID_null_acceptance"] == "13/81"
    assert any(f["exact_gap_zero_certified"] for f in c["heatbath_reference"]["prefix_fibers"])
    assert Fraction(c["positive_Hamiltonian_gap_lower"]) > 0  # Gap above all component kernels, not unique-fibre mixing.
    assert c["full_root_source_moment_bound_applicable"]


def test_complete_block_reference_is_projection_but_explicitly_exponential():
    c = stored()["actual_paired_source_controls"][2]
    assert c["ground_rank"] == c["full_fibre_span_rank"] == 9
    assert c["exact_ground_IID_null_acceptance"] == "1/9"
    assert c["positive_Hamiltonian_gap_lower"] == "1"
    assert c["heatbath_reference"]["whole_reference_work_upper"] == str(81**2)
    assert c["classical_first_block_expectation"]["local_words_evaluated"] == 81
    assert not c["dense_kernel_is_an_efficient_ground_effect"]


def test_prefix_only_apparent_improvement_loses_ideal_full_root_source():
    c = stored()["actual_paired_source_controls"][3]
    assert Fraction(c["exact_ground_IID_null_acceptance"]) < Fraction(1, 9)
    assert c["diagnostic_ideal_source_ground_acceptance"] == pytest.approx(2/27)
    assert not c["full_root_source_moment_bound_applicable"]
    assert c["conditional_pathwise_ground_rejection_upper"] is None
    assert not c["heatbath_reference"]["full_native_source_family_stationary_certified"]


def test_prefix_effect_does_not_inherit_adaptive_mask_null_invariance():
    from ternary_noise_degradation import NoisyLinearRecord
    raw = tuple(NoisyLinearRecord((1,), 0, 9, f"prefix-mask-{j}") for j in range(4))
    walk = L.PairedWordHeatbath(L.PairedWordSource(L.public_family(raw, 1, 2)), 3)
    reference = L.transition_reference(walk, 2)
    words, phases, frequencies = tuple(product(range(3), repeat=2)), [], []
    for w in words:
        phases.append(tuple(x for t in w for x in ((1, 0), (-1, 1), (0, -1))[t]))
        frequencies.append(walk.source.value(w)[0])
    P = np.zeros((9, 9))
    for i, row in enumerate(reference["conditional_transition_rows"]):
        for j, p in row: P[i, j] = float(Fraction(p))
    all_values = np.asarray(tuple(product(range(9), repeat=4)))
    numerators = all_values@np.asarray(phases).T
    probabilities = []
    for m in range(3):
        states = np.exp(2j*np.pi*(numerators+m*np.asarray(frequencies))/9)/3
        probabilities.append(np.einsum("bi,ij,bj->b", states.conj(), P, states).real)
    assert np.mean(probabilities[0]) == pytest.approx(1/3)
    # A mask selected from the actual values can maximize this prefix statistic.
    assert np.mean(np.max(probabilities, axis=0)) > .4


@pytest.mark.parametrize("index", range(4))
def test_all_finite_kernel_spectra_certify_PSD_absolute_gap_and_ground_rank(index):
    c = stored()["actual_paired_source_controls"][index]
    rows = c["heatbath_reference"]["conditional_transition_rows"]
    P = np.zeros((81, 81))
    for i, row in enumerate(rows):
        for j, w in row: P[i, j] = float(Fraction(w))
    spectrum = np.linalg.eigvalsh(np.eye(81)-P)
    assert np.max(abs(P-P.T)) < 1e-12 and np.min(np.linalg.eigvalsh(P)) >= -1e-12
    assert sum(abs(spectrum) < 1e-10) == c["ground_rank"]
    positive = spectrum[spectrum > 1e-10]
    if len(positive): assert min(positive)+1e-12 >= float(Fraction(c["positive_Hamiltonian_gap_lower"]))
    else: assert c["positive_Hamiltonian_gap_lower"] is None


def test_classical_one_block_interval_matches_actual_quantum_kernel_and_average():
    raw, mask, _, _, s = source()
    raw = tuple(type(r)(r.label, (r.value+3*j) % 9, r.modulus, r.source_id) for j, r in enumerate(raw))
    f = finite_frame(raw, mask, 1, 4);walk = L.PairedWordHeatbath(s)
    R = L.transition_reference(walk, 2)
    P = np.zeros((81, 81))
    for i, row in enumerate(R["conditional_transition_rows"]):
        for j, w in row: P[i, j] = float(Fraction(w))
    quantum = float(np.vdot(f["state"], P@f["state"]).real)
    intervals = [L.local_acceptance_interval(raw, mask, b, bits=60) for b in combinations(range(4), 2)]
    lo = sum(Fraction(c["acceptance_lower"]) for c in intervals)/6
    hi = sum(Fraction(c["acceptance_upper"]) for c in intervals)/6
    assert float(lo)-1e-12 <= quantum <= float(hi)+1e-12
    assert hi-lo <= Fraction(1, 2**60)
    assert all(not c["ground_space_projection_or_long_time_walk_simulated"] for c in intervals)


def test_large_root_local_estimator_never_enumerates_q_or_full_word_cube():
    raw, mask, _, _, _ = source(n=2, r=64, M=10)
    c = L.local_acceptance_interval(raw, mask, (0, 2), bits=80, max_local_words=9)
    assert c["original_modulus"] == 3**64 and c["local_words_evaluated"] == 9
    assert Fraction(c["acceptance_upper"])-Fraction(c["acceptance_lower"]) <= Fraction(1, 2**80)
    assert not c["all_blocks_or_whole_words_enumerated"]
    assert not c["unknown_quantum_only_phases_allowed"]


@pytest.mark.parametrize("block", ((2, 0), (0, 0), (), (0, 10), (True,)))
def test_invalid_blocks_rejected(block):
    raw, mask, _, _, _ = source()
    with pytest.raises(ValueError): L.local_acceptance_interval(raw, mask, block)


def test_whole_local_table_cap_fails_before_partial_signal_is_reported():
    raw, mask, _, _, _ = source()
    with pytest.raises(ValueError, match="whole local phase table cap"):
        L.local_acceptance_interval(raw, mask, (0, 1, 2), max_local_words=9)


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_original_law_population_bounds_round_up_and_do_not_claim_general_impossibility(n):
    M, k = n*n+12, (n+1).bit_length()
    l = L.paired_collision_ledger(n, n, M, k)
    ratio = Fraction(int(l["unoriented_difference_signatures"]), 3**(n*n))
    assert ratio <= Fraction(l["probability_any_exact_full_root_local_collision_upper"]) < Fraction(1, 2**64)
    assert not l["independent_offset_frequency_columns_assumed"]
    assert not l["generic_quantum_decoder_lower_bound_proved"]
    assert not l["temporary_syndrome_violations_or_collective_macros_excluded"]


def test_vacuous_sparse_move_bound_does_not_become_a_false_freezing_claim():
    l = L.paired_collision_ledger(1, 1, 4, 4)
    assert l["probability_any_exact_full_root_local_collision_upper"] == "1"
    assert l["probability_ground_effect_is_identity_lower"] == "0"


def run_checker(p):
    return subprocess.run(["node", "-e", "require('./research/certificates/native_word_local_decision_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')));"],
                          input=json.dumps(p), text=True, cwd=L.ROOT, capture_output=True)


def test_independent_checker_replays_live_whole_kernels_and_classical_intervals():
    p = stored();r = run_checker(p)
    assert r.returncode == 0, r.stderr
    assert not p["all_efficient_span_tests_excluded"]
    assert not p["accepted_speedup_candidate"] and not p["new_active_negative_result_created"]


@pytest.mark.parametrize("kind", ("weights", "components", "null", "gap", "prefix", "interval", "source-law", "free-projection", "population", "hash"))
def test_independent_checker_rejects_tampered_mechanism_claims(kind):
    p = deepcopy(stored());c = p["actual_paired_source_controls"][1]
    if kind == "weights": c["heatbath_reference"]["conditional_transition_rows"][0][0][1] = "0"
    elif kind == "components": c["heatbath_reference"]["connected_components"][0] = [0]
    elif kind == "null": c["exact_ground_IID_null_acceptance"] = "1/9"
    elif kind == "gap": c["positive_Hamiltonian_gap_lower"] = "1"
    elif kind == "prefix": p["actual_paired_source_controls"][3]["full_root_source_moment_bound_applicable"] = True
    elif kind == "interval": c["classical_first_block_expectation"]["acceptance_upper"] = "0"
    elif kind == "source-law": p["growing_root_local_move_ledgers"][0]["independent_offset_frequency_columns_assumed"] = True
    elif kind == "free-projection": c["dense_kernel_is_an_efficient_ground_effect"] = True
    elif kind == "population": p["growing_root_local_move_ledgers"][0]["probability_any_exact_full_root_local_collision_upper"] = "0"
    else: p["producer_sha256"] = "0"*64
    r = run_checker(p)
    assert r.returncode != 0
