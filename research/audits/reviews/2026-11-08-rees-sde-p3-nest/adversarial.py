"""Adversarial tests of WNEST (wnest.py).  Every run keeps the per-piece asserts of wnest.py on
(wt >= r*+2, wt <= 2N/3 + 2 sqrt(N)/3, invariant N* - 1.5 r* >= N - 1.5 rank F, series classes
<= 2 after peeling), so an assertion failure anywhere here would refute the worst-case proof.

(A) structured families at n = 60 (chains = large series classes, low rank, two subspaces,
    duplicated columns, sparse columns, Hamming-like projective columns, signed blocks,
    weight-gap designs), WNEST vs KOW.
(B) hill climb over instances at n in {8, 10, 12, 14}: maximize m_used (columns pulled) of
    deterministic WNEST, starting from random and from chain instances; compare with the
    formula bound and record the largest per-piece |X| - q seen.
"""
import math, sys, itertools
import numpy as np
from wnest import Run, stream_from_list, stream_random, pool_size, bound, kernel, rank

def run_mode(vectors, n, mode, rng):
    R = Run(n, stream_from_list(vectors), mode)
    sol = R.run(rng)
    return (len(R.stream) if sol is not None else None), R

def pad_stream(vectors, n, rng, total):
    """family vectors first, then random filler so that the run can always finish."""
    out = [np.asarray(v, dtype=np.int64) % 3 for v in vectors]
    while len(out) < total:
        out.append(rng.integers(0, 3, n))
    return out

def fam_chains(n, rng, a, count):
    """count chains of length a: e_1, e_2-e_1, ..., e_a - e_{a-1} in disjoint coordinate blocks,
    endpoints e_a all lying in a common subspace spanned by the last n - count*a + count coords,
    followed by random vectors in that subspace."""
    vecs = []
    base = 0
    tail_start = count * (a - 1)
    for c in range(count):
        coords = list(range(base, base + a - 1)) + [tail_start + c]
        v = np.zeros(n, dtype=np.int64); v[coords[0]] = 1; vecs.append(v)
        for j in range(1, a):
            v = np.zeros(n, dtype=np.int64); v[coords[j]] = 1; v[coords[j - 1]] = 2; vecs.append(v)
        base += a - 1
    sub = list(range(tail_start, n))
    for _ in range(3 * n):
        v = np.zeros(n, dtype=np.int64); v[sub] = rng.integers(0, 3, len(sub)); vecs.append(v)
    return vecs

def fam_lowrank(n, rng, k):
    vecs = []
    for _ in range(3 * n):
        v = np.zeros(n, dtype=np.int64); v[:k] = rng.integers(0, 3, k); vecs.append(v)
    return vecs

def fam_two_subspaces(n, rng):
    vecs = []
    h = n // 2
    for i in range(3 * n):
        v = np.zeros(n, dtype=np.int64)
        if i % 2 == 0: v[:h] = rng.integers(0, 3, h)
        else: v[h:] = rng.integers(0, 3, n - h)
        vecs.append(v)
    return vecs

def fam_duplicates(n, rng):
    vecs = []
    for _ in range(2 * n):
        v = rng.integers(0, 3, n); vecs += [v.copy(), v.copy()]
    return vecs

def fam_sparse(n, rng):
    vecs = []
    for i in range(n):
        v = np.zeros(n, dtype=np.int64); v[i] = 1; vecs.append(v)
    for _ in range(3 * n):
        v = np.zeros(n, dtype=np.int64); i, j = rng.choice(n, 2, replace=False)
        v[i] = rng.integers(1, 3); v[j] = rng.integers(1, 3); vecs.append(v)
    return vecs

def fam_projective(n, rng, k):
    """all projectively distinct nonzero vectors of F_3^k (first nonzero = 1) in the first k coords,
    in random order, each once; then random filler.  (3^k-1)/2 vectors of rank k."""
    pts = []
    for v in itertools.product(range(3), repeat=k):
        if any(v) and v[next(i for i, x in enumerate(v) if x)] == 1:
            w = np.zeros(n, dtype=np.int64); w[:k] = v; pts.append(w)
    rng.shuffle(pts)
    return pts

