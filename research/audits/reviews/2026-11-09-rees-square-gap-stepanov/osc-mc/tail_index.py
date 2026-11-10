"""Tail of B_L (and B_D) across primes at fixed kappa and lambda band: the quantity for obstruction (c) in its spread
form (topic note section 12.14).  For each band, X = B/median(B) over all primes of the band (not selected on symR).
  - Hill estimate gamma_k = mean_{i<=k} ln(X_(i)/X_(k+1)) over the top k (gamma = 1/alpha for a tail P(X>x) ~ x^-alpha),
    with a bootstrap over primes (2000 resamples) for its 2-sigma range;
  - the max ratio and gamma_max = ln(max X)/ln N.
Heuristic reading (referee round 4k-a): the sup over the N_T ~ T/(phi(kappa) ln T) primes near the threshold is about
median * N_T^gamma (power tail) or median * exp(sigma sqrt(2 ln N_T)) (lognormal). With log_kappa N_T = 3.42-5.53 at
kappa = 7-10, a power tail fills the whole B_L room (1/2 - 1/(2 ln kappa))kappa - O(1) at gamma_L ~ 0.5 and the whole
B_D room (1 - 1/ln kappa)kappa - O(1) at gamma_D ~ 1.0, up to the O(1)s (asymptotically gamma_L -> 1, gamma_D -> 2).
Primary quantity: sigma_L = sd(ln B_L) and rule T1' (predictions_k7_tail.txt, revision 1); Hill is reported only.
Usage: python tail_index.py k6     (the kappa = 6 survey, survey/*_s13.npz)
       python tail_index.py k7 <npz> ...   (kappa = 7 files, one band)"""
import sys, glob, math
import numpy as np
sys.path.insert(0, '.')
import k6_spike_survey as ks


def hill(x, k):
    x = np.sort(np.asarray(x))[::-1]
    return float(np.mean(np.log(x[:k] / x[k])))


def report(name, vals, k, what, rng):
    v = np.asarray([max(t, 1e-6) for t in vals]); med = float(np.median(v)); X = v / med; N = len(X)
    g = hill(X, k)
    bs = [hill(rng.choice(X, N, replace=True), k) for _ in range(2000)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    print('  %-14s %s: N %2d  median %.3f  max ratio %.2f  gamma_max %.2f  Hill(k=%d) %.2f (bootstrap 95%% %.2f-%.2f)  #X>2 %d' % (
        name, what, N, med, X.max(), math.log(X.max()) / math.log(N), k, g, lo, hi, int((X > 2).sum())))
    if what == 'B_L':                            # spread scale: sd of ln B_L (primary quantity, referee round 4k-a)
        lv = np.log(v); sd = float(lv.std(ddof=1))
        bsd = [float(rng.choice(lv, N, replace=True).std(ddof=1)) for _ in range(2000)]
        slo, shi = np.percentile(bsd, [2.5, 97.5])
        print('  %-14s sigma_L = sd(ln B_L) %.3f (bootstrap 95%% %.3f-%.3f)' % (name, sd, slo, shi))
        SIG[name] = (sd, lv)


rng = np.random.default_rng(1)
SIG = {}
if sys.argv[1] == 'k6':
    rows = []
    for f in sorted(glob.glob('survey/mc_k6_p*_s13.npz')):
        r = ks.analyse(f); rows.append(r)
    bands = [('[0.19, 0.25]', 0.19, 0.2501), ('(0.25, 0.31]', 0.2501, 0.31), ('[0.49, 0.56]', 0.49, 0.56)]
    for nm, a, b in bands:
        sel = [r for r in rows if a <= r['lam'] < b]
        k = max(4, len(sel) // 4)
        report(nm, [r['L'] for r in sel], k, 'B_L', rng)
        report(nm, [r['D'] for r in sel], k, 'B_D', rng)
else:
    rs = [ks.analyse(f) for f in sys.argv[2:]]
    k = max(2, len(rs) // 4)
    report('kappa=7 band', [r['L'] for r in rs], k, 'B_L', rng)
    report('kappa=7 band', [r['D'] for r in rs], k, 'B_D', rng)
    nres = sum(1 for r in rs if r['D_z'] >= 2)
    top = sorted(rs, key=lambda r: -r['D'])[:min(7, len(rs))]
    ntop = sum(1 for r in top if r['D_z'] >= 2)
    print('  B_D resolved (z >= 2) at %d of %d primes; top %d B_D values resolved: %d (gamma_D reported only if all)' % (
        nres, len(rs), len(top), ntop))
    # T1' (predictions_k7_tail.txt, revision 1): sigma_L(7) / sigma_L(6, lambda (0.25, 0.31]), bootstrap both sets
    l6 = np.log([max(ks.analyse(f)['L'], 1e-6) for f in sorted(glob.glob('survey/mc_k6_p*_s13.npz'))
                 if 0.2501 <= ks.analyse(f)['lam'] < 0.31])
    l7 = SIG['kappa=7 band'][1]; r0 = l7.std(ddof=1) / l6.std(ddof=1)
    rb = np.random.default_rng(1)
    rat = [rb.choice(l7, len(l7)).std(ddof=1) / rb.choice(l6, len(l6)).std(ddof=1) for _ in range(2000)]
    a, b = np.percentile(rat, [2.5, 97.5])
    call = 'WIDER' if a > 1 else ('NARROWER' if b < 1 else 'COMPATIBLE')
    print("  T1': sigma_L(7)/sigma_L(6) %.2f (bootstrap 95%% %.2f-%.2f; N7 %d, N6 %d) -> %s" % (r0, a, b, len(l7), len(l6), call))
    if len(sys.argv) > 2 and sys.argv[1] == 'k7':
        # extrapolated sup of B_L over N_T primes near T(7) (log_7 T = 5.57, phi(7) = 6), lognormal and power forms
        T = 7 ** 5.57; NT = T / (6 * math.log(T)); kk = 7
        sd, lv = SIG['kappa=7 band']; med = math.exp(float(np.median(lv)))
        g = hill(np.exp(lv) / med, k)
        ln_sup_logn = sd * math.sqrt(2 * math.log(NT)); ln_sup_pow = g * math.log(NT)
        print('  N_T %.0f (log_7 %.2f); median B_L %.3f; extrapolated log_7 sup: lognormal %.2f, power %.2f (L room 1.70 before O(1))' % (
            NT, math.log(NT, kk), med, math.log(med, kk) + ln_sup_logn / math.log(kk), math.log(med, kk) + ln_sup_pow / math.log(kk)))
        print('    parts: log_7 median %.2f (measured below lambda_T; same size as the O(1)); log_7(sup/median): lognormal %.2f, power %.2f' % (
            math.log(med, kk), ln_sup_logn / math.log(kk), ln_sup_pow / math.log(kk)))
