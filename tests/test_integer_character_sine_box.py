from fractions import Fraction as Q
from itertools import product
import json
from math import isqrt

import numpy as np
import pytest

from theorems import integer_character_interpolation as base
from theorems import integer_character_sine_box as s


@pytest.mark.parametrize("m,tolerance", [
    (1, Q(1, 3)), (32, Q(1, 4)), (20000, Q(1, 10)),
    (20001, Q(1, 1000)), (10**12, Q(1, 100)),
])
def test_exact_uniform_width_and_all_coordinate_success_ledger(m, tolerance):
    row = s.budget(m, tolerance)
    w = row["half_width"]
    assert w*w*tolerance*tolerance >= m
    assert (w-1)**2*tolerance*tolerance < m
    assert Q(row["ideal_failure_upper"]) < Q(5, 32)
    assert Q(row["implemented_success_lower"]) > Q(13, 16)
    assert Q(row["failure_probability_upper"]) < Q(1, 2**row["full_trials"])
    assert Q(row["source_unitary_operator_error_budget"])+Q(row["fourier_operator_error_budget"]) == Q(1, 32)
    assert not row["source_postselection"]


@pytest.mark.parametrize("width", [1, 2, 3, 8, 31])
def test_sine_path_source_normalization_eigenvalue_and_moment(width):
    weights = np.sin(np.pi*np.arange(1, 2*width+2)/(2*width+2))/np.sqrt(width+1)
    assert abs(np.dot(weights, weights)-1) < 2e-15
    overlap = np.dot(weights[:-1], weights[1:])
    lo, hi = s.moment_interval(width)
    assert float(lo)-1e-15 <= overlap <= float(hi)+1e-15
    assert hi-lo < Q(1, 10**30)
    path = np.diag(np.ones(2*width), 1)+np.diag(np.ones(2*width), -1)
    np.testing.assert_allclose(path@weights, 2*float((lo+hi)/2)*weights, atol=2e-15)


@pytest.mark.parametrize("primes,width", [((2, 5), 1), ((2, 5), 2), ((2, 5, 7), 1)])
def test_full_source_decoder_and_independent_output_law(primes, width):
    row = s.small_control(primes, width, 13)
    assert row["source_words_checked"] == (2*width+1)**len(primes)
    assert row["whole_law_max_residual"] < 1e-12
    assert max(abs(x-row["expected_coordinate_mean"]) for x in row["coordinate_cosine_means"]) < 1e-12
    assert row["mean_squared_torus_distance"] <= row["squared_distance_upper"]


def test_decoder_really_accepts_large_magnitudes_not_only_signed_trits():
    instance = s.construct((2, 5, 7), 3)
    seen = set()
    for word in product(range(-3, 4), repeat=3):
        syndrome = sum(a*y for a, y in zip(instance["labels"], word)) % instance["order"]
        assert syndrome not in seen
        seen.add(syndrome)
        assert s.decode(instance, syndrome) == word
    # A public prime outside the source alphabet is not an admissible word.
    outside = base.lifted_log(11, instance["exponent"])[0]
    assert s.decode(instance, outside) is None


