"""Planar classification with half-lines (k = d = 2, kappa = 2): P-closed label sets in F_p^2 \\ 0
with exactly m full lines (m = 2, 3 by default) and, on every other line, nothing or one of its
two P-classes.  One representative per GL_2(F_p)-orbit; decided by btc (SAT verified).
(Sets with >= 4 full lines at p = 7 contain a 4-line set and are infeasible by monotonicity.)
Usage: halflines_classify.py p [m_list] [node_limit]
"""
import itertools, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btc_run import decide_c
from bt import powers


def main():
    p = int(sys.argv[1])
    ms = [int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '2,3').split(',')]
    lim = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    P = powers(p, 2)
    r = next(x for x in range(2, p) if x not in P)
    pts = [(1, x) for x in range(p)] + [(0, 1)]
    def cls(v):   # P-class index of a nonzero vector: (point index, coset bit)
        a, b = v
        if a:
            lam = a; u = (1, (b * pow(a, -1, p)) % p)
        else:
            lam = b; u = (0, 1)
        return pts.index(u), 0 if lam in P else 1
    ncl = 2 * len(pts)
    def cid(v):
        i, c = cls(v); return 2 * i + c
    # group action on class ids via generators of GL_2(F_p)
    g0 = next(x for x in range(2, p) if all(pow(x, (p - 1) // q, p) != 1 for q in range(2, p) if (p - 1) % q == 0 and all(q % t for t in range(2, q))))
    gens = [(g0, 0, 0, 1), (p - 1, 1, p - 1, 0)]
    reps_v = {}
    for i, u in enumerate(pts):
        reps_v[2 * i] = u; reps_v[2 * i + 1] = tuple((r * x) % p for x in u)
    perms = []
    for M in gens:
        perm = []
        for c in range(ncl):
            a, b = reps_v[c]
            perm.append(cid(((M[0] * a + M[1] * b) % p, (M[2] * a + M[3] * b) % p)))
        perms.append(perm)
    # check group order via closure of permutations
    grp = {tuple(range(ncl))}; frontier = list(grp)
    while frontier:
        nf = []
        for g in frontier:
            for pm in perms:
                h = tuple(pm[g[c]] for c in range(ncl))
                if h not in grp:
                    grp.add(h); nf.append(h)
        frontier = nf
    print(f'p={p}: {ncl} P-classes; GL_2 acts on them as a group of order {len(grp)} '
          f'(expected {(p*p-1)*(p*p-p)//((p-1)//2)})', flush=True)
    grp = list(grp)
    nl = len(pts)
    for m in ms:
        seen = set(); orbits = []
        for full in itertools.combinations(range(nl), m):
            others = [i for i in range(nl) if i not in full]
            for choice in itertools.product((None, 0, 1), repeat=len(others)):
                s = set()
                for i in full:
                    s |= {2 * i, 2 * i + 1}
                for i, c in zip(others, choice):
                    if c is not None:
                        s.add(2 * i + c)
                key = frozenset(s)
                if key in seen:
                    continue
                orb = {frozenset(g[c] for c in key) for g in grp}
                seen |= orb
                orbits.append((sorted(key), len(orb)))
        print(f'm={m}: {len(orbits)} orbits', flush=True)
        tally = {}
        for key, osz in orbits:
            L = []
            for c in key:
                u = reps_v[c]
                L += [tuple((lam * x) % p for x in u) for lam in P]
            half = len(key) - 2 * m
            t0 = time.time()
            res, nodes, sol = decide_c(p, 2, 2, 2, L, node_limit=lim)
            tally.setdefault((half, res), 0); tally[(half, res)] += 1
            print(f'  m={m} halflines={half} classes={key} orbit={osz}: {res} nodes={nodes} {time.time()-t0:.1f}s', flush=True)
        print(f'm={m} summary (number of half-lines, verdict): count', flush=True)
        for kk in sorted(tally):
            print(f'   {kk}: {tally[kk]}', flush=True)


if __name__ == '__main__':
    main()
