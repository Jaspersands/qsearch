"""Explicit 2-dim gadget from two dependencies with nested supports (patterns {1,2} x F_3),
and a numerical verification on random instances built to have such a pair."""
import itertools, numpy as np
from generic_piece import defect_set
others, E = defect_set(2)
alphas = [a for a in itertools.product(range(3), repeat=2) if any(a)]
T = [(a, b) for a in (1, 2) for b in range(3)]
Es = set(E); zero6 = (0,) * 6
def lin(u, v, a, b): return tuple((a * x + b * y) % 3 for x, y in zip(u, v))
vecs = list(itertools.product(range(3), repeat=6))
sol = None
for u in vecs:
    for v in vecs:
        if u == zero6 or v == zero6 or v in (u, lin(u, u, 2, 0)): continue
        if all(lin(u, v, a, b) in Es for (a, b) in T):
            # pick one local y per class, require every alpha covered
            choice = {}
            for pi in T:
                e = lin(u, v, *pi); choice[pi] = E[e]
            for pick in itertools.product(*[choice[pi] for pi in T]):
                cov = set()
                for y in pick:
                    for j, bit in enumerate(y):
                        if bit: cov.add(alphas[j])
                if len(cov) == 8:
                    sol = (u, v, dict(zip(T, pick))); break
            if sol: break
    if sol: break
u, v, pick = sol
print("C(e1) =", u, " C(e2) =", v)
print("gadget: for alpha in F_3^2\\0, the subset y_alpha is the union of the pattern classes P_(a,b) listed:")
for j, al in enumerate(alphas):
    classes = [pi for pi in T if pick[pi][j] == 1]
    print(f"  alpha={al}: classes {classes}")
# numerical verification: build random instances with two dependencies whose patterns lie in T
rng = np.random.default_rng(3)
for q in (6, 10, 20, 40):
    for trial in range(5):
        N = q + 2
        while True:
            pats = [T[i] for i in rng.integers(0, 6, N)]
            if all(any(p == t for p in pats) for t in T): break
        d1 = np.array([p[0] for p in pats]); d2 = np.array([p[1] for p in pats])
        # random columns for first N-2, solve last two from the two relations
        while True:
            cols = [rng.integers(0, 3, q) for _ in range(N - 2)]
            M = np.array([[d1[-2], d1[-1]], [d2[-2], d2[-1]]]) % 3
            det = (M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]) % 3
            if det == 0:
                pats[-1] = T[rng.integers(0, 6)]; d1 = np.array([p[0] for p in pats]); d2 = np.array([p[1] for p in pats]); continue
            inv = (np.array([[M[1, 1], -M[0, 1]], [-M[1, 0], M[0, 0]]]) * det) % 3  # det^{-1} = det in F_3
            r1 = -sum(d1[i] * cols[i] for i in range(N - 2)) % 3
            r2 = -sum(d2[i] * cols[i] for i in range(N - 2)) % 3
            x = (inv[0, 0] * r1 + inv[0, 1] * r2) % 3; y = (inv[1, 0] * r1 + inv[1, 1] * r2) % 3
            cols += [x, y]; break
        assert (sum(d1[i] * cols[i] for i in range(N)) % 3 == 0).all() and (sum(d2[i] * cols[i] for i in range(N)) % 3 == 0).all()
        ysum = {}
        for j, al in enumerate(alphas):
            idx = [i for i in range(N) if pick[pats[i]][j] == 1]
            assert idx, "empty subset"
            ysum[al] = sum(cols[i] for i in idx) % 3
        h1, h2 = ysum[(1, 0)], ysum[(0, 1)]
        ok = all(((ysum[al] - (al[0] * h1 + al[1] * h2)) % 3 == 0).all() for al in alphas)
        indep = np.linalg.matrix_rank(np.array([h1, h2])) == 2 and not ((h1 - h2) % 3 == 0).all() and not ((h1 + h2) % 3 == 0).all() and h1.any() and h2.any()
        assert ok, "gadget sums wrong"
        if trial == 0: print(f"q={q}: 8 class-union subsets realize alpha_1 h1 + alpha_2 h2 for all alpha: OK; h1,h2 independent over F_3: {indep}")
print("nested-support gadget verified on 20 constructed instances (q = 6, 10, 20, 40); witnesses checked by direct summation")
