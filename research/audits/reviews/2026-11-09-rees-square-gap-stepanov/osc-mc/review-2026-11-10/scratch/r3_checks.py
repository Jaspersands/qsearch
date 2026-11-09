"""Round-3 referee checks (run from osc-mc/ with nice -n 19 python -I). Read-only on osc-mc."""
import sys, math, glob, os
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
sys.path.insert(0, OSC)
os.chdir(OSC)
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr, hypergeom
import k6_spike_survey as ks
from mc_classes import primroot

# ---------- survey rows (all finished s13 files) ----------
files = sorted(glob.glob('survey/mc_k6_p*_s13.npz'))
rows = {}
for f in files:
    r = ks.analyse(f)
    rows[r['p']] = r
snap28 = [1531, 1543, 1549, 1567, 1579, 1597, 1609, 1621, 1627, 1657, 1663, 1669, 1693, 1699, 1723, 1741, 1747, 1753,
          1759, 1777, 1783, 1789, 1801, 1831, 1861, 1873, 1933, 1951]
print('finished s13 files now:', len(rows), sorted(set(rows) - set(snap28)))
for p in sorted(set(rows) - set(snap28)):
    r = rows[p]
    print('  new %d lam %.3f h %d  N1/mu1 %.2f (%.2f)  PW %.2f  B_L %.3f  B_D %.2f (z %.1f) lo %.2f hi %.2f  symR %.1f' % (
        p, r['lam'], r['sym'][0], r['N1mu1'], r['N1mu1_se'], r['PW'], r['L'], r['D'], r['D_z'], r['D_lo'], r['D_hi'], r['symR']))

def band_flags(sel, label):
    b = [rows[p] for p in sel]
    med = {q: float(np.median([r[q] for r in b])) for q in ('L', 'D', 'PW', 'N1mu1')}
    fl = []
    for r in b:
        s = ('sD' if r['D_lo'] > 2 * med['D'] else '') + ('sPW' if r['PW'] > 2 * med['PW'] else '') + ('sN' if r['N1mu1'] > 2 * med['N1mu1'] else '')
        if s: fl.append('%d %s' % (r['p'], s))
    print('%s n=%d med B_L %.3f B_D %.3f PW %.3f N %.3f; flags: %s' % (label, len(b), med['L'], med['D'], med['PW'], med['N1mu1'], '; '.join(fl)))

band2_now = [p for p in rows if 0.22 <= rows[p]['lam'] < 0.2501]
band2_snap = [p for p in snap28 if 0.22 <= rows[p]['lam'] < 0.2501]
band_flags(sorted(band2_snap), 'band [0.22,0.25] snapshot')
band_flags(sorted(band2_now), 'band [0.22,0.25] now')
band3_now = [p for p in rows if 0.2501 <= rows[p]['lam'] < 0.31]
if band3_now: band_flags(sorted(band3_now), 'band (0.25,0.31] now')

# ---------- h-class tests ----------
def hclass_tests(sel, label):
    h0 = [rows[p]['D'] for p in sel if rows[p]['sym'][0] == 0]
    h3 = [rows[p]['D'] for p in sel if rows[p]['sym'][0] == 3]
    mw = mannwhitneyu(h0, h3, alternative='greater', method='exact')
    mwa = mannwhitneyu(h0, h3, alternative='greater', method='asymptotic')
    k0 = sum(x > 2 for x in h0); k3 = sum(x > 2 for x in h3)
    n = len(h0) + len(h3); K = k0 + k3
    hyp = hypergeom.sf(k0 - 1, n, len(h0), K) if K else float('nan')
    print('%s: n=%d (h0 %d, h3 %d) MW one-sided exact %.4f asym %.4f; B_D>2: %d/%d vs %d/%d, hypergeom P %.4f; medians B_D %.2f/%.2f N %.2f/%.2f' % (
        label, n, len(h0), len(h3), mw.pvalue, mwa.pvalue, k0, len(h0), k3, len(h3), hyp, np.median(h0), np.median(h3),
        np.median([rows[p]['N1mu1'] for p in sel if rows[p]['sym'][0] == 0]), np.median([rows[p]['N1mu1'] for p in sel if rows[p]['sym'][0] == 3])))

hclass_tests(snap28, 'n=28 snapshot')
hclass_tests([p for p in snap28 if p not in (1873, 1951)], 'n=26 (snapshot minus 1873,1951)')
prosp9 = [1741, 1777, 1783, 1789, 1801, 1831, 1861, 1873, 1951]
hclass_tests(prosp9, 'prospective 9')
hclass_tests(prosp9 + [1759], 'prospective 9 + 1759')
newnow = sorted(set(rows) - set(snap28))
hclass_tests(prosp9 + newnow, 'prospective 9 + new finished')
hclass_tests(sorted(rows), 'all finished now')

