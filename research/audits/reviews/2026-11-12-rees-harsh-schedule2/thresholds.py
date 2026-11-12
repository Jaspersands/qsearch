"""Thresholds of appendix-schedule2 recomputed from the closed forms (own code, mpmath).

T_W(k): closed form of prop:app-s2-TW.
T_A(k): inf{p > k+1 : Delta(p) <= 1/2 and U_k(p) < k/(k-1)}, by bisection (U_k decreasing).
T_S(k): same with U_k(p) <= 1 + 1/(8k).
Also 16 k^(2k+2), 4 k^(2k+2), (k-1) k^k, k^(k+1), k^((k+1)/2).
"""
from mpmath import mp, mpf, sqrt, exp

mp.dps = 50


def Delta(k, p):
    return ((k - 1) * (k - 2) * sqrt(p) + 2 * (k - 1)) / (p - k - 1)


def Emax(k, p):
    D = Delta(k, p)
    u = mpf(1) / 2 - D / 3 - 1 / (k * (1 - D))
    v = D / (sqrt(k) * (1 - D))
    smax = sqrt(k) * D
    # maximise -u s^2 + v s on [0, smax]
    cands = [mpf(0), smax]
    if u > 0:
        s = v / (2 * u)
        if 0 <= s <= smax:
            cands.append(s)
    return max(-u * s * s + v * s for s in cands)


def U(k, p):
    p = mpf(p)
    return k ** k * p ** (k - 1) / (p - 1) ** k + exp(Emax(k, p))


def ok(k, p, target, strict):
    if p <= k + 1 or Delta(k, p) > mpf(1) / 2:
        return False
    u = U(k, p)
    return u < target if strict else u <= target


def bisect(k, target, strict):
    lo, hi = mpf(k + 1) + mpf('1e-9'), mpf(10) ** 40
    assert ok(k, hi, target, strict)
    for _ in range(400):
        mid = (lo + hi) / 2
        if ok(k, mid, target, strict):
            hi = mid
        else:
            lo = mid
    return hi


def TW(k):
    A = (k - 2) * k ** k + 1
    return ((A + sqrt(mpf(A) ** 2 + 4 * k ** k)) / 2) ** 2


if __name__ == '__main__':
    print('k  16k^(2k+2)  4k^(2k+2)  T_W  T_A  (k-1)k^k  T_S  k^(k+1)  k^((k+1)/2)')
    for k in range(2, 10):
        ta = bisect(k, mpf(k) / (k - 1), True)
        ts = bisect(k, 1 + mpf(1) / (8 * k), False)
        print(k, 16 * k ** (2 * k + 2), 4 * k ** (2 * k + 2), mp.nstr(TW(k), 6), mp.nstr(ta, 12),
              (k - 1) * k ** k, mp.nstr(ts, 6), k ** (k + 1), mp.nstr(mpf(k) ** (mpf(k + 1) / 2), 6))
    # spot checks of the values printed in the proof of prop:app-s2-TA(ii)
    for k in (3, 4, 5):
        P = k ** (k + 1)
        print('check', k, P, mp.nstr(Delta(k, P), 4), mp.nstr(U(k, P), 6), mp.nstr(mpf(k) / (k - 1) - U(k, P), 4))
    # monotonicity spot check of U on a grid (decreasing claim)
    for k in range(2, 10):
        prev = None
        bad = 0
        p = mpf(k + 2)
        while p < 1e12:
            if Delta(k, p) <= 0.5:
                u = U(k, p)
                if prev is not None and u > prev:
                    bad += 1
                prev = u
            p *= mpf('1.01')
        print('monotone-grid', k, 'violations', bad)
