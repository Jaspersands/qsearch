"""Referee round 4d (10 Nov): the 2+2 / not-2+2 split of the kappa = 7 run at 36037 (mc_split.py 7 36037 6000 --seed 13,
the first 6000 configurations of mc_k7_p36037_s13.npz), against 35099 (unsplit) and the full 36037 run.
Own Gram-matrix path; nothing is imported from split36037_decomp.py or k6_spike_survey.py.
  own scale:          V_q,b = S1_q,b / cnt_q,b         (class values averaged over the part's own configurations)
  contribution scale: c_q,b = S1_q,b / cnt_all,b       (the part's contribution to the whole-run batch mean)
X = (sum_{b != b'} G[b,b'])/(B(B-1)), G[b,b'] = sum_cells w2 Re(V_b conj V_b'); for c_all = c_str + c_uns the cross-batch
X splits exactly into X(c_str) + X(c_uns) + X(cross).  B = sqrt(max(X - noise, 0)/W_group).
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4d_checks.py > r4d_checks.out"""
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
    sv = sorted(set(supp.tolist()))
    for a in sv:
        for b2 in sv:
            if b2 < a or (a == 0 and b2 <= 2): continue
            mm = ((supp[:, None] == a) & (supp[None, :] == b2)) | ((supp[:, None] == b2) & (supp[None, :] == a))
            if mm.any(): m[(a, b2)] = mm
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


def noise(d, w2, m, scale=1.0):
    N = d['cnt'].sum(); Vh = d['S1'].sum(0) / N
    sig2 = np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0)
    return scale ** 2 * (w2[m] * sig2[m]).sum() / float(d['Nunl'])


def stat(V, w2, m, nz, unit=1.0):
    G = gram2(V, V, w2, m); B = len(G); W = w2[m].sum(); X = Xof(G)
    se, loo = jkse(lambda idx: Xof(G, idx), B); s = X - nz
    f = lambda x: math.sqrt(max(x, 0) / W) / unit
    return dict(G=G, X=X, se=se, s=s, z=s / se, val=f(s), lo=f(s - 2 * se), hi=f(s + 2 * se), f=f, nz=nz, W=W)


sp = {q: load('%s/split_k7_p36037_%s.npz' % (SP, q)) for q in ('all', 'str', 'uns')}
full = load('mc_k7_p36037_s13.npz'); d35 = load(SP + '/mc_k7_p35099_s13.npz')
A, S_, U = sp['all'], sp['str'], sp['uns']
k, p = int(A['k']), int(A['p']); B = len(A['cnt'])
print('1. Files')
print('  split parts add up: max|S1_all - S1_str - S1_uns| = %.1e (max|S1_all| %.1e); cnt %s; S2 %.1e; same P, orb, supp, rb: %s' % (
    np.abs(A['S1'] - S_['S1'] - U['S1']).max(), np.abs(A['S1']).max(), np.array_equal(A['cnt'], S_['cnt'] + U['cnt']),
    np.abs(A['S2'] - S_['S2'] - U['S2']).max() / np.abs(A['S2']).max(),
    all(np.array_equal(A[x], q[x]) for q in (S_, U, full) for x in ('P', 'orb', 'supp', 'rb'))))
print('  prefix: split nS %d vs full %d; split batch counts <= full in every batch: %s; split all %d, str %d (per batch %d-%d), uns %d' % (
    int(A['nS']), int(full['nS']), bool((A['cnt'] <= full['cnt']).all()), int(A['cnt'].sum()), int(S_['cnt'].sum()),
    int(S_['cnt'].min()), int(S_['cnt'].max()), int(U['cnt'].sum())))
sh = S_['cnt'].sum() / A['cnt'].sum()
se_sh, _ = jkse(lambda idx: S_['cnt'][idx].sum() / A['cnt'][idx].sum(), B)
n1 = float(A['N1']) / float(A['mu1']); n1f = float(full['N1']) / float(full['mu1'])
R22 = 105 ** 2 * 7 ** 4 / p ** 2
print('  2+2 share %.4f (jackknife se %.4f; sd of batch shares / sqrt(16) %.4f); N1/mu1 split %.3f, full %.3f; R22 = 105^2 7^4/p^2 = %.4f' % (
    sh, se_sh, (S_['cnt'] / A['cnt']).std(ddof=1) / math.sqrt(B), n1, n1f, R22))
