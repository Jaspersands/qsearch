"""Referee round 4k-b part 2 (11 Nov): the 34259 split (mc_split.py 7 34259 6000 --seed 19), by my own Gram path
(functions from r4d_checks.py).  Reproduction against the band run, Q1, Q2, decomposition, the 41-configuration batch,
and the comparison numbers, with 36037's split for like-for-like.
Run:  nice -n 19 /opt/anaconda3/bin/python -I r4kb2_checks.py > r4kb2_checks.out"""
import math, itertools
import numpy as np
SPN = '/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
SPO = '/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
KEYS = ('k', 'p', 'S1', 'cnt', 'S2', 'supp', 'orb', 'P', 'rb', 'N1', 'mu1', 'Nunl', 'nS')
def load(f):
    d = np.load(f); return {x: d[x] for x in KEYS}
def masks(supp):
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    return {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}
def gram2(V1, V2, w2, m):
    A1 = V1[:, m] * np.sqrt(w2[m])[None, :]; A2 = V2[:, m] * np.sqrt(w2[m])[None, :]; return (A1 @ A2.conj().T).real
def Xof(G, idx=None):
    if idx is not None: G = G[np.ix_(idx, idx)]
    b = len(G); return (G.sum() - np.trace(G)) / (b * (b - 1))
def jkse(fn, B):
    loo = np.array([fn(np.delete(np.arange(B), t)) for t in range(B)])
    return math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum()), loo
def weights(d):
    ow = d['orb'] * np.abs(d['P'][:, int(d['rb'])]); return np.outer(ow, ow)
def noise(d, w2, m, scale=1.0, idx=None):
    if idx is None: idx = np.arange(len(d['cnt']))
    N = d['cnt'].sum(); Vh = d['S1'].sum(0) / N
    return scale ** 2 * (w2[m] * np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0)[m]).sum() / float(d['Nunl'])
def stat(V, w2, m, nz, idx=None):
    G = gram2(V, V, w2, m)
    if idx is not None: G = G[np.ix_(idx, idx)]
    B = len(G); W = w2[m].sum(); X = Xof(G); se, _ = jkse(lambda i: Xof(G, i), B); s = X - nz
    f = lambda x: math.sqrt(max(x, 0) / W)
    return dict(G=G, X=X, se=se, z=s / se, val=f(s), lo=f(s - 2 * se), hi=f(s + 2 * se), f=f, nz=nz)

def analyse_split(p, base):
    sp = {q: load('%s_%s.npz' % (base, q)) for q in ('all', 'str', 'uns')}
    A, S_, U = sp['all'], sp['str'], sp['uns']; B = len(A['cnt'])
    w2 = weights(A); M = masks(A['supp'])
    Vown = {q: sp[q]['S1'] / sp[q]['cnt'][:, None, None] for q in sp}; Vc = {q: sp[q]['S1'] / A['cnt'][:, None, None] for q in sp}
    out = dict(sp=sp, w2=w2, M=M, Vown=Vown, Vc=Vc, B=B)
    out['addup'] = (np.abs(A['S1'] - S_['S1'] - U['S1']).max() / np.abs(A['S1']).max(), np.array_equal(A['cnt'], S_['cnt'] + U['cnt']))
    out['all'] = stat(Vown['all'], w2, M['L'], noise(A, w2, M['L']))
    out['uns'] = stat(Vown['uns'], w2, M['L'], noise(U, w2, M['L']))
    out['str'] = stat(Vown['str'], w2, M['L'], noise(S_, w2, M['L']))
    out['unsc'] = stat(Vc['uns'], w2, M['L'], noise(U, w2, M['L'], U['cnt'].sum() / A['cnt'].sum()))
    def parts(idx=None):
        Gs = gram2(Vc['str'], Vc['str'], w2, M['L']); Gu = gram2(Vc['uns'], Vc['uns'], w2, M['L']); Gx = gram2(Vc['str'], Vc['uns'], w2, M['L'])
        Ga = gram2(Vc['all'], Vc['all'], w2, M['L'])
        return Xof(Gs, idx), Xof(Gu, idx), Xof(Gx + Gx.T, idx), Xof(Ga, idx)
    out['parts'] = parts
    return out

