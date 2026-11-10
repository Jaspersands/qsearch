"""Referee round 4k-a (11 Nov): the proposed tail test (sec12_14_draft.md, predictions_k7_tail.txt).  Synthetic only,
no npz reads except none; small CPU.
 A. Finite-kappa budget: log_k N_T and the gamma at which the sup would use the whole L / D tolerance (no O(1)).
 B. Operating characteristics of the rules: Hill k = floor(N/4) on N = 24 with a 2000-resample percentile bootstrap,
    under Pareto(gamma) and lognormal(sigma) populations; P(T1 HEAVIER / LIGHTER), P(T2 WITHIN / EXCEEDS); coverage.
 C. Measurement noise (multiplicative, log-sd eps) and a noise floor: bias of Hill.
 D. Alternatives: robust log-spread sigma = IQR(ln B)/1.349 and exceedance count X > 2; their sampling noise.
 E. The sample: primes p = 1 mod 7 with lambda = p/7^6 in [0.29, 0.31]; attempts to reproduce the rng(2026) draw.
Run:  nice -n 19 /opt/anaconda3/bin/python -I r4ka_checks.py > r4ka_checks.out"""
import math
import numpy as np

print('A. Finite-kappa budget (log_k T from the note; N_T = T/(phi(k) ln T) primes = 1 mod k in [T, 2T])')
phi = {7: 6, 8: 4, 9: 6, 10: 4}
for k, lt in ((7, 5.57), (8, 6.18), (9, 6.78), (10, 7.36)):
    lnT = lt * math.log(k); lnN = lnT - math.log(phi[k]) - math.log(lnT); lN = lnN / math.log(k)
    tL = (0.5 - 1 / (2 * math.log(k))) * k; tD = (1 - 1 / math.log(k)) * k
    print('  k=%2d: log_k N_T %.2f (k/2 = %.1f); tolerance L %.2f, D %.2f; gamma using all of it: L %.2f, D %.2f;'
          ' fraction per unit gamma: L %.2f, D %.2f' % (k, lN, k / 2, tL, tD, tL / lN, tD / lN, lN / tL, lN / tD))

def hill_rows(A, k):
    S = -np.sort(-A, axis=-1)
    return np.mean(np.log(S[..., :k] / S[..., k:k + 1]), axis=-1)

rng = np.random.default_rng(11)
N, K, NB, REPS = 24, 6, 2000, 300
def oc(sample, label):
    g = np.empty(REPS); lo = np.empty(REPS); hi = np.empty(REPS)
    for r in range(REPS):
        x = sample(N); g[r] = hill_rows(x[None, :], K)[0]
        bs = hill_rows(x[rng.integers(0, N, (NB, N))], K); lo[r], hi[r] = np.percentile(bs, [2.5, 97.5])
    return g, lo, hi
print('\nB. Rules under synthetic populations (N 24, k 6, %d replicates, bootstrap %d)' % (REPS, NB))
print('  population            mean Hill  sd    median CI width  P(HEAVIER lo>0.49) P(LIGHTER hi<0.11) P(WITHIN hi<1) P(EXCEEDS lo>1)  CI covers truth')
for gam in (0.05, 0.1, 0.2, 0.33, 0.5, 0.75, 1.0, 1.5, 2.5):
    g, lo, hi = oc(lambda n: rng.random(n) ** (-gam), 'pareto')
    print('  Pareto gamma %.2f       %.3f    %.3f  %.3f            %.2f               %.2f               %.2f           %.2f             %.2f' % (
        gam, g.mean(), g.std(), np.median(hi - lo), (lo > 0.49).mean(), (hi < 0.11).mean(), (hi < 1).mean(), (lo > 1).mean(),
        ((lo <= gam) & (gam <= hi)).mean()))
for sig in (0.3, 0.45, 0.7, 1.0):
    g, lo, hi = oc(lambda n: np.exp(sig * rng.standard_normal(n)), 'lognormal')
    print('  lognormal sigma %.2f    %.3f    %.3f  %.3f            %.2f               %.2f               %.2f           %.2f             (no power tail)' % (
        sig, g.mean(), g.std(), np.median(hi - lo), (lo > 0.49).mean(), (hi < 0.11).mean(), (hi < 1).mean(), (lo > 1).mean()))
