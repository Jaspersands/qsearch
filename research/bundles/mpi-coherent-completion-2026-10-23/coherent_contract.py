"""Exact budgets and finite falsifiers, not a compiled MPI quantum solver."""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
from math import isqrt
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
FIELD_PATH = HERE.parent / "inverse-trace-residual-2026-10-23/residual_sat.py"
spec = importlib.util.spec_from_file_location("mpi_completion_field", FIELD_PATH)
field_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = field_module
spec.loader.exec_module(field_module)
BinaryField = field_module.BinaryField


def box_mass(m, a, b, t):
    """Exact multinomial recurrence; inherited mathematics, independently replayed."""
    if type(m) is not int or m < 0 or type(a) is not int or type(b) is not int:
        raise ValueError("integer dimensions required")
    if not isinstance(t, F) or not 0 < t < 1:
        raise ValueError("exact probability in (0,1) required")
    if min(a, b) < 0:
        return F(0)
    active, denominator = (t / 2).as_integer_ratio()
    zero = denominator - 2 * active
    start = zero**m
    total = 0
    for plus in range(min(m, a) + 1):
        term = start
        for minus in range(min(m - plus, b) + 1):
            total += term
            if minus < min(m - plus, b):
                term, remainder = divmod(term * (m - plus - minus) * active,
                                         (minus + 1) * zero)
                if remainder:
                    raise ArithmeticError("nonintegral multinomial recurrence")
        if plus < min(m, a):
            start, remainder = divmod(start * (m - plus) * active, (plus + 1) * zero)
            if remainder:
                raise ArithmeticError("nonintegral multinomial recurrence")
    return F(total, denominator**m)


