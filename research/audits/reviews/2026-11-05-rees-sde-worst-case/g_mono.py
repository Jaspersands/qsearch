"""Exact minimum of |Good(beta)| for MONOCHROMATIC block patterns (all blocks in one class),
e <= 3 pairwise distinct offsets: Gm(p) = min over beta of #{s : beta_b + s in Q_0 u {0} for all b}.
WLOG (scaling by u with cos u = c, translation, scaling by P) class 0, beta_1 = 0,
beta_2 in a set of coset representatives.  Usage: g_mono.py kappa pmin pmax"""
import sys
import numpy as np


def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))


def primroot(p):
    fac, n, f = [], p - 1, 2
    while f * f <= n:
        if n % f == 0:
            fac.append(f)
            while n % f == 0:
                n //= f
        f += 1
    if n > 1:
        fac.append(n)
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fac))


k, lo, hi = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
worst = 1.0
for p in range(lo, hi + 1):
    if not isprime(p) or (p - 1) % k:
        continue
    g = primroot(p)
    I = np.zeros(p, dtype=np.int64)
    for y in range(p):
        if y == 0 or pow(y, (p - 1) // k, p) == 1:
            I[y] = 1
    best = int(I.sum())                      # e = 1
    for c in range(k):
        b2 = pow(g, c, p)
        J = I * np.roll(I, -b2)              # J[s] = I[s] I[s+b2]
        best = min(best, int(J.sum()))       # e = 2
        # e = 3: count_s J[s] I[s+b3] for all b3 via FFT correlation
        F = np.fft.irfft(np.conj(np.fft.rfft(J)) * np.fft.rfft(I), n=p)
        cnt = np.rint(F).astype(np.int64)    # cnt[b3] = sum_s J[s] I[s+b3]
        cnt[0] = 10 ** 9
        cnt[b2] = 10 ** 9
        best = min(best, int(cnt.min()))
    worst = min(worst, best / p)
    print(p, best, round(best / p, 4), flush=True)
print("min ratio", worst)
