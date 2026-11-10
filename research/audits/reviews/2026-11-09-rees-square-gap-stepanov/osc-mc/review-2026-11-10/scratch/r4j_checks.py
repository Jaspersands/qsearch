"""Referee round 4j (10 Nov): scoring of mechanical item 6 (kappa = 7 band at lambda ~ 0.3), by my own Gram path
(functions as in r4hb_checks.py; not k6_spike_survey.analyse).  Per prime: B_L, z, 2-sigma ends, leave-one-batch-out
range, all C(16,8) half-sample B_L, positive row means, top-cell share of X_L, bin shares; then R1-R3 under the rule
text in both clause orders, and Spearman by hand.
Run:  nice -n 19 /opt/anaconda3/bin/python -I r4j_checks.py > r4j_checks.out"""
import os, math, itertools
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
SP = '/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
KEYS = ('k', 'p', 'S1', 'cnt', 'S2', 'supp', 'orb', 'P', 'rb', 'N1', 'mu1', 'Nunl', 'nS')
def load(f):
    d = np.load(f); out = {x: d[x] for x in KEYS}; out['files'] = list(d.files); return out
def maskL(supp):
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    return (two & (ms <= 6)) | one
def binmask(supp, a, b):
    return ((supp[:, None] == a) & (supp[None, :] == b)) | ((supp[:, None] == b) & (supp[None, :] == a))
def gram(V, w2, m):
    A = V[:, m] * np.sqrt(w2[m])[None, :]; return (A @ A.conj().T).real
def Xof(G, idx=None):
    if idx is not None: G = G[np.ix_(idx, idx)]
    b = len(G); return (G.sum() - np.trace(G)) / (b * (b - 1))
F = {34259: SP + '/mc_k7_p34259_s19.npz', 34273: SP + '/mc_k7_p34273_s21.npz', 34469: SP + '/mc_k7_p34469_s23.npz',
     34693: SP + '/split_k7_p34693_all.npz', 34847: SP + '/mc_k7_p34847_s13.npz', 35099: SP + '/mc_k7_p35099_s13.npz',
     35281: SP + '/mc_k7_p35281_s25.npz', 36037: OSC + '/mc_k7_p36037_s13.npz', 36541: SP + '/mc_k7_p36541_s27.npz'}
symR = {34259: 22.05, 34273: 9.43, 34469: 16.69, 35281: 15.79, 36541: 15.32, 35099: 21.33, 34847: 16.26, 36037: 44.19, 34693: 44.22}
R = {}
ref = None
print('p      conf  B_L    z     2sig          LOO range      half-samples (12870)  y_b>0  top cell  top-3   bins (2,2) (0,3) (2,3) (3,3) (0,4) (2,4)   N1/mu1')
for p, f in F.items():
    d = load(f)
    if ref is None: ref = d
    same = all(np.array_equal(d[x], ref[x]) for x in ('supp', 'orb', 'P', 'rb')) if d['P'].shape == ref['P'].shape else False
    ow = d['orb'] * np.abs(d['P'][:, int(d['rb'])]); w2 = np.outer(ow, ow); m = maskL(d['supp'])
    V = d['S1'] / np.maximum(d['cnt'], 1)[:, None, None]
    N = d['cnt'].sum(); Vh = d['S1'].sum(0) / N
    nz = (w2[m] * np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0)[m]).sum() / float(d['Nunl'])
    G = gram(V, w2, m); B = len(G); W = w2[m].sum(); X = Xof(G); s = X - nz
    loo = np.array([Xof(G, [i for i in range(B) if i != t]) for t in range(B)])
    se = math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum())
    fB = lambda x: math.sqrt(max(x, 0) / W)
    hv = np.array([fB(Xof(G, list(c)) - nz) for c in itertools.combinations(range(B), B // 2)])
    y = (G.sum(1) - np.diag(G)) / (B - 1)
    idx = np.argwhere(m); cont = []
    for i, j in idx:
        v = V[:, i, j]; cont.append(w2[i, j] * ((np.abs(v.sum()) ** 2 - (np.abs(v) ** 2).sum()) / (B * (B - 1))))
    cont = np.sort(np.array(cont))[::-1]; tot = cont.sum()
    bins = ' '.join('%5.2f' % (Xof(gram(V, w2, binmask(d['supp'], a, b))) / X) for a, b in ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4)))
    R[p] = dict(L=fB(s), lo=fB(s - 2 * se), hi=fB(s + 2 * se), z=s / se)
    print('%5d %5d  %.3f %5.1f  %.3f-%.3f  %.3f-%.3f    %.3f-%.3f (5-95%% %.3f-%.3f)  %2d/16  %.3f     %.3f   %s   %.3f%s' % (
        p, int(N), R[p]['L'], R[p]['z'], R[p]['lo'], R[p]['hi'], fB(loo.min() - nz), fB(loo.max() - nz), hv.min(), hv.max(),
        np.percentile(hv, 5), np.percentile(hv, 95), (y > 0).sum(), cont[0] / tot, cont[:3].sum() / tot, bins,
        float(d['N1']) / float(d['mu1']), '' if same else '  [different P/orb/supp/rb from 34259]'))
band = [34259, 34273, 34469, 35281, 36541, 35099, 34847]
BL = [R[q]['L'] for q in band]; med = float(np.median(BL)); maxhi = max(R[q]['hi'] for q in band)
a, b = R[36037], R[34693]
spike = a['lo'] > maxhi and a['L'] / med >= 1.54; notshown = any(x >= 0.50 for x in BL)
print('\nband median %.3f, range %.3f-%.3f, max 2sig upper %.3f (prime %d)' % (med, min(BL), max(BL), maxhi, max(band, key=lambda q: R[q]['hi'])))
print('R1: SPIKE conditions: lower %.3f > %.3f: %s; ratio %.2f >= 1.54: %s.  NOT SHOWN condition (a band point >= 0.50): %s.'
      '  Written order (SPIKE first) -> %s; scorer order (NOT SHOWN first) -> %s' % (
          a['lo'], maxhi, a['lo'] > maxhi, a['L'] / med, a['L'] / med >= 1.54, notshown,
          'SPIKE' if spike else ('NOT SHOWN' if notshown else 'INCONCLUSIVE'), 'NOT SHOWN' if notshown else ('SPIKE' if spike else 'INCONCLUSIVE')))
r1_no34259 = [q for q in band if q != 34259]; mh2 = max(R[q]['hi'] for q in r1_no34259); md2 = float(np.median([R[q]['L'] for q in r1_no34259]))
print('    sensitivity, band without 34259: max upper %.3f, median %.3f; 36037 lower > max upper %s, ratio %.2f' % (mh2, md2, a['lo'] > mh2, a['L'] / md2))
print('R2: ABOVE %s (lower %.3f vs %.3f); INSIDE %s (band points >= 0.387: %s)' % (
    b['lo'] > maxhi, b['lo'], maxhi, any(x >= 0.387 for x in BL), [q for q in band if R[q]['L'] >= 0.387]))
def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y)); n = len(x)
    return 1 - 6 * ((rx - ry) ** 2).sum() / (n * (n * n - 1))
nine = sorted(R)
print('R3: Spearman over nine %.3f; over band %.3f (no ties in symR or B_L)' % (
    spearman([symR[q] for q in nine], [R[q]['L'] for q in nine]), spearman([symR[q] for q in band], [R[q]['L'] for q in band])))
print('ratios to band median: ' + ', '.join('%d %.2f' % (q, R[q]['L'] / med) for q in sorted(R)))
