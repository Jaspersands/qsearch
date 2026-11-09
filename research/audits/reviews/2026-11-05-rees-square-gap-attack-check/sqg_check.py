#!/usr/bin/env python
"""Independent checks for 2026-11-05-rees-square-gap-attack-check.md (tiny, seconds).

Written separately from the attack report's scripts (none of their code is reused).

T1. The law P(x) = t^|x|(1-t)^(k-|x|) - (-1)^(k-|x|) t^k on {0,1}^k, exact rationals:
    total 1, P(all ones) = 0, every proper marginal is the product law, nonnegative
    iff t <= 1/2 (k = 2..8, t on a grid of 40ths), and the |x| = k-2 atom is the
    negative one for t > 1/2 (the converse). Uniqueness of the fibre: the space of
    signed measures on {0,1}^k with all proper marginals zero is one-dimensional
    (rank computation).
T1b. Real instance: kappa = 4, p in {101, 109, 113} (all <= 4^4/2 = 128, eta_2 < 1).
    The exact law of n_0 over all y in {0} x F_p^3, the one-column factorial moments,
    their one-column brackets, and the bracket containment for m = 2 (the only order
    m >= 2 with eta_m < 1 there) under independent copies, for |S| = 1..4.
    Also the step-1 inequality eta_{kappa-1} >= 1 at p = kappa^kappa/2, kappa = 3..40,
    and the step-4 merge inequalities (i),(ii) for all a + b = m with eta_m < 1 at
    p in {primes = 1 mod kappa near kappa^kappa/2, /8, /64}, kappa = 3..12.
T2. Latin lemma behind the Chebotarev barrier, brute force: at (kappa,p) = (3,7),
    (3,13), (4,13), (4,17), (5,11), every (alpha, beta) with beta_0 = 0 whose cells all
    lie in one coset c Q_0 union {0} and that satisfies the pattern -(i+j) has all
    cells zero. Plus the illustration figures (fraction of p = 1 mod 4 with 2, 3, 5
    quartic residues) to 10^7.
P3. 4-cycle frequencies, brute force over the four cycle variables, against the
    closed forms, for every admissible (e1,e2,e3,e4) at (3,7),(3,13),(4,13),(5,11),
    (6,13), and |S| = p^2 (p-1) for each.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
from math import comb, sqrt, isqrt
import cmath, math, sys
import numpy as np

def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    r = isqrt(n)
    f = 3
    while f <= r:
        if n % f == 0: return False
        f += 2
    return True

def primroot(p):
    fs = [f for f in range(2, p) if (p-1) % f == 0 and isprime(f)]
    for g in range(2, p):
        if all(pow(g, (p-1)//f, p) != 1 for f in fs): return g

def index_table(p):
    g = primroot(p); ind = [None]*p; x = 1
    for k in range(p-1):
        ind[x] = k; x = x*g % p
    return ind

# ---------------- T1 ----------------
print("T1. explicit (k-1)-wise independent law")
bad = 0
for k in range(2, 9):
    pts = list(product((0, 1), repeat=k))
    for num in range(1, 40):
        t = Fr(num, 40)
        P = {x: t**sum(x)*(1-t)**(k-sum(x)) - (-1)**(k-sum(x))*t**k for x in pts}
        if sum(P.values()) != 1 or P[(1,)*k] != 0: bad += 1
        nonneg = min(P.values()) >= 0
        if nonneg != (t <= Fr(1, 2)): bad += 1
        if t > Fr(1, 2):
            x = (1,)*(k-2) + (0, 0)
            if not P[x] < 0: bad += 1
        # proper marginals: drop one coordinate at a time suffices (all smaller ones follow)
        for drop in range(k):
            for y in product((0, 1), repeat=k-1):
                x0 = y[:drop] + (0,) + y[drop:]; x1 = y[:drop] + (1,) + y[drop:]
                if P[x0] + P[x1] != t**sum(y)*(1-t)**(k-1-sum(y)): bad += 1
    # rank of the marginal map onto all (k-1)-marginals
    rows = []
    for drop in range(k):
        for y in product((0, 1), repeat=k-1):
            r = [0]*(2**k)
            for b in (0, 1):
                x = y[:drop] + (b,) + y[drop:]
                r[int("".join(map(str, x)), 2)] = 1
            rows.append(r)
    rk = np.linalg.matrix_rank(np.array(rows, dtype=float))
    if 2**k - rk != 1: bad += 1
    print(f"  k={k}: kernel dimension of the (k-1)-marginal map = {2**k - rk}")
print(f"  T1 failures: {bad}")

# ---------------- T1b ----------------
def E_err(l, p, k):
    return (l - 1 - l/k + k**(-l))*sqrt(p) + l/k - l*k**(-l)

def eta(m, p, k):
    return k**m*E_err(m, p, k)/(p - m)

def rho(m, p, k):
    return (p - m)/(p*k**m)

print("T1b. kappa = 4 real instances: exact law of n_0, brackets, independence")
k = 4
for p in (101, 109, 113):
    ind = index_table(p); h = (p-1)//k
    cos = np.array([-1] + [ind[x] % k for x in range(1, p)])   # coset index, -1 at 0
    Q0 = np.where(cos == 0)[0]
    # n_0(y) = #{x in Q_0 : x + y_i in Q_{-i}, i = 1,2,3}
    # A_i[y] = indicator vector over x in Q0 of (x + y in Q_{-i})
    A = []
    for i in (1, 2, 3):
        target = (-i) % k
        M = np.zeros((p, len(Q0)), dtype=np.int64)
        for y in range(p):
            M[y] = (cos[(Q0 + y) % p] == target)
        A.append(M)
    # distribution of n_0 over (y1,y2,y3): for each (y1,y2) form B = A1[y1]&A2[y2], then n = A3 @ B
    hist = np.zeros(h + 1, dtype=np.int64)
    for y1 in range(p):
        B1 = A[0][y1]
        B12 = A[1] * B1          # rows y2
        N = B12 @ A[2].T         # [y2, y3] counts
        hist += np.bincount(N.ravel(), minlength=h + 1)
    tot = hist.sum(); assert tot == p**3
    nu = hist/tot
    ns = np.arange(h + 1)
    q = nu[1:].sum(); En = (ns*nu).sum()
    fm = {a: sum(comb(int(n), a)*nu[n] for n in range(h + 1)) for a in range(0, 4)}
    print(f"  p={p}: P(n0>0)={q:.4f} E n0={En:.4f} (h^k/p^(k-1)={h**k/p**(k-1):.4f}); eta_2={eta(2,p,k):.3f} eta_3={eta(3,p,k):.3f}")
    # one-column brackets
    for a in (1, 2):
        lo = comb(h, a)*(rho(a,p,k)*(1-eta(a,p,k)))**(k-1)
        hi = comb(h, a)*(rho(a,p,k)*(1+eta(a,p,k)))**(k-1)
        print(f"    one-column a={a}: {lo:.4f} <= {fm[a]:.4f} <= {hi:.4f}: {lo - 1e-12 <= fm[a] <= hi + 1e-12}")
    # independent copies, m = 2, |S| = r
    for r in range(1, k + 1):
        val = r*fm[2] + comb(r, 2)*fm[1]**2
        lo = comb(r*h, 2)*(rho(2,p,k)*(1-eta(2,p,k)))**(k-1)
        hi = comb(r*h, 2)*(rho(2,p,k)*(1+eta(2,p,k)))**(k-1)
        print(f"    |S|={r}, m=2 under independence: {lo:.3f} <= {val:.3f} <= {hi:.3f}: {lo <= val <= hi}")

print("T1b'. step 1: eta_{k-1} at p = k^k/2 (must be >= 1); step 4 merge inequalities")
mn = min((eta(kk-1, kk**kk/2, kk), kk) for kk in range(3, 41))
print(f"  min over 3 <= k <= 40 of eta_(k-1)(k^k/2) = {mn[0]:.4f} at k = {mn[1]}")
fails = 0; pairs = 0; worst = 0.0
for kk in range(3, 13):
    for div in (2, 16, 128, 1024):
        p0 = int(kk**kk/div)
        p = p0 - (p0 - 1) % kk
        while p > kk + 1 and not isprime(p): p -= kk
        if p <= kk + 1: continue
        for m in range(2, kk):
            if eta(m, p, kk) >= 1: break
            for a in range(1, m):
                b = m - a; pairs += 1
                ea, eb, em = eta(a,p,kk), eta(b,p,kk), eta(m,p,kk)
                ra, rb, rm = rho(a,p,kk), rho(b,p,kk), rho(m,p,kk)
                if ra*rb*(1-ea)*(1-eb) < rm*(1-em): fails += 1
                if ra*rb*(1+ea)*(1+eb) > rm*(1+em): fails += 1
                worst = max(worst, (ra*rb*(1+ea)*(1+eb)/rm - 1)/em if em > 0 else 0)
print(f"  {pairs} pairs, {fails} failures, largest (upper ratio - 1)/eta_m = {worst:.4f} (proof bound 0.4)")

# ---------------- T2 ----------------
print("T2. Latin lemma: cells in one coset union {0} + Latin pattern => all cells zero")
for kk, p in ((3, 7), (3, 13), (4, 13), (4, 17), (5, 11), (6, 13)):
    ind = index_table(p)
    cos = [-1] + [ind[x] % kk for x in range(1, p)]
    found = 0; checked = 0
    # beta_0 = 0, so row 0 gives alpha_j in c Q_0 u {0}; given alpha the rows are independent.
    for c in range(kk):
        allowed = [u for u in range(p) if u == 0 or cos[u] == c]
        for al in product(allowed, repeat=kk):
            checked += 1
            ok_rows = True; nonzero = False
            for i in range(kk):
                bs = [0] if i == 0 else range(p)
                good = []
                for b in bs:
                    cells = [(al[j] + b) % p for j in range(kk)]
                    if all(u == 0 or (cos[u] == c and c == (-(i+j)) % kk) for j, u in enumerate(cells)):
                        good.append(any(cells))
                if not good: ok_rows = False; break
                if any(good): nonzero = True
            if ok_rows and nonzero: found += 1
    print(f"  (k,p)=({kk},{p}): {checked} choices (c, alpha); {found} admit a pattern-respecting single-coset configuration with a nonzero cell")

print("T2'. fraction of p = 1 mod 4 below 10^7 with 2, 3, 5 all quartic residues (Chebotarev 1/64)")
X = 10**7
sv = np.ones(X + 1, dtype=bool); sv[:2] = False
for i in range(2, isqrt(X) + 1):
    if sv[i]: sv[i*i::i] = False
ps = [int(p) for p in np.nonzero(sv)[0] if p % 4 == 1]
c2 = c235 = 0
for p in ps:
    e = (p - 1)//4
    if pow(2, e, p) == 1:
        c2 += 1
        if pow(3, e, p) == 1 and pow(5, e, p) == 1: c235 += 1
print(f"  {len(ps)} primes; 2: {c2/len(ps):.4f} (1/4); 2,3,5: {c235/len(ps):.5f} (1/64 = {1/64:.5f}), count {c235}")
p = 196681
print(f"  p=196681 prime={isprime(p)}, p%4={p%4}; quartic residues among 2..16: {[a for a in range(2,17) if pow(a,(p-1)//4,p)==1] == list(range(2,17))}")

# ---------------- P3 ----------------
print("P3. 4-cycle frequencies (four cycle variables), brute force vs closed form")
for kk, p in ((3, 7), (3, 13), (4, 13), (5, 11), (6, 13)):
    ind = index_table(p)
    om = cmath.exp(2j*math.pi/kk)
    def ch(s, u):
        u %= p
        if s % kk == 0: return 1.0
        return 0.0 if u == 0 else om**((s*ind[u]) % kk)
    def J(a, b):
        return sum(ch(a, w)*ch(b, 1 - w) for w in range(p))
    # precompute table T[s][u]
    T = np.array([[ch(s, u) for u in range(p)] for s in range(kk)])
    idx = np.add.outer(np.arange(p), np.arange(p)) % p   # [A, b] -> A + b
    worst = 0.0; n = 0; modbad = 0
    for e1, e2, e3, e4 in product(range(1, kk), repeat=4):
        if (e1 + e2 + e3 + e4) % kk: continue
        # row i: R1[A,B] = sum_b chi^e1(A+b) chi^e2(B+b);  row i': R2[A,B] = sum_b chi^e3(A+b) chi^e4(B+b)
        R1 = T[e1][idx] @ T[e2][idx].T
        R2 = T[e3][idx] @ T[e4][idx].T
        S = (R1*R2).sum()
        if (e1 + e2) % kk:
            pred = p*(p-1)*ch(e2 + e4, -1)*J(e1, e2)*J(e3, e4)
        else:
            pred = p*p*(p-1)
        worst = max(worst, abs(S - pred)); n += 1
        if abs(abs(S) - p*p*(p-1)) > 1e-6*p**3: modbad += 1
    print(f"  (k,p)=({kk},{p}): {n} tuples, max |brute - formula| = {worst:.1e}, modulus failures {modbad}")
