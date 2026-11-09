"""Independent recomputation of E_cg(E, kappa) and G_E(p) for E <= 3 (block-steered check).

Method (different from good_threshold.py, which uses FFT correlation with c_1 = 0 normalised):
all class tuples (c_1, .., c_e) are enumerated (no class normalisation), beta_1 = 0 by translation
and beta_2 runs over the kappa coset representatives (scaling by P keeps classes); the count for
every beta_3 at once is a bincount of differences t - s with s in A = {s : conditions 1, 2} and
t in T_3 = Q_{-c_3} U {0}.  Exact integers throughout.

Good(beta) = {s : beta_b + s in Q_{-c_b} U {0} for all b}.  E_cg(E, kappa): some e <= E pairwise
distinct offsets with classes not all equal have Good = empty.  G_E(p) = min |Good|.
"""
import itertools
import math
import sys

import numpy as np


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def gen(p):
    fac = [q for q in range(2, p) if (p - 1) % q == 0 and is_prime(q)]
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g


def class_table(p, k):
    """cl[y] = nu with y in g^nu P (y != 0); cl[0] = -1."""
    g = gen(p)
    cl = np.full(p, -1, dtype=np.int64)
    y = 1
    for e in range(p - 1):
        cl[y] = e % k
        y = y * g % p
    return cl, [pow(g, c, p) for c in range(k)]


def scan(p, k, E):
    cl, reps = class_table(p, k)
    ar = np.arange(p)
    # T[c] = indicator of Q_c U {0}
    T = [(cl == c) | (ar == 0) for c in range(k)]
    gmin = None
    witness = None
    for e in range(2, E + 1):
        for cls in itertools.product(range(k), repeat=e):
            if len(set(cls)) < 2:
                continue
            need = [(-c) % k for c in cls]
            for r in reps:
                A = T[need[0]] & np.roll(T[need[1]], -r)   # A[s] = [s in T0][s + r in T1]
                if e == 2:
                    cnt = int(A.sum())
                    if gmin is None or cnt < gmin:
                        gmin, witness = cnt, (cls, (0, r))
                    continue
                S = np.nonzero(A)[0]
                T3 = np.nonzero(T[need[2]])[0]
                if S.size == 0:
                    counts = np.zeros(p, dtype=np.int64)
                else:
                    diff = (T3[None, :] - S[:, None]) % p
                    counts = np.bincount(diff.ravel(), minlength=p)
                counts[0] = 10 ** 9      # beta_3 = beta_1
                counts[r] = 10 ** 9      # beta_3 = beta_2
                j = int(np.argmin(counts))
                if gmin is None or counts[j] < gmin:
                    gmin, witness = int(counts[j]), (cls, (0, r, j))
    return gmin, witness


def weil_rhs(k, e, p):
    return (p - e - (k ** e - 1) * (e - 1) * math.sqrt(p)) / k ** e


def p_weil(k, E):
    p = 2
    while not all(p - e > (k ** e - 1) * (e - 1) * math.sqrt(p) for e in range(2, E + 1)):
        p += 1
    return p


if __name__ == "__main__":
    k, E, plo, phi = map(int, sys.argv[1:5])
    print(f"# kappa={k} E={E} p_W={p_weil(k, E)} range [{plo},{phi}]", flush=True)
    exc, ratio = [], None
    for p in range(max(plo, 3), phi + 1):
        if (p - 1) % k or not is_prime(p):
            continue
        gm, w = scan(p, k, E)
        if gm == 0:
            exc.append(p)
        else:
            rr = gm / p
            if ratio is None or rr < ratio[0]:
                ratio = (rr, p, gm)
            wl = min(weil_rhs(k, e, p) for e in range(2, E + 1))
            assert gm >= wl - 1e-9, (p, gm, wl)
        print(f"p={p} G={gm} witness={w}", flush=True)
    print(f"# exceptional: {exc}")
    print(f"# min G/p over non-exceptional: {ratio}")
