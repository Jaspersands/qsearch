"""Verification step and brute-force branch of Theorem F23, exact on true labelled copies (AI-written,
pending human review).  Pass probability of phase estimation of R_hhat on one labelled copy is
<psi| (1/p) sum_t R_{hhat^t} |psi>; claimed: = 1 if <hhat> = H, <= 1/p (averaged over the uniform label) otherwise.
Also: average over all p^3(p+1) wrong hard cyclic candidates at p = 5 (the brute-force branch).
Usage: python check_verify.py p ncand seed"""
import sys, itertools, numpy as np
from ref_core import *

p, ncand, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
F = Field(p); G = Group(F); rng = np.random.default_rng(seed)

def pass_prob(vec, etah):
    sh = [G.idx(bch(G.ALL, np.broadcast_to((t * np.asarray(etah)) % p, G.ALL.shape), F)) for t in range(p)]
    return float(np.real(sum(np.vdot(vec[s], vec) for s in sh) / p))

eta = np.array([1, 3, 2, 4, 6]) % p
def copyvec():
    lam, psi = labelled_copy(G, eta, rng); return lam, dense_from_label(lam, psi, F)

res = dict(correct=[], inK=[], notK=[])
for it in range(ncand):
    lam, vec = copyvec()
    res['correct'].append(pass_prob(vec, (int(rng.integers(1, p)) * eta) % p))
    c = rng.integers(0, p, 2)
    while (c == eta[3:]).all(): c = rng.integers(0, p, 2)
    res['inK'].append(pass_prob(vec, np.array([eta[0], eta[1], eta[2], c[0], c[1]])))
    while True:
        w = rng.integers(0, p, 5)
        if (w[0] or w[1]) and not all((w[i] * eta[j] - w[j] * eta[i]) % p == 0 for i in range(3) for j in range(3)): break
    res['notK'].append(pass_prob(vec, w))
for k, v in res.items():
    print('p=%d %-8s candidates: pass probability min %.6f mean %.6f max %.6f (1/p = %.6f)' % (p, k, min(v), np.mean(v), max(v), 1 / p))

if p == 5:   # brute-force branch: every hard cyclic subgroup, one fresh copy each, exact pass probabilities
    cands = set()
    for v in itertools.product(range(p), repeat=5):
        if not (v[0] or v[1]): continue
        k = next(x for x in v if x); iv = F.inv(k); cands.add(tuple(x * iv % p for x in v))
    assert len(cands) == p ** 3 * (p + 1)
    tot = 0.0; ncorr = 0
    for cnd in cands:
        lam, vec = copyvec(); pp = pass_prob(vec, cnd)
        if all((cnd[i] * eta[j] - cnd[j] * eta[i]) % p == 0 for i in range(5) for j in range(5)): ncorr += 1; assert pp > 1 - 1e-9
        else: tot += pp
    print('p=5 brute force: %d candidates (= p^3(p+1)), %d correct (pass prob 1); mean pass prob of wrong ones %.6f (1/p = %.3f);'
          ' with v = 6 copies the union bound is p^3(p+1) p^-6 = %.4f <= 2/p^2 = %.4f' % (len(cands), ncorr, tot / (len(cands) - 1), 1 / p, (p + 1) / p ** 3, 2 / p ** 2))
