"""Independent check of G*_E(p), E <= 3, all class patterns (equal classes allowed).

G*_E(p) = min |Good(beta)| over 1 <= e <= E, classes c_1..c_e (arbitrary, all equal allowed),
pairwise distinct offsets beta_1..beta_e, where Good(beta) = {s : beta_b + s in Q_{-c_b} u {0}}.

Normalisation (exact symmetries): translate s so beta_1 = 0, then scale by any nonzero y
(scaling by y maps Q_c to Q_{c+cos y}; all class patterns are enumerated, so this is free):
beta = (0, 1) for e = 2 and beta = (0, 1, t), t not in {0, 1}, for e = 3.
e = 3 counts N(t) = sum_s B(s) A(s + t), B(s) = A0(s) A1(s + 1), are a circular correlation,
computed by FFT and checked against direct enumeration for small p (selftest).

Usage: python gstar.py KAPPA PMIN PMAX
Output: one line per prime p = 1 mod KAPPA: p, G*_3, ratio, and the minimising pattern.
"""
import sys
import numpy as np


def primes(lo, hi):
    s = np.ones(hi + 1, bool)
    s[:2] = False
    for i in range(2, int(hi ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return [int(q) for q in np.nonzero(s)[0] if q >= lo]


def classes(p, k):
    """cls[y] in 0..k-1 for y != 0 (discrete log mod k w.r.t. a primitive root); cls[0] = -1."""
    n = p - 1
    fac, m, f = [], n, 2
    while f * f <= m:
        if m % f == 0:
            fac.append(f)
            while m % f == 0:
                m //= f
        f += 1
    if m > 1:
        fac.append(m)
    g = next(g for g in range(2, p) if all(pow(g, n // q, p) != 1 for q in fac))
    cls = np.full(p, -1, np.int64)
    y = 1
    for j in range(n):
        cls[y] = j % k
        y = y * g % p
    return cls


def ind(cls, c, k):
    """Indicator of Q_c u {0}."""
    return ((cls == (c % k)) | (cls == -1)).astype(np.float64)


def gstar(p, k, want_pattern=True):
    cls = classes(p, k)
    best = ((p - 1) // k + 1, ("e=1",))
    ar = np.arange(p)
    A = [ind(cls, -c, k) for c in range(k)]       # A[c](y) = 1[y in Q_{-c} u {0}]
    Ash = [a[(ar + 1) % p] for a in A]            # y -> A(y+1)
    FA = [np.fft.rfft(a) for a in A]
    for c0 in range(k):
        for c1 in range(k):
            Bv = A[c0] * Ash[c1]
            n2 = int(round(Bv.sum()))
            if n2 < best[0]:
                best = (n2, ("e=2", c0, c1))
            FB = np.fft.rfft(Bv)
            for c2 in range(k):
                # N(t) = sum_s B(s) A2(s+t)  (circular)
                N = np.fft.irfft(np.conj(FB) * FA[c2], n=p)
                N = np.rint(N).astype(np.int64)
                N[0] = 10 ** 9
                N[1] = 10 ** 9
                t = int(np.argmin(N))
                if N[t] < best[0]:
                    best = (int(N[t]), ("e=3", c0, c1, c2, t))
    return best


def gstar_direct(p, k):
    """Plain enumeration over all distinct offsets (no normalisation), e <= 3."""
    cls = classes(p, k)
    def ok(y, c):
        y %= p
        return y == 0 or cls[y] == (-c) % k
    best = (p - 1) // k + 1
    import itertools
    for e in (2, 3):
        for betas in itertools.combinations(range(p), e):
            for cs in itertools.product(range(k), repeat=e):
                n = sum(1 for s in range(p) if all(ok(b + s, c) for b, c in zip(betas, cs)))
                best = min(best, n)
    return best


def gstar_direct_norm(p, k):
    """Direct (non-FFT) count on the normalised offsets (0,1) and (0,1,t)."""
    cls = classes(p, k)
    ar = np.arange(p)
    best = (p - 1) // k + 1
    A = [ind(cls, -c, k) for c in range(k)]
    for c0 in range(k):
        for c1 in range(k):
            Bv = A[c0] * A[c1][(ar + 1) % p]
            best = min(best, int(Bv.sum()))
            for c2 in range(k):
                for t in range(2, p):
                    best = min(best, int((Bv * A[c2][(ar + t) % p]).sum()))
    return best


def selftest():
    bad = 0
    for k, ps in ((2, [263, 1009]), (3, [67, 79, 241, 271, 307, 2767])):
        for p in ps:
            a = gstar(p, k)[0]
            b = gstar_direct_norm(p, k)
            print(f"selftest-norm kappa={k} p={p} fft={a} direct={b}", flush=True)
            bad += a != b
    for k, ps in ((2, [7, 11, 13, 17, 19, 23]), (3, [7, 13, 19, 31, 37])):
        for p in ps:
            a = gstar(p, k)[0]
            b = gstar_direct(p, k)
            print(f"selftest kappa={k} p={p} fft={a} direct={b}", flush=True)
            bad += a != b
    print("selftest mismatches", bad, flush=True)
    return bad


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    k, lo, hi = map(int, sys.argv[1:4])
    worst = (9.0, None)
    zero = []
    for p in primes(lo, hi):
        if (p - 1) % k:
            continue
        g, pat = gstar(p, k)
        if g == 0:
            zero.append(p)
        r = g / p
        if r < worst[0]:
            worst = (r, p)
        print(p, g, f"{r:.4f}", pat, flush=True)
    print("G*=0 at", zero)
    print("min ratio", worst)
