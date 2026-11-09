"""Referee's independent exact check of Lemma C of 2026-11-07-rees-sde-subquad-A.md.

Nothing is imported from the agent's folder.  D_J is computed from the literal definition
D_J(0) = 0, D_J(q) = max_{1<=k<=q} (k + 1 + D_J(q - min(J-1, k))).

Checked for J in [2, JMAX], r in [1, RMAX] (exact integers):
  (C0)  D(x) >= 2 + D(x-1); D(x) >= x+1 + D(x-J+1) for x >= J-1; F increasing
  (C1)  D(r) - D(r-m) >= t(r+1) - (J-1) t(t-1)/2,  t = floor(m/(J-1)), 0 <= m <= r
  (pi)  (C-1) r + D(q) - q >= 2 for 1 <= q <= r
  (Y)   b + (C-1) r + D(q) - q >= F(b) for 1 <= b <= q, q + b <= r          (r <= YMAX)
  (I1)  (m-1) + floor((m-1)/c)(r+1-c) + (r-1) <= F(r) - F(r-m), c+1 <= m <= q, r >= 2q+2
        [equivalently c+1 <= m <= floor((r-2)/2)]
  (I2)  r - 1 <= F(r) - F(r-m), 2(J-1) <= m <= floor((r-2)/2)
  (TS)  m + m' <= F(r) - F(r-m'), 1 <= m' <= m <= 2J-3, m' <= r
  (TS') the same with the sharper C' = max(2, J-3) claimed in Lemma T_m(c), m <= J-2
  (top) for m in [J-1, 2J-3] and r >= 2m+2:  F(r) - F(r-m) > r - 1   (T_m(c))
  (cl)  D(q) <= q^2/(2(J-1)) + q(1/(J-1) + 5/2) for J >= 3 (exact rationals)
Also prints the tight cases (slack 0) and the Section 7 numbers.
Usage: ref_ineq.py JMAX RMAX YMAX
"""
import sys
from fractions import Fraction

JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
RMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 2500
YMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 500


def D_table(J, n):
    D = [0] * (n + 1)
    for q in range(1, n + 1):
        D[q] = max(k + 1 + D[q - min(J - 1, k)] for k in range(1, q + 1))
    return D


