"""Can positive sparse residual pinning replace a nonlinear DQI filter?

Known quantum mechanism, exact rational readout and a METHOD-SPECIFIC
pin-mixture comparison. This is not a lower bound on classical optimization.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.prime_character_finite_readout import propose_weights, sqrt_interval
from theorems.opi_filter_tail_certificate import _evaluate
from theorems.prime_character_interleaved_probe import decode_burst, syndrome

REPORT = ROOT/"research/reductions/nonlinear_filter_pinning.json"


def parameters(M, rho, degree):
    if type(M) is not int or M < 1 or type(degree) is not int or not 0 <= degree <= M:
        raise ValueError("positive test count and a valid integer degree required")
    if not isinstance(rho, Q) or not 0 < rho < 1:
        raise ValueError("exact rational test density strictly between zero and one required")


def shell_norms(M, rho, degree):
    parameters(M, rho, degree)
    return tuple(Q(comb(M, k))* (rho*(1-rho))**k for k in range(degree+1))


def rational_filter(M, rho, degree, bits=256):
    """Numerics propose weights; all claims refer to this rational polynomial."""
    h = shell_norms(M, rho, degree)
    weights = propose_weights(M, rho, degree)
    coefficients = tuple(w*sqrt_interval(1/norm, bits)[0] for w, norm in zip(weights, h))
    if any(w and not a for w, a in zip(weights, coefficients)):
        raise ValueError("precision erased a proposed coefficient; increase bits")
    return coefficients


def multiply_score(coefficients, M, rho):
    parameters(M, rho, len(coefficients)-1)
    result = [Q(0)]*(min(len(coefficients)+1, M+1))
    for k, a in enumerate(coefficients):
        result[k] += a*(M*rho+(1-2*rho)*k)
        if k < M:
            result[k+1] += a*(k+1)
        if k:
            result[k-1] += a*rho*(1-rho)*(M-k+1)
    return tuple(result)


def filter_value(coefficients, M, rho, score):
    parameters(M, rho, len(coefficients)-1)
    if type(score) is not int or not 0 <= score <= M:
        raise ValueError("physical integer score required")
    previous, current = Q(0), Q(1)
    value = coefficients[0]
    for k in range(len(coefficients)-1):
        nxt = ((score-M*rho-(1-2*rho)*k)*current-rho*(1-rho)*(M-k+1)*previous)/(k+1)
        value += coefficients[k+1]*nxt
        previous, current = current, nxt
    return value


def exact_moments(coefficients, M, rho):
    parameters(M, rho, len(coefficients)-1)
    if any(not isinstance(a, (int, Q)) or isinstance(a, bool) for a in coefficients):
        raise ValueError("explicit rational polynomial required")
    a = tuple(map(Q, coefficients))
    b = multiply_score(a, M, rho)
    h = shell_norms(M, rho, len(b)-1)
    Z = sum(x*x*hi for x, hi in zip(a, h))
    if not Z:
        raise ValueError("nonzero filter required")
    mean = sum(x*y*hi for x, y, hi in zip(a, b, h))/Z
    second = sum(y*y*hi for y, hi in zip(b, h))/Z
    return Z, mean, second


def transfer_budget(dimension, degree, moment_order):
    if any(type(x) is not int or x < 0 for x in (dimension, degree, moment_order)):
        raise ValueError("nonnegative integer transfer parameters required")
    required = 2*(2*degree+moment_order)
    if required > dimension:
        raise ValueError("pairwise tests exceed the native RS independence budget")
    return {"native_RS_dimension": dimension, "filter_degree": degree,
            "moment_order": moment_order, "vertex_budget": required,
            "whole_target_score_distribution_identified": False}


def enclose(value, bits=128, upper=False):
    value = Q(value)
    scale = 1 << bits
    floor, remainder = divmod(value.numerator*scale, value.denominator)
    return Q(floor+int(upper and bool(remainder)), scale)


def tail_witness(M, mean, second, threshold):
    """A quadratic indicator minorant, verified at every physical score."""
    if type(threshold) is not int or not 1 <= threshold <= M:
        raise ValueError("nontrivial physical tail threshold required")
    variance, gap = second-mean*mean, mean-(threshold-1)
    if variance < 0:
        raise ValueError("negative variance")
    if gap <= 0:
        polynomial = (Q(0),)*3
    else:
        center = mean+variance/gap
        denominator = (center-(threshold-1))**2
        polynomial = (1-center*center/denominator, 2*center/denominator, -1/denominator)
    expected = polynomial[0]+polynomial[1]*mean+polynomial[2]*second
    for s in range(M+1):
        if _evaluate(polynomial, Q(s)) > int(s >= threshold):
            raise ArithmeticError("tail minorant failed")
    witness = {"threshold": threshold, "minorant_coefficients": list(map(str, polynomial)),
            "probability_lower_exact": str(expected), "probability_lower_dyadic": str(enclose(expected)),
            "mean": str(mean), "second_moment": str(second), "variance": str(variance),
            "support_points_checked": M+1}
    verify_tail_witness(M, witness)
    return witness


def verify_tail_witness(M, witness):
    mean, second = Q(witness["mean"]), Q(witness["second_moment"])
    poly = tuple(map(Q, witness["minorant_coefficients"]))
    if len(poly) != 3 or not 0 <= mean <= M or not mean*mean <= second <= M*M:
        raise ValueError("invalid moment or polynomial contract")
    if type(witness["threshold"]) is not int or not 1 <= witness["threshold"] <= M:
        raise ValueError("invalid tail threshold")
    for s in range(M+1):
        if _evaluate(poly, Q(s)) > int(s >= witness["threshold"]):
            raise ArithmeticError("corrupt tail minorant")
    expected = poly[0]+poly[1]*mean+poly[2]*second
    if (not 0 <= expected <= 1 or Q(witness["probability_lower_exact"]) != expected
            or Q(witness["probability_lower_dyadic"]) != enclose(expected)
            or Q(witness["variance"]) != second-mean*mean
            or witness["support_points_checked"] != M+1):
        raise ArithmeticError("corrupt expectation or rounding claim")
    return True


def binomial_tail(n, rho, threshold):
    if type(n) is not int or n < 0 or type(threshold) is not int or not isinstance(rho, Q) or not 0 < rho < 1:
        raise ValueError("exact binomial parameters required")
    if threshold <= 0:
        return Q(1)
    if threshold > n:
        return Q(0)
    a, b = rho.numerator, rho.denominator-rho.numerator
    term = comb(n, threshold)*a**threshold*b**(n-threshold)
    numerator = term
    for j in range(threshold, n):
        term, remainder = divmod(term*(n-j)*a, (j+1)*b)
        if remainder:
            raise ArithmeticError("integer binomial recurrence failed")
        numerator += term
    return Q(numerator, rho.denominator**n)


def pinning_comparison(M, rho, pins, witness, approximation_error=Q(0)):
    parameters(M, rho, 0)
    verify_tail_witness(M, witness)
    if type(pins) is not int or not 0 <= pins <= M:
        raise ValueError("explicit residual pin cap required")
    approximation_error = Q(approximation_error)
    if not 0 <= approximation_error <= 1:
        raise ValueError("valid TV approximation allowance required")
    threshold = witness["threshold"]
    # Grant every pinned residual a passing value: this dominates every component.
    exact = binomial_tail(M-pins, rho, threshold-pins)
    upper = enclose(exact, 512, upper=True)
    lower = max(Q(0), Q(witness["probability_lower_dyadic"])-approximation_error)
    norm = max(Q(1), 2*lower/upper-1) if upper else None
    large_pin_mass = max(Q(0), (lower-upper)/(1-upper)) if upper < 1 else Q(0)
    return {"max_pinned_residuals": pins, "threshold": threshold,
            "best_component_tail_expression": {"trials": M-pins, "rho": str(rho), "threshold": threshold-pins},
            "component_tail_upper_dyadic": str(upper), "dyadic_bits": 512,
            "approximation_TV_allowance": str(approximation_error),
            "positive_mixture_tail_deficit_lower": str(max(Q(0), lower-upper)),
            "positive_mixture_mass_above_pin_cap_lower": str(enclose(large_pin_mass)),
            "signed_total_absolute_weight_lower": None if norm is None else str(enclose(norm)),
            "scope": "normalized source residual-cylinder laws only; not general classical search or target code conditioning"}


def residual_map(values, multipliers, prime):
    return (values[0],)+tuple((values[i+1]+a*values[i]*values[i]) % prime for i, a in enumerate(multipliers))


def inverse_residual_map(coordinates, multipliers, prime):
    values = [coordinates[0]]
    for residual, a in zip(coordinates[1:], multipliers):
        values.append((residual-a*values[-1]*values[-1]) % prime)
    return tuple(values)


def native_control():
    """Small explicit scalar-RS calibration, never an advantage candidate."""
    p, n, L = 7, 4, 6
    multipliers = (1, 2, 3, 4, 5)
    sets = ({0, 1, 3}, {1, 2, 6}, {0, 4, 5}, {2, 3, 4}, {0, 2, 5})
    counts = [0]*L
    for coefficients in product(range(p), repeat=n):
        values = tuple(sum(c*pow(x, j, p) for j, c in enumerate(coefficients)) % p for x in range(1, L+1))
        residuals = residual_map(values, multipliers, p)[1:]
        counts[sum(r in F for r, F in zip(residuals, sets))] += 1
    rho, M, a = Q(3, 7), L-1, (Q(1), Q(2, 5))
    Z, mean, second = exact_moments(a, M, rho)
    masses = [Q(count, p**n)*filter_value(a, M, rho, s)**2 for s, count in enumerate(counts)]
    if sum(masses) != Z:
        raise ArithmeticError("native norm-transfer control failed")
    native_mean = sum(s*m for s, m in enumerate(masses))/Z
    return {"prime": p, "dimension": n, "points": list(range(1, L+1)), "multipliers": multipliers,
            "sets": [sorted(F) for F in sets], "score_counts": counts, "filter_coefficients": list(map(str, a)),
            "source_norm": str(Z), "native_norm": str(sum(masses)),
            "source_filtered_mean": str(mean), "native_filtered_mean": str(native_mean),
            "norm_transfer_valid": 4 <= n, "mean_transfer_valid": 6 <= n,
            "forbidden_mean_transfer_error": str(abs(native_mean-mean)),
            "enumerated_polynomials": p**n, "quantum_algorithm_executed": False}


def decoder_control():
    """Pay for a syndrome-only decoder at the actual 100-error degree cap."""
    p, L, n, cap = 2053, 2052, 205, 100
    rng = random.Random(260935101)
    error = [0]*L
    for i in sorted(rng.sample(range(L), cap)):
        error[i] = rng.randrange(1, p)
    measured = syndrome(p, error, n)
    decoded = decode_burst(p, L, n, cap, [measured])
    if decoded["status"] != "VERIFIED_UNIQUE_BURST" or decoded["error_rows"] != [error]:
        raise ArithmeticError("native-degree syndrome-only decoder control failed")
    reconstructed = decoded.pop("error_rows")[0]
    return {"source_error_sparse": [[i, v] for i, v in enumerate(error) if v],
            "recovered_error_sparse": [[i, v] for i, v in enumerate(reconstructed) if v],
            "decoder": decoded, "seed": 260935101, "known_unique_RS_decoder_not_new_algorithm": True,
            "basis_control_NOT_coherent_execution": True, "control_NOT_native_pilot_label_distribution": True}


def run_audit():
    dependencies = [Path(__file__), ROOT/"theorems/prime_character_finite_readout.py",
                    ROOT/"theorems/opi_filter_tail_certificate.py", ROOT/"theorems/bpqm_gibbs_frontier.py",
                    ROOT/"theorems/prime_character_interleaved_probe.py", ROOT/"theorems/prime_character_opi.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}
    p, n, M, D = 2053, 205, 2051, 50
    rho = Q(p-1, 2*p)
    a = rational_filter(M, rho, D)
    Z, mean, second = exact_moments(a, M, rho)
    witness = tail_witness(M, mean, second, 1299)
    comparisons = [pinning_comparison(M, rho, k, witness, Q(1, 100)) for k in (2*D, n-1)]
    threshold_lower = Q(witness["probability_lower_dyadic"])-Q(1, 100)
    repeats = [{"attempts": t, "success_lower_with_0.01_circuit_TV_error": str(enclose(1-(1-threshold_lower)**t))}
               for t in (1, 2, 5, 6, 10)]
    record = {"schema_version": 1, "status": "KNOWN_CONSTRUCTIVE_CANDIDATE_PINNING_ESCAPE_REVIEW_PENDING",
              "source_sha256": hashes, "parameters": {"p": p, "L": p-1, "M": M, "n": n, "D": D, "rho": str(rho)},
              "rational_filter_coefficients": list(map(str, a)), "filter_norm": str(Z),
              "target_transfer": transfer_budget(n, D, 2), "tail_witness": witness,
              "independent_ideal_or_error_budgeted_attempts": repeats, "source_pinning_comparisons": comparisons,
              "native_cutoff_countercontrol": native_control(),
              "decoder_control": decoder_control(),
              "scope": {"new_quantum_algorithm": False, "general_classical_lower_bound": False,
                        "author_benchmark_instances_or_witnesses_reproduced": False, "quantum_circuit_executed": False,
                        "compiled_cost_advantage": False, "independent_review_complete": False},
              "literature": ["https://arxiv.org/abs/2609.35101", "https://zenodo.org/records/22975424",
                             "https://arxiv.org/abs/2610.02145"]}
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}:
        raise RuntimeError("dependency changed during audit")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_audit()
    print(json.dumps({"status": report["status"], "mean_fraction": float(Q(report["tail_witness"]["mean"])/2051),
                      "success_1299_lower": float(Q(report["tail_witness"]["probability_lower_dyadic"])),
                      "pin_components": [{"pins": r["max_pinned_residuals"],
                                          "tail_upper": float(Q(r["component_tail_upper_dyadic"])),
                                          "absolute_weight_lower": float(Q(r["signed_total_absolute_weight_lower"]))}
                                         for r in report["source_pinning_comparisons"]]}))
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
