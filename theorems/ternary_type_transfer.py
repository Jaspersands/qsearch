"""Exact-type constraints: quotient obstruction and charged sampling transfer.

Written argument pending independent review. The quantum product decoder is
published prior art, not executed here. Exact character counts and a scalable
but classically easy punctured-simplex calibration test the transfer identities.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import comb, isqrt
from pathlib import Path
import time

from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/ternary_type_transfer.json"


def exact(value):
    value = Fraction(value)
    return {"numerator": value.numerator, "denominator": value.denominator}


def omega_power(value, exponent):
    """Multiply a+b*omega by omega**exponent, with omega**2+omega+1=0."""
    a, b = value
    return ((a, b), (-b, a-b), (b-a, -a))[exponent % 3]


def type_character(counts, plus_count):
    """Exact coefficient of z**h in product_a(omega**-a+z*omega**a)**n_a.

    O(m*h) arithmetic operations, with O(m)-bit integers; no floating phases.
    This evaluates one character, not a general exponential-size code census.
    """
    counts = tuple(counts)
    if (len(counts) != 3 or any(type(x) is not int or x < 0 for x in counts)
            or type(plus_count) is not int or not 0 <= plus_count <= sum(counts)):
        raise ValueError("three nonnegative counts and a valid integer type required")
    coefficients = [(1, 0)]
    for symbol, count in enumerate(counts):
        for _ in range(count):
            updated = []
            for j in range(min(len(coefficients), plus_count)+1):
                low = omega_power(coefficients[j], -symbol) if j < len(coefficients) else (0, 0)
                high = omega_power(coefficients[j-1], symbol) if j else (0, 0)
                updated.append((low[0]+high[0], low[1]+high[1]))
            coefficients = updated
    return coefficients[plus_count]


def rowspace_profiles(rows, *, cap=4096):
    """Bounded exact census, explicitly exponential in the number of rows."""
    rows = tuple(tuple(row) for row in rows)
    if (not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows)
            or any(type(x) is not int or x not in (0, 1, 2) for row in rows for x in row)):
        raise ValueError("canonical nonempty ternary matrix required")
    k, m = len(rows), len(rows[0])
    if type(cap) is not int or cap < 1 or 3**k > cap:
        raise ValueError("exact rowspace census exceeds verification cap")
    if nmod_mat(rows, 3).rank() != k:
        raise ValueError("independent rows required")
    profiles = Counter()
    distance, constant_in_rowspace = m, False
    for coefficients in product(range(3), repeat=k):
        word = tuple(sum(c*row[j] for c, row in zip(coefficients, rows)) % 3 for j in range(m))
        profile = tuple(word.count(a) for a in range(3))
        profiles[profile] += 1
        if any(coefficients):
            distance = min(distance, m-max(profile))
            constant_in_rowspace |= max(profile) == m
    return {"profiles": profiles, "words_enumerated": 3**k,
            "distance_to_constants": distance, "constant_in_rowspace": constant_in_rowspace}


def counts_from_profiles(profiles, plus_count):
    """Character-orthogonality counts, given a complete rowspace profile."""
    lengths = {sum(counts) for counts in profiles}
    if (len(lengths) != 1 or any(type(v) is not int or v <= 0 for v in profiles.values())):
        raise ValueError("positive multiplicities of equal-length profiles required")
    m = lengths.pop()
    if type(plus_count) is not int or not 0 <= plus_count <= m:
        raise ValueError("valid plus count required")
    total, real, imaginary = 0, 0, 0
    for counts, multiplicity in profiles.items():
        a, b = type_character(counts, plus_count)
        real += multiplicity*a
        imaginary += multiplicity*b
        total += multiplicity*(-1)**(m-counts[0])*2**counts[0]
    size = sum(profiles.values())
    if imaginary or total % size or real % size or not 0 <= real <= total:
        raise ValueError("profile fails exact code-count consistency checks")
    return {"full_support": total//size, "fixed_type": real//size}


def sqrt_upper(value, bits=256):
    """Outward rational bound, including perfect squares and zero."""
    value = Fraction(value)
    if value < 0 or type(bits) is not int or bits < 1:
        raise ValueError("nonnegative rational and positive precision required")
    scale = 1 << bits
    ceiling = -(-(value.numerator*scale*scale)//value.denominator)
    root = isqrt(ceiling)
    if root*root < ceiling:
        root += 1
    return Fraction(root, scale)


def transfer_budget(m, k, square_dimension, distance_to_constants, *, security_bits=40,
                    circuit_tv_budget=Fraction(1, 2**64)):
    """Conditional theorem ledger, NOT a distance-certificate verifier.

    D has dimension k, excludes constants, and every nonzero d in D has
    distance >=distance_to_constants from EACH constant word. The caller
    must prove that premise for the actual matrix. The native calibration
    below has an explicit algebraic proof; arbitrary numbers do not admit
    a candidate. The decoder bound is the published loose two-fold bound.
    """
    integers = (m, k, square_dimension, distance_to_constants, security_bits)
    if (any(type(x) is not int for x in integers) or m < 2 or m % 2
            or not 1 <= k < m or not 1 <= square_dimension <= min(m, k*(k+1)//2)
            or not 1 <= distance_to_constants <= 2*m//3 or security_bits < 1):
        raise ValueError("valid even length, dimensions, distance and confidence required")
    circuit_tv_budget = Fraction(circuit_tv_budget)
    if not 0 <= circuit_tv_budget <= 1:
        raise ValueError("circuit TV budget must lie in [0,1]")
    size, d = 3**k, distance_to_constants
    pairs = min(m//2, d)
    mass = Fraction(comb(m, m//2), 2**m)
    full_error = Fraction(size-1, 2**d)
    type_error = (size-1)*Fraction(3, 4)**pairs
    ideal_acceptance_lower = max(Fraction(0), (mass-type_error)/(1+full_error))
    decoder_error = min(Fraction(1), Fraction(3**(k+square_dimension), 2**d))
    # Coherent erasure errors may add over ALL 3**k codewords.
    erasure_tv = min(Fraction(1), 4*sqrt_upper(size*decoder_error))
    output_tv = min(Fraction(1), erasure_tv+circuit_tv_budget)
    acceptance_lower = max(Fraction(0), ideal_acceptance_lower-output_tv)
    cap = None
    if acceptance_lower:
        quotient = Fraction(security_bits, 1)/acceptance_lower
        cap = -(-quotient.numerator//quotient.denominator)
    return {
        "length": m, "quotient_dimension": k, "square_dimension": square_dimension,
        "distance_to_constants_premise": d, "unequal_symbol_pairs": pairs,
        "unconstrained_balanced_mass": exact(mass),
        "full_support_count_relative_error_upper": exact(full_error),
        "type_count_absolute_error_upper": exact(type_error),
        "ideal_acceptance_lower": exact(ideal_acceptance_lower),
        "base_decoder_failure_upper": exact(decoder_error),
        "coherent_dimension_factor": size,
        "coherent_erasure_tv_upper": exact(erasure_tv),
        "circuit_tv_budget": exact(circuit_tv_budget),
        "unconditional_output_tv_upper": exact(output_tv),
        "verified_acceptance_lower": exact(acceptance_lower),
        "bounded_base_sampler_calls": cap, "failure_probability_upper": exact(Fraction(1, 2**security_bits)),
        "cap_failure_bound_applicable": cap is not None,
        "gates_per_base_call": "Two coherent decoder calls plus polynomial preparation, Fourier, arithmetic and precision costs.",
        "circuit_budget_is_a_compilation_requirement_not_a_measured_error": True,
        "arbitrary_parameter_input_certifies_a_code": False,
        "native_quantum_circuit_executed": False,
    }


def simplex_calibration(variables=6):
    """Explicit, classically easy, growing family; no quantum-advantage evidence.

    D evaluates linear forms at every nonzero point of F3**v. D+<1>
    has distance 2*3**(v-1)-1, and D has square dimension v*(v+1)//2.
    All nonzero D words have the SAME profile, so no rowspace enumeration
    or hidden minimum-distance oracle is needed for this calibration.
    """
    if type(variables) is not int or not 2 <= variables <= 6:
        raise ValueError("bounded explicit calibration needs 2<=variables<=6")
    start = time.perf_counter()
    points = tuple(p for p in product(range(3), repeat=variables) if any(p))
    rows = tuple(tuple(p[i] for p in points) for i in range(variables))
    m, level = len(points), 3**(variables-1)
    square_rows = [tuple(a*b % 3 for a, b in zip(rows[i], rows[j]))
                   for i in range(variables) for j in range(i, variables)]
    square_rank = nmod_mat(square_rows, 3).rank()
    if square_rank != variables*(variables+1)//2 or nmod_mat(rows, 3).rank() != variables:
        raise ArithmeticError("explicit matrix does not match the algebraic dimensions")
    profiles = {(m, 0, 0): 1, (level-1, level, level): 3**variables-1}
    counts = counts_from_profiles(profiles, m//2)
    budget = transfer_budget(m, variables, square_rank, 2*level-1)
    actual = Fraction(counts["fixed_type"], counts["full_support"])
    lower = Fraction(budget["ideal_acceptance_lower"]["numerator"],
                     budget["ideal_acceptance_lower"]["denominator"])
    if not 0 <= lower <= actual:
        raise ArithmeticError("exact counting contradicts the transfer bound")
    return {
        "variables": variables, "full_constraint_matrix": ((1,)*m, *rows),
        "quotient_rows": rows, "square_dimension_checked": square_rank,
        "distance_to_constants": 2*level-1,
        "distance_certificate": "Every nonzero linear form takes each value 3^(v-1) times on F3^v; remove the zero point.",
        "exact_counts": counts, "exact_ideal_balanced_acceptance": exact(actual),
        "budget": budget, "elapsed_seconds": time.perf_counter()-start,
        "quantum_circuit_executed": False, "advantage_evidence": False,
        "classical_baseline": "Exact dynamic programming over 3^v=m+1 syndromes samples the same constrained law in polynomial time.",
    }


def finite_erasure_control(*, decoder="pgm"):
    """Execute a fixed 3-label/16-basis-state identity control, not a solver.

    The dense PGM is only a test instrument. It is not the published
    polynomial Schur-square decoder and cannot stand in for one at scale.
    Working in the Fourier-conjugated +/- basis incorporates the known
    local Fourier transforms into the receiver.
    """
    import numpy as np

    if decoder not in ("pgm", "zero"):
        raise ValueError("explicit test decoder required")
    row, size = (1, 1, 2, 2), 3
    words = tuple(product((-1, 1), repeat=len(row)))
    omega = np.exp(2j*np.pi/3)
    signals = np.asarray([[omega**((c*sum(a*y for a, y in zip(row, word))) % 3)
                           for c in range(size)] for word in words])/4
    gram = signals.conj().T @ signals
    values, vectors = np.linalg.eigh(gram)
    receiver = signals @ vectors @ np.diag(values**-0.5) @ vectors.conj().T
    # QR completes the orthonormal receiver columns; column phases do not
    # change this measurement. All work dimensions are explicitly present.
    unitary, _ = np.linalg.qr(receiver, mode="complete")
    decoded = tuple(j if j < size and decoder == "pgm" else 0 for j in range(len(words)))
    observed = unitary.conj().T @ signals
    error = sum(abs(observed[j, c])**2 for j in range(len(words))
                for c in range(size) if decoded[j] != c)/size
    erased = np.zeros_like(observed)
    for j in range(len(words)):
        for c in range(size):
            erased[j, (c-decoded[j]) % size] += observed[j, c]/np.sqrt(size)
    actual = unitary @ erased
    ideal = np.zeros_like(actual)
    ideal[:, 0] = signals.sum(axis=1)/np.sqrt(size)
    valid = np.asarray([sum(a*y for a, y in zip(row, word)) % 3 == 0 for word in words])
    balanced = valid & np.asarray([sum(word) == 0 for word in words])
    reference = valid/valid.sum()
    probabilities = np.sum(abs(actual)**2, axis=1)
    tv = float(np.sum(abs(probabilities-reference))/2)
    norm_error = float(np.linalg.norm(actual-ideal))
    tv_bound = min(1.0, 4*float(np.sqrt(size*error)))
    if (abs(float(probabilities.sum())-1) > 1e-12
            or norm_error > 2*np.sqrt(size*error)+1e-12 or tv > tv_bound+1e-12):
        raise ArithmeticError("executed coherent transfer violates the written bound")
    return {
        "public_row": row, "words": words, "decoder": decoder,
        "average_decoder_error": float(error),
        "all_failure_branches_retained": True,
        "actual_output_probabilities": probabilities.tolist(),
        "actual_output_tv_to_uniform_solutions": tv, "tv_upper": tv_bound,
        "unnormalized_ideal_norm_squared": float(np.linalg.norm(ideal)**2),
        "actual_to_unnormalized_ideal_norm": norm_error,
        "ideal_balanced_probability": float(reference[balanced].sum()),
        "actual_verified_balanced_probability": float(probabilities[balanced].sum()),
        "dense_receiver_is_only_an_identity_control": True,
        "scalable_decoder_implemented": False,
    }


def report():
    return {
        "status": "CONSTRUCTIVE_TYPE_TRANSFER_REVIEW_PENDING_NO_ADVANTAGE",
        "question": "Does a central balanced ternary histogram require an entangled quantum decoder?",
        "answer": "Not under the explicit distance and uniform-output error margins: quotient the constant direction, then use charged rejection.",
        "published_product_decoder": "https://arxiv.org/html/2610.00502v1#S5",
        "global_constraint_question": "https://arxiv.org/html/2610.00502v1#S1.SS4",
        "calibration": simplex_calibration(),
        "finite_coherent_erasure": finite_erasure_control(),
        "broken_decoder_control": finite_erasure_control(decoder="zero"),
        "remaining_blockers": [
            "Independent review of the written coherent-erasure and type-count argument.",
            "General or exponentially rare constraints are not covered by this balanced-type transfer.",
            "No classically hard concrete family or new speedup is established.",
            "The published coherent product decoder is not implemented at native scale here.",
        ],
        "candidate_accepted": False, "formalized_in_lean": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    data = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    native = data["calibration"]
    p = native["exact_ideal_balanced_acceptance"]
    print(json.dumps({"output": str(args.output), "length": len(native["quotient_rows"][0]),
                      "ideal_acceptance": p["numerator"]/p["denominator"],
                      "base_sampler_cap": native["budget"]["bounded_base_sampler_calls"],
                      "quantum_executed": False, "advantage_evidence": False}, indent=2))


if __name__ == "__main__":
    main()
