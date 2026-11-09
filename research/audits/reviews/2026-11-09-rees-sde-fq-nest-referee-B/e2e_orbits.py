"""Referee B: end-to-end semantic check of Fact F5's conclusion on real column sets.
For every spanning orbit representative L with |L| >= 3: build columns v_1..v_c' in F_5^{c'-2} whose
dependency space is exactly the row space of the 2 x c' label matrix (labels L, plus a random number
of duplicated labels), apply a random invertible change of coordinates and a random column order,
and run simple5.two_dim_piece with U = 0 (the solver picks its own dependency basis, so it sees a
GL_2-transform of L).  Asserted inside: every one of the 24 realizers is S-valued and sums to
alpha.h; outcome is gain-2 (h1, h2 independent) or a verified nonzero S-witness.
"""
import itertools, numpy as np, multiprocessing as mp, time
import simple5 as s
p = 5
vecs = [v for v in itertools.product(range(p), repeat=2) if any(v)]

def rand_gl(n, rng):
    while True:
        A = rng.integers(0, p, size=(n, n))
        if s.nullspace(A).shape[0] == 0:
            return A

def run(args):
    mask, seed = args
    rng = np.random.default_rng(seed)
    L = [vecs[i] for i in range(24) if mask >> i & 1]
    out = []
    for dup in (0, int(rng.integers(1, 5))):
        labs = L + [L[int(rng.integers(len(L)))] for _ in range(dup)]
        perm = rng.permutation(len(labs)); labs = [labs[i] for i in perm]
        R = np.array(labs, dtype=np.int64).T          # 2 x c'
        Nb = s.nullspace(R)                            # (c'-2) x c', rows annihilate the label rows
        n = Nb.shape[0]
        lam = (rand_gl(n, rng) @ Nb) % p if n else Nb
        assert s.nullspace(lam).shape[0] == 2
        U = s.Quot(n)
        res, unused = s.two_dim_piece(lam, U, list(range(lam.shape[1])))
        if res[0] == 'witness':
            x = res[1]
            assert x.any() and all(int(v) in s.S for v in x) and not ((lam @ x) % p).any()
            out.append('witness')
        else:
            h = res[3]
            Q = s.Quot(n); a = Q.add(h[0]); b = Q.add(h[1])
            assert a and b, 'claimed gain but h dependent'
            out.append('gain2')
    return len(L), out

if __name__ == '__main__':
    reps = [int(r) for r in np.load('reps_f5.npy')]
    reps = [r for r in reps if bin(r).count('1') >= 3]
    t0 = time.time(); by = {}
    with mp.Pool(8) as pool:
        for c, out in pool.imap_unordered(run, [(r, i) for i, r in enumerate(reps)], chunksize=20):
            d = by.setdefault(c, {'gain2': 0, 'witness': 0})
            for o in out:
                d[o] += 1
    print('|L|: outcomes over (exact labels, labels with duplicates) column sets')
    for c in sorted(by):
        print(f'  {c:2d}: gain2 {by[c]["gain2"]:6d}  witness {by[c]["witness"]:6d}')
    print('orbits tested', len(reps), 'x 2 column sets; 0 failures (any failure raises)', f'{time.time()-t0:.0f}s')
