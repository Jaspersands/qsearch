"""Exact WNEST guarantee recursion vs the theorem's closed form and several readings of KOW's recursion (8)."""
import math
from fractions import Fraction
from functools import lru_cache
from wnest_ref import theorem_bound
LIM = 20000
@lru_cache(None)
def Nq(q):
    N = max(1, math.ceil(1.5 * q))
    while N - 1.5 * q < 3 + math.sqrt(N):
        N += 1
    assert N == 1 or (N - 1) - 1.5 * q < 3 + math.sqrt(N - 1)   # minimality
    return N
def guarantee(n):
    consumed, best, q = 0, 0, n
    while q > 0:
        if q >= 4:
            N = Nq(q); best = max(best, consumed + N)
            consumed += math.floor(2 * N / 3 + 2 * math.sqrt(N) / 3); q -= 2
        else:
            best = max(best, consumed + q + 1); consumed += q + 1; q -= 1
    return max(best, consumed + 1)
def t3(l):
    t = 0
    while 3 ** t < l + 1:
        t += 1
    return t
KL = [Fraction(1)]                       # KOW (8) literally, rational
for l in range(1, LIM + 1):
    KL.append(max(Fraction(l), KL[-1] + Fraction(2 * (l + 1), 3) + t3(l)))
KN = [1]                                 # the note's kow_recursion (wnest.py), re-typed
for l in range(1, LIM + 1):
    r = max(1, t3(l)); KN.append(max(l + r, KN[-1] + (l + r) * 2 * 3 ** (r - 1) // (3 ** r - 1)))
def kow_int(n):                          # integer: piece floor(2(l+1)/3)+t, pool l+t, +1 final column
    cons, best = 0, 0
    for l in range(n, 0, -1):
        t = t3(l); best = max(best, cons + l + t); cons += (2 * (l + 1)) // 3 + t
    return max(best, cons + 1)
def kow_closed(n):
    return ((n + 1) * (n + 2) + 1) / 3 + n * t3(n)
G = {n: guarantee(n) for n in range(4, 3000)}
bad = [n for n in G if G[n] > theorem_bound(n)]
print("n in [4,3000) with guarantee(n) > Theorem A bound:", bad)
print("max_n guarantee(n) - (n^2/4+(8/9)(n+2)^1.5+4n+12) over [4,3000):",
      round(max(G[n] - (n*n/4 + (8/9)*(n+2)**1.5 + 4*n + 12) for n in G), 2))
for name, K in (("KOW (8) literal, ceil", lambda n: math.ceil(KL[n])), ("KOW integer pieces", kow_int),
                ("note's kow_recursion", lambda n: KN[n])):
    lose = [n for n in G if G[n] >= K(n)]
    print(f"{name:24s}: n in [4,3000) with guarantee >= KOW: count {len(lose)}, largest {max(lose) if lose else None}"
          f"  -> guarantee < KOW for all {max(lose)+1 if lose else 4} <= n < 3000")
for n in (34, 35, 64, 100, 1000, 2999):
    print(f"  n={n:5d} guarantee={G[n]:8d} KOW(8)={math.ceil(KL[n]):8d} KOWint={kow_int(n):8d} "
          f"note's={KN[n]:8d} ThmA={theorem_bound(n):10.1f} KOWclosed={kow_closed(n):10.1f}")
lose = [n for n in range(4, LIM) if theorem_bound(n) >= kow_closed(n)]
print("Theorem A closed form < KOW closed form ((n+1)(n+2)+1)/3+n*ceil(log3(n+1)) for all n in (", max(lose), f", {LIM})")
lose = [n for n in range(4, LIM) if theorem_bound(n) >= KL[n]]
print("Theorem A closed form < KOW (8) literal for all n in (", max(lose), f", {LIM})")
