"""Referee B: accounting for Theorem B, in exact integer arithmetic where it matters.
N(q) = min{N : N - 5q/4 >= 15/4 + sqrt(N)}  <=>  4N - 5q - 15 >= 0 and (4N - 5q - 15)^2 >= 16 N.
Per-stage cost cap (proof): floor((4/5) N + (4/5) sqrt N), N = N(q).
guarantee(n) = max over stages (consumed + pool) and final consumed + 1, stages q = n, n-2, ... >= 3,
then 1-d rounds of q + 1 columns for q = 2, 1.
Compared with: the note's wnest_p.guarantee; the closed form of Theorem B; KOW Thm 3.7 at q = 5
(min over r of (0.8/(1-5^-r)) n(n+1)/2 + r(n+1)); KOW Remark 3.8; SIMPLE5's guarantee.
"""
import math, sys
from functools import lru_cache
sys.path.insert(0, '../2026-11-08-rees-sde-fq-nest')
from wnest_p import guarantee as g_note, pool_size
from simple5 import guarantee_simple

@lru_cache(maxsize=None)
def isqrt_floor_cost(N):
    # floor(0.8 N + 0.8 sqrt N) = floor((4N + 4 sqrt N)/5): find largest c with 5c <= 4N + 4 sqrt(N)
    c = (4 * N) // 5
    while 5 * (c + 1) - 4 * N <= 0 or (5 * (c + 1) - 4 * N) ** 2 <= 16 * N:
        c += 1
    return c


@lru_cache(maxsize=None)
def Nq(q):
    N = max(0, (5 * q + 15) // 4 + math.isqrt(5 * q // 4))  # <= 5q/4 + 15/4 + sqrt(5q/4) <= minimum
    while not (4 * N - 5 * q - 15 >= 0 and (4 * N - 5 * q - 15) ** 2 >= 16 * N):
        N += 1
    return N

@lru_cache(maxsize=None)
def g_ref(n):
    total = worst = 0; q = n
    while q >= 3:
        N = Nq(q); worst = max(worst, total + N); total += isqrt_floor_cost(N); q -= 2
    while q >= 1:
        worst = max(worst, total + q + 1); total += q + 1; q -= 1
    return max(worst, total + 1)

closed = lambda n: n * n / 4 + 0.754 * (n + 2) ** 1.5 + 5.75 * n + math.sqrt(2 * n) + 13
closed_exact = lambda n: n * n / 4 + (8 * math.sqrt(2) / 15) * (n + 2) ** 1.5 + 5.75 * n + math.sqrt(2 * n) + 13

def kow37(n):
    return min(0.8 / (1 - 5.0 ** -r) * n * (n + 1) / 2 + r * (n + 1) for r in range(1, 40))

@lru_cache(maxsize=None)
def kow38(n):
    # Remark 3.8 recursion with r_0 = 1, r_i = ceil(log_5(i+1)): m_l = sum_{i=0}^l ((1-q^-1)/(1-q^-r_i)) i + r_i
    tot = 0.0
    for i in range(0, n + 1):
        r = 1 if i == 0 else math.ceil(math.log(i + 1, 5) - 1e-12)
        while 5 ** r < i + 1:
            r += 1
        tot += 0.8 / (1 - 5.0 ** -r) * i + r
    return tot

# 1. N(q) vs code, and N(q) <= 1.25 q + sqrt(2q) + 7
badN = [q for q in range(1, 100000) if not (4 * Nq(q) <= 5 * q + 28 + 4 * math.sqrt(2 * q))]
mis = [q for q in range(1, 3000) if Nq(q) != pool_size(5, q)]
print('N(q) <= 5q/4 + sqrt(2q) + 7 for 1 <= q < 1e5:', not badN, badN[:5])
print('referee N(q) == note pool_size(5,q) for q < 3000:', not mis, mis[:5])
# analytic: N0 = ceil(5q/4 + sqrt(2q) + 6) satisfies the defining inequality for q >= 1
badA = []
for q in range(1, 100000):
    N0 = math.ceil(1.25 * q + math.sqrt(2 * q) + 6)
    if not (4 * N0 - 5 * q - 15 >= 0 and (4 * N0 - 5 * q - 15) ** 2 >= 16 * N0):
        badA.append(q)
print('N0 = ceil(5q/4 + sqrt(2q) + 6) feasible (so N(q) <= 5q/4 + sqrt(2q) + 7) for q < 1e5:', not badA)
# the note's literal argument uses N = ceil(5q/4 + sqrt(2q) + 7); that only gives N(q) <= ... + 8
# 2. per-stage cost cap vs q + (8/5) sqrt(2q) + 8
badc = [q for q in range(3, 100000) if isqrt_floor_cost(Nq(q)) > q + 1.6 * math.sqrt(2 * q) + 8]
print('cost cap <= q + (8/5) sqrt(2q) + 8 for 3 <= q < 1e5:', not badc, badc[:5])
# 3. guarantee: referee vs note, and vs closed form
misg = [n for n in list(range(3, 400)) + [600, 1000, 3000] if g_ref(n) != g_note(5, n)[0]]
print('referee guarantee == note guarantee for 3 <= n < 400 and n = 600, 1000, 3000:', not misg, misg[:5])
slack = min((closed(n) - g_ref(n), n) for n in range(3, 5001))
slack2 = min((closed_exact(n) - g_ref(n), n) for n in range(3, 5001))
print(f'min (closed form - guarantee) over 3 <= n <= 5000: {slack[0]:.2f} at n = {slack[1]}; with 8sqrt2/15 exact: {slack2[0]:.2f}')
print('8 sqrt2/15 =', 8 * math.sqrt(2) / 15, '(note rounds to 0.754, which is >= the exact value: OK)')
# 4. comparisons
print('  n  guarantee  closed  KOW3.7  KOW3.8  SIMPLE5   (ratios / n^2)')
for n in (10, 20, 40, 60, 100, 200, 300, 1000, 3000):
    g = g_ref(n); c = closed(n); k = kow37(n); k8 = kow38(n); s5 = guarantee_simple(n)
    print(f'{n:5d} {g:9d} {c:9.0f} {k:9.0f} {k8:9.0f} {s5:8d}   {g/n/n:.3f} {c/n/n:.3f} {k/n/n:.3f} {k8/n/n:.3f} {s5/n/n:.3f}')
def first_below(f, g, lo=3, hi=5001):
    last_bad = None
    for n in range(lo, hi):
        if not f(n) < g(n):
            last_bad = n
    return last_bad
print('guarantee(n) >= KOW3.7(n) last at n =', first_below(g_ref, kow37))
print('closed(n) >= KOW3.7(n) last at n =', first_below(closed, kow37))
print('guarantee(n) >= KOW3.8(n) last at n =', first_below(g_ref, kow38))
print('closed(n) >= KOW3.8(n) last at n =', first_below(closed, kow38))
print('SIMPLE5(n) >= KOW3.7(n) last at n =', first_below(guarantee_simple, kow37))
print('SIMPLE5(n) >= guarantee(n) last at n =', first_below(guarantee_simple, g_ref))
print('max SIMPLE5(n) - n^2/4 - 3n/2 over 3..5000:', max(guarantee_simple(n) - n * n / 4 - 1.5 * n for n in range(3, 5001)))
