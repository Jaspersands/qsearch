"""Side question (2026-11-14, AI helper): is grade kappa = 10 IS-free too?

Definition plus-schedule at kappa >= 10 has only candidate (a) (S1) and the plans with node (f1),
i.e. H^+_5 with m = 5, and finishes F0, F1.  For p >= 4*10^4 the plan (1,F1) is admissible by
Lemma two-term.  This script decides, for every prime p < 40000 with 10 | p-1, whether some plan
(s,F), 1 <= s <= 11, is admissible (0 in T_s for F0, T_s = all classes for F1), using the IS-free
inner solver H°_5 from isfree_check.solve, and compares the best plan with S1 (dominance test of
isfree_check: e <= 10 L and K <= 10^{45 L}).

usage: nice -n 19 python kappa10_check.py [PMAX=40000]
"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import isfree_check as ic  # noqa: E402
pm = ic.pm


def main():
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    certs = pm.load_certs()
    tables_ok = {}
    for (p, k), (f, ell) in pm.FIVE.items():
        tables_ok[(p, k)] = pm.verify_table(p, k, f, ell)[0]
    dfs = pm.DFS()
    noplan, nodom, degs = [], [], {}
    for p in [int(q) for q in pm.sieve(PMAX) if q % 10 == 1]:
        ctx = pm.Ctx(p, dfs)
        sol, _, undef = ic.solve(ctx, certs, tables_ok, ic.FLAGS_FREE)
        assert undef is None and 5 in sol
        e5, K5, _ = sol[5]
        T = pm.T_sets(ctx, 10, 5)
        cands = []
        for s in range(1, 12):
            cls, z = T[s]
            if z:
                cands.append((s * e5, K5 ** s, 'P(H5,%d,F0)' % s))
            if len(cls) == 10:
                cands.append((s * e5 + 1, K5 ** s, 'P(H5,%d,F1)' % s))
        h = (p - 1) // 10
        t = pm.t_value(ctx, 10)
        L = math.ceil(math.log2(t))
        eS, KS = 10 * L, 10 ** (45 * L)
        if not cands:
            noplan.append((p, h % 2, t)); continue
        e = min(c[0] for c in cands)
        degs[p] = (e, min(c[1] for c in cands if c[0] == e), h % 2, t, e5)
        if not any(c[0] <= eS and c[1] <= KS for c in cands):
            nodom.append((p, e, eS, sorted(cands)[:2]))
    print('primes p < %d with 10 | p-1:' % PMAX, len(degs) + len(noplan))
    print('no IS-free plan at kappa=10:', noplan, len(noplan))
    print('dominance by S1 fails (IS-free arity could exceed A^+ at large a):', nodom[:20], len(nodom))
    mx = max(v[0] for v in degs.values()) if degs else None
    print('max IS-free degree e°_10 below %d:' % PMAX, mx, [(p, v) for p, v in degs.items() if v[0] == mx][:10])
    hist = {}
    for v in degs.values():
        hist[v[0]] = hist.get(v[0], 0) + 1
    print('degree histogram:', dict(sorted(hist.items())))
    print('STATS', pm.STATS, 'UNKNOWN', len(pm.UNKNOWN))


if __name__ == '__main__':
    main()
