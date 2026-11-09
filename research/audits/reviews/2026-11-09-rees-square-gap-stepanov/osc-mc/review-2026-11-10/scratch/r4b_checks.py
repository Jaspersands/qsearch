"""Referee round 4b (10 Nov): (1) kappa = 7 class values at 35099 against 36037, 47041 and 58787, by an own Gram-matrix
path, with k6_spike_survey.analyse as a second path; a kappa = 6 calibration of single-prime B_L ratios;
(2) 2143 at seeds 13 and 14.  35099's npz is outside the repo (scratchpad of the session).
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4b_checks.py > r4b_checks.out"""
import os, sys, glob, math, itertools
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
SP = '/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
os.chdir(OSC); sys.path.insert(0, OSC)
import k6_spike_survey as ks
rng = np.random.default_rng(2026111042)


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


def cB_null(B, reps=200000):
    V = (rng.standard_normal((reps, B)) + 1j * rng.standard_normal((reps, B))) / math.sqrt(2)
    sq = (np.abs(V.sum(1)) ** 2 - (np.abs(V) ** 2).sum(1)) / (B * (B - 1))
    return np.sqrt(np.maximum(sq, 0)).mean() * math.sqrt(B)


def own(f):
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
    r = {'p': p, 'k': k, 'lam': p / k ** (k - 1), 'B': B, 'N': int(N), 'nS': int(d['nS']), 'S1': S1}
    for g, m in (('L', (two & (ms <= 6)) | one), ('D', two & (ms >= 7))):
        G = gram(Vb, w2, m); full, loo, se = jk(G)
        noise = (w2[m] * nz2[m]).sum(); Wg = w2[m].sum(); unit = 1.0 if g == 'L' else kp2
        s = full - noise
        val = (lambda Wg, unit: (lambda x: math.sqrt(max(x, 0) / Wg) / unit))(Wg, unit)
        r[g] = dict(G=G, X=full, s=s, se=se, noise=noise, f=val, val=val(s), z=s / se, lo=val(s - 2 * se), hi=val(s + 2 * se))
    bins = {}
    sv = sorted(set(supp.tolist()))
    for a in sv:
        for b2 in sv:
            if b2 < a or (a == 0 and b2 <= 2): continue
            mm = ((supp[:, None] == a) & (supp[None, :] == b2)) | ((supp[:, None] == b2) & (supp[None, :] == a))
            if not mm.any(): continue
            G = gram(Vb, w2, mm); full, _, se = jk(G); W = w2[mm].sum()
            grp = 'L' if (a == 0 and b2 >= 3) or (a >= 2 and a + b2 <= 6) else 'D'
            bins[(a, b2)] = dict(W=W, X=full, se=se, z=full / se, grp=grp, rms=math.sqrt(max(full, 0) / W),
                                 lo=math.sqrt(max(full - 2 * se, 0) / W), hi=math.sqrt(max(full + 2 * se, 0) / W))
    r['bins'] = bins
    cB = cB_null(B)
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1)); Vdb = np.sqrt(np.maximum(sq, 0))
    z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
    den = 1 - 2 * k * (orb[pair] * (P[pair, rb] * kf)).sum().real / (n * kf)
    pm = np.zeros(w2.shape, dtype=bool); pm[pair, z0] = True; pm[z0, pair] = True
    pairterm = (w2[pm] * np.abs(Vh[pm] + k)).sum()
    nzm = np.ones(w2.shape, dtype=bool); nzm[z0, z0] = False; nzm[pm] = False
    r['PW'] = (pairterm + (w2[nzm] * Vdb[nzm]).sum()) / n / den
    r['PWf'] = (pairterm + (w2[nzm] * cB * seb[nzm]).sum()) / n / den
    r['PWcs'] = (pairterm + sum(math.sqrt(v['W'] * max(v['X'], 0)) for v in bins.values())) / n / den
    r['N1mu1'] = float(d['N1']) / float(d['mu1'])
    rate = cnt / (int(d['nS']) / B); r['N1se'] = r['N1mu1'] * rate.std(ddof=1) / math.sqrt(B) / rate.mean()
    return r


