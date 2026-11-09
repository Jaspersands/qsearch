"""Referee round 3b: independent recomputation of the 35-prime snapshot numbers in SEC12_DRAFT_r4.md
and of the kappa = 7 p = 23549 numbers (bucket + pairsym)."""
import sys, os, re, math
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
sys.path.insert(0, OSC); os.chdir(OSC)
import numpy as np
from math import comb
from scipy.stats import mannwhitneyu, spearmanr, poisson, chi2, binom
import k6_spike_survey as ks

# the 35 primes of the 03:45 snapshot (first table, before 'Earlier S-batched')
snap = {}
for line in open('review-2026-11-10/survey_snapshot.out'):
    if line.startswith('Earlier'): break
    w = line.split()
    if w and w[0].isdigit(): snap[int(w[0])] = w
P = sorted(snap); print('snapshot primes:', len(P), P[0], '...', P[-1])
R = {p: ks.analyse('survey/mc_k6_p%d_s13.npz' % p) for p in P}
# consistency of the snapshot table with the npz files (N1mu1, PW, B_L, B_D)
print('N1mu1 mismatches vs snapshot table:', [p for p in P if abs(R[p]['N1mu1'] - float(snap[p][3])) > 0.006])
lam = {p: R[p]['lam'] for p in P}
h = {p: 0 if p % 12 == 1 else 3 for p in P}
print('h from sym[0] agrees with p mod 12:', all(int(R[p]['sym'][0]) % 6 == h[p] for p in P))
def bands(ps):
    out = []
    for lo, hi in ((0.19, 0.22), (0.22, 0.2501), (0.2501, 0.31)):
        b = [p for p in ps if lo <= lam[p] < hi]
        if not b: continue
        med = {k: float(np.median([R[p][k] for p in b])) for k in ('L', 'D', 'PW', 'N1mu1')}
        fl = {}
        for p in b:
            f = ''
            if R[p]['D_lo'] > 2 * med['D']: f += 'sD'
            if R[p]['PW'] > 2 * med['PW']: f += 'sPW'
            if R[p]['N1mu1'] > 2 * med['N1mu1']: f += 'sN'
            if f: fl[p] = f
        out.append((lo, hi, b, med, fl))
    return out
for lo, hi, b, med, fl in bands(P):
    mL = max(b, key=lambda p: R[p]['L']); mD = max(b, key=lambda p: R[p]['D'])
    print('band [%.2f,%.2f) n=%d  med L/D/PW/N %.3f/%.3f/%.3f/%.3f  maxL %.3f (%d) maxD %.2f (%d)  flags %s' % (
        lo, hi, len(b), med['L'], med['D'], med['PW'], med['N1mu1'], R[mL]['L'], mL, R[mD]['D'], mD, fl))
le = [p for p in P if lam[p] <= 0.25]; gt = [p for p in P if lam[p] > 0.25]
fl_le = {}
for lo, hi, b, med, fl in bands(P):
    if hi <= 0.2501: fl_le.update(fl)
print('lambda<=0.25: n=%d, spikes %d, sD %d' % (len(le), len(fl_le), sum('sD' in f for f in fl_le.values())))
# 34-prime state (2017 not yet finished): band 3 and 1987
P34 = [p for p in P if p != 2017]
for lo, hi, b, med, fl in bands(P34):
    if lo > 0.25: print('34-prime band 3: n=%d med D %.3f, 1987 D_lo %.3f -> flags %s' % (len(b), med['D'], R[1987]['D_lo'], fl))
print('1987: D %.3f z %.2f lo %.3f hi %.3f N1 %.3f PW %.3f h %d' % (R[1987]['D'], R[1987]['D_z'], R[1987]['D_lo'], R[1987]['D_hi'], R[1987]['N1mu1'], R[1987]['PW'], h[1987]))
print('PW min lambda<=0.25: %.3f at %d; PW<1: %s' % (min(R[p]['PW'] for p in le), min(le, key=lambda p: R[p]['PW']),
      [(p, round(R[p]['PW'], 3)) for p in P if R[p]['PW'] < 1]))
print('N1mu1 min: %.3f at %d -> B %.2f' % (min(R[p]['N1mu1'] for p in P), min(P, key=lambda p: R[p]['N1mu1']), 1 / min(R[p]['N1mu1'] for p in P)))
for lab, b in (('lam<0.22', [p for p in P if lam[p] < 0.22]), ('0.22-0.25', [p for p in P if 0.22 <= lam[p] <= 0.25]), ('>0.25', gt)):
    x = np.log([R[p]['N1mu1'] / R[p]['symR'] for p in b])
    print('ratio N1/symR %-10s n=%d  geo-mean %.4f  median %.4f  log-sd %.3f (ddof1) %.3f (ddof0)' % (
        lab, len(b), math.exp(x.mean()), math.exp(np.median(x)), x.std(ddof=1), x.std()))
