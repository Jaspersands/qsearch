"""Exact checks of the counting inequalities used in Theorem A of
../2026-11-07-rees-sde-subquad-A.md, for J in [3, JMAX] and every rank r <= RMAX.

F(r) = D_J(r) + C r, C = max(2, 2J-4), c = capacity (extra blocks per round); the theorem uses c = 2(J-1).
(Y)    b + (C-1) r + D_J(q) - q >= F(b)           for 1<=b<=q, q+b<=r          [case 2]
(I1)   (qW-1) + floor((qW-1)/c)(r+1-c) + (r-1) <= F(r) - F(r-qW)
                                                  for c+1 <= qW <= floor((r-2)/2) [case 3a]
(I2)   r - 1 <= F(r) - F(r-m)                     for 2(J-1) <= m <= floor((r-2)/2) [case 3b]
(TS)   m + m' <= F(r) - F(r-m')                   for 1<=m'<=m<=2J-3, m <= floor((r-2)/2) [top stall]
Also: the minimal capacity c*(J) for which (I1) holds for all r <= RMAX, and the closed
bound D_J(q) <= q^2/(2(J-1)) + q(1/(J-1)+5/2).
Usage: dj_ineq.py JMAX RMAX
"""
import sys

JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
RMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 1500


def Dtable(J, n):
    D = [0] * (n + 1)
    for q in range(1, n + 1):
        best = 0
        if q >= J - 1:
            best = q + 1 + D[q - J + 1]          # k >= J-1: best k = q
        for k in range(1, min(q, J - 2) + 1):    # small circuits
            best = max(best, k + 1 + D[q - k])
        D[q] = best
    return D


def Dtable_brute(J, n):
    D = [0] * (n + 1)
    for q in range(1, n + 1):
        D[q] = max(k + 1 + D[q - min(J - 1, k)] for k in range(1, q + 1))
    return D


def main():
    # brute-force agreement of the fast recursion
    for J in range(2, 9):
        assert Dtable(J, 300) == Dtable_brute(J, 300), J
    print("fast D_J recursion = brute recursion for J<=8, q<=300")
    print("J  C   c=2(J-1)  c*(J)  (Y) (I1) (I2) (TS) bound   min r with case 3a possible")
    for J in range(3, JMAX + 1):
        C = max(2, 2 * J - 4)
        D = Dtable(J, RMAX)
        F = lambda x: D[x] + C * x
        okb = all(D[q] <= q * q / (2 * (J - 1)) + q * (1 / (J - 1) + 2.5) + 1e-9 for q in range(RMAX + 1))
        okY = True
        for r in range(1, min(RMAX, 300) + 1):
            for q in range(1, r):
                for b in range(1, min(q, r - q) + 1):
                    if b + (C - 1) * r + D[q] - q < F(b):
                        okY = False

        def I1(c, r, qW):
            return (qW - 1) + ((qW - 1) // c) * (r + 1 - c) + (r - 1) <= F(r) - F(r - qW)

        c0 = 2 * (J - 1)
        okI1 = all(I1(c0, r, qW) for r in range(1, RMAX + 1) for qW in range(c0 + 1, (r - 2) // 2 + 1))
        # minimal c
        cstar = None
        for c in range(1, c0 + 1):
            if all(I1(c, r, qW) for r in range(1, RMAX + 1) for qW in range(c + 1, (r - 2) // 2 + 1)):
                cstar = c
                break
        m0 = 2 * (J - 1)
        okI2 = all(r - 1 <= F(r) - F(r - m) for r in range(1, RMAX + 1) for m in range(m0, (r - 2) // 2 + 1))
        okTS = all(m + mp <= F(r) - F(r - mp) for r in range(1, RMAX + 1)
                   for m in range(1, min(2 * J - 3, (r - 2) // 2) + 1) for mp in range(1, m + 1))
        rmin = 2 * (c0 + 1) + 2
        print("%-2d %-3d %-9d %-6s %-3s %-4s %-4s %-4s %-6s %d" % (J, C, c0, cstar, okY, okI1, okI2, okTS, okb, rmin))
    # the arity at J = ceil(log_kappa a)
    print()
    print("a, kappa, J, F(a) = D_J(a)+C a, triangular (a+1)(a+2)/2, D_3(a)+2a, ratio F/(a^2/(2(J-1)))")
    import math
    for kap in (2, 3):
        for a in (16, 64, 256, 1024):
            J = max(kap, 3, math.ceil(math.log(a, kap)))
            C = max(2, 2 * J - 4)
            D = Dtable(J, a)
            D3 = Dtable(3, a)
            Fa = D[a] + C * a
            print(a, kap, J, Fa, (a + 1) * (a + 2) // 2, D3[a] + 2 * a, round(Fa / (a * a / (2 * (J - 1))), 3))


main()
