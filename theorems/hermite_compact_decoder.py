"""Compact polynomial-module Hermite decoder, with recomputation instead of a dense basis.

Classical algorithm only. The written reversible bound retains Bennett's
logarithmic workspace overhead; no linear-qubit quantum circuit is claimed.
"""
from __future__ import annotations

import argparse
from itertools import islice
import json
from math import comb
from pathlib import Path
import random
import time

from flint import fmpz_mod_ctx, fmpz_mod_mat

from theorems.hermite_pinned_decoder import (
    block_weight, canonical, dual_block, integer, jet, parameters, source_herald,
)
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/hermite_compact_decoder.json"


def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def subtract(a, b, factor, shift, p):
    out = list(a)+[0]*max(0, len(b)+shift-len(a))
    for i, x in enumerate(b):
        out[i+shift] = (out[i+shift]-factor*x) % p
    return trim(out)


def times_linear(poly, root, p):
    result = [0]*(len(poly)+1)
    for i, x in enumerate(poly):
        result[i] = (result[i]-root*x) % p
        result[i+1] = x
    return trim(result)


def divide_linear(poly, root, p):
    if len(poly) < 2:
        raise ValueError("nonconstant polynomial required for exact deflation")
    result = [0]*(len(poly)-1)
    result[-1] = poly[-1]
    for i in range(len(result)-2, -1, -1):
        result[i] = (poly[i+1]+root*result[i+1]) % p
    if (poly[0]+root*result[0]) % p:
        raise ArithmeticError("linear deflation has a nonzero remainder")
    return trim(result)


def multiply(a, b, p):
    if not a or not b:
        return []
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = (out[i+j]+x*y) % p
    return trim(out)


def leading(row, weights):
    return max((len(poly)-1+weight, j) for j, (poly, weight)
               in enumerate(zip(row, weights)) if poly)


def weak_popov(basis, weights, p):
    """Monomial row cancellation; no dense scalar matrix or transformation matrix."""
    reductions = 0
    peak = sum(len(poly) for row in basis for poly in row)
    while True:
        positions, collision = {}, None
        for i, row in enumerate(basis):
            degree, position = leading(row, weights)
            if position in positions:
                j = positions[position]
                receiver, donor = (i, j) if degree >= leading(basis[j], weights)[0] else (j, i)
                collision = receiver, donor, position
                break
            positions[position] = i
        if collision is None:
            return basis, reductions, peak
        receiver, donor, position = collision
        old = leading(basis[receiver], weights)
        shift = len(basis[receiver][position])-len(basis[donor][position])
        factor = basis[receiver][position][-1]*pow(basis[donor][position][-1], -1, p) % p
        basis[receiver] = [subtract(a, b, factor, shift, p)
                           for a, b in zip(basis[receiver], basis[donor])]
        if leading(basis[receiver], weights) >= old:
            raise ArithmeticError("shifted row reduction did not lower its leading term")
        reductions += 1
        peak = max(peak, sum(len(poly) for row in basis for poly in row))


