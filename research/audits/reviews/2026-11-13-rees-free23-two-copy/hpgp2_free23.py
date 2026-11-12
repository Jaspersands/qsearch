"""Exit (ii) of the 2026-11-12 impossibility note, free23: TWO label-carrying copies with SHARED hidden eta.
(Exact finite computation up to float round-off; it can only falsify.  AI-written, pending human review.)

Setting (as in ../2026-11-12-rees-entangled-twist-impossibility/hpgp_free23.py): G = free class-3 Lazard
group on x,y, basis x,y,z=[x,y],u=[x,z],w=[y,z]; H = <exp eta>, eta=(e1,e2,e3,eu,ew), (e1,e2) != 0.
One copy with gamma_3-label lam, base point a (uniform, unknown) is
    phi_lam(a) = p^{-1/2} sum_t  w^{-lam . C_a(t)} | pi(a exp(t eta)) >   on C[G/gamma_3] = C[F_p^3].
sigma_{eta,lam} := E_a |phi><phi|   (p^3 x p^3).   Two copies, same H, independent a_1, a_2:
    rho_h(lam1,lam2) = E_{eta | h}  sigma_{eta,lam1} (x) sigma_{eta,lam2}        (p^6 x p^6).
Hypotheses: HYP1 = line (e1:e2) of V/D (nuisance e3,eu,ew);  HYP2 = line <(e1,e2,e3)> = K/gamma_3 (nuisance eu,ew).

METHOD (exact; no p^6 x p^6 matrix is ever formed).
  * sigma_{eta,lam} commutes with U_lam(g), the left-regular action of G on the lam-sector written in the
    exp-chart section:  U_lam(g)|q> = e^{-2 pi i lam.c'/p} |q'>,  g exp(q) = exp(q' + c'), c' in gamma_3.
    (Checked numerically below: max ||[sigma, U(g)]||.)
  * A_lam = <g0, z> with lam([g0,z]) = 0 is abelian in U_lam.  Its joint eigenprojectors P_jk (exact
    character sums) give an orthonormal basis W_lam in which every sigma_{eta,lam} is block diagonal with
    p^2 blocks of size p (checked: off-block norm).
  * Hence rho_h, and the hypothesis average, are block diagonal in W_lam1 (x) W_lam2 with p^4 blocks of
    size p^2:  block(b1,b2) = E_eta  B1_eta[b1] (x) B2_eta[b2].
  * U(x') (x' outside A) permutes the blocks of one copy and commutes with every sigma, so blocks in one
    U(x')-orbit are unitarily equivalent by an h-INDEPENDENT unitary.  mode 'rep' keeps one block per
    (orbit1, orbit2) class with its weight; mode 'full' keeps all blocks (used at p = 5 to check 'rep').
  * S(rho) = sum over kept blocks of weight * (-sum ev log2 ev).  Holevo chi = S(avg_h rho_h) - avg_h S(rho_h).

VALIDATION (see main): single-copy block method vs dense method vs hpgp_free23.out; two-copy moments
tr(rho_h rho_h') from dense sigma's (no block basis) vs block representation; analytic predictions.

usage:  python hpgp2_free23.py validate p           single-copy + moment checks
        python hpgp2_free23.py table p mode [all]   two-copy chi_2 table (mode rep|full)
"""
import sys, os, itertools, time, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-12-rees-direct-twist-class3-referee'))
from lie import tensor
FREE = (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}})


def bchv(X, Y, C, p):
    inv2 = pow(2, -1, p); inv12 = pow(12, -1, p)
    XY = np.einsum('ni,nj,ijk->nk', X, Y, C) % p
    Z = X + Y + inv2 * XY
    Z = Z + inv12 * (np.einsum('ni,nj,ijk->nk', X, XY, C) - np.einsum('ni,nj,ijk->nk', Y, XY, C))
    return Z % p


def ent(ev):
    ev = np.asarray(ev).ravel(); ev = ev[ev > 1e-13]
    return float(-(ev * np.log2(ev)).sum())