print('  F = share N1/mu1 / R22 = %.2f (%.2f with the full-run N1/mu1), +- %.2f from the share; pairsym 0.045 x 1.08 / R22 = %.2f' % (
    sh * n1 / R22, sh * n1f / R22, se_sh * n1 / R22, 0.045 * 1.08 / R22))

w2 = weights(A); M = masks(A['supp'])
Vown = {q: sp[q]['S1'] / sp[q]['cnt'][:, None, None] for q in sp}
Vc = {q: sp[q]['S1'] / A['cnt'][:, None, None] for q in sp}
Vfull = full['S1'] / full['cnt'][:, None, None]; V35 = d35['S1'] / d35['cnt'][:, None, None]; w35 = weights(d35); M35 = masks(d35['supp'])
print('\n2. B_L (absolute units): value (z, 2-sigma), noise share of X')
res = {}
for nm, V, d, ww, mm, scale in (('36037 full run', Vfull, full, w2, M, 1.0), ('split all', Vown['all'], A, w2, M, 1.0),
                                ('uns, own scale', Vown['uns'], U, w2, M, 1.0), ('uns, contribution', Vc['uns'], U, w2, M, U['cnt'].sum() / A['cnt'].sum()),
                                ('str, own scale', Vown['str'], S_, w2, M, 1.0), ('str, contribution', Vc['str'], S_, w2, M, sh),
                                ('35099 (unsplit)', V35, d35, w35, M35, 1.0)):
    r = stat(V, ww, mm['L'], noise(d, ww, mm['L'], scale)); res[nm] = r
    print('  %-18s %.3f (z %.1f, %.3f-%.3f)  noise/X %.1e' % (nm, r['val'], r['z'], r['lo'], r['hi'], r['nz'] / r['X']))
ru, r35 = res['uns, own scale'], res['35099 (unsplit)']
print('  uns own scale / 35099: central %.2f; 2-sigma ends %.2f.  uns contribution / 35099: central %.2f; 2-sigma ends %.2f' % (
    ru['val'] / r35['val'], ru['lo'] / r35['hi'], res['uns, contribution']['val'] / r35['val'], res['uns, contribution']['lo'] / r35['hi']))
