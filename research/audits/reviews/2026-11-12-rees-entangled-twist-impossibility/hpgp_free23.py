"""Exit (ii) of the impossibility note, free23: how much information about the hidden line does ONE
label-carrying copy phi_lam(a) on G/gamma_3 = heis_3 carry?  (Finite computation; can only falsify.)

Setting (adaptive-twist note, Prop C(c)): G = free class-3 Lazard group on x,y with basis
x,y,z=[x,y],u=[x,z],w=[y,z] (u,w span gamma_3), BCH group law over F_p.  H = <exp eta>, eta=(e1,e2,e3,eu,ew),
(e1,e2) != 0 ("hard").  After the gamma_3-label lam is measured (and known), one copy is
    phi_lam(a) = p^{-1/2} sum_t  w^{-lam . C_a(t)} | pi(a exp(t eta)) >   on  C[G/gamma_3] = C[F_p^3],
where a exp(t eta) = exp(Q_a(t)+C_a(t)), pi = reduction mod gamma_3 (first three exp coordinates).
The base point a (unknown to the algorithm, uniform) and the central part of eta are nuisance.

Computed, exactly, for each lam:
  * rho_h = average of |phi><phi| over the nuisance, for hypotheses h:
      HYP1: h = line (e1:e2) of V/D          (p+1 hypotheses; the "line of v_1")
      HYP2: h = line <(e1,e2,e3)> of V       (p^2+p hypotheses; the hard cyclic K/gamma_3)
    nuisance: HYP1 (e3,eu,ew,a) in F_p^6; HYP2 (eu,ew,a) in F_p^5.  Control: HYP1 with a fixed to 0.
  * Holevo chi = S(avg_h rho_h) - avg_h S(rho_h) in bits: an upper bound on the mutual information of
    ANY measurement on one copy (hypotheses uniform).
  * MI of one concrete measurement: abelian Fourier sampling on F_p^3 in the exp chart (outcome k).
  * for comparison log2 of the number of hypotheses.
usage: python hpgp_free23.py p [p ...]"""
import sys, itertools, time, numpy as np
sys.path.insert(0, '../2026-11-12-rees-direct-twist-class3-referee')
from lie import tensor
FREE = (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}})

def bchv(X, Y, C, p):
    inv2 = pow(2, -1, p); inv12 = pow(12, -1, p)
    XY = np.einsum('ni,nj,ijk->nk', X, Y, C) % p
    Z = X + Y + inv2 * XY
    Z = Z + inv12 * (np.einsum('ni,nj,ijk->nk', X, XY, C) - np.einsum('ni,nj,ijk->nk', Y, XY, C))
    return Z % p

def entropy_bits(ev):
    ev = ev[ev > 1e-12]
    return float(-(ev * np.log2(ev)).sum())

def rho_for(eta_rows, a_rows, lam, C, p):
    """average of |phi><phi| over the given (eta, a) pairs (rows aligned)"""
    N = len(eta_rows); D = p ** 3
    om = np.exp(-2j * np.pi / p)
    pw = p ** np.arange(2, -1, -1)
    idx = np.empty((N, p), dtype=np.int64); amp = np.empty((N, p), dtype=complex)
    A = np.zeros((N, 5), dtype=np.int64); A[:, :3] = a_rows
    for t in range(p):
        g = bchv(A, (t * eta_rows) % p, C, p)
        idx[:, t] = g[:, :3] @ pw
        amp[:, t] = om ** ((lam[0] * g[:, 3] + lam[1] * g[:, 4]) % p) / np.sqrt(p)
    rho = np.zeros(D * D, dtype=complex)
    for t in range(p):
        for s in range(p):
            fl = idx[:, t] * D + idx[:, s]
            w = amp[:, t] * np.conj(amp[:, s])
            rho += np.bincount(fl, weights=w.real, minlength=D * D) + 1j * np.bincount(fl, weights=w.imag, minlength=D * D)
    return (rho / N).reshape(D, D)

