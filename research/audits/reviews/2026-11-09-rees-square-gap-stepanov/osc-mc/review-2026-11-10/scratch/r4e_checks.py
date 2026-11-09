"""Referee round 4e (10 Nov): scoring of the kappa = 7 run at 34847 (mc_classes.py 7 34847 6000 --seed 13) against
osc-mc/predictions_k7_p34847.txt.  Own Gram-matrix path for 34847, 35099 and 36037 (functions as in r4d_checks.py),
checked against k6_spike_survey.analyse; seed-13 stream synchronisation and batch correlations across the three primes;
the kappa = 6 calibration read with two comparison primes.
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4e_checks.py > r4e_checks.out"""
import os, sys, glob, math, itertools
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
SP = '/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
os.chdir(OSC); sys.path.insert(0, OSC)
KEYS = ('k', 'p', 'S1', 'cnt', 'S2', 'supp', 'orb', 'P', 'rb', 'N1', 'mu1', 'Nunl', 'nS')


def load(f):
    d = np.load(f); return {x: d[x] for x in KEYS}


def masks(supp):
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    m = {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}
    for a, b2 in ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4)):
        m[(a, b2)] = ((supp[:, None] == a) & (supp[None, :] == b2)) | ((supp[:, None] == b2) & (supp[None, :] == a))
    return m


def gram2(V1, V2, w2, m):
    A1 = V1[:, m] * np.sqrt(w2[m])[None, :]; A2 = V2[:, m] * np.sqrt(w2[m])[None, :]
    return (A1 @ A2.conj().T).real


def Xof(G, idx=None):
    if idx is not None: G = G[np.ix_(idx, idx)]
    b = len(G); return (G.sum() - np.trace(G)) / (b * (b - 1))


def jkse(fn, B):
    loo = np.array([fn(np.delete(np.arange(B), t)) for t in range(B)])
    return math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum()), loo


def weights(d):
    ow = d['orb'] * np.abs(d['P'][:, int(d['rb'])]); return np.outer(ow, ow)


def noise(d, w2, m):
    N = d['cnt'].sum(); Vh = d['S1'].sum(0) / N
    sig2 = np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0)
    return (w2[m] * sig2[m]).sum() / float(d['Nunl'])


def stat(V, w2, m, nz, unit=1.0):
    G = gram2(V, V, w2, m); B = len(G); W = w2[m].sum(); X = Xof(G)
    se, loo = jkse(lambda idx: Xof(G, idx), B); s = X - nz
    f = lambda x: math.sqrt(max(x, 0) / W) / unit
    return dict(G=G, X=X, se=se, s=s, z=s / se, val=f(s), lo=f(s - 2 * se), hi=f(s + 2 * se), f=f, nz=nz, loo=loo)


