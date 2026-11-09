"""Do the order-k cyclotomic numbers predict the (C1) configuration excess N1/mu1?
Heuristic: a configuration needs T (k distinct points) inside one S-bucket.  Send three points of S to
(inf, 0, 1) by PGL_2; then every t in T must have the same cyclotomic class (ind(-t), ind(1-t)) mod k,
a condition that is the SAME for every S (3-transitivity), while the remaining k-3 coordinates
ind(s_j - t) vary with S.  If those behave like independent uniform labels, the expected number of
configurations per S, relative to the random model, is
    R_k(p) = k^(2(k-1)) * sum_{a,b} (A_ab)_k / (p-2)_k,      A_ab = #{t != 0,1 : ind(-t) = a, ind(1-t) = b mod k},
with (x)_k the falling factorial.  The same argument with j points gives R_j, the predicted j-th
factorial moment of the bucket occupancy relative to Poisson (compare bucket_stats.py).
Prints R_j (j = 2..k+1) for the given primes, and, for k = 6, the measured N1/mu1 of the Monte Carlo
logs next to R_6.
Usage: python cyclo_R.py k p [p ...]      or      python cyclo_R.py 6 logs   (all mc_k6 logs here)"""
import sys, glob, re, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot


def cyclo(p, k):
    g = primroot(p); ind = np.zeros(p, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    t = np.arange(2, p)
    a = ind[(-t) % p] % k; b = ind[(1 - t) % p] % k
    return np.bincount(a * k + b, minlength=k * k).reshape(k, k)


def ff(x, j):
    return np.prod([x - i for i in range(j)], axis=0).astype(float)


def R(p, k, j, A=None):
    A = cyclo(p, k) if A is None else A
    return float(k ** (2 * (j - 1)) * ff(A.astype(float), j).sum() / ff(np.array([float(p - 2)]), j)[0])


if __name__ == '__main__':
    k = int(sys.argv[1])
    if sys.argv[2:] == ['logs']:
        meas = {}
        for f in sorted(glob.glob('mc_k%d_p*.log' % k) + glob.glob('survey/mc_k%d_p*.log' % k)):
            for line in open(f):
                m = re.search(r'p=(\d+) lambda=([\d.]+) S=(\d+) conf=(\d+).*N1/mu1=([\d.]+)', line)
                if m:
                    meas.setdefault(int(m.group(1)), []).append((float(m.group(5)), int(m.group(4)), f))
        ps = sorted(meas)
    else:
        ps = [int(x) for x in sys.argv[2:]]; meas = {}
    print('  p      lam    ' + '  '.join('R_%d' % j for j in range(2, k + 2)) + '    N1/mu1 (MC: value, conf, file)')
    for p in ps:
        A = cyclo(p, k)
        rs = [R(p, k, j, A) for j in range(2, k + 2)]
        extra = '  '.join('%.3f (%d %s)' % m for m in meas.get(p, []))
        print('%6d  %5.3f  ' % (p, p / k ** (k - 1)) + '  '.join('%5.3f' % r for r in rs) + '    ' + extra)
    if meas:
        x = np.array([R(p, k, k) for p in ps]); y = np.array([np.mean([m[0] for m in meas[p]]) for p in ps])
        rk = lambda v: np.argsort(np.argsort(v))
        print('Spearman(R_%d, N1/mu1) = %.2f over %d primes;  Pearson(log R, log N1/mu1) = %.2f' % (
            k, np.corrcoef(rk(x), rk(y))[0, 1], len(ps), np.corrcoef(np.log(x), np.log(y))[0, 1]))
