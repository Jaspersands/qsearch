"""Recompute every closed-form threshold and constant of appendix-schedule2.tex.

Independent re-derivation (2026-11-03 check of Appendix A). Uses mpmath interval
arithmetic (mpmath.iv) for every inequality that the appendix states at a single
point, so those checks are rigorous; bisection values are 50-digit floats.
Run: /opt/anaconda3/bin/python -I thresholds.py
"""
import json
from fractions import Fraction
import mpmath
from mpmath import mp, iv, mpf

mp.dps = 50
iv.dps = 50
OUT = {}


def Delta(k, p, M=mp):
    return ((k - 1) * (k - 2) * M.sqrt(p) + 2 * (k - 1)) / (p - k - 1)


def Emax(k, D, M=mp):
    u = M.mpf(1) / 2 - D / 3 - 1 / (k * (1 - D))
    v = D / (M.sqrt(k) * (1 - D))
    smax = M.sqrt(k) * D
    # max of -u s^2 + v s on [0, smax]; evaluate at the endpoints and the vertex
    cands = [M.mpf(0), -u * smax ** 2 + v * smax]
    return u, v, smax, cands


def U(k, p):
    D = Delta(k, p)
    u, v, smax, cands = Emax(k, D)
    best = max(cands)
    if u > 0:
        s = v / (2 * u)
        if 0 <= s <= smax:
            best = max(best, v * v / (4 * u))
    return mp.mpf(k) ** k * mp.mpf(p) ** (k - 1) / (mp.mpf(p) - 1) ** k + mp.e ** best, D


def U_iv(k, p):
    """Rigorous upper bound on U_k(p) at an integer/rational point p."""
    p = iv.mpf(p)
    D = Delta(k, p, iv)
    u = iv.mpf(1) / 2 - D / 3 - 1 / (k * (1 - D))
    v = D / (iv.sqrt(k) * (1 - D))
    smax = iv.sqrt(k) * D
    # upper bound for max over sigma: if u>0 use v^2/(4u) (>= true max); else endpoint
    if u.a > 0:
        em = v * v / (4 * u)
        em2 = -u * smax ** 2 + v * smax
        em = em if em.b >= em2.b else em2  # both are upper bounds; v^2/4u always is
        em = v * v / (4 * u)
    else:
        em = -u * smax ** 2 + v * smax
        if em.a < 0:
            em = iv.mpf([0, em.b])
    first = iv.mpf(k) ** k * p ** (k - 1) / (p - 1) ** k
    return first + iv.exp(em), D


def bisect(f, lo, hi, iters=300):
    for _ in range(iters):
        mid = (lo + hi) / 2
        if f(mid):
            hi = mid
        else:
            lo = mid
    return hi


def TW(k):
    A = (k - 2) * k ** k + 1
    return ((A + mp.sqrt(A * A + 4 * k ** k)) / 2) ** 2


def cond_A(k):
    return lambda p: Delta(k, p) <= mpf(1) / 2 and U(k, p)[0] < mpf(k) / (k - 1)


def cond_S(k):
    return lambda p: Delta(k, p) <= mpf(1) / 2 and U(k, p)[0] <= 1 + mpf(1) / (8 * k)


def TA(k):
    return bisect(cond_A(k), mpf(k + 1) + mpf(10) ** -30, mpf(4) * k ** (k + 2))


def TS(k):
    return bisect(cond_S(k), mpf(k + 1) + mpf(10) ** -30, mpf(40) * k ** (k + 2))