class Free23:
    def __init__(self, p):
        self.p = p; self.C = np.array(tensor(*FREE, p)); self.D = p ** 3
        self.pw = p ** np.arange(2, -1, -1)
        self.Q = np.array(list(itertools.product(range(p), repeat=3)), dtype=np.int64)   # index = q @ pw
        self.F1 = [(0, 1)] + [(1, s) for s in range(p)]

    def Phi(self, eta, lam, a_rows=None):
        """columns phi_lam(a) for a in a_rows (default: all of F_p^3)"""
        p, D = self.p, self.D
        a_rows = self.Q if a_rows is None else np.asarray(a_rows, dtype=np.int64)
        N = len(a_rows); A = np.zeros((N, 5), dtype=np.int64); A[:, :3] = a_rows
        E = np.tile(np.array(eta, dtype=np.int64), (N, 1))
        M = np.zeros((D, N), dtype=complex); cols = np.arange(N)
        for t in range(p):
            g = bchv(A, (t * E) % p, self.C, p)
            ph = np.exp(-2j * np.pi * ((lam[0] * g[:, 3] + lam[1] * g[:, 4]) % p) / p) / np.sqrt(p)
            np.add.at(M, (g[:, :3] @ self.pw, cols), ph)
        return M

    def sigma(self, eta, lam, a_rows=None):
        M = self.Phi(eta, lam, a_rows); return M @ M.conj().T / M.shape[1]

    def U(self, gvec, lam):
        p, D = self.p, self.D
        X = np.tile(np.array(list(gvec) + [0] * (5 - len(gvec)), dtype=np.int64), (D, 1))
        Y = np.zeros((D, 5), dtype=np.int64); Y[:, :3] = self.Q
        r = bchv(X, Y, self.C, p)
        M = np.zeros((D, D), dtype=complex)
        M[r[:, :3] @ self.pw, np.arange(D)] = np.exp(-2j * np.pi * ((lam[0] * r[:, 3] + lam[1] * r[:, 4]) % p) / p)
        return M

    def basis(self, lam):
        """W (D x D unitary), list of p^2 blocks (column slices), orbit reps with weights, and checks"""
        p, D = self.p, self.D
        if tuple(lam) == (0, 0):
            g0, xp = (0, 1, 0), (1, 0, 0)
        else:
            g0 = (lam[1] % p, (-lam[0]) % p, 0)          # lam([g0,z]) = lam_u*lam_w - lam_w*lam_u = 0
            xp = (0, 1, 0) if g0[1] == 0 else (1, 0, 0)  # x' not in span(g0) + D
        U0, Uz, Ux = self.U(g0, lam), self.U((0, 0, 1), lam), self.U(xp, lam)
        comm = np.abs(U0 @ Uz - Uz @ U0).max()
        om = np.exp(2j * np.pi / p)
        P0 = [np.linalg.matrix_power(U0, m) for m in range(p)]
        Pz = [np.linalg.matrix_power(Uz, n) for n in range(p)]
        cols, blocks = [], []
        for j in range(p):
            for k in range(p):
                P = sum(om ** (-(j * m + k * n)) * (P0[m] @ Pz[n]) for m in range(p) for n in range(p)) / p ** 2
                ev, V = np.linalg.eigh((P + P.conj().T) / 2)
                V = V[:, ev > 0.5]
                assert V.shape[1] == p, (lam, j, k, V.shape)
                blocks.append(slice(len(cols) * p, (len(cols) + 1) * p)); cols.append(V)
        W = np.hstack(cols)
        unit = np.abs(W.conj().T @ W - np.eye(D)).max()
        # orbits of blocks under U(x')
        nb = p * p; perm = np.empty(nb, dtype=int)
        Y = W.conj().T @ Ux @ W
        for b in range(nb):
            nrm = [np.linalg.norm(Y[blocks[c], blocks[b]]) for c in range(nb)]
            perm[b] = int(np.argmax(nrm)); assert abs(nrm[perm[b]] ** 2 - p) < 1e-6
        seen, reps = set(), []
        for b in range(nb):
            if b in seen: continue
            orb, c = [], b
            while c not in orb: orb.append(c); c = perm[c]
            seen.update(orb); reps.append((b, len(orb)))
        return dict(W=W, blocks=blocks, reps=reps, Ux=Ux, U0=U0, Uz=Uz, comm=comm, unit=unit, g0=g0, xp=xp)

    def blocks_of(self, B, sig):
        Y = B['W'].conj().T @ sig @ B['W']
        blk = np.array([Y[s, s] for s in B['blocks']])
        for s in B['blocks']: Y[s, s] = 0
        return blk, float(np.abs(Y).max())          # max off-block entry


