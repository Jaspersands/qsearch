"""Incremental swap search: q points in Fil4(F_5) whose differences cover many lines.

Output fil4_local_search.json. A set covering >= need lines at q = q_lb proves
that the exact optimum for that prior is q_lb (the union bound gives >= q_lb);
otherwise a set at q_lb + 1 proves q_min <= q_lb + 1. Every reported cover is
recomputed from scratch.
"""
import json
import random
import time
from collections import Counter
from pathlib import Path

import classical_lb as C

L = C.filiform4(5)
p, m = L.p, L.m
zero = (0,) * m
lines = {C.line_id(v, p) for v in L.elements() if v != zero}
central = {v for v in lines if all(L.br(v, e) == zero for e in C.units(m))}
els = L.elements()


def dl(x, y):
    return C.line_id(L.diff(x, y), p)


def search(q, allowed, need, budget, seed):
    rnd = random.Random(seed)
    t0 = time.time()
    best = (-1, None)
    while time.time() - t0 < budget:
        X = [zero] + rnd.sample([e for e in els if e != zero], q - 1)
        cnt = Counter(dl(X[i], X[j]) for i in range(q) for j in range(i + 1, q))
        cur = sum(1 for v in cnt if v in allowed)
        stall = 0
        while stall < 4 * q and cur < need and time.time() - t0 < budget:
            i = rnd.randrange(1, q)
            old = [dl(X[i], X[j]) if j > i else dl(X[j], X[i]) for j in range(q) if j != i]
            for v in old:
                cnt[v] -= 1
            base = sum(1 for v, c in cnt.items() if c > 0 and v in allowed)
            choice = None
            for c in rnd.sample(els, 80):
                if c in X:
                    continue
                new = [dl(c, X[j]) if j > i else dl(X[j], c) for j in range(q) if j != i]
                gain = len({v for v in new if v in allowed and cnt[v] <= 0})
                if base + gain > cur:
                    choice = (c, new, base + gain)
                    break
            if choice is None:
                for v in old:
                    cnt[v] += 1
                stall += 1
                continue
            c, new, val = choice
            X[i] = c
            for v in new:
                cnt[v] += 1
            cur, stall = val, 0
        if cur > best[0]:
            best = (cur, list(X))
        if best[0] >= need:
            break
    X = best[1]
    cov = len(C.diff_lines(L, X) & allowed)
    return cov, X


res = {}
for which, allowed in (("all", lines), ("noncentral", lines - central)):
    N = len(allowed)
    need = C.target_cov(N)
    q = C.q_union_bound(N)
    cov, X = search(q, allowed, need, 240, 11)
    entry = {"N": N, "q_lb": q, "need": need, "cov_at_q_lb": cov, "witness_q_lb": [list(x) for x in X]}
    if cov >= need:
        entry["q_min_exact"] = q
    else:
        cov1, X1 = search(q + 1, allowed, need, 120, 12)
        entry.update({"cov_at_q_lb_plus_1": cov1, "witness_q_lb_plus_1": [list(x) for x in X1],
                      "q_min_range": [q, q + 1] if cov1 >= need else [q, None]})
    res[which] = entry
    print(which, {k: v for k, v in entry.items() if not k.startswith("witness")}, flush=True)
Path(__file__).with_suffix(".json").write_text(json.dumps(res, indent=1) + "\n")