sp = lambda a, b, ps: spearmanr([R[p][a] for p in ps], [R[p][b] for p in ps])[0]
print('Spearman lam<=0.25: symR~N1 %.3f symR~L %.3f symR~D %.3f  K~N1 %.3f K~D %.3f maxD~D %.3f' % (
    sp('symR', 'N1mu1', le), sp('symR', 'L', le), sp('symR', 'D', le), sp('K', 'N1mu1', le), sp('K', 'D', le), sp('maxD', 'D', le)))
rc = [R[p]['N1mu1'] / R[p]['Csym'] for p in le]
print('N1/Csym lam<=0.25: median %.3f quartiles %.3f-%.3f' % (np.median(rc), np.percentile(rc, 25), np.percentile(rc, 75)))
def cls(ps, key='D'):
    return [R[p][key] for p in ps if h[p] == 0], [R[p][key] for p in ps if h[p] == 3]
pre = [p for p in P if p >= 1741 and p not in (1747, 1753, 1759, 1933)]
print('pre-registered set (%d):' % len(pre), pre)
for lab, ps in (('lam<=0.25', le), ('all35', P), ('pre16', pre), ('pre16&lam<=0.25', [p for p in pre if lam[p] <= 0.25]), ('pre16&lam>0.25', [p for p in pre if lam[p] > 0.25])):
    a, b = cls(ps); k0 = sum(x > 2 for x in a); k3 = sum(x > 2 for x in b)
    mw = mannwhitneyu(a, b, alternative='greater', method='exact').pvalue
    cut = comb(len(a), k0 + k3) / comb(len(ps), k0 + k3) if k3 == 0 and k0 > 0 else float('nan')
    an, bn = cls(ps, 'N1mu1')
    print('%-16s n=%d h0 %d h3 %d  B_D>2: %d/%d  cut %.4f  MW(B_D) exact %.4f  max B_D h3 %.2f  medians B_D %.3f/%.3f N1 %.3f/%.3f' % (
        lab, len(ps), len(a), len(b), k0, k3, cut, mw, max(b), np.median(a), np.median(b), np.median(an), np.median(bn)))
pred = {}
txt = open('survey/predictions_N1mu1.txt').read().split('unfinished survey primes:')[1]
for m in re.finditer(r'(\d+):([\d.]+)', txt): pred[int(m.group(1))] = float(m.group(2))
for lab, ps in (('lam<=0.25 excl 1933', [p for p in le if p in pred and p != 1933]), ('lam>0.25', [p for p in gt if p in pred])):
    e = np.array([math.log(R[p]['N1mu1'] / pred[p]) for p in ps]); i = int(np.argmax(abs(e)))
    print('prospective %-20s n=%d rms %.3f mean %+.3f max|e| %.3f (%+.3f at %d)  range %d-%d' % (lab, len(ps), math.sqrt((e ** 2).mean()), e.mean(), abs(e).max(), e[i], ps[i], ps[0], ps[-1]))
# ---- kappa = 7, p = 23549
p7 = 23549; k = 7; Ninv = comb(k, 2) * comb(k - 2, 2) // 2
R22 = Ninv ** 2 * k ** 4 / p7 ** 2
lam7 = 0.2002; M = 5 * p7
mu_perS = M * lam7 ** 7 / math.factorial(7)
print('\nk=7 p=%d: N_inv %d, N_inv^2 k^4 = %d, R22 = %.5f, Poisson configs/S (M=5p) %.4e' % (p7, Ninv, Ninv ** 2 * k ** 4, R22, mu_perS))
# bucket run: 151 configurations in 6e5 S = 135 (b=7) + 2 x 8 (b=8)
nb, nS = 151, 600000; r_b = nb / (nS * mu_perS); var = 135 + 2 * 64
print('bucket: ratio %.3f  se(cluster plug-in) %.3f  se(Poisson-only) %.3f' % (r_b, r_b * math.sqrt(var) / nb, r_b / math.sqrt(nb)))
# with Poisson composition of configurations (b=7 0.819, b=8 0.164, b=9 0.0164 -> clusters 1, 8, 36)
sh = np.array([math.exp(-0.2) * 0.2 ** j / math.factorial(j) for j in range(0, 4)]); sizes = [1, 8, 36, 120]
v_model = nb * sum(s * c for s, c in zip(sh, sizes)) / sh.sum()
print('        se with Poisson composition of bucket sizes %.3f' % (r_b * math.sqrt(v_model) / nb))
# pairsym run: 79 configurations in 3e5 S, 5 with 2+2, all from b=7 buckets (63 b=7 + 16 from two b=8)
npc, nS2, n22 = 79, 300000, 5
r_p = npc / (nS2 * mu_perS); var_p = 63 + 2 * 64
print('pairsym: ratio %.3f se %.3f; combined ratio %.3f se %.3f' % (r_p, r_p * math.sqrt(var_p) / npc, (nb + npc) / ((nS + nS2) * mu_perS),
      (nb + npc) / ((nS + nS2) * mu_perS) * math.sqrt(var + var_p) / (nb + npc)))
