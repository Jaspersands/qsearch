#!/opt/anaconda3/bin/python
r"""Finite falsifier for Lemmas stage/finish and Theorem halving of the core (2026-11-13; AI-run).

Executes the plan "s stages + finish F0/F1" of Schedule 1H at small (p, kappa) with a BRUTE-FORCE
inner solver for exponent D = kappa/2 (any total D-solver is allowed by Lemma stage), on random and
adversarial column banks, and checks the output: w in (P_kappa u 0)^M, w != 0, sum w_b lambda_b = 0,
r_b^kappa = w_b. Covers kappa = 6 (not executed by the 11-12 referee) and kappa = 4, 8.
It proves nothing for other parameters.
Run: nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-headline-38-applied/halving_executor.py
"""
import itertools
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run_cell(p, kappa, a, s, fin, n_banks, rng):
    D = kappa // 2
    h = (p - 1) // kappa
    P = sorted({pow(x, kappa, p) for x in range(1, p)})
    Pset = set(P)
    root = {}
    for x in range(1, p):
        root.setdefault(pow(x, kappa, p), x)
    PD = sorted({pow(x, D, p) for x in range(1, p)})
    q = next(x for x in PD if pow(x, h, p) == p - 1)
    eps = (-pow(q, p - 2, p)) % p
    inv = lambda x: pow(x, p - 2, p)
    # T_s with explicit representations: rep[s][eta] = tuple y of length 2^s (entries in P u 0), sum y_k c_k = eta
    c = [1]
    rep = {y: (y,) for y in P}  # T_0 = P, type (1)
    reps = [rep]
    types = [list(c)]
    for _ in range(s):
        newc = c + [eps * x % p for x in c]
        L = len(c)
        new = {}
        zero_tuple = (0,) * L
        for eta, y in rep.items():
            new.setdefault(eta, y + zero_tuple)
        for eta, y in rep.items():
            new.setdefault(eps * eta % p, zero_tuple + y)
        for e1, y1 in rep.items():
            for e2, y2 in rep.items():
                new.setdefault((e1 + eps * e2) % p, y1 + y2)
        for eta, y in new.items():
            assert sum(yk * ck for yk, ck in zip(y, newc)) % p == eta
        rep, c = new, newc
        reps.append(rep)
        types.append(list(c))
    Ts = set(rep)
    if fin == 'F0':
        assert 0 in Ts, "plan not admissible (F0)"
    else:
        assert all(x in Ts for x in range(1, p)), "plan not admissible (F1)"

    NIN = D * a + 1  # Chevalley--Warning: D*a+1 vectors always admit a nonzero D-power relation

    def inner(vecs):
        # brute-force D-solver: x in (P_D u 0)^N, x != 0, sum x_nu v_nu = 0
        choices = [0] + PD
        for _ in range(4000):  # random search first, so that mixed-class outputs (and the finish) occur
            x = [rng.choice(choices) for _ in vecs]
            if any(x) and all(sum(xi * v[j] for xi, v in zip(x, vecs)) % p == 0 for j in range(a)):
                return x
        for x in itertools.product(choices, repeat=len(vecs)):
            if not any(x): continue
            if all(sum(xi * v[j] for xi, v in zip(x, vecs)) % p == 0 for j in range(a)):
                return list(x)
        raise RuntimeError("Chevalley-Warning violated")

    NF = 1 if fin == 'F0' else a + 1
    M = NIN ** s * NF
    stats = {'ok': 0, 'early_solutions': 0, 'reached_finish': 0}
    for bank in range(n_banks):
        kind = bank % 5
        if kind == 0:
            lam = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
        elif kind == 1:   # one repeated column
            v = [rng.randrange(1, p) for _ in range(a)]
            lam = [list(v) for _ in range(M)]
        elif kind == 2:   # unit vectors in blocks (dead-bank style)
            lam = [[1 if j == (b // max(1, M // a)) % a else 0 for j in range(a)] for b in range(M)]
        elif kind == 3:   # columns from few P-classes times unit vectors
            lam = [[(rng.choice(P) * (1 if j == b % a else 0)) % p for j in range(a)] for b in range(M)]
        else:             # sparse random with zero columns
            lam = [[rng.randrange(p) if rng.random() < 0.5 else 0 for _ in range(a)] for _ in range(M)]
        # objects: (vector, [ (dict b -> weight) for each rep ])
        objs = [(lam[b], [{b: 1}]) for b in range(M)]
        solution = None
        for lev in range(s):
            nxt = []
            for g in range(0, len(objs), NIN):
                group = objs[g:g + NIN]
                x = inner([o[0] for o in group])
                I = [i for i, xi in enumerate(x) if xi and pow(xi, h, p) == 1]
                J = [i for i, xi in enumerate(x) if xi and pow(xi, h, p) == p - 1]
                assert len(I) + len(J) == sum(1 for xi in x if xi)
                if not J or not I:
                    S = I if I else J
                    scale = [x[i] if I else x[i] * inv(q) % p for i in range(len(x))]
                    w = {}
                    for i in S:
                        for b, wb in group[i][1][0].items():
                            w[b] = scale[i] * wb % p
                    solution = w
                    break
                u = [sum(x[i] * group[i][0][j] for i in I) % p for j in range(a)]
                newreps = []
                for side, idx in ((0, I), (1, J)):
                    for k in range(len(group[0][1])):
                        R = {}
                        for i in idx:
                            f = x[i] if side == 0 else x[i] * inv(q) % p
                            assert f in Pset
                            for b, wb in group[i][1][k].items():
                                R[b] = f * wb % p
                        newreps.append(R)
                nxt.append((u, newreps))
            if solution is not None:
                break
            objs = nxt
        if solution is None:
            stats['reached_finish'] += 1
            cc = types[s]
            if fin == 'F0':
                y = rep[0]
                o = objs[0]
                w = {}
                for k, yk in enumerate(y):
                    if yk:
                        for b, wb in o[1][k].items():
                            w[b] = yk * wb % p
                solution = w
            else:
                vecs = [o[0] for o in objs[:a + 1]]
                # Gaussian elimination: nonzero eta with sum eta_nu v_nu = 0 (brute force over F_p^{a+1})
                eta = None
                for e in itertools.product(range(p), repeat=a + 1):
                    if any(e) and all(sum(ei * v[j] for ei, v in zip(e, vecs)) % p == 0 for j in range(a)):
                        eta = e; break
                w = {}
                for nu, en in enumerate(eta):
                    if not en: continue
                    y = rep[en]
                    for k, yk in enumerate(y):
                        if yk:
                            for b, wb in objs[nu][1][k].items():
                                w[b] = yk * wb % p
                solution = w
        else:
            stats['early_solutions'] += 1
        # check
        assert solution and any(solution.values())
        assert all(wb in Pset for wb in solution.values())
        roots = {b: root[wb] for b, wb in solution.items()}
        assert all(pow(r, kappa, p) == solution[b] for b, r in roots.items())
        assert all(sum(wb * lam[b][j] for b, wb in solution.items()) % p == 0 for j in range(a))
        stats['ok'] += 1
    return {'p': p, 'kappa': kappa, 'a': a, 'plan': f'{s}x{fin}', 'arity_bruteforce_inner': M, **stats}


if __name__ == '__main__':
    rng = random.Random(20261113)
    cells = [(7, 6, 1, 3, 'F0'), (13, 6, 1, 2, 'F0'), (31, 6, 1, 2, 'F1'), (37, 6, 1, 1, 'F1'),
             (61, 6, 1, 1, 'F1'), (13, 4, 1, 2, 'F0'), (13, 4, 2, 2, 'F0'), (5, 4, 1, 2, 'F1'),
             (5, 4, 2, 2, 'F1'), (17, 4, 2, 1, 'F1'), (17, 8, 1, 2, 'F0'), (41, 8, 1, 2, 'F1'),
             (7, 2, 2, 1, 'F1'), (11, 2, 2, 1, 'F1'), (13, 2, 3, 1, 'F1'), (7, 6, 2, 3, 'F0')]
    out = []
    for cell in cells:
        r = run_cell(*cell, n_banks=25, rng=rng)
        print(r, flush=True)
        out.append(r)
    (HERE / 'halving_executor.json').write_text(json.dumps(out, indent=1) + '\n')
