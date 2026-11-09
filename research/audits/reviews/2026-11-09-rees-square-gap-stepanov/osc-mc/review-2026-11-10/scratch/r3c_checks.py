"""Referee round 3c: independent check of the kappa = 7 class values at p = 36037, against 47041 and 58787.
Own code path: everything is computed from the npz arrays (S1, cnt, S2, P, orb, supp, rb, N1, mu1, Nunl) through
per-batch Gram matrices G[b, b'] = sum_cells w2 Re(V_b conj V_b'); k6_spike_survey is not imported.
X = (sum G - tr G)/(B(B-1)) is the cross-batch (noise-free) estimate of sum w2 |E V|^2, as in the survey estimators.
Robustness views (batches are by S, so each S-cluster sits in one batch):
  per-batch y_b = sum_{b' != b} G[b,b']/(B-1) (X is their mean), leave-one-out and leave-two-out values,
  all C(16,8) half-samples, 8 super-batches (random pairings), and an exact sign-flip test over 2^15 patterns.
Run from anywhere: nice -n 19 python -I r3c_checks.py"""
import os, math, itertools
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
os.chdir(OSC)
rng = np.random.default_rng(20261110)
FILES = ['mc_k7_p36037_s13.npz', 'mc_k7_p47041_s12.npz', 'mc_k7_p58787_sb.npz']


def cB_null(B, reps=400000):            # E sqrt(max(U,0)) / sqrt(1/B) for iid complex N(0,1) batch means (own seed)
    V = (rng.standard_normal((reps, B)) + 1j * rng.standard_normal((reps, B))) / math.sqrt(2)
    sq = (np.abs(V.sum(1)) ** 2 - (np.abs(V) ** 2).sum(1)) / (B * (B - 1))
    return np.sqrt(np.maximum(sq, 0)).mean() * math.sqrt(B)


def gram(Vb, w2, m):
    A = Vb[:, m] * np.sqrt(w2[m])[None, :]
    return (A @ A.conj().T).real


def Xof(G, idx=None):
    if idx is not None: G = G[np.ix_(idx, idx)]
    b = len(G)
    return (G.sum() - np.trace(G)) / (b * (b - 1))


def jk(G):
    B = len(G); full = Xof(G)
    loo = np.array([Xof(G, np.delete(np.arange(B), t)) for t in range(B)])
    return full, loo, math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum())