s = n22 / npc
F_dir = n22 / (nS2 * mu_perS * R22)
print('share %.4f  F = share*N1/R22: %.3f (0.84) %.3f (0.88)  direct 5/(nS mu R22) %.3f' % (s, s * 0.84 / R22, s * 0.88 / R22, F_dir))
lo95, hi95 = chi2.ppf(0.025, 2 * n22) / 2, chi2.ppf(0.975, 2 * n22 + 2) / 2
lo68, hi68 = chi2.ppf(0.16, 2 * n22) / 2, chi2.ppf(0.84, 2 * n22 + 2) / 2
print('F Poisson CI: 68%% %.2f-%.2f  95%% %.2f-%.2f' % (lo68 / n22 * F_dir, hi68 / n22 * F_dir, lo95 / n22 * F_dir, hi95 / n22 * F_dir))
print('R22 share prediction at F=1: %.4f (0.88) %.4f (0.84)' % (R22 / 0.88, R22 / 0.84))
print('symR law: 0.038*67.44 = %.2f; log gap to 0.84: %.2f' % (0.038 * 67.44, math.log(0.038 * 67.44 / 0.84)))
print('not-2+2 rate at 23549: %.3f-%.3f' % ((1 - s) * 0.84, (1 - s) * 0.88))
# kappa = 6 shares and weights near lambda = 0.2 (pairsym files), against the kappa = 7 weight
w7 = n22 / (nS2 * mu_perS)
print('kappa=7 2+2 weight w = %.4f' % w7)
for q, shq, rq in ((1597, 0.875, 3.97), (1621, 0.741, 0.42), (1627, 0.780, 2.05), (1657, 0.830, 3.71)):
    R6 = (comb(6, 2) * comb(4, 2) // 2) ** 2 * 6 ** 4 / q ** 2
    wq = shq * rq; exp_n = wq * nS2 * mu_perS
    print('  k6 %d: share %.3f ratio %.2f -> w %.3f (R22 %.3f, F %.2f); w6/w7 %.1f; expected 2+2 at k7 if w equal: %.1f, P(<=5) %.1e' % (
        q, shq, rq, wq, R6, wq / R6, wq / w7, exp_n, poisson.cdf(5, exp_n)))
print('share-only reading: Bin(79, 0.7) P(<=5) = %.1e; Bin(79,0.741) %.1e' % (binom.cdf(5, 79, 0.7), binom.cdf(5, 79, 0.741)))
# ---- What ranks symR (finding 1 rewrite): |a| vs |L|, detrended log symR (log-log fit on all 89 primes, used at lambda <= 0.31)
sym = {}
for line in open('survey/sym_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): sym[int(w[0])] = (float(w[1]), float(w[3]))
def ab(p):
    for b in range(0, math.isqrt(p // 3) + 1):
        r = p - 3 * b * b; a = math.isqrt(r)
        if a * a == r: return (a if a % 3 == 1 else -a), b
def LM(p):
    for M in range(0, math.isqrt(4 * p // 27) + 1):
        r = 4 * p - 27 * M * M; L = math.isqrt(r)
        if L * L == r: return (L if L % 3 == 1 else -L), M
allq = sorted(sym); lo = [q for q in allq if sym[q][0] <= 0.31]
for lab, fitset in (('fit on all %d' % len(allq), allq), ('fit on the %d' % len(lo), lo)):
    c = np.polyfit(np.log([sym[q][0] for q in fitset]), np.log([sym[q][1] for q in fitset]), 1)
    res = np.log([sym[q][1] for q in lo]) - np.polyval(c, np.log([sym[q][0] for q in lo]))
    A = np.array([abs(ab(q)[0]) / math.sqrt(q) for q in lo]); Lr = np.array([abs(LM(q)[0]) / (2 * math.sqrt(q)) for q in lo])
    cube = np.array([ab(q)[1] % 3 == 0 for q in lo]); h0 = np.array([q % 12 == 1 for q in lo]); h3 = ~h0
    rr = lambda m, v: spearmanr(res[m], v[m])[0]
    allm = np.ones(len(lo), bool)
    print('%s: n=%d cube %d | rho(|a|) all %.2f h0 %.2f h3 %.2f | h0 cube %.2f non %.2f | h3 cube %.2f (n=%d) non %.2f (n=%d) | rho(|L|/2rp) %.2f | med res h0 %+.2f/%+.2f h3 %+.2f/%+.2f' % (
        lab, len(lo), cube.sum(), rr(allm, A), rr(h0, A), rr(h3, A), rr(h0 & cube, A), rr(h0 & ~cube, A), rr(h3 & cube, A), (h3 & cube).sum(),
        rr(h3 & ~cube, A), (h3 & ~cube).sum(), rr(allm, Lr), np.median(res[h0 & cube]), np.median(res[h0 & ~cube]), np.median(res[h3 & cube]), np.median(res[h3 & ~cube])))
print('|L| = 2|a| iff 3 | b, else |L| = |a +- 3b|:', all((abs(LM(q)[0]) == 2 * abs(ab(q)[0])) == (ab(q)[1] % 3 == 0) for q in lo)
      and all(abs(LM(q)[0]) in (abs(ab(q)[0] + 3 * ab(q)[1]), abs(ab(q)[0] - 3 * ab(q)[1])) for q in lo if ab(q)[1] % 3))
