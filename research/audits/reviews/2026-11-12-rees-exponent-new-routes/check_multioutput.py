"""Exact finite checks of multi-output merges (Theorem MO2 / Proposition MO3).

MO2 (stage 2): targets rho_{lambda_i} on G_2, r = 2 output registers on the
abelian quotient Q = G_1; target i gets the right action by
Phi_i(q) = delta_{w_i^(1)}(sigma q_1) * delta_{w_i^(2)}(sigma q_2).
Output entry = prod_i tr(rho_{lambda_i} R_{Phi_i(r)^{-1} Phi_i(q)}), with
tr(rho_lambda R_g) = [g_1 in t h] * omega^{lambda . g_2}  (Lemma lem:central).
Claim: entry == prod_j [q_j - r_j in t h] exactly iff W = span(w^(1), w^(2))
is totally isotropic for q_lambda(w) = sum_i w_i^2 lambda_i.
MO3 (stage d >= 3): the same ansatz with overlapping supports is not exact.
Finite checks only.
"""
import itertools, sys
import numpy as np
from lie import Cover, in_span

rng = np.random.default_rng(20261112)

def g1(cov, vecs):
    return {1: np.asarray(vecs, dtype=np.int64) % cov.p}

def entry_data(cov, v, lam, W, q, r):
    """q, r: lists of r arrays (N,m) (grade-1 quotient elements).
    Returns (indicator_product (N,), phase_exponent (N,))."""
    p = cov.p; N = q[0].shape[0]
    ind = np.ones(N, dtype=bool); ph = np.zeros(N, dtype=np.int64)
    for i in range(W.shape[0]):
        if not W[i].any():
            continue
        def Phi(x):
            out = None
            for j in range(W.shape[1]):
                term = cov.dil(int(W[i, j]), g1(cov, x[j]))
                out = term if out is None else cov.mul(out, term)
            return out
        g = cov.mul(cov.inv(Phi(r)), Phi(q))
        ind &= in_span(g[1], [v], p)
        ph = (ph + g[2] @ lam[i]) % p
    return ind, ph

def target(cov, v, q, r):
    t = np.ones(q[0].shape[0], dtype=bool)
    for qj, rj in zip(q, r):
        t &= in_span((qj - rj) % cov.p, [v], cov.p)
    return t

def iso_pairs(p, lam, gam2, M, want_iso=True, limit=1):
    """Find (w1, w2) independent, each q(w)=0; isotropic pair if want_iso else b != 0."""
    vecs = np.array(list(itertools.product(range(p), repeat=M)), dtype=np.int64)
    Lm = lam[:, gam2]                     # (M, a)
    qv = ((vecs ** 2) @ Lm) % p
    iso = vecs[np.all(qv == 0, axis=1) & vecs.any(axis=1)]
    # keep one representative per projective point
    reps = []
    seen = set()
    for w in iso:
        nz = w[np.nonzero(w)[0][0]]
        wn = tuple((w * pow(int(nz), -1, p)) % p)
        if wn not in seen:
            seen.add(wn); reps.append(np.array(wn))
    out = []
    for a_, b_ in itertools.combinations(reps, 2):
        bil = ((a_ * b_) @ Lm) % p
        if (not bil.any()) == want_iso:
            # require overlapping supports (indecomposable pair)
            if (a_ * b_).any():
                out.append((a_, b_))
                if len(out) >= limit:
                    break
    return out

