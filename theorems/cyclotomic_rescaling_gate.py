"""Native cyclotomic rescaling: legal Gaussian levels and ramification gate.

LOCAL DERIVATION / REVIEW PENDING. Explicit physical verification is p=3;
general-p power-subgroup classification is algebraic, not a new full decoder.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import fmpz_poly, nmod_mat
import numpy as np
from sympy import Matrix, isprime
from sympy.matrices.normalforms import hermite_normal_form

from dhsp_codomain_instrument import _integer, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/cyclotomic_rescaling_gate.json"
PHI = fmpz_poly([1, 1, 1])
ZETA = fmpz_poly([0, 1])
MPI = Matrix([[-1, -1], [1, -2]])


@lru_cache(maxsize=128)
def ideal_chart(level):
    _integer(level, "pi-adic level", 1)
    if level > 512:
        raise ValueError("exact arithmetic ledger capped at level512")
    H = hermite_normal_form(MPI**level)
    beta = Matrix([[2, -1]])*(MPI**(level-1)).inv()/3
    return tuple(map(int, (H[0, 0], H[0, 1], H[1, 1]))), tuple(Fraction(x.p, x.q) for x in beta)


def reduce_element(v, level):
    if len(v) != 2 or any(type(x) is not int for x in v):
        raise ValueError("two canonical integer power-basis coefficients required")
    h0, cross, h1 = ideal_chart(level)[0]
    a, b = v
    carry, b = divmod(b, h1)
    return ((a-carry*cross) % h0, b)


def multiply(u, v, level):
    p = (fmpz_poly(list(u))*fmpz_poly(list(v))) % PHI
    return reduce_element((int(p[0]), int(p[1])), level)


def plus(u, v, level):
    return reduce_element((u[0]+v[0], u[1]+v[1]), level)


def residue(v):
    return (v[0]+v[1]) % 3


def divide_pi(v, level):
    if level < 2 or residue(v):
        raise ValueError("actual pi divisibility and parent level>=2 required")
    w = MPI.inv()*Matrix(v)
    if any(x.q != 1 for x in w):
        raise ValueError("nonintegral pi quotient")
    return reduce_element(tuple(map(int, w)), level-1)


def rescale_label(v, a, level):
    if a not in (1, 2) or type(a) is not int:
        raise ValueError("nonzero canonical F3 input multiplier required")
    if a == 1:
        return reduce_element(v, level)
    # T_a(y)=(pi/sigma_(a^-1)(pi))^L sigma_(a^-1)(y).
    # For p3,a2: pi/bar(pi)=-zeta. FLINT supplies exact polynomial arithmetic.
    conjugate = (fmpz_poly([v[0]])+v[1]*(ZETA**2 % PHI)) % PHI
    p = ((-ZETA)**level*conjugate) % PHI
    return reduce_element((int(p[0]), int(p[1])), level)


def affine_label_transport(v, a, b, level):
    _integer(b, "canonical qutrit offset", 0)
    if b >= 3:
        raise ValueError("canonical qutrit offset must be below3")
    root = ZETA**b % PHI
    return rescale_label(multiply((int(root[0]), int(root[1])), v, level), a, level)


def pairing(secret, coefficient, level):
    v = multiply(secret, coefficient, level)
    beta = ideal_chart(level)[1]
    return (beta[0]*v[0]+beta[1]*v[1]) % 1


def _lambda(j, level):
    return reduce_element(((0, 0), (1, 0), (1, 1))[j], level)


def elements(level):
    if level > 4:
        raise ValueError("exhaustive ring enumeration capped at level4")
    h0, _, h1 = ideal_chart(level)[0]
    return [(a, b) for a in range(h0) for b in range(h1)]


def _phase(secret, label, j, level):
    total = sum((pairing(s, multiply(y, _lambda(j, level), level), level)
                 for s, y in zip(secret, label)), Fraction()) % 1
    return np.exp(2j*math.pi*float(total))


def gaussian_plan(labels, level):
    ideal_chart(level)
    if level < 2 or not labels or not labels[0] or any(len(v) != len(labels[0]) for v in labels):
        raise ValueError("parent level>=2 and rectangular ring-vector labels required")
    for row in labels:
        for y in row:
            reduce_element(y, level)
    n, m = len(labels[0]), len(labels)
    A = nmod_mat([[residue(labels[j][i]) for j in range(m)] for i in range(n)], 3)
    R, rank = A.rref()
    pivots = [next(j for j in range(m) if R[i, j]) for i in range(rank)]
    free = next((j for j in range(m) if j not in pivots), None)
    if free is None:
        raise ValueError("a nonzero public low-label dependence is required")
    weights = [0]*m
    weights[free] = 1
    for i, pivot in enumerate(pivots):
        weights[pivot] = -int(R[i, free]) % 3
    indices = [j for j, c in enumerate(weights) if c]
    roots = [next((a for a in (1, 2) if pow(a, level, 3) == weights[j]), None) for j in indices]
    if any(a is None for a in roots):
        raise ValueError("Gaussian coefficient outside native L-th-power residue subgroup; no weighted level drop")
    return {"low_label_rank": rank, "input_batch_size": m, "vector_dimension": n,
            "full_kernel_weights": weights, "selected_input_indices": indices,
            "qudit_input_multipliers": roots, "selected_native_qudits": len(indices),
            "unused_native_qudits": m-len(indices),
            "kernel_choice": "first free RREF column; not an exhaustive even-level admissible-kernel search",
            "selection_uses_current_higher_label_digits": False,
            "unknown_phase_preparation_or_inverse_used": False}


def physical_merge(labels, secret, level):
    plan = gaussian_plan(labels, level)
    if len(secret) != len(labels[0]) or any(len(s) != 2 or s[1] != 0 for s in secret):
        raise ValueError("integer-embedded secret is required for this same-secret Galois transformation")
    for s in secret:
        reduce_element(s, level)
    selected = [labels[j] for j in plan["selected_input_indices"]]
    roots = plan["qudit_input_multipliers"]
    r, n = len(selected), len(secret)
    if r > 5:
        raise ValueError("physical vector verification capped at five input qudits")
    transformed_labels = [[rescale_label(y, a, level) for y in row] for row, a in zip(selected, roots)]
    joint = np.empty((3,)*r, complex)
    for old in product(range(3), repeat=r):
        after_scaling = [(pow(a, -1, 3)*j) % 3 for a, j in zip(roots, old)]
        target = (after_scaling[0],)+tuple((j-after_scaling[0]) % 3 for j in after_scaling[1:])
        value = 3**(-r/2)
        for row, j in zip(selected, old):
            value *= _phase(secret, row, j, level)
        joint[target] = value
    branches = []
    for tail in product(range(3), repeat=r-1):
        x = (0,)+tail
        combined, offset = [(0, 0)]*n, [(0, 0)]*n
        for row, digit in zip(transformed_labels, x):
            root = ZETA**digit % PHI
            root = (int(root[0]), int(root[1]))
            for i, y in enumerate(row):
                combined[i] = plus(combined[i], multiply(root, y, level), level)
                offset[i] = plus(offset[i], multiply(_lambda(digit, level), y, level), level)
        child = [divide_pi(y, level) for y in combined]
        phase = sum((pairing(s, y, level) for s, y in zip(secret, offset)), Fraction()) % 1
        expected = np.array([3**(-r/2)*np.exp(2j*math.pi*float(phase))*_phase(secret, child, j, level-1) for j in range(3)])
        actual = joint[(slice(None),)+tail]
        error = float(max(abs(actual-expected)))
        assert error < 3e-12
        probability = float(sum(abs(actual)**2))
        assert abs(probability-3**(1-r)) < 3e-12
        branches.append({"difference_outcomes": list(tail), "child_label": child,
                         "branch_probability": probability,
                         "unnormalized_qudit_amplitudes": [[float(z.real), float(z.imag)] for z in actual],
                         "maximum_full_phase_identity_error": error})
    return {"parent_level": level, "prime": 3, "native_input_labels": labels,
            "integer_secret_calibration": secret, "plan": plan, "all_branches": branches,
            "full_output_norm": float(sum(abs(joint.ravel())**2)),
            "known_qudit_permutation_count": r, "known_SUM_difference_count": r-1,
            "postselection_or_cloning_used": False, "same_secret_scope_is_integer_embedding": True}


def level_classification(prime, level):
    _integer(prime, "fixed prime", 2)
    _integer(level, "pi-adic level", 1)
    if not isprime(prime) or prime > 101:
        raise ValueError("power-subgroup enumeration requires a prime<=101")
    powers = sorted({pow(a, level, prime) for a in range(1, prime)})
    return {"prime": prime, "level": level, "native_rescaling_residue_multipliers": powers,
            "power_subgroup_size": (prime-1)//math.gcd(level, prime-1),
            "arbitrary_nonzero_Gaussian_coefficients_available": math.gcd(level, prime-1) == 1,
            "all_multipliers_are_one_at_full_ramification_levels": level % (prime-1) == 0,
            "scope": "integer-embedded secret, native input-index multiplication, conjugate trace-dual label transport",
            "general_prime_physical_compiler_implemented": prime == 3,
            "all_quantum_encodings_or_merges_excluded": False}


def uniform_source_control():
    # Condition on two low labels1,1; Gaussian coefficients depend ONLY on them.
    high = [y for y in elements(3) if residue(y) == 1]
    by_outcome = [{y: 0 for y in elements(2)} for _ in range(3)]
    for y, z in product(high, repeat=2):
        # The public RREF dependence is(2,1), so T2 applies to the first state.
        first, second = rescale_label(y, 2, 3), z
        for x in range(3):
            root = ZETA**x % PHI
            merged = plus(first, multiply((int(root[0]), int(root[1])), second, 3), 3)
            by_outcome[x][divide_pi(merged, 3)] += 1
    assert all(len(set(counts.values())) == 1 for counts in by_outcome)
    counts = {y: sum(c[y] for c in by_outcome) for y in elements(2)}
    return {"parent_level": 3, "conditioned_low_labels": [1, 1], "kernel_weights": [2, 1],
            "exact_parent_pairs": len(high)**2, "all_uniform_difference_outcomes": 3,
            "child_label_counts": [{"label": list(y), "count": count} for y, count in counts.items()],
            "counts_conditioned_on_each_difference_outcome": [
                {"difference_outcome": x, "child_label_counts": [
                    {"label": list(y), "count": count} for y, count in c.items()]}
                for x, c in enumerate(by_outcome)],
            "every_child_label_has_equal_count": True,
            "every_child_label_uniform_for_each_fixed_difference_outcome": True,
            "selection_after_reading_higher_digits_covered": False}


def run_controls():
    controls = []
    for level in (3, 5):
        for seed in range(45011, 45015):
            rng = random.Random(seed)
            h0, _, h1 = ideal_chart(level)[0]
            labels = [[(rng.randrange(h0), rng.randrange(h1)) for _ in range(2)] for _ in range(3)]
            secret = [(1, 0), (2, 0)]
            row = physical_merge(labels, secret, level)
            row["unfiltered_label_seed"] = seed
            controls.append(row)
    even_failure = rescale_label((1, 0), 2, 2)
    low_total = residue(plus(even_failure, (1, 0), 2))
    assert low_total != 0
    return {"status": "GALOIS_RESIDUE_POWER_GATE_AND_LEGAL_GAUSSIAN_LEVELS_LOCAL_REVIEW_PENDING",
            "arithmetic_charts": [{"level": L, "column_HNF_diagonal_cross_diagonal": list(ideal_chart(L)[0]),
                "trace_pairing_power_basis_row": [rational(x) for x in ideal_chart(L)[1]],
                "ring_cardinality": str(3**L)} for L in range(1, 7)],
            "physical_gaussian_merge_controls": controls,
            "conditioned_exact_source_control": uniform_source_control(),
            "even_level_countercontrol": {"level": 2, "two_input_labels": [[1, 0], [1, 0]],
                "formal_Gaussian_weights": [2, 1], "transformed_first_label": list(even_failure),
                "actual_transformed_label_sum_residue": low_total,
                "same_as_formal_weighted_zero_sum": False, "native_phase_level_reduction_available": False},
            "all_ternary_index_permutation_even_level_controls": [
                {"level": 2, "native_input_label": [1, 0], "old_index_as_function_of_new": [
                    (a*j+b) % 3 for j in range(3)], "affine_multiplier": a, "affine_offset": b,
                 "transformed_label": list(affine_label_transport((1, 0), a, b, 2)),
                 "transformed_low_residue": residue(affine_label_transport((1, 0), a, b, 2)),
                 "secret_dependent_global_phase_retained": True,
                 "scope": "all six qutrit basis permutations, not arbitrary unitaries or joint instruments"}
                for a in (1, 2) for b in range(3)],
            "level_power_classifications": [level_classification(p, L) for p in (2, 3, 5, 7) for L in range(1, 13)],
            "ternary_scaling_ledgers": [{"modulus_log3": t, "initial_level": 2*t,
                "Gaussian_surjective_stages": t-1, "remaining_subset_zero_sum_stages": t,
                "batch_factor_expression": "(n+1)^(t-1)*S(n,3)^t; final decoding and recursion additional",
                "bound_scope": "conservative one-output-per-batch consumption upper ledger, not optimal sample lower bound",
                "Gaussian_only_batch_factor_expression": "(n+1)^(t-1)",
                "constant_cost_even_levels_alone_make_this_ledger_polynomial": False,
                "asymptotic_scope": "growing t=Theta(log n), not fixed modulus; this is construction accounting, not a computational lower bound",
                "quasi_polynomial_bottleneck_removed": False} for t in (1, 2, 4, 8, 16, 32)],
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False,
                "Shor_level_improvement": False, "standard_LWE_attack": False,
                "general_ring_secret_Galois_transform_preserves_same_secret": False,
                "arbitrary_even_level_coefficient_compiler": False, "independent_theorem_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "physical_merges": len(report["physical_gaussian_merge_controls"]),
                      "new_algorithm": False, "even_level_gate_preserved": True}))


if __name__ == "__main__":
    main()
