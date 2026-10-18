"""Native Fourier states, MDS ambiguity, and coherent-erasure falsifiers."""

from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path

import numpy as np
import pytest
from sympy import Matrix

import theorems.prime_character_capacity_source as module
from theorems.prime_character_capacity_source import (
    REPORT, ambiguity_bound, coherent_distance_squared, local_fourier, physical_control,
    run_controls, source_profile,
)
from theorems.prime_character_opi import from_specification, instance


@pytest.mark.parametrize("p", [7, 19, 43])
@pytest.mark.parametrize("zero", [True, False])
def test_native_centered_predicate_DFT_matches_the_closed_Gauss_source(p, zero):
    problem = instance(p, 6, 3, 2, 29, mode="mixed", include_zero=zero)
    rho = float(problem.density)
    for i in range(problem.length):
        native = np.array([problem.accepted(i, x) for x in range(p)], float)
        centered = (native - rho) / math.sqrt(rho * (1 - rho))
        transformed = np.fft.fft(centered) / p
        formula = np.array([local_fourier(problem, i, xi) for xi in range(p)])
        assert np.max(abs(transformed - formula)) < 1e-12
        assert abs(formula[0]) == 0
        assert np.max(abs(abs(formula[1:]) ** 2 - 1 / (p - 1))) < 1e-12
        assert np.vdot(formula, formula).real == pytest.approx(1, abs=1e-12)


def test_prime_one_mod_four_is_a_real_nonflat_counterexample_not_an_allowed_source():
    problem = instance(5, 4, 2, 2, 29)
    values = np.array([local_fourier(problem, 0, xi) for xi in range(5)])
    assert np.ptp(abs(values[1:]) ** 2) == pytest.approx(math.sqrt(5) / 6, abs=1e-12)
    with pytest.raises(ValueError, match="congruent"):
        source_profile(problem, 1)


@pytest.mark.parametrize("N,K,ell", [(6, 3, 1), (6, 4, 2), (6, 6, 5)])
def test_unique_distance_or_identity_regimes_have_zero_ambiguity(N, K, ell):
    b = ambiguity_bound(7, N, K, ell)
    assert all(Fraction(x) == 0 for x in b["sphere_bad_mass_upper_exact"])
    assert Fraction(b["heralded_vs_ideal_pure_trace_distance_squared_upper_exact"]) == 0


def test_actual_vandermonde_columns_are_MDS_not_just_called_MDS():
    p, N, K = 7, 6, 3
    for support in combinations(range(1, N + 1), K):
        H = Matrix([[pow(a, j, p) for a in support] for j in range(K)])
        assert int(H.det()) % p != 0
    # Repeated columns would defeat the premise, even at radius1.
    repeated = np.array([[1, 1], [2, 2], [4, 4]])
    assert np.array_equal(repeated @ np.array([1, 0]), repeated @ np.array([0, 1]))


def test_different_error_weights_must_be_compared_against_the_whole_ball():
    p, N, K = 7, 6, 4
    # A weight5 kernel word, split into errors of weights2 and3.
    points = list(range(1, 6))
    kernel = [pow(math.prod(a - b for b in points if b != a) % p, -1, p) for a in points] + [0]
    e, other = kernel[:2] + [0] * 4, [0] * 2 + [(-x) % p for x in kernel[2:]]
    H = [[pow(i + 1, j, p) for i in range(N)] for j in range(K)]
    syndrome = lambda v: tuple(sum(a * b for a, b in zip(row, v)) % p for row in H)
    assert syndrome(e) == syndrome(other) and e != other
    assert sum(x != 0 for x in e) == 2 and sum(x != 0 for x in other) == 3
    assert Fraction(ambiguity_bound(p, N, K, 2)["sphere_bad_mass_upper_exact"][2]) == 0
    assert Fraction(ambiguity_bound(p, N, K, 3)["sphere_bad_mass_upper_exact"][2]) > 0


