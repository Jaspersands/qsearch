"""Author's independent checks of round-3 findings 1 and 6 (scratch)."""
import sys, math, re, glob
import numpy as np
from scipy.stats import spearmanr
def rep_a(p):   # p = a^2 + 3 b^2, a = 1 mod 3 (sign fixed), return a, b
    for b in range(0, int(math.isqrt(p // 3)) + 1):
        r = p - 3 * b * b
        a = math.isqrt(r)
        if a * a == r:
            a = a if a % 3 == 1 else -a
            return a, b
def rep_L(p):   # 4p = L^2 + 27 M^2, L = 1 mod 3
    for M in range(0, int(math.isqrt(4 * p // 27)) + 1):
        r = 4 * p - 27 * M * M
        L = math.isqrt(r)
        if L * L == r:
            L = L if L % 3 == 1 else -L
            return L, M
sym = {}
for line in open('survey/sym_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): sym[int(w[0])] = (float(w[1]), float(w[3]))
print('finding 1: a vs L')
for p in (1951, 3571, 4219, 3889, 1597, 1657, 1621):
    a, b = rep_a(p); L, M = rep_L(p)
    print('  p %d  a %d b %d  |a|/rp %.3f   L %d M %d  |L|/(2rp) %.3f  2 cube: %s  symR %s' % (p, a, b, abs(a) / math.sqrt(p), L, M, abs(L) / (2 * math.sqrt(p)), b % 3 == 0, sym.get(p, ('-', '-'))[1]))
hi = sorted((q for q in sym if sym[q][0] > 0.45), key=lambda q: -sym[q][1])
print('  lambda > 0.45: %d primes; top symR:' % len(hi), [(q, sym[q][1]) for q in hi[:4]])
# residual of log symR on log lambda (simple linear detrend), lambda <= 0.31
lo = sorted(q for q in sym if sym[q][0] <= 0.31)
x = np.log([sym[q][0] for q in lo]); y = np.log([sym[q][1] for q in lo])
c = np.polyfit(x, y, 1); res = y - np.polyval(c, x)
A = [abs(rep_a(q)[0]) / math.sqrt(q) for q in lo]; Lr = [abs(rep_L(q)[0]) / (2 * math.sqrt(q)) for q in lo]
print('  n=%d (lambda<=0.31) Spearman(res, |a|/rp) %.2f  Spearman(res, |L|/2rp) %.2f  cube primes %d' % (
    len(lo), spearmanr(res, A)[0], spearmanr(res, Lr)[0], sum(rep_a(q)[1] % 3 == 0 for q in lo)))
print('finding 6: lambda-term')
meas = {}
for f in glob.glob('survey/mc_k6_p*_s13.log') + ['mc_k6_p3877_sb.log']:
    for line in open(f):
        m = re.search(r'p=(\d+) lambda=([\d.]+) S=(\d+) conf=(\d+).*N1/mu1=([\d.]+)', line)
        if m: meas[int(m.group(1))] = float(m.group(5))
fit = [1531, 1543, 1549, 1567, 1579, 1597, 1609, 1621, 1627, 1657, 1663, 1669, 1693, 3877]
pro = [1699, 1723, 1741, 1747, 1753, 1759, 1777, 1783, 1789, 1801, 1831, 1861, 1873]
def design(qs): return np.array([[1, math.log(sym[q][1]), math.log(sym[q][0])] for q in qs])
for lab, qs in (('as filed (14 incl 3877)', fit), ('without 3877', fit[:-1])):
    X = design(qs); yv = np.log([meas[q] for q in qs])
    co, *_ = np.linalg.lstsq(X, yv, rcond=None)
    e = np.log([meas[q] for q in pro]) - design(pro) @ co
    print('  %-24s coef %s  prospective mean %+.3f rms %.3f  (n=%d)' % (lab, np.round(co, 3), e.mean(), math.sqrt((e ** 2).mean()), len(pro)))
print('  measured N1/mu1 available for', len([q for q in pro if q in meas]), 'prospective primes; 1867, 1879 in meas:', 1867 in meas, 1879 in meas)
