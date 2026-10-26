"""Known deterministic binary-field GS ingredients and complete-list controls.

Berlekamp trace splitting, Roth-Ruckenstein coefficient extraction and a capped
dense interpolation reference. No randomized factorization, field enumeration
inside the decoder, reversible circuit, or native quantum speedup is claimed.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import fq_default_poly_ctx

from theorems.balanced_codeword_filter import integer
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.reciprocal_affine_pencil import check_root_completeness


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/binary_gs_decoder.json"


def linear_roots(bits, coefficients):
    """All DISTINCT base-field roots, via deterministic public-basis trace cuts.

    Coefficients are low-to-high in the existing repository's public field.
    Squarefree split extraction handles repeated and non-base-field factors.
    The zero polynomial is an error, not an empty complete root list.
    """
    integer(bits, 2, 128, "field bits")
    coefficients = tuple(coefficients)
    if len(coefficients) > 4097:
        raise ValueError("polynomial degree cap exceeded")
    for c in coefficients:
        integer(c, 0, (1 << bits)-1, "coefficient")
    ring = fq_default_poly_ctx(field(bits))
    y = ring.gen()
    f = ring([element(bits, c) for c in coefficients])
    if f.is_zero():
        raise ValueError("zero polynomial does not have a bounded root list")
    stats = {"modular_squarings": 0, "gcd_calls": 0, "basis_cuts": 0}
    if f.degree() == 0:
        return [], stats
    power = y % f
    for _ in range(bits):
        power = power*power % f
        stats["modular_squarings"] += 1
    split = f.gcd(power-y).monic()
    stats["gcd_calls"] += 1
    pieces = [split] if split.degree() > 0 else []
    for bit in range(bits):
        if all(p.degree() == 1 for p in pieces):
            break
        term = (y*element(bits, 1 << bit)) % split
        trace = ring.zero()
        for j in range(bits):
            trace = (trace+term) % split
            if j+1 < bits:
                term = term*term % split
                stats["modular_squarings"] += 1
        children = []
        for p in pieces:
            if p.degree() == 1:
                children.append(p)
                continue
            zero = p.gcd(trace).monic()
            stats["gcd_calls"] += 1
            one = p.exact_division(zero).monic()
            children.extend(g for g in (zero, one) if g.degree() > 0)
        pieces = children
        stats["basis_cuts"] += 1
    if any(p.degree() != 1 for p in pieces):
        raise ArithmeticError("public trace basis failed to separate distinct roots")
    roots = sorted(encoded(-p[0]/p[1]) for p in pieces)
    check_root_completeness(f, [element(bits, r) for r in roots], bits)
    return roots, stats


def _terms(bits, terms):
    integer(bits, 2, 128, "field bits")
    result = {}
    for (i, j), c in terms.items():
        integer(i, 0, 100_000, "X degree")
        integer(j, 0, 4096, "Y degree")
        integer(c, 0, (1 << bits)-1, "coefficient")
        if c:
            result[i, j] = element(bits, c)
    if not result:
        raise ValueError("nonzero bivariate polynomial required")
    return result


def _normalize(terms):
    terms = {p: c for p, c in terms.items() if c != 0}
    if not terms:
        raise ArithmeticError("injective substitution unexpectedly vanished")
    valuation = min(i for i, _ in terms)
    return {(i-valuation, j): c for (i, j), c in terms.items()}, valuation


def _specialization(bits, terms):
    ring = fq_default_poly_ctx(field(bits))
    degree = max(j for i, j in terms if i == 0)
    return ring([terms.get((0, j), field(bits).zero()) for j in range(degree+1)])


def _child(bits, terms, root):
    gamma, zero = element(bits, root), field(bits).zero()
    result = {}
    for (i, j), c in terms.items():
        for r in range(j+1):
            if r & j == r:  # Lucas parity: binom(j,r) is odd.
                key = i+r, r
                result[key] = result.get(key, zero)+c*gamma**(j-r)
    return _normalize(result)


def _substitute(bits, terms, coefficients):
    ring = fq_default_poly_ctx(field(bits))
    x, f = ring.gen(), ring([element(bits, c) for c in coefficients])
    result = ring.zero()
    for (i, j), c in terms.items():
        result += c*x**i*f**j
    return result


def polynomial_roots(bits, terms, coefficient_count):
    """All f(X), deg f<K, with Q(X,f(X))=0; bounded-width RR tree.

    No early stop when Q(X,0)=0: another root may share that entire prefix.
    The specialization-degree ledger proves a width bound on EVERY input,
    not an average branching heuristic. Root work is polynomial in n and Q.
    """
    integer(coefficient_count, 1, 4096, "coefficient count")
    original = _terms(bits, terms)
    normalized, _ = _normalize(original)
    y_degree = max(j for _, j in original)
    x_bound = max(i for i, _ in original)+coefficient_count*y_degree
    level = [((), normalized)]
    widths, budgets, root_calls = [1], [], 0
    for depth in range(coefficient_count):
        budget = sum(_specialization(bits, q).degree() for _, q in level)
        budgets.append(budget)
        if budget > y_degree:
            raise ArithmeticError("RR specialization-degree budget increased")
        children = []
        for prefix, q in level:
            specialization = _specialization(bits, q)
            roots, _ = linear_roots(bits, map(encoded, specialization.coeffs()))
            root_calls += 1
            for root in roots:
                child, valuation = _child(bits, q, root)
                quotient, multiplicity = specialization, 0
                factor = fq_default_poly_ctx(field(bits)).gen()+element(bits, root)
                while quotient.degree() > 0 and quotient(element(bits, root)) == 0:
                    quotient = quotient.exact_division(factor)
                    multiplicity += 1
                child_degree = _specialization(bits, child).degree()
                if not child_degree <= valuation <= multiplicity:
                    raise ArithmeticError("RR child exceeds root multiplicity budget")
                if max(i for i, _ in child) > x_bound:
                    raise ArithmeticError("RR X-degree cap exceeded")
                children.append((prefix+(root,), child))
        level = children
        widths.append(len(level))
        if len(level) > y_degree:
            raise ArithmeticError("RR width cap exceeded")
    roots = sorted(prefix for prefix, _ in level if _substitute(bits, original, prefix).is_zero())
    if len(roots) > y_degree or len(set(roots)) != len(roots):
        raise ArithmeticError("polynomial root count/uniqueness failed")
    return roots, {"Y_degree": y_degree, "X_degree_cap": x_bound,
                   "level_widths": widths, "specialization_degree_budgets": budgets,
                   "visited_nodes": sum(widths), "node_cap": 1+coefficient_count*y_degree,
                   "root_calls": root_calls, "all_roots_verified": True}


def gs_layout(length, dimension, radius):
    integer(length, 2, 100_000, "length")
    integer(dimension, 2, length-1, "decoder dimension")
    integer(radius, 0, length-1, "radius")
    agreement = length-radius
    gap = agreement*agreement-length*(dimension-1)
    if gap <= 0:
        raise ValueError("strict Johnson agreement required")
    multiplicity = length*(dimension-1)//gap+1
    degree = multiplicity*agreement-1
    y_degree = degree//(dimension-1)
    columns = (y_degree+1)*(degree+1)-(dimension-1)*y_degree*(y_degree+1)//2
    rows = length*multiplicity*(multiplicity+1)//2
    if columns <= rows:
        raise ArithmeticError("GS interpolation has no certified nullspace")
    return {"multiplicity": multiplicity, "weighted_degree": degree,
            "Y_degree_cap": y_degree, "interpolation_rows": rows,
            "interpolation_columns": columns,
            "rr_node_cap": 1+dimension*y_degree,
            "rr_X_degree_cap": degree+dimension*y_degree}


def _nullvector(bits, matrix, columns):
    rows, pivots, pivot_row = [row[:] for row in matrix], [], 0
    for col in range(columns):
        pivot = next((r for r in range(pivot_row, len(rows)) if rows[r][col] != 0), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inv = rows[pivot_row][col]**-1
        rows[pivot_row] = [v*inv for v in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][col] != 0:
                multiplier = rows[r][col]
                rows[r] = [u-multiplier*v for u, v in zip(rows[r], rows[pivot_row])]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    free = next(j for j in range(columns) if j not in pivots)
    vector = [field(bits).zero() for _ in range(columns)]
    vector[free] = field(bits).one()
    for r, col in enumerate(pivots):
        vector[col] = -rows[r][free]
    if any(sum((a*b for a, b in zip(row, vector)), field(bits).zero()) != 0 for row in matrix):
        raise ArithmeticError("interpolation nullspace failed exact check")
    return vector


def decode(bits, points, dimension, received, radius):
    """Complete canonical list, with a CAPPED dense interpolation reference.

    Large q is allowed. Large interpolation matrices are not run here; the
    deterministic polynomial algorithm and reversible schedule are in the note.
    """
    integer(bits, 2, 128, "field bits")
    points, received = tuple(points), tuple(received)
    if len(set(points)) != len(points) or len(received) != len(points):
        raise ValueError("distinct points and aligned received symbols required")
    for c in points+received:
        integer(c, 0, (1 << bits)-1, "field element")
    integer(dimension, 1, len(points)-1, "decoder dimension")
    integer(radius, 0, len(points)-1, "radius")
    if dimension == 1:
        counts = Counter(received)
        roots = [(c,) for c in sorted(counts) if len(points)-counts[c] <= radius]
        return roots, {"repetition_code_direct": True}
    layout = gs_layout(len(points), dimension, radius)
    if layout["interpolation_rows"]*layout["interpolation_columns"] > 65_536:
        raise ValueError("dense interpolation reference cap exceeded; no native large decoder run")
    s, degree = layout["multiplicity"], layout["weighted_degree"]
    monomials = [(i, j) for j in range(layout["Y_degree_cap"]+1)
                 for i in range(degree-(dimension-1)*j+1)]
    matrix = []
    for a, z in zip(points, received):
        alpha, value = element(bits, a), element(bits, z)
        for r in range(s):
            for t in range(s-r):
                matrix.append([alpha**(i-r)*value**(j-t) if r & i == r and t & j == t
                               else field(bits).zero() for i, j in monomials])
    vector = _nullvector(bits, matrix, len(monomials))
    interpolation = {m: encoded(c) for m, c in zip(monomials, vector) if c != 0}
    roots, ledger = polynomial_roots(bits, interpolation, dimension)
    ring = fq_default_poly_ctx(field(bits))
    kept = []
    for coefficients in roots:
        f = ring([element(bits, c) for c in coefficients])
        if sum(encoded(f(element(bits, a))) != z for a, z in zip(points, received)) <= radius:
            kept.append(coefficients)
    return kept, {"layout": layout, "rr": ledger,
                  "interpolation_terms": [[i, j, c] for (i, j), c in sorted(interpolation.items())],
                  "algebraic_roots_before_distance_filter": len(roots),
                  "complete_list_claim": "KNOWN_GS_RR_THEOREM_WITH_VERIFIED_INTERPOLANT",
                  "random_factorization_used": False, "field_table_enumerated": False,
                  "coherent_receiver_executed": False}


def exhaustive_decoder_control(bits, length, dimension, radius):
    """Independent complete code list comparison for EVERY received word."""
    if bits < 2 or bits > 4 or (1 << bits)**(length+dimension) > 8192:
        raise ValueError("exponential complete-list control cap exceeded")
    ring = fq_default_poly_ctx(field(bits))
    points = tuple(range(length))
    code = []
    for coefficients in product(range(1 << bits), repeat=dimension):
        f = ring([element(bits, c) for c in coefficients])
        code.append((coefficients, tuple(encoded(f(element(bits, a))) for a in points)))
    histogram = Counter()
    erased = 0
    for z in product(range(1 << bits), repeat=length):
        expected = sorted(c for c, word in code if sum(a != b for a, b in zip(z, word)) <= radius)
        actual, _ = decode(bits, points, dimension, z, radius)
        if actual != expected:
            raise ArithmeticError("decoder disagrees with exhaustive complete list")
        histogram[len(actual)] += 1
        if len(actual) == 1:
            # On every retained input pair (z,d), XOR-erasure must clear d.
            for c, word in code:
                if sum(a != b for a, b in zip(z, word)) <= radius:
                    if any(a ^ b for a, b in zip(c, actual[0])):
                        raise ArithmeticError("singleton erasure did not clear the true message")
                    erased += 1
    return {"bits": bits, "length": length, "dimension": dimension, "radius": radius,
            "received_words_checked": (1 << bits)**length,
            "list_size_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "retained_pairs_erased_exactly": erased,
            "exhaustive_reference_not_scalable": True}


def large_field_control(bits):
    """Small N, large n, planted decoder regression; no quantum evidence."""
    q, points = 1 << bits, tuple(range(7))
    message = (q//3, q//5)
    ring = fq_default_poly_ctx(field(bits))
    f = ring([element(bits, c) for c in message])
    received = [encoded(f(element(bits, a))) for a in points]
    for i in range(3):
        received[i] ^= 1 << i
    decoded, ledger = decode(bits, points, 2, received, 3)
    if message not in decoded:
        raise ArithmeticError("large-field planted message was omitted")
    return {"bits": bits, "points": list(points), "received": received,
            "field_modulus": list(map(int, field(bits).modulus().coeffs())),
            "planted_message": list(message), "decoded_messages": list(map(list, decoded)),
            "ledger": ledger, "native_large_code_executed": False,
            "planted_decoder_regression_only": True}


def report():
    return {"status": "KNOWN_DETERMINISTIC_BINARY_GS_BACKEND_NOT_COMPILED_QUANTUM_RECEIVER",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/BINARY_GS_DECODER.md").read_bytes()).hexdigest(),
            "random_factorization_required": False, "coherent_receiver_implemented": False,
            "quantum_speedup_established": False,
            "complete_list_controls": [exhaustive_decoder_control(*p) for p in ((2, 3, 1, 1), (2, 3, 2, 1), (2, 4, 2, 1))],
            "large_field_controls": [large_field_control(n) for n in (17, 31, 61)],
            "native_layouts_not_executed": [{"bits": n, **gs_layout(n*n, n*n//8, 3*n*n//5)} for n in (17, 31, 61)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = report()
    if args.write:
        REPORT.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"status": data["status"], "complete_list_controls": data["complete_list_controls"],
                      "large_fields": [r["bits"] for r in data["large_field_controls"]],
                      "native_layouts_not_executed": data["native_layouts_not_executed"]}, indent=2))


if __name__ == "__main__":
    main()