out = {}
for f in FILES:
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    S1, cnt, S2 = d['S1'], d['cnt'].astype(float), d['S2']; B = len(cnt); N = cnt.sum()
    Vb = S1 / cnt[:, None, None]; Vh = S1.sum(0) / N
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    n = p + 1 - 2 * k; kf = math.factorial(k); kp2 = k * k / p
    ow = orb * np.abs(P[:, rb]); w2 = np.outer(ow, ow)
    sig2 = np.maximum(S2 / N - np.abs(Vh) ** 2, 0); nz2 = sig2 / float(d['Nunl'])
    seb = np.sqrt((np.abs(Vb - Vb.mean(0)) ** 2).sum(0) / (B * (B - 1)))
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    grp = {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}
    rate = cnt / (int(d['nS']) / B)
    r = {'p': p, 'lam': p / k ** (k - 1), 'B': B, 'N': int(N), 'nS': int(d['nS']), 'N1mu1': float(d['N1']) / float(d['mu1']),
         'N1se': float(d['N1']) / float(d['mu1']) * rate.std(ddof=1) / math.sqrt(B) / rate.mean(), 'cnt': cnt}
    for g, m in grp.items():
        G = gram(Vb, w2, m); full, loo, se = jk(G)
        noise = (w2[m] * nz2[m]).sum(); Wg = w2[m].sum(); unit = 1.0 if g == 'L' else kp2
        s = full - noise; val = lambda x: math.sqrt(max(x, 0) / Wg) / unit
        y = (G.sum(1) - np.diag(G)) / (B - 1)
        l2o = min(Xof(G, [i for i in range(B) if i not in (t, u)]) for t, u in itertools.combinations(range(B), 2))
        halves = np.array([Xof(G, list(c)) for c in itertools.combinations(range(B), B // 2)])
        zs = []
        for _ in range(40):                                  # 8 super-batches from random pairings
            perm = rng.permutation(B); Vs = np.array([(S1[perm[2 * i]] + S1[perm[2 * i + 1]]) / (cnt[perm[2 * i]] + cnt[perm[2 * i + 1]]) for i in range(B // 2)])
            f8, l8, se8 = jk(gram(Vs, w2, m)); zs.append((f8 - noise) / se8)
        E = np.array([[1] + [1 - 2 * ((j >> i) & 1) for i in range(B - 1)] for j in range(2 ** (B - 1))], dtype=float)
        Xe = ((E @ G) * E).sum(1) - np.trace(G)
        off = G[~np.eye(B, dtype=bool)]
        top2 = [int(i) for i in np.argsort(-y)[:2]]; keep = [i for i in range(B) if i not in top2]; Gk = G[np.ix_(keep, keep)]
        Ek = np.array([[1] + [1 - 2 * ((j >> i) & 1) for i in range(len(keep) - 1)] for j in range(2 ** (len(keep) - 1))], dtype=float)
        Xk = ((Ek @ Gk) * Ek).sum(1) - np.trace(Gk)
        extra = (float((off > 0).mean()), top2, val(Xof(Gk) - noise), float((Xk >= Xk[0] - 1e-12 * abs(Xk[0])).mean()))
        r[g] = dict(extra=extra, val=val(s), z=s / se, lo=val(s - 2 * se), hi=val(s + 2 * se), noise=noise, X=full, y=y,
                    loo=np.array([val(x - noise) for x in loo]), l2o=val(l2o - noise),
                    half=np.array([val(x - noise) for x in halves]), z8=np.array(zs), pflip=float((Xe >= Xe[0] - 1e-12 * abs(Xe[0])).mean()),
                    Wg=Wg)
    # per-bin unbiased w-rms and jackknife z, with the batch shares of each bin's X
    bins = {}
    for a in sorted(set(supp)):
        for b2 in sorted(set(supp)):
            if b2 < a or (a == 0 and b2 <= 2): continue
            m = ((supp[:, None] == a) & (supp[None, :] == b2)) | ((supp[:, None] == b2) & (supp[None, :] == a))
            if not m.any(): continue
            G = gram(Vb, w2, m); full, loo, se = jk(G); y = (G.sum(1) - np.diag(G)) / (B - 1)
            bins[(a, b2)] = dict(w=w2[m].sum(), rms=math.sqrt(max(full, 0) / w2[m].sum()), z=full / se, y=y)
    r['bins'] = bins
    # PW_pair: debiased, null floor, CS upper (same definitions as pw_bin_cs.py / the survey)
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1)); Vdb = np.sqrt(np.maximum(sq, 0))
    cB = cB_null(B); z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
    den = 1 - 2 * k * (orb[pair] * (P[pair, rb] * kf)).sum().real / (n * kf)
    pm = np.zeros_like(two); pm[pair, z0] = True; pm[z0, pair] = True
    pairterm = (w2[pm] * np.abs(Vh[pm] + k)).sum()
    nzm = np.ones_like(pm); nzm[z0, z0] = False; nzm[pm] = False
    cs = pairterm + sum(v['w'] * v['rms'] for v in bins.values())     # sqrt(W_bin * max(X_bin, 0)) = W_bin * w-rms
    gsplit = {}
    for g, m in grp.items():
        mm = m & nzm
        gsplit[g] = ((w2[mm] * Vdb[mm]).sum() / n / den, (w2[mm] * cB * seb[mm]).sum() / n / den,
                     sum(v['w'] * v['rms'] for kk, v in bins.items() if (kk[0] == 0 and g == 'L') or (kk[0] >= 2 and ((kk[0] + kk[1] <= 6) == (g == 'L')))) / n / den)
    r['PWsplit'] = gsplit; r['PW_other'] = (w2[nzm & ~grp['L'] & ~grp['D']] * Vdb[nzm & ~grp['L'] & ~grp['D']]).sum() / n / den
    r.update(PW=(pairterm + (w2[nzm] * Vdb[nzm]).sum()) / n / den, PW_floor=(pairterm + (w2[nzm] * cB * seb[nzm]).sum()) / n / den,
             PW_cs=cs / n / den, PW_paironly=pairterm / n / den, cB=cB,
             c=float(np.median((sig2 * np.outer(orb, orb) / n)[two])),
             infl=float(np.median((seb ** 2 * N / float(d['Nunl']) / np.maximum(nz2, 1e-300))[two & (nz2 > 0)])))
    out[p] = r

for p, r in out.items():
    print('=== p=%d lambda=%.3f  B=%d batches  nS=%d  conf=%d  N1/mu1 %.3f (se %.3f)' % (p, r['lam'], r['B'], r['nS'], r['N'], r['N1mu1'], r['N1se']))
    print('  batch counts: %s  (mean %.0f, sd %.1f, Poisson sd %.1f)' % (' '.join('%d' % c for c in r['cnt']), r['cnt'].mean(), r['cnt'].std(ddof=1), math.sqrt(r['cnt'].mean())))
    print('  PW_pair debiased %.3f  null floor %.3f  CS upper %.3f  pair-term only %.3f  (c_B %.4f)  c %.3f  infl %.2f' % (
        r['PW'], r['PW_floor'], r['PW_cs'], r['PW_paironly'], r['cB'], r['c'], r['infl']))
    print('  PW_pair by group (debiased / null floor / CS): L %.3f / %.3f / %.3f   D %.3f / %.3f / %.3f   cells in neither %.4f' % (
        *r['PWsplit']['L'], *r['PWsplit']['D'], r['PW_other']))
    for g in ('L', 'D'):
        q = r[g]; unit = '' if g == 'L' else ' [k^2/p]'
        print('  B_%s%s %.3f (z %.1f, 2sig %.3f-%.3f)  noise-subtracted part %.1e of X' % (g, unit, q['val'], q['z'], q['lo'], q['hi'], q['noise'] / q['X'] if q['X'] else 0))
        ys = np.sort(q['y'])[::-1]
        print('     per-batch y_b (X = mean): %d of %d positive; largest two carry %.0f%% of sum y; median-based value %.3f' % (
            (q['y'] > 0).sum(), len(q['y']), 100 * ys[:2].sum() / q['y'].sum(), math.sqrt(max(np.median(q['y']) - q['noise'], 0) / q['Wg']) / (1.0 if g == 'L' else 49 / p)))
        print('     leave-one-out %.3f-%.3f; worst leave-two-out %.3f; half-samples (8 of 16) 5/50/95%% %.3f/%.3f/%.3f, min %.3f' % (
            q['loo'].min(), q['loo'].max(), q['l2o'], *np.percentile(q['half'], [5, 50, 95]), q['half'].min()))
        print('     positive off-diagonal G[b,b\']: %.0f%%; without the top-2 batches %s: value %.3f, exact sign-flip P %.2e (2^13 patterns)' % (
            100 * q['extra'][0], q['extra'][1], q['extra'][2], q['extra'][3]))
        print('     8 super-batches (40 random pairings): z median %.1f, range %.1f-%.1f;  exact sign-flip P(X >= observed) = %.2e' % (
            np.median(q['z8']), q['z8'].min(), q['z8'].max(), q['pflip']))
    if p == 36037:
        r47 = out.get(47041)
        print('  per-bin w-rms (z_jk); D bins with m >= 7:')
        Dk = [kk for kk in r['bins'] if kk[0] >= 2 and kk[0] + kk[1] >= 7]
        print('    ' + '  '.join('(%d,%d) %.4f (%.1f)' % (kk[0], kk[1], r['bins'][kk]['rms'], r['bins'][kk]['z']) for kk in r['bins']))
        print('    D bins: %d, z range %.1f-%.1f, all positive: %s' % (len(Dk), min(r['bins'][kk]['z'] for kk in Dk), max(r['bins'][kk]['z'] for kk in Dk), all(r['bins'][kk]['z'] > 0 for kk in Dk)))
        Y = np.array([r['bins'][kk]['y'] / np.abs(r['bins'][kk]['y']).sum() for kk in Dk])
        top = [tuple(int(i) for i in np.argsort(-r['bins'][kk]['y'])[:2]) for kk in Dk]
        print('    top-2 batches by y_b in each D bin:', top)
        C = np.corrcoef(Y); iu = np.triu_indices(len(Dk), 1)
        print('    correlation of the per-batch y_b profiles across D bins: median %.2f (range %.2f-%.2f)' % (np.median(C[iu]), C[iu].min(), C[iu].max()))
        yL = r['L']['y']; yD = r['D']['y']
        print('    corr(y_b of L, y_b of D) %.2f; batches ranked by L: %s; by D: %s' % (np.corrcoef(yL, yD)[0, 1], [int(i) for i in np.argsort(-yL)[:4]], [int(i) for i in np.argsort(-yD)[:4]]))
        for kk in ((0, 3), (2, 2), (2, 3), (3, 3)):
            print('    bin %s: 36037 %.4f (z %.1f) vs 47041 %.4f (z %.1f); per-batch y_b positive %d of 16, top-2 share %.0f%%' % (
                kk, r['bins'][kk]['rms'], r['bins'][kk]['z'], r47['bins'][kk]['rms'], r47['bins'][kk]['z'], (r['bins'][kk]['y'] > 0).sum(),
                100 * np.sort(r['bins'][kk]['y'])[::-1][:2].sum() / r['bins'][kk]['y'].sum()))
# kappa = 6 comparison (survey_snapshot.out and its replication rows): B_L, PW_pair, floor, CS
k6 = {2347: (0.302, 0.413, 0.75, 0.23, 1.02), 3571: (0.459, 0.309, 0.29, 0.15, 0.29), 3877: (0.499, 0.273, 0.26, 0.12, 0.24), 4219: (0.543, 0.367, 0.30, 0.15, 0.30)}
print('=== kappa = 6 rises from lambda ~0.5 to 2347 (0.302): B_L %s; PW_pair %s' % (
    ' '.join('%.2fx' % (k6[2347][1] / k6[q][1]) for q in (3571, 3877, 4219)), ' '.join('%.2fx' % (k6[2347][2] / k6[q][2]) for q in (3571, 3877, 4219))))
print('    kappa = 6 band (0.25, 0.31] at the snapshot: median B_L 0.430, max 0.527 (1987); PW_pair median 1.25')
r36, r47, r58 = out[36037], out[47041], out[58787]
print('=== kappa = 7 rises: B_L %.2fx (47041) %.2fx (58787); PW_pair %.2fx %.2fx; PW minus floor %.3f / %.3f / %.3f; CS upper %.3f / %.3f / %.3f' % (
    r36['L']['val'] / r47['L']['val'], r36['L']['val'] / r58['L']['val'], r36['PW'] / r47['PW'], r36['PW'] / r58['PW'],
    r36['PW'] - r36['PW_floor'], r47['PW'] - r47['PW_floor'], r58['PW'] - r58['PW_floor'], r36['PW_cs'], r47['PW_cs'], r58['PW_cs']))
