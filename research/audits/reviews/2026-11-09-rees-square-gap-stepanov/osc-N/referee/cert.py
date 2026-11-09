"""Referee C: independent re-implementation of the Theorem C certificate.
Lambda_M = E_S sum_c (b_c)_M  (S ordered distinct in F_p, t in F_p minus S, profile mod diag).
Double count: Lambda_M = (p)_M/(p)_k * avg_U sum_d (n_d(U))_k,  d in Z_k^{M-1}, sum_d n_d = p-M.
Lower: balanced split (discrete convexity of (x)_k).  Lambda_2 exact.  Upper m>=3 via Weil:
 n_d - (p-m)/D = D^{-1} sum_{r != 0} w^{-r.d} Sigma_r,  |Sigma_r| <= (l(r)-1) sqrt p + (m - l(r))
 (l(r) = #{a : e_a != 0}, e = (-sum r, r)), which is the referee's sharper count; 'theirs' uses
 (m-1) sqrt p for every r.  Max of convex sum over the box -> chord bound (integers).
"""
import sys, math, itertools
from fractions import Fraction as Fr

def ff(x, n):
    r = 1
    for i in range(n): r *= (x - i)
    return r
def g(x, k): return ff(x, k) if x >= k else 0
def isprime(n): return n > 1 and all(n % d for d in range(2, int(n**.5) + 1))

def G(N, D, k):
    q, r = divmod(N, D)
    return (D - r) * g(q, k) + r * g(q + 1, k)

def Edev(k, p, m, mode):
    D = k ** (m - 1)
    if mode == 'theirs':
        return (1 - Fr(1, D)) * (m - 1) * math.sqrt(p)
    tot = 0.0
    for r in itertools.product(range(k), repeat=m - 1):
        if not any(r): continue
        e = [(-sum(r)) % k] + list(r)
        l = sum(1 for x in e if x)
        tot += (l - 1) * math.sqrt(p) + (m - l)
    return tot / D

def chord(N, D, k, lo, hi):
    lo = max(lo, 0)
    if hi <= lo: return D * g(hi, k)
    return D * g(lo, k) + (N - D * lo) * Fr(g(hi, k) - g(lo, k), hi - lo)

def low(k, p, M):
    if M == 1: return Fr(p - k)
    if M == 2: return up(k, p, 2, 'x')
    return Fr(ff(p, M) * G(p - M, k ** (M - 1), k), ff(p, k))

def up(k, p, m, mode):
    if m == 1: return Fr(p - k)
    if m == 2:
        h = (p - 1) // k
        return Fr(p * (p - 1) * (g(h - 1, k) + (k - 1) * g(h, k)), ff(p, k))
    D = k ** (m - 1); nb = Fr(p - m, D); E = Edev(k, p, m, mode)
    return Fr(ff(p, m), ff(p, k)) * chord(p - m, D, k, math.ceil(nb - E), math.floor(nb + E))

def best(k, p, mode):
    b = (0, None)
    for M in range(2, k):
        lo = low(k, p, M)
        for m in range(1, M):
            c = ff(k - 1 - m, M - m)
            u = up(k, p, m, mode)
            if c > 0 and u > 0:
                rat = float(lo / (c * u))
                if rat > b[0]: b = (rat, (m, M))
    return b

if __name__ == '__main__':
    k = int(sys.argv[1]); pmax = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else 'ref'
    pig = (k - 1) * k ** (k - 1) + k - 1
    last_fail = None; first = None
    for p in range(k + 1, pmax + 1):
        if p % k == 1 and isprime(p):
            r, mM = best(k, p, mode)
            if r > 1 and first is None: first = p
            if r <= 1: last_fail = p
    print(f'k={k} mode={mode}: first certified prime={first}, last uncertified prime<= {pmax}: {last_fail}, pigeonhole bound p>{pig}')
