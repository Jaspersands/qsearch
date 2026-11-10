"""Referee round 4i: kappa = 4, split iota.  k4_22.py adds the pole's key as the 8th fixed key when only 7 are witnessed,
without checking it is sigma-fixed.  Here the 8 sigma-fixed keys come from enumeration (as in r4i_checks.py); for each
split iota: (i) how many fixed keys are witnessed (finite t not in S, not the pole; fixed points of iota count, as in k4_22.py); (ii) when 7 are, whether the missing one is the
pole's key; (iii) whether a fixed key's bucket ever holds a non-exceptional point without being witnessed (it cannot).
sigma maps key(t0) to key(iota t0) = key(infinity) = 0, so the pole's key is sigma-fixed iff key(t0) = 0.
Run: nice -n 19 /opt/anaconda3/bin/python -I r4i_pole.py > r4i_pole.out"""
import itertools
import numpy as np


def primroot(p):
    fs = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, int(q ** .5) + 1))]
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fs))


k = 4
for p, nS in ((197, 400), (401, 300)):
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1): ind[x] = e; x = x * g % p
    chi = ind % k; xs = np.arange(p); kp = k ** np.arange(k - 1)
    inv = np.zeros(p, dtype=np.int64); inv[1:] = [pow(i, p - 2, p) for i in range(1, p)]
    rng = np.random.default_rng(7 + p); hist = {}; seven = 0; seven_pole = 0; pole_fixed = 0; nsplit = 0; rule_used = {}; rule_wrong = {}
    for _ in range(nS):
        S = [int(v) for v in rng.choice(p, k, replace=False)]
        D = (np.array(S)[None, :] - xs[:, None]) % p; prof = chi[D]; inS = (D == 0).any(1)
        key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp
        for (i, j, u, v) in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):
            a_, b_, c_, d_ = S[i], S[j], S[u], S[v]
            ga = (a_ + b_ - c_ - d_) % p; al = (a_ * b_ - c_ * d_) % p; be = (ga * a_ * b_ - al * (a_ + b_)) % p
            A, B, C, Dd = al, be, ga, (-al) % p; det = (A * Dd - B * C) % p
            if ind[(-det) % p] % 2: continue
            nsplit += 1
            img = {i: j, j: i, u: v, v: u}; alpha = {l: (-ind[(C * S[l] + Dd) % p]) % k for l in range(4)}
            fix = set()
            for P in itertools.product(range(k), repeat=3):
                P = (0,) + P
                Q = [0] * 4
                for l in range(4): Q[img[l]] = P[l] + alpha[l]
                if all((Q[l] - Q[0]) % k == P[l] for l in range(4)): fix.add(int(np.dot(P[1:], kp)))
            assert len(fix) == 8
            den = (C * xs + Dd) % p; ok = (~inS) & (den != 0)
            im = np.full(p, -1, dtype=np.int64); im[ok] = (A * xs[ok] + B) % p * inv[den[ok]] % p
            wit = set(int(K) for K in key[ok]) & fix
            hist[len(wit)] = hist.get(len(wit), 0) + 1
            t0 = int((-Dd) * pow(C, p - 2, p) % p) if C else None
            pk = int(key[t0]) if t0 is not None and not inS[t0] else None
            if pk is not None and pk in fix: pole_fixed += 1
            full = bool((np.bincount(key[~inS], minlength=k ** 3) > 0).all())
            if len(wit) == 7:
                seven += 1; miss = (fix - wit).pop(); seven_pole += int(pk == miss)
                if pk is not None and pk not in wit:   # k4_22.py adds pk here
                    rule_used[full] = rule_used.get(full, 0) + 1; rule_wrong[full] = rule_wrong.get(full, 0) + int(pk not in fix)
    print('p=%d: %d split iota; witnessed fixed keys histogram %s; pole key sigma-fixed in %d; '
          'of %d cases with 7 witnessed, the missing key is the pole key in %d' % (
              p, nsplit, dict(sorted(hist.items())), pole_fixed, seven, seven_pole))
    print('   k4_22 rule (7 witnessed, add the pole key): used %s times [keyed by all-64-nonempty], adds a NON-fixed key %s times' % (
              rule_used, rule_wrong))
