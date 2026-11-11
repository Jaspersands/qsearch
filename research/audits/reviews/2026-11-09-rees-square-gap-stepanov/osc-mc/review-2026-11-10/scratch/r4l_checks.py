"""Referee round 4l (11 Nov): independent checks of the kappa = 8 (C1) sampler scope (predictions_k8_c1_sampler.txt).
Own sampler, own code: order t1, s1, t2, s2, ... (the mirror of the proposal's s1, t1, ...), index lists, W = product of
candidate counts.  It does not import mc_classes.
 A. Exact small case: kappa = 3, p = 31 and kappa = 4, p = 53: exact number of unordered (C1) pairs by enumerating all S
    (mc_classes' bucket rule), against E[W]/k!^2 from the sampler.
 B. N1/mu1 at kappa = 7, p = 34259 and kappa = 6, p = 1621; weighted mean of (b - k), b the T-bucket size, against
    lambda (under Poisson buckets the (C1) measure makes b - k ~ Poisson(lambda)), weighted and unweighted.
 C. kappa = 8, p = 377513: success rate, ESS fraction by chunk, max-weight share, per-step count CV; timing.
 D. The band run's N1/mu1 se (k6_spike_survey's formula, recomputed); E. the K8 pool and draw; F. room numbers.
Run: nice -n 19 /opt/anaconda3/bin/python -I r4l_checks.py > r4l_checks.out"""
import math, time, itertools
import numpy as np

def primroot(p):
    fs = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, int(q ** .5) + 1))]
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fs))
def chitab(p, k):
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1): ind[x] = e; x = x * g % p
    c = ind % k; c[0] = -1; return c

def sampler(k, p, n, seed, chi, want_b=False):
    xs = np.arange(p); rng = np.random.default_rng(seed); out = []; counts = []
    for _ in range(n):
        t1 = int(rng.integers(p)); s1 = int(rng.integers(p - 1)); s1 += s1 >= t1
        w = float(p) * (p - 1); S = [s1]; T = [t1]; cS = xs; cT = xs; c0 = int(chi[(s1 - t1) % p]); dead = False; cc = []
        for step in range(2, 2 * k):
            isT = step % 2 == 0                     # t2, s2, t3, s3, ...
            pool = cT if isT else cS
            cand = pool[~np.isin(pool, S + T)]; c = len(cand); cc.append(c)
            if c == 0: dead = True; break
            y = int(cand[rng.integers(c)]); w *= c
            if isT:   # new t constrains future s: ind(s - y) - ind(s - t1) = ind(s1 - y) - ind(s1 - t1)
                T.append(y); tgt = (int(chi[(s1 - y) % p]) - c0) % k
                cS = cS[((chi[(cS - y) % p] - chi[(cS - t1) % p]) % k) == tgt]
            else:     # new s constrains future t: ind(y - t) - ind(s1 - t) = ind(y - t1) - ind(s1 - t1)
                S.append(y); tgt = (int(chi[(y - t1) % p]) - c0) % k
                cT = cT[((chi[(y - cT) % p] - chi[(s1 - cT) % p]) % k) == tgt]
        counts.append(cc + [0] * (2 * k - 2 - len(cc)))
        if dead: out.append((0.0, None)); continue
        Sa, Ta = np.array(S), np.array(T); Mx = chi[(Sa[:, None] - Ta[None, :]) % p]
        assert (((Mx - Mx[:, :1] - Mx[:1, :] + Mx[0, 0]) % k) == 0).all() and len(set(S + T)) == 2 * k
        b = None
        if want_b:
            D = (Sa[None, :] - xs[:, None]) % p; prof = chi[D]; inS = (D == 0).any(1)
            key = ((prof[:, 1:] - prof[:, :1]) % k) @ (k ** np.arange(k - 1)); key[inS] = -1
            b = int((key == key[Ta[0]]).sum())
        out.append((w, b))
    return out, np.array(counts, dtype=float)

def mu1(k, p):
    return math.prod(range(p - 2 * k + 1, p - 1)) * float(k) ** (-(k - 1) ** 2)

print('A. Exact small cases: unordered (C1) pairs by enumeration over all S, against the sampler')
for k, p, n in ((3, 31, 40000), (4, 53, 40000)):
    chi = chitab(p, k); xs = np.arange(p); tot = 0
    for S in itertools.combinations(range(p), k):
        Sa = np.array(S); D = (Sa[None, :] - xs[:, None]) % p; prof = chi[D]; inS = (D == 0).any(1)
        key = ((prof[:, 1:] - prof[:, :1]) % k) @ (k ** np.arange(k - 1)); key[inS] = -1
        bc = np.bincount(key[~inS]); tot += sum(math.comb(int(b), k) for b in bc)
    out, _ = sampler(k, p, n, 1, chi); W = np.array([w for w, _ in out]) / math.factorial(k) ** 2
    print('  k=%d p=%d: exact %d pairs; sampler E[W]/k!^2 = %.1f +- %.1f (%d attempts); N1/mu1 exact %.4f' % (
        k, p, tot, W.mean(), W.std(ddof=1) / math.sqrt(n), n, tot * math.factorial(k) ** 2 / (p * (p - 1)) / mu1(k, p)))

