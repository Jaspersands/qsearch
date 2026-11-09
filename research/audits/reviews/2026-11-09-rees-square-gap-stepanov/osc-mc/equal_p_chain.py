"""How the OSC'(B) constants grow with kappa: noise-subtracted bin statistics for kappa = 4..7.
For each (kappa, p) with data, the two numbers that enter the threshold T (osc_prime_T.py) by
Cauchy-Schwarz, sum_group w|V| <= sqrt(W_group * sum_group w|V|^2):
  B_L = weighted rms |V| over the (L') group (one-sided non-pair classes and two-sided m <= 6), absolute;
  B_D = weighted rms |V| over the (D) group (two-sided m >= 7), in units of k^2/p;
both after removing the finite-ensemble noise sum w sigma_RC^2 / N_unl in quadrature.  Also the
common (D) bins (3,4), (4,4) and the full-support bin (k,k), per bin, in units of k^2/p.
Sources:
  kappa = 4, 5 exact class values (../osc-bdry/class_values_k4_wide.npz, class_values_k5.npz), with
    sigma_RC^2 measured in mc_k4_p197_s3.npz / mc_k5_p401_s2.npz (per-configuration variance, which
    batching does not affect) and scaled by n/n0 (noise law Var Q = c n /(orb_R orb_C));
    se from the chi-square spread of the subtracted noise (conjugate classes counted once).
  kappa = 6, 7 S-batched Monte Carlo files: unbiased weighted split-batch sums, noise from the file,
    jackknife se over batches.  Printed as estimate (z) and 2-sigma upper end.
A p-law with a constant B_D gives the same B_D at every p and kappa; a lambda-law (values a function
of the bucket occupancy lambda = p/k^(k-1)) gives equal absolute values at equal lambda; a p-law with
C(kappa) ~ kappa! gives B_D growing by a factor ~kappa per step at equal p.
Usage: python equal_p_chain.py"""
import sys, math, numpy as np
sys.path.insert(0, '.')
from mc_classes import tables


def groups(k, supp):
    ms = np.add.outer(supp, supp)
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    g = {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}
    for a in range(2, k + 1):
        for b in range(a, k + 1):
            g['(%d,%d)' % (a, b)] = ((supp[:, None] == a) & (supp[None, :] == b)) | ((supp[:, None] == b) & (supp[None, :] == a))
    return g


def exact_rows(k, exfile, mcfile, p0, pmin):
    cl, R, P, orb, rb, supp, canon, base, reps = tables(k)
    name = lambda c: ''.join(str(x) for x in c if x) or '0'
    names = [name(c) for c in cl]
    ex = np.load(exfile)
    perm = [[name(tuple(c)) for c in ex['ms']].index(x) for x in names]
    mc = np.load(mcfile); N = mc['cnt'].sum(); Vh = mc['S1'].sum(0) / N
    sig2 = np.maximum(mc['S2'] / N - np.abs(Vh) ** 2, 0); n0 = p0 + 1 - 2 * k
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    G = groups(k, supp); out = []
    for a, p in enumerate(int(x) for x in ex['ps']):
        if p < pmin: continue
        V = ex['V'][a][np.ix_(perm, perm)]; n = p + 1 - 2 * k
        Nunl = float(ex['N1'][a]) / (math.factorial(k) ** 2 * n)
        nz2 = sig2 * n / n0 / Nunl; row = {}
        for g, m in G.items():
            Wg = w2[m].sum(); s = (w2[m] * (np.abs(V[m]) ** 2 - nz2[m])).sum()
            se = math.sqrt(((w2[m] * nz2[m]) ** 2).sum() + 2 * ((w2[m] ** 2) * np.abs(V[m]) ** 2 * nz2[m]).sum())
            row[g] = (s, se, Wg)
        out.append((k, p, 'exact', row))
    return out


def mc_row(f):
    d = np.load(f); k, p = int(d['k']), int(d['p']); S1, cnt, S2 = d['S1'], d['cnt'], d['S2']; B = len(cnt)
    assert cnt.max() - cnt.min() > 1, 'pre-fix file'
    Vb = S1 / cnt[:, None, None]; N = cnt.sum(); Vh = S1.sum(0) / N
    nz2 = np.maximum(S2 / N - np.abs(Vh) ** 2, 0) / float(d['Nunl'])
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]

    def X(idx, m):
        V = Vb[idx][:, m]; b = len(idx)
        return (w2[m] * (np.abs(V.sum(0)) ** 2 - (np.abs(V) ** 2).sum(0))).sum() / (b * (b - 1))
    row = {}
    for g, m in groups(k, supp).items():
        full = X(np.arange(B), m); jk = np.array([X(np.delete(np.arange(B), t), m) for t in range(B)])
        se = math.sqrt((B - 1) / B * ((jk - jk.mean()) ** 2).sum())
        row[g] = (full - (w2[m] * nz2[m]).sum(), se, w2[m].sum())
    return (k, p, 'MC', row)


def fmt(s, se, Wg, unit):
    est = math.sqrt(max(s, 0) / Wg) / unit; lim = math.sqrt((max(s, 0) + 2 * se) / Wg) / unit
    return '%7.3f (z%5.1f) <%7.3f' % (est, s / se if se > 0 else 0, lim)


