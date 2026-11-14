"""IS-free check for Schedule 1H+ at kappa <= 9 (2026-11-14, AI helper, pending human review).

Reuses the recursion helpers of the core-plus referee's plus_mine.py (written from the merged core
text; availability by its rcdfs DFS, re-checked certificates and the Lemma plus-sm thresholds).
Nothing is written outside this folder: plus_mine.main() is NOT called.

For every odd prime p < N and every kappa <= 9 dividing p-1 it computes, recursively,
  * the full schedule (candidate (a) = S1 present at every level)            -> (e^+, K^+)
  * the IS-free schedule (candidate (a) deleted at every level, inner too)    -> (e°, K°)
and checks
  A  the IS-free candidate list is nonempty                      (solver defined without IS)
  B  e° == e^+                                                   (per prime, not only the max)
  C  K° <= c_kappa = kappa^{kappa(kappa-1)ceil(log2(kappa+1))/2}  (C_c unchanged)
  D  dominance: some IS-free candidate Z (with IS-free inner solvers) has
       e_Z <= kappa*L  and  K_Z <= kappa^{kappa(kappa-1)L/2},  L = ceil(log2 t_{p,kappa}),
     so that arity_Z(a) <= K_Z (a+1)^{e_Z} <= G(kappa,a)^L = arity of (a) for every a >= 0;
     by induction on kappa this gives A°_kappa(a) = A^+_kappa(a) for all a.
Also E°(c), c = 2..9, and the attainers at c = 9.

usage: nice -n 19 python isfree_check.py N [tail]
  tail: instead, one prime p > 2e6 in each unit class mod 5040 (searches never needed there).
"""
import sys, os, math, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(os.path.dirname(HERE), '2026-11-14-rees-core-plus-referee')
sys.path.insert(0, REF)
import plus_mine as pm  # noqa: E402

FLAGS_FULL = dict(pm.VARIANTS['full'])
FLAGS_FREE = dict(pm.VARIANTS['noS1'])
DEGS = {}


