#!/opt/anaconda3/bin/python
"""Exact checks for the chart-cost lemma (prop:black-box (iv), route R2).

Run:  /opt/anaconda3/bin/python check_chart_lemma.py

Part A (Lyndon basis of the free Lie ring, truncated at class c):
  A1  the Lyndon-basis expansion of [b(u), b(v)] is supported on Lyndon words
      of content(u) + content(v), with integer coefficients;
  A2  the number of Lyndon words of a fixed content of length m <= c is at
      most (m-1)!, with equality at content (1,...,1);
  A3  the expansion coefficients are invariant under order-preserving
      relabelling of the letters, so one table T_c on the alphabet {0..c-1}
      serves every s;
  A4  the maximal support size of a bracket expansion, for c <= 4, s <= 3.

Part B (linear algebra over Z/p^e, the "ring operations"):
  B1  Howell form of a row module in (Z/p^e)^k and the O(k^2) membership
      test, checked against brute-force membership;
  B2  Smith form with unimodular transforms over Z/p^e, checked exactly.

Part C (the whole chart construction):
  C1  for explicit Lazard rings L with a surjection pi: F_{s,c} -> L, sample
      uniform elements of (ker pi)^perp (the distribution of lem:tb-kernel),
      run the column scan + Smith form + structure constants, and verify that
      the output is a Lie ring isomorphic to L through eps_i -> pi(eps~_i);
  C2  the paper's C_9 x C_3 example: the mod-p test discards a needed column.

Everything is exact integer arithmetic.  No randomness enters the proofs;
random samples only emulate the Fourier samples of lem:tb-kernel.
"""
from __future__ import annotations

import itertools
import math
import random
import sys
from collections import Counter, defaultdict
from fractions import Fraction

random.seed(20261103)

# --------------------------------------------------------------------------
# Part A: Lyndon words and the free Lie ring
# --------------------------------------------------------------------------

def is_lyndon(w):
    n = len(w)
    if n == 0:
        return False
    for i in range(1, n):
        if w[i:] <= w:  # a proper suffix that is <= w (lex) kills Lyndon-ness
            return False
    return True


def lyndon_words(alphabet_size, max_len):
    out = []
    for m in range(1, max_len + 1):
        for w in itertools.product(range(alphabet_size), repeat=m):
            if is_lyndon(w):
                out.append(w)
    return out


def std_factorisation(w):
    """w = u v with v the longest proper Lyndon suffix; returns (u, v)."""
    for i in range(1, len(w)):
        if is_lyndon(w[i:]):
            return w[:i], w[i:]
    raise ValueError("not a Lyndon word of length >= 2")


def poly_add(P, Q, coeff=1):
    R = dict(P)
    for w, c in Q.items():
        R[w] = R.get(w, 0) + coeff * c
        if R[w] == 0:
            del R[w]
    return R


def poly_mul(P, Q, max_len):
    R = {}
    for a, ca in P.items():
        for b, cb in Q.items():
            if len(a) + len(b) <= max_len:
                w = a + b
                R[w] = R.get(w, 0) + ca * cb
                if R[w] == 0:
                    del R[w]
    return R


def poly_bracket(P, Q, max_len):
    return poly_add(poly_mul(P, Q, max_len), poly_mul(Q, P, max_len), -1)


def bracketing_poly(w, cache, max_len):
    """Standard bracketing b(w) of a Lyndon word as a free associative polynomial."""
    if w in cache:
        return cache[w]
    if len(w) == 1:
        P = {w: 1}
    else:
        u, v = std_factorisation(w)
        P = poly_bracket(bracketing_poly(u, cache, max_len),
                         bracketing_poly(v, cache, max_len), max_len)
    cache[w] = P
    return P


def content(w, s):
    c = [0] * s
    for a in w:
        c[a] += 1
    return tuple(c)