def run(p, lam, family, a_fixed=False, check=False, ecz=0):
    """ecz=1: central part (eu,ew) of eta fixed to 0 (known); ecz=2: also e3 fixed to 0 (HYP1 only)"""
    C = np.array(tensor(*FREE, p))
    F1 = [(0, 1)] + [(1, s) for s in range(p)]
    if family == 1:
        hyps = [(e1, e2, None) for (e1, e2) in F1]
    else:
        hyps = [(e1, e2, e3) for (e1, e2) in F1 for e3 in range(p)]
        # line <(e1,e2,e3)> of V: reps with (e1,e2) normalised, e3 free; excludes D itself (e1=e2=0)
    avals = [(0, 0, 0)] if a_fixed else list(itertools.product(range(p), repeat=3))
    rhos, ents = [], []
    for (e1, e2, e3) in hyps:
        rows = []
        if e3 is None:
            efs = list(itertools.product(range(p), repeat=3))
            if ecz == 1: efs = [e for e in efs if e[1] == 0 and e[2] == 0]
            if ecz == 2: efs = [(0, 0, 0)]
        else:
            efs = list(itertools.product(range(p), repeat=2))
            if ecz >= 1: efs = [(0, 0)]
        for ef in efs:
            eta = (e1, e2, ef[0], ef[1], ef[2]) if e3 is None else (e1, e2, e3, ef[0], ef[1])
            for a in avals: rows.append(eta + a)
        R = np.array(rows, dtype=np.int64)
        rho = rho_for(R[:, :5], R[:, 5:], lam, C, p)
        ev = np.linalg.eigvalsh(rho)
        if check:
            assert abs(np.trace(rho) - 1) < 1e-9
        rhos.append(rho); ents.append(entropy_bits(ev))
    rbar = sum(rhos) / len(rhos)
    chi = entropy_bits(np.linalg.eigvalsh(rbar)) - float(np.mean(ents))
    # concrete measurement: Fourier sampling on F_p^3 (exp chart)
    d1 = np.exp(2j * np.pi * np.outer(range(p), range(p)) / p) / np.sqrt(p)
    F = np.kron(np.kron(d1, d1), d1)
    P = np.array([np.real(np.einsum('ij,jk,ik->i', F, r, np.conj(F))) for r in rhos])
    P = np.clip(P, 0, None); P /= P.sum(axis=1, keepdims=True)
    pk = P.mean(axis=0)
    H = lambda q: float(-(q[q > 1e-15] * np.log2(q[q > 1e-15])).sum())
    mi = H(pk) - float(np.mean([H(q) for q in P]))
    return len(hyps), chi, mi, float(np.mean(ents)), np.log2(len(hyps))

if __name__ == '__main__':
    for p in map(int, sys.argv[1:]):
        t0 = time.time()
        print('p=%d  (rank of rho_h at most p^3=%d)' % (p, p ** 3), flush=True)
        for lam in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            for fam, af, ecz, name in [(1, False, 0, 'HYP1 line(e1:e2)'), (1, True, 0, 'HYP1, a fixed (control)'), (2, False, 0, 'HYP2 line K/g3'),
                                       (1, False, 1, 'HYP1, eta_c=0 known'), (1, False, 2, 'HYP1, eta_c=e3=0 known'), (2, False, 1, 'HYP2, eta_c=0 known')]:
                if fam == 2 and lam in [(0, 1), (1, 1)] and p > 5:
                    continue
                if lam in [(0, 1), (1, 1)] and p > 5:
                    continue   # time cap: GL_2-symmetry makes nonzero lam equivalent; one nonzero lam suffices for p=7
                nh, chi, mi, Hh, lg = run(p, lam, fam, af, check=(lam == (1, 0)), ecz=ecz)
                print('  lam=%s %-28s #hyp=%3d  log2#hyp=%.3f  Holevo chi=%.4f bits  MI(Fourier chart)=%.4f bits  mean S(rho_h)=%.3f  [%.0fs]'
                      % (lam, name, nh, lg, chi, mi, Hh, time.time() - t0), flush=True)