def check_J(J, RMAX, YMAX):
    c = 2 * (J - 1)
    C = max(2, 2 * J - 4)
    Cs = max(2, J - 3)
    D = D_table(J, RMAX)
    F = [D[x] + C * x for x in range(RMAX + 1)]
    Fs = [D[x] + Cs * x for x in range(RMAX + 1)]
    bad = dict(C0=0, mono=0, C1=0, pi=0, Y=0, I1=0, I2=0, TS=0, TSs=0, top=0, cl=0)
    slack = dict(Y=None, I1=None, I2=0, TS=None, TSs=None)
    tight = dict(Y=[], I1=[], TS=[], TSs=[])

    def upd(key, s, where):
        if slack[key] is None or s < slack[key]:
            slack[key] = s
        if s == 0 and len(tight[key]) < 4:
            tight[key].append(where)

    for x in range(1, RMAX + 1):
        if D[x] < 2 + D[x - 1]:
            bad["C0"] += 1
        if x >= J - 1 and D[x] < x + 1 + D[x - J + 1]:
            bad["C0"] += 1
        if F[x] <= F[x - 1]:
            bad["mono"] += 1
        if J >= 3:
            rhs = Fraction(x * x, 2 * (J - 1)) + x * (Fraction(1, J - 1) + Fraction(5, 2))
            if Fraction(D[x]) > rhs:
                bad["cl"] += 1
    for r in range(1, RMAX + 1):
        for m in range(0, r + 1):
            t = m // (J - 1)
            # 2*(D(r)-D(r-m)) >= 2t(r+1) - (J-1)t(t-1)
            if 2 * (D[r] - D[r - m]) < 2 * t * (r + 1) - (J - 1) * t * (t - 1):
                bad["C1"] += 1
        for q in range(1, r + 1):
            if (C - 1) * r + D[q] - q < 2:
                bad["pi"] += 1
        half = (r - 2) // 2
        for m in range(c + 1, half + 1):
            lhs = (m - 1) + ((m - 1) // c) * (r + 1 - c) + (r - 1)
            s = F[r] - F[r - m] - lhs
            upd("I1", s, (r, m))
            if s < 0:
                bad["I1"] += 1
        for m in range(c, half + 1):
            s = F[r] - F[r - m] - (r - 1)
            if slack["I2"] is None or s < slack["I2"]:
                slack["I2"] = s
            if s < 0:
                bad["I2"] += 1
        for m in range(1, 2 * J - 2):
            for mp in range(1, min(m, r) + 1):
                s = F[r] - F[r - mp] - (m + mp)
                upd("TS", s, (r, m, mp))
                if s < 0:
                    bad["TS"] += 1
        for m in range(1, max(1, J - 2) + 1):
            for mp in range(1, min(m, r) + 1):
                s = Fs[r] - Fs[r - mp] - (m + mp)
                upd("TSs", s, (r, m, mp))
                if s < 0:
                    bad["TSs"] += 1
        for m in range(J - 1, 2 * J - 2):
            if r >= 2 * m + 2 and not (F[r] - F[r - m] > r - 1):
                bad["top"] += 1
            if r >= 2 * m + 2 and not (Fs[r] - Fs[r - m] > r - 1):
                bad["top"] += 1
    for r in range(1, min(RMAX, YMAX) + 1):
        for q in range(1, r):
            for b in range(1, min(q, r - q) + 1):
                s = b + (C - 1) * r + D[q] - q - F[b]
                upd("Y", s, (r, q, b))
                if s < 0:
                    bad["Y"] += 1
    return bad, slack, tight, D


def main():
    allok = True
    print("J  c   C  violations  min_slack  tight_examples")
    for J in range(2, JMAX + 1):
        bad, slack, tight, D = check_J(J, RMAX, YMAX)
        ok = all(v == 0 for v in bad.values())
        allok &= ok
        print(J, 2 * (J - 1), max(2, 2 * J - 4), bad, slack, {k: v for k, v in tight.items() if v})
    print("ALL_OK", allok, "JMAX", JMAX, "RMAX", RMAX, "YMAX(Y)", YMAX)
    # D_J small values and the section 7 numbers
    import math
    print("D_3(q) vs floor((q+2)^2/4):", all(D_table(3, 60)[q] == (q + 2) ** 2 // 4 for q in range(1, 61)))
    print("D_2(q) vs (q+1)(q+2)/2-1:", all(D_table(2, 60)[q] == (q + 1) * (q + 2) // 2 - 1 for q in range(1, 61)))
    print("Section 7: a kappa J F(a) triangular D_3(a)+2a ratio")
    for kap, a in ((2, 16), (2, 64), (2, 256), (2, 1024), (3, 1024)):
        J = max(kap, 3, math.ceil(math.log(a, kap) - 1e-12))
        C = max(2, 2 * J - 4)
        Fa = D_table(J, a)[a] + C * a
        D3 = D_table(3, a)[a]
        print(a, kap, J, Fa, (a + 1) * (a + 2) // 2, D3 + 2 * a, round(Fa / (a * a / (2 * (J - 1))), 3))
    # F(a) <= a^2/(2(J-1)) + a(2J - 3/2 + 1/(J-1)) for J >= 3 (closed bound of Corollary A)
    okF = True
    for J in range(3, 25):
        D = D_table(J, 1500)
        C = 2 * J - 4
        for a in range(1, 1501):
            if Fraction(D[a] + C * a) > Fraction(a * a, 2 * (J - 1)) + a * (2 * J - Fraction(3, 2) + Fraction(1, J - 1)):
                okF = False
    print("F(a) <= a^2/(2(J-1)) + a(2J-3/2+1/(J-1)) for 3<=J<=24, a<=1500:", okF)


main()
