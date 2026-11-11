"""Independent, SAT-free decision of the q = 11 interval cell (S = {0,+-1,+-2}, k = 2, d = 2, labels
F_11^* x F_11), free problem modulo Lemma R (Phi arbitrary on every label).
(2026-11-11-rees-sde-interval-s.md, section 2, "SAT-free check".)

By Lemma L every direction D (base point = representative with leading coordinate 1) has line data
a_D = (u, v) in A, c_r = (u_r, v_r), and y_D(l) = f must satisfy r f + <c_r, l> in S for r = 2..5.
At p = 11 that f is UNIQUE for every a in A and every label (asserted below), so y_D = G_{a_D} is a
function of a_D alone.  Conversely any choice (a_D)_D with
    G_{a_D} - G_{a_e1} - d G_{a_e2}  in  R|_L   (R = linear functionals)  for D = (1, d), d = 1..10
gives a solution: Phi = (G_{a_e1}, G_{a_e2}), gamma_D = that functional, gamma_{rD} = r gamma_D + c_r,
weakly nondegenerate because a_D != 0.  This script enumerates ALL 600 x 600 pairs (a_e1, a_e2)
(no symmetry used) and counts the pairs for which every d has a matching a_D.
Plain Python / numpy integers.
"""
import itertools, numpy as np
p, K = 11, 2
S = sorted({x % p for x in range(-K, K + 1)}); Ss = set(S)
R = [2, 3, 4, 5]; n = len(R)
T = set()
for f in S:
    for t in itertools.product(*[[(s - r * f) % p for s in S] for r in R]): T.add(t)
Ts = {t for t in T if all(tuple((a * x) % p for x in t) in T for a in range(1, p))}
A = [(u, v) for u in Ts for v in itertools.product(range(p), repeat=n)
     if (any(u) or any(v)) and all(tuple((u[i] + b * v[i]) % p for i in range(n)) in Ts for b in range(p))]
print('|A| =', len(A))
L = [(a, b) for a in range(1, p) for b in range(p)]
def G(uv):
    u, v = uv
    out = []
    for (a, b) in L:
        fs = [f for f in S if all((r * f + u[i] * a + v[i] * b) % p in Ss for i, r in enumerate(R))]
        assert len(fs) == 1, (uv, (a, b), fs)
        out.append(fs[0])
    return np.array(out, dtype=np.int64)
Gs = np.array([G(a) for a in A])                     # 600 x 110
La = np.array([l[0] for l in L]); Lb = np.array([l[1] for l in L])
i10 = L.index((1, 0)); i11 = L.index((1, 1))
def canon(H):
    """H: (N, 110) values mod p; subtract the linear functional c with c(1,0) = H(1,0), c(1,1) = H(1,1)"""
    ca = H[:, i10]; cb = (H[:, i11] - H[:, i10]) % p
    return (H - ca[:, None] * La[None, :] - cb[:, None] * Lb[None, :]) % p
table = {row.tobytes() for row in canon(Gs)}
print('distinct classes of G_a mod R:', len(table))
good_pairs = 0; best = 0
for i1 in range(len(A)):
    H = Gs[i1][None, :] + 0 * Gs
    ok = np.ones(len(A), dtype=bool); cnt = np.zeros(len(A), dtype=np.int64)
    for d in range(1, p):
        C = canon((Gs[i1][None, :] + d * Gs) % p)    # rows: a_e2 ranges over A
        hit = np.array([row.tobytes() in table for row in C])
        ok &= hit; cnt += hit
    good_pairs += int(ok.sum()); best = max(best, int(cnt.max()))
print(f'pairs (a_e1, a_e2) checked: {len(A)**2}; pairs with a match for every d = 1..10: {good_pairs}; '
      f'max number of d matched by any pair: {best} of 10')
print('VERDICT:', 'UNSAT (no solution of the free problem mod Lemma R)' if good_pairs == 0 else 'SAT candidates exist')

# Positive control: take a pair matching the most d's, build Phi and gamma on e1, e2 and the matched
# directions (1, d) exactly as in the converse construction, and check by plain arithmetic that every
# y_{lam D}(l) (all lam in F_11^*, all l in L) lies in S on those directions and is not identically 0.
Aidx = {row.tobytes(): j for j, row in enumerate(canon(Gs))}
for i1 in range(len(A)):
    found = None
    for i2 in range(len(A)):
        match = {}
        for d in range(1, p):
            key = canon(((Gs[i1] + d * Gs[i2]) % p)[None, :])[0].tobytes()
            if key in Aidx: match[d] = Aidx[key]
        if len(match) == best:
            found = (i2, match); break
    if found: break
i2, match = found
def lam_line(uv):
    u, v = uv; c = {1: (0, 0), p - 1: (0, 0)}
    for i, r in enumerate(R):
        c[r] = (u[i], v[i]); c[p - r] = ((-u[i]) % p, (-v[i]) % p)
    return c
Phi = {l: (int(Gs[i1][j]), int(Gs[i2][j])) for j, l in enumerate(L)}
dirs = {(1, 0): (A[i1], (0, 0)), (0, 1): (A[i2], (0, 0))}
for d, j in match.items():
    H = (Gs[j] - Gs[i1] - d * Gs[i2]) % p
    ga, gb = int(H[i10]), int((H[i11] - H[i10]) % p)
    assert all((ga * a + gb * b) % p == H[k] for k, (a, b) in enumerate(L))
    dirs[(1, d)] = (A[j], (ga, gb))
bad = 0
for D, (a, g0) in dirs.items():
    c = lam_line(a); anynz = False
    for lam in range(1, p):
        al = ((lam * D[0]) % p, (lam * D[1]) % p)
        g = ((lam * g0[0] + c[lam][0]) % p, (lam * g0[1] + c[lam][1]) % p)
        for l in L:
            y = (al[0] * Phi[l][0] + al[1] * Phi[l][1] + g[0] * l[0] + g[1] * l[1]) % p
            bad += y not in Ss; anynz |= y != 0
    bad += not anynz
print(f'positive control: pair ({i1},{i2}) matches d in {sorted(match)}; partial solution on {len(dirs)} of 12 '
      f'directions checked over all lam and labels: {"OK" if bad == 0 else f"{bad} violations"}')