def etas(p, F1):
    for (e1, e2) in F1:
        for e3 in range(p):
            for eu in range(p):
                for ew in range(p):
                    yield (e1, e2), e3, (eu, ew), (e1, e2, e3, eu, ew)


# ---------------------------------------------------------------- single copy (validation)
def single(G, lam, mode='block', B=None):
    """returns dict of chi / mean S for HYP1, HYP2, HYP1 eta_c=0 known, HYP1 eta_c=e3=0 known, HYP2 eta_c=0 known,
    and (dense only) HYP1 a fixed."""
    p = G.p; F1 = G.F1; out = {}
    if mode == 'block':
        B = B or G.basis(lam)
        acc = {}; acc0 = {}
        for l, e3, ec, eta in etas(p, F1):
            blk, _ = G.blocks_of(B, G.sigma(eta, lam))
            acc[(l, e3)] = acc.get((l, e3), 0) + blk / p ** 2
            if ec == (0, 0): acc0[(l, e3)] = blk
        reps = B['reps']
        S = lambda blk: sum(w * ent(np.linalg.eigvalsh(blk[b])) for b, w in reps)
    else:
        acc = {}; acc0 = {}
        for l, e3, ec, eta in etas(p, F1):
            s = G.sigma(eta, lam)
            acc[(l, e3)] = acc.get((l, e3), 0) + s / p ** 2
            if ec == (0, 0): acc0[(l, e3)] = s
        S = lambda r: ent(np.linalg.eigvalsh(r))
    def chi(states):
        rb = sum(states) / len(states); Ss = [S(r) for r in states]
        return S(rb) - float(np.mean(Ss)), float(np.mean(Ss))
    h2 = list(acc.values()); h1 = [sum(acc[(l, e3)] for e3 in range(p)) / p for l in F1]
    out['HYP1'] = chi(h1); out['HYP2'] = chi(h2)
    out['HYP1 eta_c=0 known'] = chi([sum(acc0[(l, e3)] for e3 in range(p)) / p for l in F1])
    out['HYP1 eta_c=e3=0 known'] = chi([acc0[(l, 0)] for l in F1])
    out['HYP2 eta_c=0 known'] = chi(list(acc0.values()))
    if mode == 'dense':
        st = []
        for l in F1:
            st.append(sum(G.sigma((l[0], l[1], e3, eu, ew), lam, a_rows=[(0, 0, 0)])
                          for e3 in range(p) for eu in range(p) for ew in range(p)) / p ** 3)
        out['HYP1 a fixed'] = chi(st)
    return out


# ---------------------------------------------------------------- two copies
_CACHE = {}
def eta_blocks(G, lam, B):
    """all p^2 diagonal blocks of sigma_{eta,lam} in W_lam, for every eta in etas() order; cached"""
    key = (G.p, tuple(lam))
    if key not in _CACHE:
        while len(_CACHE) >= 2: _CACHE.pop(next(iter(_CACHE)))      # memory cap: keep at most 2 labels
        out, off = [], 0.0
        for _, _, _, eta in etas(G.p, G.F1):
            b, o = G.blocks_of(B, G.sigma(eta, lam)); out.append(b); off = max(off, o)
        _CACHE[key] = (np.array(out), off)
    return _CACHE[key]


