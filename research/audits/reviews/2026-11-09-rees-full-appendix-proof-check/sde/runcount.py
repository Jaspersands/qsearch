"""Subgroup-chain model of the restart variant of rem:sde-side-tape.

H_pi = Z_N (N = pi-part of p-1).  Anchor: pi-parts y_1..y_k.  H_1 = <y's>,
order N/g0 with g0 = gcd(y's, N).  Check at C (order n, H_1 <= C): the y's lie in
one coset of kappa*C (order n/gcd(n,kappa)), i.e. (N*gcd(n,kappa)/n) | g1, g1 =
gcd of the differences y_j - y_1 and N.  Every pair g0 | g1 | N is realised by two
coefficients (y_1 = g0, y_2 = g0 + g1).  Failure of the check is monotone under
shrinking C, so the maximal number of runs is
   1 + max over (g0,g1) and failing C >= H_1 of Omega(n) - Omega(N/g0).
Compare with r_run = nu - min_{q | kappa} v_q((p-1)/kappa).
"""
import sympy
from math import gcd

def Omega(n):
    return sum(sympy.factorint(n).values()) if n > 1 else 0

def max_runs(N, kappa):
    divs = sympy.divisors(N)
    best = 1
    for g0 in divs:
        h1 = N // g0
        for g1 in divs:
            if g1 % g0:
                continue
            for n in divs:
                if n % h1:
                    continue
                fail = g1 % (N * gcd(n, kappa) // n) != 0
                if fail:
                    best = max(best, 1 + Omega(n) - Omega(h1))
    return best

def v(q, n):
    c = 0
    while n % q == 0:
        n //= q; c += 1
    return c

bad = []
tested = 0
for kappa in list(range(2, 61)):
    qs = sympy.primefactors(kappa)
    pmax = 4000 if kappa in (6, 10, 12, 15, 30) else 3000
    for p in sympy.primerange(3, pmax):
        if (p - 1) % kappa:
            continue
        N = 1
        for q in qs:
            N *= q ** v(q, p - 1)
        nu = Omega(N)
        rrun = nu - min(v(q, (p - 1) // kappa) for q in qs)
        m = max_runs(N, kappa)
        tested += 1
        if m != rrun:
            bad.append((kappa, p, m, rrun))
print("tested (kappa,p) pairs:", tested, " mismatches (kappa,p,model max,r_run):", bad[:20], len(bad))
