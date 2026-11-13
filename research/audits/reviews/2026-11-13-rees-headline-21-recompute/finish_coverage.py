"""Coverage test for lem:stage2 objects + lem:finishK at s = 1: draw random groups until the
stage node returns J != empty (an object of type (1, eps)), collect n_F such objects on disjoint
column sets, run the finish of the plan and check the kappa-solution from scratch."""
import random, sys
from executor import Ctx, make_solver, StagePlan, check_solution, lincomb, _SOLVERS, STATS
from rc import RCSearch
from plus import PlusDegrees
S = RCSearch("rc_cache.json"); P = PlusDegrees(S)
for job in sys.argv[1:]:
    p, k, a, reps = map(int, job.split(":"))
    ctx = Ctx(p, S, P); _SOLVERS.clear(); sol = make_solver(ctx, k)
    assert isinstance(sol, StagePlan) and sol.s == 1, (p, k)
    rng = random.Random(p * 31 + k); AN = sol.N.arity(a); nF = sol.nF(a); ok = 0; tries = 0
    for rep in range(reps):
        objs, cols = [], []
        while len(objs) < nF:
            grp = [[rng.randrange(p) for _ in range(a)] for _ in range(AN)]; tries += 1
            x = sol.N.run(grp, a)
            I = [nu for nu in range(AN) if x[nu] and ctx.cl(x[nu], k) == 0]
            J = [nu for nu in range(AN) if x[nu] and ctx.cl(x[nu], k) == sol.m]
            if not J: continue
            base = len(cols); cols += grp
            u = lincomb(ctx, [x[nu] for nu in I], [grp[nu] for nu in I], a)
            qi = ctx.inv(sol.q)
            r1 = {base + nu: (x[nu], ctx.root(x[nu], k)) for nu in I}
            r2 = {base + nu: (x[nu] * qi % p, ctx.root(x[nu] * qi % p, k)) for nu in J}
            objs.append((u, [r1, r2]))
        # finish exactly as StagePlan.run does after level s
        eta = sol.Kn.run([o[0] for o in objs], a)
        u0 = next(u for u in range(k) if all((u + x) % k in sol.Tcls(2) for x in sol.Kset))
        from executor import realize
        xu = pow(ctx.g, u0, p); w = [0] * len(cols); r = [0] * len(cols)
        for nu, o in enumerate(objs):
            if not eta[nu]: continue
            y = realize(ctx, k, sol.eps, 1, xu * eta[nu] % p); assert y is not None
            for b, (wb, rb) in sol.combine(o, y).items(): assert w[b] == 0; w[b], r[b] = wb, rb
        check_solution(ctx, k, cols, w, r, a); ok += 1
    print(f"p={p} k={k} a={a} finish {sol.fin[0]} K={sorted(sol.Kset) if sol.fin[0]=='FK' else None}: {ok}/{reps} OK, stage tries {tries}")