def S1_pair(ctx, kappa):
    p = ctx.p
    if p >= 4 * kappa ** 4:
        t = 2 if ((p - 1) // kappa) % 2 == 0 else 3
    else:
        t = pm.t_value(ctx, kappa)
    L = math.ceil(math.log2(t))
    return kappa * L, kappa ** (kappa * (kappa - 1) * L // 2), t


def candidates(ctx, certs, tables_ok, flags, kappa, sol):
    """Copy of plus_mine.solve_prime's candidate list at one kappa, returning all candidates
    (degree, constant, label); identical logic, so that the two runs are comparable."""
    p = ctx.p
    big = p >= 4 * kappa ** 4
    cands = []
    if flags['S1']:
        e, K, t = S1_pair(ctx, kappa)
        cands.append((e, K, 'S1(t=%d)' % t))
    new = flags['new']
    if new and kappa in (3, 4, 5, 6) and (kappa != 6 or flags['TL6']):
        if pm.avail(ctx, kappa, tuple(range(kappa)), (0,), certs):
            cands.append((2, kappa - 1, 'TL%d' % kappa))
    if new and kappa == 9 and 3 in sol:
        if pm.avail(ctx, 9, (0, 3, 6), (0,), certs):
            cands.append((sol[3][0] + 1, sol[3][1] * 2, 'TW'))
    tb = new and flags['TB'] and p <= pm.TB_BOUND and (not flags['d28'] or p in pm.TIERB28)
    chs = pm.chains(ctx, kappa, sol, certs, flags) if tb else []
    for (Om, e, K, d) in chs:
        if Om == (0,):
            cands.append((e, K, 'TB:' + d))
    if new and flags['ELL'] and (p, kappa) in pm.FIVE and tables_ok[(p, kappa)]:
        ell = pm.FIVE[(p, kappa)][1]
        cands.append((ell, (kappa - 1) ** (ell * (ell - 1) // 2), 'L%d' % ell))
    nodes = []
    if kappa % 2 == 0:
        nodes.append((kappa // 2, sol[kappa // 2][0], sol[kappa // 2][1], 'H%d' % (kappa // 2)))
    if new and kappa == 7:
        order = list(range(1, 7))
        cu = certs.get('U', {}).get(p)
        if p > pm.DFS_TABLE_BOUND and cu is not None:
            mc = cu['K'][1]
            order = [mc] + [m for m in order if m != mc]
        for m in order:
            if pm.avail(ctx, 7, tuple(range(7)), (0, m), certs):
                nodes.append((m, 2, 6, 'U%d' % m))
                if p > pm.TB_BOUND and (big or all((u % 7) in pm.T_sets(ctx, 7, m)[1][0] for u in range(7))):
                    break
    if tb:
        for (Om, e, K, d) in chs:
            if len(Om) == 2:
                nodes.append((Om[1], e, K, 'TBn:' + d))
    fins = [(None, 0, 1, 'F0'), (tuple(range(kappa)), 1, 1, 'F1')]
    if new and flags['FOM']:
        for Dp in range(2, kappa):
            if kappa % Dp == 0:
                fins.append((tuple(range(0, kappa, Dp)), sol[Dp][0], sol[Dp][1], 'FH%d' % Dp))
    if tb:
        for (Om, e, K, d) in chs:
            fins.append((Om, e, K, 'FTB:' + d))
    for (m, eN, KN, dN) in nodes:
        if big:
            cands.append((eN + 1, KN, 'P(%s,1,F1)' % dN))
            continue
        T = pm.T_sets(ctx, kappa, m)
        for s in range(1, kappa + 2):
            cls, z = T[s]
            for (Om, eF, KF, dF) in fins:
                adm = z if Om is None else any(all(((u + k) % kappa) in cls for k in Om) for u in range(kappa))
                if adm:
                    cands.append((s * eN + eF, KN ** s * KF, 'P(%s,%d,%s)' % (dN, s, dF)))
    return cands


def solve(ctx, certs, tables_ok, flags, want_lists=False):
    p = ctx.p
    Np = math.gcd(p - 1, 2520)
    kappas = [k for k in range(1, 10) if Np % k == 0]
    sol = {1: (1, 1, 'GE')}
    lists = {}
    for kappa in kappas:
        if kappa == 1:
            continue
        c = candidates(ctx, certs, tables_ok, flags, kappa, sol)
        if not c:
            sol[kappa] = None
            lists[kappa] = []
            return sol, lists, kappa  # undefined solver
        e = min(x[0] for x in c)
        best = [x for x in c if x[0] == e]
        K = min(x[1] for x in best)
        lab = sorted(best, key=lambda x: (x[1], len(x[2])))[0][2]
        sol[kappa] = (e, K, lab)
        if want_lists:
            lists[kappa] = c
    return sol, lists, None


def primes_list(N, tail):
    if not tail:
        return [int(q) for q in pm.sieve(N) if q >= 3]
    out = []
    need = {r for r in range(5040) if math.gcd(r, 5040) == 1}
    q = 2_000_003
    from sympy import isprime
    while need:
        r = q % 5040
        if r in need and isprime(q):
            out.append(q); need.discard(r)
        q += 2
    return sorted(out)


def main():
    N = int(sys.argv[1]); tail = 'tail' in sys.argv[2:]
    t0 = time.time()
    certs = pm.load_certs()
    tables_ok = {}
    for (p, k), (f, ell) in pm.FIVE.items():
        ok, det = pm.verify_table(p, k, f, ell)
        tables_ok[(p, k)] = ok
        print('table', p, k, 'ok' if ok else 'FAIL', det, flush=True)
    dfs = pm.DFS()
    primes = primes_list(N, tail)
    print('primes:', len(primes), 'from', primes[0], 'to', primes[-1], 'tail' if tail else '', flush=True)
    bestF = {c: (0, []) for c in range(2, 10)}
    bestI = {c: (0, []) for c in range(2, 10)}
    failA, failB, failC, failD, failD1 = [], [], [], [], []
    dom_tight = {}   # kappa -> min over p of (K_S1 / K_Z) margin, logged
    n_pairs = 0
    s1_degopt_tie = []
    for p in primes:
        ctx = pm.Ctx(p, dfs)
        solF, _, _ = solve(ctx, certs, tables_ok, FLAGS_FULL)
        solI, listsI, undef = solve(ctx, certs, tables_ok, FLAGS_FREE, want_lists=True)
        if undef is not None:
            failA.append((p, undef)); continue
        for k in solI:
            if k == 1:
                continue
            DEGS['%d,%d' % (p, k)] = solI[k][0]
            n_pairs += 1
            eF, KF, _ = solF[k]; eI, KI, labI = solI[k]
            if eF != eI:
                failB.append((p, k, eF, eI))
            if KI > pm.cbound(k):
                failC.append((p, k, KI))
            eS, KS, t = S1_pair(ctx, k)
            if eS == eF:
                s1_degopt_tie.append((p, k))
            ok = [x for x in listsI[k] if x[0] <= eS and x[1] <= KS]
            if not ok:
                failD.append((p, k, eS, KS, sorted(listsI[k])[:3]))
            # D1: the same test against L = 1 (no zero-sum length used at all)
            if not [x for x in listsI[k] if x[0] <= k and x[1] <= k ** (k * (k - 1) // 2)]:
                failD1.append((p, k))
            else:
                r = max(KS / x[1] for x in ok)
                if k not in dom_tight or r < dom_tight[k][0]:
                    dom_tight[k] = (r, p, max(ok, key=lambda x: KS / x[1])[2])
        evF = [solF[math.gcd(d, p - 1)][0] for d in range(2, 10)]
        evI = [solI[math.gcd(d, p - 1)][0] for d in range(2, 10)]
        for best, ev in ((bestF, evF), (bestI, evI)):
            for c in range(2, 10):
                if p <= c:
                    continue
                v = 1 + sum(ev[:c - 1])
                if v > best[c][0]:
                    best[c] = (v, [p])
                elif v == best[c][0]:
                    best[c][1].append(p)
    print('== N', N, 'tail' if tail else '', 'time %.0fs' % (time.time() - t0))
    print('(p,kappa) pairs checked, kappa in 2..9:', n_pairs)
    for name, best in (('full', bestF), ('IS-free', bestI)):
        print(name, 'E(c), c=2..9:', [best[c][0] for c in range(2, 10)],
              '| c=9 attainers:', len(best[9][1]), 'non-2520:', [q for q in best[9][1] if (q - 1) % 2520])
    print('A  primes/kappa with NO IS-free candidate:', failA[:20], len(failA))
    print('B  per-(p,kappa) degree differences e^+ != e°:', failB[:20], len(failB))
    print('C  K° > c_kappa:', failC[:20], len(failC))
    print('D  dominance failures:', failD[:20], len(failD))
    print('D1 dominance failures with L = 1 (t-free):', failD1[:20], len(failD1))
    print('   pairs where S1 ties the least degree (info):', len(s1_degopt_tie), s1_degopt_tie[:20])
    print('   tightest dominance margin K_S1/K_Z per kappa (ratio, p, candidate):')
    for k in sorted(dom_tight):
        print('     kappa', k, '%.3g' % dom_tight[k][0], dom_tight[k][1], dom_tight[k][2])
    if not tail:
        json.dump(DEGS, open(os.path.join(HERE, 'degs_isfree_%d.json' % N), 'w'))
    print('STATS', pm.STATS, 'UNKNOWN', pm.UNKNOWN[:10], len(pm.UNKNOWN))


if __name__ == '__main__':
    main()
