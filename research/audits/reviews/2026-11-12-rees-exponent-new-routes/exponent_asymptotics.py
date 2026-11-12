"""Exponent E(c,p) = 1 + sum_{d=2}^c (1 + j_d) of the weight-doubling route of the
full version (Remark rem:fc-witness-h3(c)); exact computation of the formula.
j_d = 0 if kappa_d = 1; j_d = ceil(log2(p-1)) if kappa_d = p-1;
otherwise j_d = j*_h (h = (p-1)/kappa_d), computed exactly (FFT sumsets) for
p <= PEX, and bounded above by 1 if sqrt(p) > (k-1)(k-2)+3, else ceil(log2 k).
Primes beyond ((c-1)(c-2)+3)^2 give E <= 2c-1 (all j_d <= 1)."""
import math, sys
import numpy as np
from sympy import primerange, divisor_count

PEX = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
CMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
_cache = {}

def jstar(p, k):
    key = (p, k)
    if key in _cache:
        return _cache[key]
    D = np.zeros(p, dtype=bool); D[0] = True
    D[np.unique(np.array([pow(x, k, p) for x in range(1, p)]))] = True
    j = 0
    n = 1 << (2 * p).bit_length()
    while not D.all():
        a = np.fft.rfft(D.astype(float), n); b = np.fft.rfft(D[(-np.arange(p)) % p].astype(float), n)
        conv = np.fft.irfft(a * b, n)[:2 * p]
        s = conv[:p] + np.concatenate([conv[p:2 * p], np.zeros(0)])[:p]
        D = s > 0.5
        j += 1
    _cache[key] = j
    return j

def E(c, p, exact):
    tot = 1; nbad = 0
    for d in range(2, c + 1):
        k = math.gcd(d, p - 1)
        if k == 1:
            j = 0
        elif k == p - 1:
            j = math.ceil(math.log2(p - 1))
        elif exact and p <= PEX:
            j = jstar(p, k)
        else:
            j = 1 if math.sqrt(p) > (k - 1) * (k - 2) + 3 else math.ceil(math.log2(k))
        if j > 1:
            nbad += 1
        tot += 1 + j
    return tot, nbad

if __name__ == "__main__":
    print("c  maxE_exact(p<=PEX, bound beyond)  argmax_p  maxE_bound  2c-1  excess  max#bad  bound c^(3/4)*maxtau*log2c")
    for c in range(2, CMAX + 1):
        pmax = ((c - 1) * (c - 2) + 3) ** 2 + 1
        best = (2 * c - 1, None); bestb = 2 * c - 1; mb = 0; maxtau = 1
        for p in primerange(c + 1, max(pmax, c + 3)):
            e, nb = E(c, p, True)
            eb, _ = E(c, p, False)
            if e > best[0]:
                best = (e, p)
            bestb = max(bestb, eb); mb = max(mb, nb)
            if p <= c ** 4:
                maxtau = max(maxtau, divisor_count(p - 1))
        bnd = c ** 0.75 * maxtau * math.ceil(math.log2(c))
        print(f"{c:3d} {best[0]:5d} {str(best[1]):>8s} {bestb:5d} {2*c-1:5d} {best[0]-(2*c-1):4d} {mb:4d} {bnd:10.1f}")
        sys.stdout.flush()
