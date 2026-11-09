"""Do spike primes have unusually non-uniform cyclotomic numbers?  For order k, A_ij = #{x != 0,-1 :
ind x = i, ind(x+1) = j mod k}, D = A - mean.  Parseval fixes sum D^2 (all nontrivial Jacobi sums have
modulus sqrt p), so the tests are max|D|/sqrt p and the 4th-moment ratio K = k^2 sum D^4/(sum D^2)^2.
k = 5: Spearman rank correlation with the spike score rms(4,4) p^1.4 of spike_k5.py (exact values).
k = 6: the statistics at the Monte Carlo primes, spikes 3889 and 1951 flagged.
Usage: python cyclo_spike.py"""
import sys, math, numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot, tables
def stats(p, k):
    g = primroot(p); ind = np.zeros(p, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    xs = np.arange(1, p - 1)
    A = np.bincount((ind[xs] % k) * k + ind[xs + 1] % k, minlength=k * k).astype(float)
    D = A - A.mean()
    return np.abs(D).max() / math.sqrt(p), k * k * (D ** 4).sum() / ((D ** 2).sum() ** 2)
def ranks(v):
    r = np.empty(len(v)); r[np.argsort(v)] = np.arange(len(v)); return r
k = 5
cl, R, P, orb, rb, supp, canon, base, reps = tables(k)
name = lambda c: ''.join(str(x) for x in c if x) or '0'
names = [name(c) for c in cl]
ex = np.load('../osc-bdry/class_values_k5.npz')
perm = [[name(tuple(c)) for c in ex['ms']].index(x) for x in names]
I = np.flatnonzero(supp == 4)
rows = []
for a, p in enumerate(int(x) for x in ex['ps']):
    if p < 400: continue
    V = ex['V'][a][np.ix_(perm, perm)]
    score = math.sqrt((np.abs(V[np.ix_(I, I)]) ** 2).mean()) * p ** 1.4
    mx, K = stats(p, k)
    rows.append((score, p, mx, K))
rows.sort(reverse=True)
S = np.array([r[0] for r in rows]); MX = np.array([r[2] for r in rows]); KK = np.array([r[3] for r in rows])
rho = lambda a, b: np.corrcoef(ranks(a), ranks(b))[0, 1]
print('k = 5, %d primes 401-2311: Spearman(score, max|D|/sqrt p) = %.2f, Spearman(score, K) = %.2f' % (len(rows), rho(S, MX), rho(S, KK)))
print('  top 8 by score (p, max|D|/sqrt p, K):', ' '.join('%d:%.2f/%.2f' % (r[1], r[2], r[3]) for r in rows[:8]))
print('  median over all: max|D|/sqrt p %.2f, K %.2f' % (np.median(MX), np.median(KK)))
k = 6
print('k = 6 (spikes *):', ' '.join('%d%s:%.2f/%.2f' % ((p, '*' if p in (3889, 1951) else '') + stats(p, 6))
                                   for p in (1951, 2347, 2719, 3079, 3571, 3877, 3889, 3907, 3931, 4111, 4219, 5839, 7789, 11677)))
