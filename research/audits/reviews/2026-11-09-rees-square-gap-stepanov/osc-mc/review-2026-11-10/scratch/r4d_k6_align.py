"""Referee round 4d, supplement: is the 2+2 part ever anti-aligned with the rest?  Every finished kappa = 6 split
(split/split*_k6_p*_{all,str,uns}.npz) and the kappa = 7 split at 36037, on the contribution scale c_q,b = S1_q,b/cnt_all,b.
cos = X(cross)/(2 sqrt(X(str) X(uns))) per group (L, D), with the cross share of X(all) and its jackknife se.
Same Gram-matrix path as r4d_checks.py (functions copied, nothing imported).
Run:  nice -n 19 /opt/anaconda3/bin/python -I r4d_k6_align.py > r4d_k6_align.out"""
import os, glob, math
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
    return {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}


def gram2(V1, V2, w2, m):
    A1 = V1[:, m] * np.sqrt(w2[m])[None, :]; A2 = V2[:, m] * np.sqrt(w2[m])[None, :]
    return (A1 @ A2.conj().T).real


def Xof(G, idx=None):
    if idx is not None: G = G[np.ix_(idx, idx)]
    b = len(G); return (G.sum() - np.trace(G)) / (b * (b - 1))


def jkse(fn, B):
    loo = np.array([fn(np.delete(np.arange(B), t)) for t in range(B)])
    return math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum())


def weights(d):
    ow = d['orb'] * np.abs(d['P'][:, int(d['rb'])]); return np.outer(ow, ow)


runs = sorted(glob.glob('split/split*_k6_p*_all.npz')) + [SP + '/split_k7_p36037_all.npz']
print('run                    k  p      share   group  X(str)/X  X(uns)/X  cross/X (se)    cos     B_str/B_uns own scale')
for fa in runs:
    try:
        sp = {q: load(fa.replace('_all.npz', '_%s.npz' % q)) for q in ('all', 'str', 'uns')}
    except Exception as e:
        print('  skip %s: %s' % (fa, e)); continue
    A = sp['all']; B = len(A['cnt']); k, p = int(A['k']), int(A['p'])
    sh = sp['str']['cnt'].sum() / A['cnt'].sum()
    w2 = weights(A); M = masks(A['supp'])
    Vc = {q: sp[q]['S1'] / A['cnt'][:, None, None] for q in sp}
    Vo = {q: sp[q]['S1'] / np.maximum(sp[q]['cnt'], 1)[:, None, None] for q in sp}
    tag = os.path.basename(fa).replace('_all.npz', '')
    for g in ('L', 'D'):
        m = M[g]
        Gs, Gu, Gx = gram2(Vc['str'], Vc['str'], w2, m), gram2(Vc['uns'], Vc['uns'], w2, m), gram2(Vc['str'], Vc['uns'], w2, m)
        Ga = gram2(Vc['all'], Vc['all'], w2, m)
        xs, xu, xx, xa = Xof(Gs), Xof(Gu), Xof(Gx + Gx.T), Xof(Ga)
        se = jkse(lambda idx: Xof(Gx + Gx.T, idx) / Xof(Ga, idx), B)
        cos = xx / (2 * math.sqrt(xs * xu)) if xs > 0 and xu > 0 else float('nan')
        bo_s = math.sqrt(max(Xof(gram2(Vo['str'], Vo['str'], w2, m)), 0)); bo_u = math.sqrt(max(Xof(gram2(Vo['uns'], Vo['uns'], w2, m)), 0))
        print('%-22s %d %6d  %.3f   %s     %7.3f   %7.3f   %6.3f (%.3f)  %6.2f   %s' % (
            tag, k, p, sh, g, xs / xa, xu / xa, xx / xa, se, cos, '%.2f' % (bo_s / bo_u) if bo_u > 0 else 'inf'))
