"""Pinned Hasse-differential decoding; no native quantum execution or novelty claim.

The interpolant uses the unaugmented syndrome ONLY. Public, independently
sampled coordinate pins subsequently resolve its entire affine solution space.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
from math import comb, isqrt
from pathlib import Path
import random
import time

from flint import fmpz_mod_ctx, fmpz_mod_mat

from theorems.folded_rs_decoder import affine_solution
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/hermite_pinned_decoder.json"


def integer(x, lo, hi, label):
    if type(x) is not int or not lo <= x <= hi:
        raise ValueError(f"{label} must be an integer in [{lo},{hi}]")
    return x


def canonical(values, length, p):
    if len(values) != length or any(type(x) is not int or not 0 <= x < p for x in values):
        raise ValueError("canonical field vector of the specified length required")


def jet(coefficients, a, ell, p):
    """Taylor coefficients, not ordinary derivatives."""
    return [sum(c * comb(h, j) * pow(a, h-j, p)
                for h, c in enumerate(coefficients) if h >= j) % p
            for j in range(ell)]


def parameters(p, ell, order, radius):
    ring(p)
    integer(ell, 1, p-1, "multiplicity")
    integer(order, 0, ell-1, "differential order")
    n, k = p-1, ell*(p-1)//2
    integer(radius, 0, n-1, "guarded block radius")
    constraints = n*(ell-order)
    constant = k + (order+1)*(order+2)//2
    a = max(0, (constraints-constant)//(order+2)+1)
    degree = a+k-1
    unknowns = (order+2)*a + constant
    if unknowns <= constraints or degree >= constraints:
        raise ValueError("nonzero message-dependent interpolation not certified")
    if (n-radius)*(ell-order) <= degree:
        raise ValueError("strict multiplicity-root inequality fails")
    return dict(p=p, n=n, ell=ell, k=k, order=order, radius=radius,
                a=a, identity_degree=degree, constraints=constraints,
                unknowns=unknowns, kernel_dimension_bound=order*((k+p-1)//p),
                unique_decoding_radius=n//4)


def operator_matrix(p, k, coefficients):
    """Coefficient matrix of sum_j A_j(X) f^[j](X), including small characteristic."""
    ring(p)
    integer(k, 1, 1 << 20, "polynomial coefficient count")
    if not coefficients or len(coefficients) > p:
        raise ValueError("operator order must be less than the characteristic")
    for polynomial in coefficients:
        canonical(polynomial, len(polynomial), p)
    nonzero = [(j, h, c) for j, poly in enumerate(coefficients)
               for h, c in enumerate(poly) if c]
    if not nonzero:
        raise ValueError("nonzero differential operator required")
    shift = max(h-j for j, h, _ in nonzero)
    rows = [[0]*k for _ in range(max(0, k+shift))]
    for j, h, c in nonzero:
        for t in range(j, k):
            rows[t-j+h][t] = (rows[t-j+h][t] + c*comb(t, j)) % p
    zeros = [t for t in range(k)
             if sum(c*comb(t, j) for j, h, c in nonzero
                    if h-j == shift and t >= j) % p == 0]
    return rows, {"leading_degree_shift": shift, "unpivoted_degree_indices": zeros,
                  "kernel_dimension_bound": len(zeros),
                  "coarse_kernel_dimension_bound": (len(coefficients)-1)*((k+p-1)//p)}


def differential_space(p, ell, order, radius, received):
    spec = parameters(p, ell, order, radius)
    n, k, a = spec["n"], spec["k"], spec["a"]
    canonical(received, n*ell, p)
    sizes = [a+k] + [a+j+1 for j in range(order+1)]
    rows = []
    for block, point in enumerate(range(1, p)):
        y = received[block*ell:(block+1)*ell]
        for t in range(ell-order):
            row = [comb(h, t)*pow(point, h-t, p) % p if h >= t else 0
                   for h in range(sizes[0])]
            for j in range(order+1):
                row += [sum(comb(h, t-u)*pow(point, h-(t-u), p)
                            * comb(j+u, j)*y[j+u]
                            for u in range(t+1) if h >= t-u) % p
                        for h in range(sizes[j+1])]
            rows.append(row)
    solution = affine_solution(p, rows, [0]*len(rows), sum(sizes))
    if solution is None or not solution["basis"]:
        raise ArithmeticError("interpolation dimension count failed")
    vector = solution["basis"][0]
    pieces, start = [], 0
    for size in sizes:
        pieces.append(vector[start:start+size])
        start += size
    operator, pivot = operator_matrix(p, k, pieces[1:])
    height = max(len(operator), len(pieces[0]))
    operator += [[0]*k for _ in range(height-len(operator))]
    rhs = [(-pieces[0][h]) % p if h < len(pieces[0]) else 0 for h in range(height)]
    space = affine_solution(p, operator, rhs, k)
    if space is not None and len(space["basis"]) > pivot["kernel_dimension_bound"]:
        raise ArithmeticError("small-characteristic pivot bound violated")
    return {"parameters": spec, "interpolant": pieces, "pivot_certificate": pivot,
            "affine_space": space}


def _multiply(a, b, size, p):
    result = [0]*size
    for i, x in enumerate(a):
        for j, y in enumerate(b[:max(0, size-i)]):
            result[i+j] = (result[i+j]+x*y) % p
    return result


def dual_block(p, ell, point):
    """Residue pairing for A(X)=(X^(p-1)-1)^ell, computed without dual-code advice."""
    base = [comb(p-1, j+1)*pow(point, p-2-j, p) % p for j in range(ell)]
    denominator = [1]+[0]*(ell-1)
    for _ in range(ell):
        denominator = _multiply(denominator, base, ell, p)
    inverse = [pow(denominator[0], -1, p)]
    for t in range(1, ell):
        inverse.append(-inverse[0]*sum(denominator[j]*inverse[t-j]
                                      for j in range(1, t+1)) % p)
    return [[inverse[ell-1-j-h] if j+h < ell else 0
             for h in range(ell)] for j in range(ell)]


class HermiteSyndrome:
    """Half-rate native syndrome and explicit local duality, independent of pins."""

    def __init__(self, p, ell):
        ring(p)
        integer(ell, 1, p-1, "multiplicity")
        self.p, self.ell, self.n = p, ell, p-1
        self.k, self.width = ell*(p-1)//2, ell*(p-1)
        ctx = fmpz_mod_ctx(p)
        self.g = fmpz_mod_mat(
            [[comb(h, j)*pow(a, h-j, p) % p if h >= j else 0
              for a in range(1, p) for j in range(ell)] for h in range(self.k)], ctx)
        # First k jet columns are a confluent Vandermonde information set.
        self.right = fmpz_mod_mat(
            [[int(self.g[i, j]) for j in range(self.k)] for i in range(self.k)], ctx).inv()
        self.blocks = [fmpz_mod_mat(dual_block(p, ell, a), ctx) for a in range(1, p)]
        self.inverse_blocks = [block.inv() for block in self.blocks]

    def encode(self, polynomial):
        canonical(polynomial, self.k, self.p)
        return [x for a in range(1, self.p) for x in jet(polynomial, a, self.ell, self.p)]

    def syndrome(self, error):
        canonical(error, self.width, self.p)
        column = self.g*fmpz_mod_mat([[x] for x in error], fmpz_mod_ctx(self.p))
        return [int(column[i, 0]) for i in range(self.k)]

    def transform(self, word, *, inverse=False):
        canonical(word, self.width, self.p)
        output = []
        blocks = self.inverse_blocks if inverse else self.blocks
        for i, block in enumerate(blocks):
            column = block*fmpz_mod_mat(
                [[x] for x in word[i*self.ell:(i+1)*self.ell]], fmpz_mod_ctx(self.p))
            output += [int(column[j, 0]) for j in range(self.ell)]
        return output

    def received(self, syndrome):
        canonical(syndrome, self.k, self.p)
        column = self.right*fmpz_mod_mat([[x] for x in syndrome], fmpz_mod_ctx(self.p))
        e0 = [int(column[i, 0]) for i in range(self.k)] + [0]*(self.width-self.k)
        return e0, [(-x) % self.p for x in self.transform(e0, inverse=True)]

    def duality_verified(self):
        rows = [self.transform([int(self.g[i, j]) for j in range(self.width)])
                for i in range(self.k)]
        product = self.g*fmpz_mod_mat(rows, fmpz_mod_ctx(self.p)).transpose()
        return not any(product[i, j] for i in range(self.k) for j in range(self.k))


def pin_space(p, ell, space, pins):
    """Pins map zero-based block indices to TRUE jets of the unknown polynomial."""
    if space is None:
        return None
    k, dimension = len(space["offset"]), len(space["basis"])
    rows, rhs = [], []
    for block, values in sorted(pins.items()):
        integer(block, 0, p-2, "pin block")
        canonical(values, ell, p)
        base = jet(space["offset"], block+1, ell, p)
        directions = [jet(v, block+1, ell, p) for v in space["basis"]]
        for j in range(ell):
            rows.append([v[j] for v in directions])
            rhs.append((values[j]-base[j]) % p)
    if dimension == 0:
        return {"offset": space["offset"], "basis": []} if not any(rhs) else None
    coefficients = affine_solution(p, rows, rhs, dimension)
    if coefficients is None:
        return None
    offset = [(space["offset"][i] + sum(a*v[i] for a, v in
              zip(coefficients["offset"], space["basis"]))) % p for i in range(k)]
    basis = [[sum(a*v[i] for a, v in zip(direction, space["basis"])) % p
              for i in range(k)] for direction in coefficients["basis"]]
    return {"offset": offset, "basis": basis}


def block_weight(word, ell):
    return sum(any(word[i:i+ell]) for i in range(0, len(word), ell))


def decode(code, syndrome, pins, *, order, radius):
    """ONLY syndrome, public parameters and retained error blocks are supplied."""
    e0, y = code.received(syndrome)
    info = differential_space(code.p, code.ell, order, radius, y)
    polynomial_pins = {}
    for block, values in pins.items():
        integer(block, 0, code.n-1, "pin block")
        canonical(values, code.ell, code.p)
        column = code.inverse_blocks[block]*fmpz_mod_mat(
            [[v] for v in values], fmpz_mod_ctx(code.p))
        polynomial_pins[block] = [(int(column[j, 0])+y[block*code.ell+j]) % code.p
                                  for j in range(code.ell)]
    pinned = pin_space(code.p, code.ell, info["affine_space"], polynomial_pins)
    result = {"status": "ABSTAIN_EMPTY" if pinned is None else "ABSTAIN_AMBIGUOUS",
              "affine_dimension_before_pins": None if info["affine_space"] is None
              else len(info["affine_space"]["basis"]),
              "affine_dimension_after_pins": None if pinned is None else len(pinned["basis"]),
              "parameters": info["parameters"], "pivot_certificate": info["pivot_certificate"],
              "interpolant": info["interpolant"], "pin_blocks": sorted(pins),
              "error": None, "polynomial": None,
              "hidden_support_or_polynomial_supplied": False,
              "coefficient_field_enumeration_used": False}
    if pinned is None or pinned["basis"]:
        return result
    delta = code.transform(code.encode(pinned["offset"]))
    error = [(x+z) % code.p for x, z in zip(e0, delta)]
    valid = (block_weight(error, code.ell) <= radius
             and code.syndrome(error) == list(syndrome)
             and all(error[i*code.ell:(i+1)*code.ell] == list(v) for i, v in pins.items()))
    if valid:
        result.update(status="UNIQUE_IN_GUARDED_BALL", error=error, polynomial=pinned["offset"])
    else:
        result["status"] = "ABSTAIN_DISTANCE_OR_CHECK"
    return result


def source_herald(error, result, ell, source_cap):
    """Equality with the syndrome-only decoder AND the smaller source cap."""
    integer(ell, 1, len(error), "block width")
    if len(error) % ell:
        raise ValueError("whole source blocks required")
    integer(source_cap, 0, len(error)//ell, "source cap")
    if result["parameters"]["radius"] < source_cap+2:
        raise ValueError("second-moment transfer needs the two-block guard")
    return (block_weight(error, ell) <= source_cap
            and result["status"] == "UNIQUE_IN_GUARDED_BALL"
            and result["error"] == list(error))


def pin_failure_bound(n, ell, k, dimension, count):
    """Rank exposure bound for a fixed affine space, independent uniform pins."""
    integer(n, 1, 1 << 40, "block count")
    integer(ell, 1, 1 << 30, "multiplicity")
    integer(k, 1, n*ell//2, "degree dimension at most half rate")
    integer(dimension, 0, k, "affine dimension bound")
    integer(count, 0, n, "pin count")
    if dimension == 0 or count > (k-1)//ell:
        return Fraction(0)
    total, term = 0, 1
    for j in range(min(dimension, count+1)):
        total += term
        term = term*(count-j)//(j+1)
    return Fraction(total, 2**count)


def pin_budget(n, ell, k, dimension, security_bits):
    integer(security_bits, 1, 4096, "failure security bits")
    goal = Fraction(1, 2**security_bits)
    # Chernoff gives failure <= exp(-r/8) for r >= 4*dimension.
    lo, hi = 0, min((k-1)//ell+1, 8*(dimension+security_bits))
    while lo < hi:
        mid = (lo+hi)//2
        if pin_failure_bound(n, ell, k, dimension, mid) <= goal:
            hi = mid
        else:
            lo = mid+1
    return lo


def fraction_record(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator),
            "float": float(x)}


def resource_ledger(p=1000000007, ell=256, order=15, security_bits=40):
    """Finite inequalities only: no matrices or quantum circuit executed here."""
    n = p-1
    d = 43*n//100
    spec = parameters(p, ell, order, d+2)
    r = pin_budget(n, ell, spec["k"], spec["kernel_dimension_bound"], security_bits)
    failure = pin_failure_bound(n, ell, spec["k"], spec["kernel_dimension_bound"], r)
    lam, tau, target = Fraction(21, 50), Fraction(43, 100), Fraction(99, 100)
    radicand, scale = lam*(1-lam), 2**128
    beta_lower = Fraction(1, 2)+Fraction(isqrt(radicand.numerator*scale**2//radicand.denominator), scale)
    # The exact finite-alphabet mean is at least beta - 1/q.
    gap = beta_lower-Fraction(1, p)-target-Fraction(r, n)
    exponent = 2*(tau-lam)**2*n
    tail = Fraction(1, 2**min(security_bits, exponent.numerator//exponent.denominator))
    rejected = tail+failure
    bad_joint = min(Fraction(1), (Fraction(1, 2*n)+2*rejected)/gap**2) if gap > 0 else Fraction(1)
    synthesis_tv = Fraction(1, 2**40)
    return {"parameters": spec, "source_cap": d, "guard_radius": d+2,
            "lambda": fraction_record(lam), "tau": fraction_record(tau),
            "random_pins": r, "pin_score_loss_fraction": fraction_record(Fraction(r, n)),
            "pin_rejection_upper": fraction_record(failure),
            "tail_upper_expression": "exp(-2*(tau-lambda)^2*n)",
            "tail_upper_paid": fraction_record(tail),
            "product_score_fraction_lower": fraction_record(beta_lower-Fraction(1, p)),
            "target_score_fraction": fraction_record(target),
            "score_gap_after_pins_lower": fraction_record(gap),
            "conditional_joint_bad_output_upper": fraction_record(bad_joint),
            "required_total_synthesis_tv": fraction_record(synthesis_tv),
            "conditional_total_failure_upper": fraction_record(min(Fraction(1), rejected+bad_joint+synthesis_tv)),
            "composition_premises": [
                "published arbitrary-order one-pass product source with theta=lambda*(1-q^(-2*ell))",
                "deterministic interpolant independent of random pin set and exact coherent decoder",
                "source cap d, unique decoding in the entire guarded ball B_(d+2)",
                "uncompute all work and keep herald failures; discard auxiliary output only after sampling",
                "implement full circuit within the stated total output TV budget",
            ],
            "dense_field_storage_order": "(q*ell)^2",
            "dense_field_operation_order": "(q*ell)^3 times polynomial(order)",
            "conservative_reversible_bit_workspace": "poly(q,ell,log(q)), including computation history",
            "tight_linear_workspace_claim": False, "native_parameters_executed": False,
            "stream_length_expression": "(q-1)*q^ell",
            "growing_regime": "ell=floor(q^a), fixed 0<a<1 and fixed target/slack/order",
            "classical_lower_bound_condition": "choose a small enough for the constant C_alpha in the published bound; do not assign C_alpha a numeric value",
            "end_to_end_quantum_claim_allowed": False}


def _minimal_word(code):
    ctx = ring(code.p)
    polynomial = ctx([1])
    remaining = code.k-1
    for point in range(1, code.p):
        exponent = min(code.ell, remaining)
        polynomial *= ctx([-point, 1])**exponent
        remaining -= exponent
        if not remaining:
            break
    return [int(polynomial[i]) for i in range(code.k)]


def sparse_moment_control(code, errors, shifts, pin_indices):
    """Exact character-Gram calculation on a sparse local-observable support.

    Character orthogonality identifies Fourier-output Gram entries with
    augmented-syndrome equality. This is not a quantum gate simulation.
    """
    if not errors or not shifts:
        raise ValueError("nonempty source and local Hermitian observable required")
    for error in errors:
        canonical(error, code.width, code.p)
    for shift in shifts:
        canonical(shift, code.width, code.p)
        if block_weight(shift, code.ell) != 1:
            raise ValueError("each observable translation must change one block")
        if [-x % code.p for x in shift] not in shifts:
            raise ValueError("observable translations must include their inverses")
    for i in pin_indices:
        integer(i, 0, code.n-1, "pin block")
    if len(set(pin_indices)) != len(pin_indices):
        raise ValueError("distinct pins required")

    def histogram(words):
        result = {}
        for word in words:
            key = tuple(word)
            result[key] = result.get(key, 0)+1
        return result

    source = histogram(errors)
    neighbors = histogram([[(x+y) % code.p for x, y in zip(error, shift)]
                           for error in errors for shift in shifts])

    def push(values):
        output = {}
        for word, coefficient in values.items():
            label = tuple(code.syndrome(word))+tuple(
                word[i*code.ell+j] for i in pin_indices for j in range(code.ell))
            output[label] = output.get(label, 0)+coefficient
        return output

    encoded_source, encoded_neighbors = push(source), push(neighbors)
    norm = lambda values: sum(v*v for v in values.values())
    overlap = lambda a, b: sum(v*b.get(key, 0) for key, v in a.items())
    return {
        "source_norm_squared": norm(source), "fourier_source_norm_squared": norm(encoded_source),
        "first_moment": overlap(source, neighbors),
        "fourier_first_moment": overlap(encoded_source, encoded_neighbors),
        "second_moment": norm(neighbors), "fourier_second_moment": norm(encoded_neighbors),
        "source_support": len(source), "neighbor_support": len(neighbors),
        "augmented_neighbor_support": len(encoded_neighbors),
        "mode": "exact character orthogonality, no native quantum gates",
    }


def controls():
    start = time.monotonic()
    code = HermiteSyndrome(31, 24)
    if not code.duality_verified():
        raise ArithmeticError("explicit local duality failed")
    delta = code.transform(code.encode(_minimal_word(code)))
    support = [i for i in range(code.n) if any(delta[i*code.ell:(i+1)*code.ell])]
    split = set(support[:len(support)//2])
    left = [x if i//code.ell in split else 0 for i, x in enumerate(delta)]
    right = [0 if i//code.ell in split else -x % code.p for i, x in enumerate(delta)]
    syndrome = code.syndrome(left)
    if syndrome != code.syndrome(right):
        raise ArithmeticError("ambiguity fixture has different syndromes")
    bare = decode(code, syndrome, {}, order=4, radius=10)
    if bare["status"] != "ABSTAIN_AMBIGUOUS":
        raise ArithmeticError("ambiguous guarded ball was falsely accepted")
    selected = random.Random(2026102062).sample(range(code.n), 8)
    decoded = []
    for error in (left, right):
        pins = {i: error[i*code.ell:(i+1)*code.ell] for i in selected}
        result = decode(code, syndrome, pins, order=4, radius=10)
        if result["error"] != error:
            raise ArithmeticError("pinned ambiguity control did not recover the actual error")
        if not source_herald(error, result, code.ell, 8):
            raise ArithmeticError("valid source error failed the guarded equality herald")
        decoded.append(result)
    a = [x if i//code.ell == support[7] else 0 for i, x in enumerate(delta)]
    b = [-x % code.p if i//code.ell == support[8] else 0 for i, x in enumerate(delta)]
    shifts = [a, [-x % code.p for x in a], b, [-x % code.p for x in b]]
    lower_errors = [[(x-y) % code.p for x, y in zip(error, change)]
                    for error, change in zip((left, right), (a, b))]
    guard_negative = sparse_moment_control(code, lower_errors, shifts, [])
    guarded_positive = sparse_moment_control(code, [left, right], shifts, selected)
    if (guard_negative["source_norm_squared"] != guard_negative["fourier_source_norm_squared"]
            or guard_negative["second_moment"] == guard_negative["fourier_second_moment"]):
        raise ArithmeticError("missing two-block-guard counterexample")
    if any(guarded_positive[name] != guarded_positive["fourier_"+name]
           for name in ("source_norm_squared", "first_moment", "second_moment")):
        raise ArithmeticError("guarded sparse character-moment identity failed")
    # Sharp small-characteristic pathology: f'=0 includes all p-th powers.
    matrix, pivots = operator_matrix(5, 17, [[0], [1]])
    frobenius = affine_solution(5, matrix, [0]*len(matrix), 17)
    # Exhaust all pin subsets for a fixed nontrivial affine space, not source trials.
    basis = [[int(j == degree) for j in range(7)] for degree in (0, 5)]
    space = {"offset": [0]*7, "basis": basis}
    census = []
    for r in range(5):
        bad = sum(bool(pin_space(5, 4, space, {i: [0]*4 for i in indices})["basis"])
                  for indices in combinations(range(4), r))
        actual = Fraction(bad, comb(4, r))
        bound = pin_failure_bound(4, 4, 7, 2, r)
        if actual > bound:
            raise ArithmeticError("rank-exposure control violates bound")
        census.append({"pins": r, "ambiguity_probability": fraction_record(actual),
                       "upper": fraction_record(bound)})
    return {
        "status": "PINNED_DIFFERENTIAL_DECODER_EXECUTED_COMPOSITION_REVIEW_PENDING",
        "native": {"p": code.p, "ell": code.ell, "n": code.n, "k": code.k,
                   "source_cap": 8, "guard_radius": 10, "unique_decoding_radius": code.n//4,
                   "public_syndrome": syndrome, "two_errors": [left, right],
                   "error_weights": [block_weight(e, code.ell) for e in (left, right)],
                   "duality_verified": True, "unpinned": bare, "pinned": decoded,
                   "seconds": time.monotonic()-start},
        "frobenius_control": {"p": 5, "k": 17, "operator": "f^[1]",
                             "kernel_dimension": len(frobenius["basis"]),
                             "basis": frobenius["basis"], "pivot_certificate": pivots,
                             "false_order_only_dimension_bound_rejected": len(frobenius["basis"]) > 1},
        "rank_exposure_exhaustive_control": census, "resource_ledger": resource_ledger(),
        "guard_negative": {"error_weights": [block_weight(e, code.ell) for e in lower_errors],
                           "each_unique_in_radius": code.n//4,
                           "reason": "dual block distance is 16, exceeding twice 7",
                           "two_block_guard_omitted": True, **guard_negative},
        "guarded_moment_control": guarded_positive,
        "classical_decoder_component_only": True, "native_quantum_circuit_executed": False,
        "new_quantum_algorithm_claim_allowed": False, "novelty_established": False,
        "proof_status": "written local arguments and exact controls; independent review pending",
        "sources": ["https://arxiv.org/html/2610.01902v1",
                    "https://arxiv.org/html/2311.17841v4", "https://arxiv.org/abs/1805.01498",
                    "https://arxiv.org/pdf/1106.3951"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"path": str(args.output), "status": report["status"],
                      "native_weights": report["native"]["error_weights"],
                      "affine_dimension": report["native"]["unpinned"]["affine_dimension_before_pins"],
                      "native_seconds": report["native"]["seconds"]}, indent=2))


if __name__ == "__main__":
    main()
