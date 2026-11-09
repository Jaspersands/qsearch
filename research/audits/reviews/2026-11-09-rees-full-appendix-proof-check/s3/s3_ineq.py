#!/usr/bin/env python
"""s3 (9 Nov 2026 proof check): exact-integer checks of the displayed inequalities of
appendix-schedule3.tex (Lemmas s3-moment(d), s3-mu, s3-root(b), s3-node(c), s3-tree(c),
Prop s3-uniform(a)-(b), eq s3-ninstr, the restart bounds, Remark s3-caveat).
Finite checks only: they can falsify, never prove.  All comparisons in int / Fraction."""
from fractions import Fraction as Fr
from math import comb, gcd
import sys

def isprime(n):
    if n < 2: return False
    small = [2,3,5,7,11,13,17,19,23,29,31,37]
    for q in small:
        if n % q == 0: return n == q
    d, s = n-1, 0
    while d % 2 == 0: d//=2; s+=1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def ceil_log2_frac(x):
    """least integer B with 2^B >= x, x a positive Fraction or int"""
    x = Fr(x); B = 0
    if x <= 1:
        while Fr(2)**(B-1) >= x: B -= 1
        return B
    while Fr(2)**B < x: B += 1
    return B

fails = []
def check(cond, msg):
    if not cond:
        fails.append(msg); print("FAIL:", msg)

UMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 80
for u in range(2, UMAX+1):
    M = 4*u
    # identity in Lemma s3-mu(a)
    check((16*u*u)**(3*u) == 2**(8*u+1) * u**(2*u+1) * (2*u)**(4*u-1), f"identity u={u}")
    mu_lb = 2**(8*u+1) * u**(2*u+1)
    # Lemma s3-tree(c) displayed simplification and the 1/64 bound
    lhs = Fr((4*u)**(u-1)) * (Fr(4, mu_lb) + Fr(2, (16*u*u)**(3*u+1)))
    rhs = Fr(1, 2**(6*u+1) * u**(u+2)) + Fr(1, 2**(10*u+5) * u**(5*u+3))
    check(lhs == rhs, f"tree display u={u}")
    check(lhs <= Fr(1, 64), f"tree bank <= 1/64 u={u}")
    # Prop s3-uniform(a): beta_d <= 2^-17
    beta_ub = Fr(4, mu_lb) + 2*Fr(1, (16*u*u)**(3*u+1))
    check(beta_ub < Fr(1, 2**17), f"beta<=2^-17 u={u}")
    for c in range(2, u+1):
        T = sum(M**j for j in range(c-1))
        check(T == (M**(c-1)-1)//(M-1) and T <= M**(c-1), f"T u={u} c={c}")
        B = ceil_log2_frac(64 * M**(c-1))
        check(Fr(1, 2**B) <= Fr(1, 64*M**(c-1)), f"2^-B u={u} c={c}")
        check(3*T*Fr(1, 2**B) <= Fr(3, 64), f"3T2^-B u={u} c={c}")
        # B <= 6 + (u-1) ceil(log2 4u)
        cl = ceil_log2_frac(4*u)
        check(B <= 6 + (u-1)*cl, f"B bound u={u} c={c}")
        # eq s3-ninstr: per tree M^{c-1} + (M+1)T <= 3 M^{c-1}
        check(M**(c-1) + (M+1)*T <= 3*M**(c-1), f"ninstr u={u} c={c}")
        # node caps (Lemma s3-node(c)) for every kappa <= c
        for kap in range(1, c+1):
            L = max(1, ceil_log2_frac(kap)) if kap > 1 else 1
            K = 4 * kap**M * B
            R = 2*(B + ceil_log2_frac(M*L))
            F = K*M + M*L*R
            capF = B + ceil_log2_frac(F)
            check(F * Fr(1, 2**capF) <= Fr(1, 2**B), f"fairbit cap u={u} c={c} k={kap}")
            Lr = ceil_log2_frac(kap) if kap > 1 else 0
            check(M * Lr * Fr(2, 3)**R <= Fr(1, 2**B), f"root cap u={u} c={c} k={kap}")
print("inequalities for u <= %d: %s" % (UMAX, "all pass" if not fails else "%d FAIL" % len(fails)))

# exact mu and acceptance at actual primes (Lemma s3-mu): least prime >= 16u^2, and two Mersenne primes
def least_prime_ge(n):
    while not isprime(n): n += 1
    return n
cnt = 0
for u in range(2, 41):
    M = 4*u
    mu_lb = 2**(8*u+1) * u**(2*u+1)
    for p in (least_prime_ge(16*u*u), 2**61-1, 2**127-1):
        for kap in range(1, u+1):
            if (p-1) % kap: continue
            h = (p-1)//kap
            acc = Fr((h+1)**M - 1, 2*p**M)
            check(acc >= Fr(1, 4*kap**M), f"accept u={u} p={p} k={kap}")
            for a in range(0, u):
                mu = Fr((h+1)**M - 1, h * p**a)
                check(mu >= mu_lb, f"mu u={u} p={p} k={kap} a={a}")
                cnt += 1
print("exact mu/acceptance checks at real primes:", cnt, "cases;", "pass" if not fails else "FAIL")

# Lemma s3-moment(d) inequality chain for small p, a, M
for p in (2,3,5,7,11,13):
    for a in range(0, 6):
        for M in range(a+1, a+8):
            if a == 0: continue
            v1 = Fr(p**a - 1, p-1) / p**M
            check(v1 <= Fr(2*p**(a-1), p**M) <= Fr(2*p**a, p**M), f"rank chain p={p} a={a} M={M}")

# Lemma s3-root(b): sum_delta chi((delta+r1)(delta+r2)) = -1 and s_ne = (p-1)/2, all p < 400
def chi(x, p):
    x %= p
    if x == 0: return 0
    return 1 if pow(x, (p-1)//2, p) == 1 else -1
nroot = 0
for p in range(3, 260):
    if not isprime(p): continue
    for r1 in (0, 1):
        for r2 in range(p):
            if r2 == r1: continue
            ssum = sum(chi((d+r1)*(d+r2), p) for d in range(p))
            sne = sum(1 for d in range(p) if (d+r1) % p and (d+r2) % p and chi(d+r1,p) != chi(d+r2,p))
            check(ssum == -1 and 2*sne == p-1, f"root count p={p} r1={r1} r2={r2}")
            nroot += 1
    check(Fr(p-1, 2*p) >= Fr(1, 3), f"(p-1)/2p>=1/3 p={p}")
print("root-lemma counts:", nroot, "pairs;", "pass" if not fails else "FAIL")

# restart bounds
for mp in range(1, 400):
    check(Fr(comb(4*mp, 3*mp), 16**(3*mp)) <= Fr(1, 2**(2*mp)), f"restart16 m'={mp}")
    check(Fr(comb(4*mp, 3*mp), 4**(3*mp)) <= Fr(1, 2**(2*mp)), f"restart4 m'={mp}")
    check(Fr(comb(4*mp, 3*mp), 32**(3*mp)) <= Fr(1, 2**(2*mp)), f"restart32 m'={mp}")
# 2^-2m' <= (eps/3)^2 <= eps/3 and rank failure with m' = m + ceil(log2(3/eps))
for kk in range(2, 3000):
    eps = Fr(1, kk)
    t = ceil_log2_frac(3/eps)
    check(Fr(1, 2**(2*t)) <= (eps/3)**2 <= eps/3, f"eps k={kk}")
    check(Fr(1, 2**t) <= eps/3, f"rank eps k={kk}")
print("restart/eps checks:", "pass" if not fails else "FAIL")

# Remark s3-caveat at p = 67, kappa = 2, M = 8
p, kap, M = 67, 2, 8
D = sorted({pow(x, kap, p) for x in range(1, p)} | {0})
check(len(D) == 34, "|D|=34")
pairs = sum(1 for y1 in D for y2 in D if (y1 + y2) % p == 0)
check(pairs == 1, "only (0,0) solves y1=-y2 in D^2 at p=67")
check(chi(-1, 67) == -1, "-1 nonsquare mod 67")
N1, N2 = 34**7 - 1, 34**6 - 1
print("caveat: N(e1)=34^7-1=%d, N(e1+e2)=34^6-1=%d, ratio %.3f" % (N1, N2, N1/N2))

print("TOTAL FAILS:", len(fails))
