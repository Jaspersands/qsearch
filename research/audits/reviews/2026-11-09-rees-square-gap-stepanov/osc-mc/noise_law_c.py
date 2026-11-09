"""Noise-law constant c in Var Q(R,C) = c n /(orb_R orb_C) (section 11.4), per Monte Carlo file:
the per-configuration variance S2/N - |V_hat|^2 times orb_R orb_C / n, over two-sided class pairs.
Prints the median and the 5% / 95% quantiles.  Batching does not affect it.
Usage: python noise_law_c.py file.npz [...]"""
import sys, numpy as np
for f in sys.argv[1:]:
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    S1, cnt, S2 = d['S1'], d['cnt'], d['S2']; N = cnt.sum()
    Vh = S1.sum(0) / N; orb = d['orb']; supp = d['supp']; n = p + 1 - 2 * k
    c = (S2 / N - np.abs(Vh) ** 2) * np.outer(orb, orb) / n
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2)
    print('%s k=%d p=%d lam=%.3f conf=%d: noise-law c over two-sided pairs: median %.3f, 5%% %.3f, 95%% %.3f' % (
        f, k, p, p / k ** (k - 1), int(N), np.median(c[two]), np.quantile(c[two], .05), np.quantile(c[two], .95)))
