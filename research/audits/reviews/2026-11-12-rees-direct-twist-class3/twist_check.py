"""Exact finite check of the Ivanyos-Sanselme-Santha (ISS) twist template on graded
Lazard groups of class <= 3 (AI-written, pending human review).

Groups: exp(L) with the class-3 BCH product, elements in exponential coordinates,
encoded as integers.  All arithmetic is exact mod p; phases are exponents of
omega = exp(2 pi i / p).

For every cyclic subgroup H = <exp(eta)> of order p (every line F_p eta) and every
character label u of an abelian normal layer N, we build the ISS state
    psi_u(a) = sum_{t in F_p, z in N} omega^{-<u,z>} |a * (t eta) * z>
and test, exactly, whether right multiplication by
  (A) h = exp(eta)                      [N = gamma_2, ISS target H gamma_2]
  (B) delta_s(h), s = 2..p-1            [N = top grade Z, Ivanyos-Santha target HZ]
maps psi_u(a) to a scalar multiple of itself.  Predictions:
  (A) eigen  <=>  u_3 o ad_{v1} = 0 on L_2         (label-shift obstruction)
  (B) eigen  <=>  v1 = 0 or v_mid = 0              (dilations move HZ); v_mid = part of eta
                   in grades 2..class-1 (empty for class 2, = v2 for class 3)
For eigen cases of (A) we also record the phase exponent c(s) of
psi_u(a) . delta_s(h) = omega^{c(s)} psi_u(a) and check that c is a polynomial in s
of degree <= class with c(0) = 0, i.e. absorbable by a bounded-degree diagonal system.
"""
import itertools, sys, json
import numpy as np

ALG = {
    # name: (dim, grades, brackets {(i,j): {k: coeff}} for i<j)
    "heis3":    (3, [1, 1, 2], {(0, 1): {2: 1}}),
    "filiform4": (4, [1, 1, 2, 3], {(0, 1): {2: 1}, (0, 2): {3: 1}}),
    "free23":   (5, [1, 1, 2, 3, 3], {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}}),
}

