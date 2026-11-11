"""Planar classification (k = d = 2, kappa = 2): which unions of full lines through 0 in F_p^2
are 2-feasible (weak nondegeneracy)?  One representative per PGL_2(F_p)-orbit of line sets.
Decided by btc (C port of bt.py) (independent backtracking; SAT answers verified, UNSAT [computed]).
Usage: lines_classify.py p [max_lines] [node_limit]
"""
import itertools, sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btc_run import decide_c


def proj_points(p):
    return [(1, x) for x in range(p)] + [(0, 1)]


def canon(p, pts):
    return tuple(sorted(pts))


def act(p, M, pt):
    a, b = pt
    x, y = (M[0] * a + M[1] * b) % p, (M[2] * a + M[3] * b) % p
    if x:
        inv = pow(x, -1, p)
        return (1, (y * inv) % p)
    return (0, 1)


def orbit_reps(p, m):
    pts = proj_points(p)
    G = [M for M in itertools.product(range(p), repeat=4) if (M[0] * M[3] - M[1] * M[2]) % p
         and next(x for x in M if x) == 1]   # PGL_2: one matrix per scalar class
    seen, reps = set(), []
    for sub in itertools.combinations(pts, m):
        key = tuple(sorted(sub))
        if key in seen:
            continue
        orb = set()
        for M in G:
            orb.add(tuple(sorted(act(p, M, q) for q in sub)))
        seen |= orb
        reps.append((key, len(orb)))
    return reps


def lineset_labels(p, lines):
    return [tuple((t * x) % p for x in u) for u in lines for t in range(1, p)]


if __name__ == '__main__':
    p = int(sys.argv[1])
    mmax = int(sys.argv[2]) if len(sys.argv) > 2 else p + 1
    lim = int(sys.argv[3]) if len(sys.argv) > 3 else None
    print(f'p={p} kappa=2 k=2 d=2: unions of m full lines, one per PGL_2 orbit', flush=True)
    for m in range(2, mmax + 1):
        for lines, osz in orbit_reps(p, m):
            L = lineset_labels(p, lines)
            t0 = time.time()
            r, nodes, sol = decide_c(p, 2, 2, 2, L, node_limit=lim or 0)
            dt = time.time() - t0
            print(f'm={m} lines={lines} orbit={osz}: {r} nodes={nodes} {dt:.1f}s', flush=True)
