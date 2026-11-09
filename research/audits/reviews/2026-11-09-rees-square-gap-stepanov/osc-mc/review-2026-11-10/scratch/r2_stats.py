"""Referee round 2 (2026-11-10): look-elsewhere checks for SEC12_DRAFT.md section 12.7.

Part A: the h-class pattern (B_D > 2 only at p = 1 mod 12) on the survey table printed by k6_spike_survey.py
        (scratch/survey_out_r2.txt): hypergeometric probabilities, a permutation family-wise p over the residue
        partitions that the survey prints, and rank tests that need no cut.
Part B: the fixed-cell correlation of fixedcell.py: all 36 cells, permutation and bootstrap.
Run from osc-mc/:  nice -n 19 /opt/anaconda3/bin/python -I review-2026-11-10/scratch/r2_stats.py
"""
import sys, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from k6_spike_survey import spearman as sp_author

rng = np.random.default_rng(20261110)


from scipy.stats import rankdata


def rank(x):
    return rankdata(np.asarray(x, float))      # average ranks for ties


def spear(a, b):
    ra, rb = rank(a), rank(b); ra -= ra.mean(); rb -= rb.mean()
    return float((ra * rb).sum() / math.sqrt((ra * ra).sum() * (rb * rb).sum()))


# ---------------- Part A ----------------
surv, early = [], []
target = surv
for line in open('review-2026-11-10/scratch/survey_out_r2.txt'):
    if line.startswith('Earlier'): target = early; continue
    if line.startswith('Per band'): break
    seg = line.split('|')
    if len(seg) < 6: continue
    s0 = seg[0].split()
    if not s0 or not s0[0].isdigit(): continue
    s4 = seg[4].split()
    ind = tuple(int(x) for x in s4[2].split(','))
    target.append(dict(p=int(s0[0]), lam=float(s0[1]), N=float(s0[3]), BD=float(seg[2].split()[0]),
                       BL=float(seg[1].split()[0]), ind=ind, symR=float(seg[5].split()[0])))
print('Part A: %d survey primes parsed (+%d earlier rows)' % (len(surv), len(early)))


def parts(rows):
    I = np.array([r['ind'] for r in rows])          # ind(-1), ind(2), ind(3), ind(-3) mod 6
    return {'ind(-1)': I[:, 0], 'ind(2)%2': I[:, 1] % 2, 'ind(2)%3': I[:, 1] % 3, 'ind(2)%6': I[:, 1],
            'ind(3)%3': I[:, 2] % 3, 'ind(3)%6': I[:, 2], 'ind(-3)%6': I[:, 3]}


def hyp_tail(N, K, n, x):   # P(X >= x), X ~ Hypergeom(N, K, n)
    return sum(math.comb(K, j) * math.comb(N - K, n - j) for j in range(x, min(K, n) + 1)) / math.comb(N, n)


def min_p(top, P, n):
    best, arg = 1.0, None
    k = len(top)
    for nm, lab in P.items():
        for c in np.unique(lab):
            K = int((lab == c).sum()); x = int((lab[top] == c).sum())
            if x == 0: continue
            pv = hyp_tail(n, K, k, x)
            if pv < best: best, arg = pv, (nm, int(c), x, K)
    return best, arg


for label, rows in [('n=17 (02:16 snapshot)', [r for r in surv if r['p'] not in (1759, 1777, 1789)]), ('n=20 (now)', surv)]:
    n = len(rows); BD = np.array([r['BD'] for r in rows]); h = np.array([r['ind'][0] for r in rows])
    P = parts(rows); k = int((BD > 2).sum()); n0 = int((h == 0).sum()); n3 = n - n0
    top = np.argsort(-BD)[:k]
    print('\n%s: B_D > 2 at %s; h=0 class %d, h=3 class %d' % (label, [rows[i]['p'] for i in top], n0, n3))
    one = math.comb(n0, k) / math.comb(n, k); two = (math.comb(n0, k) + math.comb(n3, k)) / math.comb(n, k)
    print('  all %d in h=0: one-sided %.4f, either class %.4f, x4 symbols %.3f' % (k, one, two, 4 * one))
    obs, arg = min_p(top, P, n)
    # family-wise: random k-subsets as the B_D top set, min over all partitions and classes
    M = 100000; cnt = 0
    for _ in range(M):
        t = rng.choice(n, k, replace=False)
        if min_p(t, P, n)[0] <= obs + 1e-12: cnt += 1
    print('  min over partitions/classes p = %.4f at %s; permutation family-wise p = %.4f' % (obs, arg, cnt / M))
    # cut also chosen post hoc: min over top-k, k = 3..6
    obs_k = min(min_p(np.argsort(-BD)[:kk], P, n)[0] for kk in range(3, 7))
    cnt = 0; M2 = 20000
    for _ in range(M2):
        perm = rng.permutation(n)
        if min(min_p(perm[:kk], P, n)[0] for kk in range(3, 7)) <= obs_k + 1e-12: cnt += 1
    print('  with the cut free (top 3..6): min p %.4f, family-wise p = %.4f' % (obs_k, cnt / M2))
    # rank tests without a cut (two-sided permutation, difference of mean ranks)
    for nm in ('BD', 'N', 'BL', 'symR'):
        x = np.array([r[nm] for r in rows]); rx = rank(x); d0 = rx[h == 0].mean() - rx[h == 3].mean()
        U = sum((a > b) + 0.5 * (a == b) for a in x[h == 0] for b in x[h == 3])
        cnt = 0
        for _ in range(50000):
            hp = rng.permutation(h)
            if abs(rx[hp == 0].mean() - rx[hp == 3].mean()) >= abs(d0) - 1e-12: cnt += 1
        print('  %-5s by h: median %.2f vs %.2f;  U/(n0 n3) = %.3f;  two-sided permutation p = %.3f' % (
            nm, np.median(x[h == 0]), np.median(x[h == 3]), U / (n0 * n3), cnt / 50000))