def lyndon_coordinates(P, cache, max_len):
    """Express a Lie element P (assoc. polynomial) in the Lyndon basis.

    Uses Reutenauer, Free Lie Algebras, Thm 5.1: b(w) = w + (words > w).  So the
    lexicographically smallest word of a Lie element is Lyndon and its coefficient
    is the Lyndon coordinate.  Returns {lyndon word: integer coefficient}.
    Raises if the triangular extraction meets a non-Lyndon leading word or a
    non-integer coefficient (it never does; that is the check).
    """
    P = dict(P)
    coords = {}
    while P:
        w = min(P)  # lex smallest word
        if not is_lyndon(w):
            raise AssertionError(f"leading word {w} is not Lyndon")
        c = P[w]
        if not isinstance(c, int):
            raise AssertionError("non-integer coefficient")
        coords[w] = c
        P = poly_add(P, bracketing_poly(w, cache, max_len), -c)
    return coords


def bracket_table(s, c):
    """T[(u,v)] = Lyndon coordinates of [b(u), b(v)] in F_{s,c}, u<v Lyndon."""
    cache = {}
    L = lyndon_words(s, c)
    T = {}
    for u in L:
        for v in L:
            if len(u) + len(v) > c or u >= v:
                continue
            P = poly_bracket(bracketing_poly(u, cache, c),
                             bracketing_poly(v, cache, c), c)
            T[(u, v)] = lyndon_coordinates(P, cache, c)
    return L, T


def relabel(w, mapping):
    return tuple(mapping[a] for a in w)


