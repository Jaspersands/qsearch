"""Referee round 4 (10 Nov): the final kappa = 6 survey (k6_spike_survey.out, 04:49) and the pre-registered scoring
(survey/score_predictions.py/.out; survey/predictions_hclass.txt, 02:16; survey/predictions_N1mu1.txt, 01:20).
Per-prime values come from k6_spike_survey.analyse (the recorded estimator).  They are cross-checked against an own
code path (per-batch Gram matrices G[b,b'] = sum_cells w2 Re(V_b conj V_b'), as in r3c_checks.py) for B_L, B_D, z,
the 2-sigma lower end and PW_pair (debiased, null floor, CS upper).  Bands, flags, test sets, the H1-H3 scoring,
the rank tests (pooled, per band and band-stratified), the flag robustness and the N1/mu1 scoring are re-implemented
here.  leaveout_BD.py (the draft's source) is also run, so that its output is on record.
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4_checks.py > r4_checks.out"""
import os, sys, glob, math, itertools, datetime, subprocess
import numpy as np
from scipy.stats import mannwhitneyu, rankdata
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
os.chdir(OSC); sys.path.insert(0, OSC)
import k6_spike_survey as ks
rng = np.random.default_rng(2026111004)


def cB_null(B, reps=200000):            # E sqrt(max(U,0)) / sqrt(1/B) for iid complex N(0,1) batch means (own seed)
    V = (rng.standard_normal((reps, B)) + 1j * rng.standard_normal((reps, B))) / math.sqrt(2)
    sq = (np.abs(V.sum(1)) ** 2 - (np.abs(V) ** 2).sum(1)) / (B * (B - 1))
    return np.sqrt(np.maximum(sq, 0)).mean() * math.sqrt(B)


CBN = {}


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
    r = {'p': p, 'B': B, 'N': int(N)}
    for g, m in (('L', (two & (ms <= 6)) | one), ('D', two & (ms >= 7))):
        G = gram(Vb, w2, m); full, loo, se = jk(G)
        noise = (w2[m] * nz2[m]).sum(); Wg = w2[m].sum(); unit = 1.0 if g == 'L' else kp2
        s = full - noise
        val = (lambda Wg, unit: (lambda x: math.sqrt(max(x, 0) / Wg) / unit))(Wg, unit)
        r[g] = dict(G=G, X=full, s=s, se=se, noise=noise, Wg=Wg, unit=unit, f=val, val=val(s), z=s / se, lo=val(s - 2 * se),
                    raw=val(full))
    if B not in CBN: CBN[B] = cB_null(B)
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1)); Vdb = np.sqrt(np.maximum(sq, 0))
    z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
    den = 1 - 2 * k * (orb[pair] * (P[pair, rb] * kf)).sum().real / (n * kf)
    pm = np.zeros(w2.shape, dtype=bool); pm[pair, z0] = True; pm[z0, pair] = True
    pairterm = (w2[pm] * np.abs(Vh[pm] + k)).sum()
    nzm = np.ones(w2.shape, dtype=bool); nzm[z0, z0] = False; nzm[pm] = False
    cs = pairterm; sv = sorted(set(supp.tolist()))
    for a in sv:
        for b2 in sv:
            if b2 < a or (a == 0 and b2 <= 2): continue
            mm = ((supp[:, None] == a) & (supp[None, :] == b2)) | ((supp[:, None] == b2) & (supp[None, :] == a))
            if mm.any(): cs += math.sqrt(w2[mm].sum() * max(Xof(gram(Vb, w2, mm)), 0))
    r.update(PW=(pairterm + (w2[nzm] * Vdb[nzm]).sum()) / n / den, PWf=(pairterm + (w2[nzm] * CBN[B] * seb[nzm]).sum()) / n / den,
             PWcs=cs / n / den)
    r['N1mu1'] = float(d['N1']) / float(d['mu1'])
    rate = cnt / (int(d['nS']) / B); r['N1se'] = r['N1mu1'] * rate.std(ddof=1) / math.sqrt(B) / rate.mean()
    return r