# ---------- N1/mu1 vs symR ----------
b1 = [p for p in snap28 if rows[p]['lam'] < 0.22]
rat = np.array([rows[p]['N1mu1'] / rows[p]['symR'] for p in b1])
print('band1 n=%d: N1/mu1/symR geo mean %.4f, log-sd %.3f; without 1699: geo %.4f log-sd %.3f' % (
    len(b1), np.exp(np.log(rat).mean()), np.log(rat).std(ddof=1), np.exp(np.log(rat[:-1]).mean()), np.log(rat[:-1]).std(ddof=1)))
low27 = [p for p in snap28 if rows[p]['lam'] <= 0.2501]
rat27 = np.array([rows[p]['N1mu1'] / rows[p]['symR'] for p in low27])
print('lam<=0.25 n=%d: N1/mu1/symR geo mean %.4f, log-sd %.3f' % (len(low27), np.exp(np.log(rat27).mean()), np.log(rat27).std(ddof=1)))

# ---------- prospective N1/mu1 predictions ----------
pred = {}
for line in open('survey/predictions_N1mu1.txt'):
    if line.startswith('predicted') or line.startswith('2026') or line.startswith('in-sample'):
        continue
    for tok in line.split():
        if ':' in tok:
            a, b = tok.split(':'); pred[int(a)] = float(b)
fin = [p for p in pred if p in rows]
print('predicted & finished:', sorted(fin))
for sel, lab in [([p for p in fin if p in snap28 and rows[p]['lam'] <= 0.2501 and p != 1933], '13 (lam<=0.25, excl 1933)'),
                 ([p for p in fin if p in snap28 and rows[p]['lam'] <= 0.2501], 'incl 1933'),
                 ([p for p in fin if rows[p]['lam'] <= 0.2501 and p != 1933], 'lam<=0.25 now, excl 1933')]:
    e = np.array([math.log(rows[p]['N1mu1'] / pred[p]) for p in sorted(sel)])
    print('  %-28s n=%2d rms %.3f mean %+.3f max|e| %.3f' % (lab, len(e), math.sqrt((e ** 2).mean()), e.mean(), np.abs(e).max()))
for p in sorted(fin):
    print('   %d obs %.3f pred %.2f log err %+.3f' % (p, rows[p]['N1mu1'], pred[p], math.log(rows[p]['N1mu1'] / pred[p])))

# ---------- F and F*v ----------
Ninv = lambda k: math.comb(k, 2) * math.comb(k - 2, 2) // 2
R = lambda k, p: Ninv(k) ** 2 * k ** 4 / p ** 2
split = {1597: (0.860, 3.750, 4.28, 4.79), 1621: (0.708, 0.300, 0.44, 0.65), 1657: (0.833, 3.721, 11.57, 12.49),
         1789: (0.804, 3.617, 17.25, 18.66), 1933: (0.762, 2.341, 4.42, 4.98)}
for p, (sh, n2, bd, bdhi) in split.items():
    F = n2 / R(6, p); v = bd * 36 / p
    print('F(%d) split %.3f  R %.4f  v %.4f  F*v %.4f   (2sig F*v %.4f)' % (p, F, R(6, p), v, F * v, F * bdhi * 36 / p))
pairs = {1597: (0.875, 3.97), 1621: (0.741, 0.42), 1627: (0.780, 2.05), 1657: (0.830, 3.71), 1789: (0.736, 2.53),
         1933: (0.700, 2.72), 2347: (0.444, 0.80), 3877: (0.167, 0.84)}
surv = {p: rows[p]['N1mu1'] for p in rows}
surv.update({2347: 0.76, 3877: 0.85})
for p, (sh, n1) in pairs.items():
    print('F(%d) pairsym %.3f  pairsym share x survey N %.3f' % (p, sh * n1 / R(6, p), sh * surv[p] / R(6, p)))

# ---------- threshold path ----------
logT = {6: 5.14, 7: 5.57, 8: 6.18, 9: 6.78, 10: 7.36}
lamT = {7: 0.44, 8: 0.18, 9: 0.07, 10: 0.02}
for k in range(6, 11):
    T = k ** logT[k]
    line = 'k=%d T=%.4g lam %.4f  R22 %.3g  Ninv^2k^2/T %.3f' % (k, T, T / k ** (k - 1), R(k, T), Ninv(k) ** 2 * k * k / T)
    if k in lamT:
        T2 = lamT[k] * k ** (k - 1)
        line += '  | with rounded lam_T %.2f: R22 %.3g  Ninv^2k^2/T %.3f' % (lamT[k], R(k, T2), Ninv(k) ** 2 * k * k / T2)
    print(line)
