"""Hill climbing / simulated annealing against Theorem A, strict asserts on throughout.

(A) INSTANCE climbs, n in NS: maximize m_needed of the deterministic WNEST (proof variant) over
    instances with m = ceil(closed_form(n)) columns.  Mutations: flip an entry, replace a column,
    duplicate / negate-duplicate a column into another slot, swap two columns (order attack),
    replace a column by a +-sum of two others (force weight-3 dependencies), copy an early block
    later.  Objective: m_needed, tie-break by total 2-dim piece cost.  Any assertion is recorded
    with the instance saved to FAIL_*.npy.  Starts: random, series-pairs, weight-2 lines.
(B) POOL climbs, q in QS, N = N(q): maximize the per-piece cost wt (= |X|) of the pool after
    peeling + Lemma D selection; the proof's cap is floor(2N/3 + (2/3) sqrt N).  Second objective:
    z = (wt - 2N*/3)/sigma (Lemma D says <= 1).  Third: number of peeling steps and the equality
    cases of the Delta invariant (classes of size exactly 3).
    Also reports the "empirical worst-case recursion": sum over stages q = n, n-2, ... of the
    climbed max wt(q), compared with guarantee(n).
"""
import math, sys, time, os
import numpy as np
from multiprocessing import Pool
from strict_wnest import StrictRun, Fail, solve_checked, guarantee, closed_form, pool_size, piece_cap, \
    peel_strict, pick_codeword_strict, rank, kernel

def eval_instance(n, vecs, variant="proof"):
    """returns (m_needed, total2cost, status, R)"""
    try:
        sol, R, err = solve_checked(n, vecs, variant, brute_var=False)
    except AssertionError as e:
        return None, None, "ASSERT " + str(e)[:300], None
    if err:
        return None, None, "EXHAUSTED " + err, None
    tot = sum(c[2] for c in R.costs if c[1] == 2)
    return R.m_needed, tot, "ok", R

def mutate_instance(vecs, n, rng):
    v = [x.copy() for x in vecs]
    m = len(v)
    kind = rng.integers(0, 7)
    i = int(rng.integers(0, m))
    if kind == 0:
        v[i][int(rng.integers(0, n))] = int(rng.integers(0, 3))
    elif kind == 1:
        v[i] = rng.integers(0, 3, n)
    elif kind == 2:
        j = int(rng.integers(0, m)); v[j] = (v[i] * int(rng.integers(1, 3))) % 3
    elif kind == 3:
        j = int(rng.integers(0, m)); v[i], v[j] = v[j], v[i]
    elif kind == 4:
        j, k = rng.integers(0, m, 2); v[i] = (int(rng.integers(1, 3)) * v[j] + int(rng.integers(1, 3)) * v[k]) % 3
    elif kind == 5:
        L = int(rng.integers(2, 12)); a = int(rng.integers(0, max(1, m - L))); b = int(rng.integers(0, max(1, m - L)))
        for t in range(L):
            v[b + t] = v[a + t].copy()
    else:
        for _ in range(3):
            v[int(rng.integers(0, m))][int(rng.integers(0, n))] = int(rng.integers(0, 3))
    return v

def start_instance(kind, n, m, rng):
    if kind == "random":
        return [rng.integers(0, 3, n) for _ in range(m)]
    if kind == "pairs":
        out = []
        while len(out) < m:
            x = rng.integers(0, 3, n); out += [x, x.copy()]
        return out[:m]
    if kind == "lines":
        out = []
        while len(out) < m:
            i, j = rng.choice(n, 2, replace=False); x = np.zeros(n, dtype=np.int64); x[i] = 1; x[j] = int(rng.integers(1, 3)); out.append(x)
        return out[:m]
    raise ValueError