G = ru['G']; y = (G.sum(1) - np.diag(G)) / (B - 1)
hv = np.array([ru['f'](Xof(G, list(c)) - ru['nz']) for c in itertools.combinations(range(B), B // 2)])
l2o = min(ru['f'](Xof(G, [i for i in range(B) if i not in c]) - ru['nz']) for c in itertools.combinations(range(B), 2))
print('  uns own scale: y_b > 0 in %d/16, top-2 share %.2f; worst leave-two-out %.3f; half-samples min/5/50/95%% %.3f/%.3f/%.3f/%.3f (35099 max half-sample 0.304)' % (
    (y > 0).sum(), np.sort(y)[::-1][:2].sum() / y.sum(), l2o, hv.min(), *np.percentile(hv, [5, 50, 95])))

print('\n3. Exact split of X_L(all) on the contribution scale (split run)')
def parts(idx=None, m=M['L']):
    Gs = gram2(Vc['str'], Vc['str'], w2, m); Gu = gram2(Vc['uns'], Vc['uns'], w2, m); Gx = gram2(Vc['str'], Vc['uns'], w2, m)
    Ga = gram2(Vc['all'], Vc['all'], w2, m)
    xs, xu, xx, xa = Xof(Gs, idx), Xof(Gu, idx), Xof(Gx + Gx.T, idx), Xof(Ga, idx)
    return xs, xu, xx, xa
xs, xu, xx, xa = parts()
print('  X(all) - [X(str) + X(uns) + cross] = %.1e of X(all)' % ((xa - xs - xu - xx) / xa))
for i, nm in enumerate(('2+2 only', 'rest only', 'cross')):
    se_i, _ = jkse(lambda idx: parts(idx)[i] / parts(idx)[3], B)
    print('  %-9s %.3f of X(all)  (jackknife se %.3f)' % (nm, (xs, xu, xx)[i] / xa, se_i))
se_t, _ = jkse(lambda idx: (parts(idx)[0] + parts(idx)[2]) / parts(idx)[3], B)
print('  2+2 total (alone + cross) %.3f (se %.3f); alignment cos = cross/(2 sqrt(X_str X_uns)) = %.2f' % ((xs + xx) / xa, se_t, xx / (2 * math.sqrt(xs * xu))))
print('  amplitude: B_L(all) %.3f, rest contribution %.3f, so the 2+2 part adds %.3f' % (
    res['split all']['val'], res['uns, contribution']['val'], res['split all']['val'] - res['uns, contribution']['val']))
xsD, xuD, xxD, xaD = parts(m=M['D'])
print('  D group, same split: 2+2 only %.2f, rest only %.2f, cross %.2f of X_D(all)' % (xsD / xaD, xuD / xaD, xxD / xaD))

print('\n4. L bins: rest (uns, own scale) at 36037 against 35099 (whole run); w-rms |V| (z), 2-sigma ends; shares of the bin X(all)')
for kk in [x for x in M if isinstance(x, tuple) and ((x[0] == 0 and x[1] >= 3) or (x[0] >= 2 and sum(x) <= 6))]:
    u = stat(Vown['uns'], w2, M[kk], 0.0); a = stat(Vown['all'], w2, M[kk], 0.0); s = stat(V35, w35, M35[kk], 0.0)
    xs_, xu_, xx_, xa_ = parts(m=M[kk])
    rc = u['val'] / s['val'] if s['val'] > 0 else float('inf'); rl = u['lo'] / s['hi']
    print('  %s: rest %.4f (z %.1f, lo %.4f) | split all %.4f (z %.1f) | 35099 %.4f (z %.1f, hi %.4f) | rest/35099 %s, ends %.1fx | '
          'bin X(all): rest only %.2f, 2+2 only %.2f, cross %.2f' % (kk, u['val'], u['z'], u['lo'], a['val'], a['z'], s['val'], s['z'], s['hi'],
                                                                     '%.1fx' % rc if rc < 1e3 else 'inf', rl, xu_ / xa_, xs_ / xa_, xx_ / xa_))

print('\n5. Could an unsplit 2+2 part at 35099 close the gap?  Minkowski on the weighted L2 norm over L cells:')
print('   B_rest(35099) <= (B_all(35099) + s B_str,own(35099)) / (1 - s); B_all(35099) at its 2-sigma upper end 0.264')
bs = res['str, own scale']
print('   36037 own-scale B_str = %.2f (z %.1f, 2-sigma upper %.2f); alignment with the rest at 36037: cos %.2f (positive: the 2+2 part adds)' % (
    bs['val'], bs['z'], bs['hi'], xx / (2 * math.sqrt(xs * xu))))
for s in (0.0076, 0.011, 0.026):
    for tgt, tn in ((ru['lo'], "36037 rest's 2-sigma low end"), (ru['val'] / 1.54, '36037 rest / 1.54')):
        need = (tgt * (1 - s) - r35['hi']) / s
        print('   s = %.4f: to reach %.3f (%s) needs B_str,own(35099) >= %.1f, i.e. %.1fx 36037\'s own-scale value, and anti-aligned' % (
            s, tgt, tn, need, need / bs['val']))

print('\n6. D group (units k^2/p): B_D by part, and the split shares with jackknife se')
kp2 = k * k / p
for nm, V, d, scale in (('split all', Vown['all'], A, 1.0), ('uns, own scale', Vown['uns'], U, 1.0), ('str, own scale', Vown['str'], S_, 1.0)):
    r = stat(V, w2, M['D'], noise(d, w2, M['D'], scale), kp2)
    print('  %-15s B_D %.2f (z %.1f, < %.2f)' % (nm, r['val'], r['z'], r['hi']))
for i, nm in enumerate(('2+2 only', 'rest only', 'cross')):
    se_i, _ = jkse(lambda idx: parts(idx, M['D'])[i] / parts(idx, M['D'])[3], B)
    print('  %-9s %.2f of X_D(all) (jackknife se %.2f)' % (nm, (xsD, xuD, xxD)[i] / xaD, se_i))