print('  lognormal: the sup over N_T draws is median * exp(sigma sqrt(2 ln N_T)) -> log_k ratio at k=7, N_T=7^3.35: '
      + ', '.join('sigma %.2f: %.2f' % (s, s * math.sqrt(2 * 3.35 * math.log(7)) / math.log(7)) for s in (0.3, 0.45, 0.7, 1.0)))

print('\nC. Measurement noise on Hill (Pareto gamma 0.33, N 24, k 6, 4000 replicates)')
for eps in (0.0, 0.05, 0.12, 0.25):
    x = rng.random((4000, N)) ** (-0.33) * np.exp(eps * rng.standard_normal((4000, N)))
    print('  multiplicative noise log-sd %.2f: mean Hill %.3f' % (eps, hill_rows(x, K).mean()))
x = rng.random((4000, N)) ** (-0.83); x[:, :10] = 1e-6   # 10 of 24 B_D at the floor (unresolved, noise-subtracted to 0)
print('  B_D with 10 of 24 floored at 1e-6 (gamma 0.83): mean Hill %.3f; with 18 floored: %.1f' % (
    hill_rows(x, K).mean(), hill_rows(np.where(np.arange(N) < 18, 1e-6, rng.random((4000, N)) ** (-0.83)), K).mean()))

print('\nD. Alternatives (N 24)')
for sig in (0.45, 0.7):
    z = sig * rng.standard_normal((4000, N)); q = np.percentile(z, [25, 75], axis=1); s = (q[1] - q[0]) / 1.349
    sd = z.std(axis=1, ddof=1)
    X = np.exp(z - np.median(z, axis=1, keepdims=True)); c = (X > 2).sum(1)
    print('  lognormal sigma %.2f: IQR-sigma mean %.3f sd %.3f (rel %.2f); plain sd of ln B rel sd %.2f; #X>2 mean %.2f sd %.2f' % (
        sig, s.mean(), s.std(), s.std() / s.mean(), sd.std() / sd.mean(), c.mean(), c.std()))
for gam in (0.33, 0.5):
    X = rng.random((4000, N)) ** (-gam); X = X / np.median(X, axis=1, keepdims=True); c = (X > 2).sum(1)
    print('  Pareto gamma %.2f: #X>2 mean %.2f sd %.2f' % (gam, c.mean(), c.std()))

print('\nE. The sample window')
def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
lo_, hi_ = math.ceil(0.29 * 7 ** 6), math.floor(0.31 * 7 ** 6)
P = [p for p in range(lo_, hi_ + 1) if p % 7 == 1 and isprime(p)]
print('  primes = 1 mod 7 with lambda in [0.29, 0.31]: %d (p %d-%d); 36541 has lambda %.4f (inside: %s)' % (
    len(P), P[0], P[-1], 36541 / 7 ** 6, 36541 in P))
band = [34259, 34273, 34469, 34847, 35099, 35281, 36541]; picked = [36037, 34693]
pool = [p for p in P if p not in band + picked]
listed = [34147, 34217, 34231, 34511, 34651, 34679, 34721, 34819, 35141, 35393, 35533, 35603, 35617, 35771, 35897, 35911, 36107]
print('  pool (not run, not picked): %d; listed 17 all in pool: %s' % (len(pool), set(listed) <= set(pool)))
tries = {
    'rng.choice(pool, 17, replace=False)': lambda: np.random.default_rng(2026).choice(pool, 17, replace=False),
    'rng.permutation(pool)[:17]': lambda: np.random.default_rng(2026).permutation(pool)[:17],
    'pool[rng.choice(len, 17, False)]': lambda: np.array(pool)[np.random.default_rng(2026).choice(len(pool), 17, replace=False)]}
pool31 = [p for p in P if p not in band + picked] + ([36541] if 36541 not in P else [])
for nm, f in tries.items():
    print('  %-36s matches the listed set: %s' % (nm, sorted(int(v) for v in f()) == listed))
print('  kappa = 7 band ln-sd (7 primes): %.3f; IQR-sigma %.3f' % (
    np.log([0.519, 0.236, 0.131, 0.392, 0.393, 0.237, 0.245]).std(ddof=1),
    np.subtract(*np.percentile(np.log([0.519, 0.236, 0.131, 0.392, 0.393, 0.237, 0.245]), [75, 25])) / 1.349))
