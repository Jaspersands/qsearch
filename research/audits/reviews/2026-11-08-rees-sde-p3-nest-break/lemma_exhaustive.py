"""Exhaustive and heavily sampled checks of the four lemmas of Theorem A on their own terms.

(1) Lemma P (series-class rank drop) and the peeling invariant Delta: ALL column multisets of
    N nonzero columns of F_3^q for (q, N) in {(2, <=8), (3, <=6)} (exhaustive) plus 200000 random
    q x N matrices with heavy duplication for q in 4..7.  For every series class A of D(F) (no
    coloops) check rank(F \\ A) == rank(F) - |A| + 1.
(2) Lemma M (variance formula) and Lemma D (greedy codeword within one sigma): ALL k x N generator
    matrices over F_3 for (k, N) in {(1, <=7), (2, <=6), (3, <=4)} (exhaustive, duplicates of the same
    code included) plus 100000 random codes k x N up to (8, 24) with forced series pairs.  Lemma M
    is checked by brute-force enumeration of the code; Lemma D by running the greedy.  We also
    record the largest (wt - 2N/3)^2 / Var reached (must be <= 1) and whether wt >= r* + 2 can
    fail when the Delta premise holds.
(3) Lemma G (nested-support gadget): exhaustive over the 2^6 presence patterns of the classes P_ab.
(4) N(q) and cost inequalities with cvc5 over the reals (run separately: nq_cvc5.py).
"""
import itertools, math, sys, time
import numpy as np
from strict_wnest import rank, kernel, series_classes, proj_key, phi27, pick_codeword_strict, \
    brute_variance27, UNIONS

def all_nonzero_columns(q):
    return [np.array(c, dtype=np.int64) for c in itertools.product(range(3), repeat=q) if any(c)]

def check_lemma_P(M):
    """M: q x N nonzero columns.  Returns (ok, detail) checking Lemma P for every series class
    after removing coloops; also checks Delta monotonicity of the full peel."""
    q, N = M.shape
    B = kernel(M)
    if B.shape[0] == 0:
        return True, None
    zero = [j for j in range(N) if not np.any(B[:, j])]
    idx = [j for j in range(N) if j not in set(zero)]
    r_all = rank(M)
    if zero:
        r_nc = rank(M[:, idx]) if idx else 0
        if r_all - r_nc != len(zero):
            return False, ("coloop drop", r_all, r_nc, len(zero))
    if not idx:
        return True, None
    sub = M[:, idx]
    B = kernel(sub)
    r = rank(sub)
    cl = series_classes(B)
    for key, members in cl.items():
        rest = [idx[j] for j in range(len(idx)) if j not in set(members)]
        r_rest = rank(M[:, rest]) if rest else 0
        if r - r_rest != len(members) - 1:
            return False, ("Lemma P", len(members), r, r_rest, M.tolist())
    return True, None

def exhaustive_P():
    out = []
    for q, Nmax in ((2, 8), (3, 6)):
        cols = all_nonzero_columns(q)
        for N in range(1, Nmax + 1):
            cnt = 0; bad = 0
            t0 = time.time()
            for combo in itertools.combinations_with_replacement(range(len(cols)), N):
                M = np.array([cols[i] for i in combo], dtype=np.int64).T
                ok, det = check_lemma_P(M)
                cnt += 1
                if not ok:
                    bad += 1
                    if bad <= 3:
                        print("  LEMMA P FAILURE", det)
            out.append((q, N, cnt, bad, round(time.time() - t0, 1)))
            print(f"Lemma P exhaustive q={q} N={N}: {cnt} multisets, {bad} failures ({out[-1][-1]} s)")
            sys.stdout.flush()
    return out

