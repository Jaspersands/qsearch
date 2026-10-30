"""Exact controls for the independent multibasis review; not a general solver."""

import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import comb, log2
from pathlib import Path
from random import Random


ROOT = Path(__file__).resolve().parent
P = 1019
NATIVE = ROOT.parent / "small-prime-tower-2026-10-27/receipt.json"


def basis_columns(matrix, candidates, p):
    echelon = {}
    chosen = []
    for j in candidates:
        vector = [row[j] % p for row in matrix]
        for pivot, prior in sorted(echelon.items()):
            a = vector[pivot]
            if a:
                vector = [(x - a*y) % p for x, y in zip(vector, prior)]
        pivot = next((i for i, x in enumerate(vector) if x), None)
        if pivot is not None:
            inverse = pow(vector[pivot], -1, p)
            echelon[pivot] = [x*inverse % p for x in vector]
            chosen.append(j)
    return chosen


def matvec(matrix, vector, p):
    return [sum(a*x for a, x in zip(row, vector)) % p for row in matrix]


def systematic_control(matrix, syndrome, pivots, seed):
    """Bounded rejection only to verify finite countercontrols have witnesses."""
    p, k, m = P, len(matrix), len(matrix[0])
    augmented = [row[:] + [s] for row, s in zip(matrix, syndrome)]
    for i, column in enumerate(pivots):
        pivot = next(j for j in range(i, k) if augmented[j][column])
        augmented[i], augmented[pivot] = augmented[pivot], augmented[i]
        inverse = pow(augmented[i][column], -1, p)
        augmented[i] = [x*inverse % p for x in augmented[i]]
        for j in range(k):
            if j != i and augmented[j][column]:
                a = augmented[j][column]
                augmented[j] = [(x-a*y) % p for x, y in
                                zip(augmented[j], augmented[i])]
    free = sorted(set(range(m)) - set(pivots))
    rng = Random(seed)
    for trial in range(1, 101):
        word = [0]*m
        for j in free:
            word[j] = rng.randrange(1, p)
        for i, j in enumerate(pivots):
            word[j] = (augmented[i][-1] -
                       sum(augmented[i][t]*word[t] for t in free)) % p
        if all(word):
            assert matvec(matrix, word, p) == syndrome
            return {"trial": trial, "witness": word, "verified": True}
    raise AssertionError("finite control rejection cap exhausted; not UNSAT")


def rs_control(e):
    k, m, delta = 5*e+3, 22*e, 12*e-3
    n = 17*e-2
    assert n <= P
    matrix = [[pow(t, i, P) for t in range(n)] +
              [int(i == k-1)]*(m-n) for i in range(k)]
    bases = [list(range(j*k, (j+1)*k)) for j in range(3)]
    assert all(len(basis_columns(matrix, b, P)) == k for b in bases)
    assert n < 4*(k-1)
    polynomial = [1]
    for root in range(k-2):
        new = [0]*(len(polynomial)+1)
        for i, a in enumerate(polynomial):
            new[i] = (new[i]-root*a) % P
            new[i+1] = (new[i+1]+a) % P
        polynomial = new
    polynomial += [0]*(k-len(polynomial))
    codeword = [sum(polynomial[i]*matrix[i][j] for i in range(k)) % P
                for j in range(m)]
    assert sum(x != 0 for x in codeword) == delta
    answer = {
        "e": e, "k": k, "m": m, "p": P,
        "matrix_formula": "v(t)=(1,t,...,t^(k-1)), 0<=t<17e-2; then 5e+2 copies of e_(k-1)",
        "three_disjoint_bases": bases,
        "four_basis_obstruction": {"flat_rank": 1, "outside": n,
                                   "required_outside": 4*(k-1)},
        "distance_attaining_polynomial_coefficients": polynomial,
        "distance_attaining_weight": delta,
        "distance_lower_bound": "proved by polynomial root bound in review.md, not enumerated",
        "native_AG_input": False,
    }
    if e == 8:
        pivots = bases[0]
        rest = sorted(set(range(m))-set(pivots))
        syndrome = [sum(row[j] for j in rest) % P for row in matrix]
        partial = [int(j in rest) for j in range(m)]
        assert matvec(matrix, partial, P) == syndrome
        answer["nonextendible_nonzero_prefix"] = {
            "fixed_coordinates": rest, "fixed_value": 1,
            "syndrome": syndrome, "remaining_unique_solution": [0]*k,
            "global_full_support_control": systematic_control(matrix, syndrome, pivots, 7),
        }
    return answer


