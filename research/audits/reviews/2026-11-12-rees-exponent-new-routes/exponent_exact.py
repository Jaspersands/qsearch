"""Exact max_{p>c} E(c,p) for the weight-doubling route: like
exponent_asymptotics.py but computes j*_h exactly (FFT sumsets) at EVERY
(p, kappa) where the proven bound allows j > 1.  Exact formula evaluation;
it says nothing beyond the conditional theorem it evaluates."""
import math, sys
from sympy import primerange
import exponent_asymptotics as ea

CMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 24

def E_exact(c, p):
    tot = 1; nbad = 0
    for d in range(2, c + 1):
        k = math.gcd(d, p - 1)
        if k == 1:
            j = 0
        elif k == p - 1:
            j = math.ceil(math.log2(p - 1))
        elif math.sqrt(p) > (k - 1) * (k - 2) + 3:
            j = 1
        else:
            j = ea.jstar(p, k)
        nbad += j > 1
        tot += 1 + j
    return tot, nbad

if __name__ == "__main__":
    print("c  maxE  argmax_p  2c-1  excess  #grades_with_j>1_at_argmax")
    for c in range(2, CMAX + 1):
        pmax = ((c - 1) * (c - 2) + 3) ** 2 + 1
        best = (2 * c - 1, None, 0)
        for p in primerange(c + 1, max(pmax, c + 3)):
            e, nb = E_exact(c, p)
            if e > best[0]:
                best = (e, p, nb)
        print(f"{c:3d} {best[0]:5d} {str(best[1]):>8s} {2*c-1:5d} {best[0]-(2*c-1):4d} {best[2]:4d}")
        sys.stdout.flush()