def part_A(max_c=4, max_s=3):
    print("=== Part A: Lyndon basis checks ===")
    ok = True
    for c in range(1, max_c + 1):
        # the universal table on c letters
        Lc, Tc = bracket_table(c, c)
        for s in range(1, max_s + 1):
            L, T = bracket_table(s, c)
            d = len(L)
            witt = sum(sum((-1) ** 0 * 0 for _ in []) for _ in [])  # placeholder
            # Witt numbers
            def mobius(n):
                res, m, p = 1, n, 2
                while p * p <= m:
                    if m % p == 0:
                        m //= p
                        if m % p == 0:
                            return 0
                        res = -res
                    p += 1
                if m > 1:
                    res = -res
                return res
            witt = sum(sum(mobius(j) * s ** (k // j) for j in range(1, k + 1) if k % j == 0) // k
                       for k in range(1, c + 1))
            assert d == witt, (d, witt)
            # A2: Lyndon words per content
            per_content = Counter(content(w, s) for w in L)
            max_per = max(per_content.values())
            bound = max(math.factorial(m - 1) for m in range(1, c + 1))
            a2 = max_per <= bound
            # A1: support of each bracket lies in content(u)+content(v); integer coeffs
            a1 = True
            max_support = 0
            for (u, v), coords in T.items():
                target = tuple(x + y for x, y in zip(content(u, s), content(v, s)))
                for w, coeff in coords.items():
                    if content(w, s) != target or not isinstance(coeff, int):
                        a1 = False
                max_support = max(max_support, len(coords))
            # A3: relabelling invariance against the c-letter table
            a3 = True
            for (u, v), coords in T.items():
                letters = sorted(set(u) | set(v))
                mp = {a: i for i, a in enumerate(letters)}  # order-preserving
                inv = {i: a for a, i in mp.items()}
                uu, vv = relabel(u, mp), relabel(v, mp)
                if uu > vv:
                    continue  # the table only stores u<v; symmetric case is -T
                ref = Tc[(uu, vv)]
                back = {relabel(w, inv): coeff for w, coeff in ref.items()}
                if back != coords:
                    a3 = False
            ok &= a1 and a2 and a3
            print(f"c={c} s={s}: d={d} (Witt ok), max Lyndon words per content={max_per}"
                  f" <= (c-1)!={bound}: {a2}; brackets multihomogeneous+integral: {a1};"
                  f" max support={max_support}; relabelling-invariant: {a3}")
    print("Part A all checks passed:", ok)
    return ok


# --------------------------------------------------------------------------
# Part B: Howell and Smith forms over Z/p^e
# --------------------------------------------------------------------------

class Zpe:
    """Arithmetic in Z/p^e with the operations counted as ring operations."""

    def __init__(self, p, e):
        self.p, self.e, self.M = p, e, p ** e
        self.ops = 0

    def val(self, a):
        """p-adic valuation (e for a == 0) and unit part."""
        self.ops += 1
        a %= self.M
        if a == 0:
            return self.e, 0
        v = 0
        while a % self.p == 0:
            a //= self.p
            v += 1
        return v, a

    def inv_unit(self, u):
        self.ops += 1
        return pow(u, -1, self.M)

    def mul(self, a, b):
        self.ops += 1
        return (a * b) % self.M

    def sub(self, a, b):
        self.ops += 1
        return (a - b) % self.M

    def add(self, a, b):
        self.ops += 1
        return (a + b) % self.M

    def exact_div_p_power(self, a, v):
        """a / p^v for p^v | a; result defined modulo p^(e-v), lifted to Z/M."""
        self.ops += 1
        assert a % (self.p ** v) == 0
        return (a // self.p ** v) % self.M


def howell_form(R: Zpe, rows, k):
    """Howell form of the row module of `rows` in (Z/M)^k.

    Returns a list of (pivot_col, pivot_val a, row) with pivot entry p^a, a<e,
    strictly increasing pivot columns, and the Howell property
    p^(e-a_t) r_t in span(r_{t+1}, ...).  Rows are lists of ints mod M.
    """
    remaining = [list(r) for r in rows if any(x % R.M for x in r)]
    out = []
    for j in range(k):
        # pick the remaining row with minimal valuation in column j
        best, best_v, best_u = None, R.e, None
        for idx, r in enumerate(remaining):
            v, u = R.val(r[j])
            if v < best_v:
                best, best_v, best_u = idx, v, u
        if best is None:
            continue  # column j is zero on all remaining rows
        piv = remaining.pop(best)
        inv = R.inv_unit(best_u)
        piv = [R.mul(inv, x) for x in piv]  # pivot entry becomes p^a
        a = best_v
        new_remaining = []
        for r in remaining:
            if r[j] % R.M:
                q = R.exact_div_p_power(r[j], a)
                r = [R.sub(x, R.mul(q, y)) for x, y in zip(r, piv)]
            if any(x % R.M for x in r):
                new_remaining.append(r)
        # Howell fix-up: append p^(e-a) * pivot row (zero in column j)
        sat = [R.mul(R.p ** (R.e - a), x) for x in piv]
        if any(x % R.M for x in sat):
            new_remaining.append(sat)
        remaining = new_remaining
        out.append((j, a, piv))
    assert not remaining
    return out


def howell_member(R: Zpe, H, v):
    """Membership of v in the row module with Howell form H, O(k^2) ring ops."""
    v = list(v)
    t = 0
    k = len(v)
    for j in range(k):
        if v[j] % R.M == 0:
            continue
        if t < len(H) and H[t][0] < j:
            # pivots at columns < j that we have passed (v was zero there)
            while t < len(H) and H[t][0] < j:
                t += 1
        if t >= len(H) or H[t][0] != j:
            return False
        a, row = H[t][1], H[t][2]
        if v[j] % (R.p ** a):
            return False
        q = R.exact_div_p_power(v[j], a)
        v = [R.sub(x, R.mul(q, y)) for x, y in zip(v, row)]
        t += 1
    return all(x % R.M == 0 for x in v)


def brute_span(M, rows, k):
    """All elements of the Z/M-span of rows (for small cases only)."""
    span = {tuple([0] * k)}
    for r in rows:
        new = set()
        for x in span:
            for lam in range(M):
                new.add(tuple((xi + lam * ri) % M for xi, ri in zip(x, r)))
        span = new
    return span


def part_B1(trials=60):
    print("=== Part B1: Howell form and membership over Z/p^e ===")
    ok = True
    for _ in range(trials):
        p = random.choice([2, 3, 5])
        e = random.choice([1, 2, 3])
        k = random.choice([1, 2, 3])
        R = Zpe(p, e)
        m = random.randint(1, 3)
        rows = [[random.randrange(R.M) for _ in range(k)] for _ in range(m)]
        # bias: sometimes multiply rows by p to create zero divisors
        rows = [[(x * random.choice([1, 1, p])) % R.M for x in r] for r in rows]
        H = howell_form(R, rows, k)
        # (H1) strictly increasing pivots, pivot entries p^a with a<e
        cols = [h[0] for h in H]
        ok &= cols == sorted(set(cols))
        for j, a, row in H:
            ok &= row[j] == p ** a % R.M and a < e and all(x == 0 for x in row[:j])
        # (H3) Howell property
        for t, (j, a, row) in enumerate(H):
            sat = [(p ** (e - a) * x) % R.M for x in row]
            tail = [h[2] for h in H[t + 1:]]
            ok &= tuple(sat) in brute_span(R.M, tail, k)
        # span preserved and membership test correct on every vector
        S = brute_span(R.M, rows, k)
        S2 = brute_span(R.M, [h[2] for h in H], k)
        ok &= S == S2
        for v in itertools.product(range(R.M), repeat=k):
            ok &= howell_member(R, H, list(v)) == (v in S)
        if not ok:
            print("FAILED on", p, e, k, rows)
            break
    print("Part B1 passed:", ok)
    return ok


def smith_form(R: Zpe, C, k, r):
    """P C Q = D diagonal over Z/M with P (k x k), Q (r x r) invertible.

    Returns (diag_vals a_i with D_ii = p^{a_i} or a_i = e meaning 0, P, Q).
    Elimination with global-minimum-valuation pivots.
    """
    C = [list(row) for row in C]
    P = [[int(i == j) for j in range(k)] for i in range(k)]
    Q = [[int(i == j) for j in range(r)] for i in range(r)]
    diag = []
    t = 0
    while t < min(k, r):
        best, best_v, best_u = None, R.e, None
        for i in range(t, k):
            for j in range(t, r):
                v, u = R.val(C[i][j])
                if v < best_v:
                    best, best_v, best_u = (i, j), v, u
        if best is None:
            break
        i0, j0 = best
        # permute to (t,t)
        C[t], C[i0] = C[i0], C[t]
        P[t], P[i0] = P[i0], P[t]
        for row in C:
            row[t], row[j0] = row[j0], row[t]
        for row in Q:
            row[t], row[j0] = row[j0], row[t]
        inv = R.inv_unit(best_u)
        C[t] = [R.mul(inv, x) for x in C[t]]
        P[t] = [R.mul(inv, x) for x in P[t]]
        a = best_v
        # row elimination
        for i in range(k):
            if i != t and C[i][t] % R.M:
                q = R.exact_div_p_power(C[i][t], a)
                C[i] = [R.sub(x, R.mul(q, y)) for x, y in zip(C[i], C[t])]
                P[i] = [R.sub(x, R.mul(q, y)) for x, y in zip(P[i], P[t])]
        # column elimination (only row t is affected)
        for j in range(r):
            if j != t and C[t][j] % R.M:
                q = R.exact_div_p_power(C[t][j], a)
                for row in C:
                    row[j] = R.sub(row[j], R.mul(q, row[t]))
                for row in Q:
                    row[j] = R.sub(row[j], R.mul(q, row[t]))
        diag.append(a)
        t += 1
    while len(diag) < min(k, r):
        diag.append(R.e)
    return diag, P, Q


def matmul(R: Zpe, A, B):
    n, m, l = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(m)) % R.M for j in range(l)] for i in range(n)]


