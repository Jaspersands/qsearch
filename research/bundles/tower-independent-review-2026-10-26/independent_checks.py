"""Independent finite checks; no source-bundle construction helpers are used."""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from math import isqrt, prod
from pathlib import Path
import random
import sys
import time

from flint import nmod_mat


ROOT = Path(__file__).resolve().parent
P = 100003
XS = (18501, 29631, 37154, 37155, 40763, 48611, 48612, 48613,
      48614, 48615, 51887)
ALL = frozenset(range(13))
LOW = tuple(frozenset(c) for n in (0, 2, 4) for c in combinations(range(4), n))
CHARS = LOW + tuple(ALL - a for a in LOW)
SIGNS = tuple(product((1, -1), repeat=3))


def rows(a):
    return [[int(a[i, j]) for j in range(a.ncols())] for i in range(a.nrows())]


def row_basis(vectors):
    rr, rank = nmod_mat(vectors, P).rref()
    return rows(rr)[:rank]


def kernel_rows(a):
    k, n = a.nullspace()
    return [[int(k[i, j]) for i in range(a.ncols())] for j in range(n)]


def mod(q):
    return q.numerator * pow(q.denominator, -1, P) % P


@lru_cache(None)
def expansion(char, order):
    # Multiply exact binomial series, independently of the bundle's square-root recursion.
    a = [Fraction(1)] + [Fraction(0)] * order
    for branch in sorted(char):
        b = [Fraction(1)]
        for j in range(1, order + 1):
            b.append(b[-1] * (Fraction(3, 2) - j) * (-branch) / j)
        a = [sum(a[j] * b[n-j] for j in range(n+1)) for n in range(order+1)]
    return tuple(a)


