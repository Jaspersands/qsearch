"""Group-level exact simulation (BCH group law) of the template's single-copy invariance.
psi_u(a) = sum_{n in N} w^{-u(n)} |aHn>,  H = <exp(eta)>, eta notin N, N abelian ideal.
Prediction (Prop T, steps 1-2 / Lemma B): psi_u(a).alpha(h) is proportional to psi_u(a) iff
  alpha(h) in HN  and  u o ad_eta |_N = 0.   And psi_u(a).alpha(n) = w^{u(alpha n)} psi_u(a)."""
import sys, json, itertools, random, numpy as np
sys.path.insert(0, '.')
from lie import *

GENW = {'heis3': [(0, 1)], 'fil4': [(0, 1), (0, 2)], 'free23': [(0, 1), (0, 2), (1, 2)], 'fil5': [(0, 1), (0, 2), (0, 3)]}

def rand_auts(C, p, W, k, rng):
    m = C.shape[0]; out = [np.eye(m, dtype=np.int64)]
    tries = 0
    while len(out) < k and tries < 200000:
        tries += 1
        X = rng.integers(0, p, m); Y = rng.integers(0, p, m)
        if (X[0] * Y[1] - X[1] * Y[0]) % p == 0: continue
        img = [X, Y]
        for w in W: img.append(br(img[w[0]], img[w[1]], C, p))
        M = np.array(img) % p
        if all(((C[i, j] @ M) % p == br(M[i], M[j], C, p)).all() for i in range(m) for j in range(m)):
            out.append(M)
    return out

def main(name, p, seed=0):
    rng = np.random.default_rng(seed); random.seed(seed)
    m, b = ALGS[name]; C = tensor(m, b, p); cls = len(lcs(C, p)) - 1
    mul = lambda X, Y: tuple(bch(np.array(X), np.array(Y), C, p, cls).tolist())
    W = GENW[name]
    A_all = rand_auts(C, p, W, 400, rng)
    # also the dilations-type maps: X=(k,0..), Y=(0,k,..) when they are automorphisms
    for k in range(2, p):
        X = np.zeros(m, dtype=np.int64); X[0] = k; Y = np.zeros(m, dtype=np.int64); Y[1] = k
        img = [X, Y]
        for w in W: img.append(br(img[w[0]], img[w[1]], C, p))
        M = np.array(img) % p
        if all(((C[i, j] @ M) % p == br(M[i], M[j], C, p)).all() for i in range(m) for j in range(m)): A_all.append(M)
    ideals = []
    for kd in range(1, m):
        for S in subspaces(m, kd, p):
            if is_ideal(S, C, p) and is_abelian_sub(S, C, p): ideals.append(S)
    stats = dict(alg=name, p=p, cls=cls, abelian_ideals=len(ideals), cases=0, mismatches=0, eigen=0,
                 phase_cases=0, phase_mismatch=0)
    for N in ideals:
        r = len(N)
        Nel = [tuple((np.array(c) @ N % p).tolist()) for c in itertools.product(range(p), repeat=r)]
        Ncoef = list(itertools.product(range(p), repeat=r))
        auts = [M for M in A_all if rank(np.vstack([N, N @ M % p]), p) == r]   # alpha(N) = N
        auts = auts[:1] + random.sample(auts[1:], min(8, len(auts) - 1))
        etas = [e for e in itertools.product(range(p), repeat=m) if rank(np.vstack([N, np.array(e)[None]]), p) > r]
        for eta in random.sample(etas, min(6, len(etas))):
            eta = np.array(eta)
            H = [tuple((t * eta % p).tolist()) for t in range(p)]
            HN = set()
            for hh in H:
                for n in Nel: HN.add(mul(hh, n))
            a = tuple(rng.integers(0, p, m).tolist())
            aH = [mul(a, hh) for hh in H]
            adN = [br(eta, n, C, p) for n in N]     # [eta, N_s]
            for M in auts:
                g = tuple(((eta @ M) % p).tolist())         # alpha(h) = exp(alpha(eta))
                g_in_HN = g in HN
                for ucoef in itertools.product(range(p), repeat=r):
                    # functional u on N: u(sum c_s N_s) = c . ucoef
                    psi = {}
                    for c, n in zip(Ncoef, Nel):
                        ph = (-np.dot(c, ucoef)) % p
                        for x in aH: psi[mul(x, n)] = ph
                    moved = {}
                    for x, ph in psi.items(): moved[mul(x, g)] = ph
                    if set(moved) != set(psi): eig = False
                    else:
                        d = {(moved[x] - psi[x]) % p for x in psi}; eig = len(d) == 1
                    # prediction: u o ad_eta|_N = 0: u([eta,N_s]) for each s; [eta,N_s] in N, coords:
                    def ucoord(x):
                        if not np.any(x): return 0
                        Aug = np.vstack([N, x[None]]).T % p; ns = nullspace(Aug, p)[0]
                        cc = (-ns[:r] * pow(int(ns[r]), -1, p)) % p
                        return int(np.dot(cc, ucoef) % p)
                    pred = g_in_HN and all(ucoord(x) == 0 for x in adN)
                    stats['cases'] += 1; stats['eigen'] += int(eig); stats['mismatches'] += int(eig != pred)
                    # N-phase check on one random n
                    if r and rng.random() < 0.3:
                        ci = rng.integers(0, p, r); n = tuple((ci @ N % p).tolist())
                        an = tuple((np.array(n) @ M % p).tolist())
                        mv = {mul(x, an): ph for x, ph in psi.items()}
                        stats['phase_cases'] += 1
                        if set(mv) != set(psi): stats['phase_mismatch'] += 1
                        else:
                            d = {(mv[x] - psi[x]) % p for x in psi}
                            expect = ucoord(np.array(an))
                            if d != {expect}: stats['phase_mismatch'] += 1
    print(json.dumps(stats), flush=True)

if __name__ == '__main__':
    for name, p in [('heis3', 5), ('heis3', 7), ('fil4', 5), ('fil4', 7), ('free23', 5), ('fil5', 5)]:
        main(name, p)