F = {34847: SP + '/mc_k7_p34847_s13.npz', 35099: SP + '/mc_k7_p35099_s13.npz', 36037: 'mc_k7_p36037_s13.npz'}
D = {p: load(f) for p, f in F.items()}
print('1. Files and B_L, B_D by my path')
same = all(np.array_equal(D[p][x], D[34847][x]) for p in D for x in ('P', 'orb', 'supp', 'rb'))
print('  same P, orb, supp, rb at the three primes: %s' % same)
R = {}
for p, d in D.items():
    k = int(d['k']); B = len(d['cnt']); w2 = weights(d); M = masks(d['supp']); V = d['S1'] / d['cnt'][:, None, None]
    rL = stat(V, w2, M['L'], noise(d, w2, M['L'])); rD = stat(V, w2, M['D'], noise(d, w2, M['D']), k * k / p)
    G = rL['G']; y = (G.sum(1) - np.diag(G)) / (B - 1)
    loo = [rL['f'](x - rL['nz']) for x in rL['loo']]
    l2o = min(rL['f'](Xof(G, [i for i in range(B) if i not in c]) - rL['nz']) for c in itertools.combinations(range(B), 2))
    hv = np.array([rL['f'](Xof(G, list(c)) - rL['nz']) for c in itertools.combinations(range(B), B // 2)])
    R[p] = dict(L=rL, D=rD, y=y, hv=hv, V=V, w2=w2, M=M, d=d)
    print('  %d: conf %d, nS %d, S-batched (cnt spread %d-%d), N1/mu1 %.3f | B_L %.3f (z %.1f, 2sig %.3f-%.3f) | B_D %.2f (z %.1f, < %.2f)' % (
        p, int(d['cnt'].sum()), int(d['nS']), int(d['cnt'].min()), int(d['cnt'].max()), float(d['N1']) / float(d['mu1']),
        rL['val'], rL['z'], rL['lo'], rL['hi'], rD['val'], rD['z'], rD['hi']))
    print('         y_b > 0 in %d/16, top-2 share %.2f; leave-one-out %.3f-%.3f; worst leave-two-out %.3f; half-samples %.3f-%.3f (5/50/95%% %.3f/%.3f/%.3f)' % (
        (y > 0).sum(), np.sort(y)[::-1][:2].sum() / y.sum(), min(loo), max(loo), l2o, hv.min(), hv.max(), *np.percentile(hv, [5, 50, 95])))
a, b = R[34847]['L'], R[36037]['L']
rat = b['val'] / a['val']; rel = math.hypot(1 / (2 * a['z']), 1 / (2 * b['z']))
print('  36037/34847 %.3f; delta method 2sig %.2f-%.2f; ends %.2f-%.2f; 34847/35099 %.3f; 36037 min half-sample / 34847 max %.2f, / 35099 max %.2f' % (
    rat, rat * (1 - 2 * rel), rat * (1 + 2 * rel), b['lo'] / a['hi'], b['hi'] / a['lo'], a['val'] / R[35099]['L']['val'],
    R[36037]['hv'].min() / R[34847]['hv'].max(), R[36037]['hv'].min() / R[35099]['hv'].max()))
BL, lo, hi = a['val'], a['lo'], a['hi']
call = 'SPIKE' if (BL <= 0.41 and hi < 0.535) else ('NOT SHOWN' if BL >= 0.43 else 'INCONCLUSIVE')
print('  rule: B_L <= 0.41: %s; 2sig upper %.3f < 0.535: %s; call %s; close (range crosses 0.41 or 0.43): %s; prediction 0.20-0.32: %s' % (
    BL <= 0.41, hi, hi < 0.535, call, (lo <= 0.41 <= hi) or (lo <= 0.43 <= hi), 0.20 <= BL <= 0.32))
import k6_spike_survey as ks
for p in D:
    r = ks.analyse(F[p])
    print('  ks.analyse %d: B_L %.4f (mine %.4f), z %.2f (%.2f), lo %.4f (%.4f), hi %.4f (%.4f); B_D %.3f (%.3f); PW_pair %.3f floor %.3f CS %.3f; N1/mu1 se %.3f' % (
        p, r['L'], R[p]['L']['val'], r['L_z'], R[p]['L']['z'], r['L_lo'], R[p]['L']['lo'], r['L_hi'], R[p]['L']['hi'], r['D'], R[p]['D']['val'],
        r['PW'], r['PW_floor'], r['PW_cs'], r['N1mu1_se']))

print('\n2. L bins (w-rms |V|, no noise subtraction), 36037 over 34847 and over 35099: central, and 36037 lo / other hi')
for kk in ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4)):
    s = {p: stat(R[p]['V'], R[p]['w2'], R[p]['M'][kk], 0.0) for p in D}
    out = []
    for q in (34847, 35099):
        c = s[36037]['val'] / s[q]['val'] if s[q]['val'] > 0 else float('inf')
        out.append('/%d %s (>= %.1fx)' % (q, '%.1fx' % c if c < 1e3 else 'inf', s[36037]['lo'] / s[q]['hi']))
    print('  %s: 34847 %.3f (z %.1f) | 35099 %.3f (z %.1f) | 36037 %.3f (z %.1f) | %s' % (
        kk, s[34847]['val'], s[34847]['z'], s[35099]['val'], s[35099]['z'], s[36037]['val'], s[36037]['z'], '  '.join(out)))

print('\n3. Seed 13 at all three primes: are the runs correlated?')
for p in D:
    rng = np.random.default_rng(13)
    print('  %d: first three S / p: %s' % (p, ' | '.join(' '.join('%.4f' % x for x in np.sort(rng.choice(p, 7, replace=False)) / p) for _ in range(3))))
ps = list(D)
for i, j in ((0, 1), (0, 2), (1, 2)):
    p, q = ps[i], ps[j]
    cc = np.corrcoef(D[p]['cnt'], D[q]['cnt'])[0, 1]; cy = np.corrcoef(R[p]['y'], R[q]['y'])[0, 1]
    m = R[p]['M']['L']; w = np.sqrt(R[p]['w2'][m])
    dp = (R[p]['V'][:, m] - R[p]['V'][:, m].mean(0)) * w; dq = (R[q]['V'][:, m] - R[q]['V'][:, m].mean(0)) * w
    rho = lambda sh: (dp * np.roll(dq, sh, axis=0).conj()).real.sum() / math.sqrt((np.abs(dp) ** 2).sum() * (np.abs(dq) ** 2).sum())
    null = np.array([rho(t) for t in range(1, 16)])
    print('  %d-%d: corr of batch counts %.2f, of y_b %.2f (null sd 1/sqrt(15) = 0.26); cell-level rho of batch deviations %.3f '
          '(cyclic-shift null: mean %.3f, sd %.3f, max |rho| %.3f)' % (p, q, cc, cy, rho(0), null.mean(), null.std(), np.abs(null).max()))

print('\n4. kappa = 6 calibration read with two comparison primes (flags and bands as in r4c_checks.py)')
RR = {}
for f in sorted(glob.glob('survey/mc_k6_p*_s13.npz')):
    r = ks.analyse(f); RR[r['p']] = r
BANDS = [('1', 0.19, 0.22), ('2', 0.22, 0.2501), ('3', 0.2501, 0.31), ('4', 0.49, 0.56)]
allu, close_pairs, npairs = [], 0, 0
for bn, lo_, hi_ in BANDS:
    q = [p for p in RR if lo_ <= RR[p]['lam'] < hi_]
    med = {x: float(np.median([RR[p][x] for p in q])) for x in ('L', 'D', 'PW', 'N1mu1')}
    fl = {p for p in q if RR[p]['D_lo'] > 2 * med['D'] or RR[p]['PW'] > 2 * med['PW'] or RR[p]['N1mu1'] > 2 * med['N1mu1']}
    u = [RR[p]['L'] / med['L'] for p in q if p not in fl]; allu += u
    medu = float(np.median([RR[p]['L'] for p in q if p not in fl]))
    for x, y_ in itertools.combinations(u, 2):
        npairs += 1; close_pairs += max(x, y_) / min(x, y_) <= 0.245 / 0.237
    print('  band %s: all-prime median %.3f, unflagged median %.3f (ratio %.3f)' % (bn, med['L'], medu, med['L'] / medu))
au = np.array(allu)
print('  %d unflagged ratios; unflagged pairs within a band at most %.3fx apart: %d of %d (%.2f)' % (len(au), 0.245 / 0.237, close_pairs, npairs, close_pairs / npairs))
for Mx, nm in ((1.54, 'all-band unflagged max 1.54'), (1.46, 'band-3 unflagged max 1.46')):
    for b36, bn36 in ((0.635, 'central'), (0.535, '2sig low end')):
        m = b36 / Mx; r35, r34 = 0.237 / m, 0.245 / m
        f35, f34 = (au <= r35).mean(), (au <= r34).mean()
        print('  36037 %s (%.3f) at the %s needs a kappa = 7 median >= %.3f: 35099 at %.3f and 34847 at %.3f of it; '
              'kappa = 6 unflagged fractions at or below: %.3f, %.3f; product %.4f' % (bn36, b36, nm, m, r35, r34, f35, f34, f35 * f34))