def main():
    global bad
    # --- 1. closed form of E_kappa(l,p), exact in Q[sqrt p] (pairs (a,b) = a sqrt p + b)
    bad = 0
    for k in range(2, 16):
        for l in range(1, 2 * k + 3):
            sa = sum(Fraction(__import__('math').comb(l, s) * (k - 1) ** s * (s - 1), k ** l) for s in range(1, l + 1))
            sb = sum(Fraction(__import__('math').comb(l, s) * (k - 1) ** s * (l - s), k ** l) for s in range(1, l + 1))
            ca = l - 1 - Fraction(l, k) + Fraction(1, k ** l)
            cb = Fraction(l, k) - l * Fraction(1, k ** l)
            if (sa, sb) != (ca, cb):
                bad += 1
            if l <= k and not (ca <= l - 1 and cb <= 1):
                bad += 1
            if l == 1 and (ca, cb) != (0, 0):
                bad += 1
            if l == k:  # kappa^kappa E = ((k-2)k^k+1) sqrt p + k^k - k
                if (ca * k ** k, cb * k ** k) != ((k - 2) * k ** k + 1, k ** k - k):
                    bad += 1
    OUT['closed_form_E_failures'] = bad

    # --- 2. stage lemma chain at p = 4 k^{2k+2}: sqrt p >= 2 l k^l, sqrt p >= l+1; sum_{l=2}^k k^l <= 2k^k
    bad = 0
    for k in range(2, 60):
        sp = 2 * k ** (k + 1)
        for l in range(1, k + 1):
            if not (sp >= 2 * l * k ** l and sp >= l + 1 and Fraction(l, k ** l) <= 1):
                bad += 1
        s = sum(k ** l for l in range(2, k + 1))
        if not (s < Fraction(k ** (k + 1), k - 1) <= 2 * k ** k):
            bad += 1
    OUT['stage_lemma_chain_failures_k2_59'] = bad

    # --- 3. table
    rows = []
    for k in range(2, 10):
        rows.append(dict(k=k, sixteen=float(16 * mpf(k) ** (2 * k + 2)), TW=float(TW(k)), TA=float(TA(k)),
                         km1kk=(k - 1) * k ** k, TS=float(TS(k)),
                         ratio16_TW=float(16 * mpf(k) ** (2 * k + 2) / TW(k))))
    OUT['table'] = rows

    # --- 4. T_A > (k-1)k^k, T_A <= k^{k+1} (k>=3) rigorously at P, T_S <= 10 k^{k+1} / 9 k^{k+1}
    lo_fail, up_fail, ts10, ts9, margins = [], [], [], [], {}
    for k in range(2, 41):
        ta = TA(k)
        ts = TS(k)
        if not ta > (k - 1) * k ** k:
            lo_fail.append(k)
        if k >= 3:
            P = k ** (k + 1)
            Ub, Db = U_iv(k, P)
            if not (Ub.b < mpf(k) / (k - 1) and Db.b <= 0.5):
                up_fail.append(k)
            margins[k] = float(mpf(k) / (k - 1) - U(k, P)[0])
            if not ts <= 10 * mpf(k) ** (k + 1):
                ts10.append(k)
            if k >= 4 and not ts <= 9 * mpf(k) ** (k + 1):
                ts9.append(k)
        # at p = (k-1)k^k the condition must fail (lower bound proof)
        p0 = (k - 1) * k ** k
        if p0 > k + 1 and Delta(k, p0) <= 0.5 and U(k, p0)[0] < mpf(k) / (k - 1):
            lo_fail.append(('point', k))
    OUT['TA_lower_bound_failures'] = lo_fail
    OUT['TA_upper_bound_rigorous_failures_k3_40'] = up_fail
    OUT['margin_at_k^(k+1)'] = {k: margins[k] for k in (3, 4, 5, 6, 10, 20, 40)}
    OUT['TS_le_10k^(k+1)_failures'] = ts10
    OUT['TS_le_9k^(k+1)_failures_k>=4'] = ts9
    OUT['TS_over_k^(k+1)'] = {k: float(TS(k) / mpf(k) ** (k + 1)) for k in (2, 3, 4, 5, 8, 12, 20, 40)}

    # --- 5. point values quoted for kappa = 3,4,5
    pv = {}
    for k in (3, 4, 5):
        P = k ** (k + 1)
        u_, D_ = U(k, P)
        Ub, Db = U_iv(k, P)
        pv[k] = dict(P=P, Delta=float(D_), U=float(u_), U_iv_upper=float(Ub.b))
    OUT['point_values'] = pv

    # --- 6. constants of the k >= 6 argument, rigorous, k = 6..199
    # (precision raised: the terms k^{-k-1} reach 1e-460 at k = 199)
    iv.dps = 1000
    bad = []
    for k in range(6, 200):
        P = iv.mpf(k) ** (k + 1)
        D = Delta(k, P, iv)
        bound = iv.mpf(1.01) * iv.mpf(k) ** (iv.mpf(3 - k) / 2)
        exact_rhs = iv.mpf(k) ** ((iv.mpf(k) + 5) / 2) * (1 + 2 * iv.mpf(k) ** (-(iv.mpf(k) + 3) / 2)) / (
            iv.mpf(k) ** (k + 1) * (1 - 2 * iv.mpf(k) ** (-k)))
        u = iv.mpf(1) / 2 - D / 3 - 1 / (k * (1 - D))
        v = D / (iv.sqrt(k) * (1 - D))
        em = v * v / (4 * u)
        first = iv.mpf(k) ** k * P ** (k - 1) / (P - 1) ** k
        lhs = 2 * iv.mpf(k) ** (1 - k) + iv.mpf(2.4) * iv.mpf(k) ** (4 - k)
        ok = (D.b <= exact_rhs.a and exact_rhs.b <= bound.a and bound.b <= 0.1 and u.a >= 0.28
              and em.b <= 1.2 * iv.mpf(k) ** (2 - k) and em.b <= 1 and first.b <= (1 / iv.mpf(k) + 2 * iv.mpf(k) ** (-k - 1)).a
              and lhs.b < 1 and (k > 6 or lhs.b < 0.07))
        if not ok:
            bad.append(k)
    OUT['k_ge_6_constant_failures'] = bad
    iv.dps = 50

    # --- 7. TW identities
    bad = 0
    for k in range(2, 30):
        A = (k - 2) * k ** k + 1
        if A + k ** k != (k - 1) * k ** k + 1:
            bad += 1
        r = (A + mp.sqrt(A * A + 4 * k ** k)) / 2
        if abs(r * r - A * r - k ** k) > mpf(10) ** -30 * r * r:
            bad += 1
    OUT['TW_identity_failures'] = bad
    OUT['TW2'] = float(TW(2))

    print(json.dumps(OUT, indent=1, default=str))


if __name__ == "__main__":
    main()