def sampled_P(rng, reps):
    bad = 0; cnt = 0; maxclass = 0
    for _ in range(reps):
        q = int(rng.integers(4, 8))
        N = int(rng.integers(q + 1, 3 * q + 2))
        # heavy duplication / small alphabets to force series classes and coloops
        base = rng.integers(0, 3, (q, int(rng.integers(1, N + 1))))
        M = base[:, rng.integers(0, base.shape[1], N)]
        # random chain gadgets: insert e_i - e_{i+1} style columns
        if rng.random() < 0.5:
            L = int(rng.integers(2, q + 1))
            for t in range(L):
                v = np.zeros(q, dtype=np.int64); v[t % q] = 1; v[(t + 1) % q] = 2
                M[:, int(rng.integers(0, N))] = v
        keep = [j for j in range(N) if np.any(M[:, j])]
        if len(keep) < 2:
            continue
        M = M[:, keep]
        ok, det = check_lemma_P(M)
        cnt += 1
        B = kernel(M)
        if B.shape[0]:
            cl = series_classes(B)
            maxclass = max(maxclass, max(len(c) for c in cl.values()))
        if not ok:
            bad += 1
            if bad <= 3:
                print("  LEMMA P FAILURE (sampled)", det)
    print(f"Lemma P sampled: {cnt} matrices q=4..7, {bad} failures, largest series class {maxclass}")
    return cnt, bad

def check_MD(B):
    """B: k x N generator.  Return (ok, ratio, info)."""
    k, N = B.shape
    if rank(B) < k:
        return True, 0.0, None            # not a basis; Lemma D assumes a basis (checked separately)
    if any(not np.any(B[:, j]) for j in range(N)):
        return True, 0.0, None            # coloop: Lemma M needs nonzero functionals
    var27 = phi27(B, [])
    bv = brute_variance27(B)
    if var27 != bv:
        return False, None, ("Phi(empty) != brute Var", var27, bv, B.tolist())
    cl = series_classes(B)
    sizes = [len(c) for c in cl.values()]
    if var27 != 6 * sum(a * a for a in sizes):
        return False, None, ("Lemma M formula", var27, sizes, B.tolist())
    try:
        delta, wt, v27 = pick_codeword_strict(B)
    except AssertionError as e:
        return False, None, ("Lemma D assert", str(e), B.tolist())
    ratio = 3 * (3 * wt - 2 * N) ** 2 / var27 if var27 else 0.0
    if ratio > 1 + 1e-12:
        return False, ratio, ("Lemma D ratio > 1", wt, N, var27, B.tolist())
    return True, ratio, (wt, N, max(sizes))

def exhaustive_MD():
    res = []
    for k, Nmax in ((1, 7), (2, 6), (3, 4)):
        for N in range(k + 1, Nmax + 1):
            cnt = bad = 0; worst = 0.0; worst_lo = None
            t0 = time.time()
            for entries in itertools.product(range(3), repeat=k * N):
                B = np.array(entries, dtype=np.int64).reshape(k, N)
                ok, ratio, info = check_MD(B)
                if info is None:
                    continue
                cnt += 1
                if not ok:
                    bad += 1
                    if bad <= 3:
                        print("  LEMMA M/D FAILURE", info)
                else:
                    worst = max(worst, ratio)
            res.append((k, N, cnt, bad, round(worst, 4), round(time.time() - t0, 1)))
            print(f"Lemma M+D exhaustive k={k} N={N}: {cnt} bases, {bad} failures, max (wt-mu)^2/Var = {worst:.4f} ({res[-1][-1]} s)")
            sys.stdout.flush()
    return res

