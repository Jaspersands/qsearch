"""Independent exact controls. Run with python -B; outputs stay beside this file.

Geometry and elimination are implemented here, without parent helpers. Parent
imports occur only after the independent construction, for comparison.
"""

from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement, product
from math import comb, isqrt, prod
from pathlib import Path
import json
import sys


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PARENT = BASE / "small-prime-tower-2026-10-27"
P = 1019
A = (63, 66, 86, 98, 105, 107, 188, 554, 570, 578, 673, 773, 866)
XS = (0, 468, 568, 571, 614, 634, 696, 882, 926, 942, 965)
E_INDICES = (0, 3, 5, 9, 14)
FULL = (1 << 13) - 1
# Generate the character group from the four defining equations.
GENERATORS = (3, 5, 9, FULL)
MASKS = sorted({a ^ b ^ c ^ d for a in (0, 3) for b in (0, 5)
                for c in (0, 9) for d in (0, FULL)})
ROOTS = {}
for r in range(P):
    ROOTS.setdefault(r*r % P, r)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def dec(value):
    with localcontext() as ctx:
        ctx.prec = 24
        return str(Decimal(value.numerator) / Decimal(value.denominator))


class RowSpace:
    """Plain-Python modular echelon basis, independent of FLINT elimination."""

    def __init__(self, p=P):
        self.p = p
        self.rows = {}
        self.labels = []

    def add(self, vector, label=None):
        v = [x % self.p for x in vector]
        for j, row in sorted(self.rows.items()):
            if v[j]:
                c = v[j]
                v[j:] = [(a-c*b) % self.p for a, b in zip(v[j:], row[j:])]
        j = next((i for i, x in enumerate(v) if x), None)
        if j is None:
            return False
        inverse = pow(v[j], -1, self.p)
        self.rows[j] = [x*inverse % self.p for x in v]
        self.labels.append(label)
        return True

    def reduced(self):
        entries = sorted((j, row[:]) for j, row in self.rows.items())
        for index in range(len(entries)-1, -1, -1):
            j, row = entries[index]
            for _, earlier in entries[:index]:
                c = earlier[j]
                if c:
                    earlier[j:] = [(a-c*b) % self.p for a, b in zip(earlier[j:], row[j:])]
        return [row for _, row in entries], [j for j, _ in entries]


def reduce_rows(data, p=P):
    space = RowSpace(p)
    for row in data:
        space.add(row)
    return space.reduced()


def nullspace(data):
    reduced, pivots = reduce_rows(data)
    free = [j for j in range(len(data[0])) if j not in pivots]
    output = []
    for j in free:
        row = [0]*len(data[0])
        row[j] = 1
        for pivot, equation in zip(pivots, reduced):
            row[pivot] = -equation[j] % P
        assert all(sum(a*b for a, b in zip(row, constraint)) % P == 0
                   for constraint in data)
        output.append(row)
    return output, len(pivots)


def mul2(a, b):
    return ((a[0]*b[0] + 2*a[1]*b[1]) % P,
            (a[0]*b[1] + a[1]*b[0]) % P)


def inv2(a):
    inverse = pow((a[0]*a[0]-2*a[1]*a[1]) % P, -1, P)
    return (a[0]*inverse % P, -a[1]*inverse % P)


def sqrt2(a):
    # All base-field elements have square roots in F_p[theta]/(theta^2-2).
    a %= P
    if a in ROOTS:
        return ROOTS[a], 0
    return 0, ROOTS[a*pow(2, -1, P) % P]


