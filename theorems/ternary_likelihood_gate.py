"""Exact orthogonal likelihoods of native ternary MUB measurement records.

LOCAL DERIVATION / REVIEW PENDING. Statistical-query and observation-density
gates only. Raw-sample algebraic inference and quantum receivers remain open.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

import numpy as np

from ternary_incidence_decoder import decode_native_control, measurement_probabilities

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_likelihood_gate.json"


def _integer(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def centered_characters(secret, modulus):
    """Six Fourier indices on (a,c,b,o), not a table over secrets or labels."""
    _integer(modulus, "phase modulus", 3)
    secret = tuple(secret)
    if not secret or any(type(x) is not int or not 0 <= x < modulus for x in secret):
        raise ValueError("canonical nonempty modular secret calibration required")
    if modulus % 3:
        raise ValueError("modulus divisible by3 required")
    zero, negative = (0,)*len(secret), tuple(-s % modulus for s in secret)
    return ((secret, zero, 2, 2), (negative, zero, 1, 1),
            (zero, secret, 2, 1), (zero, negative, 1, 2),
            (negative, secret, 0, 2), (secret, negative, 0, 1))


def exact_centered_gram(first, second, modulus):
    if len(first) != len(second):
        raise ValueError("same secret dimension required")
    return Fraction(len(set(centered_characters(first, modulus)) & set(centered_characters(second, modulus))), 9)


def likelihood_ratio(first, second, secret, modulus, basis, outcome):
    """Density relative to uniform public labels, basis, and outcome."""
    if type(outcome) is not int or outcome not in (0, 1, 2):
        raise ValueError("canonical measurement outcome required")
    return 3*measurement_probabilities(first, second, secret, modulus, basis)[outcome]


def likelihood_spectrum(first, second, modulus, basis, outcome):
    """Sparse Fourier density as (group index, F3 coefficient phase, scale)."""
    _integer(modulus, "phase modulus", 3)
    first, second = tuple(first), tuple(second)
    if not first or len(first) != len(second) or modulus % 3:
        raise ValueError("matching nonempty frequency vectors and modulus divisible by3 required")
    if any(type(x) is not int or not 0 <= x < modulus for x in (*first, *second)):
        raise ValueError("canonical modular frequencies required")
    if any(type(x) is not int or x not in (0, 1, 2) for x in (basis, outcome)):
        raise ValueError("canonical MUB basis and outcome required")
    difference = tuple((c-a) % modulus for a, c in zip(first, second))
    positive = ((first, (-basis-outcome) % 3),
                (second, (-basis-2*outcome) % 3), (difference, -outcome % 3))
    terms = [((0,)*len(first), 0, Fraction(1))]
    for frequency, phase in positive:
        terms.append((frequency, phase, Fraction(1, 3)))
        terms.append((tuple(-x % modulus for x in frequency), -phase % 3, Fraction(1, 3)))
    return tuple(terms)


def sq_gate(n, digits, queries, tolerance, arity=1):
    for value, name in ((n, "dimension"), (digits, "root digits"), (arity, "record arity")):
        _integer(value, name)
    _integer(queries, "bounded expectation query count", 0)
    if not isinstance(tolerance, Fraction) or not 0 < tolerance <= 1:
        raise ValueError("exact Fraction tolerance in (0,1] required")
    N, norm = 3**(n*digits), Fraction(5, 3)**arity-1
    affected = norm//(tolerance*tolerance)
    success = min(Fraction(1), Fraction(queries*affected+1, N))
    return {"dimension": n, "root_digits": digits, "secret_count": str(N),
            "records_per_query": arity, "bounded_expectation_queries": queries,
            "absolute_tolerance": str(tolerance),
            "centered_likelihood_norm_squared": str(norm),
            "secrets_affected_per_reference_answer_upper": str(affected),
            "uniform_secret_identification_success_upper": str(success),
            "oracle_model": "adversarial legal STAT(tau); arbitrary bounded real function of k IID records",
            "raw_samples_or_growing_arity_joint_inference_ruled_out": False,
            "source_label_adaptive_measurements_covered": False,
            "general_classical_hardness_proved": False,
            "novelty_or_quantum_advantage_claim": False}


def observation_gate(n, digits, samples):
    for value, name in ((n, "dimension"), (digits, "root digits")):
        _integer(value, name)
    _integer(samples, "measurement record count", 0)
    N = 3**(n*digits)
    squared = min(Fraction(1), Fraction(5, 3)**samples/N)
    return {"dimension": n, "root_digits": digits, "measurement_records": samples,
            "secret_count": str(N),
            "uniform_secret_success_squared_upper": str(squared),
            "source": "IID uniform even native frequencies; uniform independent quadratic F3 MUB bases; full classical labels retained",
            "unlimited_processing_of_this_classical_record_source_covered": True,
            "arbitrary_or_collective_quantum_measurements_covered": False,
            "more_legitimately_charged_records_ruled_out": False,
            "efficient_decoding_above_threshold_proved": False}


def dense_gram_control(n, modulus):
    if type(n) is not int or n < 1 or type(modulus) is not int or modulus < 3 or modulus % 3 or modulus**n > 27:
        raise ValueError("bounded complete source calibration: modulus divisible by3 and group size<=27")
    secrets = tuple(product(range(modulus), repeat=n))
    secret_matrix = np.array(secrets, dtype=np.int64)
    centered = []
    probability_error = 0.
    for first, second, basis in product(secrets, secrets, range(3)):
        first_phase = (secret_matrix@np.array(first)) % modulus
        second_phase = (secret_matrix@np.array(second)) % modulus
        probabilities = []
        for outcome in range(3):
            amplitude = (1+np.exp(2j*np.pi*(first_phase/modulus-(basis+outcome)/3))
                         +np.exp(2j*np.pi*(second_phase/modulus-(4*basis+2*outcome)/3)))
            ratio = abs(amplitude)**2/3
            probabilities.append(ratio/3)
            centered.append(ratio-1)
        probability_error = max(probability_error, float(max(abs(sum(probabilities)-1))))
    matrix = np.array(centered)
    gram = matrix.T@matrix/len(matrix)
    target = 2/3*np.eye(len(secrets))
    error = float(np.max(abs(gram-target)))
    assert error < 1e-12 and probability_error < 1e-12
    return {"dimension": n, "phase_modulus": modulus, "secret_vectors": secrets,
            "complete_public_label_basis_outcome_records": len(matrix),
            "centered_Gram_matrix": gram.tolist(),
            "maximum_orthogonality_error": error,
            "maximum_probability_normalization_error": probability_error,
            "bounded_exhaustive_source_not_a_scalable_learner": True}


def run_controls():
    # Same observation model has a polynomial raw-sample decoder at R=3.
    # It is a mandatory counterexample to promoting SQ hardness to hardness.
    easy = decode_native_control(8, 62908)
    return {"status": "LOCAL_LIKELIHOOD_SQ_APPLICATION_REVIEW_PENDING",
            "exact_single_record_centered_Gram": "(2/3)*I on ALL modular secrets, including zero",
            "exact_k_record_centered_Gram": "((5/3)^k-1)*I",
            "dense_native_source_controls": [dense_gram_control(n, q) for n, q in ((1, 3), (1, 9), (2, 3), (1, 27))],
            "SQ_scaling_ledgers": [sq_gate(n, r, (n*r)**3, Fraction(1, n*r), k)
                                   for n, r in ((8, 1), (32, 4), (128, 8)) for k in (1, 2, 4)],
            "near_entropy_observation_ledgers": [observation_gate(n, r, n*r) for n, r in ((8, 1), (32, 4), (128, 8))],
            "raw_sample_field_decoder_counterexample": easy,
            "claim_gate": {"candidate_accepted": False, "general_classical_hardness": False,
                           "new_quantum_algorithm": False, "all_single_qutrit_measurements_excluded": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "source_Gram_controls": 4,
                      "general_classical_hardness": False}))


if __name__ == "__main__":
    main()