class Grp:
    def __init__(self, name, p):
        self.name, self.p = name, p
        m, grades, br = ALG[name]
        self.m, self.grades = m, np.array(grades)
        C = np.zeros((m, m, m), dtype=np.int64)
        for (i, j), d in br.items():
            for k, c in d.items():
                C[i, j, k] = c % p
                C[j, i, k] = (-c) % p
        self.C = C
        self.inv2 = pow(2, -1, p); self.inv12 = pow(12, -1, p)
        self.n = p ** m
        self.pw = p ** np.arange(m)
        self.coords = (np.arange(self.n)[:, None] // self.pw) % p   # n x m
        self._table()

    def br(self, A, B):
        return np.einsum('ni,nj,ijk->nk', A, B, self.C) % self.p

    def bch(self, X, Y):
        p = self.p
        XY = self.br(X, Y)
        return (X + Y + self.inv2 * XY + self.inv12 * (self.br(X, XY) - self.br(Y, XY))) % p

    def enc(self, V):
        return (np.asarray(V) % self.p) @ self.pw

    def _table(self):
        n = self.n
        T = np.empty((n, n), dtype=np.int32)
        Y = self.coords
        for a in range(n):
            X = np.broadcast_to(self.coords[a], (n, self.m))
            T[a] = self.enc(self.bch(X, Y))
        self.T = T

    def dil(self, V, s):
        return (np.asarray(V) * (s ** self.grades)) % self.p

    def bracket1(self, x, y):
        return self.br(np.array([x]), np.array([y]))[0]


def layer_positions(G, kmin):
    return [i for i in range(G.m) if G.grades[i] >= kmin]

def lines(G):
    p, m = G.p, G.m
    for v in itertools.product(range(p), repeat=m):
        v = np.array(v)
        nz = np.nonzero(v)[0]
        if len(nz) and v[nz[0]] == 1:
            yield v

def state(G, a, eta, Npos, u):
    """support indices and phase exponents of psi_u(a)."""
    p = G.p
    zs = np.array(list(itertools.product(range(p), repeat=len(Npos))), dtype=np.int64)
    Zfull = np.zeros((len(zs), G.m), dtype=np.int64); Zfull[:, Npos] = zs
    zidx = G.enc(Zfull)
    ex = (-(zs @ np.asarray(u))) % p
    S, E = [], []
    for t in range(p):
        ah = G.T[a, G.enc(t * eta)]
        S.append(G.T[ah, zidx]); E.append(ex)
    S = np.concatenate(S); E = np.concatenate(E)
    assert len(np.unique(S)) == len(S), "coset elements not distinct"
    return S, E

def right_mult_ratio(G, S, E, g):
    """None if psi.g is not a multiple of psi; else the phase exponent c with psi.g = w^c psi."""
    S2 = G.T[S, g]
    o1 = np.argsort(S); o2 = np.argsort(S2)
    if not np.array_equal(S[o1], S2[o2]):
        inter = len(np.intersect1d(S, S2))
        return None, inter
    # amplitude of psi.g at x = S2[i] is omega^{E[i]}; psi at x is omega^{E_old}
    d = (E[o2] - E[o1]) % G.p
    if np.all(d == d[0]):
        return int(d[0]), len(S)
    return None, len(S)

def poly_degree_mod_p(vals, p):
    """degree of the unique poly of degree < p interpolating vals[s], s=0..p-1."""
    # Lagrange via solving Vandermonde mod p
    A = np.array([[pow(s, k, p) for k in range(p)] for s in range(p)], dtype=object)
    b = list(vals)
    # gaussian elimination mod p
    M = [list(A[i]) + [b[i]] for i in range(p)]
    for c in range(p):
        r = next(r for r in range(c, p) if M[r][c] % p)
        M[c], M[r] = M[r], M[c]
        iv = pow(M[c][c], -1, p)
        M[c] = [(x * iv) % p for x in M[c]]
        for r in range(p):
            if r != c and M[r][c] % p:
                f = M[r][c]
                M[r] = [(x - f * y) % p for x, y in zip(M[r], M[c])]
    coef = [M[i][p] for i in range(p)]
    deg = max([k for k in range(p) if coef[k]], default=-1)
    return deg, coef

def run(name, p, rng):
    G = Grp(name, p)
    cls = int(G.grades.max())
    g1 = [i for i in range(G.m) if G.grades[i] == 1]
    g2 = [i for i in range(G.m) if G.grades[i] == 2]
    N2 = layer_positions(G, 2)          # gamma_2 (= L2 + L3 here)
    Ztop = layer_positions(G, cls)      # top grade, central
    res = {"alg": name, "p": p, "order": G.n}
    A = dict(H=0, cases=0, eigen=0, pred_mismatch=0, phase_poly_bad=0, phase_dep_a=0,
             max_phase_deg=-1)
    B = dict(H=0, cases=0, eigen=0, pred_mismatch=0, disjoint_when_not_eigen=0)
    examples = {}
    both = dict(H_A_fails_some_u=0, H_B_fails=0, H_both=0, min_A_eigen_frac_on_both=1.0)
    for eta in lines(G):
        a_eig = a_tot = 0; b_fail = False
        v1 = eta.copy(); v1[[i for i in range(G.m) if G.grades[i] != 1]] = 0
        v2 = eta.copy(); v2[[i for i in range(G.m) if not (1 < G.grades[i] < cls)]] = 0  # non-central middle grades
        hidx = int(G.enc(eta))
        a_list = [int(rng.integers(G.n)) for _ in range(2)]
        # ---------- (A) ISS template: N = gamma_2, act by h -------------
        if v1.any():
            A["H"] += 1
            adv = [G.bracket1(v1, np.eye(G.m, dtype=np.int64)[j]) for j in g2]  # [v1, x_j], x_j in L2
            for u in itertools.product(range(p), repeat=len(N2)):
                u = np.array(u)
                ufull = np.zeros(G.m, dtype=np.int64); ufull[N2] = u
                beta = [int(ufull @ w % p) for w in adv]
                pred = all(b == 0 for b in beta)
                eig = []
                for a in a_list:
                    S, E = state(G, a, eta, N2, u)
                    c, _ = right_mult_ratio(G, S, E, hidx)
                    eig.append(c is not None)
                assert eig[0] == eig[1]
                A["cases"] += 1; A["eigen"] += eig[0]; a_tot += 1; a_eig += eig[0]
                if eig[0] != pred: A["pred_mismatch"] += 1
                if eig[0]:
                    cs = []
                    for a in a_list:
                        S, E = state(G, a, eta, N2, u)
                        row = []
                        for s in range(p):
                            c, _ = right_mult_ratio(G, S, E, int(G.enc(G.dil(eta, s))))
                            row.append(c)
                        cs.append(row)
                    if cs[0] != cs[1]: A["phase_dep_a"] += 1
                    if any(c is None for c in cs[0]) or cs[0][0] != 0:
                        A["phase_poly_bad"] += 1
                    else:
                        deg, _ = poly_degree_mod_p(cs[0], p)
                        A["max_phase_deg"] = max(A["max_phase_deg"], deg)
                        if deg > cls: A["phase_poly_bad"] += 1
                elif "A_shift" not in examples and len(g2) and v2.any():
                    examples["A_shift"] = dict(eta=eta.tolist(), u=u.tolist(), beta=beta)
        # ---------- (B) IS central descent on top grade Z: act by delta_s(h) ----
        if any(eta[i] for i in range(G.m) if G.grades[i] < cls):
            B["H"] += 1
            pred = (not v1.any()) or (not v2.any())
            for lam in itertools.product(range(p), repeat=len(Ztop)):
                lam = np.array(lam)
                a = a_list[0]
                S, E = state(G, a, eta, Ztop, lam)
                for s in range(2, p):
                    c, inter = right_mult_ratio(G, S, E, int(G.enc(G.dil(eta, s))))
                    B["cases"] += 1
                    eig = c is not None
                    B["eigen"] += eig
                    if eig != pred: B["pred_mismatch"] += 1
                    if not eig and inter == 0: B["disjoint_when_not_eigen"] += 1
                    if not eig: b_fail = True
                    if not eig and "B_move" not in examples:
                        examples["B_move"] = dict(eta=eta.tolist(), lam=lam.tolist(), s=s,
                                                  support_overlap=int(inter), support=int(len(S)))
        if a_tot and a_eig < a_tot: both["H_A_fails_some_u"] += 1
        if b_fail: both["H_B_fails"] += 1
        if b_fail and a_tot and a_eig < a_tot:
            both["H_both"] += 1
            both["min_A_eigen_frac_on_both"] = min(both["min_A_eigen_frac_on_both"], a_eig / a_tot)
    res["both_routes"] = both
    res["A_iss_gamma2"] = A; res["B_is_centre"] = B; res["examples"] = examples
    return res

if __name__ == "__main__":
    rng = np.random.default_rng(20261112)
    cfg = [("heis3", 5), ("heis3", 7), ("filiform4", 5), ("filiform4", 7), ("free23", 5)]
    if len(sys.argv) > 1:
        cfg = [(sys.argv[1], int(sys.argv[2]))]
    for name, p in cfg:
        r = run(name, p, rng)
        print(json.dumps(r), flush=True)
