from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import json
import math
import random

import numpy as np
import pytest

from cyclotomic_rescaling_gate import _lambda, ideal_chart, multiply, pairing
from cyclotomic_fiber_receiver import (
    ExactFiberIndex, FrequencySource, erase_uniform_rank, frequency_coordinates,
    frequency_matrix, inverse_frequency_coordinates, native_source, receiver_control,
    general_native_frequency_matrix, run_controls, scaling_ledger, source_bijection_control,
)


def labels(level=4, dimension=2, inputs=6, seed=47011):
    rng = random.Random(seed)
    a, _, b = ideal_chart(level)[0]
    return [[(rng.randrange(a), rng.randrange(b)) for _ in range(dimension)] for _ in range(inputs)]


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("level", [2, 4, 6])
def test_native_even_source_is_exact_uniform_product_frequency_pair(level):
    r = source_bijection_control(level)
    q = r["integer_secret_modulus"]
    assert r["exhaustive_native_label_count"] == q*q
    assert r["matrix_determinant"] == -1
    assert r["even_level_two_frequencies_independently_uniform"]
    assert not r["public_frequency_coordinates_reveal_unknown_secret"]
    for u, v in product(range(q), repeat=2):
        y = inverse_frequency_coordinates(u, v, level)
        assert frequency_coordinates(y, level) == (u, v)