rows = exact_rows(4, '../osc-bdry/class_values_k4_wide.npz', 'mc_k4_p197_s3.npz', 197, 197)
rows += exact_rows(5, '../osc-bdry/class_values_k5.npz', 'mc_k5_p401_s2.npz', 401, 181)
for f in sys.argv[1:] or ['mc_k6_p1933_s11.npz', 'mc_k6_p2347_s11.npz', 'mc_k6_p3571_s11.npz', 'mc_k6_p3877_sb.npz',
                          'mc_k6_p4219_s11.npz', 'mc_k6_p11677_sb.npz', 'mc_k7_p58787_sb.npz', 'mc_k7_p47041_s12.npz']:
    try:
        rows.append(mc_row(f))
    except (FileNotFoundError, AssertionError) as e:
        print('skip', f, type(e).__name__)
print('  k      p    lam   src  |  B_L (abs) est (z) <2sig       |  B_D [k^2/p] est (z) <2sig  |  (3,4) [k^2/p]              |  (4,4) [k^2/p]              |  (k,k) [k^2/p]')
for k, p, src, row in rows:
    kp = k * k / p
    cols = [fmt(*row['L'], 1.0), fmt(*row['D'], kp)]
    for g in ['(3,4)', '(4,4)', '(%d,%d)' % (k, k)]:
        cols.append(fmt(*row[g], kp) if g in row else ' ' * 26)
    print('  %d %6d %6.2f %5s  | %s | %s | %s | %s | %s' % (k, p, p / k ** (k - 1), src, *cols))

# ---- summaries: equal p, equal lambda, and per-kappa ranges above the noise crossing ----
R = {(k, p): row for k, p, src, row in rows}
rms = lambda t: math.sqrt(max(t[0], 0) / t[2])
up = lambda t: math.sqrt((max(t[0], 0) + 2 * t[1]) / t[2])
print()
print('Equal p (absolute w-rms; ratio = higher kappa / lower kappa; "<" = 2-sigma upper end of the MC side)')
pairs = [((4, q), (5, q)) for q in (401, 421, 461, 521, 541)] + [((5, 2311), (6, 2347)), ((5, 2111), (6, 2347)), ((5, 1801), (6, 1933))]
for (k1, p1), (k2, p2) in pairs:
    if (k1, p1) not in R or (k2, p2) not in R: continue
    a, b = R[(k1, p1)], R[(k2, p2)]; out = []
    for g in ['L', 'D', '(3,4)', '(4,4)']:
        out.append('%s %.4f vs %.4f (<%.4f): %.2f' % (g, rms(a[g]), rms(b[g]), up(b[g]), rms(b[g]) / rms(a[g]) if rms(a[g]) > 0 else float('nan')))
    kp1, kp2 = k1 * k1 / p1, k2 * k2 / p2
    out.append('B_D ratio %.2f (<%.2f)' % ((rms(b['D']) / kp2) / (rms(a['D']) / kp1), (up(b['D']) / kp2) / (rms(a['D']) / kp1)))
    print('  k=%d p=%d vs k=%d p=%d:  ' % (k1, p1, k2, p2) + ';  '.join(out))
print('Equal lambda = 0.50 (absolute w-rms, noise-subtracted; ratio to kappa = 5 at p = 311; constant-B p-law predicts (k^2/p)/(25/311))')
base = R.get((5, 311))
for k, p in [(6, 3877), (7, 58787), (7, 47041)]:
    if (k, p) not in R or base is None: continue
    b = R[(k, p)]; out = []
    for g in ['D', '(2,5)', '(3,4)', '(3,5)', '(4,4)', '(4,5)', '(5,5)']:
        if g in b and g in base:
            out.append('%s %.5f<%.5f / %.4f = %.3f (<%.3f)' % (g, rms(b[g]), up(b[g]), rms(base[g]), rms(b[g]) / rms(base[g]) if rms(base[g]) > 0 else float('nan'),
                                                          up(b[g]) / rms(base[g]) if rms(base[g]) > 0 else float('nan')))
    print('  k=%d p=%d (lam %.2f; p-law prediction %.3f):' % (k, p, p / k ** (k - 1), (k * k / p) / (25 / 311)))
    for i in range(0, len(out), 3): print('     ' + ';  '.join(out[i:i + 3]))
print('Per kappa above the noise crossing (k=4: p >= 197, k=5: p >= 431, k=6, 7: S-batched MC): median and max of B_L, B_D')
for k, pmin in [(4, 197), (5, 431), (6, 0), (7, 0)]:
    sel = [(p, row) for kk, p, src, row in rows if kk == k and p >= pmin]
    if not sel: continue
    bl = [rms(r['L']) for p, r in sel]; bd = [rms(r['D']) / (k * k / p) for p, r in sel]
    print('  k=%d (%d primes): B_L median %.3f max %.3f (p=%d);  B_D median %.3f max %.3f (p=%d)' % (
        k, len(sel), float(np.median(bl)), max(bl), sel[int(np.argmax(bl))][0], float(np.median(bd)), max(bd), sel[int(np.argmax(bd))][0]))
