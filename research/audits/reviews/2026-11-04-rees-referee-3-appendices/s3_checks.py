"""Referee 3: exact checks of the displayed inequalities of appendix-schedule3.tex.

Run: /opt/anaconda3/bin/python -I s3_checks.py
Exact integer / Fraction arithmetic throughout.
"""
from fractions import Fraction as Fr
from itertools import product
from math import comb, gcd, ceil, log2
import sys

def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0: return False
        d += 2
    return True

def next_prime(n):
    while not is_prime(n): n += 1
    return n

def clog2(x):  # exact ceil(log2(x)) for positive Fraction/int
    x = Fr(x); k = 0
    if x <= 1:
        while Fr(2) ** (k - 1) >= x: k -= 1
        return k
    while Fr(2) ** k < x: k += 1
    return k

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

# Lemma s3-mu(a): (16u^2)^{3u}/(2u)^{4u-1} = 2^{8u+1}u^{2u+1}
for u in range(2, 121):
    check(Fr((16*u*u)**(3*u), (2*u)**(4*u-1)) == 2**(8*u+1) * u**(2*u+1), f"s3-mu identity u={u}")

# Lemma s3-tree(c) closed forms and sum < 1/64; Prop s3-uniform(a),(b)
for u in range(2, 121):
    M = 4*u
    lhs1 = Fr((4*u)**(u-1) * 4, 2**(8*u+1) * u**(2*u+1))
    lhs2 = Fr((4*u)**(u-1) * 2, (16*u*u)**(3*u+1))
    check(lhs1 == Fr(1, 2**(6*u+1) * u**(u+2)), f"tree term1 u={u}")
    check(lhs2 == Fr(1, 2**(10*u+5) * u**(5*u+3)), f"tree term2 u={u}")
    check(lhs1 + lhs2 < Fr(1, 64), f"tree bank sum u={u}")
    beta = Fr(4, 2**(8*u+1) * u**(2*u+1)) + Fr(2, (16*u*u)**(3*u+1))
    check(beta <= Fr(1, 2**17), f"beta<=2^-17 u={u}")
    for c in range(2, u+1):
        T = (M**(c-1) - 1) // (M - 1)
        B = clog2(64 * M**(c-1))
        check(T <= M**(c-1), "T<=M^{c-1}")
        check(3*T*Fr(1, 2**B) <= Fr(3, 64), f"3T2^-B u={u} c={c}")
        check(B == 6 + clog2(Fr(M)**(c-1)), "B identity")
        check(B <= 6 + (u-1)*clog2(4*u), f"B<=6+(u-1)ceil u={u} c={c}")
        # N_instr <= 13 m' M^{c-1}  (per m'=1)
        check(4*(M**(c-1) + (M+1)*T) + 1 <= 13 * M**(c-1), f"Ninstr u={u} c={c}")
u = 2
print("u=2 bank terms:", Fr(1, 2**13*2**4), Fr(1, 2**25*2**13))

# Lemma s3-mu(b) and (a) at concrete primes, every kappa | p-1 with kappa <= u, a in {0,u-1}
for u in range(2, 26):
    M = 4*u
    for p in (next_prime(16*u*u), 2**61-1):
        for kappa in range(1, u+1):
            if (p-1) % kappa: continue
            h = (p-1)//kappa
            check(Fr((h+1)**M - 1, 2*p**M) >= Fr(1, 4*kappa**M), f"accept u={u} p={p} k={kappa}")
            for a in (0, u-1):
                mu = Fr((h+1)**M - 1, h * p**a)
                check(mu >= 2**(8*u+1) * u**(2*u+1), f"mu u={u} p={p} k={kappa} a={a}")