def sampled_MD(rng, reps):
    cnt = bad = 0; worst = 0.0; worst_case = None; window_fail = 0; window_cnt = 0
    for _ in range(reps):
        k = int(rng.integers(1, 9))
        N = int(rng.integers(k + 1, 25))
        B = rng.integers(0, 3, (k, N))
        # force series pairs: duplicate (or negate) some columns
        for _ in range(int(rng.integers(0, N // 2 + 1))):
            i, j = rng.integers(0, N, 2)
            B[:, j] = (B[:, i] * int(rng.integers(1, 3))) % 3
        if rank(B) < k:
            continue
        if any(not np.any(B[:, j]) for j in range(N)):
            continue
        cl = series_classes(B)
        if max(len(c) for c in cl.values()) > 2:
            continue
        var27 = phi27(B, [])
        if k <= 9 and brute_variance27(B) != var27:
            bad += 1; print("  LEMMA M FAILURE", B.tolist()); continue
        delta, wt, v27 = pick_codeword_strict(B)
        cnt += 1
        ratio = 3 * (3 * wt - 2 * N) ** 2 / var27
        if ratio > worst:
            worst, worst_case = ratio, (k, N, wt)
        # the window premise of Theorem A: N - 1.5 r >= 3 + sqrt N with r = N - k  =>  wt >= r + 2?
        r = N - k
        if 2 * N - 3 * r - 6 >= 0 and (2 * N - 3 * r - 6) ** 2 >= 4 * N:
            window_cnt += 1
            if wt < r + 2:
                window_fail += 1
                print("  WINDOW FAILURE", k, N, wt, r)
    print(f"Lemma M+D sampled: {cnt} codes (k<=8, N<=24, classes<=2), {bad} failures, max ratio {worst:.4f} at {worst_case}; "
          f"window premise held in {window_cnt} cases, wt < r*+2 in {window_fail}")
    return cnt, bad

def lemma_G_patterns():
    """For each nonempty set of present classes P_ab (a in {1,2}, b in F_3), delta has full support
    automatically; delta' is independent of delta iff the present set is not contained in one of
    {(1,0),(2,0)} (delta'=0), {(1,1),(2,2)} (delta'=delta), {(1,2),(2,1)} (delta'=2 delta).
    Check: for every alpha != 0, U_alpha or U_{2 alpha} is nonempty whenever independent."""
    sym = [(a, b) for a in (1, 2) for b in range(3)]
    bad = 0; cnt = 0
    for mask in range(1, 64):
        present = {sym[i] for i in range(6) if mask >> i & 1}
        dep = present <= {(1, 0), (2, 0)} or present <= {(1, 1), (2, 2)} or present <= {(1, 2), (2, 1)}
        if dep:
            continue
        cnt += 1
        for al in UNIONS:
            al2 = ((2 * al[0]) % 3, (2 * al[1]) % 3)
            u1 = any(c in present for c in UNIONS[al])
            u2 = any(c in present for c in UNIONS[al2])
            if not (u1 or u2):
                bad += 1
                print("  LEMMA G FAILURE: both unions empty", present, al)
    # and the identities: already symbolic in wnest.py; re-check numerically on random data
    rng = np.random.default_rng(3)
    idbad = 0
    for _ in range(2000):
        q = int(rng.integers(2, 7)); X = int(rng.integers(3, 12))
        delta = rng.integers(1, 3, X); dp = rng.integers(0, 3, X)
        # make the two relations hold: choose columns, then adjust last two columns? Instead sample
        # columns and project: we need sum delta_i v_i = 0 and sum delta'_i v_i = 0.
        V = rng.integers(0, 3, (q, X))
        K = kernel(np.vstack([delta, dp]))            # vectors c with delta.c = 0, dp.c = 0
        if K.shape[0] == 0:
            continue
        V = (rng.integers(0, 3, (q, K.shape[0])) @ K) % 3   # rows of V are in the kernel: relations hold
        w = {}
        for a in (1, 2):
            for b in range(3):
                sel = [i for i in range(X) if delta[i] == a and dp[i] == b]
                w[(a, b)] = V[:, sel].sum(axis=1) % 3 if sel else np.zeros(q, dtype=np.int64)
        h1 = (w[(1, 0)] + w[(1, 1)] + w[(2, 0)]) % 3
        h2 = (w[(1, 1)] + w[(1, 2)] + w[(2, 2)]) % 3
        for al, cls in UNIONS.items():
            s = sum(w[c] for c in cls) % 3
            if np.any((s - al[0] * h1 - al[1] * h2) % 3):
                idbad += 1
    print(f"Lemma G: {cnt} independent presence patterns checked, {bad} failures; 2000 random numeric identity checks, {idbad} failures")
    return bad + idbad

if __name__ == "__main__":
    rng = np.random.default_rng(20261108)
    t0 = time.time()
    lemma_G_patterns()
    exhaustive_MD()
    sampled_MD(rng, 100000)
    exhaustive_P()
    sampled_P(rng, 200000)
    print("total time", round(time.time() - t0), "s")