def run_stage2(name, p, v, M, exhaustive=False, nsamp=4000):
    cov = Cover(name, p, 2); m = cov.m; gam2 = cov.gam[2]
    for trial in range(200):
        lam = np.zeros((M, m), dtype=np.int64)
        lam[:, gam2] = rng.integers(0, p, size=(M, len(gam2)))
        good = iso_pairs(p, lam, gam2, M, True)
        bad = iso_pairs(p, lam, gam2, M, False)
        if good and bad:
            break
    else:
        print(f"{name} p={p} M={M}: no isotropic overlapping pair found"); return
    res = {}
    for tag, (w1, w2) in [("isotropic", good[0]), ("non-isotropic", bad[0])]:
        W = np.stack([w1, w2], axis=1)
        if exhaustive:
            Q = np.array(list(itertools.product(range(p), repeat=m)), dtype=np.int64)
            idx = np.array(list(itertools.product(range(len(Q)), repeat=4)))
            q = [Q[idx[:, 0]], Q[idx[:, 1]]]; r = [Q[idx[:, 2]], Q[idx[:, 3]]]
        else:
            # same-coset pairs (all multiples of v) plus random pairs
            N = nsamp
            r = [rng.integers(0, p, size=(N, m)) for _ in range(2)]
            c = rng.integers(0, p, size=(N, 2))
            q = [(r[j] + c[:, j:j + 1] * v) % p for j in range(2)]
            rq = [rng.integers(0, p, size=(N, m)) for _ in range(2)]
            rr = [rng.integers(0, p, size=(N, m)) for _ in range(2)]
            q = [np.vstack([q[j], rq[j]]) for j in range(2)]
            r = [np.vstack([r[j], rr[j]]) for j in range(2)]
        ind, ph = entry_data(cov, v, lam, W, q, r)
        t = target(cov, v, q, r)
        ok_ind = bool(np.all(ind == t))
        ok_ph = bool(np.all(ph[t] == 0))
        res[tag] = (ok_ind, ok_ph, int(t.sum()), len(t), int((ph[t] != 0).sum()))
        print(f"{name} p={p} M={M} {tag}: W^T={W.T.tolist()} indicator_exact={ok_ind} "
              f"phase_exact={ok_ph} same-coset={t.sum()}/{len(t)} phase_failures={(ph[t]!=0).sum()}")
    return res

def run_stage3_counterexample(name, p, v, a):
    """Overlapping weights at d = 3: r_1 = e, q_1 = t v, q_2 = r_2 = t a."""
    cov = Cover(name, p, 3); m = cov.m
    e = {1: np.zeros((1, m), dtype=np.int64)}
    hv = {1: np.array([v]) % p}; aa = {1: np.array([a]) % p}
    for (w1, w2) in [(1, 1), (2, 3), (1, 0), (0, 1)]:
        Phi_r = cov.mul(cov.dil(w1, e), cov.dil(w2, aa))
        Phi_q = cov.mul(cov.dil(w1, hv), cov.dil(w2, aa))
        g = cov.mul(cov.inv(Phi_r), Phi_q)
        gr2 = g.get(2, np.zeros((1, m), dtype=np.int64))
        inHZ = bool(in_span(g[1], [v], p)[0]) and not gr2.any()
        print(f"{name} p={p} d=3 weights (w1,w2)=({w1},{w2}): grade1={g[1][0].tolist()} "
              f"grade2={gr2[0].tolist()} g in H Z_3: {inHZ}")

if __name__ == "__main__":
    print("== MO2, Heisenberg, p=3, exhaustive over Q^2 x Q^2 ==")
    run_stage2("heis", 3, np.array([1, 0, 0]), 4, exhaustive=True)
    for p in (5, 7):
        print(f"== MO2, Heisenberg, p={p}, sampled ==")
        run_stage2("heis", p, np.array([1, 0, 0]), 4)
    for p in (5, 7):
        print(f"== MO2, free class-3 (stage 2, a=3), p={p}, sampled ==")
        run_stage2("free3", p, np.array([1, 0, 1, 1, 0]), 7 if p == 5 else 7)
    print("== MO2, filiform m=4 (stage 2, a=2), p=5 ==")
    run_stage2("fili4", 5, np.array([1, 0, 0, 0]), 5)
    print("== MO3 counterexamples at d = 3 ==")
    run_stage3_counterexample("free3", 5, [1, 0, 1, 1, 0], [0, 1, 0, 0, 0])
    run_stage3_counterexample("free3", 7, [1, 0, 1, 1, 0], [0, 1, 0, 0, 0])
    run_stage3_counterexample("fili4", 5, [1, 0, 0, 0], [0, 1, 0, 0])
