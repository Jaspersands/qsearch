"""Actual soft-source physics, exact classical sampling and native lattice attacks."""

from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

import numpy as np
import pytest
from flint import nmod_mat
from flint import fmpz_mat
from sympy import Matrix

import theorems.interval_soft_decoder as module
from theorems.interval_soft_decoder import (
    REPORT, _multiply5, _q5_probabilities, _sign5, bounded_receiver, classical_lattice_control,
    interval_dp, interval_profile, parity, run_controls, sample_dp, syndrome,
)
from theorems.dcp_subset_sum_affine_cvp_baseline import exact_gram_schmidt_rows


def test_independent_fourier_profile_energy_and_all_complex_profile_ceiling():
    for p in (5, 7, 13):
        for u in range((p - 1) // 2 + 1):
            profile = interval_profile(p, u)
            a = np.zeros(p, complex)
            a[profile["support"]] = 1 / math.sqrt(2 * u + 1)
            f = np.fft.fft(a) / math.sqrt(p)
            assert np.sum(abs(f) ** 4) == pytest.approx(float(Fraction(profile["KV_collision_score_exact"])), abs=1e-13)
            if u <= (p - 1) // 4:
                L = 2 * u + 1
                assert Fraction(profile["KV_collision_score_exact"]) == Fraction(2 * L, 3 * p) + Fraction(1, 3 * p * L)
                assert Fraction(profile["all_profiles_collision_gain_over_uniform_upper_exact"]) <= Fraction(3, 2)
            # The ceiling is uniform over COMPLEX amplitudes, not only indicators.
            rng = np.random.default_rng(4441 + 10 * p + u)
            a[profile["support"]] = rng.normal(size=2 * u + 1) + 1j * rng.normal(size=2 * u + 1)
            a /= np.linalg.norm(a)
            f = np.fft.fft(a) / math.sqrt(p)
            assert max(abs(f) ** 2) <= (2 * u + 1) / p + 1e-13
            assert sum(abs(f) ** 4) <= (2 * u + 1) / p + 1e-13


def test_full_support_dual_conventions_include_zero_and_have_the_right_rank():
    for p in (5, 7, 11):
        for d in range(1, p):
            H, G = nmod_mat(parity(p, d), p), nmod_mat(parity(p, p - d), p)
            assert H.rank() == d and G.rank() == p - d
            assert H * G.transpose() == nmod_mat(d, p - d, p)
            assert list(parity(p, d)[0]) == [1] * p


@pytest.mark.parametrize("p,d,weights", [(5, 1, (1, 1, 1)), (5, 2, (4, 5, 4)), (7, 2, (1, 2, 1))])
def test_DP_partitions_and_backward_likelihood_are_exact_not_just_witnesses(p, d, weights):
    profile = interval_profile(p, 1, weights)
    dp = interval_dp(p, d, profile)
    H = parity(p, d)
    value_weights = dict(zip(profile["support"], (x * x for x in weights)))
    expected = {}
    for word in product(profile["support"], repeat=p):
        s = syndrome(H, word, p)
        weight = math.prod(value_weights[x] for x in word)
        expected[s] = expected.get(s, 0) + weight
    assert expected == dp["tables"][-1]
    assert sum(expected.values()) == profile["amplitude_norm_squared"] ** p
    for word in product(profile["support"], repeat=p):
        s = syndrome(H, word, p)
        target, probability = s, Fraction(1)
        for i in range(p - 1, -1, -1):
            prior = tuple((target[j] - H[j][i] * word[i]) % p for j in range(d))
            probability *= Fraction(value_weights[word[i]] * dp["tables"][i].get(prior, 0), dp["tables"][i + 1][target])
            target = prior
        assert probability == Fraction(math.prod(value_weights[x] for x in word), expected[s])
    rng = random.Random(4451)
    for s in expected:
        sample = sample_dp(dp, s, rng)
        assert sample is not None
        assert all(x in profile["support"] for x in sample)
        assert syndrome(H, sample, p) == s


def test_quadratic_field_MAP_comparisons_do_not_round_near_ties():
    a, b = 1, 0
    for _ in range(100):
        a, b = 9 * a + 20 * b, 4 * a + 9 * b
    assert a * a - 5 * b * b == 1
    assert _sign5((a, -b)) == 1
    assert _sign5((-a, b)) == -1
    assert _sign5((0, 0)) == 0
    assert _multiply5((a, -b), (a, b)) == (1, 0)
    for weights in ((1, 1, 1), (4, 5, 4), (1, 2, 1), (1, 1, 2), (0, 1, 0)):
        probabilities = _q5_probabilities(*weights)
        assert tuple(sum(v[j] for v in probabilities) for j in (0, 1)) == (1, 0)
        a = np.array([weights[1], weights[2], 0, 0, weights[0]], float)
        a /= np.linalg.norm(a)
        source = np.fft.fft(a) / math.sqrt(5)
        assert all(_sign5(v) >= 0 for v in probabilities)
        assert [float(v[0]) + math.sqrt(5) * float(v[1]) for v in probabilities] == pytest.approx(abs(source) ** 2, abs=1e-14)


@pytest.mark.parametrize("d,center,side", [(1, 1, 1), (1, 5, 4), (2, 1, 1), (2, 5, 4), (2, 2, 1)])
def test_actual_decoder_XOR_herald_and_QFT_preserve_every_target(d, center, side):
    row = bounded_receiver(d, center=center, side=side)
    P = row["decoder_success_probability"]
    assert row["all_pre_erasure_source_pairs_charged"] == 5 ** (5 + d)
    assert row["all_sparse_decoder_XOR_outputs_distinct"]
    assert row["failed_source_mass_retained"] == pytest.approx(1 - P)
    assert row["full_main_QFT_dimension_charged"] == 5 ** 5
    assert row["decoder_table_entries_charged"] == 5 ** (5 - d)
    assert len(row["targets"]) == 5 ** d
    assert not any(t["target_coset_empty"] for t in row["targets"])
    for t in row["targets"]:
        assert t["herald_success_probability"] == pytest.approx(P, abs=1e-12)
        assert t["source_QFT_vs_independent_amplitude_error"] < 1e-12
        assert t["probability_outside_original_syndrome_coset"] < 1e-25
        assert t["classical_exact_sample"] is not None
    assert row["average_squared_fidelity"] >= P - 1e-12
    assert row["average_conditional_valid_probability"] >= P - 1e-12
    assert row["one_attempt_average_valid_probability"] >= P * P - 1e-12
    assert row["worst_fixed_target_conditional_valid_probability"] < row["average_conditional_valid_probability"] - .001
    # This is a UNIFORM target average, not the easier planted partition distribution.
    assert row["average_conditional_valid_probability"] == pytest.approx(sum(t["conditional_quantum_valid_interval_probability"] for t in row["targets"]) / 5 ** d)
    assert not row["efficient_quantum_KV_gate_compiler_supplied"]


def test_MAP_mass_matches_an_independent_numerical_whole_syndrome_optimum():
    p, d = 5, 2
    H = np.array(parity(p, p - d))
    words = np.array(list(product(range(p), repeat=p)))
    a = np.array([5, 4, 0, 0, 4]) / math.sqrt(57)
    f = np.fft.fft(a) / math.sqrt(p)
    masses = np.prod(abs(f[words]) ** 2, axis=1)
    syndromes = (words @ H.T) % p
    keys = syndromes @ np.array([p ** j for j in range(p - d)])
    best = np.zeros(p ** (p - d))
    np.maximum.at(best, keys, masses)
    row = bounded_receiver(d, center=5, side=4)
    assert sum(best) == pytest.approx(row["decoder_success_probability"], abs=1e-13)


def test_uniform_average_bound_is_not_a_pointwise_bound_even_for_feasible_cosets():
    row = bounded_receiver(2, center=5, side=4)
    bad = next(t for t in row["targets"] if t["uniform_target_syndrome"] == [2, 0])
    assert not bad["target_coset_empty"] and bad["classical_exact_sample"] is not None
    assert bad["conditional_quantum_valid_interval_probability"] < row["decoder_success_probability"] - .04
    assert bad["real_vs_ideal_squared_fidelity"] < row["decoder_success_probability"] - .04
    assert row["average_squared_fidelity"] >= row["decoder_success_probability"]


def test_empty_cosets_are_failures_not_rerolled_or_conditioned_out():
    row = bounded_receiver(1, center=1, side=0)
    assert row["profile"]["support"] == [0]
    assert sum(t["target_coset_empty"] for t in row["targets"]) == 4
    assert row["average_conditional_valid_probability"] == pytest.approx(.2, abs=1e-12)
    assert not row["published_KV_sufficient_condition_strictly_satisfied"]
    for t in row["targets"]:
        if t["target_coset_empty"]:
            assert t["classical_exact_sample"] is None and t["real_vs_ideal_TV"] is None
            assert t["conditional_quantum_valid_interval_probability"] < 1e-25


def test_complex_and_signed_source_phases_cannot_be_replaced_by_probabilities():
    real = bounded_receiver(1)
    complex_source = bounded_receiver(2, center=1, side=1, right=2)
    assert real["maximum_TV_if_source_phases_silently_dropped"] > .7
    assert complex_source["maximum_TV_if_source_phases_silently_dropped"] > .8
    assert complex_source["average_squared_fidelity"] >= complex_source["decoder_success_probability"] - 1e-12


def test_better_finite_samples_are_not_a_better_asymptotic_KV_certificate():
    flat, center = bounded_receiver(2), bounded_receiver(2, center=2)
    assert center["average_conditional_valid_probability"] > flat["average_conditional_valid_probability"]
    assert Fraction(center["profile"]["KV_collision_score_exact"]) < Fraction(flat["profile"]["KV_collision_score_exact"])
    assert flat["published_KV_sufficient_condition_strictly_satisfied"]
    assert not center["published_KV_sufficient_condition_strictly_satisfied"]


def test_native_lattice_attack_verifies_the_original_equations_and_polynomial():
    row = classical_lattice_control(11, 2, 2)
    assert row["unimodular_transform_and_native_kernel_verified"]
    assert not row["target_or_short_solution_used_to_select_basis"]
    assert row["seed_or_basis_restarts"] == 0
    H = parity(11, 2)
    for t in row["trials"]:
        e = t["centered_affine_witness"]
        assert syndrome(H, e, 11) == tuple(t["uniform_target_syndrome"])
        coefficients = t["polynomial_coefficients"]
        for x in range(11):
            y = 0
            for a in reversed(coefficients):
                y = (y * x + a) % 11
            assert (t["particular_word"][x] - y) % 11 == e[x] % 11
    assert Fraction(row["canonical_interpolation_uniform_target_success_exact"]) == Fraction(5, 11) ** 2
    impossible = classical_lattice_control(11, 0, 2)
    assert impossible["failed_trials_retained"]
    assert not impossible["soft_decoder_condition_strictly_satisfied"]
    assert any(not t["valid_interval_solution"] for t in impossible["trials"])
    for t in impossible["trials"]:
        assert t["valid_interval_solution"] == (not any(t["uniform_target_syndrome"]))


def test_scope_guards_do_not_convert_caps_or_shrinking_density_into_hardness():
    profile = interval_profile(31, 1)
    cap = interval_dp(31, 5, profile, max_states=100)
    assert cap["status"] == "EXACT_DP_STATE_CAP_EXHAUSTED"
    assert not cap["partial_cosets_claimed_solved"]
    huge = interval_dp(4093, 4000, interval_profile(4093, 1), max_states=100)
    assert len(huge["required_states_decimal"]) > 4300
    assert not huge["full_parity_matrix_materialized"]
    assert profile["capacity_runtime_comparison_requires_fixed_rates_and_fixed_gap"]
    assert not profile["vanishing_density_or_shrinking_gap_runtime_subsumption_proved"]
    with pytest.raises(ValueError, match="complete exact"):
        sample_dp(cap, (0,) * 5, random.Random(1))
    with pytest.raises(ValueError, match="field mismatch"):
        interval_dp(7, 2, interval_profile(5, 1))
    with pytest.raises(ValueError, match="prime"):
        interval_profile(9, 1)
    with pytest.raises(ValueError, match="exact integer"):
        interval_profile(5, 1, (1, .5, 1))
    with pytest.raises(ValueError, match="both sides"):
        bounded_receiver(1, side=0, right=1)


def test_live_report_provenance_native_witnesses_and_scope():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert report["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    assert sum(r["successes"] for r in report["uniform_target_lattice_controls"]) == 24
    assert sum(r["all_syndromes_classically_solved_by_this_basis_certified"] for r in report["uniform_target_lattice_controls"]) == 4
    assert {r["parameter_family"] for r in report["uniform_target_lattice_controls"]} == {
        "constant_density_fixed_absolute_gap", "growing_sublinear_interval_relative_gap"}
    assert not report["vanishing_density_quantum_runtime_window_ruled_out"]
    assert not report["weighted_coset_sampling_dequantized_at_growing_codimension"]
    assert not report["large_KV_decoder_or_quantum_circuit_executed"]
    assert not report["new_quantum_algorithm_speedup_or_novelty_claimed"]
    assert not report["new_central_candidate_negative_or_proof_registered"]
    contract = json.loads((REPORT.parents[1] / "hypotheses/interval_soft_decoder_contract.json").read_text())
    for path in contract["evidence"]:
        assert (REPORT.parents[2] / path).is_file()


def test_saved_universal_classical_certificates_have_an_independent_exact_checker():
    report = json.loads(REPORT.read_text())
    for row in report["uniform_target_lattice_controls"]:
        rows = row["proof_basis_rows"]
        if rows is None:
            assert not row["all_syndromes_classically_solved_by_this_basis_certified"]
            continue
        p, d, u = row["profile"]["p"], row["decoder_dimension"], row["profile"]["u"]
        assert abs(int(fmpz_mat(rows).det())) == p ** d
        assert all(not any(syndrome(parity(p, d), r, p)) for r in rows)
        # A different Fraction/explicit-vector GS implementation, not the
        # producer's Bareiss + FLINT triangular inverse and returned flag.
        stars = exact_gram_schmidt_rows(Matrix(rows))
        bound2 = sum(sum(x * x for x in r) for r in stars) / 4
        bound_inf = max(sum(abs(stars[i][j]) for i in range(p)) / 2 for j in range(p))
        assert bound2 <= Fraction(row["finite_all_target_Babai_Euclidean_radius_squared_upper_exact"])
        assert bound_inf <= Fraction(row["finite_all_target_Babai_coordinate_radius_upper_exact"])
        integer_bound = min(p // 2, math.isqrt(bound2.numerator // bound2.denominator), bound_inf.numerator // bound_inf.denominator)
        assert integer_bound == row["finite_all_target_centered_infinity_norm_upper_integer"] <= u
