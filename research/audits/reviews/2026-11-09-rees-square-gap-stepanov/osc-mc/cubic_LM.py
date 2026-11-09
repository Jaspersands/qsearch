"""For p = 1 mod 3: the representation 4p = L^2 + 27 M^2 (L = 1 mod 3) and c3 = |L|/(2 sqrt p),
the |cos| of the argument of the cubic Jacobi sum J = (L + 3M sqrt(-3))/2 (up to a unit).
c3 ~ 0: J nearly purely imaginary.  Usage: python cubic_LM.py p1 p2 ..."""
import sys, math
for p in map(int, sys.argv[1:]):
    for M in range(0, int(math.isqrt(4 * p // 27)) + 1):
        L2 = 4 * p - 27 * M * M
        L = math.isqrt(L2)
        if L * L == L2:
            if L % 3 != 1: L = -L
            print('%6d  L=%5d  M=%4d  |L|/(2 sqrt p)=%.3f' % (p, L, M, abs(L) / (2 * math.sqrt(p))))
            break
