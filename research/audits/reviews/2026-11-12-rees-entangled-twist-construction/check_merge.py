"""Check 3 (exact, finite): merging two copies by measuring k = g_1 g_2^{-1}.
Two coset states of H, projected on central labels lam_1, lam_2 (right action of g3), are
combined into Psi(g) ~ psi_1(k g) psi_2(g).  We check, over the whole group:
  * Psi is right-H-invariant, has central label lam_1 + lam_2, and is supported on ONE coset
    of K = H g3 (the merge never fails);
  * strong Fourier sampling of Psi puts mass exactly 1/p on each sigma_{lam_1+lam_2,kappa}
    (regular case) and returns that irrep's H-fixed vector (closed form).
So label arithmetic is addition only, and a merged copy is distributed like a fresh copy.
Usage: python check_merge.py p trials"""
import sys, random, numpy as np
from core import *

p = int(sys.argv[1]); trials = int(sys.argv[2])
rng = random.Random(99 + p)
G = all_elements(p); NG = len(G)
om = np.exp(2j * np.pi / p)
labels = [(a, b) for a in range(p) for b in range(p) if (a, b) != (0, 0)]
g3 = [np.array([0, 0, 0, a, b]) for a in range(p) for b in range(p)]


def coset_label_state(a, v, lam):
    """P_lam |aH> as a vector on G (normalized):  sum_{t,n} w^{-lam(n)} |a h^t n>."""
    psi = np.zeros(NG, dtype=complex)
    for t in range(p):
        g = bch(a, (t * v) % p, p)
        for n in g3:
            psi[index((g + n) % p, p)] += om ** (-(lam[0] * n[U] + lam[1] * n[W]) % p)
    return psi / np.linalg.norm(psi)


bad_inv = bad_lab = bad_supp = bad_unif = bad_vec = 0; ncases = 0
for tr in range(trials):
    v = random_v(p, rng)
    lam1, lam2 = rng.choice(labels), rng.choice(labels)
    lam = ((lam1[0] + lam2[0]) % p, (lam1[1] + lam2[1]) % p)
    if lam == (0, 0) or any(Frame(l, 0, p).D(v) == 0 for l in (lam1, lam2, lam)):
        continue
    a1, a2 = random_v(p, rng, False), random_v(p, rng, False)
    psi1, psi2 = coset_label_state(a1, v, lam1), coset_label_state(a2, v, lam2)
    s1 = np.nonzero(np.abs(psi1) > 1e-12)[0]; s2 = np.nonzero(np.abs(psi2) > 1e-12)[0]
    g1, g2 = G[rng.choice(list(s1))], G[rng.choice(list(s2))]
    k = bch(g1, (-g2) % p, p)                       # measured value of g_1 g_2^{-1}
    kg = index(bch(np.broadcast_to(k, G.shape), G, p), p)
    Psi = psi1[kg] * psi2
    Psi /= np.linalg.norm(Psi)
    ncases += 1
    # right-H invariance and label
    gh = index(bch(G, np.broadcast_to(v, G.shape), p), p)
    if not np.allclose(Psi[gh], Psi):
        bad_inv += 1
    n = np.array([0, 0, 0, 1, 2]); gn = index((G + n) % p, p)
    if not np.allclose(Psi[gn], om ** (-(lam[0] * 1 + lam[1] * 2) % p) * Psi):
        bad_lab += 1
    supp = np.nonzero(np.abs(Psi) > 1e-12)[0]
    if len(supp) != p ** 3:
        bad_supp += 1
    # strong Fourier sampling over the irreps with label lam
    probs = []
    for kap in range(p):
        F = Frame(lam, kap, p)
        S = F.sigma_all(G[supp])
        Fh = np.tensordot(Psi[supp], S, axes=1)
        probs.append(p / NG * np.linalg.norm(Fh) ** 2)
        psi = F.fixed_vector_formula(v)
        u, sv, vh = np.linalg.svd(Fh)
        if sv[1] > 1e-8 or not phase_equal(vh[0].conj(), psi):
            bad_vec += 1
    if not np.allclose(probs, 1 / p):
        bad_unif += 1
print(f'p={p} merges={ncases} not_H_invariant={bad_inv} wrong_label={bad_lab} '
      f'support!=p^3={bad_supp} kappa_law_not_uniform={bad_unif} '
      f'output_not_fixed_vector={bad_vec}')