@pytest.mark.parametrize("level", [1, 3, 5])
def test_odd_source_is_constrained_not_two_free_modulus_frequencies(level):
    r = source_bijection_control(level)
    q = r["integer_secret_modulus"]
    assert r["exhaustive_native_label_count"] == q*(q//3)
    assert r["matrix_determinant"] == -3
    assert not r["even_level_two_frequencies_independently_uniform"]
    with pytest.raises(ValueError, match="second=2"):
        inverse_frequency_coordinates(0, 1, level)


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_exact_frequency_phase_matches_original_trace_for_every_bounded_label(level):
    a, _, b = ideal_chart(level)[0]
    q, _ = frequency_matrix(level)
    for y in product(range(a), range(b)):
        uv = frequency_coordinates(y, level)
        for s in range(q):
            for j in (1, 2):
                assert pairing((s, 0), multiply(y, _lambda(j, level), level), level) == Fraction(s*uv[j-1], q) % 1


def test_general_ring_secret_does_not_receive_integer_secret_coordinate_reduction():
    level, q = 4, 9
    for scalar in range(q):
        assert any(pairing((0, 1), multiply(y, _lambda(j, level), level), level)
                   != Fraction(scalar*frequency_coordinates(y, level)[j-1], q) % 1
                   for y in ((1, 0), (0, 1)) for j in (1, 2))
    with pytest.raises(ValueError, match="integer-secret"):
        receiver_control(labels(), level, [(0, 1), (1, 0)])


def test_suffix_dp_rank_and_unrank_equal_independent_lexicographic_fibers():
    source = native_source(labels(), 4)
    index = ExactFiberIndex(source)
    brute = defaultdict(list)
    for word in product(range(3), repeat=source.inputs):
        brute[source.value(word)].append(word)
    assert index.suffix[0] == {t: len(words) for t, words in brute.items()}
    for target, words in brute.items():
        for rank, word in enumerate(words):
            assert index.rank(word) == (target, rank)
            assert index.unrank(target, rank) == word
    assert index.resources()["exact_count_additions"] == 3*sum(len(c) for c in index.suffix[1:])
    assert index.resources()["stored_count_entries"] == sum(len(c) for c in index.suffix)


def test_repeated_frequencies_preserve_word_multiplicity_instead_of_unique_sums():
    source = native_source([[(0, 0)]]*4, 2)
    index = ExactFiberIndex(source)
    assert index.suffix[0] == {(0,): 81}
    for rank, word in enumerate(product(range(3), repeat=4)):
        assert index.rank(word) == ((0,), rank)
        assert index.unrank((0,), rank) == word
    with pytest.raises(ValueError, match="empty fiber"):
        index.unrank((1,), 0)
    with pytest.raises(ValueError, match="outside"):
        index.unrank((0,), 81)


@pytest.mark.parametrize("size", [1, 2, 7, 81])
def test_public_rank_erasure_is_unitary_on_arbitrary_inputs_not_unknown_state_inverse(size):
    rng = np.random.default_rng(47101+size)
    vector = rng.normal(size=size)+1j*rng.normal(size=size)
    erased = erase_uniform_rank(vector)
    assert np.linalg.norm(erased) == pytest.approx(np.linalg.norm(vector))
    assert np.max(abs(erase_uniform_rank(erased)-vector)) < 4e-12
    uniform = np.ones(size)/math.sqrt(size)
    expected = np.zeros(size)
    expected[0] = 1
    assert np.max(abs(erase_uniform_rank(uniform)-expected)) < 4e-12
    assert np.max(abs(erase_uniform_rank(expected)-uniform)) < 4e-12


def test_full_secret_receiver_uses_original_even_source_and_keeps_high_digits(report):
    rows = report["native_full_secret_receiver_controls"]
    assert len(rows) == 9
    assert {r["parent_level"] for r in rows} == {2, 4, 6}
    for r in rows:
        q, n = r["full_secret_modulus"], len(r["integer_secret_calibration"])
        assert r["full_integer_secret_group_size"] == q**n
        assert sum(r["all_full_secret_Fourier_outcome_probabilities"]) == pytest.approx(1)
        assert r["actual_full_secret_recovery_probability"] == pytest.approx(r["optimal_covariant_measurement_probability"])
        assert r["rank_register_leakage_probability"] < 3e-25
        assert r["nonzero_rank_outcomes_retained_as_failure"]
        assert not r["higher_secret_digits_discarded"]
        assert not r["unknown_state_preparation_or_inverse_used_by_receiver"]
        assert not r["exponential_DP_preprocessing_ignored"]
        assert r["classical_DP_resources"]["preprocessing_is_polynomial_in_group_size_not_its_log"]
    assert any(r["integer_secret_calibration"][0] == 26 for r in rows)


def test_reference_measurement_and_dual_certificate_are_optimal_on_full_secret_family():
    source = native_source(labels(4, 1, 4), 4)
    index = ExactFiberIndex(source)
    words = list(product(range(3), repeat=source.inputs))
    values = [source.value(word)[0] for word in words]
    q, D = source.modulus, len(words)
    states = np.array([[np.exp(2j*math.pi*s*t/q)/math.sqrt(D) for t in values] for s in range(q)])
    measurement = np.array([[np.exp(-2j*math.pi*s*t/q)/math.sqrt(q*index.suffix[0][(t,)])
                             for t in values] for s in range(q)])
    fibers = []
    weights = []
    for target, count in index.suffix[0].items():
        fibers.append(np.array([int(t == target[0])/math.sqrt(count) for t in values]))
        weights.append(math.sqrt(count/D))
    projector = sum(np.outer(v, v.conj()) for v in fibers)
    assert np.max(abs(measurement.conj().T @ measurement-projector)) < 4e-12
    Y = sum(w*np.outer(v, v.conj()) for v, w in zip(fibers, weights))*sum(weights)/q
    bound = sum(weights)**2/q
    for state in states:
        assert np.linalg.eigvalsh(Y-np.outer(state, state.conj())/q).min() > -4e-12
    actual = sum(abs((measurement @ states.T)[s, s])**2 for s in range(q))/q
    assert actual == pytest.approx(bound)
    assert np.trace(Y).real == pytest.approx(bound)


def test_measuring_public_fiber_first_erases_secret_not_a_receiver(report):
    for r in report["native_full_secret_receiver_controls"]:
        assert r["measure_public_fiber_before_readout_uniform_prior_success"] == 1/r["full_integer_secret_group_size"]
    zero = report["zero_information_countercontrol"]
    assert zero["actual_full_secret_recovery_probability"] == pytest.approx(1/3)
    assert zero["all_full_secret_Fourier_outcome_probabilities"] == pytest.approx([1/3]*3)


def test_native_to_vector_dcp_projection_is_charged_and_keeps_full_secret(report):
    for r in report["native_full_secret_receiver_controls"]:
        q, s = r["full_secret_modulus"], r["integer_secret_calibration"]
        for c in r["charged_vector_DCP_projection_controls"]:
            assert c["accepted_probability"] == pytest.approx(2/3)
            assert c["failed_probability"] == pytest.approx(1/3)
            phase = sum(a*b for a, b in zip(s, c["binary_phase_label"])) % q
            expected = [1/math.sqrt(2), np.exp(2j*math.pi*phase/q)/math.sqrt(2)]
            actual = np.array([complex(*a) for a in c["conditional_binary_amplitudes"]])
            assert np.max(abs(actual-expected)) < 4e-12
            assert c["full_integer_secret_retained"]
            assert c["all_projector_outcomes_costed"]
            assert not c["arbitrary_Gaussian_DCP_merge_supplied"]


def test_frequency_coordinate_cycle_and_inverse_extend_beyond_exhaustive_calibrations():
    rng = random.Random(47121)
    for level in range(7, 21):
        q, matrix = frequency_matrix(level)
        assert int(matrix.det()) == (-3 if level % 2 else -1)
        for _ in range(3):
            first = rng.randrange(q)
            second = (2*first+3*rng.randrange(q//3)) % q if level % 2 else rng.randrange(q)
            assert frequency_coordinates(inverse_frequency_coordinates(first, second, level), level) == (first, second)


def test_iid_even_source_collision_law_for_every_distinct_ternary_word_pair():
    pairs = list(product(range(3), repeat=2))
    words = list(product(range(3), repeat=2))
    counts = Counter()
    for left, right in product(pairs, repeat=2):
        y = [[inverse_frequency_coordinates(*uv, 2)] for uv in (left, right)]
        source = native_source(y, 2)
        values = [source.value(word) for word in words]
        for i, j in combinations(range(9), 2):
            counts[i, j] += values[i] == values[j]
    assert len(counts) == 36
    assert set(counts.values()) == {27}


def test_source_mean_optimal_information_bound_and_exact_chi_squared_moment():
    pairs = list(product(range(3), repeat=2))
    inverse = {uv: inverse_frequency_coordinates(*uv, 2) for uv in pairs}
    collision, success, supports = Fraction(), 0.0, 0
    for frequencies in product(pairs, repeat=3):
        y = tuple((inverse[uv],) for uv in frequencies)
        source = FrequencySource(y, 2, tuple(((u,), (v,)) for u, v in frequencies), 3)
        counts = Counter(source.value(word) for word in product(range(3), repeat=3))
        collision += 3*sum(Fraction(c, 27)**2 for c in counts.values())-1
        success += sum(math.sqrt(c/27) for c in counts.values())**2/3
        supports += len(counts)
    assert collision/729 == Fraction(2, 27)
    assert success/729 >= 27/29
    assert Fraction(supports, 729) >= Fraction(81, 29)


def test_growing_parameter_ledger_counts_exponential_preprocessing_without_hardness_claim(report):
    for r in report["growing_parameter_ledgers"]:
        exponent = r["vector_dimension"]*r["modulus_log3"]
        assert r["raw_native_qutrits"] == exponent+4
        assert r["full_secret_target_trits"] == exponent
        assert int(r["explicit_DP_worst_case_group_states"]) == 3**exponent
        bound = r["ideal_source_mean_PGM_success_lower_bound"]
        assert Fraction(int(bound["numerator"]), int(bound["denominator"])) == Fraction(3**(exponent+4), 3**(exponent+4)+3**exponent-1)
        entries = r["expected_final_DP_count_entries_lower_bound"]
        assert Fraction(int(entries["numerator"]), int(entries["denominator"])) == Fraction(3**(2*exponent+4), 3**(exponent+4)+3**exponent-1)
        assert not r["source_information_bound_is_new_algorithm"]
        assert not r["classical_or_quantum_optimal_runtime_lower_bound_claimed"]
    assert not any(report["claim_gate"].values())
    json.loads(json.dumps(report, allow_nan=False))


def test_exponential_reference_rejects_unbounded_work_instead_of_allocating_it():
    with pytest.raises(ValueError, match="exact DP reference capped"):
        ExactFiberIndex(native_source([[(1, 0)]], 20))
    with pytest.raises(ValueError, match="decimal exact ledger capped"):
        scaling_ledger(1025, 1)
    with pytest.raises(ValueError, match="canonical digit"):
        native_source([[(1, 0)]], 2).value([True])


def test_prime_power_target_is_not_a_same_size_finite_field():
    y = inverse_frequency_coordinates(1, 2, 4)
    source = native_source([[y]], 4)
    assert source.modulus == 9 and source.value([1]) == (1,)
    assert 3*source.value([1])[0] % source.modulus != 0
    assert 9*source.value([1])[0] % source.modulus == 0


@pytest.mark.parametrize("prime,t", list(product((2, 3, 5, 7), (1, 2, 3))))
def test_general_native_basis_and_fresh_onehot_reduction_preserve_full_secret_and_source_cost(prime, t, report):
    row = next(c for c in report["general_prime_source_and_charged_onehot_controls"]
               if c["prime"] == prime and c["modulus_logp"] == t)
    q, matrix = general_native_frequency_matrix(prime, t)
    assert abs(int(matrix.det())) == 1
    assert row["all_nonzero_native_frequencies_are_IID_uniform_Zq"]
    assert row["integer_secret_calibration"] == q-1
    assert row["onehot_projection_probability"] == pytest.approx(prime/2**(prime-1))
    assert row["failed_projection_probability"] == pytest.approx(1-prime/2**(prime-1))
    assert row["fresh_binary_registers_required"] == prime-1
    assert len(row["accepted_binary_word_indices"])+len(row["failed_binary_word_indices"]) == 2**(prime-1)
    assert not row["inverse_from_one_native_qudit_or_cloning_granted"]
    assert row["constant_overhead_requires_fixed_prime"]
    assert row["known_reduction_conformance_not_novel_algorithm"]
    exact = row["expected_binary_samples_per_native_qudit"]
    assert Fraction(int(exact["numerator"]), int(exact["denominator"])) == Fraction((prime-1)*2**(prime-1), prime)
    reverse_cost = row["expected_native_qudits_per_binary_sample"]
    assert Fraction(int(reverse_cost["numerator"]), int(reverse_cost["denominator"])) == Fraction(prime, 2)
    yield_rate = row["expected_native_qudits_yield_per_forward_binary_input"]
    assert Fraction(int(yield_rate["numerator"]), int(yield_rate["denominator"])) == Fraction(prime, (prime-1)*2**(prime-1))
    assert row["reverse_two_word_projection_probability"] == pytest.approx(2/prime)
    assert row["reverse_accepted_native_digits"] == (0, 1)
    assert row["reverse_cost_is_not_the_forward_yield"]
    cycle = row["forward_then_reverse_expected_binary_cost_per_binary_output"]
    assert Fraction(int(cycle["numerator"]), int(cycle["denominator"])) == (prime-1)*2**(prime-2)
    if prime == 3:
        assert matrix == frequency_matrix(2*t)[1]
