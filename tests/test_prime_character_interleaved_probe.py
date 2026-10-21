"""Actual recovery, rank failure and the shared-support objective mismatch."""

from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path

import numpy as np
import pytest
from flint import nmod_mat

import theorems.prime_character_interleaved_probe as module
from theorems.prime_character_interleaved_probe import (
    REPORT, classical_controls, decode_burst, marginal_certificate, physical_control,
    run_controls, syndrome, uniform_tail_upper,
)
from theorems.prime_character_opi import instance
from theorems.prime_character_capacity_source import local_fourier


def test_actual_61_bit_recovery_and_no_reroll_rank_failures():
    records = classical_controls()
    for record in records:
        decoder = record["decoder"]
        if record["name"] in ("five_independent_rows", "eight_independent_rows"):
            assert decoder["status"] == "VERIFIED_UNIQUE_BURST"
            assert decoder["error_rows"] == record["source_errors"]
            assert decoder["support"] == record["source_support"]
            assert decoder["degree"] == decoder["cap_recurrence_rank"] == 32
            assert decoder["whole_cap_uniqueness_certified"]
        else:
            assert decoder["status"].startswith("UNKNOWN_")
        assert not decoder["source_error_or_support_supplied"]
        assert record["failed_rows_not_rerolled"]
    assert records[0]["decoder"]["cap_equations"] == 14
    assert records[3]["decoder"]["cap_equations"] == 35
    assert records[3]["decoder"]["cap_recurrence_rank"] == 7
    assert records[0]["source_errors"] == records[1]["source_errors"][:2]
    assert records[1]["source_errors"] == records[2]["source_errors"][:5]


def test_rank_minor_polynomial_is_nonzero_for_every_fixed_distinct_support():
    p, columns, copies, w = 101, 32, 5, 7
    nodes = [i + 1 for i in range(columns)]
    # A block-Vandermonde witness evaluates a particular degree32 minor nonzero.
    # Zeros here prove a polynomial is nonzero; sampling remains from Fp*.
    groups = [list(range(a * w, min(columns, (a + 1) * w))) for a in range(copies)]
    rows = [[pow(nodes[l], t, p) if l in group else 0 for l in range(columns)]
            for group in groups for t in range(len(group))]
    assert len(rows) == columns
    assert nmod_mat(rows, p).rank() == columns
    assert Fraction(columns, p - 1) < 1


def test_decoder_handles_smaller_actual_weight_and_zero_rows_without_advice():
    p, N, K, cap = 7, 4, 3, 2
    errors = [[0, 3, 0, 0], [0, 0, 0, 0]]
    decoded = decode_burst(p, N, K, cap, [syndrome(p, e, K) for e in errors])
    assert decoded["status"] == "VERIFIED_UNIQUE_BURST"
    assert decoded["degree"] == decoded["cap_recurrence_rank"] == 1
    assert decoded["error_rows"] == errors
    zero = decode_burst(p, N, K, cap, [[0] * K, [0] * K])
    assert zero["degree"] == 0 and zero["whole_cap_uniqueness_certified"]


def test_whole_cap_uniqueness_replays_against_a_complete_small_burst_database():
    p, N, K, cap = 5, 4, 3, 2
    buckets = {}
    nonzero_columns = [v for v in product(range(p), repeat=2) if any(v)]
    for j in range(cap + 1):
        for support in combinations(range(N), j):
            for values in product(nonzero_columns, repeat=j):
                rows = [[0] * N for _ in range(2)]
                for i, column in zip(support, values):
                    for a in range(2):
                        rows[a][i] = column[a]
                key = tuple(tuple(syndrome(p, row, K)) for row in rows)
                buckets.setdefault(key, []).append(rows)
    successes = 0
    # Exhaust every fully nonzero two-column input on this fixed support.
    for values in product(range(1, p), repeat=4):
        rows = [list(values[:2]) + [0, 0], list(values[2:]) + [0, 0]]
        key = tuple(tuple(syndrome(p, row, K)) for row in rows)
        decoded = decode_burst(p, N, K, cap, [list(s) for s in key])
        if decoded["status"] == "VERIFIED_UNIQUE_BURST":
            assert len(buckets[key]) == 1
            assert decoded["error_rows"] == rows == buckets[key][0]
            successes += 1
    assert successes == 192  # The other64 have dependent rows, not a source reroll.
    assert Fraction(256 - successes, 256) <= Fraction(cap, p - 1)


