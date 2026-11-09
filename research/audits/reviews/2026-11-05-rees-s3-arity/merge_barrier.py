"""Linear-sketch disjoint merging (LSDM: BKW, Wagner k-tree, coordinate-block recursion).

Companion of research/audits/reviews/2026-11-05-rees-s3-arity.md, section B1.

(1) real_bkw: pair-merge BKW on actual uniform columns in F_p^n with a fixed block schedule;
    the output is checked exactly.  Pair merging is optimal per stage for fan-in 2: keep every
    item whose block value is 0 and match value v with value -v.
(2) abstract_bkw: the same algorithm, simulated with item values only.  By Lemma B1.1 of the
    report, the block values of the current items are i.i.d. uniform given the past, so only
    their counts matter.  Used to find the least arity M at which BKW succeeds w.p. >= 1/2.
(3) lower bounds of Theorem B1: M * gamma^(-l) and n*M^F*p^(-b) + M*gamma^(-n/(b-1)).
(4) block_recursion_arity: deterministic Davenport-block recursion (an LSDM with unbounded
    fan-in), arity prod_j (b_j(p-1)+1), minimised over block sizes.

Usage: nice -n 10 /opt/anaconda3/bin/python merge_barrier.py OUT.json
"""
import json
import math
import sys
import time

import numpy as np


def pair_merge_stage(vals, p):
    """vals: list of value tuples of the current items (one per item).  Returns list of groups
    (lists of item positions) forming the next items: zero singletons, and pairs v, -v."""
    groups = []
    byval = {}
    for k, v in enumerate(vals):
        byval.setdefault(v, []).append(k)
    done = set()
    for v, ks in byval.items():
        if v in done:
            continue
        if not any(v):
            groups += [[k] for k in ks]
            done.add(v)
            continue
        w = tuple((-x) % p for x in v)
        ls = byval.get(w, [])
        for a, b in zip(ks, ls):
            groups.append([a, b])
        done.add(v)
        done.add(w)
    return groups


def real_bkw(p, n, M, blocks, rng):
    """Returns a zero-sum subset (checked) or None.  blocks: list of block sizes summing to n."""
    X = rng.integers(0, p, (M, n))
    items = [[i] for i in range(M)]
    sums = X.copy()
    lo = 0
    for b in blocks:
        vals = [tuple(int(x) for x in sums[k, lo:lo + b]) for k in range(len(items))]
        groups = pair_merge_stage(vals, p)
        if not groups:
            return None
        items = [sum((items[k] for k in g), []) for g in groups]
        sums = np.array([X[it].sum(axis=0) % p for it in items])
        lo += b
    T = items[0]
    assert len(set(T)) == len(T) and np.all(X[T].sum(axis=0) % p == 0)
    return T


def abstract_bkw_final_count(p, M, blocks, rng):
    """Number of final items, simulating block values as i.i.d. uniform (Lemma B1.1)."""
    N = M
    for b in blocks:
        if N == 0:
            return 0
        q = p ** b
        counts = rng.multinomial(N, np.full(q, 1.0 / q))
        # value index -> negation index (digits base p)
        digits = np.array(np.unravel_index(np.arange(q), [p] * b)).T
        neg = np.ravel_multi_index(((-digits) % p).T, [p] * b)
        Z = int(counts[0])
        pairs = int(sum(min(counts[v], counts[neg[v]]) for v in range(1, q)) // 2)
        N = Z + pairs
    return N


def schedule(n, b):
    bl = [b] * (n // b)
    if n % b:
        bl.append(n % b)
    return bl


def min_arity_bkw(p, n, rng, trials=60, target=0.5):
    """Least M (over power-of-2^(1/4) grid and uniform block sizes) with success >= target."""
    best = None
    for b in range(1, n + 1):
        if p ** b > 2 ** 14:
            break
        bl = schedule(n, b)
        M = 2
        cap = best[0] if best else 10 ** 9
        while M < cap:
            succ = sum(abstract_bkw_final_count(p, M, bl, rng) > 0 for _ in range(trials)) / trials
            if succ >= target:
                break
            M = int(math.ceil(M * 2 ** 0.25)) + 1
        if M < cap and (best is None or M < best[0]):
            best = (M, b)
    return best


def lower_bound_F2(p, n, delta=0.5, F=2):
    """Least M allowed by Theorem B1(ii): delta <= n M^F p^-b + M gamma^-(ceil(n/(b-1)))
    must hold for some integer b >= 2 (b = max block + 1)."""
    gamma = 2 * p / (p + 1)
    lo = 1.0
    M = 2.0
    while True:
        ok = False
        for b in range(2, n + 2):
            L = math.ceil(n / (b - 1))
            if n * M ** F * p ** (-b) + M * gamma ** (-L) >= delta:
                ok = True
                break
        if ok:
            return M
        M *= 1.05


def block_recursion_arity(p, n):
    """min over compositions into equal-ish blocks of prod (b_j (p-1) + 1) and max time p^b."""
    best = None
    for b in range(1, n + 1):
        bl = schedule(n, b)
        A = 1
        for x in bl:
            A *= x * (p - 1) + 1
        if best is None or A < best[0]:
            best = (A, b, p ** b)
    return best


def main():
    out = sys.argv[1]
    rng = np.random.default_rng(7)
    res = {"real_bkw": [], "stage_ratio": [], "min_arity": [], "block_recursion": []}
    t0 = time.time()
    # (1) real columns, exact checks
    for p, n, M, b in [(3, 8, 400, 2), (3, 12, 3000, 3), (5, 6, 2000, 2), (7, 6, 4000, 2)]:
        bl = schedule(n, b)
        s = 0
        R = 40
        for _ in range(R):
            T = real_bkw(p, n, M, bl, rng)
            s += T is not None
        res["real_bkw"].append({"p": p, "n": n, "M": M, "blocks": bl, "success": s, "of": R,
                                "bound_M_gamma^-l": min(1.0, M * ((p + 1) / (2 * p)) ** len(bl))})
    # (2) per-stage ratio E|F_j| / |F_{j-1}| vs (1 + p^-b)/2
    for p in [3, 5, 7]:
        for b in [1, 2, 3]:
            N = 20000
            r = np.mean([abstract_bkw_final_count(p, N, [b], rng) / N for _ in range(50)])
            res["stage_ratio"].append({"p": p, "b": b, "measured": r, "bound": (1 + p ** (-b)) / 2})
    # (3) least BKW arity vs n, and the Theorem B1(ii) lower bound
    for p, ns in [(3, [6, 9, 12, 16, 20, 25, 30, 36]), (5, [4, 6, 9, 12, 16, 20]),
                  (7, [4, 6, 9, 12, 16])]:
        for n in ns:
            if time.time() - t0 > 1200:
                break
            best = min_arity_bkw(p, n, rng)
            res["min_arity"].append({"p": p, "n": n, "least_M": best[0] if best else None,
                                     "block": best[1] if best else None,
                                     "lower_bound_thmB1ii": lower_bound_F2(p, n),
                                     "linear_existence_g_log2p": n * math.log2(p)})
            print(res["min_arity"][-1], flush=True)
            with open(out, "w") as f:
                json.dump(res, f, indent=1)
    # (4) deterministic block recursion
    for p in [3, 5, 7]:
        for n in [8, 16, 32, 64, 128]:
            A, b, tm = block_recursion_arity(p, n)
            res["block_recursion"].append({"p": p, "n": n, "arity": A, "log2_arity": math.log2(A),
                                           "block": b, "time_per_group_p^b": tm})
    res["seconds"] = time.time() - t0
    with open(out, "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