def native_control():
    raw = NATIVE.read_bytes()
    matrix = json.loads(raw)["native_control"]["original_parity"]
    k, m = len(matrix), len(matrix[0])
    assert (k, m) == (43, 176)
    remaining = list(range(m))
    bases = []
    for _ in range(4):
        basis = basis_columns(matrix, remaining, P)
        assert len(basis) == k
        bases.append(basis)
        remaining = sorted(set(remaining)-set(basis))
    halves = [len(basis_columns(matrix, range(0, m//2), P)),
              len(basis_columns(matrix, range(m//2, m), P))]
    assert halves == [k, k]
    fiber_checks = []
    for fiber in range(11):
        indices = list(range(16*fiber, 16*(fiber+1)))
        rank = len(basis_columns(matrix, indices, P))
        word = [0]*m
        for i, j in enumerate(indices):
            word[j] = (-1 if i % 2 == 0 else 1) % P
        assert rank == 15 and matvec(matrix, word, P) == [0]*k
        fiber_checks.append({"fiber": fiber, "rank": rank,
                             "kernel_dimension": 1, "alternating_word_verified": True})
    return {"source": str(NATIVE), "source_sha256": sha256(raw).hexdigest(),
            "k": k, "m": m, "four_disjoint_bases": bases,
            "leftover": remaining, "half_ranks": halves,
            "independent_fiber_identity_checks": fiber_checks,
            "parent_block_repair_implementation_duplicated": False,
            "source_geometry_reconstructed": False,
            "general_packing_proof": "review.md; finite greedy success is not the proof"}


def arithmetic_controls():
    r = (P-3)//2
    ring_counts = {}
    for copies in (2, 3):
        exponent = copies*r
        coefficients = [0]*P
        for j in range(exponent+1):
            coefficients[j % P] = (coefficients[j % P] +
                                    (-1)**j*comb(exponent, j)) % P
        ring_counts[str(copies)] = sum(x != 0 for x in coefficients)
    assert ring_counts["2"] > 0 and ring_counts["3"] == 0

    polynomial = [1]
    for root in range(P):
        new = [0]*(len(polynomial)+1)
        for i, a in enumerate(polynomial):
            new[i] = (new[i]-root*a) % P
            new[i+1] = (new[i+1]+a) % P
        polynomial = new
    assert polynomial == [0, P-1] + [0]*(P-2) + [1]
    assert all((pow(x, P, P)-x) % P == 0 for x in range(P))

    shifted_squares = {(x*x+1) % P for x in range(P)}
    assert 0 not in shifted_squares and len(shifted_squares) == (P+1)//2
    roots = {x*x % P: x for x in range(P)}
    padding_pair = next((x, roots[(-1-x*x) % P]) for x in range(P)
                        if (-1-x*x) % P in roots)
    assert (1+sum(x*x for x in padding_pair)) % P == 0
    assert 4**22 < P**5

    e = 512
    k, m = 5*e+3, 22*e
    row_bad = Fraction(2**m, P**(5*e+1))
    kernel_bad = Fraction((P-1)*(m*(P-1))**(P-1), P**k)
    assert row_bad + kernel_bad < 1
    return {
        "group_ring_nonzero_coefficient_counts": ring_counts,
        "line_polynomial": "product_(a in F_1019)(T-a)=T^1019-T; checked coefficientwise",
        "shifted_square_image_size": len(shifted_squares),
        "invalid_sum_of_squares_padding_pair": list(padding_pair),
        "four_letter_cardinality_obstruction": "4^22 < 1019^5; exact integer check",
        "generic_no_short_kernel_existence": {
            "e": e, "k": k, "m": m, "minimum_kernel_weight_at_least": P,
            "row_bad_log2_upper": log2(row_bad.numerator)-log2(row_bad.denominator),
            "kernel_bad_log2_upper": log2(kernel_bad.numerator)-log2(kernel_bad.denominator),
            "sum_less_than_one_checked_exactly": True, "matrix_constructed": False,
        },
    }


def diagonal_controls():
    records = []
    for p in (3, 7):
        columns = [(1, a) for a in range(p)] + [(0, 1)]
        if p == 3:
            columns *= 2
        matrix = [[c[i] for c in columns] for i in range(2)]
        delta = min(sum(x != 0 for x in
                        [sum(a*b for a, b in zip(u, c)) % p for c in columns])
                    for u in product(range(p), repeat=2) if any(u))
        assert delta > 4
        counts = {(0, 0): 1}
        for column in columns:
            new = defaultdict(int)
            for syndrome, count in counts.items():
                for x in range(p):
                    target = tuple((a+b*x*x) % p for a, b in zip(syndrome, column))
                    new[target] += count
            counts = dict(new)
        assert len(counts) == p*p and min(counts.values()) > 0
        assert sum(counts.values()) == p**len(columns)
        records.append({"p": p, "k": 2, "m": len(columns), "delta": delta,
                        "minimum_diagonal_fiber_count": min(counts.values()),
                        "all_syndromes_present": True,
                        "native_AG_input": False})
    return records


def report():
    return {
        "status": "EXACT_CONTROLS_NOT_A_GENERAL_EXTRACTOR",
        "generic_three_bases_not_four": [rs_control(e) for e in (8, 16, 32)],
        "native_e8_four_bases": native_control(),
        "arithmetic": arithmetic_controls(),
        "small_diagonal_systems": diagonal_controls(),
        "stationary_walk_and_native_source_parent_controls_duplicated": False,
        "uniform_sampler_claimed": False, "quantum_advantage_claimed": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write and args.check:
        parser.error("choose --write or --check")
    result = report()
    output = ROOT / "countercontrols.json"
    if args.write:
        output.write_text(json.dumps(result, indent=2)+"\n")
    elif args.check:
        assert json.loads(output.read_text()) == result
    else:
        print(json.dumps(result, indent=2))
    print("PASS: three RS obstructions; native four bases; pinning, group-ring, PIT, alphabet, and quadratic controls.")