def climb_instance(args):
    n, steps, kind, seed = args
    rng = np.random.default_rng(seed)
    m = math.ceil(closed_form(n))
    cur = start_instance(kind, n, m, rng)
    cur_val, cur_tot, st, _ = eval_instance(n, cur)
    assert st == "ok", st
    best = (cur_val, cur_tot); best_inst = cur
    fails = []
    T0 = 1.5
    for s in range(steps):
        cand = mutate_instance(cur, n, rng)
        val, tot, st, R = eval_instance(n, cand)
        if st != "ok":
            fails.append(st)
            np.save(f"FAIL_climb_n{n}_{kind}_{seed}_{s}.npy", np.array(cand))
            continue
        T = T0 * (1 - s / steps) + 1e-3
        d = (val - cur_val) + 0.01 * (tot - cur_tot)
        if d >= 0 or rng.random() < math.exp(d / T):
            cur, cur_val, cur_tot = cand, val, tot
            if (val, tot) > best:
                best, best_inst = (val, tot), cand
    return dict(n=n, kind=kind, seed=seed, steps=steps, best_needed=best[0], best_tot=best[1],
                guar=guarantee(n), closed=math.ceil(closed_form(n)), fails=fails[:5], nfails=len(fails))

# ------------------------------------------------------------------ pool climbs
def eval_pool(M):
    """M: q x N nonzero columns.  Returns dict with wt, cap, z, Nst, rst, trace or raises."""
    q, N = M.shape
    stats = {}
    idx, B, trace = peel_strict(M, stats)
    Nst = len(idx); rst = rank(M[:, idx])
    assert (2 * Nst - 3 * rst - 6) >= 0 and (2 * Nst - 3 * rst - 6) ** 2 >= 4 * Nst, "window premise"
    delta, wt, var27 = pick_codeword_strict(B)
    assert var27 <= 12 * Nst, "Var > 4N*/9"
    assert wt >= rst + 2, ("wt < r*+2", wt, rst)
    assert wt <= piece_cap(N), ("wt > cap", wt, piece_cap(N))
    sigma = math.sqrt(var27 / 27)
    z = (wt - 2 * Nst / 3) / sigma if sigma else 0.0
    Xloc = np.nonzero(delta)[0]
    BX = kernel(M[:, [idx[j] for j in Xloc]])
    assert BX.shape[0] >= 2, "dim D(X) < 2"
    return dict(wt=wt, cap=piece_cap(N), z=z, Nst=Nst, rst=rst, npeel=len(trace), trace=trace,
                slack=wt - (rst + 2), maxclass=stats.get("max_class", 0))

def mutate_pool(M, rng):
    M = M.copy(); q, N = M.shape
    kind = rng.integers(0, 6)
    j = int(rng.integers(0, N))
    if kind == 0:
        M[int(rng.integers(0, q)), j] = int(rng.integers(0, 3))
    elif kind == 1:
        M[:, j] = rng.integers(0, 3, q)
    elif kind == 2:
        i = int(rng.integers(0, N)); M[:, j] = (M[:, i] * int(rng.integers(1, 3))) % 3
    elif kind == 3:
        i, k = rng.integers(0, N, 2); M[:, j] = (int(rng.integers(1, 3)) * M[:, i] + int(rng.integers(1, 3)) * M[:, k]) % 3
    elif kind == 4:
        i = int(rng.integers(0, N)); M[:, [i, j]] = M[:, [j, i]]
    else:
        # sparse column
        M[:, j] = 0; M[int(rng.integers(0, q)), j] = int(rng.integers(1, 3))
        if rng.random() < 0.5: M[int(rng.integers(0, q)), j] = int(rng.integers(1, 3))
    for c in range(N):                      # keep columns nonzero (step 0 of WNEST handles zeros)
        if not np.any(M[:, c]):
            M[int(rng.integers(0, q)), c] = 1
    return M

