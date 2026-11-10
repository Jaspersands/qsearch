"""Referee round 4g (10 Nov): checks for the draft sec12_12_draft.md (G = s/R22).
1. G at kappa = 6 (split shares from the npz counts) and kappa = 7, with the trivial caps 1/R22.
2. N_inv^2 kappa^2 and 1/R22 at the section 11.8 thresholds.
3. Section 12.5 item 6's F*v illustrations re-expressed with G*v = F*v/(N1/mu1).
4. kappa = 4: every Moebius involution swapping two disjoint pairs of S maps S-buckets (mc_classes keys) to S-buckets.
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4g_checks.py > r4g_checks.out"""
import os, math
import numpy as np
from math import comb
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
os.chdir(OSC)
OLD = {1597, 1621, 1657, 1789}
PR = [1531, 1543, 1549, 1567, 1579, 1597, 1609, 1621, 1627, 1657, 1663, 1669, 1693, 1699, 1723, 1741, 1747, 1753,
      1759, 1777, 1783, 1789, 1801, 1831, 1861, 1867, 1873, 1879, 1933]
Ninv = lambda k: comb(k, 2) * comb(k - 2, 2) // 2
print('1. G = s / R22')
G6, cap6, N6 = {}, {}, {}
for p in PR:
    pre = 'split/split_k6_p%d' % p if p in OLD else 'split/split13_k6_p%d' % p
    A, S = np.load(pre + '_all.npz'), np.load(pre + '_str.npz')
    s = S['cnt'].sum() / A['cnt'].sum(); R = Ninv(6) ** 2 * 6 ** 4 / p ** 2
    G6[p], cap6[p], N6[p] = s / R, 1 / R, float(A['N1']) / float(A['mu1'])
g = np.array(list(G6.values())); c = np.array(list(cap6.values()))
print('  kappa = 6 (29): N_inv %d, R22 numerator %d; G %.3f-%.3f (median %.3f, max at %d); caps 1/R22 %.3f-%.3f; G/cap %.3f-%.3f; R22 %.3f-%.3f' % (
    Ninv(6), Ninv(6) ** 2 * 6 ** 4, g.min(), g.max(), np.median(g), max(G6, key=G6.get), c.min(), c.max(), (g / c).min(), (g / c).max(), 1 / c.max(), 1 / c.min()))
print('  kappa = 6 spikes: ' + ', '.join('%d G %.2f (F %.2f, N1/mu1 %.2f)' % (p, G6[p], G6[p] * N6[p], N6[p]) for p in (1789, 1657, 1597, 1933, 1531, 1741)))
k7 = [(35281, 0.043, 'pairsym, 19'), (35099, 0.011, 'pairsym, 5'), (36037, 185 / 6000, 'split, 185'), (34693, 0.021, 'pairsym, 9'), (23549, 5 / 79, 'pairsym, 5')]
for p, s, src in k7:
    R = Ninv(7) ** 2 * 7 ** 4 / p ** 2
    print('  kappa = 7 %d: share %.4f (%s) R22 %.4f G %.3f cap %.1f' % (p, s, src, R, s / R, 1 / R))
print('\n2. N_inv^2 kappa^2 and the trivial cap at the thresholds')
for k, lT in ((4, 4.50), (5, 4.91), (6, 5.14), (7, 5.57), (8, 6.18), (9, 6.78), (10, 7.36)):
    n = Ninv(k); x = n * n * k * k
    print('  kappa %2d: N_inv %4d (< k^4/8 = %.0f: %s), log_k N_inv^2 k^2 = %.2f; at log_k T = %.2f: log_k(1/R22) = %.2f, '
          'B_L addition bound G * k^%.2f' % (k, n, k ** 4 / 8, n < k ** 4 / 8, math.log(x, k), lT, 2 * lT - math.log(n * n * k ** 4, k), math.log(n * n * k ** 4, k) - lT))
print('\n3. Section 12.5 item 6 illustrations: F*v (note) and G*v = F*v / (N1/mu1)')
Fv = {1621: 0.003, 1933: 0.27, 1597: 0.35, 1657: 0.98, 1789: 1.53}
for p, fv in Fv.items():
    print('  %d: F*v %.3f, N1/mu1 %.2f -> G*v %.3f' % (p, fv, N6[p], fv / N6[p]))
r = Fv[1789] / N6[1789] / Fv[1789]
print('  so the 1789-based additions at T(7..10) (16, 11, 6, 3) scale by %.3f: %s; w*17.3 (0.78, 0.09) -> %.2f, %.3f; L 0.09 -> %.3f' % (
    r, ', '.join('%.1f' % (x * r) for x in (16, 11, 6, 3)), 0.78 * r, 0.09 * r, 0.09 * r))
print('\n4. kappa = 4 bucket check')
rng = np.random.default_rng(7)
def ind_table(p):
    for gg in range(2, p):
        if all(pow(gg, (p - 1) // q, p) != 1 for q in {q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, int(q ** .5) + 1))}):
            break
    ind = np.zeros(p, dtype=np.int64); x = 1
    for e in range(p - 1): ind[x] = e; x = x * gg % p
    return ind
tot = bad = invb = 0
for p in (197, 389, 1009, 2017):
    k = 4; ind = ind_table(p); chi = ind % k; chi[0] = -1; xs = np.arange(p); kp = k ** np.arange(k - 1)
    for _ in range(25):
        S = rng.choice(p, 4, replace=False)
        D = (S[None, :] - xs[:, None]) % p; prof = chi[D]; inS = (D == 0).any(1)
        key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
        for (a, b), (c_, d) in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
            a, b, c_, d = int(S[a]), int(S[b]), int(S[c_]), int(S[d])
            gam = (a + b - c_ - d) % p; al = (a * b - c_ * d) % p; be = (gam * a * b - al * (a + b)) % p
            assert (-al * al - be * gam) % p
            def iota(z):
                den = (gam * z - al) % p
                return None if den == 0 else (al * z + be) * pow(den, p - 2, p) % p
            assert iota(a) == b and iota(b) == a and iota(c_) == d and iota(d) == c_
            mp = {}; ok = True; n_exc = 0
            for x in range(p):
                if inS[x]: continue
                y = iota(x)
                if y is None: n_exc += 1; continue
                kx, ky = int(key[x]), int(key[y])
                if mp.setdefault(kx, ky) != ky: ok = False
            vals = list(mp.values())
            ok = ok and len(set(vals)) == len(vals)
            tot += 1; bad += not ok; invb += sum(1 for kx, ky in mp.items() if kx == ky)
print('  %d (S, pairing) cases at p = 197, 389, 1009, 2017: key map x -> iota(x) single-valued and injective in all but %d '
      '(one point, the pole alpha/gamma, maps to infinity); invariant buckets per case %.2f on average' % (tot, bad, invb / tot))
