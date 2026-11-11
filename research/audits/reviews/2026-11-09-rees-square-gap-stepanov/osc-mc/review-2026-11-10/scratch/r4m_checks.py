"""Referee round 4m (11 Nov): independent scoring of mechanical item 8 (T1', predictions_k7_tail.txt + REVISIONS 1-2).
Own Gram path (BL as in r4kb1_checks.py), not k6_spike_survey.analyse.
Run: nice -n 19 /opt/anaconda3/bin/python -I r4m_checks.py > r4m_checks.out"""
import glob, math, itertools
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
SPO = '/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
SPN = '/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad/tail7'
def grp(supp):
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    return {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}
def BLD(f):
    d = np.load(f); supp = d['supp']; k, p = int(d['k']), int(d['p'])
    ow = d['orb'] * np.abs(d['P'][:, int(d['rb'])]); w2 = np.outer(ow, ow)
    V = d['S1'] / np.maximum(d['cnt'], 1)[:, None, None]; N = d['cnt'].sum(); Vh = d['S1'].sum(0) / N
    out = dict(k=k, p=p, nconf=int(N), eqcnt=int(d['cnt'].max() - d['cnt'].min()))
    for g, m in grp(supp).items():
        nz = (w2[m] * np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0)[m]).sum() / float(d['Nunl'])
        A = V[:, m] * np.sqrt(w2[m])[None, :]; G = (A @ A.conj().T).real; B = len(G)
        X = lambda idx: (G[np.ix_(idx, idx)].sum() - np.trace(G[np.ix_(idx, idx)])) / (len(idx) * (len(idx) - 1))
        loo = np.array([X([i for i in range(B) if i != t]) for t in range(B)]); se = math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum())
        s = X(list(range(B))) - nz; unit = 1.0 if g == 'L' else k * k / p
        out[g] = math.sqrt(max(s, 0) / w2[m].sum()) / unit; out[g + 'z'] = s / se; out[g + 's'] = s
    return out
band = {34259: 19, 34273: 21, 34469: 23, 35281: 25, 36541: 27, 35099: 13, 34847: 13}
drawn = [34147, 34217, 34231, 34511, 34651, 34679, 34721, 34819, 35141, 35393, 35533, 35603, 35617, 35771, 35897, 35911, 36107]
files = ['%s/mc_k7_p%d_s%d.npz' % (SPO, p, s) for p, s in band.items()] + ['%s/mc_k7_p%d_s%d.npz' % (SPN, p, 31 + 2 * i) for i, p in enumerate(drawn)]
R7 = [BLD(f) for f in files]
print('1. Files: all k = 7 %s; p as listed %s; nconf %s; S-batched (unequal cnt) %s; lambda %.4f-%.4f' % (
    all(r['k'] == 7 for r in R7), [r['p'] for r in R7] == list(band) + drawn, sorted({r['nconf'] for r in R7}),
    all(r['eqcnt'] > 1 for r in R7), min(r['p'] for r in R7) / 7 ** 6, max(r['p'] for r in R7) / 7 ** 6))
l7 = np.log([max(r['L'], 1e-6) for r in R7]); e7 = np.array([1 / (2 * r['Lz']) for r in R7])
K6 = [BLD(f) for f in sorted(glob.glob(OSC + '/survey/mc_k6_p*_s13.npz'))]
lam6 = np.array([r['p'] / 6 ** 5 for r in K6])
sel = [(0.25 < l <= 0.31) for l in lam6]; sel2 = [(0.2501 <= l < 0.31) for l in lam6]
print('   kappa = 6: (0.25, 0.31] gives N %d; the reader\'s [0.2501, 0.31) gives N %d; same set %s; nearest lambdas outside: %s' % (
    sum(sel), sum(sel2), sel == sel2, sorted(round(float(l), 4) for l in lam6 if 0.24 < l <= 0.25 or 0.31 <= l < 0.32)))
