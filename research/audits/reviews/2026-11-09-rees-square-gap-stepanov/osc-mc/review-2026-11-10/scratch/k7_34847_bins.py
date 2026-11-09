"""kappa = 7 at lambda ~ 0.3: per-L-bin values and robustness at 34847 (median symR; run after its scoring rule was
written), against 36037 and 35099.  Same cross-batch estimator as k6_spike_survey.analyse: X = (sum G - tr G)/(B(B-1)),
G[b,b'] = sum_cells w2 Re V_b conj V_b'.  Per bin: w-rms sqrt(X/W) with jackknife z, and 2-sigma ends sqrt((X +- 2se)/W).
For B_L: leave-one-out range, worst leave-two-out, half-sample (8 of 16) range, share of positive per-batch y_b.
Ratios 36037/x: central, and 36037's 2-sigma low end over x's 2-sigma high end.
Usage: nice -n 19 python -I k7_34847_bins.py <34847 npz> <35099 npz> <36037 npz>"""
import sys, math, itertools
import numpy as np

BINS = ((2, 2), (0, 3), (2, 3), (3, 3), (0, 4), (2, 4))


def load(f):
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    cnt = d['cnt'].astype(float); Vb = d['S1'] / cnt[:, None, None]
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    ow = orb * np.abs(P[:, rb]); w2 = np.outer(ow, ow)
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    m = {'L': (two & (ms <= 6)) | one}
    for a, b in BINS:
        m['(%d,%d)' % (a, b)] = ((supp[:, None] == a) & (supp[None, :] == b)) | ((supp[:, None] == b) & (supp[None, :] == a))
    out = {'p': p, 'N': int(cnt.sum())}
    for g, mm in m.items():
        A = Vb[:, mm] * np.sqrt(w2[mm])[None, :]; G = (A @ A.conj().T).real; B = len(G); W = w2[mm].sum()
        X = lambda idx: (G[np.ix_(idx, idx)].sum() - np.trace(G[np.ix_(idx, idx)])) / (len(idx) * (len(idx) - 1))
        full = X(list(range(B))); loo = np.array([X([i for i in range(B) if i != t]) for t in range(B)])
        se = math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum()); v = lambda x: math.sqrt(max(x, 0) / W)
        r = dict(val=v(full), z=full / se, lo=v(full - 2 * se), hi=v(full + 2 * se))
        if g == 'L':
            y = (G.sum(1) - np.diag(G)) / (B - 1)
            r.update(loo=(v(loo.min()), v(loo.max())), l2o=min(v(X([i for i in range(B) if i not in c])) for c in itertools.combinations(range(B), 2)),
                     half=[v(X(list(c))) for c in itertools.combinations(range(B), B // 2)], ypos=int((y > 0).sum()))
        out[g] = r
    return out


R = [load(f) for f in sys.argv[1:4]]
for r in R:
    L = r['L']
    print('%d (%d conf): B_L %.3f (z %.1f, 2sig %.3f-%.3f); y_b > 0 in %d of 16; leave-one-out %.3f-%.3f; worst leave-two-out %.3f; half-samples %.3f-%.3f (5/50/95%% %.3f/%.3f/%.3f)' % (
        r['p'], r['N'], L['val'], L['z'], L['lo'], L['hi'], L['ypos'], *L['loo'], L['l2o'], min(L['half']), max(L['half']), *np.percentile(L['half'], [5, 50, 95])))
    print('   bins: ' + '  '.join('%s %.3f (z %.1f)' % (g, r[g]['val'], r[g]['z']) for g in r if g.startswith('(')))
a, b, c = R
for x in (a, b):
    print('36037 over %d: ' % x['p'] + '  '.join('%s %.1fx (>= %s)' % (g, c[g]['val'] / x[g]['val'] if x[g]['val'] else float('inf'),
          '%.1fx' % (c[g]['lo'] / x[g]['hi']) if x[g]['hi'] else 'inf') for g in ['L'] + ['(%d,%d)' % t for t in BINS]))
print('34847 over 35099: ' + '  '.join('%s %.2f' % (g, a[g]['val'] / b[g]['val'] if b[g]['val'] else float('nan')) for g in ['L', '(2,2)', '(0,3)']))
print('smallest 36037 half-sample over the largest half-sample at 34847 and 35099: %.2f, %.2f' % (min(c['L']['half']) / max(a['L']['half']), min(c['L']['half']) / max(b['L']['half'])))