def fiber(x, parent_order=False):
    if x in A:
        return []
    radicands = [(x-A[0])*(x-A[i]) % P for i in (1, 2, 3)]
    radicands.append(prod(x-a for a in A) % P)
    if not all(a in ROOTS and a != 0 for a in radicands):
        return []
    roots = [pow(a, (P+1)//4, P) if parent_order else ROOTS[a] for a in radicands]
    return [(x, *(sign*r % P for sign, r in zip(signs, roots)))
            for signs in product((1, -1), repeat=4)]


@lru_cache(maxsize=None)
def radical_values(point):
    # Lift to the full elementary cover over F_p^2, then multiply roots.
    # This avoids the parent's denominator-exponent formula entirely.
    x, w1, w2, w3, y = point
    roots = [sqrt2(x-A[0])]
    roots += [mul2((w, 0), inv2(roots[0])) for w in (w1, w2, w3)]
    roots += [sqrt2(x-a) for a in A[4:12]]
    total = (1, 0)
    for r in roots:
        total = mul2(total, r)
    roots.append(mul2((y, 0), inv2(total)))
    assert all(mul2(r, r) == ((x-a) % P, 0) for r, a in zip(roots, A))
    values = {}
    for mask in MASKS:
        value = (1, 0)
        for j, r in enumerate(roots):
            if mask >> j & 1:
                value = mul2(value, r)
        assert value[1] == 0, "a cover character failed descent to F_p"
        values[mask] = value[0]
    return values


def monomials(bound):
    return [(mask, j) for mask in MASKS for j in range(bound//2+1)
            if 2*j + mask.bit_count() <= bound]


def evaluate(function, point):
    mask, j = function
    return pow(point[0], j, P)*radical_values(point)[mask] % P


def convolve(a, b, length):
    return [sum(a[j]*b[i-j] for j in range(i+1)
                if j < len(a) and i-j < len(b)) % P for i in range(length)]


def jet(function, point, length):
    mask, j = function
    x = point[0]
    radicand = [1] + [0]*(length-1)
    for i, a in enumerate(A):
        if mask >> i & 1:
            radicand = convolve(radicand, [(x-a) % P, 1], length)
    z = [radical_values(point)[mask]]
    for n in range(1, length):
        known = sum(z[i]*z[n-i] for i in range(1, n))
        z.append((radicand[n]-known)*pow(2*z[0], -1, P) % P)
    assert convolve(z, z, length) == radicand
    xj = [comb(j, n)*pow(x, j-n, P) % P if n <= j else 0
          for n in range(length)]
    return convolve(xj, z, length)


def combine(basis, evaluations):
    return [[sum(c*row[j] for c, row in zip(coefficients, evaluations)) % P
             for j in range(len(evaluations[0]))] for coefficients in basis]


def geometric_code(t, points, zeros):
    functions = monomials(11*t)
    constraints = []
    for point in zeros:
        jets = [jet(f, point, t) for f in functions]
        constraints += [[value[n] for value in jets] for n in range(t)]
    basis, rank = nullspace(constraints)
    evaluation = [[evaluate(f, point) for point in points] for f in functions]
    code = combine(basis, evaluation)
    reduced, pivots = reduce_rows(code)
    return {"t": t, "monomial_count": len(functions), "jet_rank": rank,
            "rr_dimension": len(basis), "evaluation_rank": len(pivots),
            "functions": functions, "constraints": constraints,
            "basis": basis, "matrix": code, "rref": reduced}


def prime_bound(e):
    g, d = 5*e+1, 10*e+3
    return (Fraction(9**g*g, P**(3*e+9)*30**2)
            * Fraction(2*d*P, P-1) * Fraction(33**2, P)**g)


def bounds(e):
    g, d, k, m, w = 5*e+1, 10*e+3, 5*e+3, 22*e, 15*e+6
    error = Fraction((P**k-1)*P**w, (P-1)**m)
    tail = Fraction(P**k-1, (P-1)**(m-d))
    raw = (1-error)**2/(1+tail)
    systematic = Fraction(P-1, P)**k*(1-tail)
    coarse = Fraction(P**9*2**e, P**(2*e))
    ratio = Fraction(4*9**5, P**3)*Fraction(33**2, P)**5
    bad = prime_bound(e)
    assert 0 < error < coarse < 1
    assert 0 < bad < Fraction(8247, 10**62)
    assert prime_bound(e+1)/bad < ratio < Fraction(312, 10**6)
    assert P**d >= 4*(g+1)**2*(d+6)**2
    assert 0 < tail < error
    return {"e": e, "g": g, "d": d, "k": k, "m": m, "w": w,
            "error": error, "tail": tail, "raw": raw,
            "systematic": systematic, "bad_prime": bad, "ratio": ratio}


def deterministic_witnesses(matrix):
    k, m = len(matrix), len(matrix[0])
    augmented = [row + [int(i == j) for j in range(k)] for i, row in enumerate(matrix)]
    reduced, pivots = reduce_rows(augmented)
    assert len(pivots) == k and max(pivots) < m
    free = [j for j in range(m) if j not in pivots]
    buckets = [[] for _ in free]
    for i, row in enumerate(reduced):
        nonzero = [j for j, col in enumerate(free) if row[col]]
        assert nonzero
        buckets[nonzero[-1]].append(i)
    targets = [[0]*k, [1]*k, list(range(k))]
    targets += [[int(i == j) for i in range(k)] for j in range(k)]
    witnesses = []
    for target in targets:
        rhs = [sum(a*b for a, b in zip(row[m:], target)) % P for row in reduced]
        word = [0]*m
        for j, col in enumerate(free):
            forbidden = {0}
            for i in buckets[j]:
                prior = sum(reduced[i][c]*word[c] for c in free[:j])
                forbidden.add((rhs[i]-prior)*pow(reduced[i][col], -1, P) % P)
            word[col] = next(a for a in range(1, k+2) if a not in forbidden)
        for i, col in enumerate(pivots):
            word[col] = (rhs[i]-sum(reduced[i][c]*word[c] for c in free)) % P
        assert all(word)
        assert [sum(a*b for a, b in zip(row, word)) % P for row in matrix] == target
        witnesses.append({"syndrome": target, "word": word})
    return {"target_count": len(targets), "largest_bucket": max(map(len, buckets)),
            "free_columns": free, "pivot_columns": pivots, "witnesses": witnesses}


def run():
    sys.dont_write_bytecode = True
    sources = [PARENT / name for name in ("small_prime.py", "seed_search.py", "RESULT.md",
                                          "avoidance.py", "test_small_prime.py")]
    sources += [BASE / name for name in (
        "prime-ag-tower-source-2026-10-26/TOWER_SOURCE.md",
        "ag-divisor-class-control-2026-10-26/CONTROL.md",
        "generic-divisor-class-2026-10-26/GENERIC_CLASSES.md",
        "constructive-tower-2026-10-27/PRIME_CLASS.md",
        "constructive-tower-2026-10-27/SOURCE.md",
        "constructive-tower-2026-10-27/ARITHMETIC.md",
        "constructive-tower-2026-10-27/REVIEW_RESOLUTION.md",
        "unambiguous-reduction-2026-10-26/USD_REDUCTION.md",
        "usd-review-resolution-2026-10-26/RESOLUTION.md")]
    hashes = {str(path): sha256(path.read_bytes()).hexdigest() for path in sources}
    assert all(P % divisor for divisor in range(2, isqrt(P)+1))
    assert pow(2, (P-1)//2, P) == P-1
    assert len(set(A)) == 13 and len(set(XS)) == 11 and not set(A) & set(XS)
    seed_roots = [[ROOTS[(x-a) % P] for a in A] for x in XS]
    assert all(r and r*r % P == (x-a) % P for x, roots in zip(XS, seed_roots)
               for a, r in zip(A, roots))
    all_split = [x for x in range(P) if all((x-a) % P in ROOTS and x != a for a in A)]
    split_cover = [x for x in range(P) if fiber(x)]
    extra_x = next(x for x in split_cover if x not in XS)
    assert extra_x == 6
    nonsquare_extra_indices = [i for i, a in enumerate(A) if (extra_x-a) % P not in ROOTS]
    assert nonsquare_extra_indices
    assert len({i in nonsquare_extra_indices for i in range(4)}) == 1
    points = [point for x in XS for point in fiber(x, parent_order=True)]
    zeros = [fiber(extra_x, parent_order=True)[j] for j in E_INDICES]
    assert len(set(points)) == 176 and len(set(zeros)) == 5 and not set(points) & set(zeros)
    squareclass_vectors = [[int(j == i) for j in range(13)] for i in range(13)]
    assert len(reduce_rows(squareclass_vectors, 2)[1]) == 13
    assert len(MASKS) == 16 and len({min(mask, mask ^ FULL) for mask in MASKS}) == 8
    assert sum((mask.bit_count()-1)//2 for mask in MASKS if mask) == 41
    assert (12-2)**2-4*(23+1) == 4
    low_masks = [mask for mask in MASKS if mask < 16]
    infinity_characters = [[prod(signs[i-1] for i in (1, 2, 3) if mask >> i & 1) % P
                            for mask in low_masks] for signs in product((1, -1), repeat=3)]
    assert len(reduce_rows(infinity_characters)[1]) == 8
    assert monomials(1) == [(0, 0)]
    small_constraints = [[evaluate(f, point) for f in monomials(1)] for point in zeros]
    assert len(nullspace(small_constraints)[0]) == 0
    seed = {"prime": P, "square_roots": seed_roots, "all_fully_split_x": all_split,
            "all_unramified_split_cover_x": split_cover, "extra_x": extra_x,
            "genus": 6, "cover_genus": 41, "kummer_rank": 12,
            "extra_x_nonsquare_branch_indices": nonsquare_extra_indices,
            "infinity_character_rank": 8, "dimension_L_G_minus_K": 0,
            "split_places": 23, "schoof_squared_margin": 4,
            "character_weight_histogram": dict(Counter(mask.bit_count() for mask in MASKS))}
    print("Seed and independent F_p^2 lift: PASS", flush=True)

    codes = [geometric_code(t, points, zeros) for t in (1, 2, 3)]
    expected = [(48, 5, 43, 43), (136, 10, 126, 126), (224, 15, 209, 176)]
    for code, claim in zip(codes, expected):
        assert tuple(code[key] for key in ("monomial_count", "jet_rank", "rr_dimension", "evaluation_rank")) == claim
    B = codes[0]["matrix"]
    square = RowSpace()
    for i, j in combinations_with_replacement(range(len(B)), 2):
        square.add([a*b % P for a, b in zip(B[i], B[j])], [i, j])
    square_rows = square.reduced()[0]
    assert square_rows == codes[1]["rref"]
    cube = RowSpace()
    for i, left in enumerate(B):
        for j, right in enumerate(square_rows):
            cube.add([a*b % P for a, b in zip(left, right)], [i, j])
        if len(cube.rows) == 176:
            break
    assert cube.reduced()[0] == codes[2]["rref"]
    assert len(square.rows) == 126 and len(cube.rows) == 176
    assert all(len(reduce_rows([[v for i, v in enumerate(row) if i != col] for row in B])[1]) == 43
               for col in range(176))
    classical = deterministic_witnesses(B)
    print("Jet RR and Schur controls: 43 / 126 / 176; native witnesses:", classical["target_count"], flush=True)

    # Independent normalization/product checks at every unramified split fiber.
    product_checks = 0
    for x in split_cover:
        for point in fiber(x):
            values = radical_values(point)
            for s in MASKS:
                for t in MASKS:
                    factor = prod(x-a for i, a in enumerate(A) if (s & t) >> i & 1) % P
                    assert values[s]*values[t] % P == factor*values[s ^ t] % P
                    product_checks += 1
    assert (P-1)**22 * 2 > P**22
    parameters = [bounds(e) for e in (8, 16, 32, 64, 128, 256, 512, 1024)]
    print("All split-fiber products and exact bound controls: PASS", flush=True)

    sys.path.insert(0, str(PARENT))
    import small_prime as parent
    import avoidance
    assert parent.P == P and parent.BRANCHES == A and parent.SPLITTING_X == XS
    evaluator_checks = 0
    omitted_denominator_failures = 0
    for x in split_cover:
        for point in fiber(x):
            supplied = {"x": x, "w": list(point[1:4]), "y": point[4]}
            for mask in MASKS:
                assert parent.evaluate((mask, 0), supplied) == radical_values(point)[mask]
                evaluator_checks += 1
            if point[1]*point[2] % P != radical_values(point)[6]:
                omitted_denominator_failures += 1
    for function in parent.monomials(11):
        for point in points+zeros:
            supplied = {"x": point[0], "w": list(point[1:4]), "y": point[4]}
            assert parent.evaluate(function, supplied) == evaluate(function, point)
    problem, _, certificate = parent.build_control()
    original = certificate["original_parity"]
    assert reduce_rows(original)[0] == codes[0]["rref"]
    assert (problem.k, problem.m, len(problem.W), len(problem.U)) == (43, 176, 126, 176)
    assert certificate["dimension_L_G_minus_K"] == 0
    for data in parameters:
        other = parent.parameter_bounds(P, data["e"])
        assert other["decoder_error_upper"] == data["error"]
        assert other["raw_verified_quantum_success_lower"] == data["raw"]
        assert other["bad_prime_upper"] == data["bad_prime"]
        assert other["bad_prime_one_degree_ratio_upper"] == data["ratio"]
        assert other["systematic"]["systematic_success_lower"] == data["systematic"]
    targets = [item["syndrome"] for item in classical["witnesses"]]
    parent_witnesses = []
    for target in targets:
        answer = avoidance.solve_native(P, original, target)
        word = answer["witness"]
        assert all(word)
        assert [sum(a*b for a, b in zip(row, word)) % P for row in original] == target
        parent_witnesses.append({"syndrome": target, "word": word})
    # Exhaust all invertible 2x2 matrices and targets in the guaranteed p=5 range.
    avoidance_cases = 0
    for entries in product(range(5), repeat=4):
        a, b, c, d = entries
        if (a*d-b*c) % 5 == 0:
            continue
        for target in product(range(5), repeat=2):
            result = avoidance.greedy_avoid([[a, b], [c, d]], target, 5)
            x, y = result["witness"]
            assert x*y % 5 and (a*x+b*y) % 5 != target[0] and (c*x+d*y) % 5 != target[1]
            avoidance_cases += 1
    unknown = avoidance.greedy_avoid([[1, 1], [0, 1]], [2, 2], 3)
    assert unknown["witness"] is None and not unknown["infeasibility_established"]
    assert all(sha256(path.read_bytes()).hexdigest() == hashes[str(path)] for path in sources)
    output = {"status": "PASS", "source_sha256": hashes, "seed": seed,
              "points": points, "zeros": zeros, "geometric_codes": codes,
              "square_basis_product_labels": square.labels,
              "cube_basis_product_labels": cube.labels,
              "independent_matrix_sha256": digest(B),
              "parent_matrix_sha256": digest(original),
              "parent_original_parity": original,
              "parent_rowspace_equals_independent_rowspace": True,
              "radical_product_checks": product_checks,
              "parent_radical_evaluator_checks": evaluator_checks,
              "omitted_denominator_detected_points": omitted_denominator_failures,
              "all_176_coordinate_deletions_preserve_rank": True,
              "independent_classical": classical, "parent_avoidance_witnesses": parent_witnesses,
              "exhaustive_F5_avoidance_cases": avoidance_cases,
              "bounds": [{key: dec(value) if isinstance(value, Fraction) else value
                           for key, value in item.items()} for item in parameters],
              "bounds_decimal_display_can_round_raw_success_to_one": True,
              "raw_success_strictly_less_than_one_checked_exactly": all(0 < item["raw"] < 1 for item in parameters),
              "e8_exact_bounds": {key: str(value) for key, value in parameters[0].items()},
              "generated_curve_degrees": [8],
              "higher_degree_numbers_are_conditional_forecasts": True,
              "quantum_execution": False, "uniform_Picard_claim": False,
              "parent_tests_run": False, "files_unchanged_at_end": True}
    (HERE / "evidence.json").write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "radical_product_checks": product_checks,
                      "evaluator_checks": evaluator_checks,
                      "avoidance_cases": avoidance_cases,
                      "seed": seed, "bounds": output["bounds"],
                      "source_sha256": hashes}, indent=2))


if __name__ == "__main__":
    run()
