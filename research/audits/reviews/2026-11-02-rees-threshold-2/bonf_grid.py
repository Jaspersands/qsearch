"""Failed route (report §3.6): kappa * B_m(p) on a grid, B_m from bonferroni.py."""
import sys; sys.path.insert(0, '.')
import bonferroni as b, mpmath as mp
best = None
for K in [3, 5, 7, 9, 12, 16, 20, 30]:
    for m in [2, 4, 8, 16, 24]:
        for f in [1, 2, 4, 8]:
            p = mp.mpf(K) ** K * f * mp.log(K)
            v = K * b.B_exact(p, K, m)
            print(K, m, f, mp.nstr(v, 4))
            best = v if best is None or v < best else best
print("min kappa*B_m over grid:", mp.nstr(best, 4))
