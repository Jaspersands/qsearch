"""Parameterized simultaneous phase alignment using a decoded sine-box source.

Written quantum algorithm, pending independent review. Classical decoder and
bounded Fourier controls only; no native quantum execution or speedup claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import product
import json
from math import isqrt, prod
from pathlib import Path
import random
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import arb, ctx, fmpq, fmpz_mat
from theorems import integer_character_interpolation as base
from theorems import integer_character_babai as babai
from theorems import integer_character_near_vector as near

REPORT = ROOT / "research/phase_workbench/integer_character_sine_box.json"


def _q(value):
    if type(value) not in (int, Q):
        raise ValueError("exact rational input required")
    return Q(value)


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")
    return value


def _width(m, tolerance):
    _positive(m, "dimension")
    tolerance = _q(tolerance)
    if not 0 < tolerance < Q(1, 2):
        raise ValueError("tolerance must lie strictly between zero and one half")
    p, q = tolerance.numerator, tolerance.denominator
    w = isqrt(m*q*q//(p*p))
    return w+int(w*w*p*p < m*q*q)


def budget(m, tolerance, failure_bits=20):
    """Exact ledger using pi^2 < 10 and 1-cos(2*pi*d) >= 8*d^2."""
    _positive(failure_bits, "failure bits")
    tolerance = _q(tolerance)
    w = _width(m, tolerance)
    ideal_failure = Q(5*m, 32*(w+1)**2*tolerance**2)
    tv = Q(1, 32)
    if not ideal_failure < Q(5, 32):
        raise ArithmeticError("width does not meet the simultaneous-alignment budget")
    return {
        "dimension": m, "normalized_phase_tolerance": str(tolerance),
        "half_width": w, "source_symbols_per_coordinate": 2*w+1,
        "ideal_failure_upper": str(ideal_failure),
        "implemented_output_tv_upper": str(tv),
        "implemented_success_lower": str(1-ideal_failure-tv),
        "uniform_success_lower": "13/16",
        "full_trials": failure_bits,
        "failure_probability_upper": str(Q(3, 16)**failure_bits),
        "source_postselection": False,
        "source_unitary_operator_error_budget": "1/64",
        "fourier_operator_error_budget": "1/64",
        "source_table_size_per_coordinate": 2*w+1,
        "compiled_fault_tolerant_gate_counts": False,
    }


def license_box(primes, width, exponent):
    base.validate_support(primes)
    _positive(width, "half width")
    if type(exponent) is not int or exponent < 2:
        raise ValueError("modulus exponent at least two required")
    height = prod(primes)**width
    modulus = 3**exponent
    guard = 2*height*height*max(primes)
    if modulus <= guard:
        raise ValueError("sine-box norm AND first-moment height guard fails")
    return {
        "modulus": modulus, "order": 2*3**(exponent-1), "height": height,
        "guard": guard, "exponent": exponent,
        "strict_guard": "3^k > 2*(product_i p_i)^(2*w)*max_i p_i",
    }


def construct(primes, width):
    base.validate_support(primes)
    _positive(width, "half width")
    guard = 2*prod(primes)**(2*width)*max(primes)
    exponent, modulus = 2, 9
    while modulus <= guard:
        exponent += 1
        modulus *= 3
    result = license_box(primes, width, exponent)
    labels = tuple(base.lifted_log(p, exponent)[0] for p in primes)
    base.validate_public_labels(primes, labels, exponent)
    return {**result, "primes": tuple(primes), "width": width, "labels": labels}


def decode(instance, syndrome):
    """Syndrome-only rational reconstruction with PUBLIC trial factors."""
    n, modulus = instance["order"], instance["modulus"]
    if type(syndrome) is not int or not 0 <= syndrome < n:
        raise ValueError("canonical integer syndrome required")
    ratio = base.rational_reconstruct(pow(2, syndrome, modulus), modulus)
    if ratio is None or ratio <= 0:
        return None
    numerator, denominator = ratio.numerator, ratio.denominator
    word = []
    for p in instance["primes"]:
        plus = minus = 0
        while numerator % p == 0:
            numerator //= p
            plus += 1
        while denominator % p == 0:
            denominator //= p
            minus += 1
        word.append(plus-minus)
    if numerator != 1 or denominator != 1 or any(abs(y) > instance["width"] for y in word):
        return None
    return tuple(word)


def verify(instance, centers, assignment, tolerance):
    """Exact max-coordinate certificate, not an average cosine threshold."""
    tolerance = _q(tolerance)
    if not 0 < tolerance < Q(1, 2):
        raise ValueError("strictly positive tolerance below one half required")
    n = instance["order"]
    if (type(assignment) is not int or not 0 <= assignment < n
            or len(centers) != len(instance["primes"])
            or any(type(v) is not int or not 0 <= v < n for v in centers)):
        raise ValueError("canonical assignment and one canonical center per prime required")
    residues = [(a*assignment-c) % n for a, c in zip(instance["labels"], centers)]
    errors = tuple(r if 2*r <= n else r-n for r in residues)
    maximum = max(map(abs, errors))
    return {"accepted": maximum*tolerance.denominator <= n*tolerance.numerator,
            "signed_modular_errors": errors,
            "maximum_normalized_error": Q(maximum, n)}


def moment_interval(width, precision=128):
    _positive(width, "half width")
    if type(precision) is not int or precision < 64:
        raise ValueError("interval precision at least 64 required")
    with ctx.workprec(precision):
        value = arb.cos_pi_fmpq(fmpq(1, 2*(width+1)))
        return Q(str(value.lower().fmpq())), Q(str(value.upper().fmpq()))


def small_control(primes, width, seed):
    """Dense output-space identity check, explicitly capped and not scalable."""
    instance = construct(primes, width)
    n, m = instance["order"], len(primes)
    if n > 200000 or (2*width+1)**m > 10000:
        raise ValueError("dense Fourier identity control exceeds its declared cap")
    rng = random.Random(seed)
    centers = tuple(rng.randrange(n) for _ in primes)
    symbols = tuple(range(-width, width+1))
    amplitudes = np.sin(np.pi*np.arange(1, 2*width+2)/(2*width+2))/np.sqrt(width+1)
    state = np.zeros(n, dtype=complex)
    seen = set()
    for word in product(symbols, repeat=m):
        syndrome = sum(a*y for a, y in zip(instance["labels"], word)) % n
        if syndrome in seen or decode(instance, syndrome) != word:
            raise ArithmeticError("source collision or actual decoder failure")
        seen.add(syndrome)
        phase = sum(c*y for c, y in zip(centers, word)) % n
        state[syndrome] = prod(amplitudes[y+width] for y in word)*np.exp(-2j*np.pi*phase/n)
    norm = float(np.vdot(state, state).real)
    law = abs(np.fft.ifft(state)*np.sqrt(n))**2
    # Independent product-amplitude law after correct syndrome erasure.
    direct = np.ones(n, dtype=complex)/np.sqrt(n)
    scores, squared = [], np.zeros(n)
    outputs = np.arange(n, dtype=np.int64)
    for a, c in zip(instance["labels"], centers):
        residue = (a*outputs-c) % n
        theta = 2*np.pi*residue/n
        factor = sum(amplitudes[y+width]*np.exp(1j*y*theta) for y in symbols)
        direct *= factor
        scores.append(float(np.dot(law, np.cos(theta))))
        distance = np.minimum(residue, n-residue)/n
        squared += distance*distance
    residual = float(np.max(abs(law-abs(direct)**2)))
    expected = float(sum(moment_interval(width))/2)
    if abs(norm-1) > 1e-12 or abs(float(law.sum())-1) > 1e-12 or residual > 1e-12:
        raise ArithmeticError("normalized whole-law Fourier check failed")
    if max(abs(score-expected) for score in scores) > 1e-12:
        raise ArithmeticError("a coordinate mean failed the sine-path identity")
    return {
        "primes": primes, "half_width": width, "exponent": instance["exponent"],
        "cyclic_order": n, "seed": seed, "centers": centers,
        "source_words_checked": len(seen), "source_norm": norm,
        "output_mass": float(law.sum()), "coordinate_cosine_means": scores,
        "expected_coordinate_mean": expected, "whole_law_max_residual": residual,
        "mean_squared_torus_distance": float(np.dot(law, squared)),
        "squared_distance_upper": float(Q(5*m, 32*(width+1)**2)),
        "dense_control_not_a_quantum_execution": True,
    }


def native_decoder_control():
    m, tolerance, seed = 32, Q(1, 4), 2026102043
    bound = budget(m, tolerance)
    start = time.perf_counter()
    instance = construct(base.prime_support(m), bound["half_width"])
    preprocessing = time.perf_counter()-start
    w, n = instance["width"], instance["order"]
    rng = random.Random(seed)
    words = [(w,)*m, (-w,)*m, tuple(w if j % 2 else -w for j in range(m)), (0,)*m]
    words.extend(tuple(rng.randrange(-w, w+1) for _ in range(m)) for _ in range(8))
    start = time.perf_counter()
    records = []
    for word in words:
        syndrome = sum(a*y for a, y in zip(instance["labels"], word)) % n
        recovered = decode(instance, syndrome)
        if recovered != word:
            raise ArithmeticError("native syndrome-only decoder failed")
        records.append({"word": word, "syndrome_hex": hex(syndrome), "decoded_exactly": True})
    decoding = time.perf_counter()-start
    centers = tuple(rng.randrange(n) for _ in range(m))
    start = time.perf_counter()
    _, rows = near.lattice_bases(instance["labels"], n)
    reduced = tuple(tuple(map(int, row)) for row in fmpz_mat(rows).lll(delta=0.99, eta=0.51).tolist())
    lll_seconds = time.perf_counter()-start
    start = time.perf_counter()
    exact = babai.exact_normalized_babai(reduced, instance["labels"], n, centers)
    checked = verify(instance, centers, exact["assignment"], tolerance)
    radius_squared = exact["normalized_gs_trace_upper"]/4
    certificate_seconds = time.perf_counter()-start
    return {
        "dimension": m, "budget": bound, "primes": instance["primes"],
        "labels_hex": [hex(a) for a in instance["labels"]],
        "modulus_exponent": instance["exponent"], "modulus_bits": instance["modulus"].bit_length(),
        "cyclic_order_hex": hex(n), "seed": seed, "decoder_controls": records,
        "classical_preprocessing_seconds": preprocessing,
        "classical_decoder_control_seconds": decoding,
        "classical_same_task": {
            "method": "one full-dimensional FLINT LLL and exact rational Babai; no sweep",
            "centers_hex": [hex(c) for c in centers],
            "basis_hex": [[hex(v) for v in row] for row in reduced],
            "assignment_hex": hex(exact["assignment"]),
            "accepted": checked["accepted"],
            "maximum_normalized_error": str(checked["maximum_normalized_error"]),
            "all_target_squared_euclidean_radius_upper": str(radius_squared),
            "all_target_max_coordinate_tolerance_certified": radius_squared <= tolerance*tolerance,
            "full_lattice_index_verified": exact["full_lattice_index_verified"],
            "lll_seconds": lll_seconds, "exact_certificate_seconds": certificate_seconds,
            "preprocessing_shared_and_charged": True,
            "asymptotic_classical_polynomial_guarantee_claimed": False,
        },
        "quantum_output_samples_generated": 0,
        "scalable_quantum_circuit_compiled": False,
        "classical_same_task_solver_executed": True,
        "calibration_not_hardness_evidence": True,
    }


def report():
    return {
        "id": "INTEGER-CHARACTER-SINE-BOX",
        "status": "constructive_quantum_argument_pending_independent_review",
        "task": "All prescribed prime-character phases within rational torus tolerance, on a newly licensed modulus.",
        "algorithm": "Product sine source, injective syndrome map, rational decoder erasure, cyclic QFT, exact verifier.",
        "uniform_budget_example": budget(20000, Q(1, 10)),
        "controls": [small_control((2, 5), 1, 31), small_control((2, 5), 2, 37),
                     small_control((2, 5, 7), 1, 41)],
        "native": native_decoder_control(),
        "novelty_established": False, "classical_hardness_or_speedup_established": False,
        "old_modulus_or_benchmark_reused": False,
        "prior_art": ["https://doi.org/10.1007/s10623-018-0573-3",
                      "https://arxiv.org/abs/2408.08292"],
        "next_gate": "Independent proof/novelty review and a matched classical all-coordinate solver, not a width sweep.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    native = result["native"]
    print(json.dumps({"report": str(args.output), "status": result["status"],
                      "dimension": native["dimension"],
                      "width": native["budget"]["half_width"],
                      "modulus_bits": native["modulus_bits"],
                      "preprocessing_seconds": native["classical_preprocessing_seconds"],
                      "decoding_seconds": native["classical_decoder_control_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
