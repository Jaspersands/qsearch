"""Referee round 4i (10 Nov): independent checks of the sec12_13 draft (kappa = 4 closed form, kappa >= 5 shape).
Own code (no mob_from, no k4_22/k5_22): the involution of two disjoint pairs is built as (al z + be)/(ga z - al).
 A. (c s_i + d)(c s_j + d) = -det; transport P(iota t)_{iota(l)} = P(t)_l + alpha_l + beta(t) on swapped coordinates;
    sigma_iota-fixed partial keys counted by enumerating all kappa^3 normalised partial keys (not by witnesses):
    predicted c_iota * kappa, c_iota = 1 (odd kappa), 2 [split] (even kappa).  Kappa = 4, 5, 6, 7.
 B. kappa >= 5: for t in a partial-fixed bucket, paired <=> for every unswapped l,
    ind(iota(s_l) - t) - ind(s_l - t) = P(t)_j - P(t)_i + ind(c iota(s_l) + d) - ind(c s_j + d)  (mod kappa).
    (A first run had the sign of the right side reversed and reported mismatches; this is the corrected predicate.)
    Unwitnessed partial-fixed full keys at small lambda: are their buckets empty (or exceptional points only)?
 C. #{r != 0, 1 : eta(r) = eta(1 - r) = 1} = (p - 5)/4.
 D. kappa = 4 Weil numbers: eps = 192/sqrt p; where the explicit factor (1+eps)^2/(1-eps)^4 drops below 2 and 1.1.
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4i_checks.py > r4i_checks.out"""
import math, itertools
import numpy as np


def primroot(p):
    fs = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, int(q ** .5) + 1))]
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fs))


def tables(p, k):
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1): ind[x] = e; x = x * g % p
    return ind


def run(k, p, nS, seed):
    ind = tables(p, k); chi = ind % k; chi[0] = -1; xs = np.arange(p)
    inv = np.zeros(p, dtype=np.int64); inv[1:] = [pow(i, p - 2, p) for i in range(1, p)]
    rng = np.random.default_rng(seed); tot = dict(iota=0, detbad=0, trbad=0, fixbad=0, Bbad=0, Bn=0, unw=0, unw_nonempty=0, split=0)
    for _ in range(nS):
        S = [int(v) for v in rng.choice(p, k, replace=False)]
        D = (np.array(S)[None, :] - xs[:, None]) % p; prof = chi[D]; inS = (D == 0).any(1)
        key = ((prof[:, 1:] - prof[:, :1]) % k) @ (k ** np.arange(k - 1)); key[inS] = -1
        bc = np.bincount(key[~inS], minlength=k ** (k - 1))
        for (i, j), (u, v) in itertools.combinations(itertools.combinations(range(k), 2), 2):
            if len({i, j, u, v}) < 4: continue
            a_, b_, c_, d_ = S[i], S[j], S[u], S[v]
            ga = (a_ + b_ - c_ - d_) % p; al = (a_ * b_ - c_ * d_) % p; be = (ga * a_ * b_ - al * (a_ + b_)) % p
            A, B, C, Dd = al, be, ga, (-al) % p; det = (A * Dd - B * C) % p
            f = lambda z: None if (C * z + Dd) % p == 0 else (A * z + B) * pow((C * z + Dd) % p, p - 2, p) % p
            assert f(a_) == b_ and f(b_) == a_ and f(c_) == d_ and f(d_) == c_
            tot['iota'] += 1
            for (x1, x2) in ((a_, b_), (c_, d_)):
                if (C * x1 + Dd) * (C * x2 + Dd) % p != (-det) % p: tot['detbad'] += 1
            split = ind[(-det) % p] % 2 == 0 if k % 2 == 0 else None
            tot['split'] += bool(split)
            sw = [i, j, u, v]; img = {i: j, j: i, u: v, v: u}
            alpha = {l: (-ind[(C * S[l] + Dd) % p]) % k for l in sw}
            # transport on every finite, non-exceptional t
            den = (C * xs + Dd) % p; ok = (~inS) & (den != 0)
            im = np.full(p, -1, dtype=np.int64); im[ok] = (A * xs[ok] + B) % p * inv[den[ok]] % p
            ok &= (im != xs); ok[ok] &= ~inS[im[ok]]
            lhs = np.stack([prof[im[ok], img[l]] for l in sw], 1)          # P(iota t)_{iota(l)}
            rhs = np.stack([prof[ok, l] + alpha[l] for l in sw], 1)
            dif = (lhs - rhs) % k
            tot['trbad'] += int((dif != dif[:, :1]).any())
            # sigma-fixed partial keys by enumeration: partial profile (0, x, y, z) on (i, j, u, v)
            nfix = 0; fixset = set()
            for xx, yy, zz in itertools.product(range(k), repeat=3):
                P = {i: 0, j: xx, u: yy, v: zz}
                Q = {img[l]: P[l] + alpha[l] for l in sw}                  # profile of the image, at coordinate iota(l)
                q = [(Q[l] - Q[i]) % k for l in sw]
                if q == [0, xx, yy, zz]: nfix += 1; fixset.add((xx, yy, zz))
            c_pred = 1 if k % 2 else 2 * bool(split)
            if nfix != c_pred * k: tot['fixbad'] += 1
            if k >= 5 and nfix:
                pk = (prof[:, [j, u, v]] - prof[:, [i]]) % k
                inpf = (~inS) & np.array([tuple(r) in fixset for r in pk.tolist()])
                paired = np.zeros(p, dtype=bool); paired[ok] = key[im[ok]] == key[ok]
                others = [l for l in range(k) if l not in sw]
                pred = inpf & ok
                for l in others:
                    isl = f(S[l])
                    if isl is None: pred &= False; continue
                    const = (ind[(C * isl + Dd) % p] - ind[(C * S[j] + Dd) % p]) % k   # derived: s_l - iota t = det (iota s_l - t)/((c iota s_l + d)(c t + d))
                    lhs2 = (ind[(isl - xs) % p] - ind[(S[l] - xs) % p]) % k
                    pred &= ((lhs2 - (prof[:, j] - prof[:, i]) - const) % k == 0) & ((isl - xs) % p != 0)
                m = inpf & ok
                tot['Bn'] += int(m.sum()); tot['Bbad'] += int((pred[m] != paired[m]).sum())
                # full partial-fixed keys: fixset on swapped coords x any value on the others
                fk = set()
                for t in np.flatnonzero(inpf): fk.add(int(key[t]))
                # all theoretical full keys: build from a representative profile vector
                allk = 0; unw_ne = 0
                for (xx, yy, zz) in fixset:
                    for rest in itertools.product(range(k), repeat=len(others)):
                        P = np.zeros(k, dtype=np.int64); P[j], P[u], P[v] = xx, yy, zz
                        for l, rv in zip(others, rest): P[l] = rv
                        P = (P - P[i]) % k; K = int(((P[1:] - P[0]) % k) @ (k ** np.arange(k - 1)))
                        allk += 1
                        if K not in fk:
                            tot['unw'] += 1; unw_ne += int(bc[K] > 0)
                tot['unw_nonempty'] += unw_ne
    return tot


