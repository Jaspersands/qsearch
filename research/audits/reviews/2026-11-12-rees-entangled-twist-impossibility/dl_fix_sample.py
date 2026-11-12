"""Lemma F on Dixmier-Lister and on its quotients DL/Z' (Z' a line of gamma_3), p = 5, 7:
random elements of Aut (products of the verified GAP generators); T = induced map on
V = L/gamma_3 (6-dim, D = gamma_2/gamma_3 2-dim). Count T-invariant lines of V outside D;
Lemma F says <= a fraction 1/p whenever T != id. Also: whenever T = id, the action on the top
layer must be the identity. Finite (sampled) check only."""
import sys, os, json, glob, itertools, numpy as np
sys.path.insert(0, '../2026-11-12-rees-direct-twist-class3-referee')
from lie import lcs
HERE = os.path.dirname(os.path.abspath(__file__))
def lines_outside(p, n, d):
    out = []
    for v in itertools.product(range(p), repeat=n):
        v = np.array(v); nz = np.nonzero(v)[0]
        if len(nz) and v[nz[0]] == 1 and v[:n - d].any(): out.append(v)
    return np.array(out)
def run(fn, nsamp, rng):
    r = json.load(open(fn)); p = r['p']; m = r['m']; D = np.array(r['D'])
    ser = lcs(D, p); dims = [len(s) for s in ser]          # [m, dim g2, dim g3, 0]
    # adapted basis: levels ordered, so gamma_k = span of the last dims[k-1] basis vectors
    g2, g3 = dims[1], dims[2]; n = m - g3; d = g2 - g3
    Ls = lines_outside(p, n, d)
    gens = [np.array(g) for g in r['gens']]
    worst = 0.0; nid = 0; bad_id = 0; over = 0
    for _ in range(nsamp):
        M = np.eye(m, dtype=np.int64)
        for _ in range(12):
            M = (M @ gens[rng.integers(len(gens))]) % p
        T = M[:n, :n].T % p          # columns = images (x -> x @ M, rows images); V = first n coords
        top = M[n:, n:] % p
        if (T == np.eye(n, dtype=np.int64)).all():
            nid += 1
            if not (top == np.eye(g3, dtype=np.int64)).all(): bad_id += 1
            continue
        W = (Ls @ T.T) % p           # images of each line's vector
        # v fixed iff W row proportional to v: all 2x2 minors vanish
        prop = np.ones(len(Ls), bool)
        for i in range(n):
            for j in range(i + 1, n):
                prop &= ((W[:, i] * Ls[:, j] - W[:, j] * Ls[:, i]) % p == 0)
        frac = prop.sum() / len(Ls); worst = max(worst, frac)
        if frac > 1 / p + 1e-12: over += 1
    return p, os.path.basename(fn), len(Ls), worst, over, nid, bad_id
if __name__ == '__main__':
    rng = np.random.default_rng(11)
    for fn in sorted(glob.glob(os.path.join(HERE, 'gap', 'DL*_[57].json'))):
        p, name, nl, worst, over, nid, bad = run(fn, 150, rng)
        print(f'{name}: hard lines={nl} max fixed fraction={worst:.4f} (1/p={1/p:.4f}) over_bound={over} T=id samples={nid} T=id but top!=id: {bad}', flush=True)
