"""CNF (pycosat) version of gadget_sat.py: feasibility of a d-dimensional realization from a
k-dependency bundle with pattern set L over F_p and coefficient set S (0 in S).

Variables (one-hot):  phi[l][j] in S;  g[a][i] in F_p (gamma_alpha, i-th coordinate);
                      t[a][l][i] = g[a][i]*l_i;  lam[a][l] = sum_i t (chain of adders);
                      u[a][l] = <alpha, phi(l)>;  constraint: u + lam in S.
Nondegeneracy (optional): for every alpha, some l has u + lam != 0.
Every SAT model is re-verified by brute force.  Same CLI as gadget_sat.py.
"""
import sys, itertools, argparse, time
import pycosat
from gadget_sat import parse_S, parse_L, powers


class CNF:
    def __init__(self):
        self.n = 0
        self.clauses = []

    def var(self):
        self.n += 1
        return self.n

    def onehot(self, m):
        vs = [self.var() for _ in range(m)]
        self.clauses.append(vs[:])
        for i in range(m):
            for j in range(i + 1, m):
                self.clauses.append([-vs[i], -vs[j]])
        return vs


def build(p, S, k, d, L, nondeg=True, fix=None, weak=False):
    S = sorted(S)
    Sidx = {s: i for i, s in enumerate(S)}
    alphas = [a for a in itertools.product(range(p), repeat=d) if any(a)]
    unit = {tuple(1 if i == j else 0 for i in range(d)) for j in range(d)}
    c = CNF()
    phi = {(l, j): c.onehot(len(S)) for l in L for j in range(d)}
    g = {}
    for a in alphas:
        if a in unit:
            continue
        g[a] = [c.onehot(p) for _ in range(k)]
    if fix:
        fix(c, phi, g, S)
    dir_nz = {}
    for a in alphas:
        nzs = []
        for l in L:
            # u = <alpha, phi(l)> one-hot over F_p
            u = c.onehot(p)
            for combo in itertools.product(range(len(S)), repeat=d):
                val = sum(a[j] * S[combo[j]] for j in range(d)) % p
                c.clauses.append([-phi[(l, j)][combo[j]] for j in range(d)] + [u[val]])
            if a in unit:
                lam = None
            else:
                # t_i = g_i * l_i, then lam = sum t_i by a chain
                parts = []
                for i in range(k):
                    if l[i] == 0:
                        continue
                    t = c.onehot(p)
                    for gi in range(p):
                        c.clauses.append([-g[a][i][gi], t[(gi * l[i]) % p]])
                    parts.append(t)
                if not parts:
                    lam = None
                else:
                    lam = parts[0]
                    for t in parts[1:]:
                        s2 = c.onehot(p)
                        for x in range(p):
                            for y in range(p):
                                c.clauses.append([-lam[x], -t[y], s2[(x + y) % p]])
                        lam = s2
            # y = u + lam in S; nz <-> y != 0
            nz = c.var()
            nzs.append(nz)
            if lam is None:
                for x in range(p):
                    if x not in Sidx:
                        c.clauses.append([-u[x]])
                c.clauses.append([-nz, -u[0]])
            else:
                for x in range(p):
                    for y in range(p):
                        if (x + y) % p not in Sidx:
                            c.clauses.append([-u[x], -lam[y]])
                        if (x + y) % p == 0:
                            c.clauses.append([-nz, -u[x], -lam[y]])
        if nondeg and not weak:
            c.clauses.append(nzs)
        if nondeg and weak:
            lead = next(x for x in a if x)
            key = tuple((x * pow(lead, -1, p)) % p for x in a)
            dir_nz.setdefault(key, []).extend(nzs)
    if nondeg and weak:
        for key, nzs in dir_nz.items():
            c.clauses.append(nzs)
    return c, phi, g, alphas, unit


def decode(sol, p, S, k, d, L, phi, g, alphas, unit):
    S = sorted(S)
    pos = set(v for v in sol if v > 0)
    Phi = {l: tuple(S[[i for i, v in enumerate(phi[(l, j)]) if v in pos][0]] for j in range(d)) for l in L}
    gamma = {}
    for a in alphas:
        if a in unit:
            gamma[a] = (0,) * k
        else:
            gamma[a] = tuple([x for x, v in enumerate(g[a][i]) if v in pos][0] for i in range(k))
    return Phi, gamma


def verify(p, S, k, d, L, Phi, gamma, nondeg=True, weak=False):
    Sset = set(S)
    dir_ok = {}
    for a in itertools.product(range(p), repeat=d):
        if not any(a):
            continue
        anynz = False
        for l in L:
            y = (sum(a[j] * Phi[l][j] for j in range(d)) + sum(gamma[a][i] * l[i] for i in range(k))) % p
            if y not in Sset:
                return False, (a, l, y)
            anynz |= y != 0
        lead = next(x for x in a if x)
        key = tuple((x * pow(lead, -1, p)) % p for x in a)
        dir_ok[key] = dir_ok.get(key, False) or anynz
        if nondeg and not weak and not anynz:
            return False, ('degenerate', a)
    if nondeg and weak and not all(dir_ok.values()):
        return False, ('degenerate direction',)
    return True, None


def solve(p, S, k, d, L, nondeg=True, fix=None, verbose=False, weak=False):
    t0 = time.time()
    c, phi, g, alphas, unit = build(p, S, k, d, L, nondeg, fix, weak)
    if verbose:
        print(f'  cnf: {c.n} vars, {len(c.clauses)} clauses', flush=True)
    sol = pycosat.solve(c.clauses)
    dt = time.time() - t0
    if sol == 'UNSAT':
        return 'unsat', None, dt
    Phi, gamma = decode(sol, p, S, k, d, L, phi, g, alphas, unit)
    ok, why = verify(p, S, k, d, L, Phi, gamma, nondeg, weak)
    assert ok, why
    return 'sat', (Phi, gamma), dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int)
    ap.add_argument('S')
    ap.add_argument('k', type=int)
    ap.add_argument('d', type=int)
    ap.add_argument('L')
    ap.add_argument('--no-nondeg', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--weak', action='store_true', help='nondegeneracy per projective direction only')
    A = ap.parse_args()
    S = parse_S(A.p, A.S)
    L = parse_L(A.p, A.k, A.L)
    r, sol, dt = solve(A.p, S, A.k, A.d, L, nondeg=not A.no_nondeg, verbose=not A.quiet, weak=A.weak)
    print(f'p={A.p} S={S} k={A.k} d={A.d} L={A.L} (|L|={len(L)}) nondeg={not A.no_nondeg}: {r.upper()} [{dt:.1f}s]', flush=True)
    if sol and not A.quiet:
        Phi, gamma = sol
        print(' Phi (label -> base realizer values):')
        for l in L:
            print('  ', l, '->', Phi[l])
        print(' gamma_alpha:')
        for a, gg in gamma.items():
            print('  ', a, '->', gg)


if __name__ == '__main__':
    main()