# ---------------- Part B ----------------
rows = []
for line in open('survey/sym_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): rows.append((int(w[0]), float(w[1]), float(w[3])))
p = np.array([r[0] for r in rows]); lam = np.array([r[1] for r in rows]); sR = np.array([r[2] for r in rows])
X = np.vstack([np.ones_like(lam), np.log(lam)]).T
coef, *_ = np.linalg.lstsq(X, np.log(sR), rcond=None); res = np.log(sR) - X @ coef
T = np.zeros((len(p), 6, 6)); h = np.zeros(len(p), int); i2 = np.zeros(len(p), int)
for j, q in enumerate(p):
    q = int(q); g = primroot(q); ind = np.zeros(q, dtype=np.int64); x = 1
    for e in range(q - 1): ind[x] = e; x = x * g % q
    xs = np.arange(1, q - 1)
    A = np.bincount((ind[xs] % 6) * 6 + ind[xs + 1] % 6, minlength=36).reshape(6, 6).astype(float)
    T[j] = (A - A.mean()) / math.sqrt(q); h[j] = ind[q - 1] % 6; i2[j] = ind[2] % 6
print('\nPart B: %d primes; fit %.3f %+.3f log lambda, residual sd %.3f' % (len(p), coef[0], coef[1], res.std()))
for hh in (0, 3):
    sel = (h == hh) & (lam <= 0.31)
    r0 = spear(res[sel], np.abs(T[sel, 0, hh]))
    print('h=%d lam<=0.31 n=%d: Spearman(res,|t(0,h)|) %.3f (author function %.3f); signed %.3f' % (
        hh, sel.sum(), r0, sp_author(res[sel], np.abs(T[sel, 0, hh])), spear(res[sel], T[sel, 0, hh])))
    Mx = np.array([[spear(res[sel], np.abs(T[sel, a, b])) for b in range(6)] for a in range(6)])
    print('  Spearman(res, |t(a,b)|), rows a, columns b:')
    for a in range(6): print('   ' + ' '.join('%+.2f' % v for v in Mx[a]))
    # distinct cyclotomic numbers: group cells with identical columns of values
    vals = {}
    for a in range(6):
        for b in range(6):
            key = tuple(np.round(T[sel, a, b], 9)); vals.setdefault(key, []).append((a, b))
    cls = sorted(((spear(res[sel], np.abs(np.array(kk))), v) for kk, v in vals.items()), reverse=True)
    print('  %d distinct cells; top three: %s' % (len(cls), '; '.join('%.2f %s' % (c, v[:3]) for c, v in cls[:3])))
    # leave-one-out, bootstrap, permutation
    idx = np.flatnonzero(sel)
    loo = [spear(np.delete(res[idx], m), np.delete(np.abs(T[idx, 0, hh]), m)) for m in range(len(idx))]
    bs = []
    for _ in range(10000):
        b = rng.choice(idx, len(idx), replace=True); bs.append(spear(res[b], np.abs(T[b, 0, hh])))
    perm = [spear(rng.permutation(res[idx]), np.abs(T[idx, 0, hh])) for _ in range(20000)]
    print('  LOO range %.2f-%.2f; bootstrap 95%% %.2f-%.2f; permutation p(>= obs) %.5f' % (
        min(loo), max(loo), np.percentile(bs, 2.5), np.percentile(bs, 97.5), np.mean(np.array(perm) >= r0 - 1e-12)))
    print('  confounds: Spearman(lam, res) %.2f, (lam, |t|) %.2f, (ind(2)%%3==0, |t|) %.2f' % (
        spear(lam[sel], res[sel]), spear(lam[sel], np.abs(T[sel, 0, hh])), spear((i2[sel] % 3 == 0) * 1.0, np.abs(T[sel, 0, hh]))))
# family-wise over the 16 printed statistics of fixedcell.py and over all cells of both classes
sq = (T ** 2).sum((1, 2))


def stats16(r):
    out = []
    for hh in (0, 3):
        m = h == hh
        for sel in (m, m & (lam <= 0.31)):
            t0 = T[sel, 0, hh]
            out += [spear(r[sel], t0), spear(r[sel], np.abs(t0)), spear(r[sel], sq[sel]), np.corrcoef(r[sel], t0 ** 2)[0, 1]]
    return np.array(out)


obs16 = stats16(res)
print('\n16 fixedcell statistics:', ' '.join('%.2f' % v for v in obs16))
mx = []
for _ in range(4000):
    mx.append(np.max(np.abs(stats16(rng.permutation(res)))))
print('family-wise p (max |stat| over the 16 >= %.2f): %.4f' % (np.max(np.abs(obs16)), np.mean(np.array(mx) >= np.max(np.abs(obs16)) - 1e-12)))
mx = []
for _ in range(2000):
    r = rng.permutation(res); best = 0
    for hh in (0, 3):
        sel = (h == hh) & (lam <= 0.31)
        for a in range(6):
            for b in range(6):
                best = max(best, spear(r[sel], np.abs(T[sel, a, b])))
    mx.append(best)
print('family-wise p (max over 36 cells x 2 classes, |t|, lam<=0.31, >= 0.81): %.4f' % np.mean(np.array(mx) >= 0.81 - 1e-12))
