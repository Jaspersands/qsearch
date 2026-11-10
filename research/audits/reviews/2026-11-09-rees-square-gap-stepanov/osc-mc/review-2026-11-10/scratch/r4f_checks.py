"""Referee round 4f (10 Nov): scoring of mechanical item 2 (F over the kappa = 6 survey, lambda <= 0.25) against
osc-mc/survey/predictions_F.txt.  Own code for the shares, N1/mu1, F, the arithmetic columns (pow-based, no primitive
root), the rank statistics, the survey reproduction (npz arrays, not log lines), and how much of F2/F3/F5/F7 was fixed
by data known before the runs.  Nothing imported from score_F.py.
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4f_checks.py > r4f_checks.out"""
import os, re, math, itertools
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
os.chdir(OSC)
rng = np.random.default_rng(4)
OLD = {1597, 1621, 1657, 1789}; SD = {1597, 1657, 1669, 1693, 1789, 1933}
PR = [1531, 1543, 1549, 1567, 1579, 1597, 1609, 1621, 1627, 1657, 1663, 1669, 1693, 1699, 1723, 1741, 1747, 1753,
      1759, 1777, 1783, 1789, 1801, 1831, 1861, 1867, 1873, 1879, 1933]
R22 = 45 ** 2 * 6 ** 4


def rank(x):
    x = np.asarray(x, float); o = np.argsort(x, kind='mergesort'); r = np.empty(len(x)); r[o] = np.arange(len(x))
    for v in np.unique(x):
        m = x == v; r[m] = r[m].mean()
    return r


def sp(x, y): return float(np.corrcoef(rank(x), rank(y))[0, 1])