def two(G, lam1, lam2, mode='rep', B1=None, B2=None, keep=False):
    p = G.p; F1 = G.F1
    B1 = B1 or G.basis(lam1); B2 = B2 or G.basis(lam2)
    E1, o1 = eta_blocks(G, lam1, B1); E2, o2 = eta_blocks(G, lam2, B2)
    if mode == 'full':
        cls = [(b1, b2, 1) for b1 in range(p * p) for b2 in range(p * p)]
    else:
        cls = [(b1, b2, w1 * w2) for b1, w1 in B1['reps'] for b2, w2 in B2['reps']]
    i1 = np.array([c[0] for c in cls]); i2 = np.array([c[1] for c in cls]); wt = np.array([c[2] for c in cls], float)
    n = len(cls); d = p * p
    nh = len(F1) * p
    acc = np.zeros((nh, n, d, d), dtype=complex); acc0 = np.zeros((nh, n, d, d), dtype=complex)
    offmax = max(o1, o2)
    for ie, (l, e3, ec, eta) in enumerate(etas(p, F1)):
        h = F1.index(l) * p + e3
        b1, b2 = E1[ie], E2[ie]
        K = np.einsum('nij,nkl->nikjl', b1[i1], b2[i2]).reshape(n, d, d)
        acc[h] += K / p ** 2
        if ec == (0, 0): acc0[h] = K

    def S(st):
        ev = np.linalg.eigvalsh(st)            # (n, d)
        ev = np.where(ev > 1e-13, ev, 1.0)
        return float((wt[:, None] * (-ev * np.log2(ev))).sum())

    def chi(states):
        Ss = [S(r) for r in states]; rb = sum(states) / len(states)
        return S(rb) - float(np.mean(Ss)), float(np.mean(Ss))
    tr = [float(np.real((wt[:, None] * np.einsum('nii->ni', acc[h])).sum())) for h in range(nh)]
    h1 = [acc[k * p:(k + 1) * p].mean(axis=0) for k in range(len(F1))]
    res = {'HYP1': chi(h1), 'HYP2': chi(list(acc)),
           'HYP1 eta_c=0 known': chi([acc0[k * p:(k + 1) * p].mean(axis=0) for k in range(len(F1))]),
           'HYP2 eta_c=0 known': chi(list(acc0)),
           'trace_err': max(abs(t - 1) for t in tr), 'offblock': offmax, 'nblocks': n}
    if keep: res['acc'] = acc; res['wt'] = wt
    return res


def wspec(blocks, wt):
    """full weighted spectrum (sorted) of a block-diagonal state given representative blocks and integer weights"""
    ev = np.linalg.eigvalsh(blocks)
    return np.sort(np.repeat(ev.ravel(), np.repeat(wt.astype(int), ev.shape[1])))


def single_known_states(G, lam):
    """single copy, eta_c = 0 known: HYP2 states (blocks of reps) and weights"""
    p = G.p; B = G.basis(lam); idx = np.array([b for b, _ in B['reps']]); wt = np.array([w for _, w in B['reps']], float)
    st = []
    for l, e3, ec, eta in etas(p, G.F1):
        if ec == (0, 0): st.append(G.blocks_of(B, G.sigma(eta, lam))[0][idx])
    return np.array(st), wt


def compare(G, l1, l2, lref):
    """spectra of rho_h, HYP1 states and avg state of the two-copy ensemble vs (single-copy eta_c-known ensemble for
    label lref) (x) I/p^3 (lref = (1,0) for c != -1;  lref=(0,0) with full eta averaging is the same as known for lam=0)"""
    p = G.p
    r = two(G, l1, l2, 'rep', keep=True); acc, wt = r['acc'], r['wt']
    s1, w1 = single_known_states(G, lref)
    tail = np.full(p ** 3, p ** -3.0)
    def tens(sp): return np.sort(np.outer(sp, tail).ravel())
    dif = {}
    dif['avg'] = np.abs(wspec(acc.mean(axis=0), wt) - tens(wspec(s1.mean(axis=0), w1))).max()
    dif['HYP2 states'] = max(np.abs(wspec(acc[h], wt) - tens(wspec(s1[h], w1))).max() for h in range(len(acc)))
    dif['HYP1 states'] = max(np.abs(wspec(acc[k * p:(k + 1) * p].mean(axis=0), wt) - tens(wspec(s1[k * p:(k + 1) * p].mean(axis=0), w1))).max()
                             for k in range(len(G.F1)))
    return r, dif


