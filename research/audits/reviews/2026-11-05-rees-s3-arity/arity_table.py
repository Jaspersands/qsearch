"""Exact arity comparison at the zero-sum grade d = p-1 (report section P.5).

Columns (log2 of the arity unless stated):
  doubling  : expected reads N_0(g) of the weight-doubling solver (exact, rational recursion)
  node      : fixed arity of the node of node.py at abort probability tau
  sched1    : B_{p-1}(g) = [(p-1)^{(p-1)(p-2)/2} (g+1)^{p-1}]^{ceil(log2 p)}  (Schedule 1 at d=p-1)
  kmosw_avg : p^{p^2} g^{1+floor((p+3)/4)}  (KMOSW Thm 1.10, cited, NEEDS HUMAN VERIFICATION)
  kmosw_wc  : p^{p^2} (g+1)^{p-1}           (KMOSW Thm 1.11, cited, NEEDS HUMAN VERIFICATION)
  davenport : g(p-1)+1 (existence, worst case; reachable-sum search costs p^g)
Also the exponents of g: ours 1+ceil(log2(p-1)), KMOSW avg 1+floor((p+3)/4), KMOSW wc p-1,
Schedule 1 (p-1)ceil(log2 p).
Usage: /opt/anaconda3/bin/python arity_table.py OUT.json
"""
import json
import math
import sys

from doubling import covering_time, expected_consumption, jstar_of
from node import node_arity


def log2B(p, g):
    e = math.ceil(math.log2(p))
    return e * (((p - 1) * (p - 2) / 2) * math.log2(p - 1) + (p - 1) * math.log2(g + 1))


def main():
    out = sys.argv[1]
    rows, expo = [], []
    for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 61, 127, 257]:
        expo.append({"p": p, "c": p - 1, "ours": 1 + jstar_of(p),
                     "kmosw_avg": 1 + (p + 3) // 4, "kmosw_wc": p - 1,
                     "schedule1": (p - 1) * math.ceil(math.log2(p))})
    for p in [3, 5, 7, 11, 13, 17]:
        sp = covering_time(p)
        for g in [8, 16, 32, 64]:
            N = float(expected_consumption(p, g, sp))
            M, t, L, k = node_arity(p, g, 1e-3, sp)
            rows.append({"p": p, "g": g, "s_p": float(sp),
                         "log2_doubling": math.log2(N), "log2_node_tau1e-3": math.log2(M),
                         "log2_sched1": log2B(p, g),
                         "log2_kmosw_avg": p * p * math.log2(p) + (1 + (p + 3) // 4) * math.log2(g),
                         "log2_kmosw_wc": p * p * math.log2(p) + (p - 1) * math.log2(g + 1),
                         "davenport": g * (p - 1) + 1, "log2_reachable_states": g * math.log2(p)})
    with open(out, "w") as f:
        json.dump({"exponents": expo, "rows": rows}, f, indent=1)
    for r in expo:
        print(r)
    for r in rows:
        print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    main()
