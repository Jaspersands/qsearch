"""Exact automorphism checks (AI-written, pending human review).

Lemma A (uniform scalers): an automorphism that maps HZ to itself for EVERY cyclic H of
order p acts on L/Z by a scalar; if L/Z is nonabelian that scalar is 1 and the
automorphism is the identity on [L,L], so it scales the top central grade by 1.
Checked exhaustively:
  filiform4 at p = 5, 7: all automorphisms (images of the generators x1, x2 enumerated).
  free23 at p = 5, 7: all automorphisms modulo Z (determined by the images of x, y mod Z),
    then the action on Z of every lift.
Per-H scalers: for fixed non-homogeneous H, the scalars kappa by which automorphisms
preserving H act on Z (these exist, but the automorphisms depend on H).
"""
import itertools, json, sys
import numpy as np

def bracket_tensor(m, br, p):
    C = np.zeros((m, m, m), dtype=np.int64)
    for (i, j), d in br.items():
        for k, c in d.items():
            C[i, j, k] = c % p; C[j, i, k] = (-c) % p
    return C

def brv(A, B, C, p):
    return np.einsum('ni,nj,ijk->nk', A, B, C) % p

def rank_mod_p(M, p):
    M = [list(map(int, r)) for r in M]; r = 0; rows, cols = len(M), len(M[0])
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] % p), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; iv = pow(M[r][c], -1, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % p:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        r += 1
    return r

def filiform(p):
    m = 4
    C = bracket_tensor(m, {(0, 1): {2: 1}, (0, 2): {3: 1}}, p)
    vecs = np.array(list(itertools.product(range(p), repeat=m)), dtype=np.int64)
    auts = []
    for X1 in vecs:
        if not X1[:2].any(): continue                     # must be nonzero mod gamma_2
        X1b = np.broadcast_to(X1, vecs.shape)
        X3 = brv(X1b, vecs, C, p); X4 = brv(X1b, X3, C, p)
        ok = (brv(vecs, X3, C, p) == 0).all(1) & (brv(X1b, X4, C, p) == 0).all(1) \
             & (brv(vecs, X4, C, p) == 0).all(1) & (brv(X3, X4, C, p) == 0).all(1)
        # invertible <=> images of x1, x2 independent mod gamma_2 and X4 != 0
        det2 = (X1[0] * vecs[:, 1] - X1[1] * vecs[:, 0]) % p
        ok &= (det2 != 0) & X4.any(1)
        for idx in np.nonzero(ok)[0]:
            M = np.stack([X1, vecs[idx], X3[idx], X4[idx]])   # rows = images of basis
            auts.append(M)
    auts = np.array(auts)
    for M in auts[:: max(1, len(auts) // 200)]:
        assert rank_mod_p(M, p) == 4
    out = {"alg": "filiform4", "p": p, "aut_order": int(len(auts))}
    # Lemma A: induced map on L/Z (rows 0..2, cols 0..2) scalar?
    sub = auts[:, :3, :3]
    scal = np.array([np.array_equal(S, S[0, 0] * np.eye(3, dtype=np.int64) % p) for S in sub])
    kap = auts[:, 3, 3]
    out["n_preserving_all_HZ"] = int(scal.sum())
    out["kappa_on_Z_for_those"] = sorted(set(int(k) for k in kap[scal]))
    out["kappa_on_Z_all_auts"] = sorted(set(int(k) for k in kap))
    # per-H scalers
    per = {}
    for eta in ([1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 2, 3, 0]):
        eta = np.array(eta)
        img = (eta @ auts) % p                 # alpha(eta) = sum eta_i * row_i
        # proportional to eta?
        nz = np.nonzero(eta)[0][0]
        lamb = img[:, nz]
        prop = ((img - lamb[:, None] * eta[None, :]) % p == 0).all(1)
        per[str(eta.tolist())] = sorted(set(int(k) for k in kap[prop]))
    out["kappa_on_Z_preserving_H"] = per
    return out

def free23_quotient(p):
    """L/Z = Heisenberg <x,y,z>.  Every map x->X, y->Y (mod Z) with independent L1 parts
    extends to an automorphism of free23 (free nilpotent), and of L/Z."""
    lines = []
    for v in itertools.product(range(p), repeat=3):
        v = np.array(v); nz = np.nonzero(v)[0]
        if len(nz) and v[nz[0]] == 1: lines.append(v)
    lines = np.array(lines)
    C = bracket_tensor(5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}}, p)
    count = 0; good = []
    for X in itertools.product(range(p), repeat=3):
        for Y in itertools.product(range(p), repeat=3):
            d = (X[0] * Y[1] - X[1] * Y[0]) % p
            if d == 0: continue
            M = np.array([X, Y, [0, 0, d]])      # induced on L/Z; z -> [X,Y] = d z mod Z
            count += 1
            img = lines @ M % p
            nzc = np.argmax(lines != 0, axis=1)
            lam = img[np.arange(len(lines)), nzc]
            if ((img - lam[:, None] * lines) % p == 0).all():
                good.append((X, Y))
    # action on Z of every lift of the good maps: X~ = X + n1, Y~ = Y + n2, n_i in Z
    kappas = set()
    for X, Y in good:
        for n1 in itertools.product(range(p), repeat=2):
            for n2 in itertools.product(range(p), repeat=2):
                Xt = np.array([list(X) + list(n1)]); Yt = np.array([list(Y) + list(n2)])
                Zt = brv(Xt, Yt, C, p); W1 = brv(Xt, Zt, C, p)[0]; W2 = brv(Yt, Zt, C, p)[0]
                A = np.array([W1[3:], W2[3:]])
                kappas.add(tuple(map(int, A.flatten())))
    return {"alg": "free23", "p": p, "maps_mod_Z": count, "preserving_all_lines_mod_Z": len(good),
            "those_maps": [list(map(list, g)) for g in good],
            "action_on_Z_of_all_lifts(matrix rows w1,w2)": sorted(kappas)}

if __name__ == "__main__":
    for p in (5, 7):
        print(json.dumps(filiform(p)), flush=True)
    for p in (5, 7):
        print(json.dumps(free23_quotient(p)), flush=True)
