"""Exact thresholds for coset-generic block realization (Theorem B / Lemma W).

For kappa | p-1, E blocks with classes c_1..c_E (at least two distinct classes)
and offsets beta_1..beta_E that are pairwise distinct, put

    Good(beta) = { s in F_p : beta_j + s in Q_{-c_j} U {0} for every j }.

E_cg(E, kappa) = primes p = 1 mod kappa (p > kappa+1... all p = 1 mod kappa) for
which some E' <= E, some class assignment and some pairwise distinct beta give
Good(beta) = empty.  Above the Weil bound p_W(E, kappa) (smallest p with
p - E > (kappa^E - 1)(E - 1) sqrt(p), and the same for every E' <= E) Good is
nonempty for every such beta, so an exhaustive scan up to p_W decides
E_cg exactly.

Normalisations (exact symmetries):  c_1 = 0 (scale beta by an element of Q_nu),
beta_1 = 0 (translate s), beta_2 in {g^0..g^{kappa-1}} (scale by P).  The last
offset is handled for all values at once by an FFT cross-correlation, which
also returns |Good(beta)| exactly, so G_min(p) = min |Good| is exact.

Usage:  python good_threshold.py KAPPA E PMAX     (prints one line per prime)
        python good_threshold.py weil KAPPA E
"""
import itertools
import math
import sys

import numpy as np

from common import F, is_prime


def weil_bound(kappa, E):
    """Smallest p with p - e > (kappa^e - 1)(e - 1) sqrt(p) for all 2 <= e <= E."""
    p = 2
    while True:
        if all(p - e > (kappa ** e - 1) * (e - 1) * math.sqrt(p) for e in range(2, E + 1)):
            return p
        p += 1


def weil_gmin(kappa, E, p):
    """Weil lower bound for |Good(beta)| (E distinct offsets)."""
    return (p - E - (kappa ** E - 1) * (E - 1) * math.sqrt(p)) / kappa ** E


def indicators(Fd):
    p, k = Fd.p, Fd.k
    I = np.zeros((k, p), dtype=np.float64)
    I[:, 0] = 1.0
    for y in range(1, p):
        I[Fd.cls(y), y] = 1.0
    return I  # I[c, y] = 1 iff y in Q_c U {0}


def corr(A, Y):
    """count[t] = sum_s A[s] * Y[(s + t) mod p]."""
    fa = np.fft.rfft(A)
    fy = np.fft.rfft(Y)
    n = len(A)
    c = np.fft.irfft(np.conj(fa) * fy, n)
    return np.rint(c).astype(np.int64)


def scan_prime(p, kappa, E):
    """Return (exceptional?, gmin over all E'<=E, witness of failure or None)."""
    Fd = F(p, kappa)
    I = indicators(Fd)
    reps = [Fd.rep(c) for c in range(kappa)]
    gmin = None
    for e in range(2, E + 1):
        for tail in itertools.product(range(kappa), repeat=e - 1):
            cl = (0,) + tail
            if len(set(cl)) < 2:
                continue
            need = [(-c) % kappa for c in cl]
            base = I[need[0]].copy()          # beta_1 = 0
            for r in reps:                     # beta_2 = r
                A2 = base * np.roll(I[need[1]], -r)   # A2[s] = I[s] * I[s + r]
                if e == 2:
                    cnt = int(A2.sum())
                    gmin = cnt if gmin is None else min(gmin, cnt)
                    if cnt == 0:
                        return True, 0, (cl, (0, r))
                    continue
                mids = [()]
                for _ in range(e - 3):
                    mids = [m + (t,) for m in mids for t in range(p)]
                for mid in mids:
                    used = {0, r} | set(mid)
                    if len(used) != 2 + len(mid):
                        continue
                    A = A2.copy()
                    for j, t in enumerate(mid):
                        A *= np.roll(I[need[2 + j]], -t)
                    cnt = corr(A, I[need[e - 1]])
                    mask = np.ones(p, dtype=bool)
                    for u in used:
                        mask[u] = False
                    vals = cnt[mask]
                    if vals.size == 0:
                        continue
                    m = int(vals.min())
                    gmin = m if gmin is None else min(gmin, m)
                    if m == 0:
                        t = int(np.nonzero(mask)[0][np.argmin(vals)])
                        return True, 0, (cl, (0, r) + tuple(mid) + (t,))
    return False, gmin, None


def main():
    if sys.argv[1] == "weil":
        k, E = int(sys.argv[2]), int(sys.argv[3])
        print(f"kappa={k} E={E} weil_bound={weil_bound(k, E)}")
        return
    k, E, pmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    pw = weil_bound(k, E)
    print(f"# kappa={k} E={E} Weil bound p_W={pw}; scanning p <= {pmax}")
    exc = []
    for p in range(3, pmax + 1):
        if not is_prime(p) or (p - 1) % k:
            continue
        if p - 1 == k and E > 1:
            pass
        bad, gmin, wit = scan_prime(p, k, E)
        if bad:
            exc.append(p)
        print(f"p={p} exceptional={bad} gmin={gmin} weil_gmin={weil_gmin(k, E, p):.2f} witness={wit}",
              flush=True)
    print(f"# E_cg(E={E}, kappa={k}) within p<={pmax}: {exc}")
    print(f"# largest exceptional: {max(exc) if exc else None}; complete={'yes' if pmax >= pw else 'no'}")


if __name__ == "__main__":
    main()
