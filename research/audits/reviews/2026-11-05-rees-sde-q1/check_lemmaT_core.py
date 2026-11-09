"""Exact test of the linear-algebra core of Lemma T, with arbitrary functionals: V = F_p^r,
U a hyperplane, Y_in < U, X a set of n vectors outside U with Y_in + span X = V, beta in X.
For every nonzero functional theta on U vanishing on Y_in, the pairs {a,b} in X-{beta} with
theta = 0 on (Y_in + span(X - {a,b})) cap U and on e_ab number at most one.
Exhaustive over theta for small p (all of (U/Y_in)^*).  Usage: check_lemmaT_core.py seed reps"""
import sys
import random
from itertools import combinations, product
from q1core import solve_in_span, rank

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
reps = int(sys.argv[2]) if len(sys.argv) > 2 else 50
rng = random.Random(seed)
viol = 0
tot_bad = 0
cases = 0
maxbad = 0
for p in (3, 5, 7, 11):
    for _ in range(reps):
        r = rng.randrange(3, 6)
        # U = {x_r = 0}; Y_in spanned by y random vectors in U
        yb = rng.randrange(0, r - 1)
        Y = [[rng.randrange(p) for _ in range(r - 1)] + [0] for _ in range(yb)]
        ydim = rank(Y, p)[0]
        n = rng.randrange(3, 7)
        X = []
        for _ in range(n):
            v = [rng.randrange(p) for _ in range(r - 1)] + [rng.randrange(1, p)]
            if rng.random() < 0.3 and X:          # repeated directions / parallel classes
                w = rng.choice(X)
                c = rng.randrange(1, p)
                v = [c * t % p for t in w]
            X.append(v)
        if rank(Y + X, p)[0] < r:
            continue
        beta = X[0]
        rest = list(range(1, n))
        d = {i: [(X[i][t] - X[i][-1] * pow(beta[-1], p - 2, p) * beta[t]) % p for t in range(r)]
             for i in rest}
        # enumerate all functionals theta on U = F_p^{r-1} (last coordinate 0) vanishing on Y
        for th in product(range(p), repeat=r - 1):
            if not any(th):
                continue
            th = list(th) + [0]
            val = lambda v: sum(a * b for a, b in zip(th, v)) % p
            if any(val(y) for y in Y):
                continue
            cases += 1
            bad = 0
            for a1, a2 in combinations(rest, 2):
                # e_ab in U: X[a1] + mu X[a2] with last coordinate 0
                mu = (-X[a1][-1] * pow(X[a2][-1], p - 2, p)) % p
                e = [(x + mu * y) % p for x, y in zip(X[a1], X[a2])]
                others = [i for i in rest if i not in (a1, a2)]
                if any(val(d[i]) for i in others):
                    continue
                if val(e):
                    continue
                bad += 1
            tot_bad += bad
            maxbad = max(maxbad, bad)
            viol += bad > 1
print("functionals tested", cases, "total bad pairs", tot_bad, "max bad per functional", maxbad,
      "violations", viol)
