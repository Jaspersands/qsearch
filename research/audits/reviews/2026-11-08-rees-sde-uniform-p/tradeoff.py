"""Column count F(a) = D_J(a) + max(2, 2J-4) a at the largest admissible J, for given (kappa, a, p):
  old  : Theorem A   (LW >= p/(2 kappa^E) and p >= 2 E a kappa^E)
  L1   : Corollary L1 (LW >= p/(2 kappa^E) and p >= kappa^E (E a + 2))       [zero-error pass]
  cond : conditional on fan-in <= N_loc(E, kappa) (LW >= N_loc + 1, (p-1)/kappa >= N_loc + 1)
with J >= max(kappa, 3) and J <= max(max(kappa,3), ceil(log_kappa a)) (time poly).  '-' = no J
admissible (then only the triangular count (a+1)(a+2)/2 is available)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from thresholds import LW, maxcross  # noqa  (prints its table on import)
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A"))


def DJ(q, J, _t={}):
    tab = _t.setdefault(J, [0])
    while len(tab) <= q:
        x = len(tab)
        best = x + 1 + tab[x - J + 1] if x >= J - 1 else 0
        for k in range(1, min(x, J - 2) + 1):
            best = max(best, k + 1 + tab[x - k])
        tab.append(best)
    return tab[q]


def F(a, J):
    return DJ(a, J) + max(2, 2 * J - 4) * a


def best(k, a, p, mode):
    lo = max(k, 3)
    hi = max(lo, math.ceil(math.log(a, k)))
    out = None
    for J in range(lo, hi + 1):
        E = 3 * J - 2
        lw = LW(p, k, E)
        if mode == "old":
            ok = lw >= p / (2 * k ** E) and p >= 2 * E * a * k ** E
        elif mode == "L1":
            ok = lw >= p / (2 * k ** E) and p >= k ** E * (E * a + 2)
        else:
            N = maxcross(E, k)
            ok = lw >= N + 1 and (p - 1) / k >= N + 1
        if ok:
            out = (J, F(a, J))
    return out


print()
for k in (2, 3):
    for a in (100, 1000, 10000):
        for p in (10 ** 6, 10 ** 7, 10 ** 8, 10 ** 10, 10 ** 12, 10 ** 15):
            row = []
            for mode in ("old", "L1", "cond"):
                b = best(k, a, p, mode)
                row.append("%-6s J=%-2s F=%-9s" % (mode, b[0] if b else "-", b[1] if b else "-"))
            print("kappa=%d a=%-6d p=1e%-2d tri=%-10d %s" % (k, a, round(math.log10(p)),
                                                         (a + 1) * (a + 2) // 2, " | ".join(row)))
