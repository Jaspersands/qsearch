"""Full native rescue, nonorthogonal-frame falsifiers and explicit phase cost."""

from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path

import numpy as np
import pytest

import theorems.prime_character_phase_feedback as module
from theorems.prime_character_phase_feedback import (
    REPORT, feedback_certificate, physical_control, reflection_count, reflection_product, run_controls,
)
from theorems.prime_character_capacity_source import local_fourier
from theorems.prime_character_opi import instance


def test_exact_reflection_counts_and_nontrivial_mask_lower_bound():
    for N in range(1, 8):
        for ell in range(N + 1):
            lower = sum(math.comb(N - 1, j) for j in range(ell))
            for m in range(N + 1):
                mask = (1 << m) - 1
                expected = sum((sum(1 << i for i in S) & mask).bit_count() % 2
                               for j in range(ell + 1) for S in combinations(range(N), j))
                assert reflection_count(N, ell, m) == expected
                if m:
                    assert expected >= lower
                else:
                    assert expected == 0


@pytest.mark.parametrize("p", [7, 11])
@pytest.mark.parametrize("zero", [True, False])
def test_full_native_QFT_measurement_and_actual_feedback_restore_interference(p, zero):
    row = physical_control(p, include_zero=zero)
    assert row["Gram_error"] < 1e-12
    assert row["independent_syndrome_QFT_vs_native_amplitude_error"] < 1e-12
    assert row["actual_reflection_vs_positive_branch_amplitude_error"] < 1e-12
    assert row["max_reflection_product_unitarity_residual"] < 1e-12
    assert row["corrected_mean"] > row["uncorrected_mean"] + 0.2
    assert row["corrected_mean"] < row["desired_single_copy_mean"]
    assert 0 < row["corrected_vs_target_trace_distance"] < float(Fraction(row["positive_amplitude_trace_distance_upper_exact"]))
    # Finite magnitude differences are retained, not incorrectly called perfect erasure.
    assert 0.98 < row["corrected_purity"] < 1 - 0.001
    assert len(row["every_auxiliary_outcome_probability"]) == p * p
    assert sum(row["every_auxiliary_outcome_probability"]) == pytest.approx(1, abs=1e-12)
    assert row["all_outcomes_retained"] and row["outcomes_selected_or_rerolled"] == 0
    assert row["joint_error_vectors_enumerated_and_charged"] == 1 + 4 * (p - 1) ** 2
    assert row["joint_coefficient_words_and_QFT_dimension_charged"] == p ** 4
    assert row["dense_unitary_dimension_charged"] == p * p
    assert not row["large_coherent_compiler_demonstrated"]


def test_multiple_auxiliary_rows_use_xor_of_native_signs_not_one_rows_mask():
    p, N, D = 7, 4, 49
    problem = instance(p, N, 2, 2, 29)
    accepted = np.array([[problem.accepted(i, v) for i, v in enumerate(problem.evaluations(w))]
                         for w in product(range(p), repeat=2)], float)
    rho = float(problem.density)
    g = (accepted - rho) / math.sqrt(rho * (1 - rho))
    frame = np.column_stack([np.ones(D), g]) / math.sqrt(D)
    b = np.array([complex(i + 1, (-1) ** i) for i in range(N + 1)])
    b /= np.linalg.norm(b)
    joint = np.einsum("is,js,ks,s->ijk", frame, frame, frame, b)
    corrected = np.zeros_like(joint)
    residual_wrong_mask = 0.0
    operators = {mask: reflection_product(frame, [0, 1, 2, 4, 8], mask)[0] for mask in range(16)}
    masks = [sum(1 << i for i in range(N) if g[y, i] < 0) for y in range(D)]
    for y, z in product(range(D), repeat=2):
        actual = operators[masks[y] ^ masks[z]] @ joint[:, y, z]
        expected = frame @ (b * abs(frame[y, :]) * abs(frame[z, :]))
        corrected[:, y, z] = actual
        assert np.max(abs(actual - expected)) < 1e-13
        wrong = operators[masks[y]] @ joint[:, y, z]
        residual_wrong_mask = max(residual_wrong_mask, np.linalg.norm(wrong - expected))
    assert residual_wrong_mask > 0.01
    matrix = corrected.reshape(D, D * D)
    density = matrix @ matrix.conj().T
    target = frame @ b
    distance = sum(abs(np.linalg.eigvalsh(density - np.outer(target, target.conj())))) / 2
    B = Fraction(p + 1, p - 1) ** 2
    assert distance <= float((B - 1) / (B + 1))
    assert np.trace(density).real == pytest.approx(1, abs=1e-12)


