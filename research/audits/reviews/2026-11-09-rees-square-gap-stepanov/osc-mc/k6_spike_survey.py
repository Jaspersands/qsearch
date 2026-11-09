"""kappa = 6 spike survey (MECHANICAL_FOLLOW_UP_PLAN.md "2026-11-09 Rees Square Gap: OSC' Follow-Up", item 1).
Question: does OSC' hold at lambda <= 0.25 at spike primes, and how do spikes scale with lambda?
Per prime (S-batched mc_classes.py files; default survey/mc_k6_p*_s13.npz plus the earlier S-batched files):
  lambda = p / 6^5, configurations, N1/mu1 with its batch se (configurations cluster by S, batches are by S);
  PW_pair: split-batch debiased value, its null floor (the value if every non-pair class were 0) and the
    Cauchy-Schwarz upper estimate, as in pw_bin_cs.py;
  B_L (absolute) and B_D (units k^2/p): noise-subtracted weighted rms of V over the L group (one-sided non-pair
    classes, two-sided m <= 6) and the D group (two-sided m >= 7), jackknife z, 2-sigma ends; the same
    estimator as equal_p_chain.mc_row; nu_D = the subtracted noise rms of the D group, units k^2/p;
  noise-law c: median over two-sided pairs of the per-configuration variance times orb_R orb_C / n;
  cluster-corrected constants B_L^cl, B_D^cl: configurations sharing S are correlated (a bucket of size b gives
    C(b, k) of them), so the intrinsic fluctuation of V is not sigma^2/N_unl but se_b^2 nconf/N_unl (se_b = the
    S-batch standard error, which contains the clustering; the prime's configurations are modelled as a sample
    of its S-clusters); 'infl' = median over two-sided pairs of that ratio.  OSC' as stated uses sigma^2/N_unl,
    so B_L, B_D are the OSC' constants; B^cl separates structure from cluster noise;
  order-6 cyclotomic statistics max|D|/sqrt p and K (cyclo_spike.stats);
  6th-power residue symbols ind(a) mod 6 of a = -1, 2, 3, -3;
  involution-symmetric rate (sym_rate.py, read from survey/sym_rate_k6.out when present): the configurations per
    involution-symmetric S relative to Poisson ('symR') and their share C_sym of N1/mu1; 'N1/C' = N1/mu1 / C_sym.
Per lambda band: medians, maxima, spike flags (B_D: 2-sigma lower end above twice the band median of the
estimates; PW: debiased PW_pair above twice the band median), and Spearman rank correlations.
Monte Carlo values are sampling estimates, not certificates; the noise subtraction uses the measured
per-configuration variance divided by N_unl.
Usage: python k6_spike_survey.py [files...]"""
import sys, glob, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot


def groups(k, supp):
    ms = np.add.outer(supp, supp)
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    return {'L': (two & (ms <= 6)) | one, 'D': two & (ms >= 7)}


def null_const(B, reps=200000, seed=0):
    rng = np.random.default_rng(seed)
    V = (rng.standard_normal((reps, B)) + 1j * rng.standard_normal((reps, B))) / math.sqrt(2)
    sq = (np.abs(V.sum(1)) ** 2 - (np.abs(V) ** 2).sum(1)) / (B * (B - 1))
    return np.sqrt(np.maximum(sq, 0)).mean() / math.sqrt(1 / B)