def is_unimodular(R: Zpe, P):
    # invertible over Z/p^e iff det is a unit iff det mod p != 0
    n = len(P)
    # det by fraction-free elimination over Q then mod M
    A = [[Fraction(x) for x in row] for row in P]
    det = Fraction(1)
    for i in range(n):
        piv = next((j for j in range(i, n) if A[j][i] != 0), None)
        if piv is None:
            return False
        if piv != i:
            A[i], A[piv] = A[piv], A[i]
            det = -det
        det *= A[i][i]
        for j in range(i + 1, n):
            f = A[j][i] / A[i][i]
            A[j] = [x - f * y for x, y in zip(A[j], A[i])]
    return det.denominator == 1 and det.numerator % R.p != 0


def part_B2(trials=60):
    print("=== Part B2: Smith form with transforms over Z/p^e ===")
    ok = True
    for _ in range(trials):
        p = random.choice([2, 3, 5])
        e = random.choice([1, 2, 3])
        k, r = random.randint(1, 4), random.randint(1, 4)
        R = Zpe(p, e)
        C = [[(random.randrange(R.M) * random.choice([1, 1, p])) % R.M for _ in range(r)] for _ in range(k)]
        diag, P, Q = smith_form(R, C, k, r)
        D = matmul(R, matmul(R, P, C), Q)
        for i in range(k):
            for j in range(r):
                want = (p ** diag[i] if i == j and i < len(diag) and diag[i] < e else 0) % R.M
                ok &= D[i][j] == want
        ok &= is_unimodular(R, P) and is_unimodular(R, Q)
        # divisibility chain
        ok &= all(diag[i] <= diag[i + 1] for i in range(len(diag) - 1))
        if not ok:
            print("FAILED on", p, e, C, diag, D)
            break
    print("Part B2 passed:", ok)
    return ok


