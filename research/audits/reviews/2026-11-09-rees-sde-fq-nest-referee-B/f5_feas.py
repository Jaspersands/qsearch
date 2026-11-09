"""Referee B, independent re-check of Fact F5 (p = 5, S = {0, +-1}).

For every spanning GL_2(F_5)-orbit representative L (from orbits_f5.py) decide, with an encoding
written from Lemma 2(A) only (no Lemma R, no unit-direction normalisation, Phi unrestricted in
F_5^2 -- a relaxation that Lemma 2(A)'s proof still covers):
   exists Phi: L -> F_5^2, gamma_alpha in F_5^2 (all 24 alpha != 0) with
      y_alpha(l) = <alpha, Phi(l)> + <gamma_alpha, l> in S  for all alpha != 0, l in L,
   and for each of the 6 projective directions some alpha in it has y_alpha != 0 on L.
Every model is re-checked by plain arithmetic (check()).  Also records, independently, whether a
direct witness exists (mu != 0 with <mu, l> in S for all l in L).
Additionally checks the stronger property 'strong' (every alpha != 0 has y_alpha != 0 on L) is
NOT needed: only weak is asserted.
"""
import itertools, sys, numpy as np, pycosat, multiprocessing as mp, time
p = 5
S = {0, 1, 4}
vecs = [v for v in itertools.product(range(p), repeat=2) if any(v)]
alphas = vecs
F2 = list(itertools.product(range(p), repeat=2))
def dirkey(a):
    lead = a[0] if a[0] else a[1]
    inv = pow(lead, -1, p)
    return ((a[0] * inv) % p, (a[1] * inv) % p)
dirs = {}
for a in alphas:
    dirs.setdefault(dirkey(a), []).append(a)
assert len(dirs) == 6

def check(L, Phi, gam):
    for k, ds in dirs.items():
        nz = False
        for a in ds:
            for l in L:
                y = (a[0] * Phi[l][0] + a[1] * Phi[l][1] + gam[a][0] * l[0] + gam[a][1] * l[1]) % p
                if y not in S:
                    return False
                nz |= (y != 0)
        if not nz:
            return False
    return True

def witness(L):
    for mu in vecs:
        if all((mu[0] * l[0] + mu[1] * l[1]) % p in S for l in L):
            return mu
    return None

def decide(mask):
    L = [vecs[i] for i in range(24) if mask >> i & 1]
    nv = [0]; cl = []
    def var():
        nv[0] += 1; return nv[0]
    def onehot(m):
        vs = [var() for _ in range(m)]
        cl.append(vs[:])
        for i in range(m):
            for j in range(i + 1, m):
                cl.append([-vs[i], -vs[j]])
        return vs
    PH = {l: onehot(25) for l in L}
    GA = {a: onehot(25) for a in alphas}
    for k, ds in dirs.items():
        zs = []
        for a in ds:
            for l in L:
                z = var(); zs.append(z)
                for fi, f in enumerate(F2):
                    af = a[0] * f[0] + a[1] * f[1]
                    for gi, g in enumerate(F2):
                        y = (af + g[0] * l[0] + g[1] * l[1]) % p
                        if y not in S:
                            cl.append([-PH[l][fi], -GA[a][gi]])
                        elif y == 0:
                            cl.append([-z, -PH[l][fi], -GA[a][gi]])
        cl.append(zs)
    sol = pycosat.solve(cl)
    if sol == 'UNSAT':
        return mask, len(L), False, witness(L) is not None
    pos = set(v for v in sol if v > 0)
    Phi = {l: F2[[i for i, v in enumerate(PH[l]) if v in pos][0]] for l in L}
    gam = {a: F2[[i for i, v in enumerate(GA[a]) if v in pos][0]] for a in alphas}
    ok = check(L, Phi, gam)
    return mask, len(L), ok, witness(L) is not None

if __name__ == '__main__':
    reps = np.load('reps_f5.npy')
    if len(sys.argv) > 1:
        reps = reps[:int(sys.argv[1])]
    t0 = time.time()
    by = {}
    bad = []
    with mp.Pool(8) as pool:
        for n, (mask, c, ok, wit) in enumerate(pool.imap_unordered(decide, [int(r) for r in reps], chunksize=20)):
            by.setdefault(c, [0, 0, 0])
            by[c][0] += 1; by[c][1] += ok; by[c][2] += wit
            if not ok:
                bad.append(mask)
                print('NOT VERIFIED-FEASIBLE', mask, [vecs[i] for i in range(24) if mask >> i & 1], flush=True)
            if n % 3000 == 0:
                print(f'  {n} done, {time.time() - t0:.0f}s', flush=True)
    print('|L|: orbits, verified-feasible (model re-checked), with direct witness')
    for c in sorted(by):
        print(f'  {c:2d}: {by[c][0]:5d} {by[c][1]:5d} {by[c][2]:5d}')
    print('total spanning orbits', sum(v[0] for v in by.values()), 'not verified:', len(bad), f'({time.time() - t0:.0f}s)')
