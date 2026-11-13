"""Exact F_p checks behind Lemma S (the IS degree-reduction step needs a common fil4 quotient).
(AI-written, pending human review; exact integer arithmetic mod p; finite checks only falsify.)

1. For every label lam != 0, every eta with f_lam(e) != 0 and every IS block y, the IS phase P_y(x) (isbasis.py,
   convention SGN) is a polynomial of degree <= 3 with zero constant term, and its cubic coefficient is
       a3 = kappa_lam * beta_lam(e),   beta_lam(e) = g0-coordinate of (eta/f(e) - x') in V/D,
       kappa_lam = -SGN * det(g0,x') * lam([x',z]) / 6        (analytic, from the BCH cubic term).
   a3 does not depend on y, on e3 or on eta_c.  The linear coefficient's eta_c part is SGN*lam(eta_c)/f(e).
2. beta_lam is a Mobius function of the line [e] with its pole at [e] = [g0(lam)].
3. Cancellation count: for k copies with labels lam_i and public IS-shift weights delta (in F_p^k minus 0), count the
   lines [e] (all copies pure) with sum_i delta_i^3 kappa_i beta_i(e) = 0.  Same-quotient labels admit delta with
   all lines; pairwise-independent labels: at most k lines for every delta (Lemma S).
"""
import sys, os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from isbasis import Chart, all_etas, bchv, det          # noqa: E402
SGN = -1


def polyfit_modp(vals, p):
    """coefficients a_0..a_{p-1} of the unique poly of degree < p with P(x) = vals[x] (x = 0..p-1), mod p"""
    V = np.array([[pow(x, i, p) for i in range(p)] for x in range(p)], dtype=object)
    # invert Vandermonde mod p by Gauss-Jordan
    M = [list(V[r]) + [int(vals[r]) % p] for r in range(p)]
    for c in range(p):
        q = next(r for r in range(c, p) if M[r][c] % p)
        M[c], M[q] = M[q], M[c]; iv = pow(M[c][c], -1, p); M[c] = [v * iv % p for v in M[c]]
        for r in range(p):
            if r != c and M[r][c]:
                f = M[r][c]; M[r] = [(a - f * b) % p for a, b in zip(M[r], M[c])]
    return np.array([M[r][p] for r in range(p)], dtype=np.int64)


def phases(ch, E):
    """integer phases P_y(x) (p^2, n, p) for pure etas"""
    p = ch.p; fe = np.array([ch.f((e[0], e[1])) for e in E]); assert (fe != 0).all()
    inv = np.array([pow(int(v), -1, p) for v in fe]); Et = (E * inv[:, None]) % p
    xs = np.arange(p); XP = np.array([ch.xp[0], ch.xp[1], 0, 0, 0], dtype=np.int64)
    A = (xs[None, :, None] * Et[:, None, :]) % p; B = np.broadcast_to((-xs[:, None] * XP[None, :]) % p, A.shape)
    nu = bchv(A.reshape(-1, 5), B.reshape(-1, 5), ch.C, p).reshape(A.shape)
    return (SGN * ch.ytilde(nu)) % p, Et


def bracket(a, b, C, p): return np.einsum('i,j,ijk->k', a, b, C) % p


def kappa(ch):
    p = ch.p; C = ch.C
    xp = np.array([ch.xp[0], ch.xp[1], 0, 0, 0]); g0 = np.array([ch.g0[0], ch.g0[1], 0, 0, 0]); z = np.array([0, 0, 1, 0, 0])
    lz = bracket(xp, z, C, p); lam_xz = (ch.lam[0] * lz[3] + ch.lam[1] * lz[4]) % p
    return (-SGN * det(ch.g0, ch.xp) * lam_xz * pow(6, -1, p)) % p


def beta(ch, e12):
    """g0-coordinate of e/f(e) - x' (e12: (..., 2))"""
    p = ch.p; fe = ch.f((e12[..., 0], e12[..., 1])); inv = np.vectorize(lambda v: pow(int(v), -1, p))(fe)
    v0 = (e12[..., 0] * inv - ch.xp[0]) % p; v1 = (e12[..., 1] * inv - ch.xp[1]) % p
    return ch.gcoord(np.stack([v0, v1], -1))


