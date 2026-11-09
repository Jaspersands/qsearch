"""Larger-sample check of the Theorem 2 failure bound at three parameter points."""
import random
from common import F
from legendre_reduction import class_table, build_instance, all_solutions_projective, recover_f, reveals_key, bound
rng = random.Random(99)
for kappa, p, k, trials in [(2, 1009, 14, 2000), (2, 1009, 16, 2000), (4, 1009, 9, 2000)]:
    Fd = F(p, kappa); tab = class_table(Fd); fail = 0
    for _ in range(trials):
        K = rng.randrange(p)
        inst = build_instance(Fd, K, k, 2, rng)
        if inst[0] == 'key':
            continue
        cols, u, c = inst
        sols = all_solutions_projective(Fd, cols, tab)
        fail += not all(reveals_key(Fd, recover_f(Fd, x, u, c, 2), K, 2) for x in sols)
    se = (bound(kappa, p, k) * (1 - min(1, bound(kappa, p, k))) / trials) ** 0.5
    print(f"kappa={kappa} p={p} k={k}: failure rate {fail/trials:.4f} over {trials}; union bound {bound(kappa,p,k):.4f} (binomial s.e. at the bound {se:.4f})", flush=True)