def module_interpolant(p, ell, order, radius, received, *, selection="fewest_pivots"):
    spec = parameters(p, ell, order, radius)
    canonical(received, spec["n"]*ell, p)
    rank, height = order+2, ell-order
    weights = [-(spec["k"]-1)]+[-j for j in range(order+1)]
    basis = [[[int(i == j)] if i == j else [] for j in range(rank)] for i in range(rank)]
    updates, peak = 0, rank
    for block, point in enumerate(range(1, p)):
        y = received[block*ell:(block+1)*ell]
        local = [[1]+[0]*(height-1)] + [
            [comb(j+u, j)*y[j+u] % p for u in range(height)]
            for j in range(order+1)]
        expanded = [[jet(poly, point, height, p) for poly in row] for row in basis]
        for t in range(height):
            discrepancies = [sum(expanded[i][j][t-u]*local[j][u]
                                  for j in range(rank) for u in range(t+1)) % p
                             for i in range(rank)]
            active = [i for i, value in enumerate(discrepancies) if value]
            if not active:
                continue
            pivot = min(active, key=lambda i: (leading(basis[i], weights), i))
            for i in active:
                if i == pivot:
                    continue
                factor = discrepancies[i]*pow(discrepancies[pivot], -1, p) % p
                basis[i] = [subtract(a, b, factor, 0, p) for a, b in zip(basis[i], basis[pivot])]
                expanded[i] = [[(x-factor*z) % p for x, z in zip(a, b)]
                               for a, b in zip(expanded[i], expanded[pivot])]
            basis[pivot] = [times_linear(poly, point, p) for poly in basis[pivot]]
            expanded[pivot] = [[0]+values[:-1] for values in expanded[pivot]]
            updates += 1
            peak = max(peak, sum(len(poly) for row in basis for poly in row))
    basis, reductions, reduced_peak = weak_popov(basis, weights, p)
    peak = max(peak, reduced_peak)
    if selection not in ("shortest", "fewest_pivots"):
        raise ValueError("unknown deterministic interpolant selection")
    eligible = [i for i, row in enumerate(basis) if leading(row, weights)[0] <= spec["a"]]
    profiles = [{"row": i, "shifted_degree": leading(basis[i], weights)[0],
                 "free_coordinate_bound": len(DescendingSystem(p, spec["k"], basis[i]).free)}
                for i in eligible]
    if not profiles:
        raise ArithmeticError("no module basis row satisfies the degree budget")
    chosen_profile = min(profiles, key=lambda row: (
        row["shifted_degree"] if selection == "shortest" else row["free_coordinate_bound"],
        row["shifted_degree"], row["row"]))
    chosen = chosen_profile["row"]
    pieces = basis[chosen]
    if leading(pieces, weights)[0] > spec["a"]:
        raise ArithmeticError("module shortest row exceeds the certified degree budget")
    if not any(pieces[1:]):
        raise ArithmeticError("interpolant has no differential part")
    return {"parameters": spec, "interpolant": pieces,
            "basis_leading_pairs": [list(leading(row, weights)) for row in basis],
            "module_rank": rank, "constraint_updates": updates,
            "row_reductions": reductions, "peak_basis_coefficients": peak,
            "selection": selection, "eligible_interpolants": profiles,
            "dense_scalar_interpolation_matrix_stored": False}


