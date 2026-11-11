"""Numerical check of Lemma V and Lemma 1 on SAT models found by btc:
 (V) y_alpha(l) = 0 whenever <Delta_alpha, l> = 0, Delta_alpha = gamma_{r alpha} - r gamma_alpha;
 (V') for each full line u in L: K_u = {0} u {alpha : <Delta_alpha,u> = 0} is a subspace of codim <= 1;
 (K) global kernel {alpha: y_alpha = 0 on L} is 0 (the model is weakly nondegenerate)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btc_run import decide_c
from bt import setup, pclosure, named


def lines_labels(p, lines):
    return [tuple((t * x) % p for x in u) for u in lines for t in range(1, p)]


def check(p, k, d, L, name):
    ctx = setup(p, 2, k, d)
    r = next(x for x in range(2, p) if x not in ctx['P'])
    res, nodes, sol = decide_c(p, 2, k, d, L)
    assert res == 'SAT', res
    Phi, gamma = sol
    Lc = pclosure(p, ctx['P'], L)
    y = lambda a, l: (sum(a[j] * Phi[l][j] for j in range(d)) + sum(gamma[a][i] * l[i] for i in range(k))) % p
    alphas = [a for a in itertools.product(range(p), repeat=d) if any(a)]
    badV = 0
    for a in alphas:
        ra = tuple((r * x) % p for x in a)
        D = tuple((gamma[ra][i] - r * gamma[a][i]) % p for i in range(k))
        for l in Lc:
            if sum(D[i] * l[i] for i in range(k)) % p == 0 and y(a, l) != 0:
                badV += 1
    # full lines in Lc
    Ls = set(Lc); fl = []
    for l in Lc:
        lead = next(x for x in l if x); u = tuple((x * pow(lead, -1, p)) % p for x in l)
        if u not in fl and all(tuple((t * x) % p for x in u) in Ls for t in range(1, p)):
            fl.append(u)
    badK = 0; codims = []
    for u in fl:
        Ku = [a for a in alphas if all(y(a, tuple((t * x) % p for x in u)) == 0 for t in range(1, p))]
        KuD = [a for a in alphas if sum((gamma[tuple((r * x) % p for x in a)][i] - r * gamma[a][i]) * u[i] for i in range(k)) % p == 0]
        if set(Ku) != set(KuD):
            badK += 1
        size = len(Ku) + 1
        dim = {p ** j: j for j in range(d + 1)}.get(size)
        if dim is None:
            badK += 1
        else:
            codims.append(d - dim)
    glob = [a for a in alphas if all(y(a, l) == 0 for l in Lc)]
    print(f'{name}: p={p} k={k} d={d} |L|={len(Lc)} full lines={len(fl)}: LemmaV violations={badV}, '
          f'K_u mismatches/non-subspaces={badK}, codim K_u values={sorted(set(codims))}, global kernel size={len(glob)}', flush=True)
    assert badV == 0 and badK == 0 and not glob and max(codims, default=0) <= 1


if __name__ == '__main__':
    check(5, 2, 2, named(5, 2, 'all'), 'F_5^2 full')
    check(5, 2, 2, named(5, 2, 'nest'), 'F_5^2 nested')
    check(7, 2, 2, lines_labels(7, [(1, 0), (1, 1), (1, 2)]), 'p7 3 lines')
    check(11, 2, 2, lines_labels(11, [(1, 0), (1, 1), (1, 2), (1, 3)]), 'p11 4 lines a')
    check(11, 2, 2, lines_labels(11, [(1, 0), (1, 1), (1, 2), (1, 5)]), 'p11 4 lines b')
    check(5, 3, 2, lines_labels(5, [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]), 'p5 k3 4 lines')
    check(7, 3, 2, lines_labels(7, [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 1, 1)]), 'p7 k3 5 lines')
    print('all checks passed')