def arith(p):
    h = 0 if p % 12 == 1 else (3 if p % 12 == 7 else None)
    cube2 = pow(2, (p - 1) // 3, p) == 1
    a = [s for s in range(-int(math.isqrt(p)), int(math.isqrt(p)) + 1) if s % 3 == 1 and (p - s * s) % 3 == 0
         and (p - s * s) >= 0 and math.isqrt((p - s * s) // 3) ** 2 == (p - s * s) // 3]
    e = (p - 1) // 6; x = np.arange(1, p - 1, dtype=object)
    c0 = np.array([pow(int(v), e, p) for v in range(1, p)])          # chi_6(v) as v^((p-1)/6)
    six = c0 == 1; tgt = 1 if h == 0 else p - 1                         # class 0: sixth powers; class 3: v^e = -1
    A0h = int(np.sum(six[:p - 2] & (c0[1:p - 1] == tgt)))              # x in 1..p-2 sixth power, x+1 in class h
    t = (A0h - (p - 2) / 36) / math.sqrt(p)
    return h, cube2, a, t


out = {}
for line in open('survey/score_F.out'):
    w = line.split()
    if w and w[0].isdigit() and len(w) > 12:
        out[int(w[0])] = dict(N=float(w[2]), share=float(w[3]), F=float(w[5]),
                              h=int(w[8]), cube2=w[9] == 'y', ar=float(w[10]), t=float(w[11]), sym=float(w[12]))
print('1. Reproduction, shares, F and arithmetic by my code (largest |difference| against score_F.out)')
rows = []; bad = []
for p in PR:
    pre = 'split/split_k6_p%d' % p if p in OLD else 'split/split13_k6_p%d' % p
    A, S, U = (np.load('%s_%s.npz' % (pre, q)) for q in ('all', 'str', 'uns'))
    sv = np.load('survey/mc_k6_p%d_s13.npz' % p)
    rep = (int(A['nS']) == int(sv['nS']) and np.array_equal(A['cnt'], sv['cnt']) and np.allclose(A['S1'], sv['S1'], rtol=1e-9, atol=1e-9)
           and np.allclose(A['S2'], sv['S2'], rtol=1e-9) and float(A['N1']) == float(sv['N1']))
    add = np.allclose(A['S1'], S['S1'] + U['S1'], atol=1e-6) and np.array_equal(A['cnt'], S['cnt'] + U['cnt'])
    share = S['cnt'].sum() / A['cnt'].sum(); N = float(A['N1']) / float(A['mu1']); F = share * N * p * p / R22
    h, c2, a, t = arith(p)
    rows.append(dict(p=p, lam=p / 6 ** 5, share=share, N=N, F=F, h=h, cube2=c2, ar=abs(a[0]) / math.sqrt(p), t=t,
                     new=p not in OLD, rep=rep, add=add, F1=N * p * p / R22, sym=out[p]['sym'], na=len(a)))
    o = out[p]
    bad.append((abs(round(share, 3) - o['share']), abs(round(F, 2) - o['F']), abs(round(N, 2) - o['N']), h != o['h'],
                c2 != o['cube2'], abs(round(abs(a[0]) / math.sqrt(p), 3) - o['ar']), abs(round(t, 3) - o['t'])))
b = np.array(bad, float)
print('  survey npz reproduced array by array (nS, cnt, S1, S2, N1) at %d of 29; parts add up at %d of 29; unique a at %d of 29' % (
    sum(r['rep'] for r in rows), sum(r['add'] for r in rows), sum(r['na'] == 1 for r in rows)))
print('  max |diff| (rounded as printed): share %.3f, F %.2f, N1/mu1 %.2f, h mismatches %d, cube2 mismatches %d, |a|/rp %.3f, t %.3f' % tuple(b.max(0)))
new = [r for r in rows if r['new']]; c = lambda q, rr: np.array([x[q] for x in rr], float)
print('\n2. Predictions, own statistics, scope as written')
print('  (F1) over 25: share range %.3f-%.3f, below 0.60: %s' % (c('share', new).min(), c('share', new).max(), [r['p'] for r in new if r['share'] < 0.60]))
print('  (F2) max new F %.2f (%d); overall max %.2f (%d)' % (c('F', new).max(), max(new, key=lambda r: r['F'])['p'], c('F', rows).max(), max(rows, key=lambda r: r['F'])['p']))
s3, s4, s5 = sp(c('F', new), c('N', new)), sp(c('share', new), c('N', new)), sp((1 - c('share', new)) * c('N', new), c('N', new))
print('  (F3) %.3f  (F4) %.3f  (F5) %.3f over 25' % (s3, s4, s5))
h0 = [r for r in rows if r['h'] == 0]
cub = [r['F'] for r in h0 if r['cube2']]; ncb = [r['F'] for r in h0 if not r['cube2']]
print('  (F7) over 29: Spearman(F, |a|/rp) %.3f; h = 0: median F cube %.2f (n %d) vs %.2f (n %d); Spearman(F, |t|) at h = 0 %.3f (n %d)' % (
    sp(c('F', rows), c('ar', rows)), np.median(cub), len(cub), np.median(ncb), len(ncb), sp(c('F', h0), np.abs(c('t', h0))), len(h0)))

print('\n3. What was fixed before the runs (survey N1/mu1 at all 29 was known)')
print('  (F2) F at share 1 (the most any share can give) among the 25 new: max %.2f (%d) -> F2 could not fail: %s' % (
    c('F1', new).max(), max(new, key=lambda r: r['F1'])['p'], c('F1', new).max() <= 4.0))
Nn, shn, p2 = c('N', new), c('share', new), c('p', new) ** 2
print('  (F3) with any constant share, Spearman(F, N1/mu1) = Spearman(N p^2, N) = %.3f' % sp(Nn * p2, Nn))
perm = np.array([[sp(np.r_[pp] * Nn * p2, Nn), sp((1 - np.r_[pp]) * Nn, Nn)] for pp in (rng.permutation(shn) for _ in range(20000))])
print('  shares permuted among the 25 (no share-N link): Spearman(F, N) median %.3f, P(>= 0.90) %.3f, min %.3f; '
      'Spearman((1-share)N, N) median %.3f, P(>= 0.5) %.3f, min %.3f' % (np.median(perm[:, 0]), (perm[:, 0] >= 0.9).mean(), perm[:, 0].min(),
                                                                    np.median(perm[:, 1]), (perm[:, 1] >= 0.5).mean(), perm[:, 1].min()))
lv = lambda x: np.var(np.log(x))
print('  var of log over the 25: N1/mu1 %.3f, share %.4f, p^2 %.4f, F %.3f; cov(log share, log N) %.4f' % (
    lv(Nn), lv(shn), lv(p2), lv(c('F', new)), np.cov(np.log(shn), np.log(Nn))[0, 1]))
for nm, y in (('2+2 count share N', shn * Nn), ('rest count (1-share) N', (1 - shn) * Nn), ('share', shn)):
    sl = np.polyfit(np.log(Nn), np.log(y), 1)[0]
    bs = [np.polyfit(np.log(Nn[i]), np.log(y[i]), 1)[0] for i in (rng.integers(0, 25, 25) for _ in range(4000))]
    print('  elasticity d log(%s)/d log N1/mu1 over 25: %.3f (bootstrap 95%% %.3f-%.3f)' % (nm, sl, *np.percentile(bs, [2.5, 97.5])))
F08 = 0.8 * c('N', rows) * c('p', rows) ** 2 / R22
print('  (F7) with F at share 0.8 (known before): Spearman(F08, |a|/rp) %.3f; h = 0 medians cube %.2f vs %.2f; Spearman(F08, |t|) at h = 0 %.3f' % (
    sp(F08, c('ar', rows)), np.median([F08[i] for i, r in enumerate(rows) if r['h'] == 0 and r['cube2']]),
    np.median([F08[i] for i, r in enumerate(rows) if r['h'] == 0 and not r['cube2']]),
    sp([F08[i] for i, r in enumerate(rows) if r['h'] == 0], np.abs(c('t', h0)))))
print('  same with N1/mu1 alone: Spearman(N, |a|/rp) %.3f; Spearman(N, |t|) at h = 0 %.3f; Spearman(F, symR) %.3f vs Spearman(N, symR) %.3f' % (
    sp(c('N', rows), c('ar', rows)), sp(c('N', h0), np.abs(c('t', h0))), sp(c('F', rows), c('sym', rows)), sp(c('N', rows), c('sym', rows))))
# exact permutation p for the cube split at h = 0
fh = np.array([r['F'] for r in h0]); cb = np.array([r['cube2'] for r in h0]); obs = np.median(fh[cb]) - np.median(fh[~cb])
cnt = tot = 0
for comb in itertools.combinations(range(len(h0)), int(cb.sum())):
    m = np.zeros(len(h0), bool); m[list(comb)] = True; tot += 1; cnt += np.median(fh[m]) - np.median(fh[~m]) >= obs - 1e-12
print('  (F7) cube split at h = 0: exact one-sided permutation p for the median difference %.3f (%d splits)' % (cnt / tot, tot))

print('\n4. The exploratory share-by-class result, and lambda')
sh, lam, hh = c('share', rows), c('lam', rows), np.array([r['h'] for r in rows])
print('  Spearman(share, lambda) over 29: %.3f; class counts h=0 by band (<0.22, >=0.22): %d, %d; h=3: %d, %d' % (
    sp(sh, lam), ((hh == 0) & (lam < 0.22)).sum(), ((hh == 0) & (lam >= 0.22)).sum(), ((hh == 3) & (lam < 0.22)).sum(), ((hh == 3) & (lam >= 0.22)).sum()))
def mwp(x, y, n=20000):
    z = np.r_[x, y]; U = lambda a, b: sum((u > v) + 0.5 * (u == v) for u in a for v in b); u0 = U(x, y)
    return u0, np.mean([U(*(lambda q: (q[:len(x)], q[len(x):]))(rng.permutation(z))) >= u0 for _ in range(n)])
for nm, m in (('all', np.ones(29, bool)), ('lam < 0.22', lam < 0.22), ('lam >= 0.22', lam >= 0.22)):
    x, y = sh[m & (hh == 0)], sh[m & (hh == 3)]
    u0, pv = mwp(x, y, 5000)
    print('  %-12s share median h=0 %.3f (n %d) vs h=3 %.3f (n %d); one-sided permutation MW p %.4f' % (nm, np.median(x), len(x), np.median(y), len(y), pv))
res = sh - np.polyval(np.polyfit(lam, sh, 1), lam)
u0, pv = mwp(res[hh == 0], res[hh == 3], 5000)
print('  share detrended linearly in lambda: h=0 vs h=3 one-sided permutation MW p %.4f' % pv)
print('  Spearman(share, symR) %.3f; Spearman(share, N1/mu1) over 29 %.3f; partial (share, N | lambda) by rank residuals %.3f' % (
    sp(sh, c('sym', rows)), sp(sh, c('N', rows)),
    float(np.corrcoef(rank(sh) - np.polyval(np.polyfit(rank(lam), rank(sh), 1), rank(lam)),
                      rank(c('N', rows)) - np.polyval(np.polyfit(rank(lam), rank(c('N', rows)), 1), rank(lam)))[0, 1])))
