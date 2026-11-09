"""Independent exhaustive check of Theorem B (U = 0, a circuit of q+1 random columns in F_p^q).
(i)  dim span(W_b) = E - 1 and sum_b W_b = e (= 0 here, U = 0);
(ii) R(S) intersected with Omega equals {sum beta_b W_b : Good(beta) nonempty};
(iii) at p not in E_cg(E, kappa) every coincidence-free beta is realised; at exceptional p report misses."""
import itertools
import random
import sys

import mybrt as mb


def run(p, k, q, E, trials, seed):
    rng = random.Random(seed)
    Fd = mb.Field(p, k)
    tab = {y: Fd.cos(y) for y in range(1, p)}
    Fd.cos = lambda y, tab=tab, p=p: tab[y % p]
    Sq = [0] + [y for y in range(1, p) if Fd.in_sq(y)]
    stats = dict(objs=0, dim_ok=0, ii_mism=0, iii_miss=0, iii_checked=0)
    while stats["objs"] < trials:
        cols = [[rng.randrange(p) for _ in range(q)] for _ in range(q + 1)]
        rels = mb.dependency(cols, p)
        if len(rels) != 1:
            continue
        delta = [rels[0].get(i, 0) for i in range(q + 1)]
        if not all(delta):
            continue
        bycls = {}
        for t in range(q + 1):
            bycls.setdefault(Fd.cos(delta[t]), []).append(t)
        if len(bycls) < 2 or E > q + 1 or len(bycls) > E:
            continue
        blocks, bcls = mb.split_blocks(bycls, E, rng, "random")
        W = [tuple(sum(delta[t] * cols[t][j] for t in G) % p for j in range(q)) for G in blocks]
        stats["objs"] += 1
        # (i)
        U = mb.Echelon(p, q)
        for w in W[1:]:
            if any(U.reduce(list(w))[0]):
                U.add(list(w))
        if U.nbasis == E - 1 and all(sum(w[j] for w in W) % p == 0 for j in range(q)):
            stats["dim_ok"] += 1
        # R(S) exhaustively
        R = set()
        for x in itertools.product(Sq, repeat=q + 1):
            R.add(tuple(sum(x[i] * cols[i][j] for i in range(q + 1)) % p for j in range(q)))
        # Omega points via beta with beta_0 = 0
        for beta in itertools.product(range(p), repeat=E - 1):
            beta = (0,) + beta
            pt = tuple(sum(b * w[j] for b, w in zip(beta, W)) % p for j in range(q))
            good = any(mb.good_ok(Fd, beta, bcls, s) for s in range(p))
            if good != (pt in R):
                stats["ii_mism"] += 1
            cf = all(beta[b] != beta[c] for b in range(E) for c in range(b + 1, E) if bcls[b] != bcls[c])
            if cf:
                stats["iii_checked"] += 1
                if not good:
                    stats["iii_miss"] += 1
    print(f"p={p} kappa={k} q={q} E={E}: {stats}", flush=True)


if __name__ == "__main__":
    for args in [(13, 2, 2, 3), (13, 2, 3, 3), (29, 2, 3, 4), (59, 2, 2, 3), (37, 3, 2, 3), (31, 3, 2, 3),
                 (271, 3, 2, 3), (241, 3, 2, 3), (61, 2, 3, 4), (59, 2, 3, 4)]:
        p, k, q, E = args
        run(p, k, q, E, trials=4 if p < 100 else 2, seed=p * 7 + q)