def test_coherent_comparison_pays_fiber_amplification_not_just_bad_mass():
    epsilon, M = Fraction(1, 100), 22
    # M bad labels coalesce in phase; the unique good image is orthogonal.
    ideal = np.array([math.sqrt(1 - float(epsilon)), M * math.sqrt(float(epsilon) / M)])
    ideal /= np.linalg.norm(ideal)
    actual_distance_squared = 1 - ideal[0] ** 2
    assert float(coherent_distance_squared(epsilon, M)) == pytest.approx(actual_distance_squared, abs=1e-12)
    assert math.sqrt(actual_distance_squared) > 40 * float(epsilon)
    assert coherent_distance_squared(0, M) == 0 and coherent_distance_squared(1, M) == 1
    with pytest.raises(ValueError, match="exact"):
        coherent_distance_squared(0.01, M)
    with pytest.raises(ValueError, match="positive integer"):
        coherent_distance_squared(epsilon, 0)


def test_ambiguity_bound_rejects_invalid_field_or_radius():
    with pytest.raises(ValueError, match="prime"):
        ambiguity_bound(15, 6, 3, 2)
    with pytest.raises(ValueError, match="radius"):
        ambiguity_bound(7, 6, 3, 3)
    with pytest.raises(ValueError, match="evaluation"):
        ambiguity_bound(7, 7, 3, 2)


def test_large_fixed_source_has_a_real_coherent_bound_but_no_decoder_claim():
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29, mode="mixed", include_zero=False)
    profile = source_profile(problem, 32)
    b = profile["bounds"]
    assert Fraction(b["any_radial_weight_bad_mass_upper_exact"]) < Fraction(1, 10 ** 98)
    assert Fraction(b["heralded_vs_ideal_pure_trace_distance_squared_upper_exact"]) < Fraction(1, 10 ** 68)
    assert Fraction(profile["capacity_gap_exact"]) == Fraction(7, 127)
    assert Fraction(profile["nonzero_Fourier_probability_exact"]) == Fraction(1, problem.prime - 1)
    assert not profile["source_requires_IID_shifts"]
    assert not profile["coherent_capacity_decoder_implemented"]
    assert not profile["finite_decoder_constants_or_gate_budget_supplied"]
    assert not b["field_or_error_vectors_enumerated"]
    too_near = source_profile(problem, 38)["bounds"]
    assert not too_near["coherent_error_bound_nontrivial"]


@pytest.mark.parametrize("p", [7, 19, 43])
@pytest.mark.parametrize("zero", [True, False])
def test_actual_unique_herald_and_native_Fourier_filter_physics(p, zero):
    record = physical_control(p, include_zero=zero)
    assert record["decoder_type"].startswith("EXHAUSTIVE_BALL_CALIBRATION")
    assert record["error_vectors_enumerated_and_charged"] == sum(math.comb(6, j) * (p - 1) ** j for j in range(3))
    assert record["joint_isometry_norm"] == pytest.approx(1, abs=1e-11)
    assert record["unique_herald_success"] + record["actual_bad_source_mass"] == pytest.approx(1, abs=1e-11)
    assert record["max_native_filter_amplitude_error"] < 1e-12
    assert record["native_output_TV"] ** 2 <= record["pure_trace_distance_squared"] + 1e-11
    assert record["max_actual_syndrome_list"] > 1
    assert not record["efficient_large_quantum_decoder_executed"]


def test_small_exhaustive_noise_counts_independently_check_each_sphere_bound():
    p, N, K, ell = 7, 5, 3, 2
    H = [[pow(i + 1, j, p) for i in range(N)] for j in range(K)]
    buckets = {}
    for e in product(range(p), repeat=N):
        weight = sum(x != 0 for x in e)
        if weight > ell:
            continue
        s = tuple(sum(a * b for a, b in zip(row, e)) % p for row in H)
        buckets.setdefault(s, []).append((e, weight))
    b = ambiguity_bound(p, N, K, ell)
    for j in range(ell + 1):
        bad = sum(w == j for group in buckets.values() if len(group) > 1 for _, w in group)
        actual = Fraction(bad, math.comb(N, j) * (p - 1) ** j)
        assert actual <= Fraction(b["sphere_bad_mass_upper_exact"][j])


def test_live_artifact_preserves_provenance_and_every_nonimplementation_flag():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert report["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    for row in report["analytic_large_profiles"]:
        assert from_specification(row["specification"]).dimension == 39
    assert report["source_and_ambiguity_derivation_review_pending"]
    assert not report["large_capacity_decoder_implemented_or_executed"]
    assert not report["new_algorithm_or_speedup_claimed"]
    assert not report["new_central_candidate_negative_or_proof_registered"]
