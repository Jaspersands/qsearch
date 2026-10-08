from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
import subprocess

import numpy as np
import pytest

from ternary_cyclic_extractor import random_even_source
from ternary_native_spectral_access import (
    DERIVATION, REPORT, adaptive_offset_countercontrol, bounded_fibers,
    calibration, complete_permutation, dense_optimal_unitary, dense_phase_error,
    fixed_offset_population_bound, population_reference, sqrt_integer_interval,
    translation_certificate,
)


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 27, 10**100+12345])
def test_radical_intervals_are_exact_not_floating(value):
    lo, hi = sqrt_integer_interval(value)
    assert lo*lo <= value <= hi*hi
    assert hi-lo <= Fraction(1, 2**40)
    if math.isqrt(value)**2 == value:
        assert lo == hi


@pytest.mark.parametrize("n,q,m", [(8, 9, 14), (12, 9, 22), (8, 27, 22), (128, 243, 638)])
def test_underfull_nondemolition_generator_obstruction_is_constant(n, q, m):
    bound = fixed_offset_population_bound(n, q, m)
    assert Fraction(bound["mean_minimum_squared_nondemolition_phase_error_lower"]) > Fraction(16, 9)
    assert bound["public_unitary_may_depend_on_all_labels"]
    assert bound["offset_must_be_fixed_nonzero_before_random_labels"]
    assert not bound["general_receiver_lower_bound"]
    assert not bound["efficient_unitary_construction_supplied"]


def test_more_source_copies_remove_existence_obstruction_not_compiler_debt():
    b = fixed_offset_population_bound(32, 81, 144)
    assert b["mean_minimum_squared_nondemolition_phase_error_lower"] == "0"
    assert Fraction(b["mean_minimum_squared_nondemolition_phase_error_upper"]) < Fraction(1, 1000000)
    assert not b["efficient_unitary_construction_supplied"]


@pytest.mark.parametrize("q,m,count", [(3, 1, 9), (3, 2, 81), (9, 1, 81)])
def test_whole_native_ensemble_replays_exact_population_pair_law(q, m, count):
    r = population_reference(q, m)
    assert r["entire_native_label_matrices_checked"] == count
    assert Fraction(r["mean_ordered_pair_over_word_dimension_exact"]) == Fraction(3**m-1, q)
    assert Fraction(r["mean_frequency_chi_squared_exact"]) == Fraction(q-1, 3**m)
    assert not r["finite_population_check_is_asymptotic_proof"]


def test_exhaustive_population_cap_does_not_accept_a_partial_ensemble():
    with pytest.raises(ValueError):
        population_reference(9, 2)


@pytest.mark.parametrize("mutation", ["word_cap", "group_cap", "duplicated_group", "outside_count", "float_count", "negative_count", "bad_root", "bad_offset"])
def test_complete_exact_native_fiber_schema_cannot_silently_truncate(mutation):
    source = random_even_source(2, 4, 2, 89811)
    if mutation in ("word_cap", "group_cap"):
        with pytest.raises(ValueError):
            bounded_fibers(source, **({"max_words": 8} if mutation == "word_cap" else {"max_group": 80}))
        return
    _, _, group, counts = bounded_fibers(source)
    group = list(group)
    if mutation == "duplicated_group":
        group.append(group[0])
    elif mutation == "outside_count":
        counts[(9, 9)] = 1
    elif mutation == "float_count":
        counts[(0, 0)] = 1.0
    elif mutation == "negative_count":
        counts[(0, 0)] = -1
    with pytest.raises(ValueError):
        translation_certificate(counts, group, (True, 0) if mutation == "bad_offset" else (1, 0), 5 if mutation == "bad_root" else 9)


def test_native_unitary_reference_attains_radical_optimum_not_only_permutation(artifact):
    c = artifact["native_controls"][2]
    values = [tuple(y) for y in c["complete_frequency_values"]]
    group = tuple(product(range(9), repeat=1))
    counts = Counter(values)
    cert = translation_certificate(counts, group, (1,), 9)
    assert Fraction(cert["optimal_arbitrary_public_unitary_mean_overlap_lower"]) > Fraction(cert["optimal_public_permutation_mean_overlap_exact"])
    U = dense_optimal_unitary(values, group, (1,), 9)
    assert np.linalg.norm(U.conj().T@U-np.eye(len(values)), ord=2) < 1e-12
    error = dense_phase_error(U, values, group, (1,), 9)
    assert float(Fraction(cert["minimum_arbitrary_unitary_mean_squared_phase_error_lower"]))-1e-10 <= error
    assert error <= float(Fraction(cert["minimum_arbitrary_unitary_mean_squared_phase_error_upper"]))+1e-10