def cyclo_stats(p, k):
    g = primroot(p); ind = np.zeros(p, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    xs = np.arange(1, p - 1)
    A = np.bincount((ind[xs] % k) * k + ind[xs + 1] % k, minlength=k * k).astype(float)
    D = A - A.mean()
    sym = [int(ind[a % p] % k) for a in (-1, 2, 3, -3)]
    return np.abs(D).max() / math.sqrt(p), k * k * (D ** 4).sum() / ((D ** 2).sum() ** 2), sym


CB = {}
SYM = {}
try:
    for line in open('survey/sym_rate_k6.out'):
        w = line.split()
        if w and w[0].isdigit():
            SYM[int(w[0])] = {'symR': float(w[3]), 'fixed': float(w[4]), 'f': float(w[5]), 'Csym': float(w[6])}
except FileNotFoundError:
    pass


def analyse(f):
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    S1, cnt, S2 = d['S1'], d['cnt'], d['S2']; B = len(cnt); N = cnt.sum()
    if cnt.max() - cnt.min() <= 1:
        raise AssertionError('pre-fix file (round-robin batches)')
    Vb = S1 / cnt[:, None, None]; Vh = S1.sum(0) / N
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    n = p + 1 - 2 * k; kf = math.factorial(k); kp2 = k * k / p
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    sig2 = np.maximum(S2 / N - np.abs(Vh) ** 2, 0)
    nz2 = sig2 / float(d['Nunl'])
    seb = np.sqrt((np.abs(Vb - Vb.mean(0)) ** 2).sum(0) / (B * (B - 1)))
    nzc2 = seb ** 2 * N / float(d['Nunl'])

    def X(idx, m):
        V = Vb[idx][:, m]; b = len(idx)
        return (w2[m] * (np.abs(V.sum(0)) ** 2 - (np.abs(V) ** 2).sum(0))).sum() / (b * (b - 1))
    r = {'k': k, 'p': p, 'lam': p / k ** (k - 1), 'nconf': int(N), 'nS': int(d['nS']), 'file': f}
    for g, m in groups(k, supp).items():
        full = X(np.arange(B), m); jk = np.array([X(np.delete(np.arange(B), t), m) for t in range(B)])
        se = math.sqrt((B - 1) / B * ((jk - jk.mean()) ** 2).sum()); noise = (w2[m] * nz2[m]).sum(); Wg = w2[m].sum()
        unit = 1.0 if g == 'L' else kp2
        s = full - noise
        r[g] = math.sqrt(max(s, 0) / Wg) / unit
        r[g + '_z'] = s / se if se > 0 else 0.0
        r[g + '_hi'] = math.sqrt(max(s + 2 * se, 0) / Wg) / unit
        r[g + '_lo'] = math.sqrt(max(s - 2 * se, 0) / Wg) / unit
        r[g + '_nu'] = math.sqrt(noise / Wg) / unit
        noise_cl = (w2[m] * nzc2[m]).sum()
        r[g + '_cl'] = math.sqrt(max(full - noise_cl, 0) / Wg) / unit
        r[g + '_cl_z'] = (full - noise_cl) / se if se > 0 else 0.0
        r[g + '_nucl'] = math.sqrt(noise_cl / Wg) / unit
    # PW_pair: debiased, null floor, Cauchy-Schwarz upper estimate
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1))
    Vdb = np.sqrt(np.maximum(sq, 0))
    if B not in CB: CB[B] = null_const(B)
    cB = CB[B]
    z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
    S_pair = (orb[pair] * (P[pair, rb] * kf)).sum().real
    den = 1 - 2 * k * S_pair / (n * kf)
    pm = np.zeros_like(w2, dtype=bool); pm[pair, z0] = True; pm[z0, pair] = True
    pairterm = (w2[pm] * np.abs(Vh[pm] + k)).sum()
    nzm = np.ones_like(pm); nzm[z0, z0] = False; nzm[pm] = False
    r['PW'] = (pairterm + (w2[nzm] * Vdb[nzm]).sum()) / n / den
    r['PW_floor'] = (pairterm + (w2[nzm] * cB * seb[nzm]).sum()) / n / den
    cs = pairterm
    for a in sorted(set(supp)):
        for b in sorted(set(supp)):
            if b < a or (a == 0 and b == 0) or (a == 0 and b == 2): continue
            m = ((supp[:, None] == a) & (supp[None, :] == b)) | ((supp[:, None] == b) & (supp[None, :] == a))
            if m.any(): cs += math.sqrt(w2[m].sum() * max(X(np.arange(B), m), 0.0))
    r['PW_cs'] = cs / n / den
    # configuration excess and its batch se
    rate = cnt / (int(d['nS']) / B)
    r['N1mu1'] = float(d['N1']) / float(d['mu1'])
    r['N1mu1_se'] = r['N1mu1'] * rate.std(ddof=1) / math.sqrt(B) / rate.mean()
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2)
    r['c'] = float(np.median((sig2 * np.outer(orb, orb) / n)[two]))
    r['infl'] = float(np.median((nzc2 / np.maximum(nz2, 1e-300))[two & (nz2 > 0)]))
    r['maxD'], r['K'], r['sym'] = cyclo_stats(p, k)
    sy = SYM.get(p, {}) if k == 6 else {}
    r['symR'] = sy.get('symR', float('nan')); r['Csym'] = sy.get('Csym', float('nan'))
    r['N1C'] = r['N1mu1'] / r['Csym'] if r['Csym'] == r['Csym'] and r['Csym'] > 0 else float('nan')
    return r


