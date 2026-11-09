#!/usr/bin/env python
"""Sanity checks for 2026-11-05-rees-square-gap-attack.md (tiny, seconds).

A. Explicit (kappa-1)-wise independent Bernoulli law with P(all ones)=0 iff q<=1/2.
B. Exact 4-cycle frequencies of the character expansion via Jacobi sums, and
   vanishing of S_e when the support has a vertex of degree one.
C. Chebotarev illustration: fraction of primes p = 1 (mod kappa) at which small
   primes are kappa-th powers.
D. Barrier values against the known E_2 data.
"""
from fractions import Fraction
from itertools import product
import cmath, math, sys

def is_prime(n):
    if n < 2: return False
    for d in range(2, int(n**0.5)+1):
        if n % d == 0: return False
    return True

# ---------- A ----------
def law(kappa, q):
    """P(x) = q^|x| (1-q)^(kappa-|x|) - (-1)^(kappa-|x|) q^kappa on {0,1}^kappa."""
    P = {}
    for x in product((0,1), repeat=kappa):
        w = sum(x)
        P[x] = q**w * (1-q)**(kappa-w) - (-1)**(kappa-w) * q**kappa
    return P

def check_law(kappa, q):
    P = law(kappa, q)
    nonneg = all(v >= 0 for v in P.values())
    total = sum(P.values())
    allones = P[(1,)*kappa]
    # every proper marginal equals the independent one
    ok_marg = True
    for S in product((0,1), repeat=kappa):
        if sum(S) in (0, kappa): continue
        idx = [i for i in range(kappa) if S[i]]
        for vals in product((0,1), repeat=len(idx)):
            m = sum(v for x, v in P.items() if all(x[i] == vv for i, vv in zip(idx, vals)))
            w = sum(vals)
            ind = q**w * (1-q)**(len(idx)-w)
            if m != ind: ok_marg = False
    return nonneg, total, allones, ok_marg

print("A. explicit (kappa-1)-wise independent law")
for kappa in (3, 4, 5, 6):
    for q in (Fraction(1,4), Fraction(1,2), Fraction(2,3)):
        nonneg, total, allones, ok_marg = check_law(kappa, q)
        print(f"  kappa={kappa} q={q}: nonneg={nonneg} total={total} P(all)={allones} marginals_independent={ok_marg}")

# ---------- B ----------
def chi_table(p, kappa):
    g = next(g for g in range(2, p) if all(pow(g, (p-1)//f, p) != 1 for f in range(2, p) if (p-1) % f == 0 and is_prime(f)))
    ind = {}
    x = 1
    for k in range(p-1):
        ind[x] = k
        x = x * g % p
    omega = cmath.exp(2j*math.pi/kappa)
    def chi(s, u):
        u %= p
        if u == 0: return 1.0 if s % kappa == 0 else 0.0
        return omega ** ((s * ind[u]) % kappa)
    return chi, g

def jacobi(chi, p, a, b):
    return sum(chi(a, w) * chi(b, 1 - w) for w in range(p))

print("B. 4-cycle frequencies: brute force vs p(p-1) chi^{e2+e4}(-1) J(e1,e2) J(e3,e4)")
for kappa, p in ((3, 7), (3, 13), (4, 13), (5, 11)):
    chi, g = chi_table(p, kappa)
    worst = 0.0
    tested = 0
    for e1, e2, e3, e4 in product(range(1, kappa), repeat=4):
        if (e1+e2+e3+e4) % kappa: continue
        if (e1+e2) % kappa == 0 or (e3+e4) % kappa == 0: continue
        # Sigma over alpha_j, alpha_j', beta_i, beta_i'
        S = 0
        for aj, ajp, bi, bip in product(range(p), repeat=4):
            S += chi(e1, aj+bi) * chi(e2, ajp+bi) * chi(e3, aj+bip) * chi(e4, ajp+bip)
        pred = p*(p-1) * chi(e2+e4, -1) * jacobi(chi, p, e1, e2) * jacobi(chi, p, e3, e4)
        worst = max(worst, abs(S - pred))
        tested += 1
        if tested >= 6: break
    print(f"  kappa={kappa} p={p}: {tested} tuples, max |brute - formula| = {worst:.2e}, |S| = p^2(p-1) = {p*p*(p-1)}")
    # frequencies with sum e != 0 vanish; degree-one vertex vanishes
    e = (1, 1, 1, kappa - 2) if kappa > 2 else (1,1,1,1)
    S = 0
    for aj, ajp, bi, bip in product(range(p), repeat=4):
        S += chi(e[0], aj+bi) * chi(e[1], ajp+bi) * chi(e[2], aj+bip) * chi(e[3], ajp+bip)
    print(f"    sum e = {sum(e) % kappa} (nonzero): |S| = {abs(S):.2e}")
    S = 0  # path of 3 cells: (i,j),(i,j'),(i',j'); alpha_j has degree 1
    for aj, ajp, bi, bip in product(range(p), repeat=4):
        S += chi(1, aj+bi) * chi(kappa-1, ajp+bi) * chi(1, ajp+bip)
    print(f"    path support (degree-one vertex): |S| = {abs(S):.2e}")

# ---------- C ----------
print("C. primes p = 1 (mod kappa) below X at which small primes are kappa-th powers")
X = 60000
for kappa in (4, 5, 7):
    ps = [p for p in range(kappa+1, X) if p % kappa == 1 and is_prime(p)]
    def kth_power(a, p): return pow(a, (p-1)//kappa, p) == 1
    f2 = sum(kth_power(2, p) for p in ps)
    f235 = sum(all(kth_power(a, p) for a in (2, 3, 5)) for p in ps)
    big = [p for p in ps if all(kth_power(a, p) for a in (2, 3, 5, 7, 11, 13))]
    print(f"  kappa={kappa}: {len(ps)} primes; 2 is a power at {f2} ({f2/len(ps):.3f}, 1/kappa={1/kappa:.3f});"
          f" 2,3,5 all powers at {f235} ({f235/len(ps):.4f}, kappa^-3={kappa**-3:.4f});"
          f" first p with 2..13 all powers: {big[:3]}")

# ---------- D ----------
print("D. barrier values against known E_2 data")
data = {4: 53, 5: 181, 6: 859, 7: 3221, 8: 14281, 9: 18199}
for k, m in data.items():
    print(f"  kappa={k}: max known E_2 = {m}; kappa^kappa/2 = {k**k/2:.4g}; (kappa-1)kappa^kappa = {(k-1)*k**k:.4g};"
          f" 1.5 kappa^((kappa+1)/2) = {1.5*k**((k+1)/2):.4g}; 2^(-1/(k-1)) kappa^kappa = {2**(-1/(k-1))*k**k:.4g}")
