"""Referee's exact check of the Lemma W consequences used in section 2 / Corollary A.

Claim: if p >= 8 kappa^{2E} E^2 then for every 1 <= e <= E
   kappa^{-e} (p - e - (kappa^e - 1)(e - 1) sqrt p) >= p / (2 kappa^E),            (*)
hence G*_E(p) >= p/(2 kappa^E).  Also the least integer p for which (*) holds for all e <= E
(the 'exact Weil threshold' of weil_thresholds.out), for E = 5, 7 and kappa = 2, 3.

Everything in exact integer arithmetic: (*) <=> A := 2 kappa^{E-e}(p - e) - p >= 0 and
A^2 >= (2 kappa^{E-e} (kappa^e - 1)(e - 1))^2 p.
"""
import math


def holds(p, k, E, e):
    A = 2 * k ** (E - e) * (p - e) - p
    if A < 0:
        return False
    Bc = 2 * k ** (E - e) * (k ** e - 1) * (e - 1)
    return A * A >= Bc * Bc * p


def holds_all(p, k, E):
    return all(holds(p, k, E, e) for e in range(1, E + 1))


def least_p(k, E):
    lo, hi = 1, 1
    while not holds_all(hi, k, E):
        hi *= 2
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if holds_all(mid, k, E):
            hi = mid
        else:
            lo = mid
    return hi


def main():
    ok = True
    for k in (2, 3, 4, 5):
        for E in range(2, 31):
            p0 = 8 * k ** (2 * E) * E * E
            # (*) at the threshold and on a geometric grid above it; the function
            # p - e - B sqrt p - p kappa^{e-E}/2 is increasing in p once p >= (B/(2(1-kappa^{e-E}/2)))^2,
            # which is below p0, so checking p0 suffices; the grid is a safety net.
            for f in (1, 2, 5, 10, 100, 10 ** 4, 10 ** 8):
                if not holds_all(p0 * f, k, E):
                    ok = False
                    print("FAIL", k, E, f)
    print("p >= 8 kappa^{2E} E^2 implies min_e LW(p,e) >= p/(2 kappa^E), kappa<=5, E<=30:", ok)
    for k in (2, 3):
        for E in (5, 6, 7, 8, 10):
            lp = least_p(k, E)
            # monotone beyond: spot check
            mono = all(holds_all(int(lp * f), k, E) for f in (1, 1.3, 2, 7, 50, 1000))
            print("kappa=%d E=%2d least p with (*) for all e<=E: %d   (8k^{2E}E^2 = %d)  ratio %.2f  monotone-above %s  per-pass<=1/2 needs p >= %d r"
                  % (k, E, lp, 8 * k ** (2 * E) * E * E, 8 * k ** (2 * E) * E * E / lp, mono, 2 * E * k ** E))
    # the E = 5 numbers of the Q1 referee: 61,524 and 3,748,116
    print("E=5 kappa=2:", least_p(2, 5), " E=5 kappa=3:", least_p(3, 5))
    # kappa/(p-1) <= 2 kappa^E / p for E >= 2, p >= 2 (so max(...) is the G* term)
    ok2 = all(k * p <= 2 * k ** E * (p - 1) for k in (2, 3, 5) for E in (2, 4, 7) for p in range(3, 5000))
    print("kappa/(p-1) <= 2kappa^E/p (E>=2):", ok2)


main()