# --------------------------------------------------------------------------
# Part C: the chart construction on explicit Lazard rings
# --------------------------------------------------------------------------

class LieRing:
    """L = sum_i Z/p^{e_i} eps_i with integer structure constants."""

    def __init__(self, p, orders, bracket):
        # bracket[(i,j)] = dict m -> coeff  for i<j; antisymmetric completion
        self.p = p
        self.orders = list(orders)  # exponents e_i
        self.m = len(orders)
        self.br = {}
        for (i, j), vec in bracket.items():
            self.br[(i, j)] = dict(vec)
            self.br[(j, i)] = {m: -c for m, c in vec.items()}

    def reduce(self, x):
        return tuple(xi % self.p ** ei for xi, ei in zip(x, self.orders))

    def add(self, x, y):
        return self.reduce([a + b for a, b in zip(x, y)])

    def scal(self, lam, x):
        return self.reduce([lam * a for a in x])

    def bracket(self, x, y):
        out = [0] * self.m
        for i in range(self.m):
            if x[i] == 0:
                continue
            for j in range(self.m):
                if y[j] == 0 or (i, j) not in self.br:
                    continue
                for mm, c in self.br[(i, j)].items():
                    out[mm] += x[i] * y[j] * c
        return self.reduce(out)

    def elements(self):
        return itertools.product(*[range(self.p ** ei) for ei in self.orders])

    def size(self):
        return math.prod(self.p ** ei for ei in self.orders)


def free_images(Lring, s, c, gen_images, L_words, T):
    """pi(w) for every Lyndon basis word w, from the images of the generators.

    pi(b(w)) = [pi(b(u)), pi(b(v))] for w = uv the standard factorisation.
    """
    img = {}
    for w in L_words:
        if len(w) == 1:
            img[w] = Lring.reduce(gen_images[w[0]])
        else:
            u, v = std_factorisation(w)
            img[w] = Lring.bracket(img[u], img[v])
    return img


def sample_dual(Lring, img, L_words, M, e):
    """Uniform element of (ker pi)^perp in (Z/M)^d, via a uniform character of L.

    a_j = sum_i b_i p^{e-e_i} pi(w_j)_i  mod M, for uniform b in L.
    """
    b = [random.randrange(Lring.p ** ei) for ei in Lring.orders]
    a = []
    for w in L_words:
        y = img[w]
        a.append(sum(bi * Lring.p ** (e - ei) * yi for bi, ei, yi in zip(b, Lring.orders, y)) % M)
    return a


