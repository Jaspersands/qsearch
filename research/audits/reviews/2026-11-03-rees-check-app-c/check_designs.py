"""Item 3 (campaign 4): Lemma app-sub-design, exact over F_p.

(a) mu_e for every e | p-1 with e > c.
(b) product designs from row solutions of sum_{i<=j+1} x_i^j = 0, rows chosen
    at random and adversarially (minimal support, repeated values), for all
    primes 3 <= p <= 31 and 1 <= c <= min(p-1, 7): moments 1..c vanish, points
    nonzero, M <= (c+1)!, at least c distinct points, and at least c+1 when
    c <= p-2.  The case c = p-1 is run for p = 3, 5, 7.
(c) exhaustive over multiplicity vectors mod p (p <= 7): vanishing moments
    1..c' with fewer than c'+1 distinct points force p | |S|.
Profile: the 14 design points of rees_subspace_source.json are the 14th roots
of unity mod 43, and their moments 1..9 vanish.

Run: /opt/anaconda3/bin/python check_designs.py
"""
import itertools
import json
import math
import os
import random

random.seed(5)
PRIMES = [p for p in range(3, 32) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def moments(S, p, c):
    return [sum(pow(s, j, p) for s in S) % p for j in range(1, c + 1)]


def row_solutions(p, j, limit=4000):
    """nonzero solutions of x_1^j + ... + x_{j+1}^j = 0 (exhaustive if small, else random search)."""
    n = j + 1
    sols = []
    if p ** n <= 200000:
        for v in itertools.product(range(p), repeat=n):
            if any(v) and sum(pow(x, j, p) for x in v) % p == 0:
                sols.append(v)
    else:
        tries = 0
        while len(sols) < limit and tries < 400000:
            tries += 1
            v = tuple(random.randrange(p) for _ in range(n))
            if any(v) and sum(pow(x, j, p) for x in v) % p == 0:
                sols.append(v)
    return sols


def product_design(rows):
    S = [1]
    for X in rows:
        S = [(s * x) for s in S for x in X]
    return S


def check_a():
    n = 0
    for p in PRIMES:
        g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, q))))
        for e in range(2, p):
            if (p - 1) % e:
                continue
            xi = pow(g, (p - 1) // e, p)
            S = [pow(xi, i, p) for i in range(e)]
            assert len(set(S)) == e
            for c in range(1, e):
                assert moments(S, p, c) == [0] * c
                n += 1
            # sharpness: moment e does not vanish (it equals e mod p)
            assert sum(pow(s, e, p) for s in S) % p == e % p
    print(f"(a) mu_e designs: {n} (p, e, c) triples with e | p-1, e > c: ok")


def check_b():
    n_designs = 0
    worst_ratio = 0
    for p in PRIMES:
        rowsol = {}
        for c in range(1, min(p - 1, 7) + 1):
            if c == p - 1 and p > 7:
                continue
            if math.factorial(c + 1) > 50000:
                continue
            for j in range(2, c + 1):
                if j not in rowsol:
                    rowsol[j] = row_solutions(p, j)
                    assert rowsol[j], ("Chevalley-Warning predicts a solution", p, j)
            trials = 40 if c >= 2 else 1
            for t in range(trials):
                rows = [[1, p - 1]]
                for j in range(2, c + 1):
                    sols = rowsol[j]
                    if t % 4 == 0:   # minimal support
                        v = min(sols, key=lambda v: sum(1 for x in v if x))
                    elif t % 4 == 1:  # maximal support
                        v = max(sols, key=lambda v: (sum(1 for x in v if x), -len(set(v))))
                    elif t % 4 == 2:  # most repeated values
                        v = min(sols, key=lambda v: len(set(x for x in v if x)) - 0.01 * sum(1 for x in v if x))
                    else:
                        v = random.choice(sols)
                    rows.append([x for x in v if x])
                S = [s % p for s in product_design(rows)]
                M = len(S)
                assert all(S), "zero point"
                assert moments(S, p, c) == [0] * c, ("moments", p, c, rows)
                assert M <= math.factorial(c + 1)
                nd = len(set(S))
                need = c + 1 if c <= p - 2 else c
                assert nd >= need, ("coverage", p, c, rows, nd)
                worst_ratio = max(worst_ratio, M / math.factorial(c + 1))
                n_designs += 1
    print(f"(b) product designs: {n_designs} designs over p <= 31, c <= 7 (c = p-1 for p = 3, 5, 7): "
          f"moments, nonzero, M <= (c+1)!, coverage ok")


def check_c():
    n = 0
    for p in (3, 5, 7):
        pts = list(range(1, p))
        for a in itertools.product(range(p), repeat=p - 1):
            supp = [u for u, ai in zip(pts, a) if ai]
            if not supp:
                continue
            for cp in range(len(supp), p - 1):
                if all(sum(ai * pow(u, j, p) for u, ai in zip(pts, a)) % p == 0 for j in range(1, cp + 1)):
                    raise AssertionError(("(c) violated", p, a, cp))
            n += 1
    print(f"(c) exhaustive: {n} nonzero multiplicity vectors mod p, p in (3,5,7): no vanishing-moment set with <= c' points: ok")


def check_profile():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "..", "..", "reductions", "rees_subspace_source.json")
    prof = json.load(open(path))["public_group_profile"]
    S, p, c = prof["design_points"], prof["p"], prof["class"]
    assert len(S) == 14 and len(set(S)) == 14
    assert all(pow(s, 14, p) == 1 for s in S)
    assert moments(S, p, 13) == [0] * 13 and sum(pow(s, 14, p) for s in S) % p == 14
    assert moments(S, p, c) == [0] * c
    # smallest design from (a) at the profile: smallest e | 42 with e > 9
    es = [e for e in range(c + 1, p) if (p - 1) % e == 0]
    print(f"profile p = 43, c = 9: the 14 points are mu_14, moments 1..13 vanish; divisors e > 9 of 42: {es}; "
          f"(c+1)! = {math.factorial(c + 1)}")


if __name__ == "__main__":
    check_a()
    check_c()
    check_b()
    check_profile()
    print("ALL OK")


def check_merged_odd_rows():
    """Optional variant (not in the appendix): one factor {1, -1} kills every odd moment,
    so rows are needed only for even j; M <= 2 prod_{j even <= c} (j+1)."""
    n = 0
    for p in PRIMES:
        for c in range(1, min(p - 1, 8) + 1):
            if c == p - 1 and p > 7:
                continue
            rows = [[1, p - 1]]
            for j in range(2, c + 1, 2):
                rows.append([x for x in random.choice(row_solutions(p, j)) if x])
            S = [s % p for s in product_design(rows)]
            bound = 2 * math.prod(j + 1 for j in range(2, c + 1, 2))
            assert all(S) and moments(S, p, c) == [0] * c and len(S) <= bound
            assert len(set(S)) >= (c + 1 if c <= p - 2 else c)
            n += 1
    print(f"variant: merged odd rows, {n} designs ok; at c = 9 the bound is {2 * 3 * 5 * 7 * 9} against 10! = 3628800")


if __name__ == "__main__" and True:
    check_merged_odd_rows()