class CompactHermite:
    """Fixed right inverse via Hermite cardinal polynomials, one at a time."""

    def __init__(self, p, ell):
        ring(p)
        integer(ell, 1, p-1, "multiplicity")
        self.p, self.ell, self.n = p, ell, p-1
        self.k, self.width = ell*(p-1)//2, ell*(p-1)

    def encode(self, polynomial):
        canonical(polynomial, self.k, self.p)
        return [x for a in range(1, self.p) for x in jet(polynomial, a, self.ell, self.p)]

    def syndrome(self, error):
        canonical(error, self.width, self.p)
        return [sum(error[(a-1)*self.ell+j]*comb(h, j)*pow(a, h-j, self.p)
                    for a in range(1, self.p) for j in range(min(h+1, self.ell))) % self.p
                for h in range(self.k)]

    def transform(self, word, *, inverse=False):
        canonical(word, self.width, self.p)
        output = []
        for i, point in enumerate(range(1, self.p)):
            block = fmpz_mod_mat(dual_block(self.p, self.ell, point), fmpz_mod_ctx(self.p))
            if inverse:
                block = block.inv()
            values = block*fmpz_mod_mat([[x] for x in word[i*self.ell:(i+1)*self.ell]],
                                       fmpz_mod_ctx(self.p))
            output += [int(values[j, 0]) for j in range(self.ell)]
        return output

    def received(self, syndrome):
        canonical(syndrome, self.k, self.p)
        p, ell = self.p, self.ell
        product = [1]
        for a in range(1, self.n//2+1):
            for _ in range(ell):
                product = times_linear(product, a, p)
        e0 = []
        for a in range(1, self.n//2+1):
            quotient = list(product)
            for _ in range(ell):
                quotient = divide_linear(quotient, a, p)
            local = jet(quotient, a, ell, p)
            inverse = [pow(local[0], -1, p)]
            for h in range(1, ell):
                inverse.append(-inverse[0]*sum(local[j]*inverse[h-j] for j in range(1, h+1)) % p)
            for j in range(ell):
                # Horner expansion of Z^j * (1/Q(a+Z) mod Z^(ell-j)).
                series = [0]*j+inverse[:ell-j]
                factor = []
                for value in reversed(series):
                    factor = times_linear(factor, a, p)
                    if factor:
                        factor[0] = (factor[0]+value) % p
                        trim(factor)
                    elif value:
                        factor = [value]
                cardinal = multiply(quotient, factor, p)
                e0.append(sum(x*y for x, y in zip(cardinal, syndrome)) % p)
        e0 += [0]*(self.width-self.k)
        if self.syndrome(e0) != list(syndrome):
            raise ArithmeticError("cardinal-polynomial right inverse failed")
        return e0, [-x % p for x in self.transform(e0, inverse=True)]


class DescendingSystem:
    """Implicit affine parametrization using only one coefficient vector at a time."""

    def __init__(self, p, k, pieces):
        self.p, self.k, self.q0, self.operator = p, k, pieces[0], pieces[1:]
        terms = [(j, h, c) for j, poly in enumerate(self.operator)
                 for h, c in enumerate(poly) if c]
        if not terms or len(self.operator) > p:
            raise ValueError("nonzero operator of order less than characteristic required")
        self.shift = max(h-j for j, h, _ in terms)
        top = [(j, c) for j, h, c in terms if h-j == self.shift]
        self.pivots = [sum(c*comb(t, j) for j, c in top if t >= j) % p for t in range(k)]
        self.free = [t for t, value in enumerate(self.pivots) if not value]
        self.free_set = set(self.free)
        self.height = max(len(self.q0), k+self.shift)
        self.generated_vectors = 0

    def coefficient(self, h, t):
        return sum(poly[h-t+j]*comb(t, j) for j, poly in enumerate(self.operator)
                   if t >= j and 0 <= h-t+j < len(poly)) % self.p

    def vector(self, free_index=None, *, homogeneous=False):
        f = [0]*self.k
        for t in range(self.k-1, -1, -1):
            if t in self.free_set:
                f[t] = int(t == free_index)
                continue
            h = t+self.shift
            value = self.q0[h] if not homogeneous and 0 <= h < len(self.q0) else 0
            value += sum(self.coefficient(h, u)*f[u] for u in range(t+1, self.k) if f[u])
            f[t] = -value*pow(self.pivots[t], -1, self.p) % self.p
        self.generated_vectors += 1
        return f

    def residual(self, f, h, *, homogeneous=False):
        return (sum(self.coefficient(h, t)*x for t, x in enumerate(f) if x)
                + (self.q0[h] if not homogeneous and h < len(self.q0) else 0)) % self.p

    def solve(self, pins, ell):
        p, dimension = self.p, len(self.free)
        offset = self.vector()
        echelon = {}
        pivot_rows = {t+self.shift for t, value in enumerate(self.pivots) if value}
        identities = [h for h in range(self.height) if h not in pivot_rows]
        before_pins = None
        equations_seen = 0
        for block, values in pins.items():
            integer(block, 0, p-2, "pin block")
            canonical(values, ell, p)

        def constraints():
            for h in identities:
                yield ("identity", h, 0)
            for block, values in sorted(pins.items()):
                for j, value in enumerate(values):
                    yield ("pin", (block+1, j), value)

        stream, peak_batch = iter(constraints()), 0
        batch_size = max(1, (2*self.k)//(dimension+1))
        while len(echelon) < dimension:
            batch = list(islice(stream, batch_size))
            if not batch:
                break
            # Batching reuses each regenerated direction without storing a K-by-z basis.
            rows = [[0]*dimension for _ in batch]
            right = []
            peak_batch = max(peak_batch, len(batch)*(dimension+1))
            for kind, index, target in batch:
                value = self.residual(offset, index) if kind == "identity" else jet(offset, index[0], index[1]+1, p)[index[1]]
                right.append((target-value) % p)
            for column, t in enumerate(self.free):
                direction = self.vector(t, homogeneous=True)
                for i, (kind, index, _) in enumerate(batch):
                    rows[i][column] = (self.residual(direction, index, homogeneous=True)
                                       if kind == "identity"
                                       else jet(direction, index[0], index[1]+1, p)[index[1]])
            for (kind, _, _), row, rhs in zip(batch, rows, right):
                if kind == "pin" and before_pins is None:
                    before_pins = dimension-len(echelon)
                if len(echelon) == dimension:
                    break
                equations_seen += 1
                for pivot in sorted(echelon):
                    old, old_rhs = echelon[pivot]
                    factor = row[pivot]
                    row = [(x-factor*y) % p for x, y in zip(row, old)]
                    rhs = (rhs-factor*old_rhs) % p
                pivot = next((j for j, x in enumerate(row) if x), None)
                if pivot is None:
                    if rhs:
                        return {"status": "ABSTAIN_EMPTY", "polynomial": None,
                                "free_coordinates": dimension, "equations_seen": equations_seen}
                else:
                    inv = pow(row[pivot], -1, p)
                    echelon[pivot] = ([x*inv % p for x in row], rhs*inv % p)
        if before_pins is None:
            before_pins = dimension-len(echelon)
        result = {"status": "ABSTAIN_AMBIGUOUS", "polynomial": None,
                  "free_coordinates": dimension, "dimension_before_pins": before_pins,
                  "remaining_dimension": dimension-len(echelon),
                  "equations_seen": equations_seen, "stored_echelon_field_entries": len(echelon)*(dimension+1),
                  "peak_constraint_batch_field_entries": peak_batch}
        if len(echelon) != dimension:
            return result
        coordinates = [0]*dimension
        for pivot in sorted(echelon, reverse=True):
            row, rhs = echelon[pivot]
            coordinates[pivot] = (rhs-sum(row[j]*coordinates[j] for j in range(pivot+1, dimension))) % p
        f = list(offset)
        for value, t in zip(coordinates, self.free):
            if value:
                direction = self.vector(t, homogeneous=True)
                f = [(x+value*y) % p for x, y in zip(f, direction)]
        # Recheck ALL original equations, including ones skipped after full rank.
        if (any(self.residual(f, h) for h in range(self.height))
                or any(jet(f, i+1, ell, p) != list(v) for i, v in pins.items())):
            result["status"] = "ABSTAIN_INCONSISTENT"
        else:
            result.update(status="UNIQUE_AFFINE_SOLUTION", polynomial=f)
        return result


def decode(code, syndrome, pins, *, order, radius, selection="fewest_pivots"):
    e0, y = code.received(syndrome)
    info = module_interpolant(code.p, code.ell, order, radius, y, selection=selection)
    pinned = {}
    for i, values in pins.items():
        integer(i, 0, code.n-1, "pin block")
        canonical(values, code.ell, code.p)
        block = fmpz_mod_mat(dual_block(code.p, code.ell, i+1), fmpz_mod_ctx(code.p)).inv()
        column = block*fmpz_mod_mat([[x] for x in values], fmpz_mod_ctx(code.p))
        pinned[i] = [(int(column[j, 0])+y[i*code.ell+j]) % code.p for j in range(code.ell)]
    system = DescendingSystem(code.p, code.k, info["interpolant"])
    solution = system.solve(pinned, code.ell)
    result = {**info, "status": solution["status"], "error": None,
              "polynomial": solution["polynomial"], "reduced_system": solution,
              "free_degree_indices": system.free, "coefficient_vectors_recomputed": system.generated_vectors,
              "dense_affine_basis_stored": False, "dense_syndrome_right_inverse_stored": False,
              "native_quantum_circuit_executed": False}
    if solution["polynomial"] is None:
        return result
    delta = code.transform(code.encode(solution["polynomial"]))
    error = [(a+b) % code.p for a, b in zip(e0, delta)]
    if (block_weight(error, code.ell) <= radius
            and code.syndrome(error) == list(syndrome)
            and all(error[i*code.ell:(i+1)*code.ell] == list(v) for i, v in pins.items())):
        result.update(status="UNIQUE_IN_GUARDED_BALL", error=error)
    else:
        result.update(status="ABSTAIN_DISTANCE_OR_CHECK", polynomial=None)
    return result


def workspace_ledger(p, ell, order, radius):
    spec = parameters(p, ell, order, radius)
    r, m, k, t = order+2, spec["constraints"], spec["k"], spec["kernel_dimension_bound"]
    return {"parameters": spec,
            "polynomial_module_basis_coefficient_upper": r*r*(m+k+1),
            "local_jet_cache_coefficient_upper": r*r*ell,
            "reduced_echelon_coefficient_upper": t*(t+1),
            "linear_vector_and_polynomial_scratch": "O_s(q*ell) field elements",
            "classical_workspace_bound": "O_s(q*ell*log(q)) bits for ell<q",
            "classical_time_bound": "poly_s(q,ell), including all recomputation",
            "reversible_workspace_bound": "O_s(q*ell*log(q)*log(q*ell)) via Bennett",
            "reversible_time_bound": "poly_s(q,ell)",
            "logarithmic_reversible_overhead_removed": False,
            "original_tight_linear_quantum_space_proved": False,
            "fixed_ell_scope": "ell must exceed an alpha-dependent threshold; this does not cover ell=1",
            "quantum_algorithm_claim_allowed": False,
            "status": "written complexity proof; review pending, not measured qubit usage"}


def controls():
    started = time.monotonic()
    code = CompactHermite(31, 24)
    polynomial = [1]
    remaining = code.k-1
    for a in range(1, code.p):
        for _ in range(min(remaining, code.ell)):
            polynomial = times_linear(polynomial, a, code.p)
            remaining -= 1
        if remaining == 0:
            break
    delta = code.transform(code.encode(polynomial))
    support = [i for i in range(code.n) if any(delta[i*code.ell:(i+1)*code.ell])]
    first = set(support[:8])
    errors = [[x if i//code.ell in first else 0 for i, x in enumerate(delta)],
              [0 if i//code.ell in first else -x % code.p for i, x in enumerate(delta)]]
    syndrome = code.syndrome(errors[0])
    if syndrome != code.syndrome(errors[1]):
        raise ArithmeticError("native ambiguity fixture failed")
    pin_indices = random.Random(2026102062).sample(range(code.n), 8)
    bare = decode(code, syndrome, {}, order=4, radius=10)
    if bare["status"] != "ABSTAIN_AMBIGUOUS":
        raise ArithmeticError("unpinned compact decoder falsely accepted ambiguity")
    outputs = []
    for error in errors:
        output = decode(code, syndrome, {i: error[i*code.ell:(i+1)*code.ell] for i in pin_indices},
                        order=4, radius=10)
        if output["error"] != error or not source_herald(error, output, code.ell, 8):
            raise ArithmeticError("compact decoder failed the native pinned source")
        outputs.append(output)
    short = decode(code, syndrome, {i: errors[0][i*code.ell:(i+1)*code.ell] for i in pin_indices},
                   order=4, radius=10, selection="shortest")
    if short["status"] != "ABSTAIN_AMBIGUOUS":
        raise ArithmeticError("shortest-row ambiguity negative control changed")
    return {"status": "COMPACT_HERMITE_DECODER_EXECUTED_REVERSIBLE_BOUND_REVIEW_PENDING",
            "p": code.p, "ell": code.ell, "n": code.n, "k": code.k,
            "error_weights": [block_weight(e, code.ell) for e in errors],
            "unique_decoding_radius": 7, "source_cap": 8, "guard_radius": 10,
            "public_syndrome": syndrome, "two_errors": errors, "pin_indices": pin_indices,
            "unpinned": bare, "pinned": outputs, "seconds": time.monotonic()-started,
            "shortest_interpolant_same_eight_pins": short,
            "workspace": workspace_ledger(31, 24, 4, 10),
            "dense_scalar_interpolation_matrix_stored": False,
            "native_quantum_circuit_executed": False, "novelty_established": False,
            "new_quantum_algorithm_claim_allowed": False,
            "sources": ["https://arxiv.org/html/2610.01902v1",
                        "https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf",
                        "https://arxiv.org/abs/2207.01319",
                        "https://doi.org/10.1137/0218053"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"path": str(args.output), "status": report["status"],
                      "seconds": report["seconds"],
                      "peak_basis_coefficients": report["unpinned"]["peak_basis_coefficients"],
                      "free_coordinates": report["unpinned"]["reduced_system"]["free_coordinates"]}, indent=2))


if __name__ == "__main__":
    main()