def check1(p, labels, nsample=400, seed=0):
    rng = np.random.default_rng(seed); F1, E = all_etas(p); bad = dict(deg=0, const=0, a3=0, y=0, ec=0, n=0)
    for lam in labels:
        ch = Chart(p, lam); fe = np.array([ch.f((e[0], e[1])) for e in E])
        idx = rng.choice(np.where(fe != 0)[0], min(nsample, int((fe != 0).sum())), replace=False)
        ph, Et = phases(ch, E[idx]); kap = kappa(ch); be = beta(ch, E[idx][:, :2])
        for r in range(len(idx)):
            co = np.array([polyfit_modp(ph[y, r], p) for y in range(0, p * p, max(1, p * p // 7))])
            bad['n'] += 1
            bad['deg'] += int((co[:, 4:] != 0).any()); bad['const'] += int((co[:, 0] != 0).any())
            bad['y'] += int((co[:, 3] != co[0, 3]).any())
            bad['a3'] += int(co[0, 3] != (kap * be[r]) % p)
            # eta_c part of the linear coefficient: compare with eta_c = 0
            e0 = E[idx[r]].copy(); e0[3:] = 0
            ph0, _ = phases(ch, e0[None]); c0 = polyfit_modp(ph0[0, 0], p)
            lamec = (ch.lam[0] * E[idx[r]][3] + ch.lam[1] * E[idx[r]][4]) % p
            pred = (SGN * lamec * pow(int(ch.f((E[idx[r]][0], E[idx[r]][1]))), -1, p)) % p
            bad['ec'] += int(((co[0, 1] - c0[1]) % p != pred) or (co[0, 2] != c0[2]) or (co[0, 3] != c0[3]))
    return bad


def lines(p):
    return [(0, 1)] + [(1, s) for s in range(p)]


def cancel_count(p, labels):
    """max over delta != 0 (projective) of #{generic lines [e] : sum delta_i^3 kappa_i beta_i(e) = 0}, and #delta
    attaining 'all generic lines'"""
    chs = [Chart(p, l) for l in labels]; k = len(chs)
    gen = [e for e in lines(p) if all(ch.f(e) for ch in chs)]
    T = np.array([[(kappa(ch) * int(beta(ch, np.array(e)))) % p for e in gen] for ch in chs])   # (k, #gen)
    best, nall = 0, 0
    for d in itertools.product(range(p), repeat=k):
        if not any(d) or d[next(i for i in range(k) if d[i])] != 1: continue
        w = np.array([pow(x, 3, p) for x in d])
        cnt = int((((w[:, None] * T).sum(axis=0)) % p == 0).sum())
        best = max(best, cnt); nall += int(cnt == len(gen))
    return best, nall, len(gen)


def check_e3(p, labels, nsample=200, seed=1):
    """Lemma Q input: a2(e3 + 1) - a2(e3) = -(1/2) n_lam / f(e)  with n_lam = lam([x',z]) (convention SGN = -1),
    i.e. in the intrinsic parameter t (x = f(e) t) the e3-part of the t^2 coefficient is -(1/2) e3 lam([e,z])."""
    rng = np.random.default_rng(seed); F1, E = all_etas(p); bad = n = 0
    for lam in labels:
        ch = Chart(p, lam); fe = np.array([ch.f((e[0], e[1])) for e in E]); nl = (ch.lam[0] * ch.xp[0] + ch.lam[1] * ch.xp[1]) % p
        idx = rng.choice(np.where(fe != 0)[0], min(nsample, int((fe != 0).sum())), replace=False)
        for i in idx:
            e0 = E[i].copy(); e1 = e0.copy(); e1[2] = (e1[2] + 1) % p
            a = [polyfit_modp(phases(ch, q[None])[0][y, 0], p) for q in (e0, e1) for y in (0, p + 2)]
            pred = (-nl * pow(2, -1, p) * pow(int(fe[i]), -1, p)) % p
            n += 1; bad += int((a[2][2] - a[0][2]) % p != pred or (a[3][2] - a[1][2]) % p != pred)
    return bad, n


if __name__ == '__main__':
    for p in (5, 7, 11):
        labs = [(1, 0), (2, 0), (0, 1), (1, 2), (3, 4 % p), (2, 3)]
        print('p=%d check 1 (degree <= 3, a0 = 0, a3 independent of y, a3 = kappa*beta, eta_c only in a1 as SGN lam(eta_c)/f(e)):'
              % p, check1(p, labs, nsample=150 if p == 11 else 300), flush=True)
        print('     e3-part of a2 (Lemma Q input) mismatches / checked:', check_e3(p, labs, 100 if p == 11 else 200), flush=True)
        print('     kappa(lam) for lam=(1,0),(c,0): %s  (chart for (c,0) has g0 scaled by c: kappa ~ c^2, beta ~ 1/c, so a3 ~ c)'
              % [kappa(Chart(p, (c, 0))) for c in range(1, p)], flush=True)
    for p in (5, 7, 11, 13):
        out = []
        for labs in ([(1, 0), (2, 0)], [(1, 0), (p - 1, 0)], [(1, 0), (0, 1)], [(1, 0), (1, 1)],
                     [(1, 0), (0, 1), (1, 1)], [(1, 0), (0, 1), (1, 2)], [(1, 0), (0, 1), (2, 3)], [(1, 0), (2, 0), (0, 1)]):
            b, na, ng = cancel_count(p, labs)
            out.append('%s: max lines=%d of %d generic, #delta cancelling on all=%d' % (labs, b, ng, na))
        print('p=%d IS cubic-cancellation counts:\n   ' % p + '\n   '.join(out), flush=True)
