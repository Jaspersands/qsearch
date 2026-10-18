"""Finite readout guarantees, extra-radius traps and independent dual moments."""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pytest

import theorems.prime_character_finite_readout as module
from theorems.prime_character_finite_readout import (
    REPORT, certify, jacobi_matrix, mean_tail_lower, normalization_does_not_certify_mean_control,
    rayleigh_interval, run_controls, sqrt_interval,
)
from theorems.prime_character_capacity_source import local_fourier
from theorems.prime_character_opi import REPORT as CLASSICAL_REPORT, instance


@pytest.mark.parametrize("value", [Fraction(0), Fraction(1, 4), Fraction(2), Fraction(1, 10 ** 100)])
def test_square_root_enclosures_are_exact_even_when_float_would_underflow(value):
    lower, upper = sqrt_interval(value)
    assert lower * lower <= value <= upper * upper
    assert upper - lower <= Fraction(1, 1 << 160)


def test_signed_rational_Rayleigh_bounds_match_an_independent_matrix():
    N, rho, weights = 9, Fraction(3, 7), (Fraction(2), Fraction(-3), Fraction(1, 2))
    record = rayleigh_interval(N, rho, weights)
    array = np.array(list(map(float, weights)))
    value = array @ jacobi_matrix(N, rho, 2) @ array / (array @ array)
    assert float(Fraction(record["ambient_Rayleigh_lower_exact"])) == pytest.approx(value, abs=1e-14)
    assert float(Fraction(record["ambient_Rayleigh_upper_exact"])) == pytest.approx(value, abs=1e-14)
    assert not record["global_eigenvalue_optimality_certified"]
    with pytest.raises(ValueError, match="nonzero"):
        rayleigh_interval(N, rho, [Fraction(0)])
    with pytest.raises(ValueError, match="exact radial"):
        rayleigh_interval(N, rho, [0.1])


def test_a_source_norm_certificate_cannot_be_reused_as_a_mean_certificate():
    record = normalization_does_not_certify_mean_control()
    assert record["actual_filter_norm"] == pytest.approx(1, abs=1e-13)
    assert record["source_ball_ambiguity_bound"]["any_radial_weight_bad_mass_upper_exact"] == "0"
    assert abs(record["actual_native_mean"] - record["uncorrected_ambient_mean"]) > 0.03
    assert record["new_certifier"]["status"] == "UNKNOWN_OBSERVABLE_RADIUS_REACHES_CAPACITY"
    assert not record["new_certifier"]["finite_mean_certified"]
    assert "heralded_mean_lower_exact" not in record["new_certifier"]


def _product_coefficient(N, t, j, k, beta):
    # Independent bivariate multiplication for the q_j*q_k coefficient law.
    poly = {(0, 0): 1.0}
    for step in range(N):
        factor = {(0, 0): 1, (1, 1): 1} if step < N - t else {(1, 0): 1, (0, 1): 1, (1, 1): beta}
        out = {}
        for (a, b), c in poly.items():
            for (x, y), d in factor.items():
                if a + x <= j and b + y <= k:
                    key = a + x, b + y
                    out[key] = out.get(key, 0) + c * d
        poly = out
    return poly.get((j, k), 0.0)


@pytest.mark.parametrize("zero", [True, False])
def test_nontrivial_radial_Gram_matches_independent_one_dimensional_dual_code(zero):
    # N5,K4 means one dual scalar, not a p^4 coefficient-word enumeration.
    p, N, K, ell, L = 10007, 5, 4, 2, 3
    problem = instance(p, N, K, 2, 29, mode="mixed", include_zero=zero)
    points = range(1, N + 1)
    dual = [pow(math.prod(a - b for b in points if a != b) % p, -1, p) for a in points]
    assert all(sum(pow(a, j, p) * v for a, v in zip(points, dual)) % p == 0 for j in range(K))
    highest_moment = sum(math.prod(local_fourier(problem, i, z * dual[i] % p) for i in range(N)) for z in range(1, p))
    assert abs(highest_moment.imag) < 1e-12
    moments = [1.0] + [0.0] * K + [highest_moment.real]
    rho = float(problem.density)
    beta = (1 - 2 * rho) / math.sqrt(rho * (1 - rho))
    G = np.array([[sum(_product_coefficient(N, t, j, k, beta) * moments[t] for t in range(N + 1))
                   / math.sqrt(math.comb(N, j) * math.comb(N, k))
                   for k in range(L + 1)] for j in range(L + 1)])
    result = certify(problem, ell, weights=(Fraction(1), Fraction(2), Fraction(-1)), thresholds=(4,))
    assert result["finite_mean_certified"] and not result["exact_RS_moment_regime"]
    delta = Fraction(result["radial_Gram_operator_norm_error_upper_exact"])
    assert 0 < delta < Fraction(1, 100)
    assert max(abs(np.linalg.eigvalsh(G - np.eye(L + 1)))) <= float(delta)
    u = np.array([1, 2, -1, 0]) / math.sqrt(6)
    mean = float(u @ G @ jacobi_matrix(N, problem.density, L) @ u / (u @ G @ u))
    assert float(Fraction(result["ideal_mean_lower_exact"])) <= mean <= float(Fraction(result["ideal_mean_upper_exact"]))


