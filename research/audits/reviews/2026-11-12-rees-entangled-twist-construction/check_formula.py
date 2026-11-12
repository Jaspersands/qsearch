"""Check 1 (exact, finite): the dim-p irreps sigma_{lam,kappa}, the closed-form H-fixed vector,
and that strong Fourier sampling of a coset state returns that vector.
Usage: python check_formula.py p"""
import sys, random, numpy as np
from core import *

p = int(sys.argv[1]) if len(sys.argv) > 1 else 5
rng = random.Random(1000 + p)
G = all_elements(p)
labels = [(a, b) for a in range(p) for b in range(p) if (a, b) != (0, 0)]

# (i) homomorphism, random checks
bad_hom = 0
for _ in range(200):
    F = Frame(rng.choice(labels), rng.randrange(p), p)
    g1 = random_v(p, rng, False); g2 = random_v(p, rng, False)
    if not np.allclose(F.sigma(bch(g1, g2, p)), F.sigma(g1) @ F.sigma(g2)):
        bad_hom += 1
print(f'p={p} homomorphism_failures={bad_hom}/200')

# (ii) irreducibility and inequivalence via characters (all of G)
if p <= 7:
    lam_sample = labels if p == 5 else rng.sample(labels, 6)
    worst_norm = 0.0; worst_cross = 0.0
    for lam in lam_sample:
        chars = []
        for k in range(p):
            S = Frame(lam, k, p).sigma_all(G)
            chars.append(np.trace(S, axis1=1, axis2=2))
        for i in range(p):
            worst_norm = max(worst_norm, abs(np.vdot(chars[i], chars[i]) / len(G) - 1))
            for j in range(i):
                worst_cross = max(worst_cross, abs(np.vdot(chars[i], chars[j]) / len(G)))
    print(f'p={p} labels_checked={len(lam_sample)} max|<chi,chi>-1|={worst_norm:.2e} '
          f'max|<chi_k,chi_k\'>|={worst_cross:.2e}  (sum d^2 over lam!=0 irreps = '
          f'{(p*p-1)*p*p*p} = p^5-p^3)')

# (iii) closed-form fixed vector vs orbit construction
bad_fix = bad_orbit = n = 0
for _ in range(400):
    lam = rng.choice(labels); F = Frame(lam, rng.randrange(p), p)
    v = random_v(p, rng)
    if F.D(v) == 0:
        continue
    n += 1
    psi = F.fixed_vector_formula(v)
    if not np.allclose(F.sigma(v) @ psi, psi):
        bad_fix += 1
    if not phase_equal(F.fixed_vector_orbit(v), psi):
        bad_orbit += 1
print(f'p={p} closed_form_cases={n} not_fixed={bad_fix} differs_from_orbit_vector={bad_orbit}')

# (iv) strong Fourier sampling of an actual coset state (brute force over G)
if p <= 7:
    trials = 3 if p == 5 else 1
    bad_rank = bad_vec = 0; probs_ok = 0; tot = 0
    for _ in range(trials):
        v = random_v(p, rng); a = random_v(p, rng, False)
        coset = {int(index(bch(a, (t * v) % p, p), p)) for t in range(p)}
        amp = np.zeros(len(G)); amp[list(coset)] = 1 / np.sqrt(p)
        supp = np.array(sorted(coset))
        lam_list = labels if p == 5 else rng.sample(labels, 8)
        for lam in lam_list:
            for k in range(p):
                F = Frame(lam, k, p)
                S = F.sigma_all(G[supp])
                Fh = np.tensordot(amp[supp], S, axes=1)           # sum_g psi(g) sigma(g)
                prob = p / len(G) * np.linalg.norm(Fh) ** 2
                tot += 1
                if F.D(v) == 0:
                    continue
                sv = np.linalg.svd(Fh, compute_uv=False)
                if sv[1] > 1e-8:
                    bad_rank += 1
                if abs(prob - p ** -3) < 1e-9:
                    probs_ok += 1
                # Fh = sqrt(p) sigma(a) |psi><psi|  : row space is <psi|
                psi = F.fixed_vector_formula(v)
                target = np.sqrt(p) * F.sigma(a) @ np.outer(psi, psi.conj())
                if not np.allclose(Fh, target, atol=1e-8):
                    bad_vec += 1
    print(f'p={p} SFS irreps tested={tot} regular: rank>1={bad_rank} '
          f'Fhat!=sqrt(p)*sigma(a)|psi><psi|={bad_vec} prob==p^-3 in {probs_ok} cases')