l6 = np.log([max(r['L'], 1e-6) for r in np.array(K6, dtype=object)[sel]]); e6 = np.array([1 / (2 * r['Lz']) for r in np.array(K6, dtype=object)[sel]])
s7, s6 = l7.std(ddof=1), l6.std(ddof=1)
print('2. sigma_L(7) %.4f (N %d), median B_L %.4f; sigma_L(6) %.4f (N %d); ratio %.4f' % (s7, len(l7), math.exp(np.median(l7)), s6, len(l6), s7 / s6))
rb = np.random.default_rng(1)
rat = [rb.choice(l7, len(l7)).std(ddof=1) / rb.choice(l6, len(l6)).std(ddof=1) for _ in range(2000)]
a, b = np.percentile(rat, [2.5, 97.5])
print('   T1\' replay (seed 1): %.2f-%.2f -> %s' % (a, b, 'WIDER' if a > 1 else ('NARROWER' if b < 1 else 'COMPATIBLE')))
for sd in (2, 3, 4):
    r2 = np.random.default_rng(sd); rr = [r2.choice(l7, 24).std(ddof=1) / r2.choice(l6, 31).std(ddof=1) for _ in range(4000)]
    print('   seed %d: %.2f-%.2f' % ((sd,) + tuple(np.percentile(rr, [2.5, 97.5]))))
loo = [np.delete(l7, i).std(ddof=1) for i in range(24)]
print('   leave-one-prime-out sigma_L(7) %.3f-%.3f (largest drop removing %d)' % (min(loo), max(loo), (list(band) + drawn)[int(np.argmin(loo))]))
print('3. Noise: 1/(2 z_L) %.3f-%.3f, rms %.3f; kappa = 6 rms %.3f; corrected sigma_L(7) %.4f, sigma_L(6) %.4f, ratio %.3f' % (
    e7.min(), e7.max(), math.sqrt((e7 ** 2).mean()), math.sqrt((e6 ** 2).mean()), math.sqrt(s7 ** 2 - (e7 ** 2).mean()),
    math.sqrt(s6 ** 2 - (e6 ** 2).mean()), math.sqrt(s7 ** 2 - (e7 ** 2).mean()) / math.sqrt(s6 ** 2 - (e6 ** 2).mean())))
rb = np.random.default_rng(1); rc = []; neg = 0
for _ in range(2000):
    i7 = rb.integers(0, 24, 24); i6 = rb.integers(0, 31, 31)
    v7 = l7[i7].var(ddof=1) - (e7[i7] ** 2).mean(); v6 = l6[i6].var(ddof=1) - (e6[i6] ** 2).mean(); neg += (v7 < 0) + (v6 < 0)
    rc.append(math.sqrt(max(v7, 0)) / math.sqrt(max(v6, 1e-12)))
print('   corrected ratio, pair bootstrap (seed 1): %.2f-%.2f; negative corrected variances %d' % (tuple(np.percentile(rc, [2.5, 97.5])) + (neg,)))
print('4. Band (7) against drawn (17): sigma %.3f vs %.3f; permutation over all C(24,7) splits: P(sd of 7 >= %.3f) = %.4f' % (
    l7[:7].std(ddof=1), l7[7:].std(ddof=1), l7[:7].std(ddof=1), 0))
idx = np.array(list(itertools.combinations(range(24), 7))); sds = l7[idx].std(axis=1, ddof=1)
rest = np.array([np.delete(l7, c).std(ddof=1) for c in idx[:0]])
print('   permutation P(sd of a random 7-subset >= band) = %.4f (%d splits)' % ((sds >= l7[:7].std(ddof=1) - 1e-12).mean(), len(idx)))
print('5. B_D: resolved (z >= 2) %d of 24; clipped (s < 0, reported 0) %d; z range %.2f to %.2f' % (
    sum(r['Dz'] >= 2 for r in R7), sum(r['Ds'] < 0 for r in R7), min(r['Dz'] for r in R7), max(r['Dz'] for r in R7)))
print('   per prime (p, B_L, z_L, B_D, z_D): ' + '; '.join('%d %.3f %.1f %.2f %.2f' % (r['p'], r['L'], r['Lz'], r['D'], r['Dz']) for r in R7))
