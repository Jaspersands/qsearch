"""Score mechanical item 2 (F over the survey) against survey/predictions_F.txt (written 05:59:59, before the runs).
For the 29 survey primes with lambda <= 0.25: the 2+2 share and N1/mu1 from the seed-13 split run (split/split13_k6_p*
for the 25 new runs; split/split_k6_p* for 1597, 1621, 1657, 1789), checked against the survey run it reproduces;
F = share * N1/mu1 * p^2 / 2,624,400; each part's B_L and B_D (k6_spike_survey.analyse on the _str/_uns npz);
symR (survey/sym_rate_k6.out); |a|/sqrt p with p = a^2 + 3b^2, a = 1 mod 3; whether 2 is a cube; h = ind(-1) mod 6;
t = (A(0,h) - mean A)/sqrt p for the order-6 cyclotomic matrix A (as review-2026-11-10/fixedcell.py).
Runs on whatever splits exist (n is printed).  Usage, from osc-mc: python -I survey/score_F.py"""
import os, re, sys, math
import numpy as np
sys.path.insert(0, '.')
import k6_spike_survey as ks
from mc_classes import primroot

R22 = 2624400.0
OLD = {1597, 1621, 1657, 1789}
PRIMES = [1531, 1543, 1549, 1567, 1579, 1597, 1609, 1621, 1627, 1657, 1663, 1669, 1693, 1699, 1723, 1741, 1747, 1753,
          1759, 1777, 1783, 1789, 1801, 1831, 1861, 1867, 1873, 1879, 1933]
SD = {1597, 1657, 1669, 1693, 1789, 1933}          # sD at lambda <= 0.25 (k6_spike_survey.out)


def spearman(x, y):
    return ks.spearman(np.asarray(x, float), np.asarray(y, float))


def mw_less(x, y):   # one-sided P(X >= observed U) for x > y, normal approximation with tie correction ignored
    x, y = np.asarray(x), np.asarray(y); n1, n2 = len(x), len(y)
    U = sum((a > b) + 0.5 * (a == b) for a in x for b in y)
    mu, sd = n1 * n2 / 2, math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    return U, 0.5 * math.erfc((U - mu) / sd / math.sqrt(2))