def test_exact_RS_branch_is_not_mislabeled_as_a_full_extended_Gram_certificate():
    p = instance(2 ** 61 - 1, 127, 39, 2, 29)
    row = certify(p, 19)
    assert row["mean_estimate_method"] == "EXACT_RS_MOMENTS"
    assert row["radial_Gram_operator_norm_error_upper_exact"] is None
    assert row["Gram_mean_error_upper_exact"] == "0"
    assert Fraction(row["heralded_mean_lower_exact"]) > Fraction(816, 1000)
    assert Fraction(row["heralded_mean_upper_exact"]) < Fraction(817, 1000)


def test_near_capacity_unknowns_are_not_licensed_by_a_good_numerical_Rayleigh_quotient():
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29)
    for ell in (37, 38):
        row = certify(problem, ell)
        assert not row["finite_mean_certified"]
        assert row["status"].startswith("UNKNOWN_")
        assert "heralded_mean_lower_exact" not in row


def test_degree32_has_a_finite_tail_but_no_runtime_or_circuit_claim():
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29)
    row = certify(problem, 32, thresholds=(110, 115))
    assert row["mean_estimate_method"] == "EXTENDED_RADIAL_GRAM"
    assert row["observable_extra_radius"] == 33
    assert row["observable_Gram_companion"]["ell"] == 33
    assert Fraction(row["radial_Gram_operator_norm_error_upper_exact"]) < Fraction(1, 10 ** 48)
    assert Fraction(row["heralded_mean_lower_exact"]) > Fraction(9028, 10000)
    assert Fraction(row["heralded_mean_upper_exact"]) < Fraction(9030, 10000)
    lo, hi = map(Fraction, (row["heralded_mean_lower_exact"], row["heralded_mean_upper_exact"]))
    assert 0 < hi - lo < Fraction(1, 10 ** 33)
    assert Fraction(row["tail_certificates"][0]["one_attempt_with_herald_tail_lower_exact"]) > Fraction(314, 1000)
    assert Fraction(row["tail_certificates"][1]["one_attempt_with_herald_tail_lower_exact"]) > Fraction(5, 100)
    assert not row["large_quantum_decoder_or_circuit_executed"]
    assert not row["matched_classical_quantum_runtime_comparison_supplied"]
    assert not row["accepted_speedup_candidate"]


def test_integer_score_tail_bound_is_sharp_for_a_two_point_distribution():
    N, threshold, mean = 127, 110, Fraction(9, 10)
    probability = mean_tail_lower(N, mean, threshold)
    # Saturation places all failed mass at threshold-1 and all success at N.
    assert probability * 1 + (1 - probability) * Fraction(threshold - 1, N) == mean
    assert mean_tail_lower(N, mean, 0) == 1 and mean_tail_lower(N, mean, N + 1) == 0
    with pytest.raises(ValueError, match="mean"):
        mean_tail_lower(N, 0.9, threshold)


def test_artifact_replays_and_classical_comparisons_match_the_actual_input():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == report["source_sha256"]
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    assert hashlib.sha256(CLASSICAL_REPORT.read_bytes()).hexdigest() == report["classical_input_artifact_sha256"]
    for r in report["fixed_input_profiles"]:
        assert r["saved_classical_same_input_best_score"] == (109 if r["finite_readout"]["specification"]["include_zero"] else None)
        for t in r["finite_readout"]["tail_certificates"]:
            attempt = Fraction(t["one_attempt_with_herald_tail_lower_exact"])
            for repetition in t["fresh_independent_attempts"]:
                exact = 1 - (1 - attempt) ** repetition["attempts"]
                lower = Fraction(repetition["success_lower_exact"])
                assert lower <= exact < lower + Fraction(1, 1 << repetition["dyadic_enclosure_bits"])
            assert not t["binomial_score_distribution_assumed"]
    assert not report["new_quantum_algorithm_or_speedup_claimed"]
    assert not report["new_central_candidate_negative_or_proof_registered"]
    assert not report["independent_or_formal_application_review_completed"]