def climb_pool(args):
    q, steps, objective, start, seed = args
    rng = np.random.default_rng(seed)
    N = pool_size(q)
    if start == "random":
        M = rng.integers(0, 3, (q, N))
    elif start == "pairs":
        M = rng.integers(0, 3, (q, N))
        for j in range(0, N - 1, 2):
            M[:, j + 1] = (M[:, j] * int(rng.integers(1, 3))) % 3
    elif start == "chain":
        M = np.zeros((q, N), dtype=np.int64)
        for j in range(N):
            M[j % q, j] = 1
            if j % q: M[(j % q) - 1, j] = 2
    for c in range(N):
        if not np.any(M[:, c]): M[0, c] = 1
    def obj(r):
        if objective == "wt": return r["wt"] + 0.001 * r["z"]
        if objective == "z": return r["z"] + 0.001 * r["wt"]
        if objective == "peel": return r["npeel"] + 0.001 * r["wt"]
    fails = []
    try:
        cur = eval_pool(M)
    except AssertionError as e:
        return dict(q=q, objective=objective, start=start, status="ASSERT at start " + str(e))
    cur_o = obj(cur); best = cur; best_M = M
    for s in range(steps):
        cand = mutate_pool(M, rng)
        try:
            r = eval_pool(cand)
        except AssertionError as e:
            fails.append(str(e)[:200]); np.save(f"FAIL_pool_q{q}_{objective}_{start}_{seed}_{s}.npy", cand); continue
        o = obj(r)
        T = 0.6 * (1 - s / steps) + 1e-3
        if o >= cur_o or rng.random() < math.exp((o - cur_o) / T):
            M, cur, cur_o = cand, r, o
            if obj(r) > obj(best):
                best, best_M = r, cand
    np.save(f"best_pool_q{q}_{objective}_{start}_{seed}.npy", best_M)
    return dict(q=q, N=N, objective=objective, start=start, steps=steps, best_wt=best["wt"], cap=best["cap"],
                best_z=round(best["z"], 4), Nst=best["Nst"], rst=best["rst"], slack=best["slack"], npeel=best["npeel"],
                trace=best["trace"][:8], maxclass=best["maxclass"], nfails=len(fails), fails=fails[:3])

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    t0 = time.time()
    if what in ("pool", "both"):
        tasks = []
        QS = [4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 30]
        for q in QS:
            steps = 3000 if q <= 16 else 1200
            for objective in ("wt", "z", "peel"):
                for start in ("random", "pairs", "chain"):
                    tasks.append((q, steps, objective, start, 1000 * q + hash((objective, start)) % 997))
        print(f"(B) pool climbs: {len(tasks)} tasks; per task steps as listed")
        print(" q   N  objective start   steps  best wt  cap   best z   N*  r*  wt-(r*+2)  npeel maxclass  fails  trace")
        best_wt_by_q = {}
        with Pool(workers) as P:
            for r in P.imap_unordered(climb_pool, tasks):
                if "status" in r:
                    print(r); continue
                best_wt_by_q[r["q"]] = max(best_wt_by_q.get(r["q"], 0), r["best_wt"])
                print(f"{r['q']:2d} {r['N']:3d}  {r['objective']:5s} {r['start']:7s} {r['steps']:5d}   {r['best_wt']:3d}    {r['cap']:3d}  {r['best_z']:7.4f}  {r['Nst']:3d} {r['rst']:3d}    {r['slack']:3d}       {r['npeel']:3d}    {r['maxclass']:3d}     {r['nfails']:3d}  {r['trace']}")
                sys.stdout.flush()
        print("\nclimbed max per-piece cost by q vs the proof's cap:")
        for q in sorted(best_wt_by_q):
            N = pool_size(q)
            print(f"  q={q:2d} N={N:3d} climbed max wt={best_wt_by_q[q]:3d}  cap={piece_cap(N):3d}  q+2={q + 2}")
    if what in ("inst", "both"):
        NS = [6, 8, 10, 12, 16, 20, 30]
        tasks = []
        for n in NS:
            steps = 1500 if n <= 12 else (800 if n <= 20 else 400)
            for kind in ("random", "pairs", "lines"):
                tasks.append((n, steps, kind, 7 * n + len(kind)))
        print(f"\n(A) instance climbs: {len(tasks)} tasks")
        print(" n  start   steps  best m_needed  guarantee(n)  closed form   best total 2-dim cost   fails")
        with Pool(workers) as P:
            for r in P.imap_unordered(climb_instance, tasks):
                print(f"{r['n']:2d}  {r['kind']:7s} {r['steps']:5d}     {r['best_needed']:5d}        {r['guar']:5d}        {r['closed']:5d}          {r['best_tot']:5d}            {r['nfails']}  {r['fails']}")
                sys.stdout.flush()
    print("total", round(time.time() - t0), "s")
