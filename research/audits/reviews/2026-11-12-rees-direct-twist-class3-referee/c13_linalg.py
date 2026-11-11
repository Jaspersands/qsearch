"""C1: for every central ideal N, all automorphisms alpha with alpha = kappa*id mod N
(i.e. preserving every line of L/N) solved by linear algebra: alpha = kappa*id + D, D: L -> N.
Report, per kappa, the dimension of the solution space and the action on [L,L] and on N.
C3: for every NON-central abelian ideal N: dim [L,N] and the max over labels u not
vanishing on [L,N] of the fraction of eta outside N with u o ad_eta |_N = 0."""
import sys, json, itertools, numpy as np
sys.path.insert(0, '.')
from lie import *
from c2_lines import intersect

CHARNIL7 = (7, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (0, 4): {5: 1}, (0, 5): {6: 1},
                (1, 2): {5: 5, 6: 2}, (1, 3): {6: 5}})
ALGS2 = dict(ALGS); ALGS2['charnil7'] = CHARNIL7

def line_preservers(C, N, p):
    """solve alpha = k id + D, D(e_j) in span N, alpha Lie hom; return list per k of (dim, sample checks)"""
    m = C.shape[0]; r = len(N); E = np.eye(m, dtype=np.int64)
    out = {}
    for k in range(1, p):
        # unknowns c[j, s]: D e_j = sum_s c[j,s] N_s.  equations for i<j:
        # alpha[e_i,e_j] - [alpha e_i, alpha e_j] = 0
        # alpha[e_i,e_j] = k [e_i,e_j] + sum_l C[i,j,l] D e_l
        # [alpha e_i, alpha e_j] = k^2 [e_i,e_j] + k[e_i, D e_j] + k[D e_i, e_j] + [D e_i, D e_j]
        # N central => last three vanish.  Linear: sum_l C[i,j,l] D e_l = (k^2-k)[e_i,e_j]
        A = []; bvec = []
        for i in range(m):
            for j in range(i + 1, m):
                for t in range(m):
                    row = np.zeros(m * r, dtype=np.int64)
                    for l in range(m):
                        for s in range(r):
                            row[l * r + s] = (row[l * r + s] + C[i, j, l] * N[s, t]) % p
                    A.append(row); bvec.append(((k * k - k) * C[i, j, t]) % p)
        A = np.array(A) % p; bvec = np.array(bvec) % p
        aug = np.hstack([A, bvec[:, None]])
        rA, raug = rank(A, p), rank(aug, p)
        if rA < raug: out[k] = None; continue
        # particular solution + nullspace; check action on [L,L] for random solutions
        R, piv = rref(aug, p)
        sols = []
        ns = nullspace(A, p)
        part = np.zeros(m * r, dtype=np.int64)
        for row, c in zip(R, piv):
            if c < m * r: part[c] = row[-1]
        Lp = derived(C, p)
        acts = set()
        rng = np.random.default_rng(0)
        for _ in range(30):
            c = part.copy()
            if len(ns): c = (c + rng.integers(0, p, len(ns)) @ ns) % p
            Dm = np.zeros((m, m), dtype=np.int64)
            for l in range(m): Dm[l] = (c[l * r:(l + 1) * r] @ N) % p
            M = (k * E + Dm) % p                    # rows = images
            # verify hom + invertible
            assert all(((C[i, j] @ M) % p == br(M[i], M[j], C, p)).all() for i in range(m) for j in range(m))
            if rank(M, p) < m: continue
            onLL = tuple(((Lp @ M - Lp) % p).flatten().tolist())
            onLL_scalar = [s for s in range(1, p) if ((Lp @ M - s * Lp) % p == 0).all()]
            onN = [s for s in range(1, p) if ((N @ M - s * N) % p == 0).all()]
            acts.add((tuple(onLL_scalar), tuple(onN)))
        out[k] = dict(dim_solutions=len(ns), action=[{'scalar_on_LL': list(a), 'scalar_on_N': list(b)} for a, b in sorted(acts)])
    return out

def c3(C, N, p):
    m = C.shape[0]; E = np.eye(m, dtype=np.int64)
    # [L,N]
    vs = [br(E[i], n, C, p) for i in range(m) for n in N]
    LN = np.array(rref(vs, p)[0], dtype=np.int64).reshape(-1, m)
    r = len(N)
    # u as functional on N in N-coordinates: u(sum c_s N_s) = c.u ; need [eta,N_s] in N-coords
    # coordinates of x in span N: solve
    def ncoords(x):
        A = np.vstack([N, x[None]]).T % p
        ns = nullspace(A, p); assert len(ns) >= 1
        v = ns[0]; return (-v[:r] * pow(int(v[r]), -1, p)) % p
    adm = np.zeros((m, r, r), dtype=np.int64)   # adm[i] : ad_{e_i}|_N in N coords, column s = coords of [e_i,N_s]
    for i in range(m):
        for s in range(r):
            x = br(E[i], N[s], C, p)
            adm[i, :, s] = ncoords(x) if x.any() else 0
    etas = np.array(list(itertools.product(range(p), repeat=m)), dtype=np.int64)
    outside = np.array([rank(np.vstack([N, e[None]]), p) > r for e in etas])
    etas = etas[outside]
    worst = 0.0; nbad = 0
    for u in itertools.product(range(p), repeat=r):
        u = np.array(u)
        if not u.any(): continue
        # u o ad_eta = sum_i eta_i (u @ adm[i])
        rowsU = np.array([(u @ adm[i]) % p for i in range(m)])   # (m, r)
        if not rowsU.any(): nbad += 1; continue                   # u vanishes on [L,N]
        frac = float((((etas @ rowsU) % p) == 0).all(1).mean())
        worst = max(worst, frac)
    return dict(dim_LN=len(LN), labels_vanishing_on_LN=nbad, max_frac_eta_fixing_label=worst)

if __name__ == '__main__':
    for name, p in [('heis3', 5), ('fil4', 5), ('fil4', 7), ('free23', 5), ('fil5', 5), ('fil4+1', 5), ('charnil7', 7)]:
        m, b = ALGS2[name]; C = tensor(m, b, p); assert jacobi_ok(C, p)
        Z = center(C, p); cls = len(lcs(C, p)) - 1; Lp = derived(C, p)
        # central ideals: subspaces of Z
        for kd in range(1, len(Z) + 1):
            for S in subspaces(len(Z), kd, p):
                N = np.array(rref(S @ Z % p, p)[0], dtype=np.int64)
                if len(N) == m: continue
                NL = intersect(N, Lp, p, m)
                res = line_preservers(C, N, p)
                print(json.dumps(dict(check='C1', alg=name, p=p, cls=cls, N=N.tolist(), dim_NcapLL=len(NL),
                       LmodN_nonabelian=rank(list(Lp) + list(N), p) > len(N),
                       kappas_admitting_line_preservers=[k for k, v in res.items() if v], detail=res)), flush=True)
        # non-central abelian ideals (exhaustive over subspaces, small m only)
        if m <= 5:
            cnt = 0; worst = 0; minLN = 99
            for kd in range(1, m):
                for S in subspaces(m, kd, p):
                    if not is_ideal(S, C, p) or not is_abelian_sub(S, C, p) or is_central(S, C, p): continue
                    r = c3(C, S, p); cnt += 1
                    worst = max(worst, r['max_frac_eta_fixing_label']); minLN = min(minLN, r['dim_LN'])
            print(json.dumps(dict(check='C3', alg=name, p=p, noncentral_abelian_ideals=cnt, min_dim_LN=minLN,
                                  max_frac_eta_fixing_label=worst, one_over_p=1 / p)), flush=True)