R = analyse_split(34259, SPN + '/split_k7_p34259')
A, S_, U = R['sp']['all'], R['sp']['str'], R['sp']['uns']; B = R['B']
band = load(SPO + '/mc_k7_p34259_s19.npz')
print('1. Reproduction and files')
print('  parts add up: S1 rel diff %.1e, cnt %s.  split all vs band run: cnt equal %s, S1 max rel diff %.1e, S2 %.1e, nS %d vs %d, same P/orb/supp/rb %s' % (
    R['addup'][0], R['addup'][1], np.array_equal(A['cnt'], band['cnt']), np.abs(A['S1'] - band['S1']).max() / np.abs(band['S1']).max(),
    np.abs(A['S2'] - band['S2']).max() / np.abs(band['S2']).max(), int(A['nS']), int(band['nS']),
    all(np.array_equal(A[x], band[x]) for x in ('P', 'orb', 'supp', 'rb'))))
for q in ('all', 'uns', 'str', 'unsc'):
    r = R[q]; print('  B_L %-4s %.3f (z %.1f; 2sig %.3f-%.3f)' % (q, r['val'], r['z'], r['lo'], r['hi']))
u = R['uns']
q1 = 'REST-LIFTED' if (u['val'] >= 0.45 and u['lo'] > 0.270) else ('REST-TYPICAL' if (u['val'] <= 0.33 and u['hi'] < 0.45) else 'INCONCLUSIVE')
close = (u['lo'] <= 0.33 <= u['hi']) or (u['lo'] <= 0.45 <= u['hi'])
print('  Q1: %s%s' % (q1, ' (close)' if close else ''))
sc = S_['cnt']; ac = A['cnt']; sh = sc.sum() / ac.sum()
se_jk, _ = jkse(lambda i: sc[i].sum() / ac[i].sum(), B); se_bin = math.sqrt(sh * (1 - sh) / ac.sum())
print('  per-batch 2+2 counts %s; batch totals %s' % (' '.join(str(int(c)) for c in sc), ' '.join(str(int(c)) for c in ac)))
print('  Q2: share %.4f; binomial se %.4f -> %.4f-%.4f; jackknife (ratio) se %.4f -> %.4f-%.4f; TYPICAL under both: %s' % (
    sh, se_bin, sh - 2 * se_bin, sh + 2 * se_bin, se_jk, sh - 2 * se_jk, sh + 2 * se_jk,
    not (sh + 2 * se_bin < 0.011 or sh - 2 * se_bin > 0.043) and not (sh + 2 * se_jk < 0.011 or sh - 2 * se_jk > 0.043)))
p = 34259; R22 = 105 ** 2 * 7 ** 4 / p ** 2; n1 = float(A['N1']) / float(A['mu1'])
print('  R22 %.4f, G %.2f, F %.2f' % (R22, sh / R22, sh / R22 * n1))
ib = int(np.argmax(sc)); keep = [i for i in range(B) if i != ib]
sh2 = sc[keep].sum() / ac[keep].sum(); se2, _ = jkse(lambda i: sc[keep][i].sum() / ac[keep][i].sum(), B - 1)
chi = ((sc - ac * sh) ** 2 / (ac * sh * (1 - sh))).sum()
print('\n3. The large batch (index %d, %d of %d configurations): dispersion chi2 %.1f on 15 df; without it share %.4f (jackknife se %.4f), G %.2f' % (
    ib, int(sc[ib]), int(ac[ib]), chi, sh2, se2, sh2 / R22))
