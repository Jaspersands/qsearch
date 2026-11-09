"""Exact classification at p = 5, kappa = 2 (S = {0,+-1}), k = 2 dependencies:
for every GL_2(F_5)-orbit of label sets L' subset of F_5^2 minus 0 that span F_5^2, decide whether a
2-dimensional realization exists (gadget_cnf, weak nondegeneracy = per projective direction).

Cross-check for small label sets: the realizable set is the image of S^{L'} in
F_5^{L'} / <r_1, r_2> (r_j = j-th coordinates of the labels); gain 2 iff that image contains a
2-dimensional subspace (direct enumeration when |L'| <= 9).

Output: counts by |L'|; every infeasible spanning orbit representative is printed.
"""
import itertools, sys, time
import numpy as np
from gadget_cnf import solve

p = 5
S = [0, 1, 4]
vecs = [v for v in itertools.product(range(p), repeat=2) if any(v)]   # 24 labels
idx = {v: i for i, v in enumerate(vecs)}
# GL_2(F_5) generators acting on labels
def mat_perm(M):
    return [idx[tuple(int(x) % p for x in np.array(M) @ np.array(v))] for v in vecs]
gens = [mat_perm([[1, 1], [0, 1]]), mat_perm([[0, 1], [1, 0]]), mat_perm([[2, 0], [0, 1]]), mat_perm([[1, 0], [0, 2]])]

N = 1 << 24
def perm_image(perm):
    """vectorised: image of every subset (24-bit int) under the label permutation."""
    tabs = []
    for byte in range(3):
        t = np.zeros(256, dtype=np.int64)
        for b in range(256):
            img = 0
            for bit in range(8):
                if b >> bit & 1:
                    img |= 1 << perm[8 * byte + bit]
            t[b] = img
        tabs.append(t)
    x = np.arange(N, dtype=np.int64)
    return tabs[0][x & 255] | tabs[1][(x >> 8) & 255] | tabs[2][(x >> 16) & 255]

t0 = time.time()
imgs = [perm_image(g) for g in gens]
lab = np.arange(N, dtype=np.int64)
while True:
    new = lab.copy()
    for im in imgs:
        np.minimum.at(new, im, lab)          # label of image <- min(label of image, label of x)
        new = np.minimum(new, new[im])        # propagate back
    # symmetric closure: also pull labels along inverse direction
    changed = not np.array_equal(new, lab)
    lab = new
    if not changed:
        break
reps = np.nonzero(lab == np.arange(N))[0]
print(f'orbits: {len(reps)} (union-find {time.time()-t0:.1f}s)', flush=True)

def spanning(Lp):
    M = np.array(Lp, dtype=np.int64)
    return len(Lp) >= 2 and any((a[0]*b[1]-a[1]*b[0]) % p for a in Lp for b in Lp)

def direct_gain2(Lp):
    """Image of S^c in F_5^c/<r1,r2>: contains a 2-dim subspace, or 0 has a nonzero S-realizer (witness)?"""
    c = len(Lp)
    R = np.array(Lp, dtype=np.int64).T  # 2 x c, rows r1, r2
    # complement basis: a c x (c-2) matrix whose columns are orthogonal to the rows... use quotient map
    # quotient map Q: F_5^c -> F_5^{c-2} with kernel = rowspace(R): rows of Q = basis of the annihilator
    from verify_gadget import nullspace_mod
    Q = nullspace_mod(R, p)      # (c-2) x c, rows z with R z = 0  -> kernel of Q is rowspace? no: Q rows annihilate rowspace(R)
    # vectors y, y' realize the same element iff y - y' in rowspace(R); Q y determines the class since
    # rows of Q span the annihilator of rowspace(R) (dim c-2) and Q y = Q y' iff y - y' in rowspace(R).
    img = set()
    for y in itertools.product(S, repeat=c):
        img.add(tuple(int(x) for x in (Q @ np.array(y)) % p))
    zero = tuple([0] * (c - 2))
    # direct S-dependency among class sums (a witness): nonzero y in S^c with Q y = 0
    witness = any(any(y) and tuple(int(x) for x in (Q @ np.array(y)) % p) == zero
                  for y in itertools.product(S, repeat=c))
    if witness:
        return True
    img.discard(zero)
    pts = list(img)
    for h1 in pts:
        for h2 in pts:
            if h1 >= h2:
                continue
            ok = True
            for a in range(p):
                for b in range(p):
                    if (a, b) in ((0, 0), (1, 0), (0, 1)):
                        continue
                    v = tuple((a * x + b * y) % p for x, y in zip(h1, h2))
                    if v == tuple([0] * (c - 2)) or v not in img:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return True
    return False

by_size = {}
bad = []
t0 = time.time()
for n, r in enumerate(reps):
    Lp = [vecs[i] for i in range(24) if r >> i & 1]
    if not spanning(Lp):
        continue
    res, sol, dt = solve(p, S, 2, 2, Lp, nondeg=True, weak=True)
    feas = res == 'sat'
    c = len(Lp)
    by_size.setdefault(c, [0, 0])
    by_size[c][feas] += 1
    if c <= 7:
        dg = direct_gain2(Lp)
        assert dg == feas, (Lp, dg, feas)
    if not feas:
        bad.append(Lp)
        print('INFEASIBLE', Lp, flush=True)
    if n % 2000 == 0:
        print(f'  ... {n}/{len(reps)} orbits, {time.time()-t0:.0f}s', flush=True)
print('size: (infeasible, feasible) orbits of spanning label sets')
for c in sorted(by_size):
    print(f'  |L|={c:2d}: infeasible {by_size[c][0]:5d}  feasible {by_size[c][1]:5d}')
print(f'total infeasible spanning orbits: {len(bad)}; direct cross-check done for |L| <= 7')
