"""Mutual information of IS-type measurements on k labelled free23 copies with SHARED hidden eta.
(Exact finite computation up to float round-off; it can only falsify.  AI-written, pending human review.)

States: closed-form IS front end of isbasis.py (validated there against the dense V-picture sigma of
2026-11-13-rees-free23-two-copy/hpgp2_free23.py to 1e-17).  Per copy and label lam: blocks y (p^2 of them,
the IS Fourier outcome over N_lam), each a state D_{eta,y} on the x-register C^p.  k copies: blocks
(y_1..y_k), states (x)_i D_{eta,y_i} on C^{p^k}.  Hypotheses: HYP2 = (line(e1:e2), e3) [nuisance eta_c],
HYP1 = line(e1:e2) [nuisance e3, eta_c]; uniform prior; H uniform over hard cyclic subgroups.

Orbit reduction: U(x') maps IS basis |y,x> -> |y', x+1> (a permutation, checked numerically per label), and every
measurement below is covariant under x_i -> x_i + 1 up to an outcome relabelling, so one rep block per orbit (weight
= orbit size) is exact for Holevo, PGM and measurement entropies.

Measurements (all block-wise, outcome includes the block labels y):
  pair (x1, x2):
    F2      : Fourier on x1 and on x2 (QFT_p (x) QFT_p);
    line d  : coordinates x1 = r + d x, x2 = x (d in F_p), 'line inf': x1 = x, x2 = r; measure r, then QFT_p on x.
              This is the IS Thm 5 merge step with weights (delta_1, delta_2) = (d, 1):  d = -c cancels the eta_c phase
              (Lemma J relation);  d^3 = -c cancels the cubic phase coefficient (IS's diagonal-equation step).
    comp    : computational basis (control).
  triple (x1, x2, x3):
    F3, 'line delta' (delta in P^2: measure the 2-dim residual, QFT on x), 'plane l' (measure l.x, QFT_p^2 on the plane).
Reported per measurement: MI with HYP1 and HYP2 (bits) and the MAP success probability for HYP1 (the line of v_1).
Benchmarks: Holevo chi (upper bound for every measurement), PGM (pretty good measurement; not claimed efficient),
Holevo after measuring r for each line d (shows which merge is lossless).
"""
import sys, os, time, itertools, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from isbasis import Chart, all_etas            # noqa: E402

SGN = -1                                        # convention validated in isbasis.py


def H(P):
    P = np.asarray(P).ravel(); P = P[P > 1e-300]
    return float(-(P * np.log2(P)).sum())


def Hw(P, w):
    """sum over classes (axis 0) of w * entropy contribution"""
    P = np.where(P > 1e-300, P, 1.0)
    return float((w.reshape((-1,) + (1,) * (P.ndim - 1)) * (-P * np.log2(P))).sum())


def ent_eigs(ev, w=None):
    ev = np.where(ev > 1e-14, ev, 1.0); t = -ev * np.log2(ev)
    return float(t.sum()) if w is None else float((w.reshape((-1,) + (1,) * (t.ndim - 1)) * t).sum())


def _cols(pure, amp, diag, p):
    """column sets (n, ny, p, m) with D = sum_m col col^dag; m = 1 if all rows pure else p"""
    n, ny = amp.shape[:2]
    if pure.all():
        return (amp / p)[..., None]
    cols = np.zeros((n, ny, p, p), complex)
    cols[pure, :, :, 0] = amp[pure] / p
    idx = np.arange(p)
    tmp = np.zeros((int((~pure).sum()), ny, p, p)); tmp[:, :, idx, idx] = np.sqrt(diag[~pure]); cols[~pure] = tmp
    return cols


