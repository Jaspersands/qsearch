"""Least p (searched over integers, monotone region) with
min_{1<=e<=E} kappa^{-e}(p - e - (kappa^e-1)(e-1)sqrt p) >= p/(2 kappa^E),
i.e. G*_E(p) >= p/(2 kappa^E) by Lemma W; and the per-pass failure condition
(E r/2)(2 kappa^E/p) <= 1/2  <=>  p >= 2 E r kappa^E.  Compared with 8 kappa^{2E} E^2."""
import math


def lw(p, k, e):
    return k ** (-e) * (p - e - (k ** e - 1) * (e - 1) * math.sqrt(p))


def ok(p, k, E):
    return min(lw(p, k, e) for e in range(1, E + 1)) >= p / (2 * k ** E)


for k in (2, 3):
    for E in (5, 6, 7, 8, 10, 13, 16):
        lo, hi = 2, 2
        while not ok(hi, k, E):
            hi *= 2
        lo = hi // 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ok(mid, k, E):
                hi = mid
            else:
                lo = mid
        # confirm monotone beyond (spot check)
        assert all(ok(int(hi * f), k, E) for f in (1, 1.5, 2, 10, 100, 1e4))
        print("kappa=%d E=%2d  Weil threshold %.4g   8k^{2E}E^2 = %.4g   failure<=1/2 needs p >= %d r"
              % (k, E, hi, 8 * k ** (2 * E) * E * E, 2 * E * k ** E))
