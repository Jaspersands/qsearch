"""Exact torus sum-of-squares search for the actual two-layer self loops.

Numerical linear programming selects a support only. Accepted certificates
have exact rational coefficients and a complete Laurent-polynomial identity.
No sampled angle, floating PSD test or candidate speedup is accepted.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations_with_replacement, product
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from sympy import Matrix

from ternary_two_layer_path_transfer import (
    structural_certificate, _ceil_root, complete_graph, weighted_edges,
    add, multiply, QUARTER_PHASES, ZERO, ONE, _quarter,
)
from ternary_hot_phase_mixer import sqrt_rational_upper
from ternary_covariant_noise import root_digits
from ternary_native_block_walk import _integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_continuous_loop_certificate.json"
DERIVATION = ROOT / "research/TERNARY_CONTINUOUS_LOOP_CERTIFICATE.md"
PARENT = ROOT / "research/phase_workbench/ternary_two_layer_path_transfer.json"
NODES = tuple((i, j) for i in range(3) for j in range(3))
HALF = tuple((i, j) for i in range(3) for j in range(-2, 3)
             if i > 0 or j >= 0)


def square_polynomial(coefficients):
    out = defaultdict(Fraction)
    for (i, j), a in coefficients.items():
        for (k, l), b in coefficients.items():
            out[i-k, j-l] += Fraction(a)*Fraction(b)
    return {e: a for e, a in out.items() if a}


def defect_polynomial(coefficients):
    out = {e: -a for e, a in square_polynomial(coefficients).items()}
    out[0, 0] = out.get((0, 0), Fraction()) + 81**2
    return {e: a for e, a in out.items() if a}


@lru_cache(maxsize=2)
def square_pool(terms=2):
    # The actual loops saturate at z=w=1, so each positive square must vanish
    # there. Small zero-sum integer polynomials supply a finite certificate cone.
    vectors = set()
    pairs = tuple(combinations_with_replacement(range(9), terms))
    for a, b in combinations_with_replacement(pairs, 2):
        v = [0]*9
        for i in a:
            v[i] += 1
        for i in b:
            v[i] -= 1
        if any(v):
            from math import gcd
            d = 0
            for x in v:
                d = gcd(d, x)
            v = tuple(x//d for x in v)
            if next(x for x in v if x) < 0:
                v = tuple(-x for x in v)
            vectors.add(v)
    vectors = tuple(sorted(vectors))
    columns = tuple(square_polynomial(dict(zip(NODES, v))) for v in vectors)
    return vectors, columns


def discover_certificate(coefficients, terms=2):
    coefficients = {e: Fraction(a) for e, a in coefficients.items()}
    target = defect_polynomial(coefficients)
    if not target:
        return {"status": "EXACT_TORUS_SOS", "squares": []}
    vectors, columns = square_pool(terms)
    A = np.array([[float(c.get(e, 0)) for c in columns] for e in HALF])
    b = np.array([float(target.get(e, 0)) for e in HALF])
    result = linprog(np.ones(len(columns)), A_eq=A, b_eq=b,
                     bounds=(0, None), method="highs")
    if not result.success:
        if terms == 2:
            return discover_certificate(coefficients, 3)
        return {"status": "CERTIFICATE_SEARCH_UNKNOWN",
                "reason": "finite integer-square cone did not supply a certificate"}
    support = [i for i, value in enumerate(result.x) if value > 1e-7]
    exact_A = Matrix([[columns[i].get(e, 0) for i in support] for e in HALF])
    exact_b = Matrix([target.get(e, 0) for e in HALF])
    try:
        weights, parameters = exact_A.gauss_jordan_solve(exact_b)
    except ValueError:
        return {"status": "CERTIFICATE_SEARCH_UNKNOWN",
                "reason": "numerical support did not have an exact solution"}
    if parameters.rows or any(w < 0 for w in weights):
        return {"status": "CERTIFICATE_SEARCH_UNKNOWN",
                "reason": "support lacks a unique nonnegative rational solution"}
    squares = [{"weight": str(Fraction(w)), "integer_coefficients": list(vectors[i])}
               for i, w in zip(support, weights) if w]
    certificate = {"status": "EXACT_TORUS_SOS", "squares": squares}
    verify_certificate(coefficients, certificate)
    return certificate


def verify_certificate(coefficients, certificate):
    if certificate.get("status") != "EXACT_TORUS_SOS":
        raise ValueError("unknown is not a unit-modulus certificate")
    actual = defaultdict(Fraction)
    for square in certificate["squares"]:
        weight = Fraction(square["weight"])
        vector = square["integer_coefficients"]
        if (weight <= 0 or len(vector) != 9 or any(type(v) is not int for v in vector)
                or not any(vector)):
            raise ValueError("positive rational weight and complete integer polynomial required")
        if sum(vector) != 0:
            raise ValueError("square must vanish at the saturated zero-angle point")
        for e, a in square_polynomial(dict(zip(NODES, vector))).items():
            actual[e] += weight*a
    actual = {e: a for e, a in actual.items() if a}
    if actual != defect_polynomial(coefficients):
        raise ValueError("complete exact Laurent defect identity fails")
    return True


def sharpened_envelope(n, q, inputs):
    _integer(n, "native dimension"); root_digits(q); _integer(inputs, "native input count")
    G, D = q**n, 3**inputs
    fixed = min(Fraction(1), sum(Fraction(math.comb(inputs, j))*18**j
                                for j in range(min(5, inputs)+1))/G)
    inverse = (fixed.denominator+fixed.numerator-1)//fixed.numerator
    m = _ceil_root(inverse, 5)
    rounding = Fraction(88*(n+inputs), 7*m)
    tuned = min(Fraction(1), fixed*m**4+rounding)
    born = lambda s: min(Fraction(1), s+sqrt_rational_upper(Fraction(G-1, D)*s))
    return {"dimension": n, "modulus": str(q), "original_native_inputs": inputs,
            "requires_all_137_exact_loop_certificates_and_parent_transfer_premises": True,
            "continuous_loop_growth_upper": "1", "strict_path_depth": 5,
            "off_diagonal_weight_row_norm_upper": "18",
            "all_fixed_continuous_angles_uniform_success_upper": str(fixed),
            "all_fixed_continuous_angles_Born_success_upper": str(born(fixed)),
            "implicit_four_angle_net_axis_points": str(m),
            "implicit_four_angle_net_total_points": str(m**4),
            "implicit_net_rounding_probability_error_upper": str(rounding),
            "public_adaptive_four_angle_uniform_success_upper": str(tuned),
            "public_adaptive_four_angle_Born_success_upper": str(born(tuned)),
            "fixed_coordinate_dependent_mixer_angles_covered": True,
            "arbitrary_fixed_residual_phase_functions_covered": True,
            "label_trained_coordinate_angles_or_residual_functions_not_covered": True,
            "adaptive_four_angle_bound_requires_original_mismatch_cost_template": True,
            "Born_decay_depends_on_original_input_count": True,
            "other_mixer_shapes_deeper_circuits_and_other_receivers_not_covered": True}


def fixed_function_control(n, q, beta1, beta2, phase1, phase2):
    """Capped complete native census versus the arbitrary-residual path law.

    All phases are quarter turns for exact arithmetic. The upper-bound
    theorem is continuous; this census is only a bounded regression control.
    """
    _integer(n, "native dimension"); root_digits(q)
    M, G = len(beta1), q**n
    if M < 1 or len(beta2) != M:
        raise ValueError("two nonempty coordinate mixer schedules required")
    for b in (*beta1, *beta2, *phase1, *phase2):
        _quarter(b)
    if len(phase1) != G or len(phase2) != G:
        raise ValueError("two complete full-root residual phase tables required")
    if q**(2*M*n) > 10000 or 3**M > 27 or q**(4*n) > 10000:
        raise ValueError("complete bounded census cap; never return a partial mean")
    words = tuple(product(range(3), repeat=M))
    targets = tuple(product(range(q), repeat=n))
    index = {w: i for i, w in enumerate(words)}
    def code(v):
        return sum(a*q**(n-j-1) for j, a in enumerate(v))
    total_probability = Fraction()
    born_probability = Fraction()
    for rows in product(range(q), repeat=2*M*n):
        F = [tuple(sum(rows[(2*i+t-1)*n+j] for i, t in enumerate(w) if t)
                   % q for j in range(n)) for w in words]
        for target in targets:
            residuals = [code(tuple((a-b) % q for a, b in zip(f, target))) for f in F]
            state = [ONE]*len(words)
            for schedule, phases in ((beta1, phase1), (beta2, phase2)):
                state = [multiply(a, QUARTER_PHASES[phases[d]]) for a, d in zip(state, residuals)]
                for axis, beta in enumerate(schedule):
                    phase = _quarter(beta)
                    updated = []
                    for w in words:
                        amplitude = ZERO
                        for t in range(3):
                            v = w[:axis]+(t,)+w[axis+1:]
                            gate = ((1+2*phase[0], 2*phase[1]) if t == w[axis]
                                    else (1-phase[0], -phase[1]))
                            amplitude = add(amplitude, multiply(gate, state[index[v]]))
                        updated.append(amplitude)
                    state = updated
            marked = [i for i, f in enumerate(F) if f == target]
            raw = Fraction(sum(state[i][0]**2+state[i][1]**2 for i in marked),
                           len(words)*81**M)
            total_probability += raw/G
            born_probability += raw*Fraction(len(marked), len(words))
    labels = q**(2*M*n)
    actual, born = total_probability/labels, born_probability/labels

    states, _ = complete_graph()
    terminal = {0: ONE}
    for b1, b2 in zip(beta1, beta2):
        output = defaultdict(lambda: ZERO)
        for i, w in terminal.items():
            for j, v in weighted_edges(b1, b2)[i]:
                output[j] = add(output[j], multiply(w, v))
        terminal = {j: w for j, w in output.items() if w != ZERO}
    predicted = [Fraction(), Fraction()]
    for i, weight in terminal.items():
        basis = states[i]
        moment = ZERO
        for coefficients in product(range(q), repeat=len(basis)*n):
            residuals = [code(tuple(sum(basis[k][branch]*coefficients[j*len(basis)+k]
                                       for k in range(len(basis))) % q for j in range(n)))
                         for branch in range(4)]
            phase = (phase1[residuals[0]]+phase2[residuals[1]]
                     -phase1[residuals[2]]-phase2[residuals[3]]) % 4
            moment = add(moment, QUARTER_PHASES[phase])
        numerator = multiply(weight, moment)
        denominator = q**(len(basis)*n)*81**M*G
        predicted = [p+Fraction(a, denominator) for p, a in zip(predicted, numerator)]
    if predicted[1] or predicted[0] != actual:
        raise ArithmeticError("complete arbitrary-residual native law disagrees with circuit census")
    return {"dimension": n, "modulus": str(q), "original_native_inputs": M,
            "coordinate_beta1_quarters": list(beta1), "coordinate_beta2_quarters": list(beta2),
            "full_root_phase1_quarters": list(phase1), "full_root_phase2_quarters": list(phase2),
            "entire_IID_label_matrices": labels, "complete_uniform_target_cases": labels*G,
            "actual_direct_circuit_uniform_mean_exact": str(actual),
            "actual_direct_circuit_Born_mean_exact": str(born),
            "arbitrary_residual_lattice_transfer_mean_exact": str(predicted[0]),
            "fixed_before_labels_and_target": True,
            "capped_census_is_not_a_compiled_receiver": True}


def run_controls():
    rows, unique = [], {}
    for r in structural_certificate()["all_self_loop_Laurent_coefficients"]:
        coefficients = {(a["beta1_exponent"], a["beta2_exponent"]):
                        int(a["coefficient_numerator_over81"]) for a in r["Laurent_coefficients"]}
        key = tuple(sorted(coefficients.items()))
        if key not in unique:
            unique[key] = discover_certificate(coefficients)
        rows.append({"state": r["state"], "certificate": unique[key]})
    complete = all(r["certificate"]["status"] == "EXACT_TORUS_SOS" for r in rows)
    return {"status": "ALL_CONTINUOUS_LOOPS_CERTIFIED" if complete else "PARTIAL_CERTIFICATES_ONLY",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "parent_artifact_sha256": hashlib.sha256(PARENT.read_bytes()).hexdigest(),
            "polynomial_monomials": [list(e) for e in NODES],
            "complete_lattice_states": len(rows), "unique_loop_polynomials": len(unique),
            "finite_integer_square_pool": len(square_pool()[0]),
            "larger_fallback_integer_square_pool": len(square_pool(3)[0]),
            "all_continuous_self_loop_moduli_at_most_one": complete,
            "loop_certificates": rows,
            "sharpened_population_envelopes": [sharpened_envelope(*v) for v in
                ((8, 9, 24), (32, 81, 136), (128, 243, 648), (128, 243, 12800))]
                if complete else [],
            "complete_fixed_function_native_controls": [
                fixed_function_control(2, 3, (1,), (3,),
                    tuple((i*j+2*i+j) % 4 for i, j in product(range(3), repeat=2)),
                    tuple((i*j+i+2*j) % 4 for i, j in product(range(3), repeat=2))),
                fixed_function_control(1, 3, (1, 2), (3, 1), (0, 1, 3), (2, 3, 0)),
                fixed_function_control(1, 9, (1,), (3,),
                    tuple((i*i+i) % 4 for i in range(9)),
                    tuple((i*i+2*i+1) % 4 for i in range(9)))],
            "floating_optimizer_is_only_support_selection": True,
            "complete_exact_rational_identities_required": True,
            "general_mixer_or_deeper_circuit_lower_bound": False,
            "quantum_speedup_proved": False, "candidate_record_accepted": False,
            "novelty_claim": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
        print(json.dumps({"status": report["status"], "states": report["complete_lattice_states"],
                          "certified": sum(r["certificate"]["status"] == "EXACT_TORUS_SOS"
                                           for r in report["loop_certificates"])}))
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
