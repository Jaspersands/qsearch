"""Negative controls: perturbed certificates must be caught (by check_rc and by the executor)."""
import json, random
from certs import check_rc, prim_root
import executor as X
C = json.load(open('certs_stage1.json')); rng = random.Random(3)
caught_chk = caught_exec = n = 0
for name, D, R in (('tower (9;{0,3,6})', 9, [0, 3, 6]), ('union (7;Z7->{0,m})', 7, list(range(7))), ('two-level 5', 5, list(range(5)))):
    ps = [p for p in C[name]['found'] if 2000 < int(p) < 20000][:10]
    for ps_ in ps:
        p = int(ps_); w = C[name]['found'][ps_]; al = list(w['alpha']); j = rng.randrange(1, D); al[j] = (al[j] + 1) % p
        be = {int(i): v for i, v in w['beta'].items()}; n += 1
        if not check_rc(p, prim_root(p), D, sorted(be), w['K'], al, be): caught_chk += 1
        ctx = X.Ctx(p, 9 if D == 9 else D)
        try:
            if D == 9:
                from certs import find_rc
                t3 = find_rc(p, 3, [0, 1, 2], [0]); s1 = (3, [0, 1, 2], {0}, t3[0], t3[1])
                steps = [s1, (9, [0, 3, 6], {0}, al, be)]
            else:
                steps = [(D, sorted(be), set(w['K']), al, be)]
            bad = False
            for rep in range(20):
                a = 2; A = X.arity(a, steps); lam = X.bank('uniform', A, a, p, rng)
                if D == 7: lam = X.bank('uniform', A * 3, a, p, rng); X.stage_finish_F1(ctx, lam, a, steps, w['K'][1])
                else: X.check_solution(ctx, X.chain(ctx, lam, list(range(A)), a, steps), lam, a)
        except AssertionError:
            bad = True
        caught_exec += bad
print('perturbed certificates', n, 'rejected by check_rc', caught_chk, 'caught by executor within 20 runs', caught_exec)