# ---------------------------------------------------------------- (1) kappa = 7
F7 = {35099: SP + '/mc_k7_p35099_s13.npz', 36037: 'mc_k7_p36037_s13.npz', 47041: 'mc_k7_p47041_s12.npz', 58787: 'mc_k7_p58787_sb.npz'}
K7 = {p: own(f) for p, f in F7.items()}
print('(1) kappa = 7, own Gram path (second path: k6_spike_survey.analyse, max relative difference in brackets)')
for p, r in K7.items():
    a = ks.analyse(F7[p])
    dif = max(abs(a['L'] - r['L']['val']) / a['L'], abs(a['L_z'] - r['L']['z']) / abs(a['L_z']), abs(a['D'] - r['D']['val']) / max(a['D'], 1e-9),
              abs(a['PW'] - r['PW']) / a['PW'], abs(a['PW_cs'] - r['PWcs']) / a['PW_cs'], abs(a['N1mu1'] - r['N1mu1']) / a['N1mu1'])
    GL = r['L']['G']; B = len(GL); y = (GL.sum(1) - np.diag(GL)) / (B - 1); vL = r['L']['f']; nL = r['L']['noise']
    loo = [vL(Xof(GL, np.delete(np.arange(B), t)) - nL) for t in range(B)]
    l2o = min(vL(Xof(GL, [i for i in range(B) if i not in c]) - nL) for c in itertools.combinations(range(B), 2))
    hv = np.array([vL(Xof(GL, list(c)) - nL) for c in itertools.combinations(range(B), B // 2)])
    GD = r['D']['G']; E = np.array([[1] + [1 - 2 * ((j >> i) & 1) for i in range(B - 1)] for j in range(2 ** (B - 1))], dtype=float)
    Xe = ((E @ GD) * E).sum(1) - np.trace(GD); pflip = float((Xe >= Xe[0] - 1e-12 * abs(Xe[0])).mean())
    print('  %d (lam %.3f, conf %d, nS %d) [%.0e]: N1/mu1 %.3f (%.3f); PW %.3f floor %.3f CS %.3f' % (
        p, r['lam'], r['N'], r['nS'], dif, r['N1mu1'], r['N1se'], r['PW'], r['PWf'], r['PWcs']))
    print('     B_L %.3f (z %.1f, 2sig %.3f-%.3f); y_b>0 %d/16; loo %.3f-%.3f; l2o min %.3f; halves min/5/50/95/max %.3f/%.3f/%.3f/%.3f/%.3f' % (
        r['L']['val'], r['L']['z'], r['L']['lo'], r['L']['hi'], (y > 0).sum(), min(loo), max(loo), l2o, hv.min(), *np.percentile(hv, [5, 50, 95]), hv.max()))
    print('     B_D %.2f (z %.1f, < %.2f); exact sign-flip P %.3g' % (r['D']['val'], r['D']['z'], r['D']['hi'], pflip))
    r['halves'] = hv
print('  L bins (w-rms |V|, z, 2sig): 35099 | 36037 | 47041 ; ratio 36037/35099 central, and 36037 lower end / 35099 upper end')
for kk, v in K7[36037]['bins'].items():
    if v['grp'] != 'L': continue
    u = K7[35099]['bins'][kk]; w = K7[47041]['bins'][kk]
    rc = v['rms'] / u['rms'] if u['rms'] > 0 else float('inf'); rl = v['lo'] / u['hi'] if u['hi'] > 0 else float('inf')
    sh = lambda r_, kk_: max(r_['bins'][kk_]['X'], 0) / sum(max(x['X'], 0) for x in r_['bins'].values() if x['grp'] == 'L')   # X = sum_cells w2 |V|^2
    print('   %s: %.4f (%.1f, <%.4f) | %.4f (%.1f, >%.4f) | %.4f (%.1f) ; %s, %s ; share of L sum 35099 %.2f, 36037 %.2f' % (
        kk, u['rms'], u['z'], u['hi'], v['rms'], v['z'], v['lo'], w['rms'], w['z'], '%.1fx' % rc if rc < 1e3 else 'inf',
        '%.1fx' % rl if rl < 1e3 else 'inf', sh(K7[35099], kk), sh(K7[36037], kk)))
a, b = K7[36037]['L'], K7[35099]['L']
print('  B_L ratio 36037/35099: central %.2f; 2-sigma (lower/upper) %.2f; min half-sample of 36037 / max half-sample of 35099 %.2f' % (
    a['val'] / b['val'], a['lo'] / b['hi'], K7[36037]['halves'].min() / K7[35099]['halves'].max()))
print('  L B ratio 36037/47041 %.2f, /58787 %.2f' % (a['val'] / K7[47041]['L']['val'], a['val'] / K7[58787]['L']['val']))
sym7 = {}
for fn in ('sym/sym_rate_k7.out', 'sym/sym_rate_k7_lam03.out'):
    for line in open(fn):
        w = line.split()
        if w and w[0].isdigit() and 0.28 <= float(w[1]) <= 0.32: sym7[int(w[0])] = float(w[3])
sv7 = sorted(sym7.values())
print('  symR at lam ~ 0.3: %d primes, median %.2f; 35099 (%.2f) ranks %d of %d from the bottom' % (
    len(sv7), float(np.median(sv7)), sym7[35099], sv7.index(sym7[35099]) + 1, len(sv7)))

# ---------------------------------------------------------------- kappa = 6 calibration of a single-prime B_L ratio
print('\n    kappa = 6 calibration (seed-13 survey; flags as in k6_spike_survey; unflagged = no sD, sPW or sN)')
R6 = {}
for f in sorted(glob.glob('survey/mc_k6_p*_s13.npz')):
    r = ks.analyse(f); R6[r['p']] = r
BANDS = [('1', 0.19, 0.22), ('2', 0.22, 0.2501), ('3', 0.2501, 0.31), ('4', 0.49, 0.56)]
for bn, lo_, hi_ in BANDS:
    q = [p for p in R6 if lo_ <= R6[p]['lam'] < hi_]
    med = {x: float(np.median([R6[p][x] for p in q])) for x in ('L', 'D', 'PW', 'N1mu1')}
    unf = [p for p in q if not (R6[p]['D_lo'] > 2 * med['D'] or R6[p]['PW'] > 2 * med['PW'] or R6[p]['N1mu1'] > 2 * med['N1mu1'])]
    BL = {p: R6[p]['L'] for p in q}
    top = sorted(q, key=lambda p: -BL[p])[:3]
    pairs = [(x, y) for x in unf for y in unf if x != y]
    ratio = lambda x, y: BL[x] / BL[y]
    bys = sorted(q, key=lambda p: R6[p]['symR']); tsym = bys[-1]; msym = bys[(len(bys) - 1) // 2]
    print('  band %s: %d primes, %d unflagged; B_L median %.3f; top B_L / median: %s; unflagged max/min %.2f; '
          'unflagged ordered pairs with ratio >= 2.68: %d of %d, >= 2.0: %d' % (
              bn, len(q), len(unf), med['L'], ', '.join('%d %.2f' % (p, BL[p] / med['L']) for p in top),
              max(BL[p] for p in unf) / min(BL[p] for p in unf), sum(ratio(x, y) >= 2.68 for x, y in pairs), len(pairs),
              sum(ratio(x, y) >= 2.0 for x, y in pairs)))
    print('     top-symR prime %d (symR %.1f) B_L %.3f against median-symR prime %d (symR %.1f) B_L %.3f: ratio %.2f' % (
        tsym, R6[tsym]['symR'], BL[tsym], msym, R6[msym]['symR'], BL[msym], BL[tsym] / BL[msym]))

# ---------------------------------------------------------------- (2) 2143, seeds 13 and 14
print('\n(2) 2143, seed 13 against seed 14 (own path; s = X - noise, z = s/se_jk, B^2 = s/(W unit^2))')
A, Bq = own('survey/mc_k6_p2143_s13.npz'), own('survey/mc_k6_p2143_s14.npz')
d14 = np.load('survey/mc_k6_p2143_s14.npz')
print('  seed 14: conf %d, nS %d, batch counts %d-%d (S-batched), S1 differs from seed 13: %s' % (
    Bq['N'], Bq['nS'], d14['cnt'].min(), d14['cnt'].max(), not np.allclose(A['S1'], Bq['S1'])))
for g in ('L', 'D'):
    a, b = A[g], Bq[g]
    zs = (a['s'] - b['s']) / math.hypot(a['se'], b['se'])
    seB = lambda q: q['val'] / (2 * q['z'])                   # delta method on B = sqrt(s/(W unit^2))
    zB = (a['val'] - b['val']) / math.hypot(seB(a), seB(b))
    alt = lambda q: (q['val'] ** 2) / q['z']                  # the coordinator's se from B^2/z (same W, unit at both seeds)
    zc = (a['val'] ** 2 - b['val'] ** 2) / math.hypot(alt(a), alt(b))
    print('  B_%s: %.4f (z %.2f, lo %.4f) vs %.4f (z %.2f, lo %.4f); difference in s / combined se %.2f; on the B scale %.2f; '
          'from B^2 and z %.2f; noise share of X %.3f / %.3f' % (
              g, a['val'], a['z'], a['lo'], b['val'], b['z'], b['lo'], zs, zB, zc, a['noise'] / a['X'], b['noise'] / b['X']))
print('  N1/mu1 %.3f (%.3f) vs %.3f (%.3f), z_diff %.2f; PW %.3f vs %.3f' % (
    A['N1mu1'], A['N1se'], Bq['N1mu1'], Bq['N1se'], (A['N1mu1'] - Bq['N1mu1']) / math.hypot(A['N1se'], Bq['N1se']), A['PW'], Bq['PW']))
q3 = [p for p in R6 if 0.2501 <= R6[p]['lam'] < 0.31]
m3 = {x: float(np.median([R6[p][x] for p in q3])) for x in ('D', 'PW', 'N1mu1')}
fmax = Bq['D']['z'] / 2 * (1 - (2 * m3['D'] / Bq['D']['val']) ** 2)
print('  seed-14 flags against the seed-13 band-3 medians: sD %s (lo %.3f vs %.3f, f_max %.2f), sPW %s (%.3f vs %.3f), sN %s (%.3f vs %.3f)' % (
    Bq['D']['lo'] > 2 * m3['D'], Bq['D']['lo'], 2 * m3['D'], fmax, Bq['PW'] > 2 * m3['PW'], Bq['PW'], 2 * m3['PW'],
    Bq['N1mu1'] > 2 * m3['N1mu1'], Bq['N1mu1'], 2 * m3['N1mu1']))
