"""Does the 2+2 part carry the B_L lift at 36037 (kappa = 7, lambda 0.306)?  Reads the mc_split.py run
(mc_split.py 7 36037 6000 --seed 13: the first 6000 of the 10^4 configurations of mc_k7_p36037_s13.npz) and,
for comparison, the equal-lambda typical prime 35099 (mc_classes.py 7 35099 6000 --seed 13).
Same cross-batch estimator as k6_spike_survey.analyse (X = (sum G - tr G)/(B(B-1)), G[b,b'] = sum_cells w2 Re V_b conj V_b').
Two views:
  (a) each part on its own scale, V_b = S1_part,b / cnt_part,b (what split_report.py prints);
  (b) contributions to the whole, c_q,b = S1_q,b / cnt_all,b, so V_all,b = c_str,b + c_uns,b exactly and
      X_all = X(str,str) + X(uns,uns) + 2 X(str,uns) exactly (bilinear; noise terms are < 1e-9 of X at kappa = 7).
Per L bin (a, b) and for the L group.  z is the jackknife z of each X.
Usage: nice -n 19 python -I split36037_decomp.py <split prefix> <35099 npz>"""
import sys, math
import numpy as np

pre, f35 = sys.argv[1], sys.argv[2]


def load(f):
    d = np.load(f)
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    ow = orb * np.abs(P[:, rb]); w2 = np.outer(ow, ow)
    return d, supp, w2


def masks(supp):
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    out = {'L': (two & (ms <= 6)) | one}
    for a, b in ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4)):
        out['(%d,%d)' % (a, b)] = ((supp[:, None] == a) & (supp[None, :] == b)) | ((supp[:, None] == b) & (supp[None, :] == a))
    return out


def Xpair(U, V, w2, m):
    """Unbiased cross-batch estimate of sum_m w2 Re(E U conj E V) and its jackknife se."""
    A = U[:, m] * np.sqrt(w2[m])[None, :]; C = V[:, m] * np.sqrt(w2[m])[None, :]
    G = (A @ C.conj().T).real; G = (G + G.T) / 2; B = len(G)
    X = lambda idx: (G[np.ix_(idx, idx)].sum() - np.trace(G[np.ix_(idx, idx)])) / (len(idx) * (len(idx) - 1))
    full = X(np.arange(B)); loo = np.array([X(np.delete(np.arange(B), t)) for t in range(B)])
    return full, math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum())


dA, supp, w2 = load(pre + '_all.npz'); dS, dU = np.load(pre + '_str.npz'), np.load(pre + '_uns.npz')
assert np.array_equal(dS['supp'], supp) and np.array_equal(dU['supp'], supp)
cA, cS, cU = (dd['cnt'].astype(float) for dd in (dA, dS, dU))
assert np.allclose(cS + cU, cA) and np.allclose(dS['S1'] + dU['S1'], dA['S1'])
B = len(cA); sh = cS.sum() / cA.sum()
own = {q: dd['S1'] / np.maximum(c, 1)[:, None, None] for q, dd, c in (('all', dA, cA), ('str', dS, cS), ('uns', dU, cU))}
con = {q: dd['S1'] / cA[:, None, None] for q, dd in (('str', dS), ('uns', dU))}
d35, supp35, w35 = load(f35)
V35 = d35['S1'] / d35['cnt'].astype(float)[:, None, None]
M, M35 = masks(supp), masks(supp35)
print('36037 split: %d configurations (%d 2+2, share %.4f; per-batch 2+2 counts %s)' % (cA.sum(), cS.sum(), sh, ' '.join('%d' % c for c in cS)))
print('(a) own-scale w-rms per part, z; 35099 whole for comparison.  (b) shares of X_all: str-str, uns-uns, 2 x cross.')
print('%-6s %-18s %-18s %-18s %-14s | %-8s %-8s %-8s  %s' % ('bin', 'all', '2+2', 'rest', '35099', 'ss', 'uu', '2su', 'rest/35099 (2sig low end of rest over high end of 35099)'))
for g, m in M.items():
    Wg = w2[m].sum(); row = {}
    for q in ('all', 'str', 'uns'):
        x, se = Xpair(own[q], own[q], w2, m); row[q] = (math.sqrt(max(x, 0) / Wg), x / se if se else 0, x, se)
    x35, se35 = Xpair(V35, V35, w35, M35[g]); W35 = w35[M35[g]].sum(); v35 = math.sqrt(max(x35, 0) / W35)
    hi35 = math.sqrt(max(x35 + 2 * se35, 0) / W35)
    ss, _ = Xpair(con['str'], con['str'], w2, m); uu, _ = Xpair(con['uns'], con['uns'], w2, m); su, _ = Xpair(con['str'], con['uns'], w2, m)
    tot = ss + uu + 2 * su
    xu, seu = row['uns'][2], row['uns'][3]; lou = math.sqrt(max(xu - 2 * seu, 0) / Wg)
    print('%-6s %7.3f (%5.1f)   %7.3f (%5.1f)   %7.3f (%5.1f)   %7.3f (%5.1f)  | %6.1f%%  %6.1f%%  %6.1f%%   %.2fx (>= %.2fx)' % (
        g, row['all'][0], row['all'][1], row['str'][0], row['str'][1], row['uns'][0], row['uns'][1], v35, x35 / se35,
        100 * ss / tot, 100 * uu / tot, 200 * su / tot, row['uns'][0] / v35 if v35 else float('inf'), lou / hi35 if hi35 else float('inf')))
print('Amplitude view for L: share x B_L(2+2) = %.3f, (1 - share) x B_L(rest) = %.3f; B_L(all) = %.3f' % (
    sh * math.sqrt(max(Xpair(own['str'], own['str'], w2, M['L'])[0], 0) / w2[M['L']].sum()),
    (1 - sh) * math.sqrt(max(Xpair(own['uns'], own['uns'], w2, M['L'])[0], 0) / w2[M['L']].sum()),
    math.sqrt(max(Xpair(own['all'], own['all'], w2, M['L'])[0], 0) / w2[M['L']].sum())))