def strat(ps, val, nperm=20000):
    """One-sided (class 1 > class 7) band-stratified permutation test, van Elteren weights: T = sum_b W_b/(n_b+1),
    W_b = rank-sum of class 1 within band b; class labels permuted within bands."""
    obs, parts = 0.0, []
    for bn in sorted({R[p]['band'] for p in ps}):
        q = [p for p in ps if R[p]['band'] == bn]
        c = np.array([R[p]['cls'] == 1 for p in q])
        if c.all() or (~c).all(): continue
        rk = rankdata([val(p) for p in q]); obs += rk[c].sum() / (len(q) + 1); parts.append((rk, int(c.sum()), len(q)))
    perm = np.zeros(nperm)
    for rk, n1, nb in parts:
        idx = np.argsort(rng.random((nperm, nb)), axis=1)[:, :n1]
        perm += rk[idx].sum(1) / (nb + 1)
    return float((perm >= obs - 1e-9).mean())


# ---------------------------------------------------------------- load
files = sorted(glob.glob('survey/mc_k6_p*_s13.npz'))
R = {}
for f in files:
    r = ks.analyse(f)
    r['mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(f)); r['cls'] = r['p'] % 12; r['own'] = own(f)
    R[r['p']] = r
REF = {1933: 'mc_k6_p1933_s11.npz', 2347: 'mc_k6_p2347_s11.npz', 3877: 'mc_k6_p3877_sb.npz', 4219: 'mc_k6_p4219_s11.npz'}
RR = {}
for p, f in REF.items():
    r = ks.analyse(f); r['own'] = own(f); RR[p] = r
PS = sorted(R)
print('Loaded %d survey npz (seed 13); classes: %d are 1 mod 12, %d are 7 mod 12' % (
    len(PS), sum(R[p]['cls'] == 1 for p in PS), sum(R[p]['cls'] == 7 for p in PS)))

# ---------------------------------------------------------------- 1. own code path against analyse()
print('\n1. Own estimator path against k6_spike_survey.analyse, max relative difference over the 89 primes')
for nm, a, b in [('B_L', lambda r: r['L'], lambda o: o['L']['val']), ('B_D', lambda r: r['D'], lambda o: o['D']['val']),
                 ('z_D', lambda r: r['D_z'], lambda o: o['D']['z']), ('B_D 2-sigma lower', lambda r: r['D_lo'], lambda o: o['D']['lo']),
                 ('PW_pair', lambda r: r['PW'], lambda o: o['PW']), ('PW floor', lambda r: r['PW_floor'], lambda o: o['PWf']),
                 ('PW CS', lambda r: r['PW_cs'], lambda o: o['PWcs']), ('N1/mu1', lambda r: r['N1mu1'], lambda o: o['N1mu1'])]:
    dif = [abs(a(R[p]) - b(R[p]['own'])) / max(abs(a(R[p])), 1e-9) for p in PS]
    print('   %-18s %.1e' % (nm, max(dif)))

# ---------------------------------------------------------------- 2. bands, medians, flags
BANDS = [('1', 0.19, 0.22), ('2', 0.22, 0.2501), ('3', 0.2501, 0.31), ('4', 0.49, 0.56)]
BN = [b[0] for b in BANDS]
for p in PS:
    hit = [bn for bn, lo, hi in BANDS if lo <= R[p]['lam'] < hi]
    assert len(hit) == 1, p
    R[p]['band'] = hit[0]
MED = {}
print('\n2. Bands (k6_spike_survey.py test lo <= lam < hi), medians, maxima and flags')
tot = 0
for bn, lo, hi in BANDS:
    b = [p for p in PS if R[p]['band'] == bn]
    med = {q: float(np.median([R[p][q] for p in b])) for q in ('L', 'D', 'PW', 'N1mu1', 'D_nu')}
    MED[bn] = med
    for p in b:
        r = R[p]; r['thrD'] = 2 * med['D']
        r['sD'], r['sPW'], r['sN'] = r['D_lo'] > 2 * med['D'], r['PW'] > 2 * med['PW'], r['N1mu1'] > 2 * med['N1mu1']
        o = r['own']; r['sD_own'] = o['D']['lo'] > 2 * float(np.median([R[q]['own']['D']['val'] for q in b]))
    fl = [p for p in b if R[p]['sD'] or R[p]['sPW'] or R[p]['sN']]; tot += len(fl)
    mx = lambda q: max(b, key=lambda p: R[p][q])
    print('  band %s: lam %.3f-%.3f, %d primes (classes %d/%d); median B_L %.3f B_D %.3f (nu_D %.2f) PW %.3f N1/mu1 %.3f; thr_D %.3f' % (
        bn, min(R[p]['lam'] for p in b), max(R[p]['lam'] for p in b), len(b), sum(R[p]['cls'] == 1 for p in b),
        sum(R[p]['cls'] == 7 for p in b), med['L'], med['D'], med['D_nu'], med['PW'], med['N1mu1'], 2 * med['D']))
    print('     max B_L %.3f (%d), B_D %.2f (%d), PW %.2f (%d), N1/mu1 %.2f (%d); min N1/mu1 %.2f (%d)' % (
        R[mx('L')]['L'], mx('L'), R[mx('D')]['D'], mx('D'), R[mx('PW')]['PW'], mx('PW'), R[mx('N1mu1')]['N1mu1'], mx('N1mu1'),
        min(R[p]['N1mu1'] for p in b), min(b, key=lambda p: R[p]['N1mu1'])))
    print('     flagged %d: %s' % (len(fl), '; '.join('%d(c%d) %s' % (p, R[p]['cls'], ' '.join(x for x in ('sD', 'sPW', 'sN') if R[p][x]))
                                                     for p in fl)))
    print('     own-path sD flags identical: %s' % all(R[p]['sD'] == R[p]['sD_own'] for p in b))
print('  total flagged: %d of %d; smallest N1/mu1 overall %.3f (%d)' % (tot, len(PS), min(R[p]['N1mu1'] for p in PS),
                                                                     min(PS, key=lambda p: R[p]['N1mu1'])))
for p in (2113, 2269):
    r = R[p]; print('  %d: B_D %.2f (z %.1f) PW %.2f N1/mu1 %.2f' % (p, r['D'], r['D_z'], r['PW'], r['N1mu1']))

# ---------------------------------------------------------------- 3. PW_pair < 1
print('\n3. PW_pair below 1, per band: debiased / CS upper / null floor')
for bn in BN:
    b = [p for p in PS if R[p]['band'] == bn]
    print('  band %s: %d/%d/%d of %d; max debiased %.3f (%d) whose CS is %.3f; max CS %.3f (%d)' % (
        bn, sum(R[p]['PW'] < 1 for p in b), sum(R[p]['PW_cs'] < 1 for p in b), sum(R[p]['PW_floor'] < 1 for p in b), len(b),
        R[max(b, key=lambda p: R[p]['PW'])]['PW'], max(b, key=lambda p: R[p]['PW']), R[max(b, key=lambda p: R[p]['PW'])]['PW_cs'],
        max(R[p]['PW_cs'] for p in b), max(b, key=lambda p: R[p]['PW_cs'])))
b3 = [p for p in PS if R[p]['band'] == '3']
print('  band 3 in order of p (debiased/CS): ' + ' '.join('%d:%.2f/%.2f' % (p, R[p]['PW'], R[p]['PW_cs']) for p in b3))
b4 = [p for p in PS if R[p]['band'] == '4']
print('  band 4 debiased minus floor: median %.3f, max %.3f' % (np.median([R[p]['PW'] - R[p]['PW_floor'] for p in b4]),
                                                               max(R[p]['PW'] - R[p]['PW_floor'] for p in b4)))

# ---------------------------------------------------------------- 4. sets
cut = datetime.datetime(2026, 11, 10, 2, 16)
T71 = [p for p in PS if R[p]['mtime'] > cut]
T70 = [p for p in T71 if p != 1933]
KNOWN = [2347, 3877, 3889, 4219]
T66 = [p for p in T70 if p not in KNOWN]
F17 = [p for p in PS if R[p]['mtime'] <= cut and p != 1759]
print('\n4. Sets (npz mtime against 02:16)')
print('  written after 02:16: %d primes; equal to "1741 and 1777 onward": %s' % (
    len(T71), T71 == [p for p in PS if p == 1741 or p >= 1777]))
print('  formation set: %d %s' % (len(F17), F17))
print('  mtimes: ' + ', '.join('%d %s' % (p, R[p]['mtime'].strftime('%H:%M:%S')) for p in (1741, 1753, 1759, 1777, 1933, 2143, 2347, 3877, 3889, 4219)))
print('  known before 02:16 but in the 70: 2347, 4219 (seed-11 runs), 3877 (sb run; N1 fit point) and 3889 ("seen so far",')
print('  pre-fix run).  Strict test set = 70 less these four: %d primes' % len(T66))
for p in KNOWN + [1933]:
    print('     %d class %d band %s: B_D %.2f (lo %.2f, thr %.2f) sD %s; N1/mu1 %.2f' % (
        p, R[p]['cls'], R[p]['band'], R[p]['D'], R[p]['D_lo'], R[p]['thrD'], R[p]['sD'], R[p]['N1mu1']))

# ---------------------------------------------------------------- 5. H1 and the flag margins
print('\n5. (H1) sD primes in the 70 and their margins')
print('  f_max = se factor that unflags: lower end = sqrt(max(s - 2 f se, 0)/W)/unit equals thr at f = (z/2)(1 - (thr/B_D)^2)')
for p in T70:
    r = R[p]
    if not r['sD']: continue
    o = r['own']['D']; fmax = o['z'] / 2 * (1 - (r['thrD'] / o['val']) ** 2)
    print('   %d c%d band %s: B_D %.4f lo %.4f thr %.4f (B_D/median %.2f) z %.2f  f_max %.3f' % (
        p, r['cls'], r['band'], o['val'], o['lo'], r['thrD'], o['val'] / (r['thrD'] / 2), o['z'], fmax))
print('  thresholds from other medians (band 3 / band 4): all primes %.4f / %.4f; the 70: %.4f / %.4f; strict 66: %.4f / %.4f' % tuple(
    2 * float(np.median([R[p]['D'] for p in S if R[p]['band'] == bn])) for S in (PS, T70, T66) for bn in ('3', '4')))
for p in (2143, 2179, 3823):
    bn = R[p]['band']; thrs = [2 * float(np.median([R[q]['D'] for q in S if R[q]['band'] == bn])) for S in (PS, T70, T66)]
    print('   %d: lo %.4f; flagged under the three medians: %s' % (p, R[p]['D_lo'], [R[p]['D_lo'] > t for t in thrs]))
for f in (1.0, 1.5, 2.0, 3.0):
    surv = [p for p in PS if R[p]['own']['D']['f'](R[p]['own']['D']['s'] - 2 * f * R[p]['own']['D']['se']) > R[p]['thrD']]
    s70 = [p for p in surv if p in T70]
    print('  se x %.1f: sD class 1 %s | class 7 %s ; in the 70: class 1 %d, class 7 %d' % (
        f, [p for p in surv if R[p]['cls'] == 1], [p for p in surv if R[p]['cls'] == 7], sum(R[p]['cls'] == 1 for p in s70),
        sum(R[p]['cls'] == 7 for p in s70)))

# ---------------------------------------------------------------- 6. H2, H3 and rank tests on three test sets
print('\n6. (H2), (H3) and rank tests of B_D by class (one-sided, class 1 > class 7)')
VD = lambda p: R[p]['D']
for name, T in (('70 (as scored)', T70), ('71 (the letter: all written after 02:16, 1933 included)', T71), ('66 (strict)', T66)):
    n1 = sum(R[p]['cls'] == 1 for p in T); print('  --- %s: %d primes, %d/%d' % (name, len(T), n1, len(T) - n1))
    sd7 = [p for p in T if R[p]['sD'] and R[p]['cls'] == 7]
    print('     (H1) class-7 sD primes: %s -> %s' % (sd7, 'refuted' if sd7 else 'holds'))
    qual = []
    for bn in BN:
        q = [p for p in T if R[p]['band'] == bn]
        t1 = [VD(p) for p in q if R[p]['cls'] == 1]; t7 = [VD(p) for p in q if R[p]['cls'] == 7]
        if len(t1) >= 6 and len(t7) >= 6:
            qual += q
            print('     (H2) band %s: %d/%d, medians %.3f vs %.3f -> %s; MW p %.4f; exact within-band permutation p %.4f' % (
                bn, len(t1), len(t7), np.median(t1), np.median(t7), 'holds' if np.median(t1) > np.median(t7) else 'FAILS',
                mannwhitneyu(t1, t7, alternative='greater').pvalue, strat(q, VD)))
        else:
            print('     (H2) band %s: %d/%d (does not qualify)' % (bn, len(t1), len(t7)))
    sn = [(p, R[p]['cls']) for p in T if R[p]['sN']]
    print('     (H3) sN: %s -> %s' % (sn, 'holds' if {c for _, c in sn} == {1, 7} else 'fails'))
    x1 = [VD(p) for p in T if R[p]['cls'] == 1]; x7 = [VD(p) for p in T if R[p]['cls'] == 7]
    print('     pooled MW p %.4f (medians %.2f/%.2f); band-stratified permutation p: all bands %.4f, the qualifying bands %.4f' % (
        mannwhitneyu(x1, x7, alternative='greater').pvalue, np.median(x1), np.median(x7), strat(T, VD), strat(qual, VD)))
print('  post hoc variants (stratified permutation p, all 89 / the 70 / strict 66):')
for nm, v in (('B_D unsubtracted (sqrt X)', lambda p: R[p]['own']['D']['raw']), ('B_D^cl (cluster noise)', lambda p: R[p]['D_cl']),
              ('N1/mu1', lambda p: R[p]['N1mu1']), ('symR', lambda p: R[p]['symR']), ('nu_D (noise level)', lambda p: R[p]['D_nu'])):
    print('     %-28s %.4f / %.4f / %.4f' % (nm, strat(PS, v), strat(T70, v), strat(T66, v)))
res = {}
for bn in BN:
    q = [p for p in PS if R[p]['band'] == bn]
    x = np.log([R[p]['N1mu1'] for p in q]); y = np.log([max(R[p]['D'], 0.02) for p in q])
    A = np.column_stack([np.ones_like(x), x]); cf = np.linalg.lstsq(A, y, rcond=None)[0]
    for p, e in zip(q, y - A @ cf): res[p] = e
    print('     band %s: log B_D on log N1/mu1 slope %.2f' % (bn, cf[1]))
print('     %-28s %.4f / %.4f / %.4f' % ('B_D residual given N1/mu1', strat(PS, res.get), strat(T70, res.get), strat(T66, res.get)))

# ---------------------------------------------------------------- 7. robustness of the marginal flags
print('\n7. Flag robustness (B_D in k^2/p units; thr = 2 x band median; halves = all C(16,8) half-samples)')
for p in (2143, 2179, 3823, 2053, 3889, 4129, 2137, 2221, 2341, 2113, 2269):
    r = R[p]; o = r['own']['D']; G = o['G']; B = len(G); thr = r['thrD']; val = o['f']; noise = o['noise']
    y = (G.sum(1) - np.diag(G)) / (B - 1)
    loo = [val(Xof(G, np.delete(np.arange(B), t)) - noise) for t in range(B)]
    l2o = [val(Xof(G, [i for i in range(B) if i not in c]) - noise) for c in itertools.combinations(range(B), 2)]
    halves = np.array([val(Xof(G, list(c)) - noise) for c in itertools.combinations(range(B), B // 2)])
    keep = 0
    for t in range(B):
        idx = np.delete(np.arange(B), t); full, _, se = jk(G[np.ix_(idx, idx)]); keep += val(full - noise - 2 * se) > thr
    offd = G[~np.eye(B, dtype=bool)]
    print('   %d c%d: B_D %.3f thr %.3f | y_b>0 %d/16, top-2 share %.2f, G[b,b\']>0 %.0f%% | loo min %.3f, l2o min %.3f (%d of 120 <= thr) '
          '| halves <= thr %.3f | flag kept leaving out one batch (re-jackknifed): %d/16' % (
              p, r['cls'], o['val'], thr, (y > 0).sum(), np.sort(y)[::-1][:2].sum() / y.sum(), 100 * (offd > 0).mean(), min(loo), min(l2o),
              sum(x <= thr for x in l2o), (halves <= thr).mean(), keep))
print('  leaveout_BD.py (the draft\'s source), run as given:')
for thr, ps in ((R[2143]['thrD'], (2143, 2179)), (R[3823]['thrD'], (3823,))):
    out = subprocess.run([sys.executable, '-I', 'review-2026-11-10/scratch/leaveout_BD.py', '%.4f' % thr] + [str(p) for p in ps],
                         capture_output=True, text=True, cwd=OSC)
    print('     ' + (out.stdout.strip() + out.stderr.strip()[-300:]).replace('\n', '\n     '))

# ---------------------------------------------------------------- 8. replication across seeds
print('\n8. Same prime, two seeds (s13 survey against the earlier file): difference / combined jackknife se')
for p, f in REF.items():
    a, b = R[p]['own'], RR[p]['own']
    zL = (a['L']['s'] - b['L']['s']) / math.hypot(a['L']['se'], b['L']['se'])
    zD = (a['D']['s'] - b['D']['s']) / math.hypot(a['D']['se'], b['D']['se'])
    zN = (a['N1mu1'] - b['N1mu1']) / math.hypot(a['N1se'], b['N1se'])
    print('   %d (%s, conf %d vs %d): B_L %.3f vs %.3f (z_diff %+.1f) | B_D %.2f (z %.1f) vs %.2f (z %.1f), z_diff %+.1f | '
          'N1/mu1 %.2f vs %.2f (z_diff %+.1f) | PW %.2f vs %.2f' % (
              p, f.split('_')[-1][:-4], a['N'], b['N'], a['L']['val'], b['L']['val'], zL, a['D']['val'], a['D']['z'], b['D']['val'],
              b['D']['z'], zD, a['N1mu1'], b['N1mu1'], zN, a['PW'], b['PW']))

# ---------------------------------------------------------------- 9. N1/mu1 predictions
print('\n9. N1/mu1 predictions (survey/predictions_N1mu1.txt)')
L = open('survey/predictions_N1mu1.txt').read().splitlines()
ins = {int(t.split(':')[0]): float(t.split(':')[1].split('/')[0]) for t in L[1].split()[1:]}
pred = {}
for line in L[2:]:
    if line[:1].isdigit():
        for t in line.split(): pred[int(t.split(':')[0])] = float(t.split(':')[1])
sym = lambda p: ks.SYM[p]['symR']
lam = lambda p: p / 6 ** 5
obsN = {p: (RR[3877]['N1mu1'] if p == 3877 else R[p]['N1mu1']) for p in ins}
print('  in-sample primes %d (%s); listed vs npz N1/mu1 max |diff| %.3f; predicted primes %d; survey primes in neither: %s' % (
    len(ins), sorted(ins), max(abs(ins[p] - obsN[p]) for p in ins), len(pred), [p for p in PS if p not in pred and p not in ins]))
Xi = np.array([[1, math.log(sym(p)), math.log(lam(p))] for p in sorted(ins)]); yi = np.log([obsN[p] for p in sorted(ins)])
cf, rss = np.linalg.lstsq(Xi, yi, rcond=None)[:2]
print('  refit: %+.3f %+.3f log symR %+.3f log lam; residual sd %.3f (n-3 dof) / %.3f (n)' % (
    *cf, math.sqrt(rss[0] / (len(yi) - 3)), math.sqrt(rss[0] / len(yi))))
cfile = np.array([-0.142, 0.978, 1.932])
rp = {p: math.exp(cfile @ [1, math.log(sym(p)), math.log(lam(p))]) for p in pred}
print('  file predictions reproduced from the stated formula: max |diff| %.4f (values rounded to 0.01)' % max(abs(rp[p] - pred[p]) for p in pred))
early = [(p, R[p]['mtime'].strftime('%H:%M')) for p in pred if p in R and R[p]['mtime'] < datetime.datetime(2026, 11, 10, 1, 48, 18)]
print('  predicted primes whose npz predates the file mtime 01:48: %s' % early)
err = {p: math.log(R[p]['N1mu1'] / pred[p]) for p in pred if p in R and p != 1933}
def summ(ps):
    v = np.array([err[p] for p in ps]); return '%2d: rms %.3f mean %+.3f (se %.3f)' % (len(v), math.sqrt((v ** 2).mean()), v.mean(), v.std(ddof=1) / math.sqrt(len(v)))
grp = {'lam <= 0.25': [p for p in err if R[p]['lam'] <= 0.2501], '(0.25, 0.31]': [p for p in err if R[p]['band'] == '3'],
       'lam ~ 0.5': [p for p in err if R[p]['band'] == '4']}
for nm, ps in grp.items():
    print('   %-13s as scored %s | less 2347, 4219: %s' % (nm, summ(ps), summ([p for p in ps if p not in (2347, 4219)])))
print('   all          as scored %s | less 2347, 4219: %s' % (summ(list(err)), summ([p for p in err if p not in (2347, 4219)])))
print('   largest |error| %.2f (%d); errors above 0.30 in absolute value: %d of %d' % (
    max(abs(e) for e in err.values()), max(err, key=lambda p: abs(err[p])), sum(abs(e) > 0.30 for e in err.values()), len(err)))
print('   by class: mean error class 1 %+.3f (n %d), class 7 %+.3f (n %d); two-sided MW p %.3f' % (
    np.mean([err[p] for p in err if R[p]['cls'] == 1]), sum(R[p]['cls'] == 1 for p in err), np.mean([err[p] for p in err if R[p]['cls'] == 7]),
    sum(R[p]['cls'] == 7 for p in err), mannwhitneyu([err[p] for p in err if R[p]['cls'] == 1], [err[p] for p in err if R[p]['cls'] == 7]).pvalue))
q4 = grp['lam ~ 0.5']
ls = np.log([sym(p) for p in q4]); ll = np.log([lam(p) for p in q4]); lo = np.log([R[p]['N1mu1'] for p in q4])
def ols(A, y):
    c, r_, *_ = np.linalg.lstsq(A, y, rcond=None); s2 = ((y - A @ c) ** 2).sum() / (len(y) - A.shape[1])
    return c, np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
c1, e1 = ols(np.column_stack([np.ones_like(ls), ls]), lo)
c2, e2 = ols(np.column_stack([np.ones_like(ll), ll]), lo - 0.978 * ls)
print('  lam ~ 0.5 band (%d primes; log lam range %.3f, log symR range %.2f):' % (len(q4), ll.max() - ll.min(), ls.max() - ls.min()))
print('     free symR slope within the band %.3f +- %.3f (fit 0.978); with the slope fixed, lam coefficient %.2f +- %.2f (fit 1.932)' % (
    c1[1], e1[1], c2[1], e2[1]))
s3877 = sym(3877); o3877 = RR[3877]['N1mu1']
for nm, f in (('3877 x (symR/symR_3877)^0.978, no lam term', lambda p: o3877 * (sym(p) / s3877) ** 0.978),
              ('3877 value, no symR slope', lambda p: o3877)):
    v = np.array([math.log(R[p]['N1mu1'] / f(p)) for p in q4])
    print('     anchored model "%s": rms %.3f mean %+.3f' % (nm, math.sqrt((v ** 2).mean()), v.mean()))
i13 = [p for p in sorted(ins) if p != 3877]
X13 = np.array([[1, math.log(sym(p)), math.log(lam(p))] for p in i13]); c13 = np.linalg.lstsq(X13, np.log([obsN[p] for p in i13]), rcond=None)[0]
print('  fit without 3877: %+.3f %+.3f log symR %+.3f log lam' % tuple(c13))
for nm, ps in grp.items():
    v = np.array([math.log(R[p]['N1mu1']) - c13 @ [1, math.log(sym(p)), math.log(lam(p))] for p in ps])
    print('     %-13s mean error %+.2f (factor %.1f), rms %.2f' % (nm, v.mean(), math.exp(v.mean()), math.sqrt((v ** 2).mean())))

# ---------------------------------------------------------------- 10. post hoc and Part B values
print('\n10. Post hoc counts and the values quoted in Parts A and B')
big = [p for p in PS if R[p]['D'] > 2]
n1 = sum(R[p]['cls'] == 1 for p in PS)
print('  B_D > 2: %s; all class 1: %s; P(all %d in class 1 | %d of %d) = %.4f' % (
    big, all(R[p]['cls'] == 1 for p in big), len(big), n1, len(PS), math.comb(n1, len(big)) / math.comb(len(PS), len(big))))
for nm, T in (('the 70', T70), ('strict 66', T66)):
    bt = [p for p in T if R[p]['D'] > 2]; m1 = sum(R[p]['cls'] == 1 for p in T)
    print('     in %s: %s; P = C(%d,%d)/C(%d,%d) = %.3f' % (nm, bt, m1, len(bt), len(T), len(bt), math.comb(m1, len(bt)) / math.comb(len(T), len(bt))))
print('  largest class-7 B_D: %.2f (%d)' % (max(R[p]['D'] for p in PS if R[p]['cls'] == 7), max((p for p in PS if R[p]['cls'] == 7), key=lambda p: R[p]['D'])))
print('  sN without sD or sPW: %s' % [(p, R[p]['cls']) for p in PS if R[p]['sN'] and not (R[p]['sD'] or R[p]['sPW'])])
print('  1951: N1/mu1 %.3f against 2 x band-3 median %.3f' % (R[1951]['N1mu1'], 2 * MED['3']['N1mu1']))
low = [p for p in PS if R[p]['lam'] <= 0.31]
for c in (1, 7):
    s = [p for p in low if R[p]['cls'] == c]
    print('  lam <= 0.31 class %d: %d primes, median N1/mu1 %.3f, median B_D %.3f' % (c, len(s), np.median([R[p]['N1mu1'] for p in s]),
                                                                                   np.median([R[p]['D'] for p in s])))
r = R[2347]; print('  2347 seed 13: B_L %.3f B_D %.3f PW %.3f N1/mu1 %.3f (seed 11: %.3f / %.3f / %.3f / %.3f)' % (
    r['L'], r['D'], r['PW'], r['N1mu1'], RR[2347]['L'], RR[2347]['D'], RR[2347]['PW'], RR[2347]['N1mu1']))
print('  largest B_D / PW by lambda group: lam <= 0.25 %.2f / %.2f; band 3 %.2f / %.2f; band 4 %.2f / %.2f' % tuple(
    f(R[p][q] for p in PS if R[p]['band'] in g) for g in (('1', '2'), ('3',), ('4',)) for f, q in ((max, 'D'), (max, 'PW'))))

# ---------------------------------------------------------------- 11. the symR slope by band (post hoc)
print('\n11. symR against N1/mu1 within each band (all band primes, seed-13 values; OLS of log N1/mu1 on log symR)')
for bn in BN:
    q = [p for p in PS if R[p]['band'] == bn]
    x = np.log([sym(p) for p in q]); y = np.log([R[p]['N1mu1'] for p in q])
    c, e = ols(np.column_stack([np.ones_like(x), x]), y)
    print('  band %s: %2d primes, sd log symR %.2f, sd log N1/mu1 %.2f, Spearman %.2f, slope %.2f +- %.2f, residual sd %.2f' % (
        bn, len(q), x.std(ddof=1), y.std(ddof=1), ks.spearman(x, y), c[1], e[1], (y - np.column_stack([np.ones_like(x), x]) @ c).std(ddof=2)))
q = [p for p in PS if R[p]['band'] == '4']
x = np.log([sym(p) for p in q]); z = np.log([lam(p) for p in q]); y = np.log([R[p]['N1mu1'] for p in q])
c, e = ols(np.column_stack([np.ones_like(x), x, z]), y)
print('  band 4 joint fit: slope symR %.2f +- %.2f, lam coefficient %.2f +- %.2f' % (c[1], e[1], c[2], e[2]))
print('  prediction errors by class and band (mean log error, n):')
for nm, ps in grp.items():
    a1 = [err[p] for p in ps if R[p]['cls'] == 1]; a7 = [err[p] for p in ps if R[p]['cls'] == 7]
    print('     %-13s class 1 %+.3f (%d)  class 7 %+.3f (%d)' % (nm, np.mean(a1), len(a1), np.mean(a7), len(a7)))
e1 = [err[p] for p in err if R[p]['cls'] == 1]; e7 = [err[p] for p in err if R[p]['cls'] == 7]
print('  two-sided MW p (all 74) %.5f; band-stratified permutation p (class 7 errors > class 1) %.4f' % (
    mannwhitneyu(e1, e7).pvalue, 1 - strat(list(err), err.get)))
print('  B_D class shift after adjusting for symR (per-band OLS of log max(B_D, 0.02) on log symR), stratified p all 89 / 70 / 66:')
rs = {}
for bn in BN:
    q = [p for p in PS if R[p]['band'] == bn]
    x = np.log([sym(p) for p in q]); y = np.log([max(R[p]['D'], 0.02) for p in q])
    A = np.column_stack([np.ones_like(x), x]); cf_ = np.linalg.lstsq(A, y, rcond=None)[0]
    for p, e_ in zip(q, y - A @ cf_): rs[p] = e_
    print('     band %s: slope %.2f' % (bn, cf_[1]))
print('     B_D residual given symR      %.4f / %.4f / %.4f' % (strat(PS, rs.get), strat(T70, rs.get), strat(T66, rs.get)))
conf_per_S = {int(w[0]): float(w[2]) for w in (l.split() for l in open('survey/sym_rate_k6.out')) if w and w[0].isdigit()}
print('  symR sample per prime (configurations found in the 10^5 symmetric S): band 1 %d-%d, band 4 %d-%d' % tuple(
    f(1e5 * conf_per_S[p] for p in PS if R[p]['band'] == bn) for bn in ('1', '4') for f in (min, max)))
