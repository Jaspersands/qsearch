"""C2: exhaustive over Aut(L) for central ideals N.  For each automorphism preserving N:
 - does it act trivially on N cap [L,L]?
 - which lines of L/N does it preserve?
Claims tested: (T2/3) preserving ALL lines of L/N and class>=3  =>  identity on [L,L];
(T-avg) any automorphism acting nontrivially on N cap [L,L] preserves at most a fraction
rho = (p^{m-1}+p-2)/(p^m-1) <= 2/(p+1) of the lines of L/N (m = dim L/N), class >= 3;
LP: best H-independent distribution of such twists -> min over lines of P[preserve]."""
import sys, json, itertools, numpy as np
sys.path.insert(0, '.')
from lie import *
from scipy.optimize import linprog

WORDS = {'heis3': [(0, 1)], 'fil4': [(0, 1), (0, 2)], 'free23': [(0, 1), (0, 2), (1, 2)],
         'fil5': [(0, 1), (0, 2), (0, 3)]}

def brv(A, B, C, p): return np.einsum('ni,nj,ijk->nk', A, B, C) % p

def complete_basis(B, m, p):
    rows = [list(b) for b in B]; E = np.eye(m, dtype=np.int64); comp = []
    for e in E:
        if rank(rows + [list(e)], p) > len(rows): rows.append(list(e)); comp.append(e)
    return np.array(comp, dtype=np.int64)

def quotient_proj(B, m, p):
    """matrix P (m x (m-r)) with kernel = span B, as coordinates in basis (B, comp)."""
    comp = complete_basis(B, m, p)
    T = np.vstack([B, comp]) if len(B) else comp       # rows = new basis
    # coordinates: x = c @ T  => c = x @ T^{-1}
    Tinv = inv_mod(T, p)
    return (Tinv[:, len(B):]) % p, comp

def inv_mod(T, p):
    m = len(T); A = np.hstack([T % p, np.eye(m, dtype=np.int64)])
    R, piv = rref(A, p); R = np.array(R, dtype=np.int64)
    assert piv[:m] == list(range(m))
    return R[:, m:] % p

