"""Referee round 4h-b (10 Nov): the kappa = 7 split at 34693 (mc_split.py 7 34693 6000 --seed 17).  Own Gram path
(functions as in r4e_checks.py).  Why is z(B_L) 34 here against 7-9 at the other kappa = 7 runs?  Per-bin and per-cell
decomposition of X_L, batch structure, robustness, against 34847, 35099 and 36037.
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4hb_checks.py > r4hb_checks.out"""
import os, math, itertools
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
SP = '/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
os.chdir(OSC)
KEYS = ('k', 'p', 'S1', 'cnt', 'S2', 'supp', 'orb', 'P', 'rb', 'N1', 'mu1', 'Nunl', 'nS')
def load(f):
    d = np.load(f); return {x: d[x] for x in KEYS}
def masks(supp):
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    m = {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}
    for a, b2 in ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4), (0, 5), (0, 6), (0, 7)):
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
    return (w2[m] * np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0)[m]).sum() / float(d['Nunl'])
def stat(V, w2, m, nz):
    G = gram2(V, V, w2, m); B = len(G); W = w2[m].sum(); X = Xof(G)
    se, loo = jkse(lambda idx: Xof(G, idx), B); s = X - nz
    f = lambda x: math.sqrt(max(x, 0) / W)
    return dict(G=G, X=X, se=se, s=s, z=s / se, val=f(s), lo=f(s - 2 * se), hi=f(s + 2 * se), f=f, nz=nz, W=W)
F = {'34693 all': SP + '/split_k7_p34693_all.npz', '34693 uns': SP + '/split_k7_p34693_uns.npz', '34693 str': SP + '/split_k7_p34693_str.npz',
     '34847': SP + '/mc_k7_p34847_s13.npz', '35099': SP + '/mc_k7_p35099_s13.npz', '36037': 'mc_k7_p36037_s13.npz'}
D = {q: load(f) for q, f in F.items()}
A = D['34693 all']
print('1. Files: parts add up %s; same P/orb/supp/rb as 34847 %s; nS %d; cnt per batch %d-%d (S-batched: spread > 1); str per batch %d-%d' % (
    np.allclose(A['S1'], D['34693 str']['S1'] + D['34693 uns']['S1']) and np.array_equal(A['cnt'], D['34693 str']['cnt'] + D['34693 uns']['cnt']),
    all(np.array_equal(A[x], D['34847'][x]) for x in ('P', 'orb', 'supp', 'rb')), int(A['nS']), A['cnt'].min(), A['cnt'].max(),
    D['34693 str']['cnt'].min(), D['34693 str']['cnt'].max()))
R = {}
print('\n2. B_L by my path; X, its jackknife se, and the share of X_L by bin')
for q, d in D.items():
    w2 = weights(d); M = masks(d['supp']); V = d['S1'] / np.maximum(d['cnt'], 1)[:, None, None]
    r = stat(V, w2, M['L'], noise(d, w2, M['L'])); R[q] = (r, V, w2, M)
    G = r['G']; B = len(G); y = (G.sum(1) - np.diag(G)) / (B - 1)
    hv = np.array([r['f'](Xof(G, list(c)) - r['nz']) for c in itertools.combinations(range(B), B // 2)])
    bins = ', '.join('%s %.2f' % (kk, Xof(gram2(V, V, w2, M[kk])) / r['X']) for kk in ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4), (0, 5), (0, 6), (0, 7)))
    print('  %-9s conf %5d: B_L %.3f (z %.1f, %.3f-%.3f); X %.3e se %.3e (se/X %.3f); y_b>0 %d/16, y_b cv %.2f; half-samples %.3f-%.3f\n            X shares: %s' % (
        q, int(d['cnt'].sum()), r['val'], r['z'], r['lo'], r['hi'], r['X'], r['se'], r['se'] / r['X'], (y > 0).sum(), y.std() / y.mean(), hv.min(), hv.max(), bins))
print('\n3. Bins (w-rms |V|, z), 34693 rest against the others')
for kk in ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4)):
    out = []
    for q in ('34693 uns', '34693 str', '34847', '35099', '36037'):
        r, V, w2, M = R[q]; s = stat(V, w2, M[kk], 0.0); out.append('%s %.3f (z %.1f)' % (q, s['val'], s['z']))
    print('  %s: %s' % (kk, ' | '.join(out)))
print('\n4. The cells carrying X_L: top 6 cells by contribution, with the between-batch cv of their weighted value')
for q in ('34693 uns', '34847', '36037'):
    r, V, w2, M = R[q]; m = M['L']; idx = np.argwhere(m)
    cont = []
    for i, j in idx:
        v = V[:, i, j]; Bn = len(v); c = w2[i, j] * ((np.abs(v.sum()) ** 2 - (np.abs(v) ** 2).sum()) / (Bn * (Bn - 1)))
        cont.append((c, i, j, abs(v.mean()), np.abs(v - v.mean()).std() / max(abs(v.mean()), 1e-300)))
    cont.sort(reverse=True); tot = sum(c[0] for c in cont)
    supp = D['34847']['supp']
    print('  %-9s: ' % q + '; '.join('cell (%d,%d) supp (%d,%d) %.2f of X, |V| %.3g, batch cv %.2f' % (i, j, supp[i], supp[j], c / tot, a, cv) for c, i, j, a, cv in cont[:6]))
print('\n5. The rule and ratios by my path')
u = R['34693 uns'][0]
call = 'LIFTED' if (u['val'] >= 0.40 and u['lo'] > 0.270) else ('LIKE' if (u['val'] <= 0.33 and u['hi'] < 0.478) else 'INCONCLUSIVE')
print('  rest B_L %.4f (%.4f-%.4f): call %s; close %s; whole %.4f; rest/0.241 %.2f; rest/0.573 %.2f; whole/36037 whole %.3f' % (
    u['val'], u['lo'], u['hi'], call, (u['lo'] <= 0.33 <= u['hi']) or (u['lo'] <= 0.40 <= u['hi']), R['34693 all'][0]['val'],
    u['val'] / 0.241, u['val'] / 0.573, R['34693 all'][0]['val'] / R['36037'][0]['val']))
sh = D['34693 str']['cnt'].sum() / A['cnt'].sum(); p = 34693; Rw = 105 ** 2 * 7 ** 4 / p ** 2
print('  share %.4f, R22 %.4f, G %.3f, F %.3f (N1/mu1 %.3f)' % (sh, Rw, sh / Rw, sh / Rw * float(A['N1']) / float(A['mu1']), float(A['N1']) / float(A['mu1'])))
for q in ('34693 all', '34693 uns', '34847', '36037'):
    r, V, w2, M = R[q]; d = D[q]; s = stat(V, w2, M['D'], noise(d, w2, M['D'])); kp2 = 49 / int(d['p'])
    print('  B_D %-9s %.2f (z %.1f, < %.2f) [k^2/p units]; X_D %.3e se %.3e noise %.3e' % (q, s['val'] / kp2, s['z'], s['hi'] / kp2, s['X'], s['se'], s['nz']))