for k in (7, 8, 9, 10):
    T = k ** logT[k]; x = Ninv(k) ** 2 * k * k / T
    print('  k=%d: F*v=1.531 -> %.2f ; 1621 2sig F*v=%.5f -> %.3f ; w(F=4.41) %.4f' % (k, 1.531 * x, 0.30036 * 0.65 * 36 / 1621,
          0.30036 * 0.65 * 36 / 1621 * x, 4.41 * R(k, T)))
# kappa = 7 F
for p, sh, n1b, n1p, cnt in [(35281, 19 / 446, 0.90, 0.88, 446), (35099, 5 / 455, 0.96, 0.93, 455), (36037, 28 / 624, 1.09, 1.06, 624),
                             (34693, 9 / 428, 0.89, 0.95, 428)]:
    print('k7 %d R %.4f share %.4f F(pairsym N) %.2f F(bucket N) %.2f  expected share %.4f/%.4f  not22 %.3f/%.3f' % (
        p, R(7, p), sh, sh * n1p / R(7, p), sh * n1b / R(7, p), R(7, p) / n1p, R(7, p) / n1b, (1 - sh) * n1p, (1 - sh) * n1b))
for p in (34259, 34469, 23549):
    print('k7 %d R %.4f lam %.4f' % (p, R(7, p), p / 7 ** 6))
# Spearman kappa=7 six primes
sy = {35281: 15.79, 34469: 16.69, 35099: 21.33, 34259: 22.05, 36037: 44.19, 34693: 44.22}
nm = {35281: 0.90, 34469: 0.91, 35099: 0.96, 34259: 1.11, 36037: 1.09, 34693: 0.89}
ps = sorted(sy)
print('k7 Spearman symR vs N1/mu1 (6 primes): %.3f; with 36037/34693 symR swapped: %.3f' % (
    spearmanr([sy[p] for p in ps], [nm[p] for p in ps])[0],
    spearmanr([sy[p] if p not in (36037, 34693) else {36037: 44.22, 34693: 44.19}[p] for p in ps], [nm[p] for p in ps])[0]))

# ---------- a vs L ----------
def rep_a(q):
    for a in range(int(math.isqrt(q)) + 1):
        r = q - a * a
        if r % 3 == 0 and math.isqrt(r // 3) ** 2 == r // 3:
            return a, math.isqrt(r // 3)
def rep_L(q):
    for M in range(1, int(math.isqrt(4 * q // 27)) + 1):
        r = 4 * q - 27 * M * M
        if r >= 0 and math.isqrt(r) ** 2 == r:
            return math.isqrt(r), M
for q in (1933, 1951, 3571, 3889, 4219, 1789, 1657, 1597):
    a, b = rep_a(q); L, M = rep_L(q)
    print('p=%d: |a|=%d b=%d (3|b: %s)  |a|/rp %.3f   |L|=%d M=%d  |L|/(2rp) %.3f' % (q, a, b, b % 3 == 0, a / math.sqrt(q), L, M, L / (2 * math.sqrt(q))))
lst = [(int(w[0]), float(w[1]), float(w[3])) for w in (l.split() for l in open('survey/sym_rate_k6.out')) if w and w[0].isdigit()]
P = np.array([r[0] for r in lst]); lam = np.array([r[1] for r in lst]); sR = np.array([r[2] for r in lst])
X = np.vstack([np.ones_like(lam), np.log(lam)]).T
coef, *_ = np.linalg.lstsq(X, np.log(sR), rcond=None); res = np.log(sR) - X @ coef
aa = np.array([rep_a(int(q))[0] / math.sqrt(q) for q in P]); LL = np.array([rep_L(int(q))[0] / (2 * math.sqrt(q)) for q in P])
cube = np.array([rep_a(int(q))[1] % 3 == 0 for q in P])
h = np.array([((q - 1) // 2) % 6 for q in P])
s = lam <= 0.31
print('lam<=0.31 n=%d: Spearman(res,|a|/rp) %.2f  Spearman(res,|L|/2rp) %.2f ; identical |a|=|L|/2 at %d of %d (cube primes %d)' % (
    s.sum(), spearmanr(res[s], aa[s])[0], spearmanr(res[s], LL[s])[0], int(np.sum(np.isclose(aa[s], LL[s]))), s.sum(), int(cube[s].sum())))
for hv in (0, 3):
    t = s & (h == hv)
    print('  h=%d n=%d Spearman(res,|a|/rp) %.2f (res,|L|/2rp) %.2f' % (hv, t.sum(), spearmanr(res[t], aa[t])[0], spearmanr(res[t], LL[t])[0]))
small = (LL < 0.1)
print('primes with |L|/(2rp) < 0.1 (all 89): ', [(int(q), round(float(x), 3), round(float(y), 3)) for q, x, y in zip(P[small], LL[small], aa[small])])