def source_certificate(m, n, cap, t, bits=160):
    if any(type(v) is not int for v in (m, n, cap, bits)) or min(m, n, bits) < 1 or cap < 0:
        raise ValueError("invalid source parameters")
    if n < 2 * cap + 2:
        raise ValueError("score separation requires n >= 2*cap+2")
    mass = box_mass(m, cap, cap, t)
    edge = box_mass(m - 1, cap - 1, cap, t)
    radicand = 2 * t * (1 - t)
    scale = 1 << bits
    root = isqrt(radicand.numerator * scale**2 // radicand.denominator)
    return {"mass": mass, "mean_lower": F(root, scale) * edge / mass,
            "mean_upper": F(root + 1, scale) * edge / mass}


def success_plan(mass_lower, mean_lower, *, threshold=F(3, 10),
                 score_error=F(1, 1000), instrument_error=F(1, 1000),
                 source_tries=2, failure_bits=40):
    values = (mass_lower, mean_lower, threshold, score_error, instrument_error)
    if not all(isinstance(v, F) for v in values):
        raise ValueError("rational bounds required")
    if not 0 < mass_lower <= 1 or not -1 <= mean_lower <= 1:
        raise ValueError("invalid source bounds")
    if not -1 < threshold < 1 or not 0 < score_error < 1 or not 0 <= instrument_error < 1:
        raise ValueError("invalid error or threshold")
    if any(type(v) is not int or v < 1 for v in (source_tries, failure_bits)):
        raise ValueError("positive integer caps required")
    safe_threshold = threshold + 2 * score_error
    if safe_threshold >= mean_lower or safe_threshold >= 1:
        raise ValueError("no certified score margin")
    ideal_tail = (mean_lower - safe_threshold) / (1 - safe_threshold)
    prepared = 1 - (1 - mass_lower)**source_tries
    success = prepared * ideal_tail - instrument_error
    if success <= 0:
        raise ValueError("complete-instrument error consumes the success bound")
    # Bernoulli: (1-p)^(-k) >= 1+k*p, so k=ceil(1/p) halves failure.
    half_block = (success.denominator + success.numerator - 1) // success.numerator
    rounds = half_block * failure_bits
    return {"mass_lower": mass_lower, "mean_lower": mean_lower,
            "threshold": threshold, "score_absolute_error": score_error,
            "guaranteed_acceptance_threshold": safe_threshold,
            "complete_instrument_TV_error": instrument_error,
            "source_tries_per_round": source_tries,
            "source_success_lower": prepared, "ideal_score_tail_lower": ideal_tail,
            "verified_success_per_round_lower": success,
            "round_cap": rounds, "raw_preparation_cap": source_tries * rounds,
            "failure_bits": failure_bits, "failure_upper": F(1, 1 << failure_bits),
            "bound_uses_conditioning_away_abort": False}


def resource_contract(m, n, h, cap, plan):
    if any(type(v) is not int or v < 1 for v in (m, n, h)) or h < 3:
        raise ValueError("invalid dimensions")
    if type(cap) is not int or cap < 0 or n < 2 * cap + 2 or m + n > 1 << h:
        raise ValueError("points or separation budget invalid")
    error, tries = plan["complete_instrument_TV_error"], plan["source_tries_per_round"]
    if error <= 0:
        raise ValueError("finite synthesis needs positive error")
    return {
        "cyclic_order": (1 << h) - 1,
        "logical_data_qubits_without_workspace": 2*m + n*h,
        "source_single_qubit_rotation_calls_per_round_upper": tries*m,
        "center_phase_calls_per_round_upper": 2*m,
        "modular_constant_add_subtracts_per_round": 2*m*n,
        "arbitrary_modulus_QFT_calls_per_round": n,
        "decoder_compute_and_uncompute_calls_per_round": 2,
        "max_operator_error_per_source_rotation": error / (3*tries*m),
        "max_operator_error_per_center_phase": error / (6*m),
        "max_operator_error_per_QFT": error / (3*n),
        "decoder_field_operation_asymptotic": "O(n^3 + m*n + n*h)",
        "decoder_bit_operation_asymptotic": "T=O((n^3 + m*n + n*h)*h^3), ordinary classical computation",
        "oblivious_decoder_Boolean_size_asymptotic": "O(T^2) suffices by conservative circuit simulation",
        "reversible_decoder_space_asymptotic": "O(T^2) suffices by full-history simulation of that circuit",
        "total_gate_asymptotic": "round_cap * poly(m,n,h,bitlength(t),log(1/instrument_error))",
        "explicit_public_B_required_or_preprocessing_paid": True,
        "exponentiation_uses_binary_field_arithmetic_not_qRAM": True,
        "Shor_discrete_log_calls": 0,
        "synthesized_gate_count": None,
        "compiled_quantum_solver_executed": False,
    }


def fixture():
    """Actual reduced MPI instance over F16; exponential diagnostic only."""
    field = BinaryField(4, 0b10011)
    power, logs = 1, {}
    for exponent in range(15):
        if power in logs:
            raise ArithmeticError("generator order too small")
        logs[power] = exponent
        power = field.multiply(power, 2)
    if power != 1 or len(logs) != 15:
        raise ArithmeticError("invalid multiplicative generator")
    supports, evaluations = tuple(range(4)), tuple(range(4, 8))
    matrix = np.array([[logs[t ^ z] for z in evaluations] for t in supports], dtype=int)
    patterns = tuple(y for y in product((-1, 0, 1), repeat=4)
                     if y.count(1) <= 1 and y.count(-1) <= 1)
    codebook = {tuple(map(int, (np.array(y) @ matrix) % 15)): y for y in patterns}
    if len(codebook) != len(patterns):
        raise ArithmeticError("syndrome collision")
    return matrix, patterns, codebook


def finite_decoder(words, codebook):
    """TOTAL finite reference map, not the scalable rational decoder."""
    if len(words) != 4 or any(type(w) is not int or not 0 <= w < 16 for w in words):
        raise ValueError("four 4-bit words required")
    result = codebook.get(tuple(words))
    return (False, (0,)*4) if result is None else (True, result)


def arctan_interval(inverse, tolerance):
    if type(inverse) is not int or inverse <= 1 or tolerance <= 0:
        raise ValueError("invalid arctangent parameters")
    x, total, index = F(1, inverse), F(0), 0
    while True:
        total += (-1)**index * x**(2*index+1) / (2*index+1)
        index += 1
        following = (-1)**index * x**(2*index+1) / (2*index+1)
        if abs(following) <= tolerance:
            return min(total, total+following), max(total, total+following)


def cosine_interval(residue, order, error):
    if type(order) is not int or order < 2 or type(residue) is not int:
        raise ValueError("integer residue and modulus required")
    if not isinstance(error, F) or not 0 < error < 1:
        raise ValueError("positive rational error below one required")
    # Machin's identity and alternating remainders avoid an unverified libm cutoff.
    a, b = arctan_interval(5, error/1000), arctan_interval(239, error/1000)
    pi_lo, pi_hi = 16*a[0]-4*b[1], 16*a[1]-4*b[0]
    residue %= order
    residue = min(residue, order-residue)
    ratio = F(2*residue, order)
    x = ratio*(pi_lo+pi_hi)/2
    phase_error = ratio*(pi_hi-pi_lo)/2
    term, total, index = F(1), F(1), 0
    while True:
        index += 1
        term *= -x*x/((2*index-1)*(2*index))
        total += term
        following = abs(term*x*x/((2*index+1)*(2*index+2)))
        if index >= 1 and following+phase_error <= error:
            radius = following+phase_error
            return max(F(-1), total-radius), min(F(1), total+radius)


def verified_score(matrix, centers, assignment, order, *, error=F(1, 1000), threshold=F(3, 10)):
    if (not matrix or len(matrix) != len(centers) or not assignment
            or any(len(row) != len(assignment) for row in matrix)):
        raise ValueError("inconsistent explicit objective dimensions")
    if type(order) is not int or order < 2:
        raise ValueError("invalid modulus")
    if any(type(v) is not int or not 0 <= v < order
           for v in [*centers, *assignment, *(v for row in matrix for v in row)]):
        raise ValueError("canonical integer entries required")
    lower, upper, cache = F(0), F(0), {}
    for row, center in zip(matrix, centers):
        value = (sum(b*x for b, x in zip(row, assignment))-center) % order
        if value not in cache:
            cache[value] = cosine_interval(value, order, error)
        lo, hi = cache[value]
        lower, upper = lower+lo, upper+hi
    lower, upper = lower/len(matrix), upper/len(matrix)
    return {"lower": lower, "upper": upper, "accepted": lower >= threshold}


def instrument_control():
    matrix, patterns, codebook = fixture()
    centers = np.array([0, 2, 4, 6])
    t, mass = F(1, 3), box_mass(4, 1, 1, F(1, 3))
    pilot = np.zeros((15,)*4, dtype=complex)
    sectors = {}
    padded = np.zeros((16,)*4, dtype=complex)
    for syndrome, y in codebook.items():
        active = sum(v != 0 for v in y)
        amplitude = float((1-t)**(4-active)*(t/2)**active/mass)**0.5
        amplitude *= np.exp(-2j*np.pi*int(centers @ np.array(y))/15)
        pilot[syndrome] = padded[syndrome] = amplitude
        sector = (y.count(1), y.count(-1))
        sectors.setdefault(sector, np.zeros_like(pilot))[syndrome] = amplitude
        valid, decoded = finite_decoder(syndrome, codebook)
        if not valid or decoded != y:
            raise ArithmeticError("finite decoder failed on source support")
    probabilities = abs(np.fft.ifftn(pilot, norm="ortho"))**2
    dephased = sum(abs(np.fft.ifftn(block, norm="ortho"))**2 for block in sectors.values())
    assignments = np.indices((15,)*4).reshape(4, -1).T
    scores = np.cos(2*np.pi*((assignments @ matrix.T-centers) % 15)/15).mean(axis=1)
    wrong_full = abs(np.fft.ifftn(padded, norm="ortho"))**2
    wrong_valid = wrong_full[(slice(0, 15),)*4]
    wrong_valid_mass = float(wrong_valid.sum())
    bad_decoder = sum(not finite_decoder(tuple(words), codebook)[0]
                      for words in product(range(16), repeat=4))
    return {
        "scope": "exponential finite instrument falsifier, NOT a scalable decoder or optimizer run",
        "licensed_patterns": len(patterns), "all_bitstring_syndromes_checked": 16**4,
        "decoder_invalid_outputs": bad_decoder,
        "correct_norm": float(probabilities.sum()),
        "correct_mean": float(probabilities.ravel() @ scores),
        "count_record_retained_mean": float(dephased.ravel() @ scores),
        "count_record_retained_TV_from_correct": float(abs(dephased-probabilities).sum()/2),
        "wrong_power_of_two_QFT_invalid_output_mass": 1-wrong_valid_mass,
        "wrong_power_of_two_QFT_TV_including_abort":
            float((abs(wrong_valid-probabilities).sum()+1-wrong_valid_mass)/2),
        "wrong_QFT_conditioned_valid_mean": float(wrong_valid.ravel() @ scores/wrong_valid_mass),
        "compiled_native_solver": False,
    }


def short_fraction(value, bits=160, upper=False):
    scale = 1 << bits
    numerator = value.numerator * scale
    rounded = -(-numerator // value.denominator) if upper else numerator // value.denominator
    return F(rounded, scale)


def report():
    from decoder_replay import replay
    cert = source_certificate(6000, 420, 209, F(13, 200))
    if cert["mass"] < F(7, 10) or cert["mean_lower"] < F(342, 1000):
        raise ArithmeticError("native conservative constants are not certified")
    plan = success_plan(F(7, 10), F(342, 1000))
    if plan["verified_success_per_round_lower"] < F(1, 20):
        raise ArithmeticError("one-round lower bound failed")
    source_files = [Path(__file__), HERE / "test_coherent_contract.py",
                    HERE / "decoder_replay.py", FIELD_PATH]
    return {
        "status": "constructive compilation argument UNDER REVIEW; no speedup admission",
        "native": {"m": 6000, "n": 420, "h": 13, "cap": 209, "t": "13/200"},
        "native_certificate": {"mass_lower": short_fraction(cert["mass"]),
                               "mean_lower": short_fraction(cert["mean_lower"]),
                               "mean_upper": short_fraction(cert["mean_upper"], upper=True)},
        "plan": plan, "resources": resource_contract(6000, 420, 13, 209, plan),
        "finite_control": instrument_control(), "unchanged_decoder_replay": replay(),
        "sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
        "quantum_optimizer_executed": False, "classical_hardness_established": False,
    }


if __name__ == "__main__":
    result = report()
    target = HERE / "coherent_receipt.json"
    target.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps({"receipt": str(target), "plan": result["plan"],
                      "finite_control": result["finite_control"]}, indent=2, default=str))
