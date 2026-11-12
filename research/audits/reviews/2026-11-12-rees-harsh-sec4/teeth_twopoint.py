"""Teeth for prop:descent's hypothesis that the dilations preserve H: the two-point pullback
P_2 = E_1^{-1}(h) cap E_2^{-1}(h) on the class-3 filiform cover (h = F_p(x+z+u)) is not dilation-
invariant (it contains xi_u = 2tu - 3t^2u + t^3u).  A correct conversion would output rho of the image
of P_2 in G_2; the merge with dilations instead kills the xi_u direction.  Pairs q = r * (a * image of xi_u)."""
import numpy as np, itertools
from lie import filiform4, Cover, all_elements, encode, in_span, rref
from sim_filiform import coset_ids, Source, solutions, graded_basis
rng = np.random.default_rng(5)
p = 5
L, wt = filiform4(p)
C3, C2 = Cover(L, wt), Cover(L, wt, d=2)
Lel = all_elements(L.n, p); X3 = all_elements(C3.n, p)
hB = L.span_closure_sub([[1, 0, 1, 1]])
f, _ = coset_ids(L, hB, Lel)
fhat = np.zeros(len(X3), dtype=np.int64)
for s in (1, 2):
    fhat = fhat * (p ** L.n) + f[encode(C3.E(s, X3), p)]
src = Source(C3, fhat)
lams_all, prob = src.label_law()
good = np.nonzero(prob > 1e-9)[0]
print("labels uniform on all of F_p (K=0):", np.allclose(prob, 1 / p))
xi_img = np.zeros(C2.n, np.int64)
xi_img[C2.basis.index((1, 3))] = 2; xi_img[C2.basis.index((2, 3))] = (-3) % p
tested = failed = 0
for trial in range(4):
    li = rng.choice(good, size=3); lams = [lams_all[i] for i in li]
    sols = [s for s in solutions(lams, 3, p, 3) if all(s) and any(x != 1 for x in s)]
    s = sols[rng.integers(len(sols))]
    for pr in range(4):
        r = rng.integers(0, p, C2.n)
        q = C2.A.bch(r, (rng.integers(1, p) * xi_img) % p)
        # expected under a correct conversion: 1 (q^-1 r in image of P_2)
        val = 1.0 + 0j
        for lam, si in zip(lams, s):
            val *= src.tr_merge(lam, prob[encode(lam, p)], C3.dil(int(si), C3.section_from(C2, q)), C3.dil(int(si), C3.section_from(C2, r)))
        tested += 1; failed += int(abs(val - 1) > 1e-8)
        print("witness", s, "entry", np.round(val, 6), "(correct conversion would give 1)")
print("tested=%d failed=%d" % (tested, failed))