def spearman(x, y):
    rk = lambda v: np.argsort(np.argsort(v))
    return float(np.corrcoef(rk(np.asarray(x)), rk(np.asarray(y)))[0, 1]) if len(x) > 2 else float('nan')


if __name__ == '__main__':
    files = sys.argv[1:] or sorted(glob.glob('survey/mc_k6_p*_s13.npz'))
    ref = ['mc_k6_p1933_s11.npz', 'mc_k6_p2347_s11.npz', 'mc_k6_p3571_s11.npz', 'mc_k6_p3877_sb.npz', 'mc_k6_p4219_s11.npz']
    rows, refrows = [], []
    for f in files + (ref if not sys.argv[1:] else []):
        try:
            (refrows if f in ref else rows).append(analyse(f))
        except (FileNotFoundError, AssertionError) as e:
            print('skip', f, e)
    rows.sort(key=lambda r: r['p'])
    hdr = ('     p   lam  conf    N1/mu1 (se)    PW_pair db [floor] CS  |  B_L est (z) <2sig      |  B_D [k^2/p] est (z) <2sig  nu_D'
           '  |   c   infl  B_L^cl (z)   B_D^cl (z)  |  max|D|/rp   K   ind(-1,2,3,-3) mod 6 | symR  C_sym  N1/C')
    fmt = lambda r: ('%6d %5.3f %5d  %6.2f (%.2f)  %6.2f [%5.2f] %5.2f  | %6.3f (%5.1f) <%6.3f  | %6.2f (%5.1f) <%6.2f  %5.2f  | %5.2f %5.2f  %5.3f (%5.1f) %5.2f (%5.1f) |  %5.2f  %5.2f  %s | %6.1f %6.3f %5.1f' % (
        r['p'], r['lam'], r['nconf'], r['N1mu1'], r['N1mu1_se'], r['PW'], r['PW_floor'], r['PW_cs'], r['L'], r['L_z'], r['L_hi'],
        r['D'], r['D_z'], r['D_hi'], r['D_nu'], r['c'], r['infl'], r['L_cl'], r['L_cl_z'], r['D_cl'], r['D_cl_z'],
        r['maxD'], r['K'], ','.join(str(s) for s in r['sym']), r['symR'], r['Csym'], r['N1C']))
    print('kappa = 6 spike survey: S-batched Monte Carlo, seed 13 (survey/), every p = 1 mod 6 in [1500, 2400] and [3800, 4300]')
    print(hdr)
    for r in rows: print(fmt(r))
    if refrows:
        print('Earlier S-batched files at other seeds (replication check; same estimators):')
        for r in sorted(refrows, key=lambda r: r['p']): print(fmt(r) + '   ' + r['file'])
    bands = [('lam [0.19, 0.22)', 0.19, 0.22), ('lam [0.22, 0.25]', 0.22, 0.2501), ('lam (0.25, 0.31]', 0.2501, 0.31), ('lam [0.49, 0.56]', 0.49, 0.56)]
    print()
    print('Per band: medians and maxima; spikes = 2-sigma lower end of B_D above twice the band median of B_D (sD),')
    print('or debiased PW_pair above twice the band median (sPW), or N1/mu1 above twice the band median (sN)')
    for name, lo, hi in bands:
        b = [r for r in rows if lo <= r['lam'] < hi]
        if not b: continue
        med = {q: float(np.median([r[q] for r in b])) for q in ('L', 'D', 'PW', 'N1mu1', 'D_nu', 'c', 'L_cl', 'D_cl', 'infl')}
        mx = {q: max(b, key=lambda r: r[q]) for q in ('L', 'D', 'D_hi', 'PW', 'N1mu1')}
        print('  %s: %d primes; median B_L %.3f, B_D %.2f (noise nu_D %.2f), PW_pair %.2f, N1/mu1 %.2f, c %.2f; cluster inflation %.2f, B_L^cl %.3f, B_D^cl %.2f' % (
            name, len(b), med['L'], med['D'], med['D_nu'], med['PW'], med['N1mu1'], med['c'], med['infl'], med['L_cl'], med['D_cl']))
        print('      max B_L %.3f (p=%d)  max B_D %.2f (p=%d)  max 2-sigma upper B_D %.2f (p=%d)  max PW_pair %.2f (p=%d)  max N1/mu1 %.2f (p=%d)' % (
            mx['L']['L'], mx['L']['p'], mx['D']['D'], mx['D']['p'], mx['D_hi']['D_hi'], mx['D_hi']['p'], mx['PW']['PW'], mx['PW']['p'],
            mx['N1mu1']['N1mu1'], mx['N1mu1']['p']))
        sp = []
        for r in b:
            fl = ('sD' if r['D_lo'] > 2 * med['D'] else '') + ('sPW' if r['PW'] > 2 * med['PW'] else '') + ('sN' if r['N1mu1'] > 2 * med['N1mu1'] else '')
            if fl: sp.append('%d[%s: B_L %.2f B_D %.2f (lo %.2f) PW %.2f N1/mu1 %.2f]' % (r['p'], fl, r['L'], r['D'], r['D_lo'], r['PW'], r['N1mu1']))
        print('      spikes (%d of %d): %s' % (len(sp), len(b), '; '.join(sp) if sp else 'none'))
    print()
    print('Spearman rank correlations (all survey primes, then lambda <= 0.25, then lambda in (0.25, 0.31], then [0.49, 0.56])')
    for name, sel in [('all', rows), ('lam<=0.25', [r for r in rows if r['lam'] <= 0.2501]),
                      ('0.25<lam<=0.31', [r for r in rows if 0.2501 < r['lam'] <= 0.31]), ('lam~0.5', [r for r in rows if r['lam'] > 0.45])]:
        if len(sel) < 4: continue
        col = lambda q: [r[q] for r in sel]
        print('  %-15s n=%2d  B_D vs N1/mu1 %.2f, vs PW_pair %.2f, vs K %.2f, vs max|D|/rp %.2f, vs c %.2f;  B_L vs N1/mu1 %.2f;  N1/mu1 vs K %.2f' % (
            name, len(sel), spearman(col('D'), col('N1mu1')), spearman(col('D'), col('PW')), spearman(col('D'), col('K')),
            spearman(col('D'), col('maxD')), spearman(col('D'), col('c')), spearman(col('L'), col('N1mu1')), spearman(col('N1mu1'), col('K'))))
        hs = [r for r in sel if r['symR'] == r['symR']]
        if len(hs) >= 4:
            c2 = lambda q: [r[q] for r in hs]
            print('  %-15s n=%2d  symR vs N1/mu1 %.2f, vs B_D %.2f, vs B_L %.2f, vs PW_pair %.2f;  N1/mu1 / C_sym: median %.2f, quartiles %.2f-%.2f' % (
                '', len(hs), spearman(c2('symR'), c2('N1mu1')), spearman(c2('symR'), c2('D')), spearman(c2('symR'), c2('L')),
                spearman(c2('symR'), c2('PW')), np.median(c2('N1C')), np.percentile(c2('N1C'), 25), np.percentile(c2('N1C'), 75)))
    print()
    print('Residue classes: median N1/mu1 and B_D at lambda <= 0.31 by ind(-3) mod 6 and by ind(-1) mod 6')
    low = [r for r in rows if r['lam'] <= 0.31]
    for j, nm in [(3, 'ind(-3)'), (0, 'ind(-1)')]:
        for v in sorted({r['sym'][j] for r in low}):
            s = [r for r in low if r['sym'][j] == v]
            print('  %s = %d: %2d primes, median N1/mu1 %.2f, median B_D %.2f, max B_D %.2f' % (
                nm, v, len(s), np.median([r['N1mu1'] for r in s]), np.median([r['D'] for r in s]), max(r['D'] for r in s)))
