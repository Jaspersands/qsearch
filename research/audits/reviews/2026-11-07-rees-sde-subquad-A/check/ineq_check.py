"""Independent re-check of the count inequalities of section 3 of
2026-11-07-rees-sde-subquad-A.md (does not import dj_ineq.py or subquad.py).

D_J is computed by the literal definition D(q) = max_{1<=k<=q} (k+1+D(q-min(J-1,k))).
Checked (exact integer arithmetic):
  (C1)  D(r)-D(r-m) >= t(r+1) - (J-1)t(t-1)/2,  t = floor(m/(J-1)),  0<=m<=r
  (Y)   b + (C-1) r + D(q) - q >= F(b)   for 1<=b<=q, q+b<=r   (stall with eps>=0)
  (I1)  Lemma M bound <= F(r)-F(r-m) for c+1<=m<=q, r>=2q+2  (i.e. m <= (r-2)/2)
  (I2)  r-1 <= F(r)-F(r-m) for 2(J-1)<=m<=(r-2)/2
  (TS)  m+m' <= F(r)-F(r-m') for 1<=m'<=m<=2J-3, m'<=r
  (pi)  (C-1) r + D(q) - q >= 2 for all 1<=q<=r
  closed bound D(q) <= q^2/(2(J-1)) + q(1/(J-1)+5/2)
  top-phase reachability: |X'| <= r-1 < F(r)-F(r-m) whenever m >= J-1
Also: the least capacity c for which (I1) holds (for comparison with c*(J)), and the
section 7 numbers.
"""
import sys
from fractions import Fraction as Fr


def Dtab(J, n):
    D = [0] * (n + 1)
    for q in range(1, n + 1):
        D[q] = max(k + 1 + D[q - min(J - 1, k)] for k in range(1, q + 1))
    return D


def check(J, R):
    c = 2 * (J - 1)
    C = max(2, 2 * J - 4)
    D = Dtab(J, R)
    F = [D[x] + C * x for x in range(R + 1)]
    bad = {k: 0 for k in ("C1", "Y", "I1", "I2", "TS", "pi", "closed", "topreach", "mono")}
    minslack = {"I1": None, "I2": None, "TS": None, "Y": None}

    def upd(k, s):
        if minslack[k] is None or s < minslack[k]:
            minslack[k] = s
    for x in range(1, R + 1):
        if F[x] <= F[x - 1]:
            bad["mono"] += 1
        if Fr(D[x]) > Fr(x * x, 2 * (J - 1)) + x * (Fr(1, J - 1) + Fr(5, 2)):
            bad["closed"] += 1
    for r in range(1, R + 1):
        for m in range(0, r + 1):
            t = m // (J - 1)
            if 2 * (D[r] - D[r - m]) < 2 * t * (r + 1) - (J - 1) * t * (t - 1):
                bad["C1"] += 1
        for q in range(1, r + 1):
            if (C - 1) * r + D[q] - q < 2:
                bad["pi"] += 1
        if r <= 400:
            for q in range(1, r):
                for b in range(1, min(q, r - q) + 1):
                    s = b + (C - 1) * r + D[q] - q - F[b]
                    upd("Y", s)
                    if s < 0:
                        bad["Y"] += 1
        mmax = (r - 2) // 2
        for m in range(c + 1, mmax + 1):
            lhs = (m - 1) + ((m - 1) // c) * (r + 1 - c) + (r - 1)
            s = F[r] - F[r - m] - lhs
            upd("I1", s)
            if s < 0:
                bad["I1"] += 1
        for m in range(2 * (J - 1), mmax + 1):
            s = F[r] - F[r - m] - (r - 1)
            upd("I2", s)
            if s < 0:
                bad["I2"] += 1
        for m in range(1, 2 * J - 2):
            for mp in range(1, min(m, r) + 1):
                s = F[r] - F[r - mp] - (m + mp)
                upd("TS", s)
                if s < 0:
                    bad["TS"] += 1
        for m in range(J - 1, min(2 * J - 3, r) + 1):
            if F[r] - F[r - m] <= r - 1:
                bad["topreach"] += 1
    # least capacity cc such that (I1)-type bound holds for all r <= R with m in [cc+1,(r-2)/2]
    cstar = None
    for cc in range(1, c + 1):
        ok = True
        for r in range(1, R + 1):
            for m in range(cc + 1, (r - 2) // 2 + 1):
                lhs = (m - 1) + ((m - 1) // cc) * (r + 1 - cc) + (r - 1)
                if lhs > F[r] - F[r - m]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            cstar = cc
            break
    return bad, minslack, cstar, F


def main():
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    Jmax = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    print("R =", R, "Jmax =", Jmax)
    allok = True
    for J in range(2, Jmax + 1):
        bad, ms, cstar, F = check(J, R)
        ok = all(v == 0 for v in bad.values())
        allok &= ok
        print("J=%2d c=%2d C=%2d violations=%s min_slack=%s least_c(I1)=%s" % (
            J, 2 * (J - 1), max(2, 2 * J - 4), bad, ms, cstar), flush=True)
    print("ALL_OK", allok)
    # section 7 numbers
    print("section 7: a kappa J F(a)")
    for a, k in [(16, 2), (64, 2), (256, 2), (1024, 2), (1024, 3)]:
        J = max(k, 3)
        while k ** J < a:
            J += 1
        J = max(J, k, 3)
        # J = max(kappa, 3, ceil(log_kappa a))
        Jc = 1
        while k ** Jc < a:
            Jc += 1
        J = max(k, 3, Jc)
        D = Dtab(J, a)
        print(a, k, J, D[a] + max(2, 2 * J - 4) * a, (a + 1) * (a + 2) // 2, (a + 2) ** 2 // 4 + 2 * a)


if __name__ == "__main__":
    main()
