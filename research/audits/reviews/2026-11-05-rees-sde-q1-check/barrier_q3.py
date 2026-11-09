"""Sharper necessary condition for a q = 3 heavy stall whose Y-fallback fails.
At q = 3 the optimal absorption load is >= 3 iff q+ = 0 and every round except one (l*) has all its
columns in U (Rado / matroid intersection with capacity 2: the only violating set is A = {l*}).
A round at quotient q_l with a circuit of k_l + 1 columns spans U_{l-1} + k_l dims, so a round whose
columns lie in U (dim r-3) has k_l <= q_l - 3.  Gain g = min(2, k).  Maximise sum(k_l + 1) over round
sequences from quotient r to 3, with one unconstrained round; compare with the columns the Y-failure
needs: |Rcols| + |T| >= f(r) - r + b - f(b) + 1, |T| <= 3, b = r - 3 - eps, eps >= 1."""
from functools import lru_cache
from myq1 import f


def best(r):
    @lru_cache(None)
    def g(q, used):          # max cost from quotient q down to 3; used = l* already placed
        if q == 3:
            return 0
        if q < 3:
            return -10 ** 9
        out = -10 ** 9
        for k in range(1, q + 1):
            gain = min(2, k)
            if q - gain < 3:
                continue
            if k <= q - 3:
                out = max(out, k + 1 + g(q - gain, used))
            if not used:
                out = max(out, k + 1 + g(q - gain, True))
        return out
    return g(r, False)


first = None
for r in range(7, 41):
    mx = best(r)
    poss = []
    for eps in range(1, r - 3 - 2 + 1):
        b = r - 3 - eps
        if b < 2:
            continue
        need = f(r) - r + b - f(b) + 1
        if mx + 3 >= need:
            poss.append((b, eps, mx + 3 - need))
    print("r=%2d  max|Rcols|=%3d  possible (b,eps,slack): %s" % (r, mx, poss[:4]))
    if poss and first is None:
        first = r
print("smallest r admitting a q=3 heavy stall with failing Y-count (necessary condition):", first)