print('\nB. N1/mu1 and the bucket-size check')
for k, p, n, seeds in ((7, 34259, 2500, (5, 6)), (6, 1621, 2500, (5,))):
    chi = chitab(p, k); lam = p / k ** (k - 1)
    for sd in seeds:
        t0 = time.time(); out, cnts = sampler(k, p, n, sd, chi, want_b=True); dt = time.time() - t0
        W = np.array([w for w, _ in out]); f = 1 / (p * (p - 1)) / mu1(k, p)
        ok = W > 0; b = np.array([bb for w, bb in out if w > 0]); Ws = W[ok]
        ess = Ws.sum() ** 2 / (Ws ** 2).sum()
        print('  k=%d p=%d lambda %.3f seed %d: %d attempts, %d successes, %.1f ms/attempt; N1/mu1 %.3f +- %.3f; ESS %.2f of successes;'
              ' E_w[b-k] %.3f (unweighted %.3f; lambda %.3f)' % (k, p, lam, sd, n, ok.sum(), 1000 * dt / n, W.mean() * f,
                                                                W.std(ddof=1) / math.sqrt(n) * f, ess / ok.sum(), (Ws * (b - k)).sum() / Ws.sum(), (b - k).mean(), lam))

print('\nC. kappa = 8, p = 377513 (lambda %.3f)' % (377513 / 8 ** 7))
k, p = 8, 377513; chi = chitab(p, k)
allW = []
for sd in (5, 6):
    t0 = time.time(); out, cnts = sampler(k, p, 700, sd, chi); dt = time.time() - t0
    W = np.array([w for w, _ in out]); Ws = W[W > 0]; allW.append(Ws)
    f = 1 / (p * (p - 1)) / mu1(k, p)
    reach = cnts > 0
    cv = ['%.2f' % (cnts[reach[:, j], j].std() / cnts[reach[:, j], j].mean()) if reach[:, j].sum() > 5 else '-' for j in range(cnts.shape[1])]
    mean = ['%.3g' % cnts[reach[:, j], j].mean() if reach[:, j].any() else '-' for j in range(cnts.shape[1])]
    print('  seed %d: 700 attempts, %d successes (%.3f), %.1f ms/attempt; N1/mu1 %.2f +- %.2f; ESS %.2f of successes; max weight share %.3f' % (
        sd, len(Ws), len(Ws) / 700, 1000 * dt / 700, W.mean() * f, W.std(ddof=1) / math.sqrt(700) * f,
        Ws.sum() ** 2 / (Ws ** 2).sum() / len(Ws), Ws.max() / Ws.sum()))
    print('    per-step mean count (t2 s2 t3 ...): %s\n    per-step CV: %s' % (' '.join(mean), ' '.join(cv)))
Wa = np.concatenate(allW); Wa = Wa / Wa.mean(); r = np.sort(Wa)[::-1]
kk = max(5, len(r) // 5); hill = np.mean(np.log(r[:kk] / r[kk]))
print('  pooled %d successes: ESS frac %.2f; normalised weights: max %.2f, 99%% %.2f, sd %.2f; Hill of top 20%% %.2f (tail index %.1f; finite variance needs > 2)' % (
    len(Wa), 1 / np.mean(Wa ** 2), r[0], np.percentile(Wa, 99), Wa.std(), hill, 1 / hill))

print('\nD. Band run 34259 N1/mu1 se (rate = cnt_b / nS_b)')
d = np.load('/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-kZ9WMM/2e593e3c-5bbe-4d57-9307-748faf30eaee/scratchpad/mc_k7_p34259_s19.npz')
nS = int(d['nS']); B = len(d['cnt']); nSb = np.array([len(range(b, nS, B)) for b in range(B)]); rate = d['cnt'] / nSb
v = float(d['N1']) / float(d['mu1'])
print('  N1/mu1 %.4f, se %.4f (cnt_b sd %.1f)' % (v, v * rate.std(ddof=1) / math.sqrt(B) / rate.mean(), d['cnt'].std(ddof=1)))

print('\nE. K8 pool and draw')
def isprime(n):
    if n % 2 == 0: return False
    return all(n % q for q in range(3, int(n ** .5) + 1, 2))
lo, hi = math.ceil(0.17 * 8 ** 7), math.floor(0.19 * 8 ** 7)
pool = [q for q in range(lo, hi + 1) if q % 8 == 1 and isprime(q)]
draw = sorted(int(x) for x in np.random.default_rng(2027).choice(pool, 24, replace=False))
listed = [357073, 357169, 360257, 360769, 361577, 362233, 362977, 368513, 369097, 372817, 373073, 375553, 376633, 377353,
          377681, 379369, 379817, 382601, 382649, 383729, 384913, 385817, 387161, 394153]
print('  pool %d primes (%d-%d); draw matches listed: %s; lambda range %.3f-%.3f; 377513 in pool %s' % (
    len(pool), pool[0], pool[-1], draw == listed, min(draw) / 8 ** 7, max(draw) / 8 ** 7, 377513 in pool))

print('\nF. Rooms')
for k, lt in ((7, 5.57), (8, 6.18)):
    lnT = lt * math.log(k); lnN = lnT - math.log({7: 6, 8: 4}[k]) - math.log(lnT)
    room = (0.5 - 1 / (2 * math.log(k))) * k; c = math.sqrt(2 * lnN) / math.log(k)
    print('  k=%d: log_k N_T %.3f, L room %.3f, growth coefficient sqrt(2 ln N_T)/ln k %.3f, sigma filling the room %.2f; lambda_T %.3f' % (
        k, lnN / math.log(k), room, c, room / c, k ** (lt - (k - 1))))
print('  kappa = 6 lambda effect on sigma_L: (0.19,0.25] / (0.25,0.31] = 0.494/0.352 = %.2f; per unit ln(lambda) %.2f' % (
    0.494 / 0.352, math.log(0.494 / 0.352) / math.log(0.28 / 0.22)))