def test_uniform_tail_uses_only_certified_even_moments():
    problem = instance(7, 4, 2, 2, 29)
    actual = sum(problem.score_count(word) >= 4 for word in product(range(7), repeat=2))
    bound = uniform_tail_upper(4, 2, problem.density, 4)
    assert Fraction(actual, 49) <= Fraction(bound["probability_upper_exact"])
    assert bound["moment_order"] == 2
    assert not bound["full_binomial_score_distribution_assumed"]
    assert uniform_tail_upper(4, 2, problem.density, 0)["probability_upper_exact"] == "1"
    assert uniform_tail_upper(4, 2, problem.density, 5)["probability_upper_exact"] == "0"
    with pytest.raises(ValueError, match="exact density"):
        uniform_tail_upper(4, 2, 0.5, 4)


@pytest.mark.parametrize("p", [7, 11])
@pytest.mark.parametrize("zero", [True, False])
def test_full_joint_physics_improves_product_correlation_not_individual_score(p, zero):
    row = physical_control(p, include_zero=zero)
    assert row["native_joint_amplitude_error"] < 1e-12
    assert row["joint_norm"] == pytest.approx(1, abs=1e-12)
    assert row["marginal_model_error"] < 1e-12
    assert row["marginal_purity"] == pytest.approx(Fraction(5, 16), abs=1e-12)
    assert row["shared_support_individual_mean"] == pytest.approx(row["predicted_individual_mean"], abs=1e-12)
    assert row["single_copy_DQI_mean"] > row["shared_support_individual_mean"] + 0.2
    assert row["joint_centered_product_correlation"] > 0.5
    assert row["joint_error_vectors_enumerated_and_charged"] == 1 + 4 * (p - 1) ** 2
    assert row["joint_coefficient_words_and_QFT_dimension_charged"] == p ** 4
    assert not row["large_quantum_interleaved_decoder_executed"]


@pytest.mark.parametrize("copies", [5, 8])
def test_large_single_polynomial_tail_collapses_even_with_fast_rank_recovery(copies):
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29)
    row = marginal_certificate(problem, 32, copies)
    assert row["status"] == "CERTIFIED_MARGINAL_AND_SELECTION_UPPER_BOUNDS_LOCAL_REVIEW_PENDING"
    assert row["marginal_bound_is_nontrivial"]
    assert Fraction(row["all_support_frame_delta_upper_exact"]) < Fraction(1, 10 ** 68)
    assert Fraction(row["collaborative_rank_failure_mass_upper_exact"]) == Fraction(32, problem.prime - 1)
    assert Fraction(row["heralded_each_row_TV_to_uniform_upper_exact"]) < Fraction(4, 10 ** 9)
    assert Fraction(row["each_row_mean_upper_exact"]) < Fraction(501, 1000)
    tail = row["tail_upper_certificates"][0]
    assert Fraction(tail["best_of_original_rows_tail_upper_exact"]) < Fraction(3, 10 ** 8)
    assert not tail["independence_between_output_rows_assumed"]
    assert row["independent_error_values_conditional_on_support_required"]
    assert not row["arbitrary_interleaved_algorithm_ruled_out"]
    assert not row["coherent_gate_compilation_supplied"]


