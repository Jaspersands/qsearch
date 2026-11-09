#!/usr/bin/env python
"""s3 (9 Nov 2026 proof check): independent recomputation of the mixed instance of
Proposition prop:mixed-schedule used in Table tab:fcs-budget (uniform-kernel columns) and of
the claims in the paragraph after the proposition (appendix-schedule3.tex), plus the trial
range 2^223.8 .. 2^236.0 of Section sec:schedule3 for part (iv) at u = 18.
Exact integers / Fractions for every comparison; floats only for printing log2 values."""
from fractions import Fraction as Fr
from math import gcd, log2
import sys

g_prof = [19, 17, 16, 14, 12, 9, 6, 3, 1]       # g_1 .. g_9 ; m = g_1
m, c = g_prof[0], 9
gd = {d: g_prof[d-1] for d in range(2, c+1)}
eps = Fr(1, 3)

def ceil_log2(x):
    x = Fr(x); B = 0
    while Fr(2)**B < x: B += 1
    return B

def lg(x):
    x = Fr(x)
    n, dd = x.numerator, x.denominator
    def l2(k):
        b = k.bit_length()
        if b <= 1000: return log2(k)
        return (b - 1000) + log2(k >> (b - 1000))
    return l2(n) - l2(dd)

def isprime(n):
    if n < 2: return False
    for q in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n % q == 0: return n == q
    d, s = n-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in [2,3,5,7,11,13,17,19,23,29,31,37]:
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def B_is(k, a):
    L = (k+1).bit_length() - 1
    if (1 << L) < k+1: L += 1          # ceil(log2(k+1))
    return (k**(k*(k-1)//2) * (a+1)**k) ** L

def combined(p, d):
    k = gcd(d, p-1); g = gd[d]
    if k == 1: return ('lin', g+1)
    if p >= 16 * k**(2*k+2): return ('S2', (g+1)*((k-1)*g+1))
    return ('S1', B_is(k, g))

def beta(p, d, M):
    k = gcd(d, p-1); h = (p-1)//k; g = gd[d]
    assert M > g
    return Fr(4*h*p**g, (h+1)**M - 1) + Fr(p**g - 1, (p-1)*p**M)

def instance(p, maxadd=100000):
    types, Ms = {}, {}
    for d in range(2, c+1):
        t, Mc = combined(p, d)
        k = gcd(d, p-1); u = max(2, k, gd[d]+1)
        if p >= 16*u*u and 4*u < Mc:
            t, Mc = 'S3', 4*u
        types[d], Ms[d] = t, Mc
    added = {d: 0 for d in Ms}
    def nds():
        n = {}; acc = 1
        for d in range(2, c+1):
            n[d] = acc; acc *= Ms[d]
        return n, acc
    it = 0
    while True:
        n, P = nds()
        terms = {d: n[d]*beta(p, d, Ms[d]) for d in Ms if types[d] == 'S3'}
        lhs = sum(terms.values(), Fr(0))
        if lhs <= Fr(1, 64) or not terms: break
        dmax = max(terms, key=lambda d: terms[d])
        Ms[dmax] += 1; added[dmax] += 1; it += 1
        if it > maxadd: raise RuntimeError("no convergence")
    n, P = nds()
    nS3 = sum(n[d] for d in Ms if types[d] == 'S3'); nS2 = sum(n[d] for d in Ms if types[d] == 'S2')
    B = ceil_log2(64*max(1, 3*nS3 + nS2))
    mprime = m + ceil_log2(3/eps)
    Q = 4*mprime*c*P
    trials = [4 * gcd(d, p-1)**Ms[d] * B for d in Ms if types[d] == 'S3']
    tree = lhs + (3*nS3 + nS2) * Fr(1, 2**B)
    return dict(types=types, Ms=Ms, added=added, lhs=lhs, B=B, Q=Q, trials=max(trials) if trials else None,
                tree=tree, mprime=mprime, nS3=nS3)

table = {5281: (50.3, 128.2), 2**31-1: (50.9, 121.6), 2**61-1: (52.9, 128.3), 2**127-1: (49.9, 115.2)}
print("Table tab:fcs-budget, uniform-kernel columns (paper value in brackets):")
lhs_max = None; tree_rng = []
for p in [11, 1031, 5281, 2**31-1, 2**61-1, 2**127-1]:
    r = instance(p)
    s3 = [d for d in r['types'] if r['types'][d] == 'S3']
    s2 = [d for d in r['types'] if r['types'][d] == 'S2']
    line = f"p={p}: S3 grades {s3}, S2 grades {s2}, added {sum(r['added'].values())}"
    if s3:
        line += (f", log2 Q={lg(r['Q']):.2f} [{table[p][0]}], log2 trials={lg(r['trials']):.2f} [{table[p][1]}]"
                 f", B={r['B']}, log2 lhs={lg(r['lhs']):.2f}, log2 tree-abort={lg(r['tree']):.3f}")
        lhs_max = lg(r['lhs']) if lhs_max is None else max(lhs_max, lg(r['lhs']))
        tree_rng.append(lg(r['tree']))
        line += f"  M={[r['Ms'][d] for d in range(2, c+1)]}"
    else:
        line += "  (no uniform-kernel node: table shows a dash)"
    print(line)
print(f"max log2 lhs over S3 rows = {lhs_max:.2f} (paper: at most 2^-67); tree-abort range "
      f"[{min(tree_rng):.2f}, {max(tree_rng):.2f}] (paper: 2^-6.91 .. 2^-6.38)")

# p = 151 claim: M_9 = 12, 60 columns added at grade 9
r = instance(151)
print(f"p=151: types {r['types']}, added {r['added']}, M_9={r['Ms'][9]}")
# lhs with M_9 = 12 before adding
n9 = 1
for d in range(2, 9): n9 *= combined(151, d)[1]
print(f"p=151: log2 of n_9*beta_9(12) = {lg(n9*beta(151, 9, 12)):.1f} (paper: far above 1)")

# 226 primes below 3600 with some column added
if len(sys.argv) > 1 and sys.argv[1] == "scan":
    added_primes = []
    for p in range(11, 3600):
        if not isprime(p): continue
        r = instance(p)
        if sum(r['added'].values()) > 0: added_primes.append(p)
    print(f"primes 11 <= p < 3600 with some column added: {len(added_primes)} (paper: 226); "
          f"first {added_primes[:10]}, last {added_primes[-5:]}")

# Section sec:schedule3: part (iv) at u = 18 (M = 72), per-node trials 4 kappa^M B at the four primes
u = 18; M = 4*u; B = ceil_log2(64 * M**(c-1))
vals = []
for p in [5281, 2**31-1, 2**61-1, 2**127-1]:
    assert p >= 16*u*u
    kmax = max(gcd(d, p-1) for d in range(2, c+1))
    vals.append(lg(4 * kmax**M * B))
    print(f"part (iv) u=18 p={p}: max kappa={kmax}, B={B}, log2(4 kappa^M B)={vals[-1]:.2f}")
print(f"range {min(vals):.1f} .. {max(vals):.1f} (paper: 223.8 .. 236.0); u=18 needs g_2 = {gd[2]} <= u-1 = {u-1}")