def test_corrected_height_guard_is_new_and_minimal_for_its_definition():
    instance = s.construct((2, 5), 2)
    assert instance["modulus"] > instance["guard"]
    assert instance["modulus"]//3 <= instance["guard"]
    assert instance["height"] < isqrt((instance["modulus"]-1)//2)
    with pytest.raises(ValueError, match="guard"):
        s.license_box((2, 5), 2, instance["exponent"]-1)
    old = base.construct((2, 5), 0)
    with pytest.raises(ValueError, match="guard"):
        s.license_box((2, 5), 2, old["exponent"])


def test_failure_to_erase_word_destroys_the_claimed_cosine_bias():
    instance = s.construct((2, 5), 1)
    n = instance["order"]
    # Trace out orthogonal word labels: every syndrome basis state gives
    # the same uniform QFT law, regardless of its source probability.
    uniform = np.full(n, 1/n)
    outputs = np.arange(n)
    for a in instance["labels"]:
        assert abs(np.dot(uniform, np.cos(2*np.pi*((a*outputs) % n)/n))) < 1e-15
    assert s.moment_interval(1)[0] > Q(7, 10)


def test_exact_verifier_checks_every_coordinate_and_charges_boundary():
    instance = s.construct((2, 5), 1)
    n = instance["order"]
    x = n-7
    centers = tuple(a*x % n for a in instance["labels"])
    assert s.verify(instance, centers, x, Q(1, 100))["accepted"]
    bad = (centers[0], (centers[1]+n//2) % n)
    rejected = s.verify(instance, bad, x, Q(1, 4))
    assert not rejected["accepted"]
    assert rejected["maximum_normalized_error"] == Q(1, 2)
    near = ((centers[0]+1) % n, centers[1])
    assert s.verify(instance, near, x, Q(1, n))["accepted"]
    assert not s.verify(instance, near, x, Q(1, n+1))["accepted"]


@pytest.mark.parametrize("call", [
    lambda: s.budget(0, Q(1, 10)),
    lambda: s.budget(True, Q(1, 10)),
    lambda: s.budget(32, 0.1),
    lambda: s.budget(32, Q(1, 2)),
    lambda: s.budget(32, 0),
    lambda: s.budget(32, Q(1, 10), failure_bits=0),
    lambda: s.construct((2, 3), 2),
    lambda: s.construct((2, 5), 0),
    lambda: s.moment_interval(2, precision=32),
    lambda: s.license_box((2, 5), 1, True),
])
def test_invalid_inputs_fail_closed(call):
    with pytest.raises(ValueError):
        call()


def test_dense_control_never_silently_expands_to_native_space():
    with pytest.raises(ValueError, match="cap"):
        s.small_control((2, 5), 3, 1)


def test_invalid_output_and_syndrome_inputs():
    instance = s.construct((2, 5), 1)
    with pytest.raises(ValueError):
        s.decode(instance, instance["order"])
    with pytest.raises(ValueError):
        s.verify(instance, (0, 0.0), 0, Q(1, 10))
    with pytest.raises(ValueError):
        s.verify(instance, (0, 0), instance["order"], Q(1, 10))


def test_native_report_replays_public_labels_and_boundary_decoding():
    if not s.REPORT.exists():
        pytest.skip("live report not yet generated")
    report = json.loads(s.REPORT.read_text())
    row = report["native"]
    primes, width = tuple(row["primes"]), row["budget"]["half_width"]
    instance = s.license_box(primes, width, row["modulus_exponent"])
    instance.update(primes=primes, width=width,
                    labels=tuple(int(a, 16) for a in row["labels_hex"]))
    assert instance["order"] == int(row["cyclic_order_hex"], 16)
    base.validate_public_labels(primes, instance["labels"], instance["exponent"])
    for control in row["decoder_controls"]:
        word, syndrome = tuple(control["word"]), int(control["syndrome_hex"], 16)
        assert sum(a*y for a, y in zip(instance["labels"], word)) % instance["order"] == syndrome
        assert s.decode(instance, syndrome) == word
    classical = row["classical_same_task"]
    rows = tuple(tuple(int(v, 16) for v in r) for r in classical["basis_hex"])
    centers = tuple(int(v, 16) for v in classical["centers_hex"])
    exact = s.babai.exact_normalized_babai(rows, instance["labels"], instance["order"], centers)
    assert exact["assignment"] == int(classical["assignment_hex"], 16)
    radius_squared = exact["normalized_gs_trace_upper"]/4
    assert radius_squared == Q(classical["all_target_squared_euclidean_radius_upper"])
    assert radius_squared <= Q(row["budget"]["normalized_phase_tolerance"])**2
    assert s.verify(instance, centers, exact["assignment"], Q(1, 4))["accepted"]
    assert classical["all_target_max_coordinate_tolerance_certified"]
    assert not row["scalable_quantum_circuit_compiled"]
    assert row["quantum_output_samples_generated"] == 0
    assert not report["classical_hardness_or_speedup_established"]
    assert not report["old_modulus_or_benchmark_reused"]
