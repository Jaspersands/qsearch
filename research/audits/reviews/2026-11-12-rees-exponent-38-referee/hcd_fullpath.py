"""Count top-level runs of hcd_executor that reach the finish (no early exit at top level)."""
import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import hcd_executor as H
orig_rep = H.represent
def run(p, kappa, a, reps=6):
    ctx = H.Ctx(p); rng = random.Random(7)
    n = H.arity_of(ctx, kappa, a); full = ok = tot = 0
    for _ in range(reps):
        for name, lams in H.banks(ctx, kappa, a, n, rng):
            st = {'early': 0}
            # top-level early exit <=> the returned support lies in one stage group of size N_D
            out = H.to_list(H.solve(ctx, kappa, lams, st), n)
            tot += 1; ok += H.verify(ctx, kappa, lams, out)
            ND = H.arity_of(ctx, kappa // 2, a)
            sup = [b for b in range(n) if out[b]]
            if len({b // ND for b in sup}) > 1: full += 1
    return p, kappa, a, n, f'{ok}/{tot}', 'multi-group supports (finish reached):', full
for args in [(41, 8, 1), (2521, 8, 1), (2521, 8, 2), (13, 4, 2), (17, 8, 1), (73, 8, 1), (2521, 4, 2)]:
    print(run(*args), flush=True)