print('A/B. Transport, -det identity, sigma-fixed partial keys by enumeration, and the kappa >= 5 pairing predicate')
for k, p, nS in ((4, 197, 40), (4, 401, 20), (5, 1451, 12), (5, 2521, 6), (6, 1933, 4), (7, 1009, 2)):
    t = run(k, p, nS, 100 + k)
    print('  k=%d p=%d: %d iota (%d split); -det identity failures %d; transport failures %d; fixed-key count != c*k: %d;'
          ' pairing predicate mismatches %d of %d points; unwitnessed partial-fixed full keys %d, of which nonempty %d' % (
              k, p, t['iota'], t['split'], t['detbad'], t['trbad'], t['fixbad'], t['Bbad'], t['Bn'], t['unw'], t['unw_nonempty']))
print('\nC. #{r: eta(r) = eta(1-r) = 1} against (p - 5)/4')
for p in (101, 197, 401, 1009, 2017):
    e = lambda v: pow(v % p, (p - 1) // 2, p) == 1
    n = sum(1 for r in range(2, p) if e(r) and e(1 - r))
    print('  p=%d: %d, (p-5)/4 = %d' % (p, n, (p - 5) // 4))
print('\nD. kappa = 4 explicit Weil factor, eps = 192/sqrt(p) (relative error of b_K), G(S)/((2/3)#split) in [(1-eps)^2/(1+eps)^4, (1+eps)^2/(1-eps)^4]')
for p in (4e4, 1e5, 1e6, 3e6, 1e7, 1e8):
    eps = 192 / math.sqrt(p)
    lo = (1 - eps) ** 2 / (1 + eps) ** 4 if eps < 1 else 0.0; hi = (1 + eps) ** 2 / (1 - eps) ** 4 if eps < 1 else float('inf')
    print('  p=%.0e: eps %.3f, factor in [%.3f, %.3f]' % (p, eps, lo, hi))
for target in (2.0, 1.1):
    p = 1e4
    while ((1 + 192 / math.sqrt(p)) ** 2 / (1 - 192 / math.sqrt(p)) ** 4 if 192 / math.sqrt(p) < 1 else 1e9) > target: p *= 1.01
    print('  upper factor <= %.1f from p ~ %.2e' % (target, p))
print('  kappa = 5 Weil range for m_K (main p/(2*5^5) = error 2*(2k-5)*sqrt(p)/2 ~ 5 sqrt p): p ~ %.1e' % ((5 * 2 * 5 ** 5) ** 2))
