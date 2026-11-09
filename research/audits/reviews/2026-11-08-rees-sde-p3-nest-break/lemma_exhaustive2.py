"""Exhaustive lemma checks up to equivalence.

Lemma P depends only on the matroid of the columns, so every q x N matrix of rank r is, up to
GL(q,3) and a column permutation, [I_r | A] with A in F_3^{r x (N-r)}.  Enumerating all A is a
COMPLETE check of Lemma P (and of the coloop rank drop) for that (r, N).  Done for all (r, N) with
1 <= r, r < N, r (N - r) <= 12  (3^12 = 531441 matrices each at the top).

Lemma D is stated for an arbitrary basis B of D; the algorithm uses the basis kernel() returns,
which after moving pivots first is [C | I_k].  Enumerating all C in F_3^{k x r} is a complete check
of Lemma D for the bases the algorithm can see (up to column order within the pivot / free blocks,
which Lemma D's statement does not depend on, and row order, which is fixed by the form).  Lemma M
is checked by brute force on each code (3^k codewords, k <= 7).  Done for all (k, r) with
k r <= 12, k <= 7, and codes with no coloop.  Also records the maximum ratio (wt - mu)^2 / Var and,
restricted to codes with all series classes <= 2, the maximum of wt - (r + 2) (the quantity that
must be >= 0 under the window premise; here the premise is usually false, we only record).
"""
import itertools, sys, time
import numpy as np
from strict_wnest import rank, kernel, series_classes, phi27, pick_codeword_strict, brute_variance27

def lemma_P_canonical():
    tot = 0; bad = 0
    for N in range(2, 14):
        for r in range(1, N):
            if r * (N - r) > 12:
                continue
            cnt = 0
            I = np.eye(r, dtype=np.int64)
            for entries in itertools.product(range(3), repeat=r * (N - r)):
                A = np.array(entries, dtype=np.int64).reshape(r, N - r)
                M = np.hstack([I, A])
                if any(not np.any(M[:, j]) for j in range(N)):
                    continue                        # zero columns are removed by step 0
                B = kernel(M)                       # k = N - r rows
                zero = [j for j in range(N) if not np.any(B[:, j])]
                idx = [j for j in range(N) if j not in set(zero)]
                if zero:
                    r2 = rank(M[:, idx]) if idx else 0
                    if r - r2 != len(zero):
                        bad += 1; print("  COLOOP DROP FAILURE", M.tolist())
                if idx:
                    sub = M[:, idx]; Bs = kernel(sub); rs = rank(sub)
                    for members in series_classes(Bs).values():
                        rest = [idx[j] for j in range(len(idx)) if j not in set(members)]
                        rr = rank(M[:, rest]) if rest else 0
                        if rs - rr != len(members) - 1:
                            bad += 1
                            if bad <= 5: print("  LEMMA P FAILURE", len(members), rs, rr, M.tolist())
                cnt += 1
            tot += cnt
            print(f"Lemma P canonical r={r} N={N}: {cnt} matrices, cumulative failures {bad}")
            sys.stdout.flush()
    print(f"Lemma P canonical total {tot} matrices, {bad} failures")

def lemma_MD_canonical():
    tot = 0; bad = 0; worst = 0.0; worst_at = None; worst_slack = -99; worst_slack_at = None
    for k in range(1, 8):
        for r in range(1, 13):
            if k * r > 12:
                continue
            N = k + r
            cnt = 0
            I = np.eye(k, dtype=np.int64)
            for entries in itertools.product(range(3), repeat=k * r):
                C = np.array(entries, dtype=np.int64).reshape(k, r)
                B = np.hstack([C, I])
                if any(not np.any(B[:, j]) for j in range(N)):
                    continue
                var27 = phi27(B, [])
                bv = brute_variance27(B)
                sizes = [len(c) for c in series_classes(B).values()]
                if var27 != bv or var27 != 6 * sum(a * a for a in sizes):
                    bad += 1
                    if bad <= 5: print("  LEMMA M FAILURE", var27, bv, sizes, B.tolist())
                    continue
                try:
                    delta, wt, v27 = pick_codeword_strict(B)
                except AssertionError as e:
                    bad += 1
                    if bad <= 5: print("  LEMMA D FAILURE", str(e)[:100], B.tolist())
                    continue
                ratio = 3 * (3 * wt - 2 * N) ** 2 / var27
                if ratio > worst:
                    worst, worst_at = ratio, (k, r, wt, N)
                if max(sizes) <= 2:
                    s = wt - (r + 2)
                    # record the minimum of wt - (r+2) for dual distance >= 3 codes
                    if worst_slack == -99 or s < worst_slack:
                        worst_slack, worst_slack_at = s, (k, r, wt, N)
                cnt += 1
            tot += cnt
            print(f"Lemma M+D canonical k={k} r={r} (N={N}): {cnt} bases, cumulative failures {bad}, max ratio so far {worst:.4f} at {worst_at}")
            sys.stdout.flush()
    print(f"Lemma M+D canonical total {tot} bases, {bad} failures; max (wt-mu)^2/Var = {worst:.4f} at (k,r,wt,N)={worst_at}; "
          f"min wt-(r+2) over dual-distance>=3 codes = {worst_slack} at {worst_slack_at}")

if __name__ == "__main__":
    t0 = time.time()
    lemma_MD_canonical()
    lemma_P_canonical()
    print("total", round(time.time() - t0), "s")
