"""Type calculus of SOT merges, checked on explicit states (free23 over F_p, BCH group law).
For a labelled copy psi_lam (central label on gamma_3 = span(u,w)) we compute
F_lam(g) = <psi|R_g|psi> from the explicit vector and compare with 1_K(g) chi_lam(z(g)).
A merge with automorphism twists tau_i has F(g) = prod_i F_i(tau_i g) (trace identity); we check
  (A) identity twists + zero label sum  -> F = 1_K exactly (a genuine source of K/gamma_3),
  (B) a relative twist rho with rho(K) != K -> F supported on gamma_3 and H-independent,
  (C) rho in Stab(K), T_rho != id_V -> support K, top character sum_i lam_i o C_i,
  (D) informative iff Kbar in Fix(T_rho), and the informative fraction over hard K is <= 1/p.
Finite check only."""
import sys, itertools, numpy as np
sys.path.insert(0, '../2026-11-12-rees-direct-twist-class3-referee')
from lie import tensor, br, bch
FREE = (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}})

def setup(p):
    C = tensor(*FREE, p)
    allg = np.array(list(itertools.product(range(p), repeat=5)), dtype=np.int64)
    enc = lambda V: (V @ (p ** np.arange(4, -1, -1))).astype(np.int64)
    return C, allg, enc

def bchv(X, Y, C, p):
    """vectorised BCH, class 3, rows of X with rows of Y"""
    inv2 = pow(2, -1, p); inv12 = pow(12, -1, p)
    XY = np.einsum('ni,nj,ijk->nk', X, Y, C) % p
    Z = X + Y + inv2 * XY
    Z = Z + inv12 * (np.einsum('ni,nj,ijk->nk', X, XY, C) - np.einsum('ni,nj,ijk->nk', Y, XY, C))
    return Z % p

def Fstate(eta, lam, C, allg, enc, p):
    om = np.exp(2j * np.pi / p)
    supp = []; amp = []
    for t in range(p):
        for zu, zw in itertools.product(range(p), repeat=2):
            v = (t * eta + np.array([0, 0, 0, zu, zw])) % p
            supp.append(v); amp.append(om ** (-(lam[0] * zu + lam[1] * zw)))
    supp = np.array(supp); amp = np.array(amp) / np.sqrt(len(amp))
    psi = np.zeros(p ** 5, dtype=complex); psi[enc(supp)] = amp
    n = len(supp); N = len(allg)
    X = np.repeat(supp, N, axis=0); G = np.tile(allg, (n, 1))
    XG = enc(bchv(X, G, C, p)).reshape(n, N)
    F = (np.conj(psi[XG]) * amp[:, None]).sum(axis=0)   # sum_x conj(psi(x g)) psi(x)
    return F

def predF(eta, lam, allg, p):
    """1_K(g) chi(z(g)), K = F_p eta + gamma_3; g = t*eta + z (coords, since gamma_3 central)"""
    om = np.exp(2j * np.pi / p); out = np.zeros(len(allg), dtype=complex)
    for idx, g in enumerate(allg):
        # find t with g - t eta in gamma_3
        for t in range(p):
            r = (g - t * eta) % p
            if not r[:3].any():
                # h^t = exp(t eta); g = h^t * z with z = r (central) ; F = <psi, R_g psi> -> phase om^{-lam.z}?
                out[idx] = om ** (lam[0] * r[3] + lam[1] * r[4]); break
    return out

def aut_from(a, b, c, d, e, f, C, p):
    """Lie automorphism matrix M (x -> x @ M) with x -> (a,c,e,0,0), y -> (b,d,f,0,0)"""
    X = np.array([a, c, e, 0, 0]); Y = np.array([b, d, f, 0, 0])
    Z = br(X, Y, C, p); U = br(X, Z, C, p); W = br(Y, Z, C, p)
    return np.array([X, Y, Z, U, W]) % p

def Tbar(M):
    return M[:3, :3].T  # columns = images of xb, yb, zb in V

def fixes(T, v, p):
    w = (T @ v) % p
    return all((w[i] * v[j] - w[j] * v[i]) % p == 0 for i in range(3) for j in range(3))