def multi(G, lams):
    """k copies (k = len(lams)), shared eta, independent base points; representative blocks only; streams over
    hypotheses so memory is O(#classes * p^{2k}).  Returns chi and mean S for HYP1 and HYP2."""
    p = G.p; k = len(lams); Bs = [G.basis(l) for l in lams]
    reps = [B['reps'] for B in Bs]
    cls = list(itertools.product(*reps))
    idx = [np.array([c[i][0] for c in cls]) for i in range(k)]
    wt = np.array([np.prod([c[i][1] for i in range(k)]) for c in cls], float)
    n = len(cls); d = p ** k
    def S(st):
        ev = np.linalg.eigvalsh(st); ev = np.where(ev > 1e-13, ev, 1.0)
        return float((wt[:, None] * (-ev * np.log2(ev))).sum())
    tot = np.zeros((n, d, d), complex); S2, S1, cur, h1 = [], [], None, None
    letters = 'abcdefgh'
    sub = ','.join('n' + letters[2 * i] + letters[2 * i + 1] for i in range(k))
    outs = 'n' + ''.join(letters[2 * i] for i in range(k)) + ''.join(letters[2 * i + 1] for i in range(k))
    last = None
    for l, e3, ec, eta in etas(p, G.F1):
        if (l, e3) != last:
            if cur is not None:
                S2.append(S(cur)); tot += cur; h1 = cur if h1 is None else h1 + cur
                if last[1] == p - 1: S1.append(S(h1 / p)); h1 = None
            cur = np.zeros((n, d, d), complex); last = (l, e3)
        bl = [G.blocks_of(B, G.sigma(eta, lm))[0] for B, lm in zip(Bs, lams)]
        cur += np.einsum(sub + '->' + outs, *[bl[i][idx[i]] for i in range(k)]).reshape(n, d, d) / p ** 2
    S2.append(S(cur)); tot += cur; h1 = h1 + cur; S1.append(S(h1 / p))
    Sbar = S(tot / (len(G.F1) * p))
    return {'HYP1': (Sbar - np.mean(S1), np.mean(S1)), 'HYP2': (Sbar - np.mean(S2), np.mean(S2)), 'Sbar': Sbar}


def words(G, c, nsample=3000, seed=1):
    """trace words of length 3 (all) and 4 (sampled) in the HYP2 and HYP1 states: two-copy (lam, c lam) vs
    [single copy eta_c known, lam] (x) I/p^3 (for c = -1: single lam = 0).  Equal words support (do not prove)
    a hypothesis-independent unitary equivalence of the two ensembles."""
    p = G.p
    r = two(G, (1, 0), (c, 0), 'rep', keep=True); A, wa = r['acc'], r['wt']
    s1, w1 = single_known_states(G, (0, 0) if c == p - 1 else (1, 0))
    def fam(X, nh1):
        return list(X) + [X[k * p:(k + 1) * p].mean(axis=0) for k in range(nh1)]
    FA = fam(A, len(G.F1)); FS = fam(s1, len(G.F1))
    def w3(F, w, i, j, k): return float(np.real(np.einsum('n,nab,nbc,nca->', w, F[i], F[j], F[k])))
    def w4(F, w, i, j, k, l): return float(np.real(np.einsum('n,nab,nbc,ncd,nda->', w, F[i], F[j], F[k], F[l])))
    N = len(FA); m3 = 0.0
    for i, j, k in itertools.product(range(N), repeat=3):
        if i <= j and i <= k:
            m3 = max(m3, abs(w3(FA, wa, i, j, k) - w3(FS, w1, i, j, k) * p ** -6))
    rng = np.random.default_rng(seed); m4 = 0.0
    for _ in range(nsample):
        q = rng.integers(0, N, 4)
        m4 = max(m4, abs(w4(FA, wa, *q) - w4(FS, w1, *q) * p ** -9))
    return N, m3, m4


