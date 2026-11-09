"""Feasibility of a d-dimensional realization from a k-dependency bundle over F_p.

Setting.  Columns v_i in F_p^q, a set X with dependencies delta^1..delta^k spanning
K <= D(X).  The pattern (label) of column i is ell_i = (delta^1_i, ..., delta^k_i) in F_p^k.
A d-dimensional realization with coefficient set S (0 in S) consists of class-constant
"base" realizers Phi_j : L -> S (j = 1..d, h_j := sum_ell Phi_j(ell) w_ell) and, for every
alpha in F_p^d minus 0, a vector gamma_alpha in F_p^k such that

      y_alpha(ell) := <alpha, Phi(ell)> + <gamma_alpha, ell>   lies in S for all ell in L.

Then sum_ell y_alpha(ell) w_ell = alpha . h, because sum_ell <gamma, ell> w_ell = 0 is a
combination of the k dependencies.  Nondegeneracy: for each alpha != 0, y_alpha != 0 as a
vector on L (then either h_1..h_d are independent, or some nonzero S-vector realizes 0 and
is itself a nontrivial solution).  Class-constancy is WLOG for feasibility: the constraint
at a column depends only on its label (see the note, Lemma 2).

This is the exact analogue of the pass's "pattern-set feasibility" (2026-11-08-rees-sde-p3.md,
Theorem 5) for general p and S.  Solver: z3.  Every SAT model is re-verified by brute force.

Usage: gadget_sat.py p S k d L [--nondeg] [--quiet]
  S:  'pow:KAPPA'  -> kappa-th powers and 0;  'int:K' -> {-K..K};  'set:a,b,c'
  L:  'all'        -> F_p^k minus 0
      'nest'       -> F_p^* x F_p^{k-1}     (delta^1 of full support, others inside it)
      'nest2'      -> F_p^* x F_p^* x F_p^{k-2}
      'cosets:c1,c2'  (k=1) -> delta^1 takes values in the listed P-cosets g^c P
      'file:PATH'  -> explicit list of labels
"""
import sys, itertools, argparse, time
import z3


def powers(p, kappa):
    return sorted({pow(x, kappa, p) for x in range(1, p)} | {0})


def coset_index(p, kappa):
    """cos: F_p^* -> Z_kappa using the least primitive root."""
    g = next(g for g in range(2, p) if len({pow(g, e, p) for e in range(p - 1)}) == p - 1) if p > 3 else 2
    ind = {pow(g, e, p): e for e in range(p - 1)}
    return {a: ind[a] % kappa for a in range(1, p)}, g


def parse_S(p, spec):
    kind, _, arg = spec.partition(':')
    if kind == 'pow':
        return powers(p, int(arg))
    if kind == 'int':
        K = int(arg)
        return sorted({x % p for x in range(-K, K + 1)})
    if kind == 'set':
        return sorted({int(x) % p for x in arg.split(',')})
    raise ValueError(spec)


def parse_L(p, k, spec):
    if spec == 'all':
        return [l for l in itertools.product(range(p), repeat=k) if any(l)]
    if spec == 'nest':
        return [l for l in itertools.product(range(p), repeat=k) if l[0] != 0]
    if spec == 'nest2':
        return [l for l in itertools.product(range(p), repeat=k) if l[0] != 0 and l[1] != 0]
    if spec.startswith('cosets:'):
        assert k == 1
        cs = {int(c) for c in spec[7:].split(',')}
        kappa = max(cs) + 1 if False else None
        raise ValueError('use file: for coset-restricted label sets')
    if spec.startswith('file:'):
        with open(spec[5:]) as f:
            return [tuple(int(x) for x in line.split()) for line in f if line.strip()]
    raise ValueError(spec)


def solve(p, S, k, d, L, nondeg=True, timeout_ms=None, extra=None):
    S = sorted(S)
    Sset = set(S)
    alphas = [a for a in itertools.product(range(p), repeat=d) if any(a)]
    s = z3.Solver()
    if timeout_ms:
        s.set('timeout', timeout_ms)
    Phi = {(l, j): z3.Int(f'phi_{"".join(map(str, l))}_{j}') for l in L for j in range(d)}
    for v in Phi.values():
        s.add(z3.Or([v == x for x in S]))
    unit = [tuple(1 if i == j else 0 for i in range(d)) for j in range(d)]
    gam = {}
    for a in alphas:
        if a in unit:
            continue
        gam[a] = [z3.Int(f'g_{"".join(map(str, a))}_{i}') for i in range(k)]
        for v in gam[a]:
            s.add(v >= 0, v < p)
    for a in alphas:
        nz = []
        for l in L:
            expr = sum(a[j] * Phi[(l, j)] for j in range(d))
            if a not in unit:
                expr = expr + sum(gam[a][i] * l[i] for i in range(k) if l[i])
            val = expr % p
            s.add(z3.Or([val == x for x in S]))
            nz.append(val != 0)
        if nondeg:
            s.add(z3.Or(nz))
    if extra:
        extra(s, Phi, gam)
    t0 = time.time()
    r = s.check()
    dt = time.time() - t0
    if r != z3.sat:
        return str(r), None, dt
    m = s.model()
    phi = {l: tuple(m[Phi[(l, j)]].as_long() for j in range(d)) for l in L}
    gamma = {a: tuple(m[v].as_long() for v in gam[a]) if a in gam else (0,) * k for a in alphas}
    # brute-force re-verification
    for a in alphas:
        anynz = False
        for l in L:
            y = (sum(a[j] * phi[l][j] for j in range(d)) + sum(gamma[a][i] * l[i] for i in range(k))) % p
            assert y in Sset, (a, l, y)
            anynz |= (y != 0)
        if nondeg:
            assert anynz, a
    return 'sat', (phi, gamma), dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int)
    ap.add_argument('S')
    ap.add_argument('k', type=int)
    ap.add_argument('d', type=int)
    ap.add_argument('L')
    ap.add_argument('--no-nondeg', action='store_true')
    ap.add_argument('--timeout', type=int, default=0, help='ms')
    ap.add_argument('--quiet', action='store_true')
    A = ap.parse_args()
    S = parse_S(A.p, A.S)
    L = parse_L(A.p, A.k, A.L)
    r, sol, dt = solve(A.p, S, A.k, A.d, L, nondeg=not A.no_nondeg, timeout_ms=A.timeout or None)
    print(f'p={A.p} S={S} k={A.k} d={A.d} L={A.L} (|L|={len(L)}) nondeg={not A.no_nondeg}: {r.upper()} [{dt:.1f}s]')
    if sol and not A.quiet:
        phi, gamma = sol
        print(' Phi (label -> base realizer values):')
        for l in L:
            print('  ', l, '->', phi[l])
        print(' gamma_alpha:')
        for a, g in gamma.items():
            print('  ', a, '->', g)


if __name__ == '__main__':
    main()