def test_positive_amplitude_bound_is_sharp_for_complex_coefficients():
    # Extremal two-value distribution proves the claimed bound with equality.
    B = Fraction(7, 3)
    a, b = 1 / math.sqrt(float(B)), math.sqrt(float(B))
    probability_a = b / (a + b)
    target = np.array([math.sqrt(probability_a), 1j * math.sqrt(1 - probability_a)])
    actual = target * np.array([a, b])
    actual /= np.linalg.norm(actual)
    distance = math.sqrt(max(0, 1 - abs(np.vdot(target, actual)) ** 2))
    assert distance == pytest.approx(float((B - 1) / (B + 1)), abs=1e-14)


def test_nonorthogonal_native_frame_requires_real_reflections_not_simultaneous_sum():
    p, N, K, ell = 10007, 5, 4, 3
    problem = instance(p, N, K, 2, 29)
    points = range(1, N + 1)
    dual = [pow(math.prod(a - b for b in points if a != b) % p, -1, p) for a in points]
    moment = sum(math.prod(local_fourier(problem, i, z * dual[i] % p) for i in range(N)) for z in range(1, p))
    assert abs(moment.imag) < 1e-12
    beta = float((1 - 2 * problem.density)) / math.sqrt(float(problem.density * (1 - problem.density)))
    supports = [set(S) for j in range(ell + 1) for S in combinations(range(N), j)]
    G = np.array([[1.0 if S == T else (beta ** len(S & T) * moment.real if len(S | T) == N else 0.0)
                   for T in supports] for S in supports])
    values, vectors = np.linalg.eigh(G)
    frame = (vectors * np.sqrt(values)) @ vectors.T
    row = feedback_certificate(problem, ell, 3, thresholds=(5,))
    gamma = float(Fraction(row["polar_frame_distance_upper_exact"]))
    masks = [sum(1 << i for i in S) for S in supports]
    # This mask selects disjoint complementary supports with nonzero overlap.
    mask = 3
    U, count = reflection_product(frame, masks, mask)
    ideal = np.diag([(-1) ** ((s & mask).bit_count()) for s in masks])
    assert np.linalg.norm(U - ideal, ord=2) <= 2 * count * gamma
    assert np.linalg.norm(U.conj().T @ U - np.eye(len(G)), ord=2) < 1e-12
    odd = np.diag([(s & mask).bit_count() % 2 for s in masks])
    invalid_sum = np.eye(len(G)) - 2 * frame @ odd @ frame.conj().T
    assert np.linalg.norm(invalid_sum.conj().T @ invalid_sum - np.eye(len(G)), ord=2) > 1e-8
    # Independent normalized hybrid comparison, before any assumption about magnitudes.
    coefficients = np.arange(1, len(G) + 1, dtype=float)
    coefficients /= np.linalg.norm(coefficients)
    actual = np.einsum("is,js,ks,s->ijk", frame, frame, frame, coefficients)
    hybrid = np.einsum("is,js,ks,s->ijk", np.eye(len(G)), frame, frame, coefficients)
    assert np.linalg.norm(hybrid) == pytest.approx(1, abs=1e-12)
    eta = gamma * (1 + gamma) ** 2
    assert np.linalg.norm(actual - hybrid) <= eta
    actual /= np.linalg.norm(actual)
    distance = math.sqrt(max(0, 1 - abs(np.vdot(actual, hybrid)) ** 2))
    assert distance <= 2 * eta / (1 - eta)