def fam_signed_blocks(n, rng, b):
    vecs = []
    for _ in range(3 * n):
        v = np.zeros(n, dtype=np.int64)
        blk = rng.integers(0, n // b)
        v[blk * b:(blk + 1) * b] = rng.integers(1, 3, b); vecs.append(v)
    return vecs

def fam_weightgap(n, rng):
    """columns chosen so that the first pool's dependency code is a direct sum of two codes on
    disjoint halves (block-diagonal V): weights are sums of two concentrated halves."""
    vecs = []
    h = n // 2
    for i in range(3 * n):
        v = np.zeros(n, dtype=np.int64)
        if i % 3 == 0: v[:h] = rng.integers(0, 3, h)
        elif i % 3 == 1: v[h:] = rng.integers(0, 3, n - h)
        else: v[:] = rng.integers(0, 3, n)
        vecs.append(v)
    return vecs

def part_A(rng):
    n = 60
    fams = {
        "random": lambda: [rng.integers(0, 3, n) for _ in range(3 * n)],
        "chains_a20_x3": lambda: fam_chains(n, rng, 20, 3),
        "chains_a10_x6": lambda: fam_chains(n, rng, 10, 6),
        "chains_a5_x12": lambda: fam_chains(n, rng, 5, 12),
        "lowrank_30": lambda: fam_lowrank(n, rng, 30),
        "two_subspaces": lambda: fam_two_subspaces(n, rng),
        "duplicates": lambda: fam_duplicates(n, rng),
        "sparse": lambda: fam_sparse(n, rng),
        "projective_k7": lambda: fam_projective(n, rng, 7),
        "signed_blocks_6": lambda: fam_signed_blocks(n, rng, 6),
        "weightgap": lambda: fam_weightgap(n, rng),
    }
    total = int(bound(n)) + 50
    print(f"(A) n = {n}: m_used for WNEST (deterministic) and KOW; formula bound(n) = {bound(n):.0f}; "
          f"n^2/4 = {n*n/4:.0f}, n^2/3 = {n*n/3:.0f}.  All WNEST per-piece asserts on.")
    print("family            WNEST m_used          KOW m_used        max(|X|-q) WNEST   max series class seen")
    for name, mk in fams.items():
        mw, mk_, mx, mser = [], [], [], 0
        for rep in range(3):
            vecs = pad_stream(mk(), n, rng, 3 * total)
            m1, R1 = run_mode(vecs, n, "wnest", rng)
            m2, R2 = run_mode(vecs, n, "kow", rng)
            mw.append(m1); mk_.append(m2)
            mx.append(max([c[2] - c[0] for c in R1.costs if c[1] == 2], default=None))
            # largest series class in the first pool before peeling
            P = np.eye(n, dtype=np.int64)
            F = vecs[:pool_size(n)]
            B = kernel((np.array(F).T) % 3)
            from wnest import series_class_sizes
            if B.shape[0]:
                mser = max(mser, series_class_sizes(B)[0])
        print(f"{name:17s} {str(mw):22s} {str(mk_):18s} {str(mx):18s} {mser}")
        sys.stdout.flush()

def objective(vectors, n, rng):
    """m_used of deterministic WNEST; failure (stream exhausted) counts as len+1."""
    R = Run(n, stream_from_list(vectors), "wnest")
    sol = R.run(rng)
    if sol is None:
        return len(vectors) + 1, R
    return len(R.stream), R

def part_B(rng):
    print("\n(B) hill climb over instances (maximize WNEST m_used); 'fail' = stream exhausted before a solution")
    print(" n   m_stream  formula  start      best m_used (random start, chain start)   max |X|-q   cap 2N/3+2sqrtN/3-q at q=n")
    for n in (8, 10, 12, 14):
        formula = bound(n)
        m_stream = int(formula) + 10
        results = []
        worst_piece = -10 ** 9
        for start in ("random", "chains"):
            if start == "random":
                cur = [rng.integers(0, 3, n) for _ in range(m_stream)]
            else:
                cur = pad_stream(fam_chains(n, rng, max(3, n // 3), 2), n, rng, m_stream)
            cur_val, R = objective(cur, n, rng)
            best = cur_val
            for it in range(400):
                cand = [v.copy() for v in cur]
                for _ in range(rng.integers(1, 4)):
                    i = rng.integers(0, m_stream); j = rng.integers(0, n)
                    cand[i][j] = (cand[i][j] + rng.integers(1, 3)) % 3
                val, Rc = objective(cand, n, rng)
                if val >= cur_val:
                    cur, cur_val = cand, val
                    if val > best:
                        best = val
                    pieces = [c[2] - c[0] for c in Rc.costs if c[1] == 2]
                    if pieces:
                        worst_piece = max(worst_piece, max(pieces))
            results.append(best)
        N = pool_size(n)
        cap = 2 * N / 3 + 2 * math.sqrt(N) / 3 - n
        flag = " (never failed)" if max(results) <= m_stream else " FAIL"
        print(f"{n:3d}  {m_stream:6d}   {formula:7.1f}             {results}{flag}        {worst_piece}       {cap:.2f}")
        sys.stdout.flush()

if __name__ == "__main__":
    rng = np.random.default_rng(20261108)
    part_A(rng)
    part_B(rng)
    print("\nno assertion fired: every piece satisfied wt >= r*+2 and wt <= 2N/3 + 2 sqrt(N)/3, and every witness summed to zero")