def test_more_rank_rejections_are_not_all_given_fiber_amplification():
    row = marginal_certificate(instance(2 ** 61 - 1, 127, 39, 2, 29), 32, 5)
    zeta = Fraction(row["collaborative_rank_failure_mass_upper_exact"])
    extra = Fraction(row["collision_amplification_extra_mass_upper_exact"])
    squared = Fraction(row["rank_herald_output_TV_squared_upper_exact"])
    assert squared == (zeta + extra) / (1 + extra)
    assert zeta < squared < zeta * 2
    M = int(row["single_copy_source_bound"]["max_fiber_size_support_bound_decimal"])
    assert M * zeta > 1  # The crude M*zeta shortcut would be completely useless.


def test_nontrivial_all_support_frame_and_tensor_polar_comparison():
    # One-dimensional dual sums determine this complete support Gram, without p^4 words.
    p, N, K, ell = 10007, 5, 4, 3
    problem = instance(p, N, K, 2, 29)
    points = range(1, N + 1)
    dual = [pow(math.prod(a - b for b in points if a != b) % p, -1, p) for a in points]
    moment = sum(math.prod(local_fourier(problem, i, z * dual[i] % p) for i in range(N)) for z in range(1, p))
    assert abs(moment.imag) < 1e-12
    rho = float(problem.density)
    beta = (1 - 2 * rho) / math.sqrt(rho * (1 - rho))
    supports = [set(s) for j in range(ell + 1) for s in combinations(range(N), j)]
    G = np.array([[1.0 if S == T else (beta ** len(S & T) * moment.real if len(S | T) == N else 0.0)
                   for T in supports] for S in supports])
    record = marginal_certificate(problem, ell, 3, thresholds=(5,))
    delta = float(Fraction(record["all_support_frame_delta_upper_exact"]))
    assert 0 < max(abs(np.linalg.eigvalsh(G - np.eye(len(G))))) < delta < 0.01
    values, vectors = np.linalg.eigh(G)
    F = (vectors * np.sqrt(values)) @ vectors.T
    gamma = float(Fraction(record["polar_frame_error_upper_exact"]))
    assert np.linalg.norm(F - np.eye(len(G)), ord=2) <= gamma
    coefficients = np.array([complex(i + 1, (-1) ** i) for i in range(len(G))])
    coefficients /= np.linalg.norm(coefficients)
    actual = np.einsum("is,js,ks,s->ijk", F, F, F, coefficients)
    reference = np.zeros_like(actual)
    for s, value in enumerate(coefficients):
        reference[s, s, s] = value
    eta = (1 + gamma) ** 3 - 1
    assert np.linalg.norm(actual - reference) <= eta
    actual /= np.linalg.norm(actual)
    flat = actual.reshape(len(G), -1)
    marginal = flat @ flat.conj().T
    dephased_reference = np.diag(abs(coefficients) ** 2)
    distance = sum(abs(np.linalg.eigvalsh(marginal - dephased_reference))) / 2
    assert distance <= 2 * eta / (1 - eta)


def test_single_copy_and_unsupported_fields_or_equation_counts_are_not_covered():
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29)
    with pytest.raises(ValueError, match="copies"):
        marginal_certificate(problem, 32, 1)
    assert marginal_certificate(problem, 32, 2)["status"] == "UNKNOWN_COLLABORATIVE_EQUATION_BUDGET"
    weak = marginal_certificate(instance(7, 6, 3, 2, 29), 2, 2, thresholds=(5,))
    assert weak["status"] == "UNKNOWN_SINGLE_COPY_FRAME_BOUND_TOO_WEAK"
    with pytest.raises(ValueError, match="congruent"):
        marginal_certificate(instance(5, 4, 2, 2, 29), 1, 2, thresholds=(4,))
    with pytest.raises(ValueError, match="canonical"):
        decode_burst(7, 4, 3, 2, [[0, 1, 7]])


def test_live_artifact_provenance_and_scope():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == report["source_sha256"]
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    assert not report["all_interleaving_or_all_quantum_readouts_ruled_out"]
    assert not report["new_quantum_algorithm_or_speedup_claimed"]
    assert not report["new_central_candidate_negative_or_proof_registered"]
    assert not report["independent_or_formal_application_review_completed"]
