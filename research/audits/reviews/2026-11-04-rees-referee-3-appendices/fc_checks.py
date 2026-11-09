"""Referee 3: exact checks for appendix-free-coordinate.tex.

Run: /opt/anaconda3/bin/python -I fc_checks.py
"""
from fractions import Fraction as Fr
from itertools import product, combinations
from math import comb, gcd, log, ceil, prod
import random

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

def rref(rows, p):
    A = [list(r) for r in rows]
    nr = len(A); nc = len(A[0]) if A else 0
    piv = []; r = 0
    for col in range(nc):
        sel = None
        for i in range(r, nr):
            if A[i][col] % p:
                sel = i; break
        if sel is None: continue
        A[r], A[sel] = A[sel], A[r]
        inv = pow(A[r][col], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(nr):
            if i != r and A[i][col] % p:
                f = A[i][col]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(col); r += 1
        if r == nr: break
    return A[:r], piv

# ---- eq fc-q and fc-params ----
for p in [5, 7, 11, 13, 31, 101, 1031]:
    for k in range(1, p):
        if (p - 1) % k: continue
        q = Fr((p - 1) // k + 1, p)
        check(Fr(1, k) <= q <= 1, "q range")
for u in range(2, 121):
    check(Fr(16*u*u - 1, u) >= 15*u, "h>=15u")
    t1 = Fr((4*u)**(u-1) * 4, 15**(2*u) * u**(u+1))
    t2 = Fr((4*u)**(u-1) * 2, (16*u*u)**(u+1))
    check(t1 == Fr(4**u, 225**u) / u**2, "fc closed 1")
    check(t2 == Fr(2 * 4**(u-1), 16**(u+1) * u**(u+3)), "fc closed 2")
    check(t1 + t2 < Fr(15, 100000), "fc sum")
u = 2
print("fc-params u=2:", float(Fr(4**u, 225**u) / u**2), float(Fr(2 * 4**(u-1), 16**(u+1) * u**(u+3))))
bnd = Fr(4, 15**4 * 8) + Fr(2, 64**3)
print("fc-uniform(a) bound:", float(bnd), "2^-14 =", 2**-14)
check(bnd < Fr(1, 2**14), "fc-uniform(a)")

# ---- Lemma fc-rref (b) and fc-moment exhaustive small case ----
def fc_case(p, k, a, M):
    h = (p - 1) // k
    Pk = sorted({pow(x, k, p) for x in range(1, p)})
    D = set(Pk) | {0}
    q = Fr(h + 1, p)
    from collections import defaultdict
    by_pat = defaultdict(list)
    for X in product(range(p), repeat=a * M):
        rows = [X[i*M:(i+1)*M] for i in range(a)]
        R, piv = rref(rows, p)
        by_pat[tuple(piv)].append(R)
    for piv, Rs in by_pat.items():
        r = len(piv)
        if r == 0: continue
        last = piv[-1]
        Fp_ = list(range(last + 1, M))
        if not Fp_: continue
        # law of the free block
        cnt = defaultdict(int)
        for R in Rs:
            cnt[tuple(R[i][l] for i in range(r) for l in Fp_)] += 1
        vals = set(cnt.values())
        check(len(cnt) == p ** (r * len(Fp_)) and len(vals) == 1, f"rref law {p,k,a,M,piv}")
        # moment of N on the free block, n = len(Fp_)
        n = len(Fp_)
        Ns = []
        for R in Rs:
            N = 0
            for x in product(Pk, repeat=n):
                if all((-sum(R[i][l] * xl for l, xl in zip(Fp_, x))) % p in D for i in range(r)):
                    N += 1
            Ns.append(N)
        EN = Fr(sum(Ns), len(Ns)); Var = Fr(sum(t*t for t in Ns), len(Ns)) - EN*EN
        check(EN == h**n * q**r, f"EN {p,k,a,M,piv}")
        check(Var == h**(n+1) * (q**r - q**(2*r)), f"Var {p,k,a,M,piv}")
for case in [(5, 2, 1, 3), (5, 2, 2, 3), (7, 3, 1, 3), (7, 2, 2, 3), (5, 4, 1, 3)]:
    fc_case(*case)

# ---- Lemma fc-rref(c): Pr[n'<n0] <= (p^a-1)/((p-1)p^L) exhaustively ----
for (p, a, M, n0) in [(3, 2, 4, 2), (3, 2, 4, 3), (5, 1, 3, 2), (3, 3, 4, 1), (3, 2, 3, 2)]:
    bad = 0; tot = 0
    for X in product(range(p), repeat=a * M):
        rows = [X[i*M:(i+1)*M] for i in range(a)]
        R, piv = rref(rows, p)
        last = piv[-1] + 1 if piv else 0
        nprime = M - last
        bad += nprime < n0; tot += 1
    L = M - n0
    check(Fr(bad, tot) <= Fr(p**a - 1, (p - 1) * p**L), f"rref(c) {p,a,M,n0}")

# ---- Lemma fc-choice: beta <= tau and the size bound, random parameters ----
def beta_fc(p, k, M, n0, a):
    h = (p - 1) // k; q = Fr(h + 1, p); L = M - n0
    return Fr(4) / (Fr(h) ** (n0 - 1) * q ** a) + Fr(p ** a - 1, (p - 1) * p ** L)
rng = random.Random(7)
primes = [5, 7, 11, 13, 31, 41, 61, 101, 151, 1031, 5281, 65537]
for _ in range(400):
    p = rng.choice(primes)
    ks = [k for k in range(2, p - 1) if (p - 1) % k == 0]
    if not ks: continue
    k = rng.choice(ks); ga = rng.randint(1, 20); tau = Fr(1, rng.choice([1, 2, 9, 10**3, 10**9, 10**30]))
    h = (p - 1) // k; q = Fr(h + 1, p)
    target = 8 * q ** (-ga) / tau
    kk = 0
    while Fr(h) ** kk < target: kk += 1
    n0 = 1 + kk
    j = 0
    while Fr(p) ** j < 2 / tau: j += 1
    M = n0 + ga + j
    check(beta_fc(p, k, M, n0, ga) <= tau, "fc-choice beta")
    bound = ga * (1 + 2 * log(k) / log(p / k)) + 3 * log(8 / float(tau)) / log(p / k) + 3
    check(M <= bound + 1e-9, f"fc-choice size {p,k,ga,tau}")

# ---- Lemma fc-zero-sum (a) exhaustive and (b) ----
for (p, a, M) in [(3, 1, 2), (3, 2, 3), (5, 1, 3), (3, 2, 4), (5, 2, 3)]:
    bad = tot = 0
    for X in product(range(p), repeat=a * M):
        cols = [X[i*a:(i+1)*a] for i in range(M)]
        found = False
        for s in range(1, M + 1):
            for T in combinations(range(M), s):
                if all(sum(cols[i][j] for i in T) % p == 0 for j in range(a)):
                    found = True; break
            if found: break
        bad += not found; tot += 1
    check(Fr(bad, tot) <= Fr(p**a - 1, 2**M - 1), f"zero-sum(a) {p,a,M}")
# (b): Davenport constant of C_p^g is g(p-1)+1 for p=3,g=2 (M=5) and p=5,g=1 (M=5)
for (p, a) in [(3, 2), (5, 1), (3, 1)]:
    M = a * (p - 1) + 1
    for X in product(range(p), repeat=a * M):
        cols = [X[i*a:(i+1)*a] for i in range(M)]
        found = any(all(sum(cols[i][j] for i in T) % p == 0 for j in range(a))
                    for s in range(1, M + 1) for T in combinations(range(M), s))
        check(found, f"zero-sum(b) {p,a}")

# ---- Prop rc-lower example ----
p = 5; D = {0, 1, 4}; P2 = [1, 4]
check(all((-2 * x) % p not in D for x in P2), "rc-lower example")
check(beta_fc(5, 2, 2, 1, 1) >= 1 and beta_fc(5, 2, 2, 2, 1) >= 1, "rc-lower beta>=1")
check(sum(Fr(1, p**i) for i in range(1, 60)) < Fr(1, p - 1), "geom")

# ---- Lemma fc-split-law: remark example 69/325 ----
p, k = 5, 2
Pk = {1, 4}; D = {0, 1, 4}
ys = sorted(product(range(p), repeat=2))  # lexicographic order
nonab = zero = 0
for l1 in product(range(p), repeat=2):
    for l2 in product(range(p), repeat=2):
        row = [l1[0], l2[0]]
        R, piv = rref([row], p)
        if not piv:
            Fset = [0, 1]
        else:
            Fset = list(range(piv[-1] + 1, 2))
        if len(Fset) < 1:
            continue  # n' < n0: abort
        acc = []
        for y in ys:
            if any(y[l] not in Pk for l in Fset): continue
            if piv:
                i = piv[0]
                if y[i] not in D: continue
                if (y[i] + sum(R[0][l] * y[l] for l in Fset)) % p: continue
                if any(y[l] for l in range(2) if l not in Fset and l != i): continue
            acc.append(y)
        if not acc:
            continue  # all trials rejected: abort
        pick = None
        for y in acc:
            if (y[0] * l1[1] + y[1] * l2[1]) % p == 0:
                pick = y; break
        if pick is None: pick = acc[0]
        z = ((pick[0] * l1[0] + pick[1] * l2[0]) % p, (pick[0] * l1[1] + pick[1] * l2[1]) % p)
        check(z[0] == 0, "z first coord")
        nonab += 1; zero += (z == (0, 0))
print("split remark example: Pr[z=0 | no abort] =", Fr(zero, nonab), "nonabort banks", nonab)

# ---- Prop fc-split-node(c): nu bounds ----
for Ms in [(2, 2), (2, 3, 4), (5, 2, 7, 3), (3, 3, 3, 3, 3), (10, 2), (2, 10)]:
    k_ = len(Ms); M = prod(Ms)
    n = [prod(Ms[j+1:]) for j in range(k_)]
    nu = sum(n)
    check(nu <= Fr(M - 1, min(Ms) - 1) and nu <= M - 1 and nu <= 2 * prod(Ms[1:]), f"nu {Ms}")

# ---- Remark fc-tradeoff(a): sum_{i<K}(a-i+1) = K(2a-K+3)/2 ----
for a in range(0, 30):
    for K in range(0, a + 1):
        check(2 * sum(a - i + 1 for i in range(K)) == K * (2*a - K + 3), "tradeoff count")
# (b): (1+A)(1+a-A) >= (1+a/4)(1+3a/4) >= (a/2+1)(a/4+1) for A in [a/4,3a/4]
for a in range(1, 60):
    for A4 in range(a, 3 * a + 1):  # A = A4/4
        A = Fr(A4, 4)
        check((1 + A) * (1 + a - A) >= (1 + Fr(a, 4)) * (1 + Fr(3 * a, 4)) >= (Fr(a, 2) + 1) * (Fr(a, 4) + 1), "tradeoff(b)")

print("ALL OK" if ok else "SOME CHECK FAILED")
