"""Symbolic check of the nested-support gadget: the 8 identities y_alpha = alpha_1 h1 + alpha_2 h2
hold as linear identities in the six class sums w_(a,b), a in {1,2}, b in F_3, modulo the two
relations sum_a a w_ab = 0 and sum_b b w_ab = 0.  Also the general count: a 2-dim gain needs >= 2
independent dependencies inside span(y), and a one-dependency piece has <= 8 zero-one points."""
import itertools, numpy as np
T = [(a, b) for a in (1, 2) for b in range(3)]
idx = {t: i for i, t in enumerate(T)}
rel = np.array([[a for (a, b) in T], [b for (a, b) in T]]) % 3  # 2 x 6
gadget = {(0,1): [(1,1),(1,2),(2,2)], (0,2): [(1,2),(2,1),(2,2)], (1,0): [(1,0),(1,1),(2,0)],
          (1,1): [(1,0),(2,0),(2,1)], (1,2): T, (2,0): [(1,1),(2,0),(2,2)],
          (2,1): [(2,0),(2,1),(2,2)], (2,2): [(1,0),(1,2),(2,1)]}
def vec(classes):
    v = np.zeros(6, dtype=np.int64)
    for c in classes: v[idx[c]] = 1
    return v
h1, h2 = vec(gadget[(1,0)]), vec(gadget[(0,1)])
def in_rowspace(v):
    # v in row space of rel  <=> rank([rel; v]) == rank(rel) == 2
    from kow_p3 import rank3
    return rank3(np.vstack([rel, v])) == rank3(rel)
ok = True
for al, classes in gadget.items():
    diff = (vec(classes) - al[0] * h1 - al[1] * h2) % 3
    r = in_rowspace(diff); ok &= r
    print(f"alpha={al}: y_alpha - alpha.h in span(relations): {r}")
print("all eight identities hold modulo the two relations:", ok)
# h1, h2 independent modulo the relations (no a h1 + b h2 in rowspace for (a,b) != 0)
indep = all(not in_rowspace((a * h1 + b * h2) % 3) for a in range(3) for b in range(3) if (a, b) != (0, 0))
print("h1, h2 independent modulo the relations (so the realized subgroup is 2-dim whenever the class sums satisfy only these relations):", indep)
