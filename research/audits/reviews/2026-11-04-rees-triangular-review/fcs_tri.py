#!/usr/bin/env python
"""Preview only: the 'combined Q' column of tab:fcs-budget with every Schedule 2
grade's arity (g+1)((kappa-1)g+1) replaced by (g+1)(g+2)/2 (same guard).
Reads research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json."""
import json, math, os
from math import gcd
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
d = json.load(open(os.path.join(ROOT, "research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json")))
g = dict(zip(range(2, 11), d["profile"][1:]))  # profile (g_1..g_9); grades d=2..9 use g_d
c = d["class"]
for row in d["rows"]:
    p = int(eval(row["p"].replace("^", "**"))) if "^" in row["p"] else int(row["p"])
    S = row["combined"]["S"]
    ar = row["combined"]["arities"]
    Q_old = c * S
    Q_new = c * S
    kinds = []
    for dd in range(2, c + 1):
        kind, M = ar[str(dd)]
        M = int(M)
        k = gcd(dd, p - 1)
        if kind == "S2":
            assert M == (g[dd] + 1) * ((k - 1) * g[dd] + 1), (row["label"], dd, M)
            Mt = (g[dd] + 1) * (g[dd] + 2) // 2
        else:
            Mt = M
        kinds.append(kind)
        Q_old *= M
        Q_new *= Mt
    assert Q_old == int(row["exact"]["combined_Q"]), row["label"]
    print(f'p={row["label"]:>9}: kinds={kinds}  log2 Q: table {row["table"]["combined_Q"]}, '
          f'recomputed {math.log2(Q_old):.1f}, triangular {math.log2(Q_new):.1f}')
