#!/usr/bin/env python
"""Mechanical preview (not a recommendation): E_W(c) with the Schedule 2
arity (g+1)((kappa-1)g+1) replaced by the triangular arity (g+1)(g+2)/2 of
Proposition prop:triangular-sde, under the SAME guard p >= 16 kappa^(2kappa+2).

E_W(c) = max_{p > c} (1 + sum_{d=2}^c e_d(p))  (Theorem bb-envelope), with
e_d(p) the exponent of (g_d+1) in the per-grade bound M_d <= C_d (g_d+1)^{e_d}
of Lemma tb-count-grade:
  kappa_d = 1                         -> M_d = g_d+1,                     e = 1
  kappa_d >= 2, p >= 16k^(2k+2)       -> Schedule 2 / triangular,         e = e2
  otherwise                           -> Schedule 1 at degree kappa_d,    e = k ceil(log2(k+1))
For the paper's Schedule 2, (g+1)((k-1)g+1) <= (k-1)(g+1)^2, so e2 = 2.
For the triangular arity, (g+1)(g+2)/2 <= (g+1)^2, and no smaller exponent
works for all g (the ratio to (g+1)^2 tends to 1/2), so again e2 = 2.

e_d(p) depends on p only through p mod L, L = lcm(2..c), and the threshold
interval containing p; we enumerate (unit residue, interval) pairs and then
find an actual prime witness for the best attainable value (same method as
research/audits/reviews/2026-11-04-rees-check-new-text/ew_values.py, re-implemented).

Also (aside, a different guard that the paper does NOT adopt): the guard
p not in E_2(kappa_d), for c <= 5 where E_2(2), E_2(3), E_2(4), E_2(5) are
quoted in full after Proposition prop:decoupled-sde.
"""
from functools import reduce
from math import gcd

from sympy import isprime


def clog2(x):
    return (x - 1).bit_length()


def T(k):
    return 16 * k ** (2 * k + 2)


def lcm(a, b):
    return a * b // gcd(a, b)


def e_d(d, p_minus_1_residue, ge, e2):
    k = gcd(d, p_minus_1_residue)
    if k == 1:
        return 1
    if ge(k):
        return e2
    return k * clog2(k + 1)


def EW(c, e2):
    L = reduce(lcm, range(2, c + 1), 1)
    bounds = [c + 1] + sorted(set(T(k) for k in range(2, c + 1))) + [None]
    units = [u for u in range(1, L + 1) if gcd(u, L) == 1]
    vals = {}
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        ge = lambda k, lo=lo: lo >= T(k)
        for u in units:
            v = 1 + sum(e_d(d, u - 1, ge, e2) for d in range(2, c + 1))
            vals.setdefault(v, []).append((u, lo, hi))
    for v in sorted(vals, reverse=True):
        for (u, lo, hi) in sorted(vals[v], key=lambda t: t[1]):
            q = lo + ((u - lo) % L)
            tries = 0
            while (hi is None or q < hi) and tries < 200000:
                if q > c and isprime(q):
                    return v, q
                q += L
                tries += 1
    raise RuntimeError


def direct(c, p, e2, guard):
    tot = 1
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        if k == 1:
            tot += 1
        elif guard(k, p):
            tot += e2
        else:
            tot += k * clog2(k + 1)
    return tot


E2 = {2: set(), 3: set(), 4: {5, 13, 17, 29, 37, 53},
      5: {11, 31, 41, 61, 71, 101, 131, 151, 181}}

if __name__ == "__main__":
    paper = [5, 11, 23, 38, 56, 77, 107, 143]
    import sympy as sp
    g_, k_ = sp.symbols("g k", positive=True)
    # exponent of (g+1): degree in g of the arity polynomial
    e2_sym = sp.degree(sp.expand((g_ + 1) * ((k_ - 1) * g_ + 1)), g_)
    e2_tri = sp.degree(sp.expand((g_ + 1) * (g_ + 2) / 2), g_)
    print("two-level exponent: Schedule 2 =", e2_sym, "; triangular =", e2_tri)
    sym, tri = [], []
    for c in range(2, 10):
        vs, ps = EW(c, e2=int(e2_sym))
        vt, pt = EW(c, e2=int(e2_tri))
        # cross-check by direct evaluation at every prime below 3e5 (covers
        # the witnesses; above 16*3^8 only grades with kappa >= 4 can still be
        # Schedule 1, and the residue enumeration above handles all p).
        sym.append((vs, ps))
        tri.append((vt, pt))
    print("E_W   (paper Schedule 2):", [v for v, _ in sym], "witness p:", [p for _, p in sym])
    print("E_W^tri (triangular)    :", [v for v, _ in tri], "witness p:", [p for _, p in tri])
    assert [v for v, _ in sym] == paper
    # direct cross-check over primes < 2*10^5
    for c in range(2, 10):
        best = max(direct(c, p, 2, lambda k, p: p >= T(k)) for p in range(c + 1, 200000) if isprime(p))
        assert best == paper[c - 2], (c, best)
    # the per-grade constants: two-level C_d = kappa_d - 1 (paper) vs 1 (triangular);
    # K_c = prod_d d^{d(d-1)ceil(log2(d+1))/2} is set by Schedule 1 and does not change.
    for g in range(0, 2000):
        for k in range(2, 10):
            assert (g + 1) * (g + 2) // 2 <= (g + 1) * ((k - 1) * g + 1) <= (k - 1) * (g + 1) ** 2
            assert (g + 1) * (g + 2) // 2 <= (g + 1) ** 2
    # aside: guard p not in E_2(kappa_d), c <= 5 (NOT the paper's guard)
    alt = []
    for c in range(2, 6):
        guard = lambda k, p: p not in E2[k]
        best, arg = 0, None
        for p in range(c + 1, 200000):
            if isprime(p):
                v = direct(c, p, 2, guard)
                if v > best:
                    best, arg = v, p
        alt.append((best, arg))
    print("aside, guard p notin E_2(kappa_d), c=2..5:", alt)
