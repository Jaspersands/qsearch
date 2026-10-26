"""Biased ternary phase decoding and a charged prescribed-type transfer.

Written derivation pending independent review. Local isometries and bounded
coherent controls execute; the growing quantum sampler is a resource argument,
not an executed circuit or a speedup. The calibration is classically easy.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path

import numpy as np
from flint import nmod_mat

from theorems.ternary_quotient_decoder import Span
from theorems.ternary_type_transfer import (
    counts_from_profiles, exact, omega_power, sqrt_upper,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/ternary_tilted_type.json"


def tilt(value):
    p = Fraction(value)
    if not 0 < p < 1:
        raise ValueError("interior rational tilt required; endpoints are deterministic")
    return p


def local_receiver(p):
    """4-by-2 isometry: exclusions 0,1,2 and an erasure, no postselection."""
    p = float(tilt(p))
    rho = 2*min(p, 1-p)
    omega = np.exp(2j*np.pi/3)
    rows = [[np.sqrt(rho/(6*p))*omega**(-a),
             -np.sqrt(rho/(6*(1-p)))*omega**a] for a in range(3)]
    rows.append([np.sqrt(max(0.0, 1-rho/(2*p))),
                 np.sqrt(max(0.0, 1-rho/(2*(1-p))))])
    return np.asarray(rows, dtype=complex)


def receiver_unitary(p):
    """Complete the explicit isometry, preserving its first two columns."""
    receiver = local_receiver(p)
    _, _, vh = np.linalg.svd(receiver.conj().T, full_matrices=True)
    return np.column_stack((receiver, vh.conj().T[:, 2:]))


def validated_rows(rows):
    rows = tuple(tuple(row) for row in rows)
    if (not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows)
            or any(type(x) is not int or x not in (0, 1, 2) for row in rows for x in row)
            or nmod_mat(rows, 3).rank() != len(rows)):
        raise ValueError("independent canonical nonempty F3 rows required")
    return rows


def square_basis(rows):
    rows = validated_rows(rows)
    span = Span(len(rows[0]))
    for j, left in enumerate(rows):
        for right in rows[j:]:
            span.add(tuple(a*b % 3 for a, b in zip(left, right)))
    return tuple(tuple(int(x) for x in row) for row in span.rows.values())


def projected_solution(equations, rhs, *, variables, projected):
    """Gaussian elimination certifying only the first projected coordinates."""
    equations, rhs = tuple(tuple(row) for row in equations), tuple(rhs)
    if (type(variables) is not int or type(projected) is not int
            or not 1 <= projected <= variables or len(equations) != len(rhs)
            or any(len(row) != variables for row in equations)
            or any(type(x) is not int or x not in (0, 1, 2)
                   for row in equations for x in row)
            or any(type(x) is not int or x not in (0, 1, 2) for x in rhs)):
        raise ValueError("canonical F3 linear system and valid projection required")
    matrix = np.asarray([(*row, b) for row, b in zip(equations, rhs)],
                        dtype=np.int64).reshape((-1, variables+1))
    pivots = []
    for column in range(variables):
        start = len(pivots)
        choices = np.flatnonzero(matrix[start:, column])
        if not len(choices):
            continue
        pivot = start+int(choices[0])
        matrix[[start, pivot]] = matrix[[pivot, start]]
        matrix[start] = matrix[start]*int(matrix[start, column]) % 3
        for j in range(len(matrix)):
            if j != start and matrix[j, column]:
                matrix[j] = (matrix[j]-matrix[j, column]*matrix[start]) % 3
        pivots.append(column)
    inconsistent = any(not np.any(row[:-1]) and row[-1] for row in matrix)
    free = tuple(i for i in range(variables) if i not in pivots)
    unique = not inconsistent and all(
        j in pivots and not any(matrix[pivots.index(j), f] for f in free)
        for j in range(projected))
    value = None
    if unique:
        value = tuple(int(matrix[pivots.index(j), -1]) for j in range(projected))
    return {"consistent": not inconsistent, "projection_unique": unique,
            "value": value, "rank": len(pivots), "free_variables": len(free)}


def relinearize(rows, outcomes):
    """Outcome a excludes a; outcome 3 is an erasure, not a new sample.

    Unknowns are v in D and w in D*D. Unique v suffices even if w is free.
    No codeword or auxiliary-vector enumeration occurs in this decoder.
    """
    rows = validated_rows(rows)
    outcomes = tuple(outcomes)
    if (len(outcomes) != len(rows[0])
            or any(type(x) is not int or x not in (0, 1, 2, 3) for x in outcomes)):
        raise ValueError("one exclusion or erasure per coordinate required")
    square = square_basis(rows)
    equations, rhs = [], []
    for i, excluded in enumerate(outcomes):
        if excluded == 3:
            continue
        a, b = (x for x in range(3) if x != excluded)
        equations.append(tuple(-(a+b)*row[i] % 3 for row in rows)
                         + tuple(row[i] for row in square))
        rhs.append(-a*b % 3)
    result = projected_solution(equations, rhs, variables=len(rows)+len(square),
                                projected=len(rows))
    return {**result, "square_dimension": len(square),
            "conclusive_coordinates": len(equations)}


def weighted_kernel_mass(profiles, p):
    """Exact character sum given complete code profiles, not a counting oracle."""
    p = tilt(p)
    if (not profiles or any(len(c) != 3 or any(type(x) is not int or x < 0 for x in c)
                            for c in profiles)
            or len({sum(c) for c in profiles}) != 1
            or any(type(x) is not int or x < 1 for x in profiles.values())):
        raise ValueError("equal-length profiles with positive multiplicities required")
    real, imaginary = Fraction(0), Fraction(0)
    for counts, multiplicity in profiles.items():
        value = (Fraction(1), Fraction(0))
        for a, count in enumerate(counts):
            for _ in range(count):
                low, high = omega_power(value, -a), omega_power(value, a)
                value = tuple((1-p)*x+p*y for x, y in zip(low, high))
        real += multiplicity*value[0]
        imaginary += multiplicity*value[1]
    if imaginary or not 0 <= real <= sum(profiles.values()):
        raise ValueError("profiles fail real probability consistency")
    return real/sum(profiles.values())


def tilted_budget(m, k, square_dimension, distance_to_constants, plus_count, *,
                  security_bits=40, circuit_tv_budget=Fraction(1, 2**64)):
    """Conditional theorem ledger; numerical inputs do NOT certify a code."""
    ints = (m, k, square_dimension, distance_to_constants, plus_count, security_bits)
    if (any(type(x) is not int for x in ints) or m < 2
            or not 1 <= k < m or not 1 <= square_dimension <= min(m, k*(k+1)//2)
            or not 1 <= distance_to_constants <= 2*m//3
            or not 0 < plus_count < m or security_bits < 1):
        raise ValueError("valid dimensions, distance, interior type and confidence required")
    circuit_tv_budget = Fraction(circuit_tv_budget)
    if not 0 <= circuit_tv_budget <= 1:
        raise ValueError("circuit TV budget must lie in [0,1]")
    p, size = Fraction(plus_count, m), 3**k
    q, d = min(p, 1-p), distance_to_constants
    pairs = min(m//2, d)
    beta = sqrt_upper(1-3*p*(1-p))
    full_error = (size-1)*beta**d
    type_error = (size-1)*(1-p*(1-p))**pairs
    mass = comb(m, plus_count)*p**plus_count*(1-p)**(m-plus_count)
    ideal = max(Fraction(0), (mass-type_error)/(1+full_error))
    delta = min(Fraction(1), size*3**square_dimension*(1-q)**d)
    erasure_tv = min(Fraction(1), 4*sqrt_upper(size*delta))
    eta = min(Fraction(1), erasure_tv+circuit_tv_budget)
    acceptance = max(Fraction(0), ideal-eta)
    scale = 2**192
    acceptance = Fraction((acceptance.numerator*scale)//acceptance.denominator, scale)
    calls = None
    if acceptance:
        quotient = security_bits/acceptance
        calls = -(-quotient.numerator//quotient.denominator)
    # Outward rounding keeps certificates compact without weakening bounds.
    def upper(x):
        return exact(Fraction(-(-(x.numerator*scale)//x.denominator), scale))

    def lower(x):
        return exact(Fraction((x.numerator*scale)//x.denominator, scale))

    return {
        "length": m, "dimension": k, "square_dimension": square_dimension,
        "distance_to_constants_premise": d, "plus_count": plus_count,
        "constant_row_rhs": (2*plus_count-m) % 3, "tilt": exact(p),
        "local_conclusive_probability": exact(2*q),
        "unconstrained_type_mass": lower(mass),
        "full_kernel_relative_error_upper": upper(full_error),
        "type_absolute_error_upper": upper(type_error),
        "ideal_acceptance_lower": lower(ideal),
        "decoder_failure_upper": upper(delta),
        "coherent_dimension_factor": size,
        "coherent_erasure_tv_upper": upper(erasure_tv),
        "circuit_tv_budget": exact(circuit_tv_budget),
        "output_tv_upper": upper(eta),
        "verified_acceptance_lower": lower(acceptance),
        "accepted_output_tv_to_uniform_type_upper": upper(
            min(Fraction(1), 2*eta/acceptance) if acceptance else Fraction(1)),
        "base_sampler_call_cap": calls,
        "cap_failure_bound_applicable": calls is not None,
        "failure_probability_upper": exact(Fraction(1, 2**security_bits)),
        "arbitrary_parameter_input_certifies_a_code": False,
        "native_quantum_circuit_executed": False,
    }


def finite_coherent_control(p=Fraction(1, 3), *, decoder="relinearize"):
    """Actual four-coordinate erasure circuit; all work/failure outcomes kept."""
    if decoder not in ("relinearize", "zero"):
        raise ValueError("explicit control decoder required")
    p = tilt(p)
    row = (1, 1, 2, 2)
    m, size = len(row), 3
    outcomes = tuple(product(range(4), repeat=m))
    receiver = receiver_unitary(p)
    full = receiver
    for _ in range(m-1):
        full = np.kron(full, receiver)
    omega = np.exp(2j*np.pi/3)
    signals = np.zeros((4**m, size), dtype=complex)
    for c in range(size):
        state = np.array([1.0+0j])
        for a in row:
            state = np.kron(state, [np.sqrt(float(p))*omega**(c*a % 3),
                                   np.sqrt(float(1-p))*omega**(-c*a % 3), 0, 0])
        signals[:, c] = state
    certificates = [relinearize((row,), outcome) for outcome in outcomes]
    decoded = [r["value"][0] if r["projection_unique"] and decoder == "relinearize"
               else 0 for r in certificates]
    observed = full @ signals
    error = sum(abs(observed[j, c])**2 for j in range(4**m)
                for c in range(size) if decoded[j] != c)/size
    erased = np.zeros_like(observed)
    for j in range(4**m):
        for c in range(size):
            erased[j, (c-decoded[j]) % size] += observed[j, c]/np.sqrt(size)
    actual = full.conj().T @ erased
    ideal = np.zeros_like(actual)
    ideal[:, 0] = signals.sum(axis=1)/np.sqrt(size)
    probabilities = np.zeros(2**m)
    for digits, value in zip(outcomes, np.sum(abs(actual)**2, axis=1)):
        word_index = sum((a % 2)*2**(m-1-i) for i, a in enumerate(digits))
        probabilities[word_index] += value
    words = tuple(product((1, -1), repeat=m))
    weights = np.asarray([float(p**word.count(1)*(1-p)**word.count(-1))
                          if sum(a*y for a, y in zip(row, word)) % 3 == 0 else 0
                          for word in words])
    reference = weights/weights.sum()
    tv = float(np.abs(probabilities-reference).sum()/2)
    norm_error = float(np.linalg.norm(actual-ideal))
    if (abs(float(probabilities.sum())-1) > 2e-12
            or norm_error > 2*np.sqrt(size*error)+2e-12
            or tv > min(1, 4*np.sqrt(size*error))+2e-12):
        raise ArithmeticError("actual coherent control contradicts transfer inequality")
    return {
        "row": row, "tilt": exact(p), "decoder": decoder,
        "codewords": size, "physical_dimension_including_work": 4**m,
        "average_decoder_error": float(error),
        "actual_to_unnormalized_ideal_norm": norm_error,
        "unnormalized_ideal_norm_squared": float(np.linalg.norm(ideal)**2),
        "actual_tv_to_weighted_kernel": tv,
        "actual_output_probabilities": probabilities.tolist(),
        "reference_probabilities": reference.tolist(),
        "all_failure_and_workspace_branches_retained": True,
        "test_only_dense_completion_not_a_native_hardware_compiler": True,
    }


def simplex_calibration(variables=6):
    """Explicit growing but classically easy code, with a rare UNIFORM type."""
    if type(variables) is not int or not 2 <= variables <= 6:
        raise ValueError("bounded native calibration needs 2<=variables<=6")
    points = tuple(p for p in product(range(3), repeat=variables) if any(p))
    rows = tuple(tuple(p[i] for p in points) for i in range(variables))
    m, h = len(points), 3**(variables-1)
    square = square_basis(rows)
    if len(square) != variables*(variables+1)//2:
        raise ArithmeticError("unexpected simplex square dimension")
    profiles = {(m, 0, 0): 1, (h-1, h, h): 3**variables-1}
    counts = counts_from_profiles(profiles, h)
    p = Fraction(h, m)
    kernel = weighted_kernel_mass(profiles, p)
    closed_kernel = (1+(3**variables-1)*(1-3*p*(1-p))**h)/3**variables
    if kernel != closed_kernel:
        raise ArithmeticError("independent character expressions disagree")
    weighted_mass = counts["fixed_type"]*p**h*(1-p)**(m-h)/kernel
    budget = tilted_budget(m, variables, len(square), 2*h-1, h)
    lower = budget["ideal_acceptance_lower"]
    if not Fraction(lower["numerator"], lower["denominator"]) <= weighted_mass:
        raise ArithmeticError("exact counting contradicts tilted lower bound")
    return {
        "variables": variables, "quotient_rows": rows, "plus_count": h,
        "constant_constraint_rhs": (2*h-m) % 3,
        "homogeneous_constant_row_would_be_incompatible": (2*h-m) % 3 != 0,
        "exact_counts": counts, "square_dimension_checked": len(square),
        "uniform_acceptance": exact(Fraction(counts["fixed_type"], counts["full_support"])),
        "tilted_acceptance": exact(weighted_mass), "budget": budget,
        "distance_certificate": "Nonzero linear forms have counts (3^(v-1)-1,3^(v-1),3^(v-1)); distance to every constant is >=2*3^(v-1)-1.",
        "classical_syndrome_states": 3**variables,
        "classical_baseline": "Exact syndrome-and-count dynamic programming samples the same fixed-type law in polynomial time here: 3^v=m+1.",
        "native_quantum_circuit_executed": False, "advantage_evidence": False,
    }


def report():
    return {
        "status": "CONDITIONAL_TILTED_TRANSFER_WRITTEN_REVIEW_PENDING",
        "source": "https://arxiv.org/html/2610.00502v1",
        "mechanism": "Local bias-flattening with retained erasures, projected Schur-square decoding, coherent erasure, verified type rejection.",
        "calibration": simplex_calibration(),
        "coherent_controls": [finite_coherent_control(),
                              finite_coherent_control(decoder="zero")],
        "claim_gate": {
            "independent_proof_review_complete": False,
            "native_quantum_circuit_executed": False,
            "novelty_established": False, "speedup_claim_allowed": False,
            "classical_hardness_established": False,
            "general_global_constraints_solved": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    calibration = result["calibration"]
    print(json.dumps({"status": result["status"],
                      "uniform_type_probability": float(Fraction(
                          calibration["uniform_acceptance"]["numerator"],
                          calibration["uniform_acceptance"]["denominator"])),
                      "tilted_type_probability": float(Fraction(
                          calibration["tilted_acceptance"]["numerator"],
                          calibration["tilted_acceptance"]["denominator"])),
                      "charged_sampler_cap": calibration["budget"]["base_sampler_call_cap"],
                      "advantage_evidence": False}, indent=2))


if __name__ == "__main__":
    main()