sym = {}
for line in open('survey/sym_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): sym[int(w[0])] = float(w[3])


def arith(p):
    g = primroot(p); ind = np.zeros(p, dtype=np.int64); x = 1
    for e in range(p - 1): ind[x] = e; x = x * g % p
    xs = np.arange(1, p - 1)
    A = np.bincount((ind[xs] % 6) * 6 + ind[xs + 1] % 6, minlength=36).reshape(6, 6).astype(float)
    h = int(ind[p - 1] % 6)
    t = (A[0, h] - A.mean()) / math.sqrt(p)
    cube2 = ind[2] % 3 == 0
    a = None
    for b in range(1, int(math.isqrt(p // 3)) + 1):
        r = p - 3 * b * b; s = math.isqrt(r)
        if s * s == r:
            a = s if s % 3 == 1 else -s
            break
    return h, t, bool(cube2), a


rows = []
for p in PRIMES:
    pre = 'split/split_k6_p%d' % p if p in OLD else 'split/split13_k6_p%d' % p
    if not os.path.exists(pre + '.log') or not os.path.exists(pre + '_str.npz'): continue
    m = re.search(r'S=(\d+) conf=(\d+) N1/mu1=([\d.]+).*structured share ([\d.]+) \(S-batch se ([\d.]+)\)', open(pre + '.log').read())
    if not m: continue
    nS, conf, N, share, se = int(m.group(1)), int(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5))
    sv = re.search(r'S=(\d+) conf=(\d+) .*N1/mu1=([\d.]+)', open('survey/mc_k6_p%d_s13.log' % p).read())
    same = sv and int(sv.group(1)) == nS and int(sv.group(2)) == conf and abs(float(sv.group(3)) - N) < 1e-3
    rs, ru = ks.analyse(pre + '_str.npz'), ks.analyse(pre + '_uns.npz')
    h, t, cube2, a = arith(p)
    rows.append(dict(p=p, lam=p / 6 ** 5, N=N, share=share, se=se, F=share * N * p * p / R22, same=bool(same),
                     new=p not in OLD, sym=sym.get(p, float('nan')), h=h, t=t, cube2=cube2, a=a, ar=abs(a) / math.sqrt(p),
                     DL=(rs['L'], ru['L']), DD=(rs['D'], rs['D_z'], ru['D'], ru['D_z'])))

print('%d of 29 primes have a seed-13 split (%d new)' % (len(rows), sum(r['new'] for r in rows)))
print('    p   lam   N1/mu1  share (se)    F     new same-as-survey  h cube2  |a|/rp   t      symR   | B_L str/uns   B_D str (z) / uns (z)')
for r in rows:
    print('%5d %.3f  %6.2f  %.3f (%.3f) %5.2f   %s   %s   %d  %s  %.3f  %+.3f  %6.1f   | %.3f / %.3f   %6.2f (%4.1f) / %6.2f (%4.1f)%s' % (
        r['p'], r['lam'], r['N'], r['share'], r['se'], r['F'], 'y' if r['new'] else '-', 'y' if r['same'] else 'NO',
        r['h'], 'y' if r['cube2'] else 'n', r['ar'], r['t'], r['sym'], r['DL'][0], r['DL'][1], *r['DD'], '  sD' if r['p'] in SD else ''))
new = [r for r in rows if r['new']]
col = lambda q, rr: [x[q] for x in rr]
for nm, lo, hi in (('lam < 0.22', 0, 0.22), ('lam 0.22-0.25', 0.22, 0.2501)):
    b = [r for r in rows if lo <= r['lam'] < hi]
    if b: print('band %s: n %d, F median %.2f, max %.2f (%d), min %.2f; share median %.3f, range %.3f-%.3f' % (
        nm, len(b), np.median(col('F', b)), max(col('F', b)), max(b, key=lambda r: r['F'])['p'], min(col('F', b)),
        np.median(col('share', b)), min(col('share', b)), max(col('share', b))))
if new:
    sh = col('share', new); Nn = col('N', new); Fn = col('F', new)
    print('(F1) shares of the %d new primes in [0.60, 0.92]: %s (range %.3f-%.3f)' % (len(new), all(0.60 <= s <= 0.92 for s in sh), min(sh), max(sh)))
    print('(F2) max F among the new primes %.2f (%d): %s' % (max(Fn), max(new, key=lambda r: r['F'])['p'], 'kept' if max(Fn) <= 4.0 else 'REFUTED'))
    print('(F3) Spearman(F, N1/mu1) over the new primes %.3f: %s' % (spearman(Fn, Nn), 'kept' if spearman(Fn, Nn) >= 0.90 else 'REFUTED'))
    s4 = spearman(sh, Nn)
    print('(F4) Spearman(share, N1/mu1) over the new primes %.3f: %s' % (s4, 'kept' if s4 > 0.34 else 'REFUTED'))
    s5 = spearman([(1 - s) * n for s, n in zip(sh, Nn)], Nn)
    print('(F5) Spearman((1-share) N1/mu1, N1/mu1) over the new primes %.3f: %s' % (s5, 'kept' if s5 >= 0.5 else 'REFUTED'))
    f6 = [(r['p'], r['DD'][0], r['DD'][2]) for r in new if r['p'] in SD]
    print('(F6) B_D(2+2) > B_D(rest) at the new sD primes: %s  %s' % (all(x > y for _, x, y in f6) if f6 else 'n/a', f6))
    sha, Na, Fa = col('share', rows), col('N', rows), col('F', rows)
    print('     also over all %d: shares %.3f-%.3f; max F %.2f (%d); Spearman(F, N1/mu1) %.3f; (share, N1/mu1) %.3f; ((1-share) N1/mu1, N1/mu1) %.3f' % (
        len(rows), min(sha), max(sha), max(Fa), max(rows, key=lambda r: r['F'])['p'], spearman(Fa, Na), spearman(sha, Na),
        spearman([(1 - s) * n for s, n in zip(sha, Na)], Na)))
s7 = spearman(col('F', rows), col('ar', rows))
print('(F7) over all %d: Spearman(F, |a|/sqrt p) %.3f: %s' % (len(rows), s7, 'kept' if s7 > 0 else 'REFUTED'))
h0 = [r for r in rows if r['h'] == 0]
c, nc = [r['F'] for r in h0 if r['cube2']], [r['F'] for r in h0 if not r['cube2']]
if c and nc: print('     h = 0: median F with 2 a cube %.2f (n %d) against %.2f (n %d): %s' % (np.median(c), len(c), np.median(nc), len(nc), 'kept' if np.median(c) > np.median(nc) else 'REFUTED'))
if len(h0) > 2:
    s7t = spearman(col('F', h0), [abs(r['t']) for r in h0])
    print('     h = 0: Spearman(F, |A(0,0) - mean|/sqrt p) %.3f (n %d): %s' % (s7t, len(h0), 'kept' if s7t > 0 else 'REFUTED'))
print('Also: Spearman over all %d of F with symR %.3f; share with symR %.3f; share with N1/mu1 %.3f' % (
    len(rows), spearman(col('F', rows), col('sym', rows)), spearman(col('share', rows), col('sym', rows)), spearman(col('share', rows), col('N', rows))))
c1, c7 = [r['share'] for r in rows if r['h'] == 0], [r['share'] for r in rows if r['h'] == 3]
if c1 and c7:
    U, P = mw_less(c1, c7)
    print('     share by class (exploratory): median %.3f (p = 1 mod 12, n %d) against %.3f (p = 7 mod 12, n %d); one-sided MW (1 > 7) p %.3f' % (
        np.median(c1), len(c1), np.median(c7), len(c7), P))
print('All rows reproduce their survey run (S, conf and N1/mu1): %s' % all(r['same'] for r in rows))