def run(name, p):
    m, b = ALGS[name]; C = tensor(m, b, p); W = WORDS[name]
    Lp = derived(C, p); Z = center(C, p)
    cls = len(lcs(C, p)) - 1
    # central ideals N: all nonzero subspaces of Z (central => ideal)
    Ns = []
    for k in range(1, len(Z) + 1):
        for S in subspaces(len(Z), k, p):
            Ns.append(np.array(rref(S @ Z % p, p)[0], dtype=np.int64))
    vecs = np.array(list(itertools.product(range(p), repeat=m)), dtype=np.int64)
    stats = []
    prep = []
    for N in Ns:
        P, comp = quotient_proj(N, m, p)
        q = m - len(N)
        ln = lines(q, p) @ comp % p   # representatives in L (combinations of complement)
        # N cap [L,L]
        NL = intersect(N, Lp, p, m)
        LmodN_nonab = rank(list(Lp) + list(N), p) > len(N)
        prep.append(dict(N=N, P=P, ln=ln, NL=NL, nonab=LmodN_nonab, q=q,
                         pats_nontriv=set(), pats_all=set(), n_allpres=0, allpres_nontriv=0, n_pres_N=0))
    for X in vecs:
        if not (X[0] * 1 or X[1]): pass
        Xb = np.broadcast_to(X, vecs.shape)
        img = [Xb, vecs]
        for w in W: img.append(brv(img[w[0]], img[w[1]], C, p))
        M = np.stack(img, axis=1)
        ok = ((X[0] * vecs[:, 1] - X[1] * vecs[:, 0]) % p != 0)
        for i in range(m):
            for j in range(i + 1, m):
                if not ok.any(): break
                lhs = np.einsum('k,nkl->nl', C[i, j], M) % p
                ok &= (lhs == brv(M[:, i], M[:, j], C, p)).all(1)
        M = M[ok]
        if len(M) == 0: continue
        for d in prep:
            N = d['N']
            imN = np.einsum('rk,nkl->nrl', N, M) % p          # images of N basis
            # alpha(N) subset N  <=> imN @ P == 0
            keep = ((imN @ d['P']) % p == 0).all((1, 2))
            Mk = M[keep]
            if len(Mk) == 0: continue
            d['n_pres_N'] += len(Mk)
            if len(d['NL']):
                imNL = np.einsum('rk,nkl->nrl', d['NL'], Mk) % p
                triv = (imNL == d['NL'][None]).all((1, 2))
            else:
                triv = np.ones(len(Mk), dtype=bool)
            t = (d['ln'] @ d['P']) % p                         # (L, q)
            w = np.einsum('lk,nkj,jq->nlq', d['ln'], Mk, d['P']) % p   # (n, L, q)
            cross = (w[:, :, :, None] * t[None, :, None, :] - w[:, :, None, :] * t[None, :, :, None]) % p
            pres = (cross == 0).all((2, 3))                     # (n, L)
            allp = pres.all(1)
            d['n_allpres'] += int(allp.sum()); d['allpres_nontriv'] += int((allp & ~triv).sum())
            packed = np.packbits(pres, axis=1)
            for row, tr in zip(packed, triv):
                key = row.tobytes()
                d['pats_all'].add(key)
                if not tr: d['pats_nontriv'].add(key)
    res = []
    for d in prep:
        L = len(d['ln']); q = d['q']
        rho = (p ** (q - 1) + p - 2) / (p ** q - 1) if q >= 2 else 1.0
        pats = [np.unpackbits(np.frombuffer(k, dtype=np.uint8))[:L] for k in d['pats_nontriv']]
        maxfrac = max((pt.sum() / L for pt in pats), default=None)
        lp = None
        if pats:
            A = np.array(pats, dtype=float)    # (K, L)
            K = len(A)
            # variables pi_1..pi_K, t ; maximize t s.t. A^T pi >= t, sum pi = 1
            c = np.zeros(K + 1); c[-1] = -1
            Aub = np.hstack([-A.T, np.ones((L, 1))]); bub = np.zeros(L)
            Aeq = np.hstack([np.ones((1, K)), np.zeros((1, 1))])
            r = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=[1], bounds=[(0, None)] * K + [(None, None)], method='highs')
            lp = float(-r.fun)
        res.append(dict(alg=name, p=p, cls=cls, N=d['N'].tolist(), dimNcapLL=len(d['NL']), LmodN_nonabelian=d['nonab'],
                        auts_preserving_N=d['n_pres_N'], preserving_all_lines=d['n_allpres'],
                        preserving_all_lines_but_nontrivial_on_NcapLL=d['allpres_nontriv'],
                        n_lines=L, max_frac_lines_nontriv=maxfrac, rho=rho, two_over_p1=2 / (p + 1),
                        LP_best_min_line_prob_nontriv=lp, one_over_p=1 / p))
    return res

def intersect(A, B, p, m):
    if len(A) == 0 or len(B) == 0: return np.zeros((0, m), dtype=np.int64)
    # x = a@A = b@B  -> nullspace of [A; -B]^T
    Mt = np.vstack([A, (-B) % p]).T % p
    ns = nullspace(Mt, p)
    vs = [ (n[:len(A)] @ A) % p for n in ns]
    R, _ = rref(vs, p) if vs else ([], [])
    return np.array(R, dtype=np.int64).reshape(-1, m)

if __name__ == '__main__':
    todo = [('heis3', 5), ('heis3', 7), ('fil4', 5), ('fil4', 7), ('fil5', 5), ('free23', 5)]
    if len(sys.argv) > 1: todo = [(sys.argv[1], int(sys.argv[2]))]
    for name, p in todo:
        for r in run(name, p): print(json.dumps(r), flush=True)
