"""Item 8 secondary (reported only, not scored): per-prime table, sigma_L of the 7 band primes vs the 17 drawn,
measurement-noise rms 1/(2 z_L) and the noise-corrected sigma_L. Usage: python tail_k7_24_secondary.py <7 band npz> -- <17 drawn npz>"""
import sys, math
import numpy as np
sys.path.insert(0, '.')
import k6_spike_survey as ks
i = sys.argv.index('--'); band, drawn = sys.argv[1:i], sys.argv[i + 1:]
rows = [(f, 'band', ks.analyse(f)) for f in band] + [(f, 'drawn', ks.analyse(f)) for f in drawn]
print('keys:', sorted(rows[0][2].keys()))
print('%-8s %-6s %7s %7s %6s %7s %6s' % ('p', 'set', 'lam', 'B_L', 'L_z', 'B_D', 'D_z'))
for f, s, r in rows:
    print('%-8s %-6s %7.4f %7.3f %6.2f %7.3f %6.2f' % (f.split('_p')[1].split('_')[0], s, r['lam'], r['L'], r.get('L_z', float('nan')), r['D'], r['D_z']))
rng = np.random.default_rng(1)
for nm in ('band', 'drawn', 'all'):
    lv = np.log([max(r['L'], 1e-6) for f, s, r in rows if nm == 'all' or s == nm])
    bs = [rng.choice(lv, len(lv)).std(ddof=1) for _ in range(2000)]
    print('%-5s N %2d  sigma_L %.3f (95%% %.3f-%.3f)  median B_L %.3f' % (nm, len(lv), lv.std(ddof=1), *np.percentile(bs, [2.5, 97.5]), math.exp(np.median(lv))))
z = np.array([r['L_z'] for f, s, r in rows]); noise = 1 / (2 * z)
lv = np.log([max(r['L'], 1e-6) for f, s, r in rows]); sd = lv.std(ddof=1)
rms = math.sqrt(np.mean(noise ** 2))
print('noise 1/(2 z_L): range %.3f-%.3f, rms %.3f; corrected sigma_L %.3f; corrected ratio %.2f (k6 corrected 0.359->0.352 base: %.2f)' % (
    noise.min(), noise.max(), rms, math.sqrt(sd ** 2 - rms ** 2), math.sqrt(sd ** 2 - rms ** 2) / math.sqrt(0.352 ** 2 - 0.025 ** 2), sd / 0.352))
print('lam range %.4f-%.4f' % (min(r['lam'] for f, s, r in rows), max(r['lam'] for f, s, r in rows)))
