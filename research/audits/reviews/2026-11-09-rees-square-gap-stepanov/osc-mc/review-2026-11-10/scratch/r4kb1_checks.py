"""Referee round 4k-b part 1 (11 Nov): check of tail_index.py's sigma_L, T1' ratio and extrapolations, by my own Gram
path (as r4j_checks.py; not k6_spike_survey.analyse), plus operating characteristics of T1' and the noise term.
Run:  nice -n 19 /opt/anaconda3/bin/python -I r4kb1_checks.py > r4kb1_checks.out"""
import glob, math
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
SP = '/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad'
def BL(f):
    d = np.load(f); supp = d['supp']
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2); ms = np.add.outer(supp, supp)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    m = (two & (ms <= 6)) | one
    ow = d['orb'] * np.abs(d['P'][:, int(d['rb'])]); w2 = np.outer(ow, ow)
    V = d['S1'] / np.maximum(d['cnt'], 1)[:, None, None]; N = d['cnt'].sum(); Vh = d['S1'].sum(0) / N
    nz = (w2[m] * np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0)[m]).sum() / float(d['Nunl'])
    A = V[:, m] * np.sqrt(w2[m])[None, :]; G = (A @ A.conj().T).real; B = len(G)
    X = lambda idx: (G[np.ix_(idx, idx)].sum() - np.trace(G[np.ix_(idx, idx)])) / (len(idx) * (len(idx) - 1))
    loo = np.array([X([i for i in range(B) if i != t]) for t in range(B)]); se = math.sqrt((B - 1) / B * ((loo - loo.mean()) ** 2).sum())
    s = X(list(range(B))) - nz
    return int(d['k']), int(d['p']), math.sqrt(max(s, 0) / w2[m].sum()), s / se
k6 = [BL(f) for f in sorted(glob.glob(OSC + '/survey/mc_k6_p*_s13.npz'))]
l6 = np.log([max(b, 1e-6) for k, p, b, z in k6 if 0.2501 <= p / 6 ** 5 < 0.31]); z6 = [z for k, p, b, z in k6 if 0.2501 <= p / 6 ** 5 < 0.31]
band = {34259: 19, 34273: 21, 34469: 23, 35281: 25, 36541: 27, 35099: 13, 34847: 13}
k7 = [BL('%s/mc_k7_p%d_s%d.npz' % (SP, p, s)) for p, s in band.items()]
l7 = np.log([b for k, p, b, z in k7]); z7 = [z for k, p, b, z in k7]
print('1. Own path: kappa = 6 band (0.25, 0.31]: N %d, sigma_L %.4f; kappa = 7 band: N %d, sigma_L %.4f, median B_L %.4f; ratio %.4f' % (
    len(l6), l6.std(ddof=1), len(l7), l7.std(ddof=1), math.exp(np.median(l7)), l7.std(ddof=1) / l6.std(ddof=1)))
rb = np.random.default_rng(1)
rat = [rb.choice(l7, len(l7)).std(ddof=1) / rb.choice(l6, len(l6)).std(ddof=1) for _ in range(2000)]
print('   T1\' as tail_index.py (seed 1, l7 draw then l6 draw): %.2f-%.2f' % tuple(np.percentile(rat, [2.5, 97.5])))
for sd in (7, 8, 9):
    r2 = np.random.default_rng(sd); rr = [r2.choice(l7, len(l7)).std(ddof=1) / r2.choice(l6, len(l6)).std(ddof=1) for _ in range(2000)]
    print('   other seed %d: %.2f-%.2f' % ((sd,) + tuple(np.percentile(rr, [2.5, 97.5]))))
r3 = np.random.default_rng(1); b6 = [r3.choice(l6, len(l6)).std(ddof=1) for _ in range(2000)]
print('   sigma_L(6) bootstrap (own, seed 1): %.3f-%.3f; bootstrap mean %.3f against point %.3f' % (
    tuple(np.percentile(b6, [2.5, 97.5])) + (np.mean(b6), l6.std(ddof=1))))
print('\n2. Extrapolations (log_7 T 5.57, phi 6)')
T = 7 ** 5.57; NT = T / (6 * math.log(T)); med = math.exp(np.median(l7)); sig = l7.std(ddof=1)
part = sig * math.sqrt(2 * math.log(NT)) / math.log(7)
print('   N_T %.1f; log_7 median %.3f; lognormal log_7(sup/median) %.3f (%.0f%% of 1.70) -> absolute %.3f' % (
    NT, math.log(med, 7), part, 100 * part / 1.70, math.log(med, 7) + part))
Xs = np.sort(np.exp(l7) / med)[::-1]; g = float(np.mean(np.log(Xs[:2] / Xs[2])))
print('   power (Hill k=2) %.3f: log_7(sup/median) %.3f -> absolute %.3f' % (g, g * math.log(NT) / math.log(7), math.log(med, 7) + g * math.log(NT) / math.log(7)))
print('   with the kappa = 6 band sigma 0.352: log_7(sup/median) %.3f' % (0.352 * math.sqrt(2 * math.log(NT)) / math.log(7)))
print('\n3. Measurement noise: per-prime sd of ln B ~ 1/(2z)')
e7 = 1 / (2 * np.array(z7)); e6 = 1 / (2 * np.array(z6))
print('   kappa = 7 band z %s -> 1/(2z) %s; rms %.3f, max %.3f' % (' '.join('%.1f' % z for z in z7), ' '.join('%.3f' % e for e in e7),
      math.sqrt((e7 ** 2).mean()), e7.max()))
print('   kappa = 6 band (N %d): z median %.1f, min %.1f; rms 1/(2z) %.3f' % (len(z6), np.median(z6), min(z6), math.sqrt((e6 ** 2).mean())))
print('   quadrature: sqrt(0.352^2 + rms7^2) = %.3f; with 0.12: %.3f; ratio inflation from unequal noise (true sigma 0.352 both): %.3f' % (
    math.sqrt(0.352 ** 2 + (e7 ** 2).mean()), math.sqrt(0.352 ** 2 + 0.12 ** 2),
    math.sqrt(0.352 ** 2 + (e7 ** 2).mean()) / math.sqrt(0.352 ** 2 + (e6 ** 2).mean())))
print('\n4. T1\' operating characteristics (N7 24, N6 31, 2000 bootstrap pairs, 400 replicates)')
rng = np.random.default_rng(5)
def oc(gen6, gen7):
    W = Nn = 0
    for _ in range(400):
        a6 = gen6(31); a7 = gen7(24)
        i6 = rng.integers(0, 31, (2000, 31)); i7 = rng.integers(0, 24, (2000, 24))
        rr = a7[i7].std(axis=1, ddof=1) / a6[i6].std(axis=1, ddof=1); lo, hi = np.percentile(rr, [2.5, 97.5])
        W += lo > 1; Nn += hi < 1
    return W / 400, Nn / 400
for c in (1.0, 1.25, 1.5, 2.0):
    w, n = oc(lambda n: 0.352 * rng.standard_normal(n), lambda n: c * 0.352 * rng.standard_normal(n))
    print('   normal ln B, sigma7/sigma6 = %.2f: P(WIDER) %.3f, P(NARROWER) %.3f' % (c, w, n))
for c in (1.0, 1.5):
    w, n = oc(lambda n: 0.352 / math.sqrt(2) * rng.standard_t(4, n), lambda n: c * 0.352 / math.sqrt(2) * rng.standard_t(4, n))
    print('   t4 ln B (outlier-prone), scale ratio %.2f: P(WIDER) %.3f, P(NARROWER) %.3f' % (c, w, n))
