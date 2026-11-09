"""Exact decision of d = 2 feasibility for k = 2 dependencies, nested labels F_p^* x F_p (or all
labels), coefficient set S with stabiliser P = {lambda : lambda S = S} of index kappa, by DFS.

Coset reduction (Lemma R): WLOG gamma_{lambda alpha} = lambda gamma_alpha for lambda in P, so
the free data are gamma_{r_c alpha_d} in F_p^2 for the p+1 projective directions d (rep alpha_d)
and the kappa coset reps r_c (r_0 = 1), minus gamma = 0 at the two unit directions, coset 0.
Write gamma_{d,c} = (x_{d,c}, y_{d,c}).  For a label l = (a, b) the constraint on
phi = Phi(l) in S^2 is:  for all d, c:  r_c <alpha_d, phi> + a x_{d,c} + b y_{d,c}  in S.
The good set of tuples is P-invariant, so only labels (r_c, b) [and (0, r_c) for 'all'] matter.
DFS: first x over the labels (r_c, 0), then y over the labels (r_c, b), b != 0, pruning when some
label has no admissible phi.  Nondegeneracy (weak, per direction) is checked at the leaves by
a cover search.  Every solution found is re-verified over all alpha by gadget_cnf.verify.

CLI: p S L [--count] [--limit N]      (S as in gadget_sat; L in {nest, all})
"""
import sys, itertools, time, argparse
from gadget_sat import parse_S, parse_L
from gadget_cnf import verify
from gadget_cnf3 import cosets


