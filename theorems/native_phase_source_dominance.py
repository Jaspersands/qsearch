"""Original classical-source Bayes ceiling for known phase preparation.

An exact quantum discrimination dual, NOT efficient classical dequantization.
Finite complete-source controls distinguish a readout gain from source advantage.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import fmpq, fmpq_poly
import numpy as np

from native_noisy_phase_input import quantum_input_bound
from ternary_certified_noise_sampler import rational
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_PHASE_SOURCE_DOMINANCE.md"
REPORT = ROOT / "research/classical_baselines/native_phase_source_dominance.json"


def source_likelihoods(labels, q, max_secret_count=81, max_value_count=6561):
    root_digits(q)
    labels = tuple(tuple(a) for a in labels)
    if not labels or len(labels) % 2 or not labels[0] or any(
            len(a) != len(labels[0]) or any(type(x) is not int or not 0 <= x < q for x in a) for a in labels):
        raise ValueError("complete even canonical source-label batch required")
    integer(max_secret_count, "complete secret-space cap", 1)
    integer(max_value_count, "complete classical transcript-space cap", 1)
    G, transcripts = q**len(labels[0]), q**len(labels)
    if G > max_secret_count or transcripts > max_value_count:
        return {"status": "UNKNOWN_COMPLETE_SOURCE_ENUMERATION_CAP", "secret_count": G,
                "classical_transcript_space": transcripts, "likelihoods": None,
                "truncated_reference_promoted": False}
    secrets = tuple(product(range(q), repeat=len(labels[0])))
    chi = ((-1, fmpq(1, 4)), (0, fmpq(1, 2)), (1, fmpq(1, 4)))
    by_value = {}
    for index, s in enumerate(secrets):
        center = tuple(sum(a*b for a, b in zip(row, s)) % q for row in labels)
        for errors in product(chi, repeat=len(labels)):
            values = tuple((x+e) % q for x, (e, _) in zip(center, errors))
            probability = fmpq(1)
            for _, p in errors:
                probability *= p
            if values not in by_value:
                by_value[values] = [fmpq(0)]*G
            by_value[values][index] += probability
    for i in range(G):
        if sum((row[i] for row in by_value.values()), fmpq(0)) != 1:
            raise ArithmeticError("complete conditional source law is not normalized")
    return {"status": "COMPLETE_CALIBRATION_SOURCE_LIKELIHOODS", "secret_count": G,
            "classical_transcript_space": transcripts, "secrets": secrets,
            "likelihoods": by_value, "truncated_reference_promoted": False}


def finite_source_control(n, q, count, seed):
    integer(n, "positive source dimension", 1)
    integer(count, "positive complete native count", 1)
    root_digits(q)
    if q > 9 or count > 2:
        raise ValueError("exact dense-state controls capped at q9,M2")
    rng = random.Random(seed)
    labels = tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(2*count))
    source = source_likelihoods(labels, q)
    if source["likelihoods"] is None:
        return source
    G, D = source["secret_count"], 3**count
    coefficients = [0]*(2*q//3+1)
    coefficients[0] = coefficients[q//3] = coefficients[2*q//3] = 1
    modulus, omega = fmpq_poly(coefficients), fmpq_poly([0, 1])
    roots = tuple(omega**k % modulus for k in range(q))
    words = tuple(product(range(3), repeat=count))
    matrix = lambda: [[fmpq_poly() for _ in range(D)] for _ in range(D)]
    rho = [matrix() for _ in range(G)]
    gamma = matrix()
    maximum_trace, records = fmpq(0), []
    outcome_likelihoods = [[fmpq_poly() for _ in range(G)] for _ in words]
    for values, likelihood in sorted(source["likelihoods"].items()):
        phases = tuple(sum((0, values[2*j], values[2*j+1])[word[j]] for j in range(count)) % q for word in words)
        ceiling = max(likelihood)/G
        maximum_trace += ceiling
        records.append({"values": values, "conditional_probabilities": tuple(map(str, likelihood)),
                        "max_joint_probability": str(ceiling)})
        for i in range(D):
            for j in range(D):
                pure_entry = roots[(phases[i]-phases[j]) % q]/D
                gamma[i][j] += ceiling*pure_entry
                for k, p in enumerate(likelihood):
                    if p:
                        rho[k][i][j] += p*pure_entry
        for j, t in enumerate(words):
            amplitude = sum((roots[(phase-(q//3)*sum(a*b for a, b in zip(word, t))) % q]
                             for word, phase in zip(words, phases)), fmpq_poly())
            conjugate = sum((roots[(-phase+(q//3)*sum(a*b for a, b in zip(word, t))) % q]
                              for word, phase in zip(words, phases)), fmpq_poly())
            probability = amplitude*conjugate % modulus / (D*D)
            for k, p in enumerate(likelihood):
                outcome_likelihoods[j][k] += p*probability
    encode = lambda a: [str(a[i]) for i in range(len(a)-1, -1, -1)]
    evaluate = lambda a: sum(float(a[i])*np.exp(2j*math.pi*i/q) for i in range(len(a)))
    numerical_rho = [np.array([[evaluate(a) for a in row] for row in R]) for R in rho]
    average = sum(numerical_rho)/G
    eig, basis = np.linalg.eigh((average+average.conj().T)/2)
    inverse = (basis*np.array([1/math.sqrt(x) if x > 1e-12 else 0 for x in eig]))@basis.conj().T
    pgm = sum(float(np.trace(inverse@R@inverse@R).real) for R in numerical_rho)/(G*G)
    fourier = sum(max(evaluate(p).real for p in row) for row in outcome_likelihoods)/G
    if pgm > float(maximum_trace)+1e-10 or fourier > float(maximum_trace)+1e-10:
        raise ArithmeticError("a downstream diagnostic exceeds the original source Bayes ceiling")
    return {"status": "EXACT_ORIGINAL_SOURCE_QUANTUM_DUAL_REVIEW_PENDING", "dimension": n,
            "modulus": q, "native_inputs": count, "seed": seed, "labels": labels,
            "uniform_prior_secret_order": source["secrets"],
            "classical_originals": 2*count, "classical_transcript_space": source["classical_transcript_space"],
            "complete_nonzero_transcripts": records,
            "original_source_Bayes_success_exact": str(maximum_trace),
            "quantum_discrimination_dual_exact": [[encode(a) for a in row] for row in gamma],
            "conditional_quantum_densities_exact": [[[encode(a) for a in row] for row in R] for R in rho],
            "native_F3_readout_likelihoods_exact": [[encode(a) for a in row] for row in outcome_likelihoods],
            "numerical_native_F3_MAP_success_diagnostic": float(fourier),
            "numerical_native_PGM_success_diagnostic": pgm,
            "numerical_diagnostics_are_optimality_certificates": False,
            "complete_Bayes_reference_is_efficient_classical_algorithm": False,
            "calibration_is_LWE_hardness_source": False, "computational_quantum_advantage_refuted": False}


def transfer_budget_profile(n, q, alpha, records, receiver_success_lower, failure_bits=64):
    integer(n, "positive source dimension", 1)
    success = rational(receiver_success_lower, "ideal receiver success lower bound")
    alpha = rational(alpha, "continuous source Gaussian width")
    if not 0 < success <= 1 or not 0 < alpha < 1:
        raise ValueError("positive receiver success and subunit positive alpha required")
    V = q*q*alpha*alpha/3+fmpq(1, 2)
    bound = quantum_input_bound(q, records, V, failure_bits)
    loss = rational(bound["M_state_success_loss_before_source_rounding_upper"], "pre-rounding loss")
    return {"dimension": n, "modulus": q, "alpha": str(alpha), "native_inputs": records,
            "hypothetical_ideal_receiver_success_lower": str(success),
            "published_source_parameter_guard": (alpha*q)**2 >= 4*n,
            "noise_and_gate_success_loss_upper": str(loss),
            "pre_rounding_transfer_success_lower": str(max(fmpq(0), success-loss)),
            "pre_rounding_transfer_is_positive": loss < success,
            "noise_budget_failure_is_a_receiver_impossibility_proof": False,
            "source_rounding_not_included_in_this_pre_rounding_profile": True,
            "receiver_implemented": False, "hardness_transfer_admitted": False}


def build_report():
    specs = ((1, 3, 1), (2, 3, 1), (1, 9, 1), (1, 3, 2), (2, 3, 2))
    controls = [finite_source_control(n, q, M, 132000+i) for i, (n, q, M) in enumerate(specs)]
    return {"status": "ORIGINAL_CLASSICAL_SOURCE_STATISTICAL_DOMINANCE_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "controls": controls,
            "source_budget_controls": [transfer_budget_profile(64, 3**64, "1/1048576", M, "1/2")
                                       for M in (512, 2**40)],
            "any_quantum_receiver_Bayes_success_at_most_original_source_MAP": True,
            "information_gain_over_original_classical_source": False,
            "efficient_classical_dequantization_proved": False, "quantum_speedup_refuted": False,
            "accepted_speedup_candidate": False,
            "next_algorithm_obligation": "efficient processing advantage over MATCHED ORIGINAL noisy-linear classical data, not merely a native LOCC readout gap"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "complete_controls": len(report["controls"]),
                      "Bayes_ceilings": [c["original_source_Bayes_success_exact"] for c in report["controls"]],
                      "PGM_minus_F3_MAP_diagnostics": [c["numerical_native_PGM_success_diagnostic"]-c["numerical_native_F3_MAP_success_diagnostic"] for c in report["controls"]],
                      "efficient_classical_dequantization_proved": False}, indent=2))


if __name__ == "__main__":
    main()
