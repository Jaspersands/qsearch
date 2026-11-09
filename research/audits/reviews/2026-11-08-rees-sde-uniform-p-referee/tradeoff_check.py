"""Referee check of section 4 (tradeoff): own D_J recursion, own exact LW test, admissible J under
  (a) Theorem A + Corollary L1 : LW_E(p) >= p/(2 kappa^E)  and  p >= kappa^E (E a + 2)
  (b) conditional (Q-loc)      : LW_E(p) >= N_loc + 1      and  (p-1)/kappa >= N_loc + 1
with max(kappa,3) <= J <= max(max(kappa,3), ceil(log_kappa a)).  Also the closed bound
D_J(a) <= a^2/(2(J-1)) + O(a) and the J=3 identity D_3(a) = floor((a+2)^2/4) (checked numerically),
and the time-per-level caveat: expected rejection draws p/(|Good|-|Bad|) at p = kappa^E(Er+2) with
|Good| = p/(2 kappa^E) and |Bad| = Er/2 (worst case allowed by the hypotheses) is p itself.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from thresholds_exact import lw_ge, old_cond, maxcross  # noqa (prints its table)


def DJ(q, J, _t={}):
    tab = _t.setdefault(J, [0])
    while len(tab) <= q:
        x = len(tab)
        best = 0
        for k in range(1, x + 1):
            best = max(best, k + 1 + tab[x - min(J - 1, k)])
        tab.append(best)
    return tab[q]


def F(a, J):
    return DJ(a, J) + max(2, 2 * J - 4) * a


print()
for a in (100, 1000, 10000):
    assert DJ(a, 3) == (a + 2) ** 2 // 4, (a, DJ(a, 3))
for J in (3, 4, 5, 6, 7):
    worst = max(DJ(a, J) - a * a / (2 * (J - 1)) for a in range(1, 400))
    print("J=%d: max_{a<400} D_J(a) - a^2/(2(J-1)) = %.1f (linear-term size)" % (J, worst))

print()
for k in (2, 3):
    for a in (1000, 10000):
        for p in (10 ** 6, 10 ** 7, 10 ** 8, 10 ** 10, 10 ** 12):
            lo = max(k, 3)
            hi = max(lo, math.ceil(math.log(a, k)))
            best_a = best_b = None
            for J in range(lo, hi + 1):
                E = 3 * J - 2
                if old_cond(p, k, E) and p >= k ** E * (E * a + 2):
                    best_a = (J, F(a, J))
                N = maxcross(E, k)
                if lw_ge(p, k, E, N) and p - 1 >= k * (N + 1):
                    best_b = (J, F(a, J))
            print("kappa=%d a=%-5d p=1e%-2d tri=%-9d (a) %s   (b) %s" % (k, a, round(math.log10(p)),
                                                                     (a + 1) * (a + 2) // 2, best_a, best_b))

print()
print("Time caveat for Corollary L1 at its own threshold p = kappa^E (E r + 2), kappa=2, J=3, r=40:")
k, J, r = 2, 3, 40
E = 3 * J - 2
p = k ** E * (E * r + 2)
G = p / (2 * k ** E)
bad = E * r / 2
print("  p = %d, |Good| >= p/(2k^E) = %.1f, |Bad| <= Er/2 = %.1f, |Good|-|Bad| >= %.1f: rejection sampling "
      "needs up to p/(|Good|-|Bad|) = %.0f expected trials per level (Theorem A: <= 2 kappa^E = %d)"
      % (p, G, bad, G - bad, p / (G - bad), 2 * k ** E))
p2 = 2 * E * r * k ** E
G2 = p2 / (2 * k ** E)
print("  at Theorem A's own p = 2 E r kappa^E = %d: |Good|-|Bad| >= %.1f, trials <= %.1f = 4 kappa^E"
      % (p2, G2 - bad, p2 / (G2 - bad)))
