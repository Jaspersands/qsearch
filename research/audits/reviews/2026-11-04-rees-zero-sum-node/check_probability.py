"""Exact checks of lem:fc-zero-sum(a) on small cases (exact Fractions).

[1] Pr[no nonempty zero-sum subset] for M i.i.d. uniform labels on F_p^a, by the sum-set dynamic
    programme of theorems/rees_zero_sum_node.py, against the bound (p^a-1)/(2^M-1), for
    p in {2,3,5,7}, a <= 3, M <= 6 (cases whose state count exceeds the cap are listed as skipped).
[2] Independent cross-check by full enumeration of all p^(aM) banks on the smallest cases:
    the same probability, E X and E X^2 against (2^M-1)p^-a and Var = N pi (1-pi).
[3] Pairwise independence: for every pair T != T' of nonempty subsets, (sum_T, sum_T') is
    uniform on (F_p^a)^2, by enumeration (p=3, a=1, M=3 and p=2, a=2, M=3; p=5, a=1, M=3).
[4] Davenport/Chevalley-Warning: probability exactly 0 once M >= a(p-1)+1, and the tight
    zero-sum-free example at M = a(p-1).
Run: nice -n 10 /opt/anaconda3/bin/python research/audits/reviews/2026-11-04-rees-zero-sum-node/check_probability.py
"""
import itertools
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from theorems import rees_zero_sum_node as z  # noqa: E402

out = {"exact_vs_bound": [], "enumeration": [], "pairwise": [], "davenport": [], "skipped": []}
ok = True
t0 = time.time()
for p in (2, 3, 5, 7):
    for a in (1, 2, 3):
        for M in range(1, 7):
            if p ** a > 130 or (p ** a > 50 and M > 5):
                out["skipped"].append([p, a, M])
                continue
            try:
                pr = z.exact_zero_sum_free_probability(p, a, M, max_states=2_000_000)
            except MemoryError as e:
                out["skipped"].append([p, a, M, str(e)])
                continue
            bd = z.second_moment_bound(p, a, M)
            good = pr <= bd
            dav = M >= a * (p - 1) + 1
            if dav:
                good = good and pr == 0
            ok &= good
            out["exact_vs_bound"].append(dict(p=p, a=a, M=M, prob=str(pr), prob_float=float(pr),
                                              bound=str(bd), bound_float=float(bd), ok=good,
                                              davenport_regime=dav))
            print(p, a, M, pr, float(pr), "<=", float(bd), good, f"{time.time()-t0:.0f}s", flush=True)

for p, a, M in ((2, 1, 4), (2, 2, 4), (3, 1, 5), (3, 2, 4), (5, 1, 4), (5, 2, 3), (7, 1, 3)):
    e1, e2, none = z.count_moments(p, a, M)
    pe1, pe2 = z.predicted_moments(p, a, M)
    dp = z.exact_zero_sum_free_probability(p, a, M)
    good = e1 == pe1 and e2 == pe2 and none == dp and none <= z.second_moment_bound(p, a, M)
    ok &= good
    out["enumeration"].append(dict(p=p, a=a, M=M, EX=str(e1), EX2=str(e2), prob=str(none), ok=good))
    print("enum", p, a, M, e1, e2, none, good, flush=True)

for p, a, M in ((3, 1, 3), (2, 2, 3), (5, 1, 3)):
    V = list(itertools.product(range(p), repeat=a))
    subsets = [T for k in range(1, M + 1) for T in itertools.combinations(range(M), k)]
    allgood = True
    for T, U in itertools.combinations(subsets, 2):
        cnt = {}
        for bank in itertools.product(V, repeat=M):
            sT = tuple(sum(bank[i][j] for i in T) % p for j in range(a))
            sU = tuple(sum(bank[i][j] for i in U) % p for j in range(a))
            cnt[(sT, sU)] = cnt.get((sT, sU), 0) + 1
        vals = set(cnt.values())
        allgood &= len(cnt) == p ** (2 * a) and len(vals) == 1
    ok &= allgood
    out["pairwise"].append(dict(p=p, a=a, M=M, pairs=len(subsets) * (len(subsets) - 1) // 2, uniform=allgood))
    print("pairwise", p, a, M, allgood, flush=True)

for p, a in ((3, 1), (3, 2), (5, 1), (5, 2), (7, 1), (2, 3)):
    M = a * (p - 1)
    bank = [tuple(int(j == i) for j in range(a)) for i in range(a) for _ in range(p - 1)]
    s_exh, _ = z.exhaustive_zero_sum(bank, p)
    s_dp, _ = z.dp_zero_sum(bank, p)
    tight = s_exh is None and s_dp is None and len(bank) == M
    ok &= tight
    out["davenport"].append(dict(p=p, a=a, zero_sum_free_example_columns=M, tight=tight))
    print("davenport tight example", p, a, M, tight, flush=True)

out["all_ok"] = ok
out["seconds"] = round(time.time() - t0, 1)
Path(__file__).with_name("check_probability_out.json").write_text(json.dumps(out, indent=1) + "\n")
print("ALL OK" if ok else "FAILURE", out["seconds"], "s; skipped", out["skipped"])
