"""Referee scratch: robustness of the claim-1 fit (survey/predict_n1.py) and of the claim-3 part comparison.
Run from osc-mc."""
import sys, glob, re, math
import numpy as np
sys.path.insert(0, '.')

sym = {}
for line in open('survey/sym_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): sym[int(w[0])] = (float(w[1]), float(w[3]))
meas = {}; src = {}
for f in glob.glob('survey/mc_k6_p*_s13.log') + ['mc_k6_p1933.log', 'mc_k6_p2347.log', 'mc_k6_p3877_sb.log', 'mc_k6_p4219.log', 'mc_k6_p3571.log']:
    try:
        for line in open(f):
            m = re.search(r'p=(\d+) lambda=([\d.]+) S=(\d+) conf=(\d+).*N1/mu1=([\d.]+)', line)
            if m: meas[int(m.group(1))] = float(m.group(5)); src[int(m.group(1))] = f
    except FileNotFoundError: pass

fit14 = [1531, 1543, 1549, 1567, 1579, 1597, 1609, 1621, 1627, 1657, 1663, 1669, 1693, 3877]   # the author's fit set
row = lambda q: [1, math.log(sym[q][1]), math.log(sym[q][0])]


def fit(qs, cols=(0, 1, 2)):
    X = np.array([[row(q)[c] for c in cols] for q in qs]); y = np.log([meas[q] for q in qs])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None); return coef, y - X @ coef


def pred(coef, q, cols=(0, 1, 2)):
    return float(np.exp(np.array([row(q)[c] for c in cols]) @ coef))


coef, r = fit(fit14)
print('author fit reproduced: a %.3f b %.3f c %.3f  residual sd %.3f (np.std, ddof 0); ddof=3: %.3f' % (*coef, r.std(), math.sqrt((r ** 2).sum() / (len(r) - 3))))
print('  largest residuals: ' + ', '.join('%d %+.2f' % (q, v) for q, v in sorted(zip(fit14, r), key=lambda t: -abs(t[1]))[:3]))
oos = [q for q in meas if q in sym and q not in fit14]
print('  out of sample (measured / predicted, log error): ' + '  '.join('%d %.2f/%.2f %+.2f' % (q, meas[q], pred(coef, q), math.log(meas[q] / pred(coef, q))) for q in sorted(oos)))
# leave-one-out
loo = []
for q in fit14:
    c2, _ = fit([t for t in fit14 if t != q]); loo.append((q, math.log(meas[q] / pred(c2, q)), c2[2]))
print('  leave-one-out log errors: ' + ' '.join('%d:%+.2f' % (q, e) for q, e, _ in loo) + '   (rms %.3f)' % math.sqrt(np.mean([e * e for _, e, _ in loo])))
print('  lambda coefficient when 3877 is left out: %.2f (log lambda range of the other 13: %.3f)' % (
    [c for q, e, c in loo if q == 3877][0], max(row(q)[2] for q in fit14 if q != 3877) - min(row(q)[2] for q in fit14 if q != 3877)))
# fit on the 13 low-lambda primes with a fixed slope 1 in log symR (one parameter)
low = [q for q in fit14 if q != 3877]
off = np.log([meas[q] / sym[q][1] for q in low])
print('  low-lambda primes: log(N1/mu1 / symR) mean %.3f sd %.3f (n=%d) -> N1/mu1 = %.4f symR' % (off.mean(), off.std(ddof=1), len(low), math.exp(off.mean())))
# Spearman with bootstrap
def spear(x, y):
    rk = lambda v: np.argsort(np.argsort(v)); return float(np.corrcoef(rk(np.asarray(x)), rk(np.asarray(y)))[0, 1])
sv = [q for q in meas if q in sym and 'survey' in src[q]]
x = [sym[q][1] for q in sv]; y = [meas[q] for q in sv]
rng = np.random.default_rng(0); bs = []
for _ in range(4000):
    idx = rng.integers(0, len(sv), len(sv))
    if len(set(idx)) > 3: bs.append(spear([x[i] for i in idx], [y[i] for i in idx]))
print('Spearman symR vs N1/mu1 over %d survey primes: %.3f (bootstrap 2.5-97.5%%: %.2f-%.2f)' % (len(sv), spear(x, y), *np.percentile(bs, [2.5, 97.5])))

# block_rate ratio vs N1/mu1
blk = {}
for line in open('blocks/block_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): blk[int(w[0])] = float(w[2])
bq = [q for q in blk if q in meas]
print('block_rate ratio vs N1/mu1: Spearman %.2f over %d primes: %s' % (spear([blk[q] for q in bq], [meas[q] for q in bq]), len(bq),
      ' '.join('%d:%.3f/%.2f' % (q, blk[q], meas[q]) for q in sorted(bq, key=lambda q: meas[q]))))

# claim 3: alignment of the structured and unstructured class values over the D and L groups
import k6_spike_survey as ks
for pre in ('split/split_k6_p1597', 'split/split_k6_p1657', 'split/split_k6_p1933'):
    d = {q: np.load('%s_%s.npz' % (pre, q)) for q in ('all', 'str', 'uns')}
    supp = d['all']['supp']; orb = d['all']['orb']; P = d['all']['P']; rb = int(d['all']['rb'])
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    G = ks.groups(6, supp)
    V = {q: d[q]['S1'].sum(0) / d[q]['cnt'].sum() for q in d}
    sh = d['str']['cnt'].sum() / d['all']['cnt'].sum()
    out = []
    for g in ('L', 'D'):
        m = G[g]; a_, b_ = V['str'][m], V['uns'][m]; ww = w2[m]
        cos = (ww * (a_ * np.conj(b_))).sum().real / math.sqrt((ww * abs(a_) ** 2).sum() * (ww * abs(b_) ** 2).sum())
        rat = math.sqrt((ww * abs(b_) ** 2).sum() / (ww * abs(a_) ** 2).sum())
        # share of the total's weighted square carried by the uns part's contribution (1 - sh) V_uns
        fr = (ww * abs((1 - sh) * b_) ** 2).sum() / (ww * abs(V['all'][m]) ** 2).sum()
        out.append('%s: weighted cos(V_str, V_uns) %.2f, |V_uns|/|V_str| %.2f, |(1-sh)V_uns|^2/|V_all|^2 %.3f' % (g, cos, rat, fr))
    print('%s (structured share %.3f): ' % (pre, sh) + ';  '.join(out) + '   [raw MC means, not noise-subtracted]')