def words_rel(G, c, lref, nsample=400, seed=2):
    """sampled relative trace-word differences (length 3 and 4) between the two-copy (lam=(1,0), c lam) ensemble and
    [single copy, label lref, eta_c known] (x) I/p^3, hypotheses matched by identity (HYP2 then HYP1 states).
    Different lref = (m,0) correspond, via dilation automorphisms, to permuting e3 inside each HYP1 class."""
    p = G.p
    r = two(G, (1, 0), (c, 0), 'rep', keep=True); A, wa = r['acc'], r['wt']
    s1, w1 = single_known_states(G, lref)
    fam = lambda X: list(X) + [X[k * p:(k + 1) * p].mean(axis=0) for k in range(len(G.F1))]
    FA, FS = fam(A), fam(s1); N = len(FA); rng = np.random.default_rng(seed); out = []
    for L in (3, 4):
        worst = 0.0
        for _ in range(nsample):
            q = rng.integers(0, N, L)
            def wd(F, w):
                M = F[q[0]]
                for i in q[1:]: M = np.einsum('nab,nbc->nac', M, F[i])
                return float(np.real(np.einsum('n,naa->', w, M)))
            a, b = wd(FA, wa), wd(FS, w1) * p ** (-3 * (L - 1))
            worst = max(worst, abs(a - b) / abs(a))
        out.append(worst)
    return out


def moment_check(G, lam1, lam2, res):
    """tr(rho_h rho_h') for HYP2 from dense sigma's (no block basis) vs the block representation"""
    p = G.p; F1 = G.F1; nh = len(F1) * p
    V1 = np.zeros((nh, p * p, G.D * G.D), dtype=complex); V2 = np.zeros_like(V1)
    cnt = np.zeros(nh, int)
    for l, e3, ec, eta in etas(p, F1):
        h = F1.index(l) * p + e3
        V1[h, cnt[h]] = G.sigma(eta, lam1).ravel(); V2[h, cnt[h]] = G.sigma(eta, lam2).ravel(); cnt[h] += 1
    A1 = V1.reshape(-1, G.D * G.D); A2 = V2.reshape(-1, G.D * G.D)
    G1 = A1 @ A1.conj().T; G2 = A2 @ A2.conj().T          # tr(s s') = <vec s', vec s> for Hermitian s
    M = (G1 * G2).reshape(nh, p * p, nh, p * p).mean(axis=(1, 3)).real
    acc, wt = res['acc'], res['wt']
    X = (acc * np.sqrt(wt)[None, :, None, None]).reshape(nh, -1)
    Mb = np.real(X @ X.conj().T)                           # blocks are Hermitian
    return M, Mb


def lam_list(p):
    return [(a, b) for a in range(p) for b in range(p)]


def classify(p, l1, l2):
    z1 = l1 == (0, 0); z2 = l2 == (0, 0)
    if z1 and z2: return 'both zero'
    if z1 or z2: return 'one zero'
    det = (l1[0] * l2[1] - l1[1] * l2[0]) % p
    if det: return 'independent'
    c = next(c for c in range(1, p) if ((c * l1[0] - l2[0]) % p, (c * l1[1] - l2[1]) % p) == (0, 0))
    return 'c=%d%s' % (c, ' (=-1, binary zero-sum)' if c == p - 1 else '')


