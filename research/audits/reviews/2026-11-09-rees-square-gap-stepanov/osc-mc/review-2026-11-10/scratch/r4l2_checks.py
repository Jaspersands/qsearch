"""Referee round 4l part 2: the equal-lambda kappa = 8 draw, and a few-second success-rate/timing probe at lambda ~ 0.3.
Run: nice -n 19 /opt/anaconda3/bin/python -I r4l2_checks.py > r4l2_checks.out"""
import math, time
import numpy as np
def isprime(n):
    if n % 2 == 0: return False
    return all(n % q for q in range(3, int(n ** .5) + 1, 2))
lo, hi = math.ceil(0.29 * 8 ** 7), math.floor(0.31 * 8 ** 7)
pool = [q for q in range(lo, hi + 1) if q % 8 == 1 and isprime(q)]
draw = sorted(int(x) for x in np.random.default_rng(2028).choice(pool, 24, replace=False))
listed = [608737, 611297, 617129, 617233, 618929, 620441, 621617, 622241, 622313, 623417, 623929, 624209, 624809, 627617,
          630689, 632041, 634441, 636721, 638081, 643009, 643273, 647641, 647809, 648889]
print('pool %d (%d-%d); draw matches listed %s; lambda %.3f-%.3f; disjoint from the 0.18 band: True' % (
    len(pool), pool[0], pool[-1], draw == listed, min(draw) / 8 ** 7, max(draw) / 8 ** 7))
# probe: success rate and ms/attempt at p = 623417 (same sampler as r4l_checks.py, order t1, s1, ...)
k, p = 8, 623417
fs = [q for q in range(2, 200) if (p - 1) % q == 0 and isprime(q) or q == 2 and (p - 1) % 2 == 0]
g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in {2} | {q for q in range(3, 2000) if (p - 1) % q == 0 and isprime(q)} | ({(p - 1) // math.prod([])} if False else set())))
m = p - 1; fac = set(); d = 2
while d * d <= m:
    while m % d == 0: fac.add(d); m //= d
    d += 1
if m > 1: fac.add(m)
g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fac))
ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1): ind[x] = e; x = x * g % p
chi = ind % k; chi[0] = -1; xs = np.arange(p); rng = np.random.default_rng(3); n = 300; ok = 0; W = []
t0 = time.time()
for _ in range(n):
    t1 = int(rng.integers(p)); s1 = int(rng.integers(p - 1)); s1 += s1 >= t1
    w = float(p) * (p - 1); S = [s1]; T = [t1]; cS = xs; cT = xs; c0 = int(chi[(s1 - t1) % p]); dead = False
    for step in range(2, 2 * k):
        isT = step % 2 == 0; pl = cT if isT else cS; cand = pl[~np.isin(pl, S + T)]; c = len(cand)
        if c == 0: dead = True; break
        y = int(cand[rng.integers(c)]); w *= c
        if isT:
            T.append(y); tgt = (int(chi[(s1 - y) % p]) - c0) % k; cS = cS[((chi[(cS - y) % p] - chi[(cS - t1) % p]) % k) == tgt]
        else:
            S.append(y); tgt = (int(chi[(y - t1) % p]) - c0) % k; cT = cT[((chi[(y - cT) % p] - chi[(s1 - cT) % p]) % k) == tgt]
    if not dead: ok += 1; W.append(w)
dt = time.time() - t0; W = np.array(W)
print('k=8 p=%d lambda %.3f: %d attempts, %d successes (%.3f), %.1f ms/attempt, ESS frac %.2f' % (
    p, p / 8 ** 7, n, ok, ok / n, 1000 * dt / n, (W.sum() ** 2 / (W ** 2).sum() / len(W)) if len(W) else 0))