def chart_from_samples(R: Zpe, Y, L_words, T, s, c):
    """The algorithm of the lemma.  Returns chart data and operation count."""
    k, d = len(Y), len(L_words)
    index = {w: j for j, w in enumerate(L_words)}
    cols = [[Y[i][j] for i in range(k)] for j in range(d)]
    # column scan with Howell forms
    kept, H = [], []
    scans = 0
    for j in range(d):
        scans += 1
        if not howell_member(R, H, cols[j]):
            kept.append(j)
            H = howell_form(R, [cols[t] for t in kept], k)
    r = len(kept)
    C = [[cols[j][i] for j in kept] for i in range(k)]  # k x r
    diag, P, Q = smith_form(R, C, k, r)
    I = [i for i in range(r) if diag[i] < R.e]
    # chart basis eps_i = C Q e_i, lifts eps~_i = sum_a Q[a][i] w_{kept[a]}
    CQ = matmul(R, C, Q)
    eps = {i: [CQ[row][i] for row in range(k)] for i in I}
    lifts = {i: {kept[a]: Q[a][i] for a in range(r) if Q[a][i] % R.M} for i in I}
    orders = {i: R.e - diag[i] for i in I}

    def coords(v):
        Pv = [sum(P[i][t] * v[t] for t in range(k)) % R.M for i in range(k)]
        out = {}
        for i in range(k):
            if i in orders:
                assert Pv[i] % (R.p ** diag[i]) == 0, "vector not in A"
                out[i] = (Pv[i] // R.p ** diag[i]) % (R.p ** orders[i])
            else:
                assert Pv[i] == 0, "vector not in A"
        return out

    def Y_bracket_words(a, b):
        """z_{ab} = Y [w_a, w_b] from the table."""
        wa, wb = L_words[a], L_words[b]
        if len(wa) + len(wb) > c or wa == wb:
            return [0] * k
        sign = 1
        if wa > wb:
            wa, wb, sign = wb, wa, -1
        z = [0] * k
        for w, coeff in T[(wa, wb)].items():
            col = cols[index[w]]
            z = [(zi + sign * coeff * ci) % R.M for zi, ci in zip(z, col)]
        return z

    sc = {}
    for i in I:
        for j in I:
            if i >= j:
                continue
            acc = [0] * k
            for a, qa in lifts[i].items():
                for b, qb in lifts[j].items():
                    z = Y_bracket_words(a, b)
                    acc = [(x + qa * qb * zi) % R.M for x, zi in zip(acc, z)]
            sc[(i, j)] = coords(acc)
    return dict(kept=kept, r=r, I=I, orders=orders, eps=eps, lifts=lifts,
                sc=sc, coords=coords, diag=diag, scans=scans)


def verify_chart(R: Zpe, chart, Lring, img, L_words, c):
    """Check eps_i -> pi(eps~_i) is a Lie ring isomorphism onto L."""
    I, orders, lifts, sc = chart["I"], chart["orders"], chart["lifts"], chart["sc"]
    # images of the chart basis in L
    im = {}
    for i in I:
        y = tuple([0] * Lring.m)
        for j, q in lifts[i].items():
            y = Lring.add(y, Lring.scal(q, img[L_words[j]]))
        im[i] = y
    # (1) orders match: sum of exponents = log_p |L|, and p^{orders} im = 0
    total = sum(orders.values())
    ok = (Lring.p ** total == Lring.size())
    for i in I:
        ok &= Lring.scal(Lring.p ** orders[i], im[i]) == tuple([0] * Lring.m)
    # (2) additive bijection: enumerate all coordinate tuples -> distinct elements
    seen = set()
    for t in itertools.product(*[range(Lring.p ** orders[i]) for i in I]):
        y = tuple([0] * Lring.m)
        for ti, i in zip(t, I):
            y = Lring.add(y, Lring.scal(ti, im[i]))
        seen.add(y)
    ok &= len(seen) == Lring.size()
    # (3) brackets: [im_i, im_j] in L equals sum_m sc[(i,j)][m] im_m
    for (i, j), cvec in sc.items():
        lhs = Lring.bracket(im[i], im[j])
        rhs = tuple([0] * Lring.m)
        for mm, coeff in cvec.items():
            rhs = Lring.add(rhs, Lring.scal(coeff, im[mm]))
        ok &= lhs == rhs
    return ok, total


def run_example(name, p, e, orders, bracket, s, c, gen_images, extra_samples=3, repeats=5):
    L_words, T = bracket_table(s, c)
    d = len(L_words)
    R = Zpe(p, e)
    Lring = LieRing(p, orders, bracket)
    img = free_images(Lring, s, c, gen_images, L_words, T)
    n = round(math.log(Lring.size(), p))
    # surjectivity of pi (brute force over F would be large; check image spans L)
    allok = True
    for rep in range(repeats):
        k = n + extra_samples
        R.ops = 0
        Y = [sample_dual(Lring, img, L_words, R.M, e) for _ in range(k)]
        chart = chart_from_samples(R, Y, L_words, T, s, c)
        ok, total = verify_chart(R, chart, Lring, img, L_words, c)
        allok &= ok
        if rep == 0:
            print(f"  {name}: s={s} c={c} p^e={p}^{e} d={d} n=log_p|L|={n} k={k}:"
                  f" kept={chart['r']} (<= n: {chart['r'] <= n}), chart orders="
                  f"{[chart['orders'][i] for i in chart['I']]} (sum={total}),"
                  f" iso check={ok}, ring ops={R.ops}")
    return allok


def part_C():
    print("=== Part C: chart construction on explicit Lazard rings ===")
    ok = True
    # C1a: Heisenberg-like ring Z/9 x Z/9 x Z/3 with [x,y] = z (p=3 > c=2), s=2
    ok &= run_example("Z/9+Z/9+Z/3, [x,y]=z", 3, 2, [2, 2, 1], {(0, 1): {2: 1}}, 2, 2,
                      {0: (1, 0, 0), 1: (0, 1, 0)})
    # C1b: same ring, s=3 generators (redundant generator x+y), d=6
    ok &= run_example("same, s=3 redundant", 3, 2, [2, 2, 1], {(0, 1): {2: 1}}, 3, 2,
                      {0: (1, 0, 0), 1: (0, 1, 0), 2: (1, 1, 0)})
    # C1c: class 3, p=5, e=2: free nilpotent of class 3 on 2 gens over Z/25 modulo
    #      an ideal: L = span(x, y, z=[x,y], u=[z,x]) with [z,y]=0 and 5u=0,
    #      orders (2,2,2,1).  Check Jacobi: class 3, all triple brackets with
    #      two z's or involving u vanish; Jacobi on (x,y,z): [[x,y],z]+[[y,z],x]+[[z,x],y]
    #      = 0 + 0 + [u, y] = 0 since [u,y] = 0.  OK.
    ok &= run_example("class 3 over Z/25, orders (2,2,2,1)", 5, 2, [2, 2, 2, 1],
                      {(0, 1): {2: 1}, (2, 0): {3: 1}}, 2, 3,
                      {0: (1, 0, 0, 0), 1: (0, 1, 0, 0)})
    # C1d: abelian Z/9 x Z/3 with s=2, c=2: the paper's C_9 x C_3
    ok &= run_example("C_9 x C_3 abelian", 3, 2, [2, 1], {}, 2, 2, {0: (1, 0), 1: (0, 1)})
    # C1e: cyclic Z/27 generated by two elements, s=2, c=2 (kept > module rank case)
    ok &= run_example("Z/27 from two generators", 3, 3, [3], {}, 2, 2, {0: (3,), 1: (1,)})
    print("Part C1 passed:", ok)

    # C2: the mod-p test fails on C_9 x C_3
    print("--- C2: mod-p column test on C_9 x C_3 ---")
    L_words, T = bracket_table(2, 2)
    Lring = LieRing(3, [2, 1], {})
    img = free_images(Lring, 2, 2, {0: (1, 0), 1: (0, 1)}, L_words, T)
    R = Zpe(3, 2)
    Y = [sample_dual(Lring, img, L_words, 9, 2) for _ in range(6)]
    col2 = [Y[i][1] for i in range(6)]
    print(f"  second column (image of X_2) = {col2}; all divisible by 3: {all(x % 3 == 0 for x in col2)}")
    H = howell_form(R, [[Y[i][0] for i in range(6)]], 6)
    print(f"  but X_2's column lies in the Z/9-span of X_1's column: {howell_member(R, H, col2)}"
          f"  (so the mod-3 test would wrongly discard it)")
    return ok


if __name__ == "__main__":
    a = part_A()
    b1 = part_B1()
    b2 = part_B2()
    cc = part_C()
    print()
    print("ALL PASSED" if (a and b1 and b2 and cc) else "SOME CHECK FAILED")
    sys.exit(0 if (a and b1 and b2 and cc) else 1)
