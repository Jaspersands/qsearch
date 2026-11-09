"""kappa = 4: refined (discrete-stratum) certificates at one prime p.

Classes of balanced e by (r, c) = numbers of rows / columns touched by supp(e); v = r + c.
S^D_e is invariant under row and column permutations and under transposition, so it depends
only on the r x c block of e (placed in the first r rows and c columns) up to those symmetries.

* Low classes (v <= 5): every block e is enumerated, S^D_e computed exactly for one
  representative per orbit, and the exact low-order main term
      M_5 = S0 + Re sum_{0 < v(e) <= 5} w^{-<e,c0>} S^D_e        (all placements)
  is formed with the Rees phases, together with L1_{<=5} = sum |S^D_e| over those e.
* High classes (v >= 6): `nsamp` uniform balanced block e per shape; class L1 estimated as
  (exact class size) x (sample mean |S^D_e|), with a standard error.
Prints M_5/S0, L1_low/S0, the per-class estimates and the totals for the certificates
  (R)  pure refined:  S0 > L1_low + L1_high         (all e bounded term by term)
  (H5) hybrid:        M_5 > L1_high                  (v <= 5 kept exactly)
Usage: kappa4.py p [nsamp] [seed]
"""
import sys
from itertools import permutations, product, combinations
from math import comb
import numpy as np
from dsum import dsums

K = 4


def class_size(r, c):
    """number of balanced e in Z_K^{r x c} touching all r rows and c columns (one placement)."""
    tot = 0
    for r2 in range(r + 1):
        for c2 in range(c + 1):
            m = r2 * c2
            B = K ** (m - 1) if m >= 1 else 1
            tot += (-1) ** (r - r2 + c - c2) * comb(r, r2) * comb(c, c2) * B
    return tot


def blocks(r, c):
    for vals in product(range(K), repeat=r * c):
        if sum(vals) % K:
            continue
        b = np.array(vals).reshape(r, c)
        if (b != 0).any(1).all() and (b != 0).any(0).all():
            yield b


def canon(b):
    r, c = b.shape
    best = None
    cands = [b] + ([b.T] if r == c else [])
    for m in cands:
        for pr in permutations(range(r)):
            for pc in permutations(range(c)):
                key = tuple(m[list(pr)][:, list(pc)].reshape(-1))
                if best is None or key < best:
                    best = key
    return best


def embed(b, R, C):
    e = np.zeros((K, K), dtype=np.int64)
    e[np.ix_(R, C)] = b
    return e


def main():
    p = int(sys.argv[1])
    nsamp = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    w = np.exp(2j * np.pi / K)
    c0 = np.array([[(-(i + j)) % K for j in range(K)] for i in range(K)])
    # ---- low classes: shapes (r, c) with r + c <= 5, r <= c
    low_shapes = [(1, 2), (1, 3), (1, 4), (2, 2), (2, 3)]
    reps, rep_index, low = {}, [], []
    for (r, c) in low_shapes:
        for b in blocks(r, c):
            k = canon(b)
            if k not in reps:
                reps[k] = len(reps)
            low.append((r, c, b, reps[k]))
    rep_list = [None] * len(reps)
    for (r, c, b, t) in low:
        if rep_list[t] is None:
            rep_list[t] = embed(b, list(range(r)), list(range(c)))
    # ---- high classes: samples
    high_shapes = [(2, 4), (3, 3), (3, 4), (4, 4)]
    samples = []
    for (r, c) in high_shapes:
        got = 0
        while got < nsamp:
            b = rng.integers(0, K, size=(r, c))
            if b.sum() % K or not (b != 0).any(1).all() or not (b != 0).any(0).all():
                continue
            samples.append((r, c, embed(b, list(range(r)), list(range(c)))))
            got += 1
    E = np.array(rep_list + [s[2] for s in samples])
    S, S0 = dsums(p, K, E)
    nrep = len(rep_list)
    Srep, Ssam = S[:nrep], S[nrep:]
    # ---- exact low-order part with Rees phases over all placements (and transposes)
    M = S0
    L1low = 0.0
    bycls = {}
    for (r, c, b, t) in low:
        for (rr, cc, bb) in ([(r, c, b)] + ([(c, r, b.T)] if r != c else [])):
            for R in combinations(range(K), rr):
                for C in combinations(range(K), cc):
                    e = embed(bb, list(R), list(C))
                    M += (w ** (-(e * c0).sum()) * Srep[t]).real
                    L1low += abs(Srep[t])
                    key = (min(rr, cc), max(rr, cc))
                    bycls[key] = bycls.get(key, 0.0) + abs(Srep[t])
    print(f"p={p} kappa={K} S0={S0:.6e} reps={nrep} samples={len(samples)}")
    print(f"  exact low part: M5/S0={M / S0:.5f}  L1(v<=5)/S0={L1low / S0:.5f}  " +
          " ".join(f"{k}:{x / S0:.4g}" for k, x in sorted(bycls.items())))
    est, var = 0.0, 0.0
    for t, (r, c) in enumerate(high_shapes):
        a = np.abs(Ssam[t * nsamp:(t + 1) * nsamp])
        mult = comb(K, r) * comb(K, c) * (2 if r != c else 1)
        size = class_size(r, c) * mult
        m, se = a.mean(), a.std(ddof=1) / np.sqrt(len(a))
        est += size * m
        var += (size * se) ** 2
        print(f"  class {(r, c)}: size={size} mean|S|/p^{K + 1}={m / p ** (K + 1):.4g} "
              f"(se {se / p ** (K + 1):.2g}) max/p^{K + 1}={a.max() / p ** (K + 1):.4g} "
              f"class L1/S0={size * m / S0:.4g}")
    print(f"  L1(v>=6)/S0 = {est / S0:.4f} +- {np.sqrt(var) / S0:.4f}")
    print(f"  (R)  pure refined: (L1low+L1high)/S0 = {(L1low + est) / S0:.4f}  -> {'holds' if L1low + est < S0 else 'fails'} (estimate)")
    print(f"  (H5) hybrid: M5/S0 = {M / S0:.4f} vs L1high/S0 = {est / S0:.4f} -> {'holds' if est < M else 'fails'} (estimate)", flush=True)


if __name__ == "__main__":
    main()