# Lemma s3-moment exhaustively: p=5, kappa=2, M=3, a=1 and a=2 (all label matrices)
def moment_case(p, kappa, M, a):
    h = (p-1)//kappa
    Pk = {0} | {pow(x, kappa, p) for x in range(1, p)}
    S = [y for y in product(range(p), repeat=M) if any(y) and all(v in Pk for v in y)]
    Ns = []
    rk_def = 0
    for X in product(range(p), repeat=a*M):
        rows = [X[i*M:(i+1)*M] for i in range(a)]
        N = sum(1 for y in S if all(sum(r[j]*y[j] for j in range(M)) % p == 0 for r in rows))
        Ns.append(N)
    tot = len(Ns)
    EN = Fr(sum(Ns), tot)
    VarN = Fr(sum(n*n for n in Ns), tot) - EN*EN
    D = Fr((h+1)**M - 1, h)
    mu = D / p**a
    check(EN == h*mu, f"EN {p,kappa,M,a}")
    check(VarN == h*h*D*Fr(1, p**a)*(1 - Fr(1, p**a)), f"VarN {p,kappa,M,a}")
    check(VarN <= h*EN, "Var<=hEN")
    pr = Fr(sum(1 for n in Ns if n < EN/2), tot)
    check(pr <= 4/mu, "Chebyshev")
    return EN, VarN, pr, 4/mu
for case in [(5,2,3,1), (5,2,3,2), (7,3,3,1), (5,4,3,1)]:
    print("moment", case, moment_case(*case))

# Lemma s3-moment(d) chain: (p^a-1)/(p-1) <= 2p^{a-1}
for p in (3,5,7,11,101):
    for a in range(1,6):
        check(Fr(p**a-1, p-1) <= 2*p**(a-1), "d chain")

# Lemma s3-root(b): s_neq = (p-1)/2 for every pair of distinct roots, p odd up to 101
for p in [q for q in range(3, 102) if is_prime(q)]:
    sq = {pow(x, 2, p) for x in range(1, p)}
    chi = lambda x: 0 if x % p == 0 else (1 if x % p in sq else -1)
    for r1 in range(p):
        for r2 in range(p):
            if r1 == r2: continue
            sne = sum(1 for dl in range(p) if chi(r1+dl)*chi(r2+dl) == -1)
            if sne != (p-1)//2:
                check(False, f"root split p={p}")
                break

# Lemma s3-node(c): ML(4/9)^{B+ceil log2 ML} <= 2^-B
for M in (8, 12, 72, 200):
    for Lk in range(1, 8):
        for B in range(1, 60):
            e = B + clog2(M*Lk)
            check(M*Lk*Fr(4,9)**e <= Fr(1, 2**B), "root cap")

# Remark s3-caveat: p=67, kappa=2, M=8, a=1
p, kappa, M = 67, 2, 8
P = {0} | {pow(x, 2, p) for x in range(1, p)}
check(len(P) == 34, "|P|=34")
check((p - 1) % 4 == 2 and pow(p-1, (p-1)//2, p) == p-1, "-1 nonsquare mod 67")
# x = e1+e2 : y1 = -y2 with y1,y2 in P forces both 0
pairs = [(a1, a2) for a1 in P for a2 in P if (a1 + a2) % p == 0]
check(pairs == [(0, 0)], "e1+e2 forces 0")
print("caveat ratio", Fr(34**7-1, 34**6-1).__float__())

# Restart: C(4m',3m') 16^{-3m'} <= 2^{-2m'}, and 32^{-3m'} version, m' <= 300
for mp in range(1, 301):
    check(comb(4*mp, 3*mp) * Fr(1, 16**(3*mp)) <= Fr(1, 4**mp), f"restart16 {mp}")
    check(comb(4*mp, 3*mp) * Fr(1, 4**(3*mp)) <= Fr(1, 4**mp), f"restart4 {mp}")

# Prop s3-uniform(e): (c-1)c(c+1)(c+2)/6 <= u^4 for c<=u
for u in range(2, 200):
    check((u-1)*u*(u+1)*(u+2)//6 <= u**4, "bracket count")

print("ALL OK" if ok else "SOME CHECK FAILED")