def ambient(bound):
    return [(a, j) for a in CHARS for j in range((bound-len(a))//2+1)]


def coefficient(term, exponent, signs):
    a, j = term
    shift = exponent + len(a) + 2*j
    if shift < 0 or shift % 2:
        return Fraction(0)
    low = a if a in LOW else ALL-a
    sign = prod(signs[i-1] for i in low if i)
    return sign * expansion(a, shift//2)[shift//2]


def build_points():
    result = []
    for x in XS:
        roots = tuple(pow(x-i, (P+1)//4, P) for i in range(13))
        yy = prod(roots) % P
        for y in (yy, -yy % P):
            for signs in SIGNS:
                r = (roots[0],) + tuple(roots[i]*signs[i-1] % P for i in (1, 2, 3))
                result.append((x, y, r))
    return result


POINTS = build_points()


def evaluation(term, point):
    a, j = term
    x, y, r = point
    low = a if a in LOW else ALL-a
    radical = prod(r[i] for i in low) % P
    if a not in LOW:
        radical = y * pow(radical, -1, P) % P
    return pow(x, j, P) * radical % P


def rr_code(bound, other_bound):
    terms = ambient(bound)
    constraints = [[mod(coefficient(t, -pole, signs)) for t in terms]
                   for signs in SIGNS if signs != (1, 1, 1)
                   for pole in range(other_bound+1, bound+1)]
    a = nmod_mat(constraints, P)
    basis = kernel_rows(a)
    ev = nmod_mat([[evaluation(t, pt) for pt in POINTS] for t in terms], P)
    b = row_basis(rows(nmod_mat(basis, P)*ev))
    w = row_basis([[x*y % P for x, y in zip(v, w)]
                   for v, w in combinations_with_replacement(b, 2)])
    u = row_basis([[x*y % P for x, y in zip(v, square)] for v in b for square in w])
    return b, w, u, {"ambient_dimension": len(terms), "jet_rank": a.rank()}


def explicit_f(point):
    x, _, roots = point
    w1, w2, w3 = (roots[0]*roots[i] % P for i in (1, 2, 3))
    return (-66+62*x-36*w1+18*w2-45*w1*w2*pow(x, -1, P)+w3) % P


def solve(b, h, s):
    # Independently implement the prior-art quadratic construction on supp(h).
    support = [i for i, x in enumerate(h) if x]
    t = nmod_mat([[row[i] for i in support] for row in b], P)
    rr, rank = t.rref()
    assert rank == len(b)
    pivots = [next(j for j in range(len(support)) if rr[i, j]) for i in range(rank)]
    weights = [int(j in pivots) for j in range(len(support))]
    inverse4 = pow(4, -1, P)
    offset = [(weights[j]*pow(h[i], -1, P)-2*h[i])*inverse4 % P
              for j, i in enumerate(support)]
    outside = [i for i in range(len(h)) if not h[i]]
    rhs = [2*(s[r]-sum(b[r][i] for i in outside)
              -sum(b[r][i]*offset[j] for j, i in enumerate(support))) % P
           for r in range(rank)]
    a = nmod_mat([[int(t[r, j]) for j in pivots] for r in range(rank)], P)
    z = (a*a.transpose()).solve(nmod_mat([[x] for x in rhs], P))
    linear = t.transpose()*z
    out = [1]*len(h)
    for j, i in enumerate(support):
        v = (int(linear[j, 0])+weights[j]*pow(h[i], -1, P)) % P
        out[i] = h[i]*(v*v-2)*inverse4 % P
    assert all(out)
    assert [sum(a*x for a, x in zip(row, out)) % P for row in b] == list(s)
    return len(support)


def main():
    start = time.monotonic()
    assert all(P % d for d in range(2, isqrt(P)+1))
    assert pow(2, (P-1)//2, P) == P-1
    assert len(set(XS)) == 11
    assert all(pow(x-i, (P-1)//2, P) == 1 for x in XS for i in range(13))
    report = {"prime_trial_division": True, "nonsquare": 2,
              "nonzero_square_checks": 143, "schoof_squared_margin": 4}

    # Squareclasses in F_p(x) have independent branch valuation vectors.
    # Modulo the all-ones class, only empty/full subsets are zero.
    representatives = {min(mask, mask ^ 8191) for mask in range(8192)}
    assert len(representatives) == 4096
    assert len({sum(1 << i for i in a) for a in CHARS}) == 16
    report["kummer_quotient_classes"] = len(representatives)

    f_terms = [(frozenset(), 0), (frozenset(), 1),
               (frozenset((0, 1)), 0), (frozenset((0, 2)), 0),
               (frozenset((1, 2)), 0), (frozenset((0, 3)), 0)]
    fc = [-66, 62, -36, 18, -45, 1]
    orders = {}
    for signs in SIGNS:
        series = {j: sum(c*coefficient(t, j, signs) for c, t in zip(fc, f_terms))
                  for j in range(-2, 13)}
        lead = next(j for j in series if series[j])
        orders[str(signs)] = {"order": lead, "leading_rational": str(series[lead]),
                             "leading_mod_p": mod(series[lead])}
        assert lead >= -2
        if signs == (1, 1, 1):
            assert lead == 8 and series[lead] == Fraction(-27, 32)
    report["explicit_f_infinity"] = orders

    b, w, u, info = rr_code(13, 10)
    ann = kernel_rows(nmod_mat(u, P))
    assert (len(b), len(w), len(u), len(ann)) == (43, 126, 173, 3)
    h = [explicit_f(pt)*pow(pt[1]*prod(pt[0]-x for x in XS if x != pt[0]), -1, P) % P
         for pt in POINTS]
    assert all(h)
    assert all(sum(a*x for a, x in zip(row, h)) % P == 0 for row in u)
    info.update(rank=len(b), length=len(POINTS), square_rank=len(w),
                cube_rank=len(u), annihilator_dimension=len(ann), analytic_support=sum(bool(x) for x in h))
    report["complete_code"] = info
    receipt = json.loads((ROOT / "snapshot/prime-ag-tower-source-2026-10-26/receipt.json").read_text())
    source_b = receipt["actual_degree_eight_code"]["original_parity"]
    assert len(row_basis(b+source_b)) == 43
    assert h == receipt["actual_degree_eight_code"]["analytic_annihilator"]["annihilator"]
    report["matches_source_receipt_row_space_and_residues"] = True

    # Check equality with an independently built L(3G) evaluation, not just rank <=.
    terms = ambient(39)
    constraints = nmod_mat([[mod(coefficient(t, -pole, signs)) for t in terms]
                            for signs in SIGNS if signs != (1, 1, 1)
                            for pole in range(31, 40)], P)
    cube_functions = kernel_rows(constraints)
    ev3 = nmod_mat([[evaluation(t, pt) for pt in POINTS] for t in terms], P)
    ev3 = rows(nmod_mat(cube_functions, P)*ev3)
    assert len(cube_functions) == 209
    assert len(row_basis(ev3)) == len(row_basis(ev3+u)) == 173
    report["L3G"] = {"function_dimension": 209, "evaluation_rank": 173,
                     "evaluation_kernel_dimension": 36, "equals_schur_cube": True}

    # Geometric annihilators are exactly residues of L(2I-9R).
    low_terms = ambient(2)
    jets = nmod_mat([[mod(coefficient(t, j, (1, 1, 1))) for t in low_terms]
                    for j in range(-2, 7)], P)
    low_kernel = kernel_rows(jets)
    residues = [[sum(c*evaluation(t, pt) for c, t in zip(cs, low_terms))
                 * pow(pt[1]*prod(pt[0]-x for x in XS if x != pt[0]), -1, P) % P
                 for pt in POINTS] for cs in low_kernel]
    assert len(low_kernel) == len(row_basis(residues)) == len(row_basis(residues+ann)) == 3
    report["geometric_annihilator_equals_matrix_kernel"] = True

    rng = random.Random(20261026)
    targets = [[0]*43, [1]*43, list(range(43))]
    targets += [[int(i == j) for i in range(43)] for j in range(43)]
    targets += [[rng.randrange(P) for _ in range(43)] for _ in range(32)]
    annihilators = [h]+ann
    # Enforce a zero coordinate by a nontrivial combination of two kernel rows.
    for a, c in combinations(ann, 2):
        at = next(i for i in range(176) if a[i] or c[i])
        h0 = [(c[at]*x-a[at]*y) % P for x, y in zip(a, c)]
        assert any(h0) and not h0[at]
        annihilators.append(h0)
    supports = []
    for vector in annihilators:
        assert all(sum(x*y for x, y in zip(row, vector)) % P == 0 for row in u)
        supports.append(sum(bool(x) for x in vector))
        assert supports[-1] >= 169
        for target in targets:
            solve(b, vector, target)
    report["solver"] = {"targets_per_annihilator": len(targets),
                        "annihilators": len(annihilators), "support_sizes": supports,
                        "witnesses_verified": len(targets)*len(annihilators),
                        "uniform_sampling_claimed": False}

    # 92 low-weight sign patterns in one fibre and one point in another fibre.
    low_chars = [frozenset(c) for n in (0, 1, 2) for c in combinations(range(13), n)]
    full_points = []
    for flips in low_chars:
        x = XS[0]
        roots = [pow(x-i, (P+1)//4, P)*(-1 if i in flips else 1) % P for i in range(13)]
        full_points.append((x, roots))
    full_points.append((XS[1], [pow(XS[1]-i, (P+1)//4, P) for i in range(13)]))
    eval93 = [[prod(r[i] for i in char) % P for x, r in full_points] for char in low_chars]
    eval93.append([x for x, r in full_points])
    assert nmod_mat(eval93, P).rank() == 93
    report["full_kummer_low_pole_rank"] = {"rows": 93, "points": 93, "rank": 93}

    b1, w1, u1, one = rr_code(83, 0)
    ann1 = kernel_rows(nmod_mat(u1, P))
    assert (len(b1), len(w1), len(u1), len(ann1)) == (43, 126, 173, 3)
    solve(b1, ann1[0], list(range(43)))
    one.update(rank=len(b1), square_rank=len(w1), cube_rank=len(u1), annihilator_dimension=len(ann1))
    report["one_point_control"] = one

    for e in (8, 16, 32):
        k, W, m = 5*e+3, 15*e+6, 22*e
        err = Fraction((P**k-1)*P**W, (P-1)**m)
        coarse = P**9 * Fraction(2, P**2)**e
        assert 0 < err < coarse < 1
    report["conditional_E_arithmetic_degrees"] = [8, 16, 32]
    report["snapshot_sha256"] = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                                 for p in sorted((ROOT / "snapshot").rglob("*"))
                                 if p.is_file() and p.suffix in (".py", ".md", ".json")}
    report["python"] = sys.version
    report["elapsed_seconds"] = round(time.monotonic()-start, 3)
    output = ROOT / "independent_results.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
