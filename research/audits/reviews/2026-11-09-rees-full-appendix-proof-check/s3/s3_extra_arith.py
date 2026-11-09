#!/usr/bin/env python
"""s3 (9 Nov 2026 proof check): two small exact computations for the report.
 [1] Finding 6 (main.tex:784, "it supersedes that trial count"): compare the uniform per-node cap
     2B ln2 u^(u-1) + 1 of Thm free-coordinate(ii) with the per-grade cap 4 kappa^M B of part (iv),
     and the per-node count of (ii), 2B ln2 kappa^(u-1) + 1 (from ceil(2B ln2 q^-r), q >= 1/kappa,
     r <= u-1), with 4 kappa^M B.  ln 2 is bracketed by exact rationals.
 [2] Table tab:random-column-budget (numbers.tex Rc* macros): recompute the query and QFT caps from
     4m'(trees) * (leaves * n + sum_d nodes_d (M * 2 g_d + dim G_{d-1})) + m' * m, for profiles
     INFERRED from the printed numbers (the paper does not state them).  Consistency check only."""
from fractions import Fraction as Fr

LN2_LO, LN2_HI = Fr(693147, 10**6), Fr(693148, 10**6)
print("[1] uniform cap of (ii) vs per-grade cap of (iv), B = ceil(log2(64 (4u)^(c-1))) at c = u")
viol = []
for u in range(2, 41):
    M = 4 * u
    c = u
    B = 0
    while 2**B < 64 * (4*u)**(c-1): B += 1
    for kap in (1, 2, 3):
        if kap > u: continue
        ii_cap_lo = 2 * B * LN2_LO * u**(u-1) + 1        # lower bracket of the (ii) uniform cap
        iv_cap = 4 * kap**M * B
        node_ii_hi = 2 * B * LN2_HI * kap**(u-1) + 1      # upper bracket of the (ii) per-node count
        assert node_ii_hi <= iv_cap, (u, kap)            # node-by-node supersession always holds
        if ii_cap_lo > iv_cap: viol.append((u, kap))
print("  (u, kappa) with uniform (ii) cap > (iv) cap:", viol[:6], "...", f"{len(viol)} pairs for u <= 40")
u, kap, M = 20, 2, 80
print(f"  u=20, kappa=2: (ii) cap / B = {float(2*LN2_LO*u**(u-1)):.4g} vs (iv) cap / B = {float(4*kap**M):.4g}")
print("  per-node count of (ii) <= 4 kappa^M B: holds for all u <= 40, kappa <= 3")

print("[2] Table tab:random-column-budget, inferred profiles")
def caps(p, M, m, g, eps_bits=4):
    c = len(g)                  # g = (g_1, ..., g_c), g_1 = m
    mp = m + eps_bits           # m' = m + ceil(log2 9) at eps = 1/3
    trees = 4 * mp
    n = sum(g)
    leaves = M**(c-1)
    per_tree = leaves * n
    for d in range(2, c+1):
        nodes = M**(d-2)
        per_tree += nodes * (M * 2 * g[d-1] + sum(g[:d-1]))
    qft = trees * per_tree + mp * m
    queries = trees * c * leaves
    return trees, leaves, queries, qft
rows = [("case 0", 101, 8, 3, (3, 1), dict(trees=28, leaves=8, queries=448, qft=1449)),
        ("case 1", 1009, 16, 6, (6, 3, 1), dict(trees=40, leaves=256, queries=30720, qft=132780)),
        ("case 2", 65537, 48, 13, (13,) + tuple(range(11, 0, -1)), dict(trees=68, queries="2.6e21", qft="1.8e22"))]
for name, p, M, m, g, paper in rows:
    trees, leaves, queries, qft = caps(p, M, m, g)
    u = M // 4
    print(f"  {name}: p={p} >= 16u^2={16*u*u} [{p >= 16*u*u}], c={len(g)} <= u={u} [{len(g) <= u}], "
          f"trees={trees}, leaves/tree={leaves}, queries={queries if queries < 10**12 else format(queries, ".4g")}, QFT={qft if qft < 10**12 else format(qft, ".4g")}; paper {paper}")
c3 = 40 * 5 * 24**4
print(f"  case 3: 40 trees * c=5 * 24^4 = {c3} (paper 66355200) [{c3 == 66355200}]; 577 >= 16*36 = 576 [{577 >= 576}]")
