"""IS (Ivanyos-Santha) basis for one gamma_3-labelled free23 copy, in closed form.
(AI-written, pending human review; exact F_p arithmetic, float only for amplitudes.)

For a label lam != 0 the copy lives on fil4_lam = G / ker(lam).  Take g0 in V/D with lam([g0,z]) = 0 and x' with
f(x') = 1, f(g0) = 0 (f(v) = det(g0,v)/det(g0,x')).  N_lam = exp(F_p g0 + gamma_2) is normal of index p, and abelian
modulo ker(lam).  IS Prop 7 chart: g = n * s(x), s(x) = exp(x x').  IS front end: Fourier over N_lam, outcome
y = (j,k) (character  y~(nu) = j*[g0-coord of nu] + k*nu_z + lam(nu_gamma3)), then a state on the x-register.

  * f(e) != 0 (H not inside N_lam): H is a complement of N_lam, every coset has a rep in N_lam, and the block-y
    state is PURE:  psi_y(x) = w^{sgn * y~(nu(x))} / sqrt p,  nu(x) = log( exp(x eta/f(e)) exp(-x x') ),
    a cubic polynomial phase in x (BCH, class 3).  Each y has probability 1/p^2.
  * f(e) = 0 (H inside N_lam): the block-y state is diagonal, uniform on {x0 : y~(Ad_{s(x0)} eta) = 0};
    P(y, x0) = [condition] / p^2.

validate(): compares these blocks with W^dag sigma W computed from the dense V-picture sigma of
../2026-11-13-rees-free23-two-copy/hpgp2_free23.py, with W = normalized P_jk |x x'> (IS basis inside C[V]).
"""
import sys, os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '2026-11-13-rees-free23-two-copy'))
import hpgp2_free23 as H2                      # noqa: E402  (Free23, bchv, etas)
from hpgp2_free23 import bchv, etas            # noqa: E402


def det(a, b): return a[0] * b[1] - a[1] * b[0]


class Chart:
    def __init__(self, p, lam):
        self.p, self.lam = p, (lam[0] % p, lam[1] % p)
        assert self.lam != (0, 0)
        g0 = (self.lam[1], (-self.lam[0]) % p)
        xp = (0, 1) if g0[1] == 0 else (1, 0)
        self.g0, self.xp = g0, xp
        self.dinv = pow(det(g0, xp) % p, -1, p)
        self.C = H2.Free23(p).C if p not in _CC else _CC[p]
        _CC[p] = self.C

    def f(self, v): return (det(self.g0, v) * self.dinv) % self.p

    def gcoord(self, nu):                         # nu (..., >=2) with V/D part in F_p g0
        p, g0 = self.p, self.g0
        return (nu[..., 0] * pow(g0[0], -1, p)) % p if g0[0] % p else (nu[..., 1] * pow(g0[1], -1, p)) % p

    def ytilde(self, nu):                          # returns (p^2, ...) array of y~(nu) for y=(j,k), index j*p+k
        p = self.p; s = self.gcoord(nu); z = nu[..., 2] % p
        c = (self.lam[0] * nu[..., 3] + self.lam[1] * nu[..., 4]) % p
        J = np.arange(p)[:, None]; K = np.arange(p)[None, :]
        out = (J.reshape(p, 1, *([1] * s.ndim)) * s + K.reshape(1, p, *([1] * s.ndim)) * z + c) % p
        return out.reshape(p * p, *s.shape)

    def states(self, etas_arr, sgn=1):
        """etas_arr: (n,5) ints.  Returns (pure, amp, diag):
           pure (n,) bool;  amp (n, p^2, p) complex: psi_y(x) for pure rows (zeros otherwise);
           diag (n, p^2, p) float: P(y, x) for non-pure rows (zeros otherwise).  Block prob for pure rows = 1/p^2."""
        p = self.p; E = np.asarray(etas_arr, dtype=np.int64) % p; n = len(E)
        fe = (det(self.g0, (E[:, 0], E[:, 1])) * self.dinv) % p
        pure = fe != 0
        amp = np.zeros((n, p * p, p), complex); diag = np.zeros((n, p * p, p))
        xs = np.arange(p)
        XP = np.array([self.xp[0], self.xp[1], 0, 0, 0], dtype=np.int64)
        if pure.any():
            Ep = E[pure]; inv = np.array([pow(int(v), -1, p) for v in fe[pure]])
            Et = (Ep * inv[:, None]) % p                                  # eta / f(e)
            A = (xs[None, :, None] * Et[:, None, :]) % p                  # (m, p, 5)
            B = np.broadcast_to((-xs[:, None] * XP[None, :]) % p, A.shape)
            nu = bchv(A.reshape(-1, 5), B.reshape(-1, 5), self.C, p).reshape(A.shape)
            assert (self.f((nu[..., 0], nu[..., 1])) == 0).all()
            ph = self.ytilde(nu)                                          # (p^2, m, p)
            amp[pure] = np.exp(sgn * 2j * np.pi * np.moveaxis(ph, 0, 1) / p) / np.sqrt(p)
        if (~pure).any():
            En = E[~pure]; m = len(En)
            S = (xs[:, None] * XP[None, :]) % p                           # s(x0)
            A = np.broadcast_to(S[None], (m, p, 5)).reshape(-1, 5)
            Bq = np.repeat(En, p, axis=0)
            t1 = bchv(A, Bq, self.C, p); ad = bchv(t1, (-A) % p, self.C, p).reshape(m, p, 5)
            ph = self.ytilde(ad)                                          # (p^2, m, p)
            diag[~pure] = np.moveaxis((ph == 0).astype(float), 0, 1) / p ** 2
        return pure, amp, diag