def main(p, nH):
    C, allg, enc = setup(p); rng = np.random.default_rng(p)
    stats = dict(F_formula_mism=0, A_bad=0, B_bad=0, B_Hdep=0, C_bad=0, D_mism=0, informative=0, trials=0)
    hardH = []
    while len(hardH) < nH:
        eta = rng.integers(0, p, 5)
        if eta[:2].any(): hardH.append(eta)
    cache = {}
    def F(eta, lam):
        key = (tuple(eta), tuple(lam))
        if key not in cache: cache[key] = Fstate(eta, lam, C, allg, enc, p)
        return cache[key]
    idx = {tuple(g): i for i, g in enumerate(allg)}
    def pull(Fv, M):     # g -> F(tau g), tau(g) = g @ M (Lazard: group aut = Lie aut on coords)
        img = (allg @ M) % p
        return Fv[enc(img)]
    gam3 = (~allg[:, :3].any(axis=1))
    for eta in hardH:
        lams = [rng.integers(0, p, 2) for _ in range(2)]
        lams.append((-(lams[0] + lams[1])) % p)
        for lam in lams:
            if not np.allclose(F(eta, lam), predF(eta, lam, allg, p), atol=1e-9): stats['F_formula_mism'] += 1
        Kmask = np.zeros(len(allg), bool)
        for g_i, g in enumerate(allg):
            Kmask[g_i] = any(not ((g - t * eta) % p)[:3].any() for t in range(p))
        # (A)
        FA = F(eta, lams[0]) * F(eta, lams[1]) * F(eta, lams[2])
        if not np.allclose(FA, Kmask.astype(float), atol=1e-9): stats['A_bad'] += 1
        # (B),(C),(D): random automorphism rho as relative twist on copy 2 (copy 1 untwisted)
        for trial in range(12):
            while True:
                a, b, c, d, e, f = rng.integers(0, p, 6)
                if not (a * d - b * c) % p: continue
                if trial < 6: break
                Tt = Tbar(aut_from(a, b, c, d, e, f, C, p))
                if fixes(Tt, eta[:3] % p, p) and not (Tt == np.eye(3, dtype=np.int64)).all(): break
            M = aut_from(a, b, c, d, e, f, C, p)
            T = Tbar(M); Kb = eta[:3] % p
            stats['trials'] += 1
            Fm = F(eta, lams[0]) * pull(F(eta, lams[1]), M)
            supp = np.abs(Fm) > 1e-9
            inform = supp.sum() > p * p
            if inform != fixes(T, Kb, p): stats['D_mism'] += 1
            if inform:
                stats['informative'] += 1
                # (C): support = K, character on gamma_3 = lam0 + lam1 o C
                Cm = M[3:, 3:]   # rows: images of u,w in (u,w) coords
                if not (supp == Kmask).all(): stats['C_bad'] += 1
                om = np.exp(2j * np.pi / p)
                for g_i in np.nonzero(gam3)[0]:
                    z = allg[g_i][3:]; Cz = (z @ Cm) % p
                    pred = om ** (lams[0] @ z + lams[1] @ Cz)
                    if abs(Fm[g_i] - pred) > 1e-9: stats['C_bad'] += 1; break
            else:
                if not (supp == gam3).all(): stats['B_bad'] += 1
                # H-independence: same labels, a different hard H with same twist and not fixed
                for eta2 in hardH:
                    if fixes(T, eta2[:3] % p, p): continue
                    Fm2 = F(eta2, lams[0]) * pull(F(eta2, lams[1]), M)
                    if not np.allclose(Fm, Fm2, atol=1e-9): stats['B_Hdep'] += 1
                    break
    # (D') informative fraction over ALL hard Kbar for random T != id (exact count)
    worst = 0.0
    hardK = [np.array([1, b, c]) for b in range(p) for c in range(p)] + [np.array([0, 1, c]) for c in range(p)]
    for _ in range(300):
        while True:
            a, b, c, d, e, f = rng.integers(0, p, 6)
            if (a * d - b * c) % p: break
        T = Tbar(aut_from(a, b, c, d, e, f, C, p))
        if (T % p == np.eye(3, dtype=np.int64)).all(): continue
        worst = max(worst, sum(fixes(T, K, p) for K in hardK) / len(hardK))
    print(f'p={p}', stats, 'max informative fraction over hard K (300 random T != id):', round(worst, 4), '1/p =', round(1 / p, 4), flush=True)

if __name__ == '__main__':
    main(5, 6)
    main(7, 3)
