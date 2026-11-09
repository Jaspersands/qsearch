"""Hill climb over SINGLE pools (q x N(q) column matrices, q in 8..14): maximize the Lemma D
weight minus (r* + 2) after peeling, i.e. try to push the realized piece cost toward the cap
2N/3 + 2 sqrt(N)/3.  Lemmas M and D force wt - (r*+2) <= (4/3) sqrt(N*) whenever N* - 1.5 r* is
at its minimum 3 + sqrt(N*); any violation of the asserted bounds refutes Theorem A.
Also climbs toward pools with many size-2 series classes (variance 4N*/9 attained) by seeding
with duplicated-column pools."""
import math, sys
import numpy as np
from wnest import pool_size, peel, pick_codeword, rank, series_class_sizes

def piece_stats(M):
    idx, B = peel(M)
    Nst, rst = len(idx), rank(M[:, idx])
    delta, wt, sigma = pick_codeword(B)
    return wt, rst, Nst, sigma, max(series_class_sizes(B))

rng = np.random.default_rng(3)
print(" q   N   start        max wt-(r*+2)   max wt   cap 2N/3+2sqrtN/3   max sigma   (4/3)sqrt(N)   N* range")
for q in (8, 10, 12, 14):
    N = pool_size(q)
    cap = 2 * N / 3 + 2 * math.sqrt(N) / 3
    for start in ("random", "duplicates"):
        if start == "random":
            cur = rng.integers(0, 3, (q, N))
        else:
            half = rng.integers(0, 3, (q, (N + 1) // 2))
            cur = np.hstack([half, half])[:, :N]
        def score(M):
            if not np.all(np.any(M, axis=0)):
                return -10 ** 6, None
            wt, rst, Nst, sigma, mcl = piece_stats(M)
            assert wt >= rst + 2 and wt <= cap + 1e-9
            return wt - (rst + 2), (wt, rst, Nst, sigma, mcl)
        cur_s, cur_info = score(cur)
        best_s, best_wt, best_sig, Nsts = cur_s, cur_info[0], cur_info[3], {cur_info[2]}
        for it in range(600):
            cand = cur.copy()
            for _ in range(rng.integers(1, 4)):
                cand[rng.integers(0, q), rng.integers(0, N)] = rng.integers(0, 3)
            s, info = score(cand)
            if info is None:
                continue
            Nsts.add(info[2])
            if s >= cur_s:
                cur, cur_s, cur_info = cand, s, info
                if s > best_s:
                    best_s, best_wt, best_sig = s, info[0], info[3]
        print(f"{q:2d}  {N:3d}  {start:10s}   {best_s:6d}          {best_wt:4d}    {cap:7.2f}            {best_sig:5.2f}       {(4/3)*math.sqrt(N):5.2f}      {min(Nsts)}..{max(Nsts)}")
        sys.stdout.flush()
print("no assert fired: wt >= r*+2 and wt <= 2N/3 + 2 sqrt(N)/3 on every pool visited")