def run(p, S, Lspec, count=False, limit=1, verbose=True):
    S = sorted(S); Sset = set(S)
    P, creps = cosets(p, S)
    kappa = len(creps)
    dirs = [(1, t) for t in range(p)] + [(0, 1)]
    phis = list(itertools.product(S, repeat=2))
    nphi = len(phis)
    full = (1 << nphi) - 1
    # allowed[d][c][u] = bitmask of phi with r_c <alpha_d, phi> + u in S
    allowed = [[[0] * p for _ in range(kappa)] for _ in dirs]
    zero_mask = [[[0] * p for _ in range(kappa)] for _ in dirs]   # phi with r_c<alpha,phi> + u == 0
    for di, a in enumerate(dirs):
        for ci, r in enumerate(creps):
            for u in range(p):
                m = z = 0
                for pi, phi in enumerate(phis):
                    val = (r * (a[0] * phi[0] + a[1] * phi[1]) + u) % p
                    if val in Sset:
                        m |= 1 << pi
                        if val == 0:
                            z |= 1 << pi
                allowed[di][ci][u] = m
                zero_mask[di][ci][u] = z
    slots = [(di, ci) for di in range(len(dirs)) for ci in range(kappa)]
    fixed = {(di, ci): (0, 0) for di, ci in slots if ci == 0 and dirs[di] in ((1, 0), (0, 1))}
    free = [s for s in slots if s not in fixed]
    # labels up to P-scaling
    xlabels = [(r, 0) for r in creps]                      # tuple = a*x
    ylabels = [(r, b) for r in creps for b in range(1, p)]  # tuple = a*x + b*y
    if Lspec == 'all':
        ylabels += [(0, r) for r in creps]
    sols = []
    nodes = [0]
    t0 = time.time()

    def label_mask(a, b, x, y, upto):
        m = full
        for (di, ci) in slots[:upto]:
            if (di, ci) in fixed:
                xv, yv = 0, 0
            else:
                xv, yv = x[(di, ci)], y.get((di, ci), 0)
            m &= allowed[di][ci][(a * xv + b * yv) % p]
            if not m:
                return 0
        return m

    def nondeg_and_record(x, y):
        # survivors per label (all labels, all a) and per-direction nondegeneracy cover
        gam = {}
        for (di, ci) in slots:
            a = dirs[di]; r = creps[ci]
            ar = tuple((r * v) % p for v in a)
            gam[ar] = (0, 0) if (di, ci) in fixed else (x[(di, ci)], y[(di, ci)])
        L = parse_L(p, 2, Lspec)
        surv = {}
        for (a, b) in L:
            m = full
            for (di, ci) in slots:
                xv, yv = gam[tuple((creps[ci] * v) % p for v in dirs[di])]
                m &= allowed[di][ci][(a * xv + b * yv) % p]
            if not m:
                return False
            surv[(a, b)] = m
        # direction di is nondegenerate at label l with phi iff some coset slot value != 0
        ndirs = len(dirs)
        options = []  # per label: list of direction-bitmasks achievable
        for (a, b), m in surv.items():
            opts = set()
            for pi in range(nphi):
                if not m >> pi & 1:
                    continue
                dm = 0
                for di in range(ndirs):
                    nz = False
                    for ci in range(kappa):
                        xv, yv = gam[tuple((creps[ci] * v) % p for v in dirs[di])]
                        if not zero_mask[di][ci][(a * xv + b * yv) % p] >> pi & 1:
                            nz = True
                    if nz:
                        dm |= 1 << di
                opts.add(dm)
            options.append(opts)
        reach = {0}
        for opts in options:
            reach = {r | o for r in reach for o in opts}
        if (1 << ndirs) - 1 not in reach:
            return False
        # choose Phi per label achieving the cover (greedy reconstruction) and verify over all alpha
        target = (1 << ndirs) - 1
        Phi = {}
        # backtrack over labels for a cover
        labels = list(surv)
        def pick(i, have):
            if i == len(labels):
                return have == target
            l = labels[i]
            m = surv[l]
            for pi in range(nphi):
                if not m >> pi & 1:
                    continue
                a, b = l
                dm = 0
                for di in range(ndirs):
                    for ci in range(kappa):
                        xv, yv = gam[tuple((creps[ci] * v) % p for v in dirs[di])]
                        if not zero_mask[di][ci][(a * xv + b * yv) % p] >> pi & 1:
                            dm |= 1 << di
                Phi[l] = phis[pi]
                if pick(i + 1, have | dm):
                    return True
            return False
        assert pick(0, 0)
        gamma = {}
        for ar, gv in gam.items():
            for lam in P:
                gamma[tuple((lam * v) % p for v in ar)] = tuple((lam * v) % p for v in gv)
        ok, why = verify(p, S, 2, 2, L, Phi, gamma, nondeg=True, weak=True)
        assert ok, why
        sols.append((dict(Phi), gamma))
        return True

    # joint DFS: per free slot choose (x, y) in F_p^2; masks for all labels pruned incrementally
    labels_red = xlabels + ylabels
    lab_cnt = len(labels_red)

    def dfs(i, x, y, masks):
        if len(sols) >= limit and not count:
            return
        if i == len(free):
            nondeg_and_record(x, y)
            return
        di, ci = free[i]
        al = allowed[di][ci]
        for xv in range(p):
            for yv in range(p):
                nodes[0] += 1
                nm = []
                ok = True
                for (a, b), m in zip(labels_red, masks):
                    m2 = m & al[(a * xv + b * yv) % p]
                    if not m2:
                        ok = False
                        break
                    nm.append(m2)
                if ok:
                    x[(di, ci)] = xv; y[(di, ci)] = yv
                    dfs(i + 1, x, y, nm)
                    del x[(di, ci)]; del y[(di, ci)]

    masks0 = []
    for (a, b) in labels_red:
        m = full
        for (di, ci) in fixed:
            m &= allowed[di][ci][0]
        masks0.append(m)
    dfs(0, {}, {}, masks0)
    dt = time.time() - t0
    if verbose:
        print(f'p={p} S={S} P={P} kappa={kappa} L={Lspec}: {"SAT" if sols else "UNSAT"}; solutions found={len(sols)} nodes={nodes[0]} [{dt:.1f}s]', flush=True)
    return sols


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('L')
    ap.add_argument('--count', action='store_true'); ap.add_argument('--limit', type=int, default=1)
    ap.add_argument('--show', action='store_true')
    A = ap.parse_args()
    S = parse_S(A.p, A.S)
    sols = run(A.p, S, A.L, count=A.count, limit=A.limit)
    if sols and A.show:
        Phi, gamma = sols[0]
        for l in sorted(Phi): print('  ', l, '->', Phi[l])
        for a in sorted(gamma): print('  ', a, '->', gamma[a])
