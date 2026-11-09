#!/usr/bin/env python
"""s3 (9 Nov 2026 proof check): exact checks of two main-text formulas of Section sec:schedule3
(outside appendix-schedule3 proper, checked because they sit in main.tex 764-793):
 [1] Prop rc-lower: conditional on rank r = a and pivot pattern {1..r}, the mean acceptance of a
     uniform kernel vector is (q^{M-r} - p^{-(M-r)}) q^r, q = (h+1)/p, and the conditioning event
     fails with probability <= 1/(p-1).  Exhaustive over all a x M matrices, small cases.
 [2] Thm free-coordinate(ii): beta(4u, 2u+1; a) <= 4*15^{-2u} u^{-u-1} + 2 p^{-u-1} for
     kappa <= u, a <= u-1, p >= 16u^2 (least primes), exact Fractions.
Finite checks only."""
from fractions import Fraction as Fr
from itertools import product

def rref_pivots(rows, p):
    A = [list(r) for r in rows]; piv = []; r = 0
    M = len(A[0])
    for c in range(M):
        pr = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if pr is None: continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p-2, p); A[r] = [x*inv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [(x - f*z) % p for x, z in zip(A[i], A[r])]
        piv.append(c); r += 1
    return piv

ok = True
for (p, kap, M, a) in [(5,2,3,1),(5,2,4,1),(7,3,3,1),(7,2,3,2),(5,2,3,2),(7,3,4,1),(11,2,3,1),(13,4,3,1)]:
    h = (p-1)//kap
    D = {pow(x, kap, p) for x in range(1, p)} | {0}
    S = [y for y in product(sorted(D), repeat=M) if any(y)]
    q = Fr(h+1, p)
    tot = Fr(0); cnt = 0; nmat = 0
    for X in product(range(p), repeat=a*M):
        nmat += 1
        rows = [X[i*M:(i+1)*M] for i in range(a)]
        if rref_pivots(rows, p) != list(range(a)): continue
        cnt += 1
        N = sum(1 for y in S if all(sum(r[j]*y[j] for j in range(M)) % p == 0 for r in rows))
        tot += Fr(N, p**(M-a))
    mean = tot / cnt
    formula = (q**(M-a) - Fr(1, p**(M-a))) * q**a
    fail = 1 - Fr(cnt, nmat)
    good = (mean == formula) and (formula <= q**M) and (fail <= Fr(1, p-1))
    ok &= good
    print(f"rc-lower (p,k,M,a)=({p},{kap},{M},{a}): mean={mean} formula={formula} [{mean == formula}] "
          f"<= q^M [{formula <= q**M}] Pr[not pattern]={fail} <= 1/(p-1) [{fail <= Fr(1, p-1)}]")

def isprime(n):
    if n < 2: return False
    i = 2
    while i*i <= n:
        if n % i == 0: return False
        i += 1
    return True

for u in range(2, 41):
    M, n0 = 4*u, 2*u+1; L = M - n0
    p = 16*u*u
    while not isprime(p): p += 1
    for pp in (p, p + 2*u*u):     # least prime >= 16u^2 and the next prime after 18u^2
        while not isprime(pp): pp += 1
        for kap in range(1, u+1):
            if (pp-1) % kap: continue
            h = (pp-1)//kap
            if h < 2: continue
            q = Fr(h+1, pp)
            for a in range(0, u):
                beta = 4 / (Fr(h)**(n0-1) * q**a) + Fr(pp**a - 1, (pp-1) * pp**L)
                bound = Fr(4, 15**(2*u) * u**(u+1)) + Fr(2, pp**(u+1))
                if beta > bound:
                    ok = False; print("FAIL beta(ii)", u, pp, kap, a)
print("beta bound of part (ii) checked for u <= 40 at two primes each")
print("ALL OK" if ok else "SOME FAIL")