def test_full_occupied_native_fibers_allow_q_order_unitary_but_not_exact_permutation(artifact):
    c = artifact["native_controls"][2]
    assert all(y["count"] for y in c["complete_fiber_counts"])
    values = [tuple(y) for y in c["complete_frequency_values"]]
    group = tuple(product(range(9), repeat=1))
    U = dense_optimal_unitary(values, group, (1,), 9)
    assert np.linalg.norm(np.linalg.matrix_power(U, 9)-np.eye(len(values)), ord=2) < 1e-10
    assert not c["translations"][0]["certificate"]["exact_frequency_translation_permutation_exists"]
    assert not c["translations"][0]["dense_reference_is_efficient_compiler"]


def test_native_frequency_permutation_attains_matching_optimum(artifact):
    for c in artifact["native_controls"]:
        values = [tuple(y) for y in c["complete_frequency_values"]]
        for t in c["translations"]:
            d = tuple(t["certificate"]["fixed_frequency_offset"])
            P = complete_permutation(values, d, c["modulus"])
            assert tuple(t["reference_word_permutation"]) == P
            assert sorted(P) == list(range(len(values)))


def test_adaptive_label_chosen_direction_is_not_granted_fixed_offset_population_bound():
    c = adaptive_offset_countercontrol()
    assert c["offset_was_chosen_from_labels"]
    assert Fraction(c["certificate"]["optimal_arbitrary_public_unitary_mean_overlap_lower"]) > Fraction(c["fixed_offset_population_ledger"]["mean_optimal_arbitrary_unitary_phase_overlap_upper"])
    assert not c["fixed_offset_population_bound_applies_to_this_selected_offset"]
    assert not c["one_instance_is_an_ensemble_refutation"]


def test_diagonal_secret_encoding_commutant_is_uninformative_but_mixing_can_be_informative():
    # Genuine native q3 one-input field-root source, not an invented oracle.
    c = population_reference(3, 1)
    assert c["complete_native_chart_replayed"]
    omega = np.exp(2j*np.pi/3)
    diagonal = np.diag([1, omega, omega**2])
    fourier = np.array([[omega**(-a*b) for b in range(3)] for a in range(3)])/math.sqrt(3)
    computational, informative = [], []
    for secret in range(3):
        psi = np.array([1, omega**secret, omega**(2*secret)])/math.sqrt(3)
        computational.append(np.abs(diagonal@psi)**2)
        informative.append(np.abs(fourier@psi)**2)
    assert all(np.allclose(p, computational[0]) for p in computational)
    assert all(np.argmax(p) == s for s, p in enumerate(informative))
    assert not np.allclose(informative[0], informative[1])


def test_live_native_sources_reproduce_artifacts_and_have_no_compiler_claim(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    for c in artifact["native_controls"]:
        regenerated = calibration(c["dimension"], c["modulus"], c["source_inputs"], c["seed"])
        assert json.loads(json.dumps(regenerated)) == c
        assert not c["source_has_IID_population_law_from_calibration_seed"]
    assert not artifact["native_spectral_generator_compiler_supplied"]
    assert not artifact["generic_quantum_receiver_lower_bound"]
    assert not artifact["candidate_record_accepted"]


def test_independent_access_checker_reconstructs_native_counts_and_full_populations():
    checker = REPORT.parents[1]/"certificates/ternary_native_spectral_access_crosscheck.js"
    result = subprocess.run(["node", str(checker)], check=True, capture_output=True, text=True)
    r = json.loads(result.stdout)
    assert r["status"] == "PASS"
    assert r["native_words_checked"] == 66
    assert r["reference_translation_permutations"] == 10
    assert r["complete_native_label_matrices_checked"] == 171


@pytest.mark.parametrize("mutation", ["generic_lower_bound", "fiber_count", "radical_interval", "permutation", "adaptive_scope"])
def test_independent_checker_rejects_inflated_scope_and_bad_evidence(artifact, tmp_path, mutation):
    r = deepcopy(artifact)
    c = r["native_controls"][0]
    if mutation == "generic_lower_bound":
        r["generic_quantum_receiver_lower_bound"] = True
    elif mutation == "fiber_count":
        c["complete_fiber_counts"][0]["count"] += 1
    elif mutation == "radical_interval":
        c["translations"][0]["certificate"]["all_nonzero_radical_terms"][0]["sqrt_product_lower"] = "999"
    elif mutation == "permutation":
        c["translations"][0]["reference_word_permutation"][0] = c["translations"][0]["reference_word_permutation"][1]
    else:
        r["adaptive_offset_scope_countercontrol"]["fixed_offset_population_bound_applies_to_this_selected_offset"] = True
    output = tmp_path/"bad.json"
    output.write_text(json.dumps(r))
    checker = REPORT.parents[1]/"certificates/ternary_native_spectral_access_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(output)], capture_output=True, text=True)
    assert result.returncode != 0 and not result.stdout