def orbit_reps(ch, E, nsample=60, seed=0):
    """permutation perm[y] with D_{perm y}(x+1) = D_y(x), found on a sample of etas (pure and non-pure) and then
    re-checked on a second sample; returns reps [(y, size)]"""
    p = ch.p; rng = np.random.default_rng(seed)
    fe = (np.array([ch.f((e[0], e[1])) for e in E]))
    def sample(s):
        i1 = rng.choice(np.where(fe != 0)[0], nsample, replace=False)
        i0 = rng.choice(np.where(fe == 0)[0], min(nsample // 3, int((fe == 0).sum())), replace=False)
        return np.concatenate([i1, i0])
    def dens(idx):
        pure, amp, diag = ch.states(E[idx], SGN)
        cols = _cols(pure, amp, diag, p)
        return np.einsum('nyam,nybm->nyab', cols, cols.conj())
    D = dens(sample(0)); Ds = np.roll(np.roll(D, 1, axis=2), 1, axis=3); n = len(D)
    perm = np.empty(p * p, int)
    for y in range(p * p):
        err = np.abs(D - Ds[:, y][:, None]).reshape(n, p * p, -1).max(axis=(0, 2))
        perm[y] = int(np.argmin(err)); assert err[perm[y]] < 1e-12, (y, err.min())
    D = dens(sample(1)); Ds = np.roll(np.roll(D, 1, axis=2), 1, axis=3)
    chk = max(np.abs(D[:, perm[y]] - Ds[:, y]).max() for y in range(p * p))
    assert chk < 1e-12, chk
    seen, reps = set(), []
    for y in range(p * p):
        if y in seen: continue
        orb, c = [], y
        while c not in orb: orb.append(c); c = perm[c]
        seen.update(orb); reps.append((y, len(orb)))
    return reps, chk


def copy_data(ch, E, chunk=1500):
    """orbit reps, and for every eta the rep-block data (pure flag, amp (n, nrep, p), diag (n, nrep, p))"""
    reps, chk = orbit_reps(ch, E)
    ys = np.array([y for y, _ in reps]); n = len(E); p = ch.p
    pure = np.zeros(n, bool); amp = np.zeros((n, len(ys), p), complex); diag = np.zeros((n, len(ys), p))
    for s in range(0, n, chunk):
        pu, am, dg = ch.states(E[s:s + chunk], SGN)
        pure[s:s + chunk] = pu; amp[s:s + chunk] = am[:, ys]; diag[s:s + chunk] = dg[:, ys]
    return dict(reps=reps, chk=chk, pure=pure, amp=amp, diag=diag)


# ----------------------------------------------------------------------------- measurement bases (index maps)
def pair_bases(p):
    """dict name -> (perm, nr) : new index (r, x) -> old index x1*p+x2 ; then QFT over x (last axis of length p).
    'F2' handled separately."""
    out = {}
    R, X = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
    for d in range(p):
        out['line %d' % d] = (((R + d * X) % p) * p + X).ravel()
    out['line inf'] = (X * p + R).ravel()
    return out


def triple_bases(p):
    """'line delta' -> perm over (r1, r2, x); 'plane l' -> perm over (r, x', x'') ; old index x1 p^2 + x2 p + x3"""
    proj = [v for v in itertools.product(range(p), repeat=3) if any(v) and v[next(i for i in range(3) if v[i])] == 1]
    lines, planes = {}, {}
    A, B, C = np.meshgrid(np.arange(p), np.arange(p), np.arange(p), indexing='ij')
    pw = np.array([p * p, p, 1])
    for v in proj:
        v = np.array(v); i0 = next(i for i in range(3) if v[i]); oth = [i for i in range(3) if i != i0]
        # line: x = r1 e_a + r2 e_b + x * v
        xv = np.zeros((3,) + A.shape, dtype=np.int64)
        for i in range(3): xv[i] = C * v[i]
        xv[oth[0]] += A; xv[oth[1]] += B
        lines['line %s' % ''.join(map(str, v))] = (np.tensordot(pw, xv % p, axes=1)).ravel()
        # plane: x = r e_i0 + x' (e_a - v_a e_i0) + x'' (e_b - v_b e_i0)
        xv = np.zeros((3,) + A.shape, dtype=np.int64)
        xv[i0] = A - v[oth[0]] * B - v[oth[1]] * C
        xv[oth[0]] = B; xv[oth[1]] = C
        planes['plane %s' % ''.join(map(str, v))] = (np.tensordot(pw, xv % p, axes=1)).ravel()
    return lines, planes


# ----------------------------------------------------------------------------- engine
def run(p, lams, do_pgm=True, do_post=True, line_only=None, log=print):
    k = len(lams); t0 = time.time()
    F1, E = all_etas(p); nE = len(E)
    hyp2 = np.repeat(np.arange(len(F1) * p), p * p)                  # etas() order: line, e3, eta_c
    nh2, nh1 = len(F1) * p, len(F1)
    charts = [Chart(p, l) for l in lams]
    per = [copy_data(ch, E) for ch in charts]
    log('  orbit sizes per copy: %s  (orbit check err %s)  [%.0fs]' % ([sorted(s for _, s in d['reps']) for d in per],
        ['%.0e' % d['chk'] for d in per], time.time() - t0))
    classes = list(itertools.product(*[list(enumerate(d['reps'])) for d in per]))
    dim = p ** k
    if k == 2:
        bases = pair_bases(p); bnames = ['comp', 'F2'] + list(bases)
    else:
        lines, planes = triple_bases(p); bases = {**lines, **planes}; bnames = ['comp', 'F3'] + list(bases)
    if line_only is not None: bnames = [b for b in bnames if b in line_only]
    # generic lines: every copy's state is pure (H not inside any N_lam_i); special lines are public and few
    g1 = np.array([all(d['pure'][l * p ** 3] for d in per) for l in range(nh1)]); g2 = np.repeat(g1, p)
    fams = {'HYP1': (1, np.ones(nh1, bool)), 'HYP2': (2, np.ones(nh2, bool)), 'HYP1g': (1, g1), 'HYP2g': (2, g2)}
    # accumulators (sums over classes with weights)
    S = {1: np.zeros(nh1), 2: np.zeros(nh2)}; Sbar = {f: 0.0 for f in fams}
    MH = {b: {1: np.zeros(nh1), 2: np.zeros(nh2)} for b in bnames}
    MHbar = {b: {f: 0.0 for f in fams} for b in bnames}; Msucc = {b: {f: 0.0 for f in fams} for b in bnames}
    PS = {b: {1: np.zeros(nh1), 2: np.zeros(nh2)} for b in bases} if do_post else None
    PSbar = {b: {f: 0.0 for f in fams} for b in bases} if do_post else None
    pg = {f: dict(Hh=0.0, Hbar=0.0, succ=0.0) for f in fams} if do_pgm else None
    offr = 0.0; wtot = 0
    for ci, cl in enumerate(classes):
        w = float(np.prod([s for _, (_, s) in cl])); wtot += w
        # explicit states rho_h (HYP2) built hypothesis by hypothesis (within h the line, hence every copy's
        # purity, is fixed); measurement probabilities from the same column sets
        R2 = np.zeros((nh2, dim, dim), complex)
        P2s = {bb: np.zeros((nh2, dim)) for bb in bnames}
        for h in range(nh2):
            sl = slice(h * p * p, (h + 1) * p * p)
            parts = [_cols(per[i]['pure'][sl], per[i]['amp'][sl, cl[i][0]][:, None], per[i]['diag'][sl, cl[i][0]][:, None], p)[:, 0]
                     for i in range(k)]
            if k == 2:
                T = np.einsum('nam,nbq->abnmq', *parts)
            else:
                T = np.einsum('nam,nbq,ncs->abcnmqs', *parts)
            Vh = T.reshape(dim, -1)
            R2[h] = Vh @ Vh.conj().T / (p * p)
            for bb in bnames:
                if bb == 'comp':
                    P2s[bb][h] = np.real(np.diag(R2[h]))
                    continue
                if bb in ('F2', 'F3'):
                    X = np.fft.fftn(Vh.reshape((p,) * k + (-1,)), axes=tuple(range(k)), norm='ortho')
                else:
                    nq = 1 if bb.startswith('line') else 2
                    X = Vh[bases[bb]].reshape((dim // p ** nq,) + (p,) * nq + (-1,))
                    X = np.fft.fftn(X, axes=tuple(range(1, 1 + nq)), norm='ortho')
                P2s[bb][h] = (np.abs(X) ** 2).sum(axis=-1).reshape(dim) / (p * p)
        R = {2: R2, 1: R2.reshape(nh1, p, dim, dim).mean(axis=1)}
        for lv in (1, 2):
            S[lv] += w * np.array([ent_eigs(e) for e in np.linalg.eigvalsh(R[lv])])
        for f, (lv, m) in fams.items():
            Sbar[f] += w * ent_eigs(np.linalg.eigvalsh(R[lv][m].mean(axis=0)))
        for b in bnames:
            P = {2: P2s[b], 1: P2s[b].reshape(nh1, p, dim).mean(axis=1)}
            for lv in (1, 2):
                MH[b][lv] += np.array([w * H(q) for q in P[lv]])
            for f, (lv, m) in fams.items():
                MHbar[b][f] += w * H(P[lv][m].mean(axis=0))
                Msucc[b][f] += w * P[lv][m].max(axis=0).sum() / m.sum()
        # post-measurement Holevo for each merge (measure r only)
        if do_post:
            dlin = ((-lams[1][0] * pow(lams[0][0], -1, p)) % p) if (k == 2 and lams[0][1] == lams[1][1] == 0 and lams[0][0]) else None
            for b, perm in bases.items():
                nq = 1 if b.startswith('line') else 2
                nr, bd = dim // p ** nq, p ** nq
                Q2 = R2[:, perm][:, :, perm].reshape(nh2, nr, bd, nr, bd)
                Q2d = np.einsum('hrarb->hrab', Q2)
                if dlin is not None and b == 'line %d' % dlin:
                    off = Q2.copy()
                    for r in range(nr): off[:, r, :, r, :] = 0
                    offr = max(offr, float(np.abs(off).max()))
                Q = {2: Q2d, 1: Q2d.reshape(nh1, p, nr, bd, bd).mean(axis=1)}
                for lv in (1, 2):
                    PS[b][lv] += w * np.array([ent_eigs(np.linalg.eigvalsh(q)) for q in Q[lv]])
                for f, (lv, m) in fams.items():
                    PSbar[b][f] += w * ent_eigs(np.linalg.eigvalsh(Q[lv][m].mean(axis=0)))
        # PGM per class block and per family
        if do_pgm:
            for f, (lv, m) in fams.items():
                Rf = R[lv][m]; nh = len(Rf); Rb = Rf.mean(axis=0)
                ev, U = np.linalg.eigh(Rb)
                inv = np.where(ev > 1e-13, 1 / np.sqrt(np.where(ev > 1e-13, ev, 1)), 0.0)
                Rm = (U * inv) @ U.conj().T
                Mh = np.einsum('ab,hbc,cd->had', Rm, Rf, Rm, optimize=True) / nh
                Pm = np.real(np.einsum('gab,hba->hg', Mh, Rf, optimize=True))
                pg[f]['Hh'] += sum(w * H(q) for q in Pm) / nh; pg[f]['Hbar'] += w * H(Pm.mean(axis=0))
                pg[f]['succ'] += w * Pm.max(axis=0).sum() / nh
        if ci % max(1, len(classes) // 8) == 0:
            log('    class %d/%d [%.0fs]' % (ci + 1, len(classes), time.time() - t0))
    res = {'labels': [list(l) for l in lams], 'p': p, 'wtot': wtot, 'offr': offr,
           'nhyp': {f: int(m.sum()) for f, (lv, m) in fams.items()}}
    res['chi'] = {f: Sbar[f] - S[lv][m].mean() for f, (lv, m) in fams.items()}
    res['chi']['meanS2'] = S[2].mean()
    res['meas'] = {b: {f: {'MI': MHbar[b][f] - MH[b][lv][m].mean(), 'succ': Msucc[b][f]} for f, (lv, m) in fams.items()}
                   for b in bnames}
    if do_post:
        res['post'] = {b: {f: PSbar[b][f] - PS[b][lv][m].mean() for f, (lv, m) in fams.items()} for b in bases}
    if do_pgm:
        res['pgm'] = {f: {'MI': g['Hbar'] - g['Hh'], 'succ': g['succ']} for f, g in pg.items()}
    res['time'] = time.time() - t0
    return res


def report(res, log=print):
    p = res['p']; F = ('HYP1', 'HYP1g', 'HYP2', 'HYP2g'); nh = res['nhyp']
    log('  labels=%s  weight total=%d (= p^{2k}: %d)  meanS(HYP2)=%.4f  max off-r-block (d=-c)=%.1e  #hyp %s'
        % (res['labels'], res['wtot'], p ** (2 * len(res['labels'])), res['chi']['meanS2'], res['offr'], nh))
    log('    %-12s %s' % ('', '   '.join('%-22s' % ('%s (prior %.3f)' % (f, 1 / nh[f])) for f in F)))
    log('    %-12s %s' % ('Holevo', '   '.join('chi=%.4f%14s' % (res['chi'][f], '') for f in F)))
    if 'pgm' in res:
        log('    %-12s %s' % ('PGM', '   '.join('MI=%.4f succ=%.4f ' % (res['pgm'][f]['MI'], res['pgm'][f]['succ']) for f in F)))
    for b, m in res['meas'].items():
        log('    %-12s %s' % (b, '   '.join('MI=%.4f succ=%.4f ' % (m[f]['MI'], m[f]['succ']) for f in F))
            + ('  | post-r chi: %s' % ' '.join('%.4f' % res['post'][b][f] for f in F) if 'post' in res and b in res['post'] else ''))


if __name__ == '__main__':
    p = int(sys.argv[1]); mode = sys.argv[2]
    out = os.path.join(HERE, 'json'); os.makedirs(out, exist_ok=True)
    lg = lambda s: print(s, flush=True)
    if mode == 'pairs':
        cs = [int(c) for c in sys.argv[3].split(',')] if len(sys.argv) > 3 else list(range(1, p))
        for c in cs:
            lg('p=%d pair (lam, c lam), lam=(1,0), c=%d%s; cube root of -c: %s' % (
                p, c, ' (=-1, binary)' if c == p - 1 else '', [d for d in range(p) if pow(d, 3, p) == (-c) % p]))
            r = run(p, [(1, 0), (c, 0)], log=lg); report(r, lg)
            json.dump(r, open(os.path.join(out, 'pair_p%d_c%d.json' % (p, c)), 'w'), indent=1)
    elif mode == 'pairctl':        # independent pair control
        r = run(p, [(1, 0), (0, 1)], log=lg); lg('p=%d independent pair control' % p); report(r, lg)
        json.dump(r, open(os.path.join(out, 'pair_p%d_indep.json' % p), 'w'), indent=1)
    elif mode == 'triple':
        trip = [tuple(int(a) for a in s.split(':')) for s in sys.argv[3].split(',')]
        opts = sys.argv[4].split(',') if len(sys.argv) > 4 else []
        nat = [Chart(p, t) for t in trip]
        lg('p=%d triple %s; chart normalisations n_i = lam_i([x_i\',z]) = %s  (lossless plane: l ~ n)'
           % (p, trip, [int(c.lam[0] * c.xp[0] + c.lam[1] * c.xp[1]) % p for c in nat]))
        r = run(p, trip, do_pgm='nopgm' not in opts, do_post='nopost' not in opts, log=lg); report(r, lg)
        json.dump(r, open(os.path.join(out, 'triple_p%d_%s.json' % (p, '_'.join('%d%d' % t for t in trip))), 'w'), indent=1)