for q in ('all', 'uns', 'str'):
    d = R['sp'][q]; r = stat(R['Vown'][q], R['w2'], R['M']['L'], noise(d, R['w2'], R['M']['L']), idx=keep)
    print('  without it: B_L %-4s %.3f (z %.1f; 2sig %.3f-%.3f)' % (q, r['val'], r['z'], r['lo'], r['hi']))
G = u['G']; y = (G.sum(1) - np.diag(G)) / (B - 1)
hv = np.array([u['f'](Xof(G, list(c)) - u['nz']) for c in itertools.combinations(range(B), B // 2)])
print('  uns: y_b > 0 in %d/16; large batch row mean rank %d of 16; half-samples min/5/50/95%% %.3f/%.3f/%.3f/%.3f' % (
    (y > 0).sum(), 1 + int((y > y[ib]).sum()), hv.min(), *np.percentile(hv, [5, 50, 95])))
xs, xu, xx, xa = R['parts']()
se = [jkse(lambda i, j=j: R['parts'](i)[j] / R['parts'](i)[3], B)[0] for j in range(3)]
print('\n2. Decomposition of X_L(all): 2+2 alone %.3f (se %.3f), rest alone %.3f (se %.3f), cross %.3f (se %.3f); sum check %.1e; cos %.2f' % (
    xs / xa, se[0], xu / xa, se[1], xx / xa, se[2], (xa - xs - xu - xx) / xa, xx / (2 * math.sqrt(xs * xu))))
print('  B_L all %.3f; rest contribution scale %.3f (-%.1f%%); rest own scale %.3f (-%.1f%%)' % (
    R['all']['val'], R['unsc']['val'], 100 * (1 - R['unsc']['val'] / R['all']['val']), u['val'], 100 * (1 - u['val'] / R['all']['val'])))
R6 = analyse_split(36037, SPO + '/split_k7_p36037')
xs6, xu6, xx6, xa6 = R6['parts']()
print('  36037 like for like: B_L all %.3f; rest contribution %.3f (-%.1f%%); rest own %.3f (-%.1f%%); 2+2 alone %.3f, cross %.3f' % (
    R6['all']['val'], R6['unsc']['val'], 100 * (1 - R6['unsc']['val'] / R6['all']['val']), R6['uns']['val'], 100 * (1 - R6['uns']['val'] / R6['all']['val']),
    xs6 / xa6, xx6 / xa6))
d35 = load(SPO + '/mc_k7_p35099_s13.npz'); w35 = weights(d35); M35 = masks(d35['supp'])
r35 = stat(d35['S1'] / d35['cnt'][:, None, None], w35, M35['L'], noise(d35, w35, M35['L']))
print('\n4. Comparisons for the rest (own scale %.3f, 2sig %.3f-%.3f)' % (u['val'], u['lo'], u['hi']))
print('  35099 whole %.3f (%.3f-%.3f): central %.2fx, ends %.2fx' % (r35['val'], r35['lo'], r35['hi'], u['val'] / r35['val'], u['lo'] / r35['hi']))
for nm, v, lo, hi in (('band median', 0.245, None, None), ('35281 whole', 0.392, 0.373, 0.410), ('36541 whole', 0.393, 0.366, 0.419), ('36037 rest', 0.573, 0.478, 0.654)):
    print('  %-12s %.3f: central %.2fx%s' % (nm, v, u['val'] / v, '' if hi is None else ', ends %.2fx (rest low / their high), %.2fx (rest high / their low)' % (u['lo'] / hi, u['hi'] / lo)))
# delta-method 2-sigma for the ratio rest/35099: var(ln B) = (se/(2 s))^2
zr = math.sqrt((1 / (2 * u['z'])) ** 2 + (1 / (2 * r35['z'])) ** 2)
print('  delta-method ratio rest/35099: %.2f, 2-sigma %.2f-%.2f' % (u['val'] / r35['val'], u['val'] / r35['val'] * math.exp(-2 * zr), u['val'] / r35['val'] * math.exp(2 * zr)))