if __name__ == '__main__':
    cmd, p = sys.argv[1], int(sys.argv[2])
    G = Free23(p); t0 = time.time()
    if cmd == 'validate':
        print('p=%d  single-copy validation: block method vs dense method (compare hpgp_free23.out)' % p, flush=True)
        for lam in [(0, 0), (1, 0), (0, 1), (1, 1), (2, 3)]:
            B = G.basis(lam)
            sig = G.sigma((1, 2, 3, 4, 1), lam)
            cm = max(np.abs(sig @ U - U @ sig).max() for U in (B['U0'], B['Uz'], B['Ux']))
            _, off = G.blocks_of(B, sig)
            print('  lam=%s basis: [U0,Uz]=%.1e  W unitary err=%.1e  [sigma,U] max=%.1e  off-block=%.1e  orbit sizes=%s'
                  % (lam, B['comm'], B['unit'], cm, off, sorted(w for _, w in B['reps'])), flush=True)
            rb = single(G, lam, 'block', B)
            rd = single(G, lam, 'dense') if (p == 5 or lam in [(0, 0), (1, 0)]) else None
            for k in rb:
                print('    %-24s block chi=%.4f meanS=%.3f' % (k, rb[k][0], rb[k][1])
                      + ('   dense chi=%.4f meanS=%.3f  |diff|=%.1e' % (rd[k][0], rd[k][1], abs(rd[k][0] - rb[k][0])) if rd else ''), flush=True)
            if rd:
                print('    %-24s                              dense chi=%.4f meanS=%.3f' % ('HYP1 a fixed (control)', *rd['HYP1 a fixed']), flush=True)
            print('    [%.0fs]' % (time.time() - t0), flush=True)
        print('p=%d  two-copy checks: rep vs full blocks, moments tr(rho_h rho_h\') dense-vs-block, analytic values' % p, flush=True)
        for l1, l2 in [((1, 0), (2, 0)), ((1, 0), (4 % p, 0)), ((1, 0), (0, 1)), ((1, 0), (0, 0)), ((0, 0), (0, 0)), ((1, 1), (3, 3)), ((2, 3), (1, 4))]:
            rr = two(G, l1, l2, 'rep')
            line = '  %s,%s [%s]: rep HYP1 chi=%.4f HYP2 chi=%.4f meanS2=%.4f' % (l1, l2, classify(p, l1, l2), rr['HYP1'][0], rr['HYP2'][0], rr['HYP2'][1])
            if p == 5:
                rf = two(G, l1, l2, 'full', keep=True)
                M, Mb = moment_check(G, l1, l2, rf)
                line += ' | full HYP1 chi=%.4f HYP2 chi=%.4f  |rep-full|=%.1e  moments max|dense-block|=%.1e  diag tr(rho^2)*p^5 in [%.4f,%.4f] offdiag*p^6 in [%.4f,%.4f]' % (
                    rf['HYP1'][0], rf['HYP2'][0], max(abs(rf[k][0] - rr[k][0]) + abs(rf[k][1] - rr[k][1]) for k in ('HYP1', 'HYP2')),
                    np.abs(M - Mb).max(), (np.diag(M) * p ** 5).min(), (np.diag(M) * p ** 5).max(),
                    (M[~np.eye(len(M), dtype=bool)] * p ** 6).min(), (M[~np.eye(len(M), dtype=bool)] * p ** 6).max())
            print(line + '  trace_err=%.1e offblock=%.1e [%.0fs]' % (rr['trace_err'], rr['offblock'], time.time() - t0), flush=True)
    elif cmd == 'compare':
        print('p=%d: is the two-copy ensemble (lam, c lam) spectrally identical to [single copy, eta_c known] (x) I/p^3 ?' % p, flush=True)
        for c in range(1, p):
            lref = (0, 0) if c == p - 1 else (1, 0)
            r, dif = compare(G, (1, 0), (c, 0), lref)
            print('  c=%d  ref=single lam=%s eta_c known: chi2 HYP1=%.10f HYP2=%.10f  max|spec diff| avg=%.1e HYP1=%.1e HYP2=%.1e [%.0fs]'
                  % (c, lref, r['HYP1'][0], r['HYP2'][0], dif['avg'], dif['HYP1 states'], dif['HYP2 states'], time.time() - t0), flush=True)
        for lam in [(1, 0), (0, 0)]:
            rb = single(G, lam, 'block')
            print('  reference single lam=%s: HYP1 eta_c=0 known chi=%.10f  HYP2 eta_c=0 known chi=%.10f  (full-average HYP1 chi=%.10f HYP2 chi=%.10f)'
                  % (lam, rb['HYP1 eta_c=0 known'][0], rb['HYP2 eta_c=0 known'][0], rb['HYP1'][0], rb['HYP2'][0]), flush=True)
    elif cmd == 'words':
        print('p=%d trace-word test of a hypothesis-independent unitary equivalence (two-copy vs single eta_c-known (x) I/p^3)' % p, flush=True)
        for c in range(1, p):
            N, m3, m4 = words(G, c)
            print('  c=%d: %d states (HYP2 + HYP1); max |word diff| length 3 (all) = %.1e, length 4 (3000 sampled) = %.1e  [typical word size p^-12=%.1e] [%.0fs]'
                  % (c, N, m3, m4, p ** -12.0, time.time() - t0), flush=True)
    elif cmd == 'words2':
        print('p=%d sampled RELATIVE trace-word differences, two-copy (lam, c lam) vs single eta_c-known label (m,0) (x) I/p^3' % p, flush=True)
        for c in range(1, p - 1):
            for m in range(1, p):
                w3, w4 = words_rel(G, c, (m, 0))
                print('  c=%d m=%d: max rel diff length3=%.2e length4=%.2e [%.0fs]' % (c, m, w3, w4, time.time() - t0), flush=True)
        w3, w4 = words_rel(G, p - 1, (0, 0))
        print('  c=-1 vs lam=0 (Prop M): length3=%.2e length4=%.2e' % (w3, w4), flush=True)
    elif cmd == 'multi':
        print('p=%d k-copy Holevo chi_k (bits), shared eta; log2 #hyp: HYP1 %.3f HYP2 %.3f' % (p, np.log2(p + 1), np.log2(p * p + p)), flush=True)
        for lams in [((1, 0), (0, 1), (p - 1, p - 1)), ((1, 0), (0, 1), (1, 1)), ((1, 0), (0, 1), (1, 2)), ((1, 0), (0, 1), (2, 3))]:
            r = multi(G, lams)
            print('  lams=%s: HYP1 chi=%.4f S=%.4f | HYP2 chi=%.4f S=%.4f | S(avg)=%.4f (9 log2 p = %.4f) [%.0fs]'
                  % (lams, r['HYP1'][0], r['HYP1'][1], r['HYP2'][0], r['HYP2'][1], r['Sbar'], 9 * np.log2(p), time.time() - t0), flush=True)
    elif cmd == 'table':
        mode = sys.argv[3]; allpairs = len(sys.argv) > 4 and sys.argv[4] == 'all'
        print('p=%d two-copy Holevo chi_2 (bits), mode=%s, log2 p=%.4f; columns: class | HYP1 chi, meanS | HYP2 chi, meanS | controls eta_c=0 known: HYP1 chi, HYP2 chi'
              % (p, mode, np.log2(p)), flush=True)
        bases = {}
        def Bof(l):
            if l not in bases: bases[l] = G.basis(l)
            return bases[l]
        if allpairs:
            pairs = [(l1, l2) for l1 in lam_list(p) for l2 in lam_list(p)]
        else:   # symmetry-reduced complete set: lam1 = (1,0) and every lam2, plus lam1 = 0
            pairs = [((1, 0), l2) for l2 in lam_list(p)] + [((0, 0), (0, 0)), ((0, 0), (1, 0))]
        for l1, l2 in pairs:
            r = two(G, l1, l2, mode, Bof(l1), Bof(l2))
            print('  lam1=%s lam2=%s %-26s | HYP1 chi=%.4f S=%.4f | HYP2 chi=%.4f S=%.4f | known: %.4f %.4f | tr_err=%.0e off=%.0e [%.0fs]'
                  % (l1, l2, classify(p, l1, l2), r['HYP1'][0], r['HYP1'][1], r['HYP2'][0], r['HYP2'][1],
                     r['HYP1 eta_c=0 known'][0], r['HYP2 eta_c=0 known'][0], r['trace_err'], r['offblock'], time.time() - t0), flush=True)