def test_public_predicate_phase_is_not_the_encoded_support_phase():
    problem = instance(7, 4, 2, 2, 29)
    accepted = np.array([problem.accepted(0, problem.evaluations(w)[0]) for w in product(range(7), repeat=2)])
    rho = float(problem.density)
    g = (accepted - rho) / math.sqrt(rho * (1 - rho))
    vacuum = np.ones(49) / 7
    frame = np.column_stack([vacuum, g / 7])
    U, _ = reflection_product(frame, [0, 1], 1)
    assert np.max(abs(U @ vacuum - vacuum)) < 1e-13
    cheap_wrong_action = np.sign(g) * vacuum
    assert math.sqrt(1 - abs(np.vdot(cheap_wrong_action, vacuum)) ** 2) > 0.98


@pytest.mark.parametrize("copies", [5, 8])
def test_large_rescue_survives_error_accounting_but_not_cost_accounting(copies):
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29)
    row = feedback_certificate(problem, 32, copies)
    assert row["status"] == "CONDITIONAL_FEEDBACK_RESTORATION_WITH_EXPONENTIAL_REFLECTION_CONSTRUCTION"
    assert row["bound_is_nontrivial"]
    assert Fraction(row["corrected_vs_original_single_copy_TV_upper_exact"]) < Fraction(4, 10 ** 9)
    assert Fraction(row["positive_branch_magnitude_distance_upper_exact"]) < Fraction(1, 10 ** 16)
    assert Fraction(row["reflection_product_vs_polar_phase_operator_error_upper_exact"]) < Fraction(2, 10 ** 38)
    assert Fraction(row["rank_heralded_nonzero_mask_probability_lower_exact"]) > Fraction(99, 100)
    assert int(row["every_nonzero_mask_reflection_calls_lower_decimal"]) > 4 * 10 ** 29
    assert Fraction(row["rank_heralded_expected_reflection_calls_lower_exact"]) > 4 * 10 ** 29
    readout = row["conditional_finite_readout"]
    assert Fraction(readout["rank_heralded_corrected_mean_lower_exact"]) > Fraction(902, 1000)
    assert Fraction(readout["tails"][0]["one_attempt_with_rank_herald_lower_exact"]) > Fraction(314, 1000)
    assert row["all_auxiliary_outcomes_retained"]
    assert row["exponential_cost_is_of_this_construction_not_a_general_lower_bound"]
    assert not row["polynomial_encoded_phase_compiler_supplied"]
    assert not row["native_state_reflection_gate_compiler_supplied"]
    assert not row["accepted_speedup_candidate"]


def test_unknown_cases_and_calibration_input_guards():
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29)
    assert feedback_certificate(problem, 32, 2)["status"] == "UNKNOWN_COLLABORATIVE_EQUATION_BUDGET"
    weak = feedback_certificate(instance(7, 6, 3, 2, 29), 2, 2, thresholds=(5,))
    assert weak["status"] == "UNKNOWN_POLAR_NORMALIZATION_BOUND_TOO_WEAK"
    with pytest.raises(ValueError, match="congruent"):
        feedback_certificate(instance(5, 4, 2, 2, 29), 1, 2)
    with pytest.raises(ValueError, match="copies"):
        feedback_certificate(problem, 32, 1)
    with pytest.raises(ValueError, match="mask weight"):
        reflection_count(4, 1, 5)
    with pytest.raises(ValueError, match="unit-norm"):
        reflection_product(np.ones((2, 2)), [0, 1], 1)
    with pytest.raises(ValueError, match="bounded dense"):
        reflection_product(np.eye(257), list(range(257)), 1)
    with pytest.raises(ValueError, match="capped"):
        physical_control(19)


def test_live_artifact_and_local_evidence_provenance():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert report["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    assert not report["generic_index_erasure_lower_bound_transferred_to_this_family"]
    assert not report["efficient_decoder_bypass_supplied"]
    assert not report["new_central_candidate_negative_or_proof_registered"]
    assert not report["new_algorithm_speedup_or_novelty_claimed"]
    assert not report["independent_or_formal_application_review_completed"]
    contract = json.loads((REPORT.parents[1] / "hypotheses/prime_character_phase_feedback_contract.json").read_text())
    for path in contract["evidence"]:
        assert (REPORT.parents[2] / path).is_file()