_CC = {}


def all_etas(p):
    F1 = [(0, 1)] + [(1, s) for s in range(p)]
    return F1, np.array([eta for _, _, _, eta in etas(p, F1)], dtype=np.int64)


def validate(p=5, labels=((1, 0), (1, 2), (0, 1), (3, 4)), neta=40, seed=0):
    G = H2.Free23(p); rng = np.random.default_rng(seed); F1, E = all_etas(p)
    worst = {}
    for lam in labels:
        ch = Chart(p, lam)
        g0 = (ch.g0[0], ch.g0[1], 0); xp = (ch.xp[0], ch.xp[1], 0)
        U0, Uz = G.U(g0, lam), G.U((0, 0, 1), lam)
        om = np.exp(2j * np.pi / p)
        P0 = [np.linalg.matrix_power(U0, m) for m in range(p)]; Pz = [np.linalg.matrix_power(Uz, n) for n in range(p)]
        W = np.zeros((p * p, G.D, p), complex)
        for j in range(p):
            for k in range(p):
                P = sum(om ** (-(j * m + k * n)) * (P0[m] @ Pz[n]) for m in range(p) for n in range(p)) / p ** 2
                for x in range(p):
                    q = np.array([x * xp[0] % p, x * xp[1] % p, 0]) @ G.pw
                    v = P[:, q]; W[j * p + k, :, x] = v / np.linalg.norm(v)
        Wf = W.transpose(1, 0, 2).reshape(G.D, -1)
        unit = np.abs(Wf.conj().T @ Wf - np.eye(G.D)).max()
        idx = rng.choice(len(E), neta, replace=False)
        # make sure some non-pure etas are included
        fe = (det(ch.g0, (E[:, 0], E[:, 1])) * ch.dinv) % p
        idx = np.unique(np.concatenate([idx, np.where(fe == 0)[0][:8]]))
        res = {}
        neg = np.array([((-j) % p) * p + ((-k) % p) for j in range(p) for k in range(p)])
        sigs = {int(i): G.sigma(tuple(E[i]), lam) for i in idx}
        for sgn in (1, -1):
            pure, amp, diag = ch.states(E[idx], sgn)
            for relab, perm in (('y', np.arange(p * p)), ('-y', neg)):
                errp = errn = 0.0
                for r, i in enumerate(idx):
                    sig = sigs[int(i)]
                    for b in range(p * p):
                        blk = W[b].conj().T @ sig @ W[b]; c = perm[b]
                        if pure[r]:
                            errp = max(errp, np.abs(blk - np.outer(amp[r, c], amp[r, c].conj()) / p ** 2).max())
                        else:
                            errn = max(errn, np.abs(blk - np.diag(diag[r, c])).max())
                res[(sgn, relab)] = (errp, errn)
        worst[lam] = (unit, res, int((fe[idx] == 0).sum()), len(idx))
    return worst


if __name__ == '__main__':
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for lam, (unit, res, nnp, n) in validate(p).items():
        print('p=%d lam=%s: IS basis unitary err=%.1e; %d etas (%d with H in N_lam); max|block(dense sigma) - block(formula)| (pure rows, H-in-N rows):'
              % (p, lam, unit, n, nnp), flush=True)
        for key, (ep, en) in res.items():
            print('     convention sgn=%+d, y-label %-3s : %.1e  %.1e' % (key[0], key[1], ep, en), flush=True)
